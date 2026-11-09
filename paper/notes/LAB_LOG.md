# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

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
