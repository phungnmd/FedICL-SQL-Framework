# FedLS-SQL result registry

This is the canonical presentation-name-to-checkpoint map. Internal artifact
paths are immutable even when the paper terminology changes.

| Paper label | Canonical checkpoint | Spider EX | Spider EM | Spider exec. error | Realistic EX | Syn EX | DK EX | BIRD dev EX |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| `Centralized` | `artifacts/probe_p/central_3ep/adapter` | 67.60 | 62.67 | 15.76% | 57.87 | 53.19 | 52.52 | 12.91 |
| `FL` | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter` | pending | pending | pending | pending | pending | pending | pending |
| `FedLS-SQL` (`FL-KD`) | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g` | 69.54 | 38.59 | 9.77% | 59.65 | 55.51 | 52.71 | 21.58 |

Notes:

- All values use greedy decoding at `k=0`, seed 0.
- EM is comparable only within the same training stage because server KD changes
  SQL surface convention.
- Fill the `FL` row only from Block K in `PIPELINE_NEXT.md`. The 66.05
  adapter inherits the distilled round-2 global adapter and is not FL-only.
- BIRD dev is a cross-corpus transfer evaluation, not a headline benchmark.
- Old names such as `fedkd`, `noicl`, or `fedicl` inside paths are provenance
  identifiers and must not be rewritten.
