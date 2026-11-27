# Checks: Section 4, Experimental setup, Appendices A and B

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0). Items marked "v1" come from the review
of the first drafts (tag `draft-v1-2026-11-27`); the limits that the
brief of this section still carries in its Ceiling column move into
part 3 when the brief is rewritten.

## 1. Facts about our work

- Questions that yield no pair. Two classes yield none in any round: questions on databases without rows, and questions whose gold SQL query fails or exceeds the time limit (Section 4.2 prints the two BIRD counts of gold SQL queries over the time limit, 87 and 92). Questions whose samples are all correct or all incorrect yield none in that round only; the two classes are not all the questions without pairs. (v1 B11, B41)
- Spider train, 8,659 questions: 1,759 on databases without rows, 3 with a failing gold SQL query; of the 6,900 on databases with rows, after 2 warm-up rounds 4,013 yield pairs, 2,327 have correct samples only and 557 have no correct sample. (v1 B25)
- The Spider test-suite parser: the share of queries it cannot read was measured on BIRD dev (85%). BIRD train was not measured (its databases are not on the Mac); a count of queries with syntax outside the Spider grammar gives 2,319 of 9,428, a lower bound. "Most queries of BIRD train" is not supported; "many queries of BIRD" is. (v1 B12; open, A39)
- IID setup: 146 databases over 5 clients, 29 to 30 each (Table 2): "an equal share", not "the same number". (v1 B13)
- The seed determines the order of the training examples, the sampling, the initialization of the adapter and the pairing; Appendix B lists the four. (v1 B14)
- Every federated row has T = 4. FedAvg SFT has a fifth round on Spider only, used in the comparison at equal client time; Section 4.4 says so, not Section 5.1. (v1 B17)
- Settings that follow CodeLutra, named once, in the implementation subsection: number of samples, temperature, beta, learning rate, pairs per update, epochs, weight decay. Lambda is not in the list: the NLL term here is averaged over tokens. (owner, 2026-11-27; v1 B37)
- The optimizer of the preference rounds differs from that of the SFT rounds; no control row exists yet. (referee reports, v1 B41; open, A34)
- The times of Table 7 are totals of the clients run one after another on one card.
- Appendix A prints the shortened prompt; Appendix B goes to the supplementary file first if the pages run over (owner, A8).

## 2. Facts about cited papers

- NIID-Bench (`li2022niidbench`) is the source of the partition protocol (A10).

## 3. Claims: strength, scope, what waits

- Baselines not yet run and the second training seed are described as the plan has them; Sections 4.4 and 4.5 are read again when their rows are committed (A9).
- Waiting for GPU rows in Appendix B: settings of FedDPO, the coefficient of FedProx, the epochs of Local SFT, the second training seed.

## 4. What the section carries for other sections

- The four research questions stand in the opening paragraph (A7).
- "IID" and "non-IID" in full at first use, in Section 4.2.
- The statistical protocol (exact McNemar test, Holm correction, what "significant" means) is defined here once; Sections 5 to 7 rely on it.
