# FedExec-SQL: writing plan

How the manuscript is written: who does what, what the writer is given,
the checks, the steps, the tools. It holds the workflow only. What the
paper claims is in `manuscript/CLAIMS.md`, what each section contains in
`manuscript/OUTLINE.md`, what was tried and measured on the way here in
`LAB_LOG.md` (2026-11-26, 2026-11-27), and what waits for the owner in
`manuscript/REVIEW_NOTES.md`.

## 1. Choices

| Part | Choice |
|---|---|
| Journal | CMC alone (owner, 2026-11-27). LaTeX on the Tech Science Press class in `Definitions/`; requirements in section 10 |
| Who writes | a writer in an isolated session (the `cold-session` skill; Fable 5.2, high effort), one top-level section at a time: its outline first, then the prose. It is never a subagent, which inherits `AGENTS.md` and the memory (owner, 2026-11-27). The main session coordinates and writes no sentence of the paper |
| What the writer knows | the work in full as science, nothing of the lab, and it decides the structure of its section (owner, 2026-11-27; section 3) |
| Who knows the project | the main session: it is the person of the project, and the writer is its tool for writing. The writer asks it whatever the pack does not settle, at any point, and it answers (owner, 2026-11-27; section 3.5) |
| Voice | academic (owner, 2026-11-27): dense, in the terms of the field, assertive at the strength of the evidence, the novelty said plainly, the method told by component, the results by finding and mechanism. Specified in `manuscript/VOICE_GUIDE.md`, carried by the register of the brief and shown by the example papers of the pack |
| Constraints | few. Four things bind the writer (section 3.3). Truth is checked on the draft, not fenced in beforehand; checks of words and style are signals for the editor, never rules for the writer; prose is not repaired word by word |
| Position | the paper is about supervision: where the training signal comes from. Federated learning is the setting, Text-to-SQL the task. Novelty is stated against FedAvg SFT and federated DPO as published. CodeLutra has fixed places (Section 2.2 with Table 1, a citation at the objective, one sentence in Section 4.5) and is the frame of no brief (`RESEARCH_STATE.md`, section 3.6) |
| Numbers | results and settings are macros written from the committed evaluations and configs (section 6). A number that waits prints `??` (`--` in a table); a guess is `\expect{value}` and prints `value??`. The main session sets a guess, gives it in the brief and lists it in part 3 of the checks file; `make submit` stops on either |
| Names | the method is `\method`, the trained model is "the model". Name (FedExec-SQL) and title set by the owner on 2026-11-27; the title is in `main.tex` |
| Draft first | the draft is complete first and trimmed later (owner, 2026-11-27): when a brief does not fit its length, the length is raised |
| Commits | one commit per section when its rounds of editor's notes are done, without waiting for the owner's reading |
| `CLAIMS.md` | not fixed: a line that is false against the numbers is corrected and the change recorded in `REVIEW_NOTES.md` |
| Helpers | audits, look-ups and cold reads run on Opus. No text passes through a humanizer |

## 2. Who does what

| Role | Does | Does not |
|---|---|---|
| Owner | approves each brief and the example papers; reads the sections and `REVIEW_NOTES.md` when the owner chooses; decides | |
| Main session | knows the project and stands for it; builds the numbers, the briefs and the pack; starts the writer and answers its questions; runs the checks; turns findings into a few editor's notes; fixes what is mechanical (a macro, a label, a citation key) | draft or rewrite sentences of the paper: it carries the vocabulary and the history of the lab |
| Writer | writes one section from its pack; asks the main session what the pack does not settle; decides its structure; answers the editor's notes | see anything outside its pack and the answers it is sent |
| Helpers | audit claims and statements about cited papers, read the PDF cold | talk to the writer |

One section moves through this loop; the next starts when it is
accepted, because a later section reads the earlier ones.

```text
brief (main session; the owner approves it)
  -> register of the brief measured; a brief in the words of the lab is rewritten
  -> pack assembled, and read once as the writer will read it (section 3.2)
  -> outline, one line per paragraph (a fresh writer session)
  -> the main session answers the outline (section 4.1)
  -> draft of the whole section (the same session)
     at any of these turns the writer may stop on questions; the main
     session answers and the turn is taken up again (section 3.5)
  -> make, lint, register, overlap, claim audit, cold read
  -> at most five editor's notes -> the same session revises (two rounds at most)
  -> session closed; commit
```

One session outlines, drafts and revises a section. Two writers never
run at once.

### 2.1 Starting the writer

The writer is a session of the `cold-session` skill. It loads no
`CLAUDE.md`, `AGENTS.md`, memory or user settings, has no shell, and
reads and writes only inside a temporary directory that holds a copy of
its pack. Web search is on for Sections 1, 2 and 6, which speak about
other work, and off (`-N`) for Sections 3 to 5 and 7, where everything is in
the pack (owner, 2026-11-27). A subagent is not used: it inherits the
project instructions and the memory index, and telling it to disregard
them does not take them out of what it has read.

```bash
r=.claude/skills/cold-session/run.sh
b=paper/manuscript/build
$r -m claude-fable-5-2 -e high -w -N -k -d $b/pack_NN -f $b/start_NN.md -o $b/writer_NN   # no -N for Sections 1, 2, 6
$r -r HANDLE -f $b/answer_NN.md            # the answer to the outline
$r -r HANDLE -f $b/reply_NN_1.md [FILE...] # answers to the writer's questions, with files if needed
$r -r HANDLE -f $b/notes_NN_1.md           # editor's notes, round 1; -c on the last turn
```

The files the session writes arrive in `build/writer_NN/` at the paths
it used; its replies are in the `.log` there. The main session copies
the section into `sections/` and the outline and the writer's notes
into `briefs/`.

The start prompt, and nothing else:

```text
You are the author of Section N (TITLE) of a machine learning research
manuscript prepared for Computers, Materials & Continua. Your working
directory holds the material of the paper; README.md lists it. Read
README.md, paper.md, guide.md and brief.md first, and open the rest as
you need it.

The editor is one of the researchers of the study. Whenever the material
does not settle something you need, write your questions to
notes/questions.md and stop; the editor answers them.

First deliverable: the outline that guide.md describes, written to
notes/outline.md. Stop there and wait for the editor's response.
```

For Sections 1, 2 and 6 the start prompt has one more paragraph, before
the last one:

```text
You may search the web to check a detail of a cited paper or to find
related work. List in notes/notes.md every fact and every reference you
take from the web, each with its URL and the place in the source.
```

It is continued with three kinds of message: answers to the writer's
questions, whenever it stops on them (section 3.5); the answer to the outline,
ending in "Draft the section into sections/NN_NAME.tex and write your
notes to notes/notes.md"; and, per round, "Editor's notes, round K of at
most two", the notes, and "Revise what the notes concern and leave the
remainder of the section unchanged."

### 2.2 Starting the main session

A new main session reads, before anything else and in this order:

1. `RESEARCH_STATE.md`: sections 2 (setup), 3.1 (story), 3.6 (closest
   work) and 5.0 (committed results); the first screen of
   `PIPELINE_NEXT.md` for what waits.
2. `manuscript/CLAIMS.md`, `OUTLINE.md`, `TERMS.md`.
3. This plan; `manuscript/WRITING_GUIDE.md` and `VOICE_GUIDE.md`.
4. `manuscript/REVIEW_NOTES.md`, part A, and the checks file of the
   section in hand.
5. For Sections 3 and 4, the loss and the round in the code
   (`fedicl-sql/fedls_sql/training/dpo.py`,
   `fedicl-sql/fedls_sql/federated/pref_rounds.py`).

It then tells the owner in about ten lines the components of the
framework, the baselines, the main results on BIRD dev and Spider test,
the claims that have numbers and those that wait, and the step of
section 8 it will take, and waits for the owner's yes.

No section is written yet: `sections/01` to `08` hold a heading and its
label. A brief is built from the files of section 4, and no earlier
text is its starting point.

## 3. The writer

### 3.1 The principle

What a writing agent produces follows from what it has read. Given the
notes of the lab it takes their voice and tells their history; given a
list of limits it writes below every limit; given a list of claims it
presents the list. A good section comes from an author who knows the
work in full and builds the argument freely. So (owner, 2026-11-27):

- The writer knows the science in full: the method, every result with
  its test, the papers its section cites. Rows that are weak or that
  wait stand in the tables as they are, and the writer words a finding
  at what the table carries.
- The writer knows nothing of the lab: no note, rule, date, decision,
  dropped direction, claim number or lab word. This holds by how the
  writer is run (an isolated session, a pack read before use), not by an
  instruction to ignore something.
- The writer is free. The brief gives the aim of the section and the
  points of its argument; structure, emphasis, the choice of numbers
  and examples are the writer's.
- The writer can ask. The main session is the person of the project;
  what the pack does not settle, the writer asks it at any point and
  gets an answer, instead of guessing or leaving it out (section 3.5).
- What the lab needs enforced is checked on the draft (section 7) and
  reaches the writer only as an editor's note about the reader.
- One section, one writer, one brief, so that it reads as one piece.
- A draft far from a good paper is not repaired sentence by sentence:
  the cause is in what the writer was given. The pack is corrected and
  the section written again.

### 3.2 The pack

One directory per section, assembled in `build/pack_NN/` (outside Git)
by `make pack S=NN` (`tools/pack.py`), which also writes the start
prompt, `build/start_NN.md`. Every file in it is in the register of the
paper.

| In the pack | Holds | Built from |
|---|---|---|
| `README.md` | one line per file of the pack | written with the pack |
| `paper.md` | the paper on one page: setting, limitation, key observation, framework, findings, contributions, organization. The same for every section | `WRITING_GUIDE.md`, "The paper" |
| `guide.md` | how to work: the readers, the materials, what binds (section 3.3), the outline, the deliverables | `WRITING_GUIDE.md`, "Working guide" |
| `voice.md` | the register, and the organization of every kind of section | `VOICE_GUIDE.md` |
| `terms.md` | the glossary: term, meaning, symbol | `TERMS.md` |
| `brief.md` | this section (section 4) | `briefs/NN_name.md` |
| `results/` | every table as it prints, with its tests; the figures; the settings; each macro with what it prints and the names of its arguments. All of them, not only those of the section; result commits and source files are left out | `generated/`, `figures/`, `make floats` |
| `related/` | for each citation key that stands in the brief: the abstract and the fact rows, without the quotations and the reading record | `briefs/02_related_rows.md`, `02_related_table1_rows.md`; `.sources/abstracts.json`, written by `tools/abstracts.py` (outside Git) |
| `examples/` | one or two published papers far from ours in content, as examples of how a paper of this kind is built and reads | `.sources/examples/` (outside Git) |
| `sections/` | the accepted sections, and the file of this section with its heading | `sections/` |

The method reaches the writer of Section 3 through its brief (the
algorithm, the equations, Fig. 2) and every later writer through the
accepted Section 3.

Not in the pack: the notes of the lab, `CLAIMS.md`, `OUTLINE.md`, this
plan, the checks files, `voice/`; anything that carries a date, a
decision of the owner, a claim number, a lab word or an instruction
about what not to say; the full text of CodeLutra and of OpenFedLLM
(where a brief lists them, their fact rows and abstracts are in
`related/`). With web search on, a writer can reach those two papers;
`make overlap` and the claim audit read the draft for what that
leaves.

Example papers: one from CMC and one widely read method paper, never
CodeLutra, OpenFedLLM, GradeSQL or a DPO paper. In place now: LESFT
(CMC 87(1)) and LoRA (arXiv 2106.09685), the main session's choice;
the owner may change it. `README.md` names them as examples of form; no fact is
taken from them, and `make overlap` reads the draft against them too.

`tools/pack.py` searches the pack for dates, "owner", pointers to
files of the lab and the lab words of `tools/lint.py`, and stops when
it finds one. Before the start the main session also reads the pack
once from the first file to the last, as the writer will. What is
found is removed at the source file, not in the copy.

### 3.3 What binds the writer

1. Facts: every fact about our work comes from the pack or from an
   answer of the main session; a gap is asked about and not filled by a
   guess. A fact about a cited paper comes
   from the pack or, in Sections 1, 2 and 6, from the web, and then
   stands in the notes with its URL.
2. Findings: a finding is stated as its table carries it, and its scope
   ("on BIRD", "to our knowledge") is part of it. A writer that finds
   the evidence thin for a point of the brief says so in its notes.
3. Numbers and names: macros; the names and notation of `terms.md`; the
   citation keys and labels of the brief.
4. Form: the headings of the brief, the commands of the class, a length
   near the one the brief gives.

Everything else is the writer's: paragraphs and their order, emphasis,
which numbers appear, an example, the transitions. Its notes are read:
a point it finds weak goes to the owner.

A caution of the lab is never a rule in the pack. The pack states the
fact (a sample is labeled correct when its execution result equals that
of the gold SQL query on the client's database), and the claim audit
reads the draft for a sentence that goes against it.

### 3.4 Voice

`voice.md` describes the register, and the example papers show it from
the first session on. If a pilot is still far from the range of the
papers (`make register`), the cause is looked for in the pack. `voice/`
holds the editor's calibration only (`voice/README.md`).

### 3.5 Questions and answers

The main session is to the writer what a researcher of the project is
to a colleague who writes the paper with them: it knows the method, the
runs, the results and the literature, and it answers. The writer stops
a turn on `notes/questions.md` whenever the pack does not settle
something its section needs; this can be before the outline, in the
middle of the draft or during a revision, and the number of exchanges
is not limited. Rounds of questions do not count as rounds of editor's
notes.

How the main session answers:

- From the record, not from memory: the committed results, the code,
  the notes, the cited paper itself. A number that is not a macro yet is
  first generated (`make numbers`) and sent as its macro; a new table or
  figure is sent as a file with the reply.
- With the science and nothing of the lab, as in the pack: what the
  method does and what was measured, not when something was decided,
  what was tried before or which rule applies. A question on why a
  choice was made is answered with the property the choice confers, or
  with "not established" when no experiment isolates it.
- At the strength of `CLAIMS.md`. When the answer would go beyond it,
  or the record does not hold it, the main session says that the result
  does not exist; it does not estimate. A question only the owner can
  settle goes to `REVIEW_NOTES.md`, part A, and the writer is told to
  write on without it.
- In the register of the paper and the terms of `TERMS.md`. Every reply
  and every file sent with it passes `tools/pack.py --check` first.
- Without sentences for the paper: an answer gives facts and relations
  as short entries; the wording is the writer's.

What a question shows: an answer that a later writer will also need is
added to the source of the pack (the page on the paper, the brief, the
fact rows), so that it is asked once. Many questions on one section
mean its brief was thin. The questions and the replies of a session are
in its `.log`.

## 4. Briefs (`briefs/NN_name.md`, one per top-level section)

The brief is where the language of the lab becomes that of the paper,
once, and where the owner decides content before any prose exists. It
is written in the terms of `TERMS.md` and in the register of the paper,
and holds no sentence that could stand in the paper. `tools/style_profile.py
compare` is run on it before the writer starts; a brief far below the
papers in long words, or far above them in everyday verbs, is rewritten.

- Place in the paper: headings and labels, what stands before and
  after, the length (the words of `OUTLINE.md` as the upper end, about
  10% less as the length asked for).
- Aim: what the reader holds at the end of the section, in two or three
  lines.
- Points: four to eight for the section, in the order of the argument,
  one line each: what it says, worded at the strength its evidence
  carries ("outperforms FedAvg SFT by ... points on both datasets,
  significant"; "to our knowledge the first ..."), and where the
  evidence is (a table, a figure, the macros, a reference). They are
  the points of an argument, not paragraphs to produce: the writer
  merges, splits and orders them.
- Materials: the tables and figures of the section by file; facts as
  values where no table holds them (counts, formulas checked against
  the code).
- References: the keys the section cites. Their fact rows and abstracts
  go into `related/`; every cell of Table 1 is a fact row with its
  locator in the cited paper (`briefs/02_related_rows.md`).
- The labels the section may refer to, and the kind of section, which
  names its part of `VOICE_GUIDE.md`.

A brief holds what the paper prints, not dates, run names, what was
tried, or how a value was chosen. It states what the method does and
does not grade it: no entry lists what the paper does not claim, and no
entry calls a part minor. Every caution (a wording that would be false,
a comparison the rows do not carry, a result that waits) goes into
`briefs/NN_checks.md`, which is not in the pack. Limitations are in the
brief of the Discussion, once.

Novelty in a brief is located against the federated baselines: what
federated SFT leaves unused, what federated DPO as published keeps
fixed. No point defines the method or a component as a difference from
CodeLutra. Only the briefs of Sections 2 and 4 list it among their
references, and the brief of Section 3 its citation key; since
`related/` follows the references of the brief, no other writer reads
about it.

A new brief is built from this form, from `CLAIMS.md`, `OUTLINE.md`,
the checks file of the section (its part 5 has the labels, floats,
formulas and Algorithm 1 as checked against the code),
`generated/numbers.md` and `settings.md`, `bib/report.md`, and
`briefs/inventory.txt` (macros and citation keys by section).

### 4.1 The outline of a section

Written by the writer before any prose, into `notes/outline.md`: one
line per paragraph with its function (as `voice.md` names it), its
point, the equation, table or figure it carries, and its rough length.
The main session answers in a few lines, on these questions only:

- read alone and in order, do the lines make an argument that reaches
  the aim of the brief;
- does the section have the functions the guide gives for its kind (an
  introduction without a named limitation, or a method told as stages
  of a run, goes back);
- in an introduction, does the line that states what the paper does
  answer the limitation the lines before it establish;
- is anything said twice, and do the lengths sum to the length of the
  brief.

The outline is not checked line against point. Whether a point of the
brief is missing, or stands at another strength, is read on the draft
and comes back as an editor's note. The outline is a plan and not a
contract; the owner is asked before the draft only when it departs from
the aim of the brief or from `OUTLINE.md`.

## 5. Structure and order

Content, claims and words of each section are in `OUTLINE.md`. CMC has
no page limit and its fee covers 15 pages; running text sets about 600
words a page in the class, and the reference list takes about 0.10 page
an entry (about 40 of the 55 entries of `references.bib` are cited).
The draft is trimmed toward the pages of the fee after it is complete.

| # | Section | Notes the brief is built from |
|---|---|---|
| 1 | Introduction, Fig. 1, abstract, keywords | `RESEARCH_STATE.md` 3.1; `LITERATURE.md` 1.22 |
| 2 | Related work, Table 1 | `briefs/02_related_rows.md`, `02_related_table1_rows.md`; `LITERATURE.md` 1.2 to 1.4, 1.22, 2; `DPO_RESEARCH.md` 2, 7; `RESEARCH_STATE.md` 3.6 |
| 3 | Method, Fig. 2, Algorithm 1 | `RESEARCH_STATE.md` 3.2, 3.3; the loss in `fedls_sql/training/dpo.py`; `03_checks.md` part 5 |
| 4 | Experimental setup, Table 2 | `RESEARCH_STATE.md` 2, 3.4; `FEDERATED_DATA_SETUP.md` 3, 4; `generated/settings.md` |
| 5 | Results and analysis (the ablation study is 5.3), Tables 3 to 8, Figs. 3 and 4 | `RESEARCH_STATE.md` 5.0, both tables; the generated tables |
| 6, 7 | Discussion and limitations; Conclusion | `CLAIMS.md` 5; `RESEARCH_STATE.md` 3.1, 5.0 |
| A, B | Appendix: the prompt; all settings | generated; written by the main session, no prose |

Order of writing: 3 and 1 first, as the pilot; then 4, 5, 6 with 7,
2; last, the Introduction is brought up to date, with the abstract, the
keywords and the title candidates.
The body goes in the order of the paper because a writer takes the
terms of the accepted sections: 4 defines the statistical protocol that
5 and 6 rely on, 5 gives 6 its findings, and the Introduction
promises what 5 and 6 then say.

## 6. Tables and figures

`tools/paper_numbers.py` writes one macro per cell and one `tab_*.tex`
per table from the committed evaluations (through
`paper/notes/tools/overview_results.py`; a row enters by one line in
`ARMS`), prints `--` for a row that is not committed and lists those
rows in `generated/missing.txt`. The Holm correction runs inside each
table; a test is counted once, in the first table that prints it, and
the comparisons quoted only in the text form a family of their own.
`tools/paper_settings.py` writes the settings from the committed
configs (`generated/settings.tex`, `tab_settings.tex`, `settings.md`)
and stops when two runs of one line disagree.

| Item | Content |
|---|---|
| Fig. 1 | one question trained in the two ways (to be drawn) |
| Fig. 2 | framework overview (`paper/figures/fig_method_overview.svg`) |
| Algorithm 1 | the method |
| Table 1 | closest work by property |
| Table 2 | the federated setups |
| Table 3, Fig. 3 | main results on BIRD dev and Spider test; EX by round |
| Fig. 4 | incorrect predictions by kind and round |
| Table 4 | ablations; BIRD dev also under test-suite accuracy |
| Tables 5, 6 | other models; other federated setups |
| Table 7 | Spider dev, Syn, Realistic, DK; EX and test-suite accuracy |
| Table 8 | what a round costs a client |

Supplementary file: every McNemar test with its adjusted p, pairs per
client and round, the per-client statistics of the splits, EX by round
of every line; Appendix B moves there first if the pages run over.

The writer may propose another table or figure in its notes; the owner
decides.

## 7. Checks

Applied to the draft by the main session and the helpers; the writer
does not see this section.

### 7.0 Kinds of finding

Each finding is put into its kind when it arises (owner, 2026-11-27).
One remark of a cold read often holds two: "this sentence overstates
what OpenFedLLM says" is a check (what that paper states) and a wording
note (the sentence).

| Kind | What it is | Where it is kept | How long |
|---|---|---|---|
| Check | what stays true whatever a draft says: a number, a setting, what the code does, what a cited paper states, the strength and scope of a claim, a result that waits | `briefs/NN_checks.md`, in fixed parts: facts about our work; facts about cited papers; claims; what the section carries for other sections | until submission |
| Wording | how one draft reads | `briefs/NN_notes_editor.md` | it dies with its draft |
| Decision | what only the owner can choose | `manuscript/REVIEW_NOTES.md`, part A | until decided |
| Reviewer question | what a referee will ask, and where the paper answers | `manuscript/REVIEW_NOTES.md`, part C | until submission |
| Done | what was changed | `LAB_LOG.md` and the commits | history |

A check is stated as the fact with its source, not as an instruction
about a sentence. Only wording notes reach the writer.

### 7.1 Stops

Each is about truth or the build; none is about style.

| Check | Tool | Stops on |
|---|---|---|
| Build | `make` | the section does not compile; an undefined reference |
| Numbers | `make lint` | a result number or a setting that is not a macro |
| References | `make lint`, `/ars-citation-check` | a key not in `references.bib`; an entry with no DOI, arXiv id or stable address |
| Truth | claim audit: a helper with the notes looks for a committed result that contradicts a sentence and reads each claim beside its line of `CLAIMS.md` | a false sentence; a claim above its line (a cause where the line has a difference, both sets where it has one, "first" without its bound) or with its scope dropped; a part called essential without its ablation row |
| Other papers | cited-work audit: every sentence about a cited paper and every cell of Table 1 is found in the fact rows and opened at its locator. A fact or a reference the writer took from the web is opened at its URL by a helper first, and gets its fact row and its entry in `references.bib` | a statement without a row, or a row the paper does not support |
| Overlap | `make overlap` (the arXiv sources of CodeLutra and OpenFedLLM in `.sources/`, and the example papers of the pack) | a run of five or more words shared with one of them, other than a stock phrase of the field or a name |
| Length | `make` | the abstract outside 200 to 400 words; the page count above 15 is printed, not a stop |

The claim audit reports false sentences. It does not ask for caveats,
for results the paper leaves out, or for how a value was chosen.

### 7.2 Signals

Advice for the editor; none stops a section.

| Signal | Tool | Looks for |
|---|---|---|
| Register | `make register`; `tools/style_profile.py compare FILE --kind KIND`, on a brief and on its draft | measures far outside the same kind of section in the reference papers: few long words and many everyday verbs are the words of the lab |
| Strength and coverage | the cold read; `tools/reverse_outline.py`; the draft beside the points of its brief | a reader who cannot say what is new and against what; a point of the brief that is missing or below its strength; a finding told as a list of values; a weakness outside the limitations or said twice |
| The lab showing through | `make lint` | file paths, "we first", sentences that certify, a choice defended that nobody questioned, lab words |
| Text taken from the brief | `tools/style_profile.py lifted FILE BRIEF` | a large share of the draft in runs of five or more words of the brief |
| Cold read | the `cold-session` skill, `section` template: an isolated session reads the PDF of the section as a reviewer would | where it stopped, what it could not reimplement, what it did not believe. The first source of editor's notes |
| Inflated words | `writing_quality_check` of the academic-paper skill, read by the main session | "comprehensive", "robust", "leverages" where the evidence does not carry them |
| Tables | `tools/table_lint.py` | fixed in the generator |

How a signal is used:

1. The main session reads it. It never goes to the writer as a figure,
   a count or a list of words, and no sentence is reworked to move a
   measure.
2. What is mechanical the main session fixes itself.
3. A signal that is far off points at the input: text taken from the
   brief means the brief holds sentences; a register far from the
   papers means the brief or a guide carried the words of the lab; a
   section that claims little means its brief gave limits and no
   strength; a section that presents its points one after another means
   the brief read as a checklist. The input is corrected and the section
   written again.
4. Whatever else matters to the reader becomes an editor's note.

### 7.3 Editor's notes

At most five a round, the ones that matter most, written as an editor
would write them, about the reader and the content: a fact that is
wrong, a reason the reader will ask for, a paragraph with two points,
an unclear referent, a number the reader does not need, a contribution
or a finding stated more weakly than its evidence allows. A note names
no rule, check, measure or project file, and asks for no exchange of a
word unless the word would mislead. The writer may disagree with a
reason; the owner settles it. After two rounds what is left is the
owner's to edit.

### 7.4 Notes for the owner

`manuscript/REVIEW_NOTES.md`, in Vietnamese, holds two kinds only: what
needs a decision (part A) and the questions a reviewer is likely to ask
(part C). An item is added when it arises; a decided item moves to the
bottom of the file and into the file it concerns. Remarks on wording do
not go into it.

## 8. Steps

State (2026-11-27): the build, the generated numbers, tables, settings
and charts, `CLAIMS.md`, `TERMS.md`, `OUTLINE.md`, `references.bib` (55
entries, each verified; `bib/report.md`), the two guides, the checks
files, the isolated runner and the tool that assembles a pack exist.
`WRITING_GUIDE.md` and `TERMS.md` are in the form of the pack; the
abstracts of 54 of the 56 references and two example papers are in
`.sources/`. The brief of Section 3 is written and its pack is built
(`build/pack_03/`, outside Git; `make pack S=03` builds it again); the
owner starts its writer (2026-11-27). No section is written yet:
`sections/01` to `07` hold a heading and its label; the appendices and
the statements exist.

| Step | What | Waits on |
|---|---|---|
| V1 | Done 2026-11-27: `WRITING_GUIDE.md` as two parts (the paper on one page; how to work); `TERMS.md` as a glossary, its lab words in `CLAIMS.md`, section 6; the abstracts; the example papers; `tools/pack.py` | the owner reads the page on the paper (`WRITING_GUIDE.md`, "The paper") and may change the example papers |
| V2 | Pilot: the briefs of Sections 3 and 1 in the form of section 4; the writer drafts Section 3, then Section 1 with the abstract; all checks of section 7 | the owner approves each brief, then reads the pilot |
| V3 | The pilot holds: the other sections in the order of section 5. It does not hold: the pack is corrected (section 3.1) and the pilot is written again | the owner; a brief to approve per section |
| W14 | Whole paper: one writer reads it end to end and evens it out, with `make inventory` before and after so that no number and no reference changes; reader test; `/ars-reviewer`; claim audit of the full text; page count | the owner and the advisor read |
| W15 | Statements, AI-use statement (section 10), public repository with code, splits and predictions, cover letter, `make submit` | authors, funding and competing interests from the owner |

When an evaluation is committed later: one line in `ARMS`, `make
numbers`, `make`, and the claim audit runs again for the claims that
use that row; its `\expect` guesses are replaced and their sentences
read again.

Still to build in the tools: the time limits of the labeling step as
settings for Appendix B (constants of `fedls_sql/eval/sql_exec.py`),
the test of the method against centralized SFT (claim A5), Table 1 with
its locators, the supplementary file.

## 9. Tools and folder

| Tool | Use |
|---|---|
| `make`, `make numbers`, `make figures`, `make floats` | the PDF (`build/main.pdf`); macros, tables and settings; charts; every float on its own |
| `make lint`, `make inventory` | `tools/lint.py`: numbers, references, journal form, lab words; macros and keys of every section |
| `make register`, `make overlap` | `tools/style_profile.py compare` for every section; `lifted` against the closest papers and the example papers |
| `make pack S=NN [ALSO=..] [ACCEPTED=".."]`, `tools/abstracts.py` | what the writer of a section reads, with its start prompt; the abstracts of the references |
| `tools/pack.py --check FILE...` | a reply to the writer, editor's notes or a file sent with them, searched for dates, "owner" and lab words before it is sent |
| `make submit` | the flat source the journal asks for, compiled (`tools/flatten.py`); stops on a placeholder or a guess |
| `tools/reverse_outline.py`, `tools/table_lint.py` | first sentences of a section; table conventions (from PaperOrchestra, MIT) |
| `cold-session` skill | isolated sessions: the writer (section 2.1) and the cold reads |
| `/ars-citation-check`, `/ars-reviewer`, `/ars-disclosure` | single checks. The paper is not run through the ARS pipeline |
| TeX | TeX Live 2026 basic with the packages of `tsp.cls` in the user tree; the `Makefile` puts the `l3` folders of the system tree first on `TEXINPUTS` |

```text
paper/manuscript/
  main.tex  macros.tex  floats.tex  references.bib  Makefile
  Definitions/     the class of Tech Science Press
  sections/        01_intro ... 07_conclusion, 90_statements_cmc, A_prompt, B_settings
  generated/       numbers, settings, tab_*.tex, missing.txt, the prompts
  figures/         fig_*.pdf
  CLAIMS.md  OUTLINE.md  TERMS.md  WRITING_GUIDE.md  VOICE_GUIDE.md  REVIEW_NOTES.md
  briefs/          NN_name.md (brief), NN_name_outline.md, NN_checks.md,
                   NN_notes_editor.md, the fact rows of Section 2, inventory.txt
  bib/report.md    how each reference was verified; the sources of each subsection
  voice/           the editor's calibration
  cold_reviews/    reports of the cold reads
  build/           outside Git: the PDF; pack_NN/ (what the writer of a section reads),
                   writer_NN/ (what it wrote, and the log of its session)
  .sources/        outside Git: arXiv sources for make overlap, abstracts.json,
                   examples/ (the example papers)
  tools/
```

`main_jiis.tex`, `sn-jnl.cls`, `sn-basic.bst`, `sections/90_declarations.tex`
and the `jiis` branches of the tools are the JIIS fallback, not kept up.
The JIIS submission guidelines as read on 2026-11-26 are in the Git
history of this file (its section 10.1 before 2026-11-27).

## 10. CMC requirements

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
