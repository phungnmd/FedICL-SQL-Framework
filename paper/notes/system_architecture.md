# FedICL-SQL — System Architecture

> Grounded in: `fig_architecture_source.png` (mechanism ground truth) · `fedicl_sql_outline.pdf` (section structure) · `detailed_plan.md` (spec).
> Maps directly to §3 of the paper. **Fig.1 wins on any mechanism dispute.**

---

## 1. Problem Setting

A set of `K` organizations (clients) each hold:
- A **private relational database** with schema `Sᵢ = {tables, columns, FK-paths}` — never leaves the client.
- A **private NL→SQL example store** `Qᵢ = {(qₙ, sₙ)}` (natural-language questions + gold SQL) — never leaves the client.

**Goal:** collaboratively train a lightweight local SQL model that generalizes to unseen schemas, while transmitting only encrypted, DP-perturbed model weights — no raw data, no schema, no private SQL.

---

## 2. Three-Plane Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│  FEDERATED COORDINATION SERVER  (Cloud)                             │
│                                                                     │
│  ┌──────────────────┐  reasoning+SQL  ┌─────────────────────────┐  │
│  │ Global LLM       │ ──────────────► │  ICL Hub                │  │
│  │ Teacher (M_T)    │   (on public X) │  (Demonstration         │  │
│  │ Qwen2.5-72B      │                 │   Repository)           │  │
│  │ • gen SQL+CoT    │                 │  • schema-aware pool    │  │
│  │ • produce logprobs│                │  • retrieved top-k demos│  │
│  └──────────────────┘                 └─────────────────────────┘  │
│         │ KD targets (teacher_targets.qwen72b.*)                    │
│         ▼                                                           │
│  ┌────────────────────────────────────────────────────────────────┐ │
│  │  Federated Aggregation Engine                                  │ │
│  │  FedAvg / FedProx: θ_t ← θ_{t-1} + (1/K) Σᵢ Δθᵢ             │ │
│  │  → Global SLM M_G (Qwen2.5-1.5B + aggregated LoRA adapter)    │ │
│  └────────────────────────────────────────────────────────────────┘ │
└────────────────────┬──────────────────────────────┬─────────────────┘
                     │ ▼ DOWN (blue)                 │ ▲ UP (purple dashed)
                     │  Global params M_G            │  Encrypted LoRA deltas Δθᵢ
                     │  + ICL Hub demos              │  (Weights Only)
┌────────────────────▼──────────────────────────────┴─────────────────┐
│  SECURE & PRIVACY-PRESERVING COMMUNICATION                           │
│  SSL/TLS · Secure Aggregation · DP (gradient perturbation) · Masking│
└────────────────────┬──────────────────────────────┬─────────────────┘
                     │ ▼                             │ ▲
┌────────────────────▼──────────────────────────────┴─────────────────┐
│  CLIENT / ORGANIZATION i  (on-premise)                               │
│                                                                      │
│  [Local Data & Schema]──►[Schema Encoder]──►[Retrieval]──►[ICL Prompt Constructor]
│   Sᵢ (private schema)     Schema embedding   FAISS top-k  σ(q,S,I,Q)=q⊕S⊕I⊕Q
│   Qᵢ (private NL/SQL)     (BGE-small)        from Qᵢ∪G                │
│                                                                      │
│                                              ┌──────────────────────▼──┐
│                                              │  Local SLM Student Mᵢ   │
│                                              │  Qwen2.5-1.5B + LoRA    │
│                                              │  → predicted SQL + CoT   │
│                                              └──────────────┬──────────┘
│                                                             │
│  ┌──────────────────────────────────────────────────────────▼────────┐ │
│  │  Local Training (Distillation)                                    │ │
│  │  L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec              │ │
│  │      ↑ gold Qᵢ   ↑ teacher targets X    ↑ skeleton  ↑ exec-filter│ │
│  └───────────────────────────────────────────────────────────────────┘ │
│  → LoRA delta Δθᵢ → encrypt+compress+DP-perturb → upload              │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 3. Server Components

### 3.1 Global LLM Teacher `M_T` — Qwen2.5-72B-Instruct (DeepInfra)

**Role:** SQL expert running **offline, once** on the **public set `X`** only. Never sees client private data.

**Outputs per item `x ∈ X`:**
- `reasoning` — chain-of-thought derivation steps (CoT)
- `ŝ_T` — teacher SQL (exec-validated against gold)
- `top_logprobs[20]` — per-token top-20 token probabilities → enables soft-KL KD

**Exec filter:** only items where `Exec(ŝ_T, D_X) = Exec(gold, D_X)` (exec-correct) enter the KD target cache. Items that fail exec validation are dropped.

**Two downstream feeds (both from M_T's public-X run):**
1. **→ ICL Hub:** `(q, schema, reasoning, ŝ_T)` tuples as high-quality demonstrations
2. **→ KD targets cache:** `teacher_targets.qwen72b.csv` + `teacher_targets.qwen72b.logprobs.jsonl`

### 3.2 ICL Hub `G` — Demonstration Repository

**Role:** server-side pool of teacher-authored public demonstrations, broadcast DOWN to all clients each round.

**Content:** teacher-generated `(question, schema, reasoning, SQL)` on public schemas `X`.

**Not:** cross-client private demos. Private client demos `Qᵢ` stay local and are never shared.

### 3.3 Federated Aggregation Engine

**Algorithm:** FedAvg / FedProx.

```
θ_t  ←  θ_{t-1}  +  (1/K) Σᵢ Δθᵢ
M_G  ←  base_SLM + θ_t
```

FedProx adds a proximal term `(μ/2)||θ - θ_{t-1}||²` per client to control drift under high non-IID (use if convergence is unstable).

**Uploads only LoRA deltas `Δθᵢ`** (not full weights) — bounded communication cost per round.

### 3.4 Global SLM `M_G`

Base `Qwen2.5-1.5B-Instruct` + aggregated LoRA adapter `θ_t`. Broadcast back to all clients at the start of each round. Lightweight enough to run locally at inference (<6 GB VRAM).

---

## 4. Communication Band

| Direction | What crosses | Protected by |
|---|---|---|
| **DOWN** (server → client) | Global SLM params `M_G` + ICL Hub demo slice | SSL/TLS + Secure Aggregation |
| **UP** (client → server) | LoRA delta `Δθᵢ` only (**Weights Only**) | Encrypt + compress + **DP gradient perturbation** + Secure Aggregation |
| **Never transmitted** | Raw rows, schema `Sᵢ`, private examples `Qᵢ`, full model weights | — (stays local by design) |

**Privacy mechanisms (Fig.1, 4 boxes):**
1. **SSL/TLS** — secure transmission channel
2. **Secure Aggregation** — server aggregates without seeing individual Δθᵢ
3. **Differential Privacy (Gradient Perturbation)** — Gaussian noise + clipping on Δθᵢ before upload; report (ε, EX) at Stage-B
4. **De-identification & Masking** — schema identifier masking for retrieval-similarity scoring

---

## 5. Client Components

### 5.1 Local Data & Schema (private, never leaves)

- `Sᵢ` — relational schema (tables, columns, types, FK paths)
- `Qᵢ` — NL/gold-SQL pairs on `Sᵢ`'s databases

### 5.2 Schema Encoder + Retrieval

- Schema serialized as DDL (types + FK join paths) for prompt `S`
- **BGE-small-en + FAISS** retrieval — pool depends on stage:
  - **PoC (Stage-A):** `Qᵢ` only (G not yet built — requires teacher targets)
  - **Stage-B:** `Qᵢ ∪ G` (private demos + ICL Hub teacher demos broadcast from server)
- Top-`k` at **inference/eval**: `k=3` (k ∈ {1,3} per [4]; inverted-U at k=5). At **training**: k=0 (see §5.5 note)
- **Masking = retrieval-only** ([4] §3.6): table/column names masked to canonical tokens for similarity scoring; demos shown in the prompt are **always unmasked**

### 5.3 ICL Prompt Constructor

```
σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q
```

- `q` — NL question
- `S` — serialized schema (DDL)
- `I` — system instruction ("expert SQL generator")
- `Q` — top-k retrieved demonstrations (NL + SQL, unmasked)

### 5.4 Local SLM Student `Mᵢ` — Qwen2.5-1.5B-Instruct + LoRA

- Initialized from `M_G` (server broadcast) each round
- Generates: predicted SQL `ŝ` (+ optional reasoning)
- **LoRA fp16 on both CUDA and MPS** (training always fp16 — no 4-bit quantization during training). 4-bit (`LOAD_IN_4BIT=1`) is available for inference-only eval via `StudentModel` but is not used in the training path.

### 5.5 Local Training (Distillation)

**Total loss (Fig.1 verbatim):**

```
L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec
```

| Term | Definition | Data source |
|---|---|---|
| `L_SQL` | CE(student, gold SQL) | private `Qᵢ` (supervised) |
| `L_KD` | CE(student, teacher CoT⊕SQL) + λ·KL_τ(student ‖ teacher top-20) | public `X`, teacher targets |
| `L_struct` | CE on skeleton-token subsequence (SQL clause keywords) | from `L_SQL`/`L_KD` target |
| `L_exec` | **exec-match target filter** (non-differentiable → realized as data gate) | exec against gold during target generation |

**Two-part training objective per client:**

```
L_i = L_sup(private Qᵢ)  +  L_KD(public X + teacher targets)
```

- `L_sup` uses gold labels from `Qᵢ` (own schema, org-specific — makes deltas heterogeneous)
- `L_KD` uses teacher's CoT⊕SQL text (CE hard) + top-20 logprobs (KL soft, temperature τ)

**Why both parts matter:** if clients train on `X` alone (no `Qᵢ`), all deltas are near-identical → FedAvg degenerates to single-client training → RQ1 dies (FedAvg-no-op).

**ICL in training (implementation note):** Training prompts use **k=0** (no retrieved demos) — consistent with FedCoLLM [8] engine anchor and standard NL2SQL fine-tuning practice (DAIL-SQL, SQL-Coder). ICL is applied at **inference time only** (`k=3`). Rationale: (1) adding k=3 demos to every training sequence multiplies prompt length ~3×, causing OOM on T4 14.5GB; (2) Qwen2.5-1.5B-Instruct handles ICL prompts without in-training exposure due to instruction pre-training. This is a deliberate simplification noted in §3.6 of the paper. The Fig.1 pipeline (Retrieval → ICL Prompt → SLM → Training) describes the **inference pipeline**; training follows the supervised fine-tuning protocol of [8].

---

## 6. Federated Round Loop

```
Offline (once, cached):
  teacher_targets ← {(x, r̂_T⊕ŝ_T, top_logprobs) : x ∈ X, exec_correct(x)}
  ICL_Hub G ← teacher demos on X

Round t = 1 .. T:
  1. SERVER  broadcast M_G (+ ICL Hub slice G) → all K clients
  2. CLIENT i (parallel):
       a. LoRA-train Mᵢ on L_sup(Qᵢ, k=0) + L_KD(X, teacher_targets, k=0)
          [training prompts: σ(q, Sᵢ, I, Q=[]) — no demos, standard SFT protocol [8]]
       b. Δθᵢ ← encrypt + compress + DP-perturb (θᵢ − θ_{t-1})
       c. Upload Δθᵢ  [Weights Only]
  3. SERVER  θ_t ← FedAvg({Δθᵢ})  →  M_G ← base_SLM + θ_t

Inference (per client, after training):
       a. Retrieve top-k demos from Qᵢ (PoC) or Qᵢ ∪ G (Stage-B)
       b. Build ICL prompts σ(q, Sᵢ, I, Q)  with k=3
       c. M_G.generate(prompt) → SQL

Return: M_G (global student), per-client adapters for local inference
```

---

## 7. Inference (deployment)

Each client runs `M_G` locally (no server, no teacher at inference time):
1. Schema encode `Sᵢ`
2. Retrieve top-k demos from local `Qᵢ` (+ cached ICL Hub)
3. Build prompt → `M_G.generate(prompt)` → SQL

No teacher API call at inference. Teacher cost is **one-time, offline**, amortized over all clients and all rounds.

---

## 8. Data flows summary

```
public X  ──►  M_T teacher  ──►  teacher_targets (CoT+SQL+logprobs, exec-filtered)
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                         ICL Hub G            KD loss L_KD
                         (demos, ↓ broadcast) (client-side training)

private Qᵢ  ──►  L_sup (supervised CE, stays local)
                  +
             Qᵢ ∪ G  ──►  retrieval  ──►  ICL prompt  ──►  L_SQL / inference
```

---

## 9. Key design invariants (never violate)

1. **Private data never leaves client.** `Sᵢ`, raw rows, `Qᵢ` — no outgoing arrow.
2. **Teacher only touches public `X`.** Never receives client queries or schema.
3. **Upload = Weights Only.** LoRA deltas, not full model, not data.
4. **Training on `Qᵢ` is mandatory.** Public-X-only training → FedAvg no-op.
5. **Masking = retrieval scoring only.** Never put masked SQL in the generation prompt.
6. **One stack per comparison.** Mac-fp16 ≠ CUDA-4bit — never compare cross-stack.

---

## 10. Notation reference (canonical — §0 of detailed_plan)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) |
| `T` | # federated rounds (PoC: 2–3) |
| `k` | # ICL shots (∈{1,3}; inverted-U at 5) |
| `E` | local epochs per round (1–2) |
| `λ₁…λ₄` | loss weights per Fig.1 |
| `M_T` | teacher LLM (Qwen2.5-72B) |
| `Mᵢ` | client-i student (Qwen2.5-1.5B) |
| `M_G` | global SLM (base + aggregated LoRA) |
| `Sᵢ, Qᵢ` | client-i private schema / NL-SQL pairs |
| `X` | public KD+ICL set (shared, no private schema) |
| `G` | global ICL Hub (teacher demos on X) |
| `θ, Δθᵢ` | LoRA params / client-i delta |
| `τ` | KD temperature (soft-KL scaling) |
