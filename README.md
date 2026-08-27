# FedLS-SQL

Research repository for the paper *FedLS-SQL: Execution-Verified
Large-to-Small Knowledge Transfer for Federated NL-to-SQL*.

FedLS-SQL combines private client-side LoRA fine-tuning of a lightweight SLM,
sample-weighted FedAvg, and server-side knowledge distillation from a frozen
LLM on a public Text-to-SQL pool. The deployed model is the SLM; the teacher is
not required at clients or at inference time.

The current research question is:

> Can large-to-small language model collaboration overcome the accuracy
> limitations of lightweight federated NL-to-SQL models while retaining the
> privacy, communication-efficiency, and resource advantages of federated
> learning?

This remains the advisor-level scientific target. The operational evidence
contract and limits for “overcome”, privacy, resources, and large-model FL are
defined in `paper/notes/PAPER_EVIDENCE_PLAN.md`.

- Canonical architecture and terminology: `paper/notes/system_architecture.md`
- Active experiment queue: `paper/notes/PIPELINE_NEXT.md`
- Ordered adaptive paper TODO: `paper/notes/PAPER_TODO.md`
- Related-work and claim-boundary audit: `paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`
- Evidence-mapped manuscript skeleton: `paper/notes/MANUSCRIPT_SKELETON.md`
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

The training server may contain only the inner code repository. Paper-facing
commands must therefore avoid runtime dependencies on this outer repository;
compact result artifacts are pushed from the server and reconciled with the
registry and paper tables here.

---

## Convention

Project conventions live in [`CONVENTION.MD`](CONVENTION.MD). That file is the
single source of truth for repository layout, data handling, experiment
provenance, stage discipline, and paper artifact generation.
