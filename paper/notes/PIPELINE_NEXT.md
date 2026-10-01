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

Three tracks now, two of them in parallel:

| Track | Question | Branch (nested) | Status |
|---|---|---|---|
| **A1 merge gate** | Does a weight merge keep the teacher's edge after FedAvg? | `experiment/terminal-retention` | **running** (GPU 1) |
| **P2.11 plan as an auxiliary task** | Does learning the teacher's plan as a side task help, with SQL-only clients and SQL-only inference? | `experiment/struct-aux-cot` | code in progress |
| **P2.12 latent plan at the client** | Can clients keep the plan format without plan labels, so the last round stops overwriting the teacher's plans? | `experiment/struct-aux-cot` | code in progress, after P2.11 |

Later, depending on A1: A2 (interleaved `(A -> k)^R` on BIRD shards) and
Direction B (in-domain Spider public split, unlabeled). Both are described at
the end of this section and are not implemented.

Read-only views (CPU, any time, from the branch that produced the results):

```powershell
$env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python scripts/show_p29_merges.py
```

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

## P2.11. Plan as an auxiliary task (Distilling Step-by-Step)

Private data has only gold SQL. P2.11 keeps every client and the deployed model
SQL-only. The teacher's plan enters only as a second training task inside K,
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
- Runner `scripts/run_p211_aux_plan.py` (nested branch `experiment/struct-aux-cot`).
  Commands are added here after the code is reviewed and pushed.

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

## Later (not implemented)

**A2. Interleaved schedule**, only if A1 shows the edge can survive:
`round r = 1..R (R = 3): A (FedAvg on Spider) -> k (Hinton on BIRD shard r)`.
BIRD is split into R disjoint shards, so total public data and KD steps equal
the single K of `A>K>A`. Controls: FL `A^R` and the same schedule with gold CE.
About 25–30 GPU-hours. Follows FedDF, FedCoLLM and FedMKT, which distil every
round.

**Direction B. In-domain public pool.** Hold out about 20% of Spider train as
public questions without SQL; the teacher labels them; gold stays an oracle
row. No domain gap, so the run can end on KD. Every baseline must be rerun on
the new split (about 2–3 GPU-days). BIRD stays as the harder second setting.

Older finished runbooks: `paper/archive/completed_runbooks/` and
`paper/archive/superseded_runbooks/`. They are history, not the queue.
