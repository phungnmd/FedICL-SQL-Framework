# FedLS-SQL: research state

Updated 2026-11-22; where the method stands is in section 5.0. On
2026-11-17 the owner set the project up again from clean: a new prompt,
refactored code (package `fedls_sql`) and every result produced again.
This file says what is fixed, what the method is and what is open. Runs
and decisions are in `LAB_LOG.md`.

## 1. Question

Several organisations each hold databases and questions with gold SQL that
cannot leave them. They train a small model together through federated
learning, and only that model is deployed. Standard federated training
(FedAvg SFT) uses the gold SQL and never the databases.

Main question: does training on the execution of the model's own SQL on
the clients' databases give a better model than FedAvg SFT, and than
federated DPO as published (pairs made once, reference fixed), on the same
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
| Other student models (owner, 2026-11-22) | Qwen2.5-Coder-0.5B-Instruct and deepseek-coder-1.3b-instruct run the Spider line of the 1.5B with the model changed and nothing else (FedAvg SFT rounds 1 to 4, DPO + NLL rounds 1 and 2 from FedAvg SFT round 2), each through its own chat template | queued 2026-11-22, nothing read |
| Clients | 5 clients on Spider train (8,659 rows, 146 databases), split `federated/alpha_0.1/k5` (split seed 42): every database whole at one client, Dirichlet (alpha 0.1) over four complexity tiers of the databases; private rows never leave a client. A second set since 2026-11-19: 5 clients on BIRD train with evidence (9,428 rows), split `federated/alpha_0.1/k5`, read on BIRD dev | built 2026-11-17 after `FEDERATED_DATA_SETUP.md`; whether it poses a problem is open, section 4 |
| Teacher | Qwen2.5-Coder-7B-Instruct, frozen, at the server, on public data only | not part of the method (owner, 2026-11-17); a research direction, section 4 |
| Public data | BIRD train with evidence (9,428 rows); SynSQL-2.5M may replace or join it | fixed |
| Decoding | greedy, no repetition penalty (the code sets 1.0 and never reads the model's generation config) | fixed |
| Metric | Spider test EX (2,147 rows) through vLLM; BIRD dev EX (1,534 rows) for the BIRD clients. Rounds, steps and settings may be chosen on Spider test (owner, 2026-11-17); the lab log records what was chosen on which set, and the paper does not call such a number held-out | fixed |
| Prompt | the Text-to-SQL prompt of the Qwen2.5-Coder evaluation code (schema text, a line naming SQLite, the question, a request for the SQL only), one for training, sampling and evaluation | layout fixed; schema text open between `ddl_rows` and `ddl_values`, section 4 |
| Length | `--max-len 7168`, no truncation (a longer row stops the run); 256 new tokens | fixed |
| Training recipe of the SFT baselines | LoRA SFT at lr 2e-4, FedAvg rounds of 1 local epoch, as many as the gain rule allows (more than 0.5 EX point over the best round, patience 2, at most 4 since 2026-11-18); the recipe of SPFT-SQL for this student is lr 2e-4, 3 epochs | run on Spider (FedAvg SFT 4 rounds, centralized SFT 3 epochs); on BIRD 2 rounds read, rounds 3 and 4 queued |
| Compute | RTX A5000 24 GB under WDDM, two cards; one card available from the evening of 2026-11-21 (owner) | fixed |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation,
not differential privacy.

## 3. Method

Direction (owner, 2026-11-17, revised the same day): a federated learning
method for Text-to-SQL that uses DPO with execution labels at the
clients, built to beat the federated baselines. It is the owner's own
design, not CodeLutra applied to federated learning. CodeLutra, found
later, runs a similar loop centrally; the paper cites it as the closest
work and says what differs (3.6), and the settings taken from it are said
to follow it. What has run is in section 5.0; the parts of 3.3 are
candidates, each kept only on a measured gain.

| Part | Where | Supervision | Place |
|---|---|---|---|
| Federated DPO + NLL with the improvements of 3.3 | clients | execution of the model's own SQL on the client's databases | the core |
| Pre-training with the same loss | server | execution of the model's own SQL on public data that has gold SQL | secondary; in the method if the results support it |

Whether a FedAvg SFT stage comes before the DPO rounds is now a candidate
improvement (3.3), not ruled out. The teacher is not part of the method;
what it could add is a research direction (section 4).

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
   Federated DPO as published makes its pairs once and keeps one reference
   for all rounds.
6. What execution tells differs by client. An execution error says only
   that the SQL does not run; a wrong result says that it means something
   else; a gold result that is empty, or a database without rows, cannot
   tell a right SQL from a wrong one that runs. The share of such
   questions differs across clients (1% to 41% here), and only the client
   can see it, because the databases stay with it. The pairs use each
   label at the level it informs.
7. Cost. No extra data and no extra communication (the same adapter is
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
| The federated design matters | the method above federated DPO as published (fixed pairs, fixed reference) and above the plain federated loop (ablation rows of 3.4) |
| The gain comes from correcting the model's own errors | the gain grows over the rounds and sits in the hard and extra columns; the count of executable SQL with a wrong result falls, not only the count of execution errors |
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

The plain form of the round (plain loss, pairs drawn at random, nothing
from a question whose samples are all wrong or all correct) is the
starting point the parts of 3.3 are measured against; its settings follow
CodeLutra. The method uses the clients' labelled questions only;
unlabelled questions are not part of it.

### 3.3 Candidate parts (owner, 2026-11-17)

Each is a run against the plain form from the same start and for the same
rounds, and joins the method only on a clear gain. The paper keeps the
ones that carry the story; one main improvement with a clear story is
better than a stack of small ones.

| # | Improvement | Problem it answers | Evidence so far | Ablation row |
|---|---|---|---|---|
| I1 | On-policy rounds: each round samples from the new global model, which is also the DPO reference | federated DPO as published trains on pairs made once against a fixed reference | earlier setup (reference only): fresh samples above fixed round-1 pairs by 1.72 EX at round 3 (p = 0.0049) | pairs fixed from round 1, reference fixed |
| I2 | Execution-aware pairs (main candidate): a wrong-result sample is paired with its nearest correct sample, an execution-error sample with any correct one; optionally the rejected side counted only on the tokens that differ | random pairs teach mostly that SQL should run; labels on empty results say nothing about meaning, and their share differs by client | pair read (2026-11-17): gold result empty for 1% to 5% of the questions at clients 1, 2, 3, 5 and 41% at client 4, from seven Spider databases without rows; earlier setup (reference only): DPO cut execution errors 211 to 58 while about 440 executable wrong-result rows on Spider test did not move | random pairs (plain form) |
| I3 | A FedAvg SFT stage of k rounds before the DPO rounds (owner, 2026-11-17): the method is k SFT rounds, then DPO + NLL rounds, k stated as a value; k is swept (0, 2, the best FedAvg round) | from the base student the all-wrong questions (12% here) and the questions on databases without rows (20%) give no useful pair, while gold SQL teaches them; the longer the SFT stage, the more training questions the student gets right in all 10 samples, so the fewer pairs are left (expected, not measured) | earlier setup (reference only): every DPO run there started after FedAvg SFT, +3.87 EX over FedAvg round 3 (pooled +3.91, interval +2.82 to +5.01), +2.3 to +2.75 without the repetition penalty; more SFT rounds instead gave +0.84 and then fell. Against it in the papers: SFT then plain DPO gives about zero (`DPO_RESEARCH.md`, 2.1), with an offline loss and no NLL term | k = 0 (DPO rounds from the base student); the control for the same total rounds is the FedAvg SFT line itself, continued |

Measured since (section 5.0, one seed): I1 is kept on BIRD (on-policy
rounds 2.21 above fixed pairs, p 0.008) and makes no difference on Spider
test. I2 (nearest pairs, wrong-result rejects first) gave no gain on
Spider and was not run on BIRD. I3: on Spider no difference on test EX,
and on test-suite accuracy k = 2 is above k = 0 and above FedAvg SFT on
dev, Syn and Realistic (read on the Mac, not committed); on BIRD k = 1 is
1.24 above k = 0 (p 0.19). The proposal of 2026-11-21 is to keep the SFT
stage in the method with k = 0 as an ablation row (not decided).

Smaller choices, not improvements of their own: FedAvg weights by pair
count (pairs per client run from 5,110 to 26,290 at 10 per question), and
the gold SQL of an all-wrong question in the NLL term (never as the
chosen side), which I3 would make unneeded. Run on BIRD (2026-11-21,
`bird_k0_goldnll/round_2`): 42.37 against 43.02 without it, not kept
(section 4, item 12b).

Settings for every DPO line (owner, 2026-11-17): 2 pairs per question
(10, as in CodeLutra, gives 59,510 pairs a round here, about 13-15 h of
training, estimate). A question on a database whose tables hold no rows
gives no pair; a question whose gold result is empty on a database with
rows keeps its pairs (owner: drop the empty databases only). The code
does this by default (`9dd4adce`).

### 3.4 Rows of the paper (plan)

| Row | What it is | Role |
|---|---|---|
| FedAvg SFT | gold SQL, FedAvg | federated baseline; run (Spider 4 rounds, BIRD 3, round 4 queued) |
| FedProx, FedNTD | gold SQL, other aggregators | federated baselines (item 6 of section 4) |
| Federated DPO as published | pairs from the base student's samples made once, reference fixed for all rounds (OpenFedLLM's FedDPO); same loss, same pair count | federated DPO baseline |
| Method | DPO + NLL rounds with the improvements kept | the row of the paper |
| Ablations | the method without each kept improvement | show what each adds |
| Centralized SFT, local SFT | the union of the clients; each client alone | upper and lower reference |

Columns: EX, easy, medium, hard, extra, execution errors, executable SQL
with a wrong result. Run so far: section 5.0. Not run: FedProx, FedNTD
and local SFT; the row of federated DPO as published past its first
round is open for the owner (`PIPELINE_NEXT.md`).

### 3.5 Pre-training at the server

The secondary part runs the same loop once at the server, before the
rounds, on public data. It gives the student the output format and general
SQL skill without using up the pairs on the clients' questions, which the
student has not seen.

### 3.6 Closest work

CodeLutra (arXiv 2411.05199): the closest work, a similar loop run
centrally at 8B, found after the method was designed. It starts from the base model with no SFT stage (its SFT
model is a separate baseline), draws 10 samples at T 1.0, draws 10 random
pairs per question from the model's own correct and wrong samples, and
trains DPO + SFT with beta 0.1 and lambda 1.0, LoRA r 8, lr 5e-5, one epoch
per iteration, 4 iterations. It does not mention empty gold results or
databases without rows and filters no training question. Different here:
a federated method (clients label by execution on their own databases, a
round is a re-sampling step, the reference is the round's global model),
at 1.5B, with the parts of 3.3. OpenFedLLM (arXiv
2402.06954) runs DPO inside FedAvg with fixed pairs and a reference fixed
for all rounds. The papers behind each choice are in `DPO_RESEARCH.md`;
the rest of the map is in `LITERATURE.md`.


### 3.7 Experiment plan (owner, 2026-11-17)

Phases in order; each ends with a rule that says whether to go on. Times
are GPU wall clock on one card (estimates).

| Phase | Runs | Decides |
|---|---|---|
| 0, no GPU | (a) the pairs of the base student's round 1 samples counted by rejected outcome (execution error, wrong result) per client, with the empty databases (`scripts/pair_composition.py`); (b) the wrong rows of each FedAvg round split into execution errors and wrong results by hardness (`scripts/error_breakdown.py`); (c) code for phase 1 | whether I2 is worth a run; how much DPO can still fix after SFT |
| 1, about 1 day | FedAvg SFT (running) until its rule stops it. Early read of the switch round: one DPO + NLL round from FedAvg round 2 (k = 2), against FedAvg round 3, with the pair counts per client at that start (queued first, `46509f1e`). Then DPO + NLL rounds from the best FedAvg round (k = best). Every DPO line: 10 samples at T 1.0, 2 random pairs per question, no pair from a database without rows, rule 0.5 / patience 2 / at most 6 rounds; control: the FedAvg line at the same total rounds | k = 2 at least 1 EX above FedAvg round 3: the line from k = 2 continues and k becomes an axis of the paper (EX and pairs against k); about 0: read the pair counts before the long line (start earlier, more pairs per question, or gold as the chosen side of all-wrong questions); below: stop and look. The story: a gain of 1.5 EX or more with exact McNemar p < 0.05 at the same total rounds goes on to phase 2 |
| 2, about 2-3 days | from the same start and for the same rounds: federated DPO as published (pairs fixed from round 1, reference fixed), RFT (NLL on correct samples only), DPO + NLL from the base student (k = 0), I2 if (a) shows wrong-result pairs are scarce; client drift of SFT and DPO updates and pairs per client by round, from the saved adapters | the main table and the ablations |
| 3, about 4-6 days | BIRD as a second set of clients; alpha 0.5 and IID for FedAvg and the method; FedProx and FedNTD; centralized and local SFT; a second seed of the main rows; the server pre-training last | breadth for a Q2 journal, a chance at Q1 |

Not in the plan now: the teacher, unlabelled questions, 10 pairs per
question. A switch rule computed by the clients (switch when the share
of mixed questions or the SFT gain falls) only if the best k differs
between setups. Rounds are chosen on
Spider test, as the setup allows.

### 3.8 Aggregation of the DPO rounds: options to test (owner, 2026-11-17)

Default, unchanged for phase 1: FedAvg of the LoRA factors (A and B
averaged separately), each client weighted by its pair count; FedAvg SFT
uses the same averaging weighted by question count. With 2 pairs per
mixed question the weight follows the questions a client still gets
wrong, so a client whose errors are fixed fades from the average (the
idea behind Lorar, Zhang et al. 2023).

Options, each tried only if the numbers below point to it:

| Option | Problem it answers | When to try |
|---|---|---|
| Equal weights per client | a large client dominates under non-IID data | the re-aggregation probe below shows a gain |
| Weights by question count | as FedAvg SFT | probe only; it gives weight to clients with nothing left to teach |
| FedNova-style normalisation (Wang et al., NeurIPS 2020): each update divided by its number of local steps | local steps follow the pair count, which differs about 5 times across clients, so FedAvg drifts toward the clients with more steps | client updates diverge (cosine, norms) or the probe shows a gain |
| Exact LoRA aggregation: A frozen and only B averaged (FFA-LoRA; the code has `restore_frozen_lora_a`), or FedEx-LoRA / FLoRA | the average of the factors is not the average of the products B A | `overall_relative_product_error` of the round records is large |
| FedProx in the DPO rounds | client drift | likely redundant: the DPO term already keeps each client near its reference, the round's global model; kept as an SFT baseline |
| Server optimisers (FedAdam, FedYogi), SCAFFOLD | slow convergence, drift | not planned: few rounds; SCAFFOLD doubles the state |

Read from every DPO round (already logged): the weight of each client,
`overall_relative_product_error`, and the cosine and norms of the client
updates (`delta_stats`). Probe without training (needs a small script):
the five client adapters of DPO round 1 re-aggregated with pair, equal,
question and step-normalised weights into a new directory, each evaluated
on Spider test (about 10 min each, estimate). Differences under about one
point are noise and keep the default; a clear difference earns a full
line in phase 2.

A point for the paper whatever the option: with the round's global model
as reference, DPO is a trust region around the shared model, so its
client updates may drift less than SFT updates under non-IID data. The
cosine of client updates in SFT and DPO rounds measures it (phase 2).

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
   the decoding. The runs on Spider use A (2026-11-17); B is run again
   only if a result asks for it.
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
6. Baselines with the new prompt: FedAvg (run), FedProx, FedNTD,
   federated DPO as published (section 3.4), centralized and local SFT.
7. The client split. In `alpha_0.1/k5` the share of hard and extra
   questions runs from 20% to 60% across the clients, and the clients
   hold 734 to 3,479 questions (table in `LAB_LOG.md`, 2026-11-17). No
   client lacks a hardness level: the client of the simplest tier still
   has 20% hard or extra questions. Whether the split gives a reason to
   federate is read from three rows: local training per client, FedAvg,
   centralized. If the local model of the simple client is not below
   FedAvg on the hard and extra columns, the split is too mild.
8. Whether the clients' questions give enough pairs. From the base
   student (results `1704b03b`): of 8,659 questions 5,951 are mixed, 1,631
   all correct, 1,074 all wrong; 1,616 have an empty gold result, 1,433 of
   them at client 4, from seven Spider databases without rows (table in
   `LAB_LOG.md`). Still to read: how the rejected samples of the pairs
   split between execution errors and wrong results, per client (from the
   round 1 samples on the server, no GPU), which grounds I2; and the same
   read after the server pre-training.
9. The candidate improvements of section 3.3 (I1 to I3), each as a run
   against the plain loop. Nearest-correct pairing and the rejected side
   counted on the differing tokens have not been tested on SQL in a paper
   (`DPO_RESEARCH.md`, section 2.4); gold SQL in the NLL term has one
   precedent, Iterative RPO on GSM8K (section 2.9). Code needed before the
   runs: the pair rule of I2 and a fixed reference for the published
   federated DPO baseline (fixed samples exist, `samples_from_round`).
10. BIRD as a second set of clients. The method is tried on Spider first
    (owner, 2026-11-17). On Spider about 4 points are left above the SFT
    of this student in the papers (77 to 78, highest published 82.3; 78.0
    and 82.3 are SPFT-SQL's, not used as a reference since 2026-11-20,
    section 5.1); on
    BIRD CodeLutra is 7.5 points above its SFT. Decided after the first
    read of the DPO rounds against FedAvg SFT on Spider. Needed for it: a
    client split of BIRD train by database, the prompt lengths on BIRD,
    and Spider train as the public data in that setting.
11. Content generated by the clients for their databases (recorded
    2026-11-19; owner: optional, taken up later if wanted; if it is
    tried, before the runs over seeds and alphas). The DPO rounds
    remove execution errors and leave the wrong results where they were
    (FedAvg round 4: 173 errors and 370 wrong results; DPO round 2: 84 and
    384). Two properties of the training databases weaken the labels where
    those errors sit: seven databases have no rows (1,759 questions, none
    gives a pair), and the others are small, so a wrong SQL often returns
    the gold result. The direction: each client fills its empty databases
    and then builds a few content variants of every database (rows in
    foreign-key order, seeded with the literals of its own gold SQL, added
    until the gold SQL returns a result); a sample is correct only if it
    matches gold on every variant. It continues point 6 of the story
    (3.1): the label is fixed, where I2 changed the pairing. Steps and
    stop rules are in `LAB_LOG.md` (2026-11-19), the papers in
    `LITERATURE.md`, section 1.21. Closest work: test suites for
    evaluation (Zhong et al. 2020), and SQLoom, CoRE-DB and ReViSQL, which
    train centrally with counterexample or enriched databases (section
    1.20). The boundary-value form of the idea was dropped on 2026-11-18;
    this form rests on the empty databases and on general content
    variants, which that probe did not measure.
12. Extensions toward a Q2 journal (recorded 2026-11-20; owner: tried
    after the method is settled on BIRD, in this order). One extension
    of the method at most, (b) or (c), not both.

    | # | Direction | What it would show | Evidence so far | First step | Cost (estimate) |
    |---|---|---|---|---|---|
    | a | A finding on federation: centralized DPO + NLL (the same loop on the union of the clients) next to the federated method, with the gap between federated and centralized for SFT and for DPO, and the drift of the client updates | whether the execution-preference objective keeps the centralized level under non-IID data where SFT does not; centralized SFT is no longer the upper reference (epochs 1-3: 75.08, 75.73, 75.03; method 75.87, 77.18, 77.69) | FedAvg SFT against centralized SFT at the same count: -2.65, -1.63 (p 0.030), -0.32 (p 0.69) at 1, 2, 3, so SFT is slower under this split, not lower; the method at 3 rounds is 2.66 above centralized SFT epoch 3 (p 0.0015); pairwise cosine of client updates 0.24-0.46 in DPO round 1, about 0 in FedAvg SFT rounds 2-3 (0.013-0.055 in DPO round 2) | centralized DPO + NLL on Spider, 4 iterations | 8.5 h on Spider, about 20 h on BIRD |
    | b | Each question trained on the signal it has, in one local loss: DPO + NLL on the mixed questions, NLL on the gold SQL for the all-wrong ones, nothing for the all-correct ones | a part of the method that differs from CodeLutra (which drops those questions) and stays in the story: execution where the model already has a correct SQL, gold where it has none | read 2026-11-21, not kept: `bird_k0_goldnll/round_2` is 42.37 on BIRD dev, 0.65 below `bird_k0/round_2` on the same pairs (p 0.43) and 1.89 below `bird_k1/round_1` (p 0.045); the challenging level comes part of the way back (24.14 against 19.31, p 0.039; FedAvg SFT 29.66), the simple and moderate ones fall, and from the shared parent the round breaks 81 answers against 67 without the gold rows. Not run on Spider. Gold as the chosen side is not this (no preference term on the gold here). All-wrong questions: Spider 1,074, 902, 886, 860 over rounds 1-4, BIRD 4,035 of 9,428 (round 1 from the base student). Gold as the chosen side on BIRD at 1 round: 39.24 against 41.85 without it, p 0.007 | run 2026-11-21 (owner: yes): `bird_k0_goldnll/round_2`, round 2 of `bird_k0` on its own pairs plus one NLL row per all-wrong question (`--gold-nll`, code `38610a58`), against `bird_k0/round_2` 43.02, overall and by BIRD difficulty | 4 h 52 min of training (measured) |
    | c | Questions without gold SQL, labelled by the vote over the execution results of the model's own samples; a secondary experiment, not a part of the method (owner, 2026-11-20: hiding gold is an assumption the datasets do not make; 2026-11-21: skipped, a client without gold SQL would have no questions either) | whether the execution signal still helps when labels are scarce: EX against the share of questions that keep their gold, for FedAvg SFT, the method on the labelled questions, and the method with vote labels | none of ours. CodeLutra without gold (executable against non-executable): BIRD 22.3 to 30.9 against 43.1 with gold; ScPO on GSM8K 63.91 without labels against 64.29 (`DPO_RESEARCH.md`, 2.5) | CPU only, on the Spider round 1 samples on the server: per client, the share of questions whose most voted execution result equals the gold result (script not written). A low share drops the direction | a few minutes for the probe; then 8.5 h per setting on Spider and an SFT baseline with pseudo-labels, without which FedAvg SFT loses by construction |

    | d | A hint for the questions no sample solves (proposed 2026-11-21, not approved; the owner sees it as the part with the highest value for the method if it works): the client samples those questions again with a line that names the tables and columns of its own gold SQL; a sample whose result equals the gold result becomes the chosen side, under the prompt without the hint; nothing changes at test time | a part of the method that is not in CodeLutra, aimed at the errors neither SFT nor DPO removes | for: 68% to 75% of the wrong results on Spider test and BIRD dev differ from gold in tables or columns (chat analysis, not committed); 32% of the BIRD questions give no pair in round 2. Against: gold as the chosen side for the same questions is 2.61 below on BIRD (p 0.007); one DPO + NLL round already takes 25% of them out of all wrong by itself. Probe and control (2026-11-21): with the hint 32.6% of the 3,017 questions hold a correct sample (8.9% of the correct samples equal the gold SQL); on clients 1, 3 and 4, 31.7% with the hint and 10.4% in a second draw without it, so the hint adds 21.4 points (interval 19.0 to 23.7), under the 25 of the first step, and 65% have none in either draw. NLL rows on the gold SQL of the same questions (12b) were not kept and moved the challenging level by 7 questions net; with an SFT stage that level is already 28.28 against 29.66 for FedAvg SFT. No round with hinted pairs is written; it needs the owner's yes to a second sampling prompt | a probe without training: the 3,017 all-wrong questions of `bird_k0/round_2`, sampled from the round 1 adapter with the hint and labelled; the direction is dropped under 25% of them with a correct sample | 30 min for the probe, then about 4 h for one round against `bird_k0/round_2` (43.02) |

    Also read in the same pass, without training: the five client
    adapters of a DPO round aggregated again with pair, equal, question
    and step-normalised weights (section 3.8; 10 min of evaluation each).
    Not for this paper: content generated by the clients (item 11).

## 5. Results

Spider test EX, 2,147 rows, greedy. Details in `LAB_LOG.md`.

| Row | Prompt | EX | Easy | Medium | Hard | Extra |
|---|---|---:|---:|---:|---:|---:|
| Student without training | A, `ddl_rows` | 68.05 | 87.4 | 71.4 | 59.2 | 45.9 |
| Student without training | B, `ddl_values` | 67.49 | 87.7 | 71.2 | 56.4 | 46.5 |
| FedAvg SFT, round 1 | A, `ddl_rows` | 72.43 | 89.2 | 75.3 | 63.7 | 54.9 |

The two prompts do not differ (exact McNemar p = 0.47). FedAvg SFT round 1
(results `d6bfc763`) is above the untrained student with prompt A: 165 rows
fixed, 71 broken, exact McNemar p = 8.5e-10.

### 5.0 Where the method stands (2026-11-22, one seed)

EX by total rounds; every row is in `LAB_LOG.md` with its result commit.

| Rounds | Spider test, FedAvg SFT | Spider test, DPO + NLL from the base student (k = 0) | Spider test, 2 SFT rounds then DPO (k = 2) | BIRD dev, FedAvg SFT | BIRD dev, k = 0 | BIRD dev, 1 SFT round then DPO (k = 1) | BIRD dev, 2 SFT rounds then DPO (k = 2) |
|---|---|---|---|---|---|---|---|
| 1 | 72.43 | 75.87 | | 38.85 | 41.85 | | |
| 2 | 74.10 | 77.18 | | 42.70 | 43.02 | 44.26 | |
| 3 | 74.71 | 77.69 | 77.46 | 43.68 | | | 46.22 |
| 4 | 74.71 | 78.02 | 78.20 | | | | |

- Spider: the method is 3.3 to 3.5 above FedAvg SFT at 4 rounds on
  Spider test (k = 2: 78.20), and 2.12 (k = 0, p 0.08) and 2.51 (k = 2,
  p 0.02) above on Spider dev, where no round or setting was chosen.
- BIRD: with two SFT rounds first (k = 2, the k of the best Spider
  line, set before the read) the method is 2.54 above FedAvg SFT at 3
  rounds (46.22 against 43.68, 125 questions against 86, p 0.0087) and
  above it on every difficulty level (53.08 / 36.85 / 32.41 against
  51.57 / 32.54 / 28.97). It is 1.96 above k = 1 at 2 rounds (p 0.031).
  From the base start: +3.00 at 1 round (p 0.005), +0.32 at 2 rounds (p
  0.80); with one SFT round first +1.56 at 2 rounds (p 0.13). k = 2
  stands on both datasets.
- Gold SQL on BIRD: as an SFT stage before the DPO rounds it is on the
  method's side (k = 1 is 1.24 above k = 0, p 0.19); inside a DPO round
  it has not helped in either form tried (chosen side of a pair -2.61,
  NLL rows for the all-wrong questions -0.65), and k = 1 is 1.89 above
  the round with the NLL rows (p 0.045).
- The DPO rounds add about the same on both sets: the first about +3
  over an SFT round from the same start (+3.44, +3.00), the second +1.31
  and +1.17. The SFT rounds differ: the second adds 1.67 on Spider and
  3.85 on BIRD, the third 0.61 on Spider and 0.98 on BIRD (p 0.11).
  FedAvg SFT slows on BIRD at round 3 as it did on Spider; round 4 is
  queued.
- One DPO round after SFT adds 3.36 on Spider (from round 2) and, on
  BIRD, 5.41 from round 1 and 3.52 from round 2 (`bird_k2/round_1`),
  where a third SFT round adds 0.98. Still to read on BIRD: the method
  at 4 rounds (`bird_k2/round_2` against `bird_sft` round 4) and its
  twin on fixed pairs; neither is queued.
- The DPO rounds remove execution errors and leave the wrong results;
  SFT does the reverse (BIRD at 2 rounds: 285 and 593 for FedAvg SFT,
  120 and 727 for k = 1; at 3 rounds, with timeouts counted as errors:
  276 and 588 for FedAvg SFT, 102 and 723 for k = 2).
- Where the gain sits (session read of the committed predictions,
  `LAB_LOG.md`, 2026-11-22): at 3 rounds k = 2 and FedAvg SFT have as
  many predictions on the gold's tables and columns (718 and 715) and
  the same EX on them (74.5 and 74.8); the method is ahead on the
  others (21.3 against 16.5), right answers written with other tables
  or columns than the gold's.

| Part | Spider | BIRD |
|---|---|---|
| On-policy rounds against fixed pairs | test 78.20 against 78.02; dev +1.45 (p 0.07) | +2.21 (p 0.008), kept |
| FedAvg SFT stage | test EX: no difference (k = 0, 2, 3: 78.02, 78.20, 77.97); test-suite accuracy on dev, Syn, Realistic: k = 2 above k = 0 (p 0.010, 0.0014, 0.0067) and above FedAvg SFT, k = 0 level with FedAvg SFT (`LAB_LOG.md`, 2026-11-21; not committed) | k = 1 is 1.24 above k = 0 at 2 rounds (p 0.19); k = 2 at 3 rounds is 3.19 above k = 0 at 2 rounds (p 0.0025) and 1.96 above k = 1 at 2 rounds (p 0.031), rows of unequal length |
| Gold as the chosen side | falls at round 2 | -2.61 (p 0.007) |
| NLL rows on the gold SQL of the all-wrong questions, in the round of the pairs | not run | -0.65 (p 0.43), not kept; 1.89 below k = 1 (p 0.045) |
| Nearest pairs, wrong-result rejects first | no gain | not run |

### 5.1 Published numbers for this student (reference, read 2026-11-20)

Qwen2.5-Coder-1.5B in other papers, next to ours, EX. Sources, settings
and what was not read: `LITERATURE.md`, section 1.4. No paper states a
plain-DDL prompt, greedy decoding, one sample and LoRA together, so these
rows place our numbers; they are not the same setup. Ours: Spider test
and BIRD dev, greedy.

| Set | Row | Ours | Published |
|---|---|---|---|
| Spider | without training | 68.05 (test) | SQL-Factory 69.2 (split not named); SLM-SQL test 67.61 (vote of 16) |
| Spider | SFT on Spider train | centralized 75.08, 75.73, 75.03 (epochs 1-3); FedAvg 74.71 (4 rounds) | SQL-Factory 73.2 (3 epochs, split not named) |
| Spider | best with a method | ours 78.02 (k = 0, 4 rounds), 78.20 (k = 2) | SQL-Factory 76.5 (synthetic data); SLM-SQL test 79.06 (916K rows, vote of 16) |
| Spider-Syn / Realistic / DK | without training; SFT; method | queued (`spider_variants`) | CodeS-1B SFT: 66.5 / 70.9 / 64.7 (another base model, value retrieval, beam) |
| BIRD dev | without training | 29.47 | Think2SQL 27.5; SLM-SQL 28.40; SQL-Factory 28.6 |
| BIRD dev | SFT on BIRD train | FedAvg 38.85, 42.70, 43.68 (rounds 1 to 3) | SQL-Factory 39.2 (3 epochs) |
| BIRD dev | with a method, added inputs or voting | 46.22 (2 FedAvg SFT rounds, then 1 DPO + NLL round; 3 rounds in all) | Think2SQL RL 44.2 (gold tables); CodeS-1B 50.46 (value retrieval, beam); SLM-SQL 54.17 SFT with a vote of 64, 67.08 full; FINER-SQL 59.4 SFT, 63.17 full (schema ranker, vote of 30) |

SPFT-SQL (arXiv 2509.03937) is not used as a reference (owner,
2026-11-20). Its row for this student without training is 40.6 on BIRD
dev, 11 to 13 points above the three other papers and ours, and 72.3 on
Spider test against 68.05 here; the paper prints no prompt and no
decoding, so its SFT rows (BIRD 44.3, Spider test 78.0) and its method
rows (54.0, 82.3) stand on an input we cannot name. Its SFT adds 3.7 on
BIRD, against 10.6 in SQL-Factory and 13.2 for our two FedAvg rounds.
The numbers stay in `LITERATURE.md`, section 1.4, as what the paper
prints. With it out, one plain-SFT row per dataset is left
(SQL-Factory), with its split, prompt and decoding not stated.

Federated: no result on BIRD and no federated Text-to-SQL paper besides
Zhang et al. (ACL 2023; T5-base, exact match: centralized 70.32, FedAvg
40.03, FedOPT 58.32, macro average over 8 clients).

## 6. Earlier work

Everything measured before 2026-11-17 is reference only: it was produced
with a prompt that carried a sentence left from an earlier ICL project, and
most of it with a repetition penalty of 1.1 that nobody had set. Both
repositories as they were are at the tag `archive/pre-reset-2026-11-17`
and, on the owner's Mac, in `archive/reset_2026-11-17/` (start at its
`OVERVIEW.md`). A number from there is quoted as "earlier setup" and never
as a result.
