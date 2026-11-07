# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

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
