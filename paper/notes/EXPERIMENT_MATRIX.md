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
| P0 | method direction | token-matched random hard SeqKD vs global-error selection from the shared T1 FedAvg adapter | complete negative: global-error256 is 2.03 EX below random256 and adds 18 execution errors |
| P0 | method-signal triage | client execution-result plurality, Spider prefix cascade, and execution-verified preference inventory from existing predictions | complete diagnostic: all gates pass; plurality proxy is strongest (`+10.55` public EX), but no training gain is established |
| P0 | next KD/Federated direction | hard-LLM-target CE vs the same CE + sparse client-ensemble FKL from a shared FedAvg initialization | closed negative: full-pool FedDF is 1.17 EX below hard-target CE and adds 30 execution errors |
| P1 | teacher ceiling | 4-bit Gemma 9B zero-shot on Spider | optional contextual reference; does not decide method |
| P1 | headline reliability | final T3 pure FL vs full FedLS-SQL on Spider across training seeds | seeds 0/1 complete and positive (`+5.23`, `+3.77` EX); sufficient for the current direction decision, seed 2 deferred for final reporting |
| P1 | RQ3 convergence | Pure FL and FedLS-SQL at T1, T2, T3 | seed 0 complete; seed-1 missing-cell eval active, no training required |
| P1 | RQ3 generalization | Spider, Realistic, Syn, DK, and BIRD | seed 0 complete; replication gated |
| P1 | RQ4 communication | adapter parameters/bytes per client, round, and total | CPU-only manifest implementation complete at `62cd3f6`; production artifact pending P1.4a command |
| P1 | RQ4 resources | repeated wall time, process RSS, allocated/reserved VRAM, inference latency | protocol ready at `487b3b2`; P1.1b-v2 deferred by operator, not cancelled |
| P1 | EX-oriented mechanism/error audit | paired T3 FL/FedLS transitions, hardness, SQL constructs, execution errors, deterministic examples | complete at `4527a76`: 121 corrections/67 regressions; errors 193→101; set operations are the main negative stratum |
| P1 | novelty positioning | nearest-work matrix across FedMKT, FedCoLLM, FedCoT, LaDa, federated KD/PEFT, and NL-to-SQL transfer | mandatory P1.4b; broad “first federated LLM-SLM framework” claim is prohibited |
| P2 | additional reliability | matched public-gold seeds 1/2 or extra final seeds only if earlier gates remain uncertain | conditional |
| P1 | non-IID | current domain/quantity-skewed `alpha=0.5`, K=5 split | complete for main setting |
| P1 | optimizer baseline | matched FedProx-LoRA | recommended reviewer baseline before submission; design/coefficient gate pending, not a proposed contribution |
| P2 | sensitivity | LoRA rank, teacher/student sizes, public-pool size | partial or not run |
| P2 | Gemma centralized anchor | continuous one-epoch centralized Gemma for T1 private-pass matching; three epochs only if Gemma extends to T3 | conditional after positive endpoint; not activated automatically because RKL increment is weak |
| P2 | broader skew | IID, quantity, domain, and SQL-pattern controlled suite | not complete |
| P1 | pragmatic RQ4 | matched 1.5B/7B deployment-resource benchmark; no full 7B FL by default | protocol ready; measure or narrow the claim before freeze |

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
7. Shared-server accuracy is valid, but opportunistic timing is not paper
   evidence. Resource runs require fresh execution, fixed warm-up, at least
   five independent repetitions, and descriptive GPU telemetry. PID presence
   is not used as a contention proxy; exclusivity is not claimed.
8. Treat EX as primary for the server-stage comparison. Audit `EX=1, EM=0` as
   cross-dataset SQL-form variation and an EX-validity check, not as a defect to
   optimize away; do not describe the reverse-KL increment as across-seed
   significant.

## Recommended execution order

1. Treat the existing Qwen/Gemma ladders as sufficient to retain the framework:
   hard teacher targets are the portable mechanism; RKL remains provisional.
2. Treat P0.9a as complete: global failure state is usable, while client
   disagreement is too broad and has no significant incremental correction
   signal.
3. Treat P0.9b as a closed negative branch: global-error256 loses to random256
   on EX, EM, and execution validity. Do not tune the selector or add KL to it.
4. Close P0.10 despite its positive 512-row screen. At 3,873 rows, FedDF loses
   1.17 EX to hard-target CE, adds 30 execution errors, and trails RKL by 3.20
   EX. Do not tune or run the conditional client-only ablation.
5. Freeze the existing method: execution-verified hard targets are the portable
   core and RKL remains an auxiliary Qwen endpoint rather than a stable new KD
   contribution.
6. Complete the four missing seed-1 trajectory evaluations and P1.4a before
   more training.
7. Complete the mandatory novelty matrix and method draft, then decide RQ4
   measurement versus narrowing and fixed-partition scope versus one validated
   heterogeneity sensitivity.
8. Prefer one matched FedProx-LoRA reviewer baseline before returning to
   seed-2 T2/T3. Keep teacher ceilings and all model/rank/client sweeps optional.
