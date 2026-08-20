# FedLS-SQL — Active Lab Log

> Refreshed 2026-08-20. This is the compact evidence ledger for the current
> paper. The complete chronology through this date is preserved at
> `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`.

This file records only the current protocol, decision-relevant results, claim
limits, open work, and provenance. Detailed method description belongs in
`system_architecture.md`; executable commands belong in `PIPELINE_NEXT.md`;
canonical checkpoint labels belong in `RESULT_REGISTRY.md`.

## 1. Current status

- Paper: **FedLS-SQL: A Novel Federated Large-Small Language Models Framework
  for Natural Language to SQL**.
- Method: private client LoRA fine-tuning on an SLM, sample-weighted
  factor-wise FedAvg, then server-side LLM-to-SLM distillation on public data.
- Student: `Qwen/Qwen2.5-1.5B-Instruct`.
- Frozen teacher: `Qwen/Qwen2.5-Coder-7B-Instruct`.
- Public KD pool: fixed **3,873-row** BIRD teacher-generated EX-match subset.
- Canonical inference: greedy, zero-shot, `k=0`.
- Best current FedLS-SQL endpoint: **69.54 Spider EX at T=3, seed 0**.
- Independent pure-FL T1-T3 and the final
  `Centralized <> FL <> FedLS-SQL` comparison are complete on Spider at seed 0;
  the official centralized recipe still needs its four transfer/OOD cells.
- The matched T1 public-supervision gate is complete: teacher-target CE and
  full FedLS-SQL beat an equal-row BIRD-gold CE control, so extra public
  supervision alone does not explain the gain.
- ICL is a closed negative ablation; FLoRA-NA is a closed aggregation branch.
- Internal names such as `fedicl_sql`, `fedkd`, `noicl`, and old artifact paths
  remain unchanged for compatibility and provenance.

## 2. Canonical protocol

| Item | Setting |
|---|---|
| Clients | `K=5` |
| Partition | Spider non-IID, Dirichlet `alpha=0.5`, seed 0 |
| Client model | Qwen2.5-1.5B-Instruct + LoRA |
| Client objective | gold-SQL cross-entropy |
| Local work | one epoch per round unless explicitly labeled otherwise |
| Aggregation | sample-weighted factor-wise FedAvg |
| Server teacher | frozen Qwen2.5-Coder-7B-Instruct |
| Server objective | teacher-target CE + reverse KL |
| Public data | 3,873 BIRD teacher-generated EX-match rows |
| Primary evaluation | Spider dev, 1,034 rows |
| Robustness | Spider-Realistic, Spider-Syn, Spider-DK |
| Cross-corpus | BIRD dev, 1,534 rows |
| Decoding | greedy, no ICL |

Canonical method lineage:

```text
round t:
  private client CE -> weighted FedAvg -> public teacher CE + reverse KL
```

Canonical pure-FL control lineage:

```text
base -> FedAvg T1 -> FedAvg T2 -> FedAvg T3
```

The `round_2/round_3/fedavg_adapter` objects inside a `fedkd` run are not pure
FL: they inherit earlier post-KD global adapters.

### Privacy boundary

- Raw client rows, schemas, questions, and SQL do not leave clients.
- The server teacher sees only the public pool.
- Only LoRA adapter parameters cross the network.
- This is structural data isolation, not differential privacy, secure
  aggregation, or a formal defense against update inference.

## 3. Main results

### 3.1 Final-model table

| Model | Checkpoint | Spider EX | Realistic | Syn | DK | BIRD |
|---|---|---:|---:|---:|---:|---:|
| Centralized-standard-3ep | `artifacts/baselines/central_3ep_standard_s0/adapter` | 67.31 | — | — | — | — |
| Pure FL, T=3 | `fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter` | 64.31 | 56.10 | 51.93 | 46.73 | 12.91 |
| FedLS-SQL, T=3 | `fedkd_noicl_k5_e1_t1_s0/round_3/m_g` | **69.54** | **59.65** | **55.51** | **52.71** | **21.58** |

At T3, FedLS-SQL exceeds pure FL by `+5.23`, `+3.55`, `+3.58`, `+5.98`,
and `+8.67` EX on Spider, Realistic, Syn, DK, and BIRD respectively. The paired
exact McNemar results are significant on Spider (`p=0.0001`), Syn (`p=0.0094`),
DK (`p=0.0002`), and BIRD (`p<1e-19`), but not Realistic (`p=0.095`).

On Spider, FedLS-SQL is `+2.22 EX` above the official centralized standard, but
the paired difference is not significant (`p=0.0865`). Standard centralized
OOD cells are not yet evaluated; historical restart OOD values must not be
silently attached to the standard recipe.

### 3.2 Multi-round trajectory, seed 0

| Round | Independent pure FL | FedKD-lineage pre-server | FedLS-SQL endpoint |
|---|---:|---:|---:|
| T=1 | 56.67 | 57.35 | 63.35 |
| T=2 | 62.19 | 64.02 | 66.15 |
| T=3 | 64.31 | 66.05 | **69.54** |

| Endpoint contrast | Delta | Paired `p` |
|---|---:|---:|
| T1 → T2 | +2.80 | 0.0019 |
| T2 → T3 | +3.38 | 0.0002 |
| T1 → T3 | **+6.19** | <1e-4 |

At matched two passes over private data, `T=2, E=1` beats `T=1, E=2` by
`+2.61 EX` (`p=0.0067`). The observed gain therefore comes from repeated
communication/aggregation/distillation rounds, not merely longer local
training.

The pre-server trajectory above is diagnostic only. T2 and T3 already contain
earlier KD and cannot be labeled pure FL.

### 3.3 Robustness across rounds

| FedLS-SQL endpoint EX | T=1 | T=2 | T=3 | T1 → T3 | `p` |
|---|---:|---:|---:|---:|---:|
| Spider dev | 63.35 | 66.15 | **69.54** | +6.19 | <1e-4 |
| Spider-Realistic | 52.95 | 56.30 | **59.65** | +6.69 | <1e-4 |
| Spider-Syn | 49.61 | 52.03 | **55.51** | +5.90 | <1e-4 |
| Spider-DK | 47.85 | 50.47 | **52.71** | +4.86 | 0.0007 |

The multi-round improvement has the same direction on all four benchmarks.
This is currently the strongest evidence for the method, but it is still one
seed at T2/T3.

The marginal server step is distribution-dependent: it improves canonical
Spider at T1 and T3, but none of the nine pre/post cells on the three perturbed
Spider sets is significant. It consistently reduces execution errors, even
when EX does not increase.

### 3.4 Matched T=1 public-supervision gate

All arms below start from the same seed-0 T1 FedAvg adapter and use the same
3,873 retained BIRD row identities. Only the server treatment differs.

| Arm | Spider EX | Spider EM | Exec. errors | Error rate |
|---|---:|---:|---:|---:|
| FL, shared pre-server | 57.35 | 50.58 | 236 | 22.82% |
| + matched BIRD-gold CE | 57.83 | 23.89 | 195 | 18.86% |
| + teacher-target CE | 61.32 | 30.27 | 161 | 15.57% |
| + teacher-target CE and reverse KL | **63.35** | 31.53 | **133** | **12.86%** |

Paired Spider EX contrasts on the same 1,034 rows:

| Contrast | Delta | Wins/losses | Approx. paired 95% CI | Exact McNemar `p` |
|---|---:|---:|---:|---:|
| public gold over FL | +0.48 | 127/122 | [-2.51, +3.48] | 0.800 |
| teacher target over public gold | **+3.48** | 86/50 | [+1.28, +5.68] | **0.0026** |
| reverse KL over teacher target | +2.03 | 59/38 | [+0.17, +3.89] | 0.0417 |
| full FedLS-SQL over public gold | **+5.51** | 93/36 | [+3.38, +7.64] | **<1e-6** |
| full FedLS-SQL over FL | **+6.00** | 145/83 | [+3.16, +8.84] | **<1e-4** |

Decision: Gate T1 passes. A matched public labeled pass does not improve EX
over FL, whereas teacher-generated hard targets provide the clearest causal
increment. Reverse KL adds a positive seed-0 increment but remains provisional
at the training-seed level. The full server treatment also cuts execution
errors by 103 relative to FL.

The EM decline is real under the official Spider component-set evaluator:
server-refined models produce substantially more `EX=1, EM=0` predictions
(`338` for full FedLS-SQL versus `101` for FL). Before publication, audit
whether these are legitimate equivalent SQL forms or single-database EX false
positives. Do not use EM to reject the EX result, and do not hide the gap.

Canonical result:
`fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954/`,
produced with `git_sha=b3fd32f` and committed in `7c1414b`.

### 3.5 T=1 replication and component evidence

| Stage | seed 0 | seed 1 | seed 2 | mean ± sd |
|---|---:|---:|---:|---:|
| FedAvg, pre-server | 57.35 | 57.45 | 59.77 | 58.19 ± 1.37 |
| + teacher-target CE | 61.32 | 62.28 | 59.48 | 61.03 ± 1.42 |
| + reverse KL, full endpoint | 63.35 | 62.48 | 62.38 | **62.74 ± 0.53** |

Three-seed component contrasts:

| Contrast | Mean delta | sd | `p` |
|---|---:|---:|---:|
| whole server distillation over FedAvg | **+4.55** | 1.75 | **0.046** |
| reverse KL over teacher-target CE | +1.71 | 1.38 | 0.165 |
| full method over distillation-only | +1.39 | 1.12 | 0.165 |

Safe reading:

- the full T1 endpoint is stable across three seeds;
- the server stage as a whole improves federation alone;
- the extra value of reverse KL and the private federated stage is positive but
  not established across three seeds;
- single-seed McNemar results must not be presented as across-seed method
  significance.

### 3.6 Centralized training reference

The official conventional recipe is one continuous three-epoch run. It reaches
`67.31 EX`, `64.41 EM`, and `14.31%` execution errors. The historical
three-pass-restart recipe reaches `67.60 EX`, `62.67 EM`, and `15.76%` errors.
Their EX difference is only `0.29 pp` (66 standard wins versus 69 restart wins,
`p=0.863`), so standard is selected rather than optimizing the label around
three noisy examples.

| Historical restart private-data passes | Spider EX | OOD pooled EX |
|---|---:|---:|
| 1 | 62.19 | 51.04 |
| 2 | 67.02 | **54.31** |
| 3 | **67.60** | 54.16 |

The historical restart curve saturates after the second pass. As a diagnostic
matched by private-data passes, the FedLS-SQL endpoints differ from that
restart schedule by `+1.16`, `-0.87`, and `+1.93` at passes 1, 2, and 3; none
is individually significant. These values do not replace the official
continuous three-epoch baseline above.

This is not compute matching. At three passes, FedLS-SQL uses 25,977 client
steps plus 11,619 public server steps, versus 25,977 centralized steps. Report
the additional server compute rather than claiming equal cost.

### 3.7 Communication accounting

Committed round metrics report a serialized global-adapter payload of
`73,911,080` bytes. Across five clients, one round contains `369,555,560` bytes
of uploads and `369,555,400` bytes of broadcasts, totaling `739,110,960` bytes
(`704.87 MiB`). Three rounds total `2,217,332,880` bytes (`2.065 GiB`). Pure FL
and FedLS-SQL have the same client-network payload because KD is server-local.
The count excludes transport framing and protocol metadata; trainable-parameter
count remains to be exported alongside these byte values.

### 3.8 BIRD cross-corpus transfer

| Arm | EX | Execution-error rate |
|---|---:|---:|
| Base SLM | 10.89 | 46.5% |
| T1 pure FL | 11.21 | 55.2% |
| T3 pure FL | 12.91 | 49.3% |
| T1 FedKD-lineage pre-server | 11.15 | 55.3% |
| Centralized-3pass-restart (historical) | 12.91 | 42.6% |
| T3 FedKD-lineage pre-server | 17.67 | 37.9% |
| T1 FedLS-SQL | 19.43 | 33.4% |
| T3 FedLS-SQL | **21.58** | **29.9%** |

Within the FedKD lineage, the server step contributes `+8.28 EX` at T1 and
`+3.91` at T3 (`p<1e-6`).
Independent pure FL rises from 11.21 to 12.91 EX between T1 and T3, whereas
FedLS-SQL reaches 21.58. This complements the
perturbed Spider result, where federated rounds dominate and marginal server KD
is not established.

BIRD is a cross-corpus diagnostic, not a headline benchmark. Its evaluation
databases are disjoint from the public pool, but the corpus favors the BIRD-KD
branch and the current prompt omits BIRD evidence hints.

### 3.9 ICL negative ablation

| Effect | Result |
|---|---:|
| matched client ICL training before server | -2.90 EX, `p=0.008` |
| demonstrations at inference within ICL-trained model | -3.87 EX, `p=0.003` |
| client training-time multiplier | 2.35x |

Decision: canonical FedLS-SQL uses `train_k=0`, `k_teacher=0`, and `eval_k=0`.
No further ICL sweep is planned. Detailed evidence is in
`ICL_NEGATIVE_RESULT.md` and the pre-FedLS archive.

## 4. Claims and limits

### Supported

1. Multi-round FedLS-SQL improves from T1 to T3 on Spider and all three Spider
   perturbation sets at seed 0.
2. At T3 seed 0, FedLS-SQL beats independent pure FL on Spider by `+5.23 EX`
   (`p=0.0001`), with positive gains on every additional test set.
3. At T1 across three seeds, the full server distillation stage improves over
   federation alone by `+4.55 EX` (`p=0.046`).
4. At matched T1 seed 0, teacher-target CE beats equal-row BIRD-gold CE by
   `+3.48 EX` (`p=0.0026`); full FedLS-SQL beats public-gold CE by `+5.51 EX`
   (`p<1e-6`). Extra public supervision alone does not explain the observed
   gain at this gate.
5. Server guidance strongly improves BIRD cross-corpus transfer and reduces
   execution errors across all evaluated datasets.
6. The 1.5B deployed model requires neither the 7B teacher nor public data at
   client inference time.
7. ICL and FLoRA-NA do not improve the retained configuration.

### Not yet supported

1. A statistically established multi-seed T2/T3 trajectory.
2. Better accuracy than centralized training; the T3 difference is not
   significant and compute is not matched.
3. Lower empirical cost than federated large-model training; no actual
   large-model FL baseline has been run.
4. Formal privacy guarantees.
5. A distinct structural-distillation contribution; the implemented server
   objective is teacher-target CE plus reverse KL.
6. An independently stable reverse-KL contribution across training seeds; its
   three-seed incremental contrast is positive but not significant.
7. That every `EX=1, EM=0` server-stage prediction is semantically equivalent;
   the large metric divergence still requires an error audit.

### Metric caveat

EM uses the official Spider component-set evaluator, not raw string equality.
Server refinement nevertheless changes query structure enough that EM falls
while EX and execution validity improve. Pre/post-server claims should use EX
and execution-error rate as primary metrics, report EM transparently, and
audit representative `EX=1, EM=0` cases for equivalent forms and EX false
positives.

## 5. Active queue

1. **P0:** evaluate `Centralized-standard-3ep` on Realistic, Syn, DK, and BIRD,
   then fill the canonical final-model table without borrowing restart values.
2. **P1:** export the trainable-parameter count, add fixed in-process warm-up,
   and collect controlled wall time, peak VRAM/RSS, and inference latency on an
   exclusive GPU; communication payload bytes are already consolidated.
3. **P1:** audit T1 execution errors and EX-EM disagreement, then run only
   targeted seed-1/2 public-gold controls if the causal table still needs them.

FedProx and broader-skew experiments remain behind these gates.

No ICL, FLoRA-NA, self-consistency, or T4/T5 experiment is active.

## 6. Provenance map

| Evidence | Canonical location |
|---|---|
| Centralized 3-pass adapter | `artifacts/probe_p/central_3ep/adapter` |
| Centralized standard 3-epoch adapter | `artifacts/baselines/central_3ep_standard_s0/adapter` |
| FedLS-SQL T1-T3 lineage | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0` |
| Pure-FL T1-T3 lineage | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0` |
| Frozen public pool | `processed_data/BIRD/bootstrap_full_exmatch/train.csv` |
| Matched BIRD-gold control | `processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv` |
| Teacher-logit cache | `artifacts/teacher_logit_cache/rkd_k0_full` |
| Matched T1 evaluation | `experiments/eval_arms/results/eval_arms__s0__20260820T065954` |
| Completed pure-FL command | `paper/archive/pre_fedls_2026-08/legacy_runbooks/PIPELINE_BLOCK_K_completed_2026-08-20.md` |
| Active experiment queue | `paper/notes/PIPELINE_NEXT.md` |
| Checkpoint/result labels | `paper/notes/RESULT_REGISTRY.md` |
| RQ-to-evidence status | `paper/notes/EXPERIMENT_MATRIX.md` |
| Full historical log | `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md` |

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
| 2026-08-19 | Pre-server T2/T3 identified as mixed KD lineage; pure FL required. |
| 2026-08-19 | Advisor renamed the paper FedLS-SQL and removed ICL from method. |
| 2026-08-20 | Active documentation and lab log refactored around FedLS-SQL. |
| 2026-08-20 | Independent pure-FL T1-T3 completed; final three-way table closed at seed 0. |
| 2026-08-20 | Matched public-gold gate passed: teacher targets, not merely extra public CE, explain the main T1 server gain; standalone RKL evidence remains provisional. |
| 2026-08-20 | Standard continuous and restart centralized recipes are EX-equivalent; standard 67.31 selected as official methodology, restart retained as sensitivity. |
| 2026-08-20 | Existing round metrics close adapter-payload communication accounting at 739.111 MB/round and 2.217 GB over T1-T3; standard centralized transfer/OOD evaluation becomes the next run. |

## 8. Archived branches

The full chronology retains teacher-side ICL, retriever sweeps, centralized ICL
matrices, FLoRA-NA, exact aggregation, skew-RKL, pipeline reordering, early
public-pool probes, and discarded evaluation attempts. These are useful for
reproducibility but are not active paper components.

See `paper/archive/pre_fedls_2026-08/README.md` for routing.
