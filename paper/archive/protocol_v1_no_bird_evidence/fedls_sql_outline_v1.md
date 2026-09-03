# ARCHIVED — protocol-v1 manuscript outline

**Working title:** *FedLS-SQL: Execution-Verified Large-to-Small Knowledge
Transfer for Federated NL-to-SQL*

The P1.4b audit removes the generic “novel framework” claim. FedCoLLM is the
closest architectural prior and Struct-SQL already uses execution-correct
teacher SQL. The active distinction and citation matrix live in
`paper/notes/RELATED_WORK_NOVELTY_MATRIX.md`.

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

End with the nearest-work matrix and distinguish FedLS-SQL through its frozen
teacher, execution-verified public SQL, recurring post-aggregation refinement,
adapter-only client communication, and SLM-only deployment.

## 3. Problem formulation

- Federated clients, private schemas/examples, and non-IID partition.
- Server, public pool, frozen teacher, and deployed student.
- Threat model and structural privacy boundary.
- Objectives: accuracy, communication, compute, and inference efficiency.

## 4. FedLS-SQL

Paper-ready prose and Fig. 1 are maintained in `FEDLS_SQL_METHOD.md` and
`figures/fedls_sql_architecture.svg`.

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
- Recommended missing baseline: matched FedProx-LoRA. No federated large-model
  baseline is run or implied.
- Metrics: primary EX; secondary EM and execution errors; parameters and bytes
  communicated; scoped deployment VRAM/RSS/latency; and convergence rounds.

## 6. Results

Canonical values and pending cells are maintained in
`paper/results/MAIN_RESULTS.md`. The supplied August 19 outline is a draft
planning input: this section remains adaptive and must follow validated evidence
rather than preserving the draft structure:

1. Overall performance: primary Qwen2.5 track, with the cross-family Gemma
   portability result in a separate block.
2. Round-wise convergence and robustness under the current non-IID partition.
3. Matched supervision/KD ablation and training-seed reliability.
4. Communication payload and controlled accuracy/resource trade-offs.
5. One matched FedProx-LoRA reviewer baseline and one gated stronger-skew
   sensitivity; teacher/student-size, LoRA-rank, and client-count sweeps remain
   optional and absent sweeps are not implied to be complete.
6. Error analysis by execution validity, EX-EM disagreement, SQL difficulty,
   and validated failure categories.

## 7. Discussion

- Where federation and server guidance contribute separately.
- Practical deployment and privacy limitations.
- Dependence on the public corpus and teacher quality.
- ICL as a negative result for the tested 1.5B student.

## 8. Conclusion

Summarize whether LLM-to-SLM collaboration closes the lightweight federated
accuracy gap without moving private data or deploying the LLM at clients.
