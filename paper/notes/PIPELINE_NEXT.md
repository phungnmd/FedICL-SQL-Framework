# FedLS-SQL — active protocol-v2 queue

## P2.4c cancellation — 2026-09-17

User cancelled CE2/Hinton2 for cost, not because of a negative result. Server
termination is unconfirmed: press Ctrl+C once in each K2 terminal and wait for
both Python processes to exit. Preserve checkpoints and the original cache.
Do not kill unrelated jobs or mutate the server Git worktree while jobs run.

[Old K2 commands](../archive/completed_runbooks/P24C_CANCELLED_2026-09-17.md)
are historical only; do not launch terminal A or publish incomplete outputs.

## P2.5 — SeqKD versus GKD (planned; not executable yet)

Compare `A -> K(seqKD)` and `A -> K(GKD)`; evaluate each, append the identical
one-epoch Spider-private `A`, then evaluate both terminal adapters.

- Same published Spider FL T1 parent, frozen original Qwen7B teacher and
  Qwen1.5B student. No teacher training; BIRD retains evidence.
- Proposed primary comparison uses the same 5,319 selected BIRD public prompts:
  SeqKD uses teacher SQL CE; GKD uses current student rollouts and teacher
  distributions. Do not additionally filter GKD rollouts by execution success.
- Original on-policy GKD first: forward KL, unit temperature, no auxiliary
  gold CE, reward gate or privileged teacher prompt. Refresh samples per update
  batch; no gradient through sampling or teacher. Gold-prefix cache is not usable
  for the new student prefixes.
- One public pass, matched prompt exposure and optimizer settings where possible.
  Report generation/scoring cost separately; this is not equal wall-clock or
  output-token compute. This compares recipes, not on-policy sampling alone.
- Reuse the existing SeqKD public endpoint only after checking parent, pool,
  recipe and evaluator compatibility; otherwise use a fresh immutable root.
- Keep matched-gold CE as teacher-free control. A matched offline KL control
  would be needed to isolate the on-policy effect specifically.
- Evaluate Spider, Realistic, SYN, DK and BIRD before and after A, with identical
  decoding and scorer settings. Report paired differences, not just rankings.

### Next actions

1. Confirm the operator stopped both K2 processes; retain partial artifacts.
2. Implement GKD: current code has no on-policy training path. Test causal token
   alignment, masks, frozen teacher, rollout refresh, optimizer/RNG recovery,
   stage lineage and completion verification.
3. A5000 smoke on 32–64 public prompts: memory, seconds/update, no silent
   truncation. Set full-run budget only after measured throughput.
4. Then activate single-line resumable PowerShell lanes with separate allowlisted
   publication commands. No GPU command is activated by this document revision.
5. Publish completed public parents before terminal A (stage contract requires
   committed parents). Evaluate both endpoints even if the method ranking changes.

Do not relabel offline `fkl` as GKD. Further depth, recurrence and KD variants
remain deferred until this comparison is reviewed.
