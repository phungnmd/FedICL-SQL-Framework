# FedLS-SQL: run queue

## Status

Updated 2026-11-20 00:40 (Asia/Ho_Chi_Minh). Spider test by total rounds
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
lost to the 30 s budget. Followed now (owner): the k = 0 line with gold
where the samples give no correct side (round 1: 76.67 against 75.87),
to round 2 on Spider and to round 1 on BIRD. BIRD clients, 10 samples
of the base student per question: a correct SQL for 52.4% of the 9,428
questions (Spider 87.6%), all wrong 41.9% (Spider 12%), gold fails 5.7%
(350 SQL errors, 184 golds on the 30 s budget); 9,566 pairs.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `bird/read` published 23:42; then the first task not started (`k0_gold/round_2` unless GPU 1 has it). | result `55b883c9`, published 23:42 (inferred) |
| 1 | Not known: stopped since 07:00 unless started with step 1. | no result yet that only a second worker would give |

## Run now

1. Start GPU 1 now: it takes `k0_gold/round_2` (Spider, about 4 h,
   estimate) while GPU 0 goes on with BIRD. Without it GPU 0 runs that
   round first and the BIRD rounds move back by 4 h. The
   line pulls the queue first (fast-forward only, safe while GPU 0
   runs). Skip this step if GPU 1 already runs. Add `--until HH:MM`
   after the GPU digit for a stop time:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   The same line with `--gpu 0` continues GPU 0 if it stops.

2. Send back, when they come:
   - the last lines the GPU 1 worker printed at 07:00 (the first run of
     `--until` on Windows);
   - the EX line of `k0_gold/round_2` and of each BIRD round, and the
     peak reserved VRAM on the first updates of each client;
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

4. Any time, CPU only: the 184 BIRD train golds that met the 30 s
   budget in `bird/read`, each run once alone and stopped at 60 s (at
   most 1 min per gold, 1 to 3 h, estimate; rerun continues). It says
   whether they are slow golds or the effect of 4 labels running at
   once. Send back the last table (golds under 15 s, 15 to 30 s, over
   30 s).

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; $a='audits/protocol_v2/fedpref_bird_base_p2_ddl_alpha01_s0'; $s='processed_data/protocol_v2/BIRD/original_train9428_dev1534/federated/alpha_0.1/k5'; uv run --no-sync python -m scripts.label_timeouts --audit $a --round 1 --policy base --retime --split-dir $s; if ($LASTEXITCODE -ne 0) { throw 'Retime failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: BIRD train golds that met the 30 s budget, timed alone' --paths "$a/pair_read/gold_retime_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

5. Any time, CPU only (under a minute): the wall times of every task
   finished since 2026-11-17, read from the worker's logs into
   `audits/protocol_v2/run_times/`, one file per task, then published.
   It is the first run of this script on real logs: send back all it
   prints. Run it again whenever more tasks have finished; it adds
   their files and leaves the published ones alone.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.log_times; if ($LASTEXITCODE -ne 0) { throw 'log_times failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: wall times of the finished queue tasks, read from their logs' --paths audits/protocol_v2/run_times; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `k0_gold/round_2` | Spider: does the k = 0 line with gold (all-wrong questions, databases without rows) end higher than the line without? Round 2 against k = 0 round 2 (77.18; execution errors 92, wrong results 398); rounds 3 and 4 follow if it still rises | 4 h (estimate) | first in the queue since 23:42; running if a worker is up |
| 2 | `bird_sft/round_1`, `bird_k0/round_1` | on BIRD at 1 round: FedAvg SFT against DPO + NLL from the base student (on Spider 72.43 against 75.87). Does DPO from the base student still lead where it has pairs for half of the questions only (4,783 of 9,428; base student 29.47 on BIRD dev)? | 3 h each (estimate; `bird_k0/round_1` trains on the read's 9,566 pairs and samples nothing) | queued |
| 3 | `bird_k0_gold/round_1` | BIRD round 1 with gold as chosen for the 3,955 all-wrong questions, on the same samples: against row 2 | 4-6 h (estimate; up to 7,910 more pairs) | queued |
| 4 | `bird_sft/round_2`, `bird_k0/round_2` | the same as row 2 at 2 rounds (Spider: 74.10 against 77.18) | 3 h and 6 h (estimate; the DPO round samples and labels again, 3 h 19 min in the read) | queued |
| 5 | `bird_fixed/round_2` | on-policy rounds: round 2 on the round 1 pairs with the base student as reference, against `bird_k0/round_2` (re-sampled). On Spider at k = 2: 78.02 against 78.20 | 3 h (estimate; trains only) | queued |
| 6 | `refs/central_sft` | centralized SFT on the union of the 5 Spider clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 5 |

Expected (estimates), counted from 23:42. With GPU 0 alone: row 1 at
about 03:45, row 2 by about 10:00, row 3 by about 15:30, row 4 by about
01:00 on 2026-11-21, row 5 by about 04:00. With both cards about half
of that.

Not queued yet, decided on row 2: the line with an SFT stage on
BIRD (DPO from a `bird_sft` round). Rounds 3 and 4 of the gold line on
Spider follow row 1 if it still rises.

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Open for the owner:
whether the FedAvg SFT stage stays, on rows 2 and 4; whether gold
where the samples give no correct side is a part of the method, on rows
1 and 3; whether on-policy rounds are a part of the method, on row 5; round 2 of federated DPO as
published (no NLL, fixed pairs, fixed reference) for the baseline row,
from the start the method ends up with; on BIRD, the 350 golds that fail
(kept for FedAvg SFT as released) and the 184 on the 30 s budget (step
4); a copy of the adapters, samples, pairs and logs that exist on the
server's drive D only.

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
