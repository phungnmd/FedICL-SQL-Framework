# FedLS-SQL - valid results, adapters, and missing controls

Archived evidence inventory, refreshed 2026-10-06 against committed results.
This file preserves historical evaluation lineages and adds the P2.14-P2.17
results below; it is not an executable queue. Current decisions and commands
belong to [PIPELINE_NEXT.md](../../notes/PIPELINE_NEXT.md), result interpretation
to [LAB_LOG.md](../../notes/LAB_LOG.md), and canonical historical labels to
[RESULT_REGISTRY.md](../../notes/RESULT_REGISTRY.md). The latter has not yet
incorporated the P2.14-P2.17 inventory; use the linked manifests below for those
paths and run IDs.

EX is primary; EM is secondary. Exclude any lineage that consumed BIRD data
without evidence or the truncated-context P2.1 adapters. Retained Spider-only
baselines never consumed those invalid public updates. Historical batch-8
results stay separate from the batch-16 comparisons.

## Historical evaluation results retained

| Model | Dataset/setup | Method | Seed | Stage | EX (%) | EM (%) | n | Use |
|---|---|---|---:|---|---:|---:|---:|---|
| Qwen2.5 1.5B | Spider | Base | 0 | — | 50.00 | 21.08 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Centralized, continuous 3 epochs | 0 | E3 | 67.31 | 64.41 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 0 | T1 | 56.67 | 50.39 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 0 | T2 | 62.19 | 55.13 | 1,034 | convergence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 0 | T3 | 64.31 | 57.45 | 1,034 | baseline |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 1 | T1 | 57.45 | 50.58 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 1 | T2 | 61.70 | 53.97 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 1 | T3 | 61.99 | 54.74 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider | Pure FedAvg | 2 | T1 | 59.77 | 52.32 | 1,034 | seed evidence |
| Qwen2.5 1.5B | Spider, `alpha=0.1` | Pure FedAvg | 0 | T1 | 58.90 | 50.68 | 1,034 | skew control |
| Qwen2.5 1.5B | Spider, `alpha=0.1` | Pure FedAvg | 0 | T3 | 63.64 | 57.74 | 1,034 | skew control |
| Qwen2.5 1.5B | Spider | FedProx `mu=0.01` | 0 | T1 | 55.80 | 49.42 | 1,034 | negative optimizer ablation |
| Qwen2.5 1.5B | Spider | FedProx `mu=0.01` | 0 | T2 | 59.96 | 52.90 | 1,034 | negative optimizer ablation |
| Qwen2.5 1.5B | Spider | FedProx `mu=0.01` | 0 | T3 | 62.77 | 56.00 | 1,034 | negative optimizer ablation |
| Gemma 2 2B | Spider | Base | 0 | — | 52.22 | 22.44 | 1,034 | second-family anchor |
| Gemma 2 2B | Spider | Pure FedAvg | 0 | T1 | 57.16 | 49.52 | 1,034 | second-family FL baseline |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Base | 0 | — | 15.97 | 2.09 | 1,534 | official 30-second pair rescore |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Centralized | 0 | E1 | 31.42 | 4.04 | 1,534 | full-context baseline |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Centralized | 0 | E2 | 34.94 | 4.04 | 1,534 | full-context baseline |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Pure FedAvg | 0 | T1 | 22.75 | 1.56 | 1,534 | full-context baseline |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Pure FedAvg | 0 | T2 | 28.36 | 2.67 | 1,534 | convergence |
| Qwen2.5 1.5B | BIRD-original dev, evidence | Pure FedAvg | 0 | T3 | 31.10 | 3.26 | 1,534 | full-context baseline |
| Qwen2.5-Coder 7B | BIRD-original dev, evidence | Teacher, zero-shot | 0 | P2.2 | 47.07 | 6.52 | 1,534 | public-teacher capability anchor |
| Qwen2.5-Coder 7B | Spider | Teacher, zero-shot | 0 | P2.2 | 76.69 | 51.35 | 1,034 | public-teacher capability anchor |
| Qwen2.5 1.5B | Spider private; BIRD public | Pure FedAvg | 0 | T1 | 56.96 | 50.48 | 1,034 | shared matched-ladder initialization |
| Qwen2.5 1.5B | Spider private; matched BIRD gold | Public-gold CE | 0 | T1 | 56.09 | 20.70 | 1,034 | row-matched control |
| Qwen2.5 1.5B | Spider private; matched BIRD teacher SQL | SeqKD | 0 | T1 | 57.64 | 25.24 | 1,034 | reference transfer arm |

The canonical BIRD values above come from the saved predictions rescored with
`bird_official_set_pair_timeout30_v2`. The old truncated-context P2.1 lineage
remains excluded; these rows use the corrected 7,168-token, evidence-preserving
P2.1R adapters.

### Valid protocol-v2 teacher pool

| Transfer direction | Public source | Raw targets | Gold-valid | Officially scored after quick execution | EX-matched | Coverage | Status |
|---|---|---:|---:|---:|---:|---:|---|
| BIRD public → Spider private/eval | BIRD-original with evidence | 9,428 | 9,034 | 7,823 | 5,319 | 56.42% | complete; matched teacher/gold controls ready |
| Spider public → BIRD private/eval | Spider | 8,659 | 8,656 | 8,309 | 7,251 | 83.74% | complete; matched teacher/gold controls ready |

The conditional match rates are `5,319/7,823 = 67.99%` and
`7,251/8,309 = 87.27%`; paper-facing coverage always uses the full public
source denominator. Teacher dev EX and train-pool selection measure different
splits and must not be presented as the same statistic.

## Published P2.2-P2.6 evidence (historical)

P2.2c–f, P2.3, and P2.4a are complete and published (`5e4f005`, `1b2c46a`,
`ec5b5e1`, `2a6e04c`, `ccb3e91`). Counts, EX, paired row identities, prompt
parity, and stage-parent hashes have been checked. `A>K[fkl]>A` passed the
endpoint gate against `A>A`, but did not reliably beat `A>K[ce]>A`; the gain
in that one-K comparison cannot be assigned to soft logits. The two-K P2.17
comparison is recorded separately below. Concurrent historical execution
preserves accuracy validity, but its wall time and memory measurements are not
eligible for the paper resource table.

### Published P2.2 headline and full-public-gold control

All values are EX (%); all student evaluations below use batch size 16.
Central E3 is Spider-trained. Full-gold CE/Hinton use all 9,428 BIRD public
rows; SeqKD uses 5,319 execution-selected teacher sequences.

| Evaluation | n | Central E3 | Pure FL T1 | SeqKD T1 | Full-gold CE T1 | Hinton T1 | Teacher 7B |
|---|---:|---:|---:|---:|---:|---:|---:|
| Spider | 1,034 | 67.31 | 57.35 | 57.93 | 55.03 | 58.32 | 76.69 |
| Realistic | 508 | 55.91 | 54.92 | 46.65 | 47.05 | 42.72 | 71.06 |
| SYN | 1,034 | 54.06 | 49.32 | 48.26 | 43.91 | 44.58 | 63.83 |
| DK | 535 | 53.27 | 45.23 | 45.61 | 40.93 | 45.42 | 62.43 |
| BIRD dev, evidence | 1,534 | 17.73 | 14.80 | 34.68 | 32.14 | 36.70 | 47.07 |

Reverse BIRD-private/Spider-public ladder on BIRD dev:

| Method | EX (%) | EM (%) | n |
|---|---:|---:|---:|
| Shared Pure FL T1 | 22.88 | 1.56 | 1,534 |
| Matched public-gold CE | 20.73 | 3.78 | 1,534 |
| SeqKD | 24.45 | 4.30 | 1,534 |

Use the batch-size-16 headline rows for current comparisons. The older
56.96/57.64 Spider ladder used batch size 8 and has different SQL predictions
despite identical prompts; it remains a separate evaluation lineage. Full
paired analysis and artifact map: [P22_TRANSFER_REVIEW.md](P22_TRANSFER_REVIEW.md).

### Published P2.3 terminal endpoint ladder

| Evaluation | n | Pure FL `A` | Hinton `A>K` | `A>A` | `A>K>A` |
|---|---:|---:|---:|---:|---:|
| Spider | 1,034 | 57.35 | 58.32 | 62.57 | **66.63** |
| Realistic | 508 | 54.92 | 42.72 | 55.31 | **57.09** |
| SYN | 1,034 | 49.32 | 44.58 | 52.22 | **55.32** |
| DK | 535 | 45.23 | 45.42 | 47.10 | **50.65** |
| BIRD dev, evidence | 1,534 | 14.80 | 36.70 | 16.49 | **31.03** |

The terminal Hinton endpoint is positive against `A>A` on every set. Exact
paired McNemar p-values are 0.000359/0.3557/0.00808/0.01834/<1e-40 in table
order. Full interpretation and teacher-gap accounting:
[P23_TERMINAL_CONSOLIDATION_REVIEW.md](P23_TERMINAL_CONSOLIDATION_REVIEW.md).

### Published P2.4a full-public teacher-signal control

| Evaluation | `A>K[ce]>A` EX | `A>K[fkl]>A` EX | Hinton − CE (pp) |
|---|---:|---:|---:|
| Spider | 66.54 | 66.63 | +0.09 |
| Realistic | 57.28 | 57.09 | −0.19 |
| SYN | 54.45 | 55.32 | +0.87 |
| DK | 51.21 | 50.65 | −0.56 |
| BIRD dev, evidence | 29.53 | 31.03 | +1.50 |

No paired comparison is significant (`p=1.000/1.000/.439/.749/.102`). See
[P24_TEACHER_SIGNAL_REVIEW.md](P24_TEACHER_SIGNAL_REVIEW.md).

### Published P2.5 SeqKD versus KID endpoints

| Evaluation | SeqKD `A>K` | KID `A>K` | SeqKD `A>K>A` | KID `A>K>A` |
|---|---:|---:|---:|---:|
| Spider | 57.93 | 58.03 | 64.99 | 65.47 |
| Realistic | 46.65 | 44.09 | 57.68 | 57.09 |
| SYN | 48.26 | 46.23 | 54.55 | 54.16 |
| DK | 45.61 | 44.30 | 50.28 | 50.28 |
| BIRD dev, evidence | 34.68 | 35.40 | 28.42 | 28.94 |

Terminal KID-minus-SeqKD deltas are +0.48/−0.59/−0.39/0.00/+0.52 points;
none is paired-significant (`p=.644/.761/.731/1.000/.554`). KID public training
took 75,883 seconds for 5,319 examples and is retained as a valid negative
ablation, not an active method candidate.

### Valid Spider out-of-domain results

| Method | Stage | Realistic EX/EM | Syn EX/EM | DK EX/EM |
|---|---|---:|---:|---:|
| Centralized continuous 3 epochs | E3 | 55.91 / 53.54 | 54.06 / 49.90 | 53.27 / 47.29 |
| Pure FedAvg, seed 0 | T1 | 53.35 / 44.88 | 48.84 / 41.49 | 45.42 / 38.13 |
| Pure FedAvg, seed 0 | T2 | 55.51 / 48.03 | 51.74 / 45.26 | 47.10 / 41.31 |
| Pure FedAvg, seed 0 | T3 | 56.10 / 50.00 | 51.93 / 46.03 | 46.73 / 42.43 |

## Valid adapter inventory

These paths refer to the experiment server; adapters are gitignored. Only the
listed stages have retained evidence; reuse still requires the original model
and lineage contract plus server-side file validation. No listed 1.5B adapter
may initialize the proposed 0.5B student. A `round_N/fedavg_adapter` inside an old FedLS root
is not listed, because later rounds inherit invalid public supervision.

| Stable role | Valid adapter path | Scope |
|---|---|---|
| Qwen centralized E3 | `artifacts/baselines/central_3ep_standard_s0/adapter` | Spider-trained; evaluated on five sets |
| Qwen pure FL seed 0, T1–T3 | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_{1,2,3}/fedavg_adapter` | Spider only |
| Qwen pure FL seed 1, T1–T3 | `artifacts/federated/fedavg_noicl_k5_e1_t1_s1/round_{1,2,3}/fedavg_adapter` | Spider only |
| Qwen pure FL seed 2, T1 | `artifacts/federated/fedavg_noicl_k5_e1_t1_s2/round_1/fedavg_adapter` | Spider only |
| Qwen FedProx seed 0, T1–T3 | `artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0/round_{1,2,3}/fedavg_adapter` | Spider negative ablation |
| Qwen `alpha=0.1`, T1 | `artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1/fedavg_adapter` | Spider skew baseline |
| Qwen `alpha=0.1`, T2–T3 | `artifacts/federated/p13_alpha01_k5_e1_t1_fl_s0/round_{2,3}/fedavg_adapter` | Spider skew baseline |
| Gemma pure FL seed 0, T1 | `artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` | Spider only |
| Qwen BIRD centralized, continuous E1/E2 | `artifacts/protocol_v2/bird_original_ctx7168/qwen15b/centralized_e2_s0/epochs/epoch_{1,2}` | BIRD-original with evidence; official EX published |
| Qwen BIRD pure FL, T1–T3 | `artifacts/protocol_v2/bird_original_ctx7168/qwen15b/fedavg_k5_alpha05_e1_t3_s0/round_{1,2,3}/fedavg_adapter` | BIRD-original with evidence; official EX published |
| Protocol-v2 Spider-private shared FL T1 | `artifacts/protocol_v2/p22_spider_private_t1/shared_clients_s0/round_1/fedavg_adapter` | common initialization for the matched ladder |
| Protocol-v2 Spider-private matched-gold CE T1 | `artifacts/protocol_v2/p22_spider_private_t1/matched_gold_ce_s0/round_1/m_g` | 5,319-row BIRD public-gold control |
| Protocol-v2 Spider-private SeqKD T1 | `artifacts/protocol_v2/p22_spider_private_t1/seqkd_s0/round_1/m_g` | 5,319-row BIRD teacher-target arm |
| Protocol-v2 terminal SeqKD | `artifacts/protocol_v2/p25_seqkd_gkd_s0/seqkd_terminal/fedavg_adapter` | valid `A>K[seq]>A` endpoint; seed 0 |
| Protocol-v2 KID public | `artifacts/protocol_v2/p25_seqkd_kid_s0/kid_public/m_g` | valid negative KID ablation; seed 0 |
| Protocol-v2 terminal KID | `artifacts/protocol_v2/p25_seqkd_kid_s0/kid_terminal/fedavg_adapter` | valid negative `A>K[kid]>A` endpoint; seed 0 |
| Protocol-v2 Spider-private full-gold CE T1 | `artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1/full_gold_ce_s0/round_1/m_g` | all 9,428 BIRD public rows with evidence |
| Protocol-v2 Spider-private Hinton FKL T1 | `artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1/hinton_fkl_t2_alpha05_s0/round_1/m_g` | all 9,428 BIRD gold prefixes; temperature 2; candidate parent for consolidation |
| Protocol-v2 Spider-private `A>A` | `artifacts/protocol_v2/p23_spider_private_terminal/a_a_s0/fedavg_adapter` | matched terminal-private control; published five-set endpoint |
| Protocol-v2 Spider-private `A>K[fkl]>A` | `artifacts/protocol_v2/p23_spider_private_terminal/a_k_a_s0/fedavg_adapter` | tested seed-0 endpoint; not proven teacher-specific |
| Protocol-v2 Spider-private `A>K[ce]>A` | `artifacts/protocol_v2/p24_gold_ce_terminal/a_kce_a_e1_s0/fedavg_adapter` | full-9,428-row public-gold terminal control; published five-set endpoint |
| Protocol-v2 BIRD-private shared FL T1 | `artifacts/protocol_v2/p22_bird_private_t1/shared_clients_s0/round_1/fedavg_adapter` | reverse ladder initialization |
| Protocol-v2 BIRD-private matched-gold CE T1 | `artifacts/protocol_v2/p22_bird_private_t1/matched_gold_ce_s0/round_1/m_g` | selected Spider gold control |
| Protocol-v2 BIRD-private SeqKD T1 | `artifacts/protocol_v2/p22_bird_private_t1/seqkd_s0/round_1/m_g` | selected Spider teacher sequences |

All listed P2.2 endpoints have published training/evaluation records. Weight
files remain on the server; this inventory follows published paths and does
not claim local rehashing of absent weights. Base models are anchors, not adapters.

## Current preparation and unresolved evidence (2026-10-06)

- Both owner repositories use `main`. The next preparation is a fresh
  `Qwen/Qwen2.5-Coder-0.5B-Instruct` screen with the same frozen 7B teacher:
  centralized Spider E3, pure FL `A>A>A`, full gold and Hinton `A>K>A>K>A`.
  The runner, GPU smoke, and launch commands are pending. No 0.5B result or
  adapter is registered. All new student stages must use `target_fp32`.
- Start from the fresh 0.5B base, with new output identities. Validate
  student/teacher token alignment and the full cache contract before reusing
  logits. Size and code specialization change together, so this screen cannot
  isolate a size effect.
- P2.16 centralized E1-E4 and a third public stage for P2.17 have no completed
  rows in the published manifests checked here. The older centralized E3
  reference (67.31 Spider EX) is a separate retained artifact.
- Final method selection, additional training seeds, stronger non-IID
  confirmation, and final-student resource measurements remain open. A paired
  question test at seed 0 does not establish an across-seed method advantage.
- Plan-task work is closed after P2.14/P2.15; P2.10 client plans and the A1
  merge gate are closed, P2.13 was superseded, and P2.9 retention is paused.
  P2.11/P2.12 and the old P2.7 screen are not active launch instructions.
- KID remains a published negative ablation. Partial GKD and the retired
  SeqKD-plus-Hinton hybrid are not completed evidence or reusable adapters.
- Server lane status and adapter bytes have not been checked live. Do not
  infer idle GPUs or available weights from this inventory.

Secure Sum compatibility, adapter-byte accounting, and teacher-only resource
measurements are separate technical evidence. They do not establish DP or
replace final-adapter accuracy and resource measurements. Historical concurrent
run timings are not controlled paper resource benchmarks.

## Excluded lineage

All old Qwen/Gemma FedLS, SeqKD, public-gold, reverse-KL, mixed pre-server, and BIRD
trained-arm results are archived. Their teacher targets/logits either omitted
BIRD evidence or inherited such a server update. P2.1 trained arms are also
archived because `max_len=2560` truncated required context. None may be copied
back into an active table or used to initialize protocol-v2 training.
