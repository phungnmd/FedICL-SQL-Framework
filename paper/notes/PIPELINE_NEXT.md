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
`80bae67`, `3582656`, `c93dce3`. No memory probes (owner decision: same size as 1.5B-Instruct).

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
Hinton K 3.3 h, about 10 min per evaluated set) and the 0.5B NTD overhead
(about +30%, so A[ntd] about 2.1 h; not measured at 1.5B): GPU 0 about 19 h,
GPU 1 about 18 h, then `central` about 6.5 h; about 25 h wall clock.

1. Pull and prepare, both GPUs idle (CPU only: Spider length audit and the
   cross-student teacher-cache audit, which the Hinton trainer requires for a
   new student and which also checks every BIRD row fits; teacher logits are
   not regenerated):

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

3b. Any time while lanes run, repeatable: publish every finished stage and
   evaluation so far (stage rows, receipts, evaluation config/metrics/
   predictions, runtime reports, cache audit; never the run manifest or
   summary). The pull is refused unless every incoming file is the
   publication helper, its test, a result, an audit file or Markdown, so it
   never changes code a running lane uses:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/list_p227_publication\.py|tests/test_p227_coder15b_alpha01\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; $files=@(uv run --no-sync python -m scripts.list_p227_publication --partial); if ($LASTEXITCODE -ne 0) { throw 'Finished-stage validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record finished P2.27 stages'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } } else { Write-Host 'Nothing new to publish' } }
```

4. Publish once, after all three commands finish:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p227_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.27 Coder-1.5B alpha 0.1'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

## P2.28: pass@k headroom on client training questions, seed 0

Diagnostic, no training: gate G3 for client execution-verified self-training
(STaR; rejection-sampling fine-tuning). From the P2.27 adapters a client
receives before the last private round (FL A2, gold v1 K2, Hinton v1 K2),
1,000 fixed Spider training questions (200 per alpha 0.1 client): one greedy
SQL (P2.27 evaluation decode) and 8 samples at T 0.7, all scored with
`spider_result_eq_v1`. pass@k: Chen et al. (2021) unbiased estimator. G3,
fixed before the run: pass@8 minus greedy EX >= 5 points and >= 20% of
questions with a correct sample that differs from gold. Code:
`scripts/run_p228_passk_headroom.py` (new file, imports P2.27 only to resolve
adapters). Output: `audits/protocol_v2/p228_passk_headroom_s0/`. Time, not
measured: about 1.5 h per parent (greedy as one evaluation, then 500 calls of
16 sampled sequences).

Queue: P2.27 `central` keeps the first free GPU. P2.28 runs on the second
free GPU, after the Hinton lane has recorded K2 (all three parents exist then).

1. Pull while P2.27 lanes run. Allowed incoming files: the two P2.28 files,
   results, audits, Markdown:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/run_p228_passk_headroom\.py|tests/test_p228_passk_headroom\.py|scripts/list_p227_publication\.py|tests/test_p227_coder15b_alpha01\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync pytest -q tests/test_p228_passk_headroom.py; if ($LASTEXITCODE -ne 0) { throw 'P2.28 tests failed' } }
```

2. Smoke on the free GPU (set `$gpu`): the 16 longest-schema questions from
   FL A2 into `smoke/`; report the last `peak_reserved` line (budget 21.5 GiB)
   and the time:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p228_passk_headroom --parents fl:a2 --smoke 16; if ($LASTEXITCODE -ne 0) { throw 'P2.28 smoke failed' }; Write-Host "GPU $gpu P2.28 smoke complete" }
```

3. Full run, same GPU. Rerun the identical command after an interruption;
   finished questions are skipped and samples are seeded per question:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p228_passk_headroom --parents fl:a2 gold_v1:k2 hinton_v1:k2; if ($LASTEXITCODE -ne 0) { throw 'P2.28 failed' }; Write-Host "GPU $gpu P2.28 complete" }
```

4. Publish (summary plus per-question decodes, about 1.5 MB per parent):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/list_p227_publication\.py|tests/test_p227_coder15b_alpha01\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; $dir='audits/protocol_v2/p228_passk_headroom_s0'; $files=@("$dir/summary.json","$dir/fl_a2.jsonl","$dir/gold_v1_k2.jsonl","$dir/hinton_v1_k2.jsonl"); foreach ($file in $files) { if (-not (Test-Path $file)) { throw "Missing $file" }; git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if (@(Compare-Object ($files | Sort-Object) ($actual | Sort-Object)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.28 pass@k headroom'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

Decision: G3 pass on any parent: client self-training quick test (A>A>A[M1]
vs A>A>A from FL A2). G3 fail on all three: close M1 at this size.
