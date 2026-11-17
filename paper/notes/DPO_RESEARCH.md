# DPO for federated Text-to-SQL: what the papers show and a design

Written 2026-11-17 from the papers only. It was not checked against our
own results. Section 6 lists which numbers were read in the paper text and
which were not.

Section 3 follows the method as the owner set it on 2026-11-17: the
federated DPO rounds are the core, pre-training at the server with the
same loss is a secondary part, and the teacher is a research direction
outside the method.

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
  execution results. The method does not use them (owner, 2026-11-17): it
  stays on the labelled questions.
- In a federated run, one round is one iteration: clients sample from the
  round's global model, label by execution on their own databases, and use
  that global model as the DPO reference. No published federated DPO does
  this; the existing ones use fixed pairs and a fixed reference.
- Pre-training on public data before the rounds fits this design better
  than SFT on the clients' questions: it gives general SQL skill and
  leaves the clients' questions unseen, so they still give pairs.
- No paper shows a teacher's SQL to be a better target than gold SQL for
  Text-to-SQL. The one use of a teacher with a measured gain over gold
  alone is a reverse-KL term on the student's own samples (KID).
- Gold SQL as the chosen side when no sample is correct is used by one
  paper on one dataset (Iterative RPO on GSM8K), without an ablation. The
  others drop the question.

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
when no sample is correct. It has no ablation of that choice (2.9).

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

### 2.7 A teacher or another LLM in the loop

What a larger model does in the preference-optimization papers:

| Role of the larger model | Papers | For SQL-only output |
|---|---|---|
| Writes the reasoning chain | ExCoT (GPT-4o), Liu et al. | not used: no chain of thought here |
| Gives both sides of off-policy pairs | ExCoT (GPT-4o), SENSE (a weaker model) | mixed: in Aligning CodeLLMs, pairs from another model end below the starting model |
| Its output is the chosen side and the student's output the rejected side, with no check of correctness | PLaD, DPKD | both assume the teacher is always better and work on open text; SQL can be checked by execution |
| Judges which output is better | CodeLutra, appendix | execution is the better judge: 48.2 against 27.8 with GPT-4 as judge on DS-1000 |
| Writes test cases to filter pairs | Target-DPO (GPT-4o) | not needed: the gold result exists |
| Writes new questions | SENSE (GPT-4), Distill-C; in ScPO the model itself | usable, and the student can do it (2.5) |

PLaD (summarisation, student after SFT): win rate 35.13 with SFT on gold,
37.70 with standard KD, 40.46 with PLaD. DPKD (GPT-2 120M, ROUGE-L on
Dolly): 23.3 with SFT, 22.8 with KD, 24.6 with DPKD.

A teacher's answers against gold as the training target:

| Paper | Comparison | Result |
|---|---|---|
| Kim and Rush (translation, 2016) | student trained on the teacher's output instead of gold | better: +4.0 BLEU with greedy decoding; matching the teacher's token probabilities gives +0.8 |
| Iterative RPO (maths, step-by-step solutions) | SFT on the model's own correct samples against SFT on gold | 65.2 against 63.5 |
| CodeLutra (SQL) | the model's own correct samples against SFT on gold | equal: 67.8 against 67.9 |
| KID (Text-to-SQL, 0.5B student) | data generated by teacher and student against KD on gold | about equal on Spider dev: 57.6 to 59.6 against 57.3 |
| ExCoT | GPT-4o outputs that execute correctly as the SFT set | no comparison with gold; 5.6k of the 9,428 BIRD train questions are kept |

The two cases where the teacher's output beats gold are outside SQL. For
SQL the reason is plain: a teacher's query is kept only when its result
equals the gold result, so it carries no more information about the
answer, and the questions the teacher gets wrong are lost.

The teacher's token distribution, with gold still the target. KID (EMNLP
Findings 2024) is the one Text-to-SQL paper found with a row for a student
trained on gold alone. Student Qwen1.5-0.5B; teachers Qwen1.5 1.8B, 4B and
7B, fine-tuned on the same data.

| Distillation | Against the student trained on gold alone (average of 5 benchmarks) |
|---|---|
| Forward KL on the gold sequences (Hinton's form) | -0.9 to -0.1 |
| Reverse KL on the gold sequences | +0.8 to +3.1 |
| Reverse KL on sequences the student generated (GKD) | +3.1 to +4.6 |
| KID | +3.2 to +4.7 |

On Spider dev the student goes from 57.8 to between 63.7 and 65.8. The KD
rows also carry an MLE term on gold, so the comparison with the gold-only
row is not fully like for like. The weakest teacher (1.8B; BIRD 34.2 with
evidence, Spider dev 67.3) still gives +3.17 on average, so the gap
between teacher and student matters more than the teacher's own level.
KID's teachers are fine-tuned on the task data; a frozen teacher, as ours
would be, is not tested.

### 2.8 Pre-training before the rounds

| Paper | Result |
|---|---|
| Chen et al. (ICLR 2023) | CIFAR-10, alpha 0.3: the gap between FedAvg and centralized training falls from 9.0 to 2.5 points with a pre-trained start; the gain grows with the skew. Pre-training on a distant domain gives nothing (ImageNet for chest X-ray: 69.1 against 68.9 from random weights) |
| Nguyen et al. (ICLR 2023) | a pre-trained start narrows the gap between IID and non-IID data, allows more local epochs, and narrows the differences between federated optimizers |
| Wang et al. 2023 (models under 10M parameters) | pre-training on public data: accuracy 20.68 to 28.01. With distillation from an LLM: 28.68, from 1% of the public data. Public data chosen with the federated model: 0.08% of it matches all of it |
| Yu et al. | small models have limited capacity; public data chosen to be close to the private data beats all of it (SST-2, 5M model: +4.6%) |
| OmniSQL (7B) | training on SynSQL alone: Spider test 82.2 to 83.5, BIRD dev 50.9 to 59.9. With Spider and BIRD train added: 87.9 and 63.9 |
| CodeS | the smaller the model, the larger the gain from pre-training: +10 to 12 points for the 1B model on Spider dev few-shot, +6 to 7 for the 7B model. SFT on Spider or on BIRD reaches 11.0 and 12.1 EX on a bank domain, 71.4 with data of that domain; the paper names annotation habits as the cause |
| Tramèr et al. | when the public data is close to the private data, benchmarks overstate what pre-training gives |

The two ICLR papers do not agree on the mechanism: Nguyen et al. say the
clients' updates point in closer directions, Chen et al. that client drift
is not reduced and the aggregation step is what gets more stable.

For DPO rounds with no SFT stage before them, pre-training on public data
does five things. The first four are inferences from the papers above and
from sections 2.1 to 2.6; no paper measures them in this combination.

1. It gives skill without spending the clients' pairs. SFT on the clients'
   own questions makes the model solve most of them, and DPO then has few
   pairs left (the result of Liu et al., 2.2). Public data has other
   databases, so the clients' questions stay new to the student.
2. It moves questions between the three groups: hard ones from all wrong
   to mixed, easy ones from mixed to all correct. Whether the number of
   pairs goes up or down has to be counted.
3. It takes the place of the first iteration. CodeLutra's first iteration
   only equals SFT on gold; the gain comes in iterations 2 and 3. With a
   pre-trained start the federated rounds begin where the gain is.
4. It makes FedAvg more stable, where FedPDPO reports FedAvg with DPO to
   degrade under non-IID data.
5. The advantage of a stronger start remains after preference training
   (Arctic-Text2SQL-R1: 67.9 against 64.9 on BIRD dev).

Two risks: Spider is easy, so the mixed group may be small after
pre-training; and a model with a more peaked distribution gives less
varied samples at temperature 1.0 (ScPO raises the temperature to 1.2 for
the rejected side).

What pre-training cannot bring is the client's own schemas, contents and
annotation habits (CodeS, OmniSQL above). That part is left to the rounds
at the clients. Using the same prompt at the server and at the clients
removes the part of the mismatch that is only format.

### 2.9 Gold SQL as the chosen side

Iterative RPO on GSM8K: "Since some problems might not have any
model-generated correct solution, we include the gold human written
solution (c_i, y_i) in the winning set G_i^w so it is not empty". On ARC
it skips such questions, because the dataset has no gold solution; for
MATH it does not say. There is no ablation of the choice.

The other papers: CodeLutra does not say (2.3); ScPO drops questions
without a clear majority; SENSE takes as positive the output of a weaker
model that matches the gold result, not the gold SQL itself.

Reasons the papers give or measure:

1. Gold has no reasoning chain. Most recent DPO work trains chains of
   thought, and gold is only the answer. This reason does not apply to
   SQL-only output.
2. The pair is off the reference distribution. DPO assumes the pairs are
   sampled from the reference model; gold is not.
3. The hardest questions hurt small models, and an all-wrong question is
   among the hardest (Gao et al., 2.3; chat data).

Inferences, not measured in any paper:

- A shortcut by style. Gold differs from the model's output in wording as
  well, so the model can separate the two without fixing the error.
- Redundancy. Gold can already enter through the SFT term; the pair adds
  only that this one wrong sample is wrong.

## 3. Design

The core is 3.1 to 3.5: the federated rounds. 3.6 is the secondary part,
3.7 the teacher as a research direction, 3.8 the choices the owner made
inside the rounds.

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
the gold results, which only the client has, so this cannot be done at the
server. Round 1 starts from the base student, or from the student after
the pre-training of 3.6. No SFT stage on the clients' questions comes
before it.

### 3.2 Loss

For a pair (question x, chosen c, rejected r) with weight w:

```
L = - w * log sigmoid( beta * [ D(c) - D_diff(r) ] )  -  lambda * w * log p(c | x) / len(c)
```

- `D(y)` is the log-probability of y under the trained model minus that
  under the reference `w_t`, summed over all tokens of y.
- `D_diff(r)` is the same sum over only the tokens of r that are not in the
  common subsequence with c. The plain form has `D(r)`, all tokens of r,
  in its place; which of the two the method uses is decided by a run
  (3.8).
- w = 1. A vote margin would take its place only for pairs from
  unlabelled questions, which the method does not use (3.8).
- A question whose samples are all wrong has no pair and adds nothing in
  the base form. The candidate to check is that it adds the second term
  alone, on its gold SQL (3.8).
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
  This pairing is a candidate, like the diff restriction of 3.2; the plain
  form draws the pairs at random (3.8).
- The SFT term runs on the chosen samples. With no SFT stage before the
  rounds, a question whose samples are all wrong meets its gold SQL
  nowhere; adding its gold SQL to the SFT term is an experiment to run
  (3.8).

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
- Use the same adapter aggregation as the FedAvg SFT baseline, so that the
  comparison with it is like for like.
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
   ablation only (2.9).

Step 3 is the one that adds new information; steps 1 and 2 only squeeze
the same questions. It also fits the setting: a client has its databases
but few labelled questions. It is outside the method (owner, 2026-11-17),
which stays on the labelled questions; it is kept here as what the papers
offer beyond that.

### 3.6 Pre-training at the server (secondary part)

Before round 1 the server runs the same loop on the public data (BIRD
train or SynSQL): sample from the student, run the samples on the public
databases, label them against the gold result, build pairs as in 3.3 and
train with the loss of 3.2. The reference of an iteration is the model at
its start. No teacher is involved.

- The prompt is the one the clients use.
- The number of iterations is open. CodeLutra runs 4 with the peak at the
  third.
- Its place in the paper is the starting point of the rounds. It is
  measured by two things: the three counts on the clients' questions
  before and after it (section 5, run 1), and the rounds from the
  pre-trained student against the rounds from the base student.
- SFT on the public gold SQL is the other way to pre-train and the control
  for this part.

What it is expected to do, and its two risks, are in 2.8.

### 3.7 The teacher (research direction, not in the method)

The method above uses no teacher. If the direction is taken up, the form
with evidence is a reverse-KL term to the teacher on the student's own
samples, at the server, added to a loss that keeps gold as the target
(KID, 2.7). What to check first:

- The control is the server part without the teacher. A teacher row that
  is not above it shows no effect of the teacher.
- KID's teachers are fine-tuned on the task data and ours is frozen.
- Forward KL to the teacher on the gold sequences is the form that ends
  below gold alone in KID.
- The teacher's SQL as the chosen side of a pair has no support for SQL
  (2.7).

The other role with support is writing new questions on public databases
(SENSE, OmniSQL, Distill-C), which the student can also do (3.5, step 3).

A question to guide the direction (owner, 2026-11-17; not a planned
part): can the LLM act as the repairer of the student's wrong SQL instead
of the writer of an answer?

- Where: at the server, on public data, for the questions whose samples
  are all wrong, the blind spot of the on-policy loop.
- How: the teacher gets the schema, the question, one wrong SQL of the
  student and its execution result, and is asked for the smallest fix.
  The fix is run; if its result equals the gold result it becomes the
  chosen side and the wrong SQL the rejected side, otherwise it is
  dropped.
- Why it could add something gold does not: the pair is close by
  construction, as in Target-DPO, whose pairs are a fixed program against
  its earlier wrong version (2.4). A wrong repair is removed by execution,
  so the teacher's level sets the number of pairs, not their correctness.
- What it does not reach: all-wrong questions at the clients, where no
  LLM runs.
- A check without training: on BIRD train, the share of the student's
  all-wrong questions for which a repair matches the gold result, and the
  edit distance from the wrong SQL to the repair against that to the gold
  SQL. If the repair is not clearly closer, gold is enough.
- The control in training: gold SQL as the chosen side for the same
  questions.

Three searches found no paper that builds DPO pairs this way for
Text-to-SQL. The nearest seen, in search results only and not read:
Distill-C (its FixIt part starts from a model's errors) and SQLCritic (a
DPO variant for clause-wise correction).

### 3.8 Choices made inside the rounds (owner, 2026-11-17)

1. The gold SQL of an all-wrong question in the SFT term (never as the
   chosen side of a pair) is an experiment to run, not a part of the
   method yet. The base form leaves such a question out of the round. For
   it: with no SFT stage, the question otherwise gives nothing, and
   Iterative RPO adds gold in this case. Against it: these are the hardest
   questions (Gao et al.), and no paper measures the choice.
2. The diff restriction of 3.2 and the nearest-correct pairing of 3.3 join
   the method if a run shows a clear gain over CodeLutra's plain loss with
   random pairs. Otherwise the plain form stays. Neither has been tested
   on SQL in a paper.
3. Unlabelled questions (3.5, step 3) are not in the method. The method is
   about the labelled questions the clients already hold.

### 3.9 Left out

- DPOP: its penalty does what the SFT term does.
- Pairs from the teacher or from another model: worse than the starting
  model in Aligning CodeLLMs, small gain in SENSE.
- The teacher's output as the chosen side against the student's output
  (PLaD, DPKD): it assumes the teacher is right, which execution can check
  and which fails for about half of BIRD train with a 7B teacher.
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
| Pre-training on public data before the rounds | Nguyen et al., Chen et al. (federated learning); OmniSQL, CodeS (Text-to-SQL) | pre-training with the DPO loss of the rounds, not with SFT |

## 5. Runs that settle it, shortest first

1. No training: sample 10 outputs per training question on each client
   and report the three counts per client, and how many questions have a
   gold SQL with an empty result. Once from the base student and once from
   the student after the pre-training of 3.6. This tells how many pairs
   exist, whether the pre-training adds or removes pairs, and which step
   of 3.5 matters.
2. From the base student and for the same number of rounds: FedAvg SFT
   against the rounds of 3.1 with the plain loss (DPO + SFT term, random
   pairs). This is the effect of the core.
3. On top of run 2, each against it: the gold SQL of all-wrong questions
   in the SFT term; nearest pairing with the diff restriction. Each joins
   the method only on a clear gain over run 2. Run 1 says first how many
   questions the gold SQL would touch.
4. The rounds from the pre-trained student against run 2, with SFT on the
   public gold SQL as the other starting point. This is the effect of the
   secondary part.

Not planned: unlabelled questions (3.8).

Risks to read the results against: from a base model CodeLutra's first
iteration only equals SFT on gold, so a gain over FedAvg SFT needs several
rounds; FedAvg + DPO is reported to degrade under non-IID data (2.6); the
mixed group may be small after pre-training (2.8); the diff restriction
and the vote labelling have no SQL evidence; CodeLutra's peak was at its
third iteration.

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

Sections 2.7 to 2.9: the sentence of Iterative RPO on gold in the winning
set was read word for word. The numbers of KID, PLaD, DPKD, Kim and Rush,
Chen et al., Nguyen et al., Wang et al. and Yu et al. were read through a
page-extraction tool on the arXiv pages and not checked against the PDF
tables. The OmniSQL and CodeS tables came the same way and need a check
against the PDF before they are cited. That Liu et al. drop the all-wrong
and all-correct questions was not checked in the paper. "About half of
BIRD train" for a 7B teacher rests on ExCoT's 5.6k of 9,428 with GPT-4o
and on the zero-shot BIRD dev level of Qwen2.5-Coder-7B in OmniSQL's table
(50.9), not on a count of our teacher's outputs.

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
- KID, Learning from Imperfect Data (distillation for Text-to-SQL): arXiv 2410.11371
- Kim and Rush, Sequence-Level Knowledge Distillation: arXiv 1606.07947
- PLaD: arXiv 2406.02886
- DPKD: arXiv 2406.19774
- Distill-C: arXiv 2504.00048
- SQLCritic: arXiv 2503.07996
- Nguyen et al., Where to Begin? (pre-training and initialization in FL): arXiv 2206.15387
- Chen et al., On the Importance and Applicability of Pre-Training for FL: arXiv 2206.11488
- Wang et al., Can Public LLMs Help Private Cross-device FL?: arXiv 2305.12132
- Yu et al., Selective Pre-training for Private Fine-tuning: arXiv 2305.13865
- Tramèr et al., Considerations for DP Learning with Public Pretraining: arXiv 2212.06470
- OmniSQL: arXiv 2503.02240
- CodeS: arXiv 2402.16347
