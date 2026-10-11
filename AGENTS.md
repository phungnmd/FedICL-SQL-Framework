# FedLS-SQL paper workspace: agent guide

This is the canonical instruction file for every coding agent working in this
workspace (Codex, Claude Code, and others). `CLAUDE.md` imports it. Put every
durable rule, run configuration, and lesson here, not only in `CLAUDE.md` or in
an agent's private memory.

The nested `fedicl-sql/` directory is a separate Git repository (code and
committed experiment evidence) with its own `fedicl-sql/AGENTS.md`. Codex
started inside `fedicl-sql/`, and any agent on the GPU server (which holds only
`fedicl-sql/`), does not read this file, so code and GPU rules must also live
there. Claude Code started locally inside `fedicl-sql/` loads both files.

## What the project is

Paper: *FedLS-SQL: A Novel Federated Large-Small Language Models Framework for
Natural Language to SQL*, aimed at a Q3 journal. It needs a positive headline.

FedLS-SQL trains a small SLM with private client LoRA updates,
sample-weighted factor-wise FedAvg, and server-side knowledge transfer from a
frozen Qwen2.5-Coder-7B teacher on a public pool. Since P2.27 the student is
Qwen2.5-Coder-1.5B-Instruct and the clients follow the k5 alpha 0.1
domain-cluster split (earlier: Qwen2.5-1.5B-Instruct and Coder-0.5B, alpha
0.5). Protocol v2 uses explicit
dataset profiles (BIRD with evidence). Main direction: Spider private clients,
BIRD public pool; BIRD private with a Spider public pool is the reverse check.
Deployment uses only the SLM. Canonical runs use no ICL.

- Main metrics (owner decision 2026-10-08, fixed before any P2.21 or gold
  K2AAA A3 result was read): two co-primary endpoints of the deployed SLM,
  final Spider EX (private domain) and final BIRD EX (public domain). Since
  rule R10 (2026-10-11) the Spider endpoint of confirmatory claims is Spider
  test (2,147 rows); Spider dev and its derived sets are validation. Claim
  shape: one federated SLM that serves both the clients' domain and the
  public domain. Spider-Realistic/SYN/DK measure robustness; EM is a
  diagnostic. Report a Spider-vs-BIRD plot for every arm.
- Success criterion: against a comparator at the same schedule and number of
  private rounds, (1) BIRD EX gain with exact McNemar p<.05 and (2) Spider
  non-inferiority, meaning the lower bound of the 95% Wald interval for the
  paired Spider EX difference is above -2.0 points. Both must hold
  (intersection-union test, no correction between the two). Comparators: FL
  (pipeline claim), matched public gold (teacher claim), the method without
  its new component (component claim). Centralized Spider+BIRD training is
  the reference ceiling for both domains.
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

## Current state (2026-10-11)

- Paper direction A, final (owner decision 2026-10-11): a framework paper on
  method v1, confirmed on three seeds; no new method. Plan:
  `paper/drafts/paper_direction_2026-10-11.md`; rules R1-R9 in LAB_LOG
  2026-10-11. ExST (S1) and execution-gated KD (S2) are dropped. R10 makes
  Spider test the confirmatory Spider set; R11 adds the K-first (GPT-FL
  style) baseline `hinton_k2aaa` (P2.35), since AKAKA was never shown better
  than K-first. A second
  method study found no candidate above about 5% for the owner criterion.
- Method v1 (fixed 2026-10-08): `A>K[fkl]>A[ntd]>K[fkl]>A[ntd]`, server
  Hinton KD on all 9,428 BIRD rows, client FedNTD (beta 1, tau 3). Teacher
  outputs never leave the server; only adapters move. P2.29 decides whether
  client NTD stays (rule R1).
- P2.27, seed 0 (nested `5604e61`): Hinton v1 - FedNTD BIRD +18.97, Spider
  Wald lower -0.89 (`server_kd` pass); Hinton v1 - gold v1 Spider +1.35,
  p=.23 (`teacher` fail), DK +4.67 (p<.001). FedNTD does not help at 1.5B
  (BIRD -1.37 versus FL). `central` is still running.
- Teacher mechanism (claim C3): Hinton KD forgets the private domain less
  than gold CE during K (Spider +3.48 at K1, +3.00 at K2); the next private
  round repairs gold, so the final gap narrows. Churn analysis A1 and the
  P2.28 audit support this reading.
- P2.28 (nested `238ee10`): pass@8 minus greedy is 13-18 points on client
  training questions, but it needs eight samples and a gold oracle, and half
  of the rescues are 1 or 2 hits out of 8.
- Queue: P2.29 (`h_plain`, running), then seeds 1 and 2 (P2.31, rules R7
  and R8), alpha 0.5 at 1.5B (P2.32), `central_mix` at 1.5B (P2.33).
- Split audit: the k5 alpha 0.1 split is mild cross-silo heterogeneity. The
  FL penalty shows at matched passes (0.5B: +4.6/+4.8 at E1-A1/E2-A2, on JOIN
  and extra-hard questions) and mostly vanishes at E3 because central
  overfits. Its likely cause is fewer effective optimizer steps, not drift.
- Earlier evidence that still stands: Hinton - gold Spider +2.03 (P2.17,
  1.5B-Instruct, p=.033), +2.42 (P2.18, Coder-0.5B, p=.020), +3.77 (P2.25,
  0.5B v1, p=.001). These share test sets: cite them as a consistent
  direction, not as pooled evidence. FedProx AAA is not a stronger FL
  baseline (P2.20). Earlier 0.5B and 1.5B-Instruct adapters are references,
  never parents of new runs.
- Clients and inference stay SQL-only: in P2.10, template plans at the
  clients weakened the FedAvg model before any KD.
- Closed: plan-task directions (P2.10-P2.15), A1 weight merge, P2.9 retention
  loss, KID, GKD, ICL, FLoRA-NA, SC, an in-domain public pool. P2.16
  centralized E1-E4 were never published; do not cite them.
- Both owner checkouts use `main`.

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
  runs. Exception: a runbook step that commits only finished, validated result
  files of a completed arm (never code, run manifests or summaries) and is
  skipped by the final publication. A second exception: a launch step whose
  pull allowlist admits only new files the running lane never imports.
- Do not push new nested commits while a running lane will later push its own
  result commit without pulling first; that push would be rejected. Pushing
  is safe when the next server command pulls them (a launch or publication
  step with an allowlisted pull).
- A new arm that needs both GPUs' outputs waits only for the local validated
  receipt of its parent, never for a Git publication.
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
  response window only. The CLI requires `--lm-loss` explicitly. Hinton KD
  supports it since P2.17. `full_bf16` is legacy: only for the GKD and KID
  trainers and for reproducing committed rows; on BIRD
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
  claim. Paper claims use the pooled three-seed test (rule R7).
- Every decision rule is written in LAB_LOG and committed before the results
  it judges are read. Record the outcome under the original rule; a rule found
  too strict changes only for later runs, never retroactively (P2.27 lesson).
- pass@k on training questions is a ceiling with a gold oracle, not a
  forecast of dev EX (P2.28 lesson).
- Compare central and FL at matched data passes, not only at the final
  checkpoint; a central run past its peak hides the FL penalty (rule R9).
- A subgroup found post hoc on one seed is a hypothesis; confirm it only on
  seeds that did not generate it (rule R8).
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
