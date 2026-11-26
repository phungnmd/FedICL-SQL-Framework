# Outline: Section 6, Ablation study

One line per paragraph, in order. "Serves" names the statement of the
brief (B1, B3 to B8; a promise of an earlier section by its place).
Words are running text; the caption is not counted. Total 790. The
lines are notes, not sentences of the paper; a value in brackets is
what the macro prints today.

One heading, `\section{Ablation study}\label{sec:ablation}`, and no
subsection. Order: how to read Table 8, then the parts of a preference
round (renewal of pairs and reference, NLL term, preference term), then
the warm-up rounds, then the server. The first three rows read are the
ones Sections 4.4 and 5.1 announced through FedDPO, so the section
opens where Section 5 left the reader.

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | How Table 8 is read. Each row removes or replaces one part of `\method`. Every row starts from the model `\method` starts its preference rounds from, FedAvg SFT after $T_w$ = 2 rounds, except the two rows that change $T_w$. Each row is tested against `\method` at the same number of rounds: the upper block after four rounds (two preference rounds), the lower after three (one preference round); one clause that Section 5.1 gave the step between the two. The convention of Section 5 in one sentence: "significant" is after the correction, the $p$-values quoted are unadjusted | promise of 4.6; frame of all B | Table 8 (`tab:ablation`), placed after this paragraph; `\setting{rounds.warmup}`; `sec:stat-test`, `sec:rq1` | 80 |
| 2 | Renewing the pairs and the reference model: on BIRD dev the second preference round needs it. FedDPO differs from `\method` in two ways (Section 4.4); this row isolates the first. "Fixed pairs and reference": in the second preference round the clients train again on the pairs of the first, against the reference model of the first; the NLL term stays, and the first preference round is that of `\method`, so the two rows differ in the second preference round only. BIRD dev: the two EX values, the difference, the test read through its counts (questions correct only with `\method` against only with the row), $p$, significant. One reading sentence from two cells of Table 8: the row ends at the EX `\method` has after one preference round (see editor's point 2). Spider test: the two EX values, level, $p$ | B1; promises of 2.2, 3.4, 4.4, 5.1 | `\ex{bird}{fixed}{4}` [46.15], `\ex{bird}{k2}{4}` [48.76], `\gap{bird}{k2}{4}{fixed}{4}` [2.61], `\nbrk{...}` [85], `\nfix{...}` [45], `\pval{...}` [5.7e-4]; `\ex{bird}{k2}{3}` [46.22]; `\ex{spider}{fixed}{4}` [78.02], `\ex{spider}{k2}{4}` [78.20], `\pval{spider}{k2}{4}{fixed}{4}` [0.78]; `sec:baselines` | 120 |
| 3 | The NLL term: without it, a preference round brings no gain on Spider test. The second difference of FedDPO. "Without the NLL term" is one preference round with the preference term alone; at this round the pairs and the reference model are those of `\method`, so the NLL term is the only difference. The row is FedDPO after its first preference round; the FedDPO row of Table 3 is the same training one round later, on the same pairs and reference. Spider test: EX of the row against `\method`, the difference, $p$, significant; beside it the EX of the model before the round, which the row does not reach (two numbers, no test). BIRD dev: the same comparison by macro, direction and size left to the numbers (waits). One sentence of credit: CodeLutra on Spider and Pang et al. on GSM8K report a loss of accuracy with the DPO term alone, relative to the loss with both terms, in training at one site; worded as what they report | B3; promises of 2.2, 3.4, 4.4, 5.1 | `\ex{spider}{feddpo}{3}` [73.59], `\ex{spider}{k2}{3}` [77.46], `\gap{spider}{k2}{3}{feddpo}{3}` [3.87], `\pval{...}` [7.6e-9]; `\ex{spider}{fedavg}{2}` [74.10]; `\ex{bird}{feddpo}{3}`, `\gain{bird}{k2}{3}{feddpo}{3}`, `\pval{...}`, `\ex{bird}{fedavg}{2}` [42.70]; `\cite{tao2024codelutra}`, `\cite{pang2024irpo}`; `tab:main` | 130 |
| 4 | The preference term: without it, more execution errors remain. The converse row. "Without the preference term" trains with the NLL term alone on the correct sample of each pair: the samples, labels, pairs, settings and server weights of a preference round, so that execution still selects the targets but no incorrect sample enters the loss. After three rounds: execution errors of the row against `\method` on both sets; incorrect results of the row against `\method` on both sets, where `\method` has the larger count; all four as counts of predictions, nothing on which questions moved. EX is lower on both datasets (difference and $p$ each), neither significant after the correction. The same row after four rounds, upper block: EX, difference, $p$ and execution errors by macro (waits) | B4; promises of 3.4, 4.4 | `\nerr{bird}{rft}{3}` [248], `\nerr{bird}{k2}{3}` [102], `\nerr{spider}{rft}{3}` [153], `\nerr{spider}{k2}{3}` [99]; `\nwr{bird}{rft}{3}` [605], `\nwr{bird}{k2}{3}` [723], `\nwr{spider}{rft}{3}` [365], `\nwr{spider}{k2}{3}` [385]; `\ex{bird}{rft}{3}` [44.39], `\gain{bird}{k2}{3}{rft}{3}` [-1.83], `\pval` [0.057]; `\ex{spider}{rft}{3}` [75.87], `\gain` [-1.59], `\pval` [0.015]; `\ex{bird}{rft}{4}`, `\gain{bird}{k2}{4}{rft}{4}`, `\pval`, `\nerr{bird}{rft}{4}`, the same for `spider`; `sec:rq4` | 130 |
| 5 | The number of warm-up rounds: EX on Spider test does not depend on it at the same total; test-suite accuracy does. The two rows: "No warm-up round" (four preference rounds, the first sampling from the pretrained model) and "Three warm-up rounds" (one preference round), the total kept at four. Spider test: the three EX values, neither difference significant (the two $p$). BIRD dev: the two rows by macro (waits). Under TS (Table 6, Section 5.3) the variant without warm-up rounds is below `\method` on the three sets with test suites (the three differences, the $p$ of Spider dev; significant on Spider-Syn): without warm-up rounds the EX gain over FedAvg SFT does not carry over to TS, with two it does. Spider-DK, which has no test suite: EX is higher without warm-up rounds (difference, $p$), not significant after the correction | B5; promises of 3.3, 5.3 | `\ex{spider}{k0}{4}` [78.02], `\ex{spider}{k2}{4}` [78.20], `\ex{spider}{k3}{4}` [77.97], `\pval{spider}{k2}{4}{k0}{4}` [0.85], `\pval{spider}{k2}{4}{k3}{4}` [0.74]; `\ex{bird}{k0}{4}`, `\gain{bird}{k2}{4}{k0}{4}`, `\pval`, `\ex{bird}{k3}{4}`, `\gain`, `\pval`; `\tsgain{spiderdev}{k0}{4}{k2}{4}` [+3.20], `\tspval` [0.01], `\tsgain{syn}{...}` [+4.16], `\tsgain{realistic}{...}` [+5.11]; `\gap{dk}{k0}{4}{k2}{4}` [3.55], `\pval{dk}{k0}{4}{k2}{4}` [0.032]; `tab:robust`, `sec:rq3` | 120 |
| 6 | The questions without a correct sample: the warm-up rounds leave fewer of them, and taking the gold SQL query as the correct side of a pair for them does not raise EX. The counts of training questions none of whose $N$ samples is labeled correct at the first preference round: BIRD from the pretrained model and after two warm-up rounds, of the questions of the five clients; Spider from the pretrained model, after two and after three. Counts of such questions only, no statement on pairs. A preference round constructs no pair for these questions; the warm-up rounds are how `\method` uses their gold SQL query. The variant: $M$ pairs per such question from the gold SQL query and an incorrect sample, tried on BIRD without warm-up rounds, where these questions are most numerous, in one preference round on the same samples and labels. EX with these pairs against without, not significant after the correction ($p$); execution errors fall and incorrect results rise by more (the two pairs of counts) | B5 (counts), B8; promise of 3.3 | `\fact{warmup.bird.k0.no_correct}` [4035], `\fact{cost.bird.pref1.questions}` [9428], `\fact{warmup.bird.k2.no_correct}` [2698]; `\fact{warmup.spider.k0.no_correct}` [1074], `\fact{cost.spider.pref1.questions}` [8659], `\fact{warmup.spider.k2.no_correct}` [573], `\fact{warmup.spider.k3.no_correct}` [483]; `\ex{bird}{k0gold}{1}` [39.24], `\ex{bird}{k0}{1}` [41.85], `\pval{bird}{k0}{1}{k0gold}{1}` [0.0073]; `\nerr{bird}{k0}{1}` [219], `\nerr{bird}{k0gold}{1}` [105], `\nwr{bird}{k0}{1}` [673], `\nwr{bird}{k0gold}{1}` [827]; `sec:warmup` | 125 |
| 7 | The server: the weights of the average do not change EX, and one row removes the federation from the preference rounds. The adapters that the clients send in the first preference round are averaged again by question counts, as in a warm-up round, and with equal weights; no client trains again. On both datasets the two rows are within about half a point of the average by pair counts and no difference is significant (the largest difference with its $p$, the rest left to Table 8). "Clients pooled", Spider only: from the model after the two warm-up rounds, the preference rounds run on the training data of the five clients held at one site; EX, difference to `\method` and $p$ by macro (waits) | B6, B7; promise of 3.4 | `\gain{spider}{k2}{3}{reagge}{3}` [-0.52], `\pval` [0.09]; (in the table: `reaggq` and `reagge`, both sets); `\ex{spider}{pooled}{4}`, `\gain{spider}{k2}{4}{pooled}{4}`, `\pval`; `sec:pref-round` | 85 |

No closing paragraph: each paragraph ends on what its row shows, and
the interpretation is Section 7's.

## Float and caption

| Float | Placed after | The caption says |
|---|---|---|
| Table 8 | paragraph 1 | EX (%) on BIRD dev and Spider test of `\method` and of its variants, each with one part removed or replaced; a variant is compared with `\method` at the same number of rounds, the first row of its block. $\Delta$: difference in EX to that row; $p$: unadjusted $p$-value of the exact McNemar test against it; asterisk: significant at the `\fact{test.alpha}` level after the Holm correction over the comparisons of the table. "No warm-up round" has four preference rounds and "Three warm-up rounds" three warm-up rounds and one preference round, so that both total four rounds. "Clients pooled" is run on Spider only |

## For the editor

1. Order. Neither of the two offered orders exactly: the parts of a
   preference round come first (B1, B3, B4), then the warm-up rounds
   (B5, B8), then the server (B6, B7). In the order of Section 3 the
   section would open on rows whose EX is level.
2. B1, one sentence beyond the listed evidence. On BIRD dev the row
   after four rounds has 46.15 and `\method` after three has 46.22:
   the second round on the pairs of the first adds nothing, where the
   renewed round adds 2.54 (Section 5.1). Both cells are in Table 8,
   but the brief does not list this comparison and it has no test. I
   plan one sentence that sets the two EX values side by side, without
   a word on significance. Say if it should go.
3. B3, worded under the ceiling. The row is 0.51 points below the
   model before the round (73.59 against 74.10), without a test, while
   paragraph 7 treats 0.52 points on the same set ($p$ = 0.09) as no
   difference. I plan "brings no gain: 73.59 against 74.10 before the
   round" and leave "lowers" to the tested comparison with `\method`
   (3.87 points).
4. B3, the credit. CodeLutra and Pang et al. are named; Liu et al. and
   Lanchantin et al. are not. The sentence says what the two report and
   in which tasks, and nothing general about the term.
5. B4, an optional clause. The execution errors of the model before
   the round, `\nerr{bird}{fedavg}{2}` [286] and
   `\nerr{spider}{fedavg}{2}` [183], show that the NLL term on the
   correct samples removes few of them (to 248 and 153) and both terms
   most (to 102 and 99). The brief does not list them under B4;
   Section 5.4 quotes the first. I leave them out unless wanted (about
   15 words).
6. B5 is two paragraphs: 5 reads the rows and the test-suite result, 6
   holds the counts and B8. The variant without warm-up rounds is then
   known when B8 uses it, and the counts do not stand beside the
   test-suite sentence.
7. Promise of Section 2.2 ("varies all three of these choices"). The
   row fixes the pairs and the reference model together; the reference
   model is not varied alone. Paragraph 2 says "the pairs and the
   reference model" and makes no separate claim for either.
8. Table 8. (a) The heading of the upper block, "2 warm-up rounds, 2
   preference rounds", does not hold for the two rows on the warm-up
   rounds; the caption says so. (b) The caption does not explain `--`,
   since the mark leaves with the last row. (c) Paragraph 3 quotes the
   EX of the model before the preference rounds, which the table does
   not show; a row "FedAvg SFT, 2 rounds" at the head of the lower
   block would put it there, if you want it.
9. Sentences that wait: BIRD in paragraph 3, the four-round row in
   paragraph 4, BIRD in paragraph 5, the pooled row in paragraph 7.
   Each states what is compared and prints its macros; paragraphs 3 and
   5 keep their first sentence on Spider test.
