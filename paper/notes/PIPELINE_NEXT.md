# FedLS-SQL — active experiment queue

> Run every command from the `fedicl-sql/` repository root in PowerShell.
> Each fenced block is exactly one physical command line and is independently
> resumable. The governing command rules are in `CONVENTION.MD` §6.1.

## Priority and stop rule

| Order | Evidence | Status | Why now |
|---|---|---|---|
| P0.0 | Validate frozen split and teacher cache | next | fail before spending GPU time |
| P0.1 | Pure FL and FedLS-SQL T1–T3, seed 1 | next | first independent multi-round replication |
| P0.2 | Matched Spider evaluation, seed 1 | pending | earliest decisive Q3 evidence |
| P0.3 | Pure FL and FedLS-SQL T1–T3, seed 2 | pending | complete three-seed evidence |
| P0.4 | Matched Spider evaluation, seed 2 | pending | estimate mean and variation across seeds |
| P0.5 | T3 transfer on Realistic, Syn, and DK | pending | multi-seed generalization evidence |
| P0.6 | T3 transfer on BIRD | pending | useful but slowest evaluation |
| P1 | Communication and resource consolidation | pending | Q4; no accuracy rerun required |
| P2 | FedProx, size/rank/skew sensitivity | gated | run only if requested after P0 review |

Stop and review the three-seed Spider trajectories after P0.4. Continue to
P0.5–P0.6 only if the FedLS-SQL advantage is not contradicted. Do not start a
P2 sweep merely because GPU time is available.

## Fixed scientific recipe

- Frozen private split: five non-IID Spider clients, `alpha=0.5`, split seed 0.
- Replication seeds change model/training randomness, not the private split.
- One client epoch per round; T1–T3 therefore match one to three private-data
  passes.
- No ICL anywhere: client `train_k=0`, teacher `k=0`, evaluation `k=0`.
- FedLS-SQL reuses the full-pool zero-shot teacher-logit cache. This cache is
  content-addressed and is valid across seeds only because `pool_size=0` and
  `k_teacher=0`.
- Pure FL has its own `fedavg` lineage. A `fedkd` round's `fedavg_adapter` is
  not pure FL after T1 because it inherits the preceding post-KD adapter.

Canonical seed-0 checkpoints already complete:

```text
Centralized = artifacts/probe_p/central_3ep/adapter
FL          = artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter
FedLS-SQL   = artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g
```

The `_t1_` token in the existing FedLS-SQL roots is a historical naming
misnomer. It is an immutable provenance path and must not be renamed.

## P0.0 — preflight

This checks inputs only; it does not create or overwrite anything.

```powershell
$Required=@('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json'); foreach ($P in $Required) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing required input: $P" } }; $Split=Get-Content -LiteralPath 'processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json' -Raw | ConvertFrom-Json; if (($Split.n_clients -ne 5) -or ([double]$Split.alpha -ne 0.5) -or ($Split.seed -ne 0)) { throw 'Frozen split metadata mismatch: expected K=5, alpha=0.5, seed=0' }; foreach ($I in 1..5) { $P="processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_${I}_train.csv"; if (-not (Test-Path -LiteralPath $P)) { throw "Missing client shard: $P" } }; Write-Host 'P0.0 complete: frozen split and teacher cache are present'
```

## P0.1 — seed 1 training

Run pure FL first. The output root is independent of every FedLS-SQL lineage.
Re-running the exact line resumes `_ckpt` stages and validates completed
rounds; any recipe drift at the same root fails loudly.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=1; $R="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed $S; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed $S training failed; rerun this exact line to resume" }; foreach ($N in 1..3) { $A="$R/round_$N/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete pure-FL seed $S round ${N}: $A" }; if (Test-Path -LiteralPath "$R/round_$N/m_g") { throw "Unexpected server output in pure-FL seed $S round ${N}" } }; if (-not (Test-Path -LiteralPath "$R/setup.json") -or -not (Test-Path -LiteralPath "$R/manifest.json")) { throw "Missing pure-FL seed $S setup/manifest" }; Write-Host "P0.1a complete: pure FL seed $S T1-T3"
```

Then extend the existing FedLS-SQL seed-1 T1 lineage through T3. Keep
`--teacher-4bit`: it is part of the existing setup/cache fingerprint even
though cached training does not load the teacher online.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=1; $R="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; uv run python experiments/federated/run.py run --arm fedkd --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed $S; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed $S training failed; rerun this exact line to resume" }; foreach ($N in 1..3) { foreach ($A in @("$R/round_$N/fedavg_adapter","$R/round_$N/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete FedLS-SQL seed $S round ${N}: $A" } } }; if (-not (Test-Path -LiteralPath "$R/setup.json") -or -not (Test-Path -LiteralPath "$R/manifest.json")) { throw "Missing FedLS-SQL seed $S setup/manifest" }; Write-Host "P0.1b complete: FedLS-SQL seed $S T1-T3"
```

## P0.2 — seed 1 Spider evaluation

The six arms form the matched Q3 trajectory. `--resume-dir` is unique to this
dataset/seed/config, and `--skip-completed` makes an exact completed rerun a
no-op. A partial JSONL checkpoint resumes completed row IDs.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=1; $F="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; $K="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; $E="artifacts/eval_resume/fedls_q3_spider_s$S/eval_k0"; foreach ($A in @("$F/round_1/fedavg_adapter","$F/round_2/fedavg_adapter","$F/round_3/fedavg_adapter","$K/round_1/m_g","$K/round_2/m_g","$K/round_3/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing evaluation checkpoint: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s1_t1=$F/round_1/fedavg_adapter" "fl_s1_t2=$F/round_2/fedavg_adapter" "fl_s1_t3=$F/round_3/fedavg_adapter" "fedls_s1_t1=$K/round_1/m_g" "fedls_s1_t2=$K/round_2/m_g" "fedls_s1_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Spider evaluation seed $S failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifest directory: $E/manifests" }; Write-Host "P0.2 complete: Spider trajectories for seed $S"
```

## P0.3 — seed 2 training

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=2; $R="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed $S; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed $S training failed; rerun this exact line to resume" }; foreach ($N in 1..3) { $A="$R/round_$N/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete pure-FL seed $S round ${N}: $A" }; if (Test-Path -LiteralPath "$R/round_$N/m_g") { throw "Unexpected server output in pure-FL seed $S round ${N}" } }; if (-not (Test-Path -LiteralPath "$R/setup.json") -or -not (Test-Path -LiteralPath "$R/manifest.json")) { throw "Missing pure-FL seed $S setup/manifest" }; Write-Host "P0.3a complete: pure FL seed $S T1-T3"
```

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=2; $R="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; uv run python experiments/federated/run.py run --arm fedkd --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed $S; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed $S training failed; rerun this exact line to resume" }; foreach ($N in 1..3) { foreach ($A in @("$R/round_$N/fedavg_adapter","$R/round_$N/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete FedLS-SQL seed $S round ${N}: $A" } } }; if (-not (Test-Path -LiteralPath "$R/setup.json") -or -not (Test-Path -LiteralPath "$R/manifest.json")) { throw "Missing FedLS-SQL seed $S setup/manifest" }; Write-Host "P0.3b complete: FedLS-SQL seed $S T1-T3"
```

## P0.4 — seed 2 Spider evaluation

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=2; $F="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; $K="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; $E="artifacts/eval_resume/fedls_q3_spider_s$S/eval_k0"; foreach ($A in @("$F/round_1/fedavg_adapter","$F/round_2/fedavg_adapter","$F/round_3/fedavg_adapter","$K/round_1/m_g","$K/round_2/m_g","$K/round_3/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing evaluation checkpoint: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s2_t1=$F/round_1/fedavg_adapter" "fl_s2_t2=$F/round_2/fedavg_adapter" "fl_s2_t3=$F/round_3/fedavg_adapter" "fedls_s2_t1=$K/round_1/m_g" "fedls_s2_t2=$K/round_2/m_g" "fedls_s2_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Spider evaluation seed $S failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifest directory: $E/manifests" }; Write-Host "P0.4 complete: Spider trajectories for seed $S; stop and review all three seeds"
```

## P0.5 — T3 transfer on Spider variants, seeds 1 and 2

Run this only after the P0.4 review gate. Each dataset/seed receives its own
resume namespace, so a failure in a later dataset cannot invalidate earlier
completed evaluations.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; foreach ($S in 1,2) { $F="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; $K="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; foreach ($D in @(@('processed_data/SPIDER_REALISTIC/test.csv','realistic'),@('processed_data/SPIDER_SYN/test.csv','syn'),@('processed_data/SPIDER_DK/test.csv','dk'))) { $T=$D[0]; $Tag=$D[1]; $E="artifacts/eval_resume/fedls_q3_${Tag}_s$S/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $T --arms "fl_s${S}_t3=$F/round_3/fedavg_adapter" "fedls_s${S}_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Evaluation failed for seed $S dataset $T; rerun this exact line to resume" } } }; Write-Host 'P0.5 complete: T3 Realistic, Syn, and DK for seeds 1 and 2'
```

## P0.6 — T3 transfer on BIRD, seeds 1 and 2

BIRD is isolated because execution scoring is much slower than the Spider
variants. It remains resumable per seed.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; foreach ($S in 1,2) { $F="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; $K="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; $E="artifacts/eval_resume/fedls_q3_bird_s$S/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --arms "fl_s${S}_t3=$F/round_3/fedavg_adapter" "fedls_s${S}_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "BIRD evaluation seed $S failed; rerun this exact line to resume" } }; Write-Host 'P0.6 complete: T3 BIRD for seeds 1 and 2'
```

## After each completed block

1. Preserve the output root and resume directory exactly as written.
2. Commit generated `config.json`, `metrics.json`, predictions, and manifests
   from the code repository; never commit `artifacts/` adapters or caches.
3. Update `RESULT_REGISTRY.md` and `LAB_LOG.md` only after validating the run.
4. Report seed-level EX/EM and mean ± sample SD. Paired question-level tests
   may support within-seed comparisons, not substitute for multi-seed method
   inference.

## Not scheduled yet

- P1 resource consolidation should read the timing, peak-VRAM, and
  `communication_bytes` fields already stored in federated metrics. Do not
  rerun accuracy experiments for it. Add a tested analysis utility before
  publishing a command here.
- FedProx is not implemented and therefore has no pretend command.
- Do not run new ICL, FLoRA-NA, self-consistency, T4/T5, rank, model-size,
  public-pool-size, or skew sweeps before the P0 evidence review.
