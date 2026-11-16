# FedLS-SQL: run queue

## Status

Updated 2026-11-16 at 16:00 (Asia/Ho_Chi_Minh). Last published result:
`cd8d0e8b` (14:42 on 2026-11-16: the comment check of the `codes` line).
Server work uses drive D only (owner, 2026-11-15): every command below
sets `TEMP` and `TMP` to `D:\phungthan\fediclkd\tmp`.

Queue change pushed at 16:00 on 2026-11-16 (`a7458d47`): new order below,
no code change. The worker takes it at its next publish step; nothing has
to finish first and the worker is not restarted.

| GPU | State | Known from |
|---|---|---|
| 0 | Row 2: `curve_hinton_sft` finished its 3 rounds at 14:35 and the first comment check was published at 14:42 on 2026-11-16. Next in queue order is `sqlcodes_s0/curve_hinton` (DPO round 1); whether the worker is on it is not confirmed since 14:42. | results commit `cd8d0e8b`, 14:42 on 2026-11-16 |
| 1 | Not ours: in use by another user. No worker or job to start. | owner, 2026-11-09 |

Read-only status on the server, from the `fedicl-sql` root:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.curve status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

## Run now

1. Read-only, seconds, CPU: check that the seed 0 gold server stage is on
   the server (the start of the gold control of row 2, used only if that
   control is run).

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -c "import json; from fedicl_sql.federated.stage_chain import resolve_parent; p = resolve_parent('experiments/federated/results/federated_stage__K2ce__s0__91bc5cfdd49b__ac34d6f9'); r = json.load(open('experiments/federated/results/federated_stage__K2ce-A__s0__73ae8d88b3a7__4ea78f9f/metrics.json', encoding='utf-8'))['parent']['adapter']['files']; assert p['adapter']['files'] == r, 'gold server stage adapter differs from the start of gold_k2aaa_a1'; print('ok', p['adapter']['path'])"; if ($LASTEXITCODE -ne 0) { throw 'Gold server stage check failed: send the output to the agent' } }
```

   Send back: the `ok` line or the error.

2. Only if no worker runs on GPU 0 (its window shows `STOP queue` or
   `DONE queue`, or was closed): start it. It skips finished work.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

Send back, when it appears in the worker window: any `STOP queue` line.

Next owner action:

- After each DPO round of `sqlcodes_s0/curve_hinton` (about 18:00 and
  21:00 on 2026-11-16, 00:15 on 2026-11-17): the round on Spider test
  against 76.62 / 77.18 / 77.36 without the server stage.
- After `sqlcodes_s0/publish_cmt_hinton` (about 01:00 on 2026-11-17), in
  the morning of 2026-11-17: read row 2 with the agent and say whether the
  gold control runs (17.5 h, `codes`, placed in front of whatever has not
  started). The queue does not wait for this: rows 3 and 4 follow row 2.
- After row 3 (about 04:30 on 2026-11-17): the rejected-type pilots.
- After row 4 (about 11:00 on 2026-11-17): FedAvg R3 with `codes_v2`
  against 73.17 (`codes`) and 73.45 (`codes` with comments).
- After row 5 (about 20:00 on 2026-11-17 without the gold control, about
  13:30 on 2026-11-18 with it): the method decision (server stage, teacher
  or gold, prompt). F1 is queued after it.

## Running and queued

GPU 0 in queue order. Durations are estimates; start times and current
progress need the status command above.

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 2 | `sqlcodes_s0/check_server_stage`, `curve_hinton_sft`, `curve_hinton`, `rob_hinton_a3`, `rob_hinton_dpo_r3`, `publish_rob_hinton` | Does the public stage add to the `codes` line? From the seed 0 Hinton server stage (BIRD, trained with `full` prompts, not retrained): 3 FedAvg SFT rounds and 3 DPO + NLL rounds with `codes` prompts at the clients, each round on Spider test; then both R3 adapters on Spider dev, DK, Realistic and SYN. Comparators: FedAvg R3 73.17, DPO rounds 76.62 / 77.18 / 77.36 | 10 h left | the 3 FedAvg rounds are done (73.27 / 75.64 / 75.78); DPO round 1 is next since 14:42 on 2026-11-16 |
| 2b | `sqlcodes_s0/cmt_hinton_a3`, `cmt_hinton_dpo_r3`, `publish_cmt_hinton` (after row 2) | How much the missing comments on Spider test cost for the Hinton line: its two R3 adapters evaluated with `codes_cmt` (same text, comments from `test_tables.json`). Comparators: its own `codes` rows | 4 min each | queued |
| 3 | `sqldpo_s0/pilot_rejected_exec`, `pilot_rejected_wrong` | Which rejected side DPO learns from: round 1 from `hinton_k2aaa_a3` on the round 1 samples of the Hinton line (`full`), rejected only samples that fail to execute, or only samples with a wrong result. Comparator: DPO round 1, 75.69 | 3.5 h | queued |
| 4 | `sqlcv2_s0/curve_fedavg_sft` | Does the corrected prompt hold the `codes` line? 3 FedAvg SFT rounds from the base model with `codes_v2` in every prompt, each round on Spider test. Comparators: 69.03 / 71.91 / 73.17 (`codes`), 73.45 (`codes` with comments at evaluation) | 6.5 h | queued |
| 5 | `sqlcv2_s0/curve_fedavg` | The core with the corrected prompt: 3 DPO + NLL rounds from that R3. Comparators: 76.62 / 77.18 / 77.36 (`codes`), 77.55 with comments | 9 h | queued |
| 6 | `sqldpo_s0/eval_fedprox`, `eval_fedntd`, `eval_localsft_c1` to `c5`, `publish_baselines`, `curve_central`, `extra_central_r3`, `publish_central_extra` | Standard FL baselines on the same engine; centralized DPO on pooled client rows, 3 rounds (`full`). Runs only while the method decision is open | 7.75 h | queued |
| 7 | `srvdpo_s0/check_bird`, `bird_round`, `publish_bird_round`, `eval_bird_round`, `clients_round`, `publish_clients_round`, `eval_clients_round`, `publish_eval` | Server DPO gate (`full`): one DPO + NLL round at the server on BIRD train (9,428 rows as one pooled client) from seed 0 FedAvg R3, then one client round like round 1 of `sqldpo_s0/fedavg` from that adapter; both on Spider test and BIRD dev. Comparators: FedAvg R3 71.26, DPO round 1 74.29, round 2 75.17 | 14.5 h | queued |

Rows 2-5 take about 29 h from 14:45 on 2026-11-16 (to about 20:00 on
2026-11-17); rows 6-7 about 22 h more. Row 4 is a new prompt style in
training: its first batch and the peak reserved of round 1 are the memory
check (prompts are shorter than `codes`: mean 880 tokens, longest 6,444).
The row 7 estimate is the least certain (derivation in `LAB_LOG.md`).

Cut from a full run:

- Row 2 starts from a server stage trained with `full` prompts on BIRD
  while the clients use `codes`: a server stage with `codes` is not trained
  (see below). A gain in row 2 holds for the method as it would be run; no
  gain leaves a server stage with `codes` prompts untested.
- Row 2 is seed 0, Hinton only. Its gold control (the same line from the
  seed 0 gold server stage, which separates the teacher from the public
  data) is not queued: the owner decides after reading row 2.
- Row 3 is one round, seed 0, `full`, on reused samples, like the other
  pilots of the Hinton line.
- Rows 4 and 5 are seed 0, from the base model only; the line from the
  server stage with `codes_v2` is not queued.
- Row 6 uses the `full` schema: the baselines with `codes` or `codes_v2`
  (FedProx, FedNTD, local SFT, centralized SFT and DPO) need new training
  and are not queued.
- Row 7 is seed 0, one server round and one client round (a gate), with
  `full` prompts so that it pairs with the committed `full` DPO rounds and
  BIRD prompts stay under 7,680 tokens. The 7B teacher is not used.
- The teacher with `codes` has no BIRD dev row (its `european_football_2`
  prompts reach 26,509 tokens with the answer budget).

Not queued yet:

- The gold control of row 2 (owner, 2026-11-16: the earlier seed 0 gold
  server-stage adapter is approved as its start): 3 FedAvg SFT rounds and
  3 DPO + NLL rounds with `codes` at the clients, about 17.5 h. Added in
  front of the tasks not started when the owner asks for it.
- F1, 20 clients (about 35 h with its server-stage half, about 17.5 h
  without; 10 of 20 clients per round about 19 h more): after the method
  decision, with the chosen prompt. Its curves stay defined in the queue
  file; its tasks are out of the task list.
- A server stage with `codes_v2` prompts (gold or Hinton on BIRD): the
  length of the BIRD train prompts is not measured (BIRD dev: longest
  4,988 tokens) and Hinton needs a new teacher logit cache. At least about
  20 h. Decided after row 2.
- The baselines with `codes` and seed 1 of the final method: after the
  method is fixed.
- A KD step between DPO rounds, a plan task, teacher SQL as the target,
  weight merging, SynSQL in place of BIRD at the same size: not
  recommended by the earlier rows in `LAB_LOG.md` (2026-11-16).
- DPO with result-vote labels for 3 rounds from `hinton_k2aaa_a3` (about
  3.5 h), approved for after P1.
- S1, a second non-IID split (about 21 h); S3, a second student size
  (about 15-20 h), both awaiting the owner's decision.
- M5, CPU/manual analyses; S2, K/beta sensitivity (one round, about 7 h);
  S4, FedProx seeds 1-2 (about 10 h); L1, 3 local DPO rounds (about 6 h,
  new code); B1, a second client benchmark (not measured): not approved.

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
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest" tests/test_task_queue.py tests/test_dpo.py tests/test_reuse_samples.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py tests/test_train_length_probe.py tests/test_curve.py tests/test_compare_predictions.py tests/test_eval_arms_config.py tests/test_exec_select.py tests/test_preference_labels.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
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
| SQL DPO from FedAvg R3 | control: no server stage |
| SQL DPO from `gold_k2aaa_a3` | control: server stage without the teacher |
| SQL DPO from `virtual_k2aaa_a3` | control: soft targets without the teacher (seed 0) |
| `virtual_k2aaa_a3`, `self_k2aaa_a3` | server stage with soft targets from no teacher, or from the student itself, then FedAvg (seed 0) |
| NLL-only round, extra FedAvg SFT rounds from `hinton_k2aaa_a3` | controls: no preference term, SFT at the same compute |
| SQL DPO from `hinton_k2aaa_a3` | the method so far (round 3: 76.71 on seed 0, 77.04 on seed 1); the server stage and its loss wait for the owner's decision |
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
| `sqlcodes_s0/hinton` | round 3 of `hinton_sft` | DPO + NLL round with `codes`; 3 rounds (`sqlcodes_dpo_hinton_r{k}_vllm_inproc`) |

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

### The corrected prompt (phase `sqlcv2_s0`)

The line of `sqlcodes_s0` from the base model with `codes_v2` in every
training, sampling and evaluation prompt; the recipe is otherwise the
same. Outputs: `artifacts/protocol_v2/sqlcv2_coder15b_alpha01_s0/`.

| Line (curve) | Start | Step | Arms (Spider test) |
|---|---|---|---|
| `sqlcv2_s0/fedavg_sft` | base model | one FedAvg round (lr 2e-4, 1 local epoch); 3 rounds | `sqlcv2_fedavg_r{k}_vllm_inproc` |
| `sqlcv2_s0/fedavg` | round 3 of `fedavg_sft` | DPO + NLL round, the settings of `sqldpo_s0/fedavg`; 3 rounds | `sqlcv2_dpo_fedavg_r{k}_vllm_inproc` |

### F1, 20 clients (phase `f1_s0`, not in the task list)

Split `processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k20`
(committed): the `k5` procedure with 20 clients over the same 8,659 rows.
The recipe of the `codes` line (P1) otherwise: `codes` prompts at the
clients, `--max-len 7680`. Outputs:
`artifacts/protocol_v2/f1k20_coder15b_alpha01_s0/`.

| Line (curve) | Start | Step | Arms (Spider test) |
|---|---|---|---|
| `f1_s0/fedavg_sft` | base model | one FedAvg round, every client; 3 rounds | `f1_fedavg_r{k}_vllm_inproc` |
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
