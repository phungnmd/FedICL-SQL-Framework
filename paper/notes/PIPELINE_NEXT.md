# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every PowerShell
> block below is exactly one physical line, fail-fast, and safe to rerun. The
> governing rules are in `CONVENTION.MD` §6.1.

## Active task and stop rule

T0 is closed with the **pragmatic RQ2**: demonstrate the client/deployment
resource and communication savings of retaining a 1.5B SLM rather than placing
the 7B teacher on clients or in inference. Full federated 7B training is not
part of the default evidence package.

The only active empirical task is **T1: matched public-supervision ablation**.

| Order | Action | Status |
|---|---|---|
| P0.0 | Build and verify the exact 3,873-row BIRD-gold control | next |
| P0.1 | Train the missing public-gold CE server branch from the shared T1 adapter | pending |
| P0.2 | Evaluate the four matched T1 arms on Spider | pending |
| P0.3 | Review the causal result and choose the next task | gated |

Stop after P0.2. Do not start seed replication, FedProx, heterogeneity, or
sensitivity runs until the T1 result has been reviewed against the decision
gate in `PAPER_EVIDENCE_PLAN.md`.

## Fixed T1 comparison

All four arms start from the same seed-0, round-1 client training and
factor-wise FedAvg adapter:

```text
artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter
```

| Evaluation arm | Server treatment |
|---|---|
| `fl_t1_shared` | none |
| `public_gold_ce` | CE on BIRD gold for the exact retained 3,873 rows |
| `teacher_target_ce` | CE on teacher-generated SQL (`fedavg_pub`) |
| `fedls_t1` | teacher-target CE + reverse KL (`fedkd`) |

The gold control is reconstructed by the original source `idx` stored in the
selection checkpoint. Never join it by question text: duplicate BIRD questions
make that mapping ambiguous for nine rows.

## P0.0 — build and verify the matched gold control

This command is CPU-only. It atomically rebuilds the CSV, verifies row identity
and count, and writes hashes plus target semantics to a provenance JSON.

```powershell
$O='processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv'; uv run python scripts/build_public_gold_control.py --source-csv processed_data/BIRD/centralized/train.csv --teacher-pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --selection-ckpt processed_data/BIRD/bootstrap_full_exmatch/train.score_ckpt.jsonl --out $O; if ($LASTEXITCODE -ne 0) { throw 'Public-gold control build failed' }; if (-not (Test-Path -LiteralPath $O) -or -not (Test-Path -LiteralPath "${O}.provenance.json")) { throw 'Public-gold output or provenance is missing' }; $N=(Import-Csv -LiteralPath $O).Count; $P=Get-Content -LiteralPath "${O}.provenance.json" -Raw | ConvertFrom-Json; if ($N -ne 3873 -or $P.n_rows -ne 3873 -or $P.target_semantics -ne 'bird_gold_sql') { throw "Public-gold verification failed: rows=$N provenance_rows=$($P.n_rows) target=$($P.target_semantics)" }; Write-Host 'P0.0 complete: exact 3,873-row BIRD-gold control verified'
```

## P0.1 — train only the missing public-gold CE branch

This reuses the immutable shared round-1 client and aggregation stages. On an
exact rerun, completed stages/checkpoints are skipped; configuration drift at
the same output root fails through the existing fingerprints.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $G='artifacts/federated/fedavg_pub_gold_noicl_k5_e1_t1_s0'; foreach ($P in @("$C/fedavg_adapter/adapter_config.json",'processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv','processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv.provenance.json')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing T1 input: $P" } }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $G --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Public-gold CE branch failed; rerun this exact line to resume' }; foreach ($P in @("$G/round_1/m_g/adapter_config.json","$G/setup.json","$G/manifest.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Incomplete public-gold CE output: $P" } }; Write-Host 'P0.1 complete: matched public-gold CE branch trained'
```

## P0.2 — evaluate the four matched arms

The resume directory is unique to this comparison. `--skip-completed` makes a
completed exact rerun a no-op and a partial run resumes from its JSONL rows.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $G='artifacts/federated/fedavg_pub_gold_noicl_k5_e1_t1_s0/round_1/m_g'; $H='artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g'; $K='artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g'; $E='artifacts/eval_resume/fedls_t1_public_supervision_s0/eval_k0'; foreach ($A in @("$C/fedavg_adapter",$G,$H,$K)) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing evaluation adapter: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_t1_shared=$C/fedavg_adapter" "public_gold_ce=$G" "teacher_target_ce=$H" "fedls_t1=$K" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Matched T1 evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifests: $E/manifests" }; Write-Host 'P0.2 complete: stop and review the four-arm T1 result'
```

## P0.3 — review gate

After P0.2, report the generated result directory or commit it. The review must
compare EX, execution-error rate, paired wins/losses, and uncertainty on the
same Spider rows. EM is secondary because BIRD gold and teacher SQL can be
semantically equivalent but textually different.

The result chooses the next branch:

- teacher-target CE or reverse KL beats public-gold CE: continue the FedLS-SQL
  large-to-small claim, then activate efficiency evidence;
- reverse KL is the only added value: center the paper on soft guidance;
- public-gold CE explains the gain: reframe or redesign before more compute;
- public-gold CE hurts but teacher supervision helps: retain the transfer story
  and prioritize mechanism/error analysis.

## Parked work

- Seed 1/2 replication is retained as T7 in `PAPER_EVIDENCE_PLAN.md`; its old
  executable queue remains recoverable from Git commit `b996594`.
- FedProx, heterogeneity, and sensitivity tasks remain gated.
- ICL and FLoRA-NA remain archived negative branches.

## After a completed block

1. Preserve output roots and resume directories exactly as written.
2. Commit generated configs, metrics, predictions, and manifests from the code
   repository; never commit adapter/cache directories under `artifacts/`.
3. Update `RESULT_REGISTRY.md` and `LAB_LOG.md` only after validating results.
