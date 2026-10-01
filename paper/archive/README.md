# FedLS-SQL — archive index

Everything here is history. It is kept for provenance, not for planning.
Commands in archived runbooks are records, not the current queue (that is
`paper/notes/PIPELINE_NEXT.md`). Do not edit archived content; add new
material and index entries only.

## Folders

| Folder | What it holds | Replaced by |
|---|---|---|
| `lab_log_2026-09/` | full lab log, 2026-09-03 to 2026-09-26 (protocol v2, P2.0–P2.10 setup) | `paper/notes/LAB_LOG.md` |
| `results_reviews_2026-09/` | closed P2.1–P2.4 reviews and the old valid-results/adapter ledger | `paper/notes/RESULT_REGISTRY.md`, `paper/results/MAIN_RESULTS.md` |
| `method_reviews_2026-09/` | KD method reviews (RKL; OPD, retention, ordering) and the pre-cleanup architecture | `paper/notes/system_architecture.md` |
| `paper_planning_2026-09/` | stale paper trackers and stubs | `paper/notes/EXPERIMENT_MATRIX.md`, `paper/drafts/fedls_sql_outline.md` |
| `paused_runbooks/` | P2.9 terminal retention runbook, paused and resumable | `paper/notes/PIPELINE_NEXT.md` (paused section) |
| `completed_runbooks/` | finished command blocks and dated sequencing snapshots; each file states its actual status | `paper/notes/PIPELINE_NEXT.md` |
| `superseded_runbooks/` | queued runbooks replaced before running (P2.7, P2.8, P2.13) | — |
| `closed_method_branches/` | failed method branches (P0.10 FedDF, P1.7a preference KD) | own `README.md` |
| `protocol_v1_no_bird_evidence/` | everything before the 2026-09-03 protocol reset | own `README.md` |
| `pre_fedls_2026-08/` | FedICL/ICL-era material before 2026-08-19 | own `README.md` |

## 2026-10-02 queue snapshot

[Queue before the full-gold auxiliary-plan decision](completed_runbooks/PIPELINE_PRE_FULLGOLD_PLAN_2026-10-02.md)
preserves the A1 merge commands, A2/A3 schedule proposals, P2.11 SeqKD-plan
launch command, and P2.12/local-CoT proposals. It is historical sequencing,
not evidence that those jobs completed. The active queue owns the replacement
and all future launch decisions.

## Files moved in the 2026-09-29 cleanup

Moved with `git mv`, content unchanged. Only relative links inside them were
updated to work from the new location.

| Old path | New path |
|---|---|
| `paper/notes/LAB_LOG.md` (full text) | `lab_log_2026-09/LAB_LOG_2026-09-03_to_2026-09-26.md` |
| `paper/notes/VALID_RESULTS_AND_ADAPTERS.md` | `results_reviews_2026-09/VALID_RESULTS_AND_ADAPTERS.md` |
| `paper/notes/BIRD_BASELINE_AUDIT.md` | `results_reviews_2026-09/BIRD_BASELINE_AUDIT.md` |
| `paper/results/P22_TRANSFER_REVIEW.md` | `results_reviews_2026-09/P22_TRANSFER_REVIEW.md` |
| `paper/results/P23_TERMINAL_CONSOLIDATION_REVIEW.md` | `results_reviews_2026-09/P23_TERMINAL_CONSOLIDATION_REVIEW.md` |
| `paper/results/P24_TEACHER_SIGNAL_REVIEW.md` | `results_reviews_2026-09/P24_TEACHER_SIGNAL_REVIEW.md` |
| `paper/notes/KD_METHOD_REVIEW.md` | `method_reviews_2026-09/KD_METHOD_REVIEW.md` |
| `paper/notes/PAPER_TODO.md` | `paper_planning_2026-09/PAPER_TODO.md` |
| `paper/notes/PAPER_NEXT_TASKS.md` | `paper_planning_2026-09/PAPER_NEXT_TASKS.md` |
| `paper/notes/PAPER_EVIDENCE_PLAN.md` | `paper_planning_2026-09/PAPER_EVIDENCE_PLAN.md` |
| `paper/notes/MANUSCRIPT_SKELETON.md` | `paper_planning_2026-09/MANUSCRIPT_SKELETON.md` |
| `paper/notes/PAPER_OUTLINE_TARGET.md` | `paper_planning_2026-09/PAPER_OUTLINE_TARGET.md` |
| `paper/drafts/FEDLS_SQL_METHOD.md` | `paper_planning_2026-09/FEDLS_SQL_METHOD.md` |

Copied (the active file stays, in short form):

| Active file | Full earlier copy |
|---|---|
| `paper/notes/system_architecture.md` | `method_reviews_2026-09/system_architecture_2026-09-24.md` |
| `paper/notes/PIPELINE_NEXT.md` (P2.9, decision rules, ordering study) | `paused_runbooks/P29_TERMINAL_RETENTION_PAUSED_2026-09-26.md` |

Older archived files still name the old paths above (for example
`completed_runbooks/P2_1R_P2_2_COMPLETED_2026-09-16.md` and
`completed_runbooks/P2_3_TERMINAL_CONSOLIDATION_2026-09-16.md`). Use the table
to find them.
