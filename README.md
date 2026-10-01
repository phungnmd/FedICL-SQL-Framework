# FedLS-SQL

Research repository for the paper *FedLS-SQL: A Novel Federated Large-Small
Language Models Framework for Natural Language to SQL*.

FedLS-SQL trains a small model (Qwen2.5-1.5B) on private Text-to-SQL data
held by federated clients, and uses a frozen large model (Qwen2.5-Coder-7B) on
the server, on public data only, to improve it. Only the small model is
deployed. The final method is not chosen yet.

The research question is:

> Can large-to-small language model collaboration overcome the accuracy
> limitations of lightweight federated NL-to-SQL models while retaining the
> privacy, communication-efficiency, and resource advantages of federated
> learning?

Start here (in this order):

1. `paper/notes/system_architecture.md` — the method and what we may claim.
2. `paper/notes/LAB_LOG.md` — current evidence, newest first.
3. `paper/notes/PIPELINE_NEXT.md` — the only list of commands to run.
4. `paper/notes/RESULT_REGISTRY.md` — where every number and adapter came from.
5. `paper/notes/EXPERIMENT_MATRIX.md` — research questions, evidence plan, and
   the paper-closure checklist.

Other active files:

- Paper result tables: `paper/results/MAIN_RESULTS.md`
- Manuscript outline: `paper/drafts/fedls_sql_outline.md`
- Novelty and claim limits: `paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`
- ICL negative result: `paper/notes/ICL_NEGATIVE_RESULT.md`
- Archive index (old logs, reviews, runbooks): `paper/archive/README.md`
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
