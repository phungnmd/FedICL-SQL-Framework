# Checks: Section 5, Results

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0).

## 1. Facts about our work

- BIRD dev, execution errors by round of the method: they rise in the second preference round (102 to 128). The transition from round 3 to round 4 (of 723 incorrect results, 56 become correct and 54 become execution errors) is not a macro yet.
- Correct predictions by the form of the query (claim C3): the counts are taken for each method separately; EX establishes correctness on the evaluation database only.
- Cost and the comparison beyond equal rounds (owner, 2026-11-27; `CLAIMS.md`, E2). The rows of the paper are compared at equal rounds. Table 7 prints GPU minutes (sampling, training, total) and the CPU minutes of the label step apart; no figure adds them, and none is called "client time". GPU time of a preference round against an SFT round: 1.8 and 1.3 on BIRD (310 and 223 against 173 min), 1.6 and 0.9 on Spider (201 and 106 against 124), `\fact{cost.<set>.pref<r>.gpu_min}` and `.gpu_ratio`. Label step: 159 and 168 min on BIRD, 3 and 3 on Spider. Over four rounds: BIRD 879 GPU min against 692, Spider 555 against 496. A baseline with more GPU time than the method: on Spider run (5 SFT rounds take 620 min; 78.20 against 73.92); on BIRD 5 SFT rounds would take 865 min, and 4 are run. (v1 A15, C17, C42)
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

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. The macros and
citation keys by section are in `inventory.txt`.

### `sections/05_results.tex`

Headings and labels:

- `\section{Results}` `sec:results`
- `\subsection{Comparison with the baselines (RQ1)}` `sec:rq1`
- `\subsection{Other models and federated setups (RQ2)}` `sec:rq2`
- `\subsection{Perturbed questions and test-suite accuracy (RQ3)}` `sec:rq3`
- `\subsection{Analysis of the predictions and cost of a round (RQ4)}` `sec:rq4`

Floats:

- table `tab:main`, from `generated/tab_main`
- figure `fig:rounds`
- table `tab:models`, from `generated/tab_models`
- table `tab:federated`, from `generated/tab_federated`
- table `tab:robust`, from `generated/tab_robust`
- figure `fig:errors`
- table `tab:cost`, from `generated/tab_cost`
