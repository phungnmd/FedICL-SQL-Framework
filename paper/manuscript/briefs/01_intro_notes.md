# Notes: Section 1, Introduction (with the abstract, the keywords and the title)

Files: `sections/01_intro.tex`, `sections/00_abstract.tex`,
`sections/00_keywords.tex`. Written from `briefs/01_intro_outline.md`
and the editor's answer to it.

## Length

| Part | Words | Brief |
|---|---|---|
| Introduction | about 1,020 (paragraphs 120, 153, 91, 127, 109, 142, 131, then the list with its lead-in, 146) | about 945, 1,050 at most |
| Abstract | about 236 | 150 to 250 |
| Keywords | 6 | 4 to 6 |

The Introduction is under the upper end and above the outline. The
excess is in paragraphs 2 (setting, 153 against 125), 4 (execution
label, DPO and CodeLutra, 127 against 85) and 5 (FedDPO, 109 against
95): each carries terms that Section 2 uses without defining them. If
pages have to be won, the first candidates are the description of
CodeLutra's iteration in paragraph 4, which Section 2.2 repeats, and
the first sentence of the abstract's result.

## Where the draft departs from the outline

1. Paragraph 6. The outline gave the idea two sentences (what
   execution does, then "a client samples, executes, compares") before
   the method. The second sentence said what the sentence on the
   preference rounds says again three lines later, so the idea is now
   the opening sentence alone, with "on the databases of a client" in
   it, and the procedure is told once.
2. Paragraph 7, the cost. As corrected by the editor: "requires no
   communication beyond that of FedAvg SFT, and its additional cost is
   computation at the clients", a sentence about the method and not
   about every preference round.
3. Paragraph 7, the rounds. "After `\setting{rounds.total}` rounds"
   names the number once, as asked. It prints as the digit 4 in running
   text.
4. Contributions, item 2. The outline listed "the same communication
   as FedAvg SFT" there. Paragraph 6 ends on what leaves a client and
   paragraph 7 on the communication, so a third mention within fifteen
   lines was dropped from the item.
5. Abstract. The method sentence now says "the small set of adapter
   weights that it trains and one integer", so that the adapter is
   readable without Section 3. "Execution accuracy" is written in full
   and not abbreviated, since the abstract uses it once. DPO keeps its
   abbreviation although it is used once: it is the term a reader
   searches for.

## Where the draft departs from the brief

1. Statement 3, "the databases go unused". The prompt is constructed
   from the database (its schema, and three example rows per table on
   Spider, Section 4.5), so the sentence reads: "The databases at the
   clients thus serve only to construct the prompt; as a source of
   supervision, they remain unused."
2. Statement 3, "Zhang et al. train this way". The preceding sentence
   describes FedAvg with LoRA adapters, and the brief gives T5-base
   and SFT for Zhang et al., nothing on adapters. The sentence says
   that they "study federated learning under the same supervision".
3. Statement 4, FedDPO. Worded as "DPO has been used in federated
   training, in the FedDPO of OpenFedLLM, but without such a label",
   and not as the only federated DPO: Section 2.3 also has Wu et al.,
   who train with DPO at the server. "A dataset of human preferences
   that each client holds in advance" comes from the ceiling of
   statement 4.
4. Statement 7, the percent sign. The EX values carry `\%` in
   paragraph 7 ("48.76\% ... against 42.57\%"), since the Introduction
   has no table whose caption gives the unit; the gains are "points".
   Section 5 prints the same macros without the sign. Remove the four
   `\%` if the paper should be uniform.

## What I doubt

1. "Both differences are significant" stands without the test or the
   level, which Sections 4.6 and 5.1 give. A reader of the
   Introduction alone has to take it on trust.
2. The opening sentence of paragraph 1 defines the task and names the
   benchmarks; the point of the paragraph (two lines of systems, one
   of which an organization can train and serve itself) arrives in
   its second and third sentences.
3. "By federated Text-to-SQL, we mean this federated training of the
   model" settles the phrase by saying what it means here. It does not
   name the other reading (queries over federated databases).
4. Paragraph 3 says "as currently practiced" of FedAvg with LoRA and
   SFT. The support is Section 2.3 (FederatedScope-LLM, OpenFedLLM),
   neither of which the Introduction cites at that point.
5. Section 8 describes the method in parallel. The Introduction uses
   "warm-up rounds, which are rounds of FedAvg SFT", "samples several
   queries per question from the current global model", "labels them
   by execution on its own databases", "pairs correct with incorrect
   samples", "a preference term, which is the DPO loss, and an NLL term
   on the correct sample", "the global model of the round being the
   reference model".

## What the brief lacked

1. What "LS" in the name stands for. The title candidates do not
   expand it, and neither does the text.
2. The level and the test behind "significant" as a clause fit for
   the Introduction, if doubt 1 is to be answered there.

## Not checked

The section compiles: one `pdflatex` pass of `main.tex` into a
scratch directory, without error, and the first three pages were read
as text. BibTeX was not run; the thirteen keys were found in
`references.bib`. `make` and `make lint` were not run, since they
write to `build/`.

## Title candidates

Each of 15 words or fewer, with no abbreviation other than SQL and the
name.

1. FedLS-SQL: Federated Fine-Tuning for Text-to-SQL with Execution
   Labels from the Clients' Databases (12 words)
2. FedLS-SQL: Federated Preference Optimization with Client-Side
   Execution Labels for Text-to-SQL (11 words)
3. FedLS-SQL: Learning from Query Execution on Client Databases in
   Federated Training of Text-to-SQL Models (14 words)

The first follows the argument of the paper most closely: the
supervision (execution labels), where it comes from (the clients'
databases), the task and the setting. The second names the mechanism
(preference optimization) at the price of the databases. The third
reads most easily and names neither labels nor preferences.

## A proposal

No float is proposed for the Introduction. If a later revision has
room, a three-line example in paragraph 4 (one question, its gold SQL
query, one sample that returns the same result in another form and
one that fails to execute) would show what "correct and incorrect
queries of the model's own" are before Fig. 1 does.

## Revision 1

After the editor's notes of round 1 (a reader with the first three
pages of the PDF). The Introduction is now about 1,040 words by the
same count as before (paragraphs 79, 162, 88, 136, 111, 185, 160, then
the list with its lead-in, 117), under the upper end of 1,050 with
little room; the abstract is about 232 words.

### What was done with each note

1. What the federated setting changes (paragraphs 4 to 6).
   Paragraph 5 now opens on the two things that differ from one site:
   the label can be computed only at a client, and the model whose
   queries are to be labeled is the global model, which changes with
   every round. Paragraph 6 then positions the method against
   CodeLutra in one sentence, as Section 3.4 does: CodeLutra runs the
   loop at one site, from the pretrained model; `\method` runs it
   across the clients and after the warm-up rounds, a federated round
   being the step that renews samples, labels and pairs, with its
   global model, which no single party trained, as the reference model
   of every client. "Only a client can compute the labels" is said
   once, in paragraph 5, and not again in that sentence. "From the
   pretrained model" is taken from Section 3.4, not from the brief.
   No result of the pooled row is used.
2. What the comparison is (paragraph 7). Added: the clients are
   simulated by assigning each database of the training set of BIRD or
   Spider, with all its questions, to one client, and the model is
   evaluated on databases that no client holds; the division of the
   rounds, as "(`\setting{rounds.warmup}` warm-up and
   `\setting{rounds.pref}` preference rounds for `\method`)"; "both
   significant under the exact McNemar test"; and the highest EX of
   FedAvg SFT on BIRD dev, `\ex{bird}{fedavg}{3}` at round 3, with
   `\gap{bird}{fedavg}{3}{k2}{4}` points to `\method`. The sentence
   "Further rounds of FedAvg SFT do not close this gap" gave way to
   this number.
3. The premise (paragraph 2). Added the answer from the setting:
   alone, an organization could train a model on its own few databases
   only, whereas the model is meant to serve all the organizations, on
   questions and databases beyond those that any one holds. No
   sentence on the result of local training. For the concrete case I
   added "for example a hospital or a bank". It is an illustration of
   mine and rests on no row of the brief; remove it if the paper
   should name no sector, or replace it with a case the owner prefers.
4. The two statements in conflict (paragraphs 2 and 3). (a) The
   opening of paragraph 3 is now scoped to the task: "For Text-to-SQL,
   federated fine-tuning has so far learned from the gold SQL query
   alone"; the sentence on FedAvg with LoRA and SFT follows as the
   common practice. (b) Paragraph 2 says what SFT needs the databases
   for ("the databases to which they refer, whose schemas enter the
   prompt"), so that "serve only to construct the prompt" in
   paragraph 3 reads as its continuation. The abstract no longer says
   that fine-tuning requires the databases; its gap sentence reads
   "no query is executed on the databases at the clients, although
   execution shows whether a generated query is correct".
5. Earlier work as Section 2 has it. (a) Paragraph 4 now gives both
   ways in which execution trains a model at one site: as a reward in
   reinforcement learning (SLM-SQL, Think2SQL, Arctic-Text2SQL-R1) and
   as the label of the pairs in DPO, with CodeLutra iterating the
   latter. (b) FedDPO: "each client holds a preference dataset, for
   helpfulness or harmlessness", as Section 2.3 words it; "human
   preferences" is gone. (c) "therefore" is gone: the fixed pairs
   follow from the preference dataset ("so that the pairs are fixed in
   advance and are not outputs of the model being trained"), and the
   reference model and the missing NLL term are stated beside it as
   two further properties.

### Repetitions and cuts

- The databases as unused supervision: paragraph 3 no longer ends on
  it and states only that no query is executed and the databases
  serve to construct the prompt. It remains in the abstract, at the
  end of paragraph 5 (the scoped gap of statement 4) and in
  contribution 1 (the "first" of statement 8), the last shortened to
  "the first method that uses it".
- The parameter ranges of CodeS and OmniSQL are gone from paragraph 1;
  the one range kept is that of SLM-SQL, the one the model of this
  paper falls in. OmniSQL is cited for "this line of work" without a
  description.
- To hold the length: the prompting systems are one shorter sentence;
  the idea sentence of paragraph 6 lost "a federated fine-tuning
  method"; the description of federated learning in paragraphs 2 and
  3 no longer says twice that the server averages; contribution 2 and
  the lead-in of the list are shorter.

### Other changes that follow from these

1. Spider and BIRD are now cited in paragraph 7, their first mention,
   since the clause on the cross-domain benchmarks left paragraph 1.
   What that clause said (evaluation on databases outside the training
   set) is carried by "evaluate it on databases that no client holds".
   Section 2.1 still meets both names after their citation.
2. The cost. Paragraph 6 ends: "Only the adapter and the number of
   pairs that weights it leave a client, as the adapter and the number
   of questions do in FedAvg SFT; the additional cost of the method is
   computation at the clients." The separate sentence on communication
   at the end of paragraph 7 was removed as a repetition of the first
   half.
3. Paragraph 7 opens "on two benchmarks" and names them in the next
   sentence.

### What I doubt after the revision

1. Paragraphs 6 and 7 are long (185 and 160 words). Each makes one
   point, but a split of paragraph 6 before "Whereas CodeLutra" would
   give the positioning its own opening sentence, at no cost in words.
2. "After 4 rounds (2 warm-up and 2 preference rounds for FedLS-SQL)"
   prints three digits in one line of running text.
3. The scoped claim appears twice in the body (end of paragraph 5,
   contribution 1). Both are statements of the brief; if one should
   go, contribution 1 can keep the observation and leave "first" to
   paragraph 5.
4. The length leaves about ten words under the upper end by my count
   (macros counted as one word each, citations not counted). A second
   round that adds content needs a cut named with it.

### Not checked

One `pdflatex` pass of `main.tex` into a scratch directory, without
error, after the last edit; the first two pages were read as text
before the last two wording changes. BibTeX was not run; the two new
keys (`papicchio2025think2sql`, `yao2026arctic`) are in
`references.bib`.

## Revision 2

After the editor's notes of round 2 (a second reader with the first
three pages). The Introduction is about 1,047 words by the same count
(paragraphs 73, 146, 79, 134, 82, 144, 96, 187, then the list with its
lead-in, 106), three under the upper end. The abstract is about 241
words.

### What was done with each note

1. The differences and their reasons (paragraphs 5 to 7).
   - `\method` is no longer presented as CodeLutra's loop moved to the
     clients. The sentence "Whereas CodeLutra runs such a loop ...
     `\method` runs it across the clients" is gone, and with it "which
     no single party trained" and "from the pretrained model".
     Paragraph 4 gives CodeLutra as the closest work in one sentence
     (pairs constructed anew in every iteration from correct and
     failed samples of the current model, the DPO loss and an NLL
     term); paragraph 5 says where it stops for this setting (a single
     party holding all the data, while the label can be computed only
     at a client) and, in the same paragraph, where FedDPO stops, so
     that the two halves of the novelty stand together.
   - Each part of the method now has its reason. The warm-up rounds
     come first "because pairs require a correct and an incorrect
     sample of the same question and the pretrained model leaves more
     questions without a correct sample" (Section 3.3). A new paragraph
     7 gives the reason for the renewal and for the reference model
     (Section 3.4): the global model changes with every round, so the
     pairs are constructed anew from its samples and reflect the errors
     it currently makes, and, as the model with which every client
     starts the round, it is the reference model, so that the
     preference term measures the change made by local training. The
     opening of paragraph 5 no longer raises "the global model, which
     changes with every round" without a consequence; the phrase now
     stands where its consequence follows.
   - FedDPO: paragraph 7 says that the renewal and the NLL term are
     absent from FedDPO and what the ablation study finds for each:
     holding the pairs and the reference model fixed lowers EX on BIRD
     dev (B1), and without the NLL term a preference round brings no
     gain on Spider test (B3). Both are worded as Section 6 has them,
     each with its set and without a number.
2. Paragraph 8 (the results).
   - (a) The errors are tied to the gain: "The gain comes with about
     half the execution errors (...), whereas the predictions that
     execute and return an incorrect result do not become fewer."
   - (b) The baseline at round 4: its EX at round 3 on BIRD dev "does
     not differ significantly from that at round 4 and is
     `\gap{bird}{fedavg}{3}{k2}{4}` points below `\method`".
   - (c) The size of the cost: "A preference round takes
     `\fact{cost.spider.pref2.ratio}` to `\fact{cost.bird.pref1.ratio}`
     times the client time of a FedAvg SFT round." The sentence "the
     additional cost of the method is computation at the clients" gave
     way to it; that nothing more is communicated is said at the end
     of paragraph 6 (what leaves a client).
   - (d) Contribution 3 names the variants: without the preference
     term, without the NLL term, with fixed pairs and reference model.
3. Citations. OmniSQL is no longer cited in the Introduction; the
   sentence on models of 0.5B to 1.5B parameters cites SLM-SQL alone.
   "Commonly fine-tuned across clients" cites `kuang2024fsllm` and
   `ye2024openfedllm`, and LoRA keeps its own citation. CodeLutra is
   "a method for code generation evaluated on Text-to-SQL", as in
   Section 2.2.
4. Contribution 1 is scoped as the brief has it: "We observe that the
   databases of a client are supervision that federated fine-tuning
   leaves unused, and we propose `\method`, to our knowledge the first
   method for the federated training of Text-to-SQL models that uses
   it."
5. The abstract. One name for the baseline, introduced as "federated
   averaging with supervised fine-tuning (FedAvg SFT)" and used four
   times; "a negative log-likelihood (NLL) term"; "the adapter weights
   that it trains and one number that weights them in the average,
   here its number of pairs". The first sentence is rewritten with one
   subject and one verb chain ("Organizations hold ... and cannot pool
   them to fine-tune a Text-to-SQL model"). The last sentence says
   "about half as many of its predictions end in an execution error".

### Room made

- The loop of CodeLutra is described once (paragraph 4).
- The procedure of the method is in paragraph 6 only; the former
  contribution 2, which repeated it, is merged into contribution 1.
  The list still has four items: the observation with the method, the
  results with the analysis and the cost, the ablation study, the
  release.
- The sentence "To our knowledge, no earlier method ..." at the end of
  paragraph 5 is gone; the scoped claim is made once, in contribution
  1.
- Paragraphs 1 to 3 are tighter (prompting systems and fine-tuned
  models in one sentence, the mechanics of federated learning in one,
  Zhang et al. in a clause).
- The fourth contribution reads "all predictions" for "the predictions
  of every row of our tables".

### What stays open

1. Length. Three words under the upper end by my count (macros
   counted as one word each, citations not counted). Another count
   may put it above; the first sentences to give are "for example a
   hospital or a bank" (paragraph 2) and the clause on SLM-SQL
   (paragraph 1).
2. The gap is no longer stated as a sentence where the gap is argued
   (paragraph 5); a reader meets "to our knowledge the first" only in
   the list. If it should stand in paragraph 5, the list can keep the
   observation and drop "first", at about the same length.
3. The ablation findings in paragraph 7 are one set each, as the
   committed results allow: the row without the NLL term on BIRD dev
   is not in, and with fixed pairs and reference model Spider test is
   level, which the sentence does not say. When the BIRD row is in,
   the sentence on the NLL term can name both sets or has to keep to
   Spider.
4. The NLL term has its finding and not its reason (Section 3.4: the
   preference term constrains the two samples of a pair only relative
   to each other). There was no room for it.
5. Paragraph 7 has no opening sentence that states its point; it
   starts on the reason itself ("Since the global model changes with
   every round, ..."). Paragraph 8 is 187 words.
6. "does not differ significantly from that at round 4" rests on
   Section 5.1; the Introduction gives no p-value.
7. The cost range takes the lowest and the highest of the four
   ratios of Table 7 (`cost.spider.pref2.ratio`,
   `cost.bird.pref1.ratio`). If a later run changes which round is
   lowest or highest, the two macros have to be chosen again.
8. Digits in running text: "After 4 rounds (2 warm-up and 2
   preference rounds ...)" and "0.9 to 2.7 times".
9. The contributions depart from the grouping of statement 8 (see
   "Room made").

### Not checked

One `pdflatex` pass of `main.tex` into a scratch directory, without
error, after the last edit of the Introduction; the abstract and the
method paragraphs were read as rendered text before the last trims.
BibTeX was not run; `kuang2024fsllm` is in `references.bib`.
