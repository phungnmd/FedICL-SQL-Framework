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
(BIRD with evidence). Clients send only LoRA adapters; the server sends the
aggregated adapter and, for the frozen method, once a public subset with
compressed teacher targets for client replay; only the SLM is deployed. Since
P2.27 the student is Qwen2.5-Coder-1.5B-Instruct and the clients follow the k5
alpha 0.1 split (earlier: Qwen2.5-1.5B-Instruct and Coder-0.5B, alpha 0.5).
Protocol v2 uses explicit dataset profiles. Canonical runs use no ICL.

- Method and claims are fixed in LAB_LOG (FREEZE 2026-10-26 and its two
  2026-10-28 addenda); the paper direction is
  `paper/notes/DIRECTION_PROPOSAL.md` (owner, 2026-10-28).
- Metrics (owner, 2026-10-16; loosened 2026-10-29): Spider EX, the
  clients' private domain, is the default primary metric and BIRD EX (public
  domain) the secondary one; every arm reports both, with
  Spider-Realistic/SYN/DK for robustness and EM as a diagnostic. Which
  metric carries the story is chosen for the strongest paper (owner
  decides). Spider test (2,147 rows) is the final test set; Spider dev, its
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

## Current state (2026-10-28)

- Confirmation phase (P2.53, three seeds, Spider test). Paper direction
  (owner, 2026-10-28, after an outside review): the server teacher's
  public-domain gain is lost in the FedAvg rounds and client replay of
  compressed teacher targets keeps it, Spider non-inferior; teacher on
  Spider tested by C6. `paper/notes/DIRECTION_PROPOSAL.md`. Open questions:
  `RESEARCH_STATE.md` section 4.
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
  not run; P2.44 self-teacher control built and queued.
- 2026-10-25: P2.47 client replay published (`mixkd_k2aaa` A3 Spider
  73.98, BIRD 45.24). P2.48 published (nested `8b79530`): top-50 plus tail
  replay targets match the full ones (`mixkd50_k2aaa` A3 Spider 74.08, BIRD
  44.78, the current candidate); FSL-style server steps keep Spider but each
  private round gives back most of their BIRD gain (LAB_LOG 2026-10-25).
- 2026-10-26: freeze approved (LAB_LOG FREEZE): method `mixkd50_k2aaa`;
  comparators `gmixgold_k2aaa`, `hinton_k2aaa`, `k2plus_aaa`,
  FedCoLLM-style; Spider test primary, three seeds. P2.53 runs it.
  2026-10-27: E3 (reverse roles) left the confirmation (P2.52: BIRD -1.69
  vs `hinton_k2aaa_rev`, p=.061); exploratory only.
- 2026-10-27: second setting is SynSQL-2.5M as the public pool (P2.54,
  3,336 rows without external knowledge, BIRD-size token budget), not a
  limitation story (owner). 2026-10-28: it is the robustness setting of
  the paper (does the method still work with another public pool), seed 0;
  published (nested `76496b4`): method minus FedAvg Spider dev +3.09
  (p=.002), BIRD +4.11 (p<.001), Spider test 72.99 vs 71.50 (p=.028).
  2026-10-29: `gmixgold_k2aaa` Spider test 72.05, method +0.93 (p=.098;
  nested `5a638c0`).
- 2026-10-28: seed-0 Spider test: method 73.17, `gmixgold_k2aaa` 72.61,
  `hinton_k2aaa` 73.50, `k2plus_aaa` 73.87 (LAB_LOG). FREEZE addendum 2:
  FedAvg and `gold_k2aaa` join seeds 1-2, claims C6 (`hinton_k2aaa` >
  `gold_k2aaa`) and C7 (method > FedAvg) on Spider test. E1 and
  replay-ratio sensitivity wait for a revision. 2026-10-29: E2 (0.5B
  student, three seeds) queued again after P2.53 (owner).
- Retired: per-experiment pass/fail rules (R1-R6, R11, R12) and the fixed
  phase E arm list (2026-10-12); R8, R10 and the seed-count part of R13
  (owner, 2026-10-29: rules that bind the paper's direction go). Outcomes
  recorded under retired rules stand as history.
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

Goal (owner, 2026-10-29): the strongest, most interesting Q3 paper the
results support. Only three rules are fixed, all about honesty:

- Every number in the paper has a checkpoint, config, dataset, seed,
  prediction file and Git SHA trail. A result reported only in chat is
  logged as "not committed" and stays out of the paper until it is
  committed.
- The paper never misstates how a number was obtained: every number names
  its set (dev or test), and a Spider test number is not called held-out
  once a choice (setting, arm, checkpoint, claim) was made by looking at it.
- Statistics are computed correctly: pooled seeds use the question-clustered
  test (per-question mean over seeds, test across questions). Summing
  discordant pairs over seeds treats correlated question-seed pairs as
  independent and gives p values that are too small (R13).

Everything else is practice, not rule, and gives way whenever another
choice makes the paper better (owner, 2026-10-29). Never block an option,
and never call a result invalid or worthless, because a practice was
skipped; if a reviewer could object, say so in one line and recommend what
makes the paper strongest. The owner decides.

- Explore freely: read any result, add arms after reading results, write
  no pass/fail rule beforehand. Log every run and every choice in LAB_LOG.
- Run a control only when its result could change the method or reviewers
  will certainly ask for it (owner, 2026-10-26).
- A claim stays when most of the results that test it support it; the main
  text and appendix hold only results that serve the claims; the owner
  decides which comparisons and claims the paper reports (owner,
  2026-10-28). Claims and evaluation sets may be added at any time (for
  example Spider-DK, 2026-10-29).
- Selection on dev inflates: with about 140 discordant questions per Spider
  dev contrast, the best of ten variants with no true effect still shows
  about +1.7 points, one reason dev gains shrink on test. A result that
  carries the story should hold on more seeds or on test.
- Screens are seed 0 with paired questions and exact McNemar tests; one
  Spider question is about 0.1 point. The main claims use three seeds.
- Claim only what a comparator isolates.
- Compare central and FL at matched data passes, not only at the final
  checkpoint; a central run past its peak hides the FL penalty (R9).
- pass@k on training questions is a ceiling with a gold oracle, not a
  forecast of dev EX (P2.28 lesson).

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

## Writing reports for the advisor

Learned from the owner's edits to the 2026-10-29 advisor report. The
advisor knows the project; the report gives results and the points to
decide, not the lab's reasoning.

- Tables carry the numbers. A remark states the conclusion in plain words
  (for example "cùng chiều nhưng chưa tăng rõ rệt trên Spider test") and
  does not repeat the table's numbers or compare seeds one by one.
- In result tables, bold the best value of each column among the federated
  arms, also when it is not the method, and the best reference value.
- No p-values, significance forecasts or test names in remarks and
  discussion points.
- No selection or methodology commentary (which seed or set chose what) and
  no list of runs still missing; the plan section covers progress.
- A changed setting gets one sentence on what changed; leave out
  implementation details (token budgets) and consequences the reader can
  infer.
- The discussion section is "Các điểm cần cân nhắc", not "Vấn đề". Each
  point gives the fact, the few numbers it rests on, and one plain
  explanation, not an arithmetic breakdown.
