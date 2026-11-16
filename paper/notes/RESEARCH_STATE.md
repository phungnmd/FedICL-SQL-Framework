# FedLS-SQL: research state

Updated 2026-11-16. The project restarted on 2026-11-05; everything decided
or measured before that date is archived and hidden (see `AGENTS.md`, "Fresh
start"). This file says what is fixed, what the method is, what the results
show and what is still open. Runs and reasons are in `LAB_LOG.md`.

## 1. Question

Several clients hold private Text-to-SQL data that cannot leave them. They
train a small model (SLM) together through federated learning, and only the
SLM is deployed. The server may hold a large frozen LLM teacher and public
data from another domain. How can the deployed SLM become measurably better
on the clients' domain than standard federated training?

Goal: a journal paper at Q3 or above with a good method that clearly beats
the federated baselines; the target is a direction, not a bar to hit rigidly
(owner, 2026-11-11). The teacher is an option, not a requirement (owner,
2026-11-06).

Main venue candidates (owner, 2026-11-14): Computers, Materials & Continua
(CMC) or Journal of Intelligent Information Systems (JIIS). Author guidance:
[CMC](https://www.techscience.com/cmc/info/auth_instru). The final venue is
not yet selected.

## 2. Fixed setup

| Part | Fixed choice |
|---|---|
| Student (deployed alone) | Qwen2.5-Coder-1.5B-Instruct, SQL-only output, greedy decoding |
| Prompt | `codes` schema (owner, 2026-11-16); every row before P1 uses `full`. New lines use the corrected renderer `codes_v2` (owner, 2026-11-16; `LAB_LOG.md`): CodeS-style serialization without CodeS's schema filter and value retriever |
| Decoding | Greedy, 256 new tokens. No repetition penalty from 2026-11-16 (owner); every row before that date was decoded with the penalty of the model's generation config, 1.1, in evaluation and in the DPO samples (section 5, item 11) |
| Teacher (optional) | Qwen2.5-Coder-7B-Instruct, frozen. If used, it runs only at the server and only on public data. Not used by the core (owner, 2026-11-16) |
| Clients | 5 clients on Spider train (8,659 rows), domain-cluster non-IID split `alpha_0.1/k5`. Private rows never leave a client. |
| Server public data (optional) | BIRD train with evidence (9,428 rows); SynSQL-2.5M may replace or join it (owner, 2026-11-07). Not used by the core (owner, 2026-11-16) |
| Communication | Clients send model updates, never data |
| Compute | Two RTX A5000 24 GB under WDDM (`fedicl-sql/docs/A5000_RUN_CONFIG.md`); GPU 1 is in use by another user for now |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation,
not differential privacy.

Metric: Spider test EX (2,147 rows), evaluated through vLLM
(`--vllm-determinism inproc`). Choices are made on Spider test, so it is
never called held-out. No choice has been made on Spider dev, Realistic, SYN
and DK (all four on the 20 Spider dev databases); they are the check that
does not depend on a choice.

## 3. Method

The story (owner, 2026-11-16): what a client holds and the server does not
is the database itself, and the method uses it twice, as content in the
prompt and as the training signal through execution. Standard federated
training uses the client's rows only as (question, SQL) text. Nothing but
adapter updates leaves a client.

Core (stages chosen by the owner on 2026-11-10, the prompt on 2026-11-16):

1. The `codes` prompt: each column carries its type, keys, 2 sample values
   and the text values of the database that the question quotes. It is
   CodeS's serialization (arXiv 2402.16347) and part of the setup: every
   baseline uses the same prompt.
2. FedAvg SFT: 3 rounds on the clients' Spider rows.
3. Federated DPO + NLL: 3 rounds, fixed for every line and seed. In a round
   each client samples 8 SQL for each of its questions from the current
   model, labels them by execution on its own databases, pairs a correct
   sample with a wrong one (the gold SQL is the chosen side when no sample
   is correct), trains on the pairs, and the server averages the updates.

Out of the core (owner, 2026-11-16): the server stage on BIRD and the
teacher. The public stage is more training data, not a mechanism of the
method, and the teacher's part of it is about one point: with `full`, after
DPO on Spider test, the Hinton stage leads no server stage by +1.40 and
gold SQL by +0.98 (two seeds pooled). With `codes` the stage adds 2.61
points at FedAvg R3 (75.78 against 73.17); its DPO rounds were stopped in
round 1 and are not in the queue. The measured rows stay as analysis
(section 4).

The claim rests on stage 3 and on the mechanism to be added to the core
(section 5, item 9), not on the prompt (owner, 2026-11-16). The prompt
lifts every model alike: after DPO +2.24 for the student on Spider test,
+2.19 for the 7B teacher zero-shot. What the paper reports about it is
that the gain of stage 3 holds under both prompts: +3.87 with `full`, +4.19
with `codes` (Spider test, seed 0). Federated learning is the setting the
method has to work in; the paper does not claim that federation produces
the gain (owner, 2026-11-11).

Closest prior work (`LITERATURE.md`, sections 1.16 and 2): CodeLutra
(arXiv 2411.05199) is the same recipe run centrally at 8B: samples from the
current model each iteration, execution labels, DPO with an SFT term,
SQL-only output; on Spider it goes from 67.9 after SFT to 76.6 at its best
iteration (Llama-3-8B). Also: federated DPO as local DPO with LoRA
averaging, on human preferences (OpenFedLLM, FedBiscuit); gold as the
chosen side (Iterative RPO); and reports that SQL-only DPO gave no gain at
7B and above (Liu et al., ACL 2025; ExCoT). Different here: the rounds run
at the clients, each on its own databases, at 1.5B. The recipe itself is
published, so the method needs a mechanism of its own on top of the core
(section 5, item 9).

## 4. What the results show

Seed 0 and seed 1 are complete for the three DPO lines; the soft-target
controls and the row without the NLL term are seed 0 only. Numbers and
commits: `LAB_LOG.md`. Every row of this section uses the `full` prompt,
and "the method" names the line with the Hinton server stage, the method
until 2026-11-16. The core is the row "DPO round 3 from FedAvg R3" (with
`codes`: section 5, item 7).

| Row | Spider test EX, seed 0 | Execution errors, seed 0 | Spider test EX, seed 1 | Execution errors, seed 1 |
|---|---:|---:|---:|---:|
| base model | 57.89 | 440 | | |
| centralized Spider | 70.75 | 219 | | |
| FedAvg R3 | 71.26 | 211 | 71.87 | 222 |
| virtual-teacher server stage, then FedAvg (`virtual_k2aaa_a3`) | 72.57 | 163 | | |
| self-teacher server stage, then FedAvg (`self_k2aaa_a3`) | 72.61 | 149 | | |
| gold server stage, then FedAvg (`gold_k2aaa_a3`) | 73.08 | 144 | 73.73 | 163 |
| Hinton server stage, then FedAvg (`hinton_k2aaa_a3`) | 73.31 | 129 | 74.06 | 132 |
| centralized Spider + BIRD (no privacy) | 73.96 | 163 | | |
| `hinton_k2aaa_a3` + NLL-only round | 73.50 | 117 | | |
| `hinton_k2aaa_a3` + 1 FedAvg SFT round | 74.15 | 132 | | |
| DPO round 1 from `hinton_k2aaa_a3`, with NLL / without NLL | 75.69 / 76.20 | 82 / 85 | | |
| DPO round 3 from FedAvg R3 | 75.13 | 101 | 75.83 | 95 |
| DPO round 3 from `gold_k2aaa_a3` | 75.22 | 71 | 76.57 | 71 |
| DPO round 3 from `virtual_k2aaa_a3` | 75.59 | 79 | | |
| DPO round 3 from `hinton_k2aaa_a3`, fixed round-1 samples | 74.99 | 94 | | |
| DPO round 3 from `hinton_k2aaa_a3` (the method) | **76.71** | **58** | **77.04** | 74 |

What each part adds, seed 0 (95% interval from a bootstrap over the 40
test databases):

| Part | Compared rows | Gain | 95% interval | Reading |
|---|---|---:|---|---|
| Whole method | FedAvg R3 to the method | +5.45 | +3.45 to +7.43 | clear |
| DPO stage | `hinton_k2aaa_a3` to the method | +3.40 | +2.21 to +4.53 | clear |
| DPO stage without a server stage | FedAvg R3 to its DPO round 3 | +3.87 | +2.23 to +5.60 | clear |
| Preference term | best SFT control to the method | +2.56 | +1.35 to +3.77 | clear |
| Against no privacy | centralized Spider + BIRD to the method | +2.75 | +0.84 to +4.64 | clear |
| Server stage after DPO | DPO round 3 from FedAvg R3 to the method | +1.58 | -0.09 to +3.20 | at the edge |
| BIRD with gold SQL after DPO | DPO round 3 from FedAvg R3 to DPO round 3 from gold | +0.09 | -1.64 to +1.84 | no difference |
| Teacher after DPO | DPO round 3 from gold to the method | +1.49 | -0.24 to +3.16 | at the edge |
| Teacher against a soft target, after DPO | DPO round 3 from `virtual_k2aaa_a3` to the method | +1.12 | -0.10 to +2.30 | at the edge |
| Soft target without the teacher, after DPO | DPO round 3 from gold to DPO round 3 from `virtual_k2aaa_a3` | +0.37 | -1.17 to +1.95 | no difference |
| Teacher before DPO | `gold_k2aaa_a3` to `hinton_k2aaa_a3` | +0.23 | -1.18 to +1.70 | no difference |
| NLL term, round 1 | DPO round 1 without NLL to DPO round 1 with it | -0.51 | -1.13 to +0.05 | no difference |

Both seeds pooled, clustered by question (95% interval):

| Part | Compared rows | Gain | 95% interval | Reading |
|---|---|---:|---|---|
| Whole method | FedAvg R3 to the method | +5.31 | +4.06 to +6.56 | clear |
| DPO stage | `hinton_k2aaa_a3` to the method | +3.19 | +2.35 to +4.03 | clear |
| DPO stage without a server stage | FedAvg R3 to its DPO round 3 | +3.91 | +2.82 to +5.01 | clear |
| Server stage before DPO | FedAvg R3 to `hinton_k2aaa_a3` | +2.12 | +0.95 to +3.29 | clear |
| Server stage after DPO | DPO round 3 from FedAvg R3 to the method | +1.40 | +0.32 to +2.47 | small, separable pooled |
| BIRD with gold SQL after DPO | DPO round 3 from FedAvg R3 to DPO round 3 from gold | +0.42 | -0.70 to +1.54 | no difference |
| Teacher after DPO | DPO round 3 from gold to the method | +0.98 | +0.05 to +1.91 | small, at the edge (p = 0.04) |

- The DPO stage is the solid part: 2.5 to 3.9 points from every start on
  both seeds, and
  the NLL term alone (+0.19) or more SFT rounds (+0.84, then a fall) do not
  give it. In round 1 the preference term alone does as well as DPO + NLL
  (76.20 against 75.69, not separable); at round 3 the preference term
  alone gives 76.76 against 76.71 on Spider test, seed 0, also level
  (`916e612d`; the other sets: `04861191`).
- Refreshing samples has a measured role: fixed round-1 pairs give
  75.69, 75.55 and 74.99 over three rounds, against 75.69, 76.43 and
  76.71 with fresh samples (Spider test, seed 0, `3767d097`). At round 3
  the on-policy line leads by 1.72 points (101 / 64 discordant questions,
  exact p = 0.0049), with 58 vs 94 execution errors. Fixed pairs yield
  more updates in rounds 2-3, so this is a comparison of the full refresh
  recipe, not equal update counts.
- Other sets: the method is above FedAvg R3 by 5.3 (Realistic) to 12.0 (DK)
  points on Spider dev, Realistic, SYN and DK (seed 0). After DPO the
  Hinton line leads the FedAvg line on every set and both seeds; pooled:
  Spider dev +3.53, DK +4.11, SYN +2.03, Realistic +1.38 (not separable),
  BIRD dev +11.38.
- The server stage after DPO: +1.58 on seed 0, +1.21 on seed 1 (84 / 110,
  p = 0.07), +1.40 pooled (p = 0.01). Within one seed the database
  interval touches zero. DPO closes a quarter to a half of the lead the
  stage had before it; the lead that stays is in execution errors (round
  3, seed 1: 74 against 95; wrong results 419 against 424).
- Where the gain comes from: executable SQL. From FedAvg R3 to the method,
  right rows +117, execution errors -153, wrong results +36. About 440 rows
  (20% of Spider test) are executable SQL with a wrong result in every row
  from the base model to DPO round 4; no stage lowers that count.
- The training pairs show the same: pairs whose rejected side is an
  execution error fall from 2,806 to 858 over four rounds, pairs whose
  rejected side is a wrong result only from 2,587 to 2,012.
- The line saturates: round 4 (76.94) is not separable from round 3; by
  round 4, 6,425 of 8,659 client questions have all 8 samples correct and
  58 execution errors are left on Spider test (2.7 points).
- The server stage after DPO, by seed. Seed 0: the gold stage ends level
  with no server stage (75.22 against 75.13) and the Hinton stage 1.49
  above it. Seed 1: the gold stage ends 0.75 above no server stage and the
  Hinton stage 0.47 above gold (76.57, 77.04). The gold line moves most
  between seeds (1.35 at round 3), so the seed 0 reading overstated the
  teacher's part. Pooled: teacher over gold +0.98 (p = 0.04), gold over no
  server stage +0.42 (not separable; separable on Spider dev, +2.08, and
  Realistic, +3.15). The BIRD stage keeps about 11.7 points on BIRD dev
  after DPO, with or without the teacher.
- Soft targets without the teacher (seed 0; `virtual_k2aaa_a3`, gold token
  0.73 and the rest uniform, and `self_k2aaa_a3`, the base student's
  logits; archived adapters, approved 2026-11-12 and 2026-11-13). Before
  DPO all four server stages are within 0.75 point on Spider test (gold
  73.08, virtual 72.57, self 72.61, Hinton 73.31); the Hinton stage leads on
  Spider dev and DK (over virtual +2.32 and +3.36). After DPO the virtual
  line ends with the gold line on every set (75.59 against 75.22 on Spider
  test) and the Hinton line 1.12 above it (69 / 93, p = 0.07), 3.48 on
  Spider dev, 3.93 on DK, level on Realistic, SYN and BIRD dev. A soft
  target alone does not give the lead; the control is one lineage on the
  seed whose gold line was low. The self-teacher stage costs 7.4 points on
  BIRD dev against the virtual one.
- On Spider test the Hinton line's lead after DPO sits on rows that flip
  between training lineages: where the gold and virtual lines agree (2,009
  rows) it is level (53 / 52); on the 138 rows where they disagree it is
  right on 96 (FedAvg line 82). On Spider dev and DK it also leads on the
  rows both agree on.
- The wrong results are not all out of reach: of the method's 442, 193 are
  right in at least one of the other 16 rows and 249 are wrong in every
  row.
- The teacher and the method have the same EX on Spider test and are right
  on different rows (teacher zero-shot 77.22, HF, 4-bit; archived row,
  approved 2026-11-12). Seed 0: 151 rows right only in the method, 162 only
  in the teacher; the teacher is right on 129 of the method's 442 wrong
  results and 33 of its 58 execution errors; at least one of the two is
  right on 84.26%. The teacher leads on medium and hard (82.3, 70.8 against
  79.8, 68.3), the method on extra-hard (63.0 against 57.7). The Hinton
  stage does not pass these rows on: after DPO its wins over the gold line
  are not on the rows the teacher gets right (64% against 66%).
- What the teacher's lead over the gold line is made of after DPO (seed 0,
  +32 rows): 25 from wrong results, 7 from execution errors, on extra-hard
  questions (63.0 against 59.9). Seed 1 does not repeat the extra-hard lead
  (62.7 against 63.6). Against the FedAvg line the lead is in execution
  errors on both seeds.
- Selection by execution at inference (seed 0, 8 samples, no training). A
  vote over result rows lifts FedAvg R3 to 75.55 and `hinton_k2aaa_a3` to
  76.53: level with DPO round 3 greedy from the same start (75.13, 76.71)
  in total, on different questions (they differ on 185 and 150 rows; 55% of
  the questions DPO gains were right under the start's vote). The two add
  up: the method with the vote reaches 78.39, +1.68 over its greedy output,
  +1.86 over the vote on its start and +2.84 over the vote on FedAvg R3.
  pass@8 stays near 85 in all four rows: DPO reorders the candidates and
  adds none.
- CoT at 1.5B does not help (plan + SQL: server stage 60.64, one template
  client round 62.69, self-taught rounds at most 60.64). It is a short
  analysis in the paper, not part of the method.

## 5. Open

1. The teacher's role: decided (owner, 2026-11-16), out of the core with
   the public stage. After DPO on Spider test the Hinton stage leads gold
   SQL by +1.49 (seed 0) and +0.47 (seed 1), +0.98 pooled (p = 0.04), and
   the virtual-teacher stage by +1.12 (seed 0, p = 0.07); gold and virtual
   are level. The lead is small, not given by a soft target alone, and
   about as large as the spread of the gold line between seeds (1.35).
2. Seeds. Two seeds for the three DPO lines; the DPO step and the method
   row repeat within 0.7 point. The teacher's gain over gold is at the edge
   after seed 1. Seed 2 was dropped (owner, 2026-11-15) after its Hinton
   line reached DPO round 1 (75.87 on Spider test, from 74.24); the paper
   reports two seeds for the main lines.
3. The NLL term and the pair labels. Without NLL, round 3 gives 76.76
   against 76.71 on Spider test, seed 0 (31 / 32 discordant questions).
   Dropping the term is an owner decision; the current seed comparisons
   use DPO + NLL. N2, one round without gold fallback from the same
   round-1 samples: result-vote labels 75.50, executability labels 74.99,
   gold labels 75.69 (Spider test, seed 0). The vote-label line for 3
   rounds is approved and not queued; the FedAvg half of F1 (20 clients)
   is queued.
4. What the federated setting costs in the DPO stage. Reference rows, not
   a condition of the claim. In round 1 each client's adapter alone gives
   74.24 to 75.50 on Spider test (mean 74.97), the averaged adapter 75.69.
   DPO with the same recipe on the pooled client data (centralized, 3
   rounds) left the queue on 2026-11-16 before it ran; centralized SFT
   with `codes_v2` is queued instead. A 3-round line without aggregation
   is not queued (new code, about 6 h).
5. Reference rows on the same engine, `full` prompts: the 7B teacher,
   FedProx R3 and FedNTD are committed with vLLM inproc on the six sets
   (earlier seed 0 adapters, approved 2026-11-13); the local client SFT
   models were not evaluated and left the queue on 2026-11-16. The
   baselines with the final prompt come after the method is fixed. Selection by execution over 8 samples
   at inference is in for four seed 0 rows (section 4); N3 repeats these
   four rows on seed 1.
6. The 20% of wrong results. The method does not touch them, and they
   bound EX at about 77. The focused DPO pilot (arm `fdpo`, Focused-DPO:
   the preference term on the span where chosen and rejected differ) did
   not lower them: round 1 gives 76.20 against 75.69 for DPO round 1
   (10 / 21, p = 0.07), with 439 wrong results against 440 and 72 execution
   errors against 82. The span is two thirds of the response, so the pilot
   does not separate focus from a larger preference weight. It is an
   ablation row unless the owner decides otherwise. Not chosen: stricter
   labels from mutated client databases. The two one-round pilots that
   limit the rejected side (`full`, from `hinton_k2aaa_a3`, 73.31):
   only samples that fail to execute 75.36 (3,317 pairs, 70 execution
   errors), only samples with a wrong result 74.38 (2,949 pairs, 119
   execution errors), every wrong sample 75.69 (5,393 pairs, 82). The
   pairs against a failing sample carry the larger part.
7. The schema format: `codes` (owner, 2026-11-16). P1 (`codes`: types,
   keys, 2 sample values and the matched text values per column) gives
   77.36 after DPO round 3 against 75.13 with `full` on Spider test (seed
   0, FedAvg line), and is above `full` on Spider dev, DK, Realistic and
   SYN. Open: whether the corrected renderer `codes_v2` holds these
   numbers (the base model alone: 61.95; queued: 3 FedAvg rounds and 3 DPO
   rounds from the base model, centralized SFT), and the baselines and second
   seed with the final prompt.
8. A DPO round at the server on public data: dropped with the public
   stage (owner, 2026-11-16). The gate did not run.
9. A mechanism of its own: two candidates in pilot (owner, 2026-11-16).
   The core is CodeLutra's recipe in a federated setting at 1.5B, so the
   recipe cannot carry the paper's novelty. A gap scan of 2026-11-16
   (`LITERATURE.md`, sections 1.16, 1.17 and 3) left five candidates:
   - A, new questions on the client's own databases. Each client refills
     the SQL of its labelled questions on its databases (other values,
     columns, tables or another of its databases), keeps the queries that
     execute to a non-empty result, and the base model writes a question
     for each. In a DPO round the synthetic SQL is only the label: a
     synthetic question trains when some of its 8 samples match the result
     of its SQL and some do not, and its SQL is never the chosen side. Why
     here: the loop runs out of questions (72% of the client questions
     have all 8 samples right by round 3, pairs fall 6,626 / 4,244 /
     3,706). Closest: SPFT-SQL (synthesis, weak preference stage),
     CodeLutra (the loop, no synthesis); their combination is not
     published, and no federated paper checks synthetic rows by execution
     at the client. Pilot queued on the `codes_v2` line without the
     repetition penalty: one DPO round with the synthetic rows from its DPO
     round 3, against a plain fourth round.
   - B, the other clients' adapters as extra samplers. For a question
     where all 8 samples of the global model are wrong (560 at round 3),
     a client also samples from the adapters the other clients trained in
     the last round; a correct one becomes the chosen side instead of the
     gold SQL. Closest: FedMatch (helper models for pseudo-labels, vision).
     The only candidate where federation itself has a role. The check on
     the `codes` line (with the repetition penalty, `8825bad8`) does not
     support it: of the 560 questions, 32 samples from the four peer
     adapters solve 146 and 32 more samples from the global model solve
     184; 23 are solved only by a peer, 61 only by the global model. The
     check runs again on the line without the penalty. The training pilot
     (about 3 GPU h) is not queued.
   - C, clients with few labelled questions and vote labels for the rest
     (changes the data assumption, about 6 GPU h); D, a hint for questions
     no sample solves; E, a CPU count of samples that pass by accident, on
     mutated databases. Not queued.

   Reading of the scan against the venues: the core with A is "SPFT-SQL
   plus CodeLutra, federated, at 1.5B", a combination with a measured
   reason; a part where federation has a shown role (B or C) is what would
   lift it above that.
10. The SFT level. SPFT-SQL reports 72.3 zero-shot and 78.0 after SFT for
    this student on Spider test with its own prompt; here the base model
    gives 57.89 (`full`), 61.95 with `codes_v2` (`d22463ca`), and FedAvg
    R3 73.17 (`codes`). The gap to SPFT-SQL is 10.4 points before training
    and 4.8 after SFT, so about half of it comes from the prompt and
    inference side, not from the federated split. Queued: centralized SFT
    with `codes_v2`.

11. The repetition penalty (owner, 2026-11-16). Qwen2.5-Coder's generation
    config sets a repetition penalty of 1.1, and every row so far was
    decoded with it: greedy evaluation and the DPO samples, HF and vLLM.
    The penalty also covers the prompt tokens, so the table and column
    names the SQL has to copy from the schema are penalized. It may
    account for part of the execution errors (352 of the base model's 377
    are `no such column`) and for part of what the DPO stage gains, since
    that gain is in executable SQL (section 4). Not measured yet. Queued
    first: the existing adapters on Spider test without the penalty (base,
    FedAvg R3, DPO rounds 1 and 3 with `codes`; FedAvg R3 and DPO round 3
    with `full`), then one DPO round from FedAvg R3 with samples drawn
    without it. New lines decode without the penalty; whether the numbers
    of section 4 are rerun depends on these rows.

## 6. Current phase

The three DPO lines have two seeds. Seed 0 also has the soft-target
controls, 3 rounds without NLL, one round without gold fallback, the local
adapters of round 1 and selection by execution (last published result
`3767d097`, 06:36 on 2026-11-14, including the offline control).

P1 (`codes` schema, FedAvg line, seed 0) is published (`44bbc0f5`), and
`codes` is the prompt (owner, 2026-11-16); new lines use `codes_v2`. On
BIRD dev P1 is at 27.38 (FedAvg R3) and 30.38 (DPO round 3), `full` at
25.55 and 29.66 (`c46c62cd`). With comments in the Spider test prompt the
`codes` adapters score 73.45 (FedAvg R3) and 77.55 (DPO round 3) instead of
73.17 and 77.36 (`cd8d0e8b`).

The teacher and the public stage left the core on 2026-11-16 (owner). The
`codes` line from the seed 0 Hinton server stage has its 3 FedAvg rounds
(73.27 / 75.64 / 75.78, `bff4f42b`, against 69.03 / 71.91 / 73.17 without
the stage); its DPO rounds were stopped in round 1 and no result of them
is published. The base model with `codes_v2` gives 61.95 on Spider test
(`d22463ca`, against 57.89 with `full`). The queue (`d042d287`) holds, in order:
the repetition penalty checks (section 5, item 11), the `codes_v2` line
from the base model without the penalty (3 FedAvg rounds, 3 DPO rounds),
the two mechanism pilots on that line (the peer adapter check; a DPO
round with synthetic questions against a plain fourth round), centralized
SFT with `codes_v2`, and the FedAvg half of F1 (20 clients, `codes`). Out of the
queue: the gold control, a server stage with `codes_v2`, the server DPO
gate, the local client rows and centralized DPO with `full`. Approved and
not queued: DPO with result-vote labels for 3 rounds. Run commands,
live-state provenance and estimates are in `PIPELINE_NEXT.md`.

The preference term stays plain and the core keeps DPO + NLL. First the
repetition penalty rows are read (section 5, item 11): they say how much
of the DPO gain stands without the penalty. The mechanism to add to the
core (section 5, item 9) is decided after them, from the two pilots.

## 7. Directions after the queue

Proposals (2026-11-16), not approved and not queued unless marked. Each
row of the table depends on a result of the queue. The rows that needed
the server DPO round or the teacher with `codes` left with the public
stage (2026-11-16).

| If the batch shows | Then try | Aims at | Cost (estimate) |
|---|---|---|---|
| Pairs with a wrong-result rejected sample carry gain (rejected-type pilots) | Pairs built for that error: gold SQL with one clause changed, executable, different result, as the rejected side (closest: CAPER, arXiv 2606.03327, clause-level tuples for a reward model); or a larger share of wrong-result pairs | EX: the 400 wrong results left after DPO | about 2.5 h a one-round pilot, new code |
| Those pairs carry no gain | Stop adding preference variants for wrong results; the rule drops them and halves client training | client cost | none |
| `codes` holds on the other sets | A length limit on sample values (BIRD `european_football_2` gives 26k-token prompts); seed 0 again without the 30 mislabelled questions | a clean main row | 8 to 16 h |
| `codes` keeps losing on questions without a value | `full` plus the matched values only | EX on the 1,173 questions without a value | about 16 h a line |

Independent of the batch:

- F1, the FedAvg SFT rounds with 20 clients (queued 2026-11-16, phase
  `f1_s0`, `codes`). With 5 clients FedAvg equals centralized training.
  With 20 clients each holds about 430 rows and about 270 pairs in DPO
  round 1; the run shows whether FedAvg then falls behind. The DPO rounds
  with 20 clients (about 11 h) and 10 of 20 clients per round are not
  queued.
- Sampling only the questions that are not saturated: 56% of the client
  questions have all 8 samples right at DPO round 1, 72% at round 3
  (method line, seed 0), and give no pair. A count of how many return
  needs the sample files on the server.
- Inference: resample only when the greedy SQL fails or returns an empty
  result (estimated offline at +1.2 and +1.6 on the method with `full`,
  about 2 model calls a question); a real run with the final prompt.
- Round and setting choices on a public validation set instead of Spider
  test, if its curve follows Spider test.
