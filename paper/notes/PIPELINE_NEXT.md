# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.18 completed in `45a8bdc`;
its [old commands](../archive/completed_runbooks/PIPELINE_P218_0P5B_2026-10-07.md)
are historical. P2.19 was cancelled before any result; its
[queue](../archive/superseded_runbooks/PIPELINE_P219_SCHEDULE_EXTENSION_2026-10-07.md)
is history. Keep all P2.18 adapters, receipts, cache and results.

## P2.20: placement grid and FedProx baseline, seed 0

Goal: decide the schedule S with the rule fixed in LAB_LOG (2026-10-07). All
three arms start from the base model. With P2.18 they complete this grid, every
cell at 3 Spider passes and 2 BIRD epochs:

| Schedule | Gold | Hinton |
|---|---|---|
| AKAKA (interleaved) | P2.18 60.15 | P2.18 62.57 |
| AK2AA (one K block in the middle) | P2.18 61.80 | P2.18 63.15 |
| K2AAA (public warm-start, then FL) | **P2.20** | **P2.20** |

| New arm | Stages | Role |
|---|---|---|
| `hinton_k2aaa` | K2[fkl], A1, A2, A3 | placement, schedule rule |
| `gold_k2aaa` | K2[ce], A1, A2, A3 | public warm-start baseline (Nguyen et al., ICLR 2023) |
| `fedprox_aaa` | A1, A2, A3 with FedProx `mu=0.01` | second FL baseline (v1 value) |

K2 is **one continuous two-epoch optimizer/cosine horizon**. A is one
five-client, one-local-epoch, sample-weighted factor-wise FedAvg round.
Everything else is the P2.18 recipe: Qwen2.5-Coder-0.5B, frozen Coder-7B cache,
SQL-only, `target_fp32`, batch 1/accumulation 16, LR 2e-4, LoRA r16, Hinton
CE/KL .5/.5 at T=2, all 9,428 BIRD rows with evidence, k5 alpha 0.5 split.
Evaluation follows P2.18: Spider and BIRD after every stage, all five sets at
the final stage. Analysis reuses the published P2.18 predictions.

Measured P2.18 single-GPU times, evaluation excluded: K2 Hinton 5.2 h, K2 gold
4.5 h, one A round about 1.3 h. GPU 0 is about 9 h of training; GPU 1 is
about 12.5 h.

### 0. Delete the cancelled P2.19 state, both GPUs idle

P2.19 has nothing published and P2.20 writes to new paths, so this is cleanup,
not a requirement. First list what would be deleted:

```powershell
& { $ErrorActionPreference='Stop'; $targets=@(@('audits/protocol_v2/p219_schedule_extension_s0','artifacts/protocol_v2/p219_schedule_extension_s0') | Where-Object { Test-Path $_ }); $targets+=@(Get-ChildItem artifacts/eval_resume/protocol_v2 -Directory -Filter 'p219_*' -ErrorAction SilentlyContinue | ForEach-Object FullName); $targets+=@(Get-ChildItem experiments/federated/results,experiments/eval_arms/results -Directory -ErrorAction SilentlyContinue | Where-Object { (Test-Path (Join-Path $_.FullName 'config.json')) -and (Select-String -Path (Join-Path $_.FullName 'config.json') -Pattern 'p219_' -SimpleMatch -Quiet) } | ForEach-Object FullName); $targets }
```

Check that every listed path belongs to P2.19. Then delete them. This cannot
be undone. The command refuses any path that Git tracks:

```powershell
& { $ErrorActionPreference='Stop'; $targets=@(@('audits/protocol_v2/p219_schedule_extension_s0','artifacts/protocol_v2/p219_schedule_extension_s0') | Where-Object { Test-Path $_ }); $targets+=@(Get-ChildItem artifacts/eval_resume/protocol_v2 -Directory -Filter 'p219_*' -ErrorAction SilentlyContinue | ForEach-Object FullName); $targets+=@(Get-ChildItem experiments/federated/results,experiments/eval_arms/results -Directory -ErrorAction SilentlyContinue | Where-Object { (Test-Path (Join-Path $_.FullName 'config.json')) -and (Select-String -Path (Join-Path $_.FullName 'config.json') -Pattern 'p219_' -SimpleMatch -Quiet) } | ForEach-Object FullName); foreach ($t in $targets) { $tracked=@(git ls-files -- $t); if ($LASTEXITCODE -ne 0 -or $tracked.Count -ne 0) { throw "Tracked path, not deleting: $t" } }; foreach ($t in $targets) { Remove-Item -Recurse -Force -LiteralPath $t }; Write-Host "Deleted $($targets.Count) P2.19 paths" }
```

### 1. Pull and prepare once, both GPUs idle

CPU only. Reuses the P2.18 token audit and teacher-cache audit when all input
bytes match; teacher logits are not regenerated.

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p220_placement_grid --phase prepare --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.20 preparation failed' }
```

### 2. Three short probes, before either lane

32-step longest-example probes, one process each. Each must pass reserved
<=21.5 GiB. The FedProx probe also covers the plain private stages. Passed
probes are reused on restart. Check shared GPU memory manually.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($kind in @('fedprox','gold','hinton')) { uv run --no-sync python -m scripts.run_p220_placement_grid --phase probe --probe $kind --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.20 ${kind} probe failed" } }
```

### 3. Run these two terminals concurrently

GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; uv run --no-sync python -m scripts.run_p220_placement_grid --phase run --arm hinton_k2aaa --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.20 Hinton K2AAA failed' }; Write-Host 'GPU 0 lane complete' }
```

GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; foreach ($arm in @('gold_k2aaa','fedprox_aaa')) { uv run --no-sync python -m scripts.run_p220_placement_grid --phase run --arm $arm --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.20 ${arm} failed" } }; Write-Host 'GPU 1 lane complete' }
```

On interruption, rerun the identical lane command: completed stages and
evaluations are skipped, and unfinished training continues from its last
checkpoint. Do not pull, edit, switch, commit or push on the server while
either lane runs. The recorded identity hashes all tracked code, so a pull
would block the resume.

### 4. Publish once, after both terminals finish successfully

Validates all stages, evaluations, probes, runtime reports, receipts and the
summary identity, then stages only the compact allowlisted files.

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p220_placement_grid --phase analyze --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p220_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.20 placement grid'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

Implementation: nested `af13bd2` (runner, publication, tests) and the FedProx
probe kind in the commit before it. Verification: 747 CPU tests pass, including
CLI parsing of every stage, recipe equality with P2.18 except FedProx `mu`,
base-start provenance, resume without retraining, probe drift and publication
exclusions. Windows/CUDA probes and EX results remain to be measured.

## After P2.20

Apply the LAB_LOG schedule rule, then implement centralized Hinton S (same
data and order, no FedAvg). Not queued yet.
