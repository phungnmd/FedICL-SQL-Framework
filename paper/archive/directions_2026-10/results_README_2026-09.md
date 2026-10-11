# FedLS-SQL paper results

This directory owns paper-facing result tables.

The August 19 PDF outline is a revisable planning document. It can suggest
candidate tables, but it does not freeze the experiment matrix, table schema, or
paper claims.

- `MAIN_RESULTS.md` is the single source of truth for values presented in the
  manuscript, slides, or advisor email.
- `../notes/RESULT_REGISTRY.md` maps stable result IDs to immutable checkpoints
  and committed evaluation artifacts.
- `../notes/LAB_LOG.md` records interpretation and decisions; it does not own
  canonical table values.
- Raw truth remains in `fedicl-sql/experiments/*/results/*/{config,metrics}.json`
  and prediction CSVs.

## Update contract

1. Validate a completed run against its config, metrics, predictions, manifest,
   checkpoint lineage, and Git SHA.
2. Add or update its stable ID in `RESULT_REGISTRY.md`.
3. Update only the affected table in `MAIN_RESULTS.md`.
4. Record the interpretation or gate decision in `LAB_LOG.md`.
5. Never copy a metric from an old model recipe into a new row to fill a blank.

Use `PENDING:<task>` for a scheduled missing result, `NOT RUN` for an absent
comparison, `N/A` when a metric is not applicable, and `—` only when a value is
intentionally not shown. Model family, exact model ID, transfer objective,
round, and training seed must be explicit before two results are compared.
