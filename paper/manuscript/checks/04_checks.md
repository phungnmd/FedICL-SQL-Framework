# Checks: Section 4, Experimental setup, Appendices A and B

What stays true whatever the draft says: facts and the bounds of claims.
It is read before the section is written and when it is checked; remarks
on the wording of a draft are not kept here.

## 1. Facts about our work

- Questions that yield no pair. Two classes yield none in any round: questions on databases without rows, and questions whose gold SQL query fails or exceeds the time limit (Section 4.2 prints the two BIRD counts of gold SQL queries over the time limit, 87 and 92). Questions whose samples are all correct or all incorrect yield none in that round only; the two classes are not all the questions without pairs.
- Spider train, 8,659 questions: 1,759 on databases without rows, 3 with a failing gold SQL query; of the 6,900 on databases with rows, after 2 warm-up rounds 4,013 yield pairs, 2,327 have correct samples only and 557 have no correct sample.
- The Spider test-suite parser: the share of queries it cannot read was measured on BIRD dev (85%). BIRD train was not measured (its databases are not on the Mac); a count of queries with syntax outside the Spider grammar gives 2,319 of 9,428, a lower bound. "Most queries of BIRD train" is not supported; "many queries of BIRD" is. (open, A39)
- The generated suite of BIRD dev is described in Section S6 of the Supplementary Materials, and Section 4.1 points there in one sentence (owner, 2026-11-28). The suite and its agreement with the official suite on Spider dev are macros (`\fact{suite.*}`, from the two committed summaries): 100 variants of 11 databases; 1,452 of 1,534 questions with a variant that counts; on Spider dev 99.54% agreement over 29,986 predictions (29 files), 96.65% of the 2,267 official rejections rejected, 62 predictions rejected by ours only.
- SQL extraction, the same for evaluation and for the labels (`fedls_sql/prompts/builder.py`, `extract_sql`): cut at the first semicolon, body of a fenced block when there is one, text before the first SELECT dropped, a WITH clause kept; an output without SELECT is executed as it is.
- The server averages the two LoRA factors separately (`aggregate_round`, factor-wise FedAvg), not their product.
- Training details a reader needs to repeat the runs, for Section 4.5 or Appendix B: weights in bfloat16 on the GPU (`fedls_sql/models/student.py`); an update is the mean of 16 examples (SFT) or 16 pairs (preference rounds) through gradient accumulation, and the token mean of the NLL is taken per sequence (`lora_trainer.py`, `dpo.py`); the log-likelihoods of the reference model are computed by the training code on the same model class, not by the sampling engine, and LoRA dropout is 0 in a preference round, so $m_\theta = 0$ holds at the first update.
- The 350 BIRD training questions whose gold SQL query fails are the same in every run; the gold SQL queries over the time limit differ by run (30 under the pretrained model, 87 and 92 in the two preference rounds of the main row), since the limit is elapsed time.
- Time limit and the load of the machine (`fedls_sql/eval/sql_pool.py`, `sql_exec.CPU_SHARE` 0.8): a run that meets its budget on less than 0.8 of the elapsed time in CPU time is run once more alone; the labels of the main BIRD rounds were made under this rule (`LAB_LOG.md`, the table of second runs). One committed BIRD evaluation predates the rule (the row without training, 2026-11-19); the scoring of the generated suite ran every row again and reproduced each committed EX. Predictions that reach the limit at 4 rounds on BIRD dev: 2 for FedAvg SFT, 6 for the method; Spider test none (`\fact{timeouts.*}`).
- Databases are opened read-only (`mode=ro` and `PRAGMA query_only`, `sql_exec._connect`).
- The seven databases without rows are training databases of Spider (academic, geo, imdb, music_2, restaurants, scholar, yelp); no database of an evaluation set is without rows (all 206 databases of the Spider release and the 11 of BIRD dev counted on 2026-11-28).
- Agreement of the generated suite with the official one on Spider dev is stated among the predictions correct under EX (99.34% of 20,977), not over all predictions (99.54% of 29,986, which counts the predictions both suites reject because EX rejects them).
- IID setup: 146 databases over 5 clients, 29 to 30 each (Table 2): "an equal share", not "the same number".
- The seed determines the order of the training examples, the sampling, the initialization of the adapter and the pairing; Appendix B lists the four.
- Every federated row has T = 4. FedAvg SFT has a fifth round on Spider only, used in the comparison at more GPU time for the baseline; Section 4.4 says so, not Section 5.1.
- Settings that follow CodeLutra, named once, in the implementation subsection: number of samples, temperature, beta, learning rate, pairs per update, epochs, weight decay. Lambda is not in the list: the NLL term here is averaged over tokens. (owner, 2026-11-27)
- Four training settings of the preference rounds differ from those of the SFT rounds (learning rate, weight decay, learning-rate warm-up, LoRA dropout). The control row "FedAvg SFT, preference-round settings" (`fedavgp`) of Table 4 trains FedAvg SFT rounds 3 and 4 from round 2 at them; Section 4.4 names it (owner, 2026-11-28). Its 3-round rows are committed; 4 rounds waits.
- The times of Table 8 are totals of the clients run one after another on one card: GPU minutes (sampling, training, their total) and, apart, the minutes of the label step (elapsed time of SQL execution on 16 CPU threads, not CPU time).
- Appendix A prints the shortened prompt; Appendix B goes to the supplementary file first if the pages run over (owner, A8).
- Scope of model size: every experiment uses a model of 0.5B to 1.5B parameters (the main model `\setting{model.size}`; the others `\setting{models.other}`), with LoRA. No larger model is evaluated. The section states the range once.

## 2. Facts about cited papers

- NIID-Bench (`li2022niidbench`) is the source of the partition protocol (A10).
- The three sets built from Spider, from the abstracts (read 2026-11-28): Spider-Syn, "NL questions in Spider-Syn are modified from Spider, by replacing their schema-related words with manually selected synonyms" (https://arxiv.org/abs/2106.01065); Spider-Realistic, "based on Spider dev set with explicit mentions of column names removed" (https://arxiv.org/abs/2010.12773); Spider-DK, "NL questions in Spider-DK are selected from Spider, and we modify some samples by adding domain knowledge" (https://arxiv.org/abs/2109.05157). The abstracts of Spider-Syn and Spider-DK do not name the split.
- The number of variants of the generated suite (100) was chosen among 10, 20, 50 and 100 for the highest agreement with the official suite on the same Spider dev predictions (99.03, 99.33, 99.53, 99.54); Section S6.2 of the Supplementary Materials says so in one sentence (owner, 2026-11-28).
- CodeLutra constructs ten pairs per question; a fact of the cited paper, typed, not a setting macro. Section 4.5 names it beside the two pairs of the method (owner, 2026-11-27: moved from Section 3).
- CodeLutra, Eq. (3), writes the log-likelihood of the whole response. The paper says nothing about normalization by length, and its released code was not checked. "CodeLutra sums it" is our reading of the formula, not a statement of the paper; a sentence keeps to the formula (`REVIEW_NOTES.md`, A38).

## 3. Claims: strength, scope, what waits

- No FedProx SFT and no second training seed (owner, 2026-11-28); local SFT is a baseline on BIRD only. Sections 4.3 and 4.4 are read again when the rows of local SFT, centralized SFT on BIRD and FedDPO on Spider are committed (A9).
- Waiting for GPU rows in Appendix B: the settings of FedDPO, the epochs of local SFT.

## 4. What the section carries for other sections

- No research questions (`OUTLINE.md`); the section opens on its subject.
- Section 3.5 points to Section 4.1 for how the time limit of each benchmark applies to a sample and the gold SQL query, and Section 3.6 to Section 4.2 for the questions on databases without rows.
- "IID" and "non-IID" in full at first use, in Section 4.2.
- The statistical protocol (exact McNemar test, Holm correction within each table, a test printed in two tables counting in the first, what "significant" means) is defined here once; Sections 5 and 6 rely on it. There is no family of the text: a comparison that no table prints has no p and no significance word (owner, 2026-11-28).

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. `make inventory` lists the macros and
citation keys by section.

### `sections/04_setup.tex`

Headings and labels:

- `\section{Experimental setup}` `sec:setup`
- `\subsection{Datasets and metrics}` `sec:datasets`
- `\subsection{Federated setups}` `sec:fed-setups`
- `\subsection{Models and baselines}` `sec:models`, `sec:baselines`
- `\subsection{Implementation}` `sec:implementation`
- `\subsection{Statistical test}` `sec:stat-test`

Floats:

- table `tab:setups`, from `generated/tab_setups`
