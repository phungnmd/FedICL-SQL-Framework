# FedLS-SQL: run queue

## Status

Updated 2026-11-17 (Asia/Ho_Chi_Minh). Nothing is running. The code for
the DPO rounds from the base student and the read of the pairs is pushed
(code `c03bd693`); the server checkout is at the result commit `12456b56`
(code `083a6a52`) until step 1 below is run.

| GPU | State | Known from |
|---|---|---|
| 0 | Idle. The worker ended with the queue. | owner, 2026-11-17 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Update the server checkout and run the tests (about 5 min, estimate).
   Send back the last lines: the pytest summary (428 passed on the Mac),
   or the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv sync --extra dev; if ($LASTEXITCODE -ne 0) { throw 'uv sync failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. Start the worker on GPU 0. It skips the finished tasks and runs the
   read of the pairs and its publication (15 to 30 min, estimate). While
   `pairread/base_ddl_rows` runs, look once at the shared GPU memory of
   the card in Task Manager: it should stay near zero (the memory of this
   sampling setting is not measured yet). Send back the final `DONE queue`
   or `STOP queue` line, and the shared memory you saw.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `pairread/base_ddl_rows` | how many pairs the clients' questions give: the base student samples 10 SQL per question at temperature 1.0 on the 5 clients (prompt A), each sample is labelled by execution, and the questions are counted per client as all wrong, mixed and all correct. No training | 15 to 30 min (estimate) | queued |
| 2 | `pairread/publish` | commits and pushes the summary of the read | 1 min | queued |

Not queued yet: FedAvg SFT and the DPO rounds from the base student for
the same number of rounds, then local training and centralized SFT, on
the split `federated/alpha_0.1/k5`. They wait for the read (it gives the
pairs of round 1, and with them the time of a round) and for the owner's
choice of the number of rounds. Round 1 of the DPO rounds reuses the
samples of the read.

## Reference

All commands run from the `fedicl-sql` root on the server, as one
PowerShell line, and put temp files on drive D (`TEMP`, `TMP`, pytest
`--basetemp`); drive C is not used.

Read-only status of the queue:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

GPU work runs through one queue file, `fedicl-sql/queues/active.toml`:
every task (one command), what it needs first, in priority order. One
worker per GPU takes the first ready task and rereads the queue before
every task, so tasks pushed later run after a pull without a restart.
Ctrl+C stops the worker and its running task; the start command continues
where it stopped and skips finished work. A failed task stops the worker
with `STOP queue: <task> failed: <last error line>` and the log path
(`.queue_state/logs/`); send that line back.

On the server, `artifacts/` still holds the adapters, samples and pairs of
the earlier setup. They stay where they are; new runs write to new roots.
