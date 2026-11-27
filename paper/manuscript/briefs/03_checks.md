# Checks: Section 3, Method, Fig. 1, Algorithm 1

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0). Items marked "v1" come from the review
of the first drafts (tag `draft-v1-2026-11-27`); the limits that the
brief of this section still carries in its Ceiling column move into
part 3 when the brief is rewritten.

## 1. Facts about our work

- What leaves a client in a round: the adapter and one integer, its aggregation weight (the number of questions in a warm-up round, the number of pairs in a preference round), and nothing else. Samples, execution results, execution labels and preference pairs stay at the client. (v1 B3, B6; `CLAIMS.md`, contribution 2)
- The NLL term is averaged over the tokens of the correct sample. With the same lambda it weighs less against the preference term than a summed log-likelihood would, by a factor of the length of the sample. (v1 B2)
- An empty sample is an incorrect sample under the general rule; it needs no rule of its own in the text. (v1 B7)
- The reason for warm-up rounds, in counts: questions without a correct sample when the first preference round samples are, on BIRD, 4,035 of 9,428 with the pretrained model and 2,698 after 2 warm-up rounds. On Spider, of the questions on databases with rows: 1,016, then 557. "More questions yield pairs" holds on BIRD only (4,857 to 5,877); on Spider the questions that yield pairs fall (4,454 to 4,013). (v1 A1, B25)
- Two pairs per question: the reason given is that the number of pairs sets the length of local training; the paper has no ablation over M. (owner, 2026-11-26; v1 A5)
- Fig. 1 differs from the text in three places, not changed until the owner decides: "Only LoRA adapters travel" (the text: the adapter and one integer); step 4 writes L = L_DPO + L_NLL without lambda; "2 FedAvg rounds" and "N = 10" are typed in the figure. (v1 A4)

## 2. Facts about cited papers

- CodeLutra, Eq. (3), writes the log-likelihood of the whole response. The paper says nothing about normalization by length, and its released code was not checked. "CodeLutra sums it" is our reading of the formula, not a statement of the paper. (v1 B9)
- CodeLutra constructs ten pairs per question; a fact of the cited paper, typed, not a setting macro. (v1 B8)
- The NLL term of Pang et al. is also length-normalized (fact row K.1 of `02_related_rows.md`). (v1 E)
- OpenFedLLM on pairs and the reference model: as in `02_checks.md`.

## 3. Claims: strength, scope, what waits

- Credit (owner, 2026-11-27; `AGENTS.md`, "Credit"): the method is presented as ours; the section says what CodeLutra does and where ours differs (only a client can compute the labels; a federated round renews samples, labels and pairs, with its global model as the reference model of every client; warm-up rounds of FedAvg SFT come first). No sentence says that the contribution is to bring CodeLutra's loop into federated training, and the settings that follow CodeLutra are named in Section 4.5, not here.
- "First" and "to our knowledge" belong to Section 1.

## 4. What the section carries for other sections

- How a query is read from the output of the model and how execution results are compared is in Section 4, to which this section points.
- The time limit, the adapter configuration, the settings of local training and the replacement rule of pairing are in Appendix B.
- That a client must be able to execute SQL on its databases is said in Section 7 if not here.
