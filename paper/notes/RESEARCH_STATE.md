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

Spider test, one seed (details in `LAB_LOG.md`):

- CoT at 1.5B: a teacher-plan server stage on BIRD reaches 60.64 (E5); one
  template client round 62.69; self-taught client SFT does not rise above
  E5 (60.08, 60.64, 58.69). SQL-only FedAvg R3 from the base model scores
  71.45; the base model 57.94.
- Archived results (owner allowed their use, 2026-11-10): FedAvg is level
  with centralized training on Spider (71.50 against 71.08); a BIRD server
  stage before FedAvg adds 1.5-2.4 points (`gold_k2aaa_a3` 73.03,
  `hinton_k2aaa_a3` 73.50); on Spider dev, SQL DPO + NLL raised a
  converged SFT student by about 1.5-2 points and CoT gained less from the
  same DPO rounds than SQL.

## 5. Current phase

Method (owner, 2026-11-10): a BIRD server stage with teacher KD, FedAvg on
the clients, then federated DPO + NLL on the clients' own SQL samples,
labelled by execution on each client's databases. Running on GPU 0: the
reference rows again with vLLM, SQL DPO round 1 from `hinton_k2aaa_a3` and
from FedAvg R3 (the control for the server stage), then more rounds from
`hinton_k2aaa_a3`. CoT stays as an analysis section: template client rounds
2-3, then CoT DPO, set against Liu et al. (ACL 2025).
