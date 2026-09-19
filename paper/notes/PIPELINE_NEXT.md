# FedLS-SQL — active protocol-v2 queue

## P2.4c cancellation — 2026-09-17

User cancelled CE2/Hinton2 for cost, not because of a negative result. Server
termination is unconfirmed: press Ctrl+C once in each K2 terminal and wait for
both Python processes to exit. Preserve checkpoints and the original cache.
[Old K2 commands](../archive/completed_runbooks/P24C_CANCELLED_2026-09-17.md)
are historical only; do not launch terminal A or publish incomplete outputs.

## P2.5 — SeqKD versus KID

| Lane | GPU | Endpoint 1 | Endpoint 2 |
|---|---|---|---|
| SeqKD | 0 | A → SeqKD → eval | → A → eval |
| KID | 1 | A → KID → eval | → A → eval |

### What is held fixed

- Parent: published Spider-private FL T1
  (`federated__fedavg__s0__935d572565cc__154540d3__r1`).
- Public prompts: the same 5,319 selected BIRD row identities, with evidence.
- Models: Qwen2.5-1.5B student; frozen Qwen2.5-Coder-7B teacher (4-bit).
- Training: LoRA r16, lr 2e-4, grad accum 16, max length 7,168, seed 0, one
  public pass.
- **SeqKD endpoint 1** reuses the published adapter
  `federated__fedavg_pub__s0__2b42f25abe82__9c5906d8__r1` (CE on teacher SQL).
  The runner verifies its parent, pool, and recipe, then evaluates it again
  under a single-arm contract. The earlier headline evaluation of this adapter
  (57.93/46.65/48.26/45.61/34.68) is a drift check.
- **KID endpoint 1** uses the row-matched clean BIRD gold SQL for those prompts:
  random-mask 20% of target tokens, one dropout-free student fill pass, splice
  predictions into the clean SQL, then optimize clean-target CE plus reverse
  `KL(student || teacher)` on rewritten prefixes at T=1. The teacher is online;
  no autoregressive rollout or fixed logit cache is used.
- **Endpoint 2** for both lanes is the same Spider-private A: 5 clients, one
  local epoch, plaintext FedAvg.
- **Evaluation**: Spider, Realistic, SYN, DK, BIRD; batch 16; greedy; k=0.
- SeqKD and KID share prompts but not targets/objectives. Their comparison is
  end-to-end; a clean-RKL arm is required later to isolate KID rewriting if KID
  passes this gate.
- Wall time from concurrent lanes is not paper-eligible.
- Gap: matched-gold CE on these 5,319 rows has only a batch-8 Spider evaluation.
  It is not a five-set or terminal control in this queue.

### Implementation state

GKD was cancelled before publication because its autoregressive online rollout
was too costly for the available server. Do not publish or resume GKD artifacts.
The nested repo implements `stage public --server-method kid` and the updated
`scripts/run_p25_kd_comparison.py`. Local validation:

- 461 tests pass.
- A CPU end-to-end KID run checks mask/rewrite alignment, clean CE, rewritten
  reverse KL, and optimizer behavior.
- A resumed run after a simulated crash produces an adapter identical to an
  uninterrupted run.
- Method-specific fields are written only to their own result rows; published
  CE/Hinton/FL identities remain unchanged.

Required nested commit: `a9b8621`.

### Step 0 — sync the server once

First stop the cancelled GKD process with Ctrl+C and wait for Python to exit.
Do not pull while it is still running.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed; inspect git status' }; git merge-base --is-ancestor a9b8621 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Nested commit a9b8621 is missing from this checkout' }; uv run --extra dev pytest -q tests/test_kid.py tests/test_p25_runner.py tests/test_stage_chain.py tests/test_round_loop.py; if ($LASTEXITCODE -ne 0) { throw 'P2.5 SeqKD/KID tests failed on the server' }; git log -1 --oneline
```

### Step 1 — run both lanes at the same time

GPU 0 — SeqKD: evaluate endpoint 1, train terminal A, evaluate endpoint 2.

This does not retrain public SeqKD. It reuses the published 5,319-row SeqKD
adapter, evaluates it under the P2.5 single-arm contract, then trains and
evaluates only the previously missing terminal private A stage.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase seqkd-flow; if ($LASTEXITCODE -ne 0) { throw 'SeqKD lane stopped; fix the reported cause, then rerun this exact line' }; Write-Host 'GPU-0 done: existing SeqKD public adapter evaluated and terminal A completed'
```

GPU 1 — KID: fresh 32-row smoke, budget gate, full KID, evaluate endpoint 1.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase kid-public --max-estimated-hours 12; if ($LASTEXITCODE -ne 0) { throw 'KID lane stopped; if the budget gate stopped it, review the fresh smoke estimate before raising --max-estimated-hours' }; Write-Host 'GPU-1 done: KID endpoint 1 evaluated; publish KID public next'
```

- **Smoke:** runs in a new KID-only root and prints seconds per example, setup
  time, rewritten-token count, memory, loss, and a 5,319-row estimate. A resumed
  smoke is not accepted for the budget estimate.
- **Budget gate:** above 12 hours the lane stops before full training. For
  reference, KID adds one student rewrite pass and online teacher scoring but
  no autoregressive rollout. To continue after review, rerun the same line with
  a larger `--max-estimated-hours`; the completed fresh smoke is reused. Once full KID
  has started, the gate is not applied again.
- **Resume:** both lines are resumable. Rerun the exact line after an
  interruption. A completed evaluation is reused when evaluation code is
  unchanged since it ran; publication commits do not force re-evaluation.

### Step 2a — publish KID endpoint 1 independently

Run after `kid-public` is complete, even if `seqkd-flow` has not run. This
publishes only the KID smoke, KID public training row, and its five evaluation
sets. It takes only the KID lane lock and makes the committed KID parent
available for terminal A.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase publish-kid-public; if ($LASTEXITCODE -ne 0) { throw 'KID public publication stopped; inspect git status and retry this exact line' }
```

### Step 3 — KID endpoint 2 on GPU 1

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase kid-terminal; if ($LASTEXITCODE -ne 0) { throw 'KID terminal lane stopped; rerun this exact line' }; Write-Host 'GPU-1 done: KID endpoint 2 evaluated; publish next'
```

### Step 4 — publish KID endpoint 2

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase publish-final; if ($LASTEXITCODE -ne 0) { throw 'Publication stopped; inspect git status and the message before retrying' }
```

### Step 5 — publish the combined comparison after SeqKD finishes

Run after `seqkd-flow` is complete. This publishes the existing SeqKD public
row, the new single-arm SeqKD evaluations, terminal SeqKD row/evaluations, and
verifies the already published KID public endpoint. Unchanged KID files are not
committed twice.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase publish-first; if ($LASTEXITCODE -ne 0) { throw 'SeqKD comparison publication stopped; inspect git status and retry this exact line' }
```

### Decision after P2.5

Report the following, all seed 0:

- KID − SeqKD at endpoint 1 and at endpoint 2 on all five sets.
- Paired wins/losses with exact McNemar p-values.
- Spider-family mean.
- Retention: endpoint 2 − endpoint 1.
- KID cost reported separately: seconds per example and rewritten-token count.
- If KID passes, run matched clean RKL before attributing its gain to imperfect
  rewriting. If it does not pass, keep SeqKD and close online KID.

Do not relabel historical RKD/KID as protocol-v2 evidence. Depth, recurrence,
and other KD variants stay deferred until this comparison is reviewed.
