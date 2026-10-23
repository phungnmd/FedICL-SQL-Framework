# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). P2.20, P2.25 and P2.26 are
complete; their [commands](../archive/completed_runbooks/PIPELINE_P220_P225_P226_2026-10-10.md)
are history. Keep all P2.18-P2.26 adapters, receipts, caches and results.

State 2026-10-23: P2.27, P2.28, P2.29, P2.36 published; P2.37
`hinton_k2aaa`, `gold_k2aaa`, `central_mix`, `local`, and P2.38, the P2.39
pilot, P2.40 and P2.42 are published; P2.43 `hinton_k2aaa_rev` K2 and A1 are
published. P2.43 `hinton_k2aaa_rev` reached A3 (evaluated, not published).
P2.44 `self_k2aaa` complete on GPU 0 (2026-10-24, not published). Running:
GPU 1 `gold_k2aaa_rev` to A3, then `fl_bird`. Next on GPU 0: P2.43
`central_bird`. Publish P2.43 and P2.44 when no lane runs. Local nested commit
`1384045` (KD headroom audit, a new script) is not pushed: the P2.44 step 1
and publication pull allowlists reject it. Push it after the last P2.43 and
P2.44 publications. No seed 1-2 or Spider test run
until the method is fixed (LAB_LOG 2026-10-23). Findings and open questions are
in [RESEARCH_STATE.md](RESEARCH_STATE.md).

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
& { $ErrorActionPreference='Stop'; $exp='p244_self_teacher'; $n='244'; $msg='results: record P2.44 self-teacher control'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
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
& { $ErrorActionPreference='Stop'; $exp='p243_reverse_roles'; $n='243'; $msg='results: record P2.43 reverse roles endpoints'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
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
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p238_virtual_teacher --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p238_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.38 virtual-teacher control'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p238_virtual_teacher_s0/summary.md }
```

5. P2.39 publish (publishes every evaluated endpoint, so the pilot's A1
   alone), after P2.40 step 1 has pulled the code (before that, the
   incoming-code check refuses):

```powershell
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p239_frozen_a --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p239_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.39 frozen-A rounds'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p239_frozen_a_s0/summary.md }
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
& { $ErrorActionPreference='Stop'; $exp='p240_taid'; $n='240'; $msg='results: record P2.40 TAID K2AAA'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Incoming code changes a running lane uses: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m "scripts.run_$exp" --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m "scripts.list_p${n}_publication"); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content "audits/protocol_v2/${exp}_s0/summary.md" }
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
& { $ErrorActionPreference='Stop'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming code: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync python -m scripts.run_p237_phase_e --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'Analysis failed' }; $files=@(uv run --no-sync python -m scripts.list_p237_publication); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m 'results: record P2.37 phase E baselines'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' }; Get-Content audits/protocol_v2/p237_phase_e_s0/summary.md }
```

## Next

After P2.37: read the phase E table, then fix the paper story in a dated
LAB_LOG entry (claims, comparators, test, wording per outcome) before seeds
1-2 or Spider test.

On hold until the paper story is fixed: P2.31 (seeds 1 and 2), P2.35 (K-first
over seeds 0-2), Spider test evaluations, P2.32 (alpha 0.5).
