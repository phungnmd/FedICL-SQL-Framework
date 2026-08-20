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

**Status:** complete 2026-08-20, no GPU.

**Purpose:** prevent the manuscript from promising mechanisms or settings that
the implementation does not support.

**Decisions applied:**

- Replace “heterogeneous client models” with “asymmetric server-client model
  setting”; all clients currently share the same SLM architecture.
- Use “structural data isolation” instead of a formal privacy-preserving
  mechanism.
- Remove structural distillation from the proposed method and ablation list.
- Present FedAvg-LoRA as the FL baseline/protocol, not a novel optimizer.
- State that current logit KD requires teacher/student vocabulary compatibility.
- Use the pragmatic RQ2 wording: resource/communication savings from keeping
  the 7B teacher off clients and out of deployment inference while measuring
  how much accuracy the 1.5B model retains.
- Do not claim competitive accuracy versus actual federated 7B training; full
  7B FL is not scheduled by default.
- Collapse duplicated outline baselines such as FedAvg-SLM and FedAvg-LoRA
  unless full-model FL is genuinely implemented.

**Frozen claim-to-evidence boundary:**

| Planned claim | Required evidence | Forbidden stronger wording |
|---|---|---|
| LLM guidance improves federated SLM accuracy | matched T1 supervision ladder, then targeted replication if decisive | any gain is caused by the LLM before the public-gold control |
| The 1.5B client/deployed model avoids 7B costs | adapter traffic plus matched 1.5B/7B resource measurements | empirically cheaper or more accurate than full federated 7B training |
| Private rows stay local in the implemented protocol | architecture/data-flow audit | formal privacy, DP, or secure aggregation guarantee |
| Method operates under non-IID client data | frozen split statistics and scoped results | broad non-IID robustness from one `alpha=0.5` setting |

**Gate T0:**

- If the pragmatic RQ2 is selected, a controlled 7B resource benchmark is
  sufficient; do not schedule full 7B FL automatically.
- If the strong RQ2 is retained, add an actual federated 7B feasibility task
  before the paper can claim it.

### T1 — matched public-supervision ablation

**Status:** active; P0.0 verified and P0.1 public-gold CE is currently running.
Do not interrupt P0.1; treat its accuracy as valid and its opportunistic shared-
server resource measurements as non-paper evidence.

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
- Correct the centralized ceiling before freezing the main table:
  - retain the existing three chained one-epoch artifact as
    `Centralized-3pass-restart`;
  - run `Centralized-3ep-standard` once with one optimizer and one cosine
    schedule across `epochs=3`;
  - evaluate both on identical Spider rows and use the stronger result while
    reporting its exact schedule.
- Do not revive historical “Centralized + CE” artifacts as official evidence:
  they use mismatched public-pool sizes or mixed CE/RKL/re-finetuning stages.
  After Gate T1, add a new matched centralized public-supervision lineage only
  if the final paper table needs it and the intended target is unambiguous.

**Reconstruction audit:** the selection checkpoint contains all 3,873 retained
source indices, so the control is recoverable exactly. Joining on
`(question, db_id)` is forbidden because five duplicated/ambiguous keys affect
nine rows. `scripts/build_public_gold_control.py` instead aligns by stored source
index, verifies question/database/path identity, preserves row order and prompt
fields, replaces only `query`, and records input/output hashes.

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
this gate and the centralized-recipe check are reviewed.

### T2 — efficiency and resource evidence

**Status:** activate after T1 supports a paperable method; most subtasks do not
require accuracy retraining.

**Question:** what accuracy is retained, and what client/deployment cost is
avoided by keeping the 7B teacher off clients and out of inference?

**Todo — extract existing evidence:**

- Adapter bytes and estimated trainable parameter count.
- Client upload, server broadcast, per-round total, and cumulative T3 traffic.
- Treat old client/server time as operational logs unless the run was fresh and
  hardware-exclusive. Accuracy and communication fields remain usable.
- Extract client/server training steps and communication from existing records;
  do not silently promote opportunistic wall time to paper evidence.
- One-time teacher generation, EX filtering, logit-cache build time, and cache
  disk footprint; keep offline and recurring costs separate.

**Todo — fill missing measurements:**

- Add a tested analysis utility that consumes committed metrics/manifests and
  emits a reproducible resource table.
- Use the new process resource instrumentation for all future official runs:
  synchronized elapsed time, processed examples, optimizer updates,
  examples/second, process peak RSS, peak PyTorch allocated/reserved VRAM,
  runtime versions, and fresh/resumed/reused-stage eligibility.
- Consider `paper_timing_eligible=true` necessary but not sufficient: the GPU
  must also be exclusive and the run explicitly logged as controlled.
- Never use resumed eval timing or a federated round wall time that reused
  client/server stages. Their accuracy remains valid.
- Keep metric labels precise: process RSS is not system RAM, and PyTorch
  allocated/reserved memory is not total `nvidia-smi` device memory.
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
| 2026-08-20 | T0 claim alignment | outline claims versus implemented architecture and available resource evidence | pragmatic RQ2 selected; no full 7B FL by default; claims limited to asymmetric server-client setting and structural data isolation | T1 |
| 2026-08-20 | T1 reconstruction preflight | BIRD source CSV, frozen teacher pool, selection checkpoint, duplicate-key audit | exact 3,873-row gold control is reconstructable by source index; activate only the missing gold-CE branch | T1 P0.1 |
| 2026-08-20 | baseline/resource audit | centralized configs, trainer/eval timing paths, VRAM and communication logging | keep P0.1 running for accuracy; add standard continuous 3-epoch centralized baseline; old shared-server timing is operational only; instrument future official measurements | finish T1, then centralized recipe check |

## 6. Current next actions

1. Let the currently running P0.1 public-gold CE branch finish; do not pull code
   or interrupt that process mid-run.
2. After it exits, pull the instrumentation update and run P0.2: evaluate FL,
   public-gold CE, teacher-target CE, and full FedLS-SQL on the same Spider rows.
3. Run P0.3-P0.4: one standard continuous centralized three-epoch training run,
   then evaluate it beside the existing three-pass-restart adapter.
4. Stop at the combined gate. Select the stronger explicitly named centralized
   recipe and update the plan from the observed T1 causal contrast.
5. Do not interpret P0.1's shared-server time/RAM as official resource evidence;
   T2 will use controlled, repeated, hardware-exclusive measurements.

Seed-1/seed-2 commands are parked, not scientifically cancelled; they may be
reactivated later under T7 if the final headline contrast needs replication.
