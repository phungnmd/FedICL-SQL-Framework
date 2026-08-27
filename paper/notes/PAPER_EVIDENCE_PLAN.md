# FedLS-SQL — target evidence and submission plan

> Updated 2026-08-27. This is an adaptive plan for the target outline in
> `PAPER_OUTLINE_TARGET.md`, not a promise to execute every experiment in the
> advisor's August 19 planning outline. Exact runnable commands belong only in
> `PIPELINE_NEXT.md`; the ordered adaptive backlog is `PAPER_TODO.md`.

## 1. Submission objective

The advisor's umbrella question remains the scientific target:

> Can large-to-small language model collaboration overcome the accuracy
> limitations of lightweight federated NL-to-SQL models while retaining the
> privacy, communication-efficiency, and resource advantages of federated
> learning?

The evidence-backed operational form avoids promising more than the protocol
can test:

> Execution-verified guidance from a server-side LLM improves a federated
> LoRA-adapted SLM for NL-to-SQL while client rows remain local, client
> communication is adapter-only, and deployment uses only the SLM.

The paper therefore keeps the advisor's direction but resolves its four parts
separately: EX improvement, causal large-to-small transfer, scoped non-IID
behavior, and measured communication/resource trade-offs. “Privacy” means
structural data isolation unless a formal mechanism is added; “large-model FL
advantage” requires an actual federated-7B experiment.

Execution accuracy (EX) is the primary endpoint. EM is reported transparently
as a secondary syntactic metric; it is not an optimization target because
public BIRD teacher targets and Spider evaluation can use different SQL forms.

## 2. Canonical method and claim boundary

```text
private client LoRA CE -> sample-weighted factor-wise FedAvg
                       -> execution-verified teacher-target CE
                       -> auxiliary reverse KL
```

- The portable mechanism supported by Qwen and Gemma is hard teacher-target
  transfer.
- Reverse KL is retained in the canonical Qwen endpoint but is not claimed as
  an independently stable or family-general contribution.
- FedAvg-LoRA is the federated protocol, not a novel optimizer.
- The privacy claim is structural data isolation, not DP or secure aggregation.
- The paper does not claim empirical superiority to federated 7B training.
- The exact P0.9 selection and P0.10 FedDF implementations are closed. New
  KD/Federated mechanisms remain admissible through the P1.7 hypothesis,
  matched-control, budget, and stop-rule gate.

## 3. Evidence already sufficient

- Correct centralized-standard, independent pure-FL, and FedLS-SQL comparison
  at Qwen T3 seed 0.
- FedLS-SQL improves over pure FL on Spider and has positive deltas on all
  retained robustness/cross-dataset evaluations.
- T1 server-stage improvement has three-seed evidence.
- The final T3 FedLS-SQL advantage has replicated at seeds 0 and 1 (`+5.23`
  and `+3.77` EX). This is sufficient for the current direction decision;
  seed 2 remains desirable for final three-seed reporting but is deferred.
- The matched public-supervision ladder shows that equal-row public-gold CE
  does not explain the teacher-target gain.
- Pure-FL and FedLS-SQL T1-T3 convergence trajectories exist.
- Gemma T1 provides a positive second-family endpoint and identifies hard
  teacher-target transfer as the portable mechanism.
- Adapter communication is closed at `738,590,720` logical FP32 tensor bytes
  per round and `2,215,772,160` bytes through T3; serialized artifact-file
  accounting is retained separately as an implementation audit.
- ICL, FLoRA-NA, adaptive selection, and FedDF are closed negative branches.

## 4. Definition of done for the target paper

The experimental phase is ready to freeze when all mandatory items hold:

1. the final T3 pure-FL versus FedLS contrast has seeds 0/1/2 or the claim has
   been weakened to reflect observed instability;
2. resource tables contain deterministic counts and fresh repeated
   process-memory/latency measurements with raw GPU telemetry, or the resource
   claim is narrowed to deterministic communication and structural deployment;
3. the error analysis explains EX gains, execution failures, and representative
   transfer behavior without treating EM as the target;
4. RQ3 wording is explicitly scoped to the fixed non-IID partition, or a
   minimal validated heterogeneity screen has been completed;
5. the related-work matrix locates the contribution boundary at the
   intersection of federated NL-to-SQL, asymmetric server/client models,
   execution-verified teacher transfer, and adapter-only communication without
   claiming that the individual components are new;
6. every paper value resolves to `MAIN_RESULTS.md` and `RESULT_REGISTRY.md`.

## 5. Active priority order

### Current execution state — advisor-aligned completion path

P0.8a and P0.8a-E are complete and positive, so accuracy no longer blocks the
remaining parts of the advisor question. P1.1b-v2 is reactivated as the next
GPU task. In parallel, draft the method/architecture figure, then design one
matched FedProx-LoRA baseline and one audited stronger-skew sensitivity. Seed 2
closes final reliability after these higher-value gaps. Federated 7B remains a
separate feasibility/claim gate rather than an implicit requirement.

| Lane | Order | Deliverable | Gate |
|---|---:|---|---|
| GPU complete | 1 | P0.8a pure-FL/FedLS T3 seed 1 | 61.99 vs 65.76 EX; `+3.77`, paired `p=0.00483` |
| GPU complete | 2 | P0.8a-E seed-1 trajectory cells | result commit `dbd703b`; full T1/T2/T3 trajectory registered |
| CPU complete | 1 | P1.4a deterministic efficiency/table manifest | artifact commit `147f455`; registry ID `audit.paper.tables.qwen.s0` |
| CPU complete | 2 | P1.4b related-work/novelty matrix and P2 skeleton | title narrowed; outputs `RELATED_WORK_NOVELTY_MATRIX.md` and `MANUSCRIPT_SKELETON.md` |
| CPU active | 3 | Method prose and architecture/privacy-boundary figure | immediate writing task; no GPU required |
| Method next | 4 | P1.7a execution-verified preference/contrastive KD | design/code/data frozen; run its active 512-row screen before other optional GPU work |
| GPU pending | 5 | P1.1b-v2 1.5B/7B deployment-resource benchmark | measured path and safe command are ready; run after the P1.7a screen |
| Design | 6 | P1.5 matched FedProx-LoRA | freeze coefficient rule and matched scientific contract before adding a command |
| Design | 7 | P1.3 one audited stronger-skew sensitivity | keep `K=5` and source rows fixed; T1 screen before any T3 extension |
| GPU deferred | 8 | P0.8b pure-FL/FedLS T3 seed 2 | final three-seed reporting after resource/baseline/sensitivity gaps |
| Claim gate | 9 | P1.6 federated-7B feasibility | run only if the paper retains empirical comparison with large-model FL |

### P1.1a — implement a shared-server resource benchmark

**Status:** complete through nested protocol commit `487b3b2`; the full
320-test suite passes.

**Reviewer objection resolved:** the paper claims resource and deployment
advantages but current timing came from opportunistic shared-server runs.

The benchmark must separate:

1. deterministic quantities: parameter counts, trainable counts, adapter and
   communication bytes;
2. process-scoped quantities: PyTorch peak allocated/reserved VRAM and process
   peak RSS;
3. contention-sensitive quantities: latency and throughput.

Required implementation contract:

- deterministic in-process warm-up excluded from reported rows;
- CUDA synchronization around every timed region;
- separate load, warm-up, generation, and SQL-scoring times;
- identical fixed rows and decoding within each matched comparison;
- student and teacher run sequentially on the same selected GPU;
- at least five fresh repetitions, reporting median and IQR;
- sample `nvidia-smi` device utilization, memory, clocks, pstate, and identity
  during every repetition without PID enumeration;
- treat every fresh successful repetition as independent and eligible;
- exclude only failed or resumed repetitions from the primary summary;
- preserve raw per-repetition JSON and runtime provenance.

This protocol does not claim guaranteed hardware exclusivity or automated
contention detection. The operator chooses a window with no intentionally
concurrent GPU job. Repetitions remain independent measurements and raw GPU
telemetry is disclosed as context.

**Gate:** tests must pass and the output schema must make ineligible timing
impossible to aggregate silently before P1.1b commands are added.

### P1.2 — EX-oriented error and transfer audit

**Status:** complete. Canonical artifact commit `4527a76` compares all 1,034
paired Qwen T3 Spider rows.

**Reviewer objection resolved:** what kinds of NL-to-SQL errors are corrected
by the server treatment, and are the reported EX gains interpretable?

Minimum analysis:

- paired FL/FedLS wins, losses, and unchanged rows;
- execution-error versus executable-but-wrong transitions;
- Spider hardness strata;
- validated JOIN, aggregation, nesting, set-operation, ordering/limit, and
  filtering indicators where reliable;
- fixed-rule representative successes and failures;
- a small audit of `EX=1, EM=0` cases to verify semantic correctness and
  document BIRD-to-Spider SQL-form variation.

**Gate:** promote only validated categories. If a structural classifier is not
reliable, report a smaller descriptive analysis rather than inferred labels.
Do not create a method branch merely to increase EM.

Observed decision:

- FedLS corrects 121 rows and regresses 67 (`+5.22 EX`, exact McNemar
  `p=0.0001002`).
- Execution errors fall from 193 to 101; 72 former execution failures become
  correct and another 56 become executable.
- The largest positive strata are medium difficulty (`+9.87`), LIMIT
  (`+13.23`), ORDER BY (`+11.81`), GROUP BY (`+7.22`), aggregation (`+5.99`),
  and JOIN (`+5.39`).
- Set operations are the clearest weakness (`-18.75`, 5 wins/20 losses); hard
  and nested-query subsets are approximately neutral.
- All 1,034 gold SQL parse under the SQLGlot SQLite audit. Construct strata are
  overlapping exploratory subsets, not multiple-testing-adjusted causal
  claims.

This evidence supports a targeted discussion and can motivate a new P1.7
method hypothesis. It does not by itself authorize a training branch: the
hypothesis must explain the affected EX stratum, matched control, budget, and
promotion rule. A high-value low-cost proposal may be reprioritized explicitly
rather than being blocked behind every existing queue item.

### P1.1b — collect resource evidence

**Status:** command ready but pending behind the user-prioritized P1.7a screen.
The fresh-root v2 command in `PIPELINE_NEXT.md` must not be mixed with the
superseded PID-gated collection.

The current P1.1b command collects the first evidence block:

1. deployed Qwen 1.5B FedLS versus Qwen 7B teacher inference on identical
   rows.

Two possible training-resource blocks remain a post-P0.8 decision, not an
implicit promise:

2. client 1.5B LoRA training process memory and throughput on a fixed
   microbenchmark;
3. recurring server KD process memory/throughput, separated from one-time
   teacher target generation and cache construction.

If blocks 2/3 are not run, narrow RQ4 and contribution 4 to deterministic
adapter communication plus measured deployment inference. Do not retain prose
claiming measured client/server training-resource savings without those runs.

Do not compare 1.5B client training with 7B inference as though it were an
empirical federated-7B baseline. The supported conclusion is that the teacher
is absent from clients/deployment and client network payload is adapter-only.

### P0.8 — final T3 training-seed reliability

**Status:** seed 1 final endpoint and full trajectory are complete and
positive; seed 2 is deferred. The trajectory completion is registered at
result commit `dbd703b`.

Reliability extensions use only independent pure FL and frozen FedLS-SQL on
the existing split. Seed 1 is complete; seed 2 resumes only when final
three-seed reporting is prioritized.

Seed 1 reaches 61.99 EX for pure FL and 65.76 for FedLS-SQL (`+3.77`), with
111 paired corrections versus 72 regressions (`p=0.00483`) and execution
errors reduced from 213 to 126. Together with seed 0, the completed-seed mean
delta is `+4.50` EX with sample SD `1.03`.

Seed 2 resumes the already-established canonical T1 roots
`fedavg_noicl_k5_e1_t1_s2` and `fedkd_noicl_k5_e1_t1_s2` by invoking rounds 2
and 3 explicitly. Restarting a three-round loop from round 1 or creating a new
pure-FL seed-2 root would break the intended lineage and is prohibited.

Deferred seed-2 decision gate:

- seed 2 positive: report the three-seed mean and sample SD and retain
  the headline claim;
- seed 2 positive but noisy: report uncertainty and avoid expanding all OOD runs;
- seed 2 reversed: verify lineage, weaken the claim, and diagnose instability before any
  optional experiment.

Question-level paired tests and training-seed uncertainty must remain separate.

### P1.3 — RQ3 scope decision

**Status:** the advisor-aligned path selects exactly one audited stronger-skew
sensitivity. Design and split audit precede any training command.

The scoped fallback remains valid if the split audit cannot demonstrate a
meaningful increase in heterogeneity. The selected path is:

1. construct one stronger-skew split while holding source rows and `K=5`
   fixed;
2. verify client sizes, database/domain distributions, entropy/JSD, and the
   direction of the intended skew;
3. compare only pure FL and frozen FedLS-SQL on Spider at T1;
4. extend to T3 only after a positive, interpretable preregistered gate.

Do not call `alpha=100` IID or `alpha=0.1` stronger heterogeneity until split
statistics confirm database/domain distribution, row-count variation, and
entropy/JSD differences. Separate quantity-skew and SQL-pattern-skew builders
are outside the default paper.

**Fallback gate:** if the new split is not measurably more heterogeneous or the
T1 contrast is uninterpretable, stop and scope RQ3 to the existing partition.

### P1.4a — deterministic efficiency and table manifest

**Status:** complete. Artifact-only builder lineage ends at `f59a040`; compact
JSON/CSV were committed at nested result commit `147f455` and registered as
`audit.paper.tables.qwen.s0`.

Produce a compact paper-table manifest that:

- derives trainable LoRA parameter counts and serialized adapter bytes from
  immutable artifacts without loading a model on GPU;
- records upload, broadcast, per-round, and T3 cumulative communication with
  units and formulas;
- validates the intentional seed-0 FedLS split lineage and every round's
  aggregation metadata;
- emits compact JSON/CSV that can be registered and consumed locally without
  copying terminal values or moving adapter weights.

**Gate:** no paper-facing number may lack a registry/artifact path and formula
or evaluation provenance.

### P1.4b — related-work and novelty audit

**Status:** complete 2026-08-26.

Build a comparison matrix covering recent:

- text-to-SQL LLM-to-SLM distillation;
- federated language-model distillation;
- federated PEFT/LoRA;
- federated NL-to-SQL.

The nearest-work set must explicitly cover FedMKT, FedCoLLM, FedCoT, LaDa,
FedGen/data-free server refinement, and the closest execution-aware
small-model NL-to-SQL systems. The broad large-small federated architecture is
not itself a defensible first claim.

Compare task, client/server model asymmetry, private/public data boundary,
teacher location, transferred object, execution verification, communication,
and deployed model. Revise the title if “novel” cannot be defended for the
complete combination.

Outcome: FedCoLLM is the closest architectural prior and Struct-SQL the
closest execution-filtered Text-to-SQL KD prior. The title is now
“FedLS-SQL: Execution-Verified Large-to-Small Knowledge Transfer for
Federated NL-to-SQL.” The full matrix and safe/prohibited wording are in
`RELATED_WORK_NOVELTY_MATRIX.md`; the P2 section/evidence map is in
`MANUSCRIPT_SKELETON.md`.

### P2 — manuscript build and evidence freeze

**Status:** evidence-mapped skeleton complete in `MANUSCRIPT_SKELETON.md`;
method prose and the architecture figure are next. Final resource/robustness
wording waits for the remaining decision gates.

Draft against `PAPER_OUTLINE_TARGET.md`. Freeze seven core artifacts:

1. architecture/privacy-boundary figure;
2. main centralized/FL/FedLS accuracy table;
3. matched transfer ablation;
4. convergence figure;
5. Gemma portability table;
6. accuracy-resource-communication table;
7. EX-oriented error analysis.

Perform a reviewer-style audit before scheduling anything else. Every new run
must fill a named missing cell or answer a concrete objection.

## 6. Gated reviewer baselines

These require a gate and are not yet executable commands:

- **FedProx-LoRA:** recommended before submission as the minimum stronger
  federated optimizer baseline. Match model, split, LoRA, local work, rounds,
  and evaluation; predeclare coefficient selection without test-set tuning.
- **Qwen/Gemma teacher zero-shot:** contextual accuracy/resource reference,
  not a causal method arm.
- **Federated 7B:** required only for a strong empirical claim against
  large-model FL. After P1.1b, perform a feasibility decision for at most one
  matched T1 QLoRA reference; otherwise explicitly narrow RQ2/RQ4 and keep it
  absent.
- **Model size, LoRA rank, client count, and public-pool size:** at most one
  targeted sensitivity chosen after the manuscript audit, never a Cartesian
  sweep.

## 6.1 Active method-innovation lane: P1.7a

The canonical method remains the protected comparison point, but one focused
extension is active for its frozen screen: execution-verified preference/contrastive KD.
For the same public input, the verified teacher SQL is `chosen` and a failed
pre-server global-SLM SQL is `rejected`. Uniform verified teacher-target CE
remains active on the public pool; the proposed pairwise term must add explicit
negative-sequence information rather than selecting only hard rows.

P0.10a already completed the feasibility diagnostic and found 347 global-SLM
failures on its 512-row public subset, including 122 clean executable-but-wrong
rows. Reuse those fingerprinted states. The first gate excludes client logits
and client-specific rejected outputs so the experiment is materially different
from archived FedDF. Compare against a positive-only CE control with identical
initialization, public row schedule, primary targets, updates, and seed. Promote
only for at least `+1.0` Spider EX with no execution-error increase, then require
an untuned full-3,873-row confirmation before changing the method.

The design is now frozen and implemented (`bd150c5`, pair package `d2a4d9b`).
Eligibility is all 347 failed `global_fl` outputs: 225 execution-error and 122
executable-wrong rejects. The fixed reference-free logistic loss uses
length-normalized target-sequence scores with coefficient `1.0`. The completed
P0.10d `llm_only512` checkpoint is the positive-only control. Both arms retain
512 chosen-CE microsteps and 32 optimizer updates; only P1.7a adds 347 rejected
forwards. The active command and exact resume contract live only in
`PIPELINE_NEXT.md`.

Other former candidates are inactive:

- true KID already trailed matched RKD by 1.45 EX (`p=0.072`) and cost about
  4.4 times more per step with 35% higher measured peak VRAM;
- structured-plan supervision changes the output and inference contract and is
  retained as future work;
- a new federated mechanism is deferred until FedProx and the stronger-skew
  audit identify a concrete residual drift/heterogeneity problem.

## 7. Stop rules

- Do not retune or relabel the exact failed P0.9/P0.10 implementations. A new
  mechanism that uses a materially different hypothesis remains allowed.
- Do not optimize EM at the expense of EX.
- Do not activate another KD/Federated branch alongside P1.7a unless new
  evidence invalidates this prioritization.
- Do not fill resource tables with failed, resumed, or reused-stage latency.
- Do not claim formal privacy, arbitrary cross-tokenizer KL, general non-IID
  robustness, or federated-large-model savings without corresponding evidence.

## 8. Current next actions

Follow `PAPER_TODO.md` in order. P1.4a, P1.4b, and P0.8a-E are complete. Freeze
the P1.7a matched design while continuing method prose and the architecture
figure, then run its 512-row screen as the next method experiment. Return to
P1.1b-v2 afterward, followed by the matched FedProx-LoRA baseline, one
stronger-skew screen, and seed-2 T3. Decide the federated-7B claim only after the
resource result. Do not add a model family, OOD seed sweep, or hyperparameter
Cartesian sweep by default.
