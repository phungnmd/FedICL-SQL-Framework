# Related work literature scan, 2026-11-27

Scope is 2023–2026, with one older anonymous submission retained because it bears directly on the claim. Sources used for paper checks include ACL Anthology, arXiv, OpenReview, PMLR, the AAAI proceedings, and author or university copies. Google Scholar returned no accessible page. The browser host failed before a tab opened, and a separate web fetch could not load the Scholar query. No Scholar CAPTCHA or site block was visible. OpenAlex and Semantic Scholar citation endpoints also failed. The search log gives the partial forward-citation coverage.

| Title | Authors, year | Venue | Link | What it does (1–2 sentences from the abstract) | Fits subsection | Already in LITERATURE.md (yes/no) | Read |
|---|---|---|---|---|---|---|---|
| FedParsing: a Semi-Supervised Federated Learning Model on Semantic Parsing | Anonymous, year unverified (indexed around 2021) | OpenReview submission, publication unverified | [PDF](https://openreview.net/pdf?id=Oeikp9N4fzi) | Uses Mean Teacher and exponential moving averages for semi-supervised federated semantic parsing. Its WikiSQL experiments compare training with unlabeled client data against supervised and semi-supervised baselines. | 2.4 federated semantic parsing and Text-to-SQL | no | full text |
| Knowledge Graph-Based Reinforcement Federated Learning for Chinese Question and Answering (KGRFL) | Xu et al., 2024 (online 2023) | IEEE Transactions on Computational Social Systems 11(1) | [Article abstract](https://www.researchgate.net/publication/369001039_Knowledge_Graph-Based_Reinforcement_Federated_Learning_for_Chinese_Question_and_Answering), [DOI](https://doi.org/10.1109/TCSS.2023.3246795) | A multitask BART parser predicts question categories and SPARQL statements. An RL-based fusion strategy combines models across institutions. | 2.4 federated semantic parsing and Text-to-SQL | yes | abstract |
| FedV-KGQA: Multi-Hop Question Answering over Vertically Partitioned Knowledge Graphs | Bappy and Seneviratne, 2026 | ISWC 2026 | [arXiv](https://arxiv.org/abs/2608.24846) | Combines local graph enrichment and embeddings with entity anchoring for multi-hop answer ranking across organizations with disjoint relations. Raw triples and relation parameters stay in each silo. | 2.4 federated semantic parsing and Text-to-SQL | no | full text |
| OpenSQL: Data-Efficient Text-to-SQL for Open-Source LLMs via Synthesized Intermediate Supervision | Hu et al., 2026 | PVLDB 19(7) | [Author copy](https://dbgroup.cs.tsinghua.edu.cn/ligl/papers/VLDB26-OpenSQL.pdf) | Derives supervision for intermediate decisions from existing question-SQL pairs and uses it to train open models. Reports BIRD-dev results using 14K training samples for its 32B model. | 2.1 fine-tuned models for Text-to-SQL | no | abstract |
| MSI-SQL: Unleashing Data Potential of Large Language Models for Text-to-SQL via Multi-Task Self-Iterative Generation | Gao et al., 2026 | Findings of EMNLP | [ACL Anthology](https://aclanthology.org/2026.findings-emnlp.2390/) | Builds training data through a verification-based iterative generation loop for difficult examples. An auxiliary masked SQL completion task constrains the reasoning traces, and the paper evaluates on BIRD and Spider. | 2.1 fine-tuned models for Text-to-SQL | no | abstract |
| Leveraging Open-Source Language Models for Privacy-Preserving Text-to-SQL Generation in Electronic Health Records | Chan and Kuo, 2026 | ROCLING | [ACL Anthology](https://aclanthology.org/2026.rocling-main.1/) | Studies domain fine-tuning of open models for clinical Text-to-SQL so sensitive data can stay within the deployment environment. | 2.1 fine-tuned models for Text-to-SQL | no | abstract |
| PLUM: Improving Code LMs with Execution-Guided On-Policy Preference Learning Driven By Synthetic Test Cases | Zhang et al., 2024 | arXiv preprint | [arXiv](https://arxiv.org/abs/2406.06887) | Generates tests from natural language instructions, executes code sampled from the current policy to build preference data, and trains that policy. Evaluates on HumanEval, MBPP, and LiveCodeBench. | 2.2 preference optimization and execution feedback | no | abstract |
| Not All Verifiable Preference Pairs Are Equal: Support-Aware Filtering for Stable Iterative DPO | Ngo et al., 2026 | IJCNLP-AACL, short paper | [ACL Anthology](https://aclanthology.org/2026.aacl-short.51/) | Distinguishes pairs with two on-policy outputs from fallback pairs whose chosen answer comes from the dataset. Tests different filters for the two pair types on GSM8K and MATH-500 with models from 0.5B to 3B. | 2.2 preference optimization and execution feedback | no | abstract |
| Fine-tuning text-to-SQL models with reinforcement-learning training objectives | Nguyen, Phan, and Piccardi, 2025 | Natural Language Processing Journal 10 | [Published PDF, university repository](https://opus.lib.uts.edu.au/rest/bitstreams/56c2c672-5579-4a3d-a74c-e04b21f61fda/retrieve) | Fine-tunes smaller BART and T5 models with policy gradients and a reward designed to better match SQL evaluation measures. It reports gains in exact match and execution accuracy over supervised baselines. | 2.2 preference optimization and execution feedback | no | abstract |
| ReEx-SQL: Reasoning with Execution-Aware Reinforcement Learning for Text-to-SQL | Dai et al., 2026 | ACL | [ACL Anthology](https://aclanthology.org/2026.acl-long.35/) | Uses stepwise rollouts that incorporate SQL engine feedback while the model reasons and decodes. Its composite reward encourages database exploration, with results on Spider and BIRD at 7B. | 2.2 preference optimization and execution feedback | no | abstract |
| EvoSQL: Memory-Augmented Critic-Generator Co-Evolution for Text-to-SQL | Zhou et al., 2026 | Findings of EMNLP | [ACL Anthology](https://aclanthology.org/2026.findings-emnlp.717/) | Maintains candidate memory and verifies candidate SQL with execution feedback and an LLM critic. A self-distillation policy optimization stage fine-tunes the generator and critic using execution-aware supervision. | 2.2 preference optimization and execution feedback | no | abstract |
| SQL-Trail: Multi-Turn Reinforcement Learning with Interleaved Feedback for Text-to-SQL | Hua et al., 2026 | ACL | [ACL Anthology](https://aclanthology.org/2026.acl-long.1677/) | Trains a Text-to-SQL agent to refine queries through repeated database interactions. The reward combines SQL correctness and efficient exploration, and a turn budget adapts to question difficulty. | 2.2 preference optimization and execution feedback | no | abstract |
| Private Federated Learning using Preference-Optimized Synthetic Data (POPri) | Hou et al., 2025 | ICML | [PMLR](https://proceedings.mlr.press/v267/hou25g.html) | Uses private client feedback as a reward to fine-tune an LLM with DPO and generate differentially private synthetic text. Evaluates the synthesized data on LargeFedBench and an existing benchmark. | 2.3 federated fine-tuning of LLMs | no | full text |
| APPA: Adaptive Preference Pluralistic Alignment for Fair Federated RLHF of LLMs | Srewa, Zhao, and Elmalaki, 2026 | arXiv preprint | [arXiv](https://arxiv.org/abs/2604.04261) | Dynamically reweights group rewards using historical alignment scores, targeting a shared policy that serves multiple groups with diverse human preferences. | 2.3 federated fine-tuning of LLMs | no | full text |
| Federated Variational Preference Alignment with Gumbel-Softmax Prior for Personalized User Preferences | Koo et al., 2026 | arXiv preprint | [arXiv](https://arxiv.org/abs/2605.30873) | Learns separated preference prototypes from decentralized data using a shared mixture prior and a loss that encourages separation. Evaluates preference switching on HH-RLHF. | 2.3 federated fine-tuning of LLMs | no | abstract |
| A Federated Adaptive Large Language Model Fine-Tuning Framework for Software Development | Chen et al., 2026 | IEEE Transactions on Services Computing 19(1) | [Article abstract](https://eurekamag.com/research/104/750/104750411.php), [DOI](https://doi.org/10.1109/TSC.2025.3623626) | F-CodeLLM collaboratively fine-tunes code models across organizations and adapts training to limit communication and computation. The authors report performance comparable to centralized fine-tuning and gains from sharing knowledge across programming languages. | 2.3 federated fine-tuning of LLMs | no | abstract |
| OpenFedLLM: Training Large Language Models on Decentralized Private Data via Federated Learning | Ye et al., 2024 | ACM KDD | [arXiv](https://arxiv.org/abs/2402.06954), [Proceedings DOI](https://doi.org/10.1145/3637528.3671582) | Supports federated instruction tuning and human preference alignment with seven federated algorithms. It assesses training across several domains. | 2.3 federated fine-tuning of LLMs | yes | full text |
| Is Decentralized LLM Agent RL Robust to Heterogeneity? An Asymmetric Tale (FedAgent) | Chen et al., 2026 | NeurIPS, acceptance reported by the authors | [Project abstract and paper](https://fed-agent.github.io/) | Uses federated reinforcement learning to train language agents across local environments. Studies why changing task distributions and changing environment dynamics affect training differently. | 2.3 federated fine-tuning of LLMs | no | full text |
| PubSwap: Public-Data Off-Policy Coordination for Federated RLVR | Nayak et al., 2026 | ICML workshop on offline datasets to online adaptation | [Workshop PDF](https://openreview.net/pdf/f0497bf368ccfbf6e35f57de9fc960bf0322a583.pdf) | Combines LoRA-based federated RL with occasional off-policy steps that substitute verified correct responses from other clients on shared public prompts. Evaluates mathematical and medical reasoning. | 2.3 federated fine-tuning of LLMs | yes | full text |

## Against the novelty claim

**FedParsing makes the unqualified claim that FL4SP was the only earlier work unsafe.** The public manuscript describes federated Text-to-SQL training on WikiSQL. Its authors, exact date, and publication status could not be verified. FL4SP was the only proceedings paper verified in this scan that federates training of a Text-to-SQL parser. I found no earlier paper in the sources checked that combines federated Text-to-SQL training, client-side execution against gold results, and DPO pairs rebuilt from the current model's outputs every round.

### Federated training of semantic parsers

- **FedParsing.** Section 1 states, “We apply Federated Learning to semantic parsing which is called FedParsing Model.” Sections 3.2 and 4.1 describe averaging the server and client decoders and evaluating on WikiSQL. Clients learn from a Mean Teacher using a consistency loss on unlabeled questions. [OpenReview submission, §§1, 3.2, and 4.1](https://openreview.net/pdf?id=Oeikp9N4fzi)
- **FL4SP.** The abstract says, “we re-purpose widely-used single-domain text-to-SQL datasets as clients to form a realistic heterogeneous FL setting and collaboratively train a global model.” The paper trains T5-base with supervised targets and reweights client updates by loss reduction. [ACL paper](https://aclanthology.org/2023.acl-long.678.pdf)
- **KGRFL.** The abstract describes a parser that “identifies question categories while converting questions into SPARQL statements” and an “RL-based model fusion strategy.” Its target language is SPARQL. The abstract attaches RL to model fusion. The 2024 issue year differs from the 2023 online date. [Article abstract](https://www.researchgate.net/publication/369001039_Knowledge_Graph-Based_Reinforcement_Federated_Learning_for_Chinese_Question_and_Answering), [DBLP issue record](https://dblp.org/pid/54/3420-9.html)

The RESDSQL-fed repository documents a federated T5-base fine-tuning command on Spider. A completed run and an associated paper were unverified. [Repository README](https://github.com/cirnoooo123/RESDSQL-fed/blob/main/README.md#federated-training-on-spider)

FedV-KGQA fuses graph embeddings and trains an answer-ranking model at the server. The DEBS poster on federated CEP rule generation aggregates local edits to rules after testing them on event streams and uses prompting for the LLM. [FedV-KGQA, §4](https://arxiv.org/html/2608.24846), [DEBS poster, §2](https://pure.uva.nl/ws/files/201121899/24-LLM4CEP.pdf)

### Federated learning from verified rollouts

- **PubSwap.** “During each communication round, every client performs τ local GRPO steps.” Each step samples new responses to private prompts, and the protocol adds periodic off-policy exchanges on public prompts. This is a precedent for client-generated, verifiable rollouts and LoRA averaging in math and medicine. [Workshop PDF, §§3.2–3.4](https://openreview.net/pdf/f0497bf368ccfbf6e35f57de9fc960bf0322a583.pdf)
- **Fed-GRPO (Guo et al.).** “For coding tasks, we use Qwen2.5-3B-Instruct as the base model, train on the MBPP dataset” (§5.1). The math configuration specifies eight rollouts and a binary correctness reward. Its code benchmark makes it a closer comparison than math-only federated RL. The exact MBPP verifier was unverified. [arXiv full text, §§3–5 and Appendix A](https://arxiv.org/html/2610.11502)
- **FedMOA.** “Experiments on mathematical reasoning and code generation benchmarks demonstrate that FedMOA consistently outperforms federated averaging.” It uses local online GRPO under heterogeneous reward definitions, with accuracy as the primary objective and auxiliary format-related objectives. [arXiv abstract](https://arxiv.org/abs/2602.00453), [Methods and experiments](https://arxiv.org/html/2602.00453)
- **FGRPO (Chen et al.).** “A binary reward of 1 is assigned if the prediction matches the reference, and 0 otherwise.” Each client starts from the round's global model and samples repeatedly from its current local policy. The experiments use vision-language mathematical reasoning. [arXiv full text, §§3.2.1 and 4.1](https://arxiv.org/html/2606.03094)
- **FedGRPO (Zhu et al.).** “the client performs an exact-answer check” when it holds a trusted reference answer. Clients can also use learned evaluators for server-generated candidates. The server's foundation model is the policy updated with these signals. [arXiv full text, §3.3](https://arxiv.org/html/2602.12014), [AAAI proceedings](https://ojs.aaai.org/index.php/AAAI/article/download/39027/42989)
- **FedAgent.** “the client collects a batch of trajectories” by interacting with its own environment using its current policy. Clients start from the broadcast model, optimize local returns with GRPO or PPO, and send model updates for aggregation. The authors evaluate WebShop and ALFWorld, including Qwen2.5-1.5B. This is a close precedent for private-environment rollouts inside federated rounds. [Project abstract and paper, §2.2](https://fed-agent.github.io/)
- **SemFed.** “Each client extracts compact semantic policy summaries from local training trajectories”. It shares those summaries across clients and uses interactive agent environments, including ALFWorld and WebShop. [ACL Anthology abstract and paper](https://aclanthology.org/2026.findings-emnlp.1147/)
- **Fed-SE.** “The agent first interacts with the local environment using the current policy to generate exploration trajectories.” It filters by binary task success and fits the successful trajectories with maximum likelihood. This is the closest checked precedent for the client-side rejection-sampling control. [arXiv full text, §§2–3.2](https://arxiv.org/html/2512.08870)
- **POPri.** After a DPO step, the authors “generate new synthetic data using the newly fine-tuned” model. The server generates samples and runs DPO on pairs rebuilt each round with a fixed reference. Clients score samples by embedding similarity to private text and share securely aggregated scores. This is iterative DPO with decentralized feedback and centralized policy updates. [ICML proceedings](https://proceedings.mlr.press/v267/hou25g.html), [Method, §3](https://arxiv.org/html/2504.16438)

CodeLutra remains the closest centralized comparison for the training loop. PLUM adds a code-generation precedent for executing current-policy samples to build pairs. Ngo et al. add a small-model precedent for distinguishing self-sampled pairs from gold-answer fallback pairs. [CodeLutra](https://arxiv.org/abs/2411.05199), [PLUM](https://arxiv.org/abs/2406.06887), [Ngo et al.](https://aclanthology.org/2026.aacl-short.51/)


## Search log

Counts below are results screened from each returned batch at title or snippet level. They include duplicate records across queries and sources. They are distinct from the abstract and full-text checks recorded above. The 16 main keyword searches included `after:2022-12-31 before:2026-11-28`. The initial three-query batch and targeted follow-ups also allowed older records.

### Citation searches

Scholar Cited by lists screened · 0 for each of FL4SP, CodeLutra, FedBiscuit, OpenFedLLM, PubSwap, Fed-GRPO, and KGRFL. The route was inaccessible. The checks below used other routes.

- **FL4SP** · 3 citing records checked directly in references: FedLFC, EvoSchema, and SafeNLIDB. The accessible ResearchGate version listed no resolved citations. [FedLFC PDF](https://aclanthology.org/2024.findings-naacl.98.pdf), [EvoSchema PDF](https://www.vldb.org/pvldb/vol18/p3655-zhang.pdf), [SafeNLIDB manuscript](https://www.researchgate.net/publication/397481441_SAFENLIDB_A_Privacy-Preserving_Safety_Alignment_Framework_for_LLM-based_Natural_Language_Database_Interfaces)
- **CodeLutra** · 1 citing record verified. Code-Driven Planning in Grid Worlds cites it as a code-generation example and evaluates prompting on grid-world tasks. The citation index page for CodeLutra itself was inaccessible. [Citing paper, ref. 50](https://arxiv.org/html/2505.10749)
- **FedBiscuit** · 1 citing record checked in references, the review on protecting LLM and agent data privacy. The visible ResearchGate record for the earlier title listed 0 citations, and the alternative citation page was inaccessible. [Citing review](https://journal.hep.com.cn/hcc/EN/1160602939335172801)
- **OpenFedLLM** · 16 entries screened on arXiv.gg's Cited By list. Relevant links included FedBiscuit. Targeted search also verified a reference in FedDCA and described use of the framework in FLEx. [Cited By list](https://arxiv.gg/abs/2402.06954#cited-by), [FedDCA](https://aclanthology.org/2025.findings-emnlp.52.pdf), [FLEx submission](https://openreview.net/pdf?id=T4dvY146Tk)
- **PubSwap** · 0 forward citations verified. The accessible paper's reference list led to FedAgent and FedMOA. [Workshop PDF](https://openreview.net/pdf/f0497bf368ccfbf6e35f57de9fc960bf0322a583.pdf)
- **Fed-GRPO (Guo et al.)** · 0 forward citations verified. Its paper cites FGRPO. The full text did not contain a PubSwap citation. [Fed-GRPO full text](https://arxiv.org/html/2610.11502)
- **KGRFL** · 6 visible entries screened from a ResearchGate record that displayed 11 citations, plus 1 independently found reference in the South China Normal University journal. The closest candidate was FedV-KGQA. Its primary paper describes embedding fusion and answer ranking, as detailed above. [Partial citing list](https://www.researchgate.net/publication/369001039_Knowledge_Graph-Based_Reinforcement_Federated_Learning_for_Chinese_Question_and_Answering), [SCNU paper](https://journal-n.scnu.edu.cn/cn/article/pdf/preview/10.6054/j.jscnun.2025059.pdf)
- **FedAgent follow-up** · 2 later citing texts checked. Federated Agent Optimization develops a problem formulation, and Federated Recommender Agents keeps LLM parameters fixed. [Federated Agent Optimization](https://arxiv.org/html/2610.01195), [Federated Recommender Agents](https://arxiv.org/html/2610.39289)

The following were title-based citation discovery queries. Their counts include records that mention an anchor without citing it.

- `"Federated Learning for Semantic Parsing" Zhang (cites OR citations OR Lorar OR FL4SP)` · 16
- `"CodeLutra" (SQL OR DPO OR cites OR citations)` · 15
- `("FedBiscuit" OR "Federated Binary Preference Selectors") (preference OR citations)` · 16
- `"OpenFedLLM" (FedDPO OR citations OR preference OR verifiable)` · 16
- `"PubSwap" "federated" (GRPO OR citations OR reinforcement)` · 15
- `"Fed-GRPO" "Guo" (federated OR citations OR reinforcement)` · 19
- `("KGRFL" OR "Knowledge Graph-Based Reinforcement Federated Learning") (SPARQL OR citations OR Chinese)` · 18

### Keyword searches

- `federated text-to-SQL` · 39
- `federated NL2SQL` · 18
- `federated semantic parsing` · 29
- `privacy-preserving text-to-SQL fine-tuning` · 34
- `federated direct preference optimization` · 24
- `federated RLHF preference alignment LLM` · 32
- `federated reinforcement learning verifiable rewards LLM` · 30
- `federated code generation LLM fine-tuning` · 31
- `execution feedback DPO SQL` · 17
- `on-policy iterative DPO text-to-SQL` · 24
- `self-play self-improvement text-to-SQL small model` · 33
- `"federated learning" ("text2sql" OR "text-to-SQL" OR "NL-to-SQL" OR "text to SQL") Spider WikiSQL BIRD parser` · 19
- `("federated" OR "decentralized") ("text-to-SPARQL" OR "text-to-Cypher" OR "semantic parser") training` · 18
- `"federated" "online DPO" on-policy preference optimization verification code` · 13
- `federated GRPO code execution tests programming reinforcement learning FL rollout` · 21
- `"隐私" "联邦学习" ("Text-to-SQL" OR "自然语言转SQL" OR "语义解析") 模型` · 17

### Additional searches

- `federated text-to-SQL or NL2SQL semantic parsing WikiSQL Spider BIRD KGRFL training federated model` (arxiv.org, aclanthology.org, openreview.net, ieeexplore.ieee.org) · 22
- `federated GRPO RLVR execution rewards federated reinforcement learning verifiable code reasoning LLM collaborative FedAvg` (arxiv.org, aclanthology.org, openreview.net) · 22
- `federated online DPO on-policy verifier preference optimization self-generated samples local client verification LLM` (arxiv.org, aclanthology.org, openreview.net) · 22
- `text-to-SQL self-evolving execution feedback online DPO iterative preference small language model SQL Zero EXPO SQL STaR` (arxiv.org, aclanthology.org, openreview.net) · 19
- `"FedParsing" "WikiSQL" "a Semi-Supervised Federated Learning Model on Semantic Parsing"` · 2
- `"2305.17221" "2411.05199" Semantic Scholar OpenAlex` · 0
- `"10.1109/TCSS.2023.3246795" KGRFL Xu IEEE` · 18
- `federated natural language to SQL WikiSQL federated parsing HydraNet text2SQL distributed training FL` · 24
- `"federated" ("SQL generation" OR "Text2SQL" OR "text-to-SQL") (fine-tune OR fine-tuning OR LoRA) "clients"` · 14
- `federated reinforcement learning code generation online policy test cases RLVR client aggregation consensus verifier FedRLVR` · 20
- `"Federated Learning for Semantic Parsing" OR "CodeLutra" OR "PubSwap" site:semanticscholar.org` · 2
- `"OpenFedLLM" OR "Towards Federated RLHF with Aggregated Client Preference" OR "Knowledge Graph-Based Reinforcement Federated Learning" OR "Fed-GRPO: Reward-Signal-Driven" site:semanticscholar.org` · 0
- `federated learning to train Text-to-SQL, NL2SQL or semantic parsing models, Spider, BIRD, WikiSQL, FedParsing, 2023-2026` · 12
- `federated DPO or federated RL with verifiable rewards, on-policy generations at clients, code execution, SQL, LLM, federated GRPO, 2023-2026` · 12
- `direct preference optimization Text-to-SQL 2023-2026 with self-generated SQL, execution feedback, on-policy iteration, small model` · 12

Combined counts are used when the search tool returned one merged batch for several queries.

- `"federated" "text-to-sql" training fine-tuning FL4SP semantic parsing privacy federated learning NL2SQL`. `"federated" "NL2SQL" fine tuning model federated learning`. `"federated semantic parsing" FL4SP Text-to-SQL follow up` · 16
- `FedParsing a Semi-Supervised Federated Learning Model on Semantic Parsing text to SQL Wang authors DOI` · 20
- FL4SP title and `cited by` or `OpenAlex` or `Semantic Scholar`. `"FedParsing" "Oeikp9N4fzi" OpenReview 2021 2022 ACL`. KGRFL title restricted to DBLP, IEEE, or Crossref · 13
- `"federated reinforcement learning" "GRPO" "rollouts" language model agents client verification PubSwap federated LR 2026`. `"federated" "Text-to-SQL" (FedParsing OR RESDSQL-fed OR FL4SP OR FedSQL OR FL-SQL OR FedText2SQL)`. `"federated" "text-to-SQL" ("preference" OR "reinforcement learning")` on arXiv, ACL Anthology, and OpenReview. `"federated" ("on-policy" OR "on policy") ("DPO" OR "preference optimization") ("execution" OR "verifiable" OR "reward")` on arXiv and OpenReview · 18
- FL4SP exact author and title search excluding the anchor pages / FL4SP DOI plus `references` / FL4SP title plus SafeNLIDB, EvoSchema, or FedLFC · 18
- `"SafeNLIDB" "Federated Learning for Semantic Parsing"`. `"EvoSchema" "Federated Learning for Semantic Parsing"` · 13
- FedBiscuit's earlier title and `arxiv FedBiscuit` / F-CodeLLM journal title and DOI / exact code-summarization title plus primary publisher terms / `"PLUM" "Execution-Guided On-Policy Preference Learning" proceedings venue COLM NeurIPS ICML ACL` · 19
- `"CodeLutra" citations researchgate cited by arxiv 2411.05199`. `"F-codeLLM" federated large language models practical software development Chen`. `"RESDSQL-fed" cirnoooo123 federated training Spider thesis`. `"Fed-GRPO" "PubSwap" cites related work FedMOA semanticscholar OpenAlex` · 17
- F-CodeLLM and ICSE DOI. OpenFedLLM and KDD DOI. FedVPA-GP title and arXiv ID plus workshop and OpenReview · 19
- FedV-KGQA exact title with `IEEE abstract federated semantic parsing SPARQL`. `"federated" "knowledge base question answering" train semantic parser SPARQL LLM FedV-KGQA KGRFL`. `"federated" "semantic parsing" SPARQL train language model KGRFL FedV-KGQA FedKGQA` · 15
- CEP poster exact title and `federated complex event processing authors abstract`. `"federated" "complex event processing" "rule generation" LLM verification FL SQL natural language model updates` · 16
- POPri title on PMLR. Zhu et al.'s FedGRPO title on the AAAI site. PubSwap title plus ICML workshop title. F-CodeLLM journal title and DOI suffix on IEEE Xplore · 14
- `"FedAgent" "GRPO" Chen 2026 federated agent reinforcement learning LLM arxiv`. `"FedAgent" "federated" "GRPO" LoRA ALFWorld WebShop Chen` · 17
- `"Is Decentralized LLM Agent RL Robust to Heterogeneity? An Asymmetric Tale" NeurIPS 2026 OpenReview Chen` · 14
