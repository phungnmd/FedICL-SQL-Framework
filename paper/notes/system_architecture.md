# FedICL-SQL — System Architecture

> Grounded in: `fig_architecture_source.png` (mechanism ground truth) · `fedicl_sql_outline.pdf` (section structure) · `DECISIONS.md` (spec + naming).
> Maps directly to §3 of the paper. **Fig.1 wins on any mechanism dispute.**
>
> **Re-aligned 2026-06-16:** teacher moved client-side (local 7B). Public X and ICL Hub G removed.
> **Re-aligned 2026-06-29:** KD mechanism replaced with KID (imperfect data distillation): teacher runs online per step (frozen, forward-only), student masks+rewrites gold SQL → ŷ, Reverse KL + alpha-decay loss. Offline annotation pipeline removed.

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
│  │  FedAvg / FedProx: θ_t ← θ_{t-1} + (1/K) Σᵢ Δθᵢ             │ │
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
│       ▼ (offline, once, before rounds)                           │   │
│  [Local Teacher M_T — Qwen2.5-7B-Instruct]                      │   │
│   Runs on Qᵢ: generates SQL + CoT + top-K logprobs, exec-filter │   │
│   → client_i_teacher_targets.csv + .logprobs.jsonl              │   │
│   Unloaded after generation (VRAM released for student)         │   │
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
│  │  Local Training (Distillation)                               │   │
│  │  L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec         │   │
│  │      ↑ gold Qᵢ   ↑ teacher targets Qᵢ  ↑ skeleton ↑ filter │   │
│  └──────────────────────────────────────────────────────────────┘   │
│  → LoRA delta Δθᵢ → encrypt+compress+DP-perturb → upload            │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Server Components

### 3.1 Federated Aggregation Engine

**Algorithm:** FedAvg / FedProx.

```
θ_t  ←  θ_{t-1}  +  (1/K) Σᵢ Δθᵢ
M_G  ←  base_SLM + θ_t
```

FedProx adds a proximal term `(μ/2)||θ - θ_{t-1}||²` per client to control drift under high non-IID (use if convergence is unstable).

**Uploads only LoRA deltas `Δθᵢ`** (not full weights) — bounded communication cost per round.

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

**Why BIRD for KD:** teacher never accesses private `Qᵢ` → privacy claim is absolute (no private schema in teacher's context at any point). BIRD = cross-domain NL2SQL public benchmark; teacher's SQL structural knowledge transfers cross-schema by design.

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
- At **training**: k=0 (standard SFT protocol, avoids OOM from 3× longer prompts)
- **RQ2 framing:** ICL is **redundant on the fine-tuned student** (knows patterns already → current full-test spotchecks show about −1 to −2 pp vs k=0 depending on retrieval variant; best completed diagnostic: 60.15% vs 61.32%). Fine-tuned arms (`central`, `fedkd`) reported at **k=0**. ICL's value = **parameter-free option for clients that cannot fine-tune** + privacy-preserving transfer (no source schema/DDL in prompt; `never_schema` default, `skeleton` ablation for identifier masking). RQ2 accuracy story → test ICL on **base/weak model (`base`, `local`)**, not `central`. Never claim "ICL improves a fine-tuned model".

**ICL positions (three distinct points):**

| Position | Who | Pool | k | Default |
|---|---|---|---|---|
| KID scoring (training) | Teacher | BIRD train demos | 3 | ✓ fixed |
| Student training (FT + KID) | Student | Qᵢ or BIRD | 0 | k=0 avoids OOM on T4; k=3 = ablation on A100 |
| Inference | Student | Qᵢ | 3 | ✓ fixed |

Student training ICL is configurable: `--train-k 0` (default) or `--train-k 3` (ablation). Teacher ICL is always k=3 BIRD. Inference ICL is always k=3 Qᵢ.

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

**KD ablation arms (teacher-side ICL):**

| Arm | Teacher ICL | Purpose |
|---|---|---|
| `fedkd_teacher_k3` | k=3 from `Qᵢ` (default) | ICL-enhanced soft labels |
| `fedkd_teacher_k0` | k=0 (no ICL) | baseline — shows teacher-ICL value |

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
x_q, y_q = next_batch(Qᵢ)
L_FT = CE(student(x_q), y_q)   # gold SQL supervision, k=0
```

**Stream 2 — KID distillation on public BIRD:**

Three sub-steps (1 student forward, 1 teacher forward):

1. **Masking** — sample `ρ` fraction of token positions from BIRD gold SQL `y_bird`, replace with `[MASK]`. Default strategy: Hard. Sweep `ρ ∈ {0.1, 0.2, 0.3, 0.4, 0.5}`.
2. **Predicting** — student forward over masked `y_bird` → fill mask positions → `ŷ_bird` (imperfect SQL, student-style errors).
3. **Teacher scoring** — teacher forward on `ŷ_bird` with BIRD ICL demos (k=3, question-only, `never_schema`):

```python
x_b, y_b = next_batch(BIRD_train)
y_hat = student.mask_rewrite(y_b, ratio=ρ)          # ŷ_bird, k=0
demos = faiss_retrieve(x_b, BIRD_train, k=3)
p = teacher(P_ICL(x_b, demos), y_hat)               # logprob dist, no decoding
q = student(x_b, y_hat)
L_KD = RKL(q, p)
```

**Combined loss:**

```
L = λ₁ · L_FT  +  λ₂ · L_KD
```

where `λ₂ = λ₂(t)` uses alpha-decay (1.0 → 0) to weight soft labels less as student matures.

| Term | Data | Signal |
|---|---|---|
| `L_FT` | Private `Qᵢ` (gold SQL) | Domain-specific supervised SQL |
| `L_KD` | Public BIRD (teacher soft labels on `ŷ_bird`) | General SQL structural knowledge |

**Why split datasets:** teacher never accesses `Qᵢ` → privacy absolute. BIRD is public → teacher can run without privacy constraint. SQL structural patterns (JOIN, GROUP BY, nested queries) transfer cross-schema.

**`local`/`fedavg` arms:** `L_KD = 0`, train on `L_FT` only.

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
           L_FT = CE(student(x_q), y_q)              # gold CE, k=0

           # --- Stream 2: KID on public BIRD ---
           x_b, y_b = next_batch(BIRD_train)
           y_hat = student.mask_rewrite(y_b, ρ)      # 1 forward, k=0 → ŷ_bird
           demos = faiss_retrieve(x_b, BIRD_train, k=3)
           p = teacher(P_ICL(x_b, demos), y_hat)     # 1 forward, no decoding
           q = student(x_b, y_hat)
           L_KD = RKL(q, p)

           # --- Combined loss ---
           L = λ₁ * L_FT + λ₂(step) * L_KD
           update_lora(student, L)

       Δθᵢ ← encrypt + compress + DP-perturb (θᵢ − θ_{t-1})
       Upload Δθᵢ  [Weights Only]

  3. SERVER  θ_t ← FedAvg({Δθᵢ})  →  M_G ← base_SLM + θ_t

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
2. **Teacher never touches `Qᵢ`.** Teacher runs exclusively on public BIRD data. No private schema or SQL ever enters the teacher's context. Never uploads outputs.
3. **Upload = Weights Only.** LoRA deltas, not full model, not data, not teacher targets.
4. **Training on Qᵢ is mandatory (gold + teacher).** Public-X-only training (old) → FedAvg no-op; now eliminated by design.
5. **Retrieval embeds the QUESTION only — never the schema.** Schema in the embedding corrupts cross-schema similarity. Demo rendering never includes source DDL (`demo_style=never_schema` default = verbatim SQL no DDL; `skeleton` = same but identifier-masked). `demo_style` affects *demo SQL rendering* only, not the embedding text.
6. **One stack per comparison.** Mac-fp16 ≠ CUDA-fp16 — never compare cross-stack.
7. **Co-loaded VRAM.** Teacher (7B) and student (1.5B) are loaded simultaneously during training (~17 GB total). Requires A100 40 GB+. PoC: 4-bit teacher to fit T4.
8. **Demo pool = TRAIN, never test.** ICL demos come from the model's own train data (per-client `Qᵢ` or centralized train). Test set is never a demo source → no leave-one-out. Retrieval is cross-schema (train→unseen-test). Violating this leaks near-answers and inflates EX.

---

## 10. Notation reference (canonical — §2 of DECISIONS.md)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) |
| `T` | # federated rounds (PoC: 2–3) |
| `k` | # ICL shots at inference (∈{1,3}; inverted-U at 5) |
| `E` | local epochs per round (1–2) |
| `λ(t)` | alpha-decay loss weight (1.0 → 0 over training) — balances MLE vs RKL |
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
