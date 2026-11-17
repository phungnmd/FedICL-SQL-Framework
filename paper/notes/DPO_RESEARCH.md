# DPO for federated Text-to-SQL: what the papers show and a design

Written 2026-11-17 from the papers only. It was not checked against the
other notes or against our own results. Section 6 lists which numbers were
read in the paper text and which were not.

Setting assumed: SQL-only output (no chain of thought), a small student,
clients that hold questions with gold SQL and the databases to run them on.

## 1. Short answers

- DPO does not need its own SFT stage before it. It needs a reference model
  that is the model the pairs were sampled from, and a likelihood (SFT) term
  on the correct output inside the loss. An SFT stage before DPO does not
  replace that term.
- For SQL-only output, the published setup with a large gain is CodeLutra:
  pairs from the model's own samples, DPO plus an SFT term, pairs re-sampled
  every iteration. SFT followed by plain DPO gives about zero.
- Dropping the questions where every sample is wrong or every sample is
  correct is sound. They carry no signal, and forcing the too-hard ones
  hurts small models. They are not dropped for good: re-sampling each round
  brings them back when the model can use them.
- Three changes to CodeLutra have support: pair each wrong sample with its
  nearest correct sample, restrict the rejected side of the loss to the
  tokens that differ, and remove questions whose gold SQL returns nothing.
- When the labelled questions stop giving pairs, the next source is
  unlabelled questions on the clients' databases, labelled by agreement of
  execution results.
- In a federated run, one round is one iteration: clients sample from the
  round's global model, label by execution on their own databases, and use
  that global model as the DPO reference. No published federated DPO does
  this; the existing ones use fixed pairs and a fixed reference.

## 2. What the papers show

### 2.1 Is an SFT stage needed before DPO

| Paper | Start of DPO | Likelihood term in loss | Result |
|---|---|---|---|
| DPO (Rafailov 2023) | SFT model when there is one, because the pairs were sampled from it; otherwise a model fitted on the preferred outputs | no | reason given: keep the reference close to the distribution of the pairs |
| CodeLutra (Llama-3-8B) | base model, no SFT stage | yes, on the model's own correct samples | Spider EX: base 59.3, SFT on gold 67.9, iterations 67.8 / 72.4 / 76.6 / 76.3. Without the SFT term: 17.2 |
| Iterative RPO (GSM8K) | base model | yes, length-normalised NLL | DPO from base 61.8, DPO from an SFT model 60.3, SFT on gold 63.5, DPO+NLL 73.1 |
| Arctic-Text2SQL-R1 (GRPO, with reasoning) | SFT model (OmniSQL) | n/a | BIRD dev 67.9 from OmniSQL-32B against 64.9 from Qwen2.5-Coder-32B-Instruct |

Reading: the likelihood term is what matters, and it has to be in the loss.
Without it DPO lowers the probability of the correct output while still
widening the gap to the wrong one (Iterative RPO shows the log-probability
falling, more so from an SFT start; Smaug shows the same when the two
outputs differ in few tokens, which is the usual case for SQL). A stronger
starting model still ends higher (Arctic), so SFT first is not harmful in
itself; it is the plain DPO after it that adds nothing.

CodeLutra's first iteration only equals SFT on gold (67.8 against 67.9).
The gain comes from iterations 2 and 3, each with fresh pairs from the new
model. Its SFT baseline is weak for Spider (LoRA rank 8, split not stated),
so the 8.7 points over SFT should not be expected against a strong SFT.

### 2.2 SQL-only output: what has been measured

| Paper | Setup | Result |
|---|---|---|
| CodeLutra | own samples, DPO + SFT term, 4 iterations | Spider EX 59.3 to 76.6; BIRD EX 22.3 to 43.1 (SFT 35.6) |
| SENSE (CodeLlama-7B / 13B) | SFT, then plain DPO, pairs from a weaker model | against no DPO step: Spider dev +0.9 / +0.1, BIRD dev +1.9 / +2.6 |
| Liu et al. 2025 (10 models, 6.7B to 15B) | SFT on BIRD, then plain DPO, own samples | BIRD dev greedy between -1.3 and +0.8; 6 of 10 models go down. With chain of thought: +0.8 to +4.5 |
| ExCoT (LLaMA-3.1 70B, no CoT rows) | SFT, then DPO | BIRD dev / Spider test: base 57.37 / 78.81, SFT 62.03 / 83.00, DPO row 59.97 / 81.00 |
| Aligning CodeLLMs (code, 7B) | instruct model, plain DPO, own samples | DPO beats SFT on the correct samples only, on all three models; pairs taken from another model end below the starting model |

Three properties separate CodeLutra from the rest: pairs from the model
being trained, the SFT term, and re-sampling every iteration.

### 2.3 Questions where all samples are wrong, or all are correct

CodeLutra does not say what it does with them. Its algorithm samples 10
outputs per question and draws 10 pairs, with replacement when a set is
small, and has no step for an empty set. The only reading that needs no
extra data is that such a question gives no pair in that iteration.

Why that is sound:

- The learning signal of a question grows with p(1-p), p being its share of
  correct samples. Bae et al. prove a bound of this form, largest at
  p = 0.5; in GRPO a group with equal rewards has zero gradient. They keep
  a middle band of pass rates, measured with the current policy at each
  step, and report gains over plain GRPO.
- Too-hard pairs hurt DPO in small models. Gao et al. (ICML 2025) measure a
  9.4% drop in win rate from training on the hardest pairs. Flipping their
  labels does not help, so the cause is capacity more than noise. The share
  of data worth keeping rises with size: 64% for a 3B model, 81% for 14B.
  Filtering gives the gain; easy-to-hard ordering of the kept set adds
  little. Their data is chat alignment, not SQL.
- Text-to-SQL already filters this way. Arctic-Text2SQL-R1 keeps a
  synthetic question only when at least one of 10 samples at temperature
  1.0 is correct: BIRD dev 64.6 to 66.5, Spider test 86.4 to 88.3.

Two cautions:

- "All wrong" in a small sample is not p = 0. A question with p = 0.1 is
  all wrong in 8 samples 43% of the time and in 10 samples 35% of the time;
  with p = 0.2, 17% and 11%. So nothing is dropped for good; each round
  samples again.
- Gold SQL that returns an empty result makes false positives, because many
  wrong queries also return nothing. Arctic removes these questions and the
  ones that run over 5 seconds: 1,687 of 8,659 in Spider train, 1,411 of
  9,428 in BIRD train.

Iterative RPO is the one paper that adds the gold answer as the positive
when no sample is correct. It has no ablation of that choice.

### 2.4 Near-identical pairs

A correct and a wrong SQL query usually differ in a few tokens.

- Smaug: with low edit distance DPO raises the tokens that differ and
  lowers the ones after them, and the probability of the preferred output
  can fall. Its fix (DPOP) is a penalty on that fall, which the SFT term
  already provides.
- Target-DPO: the shared tokens dilute the signal. It keeps the preferred
  side as is and counts the rejected side only on the tokens in the diff.
  Qwen2.5-Coder-7B base, average pass@1 over its code benchmarks: starting
  model 43.9, DPO 41.1, Target-DPO 55.3, with an SFT term added
  (Target-RPO) 56.3. Its pairs are a fixed program against an earlier wrong
  version of the same program, so they are aligned by construction.
- ExCoT picks, in its on-policy rounds, the pair with the smallest edit
  distance, and the largest in its off-policy round.

Neither Target-DPO nor ExCoT's pair choice has been tested on SQL-only
output.

### 2.5 Unlabelled questions

ScPO (Llama-3 8B, GSM8K and MATH) lets the model write new questions from a
few examples, samples 8 answers each, takes the most voted answer as
chosen and the least voted as rejected, drops questions without a clear
majority, and weights the loss (DPO + NLL) by the vote margin. For
rejected answers it samples again at temperature 1.2, because the model
grows more consistent as it trains. Two iterations; a third adds little.

| GSM8K greedy, after 2 iterations | Accuracy |
|---|---|
| Gold labels only (Iterative RPO) | 64.29 |
| ScPO, no labels | 63.91 |
| Gold labels + ScPO on unlabelled questions | 66.64 |

Vote share and accuracy correlate at about 0.8 in their data. For SQL the
vote is over execution results. CodeLutra's own no-gold variant (executable
against non-executable) lifts BIRD EX from 22.3 to 30.9, against 43.1 with
gold.

### 2.6 Federated DPO and federated Text-to-SQL

| Paper | What it does | What it shows |
|---|---|---|
| OpenFedLLM (FedDPO) | DPO inside FedAvg from an instruction-tuned model; fixed preference pairs; reference fixed for all rounds; LoRA only; weights by local data size | every FL algorithm beats local training |
| FedPDPO | adds personal heads and an explicit reward head per client | states that FedAvg + DPO degrades under non-IID data; beta 0.1 better than 0.01 and 0.5 |
| Spadea and Seneviratne | KTO against DPO under seven aggregators | KTO ahead on chat benchmarks; KTO needs no pairs |
| Zhang et al. 2023 (T5-base, 8 Text-to-SQL datasets as clients) | FedAvg, FedProx, FedOPT, and a re-weighting by size times loss reduction in the round (Lorar) | plain FedAvg is far below local training, worst for small clients (macro average 40.03 against 62.78); Lorar lifts FedAvg to 60.16 |

No paper was found that samples the pairs from the current global model
each round, labels them by execution at the client, or does any DPO for
federated Text-to-SQL. One arXiv search for federated Text-to-SQL returned
only Zhang et al. 2023.

## 3. Design for the federated DPO stage

### 3.1 One round

1. The server sends the global model `w_t`.
2. Each client samples M outputs per question from `w_t` at temperature
   1.0, runs them on its own databases and labels each by comparing the
   result with the gold result.
3. Each client builds pairs from the questions that have both correct and
   wrong samples, and counts its questions in three groups: all wrong,
   mixed, all correct.
4. Each client trains for one pass over its pairs with the loss in 3.2,
   with a frozen copy of `w_t` as the reference.
5. The server averages the updates and gets `w_{t+1}`.

The round is the iteration of CodeLutra. Labelling needs the databases and
the gold results, which only the client has, so this stage cannot be done
at the server.

### 3.2 Loss

For a pair (question x, chosen c, rejected r) with weight w:

```
L = - w * log sigmoid( beta * [ D(c) - D_diff(r) ] )  -  lambda * w * log p(c | x) / len(c)
```

- `D(y)` is the log-probability of y under the trained model minus that
  under the reference `w_t`, summed over all tokens of y.
- `D_diff(r)` is the same sum over only the tokens of r that are not in the
  common subsequence with c.
- w = 1 for a pair labelled with gold; the vote margin for a pair from an
  unlabelled question (3.5).
- Starting values from the papers: beta 0.1 and lambda 1 (CodeLutra's
  SQL setting), one epoch per round.

This is Target-RPO's loss with CodeLutra's iteration scheme.

### 3.3 Pairs

- Remove questions whose gold SQL returns an empty result or runs too long.
- Normalise the SQL text (case of keywords, spacing) and drop duplicates,
  so that the diff shows real differences.
- For each distinct wrong sample, pair it with the nearest correct sample
  by token edit distance. The number of pairs of a question is its number
  of distinct wrong samples, not a fixed 10 drawn with replacement, so a
  single correct sample is not repeated ten times against random partners.
- The SFT term runs on the chosen samples. When a FedAvg SFT stage on gold
  comes before this stage, gold is not added again.

### 3.4 Aggregation and non-IID data

- Weight each client by its number of pairs in the round, not by its number
  of questions. A client whose questions are all solved has nothing to
  teach in that round and should not pull the average. This follows the
  idea behind Lorar (weight by how much the client still has to learn),
  with a count instead of a loss difference.
- The reference is the same `w_t` on every client. The DPO term then pulls
  every client relative to the same point, and it saturates once the margin
  of a pair is reached. The SFT term does not saturate, so lambda is the
  knob that trades likelihood for drift between clients. This is an
  inference; no paper measures it.
- A client with few pairs should not loop over them many times; one pass
  per round, with the weight in the first point, keeps it from overfitting.
- Use the same adapter aggregation as the FedAvg SFT stage, so that the
  comparison between the two stages is like for like.
- The three counts per client and round are the stopping signal: when the
  mixed group is nearly empty, more rounds add nothing. They are integers
  and can be sent to the server.

### 3.5 When the pairs run out

In this order:

1. Questions that are all correct: sample again at a higher temperature
   (ScPO uses 1.2) to get rejected samples.
2. Questions that are all wrong: sample more outputs for these questions
   only. A correct sample from the model is a better chosen side than gold,
   because it comes from the model's own distribution.
3. Unlabelled questions on the client's databases: the client generates new
   questions, samples M outputs, groups them by execution result, takes the
   largest group as chosen and the smallest as rejected, drops questions
   without a clear majority, and uses the vote margin as w. A group whose
   result is empty or an error is never the chosen one.
4. Gold as the chosen side for questions that stay all wrong: as an
   ablation only.

Step 3 is the one that adds new information. After SFT the model solves
most of its training questions, so the mixed group is small, and steps 1
and 2 only squeeze the same questions. It also fits the setting: a client
has its databases but few labelled questions.

### 3.6 Left out

- DPOP: its penalty does what the SFT term does.
- Pairs from the teacher or from another model: worse than the starting
  model in Aligning CodeLLMs, small gain in SENSE.
- Personal heads (FedPDPO): the deployed model is one global model.
- KTO: it would bring back the all-wrong and all-correct questions as
  single examples, which 2.3 argues against. Worth a look only if clients
  have too few mixed questions.

## 4. What is taken from where

| Part | Source | What differs here |
|---|---|---|
| Own samples, DPO + SFT term, re-sampling | CodeLutra | run per client inside FedAvg; a round is an iteration |
| DPO in FedAvg | OpenFedLLM | pairs are made each round by execution at the client; reference is the round's global model, not a fixed one |
| Rejected side counted on the diff only, with an SFT term | Target-DPO / Target-RPO | pairs are two independent samples, aligned by nearest-correct pairing; SQL instead of programs |
| Nearest pair | ExCoT | SQL-only output |
| Drop equal-outcome questions, re-sample later | Bae et al., Gao et al., Arctic-Text2SQL-R1 | applied to DPO pairs at clients |
| Unlabelled questions, vote margin weight | ScPO | execution-result vote, at clients |
| Weight by what is left to learn | Zhang et al. 2023 (Lorar) | pair count instead of loss reduction |

## 5. Runs that settle it, shortest first

1. No training: with the current global model, sample 10 outputs per
   training question on each client and report the three counts per client,
   and how many questions have a gold SQL with an empty result. This tells
   how many pairs exist and which step of 3.5 matters.
2. From the same checkpoint and for the same number of rounds: FedAvg SFT
   against the round of 3.1 with the plain loss (DPO + SFT term, random
   pairs). This is the effect of the stage.
3. Add nearest pairing and the diff restriction.
4. Add unlabelled questions, if run 1 shows a small mixed group or run 2
   stops gaining after a round or two.

Risks to read the results against: SFT followed by plain DPO gave about
zero for SQL-only output in two papers (2.2); FedAvg + DPO is reported to
degrade under non-IID data (2.6); the diff restriction and the vote
labelling have no SQL evidence; CodeLutra's peak was at its third
iteration.

## 6. What was checked

Read in the paper text (arXiv HTML): CodeLutra tables, algorithm and
ablation; Liu et al. Table 1 (BIRD dev); ExCoT Tables 1 and 2; SENSE
Table 5; Iterative RPO Table 1; Smaug abstract and loss; DPO's passage on
the reference model; Target-DPO Tables 1, 2 and 4; Aligning CodeLLMs
Table 1; Gao et al. sections 1 to 5; Bae et al. Proposition 3.1 and the
algorithm; Arctic-Text2SQL-R1 sections 4 and 5; ScPO Tables 1 and 2 and
the loss; OpenFedLLM section 3; Zhang et al. Table 2.

Not read in the paper text, so not used above as numbers: Liu et al.'s pair
counts, hyperparameters, Spider table and DPO variants; ExCoT's edit
distance table and pair counts; the result tables of Bae et al. and of
Gao et al.; OpenFedLLM's value alignment table and training settings;
FedPDPO's tables. No code repository of any of these papers was read.
CodeLutra gives no link to code.

## 7. References

- CodeLutra: arXiv 2411.05199
- DPO (Rafailov et al.): arXiv 2305.18290
- Iterative Reasoning Preference Optimization: arXiv 2404.19733
- Smaug / DPO-Positive: arXiv 2402.13228
- Liu et al., chain of thought for DPO in Text-to-SQL: arXiv 2502.11656
- ExCoT: arXiv 2503.19988
- SENSE: arXiv 2408.03256
- Aligning CodeLLMs with DPO: arXiv 2410.18585
- Target-DPO (Focal Preference Alignment): arXiv 2503.02783
- Gao et al., Principled Data Selection for Alignment: arXiv 2502.09650
- Bae et al., Online Difficulty Filtering: arXiv 2504.03380
- Arctic-Text2SQL-R1: arXiv 2505.20315
- ScPO: arXiv 2411.04109
- OpenFedLLM: arXiv 2402.06954
- FedPDPO: arXiv 2603.19741
- Spadea and Seneviratne, KTO and DPO in FL: arXiv 2502.14187
- Zhang et al., Federated Learning for Semantic Parsing: arXiv 2305.17221
