# FedLS-SQL: literature

Closest published work to the fixed setup in `RESEARCH_STATE.md` (5 non-IID
Spider clients, Qwen2.5-Coder-1.5B-Instruct student with LoRA, optional frozen
Qwen2.5-Coder-7B-Instruct teacher at the server on public BIRD train, two
24 GB GPUs). Compiled 2026-11-06; updated 2026-11-14 with the papers from
five research reports on journal articles, wrong-result SQL, label-free
training, the server stage and federated mechanisms; updated 2026-11-15 with
a full reading of the published 1.5B Spider results (SPFT-SQL, SLM-SQL,
FINER-SQL, CodeS, the Qwen2.5-Coder report), section 1.4; updated
2026-11-16 with section 1.16 (mechanisms that could be added to the core)
and section 1.17 (a gap scan for the added mechanism: synthesis at the
clients, other clients' models as helpers, vote labels), and section 1.18
(training on perturbed schemas); updated 2026-11-17 with section 1.19
(prompt, training and decoding practice, for the clean setup); updated
2026-11-25 with section 1.22 (federated Text-to-SQL scan). Sections
written before 2026-11-17 compare with the earlier setup and its numbers.

How to read this file:

- "Full" and named sections/tables distinguish reading the paper body from
  reading only its abstract. Sections 1.1-1.7 retain their earlier reading
  records; new entries in 1.8-1.15 were checked against primary sources on
  2026-11-14. An abstract supports its stated mechanism and scope, not an
  assessment of experimental details absent from it.
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
| FL in LLM-based program repair, 2024 ([arXiv 2412.01072](https://arxiv.org/abs/2412.01072)) | 100 clients, Dirichlet 0.1 to ~0 | 6 code LLMs, 7B-15B, QLoRA | program repair | Federated beats local for all 6 models; heterogeneity effect called negligible | Code LLMs under strong Dirichlet skew. Published in ACM Transactions on Software Engineering and Methodology (Crossref record, DOI 10.1145/3733599) | full |
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
| FedMOA, 2026 ([arXiv 2602.00453](https://arxiv.org/abs/2602.00453)) | Federated GRPO with heterogeneous rewards | Qwen2.5-1.5B-Instruct | math, code | MATH 62.6 to 64.8, Heter+Heter, Table 1 | Aggregation-side method; matched rows and setup checked in section 1.12 | sections 3.3-4, Table 1 |

No federated DPO or RLVR work on Text-to-SQL was found, and none combines a
frozen server teacher with federated preference optimization.

### 1.4 Training small models for Text-to-SQL (SFT, CoT, DPO, RL)

| Paper | Method | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| Liu et al., "Uncovering the Impact of CoT Reasoning for DPO: Lessons from Text-to-SQL", ACL 2025 ([ACL](https://aclanthology.org/2025.acl-long.1031/)) | Self-sampled, execution-labelled DPO pairs, with and without synthetic CoT | 10 models, 6.7B-15B, incl. Qwen2.5-Coder-7B-Instruct | BIRD, Spider | BIRD dev greedy, Qwen2.5-Coder-7B: SQL-only SFT 61.6 -> DPO 61.3; CoT SFT 60.8 -> DPO 63.4. SQL-only DPO lowers EX for 6 of 10 models. Spider train yields only 0.1-0.3k pairs | Direct counter-evidence to SQL-only DPO, at 6.7B+. Notes that Spider train has no test-suite databases, so "correct" labels have false positives. No online DPO (execution cost) | full (Spider appendix not read) |
| ExCoT, Zhai et al., 2025 ([arXiv 2503.19988](https://arxiv.org/abs/2503.19988)) | CoT SFT, one off-policy DPO round on GPT-4o samples, two on-policy rounds; execution vs gold | LLaMA-3.1-70B, Qwen2.5-Coder-32B | BIRD + Spider | 70B BIRD dev / Spider test: SFT 58.1 / 81.4 -> off-policy 66.3 / 82.5 -> on-policy 68.5 / 86.6; on-policy only 66.3 / 84.2. SQL-only DPO 60.0 / 81.0, below SQL-only SFT 62.0 / 83.0 | Closest pair construction: teacher pairs as warm start, then on-policy rounds. Centralized, 32-70B, 64 H100. Venue not verified | full |
| SENSE, Yang et al., ACL 2024 ([ACL](https://aclanthology.org/2024.acl-long.425/)) | GPT-4 synthetic SFT data + DPO on execution-labelled pairs from a weak 1.3B model | CodeLLaMA-7B/13B | Spider, BIRD | DPO step adds +0.2 to +0.9 Spider dev EX, +1.9 to +2.6 BIRD dev; removing strong data costs 22-32 points | Strong data matters far more than the preference step at 7B+ | full |
| OmniSQL, Li et al., PVLDB 18(11) per header ([arXiv 2503.02240](https://arxiv.org/abs/2503.02240)) | SynSQL-2.5M with CoT; CoT-enhanced Spider + BIRD | Qwen2.5-Coder 7B-32B | Spider, BIRD, variants | 7B greedy, Spider test (TS): base 82.2, gold Spider+BIRD SFT 80.7, CoT Spider+BIRD 86.6; BIRD dev 50.9 / 55.1 / 59.6 | Plain gold SFT can lower Spider test below the base model; teacher CoT raises it. Student is 7B | full |
| CodeS, Li et al., SIGMOD 2024 ([arXiv 2402.16347](https://arxiv.org/abs/2402.16347)) | StarCoderBase incrementally pre-trained on 21.5 GB (11 GB SQL, 6 GB NL-to-code, 4.5 GB NL), then full-parameter SFT (4 epochs, batch 128, lr 5e-6, max length 4,096; no LoRA mentioned, DeepSpeed ZeRO-3, 8x A800). Prompt: trained schema item classifier (top 6 tables, top 10 columns), value retriever, representative values, PK/FK, comments. Decoding: beam 4, first executable candidate | 1B-15B | Spider, BIRD | SFT CodeS-1B, Spider dev EX / TS 77.9 / 72.2 (Table 5); Syn 66.5 / 59.3, Realistic 70.9 / 61.8, DK 64.7 (Table 7); BIRD dev EX 50.46 with evidence, 38.46 without (Table 6). No zero-shot and no Spider test number. Few-shot, before SFT, Spider dev TS: CodeS-1B 55.7 / 57.4 / 59.1 (1/3/5-shot), StarCoderBase-1B 43.7 / 46.8 / 48.6 (Table 4). 3B: dev EX 83.4 | Reference for Spider SFT at about 1B; differs in base model, SQL pre-training, full fine-tuning, schema filtering with values and execution-filtered beam search | full |
| SLM-SQL, Sheng and Xu, Findings IJCNLP-AACL 2025 ([ACL](https://aclanthology.org/2025.findings-ijcnlp.92/); [arXiv 2507.22478](https://arxiv.org/abs/2507.22478)) | SFT on SynSQL-Think-916K (filtered from SynSQL-2.5M; includes Spider and BIRD train with OmniSQL CoT), GRPO on BIRD train (9,428 rows), corrective self-consistency with a merge-revision model | Qwen2.5-Coder-0.5B/1.5B-Instruct (our checkpoint), Qwen3-0.6B, Llama-3.2-1B, DeepSeek-Coder-1.3B | SynSQL, BIRD; Spider only evaluated | Table 3, 1.5B, dev SC / CSC and test SC / CSC (16 samples): zero-shot 63.54 / 65.99 and 67.61 / 69.34; SFT 74.53 / 76.66 and 77.35 / 79.13; SFT+RL 75.15 / 76.72 and 78.42 / 79.06. BIRD dev 67.08 (CSC, 64 samples) | Targets BIRD: abstract, RL and ablations are BIRD; Spider is reported as transfer, though Spider train is in the SFT data. Training data about 50 times this project's. Every number uses sampling, none greedy; tables partly inconsistent | full |
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
greedy, single-sample, Spider-trained 1.5B Qwen2.5-Coder number.

Published Spider numbers at about 1.5B (read in full 2026-11-15). The
Qwen2.5-Coder technical report (Hui et al. 2024, [arXiv 2409.12186](https://arxiv.org/abs/2409.12186))
has no 1.5B Text-to-SQL result: its Figure 12 covers Instruct models from
7B up (7B Spider 82.0, BIRD 51.1; prompt with table content after Chang and
Fosler-Lussier). Think2SQL reports 1.5B on BIRD only.

| Paper | Model | Training data | Decoding | Zero-shot Spider | Best Spider |
|---|---|---|---|---|---|
| SPFT-SQL | Qwen2.5-Coder-1.5B | Spider train + synthetic rows per round (3K best at 7B), centralized; baseline SFT with LoRA | not stated | dev 72.4, test 72.3 | dev 79.7, test 82.3 |
| SQL-Factory ([arXiv 2504.14837](https://arxiv.org/abs/2504.14837), Table 4) | Qwen2.5-Coder-1.5B | Spider train ("+Official-Data"), or their synthetic queries; 3 epochs, lr 3e-6, batch 256 | not stated; split of "Spider" not named | 69.2 | Spider train 73.2; synthetic 76.5 |
| SLM-SQL | Qwen2.5-Coder-1.5B-Instruct | 916K CoT SFT (incl. Spider and BIRD train) + BIRD GRPO | 16 samples, SC / CSC | dev 63.54 / 65.99, test 67.61 / 69.34 | dev 75.15 / 76.72, test 78.42 / 79.06 |
| FINER-SQL | Qwen2.5-Coder-1.5B | Spider + BIRD, SFT + GRPO | schema ranker, 30-sample vote | not reported | dev 80.0 |
| MCTS-SQL ([arXiv 2501.16607](https://arxiv.org/abs/2501.16607), v3, Table 3) | Qwen2.5-Coder-1.5B-Instruct | none: training-free pipeline (schema selector, CoT few-shot generator, LLM verifier, MCTS refiner) | T 0.1, 2 children, 5 rollouts | not reported for Spider (BIRD dev single-shot 14.71) | dev 67.45, test 71.68 |
| CodeS-1B | StarCoderBase-1B + 21.5 GB SQL-centric pre-training | Spider train, full SFT | beam 4, first executable | not reported (few-shot dev TS 55.7-59.1) | dev 77.9 (TS 72.2) |

SPFT-SQL's baseline rows for this model (Table 1, read 2026-11-20; columns Spider dev EX,
test EX, then Syn, Realistic and DK EX): without training 72.4, 72.3, 55.7, 60.4, 62.0;
LoRA SFT (3 epochs, lr 2e-4, batch 64) 76.8, 78.0, 59.0, 64.8, 60.9; SPFT-SQL 79.7, 82.3,
66.7, 75.4, 67.3. Not used as a reference (owner, 2026-11-20): its untrained BIRD dev row
for this model, 40.6, is 11 to 13 points above Think2SQL, SLM-SQL, SQL-Factory and ours, and
the paper prints neither prompt nor decoding (`RESEARCH_STATE.md`, section 5.1).

Checked 2026-11-18 for further 1.5B Spider rows, none found: Think2SQL
(Spider table has 3B and 7B only; 3B 72.5 / SFT 77.0, 7B 77.6 / 82.6, BIRD-trained, T 0.7,
mean of 3 runs), the Qwen2.5-Coder report (section 7.4, figure only, 7B and up),
Text2SQL-Flow (arXiv 2511.10192, Table II: 7B and 8B only; Qwen2.5-Coder-7B-Instruct
Spider test greedy 82.2, vote of 8 at T 0.8 85.6; SFT on SQLFlow 85.1 / 86.6) and
SQuaD-SQL (WikiSQL only). Community LoRA repositories report 55-74 on Spider dev with
their own harnesses; not citable.

Zero-shot 1.5B Spider numbers range from 63.54 (dev, SC@16) to 72.4 (dev,
undisclosed prompt), so the paper must report its own zero-shot under each
prompt it uses. The large gaps come from training data volume (SLM-SQL,
CodeS) or from input processing with values and centralized training at a
similar data volume (SPFT-SQL).

Published BIRD dev numbers at 0.5B to 3B (searched 2026-11-20 by a search
agent that opened each arXiv HTML; the rows of SQL-Factory, SPFT-SQL,
SLM-SQL and Zhang et al. were read again in the saved text). "n.s." is not
stated in the parts read.

| Paper | Model | Training | Prompt, decoding | Zero-shot | Trained |
|---|---|---|---|---|---|
| SQL-Factory ([arXiv 2504.14837](https://arxiv.org/abs/2504.14837), Table 4) | Qwen2.5-Coder-1.5B | BIRD train ("+Official-Data"), 3 epochs, lr 3e-6, batch 256, max length 4,096, LLaMA-Factory defaults; LoRA or full n.s. | "official prompt templates for each model"; evidence and decoding n.s.; split of "Bird" not named | 28.6 | 39.2 (their synthetic data: 40.9) |
| same | Qwen2.5-Coder-3B; Llama-3.2-1B / 3B; DeepSeek-Coder-1.3B | same | same | 37.1; 11.3 / 30.1; 20.3 | 45.7; 26.0 / 38.9; 36.9 |
| SPFT-SQL ([arXiv 2509.03937](https://arxiv.org/abs/2509.03937), Table 1) | Qwen2.5-Coder-1.5B | training set of the benchmark, LoRA through LLaMA-Factory, 3 epochs, lr 2e-4, batch 64 | n.s. | 40.6 | SFT 44.3; SPFT-SQL 54.0 |
| SLM-SQL (Tables 2, 4, 6) | Qwen2.5-Coder-1.5B-Instruct | SFT on 916K CoT rows, then GRPO on BIRD train | schema with column descriptions and values; 64 samples | 28.40 (decoding n.s.); 46.81 with voting | SFT with voting 54.17; full 67.08 |
| FINER-SQL ([arXiv 2605.03465](https://arxiv.org/abs/2605.03465), Table II, section V-E) | Qwen2.5-Coder 0.5B / 1.5B / 3B | SFT on distilled reasoning traces, then GRPO | schema cut to 30 columns by a ranker; vote of 30 samples | no row | SFT only 42.9 / 59.4 / 63.4; final 50.85 / 63.17 / 67.73 |
| Think2SQL (Tables 1, 2) | Qwen2.5-Coder 0.5B / 1.5B / 3B | RL on BIRD train; SFT rows at 3B only (913 rows with reasoning traces) | gold tables in the schema; T 0.7, one sample, mean of 3 runs | 8.9 / 27.5 / 38.2 | RL 25.4 / 44.2 / 50.0; 3B SFT 42.7 without reasoning, 46.0 with |
| Reasoning-SQL (Table 3) | Qwen2.5-Coder-3B | SFT on 8,026 BIRD train rows, 3 epochs, lr 1e-5 | schema filtered by Gemini-1.5-pro | 45.17 | SFT 55.9; GRPO 58.67 |
| CSC-SQL ([arXiv 2505.13271](https://arxiv.org/abs/2505.13271), Table 1) | Qwen2.5-Coder-3B-Instruct | GRPO on BIRD train | schema with descriptions and values; T 0.8, vote of n | 44.70 (n = 4), 56.15 (n = 64) | 56.95 (n = 8), 63.34 (CSC, n = 64) |
| Query and Conquer ([arXiv 2503.24364](https://arxiv.org/abs/2503.24364), Table 1) | Qwen2.5-Coder-3B | none | schema with example values, evidence, CoT; greedy; a "validation subset" | 30.2 | no row |
| MCTS-SQL (Table 1) | Qwen2.5-Coder 1.5B / 3B | none | single shot; MCTS pipeline | 14.71 / 17.68 | pipeline 40.69 / 46.71 |
| CodeS (Table 6) | CodeS-1B / 3B | BIRD train, full SFT after SQL pre-training | schema classifier, value retriever; beam 4 | no row | with evidence 50.46 / 55.02; without 38.46 / 43.42 |

What this gives for our setup (Qwen2.5-Coder-1.5B, CREATE TABLE text
without rows, evidence, greedy, LoRA):

- Zero-shot: 27.5, 28.40 and 28.6 in three papers; ours 29.47. SPFT-SQL's
  40.6 stands alone and its prompt is not printed.
- Plain SFT on BIRD train: 39.2 (SQL-Factory) and 44.3 (SPFT-SQL), the
  only two rows at this size without added inputs or voting; neither
  states prompt and decoding in full, and SPFT-SQL's is on its 40.6
  baseline, so 39.2 is the one row kept as a reference. Our FedAvg SFT is at 38.85 and 42.70
  after 1 and 2 rounds.
- Every 1.5B number above about 45 adds inputs or inference we do not
  use: value retrieval and a schema classifier (CodeS), 916K rows and a
  vote of 64 (SLM-SQL), a schema ranker, distilled reasoning and a vote of
  30 (FINER-SQL).
- No paper found reports a greedy, single-sample, plain-DDL LoRA SFT of
  this model on BIRD with all four settings stated.

Second, short search (2026-11-25, search agent, numbers read in each
paper's table): no new 0.5B to 3B row on BIRD dev with plain CREATE TABLE
text, evidence, greedy and one sample. What it adds:

| Paper | Model | Setting | BIRD dev EX |
|---|---|---|---|
| ReSQL, ACL Findings 2026, Table 2 | Qwen2.5-1.5B-Instruct (general model) | LoRA SFT on BIRD train; schema with example rows and evidence; every row after two error-correction iterations | zero-shot 13.82, SFT 17.28 |
| KID ([arXiv 2410.11371](https://arxiv.org/abs/2410.11371), Table 3) | Qwen1.5-0.5B | LoRA SFT on BIRD train, CodeS-style prompt | 16.36 without evidence, 30.51 with; distillation up to 36.11 |
| SQL-R1 ([arXiv 2504.08600](https://arxiv.org/abs/2504.08600), Table 7) | Qwen2.5-Coder-3B | GRPO; column descriptions, CoT, vote of 8 | 50.5 to 54.6 |
| [arXiv 2606.29733](https://arxiv.org/abs/2606.29733), Table 2 | Qwen2.5-Coder-7B-Instruct | no training; table and column names plus evidence, greedy | 42.63 |
| OmniSQL ([arXiv 2503.02240](https://arxiv.org/abs/2503.02240), Table 4) | Qwen2.5-Coder-7B-Instruct | no training; descriptions and values, greedy | 50.9 |
| [arXiv 2607.22622](https://arxiv.org/abs/2607.22622), Table 1 | Qwen3-Coder-30B-A3B | LoRA SFT, then on-policy DPO (reference = SFT); filtered schema and matched contents; greedy | SFT 56.91, SFT + DPO 57.64 |

- The 1.5B levels stay those above: zero-shot 28.6 (SQL-Factory), SFT
  39.2 (SQL-Factory) and 44.3 (SPFT-SQL).
- No greedy single-sample DPO or RL row exists below 7B; the one greedy
  DPO-after-SFT row on BIRD dev gains 0.73 at 30B.
- No federated Text-to-SQL result on BIRD found again; OmniSQL, ExCoT,
  Alpha-SQL and the other recent SQL RL papers start at 6.7B or above.

Federated: no federated result on BIRD was found at any model size, and
no federated Text-to-SQL paper besides Zhang et al. (section 1.2; T5-base,
8 single-domain datasets as clients, exact match: centralized 70.32 /
74.21 macro / micro, FedAvg 40.03 / 57.89, FedOPT 58.32 / 68.49). Checked
without a hit: arXiv listing and API queries on federated Text-to-SQL,
NL2SQL and SQL generation; OpenFedLLM, FedLLM-Bench and FederatedScope-LLM
(no occurrence of "SQL"); the FlowerTune LLM leaderboard (no SQL task).
The papers citing Zhang et al. were not read (Semantic Scholar and DBLP
refused the requests).

Not opened: Text2SQL-Flow for BIRD rows below 7B; the model cards of
SQL-R1 (Qwen3-4B) and of community LoRA models. No row at this size in
OmniSQL, BASE-SQL and the BIRD mini-dev README.

### 1.5 LLM-to-SLM distillation

| Paper | Method | Sizes | Data | Key numbers | Closest point / main difference | Read |
|---|---|---|---|---|---|---|
| DistiLLM-2, Ko et al., ICML 2025 ([arXiv 2503.07067](https://arxiv.org/abs/2503.07067)) | Contrastive: skew KL up on teacher responses, skew reverse KL down on student responses | Qwen2.5-Coder-7B-Instruct -> Qwen2.5-Coder-1.5B (our exact pair) | WizardCoder prompts; HumanEval, MBPP | HumanEval / MBPP: student 30.7 / 60.8, GKD 40.9 / 61.9, DistiLLM-2 42.2 / 62.7 | Same model pair; training prompts differ from test distribution. Code, not SQL; the student row is the student after SFT on the gold responses (Appendix C.2, checked 2026-11-23), named without "Inst" in Table 4 | full |
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
Step-DPO ([arXiv 2406.18629](https://arxiv.org/abs/2406.18629), Table 4,
checked 2026-11-23): on MATH from Qwen2-7B-SFT at 54.8, chosen steps
corrected by GPT-4 (out of distribution for the policy) give 55.1 and
self-generated chosen steps 55.8; the rejected step is the model's own
wrong step in the paper's pipeline, and the page does not say so for the
GPT-4 row.

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
| DistiLLM-2 ([2503.07067](https://arxiv.org/abs/2503.07067)) | Table 4, Coder 7B -> 1.5B: HumanEval 30.73 -> 42.24, GKD 40.85; LoRA r16, 4x A100-80GB. Appendix D.1 (GPT-2, Dolly, ROUGE-L): on-policy 26.37, batched 26.20, off-policy 26.13 | The student is most likely the base checkpoint (30.7 vs the official base 43.9 and Instruct 70.7 in the Qwen2.5-Coder report); the checkpoint is inferred. Appendix C.2: every student is first trained with SFT on the gold responses and then distilled, so 30.73 is the row after gold SFT (checked 2026-11-23). On-policy adds little over off-policy | tables |
| KID ([2410.11371](https://arxiv.org/abs/2410.11371)) | Spider dev EX, Qwen1.5-0.5B with a 7B teacher: SFT 57.8, forward KL 57.3, reverse KL 61.5, GKD 64.3 (13.9x SFT time). TinyLLaMA: SFT 63.0, reverse KL 66.0, GKD 64.8, KID 68.1 | The teacher is fine-tuned on Spider (in-domain). Forward KL is about equal to SFT; reverse KL helps | tables |
| Reasoning-SQL ([2503.23157](https://arxiv.org/abs/2503.23157)) | Table 5, 7B Spider: base 77.85, BIRD gold SFT 68.08, GRPO 78.72 | Gold SFT on BIRD hurts Spider; execution RL on BIRD does not. Dev or test not stated | table |
| Think2SQL ([2504.15077](https://arxiv.org/abs/2504.15077)) | Table 4, 3B Spider 72.5 -> 77.0 | Needs both R1-reasoning SFT on 913 BIRD rows and QATCH-reward RL (T=0.7, 40 h on 8x H100); no 1.5B result | table |
| SLM-SQL ([ACL](https://aclanthology.org/2025.findings-ijcnlp.92/)) | Table 3, 1.5B Spider dev SC@16: zero-shot 63.54, SFT 74.53, SFT + BIRD RL 75.15; test SC@16 67.61, 77.35, 78.42 | BIRD RL adds +0.6 (dev) to +1.1 (test) on Spider once Spider is in the SFT data; no greedy numbers | table |
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

Timing: the reviewed sources do not provide a matched LLM comparison of a
server step after every round against one-time server training before FL
under this project's out-of-domain public-data setup.

What this means for the server step: on SQL-only greedy Spider EX, the
published gains from KD or RL on public data are about 1 point once the
student has seen Spider; larger KD gains need an in-domain teacher or a weak
base student. CoT training has the largest gains over gold SFT (OmniSQL), at
7B, but on Spider greedy CoT SFT alone stays below SQL-only SFT and moves
ahead only after execution-labelled DPO rounds (Liu et al., ExCoT).

### 1.8 Consistency as supervision and execution-only preference labels

These papers distinguish three signals: agreement among samples, successful
execution, and agreement with a gold result. They are different sources of
supervision. ScPO is the closest preference objective for training on vote
labels; ExeSQL is the closest SQL precedent for executes-versus-fails pairs.

| Paper / publication | Signal and scope | Evidence / relation to this setting | Read on 2026-11-14 |
|---|---|---|---|
| Prasad et al., **Self-Consistency Preference Optimization (ScPO)**, ICML 2025 ([paper](https://arxiv.org/abs/2411.04109)) | Preference pairs from answer-vote counts; consistency-weighted preference loss plus NLL; Llama-3 8B, math and logic | Table 1, GSM8K greedy after two iterations: ScPO 63.91, gold IRPO 64.29; semi-supervised ScPO 66.64. Sections 2-3 use k=8 at T=0.7 for math, with an additional 8 higher-temperature responses to find rejected answers when needed. Not an always-eight-sample recipe, and not SQL or FL | full, sections 2-5, Tables 1-5 |
| Zuo et al., **TTRL: Test-Time Reinforcement Learning**, arXiv 2025 ([paper](https://arxiv.org/abs/2504.16084)) | RL on majority-vote rewards without reference answers | Source of vote-reward training, including training on unlabelled test questions. The project can reuse the signal on training questions only; its test-time adaptation protocol conflicts with the project's data roles | abstract |
| Shafayat et al., **Can Large Reasoning Models Self-Train? (SRT)**, arXiv 2025 ([paper](https://arxiv.org/abs/2505.21444)) | Majority agreement supplies RL rewards on reasoning tasks | Reports improvement followed by reward hacking and collapse under prolonged self-training. Agreement is not an independent correctness check | abstract |
| Yu et al., **RESTRAIN: From Spurious Votes to Signals**, arXiv 2025 ([paper](https://arxiv.org/abs/2510.02172)) | Penalizes overconfident or low-consistency rollouts while using the answer distribution for label-free RL | A concrete treatment of wrong majorities; evidence is mathematical/scientific reasoning, not SQL result-set voting | abstract; conference venue not checked |
| Huang et al., **Self-Improvement in Language Models: The Sharpening Mechanism**, arXiv 2024 ([paper](https://arxiv.org/abs/2412.01951)) | Theory and experiments on amortizing inference-time verification through SFT/RLHF | Provides the sharpening/amortization framework. Similar aggregate accuracy before voting and after training does not establish that the same questions are solved | abstract; conference venue not checked |
| Gkountouras et al., **Consensus as Privileged Context for Label-Free Self-Distillation (CANON)**, arXiv 2026 ([paper](https://arxiv.org/abs/2607.13643)) | A frozen model conditioned on a majority-answer solution gives token-level supervision on student rollouts | An alternative to using consensus only as a scalar reward or preference; math/science, not execution-labelled SQL | abstract |
| Zhou et al., **Evolving Language Models without Labels (EVOL-RL)**, arXiv 2025, revised 2026 ([paper](https://arxiv.org/abs/2509.15194)) | Majority selection plus novelty and entropy terms | Identifies selection-induced diversity collapse, which matters when tracking pass@k as well as greedy accuracy | abstract |
| Zhang et al., **CodeDPO: Aligning Code Models with Self Generated and Verified Source Code**, ACL 2025 per authors' camera-ready record ([paper](https://arxiv.org/abs/2410.05605)) | Self-generated code and tests ranked jointly by a PageRank-inspired procedure; correctness and efficiency preferences | Prior preference learning without external test annotations. Its generated-test signal differs from execution against an existing SQL database | abstract |
| Liu et al., **DSTC: Direct Preference Learning with Only Self-Generated Tests and Code to Improve Code LMs**, arXiv 2024 ([paper](https://arxiv.org/abs/2411.13611)) | Self-generated tests/code, minimax selection and test-code concatenation; DPO/KTO | Another annotation-free code-preference precedent, not evidence for accurate SQL majority labels | abstract |
| Zhang et al., **ExeSQL: Self-Taught Text-to-SQL Models with Execution-Driven Bootstrapping for SQL Dialects**, Findings EMNLP 2025 ([ACL](https://aclanthology.org/2025.findings-emnlp.1320/); [body](https://arxiv.org/html/2505.17231v1)) | Execution-filtered synthesis and successful-versus-failed execution preferences for dialect adaptation; DeepSeek-Coder-7B, full fine-tuning, DPO plus SFT loss | Appendix A.4, Table 9: SFT to SFT+DPO, PostgreSQL 71.36 to 71.98, MySQL 70.34 to 72.86. These are dialect-adaptation results, not standard Spider-test greedy comparisons at 1.5B | sections 3.4, A.3-A.4, Table 9 |
| Pedrozo et al., **SQL-Zero: Self-Evolving Text-to-SQL**, arXiv 2026 ([paper](https://arxiv.org/abs/2609.04697)) | Proposer-solver self-play with GRPO and database execution, no annotated NL-SQL pairs; 3B/7B | A label-free SQL precedent with a different source of targets, the proposer's SQL. Its abstract reports BIRD-dev gains of 6.6/7.3 points over zero-shot. Main table, Spider test EX, greedy: Qwen2.5-Coder-3B zero-shot 68.0, a control trained on gold BIRD 74.4, self-play iterations 74.1 / 74.7 / 74.0; at 7B zero-shot 82.2, iterations 82.4 / 79.7 / 79.8 (only the first holds). About 820 GPU hours on H100 and B200; code in an anonymized repository. Not federated or vote-DPO evidence | full HTML, main table (2026-11-16) |

ScPO supports adapting consensus preferences to SQL, not assuming that a
vote equals a gold label. Result-set agreement can merge semantically
different SQL, including queries returning the same empty result (section
1.10). The reviewed corpus contains no matched federated 1.5B SQL experiment
establishing that vote-labelled DPO reproduces gold-labelled DPO.

### 1.9 Execution-based decoding and learned verification

| Paper / publication | Mechanism and scope | Evidence / relation | Read on 2026-11-14 |
|---|---|---|---|
| Shi et al., **Natural Language to Code Translation with Execution (MBR-EXEC)**, EMNLP 2022 ([paper](https://arxiv.org/abs/2204.11454)) | Selects candidates by agreement of execution outcomes; Spider, MBPP and NL2Bash | The direct source for execution-result voting/MBR, an inference procedure that does not update policy weights | abstract |
| Ni et al., **LEVER: Learning to Verify Language-to-Code Generation with Execution**, ICML 2023 ([paper](https://arxiv.org/html/2302.08468v3)) | A learned verifier sees question, program and execution result; combines verifier and generator probabilities and aggregates equivalent outcomes | Table 2, Spider dev with code-davinci-002: greedy 75.3, execution pruning plus likelihood 77.3, LEVER 81.9. The table's MBR-EXEC 75.2 is a previous-work row, not a matched ablation on this generator | sections 2-4, Table 2 |
| Sheng and Xu, **CSC-SQL: Corrective Self-Consistency in Text-to-SQL via Reinforcement Learning**, arXiv 2025 ([paper](https://arxiv.org/abs/2505.13271)) | GRPO-trained generator and revision model; revises the two most frequent candidate outputs | A multi-step decoding comparison, distinct from majority voting alone and from a single greedy student | abstract |
| Borchmann and Wydmuch, **Query and Conquer: Execution-Guided SQL Generation**, arXiv 2025 ([paper](https://arxiv.org/abs/2503.24364)) | Execution-result similarity selects semantically consistent SQL candidates | Relevant inference baseline; no 1.5B federated training evidence is established by the abstract | abstract |
| Richardson, **What Predicts Correctness in Text-to-SQL? A Selective-Prediction Study**, arXiv 2026 ([paper](https://arxiv.org/abs/2607.06799)) | Studies confidence signals and trained verifiers on BIRD/Spider | Abstract reports trained-verifier AUROC about 0.77-0.79 in distribution versus 0.66 on unseen schemas. This is ranking discrimination, not EX or a measured reranking gain | abstract |
| Chow et al., **Inference-Aware Fine-Tuning for Best-of-N Sampling in Large Language Models**, arXiv 2024 ([paper](https://arxiv.org/abs/2412.15287v1)) | Fine-tuning optimizes best-of-N deployment rather than greedy output | A separate objective for training/decoding interactions; math and code, not SQL | abstract, v1 |

Execution voting and learned verification add inference computation. A
training claim needs comparison under the same decoding protocol, alongside
greedy performance and pass@k. LEVER's previous-work MBR row cannot establish
that voting offers no gain for a particular strong generator.

### 1.10 Input grounding, semantic labels and synthetic SQL data

| Paper / publication | Mechanism and scope | Evidence / relation | Read on 2026-11-14 |
|---|---|---|---|
| Zhong, Yu and Klein, **Semantic Evaluation for Text-to-SQL with Distilled Test Suites**, EMNLP 2020 ([paper](https://arxiv.org/html/2010.02840v1)) | Generates and distils databases that separate non-equivalent queries | Table 2: single-database denotation accuracy has mean false-positive rate 6.5% across 21 Spider-dev submissions, 11.0% on extra-hard. These rates describe those submissions, not the error rate of this project's training pairs | full, sections 4-6, Table 2 |
| Pourreza and Rafiei, **Evaluating Cross-Domain Text-to-SQL Models and Benchmarks**, EMNLP 2023 ([paper](https://arxiv.org/abs/2310.18538)) | Manual and equivalence-based re-evaluation of questions, gold SQL and generated queries | Ambiguity, implicit assumptions and nondeterministic tied rows complicate scoring; the findings do not identify which of this project's errors are annotation errors | abstract |
| Klopfenstein et al., **SpotIt: Evaluating Text-to-SQL Evaluation with Formal Verification**, ICLR 2026 per authors' accepted record ([paper](https://arxiv.org/abs/2510.26840)) | Bounded equivalence verification searches for counterexample databases; BIRD | A stricter evaluation mechanism, not evidence that the same mechanism improves 1.5B DPO training | abstract |
| Zhu et al., **Human-Level Text-to-SQL via Reinforcement Learning on Verified Data, Without Pipeline Engineering**, arXiv 2026 ([paper](https://arxiv.org/abs/2603.20004)) | Expert-verified BIRD-Platinum data; ReViSQL-BIRD combines equivalence verification and process rewards | Separates training-data correction from reward changes. Abstract's 11-16% improvements concern Qwen3-235B on Arcwise-Plat/Spider2, not an isolated equivalence-reward ablation or a 1.5B Spider result | abstract, v4 |
| Chen et al., **GBV-SQL: Guided Generation and SQL2Text Back-Translation Validation for Multi-Agent Text2SQL**, ACL 2026 ([ACL](https://aclanthology.org/2026.acl-long.837/)) | Back-translates SQL to check alignment with the question | A semantic-validation pipeline, not a measurement of this project's residual-error ceiling | abstract |
| Li et al., **RESDSQL: Decoupling Schema Linking and Skeleton Parsing for Text-to-SQL**, AAAI 2023 ([paper](https://arxiv.org/abs/2302.05965)) | Ranks schema items before skeleton-aware seq2seq decoding | Supports schema grounding as a distinct component; encoder-decoder input restrictions differ from full-schema decoder prompts | abstract |
| Lin et al., **Bridging Textual and Tabular Data for Cross-Domain Text-to-SQL Semantic Parsing (BRIDGE)**, Findings EMNLP 2020 ([paper](https://arxiv.org/abs/2012.12627)) | Adds question-mentioned cell values to a joint question/schema representation | A source for value anchoring; no adaptation to the project's prompt is implied | abstract |
| Qin et al., **ROUTE: Robust Multitask Tuning and Collaboration for Text-to-SQL**, arXiv 2024, revised 2025 ([paper](https://arxiv.org/abs/2412.10138)) | Auxiliary schema-linking, noise-correction and continuation tasks, then multitask prompting | Programmatically related SQL tasks are an alternative to changing the preference loss; venue not verified on the opened record | abstract |
| Zhang et al., **SPFT-SQL: Enhancing Large Language Model for Text-to-SQL Parsing by Self-Play Fine-Tuning**, Findings EMNLP 2025 ([ACL](https://aclanthology.org/2025.findings-emnlp.59/); [body](https://arxiv.org/html/2509.03937v2)) | Verification-based iterative data synthesis (VBI-FT) followed by error-driven self-play; includes Qwen2.5-Coder-1.5B and CodeS-style schema processing | Table 1, 1.5B block (Spider dev EX / dev TS / test EX): zero-shot 72.4 / 62.5 / 72.3; SFT 76.8 / 70.2 / 78.0; SPIN 67.6 / 60.5 / 68.5; SPFT-SQL 79.7 / 73.5 / 82.3. Syn EX, Realistic EX, DK EX: SFT 59.0, 64.8, 60.9; SPFT-SQL 66.7, 75.4, 67.3. BIRD dev EX: SFT 44.3, SPFT-SQL 54.0. The SFT and zero-shot rows are the authors' own runs: the cited Hui et al. 2024 (Qwen2.5-Coder report) has no 1.5B Spider number. Appendix A.4: baseline SFT is LoRA through LLaMA-Factory, AdamW, batch 64, lr 2e-4, three epochs "on each training set"; LoRA rank, baseline prompt and decoding are not stated. Synthetic data per VBI-FT round is small: at 7B, 3,000 records was best and 10,000 slightly worse (Figure 4). Its SFT CodeS-1B row is copied correctly from CodeS. Centralized training differs from this project's data roles. The 7B SFT values 79.0 and 83.7 are dev TS and test EX respectively, not conflicting reports of one metric. Other anomalies in Table 1: 1.5B SFT DK below zero-shot (60.9 vs 62.0); 7B SFT dev EX below zero-shot (82.9 vs 83.5) | sections 3-4, Table 1, Appendix A.3-A.4 |
| Zhong et al., **Grounded Adaptation for Zero-shot Executable Semantic Parsing (GAZP)**, EMNLP 2020 ([paper](https://arxiv.org/html/2009.07396v3)) | Backward utterance generation plus cycle-consistency in a new database environment | Spider dev EX: baseline 55.4, GAZP 59.2 (Table 2); synthesis on train databases 52.1, no cycle filter 52.3 (Table 3). The successful adaptation uses evaluation environments; it is not permissible training on this project's test databases | sections 2-3, Tables 2 and 3 |
| Saparina and Lapata, **Improving Generalization in Semantic Parsing by Increasing Natural Language Variation**, EACL 2024 ([paper](https://arxiv.org/abs/2402.08666)) | LLM-generated question reformulations for robustness | Supports linguistic-variation analysis; the abstract alone does not establish a gain on unmodified Spider | abstract |
| Rączkowska et al., **RetrySQL: text-to-SQL training with retry data for self-correcting query generation**, arXiv 2025 ([paper](https://arxiv.org/abs/2507.02529)) | Corrupted and corrected reasoning steps for continued pretraining | Abstract explicitly reports LoRA SFT ineffective for its retry data and uses full-parameter pretraining. Its result does not justify a cheap LoRA-only replica | abstract; conference venue not checked |
| Chen et al., **SQLCritic: Correcting Text-to-SQL Generation via Clause-wise Critic**, arXiv 2025 ([paper](https://arxiv.org/abs/2503.07996)) | Clause-aware critiques, with adaptive-beta DPO for the critic | Preference training improves a separate critic, not the SQL generator directly | abstract |
| Hoang et al., **FINER-SQL: Boosting Small Language Models for Text-to-SQL**, arXiv 2026 ([paper](https://arxiv.org/abs/2605.03465)) | SFT on a reasoning bank (2 epochs, lr 2e-5), then GRPO with memory and operation-level atomic rewards (32 rollouts, lr 8e-6, 2x A6000). Inference: GRAST-SQL 0.6B schema ranker (top 30 columns), 30 candidates, majority vote. Trained only on Spider and BIRD databases | Table II, Qwen2.5-Coder 0.5B / 1.5B / 3B (Instruct not stated): BIRD dev EX 50.85 / 63.17 / 67.73, Spider dev EX 70.2 / 80.0 / 85.0. No Spider test and no zero-shot Spider number; BIRD dev 0.5B rises from 35 greedy to about 49 at T 1.0 (Figure 6). A fine-grained reward alternative with a 30-sample vote, not a matched greedy 1.5B comparison | sections IV-V, Table II, Figures 6 and 10 |
| Chen et al., **DualSQL: Text-to-SQL with Multi-Agent Reinforcement Learning**, arXiv 2026 ([paper](https://arxiv.org/abs/2609.18135)) | Shared-backbone schema-linking and SQL agents; robust execution match (REX) rewards | Another semantic-reward precedent, at 4B/8B with database tools rather than one SQL-only greedy policy | abstract |

CodeS (section 1.4) remains the main input-component reference. Its
representative values, value retrieval, keys and schema filtering need to be
separated when describing a prompt. Neither benchmark-audit percentages nor
another system's cleaned-set score estimates how many errors of this model
are fixable; that requires an audit of this model's own questions.

### 1.11 Distillation controls, public-data training and later optimization

| Paper / publication | Mechanism and scope | Evidence / relation | Read on 2026-11-14 |
|---|---|---|---|
| Yuan et al., **Revisiting Knowledge Distillation via Label Smoothing Regularization**, CVPR 2020 ([paper](https://arxiv.org/abs/1909.11723)) | KD as learned label smoothing; self-teaching and manually specified virtual teachers | Published basis for comparing teacher logits with teacher-free soft targets. Vision results motivate a control, not a conclusion about SQL transfer | abstract |
| Piskorz et al., **On-Policy or Off-Policy Learning? A Systematic Study of Distillation Dynamics**, arXiv 2026 ([paper](https://arxiv.org/html/2609.35259v1)) | Separates rollout policy, KL direction and learning rate for Llama/Qwen strong-to-weak KD | Section 5: forward KL has higher pass@10 at similar pass@1 on Countdown-3. Subsequent RLVR favors some off-policy starts; reverse-KL checkpoints collapse at LR 1e-5, but an off-policy reverse-KL start at 5e-5 also performs strongly. This is not a universal forward-KL advantage after reward training | sections 4-5, Figures 5-6 and discussion of Figure 26 |
| Zhang et al., **Towards the Law of Capacity Gap in Distilling Language Models**, ACL 2025 ([paper](https://arxiv.org/abs/2311.07052)) | Studies non-monotonic teacher-size effects and an empirical optimal-teacher scaling law | A stronger teacher need not yield a better student. Its fitted law is not a teacher-size prescription for Qwen SQL post-training | abstract |
| Peng et al., **Pre-training Distillation for Large Language Models: A Design Space Exploration**, arXiv 2024 ([paper](https://arxiv.org/abs/2410.16215)) | Teacher logits, losses, scale and offline/online KD in pretraining; 1.9B student in the initial study | Adjacent evidence about KD design; pretraining gains cannot be assumed to persist through this project's SFT and DPO stages | abstract; venue not verified on opened record |
| Wu et al., **Rethinking Kullback-Leibler Divergence in Knowledge Distillation for Large Language Models (AKL)**, COLING 2025 ([paper](https://arxiv.org/abs/2404.02657)) | Adaptive mixture of forward/reverse KL during finite training | A divergence alternative; no matched post-DPO SQL result established here | abstract |
| Liu et al., **Understanding Knowledge Distillation in Post-Training: When It Helps and When It Fails**, arXiv 2026 ([paper](https://arxiv.org/abs/2606.22942)) | Tulu 3 KD/SFT comparisons across data volume and teacher strength | KD's advantage shrinks with more data; a stronger instruction teacher can restore it. This is a different task regime from frozen-teacher BIRD-to-Spider transfer | abstract |
| Busbridge et al., **Distillation Scaling Laws**, ICML 2025 ([paper](https://arxiv.org/abs/2502.08606)) | Compute allocation between teacher/student, including existing-teacher and newly trained-teacher cases | Distillation benefit depends on student size and total compute; no Text-to-SQL-specific optimum | abstract |
| Li et al., **Small Models Struggle to Learn from Strong Reasoners**, arXiv 2025 ([paper](https://arxiv.org/abs/2502.12143)) | Studies CoT complexity and mixes short/long or weaker/stronger-teacher reasoning | Models up to 3B do not consistently benefit from long CoT; this concerns reasoning-trace distillation rather than a general failure of teacher logits | abstract |
| Chen et al., **SODA: Semi On-Policy Black-Box Distillation for Large Language Models**, Efficient Reasoning at COLM per authors' comment ([paper](https://arxiv.org/abs/2604.03873)) | Contrasts teacher outputs with a static snapshot of student responses | Distillation without refreshing rollouts at every step; no evidence here about a later SQL preference stage | abstract |
| Yang et al., **Learning beyond Teacher: Generalized On-Policy Distillation with Reward Extrapolation**, arXiv 2026 ([paper](https://arxiv.org/abs/2602.12125)) | Separates reward scaling and reference policy in OPD; math/code | Student-beyond-teacher results under this objective do not establish gains from simply enlarging the teacher in Hinton KD | abstract |
| Cai et al., **Text2SQL-Flow: A Robust SQL-Aware Data Augmentation Framework for Text-to-SQL**, arXiv 2025, revised 2026 ([paper](https://arxiv.org/abs/2511.10192)) | SQL-aware synthesis, execution checks, NL-SQL correspondence verification and CoT; releases SQLFlow | Data-quality precedent; no matched 1.5B BIRD/SynSQL initialization followed by federated DPO is established by its abstract | abstract |
| Hoang et al., **Distill-C: Enhanced NL2SQL via Distilled Customization with LLMs**, NAACL 2025 Industry Track ([paper](https://arxiv.org/abs/2504.00048)) | Teacher-generated synthetic data customized to NL2SQL domains | A teacher-correction/customization precedent; its teacher access and centralized data synthesis differ from the server-only public-data rule | abstract |

For initialization and timing, [Chen et al., ICLR 2023](https://arxiv.org/abs/2206.11488)
find that pretraining stabilizes aggregation and narrows the FL-centralized
gap on vision tasks without eliminating local drift; [Nguyen et al.](https://arxiv.org/abs/2210.08090)
study reduced sensitivity to data/system heterogeneity from pretrained
starts. [Mai et al.](https://arxiv.org/abs/2210.02614) study auxiliary server
learning even with a distribution different from the clients'. These three
abstracts were checked; none establishes the best placement of a frozen
teacher's public-data step in a federated SQL-DPO pipeline.

### 1.12 Recent federated objectives, aggregation and evaluation protocols

The names **FGRPO**, **Fed-GRPO** and **FedGRPO** below denote distinct
papers. A baseline called FedGRPO inside FedMOA means local GRPO plus
FedAvg, not Zhu et al.'s server-training method.

| Paper / publication | Mechanism and setup | Evidence / relation | Read on 2026-11-14 |
|---|---|---|---|
| Chen et al., **FGRPO: Federated GRPO with Adaptive Aggregation on Non-IID Data**, arXiv 2026 ([body](https://arxiv.org/html/2606.03094)) | Aggregation from reward improvement relative to a client EMA baseline; vision-language math, primarily 5 clients | Table 3 isolates progress weighting: Open-R1 40.66 to 41.86, GEOQA 38.66 to 40.76. Uses Qwen-VL-family models, not SQL decoders; appendix varies client count and heterogeneity | sections 4.2-4.3, Table 3, Appendix D.4 |
| Zhu et al., **FedGRPO: Privately Optimizing Foundation Models with Group-Relative Rewards from Domain Client**, AAAI 2026 oral per authors' comment ([paper](https://arxiv.org/abs/2602.12014)) | A competence graph selects client experts to return scalar rewards on server candidates | Trains a server foundation model rather than a client-trained deployed SLM; no raw-data exchange is a different structural design from model-update FL | abstract |
| Jiang, **Distributed Direct Preference Optimization**, arXiv 2026 ([paper](https://arxiv.org/abs/2605.20696)) | Federated/decentralized DPO convergence and time complexity under drift and preference heterogeneity | Theory context; not execution-labelled Text-to-SQL evidence | abstract |
| Srewa et al., **A Systematic Evaluation of Preference Aggregation in Federated RLHF for Pluralistic Alignment of LLMs**, NeurIPS 2025 workshop per authors' comment ([paper](https://arxiv.org/abs/2512.08786)) | Historical alignment performance weights group rewards in PPO | Human preference conflict differs from a common SQL correctness criterion | abstract |
| Nourzad et al., **FIRM: Federated In-client Regularized Multi-objective Alignment for Large Language Models**, arXiv 2025 ([paper](https://arxiv.org/abs/2511.16992)) | Local multi-objective regularization against disagreement drift | A preference-conflict method, not a demonstrated correction for SQL execution labels | abstract |
| Wang et al., **Beyond Client Clustering: Fine-Grained Preference Alignment in Federated RLHF via Self-Evolving Routing (FedPrism)**, IJCAI 2026 ([proceedings](https://ijcai.org/proceedings/2026/552)) | Per-instance routing to preference experts with routing learned from expert losses | A close successor to preference-selector federation; different from local execution-labelled policy DPO | proceedings abstract |
| Abourayya et al., **Beyond Parameter Aggregation: Semantic Consensus for Federated Fine-Tuning of LLMs**, arXiv 2026 ([paper](https://arxiv.org/abs/2605.11857)) | Client generations on public prompts form consensus pseudo-labels | Public-prompt behavioral exchange differs from private-database execution-result clusters | abstract |
| Du et al., **Data Quality Control in Federated Instruction-tuning of Large Language Models (FedDQC)**, arXiv 2024 ([paper](https://arxiv.org/abs/2410.11540)) | Client instruction-response quality scores and easy-to-hard training | A quality-control precedent without a task execution verifier | abstract |
| Gao et al., **FlowerTune: A Cross-Domain Benchmark for Federated Fine-Tuning of Large Language Models**, NeurIPS 2025 Datasets and Benchmarks ([proceedings](https://proceedings.neurips.cc/paper_files/paper/2025/hash/563991b5c8b45fe75bea42db738223b2-Abstract-Datasets_and_Benchmarks_Track.html); [body](https://arxiv.org/html/2506.02961v2)) | 26 models across four domains; Code-Alpaca has 10 clients, 2 per round, 15 rounds; MBPP/HumanEval/MultiPL-E | Tables 7-8, Qwen2.5-7B base with DoRA: coding average FedAvg 45.25, FedProx 44.65, FedAvgM 46.77, FlexLoRA 43.47. This is neither a Coder-model nor a LoRA-only comparison | sections 2-4.3, Tables 1-2, 7-8 |
| Zhang et al., **FedRot-LoRA: Mitigating Rotational Misalignment in Federated LoRA**, ICML 2026 ([PMLR](https://proceedings.mlr.press/v306/zhang26cc.html)) | Orthogonally aligns low-rank factors before averaging | Addresses LoRA-factor aggregation error on NLU/generation; no DPO-specific effect established here | proceedings abstract |
| Bian et al., **LoRA-FAIR: Federated LoRA Fine-Tuning with Aggregation and Initialization Refinement**, ICCV 2025 per authors' comment ([paper](https://arxiv.org/abs/2411.14961)) | Corrects factor aggregation and refines initialization; vision models | Related aggregation mechanism, not direct SQL evidence | abstract |
| Jhunjhunwala et al., **FedRPCA: Enhancing Federated LoRA Aggregation Using Robust PCA**, arXiv 2025 ([paper](https://arxiv.org/abs/2506.01194)) | Shared low-rank plus client-specific sparse update components | Reports high cosine similarity of client updates; motivates measuring actual update differences before attributing gains to drift reduction | abstract |
| Huang et al., **Stabilized Fine-Tuning with LoRA in Federated Learning: Mitigating the Side Effect of Client Size and Rank via the Scaling Factor (SFed-LoRA)**, arXiv 2026 ([paper](https://arxiv.org/abs/2603.08058)) | Scaling rule for client-count/rank-induced instability | Adjacent LoRA aggregation evidence, not an execution-DPO control | abstract |
| Singh et al., **Learning to Collaborate: An Orchestrated-Decentralized Framework for Peer-to-Peer LLM Federation (KNEXA-FL)**, AAAI 2026 per authors' comment ([paper](https://arxiv.org/abs/2601.17133)) | Bandit-based peer matching and distillation among PEFT code agents | Federated code precedent without a central model-update aggregator | abstract |

Updated evidence for existing entries in section 1.3:

- **Fed-GRPO**, [Table 4](https://arxiv.org/html/2610.11502): average 37.10
  with size-weighted FedAvg, 38.01 with reward-standard-deviation weighting,
  39.07 after reward calibration, 39.06 after sparse communication. The
  isolated weighting effect is 0.91 points, not the full method's gain.
- **FedMOA**, [Table 1](https://arxiv.org/html/2602.00453): uses
  Qwen2.5-1.5B-Instruct (not Coder), 10 clients and 3 rounds in main math
  runs, 15 clients in mixed-task runs. In Heter+Heter, MATH rises from 62.6
  to 64.8 and HumanEval from 50.61 to 52.44 against local GRPO plus FedAvg.
- **pFedDPO**, [Jiang and Sarkar](https://arxiv.org/abs/2610.12885): the
  existing entry is *Personalized Federated Direct Preference Optimization
  via LoRA Adapters*, AAAI Fall Symposium Series 2026 per authors' comment;
  shared base synchronization and private personalized adapters.

Client pair-count weighting matches the weighting of a per-pair empirical
objective. Multiple local optimizer steps followed by parameter averaging
are not identical to centralized DPO. Similarly, [DAPO's dynamic sampling](https://arxiv.org/html/2503.14476)
filters groups after current rollouts; it does not establish lossless future
sampling skips from cached outcomes. [Lanchantin et al.](https://arxiv.org/abs/2506.21495)
compare offline, semi-online and online DPO/GRPO, finding the latter two
stronger than offline on math/instruction following. Resampling in each FL
round requires client compute even when it adds no communication round.

### 1.13 Privacy of updates, preference data and deployed models

| Paper / publication | Threat or finding | Boundary relevant here | Read on 2026-11-14 |
|---|---|---|---|
| Bossy et al., **Mitigating Unintended Memorization with LoRA in Federated Learning for LLMs**, TMLR 2026 ([paper](https://arxiv.org/abs/2502.05087)) | Compares unintended memorization under LoRA and full fine-tuning | Reduced memorization is not a formal privacy guarantee or proof of no cross-client extraction | abstract |
| Feng et al., **Exposing Privacy Gaps: Membership Inference Attack on Preference Data for LLM Alignment**, AISTATS 2025 ([PMLR](https://proceedings.mlr.press/v258/feng25a.html)) | Membership inference on preference data; DPO more vulnerable than PPO in the tested setting | Relevant to preference-data exposure, not a demonstrated attack on federated SQL updates | proceedings abstract |
| Hu et al., **Simple Yet Effective: Extracting Private Data Across Clients in Federated Fine-Tuning of Large Language Models**, Findings IJCNLP-AACL 2025 ([ACL](https://aclanthology.org/2025.findings-ijcnlp.113/)) | Semi-honest participant extracts other clients' memorized PII using local context | Chinese legal-domain benchmark, not SQL-specific; global-model leakage remains possible without raw-data uploads | proceedings abstract |
| Guo et al., **Can Federated Learning Safeguard Private Data in LLM Training? Vulnerabilities, Attacks, and Defense Evaluation**, Findings EMNLP 2025 per authors' comment ([paper](https://arxiv.org/abs/2509.20680)) | Extraction from global models and update tracking | Model-update isolation and model-output exposure are separate concerns | abstract |
| Petrov et al., **DAGER: Exact Gradient Inversion for Large Language Models**, arXiv 2024 ([paper](https://arxiv.org/abs/2405.15586)) | Honest-but-curious server with gradient access reconstructs text | Its observed gradients differ from this project's multi-epoch LoRA adapter updates | abstract |
| Sami et al., **MineGrad: Gradient Inversion Attacks on LoRA Fine-Tuning**, AISTATS 2026 ([PMLR](https://proceedings.mlr.press/v300/sami26a.html)) | Malicious server manipulates the model/initialization to enable inversion | Stronger attacker than an honest-but-curious aggregator; not proof of extraction under the project's training schedule | proceedings abstract |
| Liu et al., **SAFENLIDB: A Privacy-Preserving Safety Alignment Framework for LLM-based Natural Language Database Interfaces**, AAAI 2026 extended version per authors' comment ([paper](https://arxiv.org/abs/2511.06778)) | DPO-based safety alignment against database-interface attacks | Deployment-time access and disclosure risks, distinct from federated update leakage | abstract |

The privacy statement remains structural: questions, SQL, databases and
execution results stay at their clients; model updates are exchanged.
The cited attacks preclude inferring differential privacy or resistance to
memorization, membership inference or inversion from that structure alone.

### 1.14 Recent journal articles on SQL, query distillation and federated LoRA

These are related-work examples from the journal-article survey. Their
publication does not estimate acceptance probability or select a venue for
this paper. Abstract-only entries do not support claims that an article
lacks seeds, ablations or baselines.

| Paper / publication | Mechanism and relation | Read on 2026-11-14 |
|---|---|---|
| Tritto et al., **GradeSQL: Outcome reward models for intelligent Text-to-SQL generation from LLMs**, JIIS 2026 ([publisher](https://link.springer.com/article/10.1007/s10844-026-01071-6)) | Execution-labelled outcome verifiers rank SQL candidates. RQ3 text reports Spider test 87.47 versus majority voting 85.47 at N=32. Separate generator/verifier inference, not policy DPO; directly relevant beside LEVER | full HTML methods/results, RQ3 text; standalone table endpoint unavailable |
| Yi and Chen, **SKT-SQL: multi-decoupling and skeleton prompt framework for text-to-SQL on small-scale LMs**, JIIS 2025 ([publisher](https://link.springer.com/article/10.1007/s10844-025-00963-3)) | Schema selection, SQL skeleton and T5 slot filling; execution-guided beam search. Small-model SQL precedent with a different architecture | abstract |
| Xu et al., **PPR-SQL: a robust text-to-SQL system via probabilistic graph pruning and multi-view reasoning**, JIIS 2026 ([publisher](https://link.springer.com/article/10.1007/s10844-026-01049-4)) | PageRank on foreign-key links, multi-view reasoning, value grounding and reranking; ensemble inference on BIRD | abstract |
| Zhang et al., **Enhancing SQL generation through high-quality logical guidance (LU-SQL)**, JIIS 2026 ([publisher](https://link.springer.com/article/10.1007/s10844-026-01032-z)) | Question skeletons and interpreted representations retrieve logical examples and schema-linking experience | abstract |
| Li et al., **Mitigating LLM hallucinations in Text-to-SQL parsing with a self-refinement feedback loop and memory augmentation (SRFL)**, JIIS 2026 ([publisher](https://link.springer.com/article/10.1007/s10844-026-01050-x)) | Memory and feedback extend DIN-SQL/DAIL-SQL; inference refinement rather than local preference training | abstract |
| He et al., **OilRAGSQL: A RAG-based large language model framework for NL2SQL tasks in oilfield data analysis**, JIIS 2026 ([publisher](https://link.springer.com/article/10.1007/s10844-026-01055-6)) | Domain benchmark, terminology/schema knowledge base, two-hop retrieval and reranking | abstract |
| Zhao et al., **MTC-SQL: a memory-enhanced and task-decomposed correction method for text-to-SQL**, IJDSA 2026 ([publisher](https://link.springer.com/article/10.1007/s41060-025-00995-6)) | Decomposition, schema/QA memory, retrieval and recursive correction with GPT-4 on Spider | abstract |
| Eckmann et al., **HLR-SQL: Human-like reasoning for Text-to-SQL with the human in the loop**, Information Systems 138 (2026), 102670 ([author institution](https://www.dfki.de/web/forschung/projekte-publikationen/publikation/17167)) | Incremental SQL composition/testing and optional human feedback; Spider-HJ varies join complexity. DOI 10.1016/j.is.2025.102670 | author-institution metadata and PDF introduction/methods |
| Jain and Verma, **Hierarchical aggregation framework for federated LoRA fine-tuning under heterogeneous and non-IID devices**, Wireless Networks 2026 ([publisher](https://link.springer.com/article/10.1007/s11276-026-04225-0)) | Update clustering, weighted LoRA stacking and SVD fusion; RoBERTa/DeBERTa on SST-2/QNLI, not DPO | abstract |
| Wu et al., **Communication-efficient heterogeneous federated learning for large language models: federated asymmetric adaptive LoRA fine-tuning (Fed-A2LoRA)**, IJMLC 2026 ([publisher](https://link.springer.com/article/10.1007/s13042-026-03286-z)) | One-factor training, diagonal pruning and communication-budget adaptation; NLU/NLG | abstract and passages around Tables 15-16 |
| Chen and Su, **PFDP: privacy-preserving federated distillation method for pretrained language models**, IJMLC 2025 ([publisher](https://link.springer.com/article/10.1007/s13042-025-02612-1)) | Local DP distillation and transfer aggregation for classification; an explicit privacy mechanism beyond data isolation | abstract |
| Chong et al., **Distilcyphergpt: enhancing large language models for knowledge graph question answering in cypher through knowledge distillation**, DMKD 2025 ([publisher](https://link.springer.com/article/10.1007/s10618-025-01157-9)) | Natural-language-to-Cypher KD on knowledge graphs, adjacent to SQL generation but not relational SQL or FL | abstract |
| Lin et al., **NL2SQL with partial missing metadata based on multi-view metadata graph compensation and reasoning**, Applied Intelligence 2024 ([publisher](https://link.springer.com/article/10.1007/s10489-023-05221-z)) | Graph completion compensates missing metadata; Spider with modified metadata | abstract |
| Wen et al., **UCP: a unified framework for code generation with pseudocode-based multi-task learning and reinforcement alignment**, Journal of Supercomputing 2025 ([publisher](https://link.springer.com/article/10.1007/s11227-025-07487-1)) | Pseudocode/code multitask training and reinforcement alignment; adjacent code-generation evidence | abstract |
| Hu et al., **Enhancing large language models for scientific entity recognition via fully automated self-distillation**, IJDSA 2026 ([publisher](https://link.springer.com/article/10.1007/s41060-026-01110-z)) | High-confidence pseudo-label filtering and fine-tuning; adjacent self-labelling evidence without SQL execution | abstract |

### 1.15 Weak supervision, semi-supervised learning and conversational data

| Paper / publication | Supervision and relation | Read on 2026-11-14 |
|---|---|---|
| Guo et al., **Improving Few-Shot Text-to-SQL with Meta Self-Training via Column Specificity (MST-SQL)**, IJCAI 2022 ([proceedings](https://ijcai.org/proceedings/2022/576)) | Confidence-weighted pseudo-labels for single-table few-shot SQL, not an execution-vote preference objective | proceedings abstract |
| Wolfson et al., **Weakly Supervised Text-to-SQL Parsing through Question Decomposition**, Findings NAACL 2022 ([paper](https://arxiv.org/abs/2112.06311)) | Learns without SQL annotations but with QDMR structures and gold answers; this is weak supervision, not absence of correctness labels | abstract |
| Liao et al., **LearNAT: Learning NL2SQL with AST-guided Task Decomposition for Large Language Models**, ICLR 2026 per authors' accepted record ([paper](https://arxiv.org/abs/2504.02327)) | Verifiable AST-guided decomposition and margin-aware optimization; adjacent structured-reasoning work. The earlier report's semi-supervised appendix numbers were not rechecked and are not transferred | abstract, revised 2026 record |
| Abourayya et al., **Little is Enough: Boosting Privacy by Sharing Only Hard Labels in Federated Semi-Supervised Learning (FedCT)**, arXiv 2023, revised 2024 ([paper](https://arxiv.org/abs/2310.05696)); AAAI 2025 per a search listing, not verified on the page | Clients exchange hard labels on public unlabelled data; consensus supplies local pseudo-labels, including LLM fine-tuning experiments | abstract |
| Diao et al., **SemiFL: Semi-Supervised Federated Learning for Unlabeled Clients with Alternate Training**, arXiv 2021, revised 2022 ([paper](https://arxiv.org/abs/2106.01432)) | Small labelled server dataset with completely unlabelled clients; vision SSL, a different data-role assignment from labelled Spider clients | abstract |

[SParC](https://arxiv.org/abs/1906.02285) (ACL 2019) and
[CoSQL](https://arxiv.org/abs/1909.05378) (EMNLP 2019) are annotated
conversational SQL datasets, not naturally unlabelled question logs. Their
abstracts were checked. Context-dependent turns and database/split overlap
need examination before treating their questions as extra client data;
matching counts of databases do not establish identical split membership.

### 1.16 Mechanisms that could be added to the core (read 2026-11-16)

Read through page fetches of the arXiv HTML; "verbatim" names the tables
and sections whose text was obtained in full, "summary" the parts known
only from a machine summary of the page (not to be cited without a check).

| Paper | Mechanism and setup | Evidence | Relation | Read |
|---|---|---|---|---|
| Tao et al., **CodeLutra: Boosting LLM Code Generation via Preference-Guided Refinement**, [arXiv 2411.05199v3](https://arxiv.org/abs/2411.05199), TMLR 2025 (arXiv comment field; [ML Anthology](https://mlanthology.org/tmlr/2025/tao2025tmlr-codelutra); OpenReview id `IGsEgWM4to`) | Iterative on-policy preference training: each iteration samples 10 responses per question at T 1.0, labels them by execution against the gold result, pairs a self-generated correct sample with a failed one (K = 10 pairs per question), trains DPO + lambda x SFT on the chosen side (beta 0.1, lambda 1.0 for SQL), reference = previous iteration. Llama-3-8B, LoRA r=8, lr 5e-5, 1 epoch per iteration, 4 iterations. SQL-only examples. Centralized | Table 1, EX (split not stated; evaluation samples at T 0.2): Spider base 59.3, SFT 67.9, iterations 67.8 / 72.4 / 76.6 / 76.3; BIRD 22.3, SFT 35.6, iterations 37.8 / 40.8 / 43.1 / 42.6. Table 2: DPO term alone 17.2 on Spider against 76.6. Table 3: Gemma-7B 49.9 to 72.6, StarCoder-7B 61.2 to 77.5 on Spider. Section 5.3: without negatives the curve stays near the baseline (figure only). Section 6: non-executable outputs among 100 BIRD errors fall from 40% to 11%. Labels by executability alone, no gold: BIRD 22.3 to 30.9 | The closest published recipe to the core (on-policy, execution-labelled, DPO + SFT, SQL-only, saturating at iteration 3 to 4, gain in executable SQL), centralized at 7-8B. It is counter-evidence to "SQL-only DPO gives no gain at 7B+" (Liu et al., ExCoT), with weak SFT baselines. Different here: federated, 1.5B, gold as the chosen side when no sample is correct, and the DPO term alone does not collapse (76.76 against 76.71). The paper has no model below 7B, no seed count and no code link; its checkpoint table names StarCoder-15B and a Llama-3-8B-Instruct checkpoint against the 7B StarCoder and base Llama-3-8B of the text | verbatim, whole page; figures not read |
| Zhang et al., **SPFT-SQL** (section 1.10), ablations | Verified synthesis (VBI-FT): SQL templates extracted by an unnamed LLM, slots filled with random type-compatible columns and random database values on training schemas; an iteratively fine-tuned SQL-to-Text model writes the question (Qwen2.5-Coder-7B in appendix A.10; the writer for the 1.5B row is not stated); rows are split by executing the trained model's SQL against the synthetic SQL. Self-play: a logistic (DPO-like) loss against an opponent checkpoint with execution-labelled wrong SQL. SFT uses schema filtering and value matching after CodeS | Table 2, Qwen2.5-Coder-7B, Spider dev EX / test EX / BIRD dev EX: base 83.5 / 81.5 / 51.5; full 87.2 / 87.4 / 61.0; without VBI-FT 83.9 / 83.6 / 54.2; without self-play 86.6 / 86.8 / 60.3. Table 14: SFT on 7,000 rows 83.7 Spider test; 7,000 real + 3,000 synthetic 87.4; 1 h 45 min per iteration on 2 GPUs. Table 7, synthetic rows per round, Spider test: 0: 81.5, 1,000: 86.9, 3,000: 87.4, 10,000: 86.5. Table 8: synthesis accounts for the gains on Syn, Realistic and DK as well | Verified synthesis on training databases carries almost the whole gain (+3.1 over SFT on Spider test at 7B); the self-play preference stage adds 0.6. No paper combines such synthesis with an on-policy DPO stage of CodeLutra's strength; none is federated. The synthetic SQL follows a template method cited as "Hu et al. (2023)", probably Zhao et al., arXiv 2212.08785 (section 1.17; the match is not verified). No 1.5B ablation, no code link and no seed count on the page | verbatim, whole page; figures not read |
| Yan et al., **Learning to Reason under Off-Policy Guidance (LUFFY)**, [arXiv 2504.14945](https://arxiv.org/abs/2504.14945), venue not stated | GRPO with 1 teacher trace (DeepSeek-R1) and 7 on-policy rollouts per prompt, policy shaping on the off-policy term. The teacher traces are on the training prompts | Table 3, Qwen2.5-Math-1.5B, six-benchmark average: on-policy RL 30.0, SFT on the teacher traces 31.9, LUFFY 38.0. Table 1, 7B: 45.5 / 44.1 / 50.1. Table 4, 7B: mixing without shaping 44.4, below on-policy RL | A teacher candidate in the group helps a 1.5B student, but only with shaping, and the teacher answers the training prompts themselves, which the data rule here allows only for public questions | verbatim, tables 1, 3, 4 |
| MATS, [arXiv 2512.18622](https://arxiv.org/abs/2512.18622), venue not stated | Multi-agent pipeline of small models (planner LLaMA-3.2 3B) trained with iterative ORPO on execution-labelled samples (K = 10: one greedy, nine at T 1.0 per section 5.1; section 4.2 instead names one GPT-4o-mini candidate) | Section 5.5, planner, greedy: BIRD dev 53.65 to 59.32, Spider dev 83.3 to 85.4. Table 6, iteration 1: SFT 53.65, + DPO 44.98, + ORPO 56.32 | On-policy execution preference at 3B; plain DPO without an SFT term loses, as in CodeLutra. The paper contradicts itself on whether a stronger model's candidate is in the pool | verbatim, sections 3-5 |
| **AP2O-Coder**, [arXiv 2510.02393v4](https://arxiv.org/abs/2510.02393), venue not stated | DPO on self-generated pass/fail code pairs ordered by error type (frequency low to high, or high to low), with replay of the error types the current model still makes on a validation set. Pairs generated once | Table 1, HumanEval pass@1, Qwen2.5-Coder-1.5B: initial 69.3, SFT 70.4, DPO 73.2, low-to-high 76.3, high-to-low 71.7; 0.5B: DPO 56.8, 61.5, 56.5. Table 3 (7B): without replay -0.4 to -3.3. No random-order row | An error-type curriculum at this model size gains 3.1 over DPO in one order and loses 1.5 in the other; the order is not predicted by the paper | verbatim, tables 1-3 |
| Lanchantin et al., **Bridging Offline and Online Reinforcement Learning for LLMs**, [arXiv 2506.21495](https://arxiv.org/abs/2506.21495) (cited in section 1.12) | DPO with the sampling model synchronized every s updates | Table 1, Llama-3.1-8B, Math500: offline DPO 53.7, semi-online s=100 58.9, s=10 57.2, online 58.7, GRPO 58.1 | Refreshing samples once per federated round is semi-online DPO; it matches online DPO and GRPO there | verbatim, table 1 |
| Setlur et al., **RL on Incorrect Synthetic Data Scales the Efficiency of LLM Math Reasoning by Eight-Fold**, [arXiv 2406.14532](https://arxiv.org/abs/2406.14532), venue not stated on the page | Self-generated correct solutions against positives from stronger models; per-step DPO on negatives | Abstract and section 5: self-generated positives double the efficiency of the same problems; per-step negatives are worth 8x data. 7B models, math | Positives from the learner beat positives from a stronger model; argues against teacher SQL as the chosen side | abstract, sections 1 and 5 |
| ReViSQL (section 1.10), false positives | Bounded equivalence verifier (VeriEQL, 2 tuples per table) on rollouts whose result matches gold | Abstract and section 1: 32.8% of positive result-based rewards are refuted on BIRD training rollouts. No ablation isolates the corrected reward; clean training data is named as the dominant factor | Label false positives exist at a high rate on BIRD under a bounded verifier; their cost in training is not measured | abstract and section 1 verbatim, sections 4-5 summary |
| Chowdhury et al., **Provably Robust DPO**, ICML 2024 ([PMLR](https://proceedings.mlr.press/v235/ray-chowdhury24a.html)) | DPO loss de-biased for a known flip rate of preference labels | DPO degrades under random flips; the corrected loss is more robust (IMDb, Anthropic HH) | A loss-side alternative to stricter labels, for random rather than systematic label errors | search summary only |
| PLaD (section 1.5), detail | Teacher output always preferred over student output, no verification; margin ranking loss | Table 1, LLaMA-2 13B to 7B, TL;DR win rate: SeqKD 37.92, PLaD 40.46 | Unverified teacher-preferred pairs give a small gain on text generation | verbatim, sections 4-5.2 |
| COAL-SQL, [arXiv 2609.20842](https://arxiv.org/abs/2609.20842), PVLDB template, acceptance not confirmed | 35B teacher synthesizes SQL and questions on BIRD training databases from SQL skeletons chosen for coverage; GRPO plus SFT on teacher-written reasoning for questions where no rollout is correct (15.1% of training questions at the start) | Qwen2.5-Coder-7B: Spider test 85.3 (base 82.5), random instead of coverage-guided augmentation 83.4 | Which synthetic rows are added matters; the teacher sees the training databases | sections 1-3 verbatim, results summary |

Searches on 2026-11-16 found no federated Text-to-SQL paper besides FL4SP,
no paper that trains a SQL generator on rule-based SQL mutants as negatives
(SQL mutation operators and data that kills mutants exist for testing:
SQLMutation, XData), and no federated method that runs a verifier-labelled
preference step at the server on public data (FedBiscuit and FedPrism use
learned preference selectors; PubSwap's public step runs at the clients).

What this means for an added mechanism:

- The core recipe is CodeLutra's, federated and at 1.5B. The paper has to
  cite it as the closest work and cannot rest its novelty on the recipe.
- The largest published effect at this model size on Spider comes from
  verified synthesis on training databases (SPFT-SQL), with a weak
  preference stage; CodeLutra has the strong preference stage and no
  synthesis. Their combination is not published, centralized or federated.
- Every large teacher-in-the-loop gain (LUFFY, ExCoT, COAL-SQL, SERL-SQL)
  has the teacher on the training prompts or databases. With the teacher
  restricted to public data the published gains are about 1 point (section
  1.7).

### 1.17 Gap scan for the added mechanism (2026-11-16)

From a narrative gap scan of 2026-11-16 (not a systematic review). Each
page was opened in that run and has not been rechecked since; "Read" names
the part read. Numbers quoted from an abstract are the paper's own claims.

| Paper | Mechanism and setup | Evidence | Relation | Read |
|---|---|---|---|---|
| Jeong et al., **Federated Semi-Supervised Learning with Inter-Client Consistency & Disjoint Learning (FedMatch)**, ICLR 2021 ([arXiv 2006.12097](https://arxiv.org/abs/2006.12097)) | The server sends each client the models of H = 2 other clients as helpers; a client's pseudo-labels on its own unlabelled data come from agreement with them. Image classification | Section 3.1, equations 1 to 3 | Closest prior work for other clients' adapters as extra samplers and voters. Different here: generation, votes by execution result on private databases, peer samples as chosen answers | abstract and section 3.1 |
| Zhang et al., **PPFedIT** (formerly FedPIT), ACM TIST per the arXiv comment ([arXiv 2403.06131](https://arxiv.org/abs/2403.06131)) | Each client generates synthetic instruction data in context from a few local examples, for federated instruction tuning | Abstract only | Clients that synthesize their own training data in FL exist; no verifier checks the rows | abstract |
| Huang et al., **Concordia: Self-Improving Synthetic Tables for Federated LLMs**, [arXiv 2605.09855](https://arxiv.org/abs/2605.09855), no venue | A generator per client, trained with GRPO, writes synthetic tables; tabular tasks | Abstract only | Client-side synthesis with a learned generator; not SQL, no execution check | abstract |
| Yan et al., **ExSPIN**, Entropy 27(3):235, 2025 ([PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC11940967/)) | The predecessor of SPFT-SQL: self-play fine-tuning with execution feedback | Table 3, Spider test EX, DeepSeek-Coder-6.7B: SFT 76.3, SPIN 64.2, ExSPIN 83.2. Qwen2.5-Coder 1.5B to 14B only in a figure. No code link | Self-play without execution feedback loses to SFT; with it, +6.9 at 6.7B | full text, Table 3 |
| Zhao et al., **Importance of Synthesizing High-quality Data for Text-to-SQL Parsing**, [arXiv 2212.08785](https://arxiv.org/abs/2212.08785), no venue on the page | Synthetic SQL with key relationships, strong typing and schema-distance column sampling | Abstract: earlier synthetic SQL did not help because columns were sampled independently and joins were arbitrary | The rules a client-side SQL generator has to follow: joins along keys, columns of matching type | abstract |
| Wang et al., **Learning to Synthesize Data for Semantic Parsing**, NAACL 2021 ([arXiv 2104.05827](https://arxiv.org/abs/2104.05827)); Yu et al., **GraPPa**, ICLR 2021 ([arXiv 2009.13845](https://arxiv.org/abs/2009.13845)) | A PCFG over SQL plus a BART SQL-to-text model; a synchronous grammar for pre-training | Abstracts only | Early SQL-first synthesis, centralized | abstracts |
| Ma et al., **Enhancing Text-to-SQL Capabilities of LLMs via Domain Database Knowledge Injection**, ECAI 2024 ([arXiv 2409.15907](https://arxiv.org/abs/2409.15907)) | Pre-training on database schema and cell values | Abstract only | Database content as a training signal, without generated questions | abstract |
| Li et al., **QuestA: Expanding Reasoning Capacity in LLMs via Question Augmentation**, ICLR 2026 per the arXiv comment ([arXiv 2507.13266](https://arxiv.org/abs/2507.13266)) | Partial solutions added to hard prompts during RL, 1.5B, math | Abstract: AIME24 72.50 (+10.73), AIME25 62.29 (+12.79), HMMT25 41.67 (+10.11) | A hint for questions no rollout solves; no SQL version found | abstract |
| Liang et al., **Beyond Pass@1: Self-Play with Variational Problem Synthesis Sustains RLVR (SvS)**, [arXiv 2508.14029](https://arxiv.org/abs/2508.14029), no venue | New problems synthesized from the policy's own correct solutions | Abstract: keeps pass@k from falling under RLVR | New questions as the remedy for a loop that runs out of unsolved-but-solvable ones | abstract |
| Chen et al., **Self-Questioning Language Models (SQLM)**, [arXiv 2508.03682](https://arxiv.org/abs/2508.03682), no venue | Proposer and solver; the solver's reward is a majority vote | Abstract only | Vote as the reward for self-written questions; not SQL | abstract |
| Yan et al., **What If Consensus Lies? Selective-Complementary Reinforcement Learning at Test Time (SCRL)**, ACL 2026 per the arXiv comment ([arXiv 2603.19880](https://arxiv.org/abs/2603.19880)) | A strict consensus filter and negative pseudo-labels for test-time RL | Abstract only | Weak majorities mislead; a vote label needs an agreement threshold | abstract |
| Gorbett and Shirazi, **Label-Free Reinforcement Learning via Cross-Model Entropy**, [arXiv 2605.29009](https://arxiv.org/abs/2605.29009), no venue | Reward from a second model's likelihood | Abstract: instruction following only | Another label-free signal; no execution | abstract |
| Wang et al., **Adaptive LoRA Experts Allocation and Selection for Federated Fine-Tuning (FedLEASE)**, NeurIPS 2025 per the arXiv comment ([arXiv 2509.15087](https://arxiv.org/abs/2509.15087)) | LoRA experts per client cluster, selected per input | Abstract only | Does not fit here: Spider test databases are unseen, so no client expert serves a test question | abstract |

Searches that found nothing at the intersection (web search snippets, so
"not found with these queries"): federated Text-to-SQL with an LLM or SLM
(only FL4SP); federated fine-tuning with local synthesis checked by a
verifier; training a Text-to-SQL model on vote labels (votes appear only at
inference); a hint method for SQL questions no rollout solves; federated
semi-supervised LoRA fine-tuning with votes on private data (FedCT and
Semantic Consensus vote on public prompts).

### 1.18 Training on perturbed schemas (scan of 2026-11-16)

A short scan (three web searches, two pages fetched) for the idea "same
question, perturbed schema" as training data. "Summary" marks numbers
known only from a machine summary of the page: check them before citing.

| Paper | Mechanism and setup | Evidence | Relation | Read |
|---|---|---|---|---|
| Zhang et al., **EvoSchema: Towards Text-to-SQL Robustness Against Schema Evolution**, PVLDB 18(10): 3655-3668, 2025 ([arXiv 2603.10697](https://arxiv.org/abs/2603.10697)) | The same question paired with several schema designs: add, remove, rename, split and merge columns and tables. Renames revise the gold SQL where the name occurs; add and remove leave it unchanged. GPT-3.5 proposes added and renamed items, GPT-4 and Claude 3.5 rewrite SQL for split and merge. Built on BIRD; plain fine-tuning of 7-8B models (summary) | Introduction: up to 33 points on perturbed evaluation data. Summary, Table 5, EX without / with perturbation training: original data Code Llama 58 / 57, Mistral 59 / 58, Llama 3 55 / 51, SQLCoder 58 / 58; rename columns 54 / 52, 55 / 54, 49 / 47, 56 / 55; add tables 40 / 58, 39 / 58, 37 / 52, 40 / 57 | The closest work to perturbed schemas as training data. Supervised only, centralized, with large LLMs writing the perturbations; no sampling from the model and no execution signal in training. The gain is on changed table structure, not on renames and not on the original data | sections 1-3.6 verbatim; sections 4-6 and tables summary |
| Pi et al., **Towards Robustness of Text-to-SQL Models Against Natural and Realistic Adversarial Table Perturbation (ADVETA)**, ACL 2022 ([arXiv 2212.09994](https://arxiv.org/abs/2212.09994)) | Column names replaced (gold SQL mapped to the new name) or columns added (gold SQL unchanged); the defense CTA adds one replaced and one added example per training pair, candidates from a table retriever and an NLI filter | Table 2, Spider, exact match: dev 70.8, replaced 27.6, added 39.9. Summary, Table 3, with CTA: dev 69.8, replaced 35.8, added 50.6 | Perturbation training before LLMs: robustness rises, the clean set loses 1.0 | sections 1-4 and Table 2 verbatim; Table 3 summary |
| Chang et al., **Dr.Spider**, ICLR 2023 ([arXiv 2301.08881](https://arxiv.org/abs/2301.08881)) | Benchmark of 17 perturbations of Spider dev: database (schema synonym, abbreviation, content), question and SQL | Search snippet only | An evaluation set for schema-side perturbation, on the Spider dev databases | search snippet |

Not opened: SQLong (schema augmentation for long contexts), Solid-SQL
([arXiv 2412.12522](https://arxiv.org/abs/2412.12522), augmentation for
schema linking in an in-context pipeline), EGRefine
([arXiv 2605.00628](https://arxiv.org/abs/2605.00628), schema renaming
before inference).

Not found with these queries: perturbed schemas inside on-policy,
execution-labelled preference training; a federated version; a version
without an LLM writing the perturbations. The published effect of
perturbation training is robustness on perturbed data with about one
point lost on the original set.

### 1.19 Prompt, training and decoding practice (checked 2026-11-17)

Read for the clean setup: what widely used Text-to-SQL work feeds a
fine-tuned open model, how it trains and how it decodes. "Code" means the
item was read in the paper's repository; "figure" means the paper shows it
only as an image that was not read.

| Work | Schema in the prompt | Extra parts it needs | Output | Training | Decoding | Read |
|---|---|---|---|---|---|---|
| Qwen2.5-Coder report ([arXiv 2409.12186](https://arxiv.org/abs/2409.12186)), section 7.4, and its evaluation code (`qwencoder-eval/instruct/bird-spider`) | "table representations aligned with database instructions, examples of table content, optional additional knowledge, and natural language questions", "following the work of Chang & Fosler-Lussier (2023)"; the code appends "Please output only the final SQL query, starts with keyword `SELECT`." | none | SQL only | none (evaluation of the released models) | chat mode, 1 sample, 1,024 new tokens, stops at `;` and end tokens; temperature not found; scored on Spider dev and BIRD dev | section 7.4 verbatim; prompt figure and result figure are images; the instruction field of the data file (in a zip) not read |
| Chang and Fosler-Lussier, **How to Prompt LLMs for Text-to-SQL** ([arXiv 2305.11853](https://arxiv.org/abs/2305.11853)) | `CREATE TABLE` text, then per table `/* 3 example rows: select * from t limit 3; ... */` (from Rajkumar et al., 2022) or 3 distinct values per column; then `-- Using valid SQLite, answer the following questions for the tables provided above.`, `Question: ...`, `select`. Text lower-cased and spaces unified except database content | none | SQL only | none (prompting) | Codex | sections 3-5 and appendix A.1 verbatim |
| DAIL-SQL ([arXiv 2308.15363](https://arxiv.org/abs/2308.15363)), section 3.1 | Code representation: `/* Given the following database schema: */`, `CREATE TABLE` with primary and foreign keys, `/* Answer the following: ... */`, `SELECT`. Alpaca SFT: `table(col, col)` lines | none | SQL only | fine-tuned LLaMA 7B to 33B; batch 256, learning rate searched in 1e-6 to 1e-4 (appendix D.4, summary) | not stated | listings verbatim; SFT tables summary |
| CodeLutra ([arXiv 2411.05199](https://arxiv.org/abs/2411.05199)) | zero-shot, `CREATE TABLE` text of the SQLite file in its figure; no values | none | SQL only | LoRA r 8, lr 5e-5, batch 16, 1 epoch per iteration | T 0.2, 512 new tokens, 1 sample | whole page verbatim; no code published |
| CodeS ([arXiv 2402.16347](https://arxiv.org/abs/2402.16347)), code | own serialization: `table t , columns = [ t.c ( type \| primary key \| comment : ... \| values : a , b ) ]`, `foreign keys :`, `matched contents :`, question; no instruction, no chat template | a trained schema filter (6 tables, 10 columns kept) and a BM25 value retriever | SQL, keywords upper-cased and identifiers lower-cased (`sqlparse`) | full fine-tuning, lr 5e-6, 4 epochs, batch 128, 4,096 tokens | beam 4, the first executable SQL | code and sections 6, 8, 9 |
| OmniSQL ([arXiv 2503.02240](https://arxiv.org/abs/2503.02240)), README and section 5.1; reused by SLM-SQL ([arXiv 2507.22478](https://arxiv.org/abs/2507.22478)) | one user message through the chat template: "Task Overview", `CREATE TABLE` text with column descriptions, two representative values and question-relevant values as SQL comments, question, instructions | none stated for the schema text | reasoning, then SQL in a code block | Qwen2.5-Coder 7B to 32B on SynSQL-2.5M plus Spider and BIRD train; full fine-tuning or LoRA r 256, 2 epochs, 8,192 tokens | greedy (temperature 0), 2,048 new tokens; or a vote over 8 samples at T 0.8 | README verbatim, sections 3 to 6.2 verbatim |
| DTS-SQL ([arXiv 2402.01117](https://arxiv.org/abs/2402.01117)), appendix A.2 | foreign keys, primary keys, column types and three sample rows per table (layout in a figure) | a fine-tuned schema-linking model for the two-stage method | SQL | Mistral 7B, DeepSeek 6.7B; lr 1e-5 and 5e-5 | not stated | text verbatim; prompt figures and notebooks not read |
| MSc-SQL ([arXiv 2410.12916](https://arxiv.org/abs/2410.12916)), appendix A.2 | `TABLE "t" ( "c" TEXT primary key, -- Example: "..." )` | a schema-linking step | JSON with the SQL | QLoRA r 32, alpha 128, dropout 0.05 | not read | appendix and section 5 verbatim |
| XiYanSQL-QwenCoder, README; M-Schema, code | M-Schema: `# Table: t`, `(col:TYPE, comment, Primary Key, Examples: [a, b, c])`, `【Foreign keys】`; a Chinese instruction template | none | SQL in a code block | not stated | T 0.1, top_p 0.8, 1,024 new tokens | README and `m_schema.py` |
| SPFT-SQL ([arXiv 2509.03937](https://arxiv.org/abs/2509.03937)), appendix A.4 | not published; section 3.1.2 names schema extraction, value matching and metadata | not stated for the 1.5B rows | SQL | LoRA through LLaMA-Factory, AdamW, batch 64, lr 2e-4, 3 epochs; rank not stated | not stated | main text and appendix A.4 verbatim |

Numbers on the student's family, each with its own prompt (not comparable
with ours): SPFT-SQL, Qwen2.5-Coder-1.5B, Spider test: zero-shot 72.3, SFT
78.0, the method 82.3. OmniSQL Table 4, greedy, Spider test:
Qwen2.5-Coder-7B / 14B / 32B-Instruct 82.2 / 86.6 / 87.5. SLM-SQL Table 3,
Qwen2.5-Coder-1.5B, Spider test, a vote over 16 samples: base 67.61, SFT
77.35. XiYanSQL-QwenCoder-7B-2502, Spider test: 84.15 with M-Schema, 80.01
with DDL.

What is common to them:

- The schema is `CREATE TABLE` text in most, and nearly all add a few
  database values: example rows per table (Rajkumar et al.; Chang and
  Fosler-Lussier; the Qwen2.5-Coder report; DTS-SQL) or example values per
  column (OmniSQL, MSc-SQL, CodeS, M-Schema). Plain DDL with no values is
  the minority (DAIL-SQL's code representation, CodeLutra).
- Schema filters and value retrievers are separate trained or indexed
  parts (CodeS, DTS-SQL, MSc-SQL).
- A fine-tuned small model outputs SQL only; reasoning before the SQL is
  the choice of the SynSQL line (OmniSQL, SLM-SQL).
- Chat models get one user message through the chat template and no
  system message of their own (OmniSQL, XiYanSQL), so the template's
  default system text is in the prompt.
- Decoding is greedy or near greedy; none states a repetition penalty.
- LoRA SFT at this size: lr 2e-4, 3 epochs (SPFT-SQL, the same student).

### 1.20 Counterexamples for local preference labels (2026-11-18)

Two SQL queries can return the same rows by accident. Zhong, Yu and Klein
used multiple database instances to evaluate predicted SQL
([EMNLP 2020](https://aclanthology.org/2020.emnlp-main.29/)).
ReViSQL reports that bounded equivalence checking refuted 32.8% of its
positive execution rewards in a BIRD training pilot ([section 4.1](https://arxiv.org/html/2603.20004v4)).
SQLoom already constructs counterexamples for training by changing boundary
values and adding child rows along foreign keys, then uses the verified
differences in a set-contrastive loss ([section 4 and appendix C](https://arxiv.org/html/2611.03298v1)).
The [CoRE-DB dataset card, section e](https://huggingface.co/datasets/thanhdath/CoRE-DB-BIRD-SPIDER)
reports a 1.5B comparison under the same RL recipe: original versus enriched
reward databases gave 71.57 versus 74.47 on Spider dev and 46.74 versus
47.85 on BIRD dev. The authors built the databases from gold queries and
report this comparison in the release card.

The owner dropped this direction on 2026-11-18. The CPU probe measured
constructed boundary errors. The owner's prediction audit found zero
direct boundary-operator substitutions among the executable wrong answers
of either FedAvg R4 or DPO R2 on Spider test. The training cause of those
wrong answers remains unknown.

### 1.20a CoRE-DB as built, from its repository (read 2026-11-23)

Read: the README and the build, reward and evaluation source of
[thanhdath/core-db](https://github.com/thanhdath/core-db) (Apache-2.0).
Not read: the paper. Its title in the README is "Boosting Small Language
Models for Text-to-SQL with Cost-Efficient Reinforcement Environment
against Spurious Correctness"; no preprint under that title was found.
arXiv 2605.03465 (FINER-SQL, the trainer it reuses) has no test-suite
metric and no enriched database, and names spurious correctness once, for
empty results only. The gains below are the README's words, not checked in
a table.

- Problem: a wrong SQL that returns the gold's result on the training
  database gets a positive execution reward ("spurious correctness").
  Claim: training on CoRE-DB raises execution and test-suite accuracy by
  1 to 4% and trains 1.51 times faster. The RL algorithm is unchanged
  (GRPO, 32 rollouts for one prompt, learning rate 8e-6); only the
  databases behind the reward change.
- Build, per training database (215: all of Spider train and BIRD train,
  the Spider databases without rows among them), five steps. (1) A compact
  database that keeps the rows the gold queries need. (2) Gold and
  neighbor pairs: neighbors from the grammar mutations of the Spider
  test-suite generator (dropped spans; a token replaced inside its family:
  aggregate, comparison, order direction, AND/OR, column name, literal)
  and from 30 samples at temperature 1.0 of a Text-to-SQL model; at most
  five per gold and source; only golds that return a non-NULL value on
  the original. (3) Value filling: three LLM agents (Designer, Engineer,
  Reviewer, an external model through an API) write one Python generation
  program per database; the program appends rows to copies of the compact
  database with no LLM call: values from observed columns and from the
  literals of the queries, perturbed (numbers by 1 or 2, strings with
  near variants), ties, duplicates, NULLs at the share of the source,
  parents without children, keys and constraints kept. (4) Separation:
  for each pair that agrees on the original, which instances tell gold
  from neighbor. (5) A greedy set cover picks the fewest instances that
  separate every separable pair.
- Verdict of a sample: accepted only when it matches the gold on every
  instance where the gold's result is informative (not empty, not all
  NULL); ORDER BY at the top level compares rows in order.
- Measured in the repository: a set of 800 gold and prediction pairs on
  100 BIRD and 100 Spider training questions with hand labels (152
  spurious), on which CoRE-DB still accepts 10.1% of the spurious ones
  (14.7% in the paper, per the README).
- Against our setting: the build is central, needs the gold SQL of every
  database in one place and sends schema, column values and statistics
  to an external LLM. A client cannot do that under data isolation. What
  carries over is the principle (more than one database instance behind a
  label, a sample accepted only when it matches on all informative ones)
  and the content rules a fixed program can apply without an LLM.

### 1.21 Training databases without rows, and content for them (2026-11-19)

Read by a research agent through page fetches and on downloaded copies,
not by eye, and its scripts are not committed. Each item is to be read
again in its source before the paper cites it. The direction it serves is
in `RESEARCH_STATE.md`, section 4, item 11.

Who names or handles the empty databases:

| Source | What it says or does |
| --- | --- |
| Spider repository, [issue 14](https://github.com/taoyds/spider/issues/14) | The maintainers: the six databases taken from older datasets (academic, geo, imdb, restaurants, scholar, yelp) are given as schemas only. `music_2` was reported empty in 2019 (issue 35), with no reply |
| Arctic-Text2SQL-R1 ([arXiv 2505.20315](https://arxiv.org/abs/2505.20315)) | Drops the training samples whose gold result is empty (about 1,700 on Spider, 1,400 on BIRD). For the empty Gretel-Synth schemas, GPT-4o writes INSERT statements per table, sampled again until the gold SQL returns rows: one instance, built centrally |
| Liu et al., ACL 2025 ([arXiv 2502.11656](https://arxiv.org/abs/2502.11656)) | Limitations: Spider has test-suite databases for the development set only, "leading to inaccurate preference pair construction" |
| Suhr et al., ACL 2020 | Discards `train_others` in training; in evaluation removes examples whose correct query returns an empty table |
| CodeLutra, ExCoT, SENSE, SLM-SQL, SQL-R1, Reasoning-SQL | Nothing on empty databases or empty gold results |

Content that exists for the seven databases:

- `jkkummerfeld/text2sql-data`: real data for geography in SQLite (64 KB,
  schema equal to Spider's `geo`; 556 of 564 Spider gold SQL return rows
  in the agent's check, 530 of 564 in the check of 2026-11-17, not
  reconciled) and for restaurants (56 of 125). Academic, IMDB, Yelp and
  Scholar are MySQL dumps of about 3 GB, not downloaded. No licence is
  stated for these. Nothing exists for `music_2`.
- The test-suite release of Zhong, Yu and Klein
  ([arXiv 2010.02840](https://arxiv.org/abs/2010.02840),
  `taoyds/test-suite-sql-eval`) covers Spider dev and the classical
  datasets, not Spider train. The six classical suites have Spider's
  schemas (scholar with two more tables). On Spider's gold SQL at least
  one suite database returns rows for 63% (academic 98.9%, geo 65.6%,
  imdb 95.4%, restaurants 96.0%, scholar 29.0%, yelp 96.4%); a single
  suite database does so for a small share only.
- Their fuzzer (`ruiqi-zhong/TestSuiteEval`, `fuzz/fuzz.py`; paper,
  section 4): tables filled in foreign-key order, foreign-key values drawn
  from the parent's values, other columns typed random values mixed with
  the gold query's literals and near variants; 1,000 databases per schema
  distilled to those that separate gold from its neighbour queries, about
  a week on 16 CPUs. A non-empty gold result is not enforced per database.
  The paper remarks that one sampled database "might be useful when
  occasional errors are tolerable (e.g. denotation based training)" and
  does not try it.

Generators that take a query: LASSO (Jadhav and Sudarshan,
arXiv 2610.38294; DDL and one gold SELECT in, several INSERT sets out,
SQLite dialect, not run), VeriEQL (bounded checking that returns a
counterexample database), SpotIt
([arXiv 2510.26840](https://arxiv.org/abs/2510.26840), counterexample
databases for evaluation).

Generated or checked content as a training signal: ReViSQL (a second check
by VeriEQL in the GRPO reward; section 1.20), SQLoom and CoRE-DB (section
1.20), Arctic (one LLM-written instance per empty schema, above). Not
found by the agent: labels taken from several instances generated by the
data owner, or Spider's empty training databases filled to obtain labels.

### 1.22 Federated Text-to-SQL, scan of 2026-11-25

Queries: arXiv API on abstracts (federated with text-to-SQL, NL2SQL,
semantic parsing, SQL, table question; decentralized with text-to-SQL),
OpenAlex since 2022 (federated text-to-SQL, NL2SQL, text2sql, semantic
parsing, natural language interface to databases, knowledge base QA,
text-to-SPARQL/Cypher, code generation, table QA, cross-silo text-to-SQL,
privacy-preserving text-to-SQL fine-tuning), the 9 papers citing FL4SP on
Semantic Scholar (this time the API answered), web search in English and
Chinese, ACL Anthology. Six candidates were grepped in their arXiv HTML for
"SQL", "Spider" and "BIRD".

Result: FL4SP (section 1.2) is still the only paper that trains a
Text-to-SQL model with federated learning. Its 9 citing papers are not
federated Text-to-SQL (SafeNLIDB, EvoSchema, a Text-to-SQL survey, two
federated multilingual LoRA papers, four unrelated). What the scan adds:

| Paper | What it does | Relation to our setup | Read |
|---|---|---|---|
| **KGRFL: Knowledge Graph-Based Reinforcement Federated Learning for Chinese Question and Answering**, IEEE Trans. Computational Social Systems 2023 ([DOI](https://doi.org/10.1109/TCSS.2023.3246795)) | Institutions train a BART semantic parser (question to SPARQL, plus question category) with FL; an RL-based fusion weights client models and lowers the effect of low-quality clients | The only other federated semantic parsing paper with a parser as the federated model. SPARQL over a knowledge graph, small seq2seq model, no execution labels. Citable next to FL4SP for "federated semantic parsing" | abstract |
| Fed-KGQA, J. Information Systems Engineering and Management 2025 ([DOI](https://doi.org/10.52783/jisem.v10i30s.4893)) | Federated KG embeddings (FedR, TransE) for simple-question KGQA across organizations | Not a parser and a low-tier venue; mention only if the related work lists federated QA | abstract |
| **RAG-SQL: Sovereignty-Aware Retrieval-Augmented Generation for Federated Text-to-SQL in Business Intelligence**, 2026 (companion repository on [Zenodo](https://doi.org/10.5281/zenodo.22953628); manuscript submitted to Knowledge and Information Systems) | "Federated" means a federated PostgreSQL/MariaDB deployment: schema fragments are retrieved per question, prompt schema tokens drop by up to 71%, a cloud model keeps EX 92-94%, local 3B/8B models lose accuracy | Inference over federated databases, no training. Uses the name "federated Text-to-SQL" for query federation, so our paper should define its term. Not peer-reviewed yet | Zenodo record |
| **Fan Out or Relay? Ownership-Aware Routing for LLM Agents Querying Siloed Tables**, arXiv 2026 ([2610.18157](https://arxiv.org/abs/2610.18157)), no venue | Tables of one question sit with several owners who never hand them over; an LLM coordinator routes a schema-only draft SQL to the owners. On BIRD two-table joins, fan-out answers 32-44% when one owner holds both tables and 1-4% otherwise | Same motivation (data stays with its owner), solved at inference with prompting; no model is trained | abstract |
| **A Survey on Federated Fine-tuning of Large Language Models**, TMLR 2026 ([arXiv 2503.12016](https://arxiv.org/abs/2503.12016)) | Lists BIRD among code benchmarks for federated evaluation ("database-grounded text-to-SQL", EX), called "increasingly relevant ... under privacy" | Citable for BIRD as a federated evaluation target; the survey reports no federated BIRD result | HTML grep, benchmark section and table |
| **I Can't Share Code, but I need Translation: An Empirical Study on Code Translation through Federated LLM**, arXiv 2025 ([2501.05724](https://arxiv.org/abs/2501.05724)), no venue | Clients fine-tune CodeLLaMA together for C# to Java and back; over 40% gain over local training (abstract) | Federated code LLM next to the program-repair study in section 1.2; SFT only | abstract |
| Guo et al., **LaDa: Federated Reasoning Distillation Framework with Model Learnability-Aware Data Allocation**, arXiv 2026 ([2602.18749](https://arxiv.org/abs/2602.18749)), no venue | Server LLM and client SLMs; samples allocated by the learnability gap of each LLM-SLM pair; reasoning paths aligned with a contrastive, DPO-like objective | Closest to section 1.1 (server LLM, client SLMs) with a preference-style loss; no SQL task (one mention of ZeroNL2SQL in related work) | abstract, HTML grep |
| Fed-SE, arXiv 2025 ([2512.08870](https://arxiv.org/abs/2512.08870)), no venue; **SemFed**, Findings EMNLP 2026 ([DOI](https://doi.org/10.18653/2026.findings-emnlp.1147)) | Federated training of LLM agents from local trajectories. Fed-SE: PEFT on filtered high-return trajectories, aggregation in a low-rank subspace, +10% average success over baselines on five environments. SemFed: clients send policy summaries instead of parameters (ALFWorld, WebShop) | Fed-SE's local step is rejection sampling on the client's own rollouts, the federated analogue of our RFT arm, on agent tasks; neither has SQL | abstract, HTML grep (Fed-SE) |
| **Federated In-Context Learning: Iterative Refinement for Improved Answer Quality**, ICML 2025 ([arXiv 2506.07440](https://arxiv.org/abs/2506.07440)) | Clients and server refine answers over rounds with local examples, no parameters sent | QA only, no SQL; relevant only if the paper discusses federated ICL as an alternative to training | abstract, HTML grep |
| FedHLT, WWW 2024 Companion ([DOI](https://doi.org/10.1145/3589335.3651933)); FedLFC, Findings NAACL 2024 ([ACL](https://aclanthology.org/2024.findings-naacl.98/)) | Federated LoRA for multilingual modeling; LoRA aggregated within language families or a language tree | Cite FL4SP for client heterogeneity; LoRA grouping by client similarity, not SQL | abstract |

Not federated training despite the words in the title or abstract: query
federation and secure query processing (SMCQL, Shrinkwrap, KloakDB),
SPARQL over federated knowledge graphs (arXiv 2410.06062), TablePuppet
(relational FL on joined tables, not language), MaskSQL and SafeNLIDB
(section 1.13 and `FEDERATED_DATA_SETUP.md`), EHRFL and Med-MMFL (federated
EHR models without SQL generation), FlowerTune and the Sherpa.ai
cross-domain benchmark (arXiv 2605.13936; no SQL task in either).

For the paper: "the only earlier federated Text-to-SQL work is FL4SP"
still holds; KGRFL can be cited beside it as federated semantic parsing to
SPARQL. The term "federated Text-to-SQL" is also used for querying
federated databases (RAG-SQL), so the introduction should say that here
it means federated training of the model.

## 2. What already exists

- Iterative on-policy execution-labelled DPO + SFT for SQL, centralized, at
  7-8B (CodeLutra) and at 3B with ORPO (MATS).
- Server LLM with public data helping federated SLMs (FedMKT, FedCoLLM,
  CrossLM, GPT-FL). Client gains over FedAvg are 1-3 points; teachers are
  trained, public data is in-distribution, tasks are classification or QA.
- Federated DPO as local DPO plus LoRA averaging (the "FedDPO" baseline in
  OpenFedLLM and FedBiscuit), and server-side DPO on aggregated preference
  signals (FedBiscuit). All on human preferences.
- Federated RL with verifiable rewards at small-model sizes (PubSwap,
  Fed-GRPO, FedMOA), on math and code; reward/progress-weighted aggregation
  also appears in FGRPO. These are direct precedents for verifier-driven FL,
  even though the task and optimization objective differ from SQL DPO.
- Centralized execution-verified preference training for Text-to-SQL
  (ExCoT, Liu et al., SENSE) at 7B-70B, and execution-reward RL (Arctic,
  Reasoning-SQL, Think2SQL, SLM-SQL) mostly on 8-64 large GPUs.
- Text-to-SQL distillation into ~1B students (KID) and code distillation with
  our exact model pair (DistiLLM-2).
- One federated Text-to-SQL paper (FL4SP), with T5-base and exact match.
- Label-free preference training through self-consistency (ScPO),
  self-generated code/tests (CodeDPO, DSTC), and execution-success pairs for
  SQL dialects (ExeSQL). SQL-Zero supplies a separate self-play precedent.
- Execution-result candidate selection (MBR-EXEC), learned verifiers
  (LEVER, GradeSQL), and explicit analyses of label reliability and
  cross-schema verifier transfer (sections 1.9-1.10).
- Teacher-free soft-target controls (Yuan et al.) and controlled studies
  separating rollout policy, divergence and later RLVR (Piskorz et al.).
- Verified synthesis on training databases, centralized (SPFT-SQL, ExSPIN,
  SQL-Zero), with rules for sensible synthetic SQL (Zhao et al.), and
  clients that synthesize their own training data in FL without a verifier
  (PPFedIT, Concordia).
- Other clients' models as helpers for pseudo-labels on local unlabelled
  data, in vision (FedMatch).

## 3. Gaps that fit our setup

These are gaps in the reviewed corpus as of 2026-11-14 (items 6 to 8 as of
2026-11-16), not claims of priority or an exhaustive literature search.

1. **Local execution-labelled policy DPO for cross-database federated SQL
   at 1.5B.** FL4SP covers supervised semantic parsing; OpenFedLLM covers
   federated DPO; Liu et al. and ExCoT cover centralized execution-labelled
   SQL DPO. Federated GRPO is already verifier-driven. The narrower
   intersection is the relevant distinction, not "FL with a verifier".
2. **Role of preference learning versus correct-sample fitting.** ExeSQL,
   SPFT-SQL and Iterative RPO supply related training mechanisms. Their
   objectives, label sources, model sizes and data access differ; they do
   not settle whether each component of a 1.5B federated SQL recipe helps.
3. **Gold, vote and execution-success signals under one training protocol.**
   ScPO is the closest vote-preference work, ExeSQL the execution-success
   precedent. Neither establishes their equivalence to gold-result labels
   for this setting. Hiding existing gold labels tests signal dependence;
   an actual semi-supervised extension is a separate data assumption.
4. **What a public-data initialization contributes after client DPO.**
   Yuan et al. motivate soft-target controls, while Piskorz et al. show
   that initialization coverage and later reward training interact. The
   corpus supplies no matched frozen-teacher BIRD-to-Spider experiment
   followed by 1.5B federated SQL DPO that isolates teacher information from
   extra public data and regularization.
5. **Training and decoding at equal inference cost.** MBR-EXEC, LEVER,
   GradeSQL and CSC-SQL require explicit decoding comparisons. A greedy
   gain and a voting gain answer different questions; equal aggregate
   scores do not establish per-question amortization.
6. **Verified synthesis inside an on-policy DPO loop, run where the
   databases are.** SPFT-SQL has the synthesis with a weak preference
   stage, CodeLutra the strong on-policy loop without synthesis; PPFedIT
   and Concordia synthesize at the clients without a verifier. No paper
   feeds execution-checked synthetic questions into on-policy DPO, and no
   federated paper checks synthetic rows by execution on the client's own
   databases. Federation is the setting here, not the source of the gain:
   the mechanism also works centralized.
7. **A committee of client adapters with execution-result votes.**
   FedMatch uses other clients' models for agreement-based pseudo-labels in
   vision; FedCT and Semantic Consensus vote on public prompts. No paper
   uses the other clients' adapters as extra samplers for chosen answers or
   as voters on a client's private databases.
8. **Vote-labelled DPO for clients with few labelled questions.** ScPO is
   centralized math; no SQL training on vote labels and no federated
   version was found. This changes the data assumption (item 3).

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
- Fed-GRPO and FGRPO show isolated aggregation gains in their own settings.
  They do not establish the size of the gap here; a centralized reference
  with the same objective and data is needed to measure it.
- Published 1.5B numbers mostly use self-consistency; ours must name greedy or
  sampled decoding explicitly.
- Published zero-shot 1.5B Spider numbers (63.54 to 72.4, section 1.4) sit
  well above a plain-DDL greedy prompt. A reviewer will ask whether a weak
  prompt inflates the training gain; report zero-shot under each prompt and
  name the input components (values, schema filtering) next to every
  external row.
- External 1.5B rows differ in training data volume by up to about 50
  times (SLM-SQL 916K SFT rows, CodeS 21.5 GB of pre-training). A comparison
  table names the training data and its size for each row. SPFT-SQL cites
  Hui et al. 2024 for the model only; its 1.5B SFT row is its own LoRA run.
- SQLoom reports 89.2 greedy Spider test at 1.7B. A reviewer will compare;
  the paper has to state that SQLoom trains centrally on Spider + BIRD with
  GPT-4 in the loop, while here client data never leaves and no external
  model sees it.
- A sequence-level DPO method will be asked why it does not localize the
  error (Focused-DPO, CAPER, EXPO-SQL). Either localize, or show the
  comparison.
- Vote-labelled training must cite ScPO and distinguish gold-free labels
  from a dataset with no gold annotations. ExeSQL already trains on
  successful-versus-failed execution, so that signal alone is not new.
- Inference selection needs the same sample budget and selection rule on
  the baselines. LEVER and GradeSQL are direct learned-verifier references;
  separate greedy EX, voting EX, pass@k and inference cost.
- FlowerTune documents partial participation, communication and resource
  reporting. FGRPO and FedMOA also use small client counts, so the corpus
  supports testing federation breadth without a universal minimum K.
- Teacher contribution needs gold-only and soft-target controls, and
  evidence after the later client stage. A capacity-gap law or another
  task's KL comparison is not a guarantee about a stronger SQL teacher.
- Report structural data isolation with a defined threat model. The
  privacy literature in section 1.13 does not justify claiming that LoRA
  updates reveal no data.

## 5. Scope of the 2026-11-14 literature update

The update integrates relevant references from all five research reports,
deduplicating existing papers into their original entries or explicit
updates. It preserves supporting and contrary evidence, including
cross-schema verifier failure and the dependence of synthetic-data gains
on evaluation-database adaptation.

Two publisher candidates remain outside the evidence tables because their
primary article pages could not be retrieved in this update:
[FedHRQS](https://link.springer.com/article/10.1007/s12083-026-02306-7)
and the [DKE LLM/knowledge-graph Text-to-SQL article](https://doi.org/10.1016/j.datak.2026.102580).
Their experimental numbers and claimed full-text reading status are not
transferred. General healthcare, vision and legal application examples
used only for venue comparison are outside this method-focused catalogue.

The earlier reports' acceptance odds, subjective success probabilities,
GPU-time projections and quartiles from secondary websites are not
literature findings. In particular, an estimate that one third to two
thirds of this model's errors are benchmark noise cannot be inferred from
audits of different models' failures. The SPFT-SQL dev-TS/test-EX column
confusion and LEVER's previous-work MBR row are corrected above.
