# FedLS-SQL experiment matrix

This file maps paper questions to the minimum evidence needed for a defensible
claim. `PIPELINE_NEXT.md` contains executable commands; `RESULT_REGISTRY.md`
contains canonical checkpoints and values.

| Priority | RQ | Comparison/evidence | Status |
|---|---|---|---|
| P0 | RQ1 accuracy | Centralized vs pure FL vs FedLS-SQL at three private-data passes | complete at seed 0 |
| P0 | RQ3 convergence | Pure FL and FedLS-SQL at T1, T2, T3 | seed 0 complete; seeds 1–2 next |
| P0 | RQ3 generalization | Spider, Realistic, Syn, DK, and BIRD | seed 0 complete; T3 seeds 1–2 queued |
| P0 | RQ4 communication | adapter parameters/bytes per client, round, and total | pending consolidation |
| P0 | RQ4 resources | wall time, peak VRAM, inference latency | partially recorded |
| P0 | reliability | repeat multi-round trajectories for seeds 1 and 2 | queued evidence-first |
| P1 | component value | FL, public CE, distillation-only, full method | substantially complete at T1 |
| P1 | non-IID | current domain/quantity-skewed `alpha=0.5`, K=5 split | complete for main setting |
| P2 | optimizer baseline | FedProx SLM | not implemented/run |
| P2 | sensitivity | LoRA rank, teacher/student sizes, public-pool size | partial or not run |
| P2 | broader skew | IID, quantity, domain, and SQL-pattern controlled suite | not complete |
| P2 | RQ2 large-FL comparison | actual federated 7B+ model or carefully scoped resource estimate | unresolved |

## Claim gates

1. Do not call a `fedkd` round-2/3 pre-server adapter “pure FL”; it inherits
   earlier KD.
2. Do not claim formal privacy guarantees without DP/secure aggregation.
3. Do not claim structural distillation; the implemented objectives are
   teacher-target CE and reverse KL.
4. Do not claim lower cost than large-model FL as an empirical result until an
   executable baseline or an explicitly labeled analytical comparison exists.
5. ICL and FLoRA-NA are negative/closed branches, not FedLS-SQL components.

## Recommended execution order

1. Run and evaluate pure FL and FedLS-SQL T1–T3 for seed 1, then seed 2.
2. Review the three-seed Spider trajectories; if the claim survives, evaluate
   T3 on Realistic, Syn, DK, and BIRD for seeds 1–2.
3. Consolidate communication and resource measurements from existing
   configs/logs; no accuracy rerun is required.
4. Decide with the advisor which P2 experiments are necessary before spending
   compute on model-size or skew sweeps.
