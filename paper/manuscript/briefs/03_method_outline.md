# Outline: Section 3, Method

One line per paragraph, in order. "Serves" names the statement of the
brief (subsection.number). Words are running text; displayed equations,
Algorithm 1 and the caption of Fig. 1 are not counted. Total 1,485.

No paragraph stands between `\section{Method}` and Section 3.1: the
overview of Section 3.2 does the work of an opening.

## 3.1 Setting and notation (270)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Parties and data. $K$ clients and a server; client $k$ holds $\mathcal{D}_k$, $n_k$ triples $(q, d, y^\star)$, and the databases themselves, which it can query; the server holds no data and no database. That the data cannot be pooled is the premise of the setting | 3.1.1 | $K$, $k$, $\mathcal{D}_k$, $n_k$, $(q, d, y^\star)$ | 65 |
| 2 | Model and input. A pretrained language model with frozen weights; the LoRA adapter $\theta$ is the only part that is trained and exchanged; $\pi_\theta$. The prompt $x$ is constructed from $q$ and the schema of $d$ and is the same in training, sampling and evaluation (Appendix A); the output is the SQL query alone. $\log \pi_\theta(y \mid x)$ and $\lvert y \rvert$ defined here, once, for the losses of 3.3 and 3.4 | 3.1.2 | $\theta$, $\pi_\theta$, $x$, $\log \pi_\theta(y \mid x)$, $\lvert y \rvert$; `hu2022lora`; `app:prompt` | 85 |
| 3 | Protocol. $T$ rounds with all $K$ clients in each: the server sends $\theta^{t-1}$, each client trains locally to $\theta_k^{t}$, the server aggregates to $\theta^{t}$. $\theta^{0}$ is identical at all clients and $\pi_{\theta^{0}}$ is the pretrained model. The first $T_w$ rounds are warm-up rounds, the remaining ones preference rounds; $\pi_{\theta^{T}}$ is the model that is evaluated. The values of $T$ and $T_w$ named once, with a pointer to Section 4 | 3.1.3 | $T$, $T_w$, $\theta^{t}$, $\theta_k^{t}$, $\theta^{0}$; `mcmahan2017fedavg`; `\setting{rounds.total}`, `\setting{rounds.warmup}`; `sec:setup` | 80 |
| 4 | What crosses the boundary of a client: per round its adapter and one integer, the aggregation weight. Questions, gold SQL queries, databases and everything derived from them stay at the client | 3.1.4 | | 40 |

## 3.2 Overview (180)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The idea. A client holds databases as well as questions with gold SQL queries. FedAvg SFT takes the gold SQL query as its only target and never uses the databases. `\method` in addition executes the samples of the model on the client's database and learns from which of them reproduce the execution result of the gold SQL query. Such labeling is possible only at the client, where the databases stay | 3.2.1, 3.2.2 | | 85 |
| 2 | The stages and the round, read from Fig. 1. $T_w$ warm-up rounds (3.3), then $T - T_w$ preference rounds (3.4), one global model at the end. In a preference round a client samples, executes and labels, constructs pairs and trains; the server aggregates as in a warm-up round. The next round samples from the new global model, so each federated round renews samples, labels and pairs, and the communication of FedAvg is unchanged (3.5) | 3.2.3, 3.2.4 | Fig. 1 (`fig:overview`) and its caption; `sec:warmup`, `sec:pref-round`, `sec:cost` | 95 |

## 3.3 Warm-up rounds (180)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | A warm-up round is a round of FedAvg SFT. Local training starts from $\theta^{t-1}$ and minimizes, for `\setting{sft.epochs}` epoch over $\mathcal{D}_k$, the negative log-likelihood of the gold SQL query given the prompt, averaged over the tokens of the query; the prompt tokens carry no loss. The client uploads $\theta_k^{t}$ and $n_k$; the server averages the adapters with weights proportional to $n_k$, matrix by matrix. After $T_w$ rounds, $\theta^{T_w}$ is where the preference rounds start | 3.3.1 | Eq. `eq:sft` (the SFT loss); Eq. `eq:aggregation` (the weighted average, $w_k = n_k / \sum_j n_j$), the one statement of the rule in the section; `mcmahan2017fedavg` | 80 |
| 2 | Why the preference rounds do not start from the pretrained model. A preference round draws supervision only from questions with at least one correct and one incorrect sample; for a question whose samples are all incorrect the gold SQL query is the only supervision available, and a warm-up round uses the gold SQL query of every question. The number of warm-up rounds is ablated in Section 6 | 3.3.2 | `sec:ablation` | 60 |
| 3 | What a warm-up round leaves unused: one target per question, databases that are never queried, no signal on which of the model's own queries are incorrect. A preference round adds these (bridge to 3.4) | 3.3.3 | | 40 |

## 3.4 A preference round (675)

The earlier draft, kept in its order and its paragraphs. Each line says
what changes against it.

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | What a preference round trains: the model prefers, among its own samples, those that reproduce the execution result of the gold SQL query on the client's database. In round $t$, $T_w < t \le T$, the server sends $\theta^{t-1}$ to all clients. Change: the contrast with a warm-up round is shortened, since 3.3 par. 3 now makes it | lead to 3.4.1 | Algorithm 1 (`alg:method`) | 40 |
| 2 | Sampling and labeling. $N$ samples per question from $\pi_{\theta^{t-1}}(\cdot \mid x)$, with the decoding values; $y^\star$ executed once and every sample on $d$; a sample is correct iff its execution result equals that of $y^\star$, compared as the execution accuracy of the benchmark compares them. Two kinds of incorrect sample: one whose execution raises an execution error, one that returns an incorrect result. No SQL query in the sample: incorrect; truncated at the token limit: not labeled, enters no pair. The label needs the gold SQL query and the database, so only the client can compute it. Change: editor's note 1 | 3.4.1 | $N$, $\mathrm{exec}(y, d)$; `\setting{pref.samples}`, `\setting{pref.t}`, `\setting{pref.tokens}` | 140 |
| 3 | Pair construction. For each question with both labels, $M$ pairs $(y^{+}, y^{-})$, each element drawn uniformly over the samples of its label as generated; without replacement when the question has at least $M$ samples of that label. $\mathcal{P}_k^{t}$ is the set of these pairs. Why $M$ = `\setting{pref.pairs}`: $M$ sets the length of local training, at most four times the training sequences of a warm-up round (3.5). Both elements are samples of $\pi_{\theta^{t-1}}$, so the signal is on errors the current global model makes. Changes: editor's note 3; the reason for $M$ added; $\mathcal{P}_k^{t}$ defined, which the earlier draft used without defining | 3.4.2 | $M$, $y^{+}$, $y^{-}$, $\mathcal{P}_k^{t}$; `\setting{pref.pairs}`; `sec:cost` | 115 |
| 4 | Questions that yield no pair: all samples of one label; a database whose tables contain no rows; a gold SQL query that fails to execute. The first case can change, and such a question may yield pairs in a later round; the other two are fixed by the data. Change: editor's note 2 | 3.4.2 | | 45 |
| 5 | The loss. Local training starts from $\theta^{t-1}$ and minimizes two terms: a preference term on the log-likelihood ratio of the correct over the incorrect sample relative to a reference model, and an NLL term on the correct sample, which is $\lambda$ times the loss of a warm-up round with $y^{+}$ in place of $y^\star$. The client minimizes the mean over $\mathcal{P}_k^{t}$ for `\setting{pref.epochs}` epoch, which yields $\theta_k^{t}$. Change: the definition of $\log \pi$ and $\lvert y \rvert$ leaves (now in 3.1); the NLL term refers to Eq. `eq:sft` | 3.4.3 | Eq. `eq:logratio`, Eq. `eq:loss`; $\beta$, $\lambda$, $\pi_{\mathrm{ref}}$, $\sigma$; `\setting{pref.epochs}`, `\setting{pref.beta}`, `\setting{pref.nll}` | 80 |
| 6 | The reference model and the role of each term. The preference term is the DPO loss, $\beta$ the strength of the constraint toward the reference model. $\pi_{\mathrm{ref}} = \pi_{\theta^{t-1}}$: it generated the samples, as DPO takes its reference when that model is available, and it is the same model at all clients, the one they start from and the aggregate replaces; $m_\theta = 0$ at the start; fixed during the round, so its log-probabilities are computed once and no second model is held during training. The NLL term: $m_\theta$ depends only on the difference of the two log-ratios and can grow while the likelihood of $y^{+}$ falls; the NLL term acts on that likelihood itself. Both terms ablated in Section 6. Change: the reason for the NLL term stated as the brief gives it | 3.4.3 | `rafailov2023dpo`; `sec:ablation` | 105 |
| 7 | Relation to CodeLutra, a centralized method. Followed: $N$, the temperature, uniform pairing, $\beta$, $\lambda$, the reference model being the model that generated the samples. Different: fewer pairs per question (the reason is in par. 3) and the NLL term averaged over tokens | closest work (References of the brief) | `tao2024codelutra` | 45 |
| 8 | On-policy pairs. Sampling, labeling and pair construction are repeated in every preference round from that round's global model, so the pairs follow the current errors of the model and the set of questions that yield pairs changes from round to round; FedDPO, in one clause, constructs its pairs once. Counts per round in Section 5, ablation in Section 6. Change: the counts of questions and pairs leave | 3.4.4 | `ye2024openfedllm`; `sec:results`, `sec:ablation` | 50 |
| 9 | Upload and aggregation. The client uploads $\theta_k^{t}$ and $\lvert\mathcal{P}_k^{t}\rvert$; the server applies Eq. `eq:aggregation` with the number of pairs in place of $n_k$; a client without pairs has weight zero and does not train in that round. Samples, execution results, execution labels and pairs stay at the client. Change: the displayed equation moves to 3.3 and the weight is given inline here; the size of the upload leaves (3.5) | 3.4.5 | inline $w_k = \lvert\mathcal{P}_k^{t}\rvert / \sum_j \lvert\mathcal{P}_j^{t}\rvert$; ref. to `eq:aggregation` | 55 |

## 3.5 What a round costs a client (180)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | Communication is that of FedAvg SFT: in a round of either kind a client receives and sends one adapter of the same size, and sends one integer | 3.5.1 | `\setting{adapter.mb}` | 45 |
| 2 | What a preference round adds is computation at the client, of three kinds. Generation: $N n_k$ samples, inference only. Execution: at most $N + 1$ queries per question, each bounded by the time limit, on the client's own databases and without a GPU. Training on pairs: one pass of the reference model without gradient, then two sequences per pair, at most $2 M n_k$ against the $n_k$ of a warm-up round, and fewer in practice, since only questions with both labels yield pairs. The measured times and the counts per round are in Section 5 | 3.5.2 | `\setting{pref.tokens}`; `sec:results` | 100 |
| 3 | The server is unchanged: a weighted average, no data, no query executed. The one new requirement falls on the client, which must execute SQL queries on its own databases besides fine-tuning the model | 3.5.3 | | 35 |

## Floats

| Float | Plan |
|---|---|
| Fig. 1 | After 3.2 par. 2. Caption: names the two stages and the four steps of a preference round at a client, and says that only adapters travel between server and client; no full stop at its end |
| Algorithm 1 | Beside 3.4, first cited in 3.4 par. 1. One loop over $t = 1, \dots, T$ with a branch on $t \le T_w$; the client steps of a preference round as four lines (sample, label, construct pairs, train); one line for the upload and one for the weighted average, citing Eq. `eq:aggregation`. Caption: the name of the method |

## For the editor

1. The aggregation rule is displayed once, in 3.3, with $w_k$ from
   $n_k$; 3.4 gives the weight of a preference round inline. The earlier
   draft displayed it in 3.4. The other order (rule in 3.4, 3.3 in words
   only) leaves 3.3 without the formula it defines.
2. The values of $T$ and $T_w$ are named in 3.1 par. 3, where the
   symbols are defined. Fig. 1 prints "2 FedAvg rounds" and "$N$ = 10"
   as typed digits, so it will not follow a change of the settings.
3. 3.4 par. 2 covers two steps (sampling, labeling) in 140 words and
   par. 6 two subjects (the reference model, the NLL term). I keep both
   as the earlier draft has them; each would split cleanly if you
   prefer shorter paragraphs.
4. The earlier draft runs to about 775 words. With the counts, the
   definition of $\log \pi$, the displayed aggregation and the size of
   the upload removed, and the reason for $M$, the definition of
   $\mathcal{P}_k^{t}$ and the client without pairs added, 3.4 is
   planned at 675 and may land near 700, under the limit of 750.
5. Left out of 3.1 for length: that the prompt of BIRD carries the
   external knowledge of a question ($q$ read to include it; Section 4
   and Appendix A state it), and the layout of the prompt beyond "the
   question and the schema" (Appendix A prints it).
6. 3.5 stays prose. The brief's comparison of the two kinds of round
   would also fit a seven-row table, but Section 5 has the cost table
   and the pages are limited.
