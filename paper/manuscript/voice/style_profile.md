# Style profile

The register of the paper, measured in published papers of the field
and of the target journal. The measures behind it are in
`style_profile_data.md`, written by `tools/style_profile.py`.

**Sources**: ten published papers of the field and of the
target journal: GradeSQL (Journal of Intelligent Information Systems,
2026), CodeS (SIGMOD 2024), BIRD (NeurIPS 2023), the test-suite paper
(EMNLP 2020), CodeLutra (arXiv 2411.05199), DPO (NeurIPS 2023), LoRA
(ICLR 2022), FedAvg (AISTATS 2017), FedProx (MLSys 2020), OpenFedLLM
(arXiv 2402.06954). Body text only, without abstracts, floats and
appendices: 52,000 words.

**How it binds**: register and terms are followed; the figures for
rhythm describe a range and are not targets.

**Sentence Length**: mean 21 to 26 words by kind of section
(introduction 26, related work 23, method 23, experiments 21,
discussion 24), standard deviation 10 to 14. Rhythm: variable. A
definition or a result is a short declarative sentence; a motivation or
a comparison with earlier work runs to 35 words and more.

**Paragraph Length**: mean 3.7 to 5.1 sentences. Shortest in method and
discussion, longest in related work.

**Vocabulary Preferences**:

- Hedging: sparse in the body, 2.5 to 4.0 per 1,000 words; 10 per
  1,000 in discussion and conclusion. Words: may, could, might,
  suggests, indicates, likely, potentially. A result read from a table
  is stated in the plain present tense; "suggests" and "indicates"
  introduce an explanation of it.
- Transitions: while, however, specifically, since, thus, therefore,
  for example, for instance, in practice, in particular, instead; in
  experiments also additionally and finally.
- Verbs: in method sections use, employ, denote, introduce, consider,
  note; in experiments evaluate, show, achieve, observe, report,
  compare; in introductions and related work propose, introduce,
  demonstrate.
- Formality: formal, in the terms of the field. Words of nine letters
  or more are 18 to 23% of the text. Everyday verbs (write, run, give,
  get, say, keep, leave, hold, let) are under 3 per 1,000 words. No
  contractions.
- Person and voice: "we" in 39 to 47% of the sentences of
  introduction, method and experiments and in 18% of related work.
  Passive in 14 to 21% of sentences, most in method sections, where
  the procedure is the subject.

**Citation Style**: numbered or parenthetical in 92 to 96% of cases; a
paper is named as the subject of a sentence in 4 to 8%. Density per
paragraph: related work 4.2, introduction 1.6, experiments 0.9, method
0.6.

**Modifier Style**: minimal. Intensifiers (significantly, highly,
substantially, consistently) 1.5 to 3.3 per 1,000 words, lowest in
method sections.

**Register Shifts**:

| Kind of section | Register |
|---|---|
| Introduction | assertive on the problem and on what earlier work leaves open; the longest sentences; the contribution stated in the first person |
| Related work | descriptive and impersonal; dense in citations; each line of work credited, then the point where it stops |
| Method | definitional and procedural; "we" for a design choice, the passive for a step of the procedure; almost no intensifier; a formula is followed by what it does |
| Experiments | descriptive; the present tense for what a table shows; a cause that was not tested is marked as a conjecture |
| Discussion and conclusion | interpretive and hedged; limits stated as the scope of the study |

**Terms of the field** (counts in the ten papers are in the data file):

| Concept | Terms the papers use |
|---|---|
| a query the model outputs in training | sample, candidate, candidate SQL query; at evaluation: predicted SQL query |
| the reference query | gold SQL (query), ground truth |
| producing a query | generate; sample (when several are drawn) |
| running a query | execute, execution; a query "fails to execute" or "is executable" |
| outcome | correct and incorrect; execution error |
| federated roles | client, server, global model, local training, communication round, aggregation |
| adapting the model | fine-tuning, training |

The terms this paper uses, one for each concept, are fixed in
`TERMS.md`.

**Measuring a draft**: `tools/style_profile.py compare <section>.tex
--sources DIR --kind method` gives the same measures for a drafted
section beside those of the same kind of section in the ten papers.
