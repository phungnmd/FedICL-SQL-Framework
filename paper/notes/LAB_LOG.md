# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

## 2026-11-15: seed 2 dropped; F1 and 3-round vote labels after P1

Owner drops seed 2 from the plan. Last seed 2 results, Spider test, vLLM
inproc: Hinton server stage then FedAvg R3 (`sql_hinton_k2aaa_a3_s2`) 74.24
(curve `4b9edfdd`), DPO round 1 from it 75.87 (`cbafef0b`, 86 execution
errors). Rounds 2-3 of that line and the seed 2 gold and FedAvg lines are
removed from the queue (fedicl-sql `554b7f98`); finished outputs stay on the
server. The main lines keep 2 seeds, so the teacher-versus-gold comparison
stays at +1.49 / +0.47 (seed 0 / seed 1).

Owner approves F1 (20 clients, full and partial participation) and DPO with
result-vote labels for 3 rounds, to be queued after the P1 result. Checked
locally for F1, nothing committed: `scripts.build_federated` with 20
clients, alpha 0.1, the same domain groups and the 150-row floor of `k5`
gives no split within the default 100 draws (smallest client 16 rows); with
5,000 draws it does (clients 165 to 1,015 rows). Partial participation is
not in the FedAvg or DPO round code yet.

## 2026-11-14: P1 (codes schema) approved and first in the queue

Owner approved P1 and put it ahead of the rest of the queue. Phase
`sqlcodes_s0`: the FedAvg line of seed 0 with the `codes` schema (CodeS
metadata: type, primary key, column comment, 2 sample values per column,
foreign keys, and the values the question quotes) in every training,
sampling and evaluation prompt. 3 FedAvg rounds from the base model, then
3 DPO + NLL rounds with the `sqldpo_s0/fedavg` recipe; Spider test only.
Comparator: `sqldpo_s0/fedavg` (same seed, `full` schema). Code and queue:
`8e3247ce`, `d7095e42` (fedicl-sql); full `pytest -q`, 633 passed.

Prompt measurements (Qwen2.5-Coder tokenizer, chat template, local):

| Set | `full` mean / max tokens | `codes` mean / max tokens |
|---|---|---|
| clients 1-5 (8,659 rows) | 572 / 2,259 | 996 / 7,297 |
| Spider test (2,147) | 418 / 1,140 | 677 / 2,053 |

Client training tokens grow about 1.74x, mostly client 3. The 82 client 3
rows on `baseball_1` render 7,224 to 7,432 tokens with the gold SQL, so the
line uses `--max-len 7680` (fits all 2,061 client 3 rows; SFT at 7,680 was
measured at 20.3 GiB). No other row is above 3,700 tokens.

Two code fixes before queuing. The value matcher of `codes` found a value
anywhere inside the question, so short codes ('M', 'Y', 'THE') matched in
most questions (999 of 1,896 client 1 questions); it now needs whole words,
and values under 4 characters must match the case (575 of 1,896).
`scripts.eval_standard` takes `--schema-style` (default unchanged). No
result in use was rendered with `codes`.

Not measured: DPO memory for `baseball_1` pairs (about 7,550 tokens a
sequence; the pair takes one forward pass of two rows, above the 8,192
budget). The trainer stops above 21.5 GiB, so a failure shows as a clear
stop. Estimate about 16 h (SFT about 8.5 h, DPO about 7.5 h, scaled from
seed 2 FedAvg rounds and `sqldpo_s0/curve_fedavg` by token count).

## 2026-11-14: N2 label sources and N3 seed 1 selection

Pulled code/results through `d4c215ce` (published at 10:02,
Asia/Ho_Chi_Minh). Spider test, 2,147 questions, vLLM inproc, batch 16.

N2, seed 0, one DPO round from `hinton_k2aaa_a3` on the Hinton line's
round-1 samples, every client question, no gold fallback. V labels a sample
by result vote among the 8 samples; X labels executable SQL as chosen and
execution errors as rejected. Neither reads gold SQL. Results: V `5bdb7afa`,
`f03e2ac3`; X `4bf30a6a`, `c0cc12ed`. Paired counts against
`sqldpo_hinton_r1_vllm_inproc` (gold labels with fallback), exact two-sided
binomial test on discordant questions.

| Round 1 labels | Pairs | EX | Right only here / only gold labels | Exact paired p | Execution errors |
|---|---:|---:|---|---:|---:|
| gold, with fallback (Hinton line) | 5,393 | **75.69** | - | - | 82 |
| gold, no fallback | 4,784 | 75.50 | 15 / 19 | 0.61 | 75 |
| result vote (V) | 5,670 | 75.50 | 35 / 39 | 0.73 | 69 |
| executability (X) | 3,497 | 74.99 | 31 / 46 | 0.11 | **68** |

Start model `hinton_k2aaa_a3`: 73.31. V matches gold labels without
fallback in EX at round 1, and changes more questions in both directions.
X keeps most of the round-1 gain (+1.68 over the start) with 35% fewer
pairs; all its rejected samples are execution errors, so it cannot teach
wrong-result cases. One round only: whether V holds over three on-policy
rounds is not measured (about 3.5 h for V alone).

N3, selection by execution over 8 samples (T 0.7), seed 1, all Spider test
questions; seed 0 from earlier commits. Result: `d4c215ce`.

| Model | Seed | Greedy | Fallback | Vote | pass@8 |
|---|---:|---:|---:|---:|---:|
| FedAvg R3 | 0 | 71.26 | 75.03 | 75.55 | 83.47 |
| FedAvg R3 | 1 | 71.87 | 76.01 | 75.87 | 83.70 |
| `hinton_k2aaa_a3` | 0 | 73.31 | 75.59 | 76.53 | 84.68 |
| `hinton_k2aaa_a3` | 1 | 74.06 | 76.39 | 76.34 | 84.49 |
| DPO R3 from FedAvg R3 | 0 | 75.13 | 77.04 | 76.76 | 84.86 |
| DPO R3 from FedAvg R3 | 1 | 75.83 | 77.69 | **78.39** | **85.19** |
| DPO R3 from `hinton_k2aaa_a3` | 0 | 76.71 | 77.69 | **78.39** | 85.00 |
| DPO R3 from `hinton_k2aaa_a3` | 1 | **77.04** | **78.16** | 78.02 | 84.96 |

Seed 1 repeats seed 0's ordering for greedy and fallback: selection adds
1.0 to 4.1 points, more for weaker models. The Hinton start's lead over
FedAvg R3 as DPO start is 1.58 / 1.21 greedy and 0.65 / 0.47 with fallback
(seed 0 / seed 1); with vote it is +1.63 on seed 0 and -0.37 on seed 1. At
inference with 8 samples, the server stage's contribution is small and not
consistent across seeds. Seed 2 is queued next (`sqldpo_s2/hinton_k2`);
its live state is unconfirmed.

## 2026-11-14: fixed round-1 samples lose ground over repeated DPO rounds

Pulled code/results through `3767d097` (curve published at 06:36,
Asia/Ho_Chi_Minh). Offline DPO from `hinton_k2aaa_a3`, seed 0: all five
clients, all client questions, two local epochs per round, three rounds.
Every round uses the Hinton line's round-1 samples and the same 5,393
pairs; no new sampling. Spider test, 2,147 questions, vLLM inproc, batch 16.
Round results: `5723ab7f`, `a9359bb9`, `b7a2d132`; the corresponding training
records are in `hinton_offline/dpo/round_1` to `round_3` under
`audits/protocol_v2/sqldpo_coder15b_alpha01_s0/`.

| Round | Resample each round | Fixed round-1 samples | Right only with resampling / fixed samples | Exact paired p | Execution errors, resampling / fixed |
|---|---:|---:|---|---:|---|
| 1 | 75.69 | 75.69 | 8 / 8 | 1.00 | 82 / 82 |
| 2 | 76.43 | 75.55 | 61 / 42 | 0.076 | 73 / 80 |
| 3 | **76.71** | 74.99 | 101 / 64 | 0.0049 | 58 / 94 |

Paired counts recomputed from committed prediction files with
`scripts.compare_predictions`; arm pairs `sqldpo_hinton_r{1,2,3}_vllm_inproc`
vs `sqloffline_hinton_r{1,2,3}_vllm_inproc`, set `spider_test`. Exact p is
the two-sided binomial test on discordant questions. Round 1 matches in EX,
but 119 SQL predictions differ and 16 questions change correctness.

| Round | Pairs, resampling / fixed | Optimizer updates, resampling / fixed |
|---|---|---|
| 1 | 5,393 / 5,393 | 680 / 680 |
| 2 | 3,899 / 5,393 | 490 / 680 |
| 3 | 3,208 / 5,393 | 406 / 680 |

Offline round 3 is 1.72 points below on-policy round 3, despite more
updates, and 0.70 below its own first round. The full sample-refresh recipe
has a measured role; this control does not match the number of updates.
The current method and queue stay unchanged. Offline has finished; next in
queue order is `sqldpo_s0/curve_vote_labels`, followed by executability
labels and seed 1 selection. Their live state is unconfirmed.

## 2026-11-14: N2/N3 code published

Owner explicitly approves the code push. Commit `cfa2791c` pushed to
`phungnmd/fedicl-sql` main at about 02:52 (Asia/Ho_Chi_Minh).
`PIPELINE_NEXT.md` now gives the pull/test/resume steps. Server pull and live
GPU state remain unconfirmed; no GPU task was started from this session.

## 2026-11-14: N2/N3 approved; venue candidates CMC or JIIS

Owner approves N2 and N3 after `sqldpo_s0/curve_offline`, before seed 2.
Code and queue: `cfa2791`. Verification: full `uv run pytest -q`, 631
passed; changed Python files pass Ruff, `git diff --check` is clean.
Independent code review found no blocking issue. The code push was blocked
by automatic approval review: existing origin is
`https://github.com/phungnmd/fedicl-sql.git`, but the review requires explicit
approval to export this private payload there. The owner later approved the
push; publication is recorded above.
Implemented two separate one-round DPO curves on every client's round-1
samples: `sqldpo_s0/curve_vote_labels` (V) and `curve_exec_labels` (X).
`--pair-label vote|exec --no-gold-fallback` re-executes EOS SQL at the 60 s
budget, ignoring gold SQL and cached gold outcomes. V uses inference vote's
multiset grouping and tie rule; X uses executable SQL vs execution errors.
Per-question label caches resume, with source hashes and mode in the
published stats; existing gold-label identities are unchanged. The old
cache lacks raw response text for some candidates, so their parsed-SQL
targets are marked and counted by question, candidate and pair occurrence.
Pair counts and update counts can differ; the training recipe is unchanged.

N3 adds four seed 1 selection tasks (`sqldpo_s1/xsel_*`) and publication;
seed 2 Hinton now depends on `sqldpo_s1/publish_xsel`. About 4.5 GPU-h added:
3.5 h for N2 and 1 h for N3, estimates. N2 is a one-round label-source
ablation, not the method's final three-round result; both variants for
3 rounds would cost about 10.5 h. No GPU run in this session.

F1 and P1 need explanation before approval; neither is queued. Code
inspection corrects P1's premise: `full` already contains PK/FK; `codes`
changes schema representation and adds sample values. F1 from the existing
5-client SFT adapter tests DPO after repartition, not a complete 20-client
pipeline; retraining SFT adds an estimated 5 h. At 25% participation the
number of client updates is lower, so the comparison must report exposure.

CMC (Computers, Materials & Continua) or JIIS are now the main venue
candidates. CMC's author instructions were opened on 2026-11-14: template
LaTeX available, references Vancouver, end matter and disclosure requirements
recorded in the proposal. Research state updated with the already committed
3-round no-NLL result (76.76 vs 76.71 on Spider test, seed 0), replacing the
stale pending status; no change to the chosen method. The completed advisor
report was removed in concurrent paper commit `83651b7`, which also updates
`LITERATURE.md`; that literature edit is outside this change.

## 2026-11-14: selection by execution: a vote matches DPO greedy in total, not by question, and adds 1.68 on top of the method

Spider test, seed 0, vLLM inproc, 8 samples per question at T 0.7
(fedicl-sql `44b51ef5`, 01:19). No training. Fallback: the greedy SQL when
it executes, else the most frequent sample that executes. Vote: the most
frequent result among the samples that execute. Paired counts computed from
the committed `per_question.csv` files (sign test).

| Row | Greedy | Fallback | Vote | pass@8 | Model calls, fallback |
|---|---:|---:|---:|---:|---:|
| FedAvg R3 | 71.26 | 75.03 | 75.55 | 83.47 | 1.79 |
| `hinton_k2aaa_a3` | 73.31 | 75.59 | 76.53 | 84.68 | 1.48 |
| DPO round 3 from FedAvg R3 | 75.13 | 77.04 | 76.76 | 84.86 | 1.38 |
| DPO round 3 from `hinton_k2aaa_a3` (the method) | 76.71 | 77.69 | **78.39** | **85.00** | 1.22 |

| Pair | Gain | Right only in first / second | p |
|---|---:|---|---:|
| vote on `hinton_k2aaa_a3` / method greedy | +0.19 | 73 / 77 | 0.81 |
| vote on FedAvg R3 / its DPO round 3 greedy | -0.42 | 97 / 88 | 0.56 |
| method greedy / method vote | +1.68 | 27 / 63 | < 0.001 |
| vote on `hinton_k2aaa_a3` / method vote | +1.86 | 36 / 76 | < 0.001 |
| vote on FedAvg R3 / vote on its DPO round 3 | +1.21 | 57 / 83 | 0.03 |
| vote on FedAvg R3 / method vote | +2.84 | 75 / 136 | < 0.001 |
| vote on DPO from FedAvg R3 / method vote | +1.63 | 78 / 113 | 0.01 |

Test questions grouped by the 8 samples of the start (right answers, greedy):

| Group (from the start's samples) | FedAvg R3: n | start | DPO r3 | `hinton_k2aaa_a3`: n | start | DPO r3 |
|---|---:|---:|---:|---:|---:|---:|
| vote right | 1,622 | 1,495 | 1,525 | 1,643 | 1,540 | 1,570 |
| vote wrong, some sample right | 171 | 26 | 58 | 175 | 31 | 64 |
| no sample right | 354 | 9 | 30 | 329 | 3 | 13 |

- In total a vote on the start reaches what DPO round 3 reaches greedily
  (prediction 1 of the hypothesis), but not on the same questions: the two
  differ on 150 (Hinton) and 185 (FedAvg) questions, and of the questions
  DPO gains, only 55% (61 of 110) and 56% (80 of 142) were right under the
  start's vote. More than half of DPO's net gain is on questions where the
  start's vote was wrong (Hinton: +30 where the vote was right, +33 where a
  minority sample was right, +10 where no sample was). DPO with gold labels
  is not only the vote moved into the weights.
- The two add up: a vote on the method gives 78.39, +1.68 over its greedy
  output. At the same inference cost (8 samples and a vote) the method is
  2.84 above FedAvg R3 and the DPO stage adds 1.86 (Hinton) and 1.21
  (FedAvg), about half of its greedy gain (3.40, 3.87). The server stage
  keeps 1.63 under the vote after DPO (greedy: 1.58).
- pass@8 barely moves (83.47 to 85.00): DPO does not add correct candidates,
  it changes which one comes first. Of the method's 442 wrong results, 154
  have a correct sample among the 8 and the vote recovers 43; 288 have
  none. A correct sample exists and the vote misses it on 142 questions
  (6.6 points).
- The fallback rule alone costs 1.2 to 1.8 model calls per question and
  gives +0.98 on the method, +3.77 on FedAvg R3.
- One seed, Spider test only (the cut named when queued).

## 2026-11-14: probes of the DPO stage moved ahead of seed 2

Owner (00:50): check what the DPO stage does before running further. Queue
(fedicl-sql `05d0e885`): selection by execution over 8 samples (four seed 0
rows) and the offline rounds now run before the seed 2 lines; no task
changed. Hypothesis to test with them: DPO turns what execution-based
self-consistency reaches over 8 samples into greedy EX. Predictions:
`hinton_k2aaa_a3` + vote close to DPO round 3 greedy; DPO's gained
questions mostly those the start's vote already gets right; little gain
from a vote on top of DPO round 3; DPO on vote labels (no gold) close to
DPO on gold labels (not queued, new code).

Test-suite EX on Spider dev, seed 0, vLLM inproc (CPU scoring, not
committed): FedAvg R3 67.89 EX / 62.67 TS, its DPO round 3 73.11 / 67.89;
`hinton_k2aaa_a3` 72.82 / 67.70, its DPO round 3 76.50 / 70.41. DPO gains
the same under test-suite from FedAvg R3 (+5.22 both), and about 1 point
less from `hinton_k2aaa_a3` (+3.68 EX, +2.71 TS; rows right only by EX 53
to 63). False positives of the execution check are a small part of the
gain on Spider dev.

## 2026-11-14: DPO rounds 2-3 without the NLL term: 76.76 at round 3, level with DPO + NLL

Spider test, seed 0, vLLM inproc, batch 16 (fedicl-sql `d3d56604`,
`b59b9023`, `a4d9369b`, `916e612d`; curve record `7927a7a6`). From
`hinton_k2aaa_a3`, NLL weight 0; round 1 is the earlier row on the Hinton
line's round 1 samples, rounds 2-3 sample from the previous round of this
line. Otherwise the Hinton line's settings.

| Round | DPO + NLL | No NLL | Right only with / without NLL | p |
|---|---:|---:|---|---:|
| 1 | 75.69 | 76.20 | 23 / 34 | 0.19 |
| 2 | 76.43 | 76.67 | 32 / 37 | 0.55 |
| 3 | 76.71 | 76.76 | 31 / 32 | 0.90 |

| Round 3 | EX | Execution error | Easy | Medium | Hard | Extra |
|---|---:|---:|---:|---:|---:|---:|
| DPO + NLL | 76.71 | **58** | 89.8 | 79.8 | 68.2 | **63.0** |
| No NLL | **76.76** | 68 | **90.0** | 79.8 | **69.5** | 61.3 |

Own samples on the client questions (sample accuracy by client, %):

| Round | DPO + NLL | No NLL | Pairs (NLL / no NLL) |
|---|---|---|---|
| 2 | 83.9, 83.9, 82.7, 85.0, 86.9 | 84.2, 84.4, 83.0, 85.1, 87.2 | 3,899 / 3,705 |
| 3 | 86.2, 87.6, 84.4, 86.8, 88.4 | 86.2, 87.8, 84.9, 86.8, 88.9 | 3,208 / 2,969 |

- Over 3 rounds the NLL term has no measured role: the two lines are level
  at every round (p 0.19 to 0.90), and at round 3 they differ on 63
  questions, split 31 / 32.
- No sign of the drift the term is meant to prevent: without it, the
  model's own samples on the client questions are as accurate or slightly
  more accurate in each round, with fewer pairs rejected for execution
  errors (923 against 1,037 in round 3). On Spider test the line without NLL
  has 10 more execution errors at round 3 (68 against 58), offset by fewer
  wrong results. The chosen side's log-likelihood is not logged, so the
  drift is read from samples only.
- The term costs no extra compute (same forward pass), so dropping it only
  simplifies the method. The DPO + NLL comparisons already run (seeds 0 and
  1, teacher against gold and FedAvg) all use the term; switching the method
  would need those lines again without it. No decision.

Run time: rounds 2 and 3 with their own sampling and evaluation, 1 h 29
and 1 h 20 (21:11 to 00:00).

## 2026-11-13: DPO round 1 without the gold fallback: 75.50, level with the fallback

Spider test, seed 0, vLLM inproc, batch 16 (fedicl-sql `e895c642`,
`96373824`; curve record `fbd1beb1`). DPO + NLL round 1 from
`hinton_k2aaa_a3` on the Hinton line's round 1 samples; a question with no
correct sample gives no pair (4,784 pairs, 609 gold-chosen pairs left out).

| Row | EX | Execution error | Hard | Extra |
|---|---:|---:|---:|---:|
| DPO + NLL round 1 | **75.69** | 82 | **66.7** | **61.1** |
| no gold fallback | 75.50 | **75** | 66.5 | 60.5 |

Paired: 19 questions right only with the fallback, 15 only without
(p 0.49). In round 1 the gold fallback has no measured role. Rounds 2-3 not
run (gold-chosen pairs are 11.3, 13.7 and 15.6% of the Hinton line's pairs in
rounds 1-3).

Run time: 1 h 51 (19:20 to 21:11).

## 2026-11-13: seed 2, selection by execution and baseline rows queued

Owner decisions (evening of 11-13): yes to a third seed of the three DPO
lines, with its Hinton and gold lines ahead of the offline and centralized
rows; yes to selection by execution at inference (N1); the earlier seed 0
FedProx R3, FedNTD and local client SFT adapters approved for reuse as
baselines, evaluation only (`fedicl-sql/docs/SERVER_STORAGE.md` section 5).

Queued (fedicl-sql `40b9edb5`), in this order after the no-NLL rounds 2-3:
seed 2 Hinton line, seed 2 gold line (both server stages trained anew from
the base model with the seed 0 recipe and `--seed 2`; the teacher logit
cache is reused, it does not depend on the seed), N1 on four seed 0 rows,
the 7B teacher zero-shot through vLLM (bf16) on the six sets, FedProx and
FedNTD on the six sets, the 5 local client models on Spider test, then the
offline and centralized rows, then the seed 2 FedAvg line (about 59 h on
GPU 0, estimate).

New code (fedicl-sql `dcf73bd0`): `scripts/exec_select.py` with
`fedicl_sql/eval/exec_select.py`. It samples K = 8 SQL per question through
vLLM with the DPO sampling settings and scores two rules that never read the
gold SQL: keep the greedy SQL when it executes, else take the most frequent
sample that executes; or vote over the executable samples grouped by their
result rows. The greedy column is the committed vLLM inproc row of the same
adapter. 623 tests pass on the Mac.

Cut: the local client models run on Spider test only (their six-set rows
would add about 2.5 h); N1 is seed 0 and Spider test only.

## 2026-11-13: client adapters of DPO round 1 before aggregation

Seed 0, vLLM inproc, batch 16, Spider test (fedicl-sql `f456678c`). The 5
client adapters of DPO round 1 of the Hinton line, each evaluated alone,
against the averaged round 1 adapter:

| Client | 1 | 2 | 3 | 4 | 5 | mean | averaged |
|---|---:|---:|---:|---:|---:|---:|---:|
| EX | 75.36 | 75.50 | 74.66 | 74.24 | 75.08 | 74.97 | **75.69** |

Every client adapter is below the averaged one (by 0.19 to 1.45); in round
1 averaging adds 0.72 point over the mean client adapter.

## 2026-11-13: roles of the method's parts and two reference rows queued

No result yet. Owner request: queue the runs that give each part of the
DPO stage a measured role, and the reference rows a federated-learning
reviewer will ask for. Seed 0, from `hinton_k2aaa_a3`, the Hinton line's
settings unless named (about 16 h on GPU 0, estimate):

- the 5 client adapters of DPO round 1 of the Hinton line, before
  aggregation, on Spider test (what averaging adds in round 1; no training);
- DPO round 1 without the gold fallback (609 of 5,393 pairs dropped);
- rounds 2-3 of the line without the NLL term, each with its own sampling;
- rounds 1-3 trained on the round 1 samples only (offline against
  on-policy rounds); round 1 repeats Hinton round 1, so it also shows how
  much one training rerun moves EX;
- centralized DPO: the same recipe on the pooled client rows, one model, 3
  rounds with their own sampling (a reference without privacy).

New code (fedicl-sql): `--samples-from-round N` (rounds after N train on
round N's samples; recorded in the arm identity) and `--pooled` with
`--n-clients 1` (one client reads `train.csv`; its adapter is copied as the
round's adapter, no averaging). Identities of existing roots are unchanged
(the new fields are left out when unset); 618 tests pass on the Mac.

Cut: the line without aggregation is round 1 only (3 rounds need sampling
from each client's own model, new code, about 6 h). Not queued: FedProx,
FedNTD and local client SFT rows, whose earlier adapters are not approved
for reuse (owner decision: approve them or train anew).

## 2026-11-13: soft-target control: DPO from the virtual-teacher start ends with the gold line

Seed 0, vLLM inproc, batch 16 (fedicl-sql: start `1d56507e`, rounds
`87c2d835` to `9a184a28`, other sets `c23b696b`; `self_k2aaa_a3`
`c09d1aad`). DPO rounds 1-3 from `virtual_k2aaa_a3` (the Hinton loss on BIRD
with a virtual teacher: gold token 0.73, the rest uniform; then 3 FedAvg
rounds), settings of the Hinton and gold lines. Paired counts and intervals
computed from the committed predictions (bootstrap over the test databases).

Spider test:

| Round | Gold line | Virtual line | Hinton line | Hinton minus virtual |
|---|---:|---:|---:|---:|
| start | 73.08 | 72.57 | 73.31 | +0.75 |
| 1 | 74.34 | 75.41 | 75.69 | +0.28 |
| 2 | 75.13 | 75.08 | 76.43 | +1.35 |
| 3 | 75.22 | 75.59 | **76.71** | +1.12 |

| Pair at round 3 | Gain | Right only in first / second | p | 95% interval (databases) |
|---|---:|---|---:|---|
| virtual line / Hinton line | +1.12 | 69 / 93 | 0.07 | -0.10 to +2.30 |
| gold line / virtual line | +0.37 | 65 / 73 | 0.55 | -1.17 to +1.95 |
| FedAvg line / virtual line | +0.47 | 117 / 127 | 0.57 | -1.04 to +2.13 |
| `virtual_k2aaa_a3` / virtual DPO r3 | +3.03 | 42 / 107 | < 0.001 | +1.76 to +4.34 |

Round 3 (execution errors / wrong results / extra-hard EX): gold 71 / 461 /
59.9, virtual 79 / 445 / 60.8, Hinton 58 / 442 / 63.0. Training data of the
virtual line: sample accuracy 77.5, 83.3, 85.3% by round, pairs 5,871,
4,142, 3,568 (gold line 77.5, 83.7, 85.5%; 5,794, 4,016, 3,492).

Other sets, EX; no choice was made on these:

| Row | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---:|---:|---:|---:|---:|
| `gold_k2aaa_a3` | 70.50 | 61.42 | 55.90 | 52.71 | **40.03** |
| `virtual_k2aaa_a3` | 70.50 | 61.02 | 55.42 | 54.77 | 39.77 |
| `self_k2aaa_a3` | 70.31 | 60.63 | 54.84 | 52.15 | 32.33 |
| `hinton_k2aaa_a3` | **72.82** | **62.01** | **56.67** | **58.13** | 38.33 |
| gold DPO r3 | 73.79 | **65.35** | 59.86 | 57.94 | 40.87 |
| virtual DPO r3 | 73.02 | 64.17 | **61.41** | 60.19 | 40.94 |
| Hinton DPO r3 | **76.50** | 64.17 | 61.03 | **64.11** | **41.20** |

| Pair at round 3 (right only in first / second, p) | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---|---|---|---|---|
| virtual line / Hinton line | +3.48 (32 / 68, < 0.001) | 0.00 (26 / 26) | -0.39 (58 / 54, 0.78) | +3.93 (13 / 34, 0.003) | +0.26 (103 / 107, 0.84) |
| gold line / virtual line | -0.77 (43 / 35, 0.43) | -1.18 (34 / 28, 0.53) | +1.55 (51 / 67, 0.17) | +2.24 (20 / 32, 0.13) | +0.07 (101 / 102, 1.0) |

- A soft target without the teacher ends where gold SQL ends after DPO:
  the virtual and gold lines are not separable on any set, and their
  training data match round by round.
- The Hinton line is above the virtual line by 1.12 on Spider test (at the
  edge), 3.48 on Spider dev and 3.93 on DK, level on Realistic, SYN and
  BIRD dev: the pattern of Hinton against gold on seed 0 (+1.49; +2.71,
  +6.17). Two server stages without the teacher land at 75.22 and 75.59 on
  seed 0, the Hinton stage 1.1 to 1.5 above both. The gold line moved 1.35
  between seeds, as much as these gaps; the control exists for seed 0 only.
- Where the lead sits on Spider test: on the 2,009 rows where the gold and
  virtual lines agree, the Hinton line is level (right on 53 rows both miss,
  wrong on 52 both get right). Its lead is on the 138 rows where the two
  disagree: right on 96 (FedAvg line 82). On Spider dev and DK it leads on
  the rows both agree on as well (35 / 17, 16 / 5).
- The lead is not on the teacher's rows: the teacher zero-shot is right on
  51 of the 69 rows right only in the virtual line (74%) and 61 of the 93
  right only in the Hinton line (66%).
- Before DPO, on Spider test the four server stages are within 0.75 point
  (gold 73.08, virtual 72.57, self 72.61, Hinton 73.31; none separable).
  The Hinton start leads the virtual start on Spider dev (+2.32, 34 / 58,
  p = 0.02) and DK (+3.36, 13 / 31, p = 0.01).
- The self-teacher stage costs BIRD accuracy: BIRD dev 32.33, 7.43 below
  the virtual teacher (74 / 188, p < 0.001); on the Spider sets it is level
  with gold and virtual.
- The vLLM rows of the two archived adapters match their HF rows within
  0.93 point on every set (largest: virtual on DK, 54.77 against 55.70).

Run time: `curve_virtual` 5 h 06 (09:47 to 14:53; estimate 5.5 h), its
other sets 15 min, `eval_self` 17 min. The queue is empty since 15:25.

## 2026-11-13: DPO round 1 without the NLL term: 76.20, not below DPO + NLL

Spider test, seed 0, vLLM inproc, batch 16 (fedicl-sql `41799ce5`,
`fc5793b8`; curve record `049c2f09`). DPO round 1 from `hinton_k2aaa_a3` on
the round 1 samples of the Hinton line, the same 5,393 pairs (same pair
file hash), schedule and updates; only the NLL weight is 0.

| Row (all from `hinton_k2aaa_a3`) | EX | Execution error | Wrong result | Hard | Extra |
|---|---:|---:|---:|---:|---:|
| start | 73.31 | 129 | 444 | 65.0 | 54.3 |
| NLL-only round 1 | 73.50 | 117 | 452 | 65.2 | 55.7 |
| DPO + NLL round 1 | 75.69 | 82 | 440 | 66.7 | **61.1** |
| DPO + NLL round 1, random pairs | 75.73 | 79 | 442 | 68.0 | 60.5 |
| DPO round 1, no NLL | **76.20** | 85 | **426** | **69.3** | 59.9 |
| DPO + NLL round 3 (the method) | 76.71 | 58 | 442 | 68.3 | 63.0 |

| Pair | Gain | Right only in first / second | p | 95% interval (databases) |
|---|---:|---|---:|---|
| DPO + NLL r1 / no NLL r1 | +0.51 | 23 / 34 | 0.19 | -0.05 to +1.13 |
| start / no NLL r1 | +2.89 | 39 / 101 | < 0.001 | +1.81 to +4.01 |
| no NLL r1 / DPO + NLL r3 | +0.51 | 36 / 47 | 0.27 | -0.23 to +1.20 |

- In round 1 the NLL term does not help: without it the round goes 0.51
  further (not separable), through fewer wrong results (426 against 440)
  on hard questions; execution errors are level.
- Client 1 ends training with a DPO margin of 0.47 without the term
  against 0.37 with it (pair accuracy 0.875 and 0.885). Focused DPO round 1,
  which raises the preference weight, also reaches 76.20: in round 1 DPO +
  NLL takes a smaller step than the preference term alone.
- Not tested: whether the term matters over rounds 2-3, where the usual
  reason for it (the chosen side's likelihood falling over iterations)
  would show; that needs 3 rounds with their own sampling (about 5.5 h,
  estimate).
- Of the three differences from the closest DPO work named in the advisor
  report (the NLL term, the on-policy rounds, the gold fallback), the NLL
  term has no measured role so far. No decision.

Run time: 1 h 46 (07:44 to 09:30; estimate 1 h 45).

## 2026-11-13: seed 1 gold line: the teacher's lead after DPO shrinks to 0.47

Spider test, seed 1, vLLM inproc, batch 16 (fedicl-sql `bbd6f34c` to
`03b4b3a8`; other sets `990440df`). FedAvg rounds 1-3 from the gold server
stage of seed 1 (71.45, 72.85, 73.73), then DPO rounds 1-3. Paired counts
and intervals computed from the committed predictions (bootstrap over the
40 test databases within a seed; pooled seeds resampled by question).

| Round | FedAvg line s0 / s1 | Gold line s0 / s1 | Hinton line s0 / s1 | Hinton minus gold s0 / s1 |
|---|---|---|---|---|
| start | 71.26 / 71.87 | 73.08 / 73.73 | 73.31 / 74.06 | +0.23 / +0.33 |
| 1 | 74.29 / 75.55 | 74.34 / 75.87 | 75.69 / 75.73 | +1.35 / -0.14 |
| 2 | 75.17 / 75.27 | 75.13 / 76.06 | 76.43 / 76.53 | +1.30 / +0.47 |
| 3 | 75.13 / 75.83 | 75.22 / 76.57 | **76.71 / 77.04** | +1.49 / +0.47 |

| Pair at round 3 | Seed 1 (right only in first / second, p, database interval) | Pooled by question (95%) |
|---|---|---|
| FedAvg line / gold line | +0.75 (103 / 119, 0.31, -0.57 to +2.06) | +0.42 (-0.70 to +1.54) |
| gold line / Hinton line | +0.47 (89 / 99, 0.51, -0.63 to +1.52) | +0.98 (+0.05 to +1.91, p = 0.04) |
| FedAvg line / Hinton line | +1.21 (84 / 110, 0.07) | +1.40 (+0.30 to +2.45) |
| `gold_k2aaa_a3` / gold DPO r3 | +2.84 (48 / 109, < 0.001) | +2.49 (+1.63 to +3.33) |

- The teacher's lead over gold SQL after DPO, +1.49 on seed 0, is +0.47 on
  seed 1. Pooled it is +0.98, at the edge (database-clustered pooled
  interval 0.00 to +1.93). Before DPO it is nil on both seeds.
- The gold line moves most between seeds: round 3 is 1.35 higher on seed 1
  (74 / 103, p = 0.04); the Hinton line moves 0.33, the FedAvg line 0.70.
  The seed 0 gold line looks like a low draw, so the seed 0 reading
  ("BIRD adds nothing after DPO, the teacher does") overstated the
  teacher's part.
- Gold against Hinton at round 3, seed 1: 76 wrong results become right,
  69 right rows become wrong; execution errors 71 against 74. Extra-hard
  63.6 against 62.7: the extra-hard lead of seed 0 does not repeat.
- Training data of the gold line, seed 1: sample accuracy 77.6, 83.7, 85.8%
  by round (Hinton 79.1, 84.5, 86.7; FedAvg 73.9, 81.6, 83.5); pairs
  5,796, 4,084, 3,516.

Other sets, round 3, EX (seed 0 / seed 1 / pooled by question):

| Pair | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---|---|---|---|---|
| gold line / Hinton line | +2.71 / +0.19 / +1.45 (+0.10 to +2.80) | -1.18 / -2.36 / -1.77 (-4.04 to +0.39) | +1.16 / -0.48 / +0.34 | +6.17 / +0.56 / +3.36 (+1.59 to +5.14) | +0.33 / -1.04 / -0.36 |
| FedAvg line / gold line | +0.68 / +3.48 / +2.08 (+0.34 to +3.87) | +1.77 / +4.53 / +3.15 (+0.69 to +5.71) | +1.55 / +1.84 / +1.69 | -0.93 / +2.43 / +0.75 | +11.21 / +12.26 / +11.73 |

Seed 1 gold DPO r3 EX: Spider dev 75.63, Realistic 66.93, SYN 59.86, DK
60.75, BIRD dev 41.26.

- The DK and Spider dev lead of the teacher on seed 0 (+6.17, +2.71) is
  +0.56 and +0.19 on seed 1. The gold start of seed 1 is stronger on those
  sets (Spider dev 72.34 against 70.50, DK 57.01 against 52.71); against it
  the Hinton start leads by only 0.68 and 1.12.
- Pooled, the gold stage now beats no server stage after DPO on Spider dev
  and Realistic, where seed 0 had found nothing.

What holds on both seeds: DPO gains 2.5 to 3.9 points from every start;
the BIRD server stage keeps about 11.7 points on BIRD dev after DPO; the
whole method leads FedAvg + DPO by 1.40 pooled. What does not: the teacher
as the part of the server stage that survives DPO. The soft-target control
(`curve_virtual`, seed 0) compares against the seed 0 gold line, which is
the low draw. No decision yet.

Run time: `curve_gold_sft` rounds 2-3 and `curve_gold` ended at 07:12
(estimate 07:05); the extra sets at 07:44.

## 2026-11-13: soft-target control queued (DPO from the virtual-teacher start)

No result yet. Owner decision, replacing the one of 2026-11-12 (no
soft-target control): the control runs from the earlier adapter
`virtual_k2aaa_a3`, so it costs its DPO rounds only (about 6.5 h with the
evaluations, estimate) instead of a new server stage and FedAvg rounds
(about 15.5 h). Both earlier adapters are approved: `virtual_k2aaa_a3` as a
start and a comparator, `self_k2aaa_a3` as a comparator
(`fedicl-sql/docs/SERVER_STORAGE.md` section 5).

Queue (fedicl-sql `8ebb7912`), after `sqldpo_s0/pilot_no_nll`:

- `eval_virtual`: `virtual_k2aaa_a3` with vLLM inproc on Spider test,
  Spider dev, DK, Realistic, SYN and BIRD dev, so the row sits in the
  paper's tables next to `hinton_k2aaa_a3` and `gold_k2aaa_a3`.
- `curve_virtual`: DPO rounds 1-3 from it with the settings of the Hinton
  and gold lines (root `virtual`), then round 3 on the other five sets.
  Read at round 3 against the Hinton line (76.71) and the gold line
  (75.22): if it ends near the gold line, the lead after DPO needs the 7B
  teacher; if near the Hinton line, a soft target is enough.
- `eval_self`: `self_k2aaa_a3` on the same six sets, last; no DPO line.

Cut: seed 0 only (seed 1 has no virtual-teacher adapter), one pair of
training lineages.

Checks before the push: the queue parses and the new curve has the form of
`sqldpo_s0/gold`; the evaluation command resolves six sets in a dry run;
the result rows of the two adapters differ from the `hinton_k2aaa_a3` row
only in output path, parent and stage name; 94 queue, curve and stage-chain
tests pass on the Mac. Not checked: that the two adapters are still on the
server (`check_virtual`, `check_self`).

Also read from Git: FedAvg round 1 of the gold line of seed 1 was published
at 22:34 on 11-12 (fedicl-sql `919cbb8e`), so `sqldpo_s1/check_gold`
passed.

## 2026-11-12: archived teacher controls approved for the paper

Owner decision: the archived rows below may be used in the paper as
comparators. All are Qwen2.5-Coder-1.5B-Instruct on `alpha_0.1/k5`, seed 0,
HF engine, batch 16, except the teacher row (7B, 4-bit).

| Row | Result row or prediction file in fedicl-sql | Adapter on the server | Git SHA | Sets |
|---|---|---|---|---|
| virtual teacher, K2 then 3 FedAvg rounds (`virtual_k2aaa_a3`) | `federated_stage__K2fkl,virtual-A-A-A__s0__95e15ce88661__f72e0fd5`; audit `p238_virtual_teacher_s0` | `artifacts/protocol_v2/p238_virtual_teacher_s0/virtual_k2aaa_a3/fedavg_adapter` | `02c30d3` | Spider dev, Realistic, SYN, DK, BIRD dev |
| self teacher, same chain (`self_k2aaa_a3`) | `federated_stage__K2fkl-A-A-A__s0__e18fe166a101__563b55e5`; audit `p244_self_teacher_s0` | `artifacts/protocol_v2/p244_self_teacher_s0/self_k2aaa_a3/fedavg_adapter` | `1f0bee7` | the same five |
| teacher zero-shot (`p253teacher_zeroshot`) | `eval_arms__s0__20261029T063500__af93cdc520a6__60f456f4804e4f11b55ef9c17cb45172`; audit `p253_teacher_test_s0` | none (base 7B model) | `24f0a5b` | Spider test |

- Nothing had to be restored: every result row, prediction file and audit
  of the three rows is still tracked in fedicl-sql (checked against
  `git ls-files`; `p238` 22 audit files, `p244` 24).
- The Hinton and gold comparators inside `p238` and `p244` are the adapters
  the method starts from (`p237_phase_e_s0`), so the control rows compare
  directly with `hinton_k2aaa_a3` and `gold_k2aaa_a3` under HF.
- What the rows do not cover: Spider test, the vLLM inproc engine of the
  paper's tables, and DPO after the server stage. Whether the two adapters
  are still on the server is not checked.
- `p217` and `p220` (another student or split) stay background for the
  placement question, not paper rows.

## 2026-11-12: the teacher's role, read from predictions and the archive

No run. The owner allowed, in this session, reading four archived
experiments (`audits/protocol_v2/p217_interleave_s0`,
`p220_placement_grid_s0`, `p238_virtual_teacher_s0`, `p244_self_teacher_s0`)
and pairing the method rows with the archived teacher zero-shot row
(`p253teacher_zeroshot`, Spider test, HF, 4-bit, fedicl-sql `24f0a5b`). The
method rows are vLLM inproc, so those paired counts mix two engines.

Spider test, seed 0, by kind of failure (computed from the committed
predictions):

| Row | Execution errors | of them `no such column` | Wrong results | Extra-hard EX |
|---|---:|---:|---:|---:|
| FedAvg R3 | 211 | 177 | 406 | 49.0 |
| `gold_k2aaa_a3` | 144 | 123 | 434 | 54.3 |
| `hinton_k2aaa_a3` | 129 | 111 | 444 | 54.3 |
| DPO r3 from FedAvg R3 | 101 | 61 | 433 | 56.6 |
| DPO r3 from `gold_k2aaa_a3` | 71 | 50 | 461 | 59.9 |
| DPO r3 from `hinton_k2aaa_a3` | **58** | **41** | 442 | **63.0** |

- No line writes BIRD-style SQL on Spider test (backticks, `CAST`,
  `INNER JOIN`: 0 rows in every row above).
- Hinton line against gold line at round 3 (+32 rows): 25 come from wrong
  results (85 become right, 60 become wrong), 7 from execution errors
  (24 / 17). Against the FedAvg line (+34 rows) 25 come from execution
  errors. The lead is on extra-hard questions on both seeds (seed 1: 62.7
  against 59.1 for the FedAvg line); hard is level.

Teacher zero-shot against the method (Spider test):

| | Teacher 7B zero-shot | Method, seed 0 | Method, seed 1 |
|---|---:|---:|---:|
| EX | 77.22 | 76.71 | 77.04 |
| Execution errors / wrong results | 76 / 413 | 58 / 442 | 74 / 419 |
| Easy / medium / hard / extra | 89.1 / **82.3** / **70.8** / 57.7 | **89.8** / 79.8 / 68.3 / **63.0** | |
| Right only in the method / only in the teacher | | 151 / 162 | 162 / 166 |
| Method's wrong-result rows that the teacher gets right | | 129 of 442 | 125 of 419 |
| Method's execution-error rows that the teacher gets right | | 33 of 58 | 41 of 74 |
| Right in at least one of the two | | 84.26 | 84.77 |

- Same EX, different rows: the teacher is right on about 160 rows the
  method misses (7.5 points) and wrong on about 155 the method gets right.
  Of the 410 rows the method misses on both seeds the teacher is right on
  108.
- Whether the Hinton line wins on the rows the teacher gets right (the
  teacher is right on 77% of all rows):

| Pair | Right only in the first: teacher right | Right only in the second: teacher right |
|---|---:|---:|
| `gold_k2aaa_a3` / `hinton_k2aaa_a3` (before DPO) | 48 of 76 (63%) | 66 of 81 (81%) |
| gold DPO r3 / Hinton DPO r3 | 51 of 77 (66%) | 70 of 109 (64%) |
| FedAvg DPO r3 / Hinton DPO r3, seed 0 | 62 of 101 (61%) | 99 of 135 (73%) |
| FedAvg DPO r3 / Hinton DPO r3, seed 1 | 50 of 84 (60%) | 69 of 110 (63%) |
| FedAvg R3 / FedAvg DPO r3 (no teacher) | 41 of 59 (69%) | 106 of 142 (75%) |

  Before DPO the Hinton start moves toward the teacher's answers at equal
  EX. After DPO the lead over the gold line is not on the teacher's rows
  (64% against 66%).

Archive, soft targets without the teacher (`p238`, `p244`; this student and
split, seed 0, HF, server stage K2 then 3 FedAvg rounds, no DPO; same loss
as the Hinton stage, lambda 0.5 / 0.5, T 2):

| Server-stage target | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---:|---:|---:|---:|---:|
| gold SQL | 70.41 | 61.22 | **56.38** | 52.34 | **40.03** |
| virtual teacher (gold token 0.73, the rest uniform) | 70.50 | 60.83 | 55.03 | 55.70 | 39.83 |
| self teacher (logits of the base 1.5B student) | 70.21 | 61.02 | 54.84 | 52.71 | 32.27 |
| 7B teacher (Hinton) | **72.53** | **61.81** | **56.38** | **58.32** | 38.53 |

- Hinton against the virtual teacher: Spider dev +2.03 (54 / 33, p = 0.03),
  DK +2.62 (29 / 15, p = 0.05). Against the self teacher: Spider dev +2.32
  (62 / 38, p = 0.02), DK +5.61. The virtual teacher equals gold on Spider
  dev (+0.10) and gives +3.36 on DK (34 / 16, p = 0.02).
- So before DPO the lead on Spider dev needs the 7B teacher; about half of
  the DK lead comes from any soft target. Not measured: these controls on
  Spider test, and after DPO.

Archive, where the server stage sits:

- `p220` (Qwen2.5-Coder-0.5B, split `alpha_0.5/k5`, seed 0; every arm has 2
  BIRD epochs and 3 Spider rounds). Hinton arms on Spider dev / Realistic /
  SYN / DK / BIRD dev: K>K>A>A>A 63.93 / 51.97 / 48.26 / 46.92 / 27.71;
  A>K>A>K>A 62.57 / 52.17 / 50.48 / 47.85 / 28.88; A>K>K>A>A 63.15 / 51.77 /
  49.71 / 47.48 / 27.77. Server stage first against interleaved: Spider dev
  +1.35 (58 / 44, p = 0.20), SYN -2.22 (40 / 63, p = 0.03), the other sets
  within 1.2 points and not separable.
- `p217` (Qwen2.5-1.5B-Instruct, not the Coder model): A>K>A>K>A against
  A>K>A>A, which also adds a BIRD epoch: Hinton 69.54 against 67.60 on
  Spider dev (51 / 31, p = 0.04), gold 67.50 against 67.89.
- Neither is this student and split, and neither has DPO after it. On this
  setup the server knowledge is not lost in the client rounds: BIRD dev of
  the Hinton line is 38.33 after 3 FedAvg rounds and 41.20 after DPO.

No decision yet. Using the archived rows in the paper needs the owner's
approval.

## 2026-11-12: no soft-target control for the teacher

Owner decision: no label smoothing or self-distillation server stage is
queued as a control for the teacher; self-distillation was run before the
fresh start. If the gold line of seed 1 ends level with the FedAvg line, as
on seed 0, the Hinton stage's lead over the gold stage after DPO is read as
the teacher's effect.

## 2026-11-12: seed 1, the Hinton stage keeps 1.21 points over the FedAvg line after DPO

Spider test, seed 1, vLLM inproc, batch 16 (fedicl-sql `dfab0013` to
`23b3e96d`; other sets `36466dc6`). DPO rounds 1-3 from FedAvg R3 seed 1,
next to the Hinton line of seed 1 and both lines of seed 0. Intervals: a
bootstrap over the test databases (10,000 resamples), computed from the
committed predictions.

| Round | FedAvg line, seed 0 | FedAvg line, seed 1 | Hinton line, seed 0 | Hinton line, seed 1 | Hinton minus FedAvg, seed 0 / seed 1 |
|---|---:|---:|---:|---:|---|
| start | 71.26 | 71.87 | 73.31 | 74.06 | +2.05 / +2.19 |
| 1 | 74.29 | 75.55 | 75.69 | 75.73 | +1.40 / +0.19 |
| 2 | 75.17 | 75.27 | 76.43 | 76.53 | +1.26 / +1.26 |
| 3 | 75.13 | 75.83 | 76.71 | **77.04** | +1.58 / +1.21 |

| Pair, seed 1 | Gain | Right only in the first / only in the second | p | 95% interval (databases) |
|---|---:|---:|---:|---|
| FedAvg R3 / FedAvg DPO r1 | +3.68 | 56 / 135 | < 0.001 | +2.00 to +5.53 |
| FedAvg DPO r1 / r2 | -0.28 | 31 / 25 | 0.50 | |
| FedAvg DPO r2 / r3 | +0.56 | 25 / 37 | 0.16 | |
| FedAvg R3 / FedAvg DPO r3 | +3.96 | 65 / 150 | < 0.001 | +2.37 to +5.66 |
| FedAvg R3 / `hinton_k2aaa_a3` | +2.19 | 96 / 143 | 0.003 | +0.19 to +4.19 |
| FedAvg DPO r3 / Hinton DPO r3 | +1.21 | 84 / 110 | 0.07 | -0.19 to +2.59 |
| FedAvg R3 / Hinton DPO r3 | +5.17 | 76 / 187 | < 0.001 | +3.28 to +7.05 |

Both seeds pooled, clustered by question:

| Pair | Gain | 95% interval | p |
|---|---:|---|---:|
| FedAvg DPO r3 / Hinton DPO r3 (server stage after DPO) | +1.40 | +0.32 to +2.47 | 0.01 |
| FedAvg R3 / FedAvg DPO r3 (DPO without a server stage) | +3.91 | +2.82 to +5.01 | < 0.001 |
| FedAvg R3 / `hinton_k2aaa_a3` (server stage before DPO) | +2.12 | +0.95 to +3.29 | < 0.001 |
| FedAvg R3 / Hinton DPO r3 (whole method) | +5.31 | +4.06 to +6.56 | < 0.001 |

- The FedAvg line repeats seed 0: one large step at round 1, then flat
  (75.55, 75.27, 75.83). Seed 0 and seed 1 differ by 0.70 at round 3
  (63 / 78, p = 0.24).
- The server-stage lead after DPO repeats in sign and size (+1.58, +1.21).
  Pooled by question it is separable (+1.40, p = 0.01); within each seed
  the database interval touches zero. DPO closes a quarter to a half of
  the lead the server stage had before it (seed 0: 2.05 to 1.58; seed 1:
  2.19 to 1.21).
- On seed 1 the lead is gone after round 1 (+0.19, 99 / 103) and comes back
  at rounds 2-3, because DPO round 1 from FedAvg R3 gains more on seed 1
  (+3.68) than on seed 0 (+3.03). The round 3 reading is the fixed one.
- Error types at round 3 (execution errors / wrong results): FedAvg line
  95 / 424, Hinton line 74 / 419 (seed 0: 101 / 433, 58 / 442). The lead
  is in execution errors on both seeds. By hardness the Hinton line is
  ahead on medium (80.5 against 78.4) and extra (62.7 against 59.1), level
  on easy and hard.
- Training data of the FedAvg line, seed 1: sample accuracy 73.9, 81.6,
  83.5% by round (seed 0: 74.3, 82.1, 83.9%; Hinton seed 1: 79.1, 84.5,
  86.7%); pairs 6,533, 4,338, 3,840 (rejected execution error 3,945,
  1,883, 1,463; wrong result 2,588, 2,455, 2,377).

Other sets, seed 1, EX (execution errors); no choice was made on these:

| Row | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---:|---:|---:|---:|---:|
| FedAvg R3 | 68.47 (124) | 58.27 (84) | 55.03 (159) | 54.02 (83) | 25.03 (624) |
| FedAvg DPO r3 | 72.15 (69) | 62.40 (44) | 58.03 (99) | 58.32 (52) | 29.01 (433) |
| `hinton_k2aaa_a3` | 73.02 (88) | 61.81 (55) | 57.83 (137) | 58.13 (50) | 37.03 (310) |
| Hinton DPO r3 | **75.82** (44) | **64.57** (27) | **59.38** (82) | **61.31** (31) | **40.22** (220) |

| Pair at round 3 | Spider dev | Realistic | SYN | DK | BIRD dev |
|---|---|---|---|---|---|
| FedAvg line / Hinton line, seed 1 (right only in the first / only in the second, p) | +3.68 (51 / 89, 0.002) | +2.17 (30 / 41, 0.24) | +1.35 (64 / 78, 0.28) | +2.99 (25 / 41, 0.06) | +11.21 (83 / 255, < 0.001) |
| seed 0 | +3.38 (47 / 82, 0.003) | +0.59 (36 / 39, 0.82) | +2.71 (62 / 90, 0.03) | +5.23 (19 / 47, 0.001) | +11.54 (73 / 250, < 0.001) |
| both seeds pooled by question (95% interval) | +3.53 (+1.67 to +5.39) | +1.38 (-1.40 to +4.16) | +2.03 (+0.11 to +3.95) | +4.11 (+1.57 to +6.66) | +11.38 (+9.42 to +13.33) |

- The lead after DPO has the same sign on every set and both seeds. It is
  clear on Spider dev and DK, small on SYN, not separable on Realistic. The
  first four sets share the 20 Spider dev databases, so they are one
  domain check, not four.
- DPO gains on every set from both starts on seed 1 (Spider dev +2.80 to
  +3.68, BIRD dev +3.19 and +3.98), as on seed 0: DPO on the clients'
  Spider data does not cost BIRD accuracy.
- Not answered yet: whether the lead comes from the teacher or from the
  BIRD data on seed 1 (the gold line of seed 1 is next in the queue).

Run time: `curve_fedavg` took 5 h 24 (14:10 to 19:34), the extra sets
1 h 05.

## 2026-11-12: random pairs give the same result as nearest pairs in round 1

Spider test, seed 0, vLLM inproc, batch 16 (fedicl-sql `6c06c5ce` to
`1ad627b4`). DPO round 1 from `hinton_k2aaa_a3` on the round 1 samples of
the Hinton line; only which correct and wrong sample of a question pair up
differs. Both rows have 5,393 pairs, 609 of them with gold as chosen.

| Pairs | EX | EM | Execution error | Wrong result | Easy | Medium | Hard | Extra | Mean pair similarity | Rejected: execution error / wrong result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| nearest (DPO round 1) | 75.69 | 65.16 | 82 | 440 | 89.6 | 79.0 | 66.7 | 61.1 | 0.817 | 2,806 / 2,587 |
| random | 75.73 | 65.35 | 79 | 442 | 89.1 | 78.9 | 68.0 | 60.5 | 0.715 | 2,834 / 2,559 |

- No difference: right only with nearest pairs 15, only with random pairs
  16 (p = 1.0). The two models write the same SQL on 86.9% of the rows.
- The pair sets did differ (mean similarity 0.817 against 0.715), so the
  round 1 gain does not depend on pairing the most similar two samples.
- Not tested: rounds 2 and 3 with their own sampling, and seed 1.
- Owner decision (2026-11-12): nearest pairing stays in the method
  description as a detail and leaves the list of differences from the
  closest DPO work in the advisor report (three remain: the NLL term, the
  on-policy rounds, the gold fallback). `pilot_pair_frequent` is dropped
  from the queue (fedicl-sql `467f5073`); `pilot_no_nll` now follows the
  seed 1 lines directly.

## 2026-11-12: pair order pilots and a row without the NLL term queued

No result yet. Our pairs match the most similar correct and wrong sample of
a question; this is one of the differences from the closest DPO work, with
the NLL term, the on-policy rounds and the gold fallback. Two 1-round
pilots test whether it matters (fedicl-sql `8c4af387`, `d06ab812`): DPO
round 1 from `hinton_k2aaa_a3` (seed 0) on the round 1 samples of the Hinton
line, with `--pair-order random` (a fixed hash order, the control) and
`--pair-order frequent` (the most often sampled wrong SQL against the most
often sampled correct SQL). Labels, pair count, loss, schedule and updates
equal DPO round 1 (75.69), the comparator. Each has its own root
(`hinton_pair_random`, `hinton_pair_frequent`); about 1.75 h each
(estimate).

Owner decision on the order (fedicl-sql `f485c0ad`): seed 1 has not yet
said anything about the teacher or BIRD (only its Hinton line is done), and
that question decides the method, so only the random control runs before
the rest of seed 1 (its result could change how later rounds pair). The
frequent order and a new row, DPO round 1 without the NLL term
(`--nll-alpha 0`, root `hinton_no_nll`, nearest pairs), run after the seed 1
lines.

Check before the push: with the default order the new code builds the same
pairs as the previous code on 18,000 random question records, and the
recorded pair rule identity is unchanged; 616 tests pass on the Mac.

## 2026-11-12: seed 1, the Hinton DPO line repeats (77.04 at round 3)

Spider test, seed 1, vLLM inproc, batch 16 (fedicl-sql `568f1170` to
`091da1f5`; curve record `6f4c6f07`). DPO rounds 1-3 from `hinton_k2aaa_a3`
seed 1, next to seed 0:

| Row | Seed 0 EX | Seed 1 EX | Seed 1: execution error | Wrong result | Easy | Medium | Hard | Extra |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `hinton_k2aaa_a3` | 73.31 | 74.06 | 132 | 425 | 87.9 | 78.0 | 65.4 | 57.7 |
| DPO round 1 | 75.69 | 75.73 | **71** | 450 | **88.5** | 78.9 | 68.0 | 61.3 |
| DPO round 2 | 76.43 | 76.53 | 72 | 432 | 87.7 | 80.4 | 69.3 | 61.9 |
| DPO round 3 | 76.71 | **77.04** | 74 | **419** | 88.3 | **80.5** | **70.2** | **62.7** |

| Pair | Seed 0 | Seed 1 (right only in the first / only in the second, p, 95% interval over databases) |
|---|---|---|
| start / round 1 | +2.38 (37 / 88) | +1.68 (30 / 66, < 0.001, +0.71 to +2.63) |
| round 1 / round 2 | +0.75 (24 / 40) | +0.79 (15 / 32, 0.02, +0.23 to +1.38) |
| round 2 / round 3 | +0.28 (17 / 23) | +0.51 (12 / 23, 0.09, -0.05 to +1.15) |
| start / round 3 | +3.40 (37 / 110) | +2.98 (33 / 97, < 0.001, +1.64 to +4.34) |

- The step repeats: +2.98 on seed 1 against +3.40 on seed 0, the same shape
  by round. Both seeds pooled, clustered by question: +3.19 (95% +2.35 to
  +4.03).
- The method row moves 0.33 between seeds (76.71, 77.04; 83 / 90, p = 0.65).
- The sampled data is the same on both seeds: sample accuracy 79.1, 84.5,
  86.7% by round (seed 0: 79.1, 84.4, 86.6%); pairs 5,376, 3,833, 3,157
  (seed 0: 5,393, 3,899, 3,208).
- Where the gain comes from, start to round 3: execution errors -58, wrong
  results -6 (seed 0: -71, -2). On seed 1 round 1 turns errors into queries
  that run (errors -61, wrong results +25) and rounds 2-3 lower the wrong
  results (450 to 419); on seed 0 the wrong results stayed at 433 to 442.
- Not answered yet: the lead of the Hinton stage after DPO on seed 1 (the
  FedAvg and gold lines of seed 1 are running or queued).

FedAvg from the base model, seed 1, so far: round 1 67.63, round 2 69.91
(seed 0 round 3: 71.26).

Run time: `curve_hinton` took 7 h 50 (round 1: 5 h 03, round 2: 1 h 30,
round 3: 1 h 16) against an estimate of 5.5 h. Peak reserved memory stayed
at or under 17.42 GiB in every client update. Why round 1 was slow is not
readable from Git.

## 2026-11-11: seed 1 queued (plain DPO, Hinton stage); BIRD dev for 6 rows

Owner decisions: the preference term stays plain DPO (focused DPO is an
ablation row); the method keeps the Hinton server stage; seed 1 is queued;
the gold server stage of seed 1 (`K2[ce]`, row
`federated_stage__K2ce__s1__b637761c31e0__5543c6bb`) is approved as the
start of `gold_k2aaa_a3` seed 1, on the condition that the seed 1 starts are
the standard recipe (no replay, SQL-only).

Phase `sqldpo_s1` (fedicl-sql `d36293b4`): DPO rounds 1-3 from
`hinton_k2aaa_a3` seed 1; FedAvg rounds 1-3 from the base model with seed 1,
then DPO rounds 1-3; FedAvg rounds 1-3 from the gold server stage of seed 1,
then DPO rounds 1-3; the starts and round 3 on Spider dev, Realistic, SYN,
DK and BIRD dev. About 28.5 h on GPU 0 (estimate).

Check of the reused seed 1 starts, from the committed result rows:

- `hinton_k2aaa_a3` seed 1 is the chain `K2[fkl]>A>A>A`; the config of each
  of its 4 stages equals the seed 0 stage except seed, label and output path
  (2 server epochs, lambda 0.5 / 0.5, T 2, the same teacher logit cache; 3
  FedAvg rounds, lr 2e-4, 1 local epoch; SQL-only; no replay, no retention
  term, the same client sizes).
- The gold server stage of seed 1 has the config of the seed 0 one except
  the seed (2 epochs, gold SQL only, max length 7,424, from the base model).
  Its 3 FedAvg rounds did not exist without replay: the seed 1 rows after it
  are `K2[ce]>Areplay` (clients replay BIRD rows) and are not used.
- The queued FedAvg and DPO commands parse to seed 1, SQL-only, replay
  ratio 0, no retention term, proximal weight 0.
- Not checked: that the gold server stage adapter is still on the server
  (`sqldpo_s1/check_gold`; the first task prints found or MISSING).

Earlier seed 1 results, read from the archive and the committed rows on the
owner's request (HF engine, batch 16; they are not paired with vLLM rows):
`hinton_k2aaa_a3` seed 1 has 74.10 on Spider test (138 execution errors),
72.82 on Spider dev, 58.13 on DK; seed 0 under the same engine 73.50, 72.53,
58.32. The only gold-type row of seed 1 is the replay one (73.40, 71.47,
55.51). Plain `gold_k2aaa_a3`, FedAvg R3 and any DPO round were never run on
seed 1, so nothing yet shows whether the lead after DPO repeats.

BIRD dev (1,534 rows, with evidence), seed 0, vLLM inproc (fedicl-sql
`f3f32fc5`). BIRD train is the server's public data, so this set is in the
domain of the server stage and outside the clients' domain. EX (execution
errors):

| Line | Start | DPO round 3 | Gain (right only at the start / only at round 3) |
|---|---:|---:|---|
| no server stage (FedAvg R3) | 25.55 (610) | 29.66 (439) | +4.11 (41 / 104, p < 0.001) |
| BIRD gold SFT | **40.03** (259) | 40.87 (**175**) | +0.85 (67 / 80, p = 0.32) |
| BIRD Hinton KD | 38.33 (311) | **41.20** (214) | +2.87 (47 / 91, p < 0.001) |

- DPO on the clients' Spider data does not cost BIRD accuracy: every line
  gains.
- On BIRD dev the teacher adds nothing over gold SQL: Hinton against gold is
  -1.69 before DPO (114 / 88, p = 0.08) and +0.33 after it (102 / 107,
  p = 0.78).

## 2026-11-11: DPO from the gold and FedAvg starts on Spider dev, Realistic, SYN and DK

Seed 0, vLLM inproc, batch 16 (fedicl-sql `26146044`). No choice was made on
these sets; all four are on the 20 Spider dev databases. EX:

| Row | Spider test | Dev | Realistic | SYN | DK |
|---|---:|---:|---:|---:|---:|
| DPO r1 from FedAvg R3 | 74.29 | 71.18 | 63.39 | 56.67 | 58.13 |
| DPO r2 from FedAvg R3 | 75.17 | 70.99 | 62.99 | 57.16 | 57.76 |
| DPO r3 from FedAvg R3 | 75.13 | 73.11 | 63.58 | 58.32 | 58.88 |
| DPO r1 from `gold_k2aaa_a3` | 74.34 | 73.02 | 64.57 | 58.99 | 57.38 |
| DPO r2 from `gold_k2aaa_a3` | 75.13 | 73.02 | **65.35** | 59.19 | 58.32 |
| DPO r3 from `gold_k2aaa_a3` | 75.22 | 73.79 | **65.35** | 59.86 | 57.94 |
| DPO r3 from `hinton_k2aaa_a3` | **76.71** | **76.50** | 64.17 | **61.03** | **64.11** |

Round 3, gain of the second row (right only in the first / only in the
second, p):

| Pair | Dev | Realistic | SYN | DK |
|---|---|---|---|---|
| gold line / Hinton line | +2.71 (27 / 55, 0.003) | -1.18 (29 / 23, 0.49) | +1.16 (52 / 64, 0.31) | +6.17 (7 / 40, < 0.001) |
| FedAvg line / Hinton line | +3.38 (47 / 82, 0.003) | +0.59 (36 / 39, 0.82) | +2.71 (62 / 90, 0.03) | +5.23 (19 / 47, 0.001) |
| FedAvg line / gold line | +0.68 (58 / 65, 0.59) | +1.77 (27 / 36, 0.31) | +1.55 (69 / 85, 0.23) | -0.93 (32 / 27, 0.60) |

- The teacher's lead after DPO holds on Spider dev and DK, the two sets
  where the Hinton stage already led before DPO (+2.32, +5.42). On SYN it
  has the same sign and is not separable; on Realistic the gold line is
  ahead by 1.18, not separable.
- The gold stage against no server stage is not separable on any of the
  four sets after DPO, as on Spider test.
- The four sets share their databases, so this is one more set in favour of
  the teacher, not four; seed 1 is still what confirms it.

## 2026-11-11: focused DPO pilot: a slightly larger step, the wrong results stay

Spider test, seed 0, vLLM inproc (fedicl-sql `8afdaae2`, `9d6c169d`, curve
record `8c536cab`; the task ran 1 h 43). Focused DPO round 1 from
`hinton_k2aaa_a3`, on the samples and the 5,393 pairs of DPO round 1:
**76.20**.

| Row | EX | Right | Execution error | Wrong result | Easy | Medium | Hard | Extra |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `hinton_k2aaa_a3` | 73.31 | 1,574 | 129 | 444 | 88.5 | 77.4 | 65.0 | 54.3 |
| DPO round 1 | 75.69 | 1,625 | 82 | 440 | 89.6 | 79.0 | 66.7 | 61.1 |
| focused DPO round 1 | 76.20 | 1,636 | 72 | 439 | **89.8** | 79.5 | 68.3 | 60.8 |
| DPO round 2 | 76.43 | 1,641 | 73 | **433** | 89.4 | 79.2 | **69.3** | 61.9 |
| DPO round 3 | **76.71** | **1,647** | **58** | 442 | **89.8** | **79.8** | 68.3 | **63.0** |

| Pair | Gain | Right only in the first / only in the second | p | 95% interval (databases) |
|---|---:|---:|---:|---|
| DPO r1 / focused r1 | +0.51 | 10 / 21 | 0.07 | -0.04 to +1.09 |
| `hinton_k2aaa_a3` / focused r1 | +2.89 | 28 / 90 | < 0.001 | +1.79 to +3.88 |
| focused r1 / DPO r2 | +0.23 | 29 / 34 | 0.62 | -0.61 to +1.16 |
| focused r1 / DPO r3 | +0.51 | 24 / 35 | 0.19 | -0.05 to +1.09 |

- The pilot's question was the wrong results: 440 with plain DPO, 439 with
  the focused term. Against DPO round 1, 12 wrong results become right, 7
  right rows and 7 execution errors become wrong results. The focused term
  does not reach that part.
- The 11 more right rows come from execution errors (82 to 72), the same
  mechanism as plain DPO. Focused round 1 sits between plain rounds 1 and 2
  and is separable from neither; the two round 1 models give the same SQL on
  1,913 of 2,147 rows.
- The span is not narrow here: the differing middle is 63 to 73% of the
  response tokens per client (for example 32 of 49 on client 1), no pair
  without a span. With weight 2 on two thirds of the tokens, the focused
  term is close to plain DPO with a doubled preference term, so the pilot
  does not separate "focus" from "a larger preference weight".
- Peak reserved per client 13.1 to 17.3 GiB, as in DPO round 1.
- By the rule written when it was queued (full line only if round 1 lowers
  the wrong results), the 3-round focused line is not queued. The choice of
  the preference term stays with the owner.

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
