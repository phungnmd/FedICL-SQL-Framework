# FedLS-SQL: run queue

## Status

Updated 2026-11-17 (Asia/Ho_Chi_Minh). Pushed (code `407a7ad7`): the
queue now runs the FedAvg SFT rounds alone. The read of the pairs is done
and published (`1704b03b`). The worker on the server still runs the old
code and loops on `queue queues/active.toml unreadable (... unknown keys
['when'])`.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker looping on the unreadable queue; no task running. | owner, 2026-11-17 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Stop the looping worker with Ctrl+C in its window.

2. Update the server checkout and run the tests (about 5 min, estimate).
   Send back the last line: the pytest summary (442 passed on the Mac), or
   the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv sync --extra dev; if ($LASTEXITCODE -ne 0) { throw 'uv sync failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

3. Start the worker on GPU 0 and leave it running. It runs the FedAvg SFT
   rounds. Send back:
   - in the first minutes of round 1: the peak reserved VRAM of the
     progress line and the shared GPU memory of the card in Task Manager
     (it should stay near zero; not measured yet with this prompt);
   - the time left that round 1 prints once it trains;
   - each `curve ... EX` line after an evaluation;
   - a `STOP queue` line, if one comes.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   Ctrl+C stops the worker and its task; the same command continues where
   it stopped.

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `rounds/fedavg_sft` | FedAvg SFT from the base student on the 5 clients (`alpha_0.1/k5`), prompt A, one round at a time; every round evaluated on Spider test and published | about 2 h per round plus about 10 min of evaluation (estimate); 3 to 8 rounds | queued |

How the rounds stop: a round is a gain when it beats the best round by
more than 0.5 EX point; the line stops after 2 rounds in a row without a
gain, or at 8 rounds.

Not queued: the federated DPO rounds (the pair rule for questions with an
empty gold result and the number of pairs per question are open, see
`LAB_LOG.md`), the centralized and local reference rows, the pre-training
at the server, the other splits.

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
every task, so tasks pushed later run after a pull without a restart. A
change to the queue format (a new key) needs a worker restart after the
pull. Ctrl+C stops the worker and its running task; the start command
continues where it stopped and skips finished work. A failed task stops
the worker with `STOP queue: <task> failed: <last error line>` and the log
path (`.queue_state/logs/`); send that line back.

On the server, `artifacts/` still holds the adapters, samples and pairs of
the earlier setup. They stay where they are; new runs write to new roots.
