# FedLS-SQL paper workspace: agent guide

The instruction file for every coding agent in this workspace (Codex, Claude
Code, and others); `CLAUDE.md` imports it. Durable rules and lessons go here,
and they are kept few and general on purpose.

The nested `fedicl-sql/` directory is a separate Git repository (code and
committed results, Python package `fedls_sql`) with its own
`fedicl-sql/AGENTS.md`. The GPU server holds only that repository, so the
code, GPU and server rules live there.

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
  might object. Before a proposal rests on "papers do this", name the paper
  and check it in the paper or its code; say so when it was not checked. A
  choice also has to be sound on its own: one that only lowers the
  baselines, or that the closest papers do not make, is not a way to a
  larger gain.
- The paper shows the method where its effect shows (owner, 2026-11-17).
  Among sound choices, the setup, model, prompt, comparisons and tables are
  picked for the gain over the baselines in the same setup, not for the
  highest level. A prompt or an inference step that lifts every row and
  shrinks the gain, or a comparison that does not make the paper better,
  stays in the notes and out of the paper. Each claim is worded so that it
  is true against everything the notes hold.
- The paper prints what serves it (owner, 2026-11-17): the setup as
  values, the results, the tables. How a seed, a setting, a round or a
  result was picked is not told in the paper and is not proposed for it;
  it stays in `LAB_LOG.md`, which keeps the true picture. The one limit:
  no sentence in the paper is false (a picked value is not called random,
  a number tuned on the test set is not called held-out).
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
- Method (owner, 2026-11-17, revised the same day): a federated learning
  method for Text-to-SQL that uses DPO with execution labels at the
  clients, built to beat the federated baselines (FedAvg SFT, and federated
  DPO as published: fixed pairs, fixed reference). It is the owner's own
  design, not CodeLutra applied to federated learning. CodeLutra (arXiv
  2411.05199) was found later to run a similar sample, label and DPO + NLL
  loop centrally; it is cited as the closest work, with what differs, and
  the settings taken from it are said to follow it. Candidate parts, each
  kept only on a measured gain: on-policy rounds, execution-aware pairs, a
  FedAvg SFT stage before the rounds. Pre-training at the server with the same loss on public data
  is a secondary part. The teacher is not part of the method; it is a
  research direction. The story is in `RESEARCH_STATE.md`, section 3, the
  papers behind it in `DPO_RESEARCH.md`.
- Default setup: Qwen2.5-Coder-1.5B-Instruct student, 5 Spider clients
  (`alpha_0.1/k5`), Qwen2.5-Coder-7B-Instruct teacher, BIRD train (or
  SynSQL-2.5M) as public data. Another model or setting may be proposed.
- Prompt, training recipe and decoding follow what widely used papers do,
  checked in the paper or its code (`LITERATURE.md`, section 1.19). One
  prompt serves training, sampling and evaluation, and the paper prints
  the prompt the model saw.
- Compute: RTX A5000 cards with 24 GB; a direction has to fit in memory and
  run time.
- Spider numbers are Spider test (2,147 rows). Rounds, steps and settings
  may be chosen on Spider test (owner, 2026-11-17). The notes record what
  was chosen on which set; the paper does not call such a number held-out.
- Novelty: a published mechanism adapted to this setting is acceptable.
  Cite the closest work and say what differs.

## Read first

1. `paper/notes/RESEARCH_STATE.md`: question, setup, method, what the
   results show, what is open.
2. `paper/notes/PIPELINE_NEXT.md`: what to run now and what is running.
3. `paper/notes/LAB_LOG.md`: runs, results and decisions, newest first.

Add another note only when the work needs it.

## Earlier work

The project was set up again from clean on 2026-11-17 (owner): the prompt
of every earlier adapter carried a sentence left from an ICL project, and
most rows were decoded with a repetition penalty nobody had set. Both
repositories as they were are at the tag `archive/pre-reset-2026-11-17`
and, on the owner's Mac, in `archive/reset_2026-11-17/` (ignored by Git,
not on the server; start at its `OVERVIEW.md`). Older material from the
restart of 2026-11-05 is in the same `archive/` folder.

- Everything measured before 2026-11-17 is reference only. It may be read
  to see what was tried; it is never quoted as a result, and a new claim is
  not built on it.
- Do not read or reason from material older than 2026-11-05 unless the
  owner asks.
- Processed data and teacher outputs on BIRD may be reused freely.
  Starting from an earlier adapter needs the owner's yes.
- The new code keeps no branch, field or default for the sake of an old
  result (no "historical bytes", no frozen identities).

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
  is compared against (prompt, decoding, length limit, training recipe),
  and print one rendered prompt and read it. Decoding uses no repetition
  penalty; no setting is inherited from a model's generation config.
- Run an experiment on the setup it stands for. A cut version is fine for a
  quick read; say what is cut and report the result as partial.
- A new line reuses the finished rounds it shares with an existing line
  and does not train them again (owner, 2026-11-18;
  `fedicl-sql/AGENTS.md`, Defaults).
- Log runs and decisions briefly in `LAB_LOG.md`. Commit small, with
  conventional messages.
- `paper/notes/overview.html` is the owner's project page. Update it only
  when the owner asks, from committed results; each update sets its
  `Cập nhật` stamp and adds a line to its update log at the bottom. Its
  results tab is drawn from a data block that
  `paper/notes/tools/overview_results.py` writes from the committed
  evaluations; a new evaluation needs one line in that script's `ARMS`,
  a new line or queued row an entry in the page's `LINES`, `START` or
  `PLAN`.

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
