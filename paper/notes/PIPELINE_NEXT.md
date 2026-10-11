# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

State 2026-10-11: P2.27 lanes and P2.28 are done and published; P2.27
`central` is running on GPU 0; P2.29 runs on GPU 1. Next: P2.27 step 4 after
`central`, P2.29 step 3, then P2.31. Direction A is final (framework paper,
no new method); screens S1 and S2 are dropped.
Paper direction and rules R1-R9: LAB_LOG 2026-10-11 and
[paper_direction_2026-10-11.md](../drafts/paper_direction_2026-10-11.md).

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

## P2.28: complete

Published in nested `238ee10` (G3 pass; LAB_LOG 2026-10-11). Commands:
[PIPELINE_P228_2026-10-11.md](../archive/completed_runbooks/PIPELINE_P228_2026-10-11.md).

## P2.29: plain last round from Hinton v1 K2 (rule R1), seed 0

Does v1 still need client NTD at 1.5B? `h_plain` = P2.27 Hinton v1 K2 plus one
private round without NTD (the P2.27 Hinton A3 command minus the NTD flags),
all five sets, compared with P2.27 Hinton v1 A3. Rule R1, LAB_LOG 2026-10-11.
Code: nested `88eb6ad`. Time: one A round (about 1.6 h) plus five evaluations
(about 1 h). Same memory path as the P2.27 FL rounds; no probe.

1. Pull while `central` runs on GPU 0. Allowed incoming files: the three P2.29
   files, results, audits, Markdown:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/run_p229_h_plain\.py|scripts/list_p229_publication\.py|tests/test_p229_h_plain\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run --no-sync pytest -q tests/test_p229_h_plain.py; if ($LASTEXITCODE -ne 0) { throw 'P2.29 tests failed' } }
```

2. Run on GPU 1. Rerun the identical command after an interruption:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run --no-sync python -m scripts.run_p229_h_plain --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.29 failed' }; Write-Host 'GPU 1 P2.29 complete' }
```

3. Analyze and publish (safe while `central` runs; stages only P2.29 files):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p229_h_plain --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p229_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.29 h_plain'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p229_h_plain_s0/summary.md }
```

## Next, code not yet written (no commands until runners exist)

Order and rules: [paper_direction_2026-10-11.md](../drafts/paper_direction_2026-10-11.md)
section 4, LAB_LOG 2026-10-11.

| ID | Run | GPU | Rule |
|---|---|---|---|
| P2.31 | Seeds 1 and 2: FL, FedNTD, gold, Hinton (NTD per R1), central | both GPUs, after P2.29 | R7, R8 |
| P2.32 | alpha 0.5 at Coder-1.5B: FL, gold, Hinton, central, seed 0 | after P2.31 | descriptive |
| P2.33 | `central_mix` at Coder-1.5B | when a GPU is free | reference |

Dropped 2026-10-11 (owner decision, direction A final): P2.30 (S1 ExST
screen, R4) and P2.34 (S2 execution-gated K1, R6). No runners exist for them.
