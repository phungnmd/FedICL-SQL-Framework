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
| `qwen.seqkd.random256.t1.s0` | P0.9b matched random control | `artifacts/federated/p09b_qwen_random256_seqkd_noicl_k5_e1_t1_s0/round_1/m_g` | 256 teacher targets, 16 optimizer updates |
| `qwen.seqkd.globalerror256.t1.s0` | P0.9b negative selector | `artifacts/federated/p09b_qwen_global_error256_seqkd_noicl_k5_e1_t1_s0/round_1/m_g` | failed promotion gate; not a paper component |

Canonical matched evaluation:
`fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954/`
(`git_sha=b3fd32f`, result commit `7c1414b`).

## 3. Second-family checkpoints and reserved IDs

Completed rows identify canonical artifacts; pending rows reserve presentation
semantics only.

| Stable ID | Student family | Paper role | Canonical checkpoint/output | Status |
|---|---|---|---|---|
| `gemma.base.s0` | Gemma 2 2B | untouched pretrained anchor | `google/gemma-2-2b-it`, no adapter | canonical; reported eval SHA `e144d8b` |
| `gemma.fl.t1.s0` | Gemma 2 2B | second-family pure FL | `artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0/round_1/fedavg_adapter` | canonical; train code SHA `45d5995` |
| `gemma.goldce.t1.s0` | Gemma 2 2B | gold CE on Gemma-selected rows | `artifacts/federated/gemma2_9b_selected_goldce_noicl_k5_e1_t1_s0/round_1/m_g` | canonical; nested result commit `e53bfe7` |
| `gemma.seqkd.t1.s0` | Gemma 2 2B | Gemma 2 9B teacher-target CE | `artifacts/federated/gemma2_9b_to_2b_seqkd_noicl_k5_e1_t1_s0/round_1/m_g` | canonical; nested result commit `e53bfe7` |
| `gemma.fedls.t1.s0` | Gemma 2 2B | Gemma 2 9B target CE + reverse KL | `artifacts/federated/gemma2_9b_to_2b_fedls_noicl_k5_e1_t1_s0/round_1/m_g` | canonical; nested result commit `e53bfe7` |

Gemma targets and logits must be regenerated with `google/gemma-2-9b-it` and
must never reuse Qwen artifacts. `gemma.fedls.t1.s0` becomes eligible only after
the exact Gemma 9B/2B token-to-ID compatibility check passes. Its public pool
must be derived by generating all 9,428 BIRD training rows and independently
applying the fixed 8-second quick-execution filter followed by the official EX
stage. Qwen's 3,873 selected indices are invalid inputs to this track. P0.7b
uses the immutable `gemma2_9b_targets_smoke8_fullsource` target root and matching
`gemma2_9b_to_2b_smoke8_fullsource_k0` cache root.

## 4. Canonical evaluation and audit artifacts

| Evaluation ID | Scope | Committed result directory | Status |
|---|---|---|---|
| `eval.qwen.t1.matched.s0.spider` | four-arm matched T1 ladder | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T065954` | canonical |
| `eval.qwen.central.recipe.s0.spider` | standard continuous vs restart schedule | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T132026` | canonical |
| `eval.qwen.central.standard.s0.realistic` | official centralized Realistic cell | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T143356` | canonical; result commit `7eb7d44` |
| `eval.qwen.central.standard.s0.syn` | official centralized Syn cell | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T144343` | canonical; result commit `7eb7d44` |
| `eval.qwen.central.standard.s0.dk` | official centralized DK cell | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T144700` | canonical; result commit `7eb7d44` |
| `eval.qwen.central.standard.s0.bird` | official centralized BIRD diagnostic | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260820T150048` | canonical; result commit `7eb7d44` |
| `eval.gemma.base.s0.spider` | untouched Gemma 2B, 1,034 Spider rows | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260821T183818` | canonical; reported SHA `e144d8b`, result commit `c760523` |
| `eval.gemma.fl.t1.s0.spider` | Gemma 2B pure FL T1, 1,034 Spider rows | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260821T183420` | canonical; pre-`--model-4bit` runner schema, result commit `c760523` |
| `eval.gemma.t1.matched.s0.spider` | base/FL/gold CE/teacher-target CE/full FedLS, 1,034 paired Spider rows | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260823T005329` | canonical paper evaluation; code SHA `3e673ef`, result commit `e53bfe7` |
| `eval.qwen.t1.p09b.s0.spider` | FL/full-uniform/random256/global-error256 method gate, 1,034 paired Spider rows | `fedicl-sql/experiments/eval_arms/results/eval_arms__s0__20260824T042237` | canonical negative ablation; code SHA `a45f683`, result commit `10a0bbd` |
| `audit.bird.train.gold.t60` | all 9,428 BIRD train gold SQL, read-only 60-second execution | `fedicl-sql/processed_data/BIRD/gold_exec_audit_t60/` | canonical; nested commit `3e673ef` |
| `audit.teacher.qwen-gemma.commonmask` | Qwen/Gemma selectors projected onto 9,056 valid-gold rows | `fedicl-sql/audits/bird_train_gold_exec_t60_teacher_comparison.json` | canonical; nested commit `3e673ef` |

The FL eval config predates the opt-in `--model-4bit` field while its metrics
report repository SHA `e144d8b`, showing that the worktree changed before
artifact finalization. This does not change the result: the old runner and the
new runner with `model_4bit=false` both load Gemma in the same default
full-precision path, and the e144d8b eval change only added the opt-in 4-bit
loader/fingerprint. Treat the metrics SHA as end-of-run repository state, not
exact process-code provenance for this one artifact.

Closed P0.10 artifacts are intentionally excluded from this canonical registry.
Compact evidence and the Git recovery tag are documented in
`fedicl-sql/experiments/archive/p010_feddf_2026-08/`.

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
