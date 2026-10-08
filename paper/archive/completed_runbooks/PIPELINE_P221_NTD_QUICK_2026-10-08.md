# Completed: P2.21 NTD quick test (2026-10-08)

Status: run and published in nested `30a86ae`. Results in LAB_LOG 2026-10-08. Historical commands only.

---

## P2.21: NTD quick test (priority), seed 0

Question: does FedNTD not-true retention (Lee et al., NeurIPS 2022) keep teacher
knowledge through a private round without costing Spider? One private stage from
the published P2.18 Hinton AKAKA K2 adapter, identical to P2.18 Hinton A3 except
for `--client-retention-lambda 1 --client-retention-temperature 3
--client-retention-mode ntd` (FedNTD defaults beta 1, tau 3). Control: P2.18
Hinton AKAKA A3 (same parent, data, seed). Evaluation: all five sets. About
1.7 h training plus evaluation. Decision rule: LAB_LOG 2026-10-08 (H1).

P2.20 resume no longer depends on the code hash (nested `6307096`), so pulling
now is safe for P2.20. Order on the server:

1. Stop both lanes with Ctrl+C (GPU 0 FedProx, GPU 1 gold K2AAA). Both resume
   later from their checkpoints with the same P2.20 commands.
2. Pull and prepare P2.21, both GPUs idle:

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p221_ntd_quick --phase prepare --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.21 preparation failed' }
```

3. Two terminals concurrently. GPU 0 runs the NTD probe (reserved <=21.5 GiB is
   checked automatically), then the stage and its five evaluations:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($phase in @('probe','run')) { uv run --no-sync python -m scripts.run_p221_ntd_quick --phase $phase --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.21 $phase failed" } }; Write-Host 'GPU 0 lane complete' }
```

GPU 1 resumes gold K2AAA (P2.20):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run --no-sync python -m scripts.run_p220_placement_grid --phase run --arm gold_k2aaa --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.20 gold K2AAA failed' }; Write-Host 'GPU 1 lane complete' }
```

4. Publish P2.21 once both terminals are idle:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p221_ntd_quick --phase analyze --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p221_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.21 NTD quick test'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

FedProx AAA (P2.20 GPU 0 arm) is paused; resume it later with
`--arm fedprox_aaa` before the P2.20 publication.

