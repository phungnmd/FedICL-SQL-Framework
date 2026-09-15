# FedLS-SQL — protocol-v2 paper result tables

Published P2.2 evidence checked 2026-09-15. Source paths, comparison limits,
and paired counts: [P22_TRANSFER_REVIEW.md](P22_TRANSFER_REVIEW.md).

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

EX is primary. EM is reported only as a secondary SQL-form diagnostic. The
final method remains under selection. Hinton improves on full-gold CE on four
sets, but does not preserve FL robustness on Realistic/SYN. Next is terminal
private consolidation `A→K→A` versus matched-private-budget `A→A`.

## Independent retained evidence

Resource, communication, Secure Sum compatibility, and Spider-only federated
optimizer tables will be restored after their lineage audit. No old
BIRD-dependent accuracy value is copied into this file.
