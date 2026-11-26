# Writing guide

For the agent that drafts a section of the manuscript. You work from six
things: this guide, `TERMS.md`, `voice/style_profile.md`, the passages
in `voice/` for the kind of section you are writing, the brief of your
section, and the sections already accepted in `sections/`. The other
files of the workspace are laboratory records and are not material for
the paper.

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

## Register

The paper is written in the register of the published papers of its
field: formal, exact in its specifications, and in the vocabulary the
field uses. `voice/style_profile.md` describes that register by kind of
section, with measures taken from ten papers, and the passages show it.
Your draft is measured in the same way after you return it.

- Use the term of the field for an object, a quantity or an operation
  wherever one exists: a model generates a query, a client samples from
  the model, a query is executed on a database and may fail to execute,
  a term of the loss increases a log-likelihood, the server aggregates
  the adapters. Everyday verbs (write, run, give, get, keep, leave, let)
  are rare in the papers of the field and are rare here.
- One concept has one term, that of `TERMS.md`, from its first use to
  the last. A term is not varied for the sake of variety.
- Name the quantity an operation acts on: the loss increases the
  likelihood of the correct sample, not "the correct sample".
- "We" carries what the authors propose, choose and observe; the
  passive carries a step of a procedure. Definitions and what a table
  shows are in the present tense.
- State the purpose of a formula before it and its effect after it. A
  symbol is defined where it is first used, in the notation of
  `TERMS.md`.
- A design choice comes with the problem it addresses, and a result
  with what it means. An effect whose cause was not tested is given as
  a conjecture; a number read from a table is stated without a hedge.
- No contractions, no rhetorical questions, no em dashes, and no
  adjective that praises the method. American spelling (labeled,
  optimization, behavior).

The passages in `voice/` are examples of register and structure.
Nothing in them is content for this paper, and no sentence of theirs is
reused.

## Sources

- Every fact comes from the brief or from a file the brief names: a
  setting, a count, a formula, a result, what a cited paper did. Nothing
  is supplied from memory, and that includes the details of a cited
  paper and any reference the brief does not list.
- The brief and this guide state facts in shorthand. Their sentences
  are not text for the paper: compose every sentence of the section
  yourself, in the register above.
- When something you need is missing, do not fill it in. Write the
  section without it and name the gap in your notes.

## Claims

- Each statement in the brief has a ceiling: the strongest wording its
  evidence supports and the datasets on which it holds. A sentence may
  claim less than its ceiling and never more.
- A qualifier that bounds a finding ("on BIRD", "to our knowledge",
  "not significant after correction") is part of the claim. When a
  passage has to become more convincing, improve the sentence and leave
  the claim as it is.
- Novelty is stated against the closest work: name that work and state
  the difference. "To our knowledge" and the scope accompany any claim
  of being first.
- A number whose result is not committed yet is written with its macro
  like any other and prints as a placeholder. A sentence on such a
  number states what is compared and leaves the direction and the size
  to the number.

## LaTeX

- Results and settings are macros (`\ex`, `\gain`, `\pval`, `\fact`,
  `\setting` and the others the brief lists), never typed digits. The
  brief gives each macro with exactly what it prints, unit included.
- The method is `\method`. The trained model is "the model".
- Citations are `\cite{key}` with the keys of the brief.
- Headings: the one the brief gives. Inside a subsection the order of
  the paragraphs carries the steps; `\subsubsection` only where the
  brief allows it, and never `\paragraph`.
- Refer only to the labels the brief lists; label your equations
  `eq:...`.
- Use the commands of the class and of the preamble of `main.tex`; add
  no package.
- The length in the brief is a range, and both ends bind.

## Before you return the section

Read the draft once as the reviewer would and correct what you find:

1. a concept named by two terms, or a term of `TERMS.md` replaced by a
   synonym;
2. an everyday word where the field has a term;
3. a vague word where a specific one exists ("various", "several
   aspects", "issues", "performance" without its metric);
4. a sentence that opens with words that could be deleted ("It is worth
   noting that", "In order to", "As mentioned above");
5. a sentence that repeats the one before it, or reaches its point in a
   roundabout way;
6. a run of words taken over from the brief;
7. a paragraph with two points, or one whose first sentence does not
   state its point;
8. a claim above its ceiling, or a fact that is not in the brief.

## What you return

The section as LaTeX and your notes to the editor, each in the file the
brief names. The notes say what the brief lacked, what you doubt, and
where you departed from the brief and why. The structure of the section
is yours: the paragraphs, their order, the emphasis, and which of the
available numbers appear in the text. If an example or a small figure
would serve the reader, propose it in the notes.
