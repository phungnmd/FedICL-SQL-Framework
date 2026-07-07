# FedICL-SQL — Decisions & Notation

> Slim decision record. Replaces the retired `detailed_plan.md` (deleted 2026-06-23).
> Migrated here: the locked **notation** + the locked **decisions** that are still load-bearing.
> "What to build next" is **not** pre-planned — decided per session, logged in `LAB_LOG.md`.
> Change a decision here → note it in `LAB_LOG.md` the same session.

---

## 1. Naming — arms by feature, not letters

Experiments/arms are named for **what they are**, never `A`/`B`/`Ab` letters (retired 2026-06-23).
ICL is an **eval-time overlay** (k shots), not an arm → write it as a suffix, e.g. `fedkd@k3`.

Models are **not part of an arm's name** — the arm names a *method*, the run record names the *models* (each run's `metrics.json`: `model` = student, `teacher_model` = KD teacher — no separate ledger, see `CLAUDE.md` "Experiment paths"). Default candidate pair (NOT finalized, see §3.3): student Qwen2.5-1.5B-Instruct, teacher Qwen2.5-7B-Instruct.

| name | what it is | role |
|---|---|---|
| `base` | untrained student SLM, no LoRA | floor |
| `local` | per-client solo LoRA on own `Qᵢ` — no federation, no teacher | federation floor (RQ1) |
| `central` | one LoRA fine-tuned on the pooled private data | centralized ceiling (the RQ1 bar) |
| `fedavg` | LoRA + FedAvg, **no** teacher KD (gold-CE only) | FL-without-our-pieces |
| `fedkd` | full method: client LoRA (gold CE + teacher soft-KL + struct + exec-filter) + FedAvg → global SLM | **FedICL-SQL** |
| `teacher` | LLM teacher few-shot, local per client | accuracy ceiling |

**RQ deltas** (reported as measured analysis, not pass/fail gates):
- `fedkd − local` = **federation gain** (RQ1)
- `fedkd − fedavg` = **teacher value** via soft-KL + CoT (RQ3) — the signal gold CE lacks
- RQ1 bar = `fedkd` approaches the `central` ceiling (small federation gap)

### Legacy alias map (old letters → feature name)

Old docs/runs used letter labels. Historical result dirs keep their old slugs (going-forward rename only). Mapping for reading them:

| old label / slug | feature name |
|---|---|
| `B0`, `base` | `base` |
| `B1`, teacher zero/few-shot | `teacher` |
| `B2`, `slm_only` | `local` |
| `B3`, `centralized_ft`, `b3_k0`, `b3_k3` | `central` |
| `B4`, Centralized-ICL | `central@k3` |
| `B6` / `Ab3`, `ab3_fedavg` | `fedavg` |
| `M_G`, `m_g` | `fedkd` |
| `B7`, Fed-ICL [5] adapted | `fedicl_baseline` (Fed-ICL answer-fusion competitor) |

Ablation letters (`Ab1`–`Ab5`) retired too → name by feature: `no_icl`, `no_fl` (= `local`), `no_teacher` (= `fedavg`), `k_sweep` (k∈{0,1,3,5}), `slm_swap` (Phi-3 / Gemma-2B / TinyLlama).

---

## 2. Notation (paper-facing — matches Fig.1, used in §3)

| Symbol | Meaning | Note |
|---|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) | not `L` (retired) |
| `T` | # federated rounds (PoC 2–3) | |
| `k` | # ICL shots (∈{0,1,3,5}) | lower-case |
| `E` | local epochs / round (1–2) | |
| `ρ` | masking ratio (default 0.2 per [10], sweep 0.1–0.5) | fraction of gold SQL tokens masked for imperfect data (KID only) |
| `ŷ` | imperfect SQL (student one-pass rewrite of masked `y`) | KID's KD target sequence (RKD targets gold `y`) |
| `p` | teacher logprob distribution over the KD target | soft label |
| `q` | student logprob distribution over the KD target | distill target |
| `M_T`, `Mᵢ`, `M_G` | teacher 7B (local, frozen, per client) / client-`i` student / global SLM | |
| `Sᵢ`, `Qᵢ` | client-`i` private schema / private (NL,SQL) pairs | never leave client |
| `θ` | LoRA params | no public set, no ICL Hub |

**Research questions** (verbatim from approved outline — do not rename):
RQ1 = Federated Learning effectiveness · RQ2 = In-Context Learning effectiveness · RQ3 = Large-to-Small LM knowledge transfer & efficiency.

---

## 3. Locked decisions

1. **Primary engine** — *(design updated 2026-06-29, dataset question reopened 2026-07-07, KD directions re-locked 2026-07-07)* Two-step training (Step 1 KD-pretrain on a public corpus → Step 2 gold-CE FT on private `Qᵢ`, sequential per `system_architecture.md` §5.6) + FedAvg remains the target **full-method architecture**:
   - **KD step:** online logit-level KD from **[10]**, teacher + student co-loaded, one teacher forward per step. Two directions: **RKD** (`RKL(q‖p)` on gold `y`) and **KID** (`RKL(q‖p)` on imperfect `ŷ` = student one-pass rewrite of `ρ`-masked gold). Both add the auxiliary gold-CE (MLE) loss per [10]: `L = CE + RKL`, weights 1:1 default.
   - **FT step:** `L_FT = CE(student, gold_sql)` on private `Qᵢ`, LoRA init from the KD-step adapter, teacher unloaded.
   - **CoT direction removed (2026-07-07):** Struct-SQL [11] QP-CoT distillation and its offline teacher-target pipeline are dropped entirely — no offline traces, no CoT targets, no SeqKD baseline.
   - Teacher never sees `Qᵢ` (systems property — motivation = shared public KD corpus aligns client updates / less FedAvg drift, **not** privacy: teacher is on-premise, reading `Qᵢ` would leak nothing; reframed 2026-07-06). FedAvg LoRA deltas → `fedkd` global SLM.
   - **FedAvg weighted `nᵢ/n`** (McMahan), not 1/K — non-IID split → unequal client sizes (fixed 2026-07-06). LoRA A/B-averaging caveat acknowledged in paper.
   - Fed-ICL [5] answer-fusion = parameter-free baseline.
   - **What's deferred (2026-07-07):** which corpus is the KD step's public data (BIRD dropped; no replacement locked). **Until it's picked, run the PoC (`KD_PLAN.md` §PoC) directly on Spider** — three arms from base on identical data (`central_ft` / `central_rkd` / `central_kid`), no two-step split, no federation — to validate the KD signal itself before wiring the full design to any specific corpus.
2. **Client count** — *(locked)* 3 default + sweep `{3,5,10}`. Cross-silo; matches Fed-ICL [5] (FedCoLLM [8] uses 4 — note the offset in §4.1).
3. **Teacher & student models** — ⚠️ **NOT finalized (2026-06-23).** Current **default candidates**: teacher = Qwen2.5-7B-Instruct, student = Qwen2.5-1.5B-Instruct (tokenizer-aligned → soft-KL KD without MinED). Both are CLI args (`--teacher-model`, `--model`), not hardcoded gates; alt students → `slm_swap` ablation. **The pair to lock is still open** — pick after a model sweep. Every run **records the actual ids used** in its own `metrics.json`: `model` (student), `teacher_model` (`""` when no KD). So results are never ambiguous about which models produced them. ⚠️ **Outline drift:** approved outline §4.1 lists Phi-3-mini / Gemma-2B / TinyLlama students; reconcile §4.1 with whatever pair is locked **+ supervisor sign-off**.
4. **Datasets** — *(re-opened 2026-07-07, replaces BIRD decision of 2026-06-29/07-06)* **BIRD dropped entirely** — 8.9 GB DB download too heavy and too complex (dialect gap, `evidence`-field dependence) to justify as the KD stream; also dropped as secondary eval benchmark (no cross-dataset claim for now). Primary training + eval unchanged: **Spider** (train 8659, frozen test = Spider dev 1034), same as before BIRD was ever introduced. **The public/second KD corpus question is deferred, not decided** — no dataset is locked as "the" KD stream. Before that decision, run a **PoC on Spider itself** (`KD_PLAN.md` §PoC): same private Spider data, compare training it as plain gold-CE FT vs. as a KD signal (both directions, RKD and KID) from the base model — establishes whether KD-style supervision beats plain FT on identical data, independent of which corpus eventually supplies the public KD stream.
5. **Teacher access & compute** — *(updated 2026-06-29, dataset genericized 2026-07-07)* teacher frozen, local HuggingFace, on-premise. For the PoC: runs on Spider train, same invariant as always applies once a public corpus is picked — **never touches the private/held-out `Qᵢ` the arm is evaluated on**. Co-loaded with student for **both** directions (online RKD/KID, 1 teacher forward per step, no decoding). VRAM: ~17 GB fp16 simultaneous → A100 40 GB+; 16 GB cards (T4/A5000) — 4-bit teacher (≈ 5–6 GB) + student (≈ 3 GB). Teacher ICL: k=3 from the same KD-stream demos (question-only, `never_schema`) — full method only; PoC scores at k=0.
6. **ICL demo rendering** — *(locked 2026-06-20)* default `demo_style=never_schema` (question + verbatim SQL, no source DDL). `skeleton` (identifier-masked) = stronger-privacy ablation. `full` (DDL+SQL) **removed** — reintroduced schema-bleed. Builder = `fedicl_sql/prompts/builder.py`; eval default = `experiments/eval_arms/run.py`. **ICL follows DAIL-SQL [9]:** question-similarity retrieval, SQL-only demos, k=3 (inverted-U at k=5).

   **Demo-style parity (locked 2026-07-06):** train `demo_style` == eval `demo_style` within any arm. Default `never_schema` end-to-end; paired `skeleton` (train+eval) = privacy cell; style-shift (train `skeleton` → eval `never_schema`) = separate analysis experiment, never a default. (Both deferred with the full plan, `KD_PLAN.md` §Deferred.)

   **Ablation (locked 2026-06-29, corrected 2026-07-06):**
   - `fedkd_teacher_k3` (default): teacher scores `ŷ` WITH ICL k=3 from the **KD-stream data** (never the arm's own held-out/private eval data — invariant #2) → ICL-enhanced soft labels
   - `fedkd_teacher_k0`: teacher scores `ŷ` WITHOUT ICL → shows value of ICL-enhanced teacher labels
   - `fedkd@k3` vs `fedkd` (k=0 at inference) → shows value of ICL at inference time
7. **Tracking** — *(locked 2026-06-23, ledger dropped 2026-07-07)* progress in `LAB_LOG.md`, canonical numbers in each run's `experiments/<exp>/results/<run_id>/metrics.json` via `save_results` — no separate `RUNS.csv` ledger (a derived index that drifted from the folders it summarized; `analysis/compare.py`/`analysis/log_session.py` scan the folders directly now). No A/B letters. This file = decision/notation record.
8. **KD comparison hygiene** — *(revised 2026-07-07 (2), CoT dropped)* Full control ladder (`fedavg → fedavg_pub → fedkd_rkd → fedkd`) is deferred until the public corpus is picked (see dec.4). **For now:** the PoC compares, on identical Spider data, from the base model: `central_ft` (gold CE, no teacher) vs `central_rkd` (`CE + RKL` on gold `y`) vs `central_kid` (`CE + RKL` on imperfect `ŷ`, ρ=0.2 Random). Each rung adds one ingredient: `central_rkd − central_ft` = teacher-logit value, `central_kid − central_rkd` = imperfect-data value. Old E0.3 blocker resolved — KID mask-fill mechanics pinned from [10] (`KD_PLAN.md` §mechanics). DP claim scoped to "DP-ready + (ε, EX) curve" (K=3 → no strong-ε promise). Staged run order = `KD_PLAN.md` §PoC.

---

*Grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM, [9] DAIL-SQL, [10] KID + the approved outline + Fig. 1. Mechanism source of truth: `fig1_architecture.md`. Full system: `system_architecture.md`.*

> **[10] KID** (Zhong et al. 2024, arXiv:2410.11371) — "Learning from Imperfect Data: Efficient KD for Text-to-SQL". **Source of BOTH our KD directions** (re-locked 2026-07-07): **RKD** = reverse KL on gold data (their strongest ground-truth-data baseline, +1.9…+3.1 avg) and **KID** = reverse KL on imperfect (student-rewritten) data that simulates inference's cascading errors (+3.2…+5.8 avg, best performance/latency trade-off; ~2× SFT latency vs GKD's ~11–14×). Reverse KL > forward KL for SQL (mode-seeking fits precise low-diversity tokens). Also anchors the **in-context-tuning argument**: ICL's −1..−2 pp on a `train-k=0` FT student is the SAME train/test mismatch KID targets → fix by training in the inference condition (`train-k=3`).
>
> **[11] Struct-SQL** (arXiv:2512.17053) — QP-CoT distillation direction, **dropped 2026-07-07** along with the whole offline CoT-target pipeline. Kept in the reference folder for related work only.
