# P2.3 terminal private consolidation review

Nested result commit: `2a6e04c`. Producer commit: `362aced`. All rows use
Qwen2.5-1.5B, training seed 0, greedy `k=0`, and the protocol-v2 dataset
profiles/evaluators. EX is the primary metric.

## Endpoint ladder

`A` is one Spider-private client epoch plus factor-wise FedAvg. `K[fkl]` is
one full 9,428-row BIRD-public server stage with evidence, gold-prefix CE, and
Hinton forward KL (`lambda_ft=lambda_kd=0.5`, `T=2`).

| Evaluation | n | `A` | `A>K[fkl]` | `A>A` | `A>K[fkl]>A` |
|---|---:|---:|---:|---:|---:|
| Spider | 1,034 | 57.35 | 58.32 | 62.57 | **66.63** |
| Realistic | 508 | 54.92 | 42.72 | 55.31 | **57.09** |
| SYN | 1,034 | 49.32 | 44.58 | 52.22 | **55.32** |
| DK | 535 | 45.23 | 45.42 | 47.10 | **50.65** |
| BIRD dev, evidence | 1,534 | 14.80 | **36.70** | 16.49 | **31.03** |

The final private stage restores Spider-domain robustness without erasing the
public-domain signal. Relative to matched-private-compute `A>A`, the terminal
Hinton chain gains 4.06/1.78/3.10/3.55/14.54 EX points on
Spider/Realistic/SYN/DK/BIRD. Relative to public-terminal `A>K[fkl]`, it gains
8.31/14.37/10.74/5.23 points on the four Spider-family evaluations and loses
5.67 points on BIRD.

## Paired EX evidence

Exact two-sided McNemar tests use the committed row-matched predictions.

| Evaluation | `A>K>A` wins / losses vs `A>A` | Delta (pp) | p |
|---|---:|---:|---:|
| Spider | 88 / 46 | +4.06 | 0.000359 |
| Realistic | 42 / 33 | +1.77 | 0.3557 |
| SYN | 85 / 53 | +3.09 | 0.00808 |
| DK | 39 / 20 | +3.55 | 0.01834 |
| BIRD dev | 259 / 36 | +14.54 | < 1e-40 |

This is strong seed-0 evidence, not a multi-seed reliability claim. The
Realistic difference against `A>A` is positive but not individually
significant.

## Teacher gap and claim boundary

| Evaluation | Pure FL `A` | Final student `A>K>A` | Teacher 7B | FL-to-teacher gap closed |
|---|---:|---:|---:|---:|
| Spider | 57.35 | 66.63 | 76.69 | 48.0% |
| Realistic | 54.92 | 57.09 | 71.06 | 13.4% |
| SYN | 49.32 | 55.32 | 63.83 | 41.4% |
| DK | 45.23 | 50.65 | 62.43 | 31.5% |
| BIRD dev | 14.80 | 31.03 | 47.07 | 50.3% |

The paper target is not restricted to matching centralized SFT. It asks how
much of the teacher-quality gap a federated 1.5B student can recover while
retaining the communication/resource advantages of the student. Do not claim
teacher parity from the current result; report absolute teacher gaps and the
fraction closed.

## Cost and unresolved cause

`A>A` and `A>K>A` add the same terminal private round: 369,555,560 client-upload
bytes and 369,555,400 broadcast bytes. Concurrent shared-server wall time is
not paper-comparable. Hinton still mixes public-gold CE with soft-logit KD, so
the next causal control is `A>K[ce]>A`. Only after that control may the final
gain be attributed specifically to teacher logits.

The next schedule question separates:

- `A>K>A[e3]`: one terminal client stage with three local epochs followed by
  one FedAvg, matching the cited medical-style consolidation pattern;
- `A>K>A>K>A`: a second public-transfer/private-consolidation cycle;
- `A>K>A>A` and `A>A>A`: controls for extra private training without the
  second public KD stage.

Evaluate the intermediate `A>K>A>K` checkpoint. If BIRD rises and Spider falls,
then the final `A` merely reverses domain drift; a useful recurrent method must
move the final Pareto frontier beyond `A>K>A`, not just oscillate between two
domains.
