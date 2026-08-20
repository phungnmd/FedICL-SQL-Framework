# FedLS-SQL experiment matrix

This file maps paper questions to the minimum evidence needed for a defensible
claim. `PIPELINE_NEXT.md` contains executable commands; `RESULT_REGISTRY.md`
contains canonical checkpoints and values.

| Priority | RQ | Comparison/evidence | Status |
|---|---|---|---|
| P0 | RQ1 accuracy | Centralized vs pure FL vs FedLS-SQL at three private-data passes | complete at seed 0 |
| P0 | causal attribution | FL, matched BIRD-gold CE, teacher-target CE, full FedLS-SQL | active; missing gold-CE branch only |
| P1 | RQ3 convergence | Pure FL and FedLS-SQL at T1, T2, T3 | seed 0 complete; replication gated |
| P1 | RQ3 generalization | Spider, Realistic, Syn, DK, and BIRD | seed 0 complete; replication gated |
| P1 | RQ4 communication | adapter parameters/bytes per client, round, and total | pending consolidation after causal gate |
| P1 | RQ4 resources | wall time, peak VRAM, inference latency | partially recorded |
| P2 | reliability | targeted seed 1/2 replication of final headline contrasts | parked until method/claims stabilize |
| P1 | non-IID | current domain/quantity-skewed `alpha=0.5`, K=5 split | complete for main setting |
| P2 | optimizer baseline | FedProx SLM | not implemented/run |
| P2 | sensitivity | LoRA rank, teacher/student sizes, public-pool size | partial or not run |
| P2 | broader skew | IID, quantity, domain, and SQL-pattern controlled suite | not complete |
| P2 | pragmatic RQ2 | matched 1.5B/7B resource benchmark; no full 7B FL by default | wording fixed; evidence pending |

## Claim gates

1. Do not call a `fedkd` round-2/3 pre-server adapter “pure FL”; it inherits
   earlier KD.
2. Do not claim formal privacy guarantees without DP/secure aggregation.
3. Do not claim structural distillation; the implemented objectives are
   teacher-target CE and reverse KL.
4. Scope RQ2 to avoided client/deployment use of the 7B teacher. Do not claim
   empirical superiority to full federated 7B training, which is not run.
5. ICL and FLoRA-NA are negative/closed branches, not FedLS-SQL components.

## Recommended execution order

1. Run the missing matched public-gold CE branch at T1, seed 0, then evaluate
   the four-arm supervision ladder on identical Spider rows.
2. Stop and decide whether the teacher-target and/or reverse-KL contribution
   survives the matched public-gold control.
3. If it survives, consolidate communication/resource evidence and run only
   the missing matched resource benchmarks.
4. Activate FedProx, heterogeneity, or targeted seed replication only when the
   preceding gate identifies it as necessary.
