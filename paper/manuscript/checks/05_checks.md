# Checks: Section 5, Results and analysis, Tables 3 to 8

What stays true whatever the draft says: facts and the bounds of claims.
It is read before the section is written and when it is checked; remarks
on the wording of a draft are not kept here.

## 1. Facts about our work

- BIRD dev, execution errors by round of the method: they rise in the second preference round (102 to 128). The transition from round 3 to round 4 (of 723 incorrect results, 56 become correct and 54 become execution errors) is not a macro yet.
- C3 stands in Section S6.4 of the Supplementary Materials with Table S6, not in Section 5.2 (owner, 2026-11-28, fourth revision); no other sentence of the main text uses a `form.*` fact.
- Correct predictions by the form of the query (claim C3): the counts are taken for each method separately; EX establishes correctness on the evaluation database only.
- Cost and the comparison beyond equal rounds (owner, 2026-11-27; `CLAIMS.md`, E2). The rows of the paper are compared at equal rounds. Table 8 prints GPU minutes (sampling, training, total) and the minutes of the label step apart (elapsed time on 16 CPU threads); no figure adds them, and none is called "client time". GPU time of a preference round against an SFT round: 1.8 and 1.3 on BIRD (310 and 223 against 173 min), 1.6 and 0.9 on Spider (201 and 106 against 124), `\fact{cost.<set>.pref<r>.gpu_min}` and `.gpu_ratio`. Label step: 159 and 168 min on BIRD, 3 and 3 on Spider. Over four rounds: BIRD 879 GPU min against 692, Spider 555 against 496. A baseline with more GPU time than the method: on Spider run (5 SFT rounds take 620 min; 78.20 against 73.92); on BIRD 5 SFT rounds would take 865 min, and 4 are run. (v1 A15, C17, C42)
- Cost: as in `01_checks.md`.
- "No training" is the pretrained model; Section 5.1 says so. The tables print the Holm-adjusted p and an asterisk for a significant difference; Section 4.5 says so.
- No second-seed rows, no FedProx SFT, no local SFT on Spider (owner, 2026-11-28).
- Second revision (owner, 2026-11-28): each paragraph of Section 5 leads with the finding that supports the method; a non-significant side result, a caveat or a list of non-significant differences that a table shows is printed only where a claim would be false or mislead without it. A finding that holds on one benchmark is stated for that benchmark. Section 5.2 states once, with Fig. 4, that incorrect results do not fall (C2). The per-client result (C6) is three sentences in Section 5.2 with Table S7 (`sections/S10_clients.tex`, label `sup:clients`, `generated/tab_clients`), on the clients' training questions, without a test.
- Third revision (owner, 2026-11-28, third revision): A5 is a headline claim. Its test is the note row "the method against centralized SFT" of each block of Table 3 (PDF Table 2): Spider test +3.17, padj 7.1e-5 among the 7 tests of the table; the BIRD row prints `--` until centralized SFT on BIRD is committed, and no sentence states anything for BIRD. C7 follows C6 in Section 5.2: at Spider client 4, 1,648 of 3,479 questions on databases without rows, 1,098 of its 2,276 mixed questions give no pair, 1,178 yield pairs; client 3 has 111; the other 3 clients and every BIRD client none. B7 (clients pooled, Spider, 4 rounds) is back in Table 4 with `--` and one sentence on what the row is.
- No p in the prose of Sections 5 and 6; "significant" only for a test that a table of the paper or of the Supplementary Materials prints. Tables S4 (EX by round) and S5 (TS on BIRD dev) print the tests of A2, B2 and C4 (owner, 2026-11-28).

For the ablation study (5.3):

- Table 4 (owner, 2026-11-28, fourth revision): the parts of a preference round, in two panels, (a) BIRD dev and (b) Spider test, each with the rows run on that benchmark (no blank cell; `--` a row that waits), and in each the blocks "4 rounds" and "3 rounds", EX with Δ and the adjusted p; the TS of its BIRD rows is in Table S5. Each block has a FedAvg SFT row and the control ("FedAvg SFT, preference-round settings"); the EX test of FedAvg SFT at 4 rounds is the one of Table 3, printed again. The 4-round block also has FedDPO, fixed pairs and reference, and no preference term (BIRD) or clients pooled (Spider); the 3-round block no NLL term (FedDPO after its first round) and no preference term. The rows without and with three warm-up rounds are out: the number of warm-up rounds is a setting, read in Section 5.4 (B5). Every row starts from FedAvg SFT after 2 rounds (BIRD 42.70, Spider 74.10); "Without the NLL term" on Spider (73.59) is below that starting point. Holm family: 12 tests (16 when the rows that wait are in). With the two warm-up tests out, BIRD FedAvg SFT against the method at 3 rounds went from 0.061 to 0.044 (raw 0.0087, the eighth of the family): Section 5.1 now says "significantly above FedAvg SFT on both benchmarks" after three rounds, to be read again when the rows that wait are in.
- Questions without a correct sample on Spider, on databases with rows: 1,016, 557 and 470 with 0, 2 and 3 warm-up rounds (the raw counts of the round records, 1,074, 573 and 483, include questions on databases without rows). BIRD: 4,035 and 2,698.
- Without the preference term (the NLL term alone on correct samples): the round still ends above the model before it (44.39 against 42.70 on BIRD dev; 75.87 against 74.10 on Spider test). Against the round with both terms: fewer execution errors with the preference term, stated as counts without a test (owner, 2026-11-28); a difference in EX is not significant after correction on either dataset. No ranking by "lies between" without a test.
- Warm-up rounds: at 4 rounds on Spider test, 78.02, 78.20 and 77.97 for 0, 2 and 3. What differs is test-suite accuracy (the variant without warm-up is below FedAvg SFT in TS on all three sets by value, one of three tests significant, on Spider-Syn) and the number of questions without a correct sample.
- B8 (the gold SQL query as the correct side) and B7 (clients pooled) are not in the paper; the variants of the server average are one sentence (B6) (owner, 2026-11-28). Their facts stay in `CLAIMS.md`.
- Not run (owner, 2026-11-28): without the preference term after 4 rounds on Spider; 0 and 3 warm-up rounds on BIRD dev. Waiting: the control after 4 rounds on both benchmarks (and its TS on BIRD dev in Table S5), FedDPO on Spider. When the three tests of the control at 4 rounds and of FedDPO on Spider enter the family of Table 4 (12 tests to 16), the adjusted p of the control at 3 rounds (0.013 on BIRD, 0.029 on Spider) change; the sentence of 5.3 is read again then.

## 2. Facts about cited papers

None beyond the baselines' sources in Section 4.

Section 5 quotes no number of another paper: the published results on a likelihood term beside the DPO term are in `02_checks.md` and belong to Section 2 (main session, 2026-11-28; CodeLutra has its fixed places, and three of the four results without it would be a partial list).

## 3. Claims: strength, scope, what waits

- A1: above FedAvg SFT at the same number of rounds on both datasets, significant after correction; the headline is BIRD dev.
- A2: FedAvg SFT "does not improve after round 3"; the method is significantly above its best round (Table S4). Its falls afterwards are tested in no table, so not "degrades" and not "has converged".
- A5: above Centralized SFT holds on Spider with the main setup; the BIRD row waits.
- 23 rows wait on 2026-11-28 (`generated/missing.txt` is current); a sentence on a waiting number is worded for its `\expect` value or leaves the direction to the number.

For the ablation study (5.3):

- On-policy pairs against fixed pairs and reference: lower EX on BIRD dev (+2.61 for the method, adjusted p 0.0046); level on Spider test (78.20 against 78.02, adjusted p 0.78).
- The preference term over training on correct samples at 3 rounds: +1.83 on BIRD dev (adjusted p 0.17), +1.59 on Spider test (adjusted p 0.061), in the 12 tests of Table 4.
- The control (B9) at 3 rounds: 0.52 below FedAvg SFT on BIRD dev and 0.74 above on Spider test, in points (no table prints that test); the method is above it by 3.06 (adjusted p 0.0098) and 2.01 (0.021). Nothing on 4 rounds until its rows are in.

## 4. What the section carries for other sections

- The counts of the two kinds of incorrect prediction (execution error, incorrect result) of the method and FedAvg SFT at 4 rounds are reported here, without a test (owner, 2026-11-28); Section 6 interprets them.

For the ablation study (5.3):

- Section 3 points to 5.4 for the method with other numbers of warm-up rounds (owner, 2026-11-28, fourth revision); Section 2.2 points to 5.3 for the choices varied.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. `make inventory` lists the macros and
citation keys by section.

### `sections/05_results.tex`

Headings and labels:

- `\section{Results and analysis}` `sec:results`
- `\subsection{Main results}` `sec:main`
- `\subsection{Analysis of the predictions}` `sec:analysis`
- `\subsection{Ablation study}` `sec:ablation`
- `\subsection{Other models, federated setups and perturbed questions}` `sec:breadth`, `sec:perturbed`
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

The PDF numbers each of these tables one lower (Table 3 is Table 2 in the PDF). In the Supplementary Materials: `tab:rounds` (Table S4, `sections/S8_rounds.tex`), `tab:ts` and `tab:form` (Tables S5 and S6, `sections/S9_suite.tex`; labels `sup:rounds`, `sup:suite`, `sup:form`).
