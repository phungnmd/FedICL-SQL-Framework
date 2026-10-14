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
The research question, findings and open questions are in
[`RESEARCH_STATE.md`](RESEARCH_STATE.md). No method or paper story is fixed;
this file holds only the setup, the data rules and the claim limits.

## 2. Parts

| Part | Choice |
|---|---|
| Student (SLM) | Qwen2.5-Coder-1.5B-Instruct with LoRA r = 16 since P2.27 (earlier: Qwen2.5-1.5B-Instruct, Coder-0.5B). Deployed alone. |
| Teacher | Qwen2.5-Coder-7B, frozen, 4-bit, zero-shot, server only. |
| Clients | 5 clients, domain-cluster non-IID split `k5`, `alpha_0.1` since P2.27 (6-8 of 20 clusters per client); `alpha_0.5` is the heterogeneity contrast. Private data never leaves a client. |
| Aggregation | Sample-weighted, factor-wise FedAvg of LoRA factors. Plaintext. |
| Communication | LoRA adapters only. |
| ICL | None. Train, teacher, and evaluation all use k = 0 ([negative result](../archive/directions_2026-10/ICL_NEGATIVE_RESULT.md)). |

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

## 5. Implemented components

- Server objectives: SeqKD (CE on execution-selected teacher SQL), gold CE,
  and gold CE plus Hinton forward KL (T = 2 by default; P2.41 uses T = 1).
  Variants of the KD target: the virtual-teacher control (Yuan et al., CVPR
  2020: probability `a` on the gold token, the rest uniform, no teacher) and
  TAID (Shing et al., ICLR 2025: target interpolated from the detached student
  to the teacher).
- Client options: plain FedAvg rounds, FedNTD (not-true distillation, beta 1,
  tau 3), FedProx, frozen LoRA A with B-only upload (FFA-LoRA; dropped after
  the P2.39 pilot).
- Earlier chains (for example v1 `A>K[fkl]>A[ntd]>K[fkl]>A[ntd]` and
  `h_plain`) are results, not a fixed method.
- Closed for this paper: Struct-SQL plans and other plan or CoT tasks
  (P2.10-P2.15), retention loss (P2.9), weight merge (A1), KID, GKD, reverse
  KL, MiniLLM, deeper Hinton, ExST and execution-gated KD (never run).

## 6. Evaluation

- Report final-model Spider EX and BIRD EX for every arm. The primary
  endpoint and success criterion are fixed with the paper story, in LAB_LOG,
  before confirmation runs. Spider variants measure robustness; EM is a
  diagnostic. Spider test (2,147 rows) is the confirmation set (R10).
- Five sets: Spider dev (1,034), Spider-Realistic (508), Spider-SYN (1,034),
  Spider-DK (535), BIRD dev with evidence (1,534). BIRD `test.csv` is dev.
- Scorers: `spider_result_eq_v1` for Spider; `bird_official_set_pair_timeout30_v2`
  for BIRD (one 30-second budget for the prediction/gold pair).
- Student evaluation batch size is 16. Greedy decoding, seed 0 unless stated.
- Single-seed paired comparisons use exact McNemar tests on row-matched
  predictions; pooled seeds use the question-clustered test (R13).
- Schedules, settings and checkpoints may be chosen on the dev sets during
  exploration. The chosen configuration is then frozen and confirmed on seeds
  1-2 and Spider test; only those confirmation numbers support paper claims,
  and dev numbers are reported as exploratory (rules in
  `RESEARCH_STATE.md` section 5). New private validation rows stay at clients;
  only aggregate selection metrics may leave them. Creating a new holdout
  changes the training protocol and requires matched reruns; it cannot be
  retrofitted to old checkpoints.
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
