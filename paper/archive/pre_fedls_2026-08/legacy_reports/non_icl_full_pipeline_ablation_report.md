# Non-ICL Full Pipeline: Baselines and Ablations

This report evaluates the paper's recommended non-ICL pipeline:

```text
private client fine-tuning → FedAvg → server KD
```

All evaluations use Qwen2.5-1.5B-Instruct, Spider dev (`n=1,034`), greedy
decoding, and no demonstrations at training or inference (`k=0`).

The server KD step is one optimization run with a joint objective:

```text
L_server = CE(student, teacher-generated SQL)
         + RKL(student distribution || teacher distribution)
```

The CE-only result is an ablation control. It is not an intermediate
checkpoint in the full pipeline.

## Main Three-Seed Results

| System | Training path | EX ↑ | Comparison |
|---|---|---:|---:|
| Base model | No training | 50.00 | — |
| Federation only | Client FT → FedAvg | 58.19 ± 1.37 | +8.19 vs. base |
| CE-only KD control | Client FT → FedAvg → server CE | 61.03 ± 1.42 | +2.84 ± 2.74 vs. federation only |
| **Full pipeline** | Client FT → FedAvg → server KD (CE + reverse KL) | **62.74 ± 0.53** | +4.55 ± 1.75 vs. federation only |

The complete pipeline improves over the base model by **12.74 EX points**.
Across three seeds, the full server-distillation stage contributes
**+4.55 ± 1.75 EX** over FedAvg alone (`p=0.046`). The endpoint is stable even
when the CE-only and reverse-KL effects vary across seeds.

## Centralized Reference Ceiling

Centralized FT uses the complete Spider training set at one location and is
included as a privacy-relaxed reference for the non-ICL pipeline.

| System | Data setting | EX ↑ | EM ↑ | Execution-error rate ↓ |
|---|---|---:|---:|---:|
| Base model | No training | 50.00 | 21.08 | 25.92% |
| Centralized FT, `traink0/evalk0` | All Spider training data, no federation | 62.19 | **57.16** | 20.41% |
| **Non-ICL full pipeline, seed 0** | Private client FT + FedAvg + public KD | **63.35** | 31.53 | **12.86%** |
| **Non-ICL full pipeline, three seeds** | Private client FT + FedAvg + public KD | **62.74 ± 0.53** | — | — |

The full pipeline is competitive with the centralized reference: +1.16 EX at
seed 0 and +0.55 EX using the three-seed mean. Centralized FT is a reference
ceiling in terms of data access, not a strict numerical upper bound; it uses a
different training recipe and has only one retained seed.

## Component Ablation

The seed-0 ablation removes one complete component at a time while retaining
the same evaluation set.

| Configuration | EX | Drop from full pipeline | Paired `p` |
|---|---:|---:|---:|
| **Full pipeline**: client FT → FedAvg → server KD (CE + reverse KL) | **63.35** | — | — |
| Without reverse KL: client FT → FedAvg → server CE only | 61.32 | −2.03 | 0.042 |
| Without server distillation: client FT → FedAvg | 57.35 | −6.00 | 4.8×10⁻⁵ |
| Without federation: base → server KD (CE + reverse KL) | 61.22 | −2.13 | 0.017 |
| Without both components: base model | 50.00 | −13.35 | — |

Both major components are necessary. Federation alone and server distillation
alone are weaker than their combination. Public distillation provides most of
the gain, while private federated training adds a further **2.13 EX points**
over the matched server-only pipeline.

## Seed-0 Controls

| Configuration | Role | EX | EM | Execution-error rate ↓ |
|---|---|---:|---:|---:|
| Base model | Reference | 50.00 | 21.08 | 25.92% |
| Client FT → FedAvg | Federation-only ablation | 57.35 | **50.58** | 22.82% |
| Client FT → FedAvg → server CE | CE-only KD control | 61.32 | 30.27 | 15.57% |
| **Client FT → FedAvg → server KD (CE + reverse KL)** | **Full pipeline** | **63.35** | 31.53 | **12.86%** |

The full pipeline gains **13.35 EX points** and approximately halves the
execution-error rate relative to the base model.

## Execution Accuracy by Difficulty

| Configuration | Easy | Medium | Hard | Extra hard |
|---|---:|---:|---:|---:|
| Base model | 67.74 | 54.71 | 36.78 | 24.70 |
| Centralized FT, `traink0/evalk0` | **87.50** | 62.33 | 45.98 | **40.96** |
| Federation-only ablation | 78.63 | 58.30 | 45.98 | 34.94 |
| CE-only KD control | 84.68 | 62.33 | 49.43 | 36.14 |
| **Full server KD (CE + reverse KL)** | 86.29 | **64.13** | **51.72** | 39.16 |

The full pipeline improves execution accuracy at every Spider difficulty
level, with gains of +18.55, +9.42, +14.94, and +14.46 points from easy to
extra-hard questions.

## Conclusion

The non-ICL full pipeline consistently reaches approximately **62.7–63.4 EX**.
Removing server distillation costs 6.00 EX at seed 0, while removing federation
costs 2.13 EX. It is also competitive with the 62.19 EX centralized reference.
The three-seed results confirm that the combined server stage is significantly
beneficial and that the final pipeline endpoint is stable.
