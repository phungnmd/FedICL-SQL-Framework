# FedLS-SQL run queue

This is the only active command queue. Run from the Windows `fedicl-sql/`
root on `main`. Results: [LAB_LOG.md](LAB_LOG.md). Every command follows
`CONVENTION.MD` section 6.1: one physical PowerShell line, every variable
defined, a throw after any non-zero exit, and a separate publication step.

State 2026-11-05: no GPU run is queued or running. P2.60, P2.62 and the c1
Spider test are published (nested `1eeaa6a`). Earlier runs P2.27-P2.62 are
complete or closed; their commands are preserved in
[PIPELINE_P227_P262_2026-11-04](../archive/completed_runbooks/PIPELINE_P227_P262_2026-11-04.md).

## Waiting for the owner

The next runs follow [DIRECTION.md](DIRECTION.md) section 4 (not approved
yet). Nothing below is built:

1. Step 0, eval only (under 8 GPU-h): Spider test for `s1_rl9`, `sql_rl9`
   and `sql2_e1` (extend `scripts/eval_p262_spider_test.py` beyond `c1_rlN`);
   BIRD dev for `c1_rl8` and `s1_rl9`.
2. Step 1 (about 30 GPU-h, two GPUs): the P2.62 `s1` RL route, with gold as
   chosen on all-wrong questions, started from the three seed 0 A3 adapters
   `hinton_k2aaa`, `gold_k2aaa` and FedAvg A3; fixed round count, Spider dev,
   test and DK per round. Verify on the server that the adapters exist and
   share the `target_fp32` loss mode.
3. Step 1b (about 6 GPU-h, in parallel): one DPO + NLL round from `s1_rl9`
   with `c1` rescued SQL, gold on the same 508 questions, or gold on all 1,200
   as chosen.

## Status check (read-only, any time)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; foreach ($mod in @('run_p260_cot_ceiling','run_p262_rl_from_bird')) { uv run --no-sync python -m "scripts.$mod" --phase status; if ($LASTEXITCODE -ne 0) { throw "Status failed: $mod" } } }
```
