# Closed FedLS-SQL method branches

This directory preserves post-refactor method experiments that passed a
technical or small-scale screen but failed their final preregistered promotion
gate. They remain reproducibility evidence and negative ablations, not active
paper components or sources of commands to run next.

| Archive | Scope | Decision |
|---|---|---|
| `PIPELINE_THROUGH_P010E_2026-08-25.md` | completed P0.0–P0.10 commands, including P0.9 selection and P0.10 FedDF | P0.9 and P0.10 closed; current method frozen |
| `P017A_PREFERENCE_KD_2026-08-28.md` | fixed 512-row execution-verified global-model preference-KD screen | closed negative: 54.9 vs 56.9 EX; no tuning or full extension |

Closed code and large row-level predictions may be removed from the active
tree after a compact evidence record and a recovery commit/tag exist. P0.10 is
recoverable in the nested repository from tag `archive/p010-feddf-evidence`;
its compact evidence is under
`fedicl-sql/experiments/archive/p010_feddf_2026-08/`.
P1.7a is recoverable from nested tag
`archive/p017-preference-kd-implementation`; its compact evidence is under
`fedicl-sql/experiments/archive/p017_preference_kd_2026-08/`.
