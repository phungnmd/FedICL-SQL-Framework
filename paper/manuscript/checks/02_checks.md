# Checks: Section 2, Related work, Table 1

What stays true whatever the draft says: facts and the bounds of claims.
It is read before the section is written and when it is checked; remarks
on the wording of a draft are not kept here.

## 1. Facts about our work

- Section 5.3 holds the pairs and the reference model fixed together, in one row; the DPO loss alone is a separate row. A sentence of Section 2 that points to Section 5.3 says "varies these choices", not "all three".
- The scale of the preference term, beta, is described in the same words here and in Section 3.

## 2. Facts about cited papers

Every cell of Table 1 and every sentence about a cited paper has its row and locator in `02_related_table1_rows.md` and `02_related_rows.md`. Where the lab's notes differ from the papers, the papers hold:

| Paper | The notes say | The paper says |
|---|---|---|
| Zhang et al. (FL4SP in the notes) | "full fine-tuning" | only "finetune T5-base"; neither full nor adapter, no model size printed. The paper never uses the name FL4SP. No preference stage: the cells on pairs are "not applicable" |
| OpenFedLLM | Llama2-7B int8, LoRA r=32 | that is the instruction-tuning setup; FedDPO uses Wizard-Vicuna-7B-Uncensored, LoRA rank 8, alpha 16 |
| OpenFedLLM | "every FL algorithm beats local training"; FedDPO is "DPO inside FedAvg" | on HH-RLHF, FedProx is below local training on harmlessness (Table 9); the FedDPO table also runs FedProx, SCAFFOLD, FedAvgM |
| OpenFedLLM | FedDPO "all on human preferences" | true for HH-RLHF; for UltraFeedback the paper does not say who scores |
| OpenFedLLM | pairs "constructed once" | "each client holds a preference dataset"; no step that constructs pairs again is described; the reference model is "fixed throughout the FL process". Table 1 keeps "no" for "pairs constructed anew" with this reason in the cell or a table note |
| ExCoT | "5.6k of the 9,428 BIRD train" | 9.2k. Only the on-policy rounds use the model's own outputs (the first DPO round and SFT use outputs of GPT-4o); the loss is not written as a formula |
| CodeLutra | "base model" | the checkpoint table gives Llama-3-8B-Instruct |
| CodeLutra | the gain over SFT | the text says "16.9% after four iterations"; its Table 1 gives 76.6 (iteration 3) against 67.9 for SFT, 8.7 points |
| Liu et al. | "SQL-only DPO lowers EX for 6 of 10 models" | true for greedy and Maj@16; with Pass@1 all 10 rise (Table 1). Pairs constructed once from the SFT model, 8 epochs of DPO, no NLL term |
| Lanchantin et al. | offline, semi-online, online | the paper also reports that an added NLL term did not help (Sec. 4.2) |
| Think2SQL | "GRPO with EX or partial rewards" | the best model uses a partial reward (weight 0.85) plus two format terms; arXiv v5 points to a newer TMLR paper under another title; our entry is the preprint |
| Arctic-Text2SQL-R1 | reward 1 and 0.1 | correct; its abstract says "solely execution correctness"; the final model starts from an OmniSQL checkpoint |
| SPFT-SQL | "verified synthesis plus self-play" | execution checks the model's output against the synthesized SQL; the paper does not say the synthesized SQL is executed before use; the self-play loss is of the SPIN kind, not DPO |
| KGRFL | "an RL-based fusion weights client models" | so the abstract; it does not state that the BART parser is the model trained federatedly |

The reference models of the three DPO papers of Table 1 are of three kinds: renewed each iteration, fixed, not stated.

The NLL term of CodeLutra: its Eq. (3) writes the log-likelihood of the whole response, and the paper does not say whether it is normalized by length; its code was not checked. The NLL term of Pang et al. is length-normalized, as ours is. A sentence on CodeLutra's term keeps to the formula.

SKT-SQL (`yi2025sktsql`) could not be read (the publisher blocks it; only an abstract of a preprint under another title).

SLM-SQL (`sheng2025slmsql`, arXiv 2507.22478v1) uses "small language models (SLMs) ranging from 0.5B to 1.5B parameters" for five models, three of which this paper also uses (Qwen2.5-Coder-0.5B-Instruct, DeepSeek-Coder-1.3B-Instruct, Qwen2.5-Coder-1.5B-Instruct). Its inference votes over 64 samples and its SFT uses 916K synthetic rows; our rows are greedy and train on the benchmark training sets.

## 3. Claims: strength, scope, what waits

- "To our knowledge" in Section 2.3: the approved scope is federated training of Text-to-SQL models (`CLAIMS.md`, rule 7). A wider wording, "no earlier method combines federated training with execution labels and renewed pairs of the model's own outputs", which the fact rows support for the works read (FedDPO: pairs from a dataset; Wu et al.: pairs generated once at the server; PubSwap, Fed-GRPO: a reward, no pairs), but our search covered federated fine-tuning of language models, not all federated work on code. Open with the owner (`REVIEW_NOTES.md`, A33).
- Liu et al.: their result may be reported with their decoding and model sizes, not explained (owner, A20).
- The comparison with CodeLutra is made in this section and nowhere else (owner, 2026-11-27): one paragraph in 2.2 and its row of Table 1, at full size: the same loop of sampling, execution labels and DPO with an NLL term, run centrally by one holder of the data; here the labels are computed at each client on databases the server never sees, a federated round is the re-sampling step, and the round's global model is the reference model of every client. What CodeLutra does with questions that yield no pair is not stated in its paper and is not written.

## 4. What the section carries for other sections

- Section 2 uses the abbreviations and the terms that Section 1 introduces; it expands none.
- The four published results on a likelihood term in DPO (end of this file) are for Section 2.2: all four or none; Section 5 quotes no number of another paper.

## 5. Labels, floats and formulas

Other sections and the generated tables refer to these labels. `make inventory` lists the macros and
citation keys by section.

### `sections/02_related.tex`

Headings and labels:

- `\section{Related work}` `sec:related`
- `\subsection{Fine-tuned open models for Text-to-SQL}` `sec:rel-slm`
- `\subsection{Preference optimization and execution feedback}` `sec:rel-pref`
- `\subsection{Federated fine-tuning of language models}` `sec:rel-fed`
- `\subsection{Federated semantic parsing and Text-to-SQL}` `sec:rel-fedsql`

Floats:

- table `tab:related`

## Published results on a likelihood term beside the DPO term (moved from the checks of Section 5)

Four published results on a likelihood term in DPO (locators in `02_related_rows.md`); two support the term and two do not; Section 2.2 carries all four or none:

- CodeLutra, Table 2: Spider 17.2 with the DPO term alone, 76.6 with the full loss.
- Pang et al., Table 1: GSM8K 61.8 against 73.1, one round.
- Liu et al., App. A, Table 7: an added SFT term on SQL-only output, 58.8 to 60.0, which they call a limited gain.
- Lanchantin et al., Sec. 4.2: an added NLL term did not help in their task. (Cited only here.)
