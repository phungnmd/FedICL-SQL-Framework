# Section 2, Related work: checks and editor's notes

Draft: `sections/02_related.tex`. The writer's outline:
`briefs/02_related_outline.md`; the writer's notes:
`briefs/02_related_notes.md`. The facts about the cited papers, with
quotations and locators: `briefs/02_related_table1_rows.md` (the four
papers of Table 1) and `briefs/02_related_rows.md` (the other
seventeen), both built by Opus helpers from the papers themselves.

The writer (Fable 5.2, high effort) read the guide, `TERMS.md`, the
voice folder, the brief, Sections 3 and 4 and `main.tex`, and no other
file of the notes. One agent wrote the outline and the draft.

## 1. Outline

The outline covered every statement of the brief and did not depart
from it or from `OUTLINE.md` in content. What differs in form:

| Point | Brief or `OUTLINE.md` | Outline |
|---|---|---|
| Heading of 2.1 | "Small language models for Text-to-SQL" (the wording of the headings was left to the writer) | "Fine-tuned open models for Text-to-SQL": the works credited run from 0.5B to 32B parameters, so "small" names only part of them |
| Table 1 | five properties; the two properties of the pairs in one column or in two | one column for the two: they take the same value in each of the five rows |
| Reinforcement-learning papers | named in 2.1 or 2.2 | in 2.1 only, last in its list, so that the execution-based reward leads into 2.2 |
| The stop of 2.3 | one statement | its half on FedDPO closes the paragraph on federated DPO; its half on the task closes the subsection |

Answers of mine: the finding of Liu et al. stays, in the first
paragraph of 2.2 and without a cause; the three numbers of Zhang et al.
(70.32, 40.03, 60.16) are typed; a clause that the 1.5B model of our
experiments is among the models these works fine-tune is left out (the
section sets no result of these works beside ours); the abbreviations
SFT, DPO, NLL, LoRA and EX are used without expansion, which Section 1
has to supply.

## 2. Checks of the first draft

| Check | Result |
|---|---|
| Build | `make`: 23 pages (limit 25) with Sections 1, 6, 7 and 8 empty; Section 2 runs from the lower half of page 1 to page 3, about 2.0 pages (plan 1.8); the reference list has 40 entries |
| Lint | 0 STOP. Its notes on this file are the numbers of cited papers (checked by the audit below), names of systems read as abbreviations, and SFT, DPO, NLL, LoRA, EX used without their long form, which Section 1 supplies |
| Length | 888 words by the writer's count, 843 by `style_profile.py`; the brief asks for 810 and allows 900. The excess is in 2.2 (342 against 260) |
| Style measures (signals only) | sentence mean 26.3 words (reference 23.0); 3.1 sentences per paragraph (5.1); 2.2 citations per paragraph (4.2); no hedge, no intensifier |
| Where the brief did not hold (writer) | statement 2.1.1 grouped SLM-SQL, Think2SQL and Arctic-Text2SQL-R1 as "SFT followed by reinforcement learning"; the rows support that order for SLM-SQL only, and the draft does not say what precedes the reinforcement learning |

## 3. Cited-work audit

An Opus helper checked every statement about a cited paper and every
part of Table 1 against the text of the paper itself
(`briefs/02_related_audit.md`): 37 statements and the 22 parts of
Table 1. 33 statements and all parts of the table are supported; every
typed number, model size and citation key is right. Four statements are
imprecise:

| Draft | What the papers say |
|---|---|
| "None of the works discussed in this subsection considers Text-to-SQL" (2.3) | holds for the five federated works; LoRA is cited in the subsection and its experiments include a Text-to-SQL dataset (the helper's knowledge of the paper; its text was not at hand) |
| "In all works of this subsection, the party that trains holds the questions and the databases" (2.2) | DPO, Pang et al. and Lanchantin et al. use no database |
| "DPO has also been applied in federated training, on preferences that the clients already hold" (2.3) | true of FedDPO; in Wu et al. DPO runs at the server on pairs made there |
| "\method{} follows it in its sampling and loss settings" (2.2) | Section 3.4 names two departures: fewer pairs, and the NLL term averaged over tokens |

## 4. Cold read

Run with the `cold-review` skill and its `section` template (first use;
the owner approved the template on 2026-11-27): one isolated Opus
session that saw pages 1 to 3 and the reference pages of the build and
nothing else. Its report:
`cold_reviews/2026-11-27_0338_section2_1.md`.

| # | Weight | Finding | What follows |
|---|---|---|---|
| F1 | major | The finding of Liu et al. (DPO lowers EX for six of ten models when the output is the query alone) is quoted, the model of this paper also outputs the query alone, and the section moves on | note 1 |
| F2 | major | Table 1 leaves out the federated works with verifiable rewards (PubSwap, Fed-GRPO), which train on the model's own outputs, and Liu et al.; the novelty sentence holds because "pairs" excludes reinforcement learning. Federated GRPO for Text-to-SQL reads as the obvious alternative and no reason is given to prefer pairs | the row is the owner's decision (`REVIEW_NOTES.md`, A22); the question is C26 |
| F3 | major | The contribution reads as CodeLutra inside FedAvg; a client holds the database, the gold SQL and the model and could run CodeLutra alone; nothing says what the federated setting changes | note 2; C27 |
| F4 | minor | FedDPO is "one of our baselines" and has a cross under Text-to-SQL in Table 1: which object is described | note 3 |
| F5 | minor | Why several organizations want a joint model is not argued; the sentence on the privacy motive of CodeS was read twice | Section 1 (C28); note 5 |
| F6 | minor | Averaging LoRA adapters is presented as unproblematic; the gap of Zhang et al. between FedAvg and centralized training is reported and the section does not say whether the method addresses it | note 4; aggregation work is not added (reference budget) |
| F7 | minor | "differ in what the model is trained on" does not fit the three reinforcement-learning works; sizes are given for some works without a reason | left to the writer |
| F8 | remark | the same stop four times | note 5 |
| F9 | remark | CodeLutra is a general method for code generation, described as a Text-to-SQL method | note 2 |
| F10 | remark | EX, SFT, NLL not expanded | Section 1 |

It also could not tell which task areas belong to PubSwap and which to
Fed-GRPO, and whether "during training" (caption) and "in each round"
(text) mean the same (notes 5 and 3).

## 5. Editor's notes, round 1

Five notes, sent to the writer on 2026-11-27. The brief was corrected in
the same places (list in `REVIEW_NOTES.md`, part D).

1. 2.2, Liu et al.: their setup beside the finding (pairs once, the DPO
   loss alone, a fixed reference), no cause claimed, and a pointer to
   the ablation of the same parts in Section 6.
2. 2.2, CodeLutra: the pointer to Section 3.4 carries what is taken and
   where the two differ; CodeLutra is a method for code generation; the
   paragraph repeats the first paragraph of the subsection.
3. Table 1: the rows describe the methods as published; "renewed in
   training", "during training" and "in each round"; what a cross in the
   joined column denies.
4. 2.4, Zhang et al.: the numbers raise the question whether the paper
   closes the gap between FedAvg and centralized training; say how
   their question (heterogeneous clients under SFT) relates to ours
   (the supervision).
5. The sentences that speak for a subsection: three claim more than the
   works support (audit); the same stop four times; the privacy
   sentence of 2.1; the task areas of PubSwap and Fed-GRPO.

## 6. Checks of revision 1

| Check | Result |
|---|---|
| Build | `make`: 23 pages (limit 25); Section 2 on pages 1 to 3; the reference list has 38 entries (Pang et al. and Lanchantin et al. are no longer cited) |
| Lint | 0 STOP |
| Length | 892 words by the writer's count, 847 by `style_profile.py`; 2.2 has 351 words against 260 in the brief |
| Style measures (signals only) | sentence mean 24.9 words (reference 23.0); 3.3 sentences per paragraph (5.1); 2.0 citations per paragraph (4.2); no hedge, no intensifier |
| Changed statements against the fact rows | read by the editor: the setup of Liu et al., CodeLutra as a method for code generation, the task areas of PubSwap and Fed-GRPO, Zhang et al. without numbers and the last column of Table 1 agree with the rows. The pointer to Section 3.4 agrees with that section except in two points (round 2, note 1) |
| The writer's cuts | to stay under 900 words the writer cut the sentences on Lanchantin et al. and on Pang et al.; statement 2.2.2 of the brief was then not served for Pang et al. |
| The writer's doubt 1 | "examines the same choices" against the three choices of Liu et al.: the row without renewal keeps the pairs and the reference model of the first preference round (`OUTLINE.md`, Section 6, B1), so the three are covered |

## 7. Cold read of revision 1

Second run of the skill with the `section` template, on pages 1 to 3
and 17 to 22 of the build:
`cold_reviews/2026-11-27_0351_section2r1_1.md`. The two readers are
independent; a point both make is marked.

| # | Weight | Finding | What follows |
|---|---|---|---|
| F1 | major | The difference from CodeLutra is not established: "a federated round renews the pairs" is listed as a difference although CodeLutra renews them; "takes its sampling and loss settings" is followed by settings that change; the method reads as CodeLutra inside FedAvg (both readers) | note 1; what the federated setting changes beyond that is C27 |
| F2 | major | PubSwap and Fed-GRPO are set aside by their task alone and are not in Table 1; no reason for pairs instead of a reward at the clients (both readers) | the owner: A22, C26 |
| F3 | major | Pang et al. (DPO and NLL loss, pairs renewed each iteration, the previous model as reference) is not cited, and these parts are credited to CodeLutra alone | note 2; the brief asked for it and the writer cut it for length |
| F4 | minor | Liu et al.: "the same choices" names two of three; the pointer hints that renewal and the NLL term repair their finding | note 3 |
| F5 | minor | What one organization lacks that federation supplies is not said; the step from the privacy motive of CodeS to several organizations is a change of setting (both readers) | note 5; Section 1 (C28) |
| F6 | minor | Table 1 leaves out Liu et al., PubSwap and Fed-GRPO, and the two properties the text uses against FedDPO and Liu et al. (reference model, NLL term); what the tick under Text-to-SQL means for CodeLutra | the owner: A22; the tick in note 1 |
| F7 | minor | "requires no annotator" and "what a client can learn from the databases it holds" read as a setting without gold SQL | note 4 |
| F8 | minor | Where the pairs of the FedDPO baseline come from on Text-to-SQL | Section 4.4 says it; the pointer is there |
| F9 | minor | Averaging LoRA adapters is presented as settled; the work on it is not cited (both readers) | the owner: A23 |
| F10 | remark | The stop of 2.2 argues for no gap: in federated training the client is the site that trains | note 5 |

It also noted two names for one term ("likelihood term", "NLL term";
note 1) and that the rule of Zhang et al. for a correct prediction
should be checked against the paper (checked by the audit: exact string
match).

## 8. Editor's notes, round 2 (the last)

Five notes, sent to the writer on 2026-11-27. The brief was corrected in
statements 2.1.1, 2.2.2, 2.2.3, 2.2.4, 2.2.6 and 2.4.1
(`REVIEW_NOTES.md`, part D).

1. 2.2, CodeLutra: that the pairs are renewed is common to the two and
   is not a difference; what is taken and what differs as Section 3.4
   has them; one name for the likelihood term; the tick under
   Text-to-SQL.
2. Pang et al. come back (statement 2.2.2); the room is in what the
   reader found said more than once.
3. 2.2, Liu et al.: the row without renewal keeps the pairs and the
   reference model, so Section 6 examines the three choices; no cause
   and no result promised.
4. Two sentences read as training without labels; the gold SQL query
   decides every preference.
5. The ends of 2.1 and 2.2: the stop of 2.2 argues for nothing; the
   privacy motive of CodeS joins two settings; the opening of 2.1 does
   not cover the reinforcement-learning works.

## 9. Revision 2

| Check | Result |
|---|---|
| Build | `make`: 23 pages (limit 25); Section 2 on pages 1 to 3, about 2.0 pages; 39 references (Pang et al. cited again) |
| Lint | 0 STOP |
| Length | 893 words by the writer's count (2.1 130, 2.2 406, 2.3 195, 2.4 162), 851 by `style_profile.py`; 900 at most. 2.2 holds almost half of the section |
| Style measures (signals only) | sentence mean 24.3 words (reference 23.0); 3.7 sentences per paragraph (5.1); 2.3 citations per paragraph (4.2); no hedge, no intensifier |
| New sentences against the fact rows | read by the editor: Pang et al. (row K.1: samples from the current model, pairs by the correctness of the answer, DPO and NLL, the previous model as reference), LEVER and GradeSQL (labels from the comparison with the gold result; the generator is not trained), what is taken from CodeLutra (Section 3.4) agree with the rows |

What the five notes became:

1. CodeLutra: what is taken follows Section 3.4; the differences open
   with the loop running across clients; renewal is no longer listed
   as a difference; "NLL term" throughout; the caption of Table 1 says
   what a tick under Text-to-SQL marks, with a note on CodeLutra.
2. Pang et al. are back with what is theirs; CodeLutra "applies this
   iterative scheme at one site, with execution labels". Lanchantin et
   al. stay out.
3. Liu et al.: "Section 6 varies all three of these choices"; no
   removal named, no result promised.
4. "needs no annotation beyond the gold SQL query that SFT already
   uses"; "what execution on the databases of a client adds to the gold
   SQL as supervision".
5. 2.2 has no closing sentence; the privacy motive of CodeS is out; 2.1
   is one paragraph and its opening covers the reinforcement-learning
   works.

Left for the owner's reading (`REVIEW_NOTES.md`): the sentence under
"to our knowledge" no longer carries the scope "for Text-to-SQL" of
`CLAIMS.md`, rule 7 (B21); "the scale of the DPO term" and "the uniform
pairing" before Section 3 (B22); the promise about Section 6 (B23); the
rows of Table 1 (A22) and the work on LoRA aggregation (A23). No third
cold read was run: the two rounds are used.
