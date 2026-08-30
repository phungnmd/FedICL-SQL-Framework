# P1.5d — FedProx T1/T2 Spider trajectory diagnostic

Completed 2026-08-30. Nested result commit: `9537103`. Evaluation-producing
SHA: `458a9f3`. Canonical result directory:
`experiments/eval_arms/results/eval_arms__s0__20260830T083531`.

## Purpose and boundary

Evaluate immutable FedProx T1/T2 adapters against independent pure FL at the
same rounds. This was a post-hoc mechanism diagnostic, not checkpoint selection
or coefficient tuning. EX is primary; no OOD or combined FedLS-FedProx run was
authorized by this task.

## Exact run command

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0'; $A1="$R/round_1/fedavg_adapter"; $A2="$R/round_2/fedavg_adapter"; $E='artifacts/eval_resume/p15d_fedprox_mu001_t1_t2_spider_s0/eval_k0'; foreach ($P in @('processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv',"$R/setup.json","$R/manifest.json","$A1/adapter_config.json","$A2/adapter_config.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P1.5d input: $P" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fedprox_mu001_t1=$A1" "fedprox_mu001_t2=$A2" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P1.5d FedProx T1/T2 Spider evaluation failed; rerun this exact line and resume root' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw 'Missing P1.5d evaluation manifests' }; Write-Host 'P1.5d complete: push compact eval results/config/predictions/manifests and stop for round-matched trajectory analysis; do not select a checkpoint or launch OOD/tuning'
```

## Result and decision

| Round | Pure FL EX | FedProx EX | Delta | FedProx wins/losses | Exact paired p | FL/FedProx errors |
|---:|---:|---:|---:|---:|---:|---:|
| T1 | 56.67 | 55.80 | -0.87 | 26/35 | 0.306 | 241/249 |
| T2 | 62.19 | 59.96 | -2.22 | 19/42 | 0.00444 | 202/214 |
| T3 | 64.31 | 62.77 | -1.55 | 22/38 | 0.0519 | 193/194 |

FedProx improves along its own trajectory, but remains below round-matched
FedAvg at every point. Therefore there is no early stabilization advantage to
motivate a FedLS-FedProx screen. P1.5 is closed without tuning or OOD.
