# FedLS-SQL — active protocol-v2 queue

> Run from the `fedicl-sql/` repository root on the Windows experiment server.
> Every command is one physical PowerShell line. Exact reruns resume or skip
> completed work; no command deletes artifacts.
> The retained result/adapter allowlist is `VALID_RESULTS_AND_ADAPTERS.md`.

## Active order

| Order | Task | Device | Status |
|---|---|---|---|
| P2.0a | Explicit Spider/BIRD profiles, evidence plumbing, lineage audit | CPU | complete |
| P2.0b | Quarantine known invalid protocol-v1 BIRD artifacts | CPU | ready in runner; recoverable move only |
| P2.0c | Official filtered BIRD train/cleaned-dev release | CPU | optional final-release gate; files pending |
| P2.0d | Official BIRD SQLite EX adapter + versioned fingerprint fixture | CPU | complete: `9d777db` |
| P2.0e | Materialize/audit BIRD-original and semantic K5 split | CPU | complete |
| P2.1 | Legacy-width BIRD baseline (`max_len=2560`) | complete | diagnostic only; input truncation found |
| P2.1q | Token-retention and independent EX audit | CPU | complete `e9bde43`; scorer accepted, checkpoints rejected |
| P2.1R | Full-context BIRD baseline (`max_len=7168`, fail closed) | GPU 0 | complete on server; publication pending |
| P2.2a | Evidence-aware Qwen-7B raw targets on BIRD train | GPU 1 | partial checkpoint; resume through closure runner |
| P2.1S | Rescore saved P2.1R SQL with official 30-second BIRD pair deadline | CPU | automated by closure runner after both GPU lanes |
| P2.2b | BIRD gold audit, corrected target selection, teacher dev EX | CPU + GPU 0/1 | active through closure runner |
| P2.2 | Current FedLS reference ladder in both directions | GPU | blocked by P2.2b |
| P2.3 | Diagnose and improve KD/Federated method | adaptive | blocked by P2.2 |

P2.1 is an explicitly labeled diagnostic track. Audit found 974 truncated train
prompts and complete evidence loss in 754 rows; its scores must not enter the
paper's canonical table. Independent EX rescore changed only one centralized-E1
row and found no disk-full recurrence, so evaluator repair is not required.

## Current command: close P2.1R/P2.2 prerequisites

Use `scripts/run_protocol_v2_teacher_closure.ps1`. Its `Full` phase does **not**
rerun P2.1R. It validates the code and inputs, evaluates the Qwen-7B teacher on
BIRD dev on GPU 0, resumes the existing row-level raw-target checkpoint on GPU
1, and runs the teacher-independent gold audit on CPU. After both GPU lanes
complete it automatically runs the corrected BIRD selector, builds the
row-matched gold control, and rescores the six saved P2.1R prediction files
with the official 30-second pair deadline. Child logs are written under
`artifacts/protocol_v2/run_logs/p22_teacher_closure/`.

Run only after yesterday's processes have exited. This is one physical line;
rerunning it safely skips or resumes completed work:

```powershell
$Scope=@('fedicl_sql','experiments/eval_arms/run.py','scripts','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code is dirty; review before pull' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_teacher_closure.ps1 -Phase Full; if ($LASTEXITCODE -ne 0) { throw 'P2.2 closure stopped; rerun this exact line to resume' }
```

The runner deliberately stops before FedLS training. Teacher-dev EX and the
selected-pool size determine the matched-gold, SeqKD, and RKL commands, so that
next ladder must be frozen only after these outputs are inspected.

## Concurrent P2.2 teacher lane

While P2.1R evaluates on GPU 0, GPU 1 may resume only raw BIRD teacher
generation. This invocation does not call the selector and resumes the existing
row-level checkpoint.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $B='processed_data/protocol_v2/BIRD/original_train9428_dev1534/teacher_targets/qwen7b_to_qwen15b_evidence_s0'; $R="$B/raw/train.csv"; if (-not (Test-Path -LiteralPath $S)) { throw "Missing BIRD protocol-v2 train: $S" }; uv run python scripts/build_teacher_targets.py --source-csv $S --dataset-profile bird_with_evidence --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --student-model Qwen/Qwen2.5-1.5B-Instruct --teacher-4bit --batch-size 1 --max-new-tokens 256 --schema-style full --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Evidence-aware raw teacher generation stopped; rerun this exact line to resume' }; $RV=Get-Content -LiteralPath "${R}.provenance.json" -Raw | ConvertFrom-Json; if ((Import-Csv -LiteralPath $R).Count -ne 9428 -or $RV.dataset_profile -ne 'bird_with_evidence' -or $RV.evidence_mode -ne 'provided' -or $RV.max_new_tokens -ne 256) { throw 'Raw teacher-target contract mismatch' }; Write-Host 'P2.2a complete: 9,428 evidence-aware raw targets; no selection was run'
```

After all P2.1R processes exit, pull the corrected selector/evaluator and close the
teacher lane. New `bird_official_set_pair_timeout30_v2` roots cannot reuse an older
checkpoint. The train statistic is selection coverage; teacher benchmark EX is
measured separately on BIRD dev.

Before publishing P2.1R accuracy, rescore its six saved SQL files on CPU. The
manifest paths are resolved explicitly; this does not load either model or
regenerate a token.

```powershell
$Required='2178d5a'; git merge-base --is-ancestor $Required HEAD; if ($LASTEXITCODE -ne 0) { throw "Missing official BIRD timeout commit $Required" }; $env:CUDA_VISIBLE_DEVICES=''; $env:PYTHONUTF8='1'; $D='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv'; $C='artifacts/eval_resume/protocol_v2/p21r_bird_original_ctx7168_central_birdsetv1_s0'; $F='artifacts/eval_resume/protocol_v2/p21r_bird_original_ctx7168_fl_birdsetv1_s0'; $O='audits/protocol_v2/p21r_bird_original_ctx7168_bird_pair_t30_s0'; $CM=@(Get-ChildItem -LiteralPath "$C/manifests" -Filter '*.json' -File); $FM=@(Get-ChildItem -LiteralPath "$F/manifests" -Filter '*.json' -File); if ($CM.Count -ne 1 -or $FM.Count -ne 1) { throw "Expected one completed manifest per P2.1R lane: central=$($CM.Count) fl=$($FM.Count)" }; $CV=Get-Content -LiteralPath $CM[0].FullName -Raw | ConvertFrom-Json; $FV=Get-Content -LiteralPath $FM[0].FullName -Raw | ConvertFrom-Json; if ($CV.status -ne 'completed' -or $FV.status -ne 'completed') { throw 'P2.1R evaluation manifest is incomplete' }; $Pred=@($CV.artifacts.predictions)+@($FV.artifacts.predictions); if ($Pred.Count -ne 6) { throw "Expected six P2.1R prediction files, found $($Pred.Count)" }; foreach ($Path in $Pred) { if (-not (Test-Path -LiteralPath $Path)) { throw "Missing prediction file: $Path" } }; uv run python scripts/rescore_bird_predictions.py --test-csv $D --predictions @Pred --out $O --workers 4; if ($LASTEXITCODE -ne 0) { throw 'Official BIRD 30-second rescore stopped; rerun this exact line to resume' }; $V=Get-Content -LiteralPath "$O/summary.json" -Raw | ConvertFrom-Json; if ($V.execution_evaluator -ne 'bird_official_set_pair_timeout30_v2' -or $V.n_rows -ne 1534 -or @($V.arms.PSObject.Properties).Count -ne 6) { throw 'P2.1R official rescore contract mismatch' }; Write-Host 'P2.1S complete: six saved prediction files rescored; inspect summary.json before publication'
```

```powershell
$Required='2178d5a'; $Scope=@('fedicl_sql','experiments/eval_arms/run.py','scripts/build_teacher_targets.py','scripts/filter_teacher_targets_exmatch.py','scripts/audit_gold_execution.py','scripts/build_public_gold_control.py','scripts/rescore_bird_predictions.py','tests/test_filter_teacher_targets_exmatch.py','tests/test_build_public_gold_control.py','tests/test_rescore_bird_predictions.py','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code is dirty; stop before pull' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor $Required HEAD; if ($LASTEXITCODE -ne 0) { throw "Missing corrected BIRD evaluator $Required" }; $env:PYTHONUTF8='1'; uv run --extra dev python -m pytest -q tests/test_filter_teacher_targets_exmatch.py tests/test_build_public_gold_control.py tests/test_rescore_bird_predictions.py tests/test_eval.py tests/test_data_protocol.py; if ($LASTEXITCODE -ne 0) { throw 'Corrected BIRD evaluator validation failed' }; $env:CUDA_VISIBLE_DEVICES='1'; $S='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $D='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv'; $B='processed_data/protocol_v2/BIRD/original_train9428_dev1534/teacher_targets/qwen7b_to_qwen15b_evidence_s0'; $R="$B/raw/train.csv"; $G="$B/gold_audit_t60/train.csv"; $X="$B/exec_bird_pair_timeout30_v2/train.csv"; $P="$B/exmatch_bird_pair_timeout30_v2/train.csv"; $E='artifacts/eval_resume/protocol_v2/p22_qwen7b_bird_dev_evidence_s0/eval_k0'; uv run python scripts/build_teacher_targets.py --source-csv $S --dataset-profile bird_with_evidence --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --student-model Qwen/Qwen2.5-1.5B-Instruct --teacher-4bit --batch-size 1 --max-new-tokens 256 --schema-style full --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Raw teacher generation incomplete; rerun this exact line to resume' }; uv run python scripts/audit_gold_execution.py --source-csv $S --out $G --workers 2 --exec-timeout 60; if ($LASTEXITCODE -ne 0) { throw 'Teacher-independent BIRD train gold audit stopped; rerun this exact line to resume' }; uv run python scripts/filter_teacher_targets_exmatch.py --source-csv $S --teacher-targets $R --exec-out $X --out $P --dataset-profile bird_with_evidence --workers 2 --exec-timeout 8; if ($LASTEXITCODE -ne 0) { throw 'BIRD-correct teacher selection stopped; rerun this exact line to resume' }; $GV=Get-Content -LiteralPath "${G}.provenance.json" -Raw | ConvertFrom-Json; $V=Get-Content -LiteralPath "${P}.provenance.json" -Raw | ConvertFrom-Json; $N=(Import-Csv -LiteralPath $P).Count; if ($V.execution_evaluator -ne 'bird_official_set_pair_timeout30_v2' -or $V.dataset_protocol.dataset_profile -ne 'bird_with_evidence' -or $V.n_source_rows -ne 9428 -or $N -ne $V.n_exmatched -or $N -le 0) { throw 'BIRD teacher-selection contract mismatch' }; $Coverage=[math]::Round(100.0*$N/$V.n_source_rows,2); $Conditional=[math]::Round(100.0*$N/$V.n_scored,2); Write-Host "BIRD-train selection: selected=$N/9428 coverage=$Coverage% match_over_quick_exec_scored=$Conditional% gold_valid=$($GV.n_gold_valid)/9428"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $S --test-csv $D --dataset-profile bird_with_evidence --arms teacher_qwen7b --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --model Qwen/Qwen2.5-Coder-7B-Instruct --model-4bit --batch-size 1 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Qwen-7B BIRD-dev teacher evaluation stopped; rerun this exact line to resume' }; Write-Host 'P2.2b complete: gold audit, BIRD-correct selection, and independent BIRD-dev teacher EX'
```

## Next: P2.1R full-context repair

The corrected runner uses new immutable `bird_original_ctx7168` roots,
`max_len=7168`, `--truncation-policy error`, and gradient checkpointing. The
first command trains all eight longest audited prompts; it is the VRAM gate and
also proves those rows fit without truncation. It uses only physical GPU 0.

Sync once while no experiment is active in this worktree:

```powershell
git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor d21f777 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Missing BIRD full-context repair d21f777' }; powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Validate; if ($LASTEXITCODE -ne 0) { throw 'Protocol-v2 validation failed' }
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase ContextSmoke; if ($LASTEXITCODE -ne 0) { throw 'P2.1R longest-context smoke failed; do not start full training' }
```

After the smoke passes, run the corrected full suite. Exact reruns skip completed
immutable outputs or resume `_ckpt`; they never reuse old P2.1 roots:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Full; if ($LASTEXITCODE -ne 0) { throw 'P2.1R corrected baseline stopped; rerun this exact line to resume' }
```

Publish only after all GPU work exits:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase PublishResults; if ($LASTEXITCODE -ne 0) { throw 'P2.1R allowlisted result publication failed; inspect manifests and retry' }; git log -1 --oneline
```

## Runner preparation — reference commands

The single server runner is `scripts/run_protocol_v2_baselines.ps1`. Its phases
are separated because dataset publication must precede GPU work, while result
publication must occur only after all GPU processes exit.

### 1. Sync and validate the refactor

Run only when no experiment is active in this worktree.

```powershell
$Required='d21f777'; $Scope=@('fedicl_sql','experiments/client_train/run.py','experiments/federated/run.py','experiments/eval_arms/run.py','scripts','tests','configs/archive/protocol_v1_no_bird_evidence.json','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Tracked scientific code is dirty; review before pulling' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward pull failed' }; git merge-base --is-ancestor $Required HEAD; if ($LASTEXITCODE -ne 0) { throw "Required full-context repair $Required is not in HEAD" }; powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Validate; if ($LASTEXITCODE -ne 0) { throw 'Protocol-v2 server validation failed' }
```

### 2. Prepare inputs and quarantine known invalid v1 artifacts

This invokes only exact paths from the committed protocol-v1 and truncated-P2.1
manifests. Cleanup is a recoverable move into `artifacts/archive/`; active or
partial roots are refused. The new split is rejected if it loses rows, has a
client below 150 rows, or gives one client more than 50% of BIRD train.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Prepare -QuarantineLegacy; if ($LASTEXITCODE -ne 0) { throw 'P2.0e preparation/quarantine failed; inspect the printed retirement report or split counts' }
```

Publication command — run immediately after preparation and before GPU work:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase PublishInputs; if ($LASTEXITCODE -ne 0) { throw 'P2.0e input publication failed; do not start GPU runs' }
```

### 3. Corrected P2.1R computation

This invocation first gates the eight longest prompts, then uses only physical GPU 0 and runs four stages sequentially:
centralized continuous E1/E2, pure FedAvg T1/T2/T3, base + E1 + E2 evaluation,
then T1 + T2 + T3 evaluation. GPU 1 is never selected (`e1f3127`).

Every training output is under `artifacts/protocol_v2/`. Centralized training
retains adapter-only epoch snapshots plus one `resume_latest`; FL uses immutable
setup/stage fingerprints. The completed eval lanes used the earlier 60-second
scorer identity; P2.1S rescoring promotes their saved SQL without regeneration.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Full; if ($LASTEXITCODE -ne 0) { throw 'P2.1R full-context suite stopped; rerun this exact line to resume completed checkpoints and eval rows' }
```

Publication command — invoke only after the sequential GPU-0 run has exited:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase PublishResults; if ($LASTEXITCODE -ne 0) { throw 'P2.1R allowlisted result publication failed; inspect manifests before retrying' }
```

## What the runner does not run

It does not regenerate teacher targets, run RKL, or select the final FedLS
method. Those would mix method selection into the protocol repair. First compare
base, centralized E1/E2, and FL T1/T2/T3 by BIRD official EX and execution-error
transitions. P2.2 then reruns matched public-gold, teacher-target CE, and CE+RKL
controls; P2.3 changes KD or federated mechanics only when that diagnosis gives
a concrete target.
