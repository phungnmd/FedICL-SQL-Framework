# FedLS-SQL — adaptive paper TODO

> Updated 2026-08-26. This is the ordered paper-work backlog. It records what
> to do and why; executable PowerShell commands belong only in
> `PIPELINE_NEXT.md`. Re-rank conditional items whenever an earlier gate changes
> the manuscript claim.

## Status legend

- `[ ]` not started;
- `[-]` active or partially complete;
- `[x]` complete;
- `GATE` requires a documented decision before a command is activated.

## Ordered work

### 1. Close the seed-1 convergence observations — active GPU, eval only

- [-] Run `P0.8a-E` from `PIPELINE_NEXT.md`.
- [ ] Validate four new full-Spider arms: independent FL T2, FedLS pre-server
  T2, FedLS post-server T2, and FedLS pre-server T3.
- [ ] Combine them with the existing seed-1 T1 ladder and final T3 endpoints.
- [ ] Add the seed-1 T1/T2/T3 trajectory to `MAIN_RESULTS.md`, registry, and
  lab log; keep mixed-lineage pre-server checkpoints diagnostic only.

**Done when:** every seed-1 convergence cell resolves to a checkpoint,
prediction file, config, metrics file, and result commit.

### 2. Close deterministic efficiency/accounting — active CPU

- [ ] Run `P1.4a` from `PIPELINE_NEXT.md`.
- [ ] Validate LoRA trainable-parameter counts, serialized adapter bytes,
  upload/broadcast bytes per round, and cumulative T3 communication.
- [ ] Push the server-side artifact-only JSON/CSV, then reconcile it locally
  with `RESULT_REGISTRY.md` and replace the corresponding `PENDING` cells in
  `MAIN_RESULTS.md`; the server does not require the paper repository.

**Done when:** no deterministic parameter or communication number is copied
from a terminal log or lacks a formula/provenance path.

### 3. Establish defensible novelty — mandatory research/writing

- [ ] Build the related-work comparison matrix across federated NL-to-SQL,
  federated PEFT, federated KD, and LLM-to-SLM collaboration.
- [ ] Include at minimum FedMKT, FedCoLLM, FedCoT, LaDa, FedGen/data-free
  server refinement, and the closest small-model NL-to-SQL transfer papers.
- [ ] Compare task, teacher location, direction of transfer, private/public
  boundary, execution verification, transmitted object, client model, and
  deployed model.
- [ ] Rewrite the novelty claim around the complete NL-to-SQL workflow:
  execution-verified public teacher SQL, private client LoRA/FedAvg, recurring
  server refinement, EX-oriented validation, and SLM-only deployment.
- [ ] Remove “novel” from the title if the complete combination cannot be
  distinguished clearly.

**Done when:** every contribution has a nearest-work comparison and no claim
implies that generic FL+KD, FedAvg-LoRA, or LLM-SLM collaboration is new.

### 4. Draft the method and core paper artifacts — mandatory CPU/writing

- [ ] Write the problem formulation and structural privacy boundary.
- [ ] Write the round algorithm: broadcast, private client LoRA CE,
  sample-weighted factor-wise FedAvg, public server transfer, rebroadcast.
- [ ] Specify teacher-target generation, quick execution filter, official EX
  filter, teacher-specific pools, target CE, and auxiliary reverse KL.
- [ ] Create the architecture/data-flow figure with private/public and
  client/server/deployment boundaries.
- [ ] Draft the main accuracy, matched ablation, convergence, Gemma
  portability, efficiency, and error-analysis tables/figures.
- [ ] State explicitly: EX is primary; privacy is structural rather than DP;
  RKL is auxiliary; no federated-7B empirical comparison exists.

### 5. Close or narrow RQ4 resource claims — mandatory decision gate

- [ ] `GATE`: choose between measured resource evidence and a narrower RQ4.
- [ ] Preferred path: reactivate `P1.1b-v2` for repeated student-1.5B versus
  teacher-7B deployment inference with fixed warm-up, median/IQR, process RSS,
  allocated/reserved VRAM, and raw GPU telemetry.
- [ ] Optional extension: controlled client-LoRA and recurring server-KD
  process-memory/throughput microbenchmarks.
- [ ] Narrow path: retain deterministic adapter communication and SLM-only
  deployment properties, but remove claims of measured client/server training
  savings or superiority to federated large-model training.

**Done when:** every RQ4 sentence is supported by a measured table or is
restated as a structural/deterministic property.

### 6. Decide the non-IID claim boundary — mandatory decision gate

- [ ] `GATE`: decide whether RQ3 remains scoped to the fixed
  `K=5, alpha=0.5` grouped-domain partition.
- [ ] Scoped path: remove “increasingly heterogeneous”, IID, quantity-skew,
  SQL-pattern-skew, and broad robustness language from title/RQs/contributions.
- [ ] Sensitivity path: construct and audit exactly one stronger-skew split
  while holding `K=5` and the source rows fixed; validate database/domain
  distributions, client sizes, entropy/JSD, and intended skew before training.
- [ ] If promoted, screen pure FL versus frozen FedLS-SQL at T1 first and
  extend to T3 only after a positive, interpretable gate.

**Done when:** either one controlled sensitivity exists or every federated
generalization claim explicitly names the fixed partition.

### 7. Add a stronger federated baseline — recommended before submission

- [ ] Design one matched FedProx-LoRA baseline using the same Qwen student,
  split, LoRA rank, local work, rounds, and evaluation protocol.
- [ ] Predeclare the proximal coefficient selection rule; do not tune on the
  Spider test set.
- [ ] Run only the minimum baseline needed for the headline comparison.
- [ ] If FedProx is not run, document the omission and avoid implying that
  FedAvg is representative of all federated optimizers.

### 8. Close final training-seed reporting — deferred GPU

- [ ] Reactivate `P0.8b` after the higher-value gaps above are closed.
- [ ] Continue the existing canonical seed-2 T1 FL/FedLS lineages through
  T2/T3; do not restart round 1.
- [ ] Report the three-seed T3 FL, FedLS, and paired-delta mean with sample SD.
- [ ] Keep question-level paired tests separate from training-seed uncertainty.

### 9. Final manuscript QA and submission packaging

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

Do not reopen ICL, FLoRA-NA, execution-guided selection, FedDF, structural
distillation, or an unmeasured federated-7B claim.

## Submission-readiness gate

The paper is ready to freeze when items 1–4 and 9 are complete, RQ4 and RQ3
have each taken one explicit supported path, the FedProx decision is recorded,
and final seed reporting is either completed or transparently limited to the
two positive T3 seeds. Three T3 seeds remain the preferred final package.
