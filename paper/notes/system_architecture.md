# Fed-ICKD — System Architecture

**Federated In-Context Knowledge Distillation for Text-to-SQL**

> Current design record. Rewritten 2026-07-31 to remove superseded branches.
> Detailed run history belongs in `LAB_LOG.md`; exact CLI flags belong in the
> experiment code and READMEs.

## 1. Goal and research questions

Fed-ICKD trains a small open-source Text-to-SQL model across organizations
without centralizing their databases, schemas, or query logs. A frozen 7B
teacher is used only at the server on public data. Deployment uses the 1.5B
student locally, with no teacher, API call, or server round-trip.

The project answers four questions:

1. **Federation:** can schema/domain-skewed clients collaboratively train a
   useful Text-to-SQL student while exchanging only LoRA adapters?
2. **Aggregation:** does sample-weighted FLoRA-NA improve over factor-wise
   weighted FedAvg for LoRA aggregation?
3. **Knowledge distillation:** after controlling for public-data exposure,
   does server-side reverse-KL distillation improve the aggregated model?
4. **ICL:** does training and evaluating the federated student with private
   client demonstrations help, even though adding demonstrations only at
   inference to a `k=0`-trained centralized model was harmful?

Success is measured primarily by Spider execution accuracy (EX), plus exact
match (EM), execution-error rate, latency, VRAM, and the share of the
base-to-teacher gap recovered:

```text
gap_recovery = (method_EX - base_EX) / (teacher_EX - base_EX)
```

No final claim is made until the complete federated pipeline and the matched
ICL-training comparison have run.

## 2. Setting and privacy boundary

Client `i` owns:

- private database and schema `S_i`;
- private examples `Q_i = {(question, gold_SQL)}`;
- a private ICL demo pool drawn only from `Q_i`.

Spider train databases are partitioned non-IID by domain group. The default
headline setup is `K=8`, Dirichlet `alpha=0.5`; `alpha=0.1` and IID are
robustness settings.

Only LoRA adapters cross the network. Raw rows, schemas, questions, SQL,
demos, and retrieval embeddings never leave the client. The server teacher
never receives client data and sees only the public pool `P`. This is a
structural isolation claim, not formal differential privacy.

## 3. Models and data

| Component | Default |
|---|---|
| Student | `Qwen/Qwen2.5-1.5B-Instruct` |
| Teacher | `Qwen/Qwen2.5-Coder-7B-Instruct`, frozen |
| Adapter | LoRA `r=16`, `alpha=32`, attention + MLP projections |
| Private training data | Non-IID Spider train shards |
| Evaluation | Frozen Spider dev, 1,034 rows |
| Public pool `P` | Frozen 3,873-row BIRD teacher-generated EX-match pool |

The public pool uses BIRD schemas and databases, but not BIRD gold SQL text as
the training target:

1. the teacher generates SQL zero-shot;
2. generated SQL must execute;
3. its execution result must match the BIRD gold result;
4. the retained teacher SQL becomes `y_pub`;
5. teacher logits on `y_pub` are cached offline.

Gold SQL is therefore a row-selection oracle only. All default KD arms must
use the same ordered 3,873 rows and record the pool hash. Smaller pools are
explicit smoke or data-budget ablations.

## 4. End-to-end pipeline

```text
OFFLINE ON SERVER
  Teacher 7B + public BIRD schemas/DBs
  -> zero-shot SQL generation
  -> execution + EX-match filtering
  -> frozen y_pub pool
  -> full-vocabulary teacher-logit cache

ROUND t = 1..T
  Server broadcasts global LoRA adapter theta_(t-1)

  Each client i:
    load theta_(t-1)
    train student on private Q_i with CE
    optionally inject private ICL demos using the matched ICL protocol
    upload the trained adapter only

  Server:
    aggregate client adapters with weighted FedAvg or weighted FLoRA-NA
    optionally continue on P with public CE
    optionally continue on P with public CE + reverse KL
    broadcast theta_t

INFERENCE AT CLIENT
  student + theta_T
  -> k=0 or matched private-demo ICL prompt
  -> greedy decode for the controlled ICL comparison
  -> optional self-consistency execution voting after the base comparison
```

## 5. Client training and ICL

### 5.1 Control condition

The control uses no demonstrations:

```text
train_k = 0
eval_k  = 0
L_client = CE(student(schema, question), gold_SQL)
```

### 5.2 ICL candidate retained for the full-pipeline test

The selected candidate is:

| Setting | Value |
|---|---|
| Retrieval | `dail_weighted` |
| Number of demos | `k=3` |
| Demo format | `question + SQL`, no demo schema (`never_schema`) |
| Demo pool | the same client's private `Q_i` only |
| Train/eval parity | fixed `k=3` at both training and evaluation |
| Training loss | target SQL only (`demo_loss=false`) |
| Schema format | `full` |

`dail_weighted` is selected because it was the best deployable method in the
completed centralized inference-only matrix: 64.60 EX at `k=3`. It still lost
to the matched `k=0` result of 67.31 EX, so this is a **candidate**, not a
positive finding.

The old matrix does not answer the current question: its adapter was trained
with `k=0`, then demos were introduced only at evaluation. It establishes
that unmatched inference-time ICL is harmful, but it does not test:

- in-context training with matched prompts;
- private per-client demo pools;
- non-IID federated training;
- interaction between ICL, aggregation, and server KD.

Therefore ICL remains in the project until the matched federated experiment is
complete.

### 5.3 Implemented ICL execution contract

The federated runner now exposes and fingerprints the complete client ICL
protocol: retrieval method, fixed demo count, demo/schema styles, embedder,
DAIL weights, and shortlist size. For `dail_weighted`, each client generates
and caches draft SQL skeletons using the global student at the start of the
round, then ranks its private candidates with the same weighted DAIL rule used
at evaluation. Missing draft skeletons are fatal; the run cannot silently fall
back to masked-question retrieval while being reported as `dail_weighted`.

The setup identity separates ICL from no-ICL client training, while irrelevant
retrieval flags do not split `k=0` controls. Evaluation fingerprints also
include model, pool, prompt, retrieval, embedder, and DAIL settings, preventing
stale per-round results from being reused under a changed protocol.

Deterministic tests cover private-pool/self-exclusion behavior in the existing
retriever suite, exact client ICL propagation, round-start draft generation,
cache use, setup/fingerprint separation, and the fatal missing-draft path. A
capped GPU smoke remains required before the full run.

### 5.4 ICL decision experiment

The primary comparison is matched and changes only the ICL protocol:

| Condition | Client train | Evaluation |
|---|---|---|
| no ICL | `k=0` | greedy `k=0` |
| ICL | fixed `dail_weighted k=3` | greedy `dail_weighted k=3` |

Run this comparison first on the full proposed federated arm
(`florana_kd`) using identical split, initialization, aggregation, public
pool, server step, seed, and training budget.

To localize any effect, retain the same comparison on `fedavg` or `florana`
if compute allows. Only after the greedy comparison is understood should the
winning training condition be evaluated with self-consistency. This prevents
SC from hiding or manufacturing the ICL effect.

ICL is dropped from the main method only if matched in-context training fails
to improve the federated method across the planned seeds, or if any gain is
dominated by its measured cost. The centralized `k=0`-trained matrix alone is
not a system-level drop gate.

## 6. Federated aggregation

For client weight `p_i = n_i / sum_j(n_j)` and LoRA update
`Delta W_i = B_i A_i`, the desired model-space update is:

```text
Delta W* = sum_i p_i B_i A_i
```

Factor-wise FedAvg instead produces:

```text
(sum_i p_i B_i)(sum_i p_i A_i)
```

which contains cross-client terms and generally differs from `Delta W*`.
It remains the principal aggregation baseline.

Weighted FLoRA-NA finds client-combination coefficients `u,v` such that:

```text
B_hat = sum_i u_i B_i
A_hat = sum_i v_i A_i

minimize || B_hat A_hat - Delta W* ||_F^2
```

The result remains one rank-`r` LoRA adapter. Both aggregators must report:

```text
e_agg = ||Delta W* - B_hat A_hat||_F / (||Delta W*||_F + epsilon)
```

per layer and overall.

## 7. Server distillation

After aggregation, the server may continue the adapter on `P`:

```text
L_server = lambda_ft * CE(student, y_pub)
         + lambda_kd * RKL(q_student || p_teacher)
```

Defaults are `lambda_ft=lambda_kd=1`. Reverse KL is computed over the common
teacher/student vocabulary prefix in float32.

RKD is the current direction:

- centralized `central_rkd - central_ft = +6.09 EX`;
- the paired gain is significant (`p=3.1e-7`);
- KID was 1.45 EX below RKD, but the difference was not significant
  (`p=0.072`, one seed);
- RKD uses fixed targets, so teacher logits can be cached once.

This supports the existence of a KD signal but does not yet prove that
server-side KD improves the complete federated method. That claim requires
`*_kd` versus the matched public-CE control.

## 8. Inference

Greedy decoding is the primary controlled evaluation for training and
ablation comparisons.

Self-consistency execution voting is an optional deployment overlay:

1. sample `N=8` candidates at `temperature=0.8`, `top_p=0.95`;
2. execute them on the client's local database;
3. group candidates by equivalent execution result;
4. select the majority group, breaking ties by mean log-probability.

SC previously beat verifier-gated retry on one centralized adapter, but it
must be requested explicitly with `--overlay sc`. It is evaluated only after
the matched greedy comparison because it changes decoding cost and can
interact with ICL.

## 9. Experiment ladder

### 9.1 Main federated arms

| Arm | Aggregation | Server step | Purpose |
|---|---|---|---|
| `central` | none | centralized private-data FT | non-private upper reference |
| `fedavg` | factor-wise FedAvg | none | FL baseline |
| `fedavg_pub` | factor-wise FedAvg | public CE | public-exposure control |
| `fedkd` | factor-wise FedAvg | public CE + RKL | KD after baseline aggregation |
| `florana` | weighted FLoRA-NA | none | aggregation contribution |
| `florana_pub` | weighted FLoRA-NA | public CE | matched public-exposure control |
| `florana_kd` | weighted FLoRA-NA | public CE + RKL | proposed KD backbone |
| `teacher` | none | frozen 7B inference | reference |

The main causal contrasts are:

```text
aggregation value = florana - fedavg
teacher/RKL value = florana_kd - florana_pub
public CE effect  = florana_pub - florana
ICL value         = florana_kd[train/eval k3] - florana_kd[train/eval k0]
```

Do not assume any ordering before the runs finish.

### 9.2 Execution order

1. Close the `dail_weighted` train/federated wiring and run deterministic
   prompt preflight.
2. Run a capped `K=2, T=1` six-arm smoke.
3. Run the shared-client `K=8, T=1` aggregation/server ladder.
4. Run the matched `florana_kd` no-ICL versus ICL-training comparison.
5. Inspect `e_agg`, post-aggregation/post-server EX, execution errors, and
   per-client variance.
6. Extend only viable arms to `T=2`, then `T=3`.
7. Run the selected headline conditions for three seeds; extend toward
   `T=15` only if round trends justify it.
8. Evaluate SC composition on the winning trained condition.

## 10. Evidence currently retained

| Finding | Scope |
|---|---|
| Centralized RKD beats FT by 6.09 EX | strong paired result, one training seed |
| RKD beats KID by 1.45 EX | provisional; `p=0.072` |
| Zero-shot teacher target generation beats teacher ICL on BIRD | closed for tested target-generation setup |
| `dail_weighted k=3` is the best tested deployable ICL retriever | selection fact, not a positive ICL result |
| All inference-only ICL cells hurt the `k=0`-trained Model A | closed for that centralized unmatched setup |
| SC beat verifier-gated retry | provisional deployment result, one sampling seed |
| Full federated method improves accuracy | **not tested yet** |
| Matched federated in-context training helps or hurts | **not tested yet** |

## 11. Invariants

1. Private data, schema, demos, and embeddings never leave the client.
2. The teacher never touches client data.
3. Test examples are never used as training or retrieval demos.
4. Client/demo pools and evaluation databases remain disjoint as configured.
5. All compared KD arms use the same ordered public pool and recorded hash.
6. Reverse KL means `RKL(q_student || p_teacher)`; relational KD is not used.
7. Comparisons change one named factor at a time and share seeds/splits where
   pairing is claimed.
8. Every reported result records model, adapter, data, prompt, retrieval,
   decoding, and seed identity.
9. Negative results remain reportable; their scope must not be generalized
   beyond the experiment that produced them.
10. No formal DP claim is made without an explicit DP mechanism and privacy
    accounting.

## 12. Current status

Implemented:

- non-IID Spider partitioning;
- client LoRA training with optional train-time demos;
- factor-wise weighted FedAvg and weighted FLoRA-NA;
- public CE and cached-logit RKD server stages;
- six-arm federated orchestration with checkpoint/resume, setup identity,
  manifests, and round lineage;
- greedy and SC evaluation;
- reproducible retrieval/evaluation artifacts.

Pending before paper claims:

- complete `dail_weighted` train/federated wiring;
- real `K=8` federated results;
- matched federated ICL-training comparison;
- multi-round and multi-seed confirmation;
- final method name/title decision after the ICL result.
