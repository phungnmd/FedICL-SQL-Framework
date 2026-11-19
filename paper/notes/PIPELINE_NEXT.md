# FedLS-SQL: run queue

## Status

Updated 2026-11-19 20:50 (Asia/Ho_Chi_Minh). Spider test by total rounds
trained:

| Total rounds | FedAvg SFT | 3 SFT rounds then DPO (k = 3) | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) |
|---|---|---|---|---|
| 1 | 72.43 | | | 75.87 |
| 2 | 74.10 | | | 77.18 |
| 3 | 74.71 | | 77.46 | 77.69 |
| 4 | 74.71 | 77.97 | 78.20 | 78.02 |

Settled on Spider: the method is DPO + NLL with execution labels on the
model's own samples (3.3 to 3.5 above FedAvg SFT at 4 rounds; without
the NLL term 73.59; NLL on correct samples alone 75.87 against 77.46).
Not kept: nearest pairs, gold as chosen, gold inside the round,
wrong-result rejects first. The FedAvg SFT stage shows no gain on Spider
at k = 0, 2 or 3 (78.02, 78.20, 77.97 at 4 rounds); it is read next on
BIRD. BIRD dev, base student: 29.47, with 646 of 1,534 outputs failing
to execute (570 `no such column`), 1 output cut at 256 tokens and 3 rows
lost to the 30 s budget.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `bird/read` since 20:23, done between 22:00 and 23:30 (estimate); then the BIRD rounds. | `bird/zs` result `bfa497a8`, published 20:23 (inferred) |
| 1 | Stopped since 07:00, not started again. | the results since 06:31 came in the order one worker gives (inferred) |

## Run now

1. Start GPU 1 again (optional; it takes the next BIRD round while
   GPU 0 runs another). The server needs a pull first if
   no publication has run since 20:46 (the publish step merges
   `origin/main` itself). Add
   `--until HH:MM` after the GPU digit for a stop time:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   The same line with `--gpu 0` continues GPU 0 if it stops.

2. Send back, when they come:
   - the last lines the GPU 1 worker printed at 07:00 (the first run of
     `--until` on Windows);
   - for `bird/read`: the table of questions by kind per client, how
     long sampling and labelling took, and any line that names a
     timeout;
   - the EX line of each BIRD round and the peak reserved VRAM on the
     first updates of each client;
   - the first time two vLLM jobs overlap (an evaluation on one card while
     the other samples or evaluates): the peak reserved VRAM of each and
     whether either slows down;
   - a `STOP queue` line, if one comes (the BIRD tasks are the first
     training runs on BIRD in this setup).

3. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `bird/read`, `bird/publish_read` | on BIRD train at 5 clients: for how many questions does the base student have a correct SQL among 10 samples (Spider: 87.6%; all wrong 12%)? Decides whether DPO from the base student can stand without a gold path on a harder dataset | 1.5-3 h (estimate; labels with 4 workers under the 30 s budget are the unknown part) | running since 20:23 (inferred) |
| 2 | `bird_sft/round_1`, `bird_k0/round_1` | on BIRD at 1 round: FedAvg SFT against DPO + NLL from the base student (on Spider 72.43 against 75.87). Does DPO from the base student still lead where the base student is weaker (29.47 on BIRD dev)? | 3 h each (estimate) | queued |
| 3 | `bird_sft/round_2`, `bird_k0/round_2` | the same at 2 rounds (Spider: 74.10 against 77.18) | 3 h each (estimate) | queued |
| 4 | `bird_fixed/round_2` | on-policy rounds: round 2 on the round 1 pairs with the base student as reference, against `bird_k0/round_2` (re-sampled). On Spider at k = 2: 78.02 against 78.20 | 3 h (estimate; trains only) | queued |
| 5 | `refs/central_sft` | centralized SFT on the union of the 5 Spider clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 4 |

Expected with GPU 0 alone (estimates): row 1 between 22:00 and 23:30,
row 2 by about 05:30, row 3 by about 12:00, row 4 by about 15:00.

Not queued yet, decided on rows 1 and 2: the line with an SFT stage on
BIRD (DPO from a `bird_sft` round), and a gold path for the questions
without a correct sample (NLL on the gold SQL; the trainer part is not
written).

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Open for the owner:
whether the FedAvg SFT stage stays, on rows 1 to 3; whether on-policy
rounds are a part of the method, on row 4; round 2 of federated DPO as
published (no NLL, fixed pairs, fixed reference) for the baseline row,
from the start the method ends up with; on BIRD, the 350 golds that fail
(kept for FedAvg SFT as released).

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
