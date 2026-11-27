# Checks: Section 3, Method, Fig. 1, Algorithm 1

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0). Items marked "v1" come from the review
of the first drafts (tag `draft-v1-2026-11-27`); the first
brief of this section is at the same tag, and its facts and the limits
of its Ceiling column are read from there when the new brief is built.

## 1. Facts about our work

- What leaves a client in a round: the adapter and one integer, its aggregation weight (the number of questions in a warm-up round, the number of pairs in a preference round), and nothing else. Samples, execution results, execution labels and preference pairs stay at the client. (v1 B3, B6; `CLAIMS.md`, contribution 2)
- The NLL term is averaged over the tokens of the correct sample. With the same lambda it weighs less against the preference term than a summed log-likelihood would, by a factor of the length of the sample. (v1 B2)
- An empty sample is an incorrect sample under the general rule; it needs no rule of its own in the text. (v1 B7)
- The reason for warm-up rounds, in counts: questions without a correct sample when the first preference round samples are, on BIRD, 4,035 of 9,428 with the pretrained model and 2,698 after 2 warm-up rounds. On Spider, of the questions on databases with rows: 1,016, then 557. "More questions yield pairs" holds on BIRD only (4,857 to 5,877); on Spider the questions that yield pairs fall (4,454 to 4,013). (v1 A1, B25)
- Two pairs per question: the reason given is that the number of pairs sets the length of local training; the paper has no ablation over M. (owner, 2026-11-26; v1 A5)
- Fig. 1 differs from the text in three places, not changed until the owner decides: "Only LoRA adapters travel" (the text: the adapter and one integer); step 4 writes L = L_DPO + L_NLL without lambda; "2 FedAvg rounds" and "N = 10" are typed in the figure. (v1 A4)

## 2. Facts about cited papers

- This section states no fact about CodeLutra: it cites it once, at the objective, and compares nothing. The facts about it are in `02_checks.md` and `04_checks.md`.
- The NLL term of Pang et al. is also length-normalized (fact row K.1 of `02_related_rows.md`). (v1 E)
- OpenFedLLM on pairs and the reference model: as in `02_checks.md`.

## 3. Claims: strength, scope, what waits

- Position of the method (owner, 2026-11-27): the framework and each component are motivated against federated SFT and federated DPO as published (FedAvg SFT learns from the gold SQL query alone and never uses the client's databases; FedDPO keeps the pairs and the reference model of its first round and has no NLL term). The section makes no comparison with CodeLutra and does not present a component as a difference from it; the comparison is in Section 2.2 and Table 1, the settings that follow it in Section 4.5.
- Evidence of each component, for the Evidence cell of the brief (the section reports no result and points to Sections 5 and 6): client-side execution labeling with the preference objective, A1 and A4 (+6.19 and +3.49 over FedAvg SFT; one preference round against one more SFT round); the preference term, B4 (execution errors 248 against 102 on BIRD); the NLL term, B3 (-3.87 EX without it, Spider); on-policy pair construction, B1 (+2.61 on BIRD, level on Spider); supervised warm-up, B5 (test-suite accuracy on Spider, no EX gain); aggregation weights, B6 (no difference). A component is given the property its definition confers; a gain is attributed to it only at the strength of its row.
- "First" and "to our knowledge" belong to Section 1.

## 4. What the section carries for other sections

- How a query is read from the output of the model and how execution results are compared is in Section 4, to which this section points.
- The time limit, the adapter configuration, the settings of local training and the replacement rule of pairing are in Appendix B.
- That a client must be able to execute SQL on its databases is said in Section 7 if not here.

## 5. Structure of the first draft (labels, floats, formulas)

Other sections and the generated tables refer to these labels. The macros and
citation keys each section used are in `inventory_v1.txt`.

### `sections/03_method.tex`

Headings and labels:

- `\section{Method}` `sec:method`
- `\subsection{Setting and notation}` `sec:setting`
- `\subsection{Overview}` `sec:overview`
- `\subsection{Warm-up rounds}` `sec:warmup`
- `\subsection{A preference round}` `sec:pref-round`
- `\subsection{What a round costs a client}` `sec:cost`

Floats:

- figure `fig:overview`, from `figures/fig_method_overview.pdf`
- algorithm `alg:method`

Equations, as checked against the code for the first draft:

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

Algorithm, as checked against the code for the first draft:

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
      \State label each sample $y$ by comparing $\mathrm{exec}(y, d)$
        with $\mathrm{exec}(y^\star, d)$
      \State $\mathcal{P}_k^{t} \gets$ $M$ pairs $(y^{+}, y^{-})$ for
        each question with samples of both labels
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
