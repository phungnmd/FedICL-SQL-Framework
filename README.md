# FedExec-SQL

Workspace of the paper *FedExec-SQL*: federated Text-to-SQL
where clients train a small model (Qwen2.5-Coder-1.5B-Instruct) on private
data and only that model is deployed.

Start here:

1. `paper/notes/RESEARCH_STATE.md`: question, setup, method, what is open.
2. `paper/notes/PIPELINE_NEXT.md`: what to run now and what is running.
3. `paper/notes/LAB_LOG.md`: runs, results and decisions, newest first.
4. `paper/notes/WRITING_PLAN.md`: how the manuscript in
   `paper/manuscript/` is written.

Also: `paper/notes/LITERATURE.md` (related work), `paper/references/`
(private source library), `paper/templates/` (venue templates).

Two repositories on purpose. This one holds the paper material. The code,
processed data and committed results are in `fedicl-sql/`, a separate Git
repository (Python package `fedls_sql`) and the only one on the GPU server.

Rules for agents: `AGENTS.md`. Work from before the clean reset of
2026-11-17 is at the tag `archive/pre-reset-2026-11-17` in each repository
and in the local `archive/` folder.
