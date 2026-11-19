# FedLS-SQL: run queue

## Status

Updated 2026-11-19 16:15 (Asia/Ho_Chi_Minh). Spider test by total rounds
trained:

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) |
|---|---|---|---|
| 1 | 72.43 | | 75.87 |
| 2 | 74.10 | | 77.18 |
| 3 | 74.71 | 77.46 | 77.69 |
| 4 | 74.71 | 78.20 | 78.02 |

New since 14:40: k = 0 round 4 78.02, equal to the k = 2 line at 4
rounds (p 0.85): on Spider the FedAvg SFT stage shows no gain at 3 or 4
rounds. Earlier today: gold inside the round 76.67 against 75.87
(p 0.21), not kept; DPO without the NLL term 73.59 (the NLL term stays);
wrong-result rejects first in round 1 77.27, not kept. Being prepared on
the Mac, not queued: BIRD train as a second set of clients (prompt with
evidence, client split, evaluation on BIRD dev).

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `decide/wr_round2` since 15:29, done at about 17:00 (estimate), then `decide/k3`. | k = 0 round 4 evaluation `4215a7e1`, published 15:29 (inferred) |
| 1 | Stopped since 07:00, not started again. | the results since 06:31 came in the order one worker gives (inferred) |

## Run now

1. Start GPU 1 again (optional; it halves the wait for rows 2-4 of the
   table). Add
   `--until HH:MM` after the GPU digit for a stop time:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   The same line with `--gpu 0` continues GPU 0 if it stops.

2. Send back, when they come:
   - the last lines the GPU 1 worker printed at 07:00 (the first run of
     `--until` on Windows);
   - the EX line of `decide/wr_round2` and of `decide/k3`;
   - the first time two vLLM jobs overlap (an evaluation on one card while
     the other samples or evaluates): the peak reserved VRAM of each and
     whether either slows down;
   - a `STOP queue` line, if one comes (`decide/wr_round2` is the first
     queued use of `--continue-from`).

3. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `decide/wr_round2/*` | DPO round 2 after DPO round 1 from FedAvg round 2 (not trained again), on the samples of its round 2, rejected side from wrong results first: does the rule lower the wrong results once the execution errors are low? Read against DPO round 2 (78.20; execution errors 84, wrong results 384) | 1.5 h (estimate; 3,354 pairs) | running since 15:29 (inferred) |
| 2 | `decide/k3/*` | DPO round 1 from FedAvg round 3 (k = 3): total 4 rounds, as DPO round 2 from k = 2 (78.20), k = 0 round 4 (78.02) and FedAvg round 4 (74.71); step 1 of row 4 | 3 h (estimate) | queued |
| 3 | `refs/central_sft` | centralized SFT on the union of the 5 clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 2 |
| 4 | `dpo/after_fedavg` | DPO + NLL rounds from FedAvg round 3 until the rule stops them | 2.5-3 h per round (estimate); up to 6 rounds | queued |

Expected with GPU 0 alone (estimates): row 1 at about 17:00, row 2 at
about 20:00.

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Open for the owner:
whether the FedAvg SFT stage stays (no gain on Spider at 3 or 4 rounds;
the read of the base student on BIRD comes first); if it goes, row 4
starts from the k = 0 line instead of FedAvg round 3 and row 2 is only a
row of the k table; round 2 of federated DPO as published (no NLL, fixed
pairs, fixed reference) from the `decide/nonll` root, about 2.5 h, for
the baseline row.

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
