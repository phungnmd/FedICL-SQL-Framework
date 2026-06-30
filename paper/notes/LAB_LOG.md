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
