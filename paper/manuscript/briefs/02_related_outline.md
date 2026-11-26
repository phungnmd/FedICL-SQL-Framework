# Outline: Section 2, Related work

One line per paragraph, in order. "Serves" names the statement of the
brief (subsection.number). Words are running text; the caption, the
cells and the notes of Table 1 are not counted. Total 810. The section
has no lead-in paragraph before 2.1.

## 2.1 Fine-tuned open models for Text-to-SQL (180)

Heading proposed in place of "Small language models for Text-to-SQL"
(point 1 for the editor).

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Fine-tuning an open model for Text-to-SQL is an established line, and the methods differ in what the model is trained on. CodeS as the start of the paragraph: models of 1B to 15B, pre-trained further on a SQL-centric corpus and fine-tuned on the training set of each benchmark, with data privacy as one motive (a closed model behind an API requires sending the data to its provider). Then, by training signal and not by year: synthetic data at scale (OmniSQL: SynSQL-2.5M, models of 7B to 32B fine-tuned on it with the training sets of Spider and BIRD); data synthesized from the training databases with self-play fine-tuning (SPFT-SQL); SFT followed by reinforcement learning with an execution-based reward (SLM-SQL, Think2SQL, Arctic-Text2SQL-R1). The line reaches models of 1.5B parameters and below (SLM-SQL 0.5B to 1.5B; Think2SQL from 0.5B; SPFT-SQL from 1.5B). The reinforcement-learning works are named here only, last in the list, so that the execution-based reward leads into 2.2. No accuracy of any of these papers | 2.1.1 | `li2024codes`, `li2025omnisql`, `zhang2025spftsql`, `sheng2025slmsql`, `papicchio2025think2sql`, `yao2026arctic` | 125 |
| 2 | The setting this line assumes: each method trains at one site that holds the questions, the SQL queries and the databases together, on a pooled training set. Said once, as the setting. The privacy that CodeS addresses is that of a model owner toward an API provider; several owners whose data cannot be pooled are outside its scope. One clause may add that the 1.5B model of our experiments is among the models these works fine-tune (point 6) | 2.1.2 | `sec:setup` (only if the clause stays) | 55 |

## 2.2 Preference optimization and execution feedback (265)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Execution can supply a preference between two outputs instead of a reward. DPO in one sentence: pairs of a preferred and a dispreferred output, a loss that compares the model with a reference model on the two. For SQL the preference needs no annotator: sampled queries are executed, and the comparison with the result of the gold SQL query decides which is preferred. Liu et al. and ExCoT train Text-to-SQL models with DPO on such pairs. One sentence gives the finding of Liu et al. as theirs (ten models of 6.7B to 15B, BIRD dev, greedy decoding: execution accuracy rises after DPO for all ten when chain-of-thought reasoning precedes the query and falls for six when the output is the query alone), with no explanation attached (point 2). Outside SQL, Pang et al. iterate sampling, labeling by the correctness of the final answer and training with a DPO and an NLL term, on reasoning tasks | 2.2.1, 2.2.2 | `rafailov2023dpo`, `liu2025cotdpo`, `zhai2025excot`, `pang2024irpo` | 105 |
| 2 | These methods differ in when the pairs are constructed, and CodeLutra, which renews them in every iteration, is the closest work. The regimes in one sentence: once, from the SFT model (Liu et al.); first from outputs of GPT-4o, then from outputs of the model in training (ExCoT); anew in every iteration (Pang et al., CodeLutra). Lanchantin et al. compare the regimes directly: on mathematical tasks with a verifiable answer, models trained with semi-online and online DPO are above the one trained offline (direction only, no number typed). CodeLutra then gets the room: for Text-to-SQL it samples from the current model, labels each sample by comparing its execution result with that of the reference query, pairs a correct with a failed sample, trains with a DPO term and a likelihood term on the correct samples, and repeats this over the iterations, at one site. A closing clause: the sampling and loss settings of `\method` follow it, with the pointer to Section 3.4 and no list | 2.2.3, 2.2.4 | `tao2024codelutra`, `lanchantin2025bridging`, `liu2025cotdpo`, `zhai2025excot`, `pang2024irpo`; `\method`; `sec:pref-round` | 100 |
| 3 | Whatever the execution label trains, the party that computes it holds the database. First, the other use of the label as one sentence of credit: a model that chooses among candidates at inference, a verifier in LEVER and an outcome reward model in GradeSQL, the model that generates the queries not being trained in either. Then the point where the line stops: in all works of this subsection the party that trains holds the questions and the databases; an execution label requires the database, and in federated training only the client has it | 2.2.5, 2.2.6 | `ni2023lever`, `tritto2026gradesql` | 60 |

## 2.3 Federated fine-tuning of language models (215)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Language models are fine-tuned across clients with FedAvg and LoRA: a client trains an adapter on its own data with SFT, and the server averages the adapters. The two named sources, then the packages and benchmarks: FederatedScope-LLM (parameter-efficient methods, a benchmark; code generation with nine clients, one programming language each) and OpenFedLLM (federated instruction tuning and value alignment, seven federated algorithms, a 7B model with LoRA; code generation among its domains) | 2.3.1 | `mcmahan2017fedavg`, `hu2022lora`, `kuang2024fsllm`, `ye2024openfedllm` | 70 |
| 2 | DPO has been federated, on preferences that the clients already hold. FedDPO of OpenFedLLM: each client holds a preference dataset of instructions with a preferred and a dispreferred response, the loss is the DPO loss alone, the reference model is fixed for the whole process; its datasets serve helpfulness and harmlessness. The half of statement 4 that concerns FedDPO is said here, as a description of it: the responses come with the dataset, so the pairs are not outputs of the model being trained and do not follow it over the rounds. Wu et al.: the human preference data stay at the clients, which train preference selectors that the server aggregates; the language model is trained at the server with DPO. One clause: FedDPO is a baseline of our experiments (Section 4.4) | 2.3.2, 2.3.4 (FedDPO half) | `ye2024openfedllm`, `wu2025fedbiscuit`; `sec:baselines` | 80 |
| 3 | A checkable answer has also supplied the training signal in federated learning, for tasks other than Text-to-SQL. Federated reinforcement learning with verifiable rewards: PubSwap (local reinforcement-learning steps with LoRA, adapters averaged; mathematics and medical question answering; models of 1.5B to 4B) and Fed-GRPO (the server weights a client by the spread of its rewards in the round; the reward is the correctness of the answer; mathematics and code generation). The stop closes the subsection: none of the works above trains a Text-to-SQL model, for which the label is the execution result on a database of the client. GRPO is not expanded; the works are described as reinforcement learning | 2.3.3, 2.3.4 | `nayak2026pubswap`, `guo2026fedgrpo` | 65 |

## 2.4 Federated semantic parsing and Text-to-SQL (150)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Zhang et al. are the earlier work on federated learning for Text-to-SQL, and in it the gold SQL is the only supervision. Their setup: eight single-domain datasets as the clients, T5-base, supervised training on the gold SQL, exact match as the metric. Their result with the numbers of their Table 2 (point 5): FedAvg reaches an exact match of 40.03 against 70.32 for centralized training, and their re-weighting of the clients, Lorar, raises it to 60.16. Nothing is executed, in training or in evaluation: a prediction counts when it is the same string as the gold SQL. One clause for Xu et al.: federated learning applied to a semantic parser for knowledge-graph questions | 2.4.1, 2.4.2, 2.4.3 | `zhang2023fl4sp`, `xu2024kgrfl` | 95 |
| 2 | Table 1 sets the closest methods side by side, and the combination that `\method` has appears in no earlier row. What the table shows, in one sentence and not cell by cell: CodeLutra has every property but the federated one, Zhang et al. the federated setting and the task. Then the one "to our knowledge" of the section, covering both halves: Zhang et al. is the only earlier work that trains a Text-to-SQL model with federated learning, and no earlier method does so with execution labels and pairs of the model's own outputs constructed anew in each round. Last sentence hands over: Section 3 defines such a method | 2.4.4 | Table 1 (`tab:related`); `zhang2023fl4sp`, `tao2024codelutra`; `\method`; `sec:method` | 55 |

## Floats

| Float | Plan |
|---|---|
| Table 1 (`tab:related`) | In 2.4, before par. 2, where it is first cited. `table` environment with `[t]`, caption above, `booktabs` rules, set by hand in the section file like Table 2. Rows are the five methods in the order Zhang et al., FedDPO, ExCoT, CodeLutra, `\method`, each earlier one with its citation. Columns: Method; Federated training; Text-to-SQL; Labels from execution; Pairs from the model in training, renewed during training (one column for the two pair properties, point 3). Cells: `\checkmark` (amssymb) for yes, `$\times$` for no, an en dash for "no pairs" in the row of Zhang et al., and a short entry "from the second round" for ExCoT with a table note (its first round uses pairs of GPT-4o outputs). Notes through `\footnotemark` and `\footnotetext` of the class: the ExCoT note, and one saying that CodeLutra also covers Python data-science code. Caption: the closest methods by the properties that separate them; what the dash means. No full stop at its end |

## For the editor

1. Heading of 2.1. The line the subsection credits runs from 0.5B to
   32B (OmniSQL, Arctic-Text2SQL-R1), so "small language models" names
   only part of it. I propose "Fine-tuned open models for Text-to-SQL";
   the label `sec:rel-slm` stays. If the given heading is wanted, the
   paragraph is unchanged.
2. The finding of Liu et al. (2.2, par. 1, about 30 words). The claim of
   statement 2 does not require it; its ceiling says how to report it. I
   plan to report it: it is the main result of the closest paper on DPO
   for Text-to-SQL with outputs that are SQL only, which is also the
   output of our model, and a reviewer who knows that paper will look
   for it. It is stated with its models, set and decoding and without a
   cause, and it stands in par. 1, apart from the sentence on when the
   pairs are constructed, so that the order of the sentences does not
   suggest one. If it is to stay out, 2.2 falls to about 235 words and
   the section to about 780.
3. Table 1, the two properties of the pairs. In the five rows the two
   properties take the same value in every row (FedDPO no and no, ExCoT
   later rounds and later rounds, CodeLutra and `\method` yes and yes,
   Zhang et al. no pairs), so two columns would print one fact twice. I
   plan one column whose header states both. Two columns would separate
   rows only if Liu et al. were added (own outputs, constructed once);
   the brief gives five rows and I keep five.
4. Abbreviations. Section 1 is not written. I assume it gives SFT,
   FedAvg, DPO, LoRA and EX in full; Section 3 expands NLL at its own
   first use, which comes after this section, so this section would
   carry the first "negative log-likelihood (NLL)" unless Section 1
   does. I will write "execution accuracy" in full in the sentence on
   Liu et al. and "chain-of-thought reasoning" without an abbreviation.
   Tell me which abbreviations Section 1 has defined.
5. Numbers of other papers typed in the text: only the three of Zhang
   et al. (70.32, 40.03, 60.16), which make "far below" and "a large
   part of the gap" exact in fewer words than a paraphrase. Model sizes
   are typed as the rows give them. The figures of Lanchantin et al. are
   not typed; the direction is enough there.
6. A clause not asked for by a statement (2.1, par. 2): that the 1.5B
   model of our experiments is among the models SLM-SQL, Think2SQL and
   SPFT-SQL fine-tune, with a pointer to Section 4. It ties the line to
   the paper in ten words; it goes if you prefer the subsection to end
   on the setting.
7. Statement 2.3.4 is split: its half on FedDPO closes the paragraph on
   federated DPO, where it reads as a description of FedDPO, and its
   half on Text-to-SQL closes the subsection. Likewise the stop of each
   subsection is the last sentence or the last paragraph of that
   subsection, and no sentence announces the next subsection.
8. Section 3.4 already carries the detail of the comparison with
   CodeLutra and Section 4.4 that of FedDPO. This section describes the
   two works and points to those places once each; it does not repeat
   the differences in numbers of pairs, the NLL term or the reference
   model of our method.
