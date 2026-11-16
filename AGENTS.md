# FedLS-SQL paper workspace: agent guide

The instruction file for every coding agent in this workspace (Codex, Claude
Code, and others); `CLAUDE.md` imports it. Durable rules and lessons go here,
and they are kept few and general on purpose.

The nested `fedicl-sql/` directory is a separate Git repository (code and
committed results) with its own `fedicl-sql/AGENTS.md`. The GPU server holds
only that repository, so the code, GPU and server rules live there.

## How to work

- The aim is a paper that reads well and can be accepted at the target
  journals: a method with a clear story and a visible effect.
- Use your judgement as a researcher on this project would. Where this file
  says nothing, do what makes the paper better and say what you did.
- The bar is what the target journals require. Read what they publish and
  accept (kind of contribution, baselines, datasets, seeds, size of the
  gain) and work to that; do not put demands of our own on top of it. What
  published papers do (models, baselines, data, voting, benchmarks) is open
  to us, and a part of the method is not argued away because some reviewer
  might object.
- A part belongs to the method when it fits the story and shows an effect;
  nothing is added only to raise a number.
- Earlier decisions and notes are inputs, not walls. When one stands in the
  way of a better paper, say so with the numbers and ask.
- Look for ideas from the task itself, not only around what is already
  built, and put a short run that settles a direction before long ones.

## The project

Paper: *FedLS-SQL* (working title), a journal paper at Q3 or above
(candidates: CMC, JIIS). The current state is in
`paper/notes/RESEARCH_STATE.md`.

- Topic: federated Text-to-SQL. Clients train a small model together and
  only that model is deployed.
- Method (owner, 2026-11-17), three stages: a server stage where the frozen
  teacher teaches the student on public data, FedAvg SFT at the clients,
  and federated DPO with execution labels at the clients. The story is in
  `RESEARCH_STATE.md`, section 3.
- Default setup: Qwen2.5-Coder-1.5B-Instruct student, 5 Spider clients
  (`alpha_0.1/k5`), Qwen2.5-Coder-7B-Instruct teacher, BIRD train (or
  SynSQL-2.5M) as public data. Another model or setting may be proposed.
- Compute: RTX A5000 cards with 24 GB; a direction has to fit in memory and
  run time.
- Spider numbers are Spider test (2,147 rows).
- Novelty: a published mechanism adapted to this setting is acceptable.
  Cite the closest work and say what differs.

## Read first

1. `paper/notes/RESEARCH_STATE.md`: question, setup, method, what the
   results show, what is open.
2. `paper/notes/PIPELINE_NEXT.md`: what to run now and what is running.
3. `paper/notes/LAB_LOG.md`: runs, results and decisions, newest first.

Add another note only when the work needs it.

## Earlier work

The project restarted on 2026-11-05. Everything superseded lives in
`archive/` at the workspace root (local to the owner's Mac, ignored by Git,
not on the server).

- Do not read or reason from the archive or from results before that date
  unless the owner asks.
- Teacher outputs on BIRD and processed data may be reused freely. Starting
  from an earlier adapter, or using an earlier result as a comparator, needs
  the owner's yes.

## Hard rules

Few, and each prevents a real failure.

- Honesty: we always know the true picture. Every number traces to a
  committed result (config, seed, predictions, Git SHA) and names its set,
  the notes record what each control really showed, and no number is
  invented or changed. How the paper presents its results follows what the
  target journals expect. Cite the closest work. Privacy here is data
  isolation, not differential privacy.
- Data roles: client data never leaves a client; the teacher runs only at
  the server on public data; test data never becomes training, retrieval or
  teacher data.
- Server and GPU: follow `fedicl-sql/AGENTS.md`. In short: drive D only;
  nothing under `artifacts/` is deleted, moved or overwritten; peak VRAM
  stays under about 21.5 GiB; server commands are PowerShell on one line;
  result commits are never rebased there.
- Git: two separate histories (paper here, code and results in
  `fedicl-sql/`); work on `main` in the owner's checkouts; commit messages
  never mention AI tools; never change the author settings; never commit
  adapters, weights, caches or `artifacts/`.

## Defaults

Use these unless another way is simpler; say so in one line when you
deviate.

- GPU work goes into `fedicl-sql/queues/active.toml` and is drained by
  `scripts/gpu_worker.py`. The commands the owner runs are written in
  `PIPELINE_NEXT.md` and given in chat; push when that file changes.
- Before queuing a new line, compare its resolved commands with the line it
  is compared against (prompt, decoding, length limit, training recipe).
  New lines decode without the repetition penalty.
- Run an experiment on the setup it stands for. A cut version is fine for a
  quick read; say what is cut and report the result as partial.
- Log runs and decisions briefly in `LAB_LOG.md`. Commit small, with
  conventional messages.

## Writing

- The owner works alone and is learning ML: plain words, short documents,
  progress told by runnable step and result. Replies in Vietnamese keep
  common technical terms in English. No emojis, no em dashes.
- `PIPELINE_NEXT.md` answers two questions on its first screen: what to run
  now and what is running. Four sections in this order: `Status` (what each
  GPU does and how that is known), `Run now` (numbered steps, each with one
  full command and what to send back), `Running and queued` (one table in
  queue order), `Reference`. No history in it; finished steps leave once
  they are logged; estimates are marked as estimates.
- Reports for the advisor: tables carry the numbers and the text says what
  they mean in plain words; the best value of each column is highlighted;
  lab-process detail stays out.
