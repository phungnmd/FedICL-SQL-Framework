# FedLS-SQL — active experiment queue

> Run from the `fedicl-sql/` repository root in PowerShell. Every executable
> command added here must follow `CONVENTION.MD` §6.1: one physical line,
> fail-fast, immutable output roots, and exact-command resume safety.

## Method freeze

The proposed method is frozen after the P0.10e decision gate:

```text
private client LoRA CE -> sample-weighted factor-wise FedAvg
                       -> verified LLM-target CE + auxiliary reverse KL
```

Execution-verified hard teacher targets are the supported portable mechanism.
Reverse KL remains auxiliary because its independent increment is not stable
across training seeds or the Gemma family.

The execution-guided selector and client-ensemble distillation branches are closed:

- P0.9b global-error selection loses `2.03` Spider EX to its matched random
  control and adds 18 execution errors.
- P0.10 failed its frozen full-pool EX and execution-validity gate after a
  positive small screen. Do not tune or continue it. Exact commands and provenance are archived at
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`.

## Active order

| Order | Task | Status / decision |
|---|---|---|
| P1.1a | Add and test fixed in-process warm-up for controlled inference benchmarking | **active engineering task; no experiment command yet** |
| P1.1b | Benchmark Qwen student 1.5B versus teacher 7B on exclusive hardware | blocked on P1.1a |
| P1.2 | Audit server-stage execution errors and `EX=1, EM=0` cases | next CPU evidence task |
| P0.8 | Final T3 pure-FL versus frozen FedLS-SQL at seeds 1/2 | deferred by current priority, not cancelled |
| P0.7t | Gemma 9B zero-shot Spider ceiling | optional context only |

No GPU experiment should start until P1.1a defines and tests warm-up semantics,
timing scope, repeated-run aggregation, and fresh-run eligibility. Ordinary
`eval_arms` timing is not official resource evidence because it measures the
first decode without a fixed warm-up.

## P1.1 acceptance contract

The benchmark implementation must:

1. warm up each loaded model in-process on deterministic non-reported inputs;
2. synchronize CUDA immediately before and after every timed region;
3. separate model loading, warm-up, generation, and SQL scoring time;
4. report fresh-run latency/throughput, peak allocated and reserved VRAM, and
   process RSS for at least three exclusive-hardware repetitions;
5. compare identical rows, decoding, precision/quantization declarations, and
   batch size where memory permits;
6. report medians plus dispersion and reject resumed/contended runs from the
   paper-facing resource table;
7. preserve raw per-repetition JSON and runtime/GPU provenance.

After the code and tests pass, add the exact single-line PowerShell commands
here before launching P1.1b. Do not reuse opportunistic P0.x timing values.

## Deferred command provenance

Completed and superseded commands are not duplicated in this active file:

- P0.0–P0.10e snapshot:
  `paper/archive/closed_method_branches/PIPELINE_THROUGH_P010E_2026-08-25.md`;
- pre-FedLS/ICL runbooks: `paper/archive/pre_fedls_2026-08/legacy_runbooks/`;
- immutable checkpoint and evaluation mappings: `paper/notes/RESULT_REGISTRY.md`.

## After a completed block

1. Commit only metrics, configs, predictions, manifests, and compact audits;
   never commit model weights or resume checkpoints.
2. Pull and validate row counts, fingerprints, paired EX/EM, and execution
   errors before changing the queue.
3. Update `RESULT_REGISTRY.md`, `paper/results/MAIN_RESULTS.md`, `LAB_LOG.md`,
   `EXPERIMENT_MATRIX.md`, and `PAPER_EVIDENCE_PLAN.md` once per decision gate.
4. Archive closed commands instead of leaving them in the active queue.
