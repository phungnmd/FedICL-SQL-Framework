# FedLS-SQL — protocol-v2 experiment matrix

| Priority | Question | Minimum comparison | Status / gate |
|---|---|---|---|
| P0 | Is the BIRD setup dataset-correct? | full-context with-evidence baseline, fail-closed retention, raw-SQL EX | old P2.1 rejected; P2.1R ready |
| P0 | Does FL preserve useful accuracy? | centralized vs matched pure FL within Spider and BIRD | pending P2.1R |
| P0 | Does public LLM guidance add EX? | FL vs public-gold CE vs teacher-target CE vs CE+soft-KD | pending P2.2 |
| P0 | Is the result direction-dependent? | BIRD→Spider and Spider→BIRD with explicit roles/profiles | pending P2.2 |
| P1 | What is the final mechanism? | matched ablation selected after v2 failure analysis | adaptive P2.3 |
| P1 | Is it reliable? | at least two training seeds and paired EX/error analysis | after method gate |
| P1 | Is it robust to heterogeneity? | one stronger non-IID split, same rows/budget | after method gate |
| P1 | Is it model-family specific? | Qwen primary; Gemma only after primary method stabilizes | conditional |
| P1 | What efficiency/privacy claim survives? | audited adapter bytes, final SLM/teacher inference, structural boundary | teacher-only timing retained; final-adapter benchmark pending |

EX is primary. EM is secondary. Protocol-v1 method results are historical
no-knowledge evidence and cannot fill protocol-v2 cells.
