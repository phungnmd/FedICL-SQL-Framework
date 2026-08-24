# FedLS-SQL — System Architecture

> Canonical design record from 2026-08-19. It supersedes the FedICL-SQL and
> Fed-ICKD framing. Exact commands live in `PIPELINE_NEXT.md`; empirical history
> lives in `LAB_LOG.md`; canonical paper tables live in
> `paper/results/MAIN_RESULTS.md`; superseded documents are retained under
> `paper/archive/pre_fedls_2026-08/`.

## 1. Research problem

FedLS-SQL studies whether collaboration between a server-side large language
model (LLM) and federated small language models (SLMs) can overcome the accuracy
limitations of lightweight federated NL-to-SQL while preserving its privacy,
communication-efficiency, and resource advantages.

The project answers four questions:

1. **Accuracy:** does server-side LLM-to-SLM transfer improve federated
   NL-to-SQL over pure FL and centralized SLM training?
2. **Efficiency:** can the method remain practical for resource-constrained
   clients and communicate only parameter-efficient updates?
3. **Federated behavior:** how does LLM guidance affect convergence and
   generalization under non-IID data?
4. **Trade-offs:** what accuracy is obtained for the communication, training,
   and inference cost?

## 2. System setting and privacy boundary

Client `i` owns a private database/schema `S_i` and private examples
`Q_i = {(question, gold_SQL)}`. Spider training databases are partitioned among
clients; the current headline split uses `K=5`, Dirichlet `alpha=0.5`, seed 0.

Only LoRA adapter parameters are exchanged. Raw rows, database contents,
schemas, questions, and SQL never leave a client. The server-side teacher sees
only the public pool. This is a **structural data-isolation claim**, not formal
differential privacy, secure aggregation, or protection against information
inference from model updates.

## 3. Models, data, and training units

| Component | Canonical setting |
|---|---|
| Client/deployed SLM | `Qwen/Qwen2.5-1.5B-Instruct` |
| Server LLM teacher | `Qwen/Qwen2.5-Coder-7B-Instruct`, frozen |
| Client adaptation | LoRA, default `r=16`, `alpha=32` |
| Private training | Spider non-IID client shards |
| Primary Qwen KD pool | teacher-specific `N_qwen=3,873` BIRD targets retained by quick-exec and official EX |
| Primary test | Spider dev, 1,034 rows |
| Robustness tests | Spider-Realistic, Spider-Syn, Spider-DK |
| Cross-corpus test | BIRD dev, disjoint evaluation databases |

The public targets are constructed once per frozen-teacher lineage:

1. the frozen teacher generates SQL zero-shot on public BIRD examples;
2. the SQL must pass the fixed 8-second quick-execution filter;
3. survivors must match the gold execution result under the official EX scorer;
4. the retained teacher SQL becomes the public hard target;
5. teacher logits on the same target span are cached.

### Teacher-specific KD-pool invariant

For a frozen teacher `T` and the complete public source `D_public`, define

```text
P_T = {(x, y_hat_T) in D_public : QuickExec_8s(y_hat_T) = 1
                                      and EX(y_hat_T, y_gold) = 1}
N_T = |P_T|
```

FedLS-SQL trains on the retained **teacher-generated SQL** `y_hat_T` and its
teacher logits; BIRD gold is only the execution oracle and matched-control
target. Therefore `P_T`, `N_T`, selected source indices, SQL targets, and logit
cache are teacher-specific artifacts. Replacing the teacher requires rebuilding
all of them from the complete `D_public`. A retained count such as 3,873 is an
observed output for one teacher, never a method hyperparameter or portable
public-data budget.

BIRD gold SQL is used for result-based filtering, not as the canonical method's
training target. In the primary Qwen lineage, a matched causal control replaces
the teacher SQL with BIRD gold on the exact same `N_qwen=3,873` row identities;
it is an ablation, not a FedLS-SQL component. Changing the pool or teacher cache
creates a new result lineage.

## 4. End-to-end method

```text
OFFLINE AT SERVER
  frozen 7B teacher + public BIRD schemas/databases
    -> teacher SQL generation
    -> fixed 8-second quick-execution filter
    -> official EX-match filter
    -> Qwen-specific N_qwen=3,873 target pool + teacher-logit cache

FOR ROUND t = 1..T
  server broadcasts global SLM LoRA adapter theta_(t-1)

  each client i:
    train theta_i on private Q_i with gold cross-entropy
    upload theta_i only

  server:
    sample-weighted factor-wise FedAvg -> theta_FL,t
    public CE + reverse-KL distillation -> theta_FedLS,t
    broadcast theta_FedLS,t

DEPLOYMENT
  SLM + final LoRA adapter -> greedy zero-shot NL-to-SQL inference
```

No in-context examples are used in the canonical client training, server KD,
or evaluation protocol (`train_k=0`, `k_teacher=0`, `eval_k=0`).

## 5. Optimization objectives

### 5.1 Client objective

Each client trains only on its private gold SQL:

```text
L_client = CE(q_student, y_private)
```

### 5.2 Federated aggregation

The default aggregator is sample-weighted factor-wise FedAvg over compatible
LoRA adapters:

```text
theta_FL,t = sum_i (n_i / sum_j n_j) * theta_i,t
```

FLoRA-NA was evaluated but did not improve the retained comparisons and is not
a contribution of FedLS-SQL.

### 5.3 Server LLM-to-SLM transfer

Starting from the aggregated adapter, the server optimizes the SLM on public
teacher targets:

```text
L_server = lambda_CE * CE(q_student, y_teacher)
         + lambda_KD * KL(q_student || p_teacher)
```

This implementation is teacher-target sequence KD plus token-level reverse KL.
It must not be described as a separate “structural distillation” mechanism
unless such a component is later defined, implemented, and ablated.

## 6. Canonical comparisons

The primary final-model comparison is:

| Paper label | Training path | Canonical checkpoint |
|---|---|---|
| Centralized-standard-3ep (official) | one continuous three-epoch Spider run, no FL/KD | `artifacts/baselines/central_3ep_standard_s0/adapter` |
| Centralized-3pass-restart (historical) | three independently scheduled Spider passes, no FL/KD | `artifacts/probe_p/central_3ep/adapter` |
| FL | three pure FedAvg rounds, no teacher/public pool | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter` |
| FedLS-SQL (FL-KD) | three rounds of FedAvg followed by server KD | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g` |

The standard and restart recipes reach `67.31` and `67.60` Spider EX
respectively and are statistically indistinguishable (`p=0.863`). The standard
continuous recipe is the official baseline because it matches conventional
three-epoch training; restart remains schedule-sensitivity evidence.

The `round_2/round_3/fedavg_adapter` objects inside the `fedkd` lineage are not
pure-FL controls: they inherit the previous round's post-KD global adapter.

Additional ablations isolate:

- base SLM;
- centralized SLM fine-tuning;
- pure FL;
- matched BIRD-gold CE on the same public row identities;
- teacher-target CE without teacher logits;
- distillation without private federation;
- full FedLS-SQL;
- teacher direction/objective variants where already measured.

## 7. Evaluation contract

Primary metrics:

- execution accuracy (EX);
- exact match (EM);
- execution-error rate.

Efficiency metrics required by the new paper framing:

- trainable and transmitted parameter counts;
- adapter bytes per client and total bytes per round;
- training wall time and rounds to convergence;
- client/server peak VRAM, with CPU memory where measurable;
- deployed SLM inference latency.

All headline comparisons use the same frozen test rows, greedy decoding, and
`k=0`. Every result must retain its dataset, seed, checkpoint, run
configuration, and Git SHA.

## 8. Current evidence and open gaps

Established evidence:

- FedLS-SQL reaches 69.54 Spider EX at `T=3`, seed 0;
- at T3, FedLS-SQL improves over the independent pure-FL lineage by 5.23 EX
  on Spider (`p=0.0001`), with positive deltas on all four additional tests;
- the `T=1 -> T=3` trajectory improves Spider and all three perturbation sets;
- server KD is strongly beneficial on BIRD cross-corpus evaluation;
- ICL is negative for the tested 1.5B student and is retained only as a
  negative ablation;
- factor-wise FedAvg is the selected aggregator;
- at matched T1 seed 0, public-gold CE is neutral relative to FL (`+0.48 EX`,
  `p=0.800`), teacher-target CE beats public-gold CE by `+3.48 EX`
  (`p=0.0026`), and full FedLS-SQL beats public-gold CE by `+5.51 EX`
  (`p<1e-6`);
- reverse KL adds `+2.03 EX` over teacher-target CE at seed 0, but its existing
  three-seed incremental contrast is not significant and must be presented as
  provisional;
- the server treatment reduces T1 Spider execution errors from 236 to 133;
- in the Gemma family, full FedLS beats pure FL by `+4.25` EX (`p=0.00365`),
  while teacher-target CE beats FL by `+4.06` (`p=0.00698`); full CE+RKL is
  only `+0.19` above target CE (`p=0.916`), so hard-target transfer is the
  clearest common mechanism across the two families;
- Gemma matched-gold CE is a negative control at 41.68 EX and 303 execution
  errors despite using the same 2,487 source identities as the teacher-guided
  arms; its target-form/style mismatch remains under audit.

Open evidence gaps:

1. record the 4-bit Gemma 9B zero-shot Spider reference and audit why matched
   BIRD-gold CE regresses relative to Gemma teacher targets;
2. replicate the final T3 pure-FL versus full FedLS-SQL Spider contrast at
   training seeds 1/2 before submission; currently deferred;
3. finish resource benchmarking with fixed warm-up and exclusive hardware;
4. audit the large server-stage EX-EM divergence and execution-error types.

**Method-freeze gate (2026-08-24):** the architecture above remains the
canonical fallback. P0.9a rejected client disagreement, and P0.9b showed that
global-error hard-target selection is worse than its token/update-matched
random control (`-2.03` Spider EX, `+18` execution errors). Therefore adaptive
selection is not a FedLS-SQL component and its KL extensions are closed. A
different KD/Federated mechanism may still be discussed, but it changes this
architecture only after a new preregistered positive gate; no method change is
currently active.

P0.10a does not alter this freeze. It finds client-model complementarity on a
public diagnostic: execution-result plurality plus global fallback improves
over global FL by 10.55 points, while prefix and preference diagnostics also
clear feasibility thresholds. The first design candidate is therefore an
**LLM-anchored FedDF** server stage, not pure client-ensemble FedDF: the frozen
LLM remains the knowledge anchor and client ensemble information would add a
federated signal on public rows. Its objective, client-logit location,
communication/privacy cost, and matched LLM-only control must be preregistered
before implementation. Until a positive causal gate, the diagram, checkpoints,
and paper method remain unchanged.

New LoRA aggregation is not an active direction. Existing FLoRA-NA and exact
rank-preserving/rank-expanded diagnostics showed no material accuracy headroom
at the current `K=5, T=1` configuration. FedProx remains a possible baseline,
not a proposed component unless later drift evidence changes that decision.

The second-family screen tests the full endpoint inside another compatible
teacher/student family. It does not make reverse KL cross-tokenizer: exact
token-to-ID equality is a hard prerequisite, and arbitrary mixed-family logits
remain unsupported.

The 3,873-row pool above is specific to the canonical Qwen teacher. A
second-family replication must begin with all 9,428 BIRD training rows, run its
own teacher generation, the same 8-second quick-execution filter, and the same
official EX-match stage, then derive its own retained count (`N_gemma` for
Gemma). Its gold, target-CE, and CE+RKL controls share those exact selected
indices. Reusing Qwen's success indices would condition the second-family
result on Qwen and is not method-faithful.

Communication payload accounting is already available from committed round
metrics. With five clients, each round transmits `369,555,560` upload bytes and
`369,555,400` broadcast bytes, or `739,110,960` bytes total; three rounds total
`2,217,332,880` bytes (`2.065 GiB`). Pure FL and FedLS-SQL transmit the same
client-side adapter payload because the teacher stage is confined to the
server. This count excludes transport framing and other protocol metadata.

Outline items not yet supported by current evidence include FedProx, a full
IID/quantity/SQL-pattern skew suite, teacher/student-size sweeps, and an actual
large-model federated baseline. These remain optional experiments, not current
claims.

## 9. Naming and provenance policy

- **Paper/method name:** FedLS-SQL.
- **Legacy paper names:** FedICL-SQL, Fed-ICKD, and Fed-ICL-KD are historical.
- **Internal arm names:** `fedavg`, `fedkd`, and existing run IDs remain stable.
- **Python namespace:** `fedicl_sql` remains unchanged for compatibility.
- **Artifact paths:** never rename old checkpoints or evaluation directories.
- **ICL code:** retained for reproducibility but outside the main method.

Presentation names may change; provenance identifiers must not.
