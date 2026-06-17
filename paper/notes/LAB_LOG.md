# FedICL-SQL — Lab Log

> One entry per working session. Auto-header from `analysis/log_session.py`, manual body.
> Compare all runs: `uv run python analysis/compare.py`

---

## Session 2026-06-18 — ICL demo-pool leakage fix

### Problem found
`eval_arms` + `eval_icl_floor` built the ICL retrieval pool from the **test set itself** (`held_out`/`test.csv`), retrieving demos via leave-one-out within the same DB. Spider dev has many near-duplicate questions per DB → LOO handed the model a near-answer template → inflated EX. All prior k=3 ICL runs purged (leaky, non-citable).

### Design (confirmed w/ advisor intent)
Each client = org with own schema + train data `Qᵢ`. ICL demo pool = the model's **own train data**, never the test set. Verified disjointness: train 146 DBs ∩ test 20 DBs = **0**; every `client_i` pool ∩ test = 0. So retrieval is **cross-schema** (train demos → unseen test query) and needs **no LOO**. This *is* the RQ2 mechanism (general SQL-skeleton transfer, not schema-specific answers).

Decision (user): global federated arms (`M_G`, `ab3_fedavg`) evaluated **per client pool → mean±std** over K (privacy end-to-end + free per-client variance). `M_G−B3` gap = federation cost + private-pool restriction.

### Refactor (code)
- **new** `fedicl_sql/retrieval/pool.py` — `client_pools(split_dir, K)` + `centralized_pool(train_csv)`.
- `eval_arms/run.py` — rewritten: drop `_retrieve_loo` + per-DB test index. `--pool-mode per_client` (default) = per-client pools, `{i}` placeholder adapter, mean±std + per-pool breakdown; `--pool-mode centralized` = one centralized pool, single number (B3/B4). Single ICL-eval entrypoint.
- `eval_icl_floor/run.py` — pool = centralized train, no LOO, single index.
- `centralized_ft/run.py` — unchanged (B3 = k=0). B4 Centralized-ICL = `eval_arms --pool-mode centralized --k 3` on the existing B3 adapter (no retrain).
- `notebooks/00_colab_bootstrap.ipynb` — §3b/§5a-3/§5b-2 eval cells updated to the new `--pool-mode`/`--split-dir` interface.
- **tests** +3 (`test_pool.py`): pool wiring + `pool ∩ test = ∅` invariant. **85 passed.**

### Next
- Re-run ICL numbers with the train-pool retriever (B3+ICL, then the 3-arm `m_g`/`slm_only`/`ab3` once trained).
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
