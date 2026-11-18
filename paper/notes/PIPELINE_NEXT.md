# FedLS-SQL: run queue

## Status

Updated 2026-11-18 15:30 (Asia/Ho_Chi_Minh). Done on Spider test: FedAvg
SFT rounds 1-4 (72.43, 74.10, 74.71, 74.71; best round 3); DPO from FedAvg
round 2: round 1 77.46 (random pairs), 77.08 (nearest), round 2 78.20;
RFT round 1 on the same pairs 75.87 (below DPO, p 0.015). The worker runs
the decision runs (`decide/*`); centralized SFT resumes after them.
Pushed (code `5aedf463`): the line without on-policy rounds
(`decide/fixed`, fixed pairs and reference), right after the gold-chosen
run. The running task does not load the new code; the tasks after it do,
and the code keeps their identities.

| GPU | State | Known from |
|---|---|---|
| 0 | Worker: `decide/gold_chosen` (next in queue after RFT, published 13:45). | RFT result commit `424cd93e` |
| 1 | Not ours: in use by another user. | owner, 2026-11-09 |

## Run now

1. Pull and run the tests, without the GPU, while the worker runs (about
   5 min, estimate). The worker reads the new queue before its next task.
   Send back the pytest summary (459 passed on the Mac), or the error.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Merge failed: send git status' }; uv run --no-sync pytest -q --basetemp "$tmp\pytest"; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
   ```

2. Nothing else to start. If the worker stops, start it again with the
   command below. Expected (estimates, Asia/Ho_Chi_Minh): gold chosen
   about 16:15, fixed line (2 rounds) about 19:45, k = 0 about 00:15 (19
   Nov), wrong results first about 02:45, no NLL about 05:15, k = 3 about
   08:15; then centralized SFT resumes.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; uv run --no-sync python -m scripts.gpu_worker run --gpu 0; if ($LASTEXITCODE -ne 0) { throw 'Worker stopped (see status)' } }
   ```

   Send back:
   - the EX line of each decision run;
   - for the fixed line, round 2: the log line `DPO reference fixed at
     round 1's start` and the first `DPO update 1/...` line (its margin
     is not 0, since the policy starts away from the reference);
   - for k = 0: the pair counts per client and, in its first minutes of
     training, the peak reserved VRAM (client 4 has about 4,000 pairs);
     if a round starts sampling instead of reusing the copied samples,
     say so;
   - a `STOP queue` line, if one comes.

3. Any time, CPU only (phase 0a, a few minutes): the pairs of the base
   student's round 1 samples by rejected outcome, per client, then
   published. Send back the printed tables.

   ```powershell
   & { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; $tmp='D:\phungthan\fediclkd\tmp'; New-Item -ItemType Directory -Force -Path $tmp | Out-Null; $env:TEMP=$tmp; $env:TMP=$tmp; $a='audits/protocol_v2/fedpref_base_ddlrows_alpha01_s0'; uv run --no-sync python -m scripts.pair_composition --audit $a --round 1 --policy base --split-dir processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5; if ($LASTEXITCODE -ne 0) { throw 'Composition failed' }; uv run --no-sync python -m scripts.publish_results --message 'results: composition of the base student round 1 pairs per client' --paths "$a/pair_read/composition_r1_base.json"; if ($LASTEXITCODE -ne 0) { throw 'Publish failed (rerun if the worker was publishing)' } }
   ```

## Running and queued

Every decision run except row 2 is one DPO round, read question by
question against DPO round 1 from FedAvg round 2 (77.46; execution errors
99, wrong results 385). Rows 1, 4 and 5 train on its samples from its
start and differ from it in one setting.

| # | Tasks | What it answers | About | State |
| --- | --- | --- | --- | --- |
| 1 | `decide/gold_chosen/*` | gold SQL as chosen for questions whose 10 samples are all wrong (573 in round 1) | 2.5 h (estimate) | running (inferred) |
| 2 | `decide/fixed/*` | the line without on-policy rounds, as federated DPO is published: round 1 as dpo_k2 round 1, round 2 on the round 1 pairs with FedAvg round 2 as reference. Round 2 is read against on-policy round 2 (78.20); round 1 is read against 77.46 as a rerun of the same training | 3.5 h for 2 rounds (estimate) | queued, next |
| 3 | `decide/k0/*` | DPO from the base student (k = 0), 2 pairs per question, on the samples of the pair read: is the FedAvg SFT stage needed? Read against FedAvg round 1 (72.43) and 77.46 | 4.5 h (estimate) | queued |
| 4 | `decide/wrfirst/*` | rejected side drawn from executable wrong results when there are any: does the outcome of the rejected side decide what DPO fixes? | 2.5 h (estimate) | queued |
| 5 | `decide/nonll/*` | DPO without the NLL term | 2.5 h (estimate) | queued |
| 6 | `decide/k3/*` | DPO round 1 from FedAvg round 3 (k = 3): total 4 rounds, as DPO round 2 from k = 2 (78.20) and FedAvg round 4 (74.71); step 1 of row 8 | 3 h (estimate) | queued |
| 7 | `refs/central_sft` | centralized SFT on the union of the 5 clients, same recipe, prompt and evaluation as FedAvg; one epoch per step, rule 0.5 / patience 2 / at most 8 | 2 h 10 min per epoch (estimate) | stopped in epoch 1, resumes after row 6 |
| 8 | `dpo/after_fedavg` | DPO + NLL rounds from FedAvg round 3 until the rule stops them | 2.5-3 h per round (estimate); up to 6 rounds | queued |

Reading: a setting is kept when it gains at least 0.5 EX over 77.46 with
a McNemar p below 0.05, or (row 5) when removing it loses that much. Rows
1 and 4 are also read on the wrong-result count. Row 2: on-policy rounds
stay a part of the method when round 2 on-policy (78.20) beats the fixed
round 2 by at least 0.5 with p below 0.05. The fixed round 2 trains on
8,026 pairs against 3,354 on-policy, so it gets more updates; only if it
wins does a run with its pairs cut to the on-policy count follow. Row 3
at about 74 or more opens a k = 0 line of 4 rounds; at about 72-73 the
SFT stage stays. The settings kept then run round 2 together from k = 2.
A second benchmark (BIRD, clients on BIRD train databases, BIRD dev) is
the owner's decision after rows 2 and 5.

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
