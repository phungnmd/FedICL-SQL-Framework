# FedLS-SQL: run queue

GPU work on the server runs through one queue file,
`fedicl-sql/queues/active.toml`: every task (one command), what it needs
first, in priority order. One worker per GPU takes the first ready task, so
both cards stay busy until the queue is empty. Conventions: `AGENTS.md`
("Defaults") and `CONVENTION.MD` section 5. Remove an experiment's tasks from
the queue once its results are logged in `LAB_LOG.md`.

Every task resumes when it runs again and skips finished work. Pulling while
workers run is fine; when a push changes code that a running or queued task
would load, the agent says so here and in chat.

## How to run

### Step 0: update the checkout and run the tests

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_task_queue.py tests/test_dpo.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py tests/test_train_length_probe.py tests/test_curve.py tests/test_compare_predictions.py tests/test_eval_arms_config.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
```

### Step 1: worker check, about 1 min (once)

Both workers on the `selftest` phase. Each prints its own card and sleeps
30 s, then one runs a task that needed both; press Ctrl+C once during the
sleep to see the stop, rerun, and check that each reports `DONE queue`.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 0 --phase selftest; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 1 --phase selftest; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

### Step 2: one worker per GPU, each in its own terminal

The two commands differ only in the GPU digit. Without `--phase` a worker
runs the full queue; add `--phase fedcot_s0` to run only that phase. A worker rereads the queue before every task, so
tasks pushed later run after a pull without a restart. It prints `start` /
`end` per task, the task's own progress lines prefixed `[gpu0 <task>]`, and a
final `DONE queue` line. Per-task logs: `.queue_state/logs/`.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

- Ctrl+C stops the worker and its running task; rerunning the same command
  continues where it stopped.
- The first failed task stops the worker: `STOP queue: <task> failed: <last
  error line>` and the log path. A worker that sees a failure on another
  worker stops before its next task. Rerunning a worker retries failed
  tasks.
- Each phase ends with a `publish` task that commits and pushes its results.

GPU 1 is in use by another user (2026-11-09): do not start a worker on it,
and do not run other GPU jobs next to a task on GPU 0.

### Server `--max-len` (checked 2026-11-09)

With query plan + SQL targets, the longest of the 4,109 BIRD server rows is
7,601 tokens (2 rows above 7,168, the limit set for SQL-only targets).
Training steps on the 4 longest rows peaked at 18.8 GiB reserved. The server
stages use `--max-len 7680`, which keeps every row.

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
offline runs). The checks against HF use the runs already made:

| Check | Compared | Stops when |
|---|---|---|
| `check_sql` (done) | FedAvg R3, HF row `p253ref_fl_a3` (71.50) and vLLM | EX differs by more than 0.5 (71.45: passed) |
| `check_rerun` | FedAvg R3 with vLLM default, twice | report only |
| `check_cot` | 1-epoch server stage (plan + SQL), HF and vLLM | EX differs by more than 0.5 |

The reports (agreement, discordant rows) go to
`audits/protocol_v2/vllm_eval_check_s0/`. Every fedcot number of the curves
is a vLLM evaluation; the baselines in the final table will be evaluated with
vLLM too, so rows compared question by question share one engine.

### Code pushed 2026-11-09 (next phase)

Pulling between tasks is safe: the HF evaluation and DPO defaults are
unchanged, and a worker reads the new queue before its next task. The new
queue replaces the fixed server tasks (`srv_e2`, `srv_e3`, their evaluations)
with the curves; the 2-epoch run from the base model that the old queue
started (`server_l7680_e2`) is not used by them.

### Code pushed 2026-11-09: stopping rule

`fedicl-sql` 160c2143 sets a gain threshold of 0.5 point and maxima 8 / 8 / 6
per curve. No task command changed, and no curve has started, so a pull at
any time is safe; pull before `fedcot_s0/curve_server` starts.

### Code pushed 2026-11-09: gradient checkpointing kept

`fedicl-sql` e50d05f4: client rounds and DPO rounds keep gradient
checkpointing, and `fedcot_s0/client_probe` measures only that mode (its
command changed, so it runs again, about 1.5 min). The finished
`fedcot_s0/smoke` keeps its command and is not rerun.

### Code pushed 2026-11-09: deterministic vLLM evaluation

`fedicl-sql` fb0c33b8 adds `--vllm-determinism`; the next push keeps only
the checks above and names the curve evaluations `..._vllm_inproc`. Nothing
was running (the worker stopped at `check_rerun`): pull, then start the
worker; it reruns `check_rerun` as a report, runs `check_cot`, publishes, and
starts the curves. DPO sampling keeps vLLM's default mode.

### Status (read-only, any time, second terminal)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

Add `--phase <name>` to see one phase only. EX by step and the decision of
every curve:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.curve status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

### Memory checks (owner, first time each path runs)

- `fedcot_s0/srv_e1` (BIRD-length rows): the `first optimizer update done
  ... peak reserved` line, about 20 GiB expected.
- `fedcot_s0/smoke` (vLLM plan + SQL sampling at 1,024 new tokens, then DPO
  on plan + SQL pairs, chosen and rejected in one pass; this smoke ran
  without gradient checkpointing, the full rounds use it):
  `vLLM samples loaded ... cut at max_tokens` stays low, and the
  `DPO smoke on the longest pair` line stays under 21.5 GiB (the task stops
  above it). Every full DPO round repeats that check on its own longest pair.
- `fedcot_s0/client_probe`: the `probe gc` line (peak reserved and
  `mean_seconds_after_first` on the 4 longest client rows); the task stops
  above 21.5 GiB, which keeps the client rounds from starting. Without
  gradient checkpointing the longest row (2,921 tokens) ran out of memory
  (2026-11-09); with it, 9.25 GiB and 1.7 s per step.
- Evaluations print `first batch ... peak reserved`, then a line a minute
  with EX, EM and execution errors so far; sampling prints sample accuracy
  and pass@8 so far. Numbers above 21.5 GiB show in red on the console.
- Shared GPU memory of each task's process stays near zero.

## Queue content

Spider numbers are Spider test (2,147 rows, owner 2026-11-07); Spider dev is
not evaluated. One seed (seed 0). Every line is run as a curve: each stage is
evaluated on Spider test, and the next stage starts from the best checkpoint
so far. Choices are made on Spider test, so its numbers are reported as
"chosen on Spider test", never as held-out. Reference (owner-approved reuse,
run `p227_fl_aaa_s0`): FedAvg R3 71.50 on Spider test, same contract (batch
16, greedy 256).

### Stopping rule (the same for every line)

- A step counts as a gain only if Spider test EX is more than 0.5 point
  above the best step so far (owner, 2026-11-09; slow DPO rises of 0.5-1.8
  points per round with dips in between read as flat under a 1-point
  threshold).
- Stop a stage after 2 steps in a row without a gain, or at its maximum:
  server 8 epochs, client SFT 8 rounds, DPO 6 rounds.
- The next stage starts from the best checkpoint of the stage; a tie within
  0.5 point goes to the cheaper one (fewer epochs or rounds).
- Precisely: the best step changes only on a gain, so a later step within
  0.5 point of it never replaces it. Threshold, patience and maximum are set
  per curve in the queue file (`min_gain`, `patience`, `max_steps`).
- Automated: each line is a curve (`scripts/curve.py`). It trains a step,
  evaluates it with vLLM, publishes, applies the rule, and either trains the
  next step or stops and records the decision in `audits/curves/`; the next
  line starts from that best step.

### Full pipeline (phase `fedcot_s0`)

| Line (task) | Start | Data | Target | Step |
|---|---|---|---|---|
| server (`curve_server`) | base model | 4,109 BIRD rows (teacher SQL matches gold) | teacher's query plan + SQL | one more epoch from the last, its own 1-epoch cosine schedule; up to 8 |
| client SFT (`curve_client`) | best server epoch | each client's Spider rows (8,659 in all) | plan derived from the gold SQL + gold SQL | one FedAvg round, 1 local epoch, gradient checkpointing; up to 8 |
| DPO + NLL (`curve_dpo`) | best client round | every client question each round, 8 samples through vLLM | the client's own sampled plan + SQL, labelled by execution | one federated round, 2 local epochs, chosen and rejected in one pass; up to 6 |

- One prompt (`qp_cot_v1`) for every step: server SFT, client SFT, sampling,
  evaluation (1,024 new tokens, strict parsing; an output that does not parse
  scores 0).
- DPO pairs: the most similar correct and wrong sampled outputs; an output
  that does not parse counts as wrong; when no sample is correct, the chosen
  side is the plan derived from gold + gold SQL. Beta 0.1, lr 1e-5, 2 local
  epochs, 16 pairs per update.
- Server epochs as a chain (owner, 2026-11-09): cheaper than a separate run
  per length and open-ended; an epoch from a chain may score slightly below
  a run with one schedule over the same length. A clean run of the chosen
  length can be retrained once the method is settled.
- Fixed, not tuned: 1 local epoch per client round; DPO beta, lr, local
  epochs, K=8, T=0.7.
- `fedcot_s0/smoke` (from the 1-epoch server stage, 8 questions per client)
  runs the DPO round path of the full rounds and checks its memory, not
  accuracy.

### Baselines (out of the queue for now, owner 2026-11-09)

FedAvg rounds and SQL-only federated DPO come back after the main pipeline,
under the same stopping rule (SQL-only DPO then starts from the best FedAvg
round).

### Final table (Spider test, best checkpoint of each line by the rule)

| Row | Line |
|---|---|
| FedAvg | best round by the rule |
| SQL-only DPO | best round, from the best FedAvg round |
| fedcot after client SFT | best client round |
| fedcot full | best DPO round |

### Order on GPU 0

1. `fedcot_s0/smoke`, `fedcot_s0/client_probe` (minutes each).
2. `vllm_s0`: the three checks (seconds), publish.
3. `curve_server`: epoch 1 is done (1.14 h); each further epoch about 1.1 h
   plus a vLLM evaluation (at most 7 more epochs, about 9 h).
4. `curve_client`, then `curve_dpo`; their step times are measured by the
   probe, the smoke and the first steps.

GPU 1 is in use by another user. Folders not used by the curves:
`server_l7680_e2` (a 2-epoch run from the base model of the earlier queue),
`srv_e1`, `srv_e2`, `server_e1` (stage contracts of earlier attempts).
