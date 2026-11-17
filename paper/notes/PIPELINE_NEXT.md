# FedLS-SQL: run queue

## Status

Updated 2026-11-17 (Asia/Ho_Chi_Minh). Nothing is running. Pushed (code
`66b2c01a`): the queue now holds the read of the pairs, then FedAvg SFT
and the DPO rounds from the base student one round at a time, then the
reference rows behind a condition. The server checkout is at an earlier
code until step 1 is run.

| GPU | State | Known from |
|---|---|---|
| 0 | Idle. The worker ended with the queue. | owner, 2026-11-17 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Update the server checkout and run the tests (about 5 min, estimate).
   Send back the last line: the pytest summary (442 passed on the Mac), or
   the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv sync --extra dev; if ($LASTEXITCODE -ne 0) { throw 'uv sync failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. Start the worker on GPU 0 and leave it running. It runs the read of
   the pairs (15 to 30 min, estimate), then the rounds. Send back:
   - after the read: the line `end pairread/publish`;
   - in the first minutes of the first FedAvg round and of the first DPO
     round: the peak reserved VRAM of the progress line and the shared GPU
     memory of the card in Task Manager (it should stay near zero; neither
     path is measured yet with this prompt);
   - the time left that the first DPO round prints once it trains;
   - a `STOP queue` line, if one comes.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   Ctrl+C stops the worker and its task; the same command continues where
   it stopped.

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `pairread/base_ddl_rows`, `pairread/publish` | how many pairs the clients' questions give: 10 SQL per question at temperature 1.0 from the base student on the 5 clients, labelled by execution; questions counted per client as all wrong, mixed, all correct. No training | 15 to 30 min (estimate) | queued |
| 2 | `rounds/sft_vs_dpo` | the comparison that decides the story: FedAvg SFT and federated DPO from the base student, one round each in turn (SFT round 1, DPO round 1, SFT round 2, ...). Every round is evaluated on Spider test and published, so each row of the two lines appears as it is done | about 2 h per round of either line (estimate, not measured); 4 to 16 rounds in all | queued |
| 3 | `refs/central_local` | centralized SFT and local SFT of each client, one epoch at a time. Runs only if the best DPO round is at least 2.0 EX points above the best FedAvg SFT round; otherwise it is skipped and the worker ends | about 2 h per epoch of the centralized line, and 2 h for one epoch of the five local lines together (estimate) | queued, conditional |

How the rounds stop: a round is a gain when it beats the best round of its
line by more than 0.5 EX point; a line stops after 2 rounds in a row
without a gain, or at 8 rounds. The line that stops first follows the
other one, so both are read over the same rounds.

The DPO rounds use 10 pairs per question (CodeLutra). If the first DPO
round shows a time far above 2 h, stop the worker and send the line: a
smaller number of pairs needs a new output root.

Not queued yet: the three candidate changes inside the DPO rounds, the
pre-training at the server, the other splits. They wait for the two lines.

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
