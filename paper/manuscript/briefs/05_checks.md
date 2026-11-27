# Checks: Section 5, Results and analysis, Tables 3 to 8

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0).

## 1. Facts about our work

- BIRD dev, execution errors by round of the method: they rise in the second preference round (102 to 128). The transition from round 3 to round 4 (of 723 incorrect results, 56 become correct and 54 become execution errors) is not a macro yet.
- Correct predictions by the form of the query (claim C3): the counts are taken for each method separately; EX establishes correctness on the evaluation database only.
- Cost and the comparison beyond equal rounds (owner, 2026-11-27; `CLAIMS.md`, E2). The rows of the paper are compared at equal rounds. Table 8 prints GPU minutes (sampling, training, total) and the minutes of the label step apart (elapsed time on 16 CPU threads); no figure adds them, and none is called "client time". GPU time of a preference round against an SFT round: 1.8 and 1.3 on BIRD (310 and 223 against 173 min), 1.6 and 0.9 on Spider (201 and 106 against 124), `\fact{cost.<set>.pref<r>.gpu_min}` and `.gpu_ratio`. Label step: 159 and 168 min on BIRD, 3 and 3 on Spider. Over four rounds: BIRD 879 GPU min against 692, Spider 555 against 496. A baseline with more GPU time than the method: on Spider run (5 SFT rounds take 620 min; 78.20 against 73.92); on BIRD 5 SFT rounds would take 865 min, and 4 are run. (v1 A15, C17, C42)
- Cost: as in `01_checks.md`.
- "No training" is the pretrained model; Section 5.1 says so. The captions of the result tables explain the asterisk and the unadjusted p.
- The second training seed on BIRD: its rows of Table 3 wait.

For the ablation study (5.3):

- Table 4: the blocks are "4 rounds" and "3 rounds"; BIRD dev has EX and test-suite accuracy (the generated suite), Spider test EX. The "4 rounds" block has a FedAvg SFT row: its EX test is the one of Table 3, printed again, and its test-suite test on BIRD dev is printed here only (C4: 36.70 against 41.59, p 4.2e-8). The first row is FedAvg SFT after 2 rounds (BIRD 42.70 and 36.11 under the suite, Spider 74.10; no test), the model from which every row but the two with another number of warm-up rounds starts. "Without the NLL term" on Spider (73.59) is below that starting point.
- Questions without a correct sample on Spider, on databases with rows: 1,016, 557 and 470 with 0, 2 and 3 warm-up rounds (the raw counts of the round records, 1,074, 573 and 483, include questions on databases without rows). BIRD: 4,035 and 2,698.
- Without the preference term (the NLL term alone on correct samples): the round still ends above the model before it (44.39 against 42.70 on BIRD dev; 75.87 against 74.10 on Spider test). Against the round with both terms: fewer execution errors with the preference term, significant; a difference in EX is not significant after correction on either dataset. No ranking by "lies between" without a test.
- Warm-up rounds: at 4 rounds on Spider test, 78.02, 78.20 and 77.97 for 0, 2 and 3. What differs is test-suite accuracy (the variant without warm-up is below FedAvg SFT in TS on all three sets by value, one of three tests significant, on Spider-Syn) and the number of questions without a correct sample.
- The gold SQL query as the correct side for questions without a correct sample (B8): BIRD dev only, the variant without warm-up, one preference round: 39.24 against 41.85 (-2.61, p 0.0073, 0.077 after Holm in the family of the text). A number of the text, not a row of Table 4; nothing is said for Spider. (owner, A2)
- Three waiting rows need a sentence when their results are in: without the preference term after 4 rounds; 0 and 3 warm-up rounds on BIRD dev.

## 2. Facts about cited papers

None beyond the baselines' sources in Section 4.

For the ablation study (5.3):

Four published results on a likelihood term in DPO (locators in `02_related_rows.md`); two support the term and two do not, and the section carries all four:

- CodeLutra, Table 2: Spider 17.2 with the DPO term alone, 76.6 with the full loss.
- Pang et al., Table 1: GSM8K 61.8 against 73.1, one round.
- Liu et al., App. A, Table 7: an added SFT term on SQL-only output, 58.8 to 60.0, which they call a limited gain.
- Lanchantin et al., Sec. 4.2: an added NLL term did not help in their task. (Cited only here.)

## 3. Claims: strength, scope, what waits

- A1: above FedAvg SFT at the same number of rounds on both datasets, significant after correction; the headline is BIRD dev.
- A2: FedAvg SFT "does not improve after round 3"; its falls afterwards are not significant, so not "degrades" and not "has converged".
- A5: above Centralized SFT holds on Spider with the main setup; the BIRD row waits.
- 34 rows waited on 2026-11-27 (`generated/missing.txt` is current); a sentence on a waiting number is worded for its `\expect` value or leaves the direction to the number.

For the ablation study (5.3):

- On-policy pairs against fixed pairs and reference: lower EX on BIRD dev (+2.61 for the method, p 5.7e-4); level on Spider test (78.20 against 78.02, p 0.78).
- The preference term over training on correct samples at 3 rounds: +1.83 on BIRD dev (p 0.057), +1.59 on Spider test (p 0.015, 0.18 after Holm in the 16 tests of Table 4).

## 4. What the section carries for other sections

- The tests on the two kinds of incorrect prediction (execution error, incorrect result) of the method against FedAvg SFT at 4 rounds are reported here; Section 6 interprets them.

For the ablation study (5.3):

- Section 3 points to 5.3 for the counts behind the warm-up rounds; Section 2.2 points to 5.3 for the choices varied.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. The macros and
citation keys by section are in `inventory.txt` (the file names there are
those of the eight sections of 2026-11-26).

### `sections/05_results.tex`

Headings and labels:

- `\section{Results and analysis}` `sec:results`
- `\subsection{Main results}` `sec:main`
- `\subsection{Analysis of the predictions}` `sec:analysis`
- `\subsection{Ablation study}` `sec:ablation`
- `\subsection{Other models and federated setups}` `sec:breadth`
- `\subsection{Perturbed questions}` `sec:perturbed`
- `\subsection{Computation and communication cost}` `sec:cost`

Floats, in the order of first mention:

- table `tab:main`, from `generated/tab_main` (Table 3)
- figure `fig:rounds` (Fig. 3)
- figure `fig:errors` (Fig. 4)
- table `tab:ablation`, from `generated/tab_ablation` (Table 4)
- table `tab:models`, from `generated/tab_models` (Table 5)
- table `tab:federated`, from `generated/tab_federated` (Table 6)
- table `tab:robust`, from `generated/tab_robust` (Table 7)
- table `tab:cost`, from `generated/tab_cost` (Table 8)
