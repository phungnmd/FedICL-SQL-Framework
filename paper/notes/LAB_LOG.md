# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

## 2026-11-11: gold line closed: the BIRD stage alone does not survive DPO, the teacher does

Spider test, seed 0, vLLM inproc (fedicl-sql `a5220912`, `ada6601e`, curve
record `cce543f2`). DPO round 3 from `gold_k2aaa_a3`: **75.22** (71
execution errors, 461 wrong results; 3,492 pairs, 1,174 with an execution
error and 2,318 with a wrong result on the rejected side).

| Round | No server stage (FedAvg R3) | BIRD gold SFT | BIRD Hinton KD | Hinton minus gold |
|---|---:|---:|---:|---:|
| start | 71.26 | 73.08 | 73.31 | +0.23 |
| 1 | 74.29 | 74.34 | 75.69 | +1.35 |
| 2 | 75.17 | 75.13 | 76.43 | +1.30 |
| 3 | 75.13 | 75.22 | **76.71** | +1.49 |

| Pair at round 3 | Gain | Right only in the first / only in the second | p | 95% interval (databases) |
|---|---:|---:|---:|---|
| FedAvg line / gold line | +0.09 | 123 / 125 | 0.95 | -1.64 to +1.84 |
| gold line / Hinton line | +1.49 | 77 / 109 | 0.02 | -0.24 to +3.16 |
| FedAvg line / Hinton line | +1.58 | 101 / 135 | 0.03 | -0.09 to +3.20 |
| `gold_k2aaa_a3` / gold DPO r3 | +2.14 | 47 / 93 | < 0.001 | +0.77 to +3.54 |
| gold DPO r2 / r3 | +0.09 | 27 / 29 | 0.89 | |

- The gold server stage leads FedAvg R3 by 1.82 before DPO and by nothing
  after it, at every round (+0.05, -0.04, +0.09): what BIRD with gold SQL
  adds, the DPO rounds also give.
- The Hinton stage keeps 1.3 to 1.5 points over the gold stage at every
  round, on the same BIRD questions: the part of the server stage that
  survives DPO comes from the teacher's distribution, not from the BIRD
  data. By rows it is separable at round 3 (p = 0.02), by databases the
  interval touches zero. The three rounds are one pair of lineages, not
  three tests; seed 1 is what confirms it.
- Error types at round 3 (execution errors / wrong results): FedAvg line
  101 / 433, gold line 71 / 461, Hinton line 58 / 442. The gold stage
  trades execution errors for wrong results; the Hinton stage lowers
  execution errors without that.
- Before DPO the two stages already differ on the sets no choice was made
  on (fedicl-sql `7eaad90a`): Spider dev 70.50 against 72.82 (28 / 52,
  p = 0.01, interval +1.19 to +3.64), DK 52.71 against 58.13 (6 / 35,
  p < 0.001, +2.41 to +8.09), Realistic 61.42 against 62.01 (26 / 29). The
  gold DPO rounds on these sets are queued (`rob_gold_dpo_r*`).

## 2026-11-11: focused DPO pilot queued; federation is the setting, not the claim

No run. Two owner decisions after a review of the direction (an agent's
literature check and the committed predictions).

- Federation: the method is one that works in the federated setup; the
  paper does not claim that federation produces the gain. DPO on pooled
  data (centralized) and DPO without aggregation (local only) are reference
  rows that show what the setting costs, not a condition of the claim. Not
  queued yet.
- Pilot, ahead of the gold line in the queue: arm `fdpo`, round 1 from
  `hinton_k2aaa_a3` on the round 1 samples and pairs of the Hinton line
  (fedicl-sql `43d4fb40`, queue `c3a3a16e`). The preference term follows
  Focused-DPO (arXiv 2502.11475): the response tokens of a pair are split
  into common prefix, differing middle and common suffix; the middle
  log-ratios are weighted by 2 and the rejected suffix is left out. The NLL
  term, pairs, schedule and updates are those of DPO round 1 (75.69, 82
  execution errors, 440 wrong results), which is its comparator. One round
  only; about 1 h 45 (estimate). Read: Spider test EX, wrong-result count,
  execution errors, and the span lengths in `client_*_train.json`
  (`focus`).
- What to expect (estimate, not a measurement): 0 to +1 point over DPO
  round 1. The common prefix already cancels in the plain DPO margin and
  the pairs are the nearest ones (similarity 0.83), so the loss changes
  less than in the papers (+1 to +3 over plain DPO on 7B code models,
  Focused-DPO; +1.07 on Spider test at 9B for clause against outcome
  rewards, CAPER). One paired comparison separates about 0.8 to 1 point.

How much the wrong-result rows can move, from the committed Spider test
predictions of the 17 SQL rows (vLLM inproc): of the 442 wrong-result rows
of the method (Hinton DPO round 3), 193 are right in at least one other row
and 249 are wrong in every row; 271 rows of the test set are wrong in all
17 rows (the union of the 17 rows is right on 87.38%). Of the 444
wrong-result rows of `hinton_k2aaa_a3`, 371 are still wrong results after
three DPO rounds.

Literature check (2026-11-11, not yet in `LITERATURE.md`): no federated
Text-to-SQL paper besides FL4SP was found. Federated RL with a verifier on a
small decoder now exists: FedMOA (arXiv 2602.00453) runs federated GRPO
with Qwen2.5-1.5B-Instruct on code (HumanEval gains 0 to +1.8); it and
PubSwap are the closest work to cite. Not found: execution on the client's
own databases as the verifier, federated DPO with such pairs, Text-to-SQL
with EX.

## 2026-11-11: DPO round 3 from FedAvg R3, DPO rounds 1-2 from `gold_k2aaa_a3`

Spider test, seed 0, vLLM inproc (fedicl-sql `bc3a36a0`, `f222c624`, curve
record `9238c82b`; `f03534f6`, `1b79dad0`; `d2e57969`, `0f4fdb80`). The
worker was restarted after the two crashes; the FedAvg line closed at its
maximum of 3 rounds.

| Round | From FedAvg R3 | From `gold_k2aaa_a3` | From `hinton_k2aaa_a3` |
|---|---:|---:|---:|
| start | 71.26 | 73.08 | 73.31 |
| 1 | 74.29 | 74.34 | 75.69 |
| 2 | 75.17 | 75.13 | 76.43 |
| 3 | 75.13 | running | **76.71** |

Paired, with a 95% interval from a bootstrap over the 40 test databases
(10,000 resamples), computed from the committed predictions:

| Pair | Gain | Right only in the first / only in the second | p | 95% interval |
|---|---:|---:|---:|---|
| FedAvg R3 / Hinton DPO r3 | +5.45 | 76 / 193 | < 0.001 | +3.45 to +7.43 |
| FedAvg R3 / FedAvg DPO r3 | +3.87 | 59 / 142 | < 0.001 | +2.23 to +5.60 |
| `hinton_k2aaa_a3` / Hinton DPO r3 | +3.40 | 37 / 110 | < 0.001 | +2.21 to +4.53 |
| +1 FedAvg SFT round / Hinton DPO r3 | +2.56 | 51 / 106 | < 0.001 | +1.35 to +3.77 |
| central Spider + BIRD / Hinton DPO r3 | +2.75 | 108 / 167 | < 0.001 | +0.84 to +4.64 |
| FedAvg DPO r2 / FedAvg DPO r3 | -0.04 | 20 / 19 | 1.00 | |
| FedAvg DPO r3 / Hinton DPO r3 | +1.58 | 101 / 135 | 0.03 | -0.09 to +3.20 |
| `gold_k2aaa_a3` / gold DPO r1 | +1.26 | 37 / 64 | 0.009 | +0.23 to +2.37 |
| FedAvg DPO r1 / gold DPO r1 | +0.05 | 123 / 124 | 1.00 | |
| gold DPO r1 / Hinton DPO r1 | +1.35 | 81 / 110 | 0.04 | -0.05 to +2.65 |
| gold DPO r1 / gold DPO r2 | +0.79 | 27 / 44 | 0.06 | |
| FedAvg DPO r2 / gold DPO r2 | -0.04 | 122 / 121 | 1.00 | |
| gold DPO r2 / Hinton DPO r2 | +1.30 | 76 / 104 | 0.04 | -0.09 to +2.56 |
| `gold_k2aaa_a3` / `hinton_k2aaa_a3` | +0.23 | 76 / 81 | 0.75 | -1.18 to +1.70 |

- The FedAvg line is flat after round 2. Its round 3 has 101 execution
  errors and 433 wrong results (Hinton round 3: 58 and 442).
- The server stage keeps 1.58 points after three DPO rounds; by rows it is
  separable (p = 0.03), by databases the interval touches zero.
- The gold start gains 1.26 from DPO round 1 (FedAvg R3 gains 3.03, the
  Hinton start 2.38) and ends level with DPO round 1 from FedAvg R3: after
  one DPO round the gold server stage has no lead left, the Hinton one has
  1.40. Gold round 1 has 82 execution errors and 469 wrong results.
- Round 2 repeats it: gold 75.13 against 75.17 from FedAvg R3, Hinton
  76.43 (+1.30). Gold round 2 has 77 execution errors and 457 wrong
  results.

Rejected side of the training pairs, summed over the 5 clients
(`audits/protocol_v2/sqldpo_coder15b_alpha01_s0/*/dpo/round_*/client_*_pairs_stats.json`):

| Line, round | Pairs | Rejected: execution error | Rejected: wrong result |
|---|---:|---:|---:|
| Hinton 1 | 5,393 | 2,806 | 2,587 |
| Hinton 2 | 3,899 | 1,545 | 2,354 |
| Hinton 3 | 3,208 | 1,037 | 2,171 |
| Hinton 4 | 2,870 | 858 | 2,012 |
| FedAvg 1 | 6,509 | 3,824 | 2,685 |
| FedAvg 2 | 4,161 | 1,704 | 2,457 |
| FedAvg 3 | 3,812 | 1,354 | 2,458 |
| gold 1 | 5,794 | 3,063 | 2,731 |
| gold 2 | 4,016 | 1,550 | 2,466 |

- Pairs with an execution error on the rejected side fall by two thirds
  over the rounds (2,806 to 858); pairs with a wrong result fall by a fifth
  (2,587 to 2,012) and are 70% of the pairs by round 4. The DPO rounds
  train on wrong-result pairs every round, yet the clients keep sampling
  them and the wrong-result count on Spider test does not fall.

## 2026-11-11: server went down twice during DPO round 3 from FedAvg R3

No result. Windows System log (owner): unexpected shutdowns at 08:20 and
08:39 (Kernel-Power 41, EventLog 6008), no BugCheck, no planned restart
(1074), no WHEA error, no NVIDIA event near either one; back up at 13:21. One
`nvlddmkm` event 13 at 00:08, while `rft_hinton` trained; that task finished
normally. Task log: vLLM sampling of round 3 finished at 08:19:27 (8,659
prompts); the last line, 08:19:45, starts the execution labeling of client
2, so at the first crash our task ran only SQLite execution on the CPU, with
the GPU idle. The task log has no line after the reboot, so no worker ran at
the second crash. Likely cause outside our task (hardware, power, or other
load on the machine); not confirmed. The worker restart redoes the client 2
labeling, with host RAM watched.

- Event details (owner, only the oldest lines were sent): one more
  unexpected shutdown, before a boot at 14:51 on 11-08, with BugcheckCode 0
  and no power button press, when no queue task ran (first queue commit
  that day at 22:44). A second `nvlddmkm`
  event 13 at 22:27:59 on 11-10 falls on the round 5 sampling crash of the
  Hinton line (`CUDA_ERROR_LAUNCH_FAILED`, round 4 published at 22:15).
  The events do not name the card. Both cards at the default 230 W limit,
  27 C idle.

## 2026-11-11: where the DPO gain comes from, by error type

No run. Read from the committed Spider test predictions (2,147 rows, seed 0,
vLLM inproc), each row counted as right, execution error, or wrong result
(runs but returns another result):

| Row | Right | Execution error | Wrong result |
|---|---:|---:|---:|
| base | 1,243 | 440 | 464 |
| FedAvg R3 | 1,530 | 211 | **406** |
| `hinton_k2aaa_a3` | 1,574 | 129 | 444 |
| + NLL-only round | 1,578 | 117 | 452 |
| + 1 FedAvg SFT round | 1,592 | 132 | 423 |
| + DPO round 3 | 1,647 | 58 | 442 |
| + DPO round 4 | **1,652** | **53** | 442 |
| FedAvg R3 + DPO round 2 | 1,614 | 98 | 435 |

- DPO removes execution errors (129 to 58 from `hinton_k2aaa_a3`, 211 to 98
  from FedAvg R3); SFT and the NLL term alone do not (132, 117).
- The wrong-result count stays between 406 and 464 in every row, from the
  base model to DPO round 4: rows move in and out of it (from
  `hinton_k2aaa_a3` to DPO round 3, 52 wrong results become right, 37 right
  rows become wrong results, 44 execution errors become wrong results), but
  no stage lowers it. About 20% of Spider test is executable SQL with the
  wrong result, and that part is what bounds EX now.
- By hardness, FedAvg R3 to DPO round 3: easy 88.1 to 89.8, medium 74.8 to
  79.8, hard 64.8 to 68.3, extra 49.0 to 63.0.

## 2026-11-11: DPO controls (NLL only, more SFT rounds), DPO round 2 from FedAvg R3

Spider test, seed 0, vLLM inproc (fedicl-sql `0f7d70c6`, `8258e940`,
`62663487`, `d1dc954c`; curve records `dd7c4bf8`, `d7d8f116`). All three
controls start from `hinton_k2aaa_a3` (73.31), as DPO round 1 does (75.69).

| Row | EX | Exec error | Against its start (right only in start / only here) | Against DPO r1 (only here / only in DPO r1) |
|---|---:|---:|---|---|
| NLL-only round 1, same pairs and schedule | 73.50 | 117 | 46 / 50, p = 0.76 | 29 / 76, p < 0.001 |
| +1 FedAvg SFT round | 74.15 | 132 | 32 / 50, p = 0.06 | 53 / 86, p = 0.006 |
| +2 FedAvg SFT rounds | 72.99 | 143 | 59 / 52, p = 0.57 | 53 / 111, p < 0.001 |
| DPO round 1 | **75.69** | **82** | 37 / 88, p < 0.001 | |

- The DPO gain comes from the preference term: with the same samples, pairs
  and schedule, the NLL term alone adds 0.19 point (not separable from the
  start), the full loss 2.38.
- More SFT does not give it either: one more round adds 0.84 (level with
  centralized Spider + BIRD, 73.96), a second one falls back by 1.16
  (54 / 29, p = 0.008). The method row (DPO round 3, 76.71) is 2.56 above
  the best SFT control (51 / 106, p < 0.001).
- Execution errors rise with more SFT (129 at the start, 132, 143) and fall
  with DPO (82).

DPO from FedAvg R3, round 2: **75.17** (round 1 74.29; 17 / 36, p = 0.013;
4,161 pairs, 658 with gold as chosen, 5,532 questions all correct).

| Round | From FedAvg R3 | From `hinton_k2aaa_a3` | Gap | Right only in FedAvg line / only in Hinton line |
|---|---:|---:|---:|---|
| start | 71.26 | 73.31 | 2.05 | |
| 1 | 74.29 | 75.69 | 1.40 | 110 / 140, p = 0.07 |
| 2 | 75.17 | **76.43** | 1.26 | 100 / 127, p = 0.08 |

The server stage keeps about 1.3 points after two DPO rounds, same sign in
both rounds and not separable in either. Round 3 is running.

## 2026-11-11: SQL rows on Spider dev, Realistic, SYN and DK

Seven rows evaluated with vLLM inproc, batch 16 (fedicl-sql `7eaad90a`). No
choice was made on these sets since the fresh start; all four are built on
the 20 Spider dev databases, so they are variants of one set, not four
independent ones. EX:

| Row | Spider test | Dev | Realistic | SYN | DK |
|---|---:|---:|---:|---:|---:|
| FedAvg R3 | 71.26 | 67.89 | 58.86 | 53.77 | 52.15 |
| `gold_k2aaa_a3` | 73.08 | 70.50 | 61.42 | 55.90 | 52.71 |
| `hinton_k2aaa_a3` | 73.31 | 72.82 | 62.01 | 56.67 | 58.13 |
| DPO r1 from FedAvg R3 | 74.29 | 71.18 | 63.39 | 56.67 | 58.13 |
| DPO r1 from Hinton | 75.69 | 75.53 | 62.60 | 59.19 | 62.24 |
| DPO r2 from Hinton | 76.43 | **76.89** | **64.17** | 60.83 | 63.55 |
| DPO r3 from Hinton | **76.71** | 76.50 | **64.17** | **61.03** | **64.11** |

Paired (right only in the first / only in the second):

| Pair | Dev | Realistic | SYN | DK |
|---|---|---|---|---|
| FedAvg R3 / Hinton DPO r3 | 38/127 | 27/54 | 51/126 | 14/78 |
| `hinton_k2aaa_a3` / Hinton DPO r3 | 19/57 | 11/22 | 20/65 | 5/37 |
| FedAvg DPO r1 / Hinton DPO r1 | 49/94 | 40/36 | 68/94 | 24/46 |
| Hinton DPO r1 / r3 | 9/19 | 2/10 | 10/29 | 3/13 |
| Hinton DPO r2 / r3 | 6/2 | 1/1 | 9/11 | 1/4 |

- The method row (Hinton DPO r3) is above FedAvg R3 on every set, by 5.3
  (Realistic) to 12.0 (DK) points, all p < 0.01.
- DPO over its own start holds everywhere except Realistic, where it is
  weaker (+2.17, p = 0.08).
- Rounds 2-3 are flat on every set, as on Spider test.
- The server stage after one DPO round: Hinton above FedAvg on dev, SYN and
  DK (p 0.0002-0.05), level on Realistic (-0.79).
- Sanity: `hinton_k2aaa_a3` on dev gives 72.82 with vLLM, the same as its
  HF number in the archive.
- Not on these sets yet: base model, centralized rows (archived HF numbers
  only, not paired).

## 2026-11-10: worker restarted on GPU 0, seed 1 adapter found

No new result. The owner restarted the worker on GPU 0 with the queue of
fedicl-sql `f2c1e4a7`. `sqldpo_s0/curve_hinton` closed at 23:55 without
sampling or training (`reached the maximum of 4 steps`, record
`audits/curves/sqldpo_s0__hinton_more.json`, fedicl-sql `23e22d36`); the
controls follow in queue order.

- Seed 1: `resolve_parent` on the server found the `hinton_k2aaa_a3` adapter
  of seed 1 (`artifacts/protocol_v2/p253_confirmation_s1/hinton_k2aaa_a3/fedavg_adapter`).
- Round 5 crash (`CUDA error: unspecified launch failure` in vLLM sampling):
  the owner skipped the GPU and log checks, so the cause is not known. If it
  comes back in a later task, the log goes to the agent before a third try.
- `PIPELINE_NEXT.md` has a fixed layout from now on (`AGENTS.md`, "Writing
  `PIPELINE_NEXT.md`"): status, run now, running and queued, reference.

## 2026-11-10: three SQL DPO rounds, fixed; Hinton line stops at round 4

No run. Owner decision: the SQL DPO line from `hinton_k2aaa_a3` stops at
round 4; rounds 5-6 are not run (the partial round 5 samples stay on disk).
Every SQL DPO line and seed (the method row, the gold and FedAvg control
lines, seed 1) runs 3 rounds and is reported at round 3. Round 4 of the
Hinton line is kept only to show saturation. The number was chosen by
looking at Spider test, so it is reported as "chosen on Spider test", never
held-out. Queue: fedicl-sql `f2c1e4a7` (Hinton curve maximum 6 to 4;
`curve_fedavg_more` now runs before `curve_gold`, since whether the BIRD
server stage belongs to the method matters more than the teacher question).

Spider test, seed 0, vLLM inproc; pairs and all-correct questions summed
over the 5 clients (8,659 questions):

| Round | EX | Pairs | All 8 samples correct | All wrong (gold as chosen) | Cosine between client updates |
|---|---:|---:|---:|---:|---|
| start | 73.31 | | | | |
| 1 | 75.69 | 5,393 | 4,820 | 609 | 0.19-0.36 |
| 2 | 76.43 | 3,899 | 5,773 | 534 | 0.04-0.13 |
| 3 | 76.71 | 3,208 | 6,197 | 500 | about 0 to 0.04 |
| 4 | **76.94** | 2,870 | 6,425 | 481 | about 0 to 0.04 |

| Pair | Right only in the earlier / only in the later | p |
|---|---:|---:|
| r1 / r2 | 24 / 40 | 0.06 |
| r2 / r3 | 17 / 23 | 0.43 |
| r3 / r4 | 16 / 21 | 0.51 |
| r2 / r4 | 20 / 31 | 0.16 |
| r1 / r3 | 25 / 47 | 0.013 |
| r1 / r4 | 31 / 58 | 0.006 |
| FedAvg R3 (71.26) / r3 | 76 / 193 | < 0.001 |

- Why 3: round 3 is separable from round 1 (p = 0.013), round 2 is not
  (p = 0.06). Round 4 adds 0.23 point over round 3 that is not separable
  (p = 0.51), and 3 is not the highest point on Spider test.
- Why not more: round 4 counted as a gain under the curve rule by 0.01
  point (0.51 above round 2, 11 rows), so the rule would have run rounds 5
  and 6 (about 3 h) for an expected 0.2 point each, below the noise of one
  paired comparison (about 0.3 point). The private signal keeps shrinking
  (fewer pairs, more all-correct questions, client updates close to
  orthogonal from round 3).
- Cost: each extra fixed round costs about 13 GPU-h over all lines and
  seeds (estimate). The control lines were already queued at exactly 3
  rounds.
- The curve record of the Hinton line names round 4 as the rule's best
  step; the method row is round 3 (76.71).

## 2026-11-10: SQL DPO rounds 3-4 from `hinton_k2aaa_a3`, round 5 crashed

Spider test, vLLM inproc (fedicl-sql `11a139ff`, `7502e90a`, `ce779eaa`,
`45a7d6e6`):

| Round | EX | EM | Easy | Medium | Hard | Extra | Exec error | Pairs (gold chosen) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 75.69 | 65.2 | | | | | 82 | 5,393 (609) |
| 2 | 76.43 | 65.2 | 89.4 | 79.2 | 69.3 | 61.9 | 73 | 3,899 (534) |
| 3 | 76.71 | **65.5** | **89.8** | **79.8** | 68.3 | 63.0 | 58 | 3,208 (500) |
| 4 | **76.94** | 65.0 | 89.2 | 79.5 | **69.3** | **64.7** | **53** | 2,870 (481) |

| Round 4 against | Its EX | Right only there / only in round 4 | p |
|---|---:|---:|---:|
| round 3 | 76.71 | 16 / 21 | 0.51 |
| round 2 | 76.43 | 20 / 31 | 0.16 |
| round 1 | 75.69 | 31 / 58 | 0.006 |
| `hinton_k2aaa_a3` (start) | 73.31 | 40 / 118 | < 0.001 |
| FedAvg R3 + DPO round 1 | 74.29 | 92 / 149 | < 0.001 |
| central Spider + BIRD E3 | 73.96 | 105 / 169 | < 0.001 |

- Round 3 is 0.28 above round 2 (no gain). Round 4 is 0.51 above round 2
  (1,652 against 1,641 rows, 11 rows), a gain by 0.01 point, so round 4 is
  the best step and the curve continues.
- Rounds 2-4 differ by under 0.6 point and no pair of them is separable
  (p 0.16-0.51): the line is flat after round 2, rising by about 0.25 per
  round.
- The private signal keeps shrinking: 6,425 of 8,659 questions have all 8
  samples correct in round 4; sample accuracy 85.7-89.4%.
- Round 5 sampling crashed at 7,168 / 8,659 questions with
  `CUDA_ERROR_LAUNCH_FAILED` after 25 minutes without output (no code
  change since round 4); checks and rerun in `PIPELINE_NEXT.md`.

## 2026-11-10: `hinton_k2aaa_a3` seed 1 approved for reuse

No run. Owner decision: the seed 1 adapter of `hinton_k2aaa_a3` (row
`federated_stage__K2fkl-A-A-A__s1__63d8343d817d__72f0d683`, fedicl-sql
`0704737`, 2026-10-28; same model, split and recipe as seed 0; adapter
`artifacts/protocol_v2/p253_confirmation_s1/hinton_k2aaa_a3/fedavg_adapter`)
may start the seed 1 confirmation. Its presence on the server is not
checked yet (command in `PIPELINE_NEXT.md`). Seed 1 is queued after the
controls fix the number of DPO rounds and the server-stage loss. Missing for
seed 1: FedAvg from the base model (no row on this setup) and `gold_k2aaa`
(only its server stage `p253_gold_k2_k2_s1` exists; reuse not asked).

## 2026-11-10: method review, controls queued, CoT runs dropped

No run. The owner asked for a review of the direction (archive reading
allowed in this session) and approved the queue change.

- Method kept: BIRD server stage, FedAvg SFT, then federated DPO + NLL
  labelled by execution at the clients. The paper's claim rests on the DPO
  stage; it needs the controls below before it stands.
- Open, decided by the controls: the fixed number of DPO rounds; gold or
  Hinton at the server stage (Hinton minus gold is 0.23 point before DPO;
  the teacher zero-shot, 77.22 HF from the archive, is 0.8 point above DPO
  round 2, so it has little left to give on Spider); whether the server
  stage stays in the method (the gap between starts went from 2.05 to 1.40
  after round 1).
- Final table: one fixed number of rounds for every line instead of each
  line's best step, since the method line has more steps to choose from;
  then seed 1 with that configuration.
- BIRD stays an SFT/KD stage before the client rounds. DPO on BIRD at the
  start is not run: its pairs come from a model that three SFT rounds at
  lr 2e-4 then change, and from the base model most chosen sides would be
  the gold SQL. A server DPO step on BIRD inside the client DPO rounds is a
  possible pilot after the controls.
- Dropped: template client rounds 2-3 and CoT DPO. CoT becomes a short
  analysis from the rows that exist.
- Queue (fedicl-sql `80a6a13d`), after the Hinton curve: the rows so far on
  Spider dev, Realistic, SYN and DK; NLL-only round 1 on the Hinton round 1
  samples; 2 more FedAvg SFT rounds from `hinton_k2aaa_a3`; DPO rounds 1-3
  from `gold_k2aaa_a3`; DPO rounds 2-3 from FedAvg R3; BIRD dev for 6 rows.

## 2026-11-10: SQL DPO round 2 from `hinton_k2aaa_a3`

Spider test, vLLM inproc (fedicl-sql `8423c631`, `14b14c22`): **76.43**
(EM 65.2; easy 89.4, medium 79.2, hard 69.3, extra 61.9; execution errors
73).

| Against | Its EX | Right only there / only in round 2 | p |
|---|---:|---:|---:|
| DPO round 1 | 75.69 | 24 / 40 | 0.06 |
| `hinton_k2aaa_a3` (start) | 73.31 | 37 / 104 | < 0.001 |
| FedAvg R3 + DPO round 1 | 74.29 | 96 / 142 | 0.003 |
| FedAvg R3 | 71.26 | 79 / 190 | < 0.001 |
| central Spider + BIRD E3 (no privacy) | 73.96 | 110 / 163 | 0.002 |

- Round 2 adds 0.74 point, a gain under the rule, so the curve continues.
- The private signal shrinks: 3,899 pairs (534 with gold as chosen) against
  5,393 in round 1; 5,773 of 8,659 questions have all 8 samples correct;
  sample accuracy on the clients' questions 82.7-86.9%.
- Client updates are close to orthogonal (pairwise cosine 0.04-0.13).

## 2026-11-10: SQL DPO round 1 from both starts

One federated DPO + NLL round on Spider test, vLLM inproc (fedicl-sql
`97502841` and `cb35d3ec`; curve records `1bdf7440`, `1b7f42c8`). Pairs from
K=8 samples of every client question (8,659), gold as chosen when no sample
is correct.

| Start | Start EX | DPO r1 EX | Right only in start / only in DPO | Pairs (gold chosen) |
|---|---:|---:|---:|---:|
| FedAvg R3 | 71.26 | 74.29 | 61 / 126 | 6,509 (736) |
| `hinton_k2aaa_a3` | 73.31 | **75.69** | 37 / 88 | 5,393 (609) |

- One DPO round adds about 2.4-3.0 points from either start, clearly
  (both sign tests p < 0.001).
- Gap between starts shrinks from 2.05 to 1.40 points after DPO (Hinton DPO
  right only 140 rows, FedAvg DPO 110; p = 0.07): the server stage still
  helps, less clearly.
- Hinton DPO r1 is above centralized Spider + BIRD E3 (73.96, no privacy):
  156 against 119 rows, p = 0.03.
- Memory: no budget was lowered; peak reserved 13.1-17.4 GiB per client.
  Wall clock: Hinton round 1 about 1 h 45 (samples reused), FedAvg round 1
  about 2 h 10 with sampling.

Rounds 2-6 from `hinton_k2aaa_a3` started at 18:13 under the curve rule.

## 2026-11-10: SQL DPO without gradient checkpointing does not fit

Root `hinton_mb` (no checkpointing, micro-batched): client 1 trained at
about 4.5 s per update, but client 2 ran out of memory on one pair of about
1,450 tokens under the 0.88 memory cap. Owner question: the speed-up does
not pay for the failures. Round 1 restarts in root `hinton_gc` with
checkpointing on and micro-batching kept; samples copied again.

## 2026-11-10: SQL DPO round 1 from `hinton_k2aaa_a3` restarted, micro-batched

Round 1 sampling finished in root `hinton` (pass@8 91-94% per client, 5,393
pairs; not committed). DPO training on client 1 used 8.30 GiB at about
10.5 s per update with gradient checkpointing and one pair per pass; the
owner stopped it. Owner decision: train SQL DPO without gradient
checkpointing and pack several pairs per forward pass, with a memory guard
that also holds for heavier (CoT) pairs; restart round 1, keeping only the
samples. Code: `--micro-batch-tokens` (fedicl-sql `a1b22d8b`); the round
reruns in root `hinton_mb` from the copied samples. The update gradient is
unchanged up to padding numerics.

## 2026-11-10: SQL reference rows with vLLM inproc

The reused adapters evaluated again on Spider test with vLLM inproc
(fedicl-sql `4315cee`), next to their archived HF numbers. Every DPO and
reference row from here on is compared on these vLLM rows.

| Row | vLLM inproc | HF (archive) | Exec error | Rows with a different SQL |
|---|---:|---:|---:|---:|
| base | 57.89 | 57.94 | 440 | 188 |
| central Spider E3 | 70.75 | 71.08 | 219 | 161 |
| FedAvg R3 | 71.26 | 71.50 | 211 | 150 |
| `gold_k2aaa_a3` | 73.08 | 73.03 | 144 | 142 |
| `hinton_k2aaa_a3` | 73.31 | 73.50 | **129** | 117 |
| central Spider + BIRD E3 (no privacy) | **73.96** | 73.78 | 163 | 118 |

- Engines agree within 0.33 point on every row, and the order is unchanged.
- The server stage on BIRD adds about 2 points over FedAvg (gold +1.82,
  Hinton +2.05) and has the fewest execution errors.
- FedAvg R3 inproc is 71.26 (the default-mode runs gave 71.45 and 71.22).

## 2026-11-10: method line is SQL DPO from the BIRD server stage; CoT becomes analysis

Owner read the archived results in this session and chose: a method paper
on SQL-only output (BIRD server stage with teacher KD, FedAvg, then
federated DPO + NLL labelled by execution on each client's databases), with
a section on why CoT does not help at 1.5B. Approved reuse of five earlier
adapters as starts and baselines: `hinton_k2aaa_a3`, `gold_k2aaa_a3`,
FedAvg R3 (`fl_aaa`), `central_e3`, `central_mix_e3`.

Readings behind it (archive, Spider test unless noted): every K2 arm 72.6-73.9
against FedAvg 71.50 and centralized Spider 71.08; on Spider dev, SQL DPO
from a converged SFT student +1.45 after 2 rounds (p=.04) and 75.53 after 9;
CoT route `c1` 60.64 to 70.89 against SQL `s1` 58.80 to 74.18 under the same
DPO rounds; Liu et al. (ACL 2025, 6.7B-15B) find CoT DPO above plain SFT by
0.5-0.7 on Spider dev. Gaps between starts shrank under DPO in the archive
(14.8 points to 1.35), so DPO from FedAvg R3 is run at round 1 next to the
Hinton start: it tells whether the server stage still matters after DPO.

Queue (fedicl-sql `5c8469ad`, `b03c15e9`): reference rows with vLLM inproc,
SQL DPO round 1 from both starts, rounds 2-6 from `hinton_k2aaa_a3`, then
template client rounds 2-3 (a curve that continues the stopped client
curve) and CoT DPO from the best template round, up to 3 rounds.

## 2026-11-10: CoT DPO starts from template round 1

Owner reviewed the archived results (allowed in this session): on Spider dev,
centralized, the CoT route `c1` gained less from the same DPO + NLL rounds
than the SQL route `s1` (60.64 to 70.89 against 58.80 to 74.18) despite more
pairs; in the larger-model papers (Liu et al., ExCoT) CoT is what makes DPO
work. The CoT line here has an untested combination, Spider SFT on plans
before federated DPO, so it continues with DPO.

Decision (owner): DPO from the CoT line. Start: template round 1 (62.69,
format valid on every row), not self-taught R2 (60.64); 288 rows right only
in template R1 against 244 only in R2. Fallback: the template plan of the
gold SQL, the style the start was trained on. Queue: fedicl-sql `curve_dpo`
under `dpo_tpl`.

## 2026-11-10: self-taught round 3 falls, curve stopped

Self-taught R3 from R2 (fedicl-sql `6534e5e`, `8395630`, `aece957`): 58.69 EX
on Spider test (EM 33.7; easy 80.0, medium 64.3, hard 43.6, extra 36.7;
invalid format 69, exec error 267, wrong result 551). The curve stops at its
maximum of 3, best step R2 (60.64). Training again on its own outputs from
the previous adapter lowers EX by 1.95 points; STaR restarts from the base
model each iteration for this reason. Worker stopped by the owner before the
queued DPO line.

Reference given by the owner: the untrained base model, SQL-only prompt,
scores 57.94 EX on Spider test (archived row). The CoT line adds 2.7 points
over it at the server (E5) and 2.05 more with one template client round,
while three SQL-only FedAvg rounds from the base model add 13.5 (71.45).

## 2026-11-10: self-taught client rounds 1-2 from E5

Self-taught SFT (own most frequent correct sample, else rationalized from
gold, else dropped), FedAvg weighted by targets, vLLM inproc, Spider test
(fedicl-sql `ffb1d73`, `de6744f`, `d4f7847`, `61ad6ee`), about 2:50 per
round including evaluation:

| | EX | EM | Easy | Medium | Hard | Extra | Invalid format | Exec error | Wrong result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E5 | 60.64 | 24.9 | 77.7 | 68.4 | 43.4 | **42.0** | 48 | 268 | **529** |
| Template R1 | **62.69** | **52.6** | 79.1 | **71.7** | **50.1** | 35.9 | **0** | **207** | 594 |
| Self-taught R1 | 60.08 | 27.4 | 79.1 | 66.0 | 46.7 | 38.1 | 82 | 218 | 557 |
| Self-taught R2 | 60.64 | 30.1 | **79.8** | 66.9 | 47.1 | 38.1 | 63 | 245 | 537 |

- Targets per round: about 83% of questions from the client's own samples,
  15% rationalized, 2% dropped; sample accuracy on client train 55-66%.
  Mean training loss 0.11-0.12 against 0.08 for the template round, whose
  final loss reaches 0.01.
- R2 equals E5 with 241 rows right only in each: the rounds move many answers
  and gain none. Template R1 stays ahead of R2 (288 rows right only in
  template R1, 244 only in R2).
- Format errors rise above E5 (63-82 against 48): the targets keep the
  model's own plan wording, so its format variance stays.
- The curve rule compares steps with each other, not with the start, so R2
  counts as a gain over R1 and round 3 runs.

## 2026-11-10: template client round 1 from E5

One FedAvg round on template plans + gold SQL from E5, vLLM inproc, Spider
test (fedicl-sql `bd1e7af`), 1:53 for the step:

| | EX | Easy | Medium | Hard | Extra | Invalid format | Cut | Exec error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E5 | 60.64 | 77.7 | 68.4 | 43.4 | **42.0** | 48 | 14 | 268 |
| Template R1 | **62.69** | **79.1** | **71.7** | **50.1** | 35.9 | **0** | **0** | **207** |

- +2.05 points: 275 rows right only after the round, 231 only before. Format
  errors and cut outputs vanish (the template is short and fixed), execution
  errors drop by 61, hard rises 6.7 points, extra falls 6.1.
- Still 8.8 points below SQL-only FedAvg R3 (71.45, three rounds from the
  base model).
- Kept as the comparator of the first self-taught round; the curve stops
  here.

## 2026-11-10: self-taught client SFT replaces the template rounds

No result yet. Question (owner): skip client SFT and go straight to DPO from
E5? A literature review (Liu et al. ACL 2025, ExCoT, Iterative RPO,
Struct-SQL, STaR, RFT, Tai et al. 2023) and the E5 outputs argued against:

- E5 is 60.64 on Spider test against 71.45 for SQL-only FedAvg R3; the gap is
  in-domain SQL skill (hard 43.4 against 65.4), not format (48 invalid
  outputs of 2,147). DPO at lr 1e-5 closes it slowly.
- Every Text-to-SQL DPO + CoT paper fine-tunes on CoT first; none tests DPO
  without it.
- The template plan (about 906 characters against 104 for the SQL, 350 of
  them fixed text) restates the SQL clause by clause and overwrites the
  teacher's plan style in one round; as the DPO fallback it pairs template
  text against teacher-style text.

Decision (owner, 2026-11-10): option C. Template client SFT runs one round
from E5 as the comparator; then self-taught SFT rounds: the client's own most
frequent correct sample, else a plan rationalized from the gold SQL (kept if
its SQL is correct, else dropped, as STaR and RFT keep only verified
outputs), client SFT recipe, up to 3 rounds; DPO from the best of them, with
the rationalized response as the fallback chosen side and no pair when it
fails (as Liu et al. drop all-wrong questions). One target per question, so
the self-taught round trains on at most as many rows as the template round.
Code: fedicl-sql f0aa2d7f, queue 9fe240bb.

## 2026-11-09: fedcot server curve stopped, E5 chosen

Teacher-plan SFT on 4,109 BIRD rows from the base model, one epoch per step,
vLLM inproc, Spider test (fedicl-sql `f6e316f3`, `6ccba453`, `4da3ad0c`,
`1667ed2a`, `323286bf`):

| Epoch | EX | Easy | Medium | Hard | Extra | Invalid format | Exec error |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 52.17 | 70.64 | 57.76 | 40.39 | 29.69 | - | - |
| 2 | 56.68 | 74.04 | 63.71 | 41.90 | 36.13 | - | - |
| 3 | 58.55 | 75.74 | 64.41 | **44.28** | 40.34 | 92 | **260** |
| 4 | 59.94 | **78.30** | 66.63 | 44.06 | 40.34 | 52 | 273 |
| 5 | **60.64** | 77.66 | **68.38** | 43.41 | **42.02** | **48** | 268 |
| 6 | 60.20 | - | - | - | - | - | - |

- Gains shrink: 4.51, 1.86, 1.40, 0.70. E5 counts as a gain (rule: more than
  0.5), so the curve runs at least E6.
- E3 to E4 is mostly format: invalid outputs 92 to 52, cut 36 to 17. E4 to E5
  leaves format and execution errors nearly flat; 146 rows right only in E5,
  131 only in E4, so the 0.70 point is the size of the noise (two vLLM runs
  of one adapter flip 90 rows).
- Hard stays at 43-44 since E3.
- E6 60.20, no gain. Decision (owner): server maximum cut from 8 to 6
  epochs, so the curve stops at E6 with E5 as the best epoch instead of
  training E7 only to confirm it (fedicl-sql 47324303). The client rounds
  start from E5.

## 2026-11-09: dips followed by a rise in the archive

Owner question: does the rule miss curves that dip and then rise? The rule
(gain 0.5, patience 2, maxima 8 / 8 / 6) replayed on every archived curve
(Spider dev, pre-restart):

- One dip then a rise, all caught: `tp_r` 68.09, 67.12, 70.60; `c1_rl`
  66.83, 66.25, 67.70 and 69.54, 69.44, 70.89; `s1_rl` 71.08, 70.02, 73.11.
- Two flat steps then a rise, missed: `sql_rl` 74.18, 75.05, 74.95, 74.95
  stops at round 4 with 75.05; the later retry rounds reached 75.53 (0.48
  point, the size of evaluation noise).
- With the DPO maximum of 6, `c1_rl` and `s1_rl` would stop at round 6 with
  69.54 and 71.08, against 70.89 and 74.18 at rounds 8-9. Those rounds
  sampled 1,200 questions each; rounds 1-6 covered the 6,997 eligible
  questions once and rounds 8-9 retried unsolved ones. A fedcot DPO round
  covers every question, so 6 rounds are about six such passes.
- SFT epoch and FL round curves (2-4 steps) had no dip followed by a rise.

Rule unchanged.

## 2026-11-09: vLLM against itself on plan + SQL

1-epoch server stage, Spider test, `fedcot_srv_e1_vllm_inproc` (the server
curve's step 1): EX 52.17, 4.4% cut, about 4.6 min for the whole command.

| Pair | EX | Right only in each | Same SQL |
|---|---|---:|---:|
| vLLM default / vLLM inproc | 51.70 / 52.17 | 40 / 50 | 81.4% |
| HF / vLLM default | 52.86 / 51.70 | 71 / 46 | 76.9% |
| HF / vLLM inproc | 52.86 / 52.17 | 67 / 52 | 76.3% |

- Two vLLM runs that differ only in batch scheduling already flip 90 rows
  and 0.47 point, so long greedy outputs are this sensitive to numerical
  noise; HF against vLLM flips 117-119 rows, a little more.
- The execution-error excess of the default run (28 / 7 against HF) reverses
  against `inproc` (5 / 16): it was part of the noise, not an engine bias.
  HF against `inproc` is 0.69 point, not a clear difference.
- For the curves: a numerically different but equivalent evaluation moves a
  plan + SQL EX by about 0.5 point (90 discordant rows: about 0.44 point
  standard error of the difference), the size of the rule's gain threshold.

## 2026-11-09: plan + SQL with vLLM is 1.16 points below HF; vLLM kept

`vllm_s0/check_cot`, 1-epoch server stage on Spider test: HF 52.86, vLLM
51.70; 71 rows right only with HF, 46 only with vLLM; same SQL on 76.9% of
rows, same raw output on 1,067. Cut outputs (88 / 89), invalid formats
(206 / 208) and median length (278 tokens) match. The gap is execution
errors (285 / 307; among discordant rows 28 / 7), all real SQL errors
(unknown columns or tables, aggregate misuse), and every discordant row has
a different SQL on the two sides, so scoring is not involved. Outputs
diverge about halfway through (median shared prefix 48%): numerical
differences carried through long outputs. SQL-only with the same adapter
type matches (71.50 / 71.45).

Decision (owner): every evaluation of the curves and baselines runs on vLLM
(`inproc`), each number names its engine; HF re-evaluation of the final
table rows stays possible at the end. `check_cot` is now a report.

## 2026-11-09: server epochs and Spider EX in the archive

Owner question: more server epochs on teacher plans may not raise Spider
test EX; read the archived curves for this (Spider dev, pre-restart).

- SQL-only on BIRD gold barely moves Spider at the server stage: base 59.19,
  one cosine over E1 / E2 / E3 49.13 / 58.80 / 58.22; separate K1 / K2 runs
  58.70 and 59.09. Yet gold K2 then three FedAvg rounds reached 70.41 against
  67.60 for FedAvg alone, and K2 halved Spider execution errors (24.5 to 11).
  The server stage helps through what the client rounds build on, not
  through its own Spider EX.
- Teacher CoT on 1,266 BIRD rows (one 4-epoch cosine) rose every epoch:
  54.64, 55.90, 59.57, 60.64.
- A higher server-stage Spider EX did not give the better start: `cot1_e4`
  60.64 above `sql1_e2` 58.80, but SQL SFT on Spider from them gave 70.21 and
  73.60 (output format differs, so not a clean test).

Reading for the server curve: the rule keeps the earliest epoch unless a
later one gains more than 0.5 point, and stops after 2 epochs without a gain,
so a flat curve costs 2 extra epochs (about 2.5 h) and ends at the earliest
epoch. What the archive questions is the selector itself: server-stage
Spider EX ranked starts poorly for the later stages. Rule unchanged for now.

## 2026-11-09: vLLM reruns differ in the default mode

`vllm_s0`: FedAvg R3 on Spider test, HF 71.50, vLLM 71.45 (`check_sql`
passed at 0.5). The same vLLM evaluation run twice gave 71.45 and 71.22, with
the same SQL on 2,009 of 2,147 rows (93.6%); `check_rerun` (0.2 point)
stopped the queue. Cause: vLLM's engine core runs in its own process by
default, so batch composition depends on timing. Change: evaluations run
with the engine core in-process (`--vllm-determinism inproc`), which vLLM
documents as deterministic scheduling for offline runs. Owner: no rerun
check of the fixed mode; the queue goes straight to the main pipeline. The
`inproc` mode is therefore not verified to be repeatable on this server;
vLLM batch invariance is the fallback if a rerun ever differs. Reports in
`audits/protocol_v2/vllm_eval_check_s0/` on the server (not committed).

## 2026-11-09: client rows need gradient checkpointing

`fedcot_s0/client_probe` on the 4 longest client rows (plan + SQL, 2,766-2,921
tokens, all `baseball_1`): with gradient checkpointing 9.25 GiB peak reserved,
1.7 s per step; without it the 2,921-token row ran out of memory at the 0.88
cap. Client and DPO rounds keep gradient checkpointing (`fedicl-sql`
e50d05f4); the no-checkpointing speed-up is dropped. Rerun with gradient
checkpointing only: done, same 9.25 GiB; lengths of the 8,659 client rows
p50 712, p99 2,017, max 2,921 tokens (report
`audits/protocol_v2/fedcot_lengths_s0/client_cot.json` on the server, not
committed).

## 2026-11-09: stopping rule, gain 0.5 point, higher maxima

Decision (owner, after reading the archived pre-restart curves for this
question only, all Spider dev): a gain is now more than 0.5 point over the
best step (was 1 point), patience stays 2, maxima go to 8 server epochs,
8 client rounds and 6 DPO rounds (were 5, 5, 4). In the archive the 1-point
rule cost nothing on SFT epoch and FL round curves, but those curves were
mostly still rising at their last step (3-4 steps), and it stopped two DPO
curves early (by 3.7 and 4.1 points below their later best), whose rounds
rose by 0.5-1.8 points with dips in between; a 0.5-point threshold with
patience 2 caught all of them. Those DPO rounds sampled 1,200 questions
each, so a full-data round may need fewer rounds. Code: per-curve
`min_gain` and `patience` in `scripts/curve.py`; task commands unchanged.

## 2026-11-09: faster pipeline (code, for the next phase)

Decisions (owner: "cập nhật hết"): evaluation moves to vLLM after a check
against HF; the stopping rule runs by itself; client rounds and DPO rounds
drop gradient checkpointing after a memory probe; DPO scores chosen and
rejected in one pass. Code: `scripts.eval_standard --engine vllm`,
`scripts/compare_predictions.py`, `scripts/curve.py` with three curves in the
queue (server, client, DPO), `train_length_probe.py --modes gc nogc`,
`--pair-batch`. Checks before the curves rely on vLLM: FedAvg R3 HF against
vLLM (stop above 0.5 points), vLLM twice (0.2), the 1-epoch server stage HF
against vLLM (0.5). Not run yet; all 583 local tests pass.

## 2026-11-09: server stage, epoch 1 trained

`fedcot_s0/srv_e1` (result row `federated_stage__Kqp-teacher__s0__6f4cfd89be89__48f1b96e`,
commit 94caca4b): 1 epoch on the 4,109 BIRD rows from the base model in
1.14 h, peak reserved 20.3 GiB. Not evaluated yet. The same publish commit
also picked up two older untracked result rows that were on the server
(`federated_stage__A-Kce-Aret__...`, `federated_stage__A-Kgkd__...`); they
belong to the pre-restart work and are not used; removed from Git in
`fedicl-sql` 4ce7bf54 (owner, copies in the local archive).

## 2026-11-09: server epochs as a chain

Decision (owner): the server epochs are probed as a chain, each stage one more
epoch from the last with its own 1-epoch cosine schedule, instead of a
separate run per length. It saves about 1.3 h per extra epoch and can go
past 3 epochs (maximum now 5). An epoch of the chain may score slightly
below a single-schedule run of the same length; the chosen length can be
retrained cleanly once the method is settled.

## 2026-11-09: server max-len for plan + SQL targets

`fedcot_s0/srv_e1` stopped before training: a BIRD row of 7,190 tokens
(6,665 prompt + 525 target) is above `--max-len 7168`. Probe
`lengths_s0/server_cot` (server, report under
`audits/protocol_v2/fedcot_lengths_s0/`): max 7,601 tokens (train:7343,
works_cycles), p99 6,978, 2 rows above 7,168; 2 training steps on each of the
4 longest rows from the base model peaked at 18.8 GiB reserved, 7.2-8.4 s per
step. Decision: server stages at `--max-len 7680`, every row kept, new out
roots `server_l7680_e1`, `server_l7680_e2`.

## 2026-11-09: vLLM sampling matches HF

Run `vllm_s0/bench_sql` (server, not committed): the 400 round-1 questions
of client 3 from FedAvg R3, K=8, T=0.7, through vLLM 0.33 in WSL. Whole task
3:40 against 13:52 with HF; sample accuracy 72.0% and pass@8 89.0% against
71.0% and 88.5% with HF; no output cut at 256 tokens. vLLM needed the
FlashAttention backend and no FlashInfer sampler (no nvcc in WSL). Decision:
DPO rounds sample with vLLM. The first server-stage retry failed on the stage
contract written while the sidecar was CRLF; the server stages now use the
new out roots `server_e1`, `server_e2`.

## 2026-11-09: main pipeline first; full-data DPO with vLLM

Runs: `fedpref_s0/smoke` and the round-1 sampling of the SQL-only DPO line
(400 questions per client, HF, from FedAvg R3) finished; `dpo_r1` was
training. Not committed. `fedcot_s0/srv_e1` and `srv_e2` failed at start:
the plan sidecar was checked out with CRLF on the server, so its hash did not
match (fix in `PIPELINE_NEXT.md`). Measured: HF SQL-only sampling 1.5-2.2 s
per question, peak 18.2 GiB (`A5000_RUN_CONFIG.md`).

Owner decisions: GPU 1 is in use by another user, the work runs on GPU 0;
DPO rounds use every client question; sampling moves to vLLM in the server's
WSL venv, checked first against HF (`vllm_s0/bench_sql`); evaluation may move
to vLLM if it matches HF on FedAvg R3; the server epochs stay a curve; the
stopping rule is to be automated; the SQL-only baselines leave the queue
until the main pipeline has run.

## 2026-11-08: every line run as a curve on Spider test

No run. Owner decision: evaluate each stage on Spider test and continue from
the best checkpoint (stop after 2 steps without a gain of more than 1 point;
maxima: server 3 epochs, client SFT 5 rounds, DPO 4 rounds), the same rule for
the baselines. Queue now holds the server epoch choice (1 and 2 epochs, full
runs) and FedAvg R1-R2 evaluations; the client rounds and the query-plan DPO
rounds are queued after each decision.

## 2026-11-08: full CoT pipeline queued, probe ablations dropped

No run. Owner decision: measure the whole method first and adjust from its
signals. Queue (`PIPELINE_NEXT.md`, phase `fedcot_s0`): server SFT from the
base model on the 4,109 teacher-plan BIRD rows, three FedAvg client rounds on
plans derived from gold SQL, two rounds of federated DPO + NLL on the
clients' own sampled plan + SQL (200 questions per client), Spider test after
round 3 and each DPO round. Dropped: the CoT probe arms, the RFT arm, teacher
headroom and pass@8. Kept as baselines: FedAvg R4-R5 and SQL-only DPO R1-R2
from R3. The pipeline starts from the base model rather than R3 so that the
plan format comes before any federated round and the client rounds match the
baselines (five). New code (nested repo): `--response-format qp_cot_v1` and
`--parent-stage` in `experiments/federated_pref/run.py`; unparsed samples are
rejected as format errors, the gold fallback is the derived plan + gold SQL.

## 2026-11-07: Spider test becomes the Spider metric; queue revised after a review

No run. Owner decisions: every Spider number is Spider test from now on;
Spider dev is skipped or a secondary diagnostic (rule in both `AGENTS.md`).
Choices are made on Spider test, so it is not called held-out. One seed for
this signal round. The owner wants one feasible CoT-with-teacher test.

An independent review (owner-allowed archive reading) recommended SQL-only
federated DPO + NLL as the main line and judged the archived CoT routes weaker
evidence than first stated (best-on-dev selection, matched rounds only -1.55,
no isolated prompt-format test). Accepted: the sample label note in
`DIRECTION.md` now matches the code (EX on the client's original database
only, no test-suite variants for Spider train).

Queue (`fedicl-sql/queues/active.toml`, `PIPELINE_NEXT.md`): every evaluation
on Spider test and BIRD dev; teacher headroom on Spider test (R3 71.50); R3
pass@8 stays on Spider dev as a diagnostic; an SFT round 5 control so the SFT
rounds match DPO round 2; the CoT probe now chains each server stage (teacher
plan, plan from SQL, SQL only) into one client round in the same format and
evaluates only after the client round. New code: `--parent-stage` in
`experiments/federated/run.py` resolves a committed stage row by its stage
name (nested repo, with a test).

## 2026-11-07: queue 2 written (headroom check, CoT probe server side)

No run. `PIPELINE_NEXT.md` queue 2: teacher 4-bit greedy and R3 pass@8 on
Spider dev; three server SFT stages from R3 on the 4,109 teacher-plan BIRD rows
(teacher plan, plan derived from the SQL, SQL only); one client round with
gold-derived plans. New code: `scripts/pass_at_k.py`; `scripts.eval_standard`
gained `--model-4bit` and `--response-format`. The round-1 publish step now
fast-forwards before pushing.

## 2026-11-07: CoT design for S5

No run. Owner accepts CoT at inference if the cost is feasible. Literature
(`LITERATURE.md` 1.7): on Spider greedy, CoT SFT alone stays below SQL-only and
leads only after execution-labelled DPO. Chosen design (`DIRECTION.md` 6.5):
structured query plan (`qp_cot_v1`, 512-token cap) from the existing 4,109
teacher plans on BIRD, one prompt for server SFT, client sampling and eval,
clients train on CoT too. Probe of 7 arms, about 20 GPU-h (`DIRECTION.md` 6.3).

## 2026-11-07: direction note reorganized, server options ranked

No run. `DIRECTION.md` rewritten as client choice (C1-C4) + server option
(S0-S5) + timing; owner allowed SynSQL as server data. A literature pass
(`LITERATURE.md` section 1.7) found no evidence that SQL-only KD or RL on public
data adds 2+ points greedy Spider EX once the student has seen Spider; CoT (S5)
with client execution training has the strongest support. Proposed order:
teacher headroom and R3 pass@8 on Spider dev (about 2 GPU-h), then an S5 probe
if CoT at inference is accepted, then a KD probe on SynSQL if the teacher is
4+ points above R3. Proposed drops: S3 on SynSQL, S4. Also noted: FedAvg R3 is
3.8 points below centralized SFT on Spider dev (67.60 vs 71.37), level on test.

## 2026-11-07: next direction, a server step on public BIRD

No run. Proposal recorded in `DIRECTION.md` section 8, to follow the Direction
1 verification: the server adds knowledge the clients lack, using what only it
has. Main option: on-policy KD from the frozen teacher on BIRD, gated to
questions where the teacher SQL matches gold; fallback: execution RL/DPO on
BIRD. Teacher is not used to correct student SQL (it matches gold on 56% of
BIRD train, and the server has gold). Placement: one server stage before the
client rounds first (E1, server side only from FedAvg R3), then after each
aggregation if E1 raises Spider dev. `LITERATURE.md` gained section 1.6
(clause- and token-level preference and RL, SQLoom read in full) and FedAuto.

## 2026-11-06: federated DPO + NLL pipeline, FedAvg reference reused

No run yet. Owner decisions: Direction 1 (federated on-policy DPO + NLL, no
teacher) first; reuse the earlier FedAvg SFT run `p227_fl_aaa_s0` (seed 0,
code SHA 3582656, 3 rounds, 1 local epoch) as the federated baseline and the
start point. Its recorded EX (earlier run, owner-approved reference): Spider
dev 67.60 (R3; R2 68.28), Spider test 71.50 (R3, one reference pass, no choice
made on it), BIRD dev 25.68 (R3); centralized SFT e3 71.37 dev, 71.08 test.

New code in `fedicl-sql`: on-policy sampling with execution labels,
preference pairs, a resumable DPO + NLL trainer with an RFT weight, a
federated round runner (`experiments/federated_pref/run.py`), a standard
evaluation runner and contract (`scripts/eval_standard.py`) and a test-suite
EX scorer. Sampling, prompt, decoding budget and DPO schedule follow the
earlier SQL-only DPO rounds; the prompt equals the evaluation prompt. A local
end-to-end smoke (2 clients, 3 questions) passed on the Mac. Queued in
`PIPELINE_NEXT.md`: GPU smoke, rounds 1-2 of DPO and RFT from FedAvg R3, one
more FedAvg SFT round as a control, evaluation on Spider dev and BIRD dev.

## 2026-11-06: literature review and direction proposals

No run. New `LITERATURE.md` lists the closest verified work (federated
learning with a server LLM, federated Text-to-SQL and code, federated DPO and
RLVR, small-model Text-to-SQL training, LLM-to-SLM distillation) and the gaps
for our setup. New `DIRECTION.md` proposes four directions, revised after one
round of independent Q3-reviewer critique, and recommends iterative federated
DPO with execution-labelled pairs built at each client (no teacher), with
teacher CoT plus federated DPO as the choice if the teacher must contribute.
Owner input used: client drift is negligible and DPO is effective in this
setup (earlier observations, to be re-measured). Waiting for the owner to
choose a direction and to settle whether the teacher is optional
(`RESEARCH_STATE.md`) or required (`AGENTS.md`).

## 2026-11-06: teacher becomes optional

Owner decision: the goal is a method that clearly beats the federated
baselines on the clients' domain. Using the server teacher is an option, not
a requirement; a method without it is acceptable if it is strong enough. If
the teacher is used, it still runs only at the server on public data.

## 2026-11-06: reuse of earlier outputs, storage, checkpoints, progress

Owner decision: teacher outputs on BIRD (SQL targets, logit cache, checked
CoT) and processed data may be reused freely; starting from an earlier
adapter or comparing with an earlier result needs the owner's approval;
earlier interpretations and result numbers stay hidden. Teacher outputs on
Spider train are excluded because Spider train is client data. New
`fedicl-sql/docs/SERVER_STORAGE.md` lists the reusable assets and sets the
rules for server storage (never delete or overwrite `artifacts/`), resume by
rerun, and progress output for long jobs.

## 2026-11-06: lighter process rules

Owner found the inherited process rules too rigid. `AGENTS.md` now separates
a short list of hard rules (honesty, data roles, GPU memory budget, evaluator
budgets, server checkout safety, no weights in Git, Git identity) from
defaults that may be skipped when another way is simpler. `CONVENTION.MD` was
cut to the repository layout and the essentials; the full earlier versions
are in `archive/paper/fresh_start_2026-11-05/`.

## 2026-11-05: fresh start

Owner decision: archive every earlier decision, result and literature note so
that new work is not bound by them. Kept: the topic, the fixed setup
(`RESEARCH_STATE.md` section 2), the Q3 goal (the measurable-teacher part
was dropped on 2026-11-06), the honesty rules, and the infrastructure and Git rules. Open:
method and metrics. Archived material is hidden unless the owner asks for it
in a session.
