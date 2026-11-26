# Audit of the cited work in Section 2 (Related work) and Table 1

Draft checked: `sections/02_related.tex` (as on 2026-11-27). Each statement was
checked against the paper's text in the scratchpad `papers/` and `papers2/`
folders (arXiv ids as file names), not only against the brief. Line numbers are
those of the draft. `xu2024kgrfl` was checked against its abstract (OpenAlex
record, `papers2/kg_oa.json`); `mcmahan2017fedavg` and `hu2022lora` have no text
here.

## Statements

| # | Statement in the draft (line) | Row of the brief | Paper and locator checked | Verdict | Note |
|---|---|---|---|---|---|
| 1 | Open models fine-tuned for Text-to-SQL are an established line; methods differ in what the model is trained on (5-6) | 2.1, statement 1 | rows 2 to 6 below | SUPPORTED | framing sentence |
| 2 | CodeS pre-trains models of 1B to 15B further on a SQL-centric corpus and fine-tunes them on the training set of each benchmark (7-9) | `li2024codes`: "1B, 3B, 7B and 15B"; "pre-trained further on a SQL-centric corpus of 21.5 GB, then fully fine-tuned on the training set of each benchmark" | 2402.16347: abstract "ranging from 1B to 15B"; Sec. 1 "By incrementally pre-training StarCoder ... on this corpus"; Sec. 9.1.3 "we fully fine-tune it using the training set" | SUPPORTED | |
| 3 | OmniSQL relies on synthetic data at scale, fine-tuning models of 7B to 32B on SynSQL-2.5M and the training sets of Spider and BIRD (9-11) | `li2025omnisql`: "OmniSQL at 7B, 14B and 32B ... fine-tuned on SynSQL-2.5M together with the training sets of Spider and BIRD" | 2503.02240: Sec. 5 "Using our synthetic dataset, SynSQL-2.5M, along with two widely-adopted datasets, Spider and BIRD, we present OmniSQL ... 7B, 14B, and 32B" | SUPPORTED | 32B is trained with LoRA, 7B and 14B fully; "fine-tuning" covers both |
| 4 | SPFT-SQL synthesizes its data from the training databases and fine-tunes by self-play (11-13) | `zhang2025spftsql`: "synthesizes SQL queries from templates filled with tables, columns and values of the training databases ... then fine-tunes by self-play" | 2509.03937: Sec. 3.1.1 "To generate new SQL queries based on training data schemas ... values ... are retrieved and randomly filled from the database"; Sec. 3.2, Alg. 1 | SUPPORTED | |
| 5 | SLM-SQL, Think2SQL and Arctic-Text2SQL-R1 train the model by RL with an execution-based reward (13-16) | `sheng2025slmsql`, `papicchio2025think2sql`, `yao2026arctic` rows | 2507.22478 Sec. 2, App. C (GRPO, R_EX + 0.1 R_Format); 2504.15077 Sec. 2.3, 3.1 (GRPO, reward "computed via SQL execution"); 2505.20315 Sec. 3 (GRPO; 1 / 0.1 / 0) | SUPPORTED | The brief has "SFT followed by RL"; the draft drops the SFT stage. True of the RL part in all three; SLM-SQL's 916K-sample SFT stage and Arctic's start from OmniSQL go unmentioned, which no reader would call wrong |
| 6 | ... the first of them for models of 0.5B to 1.5B (16-17) | `sheng2025slmsql`: "five models of 0.5B to 1.5B" | 2507.22478 abstract "ranging from 0.5B to 1.5B parameters"; Sec. 3.1 | SUPPORTED | |
| 7 | All of these methods assume training at one site, which holds the questions, the SQL queries and the databases together (19-20) | 2.1, statement 2: "every one trains on a pooled training set" | the six papers: none contains "federat" (grep of full text: 0 hits each); all train on pooled Spider/BIRD or synthetic sets and execute or read the databases at the trainer | SUPPORTED | "assume" is our reading; none of the six states it, none contradicts it |
| 8 | Data privacy, one of the motives of CodeS: a closed-source model behind an API requires that an organization send its data to the provider (20-23) | `li2024codes`: "a closed-source model called through an API puts data privacy at risk, since the data must be sent to the provider" | 2402.16347 Sec. 1: "(L2) Invoking these models via APIs risks data privacy, as data must be sent to model providers." | SUPPORTED | |
| 9 | DPO trains a language model on pairs of a preferred and a dispreferred output, against a reference model (29-30) | `rafailov2023dpo` rows | 2305.18290 Sec. 1; Sec. 4, Eq. (7) with pi_ref | SUPPORTED | |
| 10 | For SQL the preference requires no annotator: sampled queries are executed and compared with the result of the gold query (30-33) | 2.2, statement 2 | 2502.11656 Sec. 1; 2503.19988 Sec. 3.3; 2411.05199 Sec. 5.1 | SUPPORTED | uncited general sentence, true of the three SQL papers that follow |
| 11 | Liu et al. train ten Text-to-SQL models of 6.7B to 15B with DPO on such pairs (33-35) | `liu2025cotdpo`: "ten models of 6.7B to 15B parameters"; pairs labeled by execution | 2502.11656 Sec. 1: "we evaluate 10 open-source LLMs, ranging from 6.7B to 15B parameters"; "Correct and incorrect queries are identified through database execution to create preference pairs" | SUPPORTED | The ten are general and code LLMs (and CodeS) fine-tuned for Text-to-SQL; "ten Text-to-SQL models" reads as models trained for the task, which is what the paper does |
| 12 | ... EX on BIRD dev, greedy, rises after DPO for all ten with CoT before the query and falls for six with the query alone (35-37) | `liu2025cotdpo`: finding, BIRD dev, greedy, 6 of 10 fall, all 10 rise with CoT | 2502.11656 Table 1, Greedy columns: Vanilla falls for Deepseek-llm-7b-chat (-0.6), Qwen2.5-14B (-0.8), CodeLlama-7b (-1.3), Qwen2.5-Coder-7B (-0.3), CodeS-7B (-0.2), CodeS-15B (-0.1); Syn CoT rises for all ten (+0.3 to +4.5) | SUPPORTED | numbers 10 and 6 check |
| 13 | Liu et al. construct the pairs once, from samples of a model trained with SFT (39-41) | `liu2025cotdpo`: "the pairs are constructed once ... SFT model as the reference" | 2502.11656 Sec. 1 steps (1) to (3): "Using the SFT model, multiple SQL queries are sampled"; App. D | SUPPORTED | |
| 14 | ExCoT, also for Text-to-SQL, takes the pairs first from outputs of GPT-4o and then from outputs of the model in training (41-42) | `zhai2025excot`: "one DPO round on pairs of GPT-4o outputs, then two rounds on pairs of outputs of the model in training" | 2503.19988 Sec. 3.4, Sec. 4.1: "We conduct 1 round of off-policy DPO, followed by 2 rounds of on-policy DPO"; "the model under training itself generates new solutions" | SUPPORTED | |
| 15 | Pang et al. construct new pairs in every iteration, labeled by the correctness of the final answer, and train with a DPO and an NLL term (43-45) | `pang2024irpo`: "each iteration samples ... pairs one whose final answer is correct with one whose final answer is wrong, and trains with a DPO term plus an NLL term" | 2404.19733 Sec. 1 "On each iteration we sample multiple chain-of-thought reasoning steps and final answers ..."; Sec. 2, Eq. (1) L_DPO+NLL | SUPPORTED | On GSM8K the gold solution is also added to the winners (Sec. 3.1); does not change the sentence |
| 16 | On mathematical tasks, Lanchantin et al. report that models trained with DPO on responses generated during training surpass the model trained on responses generated once (45-48) | `lanchantin2025bridging`: semi-online and online above offline on math | 2506.21495 Table 1: offline 53.7 / 36.4 / 28.8 (Math500, NuminaMath, AMC23), every semi-online and online DPO row above on all three; Sec. 4.1 "online and semi-online trained models (s >= 1) all outperform the offline DPO model" | SUPPORTED | |
| 17 | CodeLutra trains a Text-to-SQL model at one site and renews pairs every iteration: samples from the current model, labels by comparison of execution results with the gold query, pairs a correct with a failed sample, trains with a DPO term and a likelihood term on the correct samples (50-55) | `tao2024codelutra` rows | 2411.05199 Sec. 4 "We are provided with an initial training set D"; "At each iteration t, the model pi_t generates M code responses"; "pairing one correct code ... with one rejected code"; Eq. (3) "maximize likelihood for correct codes"; Sec. 5.1 "we execute the generated SQL queries ... and directly compare execution results" | SUPPORTED | CodeLutra is a code-generation framework (SQL and data-science Python); "a Text-to-SQL model" describes its data-query runs, and Table 1 is consistent |
| 18 | \method{} follows CodeLutra in its sampling and loss settings (Section 3.4) (55-56) | 2.2, statement 4: "may be said in a clause" | `sections/03_method.tex` Sec. 3.4: "We follow CodeLutra in N, the temperature, beta, the uniform pairing and the choice of reference model. We construct fewer pairs per question ... and average the NLL term over tokens, where CodeLutra sums it" | IMPRECISE | Section 3.4 names two departures, one in sampling (pairs per question) and one in the loss (NLL averaged, so the same lambda weighs it less). A reader who goes to Section 3.4 finds that the loss is not set as CodeLutra sets it |
| 19 | Execution labels train selectors at inference, a verifier in LEVER and an ORM in GradeSQL, without training the generator (58-61) | `ni2023lever`, `tritto2026gradesql` rows | 2302.08468 abstract, Sec. 2.3 (labels from comparing with "the gold execution result"), few-shot generators; 2509.01308 Sec. III.B "labeled as correct if its result set matches that of the gold query", Sec. IV "we adopt OmniSQL-7B as the generator" | SUPPORTED | LEVER's candidates are also Python programs (GSM8K, MBPP); "candidate queries" fits its Spider and WikiTQ runs |
| 20 | In all works of this subsection, the party that trains holds the questions and the databases (61-62) | 2.2, statement 6: "the party that trains holds the questions and the databases" | DPO 2305.18290 (IMDb, TL;DR, Anthropic HH); Pang 2404.19733 (GSM8K, MATH, ARC); Lanchantin 2506.21495 (NuminaMath, WildChat); LEVER 2302.08468 (GSM8K, MBPP besides Spider, WikiTQ) | IMPRECISE | Holds for Liu et al., ExCoT, CodeLutra, GradeSQL and LEVER on Spider. DPO, Pang et al. and Lanchantin et al. involve no database at all, and DPO's data are not questions (sentiment prompts, posts to summarize, dialogues). "All works of this subsection" covers them |
| 21 | Language models are fine-tuned across clients with FedAvg and LoRA: clients train adapters with SFT, the server averages them (68-71) | 2.3, statement 1; `mcmahan2017fedavg`, `hu2022lora` named as sources | 2402.06954 Sec. 3.1 (FedAvg framework, LoRA); 2309.00363 abstract (federated PEFT) | SUPPORTED | |
| 22 | FederatedScope-LLM provides a package and a benchmark for such fine-tuning (71-72) | `kuang2024fsllm`: "a package ... with parameter-efficient methods ... with a benchmark" | 2309.00363 abstract | SUPPORTED | |
| 23 | OpenFedLLM a framework for federated instruction tuning and value alignment (72-74) | `ye2024openfedllm`: "a framework for federated instruction tuning and federated value alignment" | 2402.06954 abstract (line 29), Sec. 3.1 | SUPPORTED | |
| 24 | ... both include code generation among their tasks (74-75) | `kuang2024fsllm`: code generation, nine clients; `ye2024openfedllm`: "code generation is one of its domains" | 2309.00363 Sec. 3.1 Fed-CodeAlpaca; 2402.06954 Sec. 4.5 CodeAlpaca | SUPPORTED | |
| 25 | DPO has also been applied in federated training, on preferences that the clients already hold (77-78) | 2.3, statement 2 | 2402.06954 Sec. 3.3; 2407.03038 Sec. 4, App. A.2: "The reinforcement-learning fine-tuning takes place on the server" | IMPRECISE | True of FedDPO. The sentence also opens the paragraph on Wu et al., where DPO is not run in federated training and not on the clients' preferences: the server trains the model centrally on pairs it generated and that the aggregated selector labeled (row 29 says so correctly) |
| 26 | FedDPO of OpenFedLLM is one of our baselines (Section 4.4) (78-80) | 2.3, statement 2; Section 4.4 | `sections/04_setup.tex` lines 135-139 | SUPPORTED | Section 4.4 adapts FedDPO: its pairs are the model's own samples from the first preference round. Placed in the same sentence as "for helpfulness or harmlessness", the clause may lead a reader to expect those datasets in our baseline; Section 4.4 clears it up |
| 27 | In FedDPO each client holds a preference dataset, for helpfulness or harmlessness; the loss is the DPO loss alone; the reference model is fixed for the whole process (80-82) | `ye2024openfedllm`: FedDPO row and its two datasets | 2402.06954 Sec. 3.3: "In FedDPO, each client holds a preference dataset"; Eq. (2); "fixed throughout the FL process"; Secs. 4.7, 4.8 (UltraFeedback, HH-RLHF) | SUPPORTED | |
| 28 | Its pairs come with the dataset: they are not outputs of the model being trained and do not follow it over the rounds (82-84) | `ye2024openfedllm`: "the paper describes no step that generates or relabels responses during the rounds"; brief ceiling: "responses that come with the dataset" | 2402.06954 Sec. 4.7 "four corresponding responses of different LLMs"; Sec. 4.8 HH-RLHF | SUPPORTED | "do not follow it" rests on the absence of any regeneration step; the paper does not state it in words, but no step it describes would make it otherwise |
| 29 | Wu et al. keep human preference data at the clients, which train preference selectors, and train the LM at the server with DPO (84-86) | `wu2025fedbiscuit` rows | 2407.03038 Sec. 4 "each client independently trains a binary selector"; App. A.2, Eq. (9); Sec. 6 (TL;DR comparisons, SHP) | SUPPORTED | |
| 30 | PubSwap and Fed-GRPO apply RL at the clients with a reward for a correct answer, in mathematics, medical QA and code generation (88-91) | `nayak2026pubswap`, `guo2026fedgrpo` rows | 2604.12160 Sec. 1 "each client performs local GRPO steps", Sec. 4.1 (math, medical); 2610.11502 Sec. 6.1 "binary correctness reward", MBPP and HumanEval | SUPPORTED | medical is PubSwap only, code is Fed-GRPO only; the joint list reads correctly |
| 31 | None of the works discussed in this subsection considers Text-to-SQL (92-94) | `the five papers of this subsection`: "none of them has a Text-to-SQL task" | grep "SQL" in 2309.00363, 2402.06954, 2407.03038, 2604.12160, 2610.11502: 0 hits each. `hu2022lora` and `mcmahan2017fedavg` are also discussed in this subsection; no text here | IMPRECISE | The brief's row covers five papers; the draft's "works discussed in this subsection" also covers FedAvg and LoRA. LoRA (Hu et al.) evaluates GPT-3 175B on WikiSQL, a Text-to-SQL task (its GPT-3 experiments, WikiSQL accuracy beside MNLI and SAMSum). This comes from my knowledge of the LoRA paper; its text was not available to check |
| 32 | Federated learning for Text-to-SQL was studied earlier by Zhang et al. (98-99) | `zhang2023fl4sp`: "each client is one single-domain Text-to-SQL dataset" | 2305.17221 abstract: "we re-purpose widely-used single-domain text-to-SQL datasets as clients" | SUPPORTED | |
| 33 | A related work applies FL to a semantic parser for knowledge-graph questions (99-100) | `xu2024kgrfl`: "multitask BART model that ... converts it into a SPARQL query ... for joint modelling by several institutions" | abstract (`papers2/kg_oa.json`): "knowledge graph-based reinforcement federated learning (KGRFL)-based Q&A approach ... multitask semantic parsing model ... converting questions into SPARQL statements" | SUPPORTED | abstract only; it does not say in so many words that MSP-BART is the federated model, but the sentence reads it as the abstract presents it |
| 34 | The clients of Zhang et al. are eight single-domain datasets; a T5-base model is trained with supervision on the gold SQL of each client (100-102) | `zhang2023fl4sp`: eight clients; T5-base, supervised on gold SQL | 2305.17221 Sec. 5 "we leverage eight clients and a server"; Sec. 1 "we adopt T5-base as our backbone"; App. A, Alg. 1 | SUPPORTED | |
| 35 | In EM averaged over the clients, FedAvg 40.03 against 70.32 centralized; Lorar raises it to 60.16 (102-104) | `zhang2023fl4sp`: Table 2 MacroAvg 70.32, 40.03, 60.16 | 2305.17221 Table 2, MacroAvg column: Centralized 70.32, FedAvg 40.03, FedAvg_lorar 60.16; MacroAvg = arithmetic mean over clients (Sec. 5) | SUPPORTED | numbers check |
| 36 | Nothing is executed in Zhang et al.: gold SQL is the only supervision; a prediction is correct only when it is the same string as the gold SQL (104-106) | `zhang2023fl4sp`: "nothing is executed ... exact match" | 2305.17221 Sec. 5 "Exact Match (EM): a prediction is deemed correct only if it is exactly the same as the ground truth (i.e., exact string match)"; "execut" occurs only as "Server executes:" / "Client executes:" in Alg. 1 | SUPPORTED | |
| 37 | To our knowledge, Zhang et al. is the only earlier work that trains a Text-to-SQL model with FL, and no earlier method does so with execution labels and renewed own-output pairs (130-134) | 2.4, statement 4 | Table 1 rows; rows 32 to 36 | SUPPORTED | a claim about the literature under "to our knowledge"; nothing in the cited papers contradicts it (Xu et al. is SPARQL) |

## Table 1

| # | Cell | Row of the brief | Paper and locator checked | Verdict | Note |
|---|---|---|---|---|---|
| T1 | Zhang et al., Federated: yes | Table 1, Zhang: "federated" | 2305.17221 Sec. 5 "eight clients and a server" | SUPPORTED | |
| T2 | Zhang et al., Text-to-SQL: yes | "Text-to-SQL" | 2305.17221 abstract | SUPPORTED | |
| T3 | Zhang et al., Labels from execution: no | "nothing executed" | 2305.17221 Sec. 5, EM | SUPPORTED | |
| T4 | Zhang et al., Pairs renewed: dash | "no pairs" | 2305.17221 Alg. 1, line 18 "for each batch b = {x, y} of Di" | SUPPORTED | the dash with the caption's note is the right entry (not applicable, not "no") |
| T5 | FedDPO, Federated: yes | FedDPO: "federated" | 2402.06954 Sec. 3.3, Sec. 4.7 (5 clients, 2 per round) | SUPPORTED | |
| T6 | FedDPO, Text-to-SQL: no | "preference datasets for helpfulness and harmlessness" | 2402.06954 Secs. 4.7, 4.8; "SQL" 0 hits | SUPPORTED | |
| T7 | FedDPO, Labels from execution: no | "preference from the dataset" | 2402.06954 Sec. 4.7 "the response with the highest score as the preferred response" | SUPPORTED | |
| T8 | FedDPO, Pairs of own outputs renewed: no | "responses stored in the dataset; no step that constructs pairs" | 2402.06954 Sec. 4.7 "responses of different LLMs" | SUPPORTED | |
| T9 | ExCoT, Federated: no | ExCoT: "one site" | 2503.19988 Sec. 4.1 "64 NVIDIA H100 GPUs"; no mention of FL | SUPPORTED | |
| T10 | ExCoT, Text-to-SQL: yes | "Text-to-SQL" | 2503.19988 Table 1 caption | SUPPORTED | |
| T11 | ExCoT, Labels from execution: yes | "labels from execution against the gold result" | 2503.19988 Sec. 3.3 "compare the query's execution result to the ground-truth query result" | SUPPORTED | |
| T12 | ExCoT, Pairs renewed: yes, with note a | "first round GPT-4o outputs, later rounds the model's own" | 2503.19988 Sec. 3.4, Sec. 4.1 | SUPPORTED | |
| T13 | CodeLutra, Federated: no | CodeLutra: "one site" | 2411.05199 Sec. 4 "an initial training set D" | SUPPORTED | |
| T14 | CodeLutra, Text-to-SQL: yes | "Text-to-SQL and data-science code" | 2411.05199 Sec. 5.1 "Spider ... and BIRD ... and a data science dataset, DS-1000" | SUPPORTED | |
| T15 | CodeLutra, Labels from execution: yes | "against the reference result" | 2411.05199 Sec. 5.1 | SUPPORTED | |
| T16 | CodeLutra, Pairs renewed: yes | "pairs of the current model's samples; every iteration" | 2411.05199 Sec. 4; Sec. 5.1 "four iterations" | SUPPORTED | |
| T17 | \method{}, Federated: yes | \method{}: Secs. 3.1, 3.4 | `03_method.tex` Sec. 3.1, lines 34-37 | SUPPORTED | |
| T18 | \method{}, Text-to-SQL: yes | same | `03_method.tex` Sec. 3.1 | SUPPORTED | |
| T19 | \method{}, Labels from execution: yes | same | `03_method.tex` lines 152-162 | SUPPORTED | |
| T20 | \method{}, Pairs renewed: yes | same | `03_method.tex` "sampling, labeling and pair construction are repeated in every preference round" | SUPPORTED | |
| C1 | Caption: last column = trains on pairs of own outputs constructed anew; dash = supervised training, no pairs | Table 1 layout | as T4, T8, T12, T16, T20 | SUPPORTED | |
| C2 | Note a: after a first DPO round on pairs of GPT-4o outputs | ExCoT: "first round: outputs of GPT-4o" | 2503.19988 Sec. 3.4 "We first train the model using off-policy preference pairs derived from GPT-4o's outputs" | SUPPORTED | |

## Numbers and model sizes

All typed numbers and sizes check against the papers: 1B to 15B (CodeS), 7B to
32B (OmniSQL), 0.5B to 1.5B (SLM-SQL), ten models of 6.7B to 15B and six falls
(Liu et al., Table 1, greedy), eight clients, T5-base, 40.03, 70.32, 60.16
(Zhang et al., Table 2, MacroAvg).

## Citation keys

Every key sits on the statement about its own paper; the bibliography's arXiv
ids match the files checked (`li2024codes` 2402.16347, `li2025omnisql`
2503.02240, `zhang2025spftsql` 2509.03937, `sheng2025slmsql` 2507.22478,
`papicchio2025think2sql` 2504.15077, `yao2026arctic` 2505.20315,
`rafailov2023dpo` 2305.18290, `liu2025cotdpo` 2502.11656, `zhai2025excot`
2503.19988, `pang2024irpo` 2404.19733, `lanchantin2025bridging` 2506.21495,
`tao2024codelutra` 2411.05199, `ni2023lever` 2302.08468, `tritto2026gradesql`
2509.01308, `kuang2024fsllm` 2309.00363, `ye2024openfedllm` 2402.06954,
`wu2025fedbiscuit` 2407.03038, `nayak2026pubswap` 2604.12160,
`guo2026fedgrpo` 2610.11502, `zhang2023fl4sp` 2305.17221). No statement is
attributed to the wrong key.

## Not SUPPORTED, most serious first

1. **#31, line 92-94, "None of the works discussed in this subsection considers
   Text-to-SQL" (IMPRECISE).** The subsection also discusses LoRA
   (`hu2022lora`), whose GPT-3 experiments include WikiSQL, a Text-to-SQL task.
   The brief's row covers only the five federated papers. Scoping the sentence
   to the federated works would make it true. (The LoRA point is from
   knowledge of that paper; its text was not here to check.)
2. **#20, lines 61-62, "In all works of this subsection, the party that trains
   holds the questions and the databases" (IMPRECISE).** DPO, Pang et al. and
   Lanchantin et al. use no database (sentiment, summarization, dialogue,
   GSM8K, MATH, ARC, NuminaMath), and DPO's data are not questions. The
   sentence holds for the SQL works (Liu et al., ExCoT, CodeLutra, GradeSQL,
   LEVER on Spider).
3. **#25, lines 77-78, "DPO has also been applied in federated training, on
   preferences that the clients already hold" (IMPRECISE).** True of FedDPO.
   For Wu et al., which the same paragraph covers, DPO runs centrally at the
   server, on pairs the server generated and the aggregated selector labeled
   (2407.03038, App. A.2: "The reinforcement-learning fine-tuning takes place
   on the server"). The draft's own sentence on Wu et al. (lines 84-86) is
   correct.
4. **#18, lines 55-56, "\method{} follows it in its sampling and loss
   settings" (IMPRECISE).** Section 3.4 follows CodeLutra in N, temperature,
   beta, uniform pairing and reference model, but departs in the number of
   pairs per question and in the NLL term (averaged over tokens, so the same
   lambda weighs it less). The clause is within the brief's ceiling. A reader
   who checks Section 3.4 will still find that the loss is not set as
   CodeLutra sets it.

No statement is NOT SUPPORTED or NO ROW. Minor remark that needs no change:
#26 puts "one of our baselines" next to "for helpfulness or harmlessness",
while our FedDPO baseline trains on the model's own first-round pairs (Section
4.4). Section 4.4 makes this clear.
