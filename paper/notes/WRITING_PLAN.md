# FedLS-SQL: writing plan

How the manuscript is written: who does what, what the writer is given,
the structure of the paper, its tables and figures, the checks, the
steps in order, the tools. This is the state of 2026-11-26; how it was
reached (two pilots of Section 3.4, the ARS pipeline tried and dropped)
is in `LAB_LOG.md` under that date. What the paper claims and which
rows exist is in `RESEARCH_STATE.md` (sections 3.1, 3.4, 5.0) and
`paper/manuscript/CLAIMS.md`; this file does not repeat it.

## 1. Choices

| Part | Choice |
|---|---|
| Who writes | a writer agent, one top-level section at a time, in the order of section 8: first its outline of the section, then the prose (owner, 2026-11-26: an outline before the writing keeps the text from rambling). The main session coordinates and writes no prose of the paper |
| The writer | the author presenting finished work, in the register of the published papers of the field; its own judgement on how a section is built. It runs on Fable 5.2 at high effort (owner, 2026-11-26) |
| Constraints | few (owner, 2026-11-26). Four things bind the writer (section 3.3). Checks of words and of style are signals for the editor, never rules for the writer, and prose is not repaired word by word: rigid rules and word checks make it stiff and patched |
| When | the whole paper is drafted now (owner, 2026-11-26); a number that waits for its result is written with its macro and prints as `??` until the row is committed |
| Helpers | audits, look-ups and the reader test run on Opus |
| Format | LaTeX, to the JIIS shape first (25 pages, the tighter of the two; section 5). Section bodies live in `sections/*.tex` with no class-specific command, so a CMC version is a second main file (section 10) |
| Class | Springer Nature `sn-jnl` (December 2024 package), `\documentclass[pdflatex,sn-basic,Numbered]{sn-jnl}`, BibTeX with `sn-basic.bst`; not anonymised |
| Place | `paper/manuscript/` in the paper repository; one commit per accepted section, after the owner has read it |
| Numbers | a script writes macros and tables from the committed evaluations, and the settings from the committed configs (section 6); a result number in the text is a macro |
| Names | the method is `\method` and the paper says "the model", so the title can change without touching the text |

## 2. Who does what

| Role | Does | Does not |
|---|---|---|
| Owner | has approved `CLAIMS.md`, `TERMS.md` and the outline; approves each brief, reads each section before its commit, decides | |
| Main session | builds the numbers, the briefs and the voice folder; starts the writer; runs the checks; turns what they find into a few editor's notes; fixes what is mechanical itself (a macro, a label, a citation key, one of the earlier labels that `TERMS.md` replaced) | draft or rewrite sentences of the paper: it carries the lab's vocabulary, history and rules |
| Writer (subagent, Fable 5.2 at high effort) | writes one section from the guide, the term sheet, the voice folder and its brief; decides its structure; answers the editor's notes | read the notes of the lab |
| Helpers (subagents, Opus) | audit claims and statements about other papers, look up records, read the PDF cold | talk to the writer |

One section moves through this loop, and the next starts when it is
accepted, because a later section reads the earlier ones:

```text
brief of the section (main session; the owner approves it)
  -> outline of the section, one line per paragraph (a fresh writer: WRITING_GUIDE.md, TERMS.md, voice/, the brief, the accepted sections)
  -> the main session checks the outline against the brief and answers it (section 4.1)
  -> draft of the whole section (the same writer, from its outline)
  -> build, lint, facts against the code and the committed results; a helper reads the PDF of the section cold (main session, helpers)
  -> at most five editor's notes -> the same writer revises   (two rounds at most)
  -> the owner reads -> commit
```

One writer outlines, drafts and revises a section: it is continued, not
replaced by a new one. Two writers never run at once; the numbers, the
charts, the brief of the next section and the audits run beside the
writer. The tool that starts a subagent attaches `AGENTS.md` and the
index of the session memory to it, so the rule that the manuscript
follows the register of the field stands in `AGENTS.md` as well.

## 3. The writer

### 3.1 The principle

What a writing agent produces follows from what it has read. Given the
lab's rules it writes to satisfy them; given the lab's notes it takes
their voice and tells their history; knowing every result it reports
every result; given a long list of things to avoid, or a draft sent
back to have its words exchanged, it turns stiff and patched. So the
writer gets a reader, a register shown by published papers, and the
material of one section. Few things bind it, and each is stated once.
What the lab needs enforced is checked after the draft (section 7) and
reaches the writer only as an editor's note about the reader.

Three things follow.

- A section is written by one writer, from one brief, so that it reads
  as one piece. A subsection is not drafted on its own; the pilots of
  Section 3.4 were the exception.
- The writer outlines before it writes (section 4.1). The outline is
  its own plan, one line per paragraph, and it is what keeps a section
  to its points; no rule about wording does that.
- The writer is given no list of words to avoid, no count and no style
  figure. `TERMS.md` names the concepts the paper defines; ordinary
  words stay free.
- When a draft is far from the register of the field, the cause is in
  what the writer was given. The brief, the guide or the passages are
  corrected and the section is written again; the draft is not repaired
  sentence by sentence. The two pilots showed it: a role file and a
  packet in the plain words of the lab gave a draft in a spoken
  register with 35% of its words taken over from them, and the same
  section written from the guide, the term sheet and a brief in the
  terms of the field read as a paper.

The angle of the paper is supervision: where the training signal comes
from. Federated learning is the setting and Text-to-SQL the task; the
paper presents itself neither as an aggregation method nor as a
Text-to-SQL system. Its weight rests on the method against FedAvg SFT
on both datasets and on the analysis of where the gain sits. The guide
gives the writer this angle in its first section.

### 3.2 What the writer is given

| File | Holds |
|---|---|
| `WRITING_GUIDE.md` | about 100 lines: the paper and its reader; how it should read, as a description of the published papers and not as a list of rules; the four things that bind; what is the writer's own; what it returns |
| `TERMS.md` | the names of the paper's concepts, the abbreviations, the notation. Its third column lists only the lab words and the earlier labels a defined name replaces |
| `voice/` | passages from published papers by kind of section, and `style_profile.md` (section 3.4) |
| the brief of its section | section 4 |
| `sections/` | the sections already accepted |

Not given to it: the notes of the lab, `CLAIMS.md`, the outline, this
plan and its checks, and `voice/section_rhetoric.md`, whose paragraph
roles reach the writer through the brief.

### 3.3 What binds the writer, and what is its own

Four things bind it, all in the guide under "What binds":

1. Facts: every fact, formula and statement about a cited paper comes
   from the brief; a gap is named in the notes and not filled.
2. Claims: a sentence never claims more than the ceiling of its
   statement; a qualifier that bounds a finding stays; novelty is
   stated against the closest work. What lies above a ceiling is left
   out, not denied in print (section 4).
3. Numbers and names: results and settings are macros; the names and
   the notation are those of `TERMS.md`; citations and labels are those
   of the brief.
4. Form: the headings of the brief, the commands of the class, a length
   near the one the brief gives and not above its upper end.

The term sheet states what a label is: a sample is correct when its
execution result equals that of the gold SQL query on the client's
database. The paper never says that execution establishes correctness
without the gold SQL query.

Everything else is the writer's: how many paragraphs and in what order,
what leads, which of the available numbers appear in the text, whether
an example or a small figure is proposed, how a transition is made. The
paragraph roles of a brief are an offer. The writer's notes are read: a
gap it names goes back into the brief, and a claim it finds weak goes
to the owner.

### 3.4 Voice (`voice/`)

Voice is shown, not specified. The folder holds passages from published
papers, one file per kind of section, read from the arXiv sources of
seven papers: LoRA (ICLR 2022), FedProx (MLSys 2020) and FedAvg
(AISTATS 2017) for introductions and related work; DPO (NeurIPS 2023),
FedAvg, the test-suite paper (EMNLP 2020) and the Methodology of
GradeSQL (JIIS 2026) for the exposition of a method; CodeS (SIGMOD
2024), the test-suite paper, LoRA and GradeSQL for setup, results and
ablations; DPO for limitations. `voice/README.md` lists each passage
with its section. The owner may replace any of them.

`voice/style_profile.md` describes the register by kind of section,
measured in ten papers (the seven above, BIRD, CodeLutra and
OpenFedLLM; 52,000 words of body text): sentence and paragraph length,
word length, the share of "we" and of passive sentences, hedges,
citations per paragraph, and the terms the field uses. Its figures
describe a range and are not targets. The method section of CodeLutra
is in the measures and not among the passages: it describes the steps
this paper describes, and a draft written beside it would follow its
wording.

### 3.5 What is kept from ARS and PaperOrchestra

Both were read in their sources (the ARS `academic-paper` skill, 3.24.2;
PaperOrchestra at `fcf8a38`). Their methods of writing are kept; their
pipelines are not (section 9).

| From | Idea | Where it lives here |
|---|---|---|
| ARS | The register follows the conventions of the field and the journal, calibrated on published papers | `voice/`; the guide, "How it should read" |
| ARS, PaperOrchestra | Facts come only from the supplied material; a gap is named, not filled | the guide, "What binds", 1; numbers as generated macros |
| ARS | A claim never above its ceiling; under revision the sentence changes and the claim stays; novelty against the closest work, scoped | the guide, "What binds", 2 |
| ARS | Each section answers one question of the reader; a paragraph the paper would not miss goes | the Purpose row of a brief; the guide, "What is yours" |
| ARS | The moves of an introduction (territory, gap, what the paper does), the title and the abstract | the brief of the Introduction, from `references/intro_title_rhetoric_guide.md` and `abstract_writing_guide.md` of the skill |
| ARS | A review by an agent that has not seen the writing, two rounds at most; every reference verified against a fetched record | the cold read of section 7.2; `bib/report.md` |
| ARS, PaperOrchestra | An outline before the prose: the points of a section in order, each with the evidence it uses | the writer's outline (section 4.1) |
| PaperOrchestra | One paragraph, one point, stated in its first sentence; paragraph roles by kind of section | the guide, "How it should read"; `voice/section_rhetoric.md`, through the briefs |
| PaperOrchestra | One name per concept from abstract to conclusion | `TERMS.md` |
| PaperOrchestra | The writer sees the tables and figures it describes | a brief names their files (section 4) |
| PaperOrchestra | The failure modes of a generated paper: a method described otherwise than the code, an invented number or reference, a part called essential without its ablation, a framing the results have overtaken | the stops of section 7.1 |
| PaperOrchestra | A revision changes no number and no reference | `make inventory` before and after the whole-paper pass |
| PaperOrchestra | The argument read from the first sentences alone; table conventions | `tools/reverse_outline.py`, `tools/table_lint.py` (signals) |

Left out on purpose: a fixed scheme for every paragraph, lists of words
for the writer, a score the writer gives itself, a loop that accepts a
revision by the score of a simulated reviewer, and the instruction to
report what did not work.

## 4. Briefs (`briefs/`, one file per top-level section)

The brief is where the lab's language becomes the paper's, once, and
where the owner decides content before any prose exists. It covers a
whole section (`briefs/03_method.md`, `briefs/04_setup.md` and so on),
with one block per subsection, is written in the terms of `TERMS.md`,
and holds no sentence that could stand in the paper: statements as
short entries, facts as tables. A writer takes over the sentences it is
given, so a brief gives it none.

- Place in the paper: the headings and their labels, what stands before
  and after the section, its purpose, and its length: the words of the
  outline as the upper end and about 10% less as the length asked for
  (section 5).
- What each subsection has to establish: two to five statements, each a
  short entry with its claim, its evidence (a table, a figure, a
  reference) and its ceiling, the strongest wording the evidence
  carries and the sets it holds on. The writer may say less, in other
  words, in any order.
- The facts as values, in tables and lists: settings, counts, formulas
  checked against the code. The settings come from
  `generated/settings.md`, written from the committed configs
  (section 6).
- The tables and figures of the section by file
  (`generated/tab_*.tex`, `figures/fig_*.pdf`), which the writer opens,
  so that what it says of a figure is what the figure shows; and each
  macro with exactly what it prints, unit included.
- References: the key, and the facts about that paper the section may
  use.
- For Related work, in place of one line per reference: the facts the
  comparison needs, one row per fact (the cited paper, what it did or
  reported as a value, and the locator in that paper: section, table,
  equation or page, or the file and line of its released code). Every
  cell of Table 1 is such a row. A sentence about another paper is
  written from these rows (section 7).
- The labels the section may refer to.
- Paragraph roles that usually serve this kind of section, as an offer
  (from `voice/section_rhetoric.md`; for the Introduction, the title
  and the abstract also from the two guides named in section 3.5).

A brief holds what the paper prints. Dates, names of runs, what was
tried and dropped, how a value was chosen and results outside the
tables are not in it. The limitations are in the brief of the
Discussion, as the list approved in `CLAIMS.md`. The outline
(`paper/manuscript/OUTLINE.md`, approved 2026-11-26) gives each section
its content and its claims; a brief is built from its entry there and
from `bib/report.md`, which names the sources of each subsection.

A brief states what the method does and does not grade it (owner,
2026-11-26). A ceiling is the strongest wording allowed and the sets it
holds on. It is not a list of what the paper does not claim, and no
entry calls a part of the method minor, a setting or "not the
contribution": the writer prints what it is given. The Method brief
said that two settings were "not the contribution", and the draft said
"The rest are settings". What the paper owes its reader is the credit
to earlier work (what it did, what is taken from it), the qualifiers
that belong to a claim, and the limitations of the Discussion brief. A
caution beyond these is the editor's to check in the draft (section 7),
not an entry of the brief.

`briefs/3.4_preference_round.md`, the brief of the second pilot, is the
model for the block of one subsection. The Method brief takes it over
as its block for Section 3.4.

### 4.1 The outline of a section

`OUTLINE.md` is the outline of the paper: sections, subsections, claims
and words. The outline of a section goes one level down and is written
by the writer, before any prose, into the file its brief names
(`briefs/03_method_outline.md`): one line per paragraph, in order, with
the point of the paragraph, the statement of the brief it serves, the
equation, table or figure it carries and its rough length. The lines
are notes and not sentences of the paper.

The main session checks it against the brief and answers in a few
lines:

- every statement of the brief has a line, and no line is without a
  statement or a need of the reader;
- read alone and in order, the lines make the argument of the section;
- each equation, table and figure has its place, and nothing is said
  twice;
- no line promises more than the ceiling of its statement;
- the lengths sum to the length of the brief.

The writer then drafts from it. The outline is a plan and not a
contract: the writer may depart from it and says so in its notes. The
owner sees the outline with the draft, and is asked before the draft
only when the outline departs from the brief or from `OUTLINE.md` (a
statement dropped, subsections reordered, the length exceeded). After
the draft, the first sentences of its paragraphs
(`tools/reverse_outline.py`) are read beside the outline.

## 5. Structure of the paper

The limit is 25 pages in `sn-jnl`, references included. Results follow
research questions and the ablations have their own section, as in the
JIIS papers read (`JOURNAL_BAR.md`).

The budgets below sum to 24.6 pages. Three things were measured in the
class on 2026-11-26: running text sets about 600 words a page (3,128
words on 5.2 pages); Section 3.4 with its three displayed equations
sets 770 words on 1.6 pages; the reference list takes about 0.10 page
an entry (the 55 verified entries 5.6 pages, and 5.5 without the arXiv
id of the 31 entries that also have a DOI). The space of the tables and
figures is still an estimate; `make` prints the page count once the
sections exist. Two choices follow (owner, 2026-11-26):

- a brief gives its section the words of the outline as the upper end
  and about 10% less as its length, which fits the pages below;
- the reference list holds about 40 entries. With all 55 the paper
  would come to about 26 pages.

Appendix B (about 0.6 page) is the first thing to move to the
supplementary file when the count runs over.

| # | Section | Pages | Content | Notes the brief is built from | Can be written |
|---|---|---:|---|---|---|
| | Title, abstract, keywords | 0.7 | title as "Name: mechanism for the task in the setting"; abstract of 150 to 250 words with one number (the gain on BIRD); 4 to 6 keywords | `JOURNAL_BAR.md` 3 | last |
| 1 | Introduction | 1.7 | small models for Text-to-SQL where data cannot be pooled; FedAvg SFT learns from one gold SQL and never uses the databases, federated DPO as published keeps its first pairs and reference; execution is available only at the client; the method in three sentences; headline results; that "federated Text-to-SQL" here means training; 4 contributions, the last the released code, splits and predictions | `RESEARCH_STATE.md` 3.1; `LITERATURE.md` 1.22 | after 7 |
| 2 | Related work | 1.8 | 2.1 small models for Text-to-SQL; 2.2 preference optimization and execution feedback for SQL and code; 2.3 federated fine-tuning of language models, federated DPO; 2.4 federated semantic parsing and Text-to-SQL; Table 1 | `LITERATURE.md` 1.2, 1.3, 1.4, 1.22, 2; `DPO_RESEARCH.md` 2, 7; `RESEARCH_STATE.md` 3.6; `bib/report.md` | after 6 |
| 3 | Method | 4.0 | 3.1 setting and notation; 3.2 overview, Fig. 1; 3.3 SFT warm-up rounds; 3.4 a preference round: sampling, execution labels, pairs, the DPO + NLL loss with the round's global model as reference, aggregation; Algorithm 1; 3.5 what it costs a client | `RESEARCH_STATE.md` 3.2, 3.3 (settings), 3.8; `DPO_RESEARCH.md` 3.1 to 3.4; the loss in `fedls_sql/training/dpo.py` | first |
| 4 | Experimental setup | 2.3 | datasets and metrics; federated setups, Table 2; models; the six baselines; implementation (prompt, LoRA, rates, rounds, sampling, decoding, seed, serving); McNemar test with Holm correction | `RESEARCH_STATE.md` 2, 3.4; `FEDERATED_DATA_SETUP.md` 3, 4 | after 3 |
| 5 | Results | 5.5 | RQ1 against the baselines (Table 3, Fig. 2); RQ2 other models and federated setups (Tables 4, 5); RQ3 perturbed questions and test-suite accuracy (Table 6); RQ4 what changes in the errors and what it costs (Fig. 3, Table 7) | `RESEARCH_STATE.md` 5.0; generated tables | after 4; a number that waits prints as `??` and its sentence is read again when the row is in |
| 6 | Ablation study | 1.8 | on-policy rounds, the NLL term, the preference term, the number of warm-up rounds, aggregation weights, pooled clients (Table 8) | `RESEARCH_STATE.md` 5.0, second table | after 5; read again when its rows are in |
| 7 | Discussion and limitations | 1.2 | why the two kinds of round remove different errors; the scope of the setting: clients hold gold SQL and databases that can be queried, full participation with 5 to 10 clients, isolation of data and not differential privacy, added client compute | `RESEARCH_STATE.md` 3.1, 5.0 | after 2 |
| 8 | Conclusion | 0.3 | | | with 7 |
| | Declarations | 0.4 | funding, competing interests, data availability, code availability, author contributions, use of AI tools | `JOURNAL_BAR.md` 1 | last, by the main session |
| | References | 4.1 | about 40 entries, chosen from the 55 of `references.bib` as the sections cite them | `bib/report.md` | grows with the text |
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
in `generated/missing.txt`. The Holm correction runs inside each table
(owner, 2026-11-26): a test is counted once, in the first table that
prints it, and the comparisons quoted only in the text form a family of
their own. A row enters a table by one line in `ARMS`, as for the
overview page. The same script writes, from the committed predictions,
the correct predictions by the form of the query (`\fact{form...}`, claim C3
of `CLAIMS.md`).

Settings are generated the same way. `tools/paper_settings.py` reads the
committed records of the runs the paper prints (the `config.json` of
the FedAvg SFT rounds and of the evaluations, the `setup.json`,
`arm.json` and `round.json` of the preference rounds) and writes
`generated/settings.tex` (one macro per setting: LoRA, rates, rounds,
samples, pairs, decoding, software versions), `generated/tab_settings.tex`
(Appendix B) and `generated/settings.md` (the same values for the Setup
brief). It stops when two runs of one line disagree on a setting. A
setting in the text is a macro, like a result number.

| Item | Content | Rows still missing (2026-11-26; `generated/missing.txt` is current) |
|---|---|---|
| Fig. 1 | method overview | none (`paper/figures/fig_method_overview.svg`) |
| Algorithm 1 | the method: k warm-up rounds, then preference rounds | none |
| Table 1 | closest work by property: federated, execution labels, on-policy pairs, NLL term, model size (FL4SP, OpenFedLLM, CodeLutra, ExCoT, ours) | none |
| Table 2 | the five federated setups: clients, split, questions and databases per client | none, read from the split files |
| Table 3 | main: BIRD dev and Spider test; no training, local SFT, centralized SFT, FedAvg SFT, FedProx SFT, federated DPO as published, the method; EX, difficulty levels, gain and p against FedAvg SFT | BIRD: local SFT, centralized SFT, FedProx, federated DPO, second seed of two rows. Spider: local SFT, FedProx, federated DPO round 2 |
| Fig. 2 | EX by round, FedAvg SFT (to round 5) and the method, both datasets | none |
| Table 4 | three models on Spider, DeepSeek-Coder-1.3B on BIRD | DeepSeek rounds on Spider; all of BIRD |
| Table 5 | FedAvg SFT and the method in the five setups | IID, alpha 0.5 with 5 clients, alpha 0.5 with 10 clients |
| Table 6 | Spider dev, Syn, Realistic, DK; EX and test-suite accuracy; FedAvg SFT, the method without warm-up rounds, the method | none (the test-suite numbers are committed) |
| Fig. 3 | incorrect predictions by round split into execution errors and incorrect results, FedAvg SFT and the method | none |
| Table 7 | what the clients train on in a round (questions; in a preference round the questions that yield pairs, and the pairs), client time per round (sampling, labels, training) and megabytes sent | none, read from the round records and the logs (`scripts/log_times.py`) |
| Table 8 | ablations at 4 rounds, BIRD and Spider | BIRD: without the preference term round 2, without NLL, k = 0 rounds 3 and 4, k = 3. Spider: without the preference term round 2, pooled clients |

The writer may propose another table or figure in its notes; the owner
decides.

## 7. Checks

Applied to the draft by the main session and the helpers; the writer
does not see this section.

### 7.1 Stops

Six checks stop a section. Each is about truth or about the build, and
none is about style.

| Check | Tool | Stops on |
|---|---|---|
| Build | `make` | the section does not compile; an undefined reference |
| Numbers | `tools/lint.py` | a result number or a setting that is not a macro |
| References | `tools/lint.py`, `/ars-citation-check` | a key that is not in `references.bib`; an entry with no DOI, no arXiv id and no stable address |
| Truth | claim audit: a helper with all the notes looks for a committed result that contradicts a sentence | a false or overstated sentence; a part called essential without its ablation row; a framing taken from the story of 2026-11-17 where the results of `RESEARCH_STATE.md` 5.0 have moved on |
| Other papers | cited-work audit: a helper lists every sentence that states something about a cited paper, and every cell of Table 1, and finds its row in the brief's facts with the locator; it then opens the paper at that locator | a statement about a cited paper without a row or a locator; a row the paper at its locator does not support. Applies to Section 2 in full and to any such sentence elsewhere |
| Length | page count | the paper over 25 pages; the abstract outside 150 to 250 words |

The claim audit reports false sentences. It does not ask for caveats,
for results the paper leaves out, or for the story of how a value was
chosen.

### 7.2 Signals

The rest is advice for the editor. None of it stops a section.

| Signal | Tool | Looks for |
|---|---|---|
| The lab showing through | `tools/lint.py` | file paths, commands, "we first", "was then chosen", sentences that certify ("all numbers come from", "no test data was used"), a choice defended that nobody questioned |
| Hedging | `tools/lint.py`, a count per section | "may", "appears to", "it is worth noting" outside the limitations |
| Lab words and earlier labels | `tools/lint.py` | student, arm, queued, run names; "wrong result", "right answer"; British spelling |
| Register | `tools/style_profile.py compare FILE --kind KIND` | measures far outside the range of the same kind of section in the ten papers, as in the first pilot |
| Text taken from the brief | `tools/style_profile.py lifted FILE BRIEF...` | a large share of the draft in runs of five or more words of the brief |
| Cold read | an isolated Opus session that has seen neither the brief nor the notes reads the PDF of the section as a reviewer of the journal would: the `cold-review` skill with its `section` template (owner, 2026-11-27), given the pages of the section and the pages before it | where it stopped, what it could not reimplement, what it did not believe. The first source of editor's notes |
| Argument | `tools/reverse_outline.py`, beside the writer's outline | the first sentences of a section do not make its argument or have left the outline without a reason; a paragraph with two points |
| Tables | `tools/table_lint.py` | rules outside booktabs, a metric without its direction, uneven decimals; fixed in the generator |
| Reader | reader test (whole-paper step): a fresh helper reads the PDF and states the problem, the method, the main result, and anything the paper seemed to defend or explain about its own making | a wrong answer to the first three; anything named in the fourth |
| Review | `/ars-reviewer` on the PDF (whole-paper step) | goes to the owner; a comment is acted on when the paper gets better |

How a signal is used (owner, 2026-11-26: rules and word checks that are
too rigid make the prose stiff and patched):

1. The main session reads it. A signal never goes to the writer as a
   figure, a count or a list of words, and no sentence is reworked to
   move a measure.
2. What is mechanical the main session fixes itself: a lab word or an
   earlier label with a fixed replacement, a macro, a label, a key.
3. A signal that is far off points at what the writer was given. Text
   taken from the brief means the brief holds sentences; a register far
   from the papers means the brief or the notes carried the lab's
   words. The input is corrected and the section is written again.
4. Whatever else matters to the reader becomes an editor's note.

### 7.3 Editor's notes

At most five notes a round, the ones that matter most, written as an
editor would write them: about the reader and the content. A fact that
is wrong, a reason the reader will ask for, a paragraph that makes two
points, a referent that is unclear, a number the reader does not need.
A note names no rule, check, measure or project file, and it does not
ask for a word to be exchanged unless the word would mislead the
reader. The writer is asked to change what the notes concern and to
leave the rest as it stands. It may disagree in its reply, and a
disagreement with a reason is settled by the owner. After two rounds
what is left is edited by the owner.

### 7.4 Notes for the owner's review

While the paper is written, the main session keeps
`manuscript/REVIEW_NOTES.md` (owner, 2026-11-26), in Vietnamese, for
the owner to review later: what needs a decision (a new statement, a
departure from something decided, a figure), passages to read again,
questions a reviewer is likely to ask and where the paper answers
them, every change to a brief after its approval, and what a later
section has to carry. An item is added when it arises, not at the end
of a section; a decided item moves to the bottom of the file and into
the file it concerns (`CLAIMS.md`, a brief, this plan).

## 8. Steps

Done by 2026-11-26: the folder, the class and the build; the generated
numbers, tables, settings and charts; `CLAIMS.md`, `TERMS.md` and
`OUTLINE.md`, approved by the owner; `references.bib` with 55 entries,
each checked against a fetched record (`bib/report.md`); the voice
folder; two pilots of Section 3.4, the second accepted by the owner as
the test of this workflow (`pilot/`); Section 3, Method, with Fig. 1
and Algorithm 1 (step W7: outline, draft, two cold reads and two
rounds of editor's notes; `briefs/03_method_notes_editor.md`), and
`REVIEW_NOTES.md` with what the owner reviews later.

Next, in this order. Each step is the loop of section 2; the owner's
time is an estimate.

| Step | What | Waits on |
|---|---|---|
| W8 | Experimental setup; Appendix A and B assembled by the main session | the time limits of the labeling step as setting macros; 30 min |
| W9 | Results, the four research questions in one call. A sentence on a number that waits states what is compared and leaves the direction and the size to the number | 30 min; the final reading waits for the rows of `generated/missing.txt` |
| W10 | Ablation study | same |
| W11 | Related work with Table 1; a helper builds the rows with their locators, and the cited-work audit runs on the draft | 30 min |
| W12 | Discussion and limitations, Conclusion | 30 min |
| W13 | Introduction; then abstract, title and keywords | 30 min |
| W14 | Whole paper: one writer reads it end to end and evens it out, and the macros and `\cite` keys of every section are listed before and after that pass and compared (`make inventory`), so the pass changes no number and no reference; the `writing_quality_check` of the academic-paper skill as a diagnostic that rewrites nothing; reader test; `/ars-reviewer`; claim audit of the full text; page count | the owner and the advisor read |
| W15 | Declarations, AI-use statement (section 10.2), public repository with code, splits and predictions, cover letter, `make submit` | authors, funding and competing interests from the owner; 1 h |

No text passes through a humanizer (owner, 2026-11-26).

Still to build in the tools: the time limits of the labeling step as
settings for Appendix B (they are constants of
`fedls_sql/eval/sql_exec.py`), the test of the method against
centralized SFT (claim A5), Table 1 with its locators, the CMC wrapper
and the supplementary file. When an evaluation is committed later: one
line in `ARMS`, `make numbers`, `make`, and the claim audit runs again
for the claims that use that row.

## 9. Tools and folder

| Tool | Use | On the Mac |
|---|---|---|
| `pdflatex`, `bibtex` (TeX Live 2026 basic), `make` | build; Springer requires that the source compiles with pdflatex | installed |
| TeX packages `sttools`, `threeparttable`, `appendix`, `ncctools`, `algorithms`, `algorithmicx`, `multirow` | needed by `sn-jnl.cls` and its template | installed in the user tree (`~/Library/texmf`) |
| `paper/notes/tools/overview_results.py` | every committed run and McNemar test, imported by `paper_numbers.py` | exists |
| `paper/figures/render.py`, `STYLE.md`; matplotlib | diagrams; result charts at 119 mm in Arial 8 pt | exists; installed |
| PaperOrchestra port (`github.com/Ar9av/PaperOrchestra`, MIT, read at `fcf8a38`) | three files copied: `section_rhetoric.md` into `voice/`, `reverse_outline.py` and `table_lint.py` into `tools/` | not installed as a skill |
| `tools/style_profile.py` | `profile`: the measures of the ten papers by kind of section, from their arXiv sources in a folder outside the repository; it also writes `voice/style_reference.json`. `compare`: the same measures for a draft beside that reference, without the sources. `lifted`: the share of a draft in runs of five or more words of other files. All three are signals for the editor (section 7.2) | exists |
| `/ars-citation-check`, `/ars-reviewer`, `/ars-disclosure` | reference metadata; cold review; AI-use statement | installed |
| academic-paper skill, `references/writing_quality_check.md` | a diagnostic in the whole-paper step: it lists what it finds and rewrites nothing | installed |
| `doc-coauthoring`, stage 3 | the reader test | installed |

Not used: `humanizer` (owner, 2026-11-26: no pass rewrites the text
after the writer); the ARS pipeline (`/ars-full`, `/ars-plan`: it
starts from a topic, and this paper starts from approved claims,
generated numbers and a plan); the PaperOrchestra pipeline (its writer
gets the whole experimental log in one call, its literature agent
searches for new citations, its refinement accepts a revision by the
score of a simulated reviewer). What is kept of the two is in section
3.5.

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
                        limitations, the map of lab words
  OUTLINE.md            sections with their content, claims and words
  WRITING_GUIDE.md      what the writer works from (section 3.2)
  TERMS.md              names of the concepts, abbreviations, notation
  voice/                passages, style_profile.md with its data and
                        style_reference.json, profile.md, section_rhetoric.md
  briefs/               one brief per top-level section, and the writer's outline
                        of that section beside it (3.4_preference_round.md is
                        the brief of the pilot)
  bib/                  report.md: how each entry of references.bib was verified,
                        and the sources of each subsection
  pilot/                the accepted draft of Section 3.4 with the writer's and
                        the editor's notes, and the page that sets it (make pilot)
  tools/                paper_numbers.py paper_settings.py charts.py lint.py
                        style_profile.py flatten.py reverse_outline.py table_lint.py
  Makefile              make, make numbers, make figures, make lint, make pilot,
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

### 10.2 The AI-use statement

Decided (owner, 2026-11-26): the statement follows what published papers
commonly write. Read for it: the template most
statements follow (Elsevier's, "During the preparation of this work
the author(s) used [tool] in order to [reason]. After using this
tool, the author(s) reviewed and edited the content as needed and
take(s) full responsibility for the content"); the template of Tech
Science Press, on the CMC author page and in its policy for all
journals ("Acknowledgement: During the preparation of this
manuscript, the author(s) used [NAME OF TOOL/SERVICE] for [PURPOSE].
The author(s) subsequently reviewed and revised the relevant content
and accept(s) full responsibility for the article."); the statement
of GradeSQL (JIIS 2026, arXiv version: "This paper used a generative
AI tool (ChatGPT) for language refinement and LaTeX formatting
assistance only. All ideas, analysis, and results are original.");
and two studies of such statements (arXiv 2611.11174: 3.7% of
engineering articles of 2025 carry one, most in the template form;
a study of medical education journals: a statement names the tool
and affirms the authors' responsibility). The form is one or two
sentences: tool and version, purpose, the authors' review, their
responsibility.
- JIIS: in the Declarations, `sections/90_declarations.tex`, under
  "Use of AI tools" (the journal asks for the Methods section or a
  suitable alternative part).
- CMC: in the Acknowledgement: "During the preparation of this
  manuscript, the authors used Claude (Anthropic; model Claude Fable
  5.2) for drafting and revising the text from the authors' results,
  analyses and outline, and for assistance in writing the code of
  the experiments. The authors subsequently reviewed and revised the
  relevant content and accept full responsibility for the article."
The purpose is stated as it is: the text is drafted with the tool,
so "language editing only", the most common purpose in such
statements, would not be true here. A search result reports a newer
Springer Nature guidance that asks for an "AI Use Declaration"
pointing to the Methods section; the page was not opened (Springer
pages), and the owner may send it.

## 11. Open with the owner

1. JIIS leaves two points open (section 10.1): which class the 25 pages
   are counted in (its page names both `sn-jnl` and the older macro
   with `smallcondensed`), and the review model. Until the owner says
   otherwise the paper is written in `sn-jnl` and is not anonymised; a
   question to the editorial office settles both.
2. Fig. 1 under Springer Nature's rule on images (section 10.1): a
   scientific diagram made with a generative AI tool is not accepted, a
   flow chart without images is outside the rule. Either the owner
   draws the figure, or the owner judges it a flow chart. CMC accepts
   an explanatory image made with an AI tool when its caption names the
   tool and version. The figure is not redrawn or restyled before the
   owner decides; its labels were brought to the names and the notation
   of `TERMS.md` on 2026-11-26 (owner: fix what is needed).
3. Which journal goes first. This plan assumes JIIS.
4. Decided (owner, 2026-11-26): Section 3.4 gives the reason for two
   pairs per question where CodeLutra constructs ten: the number of
   pairs sets the length of local training (`CLAIMS.md`, section 7).
5. Decided (2026-11-26): the two proposals of the writer of Section
   3.4. No worked example (left to the main session by the owner):
   steps 2 and 3 of Fig. 1 draw three samples, their labels and the
   two pairs, an example in the text would cost about a quarter of a
   page, and a real one needs the samples of a question from the
   server. The counts by preference round are two columns of Table 7
   and leave Section 3.4 (owner).
6. Authors, funding and competing interests are not filled in yet; the
   author block, the CRediT statement and the declarations wait for
   them.
7. Decided (owner, 2026-11-26): `CLAIMS.md`, contribution 2, now says
   that the adapter and the count that weights it leave a client.
8. Two entries of `references.bib` to check by eye (`bib/report.md`):
   the second author of SLM-SQL, where arXiv and the ACL Anthology
   differ, and Holm (1979), which has no DOI and is cited by its JSTOR
   address.
