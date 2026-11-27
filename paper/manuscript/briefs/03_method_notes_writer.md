# Notes to the editor: Section 3, Method

Draft: `sections/03_method.tex`, revised after your notes of rounds 1
and 2. It has not been compiled; no LaTeX toolchain is available in this
environment.

## 0. Revision after round 1

Only the passages your notes concern were changed.

| Note | Passage | Change |
|---|---|---|
| 1 | 3.1, last paragraph | The database contributes only to the text of the prompt; neither the gold SQL query nor a query of the model is executed; no execution result enters the loss. "No query is executed on it" is gone. |
| 1 | 3.5, first sentence | "FedAvg SFT executes none of the model's queries on the client databases." |
| 2 | 3.5, first paragraph | The time limit is stated per benchmark: one limit per query on Spider, one limit for the sample followed by the gold SQL query on BIRD. A sample that reaches the limit itself is incorrect. |
| 2 | 3.5, second paragraph | The cases without a label are tied to one criterion (the sample is never compared with the gold result) and listed: token limit, BIRD shared limit reached before the gold SQL query completes, gold SQL query failing or exceeding the limit on its own. |
| 2 | 3.5, last sentence | Removed. The subsection ends on the cases without a label; that every sample is a draw from the model's distribution is already in the sampling sentence. |
| 3 | 3.6, first paragraph | The condition for pairs comes first and includes the rows; the exclusion is marked as one of pairs and not labels ("although its samples are labeled"). The two draws are separated: from the correct samples and, independently, from the incorrect ones. Identical queries are not merged. The pair count is $M$ times the number of questions that yield pairs. |
| 3 | 3.6, second paragraph | Added: a question without pairs contributes to neither term in that round, the NLL term included; the role of $M$ (weight of a question, number of local updates), without a claim about accuracy. |
| 4 | 3.7, fourth paragraph | Order is now rule, reason, exception. The integer is named as the pair count. The reason for the weights is that of federated averaging. |
| 4 | Algorithm 1 | Training and upload in a preference round are now conditional on a non-empty $\mathcal{P}_k^{t}$, with a comment that the client otherwise sends no update and has $w_k = 0$. This changes the algorithm of the brief by one `\If`. |
| 5 | 3.2, measurement | Pointer to the BIRD setup of Section 4.2, "one pass of sampling", "training questions of all clients, those without labels included". |
| 5 | 3.4, counts | Both counts now refer to the same set (labeled samples all incorrect), measured as in 3.2; the questions without labels are said to be in neither. |

Two things I did not do:

- I did not add that no client was without pairs in any round. It is an
  observation of the experiments, and the brief keeps those out of
  Section 3 apart from 3.2 and 3.4. A clause in the fourth paragraph of
  3.7 would take about ten words if you want it.
- The consequence that a question with a single sample of a label has
  that sample in all its pairs is not spelled out; it follows from "with
  replacement otherwise", and the length did not allow it.

## 0b. Revision after round 2

Again only the passages your notes concern were changed.

| Note | Passage | Change |
|---|---|---|
| 1, 3 | Lead | "Retains an NLL term" is now "adds to the loss an NLL term on the correct sample". The three respects are three verb phrases with one subject (forms, renews, adds). |
| 1 | 3.3, first two sentences | The framework "trains on execution-derived supervision"; "in addition to the gold SQL queries" is gone. The sentence that sets the two kinds of round side by side now states the role of the gold SQL query in each: training target in a warm-up round; executed to produce the execution labels, and not a training target, in a preference round. |
| 2 | Caption of Fig. 2 | Rewritten. It says what the figure depicts (order of a run; one preference round at one client), that it shows the default configuration while $T_w$ and $N$ are settings, which component each numbered step belongs to, and how "Global model", $L_{\mathrm{DPO}}$, $\lambda L_{\mathrm{NLL}}$ and the weighting at the server correspond to the terms of the section. Labels go to "the samples that are compared with the gold result". |
| 3 | 3.4, last sentence | "The labeled samples are all incorrect for ... questions" replaces "it is the case for". |
| 3 | 3.7, second paragraph, last sentence | "The log-ratios of Eq. (3) are therefore taken relative to the model that generated both samples of the pair." |
| 4 | 3.5, execution | The gold SQL query is executed once per question and each sample once. On BIRD each sample has one limit, against which its own running time and that of the gold SQL query count. The unlabeled BIRD case is restated in the same terms. |
| 4 | 3.6, databases without rows | Defined as no table containing a row. The reason is now that queries of different meaning return the same result, so that a sample that executes can match the gold result whether or not it is correct. |
| 5 | 3.6, second paragraph | "One resampling step" is replaced by the relation it stood for: one iteration of preference optimization (sampling from the current model, training on the labeled samples) coincides with one communication round, and the global model that aggregation produces in round $t-1$ is the model sampled in round $t$. |

Two choices of wording to check:

- The examples "an empty set, or the same aggregate over no rows" are
  not in 3.6; the length did not allow them.
- The unlabeled case on BIRD reads "its running time and that of the
  gold SQL query together exceed the limit". This is my rendering of
  "the limit is reached before the gold SQL query completes" once the
  gold SQL query is executed a single time per question. If the
  procedure differs, this clause needs your wording.

## 1. Length

Counted by hand, without Algorithm 1, the displayed equations and the
caption of Fig. 2. Round 1 added about 130 words and round 2 about 85.

- About 1,830 words when every inline symbol, macro, citation and
  cross-reference counts as one word. This is over the limit of 1,700.
- About 1,665 words when inline mathematics and commands are stripped.
  This is within the limit and 135 above the target.

The section is above the requested length under either convention, and
every word of the excess answers a note of round 1 or 2. If the first
convention is yours, about 130 words have to go, and they can only come
from text you asked me to leave unchanged. Forward references that the
argument does not need give 42 of them: the last sentence of 3.3 (gain
over FedAvg SFT, 11 words), the last sentence of 3.4 (effect of $T_w$,
10), the gold SQL clause at the end of 3.6 (13), the last sentence of
the fourth paragraph of 3.7 (choice of weights, 8). The rest would have
to come from the description of the prompt in 3.1, which Appendix A
repeats, and from the cases without a label in 3.5.

## 2. Points whose evidence is thinner than the brief suggests

1. **Warm-up, point 4.** The section claims only what holds on both
   datasets: fewer questions whose labeled samples are all incorrect. It
   makes no statement about the number of questions that yield pairs,
   which rises on BIRD and falls on Spider according to your answer. With
   Table 4 showing no warm-up round level with the default on Spider
   test, a reviewer will ask what warm-up is for. Section 3.4 leaves that
   to Section 5.3, which then has to carry it. The pretrained-model pair
   counts would help there, and they have no macro.
2. **Prevalence, point 2.** "The majority of the training questions" is
   scoped to BIRD. On Spider the macro prints 46.3% of all questions; the
   share among the questions on databases with rows has no macro. The
   section does not generalize the statement.
3. **On-policy pairs, point 6.** On Spider test the on-policy variant and
   the variant with fixed pairs and fixed reference model are level.
   Section 3.6 therefore asserts the property of the definition (the
   incorrect queries of each new global model are identified anew) and no
   benefit in accuracy.
4. **NLL term, point 7.** "A preference round lowers EX below the model
   it starts from" rests on 73.59 against 74.10 on Spider test. No macro
   gives a test of that comparison. Section 3 does not quote it; the
   concern is for Section 5.3.
5. **The value of $M$.** The section gives the role of $M$ and no
   evidence for its value, since none was measured. A reviewer may ask
   for it.

## 3. Departures from the outline

- **Repetitions removed.** The locality of the label is carried by
  Section 3.2; Section 3.5 does not restate it. The communication
  argument is carried by the fourth paragraph of 3.7; Section 3.6 keeps
  the clause "at no additional communication". On FedDPO, the lead names
  the three differences, 3.6 treats the pairs and the second paragraph of
  3.7 the reference model.
- **Section 3.7, definition.** The two references on the NLL term are
  attached to the definition; there is no sentence on the provenance of
  the form.
- **Section 3.5.** The motivation names FedAvg SFT only, and the
  subsection has no interpretive close.
- **Section 3.4.** The sentence that a warm-up round adds no operation
  and no message was dropped as self-evident.
- **Section 3.6.** The two forward references to Section 5.3 (fixed
  pairs and reference model; gold SQL query in place of a missing correct
  sample) are one sentence.
- **Cost.** The last paragraph names the operations of each kind of
  round, states that the reference log-likelihoods are computed once per
  pair, and compares no times.

## 4. Values and references typed without a macro or a listed label

- "up to three rows" in the prompt on Spider: no macro exists.
- "Appendix A" and "Appendix B" are typed, since no appendix label is
  listed; `fig:prompt` and `tab:settings` are referenced by label.
- `sec:fed-setups` comes from your answer and is not in the list of the
  brief. It is used in 3.2, 3.5 and 3.6; the counts of 3.4 reach it
  through their pointer to 3.2.
- The local epochs appear once, by macro, in 3.3 (`\setting{sft.epochs}`,
  `\setting{pref.epochs}`); later paragraphs say "an epoch" or "the local
  epoch". These read correctly only while both values are 1.
- "$T_w = 0$" in 3.4 is a case of the definition, not the configuration.
- No `\expect{}` is used: no number of the section awaits its result.

## 5. Statements about cited works

All come from `related/`; nothing was taken from the web.

| Statement in the section | Source |
|---|---|
| FedDPO trains each client on a fixed preference dataset whose pairs are responses contained in that dataset, not outputs of the model under training (3.6) | `related/ye2024openfedllm.md`, properties 4 and 5 (Secs. 3.3, 4.7, 4.8) |
| FedDPO retains one reference model for the whole federated process (3.7) | same file, property 6 (Sec. 3.3, text after Eq. 2) |
| The loss of FedDPO has no NLL term (lead, 3.7) | same file, property 6 |
| Federated averaging weights a client by its number of local training examples (3.7) | `related/ye2024openfedllm.md`, property 1 (aggregation weighted by relative dataset size, Sec. 3.1); the file on `mcmahan2017fedavg` holds the abstract only and does not state the weighting |
| The preference term is the DPO loss (3.7) | `related/rafailov2023dpo.md`, statement 1 (Eq. 7) |
| A preference loss combined with an NLL term on the preferred response (3.7, citation only) | `related/pang2024irpo.md`, statement 1 (Eq. 1); `related/tao2024codelutra.md`, property 6 (Eq. 3) |

One caution on the first row: the source describes no step that
regenerates pairs, which is what "fixed" renders; it does not use the
word.

The second paragraph of 3.6 describes one iteration of preference
optimization as "sampling from the current model and training on the
labeled samples". The wording follows your note 5 of round 2 and carries
no citation, since the brief cites `pang2024irpo` and `tao2024codelutra`
once, at the objective. Both files in `related/` support the
description.

## 6. Fig. 2

The caption now tells the reader how to read the figure (see 0b). The
differences themselves remain in the figure, which is fixed:

- it prints "2 FedAvg rounds" and "N = 10" as fixed text, so it will not
  follow a change of the settings, whereas the caption prints both by
  macro;
- it writes the loss as $L = L_{\mathrm{DPO}} + \lambda L_{\mathrm{NLL}}$,
  whereas the section writes $\ell(\theta)$ and "the preference term";
- it says "Global model $\theta^{t-1}$" where the section says "global
  adapter";
- step 2 shows a label on every sample, whereas 3.5 lists samples
  without one.

The caption refers to Sections 3.5 to 3.7 by label, although the figure
floats to the top of 3.3.

## 7. Where a reviewer may still hesitate

- **The pair count as a message.** The integer a client sends in a
  preference round is $M$ times the number of its questions that yield
  pairs, which says more about the client than $n_k$ does. The section
  does not discuss it, since limitations belong to Section 6. Table 4
  shows that weights by number of questions give the same accuracy,
  which would answer the objection.
- **Terminology.** The section says "incorrect queries" where the brief
  says "errors" of the model, to keep "execution error" unambiguous.

The two hesitations of the first draft on duplicate samples and on the
time limit of BIRD are settled by your notes 2 and 3.

## 8. Proposals

- An illustrative example (one question with a correct and an incorrect
  sample and their execution results) would make 3.5 and 3.6 concrete,
  at about 60 words or as a small figure. It is not in the draft: the
  length does not allow it, and Fig. 1 may already serve.

## 9. Caption of Fig. 2 (redrawn figure)

Rewritten for the redrawn `figures/fig_method_overview.pdf` and revised
after round 1 of the caption notes (replacing note 6 above on the earlier
figure); the rest of `sections/03_method.tex` is unchanged.

- **Round 1 changes to the caption.** (1) Replaced the ambiguous
  parenthetical after `clients 1, ..., K` with `communicates with each of
  clients $1, \dots, K$ via arrows labeled once at client~$k$`, attaching
  the label note to the per-client arrows rather than to the clients.
  (2) Split and shortened the notation mappings, removing the nested
  parenthetical on $\theta^{t-1}$: the arrow labels (`Global model
  $\theta^{t-1}$` and `count`) stand in one sentence, $\theta^{t-1}$ in
  steps 1 and 4 stands in its own clause as $\pi_{\theta^{t-1}}$ (which
  is $\pi_{\mathrm{ref}}$ in `Eq.~\eqref{eq:logratio}`), and step 1's
  default setting $N = {}$\setting{pref.samples} and step 4's
  $L_{\mathrm{DPO}}$ and $\lambda L_{\mathrm{NLL}}$ close the caption
  without repeating the full equation.
- **What the caption maps.** Server aggregation (`Eq.~\eqref{eq:aggregation}`,
  `Section~\ref{sec:objective}`), the client row $1, \dots, K$, the
  per-client arrows labeled once at client $k$, and the dashed boundary
  of client $k$ within which questions, gold SQL queries and client
  databases remain (`Section~\ref{sec:formulation}`); inside client $k$,
  supervised warm-up in $t = 1, \dots, T_w$ (`Section~\ref{sec:warmup}`,
  `Eq.~\eqref{eq:sft}`) and the preference rounds $t = T_w + 1, \dots, T$
  with steps 1--2 (`Section~\ref{sec:labeling}`), step 3
  (`Section~\ref{sec:pairs}`) and step 4 (`Section~\ref{sec:objective}`,
  `Eq.~\eqref{eq:loss}`); plus the figure's notation and default setting
  `N = {}$\setting{pref.samples}` as above.
- **Sentences outside the caption.** Checked throughout
  `sections/03_method.tex` (including Section 3.3, where
  `Fig.~\ref{fig:overview}` is cited alongside
  `Algorithm~\ref{alg:method}` for the two kinds of round and the role
  of the gold SQL query in each): every sentence outside the caption
  matches the redrawn figure.
- **Simplifications that remain in the figure as drawn.** Step 1 prints
  `N = 10` as fixed text (given by `\setting{pref.samples}` in the
  caption) and draws three sample chips (`SQL 1`--`SQL 3`), paired into
  two chips in step 3 without printing $M$; step 2 shows a label mark on
  every drawn sample, whereas Section 3.5 specifies cases without a
  label; the server bar shows $\theta_1^{t}, \dots, \theta_K^{t}$ (the
  general case where no client has an empty $\mathcal{P}_k^{t}$, whereas
  Section 3.7 and Algorithm 1 state the empty-pair exception); and the
  preference-round banner uses ``reference'' informally in *``gold SQL is
  the reference for the labels, not a target''*, whereas the caption ties
  `reference = $\theta^{t-1}$` in step 4 explicitly to $\pi_{\mathrm{ref}}$.
  Abbreviations in the figure (`FedAvg`, `SFT`, `NLL`, `DPO`, `LoRA`) are
  not re-expanded in the caption because Section 1 already defines all
  five (and Fig. 1 all except `LoRA`).
