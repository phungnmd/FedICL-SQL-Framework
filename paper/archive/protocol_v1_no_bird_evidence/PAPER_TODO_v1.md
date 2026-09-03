# ARCHIVED — protocol-v1 adaptive paper TODO (BIRD evidence omitted)

> Updated 2026-09-01. This is the ordered paper-work backlog. It records what
> to do and why; executable PowerShell commands belong only in
> `PIPELINE_NEXT.md`. Re-rank conditional items whenever an earlier gate changes
> the manuscript claim.

Quick operator view, including the GPU-ready queue:
`PAPER_NEXT_TASKS.md`.

## Status legend

- `[ ]` not started;
- `[-]` active or partially complete;
- `[x]` complete;
- `GATE` requires a documented decision before a command is activated.

## Immediate completion plan

Scientific decisions are ordered, while independent GPU-ready work may run
opportunistically so scarce GPU time is not wasted:

1. **P1.8 Secure Sum compatibility — complete:** implementation, tests, one
   real canonical replay, numerical equivalence, and overhead evidence are
   closed. It is optional and separate from accuracy lineages.
2. **P1.5 FedProx-LoRA — complete negative:** fixed `mu=0.01` loses to pure FL
   at T1/T2/T3; no OOD, tuning, or FedLS-FedProx extension remains.
3. **P1.3 stronger semantic-domain skew — complete positive:** on the fixed-row
   `alpha=0.1, K=5` setting, FedLS improves over FL by `+4.06` EX at T1 and
   `+4.64` at T3; the final paired result is significant (`p=0.000367`).
4. **P1.9 RKL value-at-T3 — GPU-ready:** run one recurring verified-target
   CE-only T1→T3 control from the exact stronger-skew shared T1 aggregate,
   then compare its final endpoint with the existing CE+RKL T3 model. Use this
   result to freeze whether RKL is a supported component or an auxiliary detail.
5. **P0.8b seed 2 — legacy-setup gated:** continue the existing plaintext T1
   lineages to T3 after backward-compatible setup handling is tested; never
   restart completed round 1.
6. **P2.2 paper artifacts — parallel CPU lane:** assemble all tables/figures
   whose values are already closed, retaining explicit placeholders only for
   P1.9/P0.8b.
7. **P2.3 reviewer QA/freeze — final:** resolve every value to provenance,
   audit claims and limitations, then freeze code/result SHAs.

Federated 7B and additional model/rank/client/public-pool sweeps are excluded
by default. A new method branch may start only if P1.5 or P1.3 exposes a
specific residual failure that the canonical method does not address.

## Ordered work

### 0. Validate optional Secure Sum compatibility — complete

- [x] Design P1.8 as a protocol layer over the existing sample-weighted LoRA
  FedAvg objective; do not add DP noise, clipping, robust aggregation, or a new
  client weighting rule.
- [x] Freeze numeric encoding, pairwise masking, minimum completion threshold,
  dropout-recovery simulation, and the local-simulator claim boundary before
  adding a production command.
- [x] Add equivalence, threshold/dropout, incompatible-input, and server
  transcript/artifact-boundary tests.
- [x] Replay one canonical five-client, 18,464,768-parameter aggregation and
  record numerical diagnostics plus overhead: maximum error `3.7253e-9`,
  cosine `0.9999999999999983`, `7.1147 s`, and about `49.93%` communication
  expansion.
- [x] Keep accuracy lineages on explicit plaintext weighted FedAvg. Do not
  relabel or replay every historical result because Secure Sum does not change
  the scientific objective.
- [x] Restore plaintext as the normal accuracy-experiment default. Require
  explicit `--aggregation-protocol secure_sum` only for a dedicated audit.
- [x] Scope the claim to compatibility with a local pairwise-mask simulator;
  do not claim end-to-end MPC deployment, DP, final-model leakage protection,
  or poisoning defense.

**Done:** P1.8 supports a separate compatibility/overhead row. It is not a gate
for FedProx, stronger-skew, seed reliability, or historical EX.

### 1. Close the seed-1 convergence observations — complete

- [x] Run `P0.8a-E` from `PIPELINE_NEXT.md`.
- [x] Validate four new full-Spider arms: independent FL T2, FedLS pre-server
  T2, FedLS post-server T2, and FedLS pre-server T3.
- [x] Combine them with the existing seed-1 T1 ladder and final T3 endpoints.
- [x] Add the seed-1 T1/T2/T3 trajectory to `MAIN_RESULTS.md`, registry, and
  lab log; keep mixed-lineage pre-server checkpoints diagnostic only.

**Done when:** every seed-1 convergence cell resolves to a checkpoint,
prediction file, config, metrics file, and result commit.

### 2. Close deterministic efficiency/accounting — complete

- [x] Run `P1.4a` from `PIPELINE_NEXT.md`.
- [x] Validate LoRA trainable-parameter counts, serialized adapter bytes,
  upload/broadcast bytes per round, and cumulative T3 communication.
- [x] Push the server-side artifact-only JSON/CSV, then reconcile it locally
  with `RESULT_REGISTRY.md` and replace the corresponding `PENDING` cells in
  `MAIN_RESULTS.md`; the server does not require the paper repository.

**Done when:** no deterministic parameter or communication number is copied
from a terminal log or lacks a formula/provenance path.

### 3. Establish defensible novelty — complete

- [x] Build the related-work comparison matrix across federated NL-to-SQL,
  federated PEFT, federated KD, and LLM-to-SLM collaboration.
- [x] Include at minimum FedMKT, FedCoLLM, FedCoT, LaDa, FedGen/data-free
  server refinement, and the closest small-model NL-to-SQL transfer papers.
- [x] Compare task, teacher location, direction of transfer, private/public
  boundary, execution verification, transmitted object, client model, and
  deployed model.
- [x] Rewrite the novelty claim around the complete NL-to-SQL workflow:
  execution-verified public teacher SQL, private client LoRA/FedAvg, recurring
  server refinement, EX-oriented validation, and SLM-only deployment.
- [x] Remove “novel” from the title because FedCoLLM covers the closest generic
  loop and Struct-SQL already covers execution-correct teacher SQL; use the
  narrower title and claim in `RELATED_WORK_NOVELTY_MATRIX.md`.

**Done when:** every contribution has a nearest-work comparison and no claim
implies that generic FL+KD, FedAvg-LoRA, or LLM-SLM collaboration is new.

### 4. Draft the method and core paper artifacts — active parallel CPU lane

- [x] Create the evidence-mapped manuscript skeleton in
  `MANUSCRIPT_SKELETON.md`.
- [x] Write the problem formulation and structural privacy boundary in
  `paper/drafts/FEDLS_SQL_METHOD.md`.
- [x] Write the round algorithm: broadcast, private client LoRA CE,
  sample-weighted factor-wise FedAvg, public server transfer, rebroadcast.
- [x] Specify teacher-target generation, quick execution filter, official EX
  filter, teacher-specific pools, target CE, and auxiliary reverse KL.
- [x] Create and visually verify the vector architecture/data-flow figure with
  private/public and client/server/deployment boundaries at
  `paper/drafts/figures/fedls_sql_architecture.svg`.
- [-] Draft the main accuracy, matched ablation, convergence, Gemma
  portability, efficiency, and error-analysis tables/figures.
- [x] State explicitly: EX is primary; privacy is structural rather than DP;
  RKL is auxiliary; no federated-7B empirical comparison exists.

### 4A. Test execution-verified preference/contrastive KD — closed negative

- [x] Reuse the completed P0.10a feasibility audit; do not rebuild its public
  pair inventory. It found 347 global-SLM failures on 512 public rows, including
  122 clean executable-but-wrong rows.
- [x] Freeze a reference-free pairwise objective that retains uniform verified
  teacher-target CE and ranks `chosen=y_T` above `rejected=y_global` using
  length-normalized sequence scores.
- [x] Use only rejected outputs from the pre-server global SLM in the first
  gate. Do not use client logits or client-specific rejected sequences, which
  would reopen the failed P0.10 FedDF/client-over-alignment path.
- [x] Define one matched positive-only CE control with identical initialization,
  public row schedule, optimizer steps, seed, and primary teacher targets;
  disclose any extra pair-scoring compute separately.
- [x] Freeze pair eligibility, the preference coefficient, fixed 512-row screen
  budget, EX/execution-error promotion metric, compute estimate, and stop rule
  before implementation or a PowerShell command.
- [x] Run the matched screen: `global_pref512` reached 54.93 EX with 252
  execution errors versus 56.87 and 230 for `positive_ce512`, failing both
  fixed gates.
- [x] Apply the stop rule: do not run full 3,873, retune the coefficient, or
  filter the pair subset; archive the implementation and compact negative result.
- [x] Retain the canonical method unchanged. Recovery tag:
  `archive/p017-preference-kd-implementation`; cleanup commit: `7de7840`;
  exact result archive commit: `74f0a43`.

KID is no longer an active candidate: the matched legacy experiment was 1.45
EX below RKD (`p=0.072`), while measured cost was about 4.4 times slower and
35% higher in peak VRAM. Structured-plan supervision is future work because it
changes the output/inference contract and the current complex-query audit does
not justify that scope. A new federated mechanism is deferred until FedProx and
the stronger-skew audit demonstrate a specific unresolved drift problem.

### 5. Close RQ4 deployment-resource evidence — complete for scoped inference

- [x] Select the measured deployment path for the advisor-aligned question;
  retain narrowing as the fallback if the controlled collection cannot close.
- [x] Run `P1.1b-v2` for repeated student-1.5B versus
  teacher-7B deployment inference with fixed warm-up, median/IQR, process RSS,
  allocated/reserved VRAM, and raw GPU telemetry.
- [x] Review P1.1b: retain the measured deployment-inference comparison and
  deterministic adapter communication. Do not add client/server training
  microbenchmarks by default because the manuscript makes no measured
  training-resource comparison.
- [x] Narrow the claim explicitly: no measured client/server training savings,
  energy/concurrency result, full-test timing, or superiority to federated
  large-model training.

**Done when:** every RQ4 sentence is supported by a measured table or is
restated as a structural/deterministic property.

### 6. Add a stronger federated baseline — complete negative

- [x] Design one matched FedProx-LoRA baseline using the same Qwen student,
  split, LoRA rank, local work, rounds, and evaluation protocol.
- [x] Predeclare `mu=0.01` before any FedProx Spider evaluation; do not sweep or
  select it on the test set.
- [x] Implement the client-only proximal loss, round-start reference,
  setup/client/trainer fingerprints, metrics, and server-stage isolation;
  implementation `897fb66`, 334 tests and lint pass.
- [x] Add the P1.5a PowerShell single-line, fail-fast, exact-resume smoke command
  after design/config verification.
- [x] Preserve the completed two-step P1.5a root as a diagnostic: training and
  FedAvg passed, but warm-up delayed parameter drift until after its last
  forward, so its observed proximal losses were zero.
- [x] Run and review the fresh three-step P1.5a-R root: all five clients have
  positive proximal loss; plaintext FedAvg completed with `noop_suspect=False`.
- [x] Run the minimum P1.5b T3 training lineage: all 15 client stages are fresh
  with positive proximal loss and all three plaintext aggregates are valid.
- [x] Pull P1.5c and perform paired EX and
  execution-error comparisons against registered centralized, pure-FL, and
  FedLS checkpoints without retuning `mu`.
- [x] Apply the primary stop rule: no OOD evaluation, coefficient sweep, or
  FedLS-FedProx combined screen after T3 failed to improve on pure FL.
- [x] Run P1.5d eval-only on the immutable T1/T2 adapters and compare each to
  registered pure FL at the same round. Treat it only as a post-hoc trajectory
  diagnostic; do not select a test checkpoint or revise the T3 decision.
- [x] Close the interaction hypothesis: FedProx is lower by `0.87`, `2.22`,
  and `1.55` EX at T1/T2/T3, so no FedLS-FedProx screen is promoted.
- [x] Close P1.5: FedProx has 22 paired corrections and 38 regressions versus
  pure FL (`-1.55` EX, `p=0.0519`) and 194 versus 193 execution errors.
- [x] Include the matched FedProx T3 result as a negative optimizer baseline;
  do not present FedAvg as representative of all federated optimizers.

**Done when:** the headline table includes one matched stronger federated
optimizer or the omission and claim boundary are explicit.

### 7. Test one controlled non-IID sensitivity — training active

- [x] Select the minimal-sensitivity path rather than the full IID/quantity/
  SQL-pattern Cartesian suite proposed in the August outline.
- [x] Construct exactly one stronger-skew split while holding `K=5` and the
  source rows fixed.
- [x] Validate database/domain distributions, client sizes, entropy/JSD, and
  the intended axis: same 8,659 rows; domain JSD `0.527→0.805`, entropy
  `3.029→2.183`; size ratio decreases `3.02x→1.88x`.
- [ ] Predeclare and run a pure-FL versus frozen-FedLS T1 Spider screen.
- [x] Freeze the promotion gate before evaluation: at least `+2.0` EX, more
  paired corrections than regressions, and no added execution errors.
- [ ] Extend to T3 only if the T1 result passes a positive, interpretable gate.
- [ ] If split validation or the screen fails, stop and scope RQ3 explicitly to
  the original fixed partition.

**Done when:** one controlled sensitivity supports the claim or the manuscript
falls back transparently to the fixed-partition scope.

### 8. Close final training-seed reporting — legacy-setup gated

- [ ] Add and test backward compatibility for pre-P1.8 plaintext `setup.json`,
  then reactivate the preserved continuation; it remains scientifically
  independent of the P1.5/P1.3 outcomes.
- [ ] Continue the existing canonical seed-2 T1 FL/FedLS lineages through
  T2/T3; do not restart round 1.
- [ ] Report the three-seed T3 FL, FedLS, and paired-delta mean with sample SD.
- [ ] Keep question-level paired tests separate from training-seed uncertainty.

### 9. Decide the empirical large-model-FL claim — conditional gate

- [x] Review P1.1b-v2: exclude a federated-7B training reference by default.
- [ ] If retaining “lower client requirements than large-model FL”, perform a
  feasibility audit for at most one matched T1 7B QLoRA reference and define
  its accuracy/resource/communication contract before adding a command.
- [x] State that no federated-7B baseline was run and restrict RQ4 to
  adapter communication plus measured SLM-versus-teacher deployment inference.

**Done when:** no sentence equates a 1.5B/7B inference comparison with
federated-7B training evidence.

### 10. Final manuscript QA and submission packaging

- [ ] Resolve every paper value through `MAIN_RESULTS.md` and
  `RESULT_REGISTRY.md`.
- [ ] Verify all tables use EX as the primary endpoint and label EM as a
  secondary SQL-form diagnostic.
- [ ] Audit limitations: public-pool dependence, one primary partition,
  shared-server resource protocol, no formal privacy, no federated 7B, and
  unstable standalone RKL increment.
- [ ] Perform a reviewer-style claim/evidence audit against the selected venue.
- [ ] Freeze code/result SHAs and generate the final artifact manifest.

## Optional backlog — do not activate by default

- Qwen teacher zero-shot accuracy as contextual ceiling;
- a small fixed-rule schema-linking qualitative audit;
- teacher/student size, LoRA-rank, client-count, or public-pool sensitivity;
- additional OOD seed replication.

Do not retune the exact closed ICL, FLoRA-NA, P0.9 selection, P0.10 FedDF, or
P1.7a preference-KD implementations, and do not make an unmeasured federated-7B
claim. No method-innovation branch is active; a new proposal requires a new
documented failure hypothesis and matched gate.

## Submission-readiness gate

The paper is ready to freeze when items 1–5 and 10 are complete, the
FedProx and stronger-skew gates are recorded, the
federated-7B wording is resolved, and final seed reporting is either completed
or transparently limited to the two positive T3 seeds. Three T3 seeds remain
the preferred final package.
