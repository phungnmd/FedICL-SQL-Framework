# FedLS-SQL: run queue

## Status

Updated 2026-11-17 20:45 (Asia/Ho_Chi_Minh). The worker on GPU 0 stopped
at 20:43 in FedAvg round 3, client 2, step 134 of 1542, with no error line
in the console tail; cause not known yet. Rounds 1 and 2 are published
(EX 72.43 and 74.10). Round 3 client 1 is trained and kept; client 2
starts again from step 0 on restart.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker stopped in `rounds/fedavg_sft`, round 3. | owner, 2026-11-17 20:43 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

0. Why the worker stopped (read-only, a few seconds). Send back the whole
   output: queue status, last 40 lines of the task log, `nvidia-smi`, and
   Windows errors of the last 2 hours.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; Get-Content .queue_state\logs\rounds\fedavg_sft.log -Tail 40; nvidia-smi; Get-WinEvent -FilterHashtable @{LogName='System','Application'; Level=1,2; StartTime=(Get-Date).AddHours(-2)} -MaxEvents 10 -ErrorAction SilentlyContinue | Format-List TimeCreated,ProviderName,Message }
   ```

   Then restart the worker with the command of step 3; it skips finished
   work and goes on with round 3.

Steps 1 and 2 run in a second PowerShell window, without the GPU
(`CUDA_VISIBLE_DEVICES` empty), while the worker keeps running. Skip them
if already done.

1. Pull and run the tests (about 5 min, estimate). Send back the pytest
   summary (447 passed on the Mac), or the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. Phase 0a: what the pairs of the base student's round 1 samples are
   made of, per client (CPU, a few minutes, estimate), then publish it.
   Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

3. Leave the worker running. After FedAvg stops it takes the DPO line
   (`dpo/after_fedavg`) by itself. Send back:
   - each `curve ... EX` line of FedAvg and of DPO;
   - in the first minutes of DPO round 1: the peak reserved VRAM of the
     training progress line and the shared GPU memory of the card in
     Task Manager (DPO with these prompts is not measured yet);
   - the time left that DPO round 1 prints once it trains;
   - a `STOP queue` line, if one comes.

   If the worker stops, the same command continues where it stopped:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `rounds/fedavg_sft` | FedAvg SFT from the base student on the 5 clients (`alpha_0.1/k5`), prompt A, one round at a time; every round evaluated on Spider test and published | about 2 h per round plus about 10 min of evaluation (measured round 1: 7,339 s + 206 s); 3 to 8 rounds | stopped in round 3 (rounds 1-2 done) |
| 2 | `dpo/after_fedavg` | phase 1: DPO + NLL rounds from the best FedAvg round (10 samples at T 1.0, 2 pairs per question, no pair from a database without rows), each round evaluated on Spider test and published | about 1.5-2.5 h per round (estimate); up to 6 rounds | queued |

How the rounds stop: a round is a gain when it beats the best round by
more than 0.5 EX point; a line stops after 2 rounds in a row without a
gain, or at 8 rounds (FedAvg) or 6 (DPO). The control of the DPO line is
FedAvg continued for the same number of rounds: FedAvg already holds 2
rounds after its best; if DPO runs longer, a curve that extends FedAvg is
queued then.

Not queued: phase 2 (the published federated DPO baseline, RFT, DPO from
the base student, I2) and phase 3 (BIRD, other splits, FedProx, FedNTD,
centralized and local rows, pre-training); `RESEARCH_STATE.md`, section
3.7.

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
