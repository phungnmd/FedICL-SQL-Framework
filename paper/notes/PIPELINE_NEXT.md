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
| P2.2d | Spider-private/BIRD-public Hinton-FKL T1 headline suite | run complete; compact result publication/audit pending |
| P2.2c | Reverse matched T1 ladder | run complete; compact result publication/audit pending |
| P2.2e | Full-BIRD-public gold CE T1 control | training complete |
| P2.2f | Full-gold CE five-set evaluation | complete; compact publication pending |
| P2.3a | Implement/audit terminal private FedAvg endpoint | next active task |
| P2.3b | Compare `A`, `A→K`, `A→A`, `A→K→A` at T1 | highest method-selection experiment |
| P2.3c | Select or improve KD/federated mechanism | only after the endpoint gate |

## Latest decision evidence (operator-verified manifests; publication pending)

P2.2d completed on 2026-09-13. Hinton FKL versus Pure FL EX is 58.32 versus
57.35 on Spider, 42.72 versus 54.92 on Realistic, 44.58 versus 49.32 on SYN,
45.42 versus 45.23 on DK, and 36.70 versus 14.80 on BIRD. Relative to SeqKD,
Hinton is +0.39/+2.02 points on Spider/BIRD but -3.93/-3.68/-0.19 on
Realistic/SYN/DK. Across Spider, Realistic, SYN, and DK, Hinton averages 47.76
EX versus 51.71 for Pure FL; on the three Spider robustness variants alone it
loses 5.58 points.

This is a public-domain adaptation/retention failure, not evidence that Hinton
logits alone improve the federated method. Run full-public-gold CE next to
separate public SFT from soft-logit value. In parallel, implement the terminal
`A -> K -> A` endpoint, but do not launch it until the Hinton and full-gold CE
artifacts have been audited. The current headline evaluation used batch size
16, so its shared-arm values must not silently overwrite earlier batch-size-8
rows before prediction/config reconciliation.

P2.2f now isolates the no-logit control. Full-gold CE EX is 55.0 Spider, 47.0
Realistic, 43.9 SYN, 40.9 DK, and 32.1 BIRD. Hinton improves over that control
by +3.32/+0.68/+4.52/+4.60 points on Spider/SYN/DK/BIRD, but loses 4.28 on
Realistic. Thus forward-KL logits contribute beyond public gold CE, while both
public-terminal updates still damage private-domain robustness relative to
Pure FL. P2.3a is now the next method task: implement terminal private
re-anchoring and compare `A -> K -> A` with matched `A -> A`.

## Completed command — evaluate full-public-gold CE on five sets

The P2.2e adapter is complete. Evaluate only that new arm because Pure FL,
SeqKD, and Hinton predictions already exist from the batch-size-16 headline
suite. The five deterministic resume roots keep each dataset independently
resumable.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $ST='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $BT='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $B='artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1'; $AG="$B/full_gold_ce_s0/round_1/m_g"; if (-not (Test-Path -LiteralPath "$AG/adapter_config.json")) { throw "Missing full-gold CE adapter: $AG" }; $Sets=@(@{Name='spider';Train=$ST;Test='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv';Profile='spider'},@{Name='realistic';Train=$ST;Test='processed_data/SPIDER_REALISTIC/test.csv';Profile='spider'},@{Name='syn';Train=$ST;Test='processed_data/SPIDER_SYN/test.csv';Profile='spider'},@{Name='dk';Train=$ST;Test='processed_data/SPIDER_DK/test.csv';Profile='spider'},@{Name='bird';Train=$BT;Test='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv';Profile='bird_with_evidence'}); foreach ($Set in $Sets) { foreach ($P in @($Set.Train,$Set.Test)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing evaluation input: $P" } }; $E="artifacts/eval_resume/protocol_v2/p22f_fullgold_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $Set.Train --test-csv $Set.Test --dataset-profile $Set.Profile --arms "full_gold_ce_t1=$AG" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Full-gold CE evaluation failed: $($Set.Name); rerun this exact line" }; $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $V.status -eq 'completed' -and @($V.artifacts.predictions).Count -eq 1 -and (Test-Path -LiteralPath $V.artifacts.metrics) -and (Test-Path -LiteralPath $V.artifacts.config) -and (Test-Path -LiteralPath $V.artifacts.predictions[0]) } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one completed full-gold manifest for $($Set.Name), found $($Done.Count)" } }; Write-Host 'P2.2f complete: full-gold CE evaluated on Spider, Realistic, SYN, DK, and BIRD'
```

After the run exits, publish the compact P2.2e training record and five P2.2f
evaluation records. This allowlist never stages adapters, caches, checkpoints,
or resume manifests under `artifacts/`.

```powershell
$Stage='p22d_spider_private_full_gold_ce_t1'; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $Files=[System.Collections.Generic.List[string]]::new(); $Train=@(Get-ChildItem -LiteralPath 'experiments/federated/results' -Recurse -Filter 'config.json' -File | Where-Object { try { (Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json).stage -eq $Stage } catch { $false } }); if ($Train.Count -ne 1) { throw "Expected one training result for ${Stage}, found $($Train.Count)" }; $Files.Add($Train[0].FullName); $TM=Join-Path $Train[0].Directory.FullName 'metrics.json'; if (-not (Test-Path -LiteralPath $TM)) { throw "Missing training metrics: $TM" }; $Files.Add($TM); foreach ($Name in @('spider','realistic','syn','dk','bird')) { $D="artifacts/eval_resume/protocol_v2/p22f_fullgold_${Name}_s0/eval_k0/manifests"; $Done=@(Get-ChildItem -LiteralPath $D -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $V.status -eq 'completed' -and @($V.artifacts.predictions).Count -eq 1 -and (Test-Path -LiteralPath $V.artifacts.metrics) -and (Test-Path -LiteralPath $V.artifacts.config) -and (Test-Path -LiteralPath $V.artifacts.predictions[0]) } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one completed manifest for ${Name}, found $($Done.Count)" }; $V=Get-Content -LiteralPath $Done[0].FullName -Raw | ConvertFrom-Json; $Files.Add([string]$V.artifacts.metrics); $Files.Add([string]$V.artifacts.config); $Files.Add([string]$V.artifacts.predictions[0]) }; $Sep=[IO.Path]::DirectorySeparatorChar; $Root=(Resolve-Path -LiteralPath '.').Path.TrimEnd($Sep)+$Sep; $Rel=@($Files | ForEach-Object { $F=(Resolve-Path -LiteralPath $_).Path; if (-not $F.ToLowerInvariant().StartsWith($Root.ToLowerInvariant())) { throw "Outside repository: $F" }; $F.Substring($Root.Length).Replace([string]$Sep,'/') } | Sort-Object -Unique); git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'git add failed' }; $Staged=@(git diff --cached --name-only | Sort-Object); if (@(Compare-Object $Rel $Staged).Count -ne 0) { git diff --cached --name-only; throw 'Staged allowlist mismatch' }; git commit -m 'results: publish full-gold CE transfer control'; if ($LASTEXITCODE -ne 0) { throw 'Result commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'Result push failed' }; git log -1 --oneline
```

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

## Active two-GPU launch

Run these in two independent PowerShell terminals. Both are exact-rerun safe;
do not pull, checkout, commit, or edit the server worktree until both exit.

GPU 0 runs the Spider-public -> BIRD-private matched T1 ladder from one shared
BIRD client/FedAvg stage, then evaluates all three arms with the official BIRD
30-second pair evaluator:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/BIRD/original_train9428_dev1534/federated_noniid/alpha_0.5/k5'; $P='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/teacher_targets/qwen7b_to_qwen15b_s0/exmatch_spider_result_eq_v1/train.csv'; $G='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/teacher_targets/qwen7b_to_qwen15b_s0/exmatch_spider_result_eq_v1_gold/train.csv'; $T='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $D='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv'; $B='artifacts/protocol_v2/p22_bird_private_t1'; $C="$B/shared_clients_s0/round_1"; $E='artifacts/eval_resume/protocol_v2/p22_bird_private_t1_ce_ladder_s0/eval_k0'; $Common=@('--split-dir',$S,'--n-clients','5','--local-epochs','1','--client-train-k','0','--client-dataset-profile','bird_with_evidence','--server-dataset-profile','spider','--model','Qwen/Qwen2.5-1.5B-Instruct','--lora-r','16','--lr','0.0002','--max-len','7168','--truncation-policy','error','--gradient-checkpointing','--batch-size','1','--grad-accum','16','--save-steps','200','--aggregation-protocol','plaintext','--seed','0'); uv run python experiments/federated/run.py round --arm fedavg --round 1 --client-out $C --out "$B/pure_fl_s0" --stage p22_bird_private_pure_fl_t1 @Common; if ($LASTEXITCODE -ne 0) { throw 'BIRD-private Pure-FL T1 stopped; rerun this exact line' }; $A0="$C/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A0/adapter_config.json")) { throw "Missing BIRD-private shared FedAvg adapter: $A0" }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --client-out $C --out "$B/matched_gold_ce_s0" --pool $G --pool-size 0 --distill-steps 0 --k-teacher 0 --stage p22_bird_private_matched_gold_ce_t1 @Common; if ($LASTEXITCODE -ne 0) { throw 'BIRD-private matched-gold T1 stopped; rerun this exact line' }; $AG="$B/matched_gold_ce_s0/round_1/m_g"; if (-not (Test-Path -LiteralPath "$AG/adapter_config.json")) { throw "Missing BIRD-private matched-gold adapter: $AG" }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --client-out $C --out "$B/seqkd_s0" --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --stage p22_bird_private_seqkd_t1 @Common; if ($LASTEXITCODE -ne 0) { throw 'BIRD-private SeqKD T1 stopped; rerun this exact line' }; $AS="$B/seqkd_s0/round_1/m_g"; if (-not (Test-Path -LiteralPath "$AS/adapter_config.json")) { throw "Missing BIRD-private SeqKD adapter: $AS" }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $T --test-csv $D --dataset-profile bird_with_evidence --arms "pure_fl_t1=$A0" "matched_gold_ce_t1=$AG" "seqkd_t1=$AS" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 1 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'BIRD-private matched T1 evaluation stopped; rerun this exact line' }; $Head=(git rev-parse --short HEAD).Trim(); $Done=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $F=$V.fingerprint | ConvertFrom-Json; $Arms=@($F.units.arm | Sort-Object -Unique); $Shas=@($F.units.git_sha | Sort-Object -Unique); $Missing=@($V.artifacts.predictions | Where-Object { -not (Test-Path -LiteralPath $_) }); $V.status -eq 'completed' -and ($Arms -join ',') -eq 'matched_gold_ce_t1,pure_fl_t1,seqkd_t1' -and ($Shas -join ',') -eq $Head -and @($V.artifacts.predictions).Count -eq 3 -and $Missing.Count -eq 0 } catch { $false } }); if ($Done.Count -ne 1) { throw "Expected one completed current-HEAD BIRD-private T1 manifest, found $($Done.Count)" }; Write-Host 'GPU-0 complete: reverse matched T1 trained and evaluated'
```

The former GPU-1 command that cached logits on the 5,319 execution-selected
teacher SQL rows is retired. That cache would measure the hybrid
`SeqKD + Hinton FKL`, not canonical Hinton KD. Do not resume it and do not use
it to initialize P2.2d.

After its producer process has exited, permanently delete an accidentally
started partial cache using only the two exact possible roots (active or
previously quarantined). This operator-approved cleanup reclaims disk and
cannot match another cache lineage:

```powershell
$Roots=@('artifacts/protocol_v2/teacher_logit_cache/p22d_bird_to_spider_qwen7b_to_qwen15b_hinton_fkl_t2_full_s0','artifacts/quarantine/protocol_v2/retired_p22d_selected5319_hinton_cache_20260912'); $Repo=(Resolve-Path -LiteralPath '.').Path; $Allowed=[IO.Path]::GetFullPath((Join-Path $Repo 'artifacts'))+[IO.Path]::DirectorySeparatorChar; $Found=@($Roots | Where-Object { Test-Path -LiteralPath $_ }); if ($Found.Count -eq 0) { Write-Host 'No retired 5,319-row Hinton cache exists'; exit 0 }; $Files=0; $Bytes=0; foreach ($P in $Found) { $Resolved=(Resolve-Path -LiteralPath $P).Path; if (-not $Resolved.StartsWith($Allowed,[StringComparison]::OrdinalIgnoreCase)) { throw "Refusing path outside artifacts: $Resolved" }; $Items=@(Get-ChildItem -LiteralPath $P -Recurse -File); $Files+=$Items.Count; $Bytes+=($Items | Measure-Object -Property Length -Sum).Sum }; Write-Host "Deleting $Files files ($([math]::Round($Bytes/1GB,2)) GB) from exact retired roots"; foreach ($P in $Found) { Remove-Item -LiteralPath $P -Recurse -Force; if (Test-Path -LiteralPath $P) { throw "Deletion failed: $P" } }; Write-Host 'Retired 5,319-row Hinton cache deleted permanently'
```

P2.2d will instead compare full public-gold CE against full public-gold CE plus
Hinton forward KL on all 9,428 BIRD training rows. Teacher logits are evaluated
under teacher forcing on the gold-SQL prefix, with BIRD evidence in the prompt.
This uses a new 9,428-row cache and a new output root. It is safe to run beside
the GPU-0 reverse T1 ladder because it loads only the teacher on GPU 1 and
writes to an output-disjoint artifact root. An interrupted invocation resumes
from content-addressed shards; an already completed cache is verified without
rewriting `meta.json`. The 250-GB preflight is a conservative full-vocabulary
fp16 safety budget.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $P='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $C='artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0'; if (-not (Test-Path -LiteralPath $P)) { throw "Missing full BIRD public pool: $P" }; if ((Import-Csv -LiteralPath $P).Count -ne 9428) { throw 'Canonical Hinton pool must contain all 9,428 BIRD training rows' }; $Drive=Get-PSDrive -Name ((Get-Item -LiteralPath '.').PSDrive.Name); if (-not (Test-Path -LiteralPath "$C/meta.json") -and $Drive.Free -lt 250GB) { throw "Canonical Hinton cache needs a 250-GB safety budget; free=$([math]::Round($Drive.Free/1GB,1)) GB" }; git merge-base --is-ancestor 3e85e77 HEAD; if ($LASTEXITCODE -ne 0) { throw 'Current checkout does not contain the Hinton-FKL implementation' }; if (-not (Test-Path -LiteralPath "$C/meta.json")) { uv run python scripts/build_teacher_logit_cache.py --pool $P --dataset-profile bird_with_evidence --pool-size 0 --seed 0 --model Qwen/Qwen2.5-1.5B-Instruct --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 7168 --out $C; if ($LASTEXITCODE -ne 0) { throw 'Canonical 9,428-row Hinton cache stopped; rerun this exact line to resume' } }; $M=Get-Content -LiteralPath "$C/meta.json" -Raw | ConvertFrom-Json; $N=@(Get-ChildItem -LiteralPath $C -Recurse -Filter '*.safetensors' -File).Count; if ($M.kd_objective -ne 'hinton_forward_kl' -or $M.dataset_profile -ne 'bird_with_evidence' -or $M.evidence_mode -ne 'provided' -or $M.n_examples -ne 9428 -or $M.pool_size -ne 0 -or $M.max_len -ne 7168 -or $N -le 0) { throw "Canonical Hinton cache verification failed: objective=$($M.kd_objective) profile=$($M.dataset_profile) evidence=$($M.evidence_mode) meta_n=$($M.n_examples) shards=$N" }; Write-Host "GPU-1 complete: canonical gold-prefix Hinton cache verified; examples=$($M.n_examples) unique_shards=$N"
```

The cache is an intermediate artifact and is never staged. Its pool hash,
configuration and `meta.json` hash will be included in the later Hinton T1
training result; that task receives its own publication command.

### GPU 1 priority — headline Hinton T1 and transfer evaluation

Run Hinton before the full-gold-CE ablation. This reuses the completed
Spider-private T1 clients/FedAvg adapter, trains only the balanced Hinton server
update (`0.5 CE + 0.5 T^2 KL`, `T=2`), and compares Centralized-E3,
Pure-FL-T1, SeqKD-T1 and Hinton-T1 on Spider, Realistic, SYN, DK and BIRD.
Accepted teacher anchors on Spider and BIRD are reused; Qwen-Coder-7B is
evaluated only on the three missing Spider variants. The command is
output-disjoint from the GPU-0 reverse ladder and is exact-rerun safe.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; $P='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $ST='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $SD='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv'; $BT='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $BD='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv'; $C='artifacts/protocol_v2/p22_spider_private_t1/shared_clients_s0/round_1'; $K='artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0'; $B='artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1'; $AC='artifacts/baselines/central_3ep_standard_s0/adapter'; $A0="$C/fedavg_adapter"; $AS='artifacts/protocol_v2/p22_spider_private_t1/seqkd_s0/round_1/m_g'; foreach ($X in @("$AC/adapter_config.json","$A0/adapter_config.json","$AS/adapter_config.json","$K/meta.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing headline prerequisite: $X" } }; $M=Get-Content -LiteralPath "$K/meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 9428 -or $M.kd_objective -ne 'hinton_forward_kl' -or $M.pool_sha256 -ne (Get-FileHash -LiteralPath $P -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'Canonical Hinton cache/pool contract mismatch' }; $Common=@('--split-dir',$S,'--n-clients','5','--local-epochs','1','--client-train-k','0','--client-dataset-profile','spider','--server-dataset-profile','bird_with_evidence','--model','Qwen/Qwen2.5-1.5B-Instruct','--lora-r','16','--lr','0.0002','--max-len','7168','--truncation-policy','error','--gradient-checkpointing','--batch-size','1','--grad-accum','16','--save-steps','200','--aggregation-protocol','plaintext','--pool',$P,'--pool-size','0','--distill-steps','0','--k-teacher','0','--schema-style','full','--retrieval','dail_select','--embedder','BAAI/bge-small-en-v1.5','--tau','0.85','--demo-style','never_schema','--seed','0'); uv run python experiments/federated/run.py round --arm fedkd --round 1 --client-out $C --out "$B/hinton_fkl_t2_alpha05_s0" --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache $K --lambda-ft 0.5 --lambda-kd 0.5 --kl-temperature 2 --stage p22d_spider_private_hinton_fkl_t2_alpha05_t1 @Common; if ($LASTEXITCODE -ne 0) { throw 'Headline Hinton-FKL T1 stopped; rerun this exact line' }; $AH="$B/hinton_fkl_t2_alpha05_s0/round_1/m_g"; if (-not (Test-Path -LiteralPath "$AH/adapter_config.json")) { throw "Missing Hinton adapter: $AH" }; $Sets=@(@{Name='spider';Train=$ST;Test=$SD;Profile='spider'},@{Name='realistic';Train=$ST;Test='processed_data/SPIDER_REALISTIC/test.csv';Profile='spider'},@{Name='syn';Train=$ST;Test='processed_data/SPIDER_SYN/test.csv';Profile='spider'},@{Name='dk';Train=$ST;Test='processed_data/SPIDER_DK/test.csv';Profile='spider'},@{Name='bird';Train=$BT;Test=$BD;Profile='bird_with_evidence'}); foreach ($Set in $Sets) { $E="artifacts/eval_resume/protocol_v2/p22d_headline_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $Set.Train --test-csv $Set.Test --dataset-profile $Set.Profile --arms "centralized_e3=$AC" "pure_fl_t1=$A0" "seqkd_t1=$AS" "hinton_fkl_t1=$AH" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Student headline evaluation failed: $($Set.Name); rerun this exact line" } }; $TeacherSets=@(@{Name='realistic';Test='processed_data/SPIDER_REALISTIC/test.csv'},@{Name='syn';Test='processed_data/SPIDER_SYN/test.csv'},@{Name='dk';Test='processed_data/SPIDER_DK/test.csv'}); foreach ($Set in $TeacherSets) { $E="artifacts/eval_resume/protocol_v2/p22d_teacher_$($Set.Name)_s0/eval_k0"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $ST --test-csv $Set.Test --dataset-profile spider --arms teacher_qwen7b --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-Coder-7B-Instruct --model-4bit --batch-size 1 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Teacher variant evaluation failed: $($Set.Name); rerun this exact line" } }; Write-Host 'GPU-1 headline suite complete: Spider-private FedAvg to BIRD-public Hinton T1 compared across five evaluation sets; teacher variants complete'
```

### Deferred matched ablation — do not run before the headline suite

After the headline suite, GPU 1 reuses the already completed Spider-private T1
clients/FedAvg adapter and runs two full-public-data server updates: gold CE,
then balanced Hinton KD (`0.5 CE + 0.5 T^2 KL`, `T=2`). It then evaluates these
against Pure FL and the separate 5,319-row SeqKD arm on Spider. No client is
retrained, and all roots are disjoint from the GPU-0 reverse ladder.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.5/k5'; $P='processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/train.csv'; $T='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/train.csv'; $D='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv'; $C='artifacts/protocol_v2/p22_spider_private_t1/shared_clients_s0/round_1'; $K='artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0'; $B='artifacts/protocol_v2/p22d_spider_private_fullgold_hinton_t1'; $E='artifacts/eval_resume/protocol_v2/p22d_spider_private_fullgold_hinton_t1_s0/eval_k0'; $A0="$C/fedavg_adapter"; $AS='artifacts/protocol_v2/p22_spider_private_t1/seqkd_s0/round_1/m_g'; foreach ($X in @("$A0/adapter_config.json","$AS/adapter_config.json","$K/meta.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing prerequisite: $X" } }; $M=Get-Content -LiteralPath "$K/meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 9428 -or $M.kd_objective -ne 'hinton_forward_kl' -or $M.pool_sha256 -ne (Get-FileHash -LiteralPath $P -Algorithm SHA256).Hash.ToLowerInvariant()) { throw 'Canonical Hinton cache/pool contract mismatch' }; $Common=@('--split-dir',$S,'--n-clients','5','--local-epochs','1','--client-train-k','0','--client-dataset-profile','spider','--server-dataset-profile','bird_with_evidence','--model','Qwen/Qwen2.5-1.5B-Instruct','--lora-r','16','--lr','0.0002','--max-len','7168','--truncation-policy','error','--gradient-checkpointing','--batch-size','1','--grad-accum','16','--save-steps','200','--aggregation-protocol','plaintext','--pool',$P,'--pool-size','0','--distill-steps','0','--k-teacher','0','--schema-style','full','--retrieval','dail_select','--embedder','BAAI/bge-small-en-v1.5','--tau','0.85','--demo-style','never_schema','--seed','0'); uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --client-out $C --out "$B/full_gold_ce_s0" --stage p22d_spider_private_full_gold_ce_t1 @Common; if ($LASTEXITCODE -ne 0) { throw 'Full-public-gold CE T1 stopped; rerun this exact line' }; $AG="$B/full_gold_ce_s0/round_1/m_g"; if (-not (Test-Path -LiteralPath "$AG/adapter_config.json")) { throw "Missing full-gold adapter: $AG" }; uv run python experiments/federated/run.py round --arm fedkd --round 1 --client-out $C --out "$B/hinton_fkl_t2_alpha05_s0" --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache $K --lambda-ft 0.5 --lambda-kd 0.5 --kl-temperature 2 --stage p22d_spider_private_hinton_fkl_t2_alpha05_t1 @Common; if ($LASTEXITCODE -ne 0) { throw 'Canonical Hinton-FKL T1 stopped; rerun this exact line' }; $AH="$B/hinton_fkl_t2_alpha05_s0/round_1/m_g"; if (-not (Test-Path -LiteralPath "$AH/adapter_config.json")) { throw "Missing Hinton adapter: $AH" }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $T --test-csv $D --dataset-profile spider --arms "pure_fl_t1=$A0" "seqkd_t1=$AS" "full_gold_ce_t1=$AG" "hinton_fkl_t1=$AH" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Canonical Hinton comparison evaluation stopped; rerun this exact line' }; Write-Host 'GPU-1 complete: full-gold CE and canonical Hinton T1 trained and evaluated on Spider'
```

Do not publish while GPU 0 is still using the worktree. After both processes
exit, inspect exact result directories and generate compact allowlists for the
headline and reverse-ladder results. Full-public-gold CE remains the next
matched ablation, but it does not block the Hinton-first headline result.

After the GPU-0 process exits, inspect and publish the reverse T1 result. Do not
run a publication command while another process uses the worktree. The reverse
result publication allowlist is generated only from its three exact stage
labels and completed eval manifest; caches are never staged.

After both GPU commands have exited successfully, publish the reverse result:

```powershell
$Stages=@('p22_bird_private_pure_fl_t1','p22_bird_private_matched_gold_ce_t1','p22_bird_private_seqkd_t1'); $Files=[System.Collections.Generic.List[string]]::new(); foreach ($Stage in $Stages) { $Hits=@(Get-ChildItem -LiteralPath 'experiments/federated/results' -Recurse -Filter 'config.json' -File | Where-Object { try { (Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json).stage -eq $Stage } catch { $false } }); if ($Hits.Count -ne 1) { throw "Expected one federated result for ${Stage}, found $($Hits.Count)" }; $Files.Add($Hits[0].FullName); $Metric=Join-Path $Hits[0].Directory.FullName 'metrics.json'; if (-not (Test-Path -LiteralPath $Metric)) { throw "Missing metrics for $Stage" }; $Files.Add($Metric) }; $EvalHits=@(Get-ChildItem -LiteralPath 'experiments/eval_arms/results' -Recurse -Filter 'config.json' -File | Where-Object { try { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; $Names=@($V.arms | ForEach-Object { ($_ -split '=',2)[0] } | Sort-Object); ($Names -join ',') -eq 'matched_gold_ce_t1,pure_fl_t1,seqkd_t1' -and $V.dataset_profile -eq 'bird_with_evidence' -and $V.test_csv -eq 'processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv' } catch { $false } }); if ($EvalHits.Count -ne 1) { throw "Expected one reverse T1 eval result, found $($EvalHits.Count)" }; $ED=$EvalHits[0].Directory.FullName; foreach ($P in @($EvalHits[0].FullName,(Join-Path $ED 'metrics.json'),(Join-Path $ED 'predictions/pure_fl_t1.csv'),(Join-Path $ED 'predictions/matched_gold_ce_t1.csv'),(Join-Path $ED 'predictions/seqkd_t1.csv'))) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing publication file: $P" }; $Files.Add($P) }; if (@(git diff --cached --name-only).Count -ne 0) { throw 'Index is not empty; review staged files first' }; $Sep=[IO.Path]::DirectorySeparatorChar; $Root=(Resolve-Path -LiteralPath '.').Path.TrimEnd($Sep)+$Sep; $Rel=@($Files | ForEach-Object { $F=(Resolve-Path -LiteralPath $_).Path; if (-not $F.ToLowerInvariant().StartsWith($Root.ToLowerInvariant())) { throw "Outside repository: $F" }; $F.Substring($Root.Length).Replace([string]$Sep,'/') } | Sort-Object -Unique); git add -- $Rel; if ($LASTEXITCODE -ne 0) { throw 'git add failed' }; $Staged=@(git diff --cached --name-only | Sort-Object); if (@(Compare-Object $Rel $Staged).Count -ne 0) { git diff --cached --name-only; throw 'Staged allowlist mismatch' }; git commit -m 'results: publish protocol-v2 BIRD-private T1 ladder'; if ($LASTEXITCODE -ne 0) { throw 'Result commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'Result push failed' }; git log -1 --oneline
```

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
task is to pin the full-public-gold CE and canonical 9,428-row Hinton-FKL
cache/training commands. No T2/T3 job is active.

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

full public-gold CE (all public rows)
  vs the same full-data CE + Hinton forward KL on gold prefixes
```

Open recurring T2/T3 only when T1 shows an interpretable EX gain. Hinton FKL is
the primary token-level soft-logit baseline; SeqKD remains the separate
sequence-level baseline. Do not combine them in the canonical ladder. GKD
(on-policy), MiniLLM, and a newly implemented RKL lineage remain conditional
candidates after both standard baselines are measured. Publication commands are generated after the
completion artifacts are inspected and an exact compact allowlist is known;
model adapters, trainer state, raw caches, and `artifacts/` are never staged.

The first direction does not pass the T2/T3 gate yet: SeqKD is 57.64 EX versus
56.96 for Pure FL, only seven net correct rows (140 corrections, 133
regressions). Run the reverse matched T1 ladder and full-data Hinton-FKL T1 before
selecting the method.

## Next architecture gate — terminal FedAvg after KD

Code audit confirms that the current reference executes client training,
FedAvg, then public server KD and deploys `m_g`; recurring rounds likewise end
after KD. Once the active T1 jobs finish, prioritize a candidate that sends the
post-KD adapter back to clients for one additional local epoch, aggregates the
result, and deploys that final FedAvg adapter.

Use this matched ladder from shared immutable inputs and checkpoints:

```text
A          = one private/FedAvg stage (Pure FL T1)
A -> K     = current Hinton T1 endpoint
A -> A     = two private/FedAvg stages, no KD compute control
A -> K -> A = Hinton T1 plus one terminal private/FedAvg consolidation
```

The promotion gate is primary Spider and Spider-variant EX above both `A -> K`
and `A -> A`, with useful BIRD transfer retained. Record the extra client
compute and communication. Do not open a three-epoch consolidation, recurrent
T2/T3, GKD, MiniLLM, or RKL until this one-epoch endpoint comparison is known.
No execution command is active for P2.3 yet: first implement immutable
fingerprints, correct initialization from the post-KD adapter, a distinct
output root, and final-FedAvg persistence. Do not pull or modify the server
worktree while either current GPU process is alive.
