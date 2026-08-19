# Federated ICL pipeline — K=5, T=1, seed 0

Run in PowerShell from the `fedicl-sql/` repository root. Every executable
command below is a single line. The target GPU is one NVIDIA RTX A5000 24 GB. Client/server
training uses one local epoch, batch 1, and gradient accumulation 16 because the RKL server path
requires batch 1 and the established effective batch is 16; this is a protocol
constraint, not a 16 GB-memory assumption. Teacher-cache construction stays
4-bit for headroom and cache identity. Optimizer checkpoints are written every
200 steps. Evaluation is greedy, batch 16, with row-level JSONL resume and
exact-run manifests.

Clients train with fixed `dail_weighted k=3`, question+SQL demonstrations without
demo schemas, and a full target schema. The final global adapter is evaluated
without ICL, with a centralized ICL pool, and with each private client ICL pool.

## 1. Preflight

Run this pipeline after the cache preflight/build in `PIPELINE_NO_ICL.md`, or
verify the same cache identity directly:

```powershell
git rev-parse --short HEAD
```

```powershell
git status --short
```

```powershell
$required=@('processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/SPIDER/federated_noniid/alpha_0.5/k5/split.json','processed_data/BIRD/bootstrap_full_exmatch/train.csv'); $required += 1..5 | ForEach-Object { "processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_$($_)_train.csv" }; $required | ForEach-Object { if (-not (Test-Path -LiteralPath $_ -PathType Leaf)) { throw "Missing file: $_" } }; Write-Host 'Preflight files OK'
```

```powershell
if (-not (Test-Path -LiteralPath 'artifacts/teacher_logit_cache/rkd_k0_full/meta.json' -PathType Leaf)) { throw 'Missing teacher cache meta.json' }; Get-Content -Raw 'artifacts/teacher_logit_cache/rkd_k0_full/meta.json' | ConvertFrom-Json | Select-Object pool,pool_sha256,pool_size,seed,model,teacher_model,teacher_4bit,k_teacher,schema_style,retrieval,embedder,tau,demo_style,max_len,n_examples | Format-List
```

Required cache settings are `pool_size=0`, `seed=0`, `teacher_4bit=true`,
`k_teacher=0`, `schema_style=full`, `retrieval=dail_select`,
`embedder=BAAI/bge-small-en-v1.5`, `tau=0.85`, `demo_style=never_schema`, and
`max_len=2560`. The federated runner fails before loading the student if these
settings or the public-pool hash differ.

If the cache is absent or different, build/rebuild it with this resumable
command. Rerunning it skips entries already cached:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python scripts/build_teacher_logit_cache.py --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --seed 0 --model Qwen/Qwen2.5-1.5B-Instruct --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --out artifacts/teacher_logit_cache/rkd_k0_full
```

## 2. Wiring smoke

This uses clients 1–2 from the committed K=5 split and is not a scientific K=2
result. Draft SQL/skeleton caches flush incrementally and are reused when this
same command is rerun. Optimizer checkpointing is set to every step for smoke.
The smoke uses `grad_accum=1`: with only two micro-steps, `grad_accum=16` would
make the diagnostic update unnecessarily small. The trainer also disables
warmup when a capped job has only one optimizer update, preventing that update
from running at learning rate zero. The full run still uses `grad_accum=16`.

Run or resume with the exact same command:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py run --arm florana_kd --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 2 --rounds 1 --local-epochs 1 --client-train-k 3 --client-retrieval dail_weighted --client-demo-k-fixed --client-demo-style never_schema --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --client-max-steps 2 --florana-steps 2 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 2 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 1 --max-len 2560 --save-steps 1 --out artifacts/federated/smoke_florana_kd_icl3_k2of5_t1_s0_ga1 --seed 0
```

```powershell
$clientHashes=1..2 | ForEach-Object { (Get-FileHash -Algorithm SHA256 -LiteralPath "artifacts/federated/smoke_florana_kd_icl3_k2of5_t1_s0_ga1/round_1/client_$_/adapter/adapter_model.safetensors").Hash }; if (($clientHashes | Select-Object -Unique).Count -ne 2) { throw 'Smoke failed: client adapters are byte-identical' }; $stageHashes=@('florana_adapter','m_g') | ForEach-Object { (Get-FileHash -Algorithm SHA256 -LiteralPath "artifacts/federated/smoke_florana_kd_icl3_k2of5_t1_s0_ga1/round_1/$_/adapter_model.safetensors").Hash }; if ($stageHashes[0] -eq $stageHashes[1]) { throw 'Smoke failed: server KD did not change the aggregated adapter' }; Write-Host 'Smoke adapter updates OK'
```

```powershell
uv run python -c "from fedicl_sql.runtime.manifest import resolve_m_g; print(resolve_m_g('artifacts/federated/smoke_florana_kd_icl3_k2of5_t1_s0_ga1', 1))"
```

## 3. Full ICL training

Do not share client adapter directories with the no-ICL run. Run or resume with
the exact same command. Completed clients/stages are reused, optimizer state
resumes from `_ckpt`, and draft caches resume independently.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py run --arm florana_kd --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --rounds 1 --local-epochs 1 --client-train-k 3 --client-retrieval dail_weighted --client-demo-k-fixed --client-demo-style never_schema --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out artifacts/federated/florana_kd_icl3_k5_e1_t1_s0 --seed 0
```

```powershell
uv run python -c "from fedicl_sql.runtime.manifest import resolve_m_g; print(resolve_m_g('artifacts/federated/florana_kd_icl3_k5_e1_t1_s0', 1))"
```

```powershell
$clientHashes=1..5 | ForEach-Object { (Get-FileHash -Algorithm SHA256 -LiteralPath "artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/client_$_/adapter/adapter_model.safetensors").Hash }; if (($clientHashes | Select-Object -Unique).Count -ne 5) { throw 'Full run failed validation: duplicate client adapters' }; $stageHashes=@('florana_adapter','m_g') | ForEach-Object { (Get-FileHash -Algorithm SHA256 -LiteralPath "artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/$_/adapter_model.safetensors").Hash }; if ($stageHashes[0] -eq $stageHashes[1]) { throw 'Full run failed validation: server KD did not change the aggregated adapter' }; Write-Host 'Full adapter updates OK'
```

Expected final adapter:
`artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/m_g`.

The round's `manifest.json` points to a deterministic federated
`results/<run_id>/metrics.json`. That result contains all five client training
summaries and exact train configs, aggregation diagnostics, and the server-KD
summary, including stages completed by an earlier resumed invocation. Detailed
per-layer FLoRA diagnostics remain in `round_1/florana_meta.json`.

## 4. Build the matched factor-wise FedAvg baseline

Factor-wise sample-weighted FedAvg is the aggregation baseline. Round 1 is
arm-invariant, so all three commands below reuse the five completed ICL client
adapters from section 3 through `--client-out`; they do not retrain clients.
The first command builds `fedavg_adapter`, the second adds the public-CE
control, and the third adds the matched public CE + RKL server stage. Exact
client fingerprints fail loudly if any client-training setting drifts.

If the original FLoRA-NA pipeline and its final-`m_g` evaluations are already
complete, start here. Do not rerun sections 1–3 or the existing `train_icl3`
eval commands; run only the new pre-server/FedAvg commands below.

Build or resume the aggregation-only baseline:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedavg --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 3 --client-retrieval dail_weighted --client-demo-k-fixed --client-demo-style never_schema --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1 --out artifacts/federated/fedavg_icl3_k5_e1_t1_s0 --seed 0
```

Build or resume the public-CE control from the same FedAvg adapter:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 3 --client-retrieval dail_weighted --client-demo-k-fixed --client-demo-style never_schema --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1 --out artifacts/federated/fedavg_pub_icl3_k5_e1_t1_s0 --seed 0
```

Build or resume the matched FedAvg + RKD branch:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedkd --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 3 --client-retrieval dail_weighted --client-demo-k-fixed --client-demo-style never_schema --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1 --out artifacts/federated/fedkd_icl3_k5_e1_t1_s0 --seed 0
```

```powershell
$required=@('artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/florana_adapter/adapter_model.safetensors','artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/fedavg_adapter/adapter_model.safetensors','artifacts/federated/fedkd_icl3_k5_e1_t1_s0/round_1/m_g/adapter_model.safetensors'); $required | ForEach-Object { if (-not (Test-Path -LiteralPath $_ -PathType Leaf)) { throw "Missing primary baseline artifact: $_" } }; $pre=@('florana_adapter','fedavg_adapter') | ForEach-Object { (Get-FileHash -Algorithm SHA256 -LiteralPath "artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/$_/adapter_model.safetensors").Hash }; if ($pre[0] -eq $pre[1]) { throw 'Baseline failed: FLoRA-NA and FedAvg adapters are byte-identical' }; Write-Host 'Primary FedAvg/FedKD artifacts OK'
```

After running the optional `fedavg_pub` ablation, validate it separately:

```powershell
$path='artifacts/federated/fedavg_pub_icl3_k5_e1_t1_s0/round_1/m_g/adapter_model.safetensors'; if (-not (Test-Path -LiteralPath $path -PathType Leaf)) { throw "Missing optional fedavg_pub artifact: $path" }; Write-Host 'Optional fedavg_pub artifact OK'
```

Expected comparison checkpoints are:

```text
FLoRA-NA before server: artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/florana_adapter
FLoRA-NA after RKD:     artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/m_g
FedAvg before server:   artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/fedavg_adapter
FedAvg after public CE (optional ablation): artifacts/federated/fedavg_pub_icl3_k5_e1_t1_s0/round_1/m_g
FedAvg after RKD:       artifacts/federated/fedkd_icl3_k5_e1_t1_s0/round_1/m_g
```

## 5. Evaluate without ICL

This tests whether in-context training remains usable when demonstrations are
unavailable.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms train_icl3=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_noicl --skip-completed
```

Evaluate FLoRA-NA before the server step:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_florana_pre_server=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/florana_adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_noicl_florana_pre_server --skip-completed
```

Evaluate factor-wise FedAvg before the server step:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_pre_server=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/fedavg_adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_noicl_fedavg_pre_server --skip-completed
```

Evaluate FedAvg after public CE:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_pub=artifacts/federated/fedavg_pub_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_noicl_fedavg_pub --skip-completed
```

Evaluate FedAvg after public CE + RKL:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_kd=artifacts/federated/fedkd_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_noicl_fedavg_kd --skip-completed
```

## 6. Evaluate with centralized ICL — diagnostic only

The pooled Spider-train demo source is not a valid federated deployment pool.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms train_icl3=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_centralized --skip-completed
```

Run the same centralized-ICL diagnostic separately on the four added
comparison checkpoints:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_florana_pre_server=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/florana_adapter --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_centralized_florana_pre_server --skip-completed
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_pre_server=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/fedavg_adapter --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_centralized_fedavg_pre_server --skip-completed
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_pub=artifacts/federated/fedavg_pub_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_centralized_fedavg_pub --skip-completed
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_kd=artifacts/federated/fedkd_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_centralized_fedavg_kd --skip-completed
```

## 7. Evaluate with each private client ICL pool — primary ICL result

The same global adapter is evaluated five times, once per client-private demo
pool. Retain mean, standard deviation, and all five per-pool scores.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms train_icl3=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_per_client --skip-completed
```

Run the primary private-pool evaluation separately on the four added
comparison checkpoints:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_florana_pre_server=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/florana_adapter --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_per_client_florana_pre_server --skip-completed
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_pre_server=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/fedavg_adapter --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_per_client_fedavg_pre_server --skip-completed
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_pub=artifacts/federated/fedavg_pub_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_per_client_fedavg_pub --skip-completed
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_fedavg_kd=artifacts/federated/fedkd_icl3_k5_e1_t1_s0/round_1/m_g --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_icl_per_client_fedavg_kd --skip-completed
```

## 8. Stop and retain results

Keep every printed `experiments/eval_arms/results/<run_id>/` directory.
For each eval mode compare FLoRA-NA versus FedAvg before the server, FedAvg
public CE versus FedAvg RKD, and the two post-RKD global adapters. Do not start
T=2/T=3, another seed, or self-consistency before both training runbooks and
their matched baseline arms have been reviewed together.

## 9. Evaluate individual local client adapters

This final diagnostic measures whether aggregation improves over clients that
remain local. The five adapters are the common round-1 inputs shared by
FLoRA-NA and FedAvg, so evaluate them once rather than once per aggregation
method. The `{i}` adapter template pairs client `i` with its own adapter; in
the `k=3` command, the same pool id also selects that client's private demo
pool. Do not evaluate every local adapter against every other client's pool.

Evaluate all five local adapters without ICL:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_local_clients=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/client_{i}/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_local_clients_noicl --skip-completed
```

Evaluate each local adapter with its own private client ICL pool:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode per_client --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --k-clients 5 --test-csv processed_data/SPIDER/centralized/test.csv --arms icl3_local_clients=artifacts/federated/florana_kd_icl3_k5_e1_t1_s0/round_1/client_{i}/adapter --n-eval 0 --k 3 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_icl3_k5_e1_t1_s0/eval_local_clients_own_pool --skip-completed
```

Report the mean, standard deviation, and all five client scores. Compare the
`k=0` local mean with both pre-server global adapters, and compare the `k=3`
local-own-pool mean with each global adapter evaluated over the same five
private pools.
