# FedLS-SQL: run queue

## Status

Updated 2026-11-19 09:30 (Asia/Ho_Chi_Minh). Done on Spider test: FedAvg
SFT rounds 1-4 (72.43, 74.10, 74.71, 74.71); DPO + NLL from FedAvg
round 2: round 1 77.46, round 2 78.20 (fixed pairs and reference with
NLL: 77.64, 78.02); RFT round 1 75.87; DPO round 1 from the base student
75.87. New: DPO without the NLL term 73.59, no gain over its start
(74.10) and 3.87 below DPO + NLL (p < 1e-6), so the NLL term is a part
of the method; wrong-result rejects first 77.27, the same EX as random
pairs (77.46, p 0.74) with fewer wrong results (342 against 385) and
more execution errors (146 against 99), not kept. No result since
06:31.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: free at 06:31, took the first ready task then (`dpo_k0/round_2`, or `decide/k0_gold` if GPU 1 had not taken it). | `decide/nonll` result commit `f8485b4b`, published 06:31 (inferred) |
| 1 | Free at 05:24, took `decide/k0_gold` then; stopped at 07:00 if it was restarted with `--until 07:00`. | `decide/wrfirst` result commit `cd4727a7`, published 05:24 (inferred) |

## Run now

1. Send the state of the queue (read-only), and whether GPU 1 stopped
   at 07:00 (the last lines of its terminal):

   ```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker status; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

2. To start GPU 1 again (the same line with `--gpu 0` continues GPU 0 if
   it stops; add `--until HH:MM` after the GPU digit for a stop time):

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   A task that GPU 1 left at 07:00 is taken by the GPU 0 worker after
   its own task, before the evaluation of the round it just trained
   (queue order), so with one card the EX of k = 0 round 2 comes after
   `decide/k0_gold`. Expected with GPU 0 alone (estimates): both done
   by about 12:30, k = 0 rounds 3 and 4 at about 15:30 and 18:30,
   `decide/k3` at about 21:30.

   Send back:
   - the first time two vLLM jobs overlap (an evaluation on one card while
     the other samples or evaluates): the peak reserved VRAM of each and
     whether either slows down;
   - the EX line of `decide/k0_gold` and of each k = 0 round;
   - for `decide/k0_gold`: the pair counts per client and, in the first
     updates of client 4, the peak reserved VRAM (its questions on
     databases without rows are new to DPO training);
   - for k = 0 round 2: the pair counts per client;
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
| 1 | `decide/k0_gold/*` | DPO round 1 from the base student with the gold SQL as chosen where execution gives no pair: questions whose samples are all wrong, and questions on databases without rows (rejected: their wrong samples). Does gold inside the round replace the SFT stage? Read against DPO round 1 from the base student (75.87) and from FedAvg round 2 (77.46) | 4.5 h (estimate; about 14,000 pairs against 8,908) | running or stopped at 07:00 (inferred) |
| 2 | `dpo_k0/round_2..4` | DPO rounds 2-4 from the base student (k = 0), on-policy, each evaluated: is the FedAvg SFT stage needed at the same total rounds? Round 2 against FedAvg round 2 (74.10), round 3 against 77.46, round 4 against 78.20 and FedAvg round 4 (74.71) | 3 h per round (estimate) | round 2 running (inferred) |
| 3 | `decide/k3/*` | DPO round 1 from FedAvg round 3 (k = 3): total 4 rounds, as DPO round 2 from k = 2 (78.20) and FedAvg round 4 (74.71); step 1 of row 5 | 3 h (estimate) | queued |
| 4 | `refs/central_sft` | centralized SFT on the union of the 5 clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 3 |
| 5 | `dpo/after_fedavg` | DPO + NLL rounds from FedAvg round 3 until the rule stops them | 2.5-3 h per round (estimate); up to 6 rounds | queued |

Reading: a setting is kept when it gains at least 0.5 EX over the run it
is read against with a McNemar p below 0.05. A difference of about 0.2
EX is what running the same training again gives. Row 1 runs its two
settings together; if it gains, each runs alone and the k = 0 line takes
the rule up at its next round. Row 2 is read at the same total rounds as
the k = 2 line (round 3 against 77.46, round 4 against 78.20); whether
the SFT stage stays is the owner's decision on those numbers. Open for
the owner: round 2 of federated DPO as published (no NLL, fixed pairs,
fixed reference) from the `decide/nonll` root, about 2.5 h, for the
baseline row; and the second benchmark (BIRD, clients on BIRD train
databases, BIRD dev).

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
