# Outline: Section 3, Method

Target: about 1,530 words (limit 1,700), excluding equations, Algorithm 1
and the caption of Fig. 2. The shares of the brief sum to the limit, so
each is scaled to about nine tenths. 15 paragraphs.

Every entry gives: function (as in `voice.md`, "Method"), proposition,
contents, length. Numbers are named by their macros. Open questions are
in `notes/questions.md`; none of them changes the order below, and the
entries they touch say so.

## Section lead (no heading)

**L. Location of the novelty.** About 45 words.
- Function: contribution orientation at the opening of the method section.
- Proposition: \method differs from FedAvg SFT in the origin of its
  supervision (execution on the client databases, in addition to the gold
  SQL query) and from FedDPO in three located respects: the pairs are the
  model's own samples labeled by execution, pairs and reference model are
  renewed in every round, and the loss retains an NLL term.
- No roadmap sentence beyond a clause; the subsection titles carry the order.

## 3.1 Problem Formulation (`sec:formulation`), about 260 words

**1. Setting and notation.** About 140 words.
- Function: problem formulation, setting.
- Proposition: $K$ clients each hold questions, gold SQL queries and the
  databases on which they execute, and none of the three leaves the client
  (data isolation); what is trained, communicated and aggregated is one
  LoRA adapter on a frozen pretrained model.
- Contents: $\mathcal{D}_k$ with elements $(q, d, y^\star)$, $n_k$; the
  prompt $x$ (question, schema as `CREATE TABLE` statements; rows on
  Spider, external knowledge on BIRD; `fig:prompt`), identical in training,
  sampling and evaluation; $\pi_\theta$; $T$ rounds with full
  participation; $\theta^{t}$, $\theta_k^{t}$; local training from
  $\theta^{t-1}$ with a newly initialized optimizer. Cites `hu2022lora`.

**2. The objective of FedAvg SFT and what supervises it.** About 120 words.
- Function: problem formulation, learning objective; it ends on the
  deficiency that the rest of the section answers (point 1).
- Proposition: in FedAvg SFT the target of the local objective is the gold
  SQL query alone. The database enters only as text of $x$, no query is
  executed on it, and the model receives no signal about which of its own
  queries are incorrect.
- Contents: Eq. `eq:sft`, Eq. `eq:aggregation`; a client uploads its
  adapter and $n_k$. Cites `mcmahan2017fedavg`, `ye2024openfedllm`.
- The argument is the definition itself; no result is quoted.

## 3.2 Execution-Derived Supervision (`sec:supervision`), about 135 words

**3. The signal, its locality and its prevalence.** About 135 words.
- Function: the key observation, stated formally and measured (point 2).
- Proposition: comparing $\mathrm{exec}(y, d)$ with
  $\mathrm{exec}(y^\star, d)$ partitions the model's own samples for a
  question into correct and incorrect ones, so one gold SQL query yields
  many labeled queries, the model's errors among them. The partition needs
  $d$ and $y^\star$ and is therefore computable only at the client.
- Contents: definition of $\mathrm{exec}(y, d)$. The one measurement of
  the section: for the global model after `\setting{rounds.warmup}` rounds
  of FedAvg SFT, `\fact{cost.bird.pref1.paired_pct}`% of the
  `\fact{cost.bird.pref1.questions}` BIRD training questions have both a
  correct and an incorrect sample among $N$ =
  `\setting{pref.samples}`.
- Stated as "both a correct and an incorrect sample", because the
  preference pair is not yet defined here; on BIRD the two sets coincide.
  BIRD only: the Spider percentage needs the exclusion of the databases
  without rows, which belongs to 3.6.

## 3.3 Framework Overview (`sec:overview`), about 170 words

**4. Four components, one aggregation rule, two kinds of round.** About 170 words.
- Function: framework overview.
- Proposition: \method, a federated learning framework for Text-to-SQL,
  adds execution-derived supervision to federated training through four
  components, each designated with its role in one clause: supervised
  warm-up (supplies correct samples), client-side execution labeling
  (turns the client databases into labels), on-policy pair construction
  (renews the pairs with every global model), the preference objective
  (trains on the pairs against that model). Rounds $1, \dots, T_w$ are
  warm-up rounds, rounds $T_w + 1, \dots, T$ preference rounds; the
  aggregation differs between them only in its weights.
- Contents: Fig. 2 (`fig:overview`, one preference round) and Algorithm 1
  (`alg:method`, the complete run), both placed here; the default $T$,
  $T_w$, $N$, $M$ by macro, with `tab:settings` for the rest; one forward
  reference to `sec:main` and `tab:main` for the gain of the complete
  framework.
- Caption of Fig. 2 (not counted): the path of one preference round, and
  that only adapters and pair counts are transmitted.

## 3.4 Supervised Warm-Up (`sec:warmup`), about 170 words

**5. Why and what.** About 95 words.
- Function: component, motivation then definition.
- Proposition: a preference pair requires a correct sample, and a question
  whose labeled samples are all incorrect yields none. The warm-up rounds
  are FedAvg SFT rounds (Eq. `eq:sft`, Eq. `eq:aggregation`, one local
  epoch) and raise the number of questions for which the model has a
  correct sample.
- Contents: `\fact{warmup.bird.k0.no_correct}` of
  `\fact{cost.bird.pref1.questions}` BIRD training questions without a
  correct sample for the pretrained model,
  `\fact{warmup.bird.k2.no_correct}` after `\setting{rounds.warmup}`
  warm-up rounds.

**6. Status of $T_w$.** About 75 words.
- Function: component, interpretation.
- Proposition: warm-up is a setting and not a precondition. The pretrained
  model already yields pairs, Algorithm 1 is defined for $T_w = 0$, and
  the warm-up rounds add nothing to the protocol, since they are the
  rounds of the baseline. The effect of $T_w$ on accuracy is referred to
  `sec:ablation` and not anticipated.
- Depends on questions 1 and 2: whether the net effect on the number of
  questions that yield pairs can be stated, and whether
  $\pi_{\theta^{0}}$ may be called the pretrained model. Without answers
  the paragraph keeps to the scoped count of paragraph 5.

## 3.5 Client-Side Execution Labeling (`sec:labeling`), about 220 words

**7. Sampling and the label.** About 125 words.
- Function: component, motivation then definition (point 5).
- Proposition: FedAvg SFT never queries the databases, and the two sides
  of a FedDPO pair are labeled by a dataset. Here the client draws $N$
  queries per training question from $\pi_{\theta^{t-1}}(\cdot \mid x)$
  and labels each by execution on $d$: correct if and only if
  $\mathrm{exec}(y, d) = \mathrm{exec}(y^\star, d)$.
- Contents: temperature `\setting{pref.t}` without nucleus or top-$k$
  truncation, at most `\setting{pref.tokens}` new tokens; the time limit
  and the comparison of results are those of the evaluation metric
  (`sec:setup`); a sample that fails to execute, exceeds the time limit or
  contains no query is incorrect.

**8. Unlabeled cases and locality.** About 95 words.
- Function: component, completion of the definition, then interpretation.
- Proposition: the label requires the gold SQL query and the database, so
  it exists only at the client, and it is computed with no exchange beyond
  the global adapter that the round delivers in any case. Because sampling
  is untruncated at temperature `\setting{pref.t}`, the labeled samples
  are draws from the distribution of the current global model.
- Contents: no label for a sample cut at the token limit, for the BIRD
  case of the shared time limit, and for every sample of a question whose
  gold SQL query fails to execute or exceeds the limit (counts in
  `sec:setup`).
- The coincidental match on one database is a limitation of Section 6 and
  is not raised here.

## 3.6 On-Policy Preference Pair Construction (`sec:pairs`), about 180 words

**9. Deficiency and definition.** About 110 words.
- Function: component, motivation then definition (point 6).
- Proposition: FedDPO trains each client on a fixed preference dataset
  whose two sides are not outputs of the model under training; \method
  constructs $\mathcal{P}_k^{t}$ in every preference round from that
  round's labeled samples.
- Contents: for each question with a correct and an incorrect sample, $M$
  of each, drawn uniformly and independently (without replacement when $M$
  of that label exist, with replacement otherwise), paired in the order
  drawn; $\lvert\mathcal{P}_k^{t}\rvert$ is $M$ times the number of such
  questions. No pair: samples all correct, all incorrect or unlabeled, and
  databases whose tables contain no rows. Both sides of a pair are
  samples; the gold SQL query does not stand in for a missing correct
  sample (question 5 asks whether `sec:ablation` may be cited for this).
  Cites `ye2024openfedllm`.

**10. A federated round as one resampling step.** About 70 words.
- Function: component, interpretation.
- Proposition: the pairs come from the global model that the round
  distributes, which is also the reference model. The errors of each new
  global model are therefore identified anew, errors it no longer makes
  leave the training data, and no communication is added. $M$ fixes the
  weight of a question and, with one local epoch, the length of local
  training.
- Contents: every question is sampled again in the next preference round;
  forward reference to `sec:ablation` for the variant with fixed pairs and
  fixed reference model, without its numbers.

## 3.7 Preference Objective and Aggregation (`sec:objective`), about 350 words

**11. Definition of the objective.** About 85 words.
- Function: component, formal definition (point 7).
- Proposition: the local objective of a preference round is the mean over
  $\mathcal{P}_k^{t}$ of a preference term, the DPO loss with
  $\pi_{\mathrm{ref}} = \pi_{\theta^{t-1}}$, plus $\lambda$ times the NLL
  of the correct sample. The form is adopted, not claimed: a preference
  loss with an NLL term on the preferred response is established in
  centralized training.
- Contents: Eq. `eq:logratio`, Eq. `eq:loss`; token sums in $m_\theta$,
  token mean in the NLL term as in Eq. `eq:sft`; $\beta$ =
  `\setting{pref.beta}`, $\lambda$ = `\setting{pref.nll}`. Cites
  `rafailov2023dpo`, and `pang2024irpo`, `tao2024codelutra` once.

**12. The reference model.** About 65 words.
- Function: component, interpretation.
- Proposition: at the start of local training $\theta = \theta^{t-1}$,
  hence $m_\theta = 0$ for every pair: the reference model, the model that
  generated the samples and the initialization of every client coincide.
  The preference term thus measures the change made within the round,
  against the model whose errors the pairs record. FedDPO retains one
  reference model for the whole federated process.

**13. Two terms, two roles.** About 90 words.
- Function: component, interpretation.
- Proposition: the preference term constrains only a difference of
  log-ratios. It is invariant to a common shift of
  $\log \pi_\theta(y^{+} \mid x)$ and $\log \pi_\theta(y^{-} \mid x)$ and
  can decrease while both decrease. The NLL term fixes what the difference
  leaves undetermined by raising the log-likelihood of the correct sample
  itself. The preference term in turn is the only one that uses the
  incorrect sample, the signal that FedAvg SFT lacks.
- Contents: forward reference to `sec:ablation` and `tab:ablation`, where
  each term is removed in turn. The numbers of point 7 stay in Section 5.

**14. Aggregation and communication.** About 60 words.
- Function: algorithm and complexity, communication (point 8).
- Proposition: Eq. `eq:aggregation` with $\lvert\mathcal{P}_k^{t}\rvert$
  in place of $n_k$; a client transmits its adapter
  (`\setting{adapter.mb}`) and one integer, exactly as in a warm-up round,
  so the communication per round is unchanged.
- Contents: a client with empty $\mathcal{P}_k^{t}$ does not train, sends
  no update and has weight zero; samples, execution results, execution
  labels and pairs remain at the client. The choice of weights is referred
  to `sec:ablation`.

**15. Client computation.** About 50 words.
- Function: algorithm and complexity, computation.
- Proposition: what a preference round costs is client computation:
  generation of $N n_k$ samples, their execution, and one epoch over
  $\mathcal{P}_k^{t}$ in which each pair is scored by the model and by
  the reference model, against one epoch over $\mathcal{D}_k$ in a
  warm-up round.
- Contents: forward reference to `sec:cost` and `tab:cost` for the
  measured times.

## Decisions that depart from a literal reading of the materials

1. **Lead paragraph.** `voice.md` asks for the novelty at the opening of
   the method section; the fixed headings leave no subsection for it, so
   it stands before 3.1 and is paid for by the scaled shares.
2. **Where symbols are defined.** `terms.md` says the notation is
   "defined in Section 3.1". The outline defines the symbols of the
   setting there and those of a component ($\mathrm{exec}$, $N$, $M$,
   $y^{\pm}$, $\mathcal{P}_k^{t}$, $\beta$, $\lambda$, $T_w$) where the
   component is defined. Symbols and meanings are unchanged.
3. **No number of Section 5.** Points 6 to 8 of the brief list their
   evidence (2.61 EX, the execution-error counts, the aggregation
   weights). The section points to `sec:ablation` and `sec:cost` and
   quotes none of it, as "Place in the manuscript" requires.
4. **Cost wording, paragraph 15.** Point 8 calls local training on the
   pairs an additional cost. Table 8 does not support that in general:
   the pair set shrinks, and the second preference round on Spider takes
   `\fact{cost.spider.pref2.gpu_ratio}` of the GPU time of a FedAvg SFT
   round. The paragraph therefore names the operations of each kind of
   round and leaves the comparison to Section 5.6.
5. **No table for communication and computation.** The table of the brief
   is rendered as paragraphs 14 and 15, since the tables of the paper are
   numbered and fixed. If a compact table is wanted, it would replace
   about 80 words.
