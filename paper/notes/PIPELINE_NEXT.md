# FedLS-SQL: run queue

## Status

Updated 2026-11-20 06:40 (Asia/Ho_Chi_Minh). Spider test by total rounds
trained:

| Total rounds | FedAvg SFT | 3 SFT rounds then DPO (k = 3) | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) | k = 0 with gold | Centralized SFT (epochs) |
|---|---|---|---|---|---|---|
| 1 | 72.43 | | | 75.87 | 76.67 | 75.08 |
| 2 | 74.10 | | | 77.18 | 75.73 | 75.73 |
| 3 | 74.71 | | 77.46 | 77.69 | | |
| 4 | 74.71 | 77.97 | 78.20 | 78.02 | | |

Settled on Spider: the method is DPO + NLL with execution labels on the
model's own samples (3.3 to 3.5 above FedAvg SFT at 4 rounds; without
the NLL term 73.59; NLL on correct samples alone 75.87 against 77.46).
Not kept: nearest pairs, gold as chosen, gold inside the round,
wrong-result rejects first. The FedAvg SFT stage shows no gain on Spider
at k = 0, 2 or 3 (78.02, 78.20, 77.97 at 4 rounds); it is read next on
BIRD. BIRD dev, base student: 29.47, with 646 of 1,534 outputs failing
to execute (570 `no such column`), 1 output cut at 256 tokens and 3 rows
lost to the 30 s budget. The k = 0 line with gold where the samples give no correct side
falls at round 2 on Spider (75.73 against 77.18, p 0.033; round 1:
76.67 against 75.87): not kept on Spider, rounds 3 and 4 not queued;
its round 1 on BIRD stays queued. Centralized SFT: 75.08 and 75.73
at epochs 1 and 2, the rule goes on to epoch 3. BIRD clients, 10 samples
of the base student per question: a correct SQL for 52.4% of the 9,428
questions (Spider 87.6%), all wrong 41.9% (Spider 12%), gold fails 5.7%
(350 SQL errors, 184 golds on the 30 s budget); 9,566 pairs.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `k0_gold/round_2` evaluated and published 03:54; then `bird_sft/round_1` (about 3 h, estimate). | result `1abec88c`, published 03:54; the task after it is inferred |
| 1 | Worker until 07:30: centralized SFT, epoch 2 published 06:05, epoch 3 since then; it stops in that epoch at 07:30. | result `0643b48c`, published 06:05 |

## Run now

1. Start GPU 1 now, until 07:30: it takes centralized SFT
   (`refs/central_sft`, continued from its epoch 1; it stands before
   the BIRD rounds since 2026-11-20, owner) while GPU 0 runs
   `k0_gold/round_2`. If GPU 0 does not run that round, GPU 1 takes it
   first. At 07:30 the worker stops itself and its task; the same line
   continues it later. The line pulls the queue first (fast-forward
   only, safe while GPU 0 runs):

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 1 --until 07:30; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   The same line with `--gpu 0` and without `--until` continues GPU 0
   if it stops.

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

4. Now, CPU only: pull the code that runs SQL in worker processes,
   check it on Windows (3 test files, under a minute), then label the
   samples of `bird/read` again into the root of the BIRD DPO lines
   (running since about 01:00; 4 to 6 h, estimate from client 1: 575
   of 2,011 questions after 26 min; no sampling; rerun continues). Of
   the 184 golds
   that met the 30 s budget there, 151 run alone in under 15 s, 13 in
   15 to 30 s, 20 in over 30 s. Without this step a card runs the same
   relabel as the queue task `bird/relabel` before the BIRD DPO rounds
   and stays unused meanwhile. If the tests fail the line stops before
   the relabel: send the output. Send back the test line and, per
   client, the `before`, `after`, `sample label(s) changed` and
   `SQL budget` lines.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m pytest tests/test_sql_pool.py tests/test_relabel_samples.py tests/test_eval.py -q --basetemp "$tmp\pytest_sql_pool"; if ($LASTEXITCODE -ne 0) { throw 'SQL pool tests failed on this machine: send the output' }; uv run --no-sync python -m scripts.relabel_samples --src audits/protocol_v2/fedpref_bird_base_p2_ddl_alpha01_s0 --dst audits/protocol_v2/fedpref_bird_base_p2_ddl_alpha01_ev3_s0 --round 1 --policy base --split-dir processed_data/protocol_v2/BIRD/original_train9428_dev1534/federated/alpha_0.1/k5 --dataset-profile bird_with_evidence --score-workers 4; if ($LASTEXITCODE -ne 0) { throw 'Relabel failed' } }
   ```

   The pull changes what the next tasks load, not the running one:
   evaluations and labels then run their SQL in worker processes (a
   worker that fails stops the task with `STOP queue`, it is not scored
   as wrong SQL), BIRD results carry scorer v3, and the BIRD DPO tasks
   use the `_ev3` roots and wait for `bird/relabel`. No worker restart.

5. After more tasks have finished, CPU only (under a minute): their
   wall times read from the worker's logs into
   `audits/protocol_v2/run_times/`, one file per task, then published
   (46 tasks are in since 00:29; the published files are left alone).
   Runs that start on the new code also write their times themselves.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.log_times; if ($LASTEXITCODE -ne 0) { throw 'log_times failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: wall times of the finished queue tasks, read from their logs' --paths audits/protocol_v2/run_times; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 6 | `refs/central_sft` | centralized SFT on the union of the 5 Spider clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1; before the BIRD rounds (owner, 2026-11-20): GPU 1 takes it with step 1 |
| 0 | `bird/relabel`, `bird/read_relabelled` | the labels of `bird/read` again with SQL in worker processes, into the `_ev3` root the BIRD DPO rounds use; then the pair counts of that root. How many of the 184 golds lost to the 30 s budget come back (151 run alone in under 15 s) | 4-6 h on CPU (estimate); seconds for the queue task once step 4 is through | running by hand (step 4); in the queue after `bird_sft/round_1`, so a free card trains meanwhile (a card that reaches it earlier waits for the run by hand) |
| 2 | `bird_sft/round_1`, `bird_k0/round_1` | on BIRD at 1 round: FedAvg SFT against DPO + NLL from the base student (on Spider 72.43 against 75.87). Does DPO from the base student still lead where it has pairs for half of the questions only (4,783 of 9,428; base student 29.47 on BIRD dev)? | 3 h each (estimate; `bird_k0/round_1` trains on the read's 9,566 pairs and samples nothing) | queued |
| 3 | `bird_k0_gold/round_1` | BIRD round 1 with gold as chosen for the 3,955 all-wrong questions, on the same samples: against row 2 | 4-6 h (estimate; up to 7,910 more pairs) | queued |
| 4 | `bird_sft/round_2`, `bird_k0/round_2` | the same as row 2 at 2 rounds (Spider: 74.10 against 77.18) | 3 h and 6 h (estimate; the DPO round samples and labels again, 3 h 19 min in the read) | queued |
| 5 | `bird_fixed/round_2` | on-policy rounds: round 2 on the round 1 pairs with the base student as reference, against `bird_k0/round_2` (re-sampled). On Spider at k = 2: 78.02 against 78.20 | 3 h (estimate; trains only) | queued |

Expected (estimates): `bird_sft/round_1` on GPU 0 by about 07:15.
Centralized SFT stops in epoch 3 at 07:30 with GPU 1; what is left of
it (epoch 3 and, by its rule, up to epoch 8) runs before the BIRD
rounds not started on the next free card.

Not queued yet, decided on row 2: the line with an SFT stage on
BIRD (DPO from a `bird_sft` round).

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Open for the owner:
whether the FedAvg SFT stage stays, on rows 2 and 4; whether gold
where the samples give no correct side is a part of the method on BIRD, on row
3 (not kept on Spider); whether on-policy rounds are a part of the method, on row 5; round 2 of federated DPO as
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
