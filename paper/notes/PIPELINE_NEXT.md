# FedLS-SQL: run queue

## Status

Updated 2026-11-19 03:40 (Asia/Ho_Chi_Minh). Done on Spider test: FedAvg
SFT rounds 1-4 (72.43, 74.10, 74.71, 74.71; best round 3); DPO from FedAvg
round 2: round 1 77.46, round 2 78.20 (fixed pairs and reference: 77.64,
78.02; on-policy rounds do not beat the fixed line at round 2); RFT
round 1 75.87. New: DPO round 1 from the base student (k = 0) 75.87,
above every FedAvg SFT round (round 1 by 3.44, p 6e-06; the best by 1.16,
p 0.16) and 1.59 below DPO round 1 from FedAvg round 2 (p 0.041). By the
reading rule the k = 0 line now runs to 4 rounds (`dpo_k0/*`, pushed).

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: the next ready decision run after `decide/k0` (`decide/wrfirst`, or `decide/nonll` if GPU 1 took `wrfirst`). | k = 0 result commit `96007ff6`, published 03:16 |
| 1 | Worker if step 2 was run; no result from it yet. | owner, 2026-11-19 |

## Run now

1. Pull, in any terminal, while the workers run (a running round keeps
   the code it loaded). It brings the `dpo_k0` tasks and the lock that
   lets two workers publish; the workers take the new tasks without a
   restart. The tests take about 5 min without a GPU (estimate). Send
   back the pytest summary (462 passed on the Mac), or the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. If GPU 1 has no worker yet: start one in a new terminal; leave the
   GPU 0 worker as it is. It takes the first ready task, then whatever is
   next in the queue. If a worker stops, the same command with its GPU
   digit continues. Expected with two cards (estimates, Asia/Ho_Chi_Minh,
   19 Nov; a DPO round with its evaluation has taken about 3 h 10 min):
   wrong results first, no NLL and k = 3 done by about 10:00; then the
   k = 0 line on one card (rounds 2, 3, 4 at about 13:00, 16:00, 19:00)
   and centralized SFT on the other.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 1; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   Send back:
   - the first lines of the GPU 1 worker (the task it took and its card);
   - the first time two vLLM jobs overlap (an evaluation on one card while
     the other samples or evaluates): the peak reserved VRAM of each and
     whether either slows down; two vLLM jobs at once have not run here;
   - the EX line of each decision run and of each k = 0 round;
   - for k = 0 round 2: the pair counts per client;
   - a `STOP queue` line, if one comes.

3. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

Every decision run is one DPO round, read question by question against
DPO round 1 from FedAvg round 2 (77.46; execution errors 99, wrong
results 385; run again: 77.64). Rows 1 and 2 train on its samples from
its start and differ from it in one setting.

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `decide/wrfirst/*` | rejected side drawn from executable wrong results when there are any: does the outcome of the rejected side decide what DPO fixes? | 3 h 15 min (estimate) | running or next (inferred) |
| 2 | `decide/nonll/*` | DPO without the NLL term | 2.5 h (estimate) | running or next (inferred) |
| 3 | `decide/k3/*` | DPO round 1 from FedAvg round 3 (k = 3): total 4 rounds, as DPO round 2 from k = 2 (78.20) and FedAvg round 4 (74.71); step 1 of row 6 | 3 h (estimate) | queued |
| 4 | `dpo_k0/round_2..4` | DPO rounds 2-4 from the base student (k = 0), on-policy, each evaluated: is the FedAvg SFT stage needed at the same total rounds? Round 2 against FedAvg round 2 (74.10), round 3 against 77.46, round 4 against 78.20 and FedAvg round 4 (74.71) | 3 h per round (estimate) | queued |
| 5 | `refs/central_sft` | centralized SFT on the union of the 5 clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 4 or on the free card |
| 6 | `dpo/after_fedavg` | DPO + NLL rounds from FedAvg round 3 until the rule stops them | 2.5-3 h per round (estimate); up to 6 rounds | queued |

Reading: a setting is kept when it gains at least 0.5 EX over 77.46 with
a McNemar p below 0.05, or (row 2) when removing it loses that much. A
difference of about 0.2 EX is what running the same training again
gives. Row 1 is also read on the wrong-result count. Row 4 is read at
the same total rounds as the k = 2 line (round 3 against 77.46, round 4
against 78.20); whether the SFT stage stays is the owner's decision on
those numbers. The settings kept then run round 2 together from the
start that is kept (k = 0 or k = 2). A second benchmark (BIRD, clients
on BIRD train databases, BIRD dev) is the owner's decision after row 2.

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
