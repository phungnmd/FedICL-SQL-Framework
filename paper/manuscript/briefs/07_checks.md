# Checks: Sections 7 and 8, Discussion and limitations, Conclusion

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0). Items marked "v1" come from the review
of the first drafts (tag `draft-v1-2026-11-27`); the first
brief of this section is at the same tag, and its facts and the limits
of its Ceiling column are read from there when the new brief is built.

## 1. Facts about our work

- The method has 2 preference rounds among its T = 4 rounds and is not trained further; only the variant without warm-up rounds has more. (v1 B33)
- Tests against FedAvg SFT at 4 rounds. Execution errors: BIRD dev 182 questions fail only with FedAvg SFT and 42 only with the method (p = 5.8e-22); Spider test 118 and 29 (p = 6.2e-14); both significant after Holm. Incorrect results: BIRD dev p = 0.007, 0.077 after Holm (156 and 111); Spider test p = 0.37 (111 and 97); neither significant after correction. (owner, A31)
- Cost: as in `01_checks.md`.
- The counts of pairs by kind of incorrect sample appeared only in the text of Section 7.1 in the first draft; two columns of Table 7 were proposed for them. (v1 C44)

## 2. Facts about cited papers

None of its own.

## 3. Claims: strength, scope, what waits

- The preference term is isolated in one round only; what the second preference round changes is not attributed to its pairs.
- The limitations of `CLAIMS.md`, section 5, each stated once, in the limitations subsection, at the size the evidence gives: added client computation over the rounds; a client's number of pairs depends on the model's performance on its data, and it is sent to the server; questions on databases without rows yield no pair; one training seed and one draw of the partition (the second seed on BIRD when its row is in); clients must be able to execute SQL on their databases; data isolation, not differential privacy; EX alone on BIRD dev, which has no test suite. (v1 B34, C9, C15, C41)
- The conclusion states the problem, the framework and the principal findings, and adds no qualification that the limitations subsection does not hold (`VOICE_GUIDE.md`).
- C3 (correct predictions by form of query) is reported, not interpreted (owner, A27).
- Model size is a boundary of the study (`CLAIMS.md`, section 5, items 7 and 8): models of 0.5B to 1.5B parameters with LoRA, SQLite benchmarks in English; where FedAvg SFT is still improving fast (the 0.5B model) the gain is smaller. Stated once, in the limitations subsection.

## 4. What the section carries for other sections

Nothing.

## 5. Structure of the first draft (labels, floats, formulas)

Other sections and the generated tables refer to these labels. The macros and
citation keys each section used are in `inventory_v1.txt`.

### `sections/07_discussion.tex`

Headings and labels:

- `\section{Discussion and limitations}` `sec:discussion`
- `\subsection{Interpretation of the results}` `sec:interpretation`
- `\subsection{Scope and limitations}` `sec:limitations`

### `sections/08_conclusion.tex`

Headings and labels:

- `\section{Conclusion}` `sec:conclusion`
