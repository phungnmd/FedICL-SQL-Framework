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
| `superseded_runbooks/` | superseded queues, including partially completed sequences | — |
| `closed_method_branches/` | failed method branches (P0.10 FedDF, P1.7a preference KD) | own `README.md` |
| `protocol_v1_no_bird_evidence/` | everything before the 2026-09-03 protocol reset | own `README.md` |
| `pre_fedls_2026-08/` | FedICL/ICL-era material before 2026-08-19 | own `README.md` |

## 2026-10-07 cancelled follow-up

- [P2.19 Hinton placement/depth queue](superseded_runbooks/PIPELINE_P219_SCHEDULE_EXTENSION_2026-10-07.md): cancelled before any result; replaced by the P2.20 placement grid.

## 2026-10-07 completed screen

- [P2.18 six-arm 0.5B queue](completed_runbooks/PIPELINE_P218_0P5B_2026-10-07.md): all arms/evaluations published in nested `45a8bdc`; no GPU job remains queued.

## 2026-10-06 0.5B launch layouts

- [Baseline-publication queue](superseded_runbooks/PIPELINE_0P5B_BASELINE_PUBLICATION_2026-10-06.md): replaced by local A1 receipts and one final publication.

- [Counter-removal branch update](superseded_runbooks/P218_COUNTER_REMOVAL_BRANCH_UPDATE_2026-10-06.md): replaced by pulling main after the owner confirmed the server stopped.

- [Counter-based queue](superseded_runbooks/PIPELINE_0P5B_COUNTER_GUARD_2026-10-06.md): automatic counters removed at owner request after a monitoring failure stopped FL.
- [Original manual waves](superseded_runbooks/PIPELINE_0P5B_MANUAL_LANES_2026-10-06.md): 9 command blocks.
- [Single-controller wrapper](superseded_runbooks/PIPELINE_0P5B_SINGLE_WRAPPER_2026-10-06.md): superseded after the owner clarified the required terminal layout.

The active queue uses one sequential command per GPU terminal and a local A1
receipt. Publication runs separately once both lanes finish. Training recipes
are unchanged; existing preparations have a checked identity update.

## 2026-10-05 queue snapshot

[1.5B queue before the smaller-student direction](superseded_runbooks/PIPELINE_1P5B_PRE_0P5B_2026-10-05.md)
preserves the P2.15-P2.17 launch and publication commands. P2.17's third public
stage and P2.16 centralized epochs are not marked completed by this archive.
The active queue now prepares a fresh 0.5B screen from consolidated `main`.

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
