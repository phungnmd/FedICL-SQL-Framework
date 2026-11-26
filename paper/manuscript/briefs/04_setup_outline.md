# Outline: Section 4, Experimental setup

One line per paragraph, in order. "Serves" names the statement of the
brief (subsection.number; for 4.4 the row of its table). Words are
running text; the caption of Table 2 and the text of the appendices are
not counted. Total 1,125.

## Opening (85)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The experiments answer four research questions, stated once as one running sentence with the tags RQ1 to RQ4: the gain over FedAvg SFT and the other baselines at the same number of rounds; whether it carries over to other models and other federated setups; whether it holds on perturbed questions and under test-suite accuracy; what changes in the queries the model generates and what a round costs a client. Section 5 follows this order; Section 6 then removes the parts of the method one at a time. No result, no direction | opening table of the brief | `\method`; `sec:results`, `sec:ablation` | 85 |

## 4.1 Datasets and metrics (265)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Two benchmarks; in each, the clients hold the training set and the model is evaluated on the evaluation set of the same benchmark. BIRD is the main dataset: training questions and databases, BIRD dev since its test set is not public (said once), external knowledge per question as part of the prompt; every baseline and every ablation is run on it. Spider: training questions and databases, Spider test; the main comparison again, and the experiments of RQ2 and RQ3. Training and evaluation databases are disjoint in both, so every evaluation question is on a database no client has seen | 4.1.1, 4.1.2 | `li2023bird`, `yu2018spider`; `\fact{split.bird.a0.1.k5.questions}`, `.databases`, `\fact{questions.bird}`; `\fact{split.spider.a0.1.k5.questions}`, `.databases`, `\fact{questions.spider}` | 80 |
| 2 | The sets of RQ3: Spider dev and three sets derived from it, each with what was changed in the questions (synonyms for schema-related words; column names no longer mentioned explicitly; domain knowledge required). "Perturbed" as a description of the questions | 4.1.3 | `gan2021spidersyn`, `deng2021realistic`, `gan2021spiderdk`; `\fact{questions.spiderdev}`, `.syn`, `.realistic`, `.dk` | 40 |
| 3 | EX. A prediction is correct when its execution result equals that of the gold SQL query on the database of the question. The query is read from the output of the model by one fixed rule (code block if present, text up to the first semicolon, from the first `SELECT` with a leading `WITH` kept); an output with no query, a prediction that fails to execute or one that exceeds the time limit is incorrect. Each benchmark with its own comparison and time limit: BIRD, results as sets of rows, one limit for prediction and gold SQL query together; Spider, the comparison of the test-suite evaluation code (multisets of rows up to a permutation of columns, row order only under `ORDER BY`), a limit for each query. Last sentence closes the pointer of Section 3.4: the same rule, comparison and limits produce the execution labels | 4.1.4 | `zhong2020testsuite`; `\setting{timeout.bird}`, `\setting{timeout.spider}`; `sec:pref-round` | 85 |
| 4 | TS. Stricter than EX: the prediction must match the gold SQL query on every database of the test suite of its schema, many databases with the same schema and different content. Reported where suites exist: Spider dev, Spider-Syn, Spider-Realistic; none for Spider-DK, Spider test and BIRD | 4.1.5 | `zhong2020testsuite` | 30 |
| 5 | Training questions that yield no preference pair (the two kinds of Section 3.4), as counts. Spider train: databases distributed without rows and the questions on them, plus the gold SQL queries that fail to execute. BIRD train: every database has rows; gold SQL queries that fail to execute, and those that exceed the time limit, the latter given per preference round. All these questions stay in the training set of the warm-up rounds and of every SFT baseline. Counts only, no judgement on the benchmarks | 4.1.6 | `\fact{train.spider.no_rows.databases}`, `\fact{train.spider.no_rows}`, `\fact{train.spider.gold_error}`, `\fact{train.bird.gold_error}`, `\fact{train.bird.gold_timeout.pref1}`, `.pref2`; `sec:pref-round` | 30 |

## 4.2 Federated setups (190)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | How clients are built. The clients are simulated from the training set of a benchmark: every database goes whole to one client with all its questions, so no two clients share a database, as an organization owns its databases. Stated as a simulation from a public benchmark | 4.2.1 | | 50 |
| 2 | The non-IID partition, by query complexity. Complexity of a question: the hardness level of its gold SQL query by the criteria of Spider, applied also to BIRD train, which has no levels. Each database falls into one of four tiers by its share of hard and extra hard questions (quartiles over the databases). For each tier, client proportions are drawn from $\mathrm{Dir}(\alpha)$ and the databases of the tier assigned by them: the label-distribution skew of NIID-Bench with the tier as label and a database as unit, including its cap at $1/K$ of the databases; smaller $\alpha$, more skew. Drawn again until every client holds at least 5 databases (3 with ten clients). IID setup: databases assigned uniformly at random, the same number to each client | 4.2.2 | `li2022niidbench`, `hsu2019noniid`; $\alpha$, $K$ | 95 |
| 3 | The five setups, read from Table 2. Main setup on each benchmark: $K = 5$, $\alpha = 0.1$; the clients then differ in size, in databases and in the complexity of their queries, shown by the ranges of questions and of the share of hard or extra hard questions on BIRD and on Spider. For RQ2, three more on Spider train: $\alpha = 0.5$ with 5 and with 10 clients, and IID with 5. All clients take part in every round, in every setup | 4.2.2, 4.2.3 | Table 2 (`tab:setups`); `\fact{split.bird.a0.1.k5.q_min}`, `.q_max`, `.hard_min`, `.hard_max`; the same four for `split.spider.a0.1.k5` | 45 |

## 4.3 Models (75)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The main model is a code language model of 1.5 billion parameters, a size a client can fine-tune and serve itself. For RQ2, two more: a smaller model of the same family and a model of another family. For all three the pretrained weights are frozen and a LoRA adapter is trained (Section 3.1), with the same settings; each model uses its own chat format | 4.3.1, 4.3.2, 4.3.3 | `\setting{model}`, `\setting{models.other}`; `hui2024qwen25coder`, `guo2024deepseekcoder`; `sec:setting` | 75 |

## 4.4 Baselines (215)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | What every row shares, so that a difference between two rows is a difference of training method: the same model, prompt and decoding; the federated rows also the same clients and the same number of rounds, $T$ | lead of 4.4 | `\setting{rounds.total}` | 35 |
| 2 | Three references outside federated training, each with what it shows. No training: the pretrained model, the starting point. Local SFT: each client fine-tunes alone on its own data for the stated epochs, reported as mean, minimum and maximum over the clients; what a client reaches without federation. Centralized SFT: SFT on the union of the clients' data, the whole training set, same epochs; training without the constraint of the setting, not available when the data cannot be pooled | rows No training, Local SFT, Centralized SFT | `\setting{central.epochs}` | 60 |
| 3 | The federated SFT baselines. FedAvg SFT: $T$ rounds of the warm-up round of Section 3.3, the main baseline; `\method` is this baseline with its last rounds replaced by preference rounds, so the comparison isolates the preference rounds at equal rounds. FedProx SFT: a proximal term in the local loss that keeps the client model close to the global model, with its coefficient; it tests whether a remedy for non-IID clients accounts for the difference | rows FedAvg SFT, FedProx SFT | `mcmahan2017fedavg`, `li2020fedprox`; `\setting{rounds.pref}`, `\setting{fedprox.mu}` (prints ??, waits); `sec:warmup` | 55 |
| 4 | FedDPO. Taken from OpenFedLLM: preference pairs fixed for all rounds, one reference model for all rounds, no NLL term. Ours in running it: the task has no human preference data, so the pairs are those of the first preference round of `\method`, from the execution labels of Section 3.4; it starts after the same warm-up rounds and runs for the same number of rounds, with the global model after the warm-up rounds as reference model. The comparison shows what on-policy pairs and the NLL term add to DPO in federated averaging | row FedDPO | `ye2024openfedllm`; `\setting{rounds.warmup}`, `\setting{rounds.pref}`; `sec:pref-round` | 65 |

## 4.5 Implementation (190)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The prompt. One prompt in training, sampling and evaluation, for every method and model: one user message with the schema as `CREATE TABLE` statements, a line naming SQLite, the question and a request for the SQL query alone. Layout and wording follow the Text-to-SQL evaluation code released with Qwen2.5-Coder, which renders the two benchmarks differently: Spider with three example rows after each statement, BIRD with the external knowledge before the question. Printed in Appendix A. The training target is the gold SQL query alone; prompts are not truncated | 4.5.1 | `hui2024qwen25coder`, `chang2023prompt`; `\setting{max_len}`; `app:prompt`, `fig:prompt` | 60 |
| 2 | Adapter and local training, as values. The LoRA configuration, on the attention and feed-forward projection matrices of every layer, with the size of the adapter. Warm-up rounds and every SFT baseline: AdamW, learning rate, cosine schedule, examples per update, one local epoch per round. Preference rounds: the values of Section 3.4 are not repeated; only the learning rate and the pairs per update are added. Appendix B lists every setting | 4.5.2, 4.5.3 | `hu2022lora`, `loshchilov2019adamw`; `\setting{lora}`, `\setting{adapter.mb}`, `\setting{sft.lr}`, `\setting{sft.batch}`, `\setting{sft.epochs}`, `\setting{pref.lr}`, `\setting{pref.batch}`; `app:settings`, `tab:settings` | 65 |
| 3 | Evaluation and the simulation. Greedy decoding, one output per question, the limit of new tokens, no repetition penalty; vLLM for sampling and for evaluation. The federation is simulated on one GPU, the clients of a round training one after another. One training seed for every row, which sets the order of the training examples and the sampling of the preference rounds; the two main rows on BIRD, FedAvg SFT and `\method`, are also trained with a second seed | 4.5.4, 4.5.5, 4.5.6 | `kwon2023vllm`; `\setting{eval.tokens}`, `\setting{hw.gpu}`, `\setting{seed}` | 65 |

## 4.6 Statistical test (105)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Two rows are compared on the same evaluation questions with the exact McNemar test on their paired predictions; the test uses only the questions that one model answers correctly and the other does not. Its use for two models trained once each follows Dietterich. What it measures is stated as it is: the difference over the sample of evaluation questions | 4.6.1 | `mcnemar1947note`, `dietterich1998tests` | 55 |
| 2 | Multiple comparisons. Holm correction inside each table, whose tests answer one question and form one family; a test is counted once, in the first table that prints it; the comparisons quoted only in the text form a family of their own. A difference is called significant at the stated level after the correction; the tables mark it with an asterisk and print the unadjusted p-value | 4.6.2, 4.6.3 | `holm1979simple`; `\fact{test.alpha}` | 50 |

## Floats

| Float | Plan |
|---|---|
| Table 2 (`tab:setups`) | In 4.2, after par. 2, first cited in par. 3. `table` environment, caption above, `\input{generated/tab_setups}`. Caption: the federated setups; "Per client" gives the smallest and the largest client; the last column is the share of hard and extra hard questions at a client; the first two rows are the main setups. No full stop at its end |

## The two appendices (written with the section)

| File | Plan |
|---|---|
| `sections/A_prompt.tex` | Lead-in, two sentences under 50 words: the figure prints the prompt as the model receives it, as the user message; the chat format of the model wraps the message and adds its default system message. Caption of `fig:prompt`: (a) the prompt of a question of BIRD dev, (b) of a question of Spider test; `[...]` stands for the `CREATE TABLE` statements of the other tables of the database, in (b) each with its example rows |
| `sections/B_settings.tex` | Lead-in, one sentence: the table lists every setting of the experiments, with the software and its versions. Caption of `tab:settings`: the settings of the experiments, read from the configurations of the runs; the software with version and maker |

## For the editor

1. Lengths. 4.1 is planned at 265 words against about 250 in the brief:
   six statements and the reading rule do not fit in less without
   dropping a fact a reader needs to repeat the evaluation. The 15
   words come from the opening, 4.3 and 4.6 (5 each). The total stays
   at 1,125.
2. The time limit and "no pair in any round" (4.1, par. 5). The counts
   of gold SQL queries of BIRD train that exceed the time limit differ
   between the two preference rounds, so these questions are not a
   fixed set. The paragraph gives the two fixed kinds (databases
   without rows, gold SQL queries that fail to execute) as questions
   that yield no pair in any round, and the time-limit counts as "in
   the first and in the second preference round". If one fixed number
   is wanted instead, the brief needs it.
3. Difficulty levels of the evaluation sets (simple, moderate,
   challenging on BIRD dev; easy to extra hard on Spider). The outline
   names the Spider criteria only in 4.2, where the partition needs
   them. If Section 5 reports EX by level, one clause in 4.1, par. 1,
   would introduce the levels of BIRD dev; it is left out for now to
   hold the length.
4. The seed of the partitions is in Table B and is left out of the text
   of 4.2. The cap at $1/K$ and the redraw for small clients are not in
   Table B, so they stay in the text of 4.2, par. 2.
5. The rule that reads the query (4.1, par. 3). The brief lists three
   steps without saying in which order they apply. The paragraph will
   give them in the order of the brief: the content of a fenced code
   block if there is one, then the text up to the first semicolon,
   then from the first `SELECT`, a leading `WITH` clause kept. Correct
   me if the code applies them otherwise.
6. Centralized training as "the union of the clients' data, the whole
   training set" is said in 4.4, par. 2, with the baseline, and not in
   4.2.
7. `\setting{fedprox.mu}` prints `??` and stays as it is. The second
   seed has no macro and is written as "a second seed".
8. The opening states the four questions in one running sentence with
   the tags RQ1 to RQ4, not as a list, to stay near 85 words. Sections
   4.1, 4.2 and 4.3 then refer to RQ2 and RQ3 by tag.
