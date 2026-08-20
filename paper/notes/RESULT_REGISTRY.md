# FedLS-SQL result registry

This is the canonical presentation-name-to-checkpoint map. Internal artifact
paths are immutable even when the paper terminology changes.

| Paper label | Canonical checkpoint | Spider EX | Spider EM | Spider exec. error | Realistic EX | Syn EX | DK EX | BIRD dev EX |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `Centralized-standard-3ep` (official) | `artifacts/baselines/central_3ep_standard_s0/adapter` | 67.31 | 64.41 | 14.31% | — | — | — | — |
| `Centralized-3pass-restart` (schedule sensitivity) | `artifacts/probe_p/central_3ep/adapter` | 67.60 | 62.67 | 15.76% | 57.87 | 53.19 | 52.52 | 12.91 |
| `FL` | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter` | 64.31 | 57.45 | 18.67% | 56.10 | 51.93 | 46.73 | 12.91 |
| `FedLS-SQL` (`FL-KD`) | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g` | 69.54 | 38.59 | 9.77% | 59.65 | 55.51 | 52.71 | 21.58 |

Notes:

- All values use greedy decoding at `k=0`, seed 0.
- The official standard and restart recipes are indistinguishable in paired
  Spider EX (`0.29 pp`, `p=0.863`). Standard is selected for conventional
  methodology; its OOD cells remain unevaluated rather than borrowing restart
  results.
- EM is comparable only within the same training stage because server KD changes
  SQL surface convention.
- The FL row comes from the independent `fedavg` setup
  `229fe736042acd80df29a19e577963e4f69a5e6bb62d41ac5964fbeee9f629d2`.
  The 66.05 adapter inside the FedKD lineage is not FL-only.
- BIRD dev is a cross-corpus transfer evaluation, not a headline benchmark.
- Old names such as `fedkd`, `noicl`, or `fedicl` inside paths are provenance
  identifiers and must not be rewritten.

## Matched T1 supervision ladder

All four seed-0 arms start from the same T1 FedAvg adapter and are evaluated on
the same 1,034 Spider rows.

| Paper label | Canonical checkpoint | EX | EM | Exec. error |
|---|---|---:|---:|---:|
| `FL-T1-shared` | `artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` | 57.35 | 50.58 | 22.82% |
| `FL + matched public-gold CE` | `artifacts/federated/fedavg_pub_gold_noicl_k5_e1_t1_s0/round_1/m_g` | 57.83 | 23.89 | 18.86% |
| `FL + teacher-target CE` | `artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g` | 61.32 | 30.27 | 15.57% |
| `FedLS-SQL-T1` | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g` | **63.35** | 31.53 | **12.86%** |

Canonical committed evaluation:
`fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954/`
(`git_sha=b3fd32f`, committed by `7c1414b`). The decisive paired EX contrasts
are teacher target over public gold `+3.48 pp` (`p=0.0026`) and full FedLS-SQL
over public gold `+5.51 pp` (`p<1e-6`). Question-level tests at one training
seed are not across-seed method significance.
