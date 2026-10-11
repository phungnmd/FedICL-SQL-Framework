# Experiment fact sheet (numbers only)

Project: federated NL-to-SQL with a small student model (SLM), private clients, and a
server that holds a public dataset and a frozen larger teacher model (LLM). Target venue:
a Q3 journal. All results are seed 0 unless noted. Paired tests are exact McNemar on
identical evaluation questions.

## Setup

- Private data: Spider train (8,659 rows), split over 5 clients, non-IID Dirichlet
  alpha = 0.5 over schema-embedding domain clusters. Data never leaves a client.
- Public data (server only): BIRD train, 9,428 rows, with BIRD evidence in the prompt.
- Teacher: Qwen2.5-Coder-7B-Instruct, frozen, 4-bit, zero-shot. Never deployed.
- Students: Qwen2.5-1.5B-Instruct (older runs) and Qwen2.5-Coder-0.5B-Instruct (newest
  runs). LoRA r = 16. Only the student is deployed.
- Aggregation: sample-weighted FedAvg of LoRA factors, plaintext. No ICL anywhere.
- Evaluation: execution accuracy (EX, primary) and exact match (EM). Sets: Spider dev
  (1,034), Spider-Realistic (508), Spider-Syn (1,034), Spider-DK (535), BIRD dev (1,534,
  EX only).

Notation for a training chain, read left to right:

- `A`: one federated round (each client 1 local epoch on its Spider shard, then FedAvg).
- `K`: one server epoch on the public BIRD pool, starting from the current global adapter.
  `K2`: two epochs in one continuous optimizer/LR schedule. Each separate `K` restarts the
  optimizer and schedule.
- Server objectives: `gold` = cross-entropy on BIRD gold SQL; `hinton` = 0.5 CE on gold
  + 0.5 forward KL to the teacher's token distribution (T = 2, Hinton et al. 2015);
  `seq` = CE on teacher-generated SQL that executes correctly (sequence-level KD);
  `kid`, `gkd` = other on-policy KD variants; `plan` = auxiliary task predicting a
  teacher-written query plan next to SQL CE.
- `centralized_eN`: one model trained on the whole Spider train set for N epochs
  (no BIRD, no teacher).
- Teacher zero-shot (1.5B-era evaluation): Spider 76.69, Realistic 71.06, Syn 63.83,
  DK 62.43, BIRD 47.07.

## A. Newest screen: Qwen2.5-Coder-0.5B student (P2.18), seed 0

Every arm below has exactly 3 private Spider passes (3 x A, or 3 centralized epochs).
KD arms also have 2 BIRD epochs. `akkaa` = A, K2, A, A.

Final EX (%), Spider EM (%):

| Arm | Spider EX | Spider EM | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|---:|
| centralized_e3 | 59.38 | 58.12 | 45.87 | 43.42 | 44.30 | 13.62 |
| fl_aaa | 57.54 | 52.03 | 47.24 | 41.49 | 42.80 | 14.34 |
| gold_akaka | 60.15 | 54.64 | 50.98 | 48.16 | 46.54 | 25.75 |
| hinton_akaka | 62.57 | 57.54 | 52.17 | 50.48 | 47.85 | 28.88 |
| gold_akkaa | 61.80 | 55.90 | 52.17 | 48.65 | 46.17 | 26.60 |
| hinton_akkaa | 63.15 | 56.96 | 51.77 | 49.71 | 47.48 | 27.77 |
| hinton_k2aaa (K2 first, then A, A, A) | 63.9 | 58.6 | not yet | not yet | not yet | not yet |

`hinton_k2aaa` comes from a server log and has not passed the evidence/publication check.
Its K2 stage was interrupted once and resumed from a checkpoint. Still running:
`gold_k2aaa`, `fedprox_aaa` (FedProx mu = 0.01).

Centralized E1/E2/E3 Spider: 58.03 / 60.35 / 59.38.

Spider EX after every stage (A1 is shared by all KD arms):

| Arm | Stages | Spider EX |
|---|---|---|
| fl_aaa | A1, A2, A3 | 53.38, 55.51, 57.54 |
| gold_akaka | A1, K, A, K, A | 53.38, 46.42, 59.77, 48.36, 60.15 |
| hinton_akaka | A1, K, A, K, A | 53.38, 50.58, 60.74, 53.09, 62.57 |
| gold_akkaa | A1, K2, A, A | 53.38, 48.07, 58.99, 61.80 |
| hinton_akkaa | A1, K2, A, A | 53.38, 52.42, 60.54, 63.15 |

BIRD EX right after K stages: gold_akaka K1/K2 29.07/31.16; hinton_akaka 30.96/35.53;
gold_akkaa K2 31.62; hinton_akkaa K2 35.33.

Full paired table: `raw/p218_coder05b_summary.md` (65 contrasts, all five sets).
Key Spider contrasts: hinton_akaka - gold_akaka +2.42 (66/41, p = .0199);
hinton_akkaa - gold_akkaa +1.35 (56/42, p = .189); hinton_akkaa - hinton_akaka
+0.58 (p = .581); gold_akkaa - gold_akaka +1.64 (p = .100); fl - centralized -1.84
(p = .166); hinton_akaka - fl +5.03 (p = 2e-5).

## B. Older screens: Qwen2.5-1.5B-Instruct student, seed 0

Five-set EX (%). Hinton rows before P2.17 used a bf16 full-vocabulary loss; later rows use
an fp32 loss on the response window only; a loss-mode check gave Spider -0.68 (p = .26).

| Chain | Spider | Realistic | Syn | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| centralized_e3 (Spider only) | 67.31 | 55.91 | 54.06 | 53.27 | 17.73 |
| A | 57.35 | 54.92 | 49.32 | 45.23 | 14.80 |
| A>A | 62.57 | 55.31 | 52.22 | 47.10 | 16.49 |
| A>A>A | 64.22 | 57.28 | 52.32 | 47.85 | 17.60 |
| A>A>A>A | 64.80 | 56.30 | 52.03 | 50.09 | 17.67 |
| A>K[hinton] | 58.32 | 42.72 | 44.58 | 45.42 | 36.70 |
| A>K[gold] | 55.03 | 47.05 | 43.91 | 40.93 | 32.14 |
| A>K[hinton]>A | 66.63 | 57.09 | 55.32 | 50.65 | 31.03 |
| A>K[gold]>A | 66.54 | 57.28 | 54.45 | 51.21 | 29.53 |
| A>K[gold]>A (fp32 rerun) | 65.86 | 57.68 | 53.48 | 51.21 | 29.53 |
| A>K[gold]>A>A | 67.89 | 60.83 | 56.38 | 50.84 | 30.05 |
| A>K[hinton]>A>A | 67.60 | 56.89 | 55.61 | 52.90 | 30.90 |
| A>K[gold]>A>A>A | 68.09 | 58.46 | 55.32 | 53.08 | 29.20 |
| A>K[hinton]>A>A>A | 67.79 | 59.06 | 55.03 | 53.46 | 31.81 |
| A>K[gold]>A>K[gold] | 58.03 | 50.00 | 46.62 | 43.74 | 33.57 |
| A>K[hinton]>A>K[hinton] | 62.67 | 49.21 | 50.58 | 49.16 | 39.31 |
| A>K[gold]>A>K[gold]>A | 67.50 | 58.07 | 55.42 | 50.65 | 31.62 |
| A>K[hinton]>A>K[hinton]>A | 69.54 | 59.45 | 57.93 | 54.39 | 36.18 |
| A>K[seq] (5,319 rows) | 57.93 | 46.65 | 48.26 | 45.61 | 34.68 |
| A>K[gold] same 5,319 rows | 56.29 | 43.90 | 44.87 | 43.18 | 31.68 |
| A>K[seq]>A | 64.99 | 57.68 | 54.55 | 50.28 | 28.42 |
| A>K[gold]>A same 5,319 rows | 65.09 | 58.66 | 52.90 | 49.53 | 27.51 |
| A>K[kid]>A | 65.47 | 57.09 | 54.16 | 50.28 | 28.94 |
| A>K[gold+plan]>A | 64.89 | 59.06 | 52.22 | 50.09 | 30.77 |
| A>K[seq+plan]>A (4,109 rows) | 64.89 | 56.89 | 52.71 | 50.09 | 25.62 |

Paired results recorded for the 1.5B runs:

- A>K[hinton]>A>K[hinton]>A minus the gold equivalent: Spider +2.03 (55/34, p = .033),
  Realistic +1.38 (p = .42), Syn +2.51 (p = .021), DK +3.74 (p = .002), BIRD +4.56
  (p < 1e-5).
- A>K[hinton]>A minus A>K[gold]>A: +0.09/-0.19/+0.87/-0.56/+1.50 (all p >= .10).
- Gold minus FL at equal private passes (2/3/4): Spider +3.29/+3.68/+3.29 (p <= .004).
- A>K[seq] minus same-row gold at the public endpoint: Spider +1.64 (p = .20), Syn +3.38
  (p = .006), BIRD +3.00 (p = .004); after the next A: -0.10/-0.98/+1.64/+0.75/+0.91
  (all p >= .07).
- Hinton 5-pass chain minus centralized_e3: Spider +2.22 (p = .090), BIRD +18.45.
- Reverse direction (BIRD private, Spider public), BIRD dev: FL 22.88, gold 20.73,
  seq 24.45.
- Raw paired tables: `raw/p214_*`, `raw/p215_*`, `raw/p216_*`, `raw/p217_*`.

## C. Negative or closed directions (all seed 0)

- Retention loss on the final private round (lambda = 1.0) to keep the teacher edge:
  +1.9 BIRD for -3.4 to -6.9 on every Spider-family set. Failed.
- Weight merging (WiSE-FT, task arithmetic) of KD and FL adapters: every merge lowered
  Spider. Failed.
- Teacher query-plan supervision at clients (template plans): FL model weak before KD
  (Spider 41.9 vs 57.35 SQL-only). Stopped.
- Plan as auxiliary server task: +1.84 Spider (p = .034) on a 1,000-row pool, but no gain
  on the full pool (goldplan - gold at A>K>A: Spider -0.97, p = .31). Closed.
- KID: ties seq, about 21 GPU-hours. GKD: stopped for cost.
- In-context learning (retrieved demonstrations) in training and inference: negative,
  removed.

## D. Compute

Two RTX A5000 (24 GB). 0.5B: one A round about 1.3 h; one K epoch about 2.3 h (gold) or
2.5 h (Hinton, teacher logits cached). 1.5B: K about 2.7-3.3 h, A about 1.6 h. Teacher logit
cache and teacher generation are one-time costs.

## E. Closest prior work named by the authors (verify independently)

FedCoLLM (arXiv 2411.11707): LoRA SLM clients, server-side mutual LLM/SLM KD on auxiliary
data after each FL round. FedMKT (COLING 2025): mutual KD between server LLM and client
SLMs on public data. FedDF (NeurIPS 2020): server-side ensemble distillation on proxy data.
FedPETuning (Findings ACL 2023): federated PEFT. Nguyen et al. (ICLR 2023, "Where to
Begin?"): pre-training/initialization before FL. Hinton et al. 2015 (soft-label KD).
Struct-SQL and Distilling Step-by-Step (plan/rationale distillation).
