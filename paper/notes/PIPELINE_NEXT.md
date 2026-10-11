# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

State 2026-10-11: P2.27 lanes, P2.28 and P2.29 are published; P2.27
`central` finished (publish with step 4); GPU 1 runs P2.36. P2.37 (phase
E, exploration at seed 0) follows on each GPU as it frees; findings and open
questions are in
[RESEARCH_STATE.md](RESEARCH_STATE.md).

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

4. Publish once, after all three commands finish. It rebases onto incoming
   P2.36, P2.37 or data files before pushing (none of them is imported by a
   running lane):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p227_coder15b_alpha01 --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p227_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.27 Coder-1.5B alpha 0.1'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' } }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(run_p236_g_plain|list_p236_publication|build_processed_spider_test|run_p237_phase_e|list_p237_publication|audit_test_suite_ex|audit_power_clustered)\.py|tests/test_(p236_g_plain|p237_phase_e|audit_test_suite_ex|audit_power_clustered)\.py|processed_data/SPIDER_TEST/.+|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

## P2.28: complete

Published in nested `238ee10` (G3 pass; LAB_LOG 2026-10-11). Commands:
[PIPELINE_P228_2026-10-11.md](../archive/completed_runbooks/PIPELINE_P228_2026-10-11.md).

## P2.29: complete

Published in nested `b4a52db` (R1: keep NTD; LAB_LOG 2026-10-11). Commands:
[PIPELINE_P229_2026-10-11.md](../archive/completed_runbooks/PIPELINE_P229_2026-10-11.md).

## P2.36: gold chain with a plain last round (`g_plain`), seed 0

Matched gold control of `h_plain` (P2.29): P2.27 gold v1 K2 plus one private
round without NTD (the P2.27 gold v1 A3 command minus the NTD flags), five dev
sets. Seed 0 dev contrasts are descriptive (phase E). Code: nested
`9001629`. Time: one A round (about 1.6 h) plus five evaluations (about 1 h).
Same memory path as P2.29.

1. Pull while `central` runs on GPU 0. Allowed incoming files: the P2.36
   files, the Spider test builder and CSV, results, audits, Markdown:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(run_p236_g_plain|list_p236_publication|build_processed_spider_test|run_p237_phase_e|list_p237_publication|audit_test_suite_ex|audit_power_clustered)\.py|tests/test_(p236_g_plain|p237_phase_e|audit_test_suite_ex|audit_power_clustered)\.py|processed_data/SPIDER_TEST/.+|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; uv run --no-sync pytest -q tests/test_p236_g_plain.py tests/test_p229_h_plain.py; if ($LASTEXITCODE -ne 0) { throw 'P2.36 tests failed' } }
```

2. Run on GPU 1. Rerun the identical command after an interruption:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run --no-sync python -m scripts.run_p236_g_plain --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.36 failed' }; Write-Host 'GPU 1 P2.36 complete' }
```

3. Analyze and publish (safe while another lane runs; rebases onto allowed
   incoming files, including the new P2.37 files, before pushing):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p236_g_plain --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p236_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.36 g_plain'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(run_p236_g_plain|list_p236_publication|build_processed_spider_test|run_p237_phase_e|list_p237_publication|audit_test_suite_ex|audit_power_clustered)\.py|tests/test_(p236_g_plain|p237_phase_e|audit_test_suite_ex|audit_power_clustered)\.py|processed_data/SPIDER_TEST/.+|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p236_g_plain_s0/summary.md }
```

## P2.37: phase E baselines, Coder-1.5B, seed 0

Arm list and readings: LAB_LOG 2026-10-11 (phase E). Code: nested `9a38777`.
Dev sets only; never Spider test. Measured P2.27 stage times on this server:
plain A about 1.6 h alone (2.7 h with both GPUs busy), gold K about 2.7 h,
Hinton K about 3.6-4.5 h, about 20-30 min per evaluated set.

| Lane | Arms, in order | Estimate |
|---|---|---|
| GPU 0, after P2.27 step 4 | `hinton_k2aaa`, `gold_akaka_plain`, `local` (5 clients) | about 35 h |
| GPU 1, after P2.36 step 3 | `gold_k2aaa`, `hinton_akaka_plain`, `central_mix` | about 39 h |

Memory: Hinton and gold K, plain A and Spider-only client training are the
P2.27 paths. `central_mix` is the first Coder-1.5B client training on BIRD
rows (7,424 tokens): check the process's shared GPU memory in its first 15
minutes; its peak reserved VRAM is in the result metrics.

1. Prepare (CPU, safe while P2.36 runs; pulls only new files that no running
   lane imports, then runs the P2.37 tests):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(run_p237_phase_e|list_p237_publication|audit_test_suite_ex|audit_power_clustered)\.py|tests/test_(p237_phase_e|audit_test_suite_ex|audit_power_clustered)\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; uv run --no-sync pytest -q tests/test_p237_phase_e.py; if ($LASTEXITCODE -ne 0) { throw 'P2.37 tests failed' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.37 preparation failed' } }
```

2. Lanes. Start each when its GPU is free; rerun the identical command after an
   interruption (finished stages and evaluations are skipped, training resumes
   from its last checkpoint).

GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($arm in @('hinton_k2aaa','gold_akaka_plain','local')) { uv run --no-sync python -m scripts.run_p237_phase_e --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.37 $arm failed" } }; Write-Host 'GPU 0 P2.37 lane complete' }
```

GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; foreach ($arm in @('gold_k2aaa','hinton_akaka_plain','central_mix')) { uv run --no-sync python -m scripts.run_p237_phase_e --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.37 $arm failed" } }; Write-Host 'GPU 1 P2.37 lane complete' }
```

3. Analyze and publish, after both lanes finish (needs P2.36 published):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p237_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.37 phase E baselines'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming code: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p237_phase_e_s0/summary.md }
```

## Next

After P2.37: read the phase E table, then fix the paper story in a dated
LAB_LOG entry (claims, comparators, test, wording per outcome) before seeds
1-2 or Spider test.

On hold until the paper story is fixed: P2.31 (seeds 1 and 2), P2.35 (K-first
over seeds 0-2), Spider test evaluations, P2.32 (alpha 0.5).
