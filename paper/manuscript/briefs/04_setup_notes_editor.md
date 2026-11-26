# Section 4, Experimental setup: checks and editor's notes

Draft: `sections/04_setup.tex`, with the lead-ins and captions of
`sections/A_prompt.tex` and `sections/B_settings.tex`. The writer's
outline: `briefs/04_setup_outline.md`; the writer's notes:
`briefs/04_setup_notes.md`. PDF: `make`, then `build/main.pdf` (Section
4 on pages 6 to 8, the appendices on pages 9, 10 and 13).

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief and the sections already written, and no other
file. One agent wrote the outline, the draft and the revision.

## 1. Outline

The outline covered every statement of the brief and did not depart
from it or from `OUTLINE.md`. Five points went back before the draft:
the difficulty levels of the two evaluation sets get a clause in 4.1;
RQ2 is not on Spider alone (the model of the other family is also run
on BIRD); the rule on 1/K of the databases belongs to the released code
of NIID-Bench, not to its paper; FedDPO is described first in the terms
of OpenFedLLM, then as it is run here; the default system message is a
fact of the chat format of the main model only. The brief was corrected
in these five places.

## 2. Checks of the first draft

| Check | Result |
|---|---|
| Build | compiles in the class of the manuscript, 13 pages; no undefined reference or citation |
| Lint | 1 stop, a number typed by hand ("1.5 billion"); 0 after the macros below. Notes: abbreviations without their long form, which Sections 1 and 2 give |
| Length | 1,182 words of running text (asked: about 1,125, 1,250 at most) |
| Pages | about 2.75 pages against the 2.3 of the plan; Table 2 takes about 0.3 page. The two appendices take about 1.2 pages against 0.8 |
| Macros | three numbers typed by hand replaced by macros: the size of the model (`\setting{model.size}`, new), the fewest databases of a client and the two values of alpha (`\fact{split.*.min_dbs}`, `\fact{split.*.alpha}`, new). One macro prints `??`: the coefficient of FedProx, which waits for its run |
| Terms | those of `TERMS.md`; "the model" throughout |
| Ceilings | kept: no result is quoted, no set is called held-out, the clients are "simulated" |
| Facts | two statements not exact, both from the brief: "every baseline and ablation" on BIRD (the ablation with pooled clients is on Spider only); "the same settings" for the three models (the limit on a training sequence is longer for DeepSeek-Coder) |
| Text taken from the brief | 39% of the words stand in runs of five or more words of the brief (Section 3: 31%, the pilot: 28%). The statements of the brief were too close to sentences, the research questions and Section 4.6 most of all |

Register against the experiment sections of the ten papers (a signal
for the editor, not sent to the writer): sentence length 22.9 words.

## 3. Cold read

A helper on Opus that had seen neither the brief nor the notes read
Section 3 as context and then Section 4 and the appendices as a
reviewer of the journal. It could rerun most of the experiments from
the pages. Its ten findings:

| # | Finding | Weight | What was done |
|---|---|---|---|
| 1 | One training seed for most rows; the McNemar test covers the evaluation questions only; what the second seed is for is not said; one draw of each partition | major | note 3 for the second seed and for which rows are tested. The limits of one seed and one draw belong to Section 7 (the paper states a limitation once); `REVIEW_NOTES.md`, C9 and C15 |
| 2 | No validation split is named: on which data were T, T_w and the learning rates chosen, and were the baselines tuned with the same care | major, a question | not sent: the paper does not tell how a setting was picked. `REVIEW_NOTES.md`, C10 |
| 3 | FedDPO: its settings are given nowhere; its second round trains again on the same pairs against the same reference model; it differs from the method in two things at once; "the global model after them" needed a second reading | major | note 2; the brief now states its settings. The second round on the same pairs is FedDPO as published: `REVIEW_NOTES.md`, C11 |
| 4 | Local and centralized SFT train for 3 epochs, FedAvg SFT for 4 rounds of 1; what the Local SFT row shows for K models is not said; whether the schedule starts again every round | minor | note 2 for Local SFT; Table B1 now says the optimizer and the schedule are new at every client in every round. The budgets: `REVIEW_NOTES.md`, C12 |
| 5 | Table B1 does not hold every setting | minor | Table B1 regenerated (below) |
| 6 | The paragraph on the partition was read twice; no reason for a skew by complexity; the IID setup still differs between clients | minor | note 4; the brief now carries the reason |
| 7 | The rule that reads the query was read three times; its order is not clear | minor | note 1; the brief gives the three steps in order |
| 8 | Which rows are tested is not said; the sentence on the families needed two readings; the mark follows the adjusted p while the table prints the unadjusted one | minor | note 3. The adjusted p of every test goes to the supplementary file (`WRITING_PLAN.md`, section 5) |
| 9 | Alpha names the Dirichlet concentration and the LoRA parameter; "warm-up" names the rounds and the learning-rate schedule; lambda is missing in Table B1; the time limit of the labels points back to evaluation | remark | Table B1 regenerated |
| 10 | The last paragraph of 4.1 reads as an aside; 350 gold SQL queries of BIRD train fail with no comment; 87 and 92 time out in the two rounds; the sentence on difficulty levels is elliptical | remark | note 5 for the paragraph and the levels. The counts: `REVIEW_NOTES.md`, C13 |

Also from its answers: the same prompt for every row is said in 4.4 and
in 4.5; why Spider prompts carry example rows and BIRD prompts do not
(both in note 5).

Table B1 (`tools/paper_settings.py`), changed for findings 5 and 9:
the SFT rounds print their weight decay (0.01, the default of PyTorch,
checked in the trainer); "no top-k" next to temperature and top-p; one
row says the optimizer and the schedule are new at every client in
every round; "Clients in a round: all clients of the setup" (it said
"all 5", wrong for the setup with ten); the LoRA parameter in words;
"Learning-rate warm-up" in place of "Warm-up share"; lambda named; the
limit on a training sequence, with "no sequence is truncated"; vLLM
"for sampling and evaluation". Still missing, to be added when their
runs are committed: the settings of FedDPO, the coefficient of FedProx,
the epochs of Local SFT, the second training seed.

## 4. Editor's notes, round 1

1. Section 4.1: the order of the rule that reads the query, and the
   comparison of results on Spider, which Section 3.4 points here for.
2. Section 4.4: FedDPO (its settings, the reference model, the pointer
   to the two ablations of Section 6 that take its two differences
   apart) and what the Local SFT row shows.
3. Sections 4.5 and 4.6: where the rows of the second seed are seen;
   which rows are tested against which.
4. Section 4.2: the paragraph on the partition; the reason for the skew
   by query complexity; the IID clients still differ in size.
5. Two statements that were not exact (the ablations on BIRD, "the same
   settings"); the two schemes of difficulty levels; why only Spider
   prompts carry example rows; the prompt said twice; the place of the
   last paragraph of 4.1.

Changes to the brief for these notes: the three steps of reading the
query; the ablations on BIRD; the limit on a training sequence of
DeepSeek-Coder; the settings of FedDPO; what the Local SFT row shows;
the reason for the skew and the remark on the IID setup; which rows are
tested. The ceilings were rewritten as the strongest wording allowed,
after the owner's rule of 2026-11-26 (`WRITING_PLAN.md`, section 4):
none lists any more what the paper does not claim.

## 5. Revision 1 and the second cold read

Revision 1 answered the five notes: 1,257 words (1,250 at most), about
2.9 pages, build and lint clean. The writer made room by taking out
what Table 2 and Table B1 already hold (the sizes of the training sets,
the three further setups in words, the adapted matrices, the batch
sizes), what each perturbed set changes, and the counts of gold SQL
queries of BIRD train that exceed the time limit. It questioned three
facts of the brief, rightly: "EX is reported by the same levels" as a
reason for the skew holds on Spider only; "FedAvg SFT in Section 5" as
the reference row is wrong for Table 6; the sentence on the two
ablations of Section 6 rested on the editor's message alone.

A second helper on Opus, fresh, read the pages of revision 1. It said
correctly what is compared with what, on which data and how a
difference is judged. Its eight findings:

| # | Finding | Weight | What was done |
|---|---|---|---|
| 1 | One training seed; the test covers the evaluation questions only; "reported with the main results" does not say how; does the seed set the sampling | major | note 4 for the two rows and the role of the seed. The limit of one seed: Section 7 (`REVIEW_NOTES.md`, C9) |
| 2 | No source for T, T_w, the learning rates and the recipe of the preference rounds; no validation set; did FedAvg SFT get the same care | major | note 2: the sources of the two recipes, checked in SPFT-SQL (appendix A.4) and CodeLutra (Table 4). T and T_w: not sent (`REVIEW_NOTES.md`, C10) |
| 3 | With two preference rounds FedDPO differs from the method in the pairs and the reference model of one round only; it is the authors' construction | major, a question of design | not sent. `REVIEW_NOTES.md`, C2 and C11 |
| 4 | Local and centralized SFT at 3 epochs against 4 rounds of FedAvg SFT; has FedAvg SFT converged; no baseline that trains on correct samples without the preference term is announced | minor to major | note 2 for the 3 epochs; note 5 for the pointer to Section 6. Convergence is claim A2 of Section 5 |
| 5 | The rule on 1/K contradicts Table 2 (18 of 69 databases at K = 5); the levels of BIRD train cannot be rebuilt, since the parser of Spider rejects most BIRD queries | minor | note 1. Both checked in the code: the rule is applied per tier (`fedls_sql/data/federated.py`); BIRD train uses the criteria of Spider on the sqlglot parse (`fedls_sql/data/hardness.py`). Table B1 now has both |
| 6 | The Local SFT row, a mean over K models, cannot be tested; what forms a family | minor | note 4 |
| 7 | The paragraph on the questions without pairs stands between the two metrics | minor | note 3 |
| 8 | Fig. A1 prints curly quotes for backticks; the lead-in of Appendix A was read twice; no row for Local SFT in Table B1; alpha with two meanings; "all but one of the ablations" | remarks | Fig. A1 now prints backticks and straight quotes; Table B1 writes `lora_alpha`; note 5 for the rest |

## 6. Editor's notes, round 2 (the last)

1. Section 4.2: the rule on 1/K as it is applied (per tier), the levels
   of BIRD train, the sentence with the reason for the skew.
2. Section 4.5: where the two recipes come from.
3. Section 4.1: the place of the paragraph on the questions without
   pairs.
4. Sections 4.5 and 4.6: the rows of the second seed, what the seed
   sets, which rows are tested (Table 6, Local SFT).
5. Form: three sentences of 4.4, "all but one of the ablations", the
   pointer to Section 6, the two lead-ins of the appendices.

Changes to the brief for these notes: the partition rule per tier; the
levels of BIRD train through sqlglot; the row "where the recipes come
from" with `zhang2025spftsql` and `tao2024codelutra`; the rows of the
second seed; the rows that are tested.

## 7. Revision 2 and what is left for the owner

Revision 2 answered the five notes; the two rounds are used. Build and
lint clean (0 stops), one macro prints `??` (the coefficient of
FedProx). 1,337 words against 1,250 at most; Section 4 takes about 3.1
pages (plan: 2.3) and the build has 14 pages. 41% of its words stand in
runs of five or more words of the brief.

What changed: Section 4.2 gives the reason for the skew in three steps,
the levels of the two training sets, and the rule on 1/K as it is
applied; the paragraph on the questions without pairs closes 4.2;
Section 4.5 names the sources of the two recipes and what the seed
sets; Section 4.6 states which rows are tested; the two lead-ins of the
appendices are rewritten.

The facts of revision 2 were checked against the code, the generated
tables and the two papers. Four points are left for the owner's
reading (`REVIEW_NOTES.md`, B11 to B14) and the length is the owner's
decision (A14):

| Point | State |
|---|---|
| "A preference round constructs no pair for some of them: ..." (4.2) | revision 1 said "in any round"; without it the two kinds read as the only questions without pairs |
| "Its parser cannot read most queries of BIRD train" (4.2) | the code records the share for BIRD dev (85%); the databases of BIRD train are not on the Mac, so the share on BIRD train is not measured. A count of the gold SQL queries with syntax outside Spider's grammar (backticks, CAST, CASE, IIF and others) gives 2,319 of 9,428, a lower bound only |
| "the same number of databases" in the IID setup (4.2) | Table 2 prints 29 to 30 for 146 databases at 5 clients |
| "which sets the order of the training examples and the sampling of the preference rounds" (4.5) | the seed also sets the initialization of the adapter and the pairing; Table B1 now has the full list, and the writer offers this clause as a cut |

Length: the writer lists six cuts, 81 words by its count, which bring
the section to about 1,255. Table B1 now holds what cuts 4 and 5 remove
(the role of the seed; the redraw rule), and Table 6 names its two
reference rows itself (cut 3).

Carried to Section 5 (in its brief): the row "No training" is no longer
explained in Section 4; the captions of the result tables explain the
asterisk and the unadjusted p.
