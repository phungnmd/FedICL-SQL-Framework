# FedLS-SQL — active protocol-v2 queue

## P2.4c cancellation — 2026-09-17

User cancelled CE2/Hinton2 for cost, not because of a negative result. Server
termination is unconfirmed: press Ctrl+C once in each K2 terminal and wait for
both Python processes to exit. Preserve checkpoints and the original cache.
[Old K2 commands](../archive/completed_runbooks/P24C_CANCELLED_2026-09-17.md)
are historical only; do not launch terminal A or publish incomplete outputs.

## P2.5 — SeqKD versus GKD

| Lane | GPU | Endpoint 1 | Endpoint 2 |
|---|---|---|---|
| SeqKD | 0 | A → SeqKD → eval | → A → eval |
| GKD | 1 | A → GKD → eval | → A → eval |

### What is held fixed

- Parent: published Spider-private FL T1
  (`federated__fedavg__s0__935d572565cc__154540d3__r1`).
- Public prompts: the same 5,319 selected BIRD rows, with evidence.
- Models: Qwen2.5-1.5B student; frozen Qwen2.5-Coder-7B teacher (4-bit).
- Training: LoRA r16, lr 2e-4, grad accum 16, max length 7,168, seed 0, one
  public pass.
- **SeqKD endpoint 1** reuses the published adapter
  `federated__fedavg_pub__s0__2b42f25abe82__9c5906d8__r1` (CE on teacher SQL).
  The runner verifies its parent, pool, and recipe, then evaluates it again
  under a single-arm contract. The earlier headline evaluation of this adapter
  (57.93/46.65/48.26/45.61/34.68) is a drift check.
- **GKD endpoint 1**:
  - For each 16-prompt update group, the current student samples SQL
    (temperature 1, at most 256 new tokens).
  - The teacher scores those tokens online, and the loss is forward
    `KL(teacher || student)` at T=1.
  - No gold CE, execution filter, or logit cache.
  - The longest audited BIRD prompt is 6,779 tokens, so prompt + 256 fits
    7,168.
- **Endpoint 2** for both lanes is the same Spider-private A: 5 clients, one
  local epoch, plaintext FedAvg.
- **Evaluation**: Spider, Realistic, SYN, DK, BIRD; batch 16; greedy; k=0.
- Wall time from concurrent lanes is not paper-eligible.
- Gap: matched-gold CE on these 5,319 rows has only a batch-8 Spider evaluation.
  It is not a five-set or terminal control in this queue.

### Implementation state

The nested repo implements `stage public --server-method gkd`, the on-policy
GKD trainer, and `scripts/run_p25_kd_comparison.py`. Local validation:

- 448 tests pass.
- A CPU end-to-end GKD run on a tiny Qwen2 checks exact rollout scoring windows.
- A resumed run after a simulated crash produces an adapter identical to an
  uninterrupted run.
- Review (2026-09-17): all 29 published federated rows keep identical setup
  IDs and stage recipes. GKD knobs are written only to GKD rows, so the
  published `A>K[ce]>A` stage still re-enters exactly. Old CE/Hinton
  checkpoint signatures are unchanged.

No GPU run yet. Required nested commit: `0c2ed4c`.

### Step 0 — sync the server once

Run only after both K2 Python processes have exited.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed; inspect git status' }; git merge-base --is-ancestor 0c2ed4c HEAD; if ($LASTEXITCODE -ne 0) { throw 'Nested commit 0c2ed4c is missing from this checkout' }; uv run --extra dev pytest -q tests/test_gkd.py tests/test_p25_runner.py tests/test_stage_chain.py tests/test_round_loop.py; if ($LASTEXITCODE -ne 0) { throw 'P2.5 tests failed on the server' }; git log -1 --oneline
```

### Step 1 — run both lanes at the same time

GPU 0 — SeqKD: evaluate endpoint 1, train terminal A, evaluate endpoint 2.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase seqkd-flow; if ($LASTEXITCODE -ne 0) { throw 'SeqKD lane stopped; fix the reported cause, then rerun this exact line' }; Write-Host 'GPU-0 done: SeqKD endpoints 1 and 2 evaluated; wait for GPU 1 before publication'
```

GPU 1 — GKD: 32-prompt smoke, budget gate, full GKD, evaluate endpoint 1.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase gkd-public --max-estimated-hours 12; if ($LASTEXITCODE -ne 0) { throw 'GKD lane stopped; if the budget gate stopped it, review the smoke estimate before rerunning with a larger --max-estimated-hours' }; Write-Host 'GPU-1 done: GKD endpoint 1 evaluated; wait for GPU 0 before publication'
```

- **Smoke:** runs in its own root and is kept. It prints seconds per prompt,
  setup time, and an estimate for all 5,319 prompts.
- **Budget gate:** above 12 hours the lane stops before full training. For
  reference, SeqKD CE on the same prompts took 5.5 hours; GKD adds rollouts and
  online 7B scoring. To continue after review, rerun the same line with a
  larger `--max-estimated-hours`; the completed smoke is reused. Once full GKD
  has started, the gate is not applied again.
- **Resume:** both lines are resumable. Rerun the exact line after an
  interruption. A completed evaluation is reused when evaluation code is
  unchanged since it ran; publication commits do not force re-evaluation.

### Step 2 — publish endpoint-1 results and SeqKD endpoint 2

Run after both GPU lines print `done`. This publishes compact results only: the
SeqKD endpoints, the GKD smoke, GKD endpoint 1, and their evaluations. It also
commits and pushes. Terminal A for GKD requires this committed parent.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase publish-first; if ($LASTEXITCODE -ne 0) { throw 'Publication stopped; inspect git status and the message before retrying' }
```

### Step 3 — GKD endpoint 2 on GPU 1

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase gkd-terminal; if ($LASTEXITCODE -ne 0) { throw 'GKD terminal lane stopped; rerun this exact line' }; Write-Host 'GPU-1 done: GKD endpoint 2 evaluated; publish next'
```

### Step 4 — publish GKD endpoint 2

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p25_kd_comparison.py --phase publish-final; if ($LASTEXITCODE -ne 0) { throw 'Publication stopped; inspect git status and the message before retrying' }
```

### Decision after P2.5

Report the following, all seed 0:

- GKD − SeqKD at endpoint 1 and at endpoint 2 on all five sets.
- Paired wins/losses with exact McNemar p-values.
- Spider-family mean.
- Retention: endpoint 2 − endpoint 1.
- GKD cost reported separately: seconds per prompt, rollout tokens, and capped
  rollouts.

Do not relabel offline `fkl` as GKD. Depth, recurrence, and other KD variants
stay deferred until this comparison is reviewed.
