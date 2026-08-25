# FedLS-SQL — target evidence and submission plan

> Updated 2026-08-25. This is an adaptive plan for the target outline in
> `PAPER_OUTLINE_TARGET.md`, not a promise to execute every experiment in the
> advisor's August 19 planning outline. Exact runnable commands belong only in
> `PIPELINE_NEXT.md`.

## 1. Submission objective

Build the smallest defensible Q3 evidence package for the claim:

> Execution-verified guidance from a server-side LLM improves a federated
> LoRA-adapted SLM for NL-to-SQL, while the large teacher remains outside the
> client and deployment paths and communication remains adapter-only.

Execution accuracy (EX) is the primary endpoint. EM is reported transparently
as a secondary syntactic metric; it is not an optimization target because
public BIRD teacher targets and Spider evaluation can use different SQL forms.

## 2. Frozen method and claim boundary

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
- P0.9 selection and P0.10 FedDF are closed; no new KD/Federated branch is
  active.

## 3. Evidence already sufficient

- Correct centralized-standard, independent pure-FL, and FedLS-SQL comparison
  at Qwen T3 seed 0.
- FedLS-SQL improves over pure FL on Spider and has positive deltas on all
  retained robustness/cross-dataset evaluations.
- T1 server-stage improvement has three-seed evidence.
- The matched public-supervision ladder shows that equal-row public-gold CE
  does not explain the teacher-target gain.
- Pure-FL and FedLS-SQL T1-T3 convergence trajectories exist.
- Gemma T1 provides a positive second-family endpoint and identifies hard
  teacher-target transfer as the portable mechanism.
- Adapter communication is closed at `739,110,960` bytes per round and
  `2,217,332,880` bytes through T3.
- ICL, FLoRA-NA, adaptive selection, and FedDF are closed negative branches.

## 4. Definition of done for the target paper

The experimental phase is ready to freeze when all mandatory items hold:

1. the final T3 pure-FL versus FedLS contrast has seeds 0/1/2 or the claim has
   been weakened to reflect observed instability;
2. resource tables contain deterministic counts and contention-audited process
   memory/latency measurements, with ineligible runs excluded;
3. the error analysis explains EX gains, execution failures, and representative
   transfer behavior without treating EM as the target;
4. RQ3 wording is explicitly scoped to the fixed non-IID partition, or a
   minimal validated heterogeneity screen has been completed;
5. the related-work matrix establishes novelty at the intersection of
   federated NL-to-SQL, asymmetric server/client models, execution-verified
   teacher transfer, and adapter-only communication;
6. every paper value resolves to `MAIN_RESULTS.md` and `RESULT_REGISTRY.md`.

## 5. Active priority order

### P1.1a — implement a shared-server resource benchmark

**Status:** complete. Nested implementation commits `74f70c1` and `cfa8d59`;
targeted resource/audit tests and the full 318-test suite pass.

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
- sample NVML/`nvidia-smi` state during every repetition and record visible
  foreign GPU processes, utilization, memory, clocks, and device identity;
- mark each repetition `eligible`, `contended`, `resumed`, or `failed`;
- exclude observed-contended runs from the primary latency summary;
- preserve raw per-repetition JSON and runtime provenance.

This protocol does not claim guaranteed hardware exclusivity. It claims only
that retained measurement windows had no observed foreign process on the
selected GPU. If fewer than three eligible repetitions can be collected,
latency remains a shared-server observational result and is not used for a
strong efficiency claim. Process memory and deterministic counts may still be
reported with precise labels.

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

This evidence supports a targeted discussion and future-work limitation; it
does not reopen method development before the mandatory resource and seed
gates.

### P1.1b — collect resource evidence

**Status:** active. The exact sequential GPU-0 command is in
`PIPELINE_NEXT.md`.

Collect three evidence blocks:

1. deployed Qwen 1.5B FedLS versus Qwen 7B teacher inference on identical
   rows;
2. client 1.5B LoRA training process memory and throughput on a fixed
   microbenchmark;
3. recurring server KD process memory/throughput, separated from one-time
   teacher target generation and cache construction.

Do not compare 1.5B client training with 7B inference as though it were an
empirical federated-7B baseline. The supported conclusion is that the teacher
is absent from clients/deployment and client network payload is adapter-only.

### P0.8 — final T3 training-seed reliability

**Status:** mandatory after the short resource block; commands are preserved
but not currently active.

Train only independent pure FL and frozen FedLS-SQL through T3 at seeds 1 and
2 on the existing split. Evaluate the final Spider endpoints first.

Decision gate:

- stable positive deltas: report the three-seed mean and sample SD and retain
  the headline claim;
- positive but noisy: report uncertainty and avoid expanding all OOD runs;
- a reversed seed: weaken the claim and diagnose instability before any
  optional experiment.

Question-level paired tests and training-seed uncertainty must remain separate.

### P1.3 — RQ3 scope decision

**Status:** decision gate after P0.8, not an automatic sweep.

Choose exactly one path:

1. **Scoped paper:** retain only the validated `K=5, alpha=0.5`
   grouped-domain non-IID claim; or
2. **Minimal sensitivity:** add one validated near-IID or stronger-skew split
   and compare only pure FL with FedLS-SQL on Spider.

Do not call `alpha=100` IID or `alpha=0.1` stronger heterogeneity until split
statistics confirm database/domain distribution, row-count variation, and
entropy/JSD differences. Separate quantity-skew and SQL-pattern-skew builders
are outside the default paper.

**Gate:** run the sensitivity only if the advisor/manuscript retains wording
about changing or increasing heterogeneity. Otherwise narrow RQ3 and stop.

### P1.4 — related-work and novelty audit

**Status:** mandatory CPU/writing task; may start immediately.

Build a comparison matrix covering recent:

- text-to-SQL LLM-to-SLM distillation;
- federated language-model distillation;
- federated PEFT/LoRA;
- federated NL-to-SQL.

Compare task, client/server model asymmetry, private/public data boundary,
teacher location, transferred object, execution verification, communication,
and deployed model. Revise the title if “novel” cannot be defended for the
complete combination.

### P2 — manuscript build and evidence freeze

**Status:** the skeleton may begin now; final tables wait for the mandatory
gates above.

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

## 6. Conditional reviewer baselines

These are not part of the active queue:

- **FedProx-LoRA:** add only if the target venue/advisor requires a
  heterogeneity-aware optimizer baseline or if P1.3 becomes a main claim.
- **Qwen/Gemma teacher zero-shot:** contextual accuracy/resource reference,
  not a causal method arm.
- **Federated 7B:** required only for a strong empirical claim against
  large-model FL; otherwise explicitly absent.
- **Model size, LoRA rank, client count, and public-pool size:** at most one
  targeted sensitivity chosen after the manuscript audit, never a Cartesian
  sweep.

## 7. Stop rules

- Do not reopen P0.9 or P0.10.
- Do not optimize EM at the expense of EX.
- Do not add a new KD loss without an EX-specific failure hypothesis from
  P1.2 and a preregistered matched control.
- Do not fill resource tables with resumed, reused-stage, or observed-contended
  latency.
- Do not claim formal privacy, arbitrary cross-tokenizer KL, general non-IID
  robustness, or federated-large-model savings without corresponding evidence.

## 8. Current next actions

1. Run the single P1.1b PowerShell block and review repetition eligibility.
2. If either role has fewer than three eligible repetitions, retain the result
   as observational and schedule a fresh-root retry only for that role.
3. After P1.1b closes, reactivate P0.8 seeds 1/2.
4. Decide scoped RQ3 versus one minimal heterogeneity sensitivity.
5. Build the manuscript and stop experiments unless the reviewer audit exposes
   a named evidence gap.
