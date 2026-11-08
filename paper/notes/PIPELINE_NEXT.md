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
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_task_queue.py tests/test_dpo.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
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
runs the full queue; add `--phase fedcot_s0` (or `fedpref_s0`, or both) to
run only those phases. A worker rereads the queue before every task, so
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
- A failed task blocks only the tasks that need it; the worker runs the
  others, then stops with `STOP queue` and the list. Rerunning a worker
  retries failed tasks.
- Each phase ends with a `publish` task that commits and pushes its results.

### Status (read-only, any time, second terminal)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

Add `--phase <name>` to see one phase only.

### Memory checks (owner, first time each path runs)

- `fedpref_s0/smoke` (first task on one GPU, about 10-15 min): the
  `first batch ... peak reserved` and `DPO smoke on the longest pair` lines
  stay under 21.5 GiB. The first-batch number also tells whether sampling can
  use more prompts per call in the next experiment.
- `fedcot_s0/srv` (BIRD-length rows): the `first optimizer update done
  ... peak reserved` line, about 20 GiB expected.
- `fedcot_s0/smoke` (query plan sampling at 1,024 new tokens, then DPO on
  plan + SQL pairs): the same two lines as the SQL-only smoke, and the
  sampling time per question, which sets `--questions-per-client` for the
  query-plan DPO rounds (200 now).
- Evaluations print `first batch ... peak reserved`, then a line a minute
  with EX, EM and execution errors so far; sampling prints sample accuracy
  and pass@8 so far. Numbers above 21.5 GiB show in red on the console.
- Shared GPU memory of each task's process stays near zero.

## Queue content

Spider numbers are Spider test (2,147 rows, owner 2026-11-07); Spider dev is
not evaluated. One seed (seed 0). Reference on Spider test (owner-approved
reuse, run `p227_fl_aaa_s0`): FedAvg R3 71.50, same contract (batch 16, greedy
256).

The code in this push changes `experiments/federated_pref/run.py` and
`fedicl_sql/preference/`, which every `fedpref_s0` and `fedcot_s0` DPO task
loads. Nothing has run yet: pull and run Step 0 before starting the workers.

### Full pipeline (phase `fedcot_s0`, 26 tasks)

What it measures: Spider test EX of the whole method, with a reading after
each stage so the later stages can be changed from the signal.

| Step | Where | Data | Target | Task | Eval |
|---|---|---|---|---|---|
| 0 | server, from the base model | 4,109 BIRD rows (teacher SQL matches gold) | teacher's query plan + SQL | `srv` | Spider test, lowest priority |
| 1-3 | 5 clients, FedAvg, 1 local epoch each | each client's Spider rows | plan derived from the gold SQL + gold SQL | `c1`, `c2`, `c3` | after `c3` |
| 4-5 | 5 clients, federated DPO + NLL | 200 questions per client per round | the client's own 8 sampled plan + SQL, labelled by execution | `dpo_r1`, `dpo_r2` | after each round; BIRD dev too after round 2 |

- Every step uses the same query-plan prompt (`qp_cot_v1`): server SFT,
  client SFT, sampling, evaluation (1,024 new tokens, strict parsing; an
  output that does not parse scores 0).
- DPO pairs: the most similar correct and wrong sampled outputs; a sample
  that does not parse counts as wrong; when no sample is correct, the
  chosen side is the plan derived from gold + gold SQL. Settings as the
  SQL-only rounds (beta 0.1, lr 1e-5, 2 epochs, FedAvg by pair count).
- Step 0 starts from the base model, not from FedAvg R3, so the student
  learns the plan format before any federated round, and the five client
  rounds match FedAvg R5 and SQL-only DPO R2 (3 + 2 rounds).
- Each stage row is committed (`publish_*`) before the next stage starts,
  because a stage starts only from a committed row.

### SQL-only baselines (phase `fedpref_s0`, 17 tasks)

- FedAvg SFT rounds 4 and 5 from R3 (`sft_r4`, `sft_r5`): the federated
  baseline with five client rounds.
- Federated DPO + NLL from R3, rounds 1-2 (`dpo_r1`, `dpo_r2`): 400 questions
  per client, 8 sampled SQL at T=0.7, labels by execution on the client's
  database, the same pair rule and DPO settings as above.
- Every adapter evaluated on Spider test and BIRD dev
  (`scripts.eval_standard --sets spider_test bird --allow-test`).

### Final table (Spider test)

| Row | Client rounds | Source |
|---|---|---|
| FedAvg R3 | 3 SFT | reference, 71.50 |
| FedAvg R5 | 5 SFT | `fedpref_sft_r5` |
| SQL-only DPO R2 | 3 SFT + 2 DPO | `fedpref_dpo_r2` |
| fedcot after client SFT | server + 3 SFT | `fedcot_c3` |
| fedcot full | server + 3 SFT + 2 DPO | `fedcot_dpo_r2` |

### Priority and time

The two smokes run first, then the `fedcot_s0` chain (the longest path),
then the SQL-only tasks fill the other GPU. Estimate: fedcot about 30-35
GPU-h (query-plan sampling is the large unknown, measured by its smoke),
fedpref about 16 GPU-h; about 24-30 h on both cards.
