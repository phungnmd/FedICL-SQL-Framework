# Notes to the editor: Section 2, Related work (revision 2)

File revised: `sections/02_related.tex` (the four subsections and
Table 1). The paper compiles with it, built in my scratch folder: no
undefined reference or citation, no overfull box, lint with 0 STOP. The
lint notes on this file are the typed model sizes of cited papers, the
names of systems read as abbreviations, and "lab word: feddpo" on the
two sentences that name FedDPO, the term of `TERMS.md`. I opened the
rendered page and read Table 1. I read the corrected statements of the
brief (2.1.1, 2.2.2, 2.2.3, 2.2.4, 2.2.6, 2.4.1) before revising.

## What changed for the five notes of round 2

1. CodeLutra (2.2, par. 4, a paragraph of its own).
   - What is taken is named as Section 3.4 has it: the sampling settings
     (the number of samples and the temperature), the scale of the DPO
     term, the uniform pairing and the choice of reference model. The
     number of pairs and the NLL term are no longer under "taken", so
     the two halves do not contradict each other.
   - The differences open with what is not shared: the loop runs across
     clients, a federated round takes the place of the iteration, each
     client samples from the global model of the round, "which no single
     party trained", and labels the samples on its own databases. Then
     the warm-up rounds of FedAvg SFT, fewer pairs, the NLL term
     averaged over tokens. That the pairs are renewed is not listed as a
     difference.
   - One name for the term: "NLL term" for Pang et al., CodeLutra and
     ours; "likelihood term" is gone.
   - Table 1: the caption says what a tick under Text-to-SQL means ("a
     method that is trained and evaluated on this task"), and the tick
     of CodeLutra has a note, "And on data-science code".
2. Pang et al. (2.2, par. 3). Named, with what is theirs: in each
   iteration, answers sampled from the current model, a correct one
   paired with one that is not, a DPO and an NLL term, the model of the
   previous iteration as the reference. CodeLutra is then said to apply
   "this iterative scheme at one site, with execution labels", so these
   ingredients are not credited to CodeLutra alone. The sentence on
   Lanchantin et al. stays out. The room came from the repetitions the
   reader listed (see "Length").
3. Liu et al. (2.2, par. 2). The three choices stand as three clauses of
   one sentence (pairs constructed once, the DPO loss alone, that model
   as a fixed reference), and the pointer reads: "Our model also outputs
   the query alone, and Section 6 varies all three of these choices."
   It names no removal and no expected outcome.
4. Training without labels. "The preference needs no annotation beyond
   the gold SQL query that SFT already uses" (2.2, par. 1); "Our
   question is what execution on the databases of a client adds to the
   gold SQL as supervision" (2.4, par. 1).
5. The ends of 2.1 and 2.2, and the opening of 2.1.
   - 2.2 has no closing sentence on where a label can be computed. "At
     one site" is said once, in the sentence on CodeLutra. The sentence
     on LEVER and GradeSQL moved to the first paragraph, after the
     sentence on how execution decides the preference, so that the
     subsection ends on the paragraph that leads to the method.
   - 2.1: the privacy motive of CodeS is out. I tried the step once more
     (the privacy of one site toward a provider; several sites that
     cannot share with one another) and it cost 51 words that the
     section needed for Pang et al. and for the pointer to Section 3.4.
     2.1 is one paragraph and ends on the setting these methods assume.
   - The opening of 2.1 now reads "differ in the data and in the
     objective of training", and the sentence on the three
     reinforcement-learning works says that they "change the objective".

## Length

893 words of running text by my count (citations not counted, a
reference and `\method` counted as one word each), against the upper
end of 900.

| Part | Brief | Revision 1 | Revision 2 |
| --- | --- | --- | --- |
| 2.1 | 180 | 162 | 130 |
| 2.2 | 260 | 351 | 406 |
| 2.3 | 220 | 204 | 195 |
| 2.4 | 150 | 175 | 162 |

2.2 carries the two closest works with their pointers and is now half
of the section; the other three subsections are below their budgets.
What paid for the additions: the privacy motive (51 words), the closing
sentence of 2.2 (31), the three ways of saying that the pairs of FedDPO
are fixed (now one clause), the exact-match clause on Zhang et al., and
"constructed anew in each round" in the last paragraph, which now says
"renewed pairs of the model's own outputs", the word of Table 1.
"Constructed anew" stands once in the section, in the caption that
defines "renewed"; "one site" stands twice, in 2.1 and in the sentence
on CodeLutra.

If the section has to lose words, in this order: the clause on Xu et
al. (15); "for helpfulness or harmlessness" (4); the two task areas of
PubSwap and Fed-GRPO, leaving one sentence on the two works (about 12).

## Where the brief does not hold, or is not served

1. Statement 2.1.1, the privacy motive of CodeS: left out, as its
   ceiling allows.
2. Statement 2.1.1 groups SLM-SQL, Think2SQL and Arctic-Text2SQL-R1 as
   "SFT followed by reinforcement learning". The rows support SFT before
   the reinforcement learning for SLM-SQL only. The sentence says that
   the three train the model by reinforcement learning with an
   execution-based reward, and does not say what precedes it.
3. Statement 2.2.3, Lanchantin et al.: left out, as its ceiling allows.
   The key `lanchantin2025bridging` is not cited in this section.
4. Statement 2.2.6 has no sentence of its own: "at one site" in the
   sentence on CodeLutra carries it, as the ceiling says. It is thus
   stated for CodeLutra and not, in words, for Liu et al. and ExCoT.
5. Statement 2.3.1, "with code generation among their tasks": cut in
   revision 1 for length and not restored.
6. Statement 2.3.4, the half on the execution label ("where the label is
   the execution result on a database of the client"): not repeated in
   2.3, after the note of round 1 on the four stops. The sentence reads
   "None of the federated works of this subsection considers
   Text-to-SQL."
7. Statement 2.4.1: "exact match as the metric" and the numbers of its
   Table 2 are out; "nothing is executed, in training or in evaluation"
   carries the point. "The earlier work" is written as "was studied
   earlier by Zhang et al.", so that "only" stands once, under "to our
   knowledge".
8. Statement 2.4.4: the sentence under "to our knowledge" says "no
   earlier method combines federated training with execution labels and
   renewed pairs of the model's own outputs". The sentence that read
   Table 1 aloud is not written.

## Departures from the outline

1. 2.1 is one paragraph.
2. 2.2 has four paragraphs: DPO, the preference from execution and the
   models that select among candidates; Liu et al.; the methods that
   renew the pairs (ExCoT, Pang et al.); CodeLutra with what is taken
   and what differs.
3. 2.3, par. 3: PubSwap and Fed-GRPO share one sentence; their
   mechanisms are left out.
4. 2.4: the clause on Xu et al. is in the first sentence.
5. Table 1: four columns, the last in words ("none (supervised
   training)", "from a dataset, fixed", "own outputs, renewed"); two
   notes in the caption with superscript letters in the cells, as the
   other tables explain their marks in the caption.

## Doubts

1. The paragraph on CodeLutra describes the method in about 60 words
   before Section 3 does. It uses "global model", "warm-up rounds of
   FedAvg SFT" and "NLL term" on the assumption that Section 1 has given
   the method in three sentences. "The uniform pairing" and "the scale
   of the DPO term" are explained only in Section 3.4, to which the
   sentence points.
2. "It applies this iterative scheme" describes CodeLutra by the scheme
   of the sentence before it. The rows support that the two schemes
   have the same parts; they do not say that CodeLutra builds on Pang et
   al., and the sentence does not say so.
3. "Section 6 varies all three of these choices" rests on your
   description of the ablation rows (one row keeps the pairs and the
   reference model of the first preference round, another removes the
   NLL term). Section 6 is not written; the sentence has to be read
   again when it is.
4. "Execution labels" is used in the paragraph on CodeLutra and in the
   last paragraph before Section 3 defines it. The first paragraph of
   2.2 describes the comparison and calls its outcome "labels".
5. Spider, BIRD and BIRD dev are named without a citation, on the
   assumption that Section 1 cites the benchmarks.
6. "GRPO" appears only inside the name Fed-GRPO and is not expanded.

## Left out

Facts of the brief that the section does not use:

- CodeS: StarCoder as its base, the 21.5 GB of the corpus, its three
  motives.
- OmniSQL: the counts of SynSQL-2.5M, the chain-of-thought solutions,
  Qwen2.5-Coder-Instruct as its base.
- SPFT-SQL: the templates, the SQL-to-Text model, the opponent model,
  its list of models.
- SLM-SQL: its training data and its inference by voting; Think2SQL and
  Arctic-Text2SQL-R1: their rewards in detail and their model sizes.
- DPO: that the reference is the model the preference data were sampled
  from (Section 3.4 says it).
- Liu et al.: 16 samples per question, the dropped questions, all
  weights fine-tuned.
- ExCoT: its models and benchmarks, the number of rounds and of samples,
  the chain-of-thought form of its outputs.
- Pang et al.: the chain-of-thought form of the answers, its tasks by
  name, its model.
- Lanchantin et al.: everything.
- CodeLutra: Llama-3-8B, the four iterations, the weight of its NLL
  term, the model of the previous iteration as its reference (the
  sentence on Pang et al. gives it for the scheme).
- LEVER and GradeSQL: what the verifier reads, the datasets.
- FederatedScope-LLM: the parameter-efficient methods by name, the code
  generation benchmark with nine clients. OpenFedLLM: the seven
  algorithms, the 7B model, code generation as a domain, how the two
  preference datasets were built.
- Wu et al.: that the server aggregates the selectors, that the server
  generates the pairs, that FedDPO is one of its baselines.
- PubSwap and Fed-GRPO: the averaging of LoRA adapters, the exchange of
  responses on public prompts, the weighting by the standard deviation
  of the rewards, the model sizes.
- Zhang et al.: the numbers of its Table 2, FedProx and FedOPT, the
  weighting rule of Lorar, exact match, that neither Spider nor BIRD is
  used.
- Xu et al.: BART, SPARQL, the fusion strategy.

## Proposal

None for a further float.
