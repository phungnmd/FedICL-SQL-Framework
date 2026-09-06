# FedLS-SQL — valid results, adapters, and missing controls

This is the compact active evidence ledger. A row is retained only when its
accuracy lineage does not consume BIRD prompts/targets that omitted evidence or
the truncated-context P2.1 trained adapters. EX is primary; EM is secondary.
Archived mixed result directories may still contain an individually valid
Spider-only arm listed below.

## Valid evaluation results already available

| Model | Dataset/setup | Method | Seed | Stage | EX (%) | EM (%) | n | Use |
|---|---|---|---:|---|---:|---:|---:|---|
| Qwen2.5 1.5B | Spider | Base | 0 | — | 50.00 | 21.08 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Centralized, continuous 3 epochs | 0 | E3 | 67.31 | 64.41 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 0 | T1 | 56.67 | 50.39 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 0 | T2 | 62.19 | 55.13 | 1,034 | convergence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 0 | T3 | 64.31 | 57.45 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 1 | T1 | 57.45 | 50.58 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 1 | T2 | 61.70 | 53.97 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 1 | T3 | 61.99 | 54.74 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 2 | T1 | 59.77 | 52.32 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider, `alpha=0.1` | Pure FedAvg | 0 | T1 | 58.90 | 50.68 | 1,034 | skew control |
| Qwen2.5 1.5B | Spider, `alpha=0.1` | Pure FedAvg | 0 | T3 | 63.64 | 57.74 | 1,034 | skew control |
| Qwen2.5 1.5B | Spider | FedProx `mu=0.01` | 0 | T1 | 55.80 | 49.42 | 1,034 | negative optimizer ablation |
| Qwen2.5 1.5B | Spider | FedProx `mu=0.01` | 0 | T2 | 59.96 | 52.90 | 1,034 | negative optimizer ablation |
| Qwen2.5 1.5B | Spider | FedProx `mu=0.01` | 0 | T3 | 62.77 | 56.00 | 1,034 | negative optimizer ablation |
| Gemma 2 2B | Spider | Base | 0 | — | 52.22 | 22.44 | 1,034 | second-family anchor |
| Gemma 2 2B | Spider | Pure FedAvg | 0 | T1 | 57.16 | 49.52 | 1,034 | second-family FL baseline |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Base | 0 | — | 15.97 | 2.09 | 1,534 | valid inference-only anchor |

The BIRD base row is anchored by independent rescore `e9bde43`. The archived
P2.1 Centralized E1/E2 and FL T1–T3 scores are deliberately absent because
their training prompts were truncated.

### Valid Spider out-of-domain results

| Method | Stage | Realistic EX/EM | Syn EX/EM | DK EX/EM |
|---|---|---:|---:|---:|
| Centralized continuous 3 epochs | E3 | 55.91 / 53.54 | 54.06 / 49.90 | 53.27 / 47.29 |
| Pure FedAvg, seed 0 | T1 | 53.35 / 44.88 | 48.84 / 41.49 | 45.42 / 38.13 |
| Pure FedAvg, seed 0 | T2 | 55.51 / 48.03 | 51.74 / 45.26 | 47.10 / 41.31 |
| Pure FedAvg, seed 0 | T3 | 56.10 / 50.00 | 51.93 / 46.03 | 46.73 / 42.43 |

## Valid adapter inventory

These paths refer to the experiment server; adapters are gitignored. Only the
listed stages may be reused. A `round_N/fedavg_adapter` inside an old FedLS root
is not listed, because later rounds inherit invalid public supervision.

| Stable role | Valid adapter path | Scope |
|---|---|---|
| Qwen centralized E3 | `artifacts/baselines/central_3ep_standard_s0/adapter` | Spider only |
| Qwen pure FL seed 0, T1–T3 | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_{1,2,3}/fedavg_adapter` | Spider only |
| Qwen pure FL seed 1, T1–T3 | `artifacts/federated/fedavg_noicl_k5_e1_t1_s1/round_{1,2,3}/fedavg_adapter` | Spider only |
| Qwen pure FL seed 2, T1 | `artifacts/federated/fedavg_noicl_k5_e1_t1_s2/round_1/fedavg_adapter` | Spider only |
| Qwen FedProx seed 0, T1–T3 | `artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0/round_{1,2,3}/fedavg_adapter` | Spider negative ablation |
| Qwen `alpha=0.1`, T1 | `artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1/fedavg_adapter` | Spider skew baseline |
| Qwen `alpha=0.1`, T2–T3 | `artifacts/federated/p13_alpha01_k5_e1_t1_fl_s0/round_{2,3}/fedavg_adapter` | Spider skew baseline |
| Gemma pure FL seed 0, T1 | `artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` | Spider only |

There is currently no valid trained BIRD, SeqKD, RKL, or FedLS adapter. Base
models are valid anchors but are not adapters.

## Baselines and ablations still required

Order is adaptive: do not start a lower row when its gate is unresolved.

| Order | Required comparison | Status / promotion gate |
|---:|---|---|
| 1 | BIRD full-context smoke on eight longest prompts | ready; must fit GPU 0 and trigger zero truncation |
| 2 | BIRD Centralized E1/E2 and pure FL T1/T2/T3 | pending P2.1R; establishes valid in-domain baseline |
| 3 | Spider Base / Centralized / pure FL under explicit `spider` profile | reuse audit first; rerun only if fingerprints cannot be reconciled |
| 4 | Pure FL vs matched public-gold CE | pending; control for extra public optimization/data |
| 5 | Pure FL vs teacher-target CE (SeqKD) | pending; isolates hard teacher targets generated with BIRD evidence |
| 6 | Teacher-target CE vs teacher-target CE + RKL | pending; isolates soft-logit value using a regenerated evidence-aware cache |
| 7 | T1 vs recurring T2/T3 server transfer | run only if the matched T1 ladder improves EX |
| 8 | Reverse direction: BIRD-private FL with Spider-public controls | after valid BIRD baseline and main direction |
| 9 | Final method on `alpha=0.1` and a second training seed | after method selection |
| 10 | Second model family and final-adapter resource benchmark | conditional paper-closure evidence |

Secure Sum equivalence and teacher-only resource measurements remain valid
technical evidence. They are not accuracy arms and do not replace rows 1–10.

## Excluded lineage

All old Qwen/Gemma FedLS, SeqKD, public-gold, RKL, mixed pre-server, and BIRD
trained-arm results are archived. Their teacher targets/logits either omitted
BIRD evidence or inherited such a server update. P2.1 trained arms are also
archived because `max_len=2560` truncated required context. None may be copied
back into an active table or used to initialize protocol-v2 training.
