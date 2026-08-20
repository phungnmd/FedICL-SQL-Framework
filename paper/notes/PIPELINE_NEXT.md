# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every PowerShell
> block below is exactly one physical line, fail-fast, and safe to rerun. The
> governing rules are in `CONVENTION.MD` §6.1.

> **Multi-epoch command rule:** every future `client_train/run.py --epochs N`
> command with `N > 1` must add `--save-epoch-checkpoints`. Epoch directories
> are adapter-only; only `resume_latest/` keeps optimizer/scheduler state. See
> `CONVENTION.MD` §6.1 before emitting or modifying a training command.

## Active task and stop rule

T0 is closed with the **pragmatic RQ2**: demonstrate the client/deployment
resource and communication savings of retaining a 1.5B SLM rather than placing
the 7B teacher on clients or in inference. Full federated 7B training is not
part of the default evidence package.

The matched public-supervision, centralized-recipe, and centralized OOD/BIRD
gates are complete. `Centralized-standard-3ep` is the official baseline; the
historical restart recipe remains schedule-sensitivity evidence. By current
research priority, the next GPU task is a complete second-family Gemma gate.
Gemma targets and logits are regenerated; Qwen artifacts are never mixed into
the Gemma branch. Final T3 seed replication is retained but deferred.

| Order | Action | Status |
|---|---|---|
| P0.0 | Build and verify the exact 3,873-row BIRD-gold control | complete |
| P0.1 | Train the missing public-gold CE server branch from the shared T1 adapter | complete |
| P0.2 | Evaluate the four matched T1 arms on Spider | complete; Gate T1 passed |
| P0.3 | Train standard continuous centralized 3-epoch baseline | complete; 67.31 EX |
| P0.4 | Evaluate both centralized recipes on Spider | complete; no meaningful difference |
| P0.5 | Select the official centralized ceiling | complete; standard continuous selected |
| P0.6 | Evaluate the official centralized baseline on Realistic, Syn, DK, and BIRD | complete; 55.91 / 54.06 / 53.27 / 13.04 EX |
| P0.7a | Smoke Gemma 2B training, adapter load, and inference | complete; pipeline pass, 8-row EX is non-paper diagnostic |
| P0.7b | Smoke Gemma 9B→2B targets, token-ID compatibility, and logit cache | **run next on GPU 0** |
| P0.7c | Generate Gemma 9B targets for all 9,428 BIRD training rows | gated by both smokes |
| P0.7e | EX-match Gemma targets and build its matched-gold control | gated by P0.7c; discovers `N_gemma` |
| P0.7s | Train/evaluate Gemma 2B pure FL | may run concurrently on GPU 1 |
| P0.7d | Gemma T1 five-arm ladder: base, FL, gold CE, target CE, full FedLS | gated by P0.7e |
| P0.8 | Replicate final T3 pure FL vs full FedLS-SQL at training seeds 1/2 on Spider | deferred by current research priority |
| P1.0 | Consolidate adapter-payload communication from committed round metrics | complete; no rerun needed |
| P1.1 | Add warm-up-capable controlled inference benchmark and run 1.5B vs 7B | pending after P0.7 review |

P0.1-P0.4 accuracy is valid, but opportunistic wall-time/RAM values are not
paper resource evidence. Do not rerun P0.3 merely to backfill epoch snapshots:
it completed before the snapshot feature existed. Do not start FedProx,
heterogeneity, sensitivity, or model-size/rank/client sweeps until P0.7 is
reviewed.

## Fixed T1 comparison

All four arms start from the same seed-0, round-1 client training and
factor-wise FedAvg adapter:

```text
artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter
```

| Evaluation arm | Server treatment |
|---|---|
| `fl_t1_shared` | none |
| `public_gold_ce` | CE on BIRD gold for the exact retained 3,873 rows |
| `teacher_target_ce` | CE on teacher-generated SQL (`fedavg_pub`) |
| `fedls_t1` | teacher-target CE + reverse KL (`fedkd`) |

The gold control is reconstructed by the original source `idx` stored in the
selection checkpoint. Never join it by question text: duplicate BIRD questions
make that mapping ambiguous for nine rows.

## P0.0 — build and verify the matched gold control

This command is CPU-only. It atomically rebuilds the CSV, verifies row identity
and count, and writes hashes plus target semantics to a provenance JSON.

```powershell
$O='processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv'; uv run python scripts/build_public_gold_control.py --source-csv processed_data/BIRD/centralized/train.csv --teacher-pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --selection-ckpt processed_data/BIRD/bootstrap_full_exmatch/train.score_ckpt.jsonl --out $O; if ($LASTEXITCODE -ne 0) { throw 'Public-gold control build failed' }; if (-not (Test-Path -LiteralPath $O) -or -not (Test-Path -LiteralPath "${O}.provenance.json")) { throw 'Public-gold output or provenance is missing' }; $N=(Import-Csv -LiteralPath $O).Count; $P=Get-Content -LiteralPath "${O}.provenance.json" -Raw | ConvertFrom-Json; if ($N -ne 3873 -or $P.n_rows -ne 3873 -or $P.target_semantics -ne 'bird_gold_sql') { throw "Public-gold verification failed: rows=$N provenance_rows=$($P.n_rows) target=$($P.target_semantics)" }; Write-Host 'P0.0 complete: exact 3,873-row BIRD-gold control verified'
```

## P0.1 — train only the missing public-gold CE branch

This reuses the immutable shared round-1 client and aggregation stages. On an
exact rerun, completed stages/checkpoints are skipped; configuration drift at
the same output root fails through the existing fingerprints.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $G='artifacts/federated/fedavg_pub_gold_noicl_k5_e1_t1_s0'; foreach ($P in @("$C/fedavg_adapter/adapter_config.json",'processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv','processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv.provenance.json')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing T1 input: $P" } }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool processed_data/BIRD/bootstrap_full_exmatch_gold/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $G --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Public-gold CE branch failed; rerun this exact line to resume' }; foreach ($P in @("$G/round_1/m_g/adapter_config.json","$G/setup.json","$G/manifest.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Incomplete public-gold CE output: $P" } }; Write-Host 'P0.1 complete: matched public-gold CE branch trained'
```

## P0.2 — evaluate the four matched arms

**Completed result (seed 0, Spider, 1,034 identical rows):** FL `57.35`, matched
public-gold CE `57.83`, teacher-target CE `61.32`, and full FedLS-SQL `63.35`
EX. Public gold does not improve over FL (`+0.48 pp`, paired `p=0.800`), while
teacher targets improve over matched public gold (`+3.48 pp`, `p=0.0026`) and
reverse KL adds `+2.03 pp` over teacher-target CE (`p=0.0417`). Treat the RKL
increment as provisional because its three-seed training-level contrast is not
yet significant. Canonical committed result:
`experiments/eval_arms/results/eval_arms__s0__20260820T065954/`.

The resume directory is unique to this comparison. `--skip-completed` makes a
completed exact rerun a no-op and a partial run resumes from its JSONL rows.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $G='artifacts/federated/fedavg_pub_gold_noicl_k5_e1_t1_s0/round_1/m_g'; $H='artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g'; $K='artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g'; $E='artifacts/eval_resume/fedls_t1_public_supervision_s0/eval_k0'; foreach ($A in @("$C/fedavg_adapter",$G,$H,$K)) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing evaluation adapter: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_t1_shared=$C/fedavg_adapter" "public_gold_ce=$G" "teacher_target_ce=$H" "fedls_t1=$K" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Matched T1 evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifests: $E/manifests" }; Write-Host 'P0.2 complete: stop and review the four-arm T1 result'
```

## P0.3 — standard continuous centralized baseline

The existing `central_3ep` is three independently scheduled one-epoch passes.
Keep it as `Centralized-3pass-restart`; it is process-matched to three FL
rounds but is not a conventional three-epoch run. The command below is retained
as executed provenance: it created the standard baseline with one optimizer
and one cosine schedule across all three epochs before epoch snapshots were
implemented. Do not modify or rerun it merely to backfill snapshots. A
completed adapter is skipped; a partial `_ckpt` resumes.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $O='artifacts/baselines/central_3ep_standard_s0/adapter'; if (Test-Path -LiteralPath "$O/adapter_config.json") { Write-Host "P0.3 already complete: $O" } else { uv run python experiments/client_train/run.py --client processed_data/SPIDER/centralized/train.csv --out $O --kd-direction none --epochs 3 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Standard centralized 3-epoch training failed; rerun this exact line to resume' } }; if (-not (Test-Path -LiteralPath "$O/adapter_config.json")) { throw "Incomplete standard centralized adapter: $O" }; Write-Host 'P0.3 complete: standard continuous centralized 3-epoch adapter ready'
```

## P0.4 — compare centralized recipes

This completed comparison evaluates the conventional continuous recipe and the
existing restart recipe on identical Spider rows. The standard recipe is the
paper baseline; the statistically indistinguishable restart result is retained
as schedule sensitivity.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S='artifacts/baselines/central_3ep_standard_s0/adapter'; $R='artifacts/probe_p/central_3ep/adapter'; $E='artifacts/eval_resume/central_3ep_recipe_check_s0/eval_k0'; foreach ($A in @($S,$R)) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing centralized adapter: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "central_3ep_standard=$S" "central_3pass_restart=$R" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Centralized recipe evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing centralized evaluation manifests: $E/manifests" }; Write-Host 'P0.4 complete: stop and review both centralized recipes'
```

## P0.5 — centralized review and next-block gate

Gate T1 is already decided: additional public supervision does not explain the
FedLS-SQL gain, teacher-generated hard targets provide the clearest causal
increment, and reverse KL provides a smaller positive increment whose
across-seed reliability remains unresolved. The server stage also reduces
execution errors from `22.82%` for FL to `12.86%` for full FedLS-SQL.

P0.5 is complete. Standard continuous reaches `67.31 EX`, `64.41 EM`, and
`14.31%` execution errors; three-pass restart reaches `67.60 EX`, `62.67 EM`,
and `15.76%` errors. Their paired EX difference is `0.29 pp` (`p=0.863`), so
the conventional standard recipe is selected rather than choosing three noisy
EX wins. Never relabel `central_3pass_restart` as standard three-epoch training.

## P0.6 — official centralized transfer/OOD cells (complete)

The selected standard continuous adapter reaches `55.91` Realistic, `54.06`
Syn, `53.27` DK, and `13.04` BIRD EX. Config, metrics, and all prediction rows
were validated and committed in the nested code repository as `7eb7d44` (run
code SHA `05389ad`). Timings are not paper resource evidence because this was
an accuracy run on a shared server. The executed command remains below as
provenance and an exact completed rerun is a no-op.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $A='artifacts/baselines/central_3ep_standard_s0/adapter'; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing official centralized adapter: $A" }; foreach ($D in @(@{Test='processed_data/SPIDER_REALISTIC/test.csv';Tag='realistic'},@{Test='processed_data/SPIDER_SYN/test.csv';Tag='syn'},@{Test='processed_data/SPIDER_DK/test.csv';Tag='dk'},@{Test='processed_data/BIRD/centralized/test.csv';Tag='bird'})) { $E="artifacts/eval_resume/central_3ep_standard_$($D.Tag)_s0/eval_k0"; Write-Host "=== Centralized-standard-3ep: $($D.Test)"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $D.Test --arms "central_3ep_standard=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Centralized transfer evaluation failed: $($D.Test)" }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifests: $E/manifests" } }; Write-Host 'P0.6 complete: stop, commit results, and review the final-model table before any new GPU block'
```

## P0.7 — complete Gemma-family portability gate

This gate replicates the **selection rule**, not Qwen's selected row identities.
Gemma 2 9B generates SQL for all 9,428 BIRD training rows, then its own targets
are execution-matched against BIRD gold. Let the retained count be
`N_gemma`; it is discovered by P0.7e and must not be hard-coded to 3,873.
Within the Gemma ladder, gold CE, target CE, and CE+RKL use exactly those same
`N_gemma` rows. Qwen targets, Qwen-selected indices, and Qwen logits are never
inputs to this branch.

The pair is `google/gemma-2-9b-it` teacher and
`google/gemma-2-2b-it` student. Exact token-ID equality is checked before
reverse KL is accepted.

### P0.7a — Gemma 2B client smoke (complete)

The adapter trained, reloaded, and evaluated successfully. The eight-row
diagnostic produced `37.5 EX`, `12.5 EM`, and one execution error. These
numbers are not paper evidence; the compatibility decision is **pass**.

### P0.7b — Gemma teacher/tokenizer/cache smoke on GPU 0

This technical smoke uses the first eight rows of the complete BIRD training
source. It checks model access, generation, exact Gemma 9B/2B token IDs, and
the teacher forward/logit path; it does not determine the selected pool.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='processed_data/BIRD/centralized/train.csv'; $P='processed_data/BIRD/gemma2_9b_targets_smoke8_fullsource/train.csv'; $C='artifacts/teacher_logit_cache/gemma2_9b_to_2b_smoke8_fullsource_k0'; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 2 --max-new-tokens 128 --schema-style full --limit 8 --out $P --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma target/tokenizer smoke failed; rerun this exact line to resume' }; if ((Import-Csv -LiteralPath $P).Count -ne 8 -or -not (Test-Path -LiteralPath "${P}.provenance.json")) { throw 'Gemma smoke target verification failed' }; uv run python scripts/build_teacher_logit_cache.py --pool $P --pool-size 0 --seed 0 --model google/gemma-2-2b-it --teacher-model google/gemma-2-9b-it --teacher-4bit --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --out $C; if ($LASTEXITCODE -ne 0) { throw 'Gemma teacher-logit smoke failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$C/meta.json")) { throw "Missing Gemma smoke cache metadata: $C/meta.json" }; Write-Host 'P0.7b complete: teacher generation and RKL path passed'
```

### P0.7c — generate all Gemma teacher targets on GPU 0

The source is all 9,428 BIRD training rows. Generation checkpoints each row at
`train.ckpt.jsonl`; rerunning this exact command resumes safely.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='processed_data/BIRD/centralized/train.csv'; $R='processed_data/BIRD/gemma2_9b_bootstrap_full/train.csv'; if (-not (Test-Path -LiteralPath $S)) { throw "Missing full BIRD source: $S" }; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 4 --max-new-tokens 128 --schema-style full --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Full Gemma target generation failed; rerun this exact line to resume' }; $N=(Import-Csv -LiteralPath $R).Count; $V=Get-Content -LiteralPath "${R}.provenance.json" -Raw | ConvertFrom-Json; if ($N -ne 9428 -or $V.n_output_rows -ne 9428 -or $V.n_nonempty_targets -ne 9428 -or -not $V.tokenizer_compatibility.compatible) { throw "Full Gemma target verification failed: csv=$N provenance=$($V.n_output_rows) nonempty=$($V.n_nonempty_targets) tokenizer=$($V.tokenizer_compatibility.compatible)" }; Write-Host 'P0.7c complete: all 9,428 Gemma targets generated'
```

### P0.7e — derive the Gemma-specific EX-match pool and gold control

This CPU step reproduces the canonical Qwen selection recipe: first reject
teacher SQL that cannot finish within the fixed 8-second quick-execution
timeout, then apply the official EX comparison against BIRD gold to survivors.
Both checkpoints are resumable and fingerprinted. It retains teacher SQL only
for official `match` rows and reconstructs BIRD gold on those exact indices.
The resulting `N_gemma` is a measured property of Gemma.

```powershell
$S='processed_data/BIRD/centralized/train.csv'; $R='processed_data/BIRD/gemma2_9b_bootstrap_full/train.csv'; $X='processed_data/BIRD/gemma2_9b_bootstrap_full_exec/train.csv'; $P='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.csv'; $G='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch_gold/train.csv'; foreach ($I in @($S,$R,"${R}.provenance.json")) { if (-not (Test-Path -LiteralPath $I)) { throw "Missing P0.7e input: $I" } }; uv run python scripts/filter_teacher_targets_exmatch.py --source-csv $S --teacher-targets $R --exec-out $X --exec-timeout 8 --out $P --workers 8; if ($LASTEXITCODE -ne 0) { throw 'Gemma quick-exec/EX filtering failed; rerun this exact line to resume' }; uv run python scripts/build_public_gold_control.py --source-csv $S --teacher-pool $P --selection-ckpt processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.score_ckpt.jsonl --out $G; if ($LASTEXITCODE -ne 0) { throw 'Gemma matched-gold control build failed' }; $NX=(Import-Csv -LiteralPath $X).Count; $N=(Import-Csv -LiteralPath $P).Count; $NG=(Import-Csv -LiteralPath $G).Count; $V=Get-Content -LiteralPath "${P}.provenance.json" -Raw | ConvertFrom-Json; $VG=Get-Content -LiteralPath "${G}.provenance.json" -Raw | ConvertFrom-Json; if ($N -le 0 -or $N -ne $NG -or $N -ne $V.n_exmatched -or $N -ne $VG.n_rows -or $V.n_generated -ne 9428 -or $NX -ne $V.n_exec_kept -or $V.n_scored -ne $V.n_exec_kept) { throw "Gemma pool verification failed: generated=$($V.n_generated) exec=$NX official_scored=$($V.n_scored) matched=$N gold=$NG" }; Write-Host "P0.7e complete: Gemma-specific matched pool has N_gemma=$N rows"
```

### P0.7s — independent pure-FL lane on GPU 1

Before `N_gemma` exists, only pure FL is independent of the teacher. Run this
concurrently with P0.7b-c. Do not train gold CE on Qwen's 3,873 selected rows.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $M='google/gemma-2-2b-it'; $F='artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0'; $E='artifacts/eval_resume/gemma2_2b_t1_fl_s0/eval_k0'; foreach ($X in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv')) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.7s input: $X" } }; uv run python experiments/federated/run.py run --arm fedavg --rounds 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $F --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma pure-FL T1 failed; rerun this exact line to resume' }; $A="$F/round_1/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing Gemma FL adapter: $A" }; uv run python experiments/eval_arms/run.py --model $M --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "gemma_fl_t1=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 8 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Gemma pure-FL evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing Gemma FL manifests: $E/manifests" }; Write-Host 'P0.7s complete: pure FL is ready for matched-ladder reuse'
```

### Overnight parallel launch

Run this teacher lane on GPU 0 and P0.7s above on GPU 1. If the old command is
only downloading the model, stop it and use this corrected line; the local
model cache remains reusable. The final execution-match stage is the relevant
teacher-supervision quality gate. A separate held-out teacher zero-shot
benchmark is optional P1.1 evidence, not a prerequisite for the Gemma ladder.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='processed_data/BIRD/centralized/train.csv'; $Q='processed_data/BIRD/gemma2_9b_targets_smoke8_fullsource/train.csv'; $C='artifacts/teacher_logit_cache/gemma2_9b_to_2b_smoke8_fullsource_k0'; $R='processed_data/BIRD/gemma2_9b_bootstrap_full/train.csv'; $X='processed_data/BIRD/gemma2_9b_bootstrap_full_exec/train.csv'; $P='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.csv'; $G='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch_gold/train.csv'; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 2 --max-new-tokens 128 --schema-style full --limit 8 --out $Q --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma target/tokenizer smoke failed; rerun this exact line to resume' }; uv run python scripts/build_teacher_logit_cache.py --pool $Q --pool-size 0 --seed 0 --model google/gemma-2-2b-it --teacher-model google/gemma-2-9b-it --teacher-4bit --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --out $C; if ($LASTEXITCODE -ne 0) { throw 'Gemma teacher-logit smoke failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$C/meta.json")) { throw "Missing Gemma smoke cache metadata: $C/meta.json" }; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 4 --max-new-tokens 128 --schema-style full --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Full Gemma target generation failed; rerun this exact line to resume' }; $NR=(Import-Csv -LiteralPath $R).Count; if ($NR -ne 9428) { throw "Expected 9,428 raw Gemma targets, found $NR" }; uv run python scripts/filter_teacher_targets_exmatch.py --source-csv $S --teacher-targets $R --exec-out $X --exec-timeout 8 --out $P --workers 8; if ($LASTEXITCODE -ne 0) { throw 'Gemma quick-exec/EX filtering failed; rerun this exact line to resume' }; uv run python scripts/build_public_gold_control.py --source-csv $S --teacher-pool $P --selection-ckpt processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.score_ckpt.jsonl --out $G; if ($LASTEXITCODE -ne 0) { throw 'Gemma matched-gold control build failed' }; $NX=(Import-Csv -LiteralPath $X).Count; $N=(Import-Csv -LiteralPath $P).Count; $NG=(Import-Csv -LiteralPath $G).Count; $V=Get-Content -LiteralPath "${P}.provenance.json" -Raw | ConvertFrom-Json; if ($N -le 0 -or $N -ne $NG -or $N -ne $V.n_exmatched -or $V.n_generated -ne 9428 -or $NX -ne $V.n_exec_kept -or $V.n_scored -ne $V.n_exec_kept) { throw "Gemma pool verification failed: generated=$($V.n_generated) exec=$NX official_scored=$($V.n_scored) matched=$N gold=$NG" }; Write-Host "GPU-0 lane complete: N_gemma=$N targets and matched gold rows are ready"
```

### P0.7d — Gemma-specific five-arm T1 ladder

All server-treated arms use the same Gemma-selected `N_gemma` identities:
BIRD gold CE, Gemma target CE, or Gemma target CE plus online reverse KL. Pure
FL shares the identical private-client/FedAvg stage and has no public stage.
The untouched Gemma 2B base arm anchors whether private federated training and
the complete framework improve or degrade the pretrained student.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $M='google/gemma-2-2b-it'; $T='google/gemma-2-9b-it'; $P='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.csv'; $GOLD='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch_gold/train.csv'; $F='artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0'; $G='artifacts/federated/gemma2_9b_selected_goldce_noicl_k5_e1_t1_s0'; $H='artifacts/federated/gemma2_9b_to_2b_seqkd_noicl_k5_e1_t1_s0'; $K='artifacts/federated/gemma2_9b_to_2b_fedls_noicl_k5_e1_t1_s0'; $E='artifacts/eval_resume/gemma2_9b_to_2b_t1_five_arm_s0/eval_k0'; foreach ($X in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv',$P,"${P}.provenance.json",$GOLD,"${GOLD}.provenance.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.7d input: $X" } }; $NP=(Import-Csv -LiteralPath $P).Count; $NG=(Import-Csv -LiteralPath $GOLD).Count; if ($NP -le 0 -or $NP -ne $NG) { throw "Gemma supervision pools are not matched: targets=$NP gold=$NG" }; uv run python experiments/federated/run.py run --arm fedavg --rounds 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $F --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma pure-FL T1 failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $GOLD --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out "$F/round_1" --out $G --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma matched gold CE failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out "$F/round_1" --out $H --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma teacher-target CE failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedkd --round 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model $T --teacher-4bit --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out "$F/round_1" --out $K --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Full Gemma FedLS-SQL failed; rerun this exact line to resume' }; foreach ($A in @("$F/round_1/fedavg_adapter","$G/round_1/m_g","$H/round_1/m_g","$K/round_1/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing Gemma T1 adapter: $A" } }; uv run python experiments/eval_arms/run.py --model $M --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "gemma_base=" "gemma_fl_t1=$F/round_1/fedavg_adapter" "gemma_goldce_t1=$G/round_1/m_g" "gemma_seqkd_t1=$H/round_1/m_g" "gemma_fedls_t1=$K/round_1/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 8 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Gemma five-arm T1 evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing Gemma T1 manifests: $E/manifests" }; Write-Host "P0.7d complete: stop and review the five-arm result at N_gemma=$NP"
```

**Interpretation:** this is a method-faithful second-family replication because
both families use full-source generation, the fixed 8-second quick-execution
filter, and official EX matching. It is not an equal-row cross-family
experiment when `N_gemma != 3,873`. If a later
controlled family comparison is needed, deterministically subsample each
family's own matched pool to a common budget; never condition Gemma on Qwen's
success indices.

## P0.8 — final T3 reliability at seeds 1 and 2 (deferred)

Each block is one independently resumable scientific checkpoint: train pure FL
through T3, train full FedLS-SQL through T3, then evaluate only the two final
Spider endpoints. Completed stages are validated and skipped by the federated
runner; partial stages resume from their existing `_ckpt` state. These commands
remain ready but are not active under the current research priority. When
reactivated, run seed 1, then seed 2, and review the three training-seed deltas.

### Seed 1

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=1; $F="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; $K="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; $E="artifacts/eval_resume/fedls_final_t3_spider_s$S/eval_k0"; foreach ($P in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.8 input: $P" } }; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $F --seed $S; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed $S failed; rerun this exact line to resume" }; uv run python experiments/federated/run.py run --arm fedkd --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $K --seed $S; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed $S failed; rerun this exact line to resume" }; foreach ($A in @("$F/round_3/fedavg_adapter","$K/round_3/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing final seed-${S} adapter: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s${S}_t3=$F/round_3/fedavg_adapter" "fedls_s${S}_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Final Spider evaluation seed $S failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifests: $E/manifests" }; Write-Host "P0.8 seed $S complete: final FL and FedLS-SQL T3 evaluated"
```

### Seed 2

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=2; $F="artifacts/federated/fedavg_only_noicl_k5_e1_t3_s$S"; $K="artifacts/federated/fedkd_noicl_k5_e1_t1_s$S"; $E="artifacts/eval_resume/fedls_final_t3_spider_s$S/eval_k0"; foreach ($P in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.8 input: $P" } }; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $F --seed $S; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed $S failed; rerun this exact line to resume" }; uv run python experiments/federated/run.py run --arm fedkd --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $K --seed $S; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed $S failed; rerun this exact line to resume" }; foreach ($A in @("$F/round_3/fedavg_adapter","$K/round_3/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing final seed-${S} adapter: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s${S}_t3=$F/round_3/fedavg_adapter" "fedls_s${S}_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Final Spider evaluation seed $S failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing evaluation manifests: $E/manifests" }; Write-Host "P0.8 seed $S complete: final FL and FedLS-SQL T3 evaluated"
```

## P1.0 — communication accounting from existing records

No rerun is required. The committed T1-T3 FedLS-SQL metrics and pure-FL T3
metrics agree on the adapter payload: one global adapter is `73,911,080` bytes;
five client uploads total `369,555,560` bytes and five broadcasts total
`369,555,400` bytes per round. Thus the measured payload is `739,110,960`
bytes per round and `2,217,332,880` bytes over three rounds (`2.065 GiB`). FL
and FedLS-SQL have identical client-network payload under this protocol because
teacher transfer is server-local. These are serialized adapter-weight bytes;
transport framing and protocol metadata are excluded.

After P0.6, the active GPU priority is P0.7 second-family portability. It first
smokes the Gemma 2B client and Gemma 9B teacher/cache path, then regenerates
Gemma targets and logits before a five-arm base/FL/gold/target/full T1 ladder.
Full Gemma FedLS-SQL is permitted only after exact token-ID compatibility passes. Extend
to T3/OOD only if the T1 gate is positive and material. P0.8 seed reliability
remains ready but deferred.

Before collecting official latency, add a warm-up-capable benchmark path. Do
not treat an ordinary `eval_arms` run as the final benchmark: its timer excludes
model loading but currently includes the first measured decode without a fixed
in-process warm-up. The mechanism/error audit is CPU-only and may proceed while
a GPU task runs; seed-1/2 matched public-gold controls remain conditional.

## Resource-measurement eligibility

Future results now record accelerator-synchronized elapsed time, examples/sec,
optimizer updates, process peak RSS, peak PyTorch allocated/reserved VRAM,
fresh/resumed state, runtime versions, and whether a round reused stages.
These fields make measurement scope auditable; they do not make a busy shared
machine controlled.

- Accuracy runs may execute while the server is shared.
- A resource number is paper-eligible only when `paper_timing_eligible=true`,
  the selected GPU has no competing process, and the run is explicitly logged
  as controlled.
- Resumed eval timing and federated round timing with reused stages are not
  paper-eligible. Their accuracy remains valid.
- `gpu_vram` means peak PyTorch allocated memory for this process, not total
  device VRAM. Report `gpu_peak_reserved_mb` and `process_peak_rss_mb`
  separately.
- Official latency/resource benchmarks remain gated under T2; run each recipe
  at least three times after fixed warm-up and report median plus dispersion.

Before each future controlled resource run on GPU 1, this read-only preflight
must return no PIDs:

```powershell
$Gpu=1; $Busy=@(nvidia-smi -i $Gpu --query-compute-apps=pid --format=csv,noheader,nounits | Where-Object { $_.Trim() -match '^\d+$' }); if ($LASTEXITCODE -ne 0) { throw "Cannot inspect GPU $Gpu" }; if ($Busy.Count -gt 0) { throw "GPU $Gpu is busy with PID(s): $($Busy -join ', ')" }; Write-Host "GPU $Gpu has no competing compute process"
```

## Parked work

- Final T3 seed-1/2 replication is retained as T1R/P0.8 but deferred. Its
  narrowed commands above are the only active-form provenance; older broad seed
  commands at Git commit `b996594` must not be reused. Additional component
  replication remains conditional under T7.
- No “Centralized + CE/KD” command is activated. Historical variants use
  mismatched 1k pools or mixed stages. Add a new matched centralized lineage
  only if the final reviewer audit needs to separate federation from the same
  teacher-guided server treatment.
- FedProx, heterogeneity, and sensitivity tasks remain gated.
- ICL and FLoRA-NA remain archived negative branches.

## After a completed block

1. Preserve output roots and resume directories exactly as written.
2. Commit generated configs, metrics, predictions, and manifests from the code
   repository; never commit adapter/cache directories under `artifacts/`.
3. After validation, update the stable IDs in `RESULT_REGISTRY.md`, the affected
   canonical table in `paper/results/MAIN_RESULTS.md`, and the decision in
   `LAB_LOG.md`.
