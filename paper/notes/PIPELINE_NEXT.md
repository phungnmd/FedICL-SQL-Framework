# FedLS-SQL — active protocol-v2 queue

> Run from the `fedicl-sql/` repository root in PowerShell. Commands follow
> `CONVENTION.MD` §6.1: one physical line, fail-fast, immutable roots, exact
> resume, and a separate allowlisted publication command. Protocol-v1 commands
> are archived and must not be rerun into their old roots.

## Active order

| Order | Task | Device | Status |
|---|---|---|---|
| P2.0a | Audit current Spider and original-BIRD processed pairs under explicit profiles | CPU | ready |
| P2.0b | Review server artifact retirement manifest | CPU | after P2.0a; dry-run only |
| P2.0c | Import/freeze official filtered BIRD train and chosen dev release | CPU | ingestion implemented; files/checksums pending |
| P2.0d | Add official BIRD evaluator adapter and known-answer fixture | CPU | implementation gate |
| P2.1 | Dataset-correct base/centralized/FL baselines | GPU | blocked by P2.0c-d |
| P2.2 | Rerun current FedLS reference ladder in both directions | GPU | blocked by P2.1 |
| P2.3 | Diagnose and improve KD/Federated method | adaptive | blocked by P2.2 |

The method is deliberately not frozen. P2.2 measures the previous design as a
reference; P2.3 may change hard/soft KD, selection, aggregation, local
optimization, public budget, or evidence use when a matched diagnostic supports
the change.

## P2.0a — processed-data and prompt contract audit

This is zero-GPU and does not regenerate data. It verifies explicit profiles,
source hashes, evidence coverage, prompt inclusion, and zero train/test database
overlap. The original 9,428-row BIRD release is audited only to establish a
reproducible compatibility baseline; it is not yet the chosen canonical v2
training release.

```powershell
$Expected='fc0925b'; $Head=(git rev-parse --short HEAD).Trim(); if ($Head -ne $Expected) { throw "P2.0a requires code $Expected, found $Head; pull while no experiment is running" }; $Dirty=@(git status --porcelain -- fedicl_sql experiments scripts tests uv.lock pyproject.toml processed_data/SPIDER/centralized/train.csv processed_data/SPIDER/centralized/test.csv processed_data/BIRD/centralized/train.csv processed_data/BIRD/centralized/test.csv); if ($Dirty.Count -ne 0) { $Dirty; throw 'P2.0a scientific scope is dirty' }; uv run pytest -q tests/test_data_protocol.py tests/test_prompts.py tests/test_training.py tests/test_eval_arms_config.py tests/test_logit_cache.py tests/test_round_loop.py tests/test_bird_data.py; if ($LASTEXITCODE -ne 0) { throw 'Protocol-v2 tests failed' }; uv run python scripts/audit_protocol_v2.py --train-csv processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --dataset-profile spider --dataset-version spider-original --schema-style full --out audits/protocol_v2/spider_original.json; if ($LASTEXITCODE -ne 0) { throw 'Spider protocol-v2 audit failed' }; uv run python scripts/audit_protocol_v2.py --train-csv processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --dataset-profile bird_with_evidence --dataset-version bird-original-train9428-dev1534 --schema-style full --out audits/protocol_v2/bird_original.json; if ($LASTEXITCODE -ne 0) { throw 'BIRD protocol-v2 audit failed' }; $S=Get-Content -LiteralPath audits/protocol_v2/spider_original.json -Raw | ConvertFrom-Json; $B=Get-Content -LiteralPath audits/protocol_v2/bird_original.json -Raw | ConvertFrom-Json; if ($S.database_overlap.Count -ne 0 -or $B.database_overlap.Count -ne 0 -or $B.train.rows -ne 9428 -or $B.test.rows -ne 1534 -or $B.train.evidence_populated -le 0 -or -not $B.prompt_probe.has_evidence_section) { throw 'P2.0a acceptance contract failed' }; Write-Host "P2.0a passed: Spider=$($S.train.rows)/$($S.test.rows), BIRD=$($B.train.rows)/$($B.test.rows), BIRD evidence=$($B.train.evidence_populated)"
```

Publication command:

```powershell
$Files=@('audits/protocol_v2/spider_original.json','audits/protocol_v2/bird_original.json'); git diff --cached --quiet; if ($LASTEXITCODE -ne 0) { throw 'Staged changes already exist' }; foreach ($P in $Files) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P2.0a output: $P" } }; git add -- $Files; if ($LASTEXITCODE -ne 0) { throw 'P2.0a git add failed' }; $Want=@($Files | Sort-Object); $Got=@(git diff --cached --name-only | Sort-Object); if (($Want -join '|') -ne ($Got -join '|')) { throw "Unexpected staged paths: $($Got -join ',')" }; git commit -m 'audit: freeze protocol v2 source datasets'; if ($LASTEXITCODE -ne 0) { throw 'P2.0a commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'P2.0a push failed' }; Write-Host 'P2.0a audit artifacts pushed; stop for review before P2.0b/P2.0c'
```

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

## Next activation rule

Do not add a GPU command until P2.0c and P2.0d are closed. The first GPU task
will be a small BIRD-with-evidence base/centralized smoke, followed by the pure
FL baseline. Teacher-target generation and FedLS reruns come only after those
baselines establish that train and eval use the same dataset-correct prompt.
