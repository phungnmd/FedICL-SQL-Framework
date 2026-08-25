# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every executable
> command added here must follow `CONVENTION.MD` §6.1: one physical line,
> fail-fast, immutable output roots, and exact-command resume safety.

## Method freeze

The proposed method is frozen after the P0.10e decision gate:

```text
private client LoRA CE -> sample-weighted factor-wise FedAvg
                       -> verified LLM-target CE + auxiliary reverse KL
```

Execution-verified hard teacher targets are the supported portable mechanism.
Reverse KL remains auxiliary because its independent increment is not stable
across training seeds or the Gemma family.

The execution-guided selector and client-ensemble distillation branches are closed:

- P0.9b global-error selection loses `2.03` Spider EX to its matched random
  control and adds 18 execution errors.
- P0.10 failed its frozen full-pool EX and execution-validity gate after a
  positive small screen. Do not tune or continue it. Exact commands and provenance are archived at
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`.

## Active order

| Order | Task | Status / decision |
|---|---|---|
| P1.1a | Add fixed warm-up, process metrics, and repeated GPU telemetry | complete: final protocol code `487b3b2`, full 320-test suite |
| P1.2 | Audit EX gains, execution-error transitions, and representative transfer cases | complete: artifact `4527a76` |
| P1.4a | Deterministic adapter/communication/table manifest | **active CPU command below; implementation `62cd3f6`** |
| P1.4b | Related-work matrix and manuscript skeleton | next CPU/writing task after P1.4a |
| P0.8a | Final T3 pure-FL versus frozen FedLS-SQL at seed 1 | **active GPU command below; continue canonical T1 lineages through T2/T3** |
| P0.8b | Final T3 pure-FL versus frozen FedLS-SQL at seed 2 | gated on seed-1 endpoint remaining positive |
| P1.1b | Qwen student 1.5B versus teacher 7B resource benchmark | deferred by operator; v2 command retained below, not active |
| P1.3 | Decide scoped RQ3 versus one validated heterogeneity sensitivity | conditional after P0.8 |
| P0.7t | Gemma 9B zero-shot Spider ceiling | optional context only |

Ordinary `eval_arms` timing is not official resource evidence because it
measures the first decode without a fixed warm-up. Use only the runner below
for P1.1b.

The first P1.1b collection used a superseded PID-presence rule and produced
zero eligible rows under Windows/WDDM. Retain it as observational provenance;
do not merge it with the revised independent-repetition protocol.

P1.1b-v2 is now explicitly deferred, not failed or cancelled. Do not launch it
until resource evidence is reactivated. The current GPU priority is P0.8a.
Archived seed commands must be audited against the current checkpoint/resume
contract before being copied back here; do not run an old block blindly.

## P0.8a — final T3 reliability at seed 1

**Purpose:** test whether the final T3 FedLS-SQL improvement over independent
pure FL survives a second training seed. Seed 1 already has canonical T1
checkpoints; this command extends those exact lineages through rounds 2 and 3
and evaluates only the two final Spider endpoints. It does not retrain round 1.

The preflight pins the existing T1 setup identities (`3680b91c...` for pure
FL and `c695a493...` for FedLS-SQL). Each round is an independent resumable
stage: rerun this exact command after interruption. Completed adapters and an
exact completed evaluation manifest are reused safely. Do not replace this
with the archived `run --rounds 3` block, which would restart at round 1 and
would not preserve the established seed-1 lineage.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=1; $F='artifacts/federated/fedavg_noicl_k5_e1_t1_s1'; $K='artifacts/federated/fedkd_noicl_k5_e1_t1_s1'; $E='artifacts/eval_resume/fedls_final_t3_spider_s1/eval_k0'; foreach ($P in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json',"$F/setup.json","$F/manifest.json","$F/round_1/fedavg_adapter/adapter_config.json","$K/setup.json","$K/manifest.json","$K/round_1/m_g/adapter_config.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.8a input or canonical T1 artifact: $P" } }; $FS=Get-Content -LiteralPath "$F/setup.json" -Raw | ConvertFrom-Json; $KS=Get-Content -LiteralPath "$K/setup.json" -Raw | ConvertFrom-Json; if ($FS.setup_id -ne '3680b91c34f6631fea4cca61573f28edfe30e75a51e01bef19167e87ad13b5e1') { throw "Unexpected pure-FL seed-1 setup identity: $($FS.setup_id)" }; if ($KS.setup_id -ne 'c695a4936ed59b6609bc48909f22b94ade2375cfc061386c8b4d3847f3264994') { throw "Unexpected FedLS seed-1 setup identity: $($KS.setup_id)" }; foreach ($N in @(2,3)) { $P=$N-1; $I="$F/round_${P}/fedavg_adapter"; uv run python experiments/federated/run.py round --arm fedavg --round $N --init-adapter $I --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --seed $S --stage poc --out $F; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed 1 round $N failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$F/round_${N}/fedavg_adapter/adapter_config.json")) { throw "Incomplete pure-FL seed 1 round $N" } }; foreach ($N in @(2,3)) { $P=$N-1; $I="$K/round_${P}/m_g"; uv run python experiments/federated/run.py round --arm fedkd --round $N --init-adapter $I --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1.0 --lambda-kd 1.0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --seed $S --stage poc --out $K; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed 1 round $N failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$K/round_${N}/m_g/adapter_config.json")) { throw "Incomplete FedLS-SQL seed 1 round $N" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s1_t3=$F/round_3/fedavg_adapter" "fedls_s1_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.8a final Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P0.8a evaluation manifest directory: $E/manifests" }; Write-Host 'P0.8a complete: seed-1 pure FL and FedLS-SQL T3 evaluated; stop and review the paired EX delta before seed 2'
```

After completion, push only compact federated results and evaluation
metrics/configs/predictions/manifests. Do not launch seed 2 until the paired
seed-1 EX result and lineage have been reviewed.

## P1.4a — deterministic paper-table manifest (CPU only)

**Purpose:** fill the deterministic part of RQ4 without loading either base
model. The script reads `safetensors` headers, verifies canonical registry
paths, checks every round's client/global adapter bytes against its immutable
`factor_fedavg_meta.json`, structures all canonical result tables, and records
remaining `PENDING` cells. Pure FL and FedLS T3 adapters must have the same
tensor schema.

The output root is immutable. Re-running the exact command skips a matching
JSON/CSV pair, repairs only a missing companion CSV, and rejects any changed
input or corrupted companion output.

```powershell
$O='audits/paper_table_manifest_qwen_t3_s0.json'; $C='audits/paper_table_manifest_qwen_t3_s0.communication.csv'; uv run python scripts/build_paper_table_manifest.py --adapter 'qwen.fl.t3.s0=artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter' --adapter 'qwen.fedls.t3.s0=artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g' --federated-run 'qwen.fl.t3.s0=artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0' --federated-run 'qwen.fedls.t3.s0=artifacts/federated/fedkd_noicl_k5_e1_t1_s0' --registry ../paper/notes/RESULT_REGISTRY.md --main-results ../paper/results/MAIN_RESULTS.md --n-clients 5 --rounds 3 --out $O; if ($LASTEXITCODE -ne 0) { throw 'P1.4a deterministic manifest failed; inspect provenance drift before using a new output root' }; if (-not (Test-Path -LiteralPath $O) -or -not (Test-Path -LiteralPath $C)) { throw 'P1.4a terminal JSON/CSV pair is incomplete; rerun this exact line to repair or resume' }; $V=Get-Content -LiteralPath $O -Raw | ConvertFrom-Json; if ($V.adapters.Count -ne 2 -or $V.communication.Count -ne 2 -or -not $V.validation.adapter_tensor_schema_shared -or -not $V.validation.communication_matches_round_metadata -or -not $V.validation.no_gpu_model_loading) { throw 'P1.4a manifest validation failed' }; Write-Host "P1.4a complete: adapter_params=$($V.adapters[0].adapter_tensor_parameters) FL_T3_bytes=$($V.communication[0].cumulative.round_total) FedLS_T3_bytes=$($V.communication[1].cumulative.round_total) pending_cells=$($V.pending_cells.Count)"
```

Commit the compact JSON and CSV after validating that the communication totals
agree with §5.1 of `paper/results/MAIN_RESULTS.md`. Do not commit adapters.

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

## P1.1b — Qwen 1.5B versus 7B steady-state inference

**Purpose:** measure the deployment-side cost difference on the same 32 Spider
rows. The final 1.5B FedLS adapter runs in its canonical BF16 path; the 7B
teacher runs in its canonical 4-bit reference path. This is deliberately
conservative for the teacher and is not a federated-7B training comparison.

Run both models sequentially on physical GPU 0 while no other intentional GPU
job is running. If GPU 0 is unsuitable, do not
edit only `CUDA_VISIBLE_DEVICES`; create a separately documented GPU-1 command
with new output roots and `--gpu-index 1`.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='experiments/resource_benchmark/results/p11b_v2_qwen15b_fedls_t3_spider32_s0_independent_gpu0'; $T='experiments/resource_benchmark/results/p11b_v2_qwen7b_teacher4bit_spider32_s0_independent_gpu0'; $O='experiments/resource_benchmark/results/p11b_v2_qwen15b_vs_7b_spider32_s0_independent_gpu0.json'; uv run python experiments/resource_benchmark/run.py --role deployed_student --model Qwen/Qwen2.5-1.5B-Instruct --adapter artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g --test-csv processed_data/SPIDER/centralized/test.csv --schema-style full --n-eval 32 --warmup-rows 2 --repetitions 5 --minimum-eligible 3 --batch-size 4 --max-new-tokens 256 --gpu-index 0 --seed 0 --out $S; if ($LASTEXITCODE -ne 0) { throw 'P1.1b-v2 student benchmark failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$S/result.json")) { throw "Missing student terminal result: $S/result.json" }; uv run python experiments/resource_benchmark/run.py --role teacher_reference --model Qwen/Qwen2.5-Coder-7B-Instruct --model-4bit --test-csv processed_data/SPIDER/centralized/test.csv --schema-style full --n-eval 32 --warmup-rows 2 --repetitions 5 --minimum-eligible 3 --batch-size 4 --max-new-tokens 256 --gpu-index 0 --seed 0 --out $T; if ($LASTEXITCODE -ne 0) { throw 'P1.1b-v2 teacher benchmark failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$T/result.json")) { throw "Missing teacher terminal result: $T/result.json" }; uv run python experiments/resource_benchmark/summarize.py --student "$S/result.json" --teacher "$T/result.json" --minimum-eligible 3 --out $O; if ($LASTEXITCODE -ne 0) { throw 'P1.1b-v2 comparison summary failed' }; if (-not (Test-Path -LiteralPath $O)) { throw "Missing P1.1b-v2 comparison: $O" }; $V=Get-Content -LiteralPath $O -Raw | ConvertFrom-Json; if (-not $V.paper_latency_comparison_eligible) { throw 'P1.1b-v2 has fewer than three fresh successful repetitions for one or both models' }; Write-Host "P1.1b-v2 complete: teacher/student latency ratio=$($V.teacher_over_student_latency_ratio)"
```

Do not run the two roles in parallel, reuse the superseded PID-gated roots, or
reuse opportunistic P0.x timing values.

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
