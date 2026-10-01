# FedLS-SQL — system architecture

What this file is: the method, the data rules, and the limits on what we may
claim. Results are in `LAB_LOG.md`. The run queue is `PIPELINE_NEXT.md`.

The full previous version (with the implementation commit history) is
archived at
[`system_architecture_2026-09-24.md`](../archive/method_reviews_2026-09/system_architecture_2026-09-24.md).
The executable contract is `fedicl-sql/docs/PROTOCOL_V2.md`.

## 1. Goal

Train a small model (the SLM) on private Text-to-SQL data held by several
clients, without moving that data. Use a large frozen model (the teacher) on
the server, on public data only, to make the SLM better. Deploy only the SLM.

Question: can this beat plain federated learning (FL) on accuracy, while
keeping FL's privacy, communication, and deployment advantages?

The main objective is the deployed SLM's Spider EX, approaching or exceeding
the centralized Spider-only reference. That reference is not a ceiling and
uses different data/compute. CoT is one candidate teaching signal; clients and
inference may remain SQL-only. Measure both pipeline effectiveness over FL
and the incremental teacher contribution over matched public-gold training.
These are separate claims; a gold tie limits attribution, not the observed
pipeline gain. See `RELATED_WORK_NOVELTY_MATRIX.md` for the claim ladder.

The owner's current stronger-method target is teacher CoT that improves
terminal Spider EX over both full BIRD-gold and Hinton while keeping `A>K>A`
fixed. Prioritize resolving missing private rationale labels via auxiliary
public supervision or validated local rationale generation. More private
rounds are a secondary investigation, not a requirement for this target.

## 2. Parts

| Part | Choice |
|---|---|
| Student (SLM) | Qwen2.5-1.5B-Instruct with LoRA r = 16. Deployed alone. |
| Teacher | Qwen2.5-Coder-7B, frozen, 4-bit, zero-shot, server only. |
| Clients | 5 clients, semantic non-IID split (`k5`, `alpha_0.5`). Private data never leaves a client. |
| Aggregation | Sample-weighted, factor-wise FedAvg of LoRA factors. Plaintext. |
| Communication | LoRA adapters only. |
| ICL | None. Train, teacher, and evaluation all use k = 0. See `ICL_NEGATIVE_RESULT.md`. |

Names: the paper name is **FedLS-SQL**. The code package stays `fedicl_sql`.
`fedkd` is an internal arm name, not the paper name. Old run IDs and artifact
paths never change.

## 3. Data

Every run declares its dataset profile:

| Profile | Prompt | Use |
|---|---|---|
| `spider` | schema + question | Spider training and evaluation |
| `bird_with_evidence` | schema + evidence + question | main BIRD setting |
| `bird_no_evidence` | schema + question | disclosed ablation only |
| `legacy` | old Spider-shaped prompt | protocol v1 only; banned for new paper runs |

Private (client), public (server), and evaluation data are set separately.
Dataset names are never guessed from a path.

Two directions:

```text
primary: BIRD public (with evidence) -> Spider private -> Spider evaluation
reverse: Spider public               -> BIRD private (with evidence) -> BIRD evaluation
```

Public pool sizes (protocol v2):

- BIRD public, gold CE and Hinton KD: all **9,428** training rows.
- BIRD public, SeqKD: the **5,319** rows where the teacher's SQL matches gold
  by execution.
- Spider public, SeqKD: 7,251 of 8,659 rows.
- The 3,873-row pool is protocol-v1 history. Do not use it.

Teacher-target selection has two fixed stages: an 8-second quick execution
filter, then official EX-to-gold scoring on the survivors. A selected pool
belongs to its teacher. A new teacher needs new generation and filtering.

Other rules:

- Train and test never share a database (`db_id`).
- Test data never becomes training, retrieval, or teacher data.
- BIRD training uses `max_len=7168` and fails on overflow; no silent
  truncation.
- All v2 outputs live under `artifacts/protocol_v2/`.

## 4. Stages and chains

A run is a chain of stages:

- `A` — private stage: each client trains 1 local epoch on its own data, then
  FedAvg.
- `K[...]` — public server stage on the public pool:
  - `K[seq]` (SeqKD): CE on execution-selected teacher SQL.
  - `K[ce]`: CE on gold SQL (full 9,428 rows, or the same selected rows as
    SeqKD).
  - `K[fkl]` (Hinton): `0.5 CE + 0.5 T² KL(teacher || student)` on gold
    prefixes, T = 2.
- Examples: `A>K` ends after the public stage. `A>K>A` adds one more private
  stage. `A>A` is the matched FL control.

Rules that keep comparisons honest:

- Only all-`A` chains are pure FL controls. Any chain with a `K`, such as
  `A>K[fkl]>A`, is not pure FL.
- A pre-server adapter at T2/T3 inside a `fedkd` lineage is not pure FL,
  because it inherits earlier KD.
- A KD chain must be compared with an FL chain that has the same number of
  private stages.

## 5. Method status

The final method is **not frozen**.

- Reference: one public stage, `A>K`, with SeqKD, or with full public-gold CE
  plus Hinton forward KL.
- Candidate: terminal private consolidation, `A>K[fkl]>A`. It beats `A>A` on
  all five sets at seed 0, but it does not reliably beat `A>K[ce]>A`. So the
  gain is not yet attributable specifically to the teacher.
- Selected next design: P2.13 adds an auxiliary teacher-plan task to full
  public-gold SQL training at fixed `A>K>A`. Compare with fullgold and
  fullgold plus extra SQL on the same plan rows from the first screen.
  Both private stages and inference stay SQL-only; no private plan labels
  are needed. The recipe and two-GPU commands are in `PIPELINE_NEXT.md`;
  its runner is implemented and CPU-tested. GPU validation and EX benefit
  remain unproven.
- Parked alternatives: P2.11 uses the smaller SeqKD SQL base; P2.12 conditions
  private SQL training on generated plans with masked plan loss and a template
  fallback. Masking does not freeze the shared model's plan generation.
  A3 consolidation depth and A2 interleaving are deferred schedule questions.
  Collect the existing A1 weight-merge results separately; merge success is
  not required before testing P2.13.
- Stopped (P2.10): Struct-SQL QP-CoT in every stage with template client plans.
  The recipe underperformed; format and template mechanisms need separate
  evidence. Do not generalize this result to all CoT distillation.
- Paused (P2.9): a retention loss in the last private stage, toward the frozen
  post-K model.

Implemented server objectives: SeqKD, and gold CE plus Hinton forward KL
(T = 2). Reverse KL and v1 KID are archived. Protocol-v2 KID ran and was closed
as a negative ablation. GKD, clean RKL, MiniLLM, and deeper Hinton are closed
for this paper. There is no separate structural-distillation mechanism.

Required matched controls for any claim: base SLM, centralized SFT, pure FL,
public-gold CE, SeqKD, and gold CE + Hinton FKL.

Research notes on KD options (on-policy KD, retention, KD/FL ordering):
[`KD_METHOD_REVIEW.md`](../archive/method_reviews_2026-09/KD_METHOD_REVIEW.md)
(archived; not the method).

## 6. Evaluation

- Final-model Spider EX is the primary metric. Spider variants and BIRD EX
  are secondary robustness/transfer measurements; EM is a diagnostic.
- Five sets: Spider dev (1,034), Spider-Realistic (508), Spider-SYN (1,034),
  Spider-DK (535), BIRD dev with evidence (1,534). BIRD `test.csv` is dev.
- Scorers: `spider_result_eq_v1` for Spider; `bird_official_set_pair_timeout30_v2`
  for BIRD (one 30-second budget for the prediction/gold pair).
- Student evaluation batch size is 16. Greedy decoding, seed 0 unless stated.
- Paired comparisons use exact McNemar tests on row-matched predictions.
- Select schedules/checkpoints using a declared validation rule, not the best
  reported Spider dev score across an expanding search. New private validation
  rows stay at clients; only aggregate selection metrics may leave them.
  Creating a new holdout changes the training protocol and requires matched
  reruns; it cannot be retrofitted to old checkpoints. Existing dev-guided
  screens are exploratory and need independent confirmation.
- Dataset release, role, profile, evidence mode, schema mode, evaluator, and
  source hashes enter every fingerprint.

## 7. What we may claim

- Privacy is **structural data isolation**: private rows never leave the
  client. It is not differential privacy, not secure aggregation, and not
  protection against attacks on the parameters.
- The individual parts (FL + LoRA, LLM-to-SLM KD, execution-filtered SQL) are
  not new. Claim the task-specific workflow and its matched evidence. See
  `RELATED_WORK_NOVELTY_MATRIX.md`.
- One seed supports method selection, not a reliability claim.
- A KD-containing pipeline beating equal-private-round FL establishes its
  effectiveness at that budget. It does not isolate teacher knowledge from
  public data, selection, or extra compute. Teacher superiority requires a
  matched gold contrast; CoT superiority additionally requires SQL-only and
  auxiliary-task controls. A non-significant contrast is not an equivalence
  result. Publication tier does not determine these evidence requirements.
- Protocol-v1 results (BIRD evidence left out) are historical. They never fill
  a protocol-v2 table.
- Still valid from before the reset: Spider-only centralized, FL, and FedProx
  baselines; FL adapter communication accounting; the Secure Sum
  compatibility audit; the teacher-only timing. The student-versus-teacher
  deployment comparison must be rerun with the final v2 adapter.

References: [BIRD paper](https://arxiv.org/abs/2305.03111),
[official BIRD release page](https://github.com/bird-bench/bird-bench.github.io/blob/main/index.html),
[official mini-dev fine-tuning pipeline](https://github.com/bird-bench/mini_dev/tree/main/finetuning).
