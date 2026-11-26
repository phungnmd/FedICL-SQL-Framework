# Brief: Section 4, Experimental setup (with the text of Appendices A and B)

Kind of section: experimental setup (`voice/setup.md`).
Outline to: `briefs/04_setup_outline.md`. Draft to:
`sections/04_setup.tex`. Notes to: `briefs/04_setup_notes.md`.
Also yours: the lead-in sentences and the captions of
`sections/A_prompt.tex` and `sections/B_settings.tex` (see "The two
appendices").

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Headings | `\section{Experimental setup}\label{sec:setup}`; `\subsection{Datasets and metrics}\label{sec:datasets}`; `\subsection{Federated setups}\label{sec:fed-setups}`; `\subsection{Models}\label{sec:models}`; `\subsection{Baselines}\label{sec:baselines}`; `\subsection{Implementation}\label{sec:implementation}`; `\subsection{Statistical test}\label{sec:stat-test}`. No heading below a subsection |
| Before it | Section 3 (`sec:method`, accepted, in `sections/03_method.tex`): the setting, the warm-up rounds, a preference round, Algorithm 1. It defines every symbol and names the values of $T$, $T_w$, $N$, $M$, $\beta$, $\lambda$. It leaves to this section: how the SQL query is read from the output of the model and how execution results are compared (Section 3.4 says "as in evaluation (Section 4)"), the adapter, the optimizer and the learning rates |
| After it | Section 5 (`sec:results`), organised by the four research questions; Section 6 (`sec:ablation`); Section 7 (`sec:discussion`): limitations |
| Floats | Table 2 (`tab:setups`), the federated setups, in Section 4.2 |
| Purpose | A reader can judge the experiments and repeat them. No result is reported here |
| Length | about 1,125 words of running text, 1,250 at most. About: opening 90, 4.1 250, 4.2 190, 4.3 80, 4.4 215, 4.5 190, 4.6 110. Captions and the text of the appendices are not counted |

## Opening of the section (before 4.1)

One short paragraph: the experiments answer four research questions,
stated here once and used as the order of Section 5. Sections 4.1 and
4.2 refer to them by number.

| | Question | Answered in |
|---|---|---|
| RQ1 | does `\method` improve on FedAvg SFT and the other baselines at the same number of rounds | Section 5 |
| RQ2 | does the gain carry over to other models and other federated setups | Section 5 |
| RQ3 | does it hold on perturbed questions and under test-suite accuracy | Section 5 |
| RQ4 | what changes in the queries the model generates, and what a round costs a client | Section 5 |

Section 6 then removes the parts of the method one at a time. The
subsections of Section 5 have no labels yet: point to the section.

## Section 4.1, Datasets and metrics

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Two benchmarks; the clients hold the training set of one, the model is evaluated on that benchmark's evaluation set. BIRD is the main dataset: every baseline and every ablation is run on it. Spider: the same main comparison, and the breadth experiments (RQ2, RQ3) | facts below | BIRD numbers are on BIRD dev because its test set is not public: said plainly, once. No set is called held-out; nothing on how a setting was chosen |
| 2 | Databases of training and evaluation sets are disjoint in both benchmarks, so every evaluation question is on a database no client has seen | the benchmarks | as stated |
| 3 | RQ3 sets: Spider dev and three sets derived from it | facts below | "perturbed", not "robustness benchmark" as a claim about the method |
| 4 | EX: a prediction is correct when its execution result equals that of the gold SQL query on the database of the question; each benchmark with its own comparison and time limit. The query is read from the output of the model by one fixed rule, the same in evaluation and in the labeling of Section 3.4 | facts below | as stated |
| 5 | TS: stricter than EX, the same comparison on many databases; reported where test suites exist | facts below | as stated |
| 6 | Training questions for which a preference round constructs no pair in any round (Section 3.4 names the two kinds): how many | facts below | they stay in the training set of the warm-up rounds and of every SFT baseline; no judgement on the benchmarks |

### Facts

| Item | Fact |
|---|---|
| BIRD (`li2023bird`) | train: `\fact{split.bird.a0.1.k5.questions}` questions on `\fact{split.bird.a0.1.k5.databases}` databases; evaluation on BIRD dev, `\fact{questions.bird}` questions. Each question comes with external knowledge (a sentence or formula from the annotators), which is part of the prompt in training and evaluation. Dev questions carry a difficulty level: simple, moderate, challenging |
| Spider (`yu2018spider`) | train: `\fact{split.spider.a0.1.k5.questions}` questions on `\fact{split.spider.a0.1.k5.databases}` databases; evaluation on Spider test, `\fact{questions.spider}` questions. Difficulty levels from the Spider evaluation script: easy, medium, hard, extra hard |
| RQ3 sets | Spider dev, `\fact{questions.spiderdev}` questions. Spider-Syn (`gan2021spidersyn`), `\fact{questions.syn}`: the dev questions with schema-related words replaced by synonyms. Spider-Realistic (`deng2021realistic`), `\fact{questions.realistic}`: dev questions rewritten so that column names are not mentioned explicitly. Spider-DK (`gan2021spiderdk`), `\fact{questions.dk}`: questions that need domain knowledge |
| reading the query | from the output of the model: the content of a fenced code block if the output has one; the text up to the first semicolon; from the first `SELECT` (a leading `WITH` clause is kept). An output with no query fails to execute |
| EX on BIRD | benchmark's evaluation: the two results compared as sets of rows. One time limit of `\setting{timeout.bird}` for the prediction and the gold SQL query together |
| EX on Spider | comparison of the test-suite evaluation code (`zhong2020testsuite`): results equal as multisets of rows, up to a permutation of the columns; row order counts only when the gold SQL query has `ORDER BY`. `\setting{timeout.spider}` for each query |
| a prediction that fails to execute or exceeds the time limit | incorrect (an execution error, Section 3.4) |
| TS (`zhong2020testsuite`) | a prediction is correct when it matches the gold SQL query on every database of the test suite of its schema (many databases with the same schema and different content), in addition to the original one. Suites exist for the databases of Spider dev: reported on Spider dev, Spider-Syn, Spider-Realistic. None for Spider-DK, Spider test, BIRD |
| questions without pairs, Spider train | `\fact{train.spider.no_rows.databases}` of the training databases are distributed without rows; `\fact{train.spider.no_rows}` questions are on them. The gold SQL query of `\fact{train.spider.gold_error}` further questions fails to execute |
| questions without pairs, BIRD train | every database has rows. The gold SQL query of `\fact{train.bird.gold_error}` questions fails to execute; that of `\fact{train.bird.gold_timeout.pref1}` and `\fact{train.bird.gold_timeout.pref2}` more exceeds the time limit in the first and the second preference round |

## Section 4.2, Federated setups

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Clients are built from the training set of a benchmark: every database goes whole to one client with all its questions, so no two clients share a database (an organisation owns its databases) | the recipe below | a simulation of clients from a public benchmark; not "realistic", not a claim about real organisations |
| 2 | Non-IID by query complexity: the databases are partitioned with a Dirichlet distribution over complexity tiers; smaller $\alpha$, more skew. The clients then differ in the complexity of their queries, in size and in databases | recipe; Table 2 | what Table 2 shows, as ranges; no claim on the kind of heterogeneity beyond these three |
| 3 | Five setups (Table 2). Main setup on each benchmark: $K$ = 5, $\alpha$ = 0.1. For RQ2, three more on Spider train: $\alpha$ = 0.5 with 5 and with 10 clients, and IID with 5 | Table 2 | all clients take part in every round, in every setup |

### The recipe

| Step | Fact |
|---|---|
| complexity of a question | the hardness level of its gold SQL query by the criteria of Spider (easy, medium, hard, extra hard); the same criteria applied to the gold SQL queries of BIRD train, which has no levels |
| tier of a database | one of four, by its share of hard and extra hard questions (quartiles over the databases) |
| partition | for each tier, client proportions drawn from $\mathrm{Dir}(\alpha)$ and the databases of the tier assigned by them (`hsu2019noniid`: Dirichlet partition by label; here the label is the tier and the unit a database). A client that already holds $1/K$ of the databases receives no more |
| small clients | the partition is drawn again until every client holds at least 5 databases (3 with ten clients) |
| IID | databases assigned uniformly at random, the same number to each client |
| seed of the partitions | `\setting{split.seed}` |
| centralized training | the union of the clients' data: the whole training set |

### Table 2

In a `table` environment: `\caption{...}\label{tab:setups}` above,
then `\input{generated/tab_setups}`; the caption is yours, no full stop
at its end. Do not retype its numbers; a number of the table quoted in
the text goes through its macro (`generated/numbers.md`, the
`split.*` facts).

| Column | Meaning |
|---|---|
| Clients' data | the training set the clients hold |
| Partition | $\alpha$ of the Dirichlet partition, or IID |
| Clients | $K$ |
| Questions: All, Per client | size of the training set; smallest to largest client |
| Databases: All, Per client | the same for databases |
| Hard or extra (%) | share of hard and extra hard questions at a client, smallest to largest |

Main setups, for the text: BIRD, clients of
`\fact{split.bird.a0.1.k5.q_min}` to `\fact{split.bird.a0.1.k5.q_max}`
questions, `\fact{split.bird.a0.1.k5.hard_min}`\% to
`\fact{split.bird.a0.1.k5.hard_max}`\% hard or extra hard; Spider,
`\fact{split.spider.a0.1.k5.q_min}` to
`\fact{split.spider.a0.1.k5.q_max}`,
`\fact{split.spider.a0.1.k5.hard_min}`\% to
`\fact{split.spider.a0.1.k5.hard_max}`\%.

## Section 4.3, Models

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Main model: `\setting{model}` (`hui2024qwen25coder`), a code language model of 1.5 billion parameters: a size a client can fine-tune and serve itself | the setting of the paper | no comparison with larger models, no "state of the art" |
| 2 | RQ2: two more models, `\setting{models.other}` (the second: `guo2024deepseekcoder`): a smaller model of the same family and a model of another family | | as stated |
| 3 | For every model: pretrained weights frozen, a LoRA adapter trained (Section 3.1); the same settings for the three models; each model with its own chat format | committed configs | as stated |

## Section 4.4, Baselines

Every row is the same model, prompt and decoding; the federated rows
have the same clients and the same number of rounds, $T$ =
`\setting{rounds.total}`. Each baseline with the question it answers.

| Baseline | What it is | What it answers |
|---|---|---|
| No training | the pretrained model | the starting point |
| Local SFT | each client fine-tunes alone on its own data, `\setting{central.epochs}` epochs; mean, minimum and maximum over the clients | what a client reaches without federation |
| Centralized SFT | SFT on the union of the clients' data, `\setting{central.epochs}` epochs | training without the constraint of the setting; not possible when data cannot be pooled |
| FedAvg SFT (`mcmahan2017fedavg`) | $T$ rounds of the warm-up round of Section 3.3; the main baseline. `\method` is this baseline with its last `\setting{rounds.pref}` rounds replaced by preference rounds | the gain of the preference rounds at equal rounds |
| FedProx SFT (`li2020fedprox`) | FedAvg SFT with a proximal term in the local loss that keeps the client model close to the global model; coefficient `\setting{fedprox.mu}` | whether a remedy for non-IID clients closes the gap |
| FedDPO (`ye2024openfedllm`) | federated DPO as published: preference pairs fixed for all rounds, one reference model for all rounds, no NLL term. Here: after the same `\setting{rounds.warmup}` warm-up rounds, `\setting{rounds.pref}` rounds of it; the pairs are those of the first preference round of `\method` (the task has no human preference data, so the pairs come from the execution labels of Section 3.4), the reference model is the global model after the warm-up rounds | what on-policy pairs and the NLL term add to DPO in federated averaging |

Ceiling: designs only. No sentence anticipates how a baseline
performs. FedDPO: say what is taken from OpenFedLLM (fixed pairs, fixed
reference, no NLL term) and what is ours in running it (pairs from
execution labels, the warm-up rounds before it).

## Section 4.5, Implementation

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | One prompt in training, sampling and evaluation, for every method and model: that of the evaluation code of Qwen2.5-Coder for the two benchmarks. Printed in Appendix A (`app:prompt`, Fig. `fig:prompt`) | facts below | as stated |
| 2 | Adapter and local training: the values below; all settings in Appendix B (`app:settings`, Table `tab:settings`) | macros | the text names the main values and points to the table for the rest; no list of every setting |
| 3 | Preference rounds: the values named in Section 3.4, not repeated; here only what Section 3 left out (learning rate, optimizer) | macros | as stated |
| 4 | Evaluation: greedy decoding, one output per question | macros | as stated |
| 5 | One training seed for every row; the two main rows on BIRD (FedAvg SFT and `\method`) are also trained with a second seed | CLAIMS | the paper does not report variance over seeds |
| 6 | Simulation on one GPU: the clients of a round train one after another | macros | the times of Section 5 are sums over the clients, not the wall-clock time of a federation (said there) |

### Facts

| Item | Fact |
|---|---|
| prompt | one user message in the chat format of the model: the schema of the database as `CREATE TABLE` statements, a line naming SQLite, the question, a request for the SQL query alone. Spider: each `CREATE TABLE` statement is followed by three example rows of its table, and no external knowledge. BIRD: no example rows; the external knowledge of the question precedes the question. Layout and wording: the Text-to-SQL evaluation code released with Qwen2.5-Coder (`hui2024qwen25coder`), which renders the two benchmarks in these two ways; `chang2023prompt` may be cited for `CREATE TABLE` text with example rows as a prompt format |
| training target | the gold SQL query alone |
| sequence length | prompts are not truncated; limit `\setting{max_len}` |
| adapter | `\setting{lora}` (`hu2022lora`), on the attention and feed-forward projection matrices of every layer; `\setting{adapter.mb}` |
| warm-up round and every SFT baseline | AdamW (`loshchilov2019adamw`), learning rate `\setting{sft.lr}`, cosine schedule, `\setting{sft.batch}` examples per update, `\setting{sft.epochs}` local epoch per round |
| preference round | learning rate `\setting{pref.lr}`, `\setting{pref.batch}` pairs per update, `\setting{pref.epochs}` local epoch |
| decoding in evaluation | greedy, at most `\setting{eval.tokens}` new tokens, no repetition penalty |
| generation engine | vLLM (`kwon2023vllm`) for sampling and for evaluation |
| hardware | one `\setting{hw.gpu}` |
| seed | training seed `\setting{seed}`: the order of the training examples and the sampling of the preference rounds; the partitions keep their own seed. The second seed has no macro yet: "a second seed", no number |

## Section 4.6, Statistical test

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Two rows are compared on the same evaluation questions with the exact McNemar test on their paired predictions (`mcnemar1947note`; `dietterich1998tests` for its use in comparing two trained models from one run each): the test uses the questions that one model answers correctly and the other does not | the generator of the tables | the test covers the sample of evaluation questions; it is not presented as covering variation between training runs |
| 2 | Holm correction (`holm1979simple`) inside each table: the tests of a table answer one question and form one family; a test is counted once, in the first table that prints it; the comparisons quoted only in the text form a family of their own | CLAIMS, section 7, item 1 | as stated |
| 3 | A difference is called significant at `\fact{test.alpha}` after the correction; the tables mark these with an asterisk and print the unadjusted p | the generator | as stated |

## The two appendices

The listings and the table are in place; you add the text around them
and change nothing else in the two files.

| File | Yours | Facts |
|---|---|---|
| `sections/A_prompt.tex` | one or two lead-in sentences at the `%% LEAD-IN` line (at most 50 words) and the `\caption{}` of Fig. `fig:prompt`, no full stop at its end | (a) the prompt of a question of BIRD dev, (b) of a question of Spider test, as the model receives them as the user message; `[...]` stands for the `CREATE TABLE` statements of the other tables of the database (in (b) each with its example rows). The chat format of the model wraps the message and adds its default system message |
| `sections/B_settings.tex` | one lead-in sentence at the `%% LEAD-IN` line and the `\caption{}` of Table `tab:settings` | every setting of the experiments, read from the configurations of the runs; software with version and maker |

## Macros

Text mode unless noted. A macro that prints `??` waits for its run and
stays as it is.

| Macro | Prints |
|---|---|
| `\setting{model}`, `\setting{models.other}` | Qwen2.5-Coder-1.5B-Instruct; Qwen2.5-Coder-0.5B-Instruct, DeepSeek-Coder-1.3B-Instruct |
| `\setting{lora}`, `\setting{lora.r}`, `\setting{lora.alpha}` | LoRA, rank 16, $\alpha$ 32; 16; 32 |
| `\setting{adapter.mb}` | 73.9 MB |
| `\setting{max_len}` | 7,168 tokens, no truncation |
| `\setting{rounds.total}`, `\setting{rounds.warmup}`, `\setting{rounds.pref}` | 4, 2, 2 (math mode allowed) |
| `\setting{central.epochs}` | 3 |
| `\setting{sft.lr}`, `\setting{sft.batch}`, `\setting{sft.epochs}` | $2\times10^{-4}$, 16, 1 |
| `\setting{pref.lr}`, `\setting{pref.batch}`, `\setting{pref.epochs}` | $5\times10^{-5}$, 16, 1 |
| `\setting{fedprox.mu}` | ?? (waits) |
| `\setting{eval.tokens}` | 256 |
| `\setting{timeout.bird}`, `\setting{timeout.spider}` | 30 s, 60 s |
| `\setting{seed}`, `\setting{split.seed}` | 0, 42 |
| `\setting{hw.gpu}` | NVIDIA RTX A5000, 24 GB |
| `\fact{questions.bird}`, `.spider`, `.spiderdev`, `.syn`, `.realistic`, `.dk` | 1,534; 2,147; 1,034; 1,034; 508; 535 |
| `\fact{split.bird.a0.1.k5.questions}`, `.databases`, `.q_min`, `.q_max`, `.hard_min`, `.hard_max` | 9,428; 69; 683; 3,059; 25; 58 |
| `\fact{split.spider.a0.1.k5.questions}`, `.databases`, `.q_min`, `.q_max`, `.hard_min`, `.hard_max` | 8,659; 146; 734; 3,479; 20; 60 |
| `\fact{train.spider.no_rows.databases}`, `\fact{train.spider.no_rows}`, `\fact{train.spider.gold_error}` | 7; 1,759; 3 |
| `\fact{train.bird.gold_error}`, `\fact{train.bird.gold_timeout.pref1}`, `.pref2` | 350; 87; 92 |
| `\fact{test.alpha}` | 0.05 |

## References

| Key | Facts |
|---|---|
| `li2023bird` | BIRD: a cross-domain Text-to-SQL benchmark with large databases and external knowledge per question; its test set is not public |
| `yu2018spider` | Spider: a cross-domain Text-to-SQL benchmark; databases disjoint between its training, development and test sets |
| `gan2021spidersyn`, `deng2021realistic`, `gan2021spiderdk` | Spider-Syn, Spider-Realistic, Spider-DK, as in the facts of 4.1 |
| `zhong2020testsuite` | test-suite accuracy; its evaluation code is the comparison of execution results used for Spider here |
| `hsu2019noniid` | the Dirichlet partition by label for non-IID federated data; smaller concentration, more skew |
| `hui2024qwen25coder` | Qwen2.5-Coder, a family of code language models; its released evaluation code holds the Text-to-SQL prompt used here |
| `guo2024deepseekcoder` | DeepSeek-Coder, a family of code language models |
| `mcmahan2017fedavg` | FedAvg |
| `li2020fedprox` | FedProx: a proximal term added to the local objective, for heterogeneous clients |
| `ye2024openfedllm` | OpenFedLLM: federated fine-tuning of language models, among its methods DPO as the local training of FedAvg (FedDPO) on a fixed preference dataset |
| `hu2022lora`, `loshchilov2019adamw`, `kwon2023vllm` | LoRA; AdamW; vLLM |
| `mcnemar1947note`, `dietterich1998tests`, `holm1979simple` | McNemar's test; its use for comparing two classifiers trained once; the Holm correction |
| `chang2023prompt` | a study of prompt formats for Text-to-SQL: `CREATE TABLE` text with example rows |

## Labels available

Of this section: `sec:setup`, `sec:datasets`, `sec:fed-setups`,
`sec:models`, `sec:baselines`, `sec:implementation`, `sec:stat-test`,
`tab:setups`; of the appendices: `app:prompt`, `fig:prompt`,
`app:settings`, `tab:settings`.

Of other sections: `sec:method`, `sec:setting`, `sec:overview`,
`sec:warmup`, `sec:pref-round`, `sec:cost`, `alg:method`, `eq:loss`,
`sec:results`, `sec:ablation`, `sec:discussion`. The tables and
subsections of Sections 5 and 6 have no labels yet.

## Paragraph roles (an offer)

For a setup section: what is used and why it suits the question, then
the detail a reader needs to repeat it, with the appendix for the rest.
Datasets before metrics; for each baseline, what it is and what the
comparison with it shows; the implementation as values, not as a
narrative of the runs.
