# FedLS-SQL artifact registry

This file maps stable paper result IDs to immutable checkpoints and evaluation
artifacts. Paper-facing metric values live only in
`../results/MAIN_RESULTS.md`; interpretation lives in `LAB_LOG.md`.

Presentation labels may change. Stable IDs and historical artifact paths must
not be renamed.

## 1. Primary Qwen2.5 checkpoints

| Stable ID | Paper role | Canonical checkpoint | Lineage status |
|---|---|---|---|
| `qwen.central.standard3.s0` | official centralized SLM | `artifacts/baselines/central_3ep_standard_s0/adapter` | one continuous three-epoch schedule |
| `qwen.central.restart3.s0` | schedule sensitivity only | `artifacts/probe_p/central_3ep/adapter` | three independently scheduled passes |
| `qwen.fl.t3.s0` | final independent pure FL | `artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter` | setup `229fe736042acd80df29a19e577963e4f69a5e6bb62d41ac5964fbeee9f629d2` |
| `qwen.fedls.t3.s0` | final full FedLS-SQL | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g` | teacher-target CE + reverse KL |

The `round_2/round_3/fedavg_adapter` objects inside the FedLS lineage inherit
earlier KD and are not independent pure-FL checkpoints.

## 2. Matched Qwen2.5 T1 checkpoints

All four rows start from the same seed-0 T1 client training and factor-wise
FedAvg adapter. Only the server treatment differs.

| Stable ID | Paper role | Canonical checkpoint | Server treatment |
|---|---|---|---|
| `qwen.fl.shared.t1.s0` | shared FL starting point | `artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` | none |
| `qwen.goldce.t1.s0` | matched public-supervision control | `artifacts/federated/fedavg_pub_gold_noicl_k5_e1_t1_s0/round_1/m_g` | BIRD-gold CE on the exact retained rows |
| `qwen.seqkd.t1.s0` | hard-target transfer ablation | `artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g` | teacher-target CE |
| `qwen.fedls.t1.s0` | full T1 endpoint | `artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g` | teacher-target CE + reverse KL |

Canonical matched evaluation:
`fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954/`
(`git_sha=b3fd32f`, result commit `7c1414b`).

## 3. Cross-family reserved IDs

These IDs reserve presentation semantics; they do not assert that an artifact
already exists.

| Stable ID | Student family | Paper role | Expected output root | Status |
|---|---|---|---|---|
| `gemma.fl.t1.s0` | Gemma 2 | cross-family pure FL | assign when P0.8 command is frozen | `PENDING:P0.8` |
| `gemma.seqkd.t1.s0` | Gemma 2 | cross-family teacher-target CE | assign when P0.8 command is frozen | `PENDING:P0.8` |

`gemma.seqkd.t1.s0` must not be labeled full FedLS-SQL CE+RKL. Qwen teacher
logits are not reusable across the Gemma tokenizer.

## 4. Canonical evaluation artifacts

| Evaluation ID | Scope | Committed result directory | Status |
|---|---|---|---|
| `eval.qwen.t1.matched.s0.spider` | four-arm matched T1 ladder | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954` | canonical |
| `eval.qwen.central.recipe.s0.spider` | standard continuous vs restart schedule | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T132026` | canonical |
| `eval.qwen.central.standard.s0.realistic` | official centralized Realistic cell | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T143356` | canonical; result commit `7eb7d44` |
| `eval.qwen.central.standard.s0.syn` | official centralized Syn cell | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T144343` | canonical; result commit `7eb7d44` |
| `eval.qwen.central.standard.s0.dk` | official centralized DK cell | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T144700` | canonical; result commit `7eb7d44` |
| `eval.qwen.central.standard.s0.bird` | official centralized BIRD diagnostic | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T150048` | canonical; result commit `7eb7d44` |

## 5. Registry rules

- `MAIN_RESULTS.md` owns published values; do not add a second metric table
  here.
- Every new model family receives a separate stable-ID namespace.
- Include student family/model, teacher family/model, transfer objective,
  round, training seed, checkpoint, evaluation directory, and Git SHA before a
  row becomes canonical.
- `PENDING` rows may reserve IDs but may not contain guessed metrics or paths.
- BIRD dev is cross-corpus transfer, not a headline in-domain benchmark.
- Old path tokens such as `fedkd`, `noicl`, and `fedicl` are provenance and must
  remain unchanged.
