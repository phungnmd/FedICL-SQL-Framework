# Section 3, Method: checks and editor's notes

Draft: `sections/03_method.tex`. The writer's outline:
`briefs/03_method_outline.md`; the writer's notes:
`briefs/03_method_notes.md`. PDF: `make`, then `build/main.pdf`.

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief and the earlier draft of Section 3.4, and no
other file. One agent wrote the outline, the draft and the revision.

## 1. Outline

The outline covered every statement of the brief in 24 paragraphs and
1,485 words. Four points went back before the draft: the contrast with
FedAvg SFT made once, in Section 3.2, and not again at the end of 3.3;
"only the client can compute the label" as a clause in 3.4; the
paragraph on the reference model and on the NLL term split in two;
Algorithm 1 cited first in 3.2 with Fig. 1. Statement 3 of Section 3.3
of the brief was folded into statement 1 of Section 3.2 for that
reason.

## 2. Checks of the first draft

| Check | Result |
|---|---|
| Build | compiles in the class of the manuscript; no undefined reference or citation, no overfull box |
| Lint | 0 stops. Notes: LoRA, FedAvg, SFT and FedDPO without their long form, which Sections 1 and 2 give; one "may" (a question may yield pairs in a later round) |
| Length | 1,554 words of running text, formulas not counted (asked: 1,490, 1,650 at most); Section 3.4 has 746 (750 at most) |
| Pages | about 4.5 pages against the 4.0 of the plan. The text is 64 words over its length; the rest is Fig. 1 (0.6 page), Algorithm 1 and the four displayed equations, which take about 1.85 pages where 1.5 were planned |
| Macros | every setting is a macro and prints its value; no number prints as `??`. Two numbers are words: "four times" (2M with M = 2) and "CodeLutra constructs ten" |
| Terms | those of `TERMS.md` throughout; symbols as in its notation |
| Ceilings | kept: the label is defined through the execution result of the gold SQL query; no result is quoted; Sections 5 and 6 are pointed to; nothing on differential privacy, client drift or convergence |
| Facts | every statement agrees with the brief and with the code |
| Argument | the first sentences of the paragraphs follow the outline; no paragraph with two points |
| Text taken from the brief or the voice folder | none (one run of six words, "to minimize the negative log likelihood") |

Register against the method sections of the ten papers (a signal for
the editor, not sent to the writer): sentence length 23.9 words (22.5),
letters per word 4.92 (5.58), sentences with "we" 12.7% (39.0%),
passive sentences 14.1% (20.8%).

## 3. Cold read

A helper on Opus that had seen neither the brief nor the notes read the
six pages as a reviewer of the journal. It could reimplement the loop
from the text. Its twelve findings, by weight:

| # | Finding | Weight | What was done |
|---|---|---|---|
| 1 | At the paragraph on CodeLutra the method reads as "CodeLutra run inside FedAvg": the two differences named are a smaller M and a normalization | major | note 1; the brief now gives the differences in kind |
| 2 | The reason for the warm-up rounds shows that the gold SQL query is needed somewhere, not that it belongs in earlier rounds; the alternative of using it as the correct side inside a preference round is not mentioned | major | not sent: the section may give no result. For the owner, section 5 |
| 3 | No reason for averaging the NLL term over tokens | minor | note 2 |
| 4 | The reason for the weights covers only the client without pairs | minor | note 2; the brief now carries the reason and the pointer to Section 6 |
| 5 | "On-policy" against FedDPO is drawn strongly for two preference rounds | minor | not sent; a question for Section 6 |
| 6 | Three labeling steps that need a guess: the comparison "of the benchmark", the sample "that contains no SQL query", "the tables of d contain no rows" | minor | note 3; the brief now states each |
| 7 | No pointer to the settings of local training | minor | note 3 |
| 8 | Repetition: what travels and what stays (five places and Fig. 1), the bound on local training (twice), the preference round told three times before it is specified | minor | note 4 |
| 9 | The reason for M = 2 is one of cost only | minor | not sent: the claim is limited to cost (`CLAIMS.md`, section 7, item 8) |
| 10 | The sentence on the reference model carries three reasons | remark | note 5 |
| 11 | Averaging the two factors of a LoRA matrix apart does not average their product | remark | not sent |
| 12 | The pair written with and without x; "the loss of Eq. (1)" for one summand; Fig. 1 writes L = L_DPO + L_NLL | remark | note 5 (the figure is left as it is) |

## 4. Editor's notes, round 1

1. What is ours against the closest work: the paragraph on CodeLutra
   has to say what the federated setting changes.
2. Two choices without their reason: the NLL term averaged over
   tokens; the weight by the number of pairs, with the pointer to
   Section 6.
3. Steps of the labeling that need a guess, and the missing pointer to
   the settings of local training.
4. Length and points made more than once; the brief now asks for about
   1,420 words (1,490 at most), Section 3.5 first.
5. Places where the reader stopped on the form: the sentence on the
   reference model, the notation of a pair, the summand of Eq. (1), the
   caption against the text on what travels, the place of the citation
   of Algorithm 1.

Changes to the brief for these notes: the length; how a sample is read
and the empty sample; the database without rows; the reason for the
weights; the differences in kind from CodeLutra.

## 5. Revision 1 and the second cold read

Revision 1 answered the five notes: 1,484 words (Section 3.4: 787),
about 4.3 pages, build and lint clean. 31% of its words stand in runs
of five or more words of the brief (the accepted pilot: 28%); the facts
of the next briefs are to be written in shorter shorthand.

A second helper on Opus, fresh, read the pages of revision 1. It stated
the method correctly and listed what follows CodeLutra and what
differs. Its eight findings:

| # | Finding | Weight | What was done |
|---|---|---|---|
| 1 | The differences from CodeLutra are listed side by side; the reader cannot tell which the authors claim, and reads "CodeLutra's loop with these changes" | major | note 1; the brief now says which difference is the claim and which are settings |
| 2 | The reason for the warm-up rounds still lacks its step, and the gold SQL query is never a target in a preference round | major | note 2 for the first half, with a count from the committed round records (below); the second half is for the owner, section 7 |
| 3 | "We take beta and lambda from CodeLutra" conflicts with the token average of the NLL term | major, quick | note 1; the brief states the consequence |
| 4 | "Two further cases are fixed by the data" cannot be reimplemented and was read in two ways | minor | note 3 |
| 5 | The draw: independence of the two draws, duplicate pairs; M = 2 by cost alone | minor | note 3; the brief states the draw; M stays a matter of cost |
| 6 | "everything derived from them remains at the client" is stronger than true; the weight by pairs is argued by analogy only | minor | note 4; the brief is corrected. The weights: Section 6 |
| 7 | "On-policy" rests on one resampling at four rounds | minor | not sent; a question Section 6 answers (B1, B2) |
| 8 | Fig. 1 writes L = L_DPO + L_NLL; whether truncated samples are executed; Algorithm 1 trains a client without pairs | remarks | note 3 for the truncated samples; the rest left |

The count behind note 2 (questions without a correct sample at the
first preference round, from the round records in
`fedicl-sql/audits/protocol_v2/`): BIRD 4,035 of 9,428 from the
pretrained model, 3,220 after one warm-up round, 2,698 after two;
Spider 1,074 of 8,659 from the pretrained model, 573 after two. The
questions that yield pairs rise on BIRD (4,857 to 5,877) and fall on
Spider (5,951 to 5,192, as more questions have only correct samples),
so the brief allows "fewer questions without a correct sample" and not
"more questions yield pairs".

## 6. Editor's notes, round 2 (the last)

1. The paragraph on CodeLutra: which difference is the claim of the
   paper; the value of lambda against the token average.
2. The reason for the warm-up rounds: the missing step.
3. The questions that yield no pair and the draw; whether a truncated
   sample is executed.
4. What stays at the client, named, in Section 3.1.
5. Two sentences on the reference model, the row of pointers to
   Section 6 at the end of 3.4, the upload said four times, the length
   of 3.4.

## 7. Revision 2, as it goes to the owner

| Check | Result |
|---|---|
| Build | no undefined reference or citation, no overfull box; no number prints as `??` |
| Lint | 0 stops; the notes are the abbreviations that Sections 1 and 2 give and one "may" |
| Length | 1,485 words (1,490 at most): 3.1 275, 3.2 153, 3.3 163, 3.4 761, 3.5 133 |
| Pages | about 4.3 |
| Facts | each changed sentence agrees with the brief and the code |
| Argument | 22 paragraphs, no paragraph with two points |
| Text taken from the brief | 29% of the words in runs of five or more |

What revision 2 did with the notes: the paragraph on CodeLutra names
the contribution ("to bring this execution-based supervision into
federated training, where only a client can compute it"), calls the
rest settings, takes lambda out of what is followed and states that
the token average makes the NLL term weigh less than in CodeLutra;
the reason for the warm-up rounds has its step; the two kinds of
question for which no pair is ever constructed are named with their
reason; the two draws are independent and the rule of replacement is
left to Appendix B; Section 3.1 names what stays at the client; the
reference-model paragraph is rewritten and the pass of the reference
model is in Section 3.5; one pointer to Section 6 names the three
ablations.

Where the draft departs from the writer's outline: the contrast with
FedAvg SFT is in 3.2 and 3.3 has two paragraphs; 3.4 has ten
paragraphs in the order sampling, labeling, pairs, questions without
pairs, loss, reference model, NLL term, aggregation, on-policy pairs,
closest work (the outline had closest work before the on-policy pairs
and the upload last); 3.5 has two paragraphs.

Left as they are after the two rounds, for the owner's reading
(`REVIEW_NOTES.md`, part B): the upload of the number of pairs is in
Section 3.1 ("one integer, its aggregation weight") and in Algorithm 1
only; the empty sample is no longer mentioned (it is an incorrect
sample under the general rule); the note inside Fig. 1 reads "Only
LoRA adapters travel" and the caption no longer says what else is
sent.

## 8. For the owner

- A reviewer is likely to ask why the gold SQL query is not used as
  the correct side inside a preference round for the questions without
  a correct sample. The notes hold two reads on BIRD (gold as the
  correct side at one round: 39.24 against 41.85, p 0.007; an NLL row
  on the gold SQL of those questions: 42.37 against 43.02, p 0.43).
  Neither is a row of the paper. One sentence in Section 6 or 7 would
  answer the question; it needs the owner's yes and a row in
  `CLAIMS.md`.
- Section 3.3 now gives a count-based reason for the warm-up rounds
  (fewer questions without a correct sample), with no number. It is a
  new statement of the paper: it needs a row in `CLAIMS.md` and the
  two counts as macros in Section 6.
- Both readers asked what the method is beyond CodeLutra inside
  FedAvg. The section now says which difference the paper claims; the
  argument itself is carried by Sections 1 and 2 and Table 1.
- Section 3 sets on more than its four pages even after the
  revisions, because of its floats. Appendix B is the first thing the
  plan moves to the supplementary file.

## 9. Carried to later briefs

- Section 4 defines how the query is read from the output of the model
  and how execution results are compared; Section 3.4 points there for
  both.
- Appendix B holds the time limit, the configuration of the adapter,
  the settings of local training and, if Section 3.4 leaves it out,
  the rule of replacement of the draw.
- Section 6 reports the questions without a correct sample at the
  first preference round with and without warm-up rounds, and compares
  the weights of the average.
- Section 7 says what a client must be able to do (execute SQL queries
  on its own databases); Section 3.5 no longer does.
