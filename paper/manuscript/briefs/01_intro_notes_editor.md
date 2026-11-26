# Section 1, Introduction (with the abstract and the keywords): checks and editor's notes

Drafts: `sections/01_intro.tex`, `sections/00_abstract.tex`,
`sections/00_keywords.tex`. The writer's outline:
`briefs/01_intro_outline.md`; the writer's notes, with the three title
candidates: `briefs/01_intro_notes.md`.

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief, Sections 2 to 6 and `main.tex`, and no other
file of the notes. One agent wrote the outline and the draft.

## 1. Outline

Eight paragraphs, 945 words planned, no subsection and no float; an
abstract of about 205 words with one number; six keywords. The outline
serves the eight statements of the brief and every row of "What the
later sections take from this section". It does not depart from the
brief or from `OUTLINE.md` in content. What differs in form:

| Point | Brief or `OUTLINE.md` | Outline |
|---|---|---|
| The gap | two statements (3 and 4) | three paragraphs: what federated fine-tuning uses; execution labels and CodeLutra at one site; FedDPO and the scoped gap |
| The NLL term | "a likelihood term" in the row of CodeLutra | introduced with CodeLutra as "a negative log-likelihood (NLL) term", as Section 3.4 has it |
| Values of $T$, $T_w$, $N$, $M$ | may stay in Section 3 | none |
| Closing outline of the paper | the writer's choice | none; the contributions point to the sections |

Answers of mine: the number of rounds is named once in the results
paragraph (`\setting{rounds.total}`), since "after round 3" is read
against it; `\setting{model.size}` may be used; non-IID stays out of
the Introduction (its expansion belongs to Section 4.2, noted for the
whole-paper pass); the contributions as a list of four items; in the
abstract, the adapter has to be readable without Section 3.

One correction of the brief went with the answer. Statement 7 said "a
preference round takes more client compute than an SFT round";
`\fact{cost.spider.pref2.ratio}` prints 0.9. The clause is now the one
of Section 5.4: no communication beyond that of FedAvg SFT, and the
additional cost is computation at the clients.

## 2. First draft: checks

- Length: 971 words by the style tool (the writer counts about 1,020
  in the PDF); the brief asks for about 945 and 1,050 at most. Abstract
  about 236 words, one number.
- Build: compiles, no undefined reference. The whole build is 29 pages
  against the limit of 25.
- Lint: four stops, all model sizes of cited papers typed by hand (15,
  32, 0.5, 1.5 in paragraph 1), as in Section 2.1; they are facts of
  the cited papers, not results or settings of ours.
- Against the brief: the six abbreviations are given in full; Spider
  and BIRD are cited at first mention; the six terms are introduced;
  "federated Text-to-SQL" is said once; Zhang et al. by name. A2 is
  worded as in Section 5.1.
- One difference from Section 2 that I found: paragraph 5 says FedDPO
  takes its pairs from "a dataset of human preferences", where Section
  2.3 has "a preference dataset, for helpfulness or harmlessness". The
  ceiling of statement 4 in the brief had "human preference data"; the
  OpenFedLLM paper does not say that for both of its datasets. Brief
  corrected.
- The EX values of paragraph 7 carry a percent sign; Section 5 prints
  the same macros without one. Left for the whole-paper pass.
- Style signals (for the editor only): mean sentence 29.1 words
  against 26.3 in the reference introductions; no hedge or
  intensifier.

## 3. Cold read 1

`cold_reviews/2026-11-27_0521_section1_1.md`: a reader with pages 1 to
3 of the PDF (title, abstract, Section 1 and the first lines of
Section 2.1).

| # | Finding | Weight | What I make of it |
|---|---|---|---|
| F1 | The method reads as "CodeLutra's loop run inside FedAvg, with SFT warm-up rounds first"; nothing says what federated training changed; FedDPO is a weak foil | major | The same point as the cold reads of Section 2 (C27). Section 3.4 states the difference; the Introduction does not. Note 1 |
| F2 | The reader cannot tell how the 4 rounds divide, how round 4 was chosen, or whether the baseline is read at its best round; "same number of rounds" equalises communication, not compute | major | The split of the rounds and the baseline at its highest round are in the paper (Section 5.1: 43.68 at round 3 on BIRD dev, 5.08 points below). Note 2. The compute-matched comparison is the fifth round of FedAvg SFT on Spider in Section 5.4; not asked of the Introduction |
| F3 | The premise (organizations cannot pool, yet want one model) is asserted; local fine-tuning is not ruled out; "five clients" is all the reader has on the federation | major | Notes 2 and 3. The Local SFT row waits for the GPU, so the Introduction cannot say that a lone client does worse |
| F4 | Execution-based reinforcement learning is missing: paragraph 4 gives DPO as the way execution labels are used, Section 2.1 names three works that use a reward; why DPO and not a reward is not said; the level (48.76 on BIRD dev) is not placed against that line | minor, close to major | The credit is owed and the keys are in the list: note 5. Why DPO and the level are questions for the owner (`REVIEW_NOTES.md`) |
| F5 | "Federated fine-tuning of language models, as currently practiced, learns from the gold SQL query alone" is contradicted by FedDPO two paragraphs later | minor | True; the writer's own doubt 4. Note 4 |
| F6 | "Both differences are significant" has no test | minor | Note 2 |
| F7 | The cost has no size; executing generated SQL on internal databases has risks; the integer sent to the server reveals how often the model is right on a client's data | minor | The factors are in Section 5.4. The risks and the integer are not treated anywhere in the paper: for the owner |
| F8 | "Fine-tuning requires the databases" against "the databases serve only to construct the prompt"; "a label that the gold SQL query alone does not" read twice; labels can be right by coincidence | remark | Note 4. The last is limitation 5 of Section 7 |
| F9 | The DPO paper is the only citation for "models are already trained on such labels" | remark | Note 5 |
| F10 | "therefore" in paragraph 5 follows from one of three properties; "many" and "several" samples; "federated Text-to-SQL" is defined and not used again | remark | The first in note 5. The phrase is defined because Section 2 uses it |

Also from the reader: contribution 1 ("We observe that the databases
of a client are a source of supervision...") inflates what is
established for centralized training. It is the wording of
`CLAIMS.md`, section 2, scoped to federated fine-tuning; kept, and
recorded for the owner. Repetition he listed: the databases "unused as
supervision" four times; the size ranges of paragraph 1 nearly word
for word in Section 2.1. His arithmetic on the headline numbers agrees
with the macros.

## 4. Editor's notes, round 1

1. Paragraphs 4 to 6: what the federated setting changes against the
   loop of CodeLutra, as Section 3.4 says it. No result of the row
   "Clients pooled".
2. Paragraph 7: what the comparison is. The federation (clients
   simulated by database, evaluation databases held by no client), the
   split of the rounds, the test behind "significant", the baseline at
   its highest round on BIRD dev.
3. Paragraph 2: the premise. A concrete case, and why an organization
   would not fine-tune alone, from the setting and without a claim on
   the result of local training.
4. Paragraphs 2 and 3: the opening sentence of paragraph 3 covers all
   federated fine-tuning and FedDPO contradicts it; "requires the
   databases" against "serve only to construct the prompt".
5. Paragraphs 1, 4 and 5: earlier work as Section 2 has it. The
   reward-based line of Section 2.1; the data of FedDPO as Section 2.3
   describes them; the "therefore" of paragraph 5.

The upper end of 1,050 words stays. The brief was extended with the
content of notes 1, 2 and 5 (statements 4, 6 and 7, two keys, three
macros).

Not sent: the unclear "which" of the first sentence of the abstract
(read twice by the reader); it goes into round 2 if it is still there.

## 5. Revision 1: checks

- Length: 993 words by the style tool (the writer counts about 1,038
  in the PDF), under 1,050. Abstract about 232 words.
- The five notes are taken up: paragraph 5 opens on what differs in
  federated training and paragraph 6 sets the method against CodeLutra;
  paragraph 7 gives the federation, the split of the rounds, the test
  and the highest EX of FedAvg SFT on BIRD dev (43.68 at round 3, 5.08
  points below); paragraph 2 says why an organization would not train
  alone and gives "a hospital or a bank" as the case (the writer's
  illustration); paragraph 3 opens "For Text-to-SQL, ..."; paragraph 4
  credits the reward-based line; FedDPO is described as in Section
  2.3.
- Lint: two stops, the sizes 0.5B and 1.5B of SLM-SQL in paragraph 1.
- Moved by the writer: Spider and BIRD are first named and cited in
  paragraph 7; the cost clause closes paragraph 6.
- A point of mine: "Whereas CodeLutra runs such a loop at one site ...
  `\method` runs it across the clients" presents the method as that
  loop moved to the clients, which is not how the paper presents it
  (Section 3.4; the owner's framing of 2026-11-17).

## 6. Cold read 2

`cold_reviews/2026-11-27_0533_section1r1_1.md`, on pages 1 to 3 of the
build with revision 1.

| # | Finding | Weight | What I make of it |
|---|---|---|---|
| 1 | The 6.19 points are against a baseline that "has already declined"; the gap to its best round is 5.08 and the abstract gives only 6.19; the cost has no size; two preference rounds do not show whether the method goes on improving | major | The change of FedAvg SFT from round 3 to 4 is not significant (Section 5.1). Note 2. Which number the abstract carries is the owner's choice (`REVIEW_NOTES.md`) |
| 2 | The section does not say what problem of the federated setting each choice answers; the method still reads as CodeLutra inside FedAvg; the differences to FedDPO are listed and not weighed | major | Note 1 |
| 3 | Nothing isolates execution feedback from the DPO objective and the extra compute; no control is named | major | Section 6 has the variants; the Introduction does not name them. Note 2. The rows "Clients pooled" and Local SFT wait for the GPU |
| 4 | The fall in execution errors is larger than the gain in correct answers, and the section presents the errors as a separate benefit | minor | True, and Sections 5.4, 7 and 8 say that the incorrect results are not fewer. Note 2 |
| 5 | Executing generated queries on internal databases is presented as free (load, statements that write, long queries) | minor | Not treated anywhere in the paper; for the owner |
| 6 | The execution label is treated as ground truth | minor | Limitation 5 of Section 7 |
| 7 | The weight by pair counts is unexplained and may down-weight the hardest clients | minor | Section 6 has the comparison of weights; for the owner |
| 8 | OmniSQL cited for 0.5B to 1.5B; the LoRA paper cited for the practice; CodeLutra's task not said | minor | The first is an error of revision 1. Note 3 |
| 9 | Contribution 1 overclaims ("identify") | minor | Said by both readers. Note 4 |
| 10 | Names: three for the baseline in the abstract; "a likelihood term" and "an NLL term"; "one integer"; "FedLS" never expanded | remark | Note 5. The name is the owner's |

## 7. Editor's notes, round 2 (the last)

1. Paragraphs 5 and 6: each difference with its reason (Sections 3.3,
   3.4 and 6 have them); "which no single party trained"; the method
   not as CodeLutra's loop moved to the clients.
2. Paragraph 7: where the gain arises (half the execution errors, the
   incorrect results not fewer); the baseline's change from round 3 to
   4 is not significant; the size of the cost; what the ablation
   varies.
3. Three citations that do not carry their sentence.
4. Contribution 1 in the scope of the brief.
5. The abstract against Section 1: names of the baseline, the NLL
   term, the integer; its first sentence.

## 8. Revision 2: checks, and what stays open

- Length: 1,001 words by the style tool (the writer counts about 1,047
  in the PDF), under 1,050; nine paragraphs with the list. Abstract
  about 241 words, one result number.
- Build (scratch directory): 29 pages, no undefined reference, 41
  references, 48 numbers waiting.
- Lint: the two sizes of SLM-SQL (0.5B, 1.5B) stop, as facts of the
  cited paper.
- Mechanical change of mine: the citations of BIRD and Spider moved to
  their first mention, which revision 2 had put one paragraph before
  the citing sentence.
- The five notes are taken up: the method is no longer told as the
  loop of CodeLutra moved to the clients, and each part has its reason
  (warm-up rounds, renewed pairs, the reference model) with what
  Section 6 finds for the two parts absent from FedDPO; the results
  paragraph says that the gain comes with half the execution errors
  while the incorrect results do not become fewer, that the EX of
  FedAvg SFT at round 3 on BIRD dev does not differ significantly from
  round 4, and gives the cost as a range; the three citations are
  repaired; contribution 1 is in the scope of the brief; the abstract
  has one name for the baseline.

Departures of the writer from the brief, kept:

- The contributions are regrouped: (1) the observation with the
  method, (2) the results with the analysis and the cost, (3) the
  ablation study, (4) the release. `CLAIMS.md`, section 2, lists the
  method as its own contribution.
- The scoped "to our knowledge" claim stands once, in contribution 1;
  the sentence that closed the gap paragraph is gone.
- "For example a hospital or a bank" is the writer's illustration.

Open, for the owner (`REVIEW_NOTES.md`):

- The title (three candidates in the writer's notes) and what "LS" in
  the name stands for.
- The abstract gives the 6.19 points at the same number of rounds; the
  Introduction now also gives the 5.08 points against the highest
  round of FedAvg SFT.
- The two ablation findings of paragraph 7 each name one set (BIRD dev
  for the fixed pairs and reference, Spider test for the missing NLL
  term); Section 6 has both sets.
- The NLL term has its finding in the Introduction and not its reason
  (Section 3.4).
- Questions of the two readers that the Introduction does not answer:
  why preference pairs and not a reward; the level of EX against the
  reward-based line; a baseline at equal client compute on BIRD; the
  execution of generated queries on internal databases.
- For the whole-paper pass: the percent sign after EX in Section 1 and
  not in Section 5; digits in running text ("After 4 rounds (2 warm-up
  and 2 preference rounds ...)").
