# FedLS-SQL: run queue

## Status

Updated 2026-11-17 (Asia/Ho_Chi_Minh). Nothing is running. The cleaned
code with the new prompt and the rebuilt client splits is pushed (code
`4760352b`); the server checkout is still at the earlier code (`aa17258c`)
until step 1 below is run.

| GPU | State | Known from |
|---|---|---|
| 0 | Idle. The worker was stopped by the owner. | owner, 2026-11-17 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Update the server checkout and run the tests (about 5 min, estimate).
   The worker must be stopped. The pull removes the result rows and audit
   files of the earlier setup from the working tree and the earlier client splits (5,704 files; they
   stay in Git at the tag `archive/pre-reset-2026-11-17`) and brings the
   new splits; nothing under `artifacts/` is touched. The server copies of
   27 tracked files of one earlier result row (`p229_h_plain`) differ from
   Git and stopped the first try; the command lists them and puts them in
   a stash (kept, `git stash list`) before the pull. Send back the lines
   up to the stash line and the last lines: the pytest summary (415 passed
   on the Mac), or the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git status --short --untracked-files=no; git diff --shortstat; git diff --ignore-cr-at-eol --shortstat; git stash push -m 'server copies of tracked files before the 2026-11-17 reset'; if ($LASTEXITCODE -ne 0) { throw 'Stash failed' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv sync --extra dev; if ($LASTEXITCODE -ne 0) { throw 'uv sync failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. Start the worker on GPU 0. It runs the selftest (about 1 min), then
   the two evaluations and their publication (about 25 min in all,
   estimate). Send back the final `DONE queue` or `STOP queue` line.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

If an environment variable of the old name is set on the server
(`FEDICL_TMP`, `FEDICL_VLLM_PYTHON`), it is now `FEDLS_TMP`,
`FEDLS_VLLM_PYTHON`. Neither is needed with the default paths.

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `selftest/*` | the worker and the card after the update | 1 min | queued |
| 2 | `prompt/zs_ddl_rows` | the base model with no training on Spider test, prompt A (`CREATE TABLE` + 3 example rows); checks prompt and decoding | 10 min (estimate) | queued |
| 3 | `prompt/zs_ddl_values` | the same with prompt B (`CREATE TABLE` + example values per column) | 10 min (estimate) | queued |
| 4 | `prompt/publish` | commits and pushes the two result rows | 1 min | queued |

Not queued yet: local training, FedAvg SFT, centralized SFT and the DPO
rounds on the new prompt and the new split
(`federated/alpha_0.1/k5`). They wait for the two rows above and for the
owner's choice of the training settings.

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
