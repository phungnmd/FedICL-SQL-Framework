# Checks: Sections 6 and 7, Discussion and limitations, Conclusion

What stays true whatever the draft says: facts and the bounds of claims.
It is read before the section is written and when it is checked; remarks
on the wording of a draft are not kept here.

## 1. Facts about our work

- The method has 2 preference rounds among its T = 4 rounds and is not trained further; only the variant without warm-up rounds has more.
- Tests against FedAvg SFT at 4 rounds. Execution errors: BIRD dev 182 questions fail only with FedAvg SFT and 42 only with the method (p = 5.8e-22); Spider test 118 and 29 (p = 6.2e-14); both significant after Holm. Incorrect results: BIRD dev p = 0.007, 0.077 after Holm (156 and 111); Spider test p = 0.37 (111 and 97); neither significant after correction. (owner, A31)
- Cost: as in `01_checks.md`.
- The counts of pairs by kind of incorrect sample are in no table; two columns of Table 8 are proposed for them (`REVIEW_NOTES.md`, C44).

- From the reviewer's reads of Sections 3 and 4, for the limitations: the generated suite of BIRD dev is compared with an official suite on Spider dev only, since BIRD has none; each row is one training run, so the tests do not cover the variation between runs; a gold SQL query over the time limit leaves a question without labels, and that count differs between runs (30 to 92 of 9,428 on BIRD); a comparison at more GPU time for the baseline exists on Spider only (`REVIEW_NOTES.md`, A34); with two preference rounds the pairs and the reference are renewed once.

## 2. Facts about cited papers

None of its own.

## 3. Claims: strength, scope, what waits

- The preference term is isolated in one round only; what the second preference round changes is not attributed to its pairs.
- The limitations of `CLAIMS.md`, section 5, each stated once, in the limitations subsection, at the size the evidence gives: added client computation over the rounds; a client's number of pairs depends on the model's performance on its data, and it is sent to the server; questions on databases without rows yield no pair; one training seed and one draw of the partition (the second seed on BIRD when its row is in); clients must be able to execute SQL on their databases; data isolation, not differential privacy; EX alone on BIRD dev, which has no test suite.
- The conclusion states the problem, the framework and the principal findings, and adds no qualification that the limitations subsection does not hold (`VOICE_GUIDE.md`).
- C3 (correct predictions by form of query) is reported, not interpreted (owner, A27).
- Model size is a boundary of the study (`CLAIMS.md`, section 5, items 7 and 8): models of 0.5B to 1.5B parameters with LoRA, SQLite benchmarks in English; where FedAvg SFT is still improving fast (the 0.5B model) the gain is smaller. Stated once, in the limitations subsection.

## 4. What the section carries for other sections

Nothing.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. `make inventory` lists the macros and
citation keys by section.

### `sections/06_discussion.tex`

Headings and labels:

- `\section{Discussion and limitations}` `sec:discussion`
- `\subsection{Interpretation of the results}` `sec:interpretation`
- `\subsection{Scope and limitations}` `sec:limitations`

### `sections/07_conclusion.tex`

Headings and labels:

- `\section{Conclusion}` `sec:conclusion`
