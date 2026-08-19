# Fed-ICL-KD: Full-Pipeline Evaluation

The proposed **Fed-ICL-KD** method combines client-side ICL fine-tuning,
federated aggregation, and server-side knowledge distillation. We compare it
with a non-ICL ablation, the untrained base model, and centralized fine-tuning
as a privacy-relaxed upper reference. All results use Qwen2.5-1.5B-Instruct and
the full Spider development set (`n=1,034`). Evaluations with `k=3` use
DAIL-weighted retrieval from the full centralized Spider training pool.

## Main Results

| Role | System | Training pipeline | Evaluation | EX ↑ | EM ↑ | Exec. error ↓ |
|---|---|---|---|---:|---:|---:|
| Base reference | Base, `evalk0` | None | `k=0` | 50.00 | 21.08 | 25.92% |
| Base reference | Base, `evalk3` | None | `k=3` | 52.22 | 29.30 | 23.98% |
| Centralized upper reference | Centralized FT, `traink0/evalk0` | All Spider train data, no federation | `k=0` | 62.19 | **57.16** | 20.41% |
| Centralized upper reference | Centralized FT, `traink3/evalk3` | All Spider train data, ICL `k=3`, no federation | `k=3` | 58.61 | 50.77 | 20.12% |
| Non-ICL ablation | Fed-KD, `traink0/evalk0` | Client `k=0` → FedAvg → server KD | `k=0` | **63.35** | 31.53 | **12.86%** |
| **Proposed method** | **Fed-ICL-KD, `traink3/evalk3`** | Client `k=3` → FedAvg → server KD | `k=3` | 59.38 | 28.53 | 15.86% |

Fed-ICL-KD improves over the matched `k=3` base by **7.16 EX points**. However,
the non-ICL ablation is **3.97 EX points** higher than Fed-ICL-KD and has fewer
execution errors. This isolates ICL as the component that does not improve the
current full pipeline.

## Centralized Upper-Reference Matrix

Centralized FT is not part of the proposed method. It is a privacy-relaxed
reference that fine-tunes on the complete Spider training set without
federation. `traink0` and `traink3` identify its prompt condition during
fine-tuning. The historical `central_traink3` checkpoint was trained with DAIL
Select, while its `k=3` evaluation uses DAIL Weighted.

| Centralized model | `eval k=0` | `eval k=3` | Effect of adding demos |
|---|---:|---:|---:|
| `central_traink0` | 62.19 | 61.32 | −0.87 EX |
| `central_traink3` | **64.02** | 58.61 | −5.41 EX |

In-context training improves the centralized model when both checkpoints are
evaluated without demonstrations (`+1.83 EX`). It does not improve the matched
ICL setting: `central_traink3/evalk3` is 3.58 EX below
`central_traink0/evalk0`.

## Fed-ICL-KD Inference Ablation

| Trained model | `eval k=0` | `eval k=3` | ICL inference effect |
|---|---:|---:|---:|
| Fed-ICL-KD, `traink3_fedavg_kd` | **64.02** | 59.38 | −4.64 EX |

Although this model was trained with ICL, adding three demonstrations at
inference reduces its execution accuracy by 4.64 points.

## Execution Accuracy by Difficulty

| System | Easy | Medium | Hard | Extra hard |
|---|---:|---:|---:|---:|
| Base, `evalk0` | 67.74 | 54.71 | 36.78 | 24.70 |
| Base, `evalk3` | 68.55 | 56.73 | 39.66 | 28.92 |
| Centralized FT, `traink0/evalk0` | 87.50 | 62.33 | 45.98 | 40.96 |
| Centralized FT, `traink0/evalk3` | **88.31** | 62.56 | **51.72** | 27.71 |
| Centralized FT, `traink3/evalk0` | 86.29 | **65.92** | 47.70 | **42.77** |
| Centralized FT, `traink3/evalk3` | 83.87 | 62.11 | 44.83 | 25.90 |
| **Fed-ICL-KD, `traink3/evalk3`** | 80.65 | 62.78 | 44.25 | 34.34 |
| Fed-KD ablation, `traink0/evalk0` | 86.29 | 64.13 | **51.72** | 39.16 |

The non-ICL federated pipeline is stronger than the ICL federated pipeline at
every Spider difficulty level. Centralized ICL evaluation also declines most
sharply on extra-hard questions.
