# P2.53 step 6d: teacher zero-shot on Spider test (complete)

Status 2026-10-29: published in nested `c3e3961`; teacher Spider test EX
77.22, results in LAB_LOG 2026-10-29. Kept as history.

Teacher Qwen2.5-Coder-7B zero-shot on Spider test (built, nested
`b265346`, `24f0a5b`; owner asked for it before the advisor report,
2026-10-29). `scripts/run_p253_teacher_test.py`: the P2.53 Spider test
contract with the teacher, 4-bit, batch 16; it first evaluates the 32
test rows with the longest prompts and stops above 21.5 GiB reserved.
About 1 GPU-h. It needs one GPU without a lane: stop (Ctrl+C) the lane
that is in a private round (A), not in a server stage (K, S), because
private rounds resume per client while a server stage loses at least its
current epoch (check with `scripts.status_p253 --seed 1`). The runner refuses a
GPU whose P2.37 lock is still held. Set `$gpu` to the freed GPU:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|scripts/run_p253_teacher_test\.py|tests/test_p253_teacher_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p253_teacher_test.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p253_teacher_test --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.53 teacher Spider test failed' }; uv run --no-sync python -m scripts.run_p253_teacher_test --phase status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

Resume the stopped lane on the same GPU (finished arms and stages are
skipped). GPU 0, seed 1:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $seed='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; foreach ($arm in @('hinton_k2','mixkd50_k2aaa','gold_k2','gmixgold_k2aaa','hinton_k2aaa','k2plus_aaa')) { uv run --no-sync python -m scripts.run_p253_confirmation --phase run --seed $seed --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.53 seed $seed $arm failed" }; Write-Host "GPU $gpu P2.53 seed $seed $arm complete" } }
```

GPU 1: the step 3 command. Publish the teacher row (P2.53 lanes may keep
running):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|scripts/run_p253_teacher_test\.py|tests/test_p253_teacher_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m scripts.run_p253_teacher_test --phase files); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record the teacher zero-shot Spider test (P2.53 step 6d)'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```
