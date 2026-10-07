# FedLS-SQL run queue

This file owns executable work. Results and interpretation are in
[LAB_LOG.md](LAB_LOG.md); artifact identities are in [RESULT_REGISTRY.md](RESULT_REGISTRY.md).

## 2026-10-07: P2.18 complete, no GPU jobs queued

All six Coder-0.5B arms and 58 endpoint evaluations are published in nested
`45a8bdc`: central E3, FL AAA, gold/Hinton AKAKA and AKKAA. The completed
[launch and recovery commands](../archive/completed_runbooks/PIPELINE_P218_0P5B_2026-10-07.md)
are archived. Do not rerun preparation or delete existing checkpoints.

Spider EX: Hinton AKKAA 63.15, Hinton AKAKA 62.57, gold AKKAA 61.80,
gold AKAKA 60.15, central E3 59.38, FL AAA 57.54. Hinton AKAKA-minus-gold
is +2.42 (nominal exact p=.0199); the two Hinton schedules are not separated
(p=.581). Seed 0 only.

Recommended next decision: replicate matched gold/Hinton AKAKA on seeds 1 and
2 to test the teacher effect; include both AKKAA arms if choosing the schedule
is the priority. This is a proposal, not a launch authorization or ready queue.
Each new seed needs fresh adapters and its own preparation/probe identities;
teacher-cache reuse still requires the existing exact contract.

Keep SQL-only, `target_fp32`, the existing training/eval recipe and manual
shared-memory checks. No automatic Windows counters. New launch commands will
be added here once the next run scope is selected.
