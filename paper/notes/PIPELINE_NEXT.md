# FedLS-SQL: run queue

## Status

Updated 2026-11-18 10:05 (Asia/Ho_Chi_Minh). FedAvg SFT is done: rounds
1-4 at 72.43, 74.10, 74.71, 74.71; the line stopped with best round 3.
DPO from FedAvg round 2: 77.46 (round 1), 78.20 (round 2). Running (from
the queue order after the curve record at 09:49): centralized SFT.

| GPU | State | Known from |
|---|---|---|
| 0 | `refs/central_sft`, epoch 1 (since about 09:50). | queue order and the last published result (`7285253d`) |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Leave the worker running. Expected (estimates, Asia/Ho_Chi_Minh, 18
   Nov): centralized
   SFT, from about 09:50, about 2 h 10 min per epoch with its evaluation, until its rule
   stops it (likely 3 to 5 epochs); then the DPO line from the best
   FedAvg round. If the worker stops, start it again:

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   Send back each `curve ... EX` line of FedAvg and of centralized SFT,
   and a `STOP queue` line, if one comes.

2. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `dpo_k2_nearest/reuse_samples`, `dpo_k2_nearest/round_1`, `dpo_k2_nearest/publish_round_1`, `dpo_k2_nearest/eval_1`, `dpo_k2_nearest/publish_eval_1` | I2: the round from FedAvg round 2 with each distinct wrong SQL paired with its most similar correct SQL (2 per question), on the same samples as the random round (77.46); aims at the executable wrong results, which the random round left at 385 | about 2-2.5 h, training only (estimate) | done: 77.08 (random 77.46) |
| 2 | `dpo_k2/round_2` or `dpo_k2_nearest/round_2`, each with its publish, eval and publish | I1: a second on-policy round (samples and reference from round 1's global model) with the pair rule that won round 1; the other branch is skipped | about 2.5-3 h (estimate) | done: random ran, 78.20; nearest skipped |
| 3 | `rounds/fedavg_sft` | FedAvg SFT from the base student on the 5 clients (`alpha_0.1/k5`), prompt A, one round at a time; every round evaluated on Spider test and published | about 2 h per round plus about 10 min of evaluation (measured round 1: 7,339 s + 206 s); 3 to 8 rounds | done: 72.43, 74.10, 74.71, 74.71; best round 3 |
| 4 | `refs/central_sft` | centralized SFT on the union of the 5 clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | about 2 h 10 min per epoch (estimate) | queued |
| 5 | `dpo/after_fedavg` | DPO + NLL rounds from the best FedAvg round (k = best) (10 samples at T 1.0, 2 pairs per question, no pair from a database without rows), each round evaluated on Spider test and published | about 1.5-2.5 h per round (estimate); up to 6 rounds | queued |

How the rounds stop: a round is a gain when it beats the best round by
more than 0.5 EX point; a line stops after 2 rounds in a row without a
gain, or at 4 rounds (FedAvg), 8 epochs (centralized) or 6 rounds (DPO).
The control of a DPO line is FedAvg at the same total rounds; if a DPO
line runs past FedAvg round 4, a curve that extends FedAvg is queued then.

After round 2 of the k = 2 line: more rounds of it if round 2 gains; the
line from the best FedAvg round (row 5) and k = 1, k = 0 decided on the
numbers.

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
