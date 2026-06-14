# FedICL-SQL

Research repo for the paper *FedICL-SQL: A Novel Federated Large-Small Language
Models Framework with In-Context Learning for Natural Language to SQL* (target:
IAJIT, WoS-Q3).

- Method mechanism: `paper/notes/fig1_architecture.md`
- Build & experiment plan: `paper/notes/detailed_plan.md`
- Execution checklist + results: `paper/notes/todo.md`
- Code: `fedicl-sql/` (see `fedicl-sql/README.md` for architecture + quickstart)

**Two-repo layout (intentional):** this outer repo = paper docs/plan/references
(private — reference PDFs must never be published); `fedicl-sql/` = its **own git
repo** (gitignored here, not a submodule) = the code + results evidence trail,
releasable standalone on GitHub at submission (TODO P6). Commit code-stage
progress in the inner repo; commit plan/doc changes here.

---

## Convention

Project conventions live in [`CONVENTION.MD`](CONVENTION.MD). That file is the
single source of truth for repository layout, data handling, experiment
provenance, stage discipline, and paper artifact generation.
