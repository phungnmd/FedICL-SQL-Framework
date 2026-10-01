# FedLS-SQL run queue

This file owns the next experiment and its launch commands. Results belong in
[LAB_LOG.md](LAB_LOG.md). All future commands must follow
[CONVENTION.MD section 6.1](../../CONVENTION.MD).

## Decision (2026-10-02): full-gold plus auxiliary teacher plans

Run one three-arm screen at fixed `A>K>A`, named **P2.13**. The primary metric
is final Spider EX. Keep both private stages and inference SQL-only; teacher
plans are a separate supervised task inside the public server stage only.

This tests whether teacher reasoning improves the strongest gold recipe,
beyond extra SQL exposure. Use 1,000 existing admitted plans first. Do not
start by generating plans for all BIRD rows, changing the teacher, adding
private rounds, or generating private plans.

**Status: design selected; runner not implemented, no launch command active.**
The existing P2.11 runner uses 5,319 teacher SQL rows and cannot launch this
recipe. The next engineering task is a separate P2.13 runner with the controls
below, followed by smoke verification and explicit run/publication commands.
This documentation change does not start, stop, or inspect GPU jobs.

## 1. The three arms

All arms start from the same normal SQL-only FL T1 adapter, never the P2.10
QP-CoT parent. Each then runs K once and the same terminal FedAvg round
(5 clients, 1 local epoch, plaintext aggregation).

| Arm | Base SQL task in K | Added task in K | What it answers |
|---|---|---|---|
| `G` / `fullgold` | All 9,428 BIRD gold SQL rows, weight 1 | None | Strong public-gold baseline |
| `E` / `extra_sql` | Same 9,428 gold SQL rows, weight 1 | Gold SQL again on the 1,000 plan row IDs, weight 0.5 | Effect of added selected-row exposure and updates |
| `T` / `teacher_plan` | Same 9,428 gold SQL rows, weight 1 | Teacher plan on those exact 1,000 row IDs, weight 0.5 | Added teacher-plan supervision |

The extra SQL targets in E must come from the original full-gold pool, joined
by stable row ID, not from the teacher SQL stored with the plan sidecar.

```text
A: private question + schema -> gold SQL
K: SQL instruction  + public question + schema + evidence -> gold SQL
   PLAN instruction + the same public input              -> teacher plan (T only)
A: private question + schema -> gold SQL
Inference: SQL instruction + question + schema -> SQL
```

PLAN is a target, not an input to the SQL task. Both tasks update the same
student adapter. Task separation follows
[Distilling Step-by-Step](https://aclanthology.org/2023.findings-acl.507/);
plan representation is inspired by
[Struct-SQL](https://arxiv.org/html/2512.17053v3). Their combination in
BIRD-to-Spider FL is the hypothesis being tested.

## 2. Freeze the seed-0 screen before training

- Student: Qwen2.5-1.5B-Instruct; existing Qwen2.5-Coder-7B-Instruct plans.
  Reuse the normal SQL-only FL T1 adapter after verifying its bytes/lineage.
- Base pool: the full 9,428-row BIRD train pool with evidence. Plan subset:
  the existing 1,000 P2.10 admitted rows and teacher-plan sidecar. Verify
  unique IDs, membership in the base pool, input/evidence identity, teacher
  provenance, admission results, and hashes before accepting the subset.
- Audit 50 fixed, seed-0 sampled plans across SQL-complexity strata before
  training. Check joins, predicates, aggregation, and agreement with the
  accompanying teacher SQL. Execution-correct SQL alone does not establish
  a correct plan. Record findings; repair/re-admit defective targets before
  freezing hashes, and never silently change rows between arms.
- K: one pass through each arm's examples; LR 2e-4, LoRA r16, batch 1,
  accumulation 16, max length 7,168, gradient checkpointing, `full_bf16`.
  Preserve the recorded full-gold schema/prompt and optimizer/LR recipe.
  Use the same loss implementation in all three arms and fail on truncation.
- G has 9,428 examples; E and T have 10,428. Fix auxiliary token weight
  `beta=0.5` for both E and T. Normalize weighted CE by active-token count,
  not the sum of weights that would cancel beta in an auxiliary-only batch.
  This is one mixed pass, not equal sampling of the SQL and PLAN tasks.
- E/T share the exact ordered base/auxiliary row slots, seed, batch boundaries,
  accumulation, update count, optimizer reset, warm-up, and LR horizon.
  Only the auxiliary instruction/target changes. G has its own shorter
  one-pass horizon; E controls this extra-training difference.
- Match base SQL target exposure across G/E/T. Record supervised token counts,
  sequence lengths, updates, and GPU time. E/T have matched rows and updates,
  not equal token FLOPs or an isolated proof of reasoning faithfulness.
- Terminal A uses the full-gold terminal private recipe with SQL-only prompts,
  identical client split/order, local epochs, optimizer/LR, LoRA, and aggregation
  across all arms. No retention loss, template plans, or client public replay.
  Public data, teacher targets, and caches remain server-side.

Beta 0.5 and 1,000 plans are fixed screening choices, not established optima.
Do not sweep them against Spider dev before completing the three-arm screen.

## 3. Execution order and evaluation

1. Implement/register P2.13; validate pool joins, weights, matched E/T row
   schedules, fingerprints, resume/completion guards, and publication allowlists.
   Smoke all three arms, including SQL-only evaluation and terminal training.
2. Run **G, then T, then E** at seed 0. Complete K and terminal A for every arm.
   Save raw predictions and score both endpoints on the fixed five-set suite,
   using the existing protocol-v2 SQL-only evaluator at batch 16. Do not stop
   an arm solely because post-K Spider EX is low; terminal EX decides.
3. Analyze all three terminal checkpoints together. Use the fixed end of K
   and end of A, not independently selected best checkpoints. Pair predictions
   by query ID. Predeclare T-G (practical gain) and T-E (added-plan contrast);
   report EX deltas, wins/losses, paired 95% confidence intervals, and exact
   McNemar results for both. Public-endpoint deltas diagnose transfer/retention.

Default: run a fresh G through the same implementation. Reuse the committed G
only if an explicit audit establishes identical scientific settings, parent
bytes, loss normalization, ordered examples, optimizer/LR horizon, terminal
recipe, and evaluation contract. Otherwise the old row is a reference only.

Historical seed-0 terminal references are fullgold 66.54 and Hinton 66.63
Spider EX; see the evidence ledger in [LAB_LOG.md](LAB_LOG.md). Do not treat
these as compute-matched to the added task or as substitutes for E.

## 4. Decide from terminal Spider EX

| Outcome | Interpretation and next action |
|---|---|
| T > G and T > E | Positive teacher-plan screen; compare with Hinton, then confirm the unchanged recipe on seeds 1 and 2 before increasing plan coverage |
| T > G but T <= E | Better pipeline score, but extra selected-row SQL training explains as much or more; no teacher-specific win yet |
| T > E but T <= G | Plans outperform the extra-SQL control, but have not improved the strong gold baseline |
| T <= both G and E | No gain from this recipe; inspect the frozen plan audit, loss balance, truncation, and public-to-terminal change before any new variant |

The desired outcome also exceeds the Hinton reference. A positive difference
is a screening signal, not automatically reliable: one Spider query is about
0.097 percentage points. Small or uncertain gains need seed confirmation,
not a claim of success or immediate generation of all BIRD plans. Report the
uncertainty rather than treating a non-significant result as equivalence.

For seeds 1 and 2, keep the recipe and split fixed and vary training RNG;
construct/reuse that seed's common initial A, then compare G/E/T from it.
Report per-seed and aggregate differences. A general multi-seed superiority
claim over Hinton additionally needs Hinton on the same seed/parent contracts.
Spider dev guides this screen, so report its exploratory status; do not call
those queries an untouched final test. BIRD/Spider variants are diagnostics,
not additional promotion thresholds. No extra A round is required.

Only after confirmation: consider greater plan coverage or a same-row AST
plan ablation to separate teacher content from generic structured supervision.
A null result at 1,000 plans does not reject every CoT method, but does not
justify a blind full-pool expansion either.

## 5. Launch readiness and parked work

P2.13 needs new experiment IDs, immutable seed/arm-specific output roots,
independent evaluation resume roots, and a manifest recording the frozen
recipe and pool hashes. Reuse training utilities where suitable; do not
relabel P2.11 artifacts or change its defaults to mean fullgold.

Add PowerShell run and separate publication commands here only after runner
verification, following CONVENTION.MD 6.1. Keep publication outside running
jobs; resolve the current requirement for committed intermediate parents
without mutating a worktree while another job uses it. Check live GPU/worktree
availability at launch. No cost estimate from the smaller P2.11 pool applies
without measurement.

Parked: P2.11 SeqKD-plus-plan, P2.12/local STaR-style plans, A2 interleaving,
and A3 extra private rounds. P2.10 remains stopped. A1 was last reported
running on 2026-10-01, status not checked here; collect its existing results
when available, but do not make it a prerequisite for P2.13 or relaunch it
from this queue.

The previous commands and proposal details are preserved in the
[dated queue archive](../archive/completed_runbooks/PIPELINE_PRE_FULLGOLD_PLAN_2026-10-02.md).
