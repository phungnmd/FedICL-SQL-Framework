# FedLS-SQL — Condensed Lab Log

> Rewritten 2026-07-31; active state refreshed 2026-08-20 for FedLS-SQL. This
> file keeps only decisions, results, and
> implementation milestones needed to reproduce the current research path.
> Superseded discussion remains available in Git history. Per-run truth lives
> in `experiments/*/results/*/{config,metrics,predictions}.*`.

## Current snapshot

- Advisor decision, 2026-08-19: the paper is renamed **FedLS-SQL: A Novel
  Federated Large-Small Language Models Framework for Natural Language to
  SQL**. The main method is private client LoRA fine-tuning, sample-weighted
  factor-wise FedAvg, and server-side LLM-to-SLM CE/reverse-KL distillation.
- Student/teacher: Qwen2.5-1.5B-Instruct /
  Qwen2.5-Coder-7B-Instruct.
- Public KD data: fixed **3,873-row** BIRD teacher-generated EX-match pool.
- ICL status (final decision 2026-08-19): **measured and negative** in the matched
  federated experiment. In-context client training costs `2.90 EX` before the
  server step (`p=0.008`); demos at inference cost `3.87 EX` (`p=0.003`);
  training costs `2.35x`. ICL is removed from the main method and retained as
  a negative ablation/reproducibility record.
- Established at one seed with paired tests: server-side reverse KL beats its
  matched SeqKD control by `+2.03 EX (p=0.042)` on the no-ICL ladder and
  `+2.51 EX (p=0.013)` on the ICL ladder. This supports the server-KD component;
  the paper's contribution is the complete LLM-SLM federated framework.
- On 2026-08-10 the aggregation choice was settled: factor-wise FedAvg is the
  default. FLoRA-NA lost or tied all four `k=0` head-to-head cells and is
  removed from the contribution list.
- Replication closed on the two rows that carry the proposal (2026-08-15). The
  full pipeline is `62.74 ± 0.53` and the distillation-only control is
  `61.35 ± 0.88`, both at three seeds. The federated component is therefore
  worth `+1.39 ± 1.12`, `p = 0.165` — positive in all three seeds, individually
  significant in two, not established across them. This is now the weakest
  load-bearing row in the paper.
- Pipeline order is settled: distillation last. Running it first scores
  `61.61` against `63.35` at seed 0.
- **Headline as of 2026-08-16: `T=3` reaches 69.54 EX**, up from 63.35 at
  `T=1` (`+6.19`, `p<1e−4`), with both the pre-server and post-server curves
  rising at every round. Multi-round federation is now the project's strongest
  result. The budget-matched centralized and out-of-distribution evaluations
  are complete; the independent pure-FL multi-round control is still pending.
- Scope correction 2026-08-19: the `T=2`/`T=3` pre-server adapters are not
  pure FL controls. Each starts from the previous round's post-KD `m_g`, so the
  64.02/66.05 curve already contains one/two earlier KD stages. A separate
  `--arm fedavg --rounds 3` branch is now required before reporting the requested
  `Centralized <> FL <> FL-KD` final-model comparison.
- The matched control settles what drives it: at two passes of local training,
  `T=2, E=1` beats `T=1, E=2` by `+2.61` (`p=0.0067`). The gain comes from
  repeated communication rounds, not from training clients longer.
- The centralized reference saturates after two epochs (62.19 → 67.02 → 67.60,
  third epoch `p=0.606`) while the federated curve is still rising. Matched on
  private-data passes, `T=3` is `+1.93` over `central_3ep` (`p=0.172`). The
  claim is the shape of the two curves, not the gap.
- The round result holds on every benchmark separately: `T1→T3` is `+6.19`
  Spider dev, `+6.69` Realistic, `+5.90` Syn, `+4.86` DK, all significant.
- **The two components are orthogonal** (2026-08-18). On the Spider variants the
  rounds carry everything and the server step is null in all nine cells; on BIRD
  dev the server step is `+8.28`/`+3.91` (`p<1e-6`) and federation alone is
  `+0.26` (`p=0.82`). Neither half is redundant, and Spider dev alone cannot
  separate them because both work there.
- Out-of-distribution evaluation (2026-08-15) reversed which row is safe. Over
  2,077 questions on three perturbed Spider sets, the federated stage holds
  (`+1.64`, `p=0.0098`) while distillation's increment over it collapses
  (`+0.34`, `p=0.76`). The components turn out to be complementary along
  different shift axes, which is a better argument for the combination than the
  Spider-dev ablation gave.
- One local epoch is not the converged operating point: a second identical
  Spider epoch is worth `+4.83 EX` centrally (62.19 → 67.02). The
  compute-matched comparison is unaffected; the "reference ceiling" label on
  62.19 is wrong and the ablation's external validity is open.
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
5. Every default headline KD arm uses the same ordered 3,873-row public pool
   and hash.
6. BIRD gold SQL text is not a training target. It is used only to select
   teacher-generated SQL with matching execution results.

### Training and aggregation

1. Client training is gold CE only.
2. Factor-wise sample-weighted FedAvg is the primary FL baseline.
3. Factor-wise sample-weighted FedAvg is also the FedLS-SQL aggregator.
4. FLoRA-NA is a closed exploratory branch, not a proposed contribution.
5. Server KD is `CE + RKL(q_student || p_teacher)`, with plain reverse KL.
6. Skew-RKL `alpha=0.1` is rejected as a default because it significantly
   increased execution errors despite a non-significant EX increase.
7. RKD remains the provisional KD direction; KID remains an ablation.

### ICL — closed decision

1. Canonical FedLS-SQL uses `train_k=0`, `k_teacher=0`, and `eval_k=0`.
2. The matched `dail_weighted k=3` experiment is retained as a negative
   ablation; no additional ICL sweep is planned.
3. ICL code and old artifacts remain available solely for reproducibility.
4. Teacher-side ICL target generation remains retired: zero-shot teacher
   generation was better on the tested BIRD setup.

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

An 8,127-row candidate pool was constructed during development. The canonical
headline subset was later frozen at **3,873 teacher-generated SQL rows** whose
execution results match BIRD gold; the larger candidate is not the method pool.

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
recorded on 2026-08-19. The current architecture now uses the FedLS-SQL
framing; this paragraph is retained as the chronology of the earlier decision.

### Three seeds, 2026-08-11 — the endpoint holds, the decomposition does not

Seeds 1 and 2 of the no-ICL factor-FedAvg ladder completed
(`federated__*__s{1,2}__*__r1`, evals `eval_arms__s0__20260811T*`). They change
what can be claimed, so read this before the single-seed section below.

| Stage | seed 0 | seed 1 | seed 2 | mean | sd |
|---|---:|---:|---:|---:|---:|
| FedAvg, pre-server | 57.35 | 57.45 | 59.77 | 58.19 | 1.37 |
| + SeqKD | 61.32 | 62.28 | 59.48 | 61.03 | 1.42 |
| **+ reverse KL (full pipeline)** | 63.35 | 62.48 | 62.38 | **62.74** | **0.53** |

**The full pipeline is stable: `62.74 ± 0.53`, `+12.74` over the 50.00 base.**
That result is safe.

**The per-component decomposition is not.** Seed-level deltas, two-sided `t` on
three paired differences:

| Component | per-seed | mean | sd | `p` |
|---|---|---:|---:|---:|
| SeqKD over FedAvg | 3.97 / 4.83 / **−0.29** | +2.84 | 2.74 | 0.215 |
| reverse KL over SeqKD | 2.03 / **0.20** / 2.90 | +1.71 | 1.38 | 0.165 |
| whole server distillation | 6.00 / 5.03 / 2.61 | +4.55 | 1.75 | **0.046** |

The `+2.03 (p=0.042)` recorded below was a single-seed paired McNemar, which
answers "are these two models different on these 1,034 questions" and not "are
these two methods different". Seed variance swallows it: across three seeds the
reverse-KL delta is `+1.71 ± 1.38`. Seed 1 gives it `+0.20`; seed 2 gives SeqKD
a **negative** `−0.29`. Only the server stage taken as a whole survives.

**Why, and this is the interesting part.** Higher pre-server scores buy smaller
server gains, and the endpoint barely moves:

```text
seed 0:  pre 57.35  ->  server +6.00  ->  63.35
seed 1:  pre 57.45  ->  server +5.03  ->  62.48
seed 2:  pre 59.77  ->  server +2.61  ->  62.38
```

The distillation stage pulls everything to about 62.7 regardless of where it
starts. That matches the 77% compression already measured on the ICL/no-ICL
contrast (2.90 pre-server becoming 0.68 after). It also means the federated
stage's own value is smaller than the `+2.13` recorded below: against
`base_rkl` at 61.22 the three-seed mean gives `+1.52`, and `base_rkl` still has
only one seed, so that row is untested across seeds.

Power: at `n=3`, `df=2`, an effect of 1.71 with `sd=1.38` cannot reach
significance. Detecting `d=1.24` at 80% power needs about `n=7`.

Scope correction, same day: this does not need resolving. SeqKD and reverse KL
are both distillation — hard labels and soft labels inside one component — so
the split is a design choice, not an ablation of the proposal. The ablation
that matters removes a whole component: distillation (`−4.55, p=0.046`) or the
federated stage (`−1.5`, one seed). Reverse KL stays, argued from [10] KID,
with `+1.71 ± 1.38` reported as measured and no claim resting on it.

**Unaffected:** every ICL conclusion. Those rest on six independent cells
pointing the same way with larger effects (`−3.87, p=0.003`; `−2.90, p=0.008`).

**Improved:** the no-ICL client adapters were finally evaluated
(54.55 / 53.38 / 55.71 / 53.68 / 57.64, mean 54.99). On the recommended branch
FedAvg reaches 57.35 — `+2.36` over the client mean and only `−0.29` from the
best client, a much better local-versus-federated story than the ICL branch's
`−1.84`.

### The distillation-only control at three seeds, 2026-08-15

`base_rkl` — the base model given the same server step and no private data at
all — was the last single-seed row in the ablation. Seeds 1 and 2 completed
(`artifacts/control/base_rkl_s{1,2}`, evals `eval_arms__s0__20260811T15{3849,5102}`).

| Seed | full pipeline | `base_rkl` | federated component | paired `p` |
|---|---:|---:|---:|---:|
| 0 | 63.35 | 61.22 | +2.13 | 0.017 |
| 1 | 62.48 | 60.54 | +1.93 | 0.025 |
| 2 | 62.38 | 62.28 | +0.10 | 1.000 |
| **mean** | **62.74** | **61.35** | **+1.39** | — |
| sd | 0.53 | 0.88 | 1.12 | `t=2.15`, `p=0.165` |

Per-seed `p` are exact two-sided McNemar on paired 1,034-row prediction files;
the bottom row is a two-sided `t` on three paired seed differences.

Reading: the federated stage is positive in every seed and never negative, but
seed 2 gives it essentially nothing, and across seeds it does not reach
significance. The same compression already seen elsewhere explains why — seed 2
starts from the highest pre-server score (59.77) and its distillation-only
control lands at 62.28, within 0.10 of the full pipeline. Whatever private data
adds, the teacher largely already supplies.

Consequence: the strong claim is the combination against **federation alone**
(`+4.55, p=0.046`). The claim against **distillation alone** is `+1.39` and is
reported as measured, not as established. Block B (out-of-distribution
evaluation) exists because Spider dev shares its corpus with the client shards
and not with the public BIRD pool, which biases this very row in the federated
arm's favour.

### Out-of-distribution evaluation, 2026-08-15 — the rows swap places

Six arms on `SPIDER_REALISTIC` (508), `SPIDER_SYN` (1,034), and `SPIDER_DK`
(535), seed 0, greedy, `k=0`. Runs `eval_arms__s0__20260815T*`. Motivation:
Spider dev shares its corpus with the private client shards and not with the
public BIRD pool, so the federated arm was being scored on its home
distribution.

| Arm | Spider dev | REALISTIC | SYN | DK | OOD pooled | drop |
|---|---:|---:|---:|---:|---:|---:|
| `base` | 50.00 | 40.35 | 37.04 | 41.68 | 39.05 | −10.95 |
| `fed_only` | 57.35 | 54.92 | 49.32 | 45.23 | 49.64 | **−7.71** |
| `seqkd_only` | 61.32 | 50.98 | 46.32 | 46.36 | 47.47 | −13.85 |
| `kd_only` | 61.22 | 51.18 | 47.20 | 47.85 | 48.34 | −12.88 |
| `full` | 63.35 | 52.95 | 49.61 | 47.85 | 49.98 | −13.37 |
| `central_ft` | 62.19 | 55.31 | 51.06 | 46.92 | **51.04** | −11.15 |

Pooled paired McNemar over all 2,077 questions:

| Contrast | Spider dev | OOD pooled | verdict |
|---|---:|---:|---|
| `full − base` | +13.35 | +10.93, `p<1e−4` | holds |
| `full − kd_only` (federated stage) | +2.13 | **+1.64, `p=0.0098`** | holds |
| `full − seqkd_only` (reverse KL over SeqKD) | +2.03 | **+2.50, `p=1e−4`** | stronger |
| `full − fed_only` (distillation) | +6.00 | **+0.34, `p=0.76`** | collapses |
| `full − central_ft` | +1.16 | −1.06, `p=0.30` | sign flips, neither significant |

**1. The row under test passed.** Per-set the federated stage is
`+1.77 / +2.42 / 0.00`, mean `+1.40` against the three-seed Spider figure of
`+1.39`. Pooled it reaches `p=0.0098`, tighter than anything it managed across
seeds on Spider dev. It is not an artefact of evaluating on the clients' own
corpus, and that was the question block B existed to answer.

**2. The row that was settled is the one that broke.** Distillation's marginal
value over the federated stage falls from `+6.00` (`p=4.8e−5`) to `+0.34`
(`p=0.76`), and is negative on REALISTIC. Distillation *from base* is still
worth a great deal — `kd_only − base` is `+10.15` to `+10.83` — so what
collapses is specifically its increment on top of federated training.

**3. The components are complementary along different shift axes.** On
paraphrase and synonym shift, private Spider federation carries the result and
distillation adds nothing (`fed_only − base` `+14.57` and `+12.28`). On
domain-knowledge shift it inverts: `kd_only` is `+6.17` over base while
`fed_only` manages `+3.55` (`p=0.067`). `full` is third, second, and joint first
across the three sets — the only arm that is never worst. This is a better
argument for the combination than the Spider-dev ablation was: neither half is
sufficient, and which half matters depends on the shift.

**4. Reverse KL over SeqKD is stronger off-distribution than on it.** `+2.50`,
`p=1e−4` pooled, against `+2.03` on Spider dev and `+1.71 ± 1.38` (`p=0.165`)
across seeds. Consistent with soft labels transferring teacher uncertainty in a
way hard labels do not. One seed off-distribution — do not promote it back to a
load-bearing claim, but "design choice with nothing resting on it" now
understates it.

**Cost:** `central_ft`, the compute-matched privacy-relaxed baseline, has the
best pooled OOD score. `full` beats it on Spider dev by `+1.16` and loses
off-distribution by `−1.06`, neither significant. "Competitive with centralized"
is accurate in both directions; "better than centralized" is not.

### Rounds 2 and 3, 2026-08-16 — the federated stage compounds

`fedkd` seed 0 extended to `T=3` (`federated__fedkd__s0__*__r{2,3}`), both the
pre-server aggregate and the post-server `M_G` evaluated each round
(`eval_arms__s0__20260816T034740`, `k=0`, `dail_weighted`, `n=1034`).

| Round | pre-server | endpoint |
|---|---:|---:|
| `T=1` | 57.35 | 63.35 |
| `T=2` | 64.02 | 66.15 |
| `T=3` | **66.05** | **69.54** |

| Contrast | Δ | `p` |
|---|---:|---:|
| pre-server `T=1→2` | +6.67 | <1e−4 |
| pre-server `T=2→3` | +2.03 | 0.046 |
| endpoint `T=1→2` | +2.80 | 0.0019 |
| endpoint `T=2→3` | +3.38 | 0.0002 |
| endpoint `T=1→3` | **+6.19** | <1e−4 |
| server step within `T=1` / `T=2` / `T=3` | +6.00 / +2.13 / +3.48 | <1e−4 / 0.123 / 0.0078 |

Both curves rise and every step is significant. The multi-round mechanism works,
and this is now the strongest result in the project.

**The fixed-point attractor is refuted for rounds, and only for rounds.**
Raising the pre-server score with a second *local epoch* moved the endpoint
`+0.19`; raising it with *rounds* moved the endpoint from 63.35 to 69.54.
Interleaved aggregation and distillation is what unlocks the gain; more local
training at one round does not.

**The confound control paid for itself.** At matched local work — two passes
over each client's data either way:

| | pre-server | endpoint |
|---|---:|---:|
| `T=1, E=2` | 61.90 | 63.54 |
| `T=2, E=1` | 64.02 | 66.15 |
| Δ | +2.13, `p=0.059` | **+2.61, `p=0.0067`** |

The value is in repeated communication rounds, not in more local training.
Without the `T=1, E=2` arm this would have been dismissed as "trained longer".

**Against centralized.** `T=2` beats the 1-epoch centralized reference by
`+3.97` (`p=0.0058`) and ties the 2-epoch one (`−0.87`, `p=0.552`) at matched
local work. `T=3` reaches `+2.51` over `central_2ep` (`p=0.055`) but is **not
budget-matched** — clients have taken three passes against the reference's two.
`central_3ep` is required before that row can be claimed.

Three limits: one seed; `T=3` also spends three server distillation stages
(3 × 3,873 public steps), so the compute story must be reported as a cost
column; and none of `T=2`/`T=3` has been evaluated out of distribution.

**Protocol note.** The first attempt at this evaluation
(`eval_arms__s0__20260816T015558`, deleted 2026-08-16) ran at `k=3` with
`dail_select` and `batch_size 1` because a PowerShell one-liner used `$T` for a
flag array and `$t` for a loop variable — PowerShell variable names are
case-insensitive, so the flags resolved to the integer `3` and argparse fell
back to defaults, adding a stray arm named `3`. Its numbers were discarded.
Check `config.json` for `k`, `retrieval`, and `batch_size` before trusting any
eval.

### Rounds off-distribution, per dataset, 2026-08-17

`T=2` and `T=3`, both stages, on the three perturbed Spider sets
(`eval_arms__s0__2026081{7T091741,7T093838,7T095343}`). Reported per dataset,
not pooled: the three sets probe different shift types and pooling hides which.

| Post-server EX | `T=1` | `T=2` | `T=3` | `T1→T3` | `p` |
|---|---:|---:|---:|---:|---:|
| Spider dev | 63.35 | 66.15 | 69.54 | +6.19 | <1e-4 |
| Spider-Realistic | 52.95 | 56.30 | 59.65 | +6.69 | <1e-4 |
| Spider-Syn | 49.61 | 52.03 | 55.51 | +5.90 | <1e-4 |
| Spider-DK | 47.85 | 50.47 | 52.71 | +4.86 | 0.0007 |

**The round result is distribution-independent.** Four benchmarks, same
direction, same magnitude, all significant. This is the paper's headline table.

The server step, however, is not:

| Server KD step | `T=1` | `T=2` | `T=3` |
|---|---:|---:|---:|
| Spider dev | **+6.00** (`p<1e-4`) | +2.13 (`p=0.123`) | **+3.48** (`p=0.0078`) |
| Spider-Realistic | -1.97 (`p=0.391`) | -0.79 (`p=0.767`) | +1.38 (`p=0.538`) |
| Spider-Syn | +0.29 (`p=0.887`) | -0.87 (`p=0.546`) | **0.00** (`p=1.000`) |
| Spider-DK | +2.62 (`p=0.130`) | -0.37 (`p=0.910`) | +1.87 (`p=0.229`) |

Nine off-distribution cells, none significant, signs alternating. The sharpest
comparison is Spider-Syn: `n=1034`, identical to Spider dev, so identical power.
Spider dev finds `+6.00` and `+3.48`; Spider-Syn finds `+0.29`, `-0.87`, and
exactly `0.00`. Realistic (`n=508`) and DK (`n=535`) lack the power to detect
~2 EX, so for those two the correct phrasing is "no evidence of an effect", not
"evidence of no effect".

**Execution errors tell the opposite story, and it is unanimous.** Every one of
the twelve pre→post cells reduces them:

| Exec-error rate | `T=1` | `T=2` | `T=3` |
|---|---|---|---|
| Spider dev | 22.8% → 12.9% | 18.4% → 12.0% | 17.2% → **9.8%** |
| Spider-Realistic | 23.0% → 14.4% | 19.5% → 15.2% | 18.5% → 13.0% |
| Spider-Syn | 27.8% → 17.9% | 20.8% → 17.6% | 19.6% → 16.4% |
| Spider-DK | 23.4% → 18.1% | 20.2% → 15.9% | 17.6% → 15.7% |

Read together: the teacher reliably teaches *executable* SQL everywhere, but the
conversion into *correct* SQL only shows up in distribution. Off distribution
the failures move from crashes into runnable-but-wrong answers.

**Interpretation caveat.** The `T=3` pre-server column is not a no-KD arm — its
clients started from `M_G(t=2)`, which had already been distilled twice. It
cannot be read as an ablation of the server step.

### BIRD cross-corpus transfer, 2026-08-18 — the components are orthogonal

BIRD dev, `n=1534`, `k=0`, greedy (`eval_arms__s0__20260818T140415`). This
reverses the 2026-07 decision to keep BIRD out of evaluation entirely; it enters
as a **cross-corpus transfer** row, never as a headline benchmark, and always
with its bias stated. BIRD dev's 11 databases are disjoint from the pool's 69,
so there is no schema leakage, but the corpus is the one the teacher was
distilled on, so the row favours the pipeline exactly as the Spider-derived sets
favour a Spider-trained model.

Absolute EX is low because `build_prompt` never renders BIRD's `evidence` hint.
All arms are handicapped identically, so within-table comparisons hold; the
numbers must not be compared to published BIRD results.

| Arm | EX | Exec-error |
|---|---:|---:|
| base | 10.89 | 46.5% |
| `T=1` pre-server | 11.15 | 55.3% |
| centralized 1 epoch | 11.34 | 48.9% |
| centralized 3 epochs | 12.91 | 42.6% |
| `T=3` pre-server | 17.67 | 37.9% |
| `T=1` post-server | 19.43 | 33.4% |
| **`T=3` post-server** | **21.58** | **29.9%** |

**1. The server step is decisive here**: `+8.28` at `T=1` (`p=2.8e-20`) and
`+3.91` at `T=3` (`p=6.1e-07`). Distillation's EX gain does transfer — within
the corpus it was distilled on. The precise statement is therefore not "KD does
not transfer" but **KD's gain is brittle to question paraphrase**: it appears on
BIRD (its training distribution) and on canonical Spider dev, and vanishes once
Spider questions are reworded.

**2. Federation alone buys nothing here**: `T=1` pre-server over base is `+0.26`
(`p=0.82`). Note that `t3_pre − fed_only = +6.52` is *not* the federated
contribution — `t3_pre` carries two prior distillation stages.

**3. Centralized is barely above base**: `+0.46` (`p=0.65`) at one epoch,
`+2.02` (`p=0.029`) at three. `T=3` beats `central_3ep` by `+8.67`
(`p=4.3e-20`); even `T=1` beats it by `+6.52`.

**4. The two components are orthogonal**, which is the strongest architectural
evidence the project has produced:

| | Spider-Realistic/Syn/DK | BIRD dev |
|---|---|---|
| federated rounds | +4.86 … +6.69, all significant | +0.26, `p=0.82` |
| server KD | 9 cells, none significant | +8.28 and +3.91, `p<1e-6` |

Each component carries exactly what the other leaves. Neither is redundant. On
Spider dev both work at once, which is why that benchmark alone cannot separate
them — it takes two corpora biased in opposite directions.

The asymmetry is worth stating: on the Spider variants centralized leads by
1–4 EX; on BIRD the pipeline leads by 8.67.

Also filled on 2026-08-18: the `fedkd` `T=1` cell at eval `k=3` is **60.06**,
i.e. `−3.29` against its own `k=0` result (`p=0.011`), consistent with every
other demos-at-inference measurement. The older 59.48 figure is the FLoRA-NA
branch and should not be used for the factor-FedAvg table.

### Missing pure-FL multi-round control, identified 2026-08-19

Advisor feedback requested one final-model comparison:

```text
Centralized <> FL <> FL-KD
```

The existing `fedkd_t2_preserver=64.02` and `fedkd_t3_preserver=66.05` cannot
fill the `FL` row. They are pre-server only within their current round; their
lineage is:

```text
base -> FL -> KD -> FL -> KD -> FL
```

Thus `T=2` pre-server already contains round-1 KD, and `T=3` pre-server contains
round-1 and round-2 KD. Only `T=1` pre-server (57.35) is currently a pure-FL
adapter.

Decision: run a separate factor-FedAvg branch through three rounds with no
server step at any round:

```text
base -> FL -> FL -> FL
```

Canonical output:

```text
artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0
```

The runner's `fedavg` arm has `server_method="none"`; its round output is the
FedAvg adapter itself, which becomes the next round's initialization. Exact
training and Spider/OOD/BIRD evaluation commands are Block K in
`PIPELINE_NEXT.md`. Status: **pending**. Until it completes, do not publish the
66.05 adapter under the name `FL` and do not make a causal `FL` versus `FL-KD`
claim at `T=3`.

### The budget-matched ceiling, 2026-08-16 — centralized saturates, federated does not

`central_3ep` trained as a third one-epoch continuation from
`central_ft_then_spider_ft` (same recipe that produced 67.02, one cosine cycle
per epoch), evaluated on Spider dev and the three OOD sets
(`eval_arms__s0__20260816T20{4913,5209,5930},T210235`).

| Centralized | Spider dev | Δ | `p` | OOD pooled |
|---|---:|---:|---:|---:|
| 1 epoch | 62.19 | — | — | 51.04 |
| 2 epochs | 67.02 | +4.84 | <1e−4 | 54.31 |
| 3 epochs | **67.60** | **+0.58** | **0.606** | **54.16** |

**The centralized curve is flat after epoch 2**, on Spider dev and pooled
off-distribution alike (`−0.14`, `p=0.888`). It plateaus around 67.0–67.6 EX.

Matched on passes over private data:

| Passes | federated | centralized | Δ | `p` |
|---|---:|---:|---:|---:|
| 1 | 63.35 | 62.19 | +1.16 | 0.432 |
| 2 | 66.15 | 67.02 | −0.87 | 0.552 |
| 3 | **69.54** | 67.60 | **+1.93** | 0.172 |

No cell is individually significant, so the claim is not the gap but the
**shape**: centralized goes `+4.84 → +0.58` and stops; federated goes
`+2.80 → +3.38` (`p=0.0002`) and is still rising. A plausible mechanism is that
each federated round adds a fresh teacher-distillation pass over public data,
whereas a third centralized epoch only re-reads Spider, which has run out of
signal. Execution quality differs in the same direction: `fedkd_t3` makes 101
execution errors against `central_3ep`'s 163.

**Compute is not matched, and must not be described as if it were.** `t3` spends
25,977 client steps plus 11,619 server steps (37,596 total) against `c3`'s
25,977 — about 45% more. What is matched is *private-data access*, which is the
privacy-relevant axis and the right one for this comparison, but the step counts
belong in a cost column.

**Where centralized still wins: off-distribution.** `central_3ep` is `+4.19`
(`p=0.0001`) over the `T=1` pipeline pooled across the three perturbed sets.
That gap has only ever been measured at `T=1`; `T=2` and `T=3` have not been
scored off-distribution. Closing or confirming it is now the highest-value
remaining run.

### The operating point problem, found 2026-08-15

Every federated arm trains one local epoch. A retained centralized result shows
that is far from converged:

| Adapter | Recipe | EX |
|---|---|---:|
| `ft_no_icl` | 1 epoch Spider from base | 62.19 |
| `central_ft_then_spider_ft` | plus a second identical epoch | **67.02** |

Verified: the second run's `init_adapter` is `ft_no_icl`, same data, same `lr`.
The extra pass is worth `+4.83 EX`, larger than every effect in the ablation.

This does **not** invalidate the compute-matched comparison — federated
`T=1, E=1` spends exactly one pass over the union of client data, so 62.19
remains the right matched baseline. It does invalidate the *ceiling* label:
whoever holds all the data trains to convergence, so the data-access ceiling is
67.02, not 62.19. Both belong in the paper under distinct labels. The residual
risk is external validity — arm rankings measured at an undertrained point need
not survive to convergence.

An LR-restart explanation is weakened by the code: each client runs its own
cosine schedule, so the federated branch already performs five restarts per
round and still reaches only 57.35. Working the other way, raising local epochs
under non-IID is the classic FedAvg drift trade.

Both questions were answered on 2026-08-15.

**The ceiling reproduces and it generalises** (`central_2ep`,
`eval_arms__s0__20260815T08{4527,4756,5343,5649}`):

| | Spider dev | REALISTIC | SYN | DK | OOD pooled |
|---|---:|---:|---:|---:|---:|
| `central_ft` (1 epoch) | 62.19 | 55.31 | 51.06 | 46.92 | 51.04 |
| `central_2ep` | **67.02** | **58.07** | **55.22** | **48.97** | **54.31** |

67.02 reproduces the old figure exactly under the current protocol. The second
epoch is `+4.84` on Spider dev and `+3.27` pooled off-distribution (`p<1e−4`),
so it is genuine capability, not Spider overfitting. This kills the hoped-for
argument that the public pool buys out-of-distribution robustness a centralized
model lacks — `central_2ep` leads on all four test sets.

**A second local epoch survives aggregation but not the server step**
(`eval_arms__s0__20260815T13{4454,4951,5953},T140507`):

| | Spider dev | OOD pooled |
|---|---:|---:|
| `fed_only` (`E=1`, pre-server) | 57.35 | 49.64 |
| `e2_pre_server` | **61.90** | **51.28** |
| `full` (`E=1`, endpoint) | 63.35 | 49.98 |
| `e2_full` | 63.54 | 50.02 |

The second epoch is worth `+4.55` (`p<1e−4`) before the server and `+0.19`
(`p=0.897`) after it. The classic FedAvg drift penalty did not appear at
`alpha=0.5, K=5`: `+4.83` centrally becomes `+4.55` after aggregation.

The consequence looked severe at the time: the distillation increment falls from
`+6.00` (`p<1e−4`) at `E=1` to `+1.64` (`p=0.264`) at `E=2`, and to `−1.25`
off-distribution. Read alone, that says the server stage is mostly a repair for
undertrained clients. The `T=2`/`T=3` results above put that in context — the
server step keeps contributing across rounds (`+2.13`, `+3.48`), so what `E=2`
shows is that a single round has a ceiling the server step cannot push past, not
that distillation is worthless.

### Reordering the pipeline, rejected 2026-08-12

Distillation first and the federated stage last (`kdfirst_s0`, eval
`eval_arms__s0__20260811T224124`) scores **61.61** against the current order's
63.35 at seed 0 (`+1.74` for the current order, `n01=108`, `n10=90`,
`p=0.227` — the two models disagree on 198 questions but not systematically).
Client training starting from an already-distilled model adds only `+0.38` over
`base_rkl`'s 61.22. Most of what the clients teach, the teacher already knows.
Keep distillation last.

### Centralized ICL 2x2, evaluated 2026-08-15

The federated 2x2 was completed on 2026-08-10; its centralized twin ran on
matched adapters (`ft_no_icl`, `ft_icl_k3`), evals
`eval_arms__s0__20260811T19{0659,2854}`, full Spider dev, greedy, seed 0.

| | eval `k=0` | eval `k=3` | drop under demos |
|---|---:|---:|---:|
| train `k=0` | 62.19 | 61.32 | −0.87, `p=0.526` |
| train `k=3` | **64.02** | 58.61 | **−5.42, `p=0.0001`** |
| delta | +1.84, `p=0.079` | **−2.71, `p=0.033`** | |

Two things, and they point opposite ways:

- **In-context training helps as pure augmentation, centrally.** At `k=0` the
  demo-trained adapter is `+1.84` (`p=0.079`, not significant). The federated
  pre-server cells gave the opposite sign (`−2.90, p=0.008`), so this is a
  centralized-only effect and does not rescue federated ICL.
- **At the ICL deployment mode the demo-trained model is worse**, `−2.71`
  (`p=0.033`), and it is the model that collapses hardest when handed demos
  (`−5.42, p=0.0001` versus `−0.87, p=0.526`). This is the fourth independent
  refutation of the DAIL-SQL §4.4.4 parity argument and the first one that is
  individually significant in both directions.

Net: every setting measured so far agrees that demonstrations at inference cost
this 1.5B student roughly 1–5 EX, regardless of how it was trained.

### Component ablation, K=5 T=1 seed 0, no-ICL branch

Completed 2026-08-11 when the base-only control finally ran. Every teacher
distillation before it had started from an already-trained adapter, so "base
model plus the same server step" — the ablation that removes the federated
stage — had never been measured. `experiments/client_train/run.py` with
`--init-adapter` unset on the same pool, same cache, same budget per stage;
evals in `eval_arms__s0__20260810T180648`.

| Configuration | EX | Δ vs full | `p` |
|---|---:|---:|---:|
| **Full pipeline** (client FT → FedAvg → SeqKD → RKL) | **63.35** | — | — |
| − reverse KL | 61.32 | −2.03 | 0.042 |
| − the whole server distillation | 57.35 | −6.00 | **4.8e−05** |
| − the whole federated stage (base + SeqKD + RKL) | 61.22 | −2.13 | 0.017 |
| − everything (base 1.5B) | 50.00 | −13.35 | — |

**Every component's removal costs significant EX at this seed.** The ablation
table is complete and it passes at seed 0. Superseded in part on 2026-08-15:
the `−2.13` federated row now has three seeds and becomes `−1.39, p=0.165`; the
`−2.03` reverse-KL row becomes `−1.71, p=0.165`. Only the whole-distillation
row (`−4.55, p=0.046`) survives replication. Read the three-seed section above
before quoting any number from this table.

Two readings that need stating plainly, because they change how the work is
pitched:

- **Public-pool distillation does most of the lifting.** Base → base+SeqKD+RKL
  is `+11.22` of the total `+13.35`; the federated stage adds `+2.13` on top.
  This does not weaken the ablation — a component earns its place by making
  things worse when removed, not by contributing equally — but the headline can
  no longer imply that federation produced the whole gain.
- **Federation alone is not competitive.** `fedavg_adapter` at 57.35 loses to
  public distillation from base at 61.22 (`+3.87` for the latter, `p=0.013`),
  and `base_rkl` (61.22) is statistically identical to `fedavg_pub` (61.32,
  `p=1.00`). The defensible claim is the interaction: neither half is enough on
  its own, and the combination beats each. At three seeds those two margins are
  `+1.39 (p=0.165)` over distillation alone and `+4.55 (p=0.046)` over
  federation alone — the second half of the interaction claim is established,
  the first is not.

**Reverse KL over its matched SeqKD control now replicates three times**, on
three unrelated client populations: `+1.55` from base (`p=0.121`), `+2.03`
federated no-ICL (`p=0.042`), `+2.51` federated ICL (`p=0.013`). Same sign,
magnitudes 1.55–2.51. This is the most robust result in the project.

A matched-compute control was considered and rejected. The full pipeline runs
12,532 optimiser steps against the base control's 3,873, but the extra steps
are on *different* data (private Spider shards), so re-running the control for
three epochs over the same 3,873 public rows would measure diminishing returns
on repeated data, not the value of private data. An ablation removes a
component together with its compute; that is what removing it means, and no FL
paper compute-matches ablation rows. Report the step counts as a cost column
instead. If the compute question ever needs a real answer, the control is *more
public data* (`bootstrap_full`, 7,968 rows) rather than more epochs, and it
would need a fresh teacher logit cache.

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

`scripts/exact_aggregate.py` (+ `tests/test_exact_aggregate.py`) settled it
without retraining. `stack` concatenates the factors into an exact rank-`K·r`
aggregate with `lora_alpha` rescaled so PEFT's `alpha/r` is unchanged; `svd`
gives the best rank-`r` fit to the same target — the control separating "the
aggregation error was fixed" from "the server just got a 5x bigger adapter".
Evaluated at `k=0` in `eval_arms__s0__20260810T151051`:

| Aggregator | rank | product error | EX | vs `factor_fedavg` | `p` |
|---|---:|---:|---:|---:|---:|
| `factor_fedavg` | 16 | 0.0687 | 54.45 | — | — |
| `florana` | 16 | 0.0661 | 54.45 | 0.00 | — |
| `exact_svd` | 16 | minimal at rank 16 | 54.26 | −0.19 | 0.851 |
| `exact_stack` | 80 | 0 | 55.13 | +0.68 | 0.311 |

**Aggregation error is not the cause.** `exact_svd` shares `exact_stack`'s
objective but is held at rank 16 and returns exactly nothing, so `exact_stack`'s
`+0.68` is the 5x capacity, not the exactness. Four aggregators spanning product
error 0.069 → 0 land within 0.87 EX with no cell significant, and `exact_stack`
is still 1.16 below the best client (`p=0.396`). `exact_svd` is the optimal
rank-preserving minimiser of that error, which bounds what any aggregator in the
FedEx-LoRA / Fed-SB family can buy here.

**The cause is test-set weighting.** Spider's EX weights each database by its
question count. Re-scored with databases weighted equally:

| | EX per question | EX per database |
|---|---:|---:|
| client 5 | **56.29** (1st) | 58.21 (3rd) |
| `factor_fedavg` | 54.45 | **58.25** (2nd) |
| `exact_stack` | 55.13 | **58.62** (1st) |
| clients 1 / 2 / 3 / 4 | 53.29 / 52.51 / 53.00 / 50.97 | 57.43 / 56.79 / 56.31 / 55.30 |

The ranking inverts: per database the aggregate already matches or beats every
client. Client 5 is strong on the largest databases — `world_1` (120 questions,
11.6% of the test set), `dog_kennels` (82), `tvshow` (62), `pets_1` (42) — and
those four alone exceed the whole 1.84 gap. Supporting facts: the aggregate sits
at per-database client mean **+1.24** (a broken aggregation would sit below it);
the test set shares no schema with training (20 test databases, 146 training
databases, empty intersection), so this is transfer, not memorisation; and
per-database wins are spread 4/6/4/1/5, with client 2 winning the most databases
(6/20) while ranking 5th overall. "Best client" is a property of the test set's
database-size mix, not a stable property of any client.

Verdict: the aggregate is not worse than the best client, and there is no
material headroom at the aggregation stage of this configuration.

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

Refreshed 2026-08-20 after the FedLS-SQL rename. `PIPELINE_NEXT.md` is the
executable source of truth; this section records only priority and rationale.

1. **P0 — pure FL through `T=3`, seed 0.** This is the missing independent
   lineage for the final `Centralized <> FL <> FedLS-SQL` table. Evaluate T1-T3
   on Spider dev, Realistic, Syn, DK, and BIRD.
2. **P0 — finalize the result registry.** Fill the FL row only from
   `fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter`; never use a pre-server
   adapter from the `fedkd` lineage as pure FL.
3. **P0 — consolidate efficiency evidence.** Report trainable parameters,
   adapter bytes, communication per round/total, wall time, peak VRAM, and
   deployed-SLM inference latency.
4. **P1 — replicate the T1-T3 trajectory** for seeds 1 and 2.
5. **P2 — optional baselines/sensitivity.** FedProx, teacher/student size,
   LoRA rank, and broader skew sweeps require scope agreement before compute is
   spent.

No additional ICL, FLoRA-NA, SC, or T4/T5 run is currently on the active queue.
Those branches remain reproducible but are closed or deferred under the new
paper scope.

Closed on 2026-08-18: the BIRD cross-corpus transfer table (7 arms), which
showed the two components are orthogonal, and the `fedkd` `T=1` eval-`k=3` cell.

Closed on 2026-08-17: `T=2`/`T=3` off-distribution at both stages (Block H).
The round result holds on all four benchmarks; the server step is null on all
nine off-distribution cells.

Closed on 2026-08-16: rounds 2 and 3 with per-round pre-server evaluation
(Block D), the `T=1, E=2` operating-point control and the `central_2ep` ceiling
(Block C), and `central_3ep`, the budget-matched ceiling (Block G) — which
showed the centralized curve saturating after epoch 2.

Closed on 2026-08-15: `base_rkl` seeds 1 and 2 (Block A), the six-arm
out-of-distribution evaluation (Block B), the pipeline-reorder probe, and the
centralized ICL 2x2.

Closed on 2026-08-11: seeds 1 and 2, and the no-ICL client evaluation.

Closed on 2026-08-10: the exact-aggregation diagnostic. Aggregation error is
not what separates the aggregate from the best client, and no aggregator in
that family has material headroom at `K=5, T=1`.

Closed on 2026-08-10: the 2x2 completion cell (`train_noicl` at `k=3`) ran and
refuted the parity hypothesis, so §5 is fully evidenced. Its private-pool twin
was dropped — the centralized cell already answered the question, and the
remaining nine `k=3` no-ICL cells only describe a retired eval mode.

## Closed or deferred branches

- Distillation-first pipeline order: rejected 2026-08-12, `61.61` against
  `63.35`. Distillation stays last.
- Relational hidden-state KD: removed; “RKD” means reverse-KL KD.
- Struct-SQL/SeqKD direction: removed from the active pipeline.
- Asymmetric-context KD: shelved after a negative one-seed probe.
- Skew-RKL `alpha=0.1`: rejected as default.
- BIRD as a *headline* evaluation benchmark: still not used, because it is the
  public training pool. Reopened 2026-08-18 as a **cross-corpus transfer** row
  only, with its pro-pipeline bias stated alongside the Spider variants'
  pro-centralized bias. Dev databases are disjoint from the pool's, so there is
  no schema leakage.
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
