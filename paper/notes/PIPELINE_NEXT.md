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

**Status: P2.13 implemented on `experiment/fullgold-plan`; CPU verification
complete, server preparation and GPU smokes pending.** The existing P2.11
runner retains its 5,319-row teacher-SQL recipe. No GPU job has been launched
from this development machine. Active commands are in section 5.

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
  a correct plan. Preparation exports the fixed stratified sample and pins
  its hash; the operator must review it before launching the lanes and record
  findings in the lab log. The runner does not assert a human review occurred.
  If targets are defective, stop before training and create a new admitted
  pool/run identity; never edit the frozen P2.10 pool or silently change rows.
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

1. Run one shared CPU preparation and review the exported 50-plan sample.
   Each lane then smokes its own arms: 16 public microsteps (including an
   auxiliary example for E/T), 4 microsteps per terminal client, and a 2-row
   SQL-only BIRD eval. Smoke roots are separate from full-run roots.
2. Run **GPU 0: T; GPU 1: G then E** at seed 0. This supersedes serial G/T/E
   ordering without changing their recipes. Complete K and terminal A for every arm.
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

## 5. Active two-GPU commands

Run from the **`fedicl-sql/` repository root on the GPU server**, in PowerShell.
The owner reports both GPUs idle; live availability was not independently
checked here. Do the one-time checkout/preparation before opening either lane.
Do not switch, pull, edit, or commit in this worktree while either lane runs.

Implementation: `experiment/fullgold-plan`, required commit `165a20e878db289a8d4fb6388b67109ad31e5377`.
Preparation needs the existing SQL-only FL T1 adapter, full BIRD gold, P2.10
train plans/provenance/candidates, private splits, all five eval inputs and raw
databases. It checks scoped cleanliness, original-gold joins, admission/hashes,
and all target lengths at 7,168. It generates no new teacher targets.

One-time checkout and preparation (CPU tokenizer audit):

```powershell
$ErrorActionPreference='Stop'; git fetch origin; if($LASTEXITCODE -ne 0){throw 'fetch failed'}; git switch experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'switch failed'}; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; $required='165a20e878db289a8d4fb6388b67109ad31e5377'; $head=(git rev-parse HEAD).Trim(); if($LASTEXITCODE -ne 0 -or $head -ne $required){throw 'unexpected implementation commit'}; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; git fetch origin experiment/struct-aux-cot; if($LASTEXITCODE -ne 0){throw 'P2.10 source fetch failed'}; uv run python -m scripts.restore_p213_inputs; if($LASTEXITCODE -ne 0){throw 'P2.10 input restore failed'}; uv run python -m scripts.run_p213_fullgold_plan --phase prepare; if($LASTEXITCODE -ne 0){throw 'P2.13 preparation failed'}
```

The input restore step reads exactly five existing public artifacts from
P2.10 commit `9c3476eeee3df155e75cd581b5ff7ebd4d9df5b3` on
`experiment/struct-aux-cot`. That result commit was absent from the P2.13
branch. CSV record-newline restoration is accepted only if the original
provenance SHA256 matches; a plain Git checkout of the CSV does not preserve
that hash. Existing files are never overwritten. No new teacher generation,
branch merge, or input publication occurs.

If the earlier preparation failed with missing `p210_struct_sql_s0/train.csv`,
run this recovery command before either GPU lane starts (already on
`experiment/fullgold-plan`):

```powershell
$ErrorActionPreference='Stop'; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; git fetch origin experiment/struct-aux-cot; if($LASTEXITCODE -ne 0){throw 'source fetch failed'}; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python -m scripts.restore_p213_inputs; if($LASTEXITCODE -ne 0){throw 'restore failed'}; uv run python -m scripts.run_p213_fullgold_plan --phase prepare; if($LASTEXITCODE -ne 0){throw 'prepare failed'}
```

Do not rerun restore after a preparation manifest exists. Prepared runs resume
using their lane commands, with input and code identities unchanged.

Before training, inspect the generated
`artifacts/protocol_v2/p213_fullgold_plan_s0/plan_review_sample.json` (50 plans,
stratified by SQL complexity). Record the audit; do not label the exported
sample itself as a completed semantic review. Confirm physical GPU indices
with `nvidia-smi`. These smokes exercise the auxiliary task but do not establish
worst-case sequence VRAM feasibility.

Terminal 1, physical GPU 0, teacher-plan T:

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES='0'; uv run python -m scripts.run_p213_fullgold_plan --phase run --lane teacher; if($LASTEXITCODE -ne 0){throw 'P2.13 teacher lane failed'}
```

Terminal 2, physical GPU 1, fullgold G followed by extra-SQL E:

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES='1'; uv run python -m scripts.run_p213_fullgold_plan --phase run --lane controls; if($LASTEXITCODE -ne 0){throw 'P2.13 controls lane failed'}
```

Separate publication command, **only after both lanes exit successfully**.
It verifies all 30 full evaluations, writes paired contrasts, resolves an
explicit compact-file allowlist, checks staged paths, then commits and pushes:

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python -m scripts.run_p213_fullgold_plan --phase analyze; if($LASTEXITCODE -ne 0){throw 'P2.13 analysis failed'}; $staged=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or $staged.Count -ne 0){throw 'index must be empty'}; $paths=@(uv run python -m scripts.list_p213_publication); if($LASTEXITCODE -ne 0 -or $paths.Count -eq 0){throw 'publication allowlist failed'}; git add -- $paths; if($LASTEXITCODE -ne 0){throw 'git add failed'}; $actual=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or @(Compare-Object ($paths | Sort-Object) ($actual | Sort-Object)).Count -ne 0){throw 'staged paths differ from allowlist'}; git commit -m 'results: record P2.13 full-gold plan screen'; if($LASTEXITCODE -ne 0){throw 'commit failed'}; git push origin HEAD:experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'push failed'}
```

Resume an interrupted lane with its exact command. Completed stages/evals are
reused; partial training resumes from its own checkpoint. Each lane has a
duplicate-executor lock; shared manifest updates are locked. Intermediate
parents use immutable receipts binding stage/config/metrics/adapter bytes, so
no commit is needed between K and A. The original parent remains committed.
Fingerprints changing is an error, never a reason to bypass the guard.

Outputs: `artifacts/protocol_v2/p213_fullgold_plan_s0/<arm>_<endpoint>`;
audit/summary: `audits/protocol_v2/p213_fullgold_plan_s0/`; per-arm/endpoint/set
eval resume roots under `artifacts/eval_resume/protocol_v2/p213_*_s0/eval_k0`.
Publication excludes public targets, raw data, adapters, caches and lock files.
If push alone fails after a successful commit, retry only the push.
Concurrent lanes share host resources: their timings are operational, not an
exclusive-hardware resource comparison. No P2.11 runtime estimate is assumed.

Local validation: full pytest and focused CLI/dry-run checks passed. Windows
PowerShell execution, real-data preparation, semantic review and GPU smokes
remain server-side checks; no EX result or training-speed claim is made here.

## 6. Parked work

Parked: P2.11 SeqKD-plus-plan, P2.12/local STaR-style plans, A2 interleaving,
and A3 extra private rounds. P2.10 remains stopped. A1 was last reported
running on 2026-10-01, status not checked here; collect its existing results
when available, but do not make it a prerequisite for P2.13 or relaunch it
from this queue.

The previous commands and proposal details are preserved in the
[dated queue archive](../archive/completed_runbooks/PIPELINE_PRE_FULLGOLD_PLAN_2026-10-02.md).
