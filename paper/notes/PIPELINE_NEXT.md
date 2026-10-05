# FedLS-SQL run queue

This file owns the next experiment and its launch commands. Results belong in
[LAB_LOG.md](LAB_LOG.md). Commands follow
[CONVENTION.MD section 6.1](../../CONVENTION.MD).

## Decision (2026-10-05): consolidate Git, then screen a smaller student

Both owner checkouts use `main`. Nested `main` integrates the implementation
and results from `experiment/fullgold-plan`, `experiment/struct-aux-cot`,
`experiment/terminal-retention`, and `chore/cleanup`. Historical result paths,
run IDs, and commits remain valid. The cleanup removes inactive ICL,
FLoRA-NA, retrieval, and self-consistency paths; current SQL-only runners remain.

The earlier 1.5B queue is preserved in the
[dated snapshot](../archive/superseded_runbooks/PIPELINE_1P5B_PRE_0P5B_2026-10-05.md).
P2.17 `A>K>A>K>A` is recorded (`bd4fdcb`); the third K and P2.16 centralized
E1-E4 are not treated as completed without committed evidence. Server lane
status is unverified. Do not change its checkout or delete experiment branches
on the remote while a lane may still publish to them.

## Next preparation, no GPU launch command yet

Candidate student: `Qwen/Qwen2.5-Coder-0.5B-Instruct`. Keep the frozen
`Qwen/Qwen2.5-Coder-7B-Instruct` teacher, Spider private clients, BIRD public
pool with evidence, SQL-only targets and inference, and no ICL. This changes
both size and the model family specialization relative to the existing
`Qwen/Qwen2.5-1.5B-Instruct`; any gain cannot be attributed to size alone.

Proposed seed-0 screen:

| Arm | Private Spider passes | Public BIRD epochs |
|---|---:|---:|
| Centralized Spider-only E3 | 3 | 0 |
| Pure FL `A>A>A` | 3 | 0 |
| Full gold `A>K[ce]>A>K[ce]>A` | 3 | 2 |
| Hinton `A>K[fkl]>A>K[fkl]>A` | 3 | 2 |

Gold and Hinton match private passes and public exposure. Centralized and FL
are controls at the same private depth, with less total training exposure.
Use `target_fp32` for every new student stage, the same data split, LoRA r16,
private recipe, evaluation batch 16, and execution timeouts. Report final
Spider EX and the paired Hinton-gold contrast. Replicate promising results
across seeds before claiming a general advantage.

Before adding runnable commands:

1. Parameterize the smaller-student runner with new experiment IDs and output
   roots. Existing P2.15-P2.17 constants and artifacts remain historical.
2. Start every arm from the fresh 0.5B base. No 1.5B adapter or optimizer state
   may initialize it. Validate student/teacher tokenizer alignment and the
   existing common-vocabulary KL contract; verify the full teacher-cache
   identity before deciding whether any cached logits can be reused.
3. Run CPU/config checks and a GPU smoke on the longest private and public
   examples. Measure reserved VRAM and shared GPU memory; keep the A5000
   limits in `fedicl-sql/docs/A5000_RUN_CONFIG.md`.
4. Add exact Windows launch and separate publication commands here only after
   the runner and smoke are ready. Sync the server to `main` only when idle
   and after preserving any unpublished result files.

No smaller-student run has been started by this Git consolidation.
