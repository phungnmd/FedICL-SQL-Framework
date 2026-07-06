# FedICL-SQL — System Architecture

> Grounded in: `fig_architecture_source.png` (mechanism ground truth) · `fedicl_sql_outline.pdf` (section structure) · `DECISIONS.md` (spec + naming).
> Maps directly to §3 of the paper. **Fig.1 wins on any mechanism dispute.**
>
> **Re-aligned 2026-06-16:** teacher moved client-side (local 7B). Public X and ICL Hub G removed.
> **Re-aligned 2026-06-29:** KD mechanism replaced with KID (imperfect data distillation): teacher runs online per step (frozen, forward-only), student masks+rewrites gold SQL → ŷ, Reverse KL + alpha-decay loss. Offline annotation pipeline removed. (KID source = **[10]** Zhong et al. 2024.)
> **Re-aligned 2026-06-30:** goal restated — build a **Fed + ICL + KD** framework that maximizes EX on a *small* model; the target is `(FT/KD)+ICL > either alone`. The old "ICL is redundant on a fine-tuned student / never claim ICL improves FT" framing is **retired** — it described a `train-k=0` student tested at `k=3` (a train/test mismatch, not an ICL ceiling). Path to synergy = **in-context tuning** (`train-k=3` + `skeleton` demos) so the student learns to read demos; mismatch principle grounded in KID [10].
> **Re-aligned 2026-07-06 (review fixes):** (1) **both** KD directions distill on the public KD corpus (Struct-SQL traces generated on the public KD corpus, not `Qᵢ`) → no data confound in `kid − struct`; (2) `fedavg_pub` data-matched control added (CE on the public KD corpus gold, no teacher) → teacher value = `fedkd − fedavg_pub`; (3) **demo-style parity** locked: train `demo_style` == eval `demo_style` per arm (style-shift = separate experiment); (4) teacher ICL demos = the public KD corpus (TBD) always; (5) FedAvg weighted `nᵢ/n`; (6) λ₂ alpha-decay is global across rounds. Staged run plan: `KD_PLAN.md`.
> **Re-aligned 2026-07-06 (this session, training order):** local training is now **sequential, two-step**, not a combined per-step loss. **Step 1 — KD-pretrain on the public KD corpus** (Stream 2 content only: KID / Struct-SQL / SeqKD / gold-CE per arm) runs to completion first. **Step 2 — FT on `Qᵢ`** (gold CE, Stream 1) runs second, LoRA initialized from Step 1's adapter. The old `L = λ₁·L_FT + λ₂(t)·L_KD` combined-loss design (§5.6, §6, §8 below) is retired — see §5.6. Side benefit: Direction A (KID) only needs teacher+student co-loaded during Step 1; Step 2 is student-only (lighter HW).
> **Re-aligned 2026-07-07 — the public KD corpus (TBD) dropped, scope cut to a PoC:** the public KD corpus (TBD) is out entirely (too heavy, dialect gap). **No replacement public corpus is picked yet** — that's deferred. Every "the public KD corpus (TBD)" mention below (§5.2, §5.6, §6, §8, §9) describes the **full dual-stream method design**, which still applies mechanically once a corpus is chosen — read "the public KD corpus (TBD)" there as "the public KD corpus (TBD)". Right now, only a cheap **PoC runs**: on a Spider data slice, compare training it as plain FT vs as a KD signal (both directions), from the base model, no dual-stream mixing, no federation. See `KD_PLAN.md` §PoC for the runnable plan; the rest of this document is the deferred target architecture.

---

## 1. Problem Setting

A set of `K` organizations (clients) each hold:
- A **private relational database** with schema `Sᵢ = {tables, columns, FK-paths}` — never leaves the client.
- A **private NL→SQL example store** `Qᵢ = {(qₙ, sₙ)}` (natural-language questions + gold SQL) — never leaves the client.

**Goal:** collaboratively train a lightweight local SQL model that generalizes to unseen schemas, while transmitting only encrypted, DP-perturbed model weights — no raw data, no schema, no private SQL, no teacher outputs.

---

## 2. Three-Plane Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  FEDERATED COORDINATION SERVER  (Cloud)                             │
│                                                                     │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Federated Aggregation Engine                                  │ │
│  │  FedAvg / FedProx: θ_t ← θ_{t-1} + Σᵢ (nᵢ/n) Δθᵢ           │ │
│  │  → Global SLM M_G (Qwen2.5-1.5B + aggregated LoRA adapter)    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────┬──────────────────────────────┬─────────────────┘
                     │ ▼ DOWN (blue)                 │ ▲ UP (purple dashed)
                     │  Global params M_G            │  Encrypted LoRA deltas Δθᵢ
                     │  (no ICL Hub demos)           │  (Weights Only)
┌────────────────────▼──────────────────────────────┴─────────────────┐
│  SECURE & PRIVACY-PRESERVING COMMUNICATION                           │
│  SSL/TLS · Secure Aggregation · DP (gradient perturbation) · Masking│
└────────────────────┬──────────────────────────────┬─────────────────┘
                     │ ▼                             │ ▲
┌────────────────────▼──────────────────────────────┴─────────────────┐
│  CLIENT / ORGANIZATION i  (on-premise)                               │
│                                                                      │
│  [Local Data & Schema]──────────────────────────────────────────┐   │
│   Sᵢ (private schema)                                            │   │
│   Qᵢ (private NL/SQL)                                            │   │
│       │                                                          │   │
│       │   [Public KD-corpus train split (local copy) + KD-corpus demo pool]     │   │
│       │        ▼                                                 │   │
│  [Local Teacher M_T — Qwen2.5-7B-Instruct, frozen]              │   │
│   Runs ONLY on the public KD corpus — never on Qᵢ                        │   │
│   Dir A KID: online forward per step, scores ŷ_pub             │   │
│   Dir B Struct: offline QP-CoT traces, cached, exec-filtered    │   │
│                                                                  │   │
│  [Schema Encoder]──►[Retrieval (Qᵢ only)]──►[ICL Prompt]       │   │
│   BGE-small          FAISS top-k             σ(q,S,I,Q)         │   │
│                                                    │             │   │
│                             ┌──────────────────────▼──┐         │   │
│                             │  Local SLM Student Mᵢ   │         │   │
│                             │  Qwen2.5-1.5B + LoRA    │◄────────┘   │
│                             │  init from M_G each round│   gold SQL  │
│                             └──────────────┬──────────┘             │
│                                            │                        │
│  ┌─────────────────────────────────────────▼────────────────────┐   │
│  │  Local Training (two-step, sequential)                       │   │
│  │  Step 1: KD-pretrain on the public KD corpus (KID / Struct-SQL /...)  │   │
│  │  Step 2: FT (gold CE) on Qᵢ, LoRA init from Step-1 adapter   │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  → LoRA delta Δθᵢ → encrypt+compress+DP-perturb → upload            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Server Components

### 3.1 Federated Aggregation Engine

**Algorithm:** FedAvg / FedProx.

```
θ_t  ←  θ_{t-1}  +  Σᵢ (nᵢ/n) Δθᵢ      # nᵢ = |Qᵢ| — McMahan weighting, NOT 1/K
M_G  ←  base_SLM + θ_t                    # (non-IID α=0.1 → client sizes very unequal)
```

FedProx adds a proximal term `(μ/2)||θ - θ_{t-1}||²` per client to control drift under high non-IID (use if convergence is unstable).

**Uploads only LoRA deltas `Δθᵢ`** (not full weights) — bounded communication cost per round.

**LoRA-averaging caveat:** averaging `A`,`B` factors separately ≠ averaging products (`mean(BᵢAᵢ) ≠ mean(Bᵢ)·mean(Aᵢ)`) — known FedIT/FLoRA issue. Mitigated by re-initializing every client from the same `M_G` adapter each round; acknowledge with one sentence in the paper.

### 3.2 Global SLM `M_G`

Base `Qwen2.5-1.5B-Instruct` + aggregated LoRA adapter `θ_t`. Broadcast back to all clients at the start of each round. Lightweight enough to run locally at inference (<6 GB VRAM).

> **Removed:** Global LLM Teacher (`M_T`) and ICL Hub (`G`) are no longer server components. The teacher runs locally on each client on its own private Qᵢ.

---

## 4. Communication Band

| Direction | What crosses | Protected by |
|---|---|---|
| **DOWN** (server → client) | Global SLM params `M_G` | SSL/TLS + Secure Aggregation |
| **UP** (client → server) | LoRA delta `Δθᵢ` only (**Weights Only**) | Encrypt + compress + **DP gradient perturbation** + Secure Aggregation |
| **Never transmitted** | Raw rows, schema `Sᵢ`, private examples `Qᵢ`, teacher model, teacher outputs | Stays local by design |

**Privacy mechanisms (4 boxes):**
1. **SSL/TLS** — secure transmission channel
2. **Secure Aggregation** — server aggregates without seeing individual Δθᵢ
3. **Differential Privacy (Gradient Perturbation)** — Gaussian noise + clipping on Δθᵢ before upload; report (ε, EX) at Stage-B
4. **De-identification & no-schema demos** — retrieval embeddings use question text only (no schema/DDL); retrieved demos are shown as **question + verbatim SQL with NO source DDL** (`demo_style=never_schema`, default) so no foreign schema is ever placed in the prompt. Demo SQL comes from the client's own train pool (own identifiers, never transmitted). `skeleton` (identifier-masked SQL) = stronger-privacy ablation (RQ2). `full` removed 2026-06-20.

---

## 5. Client Components

### 5.1 Local Data & Schema (private, never leaves)

- `Sᵢ` — relational schema (tables, columns, types, FK paths)
- `Qᵢ` — NL/gold-SQL pairs on `Sᵢ`'s databases

### 5.2 Local Teacher M_T — Qwen2.5-7B-Instruct (online, frozen, runs on the public KD corpus)

Teacher runs **per KD-pretrain step (Step 1 only, see §5.6)** — one forward pass over imperfect student output `ŷ_pub` (generated from masked the corpus's gold SQL). Frozen throughout. **Never sees client's private `Qᵢ`.** Not loaded during Step 2 (FT on `Qᵢ`).

**Per-step role:** student masks the corpus's gold SQL `y_pub` → rewrites → `ŷ_pub`. Teacher computes `p = softmax(logits)` over `ŷ_pub` **with ICL context from the KD corpus's train demos** (k=3, question-only, `never_schema`). Teacher prompt = `P_ICL(x_pub, demos_pub)` + `ŷ_pub`.

**Why a public corpus for KD (reframed 2026-07-06):** primary reason = **shared public distillation corpus aligns client updates** — every client distills toward the same teacher behaviour on the same data → less FedAvg drift under non-IID (FedDF/FedMD line of argument). Secondary: the corpus is (ideally) cross-domain → SQL structural knowledge transfers cross-schema. This is **NOT a privacy argument** — the teacher is on-premise, so reading `Qᵢ` would leak nothing; "teacher never touches `Qᵢ`" is a clean systems property, not the motivation. Applies to **both KD directions** (KID online scoring AND Struct-SQL offline trace generation) so `kid − struct` has no data confound.

**What teacher does NOT do:**
- No autoregressive text generation
- No access to `Qᵢ` or client's private schema `Sᵢ`
- Never uploads outputs to server

**VRAM:** teacher (7B fp16 ≈ 14 GB) + student (1.5B fp16 ≈ 3 GB) **co-loaded simultaneously, Step 1 (KD-pretrain) only** — Direction A (KID) needs teacher+student together to score `ŷ_pub`. Requires A100 40 GB+ for Step 1. PoC T4: `--load-in-4bit` teacher (≈ 8 GB) + student (≈ 3 GB) = ~11 GB. Step 2 (FT on `Qᵢ`) is student-only — teacher unloaded, runs on any HW (T4 fine). Direction B (Struct-SQL) never co-loads at all — offline trace generation, Step 1 is student SFT only on cached traces.

### 5.3 Schema Encoder + Retrieval

- Schema serialized as DDL (types + FK join paths) for prompt `S`
- **BGE-small-en + FAISS** retrieval — pool = **the deploying model's own TRAIN data**
- **Embedding text = QUESTION ONLY** (no schema in the embedding). Schema in the embedding biases cross-schema retrieval toward similar *schemas* not similar *query patterns*; train/test schemas are disjoint → DDL vectors diverge → similarity corrupted. Question-only matches Light-SQL [4] QTS_S + DAIL-SQL. *(Fixed 2026-06-19; was `question [SEP] ddl[:512]` → caused central+ICL −9.1%.)*
- **Default ICL config (2026-06-20):** `retrieval = question-similarity · demo_style = never_schema · k=3` — one embedding lookup + one generation.
  - **never_schema demos** (`build_prompt demo_style=never_schema`, default): question + **verbatim SQL, no source DDL** → no foreign schema in prompt, concrete own-pool SQL grounding kept. **skeleton** (`demo_style=skeleton`): identifiers masked → structure-only, stronger-privacy **ablation**. **`full` removed 2026-06-20** (was DDL+SQL; reintroduced schema-bleed vector, never default).
  - **Not used:** no structural rerank, no complexity gate, and no k=0 draft inspection in the current inference path. The implementation is one retrieval pass + one generation.
- Top-`k` at **inference/eval**: `k=3` (∈{1,3} per [4]; inverted-U at k=5)
- **Training k controls whether the student LEARNS TO READ demos:**
  - `train-k=0` (current default, SFT protocol) — student never sees demos in context.
    Eval-k=3 on such a student is a **train/test mismatch**: demos are OOD → student
    copies a demo's table/column names into the test query (**schema bleed**). Measured:
    `central` k0→k3 = **−30 flips net** (gain 79 / hurt 109; **54 of the 109 hurts are
    `no such column` exec errors** = pure bleed). This −1 to −2 pp is **NOT** evidence that
    ICL is useless on a fine-tuned model — it is the signature of training demo-free then
    testing demo-augmented.
  - `train-k=3` (**in-context tuning** — the framework's intended path) — student trains
    WITH retrieved demos in context, so it learns to attend to them. Mitigates the
    mismatch directly (cf. **KID [10]**: simulate the inference-time condition during
    training). **Demo-style parity (locked 2026-07-06): train `demo_style` == eval
    `demo_style` within any arm.** Default = `never_schema` end-to-end. Paired
    `skeleton` (train+eval) = stronger-privacy cell (KD_PLAN E3.4). Train-`skeleton` →
    eval-`never_schema` = the **style-shift experiment** (KD_PLAN E3.5) — an explicit
    robustness analysis, never a default, since mixing styles reintroduces exactly the
    train/test mismatch this framework exists to remove.
- **RQ2 goal — Fed + ICL + KD synergy (retargeted 2026-07-06, see retired-invariant note
  §9):** the framework targets `(FT/KD)+ICL` **>** either alone on a small model, tested at
  the **default `train-k=0`** config (student never sees demos during training; ICL is
  eval-only). Headline arms = `central@k3` / `fedkd@k3` reported under **`train-k=0`, eval
  k=3** — this is now the official reporting condition, not a "mismatch baseline" to be
  superseded. In-context tuning (`train-k=3`) is an **optional exploratory arm**
  (`central_ict`, KD_PLAN E1.6/E1.7), kept to test whether it beats the train-k=0 numbers —
  not assumed to be the answer in advance.
- ICL **also** serves as a **parameter-free option for clients that cannot fine-tune** +
  privacy-preserving transfer (no source schema/DDL in prompt; `never_schema` default,
  `skeleton` for identifier masking) — a secondary benefit, not the ceiling on its value.
- **Open empirical risks (decide by experiment, not assumption):** (a) the measured
  `central` k0→k3 result (**−30 net flips**, 54/109 hurts = `no such column`) is the
  official headline number's own known failure mode — report it, don't hide it; (b) whether
  `train-k=3` in-context tuning (exploratory) actually fixes it, worsens it (schema-copying
  shortcut — see retired-invariant note §9), or is a wash is an open question the
  `central_ict` arm answers, not a foregone conclusion; (c) cost — `train-k=3` needs A100
  (3× prompt length, OOMs T4) regardless of whether it turns out to help.

**ICL positions (three distinct points):**

| Position | Who | Pool | k | Default |
|---|---|---|---|---|
| KID scoring (training) | Teacher | the KD corpus's train demos | 3 | ✓ fixed |
| Student training (FT) | Student | Qᵢ | **0** / 3 | `train-k=0` = **official default** (SFT, no demos during training, fits T4); `train-k=3` = in-context tuning, **optional exploratory arm** (A100) — not assumed to win |
| Inference | Student | Qᵢ | 3 | ✓ fixed |

Student training ICL is configurable: `--train-k 0` (**default**) or `--train-k 3`
(in-context tuning — exploratory arm, tests whether teaching the student to read demos
during training beats the default). Teacher ICL is always k=3 from the public KD corpus. Inference ICL is
always k=3 Qᵢ.

🔴 **Demo pool = TRAIN data, never the test set.** The ICL pool is the model's own
training examples — a client's private `Qᵢ` (`client_i_train.csv`) for per-client
and federated models, or the pooled centralized train set (`centralized/train.csv`)
for the `central` baseline (± ICL). The frozen test set (`centralized/test.csv` =
Spider dev) is **never** a demo source. Because test DBs are schema-disjoint from
train (verified: 0 overlap), retrieval is always **cross-schema** (train demos →
unseen test query) and the query is never in the pool → **no leave-one-out**. The
RQ2 mechanism is exactly this: the Global SLM's general skill + cross-schema demos
carry SQL-pattern (skeleton) structure to an unseen schema, not schema-specific answers.

**Per-arm pool + reporting (eval):**

| Arm | model | demo pool | reported |
|---|---|---|---|
| `base` floor | base | k=0 (no ICL) | single |
| `local` | per-client adapter `Mᵢ` | client_i pool | mean±std over K |
| `fedavg` | one global model | each client pool (K evals) | mean±std over K |
| `fedkd` | one global `M_G` | each client pool (K evals) | mean±std over K |
| `fedkd@k3` | one global `M_G` | each client pool (K evals) | mean±std over K |
| `central` | centralized | k=0 (no ICL) | single |
| `central@k3` | centralized | centralized pool | single |

> **Headline arms (retargeted 2026-07-06):** `central@k3` / `fedkd@k3` reported under
> **`train-k=0`, eval-k=3** (the official default) are the framework's main result — they
> test `(FT/KD)+ICL > either` at the config the framework actually ships. The known
> failure mode at this config (−30 net flips, 54/109 `no such column`) is reported as-is,
> not hidden. `central_ict@k3` / in-context-tuned arms (`train-k=3`) are a **separate,
> optional exploratory line** testing whether training with demos beats the default —
> not a supersede-and-replace relationship. Always state which training-k and which demo
> style an `@k3` number used.

**KD ablation arms (teacher-side ICL):**

| Arm | Teacher ICL | Purpose |
|---|---|---|
| `fedkd_teacher_k3` | k=3 from **the public KD corpus's train split** (default — teacher never touches `Qᵢ`, invariant #2) | ICL-enhanced soft labels |
| `fedkd_teacher_k0` | k=0 (no ICL) | baseline — shows teacher-ICL value |

**KD-direction arms (§5.6.1):**

| Arm | KD direction | level | HW | role |
|---|---|---|---|---|
| `fedkd` | KID [10] (RKL on imperfect `ŷ`) | logit | A100 | primary |
| `fedkd_struct` | Struct-SQL [11] (SFT on QP-CoT⊕SQL) | data/seq | T4 | contender / fallback |
| `fedkd_seqkd` | SeqKD (SFT on teacher SQL, no CoT) | data/seq | T4 | classic baseline |
| `fedavg_pub` | none — CE on the public KD corpus **gold**, no teacher | data | T4 | **data-matched control** — isolates extra-public-data value |

All Stream-2 variants run on the **same public-corpus train split** → control ladder
`fedavg → fedavg_pub → fedkd_seqkd → fedkd_struct → fedkd`; each rung adds ONE
ingredient. Teacher value = `fedkd − fedavg_pub` (never `fedkd − fedavg` alone —
that confounds teacher with extra data). This ladder is deferred (§0 top note); staged
run order once resumed: `KD_PLAN.md` §Deferred.

**Evaluation datasets:** Spider (primary) · a second public corpus (TBD; secondary eval, dropped 2026-07-07 along with BIRD — see top note)

Global federated arms (`fedkd`, `fedavg`) are deployed once **per client** (each org
runs the shared global model with its own private demos) and reported as mean±std —
keeps the privacy story end-to-end and yields per-client variance for free. `fedkd − central`
gap therefore folds in both the federation cost and the private-pool restriction
(`central` sees the full centralized pool) — the honest federated-vs-centralized gap.

Builder = `fedicl_sql/retrieval/pool.py`; eval = `experiments/eval_arms/run.py`.

### 5.4 ICL Prompt Constructor

```
σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q
```

- `q` — NL question
- `S` — serialized schema (DDL)
- `I` — system instruction ("expert SQL generator")
- `Q` — top-k retrieved demonstrations (NL + **verbatim SQL, no source DDL** — `demo_style=never_schema`, default) from Qᵢ, via question-similarity retrieval. (`skeleton` = identifier-masked ablation.)

### 5.5 Local SLM Student `Mᵢ` — Qwen2.5-1.5B-Instruct + LoRA

- Initialized from `M_G` (server broadcast) each round
- Generates: predicted SQL `ŝ` (+ optional reasoning)
- **LoRA fp16 on both CUDA and MPS** (training always fp16 — no 4-bit during training). 4-bit available for inference-only eval via `StudentModel`.

### 5.6 Local Training — Sequential: Step 1 KD-pretrain on the public KD corpus → Step 2 FT on Qᵢ

**Retired 2026-07-06 (this session):** the earlier design combined both streams into one
per-step loss (`L = λ₁·L_FT + λ₂(t)·L_KD`, global alpha-decay). That design is **replaced**
by two sequential training steps on the same LoRA adapter — KD-pretrain runs to completion
first, FT runs second on top of it. No combined loss, no λ mixing, no decay schedule.
Rationale for trying KD first: isolate and validate the KD signal on its own (does the
teacher/KD signal teach anything at all) before layering private-data fine-tuning on top;
avoids conflating "did KD help" with "did the two losses interact well when mixed."

**Step 1 — KD-pretrain on the public KD corpus (runs first, from base model or `M_G`):**

Three sub-steps for Direction A / KID (1 student forward, 1 teacher forward per
public-corpus example); Direction B / Struct-SQL instead does plain SFT on offline-cached traces (no
teacher forward needed at this step — see §5.6.1):

1. **Masking** — sample `ρ` fraction of token positions from the corpus's gold SQL `y_pub`, replace with `[MASK]`. Default strategy: Hard. Sweep `ρ ∈ {0.1, 0.2, 0.3, 0.4, 0.5}`.
2. **Predicting** — student forward over masked `y_pub` → fill mask positions → `ŷ_pub` (imperfect SQL, student-style errors).
3. **Teacher scoring** — teacher forward on `ŷ_pub` with public-corpus ICL demos (k=3, question-only, `never_schema`):

```python
x_b, y_b = next_batch(PUB_train)
demos = faiss_retrieve(x_b, PUB_train, k=3)         # never_schema demos (public-corpus pool)
y_hat = student.mask_rewrite(P_ICL(x_b, demos), y_b, ratio=ρ)  # ŷ_pub WITH demos in ctx
p = teacher(P_ICL(x_b, demos), y_hat)               # logprob dist, no decoding
q = student(P_ICL(x_b, demos), y_hat)               # SAME ctx as teacher → consistent KD pair
L_KD = RKL(q, p)
update_lora(student, L_KD)                          # Step 1 loss — KD only, no L_FT term
```

> **Context-alignment fix (2026-06-30, still applies):** teacher and student both
> condition on `P_ICL(x_b, demos)` — consistent KD pair, avoids scoring student/teacher
> under different contexts. Cost: every forward carries k=3 context (3–4× length) → A100
> for Direction A's Step 1; still 1-pass.

Step 1 ends when its own stopping criterion is met (fixed epochs/steps over the public corpus's train split, or
early-stop on a KD-corpus-train held-out slice) — **not** tied to FT convergence, since FT hasn't
started yet. Save the resulting LoRA adapter as the Step-2 init checkpoint.

**Step 2 — FT on private Qᵢ (runs second, LoRA initialized from Step 1's checkpoint):**

```python
x_q, y_q = next_batch(Qᵢ)               # train-k=0 default; train-k=3 = in-context tuning (exploratory)
L_FT = CE(student(x_q, demos_Qᵢ), y_q)  # gold SQL supervision; demos in context iff train-k>0
update_lora(student, L_FT)              # Step 2 loss — FT only, teacher not loaded
```

> **In-context tuning hook (exploratory arms only):** if testing `train-k=3` here, inject
> `Qᵢ` demos with the same pool/k/`demo_style` as inference (see retired-invariant note,
> §9) — this is a Step-2-only concern, orthogonal to Step 1.

| Step | Data | Signal | HW |
|---|---|---|---|
| Step 1 (KD-pretrain) | Public KD corpus (teacher-scored or teacher-generated) | General SQL structural knowledge | A100 (Dir A) / T4 (Dir B) |
| Step 2 (FT) | Private `Qᵢ` (gold SQL) | Domain-specific supervised SQL | any (student-only, teacher unloaded) |

**Why split datasets:** teacher never accesses `Qᵢ` → privacy absolute. The KD corpus is public → teacher can run without privacy constraint. SQL structural patterns (JOIN, GROUP BY, nested queries) transfer cross-schema.

**Why sequential, not combined-loss:** simpler to build and debug (no loss-weight tuning,
no decay schedule), and lets Step 1 be validated in isolation (E0.4 teacher-quality probe,
Stage-1 bake-off) before any FT cost is spent. Known risk (open, not yet measured): FT in
Step 2 may partially overwrite what Step 1 taught (catastrophic forgetting) since there is
no rehearsal of the public corpus during Step 2 — this is an empirical question for Stage 1, not
assumed either way.

**`local`/`fedavg` arms:** skip Step 1 entirely, train Step 2 (`L_FT`) only from the base/`M_G` adapter.

### 5.6.1 Two KD directions (both built; compared head-to-head)

`L_KD` above is **Direction A**. Two distillation directions are implemented and
benchmarked — they sit on **different method axes**, so this is a real comparison, not an
ablation. KID is not assumed to win; Direction B is the proven fallback.

| | **Direction A — KID [10]** (primary) | **Direction B — Struct-SQL [11]** (contender) |
|---|---|---|
| Axis | **logit / distribution-level** | **data / sequence-level** |
| KD data | **public KD corpus's train split** | **public KD corpus's train split** (same — fixed 2026-07-06, traces on the public corpus not `Qᵢ` → no data confound) |
| Teacher emits | top-K logprobs over imperfect `ŷ` | **QP-CoT** structured reasoning trace + gold SQL |
| Student loss | `RKL(q‖p)` on `ŷ` (soft) | **SFT (CE)** on `QP-CoT ⊕ SQL` (hard) |
| What transfers | calibration under inference-style errors | execution-plan reasoning (Trace Schema → pick tables/cols → scan → join → filter → group) |
| Teacher active during | Step 1 (KD-pretrain) only, co-loaded with student | **not during training at all — offline, before Step 1** |
| Cost / HW | A100 (7B+1.5B co-load, 1-pass) | **T4-friendly** (offline teacher, student SFT only) |
| Needs logit access / tokenizer-align | yes | no |
| Reported gain (own paper) | +5.83% avg, 5 benchmarks | +8.1% over unstructured-CoT distillation |

**Direction B mechanism (Struct-SQL):** teacher is prompted with a **Query-Plan CoT
(QP-CoT)** template → emits a structured logical blueprint mirroring how a DB engine
executes the query. Traces are generated **offline on the public corpus's train split** (once, cached,
exec-filter kept — the corpus's DBs are local). Student is SFT'd on
`(question ⊕ QP-CoT trace ⊕ SQL)`. Key
finding [11]: SLMs **cannot internalize** structured reasoning by prompting alone — KD is
what installs it. This **subsumes our skeleton-structure loss** (skeleton = a degenerate
1-step blueprint) → adopt QP-CoT as the structured signal, keep exec-filter.

**Why both:** (a) if KID ≈ or < Struct-SQL, we ship a proven NL2SQL-specific method that
also runs on T4 and fits federation cleanly (offline teacher = no per-step co-load);
(b) the two are **composable** — Struct-SQL's QP-CoT can be the *target sequence* that KID
then makes imperfect (mask+rewrite the CoT⊕SQL), uniting structured-reasoning transfer
(B) with inference-mismatch correction (A). Decide by experiment.

> **Open:** does QP-CoT help a 1.5B student (vs the 4B in [11])? does the longer CoT
> target fit T4 VRAM at `train-k=3`? measure before locking a primary direction.

---

## 6. Federated Round Loop

> ⚠️ **Stale pseudocode below** — written for the retired combined-loss design (per-step
> `L = λ₁·L_FT + λ₂·L_KD`). Local training is now sequential (Step 1 KD-pretrain → Step 2
> FT, §5.6); how that maps onto federated rounds (does Step 1 run once globally, once per
> round, or once before round 1 starts?) is an **open question, deferred to Fed discussion**
> — not yet decided. Do not implement Fed against this loop as-is. This whole federated
> loop is deferred anyway (§0 top note, `KD_PLAN.md` §Deferred) — no public corpus is
> picked, and the currently-running PoC (`KD_PLAN.md` §PoC) has no federation at all,
> just two single-stream arms trained from base on a Spider slice.

```python
Round t = 1 .. T:
  1. SERVER  broadcast M_G → all K clients

  2. CLIENT i (parallel, teacher + student co-loaded on A100):
       student.load_lora(θ_g)
       for step in range(local_steps):

           # --- Stream 1: FT on private Qᵢ ---
           x_q, y_q = next_batch(Qᵢ)
           L_FT = CE(student(x_q), y_q)              # gold CE, k = train-k (== eval k, parity)

           # --- Stream 2: KID on the public KD corpus (teacher+student share P_ICL ctx) ---
           x_b, y_b = next_batch(PUB_train)
           demos = faiss_retrieve(x_b, PUB_train, k=3)   # never_schema (public-corpus pool)
           y_hat = student.mask_rewrite(P_ICL(x_b,demos), y_b, ρ)  # ŷ_pub WITH demos
           p = teacher(P_ICL(x_b, demos), y_hat)     # 1 forward, no decoding
           q = student(P_ICL(x_b, demos), y_hat)     # SAME ctx as teacher
           L_KD = RKL(q, p)

           # --- Combined loss ---
           L = λ₁ * L_FT + λ₂(global_step) * L_KD    # global decay across rounds
           update_lora(student, L)

       Δθᵢ ← encrypt + compress + DP-perturb (θᵢ − θ_{t-1})
       Upload Δθᵢ  [Weights Only]

  3. SERVER  θ_t ← FedAvg({Δθᵢ}, weights nᵢ/n)  →  M_G ← base_SLM + θ_t

Inference (per client):
       a. Retrieve top-k demos from own TRAIN pool Qᵢ (k=3, question-only)
       b. Build ICL prompt σ(q, Sᵢ, I, Q)
       c. M_G.generate(prompt) → SQL
       [eval: repeat per client pool → mean±std for global arms]

Return: M_G (global student)
```

---

## 7. Inference (deployment)

Each client runs `M_G` locally (no server, no teacher at inference time):
1. Schema encode `Sᵢ`
2. Retrieve top-k demos from local `Qᵢ`
3. Build prompt → `M_G.generate(prompt)` → SQL

No teacher at inference. Teacher runs during training only (on the public corpus).

---

## 8. Data flows summary

```
TRAINING Step 1 — KD-pretrain (teacher + student co-loaded, Direction A only; Direction B
                   uses offline-cached traces, student-only SFT, no teacher):
  PUB_train  ──►  mask(y_b, ρ)  ──►  student.mask_rewrite()  ──►  ŷ_pub
  PUB_train  ──►  faiss_retrieve(x_b, k=3)  ──►  P_ICL  ──►  teacher forward  ──►  p
  ŷ_pub  ──►  student(x_b)  ──►  q
  ──►  L_KD = RKL(q, p)  ──►  LoRA update  ──►  save adapter checkpoint

TRAINING Step 2 — FT (student-only, teacher unloaded, init from Step-1 checkpoint):
  private Qᵢ  ──►  student(x_q)  ──►  L_FT = CE(gold y_q)  ──►  LoRA update

INFERENCE (k=3, Qᵢ demos):
  Qᵢ  ──►  retrieval  ──►  ICL prompt σ(q, Sᵢ, I, Q)  ──►  M_G.generate() → SQL

Local Knowledge Cache (optional, Fig.1): not yet implemented.
```

---

## 9. Key design invariants (never violate)

1. **Private data never leaves client.** `Sᵢ`, raw rows, `Qᵢ`, teacher outputs — no outgoing data arrow.
2. **Teacher never touches `Qᵢ`.** Teacher runs exclusively on the public KD corpus — for BOTH directions, incl. offline QP-CoT generation. No private schema or SQL ever enters the teacher's context. Never uploads outputs. (Systems property; the motivation is update alignment via a shared public KD corpus, §5.2 — NOT privacy, since the on-premise teacher could read `Qᵢ` without leaking anything.)
3. **Upload = Weights Only.** LoRA deltas, not full model, not data, not teacher targets.
4. **Training on Qᵢ (Step 2 FT) is mandatory for every arm except the floor.** Public-corpus-only training (Step 1 alone, no Step 2) → FedAvg no-op if federated; eliminated by design — every non-floor arm must run Step 2.
5. **Retrieval embeds the QUESTION only — never the schema.** Schema in the embedding corrupts cross-schema similarity. Demo rendering never includes source DDL (`demo_style=never_schema` default = verbatim SQL no DDL; `skeleton` = same but identifier-masked). `demo_style` affects *demo SQL rendering* only, not the embedding text.
6. **One stack per comparison.** Mac-fp16 ≠ CUDA-fp16 — never compare cross-stack.
7. **Co-loaded VRAM, Step 1 only.** Teacher (7B) and student (1.5B) are loaded simultaneously **only during Step 1 (KD-pretrain, Direction A)** (~17 GB total). Requires A100 40 GB+ for Step 1; PoC: 4-bit teacher to fit T4. Step 2 (FT) is student-only, teacher unloaded, runs on any HW. Direction B never co-loads (offline trace generation before Step 1).
8. **Demo pool = TRAIN, never test.** ICL demos come from the model's own train data (per-client `Qᵢ` or centralized train). Test set is never a demo source → no leave-one-out. Retrieval is cross-schema (train→unseen-test). Violating this leaks near-answers and inflates EX.
9. **KD data = the same public corpus for every KD direction + the `fedavg_pub` gold-CE control.** `kid − struct` (direction value) and `fedkd − fedavg_pub` (teacher value) must be data-matched; `fedkd − fedavg` alone confounds teacher with extra public data. On the corpus's held-out split (secondary eval), compare KD arms against `fedavg_pub` and state the train-exposure.

> **Retired 2026-07-06 (this session): "train-k must match eval-k" invariant.** Previously
> listed here as a "never violate" rule (train-k=3 mandatory if eval uses k=3, for FT + KD
> teacher + KD student forward, plus a style-parity and target-level clause). Decision:
> train-k==eval-k parity is **not** locked as an architectural rule — whether `train-k=0`
> models use eval-time ICL well is an open empirical question, answered per-arm by
> comparing `central` vs `central@k3` (both already run), not assumed either way in advance.
> `train-k=0` (SFT, no demos during training) stands as the **default/official** training
> config; `train-k=3` in-context tuning is an **optional exploratory arm** (`central_ict`,
> E1.6, E1.7 in `KD_PLAN.md`), not a mandated fix.
>
> **Still on record, not retracted:** the measured `central` k0→k3 result — **−30 net
> flips** (79 gain / 109 hurt), **54/109 hurts are `no such column` errors** — stands as
> data. Retiring the invariant means the framework no longer *prescribes* train-k=3 as the
> answer to that number; it stays an open question tracked by the Stage-1 experiment
> ladder instead of a locked design rule.

---

## 10. Notation reference (canonical — §2 of DECISIONS.md)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) |
| `T` | # federated rounds (PoC: 2–3) |
| `k` | # ICL shots at inference (∈{1,3}; inverted-U at 5) |
| `E` | local epochs per round (1–2) |
| ~~`λ(t)`~~ | **retired** (combined-loss design dropped in favor of sequential Step 1 → Step 2, §5.6) |
| `ρ` | masking ratio (sweep 0.1–0.5) — fraction of gold SQL tokens masked |
| `ŷ` | imperfect SQL (student rewrite of masked `y`) — KD target sequence |
| `p` | teacher logprob distribution over `ŷ` (with ICL, k=3) — soft label |
| `q` | student logprob distribution over `ŷ` — distill target |
| `M_T` | teacher LLM (Qwen2.5-7B-Instruct, **local on each client, frozen**) |
| `Mᵢ` | client-i student (Qwen2.5-1.5B) |
| `M_G` | global SLM (base + aggregated LoRA) |
| `Sᵢ, Qᵢ` | client-i private schema / NL-SQL pairs |
| `θ, Δθᵢ` | LoRA params / client-i delta |
| `τ` | KD temperature (soft-KL scaling) |
