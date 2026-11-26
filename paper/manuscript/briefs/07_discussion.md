# Brief: Section 7, Discussion and limitations, and Section 8, Conclusion

Kind of section: discussion and conclusion (`voice/discussion.md`).
Outline to: `briefs/07_discussion_outline.md` (both sections). Drafts
to: `sections/07_discussion.tex` and `sections/08_conclusion.tex`.
Notes to: `briefs/07_discussion_notes.md`.

Entries below are notes in shorthand, not sentences for the paper.

## Place in the paper

| | |
|---|---|
| Headings | `\section{Discussion and limitations}\label{sec:discussion}`; `\section{Conclusion}\label{sec:conclusion}`. Subsections in Section 7 are yours to use (for example the interpretation and the limitations); none in Section 8 |
| Before them | Section 5 (`sec:results`) reports the results by research question; Section 5.4 ends its paragraph on the paired predictions with "Section 7 returns to them". Section 6 (`sec:ablation`) reports what each row of Table 8 shows and leaves the interpretation to Section 7 |
| After them | the declarations and the appendices |
| Floats | none |
| Purpose | Section 7: interpret the results of Sections 5 and 6 and state the scope of the study. Section 8: the contribution in a few sentences and the open directions |
| Length | Section 7: about 700 words, 780 at most. Section 8: about 180 words, 200 at most |

## Section 7: statements to establish

The first three are interpretation. Each is worded as a reading of
results that the earlier sections report, with the result named; none
is a new result, and none is stated as shown.

| # | Claim | Evidence (macros; the sections that report it) | Ceiling |
|---|---|---|---|
| 1 | What the pairs of the two preference rounds contain, and what holds of it on both datasets. In the first preference round more than half of the pairs have a sample with an execution error as their incorrect side, and that round removes execution errors on both evaluation sets. By the second, such pairs are few (BIRD: a quarter of the pairs), while the pairs with an incorrect result as their incorrect side are about as many as before on BIRD; the second round no longer lowers the execution errors on BIRD dev, and what it changes differs between the two sets | The pairs by the kind of their incorrect sample, as counts of both kinds: BIRD `\fact{pairs.bird.pref1.neg_error}` and `\fact{pairs.bird.pref1.neg_wrong}` of `\fact{cost.bird.pref1.pairs}`, then `\fact{pairs.bird.pref2.neg_error}` and `\fact{pairs.bird.pref2.neg_wrong}` of `\fact{cost.bird.pref2.pairs}`; Spider `\fact{pairs.spider.pref1.neg_error}` and `\fact{pairs.spider.pref1.neg_wrong}`, then `\fact{pairs.spider.pref2.neg_error}` and `\fact{pairs.spider.pref2.neg_wrong}` (percentages: `.neg_error_pct`). Predictions of `\method` by round (Section 5.4, Fig. 3): BIRD dev execution errors `\nerr{bird}{fedavg}{2}`, `\nerr{bird}{k2}{3}`, `\nerr{bird}{k2}{4}`, incorrect results `\nwr{bird}{fedavg}{2}`, `\nwr{bird}{k2}{3}`, `\nwr{bird}{k2}{4}`; Spider test `\nerr{spider}{fedavg}{2}`, `\nerr{spider}{k2}{3}`, `\nerr{spider}{k2}{4}`, `\nwr{spider}{fedavg}{2}`, `\nwr{spider}{k2}{3}`, `\nwr{spider}{k2}{4}` | the first half holds on both datasets and is the statement. No sentence says that the fall of the incorrect results on BIRD dev in the second round follows from the composition of its pairs: the pairs with an incorrect result are about as many in both rounds (5,138 and 5,278) while the incorrect results rise in the first and fall in the second, and the rise of the first is the former execution errors that now execute (statement 3). The row "Fixed pairs and reference" is not used as support: it keeps the pairs, a second pass over them and the reference model together, and on Spider test it runs against the reading |
| 2 | The two terms of the loss. A round on the correct samples alone ends above the model before it in EX (values of Table 8, no test); what the preference term adds is the use of the incorrect samples: with it, significantly fewer predictions end in an execution error, and on BIRD dev significantly more return an incorrect result; a difference in EX between the two is not established after one round | Section 6, the row "Without the preference term": EX `\ex{bird}{rft}{3}` against `\ex{bird}{k2}{3}`, `\ex{spider}{rft}{3}` against `\ex{spider}{k2}{3}`; execution errors `\nerr{bird}{rft}{3}` against `\nerr{bird}{k2}{3}` (p = `\errpval{bird}{k2}{3}{rft}{3}`), `\nerr{spider}{rft}{3}` against `\nerr{spider}{k2}{3}` (p = `\errpval{spider}{k2}{3}{rft}{3}`); incorrect results `\nwr{bird}{k2}{3}` against `\nwr{bird}{rft}{3}` (p = `\wrpval{bird}{k2}{3}{rft}{3}`). Section 6, the row "Without the NLL term": on Spider test below the model before the round | Section 6 has the numbers; here one or two are enough. Nothing beyond what Section 6 establishes: the preference term is not said to raise EX over the NLL term alone. The rows of this variant after four rounds wait; the sentence holds whatever they show |
| 3 | Against FedAvg SFT after four rounds, the gain comes with half the execution errors and with no fewer incorrect results: the paired predictions show that `\method` corrects about as many incorrect results as execution errors, while part of the former execution errors now execute and return another result. Reading: executing is necessary for a correct result and not sufficient | C1: `\nerr{bird}{fedavg}{4}` to `\nerr{bird}{k2}{4}`, `\nerr{spider}{fedavg}{4}` to `\nerr{spider}{k2}{4}`. C2: `\nwr{bird}{fedavg}{4}` against `\nwr{bird}{k2}{4}`, `\nwr{spider}{fedavg}{4}` against `\nwr{spider}{k2}{4}`. Paired predictions (Section 5.4): of the `\nfix{bird}{fedavg}{4}{k2}{4}` questions that only `\method` answers correctly on BIRD dev, `\fact{moved.bird.error.correct}` had an execution error and `\fact{moved.bird.wrong.correct}` an incorrect result with FedAvg SFT; `\fact{moved.bird.error.wrong}` of its execution errors return an incorrect result with `\method` (Spider test: `\fact{moved.spider.error.correct}`, `\fact{moved.spider.wrong.correct}`, `\fact{moved.spider.error.wrong}`) | said plainly: the incorrect results are not fewer than with FedAvg SFT. Section 5.4 has these numbers; here they are referred to, and at most two are repeated |
| 4 | The warm-up rounds. EX on Spider test is level with and without them. What is tested: against `\method`, the variant without them has a lower TS, significant on Spider-Syn only. What is a comparison of values: the variant is above FedAvg SFT in EX and below it in TS on the three sets with test suites; and fewer training questions are without a correct sample after the warm-up rounds | Section 6: the counts `\fact{warmup.bird.k0.no_correct}` and `\fact{warmup.bird.k2.no_correct}`; `\fact{warmup.spider.k0.no_correct}` and `\fact{warmup.spider.k2.no_correct}`; Table 6 and Section 5.3 for TS (`\tsgap{syn}{k0}{4}{k2}{4}`, `\tspval{syn}{k0}{4}{k2}{4}`) | each half is said with what it rests on, and "the effect appears under TS" is not said of three sets when one is significant. A reading is given only with what else the same rows admit: the variant runs four preference rounds where `\method` runs two, so it also has more rounds on execution labels. No sentence says that the counts cause the TS result. Spider-DK, where EX is higher without warm-up rounds, is not passed over if the paragraph speaks of the perturbed sets |

## Section 7: scope and limitations

The limitations the paper states, each once, in your order and
grouping. Where the paper has a check, the check is named with the
limitation.

| # | Limitation | What the paper has |
|---|---|---|
| 1 | A client needs gold SQL queries for its questions and databases on which it can execute queries; questions without gold SQL are not used. The sampled queries are executed on the client's own databases: the implementation opens every database read-only and applies the time limit of the evaluation (`\setting{timeout.bird}`, `\setting{timeout.spider}`); the load on a database in use is outside the study | the setting of Section 3.1; Section 4.1 |
| 2 | Five clients (ten in one setup), all of which take part in every round, simulated from the training set of one benchmark; they differ in domain and schema in every setup, and the skew that is varied is query complexity. Partial participation, more than ten clients and clients from different sources are not studied. The method is not trained beyond `\setting{rounds.total}` rounds (`\setting{rounds.pref}` of them preference rounds); the only line with more preference rounds is the variant without warm-up rounds, which runs four | Section 4.2 |
| 3 | The data stay at the clients; this is data isolation, not differential privacy, and nothing is claimed about what an adapter reveals. The number of pairs a client sends changes with how the model does on its data, which the number of questions does not; with the question counts as weights, Section 6 finds no significant difference in EX | Section 3.5, Section 6 (the row on the server weights) |
| 4 | The additional cost of the method is computation at the clients. Not "every preference round takes more than an SFT round": the second preference round on Spider takes less | `\fact{cost.bird.pref1.ratio}` and `\fact{cost.bird.pref2.ratio}` times an SFT round on BIRD, `\fact{cost.spider.pref1.ratio}` and `\fact{cost.spider.pref2.ratio}` on Spider (Table 7, Section 5.4, where the four are printed; their range is enough here); communication is unchanged |
| 5 | An execution label is the equality of results on one database: an incorrect query can return the gold result there, and a question on a database without rows yields no pair. EX has the same limit on the evaluation database, and the paper has its size: of the correct predictions after four rounds, those that read other tables or columns than the gold SQL query rise more than those that read the same on BIRD dev, and BIRD has no test suite, so the BIRD result is the one without a stricter check | Section 5.4: `\fact{form.bird.fedavg.4.gold_right}` to `\fact{form.bird.k2.4.gold_right}` and `\fact{form.bird.fedavg.4.other_right}` to `\fact{form.bird.k2.4.other_right}` on BIRD dev; `\fact{form.spider.fedavg.4.gold_right}` to `\fact{form.spider.k2.4.gold_right}` and `\fact{form.spider.fedavg.4.other_right}` to `\fact{form.spider.k2.4.other_right}` on Spider test. TS on Spider dev and two perturbed sets (Section 5.3); BIRD has no test suite |
| 6 | One training seed for most rows and one draw of each client partition: the test of Section 4.6 speaks of the evaluation questions, not of the variation between training runs | the second seed of the two main rows on BIRD (Table 3), when it is in |
| 7 | Models of 0.5B to 1.5B parameters with LoRA, SQLite databases, questions in English | Section 4 |
| 8 | The number of warm-up rounds is a setting: it is two for every model and dataset, and other values are tried only in the variants of Section 6. The smaller gain with the model of 0.5B parameters is a result of Section 5.2 and is not set beside this limitation, where it would read as its effect | Section 6, Table 8 |

A limitation is stated as what the study covers and does not cover.
The paper does not grade itself, apologize, or answer an objection
that nobody raised.

## Section 8: statements to establish

| # | Claim | Ceiling |
|---|---|---|
| 1 | What the paper did: a federated training method for Text-to-SQL in which the clients use their databases as supervision, by execution labels on samples of the global model, after warm-up rounds of FedAvg SFT; the loss has a preference term and an NLL term | as in the Introduction; no new claim |
| 2 | What it found, in two or three sentences: above FedAvg SFT at the same number of rounds on BIRD dev and Spider test; the execution errors fall by about half; the incorrect results do not; the cost is client compute | at most one number, the gain on BIRD dev (`\gap{bird}{fedavg}{4}{k2}{4}`); the sets are named |
| 3 | Open directions, two or three, each tied to a limitation of Section 7: stricter execution labels, for example on several instances of a client's database; questions without gold SQL; more clients and partial participation | directions, not promises; nothing is said to be under way |

## Macros

Text mode. The full list with values: `generated/numbers.md`.

| Macro | Prints |
|---|---|
| `\ex{set}{line}{round}`, `\gap{set}{a}{ra}{b}{rb}` | EX in percent, two decimals; the difference of two rows without sign. `line`: `k2` (`\method`), `fedavg`, `rft` (without the preference term) |
| `\nerr{set}{line}{round}`, `\nwr{set}{line}{round}` | predictions with an execution error; with an incorrect result. `fedavg` at round 2 is the model before the preference rounds |
| `\nfix{set}{fedavg}{4}{k2}{4}` | questions that only `\method` answers correctly |
| `\fact{moved.<set>.<with FedAvg SFT>.<with the method>}` | questions by their outcome with FedAvg SFT and with `\method` after four rounds: `correct`, `error`, `wrong` |
| `\fact{pairs.<set>.pref<r>.neg_error}`, `.neg_wrong`, `.neg_error_pct` | preference pairs of preference round `r` whose incorrect sample has an execution error; an incorrect result; the first as a percentage of the pairs |
| `\fact{cost.<set>.pref<r>.pairs}`, `\fact{cost.<set>.pref<r>.ratio}` | pairs of preference round `r`; its client time as a multiple of an SFT round |
| `\fact{warmup.<set>.k<w>.no_correct}` | training questions without a correct sample at the first preference round, with `w` warm-up rounds |
| `\errpval{set}{k2}{3}{rft}{3}`, `\wrpval{set}{k2}{3}{rft}{3}` | the p-values of the tests of Section 6 on execution errors and on incorrect results |

## Wording that holds for both sections

| | |
|---|---|
| interpretation | worded as a reading ("consistent with", "one reading is"), with the result it rests on; a cause is not asserted |
| the model | "the model" or its name; the two kinds of incorrect prediction are "execution error" and "incorrect result" |
| sets | BIRD dev and Spider test by name |
| numbers | few: Sections 5 and 6 have them. Every number is a macro |
| earlier work | where a reading meets a published result, the work is cited for what it reports |

## Labels available

`sec:discussion`, `sec:conclusion`; `sec:method`, `sec:warmup`,
`sec:pref-round`, `sec:cost`, `sec:setup`, `sec:fed-setups`,
`sec:stat-test`, `sec:results`, `sec:rq1`, `sec:rq3`, `sec:rq4`,
`sec:ablation`, `tab:main`, `tab:robust`, `tab:cost`, `tab:ablation`,
`fig:rounds`, `fig:errors`.

## Paragraph roles (an offer)

Section 7: one paragraph per reading (what the preference rounds
change and why the two rounds differ; the two terms; the warm-up
rounds), then the scope and the limitations in two or three
paragraphs grouped by kind (the setting; the labels and the metric;
the size of the study). Section 8: what was done, what was found, what
is open.
