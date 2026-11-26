# Outline: Section 7, Discussion and limitations, and Section 8, Conclusion

One line per paragraph, in order. "Serves" names the statement of the
brief (S1 to S4: the statements of Section 7; L1 to L8: its
limitations; C1 to C3: the statements of Section 8). Words are running
text. Section 7 totals 700, Section 8 totals 180. The lines are notes,
not sentences of the paper; a value in brackets is what the macro
prints today.

## Section 7

`\section{Discussion and limitations}\label{sec:discussion}` with two
subsections and no text between the heading and the first of them, as
in Sections 3 and 5:
`\subsection{Interpretation of the results}\label{sec:interpretation}`
(paragraphs 1 to 4) and
`\subsection{Scope and limitations}\label{sec:limitations}`
(paragraphs 5 to 7).

Order of 7.1: the outcome against FedAvg SFT first, since Section 5.4
hands its paired predictions to this section; then the two preference
rounds, which say when the outcome arises; then the two terms of the
loss, which say from which part; then the warm-up rounds. Each
paragraph names the result it reads and marks the reading as one.

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 1 | The gain over FedAvg SFT is a gain in queries that execute, and executing is necessary for a correct result but not sufficient. After four rounds `\method` has about half the execution errors of FedAvg SFT on both sets and no fewer incorrect results; this is said plainly, with a reference to Section 5.4 and Fig. 3 and without the totals. The paired predictions: of the questions that only `\method` answers correctly on BIRD dev, about as many had an incorrect result with FedAvg SFT as an execution error (the two counts); part of the former execution errors now execute and return another result (one count, referred to, Spider left to Section 5.4). The reading in one sentence: the method corrects both kinds of incorrect prediction, and the incorrect results are refilled by queries that formerly failed to execute | S3; promise of 5.4 | `\fact{moved.bird.wrong.correct}` [78], `\fact{moved.bird.error.correct}` [75]; `sec:rq4`, `fig:errors` | 105 |
| 2 | What a preference round changes follows the incorrect samples of its pairs. First preference round: on BIRD, the pairs whose incorrect sample has an execution error, as a count of the pairs of the round with its percentage; on Spider the percentage. That round lowers the execution errors on both evaluation sets (BIRD dev before and after, the rest in Fig. 3). Second preference round on BIRD: the same count and percentage, so that three quarters of the pairs set a correct sample against one with an incorrect result; in that round the incorrect results on BIRD dev fall (two values) and the execution errors do not fall further. On Spider the share changes less (percentage), and the second round changes the predictions on Spider test little. Worded as "consistent with" what on-policy pairs are for (Section 3.4: the pairs of a round reflect the errors the current global model makes); two rounds on two datasets, no tested relation. Optional last clause on the row "Fixed pairs and reference" of Table 8 (editor's point 2) | S1 | `\fact{pairs.bird.pref1.neg_error}` [6616], `\fact{cost.bird.pref1.pairs}` [11754], `\fact{pairs.bird.pref1.neg_error_pct}` [56], `\fact{pairs.spider.pref1.neg_error_pct}` [51]; `\nerr{bird}{fedavg}{2}` [286], `\nerr{bird}{k2}{3}` [102]; `\fact{pairs.bird.pref2.neg_error}` [1788], `\fact{cost.bird.pref2.pairs}` [7066], `\fact{pairs.bird.pref2.neg_error_pct}` [25]; `\nwr{bird}{k2}{3}` [723], `\nwr{bird}{k2}{4}` [658]; `\fact{pairs.spider.pref2.neg_error_pct}` [43]; `sec:pref-round`, `fig:errors` | 125 |
| 3 | The two terms of the loss do different work. A round with the NLL term alone on the correct samples ends above the model before it in EX (BIRD dev, the two values of Table 8, said to be values without a test): execution already helps by selecting the targets. What the preference term adds is the use of the incorrect samples: with it, significantly fewer predictions end in an execution error (the two counts on BIRD dev, no p-value repeated), on BIRD dev significantly more return an incorrect result, and a difference in EX between the two is not established after one round. The preference term alone brings no gain on Spider test (Section 6), which agrees with what CodeLutra and Pang et al. report at one site and with the reason Section 3.4 gives for the NLL term: the preference term constrains the two samples of a pair only relative to each other. Nothing says that the preference term raises EX over the NLL term alone | S2 | `\ex{bird}{rft}{3}` [44.39], `\ex{bird}{fedavg}{2}` [42.70]; `\nerr{bird}{k2}{3}` [102], `\nerr{bird}{rft}{3}` [248]; `\cite{tao2024codelutra}`, `\cite{pang2024irpo}`; `sec:ablation`, `tab:ablation`, `sec:pref-round` | 110 |
| 4 | The warm-up rounds do not show in EX on Spider test; they show in the training questions without a correct sample and in TS. The counts at the first preference round, without and with the two warm-up rounds (Spider; BIRD if the words allow). Without warm-up rounds the variant is above FedAvg SFT in EX and below it in TS on the three sets with test suites, a comparison of values; against `\method` its lower TS is significant on Spider-Syn only. The reading, marked as one: an execution label on one database also accepts a query that returns the gold result there without being equivalent to the gold SQL query, and TS is the stricter check; the warm-up rounds train on the gold SQL query of every question before any such label is used. No sentence joins the counts to the TS result as cause. Spider-DK, which has no test suite, in one clause: EX is higher without warm-up rounds, not significantly, and the reading cannot be checked there | S4 | `\fact{warmup.spider.k0.no_correct}` [1016], `\fact{warmup.spider.k2.no_correct}` [557]; `\fact{warmup.bird.k0.no_correct}` [4035], `\fact{warmup.bird.k2.no_correct}` [2698]; `\cite{zhong2020testsuite}`; `tab:robust`, `sec:rq3`, `sec:ablation`, `sec:warmup` | 115 |
| 5 | The setting the study covers. A client holds gold SQL queries for its questions and databases on which it can execute queries; questions without gold SQL are not used. Five clients, ten in one setup, all of which take part in every round; partial participation and larger numbers of clients are not studied. The data stay at the clients: this is data isolation and not differential privacy, and nothing is claimed about what an adapter reveals | L1, L2, L3 | `sec:setting`, `sec:fed-setups` | 75 |
| 6 | The execution label and the metric. A label is the equality of two execution results on one database: an incorrect query can return the gold result there, and a question on a database without rows yields no pair. EX has the same limit on the evaluation database (Section 5.4 reports correct predictions that read other tables or columns than the gold SQL query). The check the paper has is TS on Spider dev and two perturbed sets; BIRD has no test suite, so the BIRD results are in EX alone | L5 | `sec:pref-round`, `sec:rq3`, `sec:rq4` | 70 |
| 7 | The size of the study and its cost. Models of 0.5B to 1.5B parameters with LoRA, SQLite databases, questions in English. The number of warm-up rounds is a setting, held at two for every model; with the model of 0.5B parameters the gain is smaller (editor's point 4 for the clause on why). One training seed for most rows and one draw of each client partition: the test of Section 4.6 speaks of the evaluation questions and not of the variation between training runs; the two main rows on BIRD have a second seed (Table 3), named without its numbers. The cost is client computation: the four factors of Table 7 against an SFT round, communication unchanged | L7, L8, L6, L4 | `\fact{cost.bird.pref1.ratio}` [2.7], `\fact{cost.bird.pref2.ratio}` [2.3], `\fact{cost.spider.pref1.ratio}` [1.6], `\fact{cost.spider.pref2.ratio}` [0.9]; `sec:rq2`, `sec:stat-test`, `tab:main`, `tab:cost` | 100 |

## Section 8

`\section{Conclusion}\label{sec:conclusion}`, no subsection, two
paragraphs.

| # | Point of the paragraph | Serves | Carries | Words |
|---|---|---|---|---|
| 8 | What the paper did and what it found. `\method` is a federated training method for Text-to-SQL in which the clients use their databases as supervision: after warm-up rounds of FedAvg SFT, each client samples queries from the global model, labels them by execution against the gold SQL query and trains on preference pairs of correct and incorrect samples. At the same number of rounds the model is above FedAvg SFT on BIRD dev (the gain) and on Spider test; the execution errors fall by about half and the incorrect results do not fall; the communication is that of FedAvg SFT and the cost is computation at the clients | C1, C2 | `\gap{bird}{fedavg}{4}{k2}{4}` [6.19] | 115 |
| 9 | What is open, as directions and each from a limitation of Section 7: stricter execution labels, for example on several instances of a client's database (L5); questions for which a client has no gold SQL query (L1); more clients and partial participation (L2). Nothing is said to be under way | C3 | none | 65 |

## For the editor

1. Order of 7.1. The brief numbers the readings 1, 2, 3, 4; I plan
   3, 1, 2, 4. Section 5.4 ends on the paired predictions and sends the
   reader here, so the section opens where Section 5 left off, with
   the outcome after four rounds. The two preference rounds then say
   when that outcome arises and the two terms from which part of the
   loss. In the brief's order the section would open on the pairs by
   kind, which are new numbers, before the reader has the outcome
   they are meant to explain.
2. S1, one clause beyond the listed evidence. Section 6 reports that
   on BIRD dev the second round on the pairs of the first ends at
   `\ex{bird}{fixed}{4}` [46.15], against `\ex{bird}{k2}{3}` [46.22]
   after one preference round, while the renewed round reaches
   `\ex{bird}{k2}{4}` [48.76]. That row is the nearest thing the paper
   has to a check of the reading of paragraph 2, and a reviewer will
   connect the two. I plan one closing clause that refers to the row
   without its numbers ("consistent with"), and no statement on which
   of the two fixed parts matters, as Section 6 has it. Say if it
   should go.
3. L4, the factor on Spider. `\fact{cost.spider.pref2.ratio}` prints
   0.9: the second preference round on Spider takes less client time
   than an SFT round. "A preference round takes more client compute
   than an SFT round" is therefore not true of every round. I plan to
   say that the additional cost of the method is client computation
   and to give the four factors, which carry the exception themselves.
   The clause "the cost is client compute" of the Conclusion (C2)
   holds as it stands: the two preference rounds on Spider together
   take 2.5 SFT rounds against 2.
4. L8, the reason for the smaller gain. The brief says the gain is
   smaller "where FedAvg SFT is still improving fast, as with the
   model of 0.5B parameters". Section 5.2 does not say this, and
   `generated/numbers.md` has the 0.5B model only before training and
   after four rounds, so the paper holds nothing on its rounds. I plan
   to state the two facts the paper has (the number of warm-up rounds
   was held at two for every model; the gain with the 0.5B model is
   smaller, Table 4) and to leave the cause out. If you want the
   cause, give me either a macro for the EX of FedAvg SFT by round
   with that model or the wording as a conjecture.
5. S4, one step in the reading. The brief gives the reading as: an
   execution label on one database also accepts a query that is not
   equivalent to the gold SQL query, and TS is the stricter check. To
   make it a reading of the warm-up rounds, the paragraph needs one
   more clause: the warm-up rounds train on the gold SQL query of
   every question before any execution label is used. That clause is
   a fact of Section 3.3; the sentence joins the two with "one reading
   is" and "may", and the counts stay in their own sentence.
6. L5, a reference to Section 5.4. I plan one clause that points to
   the correct predictions that read other tables or columns than the
   gold SQL query (the `form.*` counts of Section 5.4), without a
   number: it is the paper's own evidence of the limit of EX. The
   brief does not list it under L5; say if it should go.
7. Citations. The brief gives no keys. I use three, each for what an
   earlier section already cites it for: `tao2024codelutra` and
   `pang2024irpo` (a lower accuracy with the DPO term alone, as in
   Section 6) and `zhong2020testsuite` (TS as the stricter metric, as
   in Section 4.1). No other work is cited.
8. Numbers. Section 7 prints about twenty macros: the pairs by kind
   as counts (new here), three pairs of values that Sections 5 and 6
   already report, the four counts of questions without a correct
   sample (the BIRD pair goes first if words are short) and the four
   cost factors. Under S3 only two counts are repeated, as the ceiling
   asks. Section 8 prints one.
9. Labels. The two subsections take `sec:interpretation` and
   `sec:limitations`, which are new; no other section refers to them
   yet.
10. Section 8, C1 "as in the Introduction". The Introduction is not
    drafted (`sections/01_intro.tex` is empty), so paragraph 8 is
    worded from Sections 3.2 and 3.4 and from the terms of the brief.
    When the Introduction is written, the two descriptions of the
    method should be read side by side once.
11. Sentences that wait. One: the second seed on BIRD in paragraph 7,
    named as a comparison and left to Table 3. The paragraphs on the
    two terms and on the warm-up rounds are bounded to the sets whose
    rows are in (BIRD dev and Spider test after one preference round;
    Spider test and the Spider sets for the warm-up rounds), so they
    hold whatever the waiting rows of Table 8 show.
