# FedLS-SQL: run queue

## Status

Updated 2026-11-21 16:09 (Asia/Ho_Chi_Minh). The server has code
`38610a58`: GPU 1 started `bird_k0_goldnll/round_2` at 16:08 (worker log
in chat) with 8,840 pairs and 3,017 gold rows, as expected (per client
1,992 + 625, 1,516 + 595, 2,150 + 641, 552 + 284, 2,630 + 872). Not
known: where `hint/probe` and `bird_sft/round_3` stand. The probe is not
published at 16:09, and `hint/publish_probe` stands before the task GPU 1
took, so the probe is not finished; the status line (Reference) says
which card holds what. `bird_k2` stands before `bird_sft/round_4`.
Last results:
`bird_k0/round_2` on BIRD dev 43.02, `bird_fixed/round_2` 40.81 (15:07);
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
0.10, 0.017; `LAB_LOG.md`).

Open, read on BIRD: what the method does with the questions that have
no correct sample (Spider 12%, BIRD 42.8% of the questions for the base
student, 34% after one SFT round, 32% after one DPO + NLL round). BIRD
dev so far:

| Total rounds | FedAvg SFT | 1 SFT round then DPO (k = 1) | DPO from the base student (k = 0) | k = 0, round 2 on fixed pairs | k = 0 with gold |
|---|---|---|---|---|---|
| 0 | 29.47 | | | | |
| 1 | 38.85 | | 41.85 | | 39.24 |
| 2 | 42.70 | 44.26 | 43.02 | 40.81 | |

At 2 rounds no line is separated from FedAvg SFT: k = 0 is +0.32 (p
0.80), k = 1 +1.56 (p 0.13), and k = 0 is 1.24 below k = 1 (p 0.19). The
second DPO round adds 1.17 where the second SFT round adds 3.85.
On-policy rounds are 2.21 above fixed pairs (p 0.008), kept by the rule;
the fixed line falls from its round 1.

By official difficulty at 2 rounds (simple 925, moderate 464,
challenging 145; read from the committed predictions, `LAB_LOG.md`,
2026-11-21): FedAvg SFT 50.49 / 31.25 / 29.66, k = 0 50.70 / 35.13 /
19.31, k = 1 50.38 / 37.07 / 28.28. k = 0 is below FedAvg SFT on the
challenging questions (3 against 18 questions, p 0.0015); k = 1 is above
it on the moderate ones (51 against 24, p 0.0024) and level on the
others.

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
| 1 | `bird_k0_goldnll/round_2`, training, since 16:08 | worker log in chat, 16:08 |
| 0 | `hint/probe` or `bird_sft/round_3` (owner, about 15:48: both ran then); the other of the two is not on a card if GPU 1 held it before 16:08 | not known at 16:09 |

## Run now

1. Send the output of the status line (Reference, read-only). It says
   which of `hint/probe` and `bird_sft/round_3` GPU 0 runs and whether
   the other one waits. If `bird_sft/round_3` waits, it resumes from its
   last checkpoint on the first free card, after row 12 in the file.

2. Only for a card whose worker has stopped: the worker line, which
   pulls first. GPU 0 as written; GPU 1 with `--gpu 1` and, if it has
   to stop at an hour, `--until HH:MM`.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

3. Send back, when they come:
   - the `DONE hint probe` line and the five `client N:` lines above it,
     or a word when `hint/publish_probe` is done (it is then read from
     the remote);
   - from `bird_k0_goldnll/round_2`: a `DPO update` line of client 1
     with its `peak reserved` and `left`;
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
| 11 | `hint/probe`, `hint/publish_probe` | do the 3,017 all-wrong questions of `bird_k0/round_2` get a correct sample when the prompt names the tables and columns of the gold SQL? Samples and labels, no training | about 30 min (estimate: sampling 9 min, labels not measured) | running (owner, about 15:48) |
| 12 | `bird_k0_goldnll/reuse_samples`, `round_2`, `eval_2`, publications | one loss for both kinds of question: the 8,840 pairs of `bird_k0/round_2` unchanged, plus NLL on the gold SQL of its 3,017 all-wrong questions (one row each, no preference term), from `bird_k0/round_1`. Does it keep the challenging level without a loss on the simple one? Against `bird_k0/round_2` (43.02), `bird_k1/round_1` (44.26), `bird_sft/round_2` (42.70) | about 4.5 h, training only (estimate), 10 min evaluation | running on GPU 1 since 16:08: 8,840 pairs and 3,017 gold rows |
| 13 | `bird_sft/round_3` with its evaluation and publications | FedAvg SFT on BIRD at 3 rounds: the baseline of the BIRD table | 2 h 50 min a round and 10 min an evaluation (measured on rounds 1 and 2) | running (owner, about 15:48) |
| 14 | `bird_k2/round_1`, `eval_1`, publications | DPO + NLL round 1 from FedAvg SFT round 2: the method at 3 rounds, against `bird_sft/round_3` | more than 5 h (estimate: sampling, labels, training) | queued 16:01 (code `38610a58`), not pulled yet; ready after row 13 on the same card, or on the card of row 12 if it ends first |
| 15 | `bird_sft/round_4` with its evaluation and publications | FedAvg SFT on BIRD at 4 rounds | 2 h 50 min and 10 min | queued 15:10; after rows 13 and 14 in the file |

Expected (estimates): the probe ends about 16:20; row 12 is read about
21:15 if its card takes it at 16:30; `bird_sft/round_3` is read about
19:00, `bird_k2/round_1` about 5.5 h after its card takes it.

After the probe (owner's choice, proposed): 25% or more of the 3,017
with a correct sample: one training round with the hinted pairs from
`bird_k0/round_1`, about 4 h; needs code (the pairs of the hinted
samples joined to the round's). It is read against row 12, which uses
the same gold SQL without a second sampling: the hint is kept only if it
is above it. Under 25% the hint is dropped.

How the reads settle the method (BIRD dev, same total rounds, kept at
0.5 EX or more with McNemar p below 0.05):

| Read | If yes | If no |
|---|---|---|
| `bird_k1/round_1` above `bird_sft/round_2` | the method holds on BIRD from an SFT start; the line runs on, and the start from the best SFT round is queued | read: 44.26 against 42.70, p 0.13, a no by the rule with the difference on the method's side. Rows 4 to 6 decide; the line is not dropped |
| `bird_k0/round_2` at least equal to `bird_k1/round_1` | no SFT stage: the method is k = 0 on both datasets | read: 43.02 against 44.26, p 0.19, a no without a separation. The method on BIRD keeps an SFT stage, k as a value; which k is open until `bird_sft` rounds 3 and 4 are read |
| `bird_k0/round_2` above `bird_fixed/round_2` | on-policy rounds are a part of the method with a measured gain | read: 43.02 against 40.81, p 0.008: yes |
| `bird_k0_gold/round_1` above `bird_k0/round_1` (41.85) and `bird_sft/round_1` (38.85) | its round 2 is queued (on Spider the gold line fell there) | read: 39.24, 2.61 below `bird_k0/round_1` (p 0.007), 0.39 above `bird_sft/round_1` (p 0.76). Gold as chosen is not kept; the one-loss form below is the next try |
| `bird_k0_goldnll/round_2` above `bird_k0/round_2` (43.02), with the challenging level near that of FedAvg SFT (29.66; `bird_k0/round_2` 19.31) and the simple one not below 50.70 | the method routes a question by its samples in one loss: DPO + NLL where they are mixed, NLL on the gold SQL where all are wrong; rows after it run in that form, and whether it still needs an SFT stage is read against `bird_k1/round_1` (44.26) | the SFT stage stays the way gold enters (k as a value); the hint, if the probe passes, is the remaining form |
| `bird_k2/round_1` above `bird_sft/round_3` | the method holds at 3 rounds from an SFT start | read with `bird_k1/round_1` against `bird_sft/round_2`: no gain over FedAvg SFT separated on BIRD at equal rounds |

Not queued yet, the owner's choice after the reads above. Open:
`bird_k1/round_2`; `bird_k0/round_3`; the round with hinted pairs (after
the probe); centralized DPO + NLL on Spider as the upper reference of
the method (about 8.5 h, estimate). Every BIRD row is read by official
difficulty as well as overall (simple 925, moderate 464, challenging
145).

After the method is settled (owner, 2026-11-20; `RESEARCH_STATE.md`,
section 4, item 12): centralized DPO + NLL with the federated against
centralized gap; questions
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
