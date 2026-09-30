# P2.10 original design and runbook — superseded 2026-09-30

Archived verbatim from the reference section of `paper/notes/PIPELINE_NEXT.md`.
This is historical context, not authorization to rerun stages or expand P2.10.
The [active queue](../../notes/PIPELINE_NEXT.md) owns remaining commands and decisions;
its optional `tsql` terminal policy overrides the original four-arm commands below.

## P2.10 reference — Struct-SQL design and original runbook (steps 0–5 done)

**What it tests.** Struct-SQL distils a teacher's query plan (QP-CoT) together
with its SQL. P2.10 uses that format in **every** stage, so training and
inference always match:

```text
A[qp]  FL round 1 from the base model; clients train a QP-CoT template of their own SQL
K      public BIRD stage (1,000 rows), early stopping on ID+OOD validation loss
A[qp]  terminal private stage (with retention if P2.9 says so)
eval   the student writes the plan, then the SQL
```

| Arm | Public stage | Question it answers |
|---|---|---|
| `fl` | none | FL control in the same format |
| `gold` | template plan + BIRD gold SQL | training without a teacher |
| `tsql` | template plan + teacher SQL | value of the teacher's SQL |
| `teacher` | teacher plan + teacher SQL | **Struct-SQL method** |

Primary decision: terminal `teacher − gold`, same gate as before (BIRD ≥ +1.0,
Spider-family mean ≥ +0.5, no Spider-family set below −1.0).

**What matches the paper, and what does not.** Matches: the QP-CoT layout and
student instruction, joint teacher plan+SQL generation, execution-only
admission, 75/25 ID/OOD database split, stratified 1,000 training rows,
150+150 validation rows, completion loss, lr 1e-4, effective batch 6, early
stopping on the aggregated validation loss, and the same format at inference.
Differs on purpose:
- LoRA rank stays 16, because every FL stage exchanges the adapter.
- The teacher prompt is zero-shot, not 2-shot.
- The paper does not report its validation cadence. P2.10 evaluates twice per
  epoch, with patience 2 and at most 4 epochs.
- BIRD has too few subquery-only rows for the paper's 22.9% quota. The
  shortfall moves to the next stratum and is recorded.

**Estimated GPU budget (one A5000).** These estimates are based on measured
SQL-only speeds. Re-estimate after the FL round.

| Step | Work | Time |
|---|---|---:|
| Teacher generation | about 2,400 QP-CoT answers | 5–7 h |
| FL `A[qp]` round 1 | 8,659 Spider rows | about 3 h |
| Public stage, per arm (×3) | 1,000 BIRD rows, ≤4 epochs, 300 validation rows | 3.5–5.5 h |
| Terminal `A[qp]`, per arm (×4) | 8,659 Spider rows | about 3 h (about 4 h with retention) |
| Terminal evaluation, per arm (×4) | 5 sets, 4,645 prompts, plan+SQL output | 4–6 h |
| Public evaluation, `teacher`, `tsql`, `gold` | Spider + BIRD | 2.5–3.5 h each |

The total is about 68 GPU-hours, which is about 35 hours on two GPUs. The
`tsql` public evaluation is included so that `teacher − tsql` (the value of
the teacher's plan) is also read before the terminal stage. Every
stage uses the target-window fp32 loss (`--lm-loss target_fp32`) and gradient
checkpointing.

Required nested commit: `d66af7a` or a descendant on
`experiment/terminal-retention`. `$L = 0` (plain terminal `A[qp]`), because
P2.9 is paused. The runner locks `$L` at the first terminal stage, so every
arm must use the same value.

### Step 0 — sync and validate

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor d66af7a HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required P2.10 code commit is missing' }; uv run --extra dev python -m pytest -q tests/test_struct_sql_qp_cot.py tests/test_rationale_scripts.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_round_loop.py tests/test_training.py tests/test_eval.py; if ($LASTEXITCODE -ne 0) { throw 'P2.10 validation failed' }; git log -1 --oneline
```

### Step 1 — CPU: candidates and client length audit

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p210_struct_sql.py --phase prepare; if ($LASTEXITCODE -ne 0) { throw 'Candidate split failed' }; uv run python scripts/run_p210_struct_sql.py --phase audit --scope clients; if ($LASTEXITCODE -ne 0) { throw 'Client length audit failed' }
```

### Step 2 — two GPU lanes in parallel

GPU 0 generates the teacher answers. GPU 1 trains the FL parent at the same
time, because FL needs only the private clients.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p210_struct_sql.py --phase generate; if ($LASTEXITCODE -ne 0) { throw 'Teacher generation failed' }; uv run python scripts/run_p210_struct_sql.py --phase pools; if ($LASTEXITCODE -ne 0) { throw 'Pool construction failed' }; uv run python scripts/run_p210_struct_sql.py --phase audit --scope pools; if ($LASTEXITCODE -ne 0) { throw 'Pool length audit failed' }
```

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p210_struct_sql.py --phase train-fl; if ($LASTEXITCODE -ne 0) { throw 'FL A[qp] failed' }
```

### Step 3 — commit the FL parent row

Later stages refuse uncommitted parents. Run this with no GPU job writing
results.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $Rel=@(uv run python scripts/list_p210_publication.py --rows fl); if ($LASTEXITCODE -ne 0) { throw 'FL row lookup failed' }; git add -- $Rel; git commit -m 'results: P2.10 FL A[qp] parent row'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin experiment/terminal-retention
```

### Step 4 — public stages (and the FL terminal) on two GPUs

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; foreach ($A in 'teacher','tsql') { uv run python scripts/run_p210_struct_sql.py --phase train-public --arm $A; if ($LASTEXITCODE -ne 0) { throw "Public $A failed" } }
```

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $L='0'; uv run python scripts/run_p210_struct_sql.py --phase train-terminal --arm fl --retention-lambda $L; if ($LASTEXITCODE -ne 0) { throw 'Terminal fl failed' }; uv run python scripts/run_p210_struct_sql.py --phase train-public --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Public gold failed' }
```

Then commit the three public rows:

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $Rel=@(uv run python scripts/list_p210_publication.py --rows public); if ($LASTEXITCODE -ne 0) { throw 'Public row lookup failed' }; git add -- $Rel; git commit -m 'results: P2.10 public stage rows'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin experiment/terminal-retention
```

### Step 5 — terminal stages and evaluation on two GPUs

Use the same `$L` as in Step 4. The runner refuses a different value.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $L='0'; foreach ($A in 'teacher','tsql') { uv run python scripts/run_p210_struct_sql.py --phase train-terminal --arm $A --retention-lambda $L; if ($LASTEXITCODE -ne 0) { throw "Terminal $A failed" }; uv run python scripts/run_p210_struct_sql.py --phase eval --arm $A --endpoint terminal; if ($LASTEXITCODE -ne 0) { throw "Eval $A failed" } }; foreach ($A in 'teacher','tsql') { uv run python scripts/run_p210_struct_sql.py --phase eval --arm $A --endpoint public; if ($LASTEXITCODE -ne 0) { throw "Public eval $A failed" } }
```

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $L='0'; uv run python scripts/run_p210_struct_sql.py --phase train-terminal --arm gold --retention-lambda $L; if ($LASTEXITCODE -ne 0) { throw 'Terminal gold failed' }; foreach ($A in 'gold','fl') { uv run python scripts/run_p210_struct_sql.py --phase eval --arm $A --endpoint terminal; if ($LASTEXITCODE -ne 0) { throw "Eval $A failed" } }; uv run python scripts/run_p210_struct_sql.py --phase eval --arm gold --endpoint public; if ($LASTEXITCODE -ne 0) { throw 'Public eval gold failed' }
```

### Step 6 — analysis and publication

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p210_struct_sql.py --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.10 analysis failed' }; Get-Content audits/protocol_v2/p210_struct_sql_s0/summary.md; $Rel=@(uv run python scripts/list_p210_publication.py); if ($LASTEXITCODE -ne 0) { throw 'P2.10 allowlist failed' }; git add -- $Rel; git diff --cached --check; if ($LASTEXITCODE -ne 0) { throw 'Staged content check failed' }; git commit -m 'results: publish P2.10 Struct-SQL lineage'; git push origin experiment/terminal-retention
```

After an interruption, rerun the same lane command. Completed stages and
evaluations are skipped. A public stage resumes with its validation history.

### Decision after P2.10

The 1,000-row quota is a deliberate screen, matching the paper's curated set
and the A5000 budget (about 2,400 teacher generations). If terminal
`teacher − gold` passes the gate:

1. Run independent seeds for `teacher` and `gold`.
2. Run a full-pool extension for those two arms: every admitted ID-pool row,
   with the same 150+150 validation rows. This tests whether more teacher data
   adds more. It needs a small "all admitted rows" mode in
   `build_rationale_candidates.py --algorithm struct_sql_v1`, which is not
   implemented yet. The teacher cache reuses every P2.10 generation, so only
   the missing rows are generated.

If the gate fails, do not scale up. The screen already answers the question.

### Deferred teacher options (use only if the teacher is the bottleneck)

P2.10 keeps the teacher frozen and zero-shot. This matches Struct-SQL, whose
GPT-4o teacher is also frozen and only prompted. The two options below
strengthen the teacher later. The zero-shot P2.10 run stays as the baseline row
of the teacher-prompt ablation.

1. **Few-shot teacher (first choice).** Use Struct-SQL's 2-shot QP-CoT prompt.
   Take the demonstrations from BIRD train rows of OOD databases that are not
   in the validation sets, with plans written by the `qp_ast_v1` template.
   - The teacher stays frozen.
   - The prompt is about 1.5k tokens longer, so generation takes about
     20–30% more time.
   - This is a new generation-cache identity. The zero-shot cache is kept.
   - Ablation: zero-shot versus 2-shot teacher. Report admission rate, teacher
     EX on the admitted pool, and terminal `teacher − gold`.
   - Trigger: a low admission rate, a poor plan-format rate, or
     `teacher − gold` failing while the student already matches teacher EX.
2. **Trained teacher (later ablation).** QLoRA-tune the 7B teacher on public
   BIRD rows with cross-fitting: train on one half and label the other, then
   swap. A teacher trained on the same gold rows would copy gold, and the
   teacher-versus-gold contrast would collapse. This option also fits the
   unlabeled-public-pool framing. It is heavy on an A5000 because prompts reach
   7k tokens.

Not implemented yet; neither option runs before P2.10 reports.
