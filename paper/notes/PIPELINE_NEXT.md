# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every executable
> command added here must follow `CONVENTION.MD` §6.1: one physical line,
> fail-fast, immutable output roots, and exact-command resume safety.
> The ordered paper backlog and decision gates live in `PAPER_TODO.md`; this
> file contains only runnable or exactly preserved deferred commands.

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
| P1.4a | Deterministic adapter/communication/table manifest | complete: producer `f59a040`, artifact commit `147f455`, registry ID `audit.paper.tables.qwen.s0` |
| P1.4b | Related-work matrix and manuscript skeleton | complete: title narrowed; canonical outputs `RELATED_WORK_NOVELTY_MATRIX.md` and `MANUSCRIPT_SKELETON.md` |
| P0.8a | Final T3 pure-FL versus frozen FedLS-SQL at seed 1 | complete: 61.99 vs 65.76 EX (`+3.77`, paired `p=0.00483`) |
| P0.8a-E | Complete the missing seed-1 T2/T3 trajectory observations | complete: result commit `dbd703b`, registered full seed-1 trajectory |
| P0.8b | Final T3 pure-FL versus frozen FedLS-SQL at seed 2 | deferred; two positive T3 seeds are sufficient for the current direction decision |
| P1.1b | Qwen student 1.5B versus teacher 7B resource benchmark | deferred by operator; v2 command retained below, not active |
| P1.3 | Decide scoped RQ3 versus one validated heterogeneity sensitivity | mandatory claim gate after the method/figure draft; no command yet |
| P1.5 | Matched FedProx-LoRA reviewer baseline | recommended before submission; no command until design/coefficient gate is approved |
| P0.7t | Gemma 9B zero-shot Spider ceiling | optional context only |

Ordinary `eval_arms` timing is not official resource evidence because it
measures the first decode without a fixed warm-up. Use only the runner below
for P1.1b.

The first P1.1b collection used a superseded PID-presence rule and produced
zero eligible rows under Windows/WDDM. Retain it as observational provenance;
do not merge it with the revised independent-repetition protocol.

P1.1b-v2 is now explicitly deferred, not failed or cancelled. Do not launch it
until resource evidence is reactivated. P0.8a-E is complete; no GPU task is
activated automatically, and P0.8b training remains intentionally delayed.
Archived seed commands must be audited against the current checkpoint/resume
contract before being copied back here; do not run an old block blindly.

P1.4b is closed. The next active work is CPU writing: method prose and the
architecture/privacy-boundary figure from `MANUSCRIPT_SKELETON.md`. No new GPU
command is activated by that completion. After the draft exposes the exact
claim boundary, decide RQ4 measurement versus narrowing, then RQ3 scope and the
matched FedProx-LoRA baseline design.

## P0.8a-E — complete

The exact command and acceptance record are archived at
`paper/archive/completed_runbooks/P0.8A_E_SEED1_TRAJECTORY_2026-08-26.md`.
Canonical result commit: `dbd703b`. Do not rerun or launch seed 2
automatically.

## P0.8b — deferred final T3 reliability at seed 2

**Purpose when reactivated:** close the three-training-seed reliability result after seed 1
replicated the final FedLS-SQL gain (`+3.77` Spider EX, `p=0.00483`). Seed 2
already has canonical T1 checkpoints. This command extends those exact
lineages through rounds 2 and 3 and evaluates only the final Spider endpoints;
it does not retrain round 1.

This block is retained for exact future resumption but is not active. The
preflight pins seed-2 setup identities (`8b02d882...` for pure FL and
`99aa70ed...` for FedLS-SQL). Every stage is independently resumable by
rerunning this exact line. Do not replace it with `run --rounds 3`, change the
roots, or reuse the seed-1 evaluation root.

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
