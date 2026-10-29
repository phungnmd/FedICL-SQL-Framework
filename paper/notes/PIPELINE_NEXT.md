# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

State 2026-10-25: P2.27-P2.29, P2.36, P2.37 (`hinton_k2aaa`, `gold_k2aaa`,
`central_mix`, `local`), P2.38, the P2.39 pilot, P2.40, P2.42, P2.43 (both
chains to A3, `fl_bird`), P2.44, P2.47 (`80d1091`) and P2.48 (`8b79530`) are published. The
CPU audits (top-k mass, token roles) are published (`4b1b4f0`). P2.43
`central_bird` is paused (Ctrl+C; it resumes from its last 200-step
checkpoint with the identical command). P2.48 is published (`8b79530`,
[runbook](../archive/completed_runbooks/PIPELINE_P248_2026-10-25.md)).
P2.49 (`db2cc09`) and P2.50 (`015429c`) are published
([runbook](../archive/completed_runbooks/PIPELINE_P249_P250_2026-10-26.md));
`gmixkd50_k2aaa` and `fslm_k2sasasa` were dropped (owner, 2026-10-26).
P2.51 finished (publish after P2.52). The freeze is approved (LAB_LOG
2026-10-26 FREEZE); the active work is the P2.53 confirmation below. P2.46
and P2.41 stay deferred.

State 2026-10-28: paper direction fixed by the owner
([DIRECTION_PROPOSAL](DIRECTION_PROPOSAL.md)); FREEZE addendum 2 adds FedAvg
and `gold_k2aaa` at seeds 1-2 (claims C6, C7). P2.53 steps 1b and 1c done
(1c published, nested `0704737`). E2 (0.5B student) is queued after step 7
(LAB_LOG 2026-10-29); E1 waits for a revision.
P2.54 seed 0 is published (nested `76496b4`), the robustness setting;
no seeds 1-2.

State 2026-10-29: P2.53 seed 1 is published (nested `ce51178`). Next:
P2.55 and P2.56 (the advisor table), then P2.53 seeds 2 and 0.

## Status check (read-only, any time, for example after a server restart)

Prints, for P2.37 `central_mix`/`local` and P2.38-P2.43: which stages are
trained, which evaluations are missing, whether they are published, any
stage interrupted mid-training, and whether a GPU lane is running. It runs the
status script from origin, so it works before the server pulls new code, and
changes nothing:

```powershell
& { $ErrorActionPreference='Stop'; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git show origin/main:scripts/status_k2aaa_lanes.py | uv run --no-sync python -; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

After a restart no lane runs, so the P2.40 step 1 pull is allowed. Since the
P2.38 launch the shared code changed only by the TAID option (off unless
`--kd-taid-t-start` is set) and the frozen-A aggregation fix, so a lane
resumed after that pull trains exactly as before. Rerun an unfinished lane
with its identical run command; it skips finished stages and resumes an
interrupted one from its checkpoint.

## P2.55 and P2.56: FedProx and LLM few-shot rows of the advisor table (seed 0)

Owner, 2026-10-29 (LAB_LOG): the FedProx-SLM and LLM few-shot rows of the
advisor's table 4.2. P2.55 is the P2.27 FedAvg run (Spider only, 5
clients, 3 rounds) with FedProx mu 0.01, about 6 h with its six
evaluations. P2.56 is the teacher zero-shot Spider test run with five
fixed Spider training demonstrations, on Spider test and the four Spider
dev sets, about 1.5-2 h. P2.53 seed 1 is published (nested `ce51178`).

1. Pull and prepare, with both GPUs idle: the pull brings the few-shot
   option of the shared evaluator (nested `0358c41`; zero-shot
   evaluations keep their prompts and identities). Run it before any
   other pull command in this file (step 1b publication, steps 2-6),
   whose allowlists do not admit these files:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -c "from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; exclusive_lock(r.AUDIT / 'gpu_0.lock').__enter__(); exclusive_lock(r.AUDIT / 'gpu_1.lock').__enter__()"; if ($LASTEXITCODE -ne 0) { throw 'A GPU lane is running' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(fedicl_sql/prompts/builder\.py|experiments/eval_arms/run\.py|scripts/run_p25[56]_[a-z_]+\.py|tests/test_(p25[56]_[a-z_]+|prompts|eval_arms_config)\.py|docs/.+|AGENTS\.md|.+\.md|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_prompts.py tests/test_eval_arms_config.py tests/test_struct_sql_qp_cot.py tests/test_p253_teacher_test.py tests/test_p255_fedprox.py tests/test_p256_teacher_fewshot.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p255_fedprox --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.55 preparation failed' }; Write-Host 'P2.55 and P2.56 ready' }
```

2. P2.55 FedProx on GPU 0 (rerun the same command to resume; finished
   rounds and evaluations are skipped). Prints FedProx against FedAvg on
   every set, with EM:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p255_fedprox --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.55 FedProx failed' }; uv run --no-sync python -m scripts.run_p255_fedprox --phase status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

3. P2.56 teacher 5-shot on GPU 1, in parallel. It writes the five
   demonstrations, runs the VRAM smoke (stops above 21.5 GiB), then
   Spider test first. Prints EX, EM and time per question per set and the
   Spider test pair with the zero-shot teacher:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p256_teacher_fewshot --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.56 teacher few-shot failed' }; uv run --no-sync python -m scripts.run_p256_teacher_fewshot --phase status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

4. Publish each once its lane has finished (set `$exp` to `p255_fedprox`
   or `p256_teacher_fewshot`; the `files` phase takes the lane lock, so it
   refuses a running lane):

```powershell
& { $ErrorActionPreference='Stop'; $exp='p256_teacher_fewshot'; $msg="results: record the $exp seed 0 rows of the advisor table"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m "scripts.run_$exp" --phase files); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

## P2.54: SynSQL-2.5M as the public pool (seed 0 published)

Seed 0 is published (nested `76496b4`; LAB_LOG 2026-10-28); the finished
steps are in the [runbook](../archive/completed_runbooks/PIPELINE_P254_2026-10-28.md).
P2.54 is the paper's robustness setting at seed 0; no further P2.54
training (owner, 2026-10-28). The `gmixgold_k2aaa` A3 Spider test is
published (nested `5a638c0`, LAB_LOG 2026-10-29; commands in the runbook).

1. Status (read-only, any time): dev EX per stage, the paired contrasts
   with exact McNemar, and the same cells with the BIRD pool.

```powershell
& { $ErrorActionPreference='Stop'; uv run --no-sync python -m scripts.status_p254 --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

## P2.53: confirmation, seeds 0-2 (both GPUs)

The frozen method and its four comparators (LAB_LOG 2026-10-26 FREEZE),
seeds 1 and 2 trained new, seed 0 reusing the published adapters. Every
final adapter is evaluated on Spider test (2,147) and the five dev sets.
Measured 1.5B times: Hinton K2 5.2 h, gold K2 4.5 h, one Hinton K 2.6 h,
plain round 1.2-1.4 h, replay round 2.1-3.3 h; about 28 h per lane below.

Status of one seed, read-only and safe while lanes run (set `$seed`): the
stages each arm has trained, the EX of every recorded final adapter on Spider
test and the five dev sets (each cell fills as soon as its set is evaluated),
and the method pairs on Spider test, Spider dev and BIRD dev. It runs the
script from origin, so no pull is needed:

```powershell
& { $ErrorActionPreference='Stop'; $seed='1'; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git show origin/main:scripts/status_p253.py | uv run --no-sync python - --seed $seed; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

1. Pull, test, prepare P2.53 (all three seeds) and P2.54 (fetch the
   SynSQL databases, seed 0). Both GPUs must be idle, since the pull brings a
   new dataset profile in shared code:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -c "from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; exclusive_lock(r.AUDIT / 'gpu_0.lock').__enter__(); exclusive_lock(r.AUDIT / 'gpu_1.lock').__enter__()"; if ($LASTEXITCODE -ne 0) { throw 'A GPU lane is running' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(fedicl_sql/data/protocol\.py|scripts/(run|list)_p25[34]_[a-z_]+\.py|scripts/build_processed_synsql\.py|tests/test_p25[34]_[a-z_]+\.py|processed_data/protocol_v2/SYNSQL/.+|docs/.+|AGENTS\.md|.+\.md|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p254_synsql_public.py tests/test_p253_confirmation.py tests/test_data_protocol.py tests/test_p250_server_replay_rows.py tests/test_p249_gold_k2_replay.py tests/test_p248_replay_compact_fsl.py tests/test_p237_phase_e.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; foreach ($seed in 0,1,2) { uv run --no-sync python -m scripts.run_p253_confirmation --phase prepare --seed $seed; if ($LASTEXITCODE -ne 0) { throw "P2.53 seed $seed preparation failed" } }; uv run --no-sync python scripts/build_processed_synsql.py --phase fetch-dbs; if ($LASTEXITCODE -ne 0) { throw 'SynSQL databases failed' }; uv run --no-sync python -m scripts.run_p254_synsql_public --phase prepare --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.54 preparation failed' }; Write-Host 'P2.53 and P2.54 prepared' }
```

1b. Seed 0 Spider test of the method and its three trained comparators
   first (owner, 2026-10-28; eval only, the seed-0 adapters are
   published; about 35 min) on an idle GPU (set `$gpu`; the GPU lock
   refuses a busy card). Prints the seed-0 Spider test EX and the pairs; the claims
   use the pooled three-seed test (step 7). The pull admits only files
   the GPU 0 lane never imports:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $seed='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_status_p253.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; foreach ($arm in @('mixkd50_k2aaa','gmixgold_k2aaa','hinton_k2aaa','k2plus_aaa')) { uv run --no-sync python -m scripts.run_p253_confirmation --phase run --seed $seed --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.53 seed $seed $arm Spider test failed" }; Write-Host "GPU $gpu P2.53 seed $seed $arm Spider test done" }; uv run --no-sync python -m scripts.status_p253 --seed $seed; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

   Publish the 1b evaluations (owner, 2026-10-29: EM and EX for the advisor
   table) with the finished-arms form of step 6: the four arms' Spider test
   evaluation and runtime files, never the seed-0 run manifest, which step 5
   still writes. The lane locks refuse a running arm:

```powershell
& { $ErrorActionPreference='Stop'; $seed='0'; $arms=@('mixkd50_k2aaa','gmixgold_k2aaa','hinton_k2aaa','k2plus_aaa'); $msg="results: record the P2.53 seed $seed Spider test of the frozen arms"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/list_p253_publication\.py|tests/test_list_p253_publication\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_list_p253_publication.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; $files=@(uv run --no-sync python -m scripts.list_p253_publication --seed $seed --arms $arms); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; uv run --no-sync python -m scripts.status_p253 --seed $seed; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

1c. Seed 0 reference rows on Spider test (owner, 2026-10-28; eval only,
   about 10 min each, about 2 h for all; `--arms` takes a subset): FedAvg,
   `gold_k2aaa`, `central_mix`, `central`, base, FedNTD, then the five
   `local` clients, with the P2.53 evaluator so each pairs with the method.
   On an idle GPU (set `$gpu`); prints the table with the method pairs:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p253_reference_test.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p253_reference_test --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.53 reference rows failed' }; uv run --no-sync python -m scripts.run_p253_reference_test --phase status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

   Publish them once the 1c lane has finished: a publication mid-run
   tracks the reference manifest that the lane still rewrites, and the next
   publication's clean-tree check would then stop:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m scripts.run_p253_reference_test --phase files); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record the P2.53 seed-0 reference rows on Spider test'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

2. Seed 1, GPU 0: the method, then its primary comparator (gold K2 and
   `gmixgold_k2aaa`), then `hinton_k2aaa` and `k2plus_aaa` (rerun to
   resume). The pull admits only the P2.53 runner fix (`..._eval_spider`
   runtime reports no longer pick up `..._eval_spider_test`) and is a no-op
   once pulled. To switch a running lane to this order, stop it with Ctrl+C
   first (training and evaluation resume):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $seed='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -c "from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; exclusive_lock(r.AUDIT / 'gpu_0.lock').__enter__()"; if ($LASTEXITCODE -ne 0) { throw 'GPU 0 lane still running' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|scripts/run_p253_confirmation\.py|tests/test_p253_confirmation\.py|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p253_confirmation.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; foreach ($arm in @('hinton_k2','mixkd50_k2aaa','gold_k2','gmixgold_k2aaa','hinton_k2aaa','k2plus_aaa')) { uv run --no-sync python -m scripts.run_p253_confirmation --phase run --seed $seed --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.53 seed $seed $arm failed" }; Write-Host "GPU $gpu P2.53 seed $seed $arm complete" } }
```

3. Seed 1, GPU 1, once the step 1c lane has finished: FedCoLLM-style (its
   own A1 start):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $seed='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; foreach ($arm in @('fedcollm_style')) { uv run --no-sync python -m scripts.run_p253_confirmation --phase run --seed $seed --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.53 seed $seed $arm failed" }; Write-Host "GPU $gpu P2.53 seed $seed $arm complete" } }
```

4. Seed 2: steps 2 and 3 with `$seed='2'`, each on the GPU that frees
   first.

5. Seed 0 (P2.37 `hinton_akaka_plain` A2-A3, the FedCoLLM-style last K,
   Spider test on every arm), on whichever GPU is free (set `$gpu`):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $seed='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p237_phase_e --phase run --arm hinton_akaka_plain; if ($LASTEXITCODE -ne 0) { throw 'P2.37 hinton_akaka_plain failed' }; foreach ($arm in @('fedcollm_style','mixkd50_k2aaa','hinton_k2aaa','k2plus_aaa','gmixgold_k2aaa')) { uv run --no-sync python -m scripts.run_p253_confirmation --phase run --seed $seed --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.53 seed $seed $arm failed" }; Write-Host "GPU $gpu P2.53 seed $seed $arm complete" } }
```

6. Publish one seed once both of its lanes have stopped (set `$seed`;
   lanes of other seeds may keep running):

```powershell
& { $ErrorActionPreference='Stop'; $seed='1'; $msg="results: record P2.53 confirmation seed $seed"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m scripts.list_p253_publication --seed $seed); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

   Finished arms of a seed while another of its lanes still runs (owner,
   2026-10-29: seed 1 numbers for the advisor while FedCoLLM-style runs;
   nested `bc5fe14`). Commits only those arms' stage, evaluation and
   runtime files, never the shared run manifest; step 6 later publishes
   the manifest and the rest. List the finished arms in `$arms`:

```powershell
& { $ErrorActionPreference='Stop'; $seed='1'; $arms=@('hinton_k2','gold_k2','mixkd50_k2aaa','gmixgold_k2aaa','hinton_k2aaa','k2plus_aaa'); $msg="results: record the finished P2.53 seed $seed arms"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/list_p253_publication\.py|tests/test_list_p253_publication\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_list_p253_publication.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; $files=@(uv run --no-sync python -m scripts.list_p253_publication --seed $seed --arms $arms); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; uv run --no-sync python -m scripts.status_p253 --seed $seed; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

Added 2026-10-28 (LAB_LOG addendum 2 and the direction entry); code not
built yet, commands follow once it is (the new arms need runner changes, made
only while no lane imports `run_p253_confirmation`, or in a new runner):

- 6b. FedAvg (3 plain rounds from the base model) and `gold_k2aaa` (the
  seed's `gold_k2` plus 3 plain rounds), seeds 1 and 2, each evaluated at A3
  on Spider test and the five dev sets. About 8 GPU-h per arm for both seeds.
- 6c. Spider dev and BIRD dev at A1 and A2 of `mixkd50_k2aaa`,
  `hinton_k2aaa`, `k2plus_aaa`, `gmixgold_k2aaa`, seeds 1 and 2 (the
  forgetting figure; about 5 GPU-h).
- 6d. Teacher Qwen2.5-Coder-7B zero-shot on Spider test: done, 77.22
  (nested `c3e3961`, LAB_LOG 2026-10-29; commands in the
  [runbook](../archive/completed_runbooks/PIPELINE_P253_TEACHER_TEST_2026-10-29.md)).

7. After all three seeds are published: the frozen test and its summary.
   Before this step, add to `--phase analyze` the seeds 1-2 sensitivity
   analysis (addendum 1) and C6, C7 with their own Holm family, reading the
   seed-0 FedAvg and `gold_k2aaa` rows from the P2.53 reference manifest
   (addendum 2).

```powershell
& { $ErrorActionPreference='Stop'; $msg='results: record the P2.53 confirmation test'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p253_confirmation --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p253_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p253_confirmation/summary.md }
```

8. After step 7: E2, student Qwen2.5-Coder-0.5B-Instruct (LAB_LOG
   2026-10-29): the method, `gmixgold_k2aaa`, `hinton_k2aaa` and FedAvg,
   seeds 0-2, Spider test and the five dev sets; about 100 GPU-h. Code
   not built yet (new runner on the P2.53 pattern, cross-student teacher
   cache audit first).

## P2.51: execution-filtered client replay (GPU 0)

`xmixkd50_k2aaa` = P2.48 `mixkd50_k2aaa` with the replay pool restricted to
the 5,319 BIRD rows whose teacher SQL executes to the gold result; about 9 h
for three rounds. No lane runs, so step 1 pulls the shared code change (a
new `--client-replay-row-filter` option, off unless set).

1. Pull, test, prepare (CPU). Both GPUs must be idle:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -c "from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; exclusive_lock(r.AUDIT / 'gpu_0.lock').__enter__(); exclusive_lock(r.AUDIT / 'gpu_1.lock').__enter__()"; if ($LASTEXITCODE -ne 0) { throw 'A GPU lane is running' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(fedicl_sql/federated/(round_loop|stage_chain)\.py|experiments/federated/run\.py|scripts/(run|list)_p251_[a-z_]+\.py|scripts/audit_client_drift\.py|tests/test_(p251_exec_filtered_replay|client_replay)\.py|docs/.+|AGENTS\.md|.+\.md|audits/.+)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_client_replay.py tests/test_p251_exec_filtered_replay.py tests/test_p250_server_replay_rows.py tests/test_p249_gold_k2_replay.py tests/test_p248_replay_compact_fsl.py tests/test_p247_client_replay.py tests/test_stage_chain.py tests/test_round_loop.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p251_exec_filtered_replay --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.51 preparation failed' }; Write-Host 'P2.51 prepared' }
```

2. Run on GPU 0 (A1, A2, A3 with their evaluations; rerun the same command
   to resume):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $arm='xmixkd50_k2aaa'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p251_exec_filtered_replay --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.51 $arm failed" }; Write-Host "GPU $gpu P2.51 $arm complete" }
```

3. Publish every evaluated endpoint when the lane has stopped:

```powershell
& { $ErrorActionPreference='Stop'; $exp='p251_exec_filtered_replay'; $n='251'; $msg='results: record P2.51 execution-filtered replay'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only HEAD); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $dirty=@($dirty | Where-Object { $_ -notlike "audits/protocol_v2/${exp}_s0/*" }); if ($dirty.Count -ne 0) { throw "Tracked changes need review: $dirty" }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md|scripts/run_p251_exec_filtered_replay\.py)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
```

## P2.52: client replay in the reverse roles (GPU 1)

`mixkd50_k2aaa_rev` = the P2.43 `hinton_k2aaa_rev` rounds (BIRD clients)
plus the method's top-50 replay from 2,000 Spider training rows with the
P2.43 Spider teacher cache. Primary metric BIRD EX. About 13-15 h. Step 1
may run while P2.51 trains on GPU 0: its pull admits only the new P2.52
files and documentation, which the P2.51 lane never imports. If it reports
shared code as incoming, run P2.51 step 1 first.

1. Pull, test, prepare (CPU). GPU 1 must be idle:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -c "from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; exclusive_lock(r.AUDIT / 'gpu_1.lock').__enter__()"; if ($LASTEXITCODE -ne 0) { throw 'GPU 1 lane is running' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(run|list)_p252_[a-z_]+\.py|tests/test_p252_reverse_replay\.py|docs/.+|AGENTS\.md|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files (run P2.51 step 1 first?): $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p252_reverse_replay.py tests/test_p243_reverse_roles.py tests/test_client_replay.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p252_reverse_replay --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.52 preparation failed' }; Write-Host 'P2.52 prepared' }
```

2. Run on GPU 1 (rerun the same command to resume):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $arm='mixkd50_k2aaa_rev'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p252_reverse_replay --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.52 $arm failed" }; Write-Host "GPU $gpu P2.52 $arm complete" }
```

3. Publish when the lane has stopped and P2.51 is not mid-publication (with
   both GPUs idle it may also pull the new P2.53 files; publish P2.51 next):

```powershell
& { $ErrorActionPreference='Stop'; $exp='p252_reverse_replay'; $n='252'; $msg='results: record P2.52 reverse-roles replay'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only HEAD); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $dirty=@($dirty | Where-Object { $_ -notlike "audits/protocol_v2/${exp}_s0/*" }); if ($dirty.Count -ne 0) { throw "Tracked changes need review: $dirty" }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md|scripts/run_p252_reverse_replay\.py|scripts/(run|list)_p253_[a-z_]+\.py|tests/test_p253_confirmation\.py)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
```

## P2.46: top-k teacher logits at K2 (deferred, owner 2026-10-24)

Question and the readings fixed before the run: LAB_LOG 2026-10-24. Code:
nested `14fa97d`, `4a9553c`. Dev sets only, seed 0.

`top50_k2aaa` and `top200_k2aaa` repeat the P2.37 `hinton_k2aaa` K2 with the
same teacher cache, cut to the top 50 or 200 teacher logits per token.
`--until k2` stops after the K2 evaluation (Spider and BIRD). Comparators:
the published Hinton and gold K2 (62.28 and 59.09 Spider). About 5-6 h per
arm, one per GPU. No new cache, no new disk. Memory: expected a few hundred
MB above the Hinton K row (19.9 GiB); check the shared GPU memory in the first
15 minutes and send the K2 peak reserved VRAM from the log.

0. CPU check first (owner, 2026-10-24): how much teacher mass the top-k cut
   keeps, read from the P2.27 cache for 1,000 sampled rows (nested
   `4a2f8c1`). Runs from origin without a pull, safe while any lane runs;
   writes only `audits/protocol_v2/teacher_topk_mass_s0/`. Send the table.
   Done 2026-10-24 (LAB_LOG). Commit its output (safe while a lane runs; it
   admits only result files, Markdown and the two audit files):

```powershell
& { $ErrorActionPreference='Stop'; $dir='audits/protocol_v2/teacher_topk_mass_s0'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md|scripts/audit_teacher_topk_mass\.py|tests/test_audit_teacher_topk_mass\.py)$' }); if ($bad.Count -ne 0) { throw "Incoming code a running lane may use: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@("$dir/summary.json", "$dir/summary.md"); foreach ($file in $files) { if (-not (Test-Path $file)) { throw "Missing $file" }; git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if (@(Compare-Object ($files | Sort-Object) ($actual | Sort-Object)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record the teacher top-k kept-mass audit'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git show origin/main:scripts/audit_teacher_topk_mass.py | uv run --no-sync python - --rows 1000; if ($LASTEXITCODE -ne 0) { throw 'Top-k mass audit failed' } }
```

1. Pull, test, prepare (CPU). Only when no lane runs on either GPU (the
   command checks the GPU locks): the pull changes code every K2AAA lane
   imports.

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; uv run --no-sync python -c "from contextlib import ExitStack; from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; s=ExitStack(); [s.enter_context(exclusive_lock(r.AUDIT / f'gpu_{d}.lock')) for d in '01']; s.close()"; if ($LASTEXITCODE -ne 0) { throw 'A GPU lane is running; wait until none runs' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_teacher_topk.py tests/test_p246_teacher_topk.py tests/test_p237_phase_e.py tests/test_taid.py tests/test_virtual_teacher.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p246_teacher_topk --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.46 preparation failed' }; Write-Host 'P2.46 prepared' }
```

   Then publish P2.43 (its step 5) and P2.44 (its step 3) before starting
   the lanes below.

2. Run K2, one arm per GPU. Rerun the identical command after an
   interruption; finished work is skipped.

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $arm='top50_k2aaa'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p246_teacher_topk --phase run --arm $arm --until k2; if ($LASTEXITCODE -ne 0) { throw "P2.46 $arm failed" }; Write-Host "GPU $gpu P2.46 $arm K2 complete" }
```

   GPU 1 runs P2.41 `hinton_t1_k2aaa` instead of `top200_k2aaa` (LAB_LOG
   2026-10-24 top-k mass audit: top-200 is nearly the top-50 target; at T=1
   the top 10 tokens are the whole target). P2.41 runs the full chain
   (about 13-15 h); its K2 is read from the status check or its manifest.

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p241_hinton_t1 --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.41 preparation failed' }; uv run --no-sync python -m scripts.run_p241_hinton_t1 --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.41 hinton_t1_k2aaa failed' }; Write-Host "GPU $gpu P2.41 hinton_t1_k2aaa complete" }
```

3. Read the result (CPU, safe while the other arm runs; it rewrites only the
   P2.46 summary files). Send the table and the kept-mass lines:

```powershell
& { $ErrorActionPreference='Stop'; uv run --no-sync python -m scripts.run_p246_teacher_topk --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.46 analysis failed' }; Get-Content audits/protocol_v2/p246_teacher_topk_s0/summary.md }
```

4. Publish every evaluated endpoint, when no P2.46 lane runs:

```powershell
& { $ErrorActionPreference='Stop'; $exp='p246_teacher_topk'; $n='246'; $msg='results: record P2.46 top-k teacher K2'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only HEAD); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $dirty=@($dirty | Where-Object { $_ -notlike "audits/protocol_v2/${exp}_s0/*" }); if ($dirty.Count -ne 0) { throw "Tracked changes need review: $dirty" }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md|scripts/audit_teacher_topk_mass\.py|tests/test_audit_teacher_topk_mass\.py)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
```

## P2.44: self-teacher control (base Coder-1.5B as the K2 teacher)

Question and the readings fixed before the run: LAB_LOG 2026-10-23. Code:
nested `e3a3e22`, `1f0bee7`. Dev sets only, seed 0.

`self_k2aaa` repeats every P2.37 `hinton_k2aaa` command; only the K2 teacher
changes, from the 4-bit 7B to the base Coder-1.5B (fp16) through a new BIRD
logit cache. Comparators: the published `hinton_k2aaa`, `gold_k2aaa` and
P2.38 `virtual_k2aaa`.

Cost: cache build about 1-3 h and about 155 GB of disk (the runner refuses to
start under 200 GB free), then the chain about 13-15 h. Send the peak
reserved VRAM of the cache build and K2 from the logs, and check the shared
GPU memory in the first 15 minutes.

1. Pull and prepare (CPU). Safe while the P2.43 lanes run: it admits only the
   three new P2.44 files, the status script and Markdown, none of which a
   running lane imports. Prints the free disk:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-status HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^A\s+(scripts/run_p244_self_teacher\.py|scripts/list_p244_publication\.py|tests/test_p244_self_teacher\.py)$' -and $_ -notmatch '^[AM]\s+(scripts/status_k2aaa_lanes\.py|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming change a running lane may import: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p244_self_teacher.py tests/test_status_k2aaa_lanes.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p244_self_teacher --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.44 preparation failed' }; $free=[math]::Round((Get-PSDrive (Get-Location).Drive.Name).Free / 1GB); Write-Host "P2.44 prepared; free disk $free GB" }
```

2. GPU 0, after its P2.43 lane prints "complete" (the P2.37 GPU lock refuses
   a busy card): cache, then the chain. Rerun the identical command after an
   interruption; finished work is skipped.

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p244_self_teacher --phase cache; if ($LASTEXITCODE -ne 0) { throw 'P2.44 self-teacher cache failed' }; uv run --no-sync python -m scripts.run_p244_self_teacher --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.44 self_k2aaa failed' }; Write-Host "GPU $gpu P2.44 self_k2aaa complete" }
```

2b. Read the result (CPU, safe while P2.43 lanes run; it reads the P2.44
   manifest and the published comparators and rewrites only the P2.44
   summary files):

```powershell
& { $ErrorActionPreference='Stop'; uv run --no-sync python -m scripts.run_p244_self_teacher --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.44 analysis failed' }; Get-Content audits/protocol_v2/p244_self_teacher_s0/summary.md }
```

3. Analyze and publish, when no P2.43 or P2.44 lane runs (the check for
   tracked changes fails while a P2.43 lane updates its manifest):

```powershell
& { $ErrorActionPreference='Stop'; $exp='p244_self_teacher'; $n='244'; $msg='results: record P2.44 self-teacher control'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only HEAD); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $dirty=@($dirty | Where-Object { $_ -notlike "audits/protocol_v2/${exp}_s0/*" }); if ($dirty.Count -ne 0) { throw "Tracked changes need review: $dirty" }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
```

## P2.43: reverse roles (BIRD private, Spider public), early signal first

Question, metric and how to read the early signal: LAB_LOG 2026-10-17 (the
entry fixing BIRD EX as the primary metric here). Code: nested `dbd7a34`,
`68f04bc`; split `7694f3f`. Dev sets only, seed 0.

- `gold_k2aaa_rev`, `hinton_k2aaa_rev`: from the base model, two server epochs
  on all 8,659 Spider train rows (gold CE, or Hinton T=2 with a new Spider
  teacher logit cache), then three plain FedAvg rounds on the BIRD
  `alpha_0.1/k5` clients. The P2.37 K2AAA recipe with the data swapped.
- `fl_bird`: three plain rounds on the BIRD clients from the base model.
- `central_bird`: all BIRD train rows in one place, three epochs.
- Evaluation: Spider and BIRD after each stage or epoch, all five sets at the
  last one.

Early signal: GPU 1 runs `gold_k2aaa_rev` to A1 (no cache needed, about 3-4 h
K2 plus 3 h A1 plus evaluations), then `fl_bird`. GPU 0 builds the Spider
cache (first build, send its time), then runs `hinton_k2aaa_rev` to A1. Send
the step 3 table after each K2 and A1 evaluation.

Memory: Spider K2 prompts are under 3,000 tokens, below every BIRD K row;
BIRD rounds and central BIRD use the P2.17 BIRD lengths (19.8 GB). Check each
process's shared GPU memory in its first 15 minutes and send the peak
reserved VRAM of the cache build, K2 and A1 from the logs.

1. Pull, test, prepare (CPU; no lane may run on either GPU). Also prints the
   free disk space; the cache needs about 100 GB and the runner refuses to
   start under 130 GB:

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; uv run --no-sync python -c "from contextlib import ExitStack; from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; s=ExitStack(); [s.enter_context(exclusive_lock(r.AUDIT / f'gpu_{d}.lock')) for d in '01']; s.close()"; if ($LASTEXITCODE -ne 0) { throw 'A GPU lane is running; wait until none runs' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p243_reverse_roles.py tests/test_p237_phase_e.py tests/test_status_k2aaa_lanes.py tests/test_stage_chain.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.43 preparation failed' }; $free=[math]::Round((Get-PSDrive (Get-Location).Drive.Name).Free / 1GB); Write-Host "P2.43 prepared; free disk $free GB" }
```

2. Run; rerun the identical command after an interruption (finished stages
   are skipped, an interrupted one resumes).

   GPU 0, Spider cache then `hinton_k2aaa_rev` to A1:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase cache; if ($LASTEXITCODE -ne 0) { throw 'P2.43 Spider teacher cache failed' }; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase run --arm hinton_k2aaa_rev --until a1; if ($LASTEXITCODE -ne 0) { throw 'P2.43 hinton_k2aaa_rev failed' }; Write-Host "GPU $gpu P2.43 hinton_k2aaa_rev through A1 complete" }
```

   GPU 1, `gold_k2aaa_rev` to A1, then `fl_bird`:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase run --arm gold_k2aaa_rev --until a1; if ($LASTEXITCODE -ne 0) { throw 'P2.43 gold_k2aaa_rev failed' }; Write-Host "GPU $gpu P2.43 gold_k2aaa_rev through A1 complete"; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase run --arm fl_bird; if ($LASTEXITCODE -ne 0) { throw 'P2.43 fl_bird failed' }; Write-Host "GPU $gpu P2.43 fl_bird complete" }
```

3. Read the early signal (CPU, read-only for the lanes, safe while they run;
   it rewrites only the summary files):

```powershell
& { $ErrorActionPreference='Stop'; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.43 analysis failed' }; Get-Content audits/protocol_v2/p243_reverse_roles_s0/summary.md }
```

4. After the early signal is read (owner's choice, LAB_LOG): continue a chain
   to A3 with the step 2 run command without `--until a1`, and run
   `central_bird` on a free GPU:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $arm='central_bird'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p243_reverse_roles --phase run --arm $arm; if ($LASTEXITCODE -ne 0) { throw "P2.43 $arm failed" }; Write-Host "GPU $gpu P2.43 $arm complete" }
```

   (`$arm` can be `hinton_k2aaa_rev` or `gold_k2aaa_rev` to finish a chain.)

5. Publish every evaluated endpoint (only when no P2.43 lane runs; the lister
   checks all P2.43 lane locks). Repeat after later endpoints:

```powershell
& { $ErrorActionPreference='Stop'; $exp='p243_reverse_roles'; $n='243'; $msg='results: record P2.43 reverse roles endpoints'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only HEAD); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $dirty=@($dirty | Where-Object { $_ -notlike "audits/protocol_v2/${exp}_s0/*" }); if ($dirty.Count -ne 0) { throw "Tracked changes need review: $dirty" }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
```

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

## P2.38 and P2.39: virtual-teacher control and frozen-A pilot (run first)

Questions and how to read them: LAB_LOG 2026-10-13. Code: nested `4a8225c`,
`94ed37b` (P2.38), `fe5ed88`, `7e8e3ba` (P2.39). Dev sets only.

- P2.38 `virtual_k2aaa`: every `hinton_k2aaa` command, with the 7B teacher
  replaced by a fixed target (probability `a` on the gold token, the rest
  spread evenly over the vocabulary). Prepare measures `a` from the P2.27
  teacher logit cache (CPU, about 10-20 min). About 20 h on one GPU.
- P2.39 `hinton_k2_fa`, `gold_k2_fa`: the private rounds of `hinton_k2aaa` and
  `gold_k2aaa`, from the same published K2 adapters, with LoRA A frozen
  (clients train and send only B). Pilot: one round of `hinton_k2_fa` with
  Spider and BIRD (about 4 h with the other GPU busy), against `hinton_k2aaa`
  A1 (Spider 71.57, BIRD 36.77). A full arm takes about 11 h.

Order: step 1 pulls code that P2.37 lanes import, so it runs only when no
P2.37 lane is running (the command checks). A P2.37 lane that finished before
step 1 is published with P2.37 step 2b after step 1 (step 2b refuses unmerged
code).

Memory: P2.38 K2 is the measured Hinton K path (19.9 GiB peak reserved) with
the cached teacher tensor replaced by a generated tensor of the same size.
P2.39 rounds are the plain A path (about 14.2 GiB) with fewer trainable
tensors. No new probe; check the process's shared GPU memory in the first 15
minutes of each.

1. Pull, test, prepare both (CPU; no P2.37 lane may be running):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; uv run --no-sync python -c "from scripts import run_p237_phase_e as r; r.idle_lanes().close()"; if ($LASTEXITCODE -ne 0) { throw 'A P2.37 lane is running; wait until none runs' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_virtual_teacher.py tests/test_p238_virtual_teacher.py tests/test_frozen_lora_a.py tests/test_p237_phase_e.py tests/test_server_retention.py tests/test_stage_chain.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p238_virtual_teacher --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.38 preparation failed' }; uv run --no-sync python -m scripts.run_p239_frozen_a --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'P2.39 preparation failed' }; Write-Host 'P2.38 and P2.39 prepared' }
```

   It prints the teacher statistics (`gold_prob` is `a`). Send them in chat.

2. GPU 0, P2.38; rerun the identical command after an interruption. Spider
   and BIRD after K2 and each private round, all five sets after A3:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p238_virtual_teacher --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.38 virtual_k2aaa failed' }; Write-Host "GPU $gpu P2.38 virtual_k2aaa complete" }
```

3. GPU 1, P2.39 pilot (one round), then print the comparison with
   `hinton_k2aaa` A1. Send the printed table in chat:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $arm='hinton_k2_fa'; $until='a1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p239_frozen_a --phase run --arm $arm --until $until; if ($LASTEXITCODE -ne 0) { throw "P2.39 $arm failed" }; uv run --no-sync python -m scripts.run_p239_frozen_a --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.39 analysis failed' } }
```

   Done 2026-10-13: Spider -1.55, BIRD +0.85 (LAB_LOG). Not continued
   (owner decision 2026-10-13). Next on GPU 1: P2.37 step 2 with `$gpu='1'`
   and `$arm='central_mix'`, then `$arm='local'`; publish each with P2.37
   step 2b after P2.40 step 1 has pulled the code.

4. P2.38 analyze and publish, after P2.40 step 1 has pulled the code (origin
   already holds P2.40-P2.42 code, so before that pull the incoming-code
   check refuses; the finished P2.38 files wait safely on the server):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p238_virtual_teacher --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p238_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.38 virtual-teacher control'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p238_virtual_teacher_s0/summary.md }
```

5. P2.39 publish (publishes every evaluated endpoint, so the pilot's A1
   alone), after P2.40 step 1 has pulled the code (before that, the
   incoming-code check refuses):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p239_frozen_a --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p239_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.39 frozen-A rounds'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p239_frozen_a_s0/summary.md }
```

## P2.40, P2.41, P2.42: TAID, Hinton T=1, central from K2 (after P2.38 and the GPU 1 lane)

Questions and how to read them: LAB_LOG 2026-10-13 (P2.40 entry; P2.41 and
P2.42 entry). Code: nested `c5d9735`, `02c30d3` (P2.40), `9849a46` (P2.41),
`129c8ee` (P2.42). Dev sets only.

- P2.40 `taid_k2aaa`: every `hinton_k2aaa` command, except that the K2 soft
  target is TAID (Shing et al., ICLR 2025): it starts as a mix of the
  student's own distribution (60%) and the teacher's (40%) in logit space and
  moves to the pure teacher by the end of K2. T=1 as published; same teacher
  logit cache, same 0.5 gold CE + 0.5 KD weights, same three private rounds.
  About 20 h on one GPU. With 1,180 K2 updates the schedule is the linear path
  from 0.4 to 1; the K2 metrics record `t` after every update.
- P2.41 `hinton_t1_k2aaa`: every `hinton_k2aaa` command with T=1 at K2 instead
  of T=2. TAID minus this arm changes only the target. About 20 h.
- P2.42 `central_k2`: the P2.27 central Spider run (three epochs, all Spider
  train rows in one place) started from the `hinton_k2aaa` K2 adapter, read
  epoch N against round aN. About 11 h.

Order: step 1 pulls training code that every running lane imports, so it runs
only when no P2.37, P2.38 or P2.39 lane runs on either GPU (the command checks
both GPU locks). It also brings any fix not yet pulled, such as the P2.39
frozen-A aggregation fix `e5c7fd6`. Then P2.40 on GPU 0 and P2.41 on GPU 1 at
the same time; P2.42 on whichever GPU frees first.

Memory: P2.40 is the Hinton K path (19.9 GiB peak reserved) plus one float32
target tensor per row, a few hundred MB; P2.41 is the Hinton K path unchanged;
P2.42 is the P2.27 central path. No new probe; check each process's shared GPU
memory in its first 15 minutes and send the P2.40 K2 peak from the log.

1. Pull, test, prepare all three (CPU; no lane may be running):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; uv run --no-sync python -c "from contextlib import ExitStack; from scripts import run_p237_phase_e as r; from scripts.run_p213_fullgold_plan import exclusive_lock; s=ExitStack(); [s.enter_context(exclusive_lock(r.AUDIT / f'gpu_{d}.lock')) for d in '01']; s.close()"; if ($LASTEXITCODE -ne 0) { throw 'A GPU lane is running; wait until none runs' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_taid.py tests/test_p240_taid.py tests/test_p241_hinton_t1.py tests/test_p242_central_from_k2.py tests/test_trainer_epoch_resume.py tests/test_frozen_lora_a.py tests/test_p237_phase_e.py tests/test_server_retention.py tests/test_stage_chain.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; foreach ($exp in 'run_p240_taid','run_p241_hinton_t1','run_p242_central_from_k2') { uv run --no-sync python -m "scripts.$exp" --phase prepare; if ($LASTEXITCODE -ne 0) { throw "$exp preparation failed" } }; Write-Host 'P2.40, P2.41 and P2.42 prepared' }
```

2. Run; rerun the identical command after an interruption. Spider and BIRD
   after each stage or epoch, all five sets at the end.

   GPU 0, P2.40:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p240_taid --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.40 taid_k2aaa failed' }; Write-Host "GPU $gpu P2.40 taid_k2aaa complete" }
```

   GPU 1, P2.41:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p241_hinton_t1 --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.41 hinton_t1_k2aaa failed' }; Write-Host "GPU $gpu P2.41 hinton_t1_k2aaa complete" }
```

   First free GPU (set `$gpu`), P2.42:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p242_central_from_k2 --phase run; if ($LASTEXITCODE -ne 0) { throw 'P2.42 central_k2 failed' }; Write-Host "GPU $gpu P2.42 central_k2 complete" }
```

3. Analyze and publish one experiment (safe while other lanes run). Shown for
   P2.40; for the others change the first three values:

   | Experiment | `$exp` | `$n` | `$msg` |
   |---|---|---|---|
   | P2.40 | `p240_taid` | `240` | `results: record P2.40 TAID K2AAA` |
   | P2.41 (needs P2.40 finished) | `p241_hinton_t1` | `241` | `results: record P2.41 Hinton T=1 K2AAA` |
   | P2.42 | `p242_central_from_k2` | `242` | `results: record P2.42 central from K2` |

```powershell
& { $ErrorActionPreference='Stop'; $exp='p240_taid'; $n='240'; $msg='results: record P2.40 TAID K2AAA'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
```

## P2.37: phase E baselines, Coder-1.5B, seed 0

Arm list and readings: LAB_LOG 2026-10-11 (phase E). Code: nested `ed6fa57`.
Dev sets only; never Spider test. Measured P2.27 stage times on this server:
plain A about 1.6 h alone (2.7 h with both GPUs busy), gold K about 2.7 h,
Hinton K about 3.6-4.5 h, about 20-30 min per evaluated set.

Run one arm at a time, in priority order, on whichever GPU frees first. Arms are independent; the order only decides
which answers arrive first.

| Priority | Arm | What it answers | Estimate |
|---:|---|---|---|
| 1 | `hinton_k2aaa` | K-first schedule (Q3), Hinton (published `5cfd646`) | about 20 h |
| 2 | `gold_k2aaa` | its gold pair: teacher vs gold under K-first (Q2) (published `dcac509`) | about 17 h |
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
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/audit_teacher_gold_agreement\.py|tests/test_audit_teacher_gold_agreement\.py|scripts/run_p254_synsql_public\.py|tests/test_p254_synsql_public\.py|scripts/audit_pool_overlap\.py|tests/test_audit_pool_overlap\.py|scripts/status_p254\.py|scripts/status_p253\.py|tests/test_status_p253\.py|scripts/run_p253_reference_test\.py|tests/test_p253_reference_test\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming code: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p237_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.37 phase E baselines'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p237_phase_e_s0/summary.md }
```

## Next

The P2.53 confirmation at the top of this file. Not queued: P2.31, P2.35,
P2.32 (alpha 0.5, now E1, waits for a revision).
