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

Required nested branch: `experiment/terminal-retention`, commit `e72ad2d` or a
descendant. It descends from the P2.8 commit, so P2.8 can resume from it later.

## Step 0 — sync and validate on the Windows server

Run from the `fedicl-sql/` repository root. Do not pull while a GPU lane runs.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git fetch origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch fetch failed' }; git switch experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch switch failed' }; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Feature-branch pull failed' }; git merge-base --is-ancestor e72ad2d HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required P2.9 code commit is missing' }; $Scope=@('fedicl_sql','experiments','scripts','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=all -- $Scope | Where-Object { $Path=$_.Substring(3).Trim('"').Replace('\','/'); $Path -notmatch '^experiments/[^/]+/results/' }); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code scope is dirty' }; uv run --extra dev python -m pytest -q tests/test_p29_retention_gate.py tests/test_stage_chain.py tests/test_round_loop.py tests/test_training.py tests/test_eval.py tests/test_eval_arms_config.py tests/test_eval_arms_cli.py; if ($LASTEXITCODE -ne 0) { throw 'P2.9 validation failed' }; git log -1 --oneline
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

## Decision after P2.9

- **`promote_multiseed_then_structured`** (all four gates pass): the KD
  generalization edge survives deployment. Next steps, in order:
  1. Seeds 1–2 for the four terminal arms (seqkd/gold × plain/ret).
  2. An out-of-domain evaluation set that terminal A cannot repair
     (KaggleDBQA).
  3. Resume the structured-rationale work on top of `A[ret]`, with
     client-side AST plans so that training and inference formats match.
- **`retention_blocks_spider_repair_retune_lambda`** (gates 1–3 pass, gate 4
  fails): the retention term is too strong. Screen a lower λ (for example 0.3)
  on the same two parents before anything else.
- **`close_terminal_retention_hypothesis`**: retention does not keep the edge.
  The flat-KD generalization claim then stands only at the public endpoint.
  Resume P2.8 from the deferred runbook, and reconsider the
  unlabeled-public-pool framing for the paper headline.

Whatever the decision, the NLL diagnostic is reported as mechanism evidence.
If teacher SQL has lower student NLL than gold SQL, that supports the
distribution-gap explanation. If it does not, the edge needs another
explanation, such as gold-label noise removed by the execution filter.
