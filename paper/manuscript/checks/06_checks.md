# Checks: Sections 6 and 7, Discussion, Conclusion

What stays true whatever the draft says: facts and the bounds of claims.
It is read before the section is written and when it is checked; remarks
on the wording of a draft are not kept here.

## 1. Facts about our work

- The method has 2 preference rounds among its T = 4 rounds and is not trained further; only the variant without warm-up rounds has more.
- Against FedAvg SFT at 4 rounds, the paper states the counts of execution errors and incorrect results without a test: no table prints it (owner, 2026-11-28). Notes only: execution errors, BIRD dev 182 questions fail only with FedAvg SFT and 42 only with the method (p = 5.8e-22), Spider test 118 and 29 (p = 6.2e-14); incorrect results, BIRD dev p = 0.007 (156 and 111), Spider test p = 0.37 (111 and 97). (owner, A31)
- Cost: as in `01_checks.md`.
- The counts of pairs by kind of incorrect sample are in no table; two columns of Table 8 are proposed for them (`REVIEW_NOTES.md`, C44).

- From the reviewer's reads of Sections 3 and 4, for the limitations: the generated suite of BIRD dev is compared with an official suite on Spider dev only, since BIRD has none; each row is one training run, so the tests do not cover the variation between runs; a gold SQL query over the time limit leaves a question without labels, and that count differs between runs (30 to 92 of 9,428 on BIRD); a comparison at more GPU time for the baseline exists on Spider only (`REVIEW_NOTES.md`, A34); with two preference rounds the pairs and the reference are renewed once.

## 2. Facts about cited papers

None of its own.

## 3. Claims: strength, scope, what waits

- The preference term is isolated in one round only; what the second preference round changes is not attributed to its pairs.
- Second revision (owner, 2026-11-28): the last paragraph of the Discussion is a statement of scope and future work, the three items of `CLAIMS.md`, section 5: gold SQL and executable databases at each client; at most ten clients with full participation, partial participation as future work; privacy as data isolation, differential privacy as future work. One training run, one draw of the partition, chance matches of execution labels and the measure of the training labels are notes for a reviewer, not printed. The reading of why execution errors fall is stated as a reading, without "which we did not test". The first paragraph opens with the gain over FedAvg SFT in every configuration trained independently (both benchmarks, each model with a committed row: Tables 2 and 4 in the PDF); a row still to come extends it without a rewrite.
- The conclusion states the problem, the framework and the principal findings, and names partial participation and differential privacy as future work, as the Discussion does (owner, 2026-11-28); it no longer states incorrect results or one training run.
- C3 (correct predictions by form of query) is reported, not interpreted (owner, A27).
- The first paragraph reads A5 with the training signal (owner, 2026-11-28, third revision): pooling the gold SQL queries of all clients does not change the reading that they are exhausted sooner, since on Spider test centralized SFT does not differ significantly from FedAvg SFT and the method is above both. Nothing is said for BIRD until its centralized row is in.
- Model size is not stated as a limitation (owner, 2026-11-28): the models are named in Section 4, and the smaller gain of the 0.5B model is stated in Section 5.4.
- The first paragraph reads the control (B9) only at 3 rounds, where its rows are committed: a further FedAvg SFT round at the settings of the preference rounds adds less than a preference round.

## 4. What the section carries for other sections

Nothing.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. `make inventory` lists the macros and
citation keys by section.

### `sections/06_discussion.tex`

Headings and labels:

- `\section{Discussion}` `sec:discussion` (no subsections (owner, 2026-11-28))

### `sections/07_conclusion.tex`

Headings and labels:

- `\section{Conclusion}` `sec:conclusion`
