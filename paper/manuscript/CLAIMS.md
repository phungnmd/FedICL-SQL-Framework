# FedExec-SQL: what the paper claims

Approved by the owner on 2026-11-26, with the decisions of section 7.
A section states a claim at the strength its row carries, in its own
words, not above it and not below it (owner, 2026-11-27). The Ceiling
column gives the strongest wording the evidence carries; the facts
behind it are in the checks file of the section
(`checks/NN_checks.md`). Values are those of
`generated/numbers.md` (one training seed); a claim whose rows are not
committed is marked "waits" and gets its values when the rows are in.

## 1. Thesis

In federated Text-to-SQL a client holds two things, questions with gold
SQL and the databases to run SQL on; FedAvg SFT learns from the first
alone, and FedExec-SQL also learns from the second, by running the model's
own queries at the client and training on which of them return the gold
result.

## 2. Contributions

1. A source of supervision. The paper points out that a client's
   databases are supervision that federated fine-tuning leaves unused:
   execution turns the one gold SQL of a question into many right and
   wrong queries of the model's own, and this can be done only at the
   client. To our knowledge it is the first federated Text-to-SQL
   training method that uses it.
2. The framework (owner, 2026-11-27: the paper names FedExec-SQL a
   framework where it introduces it; the method and its default
   configuration are unchanged). FedExec-SQL: warm-up rounds of FedAvg SFT, then preference
   rounds in which each client samples queries from the current global
   model, labels them by execution, pairs right with wrong ones and
   trains with a DPO term plus an NLL term. A federated round is one
   re-sampling step, and the round's global model is the reference of
   the DPO term. Only the adapter and the count that weights it (the
   number of pairs) leave a client, as the adapter and the number of
   questions do in FedAvg SFT. The introduction states it as the
   federated design (owner, 2026-11-28): the preference rounds start from FedAvg
   SFT warm-up rounds, a communication round is one step of sampling,
   labeling and training for all clients, the global model of the round
   is their common reference model, and only the LoRA adapter and its
   integer weight leave a client. It does not claim the renewal of pairs
   and reference as a design of its own, and does not say or imply that
   parts come from another paper.
3. The evidence. On BIRD dev and Spider test, at the same number of
   rounds, the model is 6.19 and 3.49 EX points above FedAvg SFT, and
   further FedAvg SFT rounds do not close the gap; on BIRD dev it is
   3.26 above FedDPO trained on the same first pairs (Spider waits). On
   Spider test it is also 3.17 above centralized SFT on the pooled data
   of the clients (A5; owner, 2026-11-28: in the Introduction, contribution 3
   reads "We show that it is above FedAvg SFT and FedDPO at the same
   number of rounds and, on Spider test, above centralized SFT on the
   pooled data of the clients; ..."). The paper shows where
   the gain comes from (execution errors fall by half; more answers are
   right with other tables or columns than the gold SQL's), what each
   part adds, and what a client pays in compute.
4. The release: code, client splits, and the predictions of every row.

## 3. Claims

Macro arguments are `{set}{line}{round}`; lines: `fedavg` FedAvg SFT,
`k2` the method, `fedavgp` FedAvg SFT rounds 3 and 4 continued from
FedAvg SFT round 2 at the four training settings of the preference
rounds (the control; owner, 2026-11-28), `fixed` pairs and reference of
the first preference round, `rft` without the preference term, `feddpo`
federated DPO as published (no NLL term, the pairs and reference of the
first preference round, which are the method's: at 3 rounds it is the
method without the NLL term), `k0` and `k3` no and three warm-up rounds.
p is the exact McNemar p and padj its Holm-adjusted value in the table
that prints the test. Owner, 2026-11-28: the paper prints a p only in a
table and uses "significant" only for a test that a table of the paper
or of the Supplementary Materials prints; a comparison that no table
prints is stated in points and counts, and the generator gives it no p
(the family of the text is gone). Section numbers are those of the
paper (5.4 holds the other models, setups and perturbed questions, 5.5
the cost). Table numbers of the paper are those of `OUTLINE.md`: the
PDF prints each one lower (Table 3 here is Table 2 in the PDF), since
the table of setups is Table S3. In the Supplementary Materials: Table
S4 EX by round, Table S5 TS on BIRD dev, Table S6 the form of the
correct predictions (owner, 2026-11-28), Table S7 the labels at each
client (owner, 2026-11-28).

### A. Against FedAvg SFT (Section 5.1; Table 3, Fig. 3)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| A1 | At 4 rounds the method is above FedAvg SFT | BIRD dev `\ex{bird}{k2}{4}` 48.76 against `\ex{bird}{fedavg}{4}` 42.57: `\gain{bird}{fedavg}{4}{k2}{4}` +6.19, `\nfix` 153 questions against `\nbrk` 58, `\pval` 4.6e-11, `\padj` 2.3e-10 in Table 3 (7 tests since the row of A5, owner, 2026-11-28). Spider test 78.20 against 74.71: `\gain{spider}{fedavg}{4}{k2}{4}` +3.49, p 6.4e-7, padj 2.6e-6 | BIRD dev, Spider test | "above FedAvg SFT at the same number of rounds on both datasets", significant after correction. The headline number is the BIRD gain |
| A2 | More FedAvg SFT rounds do not reach it | BIRD: FedAvg SFT is highest at round 3 (43.68); the method is `\gap{bird}{fedavg}{3}{k2}{4}` 5.08 above that (padj 1.9e-7, Table S4). Spider: FedAvg SFT is 74.71 at rounds 3 and 4 and 73.92 at round 5; the method is `\gap{spider}{fedavg}{5}{k2}{4}` 4.28 above round 5 (padj 1.2e-8, Table S4). Owner, 2026-11-28: Table S4 prints these tests (A2 is a main claim) | BIRD dev (4 rounds), Spider test (5 rounds) | "FedAvg SFT does not improve after round 3 on both datasets"; the method is significantly above its best round (Table S4). Its falls (BIRD round 4 -1.11, Spider round 5 -0.79) are tested in no table and are not stated: not "degrades", not "has converged" |
| A3 | The gain is on every difficulty level | BIRD simple / moderate / challenging `\lvl{bird}{k2}{4}{...}` 56.00 / 39.66 / 31.72 against 51.35 / 29.96 / 26.90. Spider easy / medium / hard / extra 91.91 / 81.91 / 71.06 / 60.50 against 90.64 / 78.18 / 66.74 / 55.74 | BIRD dev, Spider test | "higher on every level; largest on the moderate questions of BIRD and the extra-hard of Spider." No test per level |
| A4 | One preference round adds more than a further SFT round from the same model | From FedAvg SFT round 2: BIRD `\gap{bird}{fedavg}{2}{k2}{3}` 3.52 against `\gap{bird}{fedavg}{2}{fedavg}{3}` 0.98; Spider 3.36 against 0.61 (points, no test: owner, 2026-11-28). The two models at 3 rounds, tested directly in the block of 3 rounds of Table 4 (FedAvg SFT row, owner, 2026-11-28): BIRD `\gap{bird}{fedavg}{3}{k2}{3}` 2.54, `\padj` 0.044; Spider 2.75, `\padj` 5.7e-4 (owner, 2026-11-28, fourth revision: with the warm-up rows out of Table 4 its family has 12 tests, and the BIRD test crosses 0.05 from 0.061; when the four rows that wait enter the family, it can cross back, since its raw p 0.0087 is the eighth of the family) | BIRD dev, Spider test | "adds more than one further round of FedAvg SFT" in points (Fig. 3); after three rounds the gap on each benchmark is given in points beside the two steps, with no significance word for BIRD (the test is in Table 4; its adjusted p moves with the family) |
| A5 | Above centralized SFT on the pooled data of the clients: a headline claim (owner, 2026-11-28, third revision) | Spider test: the method `\ex{spider}{k2}{4}` 78.20 against centralized SFT (3 epochs on the union of the clients' data) `\ex{spider}{central}{3}` 75.03, `\gap{spider}{central}{3}{k2}{4}` 3.17 (`\nfix` 161 questions against `\nbrk` 93, `\pval` 2.4e-5, `\padj{spider}{central}{3}{k2}{4}` 7.1e-5 in Table 3, the row "the method against centralized SFT" of each block); centralized SFT is level with FedAvg SFT (+0.32, padj 0.69, Table 3). BIRD: the centralized SFT row is queued; its note row prints `--`. Place: the abstract (one clause), the results paragraph of the Introduction, contribution 3, its own sentence in Section 5.1, and the Discussion, where it supports the reading of the training signal | Spider test; BIRD waits | "On Spider test, significantly above centralized SFT, which does not differ significantly from FedAvg SFT." May read it as: training on execution at the clients gives more than pooling their gold SQL queries, on Spider test. Nothing for BIRD until its row is committed; the sentences are written so that the BIRD figure joins them. Not "federated training beats centralized training" in general: the centralized row is SFT on gold SQL, not the method run on pooled data (that is B7) |
| A6 | Against FedDPO (federated DPO as published), and against local SFT on BIRD | FedDPO trains on the method's first preference pairs (the same samples, labels, start and $M$), with the pairs and reference of that round fixed and no NLL term. BIRD at 4 rounds: `\ex{bird}{feddpo}{4}` 45.50 against 48.76, `\gap{bird}{k2}{4}{feddpo}{4}` 3.26 (`\nfix{bird}{k2}{4}{feddpo}{4}` 59 questions against `\nbrk` 109, `\pval` 1.4e-4, `\padj` 0.0013 in Table 4, where FedDPO is a row of the block of 4 rounds; owner, 2026-11-28); test-suite accuracy `\ts{bird}{feddpo}{4}` 37.61 against 41.59, `\tsgap{bird}{k2}{4}{feddpo}{4}` 3.98 (`\tspadj` 4.1e-5 in Table S5). At 3 rounds `\ex{bird}{feddpo}{3}` 44.98, 1.24 below the method (padj 0.33, Table 4). The second round adds `\gap{bird}{feddpo}{3}{feddpo}{4}` 0.52 to FedDPO, 2.54 to the method (points). Against FedAvg SFT at 4 rounds, FedDPO is `\gap{bird}{fedavg}{4}{feddpo}{4}` 2.93 above under EX (padj 0.014 in Table 3) and `\tsgap{bird}{fedavg}{4}{feddpo}{4}` 0.91 above under test-suite accuracy (points; no table prints this test). Notes only: 121 of its EX-correct predictions fail the suite, against 110 for the method and 90 for FedAvg SFT. Local SFT on BIRD waits. FedProx SFT and local SFT on Spider are not run (owner, 2026-11-28) | FedDPO: BIRD dev; Spider test waits (`feddpo/round_2`). Local SFT: BIRD dev, waits | "Above FedDPO at 4 rounds on BIRD, under EX and under test-suite accuracy", significant after correction (Table 4, Table S5). At 3 rounds "the difference is not significant". The baseline is always named with its pairs: FedDPO's protocol on the method's own first execution-labeled pairs, not on external pairs. FedDPO's gain over FedAvg SFT is stated under EX with its test-suite difference beside it in points; never "FedDPO is above FedAvg SFT" alone. No sentence on local SFT until its rows are in |

### B. The parts (Section 5.3; Table 4)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| B1 | Pairs sampled again each round, with the round's global model as reference, are better than the pairs and reference of the first preference round | BIRD at 4 rounds: `\ex{bird}{fixed}{4}` 46.15, `\gap{bird}{k2}{4}{fixed}{4}` 2.61, p 5.7e-4, padj 0.0046 (Table 4). Spider test: 78.02 against 78.20, padj 0.78 | BIRD dev | Stated for BIRD. Never "on both datasets", never "essential". On Spider test "the difference is not significant" |
| B2 | The second preference round still adds | BIRD `\gap{bird}{k2}{3}{k2}{4}` 2.54 (padj 4.1e-4, Table S4); Spider 0.74 (padj 0.093, Table S4) | BIRD dev | "significantly on BIRD dev only" (Table S4) |
| B3 | The NLL term is needed on Spider; on BIRD its effect is not separated | Spider at 3 rounds: without it `\ex{spider}{feddpo}{3}` 73.59, `\gap{spider}{k2}{3}{feddpo}{3}` 3.87 below (padj 9.2e-8, Table 4), and below the model it started from (74.10; no test). BIRD at 3 rounds, the same start and pairs: without it `\ex{bird}{feddpo}{3}` 44.98, 1.24 below (padj 0.33 in Table 4), test-suite accuracy 0.13 below (padj 0.94 in Table S5); the round without it still rises over its start, `\gap{bird}{fedavg}{2}{feddpo}{3}` 2.28 (points). With the pairs and reference of the first round at 4 rounds the term adds `\gain{bird}{feddpo}{4}{fixed}{4}` +0.65 (points; the rows FedDPO and "Fixed pairs and reference" of Table 4). Notes only: more execution errors without it on BIRD (133 against 102) and more outputs cut at the token limit (19 against 11). The row without the NLL term at 4 rounds with pairs sampled again (`nonll`) is not in the paper (owner, 2026-11-28) | Spider test, one preference round; BIRD dev, one preference round | "Without the NLL term the preference round lowers accuracy" on Spider, significantly. On BIRD: "does not differ significantly", and the round without it is not below its start. Never "needed on both datasets" |
| B4 | The preference term removes execution errors that training on the model's correct samples alone leaves, and on BIRD at 4 rounds it raises accuracy | At 4 rounds on BIRD, without it (samples drawn again from its own round 1): `\ex{bird}{rft}{4}` 45.24, `\gap{bird}{k2}{4}{rft}{4}` 3.52 below (`\pval` 5.2e-5, `\padj` 5.7e-4 in Table 4); the row without the term is itself `\gap{bird}{fedavg}{4}{rft}{4}` 2.67 above FedAvg SFT (points), so a part of the gain over FedAvg SFT comes from training on the samples that execution labels correct; test-suite accuracy 3.39 below (`\tspadj` 4.5e-4 in Table S5); execution errors `\nerr{bird}{rft}{4}` 228 against 128; incorrect results 612 against 658, more with the method. At 3 rounds, without it: BIRD `\nerr{bird}{rft}{3}` 248 execution errors against `\nerr{bird}{k2}{3}` 102, EX 1.83 lower (padj 0.17); Spider 153 against 99, EX 1.59 lower (padj 0.061). Owner, 2026-11-28: the tests on execution errors and on incorrect results are printed in no table and leave the paper; the counts stay. Notes only: BIRD at 3 rounds p 1.1e-24 (errors) and 1.0e-12 (incorrect results, more with the method); at 4 rounds 1.6e-14 and 0.0028; Spider at 3 rounds 4.2e-6 and 0.13 | BIRD dev at 3 and 4 rounds, Spider test at 3 rounds. The row at 4 rounds on Spider is not run (owner, 2026-11-28) | The error counts carry the claim at 3 rounds, stated as counts; for EX there "does not differ significantly on either benchmark". At 4 rounds on BIRD: "3.52 lower without it, significant after correction" (Table 4; under test-suite accuracy in Table S5), and the method has more incorrect results than the row without the term (658 against 612), said beside the error counts, without a significance word |
| B5 | Warm-up rounds make the gain hold under test-suite accuracy | The number of warm-up rounds is a setting, not a row of Table 4 (owner, 2026-11-28, fourth revision): Section 5.4 gives in one sentence the Spider test EX at 4 rounds with 0, 2 and 3 warm-up rounds, `\ex{spider}{k0}{4}` 78.02, `\ex{spider}{k2}{4}` 78.20, `\ex{spider}{k3}{4}` 77.97, against FedAvg SFT 74.71 (the gain over FedAvg SFT is there for each value; no test printed, no significance word), then the finding under test-suite accuracy below. Test-suite accuracy at 4 rounds (Table 7), no warm-up `\ts{...}{k0}{4}` / two warm-up rounds `\ts{...}{k2}{4}` / FedAvg SFT: Spider dev 67.21 / 70.41 / 67.99; Spider-Syn 51.35 / 55.51 / 51.84; Spider-Realistic 57.09 / 62.20 / 58.86. The method against itself without warm-up, `\tsgain{...}{k0}{4}{k2}{4}`: +3.20 (p 0.010), +4.16 (p 0.0014), +5.11 (p 0.0067) | Spider dev, Syn, Realistic. The rows without and with three warm-up rounds on BIRD are not run (owner, 2026-11-28) | No claim that warm-up raises EX: on these sets EX is level with and without it, and on Spider-DK, which has no test suite, EX is higher without it (67.10 against 63.55, p 0.032, printed in Table 7). "Without warm-up the method's EX gain does not carry over to test-suite accuracy; with two warm-up rounds it does." After correction the difference is significant on Spider-Syn |
| B6 | The weights of the server average do not matter | One sentence, no rows (owner, 2026-11-28): weights by questions or equal instead of by pairs move EX after one preference round by at most `\fact{weights.bird.ex_max}` 0.20 on BIRD and `\fact{weights.spider.ex_max}` 0.52 on Spider | BIRD dev, Spider test, at 3 rounds | one sentence, in points |
| B7 | Clients pooled in the preference rounds | Back in Table 4 (owner, 2026-11-28, third revision), Spider test only, 4-round block: the two preference rounds of the method on the union of the clients' data, without aggregation (line `pooled`, rounds 3 and 4). Waits: the row is queued again and prints `--`; its test will join the family of Table 4. Section 5.3 says in one sentence what the row is, and nothing on its outcome until the row is committed | Spider test | waits |
| B8 | For the questions without a correct sample, pairs of the gold SQL with an incorrect sample inside the preference round do not help | Not in the paper (owner, 2026-11-28: a variant outside the method, with a negative result); notes only. BIRD dev, without warm-up rounds, one preference round on the same samples and labels; the variant adds $M$ = 2 such pairs for each of the 4,035 questions without a correct sample: 39.24 against 41.85, -2.61, p 0.0073; execution errors 219 to 105, incorrect results 673 to 827. Spider: its run changed three things at once (76.67 against 75.87 at round 1, p 0.21, lower at round 2; `LAB_LOG.md`, 2026-11-21) | BIRD dev, from the pretrained model, one round | |
| B9 | The training settings of the preference rounds do not account for the gain (owner, 2026-11-28) | FedAvg SFT rounds 3 and 4 from FedAvg SFT round 2 at the learning rate, weight decay, learning-rate warm-up and LoRA dropout of the preference rounds (`fedavgp`, "FedAvg SFT, preference-round settings" in Table 4). At 3 rounds: BIRD `\ex{bird}{fedavgp}{3}` 43.16, `\gap{bird}{fedavg}{3}{fedavgp}{3}` 0.52 below FedAvg SFT (38 questions against 46; Spider 75.45, 0.74 above it, 51 against 35. No table prints these tests and the generator gives them no p; notes only, the exact McNemar p from these counts is 0.45 and 0.11). The method is above the control: BIRD `\gap{bird}{k2}{3}{fedavgp}{3}` 3.06 (128 against 81, `\padj{bird}{k2}{3}{fedavgp}{3}` 0.0098 in Table 4), Spider 2.01 (126 against 83, padj 0.021). At 4 rounds: waits (`\ex{bird}{fedavgp}{4}`, `\ex{spider}{fedavgp}{4}` print the placeholder); when its two tests at 4 rounds and FedDPO on Spider enter the family of Table 4 (12 to 16 tests with the pooled row of B7), the padj at 3 rounds change (the Spider value, 0.021, is the nearer to the level) | BIRD dev, Spider test, at 3 rounds; 4 rounds waits | At 3 rounds the control does not differ significantly from FedAvg SFT on either benchmark and the method is above it on both. The paper states the difference from FedAvg SFT in points (0.52 below, 0.74 above), since no table prints that test, and the method "significantly above it on both benchmarks" (Table 4). Nothing on 4 rounds until the rows are in |

### C. What changes in the answers (Section 5.2; Fig. 4)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| C1 | The preference rounds halve the execution errors | At 4 rounds, FedAvg SFT against the method: BIRD `\nerr{bird}{fedavg}{4}` 268 against `\nerr{bird}{k2}{4}` 128; Spider 173 against 84. Owner, 2026-11-28: the exact test on the execution errors is printed in no table and leaves the paper; notes only: BIRD p 5.8e-22 (182 questions fail only with FedAvg SFT, 42 only with the method), Spider 6.2e-14 (118 and 29) | BIRD dev, Spider test | "about half as many execution errors", in counts, without a significance word |
| C2 | Queries that run and return a wrong result do not become fewer (stated in Section 5.2 only, with Fig. 4: not in the abstract, the introduction, the Discussion or the conclusion; owner, 2026-11-28) | BIRD `\nwr{bird}{fedavg}{4}` 613 against `\nwr{bird}{k2}{4}` 658; Spider 370 against 384. Notes only (no table prints the test, owner, 2026-11-28): BIRD p 0.007 (156 questions only with the method, 111 only with FedAvg SFT); Spider 0.37 (111 and 97) | BIRD dev, Spider test | "incorrect results do not fall", with the counts. Never "fewer wrong results than FedAvg SFT". Inside the method the second preference round lowers them on BIRD (723 to 658) |
| C3 | The method finds right answers that are not written like the gold SQL, and FedAvg SFT does not; on BIRD this holds under test-suite accuracy (owner, 2026-11-27) | Right answers that read other tables or columns than the gold SQL, under EX: BIRD, FedAvg SFT 136, 135, 136 at rounds 2, 3, 4, the method 174 at round 3 and 191 at round 4; Spider test at 4 rounds 83 against 103 (83 without training). Right answers on the gold SQL's tables and columns at 4 rounds: BIRD 517 against 557, Spider 1,521 against 1,576. The same answers that are also correct under the generated test suite of BIRD dev (C4): other tables or columns, FedAvg SFT 84, 81, 86 at rounds 2, 3, 4, the method 117 at round 3 and `\fact{form.bird.k2.4.other_right_ts}` 132 at round 4; the gold SQL's tables and columns at 4 rounds 477 against 506. The suite rejects `\fact{form.bird.k2.4.other_ts_fail_pct}` 30.9% of the method's right answers on other tables or columns and 36.8% of those of FedAvg SFT, against `\fact{form.bird.k2.4.gold_ts_fail_pct}` 9.2% and 7.7% of those on the gold SQL's (without training 33.6% and 11.1%). Place and size (owner, 2026-11-28, fourth revision): the Supplementary Materials only, Section S6.4 with Table S6 (the counts at 4 rounds under EX and the suite, the Spider count, the counts by round and the shares the suite rejects); no sentence in Section 5.2 | BIRD dev (EX and the generated suite), Spider test (EX; it has no test suite) | Macros `\fact{form.<set>.<line>.<round>.other_right}` and `.gold_right` (with `.other`, `.gold` for the group sizes), and on BIRD `.other_right_ts`, `.gold_right_ts`, `.other_ts_fail_pct`, `.gold_ts_fail_pct`, from the committed predictions and test-suite scores. On BIRD 55 of the 95 questions of net gain under EX and 46 of the 75 under the suite, on Spider 20 of 75: "a large part of the gain on BIRD, under EX and under test-suite accuracy", never "the gain sits there". Where the paper gives the EX count of these answers on BIRD it gives the test-suite count beside it. May say that a right answer on other tables or columns fails the suite more often than one on the gold SQL's (about a third against about a tenth). No claim that the method's fail less often than those of FedAvg SFT (30.9% against 36.8%, no test). A prediction that does not parse counts with the others |
| C4 | The gain on BIRD dev holds under test-suite accuracy (owner, 2026-11-27) | BIRD has no official test suite; a suite of 100 variants of each database was generated (`LAB_LOG.md`, 2026-11-27). `\ts{bird}{fedavg}{4}` 36.70 against `\ts{bird}{k2}{4}` 41.59: `\tsgap{bird}{fedavg}{4}{k2}{4}` 4.89 (131 questions against 56, `\tspval` 4.2e-8, `\tspadj` 2.9e-7), against 6.19 under EX. Predictions correct under EX that the suite rejects: 90 for FedAvg SFT, 110 for the method. Place and size (owner, 2026-11-28): one sentence in Section 5.1, with FedDPO beside it; the test in Table S5 of the Supplementary Materials, which gives TS on BIRD dev for the BIRD rows of Table 4 and forms its own Holm family (7 tests with the rows committed on 2026-11-28); the description of the suite and its agreement with the official one on Spider dev in Section S6; Section 4.1 keeps one sentence that points there | BIRD dev | "4.89 points above FedAvg SFT under the generated suite", significant (Table S5). Not "robust", and no claim for Spider test, which has no suite. The suite is ours: the Supplementary Materials say how it was generated and how far it agrees with the official suite on Spider dev (`\fact{suite.calib.agreement_ex_correct}` 99.34% of the `\fact{suite.calib.ex_correct}` 20,977 predictions correct under EX, at 100 variants; 99.54% over all 29,986 is not the figure to print) |
| C5 | Where the removed execution errors go (main session, 2026-11-28) | Outcome of each question with FedAvg SFT and with the method at 4 rounds, `\fact{moved.<set>.<with FedAvg SFT>.<with the method>}`. BIRD dev: of the 268 execution errors of FedAvg SFT, 75 become correct, 107 run and return an incorrect result, 86 stay; Spider test: of 173, 67 become correct, 51 return an incorrect result, 55 stay. Notes only: of the 153 questions only the method answers correctly on BIRD, 75 were execution errors and 78 incorrect results; on Spider of 150, 67 and 83. Place and size (owner, 2026-11-28): one sentence in Section 5.2 | BIRD dev, Spider test | Counts, no causal word: "of the execution errors of FedAvg SFT, N are answered correctly by the method and M execute and return an incorrect result". It reads C1 and C2 together and is no claim of its own on accuracy |
| C6 | The change holds at every client (owner, 2026-11-28) | On the samples of the labeling step, which each client draws for its own training questions (`audits/protocol_v2/<root>/<arm>/round_<r>/client_<c>_pairs_stats.json`; `samples_correct` and `samples_exec_error` over `samples`). From the samples drawn from the FedAvg SFT model after the warm-up rounds (`dpo/round_1`) to those drawn after one preference round (`dpo/round_2`), the share of correct samples rises at each client by `\fact{clients.bird.correct_gain_min}` 18.0 to `\fact{clients.bird.correct_gain_max}` 22.9 points on BIRD (clients 1 to 5: 37.9, 29.2, 33.5, 30.0, 31.3 to 59.0, 47.9, 56.4, 48.0, 51.8) and 10.5 to 13.8 on Spider (74.5, 75.2, 67.9, 71.0, 71.5 to 85.0, 85.9, 81.7, 84.4, 84.4); the share of execution errors falls by `\fact{clients.bird.error_fall_min}` 23.5 to 29.4 points on BIRD (31.1, 37.4, 36.8, 38.4, 29.8 to 6.3, 10.0, 8.2, 9.0, 6.3) and 7.5 to 12.3 on Spider (12.7, 11.0, 14.1, 18.9, 13.7 to 4.3, 3.5, 4.3, 6.6, 5.6). On BIRD, after one round without the preference term (`rft/round_2`, whose round 1 has the same samples): correct 47.7, 38.0, 43.4, 38.8, 40.1, a rise of `\fact{clients.bird.rft.correct_gain_min}` 8.8 to 9.9; execution errors 20.0, 27.1, 25.7, 26.2, 20.1, a fall of 9.7 to 12.2. The ranges are taken from the shares as Table S7 prints them; the generator stops if a client does not rise, does not fall, or gains less with the preference term than without it. Spider has no committed `rft/round_2`, and its cells stay blank. Place: three sentences in Section 5.2 and Table S7 (Section S7 of the Supplementary Materials) | BIRD train and Spider train, the clients of the two main setups, at the first preference round | "at every client", on the clients' training questions, stated as a measure of the labeling step, not as EX. No test, so no significance word. Not "the gain is the same at every client", and nothing about evaluation EX per client. The cosine of the client updates and the share of questions without a correct sample are not printed |
| C7 | What execution can label differs by client (owner, 2026-11-28, third revision) | From the samples of the first preference round on Spider train (`fedpref_sftr2_ddlrows_alpha01_s0/dpo/round_1/client_<c>_pairs_stats.json`): client 4 has `\fact{clients.spider.4.no_rows}` 1,648 of its `\fact{clients.spider.4.questions}` 3,479 training questions on databases without rows; of its `\fact{clients.spider.4.mixed}` 2,276 questions with correct and incorrect samples, `\fact{clients.spider.4.mixed_no_rows}` 1,098 are on such databases and give no pair, so `\fact{clients.spider.4.paired}` 1,178 yield pairs. Client 3 has `\fact{clients.spider.3.no_rows}` 111 such questions (81 of its 1,205 mixed ones), and the other `\fact{clients.spider.no_rows_none}` 3 clients none; no client of BIRD train has any (the generator stops if one has). Place: two sentences in Section 5.2 after C6 | Spider train, BIRD train, first preference round | Stated as counts and as what it means for the method: a client contributes pairs where execution informs, and its weight in the server average, its pair count, reflects this. Section 3 states that a question on a database without rows gives no pair. No claim on accuracy per client |

### D. Breadth (Section 5.4; Tables 5, 6, 7)

| # | Claim | Values and macros | Holds on | Ceiling |
|---|---|---|---|---|
| D1 | A smaller model | Qwen2.5-Coder-0.5B: `\ex[qwen05]{spider}{k2}{4}` 66.19 against 64.09, `\gain[qwen05]{spider}{fedavg}{4}{k2}{4}` +2.10, padj 0.0056 (Table 5) | Spider test | "also above FedAvg SFT, by a smaller margin", significant |
| D2 | A model of another family (DeepSeek-Coder-1.3B) | waits (Spider rounds). Not run on BIRD (owner, 2026-11-28): Table 5 is a Spider table (writer's choice, 2026-11-28: its BIRD block would hold one row that repeats Table 3) | Spider test | |
| D3 | Other federated setups (IID, alpha 0.5 with 5 and with 10 clients) | waits | | until then the paper has two setups, both at alpha 0.1 with 5 clients |
| D4 | The gain holds on perturbed questions and under test-suite accuracy | EX gain at 4 rounds: Spider dev `\gain{spiderdev}{fedavg}{4}{k2}{4}` +2.51 (p 0.021), Syn +3.87 (p 6.3e-4), Realistic +2.75 (p 0.10), DK +3.92 (p 0.017). Test-suite accuracy: dev `\tsgain{spiderdev}{fedavg}{4}{k2}{4}` +2.42 (p 0.027), Syn +3.67 (p 4.2e-4), Realistic +3.34 (p 0.036) | Spider dev, Syn, Realistic, DK | "Above FedAvg SFT on all four sets and under both metrics"; significant after correction on Spider-Syn only. Not "robust": both models lose about 15 points from Spider dev to Spider-Syn |

### E. Cost (Section 5.5; Table 8)

| # | Claim | Values and macros | Ceiling |
|---|---|---|---|
| E1 | No added communication | The same adapter in every round of either kind: `\fact{cost.bird.adapter_mb}` 73.9 MB per client per round. Samples, labels and pairs stay at the client | as stated |
| E2 | The cost is client compute, printed as GPU time and label time apart (owner, 2026-11-27) | Minutes for the five clients of a round on one RTX A5000. GPU time is sampling and training. BIRD: a FedAvg SFT round `\fact{cost.bird.sft.train_min}` 173; the preference rounds 28 + 282 = `\fact{cost.bird.pref1.gpu_min}` 310 and 28 + 195 = 223, `\fact{cost.bird.pref1.gpu_ratio}` 1.8 and 1.3 times an SFT round. Spider: 124; 18 + 183 = 201 and 18 + 88 = 106, 1.6 and 0.9 times. The label step is SQL executed on the CPU; its figure is the elapsed time of the step on `\setting{pref.label_threads}` 16 threads, not CPU time: `\fact{cost.bird.pref1.label_min}` 159 and 168 min on BIRD, 3 and 3 on Spider. Over the four rounds the method takes 879 GPU minutes on BIRD against 692 for FedAvg SFT (5 SFT rounds: 865), and 555 against 496 on Spider (5 SFT rounds: 620). Pairs fall from the first preference round to the second (BIRD 11,754 to 7,066; Spider 8,026 to 3,354) | "A preference round takes 1.3 to 1.8 times the GPU time of an SFT round on BIRD and 0.9 to 1.6 times on Spider; executing the sampled queries on 16 CPU threads adds 159 and 168 minutes on BIRD and 3 on Spider." No figure adds the label step to the GPU time, and none is called "client time". The times are the five clients one after another on one card, not the wall-clock time of a federation. The rows are compared at equal rounds, that is, equal communication; A2 is the answer to "FedAvg SFT with more rounds", and on Spider the fifth FedAvg SFT round is a comparison at more GPU time for the baseline |

## 4. Wording that has to survive revision

Owner, 2026-11-28: the paper presents what supports the method; finding
weaknesses is the reviewer's work. Everything it prints stays true, no
number changes, and no claim goes above its ceiling (the "never"
wordings below and in section 3 still hold). A caveat, a non-significant
side result, an untested reading or an unfavourable number from outside
is printed only where a claim would be false or would mislead without
it. Where a Ceiling of section 3 says that such a result is "said
beside" a claim, it now stays in the tables and the notes: the 3-round
EX tests of A4 on BIRD, A6 and B4, the Spider rows of B1 and B2, B3 on
BIRD and the +0.65 of the NLL term with fixed pairs, the incorrect
results of B4, "by a smaller margin" of D1, the fall from Spider dev to
Spider-Syn of D4, the Spider-DK row of B5, and C2 outside Section 5.2.

1. The label needs the gold SQL: a sampled query is correct when its
   result equals the result of the gold SQL on the client's database.
   Never "without gold SQL", "unlabelled", "self-supervised", or
   "execution shows whether an answer is right".
2. One training seed. Significance is the exact McNemar test on paired
   predictions with Holm correction inside each table. The paper has no
   second-seed rows (owner, 2026-11-28): a second seed is ready if a
   reviewer asks, and Section 6 states one run as a limitation.
3. BIRD numbers are on BIRD dev; its test set is not public. No number
   is called held-out, on either dataset.
4. B1 and B2 are stated for BIRD.
5. No EX gain is claimed for the warm-up rounds, and none for the
   weights of the average.
6. C2: wrong results do not fall against FedAvg SFT.
7. "To our knowledge" on the first contribution, and its scope is
   federated training for Text-to-SQL. FL4SP is the earlier federated
   Text-to-SQL work (SFT). Verifier-driven federated training exists
   for math and code, federated DPO on fixed preference datasets
   (OpenFedLLM),
   and the same sample, label and DPO + NLL loop centrally (CodeLutra):
   the paper says so once, in the text of Section 2.2, cites CodeLutra
   at the objective in the Method section, and names in the
   implementation subsection (4.4 in the PDF) the settings of the
   preference rounds that follow it. The paragraph of Section 2.2 credits
   it without a step-by-step account (owner, 2026-11-28, third revision): it
   is named the closest work and cited; one sentence says what it does
   (at one site, execution-labeled samples of the current model, a DPO
   term and a likelihood term, several iterations) with its reported
   finding on the likelihood term, which the paragraph before needs; one
   sentence states the method in federated terms (labels at each client
   on databases the server never sees, a communication round as one
   iteration for all clients with the global model as common reference,
   the server average by pair counts, the start from FedAvg SFT warm-up
   rounds). Its sample count, its reference model, the renewal at every
   iteration and the small differences (pairs per question, the token
   mean of the NLL) are not printed there, and Section 2.2 no longer
   points to Section 4.4. Table 1 lists federated methods
   only (Zhang et al., FedDPO, PubSwap, Fed-GRPO and the method) and
   stands in Section 2.3 (owner, 2026-11-28); Liu et al., ExCoT and CodeLutra
   are described in the text of Section 2.2 and are not rows of it. No other section
   compares the method with CodeLutra: its novelty is stated against
   FedAvg SFT and federated DPO as published, and the paper does not
   say that the method takes its parts from CodeLutra (owner,
   2026-11-27).
8. Privacy is that data stay at the client. No claim about differential
   privacy or about what an adapter reveals.
9. No "state of the art". Every comparison is inside one setup: the
   same model, prompt, decoding and rounds.
10. "Federated Text-to-SQL" means federated training of the model, said
    once in the introduction.
11. The cost figures are sums over five clients run on one card.

## 5. Limitations the paper states (Discussion)

Owner, 2026-11-28 (second revision): the last paragraph of the
Discussion states the scope and future work, three items, each once.

1. The method needs a gold SQL query for each training question and
   databases on which the client can execute queries.
2. The federations studied have at most ten clients, all of which take
   part in every round; partial participation is future work.
3. Privacy is data isolation; differential privacy is future work.

Notes only, ready for a reviewer (not printed as limitations): each
model comes from one training run (Section 4.4 gives the seed as a
setting) and each setup from one draw of the partition; an execution
label, like EX, is a match of results on one database, and test-suite
accuracy measures this at evaluation, not for the training labels; the
McNemar test covers the variation over evaluation questions, not
between training runs; what an adapter or a pair count reveals; client
compute (a result of Section 5.5, E2); model sizes of 0.5B to 1.5B with
LoRA and SQLite benchmarks in English; the number of warm-up rounds as
a setting, and the smaller gain of the 0.5B model (stated in Section
5.4 as a result, D1).

## 6. Term sheet and notation

The terms and the notation of the paper are in `TERMS.md`, a glossary
that holds no lab word, date or decision; those are here. The owner
revised the terms on 2026-11-26 to the terms of the field: the labels are
"correct" and "incorrect", the two kinds of incorrect query are
"execution error" and "incorrect result", the model generates a query,
a client samples and executes. Sections 1 to 5 above keep the words
they were approved in; the paper states them in the terms of `TERMS.md`.

Lab words, which the paper never uses, and what stands for each:

| Lab word | Paper |
|---|---|
| student | the model |
| base student | the pretrained model |
| small model | small language model (SLM), with its parameter count at first use; not in the title or the name of the method |
| right, wrong | correct, incorrect |
| wrong result | incorrect result |
| DPO round | preference round |
| k2, FedPref | `\method` |
| fedavg, bird_sft | FedAvg SFT |
| SFT stage, k | warm-up rounds |
| DPO + NLL round | preference round |
| err, wr | execution error, incorrect result |
| I1 | on-policy pairs |
| feddpo | FedDPO |
| RFT | the method without the preference term |
| arm, line | a row of a table (no term) |
| bird, spider, syn, ... | the evaluation sets by name |

## 7. Decided (owner, 2026-11-26)

1. The Holm correction runs inside each table: the tests of a table
   answer one question and form one family. A test is counted once, in
   the first table that prints it. The Setup section states it. Owner,
   2026-11-28: the family of the text is removed; a comparison that no
   table prints is stated in points and counts, without a p and without
   a significance word.
2. Table 4 keeps a BIRD block and a Spider block until the BIRD rows of
   B3, B4 and B5 are read. B1 is worded for BIRD either way.
3. Table 7 has a row for the method without warm-up rounds and its test
   against the method, on every set of the table.
4. C3 is a result of the paper, written by `paper_numbers.py` from the
   committed predictions; it stands in Section 5.2 in two sentences,
   with its counts under the test suite, and its counts by round in
   Table S6 (owner, 2026-11-28).
5. The names of section 6 stand: "warm-up round", "preference round",
   "FedDPO" for the published baseline. The labels and the verbs
   were revised the same day (`TERMS.md`).
6. The first contribution is worded as in section 2.
7. The second contribution names what leaves a client exactly: the
   adapter and the count that weights it.
8. The method constructs two pairs per question, and the paper gives
   the reason in Section 3.6: the number of pairs sets the length of
   local training. The ten pairs of CodeLutra are named beside it in
   Section 4.5, not in the Method section (owner, 2026-11-27). No claim
   on accuracy at other numbers of pairs; none was run.
9. The numbers of questions that yield pairs and of pairs per round are
   columns of Table 8 (E2) and are read in Section 5.5. Changed with
   the outline of 2026-11-27 (owner): Section 3.2 states once the share
   of questions that yield preference pairs at the first
   preference round (`\fact{cost.bird.pref1.paired_pct}` 62.3% on
   BIRD); the counts by round stay in the cost table.
