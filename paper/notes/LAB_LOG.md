# FedICL-SQL — Condensed Lab Log

> Rewritten 2026-07-31. This file keeps only decisions, results, and
> implementation milestones needed to reproduce the current research path.
> Superseded discussion remains available in Git history. Per-run truth lives
> in `experiments/*/results/*/{config,metrics,predictions}.*`.

## Current snapshot

- Proposed system: private client FT + weighted FLoRA-NA + server public
  CE/reverse-KL.
- Student/teacher: Qwen2.5-1.5B-Instruct /
  Qwen2.5-Coder-7B-Instruct.
- Public KD data: fixed 8,127-row BIRD teacher-generated EX-match pool.
- ICL status: **retained as an open full-pipeline experiment**.
- Selected ICL candidate: `dail_weighted`, fixed `k=3`, `never_schema`,
  client-private demo pool, matched at train and eval.
- Important scope correction: the negative 2026-07-29 result tested
  inference-only ICL on a centralized adapter trained with `k=0`. It does not
  settle matched in-context training or federated ICL.
- Federated implementation exists; real headline `K=5` results do not.
- Matched ICL/no-ICL federated wiring was reviewed and completed on 2026-08-01;
  the remaining gate is a capped GPU smoke followed by the real runs.
- On 2026-08-01 the headline client count was reduced from `K=8` to `K=5`
  at the same Dirichlet `alpha=0.5` and seed 0. The committed split has
  910–2,749 rows and 17–49 databases per client; old K=8 artifacts are not
  mixed with the new K=5 runs.

## Active decisions

### Privacy and data

1. Raw client data, schema, demos, and embeddings never leave the client.
2. The server teacher never sees client data.
3. Only LoRA adapters cross the network.
4. Spider dev is a frozen test set and never a demo pool.
5. Every default KD arm uses the same ordered 8,127-row public pool and hash.
6. BIRD gold SQL text is not a training target. It is used only to select
   teacher-generated SQL with matching execution results.

### Training and aggregation

1. Client training is gold CE only.
2. Factor-wise sample-weighted FedAvg is the primary FL baseline.
3. Sample-weighted FLoRA-NA is the proposed aggregator.
4. Both aggregators report model-space aggregation error `e_agg`.
5. Server KD is `CE + RKL(q_student || p_teacher)`, with plain reverse KL.
6. Skew-RKL `alpha=0.1` is rejected as a default because it significantly
   increased execution errors despite a non-significant EX increase.
7. RKD remains the provisional KD direction; KID remains an ablation.

### ICL

1. Do not drop ICL before matched train/eval ICL is tested in the federated
   pipeline.
2. Use `dail_weighted k=3` as the retained candidate because it was the best
   deployable ICL cell already measured.
3. The primary ICL comparison is:

   ```text
   control: train k=0 -> greedy eval k=0
   ICL:     train fixed k=3 -> greedy eval dail_weighted k=3
   ```

4. Both conditions must share split, initialization, aggregation, public pool,
   server step, seed, and training budget.
5. Test greedy first. Evaluate SC composition only after the base ICL effect
   is known.
6. Teacher-side ICL target generation remains retired: zero-shot teacher
   generation was better on the tested BIRD setup.
7. Final paper/method naming waits for the matched federated ICL verdict.

## Retained empirical results

### Centralized baselines

| Condition | EX | EM | Notes |
|---|---:|---:|---|
| Base Qwen2.5-1.5B | 50.00 | 21.08 | retained current-family base run |
| Centralized FT | 61.70 | 42.50 | early clean baseline |
| `ft_no_icl` | 62.19 | 57.16 | later centralized reference |
| `central_rkd` | 68.28 | 61.99 | one-stage Spider RKD |

Different rows above come from different experiment snapshots; use paired
prediction files, not this table alone, for causal comparisons.

### RKD versus FT and KID

On identical Spider data from the base model:

- `central_rkd - central_ft = +6.09 EX`;
- paired McNemar `p=3.1e-7`;
- `central_kid - central_rkd = -1.45 EX`;
- RKD-versus-KID paired `p=0.072`.

Conclusion: a teacher-logit KD signal is established in the centralized PoC.
RKD versus KID is not statistically settled; RKD is retained because its fixed
targets allow offline logit caching.

### Public BIRD continuation

Plain CE on BIRD gold from the base model failed:

| Probe | EX | Verdict |
|---|---:|---|
| untrained floor | 50.00 | reference |
| 1k BIRD-gold CE | 47.10 | harmful |
| teacher bootstrap CE, 831 executable rows | 50.00 | removed the regression |

The canonical pool was later frozen at 8,127 teacher-generated SQL rows whose
execution results match BIRD gold.

A centralized `Spider FT -> BIRD CE+RKL -> Spider FT` pipeline was compared
with a matched `Spider FT -> Spider FT` control:

| Decode | Control EX | +BIRD stage EX | Delta | Evidence |
|---|---:|---:|---:|---|
| greedy | 67.02 | 67.31 | +0.29 | `p=0.830` |
| SC N=8 | 73.40 | 75.24 | +1.84 | `p=0.0699` |

Supported reading: no greedy EX gain after matched training budget; an SC
interaction is suggestive but unconfirmed. A matched teacher-target CE-only
arm is still required to attribute any effect specifically to RKL.

### Teacher-side ICL for public target generation

On a 1,000-row BIRD probe:

| Teacher prompting | Exec pass | EX-match / 1,000 |
|---|---:|---:|
| zero-shot | 83.1% | 39.3% |
| self-ICL k=3 | 77.2% | 35.9% |
| Spider-seed ICL k=3 | 72.0% | 32.6% |

Decision: public `y_pub` generation stays zero-shot. This finding is scoped to
teacher target generation and does not decide client in-context training.

### Inference-only ICL matrix

Controlled setup:

- Model A:
  `central_ft_then_kd_bird_exmatch_then_spider_ft`;
- full Spider dev, 1,034 rows;
- centralized Spider-train demo pool;
- adapter trained with `k=0`;
- greedy evaluation, seed 0.

Baseline: `k=0` = **67.31 EX / 63.93 EM**.

| k | random | question | masked | CodeS | DAIL hard | DAIL weighted | oracle |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 63.93 | 64.12 | **64.22** | 63.83 | 64.02 | 64.12 | 62.96 |
| 3 | 63.83 | 63.06 | 64.31 | 64.31 | 64.41 | **64.60** | 64.22 |

All cells were below `k=0`; every paired bootstrap interval was wholly
negative. Best deployable cell:

```text
dail_weighted k=3
EX delta = -2.71 pp
95% CI = [-5.03, -0.48]
McNemar p = 0.0251
prompt tokens = +33.1%
latency = 2.67x
```

Decision revised 2026-07-31: this closes **unmatched centralized
inference-only ICL**, not ICL for the whole project. `dail_weighted k=3`
becomes the candidate for the missing matched train/federated experiment.

### Inference overlay

On `central_rkd`, self-consistency execution voting (`N=8`,
temperature `0.8`, top-p `0.95`) beat the previous verifier-gated retry:

```text
SC EX = 72.73
gate EX = 69.92
delta = +2.81
McNemar p = 0.00042
```

This result used one sampling seed. SC remains an optional deployment overlay,
not part of the primary greedy ICL comparison.

### Skew-RKL

Matched plain-RKL versus Skew-RKL `alpha=0.1`:

| Metric | Plain RKL | Skew-RKL | Delta |
|---|---:|---:|---:|
| EX | 64.99 | 66.05 | +1.06, `p=0.222` |
| execution errors | 104 | 124 | +20, `p=0.009` |

Decision: keep plain RKL. Do not spend a federated arm on `alpha=0.1`.

## Implementation milestones retained

### Data and evaluation hygiene

- Removed test-set leave-one-out ICL leakage; demo pools now come from train
  data only.
- Implemented domain-group non-IID Spider partitions with a minimum client
  example guard.
- Evaluation artifacts record model, adapter, data/pool hashes, retrieval,
  prompt settings, decoding settings, seed, and selected demo traces.
- SC RNG seeding and resume fingerprints were fixed before headline runs.

### Federated pipeline

Implemented:

- client LoRA training;
- factor-wise weighted FedAvg;
- sample-weighted FLoRA-NA;
- public CE and public CE+RKL server stages;
- full teacher-logit cache;
- six arms: `fedavg`, `fedavg_pub`, `fedkd`, `florana`,
  `florana_pub`, `florana_kd`;
- per-layer and overall `e_agg`;
- immutable `setup.json`, content fingerprints, round lineage,
  checkpoint/resume, and deterministic result IDs;
- optional post-aggregation and post-server evaluation per round.

Real `K=5` headline training has not run.

### Evaluation-result retention

The result store was audited on 2026-07-31:

- retained 30 `eval_arms` runs covering current references, public-pool
  quality gates, matched continuation/loss controls, and the complete Model-A
  ICL matrix;
- retained two full 1,034-row inference-overlay runs;
- removed 79 superseded `eval_arms` runs and one 200-row overlay probe;
- removed categories include old model/retriever/gate sweeps, retired methods,
  obsolete local 0.5B pilots, replaced controls, out-of-scope robustness runs,
  and pre-reproducibility SC duplicates;
- `client_train/results` was intentionally untouched because it is training
  provenance.

Exact retained run IDs and rationale are recorded in:

- `experiments/eval_arms/results/README.md`;
- `experiments/inference_overlay/results/README.md`.

### ICL infrastructure

Evaluation supports:

- `random`;
- `question`;
- `masked_question`;
- `codes`;
- `dail_select`;
- `dail_weighted`;
- eval-only `oracle_structure`.

Client training supports demo injection through `train_k`, fixed or sampled
demo count, private client pools, and train/eval prompt styles.

Federated ICL preflight closed on 2026-08-01:

- the CLI and immutable setup expose/fingerprint the full client ICL policy;
- `dail_weighted` train retrieval generates cached draft skeletons with the
  round-start global student;
- fixed `k=3`, `never_schema`, `full` schema, DAIL alpha/shortlist, embedder,
  and cache paths propagate into every client configuration;
- missing drafts fail loudly instead of falling back to masked-question
  retrieval;
- per-round evaluation fingerprints now cover the complete ICL protocol;
- focused federated/training/manifest tests pass (60 tests), the full suite
  passes (267 tests), and lint is clean.

The code review also confirmed immutable setup recipes, parent-adapter hashes,
round lineage, idempotent round/result persistence, and deterministic result
paths. Round results now collect every completed client's loss/step/time/VRAM
summary and exact train config, plus aggregation diagnostics and the server-KD
summary, including stages reused after resume. No real GPU result is claimed.
The local workspace does not contain the
canonical full teacher-logit cache, so the compute environment must provide or
rebuild a cache whose metadata matches the frozen public pool before KD runs.

## Active run queue

1. Validate the canonical teacher-logit cache on the compute host.
2. Run a capped `K=2, T=1` wiring smoke using clients 1–2 of the committed
   `K=5` split; do not report it as a scientific two-client result.
3. Run matched `florana_kd`, first at `K=5, T=1`:

   ```text
   train/eval k=0
   versus
   train/eval dail_weighted k=3
   ```

4. Inspect EX/EM, execution errors, prompt cost, latency, per-client variance,
   `e_agg`, and post-aggregation/post-server changes.
5. Run the `K=5, T=1` aggregation/server ladder needed to attribute gains
   across FedAvg, FLoRA-NA, public CE, and public RKD.
6. Extend viable conditions to `T=2`, `T=3`, then three seeds.
7. Test SC composition only on the selected trained condition.
8. Decide whether ICL and the name Fed-ICKD remain in the final paper.

## Closed or deferred branches

- Relational hidden-state KD: removed; “RKD” means reverse-KL KD.
- Struct-SQL/SeqKD direction: removed from the active pipeline.
- Asymmetric-context KD: shelved after a negative one-seed probe.
- Skew-RKL `alpha=0.1`: rejected as default.
- BIRD as a trained-model evaluation benchmark: not used because it is the
  public training pool.
- Formal DP: not claimed; optional only if explicitly implemented.
- Additional ICL retriever sweeps: deferred until matched federated
  in-context training establishes whether the branch is viable.
