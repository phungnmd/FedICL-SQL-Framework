# Writing guide

This guide governs the drafting of a manuscript section. The drafting
materials comprise this guide, `VOICE_GUIDE.md`, `TERMS.md`, the brief
of the section and the previously accepted sections in `sections/`. All
other files of the workspace, including any project instructions
attached to the session, are laboratory records: they constitute neither
content nor stylistic precedent for the manuscript.

## 1. The paper and its readership

The manuscript presents \method, a federated learning framework for
Text-to-SQL, and is prepared for *Computers, Materials & Continua*
(CMC). Its central argument concerns supervision. Federated supervised
fine-tuning derives its training signal exclusively from the gold SQL
query of each question, although every client additionally holds the
databases to which its questions refer. The proposed framework exploits
these databases: queries sampled from the model are executed locally,
and the agreement of their execution results with that of the gold SQL
query provides execution-derived supervision for preference
optimization. Federated learning constitutes the setting and Text-to-SQL
the task.

The readership consists of reviewers and researchers in federated
learning and natural language processing. They assess the novelty of the
contribution, the technical soundness of the method and the adequacy of
the empirical validation, and they form this assessment primarily from
the abstract, the introduction, the figures and the tables.

## 2. Authorial stance and register

The text is written from the position of the authors of a machine
learning research paper who present a completed contribution to peers.
It is not an explanation addressed to a non-specialist, and it is not an
account of how the research was conducted. `VOICE_GUIDE.md` specifies
the register and the rhetorical organization of each section; it applies
to every sentence of the manuscript.

American spelling is used throughout. Em dashes are not used.

## 3. Binding constraints

Four constraints ensure that the manuscript is accurate and that it
compiles.

1. **Facts.** Every factual statement (a configuration, a count, a
   formula, a result, a characterization of cited work) originates from
   the brief or from a file that the brief designates. Nothing is
   supplied from memory. Where required information is unavailable, the
   section is completed without it and the omission is reported in the
   notes.
2. **Claims.** Each statement of the brief specifies the claim to be
   established, the wording strength that its evidence supports and its
   scope. The claim is formulated at the specified strength: it is
   neither amplified beyond that strength nor attenuated below it. A
   scope qualifier ("on BIRD", "to our knowledge") is part of the claim
   and is retained. If the evidence appears insufficient for the
   specified strength, the concern is recorded in the notes; the
   sentence is not weakened unilaterally.
   A number whose result is not yet committed is written with its macro
   and prints as a placeholder. Where the brief provides an expected
   value, `\expect{value}` replaces the macro, the sentence is
   formulated for that outcome, and the location is listed in the notes.
3. **Numbers and names.** Results and configuration values are macros
   (`\ex`, `\gain`, `\pval`, `\fact`, `\setting`) and are never typed as
   digits; the brief specifies each macro and its output. The only typed
   value is an expected one inside `\expect`. The method is `\method`
   and the trained model is "the model". Terminology and notation
   conform to `TERMS.md`. Citations use `\cite{key}` with the keys of
   the brief, and cross-references use the labels that the brief lists.
4. **Form.** The headings specified by the brief, with no level below
   `\subsubsection` and no `\paragraph`; the commands of the document
   class and of the preamble of `main.tex`, without additional packages;
   a length close to the target of the brief and not exceeding its upper
   bound.

The brief is a specification, not a draft. Its entries are converted
into the prose of the section; they are not transcribed.

## 4. Authorial latitude

All remaining decisions belong to the author of the section: the number
and sequence of paragraphs within the organization that `VOICE_GUIDE.md`
specifies, the emphasis, the selection among the available numbers, the
inclusion of an illustrative example, and the transitions between parts.
Before submission of the draft, the section is examined from the
perspective of a reviewer and revised wherever that reader would
hesitate: an inconsistently named concept, an uninformative opening
sentence, a redundant sentence, a paragraph serving two purposes, or a
paragraph that the section does not require.

## 5. Outline before prose

An outline of the section precedes the prose: one entry per paragraph,
in sequence, stating the rhetorical function of the paragraph (as
designated in `VOICE_GUIDE.md`), the proposition it establishes, the
statement of the brief it realizes, any equation, table or figure it
contains, and its approximate length. The lengths sum to the target of
the brief. The entries are annotations, not sentences of the manuscript.

The editor responds to the outline, and the section is drafted from it.
The outline is a plan and not a commitment: a superior organization that
emerges during drafting is adopted and reported in the notes.

## 6. Deliverables

The outline, the section in LaTeX and the notes to the editor, each in
the file designated by the brief. The notes identify information that
the brief lacked, claims whose evidence appears insufficient, and
departures from the brief or from the outline together with their
rationale. A proposal for an additional example, table or figure is
submitted in the notes.
