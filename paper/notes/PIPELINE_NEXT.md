# FedLS-SQL — active protocol-v2 queue

## Current decision

P2.6 is complete and published in nested commit `fb2329e`: flat SeqKD does not
clear the matched selected-gold terminal gate strongly enough to justify
scaling the same objective. Its completed runbook is archived at
[P26_MATCHED_GOLD_2026-09-21.md](../archive/completed_runbooks/P26_MATCHED_GOLD_2026-09-21.md).

The only active GPU gate is **P2.7**, a bounded structured-rationale screen that
follows Struct-SQL admission. Qwen2.5-Coder-7B (4-bit) sees schema, BIRD evidence
and question, never a reference SQL, and generates a query plan and SQL together
(one greedy attempt, no repair). A sample is kept only when its SQL executes to
the gold result. Candidates come from the full BIRD train split (9,428 rows),
bucketed by `sqlglot_complexity_v1`; each bucket is walked in a fixed seed-0 order
until 1,000 rows in total are admitted. The three arms share those rows and that
teacher SQL; only the plan differs:

| Arm | Public target | Response format |
|---|---|---|
| `seqkd_flat_1000` | admitted teacher SQL | SQL only |
| `qplan_local_1000` | deterministic SQL-AST plan + same teacher SQL | plan + SQL |
| `qplan_teacher_1000` | teacher's own plan + same teacher SQL | plan + SQL |

All three arms use the same Spider-private FedAvg T1 parent, one public epoch,
seed 0, optimizer/LoRA recipe and five evaluation sets. P2.7 is an experimental
method gate, not yet a paper result.

The first P2.7 variant (teacher explains the fixed SQL, plan validator with two
repairs) stopped on 2026-09-22 at 97.1% first-attempt validation with 22 rejected
rows, mostly validator false positives. It is shelved; its server artifacts under
`processed_data/protocol_v2/rationale_kd/p27_bird_selected1000_s0/` stay
untouched and unpublished. All new roots use `p27_joint` / `p27_bird_joint1000`.

Required nested branch: `experiment/structured-rationale-kd`, containing commit
`985d120` or a descendant (already pushed).

## Step 0 — server sync and validation

Run from the Windows server `fedicl-sql/` root. This does not switch `main`.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git fetch origin experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch fetch failed' }; git switch experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch switch failed' }; git pull --ff-only origin experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch pull failed' }; git merge-base --is-ancestor 985d120 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required P2.7 joint-generation commit 985d120 is missing' }; $Scope=@('fedicl_sql','experiments','scripts','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=all -- $Scope | Where-Object { $Path=$_.Substring(3).Trim('"').Replace('\','/'); $Path -notmatch '^experiments/[^/]+/results/' }); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code scope is dirty' }; uv run --extra dev python -m pytest -q tests/test_rationale_sql_plan.py tests/test_rationale_targets.py tests/test_rationale_scripts.py tests/test_p27_rationale_runner.py tests/test_stage_chain.py; if ($LASTEXITCODE -ne 0) { throw 'P2.7 validation failed' }; git log -1 --oneline
```

## Step 1 — GPU 0 joint teacher generation gate

This builds the complexity-stratified candidate order, then runs resumable joint
plan+SQL generation until 1,000 execution-correct rows are admitted (estimated
8–10 GPU hours at about 50% admission). Stop if the parse rate is below 99% or a
complexity bucket runs out of candidates; do not spend GPU time on the three arms.
The EX admission rate and plan diagnostics are reported, not gated.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p27_rationale_screen.py --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.7 candidate preparation failed; rerun this exact line' }; uv run python scripts/run_p27_rationale_screen.py --phase generate-plans; if ($LASTEXITCODE -ne 0) { throw 'P2.7 joint teacher generation failed; rerun this exact line' }; $P='processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/train.csv.provenance.json'; $V=Get-Content -LiteralPath $P -Raw | ConvertFrom-Json; if ($V.n_rows -ne 1000 -or -not $V.generation_gate_passed -or $V.parse_rate -lt 0.99) { throw "P2.7 generation gate failed: rows=$($V.n_rows) parse=$($V.parse_rate) accepted=$($V.n_accepted) ex_accept=$($V.ex_acceptance_rate)" }; Write-Host "P2.7 generation gate passed: parse=$($V.parse_rate) ex_accept=$($V.ex_acceptance_rate) generated=$($V.n_generated) plan_schema_valid=$($V.accepted_plan_schema_valid_rate) plan_select=$($V.accepted_plan_mentions_select_rate); start both training lanes"
```

## Step 2 — two concurrent GPU lanes

Start these only after Step 1 passes. They write disjoint training/evaluation
roots; the shared audit manifest is protected by an inter-process file lock.

GPU 0 — teacher-generated query plans:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p27_rationale_screen.py --phase train-teacher; if ($LASTEXITCODE -ne 0) { throw 'P2.7 teacher-plan training failed; rerun this exact line' }; uv run python scripts/run_p27_rationale_screen.py --phase eval --arm teacher; if ($LASTEXITCODE -ne 0) { throw 'P2.7 teacher-plan evaluation failed; rerun this exact line' }; Write-Host 'GPU-0 complete: qplan_teacher_1000 trained and evaluated on five sets'
```

GPU 1 — flat SeqKD control, then deterministic local-plan control:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p27_rationale_screen.py --phase train-flat; if ($LASTEXITCODE -ne 0) { throw 'P2.7 flat-control training failed; rerun this exact line' }; uv run python scripts/run_p27_rationale_screen.py --phase eval --arm flat; if ($LASTEXITCODE -ne 0) { throw 'P2.7 flat-control evaluation failed; rerun this exact line' }; uv run python scripts/run_p27_rationale_screen.py --phase train-local; if ($LASTEXITCODE -ne 0) { throw 'P2.7 local-plan training failed; rerun this exact line' }; uv run python scripts/run_p27_rationale_screen.py --phase eval --arm local; if ($LASTEXITCODE -ne 0) { throw 'P2.7 local-plan evaluation failed; rerun this exact line' }; Write-Host 'GPU-1 complete: flat and qplan_local controls trained and evaluated on five sets'
```

Both commands are resumable by rerunning the exact same line. Do not pull,
checkout, edit scientific code, commit or publish while either lane is active.

## Step 3 — CPU analysis and decision

Run only after both GPU lanes complete.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p27_rationale_screen.py --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.7 paired analysis failed' }; $S=Get-Content -LiteralPath 'audits/protocol_v2/p27_joint_rationale_screen_s0/summary.json' -Raw | ConvertFrom-Json; $S.sets.PSObject.Properties | ForEach-Object { $N=$_.Name; $A=$_.Value.arms; Write-Host "${N}: flat=$($A.flat.ex) local=$($A.local.ex) teacher=$($A.teacher.ex)" }; Write-Host "decision=$($S.decision) spider_family_mean_delta=$($S.spider_family_mean_delta_teacher_vs_flat)"; $S.gates | Format-List
```

## Step 4 — publish compact P2.7 evidence

Run only after Step 3 succeeds and no GPU process is using this worktree. This
stages only exact compact files resolved from the locked run manifest; adapters,
resume roots and model caches remain outside Git.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $Manifest='audits/protocol_v2/p27_joint_rationale_screen_s0/run_manifest.json'; $Summary='audits/protocol_v2/p27_joint_rationale_screen_s0/summary.json'; $SummaryMd='audits/protocol_v2/p27_joint_rationale_screen_s0/summary.md'; foreach ($P in @($Manifest,$Summary,$SummaryMd)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P2.7 audit file: $P" } }; $M=Get-Content -LiteralPath $Manifest -Raw | ConvertFrom-Json; $S=Get-Content -LiteralPath $Summary -Raw | ConvertFrom-Json; if ($M.experiment -ne 'p27_rationale_screen' -or $S.experiment -ne 'p27_rationale_screen' -or @($M.stages.PSObject.Properties).Count -ne 3 -or @($M.evaluations.PSObject.Properties).Count -ne 3) { throw 'P2.7 manifest/summary is incomplete' }; $Files=[System.Collections.Generic.List[string]]::new(); foreach ($P in @('processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/candidates.json','processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/generation.ckpt.jsonl','processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/generation.ckpt.meta.json','processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/train.csv','processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/train.csv.provenance.json','processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/teacher_plans_qwen25_coder_7b.jsonl','processed_data/protocol_v2/rationale_kd/p27_bird_joint1000_s0/teacher_plans_qwen25_coder_7b.jsonl.provenance.json',$Manifest,$Summary,$SummaryMd)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing allowlisted file: $P" }; $Files.Add($P) }; foreach ($Stage in $M.stages.PSObject.Properties.Value) { foreach ($Name in @('metrics.json','config.json')) { $P=Join-Path $Stage.result_dir $Name; if (-not (Test-Path -LiteralPath $P)) { throw "Missing stage result: $P" }; $Files.Add($P) } }; foreach ($Arm in $M.evaluations.PSObject.Properties.Value) { foreach ($Eval in $Arm.PSObject.Properties.Value) { foreach ($P in @($Eval.metrics,$Eval.config,$Eval.predictions)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing eval result: $P" }; $Files.Add([string]$P) } } }; $Rel=@($Files | ForEach-Object { ([string]$_).Replace('\','/') } | Sort-Object -Unique); if (@($Rel | Where-Object { $_ -like 'artifacts/*' }).Count -ne 0) { throw 'Artifact/resume path entered publication allowlist' }; git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'P2.7 staging failed' }; $Got=@(git diff --cached --name-only | Sort-Object); $Want=@($Rel | Sort-Object); if ($Got.Count -ne $Want.Count -or @(Compare-Object $Got $Want).Count -ne 0) { $Got | ForEach-Object { Write-Host "staged=$_" }; throw 'P2.7 staged allowlist mismatch' }; git diff --cached --check; if ($LASTEXITCODE -ne 0) { throw 'P2.7 staged content check failed' }; git commit -m 'results: publish P2.7 structured rationale screen'; if ($LASTEXITCODE -ne 0) { throw 'P2.7 commit failed' }; git push origin experiment/structured-rationale-kd; if ($LASTEXITCODE -ne 0) { throw 'P2.7 push failed' }; git log -1 --oneline
```

## Decision after P2.7

Scale beyond the bounded screen (`decision=promote_full_scale`) only if every
pre-registered gate in the analysis summary passes: teacher parse rate of at least
99% with exactly 1,000 admitted rows, teacher-plan BIRD gain
of at least 1.5 EX over flat SeqKD, positive gain over local plans, Spider-family
mean gain of at least 0.5 EX, and no individual Spider-family regression worse
than 1.0 EX. Otherwise close teacher-rationale KD for the current paper and do
not spend GPU time on a full-pool or multi-seed extension.
