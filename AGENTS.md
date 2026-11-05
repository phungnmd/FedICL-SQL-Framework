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

## Fresh start (owner, 2026-11-05)

The project restarted on 2026-11-05. Every earlier direction, decision,
result, lesson and literature note is archived and hidden:

- Do not read, cite or reason from material dated before 2026-11-05 unless
  the owner asks for it in the current session. This covers `paper/archive/`,
  the nested `docs/archive/` and `scripts/archive/`, the result directories
  committed before that date (`fedicl-sql/experiments/*/results/`), earlier
  adapters and checkpoints, and old commits read for their results.
- Earlier results are not baselines, parents, priors or reasons for or
  against a choice. Measure what the new work needs from scratch.
- Infrastructure facts stay in force: the GPU measurements in
  `fedicl-sql/docs/A5000_RUN_CONFIG.md`, the evaluator protocol in
  `fedicl-sql/docs/PROTOCOL_V2.md`, and the server and Git rules below.
- The code under `fedicl-sql/fedicl_sql/` and `experiments/` is tooling and
  may be reused freely. The old `scripts/run_p2*_*.py` runners belong to the
  archived work; new experiments get new runners.

## What the project is

Paper: *FedLS-SQL* (working title), aimed at a Q3 journal. Question, fixed
setup and open choices: `paper/notes/RESEARCH_STATE.md`.

- Fixed (owner): the topic (federated Text-to-SQL, a frozen LLM teacher at the
  server, an SLM trained by clients and deployed alone) and the setup
  (Qwen2.5-Coder-1.5B-Instruct student, Qwen2.5-Coder-7B-Instruct teacher,
  5 Spider clients on the `alpha_0.1/k5` split, BIRD train with evidence as
  the server's public data).
- The teacher runs only at the server, on public data. Clients never send
  data.
- Compute is the two RTX A5000 cards. A direction must fit that budget in
  memory and run time.
- Goal: a federated framework in which the server teacher contributes
  measurably. A story that reduces the teacher to an ablation does not meet
  this goal. Look for directions that keep a real teacher contribution, and
  say plainly if none is supported.
- Open: the method and the metrics. Propose them from the task itself.
- Novelty for Q3: a published mechanism adapted to federated Text-to-SQL with
  a task-specific adaptation is acceptable. Cite the closest work and state
  what differs; never claim "first" and never hide the closest prior work.
- Judging the Q3 bar: when asked whether a result, the method or the story is
  strong enough, judge as an impartial reviewer at the target venues
  (`RESEARCH_STATE.md`) would, compared with recent accepted papers in
  federated learning, LLM-to-SLM distillation and Text-to-SQL. Say with the
  numbers what a reviewer would likely accept, question or reject, including
  weaknesses that argue against the current direction. The owner decides.

## Read first

1. `paper/notes/RESEARCH_STATE.md`: question, fixed setup, what is open, what
   we know, current phase.
2. `paper/notes/PIPELINE_NEXT.md`: the only executable queue.
3. `paper/notes/LAB_LOG.md`: every run, result and decision since the fresh
   start.
4. `CONVENTION.MD`: repository layout, command contract (section 6.1), result
   retention, statistics, Git discipline.

Create `DIRECTION.md`, `LITERATURE.md` or `RESULT_REGISTRY.md` in
`paper/notes/` only when the work needs them. Do not create parallel tracker
files.

## Evidence rules

Fixed (owner), all about honesty:

- Every number in the paper has a checkpoint, config, dataset, seed,
  prediction file and Git SHA trail. A result reported only in chat is logged
  as "not committed" and stays out of the paper until it is committed.
- The paper never misstates how a number was obtained: every number names its
  set (dev or test), and a test number is not called held-out once a choice
  (setting, arm, checkpoint, claim) was made by looking at it.
- Statistics are computed correctly: pooled seeds use the question-clustered
  test (per-question mean over seeds, test across questions), never summed
  discordant pairs.

Everything else is practice and gives way whenever another choice makes the
paper better. Never block an option, and never call a result invalid, because
a practice was skipped; if a reviewer could object, say so in one line. Log
every run and every choice in `LAB_LOG.md`. Privacy is structural data
isolation, not formal differential privacy.

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
- The server checkout has `core.autocrlf=true`: every file it pulled is CRLF
  on disk (including `processed_data` inputs whose hashes are in run
  identities), while files it wrote are LF. Publication fetches and
  fast-forwards (`git merge --ff-only origin/main`) before committing and
  never rebases a local result commit: a rebase rewrites the replayed files
  as CRLF and breaks the byte hashes in receipts and manifests. Never
  renormalize line endings on the server during a phase.
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
- Student training uses `--lm-loss target_fp32` and `logits_to_keep`: the
  standard causal-LM loss over the response window only. The CLI requires
  `--lm-loss` explicitly. `full_bf16` on BIRD at 7,168 tokens paged about
  71 GB and took 16.4 h. State the loss mode whenever runs with different
  modes are compared.
- Required settings are enforced inside the runners (memory cap 0.88,
  allocator, long-example probe, evaluation batch 16). Prefer enforcement in
  code over documentation.
- Teacher generation: 4-bit, batch 8, `--exec-workers 4`. Evaluation: batch 16.
  Never lower the 30 s BIRD or 60 s Spider execution budgets.
- Every new GPU path gets a smoke that reports peak reserved VRAM. Add every new
  measurement to `fedicl-sql/docs/A5000_RUN_CONFIG.md`.
- Set `CUDA_DEVICE_ORDER=PCI_BUS_ID` with `CUDA_VISIBLE_DEVICES`.

## Repository discipline

- Commit paper, docs, and archive changes in this repository; code and results
  inside `fedicl-sql/`. Keep the two histories separate.
- Preserve old artifact paths and run IDs; presentation names may change.
- Resume and cache identities never contain a Git SHA or timestamp.
- Move superseded material to the archive with an index entry instead of
  deleting it. Keep reference PDFs private, outside the releasable inner repo.
- Make small, logical commits with conventional messages. Commit messages never
  mention AI tools. Never change the Git author identity or configuration.
- Work in the owner's checkouts (`/Users/edric/Learning/FedICL-SQL` and its
  `fedicl-sql/`), on `main` unless the queue names another branch, so the
  owner's editor shows every change. Do not create a Git worktree, least of
  all in a temporary directory. If one is unavoidable, tell the owner its path
  and branch, and remove it (`git worktree remove`) when the work is pushed.
  Before editing, check `git worktree list` and the current branch.

## Writing for the owner

- The owner works alone and is learning ML. Dense, cross-referenced documents
  are hard to follow. Use plain words, track progress by runnable step and
  trained artifact rather than paper labels, and prefer fewer documents.
- Replies in Vietnamese keep common technical terms in English (pipeline,
  prompt, token, fallback, ablation, and similar).
- No emojis. No em dashes; use commas, parentheses, colons, or hyphens.

## Writing reports for the advisor

From the owner's edits (2026-10-29). These are tendencies, not checks; follow
what reads best.

- Let tables carry the numbers. Remarks say what the numbers mean in plain
  words, with only the few numbers a point rests on.
- Highlight the best value of each column in result tables, also when it is
  not the method.
- Prefer plain verdicts ("cùng chiều nhưng chưa rõ rệt") over p-values and
  test names.
- Leave lab-process talk out (selection, which seed chose what, runs still
  missing); the plan section covers progress.
- Describe a changed setting briefly, without implementation details.
- Frame the discussion as points to consider (section "Thảo luận")
  rather than problems.
