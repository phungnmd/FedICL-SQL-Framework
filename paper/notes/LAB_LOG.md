# FedLS-SQL: lab log

Every run, result and decision since the clean reset of 2026-11-17, newest
on top. A result reported only in chat is logged as "not committed". The
log of the earlier setup is at the tag `archive/pre-reset-2026-11-17`.

## 2026-11-20: extensions toward Q2 recorded, to try after the method is settled (owner; no run)

Owner: write the directions down; they are tried after the method is
settled on BIRD. In order: (a) centralized DPO + NLL and the gap between
federated and centralized for SFT and for DPO, with the drift of the
client updates; (b) one local loss with NLL on the gold SQL for the
all-wrong questions and DPO + NLL on the mixed ones, only if the BIRD
reads ask for it; (c) questions without gold SQL labelled by the vote
over execution results. Owner on (c): hiding gold is an assumption the
datasets do not make; it is a secondary experiment at most, not a part
of the method, and it needs an SFT baseline with pseudo-labels to be a
fair comparison. Its first step is a CPU probe of the vote labels on
the Spider round 1 samples (script not written). Table with evidence
and costs: `RESEARCH_STATE.md`, section 4, item 12. Nothing is queued.

## 2026-11-20: queue turned to the earliest read of the method on BIRD; SFT stage line `bird_k1` queued; centralized SFT after the BIRD rounds (owner; queue `51d09d80`)

Owner: order the pipeline so that the direction of the method is known
soonest. No new run in this entry.

What is open is one point: what the method does with the questions
that have no correct sample (Spider 12%, BIRD 41.9% for the base
student). Three forms: nothing (k = 0), an SFT stage before the DPO
rounds, gold inside the round. On Spider the first two end equal and
the gold rule fell at round 2; that run changed three things at once
(gold for all-wrong questions, 2,032 pairs; gold on databases without
rows, 3,110 pairs; client 4's weight 0.28 to 0.43), so it is not a
clean reading of gold next to DPO. BIRD train has no database without
rows.

Queue:

- New `bird_k1/round_1`: one DPO + NLL round from `bird_sft` round 1
  (k = 1), the command of `bird_k0/round_1` with `--parent-stage
  fedavg_bird_ddl_a01_r1_s0` in place of `--from-base` and a root of its
  own (`fedpref_bird_sftr1_p2_ddl_alpha01_s0`), evaluation on BIRD dev
  and both publications. Read at 2 total rounds against `bird_sft`
  round 2 and `bird_k0` round 2. It stands before the relabel: it needs
  no label of the base student's samples, so it is the first BIRD read
  of the method a free card can produce. k = 1 and not 2 or the best
  round: its comparison rows at the same total rounds are already
  queued. Checked before queuing (new test): against `bird_k0/round_1`
  only the start and the root differ and the setup (prompt, length,
  LoRA, sampling, pair rule) is equal; against the Spider k = 2 round
  only the parent round, split, profile, schema text and root. The
  parent row resolves from its stage label; one BIRD prompt rendered
  and read. 523 tests pass, 2 skipped. Not measured: its run time, its
  pair count, memory, and free RAM with its 16 label processes next to
  the relabel by hand.
- `refs/central_sft` moves after the BIRD rounds. It stood before them
  since this morning (owner), and under that order GPU 0 would take it
  after `bird_sft/round_2`, before that round's evaluation, for up to 6
  more epochs of 2 h 10 min. It is a reference row and keeps its
  checkpoint in epoch 3.
- Kept in place: `bird_k0/round_1`, `bird_k0_gold/round_1`,
  `bird_k0/round_2`, `bird_fixed/round_2`.

The server gets the order only after a pull; if GPU 0 reaches
centralized SFT first, the worker is stopped and started again
(`PIPELINE_NEXT.md`, step 1).

Owner's expectation: DPO from the best SFT round, 1 to 2 rounds, gives
the highest level. On Spider one DPO round carries most of the gain
(+3.36 from FedAvg round 2, +3.26 from round 3; a second round +0.74,
p 0.093), and the level is the same from k = 0, 2 and 3 (78.02, 78.20,
77.97), so the start does not raise it there; on BIRD it is read from
`bird_k1` first. Not queued, decided on those reads: the BIRD lines to
4 rounds, DPO from the best `bird_sft` round, one local loss with NLL
on the gold SQL for the all-wrong questions only (needs a preference
weight per row), centralized DPO + NLL on Spider.

Journal quartiles, looked up today through search results (the pages
were not opened): Scimago 2025 lists CMC as Q2 (SJR 0.513, Computer
Science Applications) and JIIS as Q2 (SJR 0.775, Information Systems).
JCR: CMC Q3 on Peeref (JCR 2024); JIIS Q3 on Peeref (JCR 2023) and Q2
on LetPub. Which list the owner's requirement counts is open.

## 2026-11-20: FedAvg SFT round 1 on BIRD dev 38.85; 16 worker processes for the BIRD label steps (results `ec5d3ec6`, `91e5fcdd`; queue `4f9e3299`, `f0b35ba9`)

BIRD dev (1,534 rows): FedAvg SFT round 1 on the BIRD clients 38.85
(execution errors 372, 2 rows on the 30 s budget, scorer v3) against the
base student 29.47 (646, 3, scorer v2): +9.38. `bird_k0/round_1` is read
against it.

Owner: the server has 2 x 32 logical processors. The BIRD label steps
not yet run (`bird/relabel`, `bird_k0`, `bird_k0_gold`, `bird_fixed`)
take `--score-workers 16` (4 before, chosen for SQL in threads); the
worker count is not part of a sample file's identity. RAM with 16
processes on BIRD train is not measured. `bird/read_relabelled` keeps
the command of the first read (it labels nothing).

## 2026-11-20: label step runs the gold once per question; only a run short of CPU runs again alone (owner; code `a14f140a`)

Owner: the relabel of `bird/read` takes too long for one round; is the
way it is done the BIRD standard? The evaluation follows the official
evaluator (one 30 s budget per prediction/gold pair, a process per pair,
rows as sets). BIRD defines no rule for labelling training samples: the
30 s per sample is ours. Two costs came from the code of this morning,
not from any rule: the gold ran three times per question and once more
per distinct SQL, and every run that met the budget ran a second time
with the other workers waiting, also a SQL that had used the 30 s itself
(a runaway join).

Changed, the rule and the scorer name unchanged (BIRD v3):

- One job per question: the gold runs once and its measured seconds
  count in every pair (a gold that does not fit twice in 30 s is
  `gold_error`; a SQL that runs and leaves the gold less than its
  seconds gets no label; a SQL that meets 30 s is a timeout). Spider:
  60 s for the gold and for each SQL.
- A run that met the budget is repeated alone only when it had less
  than 0.8 of its wall-clock time as CPU time.
- The pool logs the SQL seconds (all, gold, runs alone).

Checked on the Mac, old against new, with each gold, two other golds of
its database and one failing SQL as the SQL to score: the same result
for all 26,804 SQL of the 8,659 Spider train questions and all 6,136
SQL of the 1,534 BIRD dev questions (6 timeouts either way); BIRD dev
179.5 s against 106.9 s with 4 workers. Not measured on the server or
on BIRD train (its databases are not on the Mac). The relabel running
by hand keeps the code it loaded; the first label step on the new code
is `bird_k0/round_2`. Its `SQL budget` line then says where the time
goes. Open for the owner: a shorter budget for label steps only (a
sample over it gets no label), and more than 4 score workers on BIRD.

## 2026-11-20: gold line round 2 falls on Spider; centralized SFT epochs 1 and 2; queue order (results `73850020`..`0643b48c`; queue `b438dec4`, `42046d18`)

Spider test (2,147 rows), read with `scripts.error_breakdown`:

| Arm | EX | exec errors | wrong results |
|---|---|---|---|
| k = 0 line with gold, round 2 (`k0_gold/round_2`) | 75.73 | 76 | 442 |
| k = 0 line, round 2 | 77.18 | 92 | 398 |
| k = 0 line with gold, round 1 | 76.67 | 53 | 444 |
| centralized SFT, epoch 1 | 75.08 | 164 | 370 |
| centralized SFT, epoch 2 | 75.73 | 149 | 370 |
| FedAvg SFT, round 2 | 74.10 | 183 | 373 |

- Gold line: round 2 is 1.45 below the k = 0 line at 2 rounds (84 rows
  fixed, 115 broken, McNemar p 0.033) and 0.94 below its own round 1.
  It does not rise, so rounds 3 and 4 are not queued. On Spider, gold as
  chosen where the samples give no correct side is not kept.
- Centralized SFT: epoch 1 continued from example 624 of 8,659 (the
  stop of 2026-11-18), epoch 2 ran in one call (2 h 10 min, peak
  reserved 20,321 MB). Epoch 2 gains 0.65 over epoch 1 (p 0.34), so the
  rule goes on to epoch 3. Against centralized epoch 2: FedAvg round 2
  is 1.63 below (p 0.030); the k = 0 DPO line at 2 rounds is 1.45 above
  (173 against 142 rows, p 0.091).
- These evaluations ran with SQL in worker processes on the server
  (`exec_timeouts` 1 in each): the first runs of the pool on Windows.

Queue (owner): centralized SFT stands before the BIRD rounds; GPU 1
started with `--until 07:30`. The relabel of `bird/read` runs by hand
since about 01:00 and stands after `bird_sft/round_1` in the queue, so
a free card trains meanwhile. Its pace on client 1: 575 of 2,011
questions after 26 min, against 26 min for the whole client in the
first read (`run_times/bird/read.json`: generate 36 min, label 2 h 42
min); result not in yet. Measured on the Mac: the golds of the 8,659
Spider train questions (17,318 jobs) take 25.8 s in threads with the
earlier check and 4.5 s in 16 worker processes.

## 2026-11-20: BIRD train golds lost to the 30 s budget came from SQL run in threads; SQL now runs in worker processes (owner; code `0063d2a3`, `addba08d`..`4b4df521`)

Owner: the BIRD read gave 534 `gold_error` questions against about 400
counted on the Mac; check the 30 s budget, then avoid the fault as far
as possible on Spider and BIRD.

Measured:

- `bird/read` labels (`timeouts_r1_base.json`, `799543a1`): 534
  `gold_error` = 350 SQL errors (the Mac count; 330 in `retail_world`)
  + 184 golds on the budget (`donor` 71, `retails` 34,
  `world_development_indicators` 20, `language_corpus` 16; client 2 85,
  client 5 73). 196 samples of 94,280 labelled `exec_error` by a
  timeout, 10 without a label (budget ended on the gold).
- The 184 golds and the 8 golds of the unlabelled samples run once
  alone on the server, stop at 60 s (`gold_retime_r1_base.json`,
  `b2aeef14`): 159 under 15 s, 13 in 15 to 30 s, 6 in 30 to 60 s, 14
  over 60 s. Of the 184: 151, 13, 6, 14.
- Cause, measured on the Mac with the repository's timeout code: the
  budget check is a Python call from SQLite every 1,000 steps, and in
  threads it waits for the interpreter lock. One 0.3 s query: 0.4 s
  alone; 0.4 s in 4 threads; about 260 s in 4 threads next to one busy
  Python thread; about 5 s the same at 100,000 steps; 0.4 s in 4
  processes. Not measured on the server itself.
- Committed evaluations: every row that timed out is slow on its own.
  Run alone on the Mac, the predictions of BIRD dev rows 106 and 369
  take 98 s and 141 s, the gold of row 701 over 180 s, the predictions
  of Spider test rows 1044 and 1040 (`aan_1`) 112 s to over 180 s. No
  published EX lost a row to load.
- Spider train labels: `gold_error` is 3 of 8,659 in all 16 label steps
  (the 3 golds known not to run). Samples labelled `exec_error` by a
  timeout on Spider: not counted (sample files are on the server).

Changed (owner: yes to SQL in processes, a sparser check, a second run
alone, timeouts written in the results):

- Every prediction and gold of an evaluation or a label step runs in a
  worker process (`fedls_sql/eval/sql_pool.py`), as the official BIRD
  evaluator runs each pair in a process of an `mp.Pool` with one 30 s
  budget (`DAMO-ConvAI/bird/llm/src/evaluation.py`, read 2026-11-20).
  The check comes every 100,000 steps. A job that meets its budget next
  to other jobs runs once more with no other job of the pool running,
  and that result counts. A worker that fails stops the run.
  Evaluations write `exec_timeouts`; pair counts carry
  `questions_gold_timeout` and `samples_exec_timeout` when not zero.
  Budgets unchanged (30 s BIRD pair, 60 s Spider query).
- Checked on the Mac: the committed predictions scored again through
  the pool give the committed EX, 1,675 of 2,147 on Spider test (k = 0
  round 4, 78.02) and 452 of 1,534 on BIRD dev (base student, 29.47;
  its 3 timeouts time out alone too). 520 tests pass.
- BIRD scorer is v3. The Spider scorer keeps its name (my choice: under
  the threads no Spider gold met the budget and no evaluation row was
  lost; a new name would stop the running Spider lines at their
  identity checks).
- `scripts/relabel_samples.py` labels the samples of `bird/read` again
  into `fedpref_bird_base_p2_ddl_alpha01_ev3_s0`; the BIRD DPO lines
  (`bird_k0`, `bird_fixed`, `bird_k0_gold`) run in `_ev3` roots and wait
  for it (`bird/relabel`, `bird/read_relabelled`). The first read stays
  as it is.

Not done: the relabel has not run (how many of the 184 come back is not
known; 151 fit by their time alone); the pool has not run on Windows.
Open for the owner: the label step runs a gold twice in one budget, so
the 13 golds of 15 to 30 s stay `gold_error`; running the gold once per
question would take them in (0.14% of the questions).

## 2026-11-20: a stopped and continued run keeps its results and its totals (owner; code `a1679b75`)

Owner: later runs must give the right numbers whatever is restarted,
stopped or continued. Read through every step for what a stop does.

Found wrong and fixed:

- SFT with dropout (FedAvg SFT, centralized SFT; LoRA dropout 0.05). A
  call that continued a checkpoint seeded itself again, so its dropout
  masks were not those of the uninterrupted training: a valid training,
  but another one. The checkpoint now holds the state of torch's
  generators; the test stops a training with dropout at a checkpoint,
  continues it and gets the same weights, and fails without the fix. No
  committed result is touched: all 20 FedAvg SFT client trainings ran in
  one call. `refs/central_sft` was stopped in epoch 1 under the earlier
  code: its continuation of that epoch is not the uninterrupted one
  (logged here so the row is read with it); from its next checkpoint on
  it is.
- Times of a continued DPO training covered the last call only. Now each
  update keeps its seconds in the checkpoint and the reference pass keeps
  its own, so `update_seconds` and `reference_seconds` count the whole
  training once whatever the number of calls (`calls`); peak memory is
  over all calls.
- Times of a continued SFT training: `calls`,
  `elapsed_seconds_all_calls` and the peak over all calls, next to the
  last call's numbers.
- Sampling and labels: a call killed inside the step left no trace and
  the next call's entry looked like the whole step. Each step now writes
  a `started` entry before and a `done` entry after, with the questions
  it found left; `round.json` sums them and `complete` is false when a
  call was stopped inside a step (its times are then in the task log).

Checked and already right: a continued DPO training equals the
uninterrupted one (seeded pair order, no dropout, test on the weights);
samples and labels are kept per question, evaluations per row; pairs
are rebuilt from the samples and compared; aggregation and publication
are written whole or not at all.

Where a part is unknown (a checkpoint of earlier code) the total is
`null`, never a part given as the whole. The rule is in
`fedicl-sql/AGENTS.md` (Hard rules) and
`docs/PROTOCOL_V2.md`, "Runs that are stopped and continued". 510 tests
pass on the committed tree. Not run on the server: the first round that
starts after the next pull writes the new fields.

## 2026-11-20: wall times of the finished tasks are in Git: 46 tasks since the reset (result `5aa73a62`, code `a2230da9`)

`scripts/log_times.py` ran on the server's logs: one file per finished
task under `audits/protocol_v2/run_times/`. The steps it reads cover 98%
or more of each round's time, so the parser matches the real logs. Its
cut was the day 2026-11-17, which let in 13 tasks of the earlier setup
from that morning (`gate_s0`, `sqlcv2_s0`, `synvc_s0`, `vote_s0`); the
cut is now 2026-11-17 11:20 and those 13 files are removed.

Spider, wall time per round on one A5000 (h:mm; FedAvg SFT from its own
records):

| Round | FedAvg SFT, training | DPO from the base student (k = 0): sampling + labels + training | Pairs |
|---|---|---|---|
| 1 | 2:02 | 0:20 + 3:05 | 8,908 |
| 2 | 2:05 | 0:19 + 1:45 | 4,566 |
| 3 | 2:06 | 0:19 + 1:15 | 3,222 |
| 4 | 2:11 | 0:18 + 1:06 | 2,740 |
| All | 8:24 | 8:27 | |

- Four rounds cost the same wall time for both lines (8:24 against
  8:27) and end at 74.71 against 78.02. A DPO round gets cheaper each
  round because fewer questions stay mixed.
- Within a DPO round's training about one fifth is the reference pass
  (round 1: 0:36 of 3:05).
- Round 1 with the gold rule: 14,050 pairs, 4:15 of training.
- `bird/read`: sampling 0:35, labels 2:42 with 4 workers (Spider: 0:02
  with 16). Labels are 82% of a BIRD sampling step.

What the earlier rounds now hold for the paper: EX and EM per question
with the prediction and the error; question kinds, samples by outcome
and pairs per client; loss, margin and accuracy per update; peak
memory; update norms and cosines; wall time per step. Not held and not
recoverable without running again: the preference and NLL parts of the
loss per update. Not held but countable on the server without a GPU:
tokens trained on (from the pairs). Bytes sent follow from the adapter
size (73,911,080 bytes) and the clients that trained.

Stops, checked against the files (owner: do stops change the numbers):

- Results. Every evaluation ran in one start. FedAvg SFT: the task was
  stopped twice, both times between rounds; all 20 client trainings are
  recorded as `fresh`. DPO: a stop inside a client's training continues
  from a checkpoint (adapter, optimizer, schedule; every 25 updates),
  the order of the pairs is a seeded shuffle and the LoRA dropout is 0,
  so the continued training is the uninterrupted one (the test compares
  the weights, equal to 1e-6). Two clients were continued this way:
  client 3 of `decide/k0_gold/round_1` (from update 25 of 206) and
  client 4 of `decide/wrfirst/round_1` (from 75 of 148). The stop of
  `dpo_k2/round_1` fell after client 1. No round was stopped while
  sampling.
- Times. The table above uses only rounds run in one start. A continued
  round's task total also holds the updates done again after the last
  checkpoint, and its interrupted client has no full step. Times are
  wall time on a machine whose other card may run a task: five
  trainings on the same 8,026 pairs took 3:02 to 3:08, so that effect
  is about 3%. The FedAvg column is the trainer's own clock; by the
  task log the four rounds with their four evaluations took 8:45.

## 2026-11-20: loss parts, setup time and environment recorded; times of finished tasks read from the logs (owner; code `03f0eb9a`, `15032280`)

Owner: later runs must hold every result and setting the paper needs,
and the earlier runs are filled in from the logs on the server.

- Later runs (every task that starts after the server pulls the code):
  each update's loss is recorded with its preference part and its NLL
  part; `timing` gains the seconds before the first update; `round.json`
  carries the runtime environment. With the
  entry below this closes what was missing in the preference rounds. A
  call that continues a checkpoint written by the earlier code works;
  its earlier updates keep the total loss only.
- Earlier runs: `scripts/log_times.py` reads `.queue_state/logs/` on the
  server and writes `audits/protocol_v2/run_times/<task id>.json` for
  every task that finished since 2026-11-17: per start of the task the
  GPU, command, start, end, seconds and exit code, and the steps its
  lines show (generation, labels per client, training per client with
  the reference pass and the updates, aggregation). A file is written
  once and never changed, because the publication step refuses a
  checkout with changed tracked files; a rerun adds the tasks finished
  since. Tested on logs built from the code's own format strings, not
  yet on the server's logs: the first run there is the check
  (`PIPELINE_NEXT.md`, Run now).
- What the logs cannot give back for the rounds already run: the
  preference and NLL parts of the loss. Token counts can still be
  counted from the pairs, which are on the server only.

`docs/PROTOCOL_V2.md`, section "What each run records", lists the files
per kind of run. 502 tests pass.

## 2026-11-19: base student on the BIRD clients: a correct SQL among 10 samples for 52.4% of the questions (results `55b883c9`, `799543a1`)

`bird/read`: 10 samples at T 1.0 for each of the 9,428 BIRD train
questions at 5 clients, labelled by execution under the 30 s budget
with 4 workers; 20:23 to 23:42. Spider, same read: 87.6% with a correct
sample, 12% all wrong.

| Client | Questions | All correct | Mixed | All wrong | Gold fails | of them: budget / SQL error | Pairs (2 per mixed question) | Sample accuracy |
|---|---|---|---|---|---|---|---|---|
| 1 | 2,011 | 34 | 1,142 | 817 | 18 | 14 / 4 | 2,284 | 23.6% |
| 2 | 1,595 | 26 | 783 | 695 | 91 | 85 / 6 | 1,566 | 17.5% |
| 3 | 2,080 | 25 | 1,119 | 925 | 11 | 11 / 0 | 2,238 | 18.8% |
| 4 | 683 | 20 | 337 | 325 | 1 | 1 / 0 | 674 | 21.3% |
| 5 | 3,059 | 51 | 1,402 | 1,193 | 413 | 73 / 340 | 2,804 | 18.2% |
| All | 9,428 | 156 (1.7%) | 4,783 (50.7%) | 3,955 (41.9%) | 534 (5.7%) | 184 / 350 | 9,566 | 19.6% |

- DPO from the base student without gold trains on half of the BIRD
  questions (4,783 of 9,428); 3,955 questions have no correct sample
  and give no pair. On Spider that share was 12%. The gold rule
  (`bird_k0_gold/round_1`, queued) adds those 3,955 questions; this is
  where it is read with the most at stake.
- Gold fails, 534: 350 SQL errors as counted before (`retail_world`
  330, `works_cycles` 10, `app_store` 6, `shooting` 4; 208 `no such
  column`, 142 `no such table`) and 184 golds that met the 30 s budget
  (`donor` 71, `retails` 34, `world_development_indicators` 20,
  `language_corpus` 16, `movie_platform` 11, `talkingdata` 11,
  `bike_share_1` 8, others 13). About 50 were expected
  (`fedicl-sql/AGENTS.md`); whether the other 130 are slow golds or the
  effect of 4 labels running at once is read by timing each gold alone (`label_timeouts --retime`,
  `PIPELINE_NEXT.md`). Until then the workers stay at 4.
- Samples that met the budget: 196 of 94,280 (0.2%), in 154 questions;
  10 samples in 8 questions were left without a label because the
  budget ended on the gold.
- 8,947 samples (9.5%) were cut at 256 new tokens at T 1.0 (greedy on
  BIRD dev: 1 of 1,534). They count as wrong samples.
- 271 questions have a gold that returns no rows (186 of them mixed):
  a sample that returns no rows is labelled correct there.

The split of the gold fails was counted by `scripts/label_timeouts.py`
(code `0063d2a3`).

## 2026-11-19: what the result files record, checked; wall time added to the preference rounds (owner; code `5f34c048`)

Owner: is everything recorded that the paper may need, so that nothing
has to run again. Checked on the committed files. Evaluations: one row
per question with the prompt, the prediction, EX, EM, the execution
error, token counts and the finish reason, so every accuracy breakdown
(per database, BIRD difficulty, error kinds, tests) is computed later
without a GPU. FedAvg SFT rounds: seconds, examples, updates, loss, peak
memory per client and bytes sent. Preference rounds: pairs and question
kinds per client, loss, margin and accuracy per update, peak memory,
update norms and cosines; they had no wall time, token count or bytes
sent in the files (times were only in the console and in the logs on
the server). Added from this commit on, for every run that starts after
the server pulls it: per client `timing` (seconds of the call and of the
updates, updates measured in this call, the update it resumed from) and
`sequence_tokens` in `client_N_train.json` and `round.json`;
`timing.json` in the round's folder with the seconds of the generation
and of each client's labels (for a pair read: `pair_read/timing_rN.json`);
`communication_bytes` in `round.json`. None of it enters a signature or
an identity (496 tests pass). For the rounds already run, the times are
in the logs on the server (`.queue_state/logs/`, a timestamp per line)
and in no committed file; bytes sent follow from the adapter size
(73,911,080 bytes, as in the FedAvg record). Not recorded and not added:
the preference and NLL parts of the loss per update (the total, the
margin and the accuracy are). Adapters, samples and logs exist on the
server's drive D only.

## 2026-11-19: what CMC and JIIS require and publish, read (owner; `JOURNAL_BAR.md`)

Owner: have the two target journals researched for what to learn before
writing. 7 CMC papers read in full, 4 JIIS papers in full and 5 by
abstract; the closest two (LESFT at CMC, GradeSQL at JIIS) read a second
time from the source. One seed with McNemar tests is the protocol of
GradeSQL (JIIS, "a fixed seed of 42", Bonferroni correction) and more
than any CMC paper read reports. The gap against both samples is one
model: every CMC language-model paper has 3 or more (LESFT: Qwen2.5-0.5B,
1.5B, 3B), GradeSQL has 7. Also seen in the federated papers and not in
our plan yet: a cost or communication table, one federated factor
varied, 4 or more baselines. JIIS fits the topic better and costs
nothing (25 pages, LaTeX); CMC is faster (USD 1,600 for 15 pages). Both
require the use of AI tools to be disclosed. Not verified: the SJR and
JCR quartiles. Nothing is queued from this; which gaps to close is the
owner's decision.

## 2026-11-19: the gold line is carried on: round 2 on Spider, round 1 on BIRD (owner; queue `1ac2c545`)

Owner: the k = 0 line with gold was higher at round 1 (76.67 against
75.87) and that is enough to follow it; its level after more rounds was
never read. The rule `--gold-chosen --gold-on-empty-databases` uses the
gold SQL only where the samples give no correct side (all-wrong
questions; databases without rows), so DPO stays the main part and the
all-correct questions are left alone. Its pairs do not run out the way
the k = 0 line's do (8,908, 4,566, 3,222, 2,740). Queued:
`k0_gold/round_2` (Spider, on-policy, in the root of `decide/k0_gold`;
the round 1 command with another round number), first among the tasks
not started so that GPU 1 takes it at once; read against k = 0 round 2
(77.18; 92 / 398), rounds 3 and 4 follow if it still rises.
`bird_k0_gold/round_1` (BIRD, same rule, samples of `bird/read` copied
into a root of its own), after `bird_k0/round_1`; read against
`bird_k0` and `bird_sft` at 1 round. BIRD train has no database without
rows, so there the rule is gold as chosen for all-wrong questions. Each
with evaluation and publications (test; 495 tests pass, 2 skipped).
Reading note: round 1 of the gold line trains on 14,050 pairs, about
the pairs of k = 0 rounds 1 and 2 together (13,474; 77.18), so at equal
rounds it has trained more. Proposed in chat and dropped, not run: NLL
on the gold SQL for every question without a pair in the same local
loss as DPO; by round 3 only 19% of the questions give a pair, so most
of such a round would be SFT (owner).

## 2026-11-19: the wrong-result count hides a turnover; the three lines solve different questions (no new run)

Question by question on Spider test from the committed predictions (C
correct, E execution error, W wrong result; script run in chat, not
committed). From the untrained student (C 1,461, E 287, W 399):

| To | E to C | E to W | E to E | W to C | W to E | W to W | C to W | C to E |
|---|---|---|---|---|---|---|---|---|
| FedAvg SFT round 4 | 107 | 77 | 103 | 128 | 38 | 233 | 60 | 32 |
| k = 0 round 4 | 147 | 94 | 46 | 130 | 13 | 256 | 53 | 10 |
| k = 2 DPO round 2 | 144 | 93 | 50 | 157 | 19 | 223 | 68 | 15 |
| k = 3 DPO round 1 | 139 | 87 | 61 | 167 | 24 | 208 | 67 | 26 |

The wrong results near 400 in every run are a net figure: each line
fixes 130 to 167 of the 399, takes in 87 to 94 questions that used to
fail to execute, and breaks 53 to 68 that were right. This corrects the
wording of the entry "the wrong results are where the untrained student
left them" below: the count stays, the questions do not. Across the
three lines at 4 rounds (k = 0, 2, 3; 1,675, 1,679, 1,674 right): right
in all three 1,508, right in at least one 1,830 (85.2%), wrong in all
three 317; wrong in every run of the table and the untrained student
256. Reading: the lines reach the same EX on partly different questions
(322 are solved by some and not all), and each loses 63 to 93 questions
the untrained student had right. No run so far tests a round that
trains on the gold SQL and on the pairs in one local loss.

## 2026-11-19: on-policy rounds read on BIRD: round 2 on the round 1 pairs queued (owner; queue `6b18a407`)

Owner: carry out the read of on-policy rounds on BIRD. On Spider at
k = 2, round 2 on the round 1 pairs with a fixed reference gives 78.02
against 78.20 on-policy (p 0.78) with 8,026 pairs against 3,354, so
re-sampling shows no gain there; BIRD is where the base student is weak
and the samples may change more between rounds. Queued after
`bird_k0` round 2: `bird_fixed/round_2`, the command of
`bird_k0/round_2` in a root of its own
(`fedpref_bird_base_p2_fixed_ddl_alpha01_s0`) with `--continue-from` the
`bird_k0` root at round 1, `--samples-from-round 1` and
`--fixed-reference`; then its evaluation on BIRD dev and both
publications. It trains one round and samples nothing. Checked before
queuing (new test): a line that continues a line from the base student
with both flags trains from that line's round 1 global adapter, on that
line's round 1 pairs, with that line's fresh LoRA initialisation (the
base student) as the reference, and writes nothing in that line's root.
494 tests pass, 2 skipped. Not run: nothing on BIRD has trained yet;
time (3 h) and memory are estimates. The matching round on Spider from
k = 0 is not queued.

## 2026-11-19: base student on BIRD dev: 29.47, 42% of the outputs fail to execute (result `bfa497a8`)

`bird/zs`: base student, BIRD dev (1,534 rows), evidence, `ddl` prompt,
greedy, 256 new tokens: EX 29.47 (452 right; easy 44.33, medium 34.53,
hard 21.78, extra 15.81 by structural hardness), EM 4.69. Execution
errors 646 (42.1%), wrong results 436 (28.4%). Of the errors, 570 are
`no such column`: in 529 the column is in the prompt's schema and is
taken from the wrong table or alias, in 11 it is spelled another way, in
30 it is not in the schema (counted with a pattern over the schema text
of the prompt). The rest: 29 syntax, 26 `no such function`, 10 misuse of
an aggregate, 7 `no such table`, 3 timeouts of the 30 s pair budget
(rows 106 and 369 on the prediction, row 701 on the gold SQL).
One output is cut at 256 tokens. By database EX runs from 11.2
(`california_schools`, 63% errors) to 42.6 (`european_football_2`). The
run took 272 s. Reading: the 256-token limit is not a factor on BIRD dev
(1 row), and the budget costs 3 rows. On Spider the same student starts
at 68.05 with 13% execution errors, and training removed mostly those;
on BIRD the errors are three times that share, so there is more of what
the method has removed so far. The level printed in the Qwen2.5-Coder
report for this size is in a figure only (Figure 12, no table), so it is
not compared here.

## 2026-11-19: k = 3 gives 77.97 at 4 rounds: no gain from the SFT stage on Spider at k = 0, 2 or 3 (results `bc901890`, `b3075597`)

`decide/k3`: DPO + NLL round 1 from FedAvg SFT round 3, 2 random pairs
per question (7,220 pairs from 4,629 mixed questions; all wrong 483, all
correct 3,544; 452 updates; peak reserved 17.01 to 18.94 GiB). Spider
test: 77.97 (easy 91.28, medium 80.86, hard 72.35, extra 60.78), EM
65.11, execution errors 111, wrong results 362, one cut output.

| At 4 total rounds | EX | exec errors | wrong results | k = 3 fixed | k = 3 broke | p |
|---|---|---|---|---|---|---|
| k = 3 (3 SFT + 1 DPO) | 77.97 | 111 | 362 | | | |
| k = 2 (2 SFT + 2 DPO) | 78.20 | 84 | 384 | 68 | 73 | 0.74 |
| k = 0 (4 DPO) | 78.02 | 69 | 403 | 133 | 134 | 1.00 |
| FedAvg SFT round 4 | 74.71 | 173 | 370 | 146 | 76 | 3e-06 |

Against its start (FedAvg round 3, 74.71): fixed 149, broke 79,
p 4e-06. Reading: at 4 total rounds the three lines are the same within
a rerun (77.97, 78.20, 78.02), each 3.3 to 3.5 above FedAvg SFT. More
SFT rounds before DPO leave more execution errors and fewer wrong
results (69 / 403, 84 / 384, 111 / 362), the same trade seen with gold
inside the round, and the sum does not move. On Spider the SFT stage is
not a part that shows an effect; BIRD is read next.

## 2026-11-19: queue turned to what settles the method: SFT and DPO from the base student on BIRD; the long Spider DPO line dropped (owner; queue `186aaf58`, `80b6f287`)

Owner: drop the long DPO line from FedAvg round 3 (`dpo/after_fedavg`)
and queue what is needed to settle the method. Settled on Spider: DPO +
NLL with execution labels on the model's own samples (NLL term and
preference term each show a gain). Open: the FedAvg SFT stage (no gain
on Spider at 3 and 4 rounds; the owner's concern is a harder dataset)
and, after it, a gold path for the questions without a correct sample.
Queued after `bird/read`, in this order, each round evaluated on BIRD
dev and published: `bird_sft/round_1` (FedAvg SFT on the BIRD clients),
`bird_k0/round_1` (DPO + NLL from the base student on the samples of
`bird/read`), `bird_sft/round_2`, `bird_k0/round_2`. The FedAvg commands
are those of the Spider line with the BIRD split, profile, schema text,
stage label and root; the DPO rounds those of the Spider k = 0 line with
the BIRD split, profile, schema text, root and 4 score workers, and one
setup with `bird/read` (test; 492 tests pass, 2 skipped with the removed
curve). Read at the same number of rounds. The line with an SFT stage on
BIRD (DPO from a `bird_sft` round) and the gold path are queued after
round 1 of both lines and the read are in. The curve
`fedpref_sft_ddlrows_alpha01_s0/dpo` and its task are removed from the
queue; `decide/k3` keeps its one round. Centralized SFT on Spider now
follows the BIRD rounds. One commit (`186aaf58`) emptied
`tests/test_active_queue.py` by mistake; restored in `80b6f287`, no run
was affected.

## 2026-11-19: the rejected-side rules flip the error type on the same questions (no new run)

Question by question on Spider test, from the committed predictions
(outcome C correct, E execution error, W wrong result; the script was run
in chat and is not committed):

| Pair | E to W | W to E | E to C | W to C | C to E or W |
|---|---|---|---|---|---|
| random R1 (`be787676`) to wrong-result first R1 (`cd4727a7`) | 6 | 38 | 11 | 27 | 42 |
| random R2 (`5c33e622`) to wrong-result first R2 (`06e81fdf`) | 5 | 16 | 5 | 12 | 28 |
| random R1 to gold chosen (`cf644e95`) | 13 | 27 | 11 | 27 | 39 |
| k = 0 R1 (`96007ff6`) to k = 0 gold rule (`9e7c66b0`) | 43 | 10 | 26 | 64 | 73 |

Reading: most of the drop in wrong results under wrong-result first is
the same questions turning into execution errors (38 of 43), and most of
the drop in execution errors under the gold rule is the same questions
turning into wrong results (43 of 44). About 320-356 wrong results and
74-82 execution errors stay in both runs of each pair. The rules change
how the model fails on questions it does not solve; they do not add
correct answers. A rule that mixes both rejected kinds can at most hold
back these flips (about 40 questions per run), not reach the stable
errors.

## 2026-11-19: BIRD zero-shot and pair read queued after k = 3 (owner; queue `4045d3af`)

Owner: queue the two BIRD runs, labels with 4 workers. `bird/zs` (base
student on BIRD dev, evidence, `ddl`, arm `zs_bird_ddl_vllm_inproc`) and
`bird/read` (10 samples per question at T 1.0 from the base student on
the BIRD `alpha_0.1/k5` clients, labelled with the BIRD evaluator,
`--score-workers 4`, root `fedpref_bird_base_p2_ddl_alpha01_s0`, 2 pairs
per question so that round 1 from the base student reuses the samples),
each with its publication, after `decide/k3` and before centralized SFT.
The read differs from `pairread/base_ddl_rows` in split, profile, schema
style, root, pairs per question and score workers; the zero-shot from
`prompt/zs_ddl_rows` in arm, set and schema style (test; 493 tests pass).
No training in either. Not measured on BIRD: run time and the share of
samples that hit the 30 s budget.

## 2026-11-19: wrong-result rejects in round 2 trade error types again, not kept (results `0f698bfa`, `06e81fdf`)

`decide/wr_round2`: DPO round 2 after dpo_k2 round 1, same samples as
dpo_k2 round 2 (3,354 pairs), rejected side from wrong results first
(2,198 wrong-result rejects against 1,921). Spider test: 77.69 (easy
91.70, medium 80.98, hard 70.84, extra 60.22), execution errors 107,
wrong results 372, no cut output.

| Against | EX | exec errors | wrong results | Fixed | Broke | p |
|---|---|---|---|---|---|---|
| dpo_k2 round 2, random pairs | 78.20 | 84 | 384 | 17 | 28 | 0.14 |
| dpo_k2 round 1 (its start) | 77.46 | 99 | 385 | 43 | 38 | 0.66 |
| k = 0 round 4 | 78.02 | 69 | 403 | 115 | 122 | 0.70 |

As in round 1: 12 fewer wrong results, 23 more execution errors, EX 0.51
lower (p 0.14). The rule moves errors from one type to the other at a
loss and is not kept; the first queued use of `--continue-from` ran
without a stop. Peak reserved 14.39-18.97 GiB, 211 updates.

## 2026-11-19: the 256-token limit and the execution budgets against the published code (no run)

Read today in the code of each source:

| Source | New tokens | Execution budget | A timeout scores |
|---|---|---|---|
| BIRD official (`DAMO-ConvAI/bird/llm/src`: `gpt_request.py`, `evaluation.py`) | 256 | 30 s for prediction and gold together (`--meta_time_out` default 30.0) | 0 |
| Spider test-suite (`taoyds/test-suite-sql-eval`, `exec_eval.py`) | | 60 s per query (`TIMEOUT = 60`) | 0 ("wrong if execution fails") |
| CodeS (`text2sql_zero_shot.py`) | 256, 4 beams | | |
| Qwen2.5-Coder evaluation (`bird-spider/test.sh`) | 1,024 | 30 s | |
| OmniSQL (README; `infer.py` not found) | 2,048, output holds reasoning | | |

Ours: 256 new tokens, 60 s per query on Spider, 30 s per pair on BIRD, a
timeout scores 0: the official evaluators' values. On Spider test the
limit does not bind: over the 20 committed arms the median output is
20-27 tokens, the 99th percentile 84-126, the longest finished output
209; 16 arms have no cut output, the others 2-4 (outputs that run to the
limit, not long SQL). Timeouts on Spider test: 0 or 1 of 2,147 per arm.
On BIRD 6 of the 1,534 dev golds and 1 train gold are longer than 256
tokens; the outputs of the model on BIRD are not measured yet. Kept as
they are; the zero-shot run on BIRD dev gives the number of cut outputs
and of timeouts, and the limit on BIRD is read again on that.

## 2026-11-19: BIRD train as a second set of clients, set up and checked on the Mac; nothing queued (owner; code `ab6bc960`..`3cfd42d3`)

Owner: BIRD clients are prepared before the decision on the SFT stage,
with the prompt as BIRD is prompted (evidence). Done on the Mac, CPU
only.

- Prompt, checked against the Qwen2.5-Coder evaluation code
  (`qwencoder-eval/instruct/bird-spider/sql_suites/preprocess_bird.py`,
  read twice, the second time independently): schema is `CREATE TABLE`
  text without rows (`SCHEMA_EXAMPLE_ROWS = 0`, our `ddl`); the lines
  `-- External Knowledge: {evidence}` and `-- Using valid SQLite and
  understanding External Knowledge, ...` go on every question, the
  evidence as given. Ours left them out when the evidence was empty and
  stripped it: fixed. On all 1,534 BIRD dev rows our text equals the
  source's except `sqlite_sequence`, which our schema leaves out (4 dev
  databases; as on Spider, kept). The Spider prompt hashes are pinned by
  a test and did not change.
- Length (limit 7,168): `ddl` longest BIRD train sequence 6,807 tokens,
  longest dev prompt 2,207, no row over; `ddl_rows` 872 train rows over
  (longest 220,797), `ddl_values` 474. BIRD runs use `ddl`.
- Split `BIRD/original_train9428_dev1534/federated/alpha_0.1/k5`, built
  as the Spider main split (Dirichlet 0.1 over 4 database tiers, seed
  42, a database whole at one client): 16 / 14 / 16 / 5 / 18 databases,
  2,011 / 1,595 / 2,080 / 683 / 3,059 questions. Tiers by share of hard
  and extra golds, the levels from Spider's hardness rules on sqlglot's
  parse (Spider's own parser reads 15% of BIRD golds; the new one agrees
  with it on 8,656 of 8,658 Spider train golds). Checked here: the five
  files are the centralized train rows exactly, no database at two
  clients, none shared with BIRD dev.
- Golds (one thread on the Mac): no BIRD train database is empty; 350
  golds raise an SQL error (340 at client 5, mostly `retail_world`), 9
  run over 60 s, about 40 more spend the 30 s pair budget; 398 questions
  would be labelled `gold_error` and give no pair. Two BIRD dev golds
  spend the pair budget and score 0 for every arm.
- Code: a public pool that holds a client database is rejected; BIRD
  rows take hardness from the sqlglot rules; a pair whose budget ends on
  the gold side is a timeout instead of a crash, and such a sample gets
  no label (it ran, its result was never compared) rather than
  `exec_error`. 492 tests pass.
- Not done: no run on the server. The memory of BIRD training is not
  measured, the labels under several score workers are not timed, the
  FedAvg SFT command was read but not run.

Open for the owner: queue the read of the base student on BIRD
(sampling and labels, no training) and the zero-shot evaluation on BIRD
dev; keep or drop the 350 failing golds for FedAvg SFT; 256 new tokens
(6 BIRD dev golds are longer).

## 2026-11-19: k = 0 round 4 reaches 78.02, equal to the k = 2 line at 4 rounds (results `4fd84bee`, `4215a7e1`)

Spider test: 78.02 (easy 88.94, medium 81.10, hard 72.57, extra 63.31),
EM 54.73, execution errors 69, wrong results 403, no cut output.

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) |
|---|---|---|---|
| 1 | 72.43 | | 75.87 |
| 2 | 74.10 | | 77.18 |
| 3 | 74.71 | 77.46 | 77.69 |
| 4 | 74.71 | 78.20 | 78.02 |

| k = 0 round 4 against | Fixed | Broke | p |
|---|---|---|---|
| k = 0 round 3 (77.69) | 48 | 41 | 0.53 |
| k = 2 DPO round 2 (78.20; 4 rounds each) | 116 | 120 | 0.85 |
| fixed pairs and reference with NLL, round 2 (78.02) | 121 | 121 | 1.0 |
| FedAvg round 4 (74.71; 4 rounds each) | 178 | 107 | 3.1e-05 |

At 3 and at 4 total rounds the line without the FedAvg SFT stage equals
the line with it (p 0.80, p 0.85): on Spider with this student the SFT
stage shows no gain. The k = 0 line: 75.87, 77.18, 77.69, 78.02; the
steps after round 2 are within what a rerun gives (+0.51 p 0.27, +0.33
p 0.53). Round 4 trained on 2,740 pairs (174 updates; rounds 1-3: 8,908,
4,566, 3,222), peak 18.84 GiB. Training questions with no correct
sample: 1,074, 902, 886, 860 at the start of rounds 1-4. Whether the
stage stays in the method is the owner's decision; the owner's concern
(2026-11-19) is a dataset or model where the base student has no correct
sample for many more questions, so BIRD clients are being set up before
the decision.

## 2026-11-19: reading: training removes execution errors; the wrong results are where the untrained student left them (no new run)

Spider test, from the committed metrics:

| Run | EX | EM | exec errors | wrong results |
|---|---|---|---|---|
| Student without training | 68.05 | 53.33 | 287 | 399 |
| FedAvg SFT round 4 | 74.71 | 64.46 | 173 | 370 |
| k = 2, DPO round 2 | 78.20 | 64.42 | 84 | 384 |
| k = 0, DPO round 3 | 77.69 | 55.29 | 82 | 397 |

Every run so far has 342-444 wrong results against 399 without
training; the EX gains are execution errors removed (287 to 173 with
gold SFT, to 82-84 with DPO). Gold SFT moves EM by 11 points and DPO
from the base student by 2: the SFT stage teaches the form of the gold
SQL, which EX does not count. On the training questions the untrained
student already has a correct SQL among its 10 samples for 7,582 of
8,659 (87.6%). Whether Qwen2.5-Coder saw Spider in pre-training is not
stated in its report (arXiv 2409.12186, read 2026-11-19): section 7.4
evaluates on Spider and BIRD (split and metric not given, results only
in figure 12) and credits "finely crafted synthetic data during both
pre-training and fine-tuning" for the Text-to-SQL level; the data
sections name no Text-to-SQL dataset; the decontamination step (section
5, 10-gram overlap) names HumanEval, MBPP, GSM8K and MATH only.

## 2026-11-19: DPO from the base student matches the SFT-then-DPO line at 3 rounds; gold inside the round not kept (results `3f9ada19`, `9e7c66b0`, `2bdd4c73`, `a3fed6d6`, `548acdab`, `947ca9d8`)

Spider test, by total rounds trained (every row one federated round of
the 5 clients per round):

| Total rounds | FedAvg SFT | 2 SFT rounds then DPO (k = 2) | DPO from the base student (k = 0) | k = 0 with the gold rule |
|---|---|---|---|---|
| 1 | 72.43 | | 75.87 | 76.67 |
| 2 | 74.10 | | 77.18 | |
| 3 | 74.71 | 77.46 | 77.69 | |
| 4 | 74.71 | 78.20 | running | |

| Run | EX | easy | medium | hard | extra | exec errors | wrong results |
|---|---|---|---|---|---|---|---|
| k = 0 round 1 | 75.87 | 90.43 | 79.00 | 68.90 | 58.26 | 101 | 417 |
| k = 0 round 1, gold rule (`decide/k0_gold`) | 76.67 | 89.79 | 80.28 | 68.47 | 61.34 | 57 | 444 |
| k = 0 round 2 | 77.18 | 90.64 | 80.51 | 70.84 | 59.66 | 92 | 398 |
| k = 0 round 3 | 77.69 | 90.43 | 80.98 | 70.41 | 62.46 | 82 | 397 |
| k = 2, DPO round 1 (3 rounds) | 77.46 | 91.49 | 80.63 | 71.06 | 59.66 | 99 | 385 |
| k = 2, DPO round 2 (4 rounds) | 78.20 | 91.91 | 81.91 | 71.06 | 60.50 | 84 | 384 |

Question by question (fixed, broke, exact McNemar p):

| Compared | Fixed | Broke | p |
|---|---|---|---|
| k = 0 round 2 against round 1 | 69 | 41 | 0.0097 |
| k = 0 round 3 against round 2 | 46 | 35 | 0.27 |
| k = 0 round 2 against FedAvg round 2 (2 rounds each) | 166 | 100 | 6e-05 |
| k = 0 round 3 against FedAvg round 3 (3 rounds each) | 170 | 106 | 0.00014 |
| k = 0 round 3 against k = 2 DPO round 1 (3 rounds each) | 124 | 119 | 0.80 |
| k = 0 round 3 against k = 2 DPO round 2 (3 against 4 rounds) | 109 | 120 | 0.51 |
| k = 0 round 2 against k = 2 DPO round 1 (2 against 3 rounds) | 131 | 137 | 0.76 |
| gold rule against k = 0 round 1 | 90 | 73 | 0.21 |
| gold rule against k = 2 DPO round 1 (1 against 3 rounds) | 106 | 123 | 0.29 |
| k = 0 round 2 against the gold rule (2 against 1 round) | 90 | 79 | 0.44 |

The k = 0 line: at the same total rounds DPO from the base student is
3.08 above FedAvg SFT at 2 rounds and 2.98 at 3, and equal to the k = 2
line at 3 rounds (+0.23, p 0.80). The FedAvg SFT stage shows no gain at
3 rounds; round 4 (running) is read against 78.20. Round 2 is a gain by
the rule (+1.31, p 0.0097); round 3 adds 0.51 (p 0.27). Pairs per round
8,908, 4,566, 3,222 (288 and 204 updates in rounds 2 and 3). On the
training samples the line leaves more questions with no correct sample
than gold SFT does: 1,074 (base), 902 after round 1, 886 after round 2,
against 573 after 2 FedAvg SFT rounds.

The gold rule (`--gold-chosen --gold-on-empty-databases`, round 1 from
the base student, same samples as k = 0 round 1): 14,050 pairs against
8,908, 5,142 with the gold as chosen (3,110 on databases without rows,
2,912 of them at client 4; 2,032 on questions whose samples are all
wrong); rejected sides 9,284 execution errors and 4,765 wrong results
(k = 0 round 1: 5,339 and 3,568). Client 4 gets 6,064 pairs (weight
0.43 in the average, 0.28 before). On test: +0.80 (p 0.21), execution
errors 101 to 57 (the lowest of any row), wrong results 417 to 444, 4
cut outputs. Not kept by the rule; the two settings do not run alone.
The added pairs are mostly "gold against a SQL that does not run", and
that is what moves on test: 44 fewer execution errors, 27 more wrong
results. Peak reserved 17.38-18.99 GiB (client 4 17.63), 880 updates.
k = 0 rounds 2 and 3 peak 18.94 and 18.90 GiB.

Server: the results came one after another in the order a single worker
gives (k = 0 round 2, then `decide/k0_gold`, then the evaluations at
12:09 and 12:13, round 3 at 13:57), so GPU 0 has run alone since 07:00
(inferred from the publication times; the owner has not sent the
worker's lines).

## 2026-11-19: wrong-result rejects queued for round 2; the NLL term stays (owner; queue `d1a3aa9f`)

Owner: the method keeps the NLL term. Wrong results on Spider test by
run: FedAvg rounds 2 and 3 373 and 379; DPO + NLL round 1 385 (random),
382 (nearest), 368 (gold chosen); round 2 384 (on-policy), 375 (fixed);
RFT 365; wrong-result rejects first 342. The gain of every DPO run so far
is in execution errors (183 at the start, 84-117 after); only the
wrong-result rule moves the wrong results, and in round 1 it pays for it
with execution errors (146). In on-policy round 2, 1,433 of the 3,354
rejected sides are still execution errors. Queued before `decide/k3`:
`decide/wr_round2`, a line that takes dpo_k2 round 1 as its own
(`--continue-from`, first queued use) and runs round 2 on the samples of
dpo_k2 round 2 (copied) with `--pair-rule wrong_result_first`; the
command differs from dpo_k2 round 2 in the rule, the root and the two
continue flags (test; 467 tests pass on the Mac). Read against dpo_k2
round 2 (78.20; 84 and 384). Root
`fedpref_sftr2_rand1wr2_ddlrows_alpha01_s0`, arm
`fedpref_sftr2_rand1wr2_dpo_ddl_rows_a01_r2_vllm_inproc`.

## 2026-11-19: without the NLL term DPO gains nothing; wrong-result rejects trade error types (results `aa05e549`, `cd4727a7`, `3a4759b5`, `f8485b4b`)

Both runs are DPO round 1 from FedAvg round 2 on its samples (8,026
pairs each), one setting changed. Spider test:

| Run | EX | easy | medium | hard | extra | exec errors | wrong results |
|---|---|---|---|---|---|---|---|
| FedAvg round 2 (the start) | 74.10 | 89.36 | 78.65 | 65.23 | 54.62 | 183 | 373 |
| RFT (NLL on correct samples only) | 75.87 | 90.43 | 79.35 | 67.60 | 59.10 | 153 | 365 |
| DPO without NLL (`decide/nonll`) | 73.59 | 88.94 | 75.50 | 68.03 | 56.02 | 167 | 400 |
| DPO + NLL, wrong-result rejects first (`decide/wrfirst`) | 77.27 | 91.06 | 79.70 | 71.49 | 60.78 | 146 | 342 |
| DPO + NLL, random pairs (dpo_k2 round 1) | 77.46 | 91.49 | 80.63 | 71.06 | 59.66 | 99 | 385 |

No NLL (NLL weight 0, same pairs, pair hashes not compared): against
DPO + NLL fixed 62, broke 145, McNemar p < 1e-6; against its start
FedAvg round 2 fixed 157, broke 168, p 0.58; against RFT fixed 123,
broke 172, p 0.005. Training reaches a larger margin (1.47-2.81 against
1.01-1.67) with the same accuracy, larger updates (norms 1.53-2.34
against 1.35-2.12), and the median output grows from 23 to 27 tokens.
Reading: the preference term alone does not move the model from its
start (as the papers on SFT then plain DPO report, `DPO_RESEARCH.md`
2.1); the NLL term alone gives +1.77; both give +3.36. The NLL term is
a part of the method by the rule. Round 1 of federated DPO as
`DPO_RESEARCH.md` describes OpenFedLLM (plain DPO, fixed pairs, fixed
reference; the paper was not read again today) is this run, since
round 1 has the same pairs and reference either way: 73.59, 3.87 below
the method. The fixed line of 2026-11-18 (77.64, 78.02) kept the NLL
term, so it is not that baseline.

Wrong-result rejects first: 5,526 of the 8,026 rejected sides are wrong
results (random: 3,939). Against random pairs fixed 38, broke 42,
p 0.74: the same EX. Wrong results fall from 385 to 342 and execution
errors rise from 99 to 146: the rejected side decides which errors DPO
removes, at about one for one. Not kept by the rule (no gain of 0.5).
Peak reserved 12.65-19.03 GiB in both runs.

## 2026-11-19: a worker can stop itself at a given time (owner; code `3958a1af`)

Owner: GPU 1 runs until 07:00 and stops by itself.
`scripts.gpu_worker run --gpu 1 --until 07:00` stops the worker and its
task at that local time the way Ctrl+C does (on Windows the Ctrl+C event
of the console; if the worker still runs 3 min later it ends its own
process tree); the task stays due and another worker continues it. Run
on the Mac with a throwaway queue: the worker stopped at the minute,
exit 0, no child left (466 tests pass). Not run on Windows yet.

## 2026-11-19: gold inside the DPO round from the base student queued; k = 0 runs before k = 3 (owner; code `c1784b46`)

Owner: run the gold rule whole, not by half. From the base student
4,205 of the 8,659 questions give no pair in round 1: 1,631 all right,
1,074 all wrong, 1,497 right and wrong on databases without rows, 3
whose gold does not run; the SFT stage trains on all of them. The run
`decide/k0_gold` is `decide/k0` round 1 on the same samples with two
settings: `--gold-chosen` (gold as chosen for an all-wrong question, in
the code since the k = 2 run, where it gave 77.41 against 77.46) and the
new `--gold-on-empty-databases`: on a database without rows the chosen
side is the gold SQL and the rejected side is drawn from the wrong
samples (an execution error or another result than the gold is wrong
whatever the rows; only "correct" says nothing there). A question there
whose samples all match the gold result still gives no pair: NLL on the
gold alone for those is not written (cut; 192 of the 1,648 such
questions of client 4). Without the setting every rule keeps its
identity and pairs (464 tests pass on the Mac). Root
`fedpref_base_p2_goldrule_ddlrows_alpha01_s0`, arm
`fedpref_base_p2_goldrule_dpo_ddl_rows_a01_r1_vllm_inproc`; about 14,000
pairs against 8,908 (estimate), FedAvg weights by pair count, so client
4 weighs more. Read against 75.87 (kept at +0.5 with p below 0.05) and
77.46. No prompt was rendered again: the command is that of `decide/k0`
round 1 with the two flags and another root (test).

Queue order now: `decide/k0_gold`, `dpo_k0/round_2..4`, then `decide/k3`
(it was before the k = 0 line): the open question is the start of the
method, and k = 3 only tunes k. At 03:28-03:29 the owner's log shows
`decide/wrfirst` on GPU 1 (client 3, peak reserved 18.98 GiB) and
`decide/nonll` on GPU 0 (client 1 done), so both cards are free at about
05:45 (estimate).

## 2026-11-19: direction recorded: content generated by the clients for their databases; to run after the method is settled (owner)

Source: an idea scan by research agents (three on ways to raise EX, one on
the empty databases). Their reports are in chat only. Paper numbers below
were read through page fetches, not by eye, and the agents' counts on the
public Spider files are not committed.

Measured here on committed predictions (Spider test, 2,147 rows):

| Row | Correct | Execution errors | Wrong results |
|---|---|---|---|
| FedAvg round 3 | 1,604 | 164 | 379 |
| FedAvg round 4 | 1,604 | 173 | 370 |
| DPO round 2 (k = 2) | 1,679 | 84 | 384 |

The 75 questions gained over FedAvg round 4 are execution errors removed;
the wrong results do not fall. FedAvg rounds 3 and 4 give the same 74.71
with different predictions (44 questions each way).

Why the wrong results may not move (agent counts, not committed):

- The seven databases without rows hold 1,759 questions (20.3%), 792 of
  the 1,579 training SQL with two or more JOINs and 753 of the 1,446 with
  DISTINCT. They give no pair in the DPO rounds.
- The other databases are small (median 9.3 rows per table). Removing
  DISTINCT from the gold SQL leaves the result unchanged in 168 of 434
  cases.
- Pairs fall from 8,026 to 3,354 between DPO rounds 1 and 2 and the
  all-correct questions rise from 33% to 67% (read by an agent from the
  committed `round.json` files).

Direction (owner: recorded, not started). Each client generates content
for its own databases: rows in foreign-key order, typed values, seeded
with the literals of its own gold SQL, and for a gold SQL that still
returns nothing a chain of rows that satisfies its joins and filters. First
for the seven empty databases, then a few variants of every database, a
sample counting as correct only if it matches gold on every variant. The
samples of the 1,759 questions are already stored (sampling covers every
question; `skip_empty_databases` acts at the pair step), so a trial round
needs relabelling on CPU and training, no new sampling.

| Step | What | Where | Stop if |
|---|---|---|---|
| 1 | The generator; share of gold SQL with a non-empty result on the seven databases | Mac, CPU | under 85% |
| 2 | Relabel the stored round 1 samples; count the new pairs and what the rejected side is | server, CPU, about 1 h (estimate) | new pairs under 10% of the round's pairs, or the rejected side is mostly execution errors |
| 3 | One DPO round from FedAvg round 2 with the new pairs, against 77.46 | server, about 4 h GPU (estimate) | under +0.5 EX and wrong results still at 365 to 385 |

The thresholds of steps 1 and 2 were set here, not by the owner. After
step 3: variants for every database. Things the generator has to handle:
ties under ORDER BY ... LIMIT and MAX/MIN, self-joins, composite keys,
HAVING COUNT thresholds, NOT IN and EXCEPT, foreign keys declared wrongly
in the Spider schemas (take them from `tables.json`), and database size
(execution time for 10 samples per question).

Standing of the direction (owner, 2026-11-19): optional, taken up later
if wanted. The paper does not need it: without it, "a question on a
database without rows gives no pair" stays a line of the setup, and
Arctic-Text2SQL-R1 drops such data too.

- No gain by the reading rule (0.5 EX, p < 0.05): dropped, nothing in the
  paper changes.
- A gain with fewer wrong results: the method corrects errors of meaning
  for the first time, has a part of its own that wins an ablation row,
  and the gain adds to the gap, because FedAvg SFT executes nothing and
  federated DPO as published has no such step.
- A gain made only of execution errors: it is the 20% of questions put
  back to use; it can stay in the method and does not change the story.
  Step 2 tells these two cases apart before any GPU time.
- Order, if it is tried: before the runs over seeds and alphas. Tried
  after them, a win means running that package again with the new part.

Relation to earlier notes: the boundary-value form of counterexample
relabelling was dropped on 2026-11-18 (entry below). This form rests on
the empty databases and on general content variants, which that probe did
not measure. Prior work that trains with enriched or counterexample
databases exists (SQLoom, CoRE-DB, ReViSQL; `LITERATURE.md`, sections 1.20
and 1.21), so the claim would be the adaptation to clients that own their
databases, not the mechanism.

Other ideas of the scan, not planned:

| Idea | Agents' chance of +1.5 EX over 78.20 | Note |
|---|---|---|
| SQL written by the client on its own schema, checked by execution, with a model-written question (about 3k rows) | 35 to 40% | needs the decision of 2026-11-17 against unlabelled questions reopened; SPFT-SQL reports 78.0 to 82.3 on Spider test at this student with a 7B question writer, GAZP reports a loss for synthesis on training databases |
| Negatives sampled on databases the sampling model has not trained on (two folds) | 25% | no Text-to-SQL DPO paper found doing it |
| Distractor tables from the client's other databases in the prompt schema | 20 to 25% | SQLong: +1.4 to +1.7 on Spider test at 7B; FedAvg can use it too |
| The server as a sixth participant on public databases | 35 to 50% in level | adds data; the baselines get the same rows; a control row, not a part of the method |
| Reasoning before the SQL | 25% | breaks SQL-only output; 4 to 6 times the sampling tokens |

Checks the scan named that need no training, not run: FedAvg round 4 with
a retry when the SQL fails to execute (a reviewer's control for a gain
made of execution errors); the existing adapters on Spider-Syn, Realistic
and DK (the data is under `data/raw/`); the server step size swept over
the saved client adapters. The agents also put the level of this student
with a DDL prompt and greedy decoding at about 78 to 80 on Spider test in
the papers, so a gain of several points more on Spider test is not
expected.

## 2026-11-19: DPO round 1 from the base student reaches 75.87; k = 0 line queued to 4 rounds (results `1e999231`, `96007ff6`; queue `787c0197`)

`decide/k0`: DPO + NLL round 1 from the base student (no SFT stage), on
the samples of the pair read, 2 random pairs per question: 8,908 pairs
(1,062 / 1,896 / 2,470 / 2,458 / 1,022 per client), rejected side 5,339
execution errors and 3,568 wrong results. Of the 8,659 questions, 5,951
have right and wrong samples (1,497 of them on databases without rows,
which give no pair), 1,631 are all right, 1,074 all wrong. Spider test
75.87 (easy 90.43, medium 79.00, hard 68.90, extra 58.26); execution
errors 101, wrong results 417; 3 outputs are cut at 256 tokens (nested
subqueries that repeat); the rows compared below have none.

| Against | EX | fixed | broke | McNemar p |
|---|---|---|---|---|
| base student, zero-shot | 68.05 | 225 | 57 | < 1e-6 |
| FedAvg round 1 (same total: 1 round) | 72.43 | 168 | 94 | 6e-06 |
| FedAvg round 2 | 74.10 | 157 | 119 | 0.026 |
| FedAvg round 3 and round 4 | 74.71 | 156 | 131 | 0.16 |
| RFT round 1 from FedAvg round 2 | 75.87 | 122 | 122 | 1 |
| DPO round 1 from FedAvg round 2 | 77.46 | 114 | 148 | 0.041 |

Training: final accuracy 0.84-0.91, final margin 0.48-1.52; client
updates: norms 1.56-2.56, pairwise cosine 0.365-0.462 (DPO round 1 from
FedAvg round 2: 0.244-0.321); peak reserved 16.99-18.98 GiB; 559 updates;
round, evaluation and publications about 3 h 10 min. Client 4 has 2,458
pairs, not the 4,000 expected: 1,648 of its 3,479 questions are on
databases without rows.

Reading: one DPO + NLL round from the base student, with no gold SQL in
the loss, is above every FedAvg SFT round (+3.44 at the same single
round, +1.16 over the best, the latter not significant) and 1.59 below
one DPO round after two FedAvg rounds (three rounds in total). It removes
execution errors as the k = 2 line does (101 against 99) and leaves more
wrong results (417 against 385). Whether the SFT stage is needed is not
settled by one round: the comparison is at the same total rounds. By the
rule written before the run (about 74 or more), the k = 0 line runs to 4
rounds: `dpo_k0/round_2..4`, on-policy as dpo_k2 round 2, the command of
round 1 with another round number (462 tests pass on the Mac), placed
after the decision runs and before centralized SFT. Read: round 2 against
FedAvg round 2 (74.10), round 3 against 77.46, round 4 against 78.20 and
FedAvg round 4 (74.71).

## 2026-11-19: second card free; one publication at a time (owner; code `ee1615e8`)

Owner: GPU 1 is free, run tasks on it in parallel. The queue already
gives each card its own worker (a lock per card and per task); the
second worker takes the first ready task, `decide/wrfirst`, while GPU 0
runs `decide/k0`. `scripts/publish_results.py` now holds a lock file in
the Git directory, so two workers publishing at once wait for each other
instead of one failing on its push and stopping both (461 tests pass on
the Mac; the Windows lock call is the one `exclusive_lock` uses, not run
there yet). Pushed together with `0017c487`.

## 2026-11-19: fixed pairs and reference match on-policy at round 2 (results `6717c7f6`, `aaae06ad`)

Round 2 of `decide/fixed`: the 8,026 pairs of round 1 again (pair hashes
equal), reference FedAvg round 2, start the line's own round 1. Spider
test 78.02 (easy 91.70, medium 81.56, hard 70.41, extra 61.34);
execution errors 97, wrong results 375. Against on-policy round 2
(78.20; 84 and 384): fixed 54, broke 58, McNemar p 0.78. Against its own
round 1 (77.64): fixed 53, broke 45, p 0.48. Against FedAvg round 4:
fixed 159, broke 88, p 7e-06. Training: the first update of each client
has a margin of 0.58-1.57 (the policy starts away from the reference),
final accuracy 0.83-0.96, final margin 1.38-2.23; client updates: norms
1.06-1.62, pairwise cosine 0.031-0.092; peak reserved 12.93-18.92 GiB.
Reading: at round 2 on-policy rounds do not beat fixed pairs with a fixed
reference; the difference (0.18) is the size of a rerun, so by the rule
on-policy rounds are not shown to be a part of the method. On-policy
round 2 reaches the level with 3,354 pairs against 8,026 (about 210
updates against 505). The fixed line does not win, so no run with its
pairs cut follows. Both lines are at about 78 after two rounds.

## 2026-11-18: a line can continue another line's finished rounds (owner; code `0017c487`)

Owner: a finished round is not trained again for another line; the fixed
line should have reused DPO round 1 instead of spending 3 h 15 min on it.
`--continue-from <root> --continue-round N` (with `--continue-arm`) makes
rounds 1..N of a line those of another root with the same setup (the pair
rule may differ): the line trains from round N + 1 under its own
settings, and round 1's start (the fixed reference) and the samples of an
earlier round are read from the root that ran them. Arms without the flag
keep their identity and behaviour (461 tests pass on the Mac). In the main
table, federated DPO as published and the method then share round 1 for
every seed and alpha. Pushed on 2026-11-19 with the publication lock;
the server's publish step merges `origin/main` before each publish, so
the tasks that follow load it. No queued task uses the flag yet.

## 2026-11-18: fixed line round 1 repeats DPO round 1 within 0.18 EX (results `7ace0aa3`, `67c17163`)

Round 1 of `decide/fixed` is the training of dpo_k2 round 1 run again in
its own root: same samples, same 8,026 pairs (pair hashes equal per
client). Spider test 77.64 (easy 91.28, medium 81.21, hard 71.27, extra
59.38); execution errors 99, wrong results 381. Against dpo_k2 round 1
(77.46): fixed 14, broke 10, McNemar p 0.54; 154 of the 2,147 predicted
SQL differ in text. So running one DPO round again moves EX by about 0.2
and flips about 24 questions; a difference of that size between two
settings is noise. On-policy round 2 (78.20) is 0.56 above this rerun
(fixed 44, broke 32, p 0.21) and 0.74 above the first run (p 0.093).
Round 2 of the fixed line runs now. Round 1 was published 3 h 15 min
after the gold-chosen run.

## 2026-11-18: gold as chosen for all-wrong questions gives the same EX (results `674b993d`, `cf644e95`)

DPO round 1 from FedAvg round 2 on the samples of dpo_k2 round 1, with
the gold SQL as the chosen side for the questions whose 10 samples are
all wrong: 9,140 pairs against 8,026, of them 1,114 with gold as chosen
(per client 120 / 204 / 364 / 328 / 98; all-wrong questions on databases
without rows give none). Spider test 77.41 (easy 90.64, medium 80.98,
hard 70.84, extra 59.94); execution errors 117, wrong results 368.
Against DPO round 1 (77.46; 99 and 385): fixed 38, broke 39, McNemar
p 1. Against RFT: fixed 106, broke 73, p 0.017. Against FedAvg round 2:
fixed 141, broke 70, p 1e-06. Reading: no gain, so the setting is not
kept. Wrong results fall by 17 and execution errors rise by 18: the gold
pairs move rows between the two kinds and fix none on net. Its result
was published 3 h 45 min after RFT's (estimate for the run: 2.5 h).

## 2026-11-18: when a train database hides a boundary error (CPU, results `e16c8f75`)

Across the five Spider train clients, 77 distinct (database, SQL text)
entries matched a simple single-table numeric inequality on a populated
database. Toggling whether the boundary is included changed the result on
30 originals. Of the other 47, setting one existing numeric cell to the
boundary in an in-memory copy separated 38. Five still agreed, three had
no numeric row to edit and one database had an invalid foreign-key
declaration. Counts are for constructed mutants, with repeated SQL text
within a database counted once. They measure an instance's ability to
expose one class of error. The prevalence in student samples and the EX
effect of training on the corrected labels are open.

Reproduce from the code repository with `python3 scripts/probe_spider_boundaries.py`.
The deterministic probe and per-client counts are in the same commit.
Owner dropped counterexample relabelling. The owner found zero direct
boundary-operator swaps among the 370 executable wrong answers of FedAvg
R4 and the 384 of DPO R2. The pilot does not explain those errors.

At the FedAvg R2 checkpoint used to start DPO, greedy evaluation on
Spider test (2,147 questions, `0699ac6d`) gives 1,591 correct, 373
executable wrong answers and 183 execution errors. Ten samples from
that checkpoint at T=1.0 give 250 all-wrong questions (`762b74a2`).
At least 556 - 250 = 306 greedy failures therefore have a correct sample;
at least 373 - 250 = 123 are executable wrong answers with a correct
sample. These are set-size bounds from the published aggregates at the
start of DPO. The number of train questions for which forcing the greedy
answer into the rejected slot would change an existing pair is unknown.

## 2026-11-18: line without on-policy rounds queued next (owner; code `5aedf463`)

`--fixed-reference` keeps round 1's start as the DPO reference of every
round; with `--samples-from-round 1` it is federated DPO as published
(fixed pairs, fixed reference). The line `decide/fixed` runs two rounds
from FedAvg round 2 right after the gold-chosen run: round 1 repeats the
training of dpo_k2 round 1 in its own root; round 2 trains on the same
8,026 pairs against FedAvg round 2, to be read against on-policy round 2
(78.20, 3,354 pairs). Why first: on-policy round 2 gained 0.74 over round
1 with p 0.093, so whether on-policy rounds are a part of the method is
open, and it decides the story before the other settings. A pair rule
mixing one execution-error and one wrong-result rejected side per
question waits for the wrong-results-first run. BIRD as a second
benchmark is left to the owner after the fixed line and the no-NLL run.

## 2026-11-18: RFT round 1 below DPO, above FedAvg (results `e1e49ee0`, `424cd93e`)

RFT (chosen side only, NLL, no preference term) on the same samples and
the same 8,026 pairs as DPO round 1 from FedAvg round 2 (pair hashes
equal per client): 75.87 on Spider test (easy 90.43, medium 79.35, hard
67.60, extra 59.10); execution errors 153, wrong results 365. Against
DPO round 1 (77.46): fixed 76, broke 110, McNemar p 0.015. Against
FedAvg round 2 (74.10): fixed 59, broke 21, p 2.5e-05. Client updates:
cosine 0.024-0.058 (DPO 0.24-0.32), norms 0.94-1.41. Reading: training
on own correct samples gives about half of the gain (+1.77 of +3.36);
the preference term adds the rest, almost all from execution errors
(153 to 99). Wrong results go the other way (365 RFT, 385 DPO), so DPO
trades some wrong results for fewer errors. The preference term stays
in the method.

## 2026-11-18: decision runs queued before centralized SFT (owner; code `baf58106`)

Owner stopped centralized SFT in epoch 1 to settle the method first. Six
one-round runs, each read against DPO round 1 from FedAvg round 2
(77.46): RFT (preference weight 0), gold as chosen for all-wrong
questions, DPO from the base student with 2 pairs per question (k = 0),
a new pair rule `wrong_result_first` (rejected side from executable
wrong results when there are any; same pair count as random), DPO
without NLL, and DPO from FedAvg round 3 (k = 3). Rows from FedAvg round
2 reuse the samples of dpo_k2 round 1. Why: nearest and random pairs
reject the same outcomes (51% execution errors) and give the same EX;
the wrong-result count stays at 370-385 in every row; CodeLutra reports
17.2 Spider EX without its NLL term, and RFT tells whether the gain needs
the preference term at all.

## 2026-11-18: FedAvg round 4, line stopped at best round 3 (results `f7adcebe`, `da0871d4`, `7285253d`)

FedAvg SFT round 4 on Spider test: 74.71 (easy 90.64, medium 78.18, hard
66.74, extra 55.74), the same as round 3; execution errors 173, wrong
results 370; against round 3 fixed 44, broke 44, McNemar p 1. Client
updates: pairwise cosine -0.020 to 0.011. The curve stopped at step 4
with best step 3. DPO round 2 of the k = 2 line (78.20) against FedAvg
round 4: fixed 150, broke 75, p 1e-06.

## 2026-11-18: nearest pairs no better; DPO round 2 reaches 78.20 (results `c3effaea`, `9253ef8e`, `8fc37f77`, `5c33e622`)

Nearest-correct pairs, round 1 from FedAvg round 2 on the samples of the
random round: 77.08 on Spider test (random 77.46); against random fixed
34, broke 42, McNemar p 0.42. Its pairs are closer (mean similarity
0.85-0.86 against 0.74-0.76) and fewer (6,869 against 8,026: one pair per
distinct wrong SQL), but they reject the same outcomes (51% execution
errors), and the wrong results stay at 382. Random won by 8 questions
(1,663 against 1,655), so round 2 ran with random pairs.

Round 2 of the random line (samples and reference: round 1's global
model): 78.20 (easy 91.91, medium 81.91, hard 71.06, extra 60.50);
execution errors 84, wrong results 384. Against round 1 fixed 48, broke
32, p 0.093; against FedAvg round 3 fixed 142, broke 67, p 2.3e-07. The
round-1 model samples the training questions far better (sample accuracy
0.82-0.86, round 1: 0.68-0.75): mixed questions fall from 5,192 to 2,244,
all-correct rise from 2,891 to 5,784, all-wrong from 573 to 628; pairs
8,026 to 3,354, execution-error rejects 51% to 43%. Training: final
accuracy 0.75-0.79 and margin 0.26-0.69 (round 1: 0.80-0.96, 0.90-1.67).
Client updates: norms 0.70-1.20, pairwise cosine 0.013-0.055 (round 1:
0.24-0.32). Round 2 took about 1 h 50 min with its evaluation.

Across FedAvg rounds 2-3 and the three DPO rows, 359 test questions are
wrong in all five and 242 are a wrong result in all five (easy 26,
medium 86, hard 65, extra 65); 83.28% are right in at least one.

## 2026-11-18: round 2 of the k = 2 line queued (owner; code `c38e7eb0`)

Owner: a second on-policy round of the k = 2 line runs before FedAvg round
4, with the pair rule that answers more Spider test questions right in
round 1 (random 1,663 / 2,147; nearest pending; a tie keeps random). The
choice is made by the queue (`queue_when arm-gain`, two tasks with
complementary conditions), so the rule is picked on Spider test.

## 2026-11-18: DPO round 1 from FedAvg round 2: 77.46 on Spider test (results `431a17e7`, `be787676`)

`dpo_k2` round 1 (random pairs, 2 per mixed question, 8,026 pairs, one
epoch, beta 0.1, NLL weight 1). On each client the margin rises from
0.06-0.20 in the first quarter of the updates to 1.19-1.55 in the last,
accuracy from 0.67-0.70 to 0.89-0.92; every pair is seen once, so these
are pairs the client had not trained on yet. Client updates against the
round-2 adapter: norms 1.35-2.12 (SFT rounds: 3.9-6.7), pairwise cosine
0.24-0.32 (FedAvg SFT round 2: 0.01-0.05, round 3: about 0), product error
of the factor average 0.005 (SFT: 0.045-0.126). The DPO updates of the
five clients point the same way where the SFT updates had become
orthogonal. Rejected side: 4,087 of 8,026 pairs (51%) reject an execution
error; greedy round 2 has 183 execution errors and 373 wrong results on
Spider test. Peak reserved 12.65-18.93 GiB.

Greedy EX on Spider test (results `be787676`): 77.46 (easy 91.49, medium
80.63, hard 71.06, extra 59.66); FedAvg round 3 74.71, round 2 74.10.
Wrong rows: execution errors 99 (round 3: 164, round 2: 183), wrong
results 385 (379, 373). Against round 3: fixed 134 (63 from execution
errors, 71 from wrong results), broke 75 (21 into execution errors, 54
into wrong results), McNemar p 5.4e-05; against round 2 (its start):
fixed 146, broke 74, p 1e-06. The whole net gain comes from execution
errors; the wrong-result count does not move, as the 51% share of
execution-error rejects predicted.

## 2026-11-18: FedAvg capped at round 4, centralized SFT next (owner; code `cb947362`)

Owner: the FedAvg line stops at round 4 (`max_steps` 8 to 4) and
centralized SFT on the union of the clients runs after it overnight
(`refs/central_sft`, curve `central_base_ddlrows_s0/sft`: same SFT recipe,
LoRA r 16 / alpha 32 / dropout 0.05, prompt and evaluation as FedAvg; one
epoch per step, rule 0.5 / patience 2 / at most 8). Then the DPO line from
the best FedAvg round. pass@k of FedAvg round 3 (results `762b74a2`):
pass@1 68.34, pass@2 77.66, pass@5 84.97, pass@10 88.68 (round 2: 65.78,
76.06, 84.35, 88.36); test questions all correct / mixed / all wrong 788 /
1116 / 243 (round 2: 686 / 1211 / 250). The third SFT round sharpens the
samples (pass@1 +2.56) and leaves pass@10 where it was.

## 2026-11-17: pass@k of FedAvg round 2 on Spider test (owner's console, not committed yet)

`scripts/pass_at_k.py` (code `532256af`), 10 samples at T 1.0, vLLM at 0.30
of the card beside the DPO round: pass@1 65.78, pass@2 76.06, pass@5
84.35, pass@10 88.36; greedy EX of the same adapter 74.10. A correct SQL
is among 10 samples for 88% of the test questions; greedy decoding lies
between pass@1 and pass@2.

## 2026-11-17: pairs at k = 2 (owner's console, not committed yet)

Round 1 of `dpo_k2` sampled from FedAvg round 2 (vLLM, 8,659 questions x
10 at T 1.0 in 15 min 21 s). Per client: sample accuracy 74.5 / 75.2 /
67.9 / 71.0 / 71.5%, pass@10 90.9-94.8%; mixed 457 / 821 / 1205 / 2276 /
433 (51-65%, 60.0% overall), all wrong 60 / 102 / 183 / 179 / 49 (6.6%),
all correct 378 / 619 / 621 / 1021 / 252 (33.4%); pairs 914 / 1642 / 2248
/ 2356 / 866 = 8,026. Base student for comparison (clients 1-3): mixed
59.3 / 61.5 / 66.3%, all wrong 11.8 / 11.7 / 15.4%. Two SFT rounds halved
the all-wrong questions and cut the mixed ones by only 6-8 points, so the
pairs do not run short at k = 2. Client 4 makes 2,356 pairs from 2,276
mixed questions: 1,098 of them are on its six databases without rows and
give none, so its share of the average falls from 0.40 (SFT) to 0.29.

## 2026-11-17: I2 queued on the k = 2 samples (owner; code `922b2660`)

Owner approved. After the random-pair round from FedAvg round 2, the same
round with nearest-correct pairs (`--pair-rule nearest`, 2 per question)
trains on the same samples, copied to root
`fedpref_sftr2_nearest_ddlrows_alpha01_s0` by `scripts/reuse_samples.py`;
same flags otherwise (test in `tests/test_active_queue.py`). Reason: FedAvg
round 3 left the executable wrong results flat at 373-379 since round 1.
Then FedAvg round 4 and on.

## 2026-11-17: FedAvg SFT round 3 (code `845db4bc`, eval `6558ebfe`)

Spider test EX 74.71 (easy 90.21, medium 78.88, hard 67.17, extra
54.06): +0.61 over round 2, a gain under the line's rule (> 0.5), but
not a clear one (fixed 61, broke 48, McNemar p = 0.25). Execution errors
215 / 183 / 164 over rounds 1-3; executable wrong results 377 / 373 / 379,
flat since round 1, and extra hard 54.90 / 54.62 / 54.06. So after round 1
SFT only removes execution errors. Pairwise cosine of the client updates
-0.014 to 0.016 (round 2: 0.01 to 0.05, round 1: 0.13 to 0.33) while the
update norms stay at 3.9 to 6.7: the clients move as far as before, in
unrelated directions, and the average cancels most of it. Mean local
loss 0.070 to 0.103.

## 2026-11-17: method is k SFT rounds, then DPO; k = 2 read queued first (owner; code `46509f1e`)

Owner: the method starts DPO after a fixed SFT stage of k FedAvg rounds,
k a value stated in the paper; "the best round" needs the test set and is
not a method. k is swept over 0, 2 and the best FedAvg round; the paper
can show EX and pairs against k. Reason to read k = 2 early: after SFT on
the clients' own questions, more of them are right in all 10 samples, so
fewer give pairs (base student: 59-66% mixed), and the line from the best
round would only show this after FedAvg ends. Queued before the FedAvg
line: one DPO + NLL round from FedAvg round 2 (root
`fedpref_sftr2_ddlrows_alpha01_s0`, same flags as the line from the best
round), compared with FedAvg round 3. Rule: at least 1 EX above, the k = 2
line continues; about 0, read the pair counts first; below, stop and look.
The worker stopped at 20:43 in FedAvg round 3, client 2; the owner chose
to restart without looking for the cause.

## 2026-11-17: FedAvg SFT round 2 (code `32e3f681`, eval `0699ac6d`)

Spider test EX 74.10 (EM 62.93; easy 89.36, medium 78.65, hard 65.23,
extra 54.62). Against round 1: fixed 85 rows, broke 49 (McNemar
p = 0.0024); execution errors 215 to 183, wrong results 377 to 373.
Mean local loss 0.094 to 0.117. Pairwise cosine of the client updates
(against the round's global start) fell from 0.13-0.33 in round 1 to
0.01-0.05: the shared part of the update was learned in round 1, and the
round-2 updates are almost orthogonal, so averaging shrinks them. Factor
FedAvg relative product error 0.126 to 0.062. Whether this costs accuracy
needs the centralized reference (not run).

## 2026-11-17: FedAvg SFT round 1 (code `29f38add`, eval `d6bfc763`)

FedAvg from the base student, `alpha_0.1/k5`, prompt A (`ddl_rows`), one
local epoch. Spider test EX 72.43 (EM 60.41; easy 89.15, medium 75.26,
hard 63.71, extra 54.90) against 68.05 for the untrained student with
prompt A (results `12456b56`): 165 rows fixed, 71 broken, exact McNemar
p = 8.5e-10. Execution errors 287 to 215, wrong results 399 to 377.
Client sizes 895 / 1542 / 2009 / 3479 / 734 (client 4 weighs 0.40); mean
local loss 0.140 to 0.152 on every client. Pairwise cosine of the client
updates against the round's start adapter 0.13 to 0.33; factor FedAvg
relative product error 0.126. Round 1 trained in 7,339 s with peak
reserved 20,311 MB; the evaluation took 206 s.

## 2026-11-17: aggregation options for the DPO rounds written down (owner)

Owner: the federated options for aggregating the DPO rounds are options to
test, not changes now. Phase 1 keeps factor-wise FedAvg weighted by pair
count. Options and the evidence that would trigger each are in
`RESEARCH_STATE.md` 3.8: equal weights, question weights, FedNova-style
normalisation, exact LoRA aggregation, FedProx (likely redundant), server
optimisers (not planned); plus a re-aggregation probe of DPO round 1
without training, to be scripted once that round exists.

## 2026-11-17: experiment plan; phase 0 and 1 in code (code `62a48999`)

Owner approved the plan of `RESEARCH_STATE.md` section 3.7 (phases 0 to
3) and ruled: drop from the pairs only the questions on databases whose
tables hold no rows, not those whose gold result is empty; 2 pairs per
question.

In the code:

- `PairRule.skip_empty_databases` (on by default; `--keep-empty-databases`
  turns it off) and `fedls_sql.data.spider.empty_databases`. On the
  `alpha_0.1/k5` clients the databases without rows are `yelp` (client 3)
  and `academic`, `geo`, `imdb`, `music_2`, `restaurants`, `scholar`
  (client 4). The pair rule identity changed, so the root of the base
  student's DPO line no longer matches the new code; it is not queued.
- Pair statistics now count the wrong samples by outcome, the mixed
  questions with a wrong-result sample and the questions on empty
  databases. `scripts/pair_composition.py` rebuilds them from a round's
  samples (phase 0a, to run on the server).
- `scripts/error_breakdown.py`: wrong rows split into execution errors,
  wrong results and cut outputs by hardness, with the exact McNemar p
  against the first arm (phase 0b). On the base model: prompt A 287
  execution errors and 399 wrong results; B against A fixed 110 rows and
  broke 122 (p = 0.47).
- `compare_predictions` prints the exact McNemar p.
- Queue: `dpo/after_fedavg`, the curve `fedpref_sft_ddlrows_alpha01_s0/dpo`
  after the FedAvg curve: `--parent-stage` of FedAvg's best round, 10
  samples at T 1.0, 2 pairs per question, rule 0.5 / 2 / at most 6.
  Resolved commands checked against the FedAvg line (prompt, length,
  LoRA, evaluation) by a test; one rendered prompt read.

447 tests pass on the Mac. Nothing of it has run on the server.

## 2026-11-17: direction of the method revised (owner)

Owner: the method is a federated learning method that uses DPO, built to
beat the federated baselines. It is the owner's own design, not CodeLutra
applied to federated learning; CodeLutra was found later to have a
similar loop and is cited as the closest work. A FedAvg SFT stage before
the DPO rounds may itself be one of the parts. Nothing of it runs yet; the server runs the FedAvg SFT
rounds.

Written in `AGENTS.md` (Method) and `RESEARCH_STATE.md` section 3: three
candidate improvements (I1 on-policy rounds with the round's global model
as reference; I2 execution-aware pairs, the main candidate; I3 a FedAvg
SFT stage before the rounds), the rows of the paper with federated DPO as
published (OpenFedLLM: fixed pairs, fixed reference) as a baseline, and
the open settings (2 pairs per question proposed for every DPO line; the
chosen side of a gold-empty question). This replaces "no SFT stage before
the rounds" of the earlier ruling that day.

## 2026-11-17: FedAvg SFT runs alone first (code `407a7ad7`)

Owner: run the FedAvg SFT rounds first; that number is needed whatever
the DPO design becomes. The queue now holds `rounds/fedavg_sft` (the
FedAvg curve under its own rule: gain of more than 0.5 EX point, patience
2, at most 8 rounds). The DPO curve and the reference curves keep their
definitions and are not run; `rounds/sft_vs_dpo` and `refs/central_local`
left the queue. If the DPO line later runs more rounds than FedAvg, a
curve that `extends` the FedAvg one adds them.

Open before the DPO line runs (owner):

- pair rule for questions whose gold result is empty: CodeLutra as is,
  gold as chosen against execution-error samples only, or Arctic's filter;
- pairs per question: 10 (CodeLutra; 59,510 pairs a round, about 13-15 h
  of training, estimate) or 2 (about 11,900, 2-3 h, estimate);
- whether the method is the federated port of CodeLutra or a change to it
  (a pair rule that uses each execution label at the level it informs,
  with the port as a baseline row).

## 2026-11-17: what CodeLutra does with empty or uninformative labels

Read in the paper text (arXiv 2411.05199v3); no code is linked. It does
not name the Spider training split, does not mention empty gold results or
databases without rows, filters no training question (it drops only wrong
samples with repeated strings) and has no step for a question whose
samples are all wrong or all correct. Pairs: 10 samples at T 1.0, 10
random pairs per question. Its section 6 variant without gold (executable
as chosen, error as rejected) lifts BIRD EX 22.3 to 30.9, against 43.1
with gold. On a database without rows our labels reduce to that variant.

## 2026-11-17: pair read of the base student; seven Spider train databases have no rows

Results `1704b03b` (`audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0/pair_read/r1_base.json`),
10 samples per question at T 1.0, prompt A, `alpha_0.1/k5`.

| Client | Questions | Mixed | All correct | All wrong | Gold empty | Pairs (10 per question) |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | 895 | 531 | 258 | 106 | 30 | 5,310 |
| 2 | 1,542 | 948 | 414 | 180 | 21 | 9,480 |
| 3 | 2,009 | 1,332 | 368 | 309 | 103 | 13,320 |
| 4 | 3,479 | 2,629 | 444 | 403 | 1,433 | 26,290 |
| 5 | 734 | 511 | 147 | 76 | 29 | 5,110 |
| All | 8,659 | 5,951 | 1,631 | 1,074 | 1,616 | 59,510 |

Sample accuracy 56.1%; 3 gold errors; 1,663 samples hit the length limit.
Of the mixed questions, 1,392 have an empty gold result (1,237 at client
4).

Cause: the official Spider release ships seven training databases with
the schema and no rows (`geo`, `scholar`, `academic`, `restaurants`,
`imdb`, `yelp`, `music_2`): 1,759 questions, 1,648 of them at client 4
(47% of its questions). On them every executable SQL returns the empty
gold result and counts as correct. No Spider dev or test question is on
them. Content for `geo` and `restaurants` exists in
`jkkummerfeld/text2sql-data` (checked on copies: 530 of 564 and 56 of 125
gold queries return rows); the others were not checked. FedAvg SFT is not
affected (it trains on gold SQL).

## 2026-11-17: the two lines queued round by round; conditional tasks in the queue (code `66b2c01a`)

Owner: run FedAvg SFT and the DPO rounds one round at a time to see a
signal early, let each go on by the gain rule, and let the queue run a
task on a condition.

In the code:

- `scripts.curve run A B` alternates the curves step by step; with
  `--same-length` a curve whose rule has stopped follows the longer one,
  and its record keeps its own decision (`rule_stop_step`). `plan` prints
  the resolved commands of the first steps.
- A queue task may carry `when`, a check the worker runs without a GPU:
  exit 0 runs the task, exit 3 skips it (and the tasks that need it),
  anything else stops the worker. `scripts.queue_when curve-gain A --over
  B --min X` reads the published curve records.
- 442 tests pass on the Mac. Nothing of it has run on the server.

Queued (`queues/active.toml`), after the read of the pairs:

- `rounds/sft_vs_dpo`: FedAvg SFT and federated DPO from the base student
  on `alpha_0.1/k5`, prompt A, alternating, same length. Rule: gain of
  more than 0.5 EX point, patience 2, at most 8 rounds. The rounds are
  chosen on Spider test.
- `refs/central_local`: centralized SFT and local SFT per client as
  curves of one epoch per step, only if the best DPO round is at least
  2.0 points above the best FedAvg SFT round.

Values set here without a ruling of the owner: the rule (0.5, 2, 8), the
same length, the 2.0 points of the condition, SFT at lr 2e-4 with one
local epoch per round.

The two lines agree in prompt, length limit (7,168), LoRA r 16 / alpha 32,
the seeded LoRA initialisation, one epoch per round, 16 examples or pairs
per update, all 5 clients per round and the evaluation. They differ in:

| Setting | FedAvg SFT | Federated DPO |
|---|---|---|
| Learning rate | 2e-4 | 5e-5 |
| Warmup ratio (cosine) | 0.03 | 0.1 |
| Weight decay | 0.01 (AdamW default) | 1e-4 |
| LoRA dropout | 0.05 | 0 |
| Aggregation weights | client rows | client pairs |

No default of either runner was changed for the queue.

Not measured: peak VRAM of a FedAvg round and of a DPO round with prompt
A (sequences up to 6,927 tokens); the time of a round. Known risk: the
centralized and local runner retrains and overwrites a finished adapter
if its command is run again; the curve's state prevents it unless
`.queue_state/` is lost.

## 2026-11-17: Spider first, with prompt A (owner)

- The method is tried on Spider first (owner). Whether BIRD joins as a
  second set of clients, or becomes the main one, is decided after the
  first read of the DPO rounds against FedAvg SFT on Spider. Behind the
  question: on Spider the SFT of this student is at 77 to 78 in the
  papers and the highest published level is 82.3 (SPFT-SQL), so about 4
  points are left above SFT; on BIRD CodeLutra is 7.5 points above its
  SFT (35.6 to 43.1). Nothing is built for BIRD clients yet (no split, no
  prompt lengths).
- The runs on Spider use prompt A (`ddl_rows`). A and B give the same
  level without training (68.05 and 67.49, p = 0.47); A is the prompt of
  the model's own evaluation code. B is not run again unless a result
  asks for it, so the first comparison is run once, not once per prompt.
- The student stays Qwen2.5-Coder-1.5B-Instruct. Both rows of the
  comparison start from it, so a weaker model lowers both; and the DPO
  rounds need questions the model answers correctly in some samples.

## 2026-11-17: the DPO rounds start from the base student, pairs and defaults after CodeLutra (code `c03bd693`)

The preference rounds were written for DPO after an SFT stage. They now
run the method as set: round 1 from the base student, CodeLutra's pairs.
No GPU run yet.

In the code (`experiments/federated_pref/run.py`):

- `--from-base`: round 1 samples from the base model with no adapter and
  every client trains from one saved LoRA initialisation, the same one the
  FedAvg SFT runner builds from the base model (a test gets bit-identical
  tensors on a tiny model on CPU). The DPO reference of round 1 is the
  base model. A start from a parent adapter still works.
- Pair rule `random` (default), as read in CodeLutra (section 4,
  Algorithm 1 lines 16 to 19, appendix A.1): 10 pairs per question, the
  chosen side drawn at random from the correct samples and the rejected
  side from the wrong ones, with replacement when a set has fewer than 10.
  The draw is over the samples as produced, so a SQL sampled three times
  is three times as likely. All-wrong and all-correct questions give no
  pair. Gold SQL as the chosen side is off (`--gold-chosen` turns it on).
- Pair rule `nearest` is kept as the candidate: each distinct wrong SQL
  with its most similar distinct correct SQL. The similarity is a
  character-level ratio, not the token edit distance of `DPO_RESEARCH.md`,
  section 3.3.
- Defaults: 10 samples at T 1.0, beta 0.1, NLL weight 1, lr 5e-5, 1 epoch
  per round, 16 pairs per update, weight decay 1e-4 (CodeLutra, section
  5.1 and Table 4). LoRA rank stays 16 (the paper has 8).
- `read`: sampling, labels and the counts per client without training,
  into `pair_read/r1_base.json`. Round 1 of the DPO arm on the same root
  reuses its samples.

Where the code is not the paper:

- The NLL term is a per-token mean; the paper writes the log-likelihood of
  the sequence. CodeLutra has no public code to check which it ran.
- Warmup 0.1 with cosine decay: the paper does not state a schedule.
- A response with no SQL counts as wrong (the paper's rule: every sample
  that does not match goes to the rejected set). A sample cut at 256
  tokens is in neither set; the paper filters "answers that contain
  repeated strings", which is not implemented apart from that.
- Aggregation weights are the clients' pair counts; FedAvg SFT weights by
  the number of questions.

Smoke on the Mac, not a result: 2 clients, 4 questions each, HF. The read
ran through (8 questions: 2 all wrong, 4 mixed, 2 all correct, 40 pairs).
The round reused the samples, client 1 trained 2 updates, and the run was
stopped during client 2 (owner: too slow on the Mac). The path from the
base student has not run through aggregation anywhere. 428 tests pass on
the Mac.

Queued: `pairread/*`, the read on `alpha_0.1/k5` with prompt A through
vLLM. Its peak memory on the card is not measured.

## 2026-11-17: the base model on Spider test with both prompts (results `12456b56`)

The student with no training, greedy, vLLM `inproc`, 2,147 rows, code
`083a6a52`. A check of the prompt and the decoding, not a result of the
method.

| Prompt | EX | Easy | Medium | Hard | Extra | Rows that do not execute | EM |
|---|---:|---:|---:|---:|---:|---:|---:|
| A, `ddl_rows` | **68.05** | 87.4 | **71.4** | **59.2** | 45.9 | **287** | **53.3** |
| B, `ddl_values` | 67.49 | **87.7** | 71.2 | 56.4 | **46.5** | 322 | 44.2 |

- A and B do not differ: 1,461 against 1,449 correct rows; 122 rows are
  correct only with A and 110 only with B (exact McNemar p = 0.47).
  1,571 rows are correct with at least one of them.
- The prompt and the decoding are sound. Every output starts with
  `SELECT`, none is empty or in a code fence, and all end at the end token
  except 2 of B that reach 256 tokens. The rows that do not execute are
  the model's errors, not a format defect: `no such column` in 270 of 287
  (A) and 304 of 322 (B), a column taken from the wrong table, most on
  databases with many tables (`bakery_1`, `cre_Doc_and_collections`,
  `cre_Students_Information_Systems`).
- Published numbers of this model on Spider test, each with its own
  prompt: 72.3 (SPFT-SQL, zero-shot), 67.61 (SLM-SQL, a vote over 16
  samples).
- B's lower EM is style (`INNER JOIN`, aliases), not correctness.
- Time: 17 s of generation for the 2,147 rows, about 2.5 min per task
  with the model load. The 10 min of the queue note was an estimate.

The choice between A and B stays open; it is made on the gain of the DPO
rounds over FedAvg SFT (`RESEARCH_STATE.md`, section 4, item 1).

On the server: the pull of the reset went through after the server copies
of 27 tracked files of one earlier result row (`p229_h_plain`) were put in
a stash; what differs in them was not reported. One test failed there
(`test_progress`, it assumed CUDA was not initialized) and was fixed in
`083a6a52`; the test summary on the server after the fix was not reported.

## 2026-11-17: the method is federated DPO; pre-training secondary, the teacher a research direction (owner)

Decision, after the reading in `DPO_RESEARCH.md`. It replaces the three
stages of the reset entry below (server stage with the teacher, FedAvg
SFT, federated DPO).

- Core: federated DPO + NLL. In each round the clients sample from the
  global model, label by execution on their own databases and train; the
  reference is the round's global model. No SFT stage comes before the
  rounds. FedAvg SFT is a baseline.
- Secondary: pre-training at the server with the same loss on public
  data, as the starting point of the rounds.
- The teacher is not part of the method. It stays as a research
  direction.
- Output is SQL only, no chain of thought.

What the papers gave for it (numbers and sources in `DPO_RESEARCH.md`):

- CodeLutra starts from the base model with no SFT stage, and SFT followed
  by plain DPO gives about zero for SQL-only output (Liu et al., ExCoT).
- No Text-to-SQL paper shows a teacher's SQL to beat gold SQL as the
  target. In KID, forward KL to the teacher ends below training on gold
  alone; reverse KL on the student's own samples ends above it.
- Pre-training on public data leaves the clients' questions unseen, so
  they still give pairs. Whether it adds or removes pairs is not known.

Choices inside the rounds (owner, the same day):

- The base form is CodeLutra's: plain loss, random pairs, nothing from a
  question whose samples are all wrong.
- The gold SQL of an all-wrong question in the NLL term (never as the
  chosen side of a pair) is an experiment to run, not a part of the method
  yet. No paper measures it; the one precedent is Iterative RPO on GSM8K.
- Nearest-correct pairing and the rejected side counted on the differing
  tokens join the method if a run shows a clear gain over the base form.
- Unlabelled questions are not in the method; it stays on the clients'
  labelled questions.

Notes changed: `RESEARCH_STATE.md` sections 2 to 4, `DPO_RESEARCH.md`
(sections 2.7 to 2.9 and 3), the run table of `FEDERATED_DATA_SETUP.md`
(13 rows on the main setting instead of 14), both `AGENTS.md`. No run and
no code change; nothing in the queue depends on it.

## 2026-11-17: what the paper prints (owner)

The paper prints what serves it: the setup as values, the results, the
tables. How a seed, a setting, a round or a result was picked is not told
in the paper; this log keeps it. No sentence in the paper is false. This
replaces the wording of the reset entry below, "the number is reported as
chosen on Spider test": the log records the set a choice was made on, the
paper does not have to.

## 2026-11-17: client splits rebuilt by database complexity tier (code `4760352b`)

Owner: rebuild the data processing after `FEDERATED_DATA_SETUP.md`.

In the code:

- Every database still goes whole to one client. The label of the
  Dirichlet is new: each of the 146 train databases gets one of four tiers
  by its share of hard and extra questions (Spider's hardness levels from
  the gold SQL, the function evaluation uses; `db_tiers.json`).
- The partition is NIID-Bench's label-Dirichlet recipe as its code has it
  (`utils.py`, `noniid-labeldir`, read 2026-11-17): per tier the clients'
  shares come from Dir(alpha), the tier's databases are cut by them, a
  client that already holds 146 / K databases takes none of the later
  tiers, and the draw is repeated until every client has 5 databases (3
  with 10 clients). The note's recipe did not have the third rule; without
  it seed 0 gave one client 85 databases and 64% of the questions.
- The IID split puts the databases in random order and cuts them into
  equal parts.
- Removed: the schema-embedding domain groups, their builder and audit,
  and the splits built from them (Spider and BIRD). They are at the tag
  `archive/pre-reset-2026-11-17`.

Hardness of Spider train (8,659 questions): easy 1,983, medium 2,999, hard
1,921, extra 1,755, one unparsed (`train:3153`). 8,658 labels equal the
level of Spider's own parse in the raw files.

| Tier | Databases | Questions | Hard or extra share of a database | Easy | Medium | Hard | Extra |
|---|---:|---:|---|---:|---:|---:|---:|
| 0 | 37 | 1,746 | 0.00 to 0.26 | 30.7% | 49.1% | 12.3% | 8.0% |
| 1 | 36 | 1,506 | 0.26 to 0.33 | 25.8% | 44.8% | 18.6% | 10.8% |
| 2 | 37 | 1,791 | 0.34 to 0.44 | 22.3% | 38.7% | 20.4% | 18.6% |
| 3 | 36 | 3,616 | 0.44 to 0.86 | 18.3% | 21.4% | 29.3% | 31.0% |

Tier 3 holds 42% of the questions: `scholar` (569) and `geo` (564) are in
it.

Split seed: 42 (owner, 2026-11-17), for all four splits. Seed 0 was built
first (code `e5c8134f`): clients of 1,084 / 288 / 1,482 / 1,857 / 3,948
questions, hard or extra 18% to 57%, third draw. The owner then asked for
seed 42 and took it from the split tables, before any training: the
smallest client has 734 questions instead of 288 and the largest 40% of
the questions instead of 46%. The paper gives the seed and the table.

Main split, `federated/alpha_0.1/k5`, seed 42 (first draw):

| Client | Databases | Questions | Easy | Medium | Hard | Extra | Hard or extra | Databases per tier 0 to 3 |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| 1 | 21 | 895 | 27.2% | 42.6% | 20.0% | 10.3% | 30.3% | 0, 20, 0, 1 |
| 2 | 34 | 1,542 | 30.9% | 49.0% | 12.0% | 8.2% | 20.2% | 34, 0, 0, 0 |
| 3 | 42 | 2,009 | 21.1% | 42.2% | 18.6% | 18.1% | 36.7% | 0, 12, 30, 0 |
| 4 | 37 | 3,479 | 18.8% | 21.2% | 28.9% | 31.1% | 60.0% | 0, 3, 0, 34 |
| 5 | 12 | 734 | 25.3% | 38.0% | 24.3% | 12.4% | 36.6% | 3, 1, 7, 1 |

The other splits (seed 42), questions per client and the range of the hard
or extra share:

| Split | Questions per client | Hard or extra share |
|---|---|---|
| `alpha_0.5/k5` | 1,238 / 1,429 / 1,170 / 1,533 / 3,289 | 21.9% to 55.6% |
| `iid/k5` | 1,866 / 1,298 / 2,005 / 1,462 / 2,028 | 33.9% to 52.4% |
| `alpha_0.5/k10` | 442 to 1,903 | 19.4% to 63.1% |
| the earlier domain-cluster split `alpha_0.1/k5` | 1,896 / 1,801 / 2,061 / 1,097 / 1,804 | 36.4% to 57.9% |

What it shows:

- At the level of databases three clients hold one tier almost alone
  (clients 1, 2 and 4); client 3 mixes tiers 1 and 2 and client 5 all
  four. At the level of questions the skew is in the proportions, 20% to
  60% hard or extra. No client lacks a level: client 2, all of tier 0,
  still holds 311 hard or extra questions of 1,542.
- `alpha_0.5/k5` (22% to 56%) is about as skewed as `alpha_0.1/k5` in this
  measure, so the alpha rows may not differ much.
- The IID split is equal in databases, not in questions or hardness
  (extra 14% to 31%), because the databases differ in size.
- Over 200 seeds at alpha 0.1 with 5 clients: the largest client holds 40%
  of the questions on average, the smallest has a median of 522.

Not done: no training on the new splits. Whether the split gives a reason
to federate needs local, FedAvg and centralized rows (`RESEARCH_STATE.md`,
section 4, item 7). 415 tests pass on the Mac.

## 2026-11-17: the prompt, two schema styles (code `3d05fa33`)

Owner: implement candidates A and B, with the SQLite sentence, no
repetition penalty and a length limit that fits.

In the code:

- One layout, taken from the Qwen2.5-Coder evaluation code: schema text,
  `-- Using valid SQLite, answer the following questions for the tables
  provided above.`, `Question: ...`, "Please output only the final SQL
  query, starts with keyword `SELECT`." One user message through the chat
  template.
- `--schema-style ddl_rows` (A, default): `CREATE TABLE` text and 3 example
  rows per table. `ddl_values` (B): `CREATE TABLE` text rebuilt per column
  with 2 example values as a comment (OmniSQL's schema text; no column
  descriptions, no question-matched values). `ddl`: no rows.
- Decoding greedy, penalty 1.0, 256 new tokens. `--max-len 7168`, policy
  `error`.
- One `extract_sql` for evaluation and DPO labels; target = gold SQL
  without a final `;` plus the end token; the prompt identity hashes a
  rendered prompt and is in the evaluation, sample and stage fingerprints;
  the sampling seed is derived per round and client.

Token lengths with the student's tokenizer (Mac, whole sets):

| Style | Spider train, sequence p50 / p99 / max | Spider test, prompt max |
|---|---|---:|
| `ddl_rows` | 821 / 3,863 / 6,927 | 2,547 |
| `ddl_values` | 620 / 3,129 / 6,440 | 1,939 |
| `ddl` | 480 / 1,653 / 2,334 | 1,086 |

No row exceeds 7,168. The longest database is `baseball_1`. BIRD is not
measured (its databases are not on the Mac).

Smoke on the Mac, not a result: the base model, HF, 40 random Spider test
rows, greedy. `ddl_rows` 25/40, `ddl_values` 27/40; every output ended at
the end token and was plain SQL with no code fence. 421 tests pass.

Queued: the base model on all of Spider test with A and B (`prompt/*`,
vLLM `inproc`).

Not done: the SFT shuffle seed per client and round, LoRA dropout and
weight decay set on purpose, a key check when an adapter is loaded.

## 2026-11-17: clean reset (owner)

Decision: the project is set up again from clean. The prompt of every
earlier adapter carried a sentence from the ICL project ("The examples
below show SQL patterns for reference..." with no example shown), most rows
were decoded with an unset repetition penalty of 1.1, and the code still
held the ICL fields and many dropped lines. Every earlier number is
reference only.

Owner's rulings of the day:

- The client stage follows CodeLutra's recipe (DPO with an SFT term on
  execution-labelled samples of the current model). Work starts with the
  client stages; the server stage and the teacher come after.
- No repetition penalty.
- Rounds and settings may be chosen on Spider test; the number is reported
  as chosen on Spider test.
- The prompt and the training recipe follow what widely used papers do.
  The `codes` prompt code leaves with the other dropped lines.
- The package is renamed `fedls_sql`.

Done:

- Worker stopped by the owner during `synvc_s0/sft_plain`; the last
  published result is `a428e174`.
- Tag `archive/pre-reset-2026-11-17` pushed in both repositories (code
  `aa17258c`, workspace `9ef705b`); both trees copied to
  `archive/reset_2026-11-17/` with an overview note and the code review.
- Code repository `7d9aab8d`: committed results, audits and the old queue
  removed from `main`; the queue holds the worker selftest only.
- A read-only review of the code found, besides the three known defects:
  the chat template adds Qwen's default system message (training and
  evaluation agree; no note had it), the prompt identity hashed a
  placeholder and not the rendered schema, the sampling seed of a question
  did not change between rounds, the default model of four entry points was
  the non-Coder Qwen2.5-1.5B, the SFT runner defaulted to a 2,560-token
  limit that cuts the start of the prompt, evaluation and DPO labels
  extracted SQL with two different functions, and the training target
  ended with a newline after the end token.

CodeLutra, read again in the paper (arXiv 2411.05199v3): it starts from
the base model with no SFT stage; its SFT model is a separate baseline
(1 epoch, lr 5e-5). Iteration 1 equals that baseline on Spider (67.8
against 67.9) and the gain comes in iterations 2 and 3 (72.4, 76.6). Its
prompt is zero-shot with the `CREATE TABLE` text of the SQLite file; the
template is not printed and no code is published. It names no repetition
penalty and evaluates one sample at T 0.2.

Prompt and training practice of ten works: `LITERATURE.md`, section 1.19.
Most add a few database values to `CREATE TABLE` text; the student's own
report uses `CREATE TABLE` plus 3 example rows per table after Chang and
Fosler-Lussier (2023).

Open, for the owner: the prompt (three candidates in `RESEARCH_STATE.md`,
section 4), then the settings of stage 3. (Prompt: see the entry above.)
