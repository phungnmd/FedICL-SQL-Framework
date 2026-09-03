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
| P2.1 | Dataset-correct base/centralized/FL baselines | GPU | blocked by P2.0c-d |
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

## Next activation rule

Do not add a GPU command until P2.0c and P2.0d are closed. The first GPU task
will be a small BIRD-with-evidence base/centralized smoke, followed by the pure
FL baseline. Teacher-target generation and FedLS reruns come only after those
baselines establish that train and eval use the same dataset-correct prompt.
