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
| **Federation engine** | **Parametric teacher→student KD.** Clients LoRA-train on own private `Qᵢ` (gold CE + local teacher KD on same `Qᵢ`), upload **LoRA deltas only** (encrypted/compressed/DP-noised), server **FedAvg/FedProx → Global SLM `M_G`** broadcast. | Fig.1; outline §3.7–3.8; **FedCoLLM [8]** |
| **Teacher `M_T`** | **Qwen2.5-7B-Instruct** via local HuggingFace (no API, no cloud cost). Runs **offline once per client** on client's own private `Qᵢ`. Top-K logprobs via HF generate → soft-KL distillation (Qwen↔Qwen tokenizer aligned, no MinED). VRAM: sequential (7B → unload → 1.5B student). | advisor request 2026-06-16 |
| **Student `Mᵢ`** | **Qwen2.5-1.5B-Instruct** (locked 2026-06-12) — tokenizer-aligned with the teacher → **soft-KL KD without MinED (single-phase, no P2)**. Phi-3-mini / Gemma-2B / TinyLlama = A5 ablation. | own choice; tokenizer match |
| **Clients** | `K = 3` default + sweep `{3,5,10}` (F6). Cross-silo (few large orgs). | Fed-ICL [5]; FedCoLLM [8] uses 4 |
| **ICL** | Schema-aware retrieval, **masking retrieval-only**, demos shown **unmasked**, run **locally** per client. | Light-SQL [4] |
| **Privacy** | No raw rows / no schema leave client; only **encrypted, DP-perturbed LoRA-delta weights** transmit. Masking + DP gradient perturbation are the mechanisms. (Never claim "no weights leave" — weights DO cross.) | Fig.1 "Weights Only" |
| **Staging** | **Stage-A PoC** (~$2, 1 seed, ~200 q/client subset, **Mac MPS or Colab Pro GPU**, `T=2–3`, `E=1`, no DP, `stage=poc`) → **SB gate** → **Stage-B headline** (paid A100-class GPU, ≥3 seeds + significance, DP measured, `stage=headline`). Only `headline` enters the paper. | budget triage |
| **Compute / repo** | **3 tiers (re-locked 2026-06-16):** (1) **Mac M4 Pro 24GB MPS** = dev + all `$0` baselines (B2, B3) + p0 floor; (2) **Colab Pro T4** = teacher targets gen (7B `--load-in-4bit` ~4 GB) + student LoRA training (~11 GB fp16; sequential: unload teacher before training); (3) **paid A100-class** = Stage-B headline only. **No API cost** — teacher is local 7B. ⚠️ one stack per comparison set. Code repo `github.com/phungnmd/fedicl-sql` (private). | locked 2026-06-16 |
| **SB gate** | PoC directionally healthy (`M_G` approaches centralized ceiling **B3** — small federation gap — and `M_G − Ab3` quantifies teacher value) **AND** supervisor sign-off on §8 + budget. Report `M_G − B2` (federation gain), `M_G − Ab3` (teacher value via soft-KL + CoT) as **measured analysis, not pass/fail gates**. | risk control |

**Reference shorthand:** [4] Light-SQL (NL2SQL+ICL base, same corresponding author) · [5] Fed-ICL (parameter-free answer-fusion + convergence proof + prompt-extraction attack) · [6] IFed-ICL (implicit vectors, classification — side ref) · [7] FedMKT (logit-space KD + token-alignment; does NOT FedAvg weights) · [8] FedCoLLM (LoRA-adapter FedAvg + global SLM + CE+λKL KD — the engine anchor) · [1] federated BART · [2] prior thesis · [3] ICL survey.

---

## 0. Canonical labels & notation (single source — todo + outline must match)

**Why this block exists:** outline, plan, and todo drifted on symbols/labels. This is the one authoritative map; everything else points here. Paper-facing notation = **Fig.1**.

**Notation (paper-facing — matches Fig.1, used in §3 + outline):**

| Symbol | Meaning | Note |
|---|---|---|
| `K` | **# clients** (default 3, sweep {3,5,10}) | ⚠️ was `L` in old plan/todo — `L` is **retired**, never reuse |
| `T` | **# federated rounds** (PoC 2–3) | ⚠️ old plan used `K` for rounds in one spot — retired |
| `k` | **# ICL shots** (∈{0,1,3,5}) | lower-case |
| `E` | local epochs / round (1–2) | |
| `λ₁…λ₄` | loss weights: SQL / KD / struct / exec | Fig.1 verbatim |
| `M_T`, `Mᵢ`, `M_G` | teacher 7B (local, per client) / client-`i` student / global SLM | |
| `Sᵢ`, `Qᵢ` | client-`i` private schema / private (NL,SQL) pairs | never leave client |
| `θ` | LoRA params | X and G retired (no public set, no ICL Hub) |

**Research questions (verbatim from approved outline — do not rename):**
RQ1 = Federated Learning effectiveness · RQ2 = In-Context Learning effectiveness · RQ3 = Large-to-Small LM knowledge transfer & efficiency.

**Baselines (B#) — one model may wear several labels:**

| B# | Name | Role | Alias |
|---|---|---|---|
| B1 | LLM-only (teacher zero/few-shot) | accuracy ceiling | — |
| B2 | SLM-only (own private, no fed/teacher) | RQ1 floor | arm `slm_only` |
| B3 | Centralized-FT (pool all private, 1 LoRA) | true parametric ceiling (the RQ1 bar) | — |
| B4 | Centralized-ICL | privacy-violating ICL ceiling | — |
| B5 | Without-ICL (SLM zero-shot) | ICL value | = **Ab1** |
| B6 | FedAvg-LoRA (no teacher, no ICL) | FL-without-our-pieces | = **Ab3a**, arm `gold_ce` |
| B7 | Fed-ICL [5] adapted to SQL | closest federated competitor | — |

**Teacher-value comparison (P1′, todo step 8) — 3 models compared on each client's own eval set:**
`m_g` (= FedICL-SQL full method) · `slm_only` (B2, per-client solo, no fed, no teacher) · `ab3_fedavg` (Ab3 = FedAvg without teacher KD, gold fallback only).
**Report** two deltas as RQ evidence (not pass/fail gates): `m_g − slm_only` (federation gain), `m_g − ab3_fedavg` (teacher value via soft-KL + CoT — signal gold CE lacks).

**Ablations (Ab#):** Ab1 Without-ICL (=B5) · Ab2 Without-FL (local-only) · Ab3 Without-Teacher = FedAvg-no-KD (gold fallback for all Qᵢ) · Ab4 Retrieval-size `k∈{0,1,3,5}` · Ab5 Different-SLMs.

**Tables/Figures:** T1 Overall · T2 Efficiency · T3 Communication. F1 Architecture · F2 Convergence · F3 Pareto · F4 Heterogeneity · F5 Privacy (F5a demo-channel / F5b weights-channel) · F6 Client-scaling.

**Stages & tiers:** `stage ∈ {smoke, poc, headline}` (RUNS.csv; only `headline` citable). Stage-A PoC → **SB gate** → Stage-B headline. Run tiers: Tier-1 must / Tier-2 should / Tier-3 nice.

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

> Each organization runs a local 7B LLM teacher on its own private data, then fine-tunes a 1.5B SLM student via knowledge distillation. Federated aggregation pools the student LoRA deltas into a Global SLM that matches or approaches the centralized ceiling — while transmitting only encrypted, DP-perturbed LoRA-delta weights, never raw schemas, data, or teacher outputs.

### 1.3 Contributions

1. **Federated LLM–SLM framework for Text-to-SQL** (FedICL-SQL): client-side local 7B teacher + per-client KD + federated aggregation engine; SLM students with local private schemas (Fig. 1). No cloud API, no shared data.
2. **Schema-aware ICL**: schema-aware retrieval + prompt construction from local Qᵢ examples (Qᵢ-only pool, no shared ICL Hub); masking supports retrieval/de-identification without placing masked SQL placeholders into the final prompt. ⚠️ **ICL must be load-bearing — it's in the title.** ICL value = held-out cross-schema generalization (RQ2). If ICL shows ~0 delta on seen *and* held-out schemas, title overclaims — surface at gate.
3. **Federated SQL knowledge distillation with local teacher domain-adaptation**: client-side 7B teacher first fine-tunes on Qᵢ (domain adaptation), then annotates Qᵢ with CoT+SQL+logprobs → SLM trains on annotated dataset (single pass: teacher target if exec_correct, else gold fallback); server FedAvg/FedProx-aggregates deltas. Novelties = **(i) per-client teacher domain-adaptation before KD**, **(ii) exec-based KD-target filtering**, **(iii) CoT distillation**, **(iv) skeleton-token structure loss**.
4. **Privacy-preserving collaborative optimization**: round-based protocol transmitting only encrypted, DP-perturbed LoRA-delta weights; bounded per-round communication; secure aggregation. Report (ε, EX) at Stage-B to validate the DP contribution.
5. **Extensive evaluation** on Spider + Spider-Realistic under a federated non-IID partition, with FL / efficiency / privacy metrics and five ablations.

### 1.4 Research questions

- **RQ1 (FL effectiveness):** does federation beat isolated per-client SLM? → Overall Performance + convergence-vs-rounds. ⚠️ *Beating B2-solo is near-guaranteed* (FedAvg pools ~K× effective data — vanilla FedAvg, not our novelty). The **publishable** RQ1 claim = `M_G` **approaches the centralized ceiling B3** (small federation gap, T3) while preserving privacy — frame it that way, not as the trivial `> B2`.
- **RQ2 (ICL effectiveness):** does schema-aware ICL improve generalization to unseen DBs? → cross-DB held-out split + Impact-of-ICL + retrieval-size ablation.
- **RQ3 (LLM→SLM transfer & efficiency):** better efficiency–performance tradeoff than LLM-only or SLM-only? → Impact-of-Teacher + efficiency table + Pareto. The **Without-Teacher ablation** isolates teacher value; soft-KL (dark knowledge) + CoT carry signal gold labels lack.

---

## 2. Method specification

### 2.1 Notation & problem (§3.1)

**Notation = §0 registry** (canonical, matches Fig.1): clients `K`, rounds `T`, shots `k`, epochs `E`, loss weights `λ₁…λ₄`. The old `L`=clients / `K`=rounds convention is **retired** — use `K`/`T` everywhere.

Federated system: server `S` + `K` clients. Client `i` holds private schema `Sᵢ = {Tᵢ, Cᵢ, Rᵢ}`, a private example store `Qᵢ = {(qₙ, sₙ)}` of NL/gold-SQL pairs, a **local teacher** `M_T` (Qwen2.5-7B, runs offline per-client on Qᵢ), and a **local SLM student** `Mᵢ` (Qwen2.5-1.5B-Instruct, LoRA-adapted). Server holds **aggregation engine** `A` and the broadcast **Global SLM** `M_G` only.

Per-client goal ([4] Eq. 1): learn `f:(q, Sᵢ) → s*` maximizing execution accuracy `EX = 1[Exec(ŝ,Dᵢ)=Exec(s*,Dᵢ)]`. Federated goal: maximize mean EX across clients while `Sᵢ` and raw `Qᵢ` stay private; only protected LoRA-delta weights cross the wire.

### 2.2 Framework overview (§3.2) — Fig. 1

```
SERVER : Aggregation Engine (FedAvg/FedProx) | Global SLM M_G
        ↕  secure channel (SSL/TLS · Secure Agg · DP gradient perturbation · masking)
        ↕  UP: encrypted LoRA deltas (Weights Only)   DOWN: global params M_G only
CLIENTS (Org 1..K) : Local Teacher M_T (7B, offline on Qᵢ) → annotated Qᵢ dataset (client_i_train_kd.csv)
                     Local Schema Sᵢ + private Qᵢ → Schema Encoder → Retrieval (Qᵢ only) → ICL Prompt
                     → Local SLM (decode) → SQL+reasoning → Local Training (single-pass KD) → LoRA delta
```

**Offline, two steps per client (before rounds):**

1. **Teacher domain-adaptation (`fine_tune_teacher.py`):** fine-tune the base 7B teacher on the client's own `Qᵢ` with LoRA (gold CE on SQL). Adapts teacher to client's schema vocabulary and SQL patterns. Output = per-client LoRA adapter. VRAM: ~28-32 GB fp16 (A100); skip with `--max-steps 0` for PoC on T4.

2. **Annotate Qᵢ (`gen_teacher_targets.py`):** load domain-adapted teacher (base + adapter merged), run on each `(q, schema) ∈ Qᵢ`, produce **annotated training dataset** `client_i_train_kd.csv` — the original Qᵢ with teacher columns added: `teacher_sql, reasoning, exec_ok, exec_correct` + per-token top-K logprobs in `.logprobs.jsonl`. Exec-filter: only `exec_correct=True` rows use teacher supervision during SLM training.

Teacher never sees other clients' data; outputs stay fully on-premise.

**One federated round `t`:**
1. **Broadcast** global params `M_G` to clients (no ICL Hub demos; retrieval is local).
2. **Local ICL** — client `i` builds prompts from `Sᵢ` + demos retrieved from `Qᵢ` only (§2.3).
3. **Local training** — client LoRA-trains its SLM on **own private `Qᵢ`** (gold CE + local teacher KD on same `Qᵢ`): `L_i = L_SQL(Qᵢ) + L_KD(Qᵢ, teacher_targets_i)` (§2.5). Per-client teacher targets make each delta carry org-specific skill → non-trivial federation.
4. **Privacy-safe upload** — LoRA deltas only, encrypted/compressed/DP-perturbed. No schema, data, full weights, or teacher outputs cross the wire.
5. **Aggregation** — `A` FedAvg/FedProx-aggregates deltas → `M_G`.

The protocol is **parametric federated distillation**, grounded in **FedCoLLM [8]**; **FedMKT [7]** is a logit-space KD reference (related work); **Fed-ICL [5]** is the parameter-free baseline. **Teacher–student collaboration (§3.5) = training-time KD roles only** — runtime low-confidence escalation is OUT (adds inference-time teacher cost + leaks client query patterns to the server, contradicting privacy); mention as deployment option in §5.

### 2.3 Schema-aware ICL (§3.6) — the RQ2 engine

Prompt construction ([4] Eq. 3): `σ(q, S, I, Q) = q ⊕ S ⊕ I ⊕ Q`
- `I`: system instruction ("expert SQL generator, output SQL only").
- `S`: schema serialized as DDL (types + FK join paths).
- `Q`: top-`k` demos retrieved via BGE embeddings in FAISS.

**Masking = retrieval-only ([4]).** Mask table/column identifiers to canonical tokens for the *retrieval-similarity* score (privacy + de-identification + structure-based transfer); the demos **shown to the model are always unmasked**. Never put masked SQL placeholders into the generation prompt. Select `k ∈ {1,3}` ([4] sweet spot, inverted-U at k=5). ⚠️ Masking can **cost** EX ([4]: MQS_S 37% < QTS_S 41%) — frame as a privacy/transfer lever, not an accuracy win.

**ICL runs locally per client** on same-schema demos from `Qᵢ` only. No server-side ICL Hub (G removed). Cross-schema generalization (RQ2) comes from the **Global SLM's skill + local ICL** on the held-out schema's own few demos.

### 2.4 Teacher & Student (§3.3–3.4)

- **Teacher `M_T`** (Qwen2.5-7B-Instruct, **local HF, per-client**): on **client's own `Qᵢ`**, produces **SQL + reasoning steps (CoT)** + top-K logprobs, exec-validated, cached locally → feeds per-client KD targets. Never sees other clients' data. Unloaded before student training.
- **Student `Mᵢ`** (Qwen2.5-1.5B-Instruct primary; Phi-3-mini / Gemma-2B / TinyLlama = A5 ablation): training = **LoRA fp16** (~11 GB T4). Inference only: optional `LOAD_IN_4BIT=1` for eval when VRAM tight. Two modes: **LoRA-adapted via KD** (parametric, primary) or **frozen + ICL** (parameter-free variant/baseline).

### 2.5 Federated SQL knowledge distillation (§3.7) — the RQ1+RQ3 engine

**Fig.1's verbatim client total loss:** `L = λ₁·L_SQL + λ₂·L_KD + λ₃·L_struct + λ₄·L_exec`. §3.7 must present **this λ-form**, then define each term.

⚠️ **Federation-validity.** Per-client teacher domain-adaptation ensures each client's KD targets reflect its own schema/domain → heterogeneous deltas → non-trivial federation. Verify with delta_stats pairwise cosine < 0.999.

**Single-pass training objective — one sequence per Qᵢ example:**

For each `(q, gold_sql) ∈ Qᵢ` (from `client_i_train_kd.csv`):
- `exec_correct=True` → `target = CoT⊕teacher_sql`, soft-KL active (source="kd")
- `exec_correct=False` → `target = gold_sql`, no KL (source="gold")

Every question appears exactly once. `exec_correct` ensures teacher_sql ≡ gold_sql semantically.

**The four Fig.1 losses, literal:**
- **SQL loss** = CE on target SQL token sequence (teacher SQL when exec_correct, gold SQL otherwise).
- **KD loss** = soft-KL distillation: `KL_τ(student logits ‖ teacher top-K logprobs)` where logprobs come from the local 7B teacher via HF generate. Qwen-7B↔Qwen-1.5B share a tokenizer → **no MinED, no separate P2 phase** (single-phase hard+soft KD).
- **Structure loss** `β·L_struct` = **weighted token-level CE on SQL skeleton-token subsequence** (clause keywords, identifiers stripped). Differentiable, backprops cleanly. NOT AST-edit-distance.
- **Execution** = teacher-target **filtering**, NOT a gradient term (exec is non-differentiable → data gate). Stored as `exec_ok` / `exec_correct` in annotated dataset. Keep target only if result set equals gold (exec-match).

**Reasoning/CoT.** Teacher emits `(reasoning, SQL)` per Qᵢ item; reasoning is part of the KD target sequence (CoT distillation). At inference, reasoning is optional (SQL-only for latency).

**Novelty framing:** exec-guidance for SQL is prior art. Our novelties = **(i) per-client teacher domain-adaptation before KD** + **(ii) exec-based KD-target filtering inside the federated loop** + **(iii) skeleton-token structure loss** + **(iv) CoT distillation**.

Client uploads **LoRA deltas only** (encrypted/compressed/DP-perturbed); server aggregates by **FedAvg/SecureAvg** → `M_G`. = **FedCoLLM [8]** (LLM→SLM half only). **Not FedMKT [7]** (logit-space KD, never FedAvgs weights).

### 2.6 Federated optimization & protocol (§3.8) — Algorithm 1

```
Algorithm 1: FedICL-SQL (parametric engine — primary)
Input: clients {Sᵢ, Qᵢ, Mᵢ}, rounds T, LoRA init θ₀
Offline (per client i, before rounds):
  M_T^i ← fine_tune_teacher(base_7B, Qᵢ)          # domain-adapt teacher on Qᵢ
  kd_data_i ← gen_teacher_targets(M_T^i, Qᵢ)       # annotated Qᵢ: CoT+SQL+logprobs, exec-filtered
  unload M_T^i                                       # free VRAM for student training
 1: M_G ← base SLM + θ₀
 2: for round t = 1..T:
 3:    broadcast M_G to all clients                  # params only, no ICL Hub
 4:    for each client i in parallel:
 5:        θᵢ ← LoRA-train Mᵢ on kd_data_i          # single-pass: teacher target if exec_correct, else gold
 6:        Δθᵢ ← encrypt/compress/DP-perturb(θᵢ − θ_{t−1})
 7:        upload Δθᵢ                                # Weights Only
 8:    θ_t ← θ_{t−1} + (1/K) Σᵢ Δθᵢ  ;  M_G ← base + θ_t   # FedAvg/FedProx
 9: return M_G ; per-client adapters for local inference
```

Convergence: cite **FedAvg (McMahan 2017) / FedProx (Li 2020)** convergence results — they cover *parametric weight aggregation*, which is our mechanism. ⚠️ Do **NOT** borrow Fed-ICL Thm 4.1/Cor. 4.2: it proves convergence for *parameter-free answer-fusion*, a different mechanism — a reviewer will flag the mismatch. Report **empirical** convergence (EX vs rounds) as the primary evidence; theory is motivation only. Per-round communication = bounded LoRA-delta size (the efficiency claim). **Baseline variant (Fed-ICL [5]):** clients propose SQL on a shared query set using own private demos; server fuses by exec-vote/Fusion-LM; iterate — parameter-free comm-cost/convergence comparator, never the method.

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

🔴 **Schema-disjoint 2-pool split (anti-leakage, mandatory).** Partition Spider DBs into **client-private `{Sᵢ}`** (one DB-group per client, all train DBs) and **held-out** (cross-schema eval = Spider dev), with `private ∩ held-out = ∅` — no DB in two pools, eval questions never in train. Persist DB-id→pool, release it. **Dirichlet(α)** over all train DBs controls heterogeneity, `α ∈ {0.1, 1.0, 100}` (low→high IID). Default `K = 3` (cross-silo); sweep `{3,5,10}` (F6). ⚠️ **Report per-client N at each K** in the F6 caption — at `K=10` data thins per client; frame as data-starvation, not a method failure. Small `K` = deliberate **cross-silo** choice.

**Eval-set provenance (state in §4.1):** per-client own-schema eval = 20% per-DB slice of **Spider train** (`train_frac=0.8`); held-out-schema eval = **Spider dev** (frozen test). Don't let a reviewer discover this footnote unaided.

**Data hygiene:** tune on `val` (a seeded slice of Spider train); the `test` split (= Spider dev) is **frozen** — touch once for final numbers. Headline = ≥3 seeds + significance.

**Data pipeline & tracking (repro contract).** Two deterministic stages, raw → processed:

```
data/raw/spider/   download_spider.py   (JSON + per-DB .sqlite; 1.9 GB; GITIGNORED, fetched per machine)
   ├─ build_processed.py  → data/processed/centralized/  train.csv · val.csv · test.csv(1034=Spider dev, FROZEN) · meta.json
   └─ build_federated.py  → data/processed/federated/<K>c-a<α>-s<seed>/
         client_i_{train,eval}.csv · held_out.csv(1034) · split.json(DB→pool map) · meta.json(seed/α/db_pool_map)
         [no public_X.csv — all train DBs go to clients]
   └─ fine_tune_teacher.py + gen_teacher_targets.py  → client_i_train_kd.csv + client_i_train_kd.logprobs.jsonl
         (per client; annotated Qᵢ with teacher columns; committed to repo ~5 MB)
```

A CSV row = `question, query, db_id, db_path`; `db_path` is **relative** (`data/raw/...sqlite`) → portable. **All processed CSVs + split.json + meta.json + teacher targets are committed** (~5 MB) — the exact frozen split travels with the repo (no rebuild, no drift); only the heavy raw DBs are regenerated. `build_*` are deterministic per `--seed`, so a rebuild reproduces the committed `db_pool_map` byte-for-byte. The `fedicl_sql` lib + `experiments/*/run.py` read these processed CSVs; the Colab bootstrap (`notebooks/00_colab_bootstrap.ipynb`) reuses the same scripts + CSVs.

### 3.2 Models (§4.1)

- **Teacher:** Qwen2.5-7B-Instruct, **local HuggingFace per client**. Step 1: LoRA-SFT on Qᵢ (domain adaptation). Step 2: generate `client_i_train_kd.csv` (annotated Qᵢ with CoT+SQL+top-K logprobs, exec-filtered). No API cost. VRAM: A100 for SFT; T4 with `--load-in-4bit` for inference.
- **Students:** **Qwen2.5-1.5B-Instruct primary** (tokenizer-aligned with the teacher → soft-KL KD without MinED); Phi-3-mini (3.8B), Gemma-2B, TinyLlama-1.1B for the SLM-arch ablation (A5). **LoRA fp16**, temp=0, max-new-tokens=256 ([4]).
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

🔴 **Statistical rigor.** Every headline number = **mean ± std over ≥3 seeds** (seeds vary partition + LoRA init + retrieval sampling). Make-or-break comparisons get a **significance test** (paired bootstrap over per-query EX, or McNemar) + p / CI. ⚠️ With only 3 clients × ~200 q/client, per-client power is low — **pool per-query EX across all clients** for the test (matched pairs on the same queries), and always report **effect size + CI**, not just p. Temp=0 fixes decoding, not seed-level variance.

### 3.5 Tables / figures (§4.2)

1. **T1** Overall — EX/EM, all methods × {Spider, Spider-Realistic}; seen vs held-out (RQ1).
2. **T2** Efficiency — latency/VRAM/FLOPs (RQ3).
3. **T3** Communication — bytes/round + rounds-to-converge vs FedAvg-LoRA & Fed-ICL (RQ1).
4. **F1** Architecture (= provided Fig. 1).
5. **F2** Convergence — EX vs round, per α (RQ1).
6. **F3** Pareto — EX vs cost; FedICL-SQL dominates SLM-only, approaches teacher (RQ3).
7. **F4** Heterogeneity — EX vs Dirichlet α (RQ1/RQ2).
8. **F5** Privacy — F5a prompt-extraction ± masking (demo channel); F5b MIA on `M_G` / DP (ε, EX) (weights channel). Never cite F5a for weights.
9. **F6** Client scaling — EX + comm vs `K ∈ {3,5,10}` (caption reports per-client N).

### 3.6 Ablations (§4.2)

1. **Without ICL** — drop demos → isolate ICL.
2. **Without federated learning** — local-only → isolate federation.
3. **Without Teacher = FedAvg-no-KD (Ab3)** — train SLM on gold SQL only (`teacher_targets=[]`, all examples fall back to gold); run FedAvg → `ab3_fedavg`. Compare to `M_G` (full method with teacher KD). Isolates teacher value: delta = CoT distillation + soft-KL dark knowledge gold CE lacks. Report `M_G − ab3_fedavg`.
4. **Retrieval size** `k ∈ {0,1,3,5}` (inverted-U per [4]).
5. **Different SLMs** — Qwen-1.5B / Phi-3 / Gemma-2B / TinyLlama.

Plus discussion subsections: Impact of ICL, Impact of LLM Teacher, Impact of FL, Communication Efficiency, **Privacy-Utility Trade-off**.

### 3.7 Implementation (§4.1)

PyTorch + HuggingFace; LoRA fp16 students (no 4-bit during training — confirmed 11 GB/T4); FAISS + bge-small retriever; lightweight custom round-loop (single-GPU, clients sequential). Fixed seeds, temp=0. **Federated hyperparams** (cost multipliers, total LoRA passes = K×T×E×runs): Stage-A PoC `T=2–3, E=1`; Stage-B pick `T` from the PoC convergence plateau (cap ≤10), `E=1–2` (high E + non-IID → drift; if drift visible, FedProx μ instead). State `T, E`, LoRA rank/α/lr in §4.1. Release code + partition scripts.

### 3.8 Run staging & minimum publishable set

The full matrix (7 baselines + 5 ablations + α-sweep + K-sweep + DP + 2 datasets × ≥3 seeds × T rounds) is hundreds of LoRA runs — triage by tier (a run belongs to the highest tier whose claim it supports):

- **Tier 1 — must, Stage B, ≥3 seeds + significance.** Teacher-value comparison (`M_G` vs B2-slm_only vs Ab3-fedavg-no-kd), T1 Spider (FedICL-SQL, SLM-only, Centralized-FT, FedAvg-no-KD), Ablation 3, T3. The paper stands or falls here.
- **Tier 2 — should, Stage B, ≥3 seeds where cheap (inference reuses checkpoints).** T2, F2, F3, Ablations 1/2/4, Fed-ICL + Centralized-ICL, RQ2 held-out, **Spider-Realistic** (promoted from Tier 3 — same DBs, only paraphrased questions → near-free, and a single-benchmark headline is thin for a Q3 journal which expects ≥2).
- **Tier 3 — nice, 1 seed, flagged in caption.** F4 α-sweep, F6 K-sweep, DP (ε, EX), Ablation 5, F5b MIA. Budget out → cut Tier 3 and say so.
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
| P1 Federated engine | schema-disjoint 2-pool split; fine_tune_teacher.py (domain-adapt 7B); gen_teacher_targets.py (annotate Qᵢ); client LoRA trainer (single-pass KD); FedAvg + no-op detector; 3-arm teacher-value comparison | P0 |
| ~~P2 Logit-KD~~ (folded into P1) | soft-KL via local 7B HF top-K logprobs (aligned Qwen tokenizer → no MinED, no separate phase) | — |
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
| Federation no gain over local | kills RQ1 | non-IID split → real heterogeneity; verify deltas differ (no-op check); FedProx if drift. ⚠️ note `M_G > B2` is near-trivial — the real bar is `M_G` → B3 ceiling |
| Teacher value modest on labeled data | weak RQ3 | soft-KL top-K logprobs carry dark knowledge gold lacks; per-client domain-adaptation amplifies teacher quality; report `M_G − Ab3` delta |
| PoC stalls mid-run (disconnect) | lost progress | T=2–3, E=1, subset, 1 seed; checkpoint per round to Drive → resume |
| Stage B funding never materializes | no headline | PoC alone not publishable; escalate at the gate |
| "Spider isn't federated" pushback | validity | explicit *simulated* federation via domain partition (standard in [5]); privacy scenario; α sweep |
| Teacher 7B fine-tuning VRAM | feasibility on T4 | fp16 LoRA of 7B needs A100; use `--max-steps 0` on T4 (skip domain-adapt, use base 7B for targets); Stage-B = A100 |
| Logit-KD tokenizer mismatch | KD soft term fails | **aligned Qwen-7B↔Qwen-1.5B tokenizer → no token alignment needed**; top-K logprobs from HF generate |
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
3. **Student model** — *(locked 2026-06-12)* Qwen2.5-1.5B-Instruct (tokenizer-aligned with Qwen2.5-7B teacher → soft-KL KD without MinED). Others → A5. ⚠️ **Outline drift:** the approved outline §4.1 lists students Phi-3-mini / Gemma-2B / TinyLlama and does **NOT** include Qwen2.5-1.5B (the locked primary). Update outline §4.1 to name Qwen-1.5B as primary (others → A5 ablation) **and get supervisor sign-off**.
4. **Second dataset** — Spider-Realistic now; BIRD only if P2 lands early. **(confirm)**
5. **Teacher access & compute** — *(locked 2026-06-16)* Qwen2.5-7B-Instruct local HuggingFace, no API cost. Per-client offline pipeline: (1) `fine_tune_teacher.py` — LoRA-SFT on Qᵢ (A100 for fp16; `--max-steps 0` to skip on T4); (2) `gen_teacher_targets.py` — annotate Qᵢ (T4 OK with `--load-in-4bit`). Student 1.5B LoRA training: T4 ~11 GB (confirmed). **Stage-A PoC**: Mac/Colab T4, skip teacher SFT, base 7B teacher only ($0). **Stage-B paid A100-class** (Colab Pro high-RAM / RunPod / Lambda). **Supervisor confirms Stage-B budget at the gate.**

---

*Grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM + the approved outline + Fig. 1. Mechanism source of truth: `fig1_architecture.md`.*
