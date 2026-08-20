# FedLS-SQL — Paper Workspace Guide

This outer repository is the private paper workspace for *FedLS-SQL: A Novel
Federated Large-Small Language Models Framework for Natural Language to SQL*.
The nested `fedicl-sql/` directory is a separate Git repository containing code
and committed experiment evidence.

## Canonical project model

FedLS-SQL trains a Qwen2.5-1.5B SLM with private client LoRA updates,
sample-weighted factor-wise FedAvg, and server-side CE/reverse-KL distillation
from a frozen Qwen2.5-Coder-7B teacher on a fixed 3,873-row public BIRD pool.
Deployment uses only the SLM. Canonical runs use no ICL.

## Read first

1. `paper/notes/system_architecture.md` — method and claim boundaries.
2. `paper/notes/LAB_LOG.md` — compact current evidence ledger.
3. `paper/notes/PIPELINE_NEXT.md` — only active executable queue.
4. `paper/notes/RESULT_REGISTRY.md` — canonical labels and checkpoints.
5. `paper/notes/EXPERIMENT_MATRIX.md` — RQ-to-evidence status.

Historical FedICL, ICL, FLoRA-NA, early PoC, email, and report material lives
under `paper/archive/pre_fedls_2026-08/`. Do not use archived documents as the
current method specification.

## Non-negotiable distinctions

- Paper name: **FedLS-SQL**.
- Internal package: `fedicl_sql` remains unchanged for compatibility.
- `fedkd` is an internal arm name, not the paper name.
- A pre-server adapter at T2/T3 inside a `fedkd` lineage is not pure FL because
  it inherits earlier KD.
- The public method pool has 3,873 rows; larger pools are historical candidates.
- Privacy is structural data isolation, not formal differential privacy.
- The implemented server objective is teacher-target CE plus reverse KL, not a
  separate structural-distillation mechanism.

## Repository discipline

- Commit paper/docs/archive changes in this repository.
- Commit code/results changes inside `fedicl-sql/`.
- Preserve old artifact paths and run IDs; presentation names may change.
- Move superseded material to archive with an index instead of deleting it.
- Keep reference PDFs private and outside the releasable inner repository.
- Never copy a result into the paper without a checkpoint, config, dataset,
  seed, prediction file, and Git SHA trail.

## Current priority

Run the independent pure-FL T1-T3 branch, fill the final Centralized/FL/FedLS
table, consolidate communication/resource metrics, then replicate the
multi-round trajectory. ICL, FLoRA-NA, SC, and T4/T5 are not active work.
