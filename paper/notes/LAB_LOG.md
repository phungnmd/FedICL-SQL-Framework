# FedLS-SQL — active lab log

> Refreshed 2026-08-27. This is the compact decision ledger for the current
> paper. The complete chronology through this date is preserved at
> `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`.

This file records protocol, interpretation, claim limits, open work, and
decisions. It deliberately does not own result tables:

- paper-facing values: `paper/results/MAIN_RESULTS.md`;
- stable checkpoints/evaluation IDs: `RESULT_REGISTRY.md`;
- executable commands: `PIPELINE_NEXT.md`;
- method definition: `system_architecture.md`.

## 1. Current status

- Paper: **FedLS-SQL: Execution-Verified Large-to-Small Knowledge Transfer for
  Federated NL-to-SQL**. P1.4b removed the generic “A Novel ... Framework”
  claim after comparison with FedCoLLM and Struct-SQL.
- Active manuscript structure: `PAPER_OUTLINE_TARGET.md`; the August 19 PDF is
  retained as the advisor-provided planning source rather than a fixed
  experiment contract.
- Primary track: Qwen2.5-1.5B-Instruct student and frozen
  Qwen2.5-Coder-7B-Instruct teacher.
- Method: private client LoRA fine-tuning, sample-weighted factor-wise FedAvg,
  then server-side teacher-target CE plus reverse KL on public data.
- Primary Qwen public pool: 3,873 BIRD teacher-generated EX-match rows; this is
  `N_qwen`, not a fixed cross-teacher budget.
- Canonical inference: greedy, zero-shot, `k=0`.
- Best current endpoint: `69.54` Spider EX at T3, training seed 0.
- The matched public-supervision, centralized-recipe, and centralized OOD/BIRD
  gates are complete.
- P1.1a's active protocol is implemented at nested commit `487b3b2`: fixed in-process warm-up,
  synchronized steady-state generation, process RSS/PyTorch VRAM, atomic
  independent fresh repetitions, descriptive device telemetry without PID
  enumeration, guarded aggregation, and cross-model comparison are tested.
- P1.2 is complete at artifact commit `4527a76`. On 1,034 paired T3 Spider
  rows, FedLS corrects 121 FL failures and regresses 67 (`p=0.0001002`) while
  reducing execution errors from 193 to 101. Medium, aggregation, GROUP BY,
  JOIN, ORDER BY, and LIMIT improve; set operations regress by 18.75 points and
  are the clearest method limitation.
- P0.7a-c/e technical prerequisites passed through selection. Gemma generated
  9,428 outcomes (9,427 non-empty), 7,162 passed quick execution, and
  `N_gemma=2,487` matched BIRD gold. The official stage also recorded 4,443
  mismatches, 231 gold failures, and one prediction failure.
- P0.7q audited all 9,428 gold SQL independently: 9,056 (`96.05%`) execute,
  while 350 have missing-table/column failures, 21 time out, and one hits a
  disk-full error. `retail_world` contributes 330/372 failures. This establishes
  a local CSV/SQLite compatibility issue but cannot assign it to upstream BIRD
  without a clean official-package schema/hash comparison.
- On the 9,056 common valid-gold rows, Qwen matches 3,869 (`42.72%`) and Gemma
  matches 2,487 (`27.46%`); 2,019 are common. The earlier 231 Gemma gold
  failures split into 198 audit-invalid and 33 audit-valid-at-rerun rows. All
  2,487 Gemma-selected training rows are audit-valid.
- P0.7d is complete on 1,034 paired Spider rows. Gemma base, FL, matched-gold
  CE, teacher-target CE, and full FedLS reach respectively `52.22`, `57.16`,
  `41.68`, `61.22`, and `61.41` EX. Full FedLS beats FL by `+4.25` (132/88,
  `p=0.00365`), establishing a positive second-family endpoint.
- Teacher-target CE alone beats FL by `+4.06` EX (137/95, `p=0.00698`) and has
  the lowest execution-error count (119). Full CE+RKL adds only `+0.19` EX
  over it (46/44, `p=0.916`) and has 137 errors, so the stable cross-family
  mechanism is hard teacher-target transfer; an independent RKL portability
  claim is unsupported.
- Matched BIRD-gold CE falls to `41.68` EX with 303 execution errors although
  it uses the same 2,487 source identities. Selection count is therefore not
  the explanation; target form/style and cross-corpus supervision mismatch
  remain an explicit audit question.
- All five P0.7d evaluations are fresh and complete. Full FedLS server training
  resumed from step 1,872 and its saved timing covers only the final 615
  examples (`paper_timing_eligible=false`); no P0.7d training time is official
  resource evidence.
- The FL eval config uses the pre-`--model-4bit` runner schema although its
  metrics report SHA `e144d8b`, indicating a mid-run worktree update. Accuracy
  remains comparable because both effective paths are unquantized defaults;
  exact process provenance is limited to the saved config for this artifact.
- P0.8a is complete. At T3 seed 1, pure FL reaches `61.99` Spider EX with 213
  execution errors and FedLS-SQL reaches `65.76` with 126 (`+3.77` EX;
  111/72 paired gains/losses; exact McNemar `p=0.00483`). The paired bootstrap
  95% interval is approximately `[+1.26,+6.38]`, and every hardness stratum is
  positive. Across seeds 0/1 the mean delta is `+4.50` EX with sample SD
  `1.03`. This is sufficient for the current direction decision. P0.8a-E is
  also complete at result commit `dbd703b`: seed-1 FedLS progresses
  `62.48→64.22→65.76` EX from T1 to T3, while pure FL progresses
  `57.45→61.70→61.99`. The FedLS T1→T3 gain is `+3.29` (78/44,
  `p=0.00266`), while pure FL plateaus from T2 to T3 (`+0.29`, `p=0.810`).
  The mixed-lineage pre-server advantage over pure FL reaches `+2.71` at T3
  (`p=0.0193`), showing retained earlier server knowledge. Incremental T2/T3
  server EX gains are positive but not separately significant; their execution
  errors fall 195→121 and 156→126. P0.8b seed 2 remains deferred.
- The 2026-08-24 method review concludes that existing evidence is sufficient
  for a defensible FedLS-SQL framework paper, but not for a new RKL objective
  claim. P0.9a retained global public error state as a candidate feature, but
  P0.9b showed that training on that signal is worse than a matched random
  subset. Uniform hard SeqKD remains the fallback. P0.10d's positive 512-row
  FedDF screen does not survive P0.10e: at 3,873 rows it loses 1.17 EX and adds
  30 execution errors versus hard-target CE, and trails RKL by 3.20 EX. P0.10
  is closed and archived without tuning; the canonical method is frozen.
- ICL is a closed negative ablation; FLoRA-NA is a closed aggregation branch.
- Internal names such as `fedicl_sql`, `fedkd`, and `noicl` remain immutable
  provenance identifiers.

## 2. Canonical protocol

| Item | Setting |
|---|---|
| Clients | `K=5` |
| Partition | Spider grouped-domain non-IID, Dirichlet `alpha=0.5`, fixed split |
| Primary student | `Qwen/Qwen2.5-1.5B-Instruct` + LoRA |
| Client objective | private gold-SQL CE |
| Local work | one epoch per round unless explicitly labeled otherwise |
| Aggregation | sample-weighted factor-wise FedAvg |
| Teacher | frozen `Qwen/Qwen2.5-Coder-7B-Instruct` |
| Server objective | teacher-target CE + reverse KL |
| Public data | Qwen-specific `N_qwen=3,873` BIRD teacher-generated EX-match rows |
| Primary evaluation | Spider dev, 1,034 rows |
| Robustness | Spider-Realistic, Spider-Syn, Spider-DK |
| Cross-corpus diagnostic | BIRD dev, 1,534 rows |
| Decoding | greedy, no ICL |

Canonical full-method lineage:

```text
private client CE -> weighted FedAvg -> public teacher CE + reverse KL
```

Canonical pure-FL lineage:

```text
base -> FedAvg T1 -> FedAvg T2 -> FedAvg T3
```

The T2/T3 `fedavg_adapter` objects inside a `fedkd` lineage inherit earlier
post-KD adapters and are not pure FL.

### Privacy boundary

- Raw client rows, schemas, questions, and SQL do not leave clients.
- The teacher sees only the public pool.
- Only LoRA adapter parameters cross the network.
- This is structural data isolation, not differential privacy, secure
  aggregation, or a formal defense against update inference.

## 3. Evidence interpretation

All canonical tables and pending cells are in
`paper/results/MAIN_RESULTS.md`. The points below record only what those tables
currently justify.

### 3.1 Headline accuracy

- At T3 seed 0, FedLS-SQL exceeds independent pure FL by `+5.23` Spider EX
  (`p=0.0001`) and has positive deltas on Realistic, Syn, DK, and BIRD.
- The Realistic difference is not significant (`p=0.095`); Spider, Syn, DK,
  and BIRD paired differences are significant.
- FedLS-SQL is `+2.22` Spider EX above centralized-standard, but the difference
  is not significant (`p=0.0865`) and compute is not matched. Do not claim
  superiority to centralized training.
- Multi-round FedLS-SQL improves from T1 to T3 on Spider and all three Spider
  perturbation sets at seed 0. The final T3 gain replicates at seed 1
  (`+3.77` EX); seed 2 remains the final reliability cell.
- The official centralized recipe is one continuous three-epoch run at `67.31`
  Spider EX. The historical three-pass restart reaches `67.60`; their `0.29`
  difference is null (`p=0.863`) and remains schedule sensitivity only.
- Centralized-standard reaches `55.91`, `54.06`, `53.27`, and `13.04` EX on
  Realistic, Syn, DK, and BIRD. FedLS-SQL is respectively `+3.74`, `+1.45`,
  `-0.56`, and `+8.54` points relative to it; only the BIRD contrast is
  significant. Do not claim uniform OOD superiority over centralized training.

### 3.2 Mechanism evidence

- In the matched T1 ladder, public-gold CE is neutral relative to FL
  (`+0.48 EX`, `p=0.800`).
- Teacher-target CE beats matched public-gold CE by `+3.48 EX` (`p=0.0026`).
- Full FedLS-SQL beats public-gold CE by `+5.51 EX` (`p<1e-6`). Extra public
  supervision alone therefore does not explain the seed-0 server gain.
- Across three T1 training seeds, the whole server stage improves over FedAvg
  by `+4.55 ± 1.75 EX` (`p=0.046`).
- Reverse KL adds a positive increment, but its three-seed contrast is
  `+1.71 ± 1.38 EX` with `p=0.165`. Treat RKL as provisional rather than an
  independently established contribution.
- Server refinement lowers execution failures but creates many more
  `EX=1, EM=0` cases. This is consistent with BIRD-to-Spider SQL-form
  variation and is not a defect to optimize away. Audit representative cases
  only to verify EX validity and explain the metric gap; report EM
  transparently as a secondary syntactic metric.

### 3.3 Efficiency evidence

- The Qwen LoRA adapter has `18,464,768` FP32 parameters across 392 tensors,
  or `73,859,072` logical tensor bytes.
- Five uploads plus five broadcasts total `738,590,720` logical tensor bytes
  per round and `2,215,772,160` bytes (`2.064 GiB`) through T3.
- Pure FL and FedLS-SQL have the same client-network payload because teacher
  transfer is server-local.
- The artifact audit also retains serialized-file accounting, but the paper
  excludes safetensors headers, transport framing, and protocol metadata.
- Shared-server timing and RAM are operational logs only. Official latency,
  VRAM, RSS, and throughput remain pending a fixed-warm-up repeated
  shared-server benchmark; the trainable-parameter cell is closed.

### 3.4 Generalization, portability, and negative evidence

- BIRD is a cross-corpus diagnostic whose evaluation databases are disjoint
  from the public pool; it favors the BIRD-trained KD branch and is not a
  headline benchmark.
- The completed centralized transfer suite makes the seed-0 final table whole:
  FedLS-SQL is competitive with centralized training across the retained
  Spider variants, while its decisive advantage remains over pure FL.
- Current primary evidence uses one Qwen student/teacher family. The planned
  Gemma T1 gate tests same-family teacher-target CE and reverse KL after exact
  Gemma 9B/2B token-ID validation; it does not test cross-tokenizer KL.
- ICL reduced accuracy and increased client training time in the matched tested
  setting. Canonical FedLS-SQL therefore uses `train_k=0`, `k_teacher=0`, and
  `eval_k=0`.
- FLoRA-NA did not improve the retained comparisons and is not a contribution.

## 4. Claims and limits

### Supported

1. FedLS-SQL improves over independent pure FL at T3 seed 0 on Spider and has
   positive deltas on all retained transfer/robustness evaluations.
2. The T1 server stage as a whole has positive three-seed evidence.
3. Teacher-generated hard targets outperform matched equal-row BIRD-gold CE at
   T1 seed 0.
4. The deployed 1.5B model requires neither the 7B teacher nor public data at
   client inference time.
5. Client-network communication consists of LoRA adapter payloads and is the
   same for pure FL and FedLS-SQL under the implemented protocol.
6. ICL and FLoRA-NA do not improve the retained configuration.
7. At seed 0, full Gemma FedLS improves over pure FL by 4.25 Spider EX with
   positive paired evidence. The endpoint transfers, while most of the gain is
   already present in the teacher-target CE ablation.

### Not yet supported

1. A statistically established multi-seed final T3 gain.
2. A family-independent incremental benefit from reverse KL beyond
   teacher-target CE.
3. Better accuracy than centralized training.
4. Lower empirical cost than federated large-model training; no federated 7B
   baseline has been run.
5. Broad robustness across IID, quantity-skew, and SQL-pattern-skew settings.
6. An independently stable reverse-KL contribution.
7. Formal privacy guarantees.
8. A distinct structural-distillation component.
9. Semantic equivalence of all `EX=1, EM=0` predictions.

## 5. Active queue

The canonical ordered backlog is `PAPER_TODO.md`. Immediate execution is:

1. Method prose and architecture/privacy-boundary figure from the completed
   P1.4b manuscript skeleton, in parallel with P1.1b-v2 as the next GPU task.
2. One matched FedProx-LoRA reviewer baseline.
3. One audited stronger-skew T1 screen, then deferred seed-2 T2/T3.
4. Federated-7B feasibility only if retaining that empirical claim, followed
   by final claim/evidence QA and manuscript freeze.

FedProx is a recommended reviewer baseline rather than a method direction.
Teacher ceilings and model-size/rank/client sweeps remain optional; broader
heterogeneity is activated only if the paper retains a broad RQ3 claim.

## 6. Provenance map

| Evidence | Canonical location |
|---|---|
| Paper-facing tables | `paper/results/MAIN_RESULTS.md` |
| Stable checkpoint/evaluation IDs | `paper/notes/RESULT_REGISTRY.md` |
| Centralized standard adapter | `artifacts/baselines/central_3ep_standard_s0/adapter` |
| Centralized restart adapter | `artifacts/probe_p/central_3ep/adapter` |
| FedLS-SQL T1-T3 lineage | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0` |
| Independent pure-FL T1-T3 | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0` |
| Gemma 2B pure-FL T1 | `artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` |
| Gemma full FedLS T1 | `artifacts/federated/gemma2_9b_to_2b_fedls_noicl_k5_e1_t1_s0/round_1/m_g` |
| Gemma canonical five-arm evaluation | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260823T005329` |
| BIRD gold audit | `fedicl-sql/processed_data/BIRD/gold_exec_audit_t60/` |
| Common-mask teacher report | `fedicl-sql/audits/bird_train_gold_exec_t60_teacher_comparison.json` |
| Frozen public pool | `processed_data/BIRD/bootstrap_full_exmatch/train.csv` |
| Matched BIRD-gold control | `processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv` |
| Teacher-logit cache | `artifacts/teacher_logit_cache/rkd_k0_full` |
| Matched T1 evaluation | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954` |
| Seed-1 trajectory completion | `fedicl-sql/experiments/eval_arms/results/eval_arms__s1__20260826T094419`; nested result commit `dbd703b` |
| Centralized-standard OOD/BIRD suite | four eval runs `20260820T143356` through `20260820T150048`; nested result commit `7eb7d44` |
| Active commands | `paper/notes/PIPELINE_NEXT.md` |
| RQ-to-evidence status | `paper/notes/EXPERIMENT_MATRIX.md` |
| Historical chronology | `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md` |

Per-run truth remains in saved `config.json`, `metrics.json`, predictions,
manifest fingerprints, and Git SHAs. Presentation labels never replace
internal artifact identities.

## 7. Decision log

| Date | Decision |
|---|---|
| 2026-08-01 | Headline setting reduced to K=5, `alpha=0.5`, seed 0. |
| 2026-08-10 | Factor-wise FedAvg retained; FLoRA-NA closed. |
| 2026-08-10 | Matched ICL evidence negative; no-ICL branch selected. |
| 2026-08-11 | T1 endpoint replicated across three seeds. |
| 2026-08-15 | Distillation-only, OOD, and local-epoch controls completed. |
| 2026-08-16 | T2/T3 and centralized three-pass reference completed. |
| 2026-08-17 | Multi-round result confirmed on three Spider perturbations. |
| 2026-08-18 | BIRD cross-corpus evaluation completed. |
| 2026-08-19 | FedKD pre-server T2/T3 identified as mixed lineage; independent pure FL required. |
| 2026-08-19 | Advisor renamed the paper FedLS-SQL and removed ICL from the method. |
| 2026-08-20 | Active documentation and lab log refactored around FedLS-SQL. |
| 2026-08-20 | Independent pure-FL T1-T3 completed; seed-0 final comparison closed. |
| 2026-08-20 | Matched public-gold gate retained teacher guidance; standalone RKL remains provisional. |
| 2026-08-20 | Continuous and restart centralized recipes are EX-equivalent; continuous selected. |
| 2026-08-20 | Adapter-payload accounting closed at 739.111 MB/round and 2.217 GB through T3. |
| 2026-08-20 | Paper tables moved to `paper/results/MAIN_RESULTS.md` and separated by model family/evidence role. |
| 2026-08-20 | P0.6 filled all centralized-standard transfer cells; no uniform FedLS-over-centralized OOD claim is supported. |
| 2026-08-20 | After P0.6, Gemma matched T1 portability moved ahead of seed replication. |
| 2026-08-21 | The portability gate was strengthened from Qwen-teacher→Gemma-student sequence KD to a complete Gemma 2 9B→2B same-family replication with regenerated targets/logits and exact token-ID validation. |
| 2026-08-21 | P0.7a Gemma 2B smoke passed (8-row diagnostic EX 37.5, EM 12.5, one execution error); teacher and student-independent work split across GPU 0/1. |
| 2026-08-21 | Corrected the Gemma pool design: 3,873 is Qwen's EX-match count, so Gemma now generates all 9,428 BIRD train rows and independently derives `N_gemma`; Qwen-selected indices are prohibited. |
| 2026-08-21 | Refactored the archived Qwen selector into the active common teacher pipeline: raw generation, fixed 8-second quick-exec, then official EX match, each fingerprinted and resumable. |
| 2026-08-21 | Added untouched Gemma 2B base to canonical P0.7d so FL and full FedLS-SQL are both anchored to the pretrained student; overnight lanes remain unchanged. |
| 2026-08-21 | The P0.7b fingerprint guard correctly rejected an old eight-row checkpoint sourced from Qwen's 3,873-row pool; corrected Gemma smoke artifacts use new `fullsource` roots, while the old artifacts remain immutable provenance. |
| 2026-08-21 | P0.7c recorded all 9,428 Gemma teacher outcomes; index 7004 deterministically produced an empty target on retry. Empty output is retained as a teacher failure and rejected before SQLite execution, not retried into success. |
| 2026-08-21 | Retired the parallel Gemma 9B/2B launch after Windows pagefile exhaustion; P0.7 runs sequentially on this host. |
| 2026-08-22 | P0.7e retained `N_gemma=2,487` from 7,162 quick-exec survivors; conditional official statuses were 2,487 match, 4,443 mismatch, 231 gold failure, and one prediction failure. |
| 2026-08-22 | Added P0.7q: a read-only, resumable audit of all 9,428 BIRD gold SQL plus Qwen/Gemma comparison on one common valid mask; conditional gold-failure counts are no longer treated as cross-family denominators. |
| 2026-08-22 | Added a 4-bit Gemma 9B zero-shot Spider reference as P0.7t; it is contextual teacher-ceiling evidence after the main Gemma ladder, not a causal method arm. |
| 2026-08-22 | Corrected the Gemma queue by adding P0.7g immediately after pure FL: the untouched 2B base is evaluated on full Spider before server training and stored in P0.7d's resume root for reuse. |
| 2026-08-22 | P0.7s/g completed: Gemma pure FL improves base by 4.94 Spider EX (141/90 paired gains/losses, `p=0.00096`) but increases execution errors by 50; retain the family branch and audit both accuracy and validity after server transfer. |
| 2026-08-22 | Recorded the P0.7s eval provenance caveat: its config predates the opt-in 4-bit field while metrics report the later repository SHA; effective inference remains the same unquantized default, but future experiment worktrees must not be pulled or changed mid-run. |
| 2026-08-22 | P0.7q found 9,056 valid and 372 invalid local BIRD gold rows; 350 are structural and 330 failures belong to `retail_world`. Every Gemma-selected row is valid, so P0.7d proceeds while the snapshot mismatch remains an explicit data-quality caveat. |
| 2026-08-23 | P0.7d completed the Gemma five-arm ladder: base 52.22, FL 57.16, gold CE 41.68, target CE 61.22, and full FedLS 61.41 EX. Retain endpoint portability over FL, identify teacher-target CE as the robust mechanism, and keep the RKL increment provisional (`+0.19`, `p=0.916`). |
| 2026-08-24 | Evidence is sufficient to retain the framework but not a new RKL-loss claim. Exact/FLoRA aggregation has no measured headroom at the current setting, so the only active method-improvement gate is federated-aware execution-guided hard-SeqKD with equal-budget uniform/random controls. |
| 2026-08-24 | Implemented P0.9a as a resumable, fingerprinted no-training diagnostic over one FedAvg adapter, its uniform-SeqKD descendant, and five client adapters on a deterministic 512-row public subset. Selector training remains blocked until its disagreement/correction report is reviewed. |
| 2026-08-24 | P0.9a completed: global FL 32.23 EX versus uniform SeqKD 53.13 on 512 public rows; 141 failures corrected and 34 regressions. Client disagreement captures 95.39% of FL errors but labels 88.67% of all rows; within-error correction enrichment is not significant (Fisher `p=0.297`). Activate global-error-only P0.9b and cancel P0.9c. |
| 2026-08-24 | Pulled nested result commit `10a0bbd` and validated P0.9b. The two training configs differ only by pool and share 256 examples, 16 optimizer updates, initialization, seed, and all training flags. Global-error256 loses 2.03 Spider EX to random256 (47/68, exact `p=0.0617`) and adds 18 execution errors; the preregistered gate fails. |
| 2026-08-24 | Closed global-error selection and its dependent disagreement/KL extensions. Retain uniform execution-verified hard SeqKD as the fallback method, but keep a separate discussion gate open for a substantively different KD/Federated hypothesis. P0.9 parallel/OOM timing, RAM, and VRAM are not paper resource evidence. |
| 2026-08-24 | Implemented P0.10a as a fingerprinted CPU-only triage over committed P0.9a and canonical Spider predictions. Reusing frozen P0.9a row states is required because re-executing SQL can shift a timeout-bound row. All three discussion gates pass: client plurality `+10.55` public EX, prefix error-risk gap `+18.29` points, and 122 clean global preference rows. Rank LLM-anchored FedDF first, KID second, preference KD third; activate no training automatically. |
| 2026-08-24 | Implemented and preregistered P0.10b code path. New `feddf` server arm keeps verified hard LLM targets and adds forward KL from a sparse five-client ensemble. Cache shards are content-addressed and resumable; metadata fingerprints client adapter weights and rendering flags; union top-k support plus an explicit tail bucket preserves total mass. P0.10c smoke was activated; P0.10d required `+1.0` Spider EX and no execution-error increase over the 512-row hard-target control. |
| 2026-08-24 | P0.10c cache smoke completed with 5 clients, 8 examples, top-32, and mean tail probability `0.000752`, comfortably passing the 10% fidelity gate. The first training launch stopped before training because its reused client stage was fingerprinted with `save_steps=200` while the command requested 4. Preserve the client stage and correct all P0.10 shared-stage commands to 200; use fresh immutable smoke output `p010c2_*` because the failed root already owns the old setup fingerprint. |
| 2026-08-24 | Pulled nested result commit `52fb878` and validated P0.10d on 1,034 paired Spider rows. Hard-target CE scores 56.87 EX / 31.91 EM with 230 execution errors; adding sparse five-client FKL scores 58.32 / 39.94 with 219 errors. The hybrid corrects 58 rows and regresses 43 (`+1.45` EX, exact McNemar `p=0.163`), passing the preregistered practical gate. Activate one untuned 3,873-row P0.10e confirmation; do not change the canonical method yet. |
| 2026-08-25 | Pulled nested result commit `e914efd` and closed P0.10e. Full-pool FedDF scores 60.15 EX / 41.01 EM with 191 execution errors, versus hard-target CE at 61.32 / 30.27 / 161 and RKL at 63.35 / 31.53 / 133. Relative to hard-target CE it has 50/62 paired gains/losses (`p=0.299`), misses the gate by 2.17 points, and adds 30 errors; relative to RKL it is `-3.20` EX (`p=0.00318`). Archive the branch without tuning and activate controlled resource benchmarking. Training resumed from step 416, so accuracy is valid but timing is not paper-eligible. |
| 2026-08-25 | Retired P0.10 from the active project surface. The nested repository keeps compact evidence under `experiments/archive/p010_feddf_2026-08/` and a full recovery point at tag `archive/p010-feddf-evidence`; active FedDF CLI/trainer/cache code and row-level predictions were removed from HEAD. Canonical result tables, registry, architecture, and queue no longer present P0.10 as a paper component. |
| 2026-08-25 | Replaced the broad planning outline with an evidence-backed target outline. EX is the primary endpoint; EM is a secondary cross-dataset SQL-form diagnostic. Resource evidence now uses fixed-warm-up, contention-audited shared-server windows rather than an infeasible exclusivity requirement. Method remains frozen; mandatory next gates are resources, EX-oriented audit, and final T3 seed reliability. |
| 2026-08-25 | Completed P1.1a implementation through `cfa8d59` and P1.2 artifact `4527a76`. The benchmark admits only fresh repetitions with no observed foreign GPU PID into primary latency summaries and preserves failed attempts for safe restart. The T3 audit confirms a 121/67 correction/regression balance and 92 fewer execution failures, but exposes set operations as a significant negative stratum; retain the frozen method and activate P1.1b rather than opening a new KD branch. |
| 2026-08-25 | Added live contention visibility at nested commit `0d0faa5`. The runner prints timestamped detection and clearance transitions with phase/repetition label, physical GPU, PID, process name when accessible, and process GPU memory; identical events remain in `contention_events`. Repeated unchanged PID sets do not spam the console, and any affected repetition remains excluded even after the foreign process clears. |
| 2026-08-25 | GPU capacity is temporarily unavailable. Preserve P1.1b as the first unchanged GPU task and P0.8 seeds as the second; do not replace either with an optional method experiment. Activate the CPU lane: deterministic efficiency/table manifest, related-work novelty audit, and manuscript skeleton. After P0.8, either collect controlled client/server training-resource microbenchmarks or narrow RQ4 to communication plus deployment inference. |
| 2026-08-25 | Implemented P1.4a at nested commit `62cd3f6`. The CPU-only builder reads adapter tensor metadata without model loading, validates stable IDs and canonical paths, reconciles every client upload/global broadcast byte count with each round's aggregation metadata, structures canonical result tables, inventories pending cells, and writes an immutable JSON/CSV pair. The production command is active; no paper values change until its server artifact is validated. |
| 2026-08-25 | The first P1.1b collection completed but the PID-presence gate classified all 5/5 student and 5/5 teacher repetitions as contended because Windows/WDDM exposed many persistent contexts. Its descriptive medians were about 25.62 s/32 queries for the 1.5B student and 53.44 s/32 queries for the 7B teacher (about 2.09x), but these are not canonical. Per operator decision, commit `487b3b2` removes PID enumeration and treats each fresh successful repetition independently while retaining device telemetry. P1.1b-v2 must use new roots and must not merge the superseded collection. |
| 2026-08-25 | Deferred P1.1b-v2 by operator decision and promoted P0.8 seed reliability. Seed 1 is now the active GPU gate; seed 2 runs only after the paired seed-1 Spider endpoint remains positive. Resource code and the v2 command remain reproducible for later reactivation, but the resource block must not delay the primary accuracy-evidence decision. |
| 2026-08-25 | Audited P0.8a against the current checkpoint contract. Seed 1 already has canonical T1 roots (`fedavg_noicl_k5_e1_t1_s1`, setup `3680b91c...`; `fedkd_noicl_k5_e1_t1_s1`, setup `c695a493...`). The active command now pins those identities, executes rounds 2 and 3 explicitly, and evaluates only final Spider T3 endpoints. The archived `run --rounds 3` recipe is superseded because it would restart at round 1 and could break the established lineage. |
| 2026-08-26 | Pulled nested result commit `2237b22` through merge `78cc611` and closed P0.8a. At seed 1, final pure FL/FedLS-SQL score 61.99/65.76 Spider EX with 213/126 execution errors. FedLS has 111 paired corrections and 72 regressions (`+3.77`, exact `p=0.00483`; paired bootstrap 95% interval about `[+1.26,+6.38]`) and remains positive in every hardness stratum. Seeds 0/1 therefore give deltas `+5.23/+3.77`, mean `+4.50`, sample SD `1.03`; activate the unchanged seed-2 continuation as P0.8b. |
| 2026-08-26 | Reprioritized after endpoint review. Seed 2 already has canonical T1 FL, teacher-target CE, and full CE+RKL checkpoints, but its T2/T3 continuation is delayed. Two positive final T3 seeds are enough for the current method-direction decision. Activate an eval-only seed-1 trajectory completion for the four missing observations; next scientific expansion should target a named gap such as federated heterogeneity or resource evidence rather than another model family/OOD seed sweep. |
| 2026-08-26 | Audited the advisor outline against current evidence and recent nearest work. The core accuracy/transfer result is sufficient to draft but not yet submission-ready for Q3: novelty positioning, deterministic/resource evidence, claim-scoped non-IID support, and baseline breadth remain the main risks. Added `PAPER_TODO.md` as the adaptive ordered backlog. Generic federated LLM-SLM novelty is no longer claimed; P1.4b must compare FedMKT, FedCoLLM, FedCoT, LaDa, federated KD/PEFT, and execution-aware NL-to-SQL. Recommend one matched FedProx-LoRA baseline before final seed-2 closure; retain one heterogeneity sensitivity only if broad RQ3 wording survives. |
| 2026-08-26 | Corrected P1.4a at code commit `a25db62` after the first server attempt showed that the training host does not contain the separate paper repository. `build_paper_table_manifest.py` now supports an artifact-only mode with explicit canonical checkpoint mappings. The server continues to verify safetensors schema, serialized payload bytes, and immutable round metadata, then pushes only compact JSON/CSV; registry and paper-table reconciliation remains a local documentation step. No adapter transfer is required. |
| 2026-08-26 | The second P1.4a attempt exposed the seed-0 FedLS split lineage rather than missing scientific evidence: round-1 clients/FedAvg were intentionally shared from `florana_kd_noicl_k5_e1_t1_s0/round_1`, while the refined `m_g` lives in `fedkd_noicl_k5_e1_t1_s0/round_1`; rounds 2–3 use the FedLS root normally. Code commit `f59a040` adds an explicit per-round artifact-source override so the audit follows the immutable historical lineage without copying files, mutating artifacts, or rerunning training. |
| 2026-08-26 | Closed P1.4a with artifact commit `147f455`, fingerprint `d665d476...`, and registry ID `audit.paper.tables.qwen.s0`. Both final adapters contain 18,464,768 FP32 parameters across the same 392-tensor schema. The paper reports method-faithful logical tensor payload: 73,859,072 bytes/adapter, 738,590,720 bytes/round for five uploads plus five broadcasts, and 2,215,772,160 bytes through T3. The serialized audit proxy is retained separately because round metadata sizes `fedavg_adapter`, while FedLS broadcasts post-server `m_g`; the final files differ only by 32 bytes of safetensors header. Runtime resource cells remain open. |
| 2026-08-26 | Closed P0.8a-E at nested result commit `dbd703b`. The four fresh 1,034-row evaluations complete seed-1 convergence without retraining: pure FL T2 61.70 EX/213 errors; FedLS mixed pre-server T2 63.25/195; FedLS T2 endpoint 64.22/121; mixed pre-server T3 64.70/156. Combined with registered T1 and T3 endpoints, FedLS rises 62.48→64.22→65.76 while pure FL rises 57.45→61.70→61.99. FedLS T1→T3 is +3.29 EX (78/44, `p=0.00266`); pure FL T2→T3 is +0.29 (`p=0.810`). The T3 pre-server model retains a significant +2.71 over pure FL (`p=0.0193`). T2/T3 server increments are +0.97/+1.06 but individually non-significant, so claim cumulative recurring transfer and retained knowledge rather than guaranteed per-round EX gains. |
| 2026-08-26 | Closed P1.4b with `RELATED_WORK_NOVELTY_MATRIX.md` and `MANUSCRIPT_SKELETON.md`. FedCoLLM already contains the closest generic client-LoRA aggregation plus recurring server LLM/SLM KD loop, and Struct-SQL already filters teacher Text-to-SQL samples by execution correctness. Removed “A Novel ... Framework” from the active title. The defensible contribution is the complete federated NL-to-SQL workflow: frozen server teacher, public result-equivalent SQL targets, private adapter-only clients, recurring global-SLM refinement, EX-oriented controls, and SLM-only deployment. Generic first/novel FL, KD, PEFT, or execution-filtering claims are prohibited. |
| 2026-08-27 | Reconciled the adaptive plan with the advisor's original scientific target. The project still asks whether large-to-small collaboration addresses lightweight federated NL-to-SQL accuracy while retaining data locality, communication efficiency, and resource advantages; the operational wording separates those testable claims and avoids formal-privacy or unmeasured federated-7B implications. Reactivated P1.1b-v2 as the next GPU task. After method/figure drafting, prioritize matched FedProx-LoRA, exactly one audited stronger-skew T1 screen, and seed-2 T3. A federated-7B T1 feasibility reference is conditional on retaining a direct large-model-FL claim. |

## 8. Archived branches

The archive retains teacher-side ICL, retriever sweeps, centralized ICL
matrices, FLoRA-NA, exact aggregation, skew-RKL, pipeline reordering, early
public-pool probes, and discarded evaluations. They remain available for
reproducibility but are not active paper components.
