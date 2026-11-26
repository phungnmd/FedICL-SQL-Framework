# FedLS-SQL: writing plan

Written 2026-11-26 and revised the same day after the owner's review.
How the manuscript is written: who does what, the writer and what it is
given, the structure of the paper, its tables and figures, the checks,
the steps in order, the tools. What the paper
claims and which rows exist is in `RESEARCH_STATE.md` (sections 3.1,
3.4, 5.0); this file does not repeat it.

## 1. Choices

| Part | Choice |
|---|---|
| Who writes | writer agents, one section at a time, in the order of section 8. The main session coordinates and writes no prose of the paper |
| The writer | a professor of data science presenting finished work, whose question is where the supervision comes from (section 3); few constraints, its own judgement on how a section is built. It runs on Fable 5.2 at high effort (owner, 2026-11-26) |
| Helpers | bibliography, audits and the reader test run on Opus |
| Format | LaTeX, to the JIIS shape first (25 pages, the tighter of the two; the writers' budgets sum to 23, section 5). Section bodies live in `sections/*.tex` with no class-specific command, so a CMC version is a second main file (section 10) |
| Class | Springer Nature `sn-jnl` (December 2024 package), `\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}`, BibTeX with `sn-basic.bst` |
| Place | `paper/manuscript/` in the paper repository; one commit per accepted section |
| Numbers | a script writes macros and tables from the committed evaluations, and the settings from the committed configs (section 6); a result number in the text is a macro |
| Names | the method is `\method` and the paper says "the model", so the title can change without touching the text |

## 2. Who does what

| Role | Does | Does not |
|---|---|---|
| Owner | approves `CLAIMS.md` and each packet's content, reads each section, decides | |
| Main session | builds the numbers, the packets and the voice folder; starts the writer; runs the checks; turns what they find into a few editor's notes; makes mechanical fixes itself (a term, a macro, a label) | draft or rewrite sentences of the paper: it carries the lab's vocabulary, history and rules |
| Writer (subagent, Fable 5.2 at high effort) | writes one section from its packet, decides its structure, answers the editor's notes | read the notes of the lab |
| Helpers (subagents, Opus) | build `references.bib`, audit claims and statements about other papers, read the PDF cold | talk to the writer |

One section moves through this loop, and the next starts when it is
accepted, because a later section reads the earlier ones:

```text
packet (main session, owner reads)
  -> draft (a fresh writer: WRITER.md, voice/, the packet, the accepted sections)
  -> build and checks (main session, helpers)
  -> at most five editor's notes -> the same writer revises   (two rounds at most)
  -> owner reads -> commit
```

A writer is given `WRITER.md`, `voice/`, its packet and the accepted
sections, and nothing else. The bibliography, the numbers, the charts
and the audits run beside the writer; two writers never run at once.

## 3. The writer

### 3.1 Why it is set up this way

What a writing agent produces follows from what it has read. Given the
lab's rules it writes to satisfy them; given the lab's notes it takes
their voice and tells their history; knowing every result it reports
every result; given a long list of things to avoid it becomes cautious
and flat. So the writer gets a role, a reader and the material of one
section. Rules are few and stated once. What the lab needs enforced is
checked after the draft (section 7) and reaches the writer only as an
editor's note.

The angle of the role (proposed 2026-11-26, owner to confirm): the
professor asks where the supervision comes from. It is the one-sentence
story of `RESEARCH_STATE.md`, section 3.1, taken as the author's point
of view. Federated learning is the setting and Text-to-SQL the task;
the paper presents itself neither as an aggregation method nor as a
Text-to-SQL system. Its weight then rests on the rows that are
strongest, the method against FedAvg SFT on both datasets, and on the
analysis of where the gain sits (which errors go, which answers are
right by result and not by the form of the gold SQL). The federated
design point, a round as one re-sampling step with the round's global
model as reference, is the second claim and is stated where it is
measured (BIRD).

### 3.2 The role (`WRITER.md`, in full)

> You are the author of this paper: a professor of data science whose
> work is on what a model can learn from when data cannot be pooled,
> and who writes and reviews for the journals this paper is going to.
> In any project your first question is where the supervision comes
> from. Here the answer is the paper. An organisation that holds a
> database holds more than labelled questions: it holds the means to
> run any query the model writes and compare its result with the result
> of the gold SQL, and that comparison can be made only where the
> database is. Execution turns the one gold SQL of a question into many
> right and wrong queries of the model's own. Federated learning is the
> setting in which this matters and Text-to-SQL the task in which a
> query can be checked by running it; you know both fields and write
> about them from this point of view. The experiments
> are finished. What remains is the part a senior author keeps for
> themselves: making a reader understand what was done, why it works
> and what it is worth.
>
> Your reader reviews for the journal. They know SQL and fine-tuning;
> they may not know preference optimization or federated learning in
> detail; they have never seen this project. They read the abstract,
> the introduction and the tables first and decide there whether to
> trust the rest.
>
> Write as you would for that reader.
>
> - Lead with the idea. Before a formula or a number, say what it is
>   for.
> - Explain why. A design choice answers a problem; a result has a
>   cause. A table shows the numbers and your text says what they mean.
> - Claim what the evidence carries, plainly. Do not undersell a clear
>   result and do not decorate a small one.
> - Be exact where it matters: definitions, notation, what is compared
>   with what.
> - Use an example where it teaches faster than a definition: a
>   question, a wrong SQL, the correct one.
> - Treat earlier work as a colleague would: say precisely what it did
>   and where this paper goes further.
>
> You decide the paragraphs, their order, the emphasis, which numbers
> to quote and where a figure or an example helps. The packet of a
> section tells you what the section has to establish and gives you the
> facts, results and references for it. Take facts, formulas and
> references from the packet, write result numbers with its macros, and
> use the names of the term sheet so the paper speaks with one
> vocabulary. If you need something the packet lacks, or think a point
> is weak or belongs elsewhere, say so in your notes instead of filling
> it from memory.
>
> This file, the voice folder and your packet are what you work from.
> The other files of this workspace are the lab's records for running
> experiments and are not material for the paper.
>
> Return the section as LaTeX and, under it, a few lines to the editor:
> what you would add if you had it, and what you doubt.

### 3.3 What binds the writer, and what is its own

Four things bind it, all in the role above: facts, formulas and
references come from the packet; result numbers are macros; names come
from the term sheet; the section keeps to its length within a tenth.
The term sheet states what a label is, in the words of the role: a
sampled query is correct when its result equals the result of the gold
SQL on the client's database, so execution turns one gold SQL into many
right and wrong queries of the model's own. The paper never says that
execution shows whether an answer is right without the gold SQL.

Everything else is the writer's: how many paragraphs and in what order,
what leads, which of the available numbers appear in the text, whether
a subsection is split or merged, whether an example or a small figure
is added, how a transition is made. The paragraph roles of section 4
are an offer, and a writer that departs from them says why in its
notes. The writer's notes are read: a gap it names goes back into the
packet, and a claim it finds weak goes to the owner.

### 3.4 Voice (`voice/`)

Voice is shown, not specified. The folder holds four to six passages,
one or two per kind of section, from papers that are written the way
the role describes, and a half-page profile drawn from them (sentence
length, how a result is introduced, how a claim is worded, how earlier
work is named). Proposed sources, to be fetched and read in step W5:
the DPO paper (Rafailov et al.) for the exposition of a method, FedProx
(Li et al.) for federated framing and analysis, CodeS for Text-to-SQL
experiments, GradeSQL for the shape of a JIIS paper. The owner may
replace any of them, or add passages by an author whose writing the
paper should resemble.

The pilot (step W4) runs on a minimal folder: two passages, one of a
method exposition and one of an experimental section, with no profile.
The full folder follows in step W6, once the pilot reads well.

## 4. Packets (`packets/`, one file per section)

The packet is where the lab's language becomes the paper's, once, and
where the owner decides content before any prose exists. It is short:
one to two pages.

- What the section is for, what the reader knows before it and should
  know after it.
- What the section has to establish: two to five statements, each with
  its evidence (a table, a figure, a reference) and its ceiling, the
  strongest wording the evidence carries and the sets it holds on. The
  writer may say less, in other words, in any order.
- The facts as values, in tables and lists: settings, counts, formulas
  checked against the code. No prose, so there is none to copy. The
  settings come from `generated/settings.md`, written from the
  committed configs (section 6).
- The tables of the section, and each macro with its value beside it.
- References: key, and one line on what the paper did.
- For Related work, in place of one line per reference: the facts the
  comparison needs, one row per fact (the cited paper, what it did or
  reported as a value, and the locator in that paper: section, table,
  equation or page, or the file and line of its released code). Every
  cell of Table 1 is such a row. A sentence about another paper is
  written from these rows (section 7).
- Length in words, from the page budget of section 5.
- Paragraph roles that usually serve this kind of section, as an offer
  (from `voice/section_rhetoric.md`: for an introduction, the limit of
  earlier work with its cause, then why this method removes it; for a
  method subsection, design, motivation, advantage; for experiments,
  the three questions; limitations as the scope of the setting).

A packet holds what the paper prints. Dates, names of runs, what was
tried and dropped, how a value was chosen and results outside the
tables are not in it. The limitations are in the packet of the
Discussion, as the list approved in `CLAIMS.md`.

## 5. Structure of the paper

The limit is 25 pages in `sn-jnl`, references included. The budgets
below sum to 23, so two pages are left for what the first full build
shows; a packet gives its section this budget in words. Appendix B is
the first thing to move to the supplementary file when the count runs
over. Results follow research questions and the ablations have their
own section, as in the JIIS papers read (`JOURNAL_BAR.md`).

| # | Section | Pages | Content | Notes the packet is built from | Can be written |
|---|---|---:|---|---|---|
| | Title, abstract, keywords | 0.7 | title as "Name: mechanism for the task in the setting"; abstract of 150 to 250 words with one number (the gain on BIRD); 4 to 6 keywords | `JOURNAL_BAR.md` 3 | last |
| 1 | Introduction | 1.7 | small models for Text-to-SQL where data cannot be pooled; FedAvg SFT learns from one gold SQL and never uses the databases, federated DPO as published keeps its first pairs and reference; execution is available only at the client; the method in three sentences; headline results; that "federated Text-to-SQL" here means training; 4 contributions, the last the released code, splits and predictions | `RESEARCH_STATE.md` 3.1; `LITERATURE.md` 1.22 | after 5 and 6 |
| 2 | Related work | 1.8 | 2.1 small models for Text-to-SQL; 2.2 preference optimization and execution feedback for SQL and code; 2.3 federated fine-tuning of language models, federated DPO; 2.4 federated semantic parsing and Text-to-SQL; Table 1 | `LITERATURE.md` 1.2, 1.3, 1.4, 1.22, 2; `DPO_RESEARCH.md` 2, 7; `RESEARCH_STATE.md` 3.6 | now |
| 3 | Method | 3.7 | 3.1 setting and notation; 3.2 overview, Fig. 1; 3.3 SFT warm-up rounds; 3.4 a preference round: sampling, execution labels, pairs, the DPO + NLL loss with the round's global model as reference, aggregation; Algorithm 1; 3.5 what it costs a client | `RESEARCH_STATE.md` 3.2, 3.3 (settings), 3.8; `DPO_RESEARCH.md` 3.1 to 3.4; the loss in `fedls_sql/training/dpo.py` | now |
| 4 | Experimental setup | 2.3 | datasets and metrics; federated setups, Table 2; models; the six baselines; implementation (prompt, LoRA, rates, rounds, sampling, decoding, seed, serving); McNemar test with Holm correction | `RESEARCH_STATE.md` 2, 3.4; `FEDERATED_DATA_SETUP.md` 3, 4 | now |
| 5 | Results | 5.5 | RQ1 against the baselines (Table 3, Fig. 2); RQ2 other models and federated setups (Tables 4, 5); RQ3 perturbed questions and test-suite accuracy (Table 6); RQ4 what changes in the errors and what it costs (Fig. 3, Table 7) | `RESEARCH_STATE.md` 5.0; generated tables | each part when its rows are in; the parts whose rows are complete (Fig. 2, Fig. 3, Table 7) as soon as the Setup section is accepted |
| 6 | Ablation study | 1.8 | on-policy rounds, the NLL term, the preference term, the number of warm-up rounds, aggregation weights, pooled clients (Table 8) | `RESEARCH_STATE.md` 5.0, second table | when its rows are in |
| 7 | Discussion and limitations | 1.2 | why the two kinds of round remove different errors; the scope of the setting: clients hold gold SQL and databases that can be queried, full participation with 5 to 10 clients, isolation of data and not differential privacy, added client compute | `RESEARCH_STATE.md` 3.1, 5.0 | after 5 and 6 |
| 8 | Conclusion | 0.3 | | | last |
| | Declarations | 0.4 | funding, competing interests, data availability, code availability, author contributions, use of AI tools | `JOURNAL_BAR.md` 1 | last, by the main session |
| | References | 2.8 | 45 to 55 entries | | grows with the text |
| A, B | Appendix | 0.8 | A the prompt as the model saw it; B all settings in one table, generated from the committed configs, with each piece of software, its version and its maker | `LITERATURE.md` 1.19; `generated/tab_settings.tex` | now, by the main session (no prose) |

Supplementary file (`ESM_1.pdf`, outside the 25 pages): Appendix B if the
count runs over, every McNemar test with its
adjusted p, pairs per client and round, cosine of the client updates,
the per-client statistics of the five splits, EX by round of every line.

## 6. Tables and figures

`tools/paper_numbers.py` imports `build()` of
`paper/notes/tools/overview_results.py`, writes one macro per cell
(`\ex{bird}{k2}{4}`, `\gain{...}`, `\pval{...}`) and one `tab_*.tex` per
table, prints `--` for a row that is not committed and lists those rows
in `generated/missing.txt`. The Holm correction runs over the tests the
paper prints. A row enters a table by one line in `ARMS`, as for the
overview page.

Settings are generated the same way. `tools/paper_settings.py` reads the
committed records of the runs the paper prints (the `config.json` of
the FedAvg SFT rounds and of the evaluations, the `setup.json`,
`arm.json` and `round.json` of the preference rounds) and writes
`generated/settings.tex` (one macro per setting: LoRA, rates, rounds,
samples, pairs, decoding, software versions), `generated/tab_settings.tex`
(Appendix B) and `generated/settings.md` (the same values for the Setup
packet). It stops when two runs of one line disagree on a setting. A
setting in the text is a macro, like a result number.

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
| Table 6 | Spider-Syn, Realistic, DK; test-suite accuracy | none (the test-suite numbers are committed) |
| Fig. 3 | wrong answers by round split into execution errors and wrong results, FedAvg SFT and the method | none |
| Table 7 | client time per round (sampling, labels, training) and megabytes sent | none, read from the logs (`scripts/log_times.py`) |
| Table 8 | ablations at 4 rounds, BIRD and Spider | BIRD: without the preference term round 2, without NLL, k = 0 rounds 3 and 4, k = 3. Spider: without the preference term round 2, pooled clients |

The writer may propose another table or figure in its notes (a worked
example of a pair, a small diagram); the owner decides.

## 7. Checks

Applied to the draft by the main session and the helpers; the writer
does not see this section.

Six checks stop a section:

| Check | Tool | Stops on |
|---|---|---|
| Build | `make` | the section does not compile; an undefined reference |
| Numbers | `tools/lint.py` | a result number or a setting that is not a macro |
| References | `tools/lint.py`, `/ars-citation-check` | a key that is not in `references.bib`; an entry without DOI or arXiv id |
| Truth | claim audit: a helper with all the notes looks for a committed result that contradicts a sentence | a false or overstated sentence; a part called essential without its ablation row; a framing taken from the story of 2026-11-17 where the results of `RESEARCH_STATE.md` 5.0 have moved on |
| Other papers | cited-work audit: a helper lists every sentence that states something about a cited paper, and every cell of Table 1, and finds its row in the packet's facts with the locator; it then opens the paper at that locator | a statement about a cited paper without a row or a locator; a row the paper at its locator does not support. Applies to Section 2 in full and to any such sentence elsewhere |
| Length | page count | the paper over 25 pages; the abstract outside 150 to 250 words |

The claim audit reports false sentences. It does not ask for caveats,
for results the paper leaves out, or for the story of how a value was
chosen.

The rest is advice. The main session reads it and decides what is worth
a note:

| Signal | Tool | Looks for |
|---|---|---|
| The lab showing through | `tools/lint.py` | file paths, commands, "we first", "was then chosen", sentences that certify ("all numbers come from", "no test data was used"), a choice defended that nobody questioned |
| Hedging | `tools/lint.py`, a count per section | "may", "appears to", "it is worth noting" outside the limitations |
| Lab words | `tools/lint.py` | student, arm, queued, run names; fixed by the main session directly |
| Argument | `tools/reverse_outline.py` | the first sentences of a section do not make its argument; a paragraph with two points |
| Tables | `tools/table_lint.py` | rules outside booktabs, a metric without its direction, uneven decimals; fixed in the generator |
| Reader | reader test (step W11): a fresh helper reads the PDF and states the problem, the method, the main result, and anything the paper seemed to defend or explain about its own making | a wrong answer to the first three; anything named in the fourth |
| Review | `/ars-reviewer` on the PDF (step W11) | goes to the owner; a comment is acted on when the paper gets better |

Editor's notes. What goes back to the writer is at most five notes a
round, the ones that matter most, written as an editor would: about the
reader and the sentence ("the reader does not need how this value was
reached; give the value", "this paragraph makes two points; the second
is the topic of section 6"). A note names no rule, check or project
file. The writer may disagree in its reply, and a disagreement with a
reason is settled by the owner. After two rounds what is left is edited
by the owner.

## 8. Steps

Times are the owner's and the machine's, estimates.

| Step | What | Done when | Time |
|---|---|---|---|
| W0 | owner's checks (section 11, items 1 to 3) | answered | owner, 15 min |
| W1 | TeX packages, the folder of section 9, `main.tex` with empty sections, the `make submit` target | `make` gives a PDF | a few minutes of install |
| W2 | `paper_numbers.py`, the eight table files, `paper_settings.py`, `charts.py` for Fig. 2 and 3, `lint.py` | every cell equals the overview page; `missing.txt` equals the missing rows of section 6; every setting traces to a committed config | none |
| W3 | `CLAIMS.md`: the thesis in one sentence, 4 contributions, each claim with its macros, the sets it holds on and its ceiling, the hedges that must survive revision, the limitations the paper states, the term sheet and the notation | owner approves | owner, 30 min |
| W4 | pilot: `WRITER.md` as in section 3.2, a minimal `voice/` (section 3.4), and the packet of section 3.4 of the paper written by the writer. It tests the role and the packet, the assumption the whole setup rests on. Before it starts the owner gives the wording of the AI-use statement (section 11, item 8) | owner reads the draft; role and packet format corrected from what it shows | owner, 20 min |
| W5 | `references.bib`: a helper takes the papers of `LITERATURE.md` and `DPO_RESEARCH.md` section 7 that the outline cites, fetches each entry from its DOI or arXiv id, prefers the published version, records how far the paper was read | `/ars-citation-check` clean | none |
| W6 | the full `voice/`: passages, profile, `section_rhetoric.md` | owner reads the passages | owner, 20 min |
| W7 | Method and Algorithm 1, then Experimental setup; appendix A and B by the main session; then the parts of Results whose rows are complete (Fig. 2, Fig. 3, Table 7) | loop of section 2 | owner, 30 min each |
| W8 | Related work, Table 1, with the cited-work audit | same | owner, 30 min |
| W9 | the other parts of Results, as `missing.txt` empties; Ablation study | same; a part is not written around `--` cells | waits for the GPU rows |
| W10 | Discussion and limitations, Conclusion, Introduction, abstract, title, keywords | same | owner, 1 h |
| W11 | whole paper: one writer reads it end to end and evens it out, and the macros and `\cite` keys of every section are listed before and after that pass and compared (`make inventory`), so the pass changes no number and no reference; the `writing_quality_check` of the academic-paper skill as a diagnostic that rewrites nothing; reader test; `/ars-reviewer`; claim audit of the full text; page count | owner and advisor read | advisor's time |
| W12 | declarations, AI-use statement (`/ars-disclosure`), public repository with code, splits and predictions, cover letter, `make submit` | the submission files compile from a clean copy | owner, 1 h |

The order was revised on 2026-11-26 (owner): the pilot, W6 in the first
version, runs right after `CLAIMS.md` as W4, and the bibliography and
the full voice folder (W4 and W5 before) follow it as W5 and W6. No
text passes through a humanizer.

W1 to W8 need no result that is missing and can start now. When an
evaluation is committed later: one line in `ARMS`, `make numbers`,
`make`, and the claim audit runs again for the claims that use that row.

## 9. Tools and folder

| Tool | Use | On the Mac |
|---|---|---|
| `pdflatex`, `bibtex` (TeX Live 2026 basic), `make` | build; Springer requires that the source compiles with pdflatex | installed |
| TeX packages `sttools`, `threeparttable`, `appendix`, `ncctools`, `algorithms`, `algorithmicx`, `multirow` | needed by `sn-jnl.cls` and its template | installed in the user tree (`~/Library/texmf`) |
| `paper/notes/tools/overview_results.py` | every committed run and McNemar test, imported by `paper_numbers.py` | exists |
| `paper/figures/render.py`, `STYLE.md`; matplotlib | diagrams; result charts at 119 mm in Arial 8 pt | exists; installed |
| PaperOrchestra port (`github.com/Ar9av/PaperOrchestra`, MIT, read at `fcf8a38`) | three files copied: `section_rhetoric.md` into `voice/`, `reverse_outline.py` and `table_lint.py` into `tools/` | not installed as a skill |
| ARS `shared/style_calibration_protocol.md` | how the voice profile is drawn from the passages | installed |
| `/ars-citation-check`, `/ars-reviewer`, `/ars-disclosure` | reference metadata; cold review; AI-use statement | installed |
| academic-paper skill, `references/writing_quality_check.md` | a diagnostic in step W11: it lists what it finds and rewrites nothing | installed |
| `doc-coauthoring`, stage 3 | the reader test | installed |
| `write-course-term-paper`: `references/writing.md`, `scripts/audit_reader_facing_prose.py` | model for the leak signals of `tools/lint.py`, rewritten for English and LaTeX | installed |

Not used: `humanizer` (owner, 2026-11-26: no pass that rewrites the
text after the writers). Not used as a writer: the ARS draft writer (a fixed paragraph scheme, a
list of hedging verbs, sections it must include, a self-score), the
PaperOrchestra pipeline (its writer gets the whole experimental log in
one call and is told to analyse what did not work; its literature agent
searches for new citations and must use 90% of them; its refinement
accepts a revision by the score of a simulated reviewer),
`write-course-term-paper` as a skill (course papers and their voice),
`/ars-full` and `/ars-plan`.

```text
paper/manuscript/
  main.tex              JIIS wrapper: class, title, abstract, \input of the sections
  sections/             01_intro 02_related 03_method 04_setup 05_results
                        06_ablation 07_discussion 08_conclusion 90_declarations
                        A_prompt B_settings
  generated/            numbers.tex, tab_*.tex, missing.txt,
                        settings.tex, tab_settings.tex, settings.md
  figures/              fig_*.pdf
  references.bib
  sn-jnl.cls  sn-basic.bst
  CLAIMS.md             thesis, contributions, claims with macros, sets and ceiling,
                        limitations, term sheet, notation
  WRITER.md             the role of section 3.2
  voice/                passages, profile.md, section_rhetoric.md
  packets/              one file per section
  tools/                paper_numbers.py paper_settings.py charts.py lint.py
                        flatten.py reverse_outline.py table_lint.py
  Makefile              make, make numbers, make figures, make lint,
                        make inventory, make submit
```

Where each requirement of sections 10 and 10.1 is built in:

| Requirement | Tool |
|---|---|
| Abstract length and form (JIIS 150 to 250 words, CMC 200 to 400; one paragraph, no citation, no undefined abbreviation), keyword count, an abbreviation defined at first use, headings of at most three levels, a footnote that is only a citation, more than 5 references in one bracket (CMC), a reference without DOI or arXiv id, a caption ending in a full stop (JIIS) | `tools/lint.py --journal jiis` or `cmc` |
| Figure width (119 mm JIIS, at most 165.1 mm CMC) and height (at most 195 mm, 200 mm), Arial or Helvetica of one size from 8 pt, lines of 0.3 pt or more, fonts embedded, vector output, no title inside the figure, panel letters a, b, c (JIIS) or A, B, C (CMC), series told apart by marker and dash | `tools/charts.py --journal jiis` or `cmc` |
| Software with version and maker, and the run parameters | `tools/paper_settings.py`, Appendix B |
| Table footnotes under the table with superscript lower-case letters | the table generator (`threeparttable`) |
| One `.tex` file without `\input`, the `.bbl` pasted in, no subfolders, figures named `Fig1`, `Fig2`, the class and style files beside it, the compiled PDF | `make submit` (`tools/flatten.py`), which also compiles the flat copy |
| Compiles on TeX Live 2018 (Editorial Manager) | the preamble holds only the packages of the Springer template (`graphicx`, `multirow`, `amsmath`, `amssymb`, `amsfonts`, `amsthm`, `mathrsfs`, `appendix`, `xcolor`, `textcomp`, `manyfoot`, `booktabs`, `algorithm`, `algorithmicx`, `algpseudocode`, `listings`), and `lint.py` stops on any other `\usepackage` |

## 10. A CMC version

Same sections and tables, a second wrapper `main_cmc.tex` on the Tech
Science Press class (`TSP-Latex.zip`: `tsp.cls`, `vancouver.bst`):

- abstract of 200 to 400 words ending with the main numbers; 3 to 10
  keywords;
- statements as the class commands (acknowledgement, funding, author
  contributions, availability of data and materials, ethics approval,
  conflicts of interest); appendices before the references;
- figures at most 16.51 cm wide, labels in Arial or Helvetica of 8 pt
  or more (the figure standard already meets this);
- no page limit; the fee covers 15 pages;
- use of AI tools that changes wording or structure is disclosed in the
  acknowledgement, and the caption of a diagram prepared with an AI
  tool names the tool and its version (author instructions, read
  2026-11-26);
- the class needs `CJKutf8`, `verse`, `bbm` and `mathcomp`, not
  installed.

From the same page, read in full on 2026-11-26, and not yet in the
tools:

- figures at most 20 cm high; the panels of a figure in one file,
  lettered A, B, C at the top left; no citation of the form "[n]"
  inside a figure; line art as vector or at 900 dpi or more
  (`charts.py`);
- the abstract is one paragraph without citations; an abbreviation is
  defined at first use in the abstract, in the text and at the first
  figure or table (`tools/lint.py`);
- Vancouver references with the DOI where one exists; at most 5
  references in one bracket (`tools/lint.py`);
- the setup names each piece of software with its version and maker,
  and the run parameters (Appendix B);
- the AI disclosure in the acknowledgement names the tool, the purpose
  and how the authors reviewed the output;
- back matter in this order: acknowledgement, funding statement, author
  contributions (CRediT wording), availability of data and materials
  (one of the journal's template sentences, with the code link), ethics
  approval ("Not applicable"), conflicts of interest; then the
  appendices; then the references;
- submission: one ZIP with all sources and images, under 200 MB; a
  cover letter that states the work is original, unpublished and not
  under review elsewhere, that all authors approved it, any ethics,
  copyright or conflict issue, and the commitment to pay the charge;
  the first and the corresponding author cannot be changed after
  submission.

### 10.1 JIIS: the submission guidelines

Read on 2026-11-26 from the owner's PDF of the page (saved the same
day), with Springer Nature's LaTeX support page and its group page on
AI. The page confirms `JOURNAL_BAR.md`: 25 pages with references,
tables and figures; LaTeX only; an abstract of 150 to 250 words without
undefined abbreviations or unspecified references; 4 to 6 keywords.

- Class: the page names two. Its Text part recommends "Springer
  Nature's LaTeX template" (`sn-jnl`, December 2024, which serves "any
  Springer Nature journal"); its Author tools part asks for "Springer's
  LaTeX macro package" with the option "smallcondensed", which belongs
  to the older `svjour3` class. The format the 25 pages are counted in
  is not stated. The plan keeps `sn-jnl`.
- Review model: not stated. The title page carries the authors and
  nothing asks for an anonymised manuscript.
- Submission: the source with all style files and figures, and a PDF of
  the compiled output; no subfolders; figure files named `Fig1`, `Fig2`
  and so on; no custom fonts; the content of the `.bbl` pasted into the
  `.tex`. A `make submit` target builds this flat copy from the working
  folder. The system is Editorial Manager, which compiles on TeX Live
  2018, so the preamble keeps to the packages of the template and to
  options that exist in that release.
- Text: decimal headings of at most three levels; an abbreviation
  defined at first mention; a footnote is never only a citation.
- References: numbers in square brackets, `sn-basic.bst`, the DOI as a
  full link; the list holds works that are published or accepted, so a
  preprint gives way to its published version where one exists; a
  dataset is cited with its identifier.
- Figures: 119 mm wide and at most 195 mm high; Arial or Helvetica of
  one size between 8 and 12 pt; lines of 0.3 pt or more; fonts
  embedded; no title inside the figure; parts labelled a, b, c (CMC
  asks for A, B, C, so `charts.py` takes the journal as an option);
  series told apart by marker or dash and not by colour alone; a
  caption without a full stop at its end; a figure in an appendix
  continues the numbering of the text.
- Tables: footnotes under the table, marked by superscript lower-case
  letters.
- Declarations before the references: funding, competing interests,
  data availability (required), code availability, author
  contributions. A submission without them is returned. Author
  contributions and competing interests are also entered in the
  submission form.
- Supplementary file: named `ESM_1.pdf`, cited in the text as "Online
  Resource 1", and carrying the title, the journal, the authors and the
  corresponding author's affiliation and e-mail.
- AI in the text: "Use of an LLM should be properly documented in the
  Methods section". "AI assisted copy editing" needs no declaration; the
  page defines it as improvements to human-generated text and says it
  does "not include generative editorial work and autonomous content
  creation". A text drafted by the writer is outside this exemption.
  The group page asks for an AI Use Declaration at the end of the paper
  and says copy editing "should be declared" as well; the journal's own
  page is the one followed here.
- AI in images: the page points to Springer's policy. The group page
  says "Generally no" for generative AI images, scientific diagrams
  included; tables, flow charts and simple graphs that contain no image
  are outside the rule. Charts drawn from the data by `charts.py` are
  outside it. Fig. 1 is the open case (section 11, item 2).
- Authors: the author group, its order and the corresponding author
  are fixed at submission and cannot change after acceptance; ORCID is
  recommended; suggested reviewers need an institutional e-mail.

## 11. Open with the owner

1. The JIIS submission guidelines were read (section 10.1). Two points
   the page leaves open: which class the 25 pages are counted in (it
   names both `sn-jnl` and the older macro with `smallcondensed`), and
   the review model. The plan writes in `sn-jnl` without anonymising; a
   question to the editorial office settles both if the owner wants
   certainty before submission. Until the owner says otherwise the
   paper is written in `sn-jnl` and is not anonymised.
2. Fig. 1 under Springer Nature's rule on images (section 10.1): a
   scientific diagram made with a generative AI tool is not accepted,
   a flow chart without images is outside the rule. Either the owner
   draws the figure, or the owner judges it a flow chart. CMC accepts
   an explanatory image made with an AI tool when its caption names
   the tool and version. The figure is not regenerated or restyled
   before the owner decides.
3. Which journal goes first. This plan assumes JIIS.
4. Closed (owner, 2026-11-26): the writer runs on Fable 5.2 at high
   effort; helpers and checks stay on Opus. The pilot tests the role
   and the packet, not two models.
5. The voice passages of section 3.4: the four proposed sources, or
   others.
6. Whether the whole experimental picture of a part enters its table.
   Example: on-policy rounds are above fixed pairs on BIRD and level
   with them on Spider test; with the Spider column in Table 8 the claim
   is stated for BIRD.
7. The angle of the role (section 3.1): supervision, with federated
   learning as the setting and Text-to-SQL as the task.
8. The wording of the AI-use statement, which the owner takes to the
   advisor. Both journals require one for a text drafted by an LLM
   (JIIS: in the Methods section or a suitable alternative part; CMC:
   in the acknowledgement, with the tool, the purpose and how the
   authors reviewed the output). The steps up to `CLAIMS.md` do not
   depend on it; the pilot starts after the owner's answer.
