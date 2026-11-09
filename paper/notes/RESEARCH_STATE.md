# FedLS-SQL: research state

Fresh start on 2026-11-05. Everything decided or measured before this date is
archived and hidden (see `AGENTS.md`, "Fresh start"). This file says what is
fixed, what is open, and what we know so far.

## 1. Question

Several clients hold private Text-to-SQL data that cannot leave them. They
train a small model (SLM) together through federated learning, and only the
SLM is deployed. The server may hold a large frozen LLM teacher and public
data from another domain. How can the deployed SLM become measurably better
on the clients' domain than standard federated training?

Goal: a Q3 journal paper with a method that clearly beats the federated
baselines. Using the server teacher is an option, not a requirement: a method
without the teacher is acceptable if it is strong enough (owner, 2026-11-06).

Target venues: Data & Knowledge Engineering, International Journal of Data
Science and Analytics, Neural Processing Letters, Distributed and Parallel
Databases; stretch: Journal of Intelligent Information Systems.

## 2. Fixed setup

| Part | Fixed choice |
|---|---|
| Student (deployed alone) | Qwen2.5-Coder-1.5B-Instruct |
| Teacher (optional) | Qwen2.5-Coder-7B-Instruct, frozen. If used, it runs only at the server and only on public data |
| Clients | 5 clients on Spider train (8,659 rows), domain-cluster non-IID split `alpha_0.1/k5`. Private rows never leave a client. |
| Server public data (optional) | BIRD train with evidence (9,428 rows); SynSQL-2.5M may replace or join it (owner, 2026-11-07) |
| Communication | Clients send model updates, never data |
| Compute | Two RTX A5000 24 GB under WDDM (`fedicl-sql/docs/A5000_RUN_CONFIG.md`) |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation, not
differential privacy.

## 3. Open

Everything else, including:

- the method: whether and how the teacher is used, what the clients train,
  the FL algorithm, adapter type and rank, prompting, decoding;
- the metrics beyond Spider EX and which other sets carry the story
  (available: BIRD dev 1,534, Spider-Realistic, Spider-SYN, Spider-DK). Spider
  numbers use Spider test (2,147); Spider dev (1,034) is skipped or secondary
  (owner, 2026-11-07);
- the baselines and the experiment plan.

## 4. What we know

Nothing measured since the fresh start.

## 5. Current phase

Running the full CoT-with-teacher pipeline (`DIRECTION.md` section 6.3, step
1) as a curve from the base model: server teacher-plan SFT (up to 5 epochs, chained one epoch at a time),
query-plan client rounds (up to 5), full-data query-plan DPO rounds (up to
4), one seed, on GPU 0. The baselines (FedAvg R1-R5, SQL-only federated DPO)
follow after it. Commands in `PIPELINE_NEXT.md`.
