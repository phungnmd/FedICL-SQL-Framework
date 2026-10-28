# FedLS-SQL — related-work and novelty audit

> What this file is: the limits on what the paper may call new. Written
> 2026-08-26 (P1.4b); not a full bibliography. Links point to primary pages.
>
> It limits claim wording, not the choice of direction. Overlap with a
> mechanism published for another task or domain is not a reason to drop a
> direction (`AGENTS.md`, novelty bar for Q3, owner 2026-10-12).
>
> Updated 2026-10-28 for the frozen method (server Hinton KD, then FedAvg
> rounds with client replay of compressed teacher targets): replay prior
> work, motivation sources and the new wording below. The method does not
> use execution-filtered teacher targets (P2.51 showed no gain).
>
> Claim framing updated 2026-10-02. The tested reference has one public stage;
> placement and subsequent private-round depth remain research variables.
> Recurring KD describes related work or a candidate schedule, not a frozen
> FedLS-SQL method. See `system_architecture.md` and `PIPELINE_NEXT.md`.

## Audit conclusion

The title **must not claim a generic novel federated large/small-language-model
framework**. FedCoLLM already combines client-side SLM LoRA federation with
recurring server-side mutual LLM/SLM distillation on auxiliary data. FedMKT,
FedCoT, and LaDa further establish federated LLM-SLM knowledge transfer as an
active method family. Separately, Struct-SQL already filters teacher-generated
Text-to-SQL supervision by execution correctness. Therefore neither FL+LoRA,
LLM-to-SLM transfer, recurring server distillation, nor execution-filtered SQL
distillation is independently new.

The defensible positioning is narrower (2026-10-28):

> In federated cross-schema NL-to-SQL, a frozen server-only LLM distills into
> the shared SLM on a public corpus before the private rounds; the public-domain
> gain is lost during FedAvg rounds, and clients keep it by replaying a small
> public subset with compressed, precomputed teacher targets (top-50 tokens
> plus tail). Clients send only LoRA adapters; only the SLM is deployed.

This is a task-specific workflow and empirical contribution, not a claim that
its individual optimization components are new. Working title (2026-10-28;
the 2026-09-30 title with "A Novel ... Framework" is withdrawn):

> **Keeping the Teacher's Knowledge: Server-Side LLM Distillation with
> Client-Side Logit Replay for Federated Text-to-SQL**

## Evidence and claim levels (2026-10-02)

| Evidence | Supported claim | Remaining limit |
|---|---|---|
| Public-KD pipeline beats pure FL with the same private rounds and protocol | The complete pipeline improves federated Spider EX at that private budget. | Added public data, selection, and server compute are not isolated. |
| KD also beats gold on the same public rows, private schedule, and controlled training budget | Teacher supervision adds value beyond those gold targets. | SQL-label, soft-logit, and plan effects require their own contrasts. |
| Teacher plan beats SQL-only exposure control and a matched template-plan arm | The teacher-plan task contributes beyond the tested extra exposure and template. | This does not prove the model follows its rationale causally. |
| Gain disappears after longer matched FL training, but target EX is reached earlier | Better private-round efficiency over the measured trajectory. | Report teacher/server cost; do not claim higher converged EX or lower total cost. |

The main empirical question is whether public teacher adaptation helps private
federated Text-to-SQL. A reliable pipeline gain can support a task-specific
empirical paper even if matched gold remains competitive, provided the public
gold result and attribution limit are explicit. It cannot support a claim
that teacher knowledge or CoT is necessary. Gold-equivalent accuracy is not
automatically an unlabeled-public-data result: the present pool admission uses
gold execution results and Hinton uses gold prefixes/CE. Removing public gold
is a different protocol requiring new evidence.

Q3 is a venue target, not a guaranteed outcome of an EX threshold. Novelty,
baseline strength, reproducibility, and journal fit remain independent review
questions. Do not weaken controls or force CoT merely to fit a preferred story.

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
| [KID](https://aclanthology.org/2024.findings-emnlp.403/) (Findings EMNLP 2024) | Centralized Text-to-SQL KD | Large autoregressive teacher → smaller student; imperfect inputs simulate inference errors | Centralized benchmark training; no FL private/public split | EX is an evaluation endpoint, not the defining teacher-target acceptance rule | Teacher distributions/constructed imperfect training data | Autoregressive Text-to-SQL student | Student | Establishes efficient specialized KD for Text-to-SQL. FedLS-SQL's distinction is the federated boundary and server-only transfer, not KD for SQL itself. |
| [Pure-KD Text2Sql](https://aclanthology.org/2025.naacl-industry.5/) (NAACL Industry 2025) | Centralized Text-to-SQL | Stronger pure-prompt teacher → impure-prompt student | Centralized Spider fine-tuning | Reports task accuracy; no generated-target EX acceptance gate | Teacher output distribution under a shorter/purer prompt | Fine-tuned Text-to-SQL model | Student | Establishes Text-to-SQL teacher/student transfer and compact prompting without federation. |
| [Struct-SQL](https://arxiv.org/abs/2512.17053) (arXiv v3, 2026) | Centralized Text-to-SQL structured-CoT KD | GPT-4o → Qwen SLM using query-plan CoT plus SQL | Centralized BIRD construction; no client/server privacy boundary | **Yes:** teacher samples are admitted only when SQL is syntactically valid and execution-correct | Teacher query plan and final SQL; QLoRA student training | Qwen3 4B QLoRA student | Student generates a plan and SQL | Establishes execution-filtered teacher SQL and SLM-only Text-to-SQL deployment. FedLS-SQL differs by federated LoRA aggregation, frozen server refinement, schedule evaluation, and matched FL/public-gold controls. |
| [FedMD](https://arxiv.org/abs/1910.03581) (NeurIPS 2019 workshop) | Heterogeneous federated classification | Client consensus scores on public data → each client | Private data local; shared public dataset | No | Class scores on public data | Heterogeneous client models | Client models | Closest replay pattern: each round clients distill on public data, then train on private data. Its soft targets are the clients' consensus; ours are a frozen server-only LLM's, computed once, on SQL generation. |
| [Zhao et al.](https://arxiv.org/abs/1806.00582) (2018) | Non-IID federated classification | No teacher | A small globally shared public set is mixed into client training | No | Model updates | Shared model | Global model | Public data sharing against non-IID drift. `gmixgold_k2aaa` (gold warm-start plus gold public replay) is this baseline in our setting. |
| [Wang et al.](https://arxiv.org/abs/2305.12132) (Findings NAACL 2024) | Private cross-device FL with a public LLM | Public LLM helps the client model before FL (pretraining on LLM-selected or LLM-generated public data) | Private data local; public data at the server | No | Model updates | Small LM | Small LM | Server-side LLM transfer before FL, close to our K2; no client replay and no study of what the FL rounds forget. |
| [Zhang et al.](https://arxiv.org/abs/2509.01750) (Globecom 2025) | Federated LLM fine-tuning, Banking77 | Server GPT2-large and clients distill shared logits each round on a 2,000-sample public set; the server model is updated | Private data local; shared public set | No | Top-k logits, LoRA projections | LLM/SLM with LoRA | Server and client models | Client-side distillation of server logits on public data every round, with adaptive top-k for communication. Our teacher is frozen, its targets are computed once, the task is SQL generation, and the purpose is retention across private rounds. |
| [DER](https://arxiv.org/abs/2004.07211) (NeurIPS 2020) | Continual learning | Past model's own logits stored in a buffer | Not federated | No | Not federated | Single model | Single model | Source mechanism for logit replay against forgetting; we replay a frozen external teacher's logits, inside FL client rounds. |
| [FedNTD](https://arxiv.org/abs/2106.03097) (NeurIPS 2022), [Flashback](https://arxiv.org/abs/2402.05558) (arXiv 2024) | Federated classification | Global model distills into local training (FedNTD: not-true classes; Flashback: dynamic distillation) | Private data local | No | Model updates | Shared model | Global model | Forgetting of global knowledge during FL is established; they keep the global model's knowledge, we keep a server teacher's public-domain knowledge. FedNTD is our appendix baseline. |
| [PubSwap](https://arxiv.org/abs/2604.12160) (arXiv 2026) | Federated RLVR for math and medical reasoning | No teacher; clients exchange response-level signals on a small public set | Private data local; small shared public set | Verifiable reward (answer correctness) | LoRA updates plus public-set responses | LoRA LLM | Global model | Prior art for ExST: verified on-policy targets used against client drift in FL. FedLS-SQL's ExST verifies by SQL execution on local databases and sits next to a server teacher. |
| [FedMOA](https://arxiv.org/abs/2602.00453) (arXiv 2026) | Federated GRPO, math and code | No teacher | Private data local | Verifiable rewards | Model updates with accuracy-aware aggregation | LLM | Personalized/global models | Federated RL with verifiable reward is prior art; do not claim it for ExST. |
| [AdaFD](https://arxiv.org/abs/2508.20557) (arXiv 2025) | Federated distillation, multi-domain non-IID text | Client ensemble distillation | Private data local | No | Model outputs | Homogeneous or heterogeneous | Global model | Frames non-IID as input-domain shift, as the alpha domain-cluster split does; cite for the heterogeneity framing. |
| **FedLS-SQL (this work)** | Federated cross-schema NL-to-SQL | Frozen server LLM → shared SLM: Hinton KD (gold CE + KL) on the public corpus before FL, then teacher top-50 targets replayed by clients in every private round | Private client NL-SQL rows never leave the clients; the public corpus and teacher targets go to the clients | No (EX is the evaluation metric; execution filtering was tested and dropped) | Client to server: LoRA adapters only; server to client: aggregated adapter, plus once a 2,000-row public subset with compressed teacher targets | Shared 1.5B SLM with LoRA | SLM only; teacher absent from clients and inference | Claim the task-specific workflow, the forgetting finding and its controls, not a new generic FL/KD/PEFT primitive. |

## Contribution-to-prior-work mapping

| Proposed contribution | Nearest work | Safe claim | Prohibited claim |
|---|---|---|---|
| Federated NL-to-SQL setting | Federated Semantic Parsing | Apply and evaluate an asymmetric server-teacher/SLM workflow in a fixed cross-schema federated setting. | “First federated NL-to-SQL/semantic-parsing system.” |
| Adapter-only client training and communication | FedPETuning; FedCoLLM | Quantify the exact LoRA payload used by FedLS-SQL. | “Novel federated LoRA” or privacy from LoRA alone. |
| Optional masked aggregation compatibility | [Bonawitz et al.](https://eprint.iacr.org/2017/281.pdf); [FedProx](https://proceedings.mlsys.org/paper/2020/file/1f5fe83998a09396ebe6477d9475ba0c-Paper.pdf) | Report the separate real-adapter numerical and overhead audit as evidence that the weighted LoRA sum admits a Secure Sum wrapper. | “All experiments used cryptographic Secure Aggregation,” end-to-end MPC, or DP. |
| Server LLM-to-SLM distillation before FL | FedCoLLM; FedMKT; Wang et al. 2024; FedDF | A frozen server-only teacher distills into the shared SLM on public data; measured against the same schedule with gold CE. | “First federated LLM-SLM collaboration” or “first server-side federated KD.” |
| Forgetting of the server stage during FedAvg rounds | FedNTD; Flashback | Measure, per round, how much of the server KD gain on the public domain the private rounds remove. | “First to observe forgetting in FL.” |
| Client-side replay of teacher targets | FedMD; Zhang et al. 2025; DER; Zhao et al. 2018 | Replay a small public subset with precomputed, compressed targets of a frozen server-only LLM inside client rounds; compare with gold replay, server-side training on the same rows, and no replay. | “Novel replay” or “first logit replay in FL.” |
| SLM-only deployment | Struct-SQL; FedCoT | Show that the trained global SLM operates without the LLM at clients or inference. | A measured resource advantage until P1.1b or equivalent evidence is closed. |
| Empirical mechanism evidence | KID; Struct-SQL; FedCoLLM | Report matched target/gold/Hinton-FKL controls, repeated rounds, final seeds, paired EX transitions, and exact communication. | General superiority across teachers, families, federated optimizers, or arbitrary non-IID settings. |

## Manuscript wording

Use this contribution sentence:

> We present FedLS-SQL, a federated NL-to-SQL workflow in which a frozen
> server-only LLM distills into the shared SLM on public data, show that the
> FedAvg rounds remove most of the public-domain gain, and keep it by having
> clients replay a small public subset with compressed, precomputed teacher
> targets.

Use this distinction sentence at the end of Related Work:

> Unlike federated LLM-SLM co-tuning (FedCoLLM, FedMKT), FedLS-SQL neither
> updates nor deploys the server LLM; unlike federated distillation on public
> data (FedMD; Zhang et al., 2025), the client targets come from a frozen
> server-only LLM, are computed once, and serve to keep the server stage's
> knowledge across private rounds of SQL generation.

Motivation for measuring the public domain at all (cite, do not invent):
generalization beyond the participating clients (participation gap, Yuan et
al., ICLR 2022, https://arxiv.org/abs/2110.14216); loss of general ability in
fine-tuning (Lin et al., 2023, https://arxiv.org/abs/2309.06256; SDFT, ACL
2024, https://aclanthology.org/2024.acl-long.58/) and in federated
fine-tuning (FedBE, Huo et al., 2025, https://arxiv.org/abs/2506.05977);
cross-domain evaluation as the definition of the task (Spider, EMNLP 2018).
State that BIRD dev shares the style of the server pool, so the result is
retention of the server's domain, not open-domain generalization.

Privacy related work: MaskSQL (NeurIPS 2025 workshop,
https://arxiv.org/abs/2509.23459) for privacy in LLM-based Text-to-SQL.

Do not use “first”, “novel framework”, “privacy-preserving” without a qualifier,
or “execution verification is novel”. Describe headline privacy as
**structural data isolation**; mention P1.8 only as an optional local Secure Sum
compatibility/overhead audit.

## Audit limits

- This audit covers the closest named method families and current literature
  found through 2026-08-26, plus a 2026-10-11 check: no federated Text-to-SQL
  work with a server LLM teacher was found; PubSwap, FedMOA and AdaFD were
  added. A 2026-10-28 check (arXiv, ACL Anthology, web; Google Scholar not
  reachable) found no federated Text-to-SQL work from 2024-2026 and no paper
  with the exact pattern of one server KD stage followed by client replay of a
  frozen server teacher's precomputed targets; FedMD, Zhao et al. 2018, Wang
  et al. 2024, Zhang et al. 2025, DER, FedNTD and Flashback were added. It is
  not a systematic-review claim.
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
