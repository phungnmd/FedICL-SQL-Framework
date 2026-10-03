# FedLS-SQL run queue

This file owns the next experiment and its launch commands. Results belong in
[LAB_LOG.md](LAB_LOG.md). All commands follow
[CONVENTION.MD section 6.1](../../CONVENTION.MD).

## Decision (2026-10-02): P2.15, the plan task on full data

P2.14 (1,000 rows) gave the first positive KD-with-CoT number: the plan task
added +1.84 Spider EX after FedAvg. P2.15 runs the same method on every BIRD
train row the teacher can solve, and adds a fresh full-gold baseline.

Same method as P2.14, all parts from published work:

- **Data (Struct-SQL,** [Thaker and Bresler](https://arxiv.org/abs/2512.17053)**):**
  the frozen teacher writes a QP-CoT plan and the SQL together, from question,
  schema and evidence only. A row is kept only if that SQL returns the gold
  result. Now over all 9,428 BIRD train rows. P2.10 kept 44% of its rows, so
  expect about 4,150 rows.
- **Training (Distilling Step-by-Step,**
  [Hsieh et al.](https://aclanthology.org/2023.findings-acl.507/)**):** the plan
  is a separate `[PLAN]` task, weight 0.8 as in
  [PARSQL](https://aclanthology.org/2025.findings-acl.37/). Clients and the
  deployed model stay SQL-only.

| Arm | Public stage K, 1 epoch | Then |
|---|---|---|
| `gold` | `[SQL]` question -> gold SQL, all 9,428 rows | SQL-only FedAvg rounds |
| `dss` | `[SQL]` question -> teacher SQL plus `[PLAN]` question -> teacher plan, admitted rows | SQL-only FedAvg rounds |
| `goldplan` (added 2026-10-03) | `[SQL]` question -> gold SQL, all 9,428 rows, plus `[PLAN]` question -> teacher plan, 4,109 admitted rows | SQL-only FedAvg rounds |

- The question: does `dss` beat `gold` and Hinton at `A>K>A`? Where the gain
  comes from (teacher SQL or plan) is not needed, so there is no `seq` arm.
- **Why `goldplan`:** `dss` learns SQL only on the 4,109 rows the teacher
  solved (mostly easier ones) and loses the other 5,319; Hinton and `gold` use
  all 9,428. `goldplan` keeps gold SQL on every row and adds only the teacher
  plan task. This is the labeled setting of Distilling Step-by-Step (human
  labels for the label task, LLM rationales only). `goldplan - gold` measures
  exactly what the teacher plan adds.
- All arms start from the committed SQL-only FL T1 adapter with the same recipe
  (LR 2e-4, batch 1 x accumulation 16, `target_fp32`, truncation as an error).
  Maximum length: 7,424 for `gold`, 8,448 for the arms with teacher plans (one
  plan row needs 7,579 tokens; with truncation as an error, a higher limit
  changes no example). `gold` is retrained so it matches `dss` exactly.
- **Hinton** is the committed `A>K[fkl]>A` row (66.63, same FL T1 parent, same
  terminal round, seed 0). The KD trainer only supports `full_bf16`, so it is not
  retrained. The analysis pairs `dss` and `gold` with its committed predictions
  (exact McNemar). It also pairs the new `gold` with the old full-gold row
  (66.54, `full_bf16`): if they are close, the change of loss mode does not
  matter and the Hinton comparison is fair.
- **More rounds** for the comparison at equal depth: `A>K>A>A` and
  `A>K>A>A>A` for `gold` and Hinton on the GPU that would otherwise wait, and
  for `dss` after its first round. All added rounds use `target_fp32`.

## Commands

Run from the **`fedicl-sql/` root on the GPU server**, PowerShell. Code: nested
branch `experiment/fullgold-plan`, commit
`de57c27849d312d3146fe032fbfd20f2c03e8f2d`. Do not switch, pull, edit or commit
in this working copy while any lane runs. Lanes write separate files and locks,
so the two terminals can run at the same time.

If step 1 already ran on the older commit, the prepared `gold` arm stays valid
(code changes no longer invalidate it). Let a running `gold` lane finish, then
pull and continue with the new commands.

1. One time, CPU (a few minutes): update the code, build the candidate list of
   all 9,428 rows, and prepare the `gold` arm.

```powershell
$ErrorActionPreference='Stop'; git fetch origin; if($LASTEXITCODE -ne 0){throw 'fetch failed'}; git switch experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'switch failed'}; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; $required='de57c27849d312d3146fe032fbfd20f2c03e8f2d'; $head=(git rev-parse HEAD).Trim(); if($LASTEXITCODE -ne 0 -or $head -ne $required){throw 'unexpected implementation commit'}; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python -m scripts.run_p215_struct_full --phase candidates; if($LASTEXITCODE -ne 0){throw 'P2.15 candidates failed'}; uv run python -m scripts.run_p215_struct_full --phase prepare --arm gold; if($LASTEXITCODE -ne 0){throw 'P2.15 gold preparation failed'}
```

2. Terminal 1, GPU 0: teacher generation (about 13-14 h; about 6,500 rows are
   new, the rest come from the P2.10 cache), preparation of `dss`, the `dss`
   lane (about 5-6 h), then two more rounds for `dss` (about 6 h). Generation
   resumes if the same command is rerun.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $R='scripts.run_p215_struct_full'; uv run python -m $R --phase generate; if($LASTEXITCODE -ne 0){throw 'P2.15 generation failed'}; uv run python -m $R --phase prepare --arm dss; if($LASTEXITCODE -ne 0){throw 'P2.15 dss preparation failed'}; uv run python -m $R --phase run --arm dss; if($LASTEXITCODE -ne 0){throw 'P2.15 dss lane failed'}; uv run python -m $R --phase extend --arm dss; if($LASTEXITCODE -ne 0){throw 'P2.15 dss depth failed'}
```

3. Terminal 2, GPU 1: the `gold` lane (about 6 h), then two more rounds for
   Hinton and for `gold` (about 6 h each).

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $R='scripts.run_p215_struct_full'; uv run python -m $R --phase run --arm gold; if($LASTEXITCODE -ne 0){throw 'P2.15 gold lane failed'}; foreach ($A in 'hinton','gold') { uv run python -m $R --phase extend --arm $A; if($LASTEXITCODE -ne 0){throw "P2.15 $A depth failed"} }
```

Each training lane first runs its memory probe on its longest examples (stops
above 21.5 GiB reserved), a short smoke, then K, evaluation, the private round,
and evaluation. Each depth round is followed by the five-set evaluation. Check
with `nvidia-smi` that each lane is on the intended GPU. Time estimates use
P2.14 speeds (about 0.87 s per example step, about 1.6 h per private round,
about 1.4-1.8 h of evaluation) and P2.10 teacher speed (about 7.5 s per row).

   If `prepare --arm dss` stopped with `training sequence exceeds max_len`
   (fixed in the commit above: teacher arms now allow 8,448 tokens, gold keeps
   7,424), update the code and resume GPU 0 from preparation. Generation is
   finished and is not rerun.

```powershell
$ErrorActionPreference='Stop'; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; $required='de57c27849d312d3146fe032fbfd20f2c03e8f2d'; $head=(git rev-parse HEAD).Trim(); if($LASTEXITCODE -ne 0 -or $head -ne $required){throw 'unexpected implementation commit'}; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $R='scripts.run_p215_struct_full'; uv run python -m $R --phase prepare --arm dss; if($LASTEXITCODE -ne 0){throw 'P2.15 dss preparation failed'}; uv run python -m $R --phase run --arm dss; if($LASTEXITCODE -ne 0){throw 'P2.15 dss lane failed'}; uv run python -m $R --phase extend --arm dss; if($LASTEXITCODE -ne 0){throw 'P2.15 dss depth failed'}
```

4. `goldplan` (about 8 h: K has about 13,500 examples, about 3.3 h). Run it
   on the first free GPU, only while no other P2.15 lane runs in this working
   copy, because the command pulls new code. If `dss` at `A>K>A` is not above
   `gold`, stop GPU 0 during `extend dss` (Ctrl+C; `A>K>A` is already
   recorded) and start this on GPU 0. Otherwise run it after `extend dss`.
   Add `--phase extend --arm goldplan` afterwards for the two depth rounds
   (about 6 h).

```powershell
$ErrorActionPreference='Stop'; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; git merge-base --is-ancestor 47aedc36668bb848e327580a161e79b2d700d44a HEAD; if($LASTEXITCODE -ne 0){throw 'goldplan code is missing'}; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $R='scripts.run_p215_struct_full'; uv run python -m $R --phase prepare --arm goldplan; if($LASTEXITCODE -ne 0){throw 'P2.15 goldplan preparation failed'}; uv run python -m $R --phase run --arm goldplan; if($LASTEXITCODE -ne 0){throw 'P2.15 goldplan lane failed'}
```

5. Publication. It can run once `gold` and `dss` have finished `A>K>A`, and
   again after the depth rounds; each run commits only new or changed files. It
   writes `audits/protocol_v2/p215_struct_full_s0/summary.md` (also printed),
   with the Spider table per depth and all paired contrasts. The first run also
   commits the public teacher pool (BIRD train rows only, as P2.10 did).

```powershell
$ErrorActionPreference='Stop'; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python -m scripts.run_p215_struct_full --phase analyze; if($LASTEXITCODE -ne 0){throw 'P2.15 analysis failed'}; $staged=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or $staged.Count -ne 0){throw 'index must be empty'}; $paths=@(uv run python -m scripts.list_p215_publication); if($LASTEXITCODE -ne 0 -or $paths.Count -eq 0){throw 'nothing new to publish'}; $big=@($paths | Where-Object { (Get-Item -LiteralPath $_).Length -gt 95MB }); if($big.Count -ne 0){throw "files above 95 MB: $big"}; git add -- $paths; if($LASTEXITCODE -ne 0){throw 'git add failed'}; $actual=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or @(Compare-Object ($paths | Sort-Object) ($actual | Sort-Object)).Count -ne 0){throw 'staged paths differ from allowlist'}; git commit -m 'results: record P2.15 full-data Struct-SQL plan-task run'; if($LASTEXITCODE -ne 0){throw 'commit failed'}; git push origin HEAD:experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'push failed'}
```

The `goldplan` command checks that its code is an ancestor of `HEAD`, not equal
to it, so it still runs after a publication commit. The publication stops on
any file above 95 MB (GitHub rejects files above 100 MB).

Run the publication only while no lane is running, because a lane would write
to the manifest during the commit. It pulls first, because the branch has code
commits newer than the running `dss` lane.

Send back: the generation summary line (admitted rows, acceptance and parse
rates), each memory probe line, and the summary table.

## P2.16: equal-depth controls (GPU 1, runs next to `goldplan`)

P2.15 compares K chains at 2, 3 and 4 private Spider passes. A claim that the
public stage helps FL, or reaches centralized training, needs controls at the
same number of passes:

| Passes | K chain (P2.15) | FL control | Centralized |
|---|---|---|---|
| 2 | `A>K>A` | `A>A` (committed) | E2 |
| 3 | `A>K>A>A` | `A>A>A` (new) | E3 |
| 4 | `A>K>A>A>A` | `A>A>A>A` (new) | E4 |

- FL rounds grow from the committed `A>A` row with the P2.15 private recipe.
- Centralized: one continuous 4-epoch Spider run (`target_fp32`, private-client
  recipe), adapter saved after each epoch, so E1-E4 come from one schedule.
- Time: FL about 4.5 h, centralized about 9.5 h (7.6 h training plus four
  five-set evaluations). Memory as a private client round (about 12.6 GB).

Launch on GPU 1 (code `9f9aa6b`). The `goldplan` lane may keep running on GPU 0:
the command pulls only after checking that every incoming change is a new P2.16
file, Markdown, `experiments/client_train/run.py`, or the baseline PowerShell
script, none of which the running lane imports.

```powershell
$ErrorActionPreference='Stop'; git fetch origin; if($LASTEXITCODE -ne 0){throw 'fetch failed'}; $changed=@(git diff --name-only HEAD origin/experiment/fullgold-plan); if($LASTEXITCODE -ne 0){throw 'diff failed'}; $allowed='^(scripts/run_p216_equal_depth\.py|scripts/list_p216_publication\.py|tests/test_p216_equal_depth\.py|experiments/client_train/run\.py|scripts/run_protocol_v2_baselines\.ps1|.+\.md)$'; $bad=@($changed | Where-Object { $_ -notmatch $allowed }); if($bad.Count -ne 0){throw "pull would change files the running lane uses: $bad"}; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; git merge-base --is-ancestor 9f9aa6b6c118c083b6a8629a6961d34e45d35577 HEAD; if($LASTEXITCODE -ne 0){throw 'P2.16 code is missing'}; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $R='scripts.run_p216_equal_depth'; uv run python -m $R --phase fl; if($LASTEXITCODE -ne 0){throw 'P2.16 FL depth failed'}; uv run python -m $R --phase central; if($LASTEXITCODE -ne 0){throw 'P2.16 centralized run failed'}
```

Publication, only when no lane runs in this working copy (P2.15 and P2.16 lanes
included). It can run more than once; each run commits only new or changed
files.

```powershell
$ErrorActionPreference='Stop'; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python -m scripts.run_p216_equal_depth --phase analyze; if($LASTEXITCODE -ne 0){throw 'P2.16 analysis failed'}; $staged=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or $staged.Count -ne 0){throw 'index must be empty'}; $paths=@(uv run python -m scripts.list_p216_publication); if($LASTEXITCODE -ne 0 -or $paths.Count -eq 0){throw 'nothing new to publish'}; git add -- $paths; if($LASTEXITCODE -ne 0){throw 'git add failed'}; $actual=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or @(Compare-Object ($paths | Sort-Object) ($actual | Sort-Object)).Count -ne 0){throw 'staged paths differ from allowlist'}; git commit -m 'results: record P2.16 equal-depth FL and centralized controls'; if($LASTEXITCODE -ne 0){throw 'commit failed'}; git push origin HEAD:experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'push failed'}
```

## P2.17: a second public stage (`A>K>A>K`, `A>K>A>K>A`)

Why: every KD variant beats full gold right after K (Hinton `A>K` Spider +3.29,
p = .012), and the next private round removes the edge. Protocol v1 ended its
chain on K (`A>K>A>K>A>K`, Spider 69.54). P2.17 adds a second K to the finished
`A>K>A` rows and one more private round:

| Arm | New stages | Compared with (same private passes) |
|---|---|---|
| `gold` | `K[ce]` (P2.15 gold recipe), then `A` | gold `A>K>A` 65.86, `A>K>A>A` 67.89 |
| `hinton` | `K[fkl]` (committed recipe and logit cache, now `target_fp32`), then `A` | Hinton `A>K>A` 66.63, `A>K>A>A` 67.60 |

- Decision rule: Hinton minus gold at `A>K>A>K>A` at least +1 Spider point;
  otherwise close interleaving. `A>K>A>K` (endpoint after K) is read the same
  way against its references.
- Hinton KD now runs with `target_fp32` (nested `0af4455`). The lane first runs
  an isolated memory probe on the longest BIRD prompt and target and stops above
  21.5 GiB. Report the printed `reserved=` value.
- Time, estimated: Hinton about 7 h (K about 4 h, A 1.6 h, two five-set
  evaluations), gold about 6 h.

Hinton on GPU 0 now (code `7096718`). P2.16 centralized may keep running on
GPU 1: the pull is checked first, and the files it changes are not imported by
the running centralized training or its evaluations.

```powershell
$ErrorActionPreference='Stop'; git fetch origin; if($LASTEXITCODE -ne 0){throw 'fetch failed'}; $changed=@(git diff --name-only HEAD origin/experiment/fullgold-plan); if($LASTEXITCODE -ne 0){throw 'diff failed'}; $allowed='^(scripts/run_p217_interleave\.py|scripts/list_p217_publication\.py|tests/.+\.py|fedicl_sql/training/lora_trainer\.py|fedicl_sql/federated/round_loop\.py|experiments/federated/run\.py|.+\.md)$'; $bad=@($changed | Where-Object { $_ -notmatch $allowed }); if($bad.Count -ne 0){throw "pull would change files the running lane uses: $bad"}; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; git merge-base --is-ancestor 709671823a00a1f96edf84e6be7e81132718f2ac HEAD; if($LASTEXITCODE -ne 0){throw 'P2.17 code is missing'}; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; uv run python -m scripts.run_p217_interleave --phase run --arm hinton; if($LASTEXITCODE -ne 0){throw 'P2.17 hinton lane failed'}
```

Gold on whichever GPU frees first (GPU 1 after P2.16 centralized, or GPU 0
after the Hinton lane). Change `CUDA_VISIBLE_DEVICES` to that GPU.

```powershell
$ErrorActionPreference='Stop'; git merge-base --is-ancestor 709671823a00a1f96edf84e6be7e81132718f2ac HEAD; if($LASTEXITCODE -ne 0){throw 'P2.17 code is missing; run the Hinton command first'}; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run python -m scripts.run_p217_interleave --phase run --arm gold; if($LASTEXITCODE -ne 0){throw 'P2.17 gold lane failed'}
```

Publication, only when no lane runs in this working copy. It can run more than
once; each run commits only new or changed files.

```powershell
$ErrorActionPreference='Stop'; git pull --ff-only origin experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'pull failed'}; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python -m scripts.run_p217_interleave --phase analyze; if($LASTEXITCODE -ne 0){throw 'P2.17 analysis failed'}; $staged=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or $staged.Count -ne 0){throw 'index must be empty'}; $paths=@(uv run python -m scripts.list_p217_publication); if($LASTEXITCODE -ne 0 -or $paths.Count -eq 0){throw 'nothing new to publish'}; $big=@($paths | Where-Object { (Get-Item -LiteralPath $_).Length -gt 95MB }); if($big.Count -ne 0){throw "files above 95 MB: $big"}; git add -- $paths; if($LASTEXITCODE -ne 0){throw 'git add failed'}; $actual=@(git diff --cached --name-only); if($LASTEXITCODE -ne 0 -or @(Compare-Object ($paths | Sort-Object) ($actual | Sort-Object)).Count -ne 0){throw 'staged paths differ from allowlist'}; git commit -m 'results: record P2.17 interleaved public stages'; if($LASTEXITCODE -ne 0){throw 'commit failed'}; git push origin HEAD:experiment/fullgold-plan; if($LASTEXITCODE -ne 0){throw 'push failed'}
```

## Parked

- P2.14 (1,000-row screen): done, see the
  [archived queue](../archive/completed_runbooks/P214_STRUCT_DSS_2026-10-02.md).
- P2.13: superseded before training
  ([archived queue](../archive/superseded_runbooks/P213_FULLGOLD_PLAN_2026-10-02.md)).
- A1 merge gate: failed, closed (lab log 2026-10-02; results not committed).
- A2 interleaving, P2.11, P2.12, A3. P2.10 stays stopped.

Earlier queue versions:
[before the full-gold plan decision](../archive/completed_runbooks/PIPELINE_PRE_FULLGOLD_PLAN_2026-10-02.md).
