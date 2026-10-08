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

**Hinton K2 is reused, not retrained.** The P2.19 Hinton K2 stage was almost
finished when P2.19 was cancelled. Its command is identical to the P2.20 Hinton
K2 except for the stage label and output folder, and the training code did not
change between nested `785863a` and P2.20. P2.20 adopts that completed stage
and its runtime report. It never retrains it.

Measured P2.18 single-GPU times, evaluation excluded: K2 gold 4.5 h, one A
round about 1.3 h. GPU 0 (Hinton A1-A3, then FedProx) is about 7.8 h of
training; GPU 1 (gold K2AAA) about 8.4 h.

### 0. Let the P2.19 Hinton K2 finish, then stop P2.19

Do not pull yet. If the P2.19 GPU 1 lane (AKAKAKA/AK2AAA) is still running,
stop it now with Ctrl+C. On GPU 0, wait until the K2 training finishes and the
log moves on to its Spider evaluation or to A1, then stop it with Ctrl+C. Check
that the K2 stage is complete; the last line must say `passed`:

```powershell
& { $ErrorActionPreference='Stop'; Get-ChildItem audits/protocol_v2/p219_schedule_extension_s0 -Filter 'runtime_k2aaa_k2_train_*.json' | Sort-Object Name | ForEach-Object { $_.Name + ' ' + (Get-Content $_.FullName -Raw | ConvertFrom-Json).status } }
```

Do not delete any P2.19 files until P2.20 is published: P2.20 uses the K2
adapter, result row and runtime report. The rest of the P2.19 state is inert.

### 1. Pull and prepare once, both GPUs idle

CPU only. Reuses the P2.18 token audit and teacher-cache audit when all input
bytes match; teacher logits are not regenerated.

```powershell
$ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync python -m scripts.run_p220_placement_grid --phase prepare --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.20 preparation failed' }
```

### 2. Two short probes, before either lane

32-step longest-example probes, one process each. Each must pass reserved
<=21.5 GiB. The FedProx probe also covers the plain private stages; no Hinton
probe is needed because the Hinton K2 is adopted. Passed probes are reused on
restart. Check shared GPU memory manually.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($kind in @('fedprox','gold')) { uv run --no-sync python -m scripts.run_p220_placement_grid --phase probe --probe $kind --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.20 ${kind} probe failed" } }
```

### 3. Run these two terminals concurrently

GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($arm in @('hinton_k2aaa','fedprox_aaa')) { uv run --no-sync python -m scripts.run_p220_placement_grid --phase run --arm $arm --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.20 ${arm} failed" } }; Write-Host 'GPU 0 lane complete' }
```

GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run --no-sync python -m scripts.run_p220_placement_grid --phase run --arm gold_k2aaa --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.20 gold K2AAA failed' }; Write-Host 'GPU 1 lane complete' }
```

On interruption, rerun the identical lane command: completed stages and
evaluations are skipped, and unfinished training continues from its last
checkpoint. Do not pull, edit or switch on the server while either lane runs.
The recorded identity hashes all tracked code, so a pull would block the
resume. The only commit allowed during the run is step 3b.

### 3b. Optional: publish the finished Hinton K2AAA arm while lanes run

Run only after all four Hinton K2AAA stages and their evaluations are done
(GPU 0 has moved on to FedProx). It validates the arm with the runner's own
checks, then commits only its compact files: stage rows, receipts, evaluation
configs, metrics and predictions, runtime reports and the two passed probes.
It does not commit `run_manifest.json` or a summary, because the lanes still
write them. It is safe during the run: run identity excludes result files and
Git SHAs, nothing is pulled, and step 4 skips files already committed. It
adds no code, so it uses an inline Python check.

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $files=@(uv run --no-sync python -c "from pathlib import Path; from scripts import run_p220_placement_grid as r, list_p220_publication as p, list_p215_publication as q, plan_experiment as s, run_p27_rationale_screen as t; m=r.read_manifest(); a='hinton_k2aaa'; E=r.ENDPOINTS[a]; A={e: r.endpoint_adapter(a, e) for e in E}; assert all(set(m.get('evaluations', {}).get(a, {}).get(e, {})) == set(r.eval_sets(a, e)) for e in E), 'Hinton K2AAA evaluations incomplete'; [s.validate_recorded(v, r.eval_contract(a, e, n, A[e]), t.SETS[n][3]) for e in E for n, v in m['evaluations'][a][e].items()]; R=[v for j, x in m['runtime'].items() if j.startswith(a + '_') for v in x.values()]; [r.old.verify_runtime(v) for v in R]; assert all(any(j.startswith(a + '_' + e + '_train') for j in m['runtime']) for e in E), 'missing training runtime'; [r.verify_probe(k) for k in r.PROBES]; P=[Path(m['stages'][a][e]) / f for e in E for f in ('config.json', 'metrics.json')] + [r.receipt_path(a, e) for e in E] + [v[f] for e in E for v in m['evaluations'][a][e].values() for f in ('config', 'metrics', 'predictions')] + [v['path'] for v in R] + [r.AUDIT / ('memory_' + k + '.json') for k in r.PROBES]; print('\n'.join(q.unpublished(sorted({p.safe_file(x) for x in P}))))"); if ($LASTEXITCODE -ne 0) { throw 'Hinton K2AAA validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.20 Hinton K2AAA arm'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

### 4. Publish once, after both terminals finish successfully

Validates all stages, evaluations, probes, runtime reports, receipts and the
summary identity, then stages only the compact allowlisted files.

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p220_placement_grid --phase analyze --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p220_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.20 placement grid'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

Implementation: nested `af13bd2` and `484e9b0` (P2.19 K2 adoption), plus the
FedProx probe kind. Verification: 749 CPU tests pass; the adopted command was
checked equal to the P2.19 command at `785863a`. Tests also cover
CLI parsing of every stage, recipe equality with P2.18 except FedProx `mu`,
base-start provenance, resume without retraining, probe drift and publication
exclusions. Windows/CUDA probes and EX results remain to be measured.

## After P2.20

Apply the LAB_LOG schedule rule, then implement centralized Hinton S (same
data and order, no FedAvg). Not queued yet. Only after publication may the
P2.19 server folders be deleted.
