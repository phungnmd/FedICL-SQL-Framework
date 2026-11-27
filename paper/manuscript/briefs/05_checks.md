# Checks: Section 5, Results

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0). Items marked "v1" come from the review
of the first drafts (tag `draft-v1-2026-11-27`); the limits that the
brief of this section still carries in its Ceiling column move into
part 3 when the brief is rewritten.

## 1. Facts about our work

- BIRD dev, execution errors by round of the method: they rise in the second preference round (102 to 128). The transition from round 3 to round 4 (of 723 incorrect results, 56 become correct and 54 become execution errors) is not a macro yet. (v1 B16)
- Correct predictions by the form of the query (claim C3): the counts are taken for each method separately; EX establishes correctness on the evaluation database only. (v1 B15, A17)
- Comparison at equal client time. Spider: run (the method takes 560 min, 5 SFT rounds 620; 78.20 against 73.92). BIRD: not run (the method takes 1,207 min, about 7 SFT rounds; 4 are run). (v1 A15, C42)
- Cost: as in `01_checks.md`.
- "No training" is the pretrained model; Section 5.1 says so. The captions of the result tables explain the asterisk and the unadjusted p.
- The second training seed on BIRD: its rows of Table 3 wait.

## 2. Facts about cited papers

None beyond the baselines' sources in Section 4.

## 3. Claims: strength, scope, what waits

- A1: above FedAvg SFT at the same number of rounds on both datasets, significant after correction; the headline is BIRD dev.
- A2: FedAvg SFT "does not improve after round 3"; its falls afterwards are not significant, so not "degrades" and not "has converged".
- A5: above Centralized SFT holds on Spider with the main setup; the BIRD row waits.
- 34 rows waited on 2026-11-27 (`generated/missing.txt` is current); a sentence on a waiting number is worded for its `\expect` value or leaves the direction to the number.

## 4. What the section carries for other sections

- The tests on the two kinds of incorrect prediction (execution error, incorrect result) of the method against FedAvg SFT at 4 rounds are reported here; Section 7 interprets them.
