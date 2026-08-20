# FedLS-SQL — active experiment queue

> This file contains only open work after the 2026-08-19 FedLS-SQL refactor.
> Completed and superseded commands are preserved in
> `paper/archive/pre_fedls_2026-08/legacy_runbooks/`.

## Status

| Priority | Task | Status |
|---|---|---|
| P0 | Pure FL through T=3, seed 0 | run next |
| P0 | Fill Centralized vs FL vs FedLS-SQL result row | waits on pure FL |
| P0 | Consolidate communication/resource metrics | pending |
| P1 | Multi-round seeds 1 and 2 | pending |
| P2 | FedProx, size/rank/skew sensitivity | scope with advisor first |

## Block K — pure FL through T=3

This is the missing causal control. Do not substitute the `fedavg_adapter`
inside round 2 or 3 of a `fedkd` run: those adapters inherit prior post-KD
global models.

Run the following single PowerShell line from the `fedicl-sql/` root. It is
fail-fast and safe to resume. `${n}` is deliberately delimited because
PowerShell otherwise parses the colon after `$n` as part of a scoped variable.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $R='artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0'; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Pure-FL training failed' }; foreach ($n in 1..3) { $A="$R/round_$n/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete FL round ${n}: $A" }; if (Test-Path -LiteralPath "$R/round_$n/m_g") { throw "Unexpected server output at pure-FL round $n" } }; foreach ($ds in @(@('processed_data/SPIDER/centralized/test.csv','fl_only_spider_s0'),@('processed_data/SPIDER_REALISTIC/test.csv','fl_only_realistic_s0'),@('processed_data/SPIDER_SYN/test.csv','fl_only_syn_s0'),@('processed_data/SPIDER_DK/test.csv','fl_only_dk_s0'))) { Write-Host "=== $($ds[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $ds[0] --arms "fl_only_t1=$R/round_1/fedavg_adapter" "fl_only_t2=$R/round_2/fedavg_adapter" "fl_only_t3=$R/round_3/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($ds[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Evaluation failed: $($ds[0])" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --arms "fl_only_t1=$R/round_1/fedavg_adapter" "fl_only_t2=$R/round_2/fedavg_adapter" "fl_only_t3=$R/round_3/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fl_only_bird_s0/eval_k0 --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'BIRD evaluation failed' }; Write-Host 'Block K complete: pure FL T1-T3 trained and evaluated on Spider, Realistic, Syn, DK, and BIRD'
```

Expected lineage:

```text
base -> round_1/fedavg_adapter
     -> round_2/fedavg_adapter
     -> round_3/fedavg_adapter
```

For arm `fedavg`, the runner returns the aggregated adapter as the next round's
global model and records no separate server `m_g` directory.

## Output to update after Block K

Fill the `FL` row in `RESULT_REGISTRY.md` using only:

```text
artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter
```

The final paper table is:

```text
Centralized = artifacts/probe_p/central_3ep/adapter
FL          = artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_3/fedavg_adapter
FedLS-SQL   = artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g
```

## Next after Block K

1. Extract round-wise FL metrics and compare T1-T3 against FedLS-SQL.
2. Consolidate trainable parameters, adapter bytes, total communication,
   training time, peak VRAM, and inference latency.
3. Run the T1-T3 trajectory for seeds 1 and 2.
4. Do not run new ICL or FLoRA-NA experiments.
5. Do not start P2 sweeps until their necessity is agreed with the advisor.
