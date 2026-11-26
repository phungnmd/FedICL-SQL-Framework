# Section 5, Results: checks and editor's notes

Draft: `sections/05_results.tex`. The writer's outline:
`briefs/05_results_outline.md`; the writer's notes:
`briefs/05_results_notes.md`. PDF: `make`, then `build/main.pdf`
(Section 5 on pages 9 to 14). Until Table 1 of Section 2 exists, the
tables print one number lower than in the brief.

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief, Sections 3 and 4, the generated numbers and
tables and the two figures, and no other file. One agent wrote the
outline and the draft.

## 1. Outline

The outline covered every statement of the brief and did not depart
from it or from `OUTLINE.md` in content. Two things differ in form: 5.1
reads Table 3 first (A1, A3, A5, A6) and then Fig. 2 (A4 before A2),
and 5.4 is headed "Analysis of the predictions and cost of a round
(RQ4)". Four points of the writer changed the brief:

| Point | What the brief said | Now |
|---|---|---|
| Equal compute (E2) | A2 and A4 answer "FedAvg SFT with the same compute": more SFT rounds do not reach it | The link to 5.1 is that FedAvg SFT does not improve after round 3. The comparison at more client time for FedAvg SFT is direct on Spider only (five FedAvg SFT rounds about 620 minutes against 560 for the four rounds of the method); on BIRD the four rounds of the method take 1,207 minutes, about seven FedAvg SFT rounds, and FedAvg SFT is run to round 4 |
| The 0.5B model (D1) | a conjecture on the smaller margin may be offered | no conjecture: no number in the paper supports it |
| Row without warm-up rounds, Table 6 | "its EX is level with the method" | "no difference in EX is significant after the correction; its TS is lower on all three sets" (on Spider-DK the variant is 3.55 points above the method, unadjusted p 0.032) |
| Table 6 | did not say which models its rows are | the models of the main Spider setup; the caption says so |

Two answers were mine: the paragraph on further FedAvg SFT rounds ends
on the comparison with the highest round of FedAvg SFT, and the
paragraph on the perturbed sets ends on the gain being kept. One clause
beyond the brief was allowed: the gain of the second preference round
(BIRD +2.54, significant; Spider +0.74, not significant) beside FedAvg
SFT after round 3.

## 2. Checks of the first draft

| Check | Result |
|---|---|
| Build | compiles in the class of the manuscript, 19 pages; no undefined reference or citation, no overfull box |
| Lint | 2 stops, the names of the two other models typed by hand; 0 after the macros below |
| Length | 1,533 words by `style_profile.py` (the writer counts 1,578); asked: about 1,620, 1,800 at most. By part: 5.1 562, 5.2 237, 5.3 269, 5.4 510. Section 5.2 grows by about 70 words when its rows are in |
| Pages | about 5.0 pages with five tables and two figures, against the 5.5 of the plan |
| Macros | 42 numbers print `??`: the coefficient of FedProx (Section 4) and 41 of this section, all on rows that wait. New macros: `\fact{model.qwen05}`, `\fact{model.dsc13}` (the names as Table 4 prints them) |
| Table 7 | Spider, preference round 2: the steps printed 19, 3 and 88 minutes and the total 109 (18.68 + 2.63 + 87.80 = 109.12). The generator now rounds the steps of a round so that they add up to its rounded total: 19, 2, 88, 109. No other cell changed |
| Terms | those of `TERMS.md`; "the model" and "execution error", "incorrect result" throughout |
| Ceilings | kept. Every sentence on a waiting number states the comparison and leaves direction and size to the macro |
| Facts | every committed number of the text read against `generated/numbers.md` and the tables: the gains and tests of 5.1, the levels (higher on all seven; largest on moderate, +9.70, and extra hard, +4.76), Table 6, the counts of 5.4, Table 7. One statement of the brief did not hold and the writer corrected it: on BIRD the labels do not take "most of the added time after training" in the second preference round (training 195 of 391 minutes); the draft says training on the pairs is the largest part in every preference round |
| Text taken from the brief | 13% of the words stand in runs of five or more words of the brief (Section 4: 39 to 41%, Section 3: 31%) |

Register against the experiment sections of the ten papers (a signal
for the editor, not sent to the writer): sentence length 28.9 words
against 21.4; a sentence here carries several macros and tests in
brackets.

Points of the writer kept for the owner, not for a note:

- Within the method on BIRD the execution errors rise from round 3 to
  round 4 (102 to 128) while the incorrect results fall (723 to 658).
  The text gives the second movement, Fig. 3 shows both.
- The 0.5B model on Spider test: execution errors 365 with FedAvg SFT
  and 268 with the method, a fall of about a quarter, not a half. The
  paper prints neither count.
- "By a smaller margin" (5.2) reads two gains; no test compares them.
- The writer proposes one example for C3: a question of BIRD dev with
  its gold SQL query and a correct prediction that reads other tables
  or columns.

## 3. Cold read

A helper on Opus that had seen neither the brief nor the notes read
Sections 3 and 4 as context and then Section 5 as a reviewer for JIIS
(pages 1 to 14 of the build). It recomputed every difference, ratio and
sum the tables allow and found the arithmetic right throughout. It
summarized the section correctly and called Fig. 2 the strongest
evidence.

| # | Where | What the reader found | Weight | What was done |
|---|---|---|---|---|
| 1 | 5.1 last paragraph, 5.4 cost | Equal client time is argued for Spider only; on BIRD the method costs about 1.75 times FedAvg SFT (1,207 against 692 minutes) and FedAvg SFT stops at round 4. BIRD is compared with the highest round of FedAvg SFT, Spider with its fifth, which is not its highest. The fifth round is not announced in Section 4.4. The method is not shown past round 4. How was T chosen | major | note 1 (the references and the fifth round); the rest is the owner's (`REVIEW_NOTES.md` A15, C10, C21) |
| 2 | 5.4, second group of correct predictions | On BIRD 55 of the 95 questions of net gain read other tables or columns, BIRD has no test suite, and Table 6 shows that preference rounds can raise EX without TS (the row without warm-up rounds). The text does not connect the two | major | note 5 (the link to 5.3 for Spider); BIRD is the owner's (C20) |
| 3 | 5.3 | "Holds" and "is thus kept" against a difference significant on one of four sets; the fall is shown for Spider-Syn only | major | note 2 |
| 4 | 5.3 last paragraph | The variant without warm-up rounds is not defined in Sections 3 or 4; the caption says "those of Table 3" for three of its rows; the EX of the variant on Spider-DK and Spider-Realistic is passed over | minor | note 3; the cells are in the table (C19) |
| 5 | 5.4 first paragraph | "The gain thus comes from queries that now execute" rests on net totals; the paired predictions would show it | minor | the outcomes of the paired predictions are now macros and do not support the sentence; note 4 |
| 6 | 5.4 second paragraph | Read twice: "written like" against the criterion of tables and columns; the clause on unparsed predictions; BIRD by round and Spider by final values | minor | note 5 |
| 7 | 5.4 last paragraph | The all-correct counts of Spider cannot be squared with Section 4.2 unless the questions on databases without rows count as all correct; the first half of the reason for the labeling time holds for Spider too; client time is a sum, a round's wall-clock is its slowest client | minor | the macros now leave those questions out; note 5; the wall-clock is the owner's (C23) |
| 8 | 5.1 levels | Direction only, no test by level; Spider easy differs by 1.27 | remark | none |

Repetition named by the reader: FedAvg SFT after round 3 in 5.1 and
5.4 (note 1); 73.9 MB in Section 3.5, in 5.4 and in Table 7; the main
rows printed in Tables 3, 4 and 5 (C24).

What the paired predictions show (FedAvg SFT against the method, both
after four rounds; `\fact{moved.*}`):

| With FedAvg SFT | BIRD dev: correct, execution error, incorrect result with the method | Spider test |
|---|---|---|
| correct | 595, 9, 49 | 1,529, 15, 60 |
| execution error | 75, 86, 107 | 67, 55, 51 |
| incorrect result | 78, 33, 502 | 83, 14, 273 |

The method corrects about as many incorrect results as execution
errors (BIRD 78 and 75, Spider 83 and 67). The incorrect results do not
become fewer because former execution errors join them (BIRD 107,
Spider 51). The sentence of the brief "the gain comes from queries that
now execute and are correct" was mine and went beyond `CLAIMS.md`, C2;
the brief now carries the counts.

Two numbers changed in the generator after the reading: the all-correct
counts leave out the questions on databases without rows (Spider 2,891
and 5,784 became 2,327 and 4,623; BIRD has no such database), and no
correct prediction of the rows quoted in 5.4 fails to parse, so the
rule for unparsed predictions is not needed in the text.

## 4. Editor's notes, round 1

Five notes, sent with the reader's reaction and the facts, not with
wording:

1. 5.1 compares with the highest round of FedAvg SFT on both sets; the
   fifth round on Spider is introduced where it appears and its
   comparison belongs to the client time of 5.4, where the sentence on
   round 3 only repeats 5.1.
2. 5.3: the opening and closing sentences say what the table shows,
   the same direction on four sets and a size close to that on Spider
   test, significant on one.
3. 5.3: the variant without warm-up rounds is defined (T_w = 0, four
   preference rounds from the pretrained model); the caption of Table 6
   names its rows.
4. 5.4: the first paragraph says what the paired predictions show.
5. 5.4: the paragraph on the two groups is made readable and points to
   the TS result of 5.3 for Spider; the all-correct counts and the
   reason for the labeling time in the last paragraph.

## 5. Revision 1 and the second cold read

Revision 1: compiles, 19 pages, lint 0 stops, 1,663 words by
`style_profile.py` (the writer counts 1,718); 5.4 has 615 words against
the 405 of the brief. Every number read again against
`generated/numbers.md`. The five notes were taken: 5.1 compares with
the highest round of FedAvg SFT on both sets and announces the fifth
round; 5.3 opens on direction and size; the variant without warm-up
rounds is defined in the text and in the caption of Table 6; 5.4 rests
on the paired predictions; the paragraph on the two groups reports both
sets alike.

A check of mine after the revision, from the committed predictions and
test-suite scores (`LAB_LOG.md`, 2026-11-26): on Spider dev the test
suite accepts 17 of the 48 EX-correct predictions of the method that
read other tables or columns, and 14 of 49 of FedAvg SFT; of those that
read the same it accepts 711 of 755 and 689 of 728. The pointer from
5.4 to the TS results of 5.3, which note 5 of round 1 asked for, is
therefore not evidence for that group. By paired questions the net gain
on BIRD dev is 60 in the first group and 35 in the second.

A second helper on Opus read the revision cold. All numbers agreed
again; its summary of the section was right.

| # | Where | What the reader found | Weight | What was done |
|---|---|---|---|---|
| 1 | 5.4, second paragraph | Over half of the BIRD gain rests on predictions checked on one database; the TS evidence is aggregate, on the benchmark where the share is small; the sentence on the execution label describes how a coincidental match is rewarded; the criterion is not defined; none of the counts is in a table | major | note 1; the claim itself is the owner's (`REVIEW_NOTES.md`, A17) |
| 2 | 5.1, 5.4 | Compute-matched on Spider only (1.1 times), not on BIRD (1.7 times). The preference rounds use a learning rate of 5e-5, the SFT rounds 2e-4, and FedAvg SFT falls after round 3: would SFT rounds at the lower rate recover part of the gap? SFT on the correct samples is in Section 6, not in Table 3 | major | the owner's (A15, C25) |
| 3 | 5.3 openings | Still firmer than one significant set of four | minor to major | note 3 |
| 4 | 5.3 last paragraph | The variant has the highest EX on Spider-DK; its lower TS bears on finding 1; the paragraph is out of place and says less than the table | minor | none; Section 6 reads the row (C19) |
| 5 | 5.4 first paragraph, Fig. 3 | The two preference rounds are treated as one step; Fig. 3a shows two | minor | note 2 |
| 6 | 5.4 last paragraph | Which benchmark the counts belong to; a seven-fold rise of all-correct questions on BIRD: does the sampling narrow, what happens at T > 4 | minor | note 4; the question is the owner's (C22) |
| 7 | 5.1 to 5.4 | Whether "significant" beside an unadjusted p means after the correction; the family of the text is not listed | minor | note 4; the list of tests is for the supplementary file (C16) |
| 8 | terms | "both models", bare "SFT", "among the highest" for a tie | remark | note 4 |

## 6. Editor's notes, round 2 (the last)

1. 5.4, second paragraph: the pointer to TS goes; "a large part of the
   gain" goes; the sentence on the execution label reads as a design
   argument; the criterion gets a clause. The paragraph carries the
   criterion, the counts and the statement that EX establishes
   correctness on the evaluation database only.
2. 5.4, first paragraph: the two preference rounds differ on BIRD and
   the text says what Fig. 3 shows.
3. 5.3: the openings give the answer the reader took: the same
   direction on every set and under both metrics, significant on
   Spider-Syn.
4. Places where the reader stumbled (significance beside an unadjusted
   p, "both models", bare "SFT", the tie, the counts of the last
   paragraph, "these gains").

## 7. Revision 2 and what is left for the owner

Revision 2: compiles, 19 pages, lint 0 stops, no overfull box, 1,676
words by `style_profile.py` (asked: about 1,620, 1,800 at most; about
70 more come with the rows of 5.2), about 5.4 pages, pages 9 to 14 of
the build (plan 5.5). 42
numbers print `??`, all on rows that wait. 16% of the words stand in
runs of five or more words of the brief. Every number of the text read
again against `generated/numbers.md`, Table 6 and Table 7.

The four notes were taken. 5.4 now has five paragraphs: the totals and
the two preference rounds by round (Fig. 3), the paired predictions,
the two groups of correct predictions, client time, and where the time
goes. The paragraph on the two groups carries the criterion, the four
pairs of counts and the statement that EX establishes correctness on
the evaluation database only; the writer added that the counts are
taken for each method separately, so that a reader does not subtract
them into "55 of 95".

The two rounds are used. Left for the owner's reading:

| Where | Point |
|---|---|
| 5.4, third paragraph | claim C3 in its reduced form; what the paper does with it is `REVIEW_NOTES.md`, A17 |
| 5.4, second paragraph | the outcomes of the paired predictions are numbers beyond `CLAIMS.md` (A16) |
| 5.4, first paragraph | on BIRD dev the execution errors rise in the second preference round (102 to 128) and the text does not say why. The paired predictions of rounds 3 and 4 exist (of the 723 incorrect results after round 3, 56 become correct and 54 become execution errors) and have no macro |
| 5.1, last paragraph | the fifth round of FedAvg SFT on Spider is announced here; Section 4.4 could carry it at its last pass |
| 5.4, cost | no comparison at equal client time on BIRD (A15) |
| 5.1 third paragraph, 5.2 second and third | sentences on rows that wait: read again when the rows are in; each then needs its finding |
| Tables 4 and 5 | they print the main rows again (C24) |
