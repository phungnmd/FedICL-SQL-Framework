# FedICL-SQL — Decisions & Notation

> Slim decision record. Replaces the retired `detailed_plan.md` (deleted 2026-06-23).
> Migrated here: the locked **notation** + the locked **decisions** that are still load-bearing.
> "What to build next" is **not** pre-planned — decided per session, logged in `LAB_LOG.md`.
> Change a decision here → note it in `LAB_LOG.md` the same session.

---

## 1. Naming — arms by feature, not letters

Experiments/arms are named for **what they are**, never `A`/`B`/`Ab` letters (retired 2026-06-23).
ICL is an **eval-time overlay** (k shots), not an arm → write it as a suffix, e.g. `fedkd@k3`.

Models are **not part of an arm's name** — the arm names a *method*, the run record names the *models* (RUNS.csv `model` = student, `teacher_model` = KD teacher). Default candidate pair (NOT finalized, see §3.3): student Qwen2.5-1.5B-Instruct, teacher Qwen2.5-7B-Instruct.

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

Old docs/runs used letter labels. Historical `RUNS.csv` rows + result dirs keep their old slugs (going-forward rename only). Mapping for reading them:

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
| `λ(t)` | alpha-decay loss weight (1.0 → 0 over **global** steps across all rounds) | balances MLE vs RKL |
| `ρ` | masking ratio (sweep 0.1–0.5) | fraction of gold SQL tokens masked for imperfect data |
| `ŷ` | imperfect SQL (student rewrite of masked `y`) | KD target sequence |
| `p` | teacher logprob distribution over `ŷ` (with ICL) | soft label |
| `q` | student logprob distribution over `ŷ` | distill target |
| `M_T`, `Mᵢ`, `M_G` | teacher 7B (local, frozen, per client) / client-`i` student / global SLM | |
| `Sᵢ`, `Qᵢ` | client-`i` private schema / private (NL,SQL) pairs | never leave client |
| `θ` | LoRA params | no public set, no ICL Hub |

**Research questions** (verbatim from approved outline — do not rename):
RQ1 = Federated Learning effectiveness · RQ2 = In-Context Learning effectiveness · RQ3 = Large-to-Small LM knowledge transfer & efficiency.

---

## 3. Locked decisions

1. **Primary engine** — *(design updated 2026-06-29, dataset question reopened 2026-07-07)* Dual-stream training (Stream 1 gold-CE FT on private `Qᵢ` + Stream 2 KD on a public corpus) + FedAvg remains the target **full-method architecture**, mechanism unchanged:
   - **Stream 1 FT:** `L_FT = CE(student, gold_sql)` on private `Qᵢ`
   - **Stream 2 KID:** student masks gold SQL (ratio `ρ`) → rewrites `ŷ` → teacher forward (frozen, k=3 ICL) scores `ŷ` → `L_KD = RKL(q‖p)`
   - **Combined:** `L = λ₁·L_FT + λ₂(t)·L_KD` (alpha-decay on `λ₂` — **global** over cumulative steps across rounds, not per-round restart; pinned 2026-07-06)
   - Teacher never sees `Qᵢ` (systems property — motivation = shared public KD corpus aligns client updates / less FedAvg drift, **not** privacy: teacher is on-premise, reading `Qᵢ` would leak nothing; reframed 2026-07-06). FedAvg LoRA deltas → `fedkd` global SLM.
   - **FedAvg weighted `nᵢ/n`** (McMahan), not 1/K — non-IID split → unequal client sizes (fixed 2026-07-06). LoRA A/B-averaging caveat acknowledged in paper.
   - Fed-ICL [5] answer-fusion = parameter-free baseline.
   - **What's deferred (2026-07-07):** which corpus is Stream 2's public data (BIRD dropped; no replacement locked). **Until it's picked, run the PoC (`KD_PLAN.md` §PoC) directly on Spider** — no dual-stream mixing, just two separate single-stream arms (FT-only vs KD-only) on the same data — to validate the KD signal itself before wiring the full dual-stream design to any specific corpus.
2. **Client count** — *(locked)* 3 default + sweep `{3,5,10}`. Cross-silo; matches Fed-ICL [5] (FedCoLLM [8] uses 4 — note the offset in §4.1).
3. **Teacher & student models** — ⚠️ **NOT finalized (2026-06-23).** Current **default candidates**: teacher = Qwen2.5-7B-Instruct, student = Qwen2.5-1.5B-Instruct (tokenizer-aligned → soft-KL KD without MinED). Both are CLI args (`--teacher-model`, `--model`), not hardcoded gates; alt students → `slm_swap` ablation. **The pair to lock is still open** — pick after a model sweep. Every run **records the actual ids used**: student in RUNS.csv `model`, teacher in RUNS.csv `teacher_model` (`""` when no KD). So results are never ambiguous about which models produced them. ⚠️ **Outline drift:** approved outline §4.1 lists Phi-3-mini / Gemma-2B / TinyLlama students; reconcile §4.1 with whatever pair is locked **+ supervisor sign-off**.
4. **Datasets** — *(re-opened 2026-07-07, replaces BIRD decision of 2026-06-29/07-06)* **BIRD dropped entirely** — 8.9 GB DB download too heavy and too complex (dialect gap, `evidence`-field dependence) to justify as the KD stream; also dropped as secondary eval benchmark (no cross-dataset claim for now). Primary training + eval unchanged: **Spider** (train 8659, frozen test = Spider dev 1034), same as before BIRD was ever introduced. **The public/second KD corpus question is deferred, not decided** — no dataset is locked as "the" KD stream. Before that decision, run a **PoC on Spider itself** (`KD_PLAN.md` §PoC): same private Spider data, compare training it as plain gold-CE FT vs. as a KD signal (both directions, KID and Struct-SQL) from the base model — establishes whether KD-style supervision beats plain FT on identical data, independent of which corpus eventually supplies the public KD stream.
5. **Teacher access & compute** — *(updated 2026-06-29, dataset genericized 2026-07-07)* teacher frozen, local HuggingFace, on-premise. For the PoC: runs on a Spider slice, same invariant as always applies once a public corpus is picked — **never touches the private/held-out `Qᵢ` the arm is evaluated on**. Co-loaded with student (online KID, 1 forward per step). VRAM: ~17 GB simultaneous. **Headline**: A100 40 GB+. **PoC**: T4 — `--load-in-4bit` teacher (≈ 8 GB) + student (≈ 3 GB) = ~11 GB. Teacher ICL: k=3 from the same KD-stream demos (question-only, `never_schema`).
6. **ICL demo rendering** — *(locked 2026-06-20)* default `demo_style=never_schema` (question + verbatim SQL, no source DDL). `skeleton` (identifier-masked) = stronger-privacy ablation. `full` (DDL+SQL) **removed** — reintroduced schema-bleed. Builder = `fedicl_sql/prompts/builder.py`; eval default = `experiments/eval_arms/run.py`. **ICL follows DAIL-SQL [9]:** question-similarity retrieval, SQL-only demos, k=3 (inverted-U at k=5).

   **Demo-style parity (locked 2026-07-06):** train `demo_style` == eval `demo_style` within any arm. Default `never_schema` end-to-end; paired `skeleton` (train+eval) = privacy cell (KD_PLAN E3.4); style-shift (train `skeleton` → eval `never_schema`) = separate analysis experiment (E3.5), never a default.

   **Ablation (locked 2026-06-29, corrected 2026-07-06):**
   - `fedkd_teacher_k3` (default): teacher scores `ŷ` WITH ICL k=3 from the **KD-stream data** (never the arm's own held-out/private eval data — invariant #2) → ICL-enhanced soft labels
   - `fedkd_teacher_k0`: teacher scores `ŷ` WITHOUT ICL → shows value of ICL-enhanced teacher labels
   - `fedkd@k3` vs `fedkd` (k=0 at inference) → shows value of ICL at inference time
7. **Tracking** — *(locked 2026-06-23)* progress in `LAB_LOG.md`, canonical numbers in `experiments/RUNS.csv` via `save_results`. No A/B letters. This file = decision/notation record.
8. **KD comparison hygiene** — *(revised 2026-07-07, PoC scope)* Full control ladder (`fedavg → fedavg_pub → fedkd_seqkd → fedkd_struct → fedkd`) is deferred until the public corpus is picked (see dec.4). **For now:** the PoC compares, on the identical Spider data slice, from the base model: `poc_ft` (gold CE, no teacher) vs `poc_struct` (QP-CoT⊕SQL from teacher) vs `poc_kid` (RKL on imperfect `ŷ` — blocked on E0.3, see `KD_PLAN.md`). `poc_struct − poc_ft` and `poc_kid − poc_ft` = does KD supervision beat plain FT on the same data, before any public-corpus or federation question is decided. DP claim scoped to "DP-ready + (ε, EX) curve" (K=3 → no strong-ε promise), unaffected by this reopening. Staged run order = `KD_PLAN.md` §PoC.

---

*Grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM, [9] DAIL-SQL, [10] KID, [11] Struct-SQL + the approved outline + Fig. 1. Mechanism source of truth: `fig1_architecture.md`. Full system: `system_architecture.md`.*

> **[10] KID** (Zhong et al. 2024, arXiv:2410.11371) — "Learning from Imperfect Data: Efficient KD for Text-to-SQL". **Source of our KD mechanism** (adopted 2026-06-29): mitigate train/inference mismatch by distilling on imperfect (student-rewritten) data that simulates inference's cascading errors. +5.83% avg across 5 NL2SQL benchmarks, all model sizes. Anchors the **in-context-tuning argument**: ICL's −1..−2 pp on a `train-k=0` FT student is the SAME train/test mismatch KID targets → fix by training in the inference condition (`train-k=3`).

> **[11] Struct-SQL** (arXiv:2512.17053) — "KD with Structured Chain-of-Thought for Text-to-SQL". **Second KD direction** (decided 2026-06-30): teacher prompted with a **Query-Plan CoT (QP-CoT)** template emits an execution-plan-structured reasoning trace (trace schema → pick tables/cols → scan → join → filter → group); student is SFT'd on `(question ⊕ QP-CoT ⊕ gold SQL)`. **Data/sequence-level** (vs KID logit-level) → different axis = honest contender, not ablation. +8.1% over unstructured-CoT distillation. SLMs can't internalize structured reasoning by prompting → KD installs it. **Subsumes our skeleton-structure loss**; teacher runs **offline on the public KD corpus's train split** (traces cached, exec-filtered; no per-step co-load) → T4-friendly + clean in federation. No corpus is locked yet (dec.4 above) — the PoC generates these traces on a Spider slice instead. Composable with KID (QP-CoT as the target KID then makes imperfect). See `system_architecture.md` §5.6.1.
