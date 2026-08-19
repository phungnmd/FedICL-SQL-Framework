# Next runs — pinning down the round-scaling result

> Rewritten 2026-08-16. Blocks A–D are closed. `T=3` reaches **69.54 EX**
> against 63.35 at `T=1`, and both the pre-server and post-server curves rise at
> every round. The open questions are no longer whether the method works but
> where the curve stops, whether it survives off-distribution, and whether it
> beats a budget-matched centralized model. Updated 2026-08-18: G, H and J are
> closed. Rounds hold on all four benchmarks; the two components turn out to be
> orthogonal. Updated 2026-08-19: the round-2/3 `pre-server` adapters were
> correctly identified as carrying KD from earlier rounds, so they are not a
> pure-FL multi-round control. Block K adds the missing ablation.

## Status

| Block | What it asked                                | Outcome                                                                                                                     |
| ----- | -------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
| A     | seeds for the distillation-only control      | closed — federated stage `+1.39 ± 1.12`, `p=0.165` at `T=1`                                                                 |
| B     | does that survive off-distribution           | closed — yes (`+1.64`, `p=0.0098`); distillation's increment does not (`+0.34`)                                             |
| C     | is one local epoch the right operating point | closed — `E=2` is `+4.55` pre-server, `+0.19` at the endpoint                                                               |
| D     | do rounds compound                           | closed — **yes**, endpoint `63.35 → 66.15 → 69.54`                                                                          |
| G     | budget-matched ceiling                       | closed — centralized saturates after epoch 2 (67.60, `p=0.606`); `T=3` is `+1.93` over it (`p=0.172`)                       |
| H     | rounds off-distribution                      | closed — rounds hold on all four benchmarks (`+4.86` … `+6.69`); the server step is null in all nine off-distribution cells |
| J     | BIRD cross-corpus transfer                   | closed — server step `+8.28`/`+3.91` (`p<1e-6`) there, federation alone `+0.26`; **the two components are orthogonal**      |
| **K** | pure FL through three rounds                 | **open — run this next**; required for `Centralized <> FL <> FL-KD`                                                         |
| **F** | where does the curve stop                    | **open — run after K**, `T=4`/`T=5`                                                                                         |
| **I** | seeds                                        | **open — run in parallel with F on the second GPU**                                                                         |

Seeds no longer wait on F: the headline is the `T=1→3` trajectory, not the
plateau value, so replicating the trajectory at seed 1 is valid whatever F
returns.

The `T=1` numbers throughout this file remain correct for `T=1`. They are
waypoints, not the method's operating point.

## K. Pure FL-only through `T=3` — RUN THIS NEXT

This is the missing causal control requested in the advisor review. The
existing `fedkd` round-2 and round-3 `fedavg_adapter` files are only pre-server
within their current round: they were initialized from the previous round's
post-KD `m_g`. They must not be named `FL` or treated as an FL-only branch.

For `--arm fedavg`, `server_method="none"`. The runner returns the round's
`fedavg_adapter` as `m_g`, so round `t+1` automatically warm-starts from the
previous FedAvg adapter. No public pool, teacher, or logit cache is read.

### One-shot command: train, validate, and evaluate everything

Run this single PowerShell line from the `fedicl-sql/` repository root. It is
fail-fast and safe to rerun for resume.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; $R='artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0'; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed 0; if ($LASTEXITCODE -ne 0) { throw 'Pure-FL training failed' }; foreach ($n in 1..3) { $A="$R/round_$n/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete FL round ${n}: $A" }; if (Test-Path -LiteralPath "$R/round_$n/m_g") { throw "Unexpected server output at pure-FL round $n" } }; foreach ($ds in @(@('processed_data/SPIDER/centralized/test.csv','fl_only_spider_s0'),@('processed_data/SPIDER_REALISTIC/test.csv','fl_only_realistic_s0'),@('processed_data/SPIDER_SYN/test.csv','fl_only_syn_s0'),@('processed_data/SPIDER_DK/test.csv','fl_only_dk_s0'))) { Write-Host "=== $($ds[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $ds[0] --arms "fl_only_t1=$R/round_1/fedavg_adapter" "fl_only_t2=$R/round_2/fedavg_adapter" "fl_only_t3=$R/round_3/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($ds[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { throw "Evaluation failed: $($ds[0])" } }; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --arms "fl_only_t1=$R/round_1/fedavg_adapter" "fl_only_t2=$R/round_2/fedavg_adapter" "fl_only_t3=$R/round_3/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fl_only_bird_s0/eval_k0 --skip-completed; if ($LASTEXITCODE -ne 0) { throw 'BIRD evaluation failed' }; Write-Host 'Block K complete: pure FL T1-T3 trained and evaluated on Spider, Realistic, Syn, DK, and BIRD'
```

### Train seed 0

Run from the `fedicl-sql/` repository root:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py run --arm fedavg --rounds 3 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0 --seed 0
```

Expected lineage:

```text
base -> round_1/fedavg_adapter
     -> round_2/fedavg_adapter
     -> round_3/fedavg_adapter
```

There must be no `round_*/m_g` directory distinct from `fedavg_adapter`, no
server-stage metrics, and no BIRD/public-pool steps.

```powershell
$R='artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0'; foreach ($n in 1..3) { $A="$R/round_$n/fedavg_adapter"; if (-not (Test-Path -LiteralPath "$A/adapter_config.json")) { throw "Incomplete FL round ${n}: $A" }; if (Test-Path -LiteralPath "$R/round_$n/m_g") { throw "Unexpected server output at pure-FL round $n" } }; Write-Host 'Pure-FL lineage OK: rounds 1-3 contain FedAvg adapters and no server M_G'
```

### Evaluate Spider dev and the three Spider robustness sets

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0'; foreach ($ds in @(@('processed_data/SPIDER/centralized/test.csv','fl_only_spider_s0'),@('processed_data/SPIDER_REALISTIC/test.csv','fl_only_realistic_s0'),@('processed_data/SPIDER_SYN/test.csv','fl_only_syn_s0'),@('processed_data/SPIDER_DK/test.csv','fl_only_dk_s0'))) { Write-Host "=== $($ds[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $ds[0] --arms "fl_only_t1=$R/round_1/fedavg_adapter" "fl_only_t2=$R/round_2/fedavg_adapter" "fl_only_t3=$R/round_3/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($ds[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $($ds[0])"; break } }
```

### Evaluate BIRD cross-corpus transfer

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/fedavg_only_noicl_k5_e1_t3_s0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --arms "fl_only_t1=$R/round_1/fedavg_adapter" "fl_only_t2=$R/round_2/fedavg_adapter" "fl_only_t3=$R/round_3/fedavg_adapter" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fl_only_bird_s0/eval_k0 --skip-completed
```

Primary table after completion:

```text
Centralized = central_3ep
FL          = fl_only_t3
FL-KD       = fedkd_t3
```

Use `T=1` as the already-matched sanity check: Centralized `62.19`, pure FL
`57.35`, FL-KD `63.35`. Do not fill the `T=3` FL row with the old
`fedkd_t3_preserver=66.05`; that adapter carries two earlier KD stages.

## Old framing, kept for the record

Run in PowerShell from the `fedicl-sql/` repository root. Every executable
command below is a single line. Blocks are ordered by what they decide about
the paper's central claim, not by cost.

The proposal is federated training combined with server-side distillation. Two
comparisons decide whether it has value:

| Comparison                                            | Status                                    |
| ----------------------------------------------------- | ----------------------------------------- |
| combination `62.74` vs federated alone `58.19`        | `+4.55`, 3 seeds, `p=0.046` — settled     |
| combination `62.74` vs **distillation alone** `61.22` | `+1.52`, control has **1 seed** — block A |

Block A is **closed** (2026-08-15). It finished the second row: across three
seeds the federated stage is worth `+1.39 ± 1.12`, `p = 0.165` — positive in
every seed, significant in two of three individually, not established across
seeds.

| Seed |  full | `base_rkl` | delta | paired `p` |
| ---- | ----: | ---------: | ----: | ---------: |
| 0    | 63.35 |      61.22 | +2.13 |      0.017 |
| 1    | 62.48 |      60.54 | +1.93 |      0.025 |
| 2    | 62.38 |      62.28 | +0.10 |      1.000 |

Block B is **closed** (2026-08-15) and it moved the target. The federated row
survives out of distribution; the distillation row does not. Full table in
section B. Remaining, in order: **C** (operating point), **D** (rounds), **E**
(seeds, optional).

Reordering the pipeline was tried and rejected on 2026-08-12: running
distillation first and the federated stage last scores 61.60, below the current
order's 63.35, because client training from an already-distilled model adds only
`+0.38`. Most of what the clients learn, the teacher already knows.

All training uses one local epoch, batch 1, gradient accumulation 16, max
length 2560, checkpoints every 200 steps. All evaluation is greedy, batch 16,
`k=0`, full Spider dev. Re-running any command resumes.

## A. Seeds for the distillation-only control (~3 h) — DONE 2026-08-15

Commands kept for reproduction. Results: `base_rkl_s1 = 60.54`,
`base_rkl_s2 = 62.28`.

`base_rkl` is the arm the whole proposal is measured against: the base model
with the same server step and **no private data at all**. It exists only for
seed 0, so the `+1.52` has no error bar. `--init-adapter` stays unset, which is
what makes these start from the base model. The teacher cache is shared —
the seed no longer blocks it, since at `--pool-size 0 --train-k 0` no seed can
change the rendered sequences.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/client_train/run.py --client processed_data/BIRD/bootstrap_full_exmatch/train.csv --out artifacts/control/base_rkl_s1/adapter --kd-direction rkd --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 1
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/client_train/run.py --client processed_data/BIRD/bootstrap_full_exmatch/train.csv --out artifacts/control/base_rkl_s2/adapter --kd-direction rkd --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 2
```

### Two GPUs: one seed each, in parallel

Each process peaks at about 26.9 GiB (`max_memory_allocated`, teacher 4-bit
co-loaded with the student), so this needs both cards to hold a full run on
their own. Launch one command per window; each trains its seed and then
evaluates it on the same card, and skips the evaluation if training failed.
The 45-second offset on the second window keeps the two evaluations from
minting the same timestamped `run_id`.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/client_train/run.py --client processed_data/BIRD/bootstrap_full_exmatch/train.csv --out artifacts/control/base_rkl_s1/adapter --kd-direction rkd --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 1; if ($LASTEXITCODE -eq 0) { uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms base_rkl_s1=artifacts/control/base_rkl_s1/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/control_base_s1/eval_k0 --skip-completed } else { Write-Host 'seed 1 training failed, eval skipped' }
```

```powershell
Start-Sleep -Seconds 45; $env:CUDA_VISIBLE_DEVICES='1'; uv run python experiments/client_train/run.py --client processed_data/BIRD/bootstrap_full_exmatch/train.csv --out artifacts/control/base_rkl_s2/adapter --kd-direction rkd --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 2; if ($LASTEXITCODE -eq 0) { uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms base_rkl_s2=artifacts/control/base_rkl_s2/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/control_base_s2/eval_k0 --skip-completed } else { Write-Host 'seed 2 training failed, eval skipped' }
```

```powershell
@('artifacts/control/base_rkl_s1/adapter','artifacts/control/base_rkl_s2/adapter') | ForEach-Object { if (-not (Test-Path -LiteralPath "$_/adapter_config.json")) { throw "Incomplete: $_" }; if (Test-Path -LiteralPath "$_/_ckpt") { throw "Still checkpointed, rerun to resume: $_" } }; Write-Host 'Block A adapters OK'
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms base_rkl_s1=artifacts/control/base_rkl_s1/adapter base_rkl_s2=artifacts/control/base_rkl_s2/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/control_base_s12/eval_k0 --skip-completed
```

Then `62.74 ± 0.53` can be tested against three control seeds instead of one.

### A-optional: the SeqKD control on seeds 1 and 2 (~1.7 h)

Only needed for the internal reverse-KL-versus-SeqKD ablation, which is no
longer the paper's main claim. Skip unless block A leaves GPU time free.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/client_train/run.py --client processed_data/BIRD/bootstrap_full_exmatch/train.csv --out artifacts/control/base_seqkd_s1/adapter --kd-direction none --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 1
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/client_train/run.py --client processed_data/BIRD/bootstrap_full_exmatch/train.csv --out artifacts/control/base_seqkd_s2/adapter --kd-direction none --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 2
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms base_seqkd_s1=artifacts/control/base_seqkd_s1/adapter base_seqkd_s2=artifacts/control/base_seqkd_s2/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/control_base_seqkd_s12/eval_k0 --skip-completed
```

## B. Out-of-distribution evaluation — DONE 2026-08-15

Six arms × three perturbed Spider test sets, 2,077 questions in total, seed 0,
greedy, `k=0`. Runs `eval_arms__s0__2026081{5T0605,5T0621,5T0630,5T0712,5T0729,5T0739}*`.

| Arm          | Spider dev | REALISTIC |   SYN |    DK | **OOD pooled** |   drop |
| ------------ | ---------: | --------: | ----: | ----: | -------------: | -----: |
| `base`       |      50.00 |     40.35 | 37.04 | 41.68 |      **39.05** | −10.95 |
| `fed_only`   |      57.35 |     54.92 | 49.32 | 45.23 |      **49.64** |  −7.71 |
| `seqkd_only` |      61.32 |     50.98 | 46.32 | 46.36 |      **47.47** | −13.85 |
| `kd_only`    |      61.22 |     51.18 | 47.20 | 47.85 |      **48.34** | −12.88 |
| `full`       |      63.35 |     52.95 | 49.61 | 47.85 |      **49.98** | −13.37 |
| `central_ft` |      62.19 |     55.31 | 51.06 | 46.92 |      **51.04** | −11.15 |

Pooled paired McNemar over all 2,077 questions, against the same contrast on
Spider dev at this seed:

| Contrast                                    | Spider dev |            OOD pooled | verdict                           |
| ------------------------------------------- | ---------: | --------------------: | --------------------------------- |
| `full − base`                               |     +13.35 |  **+10.93**, `p<1e−4` | holds                             |
| `full − kd_only` (federated stage)          |      +2.13 | **+1.64**, `p=0.0098` | **holds, and significant pooled** |
| `full − seqkd_only` (reverse KL over SeqKD) |      +2.03 |   **+2.50**, `p=1e−4` | **stronger off-distribution**     |
| `full − fed_only` (distillation)            |      +6.00 |   **+0.34**, `p=0.76` | **collapses**                     |
| `full − central_ft`                         |      +1.16 |   **−1.06**, `p=0.30` | sign flips, neither significant   |

Four readings:

1. **The federated row was the thing under test and it passed.** Per-set
   `+1.77 / +2.42 / 0.00`, mean `+1.40`, which is the three-seed Spider figure
   `+1.39` almost exactly. Pooled it reaches `p=0.0098`, better than it ever
   managed on Spider dev across seeds. It is not an artefact of evaluating on
   the clients' own corpus.
2. **The distillation row, which was the settled one, is the one that broke.**
   `+6.00` on Spider dev becomes `+0.34` pooled and is negative on REALISTIC.
   Distillation from the base model is still worth a great deal
   (`kd_only − base` is `+10.15` to `+10.83`); what collapses is its marginal
   value *on top of* the federated stage.
3. **The two components are complementary along different shift axes**, which is
   the honest positive story. On paraphrase and synonym shift (REALISTIC, SYN)
   private Spider federation carries the result and distillation adds nothing.
   On domain-knowledge shift (DK) it inverts: `kd_only` is `+6.17` over base
   while `fed_only` manages only `+3.55` (`p=0.067`). `full` is the only arm
   that is never worst — third, second, and joint first across the three sets.
   Neither half is sufficient, and which half matters depends on the shift.
4. **Reverse KL over SeqKD is stronger off-distribution than on it.** `+2.50`,
   `p=1e−4` pooled, against `+2.03` on Spider dev and `+1.71 ± 1.38 (p=0.165)`
   across seeds. Soft labels appear to transfer teacher uncertainty in a way
   hard labels do not. Still one seed off-distribution — do not promote it back
   to a claim yet, but it is no longer just a design choice.

The cost of this is that `central_ft` — the compute-matched, privacy-relaxed
centralized baseline — has the best pooled OOD score. `full` beats it on Spider
dev by `+1.16` and loses to it off-distribution by `−1.06`, neither significant.
"Competitive with centralized" is now the accurate phrase in both directions,
which is defensible; "better than centralized" is not.

### Commands, kept for reproduction (~1 h across two GPUs)

Spider dev shares its corpus with the private client shards and not with the
public BIRD pool, so the federated arm is evaluated on data drawn from its own
distribution while the distillation arm is not. That favours the federated
component, which is exactly the row the paper rests on.

The `+1.39` credited to the federated stage therefore needs to be shown outside
that distribution before it can be claimed. Three perturbed Spider test sets are
already processed; only `--test-csv` changes. Sizes: `SPIDER_REALISTIC` 508
questions, `SPIDER_SYN` 1,034, `SPIDER_DK` 535 — 2,077 in total per arm.

Style is not the concern being tested here: EX compares execution results, not
SQL text, and across the existing arms EM and EX already move in opposite
directions (the most Spider-styled model, at EM 50.58, has the *lowest* EX).
What these sets test is task distribution — paraphrases, synonym substitution,
and domain-knowledge questions.

### Arms

Three arms defend the `+1.39`; three more turn the run into a full replicate of
the seed-0 ablation table on out-of-distribution data. All six paths are the
ones the existing seed-0 evals used, so the OOD table lines up row for row with
`non_icl_full_pipeline_ablation_report.md`.

| Arm          | Adapter                                                                                                                                                                      | Why it is here                                                                                                                                                                             |
| ------------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `full`       | `federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g`                                                                                                                              | the proposed pipeline                                                                                                                                                                      |
| `kd_only`    | `control/base_rkl_s0/adapter`                                                                                                                                                | removes the federated stage                                                                                                                                                                |
| `fed_only`   | `federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter`                                                                                                              | removes distillation                                                                                                                                                                       |
| `base`       | *(none — the arm spec is `"base="`, an empty path; `parse_arm` maps that to `None`. Passing `base=base` makes PEFT treat `base` as a Hugging Face repo id and the run dies)* | the floor. EX falls on every OOD set, so without it no delta is readable                                                                                                                   |
| `central_ft` | `icl_ladder/qwen1b/ft_no_icl/adapter`                                                                                                                                        | trained on Spider only, while the pipeline also saw BIRD through the teacher. Whether the `+1.16` margin widens or narrows off-distribution is the strongest generalisation cell available |
| `seqkd_only` | `federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g`                                                                                                                         | completes the five-stage ladder; low marginal value since the SeqKD/RKL split is a design choice, drop it if GPU time is short                                                             |

Each command below loops the three test sets in order and stops on the first
failure. Both can run at once: evaluation loads only the 1.5B student
(~4.6 GB), and the `--resume-dir` paths do not overlap. The `Start-Sleep`
prevents the two processes from minting the same timestamped `run_id`.

GPU 0 — the three ablation arms:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; foreach ($s in @(@('SPIDER_REALISTIC','ood_realistic_s0'),@('SPIDER_SYN','ood_syn_s0'),@('SPIDER_DK','ood_dk_s0'))) { Write-Host "=== $($s[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv "processed_data/$($s[0])/test.csv" --arms full=artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g kd_only=artifacts/control/base_rkl_s0/adapter fed_only=artifacts/federated/florana_kd_noicl_k5_e1_t1_s0/round_1/fedavg_adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($s[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $($s[0])"; break } }
```

GPU 1 — the three reference arms, in parallel:

```powershell
Start-Sleep -Seconds 30; $env:CUDA_VISIBLE_DEVICES='1'; foreach ($s in @(@('SPIDER_REALISTIC','ood_realistic_s0_extra'),@('SPIDER_SYN','ood_syn_s0_extra'),@('SPIDER_DK','ood_dk_s0_extra'))) { Write-Host "=== $($s[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv "processed_data/$($s[0])/test.csv" --arms "base=" seqkd_only=artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s0/round_1/m_g central_ft=artifacts/icl_ladder/qwen1b/ft_no_icl/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($s[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $($s[0])"; break } }
```

The two halves land in separate `eval_arms` run IDs. Joining them is valid:
same test set, same seed, same protocol, so paired tests still work — join the
prediction files on `row_id`.

## C. The operating point — DONE 2026-08-15

Results (`eval_arms__s0__20260815T08{4527,4756,5343,5649}` and
`T13{4454,4951,5953},T140507`):

|                               | Spider dev | REALISTIC |   SYN |    DK | OOD pooled |
| ----------------------------- | ---------: | --------: | ----: | ----: | ---------: |
| `central_ft` (1 epoch)        |      62.19 |     55.31 | 51.06 | 46.92 |      51.04 |
| `central_2ep`                 |  **67.02** |     58.07 | 55.22 | 48.97 |  **54.31** |
| `fed_only` (`E=1` pre-server) |      57.35 |     54.92 | 49.32 | 45.23 |      49.64 |
| `e2_pre_server`               |      61.90 |     55.71 | 51.74 | 46.17 |      51.28 |
| `full` (`E=1` endpoint)       |      63.35 |     52.95 | 49.61 | 47.85 |      49.98 |
| `e2_full`                     |      63.54 |     51.38 | 50.48 | 47.85 |      50.02 |

- The 67.02 ceiling reproduces and **generalises** (`+3.27` pooled OOD over
  `central_ft`, `p<1e−4`), so it is capability rather than Spider overfitting.
  The hoped-for "public pool buys OOD robustness" argument is dead.
- A second local epoch is `+4.55` (`p<1e−4`) pre-server and `+0.19`
  (`p=0.897`) at the endpoint. No FedAvg drift penalty appeared at
  `alpha=0.5, K=5`.
- Its real payoff came later: it is the control proving block D's gain is
  rounds, not extra local training.

Commands below, kept for reproduction.

### The question this block asked

Every arm in the ablation trains for one local epoch. A retained result says
that is far from converged, and it was never noticed because no federated arm
has ever been trained for two.

| Adapter                     | Recipe                                    |        EX |
| --------------------------- | ----------------------------------------- | --------: |
| `ft_no_icl`                 | 1 epoch Spider from base, 8,659 steps     |     62.19 |
| `central_ft_then_spider_ft` | `ft_no_icl` plus a second identical epoch | **67.02** |

Verified lineage: the second run's `init_adapter` is `ft_no_icl`, same
`train.csv`, same `lr=2e-4`. One extra pass over the same data is worth
**+4.83 EX** — larger than every effect the ablation is arguing about.

Two things this does and does not mean:

- It does **not** invalidate the compute-matched comparison. Federated
  `T=1, E=1` spends 8,659 client examples, exactly one pass over the union, so
  62.19 remains the correct matched baseline and the report's `+1.16` stands.
- It does mean the *ceiling* row is wrong. The report calls 62.19 a "reference
  ceiling in terms of data access", but anyone holding all the data would train
  to convergence, so the ceiling is 67.02. Both numbers belong in the paper
  under different labels: 62.19 the compute-matched baseline, 67.02 the
  data-access ceiling.
- The real risk is external validity. Arm rankings measured at an undertrained
  point need not hold at convergence.

One hypothesis is already weakened: each client runs its own cosine schedule
(`lora_trainer.py`, `get_cosine_schedule_with_warmup`), so the federated branch
*already* performs five LR restarts per round and still only reaches 57.35.
The `+4.83` is therefore more likely the value of a second data pass than an
LR-restart artefact — which raises the chance that `E=2` helps federated too.
Working against that: raising local epochs under non-IID is the classic FedAvg
drift trade, so the gain may shrink or reverse after aggregation. Either
direction is a reportable FL result.

This block runs before D. If `E=2` moves the endpoint materially, rounds
measured at `E=1` are measuring the wrong operating point.

### C1. The ceiling, off-distribution too (~20 min, no training)

The 67.02 comes from an eval pruned in the 2026-08-15 audit; the adapter
survives. Re-score it under the current protocol on Spider dev and the three OOD
sets. `central_ft` (one epoch) already has the best pooled OOD score, so whether
a second Spider epoch keeps generalising or overfits to Spider decides how the
public pool is argued for.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; foreach ($s in @(@('processed_data/SPIDER/centralized/test.csv','ceiling_spider_s0'),@('processed_data/SPIDER_REALISTIC/test.csv','ceiling_realistic_s0'),@('processed_data/SPIDER_SYN/test.csv','ceiling_syn_s0'),@('processed_data/SPIDER_DK/test.csv','ceiling_dk_s0'))) { Write-Host "=== $($s[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $s[0] --arms central_2ep=artifacts/probe_p/central_ft_then_spider_ft/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($s[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $($s[0])"; break } }
```

### C2. Two local epochs, `T=1`, seed 0 (~3.3 h)

Everything else identical to the `E=1` run. This is also the control that
separates "more communication rounds" from "more local training" in block D:
`T=2, E=1` confounds the two, `T=1, E=2` does not.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedkd --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 2 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out artifacts/federated/fedkd_noicl_k5_e2_t1_s0 --seed 0
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms e2_pre_server=artifacts/federated/fedkd_noicl_k5_e2_t1_s0/round_1/fedavg_adapter e2_full=artifacts/federated/fedkd_noicl_k5_e2_t1_s0/round_1/m_g --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_noicl_k5_e2_t1_s0/eval_k0 --skip-completed
```

Read `e2_pre_server` against 57.35 — does a second local epoch survive FedAvg
under non-IID — and `e2_full` against 63.35 — does the endpoint move, or does
distillation compress it back to about 62.7 as it has done to everything else.
If the endpoint moves, re-score both on the three OOD sets before anything else.

## D. Rounds 2 and 3 on seed 0 — DONE 2026-08-16

`eval_arms__s0__20260816T034740`, `k=0`, `dail_weighted`, `n=1034`.

| Round | pre-server |  endpoint |
| ----- | ---------: | --------: |
| `T=1` |      57.35 |     63.35 |
| `T=2` |      64.02 |     66.15 |
| `T=3` |  **66.05** | **69.54** |

| Contrast                             |                     Δ |                    `p` |
| ------------------------------------ | --------------------: | ---------------------: |
| pre-server `T=1→2` / `T=2→3`         |         +6.67 / +2.03 |          <1e−4 / 0.046 |
| endpoint `T=1→2` / `T=2→3`           |         +2.80 / +3.38 |        0.0019 / 0.0002 |
| endpoint `T=1→3`                     |             **+6.19** |                  <1e−4 |
| server step at `T=1` / `T=2` / `T=3` | +6.00 / +2.13 / +3.48 | <1e−4 / 0.123 / 0.0078 |

Both curves rise, every round-to-round step is significant, and the server step
keeps contributing. **Matched on local work** — two passes over each client's
data either way — `T=2, E=1` beats `T=1, E=2` by `+2.61` (`p=0.0067`) at the
endpoint and `+2.13` (`p=0.059`) pre-server, so the gain is repeated
communication rounds and not longer local training. Block C earned its cost
here.

Against centralized: `T=2` beats the 1-epoch reference by `+3.97` (`p=0.0058`)
and ties `central_2ep` (`−0.87`, `p=0.552`) at matched passes. `T=3` is `+2.51`
over `central_2ep` (`p=0.055`) but is **not budget-matched** — see block G.

**Protocol warning.** The first attempt (`eval_arms__s0__20260816T015558`,
deleted) silently ran at `k=3` with `dail_select` and `batch_size 1`. A
PowerShell one-liner used `$T` for the flag array and `$t` for a loop variable;
PowerShell variable names are case-insensitive, so `$T` resolved to the integer
`3`, argparse fell back to every default, and a stray arm named `3` appeared.
Always check `config.json` for `k`, `retrieval`, and `batch_size` before
trusting an eval.

Commands below, kept for reproduction.

### The question this block asked

The strategic run. If the federated stage's margin over distillation-alone
grows with rounds, that is a stronger contribution than anything else on the
table; if it stays flat, that has to be known before §3 is written.

Use `round`, not `run`: `run` has no `--client-out` and would not recognise
seed 0's round 1, whose client stage lives in the shared
`florana_kd_noicl_k5_e1_t1_s0/round_1` directory. `round` validates lineage
against `<out>/manifest.json` and fails loudly if the supplied init adapter is
not the previous round's M_G.

The `_t1_` in the directory name becomes a misnomer at `T=3`. Do not rename it —
the manifest records these paths and the lineage check reads them.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedkd --round 2 --init-adapter artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_1/m_g --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out artifacts/federated/fedkd_noicl_k5_e1_t1_s0 --seed 0
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedkd --round 3 --init-adapter artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_2/m_g --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out artifacts/federated/fedkd_noicl_k5_e1_t1_s0 --seed 0
```

```powershell
uv run python -c "from fedicl_sql.runtime.manifest import resolve_m_g; print([resolve_m_g('artifacts/federated/fedkd_noicl_k5_e1_t1_s0', t) for t in (1,2,3)])"
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms fedkd_t2_preserver=artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_2/fedavg_adapter fedkd_t2=artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_2/m_g fedkd_t3_preserver=artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/fedavg_adapter fedkd_t3=artifacts/federated/fedkd_noicl_k5_e1_t1_s0/round_3/m_g --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fedkd_noicl_k5_e1_t3_s0/eval_k0 --skip-completed
```

Evaluate the pre-server adapter of every round, not only `m_g`. It costs one
extra arm and it is the artifact that answers "what if we federate several
times and distil once": round `t`'s `fedavg_adapter` *is* the pipeline with `t`
federated passes and `t−1` server steps. Check `round_2/` actually contains
`fedavg_adapter` before running the eval — in round 1 the aggregation was
written into the shared client directory because `--client-out` was set.

The figure this produces is two curves over `t = 1,2,3`: `fedavg_adapter(t)`
pre-server and `m_g(t)` post-server. Three outcomes, all reportable:

- both rise — federation compounds, extend to `T=5` and then add seeds;
- pre-server rises, endpoint flat — distillation is a fixed-point attractor.
  That is a genuine finding and it bounds the method; it would also explain why
  the federated row is only worth `+1.39`;
- both flat — `T=1` is enough, say so and spend the compute on seeds.

Prior from the data already collected: expect small. `kdfirst` showed client
training on an already-distilled model adds `+0.38`, and every seed shows the
server step pulling different starting points to roughly the same endpoint.

Read against `T=1` at 63.35 for this seed, and against the distillation-only
control at 61.22.

## E. Seeds 3-6 on the ladder (~16 h) — optional, probably skip

The proposal has two components, federated training and distillation, and the
ablation removes one at a time. SeqKD and reverse KL are both distillation —
hard labels and soft labels inside the same component — so which of them wins
is a design choice, not a component, and it does not need its own claim. The
reverse-KL argument comes from [10] KID; the `+1.71 ± 1.38` measured at `n=3`
is reported as-is and nothing rests on it.

That removes the reason this block was queued. Run it only if C and D are done
and GPU time is otherwise idle, to tighten the `−4.55` distillation row.

One caveat added 2026-08-15: block B found the distillation row collapsing
off-distribution (`+0.34` pooled), so tightening it on Spider dev alone is worth
less than it was. If these seeds run, evaluate them on the OOD sets too.

Four times, with the seed and every `_s3` path substituted:

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedavg --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out artifacts/federated/fedavg_noicl_k5_e1_t1_s3 --seed 3
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedavg_pub --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out artifacts/federated/fedavg_noicl_k5_e1_t1_s3/round_1 --out artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s3 --seed 3
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/federated/run.py round --arm fedkd --round 1 --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --client-out artifacts/federated/fedavg_noicl_k5_e1_t1_s3/round_1 --out artifacts/federated/fedkd_noicl_k5_e1_t1_s3 --seed 3
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms s3_fedavg_pre_server=artifacts/federated/fedavg_noicl_k5_e1_t1_s3/round_1/fedavg_adapter s3_fedavg_pub=artifacts/federated/fedavg_pub_noicl_k5_e1_t1_s3/round_1/m_g s3_fedavg_kd=artifacts/federated/fedkd_noicl_k5_e1_t1_s3/round_1/m_g --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fed_noicl_k5_e1_t1_s3/eval_k0 --skip-completed
```

## F. `T=4` and `T=5` on seed 0 (~8 h) — RUN THIS NEXT

The endpoint is still climbing at `T=3` (`+3.38`, `p=0.0002`) and nobody knows
where it plateaus. That plateau is the number the paper reports, so it has to be
found before §4 is written. Same command shape as block D; the `_t1_` in the
directory name is already a misnomer and must not be renamed.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/fedkd_noicl_k5_e1_t1_s0'; foreach ($n in 4,5) { $p=$n-1; Write-Host "=== round $n"; uv run python experiments/federated/run.py round --arm fedkd --round $n --init-adapter "$R/round_$p/m_g" --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed 0; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED round $n"; break } }
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/fedkd_noicl_k5_e1_t1_s0'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "fedkd_t4_preserver=$R/round_4/fedavg_adapter" "fedkd_t4=$R/round_4/m_g" "fedkd_t5_preserver=$R/round_5/fedavg_adapter" "fedkd_t5=$R/round_5/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fedkd_noicl_k5_e1_t5_s0/eval_k0 --skip-completed
```

## G. `central_3ep`, the budget-matched ceiling — DONE 2026-08-16

`eval_arms__s0__20260816T20{4913,5209,5930},T210235`.

| Centralized | Spider dev |         Δ |       `p` | OOD pooled |
| ----------- | ---------: | --------: | --------: | ---------: |
| 1 epoch     |      62.19 |         — |         — |      51.04 |
| 2 epochs    |      67.02 |     +4.84 |     <1e−4 |      54.31 |
| 3 epochs    |  **67.60** | **+0.58** | **0.606** |      54.16 |

**Centralized saturates after epoch 2**, on Spider dev and pooled
off-distribution alike (`−0.14`, `p=0.888`). Matched on passes over private
data:

| Passes | federated | centralized |         Δ |   `p` |
| ------ | --------: | ----------: | --------: | ----: |
| 1      |     63.35 |       62.19 |     +1.16 | 0.432 |
| 2      |     66.15 |       67.02 |     −0.87 | 0.552 |
| 3      | **69.54** |       67.60 | **+1.93** | 0.172 |

No cell is individually significant. The result is the **shape**: centralized
runs `+4.84 → +0.58` and stops, federated runs `+2.80 → +3.38` (`p=0.0002`) and
keeps going. Each federated round adds a fresh teacher-distillation pass over
public data; a third centralized epoch only re-reads Spider. `fedkd_t3` also
makes 101 execution errors against `central_3ep`'s 163.

**Compute is not matched and must not be presented as if it were.** `t3` spends
25,977 client steps plus 11,619 server steps against `c3`'s 25,977 — about 45%
more. What is matched is private-data access, the privacy-relevant axis; step
counts belong in a cost column.

If `T=4`/`T=5` land higher, four- and five-epoch centralized adapters are needed
on the same principle — chain them the same way.

Commands below, kept for reproduction.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; uv run python experiments/client_train/run.py --client processed_data/SPIDER/centralized/train.csv --init-adapter artifacts/probe_p/central_ft_then_spider_ft/adapter --out artifacts/probe_p/central_3ep/adapter --kd-direction none --epochs 1 --batch-size 1 --grad-accum 16 --max-len 2560 --train-k 0 --schema-style full --demo-style never_schema --save-steps 200 --seed 0
```

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; foreach ($s in @(@('processed_data/SPIDER/centralized/test.csv','c3ep_spider_s0'),@('processed_data/SPIDER_REALISTIC/test.csv','c3ep_realistic_s0'),@('processed_data/SPIDER_SYN/test.csv','c3ep_syn_s0'),@('processed_data/SPIDER_DK/test.csv','c3ep_dk_s0'))) { Write-Host "=== $($s[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv $s[0] --arms central_3ep=artifacts/probe_p/central_3ep/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($s[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $($s[0])"; break } }
```

The chain matches how 67.02 was produced: a fresh one-epoch run initialised from
the previous adapter, so each epoch gets its own cosine cycle. Do not substitute
`--epochs 3` in a single run — that is one long schedule and a different recipe.

## H. `T=2` and `T=3` off-distribution — DONE 2026-08-17

Reported per dataset, not pooled: the three sets probe different shift types and
pooling hides which one moves.

| Post-server EX   | `T=1` | `T=2` | `T=3` | `T1→T3` |    `p` |
| ---------------- | ----: | ----: | ----: | ------: | -----: |
| Spider dev       | 63.35 | 66.15 | 69.54 |   +6.19 |  <1e-4 |
| Spider-Realistic | 52.95 | 56.30 | 59.65 |   +6.69 |  <1e-4 |
| Spider-Syn       | 49.61 | 52.03 | 55.51 |   +5.90 |  <1e-4 |
| Spider-DK        | 47.85 | 50.47 | 52.71 |   +4.86 | 0.0007 |

**The round result is distribution-independent** — four benchmarks, same
direction, same magnitude, all significant. This is the headline table.

The server step is not:

| Server KD step   |                `T=1` |             `T=2` |                  `T=3` |
| ---------------- | -------------------: | ----------------: | ---------------------: |
| Spider dev       | **+6.00** (`p<1e-4`) | +2.13 (`p=0.123`) | **+3.48** (`p=0.0078`) |
| Spider-Realistic |    -1.97 (`p=0.391`) | -0.79 (`p=0.767`) |      +1.38 (`p=0.538`) |
| Spider-Syn       |    +0.29 (`p=0.887`) | -0.87 (`p=0.546`) |   **0.00** (`p=1.000`) |
| Spider-DK        |    +2.62 (`p=0.130`) | -0.37 (`p=0.910`) |      +1.87 (`p=0.229`) |

Nine off-distribution cells, none significant. Spider-Syn is the sharpest
comparison — `n=1034`, same power as Spider dev — and it returns `+0.29`,
`-0.87`, `0.00`. Realistic and DK are underpowered for ~2 EX, so for those the
phrasing is "no evidence of an effect", not the reverse.

Execution errors go the other way and are unanimous, 12/12 cells reduced
(e.g. Spider dev `17.2% → 9.8%` at `T=3`, Syn `19.6% → 16.4%`). The teacher
teaches executable SQL everywhere; only in distribution does that convert into
correct SQL.

Caveat: the `T=3` pre-server column is not a no-KD arm — those clients started
from `M_G(t=2)`, already distilled twice.

Command kept for reproduction.

Every round conclusion rests on Spider dev, which shares its corpus with the
private client shards. Block B showed a `+6.00` contrast shrinking to `+0.34`
under exactly this test, so the round result has to face it too. Block G made
this the top priority: centralized has saturated, so off-distribution is the
only axis where it still leads (`+4.19` over the `T=1` pipeline, `p=0.0001`).

```powershell
Four arms: the pre-server aggregate and the post-server `M_G` at both `T=2` and
`T=3`. Block B already measured both stages at `T=1` (`fed_only` 49.64,
`full` 49.98), so this completes a 3-rounds × 2-stages grid off-distribution.
About 45 minutes.

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $R='artifacts/federated/fedkd_noicl_k5_e1_t1_s0'; foreach ($ds in @(@('SPIDER_REALISTIC','ood_rounds_realistic_s0'),@('SPIDER_SYN','ood_rounds_syn_s0'),@('SPIDER_DK','ood_rounds_dk_s0'))) { Write-Host "=== $($ds[0])"; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv "processed_data/$($ds[0])/test.csv" --arms "fedkd_t2_preserver=$R/round_2/fedavg_adapter" "fedkd_t2=$R/round_2/m_g" "fedkd_t3_preserver=$R/round_3/fedavg_adapter" "fedkd_t3=$R/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir "artifacts/eval_resume/$($ds[1])/eval_k0" --skip-completed; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED: $($ds[0])"; break } }
```

Three things to read from the completed grid:

- **`fedkd_t3` pooled** against `full` at 49.98 and the centralized plateau at
  54.16–54.31. The `T=1` pipeline lost to `central_3ep` by `4.19` (`p=0.0001`)
  off-distribution; whether three rounds close that gap decides how §4 frames
  the centralized comparison, and whether the story is complete or bounded.
- **`m_g − fedavg_adapter` at each round**, the server step's off-distribution
  value. At `T=1` it was `+0.34` (`p=0.76`). If it grows with rounds the
  distillation component is rescued; if it stays near zero, then
  off-distribution the method is federated training alone and §4 has to say so.
- **The pre-server curve off-distribution**, `49.64 → ? → ?`. Does federation
  compound away from its home corpus, or only on it.

## J. BIRD cross-corpus transfer — DONE 2026-08-18

BIRD dev, `n=1534`, `k=0`, greedy (`eval_arms__s0__20260818T140415`). Enters as
a **cross-corpus transfer** row, never a headline benchmark: its 11 dev
databases are disjoint from the pool's 69 (no schema leakage), but the corpus is
the one the teacher was distilled on, so it favours the pipeline exactly as the
Spider-derived sets favour a Spider-trained model. Absolute EX is low because
`build_prompt` never renders BIRD's `evidence` hint — all arms equally, so
within-table comparisons hold, but these numbers must not meet a BIRD
leaderboard.

| Arm                   |        EX | Exec-error |
| --------------------- | --------: | ---------: |
| base                  |     10.89 |      46.5% |
| `T=1` pre-server      |     11.15 |      55.3% |
| centralized 1 epoch   |     11.34 |      48.9% |
| centralized 3 epochs  |     12.91 |      42.6% |
| `T=3` pre-server      |     17.67 |      37.9% |
| `T=1` post-server     |     19.43 |      33.4% |
| **`T=3` post-server** | **21.58** |  **29.9%** |

- Server step `+8.28` at `T=1` (`p=2.8e-20`) and `+3.91` at `T=3`
  (`p=6.1e-07`). KD's EX gain *does* transfer, within its own corpus.
- Federation alone is `+0.26` (`p=0.82`). `t3_pre − fed_only = +6.52` is not the
  federated contribution — `t3_pre` carries two prior distillation stages.
- Centralized is `+0.46` (ns) at one epoch and `+2.02` (`p=0.029`) at three.
  `T=3` beats `central_3ep` by `+8.67` (`p=4.3e-20`).

**The headline finding:** the components are orthogonal. Rounds carry the Spider
variants and do nothing on BIRD; the server step carries BIRD and does nothing
on the Spider variants. Spider dev alone cannot separate them because both work
there.

Note the asymmetry when writing this up: on the Spider variants centralized
leads by 1–4 EX; on BIRD the pipeline leads by 8.67.

Commands, split so the decisive arms land first (BIRD execution is far slower
than Spider — large databases, two queries scored per row, 60 s ceiling each):

```powershell
$env:CUDA_VISIBLE_DEVICES='0'; $F='artifacts/federated'; uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/BIRD/centralized/train.csv --test-csv processed_data/BIRD/centralized/test.csv --arms "t3_pre=$F/fedkd_noicl_k5_e1_t1_s0/round_3/fedavg_adapter" "t3_post=$F/fedkd_noicl_k5_e1_t1_s0/round_3/m_g" central_3ep=artifacts/probe_p/central_3ep/adapter --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/bird_transfer_s0/eval_k0 --skip-completed
```

## I. Seeds 1 and 2, rounds 2 and 3 (~8 h per seed) — run in parallel with F

Round 1 already exists for both seeds
(`artifacts/federated/fedkd_noicl_k5_e1_t1_s{1,2}/round_1/m_g`), so only rounds
2 and 3 are needed. Runs on the second GPU alongside block F.

```powershell
$env:CUDA_VISIBLE_DEVICES='1'; Start-Sleep -Seconds 45; $R='artifacts/federated/fedkd_noicl_k5_e1_t1_s1'; foreach ($n in 2,3) { $p=$n-1; Write-Host "=== s1 round $n $(Get-Date -Format 'HH:mm:ss')"; uv run python experiments/federated/run.py round --arm fedkd --round $n --init-adapter "$R/round_$p/m_g" --split-dir processed_data/SPIDER/federated_noniid/alpha_0.5/k5 --n-clients 5 --local-epochs 1 --client-train-k 0 --pool processed_data/BIRD/bootstrap_full_exmatch/train.csv --pool-size 0 --distill-steps 0 --k-teacher 0 --teacher-model Qwen/Qwen2.5-Coder-7B-Instruct --teacher-4bit --teacher-logit-cache artifacts/teacher_logit_cache/rkd_k0_full --batch-size 1 --grad-accum 16 --max-len 2560 --save-steps 200 --out $R --seed 1; if ($LASTEXITCODE -ne 0) { Write-Host "FAILED s1 round $n"; break } }; if ($LASTEXITCODE -eq 0) { uv run python experiments/eval_arms/run.py --pool-mode centralized --centralized-train processed_data/SPIDER/centralized/train.csv --test-csv processed_data/SPIDER/centralized/test.csv --arms "s1_t2_preserver=$R/round_2/fedavg_adapter" "s1_t2=$R/round_2/m_g" "s1_t3_preserver=$R/round_3/fedavg_adapter" "s1_t3=$R/round_3/m_g" --n-eval 0 --k 0 --schema-style full --demo-style never_schema --retrieval dail_weighted --embedder BAAI/bge-small-en-v1.5 --tau 0.85 --dail-alpha 0.6 --dail-shortlist 32 --overlay none --batch-size 16 --seed 0 --resume-dir artifacts/eval_resume/fedkd_noicl_k5_e1_t3_s1/eval_k0 --skip-completed }
```

Seed 2 is the same with `s1`→`s2` and `--seed 2`.

## Do not run

- Anything ICL. It is out of the method and out of the paper; the existing
  runs are the evidence for that decision and no new cell is needed.
- FLoRA-NA, or any aggregator targeting LoRA aggregation error. Exact
  aggregation bounded the whole family at this configuration.
- A matched-compute control for the base arm. An ablation removes a component
  together with its compute, and extra epochs over the same 3,873 public rows
  would measure repeated-data returns, not the value of private data.
