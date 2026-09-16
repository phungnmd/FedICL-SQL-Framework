# FedLS-SQL — protocol-v2 paper result tables

Published P2.2/P2.3 evidence checked 2026-09-16. Source paths, comparison
limits, and paired counts: [P22_TRANSFER_REVIEW.md](P22_TRANSFER_REVIEW.md)
and [P23_TERMINAL_CONSOLIDATION_REVIEW.md](P23_TERMINAL_CONSOLIDATION_REVIEW.md).

## Main accuracy table

Spider-private / BIRD-public, seed 0, EX (%). Student eval batch size is 16.
Central E3 has three continuous Spider epochs; FL/KD start from one local
epoch per client. Their private-training budgets differ.

| Evaluation | Central E3 | Pure FL T1 | SeqKD T1 | Full-gold CE T1 | Hinton T1 | Teacher 7B |
|---|---:|---:|---:|---:|---:|---:|
| Spider | 67.31 | 57.35 | 57.93 | 55.03 | 58.32 | 76.69 |
| Realistic | 55.91 | 54.92 | 46.65 | 47.05 | 42.72 | 71.06 |
| SYN | 54.06 | 49.32 | 48.26 | 43.91 | 44.58 | 63.83 |
| DK | 53.27 | 45.23 | 45.61 | 40.93 | 45.42 | 62.43 |
| BIRD dev, evidence | 17.73 | 14.80 | 34.68 | 32.14 | 36.70 | 47.07 |

SeqKD uses 5,319 selected teacher targets. Full-gold CE and Hinton use all
9,428 BIRD public rows with gold prefixes. Hinton loss is
`0.5 CE + 0.5 T² KL(teacher || student)`, temperature 2.

BIRD-private / Spider-public on BIRD dev: Pure FL T1 **22.88**, matched gold
CE **20.73**, SeqKD **24.45** EX. Separately trained BIRD baselines:
base 15.97, centralized E1/E2 31.42/34.94, pure FL T1/T2/T3 22.75/28.36/31.10.

## Terminal private consolidation

Seed-0 EX (%). `A>K>A` and `A>A` add the same one-client-epoch terminal
private/FedAvg stage to their respective T1 parents.

| Evaluation | `A` | `A>K[fkl]` | `A>A` | `A>K[fkl]>A` | Teacher 7B |
|---|---:|---:|---:|---:|---:|
| Spider | 57.35 | 58.32 | 62.57 | **66.63** | 76.69 |
| Realistic | 54.92 | 42.72 | 55.31 | **57.09** | 71.06 |
| SYN | 49.32 | 44.58 | 52.22 | **55.32** | 63.83 |
| DK | 45.23 | 45.42 | 47.10 | **50.65** | 62.43 |
| BIRD dev, evidence | 14.80 | **36.70** | 16.49 | **31.03** | 47.07 |

The terminal Hinton chain beats matched-compute `A>A` on all five evaluations,
with paired significance on Spider, SYN, DK, and BIRD. It closes
13.4%–50.3% of the Pure-FL-to-teacher gap depending on the evaluation, but is
not teacher-parity evidence. One seed is insufficient for a reliability claim.

EX is primary. EM is reported only as a secondary SQL-form diagnostic. The
method remains under selection until `A>K[ce]>A` isolates soft-logit value.
After that control, compare stronger terminal-local consolidation with a true
recurrent `A>K>A>K>A` schedule and matched private-training controls.

## Independent retained evidence

Resource, communication, Secure Sum compatibility, and Spider-only federated
optimizer tables will be restored after their lineage audit. No old
BIRD-dependent accuracy value is copied into this file.
