# FedLS-SQL — active protocol-v2 queue

> Run from the `fedicl-sql/` repository root on the Windows experiment server.
> Commands are PowerShell single lines. Exact reruns resume or skip completed
> outputs. The caller selects the GPU; runners never assign a physical GPU.

## Active order

| Order | Task | Status |
|---|---|---|
| P2.1R | BIRD-private full-context Base/Centralized/FL | complete and published |
| P2.2a | BIRD-public teacher targets for Spider-private direction | complete: 5,319/9,428 selected |
| P2.2b | Spider-public teacher targets for BIRD-private direction | complete: 7,251/8,659 selected |
| P2.2c | Matched T1 ladder in both directions | Spider-private complete; BIRD-private next |
| P2.2d | Hinton-FKL T1 | next after cache/runner contract is pinned |
| P2.3 | Select or improve KD/federated method | adaptive after P2.2c–d |

## Direction contract

The two independent directions are:

| Runner | Private clients / evaluation | Public teacher pool |
|---|---|---|
| `run_protocol_v2_spider_private.ps1` | Spider, profile `spider` | BIRD-original, profile `bird_with_evidence` |
| `run_protocol_v2_bird_private.ps1` | BIRD-original, profile `bird_with_evidence` | Spider, profile `spider` |

Both use Qwen2.5-Coder-7B-Instruct as teacher and Qwen2.5-1.5B-Instruct as
student, `k=0`, full schema, greedy generation, and teacher-specific
execution-matched selection. The Spider-private runner resumes the existing
BIRD raw-target checkpoint; a progress display such as `0/2300` means 2,300
pending rows, not a restart of all 9,428 rows.

Technical review at nested `c13fc9f` confirms that BIRD evidence reaches raw
teacher generation, server training inputs, private-client training, and BIRD
evaluation through the explicit dataset profile. SQLite execution is now
read-only as a safety guard, while the established Spider/BIRD evaluator
identities and all previously accepted results remain unchanged. Resume also
repairs only an interrupted partial final JSONL append and rejects earlier
checkpoint corruption.
Nested `633743c` additionally treats a resume directory as a collection of
fingerprinted runs: it selects the newest compatible completed manifest rather
than requiring the directory to contain exactly one JSON file. Thus a completed
teacher evaluation is preserved after code-only runner updates.

Each `Full` phase currently closes the public-teacher prerequisites: validate,
generate/resume all raw targets, audit public gold SQL, quick-execute and score
teacher SQL with the public dataset's evaluator, build the exact row-matched
gold control, and evaluate the teacher on the public dev set. The BIRD-private
runner additionally rescores the six completed P2.1R prediction files with the
official BIRD 30-second pair deadline. Neither runner starts FedLS training;
the selected-pool counts and teacher EX are the gate for the matched T1 ladder.
Therefore `Full` means the complete public-teacher prerequisite lane, not the
complete paper experiment matrix.

## Completed prerequisite runners

Run this sync once while no experiment process is using the worktree:

```powershell
$Scope=@('fedicl_sql','experiments','scripts','tests','processed_data/protocol_v2','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific scope is dirty; review before pull' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; Write-Host "Ready at $((git rev-parse --short HEAD).Trim())"
```

These exact reruns now verify or skip completed prerequisite outputs; they are
not the next accuracy jobs:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_spider_private.ps1 -Phase Full; if ($LASTEXITCODE -ne 0) { throw 'Spider-private direction stopped; rerun this exact line to resume' }
```

Reverse prerequisite verification:

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; powershell -ExecutionPolicy Bypass -File scripts/run_protocol_v2_bird_private.ps1 -Phase Full; if ($LASTEXITCODE -ne 0) { throw 'BIRD-private direction stopped; rerun this exact line to resume' }
```

Do not rerun either lane for new accuracy evidence. The next implementation
task is to pin resume-safe commands for the reverse matched T1 ladder and the
new Hinton-forward-KL cache/arm. No T2/T3 job is active.

## Completion gate

The prerequisite gate is now closed:

- teacher EX is 47.07 on BIRD dev and 76.69 on Spider;
- BIRD-public coverage is 5,319/9,428 (56.42%);
- Spider-public coverage is 7,251/8,659 (83.74%);
- official BIRD Base/Centralized-E1/E2/FL-T1/T2/T3 EX is
  15.97/31.42/34.94/22.75/28.36/31.10.

Do not regenerate already accepted Spider-only results merely because SQLite
is now opened read-only. Re-evaluate their saved adapters/predictions under the
explicit `spider` profile only where protocol-v2 provenance is still missing.

Then freeze only the T1 comparison:

```text
Pure FL
  vs matched public-gold CE
  vs execution-matched teacher-target CE (SeqKD)
  vs the same target CE + Hinton forward KL
```

Open recurring T2/T3 only when T1 shows an interpretable EX gain. Hinton FKL is
the primary soft-logit baseline and remains an ablation until it adds EX over
SeqKD. Other KD objectives remain deferred. Publication commands are generated after the
completion artifacts are inspected and an exact compact allowlist is known;
model adapters, trainer state, raw caches, and `artifacts/` are never staged.

The first direction does not pass the T2/T3 gate yet: SeqKD is 57.64 EX versus
56.96 for Pure FL, only seven net correct rows (140 corrections, 133
regressions). Run the reverse matched T1 ladder and Hinton-FKL T1 before
selecting the method.
