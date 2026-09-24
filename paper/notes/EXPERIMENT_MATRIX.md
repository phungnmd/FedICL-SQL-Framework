# FedLS-SQL — protocol-v2 experiment matrix

| Priority | Question | Minimum comparison | Status / gate |
|---|---|---|---|
| P0 | Is the BIRD setup dataset-correct? | full-context with-evidence baseline, fail-closed retention, raw-SQL EX | P2.1R accepted; original release explicitly identified |
| P0 | Does FL preserve useful accuracy? | centralized vs matched pure FL within Spider and BIRD | published; state private-training budgets |
| P0 | Does public LLM guidance add EX? | FL vs public-gold CE vs teacher-target CE vs CE+soft-KD | published; Hinton wins four sets against full-gold but loses FL robustness |
| P0 | Is the result direction-dependent? | BIRD→Spider and Spider→BIRD with explicit roles/profiles | both CE/SeqKD ladders published; reverse SeqKD +1.57 pp; reverse Hinton untested |
| P0 | Can a final private stage retain both domains? | `A→A` vs `A→K→A`, one additional local epoch | passed at seed 0: terminal Hinton wins all five absolute comparisons; Realistic paired delta remains uncertain |
| P0 | Does the final stage retain Hinton soft-logit value? | `A→K[ce]→A` vs `A→K[fkl]→A` | complete: no reliable advantage on any set; four-set mean +0.05 pp |
| P0 | Was one public epoch insufficient? | full-public `A→K2[ce]` vs `A→K2[fkl]`, then identical terminal A | closed for the current queue; repeated flat public training is not prioritized after the teacher-signal gates |
| P0 | Does sequence-level teacher signal survive the final stage? | selected-row matched gold `A→K[ce]→A` vs SeqKD `A→K[seq]→A` | P2.6 complete and published at nested `fb2329e`; SeqKD did not clear the promotion gate strongly enough to scale unchanged |
| P0 | Does the public SeqKD generalization edge survive terminal A? | same parents: `A>K[seq]>A[ret]` vs `A>K[gold]>A[ret]`, plus student NLL on teacher vs gold SQL | active P2.9; public edge is +1.64/+2.76/+3.38/+2.43/+3.00 on all five sets, plain terminal A erases most of it |
| P0 | Does structured teacher KD beat gold training and survive terminal A? | same 1,000 teacher-admitted rows: source-gold CE vs teacher plan+SQL, before and after identical A | superseded by P2.10 (its final endpoint is SQL-only); runbook archived in `archive/superseded_runbooks/P28_STRUCT_GOLD_GATE_DEFERRED_2026-09-24.md` |
| P0 | Does Struct-SQL QP-CoT KD beat gold training when every stage uses the plan format? | same FL `A[qp]` parent and 1,000 admitted rows: template+gold vs template+teacher SQL vs teacher plan+SQL, each followed by identical `A[qp]`; FL control `A[qp]>A[qp]` | P2.10 implemented (`d66af7a`), runs after P2.9; terminal teacher−gold decides |
| P1 | Does teacher plan explain any confirmed gain beyond formatting? | same teacher SQL: flat SeqKD vs local AST plan vs teacher plan | former P2.7 public-only screen retained as a secondary diagnostic; not the method gate |
| P1 | Does a stronger frozen teacher help? | zero-shot (P2.10 baseline) vs Struct-SQL 2-shot teacher prompt; later a cross-fitted QLoRA teacher | deferred; only if P2.10 shows the teacher is the bottleneck (see PIPELINE_NEXT deferred teacher options) |
| P0 | Where should LLM KD enter the federated pipeline? | R = 4 private rounds: sequential `A→K→A³`, K-first `K→A⁴`, merge `A⁴+λτ_K`, replay `A_mix⁴`, each SeqKD vs gold, against FL `A⁴` | planned; P2.9 D1 (task arithmetic) picks the first two designs |
| P1 | Can repeated transfer move the Pareto frontier? | depth/recurrent schedule using the teacher channel that passes the causal gate | deferred; do not repeat Hinton unchanged |
| P1 | Is it reliable? | at least two training seeds and paired EX/error analysis | after method gate |
| P1 | Is it robust to heterogeneity? | one stronger non-IID split, same rows/budget | after method gate |
| P1 | Is it model-family specific? | Qwen primary; Gemma only after primary method stabilizes | conditional |
| P1 | What efficiency/privacy claim survives? | audited adapter bytes, final SLM/teacher inference, structural boundary | teacher-only timing retained; final-adapter benchmark pending |

EX is primary. EM is secondary. Protocol-v1 method results are historical
no-knowledge evidence and cannot fill protocol-v2 cells.
