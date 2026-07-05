# FedICL-SQL — System Architecture

> Grounded in: `fig_architecture_source.png` (mechanism ground truth) · `fedicl_sql_outline.pdf` (section structure) · `DECISIONS.md` (spec + naming).
> Maps directly to §3 of the paper. **Fig.1 wins on any mechanism dispute.**
>
> **Re-aligned 2026-06-16:** teacher moved client-side (local 7B). Public X and ICL Hub G removed.
> **Re-aligned 2026-06-29:** KD mechanism replaced with KID (imperfect data distillation): teacher runs online per step (frozen, forward-only), student masks+rewrites gold SQL → ŷ, Reverse KL + alpha-decay loss. Offline annotation pipeline removed. (KID source = **[10]** Zhong et al. 2024.)
> **Re-aligned 2026-06-30:** goal restated — build a **Fed + ICL + KD** framework that maximizes EX on a *small* model; the target is `(FT/KD)+ICL > either alone`. The old "ICL is redundant on a fine-tuned student / never claim ICL improves FT" framing is **retired** — it described a `train-k=0` student tested at `k=3` (a train/test mismatch, not an ICL ceiling). Path to synergy = **in-context tuning** (`train-k=3` + `skeleton` demos) so the student learns to read demos; mismatch principle grounded in KID [10].
> **Re-aligned 2026-07-06 (review fixes):** (1) **both** KD directions distill on public BIRD (Struct-SQL traces generated on BIRD, not `Qᵢ`) → no data confound in `kid − struct`; (2) `fedavg_bird` data-matched control added (CE on BIRD gold, no teacher) → teacher value = `fedkd − fedavg_bird`; (3) **demo-style parity** locked: train `demo_style` == eval `demo_style` per arm (style-shift = separate experiment); (4) teacher ICL demos = BIRD always; (5) FedAvg weighted `nᵢ/n`; (6) λ₂ alpha-decay is global across rounds. Staged run plan: `KD_PLAN.md`.

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
│       │   [Public BIRD train (local copy) + BIRD demo pool]     │   │
│       │        ▼                                                 │   │
│  [Local Teacher M_T — Qwen2.5-7B-Instruct, frozen]              │   │
│   Runs ONLY on public BIRD — never on Qᵢ                        │   │
│   Dir A KID: online forward per step, scores ŷ_bird             │   │
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
│  │  Local Training (dual-stream)                                │   │
│  │  L = λ₁·L_FT + λ₂(t)·L_KD    (λ₂ global alpha-decay)       │   │
│  │      ↑ gold CE on Qᵢ  ↑ KID / Struct-SQL on public BIRD     │   │
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

### 5.2 Local Teacher M_T — Qwen2.5-7B-Instruct (online, frozen, runs on BIRD public data)

Teacher runs **per training step** — one forward pass over imperfect student output `ŷ_BIRD` (generated from masked BIRD gold SQL). Frozen throughout. **Never sees client's private `Qᵢ`.**

**Per-step role:** student masks BIRD gold SQL `y_BIRD` → rewrites → `ŷ_BIRD`. Teacher computes `p = softmax(logits)` over `ŷ_BIRD` **with ICL context from BIRD train demos** (k=3, question-only, `never_schema`). Teacher prompt = `P_ICL(x_BIRD, demos_BIRD)` + `ŷ_BIRD`.

**Why BIRD for KD (reframed 2026-07-06):** primary reason = **shared public distillation corpus aligns client updates** — every client distills toward the same teacher behaviour on the same data → less FedAvg drift under non-IID (FedDF/FedMD line of argument). Secondary: BIRD is cross-domain → SQL structural knowledge transfers cross-schema. This is **NOT a privacy argument** — the teacher is on-premise, so reading `Qᵢ` would leak nothing; "teacher never touches `Qᵢ`" is a clean systems property, not the motivation. Applies to **both KD directions** (KID online scoring AND Struct-SQL offline trace generation) so `kid − struct` has no data confound.

**What teacher does NOT do:**
- No autoregressive text generation
- No access to `Qᵢ` or client's private schema `Sᵢ`
- Never uploads outputs to server

**VRAM:** teacher (7B fp16 ≈ 14 GB) + student (1.5B fp16 ≈ 3 GB) **co-loaded simultaneously**. Requires A100 40 GB+. PoC T4: `--load-in-4bit` teacher (≈ 8 GB) + student (≈ 3 GB) = ~11 GB.

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
- **RQ2 goal — Fed + ICL + KD synergy:** the framework targets `(FT/KD)+ICL` **>** either
  alone on a small model. Mechanism: KD internalizes general SQL skill (cross-schema
  structure from the teacher); in-context tuning teaches the student to exploit its own
  private `Qᵢ` demos at inference → the two signals are complementary (general skill +
  domain-specific retrieved patterns). Headline arms reported **at the train/eval k that
  wins** (`central@k3` / `fedkd@k3` under in-context tuning), not pinned to k=0.
- ICL **also** serves as a **parameter-free option for clients that cannot fine-tune** +
  privacy-preserving transfer (no source schema/DDL in prompt; `never_schema` default,
  `skeleton` for identifier masking) — a secondary benefit, not the ceiling on its value.
- **Open empirical risks (decide by experiment, not assumption):** (a) cost — `train-k=3`
  needs A100 (3× prompt length, OOMs T4); (b) 1.5B may be too small to learn the
  read-demos meta-skill; (c) inference demos are cross-schema (train/test disjoint) so the
  structural signal must transfer. The k=0 numbers stand until the in-context-tuned arm is
  run; do not over-claim synergy before `central@k3 (train-k3, style parity)` beats both
  `central` (k0) and `base@k3`.

**ICL positions (three distinct points):**

| Position | Who | Pool | k | Default |
|---|---|---|---|---|
| KID scoring (training) | Teacher | BIRD train demos | 3 | ✓ fixed |
| Student training (FT) | Student | Qᵢ | 0 / **3** | `train-k=0` = SFT baseline (fits T4); **`train-k=3` = in-context tuning, the synergy path (A100)** |
| Inference | Student | Qᵢ | 3 | ✓ fixed |

Student training ICL is configurable: `--train-k 0` (SFT baseline) or `--train-k 3` (**in-context tuning** — teaches the student to read demos, the path to `ICL+KD > either`). Teacher ICL is always k=3 BIRD. Inference ICL is always k=3 Qᵢ.

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

> **Synergy headline arms (in-context tuning):** `central@k3` / `fedkd@k3` reported under
> **`train-k=3` with style parity** (`never_schema` train+eval by default) are the
> framework's main result — they test `(FT/KD)+ICL > either`. The same arm names under
> `train-k=0` are the **mismatch baseline** (shows the −1 to −2 pp drop that motivates
> in-context tuning). Always state which training-k AND which demo style an `@k3` number used.

**KD ablation arms (teacher-side ICL):**

| Arm | Teacher ICL | Purpose |
|---|---|---|
| `fedkd_teacher_k3` | k=3 from **BIRD train** (default — teacher never touches `Qᵢ`, invariant #2) | ICL-enhanced soft labels |
| `fedkd_teacher_k0` | k=0 (no ICL) | baseline — shows teacher-ICL value |

**KD-direction arms (§5.6.1):**

| Arm | KD direction | level | HW | role |
|---|---|---|---|---|
| `fedkd` | KID [10] (RKL on imperfect `ŷ`) | logit | A100 | primary |
| `fedkd_struct` | Struct-SQL [11] (SFT on QP-CoT⊕SQL) | data/seq | T4 | contender / fallback |
| `fedkd_seqkd` | SeqKD (SFT on teacher SQL, no CoT) | data/seq | T4 | classic baseline |
| `fedavg_bird` | none — CE on BIRD **gold**, no teacher | data | T4 | **data-matched control** — isolates extra-public-data value |

All Stream-2 variants run on the **same BIRD train data** → control ladder
`fedavg → fedavg_bird → fedkd_seqkd → fedkd_struct → fedkd`; each rung adds ONE
ingredient. Teacher value = `fedkd − fedavg_bird` (never `fedkd − fedavg` alone —
that confounds teacher with extra data). Staged run order: `KD_PLAN.md` §4.

**Evaluation datasets:** Spider (primary) · BIRD (secondary, locked 2026-06-29)

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

### 5.6 Local Training — Dual-stream: FT on Qᵢ + KID on BIRD

Two independent data streams combined into one loss per step:

**Stream 1 — Supervised FT on private Qᵢ:**

```python
x_q, y_q = next_batch(Qᵢ)               # train-k=0 default; train-k=3 = in-context tuning
L_FT = CE(student(x_q, demos_Qᵢ), y_q)  # gold SQL supervision; demos in context iff train-k>0
```

> **In-context tuning hook:** the FT stream is where the student learns the actual
> demo→SQL behaviour, so `train-k=3` must inject `Qᵢ` demos HERE — same pool (`Qᵢ`),
> same k, **same `demo_style` as inference** (parity rule, invariant #9c; default
> `never_schema`). The skeleton anti-bleed hypothesis is tested as a paired
> train+eval `skeleton` cell (KD_PLAN E3.4), never by mixing styles.
> (The KD stream below operates on `ŷ` rewrites, a different task — `train-k` there
> is about teacher/student context alignment, not learning to generate from demos.)

**Stream 2 — KID distillation on public BIRD:**

Three sub-steps (1 student forward, 1 teacher forward):

1. **Masking** — sample `ρ` fraction of token positions from BIRD gold SQL `y_bird`, replace with `[MASK]`. Default strategy: Hard. Sweep `ρ ∈ {0.1, 0.2, 0.3, 0.4, 0.5}`.
2. **Predicting** — student forward over masked `y_bird` → fill mask positions → `ŷ_bird` (imperfect SQL, student-style errors).
3. **Teacher scoring** — teacher forward on `ŷ_bird` with BIRD ICL demos (k=3, question-only, `never_schema`):

```python
x_b, y_b = next_batch(BIRD_train)
demos = faiss_retrieve(x_b, BIRD_train, k=3)         # never_schema demos (BIRD pool)
y_hat = student.mask_rewrite(P_ICL(x_b, demos), y_b, ratio=ρ)  # ŷ_bird WITH demos in ctx
p = teacher(P_ICL(x_b, demos), y_hat)               # logprob dist, no decoding
q = student(P_ICL(x_b, demos), y_hat)               # SAME ctx as teacher → consistent KD pair
L_KD = RKL(q, p)
```

> **Context-alignment fix (2026-06-30):** teacher and student now BOTH condition on
> `P_ICL(x_b, demos)`. Previously student forward was demo-free (k=0) while teacher saw
> k=3 → the KD pair was scored under different contexts (latent inconsistency). With demos
> in both, the student is distilled on *how the teacher uses demos* AND the imperfect `ŷ`
> reflects student errors *made while seeing demos* = the true inference condition. KID
> (target-level mismatch) and in-context tuning (prompt-level mismatch) now compose
> cleanly. Cost: every forward carries k=3 context (3–4× length) → A100; still 1-pass.

**Combined loss:**

```
L = λ₁ · L_FT  +  λ₂ · L_KD
```

where `λ₂ = λ₂(t)` uses alpha-decay (1.0 → 0) over **global steps across all rounds**
(`t = round·local_steps + step`) — NOT restarted per round (per-round restart = ablation
only if convergence is unstable). Soft labels weigh less as the student matures.

| Term | Data | Signal |
|---|---|---|
| `L_FT` | Private `Qᵢ` (gold SQL) | Domain-specific supervised SQL |
| `L_KD` | Public BIRD (teacher soft labels on `ŷ_bird`) | General SQL structural knowledge |

**Why split datasets:** teacher never accesses `Qᵢ` → privacy absolute. BIRD is public → teacher can run without privacy constraint. SQL structural patterns (JOIN, GROUP BY, nested queries) transfer cross-schema.

**`local`/`fedavg` arms:** `L_KD = 0`, train on `L_FT` only.

### 5.6.1 Two KD directions (both built; compared head-to-head)

`L_KD` above is **Direction A**. Two distillation directions are implemented and
benchmarked — they sit on **different method axes**, so this is a real comparison, not an
ablation. KID is not assumed to win; Direction B is the proven fallback.

| | **Direction A — KID [10]** (primary) | **Direction B — Struct-SQL [11]** (contender) |
|---|---|---|
| Axis | **logit / distribution-level** | **data / sequence-level** |
| KD data | **public BIRD train** | **public BIRD train** (same — fixed 2026-07-06, traces on BIRD not `Qᵢ` → no data confound) |
| Teacher emits | top-K logprobs over imperfect `ŷ` | **QP-CoT** structured reasoning trace + gold SQL |
| Student loss | `RKL(q‖p)` on `ŷ` (soft) | **SFT (CE)** on `QP-CoT ⊕ SQL` (hard) |
| What transfers | calibration under inference-style errors | execution-plan reasoning (Trace Schema → pick tables/cols → scan → join → filter → group) |
| Teacher in round loop | yes, co-loaded per step | **no — generates traces offline once, cached** |
| Cost / HW | A100 (7B+1.5B co-load, 1-pass) | **T4-friendly** (offline teacher, student SFT only) |
| Needs logit access / tokenizer-align | yes | no |
| Reported gain (own paper) | +5.83% avg, 5 benchmarks | +8.1% over unstructured-CoT distillation |

**Direction B mechanism (Struct-SQL):** teacher is prompted with a **Query-Plan CoT
(QP-CoT)** template → emits a structured logical blueprint mirroring how a DB engine
executes the query. Traces are generated **offline on BIRD train** (once, cached,
exec-filter kept — BIRD DBs are local). Student is SFT'd on
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

```python
Round t = 1 .. T:
  1. SERVER  broadcast M_G → all K clients

  2. CLIENT i (parallel, teacher + student co-loaded on A100):
       student.load_lora(θ_g)
       for step in range(local_steps):

           # --- Stream 1: FT on private Qᵢ ---
           x_q, y_q = next_batch(Qᵢ)
           L_FT = CE(student(x_q), y_q)              # gold CE, k = train-k (== eval k, parity)

           # --- Stream 2: KID on public BIRD (teacher+student share P_ICL ctx) ---
           x_b, y_b = next_batch(BIRD_train)
           demos = faiss_retrieve(x_b, BIRD_train, k=3)   # never_schema (BIRD pool)
           y_hat = student.mask_rewrite(P_ICL(x_b,demos), y_b, ρ)  # ŷ_bird WITH demos
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

No teacher at inference. Teacher runs during training only (on BIRD public data).

---

## 8. Data flows summary

```
TRAINING (per step, teacher + student co-loaded):
  [Stream 1 — FT]
  private Qᵢ  ──►  student(x_q)  ──►  L_FT = CE(gold y_q)

  [Stream 2 — KID]
  public BIRD_train  ──►  mask(y_b, ρ)  ──►  student.mask_rewrite()  ──►  ŷ_bird
  BIRD_train  ──►  faiss_retrieve(x_b, k=3)  ──►  P_ICL  ──►  teacher forward  ──►  p
  ŷ_bird  ──►  student(x_b)  ──►  q
  ──►  L_KD = RKL(q, p)

  L = λ₁·L_FT + λ₂(t)·L_KD  ──►  LoRA update

INFERENCE (k=3, Qᵢ demos):
  Qᵢ  ──►  retrieval  ──►  ICL prompt σ(q, Sᵢ, I, Q)  ──►  M_G.generate() → SQL

Local Knowledge Cache (optional, Fig.1): not yet implemented.
```

---

## 9. Key design invariants (never violate)

1. **Private data never leaves client.** `Sᵢ`, raw rows, `Qᵢ`, teacher outputs — no outgoing data arrow.
2. **Teacher never touches `Qᵢ`.** Teacher runs exclusively on public BIRD data — for BOTH directions, incl. offline QP-CoT generation. No private schema or SQL ever enters the teacher's context. Never uploads outputs. (Systems property; the motivation is update alignment via a shared public KD corpus, §5.2 — NOT privacy, since the on-premise teacher could read `Qᵢ` without leaking anything.)
3. **Upload = Weights Only.** LoRA deltas, not full model, not data, not teacher targets.
4. **Training on Qᵢ is mandatory (gold + teacher).** Public-X-only training (old) → FedAvg no-op; now eliminated by design.
5. **Retrieval embeds the QUESTION only — never the schema.** Schema in the embedding corrupts cross-schema similarity. Demo rendering never includes source DDL (`demo_style=never_schema` default = verbatim SQL no DDL; `skeleton` = same but identifier-masked). `demo_style` affects *demo SQL rendering* only, not the embedding text.
6. **One stack per comparison.** Mac-fp16 ≠ CUDA-fp16 — never compare cross-stack.
7. **Co-loaded VRAM.** Teacher (7B) and student (1.5B) are loaded simultaneously during training (~17 GB total). Requires A100 40 GB+. PoC: 4-bit teacher to fit T4.
8. **Demo pool = TRAIN, never test.** ICL demos come from the model's own train data (per-client `Qᵢ` or centralized train). Test set is never a demo source → no leave-one-out. Retrieval is cross-schema (train→unseen-test). Violating this leaks near-answers and inflates EX.
9. **Train condition == inference condition (two levels).** (a) *Prompt-level:* if inference uses k=3 demos, training prompt must too (`train-k=3`) — for FT, KD teacher, AND KD student forward (all share `P_ICL`). (b) *Target-level:* KID imperfect `ŷ` simulates inference's autoregressive cascade. (c) *Style-level:* `demo_style` at train == at eval within an arm (parity, locked 2026-07-06); style-shift (train `skeleton` → eval `never_schema`) = a designated experiment (KD_PLAN E3.5), never a default. Mismatch at any level = the ICL-hurts-FT / cascade failure. The `train-k=0` arm is a deliberate *baseline* exposing (a), not the deployed config.
10. **KD data = public BIRD for every KD direction + the `fedavg_bird` gold-CE control.** `kid − struct` (direction value) and `fedkd − fedavg_bird` (teacher value) must be data-matched; `fedkd − fedavg` alone confounds teacher with extra public data. On BIRD-dev (secondary eval), compare KD arms against `fedavg_bird` and state the train-exposure.

---

## 10. Notation reference (canonical — §2 of DECISIONS.md)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) |
| `T` | # federated rounds (PoC: 2–3) |
| `k` | # ICL shots at inference (∈{1,3}; inverted-U at 5) |
| `E` | local epochs per round (1–2) |
| `λ(t)` | alpha-decay loss weight (1.0 → 0 over **global** steps across all rounds) — balances MLE vs RKL |
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
