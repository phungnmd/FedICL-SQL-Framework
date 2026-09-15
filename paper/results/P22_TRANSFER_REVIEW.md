# P2.2 transfer review — 2026-09-15

## Published evidence and checks

Nested result commits: `5e4f005` (full-gold CE), `1b2c46a` (reverse
matched T1), and `ec5b5e1` (Hinton headline). Producing code SHA recorded in
the evaluation metrics is `e2ca26e`; publication SHAs are not execution SHAs.

For all five datasets, parsed prediction counts and recomputed EX agree with
metrics (within four-decimal rounding). Paired comparisons have identical
ordered `row_id`, `db_id`, question, gold SQL, and full prompt. Student
headline and full-gold evaluation both use seed 0, batch size 16, k=0.
Spider uses `spider_result_eq_v1`; BIRD uses
`bird_official_set_pair_timeout30_v2` and provided evidence.

## Spider-private / BIRD-public results

All values are EX (%). Centralized E3 is trained on Spider; its BIRD score is
cross-dataset transfer, not the BIRD-trained centralized baseline. Teacher
Spider/BIRD anchors are previously published; variant teacher runs are new.

| Evaluation | n | Central E3 | Pure FL T1 | SeqKD T1 | Full-gold CE T1 | Hinton T1 | Teacher 7B |
|---|---:|---:|---:|---:|---:|---:|---:|
| Spider | 1,034 | 67.31 | 57.35 | 57.93 | 55.03 | 58.32 | 76.69 |
| Realistic | 508 | 55.91 | 54.92 | 46.65 | 47.05 | 42.72 | 71.06 |
| SYN | 1,034 | 54.06 | 49.32 | 48.26 | 43.91 | 44.58 | 63.83 |
| DK | 535 | 53.27 | 45.23 | 45.61 | 40.93 | 45.42 | 62.43 |
| BIRD dev, evidence | 1,534 | 17.73 | 14.80 | 34.68 | 32.14 | 36.70 | 47.07 |

| Evaluation | Hinton − full-gold CE (pp) | CE errors corrected / CE successes lost | Hinton − FL (pp) | FL errors corrected / FL successes lost |
|---|---:|---:|---:|---:|
| Spider | +3.29 | 104 / 70 | +0.97 | 142 / 132 |
| Realistic | −4.33 | 33 / 55 | −12.20 | 44 / 106 |
| SYN | +0.67 | 93 / 86 | −4.74 | 104 / 153 |
| DK | +4.49 | 51 / 27 | +0.19 | 49 / 48 |
| BIRD | +4.56 | 157 / 87 | +21.90 | 389 / 53 |

The rounded console figures previously used in notes have been superseded by
these published metrics. Small net differences (10 Spider answers versus FL,
7 SYN answers versus CE, 1 DK answer versus FL) are not established robust
gains. No multi-seed or database-cluster uncertainty claim follows from them.

The Hinton recipe beats full-gold CE on four sets, with 70 additional correct
BIRD answers. This supports keeping Hinton as a candidate. It compares CE
against `0.5 CE + 0.5 T² FKL`, not an isolated change of the KL term with fixed
CE weight. The two arms share public rows, LR, context policy, and client
recipe; SeqKD uses only 5,319 selected teacher sequences, so Hinton-versus-
SeqKD also changes data budget and target prefixes.

Execution errors fall from FL to Hinton on every set. Realistic falls from
117 to 88 errors while correct answers fall from 279 to 217; executable but
wrong answers therefore rise from 112 to 203. The main observed failure is
semantic accuracy/robustness, not merely SQL execution failure. Public-domain
adaptation with loss of private robustness is a supported interpretation;
the exact cause (schedule, domain, objective, or evidence channel) is not isolated.

## Reverse direction: BIRD-private / Spider-public

| Arm | BIRD EX (%) | EM (%) | n |
|---|---:|---:|---:|
| Pure FL T1 | 22.88 | 1.56 | 1,534 |
| Matched Spider gold CE | 20.73 | 3.78 | 1,534 |
| Spider SeqKD | 24.45 | 4.30 | 1,534 |

SeqKD corrects 175 FL errors and loses 151 FL successes (net +24); matched
gold corrects 144 and loses 177 (net −33). The modest SeqKD gain is not
exclusive to BIRD-as-public data. Reverse Hinton has not been run.

## Earlier Spider ladder reconciliation

Earlier Pure FL/SeqKD EX 56.96/57.64 becomes 57.35/57.93 in the headline
rerun. Prompts and row alignment are identical. Predicted SQL changes in
86/58 rows; EX transitions are 7 wins/3 losses and 6 wins/3 losses.
Evaluation batch size changes from 8 to 16. This is a documented evaluation
difference, not proof that batching is its sole cause. Use the shared
batch-size-16 suite for present comparisons; preserve older rows as a separate
evaluation lineage. Do not attribute these rerun differences to training.

## Next decision

1. Implement and smoke the terminal private update with explicit parent
   adapter fingerprint and a new output root.
2. Run two independent arms: `A→A` from shared Pure FL T1 and `A→K→A` from
   Hinton T1. Each adds one local epoch per client and one FedAvg; no new
   teacher cache is needed. This matches private compute, not total KD cost.
3. Evaluate both on the same five sets, batch size 16. Check restored
   Spider/variant EX against both FL T1 and `A→A`, plus retained BIRD benefit.
4. If promising, add `A→gold CE→A` to isolate whether the final benefit still
   needs teacher supervision. Only then expand seeds/rounds or KD objectives.

This is exploratory method selection on development sets. Freeze the recipe
before final robustness evaluation; do not present repeated dev-guided choices
as independent held-out confirmation. One extra epoch is the first test;
three epochs are conditional on its outcome. The current round CLI rejects
round-1 initialization from a supplied adapter and requires same-root lineage
for later rounds, so a documented implementation is needed before launch.

## Artifact map

Paths below are under `fedicl-sql/experiments/eval_arms/results/`; each directory
contains `config.json`, `metrics.json`, and per-arm prediction CSVs.

| Evaluation | Headline directory | Full-gold CE directory |
|---|---|---|
| Spider | `eval_arms__s0__20260913T122834` | `eval_arms__s0__20260915T055906` |
| Realistic | `eval_arms__s0__20260913T124007` | `eval_arms__s0__20260915T060130` |
| SYN | `eval_arms__s0__20260913T125953` | `eval_arms__s0__20260915T060559` |
| DK | `eval_arms__s0__20260913T131303` | `eval_arms__s0__20260915T060854` |
| BIRD | `eval_arms__s0__20260913T141554` | `eval_arms__s0__20260915T062256` |

Reverse ladder: `eval_arms__s0__20260912T220957`. Teacher variants:
`eval_arms__s0__20260913T144510` (Realistic),
`eval_arms__s0__20260913T155617` (SYN), and
`eval_arms__s0__20260913T163445` (DK).
