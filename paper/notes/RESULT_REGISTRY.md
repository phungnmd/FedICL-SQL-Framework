# FedLS-SQL — result registry

What this file is: for every number we may use, where it came from. One row
per trained artifact or evaluation. Numbers only; their meaning is in
`LAB_LOG.md`, and paper tables are in `paper/results/MAIN_RESULTS.md`.

Rules:

- Only protocol-v2 results enter method or accuracy tables.
- A number needs a result commit (nested `fedicl-sql/`), a config, a dataset,
  a seed, and prediction files. If one is missing, the number is not used.
- Adapter paths are on the GPU server under `fedicl-sql/`. Adapters are
  gitignored. Only the adapters listed here may start a new run.
- EX is primary; EM is secondary. BIRD `test.csv` is the 1,534-row **dev** set.
- BIRD EX must use scorer `bird_official_set_pair_timeout30_v2` (one 30-second
  budget for the prediction/gold pair). The older `bird_official_set_v1` gave
  60 seconds to each query; its saved SQL can be rescored, but its embedded EX
  is diagnostic only. Spider EX uses `spider_result_eq_v1`.

Merged on 2026-09-29 from `VALID_RESULTS_AND_ADAPTERS.md` and the P2.2 review.
Full originals:
[`archive/results_reviews_2026-09/`](../archive/results_reviews_2026-09/).
Protocol-v1 registry:
`paper/archive/protocol_v1_no_bird_evidence/RESULT_REGISTRY_v1.md`.

## 1. Protocol-v2 result IDs

| Stable ID | Result | Result commit / trail |
|---|---|---|
| `v2.bird.base` | 15.97 EX | `f99febd`, rescore `e9bde43` |
| `v2.bird.central` | E1/E2 31.42/34.94 EX | `e2ca26e` (P2.1R, `max_len=7168`) |
| `v2.bird.fl` | T1/T2/T3 22.75/28.36/31.10 EX | `e2ca26e` (P2.1R) |
| `v2.teacher.pools` | BIRD public 5,319/9,428 kept; Spider public 7,251/8,659 kept | `e2ca26e` |
| `v2.spider.fl` | shared T1 57.35 EX (batch 16) | `ec5b5e1` |
| `v2.bird_to_spider.reference` | five-set headline and full-gold control | `ec5b5e1`, `5e4f005` |
| `v2.spider_to_bird.reference` | FL/gold/SeqKD 22.88/20.73/24.45 EX | `1b2c46a` |
| `v2.bird_to_spider.terminal` | `A>A` and `A>K[fkl]>A` on five sets | `2a6e04c`, producer `362aced` |
| `v2.bird_to_spider.terminal_ce` | full-gold `A>K[ce]>A` on five sets | `ccb3e91` |
| `v2.bird_to_spider.seqkd_kid` | SeqKD and KID, public and terminal | `1e69ae3`, `5d861f8` |
| `v2.bird_to_spider.selected_gold` | selected-gold public and terminal | `fb2329e` |
| `v2.bird_to_spider.p29_ret` | `ret` λ = 1.0, both arms | **not committed**; server only |

The five-set numbers for each ID are in the `LAB_LOG.md` evidence ledger.

## 2. Spider-private, BIRD-public artifacts (seed 0)

| Chain | Adapter path | Parent / run ID |
|---|---|---|
| FL `A` (shared T1) | `artifacts/protocol_v2/p22_spider_private_t1/shared_clients_s0/round_1/fedavg_adapter` | `federated__fedavg__s0__935d572565cc__154540d3__r1` |
| `A>K[ce]` selected gold, 5,319 rows | `artifacts/protocol_v2/p22_spider_private_t1/matched_gold_ce_s0/round_1/m_g` | `federated__fedavg_pub__s0__4d679d6668dd__37fd379d__r1` |
| `A>K[seq]` SeqKD, 5,319 rows | `artifacts/protocol_v2/p22_spider_private_t1/seqkd_s0/round_1/m_g` | `federated__fedavg_pub__s0__2b42f25abe82__9c5906d8__r1` |
| `A>K[ce]` full gold, 9,428 rows | `artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1/full_gold_ce_s0/round_1/m_g` | P2.2f |
| `A>K[fkl]` Hinton, 9,428 rows, T = 2 | `artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1/hinton_fkl_t2_alpha05_s0/round_1/m_g` | P2.2d |
| `A>A` | `artifacts/protocol_v2/p23_spider_private_terminal/a_a_s0/fedavg_adapter` | P2.3 |
| `A>K[fkl]>A` | `artifacts/protocol_v2/p23_spider_private_terminal/a_k_a_s0/fedavg_adapter` | P2.3 |
| `A>K[ce]>A` full gold | `artifacts/protocol_v2/p24_gold_ce_terminal/a_kce_a_e1_s0/fedavg_adapter` | P2.4a |
| `A>K[seq]>A` | `artifacts/protocol_v2/p25_seqkd_gkd_s0/seqkd_terminal/fedavg_adapter` | P2.5 |
| `A>K[kid]` | `artifacts/protocol_v2/p25_seqkd_kid_s0/kid_public/m_g` | P2.5, negative ablation |
| `A>K[kid]>A` | `artifacts/protocol_v2/p25_seqkd_kid_s0/kid_terminal/fedavg_adapter` | P2.5, negative ablation |
| `A>K[ce]>A` selected gold | `artifacts/protocol_v2/p26_matched_selected_gold_s0/terminal_a/fedavg_adapter` | P2.6, stage `p26_matched_selected_gold_terminal_s0` |

Parent run IDs are directories under `fedicl-sql/experiments/federated/results/`.
Teacher-target pool (SeqKD and selected gold):
`processed_data/protocol_v2/BIRD/original_train9428_dev1534/teacher_targets/qwen7b_to_qwen15b_evidence_s0/`.
Hinton teacher-logit cache (9,428 rows, fp16, 9,425 unique shards):
`artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0`.

### P2.2 evaluation directories

Under `fedicl-sql/experiments/eval_arms/results/`. Each holds `config.json`,
`metrics.json`, and per-arm prediction CSVs. Producing code SHA `e2ca26e`.

| Evaluation | n | Headline (FL, SeqKD, Hinton, Central E3) | Full-gold CE |
|---|---:|---|---|
| Spider | 1,034 | `eval_arms__s0__20260913T122834` | `eval_arms__s0__20260915T055906` |
| Realistic | 508 | `eval_arms__s0__20260913T124007` | `eval_arms__s0__20260915T060130` |
| SYN | 1,034 | `eval_arms__s0__20260913T125953` | `eval_arms__s0__20260915T060559` |
| DK | 535 | `eval_arms__s0__20260913T131303` | `eval_arms__s0__20260915T060854` |
| BIRD dev, evidence | 1,534 | `eval_arms__s0__20260913T141554` | `eval_arms__s0__20260915T062256` |

Reverse ladder: `eval_arms__s0__20260912T220957`. Teacher on the Spider
variants: `eval_arms__s0__20260913T144510` (Realistic),
`eval_arms__s0__20260913T155617` (SYN), `eval_arms__s0__20260913T163445` (DK).
P2.3 to P2.6 evaluation records are inside their result commits.

### Two Spider evaluation lineages

The first matched ladder used evaluation batch size 8: FL/selected gold/SeqKD
56.96/56.09/57.64 EX (EM 50.48/20.70/25.24). The headline rerun uses batch
size 16: FL 57.35, SeqKD 57.93. Prompts are identical, but predicted SQL
differs in 86 (FL) and 58 (SeqKD) rows. Use batch 16 for comparisons. Keep
batch 8 as a separate lineage. The cause of the drift is not proven.

## 3. BIRD-private artifacts (seed 0)

| Chain | EX / EM | Adapter path |
|---|---|---|
| Centralized E1, E2 | 31.42 / 4.04, 34.94 / 4.04 | `artifacts/protocol_v2/bird_original_ctx7168/qwen15b/centralized_e2_s0/epochs/epoch_{1,2}` |
| Pure FL T1, T2, T3 | 22.75 / 1.56, 28.36 / 2.67, 31.10 / 3.26 | `artifacts/protocol_v2/bird_original_ctx7168/qwen15b/fedavg_k5_alpha05_e1_t3_s0/round_{1,2,3}/fedavg_adapter` |
| Base (no adapter) | 15.97 / 2.09 | — |
| Shared FL T1 (reverse ladder) | 22.88 / 1.56 | `artifacts/protocol_v2/p22_bird_private_t1/shared_clients_s0/round_1/fedavg_adapter` |
| `A>K[ce]` selected Spider gold | 20.73 / 3.78 | `artifacts/protocol_v2/p22_bird_private_t1/matched_gold_ce_s0/round_1/m_g` |
| `A>K[seq]` Spider SeqKD | 24.45 / 4.30 | `artifacts/protocol_v2/p22_bird_private_t1/seqkd_s0/round_1/m_g` |

All on BIRD-original dev with evidence, n = 1,534.

## 4. Teacher anchors and pools

Teacher: Qwen2.5-Coder-7B, zero-shot, frozen.

| Evaluation | EX / EM | n | Trail |
|---|---|---:|---|
| BIRD dev, evidence | 47.07 / 6.52 | 1,534 | `e2ca26e` |
| Spider | 76.69 / 51.35 | 1,034 | `e2ca26e` |
| Realistic, SYN, DK | 71.06, 63.83, 62.43 EX | 508, 1,034, 535 | `ec5b5e1` |

| Direction | Public source | Raw | Gold-valid | Scored after quick execution | EX-matched | Coverage |
|---|---|---:|---:|---:|---:|---:|
| BIRD public → Spider private | BIRD-original, evidence | 9,428 | 9,034 | 7,823 | 5,319 | 56.42% |
| Spider public → BIRD private | Spider | 8,659 | 8,656 | 8,309 | 7,251 | 83.74% |

Coverage always uses the full public source as denominator. Conditional match
rates are 67.99% and 87.27%. Teacher dev EX and pool selection are different
statistics.

## 5. Spider-only baselines kept from before the reset

These never touched a BIRD-derived checkpoint or pool, so they stay valid.
Qwen2.5-1.5B unless noted; Spider dev, n = 1,034. Their trail is the archived
v1 registry plus the adapter paths below.

| Method | Seed | Stage | EX | EM |
|---|---:|---|---:|---:|
| Base | 0 | — | 50.00 | 21.08 |
| Centralized, 3 continuous epochs | 0 | E3 | 67.31 | 64.41 |
| Pure FedAvg | 0 | T1 / T2 / T3 | 56.67 / 62.19 / 64.31 | 50.39 / 55.13 / 57.45 |
| Pure FedAvg | 1 | T1 / T2 / T3 | 57.45 / 61.70 / 61.99 | 50.58 / 53.97 / 54.74 |
| Pure FedAvg | 2 | T1 | 59.77 | 52.32 |
| Pure FedAvg, `alpha=0.1` | 0 | T1 / T3 | 58.90 / 63.64 | 50.68 / 57.74 |
| FedProx `mu=0.01` (negative) | 0 | T1 / T2 / T3 | 55.80 / 59.96 / 62.77 | 49.42 / 52.90 / 56.00 |
| Gemma 2 2B base | 0 | — | 52.22 | 22.44 |
| Gemma 2 2B pure FedAvg | 0 | T1 | 57.16 | 49.52 |

Out-of-domain, EX / EM:

| Method | Stage | Realistic | SYN | DK |
|---|---|---:|---:|---:|
| Centralized | E3 | 55.91 / 53.54 | 54.06 / 49.90 | 53.27 / 47.29 |
| Pure FedAvg, seed 0 | T1 | 53.35 / 44.88 | 48.84 / 41.49 | 45.42 / 38.13 |
| Pure FedAvg, seed 0 | T2 | 55.51 / 48.03 | 51.74 / 45.26 | 47.10 / 41.31 |
| Pure FedAvg, seed 0 | T3 | 56.10 / 50.00 | 51.93 / 46.03 | 46.73 / 42.43 |

| Role | Adapter path |
|---|---|
| Centralized E3 | `artifacts/baselines/central_3ep_standard_s0/adapter` |
| Pure FL seed 0, T1–T3 | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_{1,2,3}/fedavg_adapter` |
| Pure FL seed 1, T1–T3 | `artifacts/federated/fedavg_noicl_k5_e1_t1_s1/round_{1,2,3}/fedavg_adapter` |
| Pure FL seed 2, T1 | `artifacts/federated/fedavg_noicl_k5_e1_t1_s2/round_1/fedavg_adapter` |
| FedProx seed 0, T1–T3 | `artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0/round_{1,2,3}/fedavg_adapter` |
| `alpha=0.1`, T1 | `artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1/fedavg_adapter` |
| `alpha=0.1`, T2–T3 | `artifacts/federated/p13_alpha01_k5_e1_t1_fl_s0/round_{2,3}/fedavg_adapter` |
| Gemma pure FL seed 0, T1 | `artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` |

Also still valid (not accuracy rows): deterministic LoRA communication
accounting, the Secure Sum compatibility audit, and the teacher-only Qwen 7B
Spider timing. The old student-versus-teacher resource comparison used a v1
student; rerun it with the final v2 adapter. The P2.3 terminal round adds
369,555,560 upload and 369,555,400 broadcast bytes.

## 6. Audits

| Stable ID | Artifact | Status |
|---|---|---|
| `audit.v2.spider.original` | `fedicl-sql/audits/protocol_v2/spider_original.json` | passed; nested `4ae6e35` |
| `audit.v2.bird.original` | `fedicl-sql/audits/protocol_v2/bird_original.json` | passed with evidence; compatibility release; nested `4ae6e35` |
| `audit.v2.bird.p21` | `fedicl-sql/audits/protocol_v2/p21_bird_qwen15b_integrity_t60_s0/` | scorer accepted; trained arms rejected; nested `e9bde43` |

P2.1q found 974/9,428 truncated train prompts; 754 lost all evidence. Those
checkpoints are rejected. Details:
[`BIRD_BASELINE_AUDIT.md`](../archive/results_reviews_2026-09/BIRD_BASELINE_AUDIT.md).

## 7. Never use

- Any protocol-v1 FedLS, SeqKD, public-gold, reverse-KL, mixed pre-server, or
  BIRD-trained result. Their prompts left out BIRD evidence, or they inherit
  such a server update.
- P2.1 trained arms (`max_len=2560`, truncated context).
- A `round_N/fedavg_adapter` inside an old FedLS root. Later rounds inherit the
  invalid public update.
- The retired 5,319-row `SeqKD + Hinton` hybrid and its partial cache.
- GKD partial artifacts (stopped for cost before publication).
