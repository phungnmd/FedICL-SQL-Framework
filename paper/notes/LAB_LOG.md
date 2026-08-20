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
  `Centralized <> FL <> FedLS-SQL` comparison are complete at seed 0.
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
| Centralized, 3 epochs | `artifacts/probe_p/central_3ep/adapter` | 67.60 | 57.87 | 53.19 | 52.52 | 12.91 |
| Pure FL, T=3 | `fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter` | 64.31 | 56.10 | 51.93 | 46.73 | 12.91 |
| FedLS-SQL, T=3 | `fedkd_noicl_k5_e1_t1_s0/round_3/m_g` | **69.54** | **59.65** | **55.51** | **52.71** | **21.58** |

At T3, FedLS-SQL exceeds pure FL by `+5.23`, `+3.55`, `+3.58`, `+5.98`,
and `+8.67` EX on Spider, Realistic, Syn, DK, and BIRD respectively. The paired
exact McNemar results are significant on Spider (`p=0.0001`), Syn (`p=0.0094`),
DK (`p=0.0002`), and BIRD (`p<1e-19`), but not Realistic (`p=0.095`).

FedLS-SQL also has the highest EX in all five final-model comparisons. Its
advantage over centralized training is not significant on the four Spider
sets; BIRD is the exception, but remains a cross-corpus diagnostic favorable
to the BIRD-trained public-server branch.

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

### 3.4 T=1 replication and component evidence

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

### 3.5 Centralized training reference

| Centralized private-data passes | Spider EX | OOD pooled EX |
|---|---:|---:|
| 1 | 62.19 | 51.04 |
| 2 | 67.02 | **54.31** |
| 3 | **67.60** | 54.16 |

The centralized curve saturates after the second pass. Matched by private-data
passes, the FedLS-SQL endpoints differ from centralized by `+1.16`, `-0.87`,
and `+1.93` at passes 1, 2, and 3; none is individually significant.

This is not compute matching. At three passes, FedLS-SQL uses 25,977 client
steps plus 11,619 public server steps, versus 25,977 centralized steps. Report
the additional server compute rather than claiming equal cost.

### 3.6 BIRD cross-corpus transfer

| Arm | EX | Execution-error rate |
|---|---:|---:|
| Base SLM | 10.89 | 46.5% |
| T1 pure FL | 11.21 | 55.2% |
| T3 pure FL | 12.91 | 49.3% |
| T1 FedKD-lineage pre-server | 11.15 | 55.3% |
| Centralized, 3 epochs | 12.91 | 42.6% |
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

### 3.7 ICL negative ablation

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
4. Server guidance strongly improves BIRD cross-corpus transfer and reduces
   execution errors across all evaluated datasets.
5. The 1.5B deployed model requires neither the 7B teacher nor public data at
   client inference time.
6. ICL and FLoRA-NA do not improve the retained configuration.

### Not yet supported

1. A statistically established multi-seed T2/T3 trajectory.
2. Better accuracy than centralized training; the T3 difference is not
   significant and compute is not matched.
3. Lower empirical cost than federated large-model training; no actual
   large-model FL baseline has been run.
4. Formal privacy guarantees.
5. A distinct structural-distillation contribution; the implemented server
   objective is teacher-target CE plus reverse KL.

### Metric caveat

EM is comparable only within the same training stage. Server KD changes SQL
surface conventions while EX improves, so pre/post-server claims should use EX
and execution-error rate as primary metrics.

## 5. Active queue

1. **P0:** consolidate trainable parameters, adapter bytes, total
   communication, wall time, peak VRAM, and inference latency.
2. **P1:** replicate the T1-T3 trajectory for seeds 1 and 2.
3. **P2:** run FedProx, size/rank, or broader-skew sweeps only after advisor
   scope confirmation.

No ICL, FLoRA-NA, self-consistency, or T4/T5 experiment is active.

## 6. Provenance map

| Evidence | Canonical location |
|---|---|
| Centralized 3-pass adapter | `artifacts/probe_p/central_3ep/adapter` |
| FedLS-SQL T1-T3 lineage | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0` |
| Pure-FL T1-T3 lineage | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0` |
| Frozen public pool | `processed_data/BIRD/bootstrap_full_exmatch/train.csv` |
| Teacher-logit cache | `artifacts/teacher_logit_cache/rkd_k0_full` |
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

## 8. Archived branches

The full chronology retains teacher-side ICL, retriever sweeps, centralized ICL
matrices, FLoRA-NA, exact aggregation, skew-RKL, pipeline reordering, early
public-pool probes, and discarded evaluation attempts. These are useful for
reproducibility but are not active paper components.

See `paper/archive/pre_fedls_2026-08/README.md` for routing.
