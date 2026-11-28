# Paper outline

Approved by the owner on 2026-11-26 and restructured on 2026-11-27
(owner): seven sections, no research questions, the ablation study
inside the results section, a figure in the introduction and a short
subsection on the supervision that execution gives before the framework.
Claim numbers (A1 to E2) are those of `CLAIMS.md`. A section is written
from its entry here. The bibliography keys come from `bib/report.md`,
which names the sources of each subsection.

## Structure

Seven sections. The results section has subsections named by their
content, and the ablation study and the cost are two of them: the
federated papers of the target journal that were read (LESFT, FedCO,
FedCCM) have six sections, keep the ablation inside the experiments,
give the cost a subsection or a table of its own, and use no research
questions; none of the nine federated papers read does. The setup keeps
a section of its own because it holds two datasets, six baselines and
the statistical protocol.

The order inside Section 5 follows the argument: the gain (5.1), which
predictions change (5.2), which component accounts for it (5.3), then
breadth (5.4, which holds the other models, the federated setups and the
perturbed questions) and cost (5.5) (owner, 2026-11-28).

Length (owner, 2026-11-28): about 20 pages; the fee of the journal
covers 15. The paper was cut from 32 to 21 pages on that day: the body
has about 6,000 words, and the subsections below are merged where the
text merges them (3.1 with 3.2, 3.3 with 3.4, 3.5 with 3.6; 4.3 with
4.4; 5.4 with 5.5). The word counts in the headings are those of the
text after the cut. What a reader needs only to reproduce is in the
Supplementary Materials (`supplement.tex`, built by `make` into
`build/supplement.pdf`): S1 the prompt, S2 the settings and software,
S3 the federated setups and the partition procedure (Table S3), S4
execution labeling and the time limits, S5 EX by round (Table S4), S6
the generated suite of BIRD dev, TS on BIRD dev for the rows of the
ablation (Table S5) and the correct predictions on other tables or
columns (S6.4, Table S6) (owner, 2026-11-28), S7 the labels at each
client (Table S7) (owner, 2026-11-28). The revision of
2026-11-28 (owner) brought the paper to what CMC publishes: rows that
the journal's papers do not carry left the tables (FedProx SFT, the
second seed, local SFT on Spider, DeepSeek-Coder on BIRD, the variants
of the server average and of pooling, the row without the NLL term at
4 rounds), the tables print the test of every main claim, and the
generated suite moved to the Supplementary Materials. Where an entry below names
Appendix A or B, or a float that moved, read the section of the
Supplementary Materials that holds it.

## Overview

The paper starts from one observation: a client in federated
Text-to-SQL holds databases as well as questions with gold SQL, and
federated fine-tuning uses only the second. The introduction states the
gap and the method in brief, and Fig. 1 shows the two ways of training
on one question. Related work places the method against fine-tuned
models for Text-to-SQL, preference optimization with execution
feedback, and federated fine-tuning, including federated preference
optimization, federated reinforcement learning with verifiable rewards
and federated semantic parsing. The method section defines the setting,
measures how often execution gives a signal the gold SQL does not, and
describes the framework by component. The setup section fixes data,
models, baselines and tests. The results section gives the gain over
the baselines, what changes in the predictions, the ablation study, the
breadth over models, federated setups and perturbed questions, and the
cost. The discussion interprets the two kinds of round and states the
limits of the study.

## Detailed Outline

### Front matter

- Title (owner, 2026-11-27): "FedExec-SQL: A Federated Learning Framework for Text-to-SQL with Preference Optimization from Client-Side Execution".
  The name, the mechanism, the task and the setting. No "SLM"
  and no "small" in it: the contribution is the supervision, not the
  size of the model.
- Abstract (CMC): 200 to 400 words, one paragraph, no citation, ending
  with the main numbers; the headline number is the gain on BIRD dev.
  The model is named a small language model once, with its size.
- Keywords (CMC): 3 to 10, "small language models" among them.

### 1. Introduction (~730 words, Fig. 1)

**Purpose**: state the problem, the gap, the idea and what the paper
shows.
**Content** (paragraphs, no subsections):

- From the field to the setting (owner, 2026-11-27: the paper names
  the small language model). Text-to-SQL systems built on proprietary
  LLMs send questions and schemas to a provider; a small language model
  (SLM, 0.5B to 1.5B parameters) is what an organisation can fine-tune
  and serve on its own hardware, and in this method a client also
  samples and executes queries with it. One organisation holds few
  databases, and the questions and databases of several organisations
  cannot be pooled: hence federated training of one SLM. "Federated
  Text-to-SQL" here means federated training of the model, said once.
  The SLM is the reason for the setting and the scope of the
  experiments; the paper does not present itself as an SLM Text-to-SQL
  system.
- The gap. FedAvg SFT learns from the one gold SQL of each question and
  never executes a query on the databases. FedDPO, the federated preference
  optimization of OpenFedLLM, trains each client on a fixed preference
  dataset whose two sides are responses of that dataset, not outputs of
  the model under training, and keeps one reference model. Whether a
  query returns the gold result can be established only where the
  database is.
- The idea: execution turns the one gold SQL of a question into many
  correct and incorrect queries of the model's own. The method in three
  sentences: warm-up rounds, preference rounds, what leaves a client.
- Fig. 1: one question trained in the two ways. FedAvg SFT: the gold
  SQL is the only target and the database is not used. FedExec-SQL: the
  model's sampled queries are executed on the client's database and
  labelled against the result of the gold SQL. The figure carries the
  example; the text does not repeat it.
- Headline results: A1 (the gain on BIRD dev and Spider test), A2 (more
  FedAvg SFT rounds do not reach it), C1 (execution errors halve).
- Contributions, four, as in `CLAIMS.md`, section 2.

**Transition to next**: the lines of work the idea draws on.

### 2. Related work (~800 words, Table 1)

**Purpose**: credit each line of work and state the point where it
stops short of this setting.
**Content**:

- 2.1 Small models for Text-to-SQL: fine-tuned open models and what
  they are trained on.
- 2.2 Preference optimization and execution feedback for SQL and code:
  DPO; training on a model's own outputs labelled by execution;
  CodeLutra as the closest centralized work: what it does and where
  this method differs, said here, in the text, once for the paper.
  No other section compares with it (the Method section cites it at
  the objective; the settings that follow it are named in 4.5).
- 2.3 Federated fine-tuning of language models and federated semantic
  parsing. Three earlier lines, each with the point where it stops:
  federated SFT with LoRA and FedDPO (OpenFedLLM), on fixed preference
  datasets; federated reinforcement learning with verifiable rewards
  (Fed-GRPO, PubSwap), where a client samples from the current model
  and scores the samples against a reference answer, for math and code
  and with a policy-gradient objective; federated semantic parsing and
  Text-to-SQL (FL4SP and later work), trained with SFT and scored by
  exact match.
- Table 1, in 2.3 (owner, 2026-11-28): the federated methods closest to ours
  (Zhang et al., FedDPO, PubSwap, Fed-GRPO, the method) against the
  properties that no earlier federated method has together
  (Text-to-SQL, labels from SQL execution, training on the model's own
  outputs, how the pairs arise, the reference model of the preference
  objective). Liu et al., ExCoT and CodeLutra are not rows.

**Transition to next**: no earlier federated method has all the
properties of the last row of Table 1; Section 3 defines it.

### 3. Method (~1,320 words, Fig. 2, Algorithm 1)

**Purpose**: define the method so that it can be reimplemented, and
give the reason for each design choice. Each component is motivated
against federated SFT and federated DPO as published.
**Content**:

The section is told by component of the framework, not by the stages of
a training run (owner, 2026-11-27); Fig. 2 and Algorithm 1 carry the
order of a run.

- 3.1 Problem Formulation (`sec:formulation`, ~300): clients, their
  questions, gold SQL and databases; the prompt; the adapter and the
  global model; rounds; what is and is not shared.
- 3.2 Execution-Derived Supervision (`sec:supervision`, ~150): what a
  client's database adds to the gold SQL. The gold SQL stays necessary:
  its result is what a sampled query is compared with. The measurement,
  one short paragraph: from the model after two rounds of FedAvg SFT,
  ten samples per question yield preference pairs (on BIRD, both a
  correct and an incorrect query) for
  `\fact{cost.bird.pref1.paired}` 5,877 of the
  `\fact{cost.bird.pref1.questions}` 9,428 training questions of BIRD
  (`\fact{cost.bird.pref1.paired_pct}` 62.3%); on Spider 4,013 of
  8,659 (1,759 of the 8,659 are on databases without rows and yield no
  pair). It answers how
  often the signal of Fig. 1 occurs, before the framework is
  introduced. The subsection names no warm-up round (defined in 3.4)
  and gives no counts by round (they are in the cost table).
- 3.3 Framework Overview (`sec:overview`, ~200, Fig. 2): the
  components and the role of each; the two kinds of round; several
  clients, what stays at a client and what the server averages.
- 3.4 Supervised Warm-Up (`sec:warmup`, ~200): FedAvg SFT on the gold
  SQL; why the preference rounds do not start from the pretrained
  model (the questions without a correct sample,
  `\fact{warmup.bird.k0.no_correct}` against
  `\fact{warmup.bird.k2.no_correct}`).
- 3.5 Client-Side Execution Labeling (`sec:labeling`, ~250): sampling
  from the round's global model; execution on the client's databases;
  the execution label.
- 3.6 On-Policy Preference Pair Construction (`sec:pairs`, ~200):
  pairs of a correct and an incorrect sample of the same question,
  constructed anew in each preference round; two pairs per question
  and the reason; questions that yield no pair.
- 3.7 Preference Objective and Aggregation (`sec:objective`, ~400):
  the preference term and the NLL term; the round's global model as
  the reference model; the average weighted by pair counts; what
  leaves a client; Algorithm 1; communication unchanged (E1, in kind).
  The measured times are in 5.5.

**Transition to next**: the experiments.

### 4. Experimental setup (~990 words; the table of setups is Table S3)

**Purpose**: everything a reader needs to judge and repeat the
experiments.
**Content**:

- 4.1 Datasets and metrics: BIRD (dev) and Spider (test) for the main
  results; Spider dev, Spider-Syn, Spider-Realistic and Spider-DK for
  5.4; execution accuracy and test-suite accuracy. The test suites:
  the official ones for Spider dev, Spider-Syn and Spider-Realistic,
  and one sentence that points to the generated suite of BIRD dev in
  Section S6 (owner, 2026-11-28).
- 4.2 Federated setups (Table 2): how the training sets are split over
  clients; the setups of 5.4.
- 4.3 Models: Qwen2.5-Coder-1.5B-Instruct, the 0.5B model, and
  DeepSeek-Coder-1.3B.
- 4.4 Baselines: no training, local SFT (BIRD), centralized SFT,
  FedAvg SFT, federated DPO as published; the control of 5.3 (FedAvg
  SFT at the settings of the preference rounds) is named in 4.5. No
  FedProx SFT (owner, 2026-11-28).
- 4.5 Implementation: the prompt (Appendix A), LoRA, optimizer and
  rates, rounds, sampling, decoding, seed (Appendix B has every
  setting); one sentence on the settings of the preference rounds that
  follow CodeLutra, with its ten pairs per question beside the two
  here; one run with one seed.
- 4.6 Statistical test: the exact McNemar test on paired predictions,
  Holm correction inside each table, a test printed in two tables
  counting in the first; no family of the text (owner, 2026-11-28).

**Transition to next**: the results, from the gain to its cost.

### 5. Results and analysis (~1,400 words, Tables 3 to 8, Figs. 3 and 4)

**Purpose**: show the gain, what it consists of, which component
accounts for it, how far it carries and what it costs. Owner,
2026-11-28: no p in the prose of Sections 5 and 6; "significant" only
for a test that a table of the paper or of the Supplementary Materials
prints; a comparison that no table prints is stated in points and
counts.
**Content**:

- 5.1 Main results (`sec:main`; Table 3, Fig. 3). BIRD first,
  then Spider.
  A1 the gain at four rounds; A2 FedAvg SFT stops improving after
  round 3, tested in Table S4; A3 the gain by difficulty level; A4 one
  preference round against one more SFT round, two sentences; A5
  centralized SFT; A6 FedDPO (and local SFT on BIRD when its rows are
  in); C4 in one sentence, with FedDPO beside it (Table S5).
- 5.2 Analysis of the predictions (`sec:analysis`; Fig. 4). C1
  execution errors halve and C2 incorrect results do not fall, as
  counts; C5 in one sentence; C6 the change at every client, three
  sentences with Table S7 (owner, 2026-11-28); C3 in two sentences, with the counts
  under EX and under the suite, the detail in S6.4 and Table S6.
- 5.3 Ablation study (`sec:ablation`; Table 4). EX on both datasets,
  each row tested against the method; TS of the BIRD rows in Table S5.
  The control (B9) first: FedAvg SFT at the settings of the preference
  rounds, at 3 and 4 rounds. Then B1 pairs and reference renewed each
  round, B2 the second preference round (Table S4), B4 the preference
  term, B3 the NLL term, B6 in one sentence. B5 is read in 5.4 from
  Table 7. B7 and B8 are not in the paper.
- 5.4 Other models, federated setups and perturbed questions
  (`sec:breadth`; Tables 5, 6, 7). D1 the 0.5B model and D2
  DeepSeek-Coder, on Spider test only (Table 5); D3 IID and alpha 0.5
  with 5 and 10 clients; D4 the gain on Spider dev, Spider-Syn,
  Spider-Realistic and Spider-DK under both metrics, and the row
  without warm-up rounds (B5).
- 5.5 Computation and communication cost (`sec:cost`; Table 8). E1 no
  added communication; E2 GPU time and label time of a round.

**Transition to next**: what the results say about the two kinds of
round.

### 6. Discussion (~340 words)

**Purpose**: interpret the results and state the scope of the study.
**Content** (three paragraphs, no subsections; owner, 2026-11-28):

- The gain over FedAvg SFT in every configuration trained
  independently; why a preference round adds more than a further SFT
  round, also at the settings of the preference rounds (A2, A4, B9), as
  interpretation.
- Why the preference rounds remove execution errors (C1, B4), as a
  reading.
- Scope and future work, the three items of `CLAIMS.md`, section 5
  (second revision (owner, 2026-11-28)).

### 7. Conclusion (~130 words)

**Purpose**: the contribution in a few sentences and the open
directions.

### Declarations, Supplementary Materials

Declarations: funding, competing interests, data availability, code
availability, author contributions, use of AI tools. Appendix A: the
prompt as the model saw it. Appendix B: all settings in one generated
table. These carry no argument and are assembled by the main session.

## Evidence Map

| Section | Claims | Tables and figures | Evidence type |
|---|---|---|---|
| 1 | A1, A2, C1; contributions | Fig. 1 | headline results, from the macros |
| 2 | wording 7 of `CLAIMS.md`, section 4 | Table 1 | earlier work, from `bib/report.md` |
| 3 | E1 (in kind); decision 9 of `CLAIMS.md`, section 7 | Fig. 2, Algorithm 1 | the method as built; settings from `generated/settings.tex`; the counts of 3.2 and 3.4 from the round records |
| 4 | none | Table 2; Appendix A, B | datasets, models, baselines, settings |
| 5.1 | A1 to A6, C4 | Table 3, Fig. 3; Tables S4, S5 | results and paired tests |
| 5.2 | C1, C2, C3, C5, C6 | Fig. 4; Tables S6, S7 | error counts, form of the answers, label statistics per client |
| 5.3 | B1 to B4, B6, B9 | Table 4; Tables S4, S5 | results and paired tests |
| 5.4 | D1 to D4, B5 | Tables 5, 6, 7 | results and paired tests |
| 5.5 | E1, E2 | Table 8 | measured times |
| 6 | scope items 1 to 3 | none | interpretation |

Evidence that waits on the GPU, written with its macro and printed as a
placeholder: A5 on BIRD (centralized SFT), local SFT on BIRD, FedDPO on
Spider (Tables 3 and 4), the control at 4 rounds (Table 4, and its TS
in Table S5), D2, D3 (the rows of `generated/missing.txt`, 2026-11-28).
Figs. 1 and 2 wait for the owner's decision on the images.

## Tables and figures

Numbered in the order of first mention.

| Number | Content | File |
|---|---|---|
| Fig. 1 | one question, two ways of training | `fig_idea` |
| Fig. 2 | framework overview | `fig_method_overview` (to be redrawn) |
| Fig. 3 | EX by round | `fig_rounds` |
| Fig. 4 | incorrect predictions by round | `fig_errors` |
| Table 1 | the closest methods by property | written with Section 2 |
| Table 2 | federated setups (Table S3 in the PDF) | `tab_setups` |
| Table 3 | main rows | `tab_main` |
| Table 4 | ablation, EX, with the control | `tab_ablation` |
| Table 5 | other models, Spider test | `tab_models` |
| Table 6 | federated setups, results | `tab_federated` |
| Table 7 | Spider dev and the perturbed sets | `tab_robust` |
| Table 8 | cost | `tab_cost` |
| Table S4 | EX by round | `tab_rounds` |
| Table S5 | TS on BIRD dev for the rows of Table 4 | `tab_ts` |
| Table S6 | correct predictions on the gold SQL's or other tables or columns | `tab_form` |
| Table S7 | the labels at each client | `tab_clients` |

The PDF numbers each table of the paper one lower than this list
(Table 3 here is Table 2 in the PDF), since the table of setups is in
the Supplementary Materials.

## Open with this outline

1. B5 on BIRD: the rows without warm-up and with three warm-up rounds
   are not run (owner, 2026-11-28), so B5 is read from Table 7 (Spider
   dev, Spider-Syn, Spider-Realistic) in 5.4.
2. No baseline of federated reinforcement learning with verifiable
   rewards is planned; 2.3 and Table 1 state the difference in kind.

## Word Count Summary

| Section | Words, upper end | Words aimed at | Pages in the plan |
|---|---:|---:|---:|
| 1 Introduction | 1,050 | 950 | 2.1 |
| 2 Related work | 900 | 810 | 1.8 |
| 3 Method | 1,700 | 1,530 | 4.1 |
| 4 Experimental setup | 1,350 | 1,220 | 2.5 |
| 5 Results and analysis | 2,880 | 2,590 | 7.5 |
| 6 Discussion | 780 | 700 | 1.2 |
| 7 Conclusion | 200 | 180 | 0.3 |
| Total | 8,860 | 7,980 | 19.5 |

The words of the first column were set from the pages of the plan, less
the space of the floats, at 650 words a page. Measured in the class on
2026-11-26, running text sets about 600 words a page, and the displayed
equations of the Method section take about 0.4 page. The first column
is therefore the upper end of a section, and the length aimed at is
about 10% less (second column; owner, 2026-11-26), which fits the pages
of the plan; the subsections share the reduction in proportion. Against
the outline of 2026-11-26 (8,510 words, 18.6 pages) this one adds
Fig. 1 (about 0.4 page), Section 3.2, the test suite of BIRD in 4.1 and
its results in 5.2; these additions are estimates, not measured. These
budgets were set for the 25 pages of JIIS. The paper is written for CMC
(owner, 2026-11-27), which has no page limit and charges for each page
above 15; the draft is complete first and trimmed later
(`WRITING_PLAN.md`, sections 1 and 6).
