# FedLS-SQL: writing plan

Written 2026-11-26. How the manuscript is written: format, tools, the
structure of the paper, its tables and figures, and the steps in order.
What the paper claims and which rows exist is in `RESEARCH_STATE.md`
(sections 3.1, 3.4, 5.0); this file does not repeat it.

## 1. Fixed choices

| Part | Choice |
|---|---|
| Format | LaTeX, written to the JIIS shape first (25 pages, the tighter of the two). Section bodies live in `sections/*.tex` with no class-specific command, so a CMC version is a second main file, not a rewrite (section 9) |
| Class | Springer Nature `sn-jnl` (December 2024 package), `\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}`, BibTeX with `sn-basic.bst` |
| Place | `paper/manuscript/` in the paper repository; one commit per section |
| Who writes | a writer subagent, started fresh for each section and given only that section's packet (section 7). The main session prepares the packets and runs the checks; it does not draft, because it carries the lab's vocabulary, history and rules. Other subagents build the bibliography, audit claims and read the PDF cold |
| Numbers | no result number is typed. A script writes macros and tables from the committed evaluations (section 5) |
| Names | the method is `\method` and the paper says "the model", so the title can change without touching the text |
| What a writer reads | `WRITER.md` (its role and reader), `voice/` (profile and exemplar passages), the packet of its section, the sections already accepted. Not the notes, not `AGENTS.md`, not the checks of section 8 |

Three things to check by hand before step W7; they could not be read
on 2026-11-26 because Springer sends automated requests to a login page:

1. The JIIS submission guidelines: the class it names (`JOURNAL_BAR.md`
   records the older Springer macro with `smallcondensed`; Springer's
   LaTeX page says `sn-jnl` serves every Springer Nature journal), the
   page format the 25 pages are counted in, and whether the manuscript
   is anonymised.
2. Springer Nature's rule on figures made with AI tools, for Fig. 1.
3. Which journal goes first. This plan assumes JIIS.

## 2. Tools

| Tool | Use | On the Mac |
|---|---|---|
| `pdflatex`, `bibtex` (TeX Live 2026 basic) | build; Springer requires that the source compiles with pdflatex | installed |
| TeX packages `sttools`, `threeparttable`, `appendix`, `ncctools`, `algorithms` | needed by `sn-jnl.cls` and its template (the template stops at `cuted.sty` today) | missing |
| `make` | `make` (pdflatex, bibtex, pdflatex twice), `make numbers`, `make lint`; `latexmk` is not needed | installed |
| `paper/notes/tools/overview_results.py` | `build()` returns every committed run (EX, difficulty levels, execution errors, wrong results, result commit) and every McNemar test; the paper's script imports it | exists |
| `paper/figures/render.py`, `STYLE.md` | diagrams (Fig. 1 exists) | exists |
| matplotlib | result charts, drawn at 119 mm in Arial 8 pt from the same data | installed with Python 3.11 |
| `pdftotext` | page and word counts, text for the cold reader | installed |
| `/ars-citation-check` | reference metadata against DOI and arXiv | installed |
| `/ars-reviewer` | cold read of the PDF as a journal reviewer | installed |
| `/ars-disclosure` | the AI-use statement | installed |
| `humanizer` | last pass on the prose, with an exemplar passage as its voice sample; it edits style and keeps every claim, so it does not remove content that should not be there | installed |
| ARS `shared/style_calibration_protocol.md` | the voice profile, extracted from the exemplar papers instead of the author's past papers | installed |
| ARS `references/intro_title_rhetoric_guide.md`, `abstract_writing_guide.md` | the moves of the introduction and the abstract, used when their packets are built | installed |
| ARS `references/writing_quality_check.md` | list for the edit pass (openers that say nothing, meta-commentary, triples, synonym cycling) | installed |
| PaperOrchestra port (`github.com/Ar9av/PaperOrchestra`, MIT, read at `fcf8a38`): `skills/shared/section_rhetoric.md` | paragraph roles by section, used when a packet is built: the abstract templates, the introduction's chain from the limit of prior work and its cause to why the method works, design then motivation then advantage in a method subsection, the three questions of the experiments, limitations stated as the scope of the setting | not installed; the file is copied into `voice/` |
| PaperOrchestra port: `reverse_outline.py`, `table_lint.py` | checks: the first sentences of the paragraphs read as the argument of a section; booktabs rules, metric direction in the header, decimals | not installed; the two scripts are copied into `tools/` |
| `doc-coauthoring`, stage 3 | the reader test: a fresh subagent reads the PDF and answers set questions | installed |
| `write-course-term-paper`: `references/writing.md`, `scripts/audit_reader_facing_prose.py` | the model for the leak rules of `tools/lint.py` (internal files, commands, defensive provenance, defence of a rejected method, text that certifies a requirement), rewritten for English and LaTeX | installed |

Install, not yet run:

```
tlmgr --usermode install sttools threeparttable appendix ncctools algorithms
```

Not used: `/ars-full` and `/ars-plan` (they start from a literature
search and a dialogue and know nothing of the committed results); the
ARS draft writer (a general template: a fixed paragraph scheme, a list
of hedging verbs, sections it must include, a self-score against its
contract); `write-course-term-paper` as a skill (it is scoped to course
papers and asks for their voice); the PaperOrchestra pipeline as a
whole (its writer gets the full experimental log in one call and is
told to analyse what did not work, its literature agent searches for
new citations and must use 90% of them, its tables are typed by the
model from the log, and its refinement loop accepts a revision by the
score of a simulated reviewer); Word, Overleaf. No installed skill
drafts a machine learning journal paper well; the writer is a role of
our own (section 7).

## 3. Folder

```
paper/manuscript/
  main.tex              JIIS wrapper: class, title, abstract, \input of the sections
  sections/             01_intro 02_related 03_method 04_setup 05_results
                        06_ablation 07_discussion 08_conclusion 90_declarations
                        A_prompt B_settings
  generated/            numbers.tex, tab_*.tex, missing.txt (written by the script, committed)
  figures/              fig_*.pdf (copied from paper/figures and the chart script)
  references.bib
  sn-jnl.cls  sn-basic.bst
  CLAIMS.md             thesis, contributions, claims with their keys and wording strength,
                        the limitations the paper states, terms and notation
  WRITER.md             the writer's role and reader
  voice/                profile.md, exemplar passages by section type
  packets/              one file per section: what the writer is given
  tools/paper_numbers.py  tools/charts.py  tools/lint.py
  Makefile
```

## 4. Structure of the paper

Budget for 25 pages in `sn-jnl`, references included; it is measured on
the first build with empty tables in place and corrected then. Results
follow research questions and the ablations have their own section, as
in the JIIS papers read (`JOURNAL_BAR.md`).

| # | Section | Pages | Content | Notes to read | Can be written |
|---|---|---:|---|---|---|
| | Title, abstract, keywords | 0.7 | title as "Name: mechanism for the task in the setting"; abstract of 150 to 250 words with one number (the gain on BIRD); 4 to 6 keywords | `JOURNAL_BAR.md` 3 | last |
| 1 | Introduction | 1.8 | small models for Text-to-SQL where data cannot be pooled; FedAvg SFT learns from one gold SQL and never uses the databases, federated DPO as published keeps its first pairs and reference; execution is available only at the client; the method in three sentences; headline results; a sentence that "federated Text-to-SQL" here means training, not querying federated databases; 4 contribution bullets, the last the released code, splits and predictions | `RESEARCH_STATE.md` 3.1; `LITERATURE.md` 1.22 | after 5 and 6 |
| 2 | Related work | 2.0 | 2.1 small models for Text-to-SQL; 2.2 preference optimization and execution feedback for SQL and code; 2.3 federated fine-tuning of language models, federated DPO; 2.4 federated semantic parsing and Text-to-SQL; Table 1 | `LITERATURE.md` 1.2, 1.3, 1.4, 1.22, 2; `DPO_RESEARCH.md` 2, 7; `RESEARCH_STATE.md` 3.6 | now |
| 3 | Method | 4.0 | 3.1 setting and notation (clients, databases, questions, what leaves a client); 3.2 overview, Fig. 1; 3.3 SFT warm-up rounds; 3.4 a preference round: sampling, execution labels, pairs, the DPO + NLL loss with the round's global model as reference, aggregation; Algorithm 1; 3.5 what it costs a client | `RESEARCH_STATE.md` 3.2, 3.3 (settings), 3.8; `DPO_RESEARCH.md` 3.1 to 3.4 | now |
| 4 | Experimental setup | 2.5 | datasets and metrics; federated setups, Table 2; models; the six baselines; implementation (prompt, LoRA, rates, rounds, sampling, decoding, seed, serving); McNemar test with Holm correction | `RESEARCH_STATE.md` 2, 3.4; `FEDERATED_DATA_SETUP.md` 3, 4 | now |
| 5 | Results | 6.0 | RQ1 against the baselines (Table 3, Fig. 2); RQ2 other models and federated setups (Tables 4, 5); RQ3 perturbed questions and test-suite accuracy (Table 6); RQ4 what changes in the errors and what it costs (Fig. 3, Table 7) | `RESEARCH_STATE.md` 5.0; generated tables | each part when its rows are in |
| 6 | Ablation study | 2.0 | on-policy rounds, the NLL term, the preference term, the number of warm-up rounds, aggregation weights, pooled clients (Table 8) | `RESEARCH_STATE.md` 5.0, second table | when its rows are in |
| 7 | Discussion and limitations | 1.3 | why the two kinds of round differ in the errors they remove; limits: clients need gold SQL and databases that can be queried, full participation and 5 to 10 clients, isolation of data and not differential privacy, added client compute | `RESEARCH_STATE.md` 3.1, 5.0 | after 5 and 6 |
| 8 | Conclusion | 0.4 | | | last |
| | Declarations | 0.4 | funding, competing interests, data availability, code availability, author contributions, use of AI tools | `JOURNAL_BAR.md` 1 | last |
| | References | 3.0 | 45 to 55 entries | | grows with the text |
| A, B | Appendix | 1.0 | A the prompt as the model saw it; B all settings in one table | `LITERATURE.md` 1.19 | now |

Supplementary file (outside the 25 pages): every McNemar test with its
adjusted p, pairs per client and round, cosine of the client updates,
the per-client statistics of the five splits, EX by round of every line.

## 5. Tables and figures

`tools/paper_numbers.py` imports `build()`, writes one macro per cell
(`\ex{bird}{k2}{4}`, `\gain{...}`, `\pval{...}`) and one `tab_*.tex` per
table, prints `--` for a row that is not committed and lists those rows
in `generated/missing.txt`. The Holm correction runs over the tests the
paper prints. A row enters a table by one line in `ARMS` of
`overview_results.py`, as for the overview page.

| Item | Content | Rows still missing (2026-11-26) |
|---|---|---|
| Fig. 1 | method overview | none (`paper/figures/fig_method_overview.svg`) |
| Algorithm 1 | the method: k warm-up rounds, then preference rounds | none |
| Table 1 | closest work by property: federated, execution labels, on-policy pairs, NLL term, model size (FL4SP, OpenFedLLM, CodeLutra, ExCoT, ours) | none |
| Table 2 | the five federated setups: clients, split, questions and databases per client | none, read from the split files |
| Table 3 | main: BIRD dev and Spider test; no training, local SFT, centralized SFT, FedAvg SFT, FedProx SFT, federated DPO as published, the method; EX, difficulty levels, gain and p against FedAvg SFT | BIRD: local SFT, centralized SFT, FedProx, federated DPO, second seed of two rows. Spider: local SFT, FedProx, federated DPO round 2 |
| Fig. 2 | EX by round, FedAvg SFT (to round 5) and the method, both datasets | none |
| Table 4 | three models on Spider, DeepSeek-Coder-1.3B on BIRD | DeepSeek rounds on Spider; all of BIRD |
| Table 5 | FedAvg SFT and the method in the five setups | IID, alpha 0.5 with 5 clients, alpha 0.5 with 10 clients |
| Table 6 | Spider-Syn, Realistic, DK; test-suite accuracy | the test-suite numbers are not committed |
| Fig. 3 | wrong answers by round split into execution errors and wrong results, FedAvg SFT and the method | none |
| Table 7 | client time per round (sampling, labels, training) and megabytes sent | none, read from the logs (`scripts/log_times.py`) |
| Table 8 | ablations at 4 rounds, BIRD and Spider | BIRD: without the preference term round 2, without NLL, k = 0 rounds 3 and 4, k = 3. Spider: without the preference term round 2, pooled clients |

## 6. Steps

Each step ends at its gate. Times are the owner's and the machine's,
estimates.

| Step | What | Gate | Time |
|---|---|---|---|
| W0 | the three checks of section 1 | answers written into section 1 | owner, 15 min |
| W1 | TeX packages, the folder of section 3, `main.tex` with empty sections | `make` gives a PDF | a few minutes of install |
| W2 | `paper_numbers.py`, the eight table files, `charts.py` for Fig. 2 and 3 | every cell equals the overview page; `missing.txt` equals the missing rows of section 5 | none |
| W3 | `CLAIMS.md`: the thesis in one sentence, 4 contributions, each claim with the macros that carry it, the sets it is stated for and the verb it is stated with, the limitations the paper states, the terms and the notation | owner approves | owner, 30 min |
| W4 | `references.bib`: a subagent takes the papers of `LITERATURE.md` and `DPO_RESEARCH.md` section 7 that the outline cites, fetches each entry from its DOI or arXiv id, prefers the published version, and records how far the paper was read (full or abstract) | `/ars-citation-check` clean; no entry typed by hand | none |
| W5 | `WRITER.md` and `voice/`: exemplar passages by section type from GradeSQL, CodeLutra and two JIIS papers of `JOURNAL_BAR.md`, and the profile extracted from them | owner reads the profile | owner, 15 min |
| W6 | pilot: the packet of section 3.4 (a preference round), drafted from the same packet by the writer on Opus and on the session model | owner reads both without the names and picks the model; the draft is read for the failures of section 7 and the packet format is corrected | owner, 20 min |
| W7 | Method, Algorithm 1, Experimental setup, appendix A and B | per-section loop below | owner, 30 min each |
| W8 | Related work, Table 1 | same | owner, 30 min |
| W9 | Results, part by part as `missing.txt` empties; Ablation study | same; a part is not written around `--` cells | waits for the GPU rows |
| W10 | Discussion and limitations, Conclusion, Introduction, abstract, title, keywords | same | owner, 1 h |
| W11 | whole paper: one edit pass for consistency, `humanizer`, the reader test, `/ars-reviewer`, claim audit of the full text, page count against 25 | owner and advisor read | advisor's time |
| W12 | declarations, AI-use statement (`/ars-disclosure`), public repository with code, splits and predictions, cover letter | submission files compile from a clean copy | owner, 1 h |

W1 to W8 need no result that is missing and can start now. When an
evaluation is committed later: one line in `ARMS`, `make numbers`,
`make`, and the claim audit runs again for the claims that use that row.

Per-section loop (W7 to W10):

1. The main session writes the packet (section 7.2).
2. A fresh writer drafts the section from the packet.
3. `make` and `make lint`.
4. Claim audit: a subagent with all the notes (`RESEARCH_STATE.md`,
   `LAB_LOG.md`) looks for a committed result that contradicts each
   sentence. It reports false or overstated sentences only; it does not
   ask for caveats or for the story of how a value was chosen.
5. The main session turns what the checks found into editor's notes
   (section 7.4) and the same writer revises once. A second round at
   most; what is left the owner edits by hand.
6. Owner reads, commit.

## 7. The writer

The failures to expect from a writing agent in this workspace have one
cause: what the agent has read. An agent that has read the lab's rules
writes to satisfy them, one that has read the lab's notes writes in
their voice and tells their history, and one that knows every result
reports every result. So the writer is given a role, a reader and the
material of one section, and the rules are applied by other steps after
the draft.

### 7.1 Role (`WRITER.md`)

The writer is the author of the paper, a researcher in Text-to-SQL and
federated learning presenting finished work to the readers of the
journal. Its reader is a reviewer who knows the field and has never
seen this project. It is told what a section is for and what the reader
should know at its end; it is not told what to avoid. `WRITER.md` holds
no project rule, no honesty rule, no list of forbidden words and no
list of objections a reviewer might raise.

`AGENTS.md` is loaded into every agent of the workspace. Whether a
subagent receives it has not been checked; `WRITER.md` therefore opens
by saying that the workspace files are the operating rules of the
experiment agents and that the writer's material is its packet.

### 7.2 Packet (one file per section)

Written by the main session from `CLAIMS.md` and the notes, in the
paper's terms. This is the step where lab language becomes paper
language, once, and the owner can read it before any prose exists.

- What the section is for, what the reader knows before it and has to
  know after it.
- The points to make, in order, each with the evidence that carries it
  (a table, a figure, a citation) and the verb it is stated with
  (from `CLAIMS.md`: "outperforms", "improves", "is level with").
- The facts as values, in tables and lists, never in prose the writer
  could copy: settings, counts, formulas checked against the code.
- The generated tables, and each macro with its value beside it, so the
  writer chooses the numbers that make its point.
- Citation keys, each with one line on what the paper did.
- The length in words, and one or two exemplar passages of the same
  section type.

Not in a packet: dates, names of runs, what was tried and dropped, how
a value was chosen, results the paper does not print, limitations
(they are in the packet of the Discussion alone, as the list approved
in `CLAIMS.md`).

### 7.3 Failures and what guards against each

| Failure | Where it comes from | Guard |
|---|---|---|
| Stiff, simplified prose | the notes and `AGENTS.md` are written in plain short sentences for the owner, and a writer takes the voice of its sources; lists of rules make it cautious | the packet holds no prose; voice comes from `voice/` (exemplars of the journal's register) |
| Process in the text ("we first", "was then selected", dates, run names, how k was set) | the notes are a history | the packet carries values without history; the writer cannot open the notes; `tools/lint.py` |
| Writing for the rules: sentences that certify ("all numbers come from", "no test data was used"), that defend a choice nobody questioned, that answer a reviewer in advance | the writer has read rules, checklists and reviewer objections and treats them as its audience | none of them reaches the writer; the checks run after the draft and speak to it only through editor's notes |
| Too much disclosed: results that weaken the paper, every negative finding, a caveat after each number | a model's default, made stronger by honesty rules and by sources that list everything measured | what the paper prints is decided in `CLAIMS.md` and the tables; a packet holds only that; limitations have one place and a fixed list |
| Hedging ("may", "appears to", "it is worth noting") | default register of a model; the ARS writer asks for it | the verb of each claim is given; significance is a mark in the table and one paragraph of the setup, not a p-value per sentence; the edit pass removes the rest |
| A results section that reads the table aloud, or gives each row equal space | the notes report every row | the packet names one point per paragraph and which result leads |
| Flat or timid introduction and contributions | the same caution | the packet states the contributions in the wording approved in `CLAIMS.md`; the moves of the introduction follow the rhetoric guide |
| Promotional words, the opposite failure | default register | `humanizer`, claim audit |
| Lab words ("student", "line", "row", "arm", "read", "k2") | the notes and the code | the terms of `CLAIMS.md` in every packet; `tools/lint.py` |
| Formulas and settings from memory | the writer knows DPO in general | formulas and values come from the packet, checked against the code |
| Citations from memory | same | only keys given in the packet |
| Checkers that add caveats back | an auditor with all the notes sees every exception | the auditor reports false sentences only; the main session filters its findings before they become notes |
| Bland prose after many rounds | each pass removes what stands out | two revision rounds at most; one edit pass over the whole paper |

### 7.4 Editor's notes

What a check finds goes back to the writer as a note a human editor
would write, about the reader and the sentence: "the reader does not
need to know how this value was reached; state the value", "this
paragraph makes two points; the second belongs to section 6". A note
never cites a rule, a lint name or a project file.

## 8. Checks

These are applied to the draft and are not shown to the writer.

| Check | Tool | Fails on |
|---|---|---|
| Build | `make` | undefined reference or citation, overfull table |
| Numbers | `tools/lint.py` | a digit with a decimal point or a percent sign in sections 5 to 7 that is not a macro |
| Words | `tools/lint.py` | student, owner, queued, held-out, run names, em dash |
| Leaks | `tools/lint.py` | file paths and commands, "we first", "initially", "was then chosen", "after trying", sentences that certify ("all numbers", "no test data", "strictly", "it should be noted", "we acknowledge") |
| Hedges | `tools/lint.py`, reported as a count per section | "may", "might", "appears to", "seems", "potentially", "to some extent" outside the limitations |
| Bibliography | `tools/lint.py`, `/ars-citation-check` | entry without DOI or arXiv id, uncited entry, citation of a preprint that has a published version |
| Claims | subagent, section 6 | a sentence a committed result contradicts; a part called essential without its ablation row; a framing taken from the story of 2026-11-17 where the results of section 5.0 have moved on |
| Argument | `tools/reverse_outline.py`, read by the main session | a section whose first sentences do not make its argument; a paragraph with two points |
| Tables | `tools/table_lint.py` | rules outside booktabs, a metric without its direction, uneven decimals |
| Reader | reader test (`doc-coauthoring`, stage 3): a fresh subagent reads the PDF and states the problem, the method, the main result and what the paper seemed to defend or explain about its own making | a wrong answer to the first three; anything named in the fourth |
| Review | `/ars-reviewer` on the PDF alone | reported to the owner; a comment is acted on when the paper gets better, not because it was made |
| Length | `pdftotext`, page count | more than 25 pages; abstract outside 150 to 250 words |

What the audits hold the text to:

- The setup is given as values. How a seed, a round, k or a setting was
  picked is not told. No sentence is false: a number chosen on Spider
  test is not called held-out, and the BIRD rows are BIRD dev.
- A claim names the set it holds on. Example: on-policy rounds are
  above fixed pairs on BIRD; on Spider test the two are level, so the
  paper does not say "on both datasets".
- A statement about another paper comes from a section of
  `LITERATURE.md` or `DPO_RESEARCH.md`; a paper read by abstract is
  cited only for what its abstract states. External result rows name
  their prompt, decoding and training data, or are left out.
- Numbered citations; an acronym is defined at first use in the
  abstract and again in the text.

## 9. A CMC version

Same sections and tables, a second wrapper `main_cmc.tex` on the Tech
Science Press class (`TSP-Latex.zip`: `tsp.cls`, `vancouver.bst`):

- abstract of 200 to 400 words ending with the main numbers; 3 to 10
  keywords;
- statements as the class commands (acknowledgement, funding, author
  contributions, availability of data and materials, ethics approval,
  conflicts of interest); appendices before the references;
- figures at most 16.51 cm wide, labels in Arial or Helvetica of 8 pt
  or more (the figure standard already meets this);
- no page limit; the fee covers 15 pages, so the supplementary tables
  may move into the appendix only if the pages are paid for;
- use of AI tools that changes wording or structure is disclosed in the
  acknowledgement, and the caption of a diagram prepared with an AI
  tool names the tool and its version (author instructions, read
  2026-11-26);
- the class needs `CJKutf8`, `verse`, `bbm` and `mathcomp`, not
  installed.
