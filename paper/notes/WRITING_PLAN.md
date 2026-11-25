# FedLS-SQL: writing plan

Written 2026-11-26. How the manuscript is written: who does what, the
writer and what it is given, the structure of the paper, its tables and
figures, the checks, the steps in order, the tools. What the paper
claims and which rows exist is in `RESEARCH_STATE.md` (sections 3.1,
3.4, 5.0); this file does not repeat it.

## 1. Choices

| Part | Choice |
|---|---|
| Who writes | writer agents, one section at a time, in the order of section 8. The main session coordinates and writes no prose of the paper |
| The writer | a professor of data science presenting finished work, whose question is where the supervision comes from (section 3); few constraints, its own judgement on how a section is built |
| Format | LaTeX, to the JIIS shape first (25 pages, the tighter of the two). Section bodies live in `sections/*.tex` with no class-specific command, so a CMC version is a second main file (section 10) |
| Class | Springer Nature `sn-jnl` (December 2024 package), `\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}`, BibTeX with `sn-basic.bst` |
| Place | `paper/manuscript/` in the paper repository; one commit per accepted section |
| Numbers | a script writes macros and tables from the committed evaluations (section 6); a result number in the text is a macro |
| Names | the method is `\method` and the paper says "the model", so the title can change without touching the text |

## 2. Who does what

| Role | Does | Does not |
|---|---|---|
| Owner | approves `CLAIMS.md` and each packet's content, reads each section, decides | |
| Main session | builds the numbers, the packets and the voice folder; starts the writer; runs the checks; turns what they find into a few editor's notes; makes mechanical fixes itself (a term, a macro, a label) | draft or rewrite sentences of the paper: it carries the lab's vocabulary, history and rules |
| Writer (subagent) | writes one section from its packet, decides its structure, answers the editor's notes | read the notes of the lab |
| Helpers (subagents) | build `references.bib`, audit claims, read the PDF cold | talk to the writer |

One section moves through this loop, and the next starts when it is
accepted, because a later section reads the earlier ones:

```text
packet (main session, owner reads)
  -> draft (a fresh writer: WRITER.md, voice/, the packet, the accepted sections)
  -> build and checks (main session, helpers)
  -> at most five editor's notes -> the same writer revises   (two rounds at most)
  -> owner reads -> commit
```

The bibliography, the numbers, the charts and the audits run beside the
writer; two writers never run at once.

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
> run any query the model writes and see whether the answer is right,
> and that check can be made only where the database is. Federated
> learning is the setting in which this matters and Text-to-SQL the
> task in which an answer can be checked by running it; you know both
> fields and write about them from this point of view. The experiments
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
  checked against the code. No prose, so there is none to copy.
- The tables of the section, and each macro with its value beside it.
- References: key, and one line on what the paper did.
- Length in words.
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

Budget for 25 pages in `sn-jnl`, references included; it is measured on
the first build with empty tables in place and corrected then. Results
follow research questions and the ablations have their own section, as
in the JIIS papers read (`JOURNAL_BAR.md`).

| # | Section | Pages | Content | Notes the packet is built from | Can be written |
|---|---|---:|---|---|---|
| | Title, abstract, keywords | 0.7 | title as "Name: mechanism for the task in the setting"; abstract of 150 to 250 words with one number (the gain on BIRD); 4 to 6 keywords | `JOURNAL_BAR.md` 3 | last |
| 1 | Introduction | 1.8 | small models for Text-to-SQL where data cannot be pooled; FedAvg SFT learns from one gold SQL and never uses the databases, federated DPO as published keeps its first pairs and reference; execution is available only at the client; the method in three sentences; headline results; that "federated Text-to-SQL" here means training; 4 contributions, the last the released code, splits and predictions | `RESEARCH_STATE.md` 3.1; `LITERATURE.md` 1.22 | after 5 and 6 |
| 2 | Related work | 2.0 | 2.1 small models for Text-to-SQL; 2.2 preference optimization and execution feedback for SQL and code; 2.3 federated fine-tuning of language models, federated DPO; 2.4 federated semantic parsing and Text-to-SQL; Table 1 | `LITERATURE.md` 1.2, 1.3, 1.4, 1.22, 2; `DPO_RESEARCH.md` 2, 7; `RESEARCH_STATE.md` 3.6 | now |
| 3 | Method | 4.0 | 3.1 setting and notation; 3.2 overview, Fig. 1; 3.3 SFT warm-up rounds; 3.4 a preference round: sampling, execution labels, pairs, the DPO + NLL loss with the round's global model as reference, aggregation; Algorithm 1; 3.5 what it costs a client | `RESEARCH_STATE.md` 3.2, 3.3 (settings), 3.8; `DPO_RESEARCH.md` 3.1 to 3.4; the loss in `fedls_sql/training/dpo.py` | now |
| 4 | Experimental setup | 2.5 | datasets and metrics; federated setups, Table 2; models; the six baselines; implementation (prompt, LoRA, rates, rounds, sampling, decoding, seed, serving); McNemar test with Holm correction | `RESEARCH_STATE.md` 2, 3.4; `FEDERATED_DATA_SETUP.md` 3, 4 | now |
| 5 | Results | 6.0 | RQ1 against the baselines (Table 3, Fig. 2); RQ2 other models and federated setups (Tables 4, 5); RQ3 perturbed questions and test-suite accuracy (Table 6); RQ4 what changes in the errors and what it costs (Fig. 3, Table 7) | `RESEARCH_STATE.md` 5.0; generated tables | each part when its rows are in |
| 6 | Ablation study | 2.0 | on-policy rounds, the NLL term, the preference term, the number of warm-up rounds, aggregation weights, pooled clients (Table 8) | `RESEARCH_STATE.md` 5.0, second table | when its rows are in |
| 7 | Discussion and limitations | 1.3 | why the two kinds of round remove different errors; the scope of the setting: clients hold gold SQL and databases that can be queried, full participation with 5 to 10 clients, isolation of data and not differential privacy, added client compute | `RESEARCH_STATE.md` 3.1, 5.0 | after 5 and 6 |
| 8 | Conclusion | 0.4 | | | last |
| | Declarations | 0.4 | funding, competing interests, data availability, code availability, author contributions, use of AI tools | `JOURNAL_BAR.md` 1 | last, by the main session |
| | References | 3.0 | 45 to 55 entries | | grows with the text |
| A, B | Appendix | 1.0 | A the prompt as the model saw it; B all settings in one table | `LITERATURE.md` 1.19 | now, by the main session (no prose) |

Supplementary file (outside the 25 pages): every McNemar test with its
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

The writer may propose another table or figure in its notes (a worked
example of a pair, a small diagram); the owner decides.

## 7. Checks

Applied to the draft by the main session and the helpers; the writer
does not see this section.

Five checks stop a section:

| Check | Tool | Stops on |
|---|---|---|
| Build | `make` | the section does not compile; an undefined reference |
| Numbers | `tools/lint.py` | a result number that is not a macro |
| References | `tools/lint.py`, `/ars-citation-check` | a key that is not in `references.bib`; an entry without DOI or arXiv id |
| Truth | claim audit: a helper with all the notes looks for a committed result that contradicts a sentence | a false or overstated sentence; a part called essential without its ablation row; a framing taken from the story of 2026-11-17 where the results of `RESEARCH_STATE.md` 5.0 have moved on |
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
| W1 | TeX packages, the folder of section 9, `main.tex` with empty sections | `make` gives a PDF | a few minutes of install |
| W2 | `paper_numbers.py`, the eight table files, `charts.py` for Fig. 2 and 3 | every cell equals the overview page; `missing.txt` equals the missing rows of section 6 | none |
| W3 | `CLAIMS.md`: the thesis in one sentence, 4 contributions, each claim with its macros, the sets it holds on and its ceiling, the limitations the paper states, the term sheet and the notation | owner approves | owner, 30 min |
| W4 | `references.bib`: a helper takes the papers of `LITERATURE.md` and `DPO_RESEARCH.md` section 7 that the outline cites, fetches each entry from its DOI or arXiv id, prefers the published version, records how far the paper was read | `/ars-citation-check` clean | none |
| W5 | `WRITER.md` as in section 3.2; `voice/`: passages, profile, `section_rhetoric.md` | owner reads the role and the passages | owner, 20 min |
| W6 | pilot: the packet of section 3.4 written by the writer on Opus and on the session model | owner reads both without the names and picks the model; role and packet format corrected from what the drafts show | owner, 20 min |
| W7 | Method and Algorithm 1, then Experimental setup; appendix A and B by the main session | loop of section 2 | owner, 30 min each |
| W8 | Related work, Table 1 | same | owner, 30 min |
| W9 | Results, part by part as `missing.txt` empties; Ablation study | same; a part is not written around `--` cells | waits for the GPU rows |
| W10 | Discussion and limitations, Conclusion, Introduction, abstract, title, keywords | same | owner, 1 h |
| W11 | whole paper: one writer reads it end to end and evens it out; `humanizer` with a voice passage as sample; reader test; `/ars-reviewer`; claim audit of the full text; page count | owner and advisor read | advisor's time |
| W12 | declarations, AI-use statement (`/ars-disclosure`), public repository with code, splits and predictions, cover letter | the submission files compile from a clean copy | owner, 1 h |

W1 to W8 need no result that is missing and can start now. When an
evaluation is committed later: one line in `ARMS`, `make numbers`,
`make`, and the claim audit runs again for the claims that use that row.

## 9. Tools and folder

| Tool | Use | On the Mac |
|---|---|---|
| `pdflatex`, `bibtex` (TeX Live 2026 basic), `make` | build; Springer requires that the source compiles with pdflatex | installed |
| TeX packages `sttools`, `threeparttable`, `appendix`, `ncctools`, `algorithms` | needed by `sn-jnl.cls` and its template (it stops at `cuted.sty` today) | missing: `tlmgr --usermode install sttools threeparttable appendix ncctools algorithms`, not yet run |
| `paper/notes/tools/overview_results.py` | every committed run and McNemar test, imported by `paper_numbers.py` | exists |
| `paper/figures/render.py`, `STYLE.md`; matplotlib | diagrams; result charts at 119 mm in Arial 8 pt | exists; installed |
| PaperOrchestra port (`github.com/Ar9av/PaperOrchestra`, MIT, read at `fcf8a38`) | three files copied: `section_rhetoric.md` into `voice/`, `reverse_outline.py` and `table_lint.py` into `tools/` | not installed as a skill |
| ARS `shared/style_calibration_protocol.md` | how the voice profile is drawn from the passages | installed |
| `/ars-citation-check`, `/ars-reviewer`, `/ars-disclosure` | reference metadata; cold review; AI-use statement | installed |
| `humanizer` | last pass; it edits style and keeps every claim | installed |
| `doc-coauthoring`, stage 3 | the reader test | installed |
| `write-course-term-paper`: `references/writing.md`, `scripts/audit_reader_facing_prose.py` | model for the leak signals of `tools/lint.py`, rewritten for English and LaTeX | installed |

Not used as a writer: the ARS draft writer (a fixed paragraph scheme, a
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
  generated/            numbers.tex, tab_*.tex, missing.txt
  figures/              fig_*.pdf
  references.bib
  sn-jnl.cls  sn-basic.bst
  CLAIMS.md             thesis, contributions, claims with macros, sets and ceiling,
                        limitations, term sheet, notation
  WRITER.md             the role of section 3.2
  voice/                passages, profile.md, section_rhetoric.md
  packets/              one file per section
  tools/                paper_numbers.py charts.py lint.py reverse_outline.py table_lint.py
  Makefile
```

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

## 11. Open with the owner

1. The JIIS submission guidelines, read in a browser (Springer sends
   automated requests to a login page): the class it names
   (`JOURNAL_BAR.md` records the older macro with `smallcondensed`;
   Springer's LaTeX page says `sn-jnl` serves every Springer Nature
   journal), the page format the 25 pages are counted in, whether the
   manuscript is anonymised.
2. Springer Nature's rule on figures made with AI tools, for Fig. 1.
3. Which journal goes first. This plan assumes JIIS.
4. The model of the writer: Opus by the rule for subagents, or the
   session model; step W6 decides.
5. The voice passages of section 3.4: the four proposed sources, or
   others.
6. Whether the whole experimental picture of a part enters its table.
   Example: on-policy rounds are above fixed pairs on BIRD and level
   with them on Spider test; with the Spider column in Table 8 the claim
   is stated for BIRD.
7. The angle of the role (section 3.1): supervision, with federated
   learning as the setting and Text-to-SQL as the task.
