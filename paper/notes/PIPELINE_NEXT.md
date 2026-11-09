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
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_task_queue.py tests/test_dpo.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py tests/test_train_length_probe.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
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

### Now: server `--max-len` (2026-11-09)

`fedcot_s0/srv_e1` stopped while building its examples: one BIRD row has
6,665 prompt + 525 target tokens = 7,190, above `--max-len 7168` (plan +
SQL targets are longer than the SQL-only targets the 7,168 limit was set
for). `lengths_s0/server_cot` renders all 4,109 rows as training does,
reports how many each limit would reject, and runs 8 training steps on the
4 longest rows from the base model to read the peak VRAM. Then the server
stages get a `--max-len` that keeps every row, if its peak stays under
21.5 GiB. Run only this phase (a few minutes), then paste the `lengths`,
`longest` and `probe` lines:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 0 --phase lengths_s0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

### vLLM sampling (checked 2026-11-09)

`vllm_s0/bench_sql` sampled the 400 round-1 questions of client 3 through
vLLM in the WSL venv in 3:40 for the whole task (HF: 13:52), with sample
accuracy 72.0% and pass@8 89.0% (HF on the same questions: 71.0%, 88.5%).
DPO rounds sample with `--engine vllm`. The console shows the progress and
the key vLLM lines; the full vLLM log is under `<out>/vllm/`.

The SQL-only baselines (`fedpref_s0`) left the queue (owner, 2026-11-09). A
worker still running `fedpref_s0/dpo_r1` finishes it unless stopped: press
Ctrl+C and start the worker again (this also retries the failed fedcot
tasks). Its samples and adapters stay on the server for later.

### Status (read-only, any time, second terminal)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

Add `--phase <name>` to see one phase only.

### Memory checks (owner, first time each path runs)

- `fedcot_s0/srv_e1` (BIRD-length rows): the `first optimizer update done
  ... peak reserved` line, about 20 GiB expected.
- `fedcot_s0/smoke` (query plan sampling at 1,024 new tokens, then DPO on
  plan + SQL pairs): the `first batch ... peak reserved` and `DPO smoke on
  the longest pair` lines stay under 21.5 GiB.
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

- A step counts as a gain only if Spider test EX rises by more than 1 point
  (one seed: two adapters on the same questions differ by about 0.5-0.7
  points from noise alone).
- Stop a stage after 2 steps in a row without a gain, or at its maximum:
  server 3 epochs, client SFT 5 rounds, DPO 4 rounds.
- The next stage starts from the best checkpoint of the stage; a tie within
  1 point goes to the cheaper one (fewer epochs or rounds).
- The queue cannot branch yet, so each decision is a queue edit after the
  numbers are in (automating the rule is planned).

### Full pipeline (phase `fedcot_s0`)

| Step | Where | Data | Target | Now in the queue |
|---|---|---|---|---|
| server | base model | 4,109 BIRD rows (teacher SQL matches gold) | teacher's query plan + SQL | 1 and 2 epochs (`srv_e1`, `srv_e2`), each a full run with its own cosine schedule, both evaluated |
| client SFT | 5 clients, FedAvg, 1 local epoch per round | each client's Spider rows | plan derived from the gold SQL + gold SQL | queued after the server choice |
| DPO + NLL | 5 clients, FedAvg by pair count | every client question, each round (owner, 2026-11-09), sampled with vLLM | the client's own 8 sampled plan + SQL, labelled by execution | queued after the client SFT choice |

- One prompt (`qp_cot_v1`) for every step: server SFT, client SFT, sampling,
  evaluation (1,024 new tokens, strict parsing; an output that does not parse
  scores 0).
- DPO pairs: the most similar correct and wrong sampled outputs; an output
  that does not parse counts as wrong; when no sample is correct, the chosen
  side is the plan derived from gold + gold SQL. Beta 0.1, lr 1e-5, 2 local
  epochs.
- The server step starts from the base model, so the plan format comes
  before any federated round.
- `fedcot_s0/smoke` (from the 1-epoch server stage) tests the query-plan DPO
  path and measures sampling time before the DPO rounds are queued.
- Decision 1, after `publish_srv_eval`: 2 epochs better by more than 1 point
  queues a 3-epoch run; otherwise the client rounds start from the better
  of the two.

### Baselines (out of the queue for now, owner 2026-11-09)

FedAvg R1-R5 and SQL-only federated DPO come back after the main pipeline,
under the same stopping rule (SQL-only DPO then starts from the best FedAvg
round).

### Final table (Spider test, best checkpoint of each line by the rule)

| Row | Line |
|---|---|
| FedAvg | best of R1-R5 |
| SQL-only DPO | best round, from the best FedAvg round |
| fedcot after client SFT | best client round |
| fedcot full | best DPO round |

### Order on GPU 0

`srv_e1` (about 1.3 h), `srv_e2` (about 2.6 h), the query-plan smoke, the
two server evaluations (about 1.4-2.6 h each): decision 1 after about 8-9 h.
GPU 1 is in use by another user. The server stages write to
`server_e1` and `server_e2`; the older `srv_e1` and `srv_e2` folders hold
only stage contracts from the attempt before the sidecar fix and are not
used.
