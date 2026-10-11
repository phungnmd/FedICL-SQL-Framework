# FedLS-SQL

Research repository for the paper *FedLS-SQL* (working title; subtitle open).

FedLS-SQL trains a small model (Qwen2.5-Coder-1.5B-Instruct) on private
Text-to-SQL data held by federated clients, and uses a frozen large model
(Qwen2.5-Coder-7B) on the server, on public data only, to improve it. Only
the small model is deployed. No method or paper story is fixed yet; the
project is in an exploration phase.

Start here (in this order):

1. `paper/notes/RESEARCH_STATE.md`: the question, what we know, what is open,
   and the current phase.
2. `paper/notes/LAB_LOG.md`: evidence and decisions, newest first.
3. `paper/notes/PIPELINE_NEXT.md`: the only list of commands to run.
4. `paper/notes/system_architecture.md`: setup, data rules, claim limits.
5. `paper/notes/RESULT_REGISTRY.md`: where every number and adapter came from.

Other active files:

- Related work and claim limits: `paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`,
  `paper/notes/related_papers.md`
- Archive index (old logs, directions, reviews, runbooks): `paper/archive/README.md`
- Code: `fedicl-sql/`

**Two-repo layout (intentional):** this outer repo contains private paper
materials, plans, and references. `fedicl-sql/` is a separate Git repository
containing code and the reproducibility trail. The legacy Python namespace
`fedicl_sql` is retained for compatibility; old artifact paths and run IDs are
immutable provenance identifiers, not presentation names.

The training server may contain only the inner code repository. Paper-facing
commands must therefore avoid runtime dependencies on this outer repository;
compact result artifacts are pushed from the server and reconciled with the
registry and paper tables here.

---

## Convention

Project conventions live in [`CONVENTION.MD`](CONVENTION.MD). That file is the
single source of truth for repository layout, data handling, experiment
provenance, stage discipline, and paper artifact generation.
