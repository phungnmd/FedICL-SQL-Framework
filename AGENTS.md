# FedExec-SQL paper workspace: agent guide

The instruction file for every coding agent in this workspace (Codex,
Claude Code, and others); `CLAUDE.md` imports it. Rules are few and
general on purpose: a new rule replaces or merges with an old one, and
detail lives in the note it points to.

The nested `fedicl-sql/` directory is a separate Git repository (code and
committed results, Python package `fedls_sql`) with its own
`fedicl-sql/AGENTS.md`. The GPU server holds only that repository, so the
code, GPU and server rules live there.

## How to work

- The aim is a paper that reads well and can be accepted at the target
  journal: a method with a clear story and a visible effect.
- Rules, defaults and earlier decisions are working defaults, not walls
  (owner, 2026-11-24). A choice has to be not false, help the paper and
  look sound to a reviewer. When a decision stands in the way of a
  better paper, say so with the numbers and ask.
- The bar is what the target journal requires and publishes; no demand
  of our own goes on top. What published papers do is open to us once
  it is checked in the paper or its code (name the paper; say when it
  was not checked), and the choice has to be sound on its own: not one
  that only lowers the baselines.
- The paper shows the method where its effect shows (owner,
  2026-11-17): setup, model, prompt, comparisons and tables are picked
  for the gain over the baselines in the same setup, not for the highest
  level. It prints what serves it (the setup as values, the results, the
  tables); how a seed, a setting, a round or a result was picked stays
  in `LAB_LOG.md`.
- A part belongs to the method when it fits the story and shows an
  effect; nothing is added only to raise a number.
- An assessment of the paper is impartial (owner, 2026-11-27): a rule or
  a note of this project is never the reason a weakness is acceptable.
- Look for ideas from the task itself, and put a short run that settles
  a direction before long ones.

## The project

Paper: *FedExec-SQL* (name and title set by the owner, 2026-11-27; the
title is in `paper/manuscript/main.tex`; the code package keeps its
name, `fedls_sql`), a journal paper written for CMC alone (owner, 2026-11-27;
`paper/notes/JOURNAL_BAR.md`). JIIS is a later fallback; nothing is
built or checked for it now.

- Topic: federated Text-to-SQL. Organizations train one small language
  model together, and only that model is deployed.
- Method. Federated SFT learns from the gold SQL of each question and
  never uses the databases a client also holds. The method uses them:
  after warm-up rounds of FedAvg SFT, in each preference round a client
  samples queries from the round's global model, executes them on its
  own databases, labels them against the gold result, pairs correct with
  incorrect samples and trains with a DPO term plus an NLL term; the
  server averages the adapters. It is judged against the federated
  baselines (FedAvg SFT, and federated DPO as published: fixed pairs,
  fixed reference, no NLL term), and its novelty is stated against them.
  A part is kept on a measured gain. Pre-training at the server with the
  same loss is a secondary part; a teacher is a research direction, not
  part of the method. Story: `RESEARCH_STATE.md`, section 3. Claims:
  `paper/manuscript/CLAIMS.md`.
- Closest centralized work: CodeLutra (arXiv 2411.05199), cited. It is
  not the frame of the method (owner, 2026-11-27): no note, brief or
  section defines the method or its contributions as differences from
  it. Its places are fixed: `RESEARCH_STATE.md`, section 3.6, in the
  notes; in the paper, Section 2.2 with Table 1 (what it does and where
  ours differs, once), a citation at the objective, and one sentence in
  Section 4.5 on the settings that follow it.
- Default setup: Qwen2.5-Coder-1.5B-Instruct, 5 clients on BIRD train
  and 5 on Spider train (`alpha_0.1/k5` each). Another model or setting
  may be proposed.
- Datasets (owner, 2026-11-25): BIRD is the main dataset (the main rows,
  every baseline, the ablations, a second model); Spider carries the
  breadth rows (other models, federated setups, variant sets, test-suite
  accuracy). The rows the paper needs: `RESEARCH_STATE.md`, section 3.4.
- BIRD numbers are BIRD dev (1,534 rows; its test set is not public, and
  the k of the BIRD rows was set on Spider). Spider numbers are Spider
  test (2,147 rows); rounds, steps and settings may be chosen on it
  (owner, 2026-11-17). The notes record what was chosen on which set;
  the paper calls no number held-out.
- Prompt, training recipe and decoding follow widely used papers,
  checked in the paper or its code (`LITERATURE.md`, section 1.19). One
  prompt serves training, sampling and evaluation, and the paper prints
  it.
- Compute: RTX A5000 cards with 24 GB; a direction has to fit in memory
  and run time.

## Read first

1. `paper/notes/RESEARCH_STATE.md`: question, setup, method, what the
   results show, what is open.
2. `paper/notes/PIPELINE_NEXT.md`: what to run now and what is running.
3. `paper/notes/LAB_LOG.md`: runs, results and decisions, newest first.
4. For work on the manuscript: `paper/notes/WRITING_PLAN.md`.

Add another note only when the work needs it.

## Earlier work

The project was set up again from clean on 2026-11-17 (owner): the
prompt of every earlier adapter carried a sentence left from another
project, and most rows were decoded with a repetition penalty nobody had
set. Both repositories as they were are at the tag
`archive/pre-reset-2026-11-17` and in the local `archive/` folder
(ignored by Git, not on the server).

- Everything measured before 2026-11-17 is reference only: never quoted
  as a result, and no claim is built on it. Material older than
  2026-11-05 is not read unless the owner asks.
- Processed data and teacher outputs on BIRD may be reused. Starting
  from an earlier adapter needs the owner's yes.
- The code keeps no branch, field or default for the sake of an old
  result.

## Hard rules

Few, and each prevents a real failure.

- Honesty: we always know the true picture. Every number traces to a
  committed result (config, seed, predictions, Git SHA) and names its
  set, the notes record what each control really showed, and no number
  is invented or changed. Each claim is true against everything the
  notes hold. The closest work is cited. Privacy here is data isolation,
  not differential privacy.
- Data roles: client data never leaves a client; a teacher runs only at
  the server on public data; test data never becomes training, retrieval
  or teacher data.
- Server and GPU: follow `fedicl-sql/AGENTS.md`. In short: drive D only;
  nothing under `artifacts/` is deleted, moved or overwritten; peak VRAM
  stays under about 21.5 GiB; server commands are PowerShell on one
  line; result commits are never rebased there.
- Git: two separate histories (paper here, code and results in
  `fedicl-sql/`); work on `main` in the owner's checkouts; commit
  messages never mention AI tools; never change the author settings;
  never commit adapters, weights, caches or `artifacts/`.

## Defaults

Use these unless another way is simpler; say so in one line when you
deviate.

- GPU work goes into `fedicl-sql/queues/active.toml` and is drained by
  `scripts/gpu_worker.py`. The commands the owner runs are written in
  `PIPELINE_NEXT.md` and given in chat; push when that file changes.
- Before queuing a new line, compare its resolved commands with the line
  it is compared against (prompt, decoding, length limit, training
  recipe), and print one rendered prompt, decoded from its token ids,
  and read it. Decoding uses no repetition penalty; no setting is
  inherited from a model's generation config.
- Run an experiment on the setup it stands for. A cut version is fine
  for a quick read; say what is cut and report the result as partial.
- A new line reuses the finished rounds it shares with an existing line
  and does not train them again (owner, 2026-11-18).
- Log runs and decisions briefly in `LAB_LOG.md`. Commit small, with
  conventional messages.
- Subagents run on Opus; the larger model is for the main session
  (owner, 2026-11-22: cost). One exception: the writer of the
  manuscript, an isolated session, runs on Fable 5.2 at high effort
  (owner, 2026-11-26).
- Diagrams follow `paper/figures/STYLE.md`: start from `template.svg`,
  render with `render.py`, open and check the PNG before committing.
- `paper/notes/overview.html` is the owner's project page. It is updated
  only when the owner asks, from committed results, through
  `paper/notes/tools/overview_results.py`; each update sets its
  `Cập nhật` stamp and adds a line to its update log.

## Writing

- Notes, reports and replies: the owner works alone and is learning ML.
  Plain words, short documents, progress told by runnable step and
  result. Replies in Vietnamese keep common technical terms in English.
  No emojis, no em dashes.
- The manuscript (`paper/manuscript/`; workflow in
  `paper/notes/WRITING_PLAN.md`) has an academic voice (owner,
  2026-11-27): dense, in the terms of the field, assertive at the
  strength of the evidence. The plain-words rule above is not for it.
  The main session coordinates and writes no sentence of the paper.
  The writer of a section runs in an isolated session (the
  `cold-session` skill), never as a subagent: a subagent inherits this
  file and the memory, and writes about them (owner, 2026-11-27). It is
  given a pack and nothing else; web search is on for the sections on
  other work (1, 2 and 6), and what it takes from the web it lists with
  the URL. The pack holds the work in full as
  science: the paper on one page, the brief of the section, every
  result table with its tests, the fact rows and abstracts of the papers
  the section cites, and one or two published papers far from ours as
  examples of form. It holds nothing of the lab: no note, rule, date,
  decision, claim number or lab word, and not the full text of
  CodeLutra or OpenFedLLM. The writer decides the structure of its
  section. The main session is the person of the project and the writer
  its tool for writing (owner, 2026-11-27): the writer asks it whatever
  the pack does not settle, at any point, and it answers from the
  record, with the science and nothing of the lab. What binds the text: the hard rules, the claims of
  `CLAIMS.md` at their strength and scope (not above, not below),
  numbers as generated macros, the limits of the journal; these are
  checked on the draft by the main session and reach the writer as
  editor's notes. Checks of words and style are signals for the main
  session, never rules for the writer; a draft far from a good paper is
  written again from a corrected pack, not patched.
- The draft does not wait for the results (owner, 2026-11-27). A number
  without a committed row prints `??` (`--` in a generated table), or
  stands as a marked guess, `\expect{value}`. A guess is never quoted as
  a result anywhere, and `make submit` stops on either.
- The paper, its figures and anything sent out say "the model", not
  "the student" (owner, 2026-11-25); the notes and the code keep
  "student".
- Credit (owner, 2026-11-27): the method is presented as ours. The paper
  never says that it takes its parts from another paper or brings
  another paper's loop into this setting; the closest work is credited
  at its fixed places (The project). A debt or a weakness is stated at
  the size the evidence gives it, and once.
- `PIPELINE_NEXT.md` answers on its first screen what to run now and
  what is running: `Status`, `Run now` (numbered steps, one full command
  each, what to send back), `Running and queued`, `Reference`. No
  history in it; estimates are marked as estimates.
- Reports for the advisor: tables carry the numbers and the text says
  what they mean in plain words; the best value of each column is
  highlighted; lab-process detail stays out.
