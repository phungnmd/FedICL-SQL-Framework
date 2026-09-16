# P2.4 teacher-signal review

Nested result commit: `ccb3e91`. Both endpoints start from the same Spider
private `A`, use one full 9,428-row BIRD-public epoch with evidence, and end in
the same one-epoch Spider-private/FedAvg stage. `K[ce]` uses public gold CE;
`K[fkl]` uses `0.5 CE + 0.5 T² KL(teacher || student)` at `T=2`.

## Full-public terminal comparison

All values are seed-0 EX (%).

| Evaluation | n | `A>K[ce]>A` | `A>K[fkl]>A` | Hinton − CE (pp) |
|---|---:|---:|---:|---:|
| Spider | 1,034 | 66.54 | 66.63 | +0.09 |
| Realistic | 508 | 57.28 | 57.09 | −0.19 |
| SYN | 1,034 | 54.45 | 55.32 | +0.87 |
| DK | 535 | 51.21 | 50.65 | −0.56 |
| BIRD dev, evidence | 1,534 | 29.53 | 31.03 | +1.50 |

The unweighted four-set Spider-family mean is 57.37 for CE and 57.42 for
Hinton, a difference of only +0.05 point.

## Paired EX

Exact two-sided McNemar tests use the committed row-matched predictions.

| Evaluation | Hinton wins / CE wins | Delta (pp) | p |
|---|---:|---:|---:|
| Spider | 52 / 51 | +0.10 | 1.000 |
| Realistic | 29 / 30 | −0.20 | 1.000 |
| SYN | 58 / 49 | +0.87 | 0.439 |
| DK | 18 / 21 | −0.56 | 0.749 |
| BIRD dev | 102 / 79 | +1.50 | 0.102 |

No evaluation demonstrates a statistically reliable Hinton advantage. The
terminal chain remains a strong public-training-plus-private-consolidation
result, but the current evidence does **not** attribute that gain to soft
teacher logits.

## Decision

Do not launch recurrent Hinton or `K2[fkl]` alone. First test whether the other
standard teacher channel survives terminal consolidation: append the same
private `A` to the published 5,319-row SeqKD and matched-gold parents. This
holds selected rows, private compute, aggregation, and evaluation fixed while
changing teacher-generated versus gold SQL targets. The two parent configs
differ only in `pool` and stage label; source-row ID, database, question, and
evidence match on all 5,319 rows. Target SQL differs on 4,053 rows.

If terminal SeqKD coherently beats matched gold, schedule/depth work can follow
using that teacher channel. If it does not, pause repeated-K schedules and
design a genuinely different KD mechanism (for example on-policy GKD or
MiniLLM) with a matched no-teacher control.
