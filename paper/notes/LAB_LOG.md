# FedICL-SQL — Lab Log

> One entry per working session. Auto-header from `analysis/log_session.py`, manual body.
> Compare all runs: `uv run python analysis/compare.py`

---

## Session 2026-06-17

### New runs
| experiment | k | EX | EM | loss | n_eval | device | run_id |
|---|---|---|---|---|---|---|---|
| eval_base_floor | 0 | **51.2%** | 14.1% | — | 1034 | cuda | `eval_base_floor__s0__20260617T055325` |
| centralized_ft | 0 | **61.7%** | 42.5% | 0.0554 | 1034 | cuda | `centralized_ft__s0__20260617T073618` |
| eval_arms `b3_k3` | 3 | **70.6%** | 57.9% | — | 1034 | cuda | `eval_arms__s0__20260617T081559` |

*(smoke run centralized_ft n=5 EX=1.0 — ignored)*

### Scoreboard

```
B0  base Qwen-1.5B    k=0   EX=51.2%   EM=14.1%   (no training)
B3  centralized FT    k=0   EX=61.7%   EM=42.5%   (+10.5% from LoRA SFT)
B3  centralized FT    k=3   EX=70.6%   EM=57.9%   (+8.9% from ICL)
```

**Ceiling for M_G = 70.6%** (B3+ICL). Gap from B0: +19.4% EX total.

### Observations
- `_extract_sql()` fix likely accounts for ~5-8% of B0 improvement vs old 40.5% (old code failed when model output reasoning prefix)
- ICL contribution (+8.9%) stronger than expected for k=3 LOO from test.csv itself
- ToChar / DATEDIFF warnings = sqlglot EM scoring, does not affect EX
- Training speed: 0.49s/step on T4 → 8659 steps ≈ 70 min + 22 min eval
- Smoke run detection: `compare.py` now auto-filters n_eval < 50

### Decisions
- CUDA stack, alpha_0.1/k3, full 1034 test.csv = fixed baseline for all future runs
- §3b B3+ICL: only run k=3 (b3_k0 = B3 already known, saved 22 min)
- log_session.py filters n_eval < 50 (smoke runs)

### Next
- [x] §2.5 B0 base floor
- [x] §3 B3 centralized ceiling
- [x] §3b B3+ICL k=3
- [ ] §5a-1 `slm_only` ×3 — B2 floor, per-client solo LoRA (~72 min total)
- [ ] §5a-2 `ab3_fedavg` ×3 — Ab3, FedAvg no KD (~72 min)
- [ ] §5a-3 eval federation gain + ICL (ab3_fedavg − slm_only)
- [ ] §4b `gen_teacher_targets` ×3 — annotate Qᵢ, 7B 4-bit (~13 hr client_1)
- [ ] §5b-1 `m_g` ×3 — full method teacher-KD FedAvg (~72 min)
- [ ] §5b-2 eval all arms (m_g − slm_only, m_g − ab3_fedavg)

### Recent commits — code
```
4abe9e7  feat(compare): show arm EX, filter smoke, add n_eval+k to ledger
e65455e  fix(log_session): filter smoke runs (n<50) from session table
ab8b706  fix: add k=0 field + fix eval_set label in centralized_ft and eval_base_floor
092ca0b  fix(notebook): remove redundant b3_k0 from §3b
df3c6d5  poc(alpha_0.1/k3): B3+ICL b3_k3 EX=70.6%
```

---
