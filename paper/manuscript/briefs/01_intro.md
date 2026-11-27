# Brief: Section 1, Introduction, with the abstract and the keywords

Kind of section: introduction (`voice.md`, "Introduction"); the
abstract follows `voice.md`, "Abstract".

## Place in the manuscript

First section; no subsections. Followed by Section 2 (Related work),
which positions the framework against three research directions and
carries the comparison with centralized preference optimization from
execution feedback. Section 3 (Method) is written and is in
`sections/`; the introduction names the framework and its components
in the terms of that section and defines nothing formally.

Deliverables and lengths:

| File | Content | Length |
|---|---|---|
| `sections/01_intro.tex` | `\section{Introduction}`, label `sec:intro`; Fig. 1 | at most 1,050 words, about 950 requested, excluding the caption and the contribution list markup |
| `sections/00_abstract.tex` | the abstract: one paragraph, no citation, no macro-free number | 200 to 400 words, about 250 requested |
| `sections/00_keywords.tex` | 3 to 10 keywords separated by `\kwsep`; "Small language models" among them | the present six may stand |

## Aim

After the introduction the reader can state the limitation of federated
fine-tuning for Text-to-SQL that the paper addresses, the observation
that makes it addressable, what \method does about it and by how much
it improves over FedAvg SFT; and can locate the novelty against FedAvg
SFT and against FedDPO. After the abstract alone the reader retains the
same four elements and the headline number.

## Points of the argument

1. Context. Text-to-SQL as natural language access to relational data;
   the most accurate systems prompt proprietary large language models,
   which requires sending questions and schemas to an external
   provider. A small language model (SLM; here 0.5B to 1.5B
   parameters) is a model an organization can fine-tune and serve on
   its own hardware. Evidence: the cited systems.
2. Setting. One organization possesses few databases and few annotated
   questions; the data of several organizations cannot be pooled.
   Hence federated training of one SLM, with FedAvg SFT of a LoRA
   adapter as the prevailing approach. "Federated Text-to-SQL" denotes
   federated training of the model; stated once. Evidence: the cited
   federated fine-tuning work; the one earlier study of federated
   semantic parsing.
3. Limitations of existing federated training, two, each with its
   cause.
   (a) FedAvg SFT: the supervision is the single gold SQL query of a
   question. The client databases contribute only text of the prompt;
   neither the gold SQL query nor any query of the model is executed
   on them; the model receives no signal
   about which of its own queries are incorrect.
   (b) FedDPO: preference optimization exists in federated form, but
   on a fixed preference dataset whose two sides are not outputs of
   the model under training, with one reference model for the whole
   process. It does not reach the incorrect queries of the model being
   trained.
   Common cause: the signal that identifies those queries, execution
   on the database, exists only at the client.
   Evidence: the definitions of the two methods (Section 3.1; the
   cited paper).
4. Key insight. Execution at the client converts the single gold SQL
   query of a question into many correct and incorrect queries of the
   model's own; the label requires the gold SQL query and the
   database, hence the client. Fig. 1 carries the example; the text
   does not restate it.
5. The framework. \method, a federated learning framework for
   Text-to-SQL, with its four components by name and the function of
   each against limitation (a) or (b): supervised warm-up; client-side
   execution labeling (a); on-policy pair construction (b: pairs and
   reference model renewed with every global model, so that a
   federated round is one resampling step); the preference objective
   (preference term plus NLL term). What a client transmits: the adapter
   and one integer, as in FedAvg SFT. Evidence: Section 3.
6. Empirical validation. At the same number of rounds, +6.19 EX over
   FedAvg SFT on BIRD dev and +3.49 on Spider test, both significant.
   FedAvg SFT does not improve after round 3 on either dataset; over
   its highest round on BIRD dev the gain is 5.08. The execution
   errors of the predictions fall by about half on both datasets,
   significant. Evidence: Table 3 and Section 5.1; Section 5.2.
7. Contributions, four, as an itemized list in parallel form (entries
   under Materials).

The abstract carries points 2 to 6 in the five functions of
`voice.md`: context (federated training of an SLM for Text-to-SQL),
limitation (3a, and 3b in a clause), framework by name with its
mechanism (execution of the model's own queries at the client;
preference pairs renewed each round), results (the BIRD dev gain first,
then Spider test, then the execution errors), implication (client
databases as supervision at unchanged communication).

## Materials

### Numbers (macros of `results/macros.md`)

| Quantity | Macro | Value |
|---|---|---|
| principal model | `\setting{model}`, `\setting{model.size}` | Qwen2.5-Coder-1.5B-Instruct, 1.5 billion parameters |
| rounds: total, warm-up, preference | `\setting{rounds.total}`, `\setting{rounds.warmup}`, `\setting{rounds.pref}` | 4, 2, 2 |
| EX on BIRD dev, \method and FedAvg SFT, 4 rounds | `\ex{bird}{k2}{4}`, `\ex{bird}{fedavg}{4}` | 48.76, 42.57 |
| gain on BIRD dev at 4 rounds (headline) | `\gain{bird}{fedavg}{4}{k2}{4}`, `\pval{bird}{fedavg}{4}{k2}{4}` | +6.19, $p = 4.6\times10^{-11}$ |
| gain on BIRD dev over the highest round of FedAvg SFT (round 3) | `\gain{bird}{fedavg}{3}{k2}{4}` | +5.08 |
| EX on Spider test, \method and FedAvg SFT, 4 rounds | `\ex{spider}{k2}{4}`, `\ex{spider}{fedavg}{4}` | 78.20, 74.71 |
| gain on Spider test at 4 rounds | `\gain{spider}{fedavg}{4}{k2}{4}`, `\pval{spider}{fedavg}{4}{k2}{4}` | +3.49, $p = 6.4\times10^{-7}$ |
| execution errors on BIRD dev, FedAvg SFT and \method | `\nerr{bird}{fedavg}{4}`, `\nerr{bird}{k2}{4}` | 268, 128 of 1,534 predictions |
| execution errors on Spider test | `\nerr{spider}{fedavg}{4}`, `\nerr{spider}{k2}{4}` | 173, 84 of 2,147 predictions |
| per-client upload per round, either kind of round | `\setting{adapter.mb}` | 73.9 MB |

Facts on these numbers:

- Significance: exact McNemar test on paired predictions, Holm
  correction within each table; one training seed.
- FedAvg SFT by round on BIRD dev: 42.70, 43.68, 42.57 at rounds 2, 3,
  4; on Spider test 74.71 at rounds 3 and 4, 73.92 at round 5.
- The difference in execution errors is tested per prediction and is
  significant on both datasets.
- The setup: five clients, non-IID partition by database, all clients
  in every round.

### Fig. 1

- Label `fig:idea`; file `figures/fig_idea.pdf`; one question trained
  in two ways, as two panels over the same question, client database
  and gold SQL query.
- Left panel, FedAvg SFT: prompt (question and schema as text) to the
  model; the gold SQL query as the only target; the database not
  queried.
- Right panel, \method: $N$ samples of the model for the question;
  each executed on the client database; execution results compared
  with that of the gold SQL query; correct and incorrect samples;
  preference pairs.
- Both panels inside the client boundary; only the adapter crosses it.
- The caption is part of the section.

### Contributions

1. A source of supervision: client databases as supervision that
   federated fine-tuning does not exploit and that is accessible only at
   the client; to our knowledge the first federated training method
   for Text-to-SQL that uses it.
2. The framework \method: the four components; a federated round as
   one resampling step; the round's global model as reference model;
   a client transmits only the adapter and its aggregation weight.
3. The evidence: the gain over FedAvg SFT on BIRD dev and Spider test
   at the same number of rounds; where it originates (execution
   errors; correct predictions over other tables or columns than those
   of the gold SQL query); the role of each component; the client
   cost.
4. The release: code, client splits and the predictions of every row
   of the tables.

## References

| Key | Cited for |
|---|---|
| `yu2018spider`, `li2023bird` | the Text-to-SQL benchmarks |
| `gao2024dailsql`, `pourreza2023dinsql` | Text-to-SQL by prompting proprietary large language models |
| `li2024codes`, `sheng2025slmsql` | fine-tuned open models for Text-to-SQL; the SLM range of 0.5B to 1.5B parameters |
| `hui2024qwen25coder` | the principal model |
| `mcmahan2017fedavg` | federated averaging |
| `hu2022lora` | the LoRA adapter |
| `ye2024openfedllm` | federated SFT of language models with adapters; FedDPO |
| `zhang2023fl4sp` | the earlier study of federated semantic parsing, Text-to-SQL included; cited by its authors |
| `rafailov2023dpo` | the DPO loss |

## Labels available for cross-reference

`sec:related`, `sec:method`, `sec:supervision`, `sec:overview`,
`sec:setup`, `sec:results`, `sec:main`, `sec:analysis`, `sec:ablation`,
`sec:cost`, `sec:discussion`, `fig:overview`, `tab:main`.
