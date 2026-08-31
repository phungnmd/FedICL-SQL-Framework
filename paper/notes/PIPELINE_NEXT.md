# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every executable
> command added here must follow `CONVENTION.MD` §6.1: one physical line,
> fail-fast, immutable output roots, exact-command resume safety, and a
> separate allowlisted add/commit/push publication command for every new task.
> The ordered paper backlog and decision gates live in `PAPER_TODO.md`; this
> file contains only runnable or exactly preserved deferred commands.

For a short purpose/CPU/GPU/readiness view, see `PAPER_NEXT_TASKS.md`.

## Canonical baseline and innovation gate

The evidence-backed method is held fixed as the canonical fallback and matched
baseline after the P0.10e decision gate:

```text
private client LoRA CE -> sample-weighted factor-wise FedAvg
                       -> verified LLM-target CE + auxiliary reverse KL
```

Execution-verified hard teacher targets are the supported portable mechanism.
Reverse KL remains auxiliary because its independent increment is not stable
across training seeds or the Gemma family.

This fixed reference prevents silent baseline drift; it does **not** prohibit new
KD/Federated proposals. A substantively different mechanism may enter P1.7 if
it satisfies all of the following before a training command is added:

1. targets a documented EX failure, federated limitation, or novelty gap;
2. explains why it differs from the failed P0.9 selector and P0.10 FedDF
   implementations rather than retuning them;
3. preserves or explicitly revises the client-data, communication, teacher,
   and SLM-deployment boundaries;
4. defines a matched control, fixed budget, promotion metric, and stop rule;
5. starts with the cheapest diagnostic/smoke and reaches the full pool only
   after passing its preregistered gate.

A strong P1.7 proposal may be promoted ahead of a lower-value queued run after
the expected paper contribution and compute cost are documented. The
canonical method changes only after a positive full-scale matched result;
otherwise the branch is archived without tuning.

The execution-guided selector and client-ensemble distillation branches are closed:

- P0.9b global-error selection loses `2.03` Spider EX to its matched random
  control and adds 18 execution errors.
- P0.10 failed its frozen full-pool EX and execution-validity gate after a
  positive small screen. Do not tune or continue it. Exact commands and provenance are archived at
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`.
- P1.7a failed its fixed 512-row EX gate: preference KD scored 54.93 EX versus
  56.87 for matched positive-only CE (`-1.93` points).
  Its command and implementation are closed without tuning; compact evidence
  is archived at `paper/archive/closed_method_branches/P017A_PREFERENCE_KD_2026-08-28.md`.

## Active order

| Order   | Task                                                                           | Status / decision                                                                                         |
| ------- | ------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------------------------- |
| P1.1a   | Add fixed warm-up, process metrics, and repeated GPU telemetry                 | complete: final protocol code `487b3b2`, full 320-test suite                                              |
| P1.2    | Audit EX gains, execution-error transitions, and representative transfer cases | complete: artifact `4527a76`                                                                              |
| P1.4a   | Deterministic adapter/communication/table manifest                             | complete: producer `f59a040`, artifact commit `147f455`, registry ID `audit.paper.tables.qwen.s0`         |
| P1.4b   | Related-work matrix and manuscript skeleton                                    | complete: title narrowed; canonical outputs `RELATED_WORK_NOVELTY_MATRIX.md` and `MANUSCRIPT_SKELETON.md` |
| P0.8a   | Final T3 pure-FL versus frozen FedLS-SQL at seed 1                             | complete: 61.99 vs 65.76 EX (`+3.77`, paired `p=0.00483`)                                                 |
| P0.8a-E | Complete the missing seed-1 T2/T3 trajectory observations                      | complete: result commit `dbd703b`, registered full seed-1 trajectory                                      |
| P2.1    | Method prose and architecture/privacy-boundary figure                          | complete: paper-ready draft and verified SVG under `paper/drafts/`                                        |
| P1.7a   | Execution-verified preference/contrastive KD                                   | closed negative: 54.93 vs 56.87 EX; exact artifacts archived at nested `74f0a43`                          |
| P1.1b   | Qwen student 1.5B versus teacher 7B resource benchmark                         | complete: 5/5 eligible each; student `2.09x` faster and uses `48.73%` less allocated VRAM                 |
| P1.8    | Optional Secure Sum compatibility and overhead audit                           | complete: real 18.46M-parameter replay passed; result `6c67e79`                                            |
| P1.5a-R | Matched FedProx-LoRA integration smoke retry                                   | complete: five clients, positive proximal loss, plaintext FedAvg, 104 s, `noop_suspect=False`              |
| P1.5b   | Matched FedProx-LoRA T3 production baseline                                   | complete: setup `ed34fcfd...`, code `897fb66`, compact result `d48f05b`                                   |
| P1.5c   | Full-Spider FedProx endpoint evaluation                                       | complete/closed: 62.77 vs pure-FL 64.31 EX; 22/38 paired wins/losses; result `458a9f3`                    |
| P1.5d   | FedProx T1/T2 Spider trajectory diagnostic                                    | complete: T1/T2 deltas `-0.87/-2.22` EX; result `9537103`                                                  |
| P1.5e   | FedProx OOD / FedLS-FedProx extension                                         | **do not run: primary T3 endpoint did not improve on registered pure FL**                                  |
| P2.2    | Assemble paper tables and figures from closed evidence                         | active parallel CPU lane; include the separate P1.8 compatibility/overhead row                            |
| P1.3a   | Stronger semantic-domain-skew split and audit                                  | complete: audit passed at code/data commit `e97583d`                                                       |
| P1.3b   | Shared-client FL/FedLS T1 training on stronger domain skew                     | complete: matched training records pulled at `ce93c79`                                                     |
| P1.3c   | Full-Spider T1 paired evaluation                                               | **GPU-ready now**; run/publish, then stop for the frozen paired gate                                       |
| P0.8b   | Final T3 pure-FL versus frozen FedLS-SQL at seed 2                             | blocked only by legacy setup compatibility under current code; not by Secure Sum                           |
| P1.6    | Federated-7B feasibility/claim gate                                            | default excluded after P1.1b; reopen only if the manuscript retains a direct federated-7B claim           |
| P0.7t   | Gemma 9B zero-shot Spider ceiling                                              | optional context only                                                                                     |

Ordinary `eval_arms` timing is not official resource evidence because it
measures the first decode without a fixed warm-up. Use only the runner below
for P1.1b.

The first P1.1b collection used a superseded PID-presence rule and produced
zero eligible rows under Windows/WDDM. Retain it as observational provenance;
do not merge it with the revised independent-repetition protocol.

P1.1b-v2 is complete and closes the scoped deployment-inference component of
the advisor's scientific question. It does not establish training-resource or
federated-7B superiority. P0.8b is independent of Secure Sum but its old
`setup.json` predates the aggregation-protocol fingerprint, so the continuation
command remains blocked until a tested legacy-plaintext migration exists.

P1.4b, P1.1b, P2.1, the scoped P1.8 compatibility audit, and all P1.5 FedProx
work are closed. The next experimental gate is one stronger-skew screen.
Accuracy experiments use explicit plaintext weighted aggregation for matched
lineage; Secure Sum is an optional audited layer, not an accuracy gate. Decide
federated-7B feasibility only if the manuscript retains an empirical
large-model-FL comparison.

P1.7a is closed. Its fixed global-SLM preference loss reduced Spider EX by
1.93 points versus positive-only CE, so no full-pool extension,
coefficient sweep, pair filtering, or related command remains active. The
canonical verified-target CE plus auxiliary RKL method is unchanged. A future
method proposal must begin from a new evidence-backed hypothesis rather than
retuning P1.7a.

## P1.8 — optional Secure Sum compatibility audit — complete

**Purpose:** show that FedLS-SQL's weighted LoRA aggregation can be wrapped by
a pairwise-masked Secure Sum layer without changing its numerical objective,
and quantify the added cost separately from accuracy experiments.

The implementation at `3c21b96` passed the core and dropout/equivalence tests.
The real Qwen five-client replay at result commit `6c67e79` covered 18,464,768
adapter parameters and passed with maximum error `3.7253e-9`, mean error
`1.4493e-10`, and cosine `0.9999999999999983`. It took `7.1147 s`; float64
masked uploads increased comparable round communication by approximately
`49.93%`, while protocol metadata was only `1,401` bytes.

This closes a compatibility and overhead claim, not a formal cryptographic or
DP claim. Do not relabel historical accuracy lineages as Secure-Sum-produced,
and do not replay every retained round. Standard matched accuracy experiments
use `--aggregation-protocol plaintext`; a dedicated privacy-layer audit must
opt in with `--aggregation-protocol secure_sum`. The default-policy change is
nested commit `fc7899a`. Exact command and provenance:
`paper/archive/completed_runbooks/P1_8A_SECURE_SUM_COMPATIBILITY_2026-08-29.md`.

## P1.5 — matched FedProx-LoRA baseline — complete negative

**Purpose:** answer the reviewer objection that the headline comparison uses
only FedAvg-based federated optimization. P1.5 is a baseline, not a FedLS-SQL
component or a proposed optimizer contribution.

The frozen design is:

1. canonical client loss `CE + (mu/2)||theta-theta_t||^2` over trainable LoRA
   parameters, where `theta_t` is captured from the broadcast adapter before
   any local optimizer step or crash-checkpoint restore;
2. `mu=0.01`, fixed on 2026-08-29 before any FedProx Spider evaluation; there
   is no coefficient sweep or test-set selection;
3. the same Qwen student, `K=5`, `alpha=0.5` split, LoRA rank, client rows,
   local epoch, optimizer budget, three rounds, seed 0, and evaluation protocol
   as the independent pure-FL headline lineage;
4. no public teacher stage in the FedProx-only baseline, so it tests whether a
   stronger federated optimizer alone closes the FedLS-SQL accuracy gap;
5. implementation `897fb66`: `client_prox_mu` is locked by the run setup, client-stage fingerprint, and
   trainer resume signature; the mathematical/wiring tests pass in the full
   334-test suite;
6. one production run only, followed by Spider EX/execution-error comparison
   with pure FL, centralized-standard, and FedLS-SQL.

The first P1.5a root completed all client training and weighted FedAvg, but its
acceptance check correctly found zero observed proximal loss. With two
optimizer updates, the cosine/warm-up schedule makes the first update use LR
zero; the second forward still sees the round-start parameters, and parameter
drift occurs only after that forward. Preserve
`p15a_fedprox_mu001_noicl_k5_e1_t1_smoke_s0` as a diagnostic; do not mutate or
delete it.

P1.5a-R uses three client micro-steps and `grad_accum=1`. The third forward
must observe the drift created by update two and therefore a positive proximal
term. It uses a fresh immutable root because `client_max_steps` is part of the
setup/fingerprint. This remains an integration/resume smoke, not paper accuracy
evidence. Rerunning the exact line resumes/skips completed stages safely.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/p15a2_fedprox_mu001_noicl_k5_e1_t1_smoke_s0'; uv run python experiments/federated/run.py run --arm fedavg --rounds 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --client-max-steps 3 --client-prox-mu 0.01 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 1 --max-len 2560 --save-steps 1 --aggregation-protocol plaintext --out $R --seed 0 --stage p15a2; if ($LASTEXITCODE -ne 0) { throw 'P1.5a-R FedProx smoke failed; rerun this exact line and output root to resume' }; $S=Get-Content -LiteralPath "$R/setup.json" -Raw | ConvertFrom-Json; if ([double]$S.recipe.client_prox_mu -ne 0.01 -or $S.recipe.aggregation_protocol -ne 'plaintext' -or $S.recipe.server_method -ne 'none' -or [int]$S.recipe.client_max_steps -ne 3) { throw 'P1.5a-R setup contract mismatch' }; foreach ($I in 1..5) { $A="$R/round_1/client_$I/adapter/adapter_config.json"; $M="$R/round_1/client_$I/adapter_meta.json"; if (-not (Test-Path -LiteralPath $A) -or -not (Test-Path -LiteralPath $M)) { throw "Incomplete P1.5a-R client $I" }; $V=Get-Content -LiteralPath $M -Raw | ConvertFrom-Json; if ([double]$V.prox_mu -ne 0.01 -or [double]$V.mean_prox_loss_this_call -le 0) { throw "FedProx objective was not exercised for client $I" } }; if (-not (Test-Path -LiteralPath "$R/round_1/fedavg_adapter/adapter_config.json")) { throw 'Missing P1.5a-R weighted FedAvg output' }; Write-Host 'P1.5a-R complete: client-only FedProx objective, fingerprints, resume path, and plaintext weighted FedAvg integration passed; stop and review before P1.5b'
```

P1.5a-R passed: all five clients reported positive mean proximal loss, the
sample-weighted plaintext factor FedAvg completed in 104 seconds,
`noop_suspect=False`, and the minimum client-delta cosine was `0.2759`. The
smoke has no accuracy interpretation.

P1.5b is the single frozen production lineage. It matches the registered
seed-0 pure-FL run in student, split, client rows, one local epoch, LoRA rank,
optimizer budget, three rounds, and seed; the only intended training change is
`client_prox_mu=0.01`. No public pool, teacher, CE server stage, or RKL stage is
present. Rerun the exact line and root after interruption; completed clients and
rounds are skipped by their immutable fingerprints.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0'; foreach ($P in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_1_train.csv','processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_2_train.csv','processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_3_train.csv','processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_4_train.csv','processed_data/SPIDER/federated_noniid/alpha_0.5/k5/client_5_train.csv')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P1.5b input: $P" } }; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --client-prox-mu 0.01 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --aggregation-protocol plaintext --out $R --seed 0 --stage p15b; if ($LASTEXITCODE -ne 0) { throw 'P1.5b FedProx T3 training failed; rerun this exact line and output root to resume' }; $S=Get-Content -LiteralPath "$R/setup.json" -Raw | ConvertFrom-Json; if ([double]$S.recipe.client_prox_mu -ne 0.01 -or $S.recipe.aggregation_protocol -ne 'plaintext' -or $S.recipe.server_method -ne 'none' -or $null -ne $S.recipe.client_max_steps -or [int]$S.recipe.local_epochs -ne 1) { throw 'P1.5b setup contract mismatch' }; foreach ($N in 1..3) { foreach ($I in 1..5) { $A="$R/round_$N/client_$I/adapter/adapter_config.json"; $M="$R/round_$N/client_$I/adapter_meta.json"; if (-not (Test-Path -LiteralPath $A) -or -not (Test-Path -LiteralPath $M)) { throw "Incomplete P1.5b round $N client $I" }; $V=Get-Content -LiteralPath $M -Raw | ConvertFrom-Json; if ([double]$V.prox_mu -ne 0.01 -or [double]$V.mean_prox_loss_this_call -le 0 -or [int]$V.steps -le 0) { throw "Invalid P1.5b proximal metadata at round $N client $I" } }; if (-not (Test-Path -LiteralPath "$R/round_$N/fedavg_adapter/adapter_config.json")) { throw "Missing P1.5b aggregate at round $N" } }; if (-not (Test-Path -LiteralPath "$R/manifest.json")) { throw 'Missing P1.5b manifest' }; Write-Host 'P1.5b complete: matched FedProx-LoRA T3 trained with positive proximal loss in all 15 client stages; push compact results and stop before P1.5c evaluation'
```

P1.5b passed artifact review at result commit `d48f05b`. All three rounds use
setup `ed34fcfd0ac7e24a6082753e05ede6e5478ba49f75e521e1011941cf5250bc28`
and producing code `897fb66`; each round contains all 8,659 examples, 543
optimizer updates, five fresh client stages, positive proximal loss, and a
plaintext aggregate with `noop_suspect=False`. Mean client proximal losses
range from `0.0605–0.0753` at T1, `0.0335–0.0434` at T2, and
`0.0313–0.0398` at T3. Minimum pairwise client-delta cosine declines
`0.4527 -> 0.0616 -> 0.0123`; this documents persistent client disagreement
but is not an accuracy conclusion. Training wall time/VRAM are not promoted to
paper resource evidence because P1.5b was not a controlled repeated benchmark.

P1.5c evaluates only the new T3 endpoint on all 1,034 Spider test rows.
Centralized-standard, pure-FL T3, and FedLS-SQL T3 are not redundantly decoded;
their registered predictions are used for the local paired comparison after
the new result is pulled. Rerun this exact line to resume missing rows safely.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $A='artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0/round_3/fedavg_adapter'; $E='artifacts/eval_resume/p15c_fedprox_mu001_t3_spider_s0/eval_k0'; foreach ($P in @('processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv',"$A/adapter_config.json",'artifacts/federated/p15b_fedprox_mu001_noicl_k5_e1_t3_s0/manifest.json')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P1.5c input: $P" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fedprox_mu001_t3=$A" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P1.5c FedProx T3 Spider evaluation failed; rerun this exact line and resume root' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw 'Missing P1.5c evaluation manifests' }; Write-Host 'P1.5c complete: push compact eval results/config/predictions/manifests and stop for paired comparison against registered centralized, pure-FL, and FedLS-SQL T3 controls'
```

The primary FedProx promotion decision is closed. FedProx-LoRA T3 scores 62.77 EX/56.00 EM with 194 execution
errors versus pure FL's 64.31/57.45/193. On identical rows it has 22 gains and
38 regressions (`-1.55` EX; exact McNemar `p=0.0519`). The penalty reduces
mean client-delta norms by 44.1%, 47.6%, and 47.4% across rounds, but client CE
is 2.9%, 6.2%, and 8.7% higher than pure FL.

P1.5d is complete at result commit `9537103`. FedProx versus round-matched pure
FL is `55.80 vs 56.67` EX at T1 (`26/35` wins/losses, `p=0.306`) and
`59.96 vs 62.19` at T2 (`19/42`, `p=0.00444`). Together with T3's
`62.77 vs 64.31`, FedProx is lower at every observed round. There is no early
round advantage to motivate a FedLS-FedProx interaction screen. P1.5e remains
closed: do not run OOD, sweep `mu`, add a teacher stage, or start a combined
arm. Exact command and provenance are archived at
`paper/archive/completed_runbooks/P1_5D_FEDPROX_TRAJECTORY_2026-08-30.md`.

## P1.3 — stronger semantic-domain-skew sensitivity

P1.3a is complete at nested commit `e97583d`. The candidate is the canonical
grouped-domain Dirichlet split `alpha=0.1, K=5, seed=0`, compared with the main
`alpha=0.5, K=5, seed=0` split. Both contain the exact same 8,659-row multiset
(`sha256=dadda0e4...`) and keep databases disjoint across clients. Mean
per-client domain entropy falls from `3.0291` to `2.1834` bits and mean pairwise
domain JSD rises from `0.5266` to `0.8047` bits. Client-size ratio decreases
from `3.02x` to `1.88x`, so the claim is specifically stronger semantic-domain
skew, not stronger quantity skew or stronger heterogeneity on every axis.

P1.3b trains one arm-invariant client/FedAvg stage and reuses it for the FedLS
server stage. This makes the T1 comparison exactly matched in private rows,
initialization, local optimization, and aggregate. Accuracy uses explicit
plaintext weighted FedAvg; the existing Secure Sum audit is separate. The
production run is complete. The block below is retained as launch provenance;
do not rerun it after the acceptance-only failure. Use the corrected verifier
and publication command that follow, then stop for artifact review.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $H=(git rev-parse --short HEAD).Trim(); if ($H -ne 'e97583d') { throw "P1.3b requires nested code/data commit e97583d, found $H" }; $D='processed_data/SPIDER/federated_noniid/alpha_0.1/k5'; $A='audits/p13_alpha01_k5_s0_vs_alpha05_k5_s0.json'; $Scope=@('fedicl_sql','experiments/federated',$D,$A,'processed_data/BIRD/bootstrap_full_exmatch/train.csv','pyproject.toml','uv.lock'); git diff --quiet -- $Scope; if ($LASTEXITCODE -ne 0) { throw 'Uncommitted P1.3b code/input changes detected; inspect the scoped diff before running' }; git diff --cached --quiet -- $Scope; if ($LASTEXITCODE -ne 0) { throw 'Staged P1.3b code/input changes detected; publish or unstage them separately' }; $C='artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1'; $F='artifacts/federated/p13_alpha01_k5_e1_t1_fl_s0'; $K='artifacts/federated/p13_alpha01_k5_e1_t1_fedls_s0'; foreach ($P in @($A,"$D/meta.json","$D/split.json","$D/client_1_train.csv","$D/client_2_train.csv","$D/client_3_train.csv","$D/client_4_train.csv","$D/client_5_train.csv",'processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json')) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P1.3b input: $P" } }; $V=Get-Content -LiteralPath $A -Raw | ConvertFrom-Json; if (-not $V.passed -or [int]$V.candidate.n_rows -ne 8659 -or $V.candidate.source_multiset_sha256 -ne 'dadda0e4eda6ccc08ec2784cb892bece2dd6704ffb50556eac841150414eeb42' -or [double]$V.comparison.mean_pairwise_jsd_increase_bits -lt 0.10 -or [double]$V.comparison.mean_client_entropy_decrease_bits -lt 0.25) { throw 'P1.3a stronger-domain-skew audit contract failed' }; uv run python experiments/federated/run.py round --arm fedavg --round 1 --split-dir $D --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --aggregation-protocol plaintext --client-out $C --out $F --seed 0 --stage p13b; if ($LASTEXITCODE -ne 0) { throw 'P1.3b pure-FL/shared-client T1 failed; rerun this exact line to resume' }; uv run python experiments/federated/run.py round --arm fedkd --round 1 --split-dir $D --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1.0 --lambda-kd 1.0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --aggregation-protocol plaintext --client-out $C --out $K --seed 0 --stage p13b; if ($LASTEXITCODE -ne 0) { throw 'P1.3b FedLS T1 server stage failed; rerun this exact line to resume' }; foreach ($P in @("$C/fedavg_adapter/adapter_config.json","$F/manifest.json","$K/round_1/m_g/adapter_config.json","$K/manifest.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Incomplete P1.3b terminal artifact: $P" } }; $FS=Get-Content -LiteralPath "$F/setup.json" -Raw | ConvertFrom-Json; $KS=Get-Content -LiteralPath "$K/setup.json" -Raw | ConvertFrom-Json; if ($FS.recipe.split_dir -ne $D -or $KS.recipe.split_dir -ne $D -or $FS.recipe.aggregation_protocol -ne 'plaintext' -or $KS.recipe.aggregation_protocol -ne 'plaintext' -or $FS.recipe.server_method -ne 'none' -or $KS.recipe.server_method -ne 'rkl') { throw 'P1.3b setup contract mismatch' }; Write-Host 'P1.3b complete: shared private-client/FedAvg stage and FedLS T1 endpoint ready; run the publication command, push, and stop before P1.3c evaluation'
```

The first invocation completed both branches, then the old acceptance check
compared the absolute `recipe.split_dir` with relative `$D`. Training and
manifests are unaffected. Run this corrected verifier only; it performs no
training.

```powershell
$D='processed_data/SPIDER/federated_noniid/alpha_0.1/k5'; $C='artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1'; $F='artifacts/federated/p13_alpha01_k5_e1_t1_fl_s0'; $K='artifacts/federated/p13_alpha01_k5_e1_t1_fedls_s0'; foreach ($P in @("$C/fedavg_adapter/adapter_config.json","$F/setup.json","$F/manifest.json","$K/setup.json","$K/round_1/m_g/adapter_config.json","$K/manifest.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Incomplete P1.3b terminal artifact: $P" } }; $FS=Get-Content -LiteralPath "$F/setup.json" -Raw | ConvertFrom-Json; $KS=Get-Content -LiteralPath "$K/setup.json" -Raw | ConvertFrom-Json; $DR=(Resolve-Path -LiteralPath $D).Path; Write-Host "FL: split=$($FS.recipe.split_dir) protocol=$($FS.recipe.aggregation_protocol) server=$($FS.recipe.server_method)"; Write-Host "FedLS: split=$($KS.recipe.split_dir) protocol=$($KS.recipe.aggregation_protocol) server=$($KS.recipe.server_method)"; if ($FS.recipe.split_dir -ne $DR -or $KS.recipe.split_dir -ne $DR -or $FS.recipe.aggregation_protocol -ne 'plaintext' -or $KS.recipe.aggregation_protocol -ne 'plaintext' -or $FS.recipe.server_method -ne 'none' -or $KS.recipe.server_method -ne 'rkl') { throw 'P1.3b corrected setup verification failed' }; $FR=(Get-Content -LiteralPath "$F/manifest.json" -Raw | ConvertFrom-Json).rounds.'1'.result_path; $KR=(Get-Content -LiteralPath "$K/manifest.json" -Raw | ConvertFrom-Json).rounds.'1'.result_path; if ([string]::IsNullOrWhiteSpace($FR) -or [string]::IsNullOrWhiteSpace($KR) -or -not (Test-Path -LiteralPath $FR) -or -not (Test-Path -LiteralPath $KR)) { throw 'P1.3b manifests do not resolve compact results' }; Write-Host 'P1.3b corrected verification passed; run the publication command next, without retraining'
```

Publication command for the completed P1.3b training records only; it excludes
all adapters, checkpoints, resume state, and ignored `artifacts/` content.

```powershell
$F='artifacts/federated/p13_alpha01_k5_e1_t1_fl_s0'; $K='artifacts/federated/p13_alpha01_k5_e1_t1_fedls_s0'; git diff --cached --quiet; if ($LASTEXITCODE -ne 0) { throw 'Staged changes already exist; publish them separately before P1.3b results' }; $FR=(Get-Content -LiteralPath "$F/manifest.json" -Raw | ConvertFrom-Json).rounds.'1'.result_path; $KR=(Get-Content -LiteralPath "$K/manifest.json" -Raw | ConvertFrom-Json).rounds.'1'.result_path; if ([string]::IsNullOrWhiteSpace($FR) -or [string]::IsNullOrWhiteSpace($KR)) { throw 'Missing P1.3b result paths in manifests' }; $FD=Split-Path -Parent $FR; $KD=Split-Path -Parent $KR; $Files=@("$FD/config.json","$FD/metrics.json","$KD/config.json","$KD/metrics.json"); foreach ($P in $Files) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing compact P1.3b result file: $P" } }; git add -- $Files; if ($LASTEXITCODE -ne 0) { throw 'P1.3b git add failed' }; $Want=@($Files | ForEach-Object { ((Resolve-Path -LiteralPath $_ -Relative) -replace '^\.\\','' -replace '\\','/') } | Sort-Object); $Got=@(git diff --cached --name-only | Sort-Object); if (($Want -join '|') -ne ($Got -join '|')) { throw "Unexpected staged paths; expected=$($Want -join ',') actual=$($Got -join ',')" }; git commit -m 'exp: add stronger-domain-skew T1 training'; if ($LASTEXITCODE -ne 0) { throw 'P1.3b git commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'P1.3b git push failed' }; Write-Host 'P1.3b compact training results committed and pushed; stop for pull/review before evaluation'
```

The frozen P1.3c promotion gate is Spider EX improvement of at least `+2.0`
points, paired corrections greater than regressions, and no increase in
execution-error count. Passing opens a T3 extension; a smaller positive result
is reported as directional T1 evidence but does not open T3. Failure closes
the sensitivity and narrows RQ3 to the main `alpha=0.5` partition.

P1.3b artifact review passed at nested result commit `ce93c79`. The two records
contain byte-equivalent `client_training` and `aggregation` summaries: 8,659
private examples, 543 optimizer updates, five fresh client stages, and the
same non-noop plaintext aggregate (`min_cosine=0.407722`). FedLS adds exactly
one fresh RKL server stage over 3,873 teacher-selected public rows, initialized
from that shared aggregate. These are valid training endpoints but contain no
accuracy result; P1.3c evaluates both on the same 1,034 canonical Spider rows.
The tracked-diff and Git-blob checks intentionally fail if the server's
centralized CSVs differ from the committed evaluation inputs; inspect such
drift instead of silently evaluating a different test set. Git blob identity
is used instead of raw file SHA so a clean Windows checkout is not rejected
only because of line-ending conversion. Rerun the exact command and resume root
after interruption.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $H=(git rev-parse --short HEAD).Trim(); if ($H -ne 'ce93c79') { throw "P1.3c requires nested result commit ce93c79, found $H" }; $T='processed_data/SPIDER/centralized/train.csv'; $X='processed_data/SPIDER/centralized/test.csv'; $C='artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1/fedavg_adapter'; $K='artifacts/federated/p13_alpha01_k5_e1_t1_fedls_s0/round_1/m_g'; $E='artifacts/eval_resume/p13c_alpha01_fl_fedls_t1_spider_s0/eval_k0'; foreach ($P in @($T,$X,"$C/adapter_config.json","$K/adapter_config.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P1.3c input: $P" } }; git diff --quiet -- $T $X; if ($LASTEXITCODE -ne 0) { throw 'P1.3c Spider evaluation inputs have unstaged tracked edits; inspect/reconcile them before evaluation' }; git diff --cached --quiet -- $T $X; if ($LASTEXITCODE -ne 0) { throw 'P1.3c Spider evaluation inputs have staged tracked edits; publish or restore them separately' }; $TB=(git rev-parse "HEAD:$T").Trim(); $XB=(git rev-parse "HEAD:$X").Trim(); if ($TB -ne 'c963d55bd42a2e6dddf73c06b355954855fc96a5' -or $XB -ne '5ab607083d932c05c4fdabe226a10e1729f6169c') { throw 'P1.3c canonical Spider Git-blob identity mismatch' }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train $T --test-csv $X --arms "fl_alpha01_t1=$C" "fedls_alpha01_t1=$K" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed 0 --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P1.3c paired Spider evaluation failed; rerun this exact line to resume' }; $M=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | ForEach-Object { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; if ($V.status -eq 'completed') { $_ } }); if ($M.Count -ne 1) { throw "Expected one completed P1.3c manifest, found $($M.Count)" }; Write-Host 'P1.3c evaluation complete; run the publication command and stop for paired gate analysis'
```

Publication command for P1.3c only. It resolves the timestamped result through
the dedicated completed manifest and publishes config, metrics, and both
prediction files; the resume checkpoint and manifest remain server-local.

```powershell
$E='artifacts/eval_resume/p13c_alpha01_fl_fedls_t1_spider_s0/eval_k0'; git diff --cached --quiet; if ($LASTEXITCODE -ne 0) { throw 'Staged changes already exist; publish them separately before P1.3c' }; $M=@(Get-ChildItem -LiteralPath "$E/manifests" -Filter '*.json' -File | ForEach-Object { $V=Get-Content -LiteralPath $_.FullName -Raw | ConvertFrom-Json; if ($V.status -eq 'completed') { [PSCustomObject]@{ Path=$_.FullName; Value=$V } } }); if ($M.Count -ne 1) { throw "Expected one completed P1.3c manifest, found $($M.Count)" }; $V=$M[0].Value; $Files=@([string]$V.artifacts.config,[string]$V.artifacts.metrics)+@($V.artifacts.predictions | ForEach-Object { [string]$_ }); if ($Files.Count -ne 4) { throw "Expected four compact P1.3c files, found $($Files.Count)" }; foreach ($P in $Files) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing compact P1.3c result file: $P" } }; $Cfg=Get-Content -LiteralPath $V.artifacts.config -Raw | ConvertFrom-Json; $Met=Get-Content -LiteralPath $V.artifacts.metrics -Raw | ConvertFrom-Json; if ($Cfg.resume_dir -ne $E -or (@($Cfg.arms) -join '|') -ne 'fl_alpha01_t1=artifacts/federated/p13_alpha01_k5_e1_t1_shared_s0/round_1/fedavg_adapter|fedls_alpha01_t1=artifacts/federated/p13_alpha01_k5_e1_t1_fedls_s0/round_1/m_g' -or [int]$Met.n_eval -ne 1034 -or @($Met.arms.PSObject.Properties.Name).Count -ne 2) { throw 'P1.3c compact result contract mismatch' }; foreach ($P in @($V.artifacts.predictions)) { if ((Import-Csv -LiteralPath $P).Count -ne 1034) { throw "Incomplete P1.3c predictions: $P" } }; git add -- $Files; if ($LASTEXITCODE -ne 0) { throw 'P1.3c git add failed' }; $Want=@($Files | ForEach-Object { ((Resolve-Path -LiteralPath $_ -Relative) -replace '^\.\\','' -replace '\\','/') } | Sort-Object); $Got=@(git diff --cached --name-only | Sort-Object); if (($Want -join '|') -ne ($Got -join '|')) { throw "Unexpected staged paths; expected=$($Want -join ',') actual=$($Got -join ',')" }; git commit -m 'exp: evaluate stronger-domain-skew T1'; if ($LASTEXITCODE -ne 0) { throw 'P1.3c git commit failed' }; git push; if ($LASTEXITCODE -ne 0) { throw 'P1.3c git push failed' }; Write-Host 'P1.3c compact evaluation committed and pushed; stop for pull/review before any T3 extension'
```

## P0.8a-E — complete

The exact command and acceptance record are archived at
`paper/archive/completed_runbooks/P0.8A_E_SEED1_TRAJECTORY_2026-08-26.md`.
Canonical result commit: `dbd703b`. Do not rerun or launch seed 2
automatically.

## P0.8b — blocked pending legacy plaintext setup compatibility

**Purpose when reactivated:** close the three-training-seed reliability result after seed 1
replicated the final FedLS-SQL gain (`+3.77` Spider EX, `p=0.00483`). Seed 2
already has canonical T1 checkpoints. This command extends those exact
lineages through rounds 2 and 3 and evaluates only the final Spider endpoints;
it does not retrain round 1.

The block below is retained only for lineage and resume-contract audit. **Do
not run it under current code:** the old roots predate the aggregation-protocol
field now included in `setup.json`. Reactivate it only after a tested migration
treats the missing legacy field as explicit plaintext while preserving setup
identities (`8b02d882...` and `99aa70ed...`). Secure Sum is not required for
this accuracy continuation. Do not restart round 1 or change scientific flags.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $S=2; $F='artifacts/federated/fedavg_noicl_k5_e1_t1_s2'; $K='artifacts/federated/fedkd_noicl_k5_e1_t1_s2'; $E='artifacts/eval_resume/fedls_final_t3_spider_s2/eval_k0'; foreach ($P in @('processed_data/SPIDER/federated_noniid/alpha_0.5/k5/meta.json','processed_data/SPIDER/centralized/train.csv','processed_data/SPIDER/centralized/test.csv','processed_data/BIRD/bootstrap_full_exmatch/train.csv','artifacts/teacher_logit_cache/rkd_k0_full/meta.json',"$F/setup.json","$F/manifest.json","$F/round_1/fedavg_adapter/adapter_config.json","$K/setup.json","$K/manifest.json","$K/round_1/m_g/adapter_config.json")) { if (-not (Test-Path -LiteralPath $P)) { throw "Missing P0.8b input or canonical T1 artifact: $P" } }; $FS=Get-Content -LiteralPath "$F/setup.json" -Raw | ConvertFrom-Json; $KS=Get-Content -LiteralPath "$K/setup.json" -Raw | ConvertFrom-Json; if ($FS.setup_id -ne '8b02d882fc9f3d4b1053959a189731d4d59969d430a1032a90e71f56520e4447') { throw "Unexpected pure-FL seed-2 setup identity: $($FS.setup_id)" }; if ($KS.setup_id -ne '99aa70edb94e06feff864ed5cfea6516e934e79314a60d11a38bac3f8ceb9ef3') { throw "Unexpected FedLS seed-2 setup identity: $($KS.setup_id)" }; foreach ($N in @(2,3)) { $P=$N-1; $I="$F/round_${P}/fedavg_adapter"; uv run python experiments/federated/run.py round --arm fedavg --round $N --init-adapter $I --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --seed $S --stage poc --out $F; if ($LASTEXITCODE -ne 0) { throw "Pure-FL seed 2 round $N failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$F/round_${N}/fedavg_adapter/adapter_config.json")) { throw "Incomplete pure-FL seed 2 round $N" } }; foreach ($N in @(2,3)) { $P=$N-1; $I="$K/round_${P}/m_g"; uv run python experiments/federated/run.py round --arm fedkd --round $N --init-adapter $I --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --client-retrieval dail_weighted --client-demo-style never_schema --client-demo-k-fixed --client-schema-style full --client-embedder BAAI/bge-small-en-v1.5 --client-tau 0.85 --client-dail-alpha 0.6 --client-dail-shortlist 32 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --lambda-ft 1.0 --lambda-kd 1.0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --schema-style full --retrieval dail_select --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --demo-style never_schema --model Qwen/Qwen2.5-1.5B-Instruct --lora-r 16 --lr 0.0002 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --seed $S --stage poc --out $K; if ($LASTEXITCODE -ne 0) { throw "FedLS-SQL seed 2 round $N failed; rerun this exact line to resume" }; if (-not (Test-Path -LiteralPath "$K/round_${N}/m_g/adapter_config.json")) { throw "Incomplete FedLS-SQL seed 2 round $N" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fl_s2_t3=$F/round_3/fedavg_adapter" "fedls_s2_t3=$K/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --model Qwen/Qwen2.5-1.5B-Instruct --batch-size 16 --seed $S --resume-dir $E --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'P0.8b final Spider evaluation failed; rerun this exact line to resume' }; if (-not (Test-Path -LiteralPath "$E/manifests")) { throw "Missing P0.8b evaluation manifest directory: $E/manifests" }; Write-Host 'P0.8b complete: seed-2 pure FL and FedLS-SQL T3 evaluated; push compact results and stop for three-seed analysis'
```

After completion, push only compact federated results and evaluation
metrics/configs/predictions/manifests. Stop for paired validation and the
three-seed mean/sample-SD calculation; do not launch an OOD seed sweep.

Completed P0.8a command provenance is archived at
`paper/archive/completed_runbooks/P0.8A_SEED1_T3_2026-08-26.md`.

## P1.4a — complete

The exact command, failure history, split-lineage handling, and acceptance
record are archived at
`paper/archive/completed_runbooks/P1.4A_COMMUNICATION_2026-08-26.md`. Do not
rerun unless an audited source artifact changes and a new immutable output is
explicitly required.

## P1.1 acceptance contract

The benchmark implementation must:

1. warm up each loaded model in-process on deterministic non-reported inputs;
2. synchronize CUDA immediately before and after every timed region;
3. separate model loading, warm-up, generation, and SQL scoring time;
4. report fresh-run latency/throughput, peak allocated and reserved VRAM, and
   process RSS for at least five repetitions;
5. compare identical rows and decoding, declare precision/quantization and
   batch size, and run student/teacher sequentially on the same selected GPU;
6. sample device utilization, memory, clocks, and pstate throughout each
   repetition without enumerating PIDs; telemetry is descriptive;
7. label every fresh successful repetition `eligible`, report medians plus IQR,
   and exclude only failed or resumed rows from the primary latency table;
8. preserve raw per-repetition JSON and runtime/GPU provenance.

This is a repeated shared-server benchmark, not a guarantee of hardware
exclusivity. The operator selects a time with no intentionally concurrent GPU
job. Repetitions are analyzed independently; PID presence is neither sampled
nor used as an exclusion rule.

P1.1a is implemented by `experiments/resource_benchmark/run.py` and guarded by
`experiments/resource_benchmark/summarize.py`. Each complete repetition is an
atomic resumable unit. Re-running the exact command skips a terminal result or
continues missing repetitions; a fingerprint mismatch requires a new root.

## P1.1b — Qwen 1.5B versus 7B steady-state inference — complete

**Status:** complete; canonical comparison fingerprint
`60665e60a63ae93c1871401d01a9094caa0e82454f79bf1be473085d794c13c9`.

**Purpose:** measure the deployment-side cost difference on the same 32 Spider
rows. The final 1.5B FedLS adapter runs in its canonical BF16 path; the 7B
teacher runs in its canonical 4-bit reference path. This is deliberately
conservative for the teacher and is not a federated-7B training comparison.

Both models completed 5/5 eligible fresh repetitions on identical 32-row
Spider inputs. Median latency was 0.7873 s/query for the BF16 FedLS-SQL student
and 1.6460 s/query for the 4-bit teacher (`2.09x`); peak allocated VRAM was
3,474.6 versus 6,776.8 MB. Exact commands, protocol, output roots, dispersion,
and claim limits are archived at
`paper/archive/completed_runbooks/P1_1B_RESOURCE_BENCHMARK_2026-08-28.md`.
Do not rerun unless the deployment claim, hardware, model precision, or
protocol changes and a new immutable comparison is explicitly required.

## Deferred command provenance

Completed and superseded commands are not duplicated in this active file:

- P0.0–P0.10e snapshot:
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`;
- pre-FedLS/ICL runbooks: `paper/archive/pre_fedls_2026-08/legacy_runbooks/`;
- immutable checkpoint and evaluation mappings: `paper/notes/RESULT_REGISTRY.md`.

## After a completed block

1. Commit only metrics, configs, predictions, manifests, and compact audits;
   never commit model weights or resume checkpoints.
2. Pull and validate row counts, fingerprints, paired EX/EM, and execution
   errors before changing the queue.
3. Update `RESULT_REGISTRY.md`, `paper/results/MAIN_RESULTS.md`, `LAB_LOG.md`,
   `EXPERIMENT_MATRIX.md`, and `PAPER_EVIDENCE_PLAN.md` once per decision gate.
4. Archive closed commands instead of leaving them in the active queue.
