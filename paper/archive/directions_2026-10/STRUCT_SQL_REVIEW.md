# Struct-SQL review — error taxonomy, CoT lineage, rationale-augmented SeqKD

> Status (2026-09-18): literature review only. Not protocol-v2 evidence.

arXiv:2512.17053v3 (Thaker & Bresler, Crater Labs; Canadian AI 2026).
Teacher GPT-4o, student Qwen3-4B-Instruct-2507, ablation Mistral-7B-Instruct-v3.0.
BIRD train → BIRD mini-dev. QLoRA r=64, alpha=128, lr 1e-4, one H200.

## 1. Error taxonomy

Every failure is classified into three levels, ordered by severity.

| Level | Meaning | Subcategories |
|---|---|---|
| GEN | no recognisable SQL produced | — |
| SYN | SQL unexecutable | no such column, no such table, keyword issue, clause order, other |
| SEM | executes but wrong result | column / row / row+column / value mismatch, empty output |

The ordering is the point: it turns one EX number into a claim about what kind
of model you have. GPT-4o fails mostly on SEM (bounded by logic). The untuned
4B student fails mostly on SYN, i.e. schema hallucination (bounded by not
knowing the database). Different problems, different fixes.

Two derived views:

- **State transitions** — classify each example before and after tuning, count
  the moves. Shows repair versus reshuffle. Struct-SQL keeps >81% of the base
  student's successes, converts 41.3% of SEM into successes, repairs 29% of SYN
  and demotes 41% of SYN to SEM; GEN 4.0% → 0.4%.
- **Gains vs losses against the teacher** — teacher right / student wrong
  (failed transfer) versus student right / teacher wrong (real generalisation).
  Struct-SQL has fewest losses, most gains.

Recorded numbers (share of mini-dev):

| Arm | GEN | SYN | no such column | SEM | empty output | value mismatch |
|---|---:|---:|---:|---:|---:|---:|
| Untuned student | 4.0 | 24.6 | — | 53.8 | — | — |
| FN-Gold | — | 23.6 | — | 33.0 | — | — |
| ReasonSQL | 2.2 | 21.2 | 19.0 | 39.8 | 10.6 | 18.2 |
| Struct-SQL | 0.4 | 16.8 | 15.8 | — | 7.6 | 19.6 |

Reading: FN-Gold cuts SEM hard (53.8 → 33.0) and barely moves SYN (24.6 →
23.6) — training on the final query alone does not teach grammar. Only the
structured rationale moves SYN (21.2 → 16.8).

Limits: outcome-based, so it names symptoms not causes; "other" is unclassified
by construction; it is really a parser over executor error strings plus a
result-set comparison.

**For us:** needs only prediction files, gold SQL and databases — no GPU. It is
the cheapest instrument for turning our open "why does the public stage damage
robustness" hypothesis into a measurement. Caveat: GEN and SYN are
scorer-independent, but every SEM subcategory depends on comparison semantics,
so compute and report SEM separately for Spider EX and the BIRD
set-of-row-tuples scorer. Do not pool.

## 2. CoT lineage

1. Plain CoT — think step by step.
2. Decomposition with multiple calls — DIN-SQL (schema linking, classification,
   generation, self-correction), Divide-and-Conquer CoT. Accurate, but one call
   per stage.
3. Single-pass structural CoT — emit a formal blueprint then the SQL in one
   generation. QP-CoT (from CHASE-SQL), QDecompose.

Struct-SQL sits on 3 and borrows the QP-CoT prompt unchanged. The contribution
is using that prompt as a *distillation target*, not as a prompt.

QP-CoT imitates `EXPLAIN`: which tables to scan, which filters, which join
path, which grouping and aggregation, in execution order. It is a procedure,
not an explanation — closed vocabulary, constrained step order, where free-form
CoT is open on both.

**The key ablation.** ReasonSQL (trained on free-form CoT) evaluated with the
QP-CoT prompt scores 29.20 against 36.90 with its native prompt: −7.7 points.
Two conclusions:

- ICL alone cannot install structure in an SLM. The few-shot prompt shows
  exactly how to write a plan and the untuned 4B model still scores 17.00 with
  it. Structure must enter through training. Consistent with our own negative
  ICL result.
- Training format and inference format must match.

The second is a direct conflict with `A>K>A`: our private clients train a flat
prompt, so if stage `K` trains QP-CoT and terminal `A` pulls back to flat, we
build the mismatch on purpose. Way out not considered by the paper: derive the
plan from gold SQL **locally** (`EXPLAIN QUERY PLAN` or linearised AST), no
teacher call, no breach of data isolation, private and server stages speak the
same format.

## 3. SeqKD with a rationale

Plain SeqKD trains on `Y_T` (teacher SQL). Rationale-augmented SeqKD trains on
`Z_T = R_T ⊕ Y_T`, same plain NLL loss:

```text
L_KD = − Σ log P_student(Z_T | Q, S)
```

No temperature, no KL, no teacher logits anywhere — the teacher is an API, so
logits were never available. The only variable is `R_T`:

- free-form CoT → **ReasonSQL**
- query execution plan → **Struct-SQL**

At inference the student reproduces the shape: plan first, then SQL. The plan
is generated, not supplied.

**Data construction.** Split databases 75/25 by `db_id` into in-domain and
out-of-domain pools (no shared schema). Sample stratified by SQL structure
category. Admit a sample only if the teacher's SQL is syntactically valid and
execution-correct. Final: 1,000 train / 150 ID val / 150 OOD val — categories
295 single-table, 229 subquery, 398 join-or-set-op, 78 both. ReasonSQL and
Struct-SQL use the same admitted rows and differ only in target format.

The execution filter is exactly our SeqKD selection rule (we keep 5,319 of
9,428). The stratification is not something we do.

**Results** — BIRD mini-dev EX, average generated tokens:

| Arm | Prompt | EX | Tokens | Simple | Moderate | Challenging |
|---|---|---:|---:|---:|---:|---:|
| Teacher GPT-4o | QP-CoT | 53.60 | 298 ± 96 | 68.24 | 52.00 | 36.27 |
| Student untuned | QP-CoT | 17.00 | 1465 ± 136 | 34.45 | 9.60 | 9.80 |
| FN-Gold | QP-CoT | 34.30 | 198 ± 257 | 45.94 | 32.80 | 20.58 |
| ReasonSQL | CoT | 36.90 | 99 ± 99 | 49.32 | 33.20 | **27.45** |
| ReasonSQL mismatched | QP-CoT | 29.20 | 145 ± 49 | 46.62 | 24.80 | 14.71 |
| **Struct-SQL** | QP-CoT | **45.00** | 362 ± 201 | 65.54 | 40.40 | 25.49 |

Mistral-7B: 7.22 / 25.10 / 29.31. Official BIRD test, single model, greedy:
60.42 (69.02 / 54.41 / 43.51), first among ≤4B as of 30 January 2026.

**Counterweights to cite alongside the +8.1:** Struct-SQL loses on Challenging
(25.49 vs 27.45) and on JOIN queries (25.5; ReasonSQL best, teacher only 36.4);
set operations weak everywhere; value mismatch slightly worse; inference costs
3.6× tokens; the execution filter caps the student at what the teacher can
already solve — a property we inherit in SeqKD.

## 4. Mapping and boundaries

| Their arm | Signal | Ours |
|---|---|---|
| FN-Gold | gold SQL | public-gold CE |
| ReasonSQL | teacher CoT + teacher SQL | SeqKD + rationale |
| Struct-SQL | teacher plan + teacher SQL | SeqKD + structured rationale |
| — | — | Hinton FKL, KID (no counterpart) |

- **No logit KD in this paper.** Not evidence for or against Hinton or the
  active KID lane. Keep it out of that argument.
- **Scale gap.** Smallest student tested is 4B; ours is 1.5B.
- **Teacher numbers are not comparable.** GPT-4o 53.60 on mini-dev vs our
  Qwen2.5-Coder-7B 47.07 on full evidence-aware dev — different splits. Check
  our teacher's plan quality directly.
- **No robustness evidence.** BIRD only, deliberately. Our failure mode
  (Realistic / SYN / DK after a public update) is untested here.

## 5. Actionable

**No GPU:** build the taxonomy over existing predictions for `A`, `A>K[fkl]`,
`A>A`, `A>K[fkl]>A`, `A>K[ce]>A` on all five sets, plus state transitions and
gains-vs-losses, SEM per scorer.

**GPU, gated:** arm `K[seq_qp]` on the same 5,319 rows as `K[seq]`, same
terminal `A`, same five-set gate. Gates first: (1) teacher plan quality on ~200
rows against the current 7,823/9,428 flat rate; (2) `prompt + plan + SQL`
length against `max_len=7168` and fail-closed; (3) decide the private-stage
prompt format before training, per §2.

**Fallback if 1.5B cannot carry a plan:** keep flat SeqKD, adopt only the
stratified execution-filtered pool construction. Their 1,000-curated-beats-
9,000-gold result is size-independent and speaks to our open pool-composition
question.

## 6. Open questions

- Does the syntax gain survive at 1.5B, or does the plan become the error
  source?
- Does a locally derived plan carry the same signal as a teacher-written one?
  If yes, the rationale stops needing the teacher — interesting for FL.
- Does any rationale survive terminal private consolidation? `A>K>A` erased
  teacher-specific effects before.
- Is the JOIN regression a property of query plans, or of this template?
