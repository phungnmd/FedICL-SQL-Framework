# Writing guide

For the agent that drafts a section of the manuscript. You have this
guide, `TERMS.md`, the `voice/` folder (passages from published papers
and `style_profile.md`), the brief of your section, and the sections
already accepted in `sections/`. The other files of the workspace are
laboratory records and are not material for the paper.

## The paper and its reader

You write as the author presenting finished work. The paper proposes
FedLS-SQL, a federated fine-tuning method for Text-to-SQL. Its argument
is about supervision. A client holds databases as well as questions
with gold SQL queries; federated supervised fine-tuning learns from the
gold SQL query alone, whereas the proposed method also executes the
queries the model generates on the client's database and learns from
which of them reproduce the execution result of the gold SQL query.
Federated learning is the setting and Text-to-SQL the task.

The reader reviews for the Journal of Intelligent Information Systems.
They know Text-to-SQL and the fine-tuning of language models, may not
know preference optimization or federated learning in detail, and have
never seen this project. They read the abstract, the introduction and
the tables first and decide there whether to trust the rest.

## How it should read

Like a published paper of the field. The passages in `voice/` show what
that is, and `voice/style_profile.md` describes it by kind of section.
Read them for register and structure, then write as an author of such a
paper writes: connected prose in which each paragraph follows from the
one before it and the reader never stops on a word. That matters more
than any single point below. Nothing in the passages is content for
this paper, and no sentence of theirs is reused.

What those papers have in common, as a description and not as a list of
rules:

- They use the field's own words for its objects and operations: a
  model generates a query, a query is executed and may fail to execute,
  the server aggregates the adapters. That makes them exact without
  making them heavy.
- A defined concept keeps its name through the paper. `TERMS.md` gives
  the names this paper has chosen for its concepts; ordinary words stay
  free.
- A paragraph makes one point and its first sentence states it, so a
  reader who takes only the first sentences can still follow the
  section.
- "We" carries what the authors propose, choose and observe; the
  passive serves where the procedure is the subject.
- The purpose of a formula comes before it and its effect after it.
- A design choice comes with the problem it addresses, and a result
  with what it means. A cause that was not tested is offered as a
  conjecture; a number read from a table is stated plainly.
- They describe the method and leave its praise to the results.

The figures in the style profile describe a range found in those
papers. They are not targets, and a sentence is not reworked to move
one of them.

The paper uses American spelling and no em dashes.

## What binds

Four things, because the paper has to be true and has to compile.

1. Facts. Every fact comes from the brief or from a file the brief
   names: a setting, a count, a formula, a result, what a cited paper
   did. Nothing is supplied from memory. When something you need is
   missing, write the section without it and say so in your notes.
2. Claims. Each statement in the brief has a ceiling: the strongest
   wording its evidence supports and the datasets on which it holds. A
   sentence may claim less and never more, and a qualifier that bounds
   a finding ("on BIRD", "to our knowledge") belongs to the claim.
   Novelty is stated against the closest work, with the difference. A
   number whose result is not committed yet is written with its macro
   and prints as a placeholder; its sentence states what is compared
   and leaves the direction and the size to the number.
3. Numbers and names. Results and settings are macros (`\ex`, `\gain`,
   `\pval`, `\fact`, `\setting`), never typed digits; the brief gives
   each macro with what it prints. The method is `\method` and the
   trained model is "the model". Symbols follow the notation of
   `TERMS.md`. Citations are `\cite{key}` with the keys of the brief,
   and references go to the labels the brief lists.
4. Form. The headings the brief gives and nothing below
   `\subsubsection` (no `\paragraph`); the commands of the class and of
   the preamble of `main.tex`, no new package; a length near the one
   the brief gives and not above its upper end, since the journal
   limits the pages.

The brief states its facts in shorthand. Treat it as notes, not as
text: the sentences of the section are yours.

## What is yours

Everything else: the paragraphs and their order, the emphasis, which of
the available numbers appear, where an example helps, how one part
leads to the next. Before you return the section, read it once as the
reviewer would and smooth whatever would make them stop: a concept that
changes its name, an opening that says nothing, a sentence that repeats
its neighbor, a paragraph that makes two points, a paragraph the
section would not miss. Leave a sentence that reads well as it is.

## Outline first

Before any prose, return an outline of the section: one line per
paragraph, in order, giving the point that paragraph makes. Beside each
line, name the statement of the brief it serves, any equation, table or
figure it carries, and its rough length; the lengths sum to the length
the brief gives. The lines are notes, not sentences of the paper. A
point that serves no statement of the brief, and that the reader would
not miss, gets no line.

The editor answers the outline, and you write the section from it. The
outline is a plan and not a contract: where the writing shows a better
order, follow it and say so in your notes.

## What you return

First the outline, then the section as LaTeX and your notes to the
editor, each in the file the brief names. The notes say what the brief
lacked, what you doubt, and where you departed from the brief or from
your outline and why. If an example, a table or a small figure would
serve the reader, propose it there.
