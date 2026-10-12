# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

State 2026-10-12: P2.27, P2.28, P2.29 and P2.36 are published; both GPUs
run P2.37 arms. P2.37 (phase
E, exploration at seed 0) runs one arm at a time in priority order; findings and open
questions are in
[RESEARCH_STATE.md](RESEARCH_STATE.md).

## P2.27: complete

Published in nested `5767704` (R3 and R9 in LAB_LOG 2026-10-11). Commands:
[PIPELINE_P227_2026-10-11.md](../archive/completed_runbooks/PIPELINE_P227_2026-10-11.md).

## P2.28: complete

Published in nested `238ee10` (G3 pass; LAB_LOG 2026-10-11). Commands:
[PIPELINE_P228_2026-10-11.md](../archive/completed_runbooks/PIPELINE_P228_2026-10-11.md).

## P2.29: complete

Published in nested `b4a52db` (R1: keep NTD; LAB_LOG 2026-10-11). Commands:
[PIPELINE_P229_2026-10-11.md](../archive/completed_runbooks/PIPELINE_P229_2026-10-11.md).

## P2.36: complete

Published in nested `31a568e` (LAB_LOG 2026-10-12). Commands, including the
P2.29 LF restore:
[PIPELINE_P236_2026-10-12.md](../archive/completed_runbooks/PIPELINE_P236_2026-10-12.md).

## P2.37: phase E baselines, Coder-1.5B, seed 0

Arm list and readings: LAB_LOG 2026-10-11 (phase E). Code: nested `ed6fa57`.
Dev sets only; never Spider test. Measured P2.27 stage times on this server:
plain A about 1.6 h alone (2.7 h with both GPUs busy), gold K about 2.7 h,
Hinton K about 3.6-4.5 h, about 20-30 min per evaluated set.

Run one arm at a time, in priority order, on whichever GPU frees first. Arms are independent; the order only decides
which answers arrive first.

| Priority | Arm | What it answers | Estimate |
|---:|---|---|---|
| 1 | `hinton_k2aaa` | K-first schedule (Q3), Hinton | about 20 h |
| 2 | `gold_k2aaa` | its gold pair: teacher vs gold under K-first (Q2) | about 17 h |
| 3 | `hinton_akaka_plain` | `h_plain` with NTD removed (A>K>A>K>A); if it matches `h_plain`, NTD leaves the method | about 13 h |
| 4 | `gold_akaka_plain` | its gold pair (`g_plain` without NTD) | about 12 h |
| 5 | `central_mix` | ceiling with all data in one place (Q4); frames the claims, does not choose them | about 10 h |
| 6 | `local` (5 clients) | federation vs local-only (Q1); outcome predictable, reviewers expect it | about 8 h |

All six stay in the fixed arm list and are required before step 3.

Memory: Hinton and gold K, plain A and Spider-only client training are the
P2.27 paths. `central_mix` is the first Coder-1.5B client training on BIRD
rows (7,424 tokens): check the process's shared GPU memory in its first 15
minutes; its peak reserved VRAM is in the result metrics.

1. Prepare (CPU, safe while P2.36 runs; pulls only new files that no running
   lane imports, then runs the P2.37 tests):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(run_p237_phase_e|list_p237_publication|audit_test_suite_ex|audit_power_clustered)\.py|tests/test_(p237_phase_e|audit_test_suite_ex|audit_power_clustered)\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; uv run --no-sync pytest -q tests/test_p237_phase_e.py; if ($LASTEXITCODE -ne 0) { throw 'P2.37 tests failed' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.37 preparation failed' } }
```

2. Run one arm. Set `$gpu` to the free GPU and `$arm` to the next arm in the
   priority table; rerun the identical command after an interruption
   (finished stages and evaluations are skipped, training resumes from its
   last checkpoint). Example, GPU 0 now:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $arm='hinton_k2aaa'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p237_phase_e --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.37 $arm failed" }; Write-Host "GPU $gpu P2.37 $arm complete" }
```

2b. Publish one finished lane (safe while other lanes run). Set `$lane` to
   the finished arm (`local` for the five local clients). It commits only
   stage rows, receipts and evaluation files of that lane; the run manifest,
   runtime reports and summary wait for step 3, which skips files already
   committed. If the push is rejected, stop and report; never rebase.

```powershell
& { $ErrorActionPreference='Stop'; $lane='hinton_k2aaa'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/list_p237_arm_publication\.py|tests/test_list_p237_arm_publication\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_list_p237_arm_publication.py; if ($LASTEXITCODE -ne 0) { throw 'Lister tests failed' }; $files=@(uv run --no-sync python -m scripts.list_p237_arm_publication $lane); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m "results: record P2.37 $lane"; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Write-Host "Published P2.37 $lane ($($files.Count) files)" }
```

3. Analyze and publish, after all six arms finish (needs P2.36 published):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming code: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p237_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.37 phase E baselines'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p237_phase_e_s0/summary.md }
```

## Next

After P2.37: read the phase E table, then fix the paper story in a dated
LAB_LOG entry (claims, comparators, test, wording per outcome) before seeds
1-2 or Spider test.

On hold until the paper story is fixed: P2.31 (seeds 1 and 2), P2.35 (K-first
over seeds 0-2), Spider test evaluations, P2.32 (alpha 0.5).
