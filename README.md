# FedLS-SQL

Research repository for the paper *FedLS-SQL: A Novel Federated Large-Small
Language Models Framework for Natural Language to SQL*.

FedLS-SQL combines private client-side LoRA fine-tuning of a lightweight SLM,
sample-weighted FedAvg, and server-side knowledge distillation from a frozen
LLM on a public Text-to-SQL pool. The deployed model is the SLM; the teacher is
not required at clients or at inference time.

The current research question is:

> Can large-to-small language model collaboration overcome the accuracy
> limitations of lightweight federated NL-to-SQL models while retaining the
> privacy, communication-efficiency, and resource advantages of federated
> learning?

- Canonical architecture and terminology: `paper/notes/system_architecture.md`
- Active experiment queue: `paper/notes/PIPELINE_NEXT.md`
- RQ-to-evidence map: `paper/notes/EXPERIMENT_MATRIX.md`
- Canonical paper result tables: `paper/results/MAIN_RESULTS.md`
- Checkpoint/evaluation artifact map: `paper/notes/RESULT_REGISTRY.md`
- Complete research history: `paper/notes/LAB_LOG.md`
- Superseded FedICL/ICL material: `paper/archive/pre_fedls_2026-08/`
- Code: `fedicl-sql/`

**Two-repo layout (intentional):** this outer repo contains private paper
materials, plans, and references. `fedicl-sql/` is a separate Git repository
containing code and the reproducibility trail. The legacy Python namespace
`fedicl_sql` is retained for compatibility; old artifact paths and run IDs are
immutable provenance identifiers, not presentation names.

---

## Convention

Project conventions live in [`CONVENTION.MD`](CONVENTION.MD). That file is the
single source of truth for repository layout, data handling, experiment
provenance, stage discipline, and paper artifact generation.
