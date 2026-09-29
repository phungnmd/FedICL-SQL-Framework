# BIRD baseline acceptance — P2.1 CPU audit

The target is a correctly specified BIRD-with-evidence baseline. Evidence is an
input contract; its causal benefit is not an experiment in the active queue.

## Fixed setup and observed results

P2.1 uses Qwen2.5-1.5B-Instruct (not Coder), original BIRD 9,428 train / 1,534
development rows, full schema, provided evidence, LoRA CE and greedy generation.
The filename `test.csv` denotes BIRD **dev**, not the hidden official test set.
Result commit: nested `f99febd`.

| Arm | Recorded EX (%) | Correct / 1,534 | Execution-error field nonempty |
|---|---:|---:|---:|
| Base | 15.97 | 245 | 874 |
| Centralized E1 | 31.55 | 484 | 410 |
| Centralized E2 | 35.07 | 538 | 349 |
| Pure FL T1 | 22.56 | 346 | 626 |
| Pure FL T2 | 27.31 | 419 | 540 |
| Pure FL T3 | 29.99 | 460 | 461 |

These are retained diagnostic results, not canonical baselines. The completed
audit found that their training contract silently truncated required inputs.
The error column includes gold/environment failures and must not be interpreted solely as invalid model SQL.
The centralized-versus-FL contrast also differs in epoch/round budgets; it does
not isolate aggregation alone. Base-to-SFT improvement does not isolate evidence.

## Completed audit (`e9bde43`)

- All six prediction files cover 1,534 dev rows; 1,386 rendered prompts contain
  evidence, matching populated dev evidence. Maximum recorded prompt: 2,264 tokens.
- Training uses `bird_with_evidence`; E2 is one continuous 2-epoch invocation.
- The scorer dispatches to set-of-row-tuples equality for BIRD.
- Of 9,428 train rows, 974 prompts were truncated and 754 lost every evidence
  token. No row became target-only; maximum untruncated prompt length was 6,779
  tokens. The 2,560-token Spider-tuned budget is therefore invalid for this
  BIRD-full-schema contract.
- Independent read-only rescore was stable: five arms were identical and
  centralized E1 changed by one row (31.55 to 31.62 EX). No `disk full` event
  recurred. Dev gold was executable for 1,532/1,534 rows; two timed out at 60 s.
- The scoring implementation is accepted. The P2.1 checkpoints are rejected as
  canonical BIRD baselines because their training input was incomplete.

## Repair contract

Nested commit `d21f777` adds the corrective contract:

- `max_len=7168`, above the measured 6,865-token maximum assembled
  prompt-plus-target sequence;
- `truncation_policy=error`, fingerprinted in centralized checkpoints and the
  federated setup, so any remaining overflow aborts before optimization;
- non-reentrant gradient checkpointing and `use_cache=False` to make the longer
  context viable on the single 24 GiB GPU;
- a deterministic eight-row smoke drawn from the longest audited prompts before
  any full retraining;
- new immutable `bird_original_ctx7168` roots. Old P2.1 roots are never reused.

The official BIRD fine-tuning example uses `max_length=18000` and gradient
checkpointing. Our 7,168 budget is dataset-measured for the frozen Qwen 1.5B,
full-schema, no-demo contract rather than copied from a different 3B/FSDP setup.

`scripts/run_bird_baseline_audit.ps1` performed:

Implementation: nested `0bf1ef0`; completed artifacts: nested `e9bde43`.

1. Hash source CSVs, saved predictions, tokenizer, prompt implementation and
   current SQLite databases; reject a changed contract on resume.
2. Reconstruct every train input through the actual chat template and `_assemble`;
   report lost prompt/evidence tokens and target-only rows.
3. Execute every dev gold independently of model predictions.
4. Rescore all six prediction files, checking row/question/gold identity and
   provided evidence before execution. Retain raw SQL and the full denominator.
5. Report changed EX, separate gold/prediction errors, timeouts and disk failures.

Scoring follows the raw-SQL comparison in the upstream
[EX evaluator](https://github.com/bird-bench/mini_dev/blob/main/evaluation/evaluation_ex.py)
and [SQLite executor](https://github.com/bird-bench/mini_dev/blob/main/evaluation/evaluation_utils.py).
This is an independent implementation, not an invocation of upstream scripts:
read-only SQLite, one spawned process per pair, and a declared 60-second pair
deadline including startup. Upstream mini-dev defaults to 30 seconds and uses
`func_timeout`; the original project allowed 60 seconds per individual query.
Any changed scores therefore need row-level review for SQL normalization,
timeout and resource differences. Never silently overwrite old scores.

SQLite scratch files use the audit output volume. The audit pauses below 5 GiB
free; this is a minimum check, not a guarantee that large joins fit. Remaining
resource failures require another explicit rescore root after remediation.

Do not promote the original P2.1 accuracy values into paper tables. Run the
long-context smoke, then regenerate centralized and FL checkpoints/evaluation
under the corrected immutable roots.

## Literature context

[SLM-SQL Table 2](https://arxiv.org/html/2507.22478v1) reports 28.40 EX for
Qwen2.5-Coder-1.5B and 67.08 for its complete system. The latter uses large
synthetic training corpora, RL and corrective self-consistency, so neither number
is a matched baseline for our general-purpose Instruct model and 2-epoch LoRA.
[Feather-SQL](https://aclanthology.org/2025.findings-ijcnlp.130.pdf) also changes
schema processing and inference budget. Parameter count alone cannot establish
baseline equivalence or validate our pipeline.

The primary method direction remains **Spider private FL → BIRD public KD →
Spider dev evaluation**. P2.1 BIRD-private baselines support protocol validation
and the later reverse-direction experiment. Final KD/federated choices remain open.
