# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

## P2.27: Coder-1.5B on the alpha 0.1 split, seed 0

New student and a harder split (owner decision 2026-10-10): fresh
Qwen2.5-Coder-1.5B-Instruct, P2.18 recipe, 5 clients from the k5 alpha 0.1
domain-cluster split (nested `02dabf4`). Each client spans 6-8 of 20 domain
clusters (alpha 0.5: 9-13). Rule: LAB_LOG 2026-10-10 (P2.27). Code: nested
`80bae67`. No memory probes (owner decision: same size as 1.5B-Instruct).

| Arm | Stages | Role |
|---|---|---|
| `base` | none | untrained Coder-1.5B, all five sets |
| `fl` | A, A, A | FL baseline; its A1 is the shared start of every federated arm |
| `fedntd` | A, A[ntd], A[ntd] | published non-IID FL baseline; method without server KD |
| `gold_v1` | A, K[ce], A[ntd], K[ce], A[ntd] | matched public gold |
| `hinton_v1` | A, K[fkl], A[ntd], K[fkl], A[ntd] | method v1 |
| `central` | Spider E1-E3 | centralized Spider reference (heterogeneity penalty) |

Spider and BIRD after every stage; all five sets at the final stage. Time,
from the 1.5B-Instruct measurements (A round about 1.6 h, gold K 2.7 h,
Hinton K 3.3 h; NTD rounds and 1.5B evaluation not measured yet): about 25 h
per lane, then about 10 h for `central`.

1. Pull and prepare, both GPUs idle (CPU only: length audit of the three
   training pools and the cross-student teacher-cache audit, which the Hinton
   trainer requires for a new student; teacher logits are not regenerated):

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.27 preparation failed' }
```

2. Two terminals concurrently. GPU 1 runs `base` first; `gold_v1` and
   `fedntd` then wait for the local FL A1 from GPU 0 (no Git step needed).

GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($arm in @('fl','hinton_v1')) { uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.27 $arm failed" } }; Write-Host 'GPU 0 lane complete' }
```

GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; foreach ($arm in @('base','gold_v1','fedntd')) { uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.27 $arm failed" } }; Write-Host 'GPU 1 lane complete' }
```

3. `central` on the first GPU that finishes. Set `$gpu` to that card:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase run --arm central; if ($LASTEXITCODE -ne 0) { throw 'P2.27 central failed' }; Write-Host "GPU $gpu central complete" }
```

On interruption, rerun the identical command: completed stages and
evaluations are skipped, unfinished training resumes from its last
checkpoint. Do not pull, edit or switch on the server while a lane runs.

4. Publish once, after all three commands finish:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p227_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.27 Coder-1.5B alpha 0.1'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```
