# Editor's notes: Section 1, Introduction, abstract, keywords

Wording notes on one draft (`WRITING_PLAN.md`, section 7.0); they die
with it. What stays true whatever the draft says is in `01_checks.md`.
The messages as sent are in `build/` (`answer_01.md`, `notes_01_N.md`,
outside Git); this file keeps what each note asked and what the writer
did.

## Draft 1 (2026-11-28)

Checks on the draft: build passes (16 pages); lint stopped on a typed
"0.5" in paragraph 1, fixed by the editor with a setting macro
(`\setting{models.size.min}`, `tools/paper_settings.py`), then no stop;
its notes on abbreviations in the abstract are expected (the abstract
expands its own). No run of five words shared with the closest papers
or the example papers. 17% of the words of the section and 20% of the
abstract stand in runs of five or more words of the brief. Register
against the introductions of the reference papers: 966 words; sentences
of 34.8 words on average (reference 26.3); 22.0% long words (20.7);
32% of sentences with "we" (44%); everyday verbs 3.1 per thousand
(1.0). Cold read on the PDF of the section (`cold_reviews/
2026-11-28_0128_section1_1.md`; the run used the default journal name
of the tool, JIIS, so its point on the template is void).

My answer to the outline (point 3) described the earlier Fig. 1, a
Spider question with samples of the pretrained model; the figure had
been redrawn with a BIRD question in the meantime. The caption followed
my answer. Note 1 corrects it.

### Round 1, five notes

| # | Place | The note | Source |
|---|---|---|---|
| 1 | Caption of Fig. 1 | Dataset, model that sampled, counts of outcomes, server and adapter not drawn; evidence missing from panel A's prompt; caption restates paragraph 4 | claim audit 1-3, 9; cold read F5 |
| 2 | Paragraph 1 | "The highest-accuracy systems rely on prompting proprietary LLMs" (present tense) against the rows; privacy and schemas attributed to SLM-SQL | claim audit 5, 10 |
| 3 | Paragraph 3, abstract | "Without query execution" false on Spider; "no supervision penalizes incorrect queries" read as overstated (touches A44, open: both facts given, the wording left to the writer); token-averaged NLL attributed to cited works; FedDPO is not Text-to-SQL work, its citation, the evidence on its parts with sets; the "shared structural cause" false for FedDPO; one sentence on centralized execution feedback allowed | claim audit 4, 6, 7; cold read F1, F2 |
| 4 | Paragraphs 5, 6 | Warm-up "correct samples across client questions" against 4,035 and 2,698; the test behind the p-values; which incorrect-result count is whose, and that they are higher; the peak on Spider | cold read F3, F6, F8; own reading |
| 5 | Contributions 2, 3 | Alignment holds for preference rounds; C3 facts at their strength and scope (more such answers, a third fail the suite, a large part of the BIRD gain, not Spider) | claim audit 11, 12; cold read F7 |

Not sent, with the reason:

- No result against FedDPO (cold read F2): the row waits (`CLAIMS.md`,
  A6); no sentence states one.
- Equal rounds, not equal compute; no zero-shot, local or centralized
  number in the Introduction (cold read F4): decided by the owner
  (headline at equal rounds, cost in Section 5.6); `REVIEW_NOTES.md`,
  C42.
- One seed and one partition behind the p-values (cold read F3):
  `REVIEW_NOTES.md`, C9 and C15; the note asks only to name the test.
- The pair count as a message reveals how a client does (cold read):
  `REVIEW_NOTES.md`, C41.
- Fig. 1 pairs, SQL 1 as chosen side of both pairs, impossible under
  the rule (claim audit 8): a fault of the figure, not of the text;
  `01_checks.md`, part 1, open for the figure.
- Repetition (the upload of adapter and weight four times, the
  critique of FedAvg SFT and FedDPO in abstract and paragraph 3) and
  sentence length: round 2 if it still stands.

What the writer did with round 1: all five carried out. The caption
describes the BIRD figure (first preference round after the warm-up
rounds; 7, 2 and 1; evidence in the prompt of panel A; no server).
Paragraph 1 says prompting of proprietary LLMs is widely adopted and
gives CodeS the privacy motive and SLM-SQL the size range and fast
inference. Paragraph 3 states the FedAvg SFT facts as procedure
("nothing identifies which of the model's queries are incorrect"),
points the token-averaged NLL to Section 3, gives FedDPO to OpenFedLLM
on helpfulness and harmlessness data and DPO to Rafailov et al., cites
centralized execution feedback in one sentence (CodeLutra, ExCoT,
Think2SQL, Arctic-Text2SQL-R1) and replaces the shared cause by the
fact that only the client can produce execution supervision. Paragraph
5 gives warm-up as fewer all-incorrect questions (4,035 to 2,698);
paragraph 6 names the test, the Spider plateau and the order of the
incorrect-result counts. Contributions 2 and 3 are scoped to the
preference rounds and to BIRD, with the TS gain.

## Draft 2 (2026-11-28)

Checks: build passes (17 pages, Fig. 2 redrawn larger); lint no stop
(notes: "DPO" and "APIs" without long form, "McNemar" and
"student_loan" read as abbreviation and lab word); no overlap; 9% of
the section and 12% of the abstract in runs of the brief. Register:
1,059 words; sentences of 41.2 words on average (draft 1: 34.8;
reference 26.3); 31% of sentences with "we" (43.6).
Second cold read on the PDF of the section (`cold_reviews/
2026-11-28_0143_section1_r1_1.md`, journal CMC) and second claim audit:
no number wrong; p-values of two kinds in one paragraph; pair
construction credited with the renewal of the reference; scope of
paragraph 4 on Spider; "prevailing" and "local hardware" without a row.

### Round 2, five notes

| # | Place | The note | Source |
|---|---|---|---|
| 1 | Paragraphs 3, 5 | "Two reasons" slip (FedDPO executes nothing and is not Text-to-SQL); "cannot target evolving errors" is a fact of FedDPO as published; the nearest committed row (fixed pairs and reference, BIRD -2.61, level on Spider); the reference renewal belongs to the objective, not to pair construction; last sentence of paragraph 3 at length | cold read 2 F1, F8; claim audit 2 no. 3 |
| 2 | Paragraph 6 | Raw p printed under "with per-table Holm correction", 0.077 adjusted beside 0.37 raw; both kinds given; BIRD peak round; Spider round 5 with its point (+4.28) or not at all | claim audit 2 no. 1; cold read 2 F6, part 2 |
| 3 | Contribution 3 | Read as a warning sign; C3 and C4 facts (answers written differently that return the gold result; 132 against 86 under the suite; a third against a tenth fail it); the suite is generated; one sentence with four claims | cold read 2 F2, part 5 |
| 4 | Paragraphs 1, 2, 4, abstract | Paragraph 4 scope on Spider; "prevailing" without a row; SLM-SQL "edge deployment"; NLL term named three ways; "DPO" without long form; FedAvg SFT clauses repeated | claim audit 2 nos. 4, 5; cold read 2 F7, F9; lint |
| 5 | Whole section | 1,059 words, sentences of 41 words; passages read twice; four repeated statements | register; cold read 2 part 5 |

Not sent, with the reason:

- Novelty against centralized iterative DPO with execution labels, and
  credit at the place of the components (cold read 2 F1): the paper
  credits the closest work in Section 2.2, Table 1 and at the objective
  (owner, 2026-11-27); `REVIEW_NOTES.md`, C1.
- Fig. 1: the correct sample `COUNT(*)` against the gold `COUNT(name)`
  read as a match by coincidence, and both pairs with SQL 1 as chosen
  side (cold read 2 F2, F7; claim audit 2 no. 2): faults or choices of
  the figure; open for the owner. Whether `name` can be NULL in
  `enrolled` was not checked: the BIRD train databases are not on this
  machine.
- One run and one split behind the p-values (F3): C9, C15. Equal
  compute (F4): C42. Pair count as a message (F10): C41.
- An execution filter at inference as a cheaper alternative (F5):
  reviewer question, `REVIEW_NOTES.md`.
- Rounds and settings chosen on the evaluation sets (F6): the setup
  section states what was chosen on which set; nothing for the
  Introduction.
- Running head "2026submitted" and the licence line: the template, not
  the section.

What the writer did with round 2: all five carried out. Paragraph 3
opens on the fact both lack (no query of the model executed) and scopes
the fixed pairs and reference to FedDPO as published; pair renewal and
reference renewal are given to their own components; paragraph 6
prints Holm-adjusted p throughout, names round 3 and pairs the Spider
round 5 with its +4.28; contribution 3 is three sentences with the
suite counts; "prevailing", "local hardware" and the fourth statement
of the FedAvg SFT gap are gone; the NLL term is named once with its
weight. Draft 3: 989 words, 28.9 words per sentence, 28% "we"
sentences; abstract about 250 words; build, lint, overlap clean.

Open after round 2 (no third round without the owner):

- Contribution 3, "after the suite rejects 30.9% of EX matches": the
  share is of the answers on other tables or columns; of all the
  method's EX matches the suite rejects 110 of 748.
- Paragraph 3, FedDPO "even with execution-labeled initial pairs ...
  (Section 5.3)": the row pointed to keeps the NLL term and is not
  FedDPO; its effect is stated for BIRD.
- Abstract, "existing federated alignment methods based on DPO, such as
  FedDPO": the record holds FedDPO of OpenFedLLM. Paragraph 5, "every
  round forms one resampling step": the preference rounds.
- Fig. 1 is being redrawn with the pairs the run built (a new example
  question); the caption follows the committed figure.
