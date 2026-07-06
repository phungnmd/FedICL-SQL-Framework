# FedICL-SQL — Lab Log

> One entry per working session. Auto-header from `analysis/log_session.py`, manual body.
> Compare all runs: `uv run python analysis/compare.py`

---

## Session 2026-06-29 — architecture pivot to KID + lock decisions

### What changed

**Architecture pivot:** KD mechanism replaced with KID (Learning from Imperfect Data, EMNLP Findings 2024). Primary driver: KID teacher runs forward-only per step (not autoregressive offline) → ~100× cheaper than old offline annotation.

**KD mechanism (new):**
- Teacher: Qwen2.5-7B frozen, co-loaded with student, online per training step
- Per step: student masks gold SQL (ratio `ρ`, Hard strategy) → rewrite → `ŷ` → teacher forward with ICL k=3 from `Qᵢ` → soft labels `p` → `L = λ(t)·MLE + (1-λ(t))·RKL(q‖p)`
- Alpha-decay `λ(t)`: 1.0 → 0 over training
- Reverse KL (mode-seeking, SQL-compatible)
- No offline annotation, no exec-filter, no L_struct, no CoT

**ICL:** follows DAIL-SQL [9] — question-similarity retrieval, never_schema demos, k=3 inference, k=0 training.

**Datasets locked:**
- Primary: Spider
- Secondary: BIRD *(locked)*

**Ablations locked:**
- `fedkd_teacher_k3` (default) vs `fedkd_teacher_k0` — value of ICL-enhanced teacher labels
- `fedkd@k3` vs `fedkd` — value of ICL at inference

**VRAM:** teacher (14 GB) + student (3 GB) co-loaded → A100 required. T4 PoC: 4-bit teacher.

### Files updated
- `system_architecture.md` — §5.2, §5.6, §6, §8, §9, §10, arm table, eval datasets
- `DECISIONS.md` — §2 notation, §3 decisions #1, #4, #5, #6
- `fig1_architecture.md` — three-plane, teacher, training loss, caption, innovations, outline mapping

### Next
- Implement KID training loop (`lora_trainer.py`): mask+rewrite pipeline + online teacher forward + RKL + alpha-decay
- Run `local` ×3 + `fedavg` ×3 (gold CE only, no teacher) → establish federation baseline
- Run `fedkd_teacher_k3` ×3 → full method
- Eval all arms on Spider + BIRD

---

## Session 2026-06-23 — naming refactor + retire detailed_plan

### What changed
Killed the A/B/Ab letter labels and the `detailed_plan.md` mega-doc. Arms now
named by **feature**, not letter. No pre-planned full roadmap — work is decided
per session and logged here.

**Naming map (old → new):**

| old | new | what it is |
|---|---|---|
| B0 / `base` | `base` | untrained SLM floor |
| B2 / `slm_only` | `local` | per-client solo LoRA (no fed, no teacher) |
| B3 / `centralized_ft` / `b3_k0` / `b3_k3` | `central` | pool-all centralized ceiling |
| B4 / Centralized-ICL | `central@k3` | central + ICL eval overlay |
| Ab3 / B6 / `ab3_fedavg` | `fedavg` | FedAvg, no teacher KD |
| M_G / `m_g` | `fedkd` | full method (FedAvg + teacher KD) |
| B1 | `teacher` | LLM teacher few-shot ceiling |

ICL = eval overlay (`@k3` suffix), not an arm. `M_G` kept **only** as the Fig.1
math symbol for the global SLM (notation, not an arm label).

**Scope = going-forward only.** Historical `RUNS.csv` rows + Drive result dirs keep
their old slugs; `compare.py` maps both old and new slugs to the same identity so
the scoreboard still renders. New runs emit new names.

### Files touched
- **new** `DECISIONS.md` — slim decision + notation record (migrated `detailed_plan` §0 notation + §8 locked decisions + the naming map). **`detailed_plan.md` deleted.**
- `compare.py` — `IDENTITY`/`LABEL` → feature names, legacy slugs still map; widened columns. Verified renders clean on existing RUNS.csv.
- `eval_arms/run.py`, `centralized_ft/run.py`, `client_train/run.py`, `dataset.py`, `lora_trainer.py`, `pool.py`, `retriever.py`, `icl_diff.py`, `icl_ab_local.py` — docstrings/comments → feature names.
- `notebooks/00_colab_bootstrap.ipynb` — all arm slugs + dir paths renamed (`m_g_round`→`fedkd_round`, etc.); JSON re-validated.
- Root `CLAUDE.MD`, `fedicl-sql/CLAUDE.md`, `README.md`, `system_architecture.md` — repointed `detailed_plan` → `DECISIONS.md`, arm-naming tables + delta language → feature names.

### Next
- Unchanged from below: train `local` ×3 + `fedavg` ×3 → CUDA; gen teacher targets; train `fedkd`; eval all arms (`fedkd − local`, `fedkd − fedavg`).

---

## Session 2026-06-18 — ICL demo-pool leakage fix

### Problem found
`eval_arms` built the ICL retrieval pool from the **test set itself** (`held_out`/`test.csv`), retrieving demos via leave-one-out within the same DB. Spider dev has many near-duplicate questions per DB → LOO handed the model a near-answer template → inflated EX. All prior k=3 ICL runs purged (leaky, non-citable).

### Design (confirmed w/ advisor intent)
Each client = org with own schema + train data `Qᵢ`. ICL demo pool = the model's **own train data**, never the test set. Verified disjointness: train 146 DBs ∩ test 20 DBs = **0**; every `client_i` pool ∩ test = 0. So retrieval is **cross-schema** (train demos → unseen test query) and needs **no LOO**. This *is* the RQ2 mechanism (general SQL-skeleton transfer, not schema-specific answers).

Decision (user): global federated arms (`M_G`, `ab3_fedavg`) evaluated **per client pool → mean±std** over K (privacy end-to-end + free per-client variance). `M_G−B3` gap = federation cost + private-pool restriction.

### Refactor (code)
- **new** `fedicl_sql/retrieval/pool.py` — `client_pools(split_dir, K)` + `centralized_pool(train_csv)`.
- `eval_arms/run.py` — rewritten: drop `_retrieve_loo` + per-DB test index. `--pool-mode per_client` (default) = per-client pools, `{i}` placeholder adapter, mean±std + per-pool breakdown; `--pool-mode centralized` = one centralized pool, single number (B3/B4). Single ICL-eval entrypoint.
- `centralized_ft/run.py` — unchanged (B3 = k=0). B4 Centralized-ICL = `eval_arms --pool-mode centralized --k 3` on the existing B3 adapter (no retrain).
- `notebooks/00_colab_bootstrap.ipynb` — §3b/§5a-3/§5b-2 eval cells updated to the new `--pool-mode`/`--split-dir` interface.
- **tests** +3 (`test_pool.py`): pool wiring + `pool ∩ test = ∅` invariant. **85 passed.**

### New runs (train-pool retriever, no leakage)

| experiment | arm   | k | pool              | EX         | EM     | n_eval | device | run_id                           |
|------------|-------|---|-------------------|------------|--------|--------|--------|----------------------------------|
| eval_arms  | b3_k3 | 3 | centralized train | **52.61%** | 37.14% | 1034   | cuda   | `eval_arms__s0__20260618T123344` |

### Key finding 🔴

B3+ICL k=3 (cross-schema, centralized train pool) = **52.61%** — **−9.1% vs B3 k=0 (61.7%)**. Cross-schema ICL hurts significantly. Prior 70.6% result was from leaky test-pool LOO → now invalidated and purged.

**Scoreboard (clean, train-pool only):**

```
B0  base Qwen-1.5B    k=0   EX=51.2%   EM=14.1%   (no training)
B3  centralized FT    k=0   EX=61.7%   EM=42.5%   (+10.5% from LoRA SFT)
B3  centralized FT    k=3   EX=52.61%  EM=37.14%  (−9.1% from cross-schema ICL 🔴)
```

**Implications for RQ2:** cross-schema ICL with train-pool demos actively hurts the centralized model. Per [4]: masked cross-schema ICL also costs EX. This means if M_G shows the same pattern, the paper's ICL contribution is at risk — title claims "In-Context Learning" but ICL hurts. Must surface at SB gate. Possible reframe: ICL as privacy/transfer lever, not accuracy lever (frame per §2.3 + [4]).

**However:** B3 is centralized and already sees all 8659 train examples (= strong baseline). M_G is federated with per-client ICL from smaller Qᵢ pools. The relative ICL contribution for M_G may differ. Confirm once M_G is trained.

### Next

- Proceed to step 4 (B2 solo LoRA ×3) + Ab3 (FedAvg no-KD) → CUDA.
- After M_G trained: re-run ICL eval with `--pool-mode per_client` to check whether M_G+ICL recovers or also loses vs k=0.
- B0/B3 k=0 numbers (51.2% / 61.7%) unaffected — clean, still valid.

---

## Session 2026-06-17

### New runs
| experiment | k | EX | EM | loss | n_eval | device | run_id |
|---|---|---|---|---|---|---|---|
| eval_base_floor | 0 | **51.2%** | 14.1% | — | 1034 | cuda | `eval_base_floor__s0__20260617T055325` |
| centralized_ft | 0 | **61.7%** | 42.5% | 0.0554 | 1034 | cuda | `centralized_ft__s0__20260617T073618` |

### Scoreboard

```
B0  base Qwen-1.5B    k=0   EX=51.2%   EM=14.1%   (no training)
B3  centralized FT    k=0   EX=61.7%   EM=42.5%   (+10.5% from LoRA SFT)
```

(k=3 ICL numbers pending — see 2026-06-18 demo-pool fix; must re-run with train-pool retriever.)

### Observations
- `_extract_sql()` fix likely accounts for ~5-8% of B0 improvement vs old 40.5% (old code failed when model output reasoning prefix)
- ToChar / DATEDIFF warnings = sqlglot EM scoring, does not affect EX
- Training speed: 0.49s/step on T4 → 8659 steps ≈ 70 min + 22 min eval
- Smoke run detection: `compare.py` now auto-filters n_eval < 50

### Decisions
- CUDA stack, alpha_0.1/k3, full 1034 test.csv = fixed baseline for all future runs
- log_session.py filters n_eval < 50 (smoke runs)

### Next
- [x] §2.5 B0 base floor
- [x] §3 B3 centralized ceiling
- [ ] §5a-1 `slm_only` ×3 — B2 floor, per-client solo LoRA (~72 min total)
- [ ] §5a-2 `ab3_fedavg` ×3 — Ab3, FedAvg no KD (~72 min)
- [ ] §5a-3 eval federation gain + ICL (ab3_fedavg − slm_only)
- [ ] §4b `gen_teacher_targets` ×3 — annotate Qᵢ, 7B 4-bit (~13 hr client_1)
- [ ] §5b-1 `m_g` ×3 — full method teacher-KD FedAvg (~72 min)
- [ ] §5b-2 eval all arms (m_g − slm_only, m_g − ab3_fedavg)

---

---

## 2026-06-30 — RQ2 reframed to Fed+ICL+KD synergy; +ref [10] KID

**Error analysis (k0 vs k3 flips, dail_select):**
- BASE (chưa FT): 49.0%→52.5% (+36 net; gain 137 / hurt 101). GAIN = structure fixes (over-join, alias, ORDER BY LIMIT); HURT = JOIN-heavy.
- CENTRAL (FT): 63.1%→60.2% (−30 net; gain 79 / hurt 109). **54/109 hurts = `no such column` exec errors = schema bleed** (student copies demo's table/col names from a different DB).
- Mechanism: ICL has 2 channels — *structure-transfer* (gain, schema-agnostic) + *schema-bleed* (hurt). FT saturates the gain channel (already knows structure) but not the bleed channel → net negative. = train/test MISMATCH (train k=0, eval k=3), NOT an ICL ceiling.

**Decision — RETIRE "never claim ICL improves FT" framing.** Goal restated: build Fed+ICL+KD → max EX on small model; target `(FT/KD)+ICL > either`. Path = **in-context tuning** (`train-k=3` + `skeleton` demos) so student learns to read demos + anti-bleed prior. Grounded in KID [10] (train/inference mismatch). Updated `system_architecture.md` (top note + §5.3 RQ2 + §5.6 FT stream + ICL-positions table + per-arm table) and `DECISIONS.md` ref list.

**Added reference [10]** = KID (Zhong et al. 2024, arXiv:2410.11371) — source of the adopted KD mechanism. PDF+MD in `paper/references/`.

### Next
- [ ] Verify `--train-k 3` + train-time `demo_style=skeleton` are wired in trainer + eval run.py
- [ ] Run synergy arm: `central` train-k=3 skeleton, eval k=3 skeleton (A100) vs `central` k0 vs `base@k3`. Count bleed-error drop (expect 54→low).
- [ ] If synergy confirmed → promote to RQ2 headline; else report honest k=0.

### 2026-06-30 addendum — 2 KD directions locked + ref [11]
- KD now has **two directions** benchmarked head-to-head (`system_architecture.md` §5.6.1):
  - **Dir A — KID [10]** (logit-level, RKL on imperfect ŷ, A100 co-load) = primary.
  - **Dir B — Struct-SQL [11]** (data/seq-level, SFT on QP-CoT⊕SQL, teacher offline → T4-friendly) = contender/fallback; subsumes skeleton-structure loss; composable with KID.
- Reason for B: not certain KID wins → need a proven NL2SQL-specific method on a different axis. Arms: `fedkd` (KID) / `fedkd_struct` (Struct-SQL) / `fedkd_seqkd` (optional classic).
- Also locked: KD-stream teacher+student now share `P_ICL` context (fixed latent k3-vs-k0 inconsistency); invariant #9 "train condition == inference condition" added.
- Added **reference [11]** = Struct-SQL (arXiv:2512.17053). PDF+MD in `paper/references/`.
- Next: verify QP-CoT fits 1.5B + T4 VRAM; run Dir A vs Dir B vs base@k3 on A100.

- KD impl plan → `paper/notes/KD_PLAN.md` (2 directions × ICL on/off matrix; Phase 0.5 = wire ICL into KD path first).

---

## 2026-07-06 — KD architecture review → 6 fixes locked; KD_PLAN rewritten with staged experiment list

**Review found 4 serious flaws in the KD design docs; all fixed today:**

1. **`kid − struct` was confounded** — KID distilled on BIRD, Struct-SQL traces were to be generated on `Qᵢ` (old offline pipeline) → the comparison differed on loss level AND data AND teacher mode at once. **Fix: both directions now distill on BIRD train** (Struct-SQL traces generated offline on BIRD, cached, exec-filtered).
2. **`fedkd − fedavg` confounded teacher with extra public data** (KD arms see Qᵢ+BIRD, fedavg sees Qᵢ only). **Fix: new `fedavg_bird` control** (CE on BIRD gold, no teacher) → control ladder `fedavg → fedavg_bird → seqkd → struct → kid`, each rung isolates one ingredient. Teacher value = `fedkd − fedavg_bird`. Same control used for exposure-fair BIRD-dev secondary eval.
3. **Demo-style mismatch baked in** — plan had train `skeleton` + eval `never_schema` (same class of train/test mismatch as the −30-flip bug). **Fix: style parity locked** — train style == eval style per arm; default `never_schema` end-to-end; paired `skeleton` = privacy cell (E3.4); style-shift = its own experiment (E3.5). Invariant #9 gains level (c).
4. **Doc self-contradictions** — §2 diagram still showed old offline-teacher-on-Qᵢ + 4-term loss; ablation table said teacher ICL "from Qᵢ" (violated invariant #2); `skeleton` vs `never_schema` inconsistent in pseudocode. All patched to match §5.2/§5.6.

**Also pinned:** FedAvg weighted `nᵢ/n` (McMahan, was 1/K) + LoRA A/B-averaging caveat; λ₂ alpha-decay = GLOBAL over cumulative steps across rounds; privacy reframed (BIRD = update-alignment rationale, not "privacy absolute" — teacher is on-premise); DP claim scoped to "(ε, EX) curve" at K=3, no strong-ε promise; new invariant #10 (KD data = BIRD for all directions + data-matched comparisons).

**KD_PLAN.md rewritten** — full staged experiment list:
- Stage 0 probes: E0.1 BIRD→Spider transfer probe (1k gold SFT, kill-switch before A100 spend) · E0.2 train-k=3 T4 VRAM probe · E0.3 pin KID mask-fill mechanics vs [10] (causal LM has no `[MASK]` — blocks Phase 2).
- Stage 1 direction bake-off on client_1 only (no FedAvg, ⅓ cost): local_1 / local_bird_1 / seqkd / struct±ICL / kid±ICL → gate G1: winner must beat `local_bird_1` else teacher adds nothing → ship `fedavg_bird` as method.
- Stage 2 federate winner: fedavg / fedavg_bird / fedkd(winner) / central.
- Stage 3 headline: 3 seeds + significance · ρ sweep (KID, 1 seed) · teacher-k0 · skeleton privacy cell · style-shift · k-sweep · bleed analysis · BIRD-dev · DP curve.

Updated: `KD_PLAN.md` (rewrite) · `system_architecture.md` (header note, §2 diagram, §3.1, §5.2, §5.3, §5.6, §5.6.1, §6, invariants #2/#9/#10, §10) · `DECISIONS.md` (§1 dec.1/4/6 amended, dec.8 added, λ notation).

### Next
- [ ] Phase 0 scaffold: `--kd-direction` flag, BIRD loader + FAISS pool, weighted-FedAvg fix
- [ ] E0.1 + E0.2 probes (T4) before any A100 booking
- [ ] E0.3: read KID [10] §method, pin mask-fill mechanics (left-to-right teacher-forced? sampling temp? stop-grad through ŷ)

---

## Session 2026-07-07 — BIRD dropped, KD scope cut to a PoC

### What changed

**BIRD dropped entirely** — too heavy (8.9 GB DB download) and too complex
(`evidence`-field dependence, dialect gap vs Spider) to justify as the KD stream, and
dropped as secondary eval benchmark too (no cross-dataset claim for now). **No
replacement public KD corpus is picked** — that decision is deferred, not re-locked
to anything else (not `train_others`, not a new corpus). Spider itself is unchanged
(same train/test split as always).

**Scope cut to a PoC before any further build:** compare, on an identical slice of
Spider data, training it as plain gold-CE FT (`poc_ft`) vs as a KD signal via Struct-SQL
(`poc_struct`) vs via KID (`poc_kid`, still blocked on E0.3's mask-fill mechanics) — all
from the base model, no dual-stream mixing, no federation. Isolates whether the KD
*signal* itself beats plain FT on the same data, independent of which corpus eventually
supplies a public KD stream.

**Code cleanup:**
- Deleted `fedicl_sql/data/bird.py`, `tests/test_bird.py`, `scripts/download_bird.py`,
  `scripts/build_bird_processed.py`.
- Renamed `--bird-train`/`--bird-teacher-targets` → `--kd-train`/`--kd-teacher-targets`
  in `experiments/client_train/run.py`; `train_dual_stream(bird, bird_teacher_targets, ...)`
  → `train_dual_stream(kd_data, kd_teacher_targets, ...)` in `lora_trainer.py`.
- Deleted the 6 KD notebooks (`notebooks/kd/00_bird_data_prep.ipynb` ..
  `04_stage3_headline.ipynb`); replaced with `notebooks/kd/README.md` (CLI-only PoC
  runbook — no notebooks going forward for this workstream).
- Removed the 1.4 GB local `data/raw/bird/` download (gitignored, was never committed).

### Files updated
- `DECISIONS.md` — §3 dec.1, 4, 5, 8 (dataset question reopened; PoC framing)
- `KD_PLAN.md` — full rewrite: `§PoC` (runnable now) + `§Deferred` (old BIRD-era
  4-stage plan, kept for reference, not built against)
- `system_architecture.md` — top note + BIRD→generic "public KD corpus (TBD)"
  throughout §5.2/§5.6/§5.6.1/§6/§8/§9
- `CLAUDE.md`, `README.md` — KD section rewritten for the PoC CLI flow

### Next
- [ ] Run the PoC: carve slice `X`, train `poc_ft` + `poc_struct`, eval on frozen
      Spider test, read off `poc_struct − poc_ft`
- [ ] E0.3: pin KID [10] mask-fill mechanics before attempting `poc_kid`
- [ ] Once the PoC has a verdict, decide the public KD corpus question (or decide to
      skip a public corpus and reuse the private pool for Stream 2)
