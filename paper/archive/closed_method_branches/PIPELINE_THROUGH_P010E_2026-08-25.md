# FedLS-SQL — archived experiment queue through P0.10e

> Archived 2026-08-25 after the full-pool LLM-anchored FedDF gate failed.
> This snapshot preserves completed commands and the operator's GPU choices as
> execution provenance. It is not an active run queue. Current work is owned by
> `paper/notes/PIPELINE_NEXT.md`.

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

The matched public-supervision, centralized-recipe, centralized OOD/BIRD, and
second-family gates are complete. The evidence is sufficient to retain the
FedLS-SQL framework, but not to present plain RKL as a stable new KD method.
P0.9 has closed global-error selection. P0.10a then triaged three substantively
different directions without training. Client execution-result plurality gives
the strongest feasibility signal, so **LLM-anchored FedDF** is now the first
discussion candidate; KID and execution-verified preference KD rank second and
third. This is not yet a method change. The current uniform FedLS-SQL method
remains the frozen fallback. P0.10b froze a hard-LLM-target control against the
same target plus sparse client-ensemble forward KL. P0.10c passed its technical
smoke, and P0.10d passed the preregistered 512-row causal gate. P0.10e is now
the only active method run: one untuned 3,873-row confirmation against the
existing canonical hard-target and reverse-KL endpoints.

| Order  | Action                                                                                | Status                                                                        |
| ------ | ------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------- |
| P0.0   | Build and verify the exact 3,873-row BIRD-gold control                                | complete                                                                      |
| P0.1   | Train the missing public-gold CE server branch from the shared T1 adapter             | complete                                                                      |
| P0.2   | Evaluate the four matched T1 arms on Spider                                           | complete; Gate T1 passed                                                      |
| P0.3   | Train standard continuous centralized 3-epoch baseline                                | complete; 67.31 EX                                                            |
| P0.4   | Evaluate both centralized recipes on Spider                                           | complete; no meaningful difference                                            |
| P0.5   | Select the official centralized ceiling                                               | complete; standard continuous selected                                        |
| P0.6   | Evaluate the official centralized baseline on Realistic, Syn, DK, and BIRD            | complete; 55.91 / 54.06 / 53.27 / 13.04 EX                                    |
| P0.7a  | Smoke Gemma 2B training, adapter load, and inference                                  | complete; pipeline pass, 8-row EX is non-paper diagnostic                     |
| P0.7b  | Smoke Gemma 9B→2B targets, token-ID compatibility, and logit cache                    | complete                                                                      |
| P0.7c  | Generate Gemma 9B targets for all 9,428 BIRD training rows                            | generation complete; one deterministic empty target is recorded at index 7004 |
| P0.7e  | Quick-exec and official-EX filter Gemma targets; build matched gold                   | complete; `N_gemma=2,487`                                                     |
| P0.7s  | Train/evaluate Gemma 2B pure FL                                                       | complete; 57.16 EX / 49.52 EM                                                 |
| P0.7g  | Evaluate untouched Gemma 2B base on full Spider                                       | complete; 52.22 EX / 22.44 EM                                                 |
| P0.7q  | Audit all 9,428 BIRD gold SQL once and compare both teachers on the common valid mask | complete; 9,056 valid / 372 invalid                                           |
| P0.7d  | Gemma T1 five-arm ladder: base, FL, gold CE, target CE, full FedLS                    | complete; 52.22 / 57.16 / 41.68 / 61.22 / 61.41 EX                            |
| P0.9a  | Profile Qwen T1 public-pool failures and client disagreement from existing adapters   | complete; global-error signal retained, disagreement rejected                 |
| P0.9b  | Matched random-subset vs global-error hard-SeqKD screen                               | complete; negative, gate failed                                               |
| P0.9c  | Add client-disagreement selection                                                     | cancelled at this gate; no incremental correction evidence                    |
| P0.9d  | Add cached logits/skew/AKL to the winning selector                                    | cancelled; selector did not win                                               |
| P0.10a | No-training triage of client ensemble, prefix-cascade, and preference-pair signals    | complete; all gates pass, FedDF proxy ranks first                             |
| P0.10b | Specify and preregister an LLM-anchored FedDF screen                                  | complete; hard LLM CE anchor + sparse client FKL                              |
| P0.10c | Build 8-row sparse cache and smoke the hybrid training/resume path                    | complete; mean tail `0.000752`, training path passed                          |
| P0.10d | Matched 512-row hard-SeqKD control vs LLM-anchored FedDF                              | complete; `+1.45` EX and 11 fewer execution errors, gate passed               |
| P0.10e | Full 3,873-row LLM-anchored FedDF confirmation                                        | **active; run next**                                                          |
| P0.7t  | Evaluate the 4-bit Gemma 9B teacher zero-shot on Spider                               | optional contextual ceiling; does not decide the method                       |
| P0.8   | Replicate final T3 pure FL vs full FedLS-SQL at training seeds 1/2 on Spider          | deferred by current research priority                                         |
| P1.0   | Consolidate adapter-payload communication from committed round metrics                | complete; no rerun needed                                                     |
| P1.1   | Add warm-up-capable controlled inference benchmark and run 1.5B vs 7B                 | pending after method freeze                                                   |

P0.1-P0.4 accuracy is valid, but opportunistic wall-time/RAM values are not
paper resource evidence. Do not rerun P0.3 merely to backfill epoch snapshots:
it completed before the snapshot feature existed. P0.9b commands below are
retained as executed provenance, not active work. Do not improvise another
selector or start FedProx, heterogeneity, new aggregation, sensitivity, or
model-size/rank/client sweeps while the preregistered P0.10e confirmation is
active.

## Fixed T1 comparison

All four arms start from the same seed-0, round-1 client training and
factor-wise FedAvg adapter:

```text
artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter
```

| Evaluation arm      | Server treatment                                  |
| ------------------- | ------------------------------------------------- |
| `fl_t1_shared`      | none                                              |
| `public_gold_ce`    | CE on BIRD gold for the exact retained 3,873 rows |
| `teacher_target_ce` | CE on teacher-generated SQL (`fedavg_pub`)        |
| `fedls_t1`          | teacher-target CE + reverse KL (`fedkd`)          |

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
`train.ckpt.jsonl`; rerunning this exact command resumes safely. Coverage means
every source identity has a recorded teacher outcome. A deterministic empty
generation remains a teacher failure in provenance and is rejected by P0.7e;
do not retry until the teacher happens to succeed.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='processed_data/BIRD/centralized/train.csv'; $R='processed_data/BIRD/gemma2_9b_bootstrap_full/train.csv'; if (-not (Test-Path -LiteralPath $S)) { throw "Missing full BIRD source: $S" }; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 4 --max-new-tokens 128 --schema-style full --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Full Gemma target generation failed; rerun this exact line to resume' }; $N=(Import-Csv -LiteralPath $R).Count; $V=Get-Content -LiteralPath "${R}.provenance.json" -Raw | ConvertFrom-Json; $NE=@($V.empty_target_indices).Count; if ($N -ne 9428 -or $V.n_output_rows -ne 9428 -or ($V.n_nonempty_targets + $NE) -ne 9428 -or -not $V.tokenizer_compatibility.compatible) { throw "Full Gemma target verification failed: csv=$N provenance=$($V.n_output_rows) nonempty=$($V.n_nonempty_targets) empty=$NE tokenizer=$($V.tokenizer_compatibility.compatible)" }; Write-Host "P0.7c complete: all 9,428 teacher outcomes recorded; empty teacher failures=$NE"
```

### P0.7e — derive the Gemma-specific EX-match pool and gold control

This CPU step reproduces the canonical Qwen selection recipe: first reject
teacher SQL that cannot finish within the fixed 8-second quick-execution
timeout, then apply the official EX comparison against BIRD gold to survivors.
Both checkpoints are resumable and fingerprinted. It retains teacher SQL only
for official `match` rows and reconstructs BIRD gold on those exact indices.
The resulting `N_gemma` is a measured property of Gemma. This stage completed
with 9,428 generated outcomes, 7,162 quick-exec survivors, and
`N_gemma=2,487` official matches. The official stage recorded 4,443
mismatches, 231 gold-execution failures, and one prediction-execution failure.
Those 231 rows are conditional on Gemma's survivor set, so they must not be
compared directly with Qwen's 23 conditional gold failures.

```powershell
$S='processed_data/BIRD/centralized/train.csv'; $R='processed_data/BIRD/gemma2_9b_bootstrap_full/train.csv'; $X='processed_data/BIRD/gemma2_9b_bootstrap_full_exec/train.csv'; $P='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.csv'; $G='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch_gold/train.csv'; foreach ($I in @($S,$R,"${R}.provenance.json")) { if (-not (Test-Path -LiteralPath $I)) { throw "Missing P0.7e input: $I" } }; uv run python scripts/filter_teacher_targets_exmatch.py --source-csv $S --teacher-targets $R --exec-out $X --exec-timeout 8 --out $P --workers 8; if ($LASTEXITCODE -ne 0) { throw 'Gemma quick-exec/EX filtering failed; rerun this exact line to resume' }; uv run python scripts/build_public_gold_control.py --source-csv $S --teacher-pool $P --selection-ckpt processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.score_ckpt.jsonl --out $G; if ($LASTEXITCODE -ne 0) { throw 'Gemma matched-gold control build failed' }; $NX=(Import-Csv -LiteralPath $X).Count; $N=(Import-Csv -LiteralPath $P).Count; $NG=(Import-Csv -LiteralPath $G).Count; $V=Get-Content -LiteralPath "${P}.provenance.json" -Raw | ConvertFrom-Json; $VG=Get-Content -LiteralPath "${G}.provenance.json" -Raw | ConvertFrom-Json; if ($N -le 0 -or $N -ne $NG -or $N -ne $V.n_exmatched -or $N -ne $VG.n_rows -or $V.n_generated -ne 9428 -or $NX -ne $V.n_exec_kept -or $V.n_scored -ne $V.n_exec_kept) { throw "Gemma pool verification failed: generated=$($V.n_generated) exec=$NX official_scored=$($V.n_scored) matched=$N gold=$NG" }; Write-Host "P0.7e complete: Gemma-specific matched pool has N_gemma=$N rows"
```

### P0.7q — teacher-independent BIRD gold audit and common-mask comparison

Run this CPU step alone so concurrent SQLite jobs cannot introduce shared-disk
or timeout noise. It executes gold SQL for all 9,428 source rows in read-only
mode with the same 60-second timeout used by official EX. The checkpoint is
fingerprinted by the source CSV, timeout, and local SQLite inventory. The
second script then projects both teacher score checkpoints onto this one valid
gold mask. The paper-safe cross-family quantities are each teacher's
`matches / n_gold_valid`, not the conditional `gold_exec_failed` counts from
different survivor sets. Rerun the exact line to resume.

This proves whether both selectors are being judged against the same local
gold/database snapshot. It does **not** by itself prove that the official BIRD
release is wrong: if structural failures remain, compare the affected local
SQLite schemas/files with a clean official BIRD download before assigning the
fault to the dataset rather than local data assembly/version drift.

P0.7q completed with 9,056/9,428 (`96.05%`) gold rows executable under the
60-second audit and 372 invalid outcomes: 350 stable missing-table/column
failures, 21 timeouts, and one `database or disk is full` failure. `retail_world`
accounts for 330/372 failures. On the common valid mask, Qwen matches 3,869
rows (`42.72%`) and Gemma matches 2,487 (`27.46%`), with 2,019 common matches.
All 2,487 Gemma-selected training rows are audit-valid, so P0.7d used the pool
without reconstruction;
the 372-row snapshot issue remains a data-quality limitation, not teacher
training data. Canonical committed artifacts are
`processed_data/BIRD/gold_exec_audit_t60/` and
`audits/bird_train_gold_exec_t60_teacher_comparison.json` (nested commit
`3e673ef`).

```powershell
$S='processed_data/BIRD/centralized/train.csv'; $A='processed_data/BIRD/gold_exec_audit_t60/train.csv'; $Q='processed_data/BIRD/bootstrap_full_exmatch/train.score_ckpt.jsonl'; $G='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.score_ckpt.jsonl'; $C='artifacts/audits/bird_train_gold_exec_t60_teacher_comparison.json'; foreach ($I in @($S,$Q,$G)) { if (-not (Test-Path -LiteralPath $I)) { throw "Missing P0.7q input: $I" } }; uv run python scripts/audit_gold_execution.py --source-csv $S --out $A --exec-timeout 60 --workers 1; if ($LASTEXITCODE -ne 0) { throw 'BIRD gold audit failed; rerun this exact line to resume' }; $V=Get-Content -LiteralPath "${A}.provenance.json" -Raw | ConvertFrom-Json; $N=(Import-Csv -LiteralPath $A).Count; if ($V.n_scored -ne 9428 -or $N -ne $V.n_gold_valid) { throw "Gold audit verification failed: scored=$($V.n_scored) valid_csv=$N valid_provenance=$($V.n_gold_valid)" }; uv run python scripts/summarize_teacher_selection_on_gold_mask.py --gold-audit "${A}.provenance.json" --teacher-checkpoint "qwen=$Q" --teacher-checkpoint "gemma=$G" --out $C; if ($LASTEXITCODE -ne 0) { throw 'Common-mask teacher comparison failed' }; if (-not (Test-Path -LiteralPath $C)) { throw "Missing common-mask report: $C" }; Write-Host "P0.7q complete: gold-valid=$N; review $C before interpreting cross-family retention"
```

### P0.7s — pure FL after the teacher lane

Pure FL is logically independent of the teacher, but Gemma 9B and Gemma 2B
cannot run safely in parallel on the current Windows host because they share
RAM and pagefile. Run P0.7s only after P0.7b-c/e. Do not train gold CE on
Qwen's 3,873 selected rows. This stage is complete: pure FL reaches `57.16 EX`,
`49.52 EM`, with 212 execution errors on all 1,034 Spider rows. The client-1
stage resumed from row 1,248 and completed the remaining 1,129 rows; all five
client adapters and factor-wise aggregation are complete. Accuracy is valid,
but the resumed training resource measurements are not paper evidence.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $M='google/gemma-2-2b-it'; $F='artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0'; $E='artifacts/eval_resume/gemma2_2b_t1_fl_s0/eval_k0'; foreach ($X in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv')) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.7s input: $X" } }; uv run python experiments/federated/run.py run --arm fedavg --rounds 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $F --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma pure-FL T1 failed; rerun this exact line to resume' }; $A="$F/round_1/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing Gemma FL adapter: $A" }; uv run python experiments/eval_arms/run.py --model $M --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "gemma_fl_t1=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 8 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Gemma pure-FL evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing Gemma FL manifests: $E/manifests" }; Write-Host 'P0.7s complete: pure FL is ready for matched-ladder reuse'
```

### P0.7g — untouched Gemma 2B base anchor

This stage is complete on all 1,034 Spider rows: the untouched base reaches
`52.22 EX`, `22.44 EM`, with 162 execution errors. Pure FL therefore adds
`+4.94 EX` with 141 paired gains and 90 losses (exact McNemar `p=0.00096`), but
also adds 50 execution errors. The result uses P0.7d's resume root, so the later
five-arm evaluation reuses the completed base checkpoint rather than
generating it again.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $E='artifacts/eval_resume/gemma2_9b_to_2b_t1_five_arm_s0/eval_k0'; foreach ($X in @('processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv')) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.7g input: $X" } }; uv run python experiments/eval_arms/run.py --model google/gemma-2-2b-it --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "gemma_base=" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 8 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Gemma base evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing Gemma base manifests: $E/manifests" }; Write-Host 'P0.7g complete: compare untouched Gemma base against the P0.7s pure-FL result before server training'
```

### Retired parallel launch — do not run

The former combined GPU-0/GPU-1 overnight recipe is retained below only for
command provenance. It caused Windows commit-memory pressure and must not be
used. Run the individual P0.7 stages sequentially. A separate held-out teacher
zero-shot benchmark remains optional P1.1 evidence, not a prerequisite for the
Gemma ladder.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $S='processed_data/BIRD/centralized/train.csv'; $Q='processed_data/BIRD/gemma2_9b_targets_smoke8_fullsource/train.csv'; $C='artifacts/teacher_logit_cache/gemma2_9b_to_2b_smoke8_fullsource_k0'; $R='processed_data/BIRD/gemma2_9b_bootstrap_full/train.csv'; $X='processed_data/BIRD/gemma2_9b_bootstrap_full_exec/train.csv'; $P='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.csv'; $G='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch_gold/train.csv'; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 2 --max-new-tokens 128 --schema-style full --limit 8 --out $Q --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma target/tokenizer smoke failed; rerun this exact line to resume' }; uv run python scripts/build_teacher_logit_cache.py --pool $Q --pool-size 0 --seed 0 --model google/gemma-2-2b-it --teacher-model google/gemma-2-9b-it --teacher-4bit --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --out $C; if ($LASTEXITCODE -ne 0) { throw 'Gemma teacher-logit smoke failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$C/meta.json")) { throw "Missing Gemma smoke cache metadata: $C/meta.json" }; uv run python scripts/build_teacher_targets.py --source-csv $S --teacher-model google/gemma-2-9b-it --student-model google/gemma-2-2b-it --teacher-4bit --batch-size 4 --max-new-tokens 128 --schema-style full --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Full Gemma target generation failed; rerun this exact line to resume' }; $NR=(Import-Csv -LiteralPath $R).Count; if ($NR -ne 9428) { throw "Expected 9,428 raw Gemma targets, found $NR" }; uv run python scripts/filter_teacher_targets_exmatch.py --source-csv $S --teacher-targets $R --exec-out $X --exec-timeout 8 --out $P --workers 8; if ($LASTEXITCODE -ne 0) { throw 'Gemma quick-exec/EX filtering failed; rerun this exact line to resume' }; uv run python scripts/build_public_gold_control.py --source-csv $S --teacher-pool $P --selection-ckpt processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.score_ckpt.jsonl --out $G; if ($LASTEXITCODE -ne 0) { throw 'Gemma matched-gold control build failed' }; $NX=(Import-Csv -LiteralPath $X).Count; $N=(Import-Csv -LiteralPath $P).Count; $NG=(Import-Csv -LiteralPath $G).Count; $V=Get-Content -LiteralPath "${P}.provenance.json" -Raw | ConvertFrom-Json; if ($N -le 0 -or $N -ne $NG -or $N -ne $V.n_exmatched -or $V.n_generated -ne 9428 -or $NX -ne $V.n_exec_kept -or $V.n_scored -ne $V.n_exec_kept) { throw "Gemma pool verification failed: generated=$($V.n_generated) exec=$NX official_scored=$($V.n_scored) matched=$N gold=$NG" }; Write-Host "GPU-0 lane complete: N_gemma=$N targets and matched gold rows are ready"
```

### P0.7d — Gemma-specific five-arm T1 ladder

All server-treated arms use the same Gemma-selected `N_gemma` identities:
BIRD gold CE, Gemma target CE, or Gemma target CE plus online reverse KL. Pure
FL shares the identical private-client/FedAvg stage and has no public stage.
The untouched Gemma 2B base arm anchors whether private federated training and
the complete framework improve or degrade the pretrained student.

**Completed result (seed 0, Spider, 1,034 identical rows):** base `52.22`, FL
`57.16`, matched-gold CE `41.68`, teacher-target CE `61.22`, and full FedLS
`61.41` EX. Teacher-target CE beats FL by `+4.06` (137/95 paired gains/losses,
`p=0.00698`); full FedLS beats FL by `+4.25` (132/88, `p=0.00365`). Full FedLS
is only `+0.19` over target CE (46/44, `p=0.916`), so RKL portability is not an
independent claim. Canonical committed evaluation:
`experiments/eval_arms/results/eval_arms__s0__20260823T005329/`.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $M='google/gemma-2-2b-it'; $T='google/gemma-2-9b-it'; $P='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch/train.csv'; $GOLD='processed_data/BIRD/gemma2_9b_bootstrap_full_exec_exmatch_gold/train.csv'; $F='artifacts/federated/gemma2_2b_fedavg_only_noicl_k5_e1_t1_s0'; $G='artifacts/federated/gemma2_9b_selected_goldce_noicl_k5_e1_t1_s0'; $H='artifacts/federated/gemma2_9b_to_2b_seqkd_noicl_k5_e1_t1_s0'; $K='artifacts/federated/gemma2_9b_to_2b_fedls_noicl_k5_e1_t1_s0'; $E='artifacts/eval_resume/gemma2_9b_to_2b_t1_five_arm_s0/eval_k0'; foreach ($X in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv',$P,"${P}.provenance.json",$GOLD,"${GOLD}.provenance.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.7d input: $X" } }; $NP=(Import-Csv -LiteralPath $P).Count; $NG=(Import-Csv -LiteralPath $GOLD).Count; if ($NP -le 0 -or $NP -ne $NG) { throw "Gemma supervision pools are not matched: targets=$NP gold=$NG" }; uv run python experiments/federated/run.py run --arm fedavg --rounds 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $F --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma pure-FL T1 failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $GOLD --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out "$F/round_1" --out $G --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma matched gold CE failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out "$F/round_1" --out $H --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Gemma teacher-target CE failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedkd --round 1 --model $M --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model $T --teacher-4bit --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out "$F/round_1" --out $K --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Full Gemma FedLS-SQL failed; rerun this exact line to resume' }; foreach ($A in @("$F/round_1/fedavg_adapter","$G/round_1/m_g","$H/round_1/m_g","$K/round_1/m_g")) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing Gemma T1 adapter: $A" } }; uv run python experiments/eval_arms/run.py --model $M --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "gemma_base=" "gemma_fl_t1=$F/round_1/fedavg_adapter" "gemma_goldce_t1=$G/round_1/m_g" "gemma_seqkd_t1=$H/round_1/m_g" "gemma_fedls_t1=$K/round_1/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 8 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Gemma five-arm T1 evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing Gemma T1 manifests: $E/manifests" }; Write-Host "P0.7d complete: stop and review the five-arm result at N_gemma=$NP"
```

**Interpretation:** this is a method-faithful second-family replication because
both families use full-source generation, the fixed 8-second quick-execution
filter, and official EX matching. It is not an equal-row cross-family
experiment when `N_gemma != 3,873`. If a later
controlled family comparison is needed, deterministically subsample each
family's own matched pool to a common budget; never condition Gemma on Qwen's
success indices. The endpoint transfers, but the common cross-family mechanism
supported most clearly is hard teacher-target CE; reverse KL remains
model-family dependent.

## P0.9 — global-error method-direction gate (closed negative)

P0.9 tested whether the paper should promote a federated-aware
execution-guided distillation method. P0.9a diagnosed the signal and P0.9b
tested the intervention under a matched budget. The intervention failed; all
commands in this section are completed provenance.

### P0.9a — public failure/disagreement diagnostic

**Completed result (512 Qwen public rows):** the shared FL adapter obtains
`32.23` EX and uniform SeqKD obtains `53.13` EX. Uniform SeqKD corrects 141 FL
errors and regresses 34 correct rows (net `+107`, or `+20.90` EX points on this
training-domain diagnostic). FL has 347 errors; high client disagreement finds
331 of them (`95.39%`) but flags 454/512 rows (`88.67%`). Disagreement is
associated with FL error (odds ratio `7.06`, Fisher `p=2.69e-11`), yet among FL
errors its SeqKD correction rate is 137/331 versus 4/16 (odds ratio `2.12`,
`p=0.297`). Thus it is not selective enough and adds no established signal to
the directly observed global execution state. P0.9c is cancelled; P0.9b uses
global state only. These public-pool numbers are diagnostics, not paper test
accuracy.

Use the immutable Qwen T1 client adapters and their shared FedAvg adapter. On a
deterministic public subset from the existing 3,873-row verified teacher pool,
record per row:

- global-adapter SQL, execution status, and EX against the verified teacher
  target, which was retained only after EX matching to public gold;
- each client-adapter SQL and execution-result-group agreement;
- SQL structure and length;
- stable source index, hashes, adapter IDs, and decoding configuration.

Teacher-target NLL/KL is deliberately excluded from this first diagnostic. It
requires an additional student-forward path and is activated only if execution
state plus client disagreement are insufficient to define a selector.

The first report must answer whether global execution errors and client
disagreement identify different rows and whether either predicts errors after
uniform SeqKD. If disagreement adds no signal beyond the global model, cancel
P0.9c and keep the cheaper global-error selector.

The command builds one deterministic 512-row subset, evaluates the shared T1
FedAvg adapter, its uniform hard-SeqKD descendant, and all five uploaded client
adapters with greedy `k=0`, then groups client predictions by execution-result
equivalence. Evaluation and the final SQL analysis both resume from
fingerprinted checkpoints. Rerunning the exact line skips verified completed
work; any source/adapter/config drift requires a new immutable root.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $H='artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0'; $S='processed_data/BIRD/bootstrap_full_exmatch/train.csv'; $U='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $E='artifacts/eval_resume/p09a_qwen_t1_public512_s0/eval_k0'; $O='artifacts/analysis/p09a_qwen_t1_public512_s0'; foreach ($P in @($S,"$C/fedavg_adapter/adapter_config.json","$H/round_1/m_g/adapter_config.json") + @(1..5 | ForEach-Object { "$C/client_$_/adapter/adapter_config.json" })) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.9a input: $P" } }; uv run python scripts/build_fedkd_diagnostic_subset.py --source-csv $S --out $U --size 512 --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.9a subset build failed; rerun this exact line to resume' }; if ((Import-Csv -LiteralPath $U).Count -ne 512 -or -not (Test-Path -LiteralPath "${U}.provenance.json")) { throw 'P0.9a subset verification failed' }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/BIRD/centralized/train.csv --test-csv $U --arms "global_fl=$C/fedavg_adapter" "uniform_seqkd=$H/round_1/m_g" "client_1=$C/client_1/adapter" "client_2=$C/client_2/adapter" "client_3=$C/client_3/adapter" "client_4=$C/client_4/adapter" "client_5=$C/client_5/adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.9a public adapter evaluation failed; rerun this exact line to resume' }; uv run python scripts/analyze_fedkd_public_diagnostic.py --subset-csv $U --eval-manifest-dir "$E/manifests" --global-arm global_fl --seqkd-arm uniform_seqkd --client-prefix client_ --n-clients 5 --exec-timeout 8 --workers 8 --out $O; if ($LASTEXITCODE -ne 0) { throw 'P0.9a disagreement analysis failed; rerun this exact line to resume' }; foreach ($P in @("$O/rows.csv","$O/summary.json","$O/provenance.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.9a output: $P" } }; $V=Get-Content -LiteralPath "$O/summary.json" -Raw | ConvertFrom-Json; if ($V.n_rows -ne 512 -or $V.n_clients -ne 5) { throw "P0.9a summary verification failed: rows=$($V.n_rows) clients=$($V.n_clients)" }; Write-Host "P0.9a complete: review $O/summary.json before activating any selector training"
```

### P0.9b — matched hard-SeqKD screen

**Completed result (seed 0, 1,034 paired Spider rows):** global FL is `57.35`
EX / `50.58` EM with 236 execution errors; full uniform SeqKD is `61.32` /
`30.27` with 161 errors; `random256` is `58.70` / `35.88` with 222 errors; and
`global_error256` is `56.67` / `30.66` with 240 errors. Against the matched
random control, global-error selection loses `2.03` EX (47 gains / 68 losses,
exact McNemar `p=0.0617`), loses `5.22` EM (`p=5.15e-9`), and introduces 18
net execution errors. It therefore fails both the `+1.0` EX and no-error-
increase gates. Close this selector and do not tune its fraction or add a logit
loss to rescue it. The full uniform arm has about 15 times the row/update budget
and is contextual, not the matched causal control.

From the same pre-server T1 FedAvg adapter compare:

```text
uniform full/subset hard SeqKD
random subset hard SeqKD
global-error-balanced subset hard SeqKD
```

The activated screen uses 256 rows per arm. The hard pool explicitly samples
96 global execution errors and 96 executable-wrong rows, then draws 64 rows
uniformly without replacement from the remainder. The control is a 256-row
uniform random sample chosen only to match the hard pool's teacher-SQL token
count. Both arms therefore start at the same pre-server adapter and receive 256
examples, 16 optimizer updates (`batch=1`, accumulation 16), and nearly equal
target tokens. The existing 3,873-row uniform SeqKD arm is shown only as a
full-budget context, not as the matched primary control. Selection provenance
saves source indices, states, token totals, hashes, and the random seed.

Build the two CPU-only immutable pools:

```powershell
$U='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $D='artifacts/analysis/p09a_qwen_t1_public512_s0/rows.csv'; $H='processed_data/BIRD/p09b_qwen_global_error256_s0/train.csv'; $R='processed_data/BIRD/p09b_qwen_random256_s0/train.csv'; foreach ($P in @($U,$D)) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.9b pool input: $P" } }; uv run python scripts/build_fedkd_training_pools.py --subset-csv $U --analysis-rows $D --hard-out $H --random-out $R --size 256 --hard-fraction 0.75 --match-trials 4096 --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.9b pool build failed; rerun this exact line' }; $V=Get-Content -LiteralPath "${H}.provenance.json" -Raw | ConvertFrom-Json; $TD=[Math]::Abs([int]$V.teacher_sql_token_difference); if ((Import-Csv -LiteralPath $H).Count -ne 256 -or (Import-Csv -LiteralPath $R).Count -ne 256 -or $TD -gt [Math]::Ceiling(0.01*[int]$V.hard_teacher_sql_tokens)) { throw "P0.9b pool verification failed: token_difference=$TD" }; Write-Host "P0.9b pools complete: hard/random=256 rows, token_difference=$TD"
```

Train the matched random control (GPU):

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $P='processed_data/BIRD/p09b_qwen_random256_s0/train.csv'; $O='artifacts/federated/p09b_qwen_random256_seqkd_noicl_k5_e1_t1_s0'; foreach ($X in @("$C/fedavg_adapter/adapter_config.json",$P,'processed_data/BIRD/p09b_qwen_global_error256_s0/train.csv.provenance.json')) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.9b random input: $X" } }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.9b random SeqKD failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P0.9b random output: $X" } }; Write-Host 'P0.9b matched random SeqKD complete'
```

Train the global-error pool from the same FedAvg adapter (GPU):

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $P='processed_data/BIRD/p09b_qwen_global_error256_s0/train.csv'; $O='artifacts/federated/p09b_qwen_global_error256_seqkd_noicl_k5_e1_t1_s0'; foreach ($X in @("$C/fedavg_adapter/adapter_config.json",$P,"${P}.provenance.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.9b hard input: $X" } }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.9b global-error SeqKD failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P0.9b hard output: $X" } }; Write-Host 'P0.9b global-error SeqKD complete'
```

Evaluate the matched arms on all 1,034 Spider rows (GPU). `uniform_full` is
context only; the preregistered comparison is `global_error256` versus
`random256`:

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter'; $F='artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g'; $R='artifacts/federated/p09b_qwen_random256_seqkd_noicl_k5_e1_t1_s0/round_1/m_g'; $H='artifacts/federated/p09b_qwen_global_error256_seqkd_noicl_k5_e1_t1_s0/round_1/m_g'; $E='artifacts/eval_resume/p09b_qwen_global_error_vs_random256_spider_s0/eval_k0'; foreach ($A in @($C,$F,$R,$H)) { if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Missing P0.9b evaluation adapter: $A" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "global_fl=$C" "uniform_full=$F" "random256=$R" "global_error256=$H" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.9b Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P0.9b evaluation manifests: $E/manifests" }; Write-Host 'P0.9b complete: stop and review global_error256 versus random256 before any new method run'
```

The preregistered promotion gate was at least `+1.0` Spider EX over `random256`
with no increase in execution-error count. P0.9b failed both conditions. These
commands are now provenance only.

### P0.9c-d — conditional extensions

- Client-disagreement selection is cancelled for this gate: P0.9a found no
  significant incremental correction signal.
- Cached RKL/skew/AKL on this selector is cancelled. Do not use a logit-loss
  change to rescue the failed selection rule.
- The selection arm is harmful rather than neutral; retain current hard SeqKD
  as fallback. P0.10a diagnoses different mechanisms without reopening it.

## P0.10 — bounded KD/Federated method triage

### P0.10a — no-training feasibility audit (complete)

The audit reuses the frozen P0.9a row-level execution states and canonical
Spider T1 predictions; it performs no model training and no teacher inference.
On the 512 public BIRD rows, execution-result plurality among five clients,
falling back to the global model when no unique plurality exists, scores
`42.77` EX versus global FL at `32.23` (`+10.55` points), with 62 corrections,
8 regressions, and `71.88%` unique-plurality coverage. Any client is correct on
107/347 global failures, establishing ensemble complementarity but not yet a
trainable FedDF gain.

On canonical Spider T1 predictions, 82.20% of the FL model's 236 execution
errors diverge from gold within the first token quartile; early-divergence rows
have an execution-error rate 18.29 points above late-divergence rows. This
passes the KID discussion gate but is lexical correlation, not causal evidence.
The public audit also constructs 2,177 execution-verified preference pairs;
only 122 distinct global-model rows provide clean executable-wrong pairs, so
preference KD is feasible but narrower.

Decision order: (1) LLM-anchored FedDF, (2) KID, (3) execution-verified
preference KD. All three gates are diagnostic. No candidate is a FedLS-SQL
component and no GPU run is activated by this result.

Reproduce the CPU-only audit from the immutable P0.9a analysis rows. Using
`--public-analysis-rows` avoids re-executing SQL and therefore avoids changing
the result because of transient execution timeouts. The line is fingerprinted,
safe to rerun, and refuses incompatible reuse of the output root.

```powershell
$U='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $D='artifacts/analysis/p09a_qwen_t1_public512_s0/rows.csv'; $P='experiments/eval_arms/results/eval_arms__s0__20260823T205511/predictions'; $S='experiments/eval_arms/results/eval_arms__s0__20260820T065954/predictions'; $O='artifacts/analysis/p010a_fedkd_method_triage_s0'; foreach ($X in @($U,$D,$P,$S)) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10a input: $X" } }; uv run python scripts/analyze_fedkd_method_triage.py --public-subset $U --public-pred-dir $P --public-analysis-rows $D --spider-pred-dir $S --out $O --feddf-min-delta-pp 2 --feddf-min-coverage-pct 50 --kid-min-early-exec-pct 60 --kid-min-risk-diff-pp 15 --preference-min-clean-rows 100 --preference-min-unique-pct 80; if ($LASTEXITCODE -ne 0) { throw 'P0.10a audit failed; rerun this exact line to resume' }; foreach ($X in @("$O/summary.json","$O/public_ensemble_rows.csv","$O/spider_prefix_rows.csv","$O/preference_pairs.csv","$O/provenance.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10a output: $X" } }; $V=Get-Content -LiteralPath "$O/summary.json" -Raw | ConvertFrom-Json; if (-not $V.gates.llm_anchored_feddf -or -not $V.gates.kid -or -not $V.gates.preference_kd) { throw 'P0.10a decision verification failed' }; Write-Host 'P0.10a complete: all discussion gates pass; no training is activated'
```

### P0.10b — LLM-anchored FedDF design gate (complete)

The frozen screen uses the verified LLM SQL as the hard target in both arms.
The proposed arm adds forward KL from the five-client ensemble on the same
teacher-forced public trajectory:

```text
control: CE(y_LLM)
hybrid:  CE(y_LLM) + 0.5 * KL(p_clients || q_student)
```

Each client contributes its top-32 probabilities per target position. The
cache stores their union plus an averaged tail bucket, so truncated probability
mass is preserved rather than silently treated as zero. Client distributions
are computed server-side from the already-uploaded adapters on public rows;
there is no new client transmission and the current adapter-network payload is
unchanged. Cache metadata fingerprints every adapter, row/rendering flag,
temperature, and source file. This is LLM-anchored FedDF, not the existing RKL:
the LLM supplies the verified target while the client ensemble supplies the
additional distributional term.

### P0.10c — 8-row cache/training smoke (complete)

Run this first. It sequentially loads the five T1 client adapters, creates a
resume-safe top-32 cache for eight deterministic rows, rejects a mean tail mass
above 10%, then runs eight hybrid micro-steps from the shared FedAvg adapter.
Rerunning the exact line skips complete cache shards and resumes server
training; any fingerprint drift requires a new root.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $P='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $K='artifacts/client_ensemble_logit_cache/p010c_qwen_clients5_public8_top32_t1_s0'; $O='artifacts/federated/p010c2_qwen_llm_client_feddf8_noicl_k5_e1_t1_s0'; $A=@(1..5 | ForEach-Object { "$C/client_$_/adapter" }); foreach ($X in @($P,"$C/fedavg_adapter/adapter_config.json") + @($A | ForEach-Object { "$_/adapter_config.json" })) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10c input: $X" } }; uv run python scripts/build_client_ensemble_logit_cache.py --pool $P --pool-size 8 --client-adapters $A --model Qwen/Qwen2.5-1.5B-Instruct --top-k 32 --temperature 1 --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --seed 0 --out $K; if ($LASTEXITCODE -ne 0) { throw 'P0.10c client-ensemble cache smoke failed; rerun this exact line to resume' }; $M=Get-Content -LiteralPath "$K/meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 8 -or $M.n_clients -ne 5 -or $M.top_k -ne 32 -or $M.mean_tail_probability -gt 0.10) { throw "P0.10c cache gate failed: examples=$($M.n_examples) clients=$($M.n_clients) top_k=$($M.top_k) mean_tail=$($M.mean_tail_probability)" }; uv run python experiments/federated/run.py round --arm feddf --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 8 --distill-steps 8 --k-teacher 0 --lambda-ft 1 --lambda-kd 0 --client-ensemble-cache $K --lambda-client-kd 0.5 --client-kd-temperature 1 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.10c FedDF training smoke failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/round_1/m_g_meta.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P0.10c output: $X" } }; Write-Host "P0.10c passed: sparse client cache and hybrid training path complete; mean_tail=$($M.mean_tail_probability)"
```

### P0.10d — matched 512-row causal screen (complete)

The smoke passed with mean top-32 tail probability `0.000752`. On 1,034 paired
Spider rows, `llm_only512` reached `56.87` EX / `31.91` EM with 230 execution
errors, while `llm_client_feddf512` reached `58.32` EX / `39.94` EM with 219
execution errors. The hybrid corrected 58 control failures and regressed 43
control successes: a net 15 questions (`+1.45` EX), with 11 fewer execution
errors. This passes the frozen `+1.0` EX/no-error-increase gate. The paired EX
effect is still uncertain at this budget (exact McNemar `p=0.163`), so it
authorizes one full-pool confirmation rather than a method claim or parameter
sweep.

After P0.10c passes, build the full cache:

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $P='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $K='artifacts/client_ensemble_logit_cache/p010d_qwen_clients5_public512_top32_t1_s0'; $A=@(1..5 | ForEach-Object { "$C/client_$_/adapter" }); foreach ($X in @($P) + @($A | ForEach-Object { "$_/adapter_config.json" })) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10d cache input: $X" } }; uv run python scripts/build_client_ensemble_logit_cache.py --pool $P --pool-size 0 --client-adapters $A --model Qwen/Qwen2.5-1.5B-Instruct --top-k 32 --temperature 1 --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --seed 0 --out $K; if ($LASTEXITCODE -ne 0) { throw 'P0.10d full client-ensemble cache failed; rerun this exact line to resume' }; $M=Get-Content -LiteralPath "$K/meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 512 -or $M.n_clients -ne 5 -or $M.top_k -ne 32 -or $M.mean_tail_probability -gt 0.10) { throw "P0.10d cache gate failed: examples=$($M.n_examples) clients=$($M.n_clients) top_k=$($M.top_k) mean_tail=$($M.mean_tail_probability)" }; Write-Host "P0.10d cache complete: mean_tail=$($M.mean_tail_probability)"
```

Train the matched hard-SeqKD control (GPU 0):

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $P='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $O='artifacts/federated/p010d_qwen_llm_only512_noicl_k5_e1_t1_s0'; foreach ($X in @($P,"$C/fedavg_adapter/adapter_config.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10d control input: $X" } }; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1 --lambda-kd 0 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.10d LLM-only control failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P0.10d control output: $X" } }; Write-Host 'P0.10d matched LLM-only control complete'
```

Train the hybrid from the same initialization and budget (GPU 1; may run in
parallel with the control only after the cache build has exited):

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $P='processed_data/BIRD/p09a_qwen_public512_s0/train.csv'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $K='artifacts/client_ensemble_logit_cache/p010d_qwen_clients5_public512_top32_t1_s0'; $O='artifacts/federated/p010d_qwen_llm_client_feddf512_noicl_k5_e1_t1_s0'; foreach ($X in @($P,"$C/fedavg_adapter/adapter_config.json","$K/meta.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10d hybrid input: $X" } }; uv run python experiments/federated/run.py round --arm feddf --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1 --lambda-kd 0 --client-ensemble-cache $K --lambda-client-kd 0.5 --client-kd-temperature 1 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.10d LLM-anchored FedDF failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P0.10d hybrid output: $X" } }; Write-Host 'P0.10d matched LLM-anchored FedDF complete'
```

Evaluate both arms on all 1,034 Spider rows:

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/p010d_qwen_llm_only512_noicl_k5_e1_t1_s0/round_1/m_g'; $H='artifacts/federated/p010d_qwen_llm_client_feddf512_noicl_k5_e1_t1_s0/round_1/m_g'; $E='artifacts/eval_resume/p010d_qwen_llm_only_vs_feddf512_spider_s0/eval_k0'; foreach ($X in @($C,$H)) { if (-not (Test-Path -LiteralPath "$X/adapter_config.json")) { throw "Missing P0.10d evaluation adapter: $X" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "llm_only512=$C" "llm_client_feddf512=$H" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.10d Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P0.10d evaluation manifests: $E/manifests" }; Write-Host 'P0.10d complete: stop and compare hybrid versus llm_only512 before any extension'
```

Promotion requires at least `+1.0` Spider EX and no increase in execution-error
count over `llm_only512`. Otherwise close the branch without tuning lambda,
temperature, top-k, or row selection. A positive seed-0 gate permits one full-
pool confirmation and then a client-only ablation; it does not immediately
replace the canonical method or trigger a parameter sweep.

### P0.10e — full 3,873-row confirmation (GPU, active)

This confirmation freezes the successful screen settings: five clients,
top-32, temperature 1, client-KL weight 0.5, seed 0, and the complete canonical
Qwen teacher-selected pool. Do not tune from P0.10d. The existing
`qwen.seqkd.t1.s0` checkpoint is the exact hard-target-only control: it starts
from the same shared T1 FedAvg adapter and trains once over these same 3,873
targets with the same optimizer/rendering flags. It must be reused rather than
retrained. The existing `qwen.fedls.t1.s0` reverse-KL endpoint is evaluated as
context for deciding which server objective belongs in the paper.

First build the full client-ensemble cache. This is the expensive inference
stage and sequentially loads the five 1.5B client adapters on one GPU. Rerun the
exact line to resume complete content-addressed shards.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $P='processed_data/BIRD/bootstrap_full_exmatch/train.csv'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $K='artifacts/client_ensemble_logit_cache/p010e_qwen_clients5_public3873_top32_t1_s0'; $A=@(1..5 | ForEach-Object { "$C/client_$_/adapter" }); foreach ($X in @($P,"$C/fedavg_adapter/adapter_config.json") + @($A | ForEach-Object { "$_/adapter_config.json" })) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10e cache input: $X" } }; if ((Import-Csv -LiteralPath $P).Count -ne 3873) { throw 'P0.10e requires the exact 3,873-row Qwen teacher pool' }; uv run python scripts/build_client_ensemble_logit_cache.py --pool $P --pool-size 0 --client-adapters $A --model Qwen/Qwen2.5-1.5B-Instruct --top-k 32 --temperature 1 --k-teacher 0 --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --max-len 2560 --seed 0 --out $K; if ($LASTEXITCODE -ne 0) { throw 'P0.10e full client-ensemble cache failed; rerun this exact line to resume' }; $M=Get-Content -LiteralPath "$K/meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 3873 -or $M.n_clients -ne 5 -or $M.top_k -ne 32 -or $M.mean_tail_probability -gt 0.10) { throw "P0.10e cache gate failed: examples=$($M.n_examples) clients=$($M.n_clients) top_k=$($M.top_k) mean_tail=$($M.mean_tail_probability)" }; Write-Host "P0.10e cache complete: mean_tail=$($M.mean_tail_probability)"
```

After the cache exits, train the single new hybrid endpoint. The exact line is
resume-safe through the federated setup/stage fingerprints and `_ckpt`.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $P='processed_data/BIRD/bootstrap_full_exmatch/train.csv'; $C='artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1'; $K='artifacts/client_ensemble_logit_cache/p010e_qwen_clients5_public3873_top32_t1_s0'; $O='artifacts/federated/p010e_qwen_llm_client_feddf3873_noicl_k5_e1_t1_s0'; foreach ($X in @($P,"$C/fedavg_adapter/adapter_config.json","$K/meta.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.10e training input: $X" } }; $M=Get-Content -LiteralPath "$K/meta.json" -Raw | ConvertFrom-Json; if ($M.n_examples -ne 3873 -or $M.n_clients -ne 5 -or $M.top_k -ne 32) { throw 'P0.10e cache metadata does not match the frozen full-pool design' }; uv run python experiments/federated/run.py round --arm feddf --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-schema-style full --pool $P --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1 --lambda-kd 0 --client-ensemble-cache $K --lambda-client-kd 0.5 --client-kd-temperature 1 --schema-style full --retrieval dail_select --demo-style never_schema --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out $C --out $O --seed 0; if ($LASTEXITCODE -ne 0) { throw 'P0.10e full LLM-anchored FedDF failed; rerun this exact line to resume' }; foreach ($X in @("$O/round_1/m_g/adapter_config.json","$O/round_1/m_g_meta.json","$O/setup.json","$O/manifest.json")) { if (-not (Test-Path -LiteralPath $X)) { throw "Incomplete P0.10e output: $X" } }; Write-Host 'P0.10e full LLM-anchored FedDF training complete'
```

Then evaluate the new hybrid against both immutable canonical server controls
on all 1,034 Spider rows.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $C='artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g'; $R='artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g'; $H='artifacts/federated/p010e_qwen_llm_client_feddf3873_noicl_k5_e1_t1_s0/round_1/m_g'; $E='artifacts/eval_resume/p010e_qwen_seqkd_vs_rkl_vs_feddf3873_spider_s0/eval_k0'; foreach ($X in @($C,$R,$H)) { if (-not (Test-Path -LiteralPath "$X/adapter_config.json")) { throw "Missing P0.10e evaluation adapter: $X" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "teacher_target_ce=$C" "fedls_rkl=$R" "llm_client_feddf3873=$H" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.10e Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P0.10e evaluation manifests: $E/manifests" }; Write-Host 'P0.10e complete: stop and review full-pool FedDF before any ablation or method change'
```

The full-pool causal gate remains `+1.0` EX over `teacher_target_ce` with no
execution-error increase. Also report the paired comparison with `fedls_rkl`:
beating it clearly supports replacing RKL in the proposed endpoint; matching it
within normal paired uncertainty supports FedDF as a more federated-specific,
tokenizer-independent alternative; materially trailing it keeps FedDF as an
ablation only. A passing result permits one client-only ablation. A failed
result closes P0.10 without lambda, temperature, top-k, or selection tuning.

### P0.7t — Gemma 9B teacher zero-shot Spider reference

There is no completed Gemma teacher/Spider result yet. The existing teacher
reference is Qwen2.5-Coder-7B-Instruct (`78.72 EX`, `51.64 EM`). This command
evaluates the same 4-bit Gemma 9B instance used by P0.7 generation on all 1,034
Spider dev rows. It is a teacher ceiling/context diagnostic, not a replacement
for the P0.7d method comparison, so run it after the five-arm ladder. Batch size
2 is intentionally conservative for the current Windows RAM/pagefile limit.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $E='artifacts/eval_resume/gemma2_9b_teacher_spider_s0/eval_k0'; foreach ($X in @('processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv')) { if (-not (Test-Path -LiteralPath $X)) { throw "Missing P0.7t input: $X" } }; uv run python experiments/eval_arms/run.py --model google/gemma-2-9b-it --model-4bit --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "gemma2_9b_teacher=" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 2 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'Gemma 9B Spider teacher evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing Gemma teacher evaluation manifests: $E/manifests" }; Write-Host 'P0.7t complete: commit the result and report it as a 4-bit teacher reference'
```

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

The second-family ladder and P0.9 gate are complete. P0.10c/d passed: the
512-row hybrid gains 1.45 Spider EX and removes 11 execution errors. Run only
the frozen P0.10e full-pool confirmation next. Its result decides whether to
run one client-only ablation or freeze the original uniform FedLS-SQL method
and return to P1.1 resources and P0.8 final reliability. P0.7t remains optional
ceiling context.

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
