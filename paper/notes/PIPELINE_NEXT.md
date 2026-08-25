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
| P1.1a | Add fixed warm-up, process metrics, and observed-contention auditing | complete: final code `0d0faa5`, 13 targeted tests plus full 319-test suite |
| P1.2 | Audit EX gains, execution-error transitions, and representative transfer cases | complete: artifact `4527a76` |
| P1.4a | Deterministic adapter/communication/table manifest | **active CPU command below; implementation `62cd3f6`** |
| P1.4b | Related-work matrix and manuscript skeleton | next CPU/writing task after P1.4a |
| P1.1b | Benchmark Qwen student 1.5B versus teacher 7B sequentially on one contention-audited GPU | first queued GPU task; temporarily unavailable |
| P0.8 | Final T3 pure-FL versus frozen FedLS-SQL at seeds 1/2 | mandatory second GPU task after the short resource block |
| P1.3 | Decide scoped RQ3 versus one validated heterogeneity sensitivity | conditional after P0.8 |
| P0.7t | Gemma 9B zero-shot Spider ceiling | optional context only |

Ordinary `eval_arms` timing is not official resource evidence because it
measures the first decode without a fixed warm-up. Use only the runner below
for P1.1b.

GPU hold rule: leave the command and immutable roots unchanged while capacity
is unavailable. Do not substitute an optional teacher ceiling, method branch,
or opportunistic timing run. Continue P1.4a/b and manuscript preparation, then
return to this exact queue when a GPU is usable.

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
6. sample GPU state throughout each repetition, print timestamped foreign-PID
   appearance/clearance transitions live, retain them as `contention_events`,
   and label the run `eligible`, `contended`, `resumed`, or `failed`;
7. report medians plus IQR and exclude observed-contended/resumed runs from the
   primary paper-facing latency table;
8. preserve raw per-repetition JSON and runtime/GPU provenance.

This is a contention-audited shared-server benchmark, not a guarantee of
hardware exclusivity. If fewer than three eligible repetitions are available,
latency remains observational; deterministic counts and precisely labeled
process-memory measurements may still be reported.

P1.1a is implemented by `experiments/resource_benchmark/run.py` and guarded by
`experiments/resource_benchmark/summarize.py`. Each complete repetition is an
atomic resumable unit. Re-running the exact command skips a terminal result or
continues missing repetitions; a fingerprint mismatch requires a new root.

## P1.1b — Qwen 1.5B versus 7B steady-state inference

**Purpose:** measure the deployment-side cost difference on the same 32 Spider
rows. The final 1.5B FedLS adapter runs in its canonical BF16 path; the 7B
teacher runs in its canonical 4-bit reference path. This is deliberately
conservative for the teacher and is not a federated-7B training comparison.

Run both models sequentially on physical GPU 0. If GPU 0 is unsuitable, do not
edit only `CUDA_VISIBLE_DEVICES`; create a separately documented GPU-1 command
with new output roots and `--gpu-index 1`.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='experiments/resource_benchmark/results/p11b_qwen15b_fedls_t3_spider32_s0_gpu0'; $T='experiments/resource_benchmark/results/p11b_qwen7b_teacher4bit_spider32_s0_gpu0'; $O='experiments/resource_benchmark/results/p11b_qwen15b_vs_7b_spider32_s0_gpu0.json'; uv run python experiments/resource_benchmark/run.py --role deployed_student --model Qwen/Qwen2.5-1.5B-Instruct --adapter artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g --test-csv processed_data/SPIDER/centralized/test.csv --schema-style full --n-eval 32 --warmup-rows 2 --repetitions 5 --minimum-eligible 3 --batch-size 4 --max-new-tokens 256 --gpu-index 0 --seed 0 --out $S; if ($LASTEXITCODE -ne 0) { throw 'P1.1b student benchmark failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$S/result.json")) { throw "Missing student terminal result: $S/result.json" }; uv run python experiments/resource_benchmark/run.py --role teacher_reference --model Qwen/Qwen2.5-Coder-7B-Instruct --model-4bit --test-csv processed_data/SPIDER/centralized/test.csv --schema-style full --n-eval 32 --warmup-rows 2 --repetitions 5 --minimum-eligible 3 --batch-size 4 --max-new-tokens 256 --gpu-index 0 --seed 0 --out $T; if ($LASTEXITCODE -ne 0) { throw 'P1.1b teacher benchmark failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$T/result.json")) { throw "Missing teacher terminal result: $T/result.json" }; uv run python experiments/resource_benchmark/summarize.py --student "$S/result.json" --teacher "$T/result.json" --minimum-eligible 3 --out $O; if ($LASTEXITCODE -ne 0) { throw 'P1.1b comparison summary failed' }; if (-not (Test-Path -LiteralPath $O)) { throw "Missing P1.1b comparison: $O" }; $V=Get-Content -LiteralPath $O -Raw | ConvertFrom-Json; if ($V.paper_latency_comparison_eligible) { Write-Host "P1.1b complete: teacher/student latency ratio=$($V.teacher_over_student_latency_ratio)" } else { Write-Warning 'P1.1b completed but has fewer than three clean repetitions for one or both models; retain as observational and review contention before scheduling a fresh-root retry' }
```

Do not run the two roles in parallel or reuse opportunistic P0.x timing values.

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
