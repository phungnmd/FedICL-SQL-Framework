# FedLS-SQL: run queue

## Status

Updated 2026-11-17 (Asia/Ho_Chi_Minh). Nothing is running and the queue
is empty: the base model on Spider test is done and published (results
`12456b56`; EX 68.05 with prompt A, 67.49 with prompt B). The server
checkout has the code `083a6a52` (known from the published result rows).

| GPU | State | Known from |
|---|---|---|
| 0 | Idle. The worker ended with the queue. | owner, 2026-11-17 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

Nothing to run. The next step is the read of the pairs without training
(10 samples per question on each client, from the base student); its
code is not pushed yet.

## Running and queued

Nothing queued.

Not queued yet: the read of the pairs, then FedAvg SFT and the DPO rounds
from the base student for the same number of rounds, then local training
and centralized SFT, on the split `federated/alpha_0.1/k5`. The training
rows wait for the owner's choice of the training settings.

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
