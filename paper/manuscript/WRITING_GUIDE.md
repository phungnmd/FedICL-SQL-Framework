# The paper

One page on the manuscript as a whole, identical for every section. It
orients the author of a section; the brief specifies the section itself.
The entries below are notes and not sentences of the manuscript.

**Title.** \method: A Federated Learning Framework for Text-to-SQL with
Preference Optimization from Client-Side Execution. Prepared for
*Computers, Materials & Continua* (CMC).

**Subject.** Supervision in federated Text-to-SQL, that is, the origin
of the training signal. Federated learning constitutes the setting and
Text-to-SQL the task.

## Setting

- Several organizations each possess databases and questions with gold
  SQL queries; neither is shared outside the organization.
- They jointly train one small language model (0.5B to 1.5B parameters;
  principal model Qwen2.5-Coder-1.5B-Instruct with a LoRA adapter), and
  only that model is deployed.
- Privacy denotes data isolation: all data remain at the client. No
  differential privacy is involved.

## Limitation of existing federated training

- FedAvg SFT derives its training signal exclusively from the single
  gold SQL query of each question. The model receives no signal about
  which of its own queries are incorrect, and the client databases
  remain unused.
- FedDPO, the federated preference optimization of OpenFedLLM,
  constructs its preference pairs once, retains one reference model for
  all rounds and has no NLL term; it addresses human preference data.

## Key observation

- A SQL query is verifiable by execution, and execution is possible
  only where the database resides, at the client.
- Execution converts the single gold SQL query of a question into many
  correct and incorrect queries of the model's own: a sample is correct
  when its execution result equals that of the gold SQL query on the
  client's database. This is execution-derived supervision.

## Framework

| Component | Function |
|---|---|
| Supervised warm-up | $T_w$ warm-up rounds of FedAvg SFT |
| Client-side execution labeling | each client samples $N$ queries per question from the current global model, executes them on its own databases and assigns each an execution label |
| On-policy pair construction | $M$ preference pairs per question, constructed anew in every preference round from that round's labeled samples |
| Preference objective | the preference term (the DPO loss), whose reference model is the global model at the start of the round, plus the weighted NLL term |

- Aggregation: federated averaging of the adapters, weighted by the
  number of preference pairs. A client transmits only the adapter and
  that count, as it transmits the adapter and the number of questions
  in FedAvg SFT.
- A federated round constitutes one resampling step: the errors of each
  new global model are identified again without additional
  communication.
- Default configuration: $T = 4$ rounds with $T_w = 2$, $N = 10$,
  $M = 2$.

## Evidence

Protocol: execution accuracy (EX) on BIRD dev, the principal dataset,
and on Spider test; Spider dev, Spider-Syn, Spider-Realistic and
Spider-DK, with test-suite accuracy (TS), for breadth. Five clients
under a non-IID partition; one training seed; the exact McNemar test on
paired predictions with Holm correction within each table. The folder
`results/` contains every table and every macro; a cell printed as `--`
awaits its result.

- Against FedAvg SFT at the same number of rounds: `\gain{bird}{fedavg}{4}{k2}{4}`
  EX on BIRD dev (+6.19) and `\gain{spider}{fedavg}{4}{k2}{4}` on Spider
  test (+3.49), both significant, and higher on every difficulty level.
- FedAvg SFT stops improving after round 3 on both datasets; additional
  FedAvg SFT rounds do not close the gap.
- From the same model, one preference round adds more than a further
  FedAvg SFT round.
- The preference rounds halve the execution errors on both datasets;
  the number of incorrect results does not decrease.
- A large part of the gain on BIRD consists of correct predictions that
  use other tables or columns than the gold SQL query.
- Components: on BIRD, on-policy pairs outperform the pairs and the
  reference model of the first preference round; without the NLL term a
  preference round lowers accuracy (Spider); the preference term
  removes execution errors that persist under training on the correct
  samples alone; with warm-up rounds the gain persists under TS on the Spider
  sets; the weights of the aggregation are immaterial.
- Breadth: the 0.5B model also improves over FedAvg SFT, by a smaller
  margin; the gain persists on the perturbed sets and under TS.
- Cost: no additional communication; the cost is client computation
  for sampling, execution and local training.

## Contributions

1. A source of supervision: the databases of a client constitute
   supervision that federated fine-tuning does not exploit, and it is
   accessible only at the client. To our knowledge, \method is the first federated
   training method for Text-to-SQL that uses it.
2. The framework \method, as specified above.
3. The evidence: the gain over FedAvg SFT on BIRD dev and Spider test,
   its origin, the role of each component and the cost for a client.
4. The release: code, client splits and the predictions of every row.

## Organization

| Section | Content | Tables and figures |
|---|---|---|
| 1 Introduction | problem, limitation, key observation, framework, results, contributions | |
| 2 Related work | fine-tuned models for Text-to-SQL; preference optimization and execution feedback; federated fine-tuning of language models; federated semantic parsing | Table 1 |
| 3 Method | problem formulation, framework overview, the components, algorithm and cost | Fig. 1, Algorithm 1 |
| 4 Experimental setup | datasets, federated setups, models, baselines, metrics, implementation, statistical protocol | Table 2 |
| 5 Results | RQ1 the gain over the baselines; RQ2 other models and federated setups; RQ3 perturbed questions and TS; RQ4 the change in the predictions and the cost | Tables 3 to 7, Figs. 2 and 3 |
| 6 Ablation study | the contribution of each component | Table 8 |
| 7 Discussion and limitations | mechanisms and implications; the scope of the study | |
| 8 Conclusion | synthesis and future work | |

The limitations, each stated once in Section 7: gold SQL queries and
queryable databases are required at every client; five clients (ten in
one setup) with full participation; data isolation without differential
privacy; additional client computation; an execution label rests on one
database, so that an incorrect query may match by coincidence; one
training seed for most rows; models of 0.5B to 1.5B parameters with
LoRA on English SQLite benchmarks; the number of warm-up rounds is a
setting.

# Working guide

## 1. Readership and stance

The readership consists of reviewers and researchers in federated
learning and natural language processing. They assess the novelty of the
contribution, the technical soundness of the method and the adequacy of
the empirical validation, and they form this assessment primarily from
the abstract, the introduction, the figures and the tables.

The section is written from the position of the authors of a machine
learning research paper who present a completed contribution to peers.
`voice.md` specifies the register and the rhetorical organization of
each kind of section. American spelling is used throughout, and em
dashes are not used.

## 2. Materials

`README.md` lists the files of the working directory. `brief.md` specifies
the aim of the section and the points of its argument; `results/`
contains every table, figure and macro of the paper, not only those of
the section; `related/` contains the cited works of the section;
`sections/` contains the sections already written and the file of the
present section. The papers in `examples/` illustrate how a paper of
this kind is constructed and how it reads; they supply neither facts nor
wording.

## 3. Constraints

Four constraints ensure that the manuscript is accurate and that it
compiles.

1. **Facts.** Every statement about the present work (a configuration,
   a count, a formula, a result) originates from the materials. A
   statement about a cited work originates from `related/` or, where web
   search is available, from the source itself; such a statement is
   listed in the notes with its address and its location in the source.
   Where required information is unavailable, it is requested from the
   editor (Section 5); nothing is supplied by conjecture.
2. **Findings.** A finding is stated as its table supports it, and its
   scope ("on BIRD", "to our knowledge") forms part of the finding. If
   the evidence appears insufficient for a point of the brief, the
   concern is recorded in the notes.
3. **Numbers and names.** Results and configuration values are macros
   (`results/macros.md`, `results/settings.md`) and are never typed as
   digits. A number that awaits its result is written with its macro
   and prints as a placeholder; where the brief provides an expected
   value, `\expect{value}` replaces the macro and the location is listed
   in the notes. The method is `\method` and the trained model is "the
   model". Terminology and notation conform to `terms.md`. Citations use
   `\cite{key}` with the keys of the brief, and cross-references use the
   labels that the brief lists.
4. **Form.** The headings specified by the brief, with no level below
   `\subsubsection` and no `\paragraph`; the commands of the document
   class, without additional packages; a length close to the target of
   the brief.

## 4. Authorial latitude

All remaining decisions belong to the author of the section: the number
and sequence of paragraphs, the emphasis, the selection among the
available numbers, an illustrative example, the transitions. The points
of the brief are the points of an argument and not a list of paragraphs
to produce: they are merged, divided and ordered as the argument
requires. Before the draft is delivered, the section is examined from
the perspective of a reviewer and revised wherever that reader would
hesitate.

## 5. Questions to the editor

The editor is one of the researchers of the study and has the complete
record of the work: the method in every detail, every experiment and
its outcome, and the cited literature. At any stage (before the outline,
during drafting, during a revision) a question whose answer the section
requires and the materials do not provide is addressed to the editor:
the questions are written to `notes/questions.md`, each with the passage
it concerns and the reason it is required, and the turn ends there. The
editor replies with the answers and, where appropriate, with additional
files. Typical subjects are a property of the method, the configuration
or the outcome of an experiment, an additional number or comparison,
the interpretation of a result, and what a cited work states. A question
is preferable to a conjecture and to an omission; questions on one
passage are submitted together.

## 6. Outline before prose

An outline precedes the prose and is written to `notes/outline.md`: one
entry per paragraph, in sequence, stating the rhetorical function of
the paragraph (as designated in `voice.md`), the proposition it
establishes, any equation, table or figure it contains, and its
approximate length. Read in sequence, the entries constitute the
argument of the section. The entries are annotations, not sentences of
the manuscript.

The editor responds to the outline, and the section is drafted from it.
The outline is a plan and not a commitment: a superior organization that
emerges during drafting is adopted and reported in the notes.

## 7. Deliverables

The outline in `notes/outline.md`, the section in LaTeX in its file
under `sections/`, questions in `notes/questions.md`, and the notes to
the editor in `notes/notes.md`. The notes identify points whose evidence
appears insufficient, statements and references taken from the web, and
proposals for an additional example, table or figure.
