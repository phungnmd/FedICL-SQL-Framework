# FedLS-SQL — protocol-v2 architecture

> Reset on 2026-09-03 after confirming that protocol v1 retained BIRD
> `evidence` in CSV but omitted it from every teacher, student, training, and
> evaluation prompt. The full v1 record is archived under
> `paper/archive/protocol_v1_no_bird_evidence/`.

## Research target

Current queue update (2026-09-16): prioritize P2.4c, matched two-epoch
full-public CE/Hinton, with evaluation before and after terminal A. This tests
under-training and retention separately. Terminal SeqKD below is deferred;
the one-epoch result does not establish CE/Hinton equivalence.

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

The implemented v2 reference currently mirrors the previous workflow under
corrected prompts and **ends at the public KD checkpoint**:

```text
private client LoRA CE
  -> sample-weighted factor-wise FedAvg
  -> one public-server update:
       (a) execution-verified teacher-target CE (SeqKD), or
       (b) full public-gold CE + Hinton forward KL on gold prefixes
  -> SLM deployment
```

Let `A` denote one private client-update plus FedAvg stage and `K` one public
server KD stage. The current T1 endpoint is therefore `A -> K`; recurrent
rounds follow `(A -> K)^T` and also end at `K`. This is an implementation fact,
not a frozen architectural choice.

The current seed-0 endpoint candidate adds one private consolidation stage
after KD and deploys the resulting aggregate:

```text
private clients/FedAvg (A)
  -> public KD (K)
  -> private client re-anchoring/FedAvg (A)
  -> SLM deployment
```

Its T1 form is `A -> K -> A`. It tests whether the public BIRD KD gain can be
retained while the final Spider-private update restores the deployment-domain
input distribution. Because it adds private training and communication, it
must be compared with the matched no-KD control `A -> A`, not only with `A`
and `A -> K`. Seed-0 P2.3 passes this gate: `A>K[fkl]>A` beats `A>A` on all
five evaluations. P2.4a then found no reliable advantage over the same chain
with public-gold CE, so the benefit is not currently attributable to Hinton
soft logits.

The next causal screen keeps one local epoch in every private stage and tests
the second standard teacher channel:

```text
matched selected gold: A -> K[ce, 5319 gold rows] -> A
sequence KD:          A -> K[seq, same 5319 rows] -> A
```

The two parents are already published and differ in target SQL, not selected
row identities. Their identical terminal `A` stages test whether a
teacher-generated sequence signal survives private re-anchoring. Repeated KD
depth and recurrence are deferred until either SeqKD or another KD objective
passes a matched terminal causal gate. Multi-local-epoch `A[e2/e3]` remains
deprioritized because the non-IID clients make local drift a more plausible
effect than useful consolidation.

Required matched controls are base SLM, centralized SFT, pure FL, public-gold
CE, teacher-target CE (SeqKD), and full-public-gold CE plus temperature-scaled
`KL(p_teacher || p_student)` under teacher forcing on gold SQL. SeqKD is the
sequence-level baseline; Hinton FKL is the token-level soft-logit baseline.
They are separate arms, not a required hybrid. EX is primary. Neither becomes
part of the final claimed method without reproducible protocol-v2 gain.
Historical protocol-v1 reverse KL and KID remain archived. They do not count as
protocol-v2 evidence. A fresh, provenance-isolated protocol-v2 KID lane is now
the bounded method candidate after autoregressive GKD was closed for excessive
compute cost. It uses one-pass student rewriting plus reverse KL and must pass
the same five-set EX gate before entering the proposed method. MiniLLM and a
clean-RKL isolation arm remain conditional follow-ups.

After the rerun, the method-improvement queue is adaptive. The first gate was
the terminal checkpoint comparison `A`, `A -> K`, `A -> A`, and
`A -> K -> A`; it passed at seed 0. Candidate changes
must target a measured failure, use a matched compute/data control, and pass a
predeclared EX gate before full runs. KD and federated mechanisms may both
change; failed v1 branches are not automatically reopened.

## Current protocol-v2 evidence gate

Both public-teacher pipelines are frozen. BIRD→Spider selects 5,319/9,428
execution-matched targets; Spider→BIRD selects 7,251/8,659. Qwen-Coder-7B
zero-shot EX is 47.07 on evidence-aware BIRD dev and 76.69 on Spider.

For BIRD-public→Spider-private T1, the original matched batch-size-8 ladder gave
56.96/56.09/57.64 EX for Pure FL/matched-gold CE/SeqKD. The later shared
batch-size-16 headline evaluation gives 57.35 Pure FL, 57.93 SeqKD, and 58.32
Hinton FKL on Spider. Hinton reaches 36.70 on BIRD versus 14.80 for Pure FL,
but falls from 54.92 to 42.72 on Realistic and from 49.32 to 44.58 on SYN; DK
is effectively flat (45.23 to 45.42). Thus the public update transfers strongly
to BIRD but damages robustness to Spider distribution shifts.

This observation motivated terminal private consolidation. P2.3 now shows
that `A>K[fkl]>A` reaches 66.63/57.09/55.32/50.65/31.03 on
Spider/Realistic/SYN/DK/BIRD, versus 62.57/55.31/52.22/47.10/16.49 for
matched `A>A`. It does not yet prove that soft teacher logits solve retention.
P2.4a resolves that question negatively for the current Hinton recipe.
The completed no-logit full-BIRD-public gold CE
control scores 55.03/47.05/43.91/40.93/32.14 on Spider/Realistic/SYN/DK/BIRD;
Hinton is +3.29/−4.33/+0.67/+4.49/+4.56 points relative to it. This supports
the combined Hinton recipe on four datasets, but neither public-terminal
objective preserves FL robustness. Exact paired prompts match across arms.
Earlier batch-size-8 and headline batch-size-16 predictions differ in 86/58
rows for FL/SeqKD; preserve those evaluation lineages separately. The sole
cause of that rerun drift has not been established.

Reverse BIRD-private/Spider-public FL/gold/SeqKD reaches 22.88/20.73/24.45 EX.
The reference and terminal result commits are published and audited
(`5e4f005`, `1b2c46a`, `ec5b5e1`, `2a6e04c`); see the P2.2 and P2.3 reviews.
P2.4a (`ccb3e91`) gives `A>K[ce]>A` EX of
66.54/57.28/54.45/51.21/29.53. Relative Hinton deltas are
+0.09/−0.19/+0.87/−0.56/+1.50 points and none is paired-significant. The next
gate is terminal selected-row SeqKD versus matched gold; a controlled
depth/recurrent screen opens only for a teacher channel that passes. The exact
mechanism of the robustness loss remains a hypothesis, not a proven prompt
defect.

## Evaluation and lineage

P2.1 BIRD-private results at `f99febd` are diagnostic only. P2.1q (`e9bde43`)
accepted the raw-SQL scorer but found 974 truncated train prompts and complete
evidence loss in 754 rows. Canonical BIRD training now uses a measured
`max_len=7168`, fail-closed overflow handling, gradient checkpointing and new
immutable roots (`d21f777`). Evidence is required input; its causal benefit is
not an active ablation. See `BIRD_BASELINE_AUDIT.md`.
The primary method run remains Spider private FL → BIRD public KD → Spider eval;
the existing BIRD-private baselines support a later reverse-direction comparison.

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
FedProx comparisons, pure-FL adapter communication accounting, Secure Sum
compatibility, or the standalone teacher resource measurement. It does
invalidate canonical status for FedLS/KD lineages trained from no-evidence BIRD
pools and BIRD evals reported without the no-knowledge label. The final
student-versus-teacher deployment comparison must be rerun with the selected v2
student adapter.

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
dispatches Spider EX versus BIRD set-of-row-tuples EX from the dataset profile.
Commit `2178d5a` completes the official BIRD timing contract with one 30-second
budget for the prediction/gold pair; scorer identity
`bird_official_set_pair_timeout30_v2` enters resume fingerprints. One phase-separated
PowerShell runner owns quarantine, BIRD-original preparation, baseline
training/evaluation, and allowlisted publication. Nested commit `40255f4` added
the former two-lane scheduler; `e1f3127` supersedes that orchestration and runs
centralized training, FL training, centralized evaluation, and FL evaluation
sequentially on physical GPU 0. Scientific flags and artifact roots are
unchanged. Commit `8a17542` makes the validation phase self-provision its
locked test dependency on compute-only servers; it does not affect experiments.
Commit `767301d` fixes the runner's Python subprocess encoding to UTF-8 on
Windows; dataset and experiment semantics remain unchanged.
Nested `e9bde43` publishes the completed retention/rescore audit. Nested
`d21f777` fingerprints truncation policy and gradient checkpointing, introduces
fail-closed assembly, selects the eight longest audited prompts for a GPU memory
gate, and moves corrected runs to `bird_original_ctx7168` roots.
Nested `8caa610` freezes a metadata-complete Spider protocol-v2 copy and the
same semantic K5 split, then replaces the hard-coded two-GPU closure scheduler
with two independent direction runners. `spider_private` binds BIRD-public
with-evidence transfer to Spider clients/evaluation; `bird_private` binds
Spider-public transfer to BIRD clients/evaluation with evidence. Neither runner
sets a physical GPU: the calling PowerShell process exposes exactly one device.
Nested `c13fc9f` hardens both lanes without changing scientific result
identity: SQL execution is read-only, interrupted teacher JSONL tails recover
atomically, matched-gold provenance is dataset-neutral, and dataset/split
contracts fail closed before model loading. Nested `8c72764` pins that reviewed
base for server execution. Existing accepted results remain valid because the
evaluator algorithms and their recorded identities did not change.
Nested `810d8c4` adds composable stage chains (`run.py stage private|public`)
because the round loop cannot append a private stage after KD. Each stage
warm-starts from a committed parent result row, derives its chain (`A`,
`K[ce]`, `K[fkl]`) from that row, binds the parent adapter hashes and recipe in
an immutable `stage.json`, and writes one `federated_stage` result row. Round
setup IDs are unchanged. This is the execution path for `A -> A` and
`A -> K -> A`.
Review fixes through nested `014b118` bind full parent metrics/config hashes,
require both files committed and unchanged, and reject historical reverse-KL
or unknown objectives rather than infer Hinton from `fedkd`. Version-2 stage
contracts are written atomically; incomplete result publication can be
repaired without retraining. Existing round recipes/results remain unchanged;
pre-hardening version-1 stage roots are preserved but not silently migrated.
Nested `362aced` gives auto-generated eval results fingerprint/UUID-based
publication IDs with exclusive directory creation. Independent GPU lanes no
longer serialize evaluation; their per-lane resume manifests remain distinct.
This changes result naming only, not scoring or historical result validity.
The executable contract is documented in
`fedicl-sql/docs/PROTOCOL_V2.md`.

Primary references: [BIRD paper](https://arxiv.org/abs/2305.03111),
[official BIRD release page](https://github.com/bird-bench/bird-bench.github.io/blob/main/index.html),
and [official mini-dev fine-tuning pipeline](https://github.com/bird-bench/mini_dev/tree/main/finetuning).
