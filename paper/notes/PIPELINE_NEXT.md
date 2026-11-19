# FedLS-SQL: run queue

## Status

Updated 2026-11-19 19:50 (Asia/Ho_Chi_Minh). Spider test by total rounds
trained:

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) |
|---|---|---|---|
| 1 | 72.43 | | 75.87 |
| 2 | 74.10 | | 77.18 |
| 3 | 74.71 | 77.46 | 77.69 |
| 4 | 74.71 | 78.20 | 78.02 |

Settled on Spider: the method is DPO + NLL with execution labels on the
model's own samples (3.3 to 3.5 above FedAvg SFT at 4 rounds; without
the NLL term 73.59; NLL on correct samples alone 75.87 against 77.46).
Not kept: nearest pairs, gold as chosen, gold inside the round,
wrong-result rejects first (round 2: 77.69 against 78.20, p 0.14). Open:
the FedAvg SFT stage (no gain on Spider at 3 and 4 rounds), read next on
BIRD, where the base student may have no correct sample for many more
questions. BIRD train as a second set of clients is set up and checked;
its runs are queued (`186aaf58`). The long DPO line from FedAvg round 3
is dropped.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `decide/k3/round_1` since 17:03, done at about 20:00 (estimate); then its evaluation, `bird/zs`, `bird/read`, the BIRD rounds. | `decide/wr_round2` evaluation `06e81fdf`, published 17:03 (inferred) |
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
   - the EX line of `decide/k3`, of `bird/zs` and of each BIRD round, the
     peak reserved VRAM on the first updates of each client in the BIRD
     rounds, and for `bird/read` the
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
| 4 | `bird_sft/round_1`, `bird_k0/round_1` | on BIRD at 1 round: FedAvg SFT against DPO + NLL from the base student (on Spider 72.43 against 75.87). Does DPO from the base student still lead where the base student is weaker? | 3 h each (estimate) | queued |
| 5 | `bird_sft/round_2`, `bird_k0/round_2` | the same at 2 rounds (Spider: 74.10 against 77.18) | 3 h each (estimate) | queued |
| 6 | `refs/central_sft` | centralized SFT on the union of the 5 Spider clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 5 |

Expected with GPU 0 alone (estimates): row 1 at about 20:15 with its
evaluation, row 2 at about 20:30, row 3 between 22:00 and 23:30, row 4
by about 05:30, row 5 by about 12:00.

Not queued yet, decided on rows 3 and 4: the line with an SFT stage on
BIRD (DPO from a `bird_sft` round), and a gold path for the questions
without a correct sample (NLL on the gold SQL; the trainer part is not
written).

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Open for the owner:
whether the FedAvg SFT stage stays, on rows 3 to 5; whether on-policy
rounds are a part of the method (at round 2 on Spider fixed pairs with
the NLL term give the same EX, 78.02 against 78.20); round 2 of
federated DPO as published (no NLL, fixed pairs, fixed reference) for
the baseline row, from the start the method ends up with; on BIRD, the
350 golds that fail (kept for FedAvg SFT as released) and the 256-token
limit (read on row 2).

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
