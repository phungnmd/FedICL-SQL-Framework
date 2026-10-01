# FedLS-SQL — lab log

Newest first. Each entry says what ran, the key numbers, where the evidence
lives, and what was decided. All numbers are seed 0, EX (%), protocol v2.

Older detail:

- 2026-09-03 to 2026-09-26, full text:
  [`LAB_LOG_2026-09-03_to_2026-09-26.md`](../archive/lab_log_2026-09/LAB_LOG_2026-09-03_to_2026-09-26.md)
- Protocol v1 (no BIRD evidence):
  `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`
- Before FedLS-SQL: `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`

## Where we are (2026-10-02, documentation review)

- Method: not frozen. Best tested endpoint so far is a public stage followed
  by one more private stage (`A>K>A`).
- Main objective: final Spider EX. Separate pipeline effectiveness over FL,
  private-round efficiency, and teacher-specific improvement over gold.
- Direction 1: A1 last reported running on 2026-10-01, not checked live in this
  review. A3 depth and A2 interleaving deferred behind the fixed-AKA CoT gate.
- Direction 2: P2.11 auxiliary-plan screen ready; P2.12 code ready but conditional
  and lower priority. Commands and decision gates belong to `PIPELINE_NEXT.md`.
- Current success target: teacher CoT exceeds full-gold and Hinton terminal
  Spider EX at `A>K>A`. Full-gold plus auxiliary teacher plans is a proposed
  direct contrast; it is not the implemented SeqKD-based P2.11 recipe.
- Stopped: P2.10 (QP-CoT everywhere with template client plans). Paused: P2.9
  retention.

## Evidence ledger — Spider private, BIRD public

`A` = one private round (5 clients, 1 local epoch, FedAvg). `K` = one public
server stage. Evaluation batch size 16. Exact paths and run IDs:
`RESULT_REGISTRY.md`.

| Trained artifact | Spider | Realistic | SYN | DK | BIRD | Result commit (nested) |
|---|---:|---:|---:|---:|---:|---|
| Teacher 7B, zero-shot | 76.69 | 71.06 | 63.83 | 62.43 | 47.07 | `e2ca26e`, `ec5b5e1` |
| Centralized E3 (Spider only) | 67.31 | 55.91 | 54.06 | 53.27 | 17.73 | `ec5b5e1` |
| Pure FL `A` (T1) | 57.35 | 54.92 | 49.32 | 45.23 | 14.80 | `ec5b5e1` |
| FL control `A>A` | 62.57 | 55.31 | 52.22 | 47.10 | 16.49 | `2a6e04c` |
| `A>K[fkl]` Hinton, 9,428 rows | 58.32 | 42.72 | 44.58 | 45.42 | 36.70 | `ec5b5e1` |
| `A>K[ce]` full gold, 9,428 rows | 55.03 | 47.05 | 43.91 | 40.93 | 32.14 | `5e4f005` |
| `A>K[fkl]>A` | 66.63 | 57.09 | 55.32 | 50.65 | 31.03 | `2a6e04c` |
| `A>K[ce]>A` full gold | 66.54 | 57.28 | 54.45 | 51.21 | 29.53 | `ccb3e91` |
| `A>K[seq]` SeqKD, 5,319 rows | 57.93 | 46.65 | 48.26 | 45.61 | 34.68 | `ec5b5e1`, `1e69ae3` |
| `A>K[ce]` selected gold, same 5,319 rows | 56.29 | 43.90 | 44.87 | 43.18 | 31.68 | `fb2329e` |
| `A>K[kid]` | 58.03 | 44.09 | 46.23 | 44.30 | 35.40 | `1e69ae3` |
| `A>K[seq]>A` | 64.99 | 57.68 | 54.55 | 50.28 | 28.42 | `1e69ae3` |
| `A>K[ce]>A` selected gold | 65.09 | 58.66 | 52.90 | 49.53 | 27.51 | `fb2329e` |
| `A>K[kid]>A` | 65.47 | 57.09 | 54.16 | 50.28 | 28.94 | `5d861f8` |
| `A>K[seq]>A[ret]`, λ = 1.0 | 61.61 | 50.79 | 49.90 | 46.92 | 30.31 | not committed (server) |
| `A>K[ce]>A[ret]` selected gold, λ = 1.0 | 60.74 | 50.20 | 49.42 | 45.79 | 28.88 | not committed (server) |

Reverse direction (BIRD private, Spider public), BIRD dev: pure FL 22.88,
selected gold 20.73, SeqKD 24.45 (`1b2c46a`).

BIRD-only baselines (BIRD private, no KD): base 15.97, centralized E1/E2
31.42/34.94, pure FL T1/T2/T3 22.75/28.36/31.10 (`e2ca26e`).

## What we have learned so far

1. The last private stage matters. `A>K[fkl]>A` beats `A>A` on all five sets
   (exact McNemar p = 0.000359/0.3557/0.00808/0.01834/<1e-40).
2. Hinton soft logits add nothing reliable after that stage. Against full-gold
   `A>K[ce]>A` the gap is +0.09/−0.19/+0.87/−0.56/+1.50 (p =
   1.000/1.000/.439/.749/.102).
3. KID ties SeqKD after the last stage and costs about 21.1 GPU-hours. Closed.
4. SeqKD beats selected gold at the public endpoint on all five sets. The last
   private stage removes most of the gap.
5. Keeping that gap with a retention loss (λ = 1.0) failed its gates.
6. The reverse direction agrees in sign: SeqKD beats FL, selected gold does
   not.

## 2026-10-02 - Research objective and continuation hypotheses (no GPU run)

- Subsequent owner clarification prioritizes a stronger teacher-CoT method
  over full BIRD-gold/Hinton at fixed `A>K>A`. Depth experiments are secondary.
  Added paper-grounded auxiliary-task and local STaR-SQL-style options, with
  explicit separation of existing runners, proposed variants, and unproven
  transfer to 1.5B federated Spider. No GPU run or code change followed.
- Owner clarified that the paper should establish useful public KD for
  federated Spider EX. CoT and a fixed `A>K>A>A>A` schedule are not requirements.
- The private MedQA example is an informal motivation only. No paper/repo was
  provided or audited; no result from it is treated as evidence for this task.
- Added A3: study consolidation depth after one public stage with matched FL
  and gold trajectories. Depth and stopping rule remain to be frozen; no new
  command, code, result, or GPU run was activated.
- Clarified the pipeline-versus-teacher claim ladder and centralized-reference
  limits. A gold tie restricts attribution without erasing a pipeline gain.
- Corrected P2.11 exposure-control wording and P2.12's unsupported claim that
  masking plan CE guarantees preserving plan generation. Kept the original
  A1 gate as a historical diagnostic alongside the new Spider-first objective.

## 2026-09-26 — P2.9 retention at λ = 1.0 fails; P2.9 paused

- Ran: `ret` for both arms, predictions read on the server (not committed).
- SeqKD − gold after `ret`: +0.87/+0.59/+0.48/+1.12/+1.43 (exact McNemar p
  .368/.78/.696/.362/.117).
- Gates: BIRD ≥ 1.5 fails. Spider-family mean (+0.77) ≥ 1.0 fails. No set
  below −1.0 passes. SeqKD Spider cost (−3.38) ≤ 1.0 fails.
- Retention buys +1.9 BIRD for −3.4 to −6.9 on every Spider-family set. It is
  dominated by a straight line between the public and plain-terminal points.
- Reading: the teacher edge shrinks as the model moves back to Spider
  (Spider-family mean +2.55 public, +0.77 `ret`, +0.33 terminal). The SQL-only
  edge looks like a gentler update, not extra knowledge.
- Decision: pause P2.9 and run P2.10 with a plain terminal stage. The
  target-NLL script was fixed first (nested `f210071`, `d8b4d5f`).

## 2026-09-25 — P2.9 variants added (no GPU run)

- Nested `78a34bd`: λ = 0.1 retention variant and WiSE-FT (exact LoRA
  midpoint). Reason: λ = 1.0 is 10× FedGKD's NLP weight.
- Nested `419a878`: D1 task arithmetic, `A>A + λ·(A>K − A)` with λ = 0.5 and
  1.0. It tells whether the KD update adds on top of FL. Tests: 690 pass.
- Literature check (LwF, FedGKD, FedNTD, WiSE-FT) is in
  `paper/archive/method_reviews_2026-09/KD_METHOD_REVIEW.md` §10–11.

## 2026-09-24 — Struct-SQL lineage implemented (P2.10, no GPU run)

- The P2.7/P2.8 plan format was not the paper's QP-CoT, and private stages
  were SQL-only. Nested `d66af7a` adds the real Struct-SQL lineage: format
  `qp_cot_v1`, private template `qp_ast_v1`, 75/25 ID/OOD split, 150+150
  validation rows, early stopping, stages `A[qp]`, `K[qp-ast]`,
  `K[qp-teacher]`, and a four-arm runner. Tests: 684 pass.
- CPU audits: template works on all 20,655 Spider/BIRD rows. Median target is
  247 tokens (Spider) and 297 (BIRD). BIRD has only 261 subquery-only rows, so
  that quota falls short; the shortfall is recorded.
- Deliberate differences from the paper: LoRA r = 16, zero-shot teacher, and
  our own validation cadence.

## 2026-09-24 — P2.6 public edge re-analyzed (CPU only)

SeqKD minus selected gold on the same 5,319 rows (committed batch-16
predictions from `fb2329e`), exact McNemar p in brackets:

| Endpoint | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| public `A>K` | +1.64 (.20) | +2.76 (.19) | +3.38 (.006) | +2.43 (.14) | +3.00 (.004) |
| terminal `A>K>A` | −0.10 (1.0) | −0.98 (.57) | +1.64 (.07) | +0.75 (.63) | +0.91 (.25) |

- At the public endpoint SeqKD also has fewer non-executable predictions on
  every set (for example Spider 19.5% → 14.1%).
- Decision: test whether a retention loss keeps the edge (P2.9, nested
  `e72ad2d`). P2.8 was archived unrun.

## Before 2026-09-24 (one line each)

Full text is in the archived log.

- 2026-09-23: P2.7 hardening (teacher journal, token counts). No new EX.
- 2026-09-22: P2.6 published (`fb2329e`). Terminal SeqKD − selected gold
  misses the promotion gate.
- 2026-09-20: P2.5 published. KID ties SeqKD; KID closed.
- 2026-09-17: GKD stopped for cost; partial artifacts are not evidence.
- 2026-09-16: P2.4a (`ccb3e91`): Hinton does not beat full-gold CE after
  terminal A. P2.3 (`2a6e04c`): `A>K>A` beats `A>A`.
- 2026-09-15: P2.2 published (`5e4f005`, `1b2c46a`, `ec5b5e1`). Stage chains
  (`run.py stage`) added (nested `810d8c4`, hardened to `014b118`).
- 2026-09-14: Hinton T1 learns BIRD but loses Spider robustness.
- 2026-09-11: teacher pools and BIRD baselines published (`e2ca26e`). Hinton
  forward KL replaces reverse KL as the soft-logit baseline.
- 2026-09-10: BIRD scorer set to the official 30-second pair timeout
  (`2178d5a`, `bird_official_set_pair_timeout30_v2`).
- 2026-09-06: P2.1 BIRD checkpoints rejected (974 truncated prompts). New
  7,168-token contract (`d21f777`).
- 2026-09-03: protocol reset. BIRD evidence had been left out of every prompt
  in protocol v1.
