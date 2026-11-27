# Brief: Section 3, Method

Kind of section: method (`VOICE_GUIDE.md`, Section 2).
Outline to: `briefs/03_method_outline.md`. Draft to:
`sections/03_method.tex`. Notes to: `briefs/03_method_notes.md`.
Earlier draft of Section 3.4: `pilot/3.4_preference_round.tex` (see the
block of Section 3.4).

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Headings | `\section{Method}\label{sec:method}`; `\subsection{Setting and notation}\label{sec:setting}`; `\subsection{Overview}\label{sec:overview}`; `\subsection{Warm-up rounds}\label{sec:warmup}`; `\subsection{A preference round}\label{sec:pref-round}`; `\subsection{What a round costs a client}\label{sec:cost}`. No heading below a subsection |
| Before it | Section 1: the problem, the idea, the contributions; SFT, FedAvg, DPO and LoRA given in full there. Section 2 (`sec:related`): earlier work, closing on Table 1, in which no earlier method has all the properties of `\method` |
| After it | Section 4 (`sec:setup`): datasets, client splits, models, baselines, every setting (optimizer, learning rates, LoRA rank, decoding); Appendix A (`app:prompt`): the prompt as the model receives it; Appendix B (`app:settings`): all settings in one table. Section 5 (`sec:results`): results, among them the measured cost of a round. Section 6 (`sec:ablation`): on-policy pairs, the two terms of the loss, the number of warm-up rounds, the aggregation weights. Section 7 (`sec:discussion`): limitations |
| Floats | Fig. 1 (`fig:overview`), referred to from Section 3.2. Algorithm 1 (`alg:method`), the whole method, set beside Section 3.4 |
| Purpose | The reader can reimplement the method from this section and knows the reason for each design choice. No result is reported here |
| Length | about 1,420 words of running text, 1,490 at most (lowered after the first draft: Fig. 1, Algorithm 1 and the displayed equations take more of the four pages of the section than planned). By subsection, about: 3.1 240, 3.2 150, 3.3 170, 3.4 740, 3.5 120. Displayed equations, Algorithm 1 and the caption of Fig. 1 are not counted; inline formulas are not counted as words |

## Section 3.1, Setting and notation

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Parties and data: $K$ clients and a server. Client $k$: private training set $\mathcal{D}_k$ of $n_k$ triples $(q, d, y^\star)$, and the databases themselves, which it can query. Server: no data, no database | definition | the data of a client cannot be pooled: a premise of the setting, not argued |
| 2 | Model: pretrained language model, weights frozen; a LoRA adapter $\theta$ is the only trained and exchanged part; $\pi_\theta$. Input: prompt $x$ from $q$ and the schema of $d$, identical in training, sampling and evaluation. Output: the SQL query alone | definition; `hu2022lora` | as stated |
| 3 | Protocol: $T$ rounds; in round $t$ the server sends $\theta^{t-1}$ to all $K$ clients, each trains locally to $\theta_k^{t}$, the server aggregates to $\theta^{t}$. The first $T_w$ rounds are warm-up rounds, the rest preference rounds. $\pi_{\theta^{T}}$ is the model that is evaluated | definition; `mcmahan2017fedavg` | full participation is the setting studied; nothing on partial participation |
| 4 | What crosses the boundary of a client: per round its adapter and one integer (the aggregation weight), and nothing else. Questions, gold SQL queries and databases stay, and so does what a preference round produces from them at the client: the samples, their execution results, the labels and the pairs. Not "everything derived from the data stays": the adapter and the integer are computed from the data and are sent | protocol | data isolation. Nothing on differential privacy, nothing on what an adapter reveals |

### Facts

| Item | Fact |
|---|---|
| a training example | $(q, d, y^\star)$: question, the database it refers to, gold SQL query. A client holds several databases |
| $x$ | schema of $d$ as `CREATE TABLE` statements, then $q$, then an instruction to return only the SQL query; one user message in the chat format of the model. Printed in full in Appendix A. Where a benchmark attaches external knowledge to a question (BIRD), it is part of the prompt: a detail of Section 4 and Appendix A, and $q$ may be read to include it |
| $\theta$ | all matrices of the LoRA adapter. Rank, adapted matrices and size: Section 4 and Appendix B |
| $\theta^{0}$ | the initial adapter, identical at all clients; $\pi_{\theta^{0}}$ is the pretrained model (a LoRA adapter at initialization leaves the output of the model unchanged) |
| $\log \pi_\theta(y \mid x)$, $\lvert y \rvert$ | sum of the log-probabilities of the tokens of $y$; number of tokens of $y$. Used by the losses of Sections 3.3 and 3.4 |
| participation | all $K$ clients in every round |
| values of $T$, $T_w$ | `\setting{rounds.total}`, `\setting{rounds.warmup}` (`\setting{rounds.pref}` preference rounds); Section 4 states them, and this section may name them once |
| notation | `TERMS.md`, "Notation". The symbols of the setting belong here; where the symbols of a preference round ($N$, $M$, $\mathrm{exec}$, $y^{+}$, $y^{-}$, $\mathcal{P}_k^{t}$, $\beta$, $\lambda$) are introduced is yours (the earlier draft of Section 3.4 introduces them in place) |

## Section 3.2, Overview

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | The idea. A client holds databases as well as questions with gold SQL queries. FedAvg SFT: the gold SQL query is the only target, the databases are never used, and there is no signal on which of the model's own queries are incorrect (the contrast is made here, once for the section). `\method` in addition: executes the samples of the model on the client's database, learns from which of them reproduce the execution result of the gold SQL query | the design | The label needs the gold SQL query: never "without gold SQL", "unlabelled", "self-supervised", never that execution alone establishes correctness |
| 2 | Execution-based labeling is possible only at the client: the databases stay there | setting (3.1) | as stated |
| 3 | Two stages: $T_w$ warm-up rounds (FedAvg SFT, Section 3.3), then $T - T_w$ preference rounds (Section 3.4). One global model results | Fig. 1, top | no result, no comparison here |
| 4 | A preference round at a client: sample, execute and label, construct pairs, train; the server aggregates as in a warm-up round. The next round samples from the new global model, so one federated round is one step of renewing samples, labels and pairs; the communication of FedAvg is unchanged | Fig. 1; Section 3.5 | "no added communication" as stated; cost of computation is Section 3.5 |

### Fig. 1

File to open: `../figures/fig_method_overview.png`. In the section:
`\includegraphics{figures/fig_method_overview.pdf}` in a `figure`
environment with `\label{fig:overview}`; the caption is yours, without
a full stop at its end (journal style).

| Part of the figure | Shows |
|---|---|
| strip at the top | the two stages in order (warm-up rounds, preference rounds), then the deployed global model |
| server band | the client adapters aggregated into the next global model; in a preference round weighted by the number of pairs |
| arrows between server and client | down: the global model of the round. Up: the adapter of the client. Nothing else crosses |
| client panel, dashed border | what stays at the client. Four numbered steps of a preference round: 1 sample ($N$ queries per question from the round's global model); 2 execute (each sample on the client's database, giving its execution label; drawn as one correct and two incorrect samples); 3 pair (the correct sample preferred over each incorrect one); 4 train (the adapter, preference term plus NLL term on the pairs, reference model = the round's global model) |
| note between the arrows | the next round samples again from the new global model |
| key at the bottom | three colors: federated averaging, steps of the method, private client data |

The figure uses the names and the notation of `TERMS.md`. Abbreviations
that appear inside it: FedAvg, SQL, LoRA, DPO, NLL. Its step 4 writes
the loss as $L = L_{\mathrm{DPO}} + L_{\mathrm{NLL}}$: the preference
term and the NLL term of Section 3.4.

## Section 3.3, Warm-up rounds

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | A warm-up round = a round of FedAvg SFT: local training on the gold SQL queries from $\theta^{t-1}$, aggregation weighted by $n_k$. After $T_w$ rounds: $\theta^{T_w}$, the start of the preference rounds | definition; `mcmahan2017fedavg` | as stated |
| 2 | Why the preference rounds do not start from the pretrained model: a preference round draws supervision only from questions with at least one correct and one incorrect sample. For a question whose samples are all incorrect the gold SQL query is the only supervision available, and a warm-up round uses the gold SQL query of every question. Why in earlier rounds: the first preference round then samples from a model that has been trained on the gold SQL query of every question, and fewer questions are left without a correct sample | follows from pair construction (Section 3.4); the questions without a correct sample at the first preference round are fewer after two warm-up rounds than from the pretrained model on both datasets (committed counts; Section 6 reports them and ablates the number of warm-up rounds) | a design reason and a count. No claim that warm-up rounds raise execution accuracy; no number here; point to Section 6. Not "more questions yield pairs": that holds on BIRD only |

### Facts

Checked against the code.

$$ \mathcal{L}_k^{\mathrm{SFT}}(\theta) = \frac{1}{n_k} \sum_{(q, d, y^\star) \in \mathcal{D}_k} -\frac{1}{\lvert y^\star \rvert} \log \pi_\theta(y^\star \mid x) $$

| Item | Fact |
|---|---|
| local training | initialized at $\theta^{t-1}$; `\setting{sft.epochs}` epoch over $\mathcal{D}_k$; result $\theta_k^{t}$ |
| loss | negative log-likelihood of the gold SQL query given the prompt, averaged over the tokens of the query; the prompt tokens carry no loss |
| aggregation | $\theta^{t} = \sum_k w_k \theta_k^{t}$, $w_k = n_k / \sum_j n_j$, applied to every matrix of the adapter. Same rule as in a preference round, where the weight is the number of pairs (equation of Section 3.4); one statement of the rule in the section is enough |
| upload | $\theta_k^{t}$ and $n_k$ |
| $T_w$ | `\setting{rounds.warmup}` |
| optimizer, learning rate, batch | Section 4 and Appendix B, not here |

## Section 3.4, A preference round

The earlier draft (`pilot/3.4_preference_round.tex`) is the accepted
text of this subsection, written before Sections 3.1 to 3.3 existed.
Revise it where the section, this brief or the notes below require it,
and leave the rest as it stands.

Editor's notes on the earlier draft:

1. "An incorrect sample is either an execution error, which fails to
   execute ...": a sample is a query, and the error is what its
   execution raises. The two kinds should read as kinds of incorrect
   sample.
2. "In the first case, the question is sampled again in the next
   preference round": every question is sampled in every preference
   round. What the reader needs is that such a question can yield
   pairs in a later round.
3. "at least $M$ samples of the label": of that label.

What changed around it: Sections 3.1 to 3.3 now define the setting, the
notation, the SFT loss and the aggregation with $n_k$; the size of the
upload is stated once, in Section 3.5; the counts of questions and
pairs per round are reported in Section 5, with the cost of a round,
and no longer here; a reason for the value of $M$ is given below; the
length asked for is lower than that of the earlier draft.

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Label = execution result of the sample against that of the gold SQL query, on the client's database. Only the client can compute it | definition | The label needs the gold SQL query: never "without gold SQL", "unlabelled", "self-supervised", never that execution alone establishes correctness |
| 2 | Pair = two samples of the model itself for one question, one correct, one incorrect: the signal is on errors the current model makes. A question with one label only: no pair this round, may yield pairs in a later one | pair construction | as stated |
| 3 | Loss = preference term + NLL term. Preference term: log-likelihood ratio of correct over incorrect sample, relative to a reference model. Reference model = the global model at the start of the round. NLL term on the correct sample | definition; both terms ablated in Section 6 | point to Section 6, no result here |
| 4 | On-policy pairs: every preference round samples all questions again from its own global model, so the pairs follow the current errors of the model, and the set of questions that yield pairs changes from round to round | by construction; ablated in Section 6; the counts per round are in Section 5 | no count and no result here; point to Sections 5 and 6 |
| 5 | Upload = adapter + number of pairs (the aggregation weight). Samples, execution results, labels and pairs stay at the client | protocol | data isolation; nothing on differential privacy or on what an adapter reveals |

### Facts

#### Preference round $t$, for $T_w < t \le T$

| Step | Actor | Operation | Values |
|---|---|---|---|
| 1 | server | sends $\theta^{t-1}$ to the clients | all $K$ clients |
| 2 | client | sampling: for each $(q, d, y^\star) \in \mathcal{D}_k$, $N$ samples from $\pi_{\theta^{t-1}}(\cdot \mid x)$ | $N$ = `\setting{pref.samples}`; temperature `\setting{pref.t}`; no top-$p$ or top-$k$ truncation; at most `\setting{pref.tokens}` new tokens |
| 3 | client | labeling: executes $y^\star$ once and every complete sample on $d$ (a truncated sample is not executed). A sample $y$ is correct iff $\mathrm{exec}(y, d) = \mathrm{exec}(y^\star, d)$, results compared as the execution accuracy of the benchmark compares them; otherwise incorrect | two kinds of incorrect sample: one whose execution raises an execution error (fails to execute, or exceeds the time limit), one that returns an incorrect result (executes, different result). The query is read from the output of the model in the same way as in evaluation, and the comparison of results is that of execution accuracy; Section 4 defines both. An empty sample (an output that holds no query text): incorrect. A sample truncated at the token limit: an incomplete query, not labeled, enters no pair. The value of the time limit is in Appendix B, not here |
| 4 | client | pair construction: for each question with at least one correct and one incorrect sample, $M$ pairs $(y^{+}, y^{-})$; $y^{+}$ uniform over its correct samples, $y^{-}$ uniform over its incorrect samples | $M$ = `\setting{pref.pairs}`. Why this value: $M$ sets the length of local training (at most $M n_k$ pairs, two training sequences each; Section 3.5), and $M$ = 2 bounds it at four times the sequences of a warm-up round; a reason of cost, nothing on accuracy at other values of $M$. Drawn over the samples as generated: a query generated three times is three times as likely. The $M$ correct and the $M$ incorrect samples are drawn independently of each other and paired in the order drawn. Without replacement when the question has at least $M$ samples of that label, with replacement otherwise, so a question with one correct and one incorrect sample yields the same pair $M$ times. The rule of replacement may be left to Appendix B |
| 5 | client | local training: initialized at $\theta^{t-1}$; `\setting{pref.epochs}` epoch over $\mathcal{P}_k^{t}$ with the loss below; result $\theta_k^{t}$ | |
| 6 | client | uploads $\theta_k^{t}$ and $\lvert\mathcal{P}_k^{t}\rvert$ | |
| 7 | server | aggregation: $\theta^{t} = \sum_k w_k \theta_k^{t}$, $w_k = \lvert\mathcal{P}_k^{t}\rvert / \sum_j \lvert\mathcal{P}_j^{t}\rvert$, applied to every matrix of the adapter | in a warm-up round $w_k \propto n_k$. In both kinds of round the weight is the amount of data the client trained on in that round. A client without pairs has $w_k = 0$ and does not train in that round. Section 6 compares these weights with others |

Questions that yield no pair in a round:

| Case | Reason | Over the rounds |
|---|---|---|
| all samples correct, or all incorrect | no pair of opposite labels exists | can change: all questions are sampled again in every preference round |
| the database holds no rows: none of its tables contains a row (a property of the database as released, not of the question or of the gold SQL query) | the comparison of execution results is uninformative there: without rows, queries that differ return the same result | fixed by the data |
| the gold SQL query fails to execute or exceeds the time limit | no label can be assigned | fixed by the data |

#### Loss of one pair $(x, y^{+}, y^{-})$

Checked against the code.

$$ m_\theta = \beta \left[ \log \frac{\pi_\theta(y^{+} \mid x)}{\pi_{\mathrm{ref}}(y^{+} \mid x)} - \log \frac{\pi_\theta(y^{-} \mid x)}{\pi_{\mathrm{ref}}(y^{-} \mid x)} \right] $$

$$ \ell(\theta) = -\log \sigma(m_\theta) \; - \; \frac{\lambda}{|y^{+}|} \log \pi_\theta(y^{+} \mid x) $$

| Item | Fact |
|---|---|
| $\sigma$ | logistic function |
| first term | the DPO loss (`rafailov2023dpo`) |
| second term | $\lambda$ times the loss of a warm-up round (Section 3.3) with $y^{+}$ in place of $y^\star$: negative log-likelihood of the correct sample, averaged over its tokens, hence on the same scale for short and long queries |
| why a second term | $m_\theta$ depends only on the difference of the two log-ratios: it can grow while the likelihood of $y^{+}$ falls, as long as that of $y^{-}$ falls faster. The NLL term acts on the likelihood of $y^{+}$ itself |
| objective of client $k$ | mean of $\ell$ over $\mathcal{P}_k^{t}$ |
| $\beta$, $\lambda$ | `\setting{pref.beta}`, `\setting{pref.nll}` |

Reference model:

| Item | Fact |
|---|---|
| $\pi_{\mathrm{ref}}$ | $\pi_{\theta^{t-1}}$; fixed during the round |
| it generated the samples | DPO takes as reference the model from which the pairs were sampled, when that model is available (`rafailov2023dpo`) |
| identical at all clients | the preference term of every client measures the change from the same model: the one all clients start from and the aggregate replaces |
| start of local training | model and reference model coincide: $m_\theta = 0$ for every pair |
| computation | its log-probabilities of the pairs are computed once, before local training; no second model is held during training |
| ceiling | nothing on client drift or on convergence |

## Section 3.5, What a round costs a client

### Statements to establish

| # | Claim | Evidence | Ceiling |
|---|---|---|---|
| 1 | Communication is that of FedAvg SFT: in every round of either kind a client receives and sends one adapter of the same size, plus one integer | protocol; `\setting{adapter.mb}` | "no added communication", as stated |
| 2 | What a preference round adds is computation at the client, of three kinds: generating the samples, executing them, training on pairs instead of single targets | table below | in kind only. No minutes, no ratio to a warm-up round: the measured times are in Section 5. Not "negligible", not "small" |
| 3 | The server is unchanged: a weighted average; it holds no data and executes no query | protocol | as stated |

### Facts

| Quantity, per client and round | Warm-up round | Preference round |
|---|---|---|
| received and sent | one adapter each way, `\setting{adapter.mb}`; one integer ($n_k$) | the same adapter; one integer ($\lvert\mathcal{P}_k^{t}\rvert$) |
| generation | none | $N n_k$ samples of at most `\setting{pref.tokens}` new tokens; inference only |
| execution | none | per question $y^\star$ once and its samples: at most $N + 1$ executions, each bounded by the time limit; on the client's own databases, no GPU |
| reference model | none | one pass over the pairs without gradient |
| training sequences in the epoch | $n_k$ (prompt and $y^\star$) | two per pair (the prompt with $y^{+}$, the prompt with $y^{-}$); at most $M n_k$ pairs, so at most $2 M n_k$ sequences; with $M$ = 2, at most $4 n_k$ against $n_k$. Fewer in practice, since only questions with both labels yield pairs; the numbers of questions and pairs per round are reported with the measured times in Section 5 |
| server | weighted average | the same weighted average |
| what the client must be able to do | fine-tune the model | the same, and execute SQL queries on its own databases |

## Algorithm 1

`algorithm` and `algorithmic` environments (`algpseudocode`),
`\label{alg:method}`, the caption yours. The whole method; the symbols
of `TERMS.md`.

| Part | Content |
|---|---|
| input | $\{\mathcal{D}_k\}_{k=1}^{K}$, the pretrained model, $T$, $T_w$, $N$, $M$, $\beta$, $\lambda$ |
| output | $\theta^{T}$ |
| initialization | $\theta^{0}$ |
| round $t = 1, \dots, T$ | the server sends $\theta^{t-1}$; every client in parallel: warm-up round ($t \le T_w$): local SFT on $\mathcal{D}_k$ from $\theta^{t-1}$, weight $n_k$. Preference round ($t > T_w$): steps 2 to 5 of the table of Section 3.4, weight $\lvert\mathcal{P}_k^{t}\rvert$. The client uploads $\theta_k^{t}$ and its weight; the server sets $\theta^{t}$ to the weighted average |

## Macros of the settings

Numeric macros may be used in math mode.

| Macro | Prints |
|---|---|
| `\setting{rounds.total}` | 4 |
| `\setting{rounds.warmup}` | 2 |
| `\setting{rounds.pref}` | 2 |
| `\setting{sft.epochs}` | 1 |
| `\setting{pref.samples}` | 10 |
| `\setting{pref.t}` | 1 |
| `\setting{pref.tokens}` | 256 |
| `\setting{pref.pairs}` | 2 |
| `\setting{pref.epochs}` | 1 |
| `\setting{pref.beta}` | 0.1 |
| `\setting{pref.nll}` | 1 |
| `\setting{adapter.mb}` | 73.9 MB (the unit is part of the macro; text mode only) |

## References

| Key | Facts |
|---|---|
| `mcmahan2017fedavg` | FedAvg. Clients train locally from the global model; the server averages the client models, weighted by the amount of local data |
| `hu2022lora` | LoRA. The pretrained weights stay frozen; trainable low-rank matrices are added to chosen weight matrices, and only these are trained |
| `rafailov2023dpo` | DPO. A loss over pairs of a preferred and a dispreferred output that increases the likelihood of the preferred one relative to a fixed reference model; $\beta$ sets the strength of the constraint towards the reference model. The reference is the model from which the pairs were sampled when that model is available, which keeps it close to the distribution of the pairs. The first term of the loss is the DPO loss |
| `tao2024codelutra` | CodeLutra, centralized, for code and SQL generation. Per iteration: 10 responses per input generated by the current model at temperature 1.0; labeled by execution against the gold result; correct paired with incorrect responses at random; trained with a DPO term whose reference model is the model of the current iteration, plus $\lambda$ times the log-likelihood of the correct response. $\beta$ = 0.1 and $\lambda$ = 1.0 for its data query task. Followed here: number of samples, temperature, random pairing, $\beta$, $\lambda$, and the reference model being the model that generated the samples. Different here in two settings: $M$ = 2 pairs per question where CodeLutra constructs 10 (reason: step 4 of the table of Section 3.4); the NLL term is averaged over tokens where CodeLutra's is the log-likelihood of the sequence. The value of $\lambda$ is CodeLutra's but its effect is not: with the average, the NLL term weighs less against the preference term than in CodeLutra, by the number of tokens of $y^{+}$. Different in kind, to be said where the closest work is named: CodeLutra runs the loop at one party that holds all the data and the databases, and it starts from the pretrained model, with no SFT stage. Here the questions, gold SQL queries and databases are at $K$ clients and are not pooled: each client computes the labels on its own databases; one federated round is one iteration of the loop (every client samples from the same global model, which is also the reference model of every client, and the server averages the adapters, weighted by the numbers of pairs); $T_w$ warm-up rounds of FedAvg SFT come first. What the paragraph leads with, after the credit: execution on the clients' databases is supervision that federated fine-tuning leaves unused and that only a client can compute; the method brings it into federated training by making a federated round the step that renews samples, labels and pairs, with the round's global model as the reference of every client. Ceiling: CodeLutra is credited with the loop of sampling, execution labels and a DPO + NLL loss, run centrally; the strongest wording for `\method` here is that it brings this supervision into federated training; "first" and "to our knowledge" belong to Section 1, not here Credit (owner, 2026-11-27; `AGENTS.md`, Writing, "Credit"): Section 3.4 does not say that the method follows or takes these from CodeLutra; the values that follow it are named once, in Section 4.5. The paragraph on CodeLutra says what CodeLutra does and where a preference round differs, and does not name the contribution of the method as bringing CodeLutra's loop into federated training. |
| `ye2024openfedllm` | OpenFedLLM, FedDPO: DPO as the local training of FedAvg. Each client holds a fixed set of preference pairs; one reference model for all rounds; no NLL term. Available for one clause of contrast with on-policy pairs; its discussion is Section 2 |

## Labels available

Of this section: `sec:method`, `sec:setting`, `sec:overview`,
`sec:warmup`, `sec:pref-round`, `sec:cost`, `fig:overview`,
`alg:method`; equation labels are yours (the earlier draft has
`eq:logratio`, `eq:loss`, `eq:aggregation`).

Of other sections: `sec:related`, `sec:setup`, `sec:results`,
`sec:ablation`, `sec:discussion`, `app:prompt`, `app:settings`. A
pointer to a later section goes to the section as a whole; its
subsections and tables have no labels yet.

## Paragraph roles (an offer)

For each subsection of a method: the design (inputs, each step,
outputs), the motivation of each choice (the problem it addresses), and
what the choice achieves, tied to what the paper measures. For the
setting: the parties and their data, the model and its input, the
protocol of a round, what is shared. For the overview: the idea, then
the stages and the round with the figure.
