# FedLS-SQL — active protocol-v2 queue

> Run from the `fedicl-sql/` repository root on the Windows experiment server.
> PowerShell single-line commands; caller selects GPU. Exact reruns reuse or
> resume completed work under the same fingerprints. Do not change Git while jobs run.

## Current queue — P2.3 only

| Order | Action | Status / condition |
|---|---|---|
| 1 | Finish smoke; sync code containing `362aced` | smoke last reported running on 2026-09-16; do not pull mid-run |
| 2 | GPU 0: `A>A`; GPU 1: `A>K[fkl]>A` | each trains then evaluates five sets automatically; both lanes may run concurrently |
| 3 | Publish smoke + both lanes | only after both entire commands exit |
| 4 | Paired analysis and method decision | no additional experiment auto-starts |

Purpose: test whether terminal private training/FedAvg recovers Spider robustness
while retaining the BIRD gain from Hinton. Both arms add one private epoch/client
with identical settings; only their parent adapters differ. No teacher/cache rebuild.

Completed P2.1R/P2.2 commands and prior gates are in the
[archived runbook](../archive/completed_runbooks/P2_1R_P2_2_COMPLETED_2026-09-16.md).
Evidence: [P22 transfer review](../results/P22_TRANSFER_REVIEW.md).
Broader conditional tasks: [PAPER_TODO.md](PAPER_TODO.md).

## Active P2.3 commands — terminal private consolidation

Required code: nested `362aced` or a descendant. Parent results must be committed
and unchanged; stage contracts bind parent/data/recipe hashes. Preserve and
inspect any old version-1 stage root instead of deleting or silently upgrading it.

**1. Sync once, then smoke (one GPU).** Run while no experiment process uses
the worktree. The smoke caps each client at two steps from the Hinton T1 parent
and checks the derived chain.

```powershell
$ErrorActionPreference='Stop'; $Scope=@('fedicl_sql','experiments','scripts','tests','processed_data/protocol_v2','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific scope is dirty; review before pull' }; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; git merge-base --is-ancestor 362aced HEAD; if ($LASTEXITCODE -ne 0) { throw 'Checkout does not contain stage-chain commit 362aced' }; Write-Host 'P2.3 code ready; run smoke next, then open the two training terminals'
```

Then run the smoke. This line contains no pull/commit and is safe to rerun for
checkpoint recovery:

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; $R='experiments/federated/results/federated__fedkd__s0__55c03ff12654__8a1e6694__r1'; $O='artifacts/protocol_v2/p23_smoke/a_k_a_steps2_s0'; uv run python experiments/federated/run.py stage private --aggregation-protocol plaintext --parent-result $R --split-dir $S --n-clients 5 --local-epochs 1 --client-train-k 0 --client-dataset-profile spider --client-max-steps 2 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --stage p23_smoke_a_k_a --out $O; if ($LASTEXITCODE -ne 0) { throw 'P2.3 smoke failed; inspect the error before any full run' }; $St=Get-Content -LiteralPath "$O/stage.json" -Raw | ConvertFrom-Json; if ($St.version -ne 2 -or $St.chain -ne 'A>K[fkl]>A' -or -not $St.contains_kd -or $St.parent.run_id -ne 'federated__fedkd__s0__55c03ff12654__8a1e6694__r1' -or -not (Test-Path -LiteralPath "$O/fedavg_adapter/adapter_config.json")) { throw "Unexpected smoke contract: chain=$($St.chain)" }; Write-Host "P2.3 smoke passed at $((git rev-parse --short HEAD).Trim()): chain=$($St.chain) stage_id=$($St.stage_id)"
```

**2. After smoke passes: one continuous train → five-set eval command per GPU.**

If the reported smoke is still running, let it finish before pulling code.
Then sync nested `362aced` or a descendant using the sync command above before
launching either full lane. That commit removes eval result-name collisions;
an already successful `014b118` smoke does not need retraining. Keep smoke
output; its compact publication is deferred to the final command below.

Start the following in two terminals. Both training and evaluation can run
concurrently; each lane automatically evaluates Spider,
Realistic, SYN, DK, and BIRD. Both use one extra private epoch/client and
plaintext FedAvg, with no new teacher/KD/cache generation.

New result directories include fingerprint hash + UUID and are reserved
atomically; no shared mutex or eval queue remains. Training roots and the
lane-specific evaluation resume roots are unchanged. Existing timestamp-only
results are preserved. Resume/skip still uses the exact fingerprint (including
Git SHA), so do not update a checkout while either lane is running. Older
paired-eval roots are preserved but are not the lane-specific resume roots.

GPU 0 — `A>A`: train → evaluate five sets:

```powershell
$ErrorActionPreference='Stop'; git merge-base --is-ancestor 362aced HEAD; if ($LASTEXITCODE -ne 0) { throw 'Sync reviewed P2.3 code before starting any GPU job' }; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; $R='experiments/federated/results/federated__fedavg__s0__935d572565cc__154540d3__r1'; $O='artifacts/protocol_v2/p23_spider_private_terminal/a_a_s0'; $ST='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $BT='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $Sets=@(@{Name='spider';Train=$ST;Test='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv';Profile='spider'},@{Name='realistic';Train=$ST;Test='processed_data/SPIDER_REALISTIC/test.csv';Profile='spider'},@{Name='syn';Train=$ST;Test='processed_data/SPIDER_SYN/test.csv';Profile='spider'},@{Name='dk';Train=$ST;Test='processed_data/SPIDER_DK/test.csv';Profile='spider'},@{Name='bird';Train=$BT;Test='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv';Profile='bird_with_evidence'}); $Scope=@('fedicl_sql','experiments','scripts','pyproject.toml','uv.lock',$S,$R); foreach ($Set in $Sets) { foreach ($P in @($Set.Train,$Set.Test)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing evaluation input: $P" }; $Scope+=$P } }; $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($LASTEXITCODE -ne 0) { throw 'Git preflight failed' }; if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific scope is dirty; review before launch' }; uv run python experiments/federated/run.py stage private --aggregation-protocol plaintext --parent-result $R --split-dir $S --n-clients 5 --local-epochs 1 --client-train-k 0 --client-dataset-profile spider --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --stage p23_spider_private_a_a --out $O; if ($LASTEXITCODE -ne 0) { throw 'A>A stopped; rerun this exact line' }; $St=Get-Content -LiteralPath "$O/stage.json" -Raw | ConvertFrom-Json; if ($St.version -ne 2 -or $St.chain -ne 'A>A' -or $St.contains_kd -or -not (Test-Path -LiteralPath "$O/fedavg_adapter/adapter_config.json")) { throw "Unexpected A>A contract: chain=$($St.chain)" }; $Lane='a_a'; $Arm='pure_fl_a_a'; $A="$O/fedavg_adapter"; $Head=(git rev-parse --short HEAD).Trim(); Write-Host 'Training done; evaluating five sets on this GPU'; foreach ($Set in $Sets) { $E="artifacts/eval_resume/protocol_v2/p23_terminal_${Lane}_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $Set.Train --test-csv $Set.Test --dataset-profile $Set.Profile --arms "${Arm}=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "P2.3 ${Lane} evaluation failed: $($Set.Name); rerun this exact line" }; $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $F=$V.fingerprint | ConvertFrom-Json; $U=@($F.units); $V.status -eq 'completed' -and $U.Count -eq 1 -and $U[0].arm -eq $Arm -and $U[0].git_sha -eq $Head -and $U[0].test_source.path -eq $Set.Test -and $U[0].adapter.path -eq $A -and @($V.artifacts.predictions).Count -eq 1 -and (Test-Path -LiteralPath $V.artifacts.metrics) -and (Test-Path -LiteralPath $V.artifacts.config) -and (Test-Path -LiteralPath $V.artifacts.predictions[0]) } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one compatible completed manifest for ${Lane}/$($Set.Name), found $($Done.Count)" } }; Write-Host 'P2.3 a_a complete: trained and evaluated on all five sets; publish only after both terminals exit'
```

GPU 1 — `A>K[fkl]>A`: train → evaluate five sets:

```powershell
$ErrorActionPreference='Stop'; git merge-base --is-ancestor 362aced HEAD; if ($LASTEXITCODE -ne 0) { throw 'Sync reviewed P2.3 code before starting any GPU job' }; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; $R='experiments/federated/results/federated__fedkd__s0__55c03ff12654__8a1e6694__r1'; $O='artifacts/protocol_v2/p23_spider_private_terminal/a_k_a_s0'; $ST='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $BT='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $Sets=@(@{Name='spider';Train=$ST;Test='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv';Profile='spider'},@{Name='realistic';Train=$ST;Test='processed_data/SPIDER_REALISTIC/test.csv';Profile='spider'},@{Name='syn';Train=$ST;Test='processed_data/SPIDER_SYN/test.csv';Profile='spider'},@{Name='dk';Train=$ST;Test='processed_data/SPIDER_DK/test.csv';Profile='spider'},@{Name='bird';Train=$BT;Test='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv';Profile='bird_with_evidence'}); $Scope=@('fedicl_sql','experiments','scripts','pyproject.toml','uv.lock',$S,$R); foreach ($Set in $Sets) { foreach ($P in @($Set.Train,$Set.Test)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing evaluation input: $P" }; $Scope+=$P } }; $Dirty=@(git status --porcelain --untracked-files=no -- $Scope); if ($LASTEXITCODE -ne 0) { throw 'Git preflight failed' }; if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific scope is dirty; review before launch' }; uv run python experiments/federated/run.py stage private --aggregation-protocol plaintext --parent-result $R --split-dir $S --n-clients 5 --local-epochs 1 --client-train-k 0 --client-dataset-profile spider --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --stage p23_spider_private_a_k_a --out $O; if ($LASTEXITCODE -ne 0) { throw 'A>K>A stopped; rerun this exact line' }; $St=Get-Content -LiteralPath "$O/stage.json" -Raw | ConvertFrom-Json; if ($St.version -ne 2 -or $St.chain -ne 'A>K[fkl]>A' -or -not $St.contains_kd -or -not (Test-Path -LiteralPath "$O/fedavg_adapter/adapter_config.json")) { throw "Unexpected A>K>A contract: chain=$($St.chain)" }; $Lane='a_k_a'; $Arm='hinton_a_k_a'; $A="$O/fedavg_adapter"; $Head=(git rev-parse --short HEAD).Trim(); Write-Host 'Training done; evaluating five sets on this GPU'; foreach ($Set in $Sets) { $E="artifacts/eval_resume/protocol_v2/p23_terminal_${Lane}_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $Set.Train --test-csv $Set.Test --dataset-profile $Set.Profile --arms "${Arm}=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "P2.3 ${Lane} evaluation failed: $($Set.Name); rerun this exact line" }; $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $F=$V.fingerprint | ConvertFrom-Json; $U=@($F.units); $V.status -eq 'completed' -and $U.Count -eq 1 -and $U[0].arm -eq $Arm -and $U[0].git_sha -eq $Head -and $U[0].test_source.path -eq $Set.Test -and $U[0].adapter.path -eq $A -and @($V.artifacts.predictions).Count -eq 1 -and (Test-Path -LiteralPath $V.artifacts.metrics) -and (Test-Path -LiteralPath $V.artifacts.config) -and (Test-Path -LiteralPath $V.artifacts.predictions[0]) } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one compatible completed manifest for ${Lane}/$($Set.Name), found $($Done.Count)" } }; Write-Host 'P2.3 a_k_a complete: trained and evaluated on all five sets; publish only after both terminals exit'
```

On interruption, rerun the exact affected line: completed training is reused,
unfinished checkpoints resume, and completed eval sets are skipped. Keep Git
unchanged until **both entire commands** exit (including evaluation). If one
GPU is available, run the Hinton-parent lane first, then the pure-FL lane,
changing only `CUDA_VISIBLE_DEVICES`. Never launch two copies of one lane.

**3. Publish after both lanes finish.** This is the separate publication command
for both lanes and the earlier smoke: three stage rows (smoke + two full runs)
and ten single-arm eval records. Only metrics/config/predictions enter Git.
No adapters, caches, resume manifests, or interrupted-publication sidecars.

```powershell
$ErrorActionPreference='Stop'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $Files=[System.Collections.Generic.List[string]]::new(); $Stages=@(@{Label='p23_smoke_a_k_a';Out='artifacts/protocol_v2/p23_smoke/a_k_a_steps2_s0'},@{Label='p23_spider_private_a_a';Out='artifacts/protocol_v2/p23_spider_private_terminal/a_a_s0'},@{Label='p23_spider_private_a_k_a';Out='artifacts/protocol_v2/p23_spider_private_terminal/a_k_a_s0'}); foreach ($Stage in $Stages) { $St=Get-Content -LiteralPath "$($Stage.Out)/stage.json" -Raw | ConvertFrom-Json; if ($St.version -ne 2) { throw 'Expected version-2 stage contract' }; $Hits=@(Get-ChildItem -LiteralPath 'experiments/federated/results' -Directory -Filter 'federated_stage__*' | Where-Object { try { $M=Get-Content -LiteralPath (Join-Path $_.FullName 'metrics.json') -Raw | ConvertFrom-Json; $C=Get-Content -LiteralPath (Join-Path $_.FullName 'config.json') -Raw | ConvertFrom-Json; $M.stage_id -eq $St.stage_id -and $M.stage -eq $Stage.Label -and $C.out -eq $Stage.Out } catch { $false } }); if ($Hits.Count -ne 1) { throw "Expected one completed result for $($Stage.Label), found $($Hits.Count)" }; $Files.Add((Join-Path $Hits[0].FullName 'metrics.json')); $Files.Add((Join-Path $Hits[0].FullName 'config.json')) }; foreach ($Lane in @('a_a','a_k_a')) { $Arm=if ($Lane -eq 'a_a') { 'pure_fl_a_a' } else { 'hinton_a_k_a' }; $A="artifacts/protocol_v2/p23_spider_private_terminal/$Lane/fedavg_adapter"; foreach ($Name in @('spider','realistic','syn','dk','bird')) { $D="artifacts/eval_resume/protocol_v2/p23_terminal_${Lane}_${Name}_s0/eval_k0/manifests"; $Done=@(Get-ChildItem -LiteralPath $D -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $F=$V.fingerprint | ConvertFrom-Json; $U=@($F.units); $V.status -eq 'completed' -and $U.Count -eq 1 -and $U[0].arm -eq $Arm -and $U[0].adapter.path -eq $A -and @($V.artifacts.predictions).Count -eq 1 -and (Test-Path -LiteralPath $V.artifacts.metrics) -and (Test-Path -LiteralPath $V.artifacts.config) -and (Test-Path -LiteralPath $V.artifacts.predictions[0]) } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one completed manifest for ${Lane}/${Name}, found $($Done.Count)" }; $V=Get-Content -LiteralPath $Done[0].FullName -Raw | ConvertFrom-Json; $Files.Add([string]$V.artifacts.metrics); $Files.Add([string]$V.artifacts.config); $Files.Add([string]$V.artifacts.predictions[0]) } }; $Sep=[IO.Path]::DirectorySeparatorChar; $Root=(Resolve-Path -LiteralPath '.').Path.TrimEnd($Sep)+$Sep; $Rel=@($Files | ForEach-Object { $F=(Resolve-Path -LiteralPath $_).Path; if (-not $F.ToLowerInvariant().StartsWith($Root.ToLowerInvariant())) { throw "Outside repository: $F" }; $F.Substring($Root.Length).Replace([string]$Sep,'/') } | Sort-Object -Unique); git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'Result staging failed' }; $Staged=@(git diff --cached --name-only | Sort-Object); $Expected=@(git diff HEAD --name-only -- $Rel | Sort-Object); if ($Expected.Count -ne $Staged.Count -or ($Staged.Count -gt 0 -and @(Compare-Object $Expected $Staged).Count -ne 0)) { throw 'Staged allowlist mismatch' }; if ($Staged.Count -gt 0) { git commit -m 'results: publish P2.3 terminal consolidation and five-set evaluations'; if ($LASTEXITCODE -ne 0) { throw 'Result commit failed' } }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Result push failed; retry publication after reviewing remote status' }; git log -1 --oneline
```

**4. Decision gate — stop here for paired analysis.** No new KD objective,
three-epoch consolidation, or extra arm runs automatically. The existing
Pure-FL `A` and Hinton `A>K[fkl]` headline predictions supply the two
pre-consolidation controls with the same evaluation recipe.

Promotion gate: `A>K[fkl]>A` must exceed both `A>K[fkl]` and `A>A` on Spider
and the Spider variants while retaining useful BIRD transfer. Report the extra
client compute and each stage row's `communication_bytes`.

If the endpoint comparison is promising, add `A>gold CE>A` to isolate the
teacher contribution before claiming a KD-specific final benefit. Other KD
methods, three-epoch consolidation, and recurrent T2/T3 remain conditional on
this result; consult PAPER_TODO rather than launching archived commands.
