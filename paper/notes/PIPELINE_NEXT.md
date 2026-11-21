# FedLS-SQL: run queue

## Status

Updated 2026-11-21 12:45 (Asia/Ho_Chi_Minh). Last result:
`bird_k0_gold/round_1` on BIRD dev, 39.24, published 2026-11-21 06:58.
From the owner's console at 12:25, not committed: after one DPO + NLL
round on BIRD 3,017 of the 9,428 questions have no correct sample (4,035
before it, 3,220 after one FedAvg SFT round), and round 2 trains on
8,840 pairs (round 1: 9,714).
Centralized SFT ends at 3 epochs (owner, 10:55): 75.08, 75.73, 75.03;
epoch 4 was stopped in training and is not used.
Queued last (owner, 11:15): six Spider rows on Spider dev, Spider-Syn,
Spider-Realistic and Spider-DK, evaluation only (code `930db2d0`).

Spider test by total rounds trained:

| Total rounds | FedAvg SFT | 3 SFT rounds then DPO (k = 3) | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) | k = 0 with gold | Centralized SFT (epochs) |
|---|---|---|---|---|---|---|
| 1 | 72.43 | | | 75.87 | 76.67 | 75.08 |
| 2 | 74.10 | | | 77.18 | 75.73 | 75.73 |
| 3 | 74.71 | | 77.46 | 77.69 | | 75.03 |
| 4 | 74.71 | 77.97 | 78.20 | 78.02 | | |

Settled on Spider: DPO + NLL with execution labels on the model's own
samples, 2 random pairs per question (3.3 to 3.5 above FedAvg SFT at 4
rounds; without the NLL term 73.59; NLL on correct samples alone 75.87
against 77.46). No gain on Spider: nearest pairs, wrong-result rejects
first, on-policy rounds over fixed pairs (78.20 against 78.02, with
3,354 pairs against 8,026), the FedAvg SFT stage (k = 0, 2, 3: 78.02,
78.20, 77.97), gold as chosen (round 2 falls: 75.73 against 77.18).

Open, read on BIRD: what the method does with the questions that have
no correct sample (Spider 12%, BIRD 42.8% of the questions for the base
student, 34% after one SFT round, 32% after one DPO + NLL round). BIRD
dev so far:

| Total rounds | FedAvg SFT | 1 SFT round then DPO (k = 1) | DPO from the base student (k = 0) | k = 0 with gold |
|---|---|---|---|---|
| 0 | 29.47 | | | |
| 1 | 38.85 | | 41.85 | 39.24 |
| 2 | 42.70 | 44.26 | running | |

k = 0 at 1 round is 3.00 above FedAvg SFT, exact McNemar p 0.005 (152
questions fixed, 106 broken): kept by the rule, as on Spider (+3.44 at 1
round). k = 1 at 2 rounds is 1.56 above, p 0.13 (127 fixed, 103 broken):
not separated. Both rounds cut the execution errors (371 to 211, 285 to
120) and leave more wrong results (566 to 673, 593 to 727). Gold as
chosen for the 4,035 all-wrong questions is 2.61 below k = 0 without it,
p 0.007 (86 fixed, 126 broken; execution errors 211 to 76, wrong
results 673 to 827), and 0.39 above FedAvg SFT, p 0.76: not kept, as on
Spider, where it fell at round 2. A BIRD round with samples takes about 8 h (sampling 27
min, labels 3 h 06 min, training 4 h 17 min). Of the labels, 2 h 03 min
are SQL run again alone after meeting the 30 s under load, on clients 1,
2 and 5 (`LAB_LOG.md`, 2026-11-21). From code `0910b84f` a label step
runs them after its other questions, 4 at a time (labels about 1.5 h,
estimate). The server has that code: the result commit of 06:50 sits on
it, and `bird_k0/round_2` started after it. The label time of that round
is read from its `timing.json` when it is published; the console of
12:25 does not show it.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker on `bird_k0/round_2` since 10:33: pairs built at 11:07, clients 1 to 3 trained, client 4 in its DPO updates at 12:25, client 5 left (2,630 pairs). EX about 14:45 (estimate). Before it, on the same card: `bird_fixed/round_2`, 06:58 to 10:33. | status output and task log, owner's console, 12:25 |
| 1 | No worker. `bird_fixed/publish_round_2`, `bird_fixed/eval_2` and rows 8 to 10 are ready and wait; with GPU 0 alone they start after the evaluation of `bird_k0/round_2`, about 14:50 (estimate). | status output, owner's console, 12:25 |

## Run now

1. Nothing to start on GPU 0: its worker runs the BIRD rounds in the
   order of the table below. If it stops, the same line continues it
   (it pulls first):

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

2. GPU 1 has no worker (12:25). If the card is free: the check of step 5
   first (seconds), then the same line with `--gpu 1` and the hour it
   has to stop. It takes what is left of `bird_fixed` (the evaluation of
   round 2 and the two publications: its EX in about 15 min), then rows
   8 to 10 (about 1 h, estimate).

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 1 --until HH:MM; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

3. Send back, when they come:
   - the EX lines of `bird_fixed/round_2` and `bird_k0/round_2`, or a
     word that they are published (they are then read from the remote,
     with the round's times and its `questions_gold_timeout`);
   - from the log of `bird_k0/round_2`
     (`.queue_state/logs/bird_k0/round_2.log`): the lines with
     `SQL budget, this call` (jobs run again after the others, jobs
     alone, seconds of each);
   - the EX line of each later BIRD round;
   - a `STOP queue` line, if one comes.

4. Any time, CPU only (a few minutes each), if not done yet: the pairs
   of the base student's round 1 samples by rejected outcome, and the
   wall times of the finished tasks. Send back the printed tables of the
   first.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.log_times; if ($LASTEXITCODE -ne 0) { throw 'log_times failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: wall times of the finished queue tasks, read from their logs' --paths audits/protocol_v2/run_times; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

5. Any time, CPU only (seconds), before the Spider dev rows start: are
   the databases of the four sets and the five adapters on the server?
   Send back its last line, or the paths it lists. A missing path fails
   the evaluation task, and a failed task stops its worker. Not run
   here: the Mac has no PowerShell.

   ```powershell
   & { $ErrorActionPreference='Stop'; $miss=@(); foreach ($f in 'processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv','processed_data/SPIDER_SYN/test.csv','processed_data/SPIDER_REALISTIC/test.csv','processed_data/SPIDER_DK/test.csv') { $miss += Import-Csv $f | Select-Object -ExpandProperty db_path -Unique | Where-Object { -not (Test-Path $_) } }; foreach ($a in 'artifacts/protocol_v2/fedavg_base_ddlrows_alpha01_s0/round_4/fedavg_adapter','artifacts/protocol_v2/central_base_ddlrows_s0/e2/adapter','artifacts/protocol_v2/fedpref_base_p2_ddlrows_alpha01_s0/dpo/round_4/global_adapter','artifacts/protocol_v2/fedpref_sftr2_ddlrows_alpha01_s0/dpo/round_2/global_adapter','artifacts/protocol_v2/fedpref_sftr2_fixed_ddlrows_alpha01_s0/dpo/round_2/global_adapter') { if (-not (Test-Path $a)) { $miss += $a } }; if ($miss.Count) { $miss; throw "$($miss.Count) path(s) missing" } else { 'OK: the databases and adapters of the Spider dev and variant evaluations are there' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 6 | `bird_k0/round_2` | DPO from the base student at 2 rounds, against `bird_sft` round 2 (42.70) and `bird_k1/round_1` (44.26) | training about 3 h 25 min for its 8,840 pairs (estimate from round 1's seconds per pair) | running on GPU 0 since 10:33 on code `0910b84f`; client 4 of 5 in training at 12:25 |
| 7 | `bird_fixed/round_2` | on-policy rounds on BIRD: round 2 on the round 1 pairs with a fixed reference, against row 6 (8,840 new pairs there) | evaluation about 10 min | trained on GPU 0 in 3 h 35 min, ended 10:33; publication and evaluation ready, no worker free |
| 8 | `refs/central_sft` | the record of the centralized SFT curve: 3 epochs, best epoch 2 (75.73); trains nothing | seconds | queued |
| 9 | `spider_dev/*` (6 evaluations, one publication) | Spider dev (1,034 rows) for the base student, FedAvg SFT round 4, centralized SFT epoch 2, k = 0 round 4, k = 2 round 2 and its fixed-pair line: does the gain over FedAvg SFT hold on the set most papers report, where no round or setting was chosen? | 20 min (estimate; a Spider test evaluation took 2.5 to 5.5 min) | queued, no training |
| 10 | `spider_variants/*` (6 evaluations, one publication) | the same six rows on Spider-Syn (1,034), Spider-Realistic (508) and Spider-DK (535) | 40 min (estimate) | queued last, no training |

Expected with GPU 0 alone (estimates, from the measured times of
`bird_k0/round_1`): the EX of `bird_k0/round_2` by about 14:45, that of
`bird_fixed/round_2` about 15:00, rows 8 to 10 by about 16:00. With a
worker on GPU 1 from now: the EX of `bird_fixed/round_2` in about 15
min, rows 8 to 10 an hour later. Rows 9 and 10 need no earlier task.

How the reads settle the method (BIRD dev, same total rounds, kept at
0.5 EX or more with McNemar p below 0.05):

| Read | If yes | If no |
|---|---|---|
| `bird_k1/round_1` above `bird_sft/round_2` | the method holds on BIRD from an SFT start; the line runs on, and the start from the best SFT round is queued | read: 44.26 against 42.70, p 0.13, a no by the rule with the difference on the method's side. Rows 4 to 6 decide; the line is not dropped |
| `bird_k0/round_2` at least equal to `bird_k1/round_1` | no SFT stage: the method is k = 0 on both datasets | the method is k SFT rounds, then DPO + NLL, k as a value |
| `bird_k0_gold/round_1` above `bird_k0/round_1` (41.85) and `bird_sft/round_1` (38.85) | its round 2 is queued (on Spider the gold line fell there) | read: 39.24, 2.61 below `bird_k0/round_1` (p 0.007), 0.39 above `bird_sft/round_1` (p 0.76). Gold as chosen is not kept; the one-loss form below is the next try |

Not queued yet, each decided on the reads above: the winning BIRD line
and `bird_sft` to 4 rounds; DPO from the best `bird_sft` round, 1 to 2
rounds (owner's expectation of the highest level); one local loss with
DPO + NLL on the mixed questions and NLL on the gold SQL for the
all-wrong ones (needs code: a preference weight per row); centralized
DPO + NLL on Spider as the upper reference of the method (about 8.5 h,
estimate).

After the method is settled (owner, 2026-11-20; `RESEARCH_STATE.md`,
section 4, item 12): centralized DPO + NLL with the federated against
centralized gap; the one-loss form above if BIRD asks for it; questions
without gold SQL labelled by vote, as a secondary experiment, after a
CPU probe of the vote labels.

Reading: a difference of about 0.2 EX is what running the same training
again gives. Open for the owner: a probe of a table-and-column hint for
the questions without a correct sample on BIRD (proposed in chat,
2026-11-21; not approved, needs code; sampling and labels of the 3,017
questions of `bird_k0/round_2`, about 30 min on a free card, estimate);
round 2 of federated DPO as published
(no NLL, fixed pairs, fixed reference) for the baseline row, from the
start the method ends up with; on BIRD, the 350 golds that fail (kept
for FedAvg SFT as released) and the 184 on the 30 s budget (the relabel); a
copy of the adapters, samples, pairs and logs that exist on the server's
drive D only.

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
