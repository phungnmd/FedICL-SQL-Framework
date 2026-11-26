# Brief: Section 5, Results

Kind of section: results (`voice/results.md`).
Outline to: `briefs/05_results_outline.md`. Draft to:
`sections/05_results.tex`. Notes to: `briefs/05_results_notes.md`.

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Headings | `\section{Results}\label{sec:results}`; `\subsection{Comparison with the baselines (RQ1)}\label{sec:rq1}`; `\subsection{Other models and federated setups (RQ2)}\label{sec:rq2}`; `\subsection{Perturbed questions and test-suite accuracy (RQ3)}\label{sec:rq3}`; `\subsection{What changes and what it costs (RQ4)}\label{sec:rq4}`. The wording of the four headings is yours; no heading below a subsection |
| Before it | Section 4 (`sec:setup`, in `sections/04_setup.tex`): the research questions, datasets and metrics, the federated setups (Table 2), models, baselines, settings, the statistical test. Nothing of it is repeated here |
| After it | Section 6 (`sec:ablation`): each part of the method removed in turn (Table 8). Section 7 (`sec:discussion`): interpretation and limitations |
| Floats | Table 3 (`tab:main`), Fig. 2 (`fig:rounds`), Table 4 (`tab:models`), Table 5 (`tab:federated`), Table 6 (`tab:robust`), Fig. 3 (`fig:errors`), Table 7 (`tab:cost`) |
| Purpose | Answer the four research questions, each from its table or figure; say what each number means for the question |
| Length | about 1,620 words of running text, 1,800 at most. About: 5.1 495, 5.2 405, 5.3 315, 5.4 405. Captions are not counted |

## Numbers that wait

Some rows are not run yet; their cells print `--` in the tables and
their macros print `??`. A sentence on such a number says what is
compared and leaves the direction and the size to the macros: it must
stay true whichever way the number falls, and it is read again when
the row is in. A sentence on such a row holds whatever the row shows. The statements below
mark these as "waits".

## Section 5.1, RQ1: against the baselines (Table 3, Fig. 2)

### Statements to establish

| # | Claim | Evidence (macros) | Ceiling |
|---|---|---|---|
| A1 | At $T$ = 4 rounds `\method` is above FedAvg SFT on both datasets. The headline is BIRD | BIRD dev: `\ex{bird}{k2}{4}` against `\ex{bird}{fedavg}{4}`, `\gain{bird}{fedavg}{4}{k2}{4}` points; `\nfix{bird}{fedavg}{4}{k2}{4}` questions correct only with `\method` against `\nbrk{bird}{fedavg}{4}{k2}{4}` correct only with FedAvg SFT; p = `\pval{bird}{fedavg}{4}{k2}{4}`. Spider test: `\ex{spider}{k2}{4}` against `\ex{spider}{fedavg}{4}`, `\gain{spider}{fedavg}{4}{k2}{4}`, p = `\pval{spider}{fedavg}{4}{k2}{4}` | "above FedAvg SFT at the same number of rounds on both datasets", significant after correction; the comparison is inside one setup |
| A2 | More FedAvg SFT rounds do not close the gap: FedAvg SFT stops improving after round 3 on both datasets (Fig. 2) | BIRD: highest at round 3, `\ex{bird}{fedavg}{3}`; `\method` at 4 rounds is `\gain{bird}{fedavg}{3}{k2}{4}` above it (p = `\pval{bird}{fedavg}{3}{k2}{4}`). Spider: `\ex{spider}{fedavg}{3}` at rounds 3 and 4, `\ex{spider}{fedavg}{5}` at round 5; `\method` is `\gain{spider}{fedavg}{5}{k2}{4}` above round 5. FedAvg SFT has a fifth round on Spider only; Section 4.4 gives $T$ = 4 for every federated row, so the text says where the fifth round comes in. The highest round of FedAvg SFT on Spider is rounds 3 and 4, so `\method` against its highest round is the gain of A1 | Its falls (BIRD round 4 `\gain{bird}{fedavg}{3}{fedavg}{4}`, p = `\pval{bird}{fedavg}{3}{fedavg}{4}`; Spider round 5 `\gain{spider}{fedavg}{4}{fedavg}{5}`, p = `\pval{spider}{fedavg}{4}{fedavg}{5}`) are not significant and are called so where they are mentioned. Strongest wording: FedAvg SFT "does not improve after round 3" |
| A4 | From the same model (FedAvg SFT after 2 rounds), one preference round adds more than one further SFT round | BIRD: `\gain{bird}{fedavg}{2}{k2}{3}` (p = `\pval{bird}{fedavg}{2}{k2}{3}`) against `\gain{bird}{fedavg}{2}{fedavg}{3}` (p = `\pval{bird}{fedavg}{2}{fedavg}{3}`). Spider: `\gain{spider}{fedavg}{2}{k2}{3}` (p = `\pval{spider}{fedavg}{2}{k2}{3}`) against `\gain{spider}{fedavg}{2}{fedavg}{3}` (p = `\pval{spider}{fedavg}{2}{fedavg}{3}`) | as stated; this is the answer to "FedAvg SFT with one more round" |
| A3 | The gain is on every difficulty level | BIRD simple, moderate, challenging: `\lvl{bird}{k2}{4}{simple}`, `{moderate}`, `{challenging}` against `\lvl{bird}{fedavg}{4}{...}`. Spider easy, medium, hard, extra: `\lvl{spider}{k2}{4}{easy}` ... against `\lvl{spider}{fedavg}{4}{...}` | "higher on every level; the largest difference on the moderate questions of BIRD and the extra hard of Spider". The levels are compared by their EX; the tests are on the whole sets |
| A5 | Centralized SFT. Spider: level with FedAvg SFT, and `\method` is above it. BIRD: waits | Spider: `\ex{spider}{central}{3}`; against FedAvg SFT `\gain{spider}{fedavg}{4}{central}{3}`, p = `\pval{spider}{fedavg}{4}{central}{3}`; `\method` against it `\gain{spider}{central}{3}{k2}{4}`, p = `\pval{spider}{central}{3}{k2}{4}`. BIRD (waits): `\ex{bird}{central}{3}`, `\gain{bird}{central}{3}{k2}{4}`, `\pval{bird}{central}{3}{k2}{4}` | "above SFT on the pooled data", on Spider with its main setup |
| A6 | Local SFT, FedProx SFT, FedDPO: wait on both datasets | local SFT: `\fact{local.bird.mean}` (`\fact{local.bird.min}` to `\fact{local.bird.max}`), the same with `spider`. FedProx SFT: `\ex{bird}{fedprox}{4}`, `\gain{bird}{fedavg}{4}{fedprox}{4}`, `\pval{...}`; the same with `spider`. FedDPO: `\ex{bird}{feddpo}{4}`, `\gain{bird}{fedavg}{4}{feddpo}{4}`; the same with `spider` | one or two sentences that say which rows of Table 3 answer what (Section 4.4) and carry the macros; worded so that they hold whatever the rows show |
| | Second seed of the two main rows on BIRD: waits | `\ex[qwen15:s1]{bird}{fedavg}{4}`, `\ex[qwen15:s1]{bird}{k2}{4}`, `\gain[qwen15:s1]{bird}{fedavg}{4}{k2}{4}` | one sentence: the gain on the second seed, with its test |

### Table 3

`table` environment, `\caption{...}\label{tab:main}` above,
`\input{generated/tab_main}`.

| Part | Content |
|---|---|
| blocks | BIRD dev, then Spider test |
| rows | No training (the pretrained model; Section 4 does not explain this row, so 5.1 says it in a clause); Local SFT (mean over the clients, lowest to highest client in brackets; no test); Centralized SFT; FedAvg SFT; FedProx SFT; FedDPO; `\method`; on BIRD the two main rows on a second seed |
| columns | EX; EX by difficulty level; $\Delta$: difference in EX to FedAvg SFT of the block (second-seed row: to FedAvg SFT of that seed); $p$: exact McNemar test against that row, unadjusted, asterisk when significant after the Holm correction (Section 4.6). The caption says what the asterisk and the $p$ are: Section 4.6 leaves it to the captions |
| bold | best value of a column among the federated rows |
| all federated rows | at $T$ = 4 rounds; centralized and local SFT at 3 epochs |

### Fig. 2

`figure` environment, `\includegraphics{figures/fig_rounds.pdf}`,
`\caption{...}\label{fig:rounds}` below; file to look at:
`figures/fig_rounds.pdf`.

| Part | Shows |
|---|---|
| panels | a BIRD dev, b Spider test; EX by round |
| dashed line | FedAvg SFT, rounds 0 (no training) to 4 on BIRD, to 5 on Spider |
| solid line | `\method`: leaves the FedAvg SFT curve at round 2 (its warm-up rounds are the first two FedAvg SFT rounds), rounds 3 and 4 are preference rounds |

## Section 5.2, RQ2: other models and federated setups (Tables 4, 5)

### Statements to establish

| # | Claim | Evidence (macros) | Ceiling |
|---|---|---|---|
| D1 | A smaller model of the same family: also above FedAvg SFT, by a smaller margin | Qwen2.5-Coder-0.5B, Spider test: `\ex[qwen05]{spider}{k2}{4}` against `\ex[qwen05]{spider}{fedavg}{4}`, `\gain[qwen05]{spider}{fedavg}{4}{k2}{4}`, p = `\pval[qwen05]{spider}{fedavg}{4}{k2}{4}` (the 1.5B model: `\gain{spider}{fedavg}{4}{k2}{4}`) | significant; the margin is stated beside that of the 1.5B model |
| D2 | A model of another family, DeepSeek-Coder-1.3B: waits (Spider and BIRD) | `\ex[dsc13]{spider}{base}{0}` is in; `\ex[dsc13]{spider}{fedavg}{4}`, `\ex[dsc13]{spider}{k2}{4}`, `\gain[dsc13]{spider}{fedavg}{4}{k2}{4}`, `\pval[dsc13]{...}`; the same with `bird` | what is compared, with the macros |
| D3 | Other federated setups on Spider (IID; $\alpha$ = 0.5 with 5 and with 10 clients): wait | Table 5; lines `fedavg_iid`, `k2_iid`, `fedavg_a05`, `k2_a05`, `fedavg_a05k10`, `k2_a05k10` in `\ex{spider}{<line>}{4}` and `\gain{spider}{fedavg_iid}{4}{k2_iid}{4}` (and so on) | the two main setups carry the result; the sentence on the three further setups carries the macros and holds whatever they show |

### Tables 4 and 5

`\input{generated/tab_models}` with `\label{tab:models}`;
`\input{generated/tab_federated}` with `\label{tab:federated}`.

| Table | Rows and columns |
|---|---|
| 4 | per evaluation set and model: EX without training, of FedAvg SFT and of `\method` at 4 rounds, $\Delta$ and $p$ of `\method` against FedAvg SFT. Main setup of each benchmark |
| 5 | per federated setup of Table 2: EX of FedAvg SFT and of `\method` at 4 rounds, $\Delta$, $p$. The first two rows are the main rows of Table 3 |

## Section 5.3, RQ3: perturbed questions and test-suite accuracy (Table 6)

### Statements to establish

| # | Claim | Evidence (macros) | Ceiling |
|---|---|---|---|
| D4 | The gain over FedAvg SFT holds on the four sets and under both metrics | EX: `\gain{spiderdev}{fedavg}{4}{k2}{4}` (p = `\pval{...}`), `\gain{syn}{fedavg}{4}{k2}{4}`, `\gain{realistic}{fedavg}{4}{k2}{4}`, `\gain{dk}{fedavg}{4}{k2}{4}`. TS: `\tsgain{spiderdev}{fedavg}{4}{k2}{4}` (p = `\tspval{...}`), `\tsgain{syn}{...}`, `\tsgain{realistic}{...}` | "above FedAvg SFT on all four sets and under both metrics"; after the correction significant on Spider-Syn only (the asterisks of Table 6), and the text says so. Both models lose about as much from Spider dev to Spider-Syn (`\ex{spiderdev}{k2}{4}` to `\ex{syn}{k2}{4}`; `\ex{spiderdev}{fedavg}{4}` to `\ex{syn}{fedavg}{4}`), so the strongest wording is "the gain holds on the perturbed sets" |
| | TS is lower than EX for every row, as expected of a stricter metric; `\method` stays above FedAvg SFT under it | `\ts{spiderdev}{k2}{4}`, `\ts{spiderdev}{fedavg}{4}` and the same for `syn`, `realistic` | as stated |
| | Table 6 also has the row of `\method` without warm-up rounds: no difference in EX to `\method` is significant after the correction, and its TS is lower on all three sets. The variant is `\method` with $T_w = 0$: all four rounds are preference rounds, the first from the pretrained model; Sections 3 and 4 do not define it, so the sentence does. One sentence here that points to Section 6, where it is read | `\ts{spiderdev}{k0}{4}` against `\ts{spiderdev}{k2}{4}` | the pointer to Section 6, where the row is read |

### Table 6

`\input{generated/tab_robust}` with `\label{tab:robust}`. Columns: EX
and TS on Spider dev, Spider-Syn, Spider-Realistic; EX on Spider-DK (no
test suite). Rows: No training; FedAvg SFT; `\method` without warm-up
rounds; `\method`; then $\Delta$ and $p$ of `\method` against FedAvg
SFT, and against `\method` without warm-up rounds. All at 4 rounds.
The rows are the models of the main Spider setup: the Spider rows of
Table 3, and `\method` without warm-up rounds trained in the same
setup. The caption says so.

## Section 5.4, RQ4: what changes and what it costs (Fig. 3, Table 7)

### Statements to establish

| # | Claim | Evidence (macros) | Ceiling |
|---|---|---|---|
| C1 | The preference rounds halve the execution errors | at 4 rounds, FedAvg SFT against `\method`: BIRD `\nerr{bird}{fedavg}{4}` against `\nerr{bird}{k2}{4}`; Spider `\nerr{spider}{fedavg}{4}` against `\nerr{spider}{k2}{4}` | as stated |
| C2 | Incorrect results do not become fewer than with FedAvg SFT | BIRD `\nwr{bird}{fedavg}{4}` against `\nwr{bird}{k2}{4}`; Spider `\nwr{spider}{fedavg}{4}` against `\nwr{spider}{k2}{4}`. Inside `\method`, the second preference round lowers them on BIRD (`\nwr{bird}{k2}{3}` to `\nwr{bird}{k2}{4}`) | the finding, said plainly, from the paired predictions of the two rows at 4 rounds (`\fact{moved.<set>.<with FedAvg SFT>.<with the method>}`, outcomes `correct`, `error`, `wrong`). Of the questions correct only with `\method`, about half had an execution error with FedAvg SFT and half an incorrect result: BIRD `\fact{moved.bird.error.correct}` and `\fact{moved.bird.wrong.correct}`, Spider `\fact{moved.spider.error.correct}` and `\fact{moved.spider.wrong.correct}`. Of the execution errors of FedAvg SFT, many execute with `\method` and return an incorrect result: BIRD `\fact{moved.bird.error.wrong}` of `\nerr{bird}{fedavg}{4}`, Spider `\fact{moved.spider.error.wrong}` of `\nerr{spider}{fedavg}{4}`. This is why the incorrect results do not become fewer. The two preference rounds differ on BIRD (Fig. 3): the first lowers the execution errors (`\nerr{bird}{fedavg}{2}` to `\nerr{bird}{k2}{3}`) and raises the incorrect results (`\nwr{bird}{fedavg}{2}` to `\nwr{bird}{k2}{3}`); the second lowers the incorrect results (to `\nwr{bird}{k2}{4}`) while the execution errors rise (to `\nerr{bird}{k2}{4}`). On Spider the execution errors fall in both rounds and the incorrect results stay level. Why the preference rounds leave them is Section 7 |
| C3 | `\method` reaches correct predictions that are not written like the gold SQL query, and FedAvg SFT does not | correct predictions that read other tables or columns than the gold SQL query. BIRD: FedAvg SFT `\fact{form.bird.fedavg.2.other_right}`, `\fact{form.bird.fedavg.3.other_right}`, `\fact{form.bird.fedavg.4.other_right}` at rounds 2, 3, 4; `\method` `\fact{form.bird.k2.3.other_right}` and `\fact{form.bird.k2.4.other_right}` at rounds 3 and 4. Spider at 4 rounds: `\fact{form.spider.fedavg.4.other_right}` against `\fact{form.spider.k2.4.other_right}` (no training: `\fact{form.spider.base.0.other_right}`). Correct predictions on the tables and columns of the gold SQL query, at 4 rounds: BIRD `\fact{form.bird.fedavg.4.gold_right}` against `\fact{form.bird.k2.4.gold_right}`; Spider `\fact{form.spider.fedavg.4.gold_right}` against `\fact{form.spider.k2.4.gold_right}` | the counts, for the two sets. Not "a large part of the gain": by the sizes of the groups the second grows by 55 of the 95 questions of net gain on BIRD, by paired questions the gain is 60 in the first group and 35 in the second (no macros; not printed). EX establishes the correctness of such a prediction on the evaluation database only, and the paragraph says so; the TS results of 5.3 are not evidence for this group (on Spider dev the test suite accepts 17 of 48 such predictions of `\method` and 14 of 49 of FedAvg SFT; `LAB_LOG.md`, 2026-11-26). How the two groups are told apart: the set of tables and the set of table.column names the parsed query reads, subqueries included; the same group when both sets equal those of the gold SQL query. No correct prediction of the rows quoted fails to parse, so the text needs no rule for one |
| E1 | No added communication | `\fact{cost.bird.adapter_mb}` MB per client and round, in a warm-up round and in a preference round; samples, labels and pairs stay at the client | as stated |
| E2 | The cost is client compute | minutes for the five clients of a round, one after another on one GPU (Table 7). BIRD: a FedAvg SFT round `\fact{cost.bird.sft.train_min}`; the two preference rounds, sampling + labels + training: `\fact{cost.bird.pref1.sample_min}` + `\fact{cost.bird.pref1.label_min}` + `\fact{cost.bird.pref1.train_min}` and `\fact{cost.bird.pref2.sample_min}` + `\fact{cost.bird.pref2.label_min}` + `\fact{cost.bird.pref2.train_min}`. Spider: `\fact{cost.spider.sft.train_min}`; the same macros with `spider`. Questions that yield pairs and pairs fall from the first to the second preference round: BIRD `\fact{cost.bird.pref1.paired}` of `\fact{cost.bird.pref1.questions}` questions and `\fact{cost.bird.pref1.pairs}` pairs, then `\fact{cost.bird.pref2.paired}` and `\fact{cost.bird.pref2.pairs}`; Spider `\fact{cost.spider.pref1.paired}`, `\fact{cost.spider.pref1.pairs}`, then `\fact{cost.spider.pref2.paired}`, `\fact{cost.spider.pref2.pairs}` | the times are sums over the five clients on one card and are named so (client time). A preference round against a FedAvg SFT round, in client time: `\fact{cost.bird.pref1.ratio}` and `\fact{cost.bird.pref2.ratio}` times on BIRD, `\fact{cost.spider.pref1.ratio}` and `\fact{cost.spider.pref2.ratio}` times on Spider (totals: `\fact{cost.bird.pref1.total_min}`, `\fact{cost.bird.pref2.total_min}`, `\fact{cost.spider.pref1.total_min}`, `\fact{cost.spider.pref2.total_min}` minutes). The link to Section 5.1: FedAvg SFT does not improve after round 3 (A2). On Spider the five FedAvg SFT rounds of Fig. 2 take more client time than the four rounds of `\method` (Table 7), so the comparison at more client time for FedAvg SFT is direct there; on BIRD FedAvg SFT is run to round 4, and the sentence stays inside those rounds |
| | Why the second preference round is cheaper: more questions have only correct samples, so fewer yield pairs | `\fact{cost.bird.pref1.all_correct}` to `\fact{cost.bird.pref2.all_correct}`; Spider `\fact{cost.spider.pref1.all_correct}` to `\fact{cost.spider.pref2.all_correct}` (questions on databases with rows; those on the databases without rows yield no pair in any round and are not counted here) | as stated |
| | Training on the pairs is the largest part of the client time in every preference round. On BIRD the labels come second and take more than sampling; on Spider a few minutes | the step columns of Table 7 | the reason is offered as a reason: the databases of BIRD are far larger than those of Spider (`li2023bird`), and every sample is executed |

### Fig. 3

`\includegraphics{figures/fig_errors.pdf}`,
`\caption{...}\label{fig:errors}`; file to look at:
`figures/fig_errors.pdf`.

| Part | Shows |
|---|---|
| panels | a BIRD dev, b Spider test; incorrect predictions by round |
| bars | per round FedAvg SFT (blue) and, from round 3, `\method` (purple); each bar split into incorrect results (plain) and execution errors (hatched) |

### Table 7

`\input{generated/tab_cost}` with `\label{tab:cost}`. Per benchmark a
FedAvg SFT round (a warm-up round) and the two preference rounds:
what the clients train on (questions; in a preference round the
questions that yield pairs, and the pairs), minutes per round for
sampling, labels and training, their total, and megabytes a client
sends.

## Macros

Text mode; a signed gain prints its sign. The full list with values:
`generated/numbers.md`.

| Macro | Prints |
|---|---|
| `\ex[model]{set}{line}{round}` | EX in percent, two decimals, without the percent sign. `model`: omitted for Qwen2.5-Coder-1.5B, `qwen05`, `dsc13`, `qwen15:s1` (second seed). `set`: `bird`, `spider`, `spiderdev`, `syn`, `realistic`, `dk`. `line`: `base` (no training, round 0), `fedavg`, `k2` (`\method`), `k0` (`\method` without warm-up rounds), `central` (round 3), `fedprox`, `feddpo` |
| `\lvl{set}{line}{round}{level}` | EX on a difficulty level: `simple`, `moderate`, `challenging`; `easy`, `medium`, `hard`, `extra` |
| `\gain{set}{a}{ra}{b}{rb}` | EX of row b minus EX of row a, signed (e.g. `\gain{bird}{fedavg}{4}{k2}{4}` prints +6.19); `\gap{...}` the same without sign |
| `\pval{set}{a}{ra}{b}{rb}`, `\padj{...}` | exact McNemar p of that comparison; its Holm-adjusted value |
| `\nfix{...}`, `\nbrk{...}` | questions correct in b and not in a; correct in a and not in b |
| `\ts{set}{line}{round}`, `\tsgain{...}`, `\tspval{...}` | the same for test-suite accuracy |
| `\nerr{set}{line}{round}`, `\nwr{set}{line}{round}` | predictions with an execution error; with an incorrect result |
| `\fact{form.<set>.<line>.<round>.other_right}`, `.gold_right` | correct predictions that read other tables or columns than the gold SQL query; that read the same |
| `\fact{moved.<set>.<a>.<b>}` | questions with outcome a with FedAvg SFT and outcome b with `\method`, both at 4 rounds; a and b are `correct`, `error` (execution error), `wrong` (incorrect result). `set`: `bird`, `spider` |
| `\fact{model.qwen05}`, `\fact{model.dsc13}` | the names of the two other models, as Table 4 prints them |
| `\fact{cost.<set>.sft.train_min}`, `\fact{cost.<set>.pref<r>.sample_min}`, `.label_min`, `.train_min`, `.total_min`, `.ratio`, `.paired`, `.pairs`, `.questions`, `.all_correct`, `\fact{cost.<set>.adapter_mb}` | Table 7 |
| `\fact{questions.<set>}` | size of an evaluation set |

## Wording that holds for the whole section

| | |
|---|---|
| sets | the sets by their names: BIRD dev, Spider test |
| seeds | one training seed; significance is the test of Section 4.6 |
| comparisons | every comparison is inside one setup: the same model, prompt, decoding and rounds |
| the model | "the model" or its name; the two kinds of incorrect prediction are "execution error" and "incorrect result" |
| causes | a cause that the ablations test is left to Section 6 with a pointer; a cause that nothing tests is a conjecture or is left out |

## Labels available

Of this section: `sec:results`, `sec:rq1`, `sec:rq2`, `sec:rq3`,
`sec:rq4`, `tab:main`, `fig:rounds`, `tab:models`, `tab:federated`,
`tab:robust`, `fig:errors`, `tab:cost`.

Of other sections: `sec:method`, `sec:warmup`, `sec:pref-round`,
`sec:cost`, `sec:setup`, `sec:datasets`, `sec:fed-setups`,
`sec:models`, `sec:baselines`, `sec:implementation`, `sec:stat-test`,
`tab:setups`, `sec:ablation`, `sec:discussion`.

## Paragraph roles (an offer)

For each research question: the question in a clause, the table or
figure that answers it, the finding as a number, and what the number
means for the question. A comparison names both rows and the size of
the difference; a difference that is not significant is called so.
