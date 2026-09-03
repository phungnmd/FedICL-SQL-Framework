# FedLS-SQL — active protocol-v2 queue

> Run from the `fedicl-sql/` repository root in PowerShell. Commands follow
> `CONVENTION.MD` §6.1: one physical line, fail-fast, immutable roots, exact
> resume, and a separate allowlisted publication command. Protocol-v1 commands
> are archived and must not be rerun into their old roots.

## Active order

| Order | Task | Device | Status |
|---|---|---|---|
| P2.0a | Audit current Spider and original-BIRD processed pairs under explicit profiles | CPU | complete: `4ae6e35` |
| P2.0b | Review server artifact retirement manifest | CPU | ready; dry-run only |
| P2.0c | Import/freeze official filtered BIRD train and chosen dev release | CPU | ingestion implemented; files/checksums pending |
| P2.0d | Add official BIRD evaluator adapter and known-answer fixture | CPU | implementation gate |
| P2.0e | Materialize/audit original BIRD with evidence and build semantic K5 split | CPU | ready; compatibility track |
| P2.1a | BIRD-original centralized SFT, evidence, Qwen 1.5B, E2, seed 0 | GPU 0 | ready after P2.0e publication |
| P2.1b | BIRD-original pure FL, evidence, Qwen 1.5B, K5/T3, seed 0 | GPU 1 | ready after P2.0e publication |
| P2.2 | Rerun current FedLS reference ladder in both directions | GPU | blocked by P2.1 |
| P2.3 | Diagnose and improve KD/Federated method | adaptive | blocked by P2.2 |

The method is deliberately not frozen. P2.2 measures the previous design as a
reference; P2.3 may change hard/soft KD, selection, aggregation, local
optimization, public budget, or evidence use when a matched diagnostic supports
the change.

## P2.0a — complete

Artifact commit `4ae6e35` freezes source hashes and prompt probes. Spider has
8,659/1,034 rows, no evidence, and no DB overlap. Original BIRD has 9,428/1,534
rows, 8,783/1,386 populated evidence values, an evidence-bearing prompt probe,
and no DB overlap. This is a compatibility audit, not selection of the final
BIRD release.

## P2.0b — server retirement dry-run

This command never deletes or moves data. It inventories only exact paths in
the committed manifest and writes hashes/sizes/statuses for review. Add missing
v1 roots to the manifest in a code commit before using `--apply`; do not edit
the manifest on the experiment server during a run.

```powershell
$R='artifacts/archive/protocol_v1_no_bird_evidence/dry_run_report.json'; uv run python scripts/retire_protocol_artifacts.py --manifest configs/archive/protocol_v1_no_bird_evidence.json --report $R; if ($LASTEXITCODE -ne 0) { throw 'P2.0b retirement dry-run found a refused path; inspect the report' }; $V=Get-Content -LiteralPath $R -Raw | ConvertFrom-Json; $V.entries | Select-Object root,status,files,bytes,reason | Format-Table -Wrap; Write-Host 'P2.0b dry-run complete; do not apply until the exact inventory is reviewed'
```

No publication command is attached to P2.0b because the report contains
server-local artifact inventory and remains under ignored `artifacts/`.

## Server sync for P2.0e/P2.1

Run only when no experiment is active in this worktree. This pulls nested code
commit `11ab685`, checks the exact scientific code scope, and validates the
protocol-v2 preparation path. It does not touch unrelated untracked artifacts.

```powershell
$Expected='11ab685'; $Scope=@('fedicl_sql','experiments/client_train/run.py','experiments/federated/run.py','scripts/build_db_groups.py','scripts/build_federated.py','scripts/materialize_protocol_v2_dataset.py','scripts/audit_protocol_v2.py','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Tracked scientific code is dirty; review before pulling' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward pull failed' }; $Head=(git rev-parse --short HEAD).Trim(); if ($Head -ne $Expected) { throw "Expected code commit $Expected, found $Head" }; uv run pytest -q tests/test_materialize_protocol_v2_dataset.py tests/test_build_federated_v2.py tests/test_data_protocol.py tests/test_federated_split.py; if ($LASTEXITCODE -ne 0) { throw 'Protocol-v2 server validation failed' }; Write-Host "Server refactor ready at $Head"
```

## P2.0e — materialize BIRD-original protocol v2 and semantic K5 split

This is the audited original BIRD 9,428/1,534 release, explicitly labeled; it
does not claim to be the still-pending filtered/cleaned release. Semantic schema
groups avoid the weak global-Dirichlet fallback. Stop if a client exceeds 50%
of training rows; inspect the deterministic split rather than silently changing
the seed.

```powershell
$env:CUDA_VISIBLE_DEVICES=''; $D='processed_data/protocol_v2/BIRD/original_train9428_dev1534'; $T="$D/centralized/train.csv"; $E="$D/centralized/test.csv"; $G="$D/db_groups_g10_s0.json"; $F="$D/federated_noniid/alpha_0.5/k5"; $A='audits/protocol_v2/bird_original_materialized.json'; $Scope=@('fedicl_sql','scripts/materialize_protocol_v2_dataset.py','scripts/audit_protocol_v2.py','scripts/build_db_groups.py','scripts/build_federated.py','processed_data/BIRD/centralized/train.csv','processed_data/BIRD/centralized/test.csv'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'P2.0e scientific scope is dirty' }; uv run python scripts/materialize_protocol_v2_dataset.py --train-csv processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --dataset-profile bird_with_evidence --dataset-version bird-original-train9428-dev1534 --out $D; if ($LASTEXITCODE -ne 0) { throw 'BIRD-original materialization failed; rerun this exact line to resume' }; uv run python scripts/audit_protocol_v2.py --train-csv $T --test-csv $E --dataset-profile bird_with_evidence --dataset-version bird-original-train9428-dev1534 --schema-style full --out $A; if ($LASTEXITCODE -ne 0) { throw 'BIRD-original protocol audit failed' }; uv run python scripts/build_db_groups.py --train-csv $T --dataset-profile bird_with_evidence --n-groups 10 --seed 0 --out $G; if ($LASTEXITCODE -ne 0) { throw 'BIRD semantic DB grouping failed; rerun this exact line to resume' }; uv run python scripts/build_federated.py --train-csv $T --test-csv $E --dataset-profile bird_with_evidence --out $F --db-groups $G --n-clients 5 --alpha 0.5 --seed 0 --min-client-examples 150; if ($LASTEXITCODE -ne 0) { throw 'BIRD semantic K5 split failed; rerun this exact line to resume' }; $NT=(Import-Csv -LiteralPath $T).Count; $NE=(Import-Csv -LiteralPath $E).Count; $Counts=@(1..5 | ForEach-Object { (Import-Csv -LiteralPath "$F/client_${_}_train.csv").Count }); $Sum=($Counts | Measure-Object -Sum).Sum; $Max=($Counts | Measure-Object -Maximum).Maximum; if ($NT -ne 9428 -or $NE -ne 1534 -or $Sum -ne 9428 -or ($Counts | Measure-Object -Minimum).Minimum -lt 150 -or $Max -gt 4714) { throw "P2.0e verification failed: train=$NT test=$NE clients=$($Counts -join ',')" }; Write-Host "P2.0e ready: clients=$($Counts -join ',')"
```

Publication command — run immediately after P2.0e passes and before either GPU
job starts, because the generated CSVs are the exact training inputs.

```powershell
$D='processed_data/protocol_v2/BIRD/original_train9428_dev1534'; $F="$D/federated_noniid/alpha_0.5/k5"; $Allow=@('audits/protocol_v2/bird_original_materialized.json',"$D/protocol.json","$D/centralized/train.csv","$D/centralized/test.csv","$D/db_groups_g10_s0.json","$F/client_1_train.csv","$F/client_2_train.csv","$F/client_3_train.csv","$F/client_4_train.csv","$F/client_5_train.csv","$F/split.json","$F/stats.csv","$F/meta.json"); if (@(git diff --cached --name-only).Count -ne 0) { throw 'Refusing publication because files are already staged' }; foreach ($P in $Allow) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P2.0e publication file: $P" } }; git add -- $Allow; if ($LASTEXITCODE -ne 0) { throw 'P2.0e git add failed' }; $Staged=@(git diff --cached --name-only); $Diff=@(Compare-Object ($Allow | Sort-Object) ($Staged | Sort-Object)); if ($Diff.Count -ne 0) { $Staged | ForEach-Object { Write-Host $_ }; throw 'P2.0e staged allowlist mismatch' }; git commit -m 'data: freeze BIRD original protocol v2 split'; if ($LASTEXITCODE -ne 0) { throw 'P2.0e commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'P2.0e push failed' }; Write-Host "P2.0e published at $((git rev-parse --short HEAD).Trim())"
```

## P2.1 overnight GPU launch

Run the following blocks in two separate PowerShell terminals only after P2.0e
is committed and pushed. Both commands are independently resumable by rerunning
the exact same line. They train only; base/E1/E2/T1/T2/T3 EX evaluation waits
for P2.0d, so a later evaluator change cannot contaminate checkpoint lineage.

GPU 0 — centralized continuous two-epoch SFT. Epoch 1 and epoch 2 adapters are
both retained, with only `resume_latest` retaining trainer state.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $T='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $O='artifacts/protocol_v2/bird_original/qwen15b/centralized_e2_s0'; $I='p21a_bird_original_qwen15b_central_e2_s0'; $Scope=@('fedicl_sql','experiments/client_train/run.py','pyproject.toml','uv.lock',$T); $Dirty=@(git status --porcelain -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'P2.1a scientific scope is dirty' }; uv run python experiments/client_train/run.py --client $T --dataset-profile bird_with_evidence --out $O --stage p21a_bird_original_central --result-id $I --epochs 2 --save-epoch-checkpoints --batch-size 1 --grad-accum 16 --lr 2e-4 --lora-r 16 --max-len 2560 --save-steps 200 --model Qwen/Qwen2.5-1.5B-Instruct --train-k 0 --schema-style full --demo-style never_schema --retrieval dail_select --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.1a centralized training failed; rerun this exact line to resume' }; foreach ($P in @("$O/adapter_config.json","$O/epochs/epoch_1/adapter_config.json","$O/epochs/epoch_2/adapter_config.json","$O/resume_latest/adapter_config.json","$O/resume_latest/trainer_state.pt","$O/resume_latest/checkpoint_meta.json","experiments/client_train/results/$I/metrics.json","experiments/client_train/results/$I/config.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "P2.1a incomplete: $P" } }; Write-Host 'P2.1a complete: BIRD-original evidence-aware centralized E1/E2 checkpoints ready'
```

GPU 1 — pure FedAvg for three communication rounds. Each round performs one
local epoch over every client shard and resumes completed client/aggregation
stages from their fingerprints.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $F='processed_data/protocol_v2/BIRD/original_train9428_dev1534/federated_noniid/alpha_0.5/k5'; $O='artifacts/protocol_v2/bird_original/qwen15b/fedavg_k5_alpha05_e1_t3_s0'; $Scope=@('fedicl_sql','experiments/federated/run.py','pyproject.toml','uv.lock',$F); $Dirty=@(git status --porcelain -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'P2.1b scientific scope is dirty' }; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir $F --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --client-dataset-profile bird_with_evidence --aggregation-protocol plaintext --batch-size 1 --grad-accum 16 --lr 2e-4 --lora-r 16 --max-len 2560 --save-steps 200 --model Qwen/Qwen2.5-1.5B-Instruct --stage p21b_bird_original_fl --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P2.1b pure-FL training failed; rerun this exact line to resume' }; foreach ($N in 1..3) { if (-not (Test-Path -LiteralPath "$O/round_$N/fedavg_adapter/adapter_config.json")) { throw "P2.1b incomplete round ${N}" } }; $M=Get-Content -LiteralPath "$O/manifest.json" -Raw | ConvertFrom-Json; $S=Get-Content -LiteralPath "$O/setup.json" -Raw | ConvertFrom-Json; if ($M.latest_round -ne 3 -or $S.recipe.client_dataset_protocol.name -ne 'bird_with_evidence' -or $S.recipe.aggregation_protocol -ne 'plaintext') { throw 'P2.1b manifest/setup verification failed' }; Write-Host 'P2.1b complete: BIRD-original evidence-aware pure FL T1-T3 ready'
```

Do not run either publication block until **both** GPU processes have exited.
GPU jobs share no checkpoints, but a commit/pull during either process would
invalidate its final Git provenance.

P2.1a publication:

```powershell
$I='p21a_bird_original_qwen15b_central_e2_s0'; $Allow=@("experiments/client_train/results/$I/metrics.json","experiments/client_train/results/$I/config.json"); if (@(git diff --cached --name-only).Count -ne 0) { throw 'Refusing publication because files are already staged' }; foreach ($P in $Allow) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P2.1a result: $P" } }; $C=Get-Content -LiteralPath $Allow[1] -Raw | ConvertFrom-Json; if ($C.dataset_profile -ne 'bird_with_evidence' -or $C.epochs -ne 2 -or $C.result_id -ne $I) { throw 'P2.1a result contract mismatch' }; git add -- $Allow; $Staged=@(git diff --cached --name-only); if (@(Compare-Object ($Allow | Sort-Object) ($Staged | Sort-Object)).Count -ne 0) { throw 'P2.1a staged allowlist mismatch' }; git commit -m 'results: add BIRD v2 centralized training'; if ($LASTEXITCODE -ne 0) { throw 'P2.1a commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'P2.1a push failed' }
```

P2.1b publication:

```powershell
$O='artifacts/protocol_v2/bird_original/qwen15b/fedavg_k5_alpha05_e1_t3_s0'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Refusing publication because files are already staged' }; $M=Get-Content -LiteralPath "$O/manifest.json" -Raw | ConvertFrom-Json; $Allow=@(); foreach ($N in 1..3) { $P=([string]$M.rounds."$N".result_path).Replace('\','/'); if (-not $P.StartsWith('experiments/federated/results/')) { throw "Unexpected P2.1b result path: $P" }; $R=Split-Path -Parent $P; $Allow+=@("$R/metrics.json","$R/config.json") }; foreach ($P in $Allow) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P2.1b result: $P" } }; git add -- $Allow; if ($LASTEXITCODE -ne 0) { throw 'P2.1b git add failed' }; $Staged=@(git diff --cached --name-only); if (@(Compare-Object ($Allow | Sort-Object) ($Staged | Sort-Object)).Count -ne 0) { throw 'P2.1b staged allowlist mismatch' }; git commit -m 'results: add BIRD v2 pure-FL training'; if ($LASTEXITCODE -ne 0) { throw 'P2.1b commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'P2.1b push failed' }
```

## Next activation rule

P2.1a/P2.1b may train now because evaluator selection does not affect their
checkpoints. Do not publish any BIRD EX table until P2.0d is closed. Do not run
teacher-target generation or FedLS until base, centralized E1/E2, and FL T1-T3
have been evaluated under the same official evaluator contract.
