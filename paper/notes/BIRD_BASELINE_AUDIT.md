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

These are recorded results pending the audit below. The error column includes
gold/environment failures and must not be interpreted solely as invalid model SQL.
The centralized-versus-FL contrast also differs in epoch/round budgets; it does
not isolate aggregation alone. Base-to-SFT improvement does not isolate evidence.

## Checks already made

- All six prediction files cover 1,534 dev rows; 1,386 rendered prompts contain
  evidence, matching populated dev evidence. Maximum recorded prompt: 2,264 tokens.
- Training uses `bird_with_evidence`; E2 is one continuous 2-epoch invocation.
- The scorer dispatches to set-of-row-tuples equality for BIRD.
- Train assembly keeps the SQL target and left-trims the prompt at 2,560 tokens.
  Evidence precedes schema, so its retention must be checked on actual tokens.
- E2 has 17 rows containing `database or disk is full` and 11 containing
  `gold SQL failed`; these groups overlap. Full independent CPU rescore is pending.

## Acceptance work

`scripts/run_bird_baseline_audit.ps1` performs:

Implementation: nested `0bf1ef0`. Relevant tests: 42 passed; actual cached Qwen
tokenizer retention smoke passed locally. Full data audit awaits the server's
BIRD SQLite files; PowerShell runtime is unavailable on this local machine.

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

No production training policy changes until measured retention is available.
If evidence or required schema was lost, choose a context budget or schema
strategy that preserves the required input and use new checkpoint roots. If
retention passes, existing checkpoints can be kept and scoring addressed alone.

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
