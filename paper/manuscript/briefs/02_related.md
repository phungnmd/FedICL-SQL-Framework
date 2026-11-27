# Brief: Section 2, Related work (with Table 1)

Kind of section: related work (`VOICE_GUIDE.md`, Section 2).
Outline to: `briefs/02_related_outline.md`. Draft to:
`sections/02_related.tex`. Notes to: `briefs/02_related_notes.md`.

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Headings | `\section{Related work}\label{sec:related}`; `\subsection{Small language models for Text-to-SQL}\label{sec:rel-slm}`; `\subsection{Preference optimization and execution feedback}\label{sec:rel-pref}`; `\subsection{Federated fine-tuning of language models}\label{sec:rel-fed}`; `\subsection{Federated semantic parsing and Text-to-SQL}\label{sec:rel-fedsql}`. The wording of the four headings is yours; no heading below a subsection |
| Before it | Section 1 (`sec:intro`, not written yet). It will have stated: organisations hold questions with gold SQL queries and the databases they run on, and cannot pool them; a small model is trained across them with federated learning, and only that model is deployed; FedAvg SFT learns from the one gold SQL query of a question and never uses the databases; whether a query returns the gold result can be established only where the database is; the method in three sentences, the headline results, the contributions. It also says once that "federated Text-to-SQL" means federated training of the model. None of this is repeated here |
| After it | Section 3 (`sec:method`, accepted, in `sections/03_method.tex`) defines the method. Its Section 3.4 states where a preference round differs from CodeLutra (the federated round, the number of pairs, the NLL term averaged over tokens), and sets on-policy pairs against the pairs of FedDPO. Section 4.4 (`sec:baselines`) describes FedDPO as a baseline. This section names these works and what they did; the detail of the comparison stays where it is |
| Float | Table 1 (`tab:related`), set by you in this section's file (see "Table 1") |
| Purpose | Credit each line of work the method draws on, and state the point where it stops short of this setting: training a Text-to-SQL model across clients that keep their questions and their databases |
| Length | about 810 words of running text, 900 at most. About: 2.1 180, 2.2 260, 2.3 220, 2.4 150. The caption and the cells of Table 1 are not counted |

## Section 2.1, Small language models for Text-to-SQL

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Open models fine-tuned for Text-to-SQL are an established line of work, with data privacy as one of its motives (CodeS), and it reaches models of 1.5B parameters and below. The methods differ in what the model is trained on: a SQL-centric pre-training corpus and the training set of a benchmark (CodeS), synthetic data at scale (OmniSQL), data synthesized from the training databases with self-play fine-tuning (SPFT-SQL), SFT followed by reinforcement learning with an execution-based reward (SLM-SQL, Think2SQL, Arctic-Text2SQL-R1) | the rows of `li2024codes`, `li2025omnisql`, `zhang2025spftsql`, `sheng2025slmsql`, `papicchio2025think2sql`, `yao2026arctic` | what each paper did, at the sizes it states. No accuracy of another paper is set against ours: their prompts, data and decoding differ from ours. The privacy motive of CodeS concerns one organization and the provider of an API; our setting is several organizations that cannot pool their data. The motive is credited only if the step between the two is said; it may be left out |
| 2 | Where this line stops for our setting: each of these methods trains at one site that holds the questions, the SQL queries and the databases together | the rows: every one trains on a pooled training set | said as the setting they assume, once; it is not a weakness of the methods |

## Section 2.2, Preference optimization and execution feedback

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | DPO trains a model from pairs of a preferred and a dispreferred output, against a reference model | the rows of `rafailov2023dpo` | as stated |
| 2 | For SQL the preference needs no annotation beyond the gold SQL query that SFT already uses: queries sampled from a model are executed, and the comparison with the result of the gold query decides which is preferred. Liu et al. and ExCoT train Text-to-SQL models with DPO on such pairs; outside SQL, Pang et al. iterate sampling, labeling by the correctness of the final answer and training with a DPO and an NLL term | the rows of `liu2025cotdpo`, `zhai2025excot`, `pang2024irpo` | sizes and tasks as each paper states them. What Liu et al. find for outputs that are SQL only is reported as their finding, with their decoding and their model sizes, and with their setup beside it as the rows give it (pairs constructed once, the DPO loss alone, a fixed reference). No cause is claimed for their result; the paper points to its own ablation of the same parts (Section 6, `sec:ablation`): the row without renewal keeps the pairs and the reference model of the first preference round, and another row removes the NLL term, so the three choices are all examined there. The section does not read as training without labels: the gold SQL query decides every preference. The reinforcement-learning papers of Section 2.1 also learn from execution; whether they are named here or there is yours |
| 3 | When the pairs are constructed differs: once, from one model (Liu et al.); first from another model, then from the model in training (ExCoT); anew in every iteration (CodeLutra, Pang et al.). Lanchantin et al. compare the regimes directly | the rows of these papers and of `lanchantin2025bridging` | what each reports on its own tasks. Pang et al. are named: the DPO and NLL loss with pairs constructed anew in every iteration and the model of the previous iteration as the reference is theirs before CodeLutra. The sentence on Lanchantin et al. may be left out for length (the key is then cited in Section 6 only) |
| 4 | CodeLutra is the closest work: the loop of sampling from the current model, execution-based labeling against the result of the gold query, pairs of a correct and a failed sample, and training with a DPO and a likelihood term, repeated over iterations, at one site | the rows of `tao2024codelutra` | "the same loop, run centrally"; CodeLutra is a method for code generation, evaluated on Text-to-SQL and on data-science code. The pointer to Section 3.4 says that the section compares the two methods. Nothing is listed as taken from CodeLutra (owner, 2026-11-27; `AGENTS.md`, Writing, "Credit"): the values that follow it are named once, in Section 4.5. Different, as the paragraph states it: training runs across clients that cannot pool their data (the federated round takes the place of the iteration; each client labels on its own databases and samples from the global model of the round), and warm-up rounds of FedAvg SFT come first. The number of pairs and the averaged NLL term are settings and stay in Section 3.4. That the pairs are renewed is common to the two and is not listed as a difference. One name for the likelihood term |
| 5 | Execution labels also train models that choose among candidates at inference: a verifier (LEVER), outcome reward models (GradeSQL) | the rows of `ni2023lever`, `tritto2026gradesql` | credit in a sentence; in both the model that generates the query is not trained |
| 6 | Where this line stops for our setting: the works that label by execution train at one site, which holds the questions and the databases | the rows above | said once in the subsection, where it serves (the sentence on CodeLutra already has "at one site"). That an execution label can be computed only where the database is belongs to Section 1 and is not argued again here |

## Section 2.3, Federated fine-tuning of language models

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Language models are fine-tuned across clients with FedAvg and LoRA: a client trains an adapter on its data with SFT and the server averages the adapters. Packages and benchmarks exist for it (FederatedScope-LLM, OpenFedLLM), with code generation among their tasks | `mcmahan2017fedavg`, `hu2022lora` (named as the sources of FedAvg and LoRA); the rows of `kuang2024fsllm`, `ye2024openfedllm` | as stated |
| 2 | DPO in federated settings: in the FedDPO of OpenFedLLM each client holds a preference dataset, the loss is the DPO loss alone and the reference model is fixed for the whole process; its data are preference datasets for helpfulness and harmlessness. Wu et al. keep human preference data at the clients, which train preference selectors, and train the language model at the server with DPO (in their work DPO runs at the server, not at the clients) | the rows of `ye2024openfedllm`, `wu2025fedbiscuit` | the pairs of FedDPO are responses that come with the dataset: not outputs of the model being trained. "Human preferences" only where the row says so |
| 3 | Federated training in which a checkable answer supplies the signal exists for mathematics, medical question answering and code: federated reinforcement learning with verifiable rewards (PubSwap, Fed-GRPO) | the rows of `nayak2026pubswap`, `guo2026fedgrpo` | said plainly, as earlier work on verifiable rewards in federated training |
| 4 | Where this line stops for our setting: none of these federated works (FederatedScope-LLM, OpenFedLLM, Wu et al., PubSwap, Fed-GRPO) trains a Text-to-SQL model, where the label is the execution result on a database of the client; the pairs of FedDPO do not come from the model and do not follow it over the rounds | the rows above | as stated |

## Section 2.4, Federated semantic parsing and Text-to-SQL

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Zhang et al. are the earlier work on federated learning for Text-to-SQL: eight single-domain datasets as the clients, T5-base, supervised training on the gold SQL, exact match as the metric; plain FedAvg falls far below centralized training on these clients, and their re-weighting of the clients (Lorar) recovers a large part of the gap | the rows of `zhang2023fl4sp` | "the earlier work"; that it is the only one is said under the "to our knowledge" of statement 4. Their question is the heterogeneity of the clients under supervised training, ours what execution on the databases of a client adds to the gold SQL as supervision: the paragraph says how the two relate, and does not read as learning from the databases without the gold SQL. Its numbers as its Table 2 has them, if any serves that |
| 2 | Federated learning has also been applied to a semantic parser for knowledge-graph questions (Xu et al.) | the row of `xu2024kgrfl` | one clause, no more than its row: only its abstract was read |
| 3 | In Zhang et al. nothing is executed: the gold SQL is the only supervision, in training and in evaluation | the rows of `zhang2023fl4sp` | stated for Zhang et al. only |
| 4 | Table 1 sets the closest methods side by side. To our knowledge Zhang et al. is the only earlier work that trains a Text-to-SQL model with federated learning, and no earlier method does so with execution labels and pairs of the model's own outputs constructed anew in each round; Section 3 defines one | Table 1 | "to our knowledge", once, covering both halves, with this scope. The table shows what each work has: CodeLutra every property but the federated one, Zhang et al. the federated setting and the task |

## Table 1

The closest methods by the properties that separate them. Five rows:
Zhang et al. (`zhang2023fl4sp`), FedDPO (`ye2024openfedllm`), ExCoT
(`zhai2025excot`), CodeLutra (`tao2024codelutra`), \method{}. The
layout is yours: one column per property, or the two properties of the
pairs in one column; words, or symbols of the packages `main.tex`
already loads; a cell that is not a plain yes or no gets a short entry
or a table note. The rows describe the methods as published (FedDPO is
also run on Text-to-SQL as a baseline of this paper, Section 4.4). The float is set like the other tables of the paper
(Table 2 in `sections/04_setup.tex`).

| Property | Zhang et al. | FedDPO | ExCoT | CodeLutra | \method{} |
|---|---|---|---|---|---|
| Federated training | yes | yes | no | no | yes |
| Text-to-SQL | yes | no: preference datasets for helpfulness and harmlessness | yes | yes; also Python data-science code | yes |
| Labels from execution | no: nothing is executed | no: the preference comes with the dataset | yes: against the result of the gold query | yes: against the result of the gold query | yes: at the client, against the result of the gold SQL query |
| Pairs of the model's own outputs | no pairs (supervised training) | no: responses stored in the dataset | first round: outputs of GPT-4o; later rounds: outputs of the model in training | yes | yes |
| Pairs constructed anew during training | no pairs | no: each client holds its preference dataset | yes, in the later rounds | yes, in every iteration | yes, in every preference round |

The locator of every cell is in "Facts about the cited papers".

## Wording that holds for the whole section

- A sentence about a cited paper says what its rows below say, and
  nothing beyond them. Model sizes, counts and results of other papers
  are typed as the rows give them.
- The point where a line of work stops is the setting it assumes (who
  holds the data and the databases), not a fault of its methods.
- No result of another paper is compared with a result of ours.
- "To our knowledge" stands once, on statement 4 of Section 2.4.
- A work without a name of its own is cited by its authors: Zhang et
  al. ("FL4SP" is not a word of that paper; its re-weighting is called
  Lorar), Liu et al., Pang et al., Lanchantin et al., Wu et al., Xu et
  al. The key `papicchio2025think2sql` is the preprint of Think2SQL.
- Privacy in this paper is that the data stay at the client.
- The reference list of the paper is held near 40 entries. The keys
  below are those of this section; a key is cited where a sentence
  uses its paper.

## Facts about the cited papers

One row per fact. A sentence about a paper is written from its rows.
The locators are for the check of the draft and are not printed; page
numbers are those of the arXiv version of each paper.

### Section 2.1

| Key | Fact | Locator |
|---|---|---|
| `li2024codes` (CodeS) | a series of open-source language models built for Text-to-SQL, at 1B, 3B, 7B and 15B parameters | abstract, p. 1; Sec. 4, p. 4 |
| | StarCoder models pre-trained further on a SQL-centric corpus of 21.5 GB, then fully fine-tuned on the training set of each benchmark (Spider, BIRD) | Sec. 1, p. 2; Sec. 5.2, p. 6; Sec. 9.1.3, p. 10 |
| | its motive: a closed-source model called through an API puts data privacy at risk, since the data must be sent to the provider; cost and undisclosed training details are the other two | Sec. 1, pp. 1 to 2 |
| `li2025omnisql` (OmniSQL) | SynSQL-2.5M: 2,544,390 synthetic Text-to-SQL samples over 16,583 synthetic databases, each with a chain-of-thought solution | Sec. 1, p. 2; abstract |
| | OmniSQL at 7B, 14B and 32B: Qwen2.5-Coder-Instruct models fine-tuned on SynSQL-2.5M together with the training sets of Spider and BIRD | Sec. 5, p. 8; Sec. 6.1.3, p. 9 |
| `zhang2025spftsql` (SPFT-SQL) | synthesizes SQL queries from templates filled with tables, columns and values of the training databases, and their questions with a SQL-to-Text model; executes the outputs of the fine-tuned model on the synthesized data and compares them with the synthesized SQL; then fine-tunes by self-play between a main and an opponent model, with a reward computed by execution | Sec. 3.1, Eq. (1), p. 4; Sec. 3.2, Algorithm 1, Eqs. (2) and (3), p. 5 |
| | models: Qwen2.5-Coder at 1.5B, 7B, 14B and 32B, Llama3-8B-Instruct, Deepseek-Coder-7B-Instruct | Sec. 4.1, p. 7 |
| `sheng2025slmsql` (SLM-SQL) | five models of 0.5B to 1.5B parameters, among them Qwen2.5-Coder-0.5B-Instruct and Qwen2.5-Coder-1.5B-Instruct | abstract, p. 1; Sec. 3.1, p. 3; App. B, p. 8 |
| | training: SFT on 916,156 samples with chain-of-thought solutions (filtered from SynSQL-2.5M), then GRPO on BIRD train, with a reward for a correct execution result plus a small format term | Sec. 2, p. 3; Table 1, p. 3; App. C, Eqs. (1) to (3), p. 9 |
| | inference: 64 samples by default, grouped by execution result and voted; a second trained model writes the final query when the vote is not consistent | Sec. 2, "Inference", p. 3; App. B, p. 8 |
| `papicchio2025think2sql` (Think2SQL) | GRPO on BIRD train (9,007 samples) with a reward computed by execution (execution accuracy, or a partial score of the returned cells) plus format terms; Qwen2.5-Coder-Instruct at 0.5B, 1.5B, 3B, 7B and 14B | Sec. 2.3, p. 5; Sec. 3.1, p. 6 |
| `yao2026arctic` (Arctic-Text2SQL-R1) | GRPO with reward 1 when the execution result matches that of the gold query, 0.1 when the query only executes, 0 otherwise; models of 7B, 14B and 32B, started from OmniSQL; trained on filtered BIRD and Spider training data and synthetic data | Sec. 3, p. 4; Sec. 4, p. 4; Sec. 5, p. 7 |

### Section 2.2

| Key | Fact | Locator |
|---|---|---|
| `rafailov2023dpo` (DPO) | optimizes a language model on pairs of a preferred and a dispreferred response "without explicit reward modeling or reinforcement learning"; the loss (its Eq. 7) compares the model with a reference model on the two responses | Sec. 1, p. 2; Sec. 4, Eq. (7), p. 4 |
| | the reference model is the SFT model that the preference data were sampled from, when there is one | Sec. 4, "DPO outline", p. 5 |
| `liu2025cotdpo` (Liu et al.) | SFT on BIRD train; then 16 samples per training question from the SFT model, each executed and labeled correct only when its result matches that of the gold query; a correct and an incorrect sample form a pair; questions whose samples are all correct or all incorrect are dropped | Sec. 3.3 and 3.4, p. 4; App. D, p. 14 |
| | the pairs are constructed once; the loss is the DPO loss alone, with the SFT model as the reference | Sec. 3.3 and 3.4, p. 4; App. D, p. 14 |
| | ten models of 6.7B to 15B parameters, all weights fine-tuned | Sec. 1, p. 2; App. D, p. 14 |
| | finding, BIRD dev with greedy decoding: when the output is the SQL query alone, EX falls after DPO for 6 of the 10 models; when the output is chain-of-thought reasoning followed by the query, it rises for all 10 | Sec. 1, p. 2; Table 1, p. 6 |
| `zhai2025excot` (ExCoT) | Text-to-SQL on BIRD and Spider, trained at one site; models of 70B (Llama-3.1) and 32B (Qwen2.5-Coder) | Sec. 4.1, pp. 5 to 6; Table 1, p. 6 |
| | the SQL of each output is executed and its result compared with that of the gold query | Sec. 3.3, p. 4 |
| | one DPO round on pairs of GPT-4o outputs, then two rounds on pairs of outputs of the model in training (up to 32 new samples per question in each); the outputs are chain-of-thought text ending in SQL | Sec. 3.4, p. 5; Sec. 4.1, p. 6 |
| `pang2024irpo` (Pang et al., Iterative RPO) | each iteration samples chain-of-thought answers from the current model, pairs one whose final answer is correct with one whose final answer is wrong, and trains with a DPO term plus an NLL term on the correct one; the reference is the model of the previous iteration | Sec. 1, p. 1; Sec. 2, Eq. (1), p. 3 |
| | tasks: mathematical and science reasoning (GSM8K, MATH, ARC-Challenge); model: Llama-2-70B-Chat | Sec. 3.1 to 3.3, pp. 4 to 8 |
| `lanchantin2025bridging` (Lanchantin et al.) | compares DPO trained offline (the responses generated once), semi-online (the model that generates is synchronised with the model in training every $s$ steps) and online; on mathematical tasks with a verifiable answer the semi-online and online models are above the offline one (Math500: 53.7 offline, 58.9 at $s = 100$, 58.7 online); Llama-3.1-8B-Instruct | Sec. 2.3, p. 3; Sec. 4.1, p. 6; Table 1, p. 5; Sec. 3, p. 4 |
| `tao2024codelutra` (CodeLutra) | one training set at one site; Text-to-SQL on Spider and BIRD, and Python data-science code; Llama-3-8B for the main results | Sec. 4, p. 5; Sec. 5.1, pp. 6 to 7 |
| | each sampled SQL query is executed and its result compared with that of the reference query | Sec. 5.1, p. 7; Algorithm 1, line 8, p. 7 |
| | a pair is one correct and one failed sample of the current model; sampling, labeling and pairs are repeated in every iteration (four iterations) | Sec. 4, p. 5; Algorithm 1, p. 7; Sec. 5.1, p. 7 |
| | loss: a DPO term plus a weighted log-likelihood of the correct samples; the reference of the DPO term is the model of the previous iteration | Sec. 4, Eq. (3), p. 6 |
| `ni2023lever` (LEVER) | trains a verifier that judges a program sampled from a code language model from the question, the program and its execution result, and reranks the samples with it; the training labels come from comparing execution results with the gold result; the model that generates is not fine-tuned; Spider is one of its four datasets | abstract, p. 1; Sec. 2.3, p. 3; Sec. 3.1 and 3.2, pp. 3 to 4 |
| `tritto2026gradesql` (GradeSQL) | candidates sampled from a Text-to-SQL model for the training questions are labeled by comparing their execution result with that of the gold query; a language model fine-tuned on these labels (an outcome reward model) ranks the candidates at inference; the model that generates is used as released | Sec. III.B, p. 4; Sec. I, p. 2; Sec. IV, p. 6 |

### Section 2.3

| Key | Fact | Locator |
|---|---|---|
| `mcmahan2017fedavg`, `hu2022lora` | FedAvg; LoRA (named as their sources) | |
| `kuang2024fsllm` (FederatedScope-LLM) | a package for fine-tuning language models in federated learning with parameter-efficient methods (LoRA, P-tuning, prompt tuning), with a benchmark; one of its benchmarks is code generation with nine clients, one programming language each | abstract, p. 1; Sec. 3.1, p. 4 |
| `ye2024openfedllm` (OpenFedLLM) | a framework for federated instruction tuning and federated value alignment with seven federated algorithms, FedAvg, FedProx and SCAFFOLD among them; a 7B model with LoRA; code generation is one of its domains | Sec. 3.1, p. 5; Sec. 4.1, pp. 7 to 8; Sec. 4.5, p. 11 |
| | FedDPO, its method for value alignment: each client holds a preference dataset of instructions with a preferred and a dispreferred response; the loss is the DPO loss alone; the reference model "is fixed throughout the FL process" | Sec. 3.3, Eq. (2), pp. 6 to 7 |
| | its two datasets: for helpfulness, the highest-scored of four responses of different language models as the preferred one and a random other one as the dispreferred; for harmlessness, a dataset of human preferences | Sec. 4.7, p. 11; Sec. 4.8, p. 12 |
| | the paper describes no step that generates or relabels responses during the rounds | Sec. 3.1, 3.3, 4.1, 4.7, 4.8 |
| `wu2025fedbiscuit` (Wu et al.; their methods are named FedBis and FedBiscuit) | each client trains a binary selector on its pairwise human preference data and the server aggregates the selectors; the language model is trained at the server, with DPO, on pairs that it generated and the selector labeled | Sec. 4, p. 4; App. A.2, pp. 17 to 18; Sec. 6, p. 8 |
| | FedDPO is one of its two baselines | Sec. 7, p. 8 |
| `nayak2026pubswap` (PubSwap) | federated reinforcement learning with verifiable rewards: each client runs local GRPO steps with LoRA and the adapters are averaged; on shared public prompts the server passes responses between the clients; mathematics and medical question answering; models of 1.5B to 4B parameters | Sec. 1, p. 2; Sec. 3, pp. 5 to 6; Sec. 4.1, pp. 6 to 7 |
| `guo2026fedgrpo` (Fed-GRPO) | federated GRPO in which the server weights a client by the standard deviation of its rewards in the round; the reward is the correctness of the answer; mathematics and code generation; models of 3B and 4B parameters | abstract, p. 1; Eq. (4), p. 5; Sec. 6.1, p. 8 |
| the five papers of this subsection | none of them has a Text-to-SQL task | the full text of each searched |

### Section 2.4

| Key | Fact | Locator |
|---|---|---|
| `zhang2023fl4sp` (Zhang et al.) | eight clients and a server learn a global model without sharing a client's data; each client is one single-domain Text-to-SQL dataset; neither Spider nor BIRD is used | abstract, p. 1; Sec. 5, pp. 5 to 6 |
| | T5-base, trained with supervision on the gold SQL of each client; no output of the model is generated during training | Sec. 3, p. 3; App. A, Algorithm 1, p. 11 |
| | nothing is executed: a prediction is correct only when it is the same string as the gold SQL (exact match) | Sec. 5, "Evaluation Metrics", p. 6 |
| | FedAvg, FedProx and FedOPT, each with and without Lorar, which weights a client in the average by the size of its training set times the reduction of its training loss in the round | abstract, p. 1; Sec. 4.2, Eq. (6), p. 5 |
| | exact match averaged over the eight clients: centralized training 70.32, FedAvg 40.03, FedAvg with Lorar 60.16, the best federated variant (FedOPT with Lorar) 62.55; training each client alone reaches 62.78 | Table 2, p. 7 |
| `xu2024kgrfl` (Xu et al.) | a multitask BART model that identifies the category of a question and converts it into a SPARQL query over a knowledge graph, for joint modelling by several institutions; a model fusion strategy based on reinforcement learning is proposed for its federated learning | abstract |

### Table 1

| Row | Cell | Locator |
|---|---|---|
| Zhang et al. | federated; Text-to-SQL; nothing executed; no pairs | the rows of Section 2.4 above |
| FedDPO | federated; preference datasets for helpfulness and harmlessness; preference from the dataset; responses stored in the dataset; no step that constructs pairs during training | the rows of `ye2024openfedllm` above |
| ExCoT | one site; Text-to-SQL; labels from execution against the gold result; first round GPT-4o outputs, later rounds the model's own; new samples in the later rounds | the rows of `zhai2025excot` above |
| CodeLutra | one site; Text-to-SQL and data-science code; labels from execution against the reference result; pairs of the current model's samples; every iteration | the rows of `tao2024codelutra` above |
| \method{} | every cell | Sections 3.1 and 3.4 (`sec:setting`, `sec:pref-round`) |

## Labels available

Of this section: `sec:related`, `sec:rel-slm`, `sec:rel-pref`,
`sec:rel-fed`, `sec:rel-fedsql`, `tab:related`.

Of other sections: `sec:intro`, `sec:method`, `sec:setting`,
`sec:pref-round`, `sec:setup`, `sec:baselines`, `sec:results`,
`sec:ablation`, `sec:discussion`.

## Paragraph roles (an offer)

For each line of work: its scope in a sentence; the representative
methods, compactly, by what they do; the point where the line stops for
this setting; the link to the method or to the next line. Grouped by
mechanism, never by year. The closest works get the most room, and
Table 1 carries the comparison that the text need not spell out cell
by cell.
