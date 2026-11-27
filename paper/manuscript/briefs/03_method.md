# Brief: Section 3, Method

Kind of section: method (`voice.md`, "Method").

## Place in the manuscript

Preceded by Section 2 (Related work), whose final paragraph and Table 1
establish that no prior federated training method for Text-to-SQL
derives its supervision from execution on client databases. Followed by Section 4 (Experimental
setup), which specifies datasets, federated setups, models, baselines,
metrics and the statistical protocol. Section 3 reports no experimental
result apart from the measurement of Section 3.2 and the counts of
Section 3.4; the evidence for each component is in Section 5.

Length: at most 1,700 words, about 1,530 requested, excluding
equations, Algorithm 1 and the caption of Fig. 2.

Headings and labels, fixed:

| Heading | Label | Approximate share |
|---|---|---|
| `\section{Method}` | `sec:method` | |
| `\subsection{Problem Formulation}` | `sec:formulation` | 300 |
| `\subsection{Execution-Derived Supervision}` | `sec:supervision` | 150 |
| `\subsection{Framework Overview}` | `sec:overview` | 200 |
| `\subsection{Supervised Warm-Up}` | `sec:warmup` | 200 |
| `\subsection{Client-Side Execution Labeling}` | `sec:labeling` | 250 |
| `\subsection{On-Policy Preference Pair Construction}` | `sec:pairs` | 200 |
| `\subsection{Preference Objective and Aggregation}` | `sec:objective` | 400 |

## Aim

At the end of the section the reader can reimplement \method, knows for
each component the deficiency of federated SFT or of FedDPO that it
addresses and the property that its definition confers, and knows what
a client transmits and what it computes in each kind of round.

## Points of the argument

1. Formal setting and the supervision of FedAvg SFT. Each client holds
   questions, gold SQL queries and the databases on which they execute;
   the target of the objective of FedAvg SFT (Eq. `eq:sft`) is the gold
   SQL query alone. A database enters training only as text of the
   prompt; no query is executed on it, and the model receives no signal
   about which of its own queries are incorrect. Evidence: the
   definition itself.
2. Execution-derived supervision as an unused, client-local signal.
   Execution on $d$ partitions the model's own samples for a question
   into correct and incorrect ones; the partition is computable only
   where $d$ resides. Its prevalence is measured: for the model after
   two rounds of FedAvg SFT, the $N$ samples of a question yield
   preference pairs for 62.3% of the BIRD training questions, which on
   BIRD are exactly the questions with both a correct and an incorrect
   sample. Evidence: the counts under Materials.
3. The framework as four components and an aggregation rule: supervised
   warm-up, client-side execution labeling, on-policy pair construction
   and the preference objective, organized into two kinds of round.
   Fig. 2 and Algorithm 1 convey the order of a run. Evidence: the
   definitions; the gain of the complete framework over FedAvg SFT is
   reported in Section 5.1 (Table 3).
4. Supervised warm-up reduces the number of questions that cannot
   yield a preference pair for lack of a correct sample. A preference
   pair requires a correct sample; for the pretrained model 4,035 of
   the 9,428 BIRD training questions have none, and after two warm-up
   rounds 2,698. Warm-up is not a requirement of the preference rounds:
   the pretrained model already yields pairs, and $T_w$ is a setting of
   the framework. Evidence: the counts under
   Materials; the effect of the number of warm-up rounds on accuracy is
   the subject of Section 5.3 and is not anticipated here.
5. Client-side execution labeling defines the label and its locality.
   A sample is correct when its execution result equals that of the
   gold SQL query on the client's database; the label therefore
   requires the gold SQL query and the database, and it is computed
   without any exchange beyond the global adapter. Evidence: the
   definition; the comparison of execution results is that of the
   evaluation metric (Section 4).
6. On-policy pair construction makes each federated round one
   resampling step. The pairs of a preference round are constructed
   from samples of that round's global model, which is also the
   reference model; the errors of every new global model are thus
   identified anew at no additional communication. FedDPO trains on a
   fixed set of pairs and retains one reference model for all rounds. Evidence: on BIRD
   dev the on-policy variant exceeds the variant with fixed pairs and
   fixed reference model by 2.61 EX, significant; on Spider test the two
   are level (Table 4, Section 5.3).
7. The preference objective combines two terms with distinct roles
   (Eq. `eq:loss`). The preference term raises the likelihood of the
   correct sample relative to the incorrect one, measured against the
   reference model; it constrains only a difference of log-ratios. The
   NLL term acts on what that difference leaves undetermined: it raises
   the log-likelihood of the correct sample itself.
   Evidence, both in Table 4 and Section 5.3: without the NLL term a
   preference round lowers EX below the model it starts from (Spider
   test); without the preference term more predictions end in an
   execution error, 248 against 102 on BIRD dev and 153 against 99 on
   Spider test, both differences significant.
8. Aggregation and client cost. Federated averaging of the adapters
   with weights proportional to the pair counts; a client transmits the
   adapter and one integer, exactly as in a FedAvg SFT round, so that
   the communication per round is unchanged. The additional cost is
   client computation: sampling, execution and local training on the
   pairs. Evidence: the definitions; the measured times are in
   Section 5.6 (Table 8), and the aggregation weights are immaterial to
   accuracy (Table 4).

## Materials

### Setting and notation

Notation as in `terms.md`. Further facts:

- The pretrained model is frozen; a LoRA adapter $\theta$ is trained,
  and it is the only set of parameters that is communicated and
  aggregated (`\setting{adapter.mb}` per client per round). With its
  adapter a client sends one integer, its aggregation weight.
- All $K$ clients participate in every round. Local training in round
  $t$ starts from $\theta^{t-1}$ with a newly initialized optimizer.
- The prompt $x$ contains the question $q$ and the schema of $d$ as
  `CREATE TABLE` statements; on Spider each table is followed by up to
  three of its rows, and on BIRD the prompt includes the external
  knowledge that the benchmark attaches to the question. The same
  prompt serves training, sampling and
  evaluation. Its exact form is printed in Appendix A (`fig:prompt`).
- Default configuration: $T$ = `\setting{rounds.total}`, $T_w$ =
  `\setting{rounds.warmup}`, $N$ = `\setting{pref.samples}`, $M$ =
  `\setting{pref.pairs}`, $\beta$ = `\setting{pref.beta}`, $\lambda$ =
  `\setting{pref.nll}`; one local epoch in either kind of round
  (`\setting{sft.epochs}`, `\setting{pref.epochs}`). All remaining
  settings are in Appendix B (`tab:settings`).

### Equations

Warm-up round, local objective of client $k$:

```latex
\begin{equation}
  \mathcal{L}_k^{\mathrm{SFT}}(\theta) = \frac{1}{n_k}
    \sum_{(q, d, y^\star) \in \mathcal{D}_k}
    -\frac{1}{\lvert y^\star \rvert} \log \pi_\theta(y^\star \mid x).
  \label{eq:sft}
\end{equation}
```

Aggregation (warm-up round; in a preference round $n_k$ is replaced by
$\lvert\mathcal{P}_k^{t}\rvert$):

```latex
\begin{equation}
  \theta^{t} = \sum_{k=1}^{K} w_k \, \theta_k^{t},
  \qquad
  w_k = \frac{n_k}{\sum_{j=1}^{K} n_j},
  \label{eq:aggregation}
\end{equation}
```

Preference round, for a pair $(y^{+}, y^{-})$ of a question with prompt
$x$, with $\pi_{\mathrm{ref}} = \pi_{\theta^{t-1}}$:

```latex
\begin{equation}
  m_\theta = \beta \left[
    \log \frac{\pi_\theta(y^{+} \mid x)}{\pi_{\mathrm{ref}}(y^{+} \mid x)}
    - \log \frac{\pi_\theta(y^{-} \mid x)}{\pi_{\mathrm{ref}}(y^{-} \mid x)}
  \right]
  \label{eq:logratio}
\end{equation}
```

```latex
\begin{equation}
  \ell(\theta) = -\log \sigma(m_\theta)
    - \frac{\lambda}{\lvert y^{+} \rvert} \log \pi_\theta(y^{+} \mid x),
  \label{eq:loss}
\end{equation}
```

Properties of these definitions:

- The local objective of a preference round is the mean of $\ell$ over
  $\mathcal{P}_k^{t}$.
- The log-likelihoods of $m_\theta$ are sums over the tokens of the
  query; the NLL term is a mean over the tokens of $y^{+}$, as is the
  loss of Eq. `eq:sft`.
- At the start of local training $\theta = \theta^{t-1}$, hence
  $m_\theta = 0$ for every pair: the reference model, the model that
  generated the samples and the initialization of every client
  coincide.
- The preference term is invariant to a common shift of
  $\log \pi_\theta(y^{+} \mid x)$ and $\log \pi_\theta(y^{-} \mid x)$;
  it can decrease while both likelihoods decrease.

### Execution labeling and pair construction

- Sampling: $N$ queries per training question from
  $\pi_{\theta^{t-1}}(\cdot \mid x)$ at temperature `\setting{pref.t}`,
  without nucleus or top-$k$ truncation, at most `\setting{pref.tokens}`
  new tokens per sample.
- Execution: each sample and the gold SQL query are executed on the
  database $d$ of the question, under the time limit of the evaluation
  of the respective benchmark.
- Label: correct if $\mathrm{exec}(y, d) = \mathrm{exec}(y^\star, d)$
  under the comparison of the evaluation metric; incorrect otherwise. A
  sample that fails to execute, exceeds the time limit or contains no
  query is incorrect. A sample that reaches the token limit before
  completion is not executed and receives no label. On BIRD, where a
  sample and the gold SQL query share one time limit, a sample that
  executes but whose comparison with the gold result is not completed
  within the limit likewise receives no label.
- Questions without labels: those whose gold SQL query fails to execute
  or exceeds the time limit (their counts are given in Section 4.2).
- Pair construction: for each question with at least one correct and
  one incorrect sample, $M$ correct and $M$ incorrect samples are drawn
  uniformly and independently, without replacement when the question
  has at least $M$ samples of that label and with replacement
  otherwise, and paired in the order drawn. Hence
  $\lvert\mathcal{P}_k^{t}\rvert = M$ times the number of such
  questions of client $k$.
- Questions that yield no pair in a round: those whose samples are all
  correct or all incorrect, and those on a database whose tables
  contain no rows, where execution results do not discriminate between
  queries. All questions are sampled again in the next preference
  round.
- A client whose $\mathcal{P}_k^{t}$ is empty performs no local
  training and sends no update in that round; its aggregation weight
  is zero.
- The value of $M$ determines the length of local training, since one
  local epoch passes once over $\mathcal{P}_k^{t}$.

### Counts (macros of `results/macros.md`)

| Quantity | BIRD train | Spider train |
|---|---|---|
| training questions of the clients | `\fact{cost.bird.pref1.questions}` 9,428 | `\fact{cost.spider.pref1.questions}` 8,659 |
| of these, on databases without rows | `\fact{train.bird.no_rows}` 0 | `\fact{train.spider.no_rows}` 1,759 |
| first preference round: questions that yield preference pairs | `\fact{cost.bird.pref1.paired}` 5,877 (`\fact{cost.bird.pref1.paired_pct}` 62.3%) | `\fact{cost.spider.pref1.paired}` 4,013 (`\fact{cost.spider.pref1.paired_pct}` 46.3%) |
| questions without a correct sample, pretrained model | `\fact{warmup.bird.k0.no_correct}` 4,035 | `\fact{warmup.spider.k0.no_correct}` 1,016 |
| questions without a correct sample, after two warm-up rounds | `\fact{warmup.bird.k2.no_correct}` 2,698 | `\fact{warmup.spider.k2.no_correct}` 557 |

On BIRD the questions that yield preference pairs are all questions
with both a correct and an incorrect sample. On Spider the count
excludes the questions on databases without rows, including those with
samples of both labels. The Spider counts of the last two rows refer to
the questions on databases with rows. The model of the first preference
round is the global model after two rounds of FedAvg SFT.

### Figure and algorithm

- Fig. 2, the overview of the framework: `results/fig_method_overview.pdf`,
  label `fig:overview`, included with
  `\includegraphics[width=\linewidth]{figures/fig_method_overview.pdf}`.
  The caption is part of the section.
- Algorithm 1, label `alg:method`:

```latex
\begin{algorithm}[t]
\caption{\method}\label{alg:method}
\begin{algorithmic}[1]
\Require training sets $\{\mathcal{D}_k\}_{k=1}^{K}$, pretrained model,
  $T$, $T_w$, $N$, $M$, $\beta$, $\lambda$
\Ensure global adapter $\theta^{T}$
\State initialize the adapter $\theta^{0}$
\For{$t = 1, \dots, T$}
  \State the server sends $\theta^{t-1}$ to all $K$ clients
  \ForAll{clients $k = 1, \dots, K$ in parallel}
    \If{$t \le T_w$} \Comment{warm-up round}
      \State $\theta_k^{t} \gets$ local training from $\theta^{t-1}$ on
        $\mathcal{D}_k$ with the loss of Eq.~\eqref{eq:sft}
      \State upload $\theta_k^{t}$ and $n_k$
    \Else \Comment{preference round}
      \State sample $N$ queries from $\pi_{\theta^{t-1}}(\cdot \mid x)$
        for each $(q, d, y^\star) \in \mathcal{D}_k$
      \State label the samples by comparing $\mathrm{exec}(y, d)$
        with $\mathrm{exec}(y^\star, d)$
        (Section~\ref{sec:labeling})
      \State $\mathcal{P}_k^{t} \gets$ $M$ pairs $(y^{+}, y^{-})$ for
        each question that yields pairs (Section~\ref{sec:pairs})
      \State $\theta_k^{t} \gets$ local training from $\theta^{t-1}$ on
        $\mathcal{P}_k^{t}$ with the loss of Eq.~\eqref{eq:loss},
        $\pi_{\mathrm{ref}} = \pi_{\theta^{t-1}}$
      \State upload $\theta_k^{t}$ and $\lvert\mathcal{P}_k^{t}\rvert$
    \EndIf
  \EndFor
  \State $\theta^{t} \gets \sum_{k=1}^{K} w_k \, \theta_k^{t}$, with
    $w_k \propto n_k$ if $t \le T_w$ and
    $w_k \propto \lvert\mathcal{P}_k^{t}\rvert$ otherwise
\EndFor
\State \Return $\theta^{T}$
\end{algorithmic}
\end{algorithm}
```

### Communication and computation of a round

| | Warm-up round | Preference round |
|---|---|---|
| server to client | global adapter | global adapter |
| client to server | adapter, $n_k$ | adapter, $\lvert\mathcal{P}_k^{t}\rvert$ |
| remains at the client | questions, gold SQL queries, databases | the same, and the samples, execution results, execution labels and preference pairs |
| client computation | one epoch over $\mathcal{D}_k$ | generation of $N n_k$ samples; their execution; one epoch over $\mathcal{P}_k^{t}$, each pair scored by the model and by the reference model |

## References

| Key | Cited for |
|---|---|
| `mcmahan2017fedavg` | federated averaging |
| `hu2022lora` | the LoRA adapter |
| `ye2024openfedllm` | federated SFT of language models with adapters; FedDPO, whose pairs and reference model are fixed and whose loss has no NLL term |
| `rafailov2023dpo` | the DPO loss, that is, the preference term |
| `pang2024irpo`, `tao2024codelutra` | a preference loss combined with an NLL term on the preferred response; cited once, at the objective |

## Labels available for cross-reference

`sec:related`, `sec:setup`, `sec:results`, `sec:main`, `sec:analysis`,
`sec:ablation`, `sec:cost`, `sec:discussion`, `tab:main`,
`tab:ablation`, `tab:cost`, `fig:prompt`, `tab:settings`.
