# FedLS-SQL experiment matrix

This file maps paper questions to the minimum evidence needed for a defensible
claim. `PIPELINE_NEXT.md` contains executable commands;
`paper/results/MAIN_RESULTS.md` contains canonical paper values; and
`RESULT_REGISTRY.md` maps stable IDs to checkpoints and evaluation artifacts.

| Priority | RQ | Comparison/evidence | Status |
|---|---|---|---|
| P0 | RQ1 accuracy | standard continuous centralized 3 epochs and 3-pass-restart vs pure FL vs FedLS-SQL | seed-0 Spider/OOD/BIRD table complete; standard recipe selected |
| P0 | causal attribution | FL, matched BIRD-gold CE, teacher-target CE, full FedLS-SQL | complete at T1 seed 0; teacher guidance survives matched control |
| P0 | second-family portability | Gemma 2 9B generates all BIRD train rows, then uses the canonical selector to obtain `N_gemma`; T1 base vs FL vs same-row gold CE vs target CE vs full CE+RKL | complete: FL 57.16, target CE 61.22, full 61.41 EX; full-vs-FL significant, RKL-vs-target CE not significant |
| P0 | teacher/data audit | Execute all 9,428 BIRD gold SQL independently; compare Qwen/Gemma matches on one valid-gold mask | complete: 9,056 valid; Qwen 42.72%, Gemma 27.46% match yield |
| P0 | method direction | token-matched random hard SeqKD vs global-error selection from the shared T1 FedAvg adapter | P0.9a complete; P0.9b activated, client-disagreement arm cancelled |
| P1 | teacher ceiling | 4-bit Gemma 9B zero-shot on Spider | optional contextual reference; does not decide method |
| P1 | headline reliability | final T3 pure FL vs full FedLS-SQL on Spider at training seeds 0/1/2 | seed 0 complete; seeds 1/2 deferred, not cancelled |
| P1 | RQ3 convergence | Pure FL and FedLS-SQL at T1, T2, T3 | seed 0 complete; replication gated |
| P1 | RQ3 generalization | Spider, Realistic, Syn, DK, and BIRD | seed 0 complete; replication gated |
| P1 | RQ4 communication | adapter parameters/bytes per client, round, and total | payload bytes consolidated; trainable-parameter count and table export pending |
| P1 | RQ4 resources | controlled repeated wall time, process RSS, allocated/reserved VRAM, inference latency | instrumentation ready; official controlled runs pending |
| P2 | additional reliability | matched public-gold seeds 1/2 or extra final seeds only if earlier gates remain uncertain | conditional |
| P1 | non-IID | current domain/quantity-skewed `alpha=0.5`, K=5 split | complete for main setting |
| P2 | optimizer baseline | FedProx SLM | not implemented/run; baseline only, not proposed direction without drift evidence |
| P2 | sensitivity | LoRA rank, teacher/student sizes, public-pool size | partial or not run |
| P2 | Gemma centralized anchor | continuous one-epoch centralized Gemma for T1 private-pass matching; three epochs only if Gemma extends to T3 | conditional after positive endpoint; not activated automatically because RKL increment is weak |
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
6. Do not call the existing chained centralized artifact “standard 3 epochs”;
   label it `Centralized-3pass-restart` and compare it with one continuous
   `epochs=3` run.
7. Shared-server accuracy is valid, but timing is not paper evidence. Official
   resource runs require fresh execution, exclusive hardware, and repetition.
8. Treat EX as primary for the server-stage comparison. The large EX-EM
   divergence requires an explicit equivalent-SQL/error audit; do not describe
   the reverse-KL increment as across-seed significant.

## Recommended execution order

1. Treat the existing Qwen/Gemma ladders as sufficient to retain the framework:
   hard teacher targets are the portable mechanism; RKL remains provisional.
2. Treat P0.9a as complete: global failure state is usable, while client
   disagreement is too broad and has no significant incremental correction
   signal.
3. Run the activated equal-row/update/token P0.9b comparison between random256
   and global-error256 hard SeqKD. Do not add a disagreement arm.
4. Promote the new method only after its preregistered T1 gate; otherwise freeze
   the current framework and stop method search.
5. After method freeze, complete controlled resources, error audit, and final
   T3 seed replication for the selected method.
6. Keep Gemma teacher ceiling and target-form audit as context. Extend the new
   method to Gemma only after a positive Qwen gate.
7. FedProx remains a reviewer baseline. Exact aggregation/FLoRA-NA are closed
   as method directions at the current `K=5, T=1` setting; broader
   heterogeneity is conditional rather than an automatic sweep.
