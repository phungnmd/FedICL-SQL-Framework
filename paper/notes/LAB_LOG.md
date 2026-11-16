# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

## 2026-11-16: questions that do not name the gold columns; scan on schema perturbation (local analysis)

Owner (evening of 2026-11-16): the data assumption stays, every client
question keeps its gold SQL, so candidate C (clients with few labelled
questions) is dropped. Asked for other mechanism ideas and approved two
checks that need no server: this analysis and a literature scan, both for
the idea "same question, perturbed schema" as a source of pairs for the
DPO rounds (the client renames tables and columns or adds distractor
tables on a copy of its database; the gold SQL is renamed with it).

No GPU run. Spider test, `codes`, seed 0, without the repetition penalty,
from the committed prediction files (`sqlcodes_fedavg_r3_np_vllm_inproc`,
`sqlcodes_dpo_fedavg_r3_np_vllm_inproc`). A gold column counts as named
when every word of its name occurs in the question (split on `_`, plural
endings stripped); columns that occur only in join conditions are left
out. The script is not committed.

| Gold columns outside joins | Questions | FedAvg R3 | DPO round 3 |
|---|---:|---:|---:|
| all named in the question | 883 | 82.11 | **83.81** |
| some named | 853 | 67.06 | 70.34 |
| none named | 331 | 69.49 | 71.30 |
| no such column (`count(*)` and the like) | 80 | 96.25 | 97.50 |

DPO round 3, EX (questions) by the number of gold columns and how many
of them the question does not name:

| Gold columns | 0 unnamed | 1 unnamed | 2 or more unnamed |
|---|---:|---:|---:|
| 1 | 87.0 (376) | 84.2 (158) | |
| 2 | 81.8 (341) | 73.3 (382) | 61.0 (136) |
| 3 | 82.3 (130) | 72.2 (162) | 70.2 (124) |
| 4 or more | 75.0 (36) | 77.2 (79) | 52.4 (143) |

The same for tables: one gold table, named 90.9 (950), not named 73.6
(280); two gold tables, both named 73.6 (311), one not named 61.3 (284).

- 1,184 of the 2,147 questions (55%) have a gold column the question
  does not name, and EX there is 10 to 20 points lower at the same number
  of columns. If these rows reached the EX of the named rows with the same
  column count, the gain would be about 127 questions (5.9 points): an
  upper bound, since these questions also ask for more inference.
- The model still finds the column: 93.1% of the unnamed gold columns are
  in the predicted SQL against 95.2% of the named ones. Of the 491 wrong
  rows of DPO round 3, 87 miss an unnamed gold column (4.1 points) and 76
  a named one. The loss on these questions is mostly not a missing column.
- DPO gains in every group (+1.70, +3.28, +1.81) and does not close the
  gap between them.

Literature scan (`LITERATURE.md`, section 1.18): training on the same
question with perturbed schemas is published as plain SFT (EvoSchema,
ADVETA). Both report gains on perturbed evaluation data and a small loss
on the unperturbed set (about 1 point; table values known from a machine
summary only). No paper was found that uses perturbed schemas inside
on-policy, execution-labelled preference training, and none is federated.

Reading: the slice exists on Spider test, but the published effect of
schema perturbation is robustness, not EX on the original set. Not
queued; the pilot (one DPO round, about 4 h, new code) waits for the
owner and for the synthetic round (`synth_s0`).

## 2026-11-16: method debate between two agents, two short reads queued (owner)

The owner asked for two agents to look for a method that would stand at
Q3 or Q2 without a contrived setup: one as the PhD student on this paper
(reads the notes and the committed predictions, told not to trust the
project's own conclusions), one as an outside researcher (a one-page
brief and web search only). Three rounds: proposals, criticism of each
other, final positions. Their files are session scratch and not
committed; the paper numbers the outside agent quotes were read through a
summarising page fetch and are not in `LITERATURE.md` yet.

Counts by the inside agent on committed rows (Spider test, `codes`,
seed 0, no penalty; table sets read with sqlglot):

| | Base | FedAvg R3 | DPO R3 | 7B teacher |
|---|---:|---:|---:|---:|
| Wrong, table set differs from gold | 396 | 276 | 226 | 122 |
| Wrong, same tables, execution error | 80 | 40 | 27 | 43 |
| Wrong, same tables, wrong result | 260 | 227 | 240 | 252 |

- A wrong table set is the largest class after DPO (about 9 points once
  the rate of right answers with another table set is taken off) and the
  only one training moves. EX by number of gold tables: 87.0 / 68.4 /
  55.2 / 33.3 (one, two, three, four or more).
- With the gold tables given, at best 147 of those rows turn right (6.85
  points): rows where a sample or the teacher is right.
- 15 of the 40 test databases hold 76% of the errors; 91 of the 226
  table-set errors repeat one confusion three or more times in a database.
- Doubt on the DPO decision: its SFT controls (`sqlsft_hinton_x1` 74.15,
  `sqlrft_hinton_r1` 73.50) were decoded with the penalty, which costs SFT
  rows 1.1 to 1.5 points and DPO rows nothing.

Both agents end on the same two parts and both put Q3 at about 55%
(Q2 at 12% and 20%):

1. Tables first: the same adapter lists the tables a question needs
   (labels read from the clients' gold SQL), then writes the SQL on the
   schema cut to them; two greedy calls. Closest: DTS-SQL, JOLT-SQL
   (centralized, 7B). Expected +1 to +3.2.
2. A new site without labels: the adapter also learns SQL to question; a
   site with databases and no questions builds SQL on them, writes the
   questions, keeps pairs checked by execution and trains one local round.
   Closest: GAZP, YORO, SQL-Zero. Its gain shows on the adapted
   databases, so not on Spider test unless test databases may be used;
   that and a held-out client as the new site are open owner decisions.

Dropped in the debate: gold SQL mutants as the rejected side, a full plan
before the SQL, an exchange of failing SQL skeletons between clients, a
teacher on public join rows, a repair call as more than a component.

Queued after the `codes_v2` FedAvg rounds and before its DPO rounds
(phase `gate_s0`, about 50 min, `e4f54e3a`): the five control rows of the
Hinton line without the penalty, and FedAvg R3, DPO round 3 and the base
model with the schema cut to the gold tables (`--oracle-tables`,
`236479aa`; arms `*_oracletab_*`, a diagnostic and never a result). On
all 2,147 test rows the oracle prompt keeps 1.57 of 4.89 tables and
changes 1,978 prompts.

## 2026-11-16: the two short reads moved ahead of the `codes_v2` line (owner); synthetic rows built

- Owner, 23:48: the gold-table rows and the controls run first, to fix
  the method direction as early as possible (`70877dc4`). The worker had
  started the `codes_v2` FedAvg rounds at about 23:47 and is restarted;
  the rounds continue after the reads.
- `synth_s0/build` (`04922932`), base model as the question writer,
  without the penalty, root `sqlsynnp_coder15b_alpha01_s0`: 5,645
  questions written, 5,434 kept (1,118 / 1,046 / 1,180 / 1,052 / 1,038 by
  client); with the penalty 5,494 were kept. The rows have not been read
  by hand.

## 2026-11-16: one DPO round with samples drawn without the repetition penalty

`norp_s0/curve_fedavg` (`f6a2a6a1`, `8a883578`): DPO + NLL round 1 from
FedAvg R3 of the `codes` line, samples and evaluation without the penalty,
arm `sqlcodes_npdpo_fedavg_r1_np_vllm_inproc`. Spider test, seed 0.

| Row (evaluated without the penalty) | EX | Execution errors | New row: gained / lost |
|---|---:|---:|---:|
| FedAvg R3 | 74.71 | 171 | 99 / 51 |
| DPO round 1, samples with the penalty | 76.29 | 98 | 46 / 32 |
| DPO round 3, samples with the penalty | **77.04** | **82** | 45 / 47 |
| DPO round 1, samples without the penalty | 76.94 | 88 | |

Round 1 pairs, samples with the penalty against without: 6,626 against
5,280 pairs; questions with all 8 samples right 4,096 against 4,870;
mean sample accuracy 74.8% against 79.2%; rejected side fails to execute
4,078 against 3,117, wrong result 2,548 against 2,163.

- The DPO stage keeps its gain with clean samples: +2.23 over FedAvg R3
  in one round, from fewer pairs.
- One clean round equals three rounds trained on penalised samples
  (76.94 against 77.04); whether clean rounds 2 and 3 add more is the
  `codes_v2` line.

## 2026-11-16: zero-shot prompt variants and a schema filter without training (local probe, not committed)

Question: the base model is 6.6 below the zero-shot number SPFT-SQL
reports for the same model (65.72 against 72.3 on Spider test); does the
wording of the instruction or a simple schema filter close it, before the
`codes_v2` line trains with the current prompt.

Probe, not committed: the base model, `codes_v2` schema, 300 random rows of
the five clients' Spider train files (seed 0), greedy, no repetition
penalty, Hugging Face on the Mac, the project's scorer.

| Prompt | EX | Execution errors | Gained / lost against the current prompt |
|---|---:|---:|---:|
| current | 68.00 | 45 | |
| without the sentence "The examples below show SQL patterns for reference." | 68.00 | 45 | 2 / 2 |
| that, plus "SQLite" and "use only the tables the question needs, take each column from the table that defines it, return only the columns the question asks for" | **70.00** | 44 | 14 / 8 |
| OmniSQL layout (task overview, engine, schema, question, instructions), SQL only | 69.67 | **41** | 30 / 25 |

Schema filter without training, counted on all 8,659 client rows (no
model): tables that share a word with the question, hold a matched value
or bridge two kept tables keep every gold table on 89.28% of the questions
(54.7% of the tables left); adding the foreign-key neighbours of the kept
tables gives 97.60% (77.2% of the tables left).

- No variant differs from the current prompt beyond what 300 rows can
  show; the wording of the instruction does not explain the 6.6.
- The filter removes a needed table more often than it could help; a
  filter needs a trained classifier, as in CodeS.
- The scorer is not the difference either: it is the result comparison of
  `test-suite-sql-eval` on the one distributed database.
- Decision: no prompt change, nothing added to the queue; the `codes_v2`
  line trains with the current prompt.

## 2026-11-16: repetition penalty 1.1 in every generation (local probe, not committed)

Question (owner): why the base model scores below the published numbers
for the same model and set.

Finding in code: every generation takes `repetition_penalty` from the
model's `generation_config.json`, which is 1.1 for Qwen2.5-Coder
(`fedicl_sql/models/vllm_student.py`, also the Hugging Face path): greedy
evaluation, the 8 samples of a DPO round, selection by execution. The
penalty also applies to tokens of the prompt, and SQL has to copy table
and column names from the prompt.

Probe, not committed: the base model on 400 random rows of Spider test
(seed 0), the exact `codes_v2` prompts of `d22463ca`, greedy, Hugging Face
on the Mac (float32, MPS), the project's parser and scorer. Only the
penalty changes.

| Penalty | EX | Execution errors | `no such column` | Wrong results | SQL with `AS T1` aliases |
|---|---:|---:|---:|---:|---:|
| 1.1 | 61.50 | 72 | 68 | 82 | 126 |
| 1.0 | 65.50 | 53 | 53 | 85 | 83 |

- Without the penalty +4.00 on these rows: 33 questions gained, 17 lost
  (p = 0.03). The server run (vLLM, penalty 1.1) gives 61.25 on the same
  400 rows; the local run with 1.1 gives the same SQL on 367 rows and the
  same verdict on 391.
- The penalty raises execution errors and leaves wrong results unchanged.
  The DPO rounds have the same signature (execution errors 205 to 86 with
  `codes`, wrong results about 400), and their samples are drawn with the
  penalty. How much of the DPO gain is left without the penalty is not
  measured: the adapters are on the server.
- Other points checked and standard: chat template in training and
  evaluation, loss on the SQL only, LoRA (r 16, alpha 32, all linear
  layers, lr 2e-4, cosine), the test-suite `result_eq` evaluator, the data
  (8,659 train rows, 2,147 test rows).
- Published numbers for this model, untrained, are not measured the same
  way: SLM-SQL 67.61 on Spider test is a vote over 16 or 64 samples with a
  reasoning prompt (no inference code released); SPFT-SQL 72.3 has no code
  and no prompt; `tarubee19/instaquery` (code) gives 68.5 on Spider dev,
  greedy, with `repetition_penalty=1.0` set by hand; three other
  repositories with code give 46.4 to 58.7 on Spider dev or a subset.

Proposed, not approved: evaluate the base model, FedAvg R3 and DPO round 3
(`codes`) on the server with penalty 1.0 (about 30 min, a new option and
new arm names; existing results keep their identities). Script and rows of
the probe are in the session scratchpad only.

## 2026-11-16: vote label check and selection by execution queued (owner)

Owner at about 20:40 on 2026-11-16: yes to two short reads behind the DPO
rounds of the `codes_v2` line. Code `3c6f849a`, queue `3c505c09`.

- `vote_s0/check` (`scripts/vote_label_check.py`, CPU): the samples of
  DPO rounds 1-3 labelled by a vote over execution results, against the
  recorded gold labels: how often the vote winner is right, how many
  vote-labelled pairs have a right chosen side and a wrong rejected side,
  and both when a question is used only above a vote size. The first
  number for candidate C (clients with few labelled questions). After
  the peer check of the `codes` line, B is the only queued candidate with
  a role for federation, and it leans negative.
- `vote_s0/xsel_dpo_r3`: selection by execution over 8 samples of DPO
  round 3 on Spider test without the penalty (vote, pass@8).

Not queued, to decide from results: the rejected-type ablation with
samples drawn without the penalty (about 3.5 h), the control with equal
pair counts for the synthetic round (about 3 h), the baselines and other
earlier rows evaluated without the penalty (about 6 min a row).

## 2026-11-16: the six existing rows without the repetition penalty

`456d1fea` (19:47) and `05c22e54` (19:58 on 2026-11-16): committed
adapters, Spider test, 2,147 rows, seed 0, vLLM inproc,
`--repetition-penalty 1.0`, arms with `_np`. Gained / lost are questions
against the same adapter with the penalty.

| Row | EX, penalty 1.1 | Errors | EX, no penalty | Errors | Gained / lost |
|---|---:|---:|---:|---:|---|
| base model, `codes_v2` | 61.95 | 377 | 65.72 | 272 | 168 / 87 |
| FedAvg R3, `full` | 71.26 | 211 | 72.33 | 183 | 93 / 70 (p = 0.08) |
| DPO round 3 from it, `full` | 75.13 | 101 | 75.08 | 107 | 62 / 63 |
| FedAvg R3, `codes` | 73.17 | 205 | 74.71 | 171 | 74 / 41 (p = 0.003) |
| DPO round 1, `codes` | 76.62 | 94 | 76.29 | 98 | 46 / 53 |
| DPO round 3, `codes` | **77.36** | 86 | **77.04** | **82** | 42 / 49 |

| Gain of the DPO stage over FedAvg R3 | Penalty 1.1 | No penalty |
|---|---:|---:|
| `full`, round 3 | +3.87 | +2.75 (112 / 53) |
| `codes`, round 1 | +3.45 | +1.58 (79 / 45) |
| `codes`, round 3 | +4.19 | +2.33 (115 / 65) |

- The penalty costs the models that were never trained on their own
  samples: 3.77 points for the base model, 1.07 to 1.54 for FedAvg R3.
  The DPO adapters do not move under either prompt.
- The DPO stage keeps a clear gain without the penalty, 2.3 to 2.75
  points at round 3; 1.1 to 1.9 points of the reported gain were the
  penalty's cost on the SFT model.
- `codes` over `full` holds: +2.38 at FedAvg R3 and +1.96 after DPO
  without the penalty (+1.91 and +2.23 with it).
- These DPO adapters were trained on samples drawn with the penalty;
  the round with samples drawn without it is running
  (`norp_s0/curve_fedavg`).

The first two rows in detail:

### 2026-11-16: FedAvg R3 and DPO round 3 of the `codes` line without the repetition penalty

`456d1fea` (19:47 on 2026-11-16), arms `sqlcodes_fedavg_r3_np_vllm_inproc`
and `sqlcodes_dpo_fedavg_r3_np_vllm_inproc`: the committed adapters,
Spider test, 2,147 rows, seed 0, vLLM inproc, `--repetition-penalty 1.0`.
The worker was restarted on the new queue before 19:47 (time not
reported).

| `codes` line, Spider test | EX, penalty 1.1 | Errors | EX, no penalty | Errors |
|---|---:|---:|---:|---:|
| FedAvg R3 | 73.17 | 205 | 74.71 | 171 |
| DPO round 3 | **77.36** | 86 | **77.04** | **82** |
| DPO round 3 over FedAvg R3 | +4.19 | | +2.33 | |

- FedAvg R3 gains 1.54 points without the penalty (74 questions gained,
  41 lost, p = 0.003) and loses 34 execution errors. By hardness the gain
  is on medium (75.4 to 77.8) and hard (65.2 to 68.7).
- DPO round 3 does not move (42 gained, 49 lost, p = 0.53). Its samples
  were drawn with the penalty, so the rounds trained the model to give
  executable SQL under it.
- The DPO stage keeps a gain without the penalty: +2.33 (115 gained, 65
  lost, p < 0.001), against +4.19 with it. About 1.9 points of the
  reported gain were the penalty's cost on the SFT model, which DPO
  removed.
- Open until the next rows: what DPO gives when its samples are drawn
  without the penalty (`norp_s0/curve_fedavg`), and the base model, DPO
  round 1 and the `full` pair.

## 2026-11-16: the repetition penalty: checks first, new lines decode without it (owner)

Owner at about 18:10 on 2026-11-16: the repetition penalty of 1.1 lowers
EX and raises execution errors, it touches the whole paper; check it
first and turn it off.

What the code did: Qwen2.5-Coder's `generation_config.json` sets
`repetition_penalty: 1.1`. `StudentModel` (HF) takes it through
`model.generate`, `VllmStudent` read it from the same file and passed it
to vLLM. So every committed row was decoded with it: greedy evaluation,
the 8 samples of the DPO rounds, selection by execution, the peer check.
Both engines apply the penalty to the prompt tokens as well as the
output, so the table and column names of the schema, which the SQL has
to repeat, are penalized. SFT and DPO training do not decode and are not
touched; the DPO pairs are, through the samples.

Local check, not a committed result (HF on the Mac, fp16, base model,
`codes_v2`, 200 random Spider test questions, greedy):

| Repetition penalty | EX | Execution errors |
|---|---:|---:|
| 1.1 | 65.5 (131) | 37 |
| 1.0 | **71.0** (142) | **25** |

18 questions are right only without the penalty and 7 only with it; the
SQL differs on 128 of 200. With the penalty the model avoids repeating a
table name: it writes aliases (`T1`, `T2`), adds a join the question
does not need and puts the column under the wrong alias (`no such
column`: 34 of the 37 errors, 23 of 25 without the penalty). The size on
the trained adapters and on all 2,147 rows is what the queued rows
measure.

Code (`b0d117be`): `--repetition-penalty` on `scripts.eval_standard`
(and `experiments/eval_arms/run.py`), the DPO round, `scripts.peer_check`,
`scripts.exec_select` and `scripts.synth_questions`. Without the option
the generation config applies and every existing resume key and root
identity is unchanged (tests). In a DPO root the penalty is a setting of
the root. Arms without the penalty carry `_np`.

Queue (`d042d287`, pushed at 19:33):

1. Existing adapters on Spider test without the penalty: FedAvg R3 and
   DPO rounds 1 and 3 of the `codes` line, the base model with
   `codes_v2`, FedAvg R3 and its DPO round 3 with `full`.
2. One DPO round from FedAvg R3 of the `codes` line with samples drawn
   without the penalty (root `fedavg_np`), evaluated without it.
3. The `codes_v2` line (3 FedAvg rounds, 3 DPO rounds), centralized SFT
   and the F1 FedAvg rounds decode without the penalty.
4. The mechanism pilots move behind the DPO rounds of the `codes_v2`
   line and run on it; the synthetic rows are built again without the
   penalty in a new root (`sqlsynnp_coder15b_alpha01_s0`).

The server had started the pilots of the earlier queue before the push
(next entry) and was in the DPO round with synthetic questions (`codes`
line, with the penalty); `PIPELINE_NEXT.md` asks the owner to stop it,
pull and restart. Its files stay on the server.

## 2026-11-16: rejected-type pilot 2, peer adapter check, synthetic rows (`codes` line, with the penalty)

All decoded with the repetition penalty of 1.1 (entry above).

Rejected-type pilots, complete (`d4b497ec`, 18:51). DPO round 1 from
`hinton_k2aaa_a3` (73.31, 129 execution errors) on the round 1 samples of
the Hinton line, `full`, seed 0, Spider test:

| Rejected side | Pairs | EX | Execution errors |
|---|---:|---:|---:|
| every wrong sample (DPO round 1) | 5,393 | **75.69** | 82 |
| only samples that fail to execute | 3,317 | 75.36 | **70** |
| only samples with a wrong result | 2,949 | 74.38 | 119 |

The pairs against a failing sample give most of the round's gain (+2.05
of +2.38) and the fall in execution errors; pairs against a wrong result
give +1.07 and leave the errors near the start. The discordant questions
are not counted yet.

Peer adapter check (`8825bad8`, 19:17; `codes` line, DPO round 3, 560
questions with all 8 samples wrong):

| 32 samples from | Questions solved | Share |
|---|---:|---:|
| the four other clients' round 2 adapters (8 each) | 146 | 26.1% |
| the round 2 global adapter | **184** | **32.9%** |
| either | 207 | 37.0% |

23 questions are solved only by a peer adapter, 61 only by the global
adapter. At the same number of samples the other clients' adapters find
fewer correct SQL than the global model itself, so this check gives no
support for candidate B. Each peer adapter alone solves 64 to 78
questions with 8 samples; 8 more global samples solve 93.

Synthetic rows (`31379f82`, 19:23): 5,645 questions written, 5,494 kept
(1,042 to 1,176 per client), 151 dropped because one wording was written
for two queries. Not read by hand yet. The DPO round on them started at
about 19:23 and is the task to stop.

## 2026-11-16: rejected-type pilot 1, rejected side fails to execute

`415c62f3` (17:54 on 2026-11-16), arm `sqlrejexec_hinton_r1_vllm_inproc`:
DPO round 1 from `hinton_k2aaa_a3` on the round 1 samples of the Hinton
line (`full`, seed 0), pairs only where the rejected sample fails to
execute. Spider test, 2,147 rows.

| Round 1 from `hinton_k2aaa_a3` | Pairs | EX | Execution errors |
|---|---:|---:|---:|
| DPO, every wrong sample as rejected | 5,393 | 75.69 | 82 |
| rejected side fails to execute | 3,317 | 75.36 | 70 |

The discordant questions are not counted yet; the reading waits for the
second pilot (rejected side with a wrong result). The server took the
queue and code of `091415a1` with this publish, without a restart.

## 2026-11-16: mechanism pilots queued: synthetic questions at the clients, peer adapter check (owner)

Owner on 2026-11-16: yes to the pilot of synthetic
questions in its SQL-first form, yes to the peer adapter check, update
`LITERATURE.md`, and the queue holds the pilots of these directions.

Before it, a gap scan for the mechanism to add to the core (narrative,
web sources opened in the run; `LITERATURE.md` section 1.17 and gaps 6 to
8). Candidates it left, with the numbers of the `codes` line they rest on
(Spider test and client samples, seed 0):

| Candidate | What it does | Rests on | State |
|---|---|---|---|
| A | new questions for SQL generated on each client's own databases, as label-only rows of the DPO rounds | 72% of the client questions have all 8 samples right by round 3; pairs 6,626 / 4,244 / 3,706 | pilot queued |
| B | the other clients' adapters as extra samplers on questions the global model does not solve | 560 questions with all 8 samples wrong at round 3; vote of the five client adapters 76.85 against 75.69 for their average (`full`, round 1) | check queued, training pilot not queued |
| C | clients with few labelled questions, vote labels for the rest | vote labels 75.50 against gold labels 75.69 (one round, `full`) | not queued, changes the setup |
| D | a hint for questions no sample solves | the same 560 questions | not queued |
| E | CPU count of samples that pass on the client database by accident | none yet | not queued |

Left out by the scan: federated GRPO, other LoRA aggregation rules, an
expert per client, the teacher again, token or clause DPO, CoT.

Code (`9ec6e452`) and queue (`091415a1`), pushed at 17:45 on 2026-11-16:

- `fedicl_sql/preference/synthesis.py`, `scripts/synth_questions.py`: per
  client, the SQL of its rows is refilled on its own databases in four
  ways (other values 15%, other columns 35%, other tables 25%, another
  database of the client 25%); joins only along declared foreign keys,
  columns keep their kind and key role. A query is kept when it runs
  within 5 s to a non-empty result that is not a lone zero or NULL, at
  most 2 per query shape. The base model, no adapter, writes one question
  per query with 3 (SQL, question) examples from the client's rows. The
  new rows follow the client's rows in a new split.
- `--no-fallback-prefix syn:` on the DPO round: a synthetic question with
  no correct sample gives no pair, so its SQL is never the chosen side.
  The default rule and the identities of existing roots are unchanged
  (tests).
- `scripts/peer_check.py`: for the questions with all samples wrong at
  round 3, 8 samples from each other client's round 2 adapter and 32 new
  samples from the global adapter, labelled against gold on the client's
  databases. No training.

Pilots, all on the `codes` line, seed 0 (its adapters and samples exist;
the `codes_v2` line has none yet):

| Tasks | Run | Comparator |
|---|---|---|
| `peer_s0/check` | the peer check at round 3 | share of the questions solved by a peer adapter against the share solved by 32 more global samples |
| `synth_s0/build` | 1,200 queries per client, questions written through vLLM | by hand: about 30 synthetic rows |
| `synth_s0/round_synth`, `eval_synth` | one DPO round from DPO round 3 on the split with synthetic rows, arm `sqlsyn_dpo_fedavg_r4_vllm_inproc` | the plain round below; 77.36 at round 3 |
| `synth_s0/round_plain`, `eval_plain` | round 4 of the `codes` line, arm `sqlcodes_dpo_fedavg_r4_vllm_inproc` | 77.36 at round 3 |

Cut: one round, one seed. The synthetic round has more pairs than the
plain round, so the comparison is of the whole step, not of equal update
counts; a control with equal pair counts is not queued. No selection pass
on the synthetic rows beyond the pair rule (1 to 7 of 8 samples right).

Local checks, not committed results: the generator keeps 1,080 to 1,200
queries per client in seconds; of 32 questions the base model wrote, about
60% matched their SQL (wrong returned column, "after 2006" for `<>`). A
wrong question only costs the row when no sample reproduces the result of
its SQL; when some do, the model is pushed toward that SQL for a question
that does not ask it. The 30 rows read by hand after the build measure
how often. Nothing of the new code has run on the server (the vLLM paths
of both scripts, the round 2 client adapters and round 3 samples on
disk).

The pilots sit before the `codes_v2` line, which starts about 8 h later
than planned.

## 2026-11-16: the base model with `codes_v2` on Spider test

`d22463ca` (16:47 on 2026-11-16), arm `sqlcv2_base_vllm_inproc`, vLLM
inproc, greedy, 2,147 rows, seed 0. First task of the core-only queue, so
the worker was restarted on `9af6b7c7`; the stop and start times were not
reported.

| Base model, Spider test | EX | Execution errors | Wrong results | Prompt tokens, mean |
|---|---:|---:|---:|---:|
| `full` | 57.89 | 440 | 464 | 418 |
| `codes_v2` | 61.95 | 377 | 440 | 669 |

- `codes_v2` over `full`: +4.06, 258 questions gained and 171 lost
  (p < 0.001). The longest test prompt is 2,028 tokens.
- 352 of the 377 execution errors are `no such column` (a column taken
  from the wrong table), 15 `no such table`.
- Published zero-shot numbers for this model on Spider test are higher:
  67.61 (SLM-SQL) and 72.3 (SPFT-SQL, prompt not published). The gap to
  SPFT-SQL is 10.4 points before training and 4.8 after SFT (73.17 for
  FedAvg R3 with `codes` against its 78.0), so about half of it is there
  before any training.
- The instruction keeps the sentence "The examples below show SQL
  patterns for reference" although the prompt has no examples (k = 0).
  Every arm shares it, so comparisons inside the project are not
  affected.

## 2026-11-16: teacher and public stage out of the core, queue keeps the core (owner)

Owner decision at about 16:20 on 2026-11-16: stop the `codes` line from
the Hinton server stage now and keep only the core in the queue. This
replaces the order of the entry below.

What the decision rests on:

- The teacher's part is about one point and at the edge: after DPO on
  Spider test, Hinton over gold +1.49 (seed 0) and +0.47 (seed 1), +0.98
  pooled (p = 0.04), with `full`. The teacher may only see public data,
  and the published teacher gains of that kind are about 1 point; the
  large ones have the teacher on the training prompts or databases
  (`LITERATURE.md` sections 1.7 and 1.16).
- The public stage is more training data (BIRD with gold SQL), not a
  mechanism: with `codes` it adds 2.61 points at FedAvg R3 (75.78 against
  73.17), and with `full` gold SQL after DPO adds +0.42 pooled (not
  separable).
- The core recipe (on-policy samples, execution labels, DPO + SFT term,
  SQL-only) is CodeLutra's (arXiv 2411.05199, centralized, Llama-3-8B:
  Spider 67.9 after SFT, 76.6 at its best iteration). The paper needs a
  mechanism of its own on top of the core; neither the teacher nor the
  public stage is one. Literature read for this: `LITERATURE.md` section
  1.16 (`8cd7598`).

Stop: `sqlcodes_s0/curve_hinton` is stopped by hand (Ctrl+C on the GPU 0
worker) during DPO round 1. No result of its DPO rounds is published; its
outputs stay on the server. The stop time is not reported yet.

Queue `9af6b7c7` (no code change):

- Out of the task list: `sqlcodes_s0/curve_hinton` with its Spider dev,
  DK, Realistic, SYN rows and comment check; the `full` reference rows
  that had not run (5 local client models, centralized DPO); the server
  DPO gate on BIRD (`srvdpo_s0`, nothing ran). The gold control and a
  server stage with `codes_v2` are no longer planned. The 7B teacher,
  FedProx R3 and FedNTD rows with vLLM inproc are committed.
- New order: the base model with `codes_v2` on Spider test
  (`sqlcv2_base_vllm_inproc`, about 15 min); the rejected-type pilots
  (3.5 h); `codes_v2` FedAvg rounds (6.5 h) and DPO rounds (9 h) from the
  base model; centralized SFT with `codes_v2` (about 7 h); the FedAvg half
  of F1 with 20 clients and `codes` (6.5 h). About 33 h in all.
- Centralized SFT with `codes_v2`: the recipe of `p227_central_e3_s0`
  (pooled Spider train, 8,659 rows, 3 epochs, lr 2e-4, LoRA r 16, seed 0)
  with `--schema-style codes_v2 --max-len 7680`; result id
  `sqlcv2_central_e3_s0`, arm `sqlcv2_central_e3_vllm_inproc`.
- The two new rows answer where the SFT level sits: SPFT-SQL reports 72.3
  zero-shot and 78.0 after SFT for this student on Spider test (its own
  prompt), against 57.89 (base, `full`) and 73.17 (FedAvg R3, `codes`)
  here. The base row isolates the prompt, the centralized row the
  federated split.

Not approved, not queued: a pilot of the mechanism with the most support
in the literature, execution-verified data synthesis at the clients
combined with the DPO rounds (new code, about 6-8 h).

## 2026-11-16: queue order until the method decision (owner)

Owner decisions (2026-11-16, after the FedAvg rounds of the `codes` line
from the server stage and the comment check):

- Order: the DPO rounds of that line, the rejected-type pilots, the
  `codes_v2` line from the base model (3 FedAvg rounds, then 3 DPO rounds;
  new phase `sqlcv2_s0`), then the method decision (server stage, teacher
  or gold, prompt). F1 runs after the decision with the chosen prompt; its
  tasks left the task list. The `full` baselines and the server DPO gate
  stay at the end and run only while the decision is open. Queue
  `a7458d47`.
- The gold control of the `codes` line from the server stage may start
  from the earlier seed 0 gold server-stage adapter
  (`federated_stage__K2ce__s0__91bc5cfdd49b__ac34d6f9`). Whether it runs
  (17.5 h) is decided after the DPO rounds of the Hinton line; it uses
  `codes`, the prompt of the line it is compared with.

## 2026-11-16: `codes` line from the Hinton server stage, FedAvg rounds; comment check

Results `eff28d67` to `cd8d0e8b` (last at 14:42 on 2026-11-16). Spider test,
seed 0, `codes` prompts at the clients, vLLM inproc, batch 16. The server
stage is the seed 0 Hinton stage trained with `full` prompts on BIRD.

| FedAvg round | From the base model | From the Hinton server stage |
|---|---|---|
| 1 | 69.03 | 73.27 |
| 2 | 71.91 | 75.64 |
| 3 | 73.17 | **75.78** |

- Round 3: +2.61, paired +130 / -74; execution errors 205 to 136. With
  `full` the same step gave +2.05 (71.26 to 73.31).
- A round took 2.02 h, peak reserved 20.18 GiB.
- The DPO curve starts from round 3 (fixed by name; the curve rule marks
  round 2 as best because round 3 adds 0.14).

Comment check (`codes_cmt` at evaluation: the `codes` text with comments
from `test_tables.json`; 2,017 of 2,147 prompts carry a comment, 0 before):

| Adapter (`codes` line from the base model) | `codes` | `codes_cmt` | Paired | Execution errors |
|---|---|---|---|---|
| FedAvg R3 | 73.17 | **73.45** | +45 / -39 | 205 to 174 |
| DPO round 3 | 77.36 | **77.55** | +47 / -43 | 86 to 84 |

The missing comments on Spider test cost 0.2 to 0.3 point on these
adapters. The other changes of `codes_v2` (fewer redundant comments in
training, value limits, every matched value) are not measured by this
check.

## 2026-11-16: `codes_v2` and `codes_cmt` schema styles (owner: fix the prompt, then rerun)

Owner decision (2026-11-16): correct the `codes` prompt towards CodeS and
train the `codes` lines again; no schema filter, no BM25 matcher.

Code `12ccd01d`, `a3091816` (pushed 12:05 on 2026-11-16):

- `codes` is unchanged: every stored prompt of
  `sqlcodes_fedavg_r3_vllm_inproc` on Spider test, dev, DK, Realistic, SYN
  and BIRD dev re-rendered with 0 differences; client SFT and DPO prompts
  on 335 rows likewise.
- `codes_cmt`: `codes` with comments from the dataset's own tables file
  (same text as `codes` on Spider train and dev databases). Used only to
  re-evaluate the `codes` adapters on Spider test (queued, `7f5a7f8e`).
- `codes_v2`: that comment source; a comment equal to the column name
  without `_` and spaces is dropped; sample values stripped, empty ones and
  those above 25 characters dropped; every matched value of a column kept
  (sorted, at most 25); on BIRD the evidence is matched as well.

Prompt tokens (Qwen chat template), `codes` to `codes_v2`:

| Set | Mean | Max | Prompts with a comment |
|---|---|---|---|
| Spider client train (8,659) | 996 to 880 | 7,297 to 6,444 | 8,363 to 2,852 |
| Spider dev | 827 to 730 | 1,935 to 1,619 | 1,034 to 342 |
| Spider test | 677 to 669 | 2,053 to 2,028 | 0 to 350 |
| BIRD dev | 3,922 to 1,932 | 26,253 to 4,988 | 0 to 1,102 |

Still different from CodeS: no schema filter, exact whole-word matching on
text columns instead of BM25 plus LCS, names in original case and not
quoted (37 of 806 BIRD dev columns would be quoted, 4 in all Spider
databases). Not checked: BIRD train databases (not on the Mac).

## 2026-11-16: literature pass on server warm start and KD between rounds; vote of the five client adapters

A literature pass (about 25 papers: warm start, FedDF family, LLM-to-SLM
co-tuning, LoRA aggregation, federated Text-to-SQL; several read as
abstracts only) found no published server step that fits the setup and is
not already covered by a run here. The published gains rest on training
from scratch, strong client drift, public data from the clients' own
distribution, or DP noise. Three ideas were kept for the owner:

1. A Hinton KD step between FedAvg R3 and DPO on SynSQL rows that the
   federated student gets wrong and the teacher gets right (closest:
   arXiv 2305.12132, selection of public rows with a federated checkpoint).
   About 8 h for a one-round gate. Not queued.
2. The queued server DPO gate, read as a replacement for a client round.
3. FedDF-type fusion (distill the client ensemble into the averaged
   adapter on public prompts, arXiv 2006.07242), for F1 only.

Check for idea 3, CPU analysis of committed predictions (script not
committed; results compared with a 10 s budget and sorted rows, not the
official evaluator), DPO round 1 of the Hinton line, `full`, Spider test:

| | EX |
|---|---|
| Client adapters 1 to 5 | 75.36 / 75.50 / 74.66 / 74.24 / 75.08 |
| Averaged adapter | 75.69 |
| Result vote of the five | 76.85 |
| Any of the five right | 80.95 |

The five client adapters agree on one result for 1,682 of 2,147 questions.
The vote is 1.16 above the average: that is the most a fusion step could
recover with 5 clients.

## 2026-11-16: audit of the `codes` prompt against CodeS (arXiv 2402.16347)

Read-only audit of `fedicl_sql/data/spider.py` against the paper and the
official repository. No code changed. Our prompt copies CodeS's
serialization (types, primary and foreign keys, 2 sample values, matched
values) and differs in these places:

- Comments: the renderer reads `tables.json` three folders above the
  database, so Spider test (its file is `test_tables.json`) and BIRD get no
  comment, while training prompts do. Counted in the committed prompts of
  `sqlcodes_fedavg_r3_vllm_inproc`: Spider test 0 of 2,147, Spider dev
  1,034 of 1,034, Realistic 508 of 508, SYN 1,034 of 1,034, DK 408 of 535,
  BIRD dev 0 of 1,534. Every `codes` number on Spider test so far is
  measured with prompts that lack the comment field seen in training.
- Reported by the audit, not rechecked: CodeS drops a comment equal to the
  column name without `_` (244 comments on Spider train against our
  2,998, about 117 tokens a training prompt); CodeS strips sample values
  and drops those above 25 characters (BIRD dev schema 3,741 to 1,645
  tokens on average, `european_football_2` 25.9k to 4.5k); CodeS keeps
  several matched values a column, ours one (553 question-column pairs on
  Spider train and test); CodeS matches BIRD values against evidence plus
  question; CodeS filters the schema to 6 tables and 10 columns a table
  with a trained classifier (we have none).
- Training and evaluation render the same text for the same database
  (client SFT, DPO and the stored evaluation prompts).

Open, owner's decision: a corrected renderer changes the training prompts,
so the `codes` lines would be trained again.

## 2026-11-16: P1 on BIRD dev (`codes`, no server stage)

Results commit `c46c62cd` (08:18 on 2026-11-16), seed 0, vLLM `inproc`,
batch 16, BIRD dev 1,534 rows. EX and rows with an execution error:

| Adapter | `full` | `codes` | Paired, `codes` vs `full` |
|---|---|---|---|
| FedAvg R3 | 25.55 (610) | 27.38 (658) | +146 / -118 |
| DPO round 3 from it | 29.66 (439) | 30.38 (475) | +137 / -126 |
| DPO gain | +4.11 | +3.00 | |

- `codes` changes little on BIRD dev (+1.83 and +0.72), against +1.91 and
  +2.24 on Spider test. DPO gains on BIRD dev with both prompts.
- The distance to a line with a server stage on BIRD stays about 11 points
  (Hinton line, `full`, DPO round 3: 41.20).
- `european_football_2` (129 questions, `codes` prompts above the 7,680
  training limit, up to 26,253 tokens): `codes` loses there (FedAvg R3
  30.23 to 27.13, DPO round 3 33.33 to 32.56). Without it: 25.12 to 27.40
  and 29.32 to 30.18.
- Errors of `codes` DPO round 3: 344 of 475 are `no such column`.
- Each evaluation took 3.1 h (estimate was 1.25 h); row 2 of the queue
  starts about 3.7 h later than planned.

## 2026-11-16: `codes` is the prompt; the queue starts with the `codes` line from the Hinton server stage

Owner decisions (2026-11-16): `codes` is the prompt from now on; the queue
is fixed with the runs most likely to settle the method first.

Queue order after the BIRD dev rows of P1 (code commit of 03:05):

1. `sqlcodes_s0/curve_hinton_sft`, `curve_hinton`: the seed 0 Hinton server
   stage (BIRD, trained with `full` prompts, not retrained), then 3 FedAvg
   SFT rounds and 3 DPO + NLL rounds with `codes` prompts at the clients;
   Spider test every round, the four other Spider sets at both R3. It
   answers whether the public stage adds to the `codes` line (73.17 and
   77.36 without it). About 17.5 h.
2. The rejected-type pilots (unchanged).
3. F1 with `codes` prompts at the clients (it was `full`; nothing of it had
   started), every client.
4. The server DPO gate (`full`), moved behind F1 with every client; then F1
   with 10 of 20 clients, then the `full` baselines.

A server stage with `codes` prompts is not queued: the BIRD train prompt
lengths with `codes` are not measured (BIRD dev reaches 26,253 tokens),
and Hinton would need a new teacher logit cache. The start adapter of row
1 and of the F1 Hinton line is the earlier
`p237_phase_e_s0/hinton_k2aaa_k2/m_g`; the owner approves it by running the
pull command of `PIPELINE_NEXT.md`.

## 2026-11-16: earlier KD variants, read with the owner's permission

The owner allowed reading the earlier arms `seqkd`, `kid`, `dss`,
`goldplan`, `tsql`, `taid`, `arith` and `wise` (owner, 2026-11-16), with
the gold, Hinton and FedAvg rows of the same phases as comparators. A
reading of committed prediction files, not a new run. All rows: seed 0,
`full` prompts, HF engine, Spider dev (none has a Spider test row). Except
TAID, the chain is short: FedAvg round 1, one server epoch on BIRD, one
client round. Not read: `p228` (pass@k headroom), `p254` (SynSQL as public
data), `p256` (teacher few-shot); their runners exist in the archive.

| Question | Row and comparator | Spider dev | DK | Realistic | SYN | BIRD dev |
|---|---|---:|---:|---:|---:|---:|
| Teacher SQL as the target, 5,319 rows the teacher solves, right after the server stage | `seqkd_public` | **57.93** | **45.61** | **46.65** | **48.26** | **34.68** |
| | gold SQL on the same rows (`matched_gold_public`) | 56.29 | 43.18 | 43.90 | 44.87 | 31.68 |
| The same after one client round | `seqkd_terminal` | 64.99 | 50.28 | 57.68 | **54.55** | 28.42 |
| | `matched_gold_terminal` | 65.09 | 49.53 | **58.66** | 52.90 | 27.51 |
| | KID, KD that simulates inference-time errors (`kid_terminal`) | **65.47** | 50.28 | 57.09 | 54.16 | **28.94** |
| Teacher plan as a second task, 1,000 rows, after one client round | `p214_dss_terminal` | **63.35** | **48.97** | **56.30** | 50.97 | 24.05 |
| | teacher SQL only (`p214_seq_terminal`) | 61.51 | 48.79 | 54.13 | **51.45** | **24.45** |
| The same with every BIRD row, after one client round | gold SQL (`p215_gold_terminal`) | **65.86** | **51.21** | 57.68 | **53.48** | 29.53 |
| | teacher SQL + teacher plan (`p215_dss_terminal`) | 64.89 | 50.09 | 56.89 | 52.71 | 25.62 |
| | gold SQL + teacher plan (`p215_goldplan_terminal`) | 64.89 | 50.09 | **59.06** | 52.22 | **30.77** |
| Plan then SQL as the output format (Struct-SQL), after one client round | teacher plan (`p210_teacher_terminal`) | 52.22 | 39.63 | 43.31 | 40.14 | 17.73 |
| | no public data (`p210_fl_terminal`) | **56.38** | **42.62** | **47.24** | **44.00** | **18.38** |
| TAID in place of Hinton, 2 server epochs then 3 client rounds | `p240_taid_k2aaa_a3` | 70.70 | 54.21 | **62.20** | **57.16** | 39.57 |
| | `p237_hinton_k2aaa_a3` | **72.53** | **58.32** | 61.81 | 56.38 | 38.53 |
| | `p237_gold_k2aaa_a3` | 70.41 | 52.34 | 61.22 | 56.38 | **40.03** |
| Keeping the server stage through the client round (parent SeqKD; plain client round 64.99 / 28.42) | midpoint of the two adapters (`p29_seqkd_wise0p5`) | 63.64 | 49.72 | 52.76 | 51.45 | 33.25 |
| | KD task vector added to FedAvg, weight 0.5 / 1.0 (`p29_seqkd_arith*`) | 63.93 / 57.54 | 49.91 / 45.05 | 52.36 / 43.11 | 50.48 / 46.23 | 28.62 / 34.42 |
| | client KL toward the server-stage model (`p29_seqkd_terminal_ret`) | 61.61 | 46.92 | 50.79 | 49.90 | 30.31 |

- The teacher's SQL beats gold SQL on the same rows right after the server
  stage (+1.64 Spider dev, all five sets); one client round removes the
  difference on Spider dev (-0.10).
- A plan task helps on 1,000 rows (+1.84) and not with every row (-0.97
  against gold SQL); plan-then-SQL output is below FedAvg without public
  data.
- TAID is below Hinton on Spider dev (-1.83) and DK (-4.11).
- Every way of keeping the server-stage weights through the client round
  (midpoint, task vector, client KL; the gold parent gives the same
  picture) keeps more BIRD dev and loses 1 to 7.5 points of Spider dev
  against the plain client round.
- These rows do not cover `codes` prompts, Spider test, more than one
  client round (except TAID) or the DPO stage.

## 2026-11-16: earlier rows with SynSQL as the public pool, read with the owner's permission

The owner allowed reading `p254` and `p228` (owner, 2026-11-16). A reading
of committed prediction files, not a new run. `p254`: the server pool is a
SynSQL-2.5M subset with the SQL target-token count of BIRD train in place
of BIRD, everything else as the BIRD rows next to it; seed 0, `full`
prompts, HF engine. `p228` (pass@k of the client questions before DPO
existed) has no evaluation row and adds nothing to the pair statistics of
the current lines.

| Row | Public pool | Spider test | Spider dev | DK | Realistic | SYN | BIRD dev |
|---|---|---:|---:|---:|---:|---:|---:|
| Hinton server stage, 3 client rounds with replay of teacher targets (`mixkd50_k2aaa_a3`) | BIRD | **73.17** | **74.08** | **57.20** | **63.58** | **58.70** | **44.78** |
| | SynSQL | 72.99 | 70.70 | 54.95 | 61.22 | 54.84 | 29.79 |
| Gold server stage, 3 client rounds with replay of gold (`gmixgold_k2aaa_a3`) | BIRD | 72.61 | 71.57 | 53.83 | 62.01 | 55.13 | 41.26 |
| | SynSQL | 72.05 | 69.92 | 54.58 | 61.02 | 53.09 | 28.81 |
| FedAvg, 3 rounds (`fl_a3`) | none | 71.50 | 67.60 | 53.27 | 59.65 | 53.68 | 25.68 |
| Server stage alone, Hinton / gold (`*_k2_k2`) | BIRD | - | 62.28 / 59.09 | - | - | - | 43.61 / 43.48 |
| | SynSQL | - | 66.05 / 66.25 | - | - | - | 28.62 / 27.25 |

- Right after the server stage SynSQL is 4 to 7 points of Spider dev above
  BIRD, with no client data: it is the closer domain.
- After the client rounds the order turns: BIRD ends 0.2 to 0.6 above
  SynSQL on Spider test and 1.7 to 3.4 above on Spider dev. Public data in
  the clients' style adds less to client training than BIRD does.
- Not covered: a larger SynSQL pool (this one matches BIRD in size), the
  line without replay, `codes` prompts, the DPO stage.

## 2026-11-16: what the teacher holds that the student lacks: 4.5 points outside the student's 8 samples (local analysis)

No GPU run. Spider test, `codes`, seed 0, from committed files: the greedy
rows of the teacher and of DPO r3 from FedAvg R3, and the 8 samples of
`xsel_codes_dpo_r3`. The script is not committed.

| Student's 486 wrong questions | Questions | Teacher greedy right |
|---|---:|---:|
| A correct SQL among its 8 samples (not chosen) | 198 | 124 |
| No correct SQL among its 8 samples | 288 | 95 |

- Adding the teacher's greedy answer to the student's 8 samples lifts
  pass@8 from 86.45 to 90.96 (97 of the 291 questions the samples miss).
- The server stage so far does not move pass@8 on Spider test once DPO has
  run (`full`, seed 0 / seed 1): 85.00 / 84.96 with the Hinton stage,
  84.86 / 85.19 without it. Before DPO it adds about 1 point (84.68 / 84.49
  against 83.47 / 83.70). On the clients' training questions the gap stays
  after 3 DPO rounds: 500 / 518 questions with all 8 samples wrong against
  617 / 613.

## 2026-11-16: `codes` on the other Spider sets; the teacher with `codes` is 3.2 above the student; selection by execution with `codes`

Results commits `a00a5f62` (01:37) and `e2f048c7` (02:06): the first three
groups of the decision batch and the 7B teacher with `full` through vLLM.
Seed 0, vLLM inproc, greedy.

| Row | Spider test | Spider dev | DK | Realistic | SYN |
|---|---:|---:|---:|---:|---:|
| FedAvg R3, `full` | 71.26 | 67.89 | 52.15 | 58.86 | 53.77 |
| FedAvg R3, `codes` | 73.17 | 70.31 | 55.51 | 65.94 | 56.87 |
| DPO r3 from FedAvg R3, `full` | 75.13 | 73.11 | 58.88 | 63.58 | 58.32 |
| DPO r3 from FedAvg R3, `codes` | 77.36 | 73.79 | 60.19 | 70.67 | 60.83 |
| Method (Hinton stage, DPO r3, `full`) | 76.71 | 76.50 | 64.11 | 64.17 | 61.03 |
| Teacher 7B zero-shot, `full` | 78.39 | **78.72** | 63.93 | 73.82 | 65.47 |
| Teacher 7B zero-shot, `codes` | **80.58** | 78.05 | **66.17** | **75.59** | **65.67** |

The comparisons below are question by question from the committed
prediction files; the script is not committed.

- `codes` against `full` has the same sign in all ten comparisons (two
  rows, five sets). After DPO: Spider test +2.24, dev +0.68, DK +1.31,
  Realistic +7.09, SYN +2.51. Only Realistic is separable over databases
  (+3.71 to +12.08 over 19 databases, 61 / 25 questions); dev and DK are
  not separable by question either (82 / 75 and 47 / 40).
- The DPO stage gains on every set with `codes`: +4.19, +3.48, +4.67,
  +4.72, +3.97, each separable over databases.
- `codes` without a server stage against the method on `full`: Spider
  test +0.65, dev -2.71 (70 / 98), DK -3.93 (44 / 65), Realistic +6.50
  (71 / 38), SYN -0.19. The server stage and `codes` lead on different
  sets; no row has both.
- The teacher through vLLM bf16 with `full` gives 78.39 on Spider test
  (the earlier HF 4-bit row: 77.22) and 48.31 on BIRD dev; the method is
  1.68 below it on Spider test (173 / 137, p = 0.05).
- The teacher gains from `codes` on Spider test (+2.19, 130 / 83, +0.05
  to +4.41 over databases), not separably elsewhere (dev -0.68, DK +2.24,
  Realistic +1.77, SYN +0.19). It has no BIRD dev row with `codes`.
- With `codes` the teacher is above the student on every set: Spider test
  +3.21 (219 / 150, +0.58 to +5.85 over databases), dev +4.26, DK +5.98,
  Realistic +4.92, SYN +4.84. On Spider test the teacher is right on 219
  of the student's 486 wrong questions and on 161 of its 400 wrong
  results; one of the two is right on 87.56% of the questions. Errors on
  Spider test: teacher 69 execution errors and 348 wrong results, student
  86 and 400.
- Selection by execution on DPO r3 with `codes`, Spider test, 8 samples:
  greedy 77.36, fallback 78.90 at 1.32 model calls a question, result
  vote 79.83 at 8 calls; pass@8 86.45; 25 questions without an executable
  sample.

Not decided (owner): `codes` as the prompt of the paper; a server stage
with `codes`.

## 2026-11-16: F1 queued: 20 clients, with and without the server stage

Owner decisions (2026-11-16): F1 with and without the server stage is
queued now, so its results arrive before the method is fixed; the server
DPO round (`srvdpo_s0`) runs on the full BIRD train set, not a part.

Queued in phase `f1_s0`, after the decision batch and before the baseline
and centralized tasks: two lines, seed 0, `full` schema, the seed 0 recipe
(3 FedAvg SFT rounds, then 3 DPO + NLL rounds, Spider test every round,
vLLM inproc, batch 16). One starts from the base model; one from the seed 0
Hinton server stage (row `federated_stage__K2fkl__s0__132e798a5be2__8393f0f9`,
adapter `artifacts/protocol_v2/p237_phase_e_s0/hinton_k2aaa_k2/m_g`, the
start of `hinton_k2aaa_a3`; not retrained, since it does not depend on the
clients; `f1_s0/check_server_stage` checks its bytes against the start
recorded by `hinton_k2aaa_a1`). Every client first, then the same four
curves with 10 of 20 clients per round.

Choices where the approved F1 (2026-11-15) is not specific:

- Partial participation: 10 of 20 clients per round, drawn by ranking
  sha256 of (phase, seed, round, client); FedAvg and DPO rounds draw
  separately, and both lines draw the same clients in a round (the draw
  counts client rounds, not the server stage). Over 3 FedAvg rounds
  clients 1 and 18 never train, over 3 DPO rounds clients 7, 11 and 19.
- Both participation settings for both lines; partial costs about half a
  full line, so full participation runs first.

Split (`alpha_0.1/k20`, committed in `fedicl-sql` `bd50b4f7`):
`scripts/build_federated.py` with the `k5` settings (same 8,659 rows,
domain groups, alpha 0.1, seed 0, 150-row floor) and `--max-resample
5000`, because no draw within the default 100 clears the floor. Rebuilding
gives the same files. Every row is used once and no database is shared.

| Clients | Rows | Databases |
|---|---|---|
| smallest five (14, 5, 15, 9, 10) | 165, 187, 192, 215, 220 | 3, 7, 5, 4, 5 |
| the two middle ones (1, 8) | 358, 387 | 6, 5 |
| largest three (17, 2, 20) | 783, 869, 1,015 | 4, 7, 16 |

No client is empty; the smallest has 165 rows, about 10 SFT updates of 16
rows. FedAvg weights clients by rows; DPO weights by pair count, and a
client with no pair sends no update that round.

Comparators (5 clients, seed 0, Spider test): FedAvg R3 71.26,
`hinton_k2aaa_a3` 73.31, DPO round 3 from each 75.13 and 76.71;
centralized Spider SFT `sql_central_e3_vllm_inproc` 70.75.

Estimates from committed timings: a 5-client FedAvg round takes 5,200 to
5,830 s on the server (seed 1, 2026-11-12), almost all client training at
about 0.65 s a row, so a 20-client round is about 1.7 h with 15 more
model loads; a DPO round about 2 h 10 with 5 clients plus about 15 min for
the extra clients. About 13 h a line with every client, 7 h with 10 of 20.
Memory is that of the 5-client rounds (same rows and prompt lengths).

Code (`fedicl-sql` `ddcaf311`): `--clients-per-round` in
`experiments/federated/run.py` (`run`, `round`, `stage private`, `client`)
and `experiments/federated_pref/run.py`; the chosen clients enter the
round fingerprint and the round record. With the default (0) every
identity and result config is unchanged (full suite, the frozen identity
tests and the published stage config check pass).

Not verified: the 20-client round times; the server-stage adapter on the
server (checked by the first task of the Hinton line).

## 2026-11-16: decision batch, stage 2 queued: a server DPO gate on BIRD, the rejected-type pilots

Queued after stage 1 and before `sqldpo_s0/check_baselines` (seed 0,
Spider test and BIRD dev through vLLM inproc, batch 16). Nothing is decided
on a server DPO stage; these rows inform that decision.

- Server DPO gate (phase `srvdpo_s0`, outputs
  `artifacts/protocol_v2/srvdpo_coder15b_alpha01_s0/`). Step A: one DPO +
  NLL round at the server on BIRD train with evidence (9,428 rows, one
  pooled client, `bird_with_evidence`, BIRD evaluator with the 30 s
  budget), from seed 0 FedAvg R3 (`full`), with the sampling, pair rule and
  DPO settings of the `sqldpo_s0/fedavg` client round and `--max-len 7680`.
  Step B: one client round, the command of round 1 of `sqldpo_s0/fedavg`
  with `--start-adapter` on the Step A adapter. Comparators (Spider test):
  `sql_fedavg_r3_vllm_inproc` 71.26 (211 execution errors, 177 `no such
  column`), `sqldpo_fedavg_r1_vllm_inproc` 74.29 (107, 67),
  `sqldpo_fedavg_r2_vllm_inproc` 75.17 (98, 60). Step B against round 2
  asks whether a BIRD round can stand in for a client round; Step A against
  FedAvg R3 asks how much a public-data round alone moves the client
  domain. The teacher is not used.
- Rejected-type pilots (curves `sqldpo_s0/rejexec_hinton`,
  `rejwrong_hinton`): DPO round 1 from `hinton_k2aaa_a3` on the round 1
  samples of the Hinton line, the rejected side limited to samples that
  fail to execute, or to samples that execute with a wrong result.
  Comparator `sqldpo_hinton_r1_vllm_inproc` 75.69. Round 1 has 2,806 and
  2,587 pairs of the two kinds (entry below); the gold fallback stays.

Estimates: Step A about 12 h (8 samples per BIRD question about 0.5 h,
labelling on the BIRD databases about 1 h, both unmeasured; about 12,700
pairs from the BIRD dev EX of FedAvg R3, 25.55, at about 2.5 times the
tokens of a Spider pair, against 6,509 pairs in about 2 h 10 for the
FedAvg-start round on Spider), Step B about 2.2 h, evaluations about
10 min each: about 14.5 h. Pilots about 1 h 45 each (the reused-samples
round). Memory: BIRD train rows reach 6,779 tokens (committed token audit
of `p21_bird_qwen15b_integrity_t60_s0`, not remeasured); a pair whose two
rows exceed the 8,192-token pass runs as two one-row passes, and P1 client
3 with 7,300-token pairs peaked at 19.29 GiB.

Code (`fedicl-sql` `5d164721`): `--start-adapter` lets round 1 of a new
root start from an adapter of another root (recorded in the arm identity
with its file hashes and checked before training); `--rejected-kind`
(`any`, `exec_error`, `wrong_result`) filters the rejected side. Both
default to the old behaviour and leave existing setup and arm identities
unchanged (tests added).

Not verified: BIRD sampling, labelling time and pair count; the first DPO
batch on BIRD rows; whether every BIRD train database is on the server
(`srvdpo_s0/check_bird` checks before training).

## 2026-11-16: decision batch, stage 1 queued: `codes` beyond Spider test, the teacher with `codes`, selection with `codes`

Queued ahead of every task not started yet (phase `sqlcodes_s0`, seed 0,
no training), because the owner's decisions on `codes`, on the teacher and
on a server DPO stage wait on them:

- P1 FedAvg R3 and DPO round 3 (`codes`) on Spider dev, DK, Realistic and
  SYN (`rob_*`), then BIRD dev (`bird_*`), under the arm names of their
  Spider test rows. Comparators, question by question:
  `sql_fedavg_r3_vllm_inproc` and `sqldpo_fedavg_r3_vllm_inproc` (`full`),
  committed on all five sets with vLLM 0.33 inproc, batch 16, 4 score
  workers, seed 0, the same evaluators (Spider `spider_result_eq_v1`, BIRD
  `bird_official_set_pair_timeout30_v2`) as the new rows will use.
- The 7B teacher zero-shot with `codes` prompts (bf16, vLLM inproc) on
  Spider test and the four Spider sets (`eval_teacher_codes`). Its paired
  comparator is the `full` row of `sqldpo_s0/eval_teacher`, queued after
  it; the HF 4-bit row `p253teacher_zeroshot` (77.22) is another engine.
- Selection by execution over 8 samples on DPO round 3 with `codes`
  (`xsel_dpo_r3`, the `xsel_*` settings).

Prompt lengths, measured on CPU with the evaluation prompt builder and the
student tokenizer (chat template included); the Spider test means repeat
the 418 and 677 of the P1 entry:

| Set | `full` mean / max | `codes` mean / max |
|---|---:|---:|
| Spider test | 418 / 1,140 | 677 / 2,053 |
| Spider dev | 445 / 986 | 827 / 1,935 |
| Spider-DK | 422 / 960 | 843 / 1,877 |
| Spider-Realistic | 425 / 984 | 754 / 1,934 |
| Spider-SYN | 446 / 986 | 827 / 1,934 |
| BIRD dev | 981 / 2,264 | 3,922 / 26,253 |

- On BIRD dev the `codes` schema of `european_football_2` (129 of 1,534
  questions) is 25,919 tokens: the 2 sample values of the XML columns of
  `Match` (`cross`, `foulcommit`, `shotoff`, `shoton`, `corner`, ...) fill
  about 55,000 characters. The next longest `codes` schemas are
  `card_games` 3,591 and `california_schools` 2,317 tokens. vLLM sets its
  context to the longest prompt plus 256, under the model's 32,768, so no
  prompt is cut or dropped; these 129 prompts lie far beyond the 7,680
  tokens of training, so BIRD dev is read with and without that database.
- Spider-DK and BIRD databases have no `tables.json` next to them, so their
  `codes` columns carry no comment (column name in words); Spider dev,
  Realistic and SYN have them. This holds for the `codes` rows of every
  adapter.
- The matched-value scan reads every text column of the database per
  question: under 0.03 s on Spider, about 5-8 s on `card_games`,
  `codebase_community` and `european_football_2`; about 48 min for the
  1,534 BIRD dev questions on a laptop CPU. The evaluation built every
  prompt twice on the vLLM path (before decoding and while scoring); it now
  keeps the schema text per question (`experiments/eval_arms/run.py`,
  same prompts byte for byte, test added), and `scripts/exec_select.py`
  takes `--schema-style` (default `full`, identity unchanged).
- The teacher skips BIRD dev: its longest `codes` prompt (26,253 tokens,
  26,509 with the answer budget) against the KV cache that 0.80 of the card
  leaves next to the 7B weights is not measured, and each pass costs about
  50 min of prompt building.

Not verified: the 7B through vLLM has never run on the server
(`eval_teacher_codes` is the first such task); the prompt-building time on
the server CPU.

## 2026-11-16: pair statistics of the DPO rounds (client training questions)

From the committed `client_*_pairs_stats.json`, summed over the 5 clients.
These are the clients' training questions (8,659), not a test set.

Method line, seed 0 (`sqldpo_s0/hinton_gc`), at the start of each round:

| Round | All 8 right | All 8 wrong | Pairs | Rejected fails to execute | Rejected executes, wrong result | Sample accuracy |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 4,820 | 609 | 5,393 | 2,806 | 2,587 | 79.12 |
| 2 | 5,773 | 534 | 3,899 | 1,545 | 2,354 | 84.37 |
| 3 | 6,197 | 500 | 3,208 | 1,037 | 2,171 | 86.59 |
| 4 | 6,425 | 481 | 2,870 | 858 | 2,012 | 87.77 |

- The pairs whose rejected sample fails to execute fall by 63% in two
  rounds (2,806 to 1,037), those with a wrong result by 16% (2,587 to
  2,171): the rounds remove execution errors first.
- At the start of round 1, by server stage (seed 0 / seed 1): sample
  accuracy without a server stage 74.27 / 73.89, gold 77.50 / 77.62,
  virtual teacher 77.49 (seed 0), Hinton 79.12 / 79.13 (seed 2: 79.02);
  questions with all 8 wrong 736 / 800, 671 / 680, 681, 609 / 657.
- The `codes` line (`sqlcodes_s0/fedavg`), rounds 1-3: pairs 6,626 /
  4,244 / 3,706, sample accuracy 74.59 / 82.84 / 84.76.

## 2026-11-16: earlier server-stage variants, read with the owner's permission

The owner allowed reading these rows from before the 2026-11-05 fresh
start (owner, 2026-11-16); nothing else of the earlier work was read. A reading of committed prediction files
(`experiments/eval_arms/results/*/predictions/<arm>.csv`), not a new run.
All are SFT-stage rows (before DPO), HF engine, after 3 client rounds. A =
client round, K2 = 2-epoch server stage on BIRD, S = extra server step.

| Row | Schedule | Spider test s0 / s1 | Spider dev s0 | BIRD dev s0 |
|---|---|---|---|---|
| FedAvg (`p253ref_fl_a3` / `p227_fl_a3`) | A A A | 71.50 / - | 67.60 | 25.68 |
| gold server stage (`p253ref_gold_k2aaa_a3` / `p237_gold_k2aaa_a3`) | K2 A A A | 73.03 / - | 70.41 | 40.03 |
| Hinton server stage (`p253_hinton_k2aaa_a3` / `p237_hinton_k2aaa_a3`) | K2 A A A | 73.50 / **74.10** | 72.53 | 38.53 |
| short server Hinton step on 1,731 BIRD rows after client rounds 1 and 2 (`p248_fsl_k2asasa_a3`) | K2 A S A S A | not measured | 73.21 | 40.29 |
| one more server step on 5,193 BIRD rows before the rounds (`p253_k2plus_aaa_a3` / `p250_k2plus_aaa_a3`) | K2 S A A A | **73.87** / 73.40 | 73.21 | 37.81 |
| clients replay BIRD rows with the teacher's top-50 targets (`p253_mixkd50_k2aaa_a3` / `p248_mixkd50_k2aaa_a3`) | K2 A A A with replay | 73.17 / **74.57** | **74.08** | **44.78** |
| gold server stage, clients replay BIRD rows with gold (`p253_gmixgold_k2aaa_a3` / `p249_gmixgold_k2aaa_a3`) | K2 A A A with replay | 72.61 / 73.40 | 71.57 | 41.26 |
| centralized Spider + BIRD (`p253ref_central_mix_e3` / `p237_central_mix_e3`) | centralized | 73.78 / - | 73.21 | 43.68 |
| server KD after every round, the last included (`p253_fedcollm_style_k3`, seed 1) | A K A K A K | - / 66.88 | 63.73 (seed 1) | 43.42 (seed 1) |

In `fsl_k2asasa`, right after each server step Spider dev is 65.57 (`s1`)
and 68.28 (`s2`) and BIRD dev 45.18 and 43.68; the next client round
brings Spider dev back to 72.05 and 73.21 and BIRD dev to 39.77 and 40.29.

- On Spider test every variant with more public training lies within
  about 0.7 point of the plain Hinton server stage, and the sign flips
  between the two seeds (one more server step +0.37 / -0.70; replay with
  teacher targets -0.33 / +0.47).
- The interleaved step ends +0.68 on Spider dev (7 questions), one seed,
  with no Spider test row.
- Ending on a server step costs the client domain: 66.88 against 74.10
  (seed 1, Spider test).
- The clear gains of more public training are on BIRD dev (up to 44.78
  against 38.53).

## 2026-11-16: P1 result: the DPO gain holds with `codes`; `codes` adds 2.24, on value questions and two databases

`sqlcodes_s0/curve_fedavg` finished its 3 DPO rounds (curve `44bbc0f5`,
23:57 on 2026-11-15). Seed 0, Spider test, vLLM inproc, no server stage in
either schema. Round 1 of the `codes` line trained with the 30 mislabelled
client questions (entry below); the FedAvg R3 `codes` row still holds the 7
disk-full rows (73.17 is 73.41 on the other 2,140 rows; DPO round 3 is
77.48 there).

| Row | EX | Execution errors | of them `no such column` | Wrong results | Gold SQL with a value (974 rows) | Gold SQL without one (1,173 rows) |
|---|---:|---:|---:|---:|---:|---:|
| FedAvg R3, `full` | 71.26 | 211 | 177 | 406 | 60.99 | 79.80 |
| DPO r1, `full` | 74.29 | 107 | 67 | 445 | 64.17 | 82.69 |
| DPO r2, `full` | 75.17 | 98 | 60 | 435 | 64.89 | 83.72 |
| DPO r3, `full` | 75.13 | 101 | 61 | 433 | 64.78 | 83.72 |
| FedAvg R3, `codes` | 73.17 | 205 | 177 | **371** | 66.84 | 78.43 |
| DPO r1, `codes` | 76.62 | 94 | 72 | 408 | 71.87 | 80.56 |
| DPO r2, `codes` | 77.18 | 93 | 66 | 397 | 72.59 | 80.99 |
| DPO r3, `codes` | **77.36** | 86 | 63 | 400 | **72.79** | 81.16 |
| Method (Hinton DPO r3, `full`) | 76.71 | **58** | **41** | 442 | 66.12 | **85.51** |

"With a value": the gold SQL holds a quoted text or a number outside
`LIMIT` (the entry of 2026-11-15 counted quoted text only, 622 rows). The
comparisons below are from the committed prediction files; the comparison
script is not committed.

- The DPO stage gives the same gain in both schemas: +4.19 with `codes`
  (148 / 58 questions, database bootstrap +2.53 to +6.02), +3.87 with
  `full` (142 / 59, +2.25 to +5.56). `no such column` falls 177 to 63 and
  177 to 61.
- `codes` against `full` after DPO round 3: +2.24 (164 / 116, exact
  p = 0.005), the same size at every round (+2.33, +2.00, +2.24). The
  bootstrap over the 40 test databases gives -0.70 to +5.29: `codes` is
  better on 20 databases, worse on 15, equal on 5, and `art_1` (+20
  questions) and `bakery_1` (+21) hold 41 of the 48 net questions.
- The gain is on questions with a value: +8.01 (131 / 53). Questions
  without one lose 2.56 (33 / 63, p = 0.003); before DPO the loss was 1.36
  (51 / 67, not separable). The 63 lost rows pick another column or table
  (18 execution errors, 11 of them `no such column`), they do not add a
  condition. DPO gains less on these rows with `codes` (+2.73) than with
  `full` (+3.92).
- `codes` with no server stage against the method on `full`: +0.65
  (157 / 143, not separable). The two differ by slice: values 72.79
  against 66.12, no value 81.16 against 85.51.
- Round 3 against round 1 with `codes`: +0.75 (51 / 35, not separable);
  the curve's best step by its 0.5 rule is round 2.
- Mean prompt on Spider test: 418 tokens with `full`, 677 with `codes`.

Not decided (owner): whether `codes` becomes the prompt of the paper.

## 2026-11-15: P1 DPO round 1 trained, its evaluation stopped by WSL

The owner restarted the queue without the label fix, so P1 round 1 trained
with the 30 client questions labelled under the full drive C (clients 3
and 5). `sqlcodes_s0/curve_fedavg` finished training round 1 (2:45 after
the restart) and failed at 16:58 when its Spider test evaluation started
vLLM: WSL could not create the process (`getpwnam(user01st) failed 5`,
`fopen(/etc/default/locale) failed 5`, `I/O error`), so the distro could
not read its own files. A retry at 17:17 failed the same way. Code 5 is
EIO; the WSL disk file grows on the drive that holds it, so a full drive C
under that file is the likely cause (to check with the owner's drive and
distro listing). No code change.

## 2026-11-15: where the wrong results are; resampling on an empty result (local analysis)

No GPU run. Spider test, from the committed prediction files: an automatic
comparison of predicted and gold SQL (sqlglot syntax tree; a row can differ
in several parts) and a local execution of both on the test databases (10 s
limit). The scripts and their output are not committed.

Wrong-result rows (executable SQL, wrong result) by the part that differs
from gold, seed 0:

| Differs in | FedAvg R3, `full` | FedAvg R3, `codes` | Method (Hinton DPO r3, `full`) |
|---|---:|---:|---:|
| wrong results in all | 406 | **371** | 442 |
| columns in conditions | 181 | **140** | 201 |
| set of tables | **157** | 162 | 171 |
| literal values | 119 | **76** | 139 |
| condition operators | **118** | 119 | 129 |
| select columns | **106** | 112 | 114 |
| structure (nested queries, set operations) | **81** | 90 | 84 |
| distinct | 82 | **67** | 94 |
| group by | 71 | **68** | 83 |
| aggregate | 63 | 60 | **59** |
| order / limit | **41** | **41** | 47 |
| predicted result empty or zero, gold result not | 117 | **64** | 134 |
| right rows with an empty or zero result | 49 of 1,530 | 57 of 1,571 | 48 of 1,647 |

- 30% of the method's wrong results (134 of 442) return an empty or zero
  result where gold returns rows; 2.9% of its right rows do. An empty result
  is wrong in 134 of 182 rows.
- `codes` removes the value errors and nothing else: empty results 117 to
  64, literal values 119 to 76, condition columns 181 to 140; table-set and
  structure differences do not fall (157 to 162, 81 to 90).
- Table-set differences are not lowered by `codes` or DPO, but most are an
  extra table, not a wrong join path. Method, 442 wrong results: same
  tables as gold 271, an added table 109, a missing gold table 38, other
  24; 110 of its 1,647 right rows also use a different table set. So 61%
  of the wrong results are wrong inside the right tables (conditions,
  values, select columns, aggregates).
- The teacher zero-shot is right on 20 to 41% of every group (method:
  tables 37%, literal values 31%, structure 30%): no group is its own.
- One difference only: 132 of the method's 442 rows (distinct 22, group by
  15, order / limit 4 among them).

Inference rule, estimated offline: keep the greedy SQL unless it fails or
returns an empty or zero result, then take the committed 8-sample vote
(`experiments/exec_select/results/`). An estimate, not a run: the vote was
not restricted to non-empty results.

| Row | Greedy | Fallback | Vote | Rule | Questions resampled | Gained / lost against greedy |
|---|---:|---:|---:|---:|---:|---|
| FedAvg R3, seed 0 | 71.26 | 75.03 | **75.55** | 75.50 | 17.6% | 93 / 2 |
| FedAvg R3, seed 1 | 71.87 | 76.01 | 75.87 | **76.85** | 18.2% | 107 / 0 |
| DPO r3 from FedAvg R3, seed 0 | 75.13 | 77.04 | 76.76 | **77.22** | 13.3% | 47 / 2 |
| DPO r3 from FedAvg R3, seed 1 | 75.83 | 77.69 | **78.39** | 78.20 | 12.9% | 51 / 0 |
| Method, seed 0 | 76.71 | 77.69 | **78.39** | 77.92 | 11.2% | 27 / 1 |
| Method, seed 1 | 77.04 | 78.16 | 78.02 | **78.62** | 12.0% | 36 / 2 |

The rule costs about 2 model calls a question on the method (the vote: 9)
and gives +1.2 and +1.6 over greedy. On the rows with an empty result the 8
samples rarely hold a better answer, so these errors need the value in the
input, not another sample.

## 2026-11-15: full drive C reached P1: 7 test rows of FedAvg R3, 30 client questions of DPO round 1

`codes` against `full`, FedAvg R3, seed 0, Spider test, question by question
from the committed predictions (`sqlcodes_fedavg_r3_vllm_inproc`,
`sql_fedavg_r3_vllm_inproc`; the comparison itself is not committed):

| | `full` | `codes` |
|---|---:|---:|
| EX | 71.26 | **73.17** |
| Execution errors | 211 | **205** |
| of them `no such column` | 177 | 177 |
| Wrong results | 406 | **371** |
| Gold SQL with a quoted value (622 rows) | 56.11 | **65.59** |
| Gold SQL without one (1,525 rows) | **77.44** | 76.26 |
| Easy / medium / hard / extra | 88.1 / 74.8 / 64.8 / 49.0 | **91.5 / 75.4 / 65.2 / 54.1** |

- Right only with `full` 129, only with `codes` 170 (exact p = 0.02); the
  bootstrap over the 40 test databases gives -1.17 to +4.77, so the +1.91
  is not separable by database.
- The gain is on questions that need a value (+9.5 points); the rest lose
  1.2. Wrong results fall by 35 and `no such column` errors do not move, so
  the errors DPO removed on the `full` line (177 to 41) are all still
  there before DPO. Whether DPO removes them with `codes` is the pending
  P1 result.

Drive C was full during part of P1. `_execute` in
`fedicl_sql/eval/metrics.py` returns any SQLite error text as the error of
the SQL, so `database or disk is full` is scored as an execution error in an
evaluation and labelled `exec_error` on a sample (a gold SQL that fails this
way drops its question).

- FedAvg R3 `codes` (evaluated 08:37 to 08:40): 7 rows on `aan_1` carry the
  error and count as wrong. The committed 73.17 is a lower bound: 73.17 to
  73.50 on the 2,147 rows, 73.41 on the 2,140 rows without them. R1 and R2
  (R2 evaluated at 06:17) have none. No other result row since the fresh
  start has the error (`git grep` over `experiments/` and `audits/`).
- DPO round 1 samples of `sqlcodes_s0/fedavg` (owner's check on the server,
  questions whose record holds the error): client 1: 0, client 2: 0,
  client 3: 6 of 2,061, client 4: 0, client 5: 24 of 1,804. The adapters of
  clients 1-2, already trained, are clean; 30 of 8,659 questions (0.35%)
  hold a false label or lost their pair. Not counted: the candidates and
  pairs these 30 questions give.
- Until R3 is evaluated again, a DPO gain of P1 is read against R3 on the
  2,140 rows or with the 73.17 to 73.50 range.

No fix is written. Open (owner): label the 30 questions again before
clients 3 and 5 train, evaluate R3 again (about 3 min), and make a storage
error stop a run instead of becoming a label.

## 2026-11-15: P1 FedAvg rounds; DPO round 1 out of memory on client 3

P1 FedAvg with the `codes` schema, seed 0, Spider test, vLLM inproc
(curve `fbdd85bd`): R1 69.03, R2 71.91, R3 73.17. The `full` schema FedAvg
R3 of seed 0 is 71.26, so `codes` adds 1.91 points before any DPO.

P1 DPO round 1 stopped at client 3, update 11 of 194 (peak 17.67 GiB through
update 10): out of memory under the 0.88 cap in backward, 19.15 GiB
allocated and 4.75 GiB asked, which is the float32 attention tensor of
SDPA's math path for one `baseball_1` pair (2 rows x 12 heads x about
7,290^2). With `--micro-batch-tokens 8192` such a pair already had a pass of
its own, so halving the budget could not help. Fix (fedicl-sql `68cae2dd`,
full `pytest -q` 635 passed): a pair whose two rows exceed the budget scores
chosen and rejected in two one-row passes, in the reference and in the
updates, and a run with such pairs scores its reference again. Only client 3
`codes` pairs are affected (every `full` schema pair stays under 4,096
tokens a sequence); clients 1-2 of round 1 trained before the fix and are
kept, since none of their pairs splits. Peak of the one-row passes not
measured yet.

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
