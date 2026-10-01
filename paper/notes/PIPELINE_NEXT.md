# FedLS-SQL — run queue

This is the only file with commands to run. Each command is one line of
PowerShell. Run it from the `fedicl-sql/` root on the Windows GPU server.
Results and decisions go to `LAB_LOG.md` after a run finishes.

## Now (2026-10-02)

Primary objective: highest final-model Spider EX from public teacher
adaptation plus private FL. CoT is optional. Track pipeline gain over matched
FL separately from teacher gain over matched public gold; see the claim
ladder in `RELATED_WORK_NOVELTY_MATRIX.md`. BIRD and Spider variants are
secondary diagnostics, not substitutes for the primary objective.

What we know (details in `LAB_LOG.md`):

- A public BIRD stage followed by one more FedAvg round beats FL alone on all
  five sets and gets close to centralized training.
- Right after the public stage (`A>K`), Hinton and SeqKD beat plain gold
  training on Spider. After the extra FedAvg round (`A>K>A`), the matched
  comparisons show no reliable teacher-specific advantage at seed 0.
- P2.10 (QP-CoT everywhere, template client plans) underperformed and is
  stopped. Template-induced JOIN errors and inference-format cost are working
  explanations, not isolated causal findings. Strict and SQL-marker EX must
  be distinguished. **Do not rerun P2.10.** Its committed public rows remain
  inputs for the optional P2.12 screen.

Two research directions. GPU status below was last reported on 2026-10-01;
the 2026-10-02 documentation review did not inspect or start server jobs.

| Direction | Goal | Steps | Branch (nested) | Status |
|---|---|---|---|---|
| **1. Public adaptation and FL convergence** | Raise final Spider EX and measure teacher contribution | A1 existing merge screen; A3 consolidation-depth screen; A2 interleaving if justified | `experiment/terminal-retention` | A1 last reported running (GPU 1); A3/A2 planned |
| **2. Teacher plans without private plan labels** | Improve SQL prediction through public reasoning supervision | P2.11 auxiliary plan first; P2.12 conditional | `experiment/struct-aux-cot` | P2.11 ready (GPU 0); P2.12 code ready, lower priority |

Not pursued: an in-domain public pool (holding out Spider as public data), and
rerunning P2.10.

Read-only views (CPU, any time, from the branch that produced the results):

```powershell
$env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python scripts/show_p29_merges.py
```

# Direction 1: Public adaptation and FL convergence

## A1. Merge gate (last reported running)

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

The existing A1 teacher-retention gate, for teacher minus gold on the same
merge: BIRD ≥ +1.5, Spider-family mean ≥ +1.0, no Spider-family set below −1.0,
and Spider not more than 1.0 below the plain terminal.

Keep that gate as the original diagnostic and report its outcome unchanged.
It is not the new method-selection objective. Also report absolute Spider EX,
gain over the plain terminal and matched FL, and teacher-minus-gold on Spider.
Do not prefer a lower-Spider endpoint solely because it retains a larger
teacher edge or more BIRD accuracy. Neither A3 nor A2 logically requires this
merge gate to pass.

The command last reported running on GPU 1 (nested commit `9ad7239` or later):

```powershell
$G='1'; $ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES=$G; $env:PYTHONUTF8='1'; $R='scripts/run_p29_retention_gate.py'; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor 9ad7239 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required commit 9ad7239 missing' }; foreach ($P in @(@('hinton','fullgold'), @('seqkd','gold'))) { foreach ($V in 'arith0p5','wise0p5','arith1p0') { foreach ($A in $P) { uv run python $R --phase merge --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V merge failed" }; uv run python $R --phase eval --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V eval failed" } }; uv run python scripts/show_p29_merges.py } }; Write-Host 'A1 merge gate complete'
```

## A2. Interleaved schedule (planned, not implemented)

Consider after the simpler A3 depth screen. Interleaving is a separate
hypothesis; failure of a post-hoc merge does not reject it. Example only:

```text
round r = 1..R (R = 3):   A (FedAvg on Spider)  ->  k (Hinton on BIRD shard r)
```

- Hold total A rounds, public rows/exposure, update budget, and optimizer/LR
  policy fixed against a one-K schedule. Three A rounds versus the historical
  two-round `A>K>A` changes the private budget as well as the schedule.
- Controls: FL `A^R`, the gold version of each schedule, and a one-K placement
  at the same R. Record shard order, optimizer resets, and LR horizons.
- Ending on k is a candidate, not a requirement. Choose deployment endpoint
  by the declared Spider validation rule; account for any added final A in
  every control. Existing evidence favors private consolidation after K.
- The old 25–30 GPU-hour estimate covers only Hinton plus gold interleaving;
  controls, new endpoints, and the selected R need a revised cost estimate.
- Needed code: a K stage on a row shard, and an R-round schedule runner.

## A3. Consolidation depth after one K (planned, no command activated)

Test the family `A>K>A^m`, not a fixed `A>K>A>A>A`. The private MedQA example
reported by the owner is motivation only, not a source, replication target,
or evidence for Spider. The question is whether K supplies a useful starting
point that benefits from more task-specific private training.

| Arm at depth m | Purpose |
|---|---|
| `A^(m+1)` | Pure FL with the same number of private rounds |
| `A>K[gold]>A^m` | Public-data adaptation control |
| `A>K[KD]>A^m` | Public teacher pipeline |

- Start with the SQL-only Hinton/full-gold pair on the same 9,428 BIRD rows
  and its pure-FL control. Their committed m=1 endpoints already exist.
  Reuse them only with verified adapter bytes and matching continuation
  contracts; append fresh immutable A stages without repeating K. Never use
  a KD-derived adapter as the pure-FL parent.
- Freeze a small maximum m and a common validation/plateau rule before a new
  run. Evaluate matched checkpoints along the trajectory, including m=0 and
  m=1 where available. A larger m may help, saturate, or hurt; it is not a
  presumed improvement. Historical dev-guided screens remain exploratory.
- Match clients, splits, local epochs, private optimizer/reset/LR policy,
  seed, LoRA, prompts, aggregation, and evaluator across all arms. Equal A
  count matches private exposure, not total compute. Report public-stage cost
  and compare with additional private training at similar compute if claiming
  overall efficiency.
- Track Spider EX, KD-minus-FL, gold-minus-FL, and KD-minus-gold at every
  matched depth, with paired wins/losses. Preserve all checkpoint results;
  do not independently cherry-pick each arm's best test score. Distinguish
  higher final EX from reaching the same EX in fewer private rounds.
- If P2.11 is competitive, apply the same depth protocol to its SQL-only
  client lineage, retaining SeqKD and template/extra-exposure controls. Do
  not combine a new schedule, plan format, and teacher in one comparison.
- If all arms plateau together, extra A does not rescue a teacher-specific
  claim. If KD loses an advantage only after A, investigate placement or
  interleaving next. If KD beats matched FL but ties gold, retain the pipeline
  finding and its attribution limit.
- Isolate placement later as `A^r>K>A^(R-r)` at fixed total R and K budget;
  do not run a full depth-by-placement-by-objective sweep before a signal.
- Before activation: verify continuation and checkpoint selection in the
  runner, freeze the horizon/validation contract, and add separate run and
  publication commands. No new result or GPU execution is implied here.

# Direction 2: Struct-SQL with a client fix

Private Spider data has only gold SQL. P2.10's template-plan recipe
underperformed. P2.11 keeps clients SQL-only; P2.12 masks direct plan loss but
still conditions SQL training on generated or fallback template plans.

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

- `tplan − seqkd` screens the whole added training task: it also adds 1,000
  examples, steps, and a longer LR trajectory, so it does not isolate plans.
- `tplan − aplan` compares teacher versus template targets on identical rows
  and step counts; target lengths/compute can differ. A harmful template is
  not enough evidence that teacher reasoning beats no-plan training.
- If promising, add SQL-only exposure on those same 1,000 rows, matching the
  base SQL stream and update/LR budget; report token and compute differences.
- Keep the same FL T1 parent and SQL recipe. Check absolute terminal Spider
  EX against the stronger full-gold/Hinton endpoints as practical references,
  not as equal-data causal controls for P2.11.
- Cost: about 6–8 GPU-hours per arm (K, commit, terminal A, two evaluations).
- Runner `scripts/run_p211_aux_plan.py`, nested branch `experiment/struct-aux-cot`,
  commit `4fc9c61` or later. Detailed phase notes: `docs/P211_P212_RUNBOOK.md`.
- Loss mode `full_bf16`, the mode of the committed SeqKD rows, so the plan task
  is the only difference against them.

`experiment/struct-aux-cot` contains the A1 code. Before the branch-changing
launch command below, wait for jobs using that worktree to exit, or use a
separate worktree with disjoint outputs, as required by `CONVENTION.MD` 6.1.
GPU 0, both arms in order (`tplan`, then `aplan`), about 6–7 h per arm:

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

- Masking plan labels removes direct plan CE, not updates to shared parameters.
  SQL gradients can still change the ability to generate plans; preservation
  of teacher style is a hypothesis, not a guarantee.
- The implemented policy is self-correct plan, then gold-hinted
  rationalization, then AST-template fallback. Audit these proportions and
  plan quality before a full screen. Execution-correct SQL does not validate
  each reasoning step or its structural agreement with the gold SQL target.
- This only changes the final private stage; it inherits the P2.10 parent.
  Inference still needs a generated CoT. Use strict and SQL-marker EX and
  matching public-parent/plain-terminal controls.
- Cost: plan generation about 2–3 h per arm, the round about 1.9 h, evaluation
  about 2 h.
- Lower priority than P2.11 and the simple depth screen. Runner
  `scripts/run_p212_latent_plan.py` is ready; activation depends on the plan
  audit and evidence, not an automatic step after P2.11.

Older finished runbooks: `paper/archive/completed_runbooks/` and
`paper/archive/superseded_runbooks/`. They are history, not the queue.
