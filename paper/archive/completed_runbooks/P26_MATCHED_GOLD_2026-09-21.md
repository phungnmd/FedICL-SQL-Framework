# FedLS-SQL — active protocol-v2 queue

## P2.5 decision — complete

SeqKD and protocol-v2 KID are complete at both `A>K` and `A>K>A` endpoints.
KID terminal is statistically indistinguishable from SeqKD terminal on all
five evaluation sets while its public stage costs about 21.1 GPU-hours.
KID, GKD, clean RKL/MiniLLM follow-ups, and deeper Hinton are closed for the
current paper queue. The completed commands are preserved in
[P25_SEQKD_KID_2026-09-20.md](../archive/completed_runbooks/P25_SEQKD_KID_2026-09-20.md).

| Evaluation | SeqKD public | KID public | SeqKD terminal | KID terminal |
|---|---:|---:|---:|---:|
| Spider | 57.93 | 58.03 | 64.99 | 65.47 |
| Realistic | 46.65 | 44.09 | 57.68 | 57.09 |
| SYN | 48.26 | 46.23 | 54.55 | 54.16 |
| DK | 45.61 | 44.30 | 50.28 | 50.28 |
| BIRD dev, evidence | 34.68 | 35.40 | 28.42 | 28.94 |

## P2.6 — matched selected-gold terminal gate

This is the next mandatory causal gate. It uses the already published
one-epoch matched-gold parent on exactly the same 5,319 ordered BIRD prompts as
SeqKD. GPU 0 appends the missing terminal Spider-private `A`; GPU 1 independently
evaluates the existing public endpoint on all five sets. They only read the
same committed parent/adapter and may run concurrently.

Held fixed against P2.5 SeqKD: FL parent, 5,319 row identities, evidence-aware
public prompts, one public pass, one terminal local epoch, optimizer/LoRA
recipe, evaluation datasets, batch size 16, decoding and seed. The only public
target difference is BIRD gold SQL versus execution-verified teacher SQL.

Do **not** start SeqKD-2, retention KD, structured-rationale KD, or another KD
objective before this gate is published and reviewed. A second public epoch
must later be planned from the FL parent with a matched two-epoch gold control;
it must not be presented as an extension equivalent to a two-epoch schedule
planned from step zero.

### Step 0 — sync and verify once

Run from the Windows server `fedicl-sql/` root. Required nested result commit:
`5d861f8` or a descendant.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; git pull --ff-only origin main; if ($LASTEXITCODE -ne 0) { throw 'Pull failed; inspect git status' }; git merge-base --is-ancestor 5d861f8 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Required P2.5 result commit 5d861f8 is missing' }; $Scope=@('fedicl_sql','experiments','scripts','tests','pyproject.toml','uv.lock'); $Dirty=@(git status --porcelain --untracked-files=all -- $Scope | Where-Object { $Path=$_.Substring(3).Trim('"').Replace('\','/'); $Path -notmatch '^experiments/[^/]+/results/' }); if ($Dirty.Count -ne 0) { $Dirty | ForEach-Object { Write-Host $_ }; throw 'Scientific code scope is dirty' }; git log -1 --oneline
```

### Step 1 — run both lanes concurrently

GPU 0 — append terminal private `A` to the existing selected-row gold-CE
parent, then evaluate the terminal adapter on all five sets.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $R='experiments/federated/results/federated__fedavg_pub__s0__4d679d6668dd__37fd379d__r1'; $P='processed_data/protocol_v2/BIRD/original_train9428_dev1534/teacher_targets/qwen7b_to_qwen15b_evidence_s0/exmatch_bird_pair_timeout30_v2_gold/train.csv'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; $O='artifacts/protocol_v2/p26_matched_selected_gold_s0/terminal_a'; $ST='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $BT='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $Sets=@(@{Name='spider';Train=$ST;Test='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv';Profile='spider';N=1034},@{Name='realistic';Train=$ST;Test='processed_data/SPIDER_REALISTIC/test.csv';Profile='spider';N=508},@{Name='syn';Train=$ST;Test='processed_data/SPIDER_SYN/test.csv';Profile='spider';N=1034},@{Name='dk';Train=$ST;Test='processed_data/SPIDER_DK/test.csv';Profile='spider';N=535},@{Name='bird';Train=$BT;Test='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv';Profile='bird_with_evidence';N=1534}); foreach ($X in @("$R/metrics.json","$R/config.json","$P")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P2.6 prerequisite: $X" } }; $C=Get-Content -LiteralPath "$R/config.json" -Raw | ConvertFrom-Json; $M=Get-Content -LiteralPath "$R/metrics.json" -Raw | ConvertFrom-Json; if ($C.pool -ne $P -or $M.server_training.train_config.epochs -ne 1 -or $M.server_training.n_examples -ne 5319 -or $M.server_training.train_config.kd_direction -ne 'none') { throw 'Matched-gold parent contract mismatch' }; uv run python experiments/federated/run.py stage private --parent-result $R --split-dir $S --n-clients 5 --local-epochs 1 --client-train-k 0 --client-dataset-profile spider --aggregation-protocol plaintext --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --stage p26_matched_selected_gold_terminal_s0 --out $O; if ($LASTEXITCODE -ne 0) { throw 'P2.6 terminal matched-gold training stopped; rerun this exact line' }; $V=Get-Content -LiteralPath "$O/stage.json" -Raw | ConvertFrom-Json; if ($V.version -ne 2 -or $V.chain -ne 'A>K[ce]>A' -or -not (Test-Path -LiteralPath "$O/fedavg_adapter/adapter_config.json")) { throw "P2.6 terminal stage contract mismatch: $($V.chain)" }; foreach ($Set in $Sets) { $E="artifacts/eval_resume/protocol_v2/p26_matched_gold_terminal_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $Set.Train --test-csv $Set.Test --dataset-profile $Set.Profile --arms "matched_gold_terminal=$O/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "P2.6 terminal evaluation failed for $($Set.Name); rerun this exact line" }; $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $Q=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $Q.status -eq 'completed' -and @($Q.artifacts.predictions).Count -eq 1 } catch { $false } }); if ($Done.Count -lt 1) { throw "No completed terminal manifest for $($Set.Name)" } }; Write-Host 'GPU-0 complete: selected-row matched-gold terminal endpoint trained and evaluated'
```

GPU 1 — evaluate the already published matched-gold public adapter. This lane
does not retrain it.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $R='experiments/federated/results/federated__fedavg_pub__s0__4d679d6668dd__37fd379d__r1'; $P='processed_data/protocol_v2/BIRD/original_train9428_dev1534/teacher_targets/qwen7b_to_qwen15b_evidence_s0/exmatch_bird_pair_timeout30_v2_gold/train.csv'; $A='artifacts/protocol_v2/p22_spider_private_t1/matched_gold_ce_s0/round_1/m_g'; $ST='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $BT='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $Sets=@(@{Name='spider';Train=$ST;Test='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv';Profile='spider';N=1034},@{Name='realistic';Train=$ST;Test='processed_data/SPIDER_REALISTIC/test.csv';Profile='spider';N=508},@{Name='syn';Train=$ST;Test='processed_data/SPIDER_SYN/test.csv';Profile='spider';N=1034},@{Name='dk';Train=$ST;Test='processed_data/SPIDER_DK/test.csv';Profile='spider';N=535},@{Name='bird';Train=$BT;Test='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv';Profile='bird_with_evidence';N=1534}); foreach ($X in @("$R/metrics.json","$R/config.json","$A/adapter_config.json","$P")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P2.6 prerequisite: $X" } }; $C=Get-Content -LiteralPath "$R/config.json" -Raw | ConvertFrom-Json; $M=Get-Content -LiteralPath "$R/metrics.json" -Raw | ConvertFrom-Json; if ($C.pool -ne $P -or $M.server_training.train_config.epochs -ne 1 -or $M.server_training.n_examples -ne 5319 -or $M.server_training.train_config.kd_direction -ne 'none' -or ([string]$M.m_g).Replace('\','/') -ne $A) { throw 'Matched-gold public adapter contract mismatch' }; foreach ($Set in $Sets) { $E="artifacts/eval_resume/protocol_v2/p26_matched_gold_public_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $Set.Train --test-csv $Set.Test --dataset-profile $Set.Profile --arms "matched_gold_public=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "P2.6 public evaluation failed for $($Set.Name); rerun this exact line" }; $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $Q=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $Q.status -eq 'completed' -and @($Q.artifacts.predictions).Count -eq 1 } catch { $false } }); if ($Done.Count -lt 1) { throw "No completed public manifest for $($Set.Name)" } }; Write-Host 'GPU-1 complete: selected-row matched-gold public endpoint evaluated on five sets'
```

Both commands are resumable by rerunning the exact same line. Do not pull,
commit or publish while either lane is active.

### Step 2 — publish after both lanes finish

This command stages only the terminal federated row and the exact ten compact
evaluation triplets. It never stages adapters, caches or resume artifacts.

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $O='artifacts/protocol_v2/p26_matched_selected_gold_s0/terminal_a'; $A0='artifacts/protocol_v2/p22_spider_private_t1/matched_gold_ce_s0/round_1/m_g'; $A1="$O/fedavg_adapter"; $St=Get-Content -LiteralPath "$O/stage.json" -Raw | ConvertFrom-Json; if ($St.version -ne 2 -or $St.chain -ne 'A>K[ce]>A') { throw 'P2.6 terminal stage is missing or invalid' }; $Hits=@(Get-ChildItem -LiteralPath 'experiments/federated/results' -Directory -Filter 'federated_stage__*' | Where-Object { try { $M=Get-Content -LiteralPath (Join-Path $_.FullName 'metrics.json') -Raw | ConvertFrom-Json; $C=Get-Content -LiteralPath (Join-Path $_.FullName 'config.json') -Raw | ConvertFrom-Json; $M.stage_id -eq $St.stage_id -and $M.stage -eq 'p26_matched_selected_gold_terminal_s0' -and $C.out -eq $O } catch { $false } }); if ($Hits.Count -ne 1) { throw "Expected one P2.6 terminal result row, found $($Hits.Count)" }; $Files=[System.Collections.Generic.List[string]]::new(); $Files.Add((Join-Path $Hits[0].FullName 'metrics.json')); $Files.Add((Join-Path $Hits[0].FullName 'config.json')); foreach ($Lane in @(@{Name='public';Arm='matched_gold_public';Adapter=$A0},@{Name='terminal';Arm='matched_gold_terminal';Adapter=$A1})) { foreach ($Set in @('spider','realistic','syn','dk','bird')) { $E="artifacts/eval_resume/protocol_v2/p26_matched_gold_$($Lane.Name)_${Set}_s0/eval_k0"; $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $C=Get-Content -LiteralPath $V.artifacts.config -Raw | ConvertFrom-Json; $V.status -eq 'completed' -and @($V.artifacts.predictions).Count -eq 1 -and @($C.arms).Count -eq 1 -and $C.arms[0] -eq "$($Lane.Arm)=$($Lane.Adapter)" -and $C.resume_dir -eq $E -and (Test-Path -LiteralPath $V.artifacts.metrics) -and (Test-Path -LiteralPath $V.artifacts.config) -and (Test-Path -LiteralPath $V.artifacts.predictions[0]) } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one exact P2.6 eval for $($Lane.Name)/${Set}, found $($Done.Count)" }; $V=Get-Content -LiteralPath $Done[0].FullName -Raw | ConvertFrom-Json; $Files.Add([string]$V.artifacts.metrics); $Files.Add([string]$V.artifacts.config); $Files.Add([string]$V.artifacts.predictions[0]) } }; $Sep=[IO.Path]::DirectorySeparatorChar; $Root=(Resolve-Path -LiteralPath '.').Path.TrimEnd($Sep)+$Sep; $Rel=@($Files | ForEach-Object { $F=(Resolve-Path -LiteralPath $_).Path; if (-not $F.ToLowerInvariant().StartsWith($Root.ToLowerInvariant())) { throw "Outside repository: $F" }; $F.Substring($Root.Length).Replace([string]$Sep,'/') } | Sort-Object -Unique); git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'P2.6 staging failed' }; $Got=@(git diff --cached --name-only | Sort-Object); $Want=@(git diff HEAD --name-only -- $Rel | Sort-Object); if ($Got.Count -ne $Want.Count -or @(Compare-Object $Got $Want).Count -ne 0) { throw 'P2.6 staged allowlist mismatch' }; git commit -m 'results: publish P2.6 matched selected-gold endpoints'; if ($LASTEXITCODE -ne 0) { throw 'P2.6 commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'P2.6 push failed' }; git log -1 --oneline
```

## Decision after P2.6

Compare matched-gold versus SeqKD at both public and terminal endpoints using
EX, paired wins/losses and exact McNemar tests on all five sets.

- Promote SeqKD only if terminal BIRD improves by at least 1.0 point,
  Spider-family mean improves by at least 0.5 point, and no individual Spider
  evaluation regresses by more than 1.0 point.
- If SeqKD passes, next implement a terminal knowledge-retention objective and
  only then schedule matched SeqKD-2 versus gold-CE-2 from the common FL parent.
- If SeqKD fails, do not spend GPU time on repeated flat offline KD. Run the
  bounded structured-rationale quality/length screen before implementing a new
  teacher objective.
