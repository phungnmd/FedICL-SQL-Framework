# FedLS-SQL experiment matrix

This file maps paper questions to the minimum evidence needed for a defensible
claim. `PIPELINE_NEXT.md` contains executable commands;
`paper/results/MAIN_RESULTS.md` contains canonical paper values; and
`RESULT_REGISTRY.md` maps stable IDs to checkpoints and evaluation artifacts.

| Priority | RQ | Comparison/evidence | Status |
|---|---|---|---|
| P0 | RQ1 accuracy | standard continuous centralized 3 epochs and 3-pass-restart vs pure FL vs FedLS-SQL | seed-0 Spider/OOD/BIRD table complete; standard recipe selected |
| P0 | causal attribution | FL, matched BIRD-gold CE, teacher-target CE, full FedLS-SQL | complete at T1 seed 0; teacher guidance survives matched control |
| P0 | second-family portability | Gemma 2 9B generates all BIRD train rows, then uses the canonical selector to obtain `N_gemma`; T1 base vs FL vs same-row gold CE vs target CE vs full CE+RKL | active; `N_gemma=2,487`, training ladder pending |
| P0 | teacher/data audit | Execute all 9,428 BIRD gold SQL independently; compare Qwen/Gemma matches on one valid-gold mask | queued as P0.7q |
| P1 | teacher ceiling | 4-bit Gemma 9B zero-shot on Spider | queued after Gemma five-arm ladder |
| P1 | headline reliability | final T3 pure FL vs full FedLS-SQL on Spider at training seeds 0/1/2 | seed 0 complete; seeds 1/2 deferred, not cancelled |
| P1 | RQ3 convergence | Pure FL and FedLS-SQL at T1, T2, T3 | seed 0 complete; replication gated |
| P1 | RQ3 generalization | Spider, Realistic, Syn, DK, and BIRD | seed 0 complete; replication gated |
| P1 | RQ4 communication | adapter parameters/bytes per client, round, and total | payload bytes consolidated; trainable-parameter count and table export pending |
| P1 | RQ4 resources | controlled repeated wall time, process RSS, allocated/reserved VRAM, inference latency | instrumentation ready; official controlled runs pending |
| P2 | additional reliability | matched public-gold seeds 1/2 or extra final seeds only if earlier gates remain uncertain | conditional |
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
6. Do not call the existing chained centralized artifact “standard 3 epochs”;
   label it `Centralized-3pass-restart` and compare it with one continuous
   `epochs=3` run.
7. Shared-server accuracy is valid, but timing is not paper evidence. Official
   resource runs require fresh execution, exclusive hardware, and repetition.
8. Treat EX as primary for the server-stage comparison. The large EX-EM
   divergence requires an explicit equivalent-SQL/error audit; do not describe
   the reverse-KL increment as across-seed significant.

## Recommended execution order

1. Gemma 2B client/LoRA compatibility smoke is complete.
2. The Gemma 9B target/logit smoke and full 9,428-row generation are complete;
   deterministic empty generations remain recorded teacher failures.
3. Run the teacher-independent full BIRD gold audit and common-mask comparison.
4. Run pure FL sequentially because the current host cannot safely co-load
   Gemma 9B/2B.
5. Build gold on Gemma's selected indices, then run gold CE, target CE, and full online CE+RKL,
   followed by the five-arm T1 ladder: untouched base, FL, public-gold CE,
   Gemma-target CE, and full CE+RKL.
   Build a full cache only if T3 reuse is justified.
6. Review portability, then optionally evaluate the 4-bit Gemma 9B teacher on
   Spider before any Gemma T3/OOD or model-size expansion.
7. Add fixed in-process warm-up to the resource benchmark path, then run only
   the missing matched 1.5B/7B measurements on an exclusive GPU.
8. Audit the matched T1 predictions, especially execution errors and
   `EX=1, EM=0` cases; replicate public-gold seeds 1/2 only if needed for the
   headline causal claim.
9. Reactivate final T3 seeds, FedProx, or heterogeneity only when the
   preceding gate identifies it as necessary.
