# FedLS-SQL: research state

Updated 2026-11-12. The project restarted on 2026-11-05; everything decided
or measured before that date is archived and hidden (see `AGENTS.md`, "Fresh
start"). This file says what is fixed, what the method is, what the results
show and what is still open. Runs and reasons are in `LAB_LOG.md`.

## 1. Question

Several clients hold private Text-to-SQL data that cannot leave them. They
train a small model (SLM) together through federated learning, and only the
SLM is deployed. The server may hold a large frozen LLM teacher and public
data from another domain. How can the deployed SLM become measurably better
on the clients' domain than standard federated training?

Goal: a journal paper at Q3 or above with a good method that clearly beats
the federated baselines; the target is a direction, not a bar to hit rigidly
(owner, 2026-11-11). The teacher is an option, not a requirement (owner,
2026-11-06).

Target venues: Data & Knowledge Engineering, International Journal of Data
Science and Analytics, Neural Processing Letters, Distributed and Parallel
Databases; stretch: Journal of Intelligent Information Systems.

## 2. Fixed setup

| Part | Fixed choice |
|---|---|
| Student (deployed alone) | Qwen2.5-Coder-1.5B-Instruct, SQL-only output, greedy decoding |
| Teacher (optional) | Qwen2.5-Coder-7B-Instruct, frozen. If used, it runs only at the server and only on public data |
| Clients | 5 clients on Spider train (8,659 rows), domain-cluster non-IID split `alpha_0.1/k5`. Private rows never leave a client. |
| Server public data (optional) | BIRD train with evidence (9,428 rows); SynSQL-2.5M may replace or join it (owner, 2026-11-07) |
| Communication | Clients send model updates, never data |
| Compute | Two RTX A5000 24 GB under WDDM (`fedicl-sql/docs/A5000_RUN_CONFIG.md`); GPU 1 is in use by another user for now |

Data rules: train and test never share a database; test data never becomes
training, retrieval or teacher data; privacy is structural data isolation,
not differential privacy.

Metric: Spider test EX (2,147 rows), evaluated through vLLM
(`--vllm-determinism inproc`). Choices are made on Spider test, so it is
never called held-out. No choice has been made on Spider dev, Realistic, SYN
and DK (all four on the 20 Spider dev databases); they are the check that
does not depend on a choice.

## 3. Method

Chosen by the owner on 2026-11-10. Three stages:

1. Server stage: the student trains at the server on BIRD for 2 epochs,
   with Hinton KD from the teacher. Under test: the same stage with gold SQL
   only (no teacher), and no server stage at all.
2. FedAvg SFT: 3 rounds on the clients' Spider rows.
3. Federated DPO + NLL: 3 rounds, fixed for every line and seed. In a round
   each client samples 8 SQL for each of its questions from the current
   model, labels them by execution on its own databases, pairs a correct
   sample with a wrong one (the gold SQL is the chosen side when no sample
   is correct), trains on the pairs, and the server averages the updates.

The claim rests on stage 3. Stage 1 and the teacher stay in the method only
if the controls show their role (section 5). Federated learning is the
setting the method has to work in; the paper does not claim that federation
produces the gain (owner, 2026-11-11).

Closest prior work (`LITERATURE.md`): federated DPO as local DPO with LoRA
averaging, on human preferences (OpenFedLLM, FedBiscuit); centralized DPO on
execution-labelled SQL samples at 7B and above, where SQL-only DPO gave no
gain (Liu et al., ACL 2025; ExCoT); gold as the chosen side (Iterative RPO).
Different here: the pairs are built and labelled at each client by
execution on its own databases, for Text-to-SQL, at 1.5B.

## 4. What the results show

Seed 0 is complete; seed 1 has the Hinton and FedAvg lines, the gold line
is running. Numbers and commits: `LAB_LOG.md`.

| Row | Spider test EX, seed 0 | Execution errors, seed 0 | Spider test EX, seed 1 | Execution errors, seed 1 |
|---|---:|---:|---:|---:|
| base model | 57.89 | 440 | | |
| centralized Spider | 70.75 | 219 | | |
| FedAvg R3 | 71.26 | 211 | 71.87 | 222 |
| gold server stage, then FedAvg (`gold_k2aaa_a3`) | 73.08 | 144 | running | |
| Hinton server stage, then FedAvg (`hinton_k2aaa_a3`) | 73.31 | 129 | 74.06 | 132 |
| centralized Spider + BIRD (no privacy) | 73.96 | 163 | | |
| `hinton_k2aaa_a3` + NLL-only round | 73.50 | 117 | | |
| `hinton_k2aaa_a3` + 1 FedAvg SFT round | 74.15 | 132 | | |
| DPO round 3 from `gold_k2aaa_a3` | 75.22 | 71 | queued | |
| DPO round 3 from FedAvg R3 | 75.13 | 101 | 75.83 | 95 |
| DPO round 3 from `hinton_k2aaa_a3` (the method) | **76.71** | **58** | **77.04** | **74** |

What each part adds, seed 0 (95% interval from a bootstrap over the 40
test databases):

| Part | Compared rows | Gain | 95% interval | Reading |
|---|---|---:|---|---|
| Whole method | FedAvg R3 to the method | +5.45 | +3.45 to +7.43 | clear |
| DPO stage | `hinton_k2aaa_a3` to the method | +3.40 | +2.21 to +4.53 | clear |
| DPO stage without a server stage | FedAvg R3 to its DPO round 3 | +3.87 | +2.23 to +5.60 | clear |
| Preference term | best SFT control to the method | +2.56 | +1.35 to +3.77 | clear |
| Against no privacy | centralized Spider + BIRD to the method | +2.75 | +0.84 to +4.64 | clear |
| Server stage after DPO | DPO round 3 from FedAvg R3 to the method | +1.58 | -0.09 to +3.20 | at the edge |
| BIRD with gold SQL after DPO | DPO round 3 from FedAvg R3 to DPO round 3 from gold | +0.09 | -1.64 to +1.84 | no difference |
| Teacher after DPO | DPO round 3 from gold to the method | +1.49 | -0.24 to +3.16 | at the edge |
| Teacher before DPO | `gold_k2aaa_a3` to `hinton_k2aaa_a3` | +0.23 | -1.18 to +1.70 | no difference |

Both seeds pooled, clustered by question (95% interval):

| Part | Compared rows | Gain | 95% interval | Reading |
|---|---|---:|---|---|
| Whole method | FedAvg R3 to the method | +5.31 | +4.06 to +6.56 | clear |
| DPO stage | `hinton_k2aaa_a3` to the method | +3.19 | +2.35 to +4.03 | clear |
| DPO stage without a server stage | FedAvg R3 to its DPO round 3 | +3.91 | +2.82 to +5.01 | clear |
| Server stage before DPO | FedAvg R3 to `hinton_k2aaa_a3` | +2.12 | +0.95 to +3.29 | clear |
| Server stage after DPO | DPO round 3 from FedAvg R3 to the method | +1.40 | +0.32 to +2.47 | small, separable pooled |

- The DPO stage is the solid part: 3.2 to 3.9 points from either start on
  both seeds, and
  the NLL term alone (+0.19) or more SFT rounds (+0.84, then a fall) do not
  give it.
- Other sets: the method is above FedAvg R3 by 5.3 (Realistic) to 12.0 (DK)
  points on Spider dev, Realistic, SYN and DK (seed 0). After DPO the
  Hinton line leads the FedAvg line on every set and both seeds; pooled:
  Spider dev +3.53, DK +4.11, SYN +2.03, Realistic +1.38 (not separable),
  BIRD dev +11.38.
- The server stage after DPO: +1.58 on seed 0, +1.21 on seed 1 (84 / 110,
  p = 0.07), +1.40 pooled (p = 0.01). Within one seed the database
  interval touches zero. DPO closes a quarter to a half of the lead the
  stage had before it; the lead that stays is in execution errors (round
  3, seed 1: 74 against 95; wrong results 419 against 424).
- Where the gain comes from: executable SQL. From FedAvg R3 to the method,
  right rows +117, execution errors -153, wrong results +36. About 440 rows
  (20% of Spider test) are executable SQL with a wrong result in every row
  from the base model to DPO round 4; no stage lowers that count.
- The training pairs show the same: pairs whose rejected side is an
  execution error fall from 2,806 to 858 over four rounds, pairs whose
  rejected side is a wrong result only from 2,587 to 2,012.
- The line saturates: round 4 (76.94) is not separable from round 3; by
  round 4, 6,425 of 8,659 client questions have all 8 samples correct and
  58 execution errors are left on Spider test (2.7 points).
- The server stage: BIRD with gold SQL has no lead left after DPO (74.34,
  75.13, 75.22 at rounds 1 to 3, against 74.29, 75.17, 75.13 from
  FedAvg R3). The Hinton stage keeps 1.3 to 1.5 points over the gold stage
  at every round, on the same BIRD questions: what survives DPO comes from
  the teacher, not from the BIRD data. Before DPO the Hinton stage is
  already ahead of the gold stage on Spider dev (+2.32) and DK (+5.42),
  sets no choice was made on.
- The wrong results are not all out of reach: of the method's 442, 193 are
  right in at least one of the other 16 rows and 249 are wrong in every
  row.
- CoT at 1.5B does not help (plan + SQL: server stage 60.64, one template
  client round 62.69, self-taught rounds at most 60.64). It is a short
  analysis in the paper, not part of the method.

## 5. Open

1. The teacher's role. On seed 0 the answer is: Hinton KD at the server
   stage, or no server stage; the gold stage adds nothing after DPO.
   Hinton against gold is +0.23 before DPO and +1.35, +1.30, +1.49 after
   one to three DPO rounds, one pair of training lineages. Seed 1 repeats
   the lead over the FedAvg line (+1.21; +1.40 pooled); the gold line of
   seed 1 decides whether that lead is the teacher's or BIRD's (running).
2. Seeds. Two seeds for the Hinton and FedAvg lines; the DPO step and the
   method row repeat within 0.7 point. A third seed is worth its cost
   (about 30 h on one card for the FedAvg and DPO rounds of the three
   lines, plus two server stages; estimate) only if the teacher's gain
   over gold stays at the edge after seed 1.
3. What the federated setting costs in the DPO stage. Reference rows, not
   a condition of the claim; not run and not queued: DPO with the same
   recipe on the pooled client data (centralized), and DPO at each client
   without aggregation (local only). About 5.5 to 6 GPU-h each (estimate).
4. Reference rows on the same engine: FedProx, FedNTD and the local client
   models have no vLLM inproc number yet. BIRD dev is queued for 6 rows.
5. The 20% of wrong results. The method does not touch them, and they
   bound EX at about 77. The focused DPO pilot (arm `fdpo`, Focused-DPO:
   the preference term on the span where chosen and rejected differ) did
   not lower them: round 1 gives 76.20 against 75.69 for DPO round 1
   (10 / 21, p = 0.07), with 439 wrong results against 440 and 72 execution
   errors against 82. The span is two thirds of the response, so the pilot
   does not separate focus from a larger preference weight. It is an
   ablation row unless the owner decides otherwise. Not chosen: stricter
   labels from mutated client databases.

## 6. Current phase

Phase `sqldpo_s1` on GPU 0 (`PIPELINE_NEXT.md`): the Hinton and FedAvg
lines of seed 1 are done, with the other sets; the gold line runs next
(about 07:15 on 11-13 with its other sets, estimate), then DPO round 1
without the NLL term (seed 0). The preference term stays plain and the
method keeps the Hinton server stage until the gold line of seed 1 is read
(owner, 2026-11-11).

Next owner decisions, after the seed 1 lines:

- whether the teacher stays in the method (open point 1): Hinton against
  the FedAvg and gold lines after DPO, both seeds pooled by question;
- then the reference rows of open points 3 and 4, and a third seed if the
  teacher's gain is at the edge.
