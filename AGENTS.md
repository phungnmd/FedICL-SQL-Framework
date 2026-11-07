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

The project restarted on 2026-11-05. Earlier work falls in three groups
(owner, 2026-11-06; paths in `fedicl-sql/docs/SERVER_STORAGE.md` section 5):

- Reuse freely: teacher outputs on BIRD (SQL targets, logit cache, checked
  CoT) and processed data. They carry no conclusion. Teacher outputs on Spider
  train are not allowed: Spider train is client data.
- Ask the owner first: starting from an earlier adapter, or using an earlier
  result as a baseline or paired comparator.
- Hidden: earlier interpretations, decisions, directions, literature notes
  and lessons (the local `archive/` folder, see below) and the numbers of
  earlier results. Do not read, cite or reason from them unless the owner asks
  in the current session; they are not priors or reasons for or against a
  choice.
- Infrastructure facts stay in force: the GPU measurements in
  `fedicl-sql/docs/A5000_RUN_CONFIG.md`, the evaluator protocol in
  `fedicl-sql/docs/PROTOCOL_V2.md`, server storage, checkpoints and progress
  in `fedicl-sql/docs/SERVER_STORAGE.md`, and the rules below.
- The code under `fedicl-sql/fedicl_sql/`, `experiments/` and the data,
  teacher and audit tools in `scripts/` is tooling and may be reused freely.
  Every old experiment runner moved to the local `archive/` folder; new
  experiments get new runners.

## What the project is

Paper: *FedLS-SQL* (working title), aimed at a Q3 journal. Question, fixed
setup and open choices: `paper/notes/RESEARCH_STATE.md`.

- Fixed (owner): the topic (federated Text-to-SQL, an SLM trained by clients
  and deployed alone) and the setup (Qwen2.5-Coder-1.5B-Instruct student,
  5 Spider clients on the `alpha_0.1/k5` split). Available at the server, use
  optional: a frozen Qwen2.5-Coder-7B-Instruct teacher and BIRD train with
  evidence as public data; SynSQL-2.5M may replace or join it at the server
  (owner, 2026-11-07).
- If the teacher is used, it runs only at the server, on public data. Clients
  never send data.
- Compute is the two RTX A5000 cards. A direction must fit that budget in
  memory and run time.
- Goal (owner, 2026-11-06): a method that clearly beats the federated
  baselines on the clients' domain. The teacher is an option, not a
  requirement; a method without it is acceptable if it is strong enough.
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
2. `paper/notes/PIPELINE_NEXT.md`: commands to run next.
3. `paper/notes/LAB_LOG.md`: runs, results and decisions since the fresh
   start.

Create other notes (direction, literature, result registry) only when the
work needs them. Do not create parallel tracker files.

## Hard rules

Only these are fixed. Each prevents a real failure or protects honesty.

- Honesty: every number in the paper traces to a checkpoint, config, dataset,
  seed, prediction file and Git SHA; a result reported only in chat stays out
  of the paper until committed. Every number names its set (dev or test), and
  a test number is not called held-out once a choice was made by looking at
  it. Pooled seeds use the question-clustered test, never summed discordant
  pairs. Privacy is structural data isolation, not differential privacy.
- Data roles: the teacher, if used, runs only at the server on public data; client data
  never leaves a client; test data never becomes training, retrieval or
  teacher data.
- GPU: WDDM pages VRAM to host RAM instead of raising OOM, so an over-budget
  job only runs slowly. Keep peak reserved VRAM under about 21.5 GiB and check
  memory on the first batch of any new memory-heavy path
  (`fedicl-sql/docs/A5000_RUN_CONFIG.md`).
- Evaluation: never lower the 30 s BIRD or 60 s Spider execution budgets.
  Results that are compared question by question use the same evaluation
  batch size (16 so far).
- Server: it holds only `fedicl-sql/`. Do not pull, edit or commit in the
  server checkout while a job there runs. The server checkout has
  `core.autocrlf=true`: never rebase a result commit there (it rewrites files
  as CRLF and breaks recorded hashes); fetch and fast-forward instead.
- Server commands are PowerShell and each command is one physical line,
  because the owner copy-pastes them over a remote session. A command runs
  from the `fedicl-sql/` root, defines every variable it uses and throws after
  any non-zero exit.
- Server storage: never delete, overwrite, move or rename anything under
  `artifacts/` on the server unless the owner asks with an explicit path list;
  new outputs get their own root.
- Every job longer than a few minutes resumes by rerunning the same command
  and shows progress while it runs (done / total, elapsed, time left, peak
  reserved VRAM; a clear final line; a read-only status command for long
  multi-step jobs). Details: `fedicl-sql/docs/SERVER_STORAGE.md`.
- Never commit adapters, model weights, caches, trainer state or
  `artifacts/`.
- Resume and cache identities never contain a Git SHA or timestamp.
- Git: two separate histories (paper here, code and results in
  `fedicl-sql/`); commit messages never mention AI tools; never change the Git
  author identity or configuration; work in the owner's checkouts on `main`
  (no hidden worktrees; check `git worktree list` before editing).

## Defaults

Use these unless another way is simpler or faster for the task at hand; say
so in one line when you deviate. None of them may block an option or make a
result invalid.

- Server commands are written in `PIPELINE_NEXT.md` and also given in chat. Push the paper
  repository when `PIPELINE_NEXT.md` changes, since the owner copies from it.
- Results are committed after a run by staging only the compact files
  (config, metrics, predictions, manifests). One publication command per
  batch of runs is enough.
- Remove finished commands from `PIPELINE_NEXT.md` once their results are
  logged; Git history keeps them.
- Student training uses `--lm-loss target_fp32` with `logits_to_keep`. Teacher
  generation uses 4-bit, batch 8, `--exec-workers 4`. Set
  `CUDA_DEVICE_ORDER=PCI_BUS_ID` with `CUDA_VISIBLE_DEVICES`. Record new memory
  or speed measurements in `A5000_RUN_CONFIG.md`.
- Log runs and decisions in `LAB_LOG.md`, briefly.
- Explore freely: read any new result, add or drop arms after reading
  results, no pass/fail rules written in advance. Run a control when its
  result could change the method or a reviewer will certainly ask for it.
- Prefer small commits with conventional messages; move superseded documents
  to the archive instead of deleting them.
- Archive: everything superseded lives in `archive/` at the workspace root
  (`archive/paper/` from the outer repository, `archive/fedicl-sql/` from the
  nested one). It is local to the owner's Mac and ignored by Git; Git history
  still holds every file (`archive/README.md` names the last commits that
  tracked them). The server has no archive.

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
