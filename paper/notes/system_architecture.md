# FedLS-SQL — protocol-v2 architecture

> Reset on 2026-09-03 after confirming that protocol v1 retained BIRD
> `evidence` in CSV but omitted it from every teacher, student, training, and
> evaluation prompt. The full v1 record is archived under
> `paper/archive/protocol_v1_no_bird_evidence/`.

## Research target

FedLS-SQL studies whether server-side LLM-to-SLM collaboration can improve an
SLM trained across private federated Text-to-SQL clients while retaining SLM
deployment and adapter-only communication.

The final KD loss, target construction, aggregation rule, and round schedule
are not frozen. Protocol v2 first establishes comparable dataset-correct
baselines, reruns the previous method as a reference, then permits targeted
method improvements supported by the observed failure modes.

## Dataset contract

Every example contains question, SQL, database identity/path, optional
evidence, dataset/release identity, source-row identity, and dialect. Every run
declares one of these profiles:

| Profile | Prompt policy | Paper role |
|---|---|---|
| `spider` | schema + question; no evidence | Spider baseline/evaluation |
| `bird_with_evidence` | schema + evidence + question | primary BIRD baseline/evaluation |
| `bird_no_evidence` | schema + question | disclosed knowledge ablation |
| `legacy` | historical Spider-shaped prompt | v1 compatibility only |

BIRD's official formulation conditions generation on external evidence and
reports both with-knowledge and without-knowledge settings. Therefore v1 is
retained as a no-knowledge historical ablation, but it is not canonical
evidence for the new with-evidence setup. The current BIRD release choice is a
gate: prefer the official filtered training set and identify cleaned/original
dev explicitly rather than combining releases silently.

## Role-independent pipeline

Configuration separates:

1. private/client dataset and profile;
2. public/server dataset and profile;
3. evaluation dataset and profile.

This supports both directions without dataset-specific branches:

```text
BIRD public(with evidence) -> Spider private -> Spider evaluation
Spider public              -> BIRD private(with evidence) -> BIRD evaluation
```

For BIRD-private training, evidence is available only inside the client prompt.
For BIRD-public transfer, teacher and student server stages use the same
declared evidence policy. A later teacher-privileged-evidence experiment would
be a distinct learning-with-privileged-information method, not the default.

## Reference method, not frozen method

The first v2 rerun mirrors the previous workflow under corrected prompts:

```text
private client LoRA CE
  -> sample-weighted factor-wise FedAvg
  -> execution-verified public teacher-target CE
  -> optional reverse KL
  -> SLM deployment
```

Required matched controls are base SLM, centralized SFT, pure FL, public-gold
CE, teacher-target CE, and target-CE plus RKL. EX is primary. RKL is not part of
the final claimed method unless it adds reproducible EX under protocol v2.

After the rerun, the method-improvement queue is adaptive. Candidate changes
must target a measured failure, use a matched compute/data control, and pass a
predeclared EX gate before full runs. KD and federated mechanisms may both
change; failed v1 branches are not automatically reopened.

## Evaluation and lineage

- Split train/validation by `db_id`; database overlap is forbidden.
- Spider and BIRD use dataset-specific evaluation profiles.
- EX is primary; EM remains a surface-form diagnostic.
- Dataset release, role, profile, evidence mode, schema mode, evaluator, and
  source hashes enter setup/checkpoint/evaluation fingerprints.
- Every v2 output lives under `artifacts/protocol_v2/`; v1 roots are immutable
  even after quarantine.
- Full teacher generation precedes execution filtering. Selection remains
  teacher-specific and preserves source-row identity and prompt provenance.

## Claims retained independently of the reset

The BIRD prompt defect does not invalidate Spider-only centralized/pure-FL/
FedProx comparisons, adapter communication accounting, Secure Sum compatibility,
or the controlled Spider deployment benchmark. It does invalidate canonical
status for FedLS/KD lineages trained from no-evidence BIRD pools and BIRD evals
reported without the no-knowledge label.

## Implementation

Protocol profiles, dataset-neutral splits, audits, and versioned BIRD ingestion
were added in nested commits `fa29734`, `2b40b73`, `dc1d24d`, and `fc0925b`.
Nested commit `346342c` adds immutable v2 materialization, dataset-neutral
semantic DB grouping, and deterministic centralized result identities. This
allows BIRD-original with-evidence centralized and FL checkpoints to train
before evaluator integration; they remain unevaluated compatibility artifacts
until the official BIRD evaluator contract is frozen.
Nested commit `11ab685` additionally binds each generated client shard, split,
and statistics file by hash and refuses drift on an exact rerun.
Nested commit `9d777db` closes the baseline execution path: evaluation now
dispatches `spider_result_eq_v1` versus `bird_official_set_v1` from the dataset
profile, scorer identity enters resume fingerprints, and one phase-separated
PowerShell runner owns quarantine, BIRD-original preparation, baseline
training/evaluation, and allowlisted publication. Nested commit `40255f4` added
the former two-lane scheduler; `e1f3127` supersedes that orchestration and runs
centralized training, FL training, centralized evaluation, and FL evaluation
sequentially on physical GPU 0. Scientific flags and artifact roots are
unchanged.
The executable contract is documented in
`fedicl-sql/docs/PROTOCOL_V2.md`.

Primary references: [BIRD paper](https://arxiv.org/abs/2305.03111),
[official BIRD release page](https://github.com/bird-bench/bird-bench.github.io/blob/main/index.html),
and [official mini-dev fine-tuning pipeline](https://github.com/bird-bench/mini_dev/tree/main/finetuning).
