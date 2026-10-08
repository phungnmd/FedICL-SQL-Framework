# P2.24 runbook (completed 2026-10-08, results nested `5609a15`)

## P2.24 (GPU 0): two-sided retention screen (v2), seed 0

v1 = Hinton K + client FedNTD (adopted). v2 adds server retention: during the
Hinton K stage the SLM also keeps the not-true distribution of the adapter it
received from FedAvg, on BIRD inputs (FedNTD loss, Learning without Forgetting
placement), so K forgets less Spider. From the published P2.18 Hinton AKAKA
A2: K (`K[fkl,ntd]`, one epoch, beta 1, tau 3), then the P2.21 client-NTD round.
Spider and BIRD after each. Rule: LAB_LOG 2026-10-08 (P2.24). Code: nested
`f2e02be`. Time: probe 10 min, K about 3.3 h, A about 1.7 h, evaluations
about 1.2 h; about 6.3 h.

GPU 1 meanwhile resumes FedProx AAA (P2.20); P2.20 step 4 publishes the grid
once it finishes. P2.22/P2.23 commands are
[archived](../archive/completed_runbooks/PIPELINE_P222_P223_NTD_2026-10-08.md).

1. Stop FedProx if it is running (Ctrl+C), so both GPUs are idle. Pull and
   prepare:

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p224_server_ntd --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.24 preparation failed' }
```

2. GPU 0: the `hinton_ntd` memory probe (must pass reserved <=21.5 GiB; check
   shared GPU memory manually), then both stages and evaluations:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($phase in @('probe','run')) { uv run --no-sync python -m scripts.run_p224_server_ntd --phase $phase; if ($LASTEXITCODE -ne 0) { throw "P2.24 $phase failed" } }; Write-Host 'GPU 0 lane complete' }
```

3. GPU 1, at the same time:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run --no-sync python -m scripts.run_p220_placement_grid --phase run --arm fedprox_aaa --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.20 FedProx AAA failed' }; Write-Host 'GPU 1 lane complete' }
```

4. Publish P2.24 when GPU 0 finishes. It first pulls, but only if every incoming
   file is a result, an audit file or Markdown (for example a FedProx publication),
   so it is safe while GPU 1 runs:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms)/results/|audits/|.+\.md$)' }); if ($bad.Count -ne 0) { throw "Incoming code changes; publish after both lanes finish: $bad" }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p224_server_ntd --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p224_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.24 two-sided retention screen'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```
