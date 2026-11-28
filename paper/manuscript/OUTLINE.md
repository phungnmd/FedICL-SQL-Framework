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
predictions change and whether the gain survives a change of the
database contents (5.2), which component accounts for it (5.3), then
breadth (5.4, 5.5) and cost (5.6).

Length (owner, 2026-11-28): about 20 pages; the fee of the journal
covers 15. The paper was cut from 32 to 21 pages on that day: the body
has about 6,000 words, and the subsections below are merged where the
text merges them (3.1 with 3.2, 3.3 with 3.4, 3.5 with 3.6; 4.3 with
4.4; 5.4 with 5.5). The word counts in the headings are those of the
text after the cut. What a reader needs only to reproduce is in the
Supplementary Materials (`supplement.tex`, built by `make` into
`build/supplement.pdf`): S1 the prompt, S2 the settings and software,
S3 the federated setups and the partition procedure (Table S3), S4 the
perturbed questions (Table S4), S5 execution labeling, the time limits
and the generated suite of BIRD dev. Where an entry below names
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
  this method differs, said here and in Table 1, once for the paper.
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
- Table 1: the closest methods against the properties that separate
  them (federated, Text-to-SQL, labels from execution, pairs of the
  model's own outputs, pairs made again each round). It gains a row
  for federated reinforcement learning with verifiable rewards; the
  fact rows of Fed-GRPO and PubSwap are built before the pack of this
  section.

**Transition to next**: no earlier method has all the properties of the
last row of Table 1; Section 3 defines it.

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
  The measured times are in 5.6.

**Transition to next**: the experiments.

### 4. Experimental setup (~990 words; the table of setups is Table S3)

**Purpose**: everything a reader needs to judge and repeat the
experiments.
**Content**:

- 4.1 Datasets and metrics: BIRD (dev) and Spider (test) for the main
  results; Spider dev, Spider-Syn, Spider-Realistic and Spider-DK for
  5.5; execution accuracy and test-suite accuracy. The test suites:
  the official ones for Spider dev, Spider-Syn and Spider-Realistic,
  and for BIRD dev a generated suite (100 variants of each database),
  with how it was generated and how far it agrees with the official
  suite on Spider dev.
- 4.2 Federated setups (Table 2): how the training sets are split over
  clients; the setups of 5.4.
- 4.3 Models: Qwen2.5-Coder-1.5B-Instruct, the 0.5B model, and
  DeepSeek-Coder-1.3B.
- 4.4 Baselines: no training, local SFT, centralized SFT, FedAvg SFT,
  FedProx SFT, federated DPO as published.
- 4.5 Implementation: the prompt (Appendix A), LoRA, optimizer and
  rates, rounds, sampling, decoding, seed (Appendix B has every
  setting); one sentence on the settings of the preference rounds that
  follow CodeLutra, with its ten pairs per question beside the two
  here.
- 4.6 Statistical test: the exact McNemar test on paired predictions,
  Holm correction inside each table.

**Transition to next**: the results, from the gain to its cost.

### 5. Results and analysis (~1,600 words, Tables 2 to 6, Figs. 3 and 4; the perturbed sets in Table S4)

**Purpose**: show the gain, what it consists of, which component
accounts for it, how far it carries and what it costs.
**Content**:

- 5.1 Main results (`sec:main`, ~550; Table 3, Fig. 3). BIRD first,
  then Spider.
  A1 the gain at four rounds; A2 FedAvg SFT stops improving after
  round 3; A3 the gain by difficulty level; A4 one preference round
  against one more SFT round; A5 centralized SFT; A6 local SFT,
  FedProx SFT and federated DPO.
- 5.2 Analysis of the predictions (`sec:analysis`, ~450; Fig. 4,
  Table 4). Which predictions change, and whether the gain survives a
  change of the database contents. C1 execution errors halve; C2
  incorrect results do not fall; C3 correct answers written otherwise
  than the gold SQL, with their counts under EX and under the test
  suite on BIRD; C4 the gain on BIRD dev under test-suite accuracy,
  read from the FedAvg SFT row of Table 4.
- 5.3 Ablation study (`sec:ablation`, ~880; Table 4). Table 4 gives
  EX on both datasets and test-suite accuracy on BIRD dev, each row
  tested against the method. The components in the order of Section 3: B5 the number of warm-up rounds; B1 pairs and reference
  renewed each round against those of the first preference round, B2
  the second preference round and B8 pairs of the gold SQL for the
  questions without a correct sample; B4 the preference term and B3
  the NLL term; B6 the weights of the server average and B7 clients
  pooled in the preference rounds.
- 5.4 Other models and federated setups (`sec:breadth`, ~450;
  Tables 5, 6). The
  changes of the training configuration: D1 the 0.5B model; D2
  DeepSeek-Coder; D3 IID and alpha 0.5 with 5 and 10 clients.
- 5.5 Perturbed questions (`sec:perturbed`, ~350; Table 7). D4 the gain on Spider dev,
  Spider-Syn, Spider-Realistic and Spider-DK under both metrics, apart
  from the fall of either model when the question is perturbed; the
  row without warm-up rounds (B5).
- 5.6 Computation and communication cost (`sec:cost`, ~200; Table 8). E1 no added
  communication; E2 GPU time and label time of a round.

**Transition to next**: what the results say about the two kinds of
round.

### 6. Discussion and limitations (~470 words)

**Purpose**: interpret the results and state the scope of the study.
**Content**:

- Why the two kinds of round remove different errors (C1, C2, B4, B5),
  as interpretation.
- The scope of the setting and the eight limitations of `CLAIMS.md`,
  section 5.

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
| 5.1 | A1 to A6 | Table 3, Fig. 3 | results and paired tests |
| 5.2 | C1 to C4 | Fig. 4, Table 4 | error counts, form of the answers, test-suite scores |
| 5.3 | B1 to B8 | Table 4 (and Table 7) | results and paired tests |
| 5.4 | D1 to D3 | Tables 5, 6 | results and paired tests |
| 5.5 | D4, B5 | Table 7 | results and paired tests |
| 5.6 | E1, E2 | Table 8 | measured times |
| 6 | limitations 1 to 8 | none | interpretation |

Evidence that waits on the GPU, written with its macro and printed as a
placeholder: A5 on BIRD, A6, the second seed of Table 3, D2, D3, the
BIRD rows of B3, B4 and B5, B7 (the 34 rows of `generated/missing.txt`).
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
| Table 2 | federated setups | `tab_setups` |
| Table 3 | main rows | `tab_main` |
| Table 4 | ablation; BIRD dev also under test-suite accuracy | `tab_ablation` |
| Table 5 | other models | `tab_models` |
| Table 6 | federated setups, results | `tab_federated` |
| Table 7 | Spider dev and the perturbed sets | `tab_robust` |
| Table 8 | cost | `tab_cost` |

## Open with this outline

1. B5 on BIRD: the rows without warm-up and with three warm-up rounds
   at 4 rounds wait, so 5.3 reads B5 from Table 7 (Spider dev,
   Spider-Syn, Spider-Realistic), which the reader meets in 5.5.
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
| 6 Discussion and limitations | 780 | 700 | 1.2 |
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
