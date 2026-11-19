# FedLS-SQL: run queue

## Status

Updated 2026-11-19 19:20 (Asia/Ho_Chi_Minh). Spider test by total rounds
trained:

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) |
|---|---|---|---|
| 1 | 72.43 | | 75.87 |
| 2 | 74.10 | | 77.18 |
| 3 | 74.71 | 77.46 | 77.69 |
| 4 | 74.71 | 78.20 | 78.02 |

New since 16:15: wrong-result rejects in round 2 (`decide/wr_round2`)
77.69 against 78.20 (p 0.14), 12 fewer wrong results and 23 more
execution errors, not kept. BIRD train as a second set of clients is set
up and checked (prompt with evidence against the Qwen2.5-Coder code,
client split, labels, evaluation on BIRD dev); its first two runs are
queued (`4045d3af`), no training in either. Earlier today: k = 0 equals
the k = 2 line at 3 and 4 rounds; gold inside the round not kept; DPO
without the NLL term 73.59 (the NLL term stays).

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `decide/k3/round_1` since 17:03, done at about 20:00 (estimate); then its evaluation, `bird/zs`, `bird/read`. | `decide/wr_round2` evaluation `06e81fdf`, published 17:03 (inferred) |
| 1 | Stopped since 07:00, not started again. | the results since 06:31 came in the order one worker gives (inferred) |

## Run now

1. Start GPU 1 again (optional; it takes `bird/zs` and `bird/read` at
   once instead of after `decide/k3`). The server needs a pull first if
   no publication has run since 19:10 (the publish step merges
   `origin/main` itself). Add
   `--until HH:MM` after the GPU digit for a stop time:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   The same line with `--gpu 0` continues GPU 0 if it stops.

2. Send back, when they come:
   - the last lines the GPU 1 worker printed at 07:00 (the first run of
     `--until` on Windows);
   - the EX line of `decide/k3` and of `bird/zs`, and for `bird/read` the
     table of questions by kind per client, how long sampling and
     labelling took, and any line that names a timeout;
   - the first time two vLLM jobs overlap (an evaluation on one card while
     the other samples or evaluates): the peak reserved VRAM of each and
     whether either slows down;
   - a `STOP queue` line, if one comes (the BIRD tasks are the first runs
     on BIRD in this setup: a missing database under
     `data/raw/bird/train/train_databases/` would stop `bird/read` at
     its start).

3. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `decide/k3/*` | DPO round 1 from FedAvg round 3 (k = 3): total 4 rounds, as DPO round 2 from k = 2 (78.20), k = 0 round 4 (78.02) and FedAvg round 4 (74.71); step 1 of row 5 | 3 h (estimate) | running since 17:03 (inferred) |
| 2 | `bird/zs`, `bird/publish_zs` | base student on BIRD dev (1,534 rows, evidence, `ddl`, greedy): the level before training, and how many outputs are cut at 256 tokens or hit the 30 s budget | 15 min (estimate) | queued |
| 3 | `bird/read`, `bird/publish_read` | on BIRD train at 5 clients: for how many questions does the base student have a correct SQL among 10 samples (Spider: 87.6%; all wrong 12%)? Decides whether DPO from the base student can stand without a gold path on a harder dataset | 1.5-3 h (estimate; labels with 4 workers under the 30 s budget are the unknown part) | queued |
| 4 | `refs/central_sft` | centralized SFT on the union of the 5 Spider clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 3 |
| 5 | `dpo/after_fedavg` | DPO + NLL rounds from FedAvg round 3 until the rule stops them | 2.5-3 h per round (estimate); up to 6 rounds | queued |

Expected with GPU 0 alone (estimates): row 1 at about 20:15 with its
evaluation, row 2 at about 20:30, row 3 between 22:00 and 23:30.

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Open for the owner:
whether the FedAvg SFT stage stays (no gain on Spider at 3 or 4 rounds;
the read of the base student on BIRD, row 3, comes first); if it goes,
row 5 starts from the k = 0 line instead of FedAvg round 3 and row 1 is
only a row of the k table; round 2 of federated DPO as published (no NLL, fixed
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
