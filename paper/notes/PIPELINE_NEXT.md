# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every executable
> command added here must follow `CONVENTION.MD` §6.1: one physical line,
> fail-fast, immutable output roots, and exact-command resume safety.
> The ordered paper backlog and decision gates live in `PAPER_TODO.md`; this
> file contains only runnable or exactly preserved deferred commands.

For a short purpose/CPU/GPU/readiness view, see `PAPER_NEXT_TASKS.md`.

## Canonical baseline and innovation gate

The evidence-backed method is held fixed as the canonical fallback and matched
baseline after the P0.10e decision gate:

```text
private client LoRA CE -> sample-weighted factor-wise FedAvg
                       -> verified LLM-target CE + auxiliary reverse KL
```

Execution-verified hard teacher targets are the supported portable mechanism.
Reverse KL remains auxiliary because its independent increment is not stable
across training seeds or the Gemma family.

This fixed reference prevents silent baseline drift; it does **not** prohibit new
KD/Federated proposals. A substantively different mechanism may enter P1.7 if
it satisfies all of the following before a training command is added:

1. targets a documented EX failure, federated limitation, or novelty gap;
2. explains why it differs from the failed P0.9 selector and P0.10 FedDF
   implementations rather than retuning them;
3. preserves or explicitly revises the client-data, communication, teacher,
   and SLM-deployment boundaries;
4. defines a matched control, fixed budget, promotion metric, and stop rule;
5. starts with the cheapest diagnostic/smoke and reaches the full pool only
   after passing its preregistered gate.

A strong P1.7 proposal may be promoted ahead of a lower-value queued run after
the expected paper contribution and compute cost are documented. The
canonical method changes only after a positive full-scale matched result;
otherwise the branch is archived without tuning.

The execution-guided selector and client-ensemble distillation branches are closed:

- P0.9b global-error selection loses `2.03` Spider EX to its matched random
  control and adds 18 execution errors.
- P0.10 failed its frozen full-pool EX and execution-validity gate after a
  positive small screen. Do not tune or continue it. Exact commands and provenance are archived at
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`.
- P1.7a failed its fixed 512-row EX gate: preference KD scored 54.93 EX versus
  56.87 for matched positive-only CE (`-1.93` points).
  Its command and implementation are closed without tuning; compact evidence
  is archived at `paper/archive/closed_method_branches/P017A_PREFERENCE_KD_2026-08-28.md`.

## Active order

| Order   | Task                                                                           | Status / decision                                                                                         |
| ------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| P1.1a   | Add fixed warm-up, process metrics, and repeated GPU telemetry                 | complete: final protocol code `487b3b2`, full 320-test suite                                              |
| P1.2    | Audit EX gains, execution-error transitions, and representative transfer cases | complete: artifact `4527a76`                                                                              |
| P1.4a   | Deterministic adapter/communication/table manifest                             | complete: producer `f59a040`, artifact commit `147f455`, registry ID `audit.paper.tables.qwen.s0`         |
| P1.4b   | Related-work matrix and manuscript skeleton                                    | complete: title narrowed; canonical outputs `RELATED_WORK_NOVELTY_MATRIX.md` and `MANUSCRIPT_SKELETON.md` |
| P0.8a   | Final T3 pure-FL versus frozen FedLS-SQL at seed 1                             | complete: 61.99 vs 65.76 EX (`+3.77`, paired `p=0.00483`)                                                 |
| P0.8a-E | Complete the missing seed-1 T2/T3 trajectory observations                      | complete: result commit `dbd703b`, registered full seed-1 trajectory                                      |
| P2.1    | Method prose and architecture/privacy-boundary figure                          | complete: paper-ready draft and verified SVG under `paper/drafts/`                                        |
| P1.7a   | Execution-verified preference/contrastive KD                                   | closed negative: 54.93 vs 56.87 EX; exact artifacts archived at nested `74f0a43`                          |
| P1.1b   | Qwen student 1.5B versus teacher 7B resource benchmark                         | complete: 5/5 eligible each; student `2.09x` faster and uses `48.73%` less allocated VRAM                 |
| P1.8    | Optional Secure Sum compatibility and overhead audit                           | complete: real 18.46M-parameter replay passed; result `6c67e79`                                            |
| P1.5    | Matched FedProx-LoRA reviewer baseline                                         | **active design; accuracy runs use explicit plaintext aggregation**                                        |
| P2.2    | Assemble paper tables and figures from closed evidence                         | active parallel CPU lane; include the separate P1.8 compatibility/overhead row                            |
| P1.3    | One audited stronger-skew sensitivity                                          | gated after P1.5; preserve `K=5`/source rows and screen T1 before T3                                      |
| P0.8b   | Final T3 pure-FL versus frozen FedLS-SQL at seed 2                             | blocked only by legacy setup compatibility under current code; not by Secure Sum                           |
| P1.6    | Federated-7B feasibility/claim gate                                            | default excluded after P1.1b; reopen only if the manuscript retains a direct federated-7B claim           |
| P0.7t   | Gemma 9B zero-shot Spider ceiling                                              | optional context only                                                                                     |

Ordinary `eval_arms` timing is not official resource evidence because it
measures the first decode without a fixed warm-up. Use only the runner below
for P1.1b.

The first P1.1b collection used a superseded PID-presence rule and produced
zero eligible rows under Windows/WDDM. Retain it as observational provenance;
do not merge it with the revised independent-repetition protocol.

P1.1b-v2 is complete and closes the scoped deployment-inference component of
the advisor's scientific question. It does not establish training-resource or
federated-7B superiority. P0.8b is independent of Secure Sum but its old
`setup.json` predates the aggregation-protocol fingerprint, so the continuation
command remains blocked until a tested legacy-plaintext migration exists.

P1.4b, P1.1b, P2.1, and the scoped P1.8 compatibility audit are closed. The
next method task is matched FedProx-LoRA, followed by one stronger-skew screen.
Accuracy experiments use explicit plaintext weighted aggregation for matched
lineage; Secure Sum is an optional audited layer, not an accuracy gate. Decide
federated-7B feasibility only if the manuscript retains an empirical
large-model-FL comparison.

P1.7a is closed. Its fixed global-SLM preference loss reduced Spider EX by
1.93 points versus positive-only CE, so no full-pool extension,
coefficient sweep, pair filtering, or related command remains active. The
canonical verified-target CE plus auxiliary RKL method is unchanged. A future
method proposal must begin from a new evidence-backed hypothesis rather than
retuning P1.7a.

## P1.8 — optional Secure Sum compatibility audit — complete

**Purpose:** show that FedLS-SQL's weighted LoRA aggregation can be wrapped by
a pairwise-masked Secure Sum layer without changing its numerical objective,
and quantify the added cost separately from accuracy experiments.

The implementation at `3c21b96` passed the core and dropout/equivalence tests.
The real Qwen five-client replay at result commit `6c67e79` covered 18,464,768
adapter parameters and passed with maximum error `3.7253e-9`, mean error
`1.4493e-10`, and cosine `0.9999999999999983`. It took `7.1147 s`; float64
masked uploads increased comparable round communication by approximately
`49.93%`, while protocol metadata was only `1,401` bytes.

This closes a compatibility and overhead claim, not a formal cryptographic or
DP claim. Do not relabel historical accuracy lineages as Secure-Sum-produced,
and do not replay every retained round. Standard matched accuracy experiments
use `--aggregation-protocol plaintext`; a dedicated privacy-layer audit must
opt in with `--aggregation-protocol secure_sum`. The default-policy change is
nested commit `fc7899a`. Exact command and provenance:
`paper/archive/completed_runbooks/P1_8A_SECURE_SUM_COMPATIBILITY_2026-08-29.md`.

## P1.5 — matched FedProx-LoRA baseline — active design

**Purpose:** answer the reviewer objection that the headline comparison uses
only FedAvg-based federated optimization. P1.5 is a baseline, not a FedLS-SQL
component or a proposed optimizer contribution.

The design must freeze all of the following before any command is added:

1. the FedProx client objective over trainable LoRA parameters, referenced to
   the broadcast adapter at the start of each client/round;
2. a proximal-coefficient rule that does not inspect Spider test EX;
3. the same Qwen student, `K=5`, `alpha=0.5` split, LoRA rank, client rows,
   local epoch, optimizer budget, three rounds, seed 0, and evaluation protocol
   as the independent pure-FL headline lineage;
4. no public teacher stage in the FedProx-only baseline, so it tests whether a
   stronger federated optimizer alone closes the FedLS-SQL accuracy gap;
5. exact-resume fingerprints, unit tests for the proximal term/reference, and
   a smoke run before the production PowerShell line;
6. one production run only, followed by Spider EX/execution-error comparison
   with pure FL, centralized-standard, and FedLS-SQL.

Do not add a coefficient sweep, tune on Spider test, combine FedProx with a new
KD objective, or start P1.3 before this design gate is resolved.

## P0.8a-E — complete

The exact command and acceptance record are archived at
`paper/archive/completed_runbooks/P0.8A_E_SEED1_TRAJECTORY_2026-08-26.md`.
Canonical result commit: `dbd703b`. Do not rerun or launch seed 2
automatically.

## P0.8b — blocked pending legacy plaintext setup compatibility

**Purpose when reactivated:** close the three-training-seed reliability result after seed 1
replicated the final FedLS-SQL gain (`+3.77` Spider EX, `p=0.00483`). Seed 2
already has canonical T1 checkpoints. This command extends those exact
lineages through rounds 2 and 3 and evaluates only the final Spider endpoints;
it does not retrain round 1.

The block below is retained only for lineage and resume-contract audit. **Do
not run it under current code:** the old roots predate the aggregation-protocol
field now included in `setup.json`. Reactivate it only after a tested migration
treats the missing legacy field as explicit plaintext while preserving setup
identities (`8b02d882...` and `99aa70ed...`). Secure Sum is not required for
this accuracy continuation. Do not restart round 1 or change scientific flags.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=2; $F='artifacts/federated/fedavg_noicl_k5_e1_t1_s2'; $K='artifacts/federated/fedkd_noicl_k5_e1_t1_s2'; $E='artifacts/eval_resume/fedls_final_t3_spider_s2/eval_k0'; foreach ($P in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json',"$F/setup.json","$F/manifest.json","$F/round_1/fedavg_adapter/adapter_config.json","$K/setup.json","$K/manifest.json","$K/round_1/m_g/adapter_config.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.8b input or canonical T1 artifact: $P" } }; $FS=Get-Content -LiteralPath "$F/setup.json" -Raw | ConvertFrom-Json; $KS=Get-Content -LiteralPath "$K/setup.json" -Raw | ConvertFrom-Json; if ($FS.setup_id -ne '8b02d882fc9f3d4b1053959a189731d4d59969d430a1032a90e71f56520e4447') { throw "Unexpected pure-FL seed-2 setup identity: $($FS.setup_id)" }; if ($KS.setup_id -ne '99aa70edb94e06feff864ed5cfea6516e934e79314a60d11a38bac3f8ceb9ef3') { throw "Unexpected FedLS seed-2 setup identity: $($KS.setup_id)" }; foreach ($N in @(2,3)) { $P=$N-1; $I="$F/round_${P}/fedavg_adapter"; uv run python experiments/federated/run.py round --arm fedavg --round $N --init-adapter $I --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --seed $S --stage poc --out $F; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed 2 round $N failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$F/round_${N}/fedavg_adapter/adapter_config.json")) { throw "Incomplete pure-FL seed 2 round $N" } }; foreach ($N in @(2,3)) { $P=$N-1; $I="$K/round_${P}/m_g"; uv run python experiments/federated/run.py round --arm fedkd --round $N --init-adapter $I --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1.0 --lambda-kd 1.0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --seed $S --stage poc --out $K; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed 2 round $N failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$K/round_${N}/m_g/adapter_config.json")) { throw "Incomplete FedLS-SQL seed 2 round $N" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s2_t3=$F/round_3/fedavg_adapter" "fedls_s2_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.8b final Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P0.8b evaluation manifest directory: $E/manifests" }; Write-Host 'P0.8b complete: seed-2 pure FL and FedLS-SQL T3 evaluated; push compact results and stop for three-seed analysis'
```

After completion, push only compact federated results and evaluation
metrics/configs/predictions/manifests. Stop for paired validation and the
three-seed mean/sample-SD calculation; do not launch an OOD seed sweep.

Completed P0.8a command provenance is archived at
`paper/archive/completed_runbooks/P0.8A_SEED1_T3_2026-08-26.md`.

## P1.4a — complete

The exact command, failure history, split-lineage handling, and acceptance
record are archived at
`paper/archive/completed_runbooks/P1.4A_COMMUNICATION_2026-08-26.md`. Do not
rerun unless an audited source artifact changes and a new immutable output is
explicitly required.

## P1.1 acceptance contract

The benchmark implementation must:

1. warm up each loaded model in-process on deterministic non-reported inputs;
2. synchronize CUDA immediately before and after every timed region;
3. separate model loading, warm-up, generation, and SQL scoring time;
4. report fresh-run latency/throughput, peak allocated and reserved VRAM, and
   process RSS for at least five repetitions;
5. compare identical rows and decoding, declare precision/quantization and
   batch size, and run student/teacher sequentially on the same selected GPU;
6. sample device utilization, memory, clocks, and pstate throughout each
   repetition without enumerating PIDs; telemetry is descriptive;
7. label every fresh successful repetition `eligible`, report medians plus IQR,
   and exclude only failed or resumed rows from the primary latency table;
8. preserve raw per-repetition JSON and runtime/GPU provenance.

This is a repeated shared-server benchmark, not a guarantee of hardware
exclusivity. The operator selects a time with no intentionally concurrent GPU
job. Repetitions are analyzed independently; PID presence is neither sampled
nor used as an exclusion rule.

P1.1a is implemented by `experiments/resource_benchmark/run.py` and guarded by
`experiments/resource_benchmark/summarize.py`. Each complete repetition is an
atomic resumable unit. Re-running the exact command skips a terminal result or
continues missing repetitions; a fingerprint mismatch requires a new root.

## P1.1b — Qwen 1.5B versus 7B steady-state inference — complete

**Status:** complete; canonical comparison fingerprint
`60665e60a63ae93c1871401d01a9094caa0e82454f79bf1be473085d794c13c9`.

**Purpose:** measure the deployment-side cost difference on the same 32 Spider
rows. The final 1.5B FedLS adapter runs in its canonical BF16 path; the 7B
teacher runs in its canonical 4-bit reference path. This is deliberately
conservative for the teacher and is not a federated-7B training comparison.

Both models completed 5/5 eligible fresh repetitions on identical 32-row
Spider inputs. Median latency was 0.7873 s/query for the BF16 FedLS-SQL student
and 1.6460 s/query for the 4-bit teacher (`2.09x`); peak allocated VRAM was
3,474.6 versus 6,776.8 MB. Exact commands, protocol, output roots, dispersion,
and claim limits are archived at
`paper/archive/completed_runbooks/P1_1B_RESOURCE_BENCHMARK_2026-08-28.md`.
Do not rerun unless the deployment claim, hardware, model precision, or
protocol changes and a new immutable comparison is explicitly required.

## Deferred command provenance

Completed and superseded commands are not duplicated in this active file:

- P0.0–P0.10e snapshot:
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`;
- pre-FedLS/ICL runbooks: `paper/archive/pre_fedls_2026-08/legacy_runbooks/`;
- immutable checkpoint and evaluation mappings: `paper/notes/RESULT_REGISTRY.md`.

## After a completed block

1. Commit only metrics, configs, predictions, manifests, and compact audits;
   never commit model weights or resume checkpoints.
2. Pull and validate row counts, fingerprints, paired EX/EM, and execution
   errors before changing the queue.
3. Update `RESULT_REGISTRY.md`, `paper/results/MAIN_RESULTS.md`, `LAB_LOG.md`,
   `EXPERIMENT_MATRIX.md`, and `PAPER_EVIDENCE_PLAN.md` once per decision gate.
4. Archive closed commands instead of leaving them in the active queue.
