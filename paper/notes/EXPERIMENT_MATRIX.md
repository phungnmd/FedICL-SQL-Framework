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
| P1 | RQ3 convergence | Pure FL and FedLS-SQL at T1, T2, T3 | complete at seeds 0/1; seed-1 FedLS T1→T3 `+3.29` EX (`p=0.00266`), pure FL plateaus T2→T3 |
| P1 | RQ3 generalization | Spider, Realistic, Syn, DK, and BIRD | seed 0 complete; replication gated |
| P1 | RQ4 communication | adapter parameters/bytes per client, round, and total | complete at nested result commit `147f455`: 18,464,768 FP32 LoRA parameters; 738,590,720 logical tensor bytes/round; 2,215,772,160 through T3 |
| P1 | RQ4 resources | repeated wall time, process RSS, allocated/reserved VRAM, inference latency | protocol ready at `487b3b2`; P1.1b-v2 reactivated as next GPU task on 2026-08-27 |
| P1 | EX-oriented mechanism/error audit | paired T3 FL/FedLS transitions, hardness, SQL constructs, execution errors, deterministic examples | complete at `4527a76`: 121 corrections/67 regressions; errors 193→101; set operations are the main negative stratum |
| P1 | novelty positioning | nearest-work matrix across FedMKT, FedCoLLM, FedCoT, LaDa, federated KD/PEFT, and NL-to-SQL transfer | complete in `RELATED_WORK_NOVELTY_MATRIX.md`; title narrowed; FedCoLLM and Struct-SQL are the closest priors |
| P2 | additional reliability | matched public-gold seeds 1/2 or extra final seeds only if earlier gates remain uncertain | conditional |
| P1 | non-IID | current domain/quantity-skewed `alpha=0.5`, K=5 split | complete for main setting |
| P1 | optimizer baseline | matched FedProx-LoRA | next experiment design after P1.1b; implementation and coefficient rule must be frozen before a command |
| P1/P2 | method innovation | new KD/Federated mechanism against the fixed canonical control | open P1.7 lane; requires documented failure/novelty hypothesis, materially new mechanism, matched budget/control, staged promotion, and full-scale confirmation |
| P2 | sensitivity | LoRA rank, teacher/student sizes, public-pool size | partial or not run |
| P2 | Gemma centralized anchor | continuous one-epoch centralized Gemma for T1 private-pass matching; three epochs only if Gemma extends to T3 | conditional after positive endpoint; not activated automatically because RKL increment is weak |
| P1 | stronger-skew sensitivity | exactly one audited split with fixed source rows and `K=5`; FL vs FedLS T1 screen before any T3 extension | selected advisor-aligned RQ3 path; design/audit pending, not a broad skew suite |
| P1 | pragmatic RQ4 | matched 1.5B/7B deployment-resource benchmark; no full 7B FL by default | protocol ready; measure or narrow the claim before freeze |
| P2 | federated-7B claim | at most one matched T1 QLoRA feasibility/reference | conditional after P1.1b; required only for an empirical large-model-FL claim |

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
5. Protect the existing method as the canonical baseline: execution-verified
   hard targets are the portable core and RKL remains an auxiliary Qwen
   endpoint. This does not prohibit a materially new P1.7 proposal.
6. P1.4a and the four seed-1 trajectory evaluations are complete; their
   communication and convergence artifacts are registered.
7. P1.4b is complete. Draft the method and architecture figure from
   `MANUSCRIPT_SKELETON.md` while running P1.1b-v2 as the next GPU task.
8. Then design/run one matched FedProx-LoRA baseline, audit and screen one
   stronger-skew split at T1, and close seed-2 T3. Decide federated-7B
   feasibility only if retaining the corresponding empirical claim. Keep
   teacher ceilings and all model/rank/client sweeps optional.
9. Treat that order as the default rather than a ban on method research. A
   P1.7 KD/Federated proposal may move earlier if it targets a documented gap,
   is materially different from P0.9/P0.10, and has a cheaper falsifiable gate
   plus a credible paper contribution.
