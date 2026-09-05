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
| P2.0e | Materialize/audit BIRD-original and semantic K5 split | CPU | ready |
| P2.1 | Base, centralized E1/E2, pure-FL T1/T2/T3 with evidence | GPU 0 | results published `f99febd`; audit before acceptance |
| P2.1q | Actual train token retention + independent dev gold and saved-prediction EX audit | CPU | next; no generation or retraining |
| P2.2 | Current FedLS reference ladder in both directions | GPU | blocked by P2.1 analysis |
| P2.3 | Diagnose and improve KD/Federated method | adaptive | blocked by P2.2 |

P2.1 is an explicitly labeled `BIRD-original + evidence` compatibility track.
It provides the corrected baseline evidence now. The 6,601-row official
filtered-train release remains a later matched data-quality experiment rather
than silently replacing this lineage.

## Next: P2.1q baseline integrity audit

Run on the Windows server containing the original BIRD SQLite files and cached
Qwen tokenizer, after pulling the audit implementation. No GPU is required.
This checks correct BIRD use; it does not compare evidence on versus off.
Train evidence retention and SQL rescore require server data absent locally.
The complete protocol is in `BIRD_BASELINE_AUDIT.md`.

Sync once while no experiment is active in this worktree:

```powershell
git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor 0bf1ef0 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Missing BIRD audit commit 0bf1ef0' }
```

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_bird_baseline_audit.ps1 -Phase Run; if ($LASTEXITCODE -ne 0) { throw 'P2.1q CPU audit stopped; rerun this exact line to resume' }
```

Publish after Run completes, including when `requires_review=True` (that is an
audit finding to analyze, not permission to promote accuracy claims):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_bird_baseline_audit.ps1 -Phase Publish; if ($LASTEXITCODE -ne 0) { throw 'P2.1q audit publication failed; inspect output and retry Publish' }; git log -1 --oneline
```

The immutable contract binds tokenizer, script, data and database hashes. Resume
the same command. The audit preserves original predictions and publishes only
`contract.json`, `tokens.json`, `rows.jsonl`, and `summary.json` from its exact root.
After reviewing this audit, prioritize Spider-private FL → BIRD-public KD →
Spider evaluation. The BIRD-private reverse direction follows the main flow.

## Completed P2.1 baseline runner — reference commands

The single server runner is `scripts/run_protocol_v2_baselines.ps1`. Its phases
are separated because dataset publication must precede GPU work, while result
publication must occur only after all GPU processes exit.

### 1. Sync and validate the refactor

Run only when no experiment is active in this worktree.

```powershell
$Expected='d1df12d'; $Scope=@('fedicl_sql','experiments/client_train/run.py','experiments/federated/run.py','experiments/eval_arms/run.py','scripts','tests','configs/archive/protocol_v1_no_bird_evidence.json','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Tracked scientific code is dirty; review before pulling' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward pull failed' }; $Head=(git rev-parse --short HEAD).Trim(); if ($Head -ne $Expected) { throw "Expected code commit $Expected, found $Head" }; powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Validate; if ($LASTEXITCODE -ne 0) { throw 'Protocol-v2 server validation failed' }
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

### 3. Full overnight P2.1 computation

This invocation uses only physical GPU 0 and runs four stages sequentially:
centralized continuous E1/E2, pure FedAvg T1/T2/T3, base + E1 + E2 evaluation,
then T1 + T2 + T3 evaluation. GPU 1 is never selected (`e1f3127`).

Every training output is under `artifacts/protocol_v2/`. Centralized training
retains adapter-only epoch snapshots plus one `resume_latest`; FL uses immutable
setup/stage fingerprints; both eval lanes use `bird_official_set_v1` in their
resume fingerprint. Rerun the exact command after interruption.

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase Full; if ($LASTEXITCODE -ne 0) { throw 'P2.1 full baseline suite stopped; rerun this exact line to resume completed checkpoints and eval rows' }
```

Publication command — invoke only after the sequential GPU-0 run has exited:

```powershell
powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_baselines.ps1 -Phase PublishResults; if ($LASTEXITCODE -ne 0) { throw 'P2.1 allowlisted result publication failed; inspect manifests before retrying' }
```

## What the runner does not run

It does not regenerate teacher targets, run RKL, or select the final FedLS
method. Those would mix method selection into the protocol repair. First compare
base, centralized E1/E2, and FL T1/T2/T3 by BIRD official EX and execution-error
transitions. P2.2 then reruns matched public-gold, teacher-target CE, and CE+RKL
controls; P2.3 changes KD or federated mechanics only when that diagnosis gives
a concrete target.
