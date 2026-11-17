# FedLS-SQL: run queue

## Status

Updated 2026-11-17 (Asia/Ho_Chi_Minh), after the clean reset. The queue
holds the worker selftest only; nothing is running.

| GPU | State | Known from |
|---|---|---|
| 0 | Idle. The worker was stopped by the owner during `synvc_s0/sft_plain` of the earlier setup. | owner, 2026-11-17 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

The server checkout is still at the code of the earlier setup
(`aa17258c`). The cleaned code (package `fedls_sql`) is not pushed yet; the
update command comes here when it is.

## Run now

Nothing to run on the server.

Next moments the owner is needed:

- Choose the prompt (three candidates in `RESEARCH_STATE.md`, section 4).
- After the cleaned code is pushed: update the server checkout, run the
  tests and the worker selftest (commands will be listed here).

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| | none | | | |

## Reference

All commands run from the `fedicl-sql` root on the server, as one
PowerShell line, and put temp files on drive D (`TEMP`, `TMP`, pytest
`--basetemp`); drive C is not used.

Read-only status of the queue:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

Worker on GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
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
