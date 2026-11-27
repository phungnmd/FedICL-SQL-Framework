# Paper outline

Approved by the owner on 2026-11-26. Built from `WRITING_PLAN.md`,
section 5, and the approved `CLAIMS.md`; claim numbers (A1 to E2) are
those of `CLAIMS.md`. The brief of a section is built from its entry
here. The bibliography keys come from `bib/report.md`, which names the
sources of each subsection.

## Structure

Results are organised by research question and the ablations have a
section of their own, as in the papers of the target journal.

## Overview

The paper starts from one observation: a client in federated
Text-to-SQL holds databases as well as questions with gold SQL, and
federated fine-tuning uses only the second. The introduction states the
gap and the method in brief; related work places it against small
models for Text-to-SQL, preference optimization with execution
feedback, federated fine-tuning and federated DPO, and federated
semantic parsing. The method section defines the setting and describes
the two kinds of round. The setup section fixes data, models, baselines
and tests. Four research questions organise the results: the gain over
the baselines, its breadth over models and federated setups, whether it
holds on perturbed questions and under test-suite accuracy, and what
changes in the answers and at what cost. The ablation study takes the
method apart. The discussion interprets the two kinds of round and
states the limits of the study.

## Research questions

| # | Question | Section | Claims |
|---|---|---|---|
| RQ1 | Does the method improve on FedAvg SFT and the other baselines at the same number of rounds? | 5.1 | A1 to A6 |
| RQ2 | Does the gain carry to other models and other federated setups? | 5.2 | D1 to D3 |
| RQ3 | Does the gain hold on perturbed questions and under test-suite accuracy? | 5.3 | D4, with B5 |
| RQ4 | What changes in the model's answers, and what does a client pay? | 5.4 | C1 to C3, E1, E2 |

## Detailed Outline

### Front matter

- Title: the name, the mechanism, the task and the setting.
- Abstract: 150 to 250 words, one paragraph, no citation, one number
  (the gain on BIRD dev).
- Keywords: 4 to 6.

### 1. Introduction (~1,050 words)

**Purpose**: state the problem, the gap, the idea and what the paper
shows.
**Content** (paragraphs, no subsections):

- Small models for Text-to-SQL are what an organisation can train and
  serve itself; the questions and databases of several organisations
  cannot be pooled. "Federated Text-to-SQL" here means federated
  training of the model, said once.
- The gap. FedAvg SFT learns from the one gold SQL of each question and
  never uses the databases. Federated DPO as published builds its pairs
  once and keeps one reference model. Whether a query returns the gold
  result can be established only where the database is.
- The idea: execution turns the one gold SQL of a question into many
  correct and incorrect queries of the model's own. The method in three
  sentences: warm-up rounds, preference rounds, what leaves a client.
- Headline results: A1 (the gain on BIRD dev and Spider test), A2 (more
  FedAvg SFT rounds do not reach it), C1 (execution errors halve).
- Contributions, four, as in `CLAIMS.md`, section 2.

**Transition to next**: the three lines of work the idea draws on.

### 2. Related work (~900 words, Table 1)

**Purpose**: credit each line of work and state the point where it
stops short of this setting.
**Content**:

- 2.1 Small models for Text-to-SQL: fine-tuned open models and what
  they are trained on.
- 2.2 Preference optimization and execution feedback for SQL and code:
  DPO; training on a model's own outputs labelled by execution;
  CodeLutra as the closest centralized work (the settings that follow
  it are named in 4.5 only).
- 2.3 Federated fine-tuning of language models: FedAvg with LoRA;
  federated DPO (OpenFedLLM) on fixed human-preference pairs;
  verifier-driven federated training for math and code.
- 2.4 Federated semantic parsing and Text-to-SQL: FL4SP and later work,
  which train with SFT.
- Table 1: the closest methods against the properties that separate
  them (federated, Text-to-SQL, labels from execution, pairs of the
  model's own outputs, pairs made again each round).

**Transition to next**: no earlier method has all the properties of the
last row of Table 1; Section 3 defines it.

### 3. Method (~1,650 words, Fig. 1, Algorithm 1)

**Purpose**: define the method so that it can be reimplemented, and
give the reason for each design choice.
**Content**:

The section is told by component of the framework, not by the stages of
a training run (owner, 2026-11-27); Fig. 1 and Algorithm 1 carry the
order of a run.

- 3.1 Problem Formulation (`sec:formulation`, ~300): clients, their
  questions, gold SQL and databases; the prompt; the adapter and the
  global model; rounds; what is and is not shared.
- 3.2 Framework Overview (`sec:overview`, ~200, Fig. 1): the
  components and the role of each; the two kinds of round.
- 3.3 Supervised Warm-Up (`sec:warmup`, ~200): FedAvg SFT on the gold
  SQL; why the preference rounds do not start from the pretrained
  model.
- 3.4 Client-Side Execution Labeling (`sec:labeling`, ~250): sampling
  from the round's global model; execution on the client's databases;
  the execution label.
- 3.5 On-Policy Preference Pair Construction (`sec:pairs`, ~200):
  pairs of a correct and an incorrect sample of the same question,
  constructed anew in each preference round; questions that yield no
  pair.
- 3.6 Preference Optimization Objective (`sec:objective`, ~300): the
  preference term and the NLL term; the round's global model as the
  reference model.
- 3.7 Aggregation and Client Cost (`sec:aggregation`, ~200): the
  average weighted by pair counts; what leaves a client; Algorithm 1;
  the added steps in kind, communication unchanged (E1). The measured
  times are in 5.4.

**Transition to next**: the questions the experiments answer.

### 4. Experimental setup (~1,250 words, Table 2)

**Purpose**: everything a reader needs to judge and repeat the
experiments.
**Content**:

- 4.1 Datasets and metrics: BIRD (dev) and Spider (test) for the main
  results; Spider dev, Spider-Syn, Spider-Realistic and Spider-DK for
  RQ3; execution accuracy and test-suite accuracy.
- 4.2 Federated setups (Table 2): how the training sets are split over
  clients; the setups of RQ2.
- 4.3 Models: Qwen2.5-Coder-1.5B-Instruct, the 0.5B model, and
  DeepSeek-Coder-1.3B.
- 4.4 Baselines: no training, local SFT, centralized SFT, FedAvg SFT,
  FedProx SFT, federated DPO as published.
- 4.5 Implementation: the prompt (Appendix A), LoRA, optimizer and
  rates, rounds, sampling, decoding, seed (Appendix B has every
  setting).
- 4.6 Statistical test: the exact McNemar test on paired predictions,
  Holm correction inside each table.

**Transition to next**: the four research questions.

### 5. Results (~1,800 words, Tables 3 to 7, Figs. 2 and 3)

**Purpose**: answer the four research questions.
**Content**:

- 5.1 RQ1, against the baselines (~550; Table 3, Fig. 2). A1 the gain
  at four rounds; A2 FedAvg SFT stops improving after round 3; A3 the
  gain by difficulty level; A4 one preference round against one more
  SFT round; A5 centralized SFT; A6 local SFT, FedProx SFT and
  federated DPO.
- 5.2 RQ2, other models and federated setups (~450; Tables 4, 5). D1
  the 0.5B model; D2 DeepSeek-Coder; D3 IID and alpha 0.5 with 5 and
  10 clients.
- 5.3 RQ3, perturbed questions and test-suite accuracy (~350;
  Table 6). D4 the gain on the four sets under both metrics; the row
  without warm-up rounds, discussed in Section 6.
- 5.4 RQ4, what changes and what it costs (~450; Fig. 3, Table 7). C1
  execution errors halve; C2 incorrect results do not fall; C3 correct
  answers written otherwise than the gold SQL; E1 and E2 the cost.

**Transition to next**: which part of the method each effect comes
from.

### 6. Ablation study (~880 words, Table 8)

**Purpose**: show what each part of the method adds.
**Content**: B1 pairs and reference renewed each round against those of
the first preference round; B2 the second preference round; B3 the NLL
term; B4 the preference term; B5 the number of warm-up rounds, read
with Table 6; B6 the weights of the server average; B7 clients pooled
in the preference rounds.

**Transition to next**: what the pattern of the ablations says about
the two kinds of round.

### 7. Discussion and limitations (~780 words)

**Purpose**: interpret the results and state the scope of the study.
**Content**:

- Why the two kinds of round remove different errors (C1, C2, B4, B5),
  as interpretation.
- The scope of the setting and the eight limitations of `CLAIMS.md`,
  section 5.

### 8. Conclusion (~200 words)

**Purpose**: the contribution in a few sentences and the open
directions.

### Declarations, Appendix A, Appendix B

Declarations: funding, competing interests, data availability, code
availability, author contributions, use of AI tools. Appendix A: the
prompt as the model saw it. Appendix B: all settings in one generated
table. These carry no argument and are assembled by the main session.

## Evidence Map

| Section | Claims | Tables and figures | Evidence type |
|---|---|---|---|
| 1 | A1, A2, C1; contributions | none | headline results, from the macros |
| 2 | wording 7 of `CLAIMS.md`, section 4 | Table 1 | earlier work, from `bib/report.md` |
| 3 | E1 (in kind) | Fig. 1, Algorithm 1 | the method as built; settings from `generated/settings.tex` |
| 4 | none | Table 2; Appendix A, B | datasets, models, baselines, settings |
| 5.1 | A1 to A6 | Table 3, Fig. 2 | results and paired tests |
| 5.2 | D1 to D3 | Tables 4, 5 | results and paired tests |
| 5.3 | D4, B5 | Table 6 | results and paired tests |
| 5.4 | C1 to C3, E1, E2 | Fig. 3, Table 7 | error counts, form of the answers, measured times |
| 6 | B1 to B7 | Table 8 (and Table 6) | results and paired tests |
| 7 | limitations 1 to 8 | none | interpretation |

Evidence that waits on the GPU, written with its macro and printed as a
placeholder: A5 on BIRD, A6, the second seed of Table 3, D2, D3, the
BIRD rows of B3, B4 and B5, B7 (the 34 rows of `generated/missing.txt`).
Fig. 1 waits for the owner's decision on the image.

## Word Count Summary

| Section | Words, upper end | Words asked in the brief | Pages in the plan |
|---|---:|---:|---:|
| 1 Introduction | 1,050 | 950 | 1.7 |
| 2 Related work | 900 | 810 | 1.8 |
| 3 Method | 1,650 | 1,490 | 4.0 |
| 4 Experimental setup | 1,250 | 1,130 | 2.3 |
| 5 Results | 1,800 | 1,620 | 5.5 |
| 6 Ablation study | 880 | 790 | 1.8 |
| 7 Discussion and limitations | 780 | 700 | 1.2 |
| 8 Conclusion | 200 | 180 | 0.3 |
| Total | 8,510 | 7,670 | 18.6 |

The words of the first column were set from the pages of the plan, less
the space of the floats, at 650 words a page. Measured in the class on
2026-11-26, running text sets about 600 words a page, and the displayed
equations of the Method section take about 0.4 page. A brief therefore
gives the first column as the upper end of its section and asks for
about 10% less (second column; owner, 2026-11-26), which fits the pages
of the plan; the
subsections share the reduction in proportion. These budgets were set
for the 25 pages of JIIS. The paper is written for CMC (owner,
2026-11-27), which has no page limit and charges for each page above
15; the draft is complete first and trimmed later
(`WRITING_PLAN.md`, sections 1 and 5).
