# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every executable
> command added here must follow `CONVENTION.MD` §6.1: one physical line,
> fail-fast, immutable output roots, and exact-command resume safety.
> The ordered paper backlog and decision gates live in `PAPER_TODO.md`; this
> file contains only runnable or exactly preserved deferred commands.

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

## Active order

| Order | Task | Status / decision |
|---|---|---|
| P1.1a | Add fixed warm-up, process metrics, and repeated GPU telemetry | complete: final protocol code `487b3b2`, full 320-test suite |
| P1.2 | Audit EX gains, execution-error transitions, and representative transfer cases | complete: artifact `4527a76` |
| P1.4a | Deterministic adapter/communication/table manifest | complete: producer `f59a040`, artifact commit `147f455`, registry ID `audit.paper.tables.qwen.s0` |
| P1.4b | Related-work matrix and manuscript skeleton | complete: title narrowed; canonical outputs `RELATED_WORK_NOVELTY_MATRIX.md` and `MANUSCRIPT_SKELETON.md` |
| P0.8a | Final T3 pure-FL versus frozen FedLS-SQL at seed 1 | complete: 61.99 vs 65.76 EX (`+3.77`, paired `p=0.00483`) |
| P0.8a-E | Complete the missing seed-1 T2/T3 trajectory observations | complete: result commit `dbd703b`, registered full seed-1 trajectory |
| P2.1 | Method prose and architecture/privacy-boundary figure | active CPU/writing task; no experiment command |
| P1.7a | Execution-verified preference/contrastive KD | **implemented at code commits `bd150c5` + `d2a4d9b`; 512-row screen below is the next GPU run** |
| P1.1b | Qwen student 1.5B versus teacher 7B resource benchmark | ready and still required for RQ4, but pending behind the P1.7a screen |
| P1.5 | Matched FedProx-LoRA reviewer baseline | next experiment design; no command until implementation and coefficient gates are approved |
| P1.3 | One audited stronger-skew sensitivity | advisor-aligned RQ3 design; preserve `K=5`/source rows and screen T1 before T3 |
| P0.8b | Final T3 pure-FL versus frozen FedLS-SQL at seed 2 | deferred; two positive T3 seeds are sufficient for the current direction decision |
| P1.6 | Federated-7B feasibility/claim gate | conditional after P1.1b; no command and no empirical claim yet |
| P0.7t | Gemma 9B zero-shot Spider ceiling | optional context only |

Ordinary `eval_arms` timing is not official resource evidence because it
measures the first decode without a fixed warm-up. Use only the runner below
for P1.1b.

The first P1.1b collection used a superseded PID-presence rule and produced
zero eligible rows under Windows/WDDM. Retain it as observational provenance;
do not merge it with the revised independent-repetition protocol.

P1.1b-v2 remains ready to close the resource component of the advisor's
scientific question, but the user-prioritized P1.7a screen now precedes it. Its
existing fresh-root command remains valid and must not be launched concurrently
with P1.7a training. P0.8b remains intentionally delayed. Archived seed
commands must be audited against the current checkpoint/resume contract before
being copied back here; do not run an old block blindly.

P1.4b is closed. Continue CPU writing from `MANUSCRIPT_SKELETON.md` while
running the frozen P1.7a screen. After its decision, return to P1.1b, then design FedProx-LoRA,
audit one stronger-skew T1 screen, and close seed-2 T3. Decide federated-7B
feasibility only if the manuscript retains an empirical large-model-FL
comparison.

P1.7a is the only active method-innovation candidate. It keeps uniform verified
teacher-target CE as the anchor and adds a pairwise loss that ranks a verified
teacher SQL above a failed SQL produced by the pre-server global SLM. P0.10a
already established pair feasibility; do not rerun that diagnostic. The first
training gate must use global-SLM rejected outputs only, not client logits or
client-specific rejected outputs, so it does not reopen the failed P0.10 FedDF
mechanism. The frozen screen uses all 347 failed `global_fl` rows in the fixed
512-row public subset (225 execution errors and 122 executable-wrong outputs),
reference-free logistic ranking over length-normalized chosen/rejected sequence
log-probabilities, `lambda_preference=1.0`, and uniform chosen CE on all 512
rows. It preserves the positive-only control's 512 microsteps and 32 optimizer
updates; the 347 rejected-sequence forwards are additional compute and are
reported separately. The arm and its compact derived pair package are frozen
at code commits `bd150c5` and `d2a4d9b`.

## P1.7a — active 512-row execution-preference screen

**Purpose:** test whether explicit negative SQL information improves the
already-positive hard-target transfer signal. This is not FedDF: the server
loads only the 1.5B student, ranks each verified teacher SQL over the failed
pre-server global-FL SQL for the same public input, and never consumes client
logits or client-specific outputs.

**Matched control:** reuse the completed immutable P0.10d `llm_only512` arm.
Both arms start from the exact same round-1 factor-wise FedAvg adapter, traverse
the same 512 teacher-target rows in the same seed-0 order, use the same CE,
optimizer schedule, 512 microsteps, and 32 optimizer updates. P1.7a alone adds
347 rejected-sequence forwards. The fixed coefficient is `1.0`; do not sweep it
or replace the subset after observing Spider.

**Promotion/stop rule:** promote once to an untuned full-3,873 screen only if
P1.7a is at least `+1.0` Spider EX over `positive_ce512` and has no more
execution errors. Otherwise archive the branch immediately. EM is diagnostic
only and cannot override the EX gate.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $P='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $Q='processed_data/BIRD/p017a_qwen_global_preference512_s0/preference_pairs.csv'; $V='processed_data/BIRD/p017a_qwen_global_preference512_s0/provenance.json'; $H='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $C='artifacts/federated/p010d_qwen_llm_only512_noicl_k5_e1_t1_s0/round_1/m_g'; $O='artifacts/federated/p017a_qwen_globalpref512_noicl_k5_e1_t1_s0'; $E='artifacts/eval_resume/p017a_qwen_positivece_vs_globalpref512_spider_s0/eval_k0'; $G=(git rev-parse HEAD).Trim(); if ($G -ne 'd2a4d9b1c8113e4bbcce00c47b6bead0fe6d0492') { throw "P1.7a requires code/data commit d2a4d9b1c8113e4bbcce00c47b6bead0fe6d0492; current=$G" }; foreach ($X in @($P,$Q,$V,"$H/fedavg_adapter/adapter_config.json","$C/adapter_config.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P1.7a frozen input: $X" } }; $PV=Get-Content -LiteralPath $V -Raw | ConvertFrom-Json; $QH=(Get-FileHash -Algorithm SHA256 -LiteralPath $Q).Hash.ToLowerInvariant(); if ($PV.source_arm -ne 'global_fl' -or $PV.n_pairs -ne 347 -or $PV.rejected_state_counts.execution_error -ne 225 -or $PV.rejected_state_counts.executable_wrong -ne 122 -or $PV.output.sha256 -ne $QH) { throw "P1.7a pair provenance mismatch: source=$($PV.source_arm) n=$($PV.n_pairs) sha=$QH" }; uv run python experiments/federated/run.py round --arm fedpref --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1 --lambda-kd 0 --preference-pairs $Q --preference-source-arm global_fl --lambda-preference 1 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $H --out $O --seed 0 --stage poc; if ($LASTEXITCODE -ne 0) { throw 'P1.7a preference training failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/round_1/m_g_meta.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P1.7a output: $X" } }; $M=Get-Content -LiteralPath "$O/round_1/m_g_meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 512 -or $M.n_preference_examples -ne 347 -or $M.steps -ne 512) { throw "P1.7a terminal-count mismatch: examples=$($M.n_examples) pairs=$($M.n_preference_examples) steps=$($M.steps)" }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "positive_ce512=$C" "global_pref512=$O/round_1/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P1.7a Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P1.7a evaluation manifests: $E/manifests" }; Write-Host 'P1.7a screen complete: push compact results and stop for the fixed EX/execution-error gate; do not tune lambda or launch full 3,873 yet'
```

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

**Status:** command ready; pending behind the user-prioritized P1.7a screen.

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
