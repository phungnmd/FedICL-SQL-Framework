# FedLS-SQL — protocol-v2 experiment matrix

| Priority | Question | Minimum comparison | Status / gate |
|---|---|---|---|
| P0 | Is the BIRD setup dataset-correct? | original-release with-evidence baseline, actual token retention, raw-SQL EX rescore | P2.1 recorded; acceptance pending P2.1q |
| P0 | Does FL preserve useful accuracy? | centralized vs matched pure FL within Spider and BIRD | pending P2.1 |
| P0 | Does public LLM guidance add EX? | FL vs public-gold CE vs teacher-target CE vs CE+soft-KD | pending P2.2 |
| P0 | Is the result direction-dependent? | BIRD→Spider and Spider→BIRD with explicit roles/profiles | pending P2.2 |
| P1 | What is the final mechanism? | matched ablation selected after v2 failure analysis | adaptive P2.3 |
| P1 | Is it reliable? | at least two training seeds and paired EX/error analysis | after method gate |
| P1 | Is it robust to heterogeneity? | one stronger non-IID split, same rows/budget | after method gate |
| P1 | Is it model-family specific? | Qwen primary; Gemma only after primary method stabilizes | conditional |
| P1 | What efficiency/privacy claim survives? | audited adapter bytes, SLM/teacher inference, structural boundary | retained-lineage audit pending |

EX is primary. EM is secondary. Protocol-v1 method results are historical
no-knowledge evidence and cannot fill protocol-v2 cells.
