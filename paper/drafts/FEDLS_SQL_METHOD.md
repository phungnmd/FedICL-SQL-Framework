# 3. FedLS-SQL

> Paper-ready Method draft. Canonical design: `paper/notes/system_architecture.md`.
> Implementation anchors: `fedicl_sql/federated/round_loop.py`,
> `fedicl_sql/federated/aggregate.py`, `fedicl_sql/training/lora_trainer.py`,
> and `fedicl_sql/training/losses.py` in the nested code repository.

## 3.1 Problem formulation and data-isolation boundary

We consider cross-silo federated NL-to-SQL with (K) clients. Client (k)
owns a private dataset

\[
\mathcal{D}_k=\{(x_j,s_j,y_j)\}_{j=1}^{n_k},
\]

where (x_j) is a natural-language question, (s_j) is its database schema,
and (y_j) is the executable gold SQL. All clients share a frozen small
language model (SLM) backbone and optimize only LoRA parameters. We denote the
global adapter entering round (t) by \(\theta^{t-1}\). A larger frozen
teacher (p_{\phi}\) and a separate public corpus \(\mathcal{D}_{pub}\) are
available only at the server.

The trust boundary is structural. Raw client questions, schemas, databases,
and SQL labels remain at their originating clients. The server receives and
broadcasts only SLM LoRA tensors; the teacher never observes private client
examples. This design provides data locality, but it is not differential
privacy, secure aggregation, or a guarantee against leakage from model
updates. Test examples are used only for evaluation and never enter client
training, public-target construction, or retrieval.

## 3.2 Execution-verified public teacher targets

FedLS-SQL constructs a teacher-specific public supervision pool once before
federated training. For every public example \((x,s,y)\in\mathcal{D}_{pub}\),
the frozen teacher generates a SQL query \(\hat y_{\phi}\) without in-context
demonstrations. The generated query is retained only if it (i) executes within
the fixed eight-second quick-execution stage and (ii) returns the same result
as the public gold query under the official execution-accuracy evaluator:

\[
\mathcal{P}_{\phi}=\{(x,s,\hat y_{\phi}):
\operatorname{QuickExec}_{8s}(\hat y_{\phi})=1 \land
\operatorname{EX}(\hat y_{\phi},y)=1\}.
\]

The resulting size \(N_{\phi}=|\mathcal{P}_{\phi}|\) is an observed property of
the teacher, not a tunable data budget. Consequently, replacing the teacher
requires regeneration from the complete public source and reconstruction of
the selected rows, generated targets, and teacher-logit cache. In the main
Qwen configuration, this procedure retains 3,873 of the 9,428 BIRD training
examples. The public gold SQL is the execution oracle and the target of a
matched causal control; the canonical method trains on the verified
teacher-generated SQL.

## 3.3 Federated round lifecycle

Each round contains a private federated stage followed by a public server
transfer stage, as illustrated in Fig. 1.

First, the server broadcasts \(\theta^{t-1}\) to all clients. Client (k)
initializes its local adapter from this common state and performs one local
epoch of teacher-free causal language-model training on \(\mathcal{D}_k\):

\[
\theta_k^t=\arg\min_{\theta}
\frac{1}{n_k}\sum_{(x,s,y)\in\mathcal{D}_k}
\mathcal{L}_{CE}(q_{\theta}(\cdot\mid x,s),y).
\]

Only \(\theta_k^t\) is uploaded. The server validates that all LoRA adapters
share the same tensor keys, shapes, and PEFT configuration, and applies
sample-weighted factor-wise FedAvg:

\[
\theta_{FL}^{t}=\sum_{k=1}^{K}\frac{n_k}{\sum_{j=1}^{K}n_j}\theta_k^t.
\]

This aggregation is the standard federated backbone rather than a claimed new
optimizer. Starting from \(\theta_{FL}^{t}\), the server then refines the SLM
on the complete verified public pool to obtain \(\theta_{FedLS}^{t}\). This
post-server adapter is the global state broadcast at round \(t+1\). Therefore,
the pre-server FedAvg adapters in rounds (t>1) already inherit teacher
knowledge from earlier rounds and must not be reported as independent pure-FL
controls. Pure FL is maintained as a separate lineage with no public server
stage.

### Algorithm 1: one FedLS-SQL round

```text
Input: previous global adapter theta^(t-1), private client datasets D_1...D_K,
       verified public pool P_phi, frozen teacher p_phi

Server broadcasts theta^(t-1)
for each client k in parallel do
    theta_k^t <- LocalLoRA-CE(theta^(t-1), D_k)
    upload theta_k^t                         // no raw client rows
end for
theta_FL^t <- FactorFedAvg({theta_k^t}, weights={n_k})
theta_FedLS^t <- PublicTransfer(theta_FL^t, P_phi, p_phi)
return theta_FedLS^t                         // next-round broadcast
```

## 3.4 Server-side large-to-small transfer

For each \((x,s,\hat y_{\phi})\in\mathcal{P}_{\phi}\), the SLM learns the
verified teacher sequence through hard target cross-entropy. In the full Qwen
configuration, it also minimizes token-level reverse KL over target positions:

\[
\mathcal{L}_{server}=
\lambda_{CE}\mathcal{L}_{CE}(q_{\theta},\hat y_{\phi})+
\lambda_{KD}\mathcal{D}_{KL}(q_{\theta}^{\tau}\|p_{\phi}^{\tau}),
\]

\[
\mathcal{D}_{KL}(q\|p)=
\frac{1}{|\mathcal{M}|}\sum_{u\in\mathcal{M}}
\sum_{v\in\mathcal{V}}q_u(v)
\left[\log q_u(v)-\log p_u(v)\right],
\]

where \(\mathcal{M}\) contains only causal target-token positions. The
implementation computes this term in FP32, applies the conventional
\(\tau^2\) scale, and uses \(\lambda_{CE}=\lambda_{KD}=1\) and \(\tau=1\) in
the canonical configuration. Teacher and student must have identical token-ID
semantics; embedding matrices may differ only by unused padded rows, which are
removed by restricting both distributions to their common vocabulary prefix.
Arbitrary cross-tokenizer logit matching is unsupported.

Hard teacher-target CE is the portable large-to-small mechanism: it improves
over FL in both the Qwen and Gemma families. Reverse KL is retained as an
auxiliary Qwen component because its independent increment is not stable
across seeds and is negligible in the Gemma replication. Accordingly, we do
not describe FedLS-SQL as a new KL objective or as structural distillation.

## 3.5 Communication, deployment, and privacy properties

Each client uploads one LoRA adapter and receives one global LoRA adapter per
round. The main Qwen adapter contains 18,464,768 FP32 parameters, corresponding
to 73,859,072 logical tensor bytes. With five clients, five uploads and five
broadcasts total 738,590,720 logical bytes per round and 2,215,772,160 bytes
through three rounds. Pure FL and FedLS-SQL therefore have the same client
network payload; the teacher computation is confined to the server.

Deployment uses only the SLM backbone and the final adapter
\(\theta_{FedLS}^{T}\), with greedy zero-shot decoding. Neither the teacher nor
the public pool is required after training. In the controlled deployment
benchmark, the BF16 1.5B model is 2.09 times faster and uses 48.73% less peak
allocated VRAM than the 4-bit 7B teacher on the same fixed 32-query protocol.
This measurement supports deployment inference efficiency only; it is not a
training-cost, energy, concurrency, or federated-7B comparison.

Execution accuracy (EX) is the primary task endpoint because it tests whether
the predicted SQL returns the correct result. Exact match (EM) and execution
errors are reported as secondary form and failure diagnostics. The empirical
comparison covers centralized SLM training, pure SLM FL, and FedLS-SQL; no
federated 7B experiment is included or implied.

Figure source: `paper/drafts/figures/fedls_sql_architecture.svg`.
