# FedLS-SQL: run queue

## Status

Updated 2026-11-16 at 01:33 (Asia/Ho_Chi_Minh). Last published result:
`44bbc0f5` (P1 DPO rounds 1-3 with the `codes` schema, Spider test: 76.62,
77.18, 77.36); no newer results commit. Server work uses drive D only
(owner, 2026-11-15): every command below sets `TEMP` and `TMP` to
`D:\phungthan\fediclkd\tmp`.

| GPU | State | Known from |
|---|---|---|
| 0 | `sqlcodes_s0/curve_fedavg` finished at 23:57 on 2026-11-15. Whether the worker is still running is not confirmed; if it is, it took `sqldpo_s0/check_baselines` next and may be in `sqldpo_s0/eval_teacher`. | results commit `44bbc0f5`, 23:57 on 2026-11-15 |
| 1 | Not ours: in use by another user. No worker or job to start. | owner, 2026-11-09 |

Read-only status on the server, from the `fedicl-sql` root:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.curve status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

## Run now

1. Pull the queue, the 20-client split and the code changes: evaluation
   prompts are built once per question, selection by execution takes
   `--schema-style`, DPO rounds take `--start-adapter` and
   `--rejected-kind`, and FedAvg and DPO rounds take `--clients-per-round`.
   A running worker keeps running: do not stop it. A running task finishes
   with the outputs it would have given. Every FedAvg, stage and DPO task
   started after the pull (and a later step of a running curve, such as
   `sqldpo_s0/curve_central`) loads the new code; without the new options
   it behaves as before and keeps the same identities. Run it in a second
   PowerShell window, from the `fedicl-sql` root, while the worker window
   does not show a `publish_` task running. The last lines list the
   `f1_s0` tasks, `waiting` or `ready`.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest" tests/test_task_queue.py tests/test_eval_standard.py tests/test_eval_arms_config.py tests/test_exec_select.py tests/test_curve.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_dpo.py tests/test_reuse_samples.py tests/test_round_loop.py tests/test_stage_chain.py tests/test_participation.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' }; uv run --no-sync python -m scripts.gpu_worker status --phase f1_s0; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

2. Only if no worker runs on GPU 0 (its window shows `STOP queue` or
   `DONE queue`, or was closed): start it. It skips finished work and takes
   row 1 of the table below first.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
```

Send back: the last lines of step 1 and whether the worker was running.
Then, when they appear in the worker window:

- `sqlcodes_s0/eval_teacher_codes`, the first 7B run through vLLM: its
  `vllm | ... KV cache ...` and `Maximum concurrency` lines and its first
  progress line.
- `sqlcodes_s0/bird_fedavg_r3`: the lines from `=== arm` to its first
  progress line. After `=== arm` it prints nothing for about 50 min
  (measured on a laptop CPU; the server may differ) while it builds the
  1,534 BIRD prompts (each question scans the text values of its
  database); it is not stuck. The vLLM lines then show a context of
  26,509 tokens (the longest prompt, `european_football_2`, plus 256). A
  silence of more than 2 h: send the lines.
- `srvdpo_s0/check_bird`: its last line, `ok: 9428 BIRD train rows, 69
  databases` or `MISSING BIRD train databases`.
- `srvdpo_s0/bird_round`: the sampling progress line after 10 min, and the
  DPO lines up to the first `peak reserved` (the first DPO run on BIRD
  rows, up to about 6,800 tokens a sequence).
- `f1_s0/check_server_stage`: its last line, `ok artifacts/protocol_v2/p237_phase_e_s0/hinton_k2aaa_k2/m_g`
  or the error.
- `f1_s0/curve_fedavg_sft`: the first `[client 1]` progress lines of round
  1 (20 clients of 165 to 1,015 rows, so about 1.7 h a round).
- Any `STOP queue` line.

Next owner action:

- After `sqlcodes_s0/publish_rob` (about 30 min after row 1 starts): read
  the `codes` rows on the four Spider sets with the agent; BIRD dev
  follows in row 3. The decision on `codes` waits on rows 1-3. F1 and the
  3-round vote-label line are queued after that decision.
- After `srvdpo_s0/publish_eval` (about 18 h after row 1 starts): read the
  server DPO gate with the agent.
- After `sqldpo_s0/pilot_rejected_wrong` (about 22 h after row 1 starts):
  read the rejected-type pilots with the agent.
- After `f1_s0/curve_hinton_sft` (about 33 h after row 1 starts): FedAvg
  and the Hinton line with 20 clients at R3; after `f1_s0/curve_hinton`
  (about 48 h): both after DPO. Read each with the agent.
- After row 10 (about 70 h after row 1 starts): partial participation, the
  baselines and centralized DPO.

## Running and queued

GPU 0 in queue order. Durations are estimates; start times and current
progress need the status command above.

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `sqlcodes_s0/rob_fedavg_r3`, `rob_dpo_r3`, `publish_rob` | Does `codes` beat `full` beyond Spider test: P1 FedAvg R3 and DPO round 3 on Spider dev, DK, Realistic and SYN, paired with the `full` rows of the same lines | 30 min | queued, first after the task the worker runs now |
| 2 | `sqlcodes_s0/eval_teacher_codes`, `xsel_dpo_r3`, `publish_teacher_xsel` | The 7B teacher zero-shot with `codes` prompts on Spider test and the four Spider sets (room for distillation with `codes`); greedy, fallback and vote over 8 samples on P1 DPO round 3, Spider test | 1 h 5 min | queued |
| 3 | `sqlcodes_s0/bird_fedavg_r3`, `bird_dpo_r3`, `publish_bird` | The same two P1 adapters on BIRD dev | 2.5 h | queued |
| 4 | `srvdpo_s0/check_bird`, `bird_round`, `publish_bird_round`, `eval_bird_round`, `clients_round`, `publish_clients_round`, `eval_clients_round`, `publish_eval` | Server DPO gate: one DPO + NLL round at the server on BIRD train with evidence (9,428 rows as one pooled client) from seed 0 FedAvg R3 (`full`), then one client round exactly like round 1 of `sqldpo_s0/fedavg` from that adapter; both on Spider test and BIRD dev. Comparators: FedAvg R3 71.26, DPO round 1 74.29, round 2 75.17 | 14.5 h | queued |
| 5 | `sqldpo_s0/pilot_rejected_exec`, `pilot_rejected_wrong` | Which rejected side DPO learns from: round 1 from `hinton_k2aaa_a3` on the round 1 samples of the Hinton line, rejected only samples that fail to execute, or only samples with a wrong result. Comparator: DPO round 1, 75.69 | 3.5 h | queued |
| 6 | `f1_s0/curve_fedavg_sft`, `check_server_stage`, `curve_hinton_sft` | F1, 20 clients, every client: 3 FedAvg SFT rounds from the base model, and from the seed 0 Hinton server stage (`p237_phase_e_s0/hinton_k2aaa_k2/m_g`, the start of `hinton_k2aaa_a3`); each round on Spider test. Does FedAvg fall behind centralized SFT (70.75) with 20 clients, and does the server stage gain more than with 5 (71.26 against 73.31)? | 11 h | queued |
| 7 | `f1_s0/curve_fedavg`, `curve_hinton` | F1, every client: 3 DPO + NLL rounds from each R3 (5-client rows: 75.13 and 76.71) | 14.5 h | queued |
| 8 | `f1_s0/curve_fedavg_sft_p10`, `curve_hinton_sft_p10`, `curve_fedavg_p10`, `curve_hinton_p10` | Rows 6-7 with 10 of the 20 clients per round | 14 h | queued |
| 9 | `sqldpo_s0/check_baselines`, `eval_teacher` | Teacher 7B zero-shot through vLLM bf16 with `full`, six sets (also the comparator of row 2) | 1 h | queued or running (not confirmed) |
| 10 | `sqldpo_s0/eval_fedprox`, `eval_fedntd`, `eval_localsft_c1` to `c5`, `publish_baselines`, `curve_central`, `extra_central_r3`, `publish_central_extra` | Standard FL baselines on the same engine; centralized DPO on pooled client rows, 3 rounds | 7.75 h | queued |

All rows total about 70 h. If the worker is in `eval_teacher` when the pull
lands, row 1 starts when that task ends and row 9 is then finished. The
row 4 estimate is the least certain (BIRD sampling, labelling and pair
count are not measured; derivation in `LAB_LOG.md`).

Cut from a full run:

- Rows 1-3 are seed 0 only (P1 has no seed 1): they pair with seed 0
  `full` rows only.
- Row 2: the teacher with `codes` skips BIRD dev. Its `european_football_2`
  prompts reach 26,509 tokens with the answer budget, close to what 0.80
  of the card leaves for the 7B cache, and each BIRD pass costs about
  50 min of prompt building;
  with the four Spider sets the row still answers whether the teacher
  gains from `codes`.
- Row 3: on BIRD dev the `codes` schema of `european_football_2` (129 of
  1,534 questions) carries 2 sample values of the XML columns of `Match`,
  up to 26,253 tokens against 7,680 in training; the rows are read with and
  without that database.
- Row 4 is seed 0, one server round and one client round (a gate, not the
  3-round line), from the `full` FedAvg R3 so that it pairs with the
  committed `full` DPO rounds; the server round uses `--max-len 7680`
  (the longest BIRD train row is 6,779 tokens in the committed token
  audit, so no row is dropped). The 7B teacher is not used.
- Row 5 is one round, seed 0, on reused samples, like the other pilots of
  the Hinton line.
- Rows 6-8 (F1) are seed 0, `full` schema: the Hinton server stage exists
  only with `full`, and a `codes` server stage is not trained.
- Row 8, partial participation: 10 of 20 clients per round, drawn by a
  fixed rule from (seed, round), separately for FedAvg and DPO rounds; over
  the 3 FedAvg rounds clients 1 and 18 never take part, over the 3 DPO
  rounds clients 7, 11 and 19.
- Centralized DPO is seed 0 only.
- The local SFT models are evaluated only on Spider test; six sets would
  add about 2.5 h. DPO without aggregation is not queued.
- Rows 4-10 use the `full` schema, like every row before P1.

Not queued yet:

- A server stage with `codes` (gold or Hinton on BIRD with `codes`, then 3
  FedAvg rounds and 3 DPO rounds with `codes`): at least about 20 h from
  committed timings (2 BIRD epochs at 2.7 h each with `full`, more with
  the longer `codes` prompts; 3 FedAvg rounds; 3 DPO rounds at about 3 h).
  Hinton needs a new teacher logit cache for `codes` prompts (cost not
  measured), and the `european_football_2` rows exceed 7,680 tokens. Waits
  on the `codes` decision.
- A KD step between DPO rounds: not recommended by the earlier rows in
  `LAB_LOG.md` (2026-11-16, server-stage variants).
- F1 with the gold server stage (the control without the teacher, about
  13 h with every client): needed only if the Hinton line gains with 20
  clients.
- F1 with `codes`: needs a `codes` server stage first.
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

### F1, 20 clients (phase `f1_s0`)

Split `processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k20`
(committed): the `k5` procedure with 20 clients over the same 8,659 rows.
Seed 0 recipe and `full` schema otherwise. Outputs:
`artifacts/protocol_v2/f1k20_coder15b_alpha01_s0/`.

| Line (curve) | Start | Step | Arms (Spider test) |
|---|---|---|---|
| `f1_s0/fedavg_sft` | base model | one FedAvg round, every client; 3 rounds | `f1_fedavg_r{k}_vllm_inproc` |
| `f1_s0/hinton_sft` | seed 0 Hinton server stage, row `federated_stage__K2fkl__s0__132e798a5be2__8393f0f9` | same | `f1_hinton_k2aaa_a{k}_vllm_inproc` |
| `f1_s0/fedavg`, `f1_s0/hinton` | round 3 of the line above | DPO + NLL round, the settings of `sqldpo_s0/fedavg`; 3 rounds | `f1dpo_fedavg_r{k}`, `f1dpo_hinton_r{k}` (`_vllm_inproc`) |
| `*_p10` | the same, `p10_` folders | the same with `--clients-per-round 10` | `f1p10...` |

Comparators (5 clients, seed 0, Spider test): FedAvg R3 71.26,
`hinton_k2aaa_a3` 73.31, DPO round 3 from each 75.13 and 76.71;
centralized Spider SFT `sql_central_e3_vllm_inproc` 70.75.

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
