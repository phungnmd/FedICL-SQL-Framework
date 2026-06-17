# FedICL-SQL — Lab Log

> One entry per working session. Auto-header from `analysis/log_session.py`, manual body.

## Session 2026-06-17

### New runs
| experiment | stage | seed | EX | EM | loss | n | device | run_id |
|---|---|---|---|---|---|---|---|---|
| eval_base_floor | poc | 0 | 0.5116 | 0.1412 | — | 1034 | cuda | `eval_base_floor__s0__20260617T055325` |
| centralized_ft | poc | 0 | 1.0000 | 0.2000 | 0.5295 | 8659 | cuda | `centralized_ft__s0__20260617T055949` |
| centralized_ft | poc | 0 | 0.6170 | 0.4246 | 0.0554 | 8659 | cuda | `centralized_ft__s0__20260617T073618` |

### Recent commits — code (`fedicl-sql/`)
  2192865 refactor(centralized_ft): use centralized/train.csv directly, drop --split-dir
  050bb47 fix(notebook): cell-9 header + cell-18 formatting and completeness check
  09c40b8 fix(notebook): B0 comment — base floor independent of split
  956f65e poc(alpha_0.1/k3): results + teacher-annotated datasets
  c608771 fix(notebook): full review pass — stale text, variable guards, config variable

### Recent commits — paper (`paper/`)
  83713db docs: fix stale refs in detailed_plan + outline
  4a3d0a0 chore: stage cleanup — update CLAUDE.MD, remove stale drafts and old LAB_LOG
  80b8e1d docs: full consistency pass — align todo + detailed_plan to new architecture
  10a9eff docs(method): teacher domain-adaptation + annotated Qi dataset
  a89af8b docs(method): single-pass KD — one sequence per Qᵢ example

### Observations
- B0 (base Qwen2.5-1.5B-Instruct, k=0, no training) = **EX 51.2% EM 14.1%** (1034 ex, CUDA, alpha_0.1/k3)
- B3 (centralized FT, 1 epoch, 8659 ex) = **EX 61.7% EM 42.5%** (1034 ex, CUDA, k=0)
- B3+ICL (k=3, LOO retrieval from test.csv) = **EX 70.6% EM 57.9%**
- Gap B3−B0 = **+10.5% EX** → LoRA fine-tuning
- Gap B3+ICL − B3 = **+8.9% EX** → ICL contribution
- True ceiling for M_G to approach = **70.6%** (B3+ICL)
- `centralized_ft__s0__20260617T055949` is smoke run (EX=1.0 on 5 ex) — ignore
- `_extract_sql()` fix may account for ~5-8% of B0 vs old 40.5% result
- ToChar / DATEDIFF warnings = sqlglot EM scoring issue, does not affect EX

### Decisions
- Confirmed CUDA stack + alpha_0.1/k3 + full 1034 test.csv as the comparison baseline
- All future runs: same stack, no --n-eval limit

### Next
- §3b B3+ICL: eval B3 adapter with k=3 on test.csv (LOO retrieval within test DBs)
- §5a-1 slm_only ×3: per-client solo LoRA, B2 floor (~3-4 hr on T4)
- §5a-2 ab3_fedavg ×3: FedAvg without KD, Ab3 baseline
- §4b gen_teacher_targets ×3: annotate client Qᵢ with 7B teacher (--load-in-4bit)
- §5b-1 m_g ×3: full method (teacher KD FedAvg)

---
