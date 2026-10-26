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

Paper: *FedLS-SQL* (working title; subtitle open), aimed at a Q3 journal.

Clients hold private Text-to-SQL data (Spider, domain-cluster split) and train
a small SLM with LoRA and sample-weighted factor-wise FedAvg. The server holds
a frozen Qwen2.5-Coder-7B teacher and a public pool from another domain
(BIRD with evidence). Only adapters move; only the SLM is deployed. Since
P2.27 the student is Qwen2.5-Coder-1.5B-Instruct and the clients follow the k5
alpha 0.1 split (earlier: Qwen2.5-1.5B-Instruct and Coder-0.5B, alpha 0.5).
Protocol v2 uses explicit dataset profiles. Canonical runs use no ICL.

- No method or paper story is fixed. Exploration (seed 0, dev sets) is open;
  the story and success criterion are fixed in a dated LAB_LOG entry before
  seeds 1-2 or Spider test (evidence rules below).
- Primary metric (owner, 2026-10-16), fixed for every phase: Spider EX, the
  clients' private domain (Spider dev in exploration, Spider test at
  confirmation). BIRD EX (public domain) is secondary: rank options by Spider
  first; a BIRD gain counts only when Spider EX is not lower, and between
  options whose Spider EX does not differ the higher BIRD wins. Never trade
  Spider for BIRD. Every arm still reports both; Spider-Realistic/SYN/DK
  measure robustness; EM is a diagnostic. In the reverse-roles setting
  (P2.43: BIRD at the clients, Spider at the server) the primary metric is
  BIRD EX, the private domain, with Spider secondary under the same rule
  (owner, 2026-10-17).
- Spider test (2,147 rows) is only for confirmation (R10). Spider dev, its
  variants and BIRD dev are development sets.
- Ground every method component in a published paper and name it. Flag any
  component that has no source instead of inventing one silently.
- Compute is the two RTX A5000 cards. A direction must fit that budget in
  memory and run time; a 14B or 32B teacher does not (owner, 2026-10-12).
  Within the budget, model, method and schedule choices stay open.
- The teacher runs only at the server, on public data; running it at the
  clients is ruled out (owner, 2026-10-12).
- The paper's goal is a federated framework in which the server LLM teacher
  contributes measurably, for a Q3 journal. A story that reduces the teacher
  to an ablation (for example "public data at the server closes the FL
  penalty, the teacher adds nothing") does not meet that goal and is not
  strong enough for Q3 on its own. Do not offer it as the default fallback;
  look for directions that keep a real teacher contribution within the fixed
  constraints, and say plainly if none is supported.
- Novelty bar for Q3 (owner, 2026-10-12): applying a published mechanism to
  federated Text-to-SQL with a task-specific adaptation (execution checks,
  schema handling, the private/public split, the FL schedule) is enough
  novelty for this venue. Do not drop or down-rank a direction because a
  similar mechanism exists in another task or domain (for example FedCoT,
  FDKT, GKD, STaR). Cite the closest work, state what differs, and judge the
  direction on whether its evidence can hold. Only the wording stays limited:
  no "first" claims and no hiding the closest prior work
  (`paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`).
- Floor and aim (owner, 2026-10-14). Q3 is an applied venue. The floor is a
  standard Q3 applied paper: the federated framework works end to end; each
  component is a published mechanism with a task-specific adaptation; the
  teacher contribution is measured against the matched gold bootstrap at the
  final endpoint and confirmed over the three seeds; components may simply add
  up (no synergy required); controls and dev exploration are reported. The
  aim is above Q3 when a direction within the constraints can reach it, for
  example a mechanism whose gain depends on the federated structure (a client
  method that enlarges the teacher contribution) or a confirmed account of
  where the teacher's knowledge goes during FL. Pursue the aim only with
  evidence. Never drop, down-rank or delay a direction that reaches the floor
  because it misses the aim, and judge any fallback against the floor. A
  story below the floor (teacher as an ablation) stays ruled out.

## Read first

1. `paper/notes/RESEARCH_STATE.md`: question, findings with their strength,
   open questions, current phase, rules in force.
2. `paper/notes/PIPELINE_NEXT.md`: the only active executable queue.
3. `paper/notes/LAB_LOG.md`: evidence ledger and decisions (from 2026-10-10;
   older entries are archived).
4. `paper/notes/system_architecture.md`: setup, data rules, claim limits.
5. `paper/notes/RESULT_REGISTRY.md`: canonical labels and checkpoints.
6. `CONVENTION.MD`: repository layout, command contract (section 6.1), result
   retention, statistics, Git discipline.

Archived material (earlier directions and plans, FedICL, ICL, FLoRA-NA, early
PoC, superseded runbooks) lives under `paper/archive/`. Never use it as the
current plan.

## Current state (2026-10-26)

- Exploration under the simplified rules (LAB_LOG 2026-10-12). Open
  questions: `RESEARCH_STATE.md` section 4. Direction proposal (not fixed):
  `paper/notes/DIRECTION_PROPOSAL.md`.
- Owner decision 2026-10-13: K2AAA alone is too simple to be the
  contribution; it is the strongest simple baseline a method must beat.
- Published at seed 0: P2.27 (base, FL, FedNTD, gold v1, Hinton v1,
  `central`), P2.28, P2.29 (`h_plain`), P2.36 (`g_plain`), P2.37
  `hinton_k2aaa`, `gold_k2aaa`, `central_mix`, `local`; P2.38, the P2.39
  pilot, P2.40, P2.42. P2.41 not run (its condition failed). Deferred: the
  P2.37 `akaka_plain` pair.
- Next direction (owner, 2026-10-17): reverse roles, BIRD private and Spider
  public. P2.43 is built; its Hinton K2 and A1 are published and both chains
  run to A3.
- 2026-10-23 (LAB_LOG): plan judged by acceptance at a Q3 journal; P2.45
  not run; P2.44 self-teacher control built and queued; no seed 1-2 or
  Spider test run until every seed 0 control is in and a freeze entry fixes
  the method.
- 2026-10-25: P2.47 client replay published (`mixkd_k2aaa` A3 Spider
  73.98, BIRD 45.24). P2.48 published (nested `8b79530`): top-50 plus tail
  replay targets match the full ones (`mixkd50_k2aaa` A3 Spider 74.08, BIRD
  44.78, the current candidate); FSL-style server steps keep Spider but each
  private round gives back most of their BIRD gain (LAB_LOG 2026-10-25).
- 2026-10-26: freeze approved (LAB_LOG FREEZE): method `mixkd50_k2aaa`;
  comparators `gmixgold_k2aaa`, `hinton_k2aaa`, `k2plus_aaa`,
  FedCoLLM-style; Spider test primary, three seeds. P2.53 runs it.
- Retired 2026-10-12: per-experiment pass/fail rules (R1-R6, R11, R12) and
  the fixed phase E arm list. In force: R10, R13, R8 (confirmation) and R9
  (reporting). Outcomes recorded under retired rules stand as history.
- Earlier 0.5B and 1.5B-Instruct adapters are references, never parents of
  new runs. P2.16 centralized E1-E4 were never published; do not cite them.
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
  forward KL (`T=2` by default), the virtual-teacher control of Yuan et al.
  (CVPR 2020) in place of the teacher, TAID (Shing et al., ICLR 2025) as the
  KD target, and an auxiliary plan task next to SQL CE. Client option: frozen
  LoRA A (FFA-LoRA, Sun et al., ICLR 2024; dropped after the P2.39 pilot).

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
  as CRLF and breaks the byte hashes in receipts and manifests (P2.36
  lesson). Never renormalize line endings on the server during a phase.
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
- Three rules govern selection (owner, 2026-10-12):
  1. Exploration is open. On seed 0 and the dev sets, any result may be read
     and used to choose the next arm, setting, schedule or direction; arms may
     be added after reading results; no pass/fail rule is written before an
     exploratory run. Log every run and every choice in LAB_LOG.
  2. Freeze, then confirm. Before any seed 1-2 run or Spider test
     evaluation, a dated LAB_LOG entry fixes the method, configuration,
     comparators, test and claims. Paper claims come only from these
     confirmation runs, never from the dev numbers that chose them. Nothing
     in that entry changes after a confirmation result is read.
  3. Disclose briefly (narrowed by the owner, 2026-10-26). The paper calls
     dev numbers exploratory and states how many variants and checkpoints
     were evaluated on dev; it does not report exploratory arms one by one.
  What rule 2 protects: with about 140 discordant questions per Spider dev
  contrast, the best of ten variants with no true effect still shows about
  +1.7 points, and roughly 40% of such searches yield one p<.05.
- Lean exploration, strongest story (owner, 2026-10-26):
  - Run a control during exploration only when its result could change the
    method or it is a baseline reviewers will certainly ask for. Skip
    controls whose outcome would not change what we do next. Do not write
    readings or criteria before exploratory runs; log what ran and what was
    chosen, and read the results freely.
  - The paper carries the strongest supported story. Choose the claims from
    what the evidence supports best; the main text and appendix hold only
    results that serve those claims. A weak or neutral result (for example a
    small margin over a baseline) stays out of the paper, as long as the
    paper makes no claim that this result tests. Drop the claim rather than
    hide the result that tests it.
  - Hard limits that stay: no claim that an omitted result contradicts; the
    comparators and claims fixed in the freeze entry are reported with every
    confirmation result, favourable or not; every number in the paper keeps
    its evidence trail.
- Screens are seed 0 with paired questions and exact McNemar tests. One Spider
  question is about 0.1 point; small differences need more seeds before any
  claim. Paper claims use the three-seed confirmation with the
  question-clustered test (R13).
- pass@k on training questions is a ceiling with a gold oracle, not a
  forecast of dev EX (P2.28 lesson).
- Compare central and FL at matched data passes, not only at the final
  checkpoint; a central run past its peak hides the FL penalty (rule R9).
- A subgroup found post hoc on one seed is a hypothesis; confirm it only on
  seeds that did not generate it (rule R8).
- Pool seeds with a question-clustered test (per-question mean over seeds,
  test across questions). Summing discordant pairs over seeds treats
  correlated question-seed pairs as independent and gives p values that are
  too small (rule R13). Fix the number of seeds from a power check before any
  confirmation result; never add seeds because p missed .05.
- Fix the paper wording for each possible outcome before the confirmation
  results are read, and claim only what a comparator isolates. A component
  kept from an earlier version without evidence in the current setting is
  labeled inherited and is not claimed.
- Keep a record of how the method was selected (rule dates, data seen,
  number of checkpoints evaluated on dev); the paper reports it (R13).
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
