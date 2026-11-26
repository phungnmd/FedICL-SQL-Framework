# Outline: Section 5, Results

One line per paragraph, in order. "Serves" names the statement of the
brief (A1 to A6, D1 to D4, C1 to C3, E1, E2; an unnumbered row by its
content). Words are running text; captions are not counted. Total
1,620. The lines are notes, not sentences of the paper; a value in
brackets is what the macro prints today.

No text between `\section{Results}` and 5.1: Section 4 has stated the
four questions and their order.

## 5.1 Comparison with the baselines (RQ1) (495)

Table 3 is read first (three paragraphs), then Fig. 2 (two).

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The headline. At the same $T$ rounds `\method` is above FedAvg SFT on both datasets. Table 3 in one clause: the federated rows after $T$ rounds, "No training" the pretrained model. BIRD dev first: the two EX values and the gain; the test read through its counts (questions correct only with `\method` against correct only with FedAvg SFT), then $p$. Spider test: the two EX values, the gain, $p$. Both significant after the correction. Last sentence, the second seed on BIRD: the two rows and their difference with its test, direction and size left to the macros (waits) | A1; second seed | Table 3 (`tab:main`); `\ex{bird}{k2}{4}`, `\ex{bird}{fedavg}{4}`, `\gain{bird}{fedavg}{4}{k2}{4}`, `\nfix`, `\nbrk`, `\pval` of that comparison; the same for `spider` without the counts; `\ex[qwen15:s1]{bird}{fedavg}{4}`, `\ex[qwen15:s1]{bird}{k2}{4}`, `\gain[qwen15:s1]{...}`, `\pval[qwen15:s1]{...}`; `sec:stat-test` | 125 |
| 2 | The gain is not confined to one kind of question: `\method` is higher on every difficulty level of both sets. The largest difference is on the moderate questions of BIRD and the extra hard of Spider, each quoted as its pair of EX values; the other levels are left to the table. No statement of significance by level | A3 | `\lvl{bird}{k2}{4}{moderate}`, `\lvl{bird}{fedavg}{4}{moderate}`, `\lvl{spider}{k2}{4}{extra}`, `\lvl{spider}{fedavg}{4}{extra}` | 60 |
| 3 | The other rows of Table 3, each with the question it answers. Centralized SFT on Spider: level with FedAvg SFT (difference not significant), and `\method` above it, so the gain is more than what pooling the data gives SFT; BIRD: the same two comparisons by macro (waits). Local SFT: mean and range over the clients, against the federated rows (waits). FedProx SFT: its difference to FedAvg SFT, the answer to whether a remedy for non-IID clients under the same supervision accounts for the gain (waits). FedDPO: its EX and its difference to FedAvg SFT; Section 6 separates what distinguishes it from `\method` (waits). Every waiting sentence states the comparison and prints the macros | A5, A6 | `\ex{spider}{central}{3}`, `\gain{spider}{fedavg}{4}{central}{3}`, `\pval` of it, `\gain{spider}{central}{3}{k2}{4}`, `\pval` of it; `\ex{bird}{central}{3}`, `\gain{bird}{central}{3}{k2}{4}`, `\pval` of it; `\fact{local.bird.mean}`, `.min`, `.max`, the same for `spider`; `\ex{bird}{fedprox}{4}`, `\gain{bird}{fedavg}{4}{fedprox}{4}`, `\pval`, the same for `spider`; `\ex{bird}{feddpo}{4}`, `\gain{bird}{fedavg}{4}{feddpo}{4}`, the same for `spider`; `sec:baselines`, `sec:ablation` | 120 |
| 4 | Where the gain arises. Fig. 2: EX by round; the two curves coincide through round 2, since the warm-up rounds of `\method` are the first two rounds of FedAvg SFT. From that common model, one preference round adds more than one further SFT round: on BIRD and on Spider the gain of the preference round with its $p$ (significant) against the gain of the SFT round with its $p$ (not significant, called so) | A4 | Fig. 2 (`fig:rounds`); `\gain{bird}{fedavg}{2}{k2}{3}`, `\pval`; `\gain{bird}{fedavg}{2}{fedavg}{3}`, `\pval`; the same four for `spider`; `sec:warmup` | 95 |
| 5 | More FedAvg SFT rounds do not close the gap. FedAvg SFT does not improve after round 3 on either dataset: BIRD highest at round 3, Spider the same EX at rounds 3 and 4 and lower at round 5; its two falls are not significant and are called so. `\method` at $T$ rounds is above the highest round of FedAvg SFT on BIRD (gain, $p$) and above its fifth round on Spider (gain). The gain at round 4 on BIRD is thus not an effect of the round at which FedAvg SFT is read | A2 | `\ex{bird}{fedavg}{3}`, `\gain{bird}{fedavg}{3}{k2}{4}`, `\pval` of it; `\gain{bird}{fedavg}{3}{fedavg}{4}`, `\pval`; `\ex{spider}{fedavg}{3}`, `\ex{spider}{fedavg}{5}`, `\gain{spider}{fedavg}{4}{fedavg}{5}`, `\pval`; `\gain{spider}{fedavg}{5}{k2}{4}` | 95 |

## 5.2 Other models and federated setups (RQ2) (405)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | A smaller model of the same family is also above FedAvg SFT, by a smaller margin. Opening clause: the model or the setup is varied, everything else as in Section 5.1. Table 4; Qwen2.5-Coder-0.5B on Spider test: the two EX values, the gain, $p$ (significant), beside the gain of the main model. One sentence of conjecture on the smaller margin: two warm-up rounds may leave the smaller model further from the level SFT reaches, so its first preference round starts from a weaker model | D1 | Table 4 (`tab:models`); `\ex[qwen05]{spider}{k2}{4}`, `\ex[qwen05]{spider}{fedavg}{4}`, `\gain[qwen05]{spider}{fedavg}{4}{k2}{4}`, `\pval[qwen05]{...}`, `\gain{spider}{fedavg}{4}{k2}{4}`; `sec:models` | 130 |
| 2 | A model of another family. DeepSeek-Coder-1.3B on Spider test and on BIRD dev: EX of the pretrained model, of FedAvg SFT and of `\method`, the difference and its test on each set. What is compared, direction and size left to the macros (waits; only the pretrained model on Spider is in). A reading sentence is added when the rows are in | D2 | `\ex[dsc13]{spider}{base}{0}`, `\ex[dsc13]{spider}{fedavg}{4}`, `\ex[dsc13]{spider}{k2}{4}`, `\gain[dsc13]{spider}{fedavg}{4}{k2}{4}`, `\pval[dsc13]{...}`; the same for `bird` | 105 |
| 3 | Other federated setups. Table 5 lists the setups of Table 2; its first two rows are the main rows of Table 3, on which the result so far rests. The three further setups on Spider, each named by what it changes against the main setup (a weaker skew, IID clients, ten clients): EX of FedAvg SFT and of `\method`, the difference and its test (waits). A reading sentence (does the difference follow the strength of the skew or the number of clients) is added when the rows are in | D3 | Table 5 (`tab:federated`); `\ex{spider}{fedavg_a05}{4}`, `\ex{spider}{k2_a05}{4}`, `\gain{spider}{fedavg_a05}{4}{k2_a05}{4}`, `\pval`; the same for `_iid` and `_a05k10`; `tab:setups` | 170 |

## 5.3 Perturbed questions and test-suite accuracy (RQ3) (315)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The gain holds on the perturbed sets. Table 6; `\method` is above FedAvg SFT in EX on Spider dev and on the three perturbed sets, the four gains quoted. After the correction the difference is significant on Spider-Syn only, said plainly, with the unadjusted $p$ of Spider dev as the example. Both models lose about as much from Spider dev to Spider-Syn (the two pairs of EX), so the perturbation costs both alike and the gain is kept, not widened | D4 | Table 6 (`tab:robust`); `\gain{spiderdev}{fedavg}{4}{k2}{4}`, `\pval`; `\gain{syn}{...}`, `\gain{realistic}{...}`, `\gain{dk}{...}`; `\ex{spiderdev}{k2}{4}`, `\ex{syn}{k2}{4}`, `\ex{spiderdev}{fedavg}{4}`, `\ex{syn}{fedavg}{4}`; `sec:datasets` | 150 |
| 2 | The gain also holds under the stricter metric. TS is lower than EX in every row, as expected; `\method` stays above FedAvg SFT under TS on the three sets with test suites, by gains close to those in EX (the three TS gains, the $p$ of Spider dev; significant after the correction on Spider-Syn only). The gain in EX therefore does not consist of predictions that match the gold SQL query on the evaluation database alone | D4; TS row | `\ts{spiderdev}{k2}{4}`, `\ts{spiderdev}{fedavg}{4}`, `\tsgain{spiderdev}{fedavg}{4}{k2}{4}`, `\tspval`; `\tsgain{syn}{...}`, `\tsgain{realistic}{...}` | 110 |
| 3 | Pointer for the remaining row. `\method` without warm-up rounds: no difference in EX to `\method` is significant after the correction, while its TS is lower on all three sets (the pair on Spider dev). Section 6 reads this row | no-warm-up row | `\ts{spiderdev}{k0}{4}`, `\ts{spiderdev}{k2}{4}`; `sec:ablation` | 55 |

## 5.4 Analysis of the predictions and cost of a round (RQ4) (405)

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | What changes: the execution errors. Fig. 3 splits the incorrect predictions of each round into incorrect results and execution errors. At $T$ rounds `\method` has about half the execution errors of FedAvg SFT on both sets (the two pairs). The incorrect results do not become fewer than with FedAvg SFT (the two pairs); within `\method` the second preference round lowers them on BIRD (round 3 to round 4). The gain thus consists of queries that now execute and return the correct result. Why the incorrect results stay: pointer to Section 7 | C1, C2 | Fig. 3 (`fig:errors`); `\nerr{bird}{fedavg}{4}`, `\nerr{bird}{k2}{4}`, `\nerr{spider}{fedavg}{4}`, `\nerr{spider}{k2}{4}`; `\nwr` for the same four; `\nwr{bird}{k2}{3}`; `sec:discussion` | 115 |
| 2 | `\method` reaches correct predictions that are not written like the gold SQL query. The two groups in one clause: a correct prediction reads the tables and columns of the gold SQL query or reads others (a prediction that cannot be parsed counts among the others). On BIRD the second group stays flat with FedAvg SFT over rounds 2 to 4 and grows in each preference round; on Spider at $T$ rounds FedAvg SFT has as many as the pretrained model, `\method` more. The first group grows too (the pairs at $T$ rounds), so both contribute; on BIRD the second group is a large part of the gain. Tie to the method in one sentence, as a property and not as a tested cause: an execution label depends on the execution result of a sample and not on its form | C3 | `\fact{form.bird.fedavg.2.other_right}`, `.3.`, `.4.`; `\fact{form.bird.k2.3.other_right}`, `.4.`; `\fact{form.spider.fedavg.4.other_right}`, `\fact{form.spider.k2.4.other_right}`, `\fact{form.spider.base.0.other_right}`; `.gold_right` at round 4 for `bird` and `spider`, both rows; `sec:pref-round` | 110 |
| 3 | What it costs: no communication, client time. Table 7. A client sends the same adapter in a warm-up and in a preference round. Client time, named so: the minutes of the five clients of a round, trained one after another on one GPU. A FedAvg SFT round against the two preference rounds as ratios, BIRD then Spider; the second preference round on Spider takes less than a FedAvg SFT round. Link to Section 5.1: FedAvg SFT does not improve after round 3, so this time spent on further SFT rounds does not yield the gain | E1, E2 | Table 7 (`tab:cost`); `\fact{cost.bird.adapter_mb}`; `\fact{cost.bird.sft.train_min}`, `\fact{cost.bird.pref1.total_min}`, `.pref2.total_min`, `.pref1.ratio`, `.pref2.ratio`; the same for `spider`; `sec:cost`, `sec:rq1` | 100 |
| 4 | Where the client time goes. Training on the pairs is the largest part and shrinks in the second preference round because fewer questions yield pairs: more of them have only correct samples (questions with pairs, pairs and questions with only correct samples in the two rounds; BIRD with numbers, Spider by reference to the table and its all-correct counts). Labeling: on BIRD more than sampling and second to training, on Spider a few minutes; offered as a reason: every sample is executed and the databases of BIRD are far larger | E2; the two unnumbered rows of 5.4 | `\fact{cost.bird.pref1.paired}`, `.questions`, `.pairs`, `.all_correct`; `\fact{cost.bird.pref2.paired}`, `.pairs`, `.all_correct`; `\fact{cost.spider.pref1.all_correct}`, `.pref2.all_correct`; `\fact{cost.bird.pref1.label_min}`, `.pref2.label_min`, `\fact{cost.spider.pref1.label_min}`; `li2023bird` | 80 |

## Floats and captions

| Float | Placed after | The caption says |
|---|---|---|
| Table 3 | 5.1, paragraph 1 | EX (%) overall and by difficulty level; federated rows after $T$ rounds, Centralized and Local SFT after their epochs; Local SFT as mean with lowest and highest client; $\Delta$ to FedAvg SFT of the block (second seed: of that seed); $p$ the unadjusted exact McNemar test against that row, asterisk significant at the `\fact{test.alpha}` level after the Holm correction; bold the best federated row |
| Fig. 2 | 5.1, paragraph 4 | EX by round, panels a and b; round 0 the pretrained model; `\method` shares rounds 1 and 2 with FedAvg SFT, rounds 3 and 4 are preference rounds |
| Table 4 | 5.2, paragraph 1 | EX of the pretrained model, FedAvg SFT and `\method` after $T$ rounds, main setup of each benchmark; $\Delta$, $p$ and asterisk as in Table 3 |
| Table 5 | 5.2, paragraph 3 | EX after $T$ rounds in the setups of Table 2; the first two rows are those of Table 3; $\Delta$, $p$, asterisk as in Table 3 |
| Table 6 | 5.3, paragraph 1 | EX and TS (%), all rows after $T$ rounds; no test suite for Spider-DK; the two pairs of $\Delta$ and $p$ rows and what each is against; asterisk as in Table 3 |
| Fig. 3 | 5.4, paragraph 1 | incorrect predictions by round, split into incorrect results and execution errors; `\method` from round 3 |
| Table 7 | 5.4, paragraph 3 | what the clients train on in a round, minutes summed over the five clients trained one after another on one GPU, megabytes a client sends per round |

## For the editor

1. Equal compute on BIRD (5.4, paragraph 3; ceiling of E2). By Table 7
   the four rounds of `\method` take 2 x 173 + 470 + 391 = 1,207
   minutes of client time on BIRD, about seven FedAvg SFT rounds, and
   FedAvg SFT is run to round 4. On Spider they take 560 minutes and
   five FedAvg SFT rounds take 620, so Fig. 2b holds a direct comparison
   at more client time for FedAvg SFT; on BIRD there is none. I plan to
   word the link as "FedAvg SFT does not improve after round 3" and to
   state the direct comparison for Spider only, without typed digits. A
   sentence that says more SFT rounds "do not reach it" on BIRD at equal
   client time would go beyond rounds 0 to 4. FedAvg SFT rounds 5 to 7
   on BIRD (about 173 minutes each) would close this.
2. D1, the conjecture. Its premise (FedAvg SFT of the 0.5B model still
   improves at round 4) has no number in the paper. I plan the
   conjecture without that premise, as in paragraph 1 of 5.2. If
   `\ex[qwen05]{spider}{fedavg}{3}` can be given, the premise can be
   stated; otherwise the sentence can also be dropped.
3. No-warm-up row, Spider-DK (5.3, paragraph 3). The brief calls its EX
   "level with `\method`". On Spider-DK it is 3.55 points above
   `\method` (unadjusted p 0.032, not significant after the correction),
   and the table prints it. I word the pointer as "no difference in EX
   is significant after the correction". Its TS is lower on all three
   sets, significant after the correction on Spider-Syn only; the
   pointer says "lower" and leaves the test to Section 6.
4. Section 5.2 is short for now. Paragraphs 2 and 3 can hold only what
   is compared; their reading sentences (about 25 and 45 words) wait for
   the rows. Until then 5.2 runs to about 335 words and the section to
   about 1,550.
5. Order in 5.1: Table 3 first (headline, levels, other rows), then
   Fig. 2 with A4 before A2, since the figure is read from the round
   where the curves part to the rounds after it. The brief lists A2 and
   A4 before A3.
6. Table 6, a missing fact: the brief does not say on which clients the
   rows of Table 6 were trained. I take them to be the models of the
   main Spider setup and say so in the caption unless told otherwise.
7. Two optional clauses, left out unless wanted. (a) 5.1, paragraph 4:
   the EX gain of the second preference round,
   `\gain{bird}{k2}{3}{k2}{4}` (+2.54, significant) and
   `\gain{spider}{k2}{3}{k2}{4}` (+0.74, not significant); the macros
   exist, the brief does not list them. (b) 5.3, paragraph 1: on
   Spider-DK FedAvg SFT is at the level of the pretrained model (59.63
   against 60.19) while `\method` is above both.
8. Heading of 5.4: "Analysis of the predictions and cost of a round
   (RQ4)" in place of "What changes and what it costs (RQ4)"; the other
   three as in the brief.
