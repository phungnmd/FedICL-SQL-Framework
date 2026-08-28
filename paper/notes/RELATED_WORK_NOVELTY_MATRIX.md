# FedLS-SQL — related-work and novelty audit

> Completed 2026-08-26 for P1.4b. This is the canonical claim-boundary audit,
> not a complete bibliography. It prioritizes the work nearest to the method's
> federated large/small-model loop, parameter-efficient communication, and
> execution-aware NL-to-SQL supervision. Links point to primary paper pages.

## Audit conclusion

The title **must not claim a generic novel federated large/small-language-model
framework**. FedCoLLM already combines client-side SLM LoRA federation with
recurring server-side mutual LLM/SLM distillation on auxiliary data. FedMKT,
FedCoT, and LaDa further establish federated LLM-SLM knowledge transfer as an
active method family. Separately, Struct-SQL already filters teacher-generated
Text-to-SQL supervision by execution correctness. Therefore neither FL+LoRA,
LLM-to-SLM transfer, recurring server distillation, nor execution-filtered SQL
distillation is independently new.

The defensible positioning is narrower:

> FedLS-SQL studies an execution-oriented workflow for **federated
> cross-schema NL-to-SQL** in which private clients train and communicate only
> SLM LoRA adapters, a frozen server-only LLM supplies SQL targets selected on
> a public corpus by result-equivalent execution, the aggregated SLM is refined
> after each round, and only the SLM is deployed.

This is a task-specific workflow and empirical contribution, not a claim that
its individual optimization components are new. The recommended active title
is:

> **FedLS-SQL: Execution-Verified Large-to-Small Knowledge Transfer for
> Federated NL-to-SQL**

## Nearest-work matrix

Abbreviations: `C→S` = client to server, `S→C` = server to client, `PEFT` =
parameter-efficient fine-tuning, and `NR` = not a defining or reported property
of the cited method.

| Work | Task | Teacher and transfer direction | Private/public boundary | Execution verification | Transmitted object | Client model | Deployed/output model | Difference from FedLS-SQL |
|---|---|---|---|---|---|---|---|---|
| [Federated Learning for Semantic Parsing](https://aclanthology.org/2023.acl-long.678/) (ACL 2023) | Federated semantic parsing using eight single-domain Text-to-SQL datasets as clients | No large teacher; client updates → one global parser | Client semantic-parsing rows stay local | Evaluation concerns parsing accuracy; no teacher-target execution gate | Full model updates under FedAvg/FedOPT/FedProx with loss-reduction reweighting | Shared semantic parser in a cross-silo setup | Global parser | Establishes federated Text-to-SQL/semantic parsing; does not add an LLM teacher, public transfer pool, or adapter-only SLM protocol. |
| [FedPETuning](https://aclanthology.org/2023.findings-acl.632/) (Findings ACL 2023) | General PLM downstream tasks | No asymmetric teacher; federated PEFT | Local downstream data remain at clients | No | PEFT parameters/prompts/adapters | A pretrained language model with a PEFT module | Federated tuned PLM | Establishes federated PEFT efficiency; FedLS-SQL does not claim LoRA federation as new. |
| [FedDF](https://proceedings.neurips.cc/paper/2020/hash/18df51b97ccd68128e994804f3eccc87-Abstract.html) (NeurIPS 2020) | General CV/NLP classification | Client-model ensemble → server global model | Client data remain local; server uses unlabeled or generated proxy inputs | No task-semantic execution oracle | Client models/updates; ensemble predictions are used for server distillation | May be heterogeneous | Refined server model | Establishes post-aggregation server refinement by distillation, but has no external LLM teacher or NL-to-SQL verification. |
| [FedGen](https://proceedings.mlr.press/v139/zhu21b.html) (ICML 2021) | Heterogeneous federated classification | Client prediction rules → server generator → client models | Data-free: server learns a label-conditioned generator without external proxy data | No | Prediction-layer information upward; lightweight generator downward | Heterogeneous user models | Improved user/global models | Establishes data-free federated knowledge transfer; its generated latent features and local regulation differ from public SQL-target refinement. |
| [FedMKT](https://aclanthology.org/2025.coling-main.17/) (COLING 2025) | General NLP text generation | Server LLM ↔ client SLMs through selective mutual KD and token alignment | Clients retain private data; all parties access a public dataset | No task executor | Client and LLM logits on public data | Homogeneous or heterogeneous SLMs | Both server LLM and client SLMs are enhanced | Broad LLM-SLM federation and public-data transfer are prior art. FedLS-SQL is one-way into a shared global SLM, keeps the teacher frozen, and verifies SQL by EX. |
| [FedCoLLM](https://arxiv.org/abs/2411.11707) (arXiv v3, 2026) | General QA/text generation | Aggregated SLM ↔ server LLM mutual KD on auxiliary data after each FL round | Private client data stay local; auxiliary data are server-side; paper supports secure aggregation | No task executor | SLM LoRA adapters between clients/server; LLM/SLM distributions interact on server | Shared SLM with LoRA | Both tuned LLM and global/client SLM | **Closest architectural prior:** it already has LoRA clients, aggregation, recurring server KD, and rebroadcast. FedLS-SQL differs through frozen one-way teacher guidance, execution-matched public SQL targets, EX-first causal controls, and SLM-only deployment. |
| [FedCoT](https://aclanthology.org/2025.findings-emnlp.454/) (Findings EMNLP 2025) | General text-generation/reasoning tasks | Server LLM → client task-specific SLM via CoT rationales | Client prompts are perturbed using exponential-mechanism strategies before server use; rationales return to clients | No task executor | Perturbed prompts and generated/decoded rationales | Task-specific SLM at each client | Client SLM | Establishes privacy-aware server-LLM-to-client-SLM rationale transfer, but not an aggregated global NL-to-SQL SLM or execution-filtered SQL targets. |
| [LaDa](https://arxiv.org/abs/2602.18749) (arXiv 2026) | Federated reasoning distillation | Bidirectional LLM↔SLM transfer with learnability-aware sample allocation and contrastive reasoning-path distillation | Federated local domains; selected samples are allocated by model-pair learnability | No task executor | Selected reasoning examples/signals within a host collaboration framework | Client SLMs | LLM and SLMs in the host framework | Establishes adaptive sample selection and reasoning transfer; FedLS-SQL uses a fixed teacher-specific EX-valid public pool and does not claim learnability-aware allocation. |
| [KID](https://aclanthology.org/2024.findings-emnlp.403/) (Findings EMNLP 2024) | Centralized Text-to-SQL KD | Large autoregressive teacher → smaller student; imperfect inputs simulate inference errors | Centralized benchmark training; no FL private/public split | EX is an evaluation endpoint, not the defining teacher-target acceptance rule | Teacher distributions/constructed imperfect training data | Autoregressive Text-to-SQL student | Student | Establishes efficient specialized KD for Text-to-SQL. FedLS-SQL's distinction is the federated boundary and recurring server-only transfer, not KD for SQL itself. |
| [Pure-KD Text2Sql](https://aclanthology.org/2025.naacl-industry.5/) (NAACL Industry 2025) | Centralized Text-to-SQL | Stronger pure-prompt teacher → impure-prompt student | Centralized Spider fine-tuning | Reports task accuracy; no generated-target EX acceptance gate | Teacher output distribution under a shorter/purer prompt | Fine-tuned Text-to-SQL model | Student | Establishes Text-to-SQL teacher/student transfer and compact prompting without federation. |
| [Struct-SQL](https://arxiv.org/abs/2512.17053) (arXiv v3, 2026) | Centralized Text-to-SQL structured-CoT KD | GPT-4o → Qwen SLM using query-plan CoT plus SQL | Centralized BIRD construction; no client/server privacy boundary | **Yes:** teacher samples are admitted only when SQL is syntactically valid and execution-correct | Teacher query plan and final SQL; QLoRA student training | Qwen3 4B QLoRA student | Student generates a plan and SQL | Establishes execution-filtered teacher SQL and SLM-only Text-to-SQL deployment. FedLS-SQL differs by federated LoRA aggregation, frozen recurring server refinement, direct SQL targets, and matched FL/public-gold controls. |
| **FedLS-SQL (this work)** | Federated cross-schema NL-to-SQL | Frozen server LLM → aggregated global SLM after every round; hard-target CE plus auxiliary same-tokenizer RKL | Private client NL-SQL rows never enter the server pool; server transfer uses public BIRD rows | **Yes:** quick execution followed by official result-equivalent EX-to-gold filtering | Client SLM LoRA adapters only; no private prompt/schema upload to teacher in the canonical protocol | Shared 1.5B/2B SLM with LoRA | Refined SLM only; teacher absent from clients and inference | Claim the complete task-specific workflow and its evidence, not a new generic FL/KD/PEFT primitive. |

## Contribution-to-prior-work mapping

| Proposed contribution | Nearest work | Safe claim | Prohibited claim |
|---|---|---|---|
| Federated NL-to-SQL setting | Federated Semantic Parsing | Apply and evaluate an asymmetric server-teacher/SLM workflow in a fixed cross-schema federated setting. | “First federated NL-to-SQL/semantic-parsing system.” |
| Adapter-only client training and communication | FedPETuning; FedCoLLM | Quantify the exact LoRA payload used by FedLS-SQL. | “Novel federated LoRA” or privacy from LoRA alone. |
| Optional masked aggregation compatibility | [Bonawitz et al.](https://eprint.iacr.org/2017/281.pdf); [FedProx](https://proceedings.mlsys.org/paper/2020/file/1f5fe83998a09396ebe6477d9475ba0c-Paper.pdf) | Report the separate real-adapter numerical and overhead audit as evidence that the weighted LoRA sum admits a Secure Sum wrapper. | “All experiments used cryptographic Secure Aggregation,” end-to-end MPC, or DP. |
| Recurring server LLM-to-SLM refinement | FedCoLLM; FedMKT; FedDF | Freeze the teacher and refine only the aggregated SLM on task-verified public supervision. | “First federated LLM-SLM collaboration” or “first server-side federated KD.” |
| Execution-verified teacher SQL | Struct-SQL; KID; Pure-KD | Integrate result-equivalent teacher-target selection into the private-client/public-server FL loop and validate it against equal-row gold CE. | “First execution-aware Text-to-SQL distillation.” |
| SLM-only deployment | Struct-SQL; FedCoT | Show that the trained global SLM operates without the LLM at clients or inference. | A measured resource advantage until P1.1b or equivalent evidence is closed. |
| Empirical mechanism evidence | KID; Struct-SQL; FedCoLLM | Report matched target/gold/RKL controls, two model families, repeated rounds, two final seeds, paired EX transitions, and exact communication. | General superiority across teachers, families, federated optimizers, or arbitrary non-IID settings. |

## Manuscript wording

Use this contribution sentence:

> We present FedLS-SQL, an execution-oriented federated NL-to-SQL workflow
> that combines private client-side SLM LoRA adaptation with recurring,
> server-only refinement from a frozen LLM on execution-verified public SQL.

Use this distinction sentence at the end of Related Work:

> Unlike prior federated LLM-SLM co-tuning, FedLS-SQL does not update or deploy
> the server LLM; unlike centralized Text-to-SQL distillation, it inserts
> result-verified teacher supervision after aggregation while client data and
> communication remain confined to SLM LoRA updates.

Do not use “first”, “novel framework”, “privacy-preserving” without a qualifier,
or “execution verification is novel”. Describe headline privacy as
**structural data isolation**; mention P1.8 only as an optional local Secure Sum
compatibility/overhead audit.

## Audit limits

- This audit covers the closest named method families and current literature
  found through 2026-08-26; it is not a systematic-review claim.
- FedCoLLM is an arXiv preprint whose current v3 overlaps the architecture more
  closely than its older abstract alone suggests; it must be discussed, not
  hidden behind publication status.
- LaDa and Struct-SQL are also recent preprints. Their claims should be labeled
  accordingly in the manuscript while still being treated as relevant prior
  art.
- The remaining novelty risk is algorithmic: a reviewer may view FedLS-SQL as
  a task-specific FedCoLLM variant plus execution-filtered SeqKD. The paper
  should therefore lead with the NL-to-SQL problem formulation, frozen-teacher
  boundary, causal controls, EX evidence, and reproducible communication—not a
  generic framework claim.
