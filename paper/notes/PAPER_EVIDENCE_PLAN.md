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
8. After validating a result, update its stable ID in `RESULT_REGISTRY.md` and
   its single paper-facing value in `paper/results/MAIN_RESULTS.md`; do not
   create a competing summary table in the plan or lab log.

## 3. Current assessment

### Evidence already strong enough to retain

- Correct independent comparison among Centralized, pure FL, and FedLS-SQL at
  T3, seed 0.
- FedLS-SQL exceeds pure FL on Spider and has positive T3 deltas on Realistic,
  Syn, DK, and BIRD.
- T1 server-stage effect has three-seed evidence.
- The matched T1 seed-0 ladder separates teacher guidance from an equal-size
  public-gold CE control: public gold is neutral, teacher targets add `3.48`
  EX, and full FedLS-SQL adds `5.51` EX over public gold.
- Pure FL and FedLS-SQL T1-T3 trajectories exist at seed 0.
- ICL and FLoRA-NA are closed negative branches.
- The privacy boundary is documented as structural data isolation rather than
  formal differential privacy.

### Main unresolved threats

1. **Headline reliability:** the final T3 FL-versus-FedLS-SQL contrast has only
   one training seed.
2. **Model-family scope:** student and teacher are both Qwen-family models, and
   token-level RKL is vocabulary-dependent.
3. **Efficiency claim:** communication is recorded, but the client/server
   resource story and fair 1.5B-versus-7B comparison are incomplete.
4. **Mechanism/metric risk:** server refinement sharply reduces EM while EX and
   execution validity improve; equivalent-SQL and false-positive EX cases need
   an explicit audit.
5. **Component reliability:** teacher-target CE is causally supported at seed
   0, but the standalone reverse-KL increment is not established across seeds.
6. **Baseline strength:** FedProx-LoRA is absent.
7. **Non-IID scope:** only one grouped Dirichlet setting is evaluated.

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

**Status:** complete at seed 0 on 2026-08-20; Gate T1 passed. Shared-server
accuracy is valid, but opportunistic resource measurements are non-paper
evidence.

**Question:** does improvement come from LLM guidance, or merely from adding a
public supervised training pass?

**Required matched ladder:**

| Arm | Shared starting point | Server treatment |
|---|---|---|
| FL | same FedAvg adapter | none |
| FL + public-gold CE | same FedAvg adapter | CE on BIRD gold SQL for the exact retained 3,873 rows |
| FL + teacher-target CE | same FedAvg adapter | CE on teacher SQL (`fedavg_pub`) |
| FedLS-SQL | same FedAvg adapter | teacher-target CE + reverse KL (`fedkd`) |

**Observed matched result:**

| Arm | EX | EM | Execution-error rate |
|---|---:|---:|---:|
| FL | 57.35 | 50.58 | 22.82% |
| FL + matched public-gold CE | 57.83 | 23.89 | 18.86% |
| FL + teacher-target CE | 61.32 | 30.27 | 15.57% |
| FedLS-SQL | **63.35** | 31.53 | **12.86%** |

On the same 1,034 rows, public gold over FL is `+0.48 pp` with 127 wins and 122
losses (`p=0.800`); teacher targets over public gold are `+3.48 pp`, 86/50
(`p=0.0026`); reverse KL over teacher-target CE is `+2.03 pp`, 59/38
(`p=0.0417`); and full FedLS-SQL over public gold is `+5.51 pp`, 93/36
(`p<1e-6`). These are paired question-level tests for one training seed.

**Remaining work attached to T1:**

- Audit execution-error categories and representative `EX=1, EM=0` cases.
- Do not infer that reverse KL is independently stable from seed 0: the
  existing three-seed reverse-KL contrast is `+1.71 ± 1.38 pp`, `p=0.165`.
- Replicate only the missing public-gold control at seeds 1/2 if the final
  headline causal statement requires training-seed uncertainty.
- The centralized correction is complete: standard continuous is `67.31 EX`
  and three-pass restart is `67.60 EX`; the `0.29 pp` paired difference is null
  (`p=0.863`). Use standard as the official conventional baseline and retain
  restart only as schedule sensitivity.
- Do not revive historical “Centralized + CE” artifacts as official evidence:
  they use mismatched public-pool sizes or mixed CE/RKL/re-finetuning stages.
  Add a new matched centralized teacher-guidance lineage only if the final
  reviewer audit needs to separate federation from the same server treatment.

**Reconstruction audit:** the selection checkpoint contains all 3,873 retained
source indices, so the control is recoverable exactly. Joining on
`(question, db_id)` is forbidden because five duplicated/ambiguous keys affect
nine rows. `scripts/build_public_gold_control.py` instead aligns by stored source
index, verifies question/database/path identity, preserves row order and prompt
fields, replaces only `query`, and records input/output hashes.

**Gate T1 decision:** retain LLM-to-SLM guidance as the central contribution.
The null public-gold control rules out “merely one extra public supervised pass”
as the main explanation at seed 0. Attribute the strongest supported mechanism
to teacher-generated hard targets; describe reverse KL as an additional
positive component pending stronger across-seed evidence. Do not claim that it
transfers latent reasoning without a dedicated analysis.

Do not activate FedProx, heterogeneity sweeps, or broad replication before the
second-family gate is reviewed. Final-endpoint replication remains required
before submission, but it is deferred under the current evidence-discovery
priority.

### T1R — final-endpoint reliability

**Status:** deferred by current research priority; commands are preserved as
P0.8 and may be reactivated after the portability/resource gates.

**Question:** is the headline T3 gain over independent pure FL stable across
training randomness, rather than a seed-0 outcome?

**Minimum screen:**

- Train only independent pure FL and full FedLS-SQL through T3 at training
  seeds 1 and 2 on the existing fixed `K=5, alpha=0.5` partition.
- Evaluate only the final T3 endpoints on Spider first.
- Do not repeat all intermediate rounds, OOD datasets, public-gold controls, or
  centralized baselines unless the final contrast is unstable.
- Report the three training-seed FL/FedLS deltas and mean ± sample SD. Keep
  question-level paired tests separate from training-seed uncertainty.

**Gate T1R:**

- **Direction and magnitude remain stable:** retain the headline accuracy
  claim and proceed to second-family portability.
- **Direction is stable but noisy:** report the uncertainty and consider only
  one additional seed; do not expand the whole grid.
- **One or both new seeds reverse the gain:** weaken the headline claim and
  investigate training instability before spending compute on portability or
  heterogeneity.

### T1F — second-family full-method screen

**Status:** active as P0.7; the Gemma 2B client smoke passed. Run the
teacher/tokenizer/cache smoke next, then one round and one seed before any
expansion.

**Question:** does the complete teacher-guided server stage transfer from the
Qwen family to a second, internally tokenizer-compatible Gemma teacher/student
pair?

**Minimum screen:**

- Use `google/gemma-2-9b-it` as teacher and `google/gemma-2-2b-it` as student,
  subject to license access, student LoRA/inference smoke, and an exact
  token-to-ID compatibility check.
- Generate targets for all 9,428 BIRD training rows, apply Qwen's same
  8-second quick-execution filter and official EX-to-gold stage independently
  to Gemma, and call the retained count `N_gemma`. Build the gold control on
  exactly those Gemma-selected indices; never select Gemma rows using Qwen's
  3,873 success indices.
- Before making a cross-family retention claim, execute all 9,428 source gold
  SQL independently and report each teacher's matches over the same valid-gold
  mask. Teacher-conditioned `gold_exec_failed` counts are diagnostics, not
  comparable denominators.
- Keep the Spider split, prompts, LoRA policy, seed 0, and T1 evaluation fixed.
  Score logits online for T1; cache the full pool only if later rounds reuse it.
- Evaluate the untouched Gemma 2B base, then from one shared Gemma T1 FedAvg
  adapter compare no server treatment, CE on the exact matched BIRD-gold rows,
  CE on Gemma-teacher SQL, and CE plus reverse KL from the Gemma teacher. Never
  reuse Qwen targets or Qwen logits.
- Label the final compatible-family endpoint full FedLS-SQL; retain the
  teacher-target-only branch as the sequence-KD ablation.
- Do not add model-size sweeps or a second alternative family at this gate.
- Evaluate the 4-bit Gemma 9B teacher zero-shot on Spider only after the main
  ladder; use it as ceiling/context evidence, not as a substitute for FL vs
  FedLS causal comparisons.

**Gate T1F:**

- **Full Gemma FedLS materially beats FL and matched public gold, with a useful
  teacher-target increment:** the complete framework has second-family
  evidence; consider extending only this track to T3/Spider.
- **Small or uncertain gain:** add at most one training seed before deciding.
- **No gain or regression:** stop the branch and scope the paper to the tested
  Qwen setting; do not tune Gemma until positive.

The claim remains family-level replication, not arbitrary cross-tokenizer
distillation. It replicates the generation and selection procedure, not an
equal-row cross-family budget: `N_gemma` may differ from Qwen's 3,873. A later
equal-budget comparison must subsample each teacher's own matched pool to a
common count. Full-vocabulary reverse KL is allowed only after exact token-ID
compatibility passes; a failure stops the full Gemma branch rather than
silently slicing unrelated vocabularies.

### T2 — efficiency and resource evidence

**Status:** communication payload is complete; controlled measurement follows
the active T1F gate. It supports the efficiency claim but does not replace
eventual final-endpoint reliability.

**Question:** what accuracy is retained, and what client/deployment cost is
avoided by keeping the 7B teacher off clients and out of inference?

**Todo — extract existing evidence:**

- Adapter bytes are closed; export the exact trainable parameter count beside
  them.
- Client upload, server broadcast, per-round total, and cumulative T3 traffic
  are closed: `369,555,560` upload + `369,555,400` broadcast = `739,110,960`
  bytes per round and `2,217,332,880` bytes through T3.
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

**Status:** manuscript skeleton may now begin; freeze results only after T2-T5
decisions.

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
- Freeze all table values through `paper/results/MAIN_RESULTS.md`; manuscript
  drafts should consume that file rather than maintain independent numbers.
- Record limitations: no formal privacy, public-pool dependence,
  vocabulary-compatible KD, one teacher/student family, and offline teacher
  cost.

**Gate T6:**

- Perform a reviewer-style evidence audit. Any new run must map to a concrete
  missing cell or objection; otherwise it is not scheduled.

### T7 — additional targeted reliability replication

**Status:** intentionally late and conditional. T1R already covers the final
T3 FL-versus-FedLS-SQL headline contrast; this task covers only uncertainty
that remains after the main gates.

**Question:** which causal components or secondary contrasts still depend too
heavily on seed 0 after T1R closes the final endpoint comparison?

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
| 2026-08-20 | T1 matched-supervision gate | 1,034 paired Spider predictions for FL, public-gold CE, teacher-target CE, and full FedLS-SQL | teacher targets beat matched public gold by 3.48 EX; full method beats it by 5.51 EX; retain large-to-small claim, keep standalone RKL claim provisional | P0.3-P0.4 centralized recipe check |
| 2026-08-20 | P0.5 centralized-recipe gate | standard continuous 3 epochs versus three-pass restart on 1,034 paired Spider rows | recipes are indistinguishable in EX; select standard 67.31 as official baseline, retain restart 67.60 as schedule sensitivity | T2 resources and T1 mechanism audit |
| 2026-08-20 | post-P0.5 evidence audit | canonical registry, committed communication metrics, and resource instrumentation | fill standard centralized OOD/BIRD cells first; communication payload needs no rerun; add fixed in-process warm-up before official latency | P0.6 centralized transfer suite |
| 2026-08-20 | Q3 evidence-priority review | headline seed coverage, Qwen-only scope, resource claim, and compute cost | after P0.6, prioritize final T3 seed-1/2 reliability, then one-round Gemma sequence-KD portability; resource benchmark follows those scientific-validity gates | P0.6, then T1R |
| 2026-08-20 | P0.6 centralized transfer gate | official standard adapter on Realistic, Syn, DK, and BIRD with paired final-model audit | fill final table; retain competitiveness claim but reject uniform FedLS-over-centralized OOD superiority | T1R/P0.7 |
| 2026-08-20 | post-P0.6 priority revision | advisor outline ablations, Qwen-only limitation, existing seed-0 breadth, and user compute priority | defer final seed replication; activate a cheap Gemma smoke followed by a matched FL/public-gold/teacher-target T1 portability ladder | T1F/P0.7a |
| 2026-08-21 | same-family replication revision | a mixed Qwen-teacher/Gemma-student run cannot test the full reverse-KL endpoint | use Gemma 2 9B→2B, regenerate targets and logits, and compare the five-arm base/FL/gold/target/full ladder after strict tokenizer validation | T1F/P0.7a-d |
| 2026-08-21 | Gemma lineage correction | fingerprint audit found the old smoke output was sourced from Qwen's selected 3,873 rows | use new immutable `fullsource` smoke roots and the common raw-generation → 8-second quick-exec → official-EX selector over all 9,428 BIRD rows | T1F/P0.7b-e |

## 6. Current next actions

1. P0.7a is complete: Gemma 2B training/reload/inference compatibility passed;
   do not interpret its eight-row accuracy.
2. P0.7b-c generated all Gemma teacher outcomes; retain deterministic empty
   generations as teacher failures and reject them before SQL execution.
3. Run P0.7e next, then run P0.7s sequentially because this host cannot safely
   co-load the 9B teacher and train the 2B student.
4. After selection completes, run P0.7d gold CE, target CE, full online CE+RKL,
   and the canonical five-arm base/FL/gold/target/full evaluation. Defer a full
   cache until a positive T1 result justifies T3 reuse.
5. Review full FedLS against FL, matched public gold, and sequence KD before any
   T3/OOD or additional family/size expansion.
6. After T1F, export the exact LoRA trainable-parameter count and add fixed
   in-process warm-up before the controlled 1.5B/7B resource benchmark.
6. Run the no-GPU T1 execution-error/EX-EM audit whenever it does not block the
   active GPU task.
7. Retain T1R/P0.8 final seed replication as a pre-submission reliability task;
   do not start it until the current discovery-first gate is reviewed.
8. Do not interpret shared-server time/RAM as official evidence;
   T2 will use controlled, repeated, hardware-exclusive measurements.

Final T3 seed-1/2 replication is deferred, not cancelled. Additional component
replication remains parked under T7.
