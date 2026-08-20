# FedLS-SQL — adaptive paper evidence plan

> Updated 2026-08-20. This is a decision plan, not a fixed experiment list.
> Results from an earlier task may reorder, replace, or cancel later tasks.
> `PIPELINE_NEXT.md` contains commands only for the task currently activated by
> this plan; it must not be treated as an unconditional queue.

## 1. Objective

Build the smallest defensible evidence package for a Q3 paper around the claim:

> Server-side LLM guidance can improve a federated LoRA-adapted SLM for
> NL-to-SQL while the clients and deployed system retain the communication and
> inference advantages of the smaller model.

The plan prioritizes threats to this claim over experiment volume. Additional
seeds, model sizes, ranks, clients, and datasets are added only when they resolve
an uncertainty exposed by an earlier result.

## 2. Working rules

1. Keep only one GPU-intensive task active at a time.
2. Before activating a task, state which RQ or reviewer objection it resolves.
3. Begin with the cheapest valid screen. Expand to more rounds or seeds only
   after the screen justifies it.
4. Never continue a sweep automatically. Review effect size, uncertainty,
   failure modes, compute cost, and claim consequences first.
5. A negative result may narrow the paper, replace a contribution, or stop a
   branch. It is not a reason to keep tuning until the desired result appears.
6. Preserve immutable artifact roots and provenance. New scientific settings
   receive new output and evaluation-resume directories.
7. After each decision gate, update this file, `EXPERIMENT_MATRIX.md`, and the
   active portion of `PIPELINE_NEXT.md` before launching more work.

## 3. Current assessment

### Evidence already strong enough to retain

- Correct independent comparison among Centralized, pure FL, and FedLS-SQL at
  T3, seed 0.
- FedLS-SQL exceeds pure FL on Spider and has positive T3 deltas on Realistic,
  Syn, DK, and BIRD.
- T1 server-stage effect has three-seed evidence.
- Pure FL and FedLS-SQL T1-T3 trajectories exist at seed 0.
- ICL and FLoRA-NA are closed negative branches.
- The privacy boundary is documented as structural data isolation rather than
  formal differential privacy.

### Main unresolved threats

1. **Causal attribution:** teacher guidance is not yet separated cleanly from
   learning on an additional public labeled pool.
2. **Efficiency claim:** communication is recorded, but the client/server
   resource story and fair 1.5B-versus-7B comparison are incomplete.
3. **Baseline strength:** FedProx-LoRA is absent.
4. **Non-IID scope:** only one grouped Dirichlet setting is evaluated.
5. **Analysis depth:** paper-facing error analysis is absent.
6. **Reliability:** T2/T3 has one training seed, but this is secondary until the
   final causal comparison and paper claims are stable.

## 4. Adaptive task queue

The order below is the current best order. Only the first unfinished task whose
prerequisites remain valid is active. Decision gates may change everything
below it.

### T0 — align claims and experimental vocabulary

**Status:** next, no GPU.

**Purpose:** prevent the manuscript from promising mechanisms or settings that
the implementation does not support.

**Todo:**

- Replace “heterogeneous client models” with “asymmetric server-client model
  setting”; all clients currently share the same SLM architecture.
- Use “structural data isolation” instead of a formal privacy-preserving
  mechanism.
- Remove structural distillation from the proposed method and ablation list.
- Present FedAvg-LoRA as the FL baseline/protocol, not a novel optimizer.
- State that current logit KD requires teacher/student vocabulary compatibility.
- Decide the RQ2 wording:
  - pragmatic: resource/communication savings relative to using a 7B model;
  - strong: competitive accuracy versus actual federated 7B training.
- Collapse duplicated outline baselines such as FedAvg-SLM and FedAvg-LoRA
  unless full-model FL is genuinely implemented.

**Deliverable:** one frozen claim-to-evidence table identifying each planned
paper claim, its current support, and its forbidden stronger wording.

**Gate T0:**

- If the pragmatic RQ2 is selected, a controlled 7B resource benchmark is
  sufficient; do not schedule full 7B FL automatically.
- If the strong RQ2 is retained, add an actual federated 7B feasibility task
  before the paper can claim it.

### T1 — matched public-supervision ablation

**Status:** highest-priority empirical task after T0.

**Question:** does improvement come from LLM guidance, or merely from adding a
public supervised training pass?

**Required matched ladder:**

| Arm | Shared starting point | Server treatment |
|---|---|---|
| FL | same FedAvg adapter | none |
| FL + public-gold CE | same FedAvg adapter | CE on BIRD gold SQL for the exact retained 3,873 rows |
| FL + teacher-target CE | same FedAvg adapter | CE on teacher SQL (`fedavg_pub`) |
| FedLS-SQL | same FedAvg adapter | teacher-target CE + reverse KL (`fedkd`) |

**Todo:**

- Build a provenance-preserving public-gold CSV using exactly the row identities
  in the frozen 3,873-row teacher pool.
- Verify schema/database paths, row count, row identity, split isolation, and
  target-source metadata.
- Reuse the same T1 FedAvg checkpoint so only server supervision changes.
- Initially run only the missing public-gold server arm at seed 0.
- Evaluate all four arms on identical Spider rows with the canonical greedy,
  zero-shot protocol.
- Compare EX, execution-error rate, paired wins/losses, and confidence intervals;
  treat EM as secondary across different target conventions.

**Gate T1:**

- **Teacher targets and/or logits clearly improve over matched public gold:**
  retain LLM-to-SLM guidance as the central contribution. Decide whether the
  comparison must be extended to T3 or additional seeds based on effect size
  and uncertainty.
- **Teacher-target CE is similar to public-gold CE, but reverse KL adds value:**
  center the method on soft teacher guidance; replicate only the decisive
  public-gold versus full comparison.
- **Public-gold CE explains most or all of the gain:** reframe the paper as
  public-data-assisted federated SLM training, or redesign the transfer
  mechanism before spending compute on robustness/seeds.
- **Public-gold CE is harmful while teacher supervision helps:** retain the
  large-to-small story, but analyze why teacher-generated equivalent SQL is
  easier or more useful than BIRD gold.

Do not activate FedProx, heterogeneity sweeps, or T2/T3 seed replication until
this gate is reviewed.

### T2 — efficiency and resource evidence

**Status:** activate after T1 supports a paperable method; most subtasks do not
require accuracy retraining.

**Question:** what accuracy is retained, and what client/deployment cost is
avoided by keeping the 7B teacher off clients and out of inference?

**Todo — extract existing evidence:**

- Adapter bytes and estimated trainable parameter count.
- Client upload, server broadcast, per-round total, and cumulative T3 traffic.
- Client training time and peak VRAM by client and round.
- Server CE/KD time and peak VRAM by round.
- One-time teacher generation, EX filtering, logit-cache build time, and cache
  disk footprint; keep offline and recurring costs separate.

**Todo — fill missing measurements:**

- Add a tested analysis utility that consumes committed metrics/manifests and
  emits a reproducible resource table.
- Record CPU peak memory or explicitly mark it unavailable.
- Run matched inference benchmarks for:
  - base 1.5B SLM;
  - final FedLS-SQL 1.5B;
  - zero-shot 7B teacher.
- Use identical GPU, rows, max length, decoding, batch size, warm-up, and timing
  procedure.
- If RQ2 uses a training-cost comparison, run a controlled client LoRA
  microbenchmark for 1.5B and 7B with identical examples and optimizer updates.

**Gate T2:**

- **Clear client/inference savings with acceptable accuracy retention:** retain
  the accuracy-efficiency contribution and proceed.
- **Inference savings are clear but client training remains too memory-heavy:**
  narrow the claim to deployment and avoidance of the client-side 7B teacher;
  do not call the current clients edge devices.
- **The strong RQ2 was selected and the microbenchmark is insufficient:** scope
  an actual 7B FedAvg-LoRA run or weaken RQ2 before proceeding.
- **Resource measurements expose an unacceptable bottleneck:** decide whether
  gradient checkpointing/QLoRA is a future-work limitation or a method change.
  A method change requires a new lineage and revalidation of headline results.

### T3 — FedProx-LoRA baseline

**Status:** conditional on T1-T2 retaining the current method.

**Question:** does FedLS-SQL still provide value against a standard
heterogeneity-aware FL optimizer rather than only FedAvg-LoRA?

**Todo:**

- Implement FedProx as a separate, fingerprinted aggregation/training setting.
- Add unit tests for the proximal objective and zero-coefficient equivalence to
  the existing local objective.
- Start with a short smoke run, then run T1-T3 on the main `K=5, alpha=0.5`
  split at seed 0.
- Evaluate the final T3 checkpoint on Spider first.

**Gate T3:**

- **FedLS-SQL remains clearly above FedProx:** retain FedAvg and FedProx as main
  FL baselines; broader optimizer sweeps are unnecessary.
- **FedProx closes the gap:** determine whether server KD on top of FedProx is
  required to establish optimizer-independent teacher value.
- **FedProx exceeds FedLS-SQL:** stop robustness/seeds and revisit the method or
  narrow the contribution to a FedAvg-based setting.

### T4 — controlled heterogeneity screen

**Status:** conditional on T3 and on the final RQ3 wording.

**Question:** does teacher guidance remain useful as client data become more
heterogeneous?

**Initial screen:**

| Setting | Intended interpretation |
|---|---|
| `alpha=100` | near-IID/domain-balanced reference |
| `alpha=0.5` | current main grouped-domain non-IID setting |
| `alpha=0.1` | stronger grouped-domain/quantity skew |

**Todo:**

- Validate that the three generated splits actually differ using client row
  counts, database counts, coefficient of variation, and domain-distribution
  entropy/JSD.
- Do not label `alpha=100` IID until the statistics support that description.
- Run seed-0 pure FL and FedLS-SQL through T3 for the two missing settings.
- Evaluate Spider first; expand OOD evaluation only if the heterogeneity result
  is interpretable and relevant.

**Gate T4:**

- **FedLS-SQL gain persists or grows with heterogeneity:** retain an RQ3
  robustness/convergence claim and consider one targeted replication.
- **Gain appears only at the main split:** scope conclusions to grouped-domain
  `alpha=0.5`; do not claim general non-IID robustness.
- **Split statistics do not isolate meaningful heterogeneity:** redesign the
  partition protocol before running models.
- **The outline still requires separate quantity and SQL-pattern skew:** add
  controlled partition builders as new tasks; do not infer those settings from
  Dirichlet alpha alone.

### T5 — paper-facing error and mechanism analysis

**Status:** perform after the final main comparison set is known; no GPU unless
analysis exposes a specific missing prediction set.

**Todo:**

- Compare matched prediction rows for FL, FedProx, public-gold CE,
  teacher-target CE, and FedLS-SQL where available.
- Report wins, losses, and unchanged cases.
- Stratify by Spider hardness and SQL constructs: JOIN, aggregation, GROUP BY,
  nested query, set operator, ordering/limit, and filtering.
- Separate invalid-SQL/execution failures from executable-but-wrong predictions.
- Inspect representative LLM-SLM transfer successes and failures without
  cherry-picking only favorable examples.
- Treat schema-linking analysis as approximate unless table/column extraction
  is implemented and validated.

**Gate T5:**

- Use the observed error pattern to support mechanism discussion.
- If no stable pattern appears, report a descriptive error analysis and avoid
  causal claims about why reverse KL works.

### T6 — manuscript skeleton and table freeze

**Status:** can begin after T1; freeze results only after T2-T5 decisions.

**Todo:**

- Draft Introduction, Related Work, Method, and Experimental Setup using only
  claims approved at T0-T2.
- Replace the broad outline experiment menu with experiments actually needed
  by the final RQs.
- Prepare four core artifacts:
  1. overall accuracy table;
  2. matched supervision/KD ablation table;
  3. convergence/heterogeneity figure;
  4. accuracy-resource-communication table.
- Record limitations: no formal privacy, public-pool dependence,
  vocabulary-compatible KD, one teacher/student family, and offline teacher
  cost.

**Gate T6:**

- Perform a reviewer-style evidence audit. Any new run must map to a concrete
  missing cell or objection; otherwise it is not scheduled.

### T7 — targeted reliability replication

**Status:** intentionally late and conditional.

**Question:** which final headline contrasts still depend too heavily on seed 0?

**Todo:**

- Replicate only the smallest set of decisive comparisons selected after T6.
- Prefer final endpoints and causal contrasts over repeating every intermediate
  arm on every dataset.
- Use seeds 1 and 2 only where they change a headline mean, variance estimate,
  or reviewer-facing conclusion.
- Do not automatically repeat BIRD or all OOD datasets if Spider and the main
  heterogeneity setting answer the reliability question.

**Gate T7:**

- **Direction and magnitude remain stable:** report mean ± sample SD and close
  the experimental phase.
- **Result is unstable:** weaken the claim, increase replication only for the
  unstable contrast, or revisit the method; do not hide the variance by pooling
  question-level tests.

### T8 — optional sensitivity work

**Status:** not active. Requires an explicit paper/advisor justification after
the T6 audit.

Candidates include teacher size, student size, LoRA rank, public-pool size,
number of clients, separate quantity skew, and SQL-pattern skew. Select at most
the experiments that resolve a known limitation. A full Cartesian sweep is not
part of the default plan.

## 5. Live decision ledger

Update this table after every gate. Never rewrite old decisions silently.

| Date | Gate | Evidence reviewed | Decision | Next active task |
|---|---|---|---|---|
| 2026-08-20 | initial architecture review | outline, architecture, lab log, result registry, implementation | multi-seed moved behind causal, efficiency, baseline, and heterogeneity evidence | T0 |

## 6. Current next actions

1. Complete T0 and choose pragmatic versus strong RQ2 wording.
2. Design the exact 3,873-row public-gold control for T1 and verify that its
   provenance can be reconstructed without changing the frozen teacher pool.
3. Only after that verification, replace the active seed commands in
   `PIPELINE_NEXT.md` with the smallest resumable T1 command block.

Until T1 is reviewed, the existing seed-1/seed-2 commands are parked, not
deleted; they may become useful later under T7.
