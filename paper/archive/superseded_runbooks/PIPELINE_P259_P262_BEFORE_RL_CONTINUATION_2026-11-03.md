# P2.59-P2.62 queue before the RL continuation fixes

Historical commands only. Replaced by the active continuation section in PIPELINE_NEXT.md.
P2.61 E1 and P2.60 SQL through round 2 were published; P2.62 lanes were running.

## P2.62: RL on Spider straight from the BIRD SFT (active)

Code: `scripts/run_p262_rl_from_bird.py` (nested `cf408e1`), seed 0, Spider dev. Drops `cot2`: from the best P2.60
`cot1` epoch (`cot1_e4` 60.64), DPO + NLL rounds on Spider train with the P2.60 settings and question sets (K=8
samples without gold, gold as execution oracle, 1,200 new questions per round, at most 7 rounds, stop after two
gains in a row below 1 point). Route `s1` is the same from `sql1_e2` without CoT. Marks: `sql2_e1` 73.60 and the
P2.60 SQL RL ceiling once it runs (LAB_LOG 2026-11-03). About 2.5-4 GPU-h per CoT round on one GPU.

1. GPU 1, while the P2.60 SQL lane keeps GPU 0. This pull admits only new files and P2.61, which no lane runs; it also prints the count of
   teacher rows with both a correct and a wrong output (the input of direction 3), then starts route `c1`:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/run_p26[12]_(gold_signal|rl_from_bird)\.py|tests/test_p262_rl_from_bird\.py|docs/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p262_rl_from_bird.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p262_rl_from_bird --phase pairs; if ($LASTEXITCODE -ne 0) { throw 'Pair count failed' }; uv run --no-sync python -m scripts.run_p262_rl_from_bird --phase lane --route c1; if ($LASTEXITCODE -ne 0) { throw 'P2.62 lane failed' } }
```

2. Optional, when `s1` (step 3) has finished: GPU 0 joins route `c1` (the sampling shards split across GPUs):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p262_rl_from_bird --phase lane --route c1; if ($LASTEXITCODE -ne 0) { throw 'P2.62 lane failed' } }
```

3. Now on GPU 0 (P2.60 SQL lane finished, published `d7c3ccb`): the same route without CoT, the matched control of `c1`:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p262_rl_from_bird --phase lane --route s1; if ($LASTEXITCODE -ne 0) { throw 'P2.62 lane failed' } }
```

4. Read-only, any time:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.run_p262_rl_from_bird --phase status; if ($LASTEXITCODE -ne 0) { throw 'Read failed' } }
```

5. Publish when no P2.62 task is running:

```powershell
& { $ErrorActionPreference='Stop'; $exp='p262_rl_from_bird'; $mod=$exp; $msg="results: record the $exp seed 0 rounds"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(diagnose_p260_cot|run_p261_gold_signal|run_p262_rl_from_bird)\.py|tests/test_(p260_cot_ceiling|p261_gold_signal|p262_rl_from_bird)\.py|docs/.+|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m "scripts.run_$mod" --phase files | Where-Object { $_ }); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

## P2.61: what the Spider stage of the CoT route needs (E1 done, E2-E4 not queued)

Code: `scripts/run_p261_gold_signal.py`, seed 0, Spider dev. P2.60 `cot2` gains nothing on Spider and 77.33% of its
targets repeat its parent's greedy output (LAB_LOG 2026-11-03), so the CoT lane stops and the SQL lane continues.
From `cot1_e4`, read at E1: `cot2g` (`cot2` rows and reasoning, gold SQL) against `cot2_e1` 60.35 and `sql2_e1` 73.60;
`sqlc` (SQL-only gold, all rows) against `sql2_e1`. About 2-2.5 GPU-h per arm.

1. Stop both P2.60 lanes (Ctrl+C), then start the controls on GPU 1. This pull admits only new or unused files:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(diagnose_p260_cot|run_p261_gold_signal)\.py|tests/test_(p260_cot_ceiling|p261_gold_signal)\.py|docs/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p261_gold_signal.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p261_gold_signal --phase lane --epochs 1; if ($LASTEXITCODE -ne 0) { throw 'P2.61 lane failed' } }
```

2. When step 1 has passed its tests, continue only the SQL route on GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase lane --stage sql; if ($LASTEXITCODE -ne 0) { throw 'P2.60 SQL lane failed' } }
```

3. Read-only, any time:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.run_p261_gold_signal --phase status; if ($LASTEXITCODE -ne 0) { throw 'Read failed' } }
```

4. Publish E1 when its lane has stopped:

```powershell
& { $ErrorActionPreference='Stop'; $exp='p261_gold_signal'; $mod=$exp; $msg="results: record the $exp seed 0 E1 controls"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(diagnose_p260_cot|run_p261_gold_signal|run_p262_rl_from_bird)\.py|tests/test_(p260_cot_ceiling|p261_gold_signal|p262_rl_from_bird)\.py|docs/.+|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m "scripts.run_$mod" --phase files | Where-Object { $_ }); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

## P2.60: does CoT + RL reach a higher ceiling than SQL (BIRD, ready to run)

Code: `scripts/run_p260_cot_ceiling.py`, seed 0, Spider dev. Owner, 2026-11-01/02: the question is whether
CoT + RL beats SQL-only SFT, comparing ceilings and not equal steps. The teacher never sees gold SQL.

| Step | What | Size | Stop |
|---|---|---|---|
| `pilot`, `pool` | teacher 7B writes CoT on BIRD with evidence: greedy, then K=2 on unsolved rows; keeps rows matching gold on execution | 300 then 1,700 rows, about 1,000 kept expected | none |
| `cot1_e*` | student SFT on the kept rows | at most 4 epochs | first epoch whose Spider dev EX does not rise |
| `cs*` | best `cot1` epoch solves Spider train without gold: greedy, then K=4 on failures | 8,659 rows | none |
| `cot2_e*` | student SFT on its correct rows | at most 4 epochs | as `cot1` |
| `cot_rl1-7` | DPO + NLL, 1,200 new questions per round until Spider train is used up | at most 7 rounds | two gains in a row below 1 point |

Estimated 45-85 GPU-h for the route (teacher about 20, `cs` 6-8, `cot2` up to 12, each RL round 2-4); the
first batches and receipts replace these numbers. Earlier SQL numbers come from another pool or stop at one RL round, so none is a mark for this route (owner,
2026-11-02); `--stage sql` gives the matched SQL ceiling. Adding BIRD into RL and more teacher rows are later options.

1. Pilot on GPU 0, after the template follow-up has stopped, because this pull changes the trainer that lane
   imports (about 3-4 GPU-h):

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(fedicl_sql/training/lora_trainer\.py|scripts/(diagnose_p259_writers|run_p260_cot_ceiling)\.py|tests/test_(p259_cot_then_rl|p260_cot_ceiling|trainer_epoch_resume)\.py|docs/.+|.+\.md|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_p260_cot_ceiling.py tests/test_trainer_epoch_resume.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase lane --stage pilot; if ($LASTEXITCODE -ne 0) { throw 'P2.60 pilot lane failed' } }
```

2. Optional, the same pilot on GPU 1:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase lane --stage pilot; if ($LASTEXITCODE -ne 0) { throw 'P2.60 lane failed' } }
```

3. Read-only, any time:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase status; if ($LASTEXITCODE -ne 0) { throw 'Read failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase preview; if ($LASTEXITCODE -ne 0) { throw 'Read failed' } }
```

4. Read the pilot, then the full route, one command per GPU. Tasks already done are skipped:

```powershell
& { $ErrorActionPreference='Stop'; $gpu='0'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase lane --stage all; if ($LASTEXITCODE -ne 0) { throw 'P2.60 lane failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $gpu='1'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES=$gpu; uv run --no-sync python -m scripts.run_p260_cot_ceiling --phase lane --stage all; if ($LASTEXITCODE -ne 0) { throw 'P2.60 lane failed' } }
```

Diagnosis of the CoT gap, read-only, safe while lanes run:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git fetch origin main; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git show origin/main:scripts/diagnose_p260_cot.py | uv run --no-sync python -; if ($LASTEXITCODE -ne 0) { throw 'Diagnosis failed' } }
```

5. Publish when the lanes have stopped, or at any point when no task is running:

```powershell
& { $ErrorActionPreference='Stop'; $exp='p260_cot_ceiling_bird'; $mod='p260_cot_ceiling'; $msg="results: record the $exp seed 0 teacher pool, SFT stages and SQL rounds"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(scripts/(diagnose_p260_cot|run_p261_gold_signal|run_p262_rl_from_bird)\.py|tests/test_(p260_cot_ceiling|p261_gold_signal|p262_rl_from_bird)\.py|docs/.+|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m "scripts.run_$mod" --phase files | Where-Object { $_ }); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```


## P2.59 follow-up: template through SFT then RL (recommended, about 4 GPU-h)

P2.59 is published (nested `9456e09`; runbook in `paper/archive/completed_runbooks/PIPELINE_P259_2026-11-01.md`).
Template against SQL on the same route is the cheapest read of whether a stepwise format can pass `g3d`,
before the teacher pool is paid for. Needs no new code. GPU 1, while the P2.60 pilot runs on GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; foreach ($task in @('tp2','eval_tp2','tp3_samp0','tp3_samp1','tp3_samp2','tp3_samp3','tp3','eval_tp3')) { uv run --no-sync python -m scripts.run_p259_cot_then_rl --phase task --task $task; if ($LASTEXITCODE -ne 0) { throw "$task failed" } } }
```

Publish when the window has finished (`files` cannot detect these tasks):

```powershell
& { $ErrorActionPreference='Stop'; $exp='p259_cot_then_rl'; $msg="results: record the $exp seed 0 template route B"; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; git diff --quiet HEAD; if ($LASTEXITCODE -ne 0) { throw 'Tracked changes need review' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; $incoming=@(git diff --name-only HEAD...origin/main); if ($LASTEXITCODE -ne 0) { throw 'Diff failed' }; $bad=@($incoming | Where-Object { $_ -notmatch '^(fedicl_sql/training/lora_trainer\.py|scripts/(diagnose_p259_writers|run_p260_cot_ceiling)\.py|tests/test_(p259_cot_then_rl|p260_cot_ceiling|trainer_epoch_resume)\.py|experiments/(federated|eval_arms|client_train)/results/.+|audits/.+|.+\.md)$' }); if ($bad.Count -ne 0) { throw "Unexpected incoming files: $bad" }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $files=@(uv run --no-sync python -m "scripts.run_$exp" --phase files); if ($LASTEXITCODE -ne 0) { throw 'Publication validation failed' }; if ($files.Count -eq 0) { throw 'Nothing to publish' }; foreach ($file in $files) { git add -- $file; if ($LASTEXITCODE -ne 0) { throw 'Staging failed' } }; $actual=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0) { throw 'Staged-set check failed' }; if (@(Compare-Object ($files | Sort-Object -Unique) ($actual | Sort-Object -Unique)).Count -ne 0) { throw 'Staged set differs from allowlist' }; git commit -m $msg; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```
