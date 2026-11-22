# FedLS-SQL: run queue

## Status

Updated 2026-11-22 10:31 (Asia/Ho_Chi_Minh). One card only (owner, chat,
2026-11-21 about 22:20). Queued at 10:29 (owner, code `05cf77cc`): the
Spider line on two more student models, Qwen2.5-Coder-0.5B-Instruct and
deepseek-coder-1.3b-instruct, after `bird_sft/round_4`; the worker gets
the rows when it publishes that round. `bird_k2/round_1` is published (09:28,
evaluation 09:34): one DPO + NLL round from FedAvg SFT round 2 is 46.22
on BIRD dev, 2.54 above FedAvg SFT at 3 rounds (125 questions against
86, p 0.0087) and 3.52 above its start (p 0.0003): the first gain over
FedAvg SFT at equal rounds from an SFT start that is separated on BIRD,
at the k of the best Spider line. `bird_sft/round_3` (01:35): 43.68, 0.98 above round 2
(p 0.11). The worker takes `bird_sft/round_4` next in file order, the
last queued row: not confirmed, and nothing of it is published at
09:53. `bird_k0_goldnll/round_2` (2026-11-21, 22:48):
42.37, 0.65 below the same round without the gold rows (p 0.43); the
one-loss form is not kept. Hint probe and control (17:21,
18:05): on clients 1, 3 and 4, 31.7% of the all-wrong questions of
`bird_k0/round_2` hold a correct sample with the hint and 10.4% without
it; the hint adds 21.4 points (interval 19.0 to 23.7), and 65% have none
in either draw.
Last results:
`bird_k2/round_1` on BIRD dev 46.22 (2026-11-22, 09:34);
`bird_sft/round_3` 43.68 (01:35);
`bird_k0_goldnll/round_2` 42.37 (22:48);
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
student, 34% after one SFT round, 28.6% after two, 32% after one DPO +
NLL round). BIRD
dev so far:

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | 1 SFT round then DPO (k = 1) | DPO from the base student (k = 0) | k = 0, round 2 on fixed pairs | k = 0, gold as the chosen side | k = 0, round 2 with NLL rows on the gold SQL |
|---|---|---|---|---|---|---|---|
| 0 | 29.47 | | | | | | |
| 1 | 38.85 | | | 41.85 | | 39.24 | |
| 2 | 42.70 | | 44.26 | 43.02 | 40.81 | | 42.37 |
| 3 | 43.68 | 46.22 | | | | | |

At 3 rounds k = 2 is 2.54 above FedAvg SFT (p 0.0087), 1.96 above k = 1
at 2 rounds (p 0.031) and 3.19 above k = 0 at 2 rounds (p 0.0025). From
FedAvg SFT round 2 the DPO + NLL round fixes 135 answers and breaks 81,
the third SFT round 45 and 30; execution errors go from 286 to 102,
wrong results from 593 to 723.
At 2 rounds no line is separated from FedAvg SFT: k = 0 is +0.32 (p
0.80), k = 1 +1.56 (p 0.13), and k = 0 is 1.24 below k = 1 (p 0.19). The
second DPO round adds 1.17 where the second SFT round adds 3.85. The
third SFT round adds 0.98 (45 questions fixed, 30 broken, p 0.11):
FedAvg SFT slows on BIRD as it did on Spider (+1.67, +0.61, 0), and
k = 1 at 2 rounds is level with it at 3 rounds (126 against 117
questions, p 0.61; on the moderate ones 50 against 29, p 0.024).
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
33.41 / 24.14; FedAvg SFT at 3 rounds 51.57 / 32.54 / 28.97, k = 2 at 3
rounds 53.08 / 36.85 / 32.41 (above FedAvg SFT on all three, the
moderate one separated: 41 questions against 21, p 0.015). k = 0 is
below FedAvg SFT on the
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
estimate; measured in `bird_k2/round_1`: 2 h 39 min of labels in a round
of 7 h 50 min). The server has that code: the result commit of 06:50 sits on
it. `bird_k0/round_2` does not measure the change: its sampling ran in
three calls, two of them stopped, and client 1 was labelled on the code
before it (`LAB_LOG.md`, 2026-11-21). Golds on the 30 s budget in that
round: 72, against 50 in `bird_k1/round_1`; the `SQL budget` lines of
its log say whether the second runs 4 at a time cost them.

| GPU | State | Known from |
|---|---|---|
| the one card that runs (which of the two was not said) | `bird_sft/round_4`, expected since 09:35; then rows 16 to 20 | owner in chat, 2026-11-21 about 22:20: one card only; remote, read 10:29: `bird_k2/round_1` published at 09:28 and 09:34, nothing of `bird_sft/round_4` yet |
| the other | not available | owner in chat |

## Run now

1. Nothing to start while the worker runs: its publication of
   `bird_sft/round_4` pulls the new rows, and it takes them in file
   order. If the worker had already ended (`DONE queue`) or stopped,
   start it with the line of step 2.

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
   - a word when `bird_sft/round_4` is published (it is then read from
     the remote);
   - a look at the worker about 13:00 (estimate), when row 16 should be
     done: the task it shows, or its `STOP queue` line. Row 16 is where
     a new model fails if it fails: a download that does not come, a
     probe above 21.5 GiB, a model vLLM does not load;
   - a `STOP queue` line, whenever one comes.

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
| 15 | `bird_sft/round_4` with its evaluation and publications | FedAvg SFT on BIRD at 4 rounds | 2 h 50 min and 10 min | queued 2026-11-21 15:10; next in file order since 09:35, not confirmed |
| 16 | `models/probe_qwen05b`, `models/probe_dsc13b`, `models/base_qwen05b`, `models/base_dsc13b` with their publications | do the two models download, fit in memory and decode; their rows without training on Spider test | 25 min | queued 2026-11-22 10:29 |
| 17 | `qwen05b_sft/round_1` and `round_2`, `qwen05b_k2/round_1`, `qwen05b_sft/round_3`, each with its evaluation and publications | Qwen2.5-Coder-0.5B on Spider: the method at 3 rounds (2 SFT rounds, 1 DPO + NLL round) against FedAvg SFT at 3 rounds | 5 h | queued 2026-11-22 10:29 |
| 18 | `qwen05b_k2/round_2`, `qwen05b_sft/round_4` | the same at 4 rounds | 3 h | queued 2026-11-22 10:29 |
| 19 | `dsc13b_sft/round_1` and `round_2`, `dsc13b_k2/round_1`, `dsc13b_sft/round_3` | DeepSeek-Coder-1.3B on Spider: the method at 3 rounds against FedAvg SFT at 3 rounds | 10 h | queued 2026-11-22 10:29 |
| 20 | `dsc13b_k2/round_2`, `dsc13b_sft/round_4` | the same at 4 rounds | 5.5 h | queued 2026-11-22 10:29 |

Expected on one card (estimates; no round of either model is measured):
`bird_sft/round_4` is read about 12:35, row 16 about 13:00, the 0.5B at
3 rounds about 18:00 and at 4 rounds about 21:00, DeepSeek at 3 rounds
about 07:00 on 2026-11-23 and at 4 rounds about 12:30.

Rows 16 to 20 (owner, 2026-11-22): each model runs the line of
Qwen2.5-Coder-1.5B with the model changed and nothing else: prompt
`ddl_rows` through the model's own chat template, the SFT recipe, FedAvg
SFT rounds 1 to 4, DPO + NLL rounds 1 and 2 from FedAvg SFT round 2
(k = 2, the k of the 1.5B, not chosen again per model), Spider test.
They are read as the 1.5B rows: the method against FedAvg SFT at 3 and
at 4 rounds, exact McNemar. Checked before queuing (`LAB_LOG.md`,
2026-11-22): the resolved commands against the 1.5B line, the rendered
prompt and target of both models, the lengths (longest training
sequence 6,927 tokens with the Qwen tokenizer, 6,070 with DeepSeek's).
Not measured: memory and time. A long row's memory follows heads times
length squared, which puts both models near the 1.5B's peak (19.83
GiB), and the probes of row 16 read it before any round. A task that
fails stops the worker, the other model's line included.

Open after these rows, not queued: `bird_k2/round_2` (the method at 4
rounds on BIRD, about 8 h) and its twin on fixed pairs (federated DPO
as published from an SFT start, about 4.5 h).

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
| `bird_k2/round_1` above `bird_sft/round_3` (43.68) | read: 46.22, 2.54 above (125 questions against 86, p 0.0087): yes. The method holds at 3 rounds from an SFT start, at the k of the best Spider line (k = 2) | no gain over FedAvg SFT separated on BIRD at equal rounds |

Not queued yet, the owner's choice after the reads above. Open:
`bird_k2/round_2` and its twin on fixed pairs (the method at 4 rounds,
and federated DPO as published from an SFT start; about 8 h and 4.5 h,
estimates); the two more models on BIRD, if the paper's BIRD table is
to carry them; `bird_k1/round_2`; `bird_k0/round_3`; the round with hinted pairs;
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
