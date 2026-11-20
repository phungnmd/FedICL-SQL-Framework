# FedLS-SQL: run queue

## Status

Updated 2026-11-20 11:10 (Asia/Ho_Chi_Minh). Last result: FedAvg SFT
round 2 on BIRD dev, 42.70, published 10:57. The relabel of `bird/read`
has finished (owner, 11:00; its lines not sent yet).
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
student). BIRD dev so far: base student 29.47, FedAvg SFT round 1 38.85,
round 2 42.70 (still rising: +3.85).

| GPU | State | Known from |
|---|---|---|
| 0 | Worker on `bird_k1/round_1` since about 10:58 (sampling, labels, training: 4-5 h, estimate); then the relabel tasks (seconds), `bird_k0/round_1`, `bird_k0_gold/round_1`. | result `53c7bee1` at 10:57; the task after it is the first ready one in the queue, inferred |
| 1 | No worker since 07:30. Free card: step 2 puts `bird_k0/round_1` on it now. | the `--until 07:30` of its start line |

## Run now

1. Nothing to start on GPU 0: its worker runs the BIRD rounds in the
   order of the table below. If it stops, the same line continues it
   (it pulls first):

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

2. When GPU 1 is free: the same line with `--gpu 1` and the hour it has
   to stop. The relabel is done, so it takes the relabel tasks (they
   find the work done, seconds) and then `bird_k0/round_1` (3 h,
   estimate) next to `bird_k1/round_1` on GPU 0.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 1 --until HH:MM; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

3. Send back, when they come:
   - from the relabel, per client: its `SQL budget`, `before`, `after`
     and `sample label(s) changed` lines;
   - from `bird_k1/round_1`: the questions per client by kind (all
     correct, mixed, all wrong) and the pair counts, its EX line, and
     the peak reserved VRAM on the first updates of each client;
   - the EX line and peak VRAM of each later BIRD round;
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

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 2 | `bird_k1/round_1` | SFT stage on BIRD: one DPO + NLL round from `bird_sft` round 1, at 2 total rounds against `bird_sft` round 2 (42.70). Does DPO add to an SFT start on BIRD? Its sample counts also say how many of the 3,955 all-wrong questions the SFT round turns into questions with pairs | 4-5 h (estimate: samples, labels, training; pair count not known) | running on GPU 0 since about 10:58 (inferred) |
| 3 | `bird/relabel`, `bird/read_relabelled` | the labels of `bird/read` with SQL in worker processes, into the `_ev3` root the lines from the base student use | seconds | run by hand finished (owner); the tasks only register it |
| 4 | `bird_k0/round_1` | DPO + NLL from the base student on BIRD at 1 round, against FedAvg SFT round 1 (38.85); pairs for half of the questions only (4,783 of 9,428) | 3 h (estimate; trains only) | queued; ready after row 3 |
| 5 | `bird_k0_gold/round_1` | the same round with gold as chosen for the all-wrong questions (BIRD train has no database without rows, the part that weighed on the Spider run): against row 4 | 4-6 h (estimate; up to 7,910 more pairs) | queued, after row 3 |
| 6 | `bird_k0/round_2` | DPO from the base student at 2 rounds, against `bird_sft` round 2 (42.70) and row 2 | 6 h (estimate; samples and labels again) | queued, after row 4 |
| 7 | `bird_fixed/round_2` | on-policy rounds on BIRD: round 2 on the round 1 pairs with a fixed reference, against row 6 | 3 h (estimate; trains only) | queued, after row 4 |
| 8 | `refs/central_sft` | the record of the centralized SFT curve: 3 epochs, best epoch 2 (75.73); trains nothing | seconds | queued last |

Expected with GPU 0 alone (estimates): `bird_k1/round_1` by about
15:30 to 16:00, the first read of the method on BIRD; `bird_k0/round_1`
by about 19:00; `bird_k0_gold/round_1` after midnight; `bird_k0/round_2`
in the morning of 2026-11-21. With GPU 1 from now: `bird_k0/round_1` by
about 14:30 and each later row about 3 h earlier.

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
