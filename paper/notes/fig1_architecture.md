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
  Local Teacher M_T (Qwen2.5-7B, frozen, online per step) → soft labels p over ŷ
  Schema Encoder → Retrieval (Qᵢ only) → ICL Prompt Constructor
    → Local SLM Student Mᵢ → mask(y,ρ) + rewrite → ŷ → predicted SQL
    → Local Training (Distillation): λ(t)·MLE + (1-λ(t))·RKL → Total Loss
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

2. **Local Teacher M_T (Qwen2.5-7B-Instruct, online, frozen, runs on BIRD public)**
   - Runs **per training step** — one forward pass over `ŷ_bird` (student imperfect rewrite of BIRD gold SQL)
   - Frozen throughout. **Never sees `Qᵢ` or client's private schema `Sᵢ`**
   - Output per step: per-token logprob distribution `p` over `ŷ_bird` — soft labels for RKL loss
   - ICL for teacher: k=3 demos from **BIRD train** (question-only, `never_schema`) — no private data in teacher context
   - Never uploads outputs to server
   - VRAM: co-loaded with student (~17 GB total — A100 required; T4 PoC: 4-bit teacher ≈ 8 GB)

3. **Schema Encoder** — Schema DDL → Schema Embedding (BGE-small)

4. **Retrieval Module** — Similarity Search (Query + Schema), Top-k from **Qᵢ only**

5. **ICL Prompt Constructor** — σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q

6. **Local SLM Student Mᵢ** — Qwen2.5-1.5B + LoRA → Predicted SQL + Reasoning

7. **Local Training** — Dual-stream per step:

   **Stream 1 (FT):** `L_FT = CE(student, gold_sql)` on private `Qᵢ`, k=0

   **Stream 2 (KID on BIRD):** `mask(y_bird, ρ) → ŷ_bird` (student, k=0) → teacher forward with BIRD ICL k=3 → `p` → `L_KD = RKL(q‖p)`

   `L = λ₁ · L_FT  +  λ₂(t) · L_KD`

   | Term | Data | Signal |
   |---|---|---|
   | `L_FT` | Private `Qᵢ` (gold SQL) | Domain-specific supervised SQL |
   | `L_KD` | Public BIRD (teacher soft labels on `ŷ_bird`) | General SQL structural knowledge |
   | `λ₂(t)` | Alpha-decay | Soft label weight decreases as student matures |

8. **Local Model Update (Weights Only)** — Encrypted & Compressed Upload ↑

9. **Local Knowledge Cache (Optional)** — Recent Examples / Rules / Execution Feedback

## Figure caption (updated)

> *FedICL-SQL: A Novel Federated Large-Small Language Model Framework with In-Context Learning for Natural Language to SQL. Multiple organizations collaboratively train a lightweight Text-to-SQL model without sharing data. Each client trains via dual-stream learning: supervised FT on its own private data (Spider Qᵢ) and KID distillation on public BIRD data — the student generates imperfect SQL ŷ via masking and rewriting, the frozen local 7B teacher scores ŷ with BIRD ICL context, and a Reverse KL + alpha-decay loss transfers SQL structural knowledge. The teacher never accesses private client data. Only encrypted, DP-perturbed LoRA deltas cross the wire for FedAvg aggregation. The resulting Global SLM deploys locally with schema-aware ICL — no cloud API at inference.*

## Key Innovations panel

1. Privacy-Preserving Federated Learning for Text-to-SQL
2. **Dual-stream Training** — FT on private `Qᵢ` + KID on public BIRD; teacher never touches private data → absolute privacy
3. **KID-based Distillation in Federated Setting** — student mask+rewrite on BIRD → imperfect data ŷ + Reverse KL + alpha-decay; first applied to federated NL2SQL
4. **Schema-Aware ICL at Inference** — DAIL-SQL style, k=3 from own `Qᵢ`; cross-schema, privacy-preserving
5. Cross-Schema Generalization via Global SLM (FedAvg LoRA)
6. Communication-Efficient Training (LoRA deltas only, DP-perturbed)

---

## What the figure commits us to (mechanism implications)

| Mechanism in figure | Implication for method/plan |
|---|---|
| **Teacher placement: CLIENT (local 7B, frozen, on BIRD public)** | Teacher **never sees `Qᵢ`**; runs on public BIRD train per step; forward-only; no cloud API; never uploads. |
| Aggregation = **FedAvg/FedProx over SLM weights**; **Global SLM** broadcast | Federation engine is **PARAMETRIC** (trained global SLM via weight aggregation). |
| Client **Local Training — dual-stream** `L = λ₁·L_FT + λ₂(t)·L_KD` | **Stream 1:** FT on private `Qᵢ` (gold CE). **Stream 2:** KID on BIRD (`ŷ_bird` + teacher RKL). Students LoRA-trained. |
| **"Weights Only"** upload + **"Parameters"** broadcast (both encrypted) | What crosses the wire = **LoRA deltas** only. Teacher outputs stay on-premise. |
| **Differential Privacy (Gradient Perturbation)** | DP on LoRA deltas before upload — first-class privacy mechanism. |
| **No ICL Hub (G) on server** | Retrieval pool = Qᵢ only. No cross-client demo sharing. No server-side teacher demos. |
| **No public X pool** | All Spider train DBs go to clients. More private data per client. |

## Privacy claim (corrected to match new architecture)

- **Stays local:** raw rows, database, schema (Sᵢ, Qᵢ), teacher model, teacher soft labels (p over ŷ) — never leaves client
- **Crosses the wire:** LoRA deltas only — *Weights Only*, encrypted + compressed + DP-perturbed; global SLM params on broadcast
- **Correct claim:** *"No raw data, schema, or teacher outputs leave the client. The teacher model runs fully on-premise. Only encrypted, DP-noised LoRA weight updates are transmitted to the server."*
- **Privacy preserved:** imperfect data ŷ and soft labels p are generated and consumed locally per step; zero outbound traffic during distillation.

## Outline §3 ↔ figure mapping (updated)

| Outline §3 subsection | Figure component |
|---|---|
| 3.1 Problem Formulation | (notation) |
| 3.2 Framework Overview | three planes |
| 3.3 Local LLM Teacher (Client-Side) | Local Teacher M_T (client) |
| 3.4 Local SLM Student | Local SLM Student + Global SLM |
| 3.5 Teacher–Student Collaboration | KID path: student mask+rewrite → ŷ → teacher forward (with ICL) → p → RKL |
| 3.6 Schema-Aware ICL | Schema Encoder + Retrieval (Qᵢ only) + ICL Prompt Constructor |
| 3.7 Federated SQL Knowledge Distillation | KID distillation: λ(t)·MLE + (1-λ(t))·RKL, alpha-decay, imperfect data ŷ |
| 3.8 Federated Optimization | Federated Aggregation Engine (FedAvg/FedProx, global SLM, broadcast) |
