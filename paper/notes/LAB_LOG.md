# FedLS-SQL — active lab log

> Refreshed 2026-08-20. This is the compact decision ledger for the current
> paper. The complete chronology through this date is preserved at
> `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`.

This file records protocol, interpretation, claim limits, open work, and
decisions. It deliberately does not own result tables:

- paper-facing values: `paper/results/MAIN_RESULTS.md`;
- stable checkpoints/evaluation IDs: `RESULT_REGISTRY.md`;
- executable commands: `PIPELINE_NEXT.md`;
- method definition: `system_architecture.md`.

## 1. Current status

- Paper: **FedLS-SQL: A Novel Federated Large-Small Language Models Framework
  for Natural Language to SQL**.
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
- P0.7a passed: Gemma 2B trained/reloaded/evaluated; its eight-row `37.5 EX`
  is diagnostic only. P0.7b must use the immutable `fullsource` smoke roots
  because the earlier smoke checkpoint came from Qwen's 3,873-row source.
  GPU 0 must generate Gemma targets over all 9,428 BIRD training rows, then
  apply the fixed 8-second quick-exec and official EX stages to derive
  `N_gemma`. GPU 1 may independently train pure FL, but gold CE waits for the
  selected indices.
- Final T3 seed-1/2 reliability is retained as P0.8 but deferred under the
  current discovery-first priority.
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
  perturbation sets at seed 0. Final T3 training-seed reliability remains open.
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
  `EX=1, EM=0` cases. Equivalent-SQL and EX false-positive auditing remains
  required; report EM transparently.

### 3.3 Efficiency evidence

- The serialized global adapter is `73,911,080` bytes.
- Five uploads plus five broadcasts total `739,110,960` bytes per round and
  `2,217,332,880` bytes (`2.065 GiB`) through T3.
- Pure FL and FedLS-SQL have the same client-network payload because teacher
  transfer is server-local.
- These values exclude transport framing and protocol metadata.
- Shared-server timing and RAM are operational logs only. Official latency,
  VRAM, RSS, throughput, and trainable-parameter table cells remain pending a
  fixed-warm-up, exclusive-hardware benchmark.

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

### Not yet supported

1. A statistically established multi-seed final T3 gain.
2. Family-agnostic portability of full CE+RKL FedLS-SQL.
3. Better accuracy than centralized training.
4. Lower empirical cost than federated large-model training; no federated 7B
   baseline has been run.
5. Broad robustness across IID, quantity-skew, and SQL-pattern-skew settings.
6. An independently stable reverse-KL contribution.
7. Formal privacy guarantees.
8. A distinct structural-distillation component.
9. Semantic equivalence of all `EX=1, EM=0` predictions.

## 5. Active queue

1. P0.7b-c/e/T1F, GPU 0: teacher/cache/tokenizer smoke, generate all 9,428
   BIRD targets, then apply the canonical 8-second quick-exec and official EX
   stages to obtain `N_gemma` and build its gold control.
2. P0.7s/T1F after the teacher lane: pure FL and diagnostic evaluation only;
   the current Windows host cannot safely co-load Gemma 9B and train Gemma 2B.
3. P0.7d/T1F after selection: matched gold CE, target CE, full online CE+RKL,
   and canonical five-arm base/FL/gold/target/full evaluation; build a full
   cache only after a positive gate.
4. P1.1: controlled accuracy/resource benchmark after fixed in-process warm-up.
5. CPU-only EX-EM/error audit when it does not block the active GPU task.
6. P0.8/T1R: final T3 seed-1/2 reliability remains pre-submission work but is
   not the current discovery task.

FedProx, broader heterogeneity, model-size/rank/client sweeps, and additional
component seeds remain behind these gates.

## 6. Provenance map

| Evidence | Canonical location |
|---|---|
| Paper-facing tables | `paper/results/MAIN_RESULTS.md` |
| Stable checkpoint/evaluation IDs | `paper/notes/RESULT_REGISTRY.md` |
| Centralized standard adapter | `artifacts/baselines/central_3ep_standard_s0/adapter` |
| Centralized restart adapter | `artifacts/probe_p/central_3ep/adapter` |
| FedLS-SQL T1-T3 lineage | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0` |
| Independent pure-FL T1-T3 | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0` |
| Frozen public pool | `processed_data/BIRD/bootstrap_full_exmatch/train.csv` |
| Matched BIRD-gold control | `processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv` |
| Teacher-logit cache | `artifacts/teacher_logit_cache/rkd_k0_full` |
| Matched T1 evaluation | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954` |
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

## 8. Archived branches

The archive retains teacher-side ICL, retriever sweeps, centralized ICL
matrices, FLoRA-NA, exact aggregation, skew-RKL, pipeline reordering, early
public-pool probes, and discarded evaluations. They remain available for
reproducibility but are not active paper components.
