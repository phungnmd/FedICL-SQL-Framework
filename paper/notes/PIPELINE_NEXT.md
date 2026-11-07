# FedLS-SQL: run queue

Commands to run next on the server. Conventions: `AGENTS.md` ("Defaults")
and `CONVENTION.MD` section 5. Remove a command once its result is logged in
`LAB_LOG.md`.

## Queue: federated DPO + NLL, verification run

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
RFT arm trains on the same pairs with only the NLL term.

Evaluation uses `scripts.eval_standard`: the contract of the FedAvg reference
rows (zero-shot SQL-only prompt, greedy 256 tokens, batch 16), on Spider dev
and BIRD dev.

Every command resumes when rerun unchanged. Do not pull or commit while a
job runs. Spider test is not used in this queue.

### Step 0: update the checkout (no job running)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_dpo.py tests/test_pref_rounds.py tests/test_preference_pairs.py tests/test_preference_sampling.py tests/test_test_suite.py tests/test_eval_standard.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
```

### Step 1: GPU smoke, about 10-15 min (GPU 0)

8 questions per client, its own output root. Check in the log: the
`first batch ... peak reserved` line and the `DPO smoke on the longest pair`
line stay under 21.5 GiB, and shared GPU memory stays near zero.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_smoke_s0'; uv run --no-sync python experiments/federated_pref/run.py round --arm dpo --round 1 --parent-result $P --split-dir $S --out $O --audit "$O/audit" --questions-per-client 8; if ($LASTEXITCODE -ne 0) { throw 'Smoke failed' } }
```

### Step 2: round 1 sampling, two lanes in parallel

Round 1 samples are shared by both arms. Lane 1 takes clients 1-3, lane 2
clients 4-5. Start lane 2 a few seconds after lane 1.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py collect --arm dpo --round 1 --clients 1 2 3 --parent-result $P --split-dir $S --out $O --questions-per-client 400; if ($LASTEXITCODE -ne 0) { throw 'Sampling lane 1 failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py collect --arm dpo --round 1 --clients 4 5 --parent-result $P --split-dir $S --out $O --questions-per-client 400; if ($LASTEXITCODE -ne 0) { throw 'Sampling lane 2 failed' } }
```

### Step 3: round 1 training, two lanes in parallel (after both step 2 lanes)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py round --arm dpo --round 1 --parent-result $P --split-dir $S --out $O --questions-per-client 400; if ($LASTEXITCODE -ne 0) { throw 'DPO round 1 failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py round --arm rft --round 1 --parent-result $P --split-dir $S --out $O --questions-per-client 400; if ($LASTEXITCODE -ne 0) { throw 'RFT round 1 failed' } }
```

### Status (read-only, any time, second terminal)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py status --parent-result $P --split-dir $S --out $O --questions-per-client 400 --rounds 2; if ($LASTEXITCODE -ne 0) { throw 'Status failed' } }
```

### Step 4: evaluation of round 1 (Spider dev, BIRD dev), two lanes in parallel

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; $A='fedpref_dpo_r1'; uv run --no-sync python -m scripts.eval_standard --arm $A --adapter "$O/dpo/round_1/global_adapter" --sets spider bird; if ($LASTEXITCODE -ne 0) { throw "Eval failed: $A" } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; $A='fedpref_rft_r1'; uv run --no-sync python -m scripts.eval_standard --arm $A --adapter "$O/rft/round_1/global_adapter" --sets spider bird; if ($LASTEXITCODE -ne 0) { throw "Eval failed: $A" } }
```

### Step 5: publish (no job running)

Commits only the new compact files: samples, pairs, round records, training
metrics and evaluation rows. It fast-forwards to `origin/main` first, so new
commits pushed from the Mac (queue 2 code) do not block the push.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only); if ($LASTEXITCODE -ne 0 -or $dirty.Count -ne 0) { throw 'Tracked files changed' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $new=@(git ls-files --others --exclude-standard -- audits/protocol_v2/fedpref_coder15b_alpha01_s0 experiments/eval_arms/results experiments/federated/results); if ($LASTEXITCODE -ne 0) { throw 'Listing failed' }; if ($new.Count -eq 0) { throw 'Nothing to publish' }; $new; foreach ($f in $new) { git add -- $f; if ($LASTEXITCODE -ne 0) { throw "Staging failed: $f" } }; git commit -m 'results: federated DPO and RFT rounds from the FedAvg R3 adapter'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```

### Step 6: round 2, two lanes in parallel (may start without waiting for the round 1 numbers)

Each arm samples from its own round 1 adapter, so this includes sampling.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py round --arm dpo --round 2 --parent-result $P --split-dir $S --out $O --questions-per-client 400; if ($LASTEXITCODE -ne 0) { throw 'DPO round 2 failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; uv run --no-sync python experiments/federated_pref/run.py round --arm rft --round 2 --parent-result $P --split-dir $S --out $O --questions-per-client 400; if ($LASTEXITCODE -ne 0) { throw 'RFT round 2 failed' } }
```

### Step 7: evaluation of round 2 (Spider dev, BIRD dev), two lanes

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; $A='fedpref_dpo_r2'; uv run --no-sync python -m scripts.eval_standard --arm $A --adapter "$O/dpo/round_2/global_adapter" --sets spider bird; if ($LASTEXITCODE -ne 0) { throw "Eval failed: $A" } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; $A='fedpref_rft_r2'; uv run --no-sync python -m scripts.eval_standard --arm $A --adapter "$O/rft/round_2/global_adapter" --sets spider bird; if ($LASTEXITCODE -ne 0) { throw "Eval failed: $A" } }
```

### Step 8: one more FedAvg SFT round (control), then its evaluation (one lane, about 2 h)

Same settings as the approved FedAvg run, warm-started from its R3 row.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0/sft_r4'; uv run --no-sync python experiments/federated/run.py stage private --parent-result $P --split-dir $S --n-clients 5 --local-epochs 1 --client-dataset-profile spider --client-schema-style full --model Qwen/Qwen2.5-Coder-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --lm-loss target_fp32 --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --aggregation-protocol plaintext --stage fedpref_sft_r4_s0 --out $O; if ($LASTEXITCODE -ne 0) { throw 'SFT round 4 failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $O='artifacts/protocol_v2/fedpref_coder15b_alpha01_s0'; $A='fedpref_sft_r4'; uv run --no-sync python -m scripts.eval_standard --arm $A --adapter "$O/sft_r4/fedavg_adapter" --sets spider bird; if ($LASTEXITCODE -ne 0) { throw "Eval failed: $A" } }
```

Then publish again with the step 5 command.

### Local, after publication: test-suite EX on Spider dev (CPU, Mac)

Rescores every published dev prediction file against the official test-suite
databases (`scripts/score_test_suite.py`); run by the agent after pulling.

## Queue 2: headroom check and CoT probe, server side (from FedAvg R3)

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
`fedpref_sft_r4` (queue 1, step 8), the same round in SQL-only. Evaluation is
Spider dev only; CoT evaluation uses 1,024 new tokens and strict parsing.

Lanes: each command names its GPU; change the `CUDA_VISIBLE_DEVICES` digit to
use whichever card is free. Do not run queue 2 step 0 while any job runs.

### Q2 step 0: update the checkout (no job running)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; uv run --no-sync pytest -q tests/test_eval_standard.py tests/test_pass_at_k.py tests/test_rationale_targets.py tests/test_stage_chain.py; if ($LASTEXITCODE -ne 0) { throw 'Tests failed' } }
```

### Q2 step 1: headroom check, about 1.5-2.7 h (one lane)

Teacher greedy on Spider dev (about 15 min, 14-18 GiB measured):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; uv run --no-sync python -m scripts.eval_standard --arm teacher7b_4bit --model Qwen/Qwen2.5-Coder-7B-Instruct --model-4bit --sets spider; if ($LASTEXITCODE -ne 0) { throw 'Teacher eval failed' } }
```

R3 pass@8 on Spider dev (about 1-2.4 h; check the `first batch ... peak
reserved` line):

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $A='artifacts/protocol_v2/p227_coder15b_alpha01_s0/fl_aaa/round_3/fedavg_adapter'; uv run --no-sync python -m scripts.pass_at_k --arm fedavg_r3 --adapter $A --set spider; if ($LASTEXITCODE -ne 0) { throw 'pass@8 failed' } }
```

### Q2 step 2: server stages, about 1.2-1.5 h each (any lane)

BIRD-length rows: check the peak reserved VRAM in the log on the first steps
(about 20 GiB expected) and shared GPU memory near zero.

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $POOL='processed_data/protocol_v2/rationale_kd/p215_struct_full_s0/train.csv'; $SIDE='processed_data/protocol_v2/rationale_kd/p215_struct_full_s0/teacher_plans_qwen25_coder_7b.jsonl'; $O='artifacts/protocol_v2/cotprobe_s0/srv_teacher'; uv run --no-sync python experiments/federated/run.py stage public --parent-result $P --server-method qp_teacher --rationale-targets $SIDE --pool $POOL --server-dataset-profile bird_with_evidence --schema-style full --model Qwen/Qwen2.5-Coder-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --lm-loss target_fp32 --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --lambda-ft 1 --lambda-kd 0 --stage cotprobe_srv_teacher_s0 --out $O; if ($LASTEXITCODE -ne 0) { throw 'Server stage srv_teacher failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $POOL='processed_data/protocol_v2/rationale_kd/p215_struct_full_s0/train.csv'; $O='artifacts/protocol_v2/cotprobe_s0/srv_ast'; uv run --no-sync python experiments/federated/run.py stage public --parent-result $P --server-method qp_ast --pool $POOL --server-dataset-profile bird_with_evidence --schema-style full --model Qwen/Qwen2.5-Coder-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --lm-loss target_fp32 --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --lambda-ft 1 --lambda-kd 0 --stage cotprobe_srv_ast_s0 --out $O; if ($LASTEXITCODE -ne 0) { throw 'Server stage srv_ast failed' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $POOL='processed_data/protocol_v2/rationale_kd/p215_struct_full_s0/train.csv'; $O='artifacts/protocol_v2/cotprobe_s0/srv_ce'; uv run --no-sync python experiments/federated/run.py stage public --parent-result $P --server-method ce --pool $POOL --server-dataset-profile bird_with_evidence --schema-style full --model Qwen/Qwen2.5-Coder-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --lm-loss target_fp32 --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --lambda-ft 1 --lambda-kd 0 --stage cotprobe_srv_ce_s0 --out $O; if ($LASTEXITCODE -ne 0) { throw 'Server stage srv_ce failed' } }
```

### Q2 step 3: one client round with gold-derived plans, about 2.1-2.7 h (any lane)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $P='experiments/federated/results/federated__fedavg__s0__7fd190778bbf__b928b675__r3'; $S='processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/federated_noniid/alpha_0.1/k5'; $O='artifacts/protocol_v2/cotprobe_s0/t0'; uv run --no-sync python experiments/federated/run.py stage private --parent-result $P --split-dir $S --n-clients 5 --local-epochs 1 --client-dataset-profile spider --client-schema-style full --client-response-format qp_cot_v1 --model Qwen/Qwen2.5-Coder-1.5B-Instruct --lora-r 16 --lr 0.0002 --max-len 7168 --truncation-policy error --gradient-checkpointing --lm-loss target_fp32 --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0 --aggregation-protocol plaintext --stage cotprobe_t0_s0 --out $O; if ($LASTEXITCODE -ne 0) { throw 'Client round t0 failed' } }
```

### Q2 step 4: evaluation on Spider dev (after each arm; CoT about 0.7-1.2 h)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $O='artifacts/protocol_v2/cotprobe_s0'; uv run --no-sync python -m scripts.eval_standard --arm cotprobe_srv_teacher --adapter "$O/srv_teacher/m_g" --sets spider --response-format qp_cot_v1; if ($LASTEXITCODE -ne 0) { throw 'Eval failed: srv_teacher' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $O='artifacts/protocol_v2/cotprobe_s0'; uv run --no-sync python -m scripts.eval_standard --arm cotprobe_srv_ast --adapter "$O/srv_ast/m_g" --sets spider --response-format qp_cot_v1; if ($LASTEXITCODE -ne 0) { throw 'Eval failed: srv_ast' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='0'; $O='artifacts/protocol_v2/cotprobe_s0'; uv run --no-sync python -m scripts.eval_standard --arm cotprobe_srv_ce --adapter "$O/srv_ce/m_g" --sets spider; if ($LASTEXITCODE -ne 0) { throw 'Eval failed: srv_ce' } }
```

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; $env:CUDA_DEVICE_ORDER='PCI_BUS_ID'; $env:CUDA_VISIBLE_DEVICES='1'; $O='artifacts/protocol_v2/cotprobe_s0'; uv run --no-sync python -m scripts.eval_standard --arm cotprobe_t0 --adapter "$O/t0/fedavg_adapter" --sets spider --response-format qp_cot_v1; if ($LASTEXITCODE -ne 0) { throw 'Eval failed: t0' } }
```

### Q2 step 5: publish (no job running)

```powershell
& { $ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; if ((git branch --show-current) -ne 'main') { throw 'Expected main' }; $staged=@(git diff --cached --name-only); if ($LASTEXITCODE -ne 0 -or $staged.Count -ne 0) { throw 'Index must be empty' }; $dirty=@(git diff --name-only); if ($LASTEXITCODE -ne 0 -or $dirty.Count -ne 0) { throw 'Tracked files changed' }; git fetch origin; if ($LASTEXITCODE -ne 0) { throw 'Fetch failed' }; git merge --ff-only origin/main; if ($LASTEXITCODE -ne 0) { throw 'Fast-forward failed' }; $new=@(git ls-files --others --exclude-standard -- experiments/pass_at_k/results experiments/eval_arms/results experiments/federated/results); if ($LASTEXITCODE -ne 0) { throw 'Listing failed' }; if ($new.Count -eq 0) { throw 'Nothing to publish' }; $new; foreach ($f in $new) { git add -- $f; if ($LASTEXITCODE -ne 0) { throw "Staging failed: $f" } }; git commit -m 'results: teacher and pass@8 headroom check, CoT probe server stages'; if ($LASTEXITCODE -ne 0) { throw 'Commit failed' }; git push origin main; if ($LASTEXITCODE -ne 0) { throw 'Push failed' } }
```
