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
runs the full queue; add `--phase fedpref_s0` (or `cotprobe_s0`, or both) to
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
- `cotprobe_s0/srv_*` (BIRD-length rows): peak reserved on the first steps,
  about 20 GiB expected.
- Shared GPU memory of each task's process stays near zero.

## Queue content

### Federated DPO + NLL from FedAvg R3 (phase `fedpref_s0`, 18 tasks)

What it tests: starting from the FedAvg R3 adapter (owner-approved reuse, run
`p227_fl_aaa_s0`: Spider dev 67.60), does one or two rounds of federated
on-policy DPO + NLL raise Spider dev EX, and by more than the same rounds with
the DPO term removed (RFT control) and more than one more FedAvg SFT round?

Each round, per client: 400 of its questions (a new random subset per round),
8 sampled SQL per question at T=0.7 (the earlier SQL-only DPO rounds), labels
by execution against the client's own gold with the evaluator itself (60 s
per query); only samples that end with EOS count. Up to 2 pairs per question,
the most similar correct and wrong SQL first, no sample used twice; when no
sample is correct, gold is the chosen side. 2 local epochs of LoRA DPO + NLL
(beta 0.1, lr 1e-5, the earlier schedule), FedAvg weighted by pair count. The
RFT arm trains on the same pairs with only the NLL term. Round 1 samples are
shared by both arms; in round 2 each arm samples from its own round 1
adapter.

Tasks: the smoke (8 questions per client, its own output root); round 1
sampling per client; one task per arm and round (pairs, local training,
FedAvg; in round 2 also the sampling); one evaluation per arm on Spider dev
and BIRD dev; the SFT round 4 control (same settings as the approved FedAvg
run, warm-started from its R3 row) and its evaluation; `publish_r1` once
round 1 is evaluated, `publish` at the end.

Evaluation uses `scripts.eval_standard`: the contract of the FedAvg reference
rows (zero-shot SQL-only prompt, greedy 256 tokens, batch 16), on Spider dev
and BIRD dev. Spider test is not used.

### Headroom check and CoT probe from FedAvg R3 (phase `cotprobe_s0`, 11 tasks)

What it tests (`DIRECTION.md` section 6.3, steps 0 and 1a):

- How far the 7B teacher (4-bit, SQL-only, greedy) is above R3 on Spider
  dev, and R3's sampled pass@8 there (K=8, T=0.7, the round-1 sampling). If
  the teacher is less than about 4 points above R3, the KD options stop;
  pass@8 minus greedy is the ceiling of client DPO/RFT.
- Whether the 1.5B student can use query-plan CoT (`qp_cot_v1`), whether the
  teacher's plans add anything over plans derived from the SQL, and whether
  clients' gold-derived plans beat SQL-only.

Arms, all from the R3 adapter, one pass each:

| Arm | Training | Eval mode |
|---|---|---|
| `cotprobe_srv_teacher` | server SFT on the 4,109 BIRD rows: teacher plan + teacher SQL | `qp_cot_v1` |
| `cotprobe_srv_ast` | same rows: plan derived from the SQL + the same SQL | `qp_cot_v1` |
| `cotprobe_srv_ce` | same rows: SQL only | SQL-only |
| `cotprobe_t0` | one FedAvg round on the clients' Spider rows with plans derived from their gold SQL | `qp_cot_v1` |

The teacher SQL of these rows matches BIRD gold on execution, so the three
server arms differ only in the plan. `cotprobe_t0` is compared with
`fedpref_sft_r4`, the same round in SQL-only. Evaluation is Spider dev only;
CoT evaluation uses 1,024 new tokens and strict parsing.
`cotprobe_s0/publish` commits the results at the end.

### Priority order

The teacher evaluation (about 15 min) runs next to the smoke. The DPO/RFT
chain comes first, with round 1 evaluated before round 2 starts sampling;
pass@8, the SFT round 4 control and the CoT probe fill whichever GPU has
nothing ready on the chain. Estimated total: 25-30 GPU-hours, about 13-15 h
on both cards.

## Local, after publication: test-suite EX on Spider dev (CPU, Mac)

Rescores every published dev prediction file against the official test-suite
databases (`scripts/score_test_suite.py`); run by the agent after pulling.
