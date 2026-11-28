# FedExec-SQL: run queue

## Status

A worker on GPU 0 runs the control since 2026-11-28, about 12:37. Read
at 17:35: `sft_prefset/round_3` is 75.45 on Spider test, 0.74 above
FedAvg SFT round 3 (p 0.11) and 2.01 below the method at 3 rounds
(p 0.0036); `bird_sft_prefset/round_3` is 43.16 on BIRD dev (17:42),
0.52 below FedAvg SFT round 3 (p 0.45) and 3.06 below the method at 3
rounds (p 0.0014; `LAB_LOG.md`). Round 4 of both runs next.
The other tasks wait for a card (Run now, step 2). The last published results are `bird_rft/round_2` (`7dc8e9c3`)
and `bird_feddpo` round 2 (`15f9df7d`), both read (`LAB_LOG.md`,
2026-11-28).

First to run (queued 2026-11-28, owner; code `c282b25c`, queue
`3716b8fd`): the control of the main comparison, `sft_prefset` and
`bird_sft_prefset`. FedAvg SFT rounds 3 and 4 from FedAvg SFT round 2,
trained at the settings of the DPO + NLL rounds (learning rate 5e-5,
weight decay 1e-4, warm-up 0.1, LoRA dropout 0) and otherwise as
FedAvg SFT. It answers how much of the gain over FedAvg SFT at 4 rounds (6.19 on
BIRD dev, 3.49 on Spider test) comes from those settings and not from
the DPO + NLL rounds. Run now, step 1, runs these tasks alone. The
paper has no row for the control yet: the row, its tests and the
sentences of Sections 5 and 6 on the settings follow the result. The
BIRD rounds ran longer than estimated (`bird_rft/round_2` about 8.1 h against 6 h), so the hours
below are likely low.

Queued 2026-11-28 (owner; `b8e4a44e`), after the two Spider rounds and
ahead of the rest: local SFT of each BIRD client (`bird_local`, does
federating pay) and seed 1 of the two main BIRD rows (`bird_sft_s1`,
`bird_k2_s1`, does the gain hold on a second training seed).

How to read the control on BIRD dev at 4 rounds (the method 48.76,
FedAvg SFT 42.57, the round without the preference term 45.24): near
43 to 44, the gain over FedAvg SFT stays at about 5; near 45, about
3.5 is left, the size of the gain over the round without the preference
term; 47 or more, the main claim of the paper does not hold as written.

Queued 2026-11-28 (owner; code `ba7932de`, queue `14992724`), right after
`bird_local`: `bird_local_k2`, each BIRD client alone runs the two DPO +
NLL rounds of `bird_k2` on its own rows from its local SFT epoch 2 (the
row "the method without the federation"). It answers the readers' point
that the method is CodeLutra run under FedAvg: a client holds its
databases, gold SQL and model, so what does the federation add.

Queued 2026-11-28 (owner; `c52e37ff`, pushed): `bird_nonll/round_2`,
the on-policy round 2 without the NLL term on BIRD, the "no NLL term"
cell of Table 4 at 4 rounds, after the second seed since the order of
`b8e4a44e`.

File order of what is left when the queue runs again (hours are estimates; a second card takes the
first ready task the other does not hold):

| Order | Tasks | Cells it fills | About |
|---|---|---|---|
| 0 | `sft_prefset` rounds 3 and 4, `bird_sft_prefset` rounds 3 and 4, each with its evaluation | a row to add to Tables 3 and 4: FedAvg SFT at the settings of the DPO + NLL rounds | 10.5 h |
| 1 | `feddpo/round_2`, `rft/round_2` | Table 3, Spider: FedDPO; Table 4, Spider: no preference term at 4 rounds | 6.5 h |
| 2 | `bird_local/client_1` to `client_5` | Table 3, BIRD: Local SFT (mean, lowest and highest client) | 11.5 h |
| 3 | `bird_local_k2/client_1` to `client_5`, rounds 1 and 2, each with its evaluation | a row to add, BIRD: the method run by each client alone (mean, lowest and highest client) | 18 h |
| 4 | `bird_sft_s1` rounds 1 to 4, `bird_k2_s1` rounds 1 and 2 | Table 3, BIRD: the two rows of the second seed | 28 h |
| 5 | `bird_nonll/round_2` with its evaluation | Table 4, BIRD: no NLL term at 4 rounds | 8 h |
| 6 | `pooled_k2` rounds 1 and 2, `pooled_dev` | Table 4, Spider: clients pooled | 4 h |
| 7 | `deepseek13b_sft` rounds 3 and 4, `deepseek13b_k2/round_2`, their rows on the other Spider sets | Table 5, Spider: DeepSeek-Coder-1.3B | 8 h |
| 8 | `iid_sft` rounds 1 to 4, `iid_k2` rounds 1 and 2 | Table 6: IID | 13 h |
| 9 | `bird_vote/sft_4`, `bird_vote/k2_2` | no cell of a table | 2 h |
| 10 | `bird_wrfirst` | no cell of a table | 5 h |
| 11 | `a05_sft` rounds 1 to 4, `a05_k2` rounds 1 and 2 | Table 6: alpha 0.5, 5 clients | 13 h |
| 12 | `a05k10_sft` rounds 1 to 4, `a05k10_k2` rounds 1 and 2 | Table 6: alpha 0.5, 10 clients | 13 h |
| 13 | `bird_central/sft` | Table 3, BIRD: centralized SFT | 8.5 h |

About 148 GPU hours in all (estimate). After them the tables still lack
the rows of `Not queued yet` below. The manuscript does not wait for
any of them: it is completed with placeholders and marked guesses
(`AGENTS.md`, Writing).

Read 2026-11-28 on BIRD dev (`LAB_LOG.md`): at 4 rounds the method
(48.76) is 3.26 above FedDPO (45.50, p 0.00014) and 3.52 above RFT
(45.24, p 5.2e-05); at 3 rounds 1.24 above FedDPO (44.98, p 0.17).
Without the NLL term the BIRD round still rises over its start, unlike
Spider; the term is not separated in EX on BIRD. Under the generated
test suite of BIRD dev FedDPO at 4 rounds is level with FedAvg SFT
(37.61 against 36.70, p 0.42) and 3.98 below the method (p 6.8e-06).


Dataset roles (owner, 2026-11-25; `RESEARCH_STATE.md`, section 3.4):
BIRD is the main dataset (the main rows, every baseline, the ablations
of the parts, a second student model), Spider carries the breadth rows
(the other models, the federated setups, the variant sets, test-suite
accuracy). A new row is queued on the set its role names. The rows the
paper still needs and are not queued are listed under the table of
`Running and queued`.

Earlier status (2026-11-24): The workers run (owner): the
Spider dev rows by round are published (`68c38e28`). At 4 rounds k = 2
is the highest on Spider dev under EX (77.66) and test-suite accuracy
(70.41), so k is chosen on dev (`LAB_LOG.md`, 2026-11-24). Queued
`9976390e` and `d6aa4ad7`, the method rows first: re-aggregation, FedAvg SFT rounds 5 and 6, `bird_k2/round_2`
and its fixed twin, federated DPO as published at 4 rounds, RFT round 2;
then the pooled line, the other sets and DeepSeek as before; last the
BIRD federated DPO baseline and the IID line. A worker started before
`9976390e` gets the new order at its next publication. Strict labels
are closed (77.27 against 77.46 on test, p 0.76). Which task each card
runs now is not known here.
Read between 17:30 and the stop (`LAB_LOG.md`, 2026-11-23):
`qwen05b_k4/round_1` (18:22): 65.49 on Spider test, 1.40 above its
start (p 0.058) and 1.30 above FedAvg SFT at 5 rounds (p 0.075), not
above the rows from round 2 (65.86, 66.19). The 0.5B rows on Spider
dev (18:12, 18:25): FedAvg SFT rounds 3 to 7 are 58.99, 59.77, 59.48,
59.28, 58.03; the method from round 2 is 63.35 and 65.09, 5.32 above
FedAvg SFT at 4 rounds (p 1.1e-06) and 5.80 above round 6; one DPO +
NLL round from round 4 gives 63.15 and from round 6 62.57. An early
start is at least as good as a late one on both sets, so k = 2 stands
for the 0.5B. The pair read from the BIRD-trained start (17:50): on
the Spider clients it samples like the base student (5,864 mixed and
973 all-wrong questions; base 5,951 and 1,074; FedAvg SFT round 2 on
Spider 5,192 and 573). The prefix probe (17:30): 57% to 88% of the
all-wrong questions get a correct sample, mostly the gold SQL. Running
(expected, not confirmed): `pooled_k2/round_1` on GPU 1 since about
18:12, `deepseek13b_sft/round_3` on the other card since about 18:25.
FedAvg SFT round 7 of the 0.5B (16:53): 64.32 on Spider test. `deepseek13b_k2/round_1` is read
(08:34): 75.08 on Spider test, 5.26 above its start, FedAvg SFT round 2
(192 questions against 79, p 5.0e-12); FedAvg SFT round 3 of this
model, the row at equal rounds, is not published. The Spider line of Qwen2.5-Coder-0.5B is
finished: at 4 rounds the method is 66.19 on Spider test and FedAvg SFT
64.09 (01:08), 2.10 above it (149 questions against 104, p 0.0056); at
3 rounds 65.86 against 62.69 (+3.17, p 1.3e-05). The gap narrows: the
second DPO + NLL round adds 0.33 (p 0.62) and FedAvg SFT round 4 adds
1.40 (p 0.0059), still rising. The card runs the line of
DeepSeek-Coder-1.3B: FedAvg SFT rounds 1 and 2 are 64.00 and 69.82
(02:56, 04:43). The next task is `deepseek13b_k2/round_1`: expected to
run since 04:43, not confirmed.
`bird_sft/round_4` is read (12:40): 42.57 on BIRD dev, 1.11 below round
3 (p 0.068), and the method at 3 rounds is 3.65 above it (p 0.0001).
DeepSeek-Coder-1.3B: its first probe and base row (EX 0.00, 12:55) ran
with a tokenizer that dropped every space and newline and are not
results. Fixed in code `58cd89f7`; the line is queued again as
`deepseek13b` (`e694b9fe`, 16:12) with its tokenizer from the model's
`tokenizer.json` and a length limit of 8,704; on that code its row
without training is 55.85 (16:41) and its 4 longest rows train in 8.29
GiB reserved. `bird_k2/round_1` is published (09:28,
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
DeepSeek-Coder-1.3B on Spider test, FedAvg SFT round 2 69.82
(2026-11-23, 04:43), round 1 64.00 (02:56);
Qwen2.5-Coder-0.5B on Spider test, FedAvg SFT round 4 64.09 (01:08),
DPO + NLL round 2 from FedAvg SFT round 2 66.19 (2026-11-22, 23:14),
FedAvg SFT round 3 62.69 (21:28), DPO + NLL round 1 from FedAvg SFT
round 2 65.86 (19:22), FedAvg SFT round 2 60.60 (16:46),
round 1 58.13 (14:45), without training 54.40 (12:55);
DeepSeek-Coder-1.3B without training 55.85 (16:41);
`bird_sft/round_4` on BIRD dev 42.57 (12:40);
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

The other student models on Spider test (owner, 2026-11-22; k = 2 is
the k of the 1.5B, not chosen again):

| Total rounds | Qwen 0.5B, FedAvg SFT | Qwen 0.5B, 2 SFT rounds then DPO (k = 2) | DeepSeek 1.3B, FedAvg SFT | DeepSeek 1.3B, k = 2 |
|---|---|---|---|---|
| 0 | 54.40 | | 55.85 | |
| 1 | 58.13 | | 64.00 | |
| 2 | 60.60 | | 69.82 | |
| 3 | 62.69 | 65.86 | | |
| 4 | 64.09 | 66.19 | | |

The 0.5B is 13.7 below the 1.5B without training and 14.3 below after
one round (+3.73 for the round, p 7e-6; the 1.5B +4.38). Its execution
errors do not fall in round 1 (469 to 476; the 1.5B 287 to 215). Round
2 adds 2.47 (p 6.2e-5). The DPO + NLL round from round 2 adds 5.26
(p 1.9e-12; the same step on the 1.5B 3.36), on every hardness level,
with execution errors from 429 to 304 and wrong results from 417 to
429. FedAvg SFT round 3 adds 2.09 (p 5.3e-05; execution errors 429 to
392): at 3 rounds the method is 3.17 above FedAvg SFT (154 questions
against 86, p 1.3e-05; the 1.5B 2.75), on every hardness level. FedAvg
SFT has not flattened on this model (+3.73, +2.47, +2.09 a round; the
1.5B +4.38, +1.67, +0.61, 0). At 4 rounds the method is 2.10 above it
(149 against 104, p 0.0056; the 1.5B 3.49): FedAvg SFT round 4 adds
1.40 (p 0.0059) and the second DPO + NLL round 0.33 (p 0.62; 4,810
pairs against 8,328, client updates with cosine 0.02 to 0.09 against
0.27 to 0.34, as on the 1.5B). The gain holds at equal rounds and
narrows; the level FedAvg SFT reaches on this model is not measured
(`LAB_LOG.md`, 2026-11-23).

DeepSeek-Coder-1.3B: FedAvg SFT adds 8.15 and 5.82 in rounds 1 and 2
(p 1.4e-12, 8.1e-15). Round 1 moves it to the form of the gold SQL
(exact match 15.37 to 51.14): wrong results 796 to 433, execution
errors 152 to 340, then 218 after round 2. Its DPO + NLL round starts
from a FedAvg SFT that rises faster than the 0.5B's did (+5.82 against
+2.47 in round 2).

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
| 4 | 42.57 | | | | | | |

FedAvg SFT has its best round at 3: round 4 is 1.11 below it (30
questions fixed, 47 broken, p 0.068; on the moderate ones 5 against 17,
p 0.017) and level with round 2. k = 2 at 3 rounds is 3.65 above FedAvg
SFT at 4 rounds (133 questions against 77, p 0.0001).
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
| GPU 0 | worker of queue `4a962ced`; task now not known (expected `feddpo/round_2` or `rft/round_2`) | result commits of 2026-11-28 |
| GPU 1 | worker of queue `4a962ced`; task now not known (expected the other of the two) | result commits of 2026-11-28 |

## Run now

1. The control of the main comparison, and nothing else (`--phase
   sft_prefset bird_sft_prefset`). GPU 0 as written; on a second card
   the same line with `--gpu 1`. With two cards one takes the Spider
   rounds and the other the BIRD rounds, about 6.5 h (estimate: a
   FedAvg SFT round trained 124 min on Spider and 173 min on BIRD, plus
   its evaluation); with one card about 10.5 h, the two round 3 first.
   Memory is that of the FedAvg SFT rounds (same model, batch, length
   limit and loss path). The worker pulls first, publishes each round
   and each evaluation, and stops with `DONE queue` when all are in.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0 --phase sft_prefset bird_sft_prefset; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   If a card is free for a short time only, the vote evaluations of
   BIRD dev instead (`--phase bird_vote`: FedAvg SFT round 4 and the
   method at 4 rounds, 16 samples each at T 0.8, voted by execution
   result; about 1 h each, estimate; vLLM at 0.80 of the card):

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed (a publication may be running: run the line again)' }; uv run --no-sync python -m scripts.gpu_worker run --gpu 0 --phase bird_vote; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

2. On each card that is free, and on GPU 0 once the control worker has
   stopped with `DONE queue`: the line of step 1 without `--phase
   sft_prefset bird_sft_prefset` (GPU 1 with `--gpu 1`). It takes the
   first ready task in file order that no other worker holds: the two
   Spider rounds, then the five `bird_local` clients, then the five
   `bird_local_k2` clients (each after its own local SFT), then the
   second seed. The peak reserved VRAM of round 1 of `a05_sft` and
   `a05k10_sft` is to be read when they come (expected 19.83 GiB, not
   measured on these splits).

3. Send back, when they come:
   - the `DONE queue` or `STOP queue` line of the control worker, and
     the EX of the four evaluations if they are at hand
     (`fedavg_prefset_ddl_rows_a01_r3` and `r4` on Spider test,
     `fedavg_bird_prefset_ddl_a01_r3` and `r4` on BIRD dev); the worker
     publishes the rows;
   - the `DONE queue` or `STOP queue` line of the vote worker; nothing
     else for the `bird_vote` rows: the worker publishes their results
     (`experiments/pass_at_k/results/`);
   - when the queue runs again: which card runs, and the task its
     worker shows;
   - from the log of `bird_k0/round_2`
     (`.queue_state/logs/bird_k0/round_2.log`), if not sent yet: the
     lines with `SQL budget, this call` (jobs run again after the
     others, jobs alone, seconds of each).

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
| 48 | `sft_prefset/round_3`, `round_4`, `bird_sft_prefset/round_3`, `round_4`, each with its evaluation and publications | how much of the gain over FedAvg SFT comes from the training settings: FedAvg SFT rounds 3 and 4 from FedAvg SFT round 2 at the settings of the DPO + NLL rounds (learning rate 5e-5, weight decay 1e-4, warm-up 0.1, LoRA dropout 0), run as private stages in their own roots (`fedavg_prefset_ddlrows_alpha01_s0`, `fedavg_bird_prefset_ddl_alpha01_s0`); against FedAvg SFT (Spider test 74.71, 74.71; BIRD dev 43.68, 42.57), the method (77.46, 78.20; 46.22, 48.76) and RFT (75.87; 44.39, 45.24) | about 10.5 h (estimate) | running since 2026-11-28 12:37; round 3 read: Spider test 75.45 (`1d85aa58`), BIRD dev 43.16 (`2ec3679e`) |
| 46 | `bird_rft/round_2` with its evaluation | the method without its preference term at 4 rounds on BIRD: RFT round 2, samples drawn again from RFT round 1 (44.39), against `bird_k2/round_2` (48.76) | about 8.1 h (measured) | read 2026-11-28: 45.24, 3.52 below `bird_k2/round_2` (p 5.2e-05), 0.85 above its round 1 (p 0.14) |
| 38 | `bird_feddpo/*` | federated DPO as published on BIRD from FedAvg SFT round 2: round 1 without NLL on the round 1 samples of `bird_k2` (copied), round 2 on the same pairs and reference; against `bird_k2` at 3 and 4 rounds | about 9.7 h (measured) | read 2026-11-28: round 1 44.98 (1.24 below `bird_k2/round_1`, p 0.17), round 2 45.50 (3.26 below `bird_k2/round_2`, p 0.00014) |
| 36 | `feddpo/round_2` with its evaluations (test, dev) | federated DPO as published at 4 rounds (no NLL, round 1's pairs and reference) from FedAvg SFT round 2; round 1 is `decide/nonll` (73.59) | about 3 h (estimate) | queued 2026-11-24 (`9976390e`); place in the file order of 2026-11-27 (`4a962ced`): third, with `rft/round_2` |
| 37 | `rft/round_2` with its evaluations (test, dev) | RFT at 4 rounds, on-policy (samples drawn again from RFT round 1, 75.87): the method without its preference term | about 3.5 h (estimate) | queued 2026-11-24 (`9976390e`); place in the file order of 2026-11-27 (`4a962ced`): third, after `feddpo/round_2` |
| 49 | `bird_local/client_1` to `client_5` (curves `local_bird_ddl_alpha01_s0/client_c`) | does federating pay on BIRD: SFT of each client alone on its own rows, 3 epochs, the recipe, prompt and evaluation of `bird_central`, each epoch evaluated on BIRD dev; mean, lowest and highest client against FedAvg SFT (43.68, 42.57) and the method (48.76) | about 11.5 h (estimate) | queued 2026-11-28 (`b8e4a44e`), after `rft/round_2`; one task per client |
| 51 | `bird_local_k2/client_c_round_1`, `client_c_round_2` for c = 1 to 5, each with its evaluation and publications | does the method need the federation: each BIRD client alone runs the two DPO + NLL rounds of `bird_k2` on its own rows and databases (`--local-client c --n-clients 1`, no aggregation), from its local SFT epoch 2 (`local_bird_c{c}_ddl_a01_e2_s0`), so each client trains as much as in the method at 4 rounds; roots `fedpref_local_bird_e2_p2_ddl_alpha01_s0/client_c`; mean, lowest and highest client on BIRD dev against the method (46.22, 48.76) and local SFT | about 18 h (estimate: a federated round of `bird_k2` trains the same rows in about 8 h, plus 10 evaluations) | queued 2026-11-28 (`14992724`), after `bird_local`; round 1 of a client after its local SFT |
| 50 | `bird_sft_s1/round_1` to `round_4`, `bird_k2_s1/round_1`, `round_2`, each with its evaluation (FedAvg SFT from round 2 on) | does the gain at 4 rounds (6.19 on seed 0) hold on a second training seed: the commands of `bird_sft` and `bird_k2` with `--seed 1` (LoRA initialisation, data order, dropout, samples, pairs), the client split unchanged, roots `fedavg_bird_base_ddl_alpha01_s1` and `fedpref_bird_sftr2_p2_ddl_alpha01_s1` | about 28 h (estimate) | queued 2026-11-28 (`b8e4a44e`), after `bird_local` |
| 47 | `bird_nonll/round_2` with its evaluation and publications | the method without the NLL term at 4 rounds on BIRD, on-policy: round 2 of `bird_k2` with NLL weight 0, continuing `bird_feddpo/round_1` (44.98, not trained again); against `bird_k2/round_2` (48.76) and `bird_feddpo/round_2` (45.50, also fixed pairs) | about 8 h (estimate: `bird_rft/round_2` 8.1 h) | queued 2026-11-28 (`c52e37ff`); in the file after `rft/round_2`, before `pooled_k2` |
| 28 | `pooled_k2/round_1`, `pooled_k2/round_2`, each with its evaluation and publications | do the DPO + NLL rounds lose anything to the federation: the two rounds of `dpo_k2` (1.5B, from FedAvg SFT round 2) with the clients pooled into one, no aggregation; read against 77.46 and 78.20 on Spider test. Pooled above federated: a part for the aggregation is worth a test; level: the federated rounds keep the pooled level | about 2 h a round with its evaluation (estimate, not measured) | queued 2026-11-23 16:35 (`c92b0dd3`); neither round is published; place in the file order of 2026-11-27 (`4a962ced`): fourth |
| 31 | `spider_sets_dev/*`, `spider_sets_var/*`, `qwen05b_var/*`, `pooled_dev/*` | evaluations only, the rounds the tables need on the other Spider sets: the two ablation rounds of the 1.5B on Spider dev; the 1.5B rows by round and the ten 0.5B rows on Syn, Realistic and DK; the pooled rounds on Spider dev (each after its round) | about 2 h (estimate: 3 min a row on dev, 6 min on the three sets) | queued 2026-11-23 19:15 (`e425fa42`); the rows of Table 7 are committed, `pooled_dev/*` waits for the pooled rounds |
| 22 | `deepseek13b_k2/round_1`, `deepseek13b_sft/round_3`, each with its evaluation and publications | DeepSeek-Coder-1.3B on Spider: the method at 3 rounds against FedAvg SFT at 3 rounds | 1 h 48 min a FedAvg round with its evaluation (rounds 1 and 2, between publications); the DPO round not measured, 2.5 to 3 h (estimate) | FedAvg SFT rounds 1 and 2 read (64.00, 69.82), `deepseek13b_k2/round_1` read (75.08); `deepseek13b_sft/round_3` not published, after the 0.5B rows in file order since `447f8423` |
| 23 | `deepseek13b_k2/round_2`, `deepseek13b_sft/round_4` | the same at 4 rounds | 4 to 5 h (estimate) | queued 2026-11-22 16:12 |
| 32 | `deepseek13b_dev/*`, `deepseek13b_var/*` | the DeepSeek-Coder-1.3B rows on Spider dev and on Syn, Realistic and DK (no training, FedAvg SFT rounds 1 to 4, DPO + NLL rounds 1 and 2); rows of rounds still to run wait for them | about 1 h (estimate) | queued 2026-11-23 19:15 (`e425fa42`), after the DeepSeek rounds |
| 39 | `iid_sft/round_1` to `round_4`, `iid_k2/round_1`, `round_2`, each with its evaluation | the 1.5B line on the IID split (`iid/k5`): FedAvg SFT against the method at 3 and 4 rounds, the second heterogeneity level | about 13 h (estimate) | queued 2026-11-24 (`9976390e`); place in the file order of 2026-11-27 (`4a962ced`): sixth, after the DeepSeek rows |
| 41 | `bird_vote/sft_4`, `bird_vote/k2_2`, each with its publication | does the gain hold under self-consistency on BIRD dev: 16 samples per question at T 0.8, vote by execution result, for FedAvg SFT round 4 (greedy 42.57) and the method at 4 rounds (greedy 48.76); also pass@16 of both | about 1 h a row, no training (estimate, not measured) | queued 2026-11-26 (`2df1f8b4`); place in the file order of 2026-11-27 (`4a962ced`): seventh, after the IID line |
| 42 | `bird_wrfirst/reuse_samples`, `bird_wrfirst/round_1` with its evaluation and publications | the rejected side on BIRD: `bird_k2` round 1 with `--pair-rule wrong_result_first` on the same samples; does BIRD show the trade of Spider (wrong results down, execution errors up, EX level), read against 46.22 / 102 / 723 | about 5 h, training and evaluation only (estimate) | queued 2026-11-27 (`c2d80f57`); place in the file order of 2026-11-27 (`4a962ced`): eighth, after `bird_vote` |
| 43 | `a05_sft/round_1` to `round_4`, `a05_k2/round_1`, `round_2`, each with its evaluation | the 1.5B line on `alpha_0.5/k5`: FedAvg SFT against the method at 3 and 4 rounds, a milder non-IID partition | about 13 h (estimate) | queued 2026-11-27 (`4a962ced`), ninth |
| 44 | `a05k10_sft/round_1` to `round_4`, `a05k10_k2/round_1`, `round_2`, each with its evaluation | the same on `alpha_0.5/k10`: 10 clients against 5 at the same alpha | about 13 h (estimate; 10 clients over the same 8,659 rows) | queued 2026-11-27 (`4a962ced`), tenth |
| 45 | `bird_central/sft` | centralized SFT on the union of the BIRD clients, 3 epochs, each with its evaluation on BIRD dev | about 8.5 h (estimate) | queued 2026-11-25 (`684723d7`); eleventh since 2026-11-27 |
| 30 | `spider_dev/fedavg_r1` to `r3`, `spider_dev/k0_r1` to `r3`, `spider_dev/k2_r1`, `spider_dev/k3_r1`, `spider_dev/publish_rounds` | the 1.5B rows by round on Spider dev, so that the start of the DPO + NLL rounds (k = 0, 2, 3) reads on dev at every count of rounds; dev holds k = 0 and k = 2 at 4 rounds only (77.27, 77.66) | about 25 min, no training (estimate) | queued 2026-11-23 18:55 (`185d41cd`), first in the file. With `spider_dev/k3_r1` k is read on Spider dev at 4 rounds (k = 0, 2, 3); test-suite accuracy on the Mac after its publication |
| 33 | `reagg/*` | the FedAvg weights of a DPO round: `dpo_k2/round_1` (Spider) and `bird_k2/round_1` (BIRD) aggregated again by questions and equally from the saved client adapters (pairs: the round itself, a check); read against 77.46 / 75.05 and 46.22 | about 45 min, no training (estimate) | read 2026-11-24: no weighting separated from pair counts (within 0.51 on Spider test, dev and BIRD dev); pair counts kept |
| 40 | `sft_more/round_5`, `round_6`, each with its evaluations (test, dev) | does FedAvg SFT reach the method with more rounds: on Spider dev round 4 still gained 1.94 over round 3 (p 0.0045; on test 74.71 at both); read against the method at 4 rounds (78.20 test, 77.66 dev) | about 3 h (estimate) | round 5 read: 73.92 test, 74.18 dev, below round 4 on both; round 6 dropped by the owner (`c6d9720b`) |
| 34 | `bird_k2/round_2` with its evaluation | the method at 4 rounds on BIRD, against `bird_sft/round_4` (42.57) and round 3 (43.68) | about 8 h (estimate, round 1: 7 h 50 min) | read 2026-11-25: 48.76, 6.19 above `bird_sft/round_4` (p 4.6e-11) and 5.08 above round 3 (p 4.9e-08) |
| 35 | `bird_k2_fixed/round_2` with its evaluation | the on-policy part from an SFT start on BIRD: round 2 on round 1's pairs and reference, NLL kept, against `bird_k2/round_2`; continues `bird_k2`, samples nothing | about 4 h (estimate: `bird_fixed/round_2` trained 3 h 32 min) | read 2026-11-25: 46.15, 2.61 below `bird_k2/round_2` (p 0.0006) |

The rows above are in file order; the first two and the last five are
read. The new lines
(43, 44) are the IID line with the split, the stage labels, the roots
and the arm names changed (`--n-clients 10` on the split of 10); a test
of the code repository compares the three setups with the alpha 0.1
line. Measured between publications: `qwen05b_k4/round_1` with its
evaluation 1 h 29 min, a FedAvg SFT round of the 0.5B with its
evaluation 1 h 48 min.

Rows 17 to 23 (owner, 2026-11-22; rows 17 and 18, the 0.5B line, are
finished and logged): each model runs the line of
Qwen2.5-Coder-1.5B with the model changed: prompt `ddl_rows` through
the model's own chat template, the SFT recipe, FedAvg SFT rounds 1 to
4, DPO + NLL rounds 1 and 2 from FedAvg SFT round 2 (k = 2, the k of
the 1.5B, not chosen again per model), Spider test. They are read as
the 1.5B rows: the method against FedAvg SFT at 3 and at 4 rounds,
exact McNemar. One more difference for DeepSeek: its tokenizer gives
8,238 tokens for the longest training row (82 rows above 7,168, all on
client 3), so its length limit is 8,704; no row is cut or refused for
any model. The 0.5B's memory is measured (peak reserved 20.25 GiB on
client 3 in round 1). A task that fails stops the worker, the other
model's line included.

Open after these rows, not queued, for the 0.5B: FedAvg SFT round 8 and a
DPO + NLL round from a later round, only if round 7 of row 26 still
rises by more than 0.5 EX point.

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

Next to queue (owner, 2026-11-28): clients pooled on BIRD (the DPO +
NLL rounds of `bird_k2` with the five clients as one, about 16 h,
estimate), after `bird_local_k2`.

Not queued yet: the rows the paper needs (owner, 2026-11-25;
`RESEARCH_STATE.md`, section 3.4), in the order to queue them (owner,
2026-11-27: the rows of Table 3 first, then the two warm-up rows of
Table 4, the second seed, the second model on BIRD). Hours are
estimates; each needs its queue lines and the check of its resolved
commands before it runs. The two alpha 0.5 setups are queued (rows 43
and 44 above), and so are local SFT on BIRD and the second seed (rows 49
and 50).

| # | Rows | Set | What it answers | About |
| --- | --- | --- | --- | --- |
| 2 | FedProx SFT, rounds 1 to 4 (mu to set) | BIRD | a second federated SFT baseline in the main table | 11.5 h |
| 3 | `bird_k0` rounds 3 and 4 | BIRD | k = 0 against k = 2 at 4 rounds; the read can change k on BIRD | 14 h |
| 4 | one DPO + NLL round from `bird_sft/round_3` (k = 3) | BIRD | k = 3 at 4 rounds | 7 h |
| 6 | DeepSeek-Coder-1.3B: FedAvg SFT rounds 1 to 4, DPO + NLL rounds 1 and 2 from round 2 | BIRD | the BIRD table on a second model; memory on BIRD to measure first | 30 h |
| 7 | `bird_k2/round_3`, with `bird_sft/round_5` if the row is used | BIRD | where the method stops rising | 7 h and 3 h |

On Spider, local SFT per client and FedProx run when a card is free.
Also open, the
owner's choice: `bird_k1/round_2`; the round with hinted pairs. Not
proposed any more: gold rows for every
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
