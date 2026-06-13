# FedICL-SQL — Detailed Research & Writing Plan

**Paper:** *FedICL-SQL: A Novel Federated Large-Small Language Models Framework with In-Context Learning for Natural Language to SQL*
**Venue:** International Arab Journal of Information Technology (IAJIT), WoS-Q3. IEEE two-column template.
**Authors:** Student + Quang-Hung Le (corresponding), Quy Nhon University.
**Plan dated:** 2026-06-12.

> **Doc role: SPEC — reference, read occasionally.** Day-to-day tracking lives in `todo.md` ▶️ Runbook + `LAB_LOG.md`; numbers in `experiments/RUNS.csv`. This file = "what to build & why" (the full method/experiment definitions), not a progress tracker. (CONVENTION.MD §5 doc-layers.)

This document converts the approved outline (`../drafts/fedicl_sql_outline.pdf`) and the architecture figure (`../figures/fig_architecture_source.png`, transcribed in `fig1_architecture.md`) into an executable program. Source-of-truth precedence: **outline wins on section structure; Fig.1 wins on mechanism.**

---

## Status & locked decisions (2026-06-12)

| Item | Decision | Grounding |
| --- | --- | --- |
| **Federation engine** | **Parametric teacher→student KD.** Clients LoRA-train on own private `Qᵢ` + public `X` (teacher KD targets), upload **LoRA deltas only** (encrypted/compressed/DP-noised), server **FedAvg/FedProx → Global SLM `M_G`** broadcast. | Fig.1; outline §3.7–3.8; **FedCoLLM [8]** |
| **Teacher `M_T`** | **Qwen2.5-72B-Instruct** via paid API (DeepInfra ~$0.4/M tok; full `X` ≈ $1–2; paper total < $10). Both stages. Targets generated **once** on `X`, cached. | outline; reachable, real model |
| **Student `Mᵢ`** | **Qwen2.5-1.5B-Instruct** (locked 2026-06-12) — tokenizer-aligned with the teacher → **MinED-free P2 logit-KD**. Phi-3-mini / Gemma-2B / TinyLlama = A5 ablation. | own choice; tokenizer match |
| **Clients** | `L = 3` default + sweep `{3,5,10}` (F6). Cross-silo (few large orgs). | Fed-ICL [5]; FedCoLLM [8] uses 4 |
| **ICL** | Schema-aware retrieval, **masking retrieval-only**, demos shown **unmasked**, run **locally** per client. | Light-SQL [4] |
| **Privacy** | No raw rows / no schema leave client; only **encrypted, DP-perturbed LoRA-delta weights** transmit. Masking + DP gradient perturbation are the mechanisms. (Never claim "no weights leave" — weights DO cross.) | Fig.1 "Weights Only" |
| **Staging** | **Stage-A PoC** (~$2, 1 seed, ~200 q/client subset, **Mac MPS or Colab Pro GPU**, `K=2–3`, `E=1`, no DP, `stage=poc`) → **SB gate** → **Stage-B headline** (paid A100-class GPU, ≥3 seeds + significance, DP measured, `stage=headline`). Only `headline` enters the paper. | budget triage |
| **Compute / repo** | **3 tiers (re-locked 2026-06-12, supersedes "Mac out"):** (1) **Mac M4 Pro 24GB MPS** = dev + all `$0` no-teacher baselines + p0 floor + p1 PoC (1.5B student **fp16**; bitsandbytes 4-bit is CUDA-only); (2) **Colab Pro GPU** = faster/heavier PoC + 4-bit QLoRA; (3) **paid A100-class** = Stage-B headline only. Teacher 72B = paid API regardless. ⚠️ one stack per comparison set. Code repo `github.com/phungnmd/fedicl-sql` (private); edit on Mac → run local OR push → Colab pulls via `notebooks/00_colab_bootstrap.ipynb`. Run tracking → `experiments/RUNS.csv` + `REGISTRY.md` (§7). | locked 2026-06-12 |
| **SB gate** | PoC make-or-break directionally positive (`M_G` > SLM-only AND > X-only null) **AND** supervisor sign-off on §8 + budget. Negative PoC → diagnose before any GPU spend. | risk control |

**Reference shorthand:** [4] Light-SQL (NL2SQL+ICL base, same corresponding author) · [5] Fed-ICL (parameter-free answer-fusion + convergence proof + prompt-extraction attack) · [6] IFed-ICL (implicit vectors, classification — side ref) · [7] FedMKT (logit-space KD + MinED; does NOT FedAvg weights) · [8] FedCoLLM (LoRA-adapter FedAvg + global SLM + CE+λKL KD — the engine anchor) · [1] federated BART · [2] prior thesis · [3] ICL survey.

---

## 1. Positioning, thesis, contributions

### 1.1 The gap

| Work | NL2SQL | Federated | LLM–SLM | ICL | Schema privacy | Gap |
| --- | :-: | :-: | :-: | :-: | :-: | --- |
| Light-SQL [4] | ✓ | ✗ | SLM only | ✓ | local-only | no cross-org collab; no teacher signal |
| Fed-ICL [5] | ✗ (QA) | ✓ | LM-agnostic | ✓ | ✓ | not structured SQL / schema heterogeneity |
| FedMKT [7] | ✗ | ✓ | ✓ mutual KD | ✗ | weights/logits | no ICL; needs logit transmit |
| IFed-ICL [6] | ✗ (classif.) | ✓ | LLM | implicit | ✓ | not generative SQL |
| FedCoLLM [8] | ✗ | ✓ | ✓ co-tune | ✗ | LoRA weights | no ICL; no SQL |

**Gap:** no framework jointly delivers (a) cross-organization collaboration **without sharing private schemas or data**, (b) **schema-aware ICL** generalizing to unseen DBs, and (c) **LLM-teacher → SLM-student** transfer for cheap local deployment — *for Text-to-SQL*.

### 1.2 Thesis

> A cloud LLM teacher and many on-premise SLM students collaboratively raise Text-to-SQL accuracy across heterogeneous private databases — matching or beating centralized LLM ICL — while transmitting only encrypted, DP-perturbed LoRA-delta weights and teacher-authored public demonstrations, never raw schemas or data.

### 1.3 Contributions

1. **Federated LLM–SLM framework for Text-to-SQL** (FedICL-SQL): server LLM teacher + global ICL repository + federated aggregation engine; client SLM students with local private schemas (Fig. 1).
2. **Schema-aware ICL**: schema-aware retrieval + prompt construction from local examples plus teacher/public demos (ICL Hub); masking supports retrieval/de-identification without placing masked SQL placeholders into the final prompt. ⚠️ **ICL must be load-bearing — it's in the title.** The *federated* ICL story = the **ICL Hub** (teacher demos on `X`, the only ICL piece crossing the wire) + **held-out adaptation** (RQ2). If ICL shows ~0 delta on seen *and* held-out schemas, the title overclaims — surface at the stage gate, not at review.
3. **Federated SQL knowledge distillation**: each client LoRA-trains on its **own private** NL→SQL pairs (supervised) **plus** a privacy-safe public set with **teacher KD targets**; server FedAvg/FedProx-aggregates the deltas into a Global SLM. Novelty vs prior SQL-KD = **(i) reasoning/CoT distillation** (reasoning⊕SQL targets), **(ii) exec-based KD-target filtering**, **(iii) a skeleton-token structure loss** inside the federated loop (exec-guidance itself is prior art — claim only the federated-SQL + reasoning⊕exec⊕structure combination).
4. **Privacy-preserving collaborative optimization**: round-based protocol transmitting only encrypted, compressed LoRA-delta weights; bounded per-round communication; secure aggregation. **DP (gradient perturbation on the deltas) is claimed only if measured** — report (ε, EX) + run F5 with DP on; else DP → future work.
5. **Extensive evaluation** on Spider + Spider-Realistic under a federated non-IID partition, with FL / efficiency / privacy metrics and five ablations.

### 1.4 Research questions

- **RQ1 (FL effectiveness):** does federation beat isolated per-client SLM? → Overall Performance + convergence-vs-rounds.
- **RQ2 (ICL effectiveness):** does schema-aware ICL improve generalization to unseen DBs? → cross-DB held-out split + Impact-of-ICL + retrieval-size ablation.
- **RQ3 (LLM→SLM transfer & efficiency):** better efficiency–performance tradeoff than LLM-only or SLM-only? → Impact-of-Teacher + efficiency table + Pareto.

---

## 2. Method specification

### 2.1 Notation & problem (§3.1)

**Paper notation (match Fig.1):** clients `K`, rounds `T`, shots `k`, loss weights `λ₁…λ₄`. *(This plan's working text uses `L`=#clients, `K`=rounds — translate when drafting §3.)*

Federated system: server `S` + `L` clients. Client `i` holds private schema `Sᵢ = {Tᵢ, Cᵢ, Rᵢ}`, a private example store `Qᵢ = {(qₙ, sₙ)}` of NL/gold-SQL pairs, and a local **SLM student** `Mᵢ` (Qwen2.5-1.5B-Instruct, LoRA-adapted). Server holds **LLM teacher** `M_T` (Qwen2.5-72B), **global ICL repository** `G` (teacher/public-sourced), **aggregation engine** `A`, and the broadcast **Global SLM** `M_G`.

Per-client goal ([4] Eq. 1): learn `f:(q, Sᵢ) → s*` maximizing execution accuracy `EX = 1[Exec(ŝ,Dᵢ)=Exec(s*,Dᵢ)]`. Federated goal: maximize mean EX across clients while `Sᵢ` and raw `Qᵢ` stay private; only protected LoRA-delta weights cross the wire.

### 2.2 Framework overview (§3.2) — Fig. 1

```
SERVER (Cloud) : LLM Teacher | Global ICL Hub | Aggregation Engine (FedAvg/FedProx) | Global SLM
        ↕  secure channel (SSL/TLS · Secure Agg · DP gradient perturbation · masking)
        ↕  UP: encrypted LoRA deltas (Weights Only)   DOWN: global params + ICL-Hub demos
CLIENTS (Org 1..L) : Local Schema Sᵢ + private Qᵢ → Schema Encoder → Retrieval → ICL Prompt
                     → Local SLM (decode) → SQL+reasoning → Local Training (SQL+KD+Struct+Exec) → LoRA delta
```

**Offline, once (before rounds):** teacher runs on public `X`, emits `reasoning ⊕ SQL` per item, exec-validated, cached → feeds **both** the ICL Hub demos and the KD targets. (Teacher never sees client-private data; it only touches public-`X` schemas.)

**One federated round `t`:**
1. **Broadcast** global params `M_G` (+ ICL-Hub slice) to clients.
2. **Local ICL** — client `i` builds prompts from `Sᵢ` + demos retrieved from `Qᵢ ∪ G` (§2.3).
3. **Local training** — client LoRA-trains its SLM on **own private `Qᵢ` (supervised) + public `X` (teacher-KD)**: `L_i = L_sup(Qᵢ) + L_KD(X)` (§2.5). The private-data term makes deltas heterogeneous (non-trivial federation).
4. **Privacy-safe upload** — LoRA deltas only, encrypted/compressed/DP-perturbed. No schema, data, full weights, or private demos.
5. **Aggregation** — `A` FedAvg/FedProx-aggregates deltas → `M_G`.

The protocol is **parametric federated distillation**, grounded in **FedCoLLM [8]**; **FedMKT [7]** is reserved for the P2 logit-KD/MinED refinement; **Fed-ICL [5]** is the parameter-free baseline. **Teacher–student collaboration (§3.5) = training-time KD roles only** — runtime low-confidence escalation is OUT (adds inference-time teacher cost + leaks client query patterns to the server, contradicting privacy); mention as deployment option in §5.

### 2.3 Schema-aware ICL (§3.6) — the RQ2 engine

Prompt construction ([4] Eq. 3): `σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q`
- `I`: system instruction ("expert SQL generator, output SQL only").
- `S`: schema serialized as DDL (types + FK join paths).
- `Q`: top-`k` demos retrieved via BGE embeddings in FAISS.

**Masking = retrieval-only ([4]).** Mask table/column identifiers to canonical tokens for the *retrieval-similarity* score (privacy + de-identification + structure-based transfer); the demos **shown to the model are always unmasked**. Never put masked SQL placeholders into the generation prompt. Select `k ∈ {1,3}` ([4] sweet spot, inverted-U at k=5). ⚠️ Masking can **cost** EX ([4]: MQS_S 37% < QTS_S 41%) — frame as a privacy/transfer lever, not an accuracy win.

**ICL runs locally per client** on same/related-schema demos. The shared **ICL Hub** = teacher/public-sourced demos on `X` (broadcast down). Cross-schema generalization (RQ2) comes from the **Global SLM's skill + local ICL** on the held-out schema's own few demos, not from sharing private cross-schema demos.

### 2.4 Teacher & Student (§3.3–3.4)

- **Teacher `M_T`** (Qwen2.5-72B-Instruct, paid API, server-side): on **public `X` only**, produces **SQL + reasoning steps (CoT)**, exec-validated, cached → feeds the ICL Hub demos + KD targets. Never sees raw client schema/rows.
- **Student `Mᵢ`** (Qwen2.5-1.5B-Instruct primary; Phi-3-mini / Gemma-2B / TinyLlama = A5 ablation; 4-bit QLoRA): runs locally < 6 GB VRAM. Two modes: **LoRA-adapted via KD** (parametric, primary) or **frozen + ICL** (parameter-free variant/baseline).

### 2.5 Federated SQL knowledge distillation (§3.7) — the RQ1+RQ3 engine

**Fig.1's verbatim client total loss:** `L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec`. §3.7 must present **this λ-form**, then define each term; this plan's working decomposition `L_i = L_sup(Qᵢ) + L_KD(X)` maps onto it.

⚠️ **Federation-validity (the FedAvg-no-op guard).** Clients must train on their **own private data**, not only `X`. If every client trains on the same `X` with the same teacher targets, all deltas are near-identical → `FedAvg ≈ single-client on X` → federation adds nothing → RQ1 is false by construction. Hence two parts:

`L_i = L_sup(private Qᵢ) + L_KD(public X)`

- **`L_sup`** = supervised CE on the client's **own private** `(q, gold-SQL)` pairs `Qᵢ` (own schema, never leaves client) — makes each delta carry org-specific skill so FedAvg pools heterogeneous knowledge into `M_G`. This is FedCoLLM [8]'s actual regime.
- **`L_KD`** = teacher distillation on the **shared public** `X`, over targets **pre-filtered to exec-match** (below): `L_KD = Σ_x [ CE(Mᵢ(x), r̂_T⊕ŝ_T) + λ·KL_τ(Mᵢ(x) ‖ M_T(x)) + β·L_struct(x) ]`.

**The four Fig.1 losses, literal:**
- **SQL loss** = token CE on the SQL: vs **own gold** on `Qᵢ` (= `L_sup`), vs **teacher SQL** `ŝ_T` on `X`.
- **KD loss** = distil teacher *behavior* on `X`, **including reasoning (CoT distillation)** — target = `r̂_T⊕ŝ_T` (reasoning then SQL), so the student learns the *derivation*. P1 (API teacher, no logit vectors) = sequence-CE on `r̂_T⊕ŝ_T`; soft-logit `λ·KL_τ` + MinED → **P2** (needs teacher logits).
- **Structure loss** `β·L_struct` = **weighted token-level CE on the SQL skeleton-token subsequence** (clause keywords + structural tokens, identifiers stripped). Differentiable, backprops cleanly. NOT AST-edit-distance.
- **Execution** = teacher-target **filtering**, NOT a gradient term (SQL exec is non-differentiable → a data-selection gate). Stored per target as `exec_ok` / `exec_correct`. **Simulation (`X` has gold):** keep a target only if its result set equals the gold's (**exec-match**, `kd_require_correct=True`) — "runs" ≠ "right". **Deployment (unlabeled `X`):** degrades to exec-only (+ optional self-consistency). State this divergence openly in §3.7.

**Reasoning/CoT (teacher duty #2).** Teacher emits `(reasoning, SQL)` per `X` item; reasoning is used two ways: (i) part of the KD target sequence (CoT distillation), (ii) attached to ICL-Hub demos for retrieval-augmented prompts (RQ2). At inference, reasoning is optional (SQL-only for latency, reason-then-SQL for accuracy — an ablation).

**Novelty framing (avoid over-claim):** exec-guidance for SQL is prior art. Our novelty = **exec-based KD-target filtering inside the federated KD loop** + **skeleton-token structure loss** + **CoT distillation** — not exec-guidance per se.

Client uploads **LoRA deltas only** (encrypted/compressed/DP-perturbed); server aggregates by **FedAvg/SecureAvg** → `M_G`, broadcast back. This adapter-FedAvg + global-SLM loop = **FedCoLLM [8]** (uses only the LLM→SLM half of [8]'s mutual KD). **Not FedMKT [7]** ([7] shares logits, DualMinCE in logit-space, never FedAvgs weights → grounds P2 only).

**Demo-level KD (variant, parameter-free):** teacher's correct `(q, ŝ_T)` on `X` become high-quality ICL-Hub demos — behavioral distillation through ICL, no weights. Cheap comparator to the parametric engine.

### 2.6 Federated optimization & protocol (§3.8) — Algorithm 1

```
Algorithm 1: FedICL-SQL (parametric engine — primary)
Input: clients {Sᵢ, Qᵢ, Mᵢ}, teacher M_T, public X, rounds T, LoRA init θ₀
Offline: teacher_targets ← {(x, r̂_T(x)⊕ŝ_T(x)) : x ∈ X, exec_correct(x)}   # once, cached
 1: M_G ← base SLM + θ₀
 2: for round t = 1..T:
 3:    broadcast M_G (+ ICL-Hub slice) to all clients
 4:    for each client i in parallel:
 5:        θᵢ ← LoRA-train Mᵢ on  L_sup(Qᵢ) + L_KD(teacher_targets)   # SQL+KD+Struct; Exec = target filter
 6:        Δθᵢ ← encrypt/compress/DP-perturb(θᵢ − θ_{t−1})
 7:        upload Δθᵢ                                                  # Weights Only
 8:    θ_t ← θ_{t−1} + (1/L) Σᵢ Δθᵢ     ;     M_G ← base + θ_t          # FedAvg/FedProx
 9: return M_G ; per-client predictions
```

Convergence: borrow Fed-ICL Theorem 4.1/Cor. 4.2 as theoretical motivation; report **empirical** convergence (EX vs rounds). Per-round communication = bounded LoRA-delta size (the efficiency claim). **Baseline variant (Fed-ICL [5]):** clients propose SQL on a shared query set using own private demos; server fuses by exec-vote/Fusion-LM; iterate — parameter-free comm-cost/convergence comparator, never the method.

**Privacy mechanisms (Fig.1):** (i) no raw rows/schema leave; (ii) only encrypted, compressed LoRA-delta weights transmit; (iii) **DP** on the deltas — Stage B only (PoC: no DP). Preferred DP-SGD (Opacus) on LoRA; ⚠️ per-sample grads ≈ 2–3× memory, may not fit a free T4 → fallback = Gaussian noise + clipping on the aggregated per-client delta pre-upload (client-level DP, weaker per-example guarantee — state which). (iv) secure aggregation (SSL/TLS); (v) identifier masking.

**Privacy evaluation must match the threat surface.** The engine transmits **weights**; Fed-ICL's prompt-extraction attack tests **demos** — it does not validate the weights channel. Split F5:
- **F5a (demo/ICL-Hub channel):** prompt-extraction attack ([5] §6.4), ± masking — valid only for the ICL-Hub + demo-KD variant.
- **F5b (weights channel):** membership-inference on `M_G` (per-query loss-threshold MIA) and/or the DP (ε, EX) trade-off. If neither runs → scope the weights-privacy claim to "encrypted transmission + DP available"; never present F5a as evidence for it.

---

## 3. Experimental program (§4)

### 3.1 Datasets & federated simulation (§4.1)

- **Spider** (Yu et al. 2018): 200 DBs, 138 domains, cross-domain. **Primary.**
- **Spider-Realistic**: paraphrased questions without explicit column mentions → tests schema linking.
- *(backup)* CORDIS [4] to bridge to prior work; BIRD if time permits.

🔴 **Schema-disjoint 3-pool split (anti-leakage, mandatory).** Partition Spider DBs into **public `X`** (KD medium + ICL Hub), **client-private `{Sᵢ}`** (one DB-group per client), **held-out** (cross-schema eval), with `schemas(X) ∩ private ∩ held-out = ∅` — no DB in two pools, eval questions never in any train pool. Persist DB-id→pool, release it. **Dirichlet(α)** over the **private** pool controls heterogeneity, `α ∈ {0.1, 1.0, 100}` (low→high IID), as Fed-ICL [5] §6.1. Default `L = 3` (cross-silo); sweep `{3,5,10}` (F6).

**Eval-set provenance (state in §4.1):** per-client own-schema eval = 20% per-DB slice of **Spider train** (`train_frac=0.8`); held-out-schema eval = **Spider dev** (frozen test). Don't let a reviewer discover this footnote unaided.

**Data hygiene:** tune on `val` (a seeded slice of Spider train); the `test` split (= Spider dev) is **frozen** — touch once for final numbers. Headline = ≥3 seeds + significance.

**Data pipeline & tracking (repro contract).** Two deterministic stages, raw → processed:

```
data/raw/spider/   download_spider.py   (JSON + per-DB .sqlite; 1.9 GB; GITIGNORED, fetched per machine)
   ├─ build_processed.py  → data/processed/centralized/  train.csv(7793) · val.csv(866, seeded) · test.csv(1034=Spider dev, FROZEN) · meta.json
   └─ build_federated.py  → data/processed/federated/<L>c-a<α>-s<seed>/
         public_X.csv(1475) · client_i_{train,eval}.csv · held_out.csv(1034) · split.json(DB→pool map) · meta.json(seed/α/db_pool_map)
```

A CSV row = `question, query, db_id, db_path`; `db_path` is **relative** (`data/raw/...sqlite`) → portable. **All processed CSVs + split.json + meta.json + teacher targets are committed** (~5 MB) — the exact frozen split travels with the repo (no rebuild, no drift); only the heavy raw DBs are regenerated. `build_*` are deterministic per `--seed`, so a rebuild reproduces the committed `db_pool_map` byte-for-byte. The `fedicl_sql` lib + `experiments/*/run.py` read these processed CSVs; the Colab bootstrap (`notebooks/00_colab_bootstrap.ipynb`) reuses the same scripts + CSVs. (The standalone learning notebooks `01`/`02` do NOT — they reimplement schema/EX inline and are not paper-grade.)

### 3.2 Models (§4.1)

- **Teacher:** Qwen2.5-72B-Instruct, paid OpenAI-compat API (DeepInfra primary; OpenRouter/Together alt), both stages; targets generated once on `X`, cached. Sensitivity: Groq Llama-3.3-70B targets (free) = alt-teacher data point.
- **Students:** **Qwen2.5-1.5B-Instruct primary** (tokenizer-aligned with the teacher → MinED-free P2); Phi-3-mini (3.8B), Gemma-2B, TinyLlama-1.1B for the SLM-arch ablation (A5). 4-bit QLoRA, temp=0, max-new-tokens=256 ([4]).
- **Retriever:** BAAI/bge-small-en + FAISS ([4]).

### 3.3 Baselines (§4.1) — run order = TODO P0.5

| ID | Baseline | Purpose | Needs |
| --- | --- | --- | --- |
| B1 | LLM-only (teacher zero/few-shot) | accuracy ceiling | teacher |
| B2 | SLM-only (own private only, no fed/teacher) | floor (RQ1) | fed split |
| B3 | **Centralized-FT** (pool all private, 1 LoRA SLM) | true parametric ceiling; "FedAvg cost vs centralized" reference | — |
| B4 | Centralized-ICL (pool all + ICL) | privacy-violating ICL ceiling | — |
| B5 | Without-ICL (SLM zero-shot) | ICL value (= Ablation 1) | — |
| B6 | FedAvg-LoRA (no teacher, no ICL) | FL-without-our-pieces (= gold-CE / Ablation 3) | fed |
| B7 | Fed-ICL [5] adapted to SQL | closest federated competitor | fed |

### 3.4 Metrics (§4.1)

- **Text-to-SQL:** Exact-Set-Match (EM), **Execution Accuracy (EX, primary)** — Spider protocol.
- **Federated:** communication cost (total + per-round bytes); convergence (EX vs round to plateau).
- **Efficiency:** inference latency (s/q), peak VRAM, FLOPs.
- **Privacy:** F5a prompt-extraction success (demo channel) + F5b membership-inference AUC / DP (ε, EX) (weights channel). Channel-matched.

🔴 **Statistical rigor.** Every headline number = **mean ± std over ≥3 seeds** (seeds vary partition + LoRA init + retrieval sampling). Make-or-break comparisons get a **significance test** (paired bootstrap over per-query EX, or McNemar) + p / CI. Temp=0 fixes decoding, not seed-level variance.

### 3.5 Tables / figures (§4.2)

1. **T1** Overall — EX/EM, all methods × {Spider, Spider-Realistic}; seen vs held-out (RQ1).
2. **T2** Efficiency — latency/VRAM/FLOPs (RQ3).
3. **T3** Communication — bytes/round + rounds-to-converge vs FedAvg-LoRA & Fed-ICL (RQ1).
4. **F1** Architecture (= provided Fig. 1).
5. **F2** Convergence — EX vs round, per α (RQ1).
6. **F3** Pareto — EX vs cost; FedICL-SQL dominates SLM-only, approaches teacher (RQ3).
7. **F4** Heterogeneity — EX vs Dirichlet α (RQ1/RQ2).
8. **F5** Privacy — F5a prompt-extraction ± masking (demo channel); F5b MIA on `M_G` / DP (ε, EX) (weights channel). Never cite F5a for weights.
9. **F6** Client scaling — EX + comm vs `L ∈ {3,5,10}`.

### 3.6 Ablations (§4.2)

1. **Without ICL** — drop demos → isolate ICL.
2. **Without federated learning** — local-only → isolate federation.
3. **Without Teacher LLM = gold-CE arm** — `L_sup(Qᵢ) + CE(gold-SQL on X)` vs full `L_sup(Qᵢ) + KD(teacher reasoning⊕SQL on X)`; **identical data, only the label differs** → isolates teacher value from data quantity. ⚠️ if gold-CE ≥ teacher-KD on Spider, the teacher claim narrows to (a) reasoning distillation and (b) working when `X` is unlabeled — measure this arm **in the PoC** (cheap).
4. **Retrieval size** `k ∈ {0,1,3,5}` (inverted-U per [4]).
5. **Different SLMs** — Qwen-1.5B / Phi-3 / Gemma-2B / TinyLlama.

Plus discussion subsections: Impact of ICL, Impact of LLM Teacher, Impact of FL, Communication Efficiency, **Privacy-Utility Trade-off**.

### 3.7 Implementation (§4.1)

PyTorch + HuggingFace; QLoRA (4-bit) students; FAISS + bge-small retriever; lightweight custom round-loop (single-GPU, clients sequential). Fixed seeds, temp=0. **Federated hyperparams** (cost multipliers, total LoRA passes = L×T×E×runs): Stage-A PoC `T=2–3, E=1`; Stage-B pick `T` from the PoC convergence plateau (cap ≤10), `E=1–2` (high E + non-IID → drift; if drift visible, FedProx μ instead). State `T, E`, LoRA rank/α/lr in §4.1. Release code + partition scripts.

### 3.8 Run staging & minimum publishable set

The full matrix (7 baselines + 5 ablations + α-sweep + L-sweep + DP + 2 datasets × ≥3 seeds × T rounds) is hundreds of LoRA runs — triage by tier (a run belongs to the highest tier whose claim it supports):

- **Tier 1 — must, Stage B, ≥3 seeds + significance.** Make-or-break (`M_G` vs SLM-only vs X-only null), T1 Spider (FedICL-SQL, SLM-only, LLM-only, Centralized-FT, FedAvg-LoRA), Ablation 3, T3. The paper stands or falls here.
- **Tier 2 — should, Stage B, ≥3 seeds where cheap (inference reuses checkpoints).** T2, F2, F3, Ablations 1/2/4, Fed-ICL + Centralized-ICL, RQ2 held-out.
- **Tier 3 — nice, 1 seed, flagged in caption.** F4 α-sweep, F6 L-sweep, DP (ε, EX), Ablation 5, Spider-Realistic column, F5b MIA. Budget out → cut Tier 3 and say so.
- **Stage-A PoC:** Tier-1 set only, 1 seed, eval subset — directional evidence for the gate, never cited as paper results.

---

## 4. Writing plan → IAJIT template

IAJIT = IEEE two-column. No math/symbols in title or abstract. Keywords required. ~10–14 pages.

| § | Title | Content & sources | Status |
| --- | --- | --- | --- |
| Abstract | 150–250 w | background → problem (privacy/heterogeneity/cost) → method → headline results. No symbols. | after results |
| 1 | Introduction | NL2SQL; 3 challenges; motivation; RQ1-3; 5 contributions | now |
| 2 | Related Work | 2.1 NL2SQL · 2.2 LLMs-for-SQL · 2.3 SLMs [4] · 2.4 FL [5,7,8,1] · 2.5 ICL [3,6] · 2.6 gap (§1.1 table) | now |
| 3 | Proposed Approach | 3.1–3.8 = §2 here, + Fig.1 + Algorithm 1 + equations | now |
| 4 | Experiments | 4.1 setup · 4.2 results & discussion + ablations (§3 here) | needs runs |
| 5 | Conclusion | summary, findings, future work (runtime escalation, Fed-RAG, multi-DB reasoning, continual FL) | after results |

**Drafting order:** §3 → §2 → §1 → (runs) → §4 → Abstract → §5. §3/§2/§1 are results-independent and unblock everything.

---

## 5. Milestones

| Phase | Deliverable | Blocks |
| --- | --- | --- |
| P0 Setup | repo; Spider loaded; FAISS retriever; SLM 4-bit single-query ICL; floor EX | — |
| P0.5 Baselines | no-teacher (zero-shot, Centralized-FT, Centralized-ICL) + fed-no-teacher (SLM-only, FedAvg-LoRA) | P0 |
| P1 Federated engine | schema-disjoint split; client LoRA trainer; FedAvg + no-op detector; 4-arm make-or-break; PoC runs (teacher targets → Colab Pro train → eval) | P0 |
| P2 Logit-KD | soft-logit KD + MinED (likely skippable — aligned tokenizer) | P1 validated |
| SB Stage B | paid headline matrix (Tier 1→3, ≥3 seeds, DP) | gate |
| P4 Eval | T1–T3, F2–F6, 5 ablations, privacy attack | SB |
| P5 Writing | §3,§2,§1 in parallel from P1; §4; abstract; §5; IAJIT format; citation check | P4 |
| P6 Review | `/ars-reviewer`, revise, release code, finalize, submit | P5 |

§3/§2 writing runs **concurrently** with P0.5–P4.

---

## 6. Risks & mitigations

| Risk | Impact | Mitigation |
| --- | --- | --- |
| SLM EX on Spider too low | weak headline | strong SLM; teacher-KD lifts floor; report EX+EM; held-out framing emphasizes generalization |
| Federation no gain over local | kills RQ1 | non-IID split → real heterogeneity; verify deltas differ (no-op check); FedProx if drift |
| PoC stalls mid-run (disconnect) | lost progress | T=2–3, E=1, subset, 1 seed; checkpoint per round to Drive → resume |
| Stage B funding never materializes | no headline | PoC alone not publishable; escalate at the gate |
| "Spider isn't federated" pushback | validity | explicit *simulated* federation via domain partition (standard in [5]); privacy scenario; α sweep |
| Teacher 72B compute | feasibility | paid API (~$0.4/M tok → `X` ≈ $1–2); runs once on `X`, cached |
| Logit-KD tokenizer mismatch | KD variant fails | **aligned Qwen tokenizer → MinED unneeded**; else sequence-level (demo) KD needs no logits |
| Privacy claim challenged | reviewer | F5a+F5b channel-matched; masking + DP/secure-agg; never transmit raw schema/rows |
| ICL shows ~0 delta | title overclaims | surface at the stage gate; reframe title/§3.6 if seen *and* held-out show no ICL gain |

---

## 7. Repository layout

Source of truth = `fedicl-sql/README.md`. Two-repo split: this docs repo + `fedicl-sql/` standalone code repo (releasable at P6).

```
fedicl-sql/
├── fedicl_sql/   # shared lib: data/ retrieval/ prompts/ models/ training/ federated/ eval/ runtime/
├── configs/      # one JSON per planned run (<exp>/<stage>.json)
├── data/raw|processed   # processed CSV + meta; split.json + teacher_targets*.csv committed
├── artifacts/    # heavy outputs by run_id (adapters, M_G) — gitignored
├── experiments/  # <exp>/run.py + results/<run_id>/ + REGISTRY.md + RUNS.csv
├── analysis/     # results → mean±std + significance → paper/{tables,figures}
├── paper/ scripts/ tests/ docs/
```

Provenance contract: every result carries `experiment/model/stage/seed/time_average/gpu_vram` + auto `run_id/git_sha/run_date`; `stage ∈ {smoke, poc, headline}`, only `headline` citable.

---

## 8. Open decisions (supervisor sign-off = the SB gate)

1. **Primary engine** — *(locked)* parametric teacher→student KD (client LoRA + SQL/KD/Structure loss + Exec filtering → FedAvg/FedProx → `M_G`). Demo-level KD = variant; Fed-ICL fusion = baseline.
2. **Client count** — *(locked)* 3 default + sweep `{3,5,10}` (F6). Cross-silo; matches Fed-ICL [5] (FedCoLLM [8] uses 4 — note the offset in §4.1).
3. **Student model** — *(locked 2026-06-12)* Qwen2.5-1.5B-Instruct (tokenizer-aligned with the Qwen2.5-72B teacher → MinED-free P2). Others → A5.
4. **Second dataset** — Spider-Realistic now; BIRD only if P2 lands early. **(confirm)**
5. **Teacher access & compute** — *(locked)* Qwen2.5-72B paid API both stages (`X` ≈ $1–2, paper < $10), targets cached once. **Stage-A on Mac M4 Pro (local, fp16) or Colab Pro** — no extra gate (PoC is `$0`/already-subscribed; the gate guards only Stage-B paid-per-hour spend). Mac trains the 1.5B student fine (24GB ≫ fp16 1.5B); 4-bit QLoRA path is Colab-only (bitsandbytes = CUDA). **Stage-B paid A100-class** (Colab Pro high-RAM / RunPod / Lambda). **Supervisor confirms Stage-B budget at the gate.**

---

*Grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM + the approved outline + Fig. 1. Mechanism source of truth: `fig1_architecture.md`.*
