# Brief: Section 1, Introduction (with the abstract, the keywords and the title)

Kind of section: introduction (`VOICE_GUIDE.md`, Section 2).
Outline to: `briefs/01_intro_outline.md`. Draft to:
`sections/01_intro.tex`, then `sections/00_abstract.tex` and
`sections/00_keywords.tex`. Notes to: `briefs/01_intro_notes.md`,
which also carry three candidates for the title.

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Heading | `\section{Introduction}\label{sec:intro}`. No subsection |
| Before it | the title, the abstract and the keywords (see "Front matter") |
| After it | Section 2 (`sec:related`, in `sections/02_related.tex`) credits each line of work and has Table 1. The Introduction names only the works that lead the reader to the gap; it does not survey |
| Float | none. Fig. 1 belongs to Section 3 and is not referred to here |
| Purpose | State the problem, the gap, the idea and what the paper shows |
| Length | about 945 words of running text, 1,050 at most |

## What the later sections take from this section

Sections 2 to 6 are written and rely on the Introduction for the
following. Each has to be in it.

| What | Why |
|---|---|
| The abbreviations SFT, FedAvg, DPO, NLL, LoRA and EX in full at first use | Section 2 uses them without expansion |
| Spider and BIRD cited at first mention (`yu2018spider`, `li2023bird`) | Section 2 names them without a citation |
| The terms "execution label", "global model", "warm-up round", "preference round", "NLL term" and "reference model", each understandable where it first appears | Section 2.2 uses them before Section 3 defines them |
| "Federated Text-to-SQL" means federated training of the model; said once | the phrase could be read as querying federated databases |
| Zhang et al. by the authors' names | Sections 2 and 4 write "Zhang et al.", not the name of their benchmark |
| The setting as Section 2 assumes it: organizations hold questions with gold SQL queries and the databases they refer to, and cannot pool them; one small model is trained across them, and only that model is deployed | Section 2 does not repeat it |

## Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | The task and where it stands. Text-to-SQL; one line of systems prompts proprietary models through an API, which sends the question and the schema of the database to a provider; open models fine-tuned for the task are the alternative an organization can train and serve itself, and they reach models of 0.5B to 1.5B parameters | the rows under "Works the section may cite": CodeS (data privacy when calling APIs is among its motives), OmniSQL, SLM-SQL; optionally one prompting system | the two lines are not ranked against each other, and no sentence says that small models match the large ones; the sizes are those of the cited papers. One or two sentences on prompting systems at most |
| 2 | The setting. Training such a model needs questions with gold SQL queries and the databases they refer to. An organization holds these for its own few databases; several organizations cannot pool them, since the databases and the questions asked of them are internal. The aim is one model that serves all of them, on questions and databases beyond those any one of them holds. Federated learning trains it without moving the data: only model updates leave a client | the setting of Section 3.1; Section 4.1: the model is evaluated on databases that no client has seen; FedAvg (`mcmahan2017fedavg`) | stated as the setting and its motive. No sentence says that a client training alone does worse: that comparison is the Local SFT row of Table 3, which is not in yet. Privacy here is that the data stay at the client; nothing on differential privacy or on what an adapter reveals |
| 3 | The gap, first half. Federated fine-tuning of language models is FedAvg with LoRA adapters and SFT; for Text-to-SQL, Zhang et al. train this way. SFT learns from the one gold SQL query of each question, and nothing is executed in training: the databases at the clients go unused | Section 2.3, 2.4; `hu2022lora`, `zhang2023fl4sp` | a description of what these methods use, not a fault of theirs. "the databases go unused" is about training |
| 4 | The gap, second half, with its cause. Execution gives a label that the gold SQL query alone does not: a sampled query is correct when its execution result equals that of the gold SQL query. Where one site holds everything, execution already trains models: as a reward in reinforcement learning (SLM-SQL, Think2SQL, Arctic-Text2SQL-R1; Section 2.1) and as the label of preference pairs for DPO (CodeLutra, the closest work). In federated training the label can be computed only where the database is, at the client. Federated DPO as published (FedDPO) takes its preference pairs from a dataset given in advance, keeps one reference model for all rounds and has no NLL term: its pairs are not outputs of the model being trained and do not follow it over the rounds | Section 2.2, 2.3; `rafailov2023dpo`, `tao2024codelutra`, `ye2024openfedllm` | CodeLutra is the closest work and is said to be; the sentence on FedDPO describes it as published (its pairs come from preference datasets for helpfulness or harmlessness, as Section 2.3 words it; not "human preferences": the OpenFedLLM paper does not say that for both of its datasets). The gap is scoped: to our knowledge, no earlier method for federated Text-to-SQL training uses execution on the clients' databases as supervision |
| 5 | The idea. Execution turns the one gold SQL query of a question into many correct and incorrect queries of the model's own: the client samples queries from the model, executes them and compares each result with that of the gold SQL query | Section 3.4 | the idea is stated as what the method does. Why it helps is shown by the results (statement 7), not asserted here; the interpretation is Section 7's |
| 6 | The method in about three sentences. $T_w$ warm-up rounds of FedAvg SFT; then preference rounds, in each of which every client samples $N$ queries per question from the current global model, labels them by execution on its own databases, pairs correct with incorrect samples and trains with a preference term (the DPO loss) and an NLL term, the global model of the round being the reference model; only the adapter and the number of pairs that weights it leave a client, as the adapter and the number of questions do in FedAvg SFT. Where the method differs from the loop of CodeLutra is said here as Section 3.4 says it: only a client can compute the labels; a federated round is the step that renews samples, labels and pairs, with its global model as the reference model of every client; warm-up rounds of FedAvg SFT come first | Section 3; `\setting{rounds.warmup}`, `\setting{rounds.total}`, `\setting{pref.samples}`, `\setting{pref.pairs}` if a value is wanted | what leaves a client is said exactly as here. The values may stay in Section 3 |
| 7 | What the paper shows. With five clients and a model of 1.5B parameters, at the same number of rounds, the model is above FedAvg SFT on BIRD dev and on Spider test; further rounds of FedAvg SFT do not reach it; the execution errors of the predictions fall by about half | A1: `\ex{bird}{k2}{4}` against `\ex{bird}{fedavg}{4}`, `\gap{bird}{fedavg}{4}{k2}{4}` points; `\ex{spider}{k2}{4}` against `\ex{spider}{fedavg}{4}`, `\gap{spider}{fedavg}{4}{k2}{4}` points. A2: FedAvg SFT stops improving after round 3 on both datasets (Section 5.1). C1: `\nerr{bird}{fedavg}{4}` to `\nerr{bird}{k2}{4}` on BIRD dev, `\nerr{spider}{fedavg}{4}` to `\nerr{spider}{k2}{4}` on Spider test | "above FedAvg SFT at the same number of rounds on both datasets", significant; the headline number is the gain on BIRD dev. The reader of the Introduction alone can tell what the federation is (the clients are simulated by assigning each database of a training set, with all its questions, to one client, Section 4.2; the evaluation databases are held by no client), how the rounds divide (`\setting{rounds.warmup}` warm-up and `\setting{rounds.pref}` preference rounds), what "significant" rests on (the exact McNemar test of Section 4.6) and that the baseline is not read at a low round (its highest EX on BIRD dev is `\ex{bird}{fedavg}{3}` at round 3, `\gap{bird}{fedavg}{3}{k2}{4}` points below). For A2: "stops improving after round 3", not "degrades" and not "has converged". The sets are named. The cost is said in a clause: no communication beyond that of FedAvg SFT, and more computation at the clients (Section 5.4). The clause is about the method over its rounds, not about every preference round: the second preference round on Spider takes `\fact{cost.spider.pref2.ratio}` times an SFT round |
| 8 | Contributions, four: (1) the observation that the databases of a client are supervision that federated fine-tuning leaves unused, and, to our knowledge, the first federated Text-to-SQL training method that uses it; (2) the framework, as in statement 6 ("a federated learning framework", the name the paper gives the method where it introduces it; owner, 2026-11-27); (3) the evidence: the gain on the two benchmarks at the same number of rounds, where it arises (execution errors), what each part adds (Section 6) and what a client pays in compute; (4) the release: code, client splits and the predictions of every row | Sections 3, 5 and 6 | each contribution is one a reader can find an experiment or a section for. "First" only with "to our knowledge" and only in the scope of (1). The contributions are not ranked and the paper does not grade its own parts |

Statements 3 and 4 give the limitation and its cause; statement 5
answers that cause. An outline paragraph of the paper at the end is
yours to include or leave out.

## Works the section may cite

Facts as Section 2 and its fact sheet hold them
(`briefs/02_related_rows.md` has the locators). The reference list
is near its planned size: at most two keys that no other section cites.

| Key | Fact the Introduction may use |
|---|---|
| `yu2018spider`, `li2023bird` | the two cross-domain benchmarks; their evaluation databases are not in their training sets |
| `li2024codes` | open models of 1B to 15B parameters fine-tuned for Text-to-SQL; names data privacy when calling APIs among its motives (its Section 1) |
| `li2025omnisql` | models of 7B to 32B fine-tuned on synthetic data and the benchmark training sets |
| `sheng2025slmsql` | models of 0.5B to 1.5B parameters, trained by reinforcement learning with an execution-based reward |
| `papicchio2025think2sql`, `yao2026arctic` | reinforcement learning with an execution-based reward, at one site (cited in Section 2.1) |
| `gao2024dailsql`, `pourreza2023dinsql` (not cited elsewhere) | prompting GPT-4 with the question and the schema |
| `mcmahan2017fedavg`, `hu2022lora` | FedAvg; LoRA adapters |
| `zhang2023fl4sp` | the earlier federated work on Text-to-SQL: T5-base, SFT on the gold SQL, nothing executed in training or evaluation |
| `rafailov2023dpo` | DPO: pairs of a preferred and a dispreferred output, against a reference model |
| `tao2024codelutra` | the closest work: at one site, each iteration samples from the current model, labels by execution, pairs a correct with a failed sample and trains with a DPO and a likelihood term |
| `ye2024openfedllm` | FedDPO: preference datasets held by the clients, pairs fixed, the DPO loss alone, one reference model for the whole process |

## Macros

Text mode. The full list with values: `generated/numbers.md`.

| Macro | Prints |
|---|---|
| `\method` | the name of the method |
| `\ex{set}{line}{round}` | EX in percent, two decimals, without the percent sign; `set`: `bird` (BIRD dev), `spider` (Spider test); `line`: `k2` (`\method`), `fedavg` (FedAvg SFT) |
| `\gap{set}{fedavg}{4}{k2}{4}` | the difference in EX, `\method` minus FedAvg SFT at four rounds, without sign; `\gain{...}` with sign |
| `\pval{set}{fedavg}{4}{k2}{4}` | the exact McNemar p of that difference |
| `\nerr{set}{line}{round}` | predictions that end in an execution error |
| `\setting{rounds.total}`, `\setting{rounds.warmup}`, `\setting{rounds.pref}`, `\setting{pref.samples}`, `\setting{pref.pairs}` | $T$, $T_w$, the number of preference rounds, $N$, $M$ as values |
| `\setting{model.size}` | the parameters of the main model |
| `\ex{bird}{fedavg}{3}`, `\gap{bird}{fedavg}{3}{k2}{4}` | the highest EX of FedAvg SFT over its rounds on BIRD dev, and the difference of `\method` after four rounds to it |

## Wording that holds for the whole section

| | |
|---|---|
| the model | "the model" or its name for the trained model; the method has no teacher |
| sets | BIRD dev and Spider test by name; a number names its set |
| privacy | the data stay at the client; no guarantee beyond that is claimed |
| earlier work | credited for what it did; the gap is where it stops for this setting |
| numbers | only those of statement 7; every one a macro |

## Front matter

Written after the Introduction, by you, in the same files as listed at
the top.

| Part | Content |
|---|---|
| Abstract (`sections/00_abstract.tex`) | 150 to 250 words, one paragraph, no citation, every abbreviation in full at its first use in the abstract. The reader can name the setting, the gap, the method and the result after one reading. One number: the gain in EX on BIRD dev (`\gap{bird}{fedavg}{4}{k2}{4}` points over FedAvg SFT at the same number of rounds); the Spider result may be said without its number. Each name is readable without Section 3 |
| Keywords (`sections/00_keywords.tex`) | 4 to 6, separated by commas, the terms a reader of the field would search for |
| Title | three candidates in your notes, each of 15 words or fewer: the name of the method, its mechanism, the task and the setting. No abbreviation other than SQL and the name. The owner chooses; the title is not written into `main.tex` by you |

## Labels available

Of this section: `sec:intro`.

Of other sections: `sec:related`, `sec:method`, `sec:setup`,
`sec:results`, `sec:rq1`, `sec:rq3`, `sec:rq4`, `sec:ablation`,
`sec:discussion`, `sec:conclusion`.

## Paragraph roles (an offer)

From `voice/section_rhetoric.md`, the part on introductions: the task
and why it matters here; the earlier methods and the limitation with
its cause; what this paper does and why that answers the cause; what
the experiments show; the contributions. The setting itself is new to
most readers, so an opening that goes from the task to the setting
serves. For the abstract: the task and setting, the gap, the method
with what it gains from each of its two kinds of round, the result.
