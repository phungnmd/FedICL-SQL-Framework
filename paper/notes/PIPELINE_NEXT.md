# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.18 completed in `45a8bdc`;
its [old commands](../archive/completed_runbooks/PIPELINE_P218_0P5B_2026-10-07.md)
are historical. Keep all existing adapters, receipts, cache and results.

## P2.19: Hinton placement and finite depth checks, seed 0

Owner selected Hinton only, the current Coder-0.5B setup and EX checks.
No new gold arms, centralized training, seed sweep or open-ended depth search.

| New arm | Start | Newly trained stages | Total Spider passes / BIRD epochs |
|---|---|---|---:|
| K2AAA (KKAAA) | fresh base | K2, A1, A2, A3 | 3 / 2 |
| AKAKAKA | published P2.18 Hinton AKAKA | K3 (one epoch), A4 | 4 / 3 |
| AK2AAA | published P2.18 Hinton AK2AA | A4 | 4 / 2 |

K2 is **one continuous two-epoch optimizer/cosine horizon**, not two restarted
Ks. A is one five-client, one-local-epoch, sample-weighted factor-wise FedAvg
round. All new stages preserve P2.18: Qwen2.5-Coder-0.5B, frozen Coder-7B cache,
SQL-only, `target_fp32`, batch 1/accumulation 16, LR 2e-4, LoRA r16/alpha32/dropout
.05, warmup .03, non-reentrant checkpointing, max_len 7168/error, Hinton CE/KL
.5/.5 at T=2, all 9,428 BIRD rows with evidence. Eval: Spider only, batch 16,
greedy k=0, original execution timeout. EX is primary; the evaluator also
records EM without extra generation. Seven new endpoint evaluations in total.

Analysis reuses committed P2.18 predictions. Compare K2AAA with AKAKA and AK2AA
at 3/2 exposure, then each extended endpoint against its own 3-private-pass
parent. AKAKAKA vs AK2AAA has unequal public exposure (3 vs 2), and separate K
stages reset optimizer/scheduler. A higher best observed EX is not proof of a
maximum; a flat/lower next point at seed 0 is not proof of convergence. Testing
on these sets guides exploration, not an unbiased final model-selection claim.

### 1. Pull and prepare once, both GPUs idle

No P2.18 identity migration or preparation rerun. The new runner pins the
published source manifest, checks the two parent receipts/adapters and reuses
the token audit only when all input bytes match. Cache audit is reused; teacher
logits are not regenerated. New outputs use `p219_schedule_extension_s0`.

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p219_schedule_extension --phase prepare --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.19 preparation failed' }
```

### 2. Two short probes, before either lane

A fresh-base public stage is a new orchestration path. Run the existing private
and Hinton 32-step longest-example probes with P2.19 identities, in separate
processes. Both must pass reserved <=21.5 GiB before launching. Passed P2.19
probes are reused on restart; no gold probe needed. Shared memory stays manual;
there is no Windows counter polling. Do not claim GPU validation from CPU tests.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($kind in @('private','hinton')) { uv run --no-sync python -m scripts.run_p219_schedule_extension --phase probe --probe $kind --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.19 ${kind} probe failed" } }
```

### 3. Run these two terminals concurrently

GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; uv run --no-sync python -m scripts.run_p219_schedule_extension --phase run --arm k2aaa --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.19 K2AAA failed' }; Write-Host 'GPU 0 lane complete' }
```

GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; foreach ($arm in @('akakaka','ak2aaa')) { uv run --no-sync python -m scripts.run_p219_schedule_extension --phase run --arm $arm --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.19 ${arm} failed" } }; Write-Host 'GPU 1 lane complete' }
```

Each command verifies completed stage identity and Spider predictions before
advancing. On interruption, rerun the identical lane command and output roots;
completed stages/evals skip, unfinished training uses its saved checkpoint.
There is no cross-lane publication wait. Do not pull, edit, switch, commit or
push on the server while either lane is running.

### 4. Publish once, after both terminals finish successfully

The helper validates all seven stages/evals, successful probes, runtime reports,
receipts and summary identity. It emits only unpublished compact allowlisted
files. Adapter weights, optimizer state and caches never enter Git. A failed
push can be retried with this same command once the index is empty.

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p219_schedule_extension --phase analyze --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p219_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.19 Hinton placement and depth'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

Implementation: nested `099dd48`, `785863a`. Verification: 745 CPU tests cover fresh K2 provenance, continuation
recipes, omitted SQL defaults, source receipt validation, preparation drift,
resume without retraining, failed runtime receipts and publication exclusions.
All five blocks parse in PowerShell 7.4.6; mocked two-lane success/failure and
single publication pass. Windows/CUDA smoke and final EX remain to be measured
on the server.
