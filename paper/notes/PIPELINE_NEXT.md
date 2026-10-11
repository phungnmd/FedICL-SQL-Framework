# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

State 2026-10-11: P2.27, P2.28 and P2.29 are published; GPU 1 runs P2.36;
GPU 0 is free for P2.37. P2.37 (phase
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

Arm list and readings: LAB_LOG 2026-10-11 (phase E). Code: nested `ed6fa57`.
Dev sets only; never Spider test. Measured P2.27 stage times on this server:
plain A about 1.6 h alone (2.7 h with both GPUs busy), gold K about 2.7 h,
Hinton K about 3.6-4.5 h, about 20-30 min per evaluated set.

Run one arm at a time, in priority order, on whichever GPU frees first
(GPU 1 only after P2.36 step 3). Arms are independent; the order only decides
which answers arrive first.

| Priority | Arm | What it answers | Estimate |
|---:|---|---|---|
| 1 | `hinton_k2aaa` | K-first schedule (Q3), Hinton | about 20 h |
| 2 | `gold_k2aaa` | its gold pair: teacher vs gold under K-first (Q2) | about 17 h |
| 3 | `hinton_akaka_plain` | interleaved without NTD; vs `h_plain` isolates NTD in A2 | about 13 h |
| 4 | `gold_akaka_plain` | its gold pair | about 12 h |
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

3. Analyze and publish, after all six arms finish (needs P2.36 published):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p237_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.37 phase E baselines'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming code: $bad" }; git rebase origin/main; if ($LASTEXITCODE -ne 0) { throw 'Rebase failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p237_phase_e_s0/summary.md }
```

## Next

After P2.37: read the phase E table, then fix the paper story in a dated
LAB_LOG entry (claims, comparators, test, wording per outcome) before seeds
1-2 or Spider test.

On hold until the paper story is fixed: P2.31 (seeds 1 and 2), P2.35 (K-first
over seeds 0-2), Spider test evaluations, P2.32 (alpha 0.5).
