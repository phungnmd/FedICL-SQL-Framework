# FedLS-SQL — protocol-v2 paper result tables

Accuracy tables are intentionally empty until the dataset-correct rerun. The
previous tables are preserved at
`paper/archive/protocol_v1_no_bird_evidence/MAIN_RESULTS_v1.md`.

## Main accuracy table

| Direction / dataset | Base | Centralized | FL | Public gold CE | Teacher-target CE | Target CE + RKL | Final selected method |
|---|---:|---:|---:|---:|---:|---:|---:|
| Spider in-domain | PENDING | PENDING | PENDING | — | — | — | PENDING |
| BIRD in-domain, with evidence | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| BIRD public → Spider private/eval | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |
| Spider public → BIRD private/eval | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING | PENDING |

EX is primary. EM is reported only as a secondary SQL-form diagnostic. The
rightmost method is selected after matched protocol-v2 evidence; it is not
preassigned to RKL, FedAvg, or any other optional component.

## Independent retained evidence

Resource, communication, Secure Sum compatibility, and Spider-only federated
optimizer tables will be restored after their lineage audit. No old
BIRD-dependent accuracy value is copied into this file.
