# FedLS-SQL: literature

Closest published work to the fixed setup in `RESEARCH_STATE.md` (5 non-IID
Spider clients, Qwen2.5-Coder-1.5B-Instruct student with LoRA, optional frozen
Qwen2.5-Coder-7B-Instruct teacher at the server on public BIRD train, two
24 GB GPUs). Compiled 2026-11-06; sections 1.6, 1.7 and FedAuto added 2026-11-07.

How to read this file:

- Every paper was opened at the URL given. "Full" means the numbers come from
  the paper's tables; "abstract" means only the abstract was read, so its
  numbers are the abstract's claims.
- Venues come from the ACL Anthology, the proceedings page, or the arXiv
  comment field. "Venue not verified" means the arXiv page lists none; check
  before citing a venue.
- Metrics differ across papers: EX (execution accuracy), TS (test-suite
  accuracy), greedy vs self-consistency (SC) or majority voting. Each number
  names its protocol. Numbers from different papers are not comparable with
  ours unless the protocol matches.

## 1. Closest papers

### 1.1 Federated learning with a server LLM and client SLMs

| Paper | Setting | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| FedMKT, Fan et al., COLING 2025 ([ACL](https://aclanthology.org/2025.coling-main.17/)) | Server LLM + public data; clients send logits on public data; mutual KD, both sides LoRA | LLaMA2-7B server; 1.1-1.5B clients | RTE, BoolQ, CQA, ARC, S-NI, DialogSum | Client vs FedAvg, CQA: 58.6 vs 56.4 (LLaMA2-1.3B), 61.5 vs 58.6 (OPT-1.3B). Frozen-teacher arm "LLM2SLM": CQA 59.1 vs Standalone 58.6, full method 60.7 | Server 7B + public data + ~1.5B clients. Teacher is trained; public data is a fifth of the same task's train split (in-distribution); no code or SQL | full |
| FedCoLLM, Fan et al., 2024 ([arXiv 2411.11707](https://arxiv.org/abs/2411.11707)) | Clients send LoRA; server aggregates, then mutual KD between server LLM and aggregated SLM on auxiliary data | OPT-6.7B / 1.3B; LLaMA2-7B / 1.3B | CQA, OBQA, ARC | Client SLM vs FedAvg, CQA: 60.8 vs 58.6 (OPT-1.3B); ARC-E ~0 gain. Server LLM CQA 48.7 -> 68.1 | Structurally nearest: FedAvg of SLM LoRA plus a server-side distillation step between rounds. Teacher trained; QA tasks; no "FedAvg + gold SFT on the same server data" control. Venue not verified | full |
| FedCoT, Fan et al., Findings EMNLP 2025 ([ACL](https://aclanthology.org/2025.findings-emnlp.454/)) | Server LLM writes rationales for DP-perturbed client prompts | LLaMA3-70B / Qwen1.5-14B teacher; Pythia-1.4B / Qwen1.5-0.5B student | CQA, BoolQ, ARC-E | CQA 42.4 (standalone) -> 48.1 (eps=3) -> 49.2 (non-private) | CoT distillation into an SLM. Client data (perturbed) reaches the teacher, which our data rule forbids | full |
| FedBiOT, Wu et al., KDD 2024 ([arXiv 2406.17706](https://arxiv.org/abs/2406.17706)) | Server compresses its LLM, re-aligns it on public data each round; clients tune an adapter | LLaMA-2-7B | Rosetta code (9 languages, HumanEval-X), GSM8K, Dolly | GSM8K 15.2 vs 9.9-10.2 for offsite-tuning baselines | Public-data alignment step at the server each round, evaluated on code. Deploys the full LLM, not a separate SLM | full |
| CrossLM, Deng et al., 2023 ([arXiv 2312.05842](https://arxiv.org/abs/2312.05842)) | Server LLM generates labelled synthetic data, client SLMs score it | GPT2-L / Llama-7B; BERT-size clients | SST-2, IMDb, AG News, Yahoo | SLM mean acc 0.765 standalone -> 0.825 | Teacher-generated data for clients. Classification only. Venue not verified | full |
| FedAuto, Wang et al., 2025 ([arXiv 2512.22035](https://arxiv.org/abs/2512.22035)) | Server pre-trains on public data, then each round trains on public data in parallel with the clients and merges its model with theirs (weight 1/(1 + connected clients)); extra server steps on classes missing from client updates | CNN, ResNet, ViT-86M with LoRA | MNIST, CIFAR-10/100 | CIFAR-10 non-IID: 68.35 without its two modules, 77.00 with both (Table 5, read from a summary) | The "server trains on public data during every round" pattern, with a merge rule. Vision classification, no LLM. Preprint, under review | sections I-IV |
| GPT-FL, Zhang et al., 2023 ([arXiv 2306.02210](https://arxiv.org/abs/2306.02210)) | Server generative model makes synthetic data; model pre-trained on it, then FL | not in abstract | vision/audio/text | no numbers in abstract | Teacher knowledge enters as the FL starting point; its FL-only vs synthetic-only vs both ablation is the right shape for a teacher-contribution test | abstract |

No paper in this family evaluates on SQL or code with a separate deployed SLM,
uses a frozen teacher whose public data comes from another domain, or compares
against "FedAvg plus supervised training on the same public data". Client
gains over FedAvg are 1-3 points; the large gains are on the server LLM side.

### 1.2 Federated Text-to-SQL, code and non-IID LoRA

| Paper | Setting | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| FL for Semantic Parsing (FL4SP, Lorar), Zhang et al., ACL 2023 ([arXiv 2305.17221](https://arxiv.org/abs/2305.17221)) | 8 clients, each a whole single-domain Text-to-SQL dataset; full fine-tuning | T5-base | Advising, ATIS, GeoQuery, Restaurants, Scholar, Academic, IMDB, Yelp | MacroAvg EM: centralized 70.3, per-client 62.8, FedAvg 40.0, FedProx 41.7, FedOPT 58.3, FedOPT+Lorar 62.6 | The only federated Text-to-SQL paper found. Exact match, small seq2seq model, no teacher, no Spider | full |
| FederatedScope-LLM, Kuang et al., 2023 ([arXiv 2309.00363](https://arxiv.org/abs/2309.00363)) | LoRA FL benchmark | LLaMA-7B | Fed-CodeAlpaca (9 clients by language), Dolly, GSM8K | HumanEval: centralized 13.54, FedAvg 13.29, local 10.99 | Code clients split by language: FedAvg near centralized. Venue not verified | full |
| OpenFedLLM, Ye et al., 2024 ([arXiv 2402.06954](https://arxiv.org/abs/2402.06954)) | FL instruction tuning and FedDPO framework, 7 FL algorithms | Llama2-7B int8, LoRA r=32 | Alpaca-GPT4, CodeAlpaca, finance | Code HumanEval: FedAvg 0.165, FedProx 0.146, SCAFFOLD 0.140, local 0.116 | Drift corrections give no consistent gain. Venue not verified | full |
| FedLLM-Bench, Ye et al., 2024 ([arXiv 2406.04845](https://arxiv.org/abs/2406.04845)) | Naturally partitioned FL datasets | Llama2-7B, LoRA | chat, IT, preference | Fed-ChatbotIT: FedAvg 5.51, FedProx 5.49, SCAFFOLD 5.34 | Same conclusion on drift corrections. Venue not verified | full |
| FL in LLM-based program repair, 2024 ([arXiv 2412.01072](https://arxiv.org/abs/2412.01072)) | 100 clients, Dirichlet 0.1 to ~0 | 6 code LLMs, 7B-15B, QLoRA | program repair | Federated beats local for all 6 models; heterogeneity effect called negligible | Code LLMs under strong Dirichlet skew. Venue not verified | full |
| FedPETuning, Zhang et al., 2022 ([arXiv 2212.10025](https://arxiv.org/abs/2212.10025)) | PEFT in FL | RoBERTa-base | GLUE, Dirichlet 1.0 | FedLoRA 81.0 vs centralized LoRA 84.4 | Small encoder; alpha 0.1 hurts PEFT more. Venue not verified | full |
| FLoRA, Wang et al., NeurIPS 2024 ([arXiv 2409.05976](https://arxiv.org/abs/2409.05976)) | Stacking LoRA modules instead of averaging A and B | TinyLlama-1.1B, Llama-7B | Wizard, ShareGPT, Dolly | MT-bench Llama-7B: centralized 4.38, FedIT 3.07, FLoRA 4.21 | LoRA aggregation; large gains mainly with heterogeneous ranks | full |
| FedSA-LoRA, ICLR 2025 ([arXiv 2410.01463](https://arxiv.org/abs/2410.01463)); FFA-LoRA, ICLR 2024 ([arXiv 2403.12313](https://arxiv.org/abs/2403.12313)) | LoRA aggregation variants | RoBERTa-large, LLaMA-7B | GLUE, GSM8K | +1 to +1.5 over plain federated LoRA | Aggregation only | full |

For 7B LLMs with LoRA on instruction and code data, FedAvg stays within
about a point of centralized and FedProx, SCAFFOLD and FedAdam do not beat it
consistently. The 30-point gap in FL4SP comes from a small T5 model on eight
unrelated SQL datasets. No paper measures this gap for a 1-2B decoder on
cross-database Text-to-SQL with EX; it has to come from our own centralized
reference.

### 1.3 Federated preference optimization and federated RL with verifiable rewards

| Paper | Setting | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| FedBis / FedBiscuit, Wu et al., ICLR 2025 ([arXiv 2407.03038](https://arxiv.org/abs/2407.03038)) | Clients train binary preference selectors; server aggregates them, labels its own generations, runs DPO at the server | Selectors 0.5B-7B; policy Gemma-2B, LLaMA-2-7B | TL;DR, SHP | Win rate vs FedDPO (local DPO + LoRA averaging): 86.7 vs 49.0 (Gemma-2B), 91.3 vs 77.0 (LLaMA-2-7B) | Server-side DPO between rounds; FedDPO is the standard baseline. Human preferences, no verifier, no teacher | full |
| FedPDPO, 2026 ([arXiv 2603.19741](https://arxiv.org/abs/2603.19741)); pFedDPO, 2026 ([arXiv 2610.12885](https://arxiv.org/abs/2610.12885)) | Personalized federated DPO for conflicting client preferences | LLMs | preference data | up to +4.8 average accuracy (FedPDPO) | Target non-IID preference conflict, which an execution verifier does not have | abstract |
| FedRLHF, Fan et al., AAMAS 2025 ([arXiv 2412.15538](https://arxiv.org/abs/2412.15538)) | Local reward functions, personalized RLHF, convergence guarantees | small | MovieLens, IMDb | on par with centralized RLHF | Theory-focused | abstract |
| PubSwap, Nayak et al., 2026 ([arXiv 2604.12160](https://arxiv.org/abs/2604.12160)) | Federated GRPO; server broadcasts public prompts, clients swap correct responses on them | Qwen2.5-Math-1.5B, Qwen3-1.7B/4B, Llama-3.2-3B, LoRA r=32 | MATH, DeepMath, MedQA | Pass@1 Qwen3-1.7B: FedAvg-GRPO 50.7 vs 55.8; at few local steps sometimes worse (Qwen3-4B tau=40: 66.5 vs 65.4) | Public data injected into federated RLVR at small sizes. Gains come from drift reduction at many local steps; no teacher; math | full |
| Fed-GRPO, Guo et al., 2026 ([arXiv 2610.11502](https://arxiv.org/abs/2610.11502)) | Reward-std-weighted aggregation for federated GRPO | Qwen2.5-3B, Qwen3-4B | MATH, MBPP | Math avg: centralized 40.21, FedAvg 37.10, Fed-GRPO 39.06 | FedAvg already near centralized with an objective reward | full |
| FedMOA, 2026 ([arXiv 2602.00453](https://arxiv.org/abs/2602.00453)) | Federated GRPO with heterogeneous rewards | not in abstract | math, code | up to +2.2 over FedAvg | Aggregation-side method | abstract |

No federated DPO or RLVR work on Text-to-SQL was found, and none combines a
frozen server teacher with federated preference optimization.

### 1.4 Training small models for Text-to-SQL (SFT, CoT, DPO, RL)

| Paper | Method | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| Liu et al., "Uncovering the Impact of CoT Reasoning for DPO: Lessons from Text-to-SQL", ACL 2025 ([ACL](https://aclanthology.org/2025.acl-long.1031/)) | Self-sampled, execution-labelled DPO pairs, with and without synthetic CoT | 10 models, 6.7B-15B, incl. Qwen2.5-Coder-7B-Instruct | BIRD, Spider | BIRD dev greedy, Qwen2.5-Coder-7B: SQL-only SFT 61.6 -> DPO 61.3; CoT SFT 60.8 -> DPO 63.4. SQL-only DPO lowers EX for 6 of 10 models. Spider train yields only 0.1-0.3k pairs | Direct counter-evidence to SQL-only DPO, at 6.7B+. Notes that Spider train has no test-suite databases, so "correct" labels have false positives. No online DPO (execution cost) | full (Spider appendix not read) |
| ExCoT, Zhai et al., 2025 ([arXiv 2503.19988](https://arxiv.org/abs/2503.19988)) | CoT SFT, one off-policy DPO round on GPT-4o samples, two on-policy rounds; execution vs gold | LLaMA-3.1-70B, Qwen2.5-Coder-32B | BIRD + Spider | 70B BIRD dev / Spider test: SFT 58.1 / 81.4 -> off-policy 66.3 / 82.5 -> on-policy 68.5 / 86.6; on-policy only 66.3 / 84.2. SQL-only DPO 60.0 / 81.0, below SQL-only SFT 62.0 / 83.0 | Closest pair construction: teacher pairs as warm start, then on-policy rounds. Centralized, 32-70B, 64 H100. Venue not verified | full |
| SENSE, Yang et al., ACL 2024 ([ACL](https://aclanthology.org/2024.acl-long.425/)) | GPT-4 synthetic SFT data + DPO on execution-labelled pairs from a weak 1.3B model | CodeLLaMA-7B/13B | Spider, BIRD | DPO step adds +0.2 to +0.9 Spider dev EX, +1.9 to +2.6 BIRD dev; removing strong data costs 22-32 points | Strong data matters far more than the preference step at 7B+ | full |
| OmniSQL, Li et al., PVLDB 18(11) per header ([arXiv 2503.02240](https://arxiv.org/abs/2503.02240)) | SynSQL-2.5M with CoT; CoT-enhanced Spider + BIRD | Qwen2.5-Coder 7B-32B | Spider, BIRD, variants | 7B greedy, Spider test (TS): base 82.2, gold Spider+BIRD SFT 80.7, CoT Spider+BIRD 86.6; BIRD dev 50.9 / 55.1 / 59.6 | Plain gold SFT can lower Spider test below the base model; teacher CoT raises it. Student is 7B | full |
| CodeS, Li et al., SIGMOD 2024 ([arXiv 2402.16347](https://arxiv.org/abs/2402.16347)) | SQL-centric pre-training + SFT | 1B-15B | Spider, BIRD | Spider dev EX: 77.9 (1B), 83.4 (3B); BIRD dev with evidence 50.5 (1B) | Reference for what Spider SFT reaches at ~1-3B (different base model) | full |
| SLM-SQL, Sheng and Xu, Findings IJCNLP-AACL 2025 ([ACL](https://aclanthology.org/2025.findings-ijcnlp.92/)) | 916K synthetic CoT SFT + GRPO on BIRD + corrective self-consistency | Qwen2.5-Coder-0.5B/1.5B-Instruct | SynSQL, BIRD | 1.5B Spider dev EX (SC@16): zero-shot 63.5, SFT 74.5, SFT+RL 75.2; Spider test 78.4; BIRD dev 67.1 (CSC, 64 samples) | Strongest published 1.5B numbers; all use sampling, none greedy; tables partly inconsistent | full |
| Think2SQL, Papicchio et al., 2025 ([arXiv 2504.15077](https://arxiv.org/abs/2504.15077)) | GRPO with EX or partial rewards, trained on BIRD only | Qwen2.5-Coder 0.5B-14B | BIRD, Spider | 1.5B BIRD dev (gold tables, T=0.7): 27.5 -> 44.2. BIRD-only RL raises Spider: 3B 72.5 -> 77.0, 7B 77.6 -> 82.2 | BIRD-trained reasoning transfers to Spider; gold-table schema. Venue not verified | full |
| Reasoning-SQL, Pourreza et al., 2025 ([arXiv 2503.23157](https://arxiv.org/abs/2503.23157)) | GRPO with SQL partial rewards on BIRD | Qwen2.5-Coder 3B-14B | BIRD | BIRD dev 3B: SFT 55.9 -> GRPO 58.7. Spider after BIRD training, 7B: SFT 68.1 vs GRPO 78.7 | BIRD SFT transfers badly to Spider; RL transfers. 8x H100. Venue not verified | full |
| Arctic-Text2SQL-R1, Yao et al., 2025 ([arXiv 2505.20315](https://arxiv.org/abs/2505.20315)) | GRPO, reward 1 for EX match, 0.1 for executable | 7B-32B | BIRD, Spider, synthetic | 7B BIRD dev 68.9, Spider test 88.8 greedy; online beat batch RL (66.6 vs 64.9) | Simple execution reward suffices; 64 H100. Venue not verified | full |
| CogniSQL-R1-Zero, Gajjar et al., 2025 ([arXiv 2507.06013](https://arxiv.org/abs/2507.06013)) | GRPO with LoRA, 6 rollouts | Qwen2.5-Coder-7B | BIRD | BIRD dev 60.0 single sample | Only RL run near our budget (4x A100-40GB, ~6 h per epoch). Venue not verified | full |
| SQL-R1, Ma et al., NeurIPS 2025 per arXiv comment ([arXiv 2504.08600](https://arxiv.org/abs/2504.08600)) | GRPO, 8 rollouts, layered reward | 3B-14B | SynSQL, Spider, BIRD | 3B Spider dev / test (SC@8): 78.1 / 78.9 | Headline numbers use self-consistency | full |
| MSc-SQL, Gorti et al., NAACL 2025 ([arXiv 2410.12916](https://arxiv.org/abs/2410.12916)) | Several QLoRA 7-9B models + a critic over candidates with execution results | 7B-9B | BIRD, Spider | BIRD dev 65.6, Spider test 84.7 | Multi-model inference pipeline, not a single SLM | full |
| DTS-SQL ([arXiv 2402.01117](https://arxiv.org/abs/2402.01117)), DAIL-SQL (PVLDB 17(5), [arXiv 2308.15363](https://arxiv.org/abs/2308.15363)), DIN-SQL (NeurIPS 2023, [arXiv 2304.11015](https://arxiv.org/abs/2304.11015)) | Two-stage SFT; ICL prompting; decomposed prompting | 7B; GPT-4 | Spider, BIRD | DTS-SQL Mistral-7B Spider dev 71.9 -> 78.6 | Prompting and schema-linking references | DTS full; others abstract |

Below 6.7B the only DPO-style Text-to-SQL result found is SQLoom (section
1.6: Qwen3-1.7B, token-restricted DPO terms, GPT-4-mined negatives). No
verified paper compares iterative with one-shot DPO at 1.5B or reports a
greedy, single-sample, Spider-trained 1.5B Qwen2.5-Coder number. Zero-shot 1.5B Spider dev numbers
differ by about 6 points across sources, so the paper must report its own.

### 1.5 LLM-to-SLM distillation

| Paper | Method | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| DistiLLM-2, Ko et al., ICML 2025 ([arXiv 2503.07067](https://arxiv.org/abs/2503.07067)) | Contrastive: skew KL up on teacher responses, skew reverse KL down on student responses | Qwen2.5-Coder-7B-Instruct -> Qwen2.5-Coder-1.5B (our exact pair) | WizardCoder prompts; HumanEval, MBPP | HumanEval / MBPP: student 30.7 / 60.8, GKD 40.9 / 61.9, DistiLLM-2 42.2 / 62.7 | Same model pair; training prompts differ from test distribution. Code, not SQL; unclear whether the student was the Instruct checkpoint | full |
| KID, Zhong et al., Findings EMNLP 2024 ([arXiv 2410.11371](https://arxiv.org/abs/2410.11371)) | Token-level KD on ground-truth SQL with simulated inference errors | LLaMA2-7B -> TinyLLaMA-1.1B, LoRA | Spider, BIRD, Spider variants | Average over 5 sets: SFT 46.9, reverse-KL KD 48.8 (1.4x time), GKD 49.0 (8.3x), KID 51.8 (1.5x) | White-box KD for Text-to-SQL at ~1B: on-policy KD gains little for its cost. Teacher trained on the same data, no domain shift | full |
| GKD, Agarwal et al., ICLR 2024 ([arXiv 2306.13649](https://arxiv.org/abs/2306.13649)) | On-policy KD on student samples with teacher token distributions | T5 77M-800M students | XSum, WMT, GSM8K | ~2x the gain of offline KD | Standard on-policy KD baseline | full |
| MiniLLM, Gu et al., ICLR 2024 ([arXiv 2306.08543](https://arxiv.org/abs/2306.08543)) | Reverse KL on student samples | OPT-13B -> 1.3B, others | Dolly | GPT-4 score 60.7 vs SFT 52.6 | Word-level KD and SeqKD about equal to SFT at 1.3B | full |
| Speculative KD, Xu et al., ICLR 2025 ([arXiv 2410.11325](https://arxiv.org/abs/2410.11325)) | Teacher replaces student tokens outside its top-K | Gemma-7B -> 2B, Qwen2-7B -> 0.5B | translation, summarization, GSM8K | Pure on-policy KD collapsed on translation (36.1 COMET vs 73.3 supervised KD) | Risk of on-policy KD when student samples are poor | full |
| Qwen3 Technical Report, 2025 ([arXiv 2505.09388](https://arxiv.org/abs/2505.09388)) | Off-policy then on-policy logit distillation | 32B/235B -> 0.6B-14B | reasoning | 8B: on-policy KD beats RL at 1,800 vs 17,920 GPU-h | Industrial reference for the two-phase recipe | full (sec. 4.5) |
| Small Models Struggle to Learn from Strong Reasoners, Li et al., 2025 ([arXiv 2502.12143](https://arxiv.org/abs/2502.12143)) | Long vs short CoT, large vs small teacher | Qwen2.5 0.5B-32B students | MATH etc. | 1.5B: long CoT 27.0 vs short 34.2; 72B teacher 32.2 vs 3B teacher 33.0 | Same student family and size: short CoT only. Venue not verified | full |
| Struct-SQL, Thaker and Bresler, Canadian AI 2026 ([arXiv 2512.17053](https://arxiv.org/abs/2512.17053)) | CoT derived from the query execution plan of verified teacher SQL | GPT-4o -> Qwen3-4B, QLoRA | 1,000 BIRD train rows; BIRD mini-dev | EX: gold SFT 34.3, free CoT 36.9, structured CoT 45.0 | Structured, execution-verified CoT from BIRD at small budget; in-domain eval only | full |
| Personalised Distillation, Chen et al., EMNLP 2023 ([arXiv 2310.18628](https://arxiv.org/abs/2310.18628)) | Student attempts, teacher refines that attempt, student learns from its own errors | 16B students | code | beats standard distillation with a third of the data | Teacher-as-corrector for code | abstract |
| SERL-SQL, Liu et al., 2026 ([arXiv 2608.00485](https://arxiv.org/abs/2608.00485)) | Training-only teacher rescores student SQL actions; reweights GRPO | not verified | BIRD, Spider | BIRD dev 76.6, Spider test 89.9 | Teacher used only in training for SQL | abstract |
| PLaD, Findings ACL 2024 ([arXiv 2406.02886](https://arxiv.org/abs/2406.02886)); DPKD, 2024 ([arXiv 2406.19774](https://arxiv.org/abs/2406.19774)); Zephyr dDPO, 2023 ([arXiv 2310.16944](https://arxiv.org/abs/2310.16944)) | Teacher output preferred over student output, or teacher-ranked pairs, trained with a preference loss | 120M-13B | generation tasks | see papers | Preference distillation without a verifier | abstract |
| Distilling step-by-step, Findings ACL 2023 ([arXiv 2305.02301](https://arxiv.org/abs/2305.02301)) | Rationale as an auxiliary output | T5-770M | NLP | 770M beats few-shot 540B PaLM on one benchmark | Rationale used only in training, not at inference | abstract |

Also relevant to pair sources: Iterative RPO, Pang et al., NeurIPS 2024
([arXiv 2404.19733](https://arxiv.org/abs/2404.19733), full): self-sampled
pairs labelled by answer correctness, DPO + NLL, gold added as chosen when no
sample is correct. Llama-2-70B GSM8K greedy 73.1 -> 78.0 -> 81.1 -> 81.6 over
four rounds; twice the pairs in one round gives 74.8; without NLL 61.8.
Step-DPO ([arXiv 2406.18629](https://arxiv.org/abs/2406.18629), abstract)
reports self-generated pairs beat GPT-4-generated ones, which are out of
distribution for the policy.

### 1.6 Token- and clause-level preference and RL for SQL and code

Idea shared by this group: a correct and a wrong query share most tokens, so a
sequence-level loss spreads the signal over tokens that are not the error.
Each paper localizes the error and puts the signal there.

| Paper | How the error is localized | Loss | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|---|
| Focused-DPO, Zhang et al. (Peking U.), 2025 ([arXiv 2502.11475](https://arxiv.org/abs/2502.11475)); arXiv page names no venue, Findings ACL 2025 per a search listing, not verified | Self-sampled code (k=10, T=1.5) ranked with self-generated tests; strip the common prefix and suffix of a correct and a wrong sample; the middle span is the error point | DPO with the middle-span log-ratio weighted by w=2 (w=5 hurts), rejected suffix dropped, reference = SFT model, no NLL term | 6.7-7B (DeepSeekCoder, Qwen2.5-Coder-7B base and Instruct) | 5,000 problems per policy | Qwen2.5-Coder-7B-Instruct, HumanEval+ / MBPP+: base 0.841 / 0.714, SFT 0.872 / 0.717, DPO 0.854 / 0.743, token-level TDPO 0.872 / 0.751, Focused-DPO 0.878 / 0.762. LiveCodeBench avg 0.310 (DPO) vs 0.339 | Closest loss to a SQL version of pair focusing; gains over plain DPO are 1-3 points on 7B code. Error points overlap only 32% between two models, so the points are model-specific (supports on-policy pairs). No seeds or variance | full text |
| SQLoom, Fu et al., 2026 ([arXiv 2611.03298](https://arxiv.org/abs/2611.03298)); preprint 2 Nov 2026 in a WWW 2027 template, not peer-reviewed | Three sets: parser-valid vs invalid next tokens (syntax); reference AST node vs a confusion the current model often makes, kept only if execution changes on the database or on mutated counterexample databases (semantics); question edits propagated along clause dependencies (logic). GPT-4 agents mine errors, propose confusions and edit questions; parser and execution accept or reject | Set-contrastive loss over the constrained tokens only; with one negative it is DPO restricted to those tokens. Always with an SFT term; reference = SFT warm-up model; beta 0.1 | Qwen3-1.7B, LoRA r=16, lr 5e-5 | Spider-Refined (Spider train, 378 labels fixed, GPT-4 schema descriptions added to the input) or BIRD train, one model each; 38K GPT-4 calls; 10.8 GPU-h (2.3x SFT) on one RTX 4090 | Greedy, 3 seeds: Spider dev 88.7, test 89.2, BIRD dev 73.4 (76.8 with evidence). Zero-shot Spider dev 62.9; plain LoRA SFT about 79.6 (211 errors on 1,034). Ablations on Spider test / BIRD dev: without constraint training -12.5 / -9.7, without GPT-4 error corrections -11.1 / -17.2, constraints replaced by SFT on the same data -8.8 / -10.3, retrieval context +0.7-2.1 | Nearest DPO-style Text-to-SQL work at our size; details and federated mapping below the table. Centralized, GPT-4 sees the training data. Its zero-shot baselines look implausibly low (Qwen2.5-Coder-7B 22.6 on Spider dev), and it does not say where the stage-3 retrieved pairs come from for dev databases | full |
| CAPER, Ban et al., 2026 ([arXiv 2606.03327](https://arxiv.org/abs/2606.03327)) | Compare predicted and gold SQL at the first diverging top-level clause; AST repair gives a counterfactual correct clause; fault injection on correct rollouts, kept if execution changes | A clause-level process reward model (9B, pairwise margin loss) guides GRPO with clause-level advantages, mixed with the execution reward | Qwen3.5-9B; 8x A100, 189 GPU-h | BIRD train, SynSQL-5k and Spider dev (dev overlaps evaluation) | P@1 Spider test: SFT 78.71, GRPO outcome reward 81.56, clause reward 82.63, token reward 79.17; BIRD dev 57.56 / 60.21 / 63.56 / 57.36 | Clause beats both sequence-level and token-level credit. RL with a learned PRM, far above our budget | sections 1-4 and tables 1-2 verbatim |
| EXPO-SQL, Lee et al., 2026 ([arXiv 2606.23693](https://arxiv.org/abs/2606.23693)) | Clause-wise incremental execution (FROM/JOIN, WHERE, GROUP BY, ... added in order) compared with the gold result; SQLite error messages traced back to the clause | Policy gradient with one reward per clause, all its tokens share it, KL penalty, no group baseline | Qwen2.5-Coder-7B, 14B | SynSQL-Complex-5k | 7B Spider dev / test / BIRD dev: 88.5 / 89.1 / 71.3, vs Arctic-SQL-R1-7B 87.3 / 88.8 / 68.9. Ablation (summary): BIRD dev 71.3 full, 68.5 without clause rewards | Clause localization by execution alone, no PRM and no teacher; this is the localization a client can run on its own databases | sections 1-4 verbatim; ablations from a summary |

SQLoom training, in order (Algorithm 1; `Correct` = SFT on GPT-4 corrections
of the model's own failed training predictions, each repaired by execution in
at most 5 rounds, with 10% replay, then LoRA merge 0.5 x new + 0.5 x previous):

1. SFT one epoch, then `Correct`; this model is the DPO reference.
2. Set-contrastive training, 2 epochs, then `Correct`.
3. SFT with the 3 most similar verified pairs of the same database in the
   prompt, 2 epochs, then `Correct`.

Which parts need an LLM: the syntax oracle (incremental SQLite parser over the
schema) and the counterexample databases (sub-database of referenced tables;
duplicated rows, boundary values, extra child rows; up to 10 sub-databases x
200 mutations; keys and types kept valid) need none. Semantic confusions are
proposed by GPT-4 but are of fixed types (table, column, value, COUNT vs
COUNT DISTINCT, >= vs >, quantifier, ordering) and are ranked by how often the
current model makes them. The logic level and the error corrections need
GPT-4.

What this means for pair-based training here: clause-level localization beat
sequence-level and token-level credit in CAPER and EXPO-SQL, and
error-span weighting beat plain DPO by 1-3 points on 7B code. None of the four
is federated; only SQLoom is below 7B, and it relies on GPT-4.

### 1.7 Evidence for a server step on public data (read 2026-11-07)

Collected for `DIRECTION.md` section 6. "Read" names what was checked.

| Paper | Number | What it says for us | Read |
|---|---|---|---|
| DistiLLM-2 ([2503.07067](https://arxiv.org/abs/2503.07067)) | Table 4, Coder 7B -> 1.5B: HumanEval 30.73 -> 42.24, GKD 40.85; LoRA r16, 4x A100-80GB. Appendix D.1 (GPT-2, Dolly, ROUGE-L): on-policy 26.37, batched 26.20, off-policy 26.13 | The student is most likely the base checkpoint (30.7 vs the official base 43.9 and Instruct 70.7 in the Qwen2.5-Coder report); this is inferred, the paper does not say. On-policy adds little over off-policy | tables |
| KID ([2410.11371](https://arxiv.org/abs/2410.11371)) | Spider dev EX, Qwen1.5-0.5B with a 7B teacher: SFT 57.8, forward KL 57.3, reverse KL 61.5, GKD 64.3 (13.9x SFT time). TinyLLaMA: SFT 63.0, reverse KL 66.0, GKD 64.8, KID 68.1 | The teacher is fine-tuned on Spider (in-domain). Forward KL is about equal to SFT; reverse KL helps | tables |
| Reasoning-SQL ([2503.23157](https://arxiv.org/abs/2503.23157)) | Table 5, 7B Spider: base 77.85, BIRD gold SFT 68.08, GRPO 78.72 | Gold SFT on BIRD hurts Spider; execution RL on BIRD does not. Dev or test not stated | table |
| Think2SQL ([2504.15077](https://arxiv.org/abs/2504.15077)) | Table 4, 3B Spider 72.5 -> 77.0 | Needs both R1-reasoning SFT on 913 BIRD rows and QATCH-reward RL (T=0.7, 40 h on 8x H100); no 1.5B result | table |
| SLM-SQL ([ACL](https://aclanthology.org/2025.findings-ijcnlp.92/)) | Table 3, 1.5B Spider dev SC@16: zero-shot 63.54, SFT 74.53, SFT + BIRD RL 75.15 | BIRD RL adds +0.6 on Spider once Spider is in the SFT data; no greedy numbers | table |
| OmniSQL ([2503.02240](https://arxiv.org/abs/2503.02240)) | Table 5, 7B greedy Spider dev / test: base 73.4 / 82.2, SynSQL only 74.6 / 83.5, gold Spider+BIRD 76.9 / 80.7, CoT Spider+BIRD 80.3 / 86.6, all 81.2 / 87.9 | SynSQL alone adds about 1.2 points; CoT beats gold SFT by 3.4 dev / 5.9 test. No model below 7B; generated tables carry two example rows, sparsity not discussed | table |
| Arctic-Text2SQL-R1 ([2505.20315](https://arxiv.org/abs/2505.20315)) | SynSQL "initial attempts were inconclusive"; unfiltered synthetic data 64.9 -> 64.6, filtered 66.5 | Execution RL on SynSQL needs filtering; smallest model 7B | text |
| SERL-SQL ([2608.00485](https://arxiv.org/abs/2608.00485)) | Removing the teacher rescoring: -2.55 Spider test (likely the 14B model) | The "teacher" is a synced copy of the student; students 7-32B on 16x H100 | ablation |
| Rethinking on-policy distillation ([2604.13016](https://arxiv.org/abs/2604.13016)) | An R1-Distill 1.5B student did not improve from a 7B teacher of the same pipeline | On-policy distillation fails when the teacher has no capability the student lacks. Math only | text |
| Liu et al. ACL 2025 ([2502.11656](https://arxiv.org/abs/2502.11656)) | Table 14, Spider dev greedy, 7B: CoT SFT 0.7-2.6 below SQL-only SFT; CoT + DPO ends 0.5-0.7 above SQL-only SFT. Recipe: CoT from GPT-4o-mini with gold SQL shown, K=16; DPO samples at T=1.0, one random correct/wrong pair per question, beta 0.1, LR 1e-6, 8 epochs, one offline round | CoT pays off only after execution-labelled DPO, and only a little on Spider | full text via summary |
| ExCoT ([2503.19988](https://arxiv.org/abs/2503.19988)) | 70B Spider test: CoT SFT 81.4 vs SQL-only SFT 83.0; 86.6 after 3 DPO rounds (up to 32 samples per question); zero-shot simple CoT 77.8 vs no CoT 78.8-79.3 | Same pattern at 70B; divide-and-conquer chains grow from 560 to 910 tokens | full text via summary |
| Struct-SQL ([2512.17053](https://arxiv.org/abs/2512.17053)) | Qwen3-4B, BIRD mini-dev EX: gold SFT 34.3, free CoT 36.9, query-plan CoT 45.0; free-CoT model scored with the query-plan prompt 29.2 | Structured query plans beat free CoT at 4B; prompt mismatch is costly. Weak baselines (base 17.0 from 1,465-token thinking) | full text via summary |
| STaR-SQL ([2502.13550](https://arxiv.org/abs/2502.13550)) | Llama-3.1-8B Spider dev: 75.0 vs SQL-only SFT 68.6; 8 samples per question, gold-hint rationalization, iterate | Self-generated rationales verified by execution; the SQL-only baseline looks weak | full text via summary |
| OmniSQL CoT synthesis ([2503.02240](https://arxiv.org/abs/2503.02240), sections 3.5 and 4) | Several open models given the SQL, 8 samples at T=0.8, majority vote on execution | SynSQL's shipped CoT is answer-conditioned and checked on two-row databases | full text via summary |
| Answer-conditioned CoT ([2607.14552](https://arxiv.org/abs/2607.14552)) | Chains written with the answer visible hurt distillation in a way correctness filters miss (math) | Argues against SynSQL's shipped CoT | abstract |
| FedCoT, Li et al. ([2508.10020](https://arxiv.org/abs/2508.10020)) | Clients generate and select chains locally with a discriminator; medical tasks | No execution verifier, no server teacher | abstract |
| FedDF ([2006.07242](https://arxiv.org/abs/2006.07242)) | NLP results only as a figure (DistilBERT, alpha 1) | Its gain comes from fusing drifted, heterogeneous models | figure |

Timing: no LLM paper compares a server step after every round with one-time
server training before FL.

What this means for the server step: on SQL-only greedy Spider EX, the
published gains from KD or RL on public data are about 1 point once the
student has seen Spider; larger KD gains need an in-domain teacher or a weak
base student. CoT training has the largest gains over gold SFT (OmniSQL), at
7B, but on Spider greedy CoT SFT alone stays below SQL-only SFT and moves
ahead only after execution-labelled DPO rounds (Liu et al., ExCoT).

## 2. What already exists

- Server LLM with public data helping federated SLMs (FedMKT, FedCoLLM,
  CrossLM, GPT-FL). Client gains over FedAvg are 1-3 points; teachers are
  trained, public data is in-distribution, tasks are classification or QA.
- Federated DPO as local DPO plus LoRA averaging (the "FedDPO" baseline in
  OpenFedLLM and FedBiscuit), and server-side DPO on aggregated preference
  signals (FedBiscuit). All on human preferences.
- Federated RL with verifiable rewards at 1.5-4B (PubSwap, Fed-GRPO, FedMOA),
  on math and code. FedAvg is already within 1-3 points of centralized.
- Centralized execution-verified preference training for Text-to-SQL
  (ExCoT, Liu et al., SENSE) at 7B-70B, and execution-reward RL (Arctic,
  Reasoning-SQL, Think2SQL, SLM-SQL) mostly on 8-64 large GPUs.
- Text-to-SQL distillation into ~1B students (KID) and code distillation with
  our exact model pair (DistiLLM-2).
- One federated Text-to-SQL paper (FL4SP), with T5-base and exact match.

## 3. Gaps that fit our setup

1. No federated Text-to-SQL work with a modern decoder SLM and execution
   accuracy. FL4SP is the only reference and predates LLM-based Text-to-SQL.
2. No federated preference optimization with a verifier: in Text-to-SQL each
   client can label its own samples by executing them against its own
   databases and gold SQL, so pairs are built locally without human labels.
   Federated DPO so far uses human preferences.
3. Little evidence on DPO for Text-to-SQL below 6.7B. The published finding
   (Liu et al.) is that SQL-only sequence-level DPO fails at 6.7-15B because
   pairs are scarce; a 1.5B student makes more errors and may yield many more
   pairs. The one small-model result (SQLoom, 1.7B) uses token-restricted
   terms with GPT-4-mined negatives, centrally. Whether iterative on-policy
   rounds help at 1.5B is untested.
4. No frozen-teacher-at-server design where the public data comes from
   another domain (BIRD) than the clients' (Spider), and no paper in the
   server-LLM family runs the matched control "same public data with gold
   labels, no teacher".
5. No BIRD-to-Spider distillation result for SQL at any size; the closest
   evidence (Think2SQL, Reasoning-SQL, OmniSQL) says reasoning-style training
   on BIRD transfers to Spider while plain gold SFT on BIRD can hurt it.
6. No CoT distillation for SQL at 1.5B; math evidence at 1.5B favors short
   CoT, SQL evidence at 4B favors structured, execution-verified CoT.

## 4. Points a reviewer will raise from this literature

- Liu et al. (ACL 2025) and ExCoT both report SQL-only DPO giving no gain or a
  loss at 7B+. A paper claiming a large SQL-only DPO gain at 1.5B must report
  pair counts per client, DPO with and without the NLL term, and the gain
  over an SFT model trained for the same compute.
- Spider train has no test-suite databases, so an execution-matched sample
  can be wrong (false positive chosen). This affects every pair built on
  client data.
- Server-teacher papers confound "more data at the server" with "teacher
  signal". The matched control (same BIRD questions, gold SQL instead of
  teacher output) is expected.
- With an objective verifier, FedAvg is close to centralized in every recent
  federated RLVR paper, so aggregation-side contributions have little room;
  a centralized reference with the same method is expected to show where the
  federated version stands.
- Published 1.5B numbers mostly use self-consistency; ours must name greedy or
  sampled decoding explicitly.
- SQLoom reports 89.2 greedy Spider test at 1.7B. A reviewer will compare;
  the paper has to state that SQLoom trains centrally on Spider + BIRD with
  GPT-4 in the loop, while here client data never leaves and no external
  model sees it.
- A sequence-level DPO method will be asked why it does not localize the
  error (Focused-DPO, CAPER, EXPO-SQL). Either localize, or show the
  comparison.
