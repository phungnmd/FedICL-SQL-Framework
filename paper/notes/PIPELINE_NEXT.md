# FedLS-SQL — active protocol-v2 queue

> Run from the `fedicl-sql/` repository root on the Windows experiment server.
> Every command is one physical PowerShell line. Exact reruns resume or skip
> completed work; no command deletes artifacts.

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
| P2.1R | Full-context BIRD baseline (`max_len=7168`, fail closed) | GPU 0 | next: longest-row smoke, then corrected full run |
| P2.2 | Current FedLS reference ladder in both directions | GPU | blocked by P2.1R |
| P2.3 | Diagnose and improve KD/Federated method | adaptive | blocked by P2.2 |

P2.1 is an explicitly labeled diagnostic track. Audit found 974 truncated train
prompts and complete evidence loss in 754 rows; its scores must not enter the
paper's canonical table. Independent EX rescore changed only one centralized-E1
row and found no disk-full recurrence, so evaluator repair is not required.

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

This invokes only exact paths from the committed 31-entry manifest. Cleanup is
a recoverable move into `artifacts/archive/protocol_v1_no_bird_evidence/`; active
or partial roots are refused. The new split is rejected if it loses rows, has a
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
setup/stage fingerprints; both eval lanes use `bird_official_set_v1` in their
resume fingerprint. Rerun the exact command after interruption.

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
