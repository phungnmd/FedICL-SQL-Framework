# FedLS-SQL — run queue

This is the only file with commands to run. Each command is one line of
PowerShell. Run it from the `fedicl-sql/` root on the Windows GPU server.
Results and decisions go to `LAB_LOG.md` after a run finishes.

## Now (2026-10-01)

What we know (details in `LAB_LOG.md`):

- A public BIRD stage followed by one more FedAvg round beats FL alone on all
  five sets and gets close to centralized training.
- Right after the public stage (`A>K`), Hinton and SeqKD beat plain gold
  training. After the extra FedAvg round (`A>K>A`), they only tie gold.
- Struct-SQL as run in P2.10 (QP-CoT everywhere, template plans at the clients)
  is worse: the plan format at inference hurts the 1.5B student, and template
  plans teach it to invent JOINs. **P2.10 is stopped. Do not rerun it.** Its
  committed public rows are reused by P2.12 below.

Two directions, run in parallel on the two GPUs:

| Direction | Goal | Steps | Branch (nested) | Status |
|---|---|---|---|---|
| **1. Hinton KD that survives FL** | Keep the teacher's edge after more FedAvg rounds | A1 merge gate, then A2 interleaved schedule | `experiment/terminal-retention` | A1 **running** (GPU 1); A2 planned |
| **2. Struct-SQL with a client fix** | Teacher plans help without template plans at the clients | P2.11 plan as an auxiliary task, then P2.12 latent client plan | `experiment/struct-aux-cot` | P2.11 ready (GPU 0); P2.12 code ready, runs after P2.11 |

Not pursued: an in-domain public pool (holding out Spider as public data), and
rerunning P2.10.

Read-only views (CPU, any time, from the branch that produced the results):

```powershell
$env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python scripts/show_p29_merges.py
```

# Direction 1: Hinton KD that survives FL

## A1. Merge gate (running)

Evaluation only, no training. Four arms from the same FL T1 parent:

| Arm | Public stage | Rows | Control for |
|---|---|---:|---|
| `hinton` | gold CE + Hinton forward KL | 9,428 | — |
| `fullgold` | gold CE | 9,428 | `hinton` |
| `seqkd` | SeqKD (teacher SQL) | 5,319 | — |
| `gold` | gold CE on the same rows | 5,319 | `seqkd` |

Merges per arm (seconds on CPU): `arith0p5`, `arith1p0` = FL `A>A` plus
λ × (model after K − FL T1); `wise0p5` = half the model after K plus half the
model after the last FedAvg.

Promote a merge if, for teacher minus gold on the same merge: BIRD ≥ +1.5,
Spider-family mean ≥ +1.0, no Spider-family set below −1.0, and Spider not more
than 1.0 below the plain terminal.

The command running on GPU 1 (nested commit `9ad7239` or later):

```powershell
$G='1'; $ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES=$G; $env:PYTHONUTF8='1'; $R='scripts/run_p29_retention_gate.py'; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor 9ad7239 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required commit 9ad7239 missing' }; foreach ($P in @(@('hinton','fullgold'), @('seqkd','gold'))) { foreach ($V in 'arith0p5','wise0p5','arith1p0') { foreach ($A in $P) { uv run python $R --phase merge --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V merge failed" }; uv run python $R --phase eval --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V eval failed" } }; uv run python scripts/show_p29_merges.py } }; Write-Host 'A1 merge gate complete'
```

## A2. Interleaved schedule (planned, not implemented)

Run only if A1 shows the edge can survive. It follows FedDF, FedCoLLM and
FedMKT, which distil in every round and end on the distilled model:

```text
round r = 1..R (R = 3):   A (FedAvg on Spider)  ->  k (Hinton on BIRD shard r)
```

- BIRD is split into R disjoint shards, so the total public data and KD steps
  equal the single K of `A>K>A`. Only the schedule changes.
- More FedAvg rounds than today's two, since FL is not saturated (T1/T2/T3
  Spider 57.35/62.57/64.31; centralized needs three epochs).
- The run ends on k. If Spider drops, a final merge from A1 is the fallback.
- Controls: FL `A^R`, and the same schedule with gold CE on the same shards.
- About 25–30 GPU-hours for Hinton plus gold, plus `A^R`.
- Needed code: a K stage on a row shard, and an R-round schedule runner.

# Direction 2: Struct-SQL with a client fix

Private Spider data has only gold SQL. P2.10 gave the clients template plans
written by code, and that hurt. Both steps below avoid plan labels at the
clients.

## P2.11. Plan as an auxiliary task (Distilling Step-by-Step)

P2.11 keeps every client and the deployed model SQL-only. The teacher's plan enters only as a second training task inside K,
following Distilling Step-by-Step (Hsieh et al., Findings of ACL 2023):

```text
A    clients: [SQL] question -> gold SQL                        (unchanged)
K    server:  [SQL]  question -> teacher SQL     (5,319 SeqKD rows, weight 1)
              [PLAN] question -> teacher plan    (P2.10 admitted rows, weight beta = 0.5)
A    clients: as before
eval SQL only, batch 16, five sets
```

| Arm | Plan task target | Compared with |
|---|---|---|
| `tplan` | teacher QP-CoT plan | committed `A>K[seq]` and `A>K[seq]>A` |
| `aplan` | template plan of the same rows (control) | `tplan` |

- `tplan − seqkd` asks whether the plan task helps at all.
- `tplan − aplan` asks whether the gain comes from the teacher's reasoning or
  only from having a second task.
- Same FL T1 parent and SeqKD recipe as the committed SeqKD row, so the only
  change is the added task.
- Cost: about 6–8 GPU-hours per arm (K, commit, terminal A, two evaluations).
- Runner `scripts/run_p211_aux_plan.py`, nested branch `experiment/struct-aux-cot`,
  commit `4fc9c61` or later. Detailed phase notes: `docs/P211_P212_RUNBOOK.md`.
- Loss mode `full_bf16`, the mode of the committed SeqKD rows, so the plan task
  is the only difference against them.

The server has one working copy. `experiment/struct-aux-cot` contains everything
on `experiment/terminal-retention`, and the A1 code is unchanged on it, so the
working copy switches branch while the A1 lane keeps running. GPU 0, both arms
in order (`tplan`, then `aplan`), about 6–7 h per arm:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; function P([string[]]$A) { uv run python -m scripts.run_p211_aux_plan @A; if ($LASTEXITCODE -ne 0) { throw "P2.11 $($A -join ' ') failed" } }; function C($Rows, $Arm) { $f=@(uv run python -m scripts.list_p211_publication --rows $Rows --arm $Arm); if ($LASTEXITCODE -ne 0 -or $f.Count -eq 0) { throw "P2.11 $Arm $Rows allowlist failed" }; git add -- $f; git diff --cached --quiet; if ($LASTEXITCODE -ne 0) { git commit -m "results: P2.11 $Arm $Rows stage row" -- $f; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } } }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git switch experiment/struct-aux-cot; if ($LASTEXITCODE -ne 0) { throw 'Switch failed' }; git pull --ff-only origin experiment/struct-aux-cot; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor 4fc9c61 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required commit 4fc9c61 missing' }; foreach ($A in 'tplan','aplan') { P @('--phase','smoke','--arm',$A,'--beta','0.5'); P @('--phase','train-public','--arm',$A,'--beta','0.5'); C 'public' $A; P @('--phase','eval','--arm',$A,'--endpoint','public'); P @('--phase','train-terminal','--arm',$A); C 'terminal' $A; P @('--phase','eval','--arm',$A,'--endpoint','terminal') }; P @('--phase','analyze'); Write-Host 'P2.11 complete'
```

Send the smoke output (peak reserved VRAM) and, after `tplan` public
evaluation, the public EX. `tplan − seqkd` at the public endpoint is the early
read.

## P2.12. Latent plan at the client, loss on SQL only

Keeps the Struct-SQL format end to end without plan labels on private data:

```text
parent  A[qp] > K[qp-teacher]   (committed P2.10 public rows: teacher and gold)
A       each client writes its own plan with the current global model,
        then trains on plan + gold SQL with zero loss on the plan tokens
eval    plan then SQL, five sets; strict and SQL-marker EX
```

- No gradient on plan tokens, so the last round cannot overwrite the teacher's
  plan style, which is what broke P2.10.
- Risk: the model may learn to ignore its plan. Inference still uses CoT, which
  was weak at 1.5B in P2.10.
- Cost: plan generation about 2–3 h per arm, the round about 1.9 h, evaluation
  about 2 h.
- Runs after P2.11. Runner `scripts/run_p212_latent_plan.py`; commands follow
  after review.

Older finished runbooks: `paper/archive/completed_runbooks/` and
`paper/archive/superseded_runbooks/`. They are history, not the queue.
