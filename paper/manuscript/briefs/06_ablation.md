# Brief: Section 6, Ablation study

Kind of section: ablation (`VOICE_GUIDE.md`, Section 2).
Outline to: `briefs/06_ablation_outline.md`. Draft to:
`sections/06_ablation.tex`. Notes to: `briefs/06_ablation_notes.md`.

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Headings | `\section{Ablation study}\label{sec:ablation}`. No subsection is planned for this length; if you want them, say so in the outline |
| Before it | Section 5 (`sec:results`, in `sections/05_results.tex`) answers the four research questions with the whole method. Section 5.1 already gives the step of the second preference round (round 3 to round 4 of `\method`) and the FedDPO row of Table 3; Section 5.3 already gives the test-suite accuracy of the variant without warm-up rounds (Table 6). Neither is reported again here; a clause may refer to them |
| After it | Section 7 (`sec:discussion`): why the two kinds of round remove different errors, the scope and the limitations. Interpretation beyond what a row shows is left to it |
| Float | Table 8 (`tab:ablation`), see "Table 8" |
| Purpose | Show what each part of the method adds, each from the row that removes or replaces it |
| Length | about 880 words of running text, 930 at most (B8 was added after the first number was set). The caption is not counted |

## What the earlier sections promised of this section

The section has to keep each of these, since the text is accepted or
drafted:

| Where | Promise |
|---|---|
| Section 2.2 | Liu et al. construct the pairs once, use the DPO loss alone and a fixed reference model; "Section 6 varies all three of these choices" |
| Section 3.3 | "Section 6 reports these counts and varies the number of warm-up rounds": the questions without a correct sample at the first preference round, from the pretrained model and after the warm-up rounds |
| Section 3.4 | "Section 6 ablates the on-policy pairs, the two terms of the loss and the aggregation weights" |
| Section 4.4 | FedDPO differs from `\method` in two ways (pairs and reference not renewed; no NLL term); "Section 6 ablates the two separately, and also trains on the correct samples without the preference term" |
| Section 4.6 | in Section 6 every row is tested against `\method` at the same number of rounds |
| Section 5.1 | Section 6 "examines separately the two ways in which [FedDPO] differs from `\method`" |
| Section 5.3 | "Section 6 examines this variant" (no warm-up rounds) |

## Numbers that wait

Some rows are not run yet; their cells print `--` in Table 8 and their
macros print `??`. A sentence on such a number says what is compared
and leaves the direction and the size to the macros: it holds whatever
the row shows, and it is read again when the row is in. The statements
below mark these as "waits".

## Statements to establish

Every row starts from the same model as `\method` unless the row is
about the warm-up rounds: FedAvg SFT after $T_w$ = 2 rounds. A row of
the first block is compared with `\method` after 4 rounds, a row of the
second block with `\method` after 3 rounds (one preference round).

Not every row removes or replaces one part. "Fixed pairs and reference"
holds two things fixed at once, and "Clients pooled" keeps the method
and changes the setting (B7). A sentence that says what the rows are
has to hold for these two as well.

| # | Claim | Evidence (macros) | Ceiling |
|---|---|---|---|
| B1 | Renewing the pairs and the reference model. The row "Fixed pairs and reference" keeps, in the second preference round, the pairs and the reference model of the first; the NLL term stays. On BIRD dev it is below `\method`; on Spider test the two are level. The first preference round of the row was run again on the same pairs, and its model after 3 rounds was not evaluated: the EX of the row after 4 rounds may be set beside that of `\method` after 3 as two cells of the table, and nothing is said of what the second round of the row adds | BIRD dev, 4 rounds: `\ex{bird}{fixed}{4}` against `\ex{bird}{k2}{4}`, `\gain{bird}{k2}{4}{fixed}{4}`, p = `\pval{bird}{k2}{4}{fixed}{4}`; `\nbrk{bird}{k2}{4}{fixed}{4}` questions correct only with `\method`, `\nfix{bird}{k2}{4}{fixed}{4}` only with the row. Spider test: `\ex{spider}{fixed}{4}` against `\ex{spider}{k2}{4}`, `\gain{spider}{k2}{4}{fixed}{4}`, p = `\pval{spider}{k2}{4}{fixed}{4}` | stated for BIRD; for Spider test "level", said in the same paragraph. The first preference round of this row is the same procedure on the same pairs as that of `\method`; the two rows differ in the second preference round only. The row holds the pairs and the reference model fixed together, as FedDPO does and as Liu et al. (`liu2025cotdpo`, Section 2.2) do; it does not show which of the two the difference on BIRD dev comes from, and no sentence says so. The reader of the revision looked for the row beside `\method` after three rounds (`\ex{bird}{fixed}{4}` against `\ex{bird}{k2}{3}`): the two cells may be set side by side, as two cells. On Spider test the second preference round of `\method` itself adds `\gain{spider}{k2}{3}{k2}{4}` (p = `\pval{spider}{k2}{3}{k2}{4}`, Section 5.1), on BIRD dev `\gain{bird}{k2}{3}{k2}{4}` (p = `\pval{bird}{k2}{3}{k2}{4}`): a clause may give this, so that "level" on Spider test is read against what the round has to add there |
| B3 | The NLL term. The row "Without the NLL term" is one preference round with the DPO term alone. At this round the pairs and the reference model are those of `\method`, so the NLL term is the only difference; it is also FedDPO after its first preference round (the FedDPO row of Table 3 is the same line after two, where the pairs and the reference are no longer renewed either). On Spider test the round without the NLL term lowers accuracy below the model it started from. BIRD: waits | Spider test, 3 rounds: `\ex{spider}{feddpo}{3}` against `\ex{spider}{k2}{3}`, `\gain{spider}{k2}{3}{feddpo}{3}`, p = `\pval{spider}{k2}{3}{feddpo}{3}`; the model before the round: `\ex{spider}{fedavg}{2}` (no test of the row against it). BIRD dev (waits): `\ex{bird}{feddpo}{3}`, `\gain{bird}{k2}{3}{feddpo}{3}`, `\pval{bird}{k2}{3}{feddpo}{3}`, the model before the round `\ex{bird}{fedavg}{2}` | "without the NLL term the preference round lowers accuracy" on Spider test. The BIRD sentence holds whatever the row shows. Credit in one sentence to the works that report the same for a DPO term alone (rows under "Published results on the likelihood term"); the sentence is about what they report, without their numbers, and is not worded as holding in every setting. What the two works compare: accuracy after training with the DPO term alone against accuracy after the same training with both terms. Section 2.2 promised that this section varies the three choices of Liu et al. (pairs constructed once, the DPO loss alone, a fixed reference model): B1 varies the first and the third together, B3 the second; the section cites Liu et al. where it does so |
| B4 | The preference term. The row "Without the preference term" trains with the NLL term alone, on the correct sample of each pair: the same samples, labels, pairs and settings as a preference round, and the same weights at the server, without the DPO term. Each of its rounds samples, labels and pairs anew, as a preference round does. In EX the row lies between the model before the round and `\method` on both datasets. It leaves more execution errors than `\method`, a significant difference on both datasets. The 4-round rows wait | 3 rounds, EX, the three values of each dataset: the model before the round `\ex{bird}{fedavg}{2}`, the row `\ex{bird}{rft}{3}`, `\method` `\ex{bird}{k2}{3}`; `\ex{spider}{fedavg}{2}`, `\ex{spider}{rft}{3}`, `\ex{spider}{k2}{3}`. Execution errors: BIRD dev `\nerr{bird}{rft}{3}` against `\nerr{bird}{k2}{3}`, the model before the round `\nerr{bird}{fedavg}{2}`; Spider test `\nerr{spider}{rft}{3}` against `\nerr{spider}{k2}{3}`, before the round `\nerr{spider}{fedavg}{2}`. The exact McNemar test of Section 4.6 applied to whether the prediction of a question ends in an execution error, the row against `\method`: p = `\errpval{bird}{k2}{3}{rft}{3}` on BIRD dev, `\errpval{spider}{k2}{3}{rft}{3}` on Spider test, both significant after the correction (family of the comparisons quoted in the text). The same test on whether the prediction is an incorrect result: p = `\wrpval{bird}{k2}{3}{rft}{3}` on BIRD dev, significant after the correction (more incorrect results with `\method`), `\wrpval{spider}{k2}{3}{rft}{3}` on Spider test, not significant. Incorrect results: `\nwr{bird}{rft}{3}` against `\nwr{bird}{k2}{3}`; `\nwr{spider}{rft}{3}` against `\nwr{spider}{k2}{3}`. EX: `\ex{bird}{rft}{3}`, `\gain{bird}{k2}{3}{rft}{3}`, p = `\pval{bird}{k2}{3}{rft}{3}`; `\ex{spider}{rft}{3}`, `\gain{spider}{k2}{3}{rft}{3}`, p = `\pval{spider}{k2}{3}{rft}{3}`. 4 rounds (wait): `\ex{bird}{rft}{4}`, `\gain{bird}{k2}{4}{rft}{4}`, `\pval{bird}{k2}{4}{rft}{4}`, `\nerr{bird}{rft}{4}`; the same with `spider` | the reader learns first where the EX of the row stands: the three values with the difference to `\method` and its p, "lower on both datasets", not significant after the correction; the comparison with the model before the round is one of values and has no test. Then the execution errors, with their test: "more execution errors remain without the preference term", significant on both datasets; the sentence that gives these p-values says that the test is applied to execution errors. The counts are not turned into a share that the preference term "accounts for" or that "requires" it. With the preference term the incorrect results are more numerous than without it (the two `\nwr` counts), significantly so on BIRD dev: the paragraph gives both counts and says which of the two differences are tested and significant, so that the two kinds of incorrect prediction are treated alike. What the row establishes: with the preference term fewer predictions fail to execute; a difference in EX is not established on either dataset. The first sentence of the paragraph may say exactly that; an order of the three EX values is not a tested statement |
| B5 | The warm-up rounds. With no, two and three warm-up rounds at the same total of 4 rounds, EX on Spider test is level. What the warm-up rounds change is seen in two places: fewer training questions are without a correct sample at the first preference round, and the gain of `\method` holds under test-suite accuracy (Table 6, Section 5.3), which it does not without warm-up rounds. BIRD rows: wait | Spider test, 4 rounds: `\ex{spider}{k0}{4}`, `\ex{spider}{k2}{4}`, `\ex{spider}{k3}{4}`; `\gain{spider}{k2}{4}{k0}{4}`, p = `\pval{spider}{k2}{4}{k0}{4}`; `\gain{spider}{k2}{4}{k3}{4}`, p = `\pval{spider}{k2}{4}{k3}{4}`. BIRD dev (wait): `\ex{bird}{k0}{4}`, `\gain{bird}{k2}{4}{k0}{4}`, `\pval{bird}{k2}{4}{k0}{4}`; `\ex{bird}{k3}{4}`, `\gain{bird}{k2}{4}{k3}{4}`, `\pval{bird}{k2}{4}{k3}{4}`. Questions none of whose $N$ samples is labeled correct at the first preference round: BIRD `\fact{warmup.bird.k0.no_correct}` of `\fact{cost.bird.pref1.questions}` from the pretrained model, `\fact{warmup.bird.k2.no_correct}` after two warm-up rounds; Spider `\fact{warmup.spider.k0.no_correct}`, `\fact{warmup.spider.k2.no_correct}` after two, `\fact{warmup.spider.k3.no_correct}` after three, counted among the `\fact{train.spider.with_rows}` questions on databases with rows (the `\fact{train.spider.no_rows}` questions on databases without rows yield no pair in any variant and are left out of these counts, as in Section 5.4; the Spider values are lower than in the first version of this brief for that reason). Test-suite accuracy, `\method` against the variant without warm-up: `\tsgap{spiderdev}{k0}{4}{k2}{4}` (p = `\tspval{spiderdev}{k0}{4}{k2}{4}`), `\tsgap{syn}{k0}{4}{k2}{4}` (p = `\tspval{syn}{k0}{4}{k2}{4}`, the one significant after the correction), `\tsgap{realistic}{k0}{4}{k2}{4}` (p = `\tspval{realistic}{k0}{4}{k2}{4}`). The variant against FedAvg SFT, values of Table 6 without a test: its TS is below that of FedAvg SFT on the three sets (`\ts{spiderdev}{k0}{4}` against `\ts{spiderdev}{fedavg}{4}`, `\ts{syn}{k0}{4}` against `\ts{syn}{fedavg}{4}`, `\ts{realistic}{k0}{4}` against `\ts{realistic}{fedavg}{4}`), while its EX is above on each. On Spider-DK, which has no test suite, EX is higher without warm-up: `\gap{dk}{k0}{4}{k2}{4}`, p = `\pval{dk}{k0}{4}{k2}{4}`, adjusted `\padj{dk}{k0}{4}{k2}{4}` | no gain in EX is stated for the warm-up rounds: EX is level on Spider test, and the Spider-DK difference is said. "Without warm-up rounds the EX gain of `\method` does not carry over to test-suite accuracy; with two it does" is the strongest wording, and the text says what each half rests on: the method against the variant in TS is tested, and after the correction the difference is significant on Spider-Syn only; the variant against FedAvg SFT in TS is a comparison of the values of Table 6. The three TS differences are in Table 6 and need not all be listed again. The paragraph states what the section concludes about the warm-up rounds, in its first sentence: what they change (TS; the questions without a correct sample) and what they do not (EX on Spider test), each with its basis after it. The counts are reported as counts: fewer questions without a correct sample. They are not a count of questions that yield pairs (that number rises on BIRD and falls on Spider, because more questions have only correct samples). No link from the counts to the test-suite result is stated as shown; an interpretation belongs to Section 7. Table 6 is cited, its numbers are not listed again beyond what the sentence needs |
| B8 | The gold SQL query as the correct side. For a question without a correct sample a preference round constructs no pair. A variant constructs $M$ pairs for each such question: the gold SQL query as the correct side of each, with $M$ incorrect samples of the question drawn as in Section 3.4; these pairs are added to the pairs of the other questions. Tried on BIRD in the variant without warm-up rounds, where such questions are most numerous (`\fact{warmup.bird.k0.no_correct}`), in one preference round on the same samples and labels: it does not raise EX | BIRD dev, 1 preference round from the pretrained model: `\ex{bird}{k0gold}{1}` with these pairs against `\ex{bird}{k0}{1}` without, `\gain{bird}{k0}{1}{k0gold}{1}`, p = `\pval{bird}{k0}{1}{k0gold}{1}`, adjusted `\padj{bird}{k0}{1}{k0gold}{1}`; execution errors `\nerr{bird}{k0}{1}` to `\nerr{bird}{k0gold}{1}`, incorrect results `\nwr{bird}{k0}{1}` to `\nwr{bird}{k0gold}{1}` | "does not raise EX: it is lower, and the difference is not significant after the correction; execution errors fall and incorrect results rise by more". The size of the difference is said (`\gap{bird}{k0}{1}{k0gold}{1}` points). This comparison is in no table, so both its p-values are in the text (unadjusted `\pval{bird}{k0}{1}{k0gold}{1}`, adjusted `\padj{bird}{k0}{1}{k0gold}{1}`). The counts of the two kinds of incorrect prediction describe the result; they are not given as the reason why the difference is not significant. One or two sentences, in the part on the warm-up rounds: the warm-up rounds are how `\method` uses the gold SQL of these questions. Stated for BIRD and for this variant; the comparison is a number in the text, not a row of Table 8 (it starts from the pretrained model and has one round). Nothing is said of these pairs after warm-up rounds or on Spider |
| B6 | The weights of the server average. The adapters that the clients send in the first preference round are averaged again by question counts and with equal weights; EX is level with the average by pair counts | 3 rounds: `\ex{bird}{reaggq}{3}`, `\gain{bird}{k2}{3}{reaggq}{3}`, p = `\pval{bird}{k2}{3}{reaggq}{3}`; `\ex{bird}{reagge}{3}`, `\gain{bird}{k2}{3}{reagge}{3}`, p = `\pval{bird}{k2}{3}{reagge}{3}`; the same with `spider` | one or two sentences: no significant difference among the three weightings, said of what was done: the adapters of one preference round averaged again. Nothing is said of other weights over several rounds, where the global model that the clients sample from would change too. This is not worded as "the weights do not change EX": a difference that is not significant is not shown to be absent. How far the weights move is known: the largest change of one client's weight against the weights by pair counts is `\fact{weights.bird.questions.max_shift}` percentage points (question counts) and `\fact{weights.bird.equal.max_shift}` (equal weights) on BIRD, `\fact{weights.spider.questions.max_shift}` and `\fact{weights.spider.equal.max_shift}` on Spider; give what the reader needs to judge the rows. No gain is stated for the weights by pair counts; nothing is trained again in these rows |
| B7 | Clients pooled in the preference rounds: from the same model after the two warm-up rounds, the preference rounds run on the training data of the five clients held at one site, as one client, so that nothing is averaged. The row is not a part of the method: it is the same rounds without the federation, and it shows what the preference rounds lose by running at five clients with a server average. Spider only; waits | `\ex{spider}{pooled}{4}`, `\gain{spider}{k2}{4}{pooled}{4}`, p = `\pval{spider}{k2}{4}{pooled}{4}` | one or two sentences that say what the row is for, what it is and what it is compared with; they hold whatever the row shows. Where the sentences stand is yours; the reader of the first draft met the row inside the paragraph on the weights without knowing why it was there |

The step of the second preference round (B2 of the claims) is in
Section 5.1. Here it is at most a clause that places the first block
(two preference rounds) beside the second (one).

## Table 8

`table` environment, `\caption{...}\label{tab:ablation}` above,
`\input{generated/tab_ablation}`.

| Part | Content |
|---|---|
| first row | FedAvg SFT after 2 rounds: the model from which every row but the two on the warm-up rounds starts its preference rounds. EX only; it has no test |
| blocks | headed "4 rounds" and "3 rounds". For `\method` these are 2 warm-up rounds with 2 preference rounds and with 1; the caption or the text says so. Each block opens with `\method` at that number of rounds |
| rows, first block | Fixed pairs and reference; Without the preference term; No warm-up round; Three warm-up rounds; Clients pooled (Spider only) |
| rows, second block | Without the NLL term; Without the preference term; Averaged by question count; Averaged with equal weights |
| columns | per dataset (BIRD dev, Spider test): EX; $\Delta$: difference in EX to `\method` of the block; $p$: exact McNemar test against that row, unadjusted, asterisk when significant after the Holm correction over the comparisons of the table (Section 4.6). The caption says what $\Delta$, $p$ and the asterisk are |
| rows with the same total | "No warm-up round" has 4 preference rounds, "Three warm-up rounds" 3 warm-up rounds and 1 preference round: the caption or the text says that the total stays at 4 |
| `--` | a row that is not run yet; an empty cell: the row is not planned for that dataset |

## Published results on the likelihood term

For the one sentence of credit under B3. Facts from the papers
themselves, with locators (`briefs/02_related_rows.md`); their numbers
are not typed in this section.

| Paper (key) | What it reports | Locator |
|---|---|---|
| CodeLutra (`tao2024codelutra`) | with the DPO term alone, without the likelihood term on the correct samples, accuracy on Spider falls far below the full loss; the paper calls the term a regularization | Sec. 5.3, "Importance of SFT regularization during preference optimization", Table 2, p. 9 |
| Pang et al. (`pang2024irpo`) | on GSM8K, one iteration with standard DPO is well below one iteration with the DPO and NLL loss on the same pairs; "NLL loss is necessary in our method" | Sec. 3.1, p. 6; Table 1, p. 5 |
| Liu et al. (`liu2025cotdpo`) | their loss is the DPO loss alone; an added SFT term on the correct samples, tried for outputs that are SQL only, gave a limited gain | App. A, Table 7, p. 12 |
| Lanchantin et al. (`lanchantin2025bridging`) | adding an NLL term gave no benefit in their tasks | Sec. 4.2 |

The first two report the same direction as our row. The last two are
here so that the sentence is not worded more generally than the
literature allows; whether they are named is yours.

## Macros

Text mode; a signed gain prints its sign. The full list with values:
`generated/numbers.md`.

| Macro | Prints |
|---|---|
| `\ex{set}{line}{round}` | EX in percent, two decimals, without the percent sign. `set`: `bird`, `spider` (and `spiderdev`, `syn`, `realistic`, `dk` for Table 6). `line`: `k2` (`\method`), `fedavg`, `fixed`, `feddpo` (round 3: without the NLL term), `rft` (without the preference term), `k0`, `k3`, `pooled`, `reaggq` (averaged by question count), `reagge` (equal weights), `k0gold` (round 1 of `k0` with the gold SQL query as the correct side for the questions without a correct sample; compare with `k0` at round 1) |
| `\gain{set}{a}{ra}{b}{rb}` | EX of row b minus EX of row a, signed; `\gap{...}` the same without sign. In this section a is `k2`, except `\gain{bird}{k0}{1}{k0gold}{1}` |
| `\pval{set}{a}{ra}{b}{rb}`, `\padj{...}` | exact McNemar p of that comparison; its Holm-adjusted value. Where a p below `\fact{test.alpha}` is called not significant, the adjusted value beside it spares the reader a stop |
| `\errpval{set}{a}{ra}{b}{rb}`, `\errpadj{...}` | the same test on execution errors (a question counts when its prediction ends in an execution error in one row only), and its adjusted value. Defined for `{bird}{k2}{3}{rft}{3}` and `{spider}{k2}{3}{rft}{3}` |
| `\wrpval{set}{a}{ra}{b}{rb}`, `\wrpadj{...}` | the same test on incorrect results, for the same two comparisons |
| `\nfix{...}`, `\nbrk{...}` | questions correct in b and not in a; correct in a and not in b |
| `\nerr{set}{line}{round}`, `\nwr{set}{line}{round}` | predictions with an execution error; with an incorrect result |
| `\ts{set}{line}{round}`, `\tsgain{...}`, `\tsgap{...}`, `\tspval{...}` | the same for test-suite accuracy (Table 6); `\tsgap` is the difference without sign |
| `\fact{warmup.<set>.k<w>.no_correct}` | training questions none of whose samples is labeled correct at the first preference round, with `w` warm-up rounds before it (`bird`: 0, 2; `spider`: 0, 2, 3); questions on databases without rows are not counted |
| `\fact{train.<set>.with_rows}`, `\fact{train.<set>.no_rows}` | training questions on databases with rows; on databases without rows (BIRD has none) |
| `\fact{weights.<set>.questions.max_shift}`, `\fact{weights.<set>.equal.max_shift}` | largest change of one client's weight in the server average, in percentage points, from the weights by pair counts to those by question counts and to equal weights |
| `\fact{cost.<set>.pref1.questions}` | the training questions of the five clients |

## Wording that holds for the whole section

| | |
|---|---|
| p-values | significance is always after the correction. A $p$ in the text is unadjusted, as in the tables, unless it is marked as adjusted; the section says so once. An adjusted value is quoted where an unadjusted one below `\fact{test.alpha}` is not significant |
| sets | the sets by their names: BIRD dev, Spider test |
| seeds | one training seed; significance is the test of Section 4.6 |
| comparisons | every row against `\method` at the same number of rounds, inside one setup |
| the model | "the model" or its name; the two kinds of incorrect prediction are "execution error" and "incorrect result" |
| a part and its row | what a part adds is what its row shows on the set where it shows; a result that holds on one dataset is stated for that dataset |
| causes | a row shows what removing a part does; why it does so is Section 7's, or a conjecture marked as one |

## Labels available

Of this section: `sec:ablation`, `tab:ablation`.

Of other sections: `sec:related`, `sec:rel-pref`, `sec:method`,
`sec:warmup`, `sec:pref-round`, `sec:cost`, `sec:setup`,
`sec:baselines`, `sec:stat-test`, `sec:results`, `sec:rq1`, `sec:rq3`,
`sec:rq4`, `tab:main`, `tab:robust`, `tab:cost`, `fig:rounds`,
`fig:errors`, `sec:discussion`.

## Paragraph roles (an offer)

One paragraph per part: what the row removes or replaces, the number
with its comparison, and what the number says about the part. The
order of Section 3 (warm-up rounds, then the parts of a preference
round, then the server) or the order of Table 8 both serve.
