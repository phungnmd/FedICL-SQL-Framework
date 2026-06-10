# FedICL-SQL — Detailed Research & Writing Plan

**Paper:** *FedICL-SQL: A Novel Federated Large-Small Language Models Framework with In-Context Learning for Natural Language to SQL*
**Target venue:** International Arab Journal of Information Technology (IAJIT), WoS-Q3. IEEE-style two-column template.
**Authors:** Student + Quang-Hung Le (corresponding), Quy Nhon University.
**Date of plan:** 2026-06-07.
**Revised:** 2026-06-09 (see banner below).

---

## ⚠️ REVISION 2026-06-09 — corrected direction (READ FIRST)

P1 attempt 1 failed its core test and, on re-reading the references + outline, the **method design in §2 below was partly wrong**. This banner is the corrected source of truth for the method; the §2 subsections marked `[SUPERSEDED]` are kept for reference only. Full record of attempt 1: `fedicl-sql/docs/archive/p1-attempt1-cross-schema-demo-store/`.

### What was wrong

1. **Federation mechanism.** We built a shared **demo store `G`** that clients contribute masked `(q, SQL)` demos to, and retrieved cross-client demos into the prompt. **Fed-ICL [5] does not do this** — it shares each client's **answer to a shared common query**, fused server-side (majority-vote / Fusion-LM), iterated. Demos always stay local; only answers cross the wire.
2. **Masking misused.** We put masked SQL (`tbl1`, `col2`) into the prompt → the SLM copies the placeholders into its output → unexecutable SQL (3.3% EX). **Light-SQL [4] masking is retrieval-only**; demos shown to the model are unmasked.
3. **Cross-schema transfer is the wrong premise.** SQL is schema-coupled; demos from foreign schemas mislead execution (43% vs 50% zero-shot). Generalizing to a *random unseen DB* via shared demos is unsupported by any of Light-SQL [4], Fed-ICL [5], FedMKT [7], FedCoLLM [8].
4. **Wrong ordering / wrong test.** We deferred the **teacher to P2** and led with parameter-free demo-sharing — the weakest, least-supported config. And **TEST A1 (shared store → held-out EX) was never in the outline**; it was self-imposed. The outline's RQ1 is soft ("improve in federated environments") and **centers teacher–student KD** (4 of 6 §3 subsections).

### Corrected method (the model to build) — `[RE-ALIGNED TO FIG.1, 2026-06-09]`

Mechanism source of truth = `fig1_architecture.md` (transcription of the locked architecture PNG). Fig.1's aggregation engine is **FedAvg/FedProx over SLM weights** + **Global SLM broadcast** + on-client **distillation losses (SQL+KD+Structure+Exec)** → the engine is **PARAMETRIC**. The earlier "parameter-free demo-sharing primary" was an over-correction after attempt-1 and is withdrawn.

| Component | Mechanism | RQ | Grounding |
|---|---|---|---|
| **Federation engine (primary)** | **Parametric teacher→student KD.** Each client **LoRA-trains** its SLM on **own private `Qᵢ` (supervised CE) + shared public `X` (teacher-KD)** — `L_i = L_sup(Qᵢ) + L_KD(X)`, `L_KD = CE + λ·KL(τ) + β·skeleton-CE` over exec-filtered teacher targets; uploads **LoRA deltas only** (encrypted/compressed/DP-noised); server **FedAvg/SecureAvg** → **Global SLM `M_G`** broadcast. ⚠️ **The private-data term is mandatory** — train-on-`X`-only makes all deltas identical → FedAvg degenerates to single-client → RQ1 dies. Private schemas + rows never leave; only weights cross. | RQ1, RQ3 | Fig.1 engine; outline §3.7–3.8; **FedCoLLM [8]** (clients have private local data + LoRA-adapter FedAvg + global SLM + CE+λKL KD on aux set — the exact match). **FedMKT [7] does NOT apply here** → grounds P2 logit-KD only |
| **Novel (no ref backing) — flag as contribution + risk** | **(i) Exec-based KD-target filtering** (Fig.1 "Execution loss") — filter teacher SQL by execution before KD: **exec-match vs gold** in simulation (`X` labeled), exec-only in deployment; a data-selection step, NOT a gradient term. Exec-guidance itself is prior art → claim only the *federated-KD-filtering* angle. **(ii) Skeleton-token structure loss** — weighted CE on SQL clause/structural tokens (differentiable). **(iii) DP gradient perturbation** on LoRA deltas — none of [5][7][8] use DP. **Claim DP only if measured** (report ε vs EX + F5-with-DP); else → future work. | RQ3, privacy | Fig.1 only — our novelty |
| **KD variant (parameter-free)** | **Demo-level KD.** Teacher SQL on `X` distilled in-context (fine-tune-free) — cheap comparator to the parametric engine. | RQ3 | outline §3.7 |
| **Federation baseline (parameter-free)** | **Fed-ICL answer-fusion.** Clients propose SQL on a shared query set using own private demos; server fuses by execution-vote / Fusion-LM; iterate. **NOT in Fig.1** — comm-cost/convergence comparator only, never presented as the method. | RQ1 | Fed-ICL [5] |
| **ICL for generalization** | **Schema-aware retrieval, masking retrieval-only**, demos same/related schema, run **locally** per client. Prompt always shows **unmasked** demos. | RQ2 | Light-SQL [4] |
| **Shared demo repository (server)** | Fig.1 **ICL Hub** = **teacher/public-sourced** demos on `X`, broadcast to clients. Valid (≠ attempt-1's cross-client *private* demo store). | RQ2 | Fig.1 ICL Hub |
| **Cross-schema generalization (Fig.1 innovation)** | Generalize to **unseen schemas via the Global SLM's general SQL skill + schema-aware local ICL** on the held-out schema's *own* few demos — NOT via sharing private cross-schema demos. Test: `M_G` EX on held-out-schema questions vs SLM-only. | RQ2 | Fig.1 "Cross-Schema Generalization & Adaptation"; FedCoLLM [8] skill transfer |
| **(optional, secondary)** | Horizontal federation (clients share one schema → demo transfer valid) — side experiment. | RQ1 | — |
| **Negative finding** | Cross-schema generalization via **shared private-demo store `G`** failed (attempt-1) → report as motivation for the skill-transfer route above (Text-to-SQL needs schema-aligned demos, but *skill* transfers). | — | TEST A1 |

**Revised primary claim:** *A server-side LLM teacher distills SQL-generation skill into many on-premise SLM students — clients LoRA-train locally and the server FedAvg-aggregates a Global SLM over a shared public query set — improving Text-to-SQL across organizations that keep schemas and rows private, transmitting only encrypted DP-noised weight deltas (never raw data or schema), at a better efficiency/accuracy tradeoff than LLM-only or SLM-only.*

**STAGING LOCKED 2026-06-10, REV 2 (same day) — real teacher from day 1, two-stage GPU:**
- **Teacher = Qwen2.5-72B-Instruct (the outline model) for BOTH stages** via paid API (DeepInfra `Qwen/Qwen2.5-72B-Instruct` ≈ $0.4/M tok; full `X` ≈ 2.7M tok ≈ **$1–2**, whole-paper teacher budget < $10). The earlier "free-API stand-in" interim is **withdrawn** — teacher API cost is negligible, so PoC uses the real teacher and `teacher_targets.csv` is generated ONCE, no re-gen step, no non-headline-teacher caveat. (Groq Llama-3.3-70B targets already generated are kept as `teacher_targets.<provider>.csv` → free teacher-sensitivity data point.)
- **Stage A = P1′ PoC, ~$2, now.** Goal: pipeline works end-to-end + **directional** make-or-break signal. Real teacher targets + LoRA on free cloud GPU (Kaggle 30h/wk P100/2×T4 or Colab-free T4), `L=3`, **1 seed**, eval subset (~200 q/client), `K=2–3` rounds, `E=1`, **no DP**. Results flagged `stage=poc`, never headline.
- **Stage B = headline, after PoC positive + supervisor sign-off.** Paid GPU (Colab Pro / RunPod / Lambda A100-class), full matrix per triage tiers (§3.8), **≥3 seeds + significance**, DP measured (ε vs EX). Teacher targets reused as-is (same model both stages).
- **Gate between stages:** PoC make-or-break directional positive (`M_G` > SLM-only, `M_G` > train-on-X-only null) AND supervisor confirms §8 decisions. Negative PoC → diagnose/redesign before GPU spend.

**DECISION LOCKED 2026-06-09, RE-ALIGNED TO FIG.1:**
- **Primary federation engine = PARAMETRIC teacher→student KD** (client LoRA + SQL/KD/structure/exec-guided → FedAvg/SecureAvg → Global SLM `M_G`). = Fig.1 + outline §3.7–3.8; grounded in **FedCoLLM [8]** (adapter-FedAvg + global SLM). Demo-level parameter-free KD = cheap variant.
- **Fed-ICL answer-fusion = baseline only** (share answers, fuse by vote/Fusion-LM) — gives parameter-free comm-cost/convergence comparison; not the method (absent from Fig.1).
- **Cross-client transfer = general SQL skill via the Global SLM / public set `X`, NOT schema-coupled private demos.** No private demos / data / schema cross the wire — only weights.
- **RQ2 = local SLM + schema-aware ICL, masking retrieval-only, demos shown unmasked.** Clients evaluated on their **own schemas** (seen schema, unseen questions) = primary; **cross-schema held-out now a claim (Fig.1 innovation)** tested via `M_G` skill + local ICL on the held-out schema's own demos (NOT demo-store `G` — that route failed in attempt-1).
- **Privacy = no raw rows / no schema leave client; only encrypted, DP-perturbed LoRA-delta weights transmit.** (Do NOT claim "no weights leave" — Fig.1 transmits weights.) Masking + DP gradient perturbation are the privacy mechanisms.

### Reference grounding — verified 2026-06-09 (full read of [4][5][6][7][8])

- **[8] FedCoLLM = the engine's real anchor.** Transmits LoRA adapters; server `θ ← (1/K)Σθ_k` (FedAvg/SecureAvg); KD = `ℓ_CE + λ·ℓ_KL` on aux set, mutual — we use the LLM→SLM half only. 4 clients. Our P1′ ≈ FedCoLLM specialized to SQL.
- **[7] FedMKT ≠ weight-FedAvg.** Transmits **logits + CE loss** on public set `D_p`; selective **DualMinCE in logit-space**; LoRA local but **adapters never aggregated**; **MinED** token alignment; λ=0.9, no temperature. → grounds **P2 logit-KD only**, not the P1′ engine. (Was mis-cited; fixed.)
- **[5] Fed-ICL = parameter-free answer-fusion, peers, QA (not SQL).** Shares *answers* to a shared query; majority-vote / Fusion-LM(GENFUSER); 3 clients, Dirichlet α=[0.01…100]; convergence Thm 4.1/Cor 4.2; prompt-extraction attack §6.4. → our **baseline** + the F5 privacy-attack method. SQL adaptation = execution-vote.
- **[4] Light-SQL = single-client base.** Masking **retrieval-only**, demos unmasked (confirmed). **Caveat:** masked-similarity MQS_S=37% EX **< plain QTS_S=41%** on CORDIS → masking is a *privacy/transfer* lever that can **cost** accuracy; RQ2 must not claim masking ↑ accuracy. Base uses **CORDIS, not Spider**.
- **[6] IFed-ICL = orthogonal.** Shares implicit activation-vectors + scalar coeffs, classification-only; privacy-by-abstraction. Side citation for §2.5 ICL, not the engine.
- **Novelty/no-precedent:** (i) **no reference does federated Text-to-SQL** (all QA/classification) — gap genuine, Spider-Dirichlet partition is our construction; (ii) **execution loss** and (iii) **DP** appear in Fig.1 but in **no reference** — our contributions, must be implemented (exec→KD-target filtering; DP→DP-SGD-on-LoRA) or scoped as optional.

---

## 0. How to read this document

This plan converts the approved outline (`../drafts/fedicl_sql_outline.pdf`) and the architecture figure (`../figures/fig_architecture_source.png`) into a concrete, executable research program. It has four parts:

1. **Positioning** — the gap, the thesis, and what must be true for the paper to be accepted.
2. **Method specification** — a precise, equation-level definition of FedICL-SQL grounded in the four core references.
3. **Experimental program** — datasets, federated simulation, models, baselines, metrics, ablations, and the exact tables/figures to produce.
4. **Writing & execution plan** — section-by-section content map to the IAJIT template, milestones, risks, repository layout.

Reference shorthand used throughout:
- **[4] Light-SQL** — SLM + semantic-retrieval ICL for NL-to-SQL (the NL2SQL base method; same corresponding author).
- **[5] Fed-ICL** — federated, *parameter-free*, round-based ICL with iterative refinement + convergence proof.
- **[6] IFed-ICL** — implicit federated ICL: local context → implicit vectors injected into residual stream.
- **[7] FedMKT** — federated *mutual* knowledge transfer LLM↔SLM via output logits on a public dataset + MinED token alignment.
- **[8] FedCoLLM** — parameter-efficient federated co-tuning of LLM + SLMs (LoRA + KD).
- **[1]** federated BART text classification/generation; **[2]** prior thesis; **[3]** ICL survey.

---

## 1. Positioning, thesis, and contributions

### 1.1 The gap (what no prior work does)

| Work | NL2SQL | Federated | LLM–SLM | ICL | Privacy of schema | Gap it leaves |
|------|:---:|:---:|:---:|:---:|:---:|---|
| Light-SQL [4] | ✓ | ✗ | SLM only | ✓ | local-only | no collaboration across orgs; no teacher signal |
| Fed-ICL [5] | ✗ (QA) | ✓ | LM-agnostic | ✓ | ✓ | not for structured SQL / schema heterogeneity |
| FedMKT [7] | ✗ | ✓ | ✓ mutual KD | ✗ | weights/logits | no ICL; requires shared public corpus + logit transmit |
| IFed-ICL [6] | ✗ (classif.) | ✓ | LLM | implicit | ✓ | not generative SQL; classification only |
| FedCoLLM [8] | ✗ | ✓ | ✓ co-tune | ✗ | LoRA weights | parameter transmission; no ICL; no SQL |

**Gap:** No framework jointly delivers (a) cross-organization collaboration **without sharing private schemas or data**, (b) **schema-aware ICL** that generalizes to unseen databases, and (c) **LLM-teacher → SLM-student** knowledge transfer for cheap local deployment — *specifically for Text-to-SQL*.

### 1.2 Thesis (one sentence)

> A cloud LLM teacher and many on-premise SLM students can collaboratively raise Text-to-SQL accuracy across heterogeneous private databases — matching or beating centralized LLM ICL — while transmitting only encrypted, DP-perturbed LoRA-delta weights and teacher-authored public demonstrations, never raw schemas or data. `[Fig.1: "Weights Only" upload; data/schema stay local.]`

### 1.3 Contributions (final wording target — maps to outline "Main Contributions")

1. **Federated LLM–SLM framework for Text-to-SQL** (FedICL-SQL): server-side LLM teacher + global ICL repository + federated aggregation engine; client-side SLM students with local private schemas (Fig. 1).
2. **Schema-aware In-Context Learning mechanism**: schema-aware retrieval and prompt construction using local examples plus teacher/public demonstrations from the ICL Hub; masking supports retrieval/de-identification without putting masked SQL placeholders into the final prompt. ⚠️ **ICL must be load-bearing — it's in the title** `[2026-06-10]`: the *federated* ICL story = the **ICL Hub** (teacher demos on `X`, broadcast — the only ICL piece that crosses the wire) + **held-out adaptation** (RQ2: `M_G` skill + local ICL on the unseen schema's own demos). Make both prominent in §3.6 and ensure Ablation 1 / the held-out eval actually show an ICL delta; if ICL shows ~0 on seen *and* held-out schemas, the title overclaims and the framing (or title) must change — surface this at the Stage gate, not at review.
3. **Federated SQL knowledge distillation**: each client LoRA-trains on its **own private** NL→SQL pairs (supervised) **plus** a privacy-safe shared public set with **teacher-KD targets**; server FedAvg/FedProx-aggregates the deltas into a Global SLM — pooling cross-org SQL skill without transmitting schemas or data (adapts [8] to Text-to-SQL; Fed-ICL [5] regime as parameter-free baseline). Novelty vs prior SQL-KD = **(i) reasoning/CoT distillation from the teacher (reasoning⊕SQL targets), (ii) exec-based KD-target filtering, and (iii) a skeleton-token structure loss** inside the federated loop (exec-guidance itself is prior art — do not claim it as novel; the federated-SQL setting + the reasoning⊕exec⊕structure combination is the contribution).
4. **Privacy-preserving collaborative optimization**: round-based protocol transmitting only encrypted, compressed LoRA-delta weights (Fig.1 "Weights Only"); bounded per-round communication (delta size); secure aggregation. **Differential privacy (gradient perturbation on the deltas) is claimed only if measured** — we report the (ε, EX-cost) trade-off and run the F5 attack with DP *on*; otherwise DP is scoped to future work, not a headline contribution. (No reference [5][7][8] uses DP → it is genuinely our addition, so it must be quantified to count.)
5. **Extensive evaluation** on Spider + Spider-Realistic under a federated non-IID partition, with FL / efficiency / privacy metrics and five ablations.

### 1.4 Research questions (from outline) → what each one is answered by

- **RQ1 (FL effectiveness):** Does federation across clients beat isolated per-client SLM ICL? → Overall Performance table + convergence-vs-rounds figure.
- **RQ2 (ICL effectiveness):** Does schema-aware ICL improve cross-domain generalization to unseen DBs? → cross-DB held-out split + "Impact of ICL" + retrieval-size ablation.
- **RQ3 (LLM→SLM transfer & efficiency):** Better efficiency–performance tradeoff than LLM-only or SLM-only? → "Impact of LLM Teacher" + efficiency table (latency/VRAM/FLOPs) + Pareto plot.

---

## 2. Method specification

### 2.1 Notation & problem formulation (§3.1)

**Notation reconciliation (paper-wide, fix in §3.1) `[2026-06-10]`:** Fig.1 labels clients `Organization 1…K` and loss weights `λ₁…λ₄`; this plan historically used `L` = #clients, `K` = rounds, `k` = shots, `λ` = KL weight, `β` = skeleton weight. **Paper notation: clients `K` (match figure), rounds `T`, shots `k`, loss weights `λ₁…λ₄` (match figure; the KL temperature-weight and skeleton weight live inside the definitions of `λ₂·L_KD` / `λ₃·L_struct`).** Plan text below still says `L` clients / `K` rounds — translate when drafting §3.

Federated system: server `S` + `L` clients (organizations). Client `i` holds:
- private schema `Sᵢ = {Tᵢ, Cᵢ, Rᵢ}` (tables, columns, foreign keys),
- a private example store `Qᵢ = {(qₙ, sₙ)}` of NL-question/gold-SQL pairs,
- a local **SLM student** `Mᵢ` (e.g., Phi-3-mini), frozen or LoRA-adapted.

Server holds:
- **LLM teacher** `M_T` (e.g., Qwen2.5-72B-Instruct),
- **global ICL repository** `G` (teacher/public-sourced demonstrations),
- **federated aggregation engine** `A`,
- optional **global SLM** `M_G` broadcast to clients.

Per-client goal (from [4], Eq. 1): learn `f:(q, Sᵢ) → s*` maximizing execution accuracy `EX = 1[Exec(ŝ,Dᵢ)=Exec(s*,Dᵢ)]`. Federated goal: maximize mean EX across all clients while keeping `Sᵢ` and raw `Qᵢ` private; only protected LoRA/model-update weights cross the wire.

### 2.2 Framework overview (§3.2) — map to Fig. 1

Three planes, matching the architecture figure:

```
SERVER (Cloud)        : LLM Teacher | Global ICL Repository | Aggregation Engine | Global SLM
        ↕  secure / privacy-preserving channel (encrypted LoRA/model updates; teacher/public demos only)
CLIENTS (Org 1..L)    : Local SLM | Local Schema | Local Example Store | Local Retriever (FAISS)
```

One federated round `k`:
1. **Broadcast.** Server sends global ICL repository slice `G_k` (+ optional global SLM `M_G`) to each client.
2. **Local schema-aware ICL.** Client `i` answers its query workload using `Mᵢ` with prompt built from local schema `Sᵢ` + retrieved demos from `Qᵢ ∪ G_k` (§2.3).
3. **Teacher consultation — training-time only `[LOCKED 2026-06-10]`.** Teacher–student collaboration (outline §3.5) = **training-time KD roles**: teacher produces reasoning⊕SQL targets on public `X` (KD) + ICL-Hub demos; students consume them in local LoRA training. **Runtime low-confidence escalation is OUT of P1′/the paper's main method** — it adds inference-time teacher cost and leaks client query patterns to the server, contradicting the privacy story. Mention as deployment option in §5 future work only. Write §3.5 accordingly.
4. **Local training.** Client **LoRA-trains** its SLM on **own private `Qᵢ` (supervised) + public `X` (teacher-KD)** — `L_i = L_sup(Qᵢ) + L_KD(X)` (§2.5-A). The private-data term is what makes federation non-trivial (heterogeneous deltas).
5. **Privacy-safe contribution.** Client uploads **LoRA deltas only** — encrypted, compressed, DP-perturbed (no schema, no data, no full weights, no private demos).
6. **Aggregation.** Engine `A` aggregates LoRA deltas by **FedAvg/FedProx** → **Global SLM `M_G`**; (variant) merges teacher demos into the ICL Hub `G`.

The protocol is **parametric federated distillation** (Fig.1: FedAvg/FedProx over SLM weights + Global SLM broadcast), grounded primarily in **FedCoLLM [8]**, with **FedMKT [7]** reserved for the later logit-KD/MinED refinement and **Fed-ICL [5]** used as the parameter-free baseline.

### 2.3 Schema-aware In-Context Learning (§3.6) — the RQ2 engine

> **[SUPERSEDED 2026-06-09 — see REVISION banner.]** The cross-client demo-store and masked-demos-in-prompt parts below are wrong. Corrected: masking is **retrieval-only**, demos shown unmasked, ICL runs **locally** per client on same/related-schema demos. The rest (prompt structure σ, DDL serialization) still holds.


Prompt construction follows [4] Eq. 3: `σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q`
- `I`: system instruction ("expert SQL generator, output SQL only").
- `S`: schema serialized as DDL (preserves types + FK join paths).
- `Q`: top-`k` retrieved demos via Sentence-BERT/BGE embeddings in FAISS.

**Novelty over [4]:** demos may come from *other clients* via `G`. To make cross-client demos safe and transferable we use **schema-masked, structure-preserving** demonstrations:
- mask table/column identifiers to canonical tokens (`tbl1.col2`), keep SQL *structure* (JOIN/WHERE/agg skeleton). This is [4]'s Masked-Question-Similarity selection (`MQS_S`) repurposed as the *privacy + transfer* mechanism — masking simultaneously (i) hides proprietary identifiers and (ii) lets a JOIN pattern learned at Org A help Org B.
- retrieval score = cosine similarity on masked-question embedding; select `k ∈ {1,3}` (the [4] sweet spot, inverted-U at k=5).

**Design choice to test:** local-only demos vs. federated `G` demos vs. mixed. Mixed expected best for *unseen* schemas (RQ2).

### 2.4 Global LLM Teacher & Local SLM Student (§3.3–3.4)

- **Teacher `M_T`** (Qwen2.5-72B-Instruct via paid API, both stages — server-side): on **public `X` only** (privacy — teacher never touches client-private data), produces **SQL + reasoning steps (CoT)** + optional token-level signals. Outputs exec-validated and cached → feed both the **ICL Hub** demos and the **KD targets**. (Never sees raw client schema/rows; only public-`X` schemas, which are public by construction.)
- **Student `Mᵢ`** (Phi-3-mini 3.8B / Gemma-2B / TinyLlama, 4-bit QLoRA per [4]): runs locally under <6 GB VRAM. Two operating modes:
  - **LoRA-adapted via KD** (parametric, **primary** — = Fig.1 local distillation + weight upload),
  - **frozen + ICL** (parameter-free variant / ablation baseline).

### 2.5 Federated SQL Knowledge Distillation (§3.7) — the RQ3 engine

> **[RE-ALIGNED TO FIG.1 2026-06-09 — the PRIMARY federation engine.]** Channel (A) **parametric LoRA KD** over a shared public NL→SQL set `X` leads (= Fig.1: client distillation losses → FedAvg → Global SLM). Channel (B) demo-level parameter-free KD = cheap variant. This is the outline's §3.7–3.8 and the core of RQ1+RQ3.


Two distillation channels:

**(A) Parametric LoRA/sequence-level (primary, = Fig.1 engine).**
⚠️ **FEDERATION-VALIDITY (fixes the FedAvg-no-op flaw, 2026-06-09):** clients must train on their **own private data**, not only the shared public `X`. If every client LoRA-trains on the *same* `X` with the *same* teacher targets, all deltas are near-identical → `FedAvg ≈ single-client training on X` → federation adds nothing → RQ1 is false by construction. So the client objective has **two parts**:
`L_i = L_sup(private Qᵢ) + L_KD(public X)`
- `L_sup` = supervised CE on the client's **own private** `(q, gold-SQL)` pairs `Qᵢ` (own schema `Sᵢ`, never leaves client) — this is what makes each client's delta carry *org-specific* SQL skill, so FedAvg pools heterogeneous knowledge into `M_G`. **This is FedCoLLM [8]'s actual regime** (clients have private local data; public set is only the KD-alignment medium).
- `L_KD` = teacher-distillation on the **shared public** `X`:
`L_KD = Σ_x [ CE(Mᵢ(x), r̂_T(x)⊕ŝ_T(x)) + λ·KL_τ(Mᵢ(x) ‖ M_T(x)) + β·L_struct(x) ]`, over teacher targets **pre-filtered to executable SQL only** (the exec step, see below). The teacher target is the **reasoning⊕SQL sequence** `r̂_T⊕ŝ_T`, not SQL alone (see CoT note below).

**`[RE-GROUNDED 2026-06-10 — Fig.1's 4 named losses, literal mapping]`** Fig.1's client box names exactly four losses and gives the **verbatim total**: `L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec` (see `fig1_architecture.md`). **§3.7 must present THIS λ-form** (the approved figure's equation), then define each term; this plan's working decomposition `L_i = L_sup(Qᵢ) + L_KD(X)` maps onto it as: `L_SQL` = the CE terms (gold on `Qᵢ` + teacher SQL on `X`), `L_KD` = CoT distillation, `L_struct` = skeleton-CE (the `β` here = `λ₃`), `L_exec` = realized as exec-match filtering (`λ₄`-term non-differentiable → selection gate, stated openly). Map them precisely:
- **SQL loss** = token CE on the SQL: vs **own gold** on private `Qᵢ` (= `L_sup`), vs **teacher SQL** `ŝ_T` on public `X`.
- **KD loss** = distil teacher *behavior* on `X`. **Includes reasoning (CoT distillation)** — Fig.1 teacher "produce reasoning steps", emits "Reasoning Guidance"; the teacher target is `r̂_T⊕ŝ_T` (reasoning then SQL), so the student learns the *derivation*, not just the answer. P1′ (API teacher — no logit vectors over the wire) = sequence-CE on `r̂_T⊕ŝ_T`; soft-logit `λ·KL_τ` + MinED → P2 (needs teacher logits — self-hosted Qwen or logprobs-capable serving).
- **Structure loss** = `β·L_struct` skeleton-token CE (below).
- **Execution** = teacher-target **exec-filtering** (below). Fig.1 draws it as a "loss"; SQL execution is non-differentiable, so we realize its intent as a **hard selection gate** on KD targets (drop non-executable), not a gradient term — state this explicitly in §3.7 so the figure-vs-impl divergence is owned, not hidden.

**Reasoning / CoT (teacher duty #2).** The teacher emits `(reasoning, SQL)` per `X` item; reasoning is cached and used **two ways**: (i) part of the KD target sequence above (CoT distillation), and (ii) attached to **ICL-Hub demos** to guide retrieval-augmented prompts (RQ2). Final SQL is extracted from the teacher output for exec-validation + as the `L_sql`/EX target. At student inference, reasoning is optional (decode SQL-only for latency, or reason-then-SQL for accuracy — an ablation).

**`L_struct` (precise, differentiable):** NOT an AST-edit-distance (discrete, non-differentiable). Define it as **weighted token-level CE on the SQL *skeleton-token* subsequence** — clause keywords + structural tokens (`SELECT/FROM/JOIN/ON/WHERE/GROUP BY/agg`), identifiers stripped. Up-weights getting the query *shape* right even when literals/identifiers differ. This is a normal CE term → backprops cleanly. (If even this proves unstable, fall back to a higher CE weight on skeleton tokens.)

**Exec-guided = target *filtering*, NOT a loss term `[UPGRADED 2026-06-10 to exec-match]`.** Non-differentiable, so it is a data-selection step, never inside `L`. Two strengths, both stored per target (`exec_ok`, `exec_correct` — already in code):
- **Simulation (Spider — `X` has gold):** filter = **exec-match** — keep a teacher target only if its execution **result set equals the gold result set** (`exec_correct`). "Runs" ≠ "right"; match-filtering gives near-clean KD targets. This is the default (`kd_require_correct=True`).
- **Deployment (real `X`, no gold):** filter degrades to **exec-only** (+ optionally self-consistency voting). State this honestly in §3.7: the paper's numbers use exec-match because the benchmark labels `X`; an unlabeled-public-set deployment gets the weaker filter.

**Novelty framing (avoid over-claim):** execution-guidance for SQL is prior art (exec-guided decoding, RL-with-exec-reward). Our novelty is **exec-based KD-target filtering inside the federated KD loop** + the **skeleton-token structure loss** — not exec-guidance per se. State it that way in §3.7 / contributions.
(soft-logit KL term + **MinED token alignment** [7] deferred to P2; P1′ runs sequence-CE + exec-guided filtering). Client uploads **LoRA deltas only** (encrypted/compressed, DP-perturbed); server aggregates by **FedAvg/SecureAvg** → **Global SLM `M_G`**, broadcast back. **This adapter-FedAvg + global-SLM loop = FedCoLLM [8]** (verified: [8] transmits LoRA adapters and averages them `θ ← (1/K)Σθ_k`; KD = CE+λ·KL). We use only the LLM→SLM (`L^g_KD`) half of [8]'s mutual KD — teacher→student, dropping SLM→LLM. **Not FedMKT [7]** — [7] never FedAvgs weights (shares logits, DualMinCE in logit-space); [7] grounds the P2 logit-KD + MinED variant only.

**(B) Demonstration-level (parameter-free, variant).** Teacher answers queries on `X`; correct `(q, ŝ_T)` pairs become high-quality demos in the server **ICL Hub** (teacher/public-sourced) + client stores. *Behavioral* distillation through ICL — no weights. Cheap comparator to (A). (Fed-ICL [5] answer-fusion is a separate parameter-free **baseline**, not a KD channel.)

### 2.6 Federated Optimization & protocol (§3.8) — the RQ1 engine + Algorithm 1

> **[SUPERSEDED 2026-06-09 — see REVISION banner + `fig1_architecture.md`.]** Algorithm 1 below shares masked `(q, SQL)` demos into `G` — wrong. Corrected protocol (Fig.1): **(primary, parametric)** each round, clients LoRA-train on public set `X` with teacher KD targets and upload **LoRA deltas**, server **FedAvg/FedProx** → **Global SLM `M_G`** broadcast; **(baseline, parameter-free)** Fed-ICL answer-fusion (clients share *answers* to shared queries, fused by vote/Fusion-LM). Convergence-vs-rounds + per-round comm-cost (delta-size) framing still applies.


Round-based, mirroring Fed-ICL Algorithm 1, SQL-specialized:

```
Algorithm: FedICL-SQL (one variant = parameter-free)
Input: clients {Sᵢ,Qᵢ,Mᵢ}, teacher M_T, rounds K, shots k
1: G_1 ← seed masked demos (public Spider train subset)
2: for round t = 1..K:
3:    broadcast G_t to all clients
4:    for each client i in parallel:
5:        for each query q in workload_i:
6:            Q_ret ← retrieve top-k from (Qᵢ ∪ G_t) by masked-sim
7:            ŝ ← Mᵢ( σ(q, Sᵢ, I, Q_ret) )
8:            if confidence(ŝ) < δ or exec-fail:
9:                ŝ ← M_T( σ(q, mask(Sᵢ), I, Q_ret) )      # teacher escalation
10:           if exec-valid(ŝ): add mask(q,ŝ) to C_i        # privacy-safe contribution
11:       send C_i to server                                 # only masked (q,SQL)
12:   G_{t+1} ← A.aggregate({C_i})  = dedup + quality-filter + cap        # Fed-ICL agg
13: return per-client predictions; final G_K; optional M_G
```

Convergence argument borrows Fed-ICL Theorem 4.1/Cor. 4.2 (contraction toward the all-client-conditioned optimum) — cite as theoretical motivation; we report **empirical** convergence (EX vs. rounds). Communication cost per round is **constant** (bounded masked-demo payload), the key efficiency claim.

**Privacy mechanisms to state explicitly (Fig.1):** (i) no raw rows or schema ever leave client, (ii) only **encrypted, compressed LoRA-delta weights** transmitted (never full weights/data/private demos), (iii) **differential privacy** on the deltas — Stage B only (PoC runs no DP). Preferred: DP-SGD (Opacus) on LoRA params; ⚠️ per-sample gradients ≈ 2–3× memory, may not fit a T4 with QLoRA — **fallback = Gaussian noise + clipping on the aggregated per-client LoRA delta before upload** (client-level DP on the update, weaker per-example guarantee — state which one was used; claim DP only with a measured (ε, EX)), (iv) secure aggregation (SSL/TLS), (v) identifier masking (retrieval + de-identification).

**Privacy evaluation must match the threat surface `[FIXED 2026-06-10]`:** the primary engine transmits **weights**, and Fed-ICL's prompt-extraction attack tests **shared demos** — it does NOT validate the weights channel. Split F5:

- **F5a (demo/ICL-Hub channel):** prompt-extraction attack as in Fed-ICL §6.4, with/without masking — valid only for the ICL-Hub + demo-KD variant.
- **F5b (weights channel):** **membership-inference** on `M_G` (per-query loss-threshold MIA: can adversary tell if a private `(q,SQL)` pair was in some client's train set?) and/or the DP **(ε, EX)** trade-off. If neither is run, scope the weights-privacy claim to "encrypted transmission + DP available" and say leakage of the weight channel is untested — never present F5a as evidence for it.

---

## 3. Experimental program (§4)

### 3.1 Datasets & federated simulation (§4.1)

- **Spider** (Yu et al. 2018): 200 DBs, 138 domains, cross-domain. **Primary.**
- **Spider-Realistic**: harder, paraphrased questions without explicit column mentions → tests schema linking robustness.
- **(optional backup)** CORDIS from [4] to bridge to prior work; BIRD if time permits (harder, exec-accuracy focus).

**Federated partition (the crucial novelty in evaluation):** Spider has no native federation, so we *construct* it.
- Partition Spider's databases across `L` clients **by domain**, one DB-group per client → natural **non-IID schema heterogeneity**.
- Control heterogeneity with a **Dirichlet(α)** split over domains, `α ∈ {0.1, 1.0, 100}` (low→high IID), exactly as Fed-ICL [5] §6.1.
- **Cross-DB generalization test (RQ2):** hold out a set of databases unseen by *any* client's local store; they appear only at inference → measures generalization powered by federated `G`.
- Default `L = 3` clients `[LOCKED 2026-06-09]` — **cross-silo** framing (few large orgs, not cross-device thousands; cross-silo FL = 2–100 clients → 3 is valid low-end), matches Fed-ICL [5]. Sweep `L ∈ {3,5,10}` (F6) as scaling/robustness check to preempt "3 too few" reviewer pushback. `make_partition(n_clients=...)` already parameterized.

**Eval-set provenance (state in §4.1):** per-client own-schema eval = the 20% per-DB slice of **Spider train** questions (`train_frac=0.8`) — train-distribution, not dev-curated; held-out-schema eval = Spider dev (the frozen test). Don't let a reviewer discover this footnote themselves.

🔴 **Disjoint-schema split (anti-leakage, mandatory).** Partition Spider DBs into three **schema-disjoint** pools: public `X` (KD medium + ICL Hub), client-private `{Sᵢ}` (one DB-group per client), held-out (cross-schema eval). Guarantee `schemas(X) ∩ schemas(private) ∩ schemas(held-out) = ∅` — no DB appears in two pools, eval questions never seen in any train pool. Without this, every EX/EM number is contaminated. Persist the split (DB-id → pool) and release it.

### 3.2 Models (§4.1)

- **Teacher:** **Qwen2.5-72B-Instruct** `[LOCKED 2026-06-10 REV 2 — real model from day 1]` via paid OpenAI-compat API (DeepInfra primary; OpenRouter/Together alternates), both PoC and headline; targets generated **once** on `X`, cached. Sensitivity: Groq Llama-3.3-70B targets (already generated free) = the alt-teacher data point for teacher-agnosticism. (M4 can't run 72B locally.)
- **Students:** Phi-3-mini (3.8B) primary; Gemma-2B, TinyLlama-1.1B for the SLM-architecture ablation. 4-bit QLoRA, temp=0, max-new-tokens=256 (match [4]).
- **Retriever:** BAAI/bge-small-en + FAISS (match [4]).

### 3.3 Baselines (§4.1)

| Group | Baseline | Purpose |
|---|---|---|
| LLM-only | Teacher LLM zero/few-shot (centralized) | accuracy ceiling, cost reference |
| SLM-only | Local SLM ICL, **no federation** (= Light-SQL [4] per client) | isolated lower bound (RQ1) |
| Centralized ICL | All client data pooled centrally + ICL | privacy-violating upper bound (RQ1/RQ2) |
| **Centralized-FT** | **Pool all private data, LoRA-train one SLM (no federation)** | **true parametric ceiling — the honest "how much does FedAvg cost vs centralized" reference; reviewers will demand it** |
| Without ICL | SLM zero-shot / fine-tuned only | ICL value (RQ2) |
| FL baseline | FedAvg-LoRA SLM (no teacher, no ICL) | FL-without-our-pieces |
| Parameter-free FL | Fed-ICL [5] adapted to SQL | closest federated competitor |

### 3.4 Metrics (§4.1)

- **Text-to-SQL:** Exact-Set-Match (EM), **Execution Accuracy (EX, primary)** — Spider protocol.
- **Federated:** Communication cost (total + per-round bytes), Convergence rate (EX vs. round to plateau).
- **Efficiency:** Inference latency (s/query), Peak GPU VRAM, FLOPs — per [4].
- **Privacy:** F5a prompt-extraction reconstruction success (demo channel, per Fed-ICL §6.4) + F5b membership-inference AUC / DP (ε, EX) on the weights channel (lower leak = better). Channel-matched — see §2.6.

🔴 **Statistical rigor (mandatory for credibility).** Every headline number = **mean ± std over ≥3 seeds** (seeds vary partition + LoRA init + retrieval sampling). For the make-or-break comparisons (FedICL-SQL vs SLM-only; vs Centralized-FT) run a **significance test** — paired bootstrap over per-query EX, or McNemar on exec-correct/incorrect — and report p / CI. Single deterministic runs (temp=0) are NOT sufficient evidence for a "+Z pts" claim; temp=0 fixes decoding, not the seed-level variance of training/partition.

### 3.5 Result tables / figures to produce (§4.2)

1. **T1 Overall Performance** — EX/EM, all methods × {Spider, Spider-Realistic}; seen vs. held-out DBs. *(RQ1)*
2. **T2 Efficiency** — latency/VRAM/FLOPs: teacher vs. students vs. FedICL-SQL. *(RQ3)*
3. **T3 Communication** — bytes/round + rounds-to-converge vs. FedAvg-LoRA & Fed-ICL. *(RQ1)*
4. **F1 Architecture** = provided Fig. 1.
5. **F2 Convergence** — EX vs. round, per α. *(RQ1)*
6. **F3 Pareto** — EX vs. cost (latency or params), showing FedICL-SQL dominates SLM-only and approaches teacher. *(RQ3)*
7. **F4 Heterogeneity** — EX vs. Dirichlet α. *(RQ1/RQ2)*
8. **F5 Privacy** — **F5a** prompt-extraction success with/without masking (demo/ICL-Hub channel); **F5b** membership-inference on `M_G` and/or DP (ε, EX) curve (weights channel). Never cite F5a as weights-channel evidence.

### 3.6 Ablations (§4.2, exactly the outline's five)

1. **Without ICL** — drop demos → isolate ICL contribution.
2. **Without federated learning** — local-only stores → isolate federation.
3. **Without Teacher LLM `[REDEFINED 2026-06-10 — must be same-data-different-labels]`** — NOT "drop `X` entirely" (that confounds teacher value with data quantity). Define as **gold-CE arm**: `L_sup(Qᵢ) + CE(gold-SQL on X)` vs the full method `L_sup(Qᵢ) + KD(teacher reasoning⊕SQL on X)` — identical data, only the label differs → isolates what the teacher adds over plain labels (reasoning + soft supervision). ⚠️ Known risk: free-tier teacher targets are "noisy gold"; if gold-CE ≥ teacher-KD on Spider, the teacher claim narrows to (a) reasoning distillation and (b) working when `X` is unlabeled — measure this arm **in the PoC** (cheap, +~2h GPU) for an early read.
4. **Different retrieval sizes** — `k ∈ {0,1,3,5}` (expect inverted-U per [4]).
5. **Different SLM architectures** — Phi-3 / Gemma-2B / TinyLlama.

Plus discussion subsections required by outline: Impact of ICL, Impact of LLM Teacher, Impact of FL, Communication Efficiency, **Privacy-Utility Trade-off**.

### 3.7 Implementation details (§4.1)

PyTorch + HuggingFace Transformers; QLoRA (4-bit) students; FAISS + bge-small retriever; Flower or a lightweight custom round-loop for the FL simulation (single-GPU, clients sequential). Fixed seeds, temp=0 for determinism. Release code + partition scripts (GitHub).

**Federated hyperparameters `[ADDED 2026-06-10 — these multiply every cost; fix early]`:** rounds `K` and local epochs `E` are the cost multipliers (total LoRA passes = L×K×E×runs). **Stage A PoC: K=2–3, E=1** — enough to see whether FedAvg rounds move EX at all. **Stage B: pick K from the PoC convergence curve** (where EX plateaus, cap K≤10), keep E=1–2 (high E with non-IID clients → client drift; if drift visible, FedProx μ instead of more epochs). State K, E, LoRA rank/α/lr in §4.1.

### 3.8 Run staging & minimum publishable set `[ADDED 2026-06-10]`

The full matrix (7 baselines + 5 ablations + α-sweep + L-sweep + DP + 2 datasets × ≥3 seeds × K rounds) is hundreds of LoRA runs — does not fit free tier, and even paid it needs triage. Priority tiers (a run belongs to the highest tier whose claim it supports):

- **Tier 1 — must have, Stage B, ≥3 seeds + significance.** Make-or-break (`M_G` vs SLM-only vs train-on-X-only null), T1 on Spider (FedICL-SQL, SLM-only, LLM-only, Centralized-FT, FedAvg-LoRA), Ablation 3 (no teacher), T3 communication. → answers RQ1+RQ3; the paper stands or falls here.
- **Tier 2 — should have, Stage B, ≥3 seeds where cheap (inference-only can reuse trained checkpoints).** T2 efficiency, F2 convergence, F3 Pareto, Ablations 1 (no ICL), 2 (no fed), 4 (k-sweep, inference-only), Fed-ICL [5] + Centralized-ICL baselines, RQ2 held-out eval.
- **Tier 3 — nice to have, 1 seed, flagged in caption.** F4 α-sweep, F6 L∈{3,5,10} sweep, DP (ε, EX) curve, Ablation 5 (other SLMs), Spider-Realistic column, F5b MIA. If budget runs out, cut Tier 3 and say so — a missing sweep is survivable; an unreplicated headline is not.
- **Stage A PoC runs:** Tier-1 set only, 1 seed, eval subset, free teacher — directional evidence for the stage gate, never cited in the paper as results.

---

## 4. Writing plan — section-by-section → IAJIT template

IAJIT = IEEE two-column. No math/symbols in title or abstract. Keywords required. Target ~10–14 pages.

| § | Title | Content & sources | Status need |
|---|---|---|---|
| Abstract | 150–250 w | background→problem(privacy/heterogeneity/cost)→method(Fed LLM-SLM+ICL+KD)→headline results. **No symbols.** | after results |
| 1 | Introduction | NL2SQL importance; 3 challenges (privacy, schema heterogeneity, LLM cost); motivation (FL/LLM/SLM/ICL); RQ1-3; objectives; 5 contributions | draftable now |
| 2 | Related Work | 2.1 NL2SQL [Spider, RAT-SQL, DIN/DAIL] · 2.2 LLMs-for-SQL · 2.3 SLMs [4] · 2.4 FL [5,7,8,1] · 2.5 ICL [3,6] · 2.6 **Gap analysis** (use §1.1 table) | draftable now |
| 3 | Proposed Approach | 3.1–3.8 = §2 of this plan, with Fig. 1 + Algorithm 1 + equations | draftable now |
| 4 | Experiments | 4.1 setup · 4.2 results & discussion + ablations (§3 of this plan) | needs runs |
| 5 | Conclusion | summary, findings, practical implications, future work (Fed-RAG, multi-DB reasoning, agentic SQL, continual FL, enterprise deployment) | after results |

**Drafting order (write before experiments finish):** §3 Method → §2 Related Work → §1 Intro → (run experiments) → §4 → Abstract → §5. Method and Related Work are independent of results and unblock everything.

---

## 5. Execution milestones

| Phase | Deliverable | Blocks |
|---|---|---|
| **P0 Setup** | Repo skeleton; Spider+Spider-Realistic loaded; FAISS retriever; Phi-3 4-bit running single-query ICL (reproduce [4] sanity EX) | — |
| **P1′ Federated sim** | Schema-disjoint partition ✅; client LoRA trainer ✅; FedAvg + no-op detector ✅; 4-arm make-or-break runner ✅; PoC runs (teacher targets → Kaggle train → eval) | P0 |
| **P2 Teacher + KD** | Teacher targets on `X` (Qwen2.5-72B paid API, generated once); demo-level distillation variant; (then) LoRA logit-KD + MinED | P1 |
| **P3 Baselines** | SLM-only, centralized-ICL, FedAvg-LoRA, Fed-ICL-adapted | P1 |
| **P4 Eval** | T1–T3, F2–F5, 5 ablations, privacy attack | P2,P3 |
| **P5 Writing** | §3,§2,§1 drafted in parallel from P1; fill §4; abstract+§5; IAJIT formatting; citation check | P4 |
| **P6 Review** | internal peer-review pass (`/ars-reviewer`), revise, finalize | P5 |

Method/Related-Work writing (P5 partial) runs **concurrently** with P1–P4 — they don't depend on results.

---

## 6. Risks & mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| SLM EX on Spider too low to be credible | weak headline | use Phi-3 (strong SLM); teacher-KD lifts the floor; report EX *and* EM; held-out framing emphasizes generalization not absolute SOTA |
| Federation shows no gain over local-only | kills RQ1 | ensure non-IID split creates real heterogeneity; verify deltas actually differ across clients (no-op check); FedProx if client drift |
| Free-tier PoC budget exhausted mid-P1′ | PoC stalls | K=2–3, E=1, eval subset, 1 seed; Kaggle+Colab dual accounts; checkpoint per round so sessions resume |
| Stage B funding never materializes | no headline numbers | PoC results alone are NOT publishable (free teacher, 1 seed); escalate to supervisor at the stage gate — paper timeline depends on it |
| "Federated" reviewer pushback (Spider isn't naturally federated) | validity | be explicit it's a *simulated* federation via domain partition (standard in [5]); justify with privacy scenario; Dirichlet α sweep |
| Teacher 72B compute | feasibility | paid API (DeepInfra ~$0.4/M tok → full `X` ≈ $1–2); teacher runs **once on `X` only** (~1475 ex), cached — never per-query; whole-paper teacher budget < $10 |
| Logit-KD tokenizer mismatch | KD variant fails | MinED alignment [7]; or fall back to sequence-level (demo) distillation which needs no logits |
| Privacy claim challenged | reviewer | run prompt-extraction attack (F5); state masking + optional DP/secure-agg; never transmit raw schema/rows/weights |

---

## 7. Repository layout `[SUPERSEDED by the implemented architecture — source of truth = fedicl-sql/README.md]`

Implemented 2026-06-10 (two-repo split: this docs repo + `fedicl-sql/` standalone code repo, releasable at P6):

```
fedicl-sql/
├── fedicl_sql/      # shared lib: data/ retrieval/ prompts/ models/ training/ federated/ eval/ runtime/
├── configs/         # run matrix — one JSON per planned run (<exp>/<stage>.json)
├── data/raw|processed   # processed: CSV + meta.json; split.json + teacher_targets*.csv committed
├── artifacts/       # heavy outputs by run_id (adapters, M_G) — gitignored
├── experiments/     # <exp>/run.py + results/<run_id>/ (committed) + REGISTRY.md + RUNS.csv
├── analysis/        # results → mean±std + significance → paper/{tables,figures}
├── paper/           # IAJIT latex; tables/figures GENERATED
├── scripts/ tests/ docs/
```

Provenance contract: every result carries `experiment/model/stage/seed/time_average/gpu_vram` + auto `run_id/git_sha/run_date`; `stage ∈ {smoke, poc, headline}`, only `headline` citable.

---

## 8. Open decisions to confirm with advisor

1. **Primary engine** — `[LOCKED 2026-06-09, RE-ALIGNED TO FIG.1]` **parametric teacher→student KD** (client LoRA + SQL/KD/Structure/Exec loss → FedAvg/FedProx → Global SLM `M_G`) is **primary** (Fig.1 aggregation engine; outline §3.7–3.8; FedCoLLM anchor). Demo-level parameter-free KD = cheap variant; Fed-ICL answer-fusion = parameter-free **baseline** for comm/convergence. Both "parameter-free demo-store primary" (attempt-1) and the interim "parameter-free demo-KD primary" recommendations are withdrawn — Fig.1's engine transmits weights, not demos.
2. **Client count** — `[LOCKED 2026-06-09]` **3 default + sweep `L ∈ {3,5,10}`** (robustness/scaling, F6). Rationale: **cross-silo** FL (few large orgs, not cross-device) → 3 is a valid low-end silo count; matches Fed-ICL [5] precedent. Sweep preempts the reviewer "3 too few to show scaling" pushback. Engine anchor FedCoLLM [8] uses 4 — note the minor offset in §4.1, justified by the Fed-ICL baseline match.
3. **Second dataset** — Spider-Realistic (planned) vs. add BIRD for harder EX. *Recommendation: Spider-Realistic now, BIRD only if P2 lands early.*
4. **Teacher access & compute** — `[LOCKED 2026-06-10 REV 2 — see STAGING banner]` **Teacher = Qwen2.5-72B-Instruct via paid API for BOTH stages** (DeepInfra `Qwen/Qwen2.5-72B-Instruct` primary; full `X` ≈ $1–2, paper total < $10); targets generated **once** on `X` (~1475 ex), cached to `teacher_targets.csv` — no re-gen step. Groq Llama-3.3-70B targets kept as `teacher_targets.groq-llama33-70b.csv` (alt-teacher sensitivity). **Stage A GPU:** free cloud (Kaggle 30h/wk P100/2×T4, Colab-free T4 fallback); FedAvg + all eval on the M4 Mac (MPS). **Stage B GPU (after gate):** paid A100-class (Colab Pro / RunPod / Lambda), Tier-1/2 matrix at ≥3 seeds. Record actual teacher model id + training GPU in each result's `model`/`gpu_vram` fields + `stage` (`poc`/`headline`); only `headline` numbers enter the paper.

---

*End of plan. Sources grounded in references [4] Light-SQL (NL2SQL+ICL base, same author), [5] Fed-ICL (parameter-free round protocol + convergence + privacy attack), [6] IFed-ICL, [7] FedMKT (LLM↔SLM logit KD + MinED), [8] FedCoLLM (PEFT co-tuning), and the approved outline + Fig. 1.*
