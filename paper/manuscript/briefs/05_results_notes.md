# Notes to the editor: Section 5, Results (revision 3)

File revised: `sections/05_results.tex`. The paper compiles with it
(built in a copy in my scratch folder): no undefined reference or
citation, no overfull box. 42 numbers print `??`, as before, all on
rows that wait.

## What changed, by your note

1. **5.4, the predictions that read other tables or columns.** The
   paragraph is cut to what you listed. It opens on the finding (not all
   of the additional correct predictions read the tables and columns of
   the gold SQL query), gives the criterion in one sentence (the set of
   tables and the set of columns that the parsed query reads, subqueries
   included, each column assigned to its table by the schema, compared
   with those of the gold SQL query), then the four pairs of counts
   after four rounds, and ends on the statement that EX establishes the
   correctness of such a prediction on the evaluation database only.
   Gone: the pointer to the TS results, "a large part of the gain", the
   sentence on the execution label, and the counts by round. One
   sentence is new: the counts are taken for each method separately, and
   a question that both answer correctly may be counted in different
   groups for the two. Without it a reader subtracts the printed counts
   and takes 55 of the 95 gained questions to be in the second group,
   which the paired count (35) does not support.
2. **5.4, the two preference rounds.** The paragraph on the incorrect
   predictions now follows Fig. 3: the totals after four rounds, then
   BIRD dev by round (the first preference round takes the execution
   errors from 286 to 102 while the incorrect results rise from 593 to
   723; in the second the incorrect results fall to 658 and the
   execution errors rise to 128), then Spider test by round (execution
   errors 183, 99, 84; incorrect results 373, 385, 384). The paired
   predictions after four rounds are a paragraph of their own. Its last
   sentence is bound to what the paired counts cover: the former
   execution errors that return an incorrect result are why the
   incorrect results are not fewer after four rounds.
3. **5.3, the two openings.** The first paragraph opens: `\method` is
   above FedAvg SFT on Spider dev and on each of the three perturbed
   sets, and the difference is significant on Spider-Syn. The second:
   under TS the difference has the same direction on the three sets
   with test suites and is again significant on Spider-Syn only.
4. **Places where the reader stumbled.**
   - Significance: 5.1 now says that throughout the section a
     difference is called significant or not significant after the
     correction and that the $p$-values quoted are unadjusted.
   - "Both models", "the two models" in 5.3 are now "both methods",
     "the two methods"; the paired predictions in 5.4 are those "of
     FedAvg SFT and `\method`". The caption of Table 6 speaks of rows.
     "Models" is left for the three models of 5.2, and the caption of
     Table 4 is reworded so that "three models" cannot be read as the
     three columns.
   - "A third round of FedAvg SFT"; "further rounds of SFT" went with
     the cut of note 1.
   - The end of 5.1: "On Spider test, the highest EX of FedAvg SFT is
     that of rounds 3 and 4, and the gain over it is the 3.49 points of
     Table 3."
   - Last paragraph of 5.4: each pair of counts of questions with only
     correct samples is followed by its benchmark.
   - "`\method` requires no communication beyond that of FedAvg SFT; its
     additional cost is computation at the clients."
   - 5.3: the sentence with "not confined to ... alone" is replaced by a
     plain reading of Table 6: the differences under TS are close to
     those in EX, as the stricter metric lowers both methods by a
     similar amount.

## Length

1,719 words by my count, against 1,718 for revision 2; my counts ran
about 45 above yours on the first draft.

| Part | Brief | Revision 2 | Revision 3 | Paragraphs |
| --- | --- | --- | --- | --- |
| 5.1 RQ1 | 495 | 585 | 598 | 131, 48, 169, 95, 155 |
| 5.2 RQ2 | 405 | 237 | 237 | 70, 57, 110 |
| 5.3 RQ3 | 315 | 281 | 258 | 111, 82, 65 |
| 5.4 RQ4 | 405 | 615 | 626 | 134, 107, 148, 132, 105 |

Note 1 freed about 55 words and note 2 took about 60; 5.3 lost 23 and
5.1 gained 13 with the sentence on significance. If room is needed for
the waiting sentences of 5.2, I would cut first the clause on the second
preference round in the last paragraph of 5.1 (about 30 words; its
content is now also in the by-round sentences of 5.4 as counts), then
the sentence on labeling time at the end of 5.4 (about 30 words).

## Left out against the brief

- C3: the counts by round (FedAvg SFT at rounds 2, 3 and 4, `\method`
  at round 3), the count of the pretrained model on Spider, and "a
  large part of the gain on BIRD", which your paired count withdraws.
- D4: the EX values of the fall from Spider dev to Spider-Syn; Table 6
  prints them, and the sentence now covers all three perturbed sets.
- E2: the numbers of pairs in the two preference rounds; Table 7 prints
  them.

## Doubts

1. 5.4, paragraph 1, BIRD dev by round. The sentences give totals and
   draw nothing from them. That the second preference round gains by
   correcting incorrect results would need the paired predictions of
   rounds 3 and 4, which have no macro; the totals (incorrect results
   down by 65, execution errors up by 26, 39 more correct) only suggest
   it. A reader may still ask why the execution errors rise in that
   round, and the section does not say.
2. 5.4, paragraph 2, "which is why the incorrect results are not fewer
   after four rounds". Checked on the nine paired counts as before:
   without the former execution errors the incorrect results of
   `\method` would be 551 on BIRD dev and 333 on Spider test.
3. 5.4, paragraph 3. With the TS pointer gone, the paragraph ends on a
   limit of the evidence and offers nothing against it. Your count on
   Spider dev (17 of 48 and 14 of 49 accepted by the test suite, against
   711 of 755 and 689 of 728) says such predictions are mostly not
   correct beyond the evaluation database, for either method. I have
   kept it out of the text as you asked. It bears on the discussion: on
   BIRD dev these predictions are 191 of the 748 correct predictions of
   `\method` and 136 of the 653 of FedAvg SFT, and BIRD has no test
   suite.
4. 5.3, paragraph 1, "against +3.49 on Spider test" stands beside the
   four differences without a statement that they are close; the reader
   compares. The last sentence (on no perturbed set is the difference
   smaller than on Spider dev) rests on 3.87, 2.75 and 3.92 against
   2.51, with no test.
5. Paragraph 3 of 5.1 and paragraphs 2 and 3 of 5.2 are still lists of
   waiting comparisons; they read as such until the rows are in.

## Proposal

The example for the predictions that read other tables or columns has
become more useful and less safe at once: after your count it should be
chosen and worded so that it does not suggest such predictions are
equivalent to the gold SQL query. If the discussion takes up this
group, the example belongs there.

## Revision after the owner's decision (2026-11-27)

One change, in the first paragraph of 5.4; nothing else in Section 5 is
touched.

- After the counts of execution errors after four rounds (BIRD dev and
  Spider test), a new sentence reports the test of C1: both differences
  are significant under the test of Section 4.6 applied to whether the
  prediction of a question ends in an execution error, with
  `\errpval{bird}{fedavg}{4}{k2}{4}` and
  `\errpval{spider}{fedavg}{4}{k2}{4}`.
- The counts of incorrect results now stand in a sentence of their own,
  each with its set, followed by the test of C2: under the same test
  neither difference is significant, with
  `\wrpval{bird}{fedavg}{4}{k2}{4}` and
  `\wrpval{spider}{fedavg}{4}{k2}{4}`.
- For the incorrect results on BIRD dev I also print the adjusted value,
  `\wrpadj{bird}{fedavg}{4}{k2}{4}` (0.077). The unadjusted value is
  0.007, and a reader who meets "not significant" beside it would stop,
  although 5.1 says that significance is stated after the correction.
  The macro is in `generated/numbers.md`; the brief does not name it.
- The wording follows the passage of Section 6 on the row without the
  preference term ("under the test of Section 4.6 applied to ...",
  "under the same test"), so that the two passages read alike.

The opening sentence of the paragraph stands as it was: the execution
errors are reduced by about half, and the incorrect results do not
become fewer.

Checks. The text family now has 23 tests. I read the adjusted values
of every comparison that Section 5 calls significant or not significant
in the text again, and each statement still holds. The paper compiles
with the revision: no undefined reference or citation, no overfull box,
and none of the four new macros prints `??`. `make` stops at its last
step because the paper now has 29 pages against the limit of 25; that
comes from the whole paper, not from this change.

Length: 1,788 words by my count (5.4: 680), 54 more than before this
change and 15 more from an edit in 5.3 that is not mine. My counts ran
about 45 above yours on the first draft, so this is near the limit of
1,800 before the waiting sentences of 5.2. The cuts I would make first
are those listed under "Length" above.
