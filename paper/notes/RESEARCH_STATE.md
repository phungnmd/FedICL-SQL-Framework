# FedLS-SQL: research state

Updated 2026-11-13. The project restarted on 2026-11-05; everything decided
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

Seed 0 and seed 1 are complete for the three DPO lines; the soft-target
controls and the row without the NLL term are seed 0 only. Numbers and
commits: `LAB_LOG.md`.

| Row | Spider test EX, seed 0 | Execution errors, seed 0 | Spider test EX, seed 1 | Execution errors, seed 1 |
|---|---:|---:|---:|---:|
| base model | 57.89 | 440 | | |
| centralized Spider | 70.75 | 219 | | |
| FedAvg R3 | 71.26 | 211 | 71.87 | 222 |
| virtual-teacher server stage, then FedAvg (`virtual_k2aaa_a3`) | 72.57 | 163 | | |
| self-teacher server stage, then FedAvg (`self_k2aaa_a3`) | 72.61 | 149 | | |
| gold server stage, then FedAvg (`gold_k2aaa_a3`) | 73.08 | 144 | 73.73 | 163 |
| Hinton server stage, then FedAvg (`hinton_k2aaa_a3`) | 73.31 | 129 | 74.06 | 132 |
| centralized Spider + BIRD (no privacy) | 73.96 | 163 | | |
| `hinton_k2aaa_a3` + NLL-only round | 73.50 | 117 | | |
| `hinton_k2aaa_a3` + 1 FedAvg SFT round | 74.15 | 132 | | |
| DPO round 1 from `hinton_k2aaa_a3`, with NLL / without NLL | 75.69 / 76.20 | 82 / 85 | | |
| DPO round 3 from FedAvg R3 | 75.13 | 101 | 75.83 | 95 |
| DPO round 3 from `gold_k2aaa_a3` | 75.22 | 71 | 76.57 | 71 |
| DPO round 3 from `virtual_k2aaa_a3` | 75.59 | 79 | | |
| DPO round 3 from `hinton_k2aaa_a3` (the method) | **76.71** | **58** | **77.04** | 74 |

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
| Teacher against a soft target, after DPO | DPO round 3 from `virtual_k2aaa_a3` to the method | +1.12 | -0.10 to +2.30 | at the edge |
| Soft target without the teacher, after DPO | DPO round 3 from gold to DPO round 3 from `virtual_k2aaa_a3` | +0.37 | -1.17 to +1.95 | no difference |
| Teacher before DPO | `gold_k2aaa_a3` to `hinton_k2aaa_a3` | +0.23 | -1.18 to +1.70 | no difference |
| NLL term, round 1 | DPO round 1 without NLL to DPO round 1 with it | -0.51 | -1.13 to +0.05 | no difference |

Both seeds pooled, clustered by question (95% interval):

| Part | Compared rows | Gain | 95% interval | Reading |
|---|---|---:|---|---|
| Whole method | FedAvg R3 to the method | +5.31 | +4.06 to +6.56 | clear |
| DPO stage | `hinton_k2aaa_a3` to the method | +3.19 | +2.35 to +4.03 | clear |
| DPO stage without a server stage | FedAvg R3 to its DPO round 3 | +3.91 | +2.82 to +5.01 | clear |
| Server stage before DPO | FedAvg R3 to `hinton_k2aaa_a3` | +2.12 | +0.95 to +3.29 | clear |
| Server stage after DPO | DPO round 3 from FedAvg R3 to the method | +1.40 | +0.32 to +2.47 | small, separable pooled |
| BIRD with gold SQL after DPO | DPO round 3 from FedAvg R3 to DPO round 3 from gold | +0.42 | -0.70 to +1.54 | no difference |
| Teacher after DPO | DPO round 3 from gold to the method | +0.98 | +0.05 to +1.91 | small, at the edge (p = 0.04) |

- The DPO stage is the solid part: 2.5 to 3.9 points from every start on
  both seeds, and
  the NLL term alone (+0.19) or more SFT rounds (+0.84, then a fall) do not
  give it. In round 1 the preference term alone does as well as DPO + NLL
  (76.20 against 75.69, not separable); rounds 2-3 without the NLL term
  are not run.
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
- The server stage after DPO, by seed. Seed 0: the gold stage ends level
  with no server stage (75.22 against 75.13) and the Hinton stage 1.49
  above it. Seed 1: the gold stage ends 0.75 above no server stage and the
  Hinton stage 0.47 above gold (76.57, 77.04). The gold line moves most
  between seeds (1.35 at round 3), so the seed 0 reading overstated the
  teacher's part. Pooled: teacher over gold +0.98 (p = 0.04), gold over no
  server stage +0.42 (not separable; separable on Spider dev, +2.08, and
  Realistic, +3.15). The BIRD stage keeps about 11.7 points on BIRD dev
  after DPO, with or without the teacher.
- Soft targets without the teacher (seed 0; `virtual_k2aaa_a3`, gold token
  0.73 and the rest uniform, and `self_k2aaa_a3`, the base student's
  logits; archived adapters, approved 2026-11-12 and 2026-11-13). Before
  DPO all four server stages are within 0.75 point on Spider test (gold
  73.08, virtual 72.57, self 72.61, Hinton 73.31); the Hinton stage leads on
  Spider dev and DK (over virtual +2.32 and +3.36). After DPO the virtual
  line ends with the gold line on every set (75.59 against 75.22 on Spider
  test) and the Hinton line 1.12 above it (69 / 93, p = 0.07), 3.48 on
  Spider dev, 3.93 on DK, level on Realistic, SYN and BIRD dev. A soft
  target alone does not give the lead; the control is one lineage on the
  seed whose gold line was low. The self-teacher stage costs 7.4 points on
  BIRD dev against the virtual one.
- On Spider test the Hinton line's lead after DPO sits on rows that flip
  between training lineages: where the gold and virtual lines agree (2,009
  rows) it is level (53 / 52); on the 138 rows where they disagree it is
  right on 96 (FedAvg line 82). On Spider dev and DK it also leads on the
  rows both agree on.
- The wrong results are not all out of reach: of the method's 442, 193 are
  right in at least one of the other 16 rows and 249 are wrong in every
  row.
- The teacher and the method have the same EX on Spider test and are right
  on different rows (teacher zero-shot 77.22, HF, 4-bit; archived row,
  approved 2026-11-12). Seed 0: 151 rows right only in the method, 162 only
  in the teacher; the teacher is right on 129 of the method's 442 wrong
  results and 33 of its 58 execution errors; at least one of the two is
  right on 84.26%. The teacher leads on medium and hard (82.3, 70.8 against
  79.8, 68.3), the method on extra-hard (63.0 against 57.7). The Hinton
  stage does not pass these rows on: after DPO its wins over the gold line
  are not on the rows the teacher gets right (64% against 66%).
- What the teacher's lead over the gold line is made of after DPO (seed 0,
  +32 rows): 25 from wrong results, 7 from execution errors, on extra-hard
  questions (63.0 against 59.9). Seed 1 does not repeat the extra-hard lead
  (62.7 against 63.6). Against the FedAvg line the lead is in execution
  errors on both seeds.
- CoT at 1.5B does not help (plan + SQL: server stage 60.64, one template
  client round 62.69, self-taught rounds at most 60.64). It is a short
  analysis in the paper, not part of the method.

## 5. Open

1. The teacher's role (owner decision pending). After DPO on Spider test
   the Hinton stage leads gold SQL by +1.49 (seed 0) and +0.47 (seed 1),
   +0.98 pooled (p = 0.04), and the virtual-teacher stage by +1.12 (seed 0,
   p = 0.07); gold and virtual are level. So the lead is small, not given
   by a soft target alone, and about as large as the spread of the gold
   line between seeds (1.35). Before DPO the teacher adds nothing on Spider
   test; on Spider dev and DK it leads on seed 0 before and after DPO, much
   less on seed 1.
2. Seeds. Two seeds for the three DPO lines; the DPO step and the method
   row repeat within 0.7 point. The teacher's gain over gold is at the edge
   after seed 1. A third seed of the three lines is queued (owner,
   2026-11-13), the Hinton and gold lines first, both server stages
   trained anew. The soft-target control on seed 1 needs its own server
   stage and 3 FedAvg rounds first (about 15.5 h with its DPO rounds,
   estimate); not queued.
3. The NLL term. In round 1 it adds nothing (76.20 without it, 75.69 with
   it, not separable). Whether it matters over rounds 2-3 needs 3 rounds
   without it, with their own sampling (about 5.5 h, estimate). It is one
   of the three differences from the closest DPO work named so far.
4. What the federated setting costs in the DPO stage. Reference rows, not
   a condition of the claim. In round 1 each client's adapter alone gives
   74.24 to 75.50 on Spider test (mean 74.97), the averaged adapter 75.69.
   Queued: DPO with the same recipe on the pooled client data
   (centralized, 3 rounds). A 3-round line without aggregation is not
   queued (new code, about 6 h).
5. Reference rows on the same engine: the 7B teacher, FedProx, FedNTD and
   the local client SFT models are queued with vLLM inproc (earlier seed 0
   adapters, approved 2026-11-13), and selection by execution over 8
   samples at inference on four seed 0 rows, to place the DPO stage next
   to a check that needs no training.
6. The 20% of wrong results. The method does not touch them, and they
   bound EX at about 77. The focused DPO pilot (arm `fdpo`, Focused-DPO:
   the preference term on the span where chosen and rejected differ) did
   not lower them: round 1 gives 76.20 against 75.69 for DPO round 1
   (10 / 21, p = 0.07), with 439 wrong results against 440 and 72 execution
   errors against 82. The span is two thirds of the response, so the pilot
   does not separate focus from a larger preference weight. It is an
   ablation row unless the owner decides otherwise. Not chosen: stricter
   labels from mutated client databases.

## 6. Current phase

Phases `sqldpo_s0` and `sqldpo_s1` are finished for the three DPO lines on
both seeds, the soft-target controls, DPO round 1 without the NLL term and
the client adapters of round 1 (last results 19:20 on 11-13). Queued on
GPU 0 (`PIPELINE_NEXT.md`, about 62 h from 11-13 evening, estimate): the
gold fallback and the NLL term over 3 rounds (open point 3), seed 2 of the
Hinton and gold lines (open points 1 and 2), selection by execution and
the reference rows (open point 5), the offline rounds and centralized DPO
(open point 4), then seed 2 of the FedAvg line. The preference term stays
plain and the method keeps the Hinton server stage until the owner decides
(2026-11-11).

Next owner decision: whether the teacher stays in the method (open point
1), once seed 2 of the Hinton and gold lines is in (about 09:35 on 11-15,
estimate).
