# FedLS-SQL: run queue

## Status

Updated 2026-11-17 at 10:10 (Asia/Ho_Chi_Minh). Last published result:
`a428e174` (09:45 on 2026-11-17: the SFT round with the verified synthetic
rows on Spider test, 74.15). Queue: `f6635e89` (pushed 09:18 on 2026-11-17: row 3a added, the
queue file only). `08254bcf` (02:57) added rows 5b and 13 and changed code the DPO rounds load
(`fedicl_sql/federated/pref_rounds.py`, `fedicl_sql/preference/pairs.py`,
`experiments/federated_pref/run.py`): a new option, off by default, and
setups without it keep their identity and pair counts (tests). The worker pulled it before row 3; rows 3, 5, 7 and 9 run with the new
code. Server work uses drive D only (owner,
2026-11-15): every command below sets `TEMP` and `TMP` to
`D:\phungthan\fediclkd\tmp`.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker in row 4, `synvc_s0/sft_plain` (the same FedAvg SFT round on the own rows alone). Inferred: rows 3 and 3a are published and nothing has been published since 09:45. | results commit `a428e174`, 09:45 on 2026-11-17 |
| 1 | Not ours: in use by another user. No worker or job to start. | owner, 2026-11-09 |

Read-only status on the server, from the `fedicl-sql` root:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.curve status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

## Run now

Nothing to run; do not press Ctrl+C.

Next moments the owner is needed (clock times are estimates):

- If no result commit arrives by about 12:45: run the status command above
  and send its output.
- During row 5 (about 13:00): the first lines of `srvx_s0/bird_round`
  (`first batch ... peak reserved` of the sampling and of the first
  training updates). It is the first DPO training on BIRD-length rows;
  send them back.
- After row 5 (about 17:30): rows 4 and 5 are read with the finished rows for the three
  directions (`RESEARCH_STATE.md`, section 3).
- Row 5b, minutes after row 5: the line of `srvt_s0/pairs` that starts
  `chosen side of the pairs: teacher ...`. Send it back. It tells how many
  pairs take the teacher's SQL, and so whether row 13 is worth its 4 h.
- After row 6 (about 00:00 on 2026-11-18): the server stage in the final
  setup.
- Any `STOP queue` line: send it back at once.

## Running and queued

GPU 0 in queue order. Durations are estimates. Every row decodes without
the repetition penalty (`--repetition-penalty 1.0`); every row before
2026-11-16 19:33 was decoded with 1.1.

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 4 | `synvc_s0/sft_plain`, `eval_plain` and their publish tasks | The same round on the clients' rows alone. Arm `sqlcodes_sft_x1_np_vllm_inproc` | 2.5 h, about 2 h left | running. Comparator: the round with the synthetic rows, 74.15 |
| 5 | `srvx_s0/check_bird`, `eval_stage`, `bird_round`, `eval_bird_round` and their publish tasks | Direction 2: does the clients' execution-preference round also work at the server on the public databases, after the teacher stage? From the seed 0 Hinton server stage: one DPO + NLL round on 3,000 BIRD train questions (one pooled client, `full` prompts as the stage was trained), then the round's adapter against the stage's adapter on Spider test and BIRD dev, no client training. Arms `srvdpo_hinton_q3000_r1_np_vllm_inproc`, `sql_hinton_k2_np_vllm_inproc` | 4.7 h | queued |
| 5b | `srvt_s0/samples`, `pairs`, `publish_pairs` | The teacher inside the round of row 5, the count first (CPU, no training): the samples of row 5 are copied, the teacher's stored SQL of every question with no correct sample is executed, and the pairs are built with the teacher's SQL as the chosen side where it returns the gold result (gold SQL otherwise). Read: the number of pairs whose chosen side is the teacher's SQL | 5 min | queued |
| 6 | `sqlcv2_s0/curve_hinton_sft` | Stage 1 in the final setup: 3 FedAvg SFT rounds with `codes_v2` from the seed 0 Hinton server stage (existing adapter, trained with `full` prompts), each round on Spider test. Arms `sqlcv2_hinton_k2aaa_a{1,2,3}_np_vllm_inproc`. Comparator: the base-model rounds, 72.05 / 74.57 / 74.85 | 6.5 h | queued |
| 7 | `sqlcv2_s0/curve_fedavg` | Stage 3 in the final setup without stage 1: 3 DPO + NLL rounds from FedAvg R3 with `codes_v2` (74.85). Comparators on that adapter with no training: greedy kept when it executes, else a sample, 77.78; vote over 8 samples, 78.90 | 9 h | queued |
| 8 | `vote_s0/xsel_dpo_r3` and its publish task | Selection by execution over 8 samples of DPO round 3 of row 7 on Spider test: the vote and pass@8 | 0.25 h | queued |
| 9 | `sqlcv2_s0/curve_hinton` | The method in the final setup: 3 DPO + NLL rounds from the R3 of row 6. Arms `sqlcv2_dpo_hinton_r{1,2,3}_np_vllm_inproc`. Comparator: row 7 | 9 h | queued |
| 10 | `vote_s0/xsel_hinton_dpo_r3` and its publish task | The method with selection at inference: 8 samples of DPO round 3 of row 9 | 0.25 h | queued |
| 11 | `sqlcv2_s0/central_e3`, `eval_central`, `publish_central` | How far FedAvg SFT is from training on the pooled rows: centralized SFT on the 8,659 Spider train rows, 3 epochs, `codes_v2`, then epoch 3 on Spider test. Comparator: FedAvg R3, 74.85 | 7 h | queued |
| 12 | `f1v2_s0/curve_fedavg_sft` | Does FedAvg hold with 20 clients? 3 FedAvg SFT rounds on the `k20` split with `codes_v2`, each round on Spider test. Comparator: the rounds with 5 clients, 72.05 / 74.57 / 74.85 | 6.5 h | queued |
| 13 | `srvt_s0/bird_round`, `eval_bird_round` and their publish tasks | Does the teacher add to the server round when it supplies the preferred SQL? The round of row 5 on the pairs of row 5b (same start adapter, questions, samples and settings; only the chosen side of the teacher's pairs differs), then its adapter on Spider test and BIRD dev. Arm `srvdpo_hinton_q3000_teacher_r1_np_vllm_inproc`. Comparators: the two arms of row 5 | 4 h | queued, after every other row; taken out if row 5b counts few teacher pairs or row 5 shows no gain |

Rows 4-12 take about 45.5 h from now, row 13 about 4 h more: rows 4-5 (the
reads for directions 2 and 3) end at about 17:30 on 2026-11-17, row 6 at
about 00:00 on 2026-11-18, row 10 at about 18:30 on 2026-11-18, row 12 at
about 08:00 on 2026-11-19. Row 5 runs a code path that has not run on the
server (a DPO round on BIRD); its time is not measured.

Cut from a full run:

- Every row is seed 0.
- Row 5 uses 3,000 of the 9,428 BIRD train questions and one round (the
  full round was estimated at about 12 h). It has no teacher in the round:
  BIRD has gold SQL. A gain answers whether the round transfers; its size
  with every row is not read here.
- Rows 5b and 13 put the teacher in that round on the same 3,000
  questions. The teacher's SQL is its stored greedy output (1,718 of the
  3,000 match gold by the earlier label); it is used only for questions
  with no correct sample, and those are few after a stage trained on the
  same BIRD rows. Both chosen sides are correct SQL (the teacher's or the
  gold), so the two rounds can come out equal. Not read: the round from
  the base model in place of the logit stage, and public questions without
  gold SQL, where the teacher's SQL would be the only label.
- Rows 6 and 9 start from the server stage trained with `full` prompts; a
  stage retrained with `codes_v2` prompts (new teacher logits on BIRD and
  about 7 h of training) is not queued.
- Row 4 and the finished round with the synthetic rows are a short form of verification-based synthesis (SPFT-SQL,
  arXiv 2509.03937). Cut: the questions come from the base model, not from
  a SQL-to-text model trained by the clients; one iteration; one round
  from FedAvg R3 instead of 3 rounds from the base model. They use `codes`
  prompts, the line whose comparators exist. Row 3 takes more updates than
  row 4. A gain in row 3 over row 4 answers the question; no gain does not
  rule out the full form.
- The synthetic SQL keeps the structures of the client's own queries
  (58.6% one table). Synthesis with a share per number of tables, or with
  structures from public data, is not built.
- Row 11 is centralized SFT only; centralized DPO and the centralized
  pipeline (about 9 h and more) are not queued.
- Row 12 is the FedAvg SFT half with 20 clients; the DPO rounds with 20
  clients (about 11 h) are not queued.

Not queued yet:

- For the paper's table once rows 6 to 10 are read: seed 1 of the final
  lines, the baselines with `codes_v2` (FedProx, FedNTD), the server stage
  with gold SQL only (the teacher's own part), FedAvg with six SFT rounds,
  the six evaluation sets.
- The synthetic-row read on the `codes_v2` line (`synv_s0`, about 6.4 h):
  only if rows 3-4 show a gain.
- The public 1.5B checkpoint trained on SynSQL
  (`cycloneboy/SLM-SQL-Base-1.5B`, licence CC BY-NC 4.0) on Spider test, as
  a first read of public synthetic data at the server. It needs its own
  prompt and parser. Not approved.
- A second non-IID split (about 21 h) and a second student model (about
  15-20 h): after the method's rows.
- Out of the queue since 2026-11-17: the check of result-vote labels
  against gold labels, the peer adapter check, the DPO round on synthetic
  rows from DPO round 3, the 20-client rounds with `codes` prompts.

## Reference

### Restart the worker

All commands run from the `fedicl-sql` root on the server and put temp
files on drive D (`TEMP`, `TMP`, pytest `--basetemp`); drive C is not used.
Ctrl+C stops the
worker and its running task; the start command continues where it stopped
and skips finished work. A failed task stops the worker with
`STOP queue: <task> failed: <last error line>` and the log path; rerunning
retries it. If a task fails again with `CUDA error: unspecified launch
failure`, send the last lines of its log to the agent before a third try.

For a future code update, stop the worker and its child process before
pulling shared DPO changes, then pull and run the tests:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest" tests/test_task_queue.py tests/test_dpo.py tests/test_reuse_samples.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py tests/test_train_length_probe.py tests/test_curve.py tests/test_compare_predictions.py tests/test_eval_arms_config.py tests/test_exec_select.py tests/test_preference_labels.py tests/test_synthesis.py tests/test_peer_check.py tests/test_synth_verify.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
```

Worker on GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

Worker on GPU 1 (not now: the card is in use by another user):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

Worker check, about 1 min, once per server setup (`selftest` phase; with two
cards run it on both, each prints its own card and sleeps 30 s):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0 --phase selftest; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

### The queue and the worker

GPU work on the server runs through one queue file,
`fedicl-sql/queues/active.toml`: every task (one command), what it needs
first, in priority order. One worker per GPU takes the first ready task.
Conventions: `AGENTS.md` ("Defaults") and `CONVENTION.MD` section 5.

Without `--phase` a worker runs the full queue; add `--phase <name>` to run
one phase, or to `status` to see one phase. A worker rereads the queue
before every task, so tasks pushed later run after a pull without a restart.
It prints `start` / `end` per task, the task's own progress lines prefixed
`[gpu0 <task>]`, and a final `DONE queue` line. Per-task logs:
`.queue_state/logs/`. Each group of tasks ends with a `publish` task that
commits and pushes its results.

Evaluations print `first batch ... peak reserved`, then a line a minute with
EX, EM and execution errors so far; sampling prints sample accuracy and
pass@8 so far. Numbers above 21.5 GiB show in red on the console. Shared GPU
memory of each task's process stays near zero.

### The server preference round (phases `srvx_s0`, `srvt_s0`)

One pooled "client" at the server holds BIRD train
(`experiments/federated_pref/run.py round --pooled --n-clients 1`); 3,000
questions drawn by seed and round, `full` prompts with evidence, samples
without the penalty. Roots under
`artifacts/protocol_v2/srvdpo_coder15b_alpha01_s0/`: `hinton_q3000` (gold
SQL as the chosen side of a question with no correct sample) and
`hinton_q3000_teacher` (`--fallback teacher --fallback-targets <csv>`: the
teacher's SQL when it returns the gold result under the round's
evaluator, gold otherwise; `fedicl_sql/federated/teacher_fallback.py`).
The teacher's file is
`processed_data/.../teacher_targets/qwen7b_to_qwen15b_evidence_s0/raw/train.csv`
(committed). `run.py pairs` runs the pair step alone; its counts are in
`audits/.../hinton_q3000_teacher/dpo/round_1/client_1_pairs_stats.json`
(`pairs_chosen_teacher`, `questions_unsolved`,
`questions_unsolved_teacher_correct`).

### The lines (phase `sqldpo_s0`)

Spider numbers are Spider test (2,147 rows), one seed (seed 0), evaluated
through vLLM (`--vllm-determinism inproc`). Choices are made on Spider test,
so its numbers are reported as "chosen on Spider test", never as held-out.

| Line (curve) | Start | Data | Pairs | Step |
|---|---|---|---|---|
| `sqldpo_s0/hinton`, `hinton_more` | `hinton_k2aaa_a3` (Hinton KD on BIRD 2 epochs, then FedAvg 3 rounds) | every client question each round, 8 SQL samples through vLLM (256 new tokens) | correct and wrong samples by execution on the client's databases; gold SQL as chosen when none is correct | one federated DPO + NLL round (beta 0.1, lr 1e-5, 2 local epochs, 16 pairs per update, several pairs per forward pass, gradient checkpointing); 4 rounds run, reported at round 3 |
| `sqldpo_s0/fedavg`, `fedavg_more` | FedAvg R3 from the base model | same | same | the control without a server stage; 3 rounds |
| `sqldpo_s0/gold` | `gold_k2aaa_a3` (gold SFT on BIRD 2 epochs, then FedAvg 3 rounds) | same | same | the control without the teacher; 3 rounds |
| `sqldpo_s0/virtual` (finished, 3 rounds) | `virtual_k2aaa_a3` (the Hinton loss on BIRD 2 epochs with a virtual teacher: gold token 0.73, the rest uniform; then FedAvg 3 rounds; earlier adapter, approved 2026-11-13) | same | same | the control with soft targets and no teacher; 3 rounds |
| `sqldpo_s0/rft_hinton` | `hinton_k2aaa_a3` | the round 1 samples of the Hinton line | the same pairs, chosen side only (preference weight 0) | 1 round, same schedule and updates as DPO round 1 |
| `sqldpo_s0/fdpo_hinton` (finished, 1 round) | `hinton_k2aaa_a3` | the round 1 samples of the Hinton line | the same pairs; the preference term weights the tokens where chosen and rejected differ by 2 and leaves out the rejected suffix | 1 round, same schedule and updates as DPO round 1 |
| `sqldpo_s0/pairrand_hinton` (finished, 1 round) | `hinton_k2aaa_a3` | the round 1 samples of the Hinton line | the same labels and pair count; which correct and wrong sample pair up first is random (a fixed hash) instead of the most similar two | 1 round, same schedule and updates as DPO round 1 |
| `sqldpo_s0/nonll_hinton` (finished, 1 round), `nonll_hinton_more` (finished, rounds 2-3) | `hinton_k2aaa_a3` | round 1: the round 1 samples of the Hinton line; rounds 2-3: its own samples | the same pair rule (nearest) | the preference term only (NLL weight 0), otherwise the Hinton line's round; 3 rounds |
| `sqldpo_s0/nogold_hinton` (finished, 1 round) | `hinton_k2aaa_a3` | the round 1 samples of the Hinton line | the same rule without the gold fallback: a question with no correct sample gives no pair | 1 round, same schedule as DPO round 1 |
| `sqldpo_s0/central_hinton` | `hinton_k2aaa_a3` | the pooled rows of the 5 clients (`centralized/train.csv`, 8,659), one model (`--pooled --n-clients 1`) | same rule | the Hinton line's round without aggregation (the one model is the round's adapter); 3 rounds; a reference without privacy |
| local client adapters (`sqllocal_hinton_r1_c1` to `c5`) | `hinton_k2aaa_a3` | each client's pairs of DPO round 1 of the Hinton line | same | the client adapters of that round, before averaging; evaluation only |
| `sqldpo_s0/sft_hinton` | `hinton_k2aaa_a3` | each client's Spider rows, gold SQL | none | 2 more FedAvg SFT rounds (lr 2e-4, 1 local epoch) |

SQL DPO runs 3 rounds, fixed for every line and seed, and is reported at
round 3 (owner, 2026-11-10; chosen on Spider test, seed 0). Each line is a
curve (`scripts/curve.py`): it trains a step, evaluates it, publishes, and
records the result in `audits/curves/`. Reused adapters:
`fedicl-sql/docs/SERVER_STORAGE.md` section 5.

Final table (Spider test; every SQL DPO line at round 3):

| Row | Line |
|---|---|
| base, 7B teacher, local clients, FedProx, FedNTD | reference rows |
| FedAvg R3 | from the base model |
| centralized Spider, centralized Spider + BIRD | references without privacy |
| `gold_k2aaa_a3`, `hinton_k2aaa_a3` | server stage on BIRD, then FedAvg |
| SQL DPO from FedAvg R3 | the core since 2026-11-16: no server stage, no teacher (round 3: 75.13 with `full`, 77.36 with `codes`, seed 0) |
| SQL DPO from `gold_k2aaa_a3` | control: server stage without the teacher |
| SQL DPO from `virtual_k2aaa_a3` | control: soft targets without the teacher (seed 0) |
| `virtual_k2aaa_a3`, `self_k2aaa_a3` | server stage with soft targets from no teacher, or from the student itself, then FedAvg (seed 0) |
| NLL-only round, extra FedAvg SFT rounds from `hinton_k2aaa_a3` | controls: no preference term, SFT at the same compute |
| SQL DPO from `hinton_k2aaa_a3` | the line with the Hinton server stage (round 3: 76.71 on seed 0, 77.04 on seed 1); out of the core since 2026-11-16 |
| selection by execution over 8 samples | FedAvg R3, `hinton_k2aaa_a3` and DPO round 3 from each, at inference, no training |
| CoT (short analysis) | E5, template R1, self-taught R1-R3 |

### P1, the `codes` schema (phase `sqlcodes_s0`)

The FedAvg line of seed 0 with `--schema-style codes` (training) and
`--client-schema-style codes` (FedAvg) instead of `full`, in every
training, sampling and evaluation prompt. `codes` writes one line per table;
each column carries its type, primary key, the column name in words and 2
sample values, then a foreign key block and the text values the question
quotes as whole words. `--max-len 7680` for the 82 client 3 rows on
`baseball_1` (up to 7,433 tokens); the rest of the settings are the seed 0
recipe. Outputs: `artifacts/protocol_v2/sqlcodes_coder15b_alpha01_s0/`.

| Line (curve) | Start | Step |
|---|---|---|
| `sqlcodes_s0/fedavg_sft` | base model | one FedAvg round (lr 2e-4, 1 local epoch); 3 rounds |
| `sqlcodes_s0/fedavg` | round 3 of `fedavg_sft` | DPO + NLL round, the settings of `sqldpo_s0/fedavg`; 3 rounds |
| `sqlcodes_s0/hinton_sft` | seed 0 Hinton server stage (BIRD, `full` prompts), row `federated_stage__K2fkl__s0__132e798a5be2__8393f0f9` | one FedAvg round with `codes` prompts; 3 rounds (`sqlcodes_hinton_k2aaa_a{k}_vllm_inproc`) |
| `sqlcodes_s0/hinton` (stopped in round 1 on 2026-11-16, not in the task list) | round 3 of `hinton_sft` | DPO + NLL round with `codes`; 3 rounds (`sqlcodes_dpo_hinton_r{k}_vllm_inproc`) |

Tasks `sqlcodes_s0/rob_*` and `bird_*` evaluate FedAvg R3 and DPO round 3
of these lines on Spider dev, DK, Realistic, SYN and BIRD dev under the arm
names of their Spider test rows (`sqlcodes_fedavg_r3_vllm_inproc`,
`sqlcodes_dpo_fedavg_r3_vllm_inproc`). Their `full` comparators are
`sql_fedavg_r3_vllm_inproc` and `sqldpo_fedavg_r3_vllm_inproc`, same
engine (vLLM 0.33 inproc) and batch 16. `eval_teacher_codes` is the 7B
teacher with `codes` prompts (arm `sql_teacher7b_codes_vllm_inproc`, its
`full` comparator `sql_teacher7b_vllm_inproc`); `xsel_dpo_r3` is selection
by execution on DPO round 3 with `codes` (`xsel_codes_dpo_r3`, greedy
column `sqlcodes_dpo_fedavg_r3_vllm_inproc`).

### The repetition penalty (phase `norp_s0`)

`--repetition-penalty 1.0` turns the penalty off in `scripts.eval_standard`,
the DPO round, `scripts.peer_check`, `scripts.exec_select` and
`scripts.synth_questions`. Without the option a command decodes as before,
with the model's generation config (1.1). Arms without the penalty carry
`_np`. In a DPO root the penalty of the samples is a setting of the root.

- Arms of the six evaluated rows: `sqlcodes_fedavg_r3_np_vllm_inproc`,
  `sqlcodes_dpo_fedavg_r1_np_vllm_inproc`,
  `sqlcodes_dpo_fedavg_r3_np_vllm_inproc`, `sqlcv2_base_np_vllm_inproc`,
  `sql_fedavg_r3_np_vllm_inproc`, `sqldpo_fedavg_r3_np_vllm_inproc`.
- `norp_s0/fedavg` (curve, 1 round): root
  `artifacts/protocol_v2/sqlcodes_coder15b_alpha01_s0/fedavg_np`, from
  round 3 of `sqlcodes_s0/fedavg_sft`.

### Synthetic rows and the short reads (phases `synth_s0`, `synv_s0`, `vote_s0`)

On the `codes_v2` line without the penalty, seed 0.

- `synth_s0/build` (`scripts/synth_questions.py`, finished, `04922932`):
  each client refills the SQL of its own rows on its own databases and
  the base model writes one question per query. Split:
  `artifacts/protocol_v2/sqlsynnp_coder15b_alpha01_s0/synth/split` (own
  rows, then rows with ids `syn:c<client>:<n>`); evidence:
  `audits/protocol_v2/sqlsynnp_coder15b_alpha01_s0/synth/`. The build with
  the penalty is under `sqlsyn_coder15b_alpha01_s0` and stays as it is.
- `synv_s0/collect` (`experiments/federated_pref/run.py collect`): 8
  samples per question of that split from FedAvg R3 of
  `sqlcv2_s0/fedavg_sft`, labelled by execution against the row's SQL.
  Root `artifacts/protocol_v2/sqlsynnp_coder15b_alpha01_s0/verify`,
  samples under `audits/.../verify/samples` (not published).
- `synv_s0/filter` (`scripts/synth_verify.py`, CPU): keeps a synthetic row
  when at least one finished sample returns the result of its SQL and its
  training sequence fits `--max-len 7680`. It stops if the samples were
  not drawn with `codes_v2` and without the penalty, or on another split
  file. New split: `artifacts/.../sqlsynnp_coder15b_alpha01_s0/verified/split`;
  evidence: `audits/.../verified/` (`summary.json`: rows kept by number of
  tables and by number of matching samples; `rows/client_<i>.jsonl`: one
  decision per synthetic row, ids and counts only).
- `synv_s0/sft_synth`: one FedAvg SFT round (the recipe of the rounds of
  `sqlcv2_s0/fedavg_sft`) from FedAvg R3 on the new split; stage
  `sqlcv2_sftsyn_x1_s0`, adapter
  `artifacts/.../sqlsynnp_coder15b_alpha01_s0/sft_synth/x1/fedavg_adapter`.
- `synv_s0/sft_plain`: the same round on the clients' rows; stage
  `sqlcv2_sft_x1_s0`, adapter
  `artifacts/protocol_v2/sqlcv2_coder15b_alpha01_s0/sft/x1/fedavg_adapter`.
- `synvc_s0/*`: the same five steps on the `codes` line, from FedAvg R3
  of `sqlcodes_s0/fedavg_sft` with `codes` prompts. Roots
  `verify_codes`, `verified_codes` and `sft_synth_codes/x1` under
  `artifacts/.../sqlsynnp_coder15b_alpha01_s0/`, stages
  `sqlcodes_sftsyn_x1_s0` and `sqlcodes_sft_x1_s0` (adapter
  `artifacts/protocol_v2/sqlcodes_coder15b_alpha01_s0/sft/x1/fedavg_adapter`).
- `vote_s0/check` (`scripts/vote_label_check.py`): reads the samples of
  rounds 1-3 under the DPO root's `samples` folder, labels them again by a
  vote over execution results and compares with the recorded gold labels.
  Results: `experiments/vote_check/results/cv2_dpo_np/` (`summary.json`,
  `per_question.csv`); working files under
  `artifacts/protocol_v2/vote_check/cv2_dpo_np/`.
- `vote_s0/xsel_dpo_r3` (`scripts/exec_select.py`): results under
  `experiments/exec_select/results/xsel_cv2_dpo_r3_np_s0_spider_test/`.

### The corrected prompt (phase `sqlcv2_s0`)

The line of `sqlcodes_s0` from the base model with `codes_v2` in every
training, sampling and evaluation prompt, decoded without the repetition
penalty (samples and evaluation); the recipe is otherwise the same. Outputs: `artifacts/protocol_v2/sqlcv2_coder15b_alpha01_s0/`.

| Line (curve) | Start | Step | Arms (Spider test) |
|---|---|---|---|
| `sqlcv2_s0/fedavg_sft` | base model | one FedAvg round (lr 2e-4, 1 local epoch); 3 rounds | `sqlcv2_fedavg_r{k}_np_vllm_inproc` |
| `sqlcv2_s0/fedavg` | round 3 of `fedavg_sft` | DPO + NLL round, the settings of `sqldpo_s0/fedavg`; 3 rounds | `sqlcv2_dpo_fedavg_r{k}_np_vllm_inproc` |

Two rows without a curve: the base model with no adapter
(`sqlcv2_base_vllm_inproc`), and centralized SFT on the pooled Spider train
rows (`centralized/train.csv`, 8,659 rows, 3 epochs, lr 2e-4, the recipe of
`p227_central_e3_s0` with `codes_v2` and `--max-len 7680`; result
`sqlcv2_central_e3_s0`, adapter `central_e3/epochs/epoch_3`, arm
`sqlcv2_central_e3_np_vllm_inproc`).

### F1, 20 clients (phase `f1_s0`; only `fedavg_sft` is in the task list)

Split `processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k20`
(committed): the `k5` procedure with 20 clients over the same 8,659 rows.
The recipe of the `codes` line (P1) otherwise: `codes` prompts at the
clients, `--max-len 7680`. Outputs:
`artifacts/protocol_v2/f1k20_coder15b_alpha01_s0/`.

| Line (curve) | Start | Step | Arms (Spider test) |
|---|---|---|---|
| `f1_s0/fedavg_sft` | base model | one FedAvg round, every client; 3 rounds | `f1_fedavg_r{k}_np_vllm_inproc` (evaluated without the penalty) |
| `f1_s0/hinton_sft` | seed 0 Hinton server stage, row `federated_stage__K2fkl__s0__132e798a5be2__8393f0f9` | same | `f1_hinton_k2aaa_a{k}_vllm_inproc` |
| `f1_s0/fedavg`, `f1_s0/hinton` | round 3 of the line above | DPO + NLL round, the settings of `sqldpo_s0/fedavg`; 3 rounds | `f1dpo_fedavg_r{k}`, `f1dpo_hinton_r{k}` (`_vllm_inproc`) |
| `*_p10` | the same, `p10_` folders | the same with `--clients-per-round 10` | `f1p10...` |

Comparators (5 clients, seed 0, Spider test, `codes`): FedAvg R3 73.17 and
DPO round 3 77.36 from the base model; from the server stage, the rows of
`sqlcodes_s0/hinton_sft` and `sqlcodes_s0/hinton`. Centralized Spider SFT
exists only with `full` (`sql_central_e3_vllm_inproc`, 70.75).

### Seed 1 (phase `sqldpo_s1`, finished)

The three DPO lines of seed 0 with seed 1 in every training and sampling
command; evaluation arms carry `_s1` in their names. Curve rule: every
curve has at most 3 steps, so every step runs; the DPO lines start from
round 3 of their SFT curve by name.

| Line (curve) | Start | Step |
|---|---|---|
| `sqldpo_s1/hinton` | `hinton_k2aaa_a3` seed 1 (earlier adapter, approved 2026-11-10; the seed 0 recipe with seed 1, SQL-only, no replay) | DPO + NLL round, the settings of seed 0; 3 rounds |
| `sqldpo_s1/fedavg_sft` | base model | one FedAvg round (lr 2e-4, 1 local epoch), the command of the seed 0 row; 3 rounds |
| `sqldpo_s1/fedavg` | round 3 of `fedavg_sft` | DPO + NLL round; 3 rounds |
| `sqldpo_s1/gold_sft` | gold server stage of seed 1 (`K2[ce]`, 2 epochs on BIRD; earlier adapter, approved 2026-11-11; not the `Areplay` rows) | one FedAvg round, same recipe; 3 rounds |
| `sqldpo_s1/gold` | round 3 of `gold_sft` | DPO + NLL round; 3 rounds |

Outputs: `artifacts/protocol_v2/sqldpo_coder15b_alpha01_s1/`.

### Seed 2 (phase `sqldpo_s2`, stopped)

Dropped on 2026-11-15. Finished: the Hinton server stage trained from the
base model with the seed 0 recipe and `--seed 2`, 3 FedAvg rounds from it
(`sql_hinton_k2aaa_a{1,2,3}_s2`), and DPO round 1 from round 3
(`sqldpo_hinton_r1_s2`). Outputs: `artifacts/protocol_v2/sqldpo_coder15b_alpha01_s2/`.

### Selection by execution and reference rows (phase `sqldpo_s0`)

- Selection by execution (`scripts/exec_select.py`, tasks `xsel_*`): 8
  samples per Spider test question through vLLM (T 0.7, 256 new tokens, the
  DPO sampling settings), no training. Two rules that never read the gold
  SQL: keep the greedy SQL when it executes, else the most frequent sample
  that executes; or the most frequent result among the samples that
  execute. The greedy column is the adapter's committed vLLM inproc row.
  Outputs: `experiments/exec_select/results/<arm>_s0_spider_test/`.
- Reference rows through vLLM inproc: the 7B teacher zero-shot (bf16) and
  the earlier seed 0 adapters approved on 2026-11-13 (FedProx R3, FedNTD,
  the 5 local client models; `fedicl-sql/docs/SERVER_STORAGE.md` section
  5).

### CoT analysis line (phase `fedcot_s0`, finished)

Nothing of this phase is in the queue. The paper uses its rows as a short
analysis: server stage E5 (60.64), template round 1 (62.69), self-taught
rounds 1-3 (best R2, 60.64).

| Line (task) | Start | Data | Target | Step |
|---|---|---|---|---|
| server (`curve_server`) | base model | 4,109 BIRD rows (teacher SQL matches gold) | teacher's query plan + SQL | one more epoch from the last, its own 1-epoch cosine schedule; 6 run (best: E5) |
| template client SFT (`curve_client`) | best server epoch | each client's Spider rows (8,659 in all) | plan derived from the gold SQL by a template + gold SQL | one FedAvg round, 1 local epoch, gradient checkpointing; 1 round |
| self-taught SFT (`curve_star`) | best server epoch | every client question, 8 samples through vLLM | the most frequent correct sampled plan + SQL; for a question with none, a plan the model writes with the gold SQL as a hint, kept if its SQL is correct; otherwise the question is dropped | one FedAvg round (weighted by target count), client SFT recipe (lr 2e-4, 1 local epoch); 3 rounds |

- One prompt (`qp_cot_v1`) for every step: server SFT, client SFT, sampling,
  evaluation (1,024 new tokens, strict parsing; an output that does not parse
  scores 0). The server stages use `--max-len 7680`, which keeps every row.
- Curve rule of this phase: a step counts as a gain only above 0.5 point
  over the best step so far; a stage stops after 2 steps without a gain or
  at its maximum; the next stage starts from the best step.
- Rationalization (self-taught rounds only): 4 samples at T=0.7 with the
  gold SQL after the question (the hint is never in a training prompt); a
  response whose plan names the hint ("the correct SQL ...") is not kept.
- Closest prior work for the self-taught step: STaR-SQL (He et al., ACL
  2025, arXiv 2502.13550), centralized; here federated, from a teacher-plan
  server stage, in the Struct-SQL plan format.
- Server epochs are a chain: an epoch from a chain may score slightly below
  a run with one schedule over the same length.
- Not run: template rounds 2-3 and CoT DPO (owner, 2026-11-10). Folders not
  used by the curves: `server_l7680_e2`, `srv_e1`, `srv_e2`, `server_e1`.

### vLLM (2026-11-09)

Sampling: `vllm_s0/bench_sql` sampled the 400 round-1 questions of client 3
in 3:40 for the whole task (HF: 13:52), sample accuracy 72.0% and pass@8 89.0%
(HF: 71.0%, 88.5%). DPO rounds sample with `--engine vllm`.

Evaluation: `scripts.eval_standard --engine vllm` decodes greedily through
vLLM with the same prompts, parser and scoring. In vLLM's default mode two
runs of FedAvg R3 gave 71.45 and 71.22 EX on Spider test, with a different
SQL on 138 of 2,147 rows: the engine core runs in its own process, so how
requests are grouped into batches depends on timing. The curves therefore
use `--vllm-determinism inproc` (engine core in the same process, so
scheduling is deterministic, vLLM's documented setting for reproducible
offline runs). Rows compared question by question share one engine.

| Check | Compared | Result |
|---|---|---|
| `check_sql` | FedAvg R3, HF row `p253ref_fl_a3` (71.50) and vLLM | 71.45, within 0.5 |
| `check_cot` | 1-epoch server stage (plan + SQL), HF and vLLM | HF 52.86, vLLM 51.70 |

The reports (agreement, discordant rows) are in
`audits/protocol_v2/vllm_eval_check_s0/`.
