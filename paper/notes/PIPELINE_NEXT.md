# FedLS-SQL: run queue

## Status

Updated 2026-11-18 00:55 (Asia/Ho_Chi_Minh). FedAvg rounds 1 to 3 and
their pass@k are published (EX 72.43, 74.10, 74.71; pass@10 88.36 and
88.68 for rounds 2 and 3). Running: the DPO + NLL round from FedAvg round
2 (`dpo_k2/round_1`, training since 23:21). Pushed (code `cb947362`, queue
only, nothing the running task loads): the FedAvg line stops at round 4,
then centralized SFT runs (`refs/central_sft`). No restart needed: the
worker rereads the queue before every task.

| GPU | State | Known from |
|---|---|---|
| 0 | `dpo_k2/round_1` (DPO training). | owner's console, 2026-11-17 23:25 |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Pull and run the tests, in a second PowerShell window without the GPU
   (about 5 min, estimate). Send back the pytest summary (453 passed on
   the Mac), or the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. Leave the worker running overnight. Expected order and times
   (estimates, Asia/Ho_Chi_Minh, 18 Nov): DPO round from FedAvg round 2
   and its evaluation about 01:30-01:45; the nearest-pair round about
   03:30-03:45; FedAvg round 4 about 05:50; then centralized SFT, about
   2 h 10 min per epoch with its evaluation, until its rule stops it
   (likely 3 to 5 epochs). If the worker stops, start it again:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   Send back:
   - the pair counts per client that the DPO round prints after
     sampling (all-correct, mixed, all-wrong questions, pairs);
   - in its first minutes of training: the peak reserved VRAM of the
     progress line and the shared GPU memory of the card in Task Manager
     (DPO with these prompts is not measured yet); then the time left;
   - the EX of both DPO rounds (random, nearest) and each `curve ... EX`
     line of FedAvg and of centralized SFT;
   - a `STOP queue` line, if one comes.

3. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `dpo_k2/round_1`, `dpo_k2/publish_round_1`, `dpo_k2/eval_1`, `dpo_k2/publish_eval_1` | the early read of the switch round: one DPO + NLL round from FedAvg round 2 (k = 2), against FedAvg round 3; pair counts at an SFT start | about 1.5-2.5 h (estimate) | queued, next |
| 2 | `dpo_k2_nearest/reuse_samples`, `dpo_k2_nearest/round_1`, `dpo_k2_nearest/publish_round_1`, `dpo_k2_nearest/eval_1`, `dpo_k2_nearest/publish_eval_1` | I2: the same round with each distinct wrong SQL paired with its most similar correct SQL (2 per question), on the samples of row 1; aims at the executable wrong results that SFT leaves at 373-379 | about 1-1.5 h, training only (estimate) | queued |
| 3 | `rounds/fedavg_sft` | FedAvg SFT from the base student on the 5 clients (`alpha_0.1/k5`), prompt A, one round at a time; every round evaluated on Spider test and published | about 2 h per round plus about 10 min of evaluation (measured round 1: 7,339 s + 206 s); 3 to 8 rounds | rounds 1-3 done (best 74.71 at round 3); round 4 is the last (owner, 2026-11-18) |
| 4 | `refs/central_sft` | centralized SFT on the union of the 5 clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | about 2 h 10 min per epoch (estimate) | queued |
| 5 | `dpo/after_fedavg` | DPO + NLL rounds from the best FedAvg round (k = best) (10 samples at T 1.0, 2 pairs per question, no pair from a database without rows), each round evaluated on Spider test and published | about 1.5-2.5 h per round (estimate); up to 6 rounds | queued |

How the rounds stop: a round is a gain when it beats the best round by
more than 0.5 EX point; a line stops after 2 rounds in a row without a
gain, or at 4 rounds (FedAvg), 8 epochs (centralized) or 6 rounds (DPO).
The control of a DPO line is FedAvg at the same total rounds; if a DPO
line runs past FedAvg round 4, a curve that extends FedAvg is queued then.

After the k = 2 reads: the line from k = 2 continues with the better pair
rule if it is at least 1 EX above FedAvg round 3 (74.71); the line from
the best round may be dropped if the pair counts at k = 2 already run
low; then k = 1 and k = 0 with gold; decided on the numbers.

Not queued: phase 2 (the published federated DPO baseline, RFT, DPO from
the base student (k = 0)) and phase 3 (BIRD, other splits, FedProx, FedNTD,
local rows, pre-training); `RESEARCH_STATE.md`, section
3.7.

## Reference

All commands run from the `fedicl-sql` root on the server, as one
PowerShell line, and put temp files on drive D (`TEMP`, `TMP`, pytest
`--basetemp`); drive C is not used.

Read-only status of the queue:

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

GPU work runs through one queue file, `fedicl-sql/queues/active.toml`:
every task (one command), what it needs first, in priority order. One
worker per GPU takes the first ready task and rereads the queue before
every task, so tasks pushed later run after a pull without a restart. A
change to the queue format (a new key) needs a worker restart after the
pull. Ctrl+C stops the worker and its running task; the start command
continues where it stopped and skips finished work. A failed task stops
the worker with `STOP queue: <task> failed: <last error line>` and the log
path (`.queue_state/logs/`); send that line back.

On the server, `artifacts/` still holds the adapters, samples and pairs of
the earlier setup. They stay where they are; new runs write to new roots.
