# FedLS-SQL: run queue

## Status

Updated 2026-11-16 at 23:50 (Asia/Ho_Chi_Minh). Last published result:
`e141d031` (23:41 on 2026-11-16: the DPO round with samples drawn without
the repetition penalty). Server work uses drive D only (owner,
2026-11-15): every command below sets `TEMP` and `TMP` to
`D:\phungthan\fediclkd\tmp`.

Pushed at 23:44 (`236479aa`, `e4f54e3a`): the evaluation option
`--oracle-tables` and the tasks of row 3 below. `experiments/eval_arms/run.py`
changed; without the option its prompts and result keys are the same, so
the evaluations of the running lines are not affected and nothing has to
finish first. The worker takes the new queue at its next publish task
(`synth_s0/publish_build`); no restart.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker on the queue below, most likely in row 1, `synth_s0/build`, since about 23:41 (not confirmed). | results commit `e141d031`, 23:41 on 2026-11-16 |
| 1 | Not ours: in use by another user. No worker or job to start. | owner, 2026-11-09 |

Read-only status on the server, from the `fedicl-sql` root:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.curve status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

## Run now

Nothing to run. The worker continues on its own; send back any
`STOP queue` line when it appears.

Next owner action (clock times are estimates from a start of row 2 at
about 00:05 on 2026-11-17):

- After row 3 (about 07:25 on 2026-11-17), in the morning: FedAvg R3 with
  `codes_v2` (row 2) and the two short reads of row 3. They decide
  whether the DPO rounds of row 4 continue or a table-selection step is
  tried first (`LAB_LOG.md`, 2026-11-16, method debate). Row 4 starts on
  its own after row 3; stopping it is Ctrl+C on the worker and loses at
  most the step in progress.
- After row 4 (about 16:25 on 2026-11-17): the core with `codes_v2`
  without the penalty.
- After row 8 (about 00:25 on 2026-11-18): the vote label check and the
  two mechanism pilots, then the decision on the mechanism
  (`RESEARCH_STATE.md` section 5, item 9).
- After row 9 (about 07:25 on 2026-11-18) and row 10 (about 14:00 on
  2026-11-18): centralized SFT, FedAvg with 20 clients.

## Running and queued

GPU 0 in queue order. Durations are
estimates. "Without the penalty" means `--repetition-penalty 1.0`; every
row published so far was decoded with 1.1.

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `synth_s0/build`, `publish_build` | The synthetic rows written without the penalty: per client 1,200 SQL queries refilled on its own databases, a question for each by the base model; a new root | 0.2 h | running (most likely) |
| 2 | `sqlcv2_s0/curve_fedavg_sft` | Does the corrected prompt hold the `codes` line? 3 FedAvg SFT rounds from the base model with `codes_v2`, each round on Spider test without the penalty. Comparator: FedAvg R3 with `codes` without the penalty, 74.71 | 6.5 h | queued |
| 3 | `gate_s0/*` (5 control evaluations, 3 oracle evaluations, 2 publish tasks) | Two short reads, evaluation only. (1) Does a DPO round still beat one more SFT round at the same decoding? `hinton_k2aaa_a3`, its DPO round 1, its NLL-only round and its two extra SFT rounds, `full` prompts, without the penalty (with it: 73.31, 75.69, 73.50, 74.15, 72.99). (2) How much would a perfect table-selection step give? FedAvg R3 and DPO round 3 of the `codes` line and the base model (`codes_v2`) with the schema cut to the tables of the gold SQL, arms `*_oracletab_*`; comparators 74.71, 77.04, 65.72. A diagnostic, never a result | 0.8 h | queued |
| 4 | `sqlcv2_s0/curve_fedavg` | The core with the corrected prompt and no penalty: 3 DPO + NLL rounds from that R3 | 9 h | queued |
| 5 | `vote_s0/check`, `xsel_dpo_r3` and their publish tasks | Two short reads of the line of row 4. (1) How often does a vote over a question's 8 samples agree with the gold labels, and how many vote-labelled pairs are right? Samples of DPO rounds 1-3, CPU, no training: the first number for clients with few labelled questions. (2) Selection by execution over 8 samples of DPO round 3 on Spider test: the vote and pass@8 without the penalty | 0.5 h | queued |
| 6 | `peer_s0/check`, `publish_check` | The peer adapter check on the line of row 4, at its DPO round 3. No training | 0.5 h | queued |
| 7 | `synth_s0/round_synth`, `eval_synth` and their publish tasks | Do synthetic questions give the DPO loop new pairs that help? One DPO + NLL round from DPO round 3 of row 4 on the split of row 2. Arm `sqlsyn_dpo_fedavg_r4_np_vllm_inproc`. Comparator: row 8 | 4 h | queued |
| 8 | `synth_s0/round_plain`, `eval_plain` and their publish tasks | The same round without synthetic rows: round 4 of the line of row 4. Arm `sqlcv2_dpo_fedavg_r4_np_vllm_inproc` | 3 h | queued |
| 9 | `sqlcv2_s0/central_e3`, `eval_central`, `publish_central` | How far FedAvg SFT is from training on the pooled rows: centralized SFT on the 8,659 Spider train rows, 3 epochs, `codes_v2`, then epoch 3 on Spider test without the penalty. Comparator: FedAvg R3 of row 3 | 7 h | queued |
| 10 | `f1_s0/curve_fedavg_sft` | Does FedAvg hold with 20 clients? 3 FedAvg SFT rounds on the `k20` split, `codes` prompts, each round on Spider test without the penalty. Comparator: 74.71 (5 clients, `codes`, without the penalty) | 6.5 h | queued |

Rows 1-10 take about 38 h. Rows 1, 3 and 5-8 run code that has not run
on the server in this form (the synthetic rows without the penalty, the
oracle prompts, the vote label check, the pilots on a new line); the
time of the vote label check is not measured. Row 2 is a new prompt
style in training: its first batch and the peak reserved of round 1 are
the memory check (prompts are shorter than `codes`: mean 880 tokens,
longest 6,444). Row 7 samples up to about 14,200 questions instead of
8,659.

Cut from a full run:

- Every row is seed 0.
- Six existing rows are evaluated without the penalty (`LAB_LOG.md`), and
  row 3 adds five of the Hinton line. The other committed rows (the rest
  of the Hinton line, the gold line, seed 1, the other test sets,
  FedProx, FedNTD, centralized) are not; each is about 6 min and needs no
  training.
- Row 3, part 1, reads the existing control adapters again; a fair
  control of three SFT rounds against three DPO rounds on the `codes_v2`
  line (about 6.5 h) is not queued. Part 2 is an upper bound with the gold
  tables; the step itself (a round that also learns to list tables, about
  3 to 4 h, new code) is not queued.
- The 3-round DPO line without the penalty is row 4, on `codes_v2`; the
  `codes` line has one such round (76.94, `LAB_LOG.md`).
- Row 5 counts label agreement only; a DPO line trained on vote labels
  with few labelled questions per client (about 6 h) is not queued.
- Row 6 measures candidates only; training with a peer sample as the
  chosen side (one round, about 3 h) is not queued.
- Rows 7 and 8 are one round each. Row 7 has more pairs than row 8, so
  the two compare the whole step, not equal update counts; a control with
  equal pair counts (about 3 h) is not queued.
- Row 9 is centralized SFT only. Centralized DPO with `codes_v2` (3 rounds
  on the pooled rows, about 9 h) is not queued.
- Row 10 is the FedAvg SFT half of F1 and uses `codes`, as its curve is
  defined, not `codes_v2`. It shows whether FedAvg holds with 20 clients
  and says nothing about the DPO rounds with 20 clients (about 11 h) or
  about 10 of 20 clients per round (about 19 h); neither is queued.

Not queued yet:

- The mechanism pilots on the `codes` line with the penalty: the peer
  check and the synthetic rows are published; the DPO round with
  synthetic questions was stopped at the restart and its plain
  comparator did not start. Both rounds now run on the line of row 4.
- Other mechanism candidates (`RESEARCH_STATE.md` section 5, item 9):
  clients with few labelled questions and vote labels for the rest (about
  6 h, changes the setup); a hint for questions no sample solves; a CPU
  count of samples that pass by accident, on mutated databases. Not
  approved.
- Out of the queue since 2026-11-16 (owner: the teacher and the public
  stage leave the core): the DPO rounds of the `codes` line from the
  Hinton server stage (stopped in round 1) and its gold control, a server
  stage with `codes_v2`, the server DPO gate on BIRD, the server-stage
  half of F1. Putting one back is a queue edit; the stopped line resumes
  by running its curve again.
- Reference rows with `full` that had not run: the 5 local client models,
  centralized DPO. The baselines with `codes_v2` (FedProx, FedNTD, local
  SFT) and seed 1 of the final method come after the method is fixed.
- DPO with result-vote labels for 3 rounds (about 5 h): approved
  earlier from `hinton_k2aaa_a3`; its start would now be the `codes_v2`
  line, to confirm with the owner.
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
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest" tests/test_task_queue.py tests/test_dpo.py tests/test_reuse_samples.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py tests/test_utils_files.py tests/test_vllm_student.py tests/test_train_length_probe.py tests/test_curve.py tests/test_compare_predictions.py tests/test_eval_arms_config.py tests/test_exec_select.py tests/test_preference_labels.py tests/test_synthesis.py tests/test_peer_check.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
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

### The mechanism pilots (phases `vote_s0`, `peer_s0`, `synth_s0`)

On the `codes_v2` line without the penalty, seed 0
(`artifacts/protocol_v2/sqlcv2_coder15b_alpha01_s0/`), after its DPO
rounds.

- `vote_s0/check` (`scripts/vote_label_check.py`): reads the samples of
  rounds 1-3 under the root's `samples` folder, labels them again by a
  vote over execution results and compares with the recorded gold labels.
  Results: `experiments/vote_check/results/cv2_dpo_np/` (`summary.json`,
  `per_question.csv`); working files under
  `artifacts/protocol_v2/vote_check/cv2_dpo_np/`.
- `vote_s0/xsel_dpo_r3` (`scripts/exec_select.py`): results under
  `experiments/exec_select/results/xsel_cv2_dpo_r3_np_s0_spider_test/`.
- `peer_s0/check` (`scripts/peer_check.py`): reads the round 3 samples of
  the line, takes the questions with all samples wrong, and samples them
  again through vLLM, one run per adapter: each other client's round 2
  adapter (8 samples) and the round 2 global adapter (32 samples).
  Results: `experiments/peer_check/results/cv2_dpo_r3_np/`; working files
  under `artifacts/protocol_v2/peer_check/cv2_dpo_r3_np/`. The check of
  the `codes` line with the penalty is `codes_dpo_r3`.
- `synth_s0/build` (`scripts/synth_questions.py`): writes the new split
  to `artifacts/protocol_v2/sqlsynnp_coder15b_alpha01_s0/synth/split` and
  the evidence to `audits/protocol_v2/sqlsynnp_coder15b_alpha01_s0/synth/`.
  Synthetic rows have ids `syn:c<client>:<n>`. The build with the penalty
  is under `sqlsyn_coder15b_alpha01_s0` and stays as it is.
- `synth_s0/round_synth`: root
  `artifacts/protocol_v2/sqlsynnp_coder15b_alpha01_s0/dpo_synth`, round 1
  from the round 3 global adapter of the line, with
  `--no-fallback-prefix syn:`. Its pair statistics carry the counts of
  synthetic questions by number of correct samples (`label_only_*`).
- `synth_s0/round_plain`: round 4 in the root of the line; rounds 1-3 and
  the record of the curve are not touched.

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
