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
- ICL status (revised 2026-08-10): **measured and negative** in the matched
  federated experiment. In-context client training costs `2.90 EX` before the
  server step (`p=0.008`); demos at inference cost `3.87 EX` (`p=0.003`);
  training costs `2.35x`. Proposed demotion to a §5 negative result, with the
  method name `Fed-ICKD` no longer matching the evidence. Advisor sign-off
  required before the paper's framing changes.
- Selected ICL candidate: `dail_weighted`, fixed `k=3`, `never_schema`,
  client-private demo pool, matched at train and eval.
- Important scope correction: the negative 2026-07-29 result tested
  inference-only ICL on a centralized adapter trained with `k=0`. It does not
  settle matched in-context training or federated ICL.
- Both `K=5, T=1, seed 0` ladders are trained and evaluated at `k=0`. The ICL
  side additionally has all `k=3` cells; the no-ICL side has none of them.
- Established at one seed with paired tests: server-side reverse KL beats its
  matched SeqKD control by `+2.03 EX (p=0.042)` on the no-ICL ladder and
  `+2.51 EX (p=0.013)` on the ICL ladder. This is the paper's contribution.
- On 2026-08-10 the aggregation choice was settled: factor-wise FedAvg is the
  default. FLoRA-NA lost or tied all four `k=0` head-to-head cells and is
  removed from the contribution list.
- The binding gap is now replication, not coverage: every headline delta rests
  on seed 0 alone.
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

### Federated ICL ladder, K=5 T=1 seed 0

First real federated results. Clients trained with `dail_weighted k=3` fixed,
`never_schema`, full schema; public pool `P` = BIRD `bootstrap_full_exmatch`
(3,873 rows used); server `k_teacher=0`; Spider dev `n=1034`, greedy.
Run IDs: `federated__{florana_kd,fedavg,fedavg_pub,fedkd}__s0__*__r1` plus
`eval_arms__s0__202608{05,06,07,08}T*`.

| Adapter | Aggregation | Server step | EX k=0 | EX k=3 central | EX k=3 per-client |
|---|---|---|---:|---:|---:|
| `fedavg_adapter` | factor FedAvg | none | 54.45 | 54.26 | 55.57 ± 0.97 |
| `florana_adapter` | FLoRA-NA | none | 54.45 | 54.35 | 55.65 ± 1.04 |
| `fedavg_pub` M_G | factor FedAvg | CE on teacher SQL | 61.51 | 57.74 | 58.82 ± 0.80 |
| `fedkd` M_G | factor FedAvg | CE + RKL on teacher SQL | 64.02 | 59.38 | 60.74 ± 0.65 |
| `florana_kd` M_G | FLoRA-NA | CE + RKL on teacher SQL | 63.93 | 60.06 | 61.24 ± 0.37 |

Supported readings:

- Server-side RKD carries measurable value over its matched public-CE control:
  `61.51 -> 64.02`, **+2.51 EX** on the factor-FedAvg branch. This is the
  cleanest evidence for the paper's central mechanism so far.
- **The whole server-step gain is teacher-derived; none of it is "more data".**
  Pool `P` rows carry the TEACHER's own exec-verified SQL as their target text,
  not BIRD gold (`build_exec_bootstrap_probe.py` then
  `score_bootstrap_ex_match.py`; 80.7% of the 3,873 target strings differ from
  BIRD gold). So `fedavg_pub` is sequence-level KD on hard labels, not a plain
  data top-up, and the ladder reads: no distillation `54.45` -> hard-label KD
  `61.51` (+7.06) -> hard+soft-label KD `64.02` (+2.51). `+2.51` is therefore
  the value of logit-level reverse KL OVER SeqKD, which is a sharper claim than
  "teacher helps". The plain-data arm is E0.1 and it was negative: CE on BIRD's
  own gold scored `47.10` against a `50.00` base floor.
  Execution errors drop from ~25% pre-server to 11–16% post-server.
- Client-private demo pools do not cost accuracy versus a pooled demo source
  (`61.24` vs `60.06`), with per-pool spread ≤ 1.0. The privacy framing holds.
- **FLoRA-NA and factor FedAvg are indistinguishable at this scale.** Pre-server
  EX is identical to four decimals; post-RKD they differ by 0.09–0.68 EX in
  mixed directions, well inside the ~1.5 EX binomial standard error at
  `n=1034`. FLoRA reduced relative product error `0.0893 -> 0.0827` (7% better
  reconstruction) with zero downstream effect — a real finding in itself:
  better factor reconstruction does not transfer to SQL quality. Default to
  factor FedAvg; FLoRA-NA earns a place only if a higher-`K` or `alpha=0.1`
  ablation separates them.

The `k=3` penalty visible in the last two columns is explained by the matched
no-ICL ladder below, not by the server step's `k_teacher=0` setting.

### Federated no-ICL ladder, K=5 T=1 seed 0, and the matched verdict

Identical protocol to the ICL ladder — same split, seed, pool, server step,
budget — with `--client-train-k 0`. Run IDs `federated__*__s0__*__r1` dated
2026-08-08/09, evals `eval_arms__s0__20260809T*`. The `k=0` column is complete
plus one `k=3` cell for `train_noicl`; the other nine `k=3` cells describe a
retired eval mode and were deliberately not run.

| Stage, both at eval `k=0` | ICL-train | no-ICL-train | Delta | paired `p` |
|---|---:|---:|---:|---:|
| `fedavg_adapter` | 54.45 | **57.35** | **+2.90** | **0.008** |
| `florana_adapter` | 54.45 | **56.87** | **+2.42** | **0.026** |
| + SeqKD on teacher SQL | 61.51 | 61.32 | −0.19 | — |
| + CE/RKL, factor FedAvg | **64.02** | 63.35 | −0.68 | 0.401 |
| + CE/RKL, FLoRA-NA | 63.93 | 62.57 | −1.35 | 0.060 |

All `p` are exact two-sided McNemar on paired 1,034-row prediction files.

**1. The reverse-KL claim replicates.** `+2.03 EX, p=0.042` on the no-ICL
ladder against `+2.51 EX, p=0.013` on the ICL ladder — same direction, same
magnitude, two independent client populations, both significant. The matched
SeqKD step is itself `+3.97, p=0.010`. The paper's central mechanism is the
one result here that is established rather than suggestive.

**2. In-context client training produces worse aggregated models.** The
pre-server gap is `+2.90 EX (p=0.008)` in favour of no-ICL, with fewer
execution errors (236 vs 258) and higher EM (50.6 vs 46.7). The server step
then lifts the ICL branch further (`+9.57`) than the no-ICL branch (`+6.00`)
purely because it starts lower, and the endpoints converge to a
non-significant `0.68`. Reading the endpoints alone had suggested ICL training
was a mild augmentation win; the pre-server cells show the opposite and are
the significant ones.

**3. Demonstrations at inference cost 3.87 EX, `p=0.003`,** within the ICL
model itself (`k=3` 60.06 versus `k=0` 63.93). This is the largest and
best-supported ICL effect measured, and it is negative. It also removes the
`k_teacher=0` explanation offered above: the no-ICL model never saw a demo in
training yet reaches 62.57–63.35, so nothing about the server step is
destroying a capability the clients had.

**3b. The train/eval-parity hypothesis is refuted, not merely unsupported.**
Completing the 2x2 on 2026-08-10 (`eval_arms__s0__20260809T184408`):

| | eval `k=0` | eval `k=3` | drop under demos |
|---|---:|---:|---:|
| train `k=3` | 63.93 | 60.06 | −3.87, `p=0.003` |
| train `k=0` | 62.57 | **59.48** | −3.09, `p=0.014` |
| delta | +1.35, `p=0.060` | +0.58, `p=0.572` | |

The DAIL-SQL §4.4.4 argument reproduced in `build_examples`' docstring predicts
that a `k=0`-trained adapter collapses under demos while a demo-trained one
does not. The `k=0`-trained model drops **less** (−3.09 versus −3.87). The
interaction runs the wrong way by 0.78 EX. Three independent adapters — the
2026-07-29 centralized Model A (−2.71), `train_noicl` (−3.09), `train_icl3`
(−3.87) — all lose about 3 EX when given demos regardless of how they were
trained, so the demo penalty is a property of the 1.5B student, not of the
training recipe. Matched at the ICL deployment mode the two pipelines are
indistinguishable (`+0.58, p=0.572`): in-context client training buys nothing
in the very mode that justifies paying for it.

**4. Cost, measured not estimated.** Client training 9,651 s versus 4,100 s
(**2.35x**), plus a draft-skeleton pre-pass and a per-client DAIL cache that
the no-ICL path does not build; client VRAM 28.2 GB versus 25.9 GB; inference
prompt +38.7% characters and 4.2x latency in-run (0.289 -> 1.224 s/query);
and every deployed client must hold and index a private demo pool.

**5. FLoRA-NA is closed.** Six head-to-head cells: tie, −0.09, −0.48
(`p=0.405`), −0.77 (`p=0.215`), +0.68, +0.50. The only two wins are `k=3`
cells, the eval mode this section retires. Its relative product error is lower
in both pipelines (0.0827 vs 0.0871; 0.0661 vs 0.0717) and transfers to EX in
none of them. Retain factor-wise FedAvg. Keep the negative observation —
better factor reconstruction does not improve SQL — as a §5 remark, not a
contribution.

Consequence for the paper: the defensible contribution is federated LoRA plus
server-side reverse-KL distillation on a public pool. ICL moves to §5 as a
measured negative result carrying four tests — pre-server `−2.90 (p=0.008)`,
demos at inference `−3.87 (p=0.003)`, the refuted parity interaction, and a
`2.35x` training cost. On 2026-08-10 the author decided to propose dropping
ICL from the method and renaming away from `Fed-ICKD`; advisor sign-off is
pending and the original ICL direction predates it, so nothing is rewritten in
`system_architecture.md` until that conversation happens.

### Aggregate versus the best single client, K=5 seed 0

Asked on 2026-08-10, since "federation beats going it alone" was being claimed
from the client *mean*. At `k=0` on the ICL branch the five client adapters
score 53.29 / 52.51 / 53.00 / 50.97 / 56.29 (mean 53.21) and the aggregate
scores 54.45. **The aggregate beats four clients and loses to the best one by
1.84 EX.** It beats only the weakest client significantly (+3.48, `p=0.009`).

Three diagnostics, all run on existing prediction files, no GPU:

- **Client 5's advantage is real, not a selection artefact.** Across 100 random
  half-splits it is the best client in 193/200 halves, and the two halves agree
  93/100 times. An earlier note in this log claimed the gap was mostly the
  order statistic of five noisy draws; that claim is withdrawn.
- **The gap itself is not established.** Bootstrap (2,000 resamples) gives
  `best client − FedAvg = +1.84 EX, 95% CI [−0.77, +4.16]`.
- **The advantage is domain-shaped, not uniform.** Over Spider dev's 20
  databases client 5 beats the aggregate on 8, loses on 8, ties on 4, with the
  surplus concentrated in `network_1`, `world_1`, `pets_1`, `dog_kennels`.
  Client 5 is also the *smallest* client (910 rows, FedAvg weight 0.105).

Reading: this is domain specialisation under non-IID, the standard trade a
global model makes, not evidence that aggregation is broken. Supporting that,
the aggregate sits *above* the client mean — a broken aggregation would land
below it. And the gap is confined to the pre-server stage: after distillation
the global model reaches 64.02, **7.73 EX above the best client**.

One technical hypothesis is not yet excluded, and an earlier entry in this log
overstated its closure. `factor_fedavg` does carry the FedIT error
`mean(B)·mean(A) ≠ sum_i w_i B_i A_i`, and `florana` does **not** fix it: it
only fits scalar client coefficients while staying at rank `r`, so it cannot
represent a sum of rank up to `K·r`. That is why its product error moves only
0.0687 → 0.0661 (7.8%). **Exact aggregation has therefore never been tested**
— the FLoRA-NA verdict below stands as a verdict on FLoRA-NA, not on exact
aggregation.

`scripts/exact_aggregate.py` (+ `tests/test_exact_aggregate.py`, 5 tests) was
written for this. It needs no retraining: `stack` concatenates the factors into
an exact rank-`K·r` aggregate with `lora_alpha` rescaled so PEFT's `alpha/r`
is unchanged, and `svd` gives the best rank-`r` fit to the same target — the
control that separates "the aggregation error was fixed" from "the server just
got a 5x bigger adapter". Queued as one aggregation plus one eval, about 25
minutes. Predictions: `stack` ≈ 54.45 closes the question; `stack` high with
`svd` ≈ 54.45 means capacity, not exactness; both high would make aggregation
error a real finding, though a rank-80 aggregate cannot be handed back to
rank-16 clients for a round 2, which is precisely why FedEx-LoRA uses a
residual correction instead of stacking.

EM is not comparable across the server step. It falls `46.9 -> 31.3` while EX
rises, and prediction diffs show the cause is BIRD surface convention
(`count(*)` becomes `COUNT(Singer_ID)`, separator spacing changes). Report EX
and execution errors for pre/post-server comparisons; EM only within a stage.

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

Both `K=5, T=1, seed 0` runbooks are executed as of 2026-08-10. The
ICL-versus-no-ICL question is answered and FLoRA-NA is closed; neither needs
more cells. Remaining order, highest value first:

1. **Seeds 1 and 2 on the no-ICL factor-FedAvg ladder**
   (`fedavg -> fedavg_pub -> fedkd`). Every headline number is single-seed,
   including the `+2.03` reverse-KL delta the paper rests on. About 4 h per
   seed: clients 4,100 s plus two server stages ~8,100 s. Nothing else changes
   what can be claimed.
2. **Exact-aggregation diagnostic** (`scripts/exact_aggregate.py`, `stack` and
   `svd` modes, then one `k=0` eval of both). No retraining; about 25 minutes.
   Settles whether the pre-server gap to the best client is aggregation error
   or client drift, and it is the one open question the FLoRA-NA verdict does
   not cover.
3. **Evaluate the five no-ICL client adapters at `k=0`** (about 1 h). The
   report's "local versus federated" row currently borrows ICL-branch numbers,
   and the `+7.35` step cannot be split into local training and aggregation
   without it.
4. Extend the winning condition to `T=2`, `T=3`.
5. Test SC composition only on the selected trained condition.
6. Advisor conversation on demoting ICL and renaming away from Fed-ICKD.

Closed on 2026-08-10: the 2x2 completion cell (`train_noicl` at `k=3`) ran and
refuted the parity hypothesis, so §5 is fully evidenced. Its private-pool twin
was dropped — the centralized cell already answered the question, and the
remaining nine `k=3` no-ICL cells only describe a retired eval mode.

## Closed or deferred branches

- Relational hidden-state KD: removed; “RKD” means reverse-KL KD.
- Struct-SQL/SeqKD direction: removed from the active pipeline.
- Asymmetric-context KD: shelved after a negative one-seed probe.
- Skew-RKL `alpha=0.1`: rejected as default.
- BIRD as a trained-model evaluation benchmark: not used because it is the
  public training pool.
- Formal DP: not claimed; optional only if explicitly implemented.
- Additional ICL retriever sweeps: dropped 2026-08-10. The matched federated
  ladder showed in-context client training is `2.90 EX` worse before the server
  step (`p=0.008`), so there is no branch left for a retriever sweep to tune.
- Larger pool `P` = `bootstrap_full` (7,968 rows, teacher SQL, exec-only filter)
  instead of `bootstrap_full_exmatch` (3,873, additionally filtered to match
  BIRD gold's execution result): an option, never measured downstream. The
  exmatch filter was adopted because it looks stricter, but its own docstring
  flags the trade — BIRD gold is an unreliable oracle, so the filter trades
  teacher-hallucination risk for gold-error-mimicry risk. Costs a fresh teacher
  logit cache (the current one is keyed to the 3,873-row pool hash).
- `k_teacher=3` server distillation: dropped 2026-08-10. It was proposed to
  test whether the zero-shot server step erases client ICL ability. The no-ICL
  ladder answered that without it: a model that never saw a demo in training
  reaches `62.57–63.35`, so no capability is being erased. `k_teacher=0` also
  keeps RKD logits offline cacheable.
