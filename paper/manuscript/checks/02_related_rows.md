# Related work: fact sheet for twenty-one papers

Source for the rows and sentences of Section 2 beyond Table 1 (the four
papers of Table 1 are in `02_related_table1_rows.md`). Each cell records
what the paper itself writes. Page numbers are those of the PDF named in
the "Version read" line. A cell may carry two quotations, numbered (1) and
(2), each with its own locator. "Not stated" means the property is not
written anywhere in the sections listed in that cell. Each paper has one
extra row, "Models", with the model names and sizes as the paper gives
them.

## A. Li et al. 2024, CodeS (`li2024codes`)

Version read: arXiv 2402.16347v1 (only version; arXiv comment "Accepted to SIGMOD 2024"), PDF, https://arxiv.org/abs/2402.16347v1, read on 2026-11-26: abstract, Secs. 1, 4, 5, 9.1 to 9.3 and p. 13 read; the rest searched by keyword. The SIGMOD copy (ACM) was not opened.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Open-source models for Text-to-SQL in several sizes (1B, 3B, 7B, 15B) | Yes. Four sizes: 1B, 3B, 7B, 15B. | (1) "we introduce CodeS, a series of pre-trained language models with parameters ranging from 1B to 15B, specifically designed for the text-to-SQL task." (2) "which is available in 4 scales: 1B, 3B, 7B, and 15B." | (1) Abstract, p. 1. (2) Sec. 4 (Overview), p. 4. |
| 2. Built from StarCoder / StarCoderBase by incremental pre-training on a SQL-centric corpus, then SFT on a benchmark training set | Yes, with the split by size: CodeS-15B from StarCoder-15B, CodeS-1B/3B/7B from StarCoderBase-1B/3B/7B. Corpus 21.5 GB: 11 GB SQL-related, 6 GB NL-to-code, 4.5 GB NL-related; two epochs on the SQL part, one on each of the others. SFT is full fine-tuning on the training set of each benchmark (Spider, BIRD), 4 epochs, batch 128, lr 5e-6. | (1) "Specifically, CodeS-15B is based on StarCoder-15B, while CodeS-(1B, 3B, 7B) are derived from the respective StarCoderBase-(1B, 3B, 7B)." (2) "we fully fine-tune it using the training set and evaluate the fine-tuned version on different dev and test sets." | (1) Sec. 5.2, p. 6; corpus: Sec. 1, p. 2. (2) Sec. 9.1.3, p. 10; SFT settings: Sec. 9.1.4, p. 10. |
| 3. Motive with respect to closed-source models | Three limitations of closed-source LLMs: hidden architecture and training details (L1), data privacy when calling APIs (L2), and inference overhead reflected in API cost (L3). Also deployment on local machines (GPU memory 10, 13, 20, 35 GB for 1B to 15B in float16). | "(L2) Invoking these models via APIs risks data privacy, as data must be sent to model providers." | Sec. 1, pp. 1 to 2; abstract, p. 1; deployment: p. 13 (efficiency paragraph of Sec. 9). |
| Models | CodeS-1B, 3B, 7B, 15B (from StarCoderBase-1B/3B/7B and StarCoder-15B); "SFT CodeS" for the fine-tuned versions. GPT-3.5 is used for data augmentation. | "By incrementally pre-training StarCoder [39] on this corpus, we created a series of CodeS models, with varying parameters ranging from 1B to 15B." | Sec. 1, p. 2; Sec. 5.2, p. 6. |

## B. Li et al. 2025, OmniSQL (`li2025omnisql`)

Version read: arXiv 2503.02240v2 (13 Jul 2025, PVLDB 18(11) header), PDF, https://arxiv.org/abs/2503.02240v2, read on 2026-11-26: abstract, Secs. 1, 5, 6.1.3 and the results text of Sec. 6 read; Sec. 3 searched by keyword.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. SynSQL-2.5M: number of samples and databases | 2,544,390 samples over 16,583 synthetic databases; each sample is a quadruple (database, question, SQL, chain-of-thought solution). The abstract rounds this to "2.5 million samples spanning over 16,000 synthetic databases". | "SynSQL-2.5M contains 2,544,390 text-to-SQL data samples, each represented as a quadruple of <database, question, SQL query, CoT solution>, spanning 16,583 distinct synthetic databases." | Sec. 1, "Validation", p. 2; abstract, p. 1. |
| 2. OmniSQL: base models, sizes, training data | OmniSQL-7B/14B/32B on Qwen2.5-Coder-7B/14B/32B-Instruct. Trained on SynSQL-2.5M together with the Spider and BIRD training sets, whose gold SQL is given synthesized CoT solutions. 7B and 14B fully fine-tuned; 32B with LoRA (r = 256, alpha = 512); LoRA versions of 7B and 14B also released. 2 epochs, batch 512. | (1) "Using our synthetic dataset, SynSQL-2.5M, along with two widely-adopted datasets, Spider and BIRD, we present OmniSQL" (2) "OmniSQL-7B/14B/32B is built on the Qwen2.5-Coder-7B/14B/32B-Instruct models" | (1) Sec. 5, p. 8; CoT for Spider and BIRD: Sec. 5.1, p. 9. (2) Sec. 6.1.3, p. 9; full vs LoRA: same paragraph. |
| Models | OmniSQL-7B, 14B, 32B; bases Qwen2.5-Coder-7B/14B/32B-Instruct. Data synthesis uses open models: Meta-Llama-3.1-8B/70B-Instruct, DeepSeek-Coder-6.7B/33B-Instruct, DeepSeek-Coder-V2-Lite-Instruct, Qwen2.5-7B/14B/32B/72B-Instruct, Qwen2.5-Coder-7B/14B/32B-Instruct. | "we develop OmniSQL, a powerful open-source text-to-SQL model available in three sizes: 7B, 14B, and 32B." | Abstract, p. 1; synthesis models: Sec. 3, p. 6. |

## C. Sheng and Xu 2025, SLM-SQL (`sheng2025slmsql`)

Version read: arXiv 2507.22478v1 (only version; arXiv comment "work in progress"), PDF, https://arxiv.org/abs/2507.22478v1, read in full (16 pages) on 2026-11-26.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Models studied and sizes (0.5B to 1.5B) | Yes. Five models from 0.5B to 1.5B: Qwen2.5-Coder-0.5B-Instruct, Qwen3-0.6B, Llama-3.2-1B-Instruct, DeepSeek-Coder-1.3B-Instruct, Qwen2.5-Coder-1.5B-Instruct. | "small language models (SLMs) ranging from 0.5B to 1.5B parameters currently underperform on Text-to-SQL tasks due to their limited logical reasoning capabilities." | Abstract, p. 1; model list: App. B, p. 8. |
| 2. SFT on SynSQL-Think-916K, then RL on BIRD train (algorithm, reward) | Yes. SFT (cross-entropy on CoT) on SynSQL-Think-916K (916,156 samples, filtered from SynSQL-2.5M, which includes the Spider and BIRD training sets with OmniSQL CoT), then GRPO on the BIRD training set (9,428). Reward R = R_EX + 0.1 R_Format, R_EX = 1 if the execution result is correct, else 0. A second model (merge revision) gets SFT on SynSQL-Merge-Think-310K and GRPO on BIRD-Merge-Train (7,159). GRPO: 6 rollouts, 1 epoch. | (1) "Next, we perform RL-based post-training on the BIRD training set using the Group Relative Policy Optimization (GRPO) (Shao et al., 2024) algorithm" (2) "The final reward is calculated as the weighted sum of REX and RFormat" | (1) Sec. 2, "Model Training", p. 3; data sizes: Table 1, p. 3. (2) App. C, Eqs. (1) to (3), p. 9; GRPO settings: App. B, p. 8. |
| 3. Inference: corrective self-consistency over several samples | Yes. The generation model samples (64 by default), samples are grouped by execution result and voted; if the vote is inconsistent, a merge revision model (8 samples) produces the final SQL. A 0.5B merge model is used for Qwen3-0.6B, Llama-3.2-1B and DeepSeek-Coder-1.3B. BIRD dev EX: 56.87 (0.5B), 67.08 (1.5B). | "Then, the generated SQL statements are grouped based on their execution results through a voting mechanism. If the voting results are inconsistent, the SQL is regenerated using the SQL merge revision model" | Sec. 2, "Inference", p. 3; sample counts: App. B, p. 8; results: Table 2, p. 3; ablation: Table 4, p. 4. |
| Models | The five models above as SQL generation models; merge revision models on Qwen2.5-Coder-0.5B-Instruct and Qwen2.5-Coder-1.5B-Instruct; Qwen2.5-Coder-7B-Instruct generates the candidates for the merge dataset. | "Five SLMs ranging in size from 0.5B to 1.5B were selected as base models for the experiments." | Sec. 3.1, p. 3; merge models: App. B, p. 8; 7B: Sec. 2, p. 2. |

## D. Zhang et al. 2025, SPFT-SQL (`zhang2025spftsql`)

Version read: arXiv 2509.03937v2 (11 Oct 2025; arXiv comment "EMNLP 2025 Findings"), PDF, https://arxiv.org/abs/2509.03937v2, read on 2026-11-26: abstract, Secs. 1 to 4, App. A.4 read; other appendices searched by keyword.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Verified data synthesis and self-play fine-tuning; synthetic SQL checked by execution? | Two stages. (i) Verification-based iterative fine-tuning: SQL is synthesized from templates filled with columns and values of the training databases, questions by a SQL-to-Text model; the fine-tuned Text-to-SQL model's outputs on a synthesized validation set are executed and compared with the synthesized gold SQL (Eq. 1); correct cases train the SQL-to-Text model, failed cases supply templates for the next round. (ii) Self-play: strongest candidate model is the main model, weakest is the opponent; loss (Eq. 3) is a SPIN-style logistic loss with the opponent in the denominator, weighted by an execution-based reward (Eq. 2). Whether each synthesized gold SQL is itself executed before use is not stated beyond the word "executable" (Secs. 1, 3.1 read). | (1) "The fine-tuned Text-to-SQL model is evaluated on the synthesized validation set Dval using an SQL executor E, and samples are classified based on execution results" (2) "This method randomly selects schemas (e.g., tables and columns) from the database and combines them with SQL templates to generate executable SQL queries." | (1) Sec. 3.1.3, Eq. (1), p. 4. (2) Sec. 1, p. 2; template filling: Sec. 3.1.1, p. 4; self-play: Sec. 3.2, Algorithm 1, Eqs. (2) and (3), p. 5. |
| 2. Models, including Qwen2.5-Coder-1.5B | Six models: Llama3-8B-Instruct, Deepseek-Coder-7B-Instruct, Qwen2.5-Coder 1.5B, 7B, 14B, 32B; Llama3-70B-Instruct in an appendix. Whether the Qwen2.5-Coder models are the Instruct versions is not stated. Qwen2.5-Coder-1.5B, Table 1: base / SFT / SPFT-SQL = Spider dev EX 72.4 / 76.8 / 79.7, Spider test EX 72.3 / 78.0 / 82.3, BIRD dev EX 40.6 / 44.3 / 54.0 (SPIN: 67.6, 68.5, 21.0). SFT baselines use LoRA (lr 2e-4, 3 epochs). | "six open-source LLMs, including Llama3-8B-Instruct (Touvron et al., 2023), Deepseek-Coder-7B-Instruct (Guo et al., 2024), and Qwen2.5-Coder (Hui et al., 2024) in sizes 1.5B, 7B, 14B, and 32B." | Sec. 4.1, "Models", p. 7; Table 1, p. 6; LoRA: App. A.4, p. 13; 70B: App. A.8, p. 14. |
| Models | As in row 2; Qwen2.5-Coder-7B is the base of Figure 1 and of the iteration study. | "the base model of SFT, SPIN (Chen et al., 2024b), and SPFT-SQL is Qwen2.5-Coder 7B." | Figure 1 caption, p. 1; Sec. 4.3, p. 7. |

## E. Papicchio et al. 2025, Think2SQL (`papicchio2025think2sql`)

Version read: arXiv 2504.15077v5 (4 May 2026), PDF, https://arxiv.org/abs/2504.15077v5, read on 2026-11-26: abstract, Secs. 1 to 3.3 read; appendices searched by keyword. The arXiv comment of v5 points to a newer TMLR paper on Qwen3 with another title ("Think2SQL: Blueprinting Reward Density and Advantage Scaling for Effective Text-to-SQL Reasoning"), not read.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. RL (GRPO) with execution-based rewards; training data (BIRD train); sizes | Yes, GRPO. Reward R = 0.85 R_text2SQL + 0.10 R_FR + 0.05 R_TCR, where R_text2SQL is either binary execution accuracy (R_EX) or the QATCH partial score (mean of cell precision, cell recall, tuple cardinality, all computed by execution). RL data: 9,007 BIRD training samples (BIRD train after removing 421 erroneous or duplicate entries). Optional SFT before RL on 1,142 DeepSeek-R1 reasoning traces from BIRD train. Qwen2.5-Coder-Instruct 0.5B, 1.5B, 3B, 7B, 14B; best BIRD dev weighted EX 0.602 (14B, RL with QATCH). | (1) "We show that partial scoring rewards, computed via SQL execution, are crucial for guiding models even when outputs are not fully correct." (2) "RLVR models (suffix RL) are trained with GRPO [54] for 1 epoch" | (1) Abstract, p. 1. (2) Sec. 3.1, p. 6 (9,007 BIRD samples, same paragraph); reward: Sec. 2.3, p. 5; filtering: Sec. 2.2, p. 3; results: Table 2, p. 7. |
| Models | Qwen2.5-Coder-Instruct family (Think2SQL-0.5B, 1.5B, 3B, 7B, 14B); DeepSeek-R1 for reasoning traces. | "We use the Qwen-2.5-Coder-Instruct family trained with Open-R1 [15, 62] and a fixed seed of 42." | Sec. 3.1, p. 6; sizes: Sec. 3.2, pp. 6 to 7, Fig. 3. |

## F. Yao et al. 2026, Arctic-Text2SQL-R1 (`yao2026arctic`)

Version read: arXiv 2505.20315v2 (12 Jan 2026), PDF, https://arxiv.org/abs/2505.20315v2, read on 2026-11-26: abstract, Secs. 1 to 5 read; appendices not read.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. GRPO with a reward from execution correctness: exact reward, sizes, data | GRPO with KL to a reference (SFT) model, beta = 0.001, 16 rollouts. Reward: 1 if execution results match the gold; 0.1 if the SQL is syntactically correct and executable; 0 otherwise. Final training data: filtered BIRD train (8,017), filtered Spider train (6,972) and dev (985), and Gretel-Synth-Filtered (11,811); online RL; models initialized from OmniSQL checkpoints. Sizes 7B, 14B, 32B. | (1) "we define a reward function focused solely on (1) final execution correctness and (2) basic syntax validity" (2) "the training data includes the filtered BIRD-training and SPIDER-training/dev sets, along with the model-based filtered Gretel-Synth-Filtered synthetic examples." | (1) Sec. 3, "Reward Model Design", p. 4. (2) Sec. 5, p. 7; sizes of data: Table 3, p. 3; RL settings: Sec. 4, p. 4. |
| Models | Arctic-Text2SQL-R1-7B, 14B, 32B. Starting points explored: Qwen2.5-Coder-32B (base and Instruct), Qwen2.5-Coder-14B-Instruct, QwQ-32B, OmniSQL-32B; final runs start from OmniSQL. GPT-4o writes INSERT statements for Gretel-Synth. | "As base models, we rely on the Qwen2.5-Coder series [16], including both base, instruct and reasoning-oriented variants." | Sec. 4, p. 4; Tables 4 and 5, p. 5; Table 7, p. 7. |

## G. Yi and Chen 2025, SKT-SQL (`yi2025sktsql`)

Version read: no arXiv version (arXiv API title search for "SKT-SQL" and for title words "skeleton", "decoupling", "SQL": no match). Journal record from Crossref, OpenAlex and Semantic Scholar on 2026-11-26: DOI 10.1007/s10844-025-00963-3, Journal of Intelligent Information Systems 63(5), 1779 to 1805, published 2025-07-08, authors Jiawen Yi and Guo Chen. None of the three APIs returns an abstract for the journal article (Semantic Scholar: "elided by the publisher"). The journal text (Springer) was not opened. Crossref also lists a preprint by the same two authors (DOI 10.21203/rs.3.rs-5318111/v1, posted 2024-11-06, title "Optimizing Text-to-SQL Transformations: The Potential of Skeleton Decoupling in SKT-SQL") with an abstract; the cells below come from that preprint abstract, a different version with a different title.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. What the framework does | Preprint abstract: a schema decoupler filters schema items linked to the question; a skeleton generator produces an abstract SQL skeleton that guides the model to the final SQL; evaluated on Spider (EX and EM). | "SKT-SQL employs a schema decoupler to filter relevant schema items linked to the natural language questions, reducing the burden on the model during the parsing process." | Preprint abstract (Crossref record of 10.21203/rs.3.rs-5318111/v1). |
| 2. Which models it calls small-scale | Not reachable. The registered journal title says "small-scale LMs", not "small-scale LLMs". The preprint abstract speaks of "smaller-scale language models" and names no model. | "This innovative strategy significantly enhances the accuracy of SQL skeleton generation using smaller-scale language models" | Journal title: Crossref, OpenAlex, Semantic Scholar records of 10.1007/s10844-025-00963-3; preprint abstract. |
| Models | Not reachable. | - | - |

## H. Rafailov et al. 2023, DPO (`rafailov2023dpo`)

Version read: arXiv 2305.18290v3 (29 Jul 2024), PDF, https://arxiv.org/abs/2305.18290v3, read on 2026-11-26: Secs. 1 to 4 and 6 read; appendices searched by keyword.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Pairs, loss against a reference policy, no reward model, no RL; equation number | Yes. L_DPO is Eq. (7): negative log-sigmoid of beta times the difference of the policy-to-reference log ratios of the preferred and the dispreferred response. The paper does not use the word "frozen"; it optimizes pi_theta "for the given pi_ref". | "we show how to directly optimize a language model to adhere to human preferences, without explicit reward modeling or reinforcement learning." | Sec. 1, p. 2; loss: Sec. 4, Eq. (7), p. 4; "for the given πref": Sec. 4, "DPO outline", p. 5. |
| 2. Choice of the reference model | The SFT model when available; otherwise a model trained by maximum likelihood on the preferred completions. In the dialogue experiment: Pythia-2.8B trained with Preferred-FT on the chosen completions serves as reference. | (1) "Since the preference datasets are sampled using π SFT , we initialize πref = π SFT whenever available. However, when π SFT is not available, we initialize πref by maximizing likelihood of preferred completions (x, yw )" (2) "we start with a pre-trained Pythia-2.8B, use Preferred-FT to train a reference model on the chosen completions" | (1) Sec. 4, "DPO outline", p. 5. (2) Sec. 6.2, p. 9. |
| Models | GPT-2-large (IMDb sentiment), a GPT-J SFT model (TL;DR summarization, CarperAI checkpoint), Pythia-2.8B (Anthropic HH dialogue); "up to 6B parameters". | "using language models with up to 6B parameters." | Sec. 1, p. 2; Sec. 6, p. 7; GPT-J: Sec. 6.2, p. 9. |

## I. Tao et al. 2025, CodeLutra (`tao2024codelutra`)

Version read: arXiv 2411.05199v3 (TMLR 06/2025), the PDF of `02_related_table1_rows.md`, Secs. 5.2 and 5.3 re-read on 2026-11-26.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Ablation with the DPO term alone: numbers on Spider and BIRD, table, sentence | The ablation is on Spider and DS-1000, not BIRD. Table 2: L_DPO alone 17.2 (Spider), 12.4 (DS-1000); full loss 76.6 and 48.6. The paper writes the Spider drop of 59.4 points as "↓59.4%". | "Notably, omitting optimizing the SFT loss on the correct solutions results in a marked decline in model performance, e.g., ↓59.4% on Spider." | Sec. 5.3, "Importance of SFT regularization during preference optimization", Table 2, p. 9. |
| 2. Table 1: base, SFT baseline, method by iteration (Spider, BIRD) | Llama-3-8B, EX (EM): base 59.3 (55.1) Spider, 22.3 (19.5) BIRD. SFT ("Fine-tuned LLMs" row) 67.9 (64.7), 35.6 (30.7). Iterations 1 to 4, Spider EX: 67.8, 72.4, 76.6, 76.3; BIRD EX: 37.8, 40.8, 43.1, 42.6. Best is iteration 3 on both. | "on the more challenging BIRD dataset, after three iterations, CodeLutra significantly improved the EX of the base model from 22.3 to 43.1, achieving performance very close to GPT-4." | Table 1, p. 8; Sec. 5.2, p. 8. |
| Models | Llama-3-8B (main), Gemma-7B and StarCoder-7B (Table 3); see row 7 of the property table of this paper. | "For main results, we apply our framework to the Llama-3-8B base model (Dubey et al., 2024), denoted as π0" | Sec. 5.1, p. 7. |

## J. Liu et al. 2025, CoT and DPO for Text-to-SQL (`liu2025cotdpo`)

Version read: arXiv 2502.11656v1 (only version), PDF, https://arxiv.org/abs/2502.11656v1, read on 2026-11-26: Secs. 1 to 6.2 and App. A, D, E read; other appendices searched by keyword. The ACL 2025 Anthology copy was not opened.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Pairs from the model's own samples, labelled by execution against gold, on BIRD train; models | Yes. SFT on BIRD train, then N = 16 samples per training question from the SFT model, labelled correct only if the execution result fully matches the gold; one correct and one incorrect sample form the pair; questions with all-correct or all-incorrect samples are dropped (about 1.5k to 2.5k pairs per model). Ten models, 6.7B to 15B. | "Using the SFT model, multiple SQL queries are sampled for each training sample. Correct and incorrect queries are identified through database execution to create preference pairs." | Sec. 1, p. 2; Sec. 3.4, p. 4; sample budget: App. D, p. 14; pair counts: App. E, p. 14. |
| 2. SQL-only DPO gives no consistent gain (how many models go down); CoT gives consistent gains | Yes. BIRD dev, Table 1. Vanilla (SQL only), greedy: EX goes down for 6 of 10 models (Deepseek-llm-7b-chat -0.6, Qwen2.5-14B-Instruct -0.8, CodeLlama-7b -1.3, Qwen2.5-Coder-7B -0.3, CodeS-7B -0.2, CodeS-15B -0.1); the other four gain +0.2 to +0.8. Vanilla Maj@16: down for 6 of 10. Vanilla Pass@1: up for all 10 (+0.6 to +1.3). Syn CoT: up for all 10 models under all three decodings, greedy +0.8 to +4.5 (e.g. Qwen2.5-7B-Instruct 57.4 to 61.9). | "Surprisingly, the results reveal that DPO does not consistently improve performance; in fact, it leads to performance degradation for 6 out of the 10 evaluated LLMs." | Sec. 1, p. 2; Table 1, p. 6; Sec. 5.1, p. 5. |
| 3. Likelihood term, reference model, pairs once or over rounds | Loss: plain DPO (no SFT term). An added SFT term on correct samples was tried as a "trick" on vanilla data (Qwen2.5-7B-Instruct, greedy: SFT 58.8, +SFT loss 60.0), reported as a limited gain. Reference: the SFT model, which also initializes the policy. Pairs made once from the SFT model; DPO trained 8 epochs on them. The SFT checkpoint used as reference is chosen by maj@K on the dev set. Online methods are called infeasible for SQL. | (1) "After fine-tuning, we obtain model πSF T , serving as the reference model for the subsequent DPO." (2) "Training is then continued for 8 epochs during the DPO phase." | (1) Sec. 3.3, p. 4; DPO loss: Sec. 3.4, p. 4. (2) App. D, p. 14; SFT-term trick: App. A, Table 7, p. 12; "online methods infeasible": Sec. 2, p. 3. |
| Models | Deepseek-llm-7b-chat, Meta-Llama-3.1-8B-Instruct, Qwen2.5-7B-Instruct, Qwen2.5-14B-Instruct, Deepseek-coder-6.7b-instruct, CodeLlama-7b-Instruct-hf, CodeLlama-13b-Instruct-hf, Qwen2.5-Coder-7B-Instruct, CodeS-7B, CodeS-15B; full-parameter fine-tuning. CoT synthesizer GPT-4o-mini (Qwen2.5-1.5B/7B/32B-Instruct in App. F). | "we evaluate 10 open-source LLMs, ranging from 6.7B to 15B parameters." | Sec. 1, p. 2; Table 1, p. 6; full-parameter: App. D, p. 14. |

## K. Pang et al. 2024, Iterative RPO (`pang2024irpo`)

Version read: arXiv 2404.19733v3 (26 Jun 2024), PDF, https://arxiv.org/abs/2404.19733v3, read on 2026-11-26: Secs. 1 to 3.3 read; appendices not read.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Loop: CoT from the current model, pairs by final-answer correctness, DPO + NLL, iterated; tasks | Yes. N = 30 samples per problem from M_t, K = 10 pairs per problem (GSM8K), loss Eq. (1) = DPO + alpha times length-normalized NLL on the winner, alpha = 1, beta = 0.1; reference is M_t, the previous iteration's model; four iterations on GSM8K, three on ARC-Challenge and MATH. On GSM8K the gold human solution is added to the winner set, so a winner can be a dataset solution. | (1) "On each iteration we sample multiple chain-of-thought reasoning steps and final answers over training prompts, and then construct preference pairs such that pair winners have correct answers and pair losers have wrong answers." (2) "We use the previous iteration’s model Mt as the reference model in the denominator of the DPO term." | (1) Sec. 1, p. 1. (2) Sec. 2, Eq. (1), p. 3; GSM8K setup and gold in winners: Sec. 3.1, p. 4; ARC, MATH: Secs. 3.2, 3.3, pp. 7 to 8. |
| 2. Without NLL against with NLL (GSM8K), table | Table 1: iteration 1 of Iterative RPO 73.1; standard DPO on the same first-iteration pairs 61.8 (from Llama-2-70b-chat) or 60.3 (from SFT on chosen). Iterations 1 to 4: 73.1, 78.0, 81.1, 81.6. The comparison is one round of DPO against one round of DPO + NLL; no iterated DPO without NLL is reported. ARC / MATH (Table 2): standard DPO 82.8 / 12.4, iteration 1 84.8 / 17.7. | "We see a large performance drop (73.1% vs. 61.8%) using DPO compared to our method after one iteration." | Sec. 3.1, "NLL loss is necessary in our method", p. 6; Table 1, p. 5; Table 2, p. 8. |
| Models | Llama-2-70B-Chat as M0 for all tasks. | "As a seed model M0 we use the chat version of Llama-2 70B model [Touvron et al., 2023], which is instruction fine-tuned." | Sec. 3.1, p. 4. |

## L. Lanchantin et al. 2025, offline to online RL (`lanchantin2025bridging`)

Version read: arXiv 2506.21495v1 (only version), PDF, https://arxiv.org/abs/2506.21495v1, read on 2026-11-26: Secs. 1 to 4.2 and App. Table 4 read; Sec. 5 and other appendices searched by keyword.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Offline, semi-online, online DPO (and GRPO); definition of semi-online; result with numbers | Yes, DPO in three regimes and GRPO (online). Semi-online: the generation model is synced with the trained model every s update steps (offline s = infinity, online s = 1). Verifiable math (Table 1), Math500: seed 47.4, offline DPO 53.7, semi-online s = 100 58.9, s = 10 57.2, online DPO 58.7, GRPO 58.1. Instruction following (Table 2), AlpacaEval LC with GPT-4-1106 judge: seed 27.3, offline 53.2, semi-online s = 10 81.6, s = 5 78.7, online 83.1, GRPO 75.2. In the verifiable task the DPO reference model is synced along with the generator in semi-online and online DPO, not in offline DPO; in the non-verifiable task it is not synced (Table 4). Adding an NLL term gave no benefit here. | (1) "In our work we consider a semi-online DPO setup where the generation model parameters are synchronized with the training model parameters only periodically, but potentially much more often than in the iterative setting just described." (2) "First, online and semi-online trained models (s ≥ 1) all outperform the offline DPO model (s = ∞) by a wide margin." | (1) Sec. 2.3, p. 3. (2) Sec. 4.1, p. 6; Table 1, p. 5; Table 2, p. 6; reference sync: Sec. 3, p. 4, and Table 4, p. 15; NLL: Sec. 4.2, p. 8. |
| Models | Llama-3.1-8B-Instruct for all runs; reward model Athene-RM-8B for the non-verifiable task. | "For all tasks, we initialize model parameters using the Llama-3.1-8B-Instruct model." | Sec. 3, p. 4; reward model: Sec. 3.1, p. 4. |

## M. Ni et al. 2023, LEVER (`ni2023lever`)

Version read: arXiv 2302.08468v3 (1 Sep 2023, ICML 2023), PDF, https://arxiv.org/abs/2302.08468v3, read on 2026-11-26: abstract, Secs. 1 to 3.2 and the Spider table read; the rest searched by keyword.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Verifier on question, program and execution result; reranks samples; Spider among the datasets | Yes. Verification labels by comparing each sampled program's execution result with the gold result; reranking score = generation probability times verifier probability, summed over programs with the same execution result. The code LLMs are used few-shot and not fine-tuned; only the verifier is trained. Datasets: Spider, WikiTableQuestions, GSM8K, MBPP. Spider dev EX with code-davinci-002: greedy 75.3, LEVER 81.9. | "we train verifiers to determine whether a program sampled from the LLMs is correct or not based on the natural language input, the program itself and its execution results." | Abstract, p. 1; labels: Sec. 2.3, p. 3; datasets: Sec. 3.1, p. 3; Spider: Table 2, p. 5. |
| Models | Generators: Codex (code-davinci-002), InCoder-6B, CodeGen-16B-multi. Verifiers: T5-base for Spider, T5-large for WikiTQ and MBPP, RoBERTa-large for GSM8K. | "We select T5-base for Spider, T5-large for WikiTQ and MBPP, and RoBERTa-large for GSM8k as the base LM for the verifiers" | Sec. 3.2, p. 4; verifier choice: p. 5. |

## N. Tritto et al. 2026, GradeSQL (`tritto2026gradesql`)

Version read: arXiv 2509.01308v2 (29 Oct 2025, header "Currently under review"), PDF, https://arxiv.org/abs/2509.01308v2, read on 2026-11-26: abstract, Secs. I, III, IV and the first part of V read. The Springer journal copy was not opened.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. ORMs trained on candidates labelled by execution, used at inference to select; is the generator trained? | Yes. OmniSQL-7B samples N = 32 candidates per training question; a candidate is "Yes" if its result set equals the gold one, "No" otherwise, execution errors discarded (82,640 labelled BIRD samples, 50,073 Spider). An LLM is fine-tuned with LoRA to output "Yes"/"No"; the "Yes" probability ranks candidates in Best-of-N. The generator is not trained: OmniSQL-7B is used as released. | (1) "A candidate cj ∈ Ycandidate is labeled as correct if its result set matches that of the gold query ygoldi" (2) "At inference, the ORM functions as a post-generation re-ranking module, selecting the most semantically faithful query from the candidate pool generated by the base model." | (1) Sec. III.B, Stage 2, p. 4; LoRA: Stage 3, p. 4. (2) Sec. I, p. 2; generator: Sec. IV, p. 6; dataset sizes: Table II, p. 6. |
| Models | Generator OmniSQL-7B. ORMs: Qwen2.5-1.5B-Instruct, Qwen2.5-7B-Instruct, Granite-3.3-2B-Instruct, Granite-3.3-8B-Instruct, Llama-3.2-1B-Instruct, Llama-3.1-8B-Instruct, OmniSQL-7B. | "we adopt OmniSQL-7B [27] as the generator" | Sec. IV, p. 6; ORM list: Sec. V, p. 6. |

## O. Kuang et al. 2024, FederatedScope-LLM (`kuang2024fsllm`)

Version read: arXiv 2309.00363v1 (only version), PDF, https://arxiv.org/abs/2309.00363v1, read on 2026-11-26: abstract, Secs. 3.1, 6.1 read; the whole text searched for "SQL". The KDD copy (ACM) was not opened.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Package and benchmark for federated PEFT; code generation (Fed-CodeAlpaca) and its result for centralized, FedAvg, local; "SQL"? | Yes, package with a benchmarking pipeline and federated PEFT algorithms (LoRA, P-tuning, prompt tuning). Fed-CodeAlpaca: 9 clients, one programming language each, evaluated on HumanEval (Pass@1). LLaMA-7B with LoRA, FedAvg, 500 rounds: global (centralized) 13.54, fed 13.29, local 10.99. OPT-2.7B with LoRA: 0.61, 0.43, 0.25. "SQL" does not occur in the paper. | (1) "we provide comprehensive and off-the-shelf federated parameter-efficient fine-tuning (PEFT) algorithm implementations" (2) "It simulates a nine-client FL scenario. Each client’s dataset consists of coding exercises with answers limited to one specific programming language, such as Java or Python." | (1) Abstract, p. 1. (2) Sec. 3.1, p. 4; results: Sec. 6.1, Table 2, p. 10; OPT: Table 3, p. 11. |
| Models | LLaMA-7B and OPT-2.7B. | "We use a widely adopted LLM, LLaMA-7B, with three PEFT algorithms" | Sec. 6.1, p. 10; OPT-2.7B: p. 11. |

## P. Ye et al. 2024, OpenFedLLM (`ye2024openfedllm`)

Version read: arXiv 2402.06954v1, the PDF of `02_related_table1_rows.md`, Secs. 4.1, 4.2 and 4.5 re-read on 2026-11-26.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Federated instruction tuning: algorithms, base model, LoRA | Seven FL algorithms (FedAvg, FedProx, SCAFFOLD, FedAvgM, FedAdagrad, FedYogi, FedAdam) plus local training as reference. Instruction tuning: Llama2-7B, int8, LoRA rank 32, alpha 64, 200 rounds, 10 local steps per round. | "we implement 7 representative FL baselines in OpenFedLLM. Specifically, we integrate FedAvg [20], FedProx [49], SCAFFOLD [50], FedAvgM [44], FedAdagrad, FedYogi, and FedAdam [54]." | Sec. 4.1, "Baselines", p. 7; training details: Sec. 4.1, p. 8. |
| 2. Code task (HumanEval): FedAvg, FedProx, SCAFFOLD, local | Code domain (CodeAlpaca, 20k samples, 10 clients, 2 per round), Table 7, HumanEval Pass@1: local 0.116, FedAvg 0.165, FedProx 0.146, SCAFFOLD 0.140 (FedAdagrad best, 0.183). HumanEval also appears in the general-purpose table (Alpaca-GPT4, Table 4): local 9.15, FedAvg 14.02, FedProx 14.63, SCAFFOLD 17.68. | "During training, we set the client number as 10, where we randomly sample 2 clients to be available for each round. These clients hold 20k data samples in total." | Sec. 4.5, p. 11; Table 7, p. 10; Table 4, p. 9. |
| Models | Llama2-7B for instruction tuning; Wizard-Vicuna-7B-Uncensored for FedDPO (see row 7 of the property table of this paper). | "We use the pre-trained Llama2-7B [4] as the base model and run 200 communication rounds of FL." | Sec. 4.1, p. 8. |

## Q. Wu et al. 2025, FedBis and FedBiscuit (`wu2025fedbiscuit`)

Version read: arXiv 2407.03038v3 (8 Apr 2025, ICLR 2025 header), PDF, https://arxiv.org/abs/2407.03038v3, read on 2026-11-26: abstract, Secs. 1, 4, 5 (start), 6, 7 (setup), App. A read; the whole text searched for "SQL".

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Clients train binary selectors; server aggregates, labels pairs, trains the LLM (objective); human preferences; FedDPO baseline; "SQL"? | Yes. Clients train a binary selector (cross-entropy, Eq. 3) on their pairwise preference data; the server aggregates with FedAvg (FedBiscuit: several selectors on clusters of clients, majority vote). At the server the initial LLM theta_0 generates completions for server-held instructions, the selector labels all pairs, and the LLM is trained with DPO for three epochs; pairs are made once from theta_0. Client data: human preferences (TL;DR comparisons split by worker ID into 53 clients; SHP, preference by number of likes). Baselines: FedAvg and FedDPO. "SQL" does not occur. | (1) "each client independently trains a binary selector, and the server aggregates these selectors into a global one and broadcasts it to the clients." (2) "The reinforcement-learning fine-tuning takes place on the server and includes two phases" | (1) Sec. 4, p. 4. (2) App. A.2, p. 17; DPO update: Eq. (9), p. 18; data: Sec. 6, p. 8; baselines and three epochs: Sec. 7, p. 8. |
| Models | Selectors: Qwen-2-0.5B, Gemma-2B, LLaMA-2-7B. LLMs trained: Gemma-2B and LLaMA-2-7B, both fine-tuned on Alpaca. | "We adopt Gemma-2B and LLaMA-2-7B models for the summarization and QA tasks, where both models are fine-tuned on the Alpaca dataset" | Sec. 7, p. 8. |

## R. Nayak et al. 2026, PubSwap (`nayak2026pubswap`)

Version read: arXiv 2604.12160v1 (only version), PDF, https://arxiv.org/abs/2604.12160v1, read on 2026-11-26: abstract, Secs. 1 to 4.1 read; the whole text searched for "SQL".

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Federated RLVR with GRPO at the clients; what the server adds; tasks; sizes; "SQL"? | Yes. Clients run local GRPO steps with LoRA (rank 32, alpha 64); LoRA matrices are averaged. On public-data steps the server samples a batch of public prompts, each client sends K responses, and the server returns responses for each client's GRPO update ("Random" or "Balanced": a client with fewer than K/2 correct responses gets up to K/2 - c_n correct responses from other clients). The server does not generate. Tasks: math (MATH, DeepMath) and medical (MedQA + MedMCQA). Sizes 1.5B to 4B. "SQL" does not occur. | (1) "In our approach, each client performs local GRPO steps using Low-Rank Adaptation (LoRA) (Hu et al., 2022) rather than full fine-tuning" (2) "During the public step, every client generates K responses for the same shared batch of prompts and sends these generations to the server." | (1) Sec. 1, p. 2. (2) Sec. 3, p. 5; Balanced rule: Sec. 3, p. 6; tasks and LoRA settings: Sec. 4.1, pp. 6 to 7. |
| Models | Qwen2.5-Math-1.5B, Qwen3-1.7B, Qwen3-4B-Instruct (Table 2: Qwen3-4B-Instruct-2507) for math; Llama3.2-3B-Instruct for medical. | "presenting results on Qwen2.5-MATH-1.5B (Yang et al., 2024), Qwen3-1.7B and Qwen3-4B-Instruct models" | Sec. 4.1, p. 6; medical model: p. 7. |

## S. Guo et al. 2026, Fed-GRPO (`guo2026fedgrpo`)

Version read: arXiv 2610.11502v1 (only version), PDF, https://arxiv.org/abs/2610.11502v1, read on 2026-11-26: abstract, Secs. 1, 3 (observations), 6.1 to 6.3, App. experimental details read; the whole text searched for "SQL" and "LoRA".

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. Federated GRPO with aggregation weighted by a reward statistic; tasks; sizes; "SQL"? | Yes. Aggregation weight w_k = sigma_k / sum_j sigma_j, sigma_k the reward standard deviation of client k in the round (Eq. 4); also global reward calibration and adaptive sparse communication. Tasks: math (MATH train split by difficulty over 5 clients; evaluated on GSM8K, MATH-500, AIME 2024, AIME 2025, AMC 2023) and code (MBPP train+validation, Dirichlet 0.5 over length buckets; evaluated on MBPP test and HumanEval). Binary correctness reward; 12 rounds, 5 local steps. LoRA is not mentioned (whole text searched). "SQL" does not occur. | "(i) signal-weighted aggregation that weights clients by their reward standard deviation, prioritizing clients with stronger learning signals" | Abstract, p. 1; Eq. (4), p. 5; setup: Sec. 6.1, p. 8; code results: Sec. 6.3, Table 3, p. 9. |
| Models | Qwen2.5-3B-Instruct (math and code) and Qwen3-4B-Instruct (math). | "The base models are Qwen2.5-3B-Instruct Yang et al. (2025b) and Qwen3-4B-Instruct Yang et al. (2025a)" | Sec. 6.1, p. 8. |

## T. Zhang et al. 2023, FL4SP (`zhang2023fl4sp`)

Version read: arXiv 2305.17221v1, the PDF of `02_related_table1_rows.md`, Secs. 4.2 and 6.1 re-read on 2026-11-26.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. MacroAvg EM: centralized, FedAvg, best federated variant | Table 2, MacroAvg EM: centralized 70.32; individual finetuning 62.78; FedAvg 40.03; FedAvg + Lorar 60.16; FedProx 41.67, + Lorar 58.39; FedOPT 58.32, + Lorar 62.55 (best federated). MicroAvg: centralized 74.21, FedOPT + Lorar 69.39, FedAvg 57.89. | "by equipping them with our proposed Lorar, we can reduce the gap by 4-20 points (i.e., absolute difference under MacroAvg)." | Table 2, p. 7; Sec. 6.1, "FL vs. Finetuning/Centralized", p. 6. |
| 2. What Lorar is | Aggregation weight of client i in round t proportional to its training-set size times its training-loss reduction in that round: p_i^t = \|D_i\| dL_i^t / sum_i \|D_i\| dL_i^t. Applied to FedAvg, FedOPT, FedProx. | "we use the training loss reduction to adjust the weight of each client, so as to reschedule its contribution to the global model update." | Sec. 4.2, Eq. (6), p. 5. |
| Models | T5-base (see row 7 of the property table of this paper). | "Specifically, we adopt T5-base as our backbone semantic parser in the FL paradigm" | Sec. 1, p. 2. |

## U. Xu et al. 2024, KGRFL (`xu2024kgrfl`)

Version read: no arXiv version. Abstract from OpenAlex and Semantic Scholar (identical) on 2026-11-26; Crossref record without abstract: DOI 10.1109/TCSS.2023.3246795, IEEE Transactions on Computational Social Systems 11(1), 1035 to 1045, February 2024. The IEEE text was not opened. The cells rest on the abstract only.

| Statement | What the paper says | Quotation | Locator |
|---|---|---|---|
| 1. What is trained with FL (BART parser from questions to SPARQL?) and what the RL part does | A multitask semantic parsing model (MSP-BART) identifies the question category and converts the question into SPARQL; the abstract says the approach enables multi-institution joint modeling but does not say in so many words that MSP-BART is the federated model. The RL part is a model fusion (aggregation) strategy that also reduces the effect of low-quality clients; it does not train the parser from rewards. Also a prompt-learning entity disambiguation step. | (1) "We design an end-to-end multitask semantic parsing model [MSP-bidirectional and auto-regressive transformers (BART)] that identifies question categories while converting questions into SPARQL statements" (2) "a reinforcement learning (RL)-based model fusion strategy is proposed to improve the effectiveness of federated learning" | Abstract (OpenAlex / Semantic Scholar records of 10.1109/TCSS.2023.3246795). |
| Models | BART (variant and size not given in the abstract). | - | Abstract. |

## V. Four works read from their arXiv abstract pages only (2026-11-28)

Each is cited in one clause that stays within its abstract; the papers themselves were not opened.

| Paper | What the abstract says | Quotation | Locator |
|---|---|---|---|
| Sun et al. 2024, FFA-LoRA (`sun2024ffalora`), arXiv 2403.12313v1, comments "published at ICLR 2024" | LoRA in federated learning can be unstable; a key factor is that clients optimize the two low-rank matrices jointly and the server aggregates them separately. FFA-LoRA fixes the randomly initialized matrices and fine-tunes only the zero-initialized ones | "the discordance between jointly optimizing the two low-rank matrices by local clients and separately aggregating them"; "fix the randomly initialized non-zero matrices and only fine-tune the zero-initialized matrices" | https://arxiv.org/abs/2403.12313 |
| Wang et al. 2024, FLoRA (`wang2024flora`), arXiv 2409.05976v1, no venue stated on the page | Standard aggregation of LoRA adapters is mathematically inaccurate; FLoRA aggregates by stacking and supports adapters of different ranks | "These approaches led to mathematically inaccurate aggregation noise"; "through a novel stacking-based aggregation method." | https://arxiv.org/abs/2409.05976 |
| Zhang et al. 2025, ExeSQL (`zhang2025exesql`), arXiv 2505.17231v1 | For SQL dialects other than SQLite: iterative query generation, execution-based filtering and preference-based training; the abstract names no training algorithm | "iterative query generation, execution-based filtering (e.g., rejection sampling), and preference-based training" | https://arxiv.org/abs/2505.17231 |
| Kulkarni and Srikumar 2025 (`kulkarni2025reinforcing`), arXiv 2506.06093v1, comments "Under review at EMNLP 2025" | Text-to-SQL tuned with GRPO on scalar rewards from execution, with question-answer pairs as weak supervision; the benchmark is not named in the abstract | "We use the rewards within the Group Relative Policy Optimization (GRPO) framework."; "with only weak supervision in the form of question-answer pairs" | https://arxiv.org/abs/2506.06093 |

"That averaging the two LoRA factors separately does not average their product" is arithmetic and our own sentence, not a statement of either paper. Whether the federated averaging of OpenFedLLM averages the factors separately was not checked; the sentence of Section 2.3 speaks of this paper's method and baselines only.

## Points for the editor

Statements that were wrong or imprecise:

- I.1: CodeLutra's DPO-only ablation is on Spider and DS-1000, not BIRD (Table 2: 17.2 vs 76.6 on Spider, 12.4 vs 48.6 on DS-1000). The paper writes the 59.4-point drop as "↓59.4%".
- A.2: Only CodeS-1B/3B/7B come from StarCoderBase; CodeS-15B comes from StarCoder-15B. SFT is full fine-tuning on each benchmark's training set.
- C.2: SLM-SQL trains two models (SQL generation and merge revision), each with SFT then GRPO. The GRPO reward is R_EX + 0.1 R_Format. SynSQL-Think-916K already contains Spider and BIRD training questions.
- D.1: SPFT-SQL's self-play loss is not DPO. It is a SPIN-style loss whose denominator is the opponent model, weighted by an execution-based reward. The execution check runs on the fine-tuned model's outputs, compared with the synthesized gold SQL. The paper does not say that each synthesized gold SQL is executed.
- E.1: Think2SQL's best models use the QATCH partial reward (cell precision, recall, cardinality, computed by execution) weighted 0.85 with two format terms, not binary EX alone. The RL data is BIRD train minus 421 removed entries (9,007).
- F.1: Arctic's reward is not execution correctness alone. An executable, syntactically valid query gets 0.1. The abstract nevertheless says "based solely on execution correctness". Training data also includes Spider train and dev and synthetic Gretel data, and the final models start from OmniSQL checkpoints.
- G: The registered title ends "on small-scale LMs", not "LLMs". Neither the abstract nor the models of the journal article were reachable.
- J.2: "No consistent gain" holds, but EX falls for 6 of 10 models only under greedy decoding and under Maj@16. Under Pass@1, vanilla DPO raises all ten models (+0.6 to +1.3).
- J.3: CoT-DPO's pairs are made once, from the SFT model, and DPO then runs 8 epochs. The reference is that SFT model, which was itself chosen by maj@K on BIRD dev. An SFT term was tried only as an unsuccessful "trick" on SQL-only data.
- K.2: IRPO's NLL ablation compares one round of standard DPO with one round of DPO + NLL on the same pairs. No iterated DPO without NLL is reported. On GSM8K the winner set includes the gold human solution.
- U: KGRFL's RL is for model fusion (aggregation), not for training the parser.

Disagreements inside or between papers:

- CodeLutra says that "after four iterations" Llama-3-8B "exceeded SFT performance by 16.9%". Table 1 gives the best Spider EX, 76.6, at iteration 3 (iteration 4: 76.3), against SFT 67.9: a difference of 8.7 points (12.8% relative). 16.9 does not follow from Table 1.
- SynSQL-2.5M size: OmniSQL gives 2,544,390 samples. SLM-SQL's Table 1 lists SynSQL-2.5M at 2,190,988.
- OpenFedLLM's Table 7 caption says "All FL algorithms can outperform local training". Its own cells contradict this: on CoNaLa BLEU, local 0.228 is above FedAvg 0.224, FedProx 0.221, FedYogi 0.201 and FedAdam 0.217. On HumanEvalSyn (Python), local 0.171 is above FedProx, SCAFFOLD and FedAvgM (0.152). The text says only that FedAvg is "better or comparably".
- Lanchantin et al. say "two semi-online DPO settings" but list s in [5, 10, 100]. Table 1 uses s = 100 and 10, Table 2 s = 10 and 5. The abstract expands GRPO as "Group Reward Policy Optimization".
- Fed-GRPO's Table 3 caption says coding tasks, but its column headers read GSM8K and MATH-500. The text gives MBPP test and HumanEval as the code benchmarks. All results are the best checkpoint over training.
- GradeSQL states Spider's training set as 9,000 queries; CodeS gives 8,659 (7,000 annotated plus 1,659).
- Think2SQL v5 points to a newer TMLR paper on Qwen3 under another title. A citation must say which of the two it means.
- Arctic's Table 7 lists the ExCoT models as "ExDPO-32B" and "ExDPO-70B".

What a one-line summary would get wrong:

- FL4SP: the best federated MacroAvg (FedOPT + Lorar, 62.55) is below individual per-client finetuning (62.78) as well as centralized training (70.32). FedAvg alone reaches 40.03.
- FedBiscuit is federated only in the selector. The LLM is trained centrally at the server with offline DPO on pairs generated once by the initial model. Client data are human preferences, not execution labels.
- PubSwap's server adds no model output of its own. It routes client responses on shared public prompts. Fed-GRPO, unlike PubSwap, includes a code task (MBPP, HumanEval), but neither paper has SQL.
- LEVER and GradeSQL train only a verifier or reward model. The generator is never trained in either.
- None of FS-LLM, FedBiscuit, PubSwap or Fed-GRPO contains the string "SQL". OpenFedLLM does not either (see the Table 1 sheet).
- CodeS, OmniSQL and CoT-DPO share authors (Haoyang Li, Renmin University of China, is an author of all three). CoT-DPO's models are all 6.7B to 15B. SLM-SQL, Think2SQL and SPFT-SQL are the papers here that train models of 1.5B or less.
