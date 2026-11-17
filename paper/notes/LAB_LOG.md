# FedLS-SQL: lab log

Every run, result and decision since the clean reset of 2026-11-17, newest
on top. A result reported only in chat is logged as "not committed". The
log of the earlier setup is at the tag `archive/pre-reset-2026-11-17`.

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
