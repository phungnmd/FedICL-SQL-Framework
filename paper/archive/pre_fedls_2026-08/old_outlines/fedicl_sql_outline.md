FedICL-SQL: A Novel Federated Large-Small Language Models
Framework with In-Context Learning for Natural Language to SQL

Student's Full Name1 and Quang-Hung Le*1
Department of Information Technology,
Quy Nhon University, Vietnam
Student Email, lequanghung@qnu.edu.vn

Abstract. A concise (150–250 words) summary.

  Background

o  Importance of Text-to-SQL (Natural Language to SQL) systems
o  Challenges of distributed enterprise databases

  Problem

o  Data privacy constraints
o  Schema heterogeneity
o  High computational costs of LLMs

  Proposed Method

o  Federated LLM-SLM architecture
o  Schema-aware In-Context Learning
o  Federated knowledge distillation

  Results
  Practical deployment potential for enterprise Text-to-SQL systems

1. INTRODUCTION

  Natural Language to SQL
  Challenges
  Motivation

o  Federated Learning: Collaborative learning without data sharing.
o  Large Language Models: Strong reasoning and SQL synthesis.
o  Small Language Models: Efficient deployment.
o  In-Context Learning: Rapid adaptation to unseen schemas.

  Research Questions

o  RQ1 (Federated Learning effectiveness): Can FedICL-SQL improve Text-to-SQL

performance in federated environments?

o  RQ2 (In-Context Learning effectiveness): Does schema-aware ICL improve

cross-domain generalization?

o  RQ3 (Large-to-Small Language Model knowledge transfer and efficiency): Can
LLM-to-SLM knowledge transfer achieve better efficiency-performance trade-
offs?

  Research Objectives

* Corresponding author: Quang-Hung Le (lequanghung@qnu.edu.vn)

1

o  To develop a novel privacy-preserving Text-to-SQL framework, namely FedICL-

SQL, that integrates Federated Learning, Large-Small Language Model
collaboration, and In-Context Learning to improve SQL generation performance,
schema generalization, and deployment efficiency across distributed database
environments.

  Main Contributions

o  Novel Federated LLM-SLM framework for Text-to-SQL.
o  Schema-aware In-Context Learning mechanism.
o  Federated SQL knowledge distillation strategy.
o  Privacy-preserving collaborative optimization.
o  Extensive evaluation on benchmark datasets.

2. RELATED WORK

2.1 Natural Language to SQL

2.2 Large Language Models for Text-to-SQL

2.3 Small Language Models

2.4 Federated Learning

2.5 In-Context Learning

2.6 Research Gap Analysis

3. PROPOSED APPROACH

3.1 Problem Formulation

3.2 Framework Overview

3.3 Global LLM Teacher

3.4 Local SLM Student

3.5 Teacher–Student Collaboration

3.6 Schema-Aware In-Context Learning

3.7 Federated SQL Knowledge Distillation

3.8 Federated Optimization

4. EXPERIMENTS

4.1 Experimental Setup

- Datasets:

  Spider

  Spider Realistic

- Teacher model: Qwen2.5-7B-Instruct (local HuggingFace per client)

2

- Students models: e.g., Phi-3 Mini, Gemma 2B, TinyLlama,…

- Main baselines:

  LLM-only models

  SLM-only models

  Centralized ICL systems

  Without ICL

- Evaluation Metrics:

  Text-to-SQL Metrics

o  Exact Match (EM)
o  Execution Accuracy (EX)

  Federated Learning Metrics:

o  Communication Cost,

o  Convergence Rate

  Efficiency Metrics:

o

Inference Latency,

o  GPU Memory Usage,

o  FLOPs

- Implementation details

4.2 Results & Discussion

- Overall Performance

- Impact of In-Context Learning

- Impact of LLM Teacher

- Impact of Federated Learning

- Communication Efficiency

- Privacy-Utility Trade-off

- Ablation Studies

  Without ICL

  Without federated learning

  Without Teacher LLM

  Different Retrieval Sizes

  Different SLM Architectures

5. CONCLUSION

3

  Summary of FedICL-SQL

  Main findings

  Practical implications

  Future research directions

o  Federated Retrieval-Augmented Generation

o  Multi-database reasoning

o  Agentic SQL generation

o  Continual federated learning

o  Real-world enterprise deployment

***

4

