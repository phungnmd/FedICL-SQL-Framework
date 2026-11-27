# Checks: Section 1, Introduction, abstract, keywords

For the editor (main session and helpers). The writer does not read this
file. It holds what stays true whatever the draft says: facts and the
bounds of claims. Notes on the wording of a draft are not kept here
(`WRITING_PLAN.md`, section 7.0).

## 1. Facts about our work

- Cost, as GPU time and label time apart (owner, 2026-11-27; `CLAIMS.md`, E2). A single preference round does not always take more GPU time than an SFT round: the ratios are 1.8 and 1.3 on BIRD, 1.6 and 0.9 on Spider (`\fact{cost.spider.pref2.gpu_ratio}` prints 0.9). The label step is SQL executed on the CPU: 159 and 168 min on BIRD, 3 on Spider. No figure adds the two. True: no communication beyond that of FedAvg SFT; over the four rounds the method takes more GPU time on both datasets (BIRD 879 against 692 min, Spider 555 against 496).
- The headline number of the abstract is the gain on BIRD dev at equal rounds (6.19); the gain over the highest round of FedAvg SFT (5.08) is given in Section 1 and Section 5.1. (owner, 2026-11-27, A30)

## 2. Facts about cited papers

- Zhang et al. do not call their work FL4SP; the paper is cited by its authors. Their re-weighting is named Lorar.
- FedDPO (OpenFedLLM): "preference datasets for helpfulness and harmlessness". Not "human preferences": for UltraFeedback the paper says only "the response with the highest score" among four responses of LLMs.
- OpenFedLLM states that the reference model is "fixed throughout the FL process". It does not describe any step that constructs pairs again; "constructed once" is our reading of "each client holds a preference dataset".

## 3. Claims: strength, scope, what waits

- "First" holds with "to our knowledge" and in the scope of federated training of Text-to-SQL models (`CLAIMS.md`, rule 7).
- Execution errors fall by about half against FedAvg SFT at 4 rounds, tested and significant on both sets (BIRD dev p = 5.8e-22, Spider test p = 6.2e-14). The incorrect results are not fewer, and their difference is not significant after correction. The abstract may state the first without the second (owner, 2026-11-27, B35).
- An ablation result named in the Introduction names its set: fixed pairs and reference lower EX on BIRD dev (level on Spider test); without the NLL term a preference round brings no gain on Spider test (the BIRD row is not committed).
- The method is a contribution of its own in the list of four (owner, 2026-11-27, B40): supervision left unused; the framework; results, analysis, cost and ablation; release.
- Small language model (owner, 2026-11-27). The Introduction and the abstract name the model a small language model (SLM), with its size at first use, as the reason for the setting: an organization fine-tunes and serves it on its own hardware, and a client samples and executes queries with it. Three bounds. The method is not presented as specific to SLMs: no model above 1.5B parameters was run, and on the smallest model (0.5B) the gain on Spider test is smaller (+2.10 against +3.49 at 1.5B). No claim on deployment efficiency (latency, edge devices): nothing of the kind is measured. The paper is not positioned as an SLM Text-to-SQL system: its comparisons are inside one federated setup, not against the levels of centralized SLM systems, which use voting and more data (reviewer question C40).
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
