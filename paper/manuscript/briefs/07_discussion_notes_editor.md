# Sections 7 and 8, Discussion and limitations, Conclusion: checks and editor's notes

Drafts: `sections/07_discussion.tex`, `sections/08_conclusion.tex`.
The writer's outline: `briefs/07_discussion_outline.md`; the writer's
notes: `briefs/07_discussion_notes.md`.

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief, Sections 2 to 6 and `main.tex`, and no other
file of the notes. One agent wrote the outline and the draft.

## 1. Outline

Section 7 in two subsections (7.1 Interpretation of the results, four
paragraphs; 7.2 Scope and limitations, three), 700 words planned;
Section 8 in two paragraphs, 180 words. The outline serves the four
statements, the eight limitations and the three statements of Section
8, and does not depart from the brief or from `OUTLINE.md` in content.
What differs in form: Section 7.1 opens on statement 3 (the outcome
against FedAvg SFT, where Section 5.4 hands over), then 1, 2, 4.

What the writer found against the numbers, and my answers:

| Point | Brief | Answer |
|---|---|---|
| Limitation 4 | "a preference round takes more client compute than an SFT round" | `\fact{cost.spider.pref2.ratio}` prints 0.9; the limitation is that the additional cost is computation at the clients. Brief corrected |
| Limitation 8 | the smaller gain "where FedAvg SFT is still improving fast, as with the model of 0.5B parameters" | the paper has no row by round for that model; the two facts without the cause. Brief corrected |
| Statement 1 | the pairs by kind and the counts by round | I added the counts of the row "Fixed pairs and reference" (BIRD dev 91 and 735, Spider test 97 and 375) as further evidence, with the instruction not to pass over Spider. Withdrawn after cold read 1 (section 3 below) |
| Second seed | "when it is in" | not in; the sentence has to hold with the rows empty |

## 2. First draft: checks

- Length: Section 7 prints 776 words (722 by the style tool), limit
  780; Section 8 prints 183, limit 200.
- Build and lint: no stop; every macro prints a value.
- Against the brief: the four statements and the eight limitations are
  there. Cut by the writer for length: the tested comparison of the
  variant without warm-up rounds against the method; the naming of the
  correct predictions that read other tables or columns; the 107
  former execution errors.
- Section 8 against the Introduction: the two descriptions of the
  method agree in their terms; Section 8 leaves out the NLL term.
- Style signals (for the editor only): mean sentence 28.9 words
  against 23.6 in the reference discussions.

## 3. Cold read 1

`cold_reviews/2026-11-27_0526_sections7and8_1.md`: a reader with pages
1 to 20 as context and pages 21 and 22 to review.

| # | Finding | Weight | What I make of it |
|---|---|---|---|
| 1 | The counts of Section 5.4 by tables and columns are not discussed: on BIRD dev the correct predictions that read the gold tables and columns go from 517 to 557, those that read others from 136 to 191, so more than half of the net gain of 95 questions is where EX holds on one database only; BIRD has no test suite. Section 7.1 asks this of the variant without warm-up rounds and not of the BIRD gain | major | True against `generated/numbers.md`. Limitation 5 now carries it. Note 2. For the owner: this is the sharpest question on the headline number |
| 2 | Paragraph 2 of 7.1 is not supported. In counts, the pairs with an incorrect result are 5,138 and 5,278 in the two rounds on BIRD, while the incorrect results rise by 130 and then fall by 65; what changes is the pairs with an execution error. The fixed row on Spider goes against the account (97 against 84), and the row keeps pairs, a second pass and the older reference together | major | True. Statement 1 was mine (approved in the brief) and the fixed row was my addition. Statement 1 narrowed to what holds on both datasets; the fixed row leaves. Note 1 |
| 3 | The reading of the warm-up rounds is weaker than written: TS is significant on Spider-Syn only; the variant has four preference rounds, not two; the gold-SQL variant of Section 6 is not used | major | True. Statement 4 of the brief now says what each half rests on and asks for the other reading. Note 3 |
| 4 | Numbers appear first in the Discussion (pairs by kind; the split of the fixed row) | minor | The fixed row leaves. The pairs by kind stay inline; the writer's proposal of two columns in Table 7 is recorded for the owner |
| 5 | Paragraph 3 restates Section 6, and gives the rationale of Section 3.4 as if it explained the Spider result | minor | Note 4 |
| 6 | Paragraph 1 answers "Section 7 returns to them" with the totals and a truism; "no fewer" hides that the incorrect results are more; "because" names one flow | minor | Note 4 |
| 7 | Limits left out: heterogeneity by query complexity only, within one benchmark; the pair count changes by round with the model's performance on a client's data, unlike $n_k$; the cost over the whole training is not stated | minor | The first two into limitations 2 and 3 (note 5). The total (BIRD 1,207 against 692 minutes) is in no macro; for the owner |
| 8 | "$T_w = 2$ for every model, and the gain is smaller with the 0.5B model" implies a cause | minor | Note 5; limitation 8 corrected again |
| 9 | Section 8 leaves out the NLL term; the Spider gain has no number | remark | The first in note 5; the second is the brief (one number) |
| 10 | "(values without a test)", "a comparison of values" have to be decoded | remark | They are the words of Section 6 |

## 4. Editor's notes, round 1

1. Section 7.1, paragraph 2: the reading does not hold. Statement 1
   narrowed to the first preference round on both datasets and the
   counts of both kinds of pair; the fixed row leaves.
2. Section 7.2, the label and the metric: the size of the limit in the
   counts of Section 5.4, and that the BIRD result is the one without
   a stricter check.
3. Section 7.1, paragraph 4: what is tested and what is a comparison
   of values; the other reading (four preference rounds against two);
   the gold-SQL variant.
4. Section 7.1, paragraphs 1 and 3: restatement. What Sections 5.4 and
   6 support together: the established effect is on whether a query
   executes; the incorrect results are where it is not established.
5. Section 7.2 and Section 8: the two facts of limitation 8 apart; the
   heterogeneity and the pair count; the NLL term in Section 8.

The upper ends of 780 and 200 words stay.

## 5. Revision 1: checks

- Section 7 was written again from the narrowed brief: 777 words in
  print (721 by the style tool), limit 780. Section 8: 190 words.
- Section 7.1 now makes one argument in two paragraphs (the results
  establish an effect on execution errors and not on incorrect
  results; the gain in EX comes from both kinds and is not established
  for the preference term over the NLL term alone), then the pairs by
  kind as counts, then the warm-up rounds with what is tested, a
  reading and the other reading the rows admit.
- Section 7.2 gives the BIRD dev counts of Section 5.4 (517 to 557 and
  136 to 191) and says that EX is the only check for the second group.
- The row "Fixed pairs and reference" is out of the section; the
  section cites `zhong2020testsuite` only.
- Lint: no stop. Build (scratch directory): no undefined reference.
- A check of mine on "the results establish an effect": the paper has
  no test of the execution errors of the method against FedAvg SFT
  after four rounds. From the paired counts (`moved.*`), the exact
  McNemar test gives p = 5.8e-22 on BIRD dev (182 questions fail only
  with FedAvg SFT, 42 only with the method) and 6.2e-14 on Spider test
  (118 and 29). On the incorrect results: p = 0.0070 on BIRD dev (156
  only with the method, 111 only with FedAvg SFT) and 0.37 on Spider
  test (111 and 97). Not in the generator and not in the paper; for
  the owner with A25.

## 6. Cold read 2

`cold_reviews/2026-11-27_0538_sections7and8r1_1.md`. The reader
checked every number of the two sections against Sections 5 and 6 and
found the arithmetic consistent.

| # | Finding | Weight | What I make of it |
|---|---|---|---|
| 1 | 55 of the net gain of 95 on BIRD dev is in predictions that only EX checks; no consequence is drawn, the reading of 7.1 is not applied to the method on BIRD, and Section 8 gives the 6.19 points unqualified | major | Note 3. For the owner: the sharpest question on the headline number, raised by both readers |
| 2 | The row with the NLL term alone undercuts the case for pairs with DPO: its EX is above a third round of FedAvg SFT and the preference term's own EX gain is not significant; the Conclusion reads as if both terms were shown to be needed | major | C29 of `REVIEW_NOTES.md`; the rows of that variant after four rounds are queued. Section 7.1 now says it plainly. Nothing asked of the writer |
| 3 | "No such effect is established for the incorrect results" against a significant increase on BIRD dev; "an effect of the method" rests on the test of the preference term in one round | minor | Note 1 |
| 4 | Fewer execution errors is presented as a gain in itself; 107 of 268 become incorrect results, which fail silently | minor | Note 1 |
| 5 | The second round is told in part: the execution errors rise (102 to 128), and the fall of the incorrect results (723 to 658) is left out | minor | Note 2. The first reader faulted the paragraph for deriving that fall from the pairs; the second for leaving it out. Both hold: the facts are stated whole and nothing is derived |
| 6 | Warm-up paragraph: the variant never has a gold SQL query as a training target; the reason of Section 3.3 is not revisited; Spider only | minor | Note 4 |
| 7 | Missing limits: two preference rounds; how the settings were chosen; the execution of generated queries on private databases | minor | Note 5 for the first and third. How a setting was chosen is not told in the paper |
| 8 | "Skewed by query complexity only" against Section 4.2; "more clients" against the ten-client setup | remark | My round-1 note was inexact. Note 5; brief corrected |
| 9 | The sentence on the weights implies a remedy; tested after one preference round | remark | Note 5 |
| 10 | Conclusion: the second direction conflicts with the labelling rule; the Spider gain has no number | remark | Note 5 for the first; the second is the brief |

## 7. Editor's notes, round 2 (the last)

1. Section 7.1, paragraph 1: the wording against what is tested; the
   shift from execution errors to incorrect results.
2. Section 7.1, paragraphs 2 and 3: the second round whole; what the
   evidence covers (the preference term is isolated in the first
   preference round).
3. Section 7.2 with Section 8: what is known and not known about the
   group that reads other tables or columns, for the BIRD result.
4. Section 7.1, paragraph 4: the gold SQL query never a target in the
   variant; the reason of Section 3.3; Spider only.
5. Section 7.2 and Section 8: the setups as Section 4.2 has them; the
   weights; two preference rounds; the execution of generated queries
   (read-only, time limit); the second direction.

## 8. Revision 2: checks, and what stays open

Checks:

- Length: Section 7 prints 778 words (733 by the style tool), limit
  780; Section 8 prints 197 (191), limit 200.
- Build and lint: no stop for either file; no undefined reference;
  every macro of the two sections prints a value. Section 7 is on
  pages 21 and 22 of the build, Section 8 on page 22.
- Every statement read against `generated/numbers.md`: the counts of
  the two kinds of incorrect prediction, the shift of 107 of the 268
  execution errors, the 78 and 75 questions, the pairs by kind in both
  rounds, the counts by round, the two groups of correct predictions
  (BIRD dev 136 to 191 and 517 to 557; on Spider test the group that
  reads the same tables and columns has the larger rise, 1,521 to
  1,576 against 83 to 103).
- "Read-only" checked in the code: every database is opened with
  `mode=ro` and `PRAGMA query_only=ON` (`fedls_sql/eval/sql_exec.py`,
  used by the sampling and the labelling of a preference round).
- The five notes of round 2 were all taken up (the writer's account is
  in `07_discussion_notes.md`, "Revision 2").

What stays open after the two rounds (each is in `REVIEW_NOTES.md`):

1. Section 7.2, paragraph 1: "more than two preference rounds are not
   studied" does not agree with Section 7.1, paragraph 4, where the
   variant without warm-up rounds runs four. The clause comes from row
   2 of the limitations in my brief ("Two preference rounds are all
   that is studied"). What holds: the method is not trained beyond
   four rounds, and the only line with more than two preference rounds
   is that variant. Brief corrected; the sentence waits for the pass
   over the whole paper (B33).
2. Left out of Section 7.2 for the limit of 780 words: the cost as a
   limitation (Section 8 keeps one clause; Sections 1 and 5.4 have the
   numbers), the second seed on BIRD, that a client's number of pairs
   depends on the model's performance on its data, and that a question
   on a database without rows yields no pair (B34).
3. The halving of the execution errors against FedAvg SFT is "a
   difference of counts": the paper has no test of it. The values of
   my check are in section 5 above (A31).
4. The abstract gives the halving without the clause that the
   Introduction and the Conclusion now carry (B35).
5. Of the net gain of 95 questions on BIRD dev, 55 are correct
   predictions that read other tables or columns than the gold SQL
   query, and BIRD has no test suite. Both readers raised it as the
   main question on the headline number. The section states it and
   draws no share from it (C43).
6. Section 7.1, paragraph 2, on the round with the NLL term alone, is
   C29 in the paper's words; it is to be read again when the rows of
   that variant after four rounds arrive (B36).
7. The writer's proposals: two columns in Table 7 for the pairs by the
   kind of their incorrect sample, which would save about 25 words in
   Section 7.1 (C44).

## 9. Revision 3 (owner's decisions, 2026-11-27)

The owner answered the open points on 2026-11-27. Three of them
changed Section 7; the brief carries them and the same writer was
continued. Section 8 is unchanged.

| Decision | Brief | Section 7 now |
|---|---|---|
| The halving of the execution errors against FedAvg SFT is tested (A31) | statement 3 with the four tests; the generator runs them (`ERR_TESTS`) | 7.1, paragraph 1: against FedAvg SFT after four rounds about half the execution errors, significant on both sets; the larger counts of incorrect results are not a significant difference (BIRD dev p = 0.007, 0.077 after Holm; Spider test 0.37). Then the test of the preference term in one round, as before. No p-value is printed here; Section 5.4 prints them |
| The draft is complete first and trimmed later (B34) | length about 860 words, 900 at most; rows 3, 4 and 5 of the limitations in full | 7.2 has four paragraphs: the number of pairs depends on the model's performance on a client's data, with the result of Section 6 for question counts as weights; a question on a database without rows yields no pair; the cost as a limitation, 0.9 to 2.7 times the client time of a FedAvg SFT round, communication unchanged |
| The clause on two preference rounds (B33) | row 2 corrected | "has 2 preference rounds among its T = 4 rounds and is not trained further; only the variant without warm-up rounds has more" |

Checks: Section 7 prints 894 words (833 by the style tool); lint
without a stop; the build has no undefined reference, 29 pages. Read
against `generated/numbers.md`: the four statements of paragraph 1
agree with the tests (execution errors 5.8e-22 and 6.2e-14; incorrect
results 0.077 and 0.75 after Holm; the preference term in one round
1.1e-24 and 4.2e-6 on the execution errors, 1.0e-12 on the incorrect
results of BIRD dev). The inventory of the section gained four
macros (the two cost ratios, the two round settings) and lost none.

Still out of Section 7: the second seed on BIRD (its rows of Table 3
are empty) and the time limits as values. The writer's candidates for
the later trim: the Spider pair counts of the second preference round,
the sentence on the weights, the cost range (Section 5.4 prints it).
No cold read was run on this revision; the reader test of the whole
paper covers it.
