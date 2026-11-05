# FedLS-SQL: research state

Fresh start on 2026-11-05. Everything decided or measured before this date is
archived and hidden (see `AGENTS.md`, "Fresh start"). This file says what is
fixed, what is open, and what we know so far.

## 1. Question

Several clients hold private Text-to-SQL data that cannot leave them. They
train a small model (SLM) together through federated learning. The server
holds a large frozen LLM teacher and public data from another domain. How can
the server teacher make the deployed SLM measurably better on the clients'
domain?

Goal: a Q3 journal paper in which the teacher's contribution is measurable.
A story where the teacher ends up as an ablation does not meet this goal.

Target venues: Data & Knowledge Engineering, International Journal of Data
Science and Analytics, Neural Processing Letters, Distributed and Parallel
Databases; stretch: Journal of Intelligent Information Systems.

## 2. Fixed setup

| Part | Fixed choice |
|---|---|
| Student (deployed alone) | Qwen2.5-Coder-1.5B-Instruct |
| Teacher | Qwen2.5-Coder-7B-Instruct, frozen, runs only at the server, only on public data |
| Clients | 5 clients on Spider train (8,659 rows), domain-cluster non-IID split `alpha_0.1/k5`. Private rows never leave a client. |
| Server public data | BIRD train with evidence (9,428 rows) |
| Communication | Clients send model updates, never data |
| Compute | Two RTX A5000 24 GB under WDDM (`fedicl-sql/docs/A5000_RUN_CONFIG.md`) |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation, not
differential privacy.

## 3. Open

Everything else, including:

- the method: how the teacher is used, what the clients train, the FL
  algorithm, adapter type and rank, prompting, decoding;
- the metrics and which evaluation sets carry the story (available: Spider dev
  1,034, Spider test 2,147, BIRD dev 1,534, Spider-Realistic, Spider-SYN,
  Spider-DK);
- the baselines and the experiment plan.

## 4. What we know

Nothing measured since the fresh start.

## 5. Current phase

Choosing a direction. No run is queued (`PIPELINE_NEXT.md`).
