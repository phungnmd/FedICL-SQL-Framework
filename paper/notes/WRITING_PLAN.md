# FedExec-SQL: writing plan

How the manuscript is written. What the paper claims is in
`manuscript/CLAIMS.md`, what each section contains in
`manuscript/OUTLINE.md`, what waits for the owner in
`manuscript/REVIEW_NOTES.md`. Paths below are relative to
`paper/manuscript/` unless they start with a folder of the workspace.

## 1. How it is written

- One writing session writes and revises the manuscript directly
  (owner, 2026-11-28). The owner opens it for writing, apart from the
  session that runs the experiments, and it uses one model for the
  whole paper. There is no separate writer agent and no brief, outline,
  questions or notes file per section.
- The state is in the files. A new session takes over by reading them
  (section 2); nothing depends on one conversation.
- Before it writes or revises a section the session reads the paper as
  it stands, so that a point is made once and a term keeps its meaning.
- The owner reads the text and remarks in chat; the remark is applied
  in the text in that turn. A paragraph that reads badly is written
  again, directly.
- Draft first, trim later: the paper is complete before it is cut
  toward the pages of the fee. A section is committed when it is
  written, without waiting for the owner's reading.
- Journal: CMC alone, on the Tech Science Press class in `Definitions/`
  (section 8).

## 2. Starting a writing session

Read, in this order:

1. `paper/notes/RESEARCH_STATE.md`: sections 2 (setup), 3.1 (story),
   3.6 (closest work) and 5.0 (committed results); the first screen of
   `paper/notes/PIPELINE_NEXT.md` for what waits.
2. `CLAIMS.md`, `OUTLINE.md`, `TERMS.md`.
3. This plan, and part A of `REVIEW_NOTES.md`.
4. The sections as written (`sections/`) and the generated numbers and
   tables (`generated/numbers.md`, `settings.md`, `tab_*.tex`).
5. The checks file of the section in hand (`checks/NN_checks.md`); for
   Section 2 also the fact rows (`checks/02_related_rows.md`,
   `checks/02_related_table1_rows.md`) and `bib/report.md`.
6. For Sections 3 and 4, the loss and the round in the code
   (`fedicl-sql/fedls_sql/training/dpo.py`,
   `fedicl-sql/fedls_sql/federated/pref_rounds.py`).

It then tells the owner which step of section 6 it takes.

## 3. What binds the text

1. Truth. Every statement about our work is in the record: the
   committed results, the configs, the code. A statement about a cited
   paper has a fact row with its locator (the fact rows of Section 2,
   or part 2 of a checks file) or is read in the paper itself and gets
   its row. A fact taken from the web is added to the checks file of
   its section with the URL.
2. Claims. A finding is stated at the strength and scope `CLAIMS.md`
   gives it, not above and not below; its scope ("on BIRD", "to our
   knowledge") is part of it. `CLAIMS.md` is not fixed: a line that is
   false against the numbers is corrected and the owner is told.
3. Numbers and names. Results and settings are macros of `generated/`,
   never typed digits. A number without a committed row prints `??`
   (`--` in a table); a guess is `\expect{value}` and prints `value??`;
   `make submit` stops on either. The method is `\method`, the trained
   model "the model"; terms and notation are those of `TERMS.md`.
4. Nothing of the lab. No note, rule, date, decision, claim number or
   lab word, and no account of how a value was chosen.
5. Position. The paper is about supervision: where the training signal
   comes from. Federated learning is the setting, Text-to-SQL the task.
   Novelty is stated against FedAvg SFT and federated DPO as published.
   CodeLutra has its fixed places: Section 2.2 with Table 1, a citation
   at the objective, one sentence in Section 4.5
   (`paper/notes/RESEARCH_STATE.md`, section 3.6).
6. The limits of the journal (section 8).

## 4. Voice

Academic (owner, 2026-11-27): dense, in the terms of the field,
assertive at the strength of the evidence, the novelty said plainly,
the method told by component, the results by finding and mechanism.

- The paper speaks as its authors. "We" introduces a design choice or
  a finding; a component, a client or the server is the subject of what
  it does.
- A transition word stands only where the relation between two
  sentences is not plain from their content.
- A point is made once, in the place that owns it; other places refer
  to it.
- A number is in the running text when the reader needs it there. The
  Introduction carries the headline numbers; tests and counts are in
  Section 5.
- No account of how the research went, no defense of a choice nobody
  questioned, no hedge on a finding a table carries. Limitations are
  stated once, in Section 6.
- A caption says what the figure does not say itself.
- American spelling; no em dashes.

The example papers in `.sources/examples/` (LESFT, CMC 87(1); LoRA,
arXiv 2106.09685) show the form of a paper of this kind; they supply
neither facts nor wording. No measure of words or style steers a
sentence.

## 5. Checks

| When | Check | Tool | Stops on |
|---|---|---|---|
| Every build | Build | `make` | a section that does not compile; an undefined reference; the abstract outside 200 to 400 words. The page count is printed |
| Every build | Numbers, references, form | `make lint` | a number or a setting typed by hand; a key not in `references.bib`; an entry without DOI, arXiv id or stable address. Its notes (lab words, hedges, an abbreviation not defined) are read, not obeyed |
| A section is written | Overlap | `make overlap` | a run of five or more words shared with CodeLutra, OpenFedLLM or an example paper, other than a stock phrase of the field or a name |
| A full draft; before the paper is sent; when the owner asks | Cold read | the `cold-session` skill: an isolated session on Opus, a fresh one each time, reads the PDF as a reviewer | nothing; its findings are sorted as below |
| The same | Claim audit | a helper on Opus reads each claim beside its line of `CLAIMS.md` and looks for a committed result that contradicts a sentence | a false sentence; a claim above its line or with its scope dropped |
| The same | Cited-work audit | a helper on Opus opens every sentence about a cited paper and every cell of Table 1 at its locator | a statement without a fact row, or a row the paper does not support |

Where a finding goes:

| Finding | Place |
|---|---|
| A fact that stays true whatever the draft says (a number, a setting, what the code does, what a cited paper states, the bound of a claim) | `checks/NN_checks.md` |
| How the text reads | fixed in the text; no file |
| What only the owner can decide; what a reviewer will ask | `REVIEW_NOTES.md`, parts A and C |
| What was done | `paper/notes/LAB_LOG.md` and the commits |

A cold-read report in `cold_reviews/` is deleted once its findings are
in the text, the checks or `REVIEW_NOTES.md`.

## 6. Structure, order and state

`OUTLINE.md` holds the content and the length of each section. CMC has
no page limit; its fee covers 15 pages (USD 100 for each page above).
Running text sets about 600 words a page in the class.

| # | Section | Floats |
|---|---|---|
| 1 | Introduction; abstract, keywords | Fig. 1 (one question trained in the two ways) |
| 2 | Related work | Table 1 (closest work by property) |
| 3 | Method | Fig. 2 (framework overview), Algorithm 1 |
| 4 | Experimental setup | Table 2 (federated setups) |
| 5 | Results and analysis; the ablation study is 5.3 | Table 3 and Fig. 3 (main results; EX by round), Fig. 4 (incorrect predictions by kind and round), Table 4 (ablations), Tables 5 and 6 (other models; other federated setups), Table 7 (Spider dev, Syn, Realistic, DK), Table 8 (cost) |
| 6, 7 | Discussion and limitations; Conclusion | |
| A, B | Appendix: the prompt; all settings | generated, no prose |

Numbers and tables: `tools/paper_numbers.py` writes one macro per cell
and one `tab_*.tex` per table from the committed evaluations (through
`paper/notes/tools/overview_results.py`; a row enters by one line in
`ARMS`) and lists the rows that wait in `generated/missing.txt`. The
Holm correction runs inside each table; a test is counted once, in the
first table that prints it, and the comparisons quoted only in the text
form a family of their own. `tools/paper_settings.py` writes the
settings from the committed configs. When an evaluation is committed
later: one line in `ARMS`, `make numbers`, `make`; the sentences that
use that row are read again and its `\expect` guesses replaced.

State (2026-11-28): Section 3 and Section 1 with the abstract are
drafted; Sections 2 and 4 to 7 hold a heading and its label; the
appendices and the statements exist.

| Step | What | Waits on |
|---|---|---|
| W1 | Section 3: the open points below | the owner: `REVIEW_NOTES.md`, A46 |
| W2 | Sections 4, 5, 6 with 7, then 2, in this order: 4 defines the statistical protocol that 5 and 6 rely on, and 5 gives 6 its findings | the rows that wait print `??` |
| W3 | Section 1 and the abstract brought up to date with Section 5: the open points below | W2 |
| W4 | The whole paper read end to end: repetition, terms, pages (`make inventory` before and after, so that no number and no reference changes); cold read, claim audit, cited-work audit | the owner and the advisor read |
| W5 | Statements, AI-use statement (section 8), public repository with code, splits and predictions, supplementary file, cover letter, `make submit` | authors, funding and competing interests from the owner |

Open points on the drafted sections:

- Section 3, opening paragraph: it says what the method does that is
  new; each contrast is made once (FedAvg SFT in 3.1, FedDPO in 3.6 and
  3.7).
- Section 3.4: $T_w = 0$ is a valid configuration, said in one
  sentence.
- Sections 3.2 and 3.4 use "labeled" and "unlabeled" before 3.5
  defines them, and 3.2 has two classes of sample where 3.5 has three;
  the pointer of 3.4 to the sampling protocol belongs to 3.5.
- Sections 3.5 and 3.6: the mechanics of the time limit, the three
  cases without a label and the replacement rule belong to Appendix B.
- Fig. 2: a caption of what the figure does not say; the two terms of
  the loss are named at Eq. (4).
- Section 1, results paragraph: four findings, each with at most one
  pair of numbers, the tests left to Section 5. The gain at equal
  rounds on both sets; further FedAvg SFT rounds do not close it (the
  BIRD peak, not the comparison with round 5 on Spider); above FedDPO
  on BIRD dev; execution errors halve while incorrect results rise, not
  significantly, with the direction said.
- Section 1: the sentence of the key observation as two sentences;
  contribution 3 with at most three findings and no counts in
  brackets; "the FedAvg SFT gap" is a phrase of the lab.
- Abstract: client compute named beside "unchanged communication
  cost".

Still to build in the tools: the time limits of the labeling step as
settings for Appendix B (constants of `fedls_sql/eval/sql_exec.py`),
Table 1 with its locators, the supplementary file (every McNemar test
with its adjusted p, pairs per client and round, the statistics of the
splits, EX by round of every row; Appendix B moves there first if the
pages run over).

## 7. Tools and folder

| Tool | Use |
|---|---|
| `make`, `make numbers`, `make figures`, `make floats` | the PDF (`build/main.pdf`); macros, tables and settings; charts; every float on its own |
| `make lint`, `make inventory` | `tools/lint.py`: numbers, references, journal form, lab words; the macros and citation keys of every section |
| `make overlap` | `tools/overlap.py` against the sources in `.sources/` |
| `make submit` | the flat source the journal asks for, compiled (`tools/flatten.py`); stops on a placeholder or a guess |
| `tools/abstracts.py`, `tools/table_lint.py`, `tools/pages.py` | abstracts of the references into `.sources/`; table conventions; the page count of a build |
| `cold-session` skill | isolated sessions on Opus: the cold reads |
| `/ars-citation-check`, `/ars-reviewer`, `/ars-disclosure` | single checks. The paper is not run through the ARS pipeline |
| TeX | TeX Live 2026 basic with the packages of `tsp.cls` in the user tree; the `Makefile` puts the `l3` folders of the system tree first on `TEXINPUTS` |

```text
paper/manuscript/
  main.tex  macros.tex  floats.tex  references.bib  Makefile
  Definitions/     the class of Tech Science Press
  sections/        00_abstract ... 07_conclusion, 90_statements_cmc, A_prompt, B_settings
  generated/       numbers, settings, tab_*.tex, missing.txt, the prompts
  figures/         fig_*.pdf (drawn in paper/figures/)
  CLAIMS.md  OUTLINE.md  TERMS.md  REVIEW_NOTES.md
  checks/          NN_checks.md, the fact rows of Section 2
  bib/report.md    how each reference was verified
  cold_reviews/    reports of the cold reads that are still open
  build/           outside Git: the PDF and what a build leaves
  .sources/        outside Git: arXiv sources for make overlap, abstracts.json,
                   examples/ (the example papers)
  tools/
```

`main_jiis.tex`, `sn-jnl.cls`, `sn-basic.bst`,
`sections/90_declarations.tex` and the `jiis` branches of the tools are
the JIIS fallback, not kept up. The files of the earlier workflow (the
briefs, outlines and notes of a separate writer, the voice and writing
guides) are at the tag `archive/writing-workflow-2026-11-28`.

## 8. CMC requirements

From the author instructions, read in full on 2026-11-26; `tools/lint.py
--journal cmc` and `tools/charts.py --journal cmc` check what can be
checked.

- Abstract: one paragraph of 200 to 400 words, no citation, ending with
  the main numbers; 3 to 10 keywords. An abbreviation is defined at
  first use in the abstract, in the text and at the first figure or
  table.
- Headings of at most three levels. Vancouver references with the DOI
  where one exists; at most 5 references in one bracket.
- Figures at most 16.51 cm wide and 20 cm high; labels in Arial or
  Helvetica of 8 pt or more; panels in one file, lettered A, B, C; line
  art as vector; no citation inside a figure.
- The setup names each piece of software with its version and maker,
  and the run parameters (Appendix B).
- Back matter in this order: acknowledgement, funding statement, author
  contributions (CRediT wording), availability of data and materials,
  ethics approval ("Not applicable"), conflicts of interest; then the
  appendices; then the references.
- No page limit; the fee covers 15 pages (USD 100 for each page above).
- Submission: one ZIP with all sources and images, under 200 MB; a
  cover letter (original, unpublished, not under review elsewhere,
  approved by all authors, the commitment to pay the charge). The first
  and the corresponding author cannot change after submission.
- AI tools: use that changes wording or structure is disclosed in the
  acknowledgement (tool, purpose, how the authors reviewed the output),
  and the caption of a diagram prepared with an AI tool names the tool
  and its version.

The AI-use statement (owner, 2026-11-26: it follows what published
papers write, and states the purpose as it is), in the Acknowledgement:
"During the preparation of this manuscript, the authors used Claude
(Anthropic; model Claude Fable 5.2) for drafting and revising the text
from the authors' results, analyses and outline, and for assistance in
writing the code of the experiments. The authors subsequently reviewed
and revised the relevant content and accept full responsibility for the
article."
