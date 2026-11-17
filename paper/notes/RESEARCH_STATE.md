# FedLS-SQL: research state

Updated 2026-11-17. On this date the owner set the project up again from
clean: a new prompt, refactored code (package `fedls_sql`) and every result
produced again. This file says what is fixed, what the method is and what
is open. Runs and decisions are in `LAB_LOG.md`.

## 1. Question

Several clients hold private Text-to-SQL data that cannot leave them. They
train a small model together through federated learning, and only that
model is deployed. The server may hold a large frozen LLM and public data
from another domain. How can the deployed model become measurably better
on the clients' domain than standard federated training?

Goal: a journal paper at Q3 or above (candidates: CMC, JIIS) with a method
that clearly beats the federated baselines and reports good numbers.

## 2. Setup

| Part | Choice | State |
|---|---|---|
| Student (deployed alone) | Qwen2.5-Coder-1.5B-Instruct with LoRA, SQL-only output | fixed |
| Clients | 5 clients on Spider train (8,659 rows), domain-cluster non-IID split `alpha_0.1/k5`; private rows never leave a client | fixed |
| Teacher | Qwen2.5-Coder-7B-Instruct, frozen, at the server, on public data only | fixed; used by stage 1, which comes after the client stages |
| Public data | BIRD train with evidence (9,428 rows); SynSQL-2.5M may replace or join it | fixed |
| Decoding | greedy, no repetition penalty (the code sets 1.0 and never reads the model's generation config) | fixed |
| Metric | Spider test EX (2,147 rows) through vLLM. Rounds, steps and settings may be chosen on Spider test (owner, 2026-11-17); such a number is reported as chosen on Spider test, never as held-out | fixed |
| Prompt | a standard published format, one for training, sampling and evaluation | open, section 4 |
| Training recipe | LoRA SFT at lr 2e-4, 3 FedAvg rounds of 1 local epoch (the recipe of SPFT-SQL for this student is lr 2e-4, 3 epochs) | open, section 4 |
| Compute | RTX A5000 24 GB under WDDM; GPU 1 is in use by another user | fixed |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation,
not differential privacy.

## 3. Method

Three stages (owner, 2026-11-17). The supervision a small Text-to-SQL model
needs sits in two places that cannot meet: the server has a large LLM and
public data and never sees a client's data; a client has its questions and
databases and cannot share them. The method takes each kind of supervision
where it lives, and only the small model's adapter moves between the two.

| Stage | Where | Supervision | Order of work |
|---|---|---|---|
| 1. Server stage | server | the teacher on public data | after stages 2 and 3 are in place |
| 2. FedAvg SFT | clients | the labelled questions | first |
| 3. Federated DPO + NLL | clients | execution of the model's own SQL on the client's databases | first; the centre of the paper |

Stage 3 in a round: each client samples several SQL for each of its
questions from the current model, labels them by execution on its own
databases, pairs a correct sample with a wrong one, trains with DPO plus an
NLL term on the chosen side, and the server averages the updates.

Closest work: CodeLutra (arXiv 2411.05199), the same loop run centrally at
8B. It starts from the base model with no SFT stage (its SFT model is a
separate baseline), draws 10 samples at T 1.0, uses only the model's own
correct samples as the chosen side, and trains DPO + SFT with beta 0.1 and
lambda 1.0, LoRA r 8, lr 5e-5, one epoch per iteration, 4 iterations.
Different here: federated, 1.5B, after FedAvg SFT, the gold SQL as the
chosen side when no sample is correct. The rest of the map is in
`LITERATURE.md`.

## 4. Open

1. The prompt. Checked practice is in `LITERATURE.md`, section 1.19: most
   work feeds `CREATE TABLE` text plus a few database values, as one user
   message through the chat template, and a fine-tuned small model outputs
   SQL only. Candidates, none of which needs a trained filter or a
   retriever:

   | Candidate | Schema text | Used by |
   |---|---|---|
   | A | `CREATE TABLE` text and 3 example rows per table, the line `-- Using valid SQLite, answer the following questions for the tables provided above.`, the question, "Please output only the final SQL query, starts with keyword `SELECT`." | Rajkumar et al. 2022; Chang and Fosler-Lussier 2023; the Qwen2.5-Coder report and its evaluation code |
   | B | `CREATE TABLE` text with example values of each column as SQL comments | OmniSQL, SLM-SQL (with reasoning in the output; here SQL only), MSc-SQL |
   | C | `CREATE TABLE` text alone | CodeLutra, DAIL-SQL's code representation |

   A is the format the student's authors evaluate it with. The choice is
   the owner's; a zero-shot read of the base model on Spider test with each
   candidate takes minutes per candidate.
2. The training target: the SQL followed by the end token; whether gold SQL
   is normalized (CodeS upper-cases keywords and lower-cases identifiers;
   2,046 of the 8,659 Spider train golds end with `;`).
3. Stage 3 settings where CodeLutra and the earlier setup differ: samples
   per question (10 or 8), temperature (1.0 or 0.7), pairs per question,
   LoRA rank (8 or 16), learning rate and epochs.
4. The seeds of sampling (round and client in the seed) and of the SFT
   shuffle.
5. Stage 1 and the teacher's role. In the earlier setup the teacher's own
   part was small against gold SQL on the same public data.
6. Baselines with the new prompt: FedAvg, FedProx, FedNTD, centralized SFT.

## 5. Results

None on the clean setup yet.

## 6. Earlier work

Everything measured before 2026-11-17 is reference only: it was produced
with a prompt that carried a sentence left from an earlier ICL project, and
most of it with a repetition penalty of 1.1 that nobody had set. Both
repositories as they were are at the tag `archive/pre-reset-2026-11-17`
and, on the owner's Mac, in `archive/reset_2026-11-17/` (start at its
`OVERVIEW.md`). A number from there is quoted as "earlier setup" and never
as a result.
