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
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_task_queue.py tests/test_dpo.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
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
- A failed task blocks only the tasks that need it; the worker runs the
  others, then stops with `STOP queue` and the list. Rerunning a worker
  retries failed tasks.
- Each phase ends with a `publish` task that commits and pushes its results.

### Fix once: query-plan sidecar line endings (2026-11-09)

`fedcot_s0/srv_e1` and `srv_e2` failed with `sidecar hash does not match
its provenance`: the server checkout wrote the plan sidecar with CRLF line
endings, so its bytes no longer match the recorded hash (the content is the
same). This restores the tracked files under `rationale_kd` with LF bytes
and checks the hash; it stops without touching anything if the server copy
differs in content. Safe while a worker runs.

```powershell
& { $ErrorActionPreference='Stop'; $d='processed_data/protocol_v2/rationale_kd'; $changed = git diff --name-only -- $d; if ($LASTEXITCODE -ne 0) { throw 'git diff failed' }; if ($changed) { throw "content differs from Git: $changed" }; $files = @(git ls-files -- $d); if ($LASTEXITCODE -ne 0 -or $files.Count -eq 0) { throw 'git ls-files failed' }; Remove-Item -LiteralPath $files; git -c core.autocrlf=false checkout -- $d; if ($LASTEXITCODE -ne 0) { throw 'checkout failed' }; $h = (Get-FileHash -Algorithm SHA256 "$d/p215_struct_full_s0/teacher_plans_qwen25_coder_7b.jsonl").Hash.ToLower(); if ($h -ne '6f7d3a66c11ce931ed1185cf2a33c27c103c3dd137f7efa498a594e4062a1e43') { throw "sidecar hash still $h" }; git status --short -- $d; 'sidecar restored with LF' }
```

Then stop the GPU 0 worker (Ctrl+C) and start it again (Step 2, GPU 0). A
starting worker retries failed tasks and takes `fedcot_s0/srv_e1` first;
`dpo_r1` resumes later from its last checkpoint (every 25 updates). GPU 1 is
in use by another user (2026-11-09): do not start a worker on it, and do not
run other GPU jobs next to a task on GPU 0.

### vLLM sampling check (`vllm_s0/bench_sql`, first in the queue, 2026-11-09)

Sampling with HF takes 1.5-2.2 s per question (SQL-only) and about 20 s
with the query plan, too slow for full-data DPO rounds on one card. This task
samples the same 400 round-1 questions of client 3 as
`fedpref_s0/collect_r1_c3`, through vLLM in the WSL venv
(`/home/user01st/envs/env-vllm`), on the worker's GPU. A running worker picks
it up after its current task; nothing else to start.

Read in its log (lines prefixed `vllm |`):

- the vLLM memory lines at start (model weights, KV cache, CUDA graphs), and
  Windows `nvidia-smi` for GPU 0 while it samples: under 21.5 GiB, shared GPU
  memory near zero;
- `GPU check: one visible GPU on PCI bus 0x31`;
- `vllm sampled: ... s/request ... cut at max_tokens ...`;
- the final `sampled: 400/400 ... sample accuracy ..., pass@8 ...` line,
  against HF on the same questions: 13:52, sample accuracy 71.0%, pass@8
  88.5%.

Code pushed with this task: `--engine` in `experiments/federated_pref/run.py`
(default `hf`, unchanged behavior and sample identity).

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

`vllm_s0/bench_sql` (minutes), `srv_e1` (about 1.3 h), `srv_e2` (about
2.6 h), the query-plan smoke, the two server evaluations (about 1.4-2.6 h
each): decision 1 after about 8-9 h. GPU 1 is in use by another user.
