# FedLS-SQL — active protocol-v2 queue

## Current decision

The operator reports that P2.7 Step 1 (1,000 execution-admitted joint teacher
plan+SQL rows) has finished on the Windows server. This report is not a local
artifact verification; Step 1 below checks the frozen provenance before any
new training. The former three-arm public-only P2.7 queue is preserved in
[P27_THREE_ARM_SCREEN_2026-09-23.md](../archive/superseded_runbooks/P27_THREE_ARM_SCREEN_2026-09-23.md).
Its flat and AST-plan arms remain optional diagnostics. The active scientific
question is whether structured teacher KD beats source-gold training on exactly
the same 1,000 public rows, and whether that advantage survives an identical
terminal private/FedAvg stage A.

P2.8 compares two paths from the same committed Spider-private A parent:

| Arm | Public target | Public inference | Terminal A | Final inference |
|---|---|---|---|---|
| gold | source BIRD gold SQL | SQL only | one Spider client epoch, FedAvg | SQL only |
| teacher | admitted teacher plan + teacher SQL | plan + SQL | same one Spider client epoch, FedAvg | SQL only |

Questions, row IDs/order, databases, BIRD evidence, public pass, student, LoRA
and seed are matched. The output formats differ at the public endpoint because
the structured teacher recipe includes a plan; both final endpoints use SQL-only
inference because terminal A trains with private SQL-only targets. The primary
decision is the **final**, not public, teacher-minus-gold EX. This is a seed-0
screen; promotion requires independent-seed confirmation. The selection
conditions on teacher-correct public rows, so do not generalize it to an
unlabeled or teacher-unfiltered pool.

Required nested feature branch commit: 6458b33 or a descendant. Local commits
must reach the server branch before Step 0. Do not pull or change scientific
code while a GPU lane runs.

## Step 0 — sync and validate on the Windows server

Run from the fedicl-sql/ repository root. This does not switch main.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git fetch origin experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch fetch failed' }; git switch experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch switch failed' }; git pull --ff-only origin experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch pull failed' }; git merge-base --is-ancestor 6458b33 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required P2.8 code commit is missing' }; $Scope=@('fedicl_sql','experiments','scripts','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=all -- $Scope | Where-Object { $Path=$_.Substring(3).Trim('"').Replace('\','/'); $Path -notmatch '^experiments/[^/]+/results/' }); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code scope is dirty' }; uv run --extra dev python -m pytest -q tests/test_p28_struct_gold_gate.py tests/test_p28_publication.py tests/test_p27_rationale_runner.py tests/test_stage_chain.py tests/test_eval.py tests/test_eval_arms_config.py tests/test_eval_arms_cli.py; if ($LASTEXITCODE -ne 0) { throw 'P2.8 validation failed' }; git log -1 --oneline
```

## Step 1 — CPU: verify Step 1 generation and build matched gold

This command verifies P2.7 candidate/subset/plan provenance, then joins
source-gold SQL by stable source_row_id. It refuses changed bytes on rerun.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p28_struct_gold_gate.py --phase prepare-gold; if ($LASTEXITCODE -ne 0) { throw 'P2.8 exact-row gold preparation failed' }; $P='processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/train.csv.provenance.json'; $G='processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/matched_source_gold_train.csv.provenance.json'; $V=Get-Content -LiteralPath $P -Raw | ConvertFrom-Json; $C=Get-Content -LiteralPath $G -Raw | ConvertFrom-Json; if ($V.n_rows -ne 1000 -or -not $V.generation_gate_passed -or $C.n_rows -ne 1000) { throw 'P2.7 admission or P2.8 matched-gold count failed' }; Write-Host "P2.8 ready: teacher_rows=$($V.n_rows) gold_rows=$($C.n_rows) parse_rate=$($V.parse_rate)"
```

## Step 2 — two GPU lanes

Start after Step 1 passes. The lanes use distinct training/evaluation roots;
their shared P2.8 manifest is protected by a file lock. Rerun the exact lane
command after an interruption. Do not pull, checkout, edit scientific code,
commit or publish while either lane is active.

GPU 0 — structured teacher public stage and terminal A:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p28_struct_gold_gate.py --phase train-public --arm teacher; if ($LASTEXITCODE -ne 0) { throw 'Teacher public training failed' }; uv run python scripts/run_p28_struct_gold_gate.py --phase eval-public --arm teacher; if ($LASTEXITCODE -ne 0) { throw 'Teacher public evaluation failed' }; uv run python scripts/run_p28_struct_gold_gate.py --phase train-terminal --arm teacher; if ($LASTEXITCODE -ne 0) { throw 'Teacher terminal A failed' }; uv run python scripts/run_p28_struct_gold_gate.py --phase eval-terminal --arm teacher; if ($LASTEXITCODE -ne 0) { throw 'Teacher terminal evaluation failed' }; Write-Host 'GPU-0 complete: teacher public and terminal endpoints evaluated on five sets'
```

GPU 1 — matched source-gold public stage and identical terminal A:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p28_struct_gold_gate.py --phase train-public --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Gold public training failed' }; uv run python scripts/run_p28_struct_gold_gate.py --phase eval-public --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Gold public evaluation failed' }; uv run python scripts/run_p28_struct_gold_gate.py --phase train-terminal --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Gold terminal A failed' }; uv run python scripts/run_p28_struct_gold_gate.py --phase eval-terminal --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Gold terminal evaluation failed' }; Write-Host 'GPU-1 complete: gold public and terminal endpoints evaluated on five sets'
```

## Step 3 — CPU: paired analysis and decision

Run only after both lanes finish. It checks exact prediction identities and
hashes, then reports EX, wins/losses and exact McNemar p on all five sets at
both endpoints. The final gate requires BIRD gain at least 1.0 EX, four-set
Spider-family mean gain at least 0.5 EX, and no individual Spider-family
regression worse than 1.0 EX. Passing promotes multi-seed confirmation; it is
not itself a paper-level reliability claim.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p28_struct_gold_gate.py --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.8 matched paired analysis failed' }; $S=Get-Content -LiteralPath 'audits/protocol_v2/p28_struct_gold_terminal_s0/summary.json' -Raw | ConvertFrom-Json; $S.sets.PSObject.Properties | ForEach-Object { $N=$_.Name; $T=$_.Value.terminal; Write-Host "$($N): gold=$($T.gold_ex) teacher=$($T.teacher_ex) delta=$($T.teacher_vs_gold.delta_ex) p=$($T.teacher_vs_gold.mcnemar_exact_p)" }; Write-Host "decision=$($S.decision) spider_family_mean_delta=$($S.terminal_spider_family_mean_delta)"; $S.gates | Format-List
```

## Step 4 — publish compact P2.8 evidence

Run only after Step 3 succeeds and no GPU process uses this worktree. This
publishes the frozen P2.7 generation snapshot, matched-gold pool, four compact
stage rows, paired analyses, and 20 compact evaluation triplets. It excludes
adapters, mutable caches and trainer state.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $Rel=@(uv run python scripts/list_p28_publication.py); if ($LASTEXITCODE -ne 0 -or $Rel.Count -ne 79) { throw "P2.8 publication allowlist invalid: files=$($Rel.Count)" }; git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'P2.8 staging failed' }; $Got=@(git diff --cached --name-only | Sort-Object); $Want=@(git diff HEAD --name-only -- $Rel | Sort-Object); if ($Got.Count -ne $Want.Count -or @(Compare-Object $Got $Want).Count -ne 0) { throw 'P2.8 staged allowlist mismatch' }; if ($Got.Count -gt 0) { git diff --cached --check; if ($LASTEXITCODE -ne 0) { throw 'P2.8 staged content check failed' }; git commit -m 'results: publish P2.8 matched gold terminal gate'; if ($LASTEXITCODE -ne 0) { throw 'P2.8 commit failed' }; git push origin experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'P2.8 push failed' } } else { Write-Host 'P2.8 evidence already committed' }; git log -1 --oneline
```

## Decision after P2.8

If the final teacher arm does not clear the matched-gold gate, close this
structured KD recipe for the current paper. A public-only win is insufficient.
If it clears the gate, run independent training seeds and then one stronger
non-IID split before claiming a robust Fed+KD benefit. The P2.7 flat and local
plan controls may still explain *why* a confirmed teacher benefit occurs.
