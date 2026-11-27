# Checks: Section 6, Ablation study, Table 8

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0). Items marked "v1" come from the review
of the first drafts (tag `draft-v1-2026-11-27`); the limits that the
brief of this section still carries in its Ceiling column move into
part 3 when the brief is rewritten.

## 1. Facts about our work

- Table 8: the blocks are "4 rounds" and "3 rounds"; the first row is FedAvg SFT after 2 rounds (BIRD 42.70, Spider 74.10; EX only, no test), the model from which every row but the two with another number of warm-up rounds starts. "Without the NLL term" on Spider (73.59) is below that starting point. (v1 B24)
- Questions without a correct sample on Spider, on databases with rows: 1,016, 557 and 470 with 0, 2 and 3 warm-up rounds (the raw counts of the round records, 1,074, 573 and 483, include questions on databases without rows). BIRD: 4,035 and 2,698. (v1 B25)
- Without the preference term (the NLL term alone on correct samples): the round still ends above the model before it (44.39 against 42.70 on BIRD dev; 75.87 against 74.10 on Spider test). Against the round with both terms: fewer execution errors with the preference term, significant; a difference in EX is not significant after correction on either dataset. No ranking by "lies between" without a test. (v1 B27, B36)
- Warm-up rounds: at 4 rounds on Spider test, 78.02, 78.20 and 77.97 for 0, 2 and 3. What differs is test-suite accuracy (the variant without warm-up is below FedAvg SFT in TS on all three sets by value, one of three tests significant, on Spider-Syn) and the number of questions without a correct sample. (v1 B28)
- The gold SQL query as the correct side for questions without a correct sample (B8): BIRD dev only, the variant without warm-up, one preference round: 39.24 against 41.85 (-2.61, p 0.0073, 0.077 after Holm in the family of the text). A number of the text, not a row of Table 8; nothing is said for Spider. (owner, A2)
- Three waiting rows had no sentence in the first draft: without the preference term after 4 rounds; 0 and 3 warm-up rounds on BIRD dev.

## 2. Facts about cited papers

Four published results on a likelihood term in DPO (locators in `02_related_rows.md`); two support the term and two do not, and the section carries all four:

- CodeLutra, Table 2: Spider 17.2 with the DPO term alone, 76.6 with the full loss.
- Pang et al., Table 1: GSM8K 61.8 against 73.1, one round.
- Liu et al., App. A, Table 7: an added SFT term on SQL-only output, 58.8 to 60.0, which they call a limited gain.
- Lanchantin et al., Sec. 4.2: an added NLL term did not help in their task. (Cited only here.)

## 3. Claims: strength, scope, what waits

- On-policy pairs against fixed pairs and reference: lower EX on BIRD dev (+2.61 for the method, p 5.7e-4); level on Spider test (78.20 against 78.02, p 0.78).
- The preference term over training on correct samples at 3 rounds: +1.83 on BIRD dev (p 0.057), +1.59 on Spider test (p 0.015, 0.14 after Holm).

## 4. What the section carries for other sections

- Section 3 points here for the counts behind the warm-up rounds; Section 2.2 points here for the choices varied.
