# Section 6, Ablation study: checks and editor's notes

Draft: `sections/06_ablation.tex`. The writer's outline:
`briefs/06_ablation_outline.md`; the writer's notes:
`briefs/06_ablation_notes.md`.

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief, Sections 2 to 5 and `main.tex`, and no other
file of the notes. One agent wrote the outline and the draft.

## 1. Outline

Seven paragraphs, 790 words planned, no subsection. The outline serves
every statement of the brief (B1, B3 to B8) and each sentence of
Sections 2.2, 3.3, 3.4, 4.4, 4.6, 5.1 and 5.3 that points to this
section. It does not depart from the brief or from `OUTLINE.md` in
content. What differs in form:

| Point | Brief or `OUTLINE.md` | Outline |
|---|---|---|
| Order | the order of Section 3 or of Table 8, as an offer | the parts of a preference round first (pairs and reference, NLL term, preference term), then the warm-up rounds, then the server: in the order of Section 3 the section would open on rows whose EX is level |
| B5 | one statement | two paragraphs: the rows and the test-suite result; then the counts of questions without a correct sample with B8 |
| B2 (second preference round) | in `OUTLINE.md` for Section 6 | a clause only: Section 5.1 gives its numbers (as the brief says) |

Answers of mine:

- B1: the EX of the row after four rounds may stand beside that of the
  method after three, as two cells of the table. Nothing is said of
  what the second round of the row adds: its first preference round was
  run again on the same pairs and the model after three rounds was not
  evaluated.
- B3: "brings no gain" with the two EX values for the comparison with
  the model before the round, which has no test; "lower" for the tested
  comparison with the method. The credit names CodeLutra and Pang et
  al. and says what they report.
- B4: the execution errors of the model before the round are added
  (286 on BIRD dev, 183 on Spider test), so that the three counts show
  what each term removes.
- B5: "level for the three numbers of warm-up rounds tried" on Spider
  test, not "does not depend"; test-suite accuracy is known for no and
  two warm-up rounds only.

Table 8 was changed in the generator after the outline (the writer's
point 8): the blocks are headed "4 rounds" and "3 rounds", since "2
warm-up rounds, 2 preference rounds" did not hold for the two rows on
the warm-up rounds; and the table opens with the row "FedAvg SFT, 2
rounds" (EX only, no test), the model before the preference rounds,
which the text of B3 and B4 refers to.

## 2. First draft: checks

| Check | Result |
|---|---|
| Build (`make`) | 25 pages, no error; the section is on pages 16 to 18 |
| `tools/lint.py --journal jiis` | 0 STOP |
| Length (`tools/style_profile.py`) | 874 words of running text; limit 880 |
| Numbers | every number that prints read against `generated/numbers.md`; no sentence found above a ceiling of `CLAIMS.md` |
| Mechanical change of mine | the TS differences printed with a sign ("by +3.20 points"): new macro `\tsgap`, used in Sections 5 and 6 |

## 3. Cold read 1

`cold_reviews/2026-11-27_0432_section6_1.md` (isolated session, section
template; pages 16 to 18 under review, pages 1 to 15 before them). Ten
findings; 7 and 8 are about the end of Section 5.4, which stood on the
first of the three pages.

| # | Finding | What was done |
|---|---|---|
| 1 (major) | the paragraph on the preference term opens on untested counts and never says what the term adds in EX; "the larger part of the reduction requires the preference term" is a causal claim from counts | note 1; B4 of the brief now gives the three EX values per dataset first; a paired test on execution errors added to the generator (below) |
| 2 (major) | "carries over to TS with two warm-up rounds and does not without them": one significant set of three, the variant never tested against FedAvg SFT, Spider-DK the other way | note 2; B5 now says what each half rests on |
| 3 (major) | the fixed row changes pairs and reference together; "level" on Spider test says nothing, the second preference round adds +0.74 there; one dataset, one seed | note 4; B1 says the row does not separate the two and gives the step of the second round for a clause |
| 4 (minor) | "not a significant difference (p = 0.0073)"; "does not raise" understates 2.61 points; the text family is not described; the gold-SQL pairs were run with $T_w$ = 0 only | note 3 (adjusted p beside it, the size said); the last two points are in `REVIEW_NOTES.md` |
| 5 (minor) | no ablation of $M$, $N$, $\beta$, $\lambda$ | the owner's (`REVIEW_NOTES.md`, A5) |
| 6 (minor) | "do not change EX" reads no significance as equality; how different were the weight vectors | note 5; new facts `weights.<set>.<rule>.max_shift` |
| 7, 8 | Section 5.4: share of the gain that reads other tables or columns; the comparison at equal client time is on Spider only | already in `REVIEW_NOTES.md` (A16, A17); the second added there |
| 9 (minor) | the question counts do not add up: Spider 16 too many, BIRD 87 short | generator corrected for Spider (below); BIRD: the 87 are gold queries over the time limit, which Section 4 does not mention (`REVIEW_NOTES.md`) |
| 10 (remark) | "Clients pooled" has no stated purpose and stands inside the paragraph on the weights | note 5; B7 says what the row is for |

Also from the report: Section 2.2 promised the three choices of Liu et
al. and the section never cites them (note 4); "relative to the loss
with both terms" read twice (note 4); the convention on p-values, the
description of FedDPO and the TS differences said more than once (given
to the writer with the length).

Changes in `tools/paper_numbers.py` after the cold read:

- `warmup.<set>.k<w>.no_correct` leaves out the questions on databases
  without rows, as the counts of Table 7 do. Spider: 1,016, 557 and 470
  (before: 1,074, 573, 483); BIRD unchanged. With it the Spider counts
  of the first preference round add up to the training set: 4,013 with
  pairs, 2,327 with only correct samples, 557 without a correct sample,
  1,759 on databases without rows, 3 whose gold SQL query fails.
- `train.<set>.with_rows`: the questions on databases with rows
  (Spider 6,900).
- `weights.<set>.questions.max_shift`, `weights.<set>.equal.max_shift`:
  the largest change of one client's weight against the weights by pair
  counts, in percentage points, from the committed records of the
  re-averaged adapters: BIRD 2.1 and 13.3, Spider 10.8 and 9.4.
- `\errpval`, `\errpadj`: the exact McNemar test on whether the
  prediction of a question ends in an execution error, the row without
  the preference term against the method at 3 rounds: BIRD dev 36
  questions with an error under the method only and 182 under the row
  only, p = 1.1e-24; Spider test 41 and 95, p = 4.2e-6. The two tests
  join the family of the comparisons quoted in the text (17 now); no
  other adjusted value changes its side of 0.05.

## 4. Editor's notes, round 1

Sent to the same agent with the corrected brief.

1. The preference term: the reader does not learn what it adds in EX;
   the three EX values first, then the counts with their test; the
   sentence on the share that "requires" the term goes.
2. Warm-up rounds and TS: say what each half of "carries over ... and
   does not" rests on; the TS differences are repeated from Table 6;
   "the three variants" includes the method.
3. Two p-values below 0.05 called not significant: the adjusted value
   beside them; the size of the difference for the gold SQL as the
   correct side.
4. The fixed row and what the rows are: "one part" does not hold for
   the fixed row or for "Clients pooled"; "level" on Spider test
   against what the second round adds there; Liu et al. cited where
   their choices are varied; the credit sentence says against what the
   accuracy falls.
5. The server: "no significant difference" in place of "do not change",
   with how far the weights move; what "Clients pooled" is for.

Brief corrected in the same places (B1, B3, B4, B5, B8, B6, B7, the
macro table, a paragraph on what the rows are). Length raised from 880
to 930 at most: B8 was added after the 880 of `OUTLINE.md` was set, and
the notes add numbers the reader asked for.

Answers to the writer's doubts: 1 cut; 2 yes; 3 `\tsgap`; 4 note 2; 5
each round of the row samples, labels and pairs anew (`run_train` in
`fedls_sql/federated/pref_rounds.py`); 6 a gloss of GSM8K is the
writer's choice; 7 the waiting sentences are read again when the rows
are in.

## 5. Revision 1: checks

| Check | Result |
|---|---|
| Build (`make`) | 25 pages, no error; 48 numbers print as `??` (58 before: the sentences on two waiting rows were cut for length) |
| `tools/lint.py --journal jiis` | 0 STOP |
| Length | 928 words; limit 930 |
| Style signals (`style_profile.py compare --kind experiments`) | mean sentence 33 words against 21 in the reference sections: the sentences carry many numbers. Signal only |
| Notes of round 1 | all five taken up; the writer's report lists the changes |

## 6. Cold read 2

`cold_reviews/2026-11-27_0454_section6r1_1.md` (another isolated
session, same template, pages 16 to 18 of the new build).

| # | Finding | What was done |
|---|---|---|
| 1 (major) | the preference term is not shown to matter in EX and the paragraph does not say so; "lies between" is a ranking without a test; the execution errors are tested, the incorrect results (more with the method) are not; the NLL-only row runs at the learning rate of the preference rounds | note 2; a second paired test, on incorrect results (below); the rest is the owner's (`REVIEW_NOTES.md`, C29) |
| 2 (major) | Section 5.4: more than half of the BIRD gain is in predictions that read other tables or columns than the gold query | not this section (`REVIEW_NOTES.md`, A16, A17, C20) |
| 3 (major) | the paragraph on the warm-up rounds opens on the uninformative result and draws no conclusion | note 1; B5 asks for the conclusion in the first sentence |
| 4 | Section 5.4: comparison at equal client time on Spider only | not this section (A15, C17, C23) |
| 5 (minor) | Section 2.2 promises "all three" choices varied, two are varied together; the fixed row (46.15) beside the method after three rounds (46.22) is not in the text | note 4; the sentence of Section 2.2 is in `REVIEW_NOTES.md` (B23) |
| 6 (minor) | the gold SQL as the correct side: a configuration used nowhere else, no conclusion, the colon read as a reason, "an incorrect sample" unclear | note 3; B8 says how the pairs are constructed |
| 7 (minor) | the claim on the weights is wider than the test (one round averaged again) | note 5; B6 |
| 8 (minor) | unadjusted and adjusted p-values mixed after "significance is stated after the correction" | note 3; a row on the convention in the brief |
| 9, 10 (remarks) | Section 5.4: questions with only correct samples rise sevenfold; the section moves between the blocks without a map | 9: `REVIEW_NOTES.md` (C22); 10: note 5 |

Also from the report: the same difference, -2.61, appears for two
comparisons of the section (the fixed row on BIRD dev; the gold SQL as
the correct side), both 40 questions of 1,534; the reader suspected a
copying error. Both are right (48.76 - 46.15 and 41.85 - 39.24).

Change in `tools/paper_numbers.py` after cold read 2: `\wrpval`,
`\wrpadj`, the same paired test on whether a prediction is an
incorrect result, for the same two comparisons as `\errpval`. BIRD
dev: 198 questions with an incorrect result under the method only, 80
under the row only, p = 1.0e-12. Spider test: 89 and 69, p = 0.13. The
family of the comparisons of the text has 19 tests now; the adjusted p
of the gold-SQL comparison moves from 0.058 to 0.065, and no adjusted
value changes its side of 0.05.

## 7. Editor's notes, round 2 (the last)

1. Warm-up rounds: the reader does not learn what the paper concludes;
   open on what they change and what they do not, each with its basis.
2. The preference term: "lies between" is an untested ranking; both
   kinds of incorrect prediction now have a test; the first sentence
   says what the row establishes.
3. p-values: one sentence on the convention; both values for the
   comparison that is in no table; the colon before the counts; how
   the gold-SQL pairs are constructed.
4. The fixed row: beside the method after three rounds, as two cells;
   the antecedents of "the first" and "which".
5. The opening and the server: which parts are taken apart and in what
   order; the statement on the weights scoped to what the rows test.

Brief corrected in the same places. Both rounds are used with this
one: what the next reading finds goes to `REVIEW_NOTES.md`.

## 8. Revision 2: checks, and what stays open

| Check | Result |
|---|---|
| Build (`make`) | 25 pages, no error; 48 numbers print as `??` |
| `tools/lint.py --journal jiis` | 0 STOP |
| Length | 927 words; limit 930 |
| Notes of round 2 | all five taken up; every number read against `generated/numbers.md`, no sentence above a ceiling of `CLAIMS.md` |

Both rounds are used. No third cold read was run. Open, for the owner
(`REVIEW_NOTES.md`):

- The paragraph on the preference term no longer says in words that
  the row is above the model before the round in EX; the first row of
  Table 8 shows it (B27).
- "what differs is test-suite accuracy" in the first sentence on the
  warm-up rounds rests on values and one significant test of three;
  its basis follows in the next two sentences (B28).
- Three waiting rows have no sentence in the text: the row without the
  preference term after four rounds, and the rows with no and with
  three warm-up rounds on BIRD dev. Each needs about 20 words when it
  is in; the section stands 3 words under its limit.
- The adjusted p of the gold-SQL comparison prints 0.065 (0.058 before
  the two tests on incorrect results joined the family of the text).
