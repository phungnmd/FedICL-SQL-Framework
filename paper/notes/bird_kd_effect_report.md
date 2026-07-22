# BIRD KD Effect Report: matched Spider-FT2 control

**Date:** 2026-07-20  
**Status:** single training seed + single SC sampling seed; decision-grade probe,
not yet a headline multi-seed result.

## 1. Question and causal contrast

The observed post-KD adapter had the sequence:

```text
central Spider FT → BIRD teacher-EX-match RKD → central Spider FT
```

The matched control removes only the BIRD stage:

```text
central Spider FT → central Spider FT
```

Both final Spider stages use the same 8,659 examples, one epoch, batch size 1,
gradient accumulation 16, learning rate 2e-4, LoRA rank 16, max length 2,560,
and seed 0. Therefore their comparison estimates the incremental value of
inserting the 3,873-example BIRD teacher-EX-match `CE + reverse-KL` stage before
the final Spider recovery epoch.

This contrast identifies the effect of the **whole BIRD KD stage**. It does
not, by itself, identify the reverse-KL component: the KD arm also receives
3,873 additional BIRD CE updates. A matched
`BIRD teacher-EX-match CE-only → Spider FT` arm would be required to attribute
the difference specifically to teacher logits/RKL.

## 2. Runs and comparability audit

| Condition | Run ID | Overlay | Batch | Sampling |
|---|---|---:|---:|---|
| Spider-FT2 | `eval_arms__s0__20260720T104756` | none | 16 | greedy |
| BIRD-KD→Spider-FT | `eval_arms__s0__20260720T062440` | none | 16 | greedy |
| Spider-FT2 | `eval_arms__s0__20260720T121259` | SC | 1 | N=8, T=0.8, top-p=0.95 |
| BIRD-KD→Spider-FT | `eval_arms__s0__20260720T074657` | SC | 1 | N=8, T=0.8, top-p=0.95 |

All four evaluations use the same frozen 1,034-row Spider dev set, k=0,
full-schema prompting, `never_schema`, retrieval=`question` (irrelevant at
k=0), Qwen2.5-1.5B, and seed 0. Row IDs match exactly in each paired contrast.
The earlier accidental Spider-FT2 SC run with requested batch 16 is excluded.

McNemar tests below are exact two-sided tests over paired row outcomes.
Approximate 95% confidence intervals use the paired per-row difference.

## 3. Main results

### 3.1 Greedy decoding: no measurable EX benefit

| Metric | Spider-FT2 | BIRD-KD→Spider-FT | Delta | KD-only right | FT2-only right | McNemar p | paired 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| EX | 67.02 | 67.31 | **+0.29 pp** | 45 | 42 | 0.830 | [−1.48, +2.06] pp |
| EM | 62.57 | 63.93 | **+1.35 pp** | 60 | 46 | 0.206 | [−0.60, +3.30] pp |
| Execution errors | 166 | 180 | **+14 errors** | — | — | 0.180 | — |

The EX change is only three net rows out of 1,034. Churn is much larger than
the net change (45 gains versus 42 losses), so BIRD KD does not create a
strictly better greedy model. It shifts the decision boundary with essentially
zero aggregate EX benefit. Greedy executable reliability is directionally
worse, although the +14-error difference is not significant.

Greedy EX by hardness:

| Hardness | n | Spider-FT2 | BIRD KD | Delta |
|---|---:|---:|---:|---:|
| Easy | 248 | 88.71 | 90.73 | +2.02 pp |
| Medium | 446 | 69.28 | 68.83 | −0.45 pp |
| Hard | 174 | 54.60 | 53.45 | −1.15 pp |
| Extra | 166 | 41.57 | 42.77 | +1.20 pp |

The mixed signs reinforce the null reading: there is no stable greedy
improvement across difficulty levels.

### 3.2 Matched self-consistency: positive but qualified gain

| Metric | Spider-FT2+SC | BIRD-KD→Spider-FT+SC | Delta | KD-only right | FT2-only right | McNemar p | paired 95% CI |
|---|---:|---:|---:|---:|---:|---:|---:|
| EX | 73.40 | 75.24 | **+1.84 pp** | 59 | 40 | 0.0699 | [−0.05, +3.72] pp |
| EM | 67.41 | 69.83 | **+2.42 pp** | 74 | 49 | 0.0300 | [+0.32, +4.52] pp |
| Execution errors | 52 | 43 | **−9 errors** | — | — | 0.200 | — |

The matched SC result supports a narrower interpretation than “KD improves
the model”:

- EX increases by 19 net correct rows. The direction is favorable, but the
  exact paired test narrowly misses 0.05 and the confidence interval includes
  zero. Treat this as **suggestive**, not confirmed.
- EM increases by 25 net rows and is significant at this single seed. This is
  consistent with the final Spider epoch restoring Spider-style SQL while the
  preceding KD phase leaves additional useful structure in the distribution.
- Execution failures fall by nine, reversing the greedy direction, but this
  reliability difference is not independently significant.

SC EX transitions, including executability state:

| Before (Spider-FT2) → after (BIRD KD) | Rows |
|---|---:|
| wrong → correct | 45 |
| execution error → correct | 14 |
| correct → wrong | 33 |
| correct → execution error | 7 |
| execution error → executable but wrong | 10 |
| non-error → new execution error | 15 |

The 59 gains are therefore mostly genuine wrong→correct voting changes, not
only syntax repair. The 40 losses remain substantial; this is again a boundary
shift, not monotonic correction.

### 3.3 Where the SC gain occurs

| Hardness | n | Spider-FT2+SC | BIRD KD+SC | Delta | McNemar p |
|---|---:|---:|---:|---:|---:|
| Easy | 248 | 90.32 | 91.13 | +0.81 pp | 0.688 |
| Medium | 446 | 76.91 | 77.80 | +0.90 pp | 0.644 |
| Hard | 174 | 60.34 | 67.82 | **+7.47 pp** | 0.035 |
| Extra | 166 | 52.41 | 52.41 | 0.00 pp | 1.000 |

The aggregate EX signal is concentrated in `hard`: 23 KD-only-correct versus
10 FT2-only-correct rows. This subgroup result is mechanistically plausible —
hard queries offer more alternative plans for sampling/voting — but it is an
unadjusted post-hoc subgroup test and should not be cited as independently
confirmed without replication.

EM improvement is concentrated in `medium` (+3.81 pp, p=0.030); `extra` is
unchanged. Thus KD appears to affect structural choice and canonical rendering
differently across difficulty bands rather than applying a uniform lift.

## 4. What changed inside SC voting?

| SC diagnostic | Spider-FT2 | BIRD KD | Difference |
|---|---:|---:|---:|
| Executable candidates/query (of 8) | 6.403 | 6.376 | −0.027 |
| Zero-executable queries | 52 | 43 | **−9** |
| Execution-result groups/query | 1.344 | 1.356 | +0.012 |
| Winning-group size | 5.845 | 5.809 | −0.036 |
| Tie rate | 5.32% | 4.45% | −0.87 pp |

BIRD KD does **not** simply make every sampled candidate more executable: the
mean executable-candidate count is essentially unchanged and slightly lower.
Instead, it reduces catastrophic rows where all eight candidates fail (52→43)
while preserving slightly more result-level diversity (more groups, smaller
winning cluster) and producing fewer ties.

Conditional EX supports this interpretation:

| Executable candidates | Spider-FT2 n / EX | BIRD KD n / EX |
|---|---:|---:|
| 0 | 52 / 0% | 43 / 0% |
| 1–3 | 106 / 50.0% | 124 / 50.8% |
| 4–7 | 300 / 65.7% | 283 / **70.0%** |
| 8 | 576 / 88.4% | 584 / 88.5% |

The clearest behavioral gain is in the partially executable 4–7 bucket, not
the already-easy all-eight-executable bucket. A reasonable hypothesis is that
BIRD KD reshapes probability mass among plausible SQL modes, so execution
voting selects a better result cluster on ambiguous/hard questions. This is a
mechanism hypothesis, not yet a direct causal measurement of distributional
diversity.

## 5. KD × SC interaction

| Quantity | Spider-FT2 | BIRD KD | Difference-in-differences |
|---|---:|---:|---:|
| SC lift over greedy EX | +6.38 pp | +7.93 pp | **+1.55 pp** |
| SC lift over greedy EM | +4.84 pp | +5.90 pp | **+1.06 pp** |
| SC reduction in exec errors | −114 | −137 | **23 additional errors removed** |

This is the central result: most of the BIRD-stage value is latent under
greedy decoding and becomes visible only when sampling plus execution voting
queries the output distribution. The data are consistent with KD improving
the *candidate set/voteability* rather than the top-1 mode.

The interaction is descriptive because greedy and SC are separate decoding
runs, and only one sampling seed is available. It should not be assigned its
own p-value without a pre-specified paired interaction analysis over replicated
sampling seeds.

## 6. Valid and invalid claims

### Supported now

> On a matched seed-0 control, inserting the 3,873-example BIRD teacher
> EX-match KD stage before the final Spider epoch did not improve greedy EX
> (+0.29 pp; p=0.83), but produced a suggestive +1.84 pp gain under
> self-consistency execution voting (p=0.070), with gains concentrated on hard
> queries. EM improved +2.42 pp under SC (p=0.030).

### Not supported yet

- “BIRD KD significantly improves SC execution accuracy.” The EX p-value is
  0.0699 at one seed.
- “Reverse KL caused the gain.” The current control removes the whole BIRD
  phase, not only RKL; a BIRD CE-only matched arm is absent.
- “KD generally improves the student.” Greedy EX is flat, and the observed
  benefit is decoder-dependent.
- “Hard-query improvement is confirmed.” It is a single, uncorrected subgroup
  result.

## 7. Recommended next experiments

1. **Cheapest confirmation:** rerun both SC arms for sampling seeds 1 and 2;
   no adapter retraining is required. Report mean±SD of paired EX deltas and a
   seed-stratified paired analysis. This tests whether +1.84 pp is stable or a
   seed-0 sampling fluctuation.
2. **RKL attribution:** if one additional training arm is affordable, run
   `central FT → BIRD teacher-EX-match CE-only → Spider FT` with identical
   steps/data/order. Compare it directly with the RKD arm.
3. **Mechanism diagnostics:** pre-register hard-query and zero-executable-row
   analyses, then repeat them across sampling seeds. Also log effective SC
   batch size/OOM fallback so the execution recipe is fully auditable.

## 8. Bottom line

**BIRD KD is not justified as a greedy-accuracy method by this experiment.**
It is, however, a credible candidate for an **SC-compatible distribution
shaping method**: matched SC gains are positive, practically meaningful, and
focused on hard/partially executable cases, while EM reaches nominal
significance. The correct paper stance is “promising interaction requiring
sampling-seed replication,” not “KD proven effective.”
