# Checks: Section 1, Introduction, abstract, keywords

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0).

## 1. Facts about our work

- Cost, as GPU time and label time apart (owner, 2026-11-27; `CLAIMS.md`, E2). A single preference round does not always take more GPU time than an SFT round: the ratios are 1.8 and 1.3 on BIRD, 1.6 and 0.9 on Spider (`\fact{cost.spider.pref2.gpu_ratio}` prints 0.9). The label step is SQL executed on the CPU: 159 and 168 min on BIRD, 3 on Spider. No figure adds the two. True: no communication beyond that of FedAvg SFT; over the four rounds the method takes more GPU time on both datasets (BIRD 879 against 692 min, Spider 555 against 496).
- The headline number of the abstract is the gain on BIRD dev at equal rounds (6.19); the gain over the highest round of FedAvg SFT (5.08) is given in Section 1 and Section 5.1. (owner, 2026-11-27, A30)
- Fig. 1 as drawn (paper commit 91f372f; example file `fedicl-sql/audits/protocol_v2/figure_examples/fedpref_bird_sftr2_p2_ddl_alpha01_s0_r1_dpo.json`, code 4ff3eb02): BIRD train question `train:5744` of client 5, database `language_corpus` ("How many Catalan-language Wikipedia pages are there overall?"), with its evidence line; the ten samples are those of the global model in the first preference round, after two warm-up rounds (temperature 1, 256 new tokens); 8 correct, 1 incorrect result, 1 execution error. The table prints the samples of the two pairs the round built: the two chosen samples are two different correct samples with the same SQL text (7 of the 8 correct samples share it), against the incorrect result and the execution error. The figure draws no server, adapter or aggregation.
- The earlier Fig. 1 (commit 29cac3d, `train:4462`, `student_loan`) printed pairs the run cannot have built; it was redrawn from the pairs of the round (commit 91f372f).
- FedAvg SFT, true on both datasets: the model generates no query during training, so no loss term is computed on a query of its own; neither the gold SQL query nor a model query is executed; no execution result enters the loss. "Without query execution" for the database as a whole is false on Spider (three rows per table read with a SELECT query, `fedls_sql/data/spider.py`). NLL on the gold query lowers the probability of every other continuation, so "no supervision penalizes incorrect queries" reads as overstated. (claim audit and cold read, 2026-11-28)
- Warm-up: questions of BIRD train whose ten samples are all incorrect, 4,035 of 9,428 under the pretrained model, 2,698 after two warm-up rounds (`\fact{warmup.bird.k0.no_correct}`, `\fact{warmup.bird.k2.no_correct}`). Not "correct samples across client questions".
- The p-values are exact McNemar tests on the paired predictions of one training run, Holm-adjusted within each table (`CLAIMS.md`, wording 2).

## 2. Facts about cited papers

- Zhang et al. do not call their work FL4SP; the paper is cited by its authors. Their re-weighting is named Lorar.
- FedDPO (OpenFedLLM): "preference datasets for helpfulness and harmlessness". Not "human preferences": for UltraFeedback the paper says only "the response with the highest score" among four responses of LLMs.
- OpenFedLLM states that the reference model is "fixed throughout the FL process". It does not describe any step that constructs pairs again; "constructed once" is our reading of "each client holds a preference dataset".
- FedDPO (OpenFedLLM) has no Text-to-SQL task and executes nothing; "SQL" does not occur in the paper. Among federated training approaches for Text-to-SQL the record holds Zhang et al. (federated SFT) only. (claim audit, 2026-11-28)
- Zhang et al. do not name the form of their local loss; no row gives it for OpenFedLLM. The token-averaged NLL is this paper's Eq. (1).
- DIN-SQL and DAIL-SQL prompt GPT-4 and reported the best Spider results when published (85.3 and 86.6 on Spider test). Open fine-tuned models have reported higher since (Arctic-Text2SQL-R1 7B 88.8 on Spider test, `bib/report.md`; CodeS claims new state of the art on most benchmarks). "The highest-accuracy systems rely on prompting proprietary LLMs" in the present tense is not supported.
- CodeS states the privacy motive and local deployment. SLM-SQL states the 0.5B to 1.5B range, inference speed and suitability for edge deployment; nothing on privacy or schemas.

## 3. Claims: strength, scope, what waits

- "First" holds with "to our knowledge" and in the scope of federated training of Text-to-SQL models (`CLAIMS.md`, rule 7).
- Execution errors fall by about half against FedAvg SFT at 4 rounds, tested and significant on both sets (BIRD dev p = 5.8e-22, Spider test p = 6.2e-14). The incorrect results are not fewer, and their difference is not significant after correction. The abstract may state the first without the second (owner, 2026-11-27, B35).
- An ablation result named in the Introduction names its set: fixed pairs and reference lower EX on BIRD dev (level on Spider test); without the NLL term a preference round brings no gain on Spider test (the BIRD row is not committed).
- The method is a contribution of its own in the list of four (owner, 2026-11-27, B40): supervision left unused; the framework; results, analysis, cost and ablation; release.
- Small language model (owner, 2026-11-27). The Introduction and the abstract name the model a small language model (SLM), with its size at first use, as the reason for the setting: an organization fine-tunes and serves it on its own hardware, and a client samples and executes queries with it. Three bounds. The method is not presented as specific to SLMs: no model above 1.5B parameters was run, and on the smallest model (0.5B) the gain on Spider test is smaller (+2.10 against +3.49 at 1.5B). No claim on deployment efficiency (latency, edge devices): nothing of the kind is measured. The paper is not positioned as an SLM Text-to-SQL system: its comparisons are inside one federated setup, not against the levels of centralized SLM systems, which use voting and more data (reviewer question C40).
- A cause shared by the two limitations is not in the record. The fixed pairs, fixed reference and DPO-only loss of FedDPO are choices of its design, and centralized SFT has no execution term either. Supported: the labels need the database, and in the federated setting only the client holds it, so supervision from execution can be produced only at the client (`CLAIMS.md`, contribution 1). (claim audit and cold read, 2026-11-28)
- One preference-optimization iteration and one renewal of the reference model per communication round holds for the preference rounds; warm-up rounds are FedAvg SFT rounds.
- C3 in the Introduction: the answers on other tables or columns are a large part of the net gain on BIRD (55 of 95 questions under EX, 46 of 75 under the suite), not on Spider (20 of 75); where their EX count on BIRD is given, the suite count goes beside it. The suite rejects 30.9% of the method's correct answers on other tables or columns; of all its predictions correct under EX it rejects 110 of 748 (C4).
- The "fixed pairs and reference" row keeps the NLL term; it is not FedDPO as published, and its effect is stated for BIRD (B1).
- Position (owner, 2026-11-27). The limitation, the insight and the contributions are stated against federated SFT and federated DPO as published: a client holds databases that federated fine-tuning leaves unused. The Introduction makes no comparison with CodeLutra; it may cite it in a sentence on centralized preference optimization with execution feedback. Section 2.2 carries the comparison.

## 4. What the section carries for other sections

- SFT, FedAvg, DPO, NLL, LoRA and EX in full at first use; Spider and BIRD cited at first mention; "execution label", "global model", "warm-up round", "preference round", "NLL term", "reference model" each understandable where first used. (v1 E)
- Why several organizations train one model together.
- "Federated Text-to-SQL" means federated training of the model, said once.
- "non-IID" is not introduced here; its expansion belongs to Section 4.2.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. The macros and
citation keys by section are in `inventory.txt`.

### `sections/01_intro.tex`

Headings and labels:

- `\section{Introduction}` `sec:intro`
