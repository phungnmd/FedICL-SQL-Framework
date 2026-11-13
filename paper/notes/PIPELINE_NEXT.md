# FedLS-SQL: run queue

Status: what is running. Run now: what the owner does. Running and queued:
what the worker does by itself. Reference: not needed to act. History and
reasons are in `LAB_LOG.md`.

## Status

Updated 2026-11-13, 16:30.

| GPU | State | Known from |
|---|---|---|
| 0 | Idle, waiting for the owner: the queue is empty. The last task (`publish_self`) published at 15:25 on 11-13; the worker should have printed `DONE queue` (not observed). | results commit `c09d1aad` |
| 1 | Not ours: in use by another user. No worker, no job. | owner, 2026-11-09 |

Live state, read-only, any terminal on the server (`fedicl-sql` root): the
tasks, then EX by step of every curve.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.curve status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

## Run now

Nothing to run. The owner is needed now, for two choices (results in
`LAB_LOG.md`, 2026-11-13): whether the teacher stays in the method, and
what GPU 0 runs next (list below). Once chosen, the agent queues it and
writes the pull and start commands here.

## Running and queued

Nothing running or queued on GPU 0.

Cut from a full run (finished work):

- The row without the NLL term is 1 round on seed 0 and reuses the round 1
  samples of the Hinton line (no sampling): it answers round 1 only.
- Seed 1 has the three DPO lines only. The controls of seed 0 (NLL-only
  round, extra SFT rounds, focused DPO, random pairs, no NLL, round 4, the
  soft-target lines) are not repeated.
- On Spider dev, Realistic, SYN, DK and BIRD dev, seed 1 and the virtual
  line have the start and round 3 of each line, not rounds 1 and 2.
- The soft-target control is seed 0 only, from an earlier adapter
  (`virtual_k2aaa_a3`); the self-teacher start is evaluated only, without
  DPO.

Not queued yet (each waits for the owner):

- DPO without the NLL term, rounds 1-3 with their own sampling, seed 0
  (about 5.5 h): whether the term matters after round 1.
- A third seed of the three lines (about 30 h, with two server stages).
- The soft-target control on seed 1: server stage, 3 FedAvg rounds, 3 DPO
  rounds (about 15.5 h).
- FedProx, FedNTD and the local client models through vLLM inproc: whether
  their adapters are still on the server is not checked.
- DPO on pooled client data and DPO without aggregation (reference rows,
  about 5.5 to 6 h each).
- Focused DPO rounds 2 and 3 (about 3.75 h): round 1 did not lower the
  wrong results.

## Reference

### Restart the worker

All commands run from the `fedicl-sql` root on the server. Ctrl+C stops the
worker and its running task; the start command continues where it stopped
and skips finished work. A failed task stops the worker with
`STOP queue: <task> failed: <last error line>` and the log path; rerunning
retries it. If a task fails again with `CUDA error: unspecified launch
failure`, send the last lines of its log to the agent before a third try.

Pull and run the tests (needed only after a push to fedicl-sql; pulling
while the worker runs is fine):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_task_queue.py tests/test_dpo.py tests/test_reuse_samples.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py tests/test_train_length_probe.py tests/test_curve.py tests/test_compare_predictions.py tests/test_eval_arms_config.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
```

Worker on GPU 0:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

Worker on GPU 1 (not now: the card is in use by another user):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

Worker check, about 1 min, once per server setup (`selftest` phase; with two
cards run it on both, each prints its own card and sleeps 30 s):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run --no-sync python -m scripts.gpu_worker run --gpu 0 --phase selftest; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
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
| `sqldpo_s0/nonll_hinton` (finished, 1 round) | `hinton_k2aaa_a3` | the round 1 samples of the Hinton line | the same pairs (nearest) | 1 round, the preference term only (NLL weight 0), same schedule and updates as DPO round 1 |
| `sqldpo_s0/sft_hinton` | `hinton_k2aaa_a3` | each client's Spider rows, gold SQL | none | 2 more FedAvg SFT rounds (lr 2e-4, 1 local epoch) |

SQL DPO runs 3 rounds, fixed for every line and seed, and is reported at
round 3 (owner, 2026-11-10; chosen on Spider test, seed 0). Each line is a
curve (`scripts/curve.py`): it trains a step, evaluates it, publishes, and
records the result in `audits/curves/`. Reused adapters:
`fedicl-sql/docs/SERVER_STORAGE.md` section 5.

Final table (Spider test; every SQL DPO line at round 3):

| Row | Line |
|---|---|
| base, local clients, FedProx, FedNTD | reference rows |
| FedAvg R3 | from the base model |
| centralized Spider, centralized Spider + BIRD | references without privacy |
| `gold_k2aaa_a3`, `hinton_k2aaa_a3` | server stage on BIRD, then FedAvg |
| SQL DPO from FedAvg R3 | control: no server stage |
| SQL DPO from `gold_k2aaa_a3` | control: server stage without the teacher |
| SQL DPO from `virtual_k2aaa_a3` | control: soft targets without the teacher (seed 0) |
| `virtual_k2aaa_a3`, `self_k2aaa_a3` | server stage with soft targets from no teacher, or from the student itself, then FedAvg (seed 0) |
| NLL-only round, extra FedAvg SFT rounds from `hinton_k2aaa_a3` | controls: no preference term, SFT at the same compute |
| SQL DPO from `hinton_k2aaa_a3` | the method so far (round 3: 76.71 on seed 0, 77.04 on seed 1); the server stage and its loss wait for the owner's decision |
| CoT (short analysis) | E5, template R1, self-taught R1-R3 |

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
