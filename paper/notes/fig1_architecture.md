# Fig. 1 — Architecture of the Proposed Framework (canonical transcription)

Source image: `../figures/fig_architecture_source.png` (locked user input — DO NOT modify the PNG). This MD is the text transcription used as the **source of truth for the method's mechanism**. When plan/figure conflict on mechanism → figure wins (it is the approved architecture); when outline/figure conflict on section structure → outline wins.

---

## Three planes

```
SERVER (Federated Coordination Server / Cloud)
  ├─ Global LLM Teacher (SQL Expert)
  ├─ In-Context Learning Hub (Demonstration Repository)
  ├─ Federated Aggregation Engine
  └─ Global SLM (Student Model)
        │  ▲
        │ Global Model Broadcast (Parameters)   ▲ Encrypted Model Updates (Weights Only)
        ▼  │
SECURE & PRIVACY-PRESERVING COMMUNICATION
  SSL/TLS · Secure Aggregation · Differential Privacy (Gradient Perturbation) · De-identification & Masking
        │  ▲
        ▼  │
CLIENTS (Client / Organization 1 .. K)
  Local Data & Schema → Schema Encoder → Retrieval → ICL Prompt Constructor
    → Local SLM (decode) → predicted SQL + reasoning
    → Local Training (Distillation): SQL loss + KD loss + Structure loss + Execution loss → Total Loss
    → Local Model Update (Weights Only), Encrypted & Compressed Upload
  Local Knowledge Cache (optional): recent examples / rules / execution feedback
```

## Server components (verbatim from figure)

**Global LLM Teacher (SQL Expert)**
- Understand natural language and database schema
- Generate high-quality SQL
- Produce reasoning steps and explanations
- **Provide demonstrations for ICL and distillation**
- Emits: *Reasoning Guidance* →

**In-Context Learning Hub (Demonstration Repository)**
- Schema-aware example pool
- Retrieval & ranking
- Diversity & relevance
- Prompt construction
- Inset example box: *"Example (Schema + NL + SQL) — Schema: Table, Column, …; Q: How many …?; SQL: SELECT …"*
- Emits: *Selected Examples & Prompts* (orange = Example/Prompt Flow per legend)
- **Repository is TEACHER/public-sourced** (fed by the teacher's "provide demonstrations" output), broadcast down to clients. NOT a cross-client private-demo store.

**Federated Aggregation Engine**
- **Secure aggregation (FedAvg/FedProx)**
- **Update global SLM (student)**
- **Broadcast global parameters**
- Client selection & scheduling
- Convergence monitoring

**Global SLM (Student Model)**
- Lightweight · Efficient · Deployable
- Emits: *Global Model Broadcast (Parameters)* ↓ to clients

## Communication band (verbatim, 4 boxes)

1. Secure Transmission (SSL/TLS) · 2. Secure Aggregation **(No raw data exposure)** · 3. **Differential Privacy (Gradient Perturbation)** · 4. **Prompt & Schema Privacy (De-identification & Masking)**.

## Client components (Client / Organization 1 … K — 6 numbered boxes + 2 bottom boxes)

1. **Local Data & Schema** — *Local Database (Schema Sᵢ)* + **NL-Query / SQL Pairs (Private Data)** ← the figure explicitly draws the client's private supervised set `Qᵢ` (grounds the `L_sup`/SQL-loss-on-gold term; never leaves client)
2. **Schema Encoder** — Schema Graph Encoder → Schema Embedding
3. **Retrieval Module** — Similarity Search (Query + Schema), Top-k Example Selection → Retrieved Examples **(Schema + NL + SQL)**
4. **ICL Prompt Constructor** — Assemble Prompt: Schema …, Example 1 (NL, SQL), Example 2 (NL, SQL), …, Question: `<NL>`
5. **Local SLM (Student)** — Generate SQL (Decoder) → Predicted SQL + Reasoning
6. **Local Training (Distillation)** — SQL Loss (`L_SQL`) + KD Loss (`L_KD`) + Structure Loss (`L_struct`) + Execution Loss (`L_exec`); **Total Loss box, verbatim formula:**

   `L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec`

   (gradient training, not frozen — §3.7 must present this exact λ-weighted form, then define each term; our implementation realizes `λ₄·L_exec` as **exec-match target filtering** since SQL execution is non-differentiable — own that divergence explicitly in §3.7)
7. **Local Model Update (Weights Only)** — Encrypted & Compressed Upload ↑ to server
8. **Local Knowledge Cache (Optional)** — Recent Examples / Rules / Execution Feedback

## Legend (Flows) panel (bottom-right — was missing from this transcription)

- **Reasoning / Guidance Flow** (purple solid)
- **Example / Prompt Flow** (orange)
- **Model Broadcast Flow** (blue)
- **Encrypted Upload Flow** (purple dashed)
- **Local Processing Flow** (green dashed)

Five distinct flow types → §3.2 framework-overview prose should name them when walking the figure.

## Figure caption (verbatim — reuse as the paper's Fig.1 caption base)

> *FedICL-SQL: A Novel Federated Large-Small Language Model Framework with In-Context Learning for Natural Language to SQL. Multiple organizations collaboratively train a lightweight Text-to-SQL model without sharing data. Our framework leverages a powerful LLM teacher, schema-aware in-context learning, and federated knowledge distillation to achieve high accuracy while preserving privacy and reducing communication and deployment costs.*

## Key Innovations panel (right)

1. Privacy-Preserving Federated Learning for Text-to-SQL
2. Large-Teacher to Small-Student Knowledge Transfer
3. Schema-Aware In-Context Learning
4. Cross-Schema Generalization & Adaptation
5. Communication-Efficient Training & Deployment
6. High Execution Accuracy with Lower Cost

---

## What the figure commits us to (mechanism implications)

| Mechanism in figure | Implication for method/plan |
|---|---|
| Aggregation = **FedAvg/FedProx over SLM weights**; **Global SLM** broadcast | Federation engine is **PARAMETRIC** (trained global SLM via weight aggregation), not parameter-free demo-sharing. This is the headline loop. |
| Client **Local Training (Distillation)** with SQL+KD+Structure+Exec loss | Students are **LoRA-trained**, not frozen+ICL-only. KD loss is on-client. |
| **"Weights Only"** upload + **"Parameters"** broadcast (both encrypted/compressed) | What crosses the wire = **model weights/LoRA deltas** (encrypted, DP-noised). **NOT** raw data, NOT schemas, NOT client-private demos. |
| **Differential Privacy (Gradient Perturbation)** | DP is a *first-class* privacy mechanism on the weight updates, not "optional." |
| ICL Hub = **teacher/public-sourced demos** → clients | The shared demonstration set is the **public set X**, authored by the teacher. Valid. (Attempt-1's error was sharing *client-private* demos cross-client — different thing.) |
| Teacher "provide demonstrations for ICL **and distillation**" | Teacher feeds BOTH the ICL Hub (demos) and the distillation loss (KD targets). |
| **No** answer-vote / Fusion-LM box anywhere | Fed-ICL answer-fusion is **NOT** the figure's engine. Keep it only as a parameter-free **baseline/variant** for comm-cost comparison, never as the primary method. |
| "Cross-Schema Generalization & Adaptation" in innovations | Treat as generalization through the **Global SLM + schema-aware local ICL**, not as permission to share client-private cross-schema demos. |

## Privacy claim (corrected to match figure)

- **Stays local:** raw rows, database, schema (Local Data & Schema box never has an outgoing data arrow).
- **Crosses the wire:** model updates — *Weights Only*, encrypted + compressed + DP-perturbed; global SLM parameters on broadcast.
- **Correct claim:** *"No raw data or schema leaves the client; only encrypted, DP-noised model-update weights (LoRA deltas) are transmitted."*
- **Wrong claim (do not use):** "no full weights leave the client" — figure transmits weights. Strong claim is about *data/schema*, not weights.

## Outline §3 ↔ figure mapping

| Outline §3 subsection | Figure component |
|---|---|
| 3.1 Problem Formulation | (notation) |
| 3.2 Framework Overview | three planes |
| 3.3 Global LLM Teacher | Global LLM Teacher (SQL Expert) |
| 3.4 Local SLM Student | Local SLM (decode) + Global SLM |
| 3.5 Teacher–Student Collaboration | Reasoning Guidance → ; teacher demos → ICL Hub + KD loss |
| 3.6 Schema-Aware ICL | Schema Encoder + Retrieval + ICL Prompt Constructor + ICL Hub |
| 3.7 Federated SQL Knowledge Distillation | Local Training (Distillation) losses + teacher KD targets |
| 3.8 Federated Optimization | Federated Aggregation Engine (FedAvg/FedProx, global SLM, broadcast) |
