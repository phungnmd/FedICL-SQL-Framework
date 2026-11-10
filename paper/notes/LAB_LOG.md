# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

## 2026-11-10: SQL reference rows with vLLM inproc

The reused adapters evaluated again on Spider test with vLLM inproc
(fedicl-sql `4315cee`), next to their archived HF numbers. Every DPO and
reference row from here on is compared on these vLLM rows.

| Row | vLLM inproc | HF (archive) | Exec error | Rows with a different SQL |
|---|---:|---:|---:|---:|
| base | 57.89 | 57.94 | 440 | 188 |
| central Spider E3 | 70.75 | 71.08 | 219 | 161 |
| FedAvg R3 | 71.26 | 71.50 | 211 | 150 |
| `gold_k2aaa_a3` | 73.08 | 73.03 | 144 | 142 |
| `hinton_k2aaa_a3` | 73.31 | 73.50 | **129** | 117 |
| central Spider + BIRD E3 (no privacy) | **73.96** | 73.78 | 163 | 118 |

- Engines agree within 0.33 point on every row, and the order is unchanged.
- The server stage on BIRD adds about 2 points over FedAvg (gold +1.82,
  Hinton +2.05) and has the fewest execution errors.
- FedAvg R3 inproc is 71.26 (the default-mode runs gave 71.45 and 71.22).

## 2026-11-10: method line is SQL DPO from the BIRD server stage; CoT becomes analysis

Owner read the archived results in this session and chose: a method paper
on SQL-only output (BIRD server stage with teacher KD, FedAvg, then
federated DPO + NLL labelled by execution on each client's databases), with
a section on why CoT does not help at 1.5B. Approved reuse of five earlier
adapters as starts and baselines: `hinton_k2aaa_a3`, `gold_k2aaa_a3`,
FedAvg R3 (`fl_aaa`), `central_e3`, `central_mix_e3`.

Readings behind it (archive, Spider test unless noted): every K2 arm 72.6-73.9
against FedAvg 71.50 and centralized Spider 71.08; on Spider dev, SQL DPO
from a converged SFT student +1.45 after 2 rounds (p=.04) and 75.53 after 9;
CoT route `c1` 60.64 to 70.89 against SQL `s1` 58.80 to 74.18 under the same
DPO rounds; Liu et al. (ACL 2025, 6.7B-15B) find CoT DPO above plain SFT by
0.5-0.7 on Spider dev. Gaps between starts shrank under DPO in the archive
(14.8 points to 1.35), so DPO from FedAvg R3 is run at round 1 next to the
Hinton start: it tells whether the server stage still matters after DPO.

Queue (fedicl-sql `5c8469ad`, `b03c15e9`): reference rows with vLLM inproc,
SQL DPO round 1 from both starts, rounds 2-6 from `hinton_k2aaa_a3`, then
template client rounds 2-3 (a curve that continues the stopped client
curve) and CoT DPO from the best template round, up to 3 rounds.

## 2026-11-10: CoT DPO starts from template round 1

Owner reviewed the archived results (allowed in this session): on Spider dev,
centralized, the CoT route `c1` gained less from the same DPO + NLL rounds
than the SQL route `s1` (60.64 to 70.89 against 58.80 to 74.18) despite more
pairs; in the larger-model papers (Liu et al., ExCoT) CoT is what makes DPO
work. The CoT line here has an untested combination, Spider SFT on plans
before federated DPO, so it continues with DPO.

Decision (owner): DPO from the CoT line. Start: template round 1 (62.69,
format valid on every row), not self-taught R2 (60.64); 288 rows right only
in template R1 against 244 only in R2. Fallback: the template plan of the
gold SQL, the style the start was trained on. Queue: fedicl-sql `curve_dpo`
under `dpo_tpl`.

## 2026-11-10: self-taught round 3 falls, curve stopped

Self-taught R3 from R2 (fedicl-sql `6534e5e`, `8395630`, `aece957`): 58.69 EX
on Spider test (EM 33.7; easy 80.0, medium 64.3, hard 43.6, extra 36.7;
invalid format 69, exec error 267, wrong result 551). The curve stops at its
maximum of 3, best step R2 (60.64). Training again on its own outputs from
the previous adapter lowers EX by 1.95 points; STaR restarts from the base
model each iteration for this reason. Worker stopped by the owner before the
queued DPO line.

Reference given by the owner: the untrained base model, SQL-only prompt,
scores 57.94 EX on Spider test (archived row). The CoT line adds 2.7 points
over it at the server (E5) and 2.05 more with one template client round,
while three SQL-only FedAvg rounds from the base model add 13.5 (71.45).

## 2026-11-10: self-taught client rounds 1-2 from E5

Self-taught SFT (own most frequent correct sample, else rationalized from
gold, else dropped), FedAvg weighted by targets, vLLM inproc, Spider test
(fedicl-sql `ffb1d73`, `de6744f`, `d4f7847`, `61ad6ee`), about 2:50 per
round including evaluation:

| | EX | EM | Easy | Medium | Hard | Extra | Invalid format | Exec error | Wrong result |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| E5 | 60.64 | 24.9 | 77.7 | 68.4 | 43.4 | **42.0** | 48 | 268 | **529** |
| Template R1 | **62.69** | **52.6** | 79.1 | **71.7** | **50.1** | 35.9 | **0** | **207** | 594 |
| Self-taught R1 | 60.08 | 27.4 | 79.1 | 66.0 | 46.7 | 38.1 | 82 | 218 | 557 |
| Self-taught R2 | 60.64 | 30.1 | **79.8** | 66.9 | 47.1 | 38.1 | 63 | 245 | 537 |

- Targets per round: about 83% of questions from the client's own samples,
  15% rationalized, 2% dropped; sample accuracy on client train 55-66%.
  Mean training loss 0.11-0.12 against 0.08 for the template round, whose
  final loss reaches 0.01.
- R2 equals E5 with 241 rows right only in each: the rounds move many answers
  and gain none. Template R1 stays ahead of R2 (288 rows right only in
  template R1, 244 only in R2).
- Format errors rise above E5 (63-82 against 48): the targets keep the
  model's own plan wording, so its format variance stays.
- The curve rule compares steps with each other, not with the start, so R2
  counts as a gain over R1 and round 3 runs.

## 2026-11-10: template client round 1 from E5

One FedAvg round on template plans + gold SQL from E5, vLLM inproc, Spider
test (fedicl-sql `bd1e7af`), 1:53 for the step:

| | EX | Easy | Medium | Hard | Extra | Invalid format | Cut | Exec error |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| E5 | 60.64 | 77.7 | 68.4 | 43.4 | **42.0** | 48 | 14 | 268 |
| Template R1 | **62.69** | **79.1** | **71.7** | **50.1** | 35.9 | **0** | **0** | **207** |

- +2.05 points: 275 rows right only after the round, 231 only before. Format
  errors and cut outputs vanish (the template is short and fixed), execution
  errors drop by 61, hard rises 6.7 points, extra falls 6.1.
- Still 8.8 points below SQL-only FedAvg R3 (71.45, three rounds from the
  base model).
- Kept as the comparator of the first self-taught round; the curve stops
  here.

## 2026-11-10: self-taught client SFT replaces the template rounds

No result yet. Question (owner): skip client SFT and go straight to DPO from
E5? A literature review (Liu et al. ACL 2025, ExCoT, Iterative RPO,
Struct-SQL, STaR, RFT, Tai et al. 2023) and the E5 outputs argued against:

- E5 is 60.64 on Spider test against 71.45 for SQL-only FedAvg R3; the gap is
  in-domain SQL skill (hard 43.4 against 65.4), not format (48 invalid
  outputs of 2,147). DPO at lr 1e-5 closes it slowly.
- Every Text-to-SQL DPO + CoT paper fine-tunes on CoT first; none tests DPO
  without it.
- The template plan (about 906 characters against 104 for the SQL, 350 of
  them fixed text) restates the SQL clause by clause and overwrites the
  teacher's plan style in one round; as the DPO fallback it pairs template
  text against teacher-style text.

Decision (owner, 2026-11-10): option C. Template client SFT runs one round
from E5 as the comparator; then self-taught SFT rounds: the client's own most
frequent correct sample, else a plan rationalized from the gold SQL (kept if
its SQL is correct, else dropped, as STaR and RFT keep only verified
outputs), client SFT recipe, up to 3 rounds; DPO from the best of them, with
the rationalized response as the fallback chosen side and no pair when it
fails (as Liu et al. drop all-wrong questions). One target per question, so
the self-taught round trains on at most as many rows as the template round.
Code: fedicl-sql f0aa2d7f, queue 9fe240bb.

## 2026-11-09: fedcot server curve stopped, E5 chosen

Teacher-plan SFT on 4,109 BIRD rows from the base model, one epoch per step,
vLLM inproc, Spider test (fedicl-sql `f6e316f3`, `6ccba453`, `4da3ad0c`,
`1667ed2a`, `323286bf`):

| Epoch | EX | Easy | Medium | Hard | Extra | Invalid format | Exec error |
|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | 52.17 | 70.64 | 57.76 | 40.39 | 29.69 | - | - |
| 2 | 56.68 | 74.04 | 63.71 | 41.90 | 36.13 | - | - |
| 3 | 58.55 | 75.74 | 64.41 | **44.28** | 40.34 | 92 | **260** |
| 4 | 59.94 | **78.30** | 66.63 | 44.06 | 40.34 | 52 | 273 |
| 5 | **60.64** | 77.66 | **68.38** | 43.41 | **42.02** | **48** | 268 |
| 6 | 60.20 | - | - | - | - | - | - |

- Gains shrink: 4.51, 1.86, 1.40, 0.70. E5 counts as a gain (rule: more than
  0.5), so the curve runs at least E6.
- E3 to E4 is mostly format: invalid outputs 92 to 52, cut 36 to 17. E4 to E5
  leaves format and execution errors nearly flat; 146 rows right only in E5,
  131 only in E4, so the 0.70 point is the size of the noise (two vLLM runs
  of one adapter flip 90 rows).
- Hard stays at 43-44 since E3.
- E6 60.20, no gain. Decision (owner): server maximum cut from 8 to 6
  epochs, so the curve stops at E6 with E5 as the best epoch instead of
  training E7 only to confirm it (fedicl-sql 47324303). The client rounds
  start from E5.

## 2026-11-09: dips followed by a rise in the archive

Owner question: does the rule miss curves that dip and then rise? The rule
(gain 0.5, patience 2, maxima 8 / 8 / 6) replayed on every archived curve
(Spider dev, pre-restart):

- One dip then a rise, all caught: `tp_r` 68.09, 67.12, 70.60; `c1_rl`
  66.83, 66.25, 67.70 and 69.54, 69.44, 70.89; `s1_rl` 71.08, 70.02, 73.11.
- Two flat steps then a rise, missed: `sql_rl` 74.18, 75.05, 74.95, 74.95
  stops at round 4 with 75.05; the later retry rounds reached 75.53 (0.48
  point, the size of evaluation noise).
- With the DPO maximum of 6, `c1_rl` and `s1_rl` would stop at round 6 with
  69.54 and 71.08, against 70.89 and 74.18 at rounds 8-9. Those rounds
  sampled 1,200 questions each; rounds 1-6 covered the 6,997 eligible
  questions once and rounds 8-9 retried unsolved ones. A fedcot DPO round
  covers every question, so 6 rounds are about six such passes.
- SFT epoch and FL round curves (2-4 steps) had no dip followed by a rise.

Rule unchanged.

## 2026-11-09: vLLM against itself on plan + SQL

1-epoch server stage, Spider test, `fedcot_srv_e1_vllm_inproc` (the server
curve's step 1): EX 52.17, 4.4% cut, about 4.6 min for the whole command.

| Pair | EX | Right only in each | Same SQL |
|---|---|---:|---:|
| vLLM default / vLLM inproc | 51.70 / 52.17 | 40 / 50 | 81.4% |
| HF / vLLM default | 52.86 / 51.70 | 71 / 46 | 76.9% |
| HF / vLLM inproc | 52.86 / 52.17 | 67 / 52 | 76.3% |

- Two vLLM runs that differ only in batch scheduling already flip 90 rows
  and 0.47 point, so long greedy outputs are this sensitive to numerical
  noise; HF against vLLM flips 117-119 rows, a little more.
- The execution-error excess of the default run (28 / 7 against HF) reverses
  against `inproc` (5 / 16): it was part of the noise, not an engine bias.
  HF against `inproc` is 0.69 point, not a clear difference.
- For the curves: a numerically different but equivalent evaluation moves a
  plan + SQL EX by about 0.5 point (90 discordant rows: about 0.44 point
  standard error of the difference), the size of the rule's gain threshold.

## 2026-11-09: plan + SQL with vLLM is 1.16 points below HF; vLLM kept

`vllm_s0/check_cot`, 1-epoch server stage on Spider test: HF 52.86, vLLM
51.70; 71 rows right only with HF, 46 only with vLLM; same SQL on 76.9% of
rows, same raw output on 1,067. Cut outputs (88 / 89), invalid formats
(206 / 208) and median length (278 tokens) match. The gap is execution
errors (285 / 307; among discordant rows 28 / 7), all real SQL errors
(unknown columns or tables, aggregate misuse), and every discordant row has
a different SQL on the two sides, so scoring is not involved. Outputs
diverge about halfway through (median shared prefix 48%): numerical
differences carried through long outputs. SQL-only with the same adapter
type matches (71.50 / 71.45).

Decision (owner): every evaluation of the curves and baselines runs on vLLM
(`inproc`), each number names its engine; HF re-evaluation of the final
table rows stays possible at the end. `check_cot` is now a report.

## 2026-11-09: server epochs and Spider EX in the archive

Owner question: more server epochs on teacher plans may not raise Spider
test EX; read the archived curves for this (Spider dev, pre-restart).

- SQL-only on BIRD gold barely moves Spider at the server stage: base 59.19,
  one cosine over E1 / E2 / E3 49.13 / 58.80 / 58.22; separate K1 / K2 runs
  58.70 and 59.09. Yet gold K2 then three FedAvg rounds reached 70.41 against
  67.60 for FedAvg alone, and K2 halved Spider execution errors (24.5 to 11).
  The server stage helps through what the client rounds build on, not
  through its own Spider EX.
- Teacher CoT on 1,266 BIRD rows (one 4-epoch cosine) rose every epoch:
  54.64, 55.90, 59.57, 60.64.
- A higher server-stage Spider EX did not give the better start: `cot1_e4`
  60.64 above `sql1_e2` 58.80, but SQL SFT on Spider from them gave 70.21 and
  73.60 (output format differs, so not a clean test).

Reading for the server curve: the rule keeps the earliest epoch unless a
later one gains more than 0.5 point, and stops after 2 epochs without a gain,
so a flat curve costs 2 extra epochs (about 2.5 h) and ends at the earliest
epoch. What the archive questions is the selector itself: server-stage
Spider EX ranked starts poorly for the later stages. Rule unchanged for now.

## 2026-11-09: vLLM reruns differ in the default mode

`vllm_s0`: FedAvg R3 on Spider test, HF 71.50, vLLM 71.45 (`check_sql`
passed at 0.5). The same vLLM evaluation run twice gave 71.45 and 71.22, with
the same SQL on 2,009 of 2,147 rows (93.6%); `check_rerun` (0.2 point)
stopped the queue. Cause: vLLM's engine core runs in its own process by
default, so batch composition depends on timing. Change: evaluations run
with the engine core in-process (`--vllm-determinism inproc`), which vLLM
documents as deterministic scheduling for offline runs. Owner: no rerun
check of the fixed mode; the queue goes straight to the main pipeline. The
`inproc` mode is therefore not verified to be repeatable on this server;
vLLM batch invariance is the fallback if a rerun ever differs. Reports in
`audits/protocol_v2/vllm_eval_check_s0/` on the server (not committed).

## 2026-11-09: client rows need gradient checkpointing

`fedcot_s0/client_probe` on the 4 longest client rows (plan + SQL, 2,766-2,921
tokens, all `baseball_1`): with gradient checkpointing 9.25 GiB peak reserved,
1.7 s per step; without it the 2,921-token row ran out of memory at the 0.88
cap. Client and DPO rounds keep gradient checkpointing (`fedicl-sql`
e50d05f4); the no-checkpointing speed-up is dropped. Rerun with gradient
checkpointing only: done, same 9.25 GiB; lengths of the 8,659 client rows
p50 712, p99 2,017, max 2,921 tokens (report
`audits/protocol_v2/fedcot_lengths_s0/client_cot.json` on the server, not
committed).

## 2026-11-09: stopping rule, gain 0.5 point, higher maxima

Decision (owner, after reading the archived pre-restart curves for this
question only, all Spider dev): a gain is now more than 0.5 point over the
best step (was 1 point), patience stays 2, maxima go to 8 server epochs,
8 client rounds and 6 DPO rounds (were 5, 5, 4). In the archive the 1-point
rule cost nothing on SFT epoch and FL round curves, but those curves were
mostly still rising at their last step (3-4 steps), and it stopped two DPO
curves early (by 3.7 and 4.1 points below their later best), whose rounds
rose by 0.5-1.8 points with dips in between; a 0.5-point threshold with
patience 2 caught all of them. Those DPO rounds sampled 1,200 questions
each, so a full-data round may need fewer rounds. Code: per-curve
`min_gain` and `patience` in `scripts/curve.py`; task commands unchanged.

## 2026-11-09: faster pipeline (code, for the next phase)

Decisions (owner: "cập nhật hết"): evaluation moves to vLLM after a check
against HF; the stopping rule runs by itself; client rounds and DPO rounds
drop gradient checkpointing after a memory probe; DPO scores chosen and
rejected in one pass. Code: `scripts.eval_standard --engine vllm`,
`scripts/compare_predictions.py`, `scripts/curve.py` with three curves in the
queue (server, client, DPO), `train_length_probe.py --modes gc nogc`,
`--pair-batch`. Checks before the curves rely on vLLM: FedAvg R3 HF against
vLLM (stop above 0.5 points), vLLM twice (0.2), the 1-epoch server stage HF
against vLLM (0.5). Not run yet; all 583 local tests pass.

## 2026-11-09: server stage, epoch 1 trained

`fedcot_s0/srv_e1` (result row `federated_stage__Kqp-teacher__s0__6f4cfd89be89__48f1b96e`,
commit 94caca4b): 1 epoch on the 4,109 BIRD rows from the base model in
1.14 h, peak reserved 20.3 GiB. Not evaluated yet. The same publish commit
also picked up two older untracked result rows that were on the server
(`federated_stage__A-Kce-Aret__...`, `federated_stage__A-Kgkd__...`); they
belong to the pre-restart work and are not used; removed from Git in
`fedicl-sql` 4ce7bf54 (owner, copies in the local archive).

## 2026-11-09: server epochs as a chain

Decision (owner): the server epochs are probed as a chain, each stage one more
epoch from the last with its own 1-epoch cosine schedule, instead of a
separate run per length. It saves about 1.3 h per extra epoch and can go
past 3 epochs (maximum now 5). An epoch of the chain may score slightly
below a single-schedule run of the same length; the chosen length can be
retrained cleanly once the method is settled.

## 2026-11-09: server max-len for plan + SQL targets

`fedcot_s0/srv_e1` stopped before training: a BIRD row of 7,190 tokens
(6,665 prompt + 525 target) is above `--max-len 7168`. Probe
`lengths_s0/server_cot` (server, report under
`audits/protocol_v2/fedcot_lengths_s0/`): max 7,601 tokens (train:7343,
works_cycles), p99 6,978, 2 rows above 7,168; 2 training steps on each of the
4 longest rows from the base model peaked at 18.8 GiB reserved, 7.2-8.4 s per
step. Decision: server stages at `--max-len 7680`, every row kept, new out
roots `server_l7680_e1`, `server_l7680_e2`.

## 2026-11-09: vLLM sampling matches HF

Run `vllm_s0/bench_sql` (server, not committed): the 400 round-1 questions
of client 3 from FedAvg R3, K=8, T=0.7, through vLLM 0.33 in WSL. Whole task
3:40 against 13:52 with HF; sample accuracy 72.0% and pass@8 89.0% against
71.0% and 88.5% with HF; no output cut at 256 tokens. vLLM needed the
FlashAttention backend and no FlashInfer sampler (no nvcc in WSL). Decision:
DPO rounds sample with vLLM. The first server-stage retry failed on the stage
contract written while the sidecar was CRLF; the server stages now use the
new out roots `server_e1`, `server_e2`.

## 2026-11-09: main pipeline first; full-data DPO with vLLM

Runs: `fedpref_s0/smoke` and the round-1 sampling of the SQL-only DPO line
(400 questions per client, HF, from FedAvg R3) finished; `dpo_r1` was
training. Not committed. `fedcot_s0/srv_e1` and `srv_e2` failed at start:
the plan sidecar was checked out with CRLF on the server, so its hash did not
match (fix in `PIPELINE_NEXT.md`). Measured: HF SQL-only sampling 1.5-2.2 s
per question, peak 18.2 GiB (`A5000_RUN_CONFIG.md`).

Owner decisions: GPU 1 is in use by another user, the work runs on GPU 0;
DPO rounds use every client question; sampling moves to vLLM in the server's
WSL venv, checked first against HF (`vllm_s0/bench_sql`); evaluation may move
to vLLM if it matches HF on FedAvg R3; the server epochs stay a curve; the
stopping rule is to be automated; the SQL-only baselines leave the queue
until the main pipeline has run.

## 2026-11-08: every line run as a curve on Spider test

No run. Owner decision: evaluate each stage on Spider test and continue from
the best checkpoint (stop after 2 steps without a gain of more than 1 point;
maxima: server 3 epochs, client SFT 5 rounds, DPO 4 rounds), the same rule for
the baselines. Queue now holds the server epoch choice (1 and 2 epochs, full
runs) and FedAvg R1-R2 evaluations; the client rounds and the query-plan DPO
rounds are queued after each decision.

## 2026-11-08: full CoT pipeline queued, probe ablations dropped

No run. Owner decision: measure the whole method first and adjust from its
signals. Queue (`PIPELINE_NEXT.md`, phase `fedcot_s0`): server SFT from the
base model on the 4,109 teacher-plan BIRD rows, three FedAvg client rounds on
plans derived from gold SQL, two rounds of federated DPO + NLL on the
clients' own sampled plan + SQL (200 questions per client), Spider test after
round 3 and each DPO round. Dropped: the CoT probe arms, the RFT arm, teacher
headroom and pass@8. Kept as baselines: FedAvg R4-R5 and SQL-only DPO R1-R2
from R3. The pipeline starts from the base model rather than R3 so that the
plan format comes before any federated round and the client rounds match the
baselines (five). New code (nested repo): `--response-format qp_cot_v1` and
`--parent-stage` in `experiments/federated_pref/run.py`; unparsed samples are
rejected as format errors, the gold fallback is the derived plan + gold SQL.

## 2026-11-07: Spider test becomes the Spider metric; queue revised after a review

No run. Owner decisions: every Spider number is Spider test from now on;
Spider dev is skipped or a secondary diagnostic (rule in both `AGENTS.md`).
Choices are made on Spider test, so it is not called held-out. One seed for
this signal round. The owner wants one feasible CoT-with-teacher test.

An independent review (owner-allowed archive reading) recommended SQL-only
federated DPO + NLL as the main line and judged the archived CoT routes weaker
evidence than first stated (best-on-dev selection, matched rounds only -1.55,
no isolated prompt-format test). Accepted: the sample label note in
`DIRECTION.md` now matches the code (EX on the client's original database
only, no test-suite variants for Spider train).

Queue (`fedicl-sql/queues/active.toml`, `PIPELINE_NEXT.md`): every evaluation
on Spider test and BIRD dev; teacher headroom on Spider test (R3 71.50); R3
pass@8 stays on Spider dev as a diagnostic; an SFT round 5 control so the SFT
rounds match DPO round 2; the CoT probe now chains each server stage (teacher
plan, plan from SQL, SQL only) into one client round in the same format and
evaluates only after the client round. New code: `--parent-stage` in
`experiments/federated/run.py` resolves a committed stage row by its stage
name (nested repo, with a test).

## 2026-11-07: queue 2 written (headroom check, CoT probe server side)

No run. `PIPELINE_NEXT.md` queue 2: teacher 4-bit greedy and R3 pass@8 on
Spider dev; three server SFT stages from R3 on the 4,109 teacher-plan BIRD rows
(teacher plan, plan derived from the SQL, SQL only); one client round with
gold-derived plans. New code: `scripts/pass_at_k.py`; `scripts.eval_standard`
gained `--model-4bit` and `--response-format`. The round-1 publish step now
fast-forwards before pushing.

## 2026-11-07: CoT design for S5

No run. Owner accepts CoT at inference if the cost is feasible. Literature
(`LITERATURE.md` 1.7): on Spider greedy, CoT SFT alone stays below SQL-only and
leads only after execution-labelled DPO. Chosen design (`DIRECTION.md` 6.5):
structured query plan (`qp_cot_v1`, 512-token cap) from the existing 4,109
teacher plans on BIRD, one prompt for server SFT, client sampling and eval,
clients train on CoT too. Probe of 7 arms, about 20 GPU-h (`DIRECTION.md` 6.3).

## 2026-11-07: direction note reorganized, server options ranked

No run. `DIRECTION.md` rewritten as client choice (C1-C4) + server option
(S0-S5) + timing; owner allowed SynSQL as server data. A literature pass
(`LITERATURE.md` section 1.7) found no evidence that SQL-only KD or RL on public
data adds 2+ points greedy Spider EX once the student has seen Spider; CoT (S5)
with client execution training has the strongest support. Proposed order:
teacher headroom and R3 pass@8 on Spider dev (about 2 GPU-h), then an S5 probe
if CoT at inference is accepted, then a KD probe on SynSQL if the teacher is
4+ points above R3. Proposed drops: S3 on SynSQL, S4. Also noted: FedAvg R3 is
3.8 points below centralized SFT on Spider dev (67.60 vs 71.37), level on test.

## 2026-11-07: next direction, a server step on public BIRD

No run. Proposal recorded in `DIRECTION.md` section 8, to follow the Direction
1 verification: the server adds knowledge the clients lack, using what only it
has. Main option: on-policy KD from the frozen teacher on BIRD, gated to
questions where the teacher SQL matches gold; fallback: execution RL/DPO on
BIRD. Teacher is not used to correct student SQL (it matches gold on 56% of
BIRD train, and the server has gold). Placement: one server stage before the
client rounds first (E1, server side only from FedAvg R3), then after each
aggregation if E1 raises Spider dev. `LITERATURE.md` gained section 1.6
(clause- and token-level preference and RL, SQLoom read in full) and FedAuto.

## 2026-11-06: federated DPO + NLL pipeline, FedAvg reference reused

No run yet. Owner decisions: Direction 1 (federated on-policy DPO + NLL, no
teacher) first; reuse the earlier FedAvg SFT run `p227_fl_aaa_s0` (seed 0,
code SHA 3582656, 3 rounds, 1 local epoch) as the federated baseline and the
start point. Its recorded EX (earlier run, owner-approved reference): Spider
dev 67.60 (R3; R2 68.28), Spider test 71.50 (R3, one reference pass, no choice
made on it), BIRD dev 25.68 (R3); centralized SFT e3 71.37 dev, 71.08 test.

New code in `fedicl-sql`: on-policy sampling with execution labels,
preference pairs, a resumable DPO + NLL trainer with an RFT weight, a
federated round runner (`experiments/federated_pref/run.py`), a standard
evaluation runner and contract (`scripts/eval_standard.py`) and a test-suite
EX scorer. Sampling, prompt, decoding budget and DPO schedule follow the
earlier SQL-only DPO rounds; the prompt equals the evaluation prompt. A local
end-to-end smoke (2 clients, 3 questions) passed on the Mac. Queued in
`PIPELINE_NEXT.md`: GPU smoke, rounds 1-2 of DPO and RFT from FedAvg R3, one
more FedAvg SFT round as a control, evaluation on Spider dev and BIRD dev.

## 2026-11-06: literature review and direction proposals

No run. New `LITERATURE.md` lists the closest verified work (federated
learning with a server LLM, federated Text-to-SQL and code, federated DPO and
RLVR, small-model Text-to-SQL training, LLM-to-SLM distillation) and the gaps
for our setup. New `DIRECTION.md` proposes four directions, revised after one
round of independent Q3-reviewer critique, and recommends iterative federated
DPO with execution-labelled pairs built at each client (no teacher), with
teacher CoT plus federated DPO as the choice if the teacher must contribute.
Owner input used: client drift is negligible and DPO is effective in this
setup (earlier observations, to be re-measured). Waiting for the owner to
choose a direction and to settle whether the teacher is optional
(`RESEARCH_STATE.md`) or required (`AGENTS.md`).

## 2026-11-06: teacher becomes optional

Owner decision: the goal is a method that clearly beats the federated
baselines on the clients' domain. Using the server teacher is an option, not
a requirement; a method without it is acceptable if it is strong enough. If
the teacher is used, it still runs only at the server on public data.

## 2026-11-06: reuse of earlier outputs, storage, checkpoints, progress

Owner decision: teacher outputs on BIRD (SQL targets, logit cache, checked
CoT) and processed data may be reused freely; starting from an earlier
adapter or comparing with an earlier result needs the owner's approval;
earlier interpretations and result numbers stay hidden. Teacher outputs on
Spider train are excluded because Spider train is client data. New
`fedicl-sql/docs/SERVER_STORAGE.md` lists the reusable assets and sets the
rules for server storage (never delete or overwrite `artifacts/`), resume by
rerun, and progress output for long jobs.

## 2026-11-06: lighter process rules

Owner found the inherited process rules too rigid. `AGENTS.md` now separates
a short list of hard rules (honesty, data roles, GPU memory budget, evaluator
budgets, server checkout safety, no weights in Git, Git identity) from
defaults that may be skipped when another way is simpler. `CONVENTION.MD` was
cut to the repository layout and the essentials; the full earlier versions
are in `archive/paper/fresh_start_2026-11-05/`.

## 2026-11-05: fresh start

Owner decision: archive every earlier decision, result and literature note so
that new work is not bound by them. Kept: the topic, the fixed setup
(`RESEARCH_STATE.md` section 2), the Q3 goal (the measurable-teacher part
was dropped on 2026-11-06), the honesty rules, and the infrastructure and Git rules. Open:
method and metrics. Archived material is hidden unless the owner asks for it
in a session.
