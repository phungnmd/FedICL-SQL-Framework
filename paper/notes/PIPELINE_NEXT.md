# FedLS-SQL: run queue

## Status

Updated 2026-11-20 11:00 (Asia/Ho_Chi_Minh). Last publication: the
round record of `bird_sft/round_2` at 10:52 (its evaluation is next).
Centralized SFT ends at 3 epochs (owner, 10:55): 75.08, 75.73, 75.03;
epoch 4 was stopped in training and is not used.

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
no correct sample (Spider 12%, BIRD 41.9% of the questions for the base
student). BIRD dev so far: base student 29.47, FedAvg SFT round 1 38.85.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker started again at about 10:50 on the queue order of 09:55: it published `bird_sft/round_2` at 10:52; next its evaluation on BIRD dev, then `bird_k1/round_1` (4-5 h, estimate). | result `9ccb7837` at 10:52; the owner's line of 10:49 showed epoch 4 of centralized SFT on this card before the stop; the tasks after the publication are inferred |
| 1 | No worker since 07:30. | the `--until 07:30` of its start line |

## Run now

1. Nothing to start on GPU 0: its worker runs the BIRD rounds in the
   order of the table below. If it stops, the same line continues it
   (it pulls first):

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

2. When GPU 1 is free: the same line with `--gpu 1` and the hour it has
   to stop. It takes the next BIRD round that is ready.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 1 --until HH:MM; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

3. The relabel of `bird/read` by hand (CPU). If it has finished, nothing
   to do: the queue finds it done. If a client or more is still left,
   Ctrl+C and start the line below (16 worker processes, continues
   where it stopped). `bird_k1/round_1` labels with 16 more processes
   while it runs: watch the free RAM in the first minutes of both.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m pytest tests/test_sql_pool.py tests/test_relabel_samples.py tests/test_preference_sampling.py -q --basetemp "$tmp\pytest_sql_pool"; if ($LASTEXITCODE -ne 0) { throw 'SQL pool tests failed on this machine: send the output' }; uv run --no-sync python -m scripts.relabel_samples --src audits/protocol_v2/fedpref_bird_base_p2_ddl_alpha01_s0 --dst audits/protocol_v2/fedpref_bird_base_p2_ddl_alpha01_ev3_s0 --round 1 --policy base --split-dir processed_data/protocol_v2/BIRD/original_train9428_dev1534/federated/alpha_0.1/k5 --dataset-profile bird_with_evidence --score-workers 16; if ($LASTEXITCODE -ne 0) { throw 'Relabel failed' } }
   ```

4. Send back, when they come:
   - whether the relabel has finished, and per client its `SQL budget`,
     `before`, `after` and `sample label(s) changed` lines;
   - the EX line of `bird_sft/round_2`;
   - from `bird_k1/round_1`: the questions per client by kind (all
     correct, mixed, all wrong) and the pair counts, its EX line, and
     the peak reserved VRAM on the first updates of each client;
   - the EX line and peak VRAM of each later BIRD round;
   - a `STOP queue` line, if one comes.

5. Any time, CPU only (a few minutes each), if not done yet: the pairs
   of the base student's round 1 samples by rejected outcome, and the
   wall times of the finished tasks. Send back the printed tables of the
   first.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.log_times; if ($LASTEXITCODE -ne 0) { throw 'log_times failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: wall times of the finished queue tasks, read from their logs' --paths audits/protocol_v2/run_times; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `bird_sft/round_2` | FedAvg SFT on BIRD at 2 rounds: the row the next two are read against | 10 min left (estimate) | trained and published 10:52; evaluation on BIRD dev running or next |
| 2 | `bird_k1/round_1` | SFT stage on BIRD: one DPO + NLL round from `bird_sft` round 1, at 2 total rounds against row 1. Does DPO add to an SFT start on BIRD? Its sample counts also say how many of the 3,955 all-wrong questions the SFT round turns into questions with pairs | 4-5 h (estimate: samples, labels, training; pair count not known) | queued, needs nothing more; new 09:55 |
| 3 | `bird/relabel`, `bird/read_relabelled` | the labels of `bird/read` with SQL in worker processes, into the `_ev3` root the lines from the base student use | seconds once the run by hand is through | by hand (step 3) |
| 4 | `bird_k0/round_1` | DPO + NLL from the base student on BIRD at 1 round, against FedAvg SFT round 1 (38.85); pairs for half of the questions only (4,783 of 9,428) | 3 h (estimate; trains only) | queued, after row 3 |
| 5 | `bird_k0_gold/round_1` | the same round with gold as chosen for the all-wrong questions (BIRD train has no database without rows, the part that weighed on the Spider run): against row 4 | 4-6 h (estimate; up to 7,910 more pairs) | queued, after row 3 |
| 6 | `bird_k0/round_2` | DPO from the base student at 2 rounds, against rows 1 and 2 | 6 h (estimate; samples and labels again) | queued, after row 4 |
| 7 | `bird_fixed/round_2` | on-policy rounds on BIRD: round 2 on the round 1 pairs with a fixed reference, against row 6 | 3 h (estimate; trains only) | queued, after row 4 |
| 8 | `refs/central_sft` | the record of the centralized SFT curve: 3 epochs, best epoch 2 (75.73); trains nothing | seconds | queued last |

Expected with GPU 0 alone (estimates): `bird_sft/round_2` evaluated by
about 11:10; `bird_k1/round_1` by about 16:00, the first read of the
method on BIRD; `bird_k0/round_1` by about 19:30; `bird_k0_gold/round_1`
after midnight; `bird_k0/round_2` in the morning of 2026-11-21. A second
card takes rows 4 and 5 earlier.

How the reads settle the method (BIRD dev, same total rounds, kept at
0.5 EX or more with McNemar p below 0.05):

| Read | If yes | If no |
|---|---|---|
| `bird_k1/round_1` above `bird_sft/round_2` | the method holds on BIRD from an SFT start; the line runs on, and the start from the best SFT round is queued | DPO adds nothing to SFT there at 2 rounds: rows 4 to 6 decide |
| `bird_k0/round_2` at least equal to `bird_k1/round_1` | no SFT stage: the method is k = 0 on both datasets | the method is k SFT rounds, then DPO + NLL, k as a value |
| `bird_k0_gold/round_1` above `bird_k0/round_1` and `bird_sft/round_1` | its round 2 is queued (on Spider the gold line fell there) | gold as chosen is not kept; the one-loss form below is the next try |

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
again gives. Open for the owner: round 2 of federated DPO as published
(no NLL, fixed pairs, fixed reference) for the baseline row, from the
start the method ends up with; on BIRD, the 350 golds that fail (kept
for FedAvg SFT as released) and the 184 on the 30 s budget (step 3); a
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
