# FedLS-SQL experiment matrix

This file maps paper questions to the minimum evidence needed for a defensible
claim. `PIPELINE_NEXT.md` contains executable commands; `RESULT_REGISTRY.md`
contains canonical checkpoints and values.

| Priority | RQ | Comparison/evidence | Status |
|---|---|---|---|
| P0 | RQ1 accuracy | standard continuous centralized 3 epochs and 3-pass-restart vs pure FL vs FedLS-SQL | Spider complete at seed 0; standard recipe selected; standard OOD/BIRD eval queued |
| P0 | causal attribution | FL, matched BIRD-gold CE, teacher-target CE, full FedLS-SQL | complete at T1 seed 0; teacher guidance survives matched control |
| P0 | headline reliability | final T3 pure FL vs full FedLS-SQL on Spider at training seeds 0/1/2 | seed 0 complete; seeds 1/2 next after centralized OOD fill |
| P1 | cross-family portability | Gemma 2 2B T1 pure FL vs teacher-target sequence KD | gated by headline reliability; one seed/round first |
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

1. Evaluate `Centralized-standard-3ep` on Realistic, Syn, DK, and BIRD so the
   primary comparison uses one centralized recipe in every column.
2. Replicate only final T3 pure FL versus full FedLS-SQL on Spider at training
   seeds 1/2; stop and review stability.
3. If stable, run one T1 seed-0 cross-family screen with Gemma 2 2B: pure FL
   versus teacher-target sequence KD, without Qwen logits.
4. Add fixed in-process warm-up to the resource benchmark path, then run only
   the missing matched 1.5B/7B measurements on an exclusive GPU.
5. Audit the matched T1 predictions, especially execution errors and
   `EX=1, EM=0` cases; replicate public-gold seeds 1/2 only if needed for the
   headline causal claim.
6. Activate FedProx or heterogeneity only when the
   preceding gate identifies it as necessary.
