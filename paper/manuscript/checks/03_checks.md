# Checks: Section 3, Method, Fig. 2, Algorithm 1

What stays true whatever the draft says: facts and the bounds of claims.
It is read before the section is written and when it is checked; remarks
on the wording of a draft are not kept here.

## 1. Facts about our work

- What leaves a client in a round: the adapter and one integer, its aggregation weight (the number of questions in a warm-up round, the number of pairs in a preference round), and nothing else. Samples, execution results, execution labels and preference pairs stay at the client. (`CLAIMS.md`, contribution 2)
- The NLL term is averaged over the tokens of the correct sample. With the same lambda it weighs less against the preference term than a summed log-likelihood would, by a factor of the length of the sample.
- An empty sample is an incorrect sample under the general rule; it needs no rule of its own in the text.
- The reason for warm-up rounds, in counts: questions without a correct sample when the first preference round samples are, on BIRD, 4,035 of 9,428 with the pretrained model and 2,698 after 2 warm-up rounds. On Spider, of the questions on databases with rows: 1,016, then 557. "More questions yield pairs" holds on BIRD only (4,857 to 5,877); on Spider the questions that yield pairs fall (4,454 to 4,013). The fall on Spider comes from the questions whose samples are all correct (databases with rows): 1,427 with the pretrained model, 2,327 after 2 warm-up rounds; on BIRD 156 and 416. The pretrained-model counts of questions that yield pairs and of all-correct questions have no macro and are not printed (round records of the first preference rounds, `pair_stats`).
- The adapter starts at the PEFT default (`get_peft_model` with `LoraConfig`, `fedls_sql/training/lora_trainer.py`): its update is zero, so the model with the initial adapter is the pretrained model; a preference round without warm-up samples from the pretrained model, and its clients start from one shared new adapter (`fedls_sql/federated/pref_rounds.py`).
- The log-probabilities of the reference model are computed once per pair, before the first update of a round (`fedls_sql/training/dpo.py`).
- Local training on the pairs is not an added cost in every round: the second preference round on Spider takes 0.9 of the GPU time of a FedAvg SFT round. What a preference round adds in kind is sampling and execution.
- Two pairs per question: the reason given is that the number of pairs sets the length of local training; the paper has no ablation over M. (owner, 2026-11-26)
- Fig. 2 (the overview of the framework), as committed: "Only adapters and pair counts travel"; step 4 writes L = L_DPO + lambda L_NLL; "FedAvg, weighted by number of pairs" at the server; "2 FedAvg rounds" and "N = 10" are typed in the figure as the default configuration. The figure shows the pair count as the weight; the question count of a warm-up round is in the text only.
- Counts of questions without a correct sample (4,035, 2,698; Spider 1,016, 557) are the questions whose labeled samples are all incorrect. Questions without labels (gold SQL query fails or exceeds the time limit) are not among them: on BIRD 380 for the pretrained model and 437 at the first preference round of the main row (350 that fail, 30 and 87 over the limit). BIRD, first preference round: 416 all correct + 5,877 with both labels + 2,698 all incorrect + 437 without labels = 9,428.
- "No query is executed on the database" is false on Spider: the prompt builder reads up to three rows per table with `SELECT * FROM t LIMIT 3` (`fedls_sql/data/spider.py`, `_ddl_rows`), and the printed prompt shows that statement. True on both datasets: FedAvg SFT executes neither the gold SQL query nor a query of the model, and no execution result enters its loss. (claim audit, 2026-11-28)
- Time limit of the labels on BIRD: one 30 s budget for the sample followed by the gold SQL query; the gold runs once per question and its seconds count in every pair. Budget reached while the sample runs: execution error, incorrect. Sample completed and budget reached while the gold runs: no label (`fedls_sql/preference/sampling.py`, `is_gold_timeout`). Spider: 60 s for each query.
- The number of pairs of a client is M times the number of its questions that yield pairs, after the exclusion of the databases without rows: Spider, first preference round, 5,192 questions with both labels, 8,026 pairs = 2 x 4,013. Identical samples are not merged before the draw; a question with one sample of a label has it in both pairs.
- A question without pairs is not trained on in that preference round (neither term): 3,551 of the 9,428 BIRD questions at the first preference round (416 all correct, 2,698 all incorrect, 437 without labels).
- A client without pairs neither trains nor uploads (`fedls_sql/federated/pref_rounds.py`); Algorithm 1 does not show the exception; no client was without pairs in any committed round.

## 2. Facts about cited papers

- This section states no fact about CodeLutra: it cites it once, at the objective, and compares nothing. The facts about it are in `02_checks.md` and `04_checks.md`.
- The NLL term of Pang et al. is also length-normalized (fact row K.1 of `02_related_rows.md`).
- OpenFedLLM on pairs and the reference model: as in `02_checks.md`.

## 3. Claims: strength, scope, what waits

- Position of the method (owner, 2026-11-27): the framework and each component are motivated against federated SFT and federated DPO as published (FedAvg SFT learns from the gold SQL query alone and never executes a query on the client's databases, which enter only the prompt (on Spider with up to three rows per table); FedDPO keeps the pairs and the reference model of its first round and has no NLL term). The section makes no comparison with CodeLutra and does not present a component as a difference from it; the comparison is in Section 2.2 and Table 1, the settings that follow it in Section 4.5.
- Evidence of each component (the section reports no result and points to Section 5): client-side execution labeling with the preference objective, A1 and A4 (+6.19 and +3.49 over FedAvg SFT; one preference round against one more SFT round); the preference term, B4 (execution errors 248 against 102 on BIRD; at 4 rounds on BIRD -3.52 EX without it, significant); the NLL term, B3 (-3.87 EX without it on Spider; on BIRD -1.24, not significant, 2026-11-28); on-policy pair construction, B1 (+2.61 on BIRD, level on Spider); supervised warm-up, B5 (test-suite accuracy on Spider, no EX gain); aggregation weights, B6 (no difference). A component is given the property its definition confers; a gain is attributed to it only at the strength of its row.
- "First" and "to our knowledge" belong to Section 1.

## 4. What the section carries for other sections

- How a query is read from the output of the model and how execution results are compared is in Section 4, to which this section points.
- The mechanics of the time limit of the labeling step (BIRD: one budget for the sample and the gold SQL query; Spider: one limit per query; part 1) are told in Section 4, to which Section 3.5 points. The values of the time limit, the adapter configuration and the settings of local training are in Appendix B.
- That a client must be able to execute SQL on its databases is said in Section 6 if not here.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. `make inventory` lists the macros and
citation keys by section.

### `sections/03_method.tex`

Headings and labels (`OUTLINE.md`, approved):

- `\section{Method}` `sec:method`
- `\subsection{Problem Formulation}` `sec:formulation`
- `\subsection{Execution-Derived Supervision}` `sec:supervision`
- `\subsection{Framework Overview}` `sec:overview`
- `\subsection{Supervised Warm-Up}` `sec:warmup`
- `\subsection{Client-Side Execution Labeling}` `sec:labeling`
- `\subsection{On-Policy Preference Pair Construction}` `sec:pairs`
- `\subsection{Preference Objective and Aggregation}` `sec:objective`

Floats:

- figure `fig:overview`, from `figures/fig_method_overview.pdf`
- algorithm `alg:method`

Equations, as checked against the code:

```latex
\begin{equation}
  \mathcal{L}_k^{\mathrm{SFT}}(\theta) = \frac{1}{n_k}
    \sum_{(q, d, y^\star) \in \mathcal{D}_k}
    -\frac{1}{\lvert y^\star \rvert} \log \pi_\theta(y^\star \mid x).
  \label{eq:sft}
\end{equation}
```

```latex
\begin{equation}
  \theta^{t} = \sum_{k=1}^{K} w_k \, \theta_k^{t},
  \qquad
  w_k = \frac{n_k}{\sum_{j=1}^{K} n_j},
  \label{eq:aggregation}
\end{equation}
```

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

Algorithm, as checked against the code:

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
