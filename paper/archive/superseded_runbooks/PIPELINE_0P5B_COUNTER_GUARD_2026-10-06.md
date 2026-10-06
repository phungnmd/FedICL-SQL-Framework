<!-- Superseded: automatic shared-memory counters removed at owner request. -->
# FedLS-SQL run queue

This file owns runnable experiment commands. Results belong in
[LAB_LOG.md](LAB_LOG.md). Run every command from the Windows `fedicl-sql/` root.
The earlier 1.5B queue remains in the
[dated archive](../archive/superseded_runbooks/PIPELINE_1P5B_PRE_0P5B_2026-10-05.md).

## 0.5B screen, 2026-10-06

Owner reports on 2026-10-06: CPU preparation, full teacher-cache audit and all
three server GPU probes passed. Gold initially stopped on a Windows counter
error, then gold/Hinton passed after the counter recovered. Compact reports
are not published yet; no 0.5B training result is claimed. Steps 1-2 remain for
reproduction; proceed to step 3 for the current prepared server. Server lane status is
unverified: synchronize `main` only when all old lanes are idle and unpublished
results are preserved. Never pull, edit, commit, or push this checkout while a
lane is running. Both baseline training/evaluation subprocesses must exit and both terminals
reach their publication wait before the baseline commit; both public lane
commands must exit before final publication.

Fresh student: `Qwen/Qwen2.5-Coder-0.5B-Instruct`; frozen teacher:
`Qwen/Qwen2.5-Coder-7B-Instruct`. Do not initialize from a 1.5B adapter. Changing
size and code specialization together does not isolate a model-size effect.

| Arm | Schedule | Spider passes | BIRD epochs |
|---|---|---:|---:|
| Centralized | one continuous E3 run, keep E1/E2/E3 | 3 | 0 |
| FL | A > A > A | 3 | 0 |
| Gold AKAKA | A > K[ce] > A > K[ce] > A | 3 | 2 |
| Hinton AKAKA | A > K[fkl] > A > K[fkl] > A | 3 | 2 |
| Gold AKKAA | A > K2[ce] > A > A | 3 | 2 |
| Hinton AKKAA | A > K2[fkl] > A > A | 3 | 2 |

**KK means one K with 2 continuous epochs**, one optimizer and a cosine horizon
planned for both epochs from the start. Keep epoch adapters and `resume_latest`.
Only initial A1 is shared. The first K epoch cannot be shared with AKAKA because
its LR horizon differs. The schedule comparison therefore includes the effect
of the continuous versus restarted public LR schedule.

The runner preserves the recent training recipe: seed 0; BF16 student weights,
`target_fp32`, response-window logits, batch 1, accumulation 16, AdamW LR 2e-4,
cosine/warmup .03, LoRA r16/alpha32/dropout .05 on attention and MLP, non-reentrant
gradient checkpointing. Each A uses 5 Spider clients, the existing alpha .5
split, one local epoch and sample-weighted factor-wise plaintext FedAvg. Clients
and inference stay SQL-only, no ICL. Every K uses all 9,428 BIRD rows with
evidence. Gold uses CE only; Hinton uses CE/KL .5/.5 and temperature 2. Max length
is 7,168 for private/Hinton, 7,424 for gold, with overflow rejected. Evaluation
uses batch 16 without fallback, unchanged Spider 60 s/BIRD 30 s execution budgets,
Spider/BIRD at intermediate endpoints and all five sets at final endpoints.

The 1.5B P2.17 reference was about 18.9 GiB reserved for K; the older
`full_bf16` BIRD path paged about 66.5 GiB to host RAM and took 16.4 h. These are
historical measurements, not 0.5B estimates. Keep batch 1 until the new smoke
and actual throughput show headroom. Allocator cap .88 and reserved <=21.5 GiB
are enforced. Windows per-process shared GPU memory is sampled; two consecutive
samples above 512 MiB stop the owned process tree. This is a conservative policy,
not a measured hardware boundary. Missing counter support fails closed. The
first CUDA allocation may follow long CPU preparation; successful completion
still requires an owned-PID GPU sample. Do not bypass a failed memory gate.

## 1. CPU preparation and reuse the existing teacher cache

The directory containing `qwen15b` holds **7B teacher logits rendered for the
old student tokenizer**, not 1.5B weights. Reuse is allowed only after checking
source/target rendered IDs, labels and prompt boundaries for all rows, complete
token-ID mappings, pool/profile/evidence metadata, shard shapes/dtypes/finiteness
and tensor digests. Audit is read-only, loads tokenizer/config files, and does
not regenerate logits or load teacher weights. The report is separate from the
original cache metadata. Training rechecks tokenizer/vocab identity and tensor
bytes and rejects misses. Full cache I/O can take time; run the audit once.

The local tokenizer comparison matched all 151,665 token mappings; padded output
vocabularies are 151,936 (student) and 152,064 (teacher). This preliminary check
does not establish server cache coverage. If audit fails, retain the cache and
inspect the mismatch before any Hinton run. The current screen uses seed 0.

```powershell
$ErrorActionPreference='Stop'; uv run python -m scripts.run_p218_student_schedule --phase prepare --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.18 preparation failed' }; if (!(Test-Path 'audits/protocol_v2/p218_student_schedule_s0/run_manifest.json')) { throw 'Preparation manifest missing' }
```

```powershell
$ErrorActionPreference='Stop'; uv run python -m scripts.audit_teacher_logit_cache --cache-dir artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0 --model Qwen/Qwen2.5-Coder-0.5B-Instruct --pool processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv --dataset-profile bird_with_evidence --max-len 7168 --seed 0 --out audits/protocol_v2/p218_student_schedule_s0/cache_audit.json; if ($LASTEXITCODE -ne 0) { throw 'Teacher cache reuse audit failed' }; if (!(Test-Path 'audits/protocol_v2/p218_student_schedule_s0/cache_audit.json')) { throw 'Cache audit missing' }
```

## 2. Isolated GPU probes, no training lane yet

Run each probe as a separate process so it exits and releases CUDA memory before
training. Each uses fresh temporary outputs and 32 longest-sequence/longest-target
steps, including two AdamW updates. Gold and Hinton probe their actual losses;
Hinton uses the audited cache. Reports bind recipe, code content and input hashes.
The process guard also remains active during actual training and evaluation.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; foreach ($kind in @('private','gold','hinton')) { uv run python -m scripts.run_p218_student_schedule --phase probe --probe $kind --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.18 ${kind} probe failed" }; if (!(Test-Path "audits/protocol_v2/p218_student_schedule_s0/memory_${kind}.json")) { throw "Missing ${kind} probe report" } }
```

Record measured reserved/allocated VRAM, process RSS, shared memory and timing in
`docs/A5000_RUN_CONFIG.md` after both GPUs are idle. Do not call CPU tests a GPU
pass. Add measurements after this run cohort so changing code does not invalidate
prepared identity mid-run. Probes run on GPU 0; GPU 1 runs the same A5000 recipe
with continuous per-process shared-memory monitoring.

## 3. One sequential command per GPU terminal

Owner clarification, 2026-10-06: follow the older P2.15 lane layout, with one
visible terminal per GPU and separate publication commands. The single-controller
wrapper is [superseded](../archive/superseded_runbooks/PIPELINE_0P5B_SINGLE_WRAPPER_2026-10-06.md).
Preparation, cache audit and probes are already reported successful by the owner.
The remaining workflow has **two GPU commands and two publication commands**.

| Terminal | Sequential work |
|---|---|
| GPU 0 | FL AAA + eval, wait for baseline publication, gold AKAKA, gold AKKAA |
| GPU 1 | Centralized E3 + epoch eval, wait for baseline publication, Hinton AKAKA, Hinton AKKAA |

Run the two commands below in separate terminals from `fedicl-sql/` on `main`.
Both GPUs must be free before launch. If earlier lanes are already running, let
them exit first. Keep both terminals open. The code remains nested `acbc641`;
no pull, re-prepare or repeated probe is needed for this runbook-only change.
Completed work resumes under the same recipe and output roots.

Unlike P2.15, which began from an already committed A1, this screen trains A1
fresh. Each GPU command therefore waits after its baseline subprocess exits.
When **both terminals print `Baseline complete. Waiting...`**, run the baseline
publication command below from a separate CPU terminal. The wait holds no model
or GPU lane lock. It checks the remote-tracking `origin/main` tree every 30 s;
only the successful publication push releases the public schedules. Each public
runner also validates baseline completion and its committed parent before work.
If a baseline fails, its terminal stops and the sibling remains waiting; fix the
failure and resume the failed lane before attempting publication. Do not bypass
this wait or commit while a GPU training/evaluation subprocess is still active.

GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $R='scripts.run_p218_student_schedule'; uv run --no-sync python -m $R --phase fl --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.18 fl failed' }; Write-Host 'Baseline complete. Waiting for baseline publication on origin/main...'; while ($true) { $ready=@(git ls-tree --name-only origin/main -- 'audits/protocol_v2/p218_student_schedule_s0/run_manifest.json'); if ($LASTEXITCODE -ne 0) { throw 'Publication check failed' }; if ($ready.Count -gt 0) { break }; Start-Sleep -Seconds 30 }; foreach ($arm in @('gold_akaka','gold_akkaa')) { uv run --no-sync python -m $R --phase run --arm $arm --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.18 ${arm} failed" } }; Write-Host 'GPU 0 lane complete' }
```

GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $R='scripts.run_p218_student_schedule'; uv run --no-sync python -m $R --phase central --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.18 central failed' }; Write-Host 'Baseline complete. Waiting for baseline publication on origin/main...'; while ($true) { $ready=@(git ls-tree --name-only origin/main -- 'audits/protocol_v2/p218_student_schedule_s0/run_manifest.json'); if ($LASTEXITCODE -ne 0) { throw 'Publication check failed' }; if ($ready.Count -gt 0) { break }; Start-Sleep -Seconds 30 }; foreach ($arm in @('hinton_akaka','hinton_akkaa')) { uv run --no-sync python -m $R --phase run --arm $arm --seed 0; if ($LASTEXITCODE -ne 0) { throw "P2.18 ${arm} failed" } }; Write-Host 'GPU 1 lane complete' }
```

## 4. Publish baselines, then publish the final screen

Run the first command only once both GPU terminals reach their baseline wait.
It validates exact result/evaluation contracts, requires an empty index, stages
only changed allowlisted compact files, verifies the staged set, commits and
pushes. It checks/stages paths one at a time to avoid the Windows command-length
limit. It never stages adapters, weights, optimizer state or cache shards.
Once the push succeeds, both GPU commands automatically continue their two
public arms; no GPU command needs to be pasted again.

```powershell
& { $ErrorActionPreference='Stop'; function Check-Index { $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' } }; function Publish($scope) { Check-Index; uv run --no-sync python -m scripts.run_p218_student_schedule --phase analyze --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $all=@(uv run --no-sync python -c "from scripts import list_p218_publication as p; p.runner.set_seed(0); lock=p.runner.idle_lanes(); print(chr(10).join(p.collect_paths('$scope'))); lock.close()"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; $files=@(foreach ($file in $all) { $status=@(git status --porcelain --untracked-files=all -- $file); if ($LASTEXITCODE -ne 0) { throw 'File status failed' }; if ($status.Count -gt 0) { $file } }); if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m "results: record P2.18 0.5B $scope"; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; }; Publish 'baselines' }
```

Run final publication only after **both GPU lane commands exit successfully**.
Publication stays separate from training, exactly as in the older runbooks.
A push failure can be retried with the same publication command. Do not discard
staged files after a staging/commit failure without inspecting them.

```powershell
& { $ErrorActionPreference='Stop'; function Check-Index { $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' } }; function Publish($scope) { Check-Index; uv run --no-sync python -m scripts.run_p218_student_schedule --phase analyze --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $all=@(uv run --no-sync python -c "from scripts import list_p218_publication as p; p.runner.set_seed(0); lock=p.runner.idle_lanes(); print(chr(10).join(p.collect_paths('$scope'))); lock.close()"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; $files=@(foreach ($file in $all) { $status=@(git status --porcelain --untracked-files=all -- $file); if ($LASTEXITCODE -ne 0) { throw 'File status failed' }; if ($status.Count -gt 0) { $file } }); if ($files.Count -gt 0) { foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m "results: record P2.18 0.5B $scope"; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; }; Publish 'full' }
```

Validation: both exact GPU commands and both publication commands parsed on
PowerShell 7.4.6. Two independent native PowerShell processes with mock GPU/Git
commands verified: concurrent baselines, no public work before publication,
per-GPU sequential arm order, separate final publication, and worker cleanup.
This validates the terminal workflow on macOS, not a Windows/CUDA run.

Decision: compare final Spider EX, Hinton versus gold within each schedule,
AKAKA versus AKKAA within each objective, then the FL and centralized controls.
The summary includes paired exact McNemar tests. Centralized/FL match private
passes but have no BIRD exposure. Seed 0 is a screen; replicate a promising
contrast before making a general claim. Keep 1.5B results as historical
references, not evidence of a causal size-only comparison.
