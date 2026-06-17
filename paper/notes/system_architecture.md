# FedICL-SQL — System Architecture

> Grounded in: `fig_architecture_source.png` (mechanism ground truth) · `fedicl_sql_outline.pdf` (section structure) · `detailed_plan.md` (spec).
> Maps directly to §3 of the paper. **Fig.1 wins on any mechanism dispute.**
>
> **Re-aligned 2026-06-16:** teacher moved client-side (local 7B). Public X and ICL Hub G removed.

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
4. **De-identification & Masking** — schema identifier masking for retrieval-similarity scoring (planned, RQ2)

---

## 5. Client Components

### 5.1 Local Data & Schema (private, never leaves)

- `Sᵢ` — relational schema (tables, columns, types, FK paths)
- `Qᵢ` — NL/gold-SQL pairs on `Sᵢ`'s databases

### 5.2 Local Teacher M_T — Qwen2.5-7B-Instruct (offline, per-client)

**Two-step offline process before federated rounds begin:**

**Step 1 — Domain adaptation (fine_tune_teacher.py):**
Fine-tune the base 7B teacher on the client's own `Qᵢ` using LoRA (supervised CE on gold SQL). This adapts the teacher to the client's schema naming, SQL patterns, and domain vocabulary before it generates KD targets. Output: `artifacts/teacher_adapters/client_i/` (LoRA adapter).

- VRAM: fp16 LoRA training of 7B ≈ 28-32 GB → A100 required for Stage-B. T4 PoC: use `--max-steps 0` to skip fine-tuning and use the base 7B teacher as-is.

**Step 2 — Annotate Qᵢ to produce augmented training dataset (gen_teacher_targets.py):**
Load domain-adapted teacher (base + adapter merged) and run on each `(q, schema) ∈ Qᵢ`. Produces the **annotated Qᵢ dataset** (`client_i_train_kd.csv`) — a copy of the private training data with teacher annotation columns added:

| Column | Source | Meaning |
|--------|--------|---------|
| `question`, `query` (gold), `db_id`, `db_path` | original Qᵢ | private training example |
| `teacher_sql` | teacher 7B | teacher's SQL prediction |
| `reasoning` | teacher 7B | chain-of-thought derivation steps |
| `exec_ok` | exec validation | teacher SQL runs without error |
| `exec_correct` | exec validation | teacher SQL result set = gold result set |
| `top_logprobs[K]` | teacher 7B | per-token top-K log probs (stored in `.logprobs.jsonl`) |

**Exec filter:** only rows where `exec_correct=True` contribute teacher supervision. Exec-incorrect rows fall back to gold SQL during training.

**VRAM management (sequential):**
1. Fine-tune teacher (7B LoRA) → save adapter → unload
2. Load teacher + adapter → generate annotated dataset → unload
3. Load student (1.5B) → train on annotated dataset

### 5.3 Schema Encoder + Retrieval

- Schema serialized as DDL (types + FK join paths) for prompt `S`
- **BGE-small-en + FAISS** retrieval — pool = **the deploying model's own TRAIN data**
- **Embedding text (schema-aware):** `"question [SEP] ddl[:512]"` at both index time and query time
- Top-`k` at **inference/eval**: `k=3` (∈{1,3} per [4]; inverted-U at k=5)
- At **training**: k=0 (standard SFT protocol, avoids OOM from 3× longer prompts)
- **Masking — PLANNED, NOT YET WIRED:** table/column names masked to canonical tokens for retrieval-similarity scoring only; demos shown in prompt must always be unmasked

🔴 **Demo pool = TRAIN data, never the test set.** The ICL pool is the model's own
training examples — a client's private `Qᵢ` (`client_i_train.csv`) for per-client
and federated models, or the pooled centralized train set (`centralized/train.csv`)
for the centralized baselines B3/B4. The frozen test set (`centralized/test.csv` =
Spider dev) is **never** a demo source. Because test DBs are schema-disjoint from
train (verified: 0 overlap), retrieval is always **cross-schema** (train demos →
unseen test query) and the query is never in the pool → **no leave-one-out**. The
RQ2 mechanism is exactly this: the Global SLM's general skill + cross-schema demos
carry SQL-pattern (skeleton) structure to an unseen schema, not schema-specific answers.

**Per-arm pool + reporting (eval):**

| Arm | model | demo pool | reported |
|---|---|---|---|
| base B0 floor | base | k=0 (no ICL) | single |
| `slm_only` B2 | per-client adapter `Mᵢ` | client_i pool | mean±std over K |
| `ab3_fedavg` Ab3 | one global model | each client pool (K evals) | mean±std over K |
| `m_g` method | one global `M_G` | each client pool (K evals) | mean±std over K |
| B3 Centralized-FT | centralized | k=0 (no ICL) | single |
| B4 Centralized-ICL | centralized | centralized pool | single |

Global federated arms (`M_G`, `ab3_fedavg`) are deployed once **per client** (each org
runs the shared global model with its own private demos) and reported as mean±std —
keeps the privacy story end-to-end and yields per-client variance for free. `M_G − B3`
gap therefore folds in both the federation cost and the private-pool restriction
(B3 sees the full centralized pool) — the honest federated-vs-centralized gap.

Builder = `fedicl_sql/retrieval/pool.py`; eval = `experiments/eval_arms/run.py`.

### 5.4 ICL Prompt Constructor

```
σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q
```

- `q` — NL question
- `S` — serialized schema (DDL)
- `I` — system instruction ("expert SQL generator")
- `Q` — top-k retrieved demonstrations (NL + SQL, unmasked) from Qᵢ

### 5.5 Local SLM Student `Mᵢ` — Qwen2.5-1.5B-Instruct + LoRA

- Initialized from `M_G` (server broadcast) each round
- Generates: predicted SQL `ŝ` (+ optional reasoning)
- **LoRA fp16 on both CUDA and MPS** (training always fp16 — no 4-bit during training). 4-bit available for inference-only eval via `StudentModel`.

### 5.6 Local Training (Distillation)

**Total loss (Fig.1 verbatim):**

```
L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec
```

| Term | Definition | Data source |
|---|---|---|
| `L_SQL` | CE(student, gold SQL) | private `Qᵢ` — supervised gold labels |
| `L_KD` | CE(student, teacher CoT⊕SQL) + λ·KL_τ(student ‖ teacher top-K) | private `Qᵢ` — local teacher targets |
| `L_struct` | CE on skeleton-token subsequence (SQL clause keywords) | from L_SQL / L_KD target |
| `L_exec` | exec-match target filter (non-differentiable → data gate) | exec against gold during target generation |

**Single-pass training objective — one sequence per Qᵢ example:**

```
for each (q, gold_sql) in Qᵢ:
    if teacher_target exists AND exec_correct:
        target  = CoT⊕teacher_sql      (source = "kd")
        logprobs = teacher top-K        (soft-KL active)
    else:
        target  = gold_sql              (source = "gold")
        logprobs = None                 (KL term = 0)
```

Every question appears **exactly once**. No double-pass, no implicit upweighting of exec-correct examples. `exec_correct` ensures teacher_sql is semantically equivalent to gold_sql, so dropping gold CE on those examples loses nothing.

Pass `teacher_targets=[]` for B2/Ab3 arm (all examples → gold fallback).

**Why both parts matter:** L_SQL grounds the student on correct SQL; L_KD adds CoT reasoning and soft-probability dark knowledge the gold label lacks.

**ICL in training (k=0):** training prompts use k=0 demos (no retrieved examples in prompt). ICL is applied at **inference time only** (k=3). Rationale: k=3 during training multiplies prompt length ~3×, causing OOM on T4 14.5GB. The inference pipeline (retrieval → ICL prompt → M_G) is distinct from the training pipeline.

---

## 6. Federated Round Loop

```
Offline (once per client, before rounds):
  teacher_targets_i ← {(q, teacher_sql, reasoning, top_logprobs) : (q,sql) ∈ Qᵢ, exec_correct}
  [teacher model unloaded after this step]

Round t = 1 .. T:
  1. SERVER  broadcast M_G → all K clients
  2. CLIENT i (parallel):
       a. LoRA-train Mᵢ on L_sup(Qᵢ, k=0) + L_KD(teacher_targets_i, k=0)
       b. Δθᵢ ← encrypt + compress + DP-perturb (θᵢ − θ_{t-1})
       c. Upload Δθᵢ  [Weights Only]
  3. SERVER  θ_t ← FedAvg({Δθᵢ})  →  M_G ← base_SLM + θ_t

Inference (per client, after training):
       a. Retrieve top-k demos from own TRAIN pool Qᵢ (k=3, schema-aware; cross-schema to test, no LOO)
       b. Build ICL prompts σ(q, Sᵢ, I, Q)
       c. M_G.generate(prompt) → SQL
       [eval: repeat per client pool → mean±std for the global arms]

Return: M_G (global student), per-client adapters for local inference
```

---

## 7. Inference (deployment)

Each client runs `M_G` locally (no server, no teacher at inference time):
1. Schema encode `Sᵢ`
2. Retrieve top-k demos from local `Qᵢ`
3. Build prompt → `M_G.generate(prompt)` → SQL

No teacher API call at inference. Teacher cost is **one-time, offline, per-client**, amortized over all federated rounds.

---

## 8. Data flows summary

```
OFFLINE (per client i):
  private Qᵢ  ──►  Local Teacher M_T (7B)  ──►  teacher_targets_i (exec-filtered)
                    [unload teacher]

TRAINING (k=0, no demos in prompt):
  private Qᵢ  ──►  build_prompt(q, Sᵢ, [])  ──►  L_SQL (CE vs gold SQL)
  teacher_targets_i ──►  build_prompt(q, Sᵢ, [])  ──►  L_KD (CE+KL vs teacher)

INFERENCE (k=3, demos in prompt):
  Qᵢ  ──►  retrieval  ──►  ICL prompt σ(q, Sᵢ, I, Q)  ──►  M_G.generate() → SQL

Local Knowledge Cache (optional, Fig.1): not yet implemented.
```

---

## 9. Key design invariants (never violate)

1. **Private data never leaves client.** `Sᵢ`, raw rows, `Qᵢ`, teacher outputs — no outgoing data arrow.
2. **Teacher only touches client's own Qᵢ.** Never receives other clients' data or schemas. Never uploads outputs.
3. **Upload = Weights Only.** LoRA deltas, not full model, not data, not teacher targets.
4. **Training on Qᵢ is mandatory (gold + teacher).** Public-X-only training (old) → FedAvg no-op; now eliminated by design.
5. **Masking = retrieval scoring only.** Never put masked SQL in the generation prompt.
6. **One stack per comparison.** Mac-fp16 ≠ CUDA-fp16 — never compare cross-stack.
7. **Sequential VRAM.** Teacher inference (7B) → unload → student training (1.5B). Never simultaneous.
8. **Demo pool = TRAIN, never test.** ICL demos come from the model's own train data (per-client `Qᵢ` or centralized train). Test set is never a demo source → no leave-one-out. Retrieval is cross-schema (train→unseen-test). Violating this leaks near-answers and inflates EX.

---

## 10. Notation reference (canonical — §0 of detailed_plan)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) |
| `T` | # federated rounds (PoC: 2–3) |
| `k` | # ICL shots at inference (∈{1,3}; inverted-U at 5) |
| `E` | local epochs per round (1–2) |
| `λ₁…λ₄` | loss weights per Fig.1 |
| `M_T` | teacher LLM (Qwen2.5-7B-Instruct, **local on each client**) |
| `Mᵢ` | client-i student (Qwen2.5-1.5B) |
| `M_G` | global SLM (base + aggregated LoRA) |
| `Sᵢ, Qᵢ` | client-i private schema / NL-SQL pairs |
| `θ, Δθᵢ` | LoRA params / client-i delta |
| `τ` | KD temperature (soft-KL scaling) |
