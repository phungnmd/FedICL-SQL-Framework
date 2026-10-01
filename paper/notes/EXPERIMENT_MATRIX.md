# FedLS-SQL — experiment matrix

What this file is: each research question, the comparison that answers it,
and its status. It also holds the paper-closure checklist. Numbers are in
`LAB_LOG.md`; commands are in `PIPELINE_NEXT.md`.

EX is primary. EM is secondary. Protocol-v1 results never fill a cell here.

## 1. Research questions

| # | Question | Comparison | Status |
|---|---|---|---|
| 1 | Is the BIRD setup correct? | full-context with-evidence baseline, fail-closed length, official EX | done (P2.1R) |
| 2 | How much accuracy does FL lose? | centralized vs pure FL, Spider and BIRD | done; budgets differ, say so |
| 3 | Does a public teacher stage add EX? | FL vs public-gold CE vs SeqKD vs gold CE + Hinton | done (P2.2); public stage helps BIRD, hurts Spider variants |
| 4 | Does it depend on the direction? | BIRD→Spider and Spider→BIRD | done for FL/gold/SeqKD; reverse Hinton not run |
| 5 | Does a last private stage keep both domains? | `A>A` vs `A>K>A` | done (P2.3): yes at seed 0 |
| 6 | Is the gain from Hinton soft logits? | `A>K[ce]>A` vs `A>K[fkl]>A` | done (P2.4a): no |
| 7 | Is the gain from teacher SQL? | same 5,319 rows: `A>K[ce]>A` vs `A>K[seq]>A` | done (P2.6): edge at public endpoint, mostly gone after last A |
| 8 | Can a retention loss keep the teacher edge? | `A>K>A[ret]`, SeqKD vs gold | paused (P2.9): λ = 1.0 failed |
| 8a | Does a weight merge keep the teacher edge? | WiSE-FT and task arithmetic; Hinton vs full gold, SeqKD vs matched gold | **active (A1, Direction 1)** |
| 9 | Does a teacher query plan beat gold? | Struct-SQL QP-CoT in every stage with template client plans (P2.10) | stopped: QP-CoT at inference and template plans hurt the 1.5B student |
| 9a | Does the teacher plan help as an auxiliary task? | `A>K[seq+plan]>A`, teacher plan vs template plan, vs committed `A>K[seq]>A`; SQL-only inference | **in development (P2.11, Direction 2)** |
| 9b | Does a latent client plan keep the teacher's plan style? | `A[qp]>K[qp-teacher]>A[qp-latent]`, loss on SQL only at clients | **in development (P2.12, Direction 2)** |
| 10 | Does a stronger teacher help? | zero-shot vs 2-shot teacher; later a cross-fitted QLoRA teacher | deferred; only if Direction 2 shows the teacher is the bottleneck |
| 11 | Where should KD enter FL? | interleaved `(A -> k)^R` on BIRD shards vs FL `A^R` and the gold schedule | planned (A2, Direction 1), after A1 |
| 12 | Does a teacher plan add value beyond format? | flat SeqKD vs local AST plan vs teacher plan | secondary diagnostic (old P2.7) |
| 13 | Is the result reliable? | at least 2 training seeds, paired EX and error analysis | after the method gate |
| 14 | Is it robust to heterogeneity? | one stronger non-IID split, same rows and budget | after the method gate |
| 15 | Is it model-family specific? | Qwen first; Gemma only after the method is stable | conditional |
| 16 | What efficiency and privacy claims hold? | adapter bytes, final SLM vs teacher inference, structural boundary | teacher timing kept; final-adapter benchmark pending |

Closed with a negative result: KID (ties SeqKD, too costly), GKD (too costly),
the SeqKD + Hinton hybrid, repeated Hinton depth (P2.4c cancelled).
Superseded: the SQL-only structured gate P2.8 (replaced by P2.10; runbook in
`paper/archive/superseded_runbooks/`). Stopped: P2.10, replaced by P2.11 and
P2.12. Not pursued: an in-domain public pool.

## 2. Evidence plan

1. Reproduce standard Spider and BIRD-with-evidence baselines. **Done.**
2. Run pure FL with the same data and prompts. **Done.**
3. Rerun the reference method in both directions. **Done.**
4. Attribute any EX gain with matched public-gold, SeqKD, and soft-KD controls.
   **Done so far: no teacher-specific gain after the last private stage.**
5. Improve only the part the results show is limiting. **In progress: Direction 1
   (keep the Hinton edge through FL) and Direction 2 (Struct-SQL with a client fix).**
6. Confirm the chosen method on more seeds, one harder split, and maybe a
   second model family.
7. Add communication, resource, and privacy-boundary evidence.

Submission gate (Q3 target): a reproducible EX gain over matched FL, with a
causal control that shows the teacher matters.

## 3. Paper-closure checklist

Open items from the former `PAPER_TODO.md` (archived in
`paper/archive/paper_planning_2026-09/`):

- [ ] Choose the final method from evidence, not from old names.
- [ ] Second training seed for the chosen method and its matched control.
- [ ] One stronger non-IID split (for example `alpha=0.1`).
- [ ] T1–T3 convergence for the chosen method and for pure FL.
- [ ] Final student-versus-teacher latency and memory, plus adapter bytes.
- [ ] Paired EX and error-type analysis (EM descriptive only).
- [ ] Re-check Spider base, centralized, and FL under the explicit `spider`
      profile (the v2 Spider files and K5 split are frozen at nested `8caa610`).
- [ ] Decide on the filtered/cleaned BIRD release, or state clearly that the
      paper uses BIRD-original.
- [ ] Prompt parity smoke across teacher, centralized, client, server, and
      evaluation prompts.
- [ ] Rebuild tables, figures, claims, and the reproducibility manifest.

Optional, only if reviewers need broader claims: teacher/student size sweeps,
a second model family, FedProx on BIRD, federated training of the 7B model.
