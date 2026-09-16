# FedLS-SQL — protocol-v2 experiment matrix

| Priority | Question | Minimum comparison | Status / gate |
|---|---|---|---|
| P0 | Is the BIRD setup dataset-correct? | full-context with-evidence baseline, fail-closed retention, raw-SQL EX | P2.1R accepted; original release explicitly identified |
| P0 | Does FL preserve useful accuracy? | centralized vs matched pure FL within Spider and BIRD | published; state private-training budgets |
| P0 | Does public LLM guidance add EX? | FL vs public-gold CE vs teacher-target CE vs CE+soft-KD | published; Hinton wins four sets against full-gold but loses FL robustness |
| P0 | Is the result direction-dependent? | BIRD→Spider and Spider→BIRD with explicit roles/profiles | both CE/SeqKD ladders published; reverse SeqKD +1.57 pp; reverse Hinton untested |
| P0 | Can a final private stage retain both domains? | `A→A` vs `A→K→A`, one additional local epoch | passed at seed 0: terminal Hinton wins all five absolute comparisons; Realistic paired delta remains uncertain |
| P0 | Does the final stage retain Hinton soft-logit value? | `A→K[ce]→A` vs `A→K[fkl]→A` | complete: no reliable advantage on any set; four-set mean +0.05 pp |
| P0 | Was one public epoch insufficient? | full-public `A→K2[ce]` vs `A→K2[fkl]`, then identical terminal A | active P2.4c; same FL parent and 9,428 rows, two epochs planned from step zero |
| P0 | Does sequence-level teacher signal survive the final stage? | selected-row matched gold `A→K[ce]→A` vs SeqKD `A→K[seq]→A` | deferred after matched K2; same 5,319 rows and terminal private compute |
| P1 | Can repeated transfer move the Pareto frontier? | depth/recurrent schedule using the teacher channel that passes the causal gate | deferred; do not repeat Hinton unchanged |
| P1 | Is it reliable? | at least two training seeds and paired EX/error analysis | after method gate |
| P1 | Is it robust to heterogeneity? | one stronger non-IID split, same rows/budget | after method gate |
| P1 | Is it model-family specific? | Qwen primary; Gemma only after primary method stabilizes | conditional |
| P1 | What efficiency/privacy claim survives? | audited adapter bytes, final SLM/teacher inference, structural boundary | teacher-only timing retained; final-adapter benchmark pending |

EX is primary. EM is secondary. Protocol-v1 method results are historical
no-knowledge evidence and cannot fill protocol-v2 cells.
