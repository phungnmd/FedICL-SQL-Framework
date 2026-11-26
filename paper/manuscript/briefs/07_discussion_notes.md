# Notes to the editor: Sections 7 and 8

Drafts: `sections/07_discussion.tex`, `sections/08_conclusion.tex`.
Outline: `briefs/07_discussion_outline.md`, with your answer of
2026-11-27.

## State

- Section 7 prints 776 words (running text of the PDF, headings left
  out, citation marks and references counted); the limit is 780. The
  sentences on the row "Fixed pairs and reference" that your answer
  added take about 65 of them, which is why the section sits at the
  upper end and not near 700.
- Section 8 prints 183 words.
- Both files pass `make lint`, every macro in them prints a value
  today, and the build has no undefined reference. The build still
  stops on the page count (29 pages against 25), and the four lint
  stops that remain are in `01_intro.tex`.
- I ran `make pdf` and `make lint` to check the two files; they write
  to `build/`, which Git ignores. Nothing was committed.

## Departures from the outline

1. Paragraph 1 (S3). The opening sentence now states the totals and
   nothing else (half the execution errors, no fewer incorrect
   results), and the second says that the method "nevertheless
   corrects both kinds of incorrect prediction", with the two counts.
   No sentence calls the gain a gain in queries that execute. The
   count of former execution errors that now return an incorrect
   result (107) is left to Section 5.4, so that two counts are
   repeated, as the ceiling asks. The reading is the last clause
   alone; the sentence I had planned on "what made the query fail and
   what made it incorrect" went for length.
2. Paragraph 2 (S1). The tie to the on-policy pairs moved into the
   opening sentence ("which each round constructs anew"), and the
   closing sentence of the outline is gone. The sentence "most pairs
   now set a correct sample against one with an incorrect result" is
   gone too: the 25% carries it, and "three quarters" would have been
   a number typed in words. The fall of the execution errors in the
   first round is referred to Fig. 3 without its two values. The rise
   of the execution errors on BIRD dev in the second round is said
   with both values. The fixed row is given by its counts on both
   sets, marked as values without a test, with "the pairs and the
   reference model of the first round kept".
3. Paragraph 3 (S2) prints no number; the outline planned four. It
   refers to Section 6 and Table 8.
4. Paragraph 4 (S4) prints no count of questions without a correct
   sample; it refers to Section 6. The tested comparison of the
   variant with `\method` (significant on Spider-Syn only) is also
   left to Section 6: the paragraph speaks only of the variant against
   FedAvg SFT and calls it a comparison of values. Say if the tested
   one has to stand here as well (about 13 words, which the section
   does not have).
5. Paragraph 6 (L5). The reference to Section 5.4 stayed, but without
   naming the correct predictions that read other tables or columns;
   the sentence is "EX has the same limit on the evaluation database
   (Section 5.4)". That was a cut for length.
6. Paragraph 7. The cost is given as a range, "between 0.9 and 2.7
   times the client time of a FedAvg SFT round", after the sentence
   that the additional cost is computation at the clients.

## What the brief lacked

1. A macro for the sizes of the models. The lint stops on "0.5B" and
   "1.5B" typed by hand. Paragraph 7 therefore says "models of at most
   `\setting{model.size}` parameters" [1.5 billion] and names the
   small model as `\fact{model.qwen05}` [Qwen2.5-Coder-0.5B]. The
   lower end of the range of L7 (0.5B) is not printed as a size. A
   macro for the range would let the sentence follow the brief.
2. Citation keys. I used the three of the outline, each for what an
   earlier section cites it for.

## Doubts

1. Paragraph 1, "because". "The incorrect results do not decrease
   because part of the former execution errors now execute and return
   an incorrect result" follows Section 5.4 ("which is why"). It is
   bookkeeping of the paired counts, not a tested cause, and it is
   stated without a hedge, as in Section 5.4.
2. Paragraph 3, last clause. "The preference term constrains the two
   samples of a pair only relative to each other (Section 3.4)" stands
   after a semicolon, beside the result that the term alone brings no
   gain on Spider test. It is a fact of the loss placed next to the
   result, not marked as a reading. With "a possible reason is that"
   it costs five more words.
3. Paragraph 3, the cited report. I wrote "likewise report a lower
   accuracy without the NLL term"; Section 6 has "with the DPO term
   alone than with both terms". Same content, shorter. The sentence
   repeats Section 6; if words are needed, it is the first candidate
   to go (13 words).
4. Paragraph 4, the reading. "One reading is that training first on
   the gold SQL query of every question limits what the model takes
   from such labels." "What the model takes from such labels" is loose
   on purpose: the paper has no analysis of which queries the variant
   without warm-up rounds learned. The sentence before it (a label
   accepts a query that is not equivalent to the gold SQL query, and
   TS can reject it) is stated as fact, since it follows from the
   definitions of Sections 3.4 and 4.1.
5. Paragraph 4, "level". "EX on Spider test is level with and without
   the warm-up rounds" uses the word of Section 6 for 78.02 and 78.20.
   The BIRD rows of these variants wait, and the sentence is bounded
   to Spider test.
6. Paragraph 7, the range of the cost. The sentence takes
   `\fact{cost.spider.pref2.ratio}` as the lower end and
   `\fact{cost.bird.pref1.ratio}` as the upper. If the cost numbers
   are regenerated, the order has to be checked again.
7. Paragraph 7, the second seed. "The two main rows on BIRD have a
   second seed (Table 3)" holds while the rows are empty, as Section
   4.5 already says they are trained again.
8. Section 8. "Labels them by execution on its own databases against
   the gold SQL query" compresses the definition of the execution
   label; the Introduction will state it in full. No number of clients
   is given in the Conclusion.

## Proposals

1. The pairs by the kind of their incorrect sample (paragraph 2) are
   four counts and four percentages printed inline, new in this
   section. Two columns in Table 7, which already lists the pairs of
   each preference round ("incorrect side: execution error", "incorrect
   result"), would hold them; paragraph 2 could then refer to the
   table and lose about 25 words.
2. The counts by kind of the row "Fixed pairs and reference" are in
   no float: Table 8 has its EX and Fig. 3 does not show the row. If
   paragraph 2 keeps resting on them, one more group of bars in Fig. 3
   (the fixed row at round 4) would show them.

## Revision 1

After the editor's notes of round 1 and the corrected brief
(statements 1 and 4, limitations 2, 3, 5 and 8, statement 1 of Section
8). Section 7 is rewritten, not patched: Section 7.1 has a new
argument and a new order. It prints 777 words; Section 8 prints 190.
Both files pass `make lint` and every macro prints a value. The notes
above this heading describe the first draft and no longer hold where
this section says otherwise.

What each note led to:

1. Note 1 (the pairs). The paragraph is now the third of Section 7.1
   and makes the narrower statement only. It gives the pairs of both
   kinds as counts, for both rounds and both datasets (eight counts),
   says that the first preference round lowers the execution errors on
   both evaluation sets, and that the second no longer does on BIRD
   dev while on Spider test they fall further. No sentence derives the
   fall of the incorrect results on BIRD dev from the pairs, and that
   fall is no longer mentioned here. The row "Fixed pairs and
   reference" is out of the section. The percentages and the totals of
   the pairs are out as well; with both kinds printed, the reader has
   the shares. "Agree with this account in the first preference round"
   is the only interpretive wording, and it is bounded to that round.
2. Note 2 (the label, the metric, the BIRD result). The paragraph says
   what the limit of EX is ("EX makes the same comparison on one
   evaluation database") and gives the four counts of BIRD dev (517 to
   557 for the correct predictions that read the tables and columns of
   the gold SQL query, 136 to 191 for the others), then: "for the
   latter, EX is the only check, as BIRD has no test suite". The
   sentence does not say "more than half of the gain": the counts are
   taken for each method separately (Section 5.4), and the two rises
   stand side by side. The Spider counts (1,521 to 1,576, 83 to 103)
   are left to Section 5.4 for length; the paragraph says only that TS
   on Spider dev and two perturbed sets is a stricter check for
   Spider. If the Spider counts should stand here, they cost about 14
   words.
3. Note 3 (the warm-up rounds). The paragraph opens on "The evidence
   on the warm-up rounds is narrower" and gives each half with what it
   rests on: EX on Spider test level; the tested difference in TS
   against `\method`, significant on Spider-Syn only; the comparison
   with FedAvg SFT marked as a comparison of values. The reading is
   reworded (training on execution labels from the first round favors
   queries that return the gold result on one database without being
   equivalent to the gold SQL query) and is followed at once by what
   else the same rows admit: four preference rounds in the variant
   against two. "Their effect appears under TS" is gone. Two things
   the note names are not in the paragraph, for length: the number
   behind the tested difference (`\tsgap{syn}{k0}{4}{k2}{4}`, printed
   in Section 6) and the result on the gold SQL query as the correct
   side of a pair. The second bears less on the reading as it is now
   worded, since the reading no longer speaks of training first on the
   gold SQL query; a clause on it costs about 18 words. The counts of
   questions without a correct sample are also left to Section 6.
4. Note 4 (what the reader did not have). Paragraphs 1 and 3 of the
   first draft are replaced by one argument in two paragraphs.
   Paragraph 1 states it: of the two kinds of incorrect prediction,
   the results establish an effect on one. It rests on the halved
   execution errors and on the tested effect of the preference term,
   and it gives the incorrect results as values (658 against 613, 384
   against 370) with the tested result that the preference term leaves
   more of them on BIRD dev. Paragraph 2 says what follows for the
   gain: it comes from both kinds (78 and 75) while 107 former
   execution errors now return an incorrect result, stated as three
   counts and without "because"; and it does not rest on the
   preference term alone (the round with the NLL term alone, values of
   Table 8; no established difference in EX). It closes on "What the
   preference term adds through the incorrect samples is thus
   established for the execution errors only". The truism on executing
   is gone, and so are the rationale of Section 3.4 and the sentence
   on CodeLutra and Pang et al., which Section 6 already has; the
   section now cites `zhong2020testsuite` only. The sentence that the
   preference term alone brings no gain on Spider test is gone too
   (length; Section 6 has it). The other flows the note lists (58
   questions correct with FedAvg SFT only; 42 of the 128 execution
   errors) are not printed: the paragraph names three counts as counts
   and claims no cause.
5. Note 5. (a) The 0.5B model is no longer set beside the number of
   warm-up rounds; the sentence is "a setting, $T_w = 2$ for every
   model and dataset outside the variants of Section 6". (b) The
   paragraph on the setting now says that the clients come from the
   training set of one benchmark and are skewed by query complexity
   only, and that other heterogeneity is not studied; and that a
   client's number of pairs depends on how the model performs on its
   data, with the result of Section 6 on the question counts as
   weights. (c) Section 8 now says the clients train "on pairs of a
   correct and an incorrect sample with a preference term and an NLL
   term".

Doubts after this revision:

1. Paragraph 1, "establish". The halved execution errors against
   FedAvg SFT are counts of Section 5.4 without a test of their own;
   the tested part is the effect of the preference term after one
   round (Section 6). The sentence joins the two under "the results
   establish an effect", as your note 4 words it.
2. Paragraph 2 makes two points in one topic sentence (both kinds; not
   the preference term alone). It reads as one argument about what the
   gain consists of, but it is the paragraph to split if the section
   gets more room.
3. The paragraph on the setting says "we make no claim about what is
   revealed by an adapter or by a client's number of pairs". The brief
   states the dependence of the pair counts on the model as a fact
   beside L3; I joined it to the claim on privacy, since that is where
   a reader meets it.
4. Section 8 still says "the incorrect results do not become fewer",
   as statement 2 of its brief has it, while Section 7.1 now says they
   are more numerous in value. "Do not decrease" holds either way; say
   if the Conclusion should give the direction.
5. Length. Section 7 is at 777 of 780 words with nothing spare; each
   of the items left out above (the Spider counts of the label
   paragraph, the gold SQL query as the correct side of a pair, the
   number of the tested TS difference) needs a cut elsewhere.

## Revision 2

After the editor's notes of round 2 and the brief as corrected again
(limitations 1 and 2). Section 7 prints 778 words and Section 8 prints
197; both are at their upper ends. Both files pass `make lint`, every
macro prints a value, and the build has no undefined reference. Where
this section and "Revision 1" differ, this one holds.

What each note led to:

1. Note 1 (paragraph 1 of Section 7.1). (a) "No such effect is
   established for the incorrect results" is gone. The paragraph now
   opens on what is tested, the effect of the preference term in one
   round, and gives both of its sides in one sentence: significantly
   fewer execution errors and, on BIRD dev, significantly more
   incorrect results. (b) The halving against FedAvg SFT is called "a
   difference of counts", and "the results establish an effect of
   `\method`" is gone. (c) The paragraph ends on the shift: on BIRD
   dev, 107 of the 268 execution errors of FedAvg SFT return an
   incorrect result with `\method`, "of which no error warns the
   user". The opening names its subject at once. The Conclusion says
   the same in a clause ("part of the queries that now execute return
   an incorrect result").
2. Note 2 (paragraphs 2 and 3). The closing sentence of paragraph 2
   ("established for the execution errors only") is gone; the
   paragraph is now only about the gain in EX (both kinds; not the
   preference term alone). Paragraph 3 says that the pairs of the
   first preference round agree with the tested effect, that the
   preference term is isolated in this round only, and that "we do not
   attribute the changes of the second to its pairs". The second round
   is then told in full: on BIRD dev the execution errors rise from
   102 to 128 and the incorrect results fall from 723 to 658; on
   Spider test the execution errors fall further and the incorrect
   results stay level. "Whose" is resolved ("of the 268 execution
   errors of FedAvg SFT"), and "What the preference term adds through
   the incorrect samples" is gone.
3. Note 3 (the label paragraph and Section 8). One place now says what
   is known and what is not: a label and EX both compare results on
   one database; "How much of the gain rests on such queries is known
   only in part"; on BIRD dev the larger rise is in the correct
   predictions that read other tables or columns (136 to 191 against
   517 to 557), on Spider test in the other group; "the first count
   does not say how many of its queries are not equivalent"; for
   Spider, TS keeps the direction of the difference on the three sets
   with test suites; "BIRD has no test suite, and its gain has no
   stricter check". Section 8 adds "On BIRD dev, which has no test
   suite, the gain is measured by EX alone", and its first direction
   is the stricter label. I did not write what the group mixes (an
   added join, fewer tables, other columns): the paper has no such
   breakdown, so the sentence says only that the count does not tell.
4. Note 4 (the warm-up rounds). The paragraph opens on "the evaluation
   evidence is from the Spider sets only". It takes up the reason of
   Section 3.3 (fewer training questions without a correct sample),
   then says that EX on Spider test is nevertheless level. The two
   differences of the variant that could each lower its TS are named
   together, with the statement that the rows do not separate them:
   it never trains on a gold SQL query, and it runs four preference
   rounds instead of two. The earlier "one reading" on queries that
   are not equivalent is gone from this paragraph; the label paragraph
   carries that point once.
5. Note 5. (a) The clients are "simulated from the training set of one
   benchmark and differ in domain and schema; the skew that is varied
   is query complexity"; not studied are "partial participation, more
   than ten clients, clients from different sources and more than two
   preference rounds". (b) The comparison with question counts as
   weights is out; the sentence says only that no claim is made about
   what an adapter or a client's number of pairs reveals. (c) The two
   limits are in: two preference rounds are all that is studied, and
   the sampled queries are executed on the clients' databases,
   "read-only and under the time limit of the evaluation; the load on
   a database in use is outside the study". (d) The second direction
   of Section 8 now says why it is open: "supervision for questions
   without a gold SQL query, for which the present label cannot be
   computed". The third direction names more than ten clients, partial
   participation and more preference rounds.

Repetitions the reader listed:

- The cost. Section 7 no longer has the sentence on the client time
  of a preference round or on communication (Sections 3.5 and 5.4 and
  Table 7 have them). The Conclusion keeps one clause, "at the cost of
  additional computation at the clients", and no longer speaks of
  communication.
- One database and queries that are not equivalent. It is now said
  once in Section 7 (the label paragraph). The warm-up paragraph and
  the first direction of Section 8 no longer repeat it.

Left out, and why (all for the limit of 780 words):

- Limitation 4 of the brief as a sentence of Section 7 (see above).
- Limitation 3, second half: that a client's number of pairs depends
  on how the model performs on its data, and the result with question
  counts as weights. The first is reduced to "a client's number of
  pairs" in the sentence on what is revealed; the second read as a
  remedy and rests on one preference round.
- Limitation 5: "a question on a database without rows yields no
  pair". Sections 3.4 and 4.2 state it with the counts.
- Limitation 6: the second seed of the two main rows on BIRD. Section
  4.5 announces it and Table 3 will carry it; the sentence here says
  what the test covers.
- The time limits as values (`\setting{timeout.bird}`,
  `\setting{timeout.spider}`); the sentence says "the time limit of
  the evaluation".
- From note 4 of round 1 and note 3 of this round: the Spider counts
  of the two groups of correct predictions, given here only as "the
  second group has the larger rise"; and the gold SQL query as the
  correct side of a pair.

What stays open:

1. Paragraph 1 says of the halved execution errors only that they are
   a difference of counts. A test of the execution errors of `\method`
   against FedAvg SFT after four rounds, like the one Section 6 runs
   for the preference term, would let the paper say more; the macros
   `\errpval` exist for the other comparison only.
2. "Of which no error warns the user" is an observation about the two
   kinds of incorrect prediction, not a result. If the abstract and
   the Introduction keep the halving as a headline, they should carry
   the same clause as the Conclusion now does.
3. Paragraph 3, "agree with the tested effect". It is bounded to the
   first preference round, where more than half of the pairs have a
   failing sample as their incorrect side on both datasets; the
   paragraph prints the counts and no share.
4. The label paragraph compares two rises of counts that Section 5.4
   takes for each method separately. It draws no share of the gain
   from them and says what the count does not tell.
5. The pair counts by kind and the counts of the two groups of correct
   predictions remain in the text only; the proposals above (two
   columns in Table 7) would give them a float.
6. Section 7 is at 778 words. Anything added needs a cut.
