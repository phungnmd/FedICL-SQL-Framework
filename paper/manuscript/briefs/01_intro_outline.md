# Outline: Section 1, Introduction (with the abstract)

One line per paragraph, in order. "Serves" names the statement of the
brief (1 to 8; a need of a later section by its row in "What the later
sections take from this section"). Words are running text. Total 945.
The lines are notes, not sentences of the paper; a value in brackets is
what the macro prints today.

One heading, `\section{Introduction}\label{sec:intro}`, no subsection
and no float. The order goes from the task to the setting, then the
gap in three steps (what federated fine-tuning uses, what execution
adds where one site holds everything, why that has not reached
federated training), then the method, the results and the
contributions.

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Text-to-SQL systems divide into those that prompt a proprietary model and open models fine-tuned for the task, and only the second can be trained and served by the organization that owns the data. One sentence of definition (a natural language question about a database is translated into a SQL query), with Spider and BIRD as the cross-domain benchmarks. The prompting line in one sentence: GPT-4 is given the question and the schema through an API, so both are sent to a provider. The fine-tuned line: CodeS (1B to 15B parameters, data privacy when calling an API among its motives), OmniSQL (7B to 32B), SLM-SQL (0.5B to 1.5B). The two lines are not ranked and no accuracy is quoted | 1; Spider and BIRD cited at first mention | `yu2018spider`, `li2023bird`, `gao2024dailsql`, `pourreza2023dinsql`, `li2024codes`, `li2025omnisql`, `sheng2025slmsql` | 115 |
| 2 | The setting: the data needed to fine-tune such a model are held by organizations that cannot pool them, and federated learning trains one model across them. Training needs questions with gold SQL queries and the databases they refer to; an organization holds these for its own few databases, and both the databases and the questions asked of them are internal. The aim is one model for all of them, on questions and databases beyond those any one holds. Federated learning in two sentences, in the manner of the FedAvg passage: each organization is a client, a server maintains a global model, each client trains it on its own data and only the model update leaves the client; federated averaging (FedAvg) as the standard algorithm. "Federated Text-to-SQL" is said once to mean this federated training of the model, and only the trained model is deployed. Privacy as data that stay at the client, nothing beyond | 2; the setting as Section 2 assumes it; "global model"; "federated Text-to-SQL" said once; FedAvg in full | `mcmahan2017fedavg` | 125 |
| 3 | Federated fine-tuning as it stands learns from the gold SQL query alone, and the databases at the clients go unused in training. The standard recipe: FedAvg with low-rank adaptation (LoRA), each client training an adapter by supervised fine-tuning (SFT) and the server averaging the adapters; for Text-to-SQL, Zhang et al. train with federated SFT on the gold SQL. Then what this supervision consists of: one gold SQL query per question as the only target, no query executed in training. Worded as what these methods use; the next paragraph says what is thereby left out | 3; SFT and LoRA in full; Zhang et al. by name | `hu2022lora`, `zhang2023fl4sp` | 95 |
| 4 | Execution supplies a label that the gold SQL query alone does not, and where one site holds everything, models are already trained on it. The execution label defined in a sentence: a query sampled from the model is correct when its execution result on the database equals that of the gold SQL query, and incorrect otherwise. Direct preference optimization (DPO) in a clause: pairs of a preferred and a dispreferred output, with the change of the model measured against a reference model. CodeLutra, named as the closest work: at one site, each iteration samples from the current model, labels the samples by execution, pairs a correct with a failed sample and trains with the DPO loss and a negative log-likelihood (NLL) term | 4, first half; "execution label", "reference model", "NLL term"; DPO and NLL in full | `rafailov2023dpo`, `tao2024codelutra` | 85 |
| 5 | In federated training this label can be computed only at the client, where the database is, and no federated method computes it. Federated DPO as published (FedDPO, in OpenFedLLM): the pairs come from a preference dataset given to each client in advance, one reference model serves all rounds, and the loss has no NLL term; its pairs are therefore not outputs of the model being trained and do not follow it over the rounds. The scoped gap closes the paragraph: to our knowledge, no earlier method for federated Text-to-SQL training uses execution on the clients' databases as supervision | 4, second half | `ye2024openfedllm` | 95 |
| 6 | We propose `\method`, in which execution turns the one gold SQL query of a question into many correct and incorrect queries of the model's own. The idea first, as what the method does: a client samples queries from the model, executes them on its database and compares each result with that of the gold SQL query. Then the method in three sentences. Training starts with warm-up rounds of FedAvg SFT. Preference rounds follow: in each, every client samples several queries per question from the current global model, labels them by execution on its own databases, pairs correct with incorrect samples and trains with a preference term (the DPO loss) and an NLL term, the global model of the round being the reference model. Last sentence, what leaves a client: only the adapter and the number of pairs that weights it in the average, as the adapter and the number of questions do in FedAvg SFT. No symbol and no value of $T$, $T_w$, $N$ or $M$ (point 3) | 5, 6; "warm-up round", "preference round" | `\method` | 160 |
| 7 | With five clients and a model of 1.5 billion parameters, `\method` is above FedAvg SFT at the same number of rounds on both benchmarks. Execution accuracy (EX) in full. BIRD dev: the two EX values and the gain; Spider test: the two EX values and the gain; both differences significant, without $p$-values. Further rounds do not let FedAvg SFT reach it: FedAvg SFT stops improving after round 3 on both datasets. Where the gain shows: the predictions that end in an execution error fall by about half, as two pairs of counts. The cost in a closing clause: a preference round takes more computation at a client than an SFT round | 7 (A1, A2, C1); EX in full | `\ex{bird}{k2}{4}` [48.76], `\ex{bird}{fedavg}{4}` [42.57], `\gap{bird}{fedavg}{4}{k2}{4}` [6.19]; `\ex{spider}{k2}{4}` [78.20], `\ex{spider}{fedavg}{4}` [74.71], `\gap{spider}{fedavg}{4}{k2}{4}` [3.49]; `\nerr{bird}{fedavg}{4}` [268], `\nerr{bird}{k2}{4}` [128], `\nerr{spider}{fedavg}{4}` [173], `\nerr{spider}{k2}{4}` [84]; `\setting{model.size}` [1.5 billion] | 125 |
| 8 | The contributions, as a lead-in sentence and four items. (1) The observation that the databases of a client are supervision that federated fine-tuning leaves unused, and, to our knowledge, the first federated Text-to-SQL training method that uses it. (2) The method: warm-up rounds of FedAvg SFT followed by preference rounds with execution labels computed at the clients, pairs renewed in each round and the same communication as FedAvg SFT (Section 3). (3) The evidence: the gain on BIRD dev and Spider test at the same number of rounds, where it arises, what each part of the method adds and what a round costs a client (Sections 5 and 6). (4) The release of the code, the client splits and the predictions of every row. No ranking among them and no number repeated from paragraph 7 | 8 | `\method`; `sec:method`, `sec:results`, `sec:ablation` | 145 |

No paragraph that outlines the paper: the items of paragraph 8 point to
the sections, and the length is at the brief's figure without it.

## Abstract

One paragraph of about 200 words, no citation, in the order the brief
offers.

| # | Role | Content | Words |
|---|---|---|---|
| 1 | Task and setting | Organizations that hold questions with gold SQL queries and the databases they refer to cannot pool them; federated learning trains one small Text-to-SQL model across them, and only model updates leave a client | 45 |
| 2 | Gap | Federated supervised fine-tuning (SFT) learns from the gold SQL query alone; the databases at the clients are not used in training, although executing a query on them shows whether it is correct | 35 |
| 3 | Method | `\method`: warm-up rounds of federated SFT, in which the model learns from the gold SQL query of every question; then preference rounds, in which each client samples queries from the current global model, executes them on its own databases, labels each by comparing its execution result with that of the gold SQL query and trains the model to prefer its correct over its incorrect samples, with direct preference optimization (DPO) and a likelihood term. Only the adapter and one integer leave a client, as in federated SFT | 80 |
| 4 | Result | Five clients, a model of 1.5 billion parameters: a gain of `\gap{bird}{fedavg}{4}{k2}{4}` [6.19] points in execution accuracy (EX) on BIRD dev over federated averaging with SFT at the same number of rounds; also above it on Spider test, without the number; fewer predictions end in an execution error, said without a count | 45 |

Keywords planned: Text-to-SQL, Federated learning, Preference
optimization, Execution feedback, Small language models,
Parameter-efficient fine-tuning.

## For the editor

1. The gap takes three paragraphs (3, 4, 5) where the brief has two
   statements. Statement 4 holds two points, that training on
   execution labels exists at one site and that it has not reached
   federated training, and each gets its own opening sentence. The
   four terms Section 2.2 needs ("execution label", "reference
   model", "NLL term", DPO) are then introduced in paragraph 4, with
   CodeLutra, before paragraph 5 says what FedDPO lacks.
2. The NLL term enters through CodeLutra ("the DPO loss and a negative
   log-likelihood (NLL) term"), where the brief's row says "a
   likelihood term"; Section 3.4 already describes CodeLutra with "a
   DPO and an NLL term". Paragraph 5 can then say that FedDPO "has no
   NLL term" and be understood.
3. Paragraph 6 carries no value of $T$, $T_w$, $N$ or $M$ and no
   symbol; paragraph 7 says "at the same number of rounds" without the
   number. Section 3.1 gives the values. Say if the four rounds should
   be named in paragraph 7.
4. Paragraph 7 uses `\setting{model.size}` ("1.5 billion") for the
   size of the model, as Section 4.3 does. It is not in the brief's
   table of macros. The name of the model is left to Section 4.3.
5. Paragraph 7 quotes no $p$-value and says "both differences are
   significant"; Section 5.1 has the tests. The four counts of
   execution errors are quoted, since "about half" alone would be a
   number without a macro.
6. Prompting systems: one sentence, citing both `gao2024dailsql` and
   `pourreza2023dinsql`, which uses the two keys the brief allows
   beyond those of other sections.
7. Paragraph 1 opens with one sentence that defines the task. It is
   the common definition and rests on no row of the brief.
8. "non-IID" is listed in `TERMS.md` among the abbreviations given in
   full at first use, and Sections 4.2, 4.4 and 5.1 use it without
   expansion. Statement 7 does not describe the clients as non-IID, so
   the Introduction as outlined does not introduce it. Either Section
   4.2 expands it, or paragraph 7 says "five clients whose data are
   not independent and identically distributed (non-IID)"; I plan the
   first unless told otherwise.
9. Contributions as an `itemize` list of four items after a lead-in
   sentence. Say if they should be running prose.
10. Abstract. (a) The baseline is named as "federated averaging with
    SFT" there and FedAvg is not abbreviated, since the abbreviation
    would be used once. (b) NLL is not abbreviated either: "a
    likelihood term". (c) The fall in execution errors is said without
    a count, so that the abstract keeps to its one number; it can go
    if the abstract should end on the two benchmarks.
