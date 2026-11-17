# FedLS-SQL: research state

Updated 2026-11-17. On this date the owner set the project up again from
clean: a new prompt, refactored code (package `fedls_sql`) and every result
produced again. This file says what is fixed, what the method is and what
is open. Runs and decisions are in `LAB_LOG.md`.

## 1. Question

Several organisations each hold databases and questions with gold SQL that
cannot leave them. They train a small model together through federated
learning, and only that model is deployed. Standard federated training
(FedAvg SFT) uses the gold SQL and never the databases.

Main question: does training on the execution of the model's own SQL on
the clients' databases give a better model than FedAvg SFT on the same
data?

Second question: a server usually has public Text-to-SQL data. Does
pre-training on it help, and does the gain of the main part remain on top
of it?

Goal: a journal paper at Q3 or above (candidates: CMC, JIIS) with a method
that clearly beats the federated baselines and reports good numbers.

## 2. Setup

| Part | Choice | State |
|---|---|---|
| Student (deployed alone) | Qwen2.5-Coder-1.5B-Instruct with LoRA, SQL-only output | fixed |
| Clients | 5 clients on Spider train (8,659 rows, 146 databases), split `federated/alpha_0.1/k5` (split seed 42): every database whole at one client, Dirichlet (alpha 0.1) over four complexity tiers of the databases; private rows never leave a client | built 2026-11-17 after `FEDERATED_DATA_SETUP.md`; whether it poses a problem is open, section 4 |
| Teacher | Qwen2.5-Coder-7B-Instruct, frozen, at the server, on public data only | not part of the method (owner, 2026-11-17); a research direction, section 4 |
| Public data | BIRD train with evidence (9,428 rows); SynSQL-2.5M may replace or join it | fixed |
| Decoding | greedy, no repetition penalty (the code sets 1.0 and never reads the model's generation config) | fixed |
| Metric | Spider test EX (2,147 rows) through vLLM. Rounds, steps and settings may be chosen on Spider test (owner, 2026-11-17); the lab log records what was chosen on which set, and the paper does not call such a number held-out | fixed |
| Prompt | the Text-to-SQL prompt of the Qwen2.5-Coder evaluation code (schema text, a line naming SQLite, the question, a request for the SQL only), one for training, sampling and evaluation | layout fixed; schema text open between `ddl_rows` and `ddl_values`, section 4 |
| Length | `--max-len 7168`, no truncation (a longer row stops the run); 256 new tokens | fixed |
| Training recipe of the SFT baselines | LoRA SFT at lr 2e-4, 3 FedAvg rounds of 1 local epoch (the recipe of SPFT-SQL for this student is lr 2e-4, 3 epochs) | open, section 4 |
| Compute | RTX A5000 24 GB under WDDM; GPU 1 is in use by another user | fixed |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation,
not differential privacy.

## 3. Method

One core part and one secondary part (owner, 2026-11-17, replacing the
three stages set earlier that day: a server stage with the teacher, FedAvg
SFT, federated DPO).

| Part | Where | Supervision | Place |
|---|---|---|---|
| Federated DPO + NLL | clients | execution of the model's own SQL on the client's databases | the core |
| Pre-training with the same loss | server | execution of the model's own SQL on public data that has gold SQL | secondary; in the method if the results support it |

No SFT stage comes before the DPO rounds; FedAvg SFT is a baseline. The
teacher is not part of the method; what it could add is a research
direction (section 4).

### 3.1 The story (draft, owner, 2026-11-17; follows the results)

In one sentence: a client holds not only labels but also the databases to
run SQL on; FedAvg SFT uses the labels, the method uses both.

1. Setting. Each organisation has its own databases and its own questions
   with SQL, and cannot share them. They train one small model together.
2. What is missing. FedAvg SFT makes the model imitate one gold SQL per
   question. It never tells the model which of its own outputs are wrong.
3. Observation. Text-to-SQL can be checked by running the SQL, and the
   only place where it can be run is the client, where the databases are.
   The server never has this signal.
4. Method. In each round a client samples SQL from the global model, runs
   it on its own databases, pairs correct samples with wrong ones and
   trains with DPO + NLL. The server averages.
5. Why it fits federated learning. A federated round is one re-sampling
   iteration of the DPO loop: the errors of the new global model are found
   again in the next round at no extra cost. The reference is the round's
   global model, so every client moves the model from the same point.
6. Cost. No extra data and no extra communication (the same adapter is
   sent). The extra cost is compute at the client, for sampling and
   running SQL.

The second question, pre-training. If pre-training on public data helps
and the gain of the rounds remains on top of it, the story becomes one
objective in two places: the server learns from execution on public
databases, the clients from execution on their own. Public data gives
general SQL skill; the clients correct what public data does not hold,
their schemas and the model's errors on their databases. If pre-training
lifts every row and the gain shrinks, it stays in the notes and the paper
keeps the main line.

What the results have to show:

| Part of the story | Result that carries it |
|---|---|
| Execution at the client adds to the labels | federated DPO above FedAvg SFT, from the same start and for the same rounds |
| The gain comes from correcting the model's own errors | the gain grows over the rounds and sits in the hard and extra columns |
| It holds under non-IID data | the gain remains at alpha 0.1, 0.5 and IID |
| Pre-training helps and does not use up the gain | pre-training + federated DPO above pre-training + FedAvg SFT |

The first row decides the story. In CodeLutra the first iteration only
equals SFT on gold and the gain comes in iterations 2 and 3, so the
comparison needs enough rounds.

### 3.2 The core in a round

Only the small model's adapter leaves a client.

1. The server sends the global model.
2. Each client samples several SQL for each of its questions from that
   model, runs them on its own databases and labels each by comparing its
   result with the gold result.
3. A question with both correct and wrong samples gives pairs: a wrong
   sample with a correct sample of the model. A question whose samples are
   all wrong or all correct gives no pair in that round and is sampled
   again in the next.
4. The client trains with DPO plus an NLL term on the chosen side. The
   reference of the DPO term is the round's global model.
5. The server averages the updates.

Choices inside the rounds (owner, 2026-11-17):

- The base form is CodeLutra's: the plain loss, pairs drawn at random, and
  nothing from a question whose samples are all wrong.
- Three changes to it are candidates, each to be checked by a run and
  taken into the method only on a clear gain: the gold SQL of an all-wrong
  question in the NLL term (never as the chosen side of a pair); each
  wrong sample paired with its nearest correct sample; the rejected side
  counted only on the tokens that differ.
- The method uses the clients' labelled questions only. Unlabelled
  questions are not part of it.

### 3.3 Pre-training at the server

The secondary part runs the same loop once at the server, before the
rounds, on public data. It gives the student the output format and general
SQL skill without using up the pairs on the clients' questions, which the
student has not seen.

### 3.4 Closest work

CodeLutra (arXiv 2411.05199), the same loop run centrally at
8B. It starts from the base model with no SFT stage (its SFT model is a
separate baseline), draws 10 samples at T 1.0, uses only the model's own
correct samples as the chosen side, and trains DPO + SFT with beta 0.1 and
lambda 1.0, LoRA r 8, lr 5e-5, one epoch per iteration, 4 iterations.
Different here: federated and at 1.5B. A round is an iteration, the pairs
are made at each client by execution on its own databases, and the
reference is the round's global model. OpenFedLLM (arXiv 2402.06954) runs
DPO inside FedAvg with fixed pairs and a reference fixed for all rounds.
The papers behind each choice are in `DPO_RESEARCH.md`; the rest of the
map is in `LITERATURE.md`.

## 4. Open

1. The schema text of the prompt. Both candidates are in the code
   (`--schema-style`), with the same layout around them; checked practice
   is in `LITERATURE.md`, section 1.19.

   | Style | Schema text | After | Longest Spider train sequence | Longest Spider test prompt |
   |---|---|---|---:|---:|
   | `ddl_rows` (A) | `CREATE TABLE` text and 3 example rows per table | the Qwen2.5-Coder evaluation code on Spider (Rajkumar et al. 2022; Chang and Fosler-Lussier 2023) | 6,927 tokens | 2,547 |
   | `ddl_values` (B) | `CREATE TABLE` text rebuilt per column, 2 example values of each column as a comment | the schema text of OmniSQL, without its column descriptions and question-matched values | 6,440 | 1,939 |
   | `ddl` | `CREATE TABLE` text alone | the same evaluation code on BIRD; CodeLutra | 2,334 | 1,086 |

   The base model with no training gives the same level with both (68.05
   and 67.49, section 5), and the outputs show no defect of the prompt or
   the decoding. The choice between A and B is made on the gain of the
   federated DPO rounds over FedAvg SFT with each.
2. The training target is the gold SQL without a final `;`, followed by
   the end-of-turn token. No other normalization (CodeS upper-cases
   keywords and lower-cases identifiers; not done here).
3. Settings of the DPO rounds. The code defaults are CodeLutra's: 10
   samples per question at temperature 1.0, 10 pairs per question drawn
   at random, beta 0.1, NLL weight 1, lr 5e-5, 1 epoch per round, weight
   decay 1e-4. Open: the number of rounds; LoRA rank 16 for every line
   against 8 in the paper; the NLL term as a per-token mean, where the
   paper writes the log-likelihood of the sequence; the aggregation
   weights (pair counts here, question counts in FedAvg SFT).
4. The SFT shuffle seed is the same for every client and round. (The
   sampling seed of the DPO rounds is now derived per round and client.)
   LoRA dropout is 0.05 in SFT and 0 in DPO, and AdamW keeps its default
   weight decay of 0.01; both are to be set on purpose with the recipe.
5. The teacher, as a research direction. In the earlier setup its own
   part was small against gold SQL on the same public data. In the papers
   (`DPO_RESEARCH.md`, section 2.7), a teacher's SQL is no better a target
   than gold SQL, forward KL to the teacher is below training on gold
   alone, and reverse KL on the student's own samples is above it.
   A question to guide this direction, not a planned part: at the server,
   can the LLM repair a wrong SQL of the student with a small edit, so
   that a question whose samples are all wrong still gives a pair, with
   execution deciding whether the repair is kept? (`DPO_RESEARCH.md`,
   section 3.7.)
6. Baselines with the new prompt: FedAvg, FedProx, FedNTD, centralized SFT.
7. The client split. In `alpha_0.1/k5` the share of hard and extra
   questions runs from 20% to 60% across the clients, and the clients
   hold 734 to 3,479 questions (table in `LAB_LOG.md`, 2026-11-17). No
   client lacks a hardness level: the client of the simplest tier still
   has 20% hard or extra questions. Whether the split gives a reason to
   federate is read from three rows: local training per client, FedAvg,
   centralized. If the local model of the simple client is not below
   FedAvg on the hard and extra columns, the split is too mild.
8. Whether the clients' questions give enough pairs. Read without
   training: 10 samples per question on each client, counted as all wrong,
   mixed and all correct, from the base student and from the student after
   the server pre-training. The pre-training moves hard questions into the
   mixed group and easy ones out of it; which side wins is not known.
   The read from the base student is queued (`pairread/*`).
9. The three candidate changes of section 3, each as a run against the
   base form from the same start and for the same rounds:
   - the gold SQL of all-wrong questions in the NLL term. No paper
     measures it; the one precedent is Iterative RPO on GSM8K
     (`DPO_RESEARCH.md`, section 2.9). The count of item 8 says how many
     questions it touches;
   - nearest-correct pairing and the rejected side counted on the
     differing tokens. Neither has been tested on SQL in a paper
     (`DPO_RESEARCH.md`, section 2.4).

## 5. Results

Spider test EX, 2,147 rows, greedy. Details in `LAB_LOG.md`.

| Row | Prompt | EX | Easy | Medium | Hard | Extra |
|---|---|---:|---:|---:|---:|---:|
| Student without training | A, `ddl_rows` | 68.05 | 87.4 | 71.4 | 59.2 | 45.9 |
| Student without training | B, `ddl_values` | 67.49 | 87.7 | 71.2 | 56.4 | 46.5 |

The two prompts do not differ (exact McNemar p = 0.47). No trained row
yet.

## 6. Earlier work

Everything measured before 2026-11-17 is reference only: it was produced
with a prompt that carried a sentence left from an earlier ICL project, and
most of it with a repetition penalty of 1.1 that nobody had set. Both
repositories as they were are at the tag `archive/pre-reset-2026-11-17`
and, on the owner's Mac, in `archive/reset_2026-11-17/` (start at its
`OVERVIEW.md`). A number from there is quoted as "earlier setup" and never
as a result.
