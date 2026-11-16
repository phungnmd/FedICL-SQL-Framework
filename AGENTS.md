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

## Read this first: aim for a good paper, do not be stricter than asked

Owner, 2026-11-17. Before this date agents argued parts out of the method
and options off the table on grounds nobody had asked for, and it cost the
owner many days. These rules come before the defaults and before an agent's
own caution. Only the hard rules (honesty, data roles, GPU, server) rank
above them.

1. The aim is a paper that reads well and is accepted at the target
   journals: a method with a clear story and a visible effect. It is not the
   strictest possible experiment design.
2. Being strict is the reviewer's work. Do not weaken, shrink or drop a part
   of the method, and do not advise against an option, on an argument a
   reviewer might make: "a control explains part of the gain", "this is
   already published", "the baseline could be stronger", "it only adds one
   point". Report what a control shows, keep the part when its effect is
   real, and give a reviewer's judgement only when the owner asks for one.
3. What accepted papers do is open to us: the student model (another one in
   place of or beside Qwen2.5-Coder-1.5B), the baselines shown, the training
   sets, voting or more than one call at inference, the benchmarks reported,
   the comparison a gain is stated against. When an option matches published
   practice, present it as available: name the paper that does the same and
   what it costs here, and let the owner decide.
4. A published mechanism adapted to this setting is enough novelty. Do not
   make "a mechanism of our own" a condition for the method, and do not keep
   searching for one while the method stands.
5. Read a result the way papers present theirs: against the base model and
   the federated baselines, on every benchmark we evaluate. The hardest
   control and the weakest single number belong in the ablation, not in the
   verdict on the method.
6. No pile of parts either: a part belongs to the method only with a place
   in the story and a shown effect in the final setup. Nothing is added only
   because it raises a number.
7. A search for ideas or literature starts from the task, not from the
   pipeline we have. Cover method families we have not tried, and include a
   pass by an agent that gets only the generic problem and does not read the
   project. Earlier rounds looked only at neighbours of the current line.
8. A reviewer's judgement, when the owner asks for one, is calibrated to the
   target journals: read what they published recently (kind of contribution,
   number of datasets, baselines and seeds, size of the gain) and judge
   against that, not against top machine-learning conferences.
9. A short run that decides the direction goes ahead of long runs. Do not
   leave the owner waiting on a long line for a question an hour answers.
10. An earlier decision is an input, not a wall. When a rule, a decision or
    an agent's reading of it blocks something that would make the paper
    better, say so with the numbers and ask; the owner changes decisions.

What this cost before the rule, as examples of what not to repeat:

- The server stage and the teacher were taken out of the method on
  2026-11-16 because the teacher's own part was about one point; they came
  back on 2026-11-17.
- "A mechanism of its own" was required on top of a recipe that a published
  paper presents alone; five candidates, a debate and several runs followed.
- Gains were read on Spider test against the hardest control only (+0.9),
  while the method stood +5.3 over FedAvg on two seeds and +5 to +12 on the
  other sets.
- One student model and one greedy call were treated as limits; published
  papers use several models and voting.

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

Paper: *FedLS-SQL* (working title), aimed at a Q3 journal or above. Question,
fixed setup and open choices: `paper/notes/RESEARCH_STATE.md`.

- Target (owner, 2026-11-11): one paper at Q3 or above with a good method.
  The target is a direction, not a bar to hit rigidly. Do not close a
  question with "this already passes Q3", and do not drop an idea only
  because it leaves one number (for example Spider test EX) unchanged. Judge
  a change by whether it makes the method better: a clearer mechanism, each
  part with a shown role, stronger or broader results.

- Fixed (owner): the topic (federated Text-to-SQL, an SLM trained by clients
  and deployed alone) and the setup (Qwen2.5-Coder-1.5B-Instruct student,
  5 Spider clients on the `alpha_0.1/k5` split; this is the default setup,
  and another student model or setting may be proposed under rule 3 of
  "Read this first"). Available at the server: a frozen Qwen2.5-Coder-7B-Instruct teacher and BIRD train with
  evidence as public data; SynSQL-2.5M may replace or join it at the server
  (owner, 2026-11-07).
- If the teacher is used, it runs only at the server, on public data. Clients
  never send data.
- Compute is the two RTX A5000 cards. A direction must fit that budget in
  memory and run time.
- Goal (owner, 2026-11-06): a method that clearly beats the federated
  baselines on the clients' domain. The teacher is an option, not a
  requirement; a method without it is acceptable if it is strong enough.
- Open: the metrics, the title, and parts that may still join the method.
  Propose them from the task itself.
- Spider metric (owner, 2026-11-07): every Spider number from now on is
  Spider test (2,147 rows); Spider dev is skipped or reported only as a
  secondary diagnostic. Choices are made on Spider test, so it is never
  called held-out (honesty rule below).
- Method (owner, 2026-11-17): fixed as three stages, with the story in
  `RESEARCH_STATE.md`, section 3: the server stage on public data with the
  teacher, FedAvg SFT at the clients, federated DPO with execution labels
  at the clients. The decision of 2026-11-16 that took the server stage and
  the teacher out of the method is withdrawn. A part belongs to the method
  only when it has a place in the story and a shown effect in the final
  setup; a part without one is an analysis row or is dropped, and nothing
  is added only because it raises a number. Further parts (synthetic rows
  checked at the clients) join under the same condition. How to judge and
  defend it: "Read this first" at the top.
- Novelty for Q3: a published mechanism adapted to federated Text-to-SQL with
  a task-specific adaptation is acceptable. Cite the closest work and state
  what differs; never claim "first" and never hide the closest prior work.
- Judging the Q3 bar: only when asked. When asked whether a result, the
  method or the story is strong enough, judge as an impartial reviewer at
  the target venues (`RESEARCH_STATE.md`: CMC, JIIS) would, calibrated to
  what those journals published recently in federated learning, LLM-to-SLM
  distillation and Text-to-SQL, not to top conferences. Say with the
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
- Server: it holds only `fedicl-sql/`. Pulling, editing and committing there
  while jobs run is allowed. When an agent changes code that a running job or
  a queued task of an unfinished experiment may still load, it says so when
  it pushes, in chat and in `PIPELINE_NEXT.md`, and names what to let finish
  first. The server checkout has
  `core.autocrlf=true`: never rebase a result commit there (it rewrites files
  as CRLF and breaks recorded hashes); fetch and fast-forward instead.
- Server commands are PowerShell and each command is one physical line,
  because the owner copy-pastes them over a remote session. A command runs
  from the `fedicl-sql/` root, defines every variable it uses and throws after
  any non-zero exit.
- Server storage: never delete, overwrite, move or rename anything under
  `artifacts/` on the server unless the owner asks with an explicit path list;
  new outputs get their own root.
- Server disks (owner, 2026-11-15): drive D only, never drive C. Temp
  files default to `D:\phungthan\fediclkd\tmp` (on Windows, importing
  `fedicl_sql` sets `TEMP`, `TMP`, `TMPDIR`; `fedicl-sql/AGENTS.md`); server
  commands also set `TEMP` and `TMP` there and run pytest with
  `--basetemp` there.
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

- GPU work goes into the queue file `fedicl-sql/queues/active.toml` (tasks,
  dependencies, priority order, `<phase>/<name>` ids), drained by one worker
  per GPU (`scripts/gpu_worker.py`, full queue or `--phase`); one task per
  experiment step. Server commands are written in `PIPELINE_NEXT.md`
  and also given in chat. Push the paper repository when `PIPELINE_NEXT.md`
  changes, since the owner copies from it.
- Results are committed after a run by staging only the compact files
  (config, metrics, predictions, manifests): a `scripts/publish_results.py`
  task in the queue, after the tasks that write its paths.
- Remove finished commands from `PIPELINE_NEXT.md` once their results are
  logged; Git history keeps them.
- Decoding (owner, 2026-11-16): new lines decode without the repetition
  penalty (`--repetition-penalty 1.0` in evaluation and sampling). Rows
  before that date used the model's generation config, 1.1; rows without the
  penalty carry `_np` in their arm name (`fedicl-sql/AGENTS.md`).
- Student training uses `--lm-loss target_fp32` with `logits_to_keep`. Teacher
  generation uses 4-bit, batch 8, `--exec-workers 4`. Set
  `CUDA_DEVICE_ORDER=PCI_BUS_ID` with `CUDA_VISIBLE_DEVICES`. Record new memory
  or speed measurements in `A5000_RUN_CONFIG.md`.
- Check a new experiment line against its sources before it is queued
  (owner, 2026-11-17; the 1.1 repetition penalty and the first `codes`
  prompt each went unnoticed for days): the paper's method section itself
  when it follows a paper, with the differences written down; the resolved
  commands against the line it is compared with (prompt style, decoding,
  length limit, LoRA recipe); and a check in code where a step reads what
  an earlier step wrote. Full rule: `fedicl-sql/AGENTS.md`, "Defaults".
- Run an experiment on the setup it stands for: all of each client's data,
  every evaluation row, the planned rounds and epochs. A part (a subset of
  questions or rows, fewer rounds) is fine when the full run does not fit the
  GPU budget or a quick check is the point (smoke, memory probe). Then say so
  when queuing it, in chat and in `PIPELINE_NEXT.md`: what is cut, why, what
  the full version would cost, and whether the result still answers the
  question. A partial result is reported as partial.
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

## Writing `PIPELINE_NEXT.md`

The owner opens this file to learn two things: what to run now, and what is
running (owner, 2026-11-10). Both are answered on the first screen. The file
has four sections, in this order:

1. `## Status`: the time of the update, then one row per GPU: the running
   task, idle, waiting for the owner, or not ours. Say what the state is
   known from (the owner's message, a results commit) and since when; an
   agent never presents a guess as the live state. The read-only status
   commands sit right under the table.
2. `## Run now`: numbered steps in the order to run them. Each step is one
   line of purpose, one full command, and what to send back, if anything.
   When there is nothing to run, the section says so and names the next
   moment the owner is needed: after which task, about when, what to read
   and what to do with it.
3. `## Running and queued`: one table in queue order with the task ids of
   the queue file, the question each answers, the time estimate and the
   state (running, queued). Under it only: what is cut from a full run and
   what is not queued yet and why.
4. `## Reference`: commands that stay valid (restart, pull and test, the
   other GPU) and the description of the lines. Nothing in it is needed to
   act.

- Every command the owner needs now is written in full in "Run now"; the
  owner never scrolls to another section to act.
- No history: why something was restarted, what failed, a decision and its
  reasons, results. Those go to `LAB_LOG.md`; this file gives the current
  state only.
- A finished step or task leaves the file once it is logged; a diagnostic
  the owner chose to skip leaves at once.
- Update `Status` and the table in the same commit as a queue change, and
  whenever the owner reports a start, stop or failure, or a results commit
  shows a task finished.
- Estimates are marked as estimates ("about"); a clock time is given with
  its date.

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
