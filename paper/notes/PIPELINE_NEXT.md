# FedLS-SQL: run queue

## Status

Updated 2026-11-21 23:34 (Asia/Ho_Chi_Minh). One card only (owner, chat,
about 22:20). `bird_k0_goldnll/round_2` is published (22:40, evaluation
22:48): 42.37 on BIRD dev, 0.65 below the same round without the gold
rows (p 0.43); the one-loss form is not kept. The worker takes
`bird_sft/round_3` next, then `bird_k2/round_1` and `bird_sft/round_4`,
in file order: not confirmed after 22:48, and nothing of
`bird_sft/round_3` is published yet. Hint probe and control (17:21,
18:05): on clients 1, 3 and 4, 31.7% of the all-wrong questions of
`bird_k0/round_2` hold a correct sample with the hint and 10.4% without
it; the hint adds 21.4 points (interval 19.0 to 23.7), and 65% have none
in either draw.
Last results:
`bird_k0_goldnll/round_2` on BIRD dev 42.37 (22:48);
`bird_k0/round_2` 43.02, `bird_fixed/round_2` 40.81 (15:07);
the six Spider rows on Spider dev, Syn, Realistic and DK (15:33). After
one DPO + NLL round on BIRD 3,017 of the 9,428 questions have no correct
sample (4,035 before it, 3,220 after one FedAvg SFT round), and round 2
trains on 8,840 pairs (round 1: 9,714).
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
On Spider dev (1,034 rows, no round or setting chosen there) the same
adapters give FedAvg SFT 75.15, k = 0 77.27 (+2.12, p 0.08), k = 2 77.66
(+2.51, p 0.02), the fixed-pair line 76.21, centralized SFT 73.02. On
Spider-Syn, Realistic and DK k = 0 is 3.00, 3.54 and 7.47 above FedAvg
SFT (p 0.024, 0.063, 2.4e-5) and k = 2 3.87, 2.75 and 3.92 (p 0.0006,
0.10, 0.017; `LAB_LOG.md`). On test-suite accuracy (dev, Syn, Realistic;
read on the Mac with the project's judge, not committed) k = 0 is level
with FedAvg SFT (p 0.58, 0.76, 0.40) and k = 2 is 2.42, 3.67 and 3.34
above it (p 0.027, 0.0004, 0.036): there the gain needs the SFT stage
(`LAB_LOG.md`, 2026-11-21).

Open, read on BIRD: what the method does with the questions that have
no correct sample (Spider 12%, BIRD 42.8% of the questions for the base
student, 34% after one SFT round, 32% after one DPO + NLL round). BIRD
dev so far:

| Total rounds | FedAvg SFT | 1 SFT round then DPO (k = 1) | DPO from the base student (k = 0) | k = 0, round 2 on fixed pairs | k = 0, gold as the chosen side | k = 0, round 2 with NLL rows on the gold SQL |
|---|---|---|---|---|---|---|
| 0 | 29.47 | | | | | |
| 1 | 38.85 | | 41.85 | | 39.24 | |
| 2 | 42.70 | 44.26 | 43.02 | 40.81 | | 42.37 |

At 2 rounds no line is separated from FedAvg SFT: k = 0 is +0.32 (p
0.80), k = 1 +1.56 (p 0.13), and k = 0 is 1.24 below k = 1 (p 0.19). The
second DPO round adds 1.17 where the second SFT round adds 3.85.
On-policy rounds are 2.21 above fixed pairs (p 0.008), kept by the rule;
the fixed line falls from its round 1. NLL rows on the gold SQL of the
3,017 all-wrong questions, in the same round as the pairs, are 0.65
below the round without them (59 questions fixed, 69 broken, p 0.43)
and 1.89 below k = 1 (p 0.045): not kept. On BIRD the gold SQL has
helped as an SFT stage before the DPO rounds and in neither form tried
inside them.

By official difficulty at 2 rounds (simple 925, moderate 464,
challenging 145; read from the committed predictions, `LAB_LOG.md`,
2026-11-21): FedAvg SFT 50.49 / 31.25 / 29.66, k = 0 50.70 / 35.13 /
19.31, k = 1 50.38 / 37.07 / 28.28, k = 0 with the gold rows 49.73 /
33.41 / 24.14. k = 0 is below FedAvg SFT on the
challenging questions (3 against 18 questions, p 0.0015); k = 1 is above
it on the moderate ones (51 against 24, p 0.0024) and level on the
others. The gold rows bring back part of the challenging level (8
against 1 question over k = 0, p 0.039) and lose on the two others.

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
it. `bird_k0/round_2` does not measure the change: its sampling ran in
three calls, two of them stopped, and client 1 was labelled on the code
before it (`LAB_LOG.md`, 2026-11-21). Golds on the 30 s budget in that
round: 72, against 50 in `bird_k1/round_1`; the `SQL budget` lines of
its log say whether the second runs 4 at a time cost them.

| GPU | State | Known from |
|---|---|---|
| the one card that runs (which of the two was not said) | `bird_sft/round_3`, going on from its checkpoints, expected since 22:48 | owner in chat, about 22:20: one card only; remote, read 23:30: `bird_k0_goldnll/round_2` published at 22:40 and 22:48, nothing of `bird_sft/round_3` yet |
| the other | not available | owner in chat |

## Run now

1. Nothing to start: the worker takes the rows below in file order.

2. Only for a card whose worker has stopped: the worker line, which
   pulls first. GPU 0 as written; GPU 1 with `--gpu 1` and, if it has
   to stop at an hour, `--until HH:MM`.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

3. Send back, when they come:
   - which card runs, and the task its worker shows now;
   - from the log of `bird_k0/round_2`
     (`.queue_state/logs/bird_k0/round_2.log`): the lines with
     `SQL budget, this call` (jobs run again after the others, jobs
     alone, seconds of each);
   - a word when `bird_sft/round_3` is published (it is then read from
     the remote);
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
| 13 | `bird_sft/round_3` with its evaluation and publications | FedAvg SFT on BIRD at 3 rounds: the baseline of the BIRD table | 2 h 50 min a round and 10 min an evaluation (measured on rounds 1 and 2) | stopped about 16:08 for the gold-row round (owner); goes on from its checkpoints on the one card, expected since 22:48, not confirmed |
| 14 | `bird_k2/round_1`, `eval_1`, publications | DPO + NLL round 1 from FedAvg SFT round 2: the method at 3 rounds, against `bird_sft/round_3` | 6.5 to 8 h (estimate: `bird_k1/round_1` took 7 h 50 min with 3 h 06 min of labels, before the label change of `0910b84f`) | queued 16:01 (code `38610a58`); after row 13 on the same card |
| 15 | `bird_sft/round_4` with its evaluation and publications | FedAvg SFT on BIRD at 4 rounds | 2 h 50 min and 10 min | queued 15:10; after rows 13 and 14 in the file |

Expected on one card (estimates): `bird_sft/round_3` is read by about
01:45, sooner by what its checkpoints hold; `bird_k2/round_1` 6.5 to 8 h
after it, about 08:30 to 10:00; `bird_sft/round_4` about 3 h after that.

The slot after `bird_k2/round_1` (proposed in chat, 2026-11-21; owner's
choice): if it is above `bird_sft/round_3` without a separation,
`bird_k2/round_2` goes before `bird_sft/round_4` and before any new part
(the method at 4 rounds, about 8 h, estimate); if it is separated, the
card goes to FedAvg SFT of a second model on Spider; if it is below,
nothing is queued before the rows are read.

The hinted round (owner's choice, not written): the hint adds 21.4
points of all-wrong questions with a correct sample over a second draw
without it, under the 25 proposed as the bar. The gold-row round is
read and did not keep the challenging level (24.14 against 29.66 for
FedAvg SFT), so by the table below the hint is the remaining form
inside a DPO round. One round with the hinted pairs from
`bird_k0/round_1` is about 4 h of training (estimate; sampling and
labels are done). It needs code (the pairs of the hinted samples joined
to the round's, trained under the prompt without the hint) and the
owner's yes to a second sampling prompt. Against it: the gold rows
covered all 3,017 questions and moved the challenging level by 7
questions net, the hint reaches about a third of them, and with an SFT
stage that level is already 28.28.

How the reads settle the method (BIRD dev, same total rounds, kept at
0.5 EX or more with McNemar p below 0.05):

| Read | If yes | If no |
|---|---|---|
| `bird_k1/round_1` above `bird_sft/round_2` | the method holds on BIRD from an SFT start; the line runs on, and the start from the best SFT round is queued | read: 44.26 against 42.70, p 0.13, a no by the rule with the difference on the method's side. Rows 4 to 6 decide; the line is not dropped |
| `bird_k0/round_2` at least equal to `bird_k1/round_1` | no SFT stage: the method is k = 0 on both datasets | read: 43.02 against 44.26, p 0.19, a no without a separation. The method on BIRD keeps an SFT stage, k as a value; which k is open until `bird_sft` rounds 3 and 4 are read |
| `bird_k0/round_2` above `bird_fixed/round_2` | on-policy rounds are a part of the method with a measured gain | read: 43.02 against 40.81, p 0.008: yes |
| `bird_k0_gold/round_1` above `bird_k0/round_1` (41.85) and `bird_sft/round_1` (38.85) | its round 2 is queued (on Spider the gold line fell there) | read: 39.24, 2.61 below `bird_k0/round_1` (p 0.007), 0.39 above `bird_sft/round_1` (p 0.76). Gold as chosen is not kept; the one-loss form below is the next try |
| `bird_k0_goldnll/round_2` above `bird_k0/round_2` (43.02), with the challenging level near that of FedAvg SFT (29.66; `bird_k0/round_2` 19.31) and the simple one not below 50.70 | the method routes a question by its samples in one loss: DPO + NLL where they are mixed, NLL on the gold SQL where all are wrong; rows after it run in that form, and whether it still needs an SFT stage is read against `bird_k1/round_1` (44.26) | read: 42.37, 0.65 below `bird_k0/round_2` (p 0.43); simple 49.73, moderate 33.41, challenging 24.14; 1.89 below `bird_k1/round_1` (p 0.045): a no. The SFT stage stays the way gold enters (k as a value); the hint is the remaining form inside a round |
| `bird_k2/round_1` above `bird_sft/round_3` | the method holds at 3 rounds from an SFT start | read with `bird_k1/round_1` against `bird_sft/round_2`: no gain over FedAvg SFT separated on BIRD at equal rounds |

Not queued yet, the owner's choice after the reads above. Open:
`bird_k2/round_2` and its twin on fixed pairs (the method at 4 rounds,
and federated DPO as published from an SFT start; about 8 h and 4.5 h,
estimates); FedAvg SFT of a second and a third model on Spider (every
language-model paper read at CMC has three or more, `JOURNAL_BAR.md`);
`bird_k1/round_2`; `bird_k0/round_3`; the round with hinted pairs;
centralized DPO + NLL on Spider as the upper reference of the method
(about 8.5 h, estimate). Not proposed any more: gold rows for every
question (`LAB_LOG.md`, 2026-11-21: the gold rows raised the broken
answers). Every BIRD row is read by official difficulty as well as
overall (simple 925, moderate 464, challenging 145).

After the method is settled (owner, 2026-11-20; `RESEARCH_STATE.md`,
section 4, item 12): centralized DPO + NLL with the federated against
centralized gap.

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
