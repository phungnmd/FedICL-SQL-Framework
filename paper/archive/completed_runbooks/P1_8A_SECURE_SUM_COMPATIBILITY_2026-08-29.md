# P1.8a — Secure Sum compatibility replay — complete

## Decision

P1.8a validates Secure Sum as an optional aggregation/privacy layer over the
same sample-weighted factor-wise FedAvg objective. It is not an accuracy
component and does not require historical or future accuracy experiments to be
rerun through the masked protocol.

The canonical five-client Qwen round-1 replay covered 18,464,768 LoRA
parameters and passed the frozen numerical gate:

- maximum absolute error: `3.725290298461914e-9`;
- mean absolute error: `1.4492840809562156e-10`;
- cosine similarity: `0.9999999999999983`;
- tolerance: `1e-6`;
- aggregation time: `7.1147 s` on the replay host;
- masked upload: `738,590,720` bytes;
- protocol metadata: `1,401` bytes;
- observed total communication expansion versus the comparable plaintext
  upload-plus-broadcast accounting: approximately `49.93%`.

Artifact: `experiments/federated/results/p18a_secure_replay_qwen_fl_s0_r1/metrics.json`,
result commit `6c67e79`, producing code `3c21b96`.

This is a local pairwise-mask protocol simulation and compatibility audit, not
an end-to-end cryptographic deployment or a differential-privacy mechanism.
Paper accuracy tables retain their standard weighted-FedAvg lineage. New
Secure Sum audits must opt in explicitly with
`--aggregation-protocol secure_sum`; normal matched accuracy experiments use
`--aggregation-protocol plaintext`.

## Completed command

Run from the `fedicl-sql/` root in PowerShell. This command is retained only as
provenance and is not active.

```powershell
$C='artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0/round_1'; $O='artifacts/secure_aggregation_replay/p18a_qwen_fl_s0_r1'; $J='experiments/federated/results/p18a_secure_replay_qwen_fl_s0_r1/metrics.json'; git merge-base --is-ancestor 3c21b9651835409eec3b8c590b685d1b773fb0a8 HEAD; if ($LASTEXITCODE -ne 0) { throw 'P1.8 implementation commit is not present' }; $Need=@("$C/round_init_adapter/adapter_config.json","$C/fedavg_adapter/adapter_config.json"); foreach ($I in 1..5) { $Need += "$C/client_$I/adapter/adapter_config.json" }; foreach ($P in $Need) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P1.8a input: $P" } }; uv run python experiments/federated/run.py aggregate --arm fedavg --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --client-dir $C --init-adapter "$C/round_init_adapter" --reference-adapter "$C/fedavg_adapter" --out $O --report-out $J --seed 0 --aggregation-protocol secure_sum --secure-threshold 3 --secure-mask-scale 1.0 --secure-equivalence-atol 0.000001; if ($LASTEXITCODE -ne 0) { throw 'P1.8a secure replay failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath $J)) { throw "Missing P1.8a report: $J" }; $V=Get-Content -LiteralPath $J -Raw | ConvertFrom-Json; $E=$V.metrics.equivalence; if (-not $E.accepted -or [double]$E.max_abs_error -gt 0.000001 -or [double]$E.cosine_similarity -lt 0.999999999) { throw "P1.8a equivalence gate failed: accepted=$($E.accepted) max_abs=$($E.max_abs_error) cosine=$($E.cosine_similarity)" }; Write-Host "P1.8a complete: bit_identical=$($E.bit_identical) max_abs=$($E.max_abs_error) cosine=$($E.cosine_similarity); push $J and stop for review"
```
