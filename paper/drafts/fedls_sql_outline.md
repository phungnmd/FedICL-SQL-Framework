# FedLS-SQL manuscript outline

**Working title:** *FedLS-SQL: A Novel Federated Large-Small Language Models
Framework for Natural Language to SQL*

## Research question

Can large-to-small language model collaboration overcome the accuracy
limitations of lightweight federated NL-to-SQL models while retaining the
privacy, communication-efficiency, and resource advantages of federated
learning?

## 1. Introduction

- Motivation: accurate NL-to-SQL models are large or centrally trained, while
  organizational databases and query logs are private.
- Gap: lightweight federated models are deployable but accuracy-constrained;
  federating a large model is costly.
- Idea: keep the SLM at clients and transfer LLM knowledge only at the server
  through a public corpus.
- Contributions: FedLS-SQL architecture, server-side LLM-to-SLM transfer,
  parameter-efficient federated training, and accuracy/resource evaluation.

## 2. Related work

1. NL-to-SQL and cross-domain semantic parsing.
2. Federated learning for NLP and parameter-efficient fine-tuning.
3. LLM-based NL-to-SQL and knowledge distillation.
4. Large-small language model collaboration.

## 3. Problem formulation

- Federated clients, private schemas/examples, and non-IID partition.
- Server, public pool, frozen teacher, and deployed student.
- Threat model and structural privacy boundary.
- Objectives: accuracy, communication, compute, and inference efficiency.

## 4. FedLS-SQL

1. System overview.
2. Client-side LoRA fine-tuning on private gold SQL.
3. Sample-weighted factor-wise FedAvg.
4. Public teacher-target construction and logit caching.
5. Server objective: teacher-target CE plus reverse KL.
6. Multi-round optimization and deployment.

The current method does not include ICL or a distinct structural-distillation
module.

## 5. Experimental setup

- Data: Spider training/dev, Spider-Realistic, Spider-Syn, Spider-DK, and BIRD.
- Models: Qwen2.5-1.5B student and frozen Qwen2.5-Coder-7B teacher.
- Main baselines: base SLM, centralized SLM, pure FL, and FedLS-SQL.
- Additional baselines where feasible: FedProx and resource comparison with
  large-model FL.
- Metrics: EX, EM, execution errors, parameters, bytes communicated, time,
  VRAM/CPU memory, latency, and convergence rounds.

## 6. Results

1. Final Centralized vs FL vs FedLS-SQL comparison.
2. Round-wise convergence under non-IID partitioning.
3. Robustness and cross-corpus transfer.
4. Accuracy/communication/resource trade-offs.
5. Component and sensitivity ablations.
6. Error analysis by SQL difficulty and failure type.

## 7. Discussion

- Where federation and server guidance contribute separately.
- Practical deployment and privacy limitations.
- Dependence on the public corpus and teacher quality.
- ICL as a negative result for the tested 1.5B student.

## 8. Conclusion

Summarize whether LLM-to-SLM collaboration closes the lightweight federated
accuracy gap without moving private data or deploying the LLM at clients.
