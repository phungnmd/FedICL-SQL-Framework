# FedLS-SQL — active protocol-v2 queue

## Current decision

Run **P2.9, the terminal-retention gate**, before any more structured-rationale
(Struct-SQL) work. The P2.8 matched-gold structured gate is deferred, not
closed. Its full runbook is preserved in
[P28_STRUCT_GOLD_GATE_DEFERRED_2026-09-24.md](../archive/superseded_runbooks/P28_STRUCT_GOLD_GATE_DEFERRED_2026-09-24.md).

Why P2.9 comes first: the committed P2.6 predictions, re-analyzed on
2026-09-24 (see `LAB_LOG.md`), show that SeqKD beats row-matched gold CE on
all five sets at the **public** endpoint, with the largest gains on the
out-of-domain sets:

| SeqKD − matched gold (EX) | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| after K (public) | +1.64 | +2.76 | **+3.38** | +2.43 | **+3.00** |
| after plain terminal A | −0.10 | −0.98 | +1.64 | +0.75 | +0.91 |

Bold values have exact McNemar p < .01. The terminal private stage removes most
of the edge. If a retention term keeps the edge after terminal A, the paper gets
a positive teacher-specific claim: KD transfers BIRD knowledge to Spider with
less negative transfer than gold training. Any structured-rationale arm then
builds on that terminal stage.

## What P2.9 trains

Two new terminal stages. Everything else is reused from committed results.

| Arm | Parent (committed public row) | New stage | Loss at each client |
|---|---|---|---|
| seqkd | SeqKD on 5,319 teacher SQL rows (`2b42f25`) | `A>K[ce]>A[ret]` | Spider CE + 1.0 · KL(post-K model ‖ student) |
| gold | CE on the same rows with source gold SQL (`4d679d6`) | `A>K[ce]>A[ret]` | same |

- The terminal recipe matches P2.5/P2.6 exactly: 5 clients, 1 local epoch,
  FedAvg, same Spider split, same training flags. The only change is the
  retention term.
- Retention reference = the frozen post-K global adapter. No teacher runs at
  the clients, and communication is unchanged.
- KL covers only SQL target tokens, at T = 1. The reference is a second frozen
  1.5B copy, which adds about 3 GiB of VRAM.
- A diagnostic also scores the pure-FL student's NLL on teacher SQL versus gold
  SQL for the same 5,319 BIRD prompts. It tests the "teacher SQL is closer to
  the student's distribution" explanation.

Required nested branch: `experiment/terminal-retention`, commit `70a5410` or a
descendant. It descends from the P2.8 commit, so P2.8 can resume from it later.
Commit `70a5410` also adds an opt-in faster student CE path (`--lm-loss
target_fp32`) and its benchmark. P2.9 does **not** use it. All P2.9 arms stay
on the published `full_bf16` path so they remain row-comparable with P2.6.

## Step 0 — sync and validate on the Windows server

Run from the `fedicl-sql/` repository root. Do not pull while a GPU lane runs.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git fetch origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch fetch failed' }; git switch experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch switch failed' }; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch pull failed' }; git merge-base --is-ancestor 70a5410 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required P2.9 code commit is missing' }; $Scope=@('fedicl_sql','experiments','scripts','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=all -- $Scope | Where-Object { $Path=$_.Substring(3).Trim('"').Replace('\','/'); $Path -notmatch '^experiments/[^/]+/results/' }); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code scope is dirty' }; uv run --extra dev python -m pytest -q tests/test_p29_retention_gate.py tests/test_stage_chain.py tests/test_round_loop.py tests/test_training.py tests/test_eval.py tests/test_eval_arms_config.py tests/test_eval_arms_cli.py; if ($LASTEXITCODE -ne 0) { throw 'P2.9 validation failed' }; git log -1 --oneline
```

## Step 1 — GPU 0: smoke (a few minutes)

Four client steps of the seqkd arm. The smoke checks that the reference model
loads, the retention KL is finite and small, and VRAM stays below about
21 GiB. Above that, WDDM pages to host RAM instead of raising OOM, so the run
slows down rather than failing. The smoke root is separate from the real run.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p29_retention_gate.py --phase smoke; if ($LASTEXITCODE -ne 0) { throw 'P2.9 smoke failed' }
```

Continue if every client line shows `peak_reserved_mb` below about 21500 and a
finite `retention_kl`. If VRAM is higher, stop and report the printed lines.

## Step 2 — two GPU lanes

Start both lanes after the smoke passes. Their training and evaluation roots
are disjoint, and a file lock protects the shared manifest. After an
interruption, rerun the exact lane command. Completed clients, stages, and
evaluations are skipped. Each terminal stage took 1.6–2.5 h without retention.
Expect about 30–50% more time with the reference forward pass, plus the
five-set evaluation.

GPU 0 — SeqKD parent:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p29_retention_gate.py --phase train --arm seqkd; if ($LASTEXITCODE -ne 0) { throw 'SeqKD A[ret] failed' }; uv run python scripts/run_p29_retention_gate.py --phase eval --arm seqkd; if ($LASTEXITCODE -ne 0) { throw 'SeqKD A[ret] evaluation failed' }; Write-Host 'GPU-0 complete: seqkd A[ret] trained and evaluated on five sets'
```

GPU 1 — matched-gold parent, then the NLL diagnostic:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p29_retention_gate.py --phase train --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Gold A[ret] failed' }; uv run python scripts/run_p29_retention_gate.py --phase eval --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Gold A[ret] evaluation failed' }; uv run python scripts/run_p29_retention_gate.py --phase nll; if ($LASTEXITCODE -ne 0) { throw 'Target NLL diagnostic failed' }; Write-Host 'GPU-1 complete: gold A[ret] evaluated; target NLL scored'
```

## Step 3 — CPU: paired analysis and decision

Run after both lanes finish. The analysis reports, for each of the five sets:
SeqKD − gold at the public, plain-terminal, and retention-terminal endpoints;
the effect of retention within each arm; EX; and the execution-error rate.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p29_retention_gate.py --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.9 analysis failed' }; Get-Content audits/protocol_v2/p29_retention_terminal_s0/summary.md; Get-Content audits/protocol_v2/p29_retention_terminal_s0/target_nll_pure_fl_t1/summary.json
```

Registered seed-0 gate for `A>K>A[ret]`, SeqKD − gold:

1. BIRD ≥ +1.5 EX. This keeps about half of the public-endpoint +3.00.
2. Spider-family mean (Spider, Realistic, SYN, DK) ≥ +1.0 EX. The public
   endpoint gives +2.55; plain terminal A gives +0.33.
3. No Spider-family set below −1.0 EX.
4. Retention does not block the Spider repair: SeqKD `A[ret]` Spider EX is at
   most 1.0 below SeqKD plain terminal (64.99).

## Step 4 — publish compact P2.9 evidence

Run after Step 3 succeeds and no GPU process uses this worktree. This publishes
two stage rows, ten evaluation triplets, the NLL audit, and the summary: 40
files. Adapters, caches, and the smoke row are excluded.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $Rel=@(uv run python scripts/list_p29_publication.py); if ($LASTEXITCODE -ne 0 -or $Rel.Count -ne 40) { throw "P2.9 publication allowlist invalid: files=$($Rel.Count)" }; git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'P2.9 staging failed' }; $Got=@(git diff --cached --name-only | Sort-Object); $Want=@(git diff HEAD --name-only -- $Rel | Sort-Object); if ($Got.Count -ne $Want.Count -or @(Compare-Object $Got $Want).Count -ne 0) { throw 'P2.9 staged allowlist mismatch' }; if ($Got.Count -gt 0) { git diff --cached --check; if ($LASTEXITCODE -ne 0) { throw 'P2.9 staged content check failed' }; git commit -m 'results: publish P2.9 terminal retention gate'; if ($LASTEXITCODE -ne 0) { throw 'P2.9 commit failed' }; git push origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'P2.9 push failed' } } else { Write-Host 'P2.9 evidence already committed' }; git log -1 --oneline
```

## Step 5 (optional) — benchmark the faster student CE path

Run only when no other GPU job is active, because timing needs exclusive
hardware. It trains nothing and writes one JSON report. It compares the current
path (`full_bf16` with gradient checkpointing) against `target_fp32` with and
without checkpointing. Rows: the 8 longest plus 24 random rows from the five
Spider clients, warm-started from the SeqKD public adapter.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; uv run python scripts/benchmark_student_loss.py --client-csv "$S/client_1_train.csv" "$S/client_2_train.csv" "$S/client_3_train.csv" "$S/client_4_train.csv" "$S/client_5_train.csv" --adapter artifacts/protocol_v2/p22_spider_private_t1/seqkd_s0/round_1/m_g --out audits/protocol_v2/student_loss_benchmark_s0.json; if ($LASTEXITCODE -ne 0) { throw 'Student loss benchmark failed' }
```

Report the three printed lines. The new path is worth adopting for the next
full lineage only if all three hold:

- `max_abs_loss_delta_vs_baseline` is small (below about 0.01);
- the no-checkpointing variant stays below about 21500 MB peak reserved;
- it is clearly faster per row.

Adopt it only for a whole new comparison ladder, never inside P2.9 or its
seed replicates.

## Decision after P2.9

- **`promote_multiseed_then_structured`** (all four gates pass): the KD
  generalization edge survives deployment. Next steps, in order:
  1. Seeds 1–2 for the four terminal arms (seqkd/gold × plain/ret).
  2. An out-of-domain evaluation set that terminal A cannot repair
     (KaggleDBQA).
  3. Run P2.10 below (Struct-SQL lineage) with `$L = 1.0` retention at the
     terminal stage.
- **`retention_blocks_spider_repair_retune_lambda`** (gates 1–3 pass, gate 4
  fails): the retention term is too strong. Screen a lower λ (for example 0.3)
  on the same two parents before anything else, then run P2.10 with that λ.
- **`close_terminal_retention_hypothesis`**: retention does not keep the edge.
  The flat-KD generalization claim then stands only at the public endpoint.
  Run P2.10 below with `$L = 0` (plain terminal A). P2.10 supersedes the
  deferred P2.8 gate, whose final endpoint is SQL-only. Reconsider the
  unlabeled-public-pool framing for the paper headline.

Whatever the decision, the NLL diagnostic is reported as mechanism evidence.
If teacher SQL has lower student NLL than gold SQL, that supports the
distribution-gap explanation. If it does not, the edge needs another
explanation, such as gold-label noise removed by the execution filter.

## P2.10 — Struct-SQL lineage (prepared; start only after P2.9 decides)

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
| Public evaluation, `teacher` and `gold` | Spider + BIRD | 2.5–3.5 h each |

The total is about 65 GPU-hours, which is about 34 hours on two GPUs. Every
stage uses the target-window fp32 loss (`--lm-loss target_fp32`) and gradient
checkpointing.

Required nested commit: `d66af7a` or a descendant on
`experiment/terminal-retention`. Set `$L` from the P2.9 decision: `1.0`, the
retuned λ, or `0`.

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
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $L='1.0'; uv run python scripts/run_p210_struct_sql.py --phase train-terminal --arm fl --retention-lambda $L; if ($LASTEXITCODE -ne 0) { throw 'Terminal fl failed' }; uv run python scripts/run_p210_struct_sql.py --phase train-public --arm gold; if ($LASTEXITCODE -ne 0) { throw 'Public gold failed' }
```

Then commit the three public rows:

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $Rel=@(uv run python scripts/list_p210_publication.py --rows public); if ($LASTEXITCODE -ne 0) { throw 'Public row lookup failed' }; git add -- $Rel; git commit -m 'results: P2.10 public stage rows'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin experiment/terminal-retention
```

### Step 5 — terminal stages and evaluation on two GPUs

Use the same `$L` as in Step 4. The runner refuses a different value.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $L='1.0'; foreach ($A in 'teacher','tsql') { uv run python scripts/run_p210_struct_sql.py --phase train-terminal --arm $A --retention-lambda $L; if ($LASTEXITCODE -ne 0) { throw "Terminal $A failed" }; uv run python scripts/run_p210_struct_sql.py --phase eval --arm $A --endpoint terminal; if ($LASTEXITCODE -ne 0) { throw "Eval $A failed" } }; uv run python scripts/run_p210_struct_sql.py --phase eval --arm teacher --endpoint public; if ($LASTEXITCODE -ne 0) { throw 'Public eval teacher failed' }
```

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $L='1.0'; uv run python scripts/run_p210_struct_sql.py --phase train-terminal --arm gold --retention-lambda $L; if ($LASTEXITCODE -ne 0) { throw 'Terminal gold failed' }; foreach ($A in 'gold','fl') { uv run python scripts/run_p210_struct_sql.py --phase eval --arm $A --endpoint terminal; if ($LASTEXITCODE -ne 0) { throw "Eval $A failed" } }; uv run python scripts/run_p210_struct_sql.py --phase eval --arm gold --endpoint public; if ($LASTEXITCODE -ne 0) { throw 'Public eval gold failed' }
```

### Step 6 — analysis and publication

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p210_struct_sql.py --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.10 analysis failed' }; Get-Content audits/protocol_v2/p210_struct_sql_s0/summary.md; $Rel=@(uv run python scripts/list_p210_publication.py); if ($LASTEXITCODE -ne 0) { throw 'P2.10 allowlist failed' }; git add -- $Rel; git diff --cached --check; if ($LASTEXITCODE -ne 0) { throw 'Staged content check failed' }; git commit -m 'results: publish P2.10 Struct-SQL lineage'; git push origin experiment/terminal-retention
```

After an interruption, rerun the same lane command. Completed stages and
evaluations are skipped. A public stage resumes with its validation history.
