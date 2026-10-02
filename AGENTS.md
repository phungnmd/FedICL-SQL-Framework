# FedLS-SQL paper workspace: agent guide

This is the canonical instruction file for every coding agent working in this
workspace (Codex, Claude Code, and others). `CLAUDE.md` imports it. Put every
durable rule, run configuration, and lesson here, not only in `CLAUDE.md` or in
an agent's private memory.

The nested `fedicl-sql/` directory is a separate Git repository (code and
committed experiment evidence) with its own `fedicl-sql/AGENTS.md`. An agent
started inside `fedicl-sql/` does not read this file, so code and GPU rules must
also live there. The GPU server holds only `fedicl-sql/`.

## What the project is

Paper: *FedLS-SQL: A Novel Federated Large-Small Language Models Framework for
Natural Language to SQL*, aimed at a Q3 journal. It needs a positive headline.

FedLS-SQL trains a Qwen2.5-1.5B SLM with private client LoRA updates,
sample-weighted factor-wise FedAvg, and server-side knowledge transfer from a
frozen Qwen2.5-Coder-7B teacher on a public pool. Protocol v2 uses explicit
dataset profiles (BIRD with evidence). Main direction: Spider private clients,
BIRD public pool; BIRD private with a Spider public pool is the reverse check.
Deployment uses only the SLM. Canonical runs use no ICL.

- Main metric: final Spider EX (private data). Target: the federated SLM
  approaches centralized training at the same number of Spider epochs
  (centralized plus BIRD gold is a higher ceiling).
- Success criterion: a chain-of-thought KD method whose final
  `A>K>A...` Spider EX beats `A>K[full BIRD gold]>A...` and Hinton at the same
  number of private rounds. Current references at `A>K>A`, seed 0: Hinton
  66.63, full gold 66.54, centralized Spider-only 67.31.
- Ground every method component in a published paper and name it. Flag any
  component that has no source instead of inventing one silently.

## Read first

1. `paper/notes/PIPELINE_NEXT.md`: the only active executable queue.
2. `paper/notes/LAB_LOG.md`: compact evidence ledger and decisions.
3. `paper/notes/system_architecture.md`: method and claim boundaries.
4. `paper/notes/RESULT_REGISTRY.md`: canonical labels and checkpoints.
5. `paper/notes/EXPERIMENT_MATRIX.md`: research question to evidence status.
6. `CONVENTION.MD`: repository layout, command contract (section 6.1), result
   retention, statistics, Git discipline.

Archived material (FedICL, ICL, FLoRA-NA, early PoC, superseded runbooks) lives
under `paper/archive/`. Never use it as the current method specification.

## Current state (2026-10-02)

- Active: P2.15 on nested branch `experiment/fullgold-plan`. Struct-SQL data
  over all 9,428 BIRD train rows (teacher plan and SQL written together, kept
  only when the SQL is execution-correct; Thaker and Bresler, arXiv 2512.17053)
  trained with Distilling Step-by-Step (plan as a separate task; Hsieh et al.,
  Findings ACL 2023), plan weight 0.8 (PARSQL, Findings ACL 2025). Arms `gold`
  and `dss`, one public epoch, then SQL-only FedAvg rounds (`A>K>A`, then
  `A>K>A>A` and `A>K>A>A>A`). Hinton is the committed `A>K[fkl]>A` row, extended
  with the same extra rounds. Clients and inference stay SQL-only.
- The question is only whether `dss` beats gold and Hinton. Where the gain comes
  from (teacher SQL or plan) is not needed.
- Done: P2.14 (1,000 rows, 3 epochs): the plan task gave Spider +1.84 after
  FedAvg at seed 0 (nested results `e622e1f`), the first KD variant whose
  Spider edge appears after FedAvg instead of disappearing.
- Why clients stay SQL-only: in P2.10, template plans at the clients made the
  FedAvg model weak before any KD (QP T1 Spider 41.9 versus SQL-only 57.35).
- Closed: P2.13 (superseded before training), P2.10 (stopped), A1 weight-merge
  gate (failed; results not committed). Paused: P2.9 retention.
- Known pattern: every KD variant so far (Hinton, SeqKD, KID) beats gold right
  after K, and the edge on Spider disappears after the next private round.
- Not active: A2 interleaving, P2.11, P2.12, A3 depth, an in-domain public pool,
  an unlabeled-pool reframing, ICL, FLoRA-NA, SC, T4/T5.

## Non-negotiable distinctions

- Paper name: **FedLS-SQL**. Internal package `fedicl_sql` stays unchanged.
  `fedkd` is an internal arm name, not the paper name.
- A chain containing `K` (for example `A>K[fkl]>A`) is not pure FL; only all-`A`
  chains are FL controls. A pre-server adapter at T2/T3 inside a `fedkd` lineage
  inherits earlier KD and is not pure FL.
- Protocol-v2 BIRD public pools: all 9,428 training rows for public-gold CE and
  Hinton KD; 5,319 execution-selected teacher targets for SeqKD; the 1,000
  Struct-SQL admitted rows for P2.14. The 3,873-row pool is protocol-v1 history.
- Privacy is structural data isolation, not formal differential privacy.
- Implemented server objectives: teacher-target CE (SeqKD), gold CE plus Hinton
  forward KL (`T=2`), and an auxiliary plan task next to SQL CE.

## Experiment commands

- `paper/notes/PIPELINE_NEXT.md` is the only owner of runnable commands. Move
  finished or superseded command blocks to a dated file under
  `paper/archive/completed_runbooks/` or `superseded_runbooks/` and link it.
- Commands target PowerShell on the Windows server, one physical line each,
  run from the `fedicl-sql/` root, define every variable they use, and throw
  after any non-zero exit. Follow `CONVENTION.MD` section 6.1 in full.
- Server commands touch only `fedicl-sql/`; the paper repository is not on the
  server. Push the paper repository whenever a runbook changes, and give the
  exact commands in chat as well.
- Every run has a separate publication command: empty index check, explicit
  allowlist of compact files, staged-set check, commit, then push.
- Do not pull, switch, edit, or commit in the server working copy while a lane
  runs. Do not push new commits to a nested branch whose running lane will push
  its own result commit later; that push would be rejected.
- For `experiments/client_train/run.py` with `--epochs` greater than 1: pass
  `--save-epoch-checkpoints`; adapter-only snapshots go to
  `<out>/epochs/epoch_N`; the only resumable optimizer state is
  `<out>/resume_latest`; resume by rerunning the exact command and output root;
  extend a finished run only from `resume_latest` into a new output root with
  the new total `--epochs` and `--allow-epoch-extension`, and never describe an
  extended cosine horizon as identical to one planned from step zero.

## GPU rules (details in `fedicl-sql/docs/A5000_RUN_CONFIG.md`)

- Two RTX A5000 24 GB cards under WDDM. WDDM never raises CUDA OOM; it pages
  VRAM to host RAM and the job silently slows down. Keep peak reserved VRAM
  under about 21.5 GiB and the process's shared GPU memory near zero.
- Student training uses `--lm-loss target_fp32` and `logits_to_keep`. It is the
  standard causal-LM loss (Hugging Face upcasts logits to fp32) over the
  response window only. The CLI requires `--lm-loss` explicitly. `full_bf16` is
  legacy: only for the KD trainers and for reproducing committed rows; on BIRD
  at 7,168 tokens it paged about 71 GB and took 16.4 h. State the loss mode
  whenever runs with different modes are compared.
- Required settings are enforced inside the runners (memory cap 0.88, allocator,
  long-example probe, evaluation batch 16). Prefer enforcement in code over
  documentation.
- Teacher generation: 4-bit, batch 8, `--exec-workers 4`. Evaluation: batch 16.
  Never lower the 30 s BIRD or 60 s Spider execution budgets.
- Every new GPU path gets a smoke that reports peak reserved VRAM. Add every new
  measurement to `fedicl-sql/docs/A5000_RUN_CONFIG.md`.
- Set `CUDA_DEVICE_ORDER=PCI_BUS_ID` with `CUDA_VISIBLE_DEVICES`.

## Evidence rules

- Never copy a result into the paper without a checkpoint, config, dataset,
  seed, prediction file, and Git SHA trail. A result reported only in chat is
  logged as "not committed" and stays out of the paper.
- Screens are seed 0 with paired questions and exact McNemar tests. One Spider
  question is about 0.1 point; small differences need more seeds before any
  claim.
- Resume and cache identities never contain a Git SHA or timestamp.

## Repository discipline

- Commit paper, docs, and archive changes in this repository; code and results
  inside `fedicl-sql/`. Keep the two histories separate.
- Preserve old artifact paths and run IDs; presentation names may change.
- Move superseded material to the archive with an index entry instead of
  deleting it. Keep reference PDFs private, outside the releasable inner repo.
- Make small, logical commits with conventional messages. Commit messages never
  mention AI tools. Never change the Git author identity or configuration.
- Work in the owner's checkouts (`/Users/edric/Learning/FedICL-SQL` and its
  `fedicl-sql/`), on the branch named in the active queue, so the owner's
  editor shows every change. Do not create a Git worktree, least of all in a
  temporary directory. If one is unavoidable, tell the owner its path and
  branch, and remove it (`git worktree remove`) when the work is pushed.
  Before editing, check `git worktree list` and the current branch.

## Writing for the owner

- The owner works alone and is learning ML. Dense, cross-referenced documents
  are hard to follow. Use plain words, track progress by runnable step and
  trained artifact rather than paper labels, and prefer fewer documents. Do not
  create parallel tracker files.
- Replies in Vietnamese keep common technical terms in English (pipeline,
  prompt, token, fallback, ablation, and similar).
- No emojis. No em dashes; use commas, parentheses, colons, or hyphens.
