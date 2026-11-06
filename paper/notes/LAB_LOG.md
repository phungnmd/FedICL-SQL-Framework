# FedLS-SQL: lab log

Every run, result and decision since the 2026-11-05 fresh start, newest on
top. A result reported only in chat is logged as "not committed".

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
(`RESEARCH_STATE.md` section 2), the Q3 goal with a measurable teacher
contribution, the honesty rules, and the infrastructure and Git rules. Open:
method and metrics. Archived material is hidden unless the owner asks for it
in a session.
