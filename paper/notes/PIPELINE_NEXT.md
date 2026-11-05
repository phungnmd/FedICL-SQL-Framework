# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). Every command follows
`CONVENTION.MD` section 6.1: one physical PowerShell line, every variable
defined, a throw after any non-zero exit, and a separate publication step.

State 2026-11-04: no GPU run is queued or running. P2.60, P2.62 and the c1
Spider test are published (nested `1eeaa6a`). Earlier runs P2.27-P2.62 are
complete or closed; their commands are preserved in
[PIPELINE_P227_P262_2026-11-04](../archive/completed_runbooks/PIPELINE_P227_P262_2026-11-04.md).

## Waiting for the owner

The next runs depend on the direction choice in [DIRECTION.md](DIRECTION.md).
Nothing below is built yet:

1. Spider test for `s1_rl9`, `sql_rl9` and `sql2_e1` (extend
   `scripts/eval_p262_spider_test.py` beyond `c1_rlN`). Baseline test numbers
   for every direction.
2. Direction D pilot (DIRECTION section 3.5): CoT rescue pairs from `c1_rl8`
   on the questions `s1_rl9` still fails, against gold-chosen and plain SQL
   retry rounds; Spider dev and test (one GPU, about half a day).

## Status check (read-only, any time)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; foreach ($mod in @('run_p260_cot_ceiling','run_p262_rl_from_bird')) { uv run --no-sync python -m "scripts.$mod" --phase status; if ($LASTEXITCODE -ne 0) { throw "Status failed: $mod" } } }
```
