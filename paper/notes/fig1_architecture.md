# Fig. 1 — Architecture of the Proposed Framework (canonical transcription)

Source image: `../figures/fig_architecture_source.png` (locked user input — DO NOT modify the PNG). This MD is the text transcription used as the **source of truth for the method's mechanism**. When plan/figure conflict on mechanism → figure wins (it is the approved architecture); when outline/figure conflict on section structure → outline wins.

> **Architecture re-aligned 2026-06-16:** teacher moved from server-side cloud API to **client-side local 7B model**. Public set X and ICL Hub G removed. See `system_architecture.md` for full detail.

---

## Three planes

```
SERVER (Federated Coordination Server)
  ├─ Federated Aggregation Engine (FedAvg / FedProx)
  └─ Global SLM M_G (Qwen2.5-1.5B + aggregated LoRA)
        │  ▲
        │ Global Model Broadcast (Parameters)   ▲ Encrypted Model Updates (Weights Only)
        ▼  │
SECURE & PRIVACY-PRESERVING COMMUNICATION
  SSL/TLS · Secure Aggregation · Differential Privacy (Gradient Perturbation) · De-identification & Masking
        │  ▲
        ▼  │
CLIENTS (Client / Organization 1 .. K)
  Local Data & Schema (Sᵢ, Qᵢ — never leaves client)
  Local Teacher M_T (Qwen2.5-7B, offline per-client on Qᵢ) → per-client teacher_targets
  Schema Encoder → Retrieval (Qᵢ only) → ICL Prompt Constructor
    → Local SLM Student Mᵢ (decode) → predicted SQL + reasoning
    → Local Training (Distillation): SQL loss + KD loss + Structure loss + Exec filter → Total Loss
    → Local Model Update (Weights Only), Encrypted & Compressed Upload
  Local Knowledge Cache (optional): recent examples / rules / execution feedback
```

## Server components

**Federated Aggregation Engine**
- Secure aggregation (FedAvg / FedProx)
- Update global SLM (student)
- Broadcast global parameters
- Client selection & scheduling
- Convergence monitoring

**Global SLM M_G (Student Model)**
- Lightweight · Efficient · Deployable (Qwen2.5-1.5B + LoRA)
- Emits: *Global Model Broadcast (Parameters)* ↓ to clients

> **Removed from server:** Global LLM Teacher and ICL Hub are no longer server components. The teacher runs locally on each client.

## Communication band (4 privacy mechanisms)

1. Secure Transmission (SSL/TLS)
2. Secure Aggregation **(no raw data exposure)**
3. **Differential Privacy (Gradient Perturbation)** — on LoRA deltas before upload
4. **Prompt & Schema Privacy (De-identification & Masking)**

| Direction | Content | Protected by |
|---|---|---|
| **DOWN** (server → client) | Global SLM params M_G | SSL/TLS + Secure Aggregation |
| **UP** (client → server) | LoRA delta Δθᵢ (**Weights Only**) | Encrypt + compress + DP gradient perturbation |
| **NEVER transmitted** | Raw rows, schema Sᵢ, private Qᵢ, teacher outputs | Stays local by design |

## Client components

1. **Local Data & Schema** — *Local Database (Schema Sᵢ)* + **NL-Query / SQL Pairs (Private Data Qᵢ)** ← private supervised set; never leaves client

2. **Local Teacher M_T (Qwen2.5-7B-Instruct, offline per-client)**
   - Runs **offline once per client** on the client's own private Qᵢ before federated rounds begin
   - Never sees other clients' data; never uploads outputs to server
   - Outputs per item: `reasoning` (CoT), `teacher_sql` (exec-validated), `top_logprobs[K]`
   - Exec filter: only items where `Exec(teacher_sql) = Exec(gold)` enter KD target cache
   - Stored locally: `client_i_teacher_targets.csv` + `client_i_teacher_targets.logprobs.jsonl`
   - VRAM: loaded for inference, then `unload()` before student LoRA training (sequential)

3. **Schema Encoder** — Schema DDL → Schema Embedding (BGE-small)

4. **Retrieval Module** — Similarity Search (Query + Schema), Top-k from **Qᵢ only**

5. **ICL Prompt Constructor** — σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q

6. **Local SLM Student Mᵢ** — Qwen2.5-1.5B + LoRA → Predicted SQL + Reasoning

7. **Local Training (Distillation)** — verbatim loss:

   `L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec`

   | Term | Data source | Signal |
   |---|---|---|
   | `L_SQL` | Private Qᵢ (gold SQL) | Own schema, org-specific skill |
   | `L_KD` | Private Qᵢ (teacher CoT⊕SQL + top-K logprobs) | Dark knowledge, CoT reasoning |
   | `L_struct` | Skeleton tokens from above | SQL clause structure |
   | `L_exec` | Exec-match filter on teacher targets (non-differentiable) | Data quality gate |

   Same Qᵢ examples appear in both L_SQL (gold labels) and L_KD (teacher labels, exec-filtered).

8. **Local Model Update (Weights Only)** — Encrypted & Compressed Upload ↑

9. **Local Knowledge Cache (Optional)** — Recent Examples / Rules / Execution Feedback

## Figure caption (updated)

> *FedICL-SQL: A Novel Federated Large-Small Language Model Framework with In-Context Learning for Natural Language to SQL. Multiple organizations collaboratively train a lightweight Text-to-SQL model without sharing data. Each client runs a local 7B LLM teacher on its own private data to generate KD targets, then LoRA-trains a 1.5B student on gold + teacher supervision. Only encrypted, DP-perturbed LoRA deltas cross the wire to the server for FedAvg aggregation. The resulting Global SLM is deployed locally with schema-aware ICL — no cloud API needed at inference.*

## Key Innovations panel

1. Privacy-Preserving Federated Learning for Text-to-SQL
2. **Client-Side** Local LLM Teacher → Small Student Knowledge Transfer (no cloud API)
3. Schema-Aware In-Context Learning (retrieval from own Qᵢ)
4. Cross-Schema Generalization via Global SLM
5. Communication-Efficient Training & Deployment (LoRA deltas only)
6. High Execution Accuracy with Lower Cost

---

## What the figure commits us to (mechanism implications)

| Mechanism in figure | Implication for method/plan |
|---|---|
| **Teacher placement: CLIENT (local 7B)** | Teacher is **NOT on the server**; runs **offline per-client** on private Qᵢ; no cloud API. |
| Aggregation = **FedAvg/FedProx over SLM weights**; **Global SLM** broadcast | Federation engine is **PARAMETRIC** (trained global SLM via weight aggregation). |
| Client **Local Training (Distillation)** with SQL+KD+Structure+Exec loss | Students are **LoRA-trained**. Both L_SQL (gold) and L_KD (teacher) use same private Qᵢ. |
| **"Weights Only"** upload + **"Parameters"** broadcast (both encrypted) | What crosses the wire = **LoRA deltas** only. Teacher outputs stay on-premise. |
| **Differential Privacy (Gradient Perturbation)** | DP on LoRA deltas before upload — first-class privacy mechanism. |
| **No ICL Hub (G) on server** | Retrieval pool = Qᵢ only. No cross-client demo sharing. No server-side teacher demos. |
| **No public X pool** | All Spider train DBs go to clients. More private data per client. |

## Privacy claim (corrected to match new architecture)

- **Stays local:** raw rows, database, schema (Sᵢ, Qᵢ), teacher model, teacher outputs (targets, logprobs) — never leaves client
- **Crosses the wire:** LoRA deltas only — *Weights Only*, encrypted + compressed + DP-perturbed; global SLM params on broadcast
- **Correct claim (new):** *"No raw data, schema, or teacher outputs leave the client. The teacher model runs fully on-premise. Only encrypted, DP-noised LoRA weight updates are transmitted to the server."*
- **Stronger than before:** eliminates even the public-X teacher API call; zero external network traffic during KD target generation.

## Outline §3 ↔ figure mapping (updated)

| Outline §3 subsection | Figure component |
|---|---|
| 3.1 Problem Formulation | (notation) |
| 3.2 Framework Overview | three planes |
| 3.3 Local LLM Teacher (Client-Side) | Local Teacher M_T (client) |
| 3.4 Local SLM Student | Local SLM Student + Global SLM |
| 3.5 Teacher–Student Collaboration | L_KD path: teacher targets → student training |
| 3.6 Schema-Aware ICL | Schema Encoder + Retrieval (Qᵢ only) + ICL Prompt Constructor |
| 3.7 Federated SQL Knowledge Distillation | Local Training losses + per-client teacher targets |
| 3.8 Federated Optimization | Federated Aggregation Engine (FedAvg/FedProx, global SLM, broadcast) |
