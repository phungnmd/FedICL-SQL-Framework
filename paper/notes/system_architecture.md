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

The objective (since 2026-10-08) is one deployed SLM that is accurate on both
the clients' private domain (Spider EX) and the public domain (BIRD EX),
measured as two co-primary endpoints. Centralized Spider+BIRD training is the
reference ceiling for both; centralized Spider-only uses different data. CoT is one candidate teaching signal; clients and
inference may remain SQL-only. Measure both pipeline effectiveness over FL
and the incremental teacher contribution over matched public-gold training.
These are separate claims; a gold tie limits attribution, not the observed
pipeline gain. See `RELATED_WORK_NOVELTY_MATRIX.md` for the claim ladder.

Paper direction (owner decision 2026-10-11): direction A, an
empirical-method paper on method v1 confirmed on three seeds, with bounded
screens (ExST, execution-gated KD) under rules fixed in LAB_LOG 2026-10-11.
Plan: `paper/drafts/paper_direction_2026-10-11.md`. The earlier teacher-CoT
target is closed (P2.15).

## 2. Parts

| Part | Choice |
|---|---|
| Student (SLM) | Qwen2.5-Coder-1.5B-Instruct with LoRA r = 16 since P2.27 (earlier: Qwen2.5-1.5B-Instruct, Coder-0.5B). Deployed alone. |
| Teacher | Qwen2.5-Coder-7B, frozen, 4-bit, zero-shot, server only. |
| Clients | 5 clients, domain-cluster non-IID split `k5`, `alpha_0.1` since P2.27 (6-8 of 20 clusters per client); `alpha_0.5` is the heterogeneity contrast. Private data never leaves a client. |
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

Method v1 (fixed 2026-10-08): `A>K[fkl]>A[ntd]>K[fkl]>A[ntd]`, server Hinton
KD on all 9,428 BIRD rows, client FedNTD (beta 1, tau 3). Confirmation on
three seeds is pending (P2.31).

- Open: whether to keep client NTD. P2.29 (`h_plain`) decides by rule R1; if
  NTD is dropped, the method is Hinton AKAKA and its matched control is gold
  AKAKA.
- Bounded screens, not the method: ExST (client execution-verified
  self-training; S1, rules R4/R5; proposal in
  `paper/drafts/method_v2_proposal_2026-10-11.md`) and execution-gated Hinton
  KD (S2, rule R6, no published source).
- Stopped (P2.10): Struct-SQL QP-CoT in every stage with template client plans.
  The recipe underperformed; format and template mechanisms need separate
  evidence. Do not generalize this result to all CoT distillation.
- Closed: plan-task directions (P2.13-P2.15), P2.11, P2.12, P2.9 retention
  loss, weight merge (A1).

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

- Final-model Spider EX and BIRD EX are co-primary. Success: BIRD gain with
  exact McNemar p<.05 and Spider non-inferiority (95% Wald lower bound of the
  paired difference above -2.0 points), both against the same comparator.
  Spider variants measure robustness; EM is a diagnostic.
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
