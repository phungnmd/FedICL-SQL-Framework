# FedLS-SQL — Paper Workspace Guide

This outer repository is the private paper workspace for *FedLS-SQL: A Novel
Federated Large-Small Language Models Framework for Natural Language to SQL*.
The nested `fedicl-sql/` directory is a separate Git repository containing code
and committed experiment evidence.

## Canonical project model

FedLS-SQL trains a Qwen2.5-1.5B SLM with private client LoRA updates,
sample-weighted factor-wise FedAvg, and server-side knowledge transfer from a
frozen Qwen2.5-Coder-7B teacher on a public pool. Protocol v2 uses explicit
dataset profiles (BIRD with evidence). The primary direction is Spider private
clients with a BIRD public pool; BIRD private with a Spider public pool is the
reverse check. The final method is not frozen: the current reference ends at
one public stage (SeqKD, or full public-gold CE plus Hinton forward KL), and
terminal private consolidation (`A>K[fkl]>A`) is the active candidate.
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
- A stage chain containing `K` (for example `A>K[fkl]>A`) is not pure FL; only
  all-`A` chains are FL controls.
- Protocol-v2 BIRD public pools: all 9,428 training rows for public-gold CE and
  Hinton KD; 5,319 execution-selected teacher targets for SeqKD. The 3,873-row
  pool is protocol-v1 history.
- Privacy is structural data isolation, not formal differential privacy.
- The implemented server objectives are teacher-target CE (SeqKD) and gold CE
  plus Hinton forward KL (`T=2`). Reverse KL/KID are archived; there is no
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

Execute P2.10 from `paper/notes/PIPELINE_NEXT.md`: Struct-SQL QP-CoT in every
stage (runner `scripts/run_p210_struct_sql.py`) with a plain terminal stage
(`$L = 0`), on nested branch `experiment/terminal-retention`. P2.9 is paused
after retention at λ = 1.0 failed its gates; its remaining variants and the
target-NLL diagnostic are deferred and resumable. Extra seeds, recurrence, and
new KD objectives wait for the P2.10 gate. ICL, FLoRA-NA, SC, and T4/T5 are not
active work.
