# FedLS-SQL — target paper outline

> Target outline for the evidence-backed Q3 submission. This document replaces
> the August 19 outline as the active manuscript structure; the PDF remains the
> advisor-provided planning source. The outline follows validated claims rather
> than treating every suggested sweep as mandatory.

## Paper title

**FedLS-SQL: A Novel Federated Large-Small Language Models Framework for
Natural Language to SQL**

This retains the advisor-provided working title. Keep “novel” in the submitted
title only after the related-work audit confirms that the complete system
setting and transfer loop are not already covered.

## Target claim

Server-side LLM guidance on public, execution-verified SQL can improve a
federated LoRA-adapted SLM for NL-to-SQL. The large teacher remains outside the
client and deployment paths, while client communication remains adapter-only.

Execution accuracy (EX) is the primary task endpoint. Exact match (EM) is a
secondary syntactic metric: BIRD-derived teacher supervision and Spider
evaluation can express equivalent SQL in different forms, so low EM is not by
itself a method failure or an optimization target.

## Research questions

1. **RQ1 — Accuracy:** Does FedLS-SQL improve execution accuracy over pure
   federated SLM training and remain competitive with centralized SLM training?
2. **RQ2 — Transfer mechanism:** Do execution-verified teacher targets provide
   value beyond an equal-row public-gold training pass, and which part of the
   server treatment transfers across model families?
3. **RQ3 — Federated behavior:** How does repeated server-side teacher guidance
   affect convergence and generalization in the fixed domain-skewed non-IID
   setting?
4. **RQ4 — Efficiency:** What accuracy, communication, memory, and inference
   trade-offs result from keeping the large teacher off clients and out of
   deployment inference?

Do not strengthen RQ3 to broad heterogeneity robustness unless the controlled
heterogeneity screen is completed. Do not compare empirically with federated
7B training unless such a baseline is actually run.

## Contributions

1. A federated NL-to-SQL architecture combining private client-side SLM LoRA
   adaptation, factor-wise FedAvg, and server-side large-to-small transfer on
   public data.
2. An execution-verified public teacher-target pipeline that transfers teacher
   SQL to the global SLM without exposing client rows or placing the LLM on
   clients.
3. Causal evidence separating additional public supervision, teacher-generated
   hard targets, and auxiliary reverse KL, plus a same-family replication with
   a second model family.
4. An evaluation of execution accuracy, convergence, cross-dataset
   generalization, and adapter communication. Process memory and deployment
   inference cost remain part of this contribution only after the repeated
   shared-server resource block is completed.

FedAvg-LoRA and reverse KL are not claimed as independently novel algorithms.
The portable mechanism supported across Qwen and Gemma is execution-verified
hard teacher-target transfer; reverse KL is an auxiliary Qwen component.

## 1. Introduction

- NL-to-SQL utility and the importance of execution correctness.
- Limitations of centralized LLM deployment and centralized private data.
- Accuracy limitations of lightweight federated NL-to-SQL.
- Gap at the intersection of federated NL-to-SQL and server-side LLM-to-SLM
  collaboration.
- FedLS-SQL overview, research questions, contributions, and claim limits.

## 2. Related work

### 2.1 NL-to-SQL and execution-based evaluation

### 2.2 Federated learning and PEFT for language models

### 2.3 LLM-to-SLM knowledge distillation for NL-to-SQL

### 2.4 Federated distillation and public-proxy server refinement

End with a comparison matrix locating FedLS-SQL by task, private/public data
boundary, model asymmetry, transferred object, execution verification, client
payload, and deployed model. Novelty must be assigned to the complete setting
and workflow, not to KD, LoRA, or FedAvg in isolation.

The mandatory nearest-work set includes FedMKT, FedCoLLM, FedCoT, LaDa,
FedGen/data-free server refinement, federated PEFT, and the closest
small-model NL-to-SQL transfer systems. Generic “first federated LLM-SLM
framework” wording is prohibited; the defensible candidate novelty is the
execution-verified NL-to-SQL workflow and its private/public/deployment
boundary.

## 3. FedLS-SQL

### 3.1 Problem formulation and structural data-isolation boundary

- Client-private schemas and NL-SQL pairs.
- Public server pool.
- Shared SLM architecture across clients and larger frozen server teacher.
- No formal DP, secure aggregation, or model-update leakage guarantee.

### 3.2 Overall architecture and round lifecycle

- Broadcast global SLM adapter.
- Private local LoRA training.
- Sample-weighted factor-wise FedAvg.
- Public server transfer.
- Broadcast the refined adapter.

### 3.3 Execution-verified teacher-target construction

- Zero-shot teacher generation on complete public BIRD training data.
- Fixed quick-execution filter.
- Official execution-match filter.
- Teacher-specific retained pools and provenance.
- BIRD gold as execution oracle and matched-control target, not the canonical
  FedLS-SQL training target.

### 3.4 Client-side parameter-efficient adaptation

Define private CE, LoRA configuration, local epochs, and transmitted objects.

### 3.5 Federated aggregation

Define sample-weighted factor-wise FedAvg. Present it as the protocol, not a
new optimizer.

### 3.6 Server-side large-to-small transfer

Define teacher-target CE and auxiliary reverse KL. State the exact
vocabulary/token-ID compatibility requirement for full-vocabulary KL.

### 3.7 Communication, deployment, and privacy properties

Separate structural properties from empirical resource measurements.

## 4. Experiments

### 4.1 Setup

- Spider private federated training and Spider dev primary evaluation.
- Fixed `K=5`, grouped-domain Dirichlet `alpha=0.5`, seed policy.
- BIRD public teacher pool and disjoint BIRD dev diagnostic.
- Spider-Realistic, Spider-Syn, and Spider-DK robustness sets.
- Qwen2.5 1.5B/7B primary pair and Gemma 2 2B/9B replication pair.
- LoRA/training/decoding details and immutable provenance.
- EX as primary metric; EM and execution-error rate as secondary diagnostics.

### 4.2 Main execution-accuracy results — RQ1

Compare centralized-standard SLM, independent pure FL, and FedLS-SQL at T3.
Report Spider first, followed by retained robustness/cross-dataset results and
paired question-level tests. Report training-seed uncertainty separately.

### 4.3 Transfer-mechanism ablation — RQ2

Use the matched T1 ladder:

1. shared pure-FL adapter;
2. matched public-gold CE;
3. teacher-target CE;
4. teacher-target CE plus reverse KL.

The main causal statement concerns execution-verified teacher guidance. Treat
the independent RKL increment as provisional.

### 4.4 Convergence and scoped generalization — RQ3

- Independent pure-FL versus FedLS-SQL at T1, T2, and T3.
- Same-work comparison of more rounds versus more local epochs.
- Spider perturbation results.
- Explicitly scope conclusions to the frozen non-IID partition unless the
  optional heterogeneity screen is promoted.

### 4.5 Second-family portability

Present the Gemma base/FL/gold-CE/teacher-target-CE/full ladder separately from
the Qwen headline table. Claim endpoint and hard-target portability, not a
controlled size effect or a family-independent RKL gain.

### 4.6 Communication and resource trade-offs — RQ4

- Trainable parameters, logical tensor payload, and serialized-file audit.
- Upload, broadcast, per-round, and T3 cumulative communication.
- Client LoRA process memory.
- Server-KD process memory.
- Student versus teacher deployment inference latency, throughput, and memory.
- Repeated shared-server protocol, fresh-run count, descriptive GPU telemetry,
  median, and dispersion.

### 4.7 EX-oriented error and mechanism analysis

- FL failures corrected or regressed by teacher transfer.
- Execution error versus executable-but-wrong SQL.
- Breakdown by Spider hardness and validated SQL constructs.
- A small audit of `EX=1, EM=0` to verify semantic correctness and explain
  cross-dataset SQL-form variation; do not optimize or rank methods by EM.
- Representative transfer successes and failures selected by fixed rules.

### 4.8 Optional heterogeneity sensitivity

Include only if a validated near-IID or stronger-skew comparison is completed.
Otherwise state that all federated conclusions concern the fixed
`K=5, alpha=0.5` partition.

## 5. Discussion

- Why execution-verified teacher targets help the federated SLM.
- Accuracy-resource-communication trade-off.
- Why teacher-target CE is more portable than the measured RKL increment.
- Structural data isolation and its difference from formal privacy.
- Public-pool dependence, offline teacher cost, shared-server benchmark limits,
  one primary partition, and no federated large-model baseline.

## 6. Conclusion

Answer the four RQs without introducing new claims or future-work mechanisms
as completed contributions.

## Core paper artifacts

1. Architecture/data-flow figure with the privacy boundary.
2. Main T3 accuracy table: centralized, pure FL, FedLS-SQL.
3. Matched public-supervision/transfer ablation table.
4. Pure-FL versus FedLS convergence figure.
5. Separate Gemma portability table.
6. Accuracy-resource-communication table.
7. EX-oriented error analysis table or figure.

The ordered production and decision checklist for these artifacts is
`PAPER_TODO.md`.

## Explicitly outside the target paper

- ICL as a method component;
- structural distillation;
- FedDF/client-ensemble KD;
- a novel federated optimizer claim;
- formal privacy guarantees;
- federated 7B efficiency claims without a corresponding experiment;
- full teacher-size, student-size, LoRA-rank, client-count, or skew Cartesian
  sweeps;
- treating Qwen and Gemma as a controlled parameter-size comparison.

FedProx-LoRA is a recommended reviewer baseline, not a proposed contribution.
One matched run is preferred before submission; if omitted, explain the scope
instead of presenting FedAvg as representative of every federated optimizer.
