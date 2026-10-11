# FedLS-SQL — lab log

Newest first. Each entry says what ran, the key numbers, where the evidence
lives, and what was decided. All numbers are seed 0, EX (%), protocol v2.

Older detail:

- 2026-09-24 to 2026-10-09 (Coder-0.5B, Qwen2.5-1.5B-Instruct, P2.2-P2.26):
  [`LAB_LOG_2026-09-24_to_2026-10-09.md`](../archive/lab_log_2026-10/LAB_LOG_2026-09-24_to_2026-10-09.md)
- 2026-09-03 to 2026-09-26, full text:
  [`LAB_LOG_2026-09-03_to_2026-09-26.md`](../archive/lab_log_2026-09/LAB_LOG_2026-09-03_to_2026-09-26.md)
- Protocol v1 (no BIRD evidence):
  `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`
- Before FedLS-SQL: `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`

## Where we are (2026-10-11)

- Phase E (exploration): complete the Coder-1.5B baselines at seed 0 on the
  dev sets, then fix the paper story in a dated entry before any seed 1-2 run
  or Spider test evaluation. Findings, open questions and rules in force:
  [`RESEARCH_STATE.md`](RESEARCH_STATE.md).
- P2.27 complete; `central` finished on the server, publication pending.
  P2.28 and P2.29 published. P2.36 (`g_plain`) on GPU 1.

## 2026-10-11: phase E arm list (P2.37), fixed before any run

Coder-1.5B, alpha 0.1, seed 0, P2.27 recipe and evaluation; Spider dev, its
variants and BIRD dev only. Code: nested `9a38777`
(`scripts/run_p237_phase_e.py`). No arm is added after results are read.

| Arm | Stages | Question (RESEARCH_STATE) |
|---|---|---|
| `hinton_k2aaa`, `gold_k2aaa` | K2 from base (two continuous epochs), then A, A, A plain | Q2, Q3: K-first, teacher vs gold |
| `hinton_akaka_plain`, `gold_akaka_plain` | P2.27 K1 of the same objective, then A, K, A, all plain | Q2, Q3: interleaved without NTD; with `h_plain`/`g_plain` it isolates NTD in A2 |
| `local_c1`..`local_c5` | each client alone, 3 epochs on its own split | Q1: value of federation |
| `central_mix` | P2.26 Spider+BIRD union, 3 epochs, centralized | Q4: reference with all data in one place |

Already available: base, FL, FedNTD, gold v1, Hinton v1, `central` (P2.27),
`h_plain` (P2.29), `g_plain` (P2.36).

- Read descriptively (exact McNemar and Wald per set, both domains):
  teacher - gold at each schedule; K-first - interleaved per objective;
  interleaved plain - `h_plain`/`g_plain` (NTD in A2); each arm - FL;
  `central` and `central_mix` - FL; FL - best local client; trajectories
  after every stage. No decision rule: phase E informs the story entry.
- Not in phase E: SeqKD (P2.6: its edge at the public endpoint was gone
  after the last private round), alpha 0.5 (Q6), AK2AA (between K-first and
  interleaved at 0.5B, weakest teacher edge).

## 2026-10-11: docs reset; exploration phase E before a paper story

Owner decision. The plan had fixed a method and a story too early (direction
A, then B with `h_plain`), while the Coder-1.5B table still lacked basic
baselines: local-only training, K-first schedules, an interleaved chain
without NTD, and `central_mix`. Several choices were kept by inertia:
AKAKA was the 2026-10-07 default schedule, and NTD in A2 came from method v1
although P2.25 showed it has no effect.

- R12 (method `h_plain`, claims P/T/D) and R11 are suspended. Recorded
  outcomes under all earlier rules stand.
- Still in force: R10 (Spider test only for confirmation), R13 (clustered
  pooled test, three seeds, no seeds added after reading), R8, R9, and the
  disclosure requirement of R13.
- Phase E runs at seed 0 on Spider dev, its variants and BIRD dev only. Its
  arm list is fixed in a separate entry before the first run; no arm is added
  after results are read.
- The story (claims, comparators, test, wording per outcome) is fixed in a
  dated entry before seeds 1-2 or Spider test.
- Docs: `RESEARCH_STATE.md` replaces the direction plan, the experiment matrix
  and the stale result tables; those, the manuscript outline and closed notes
  moved to `paper/archive/directions_2026-10/`. Entries before 2026-10-10
  moved to the archived log above.

## 2026-10-11: R13, amendment to R7 and R12: clustered test, seed count, fallback wording, disclosure

Owner decision, written before any seed 1-2 result, any Spider test
evaluation, and before P2.36 (`g_plain`) is read. Evidence for the power
numbers: nested `007989f` (`scripts/audit_power_clustered.py`,
`audits/protocol_v2/power_clustered/`; local commit, pushed after the
running lanes publish).

Why: the R7 test (exact conditional test on summed discordant pairs) treats
each question-seed pair as independent. The same question is correlated
across seeds: in P2.22 the per-question paired difference correlates 0.60
(Spider dev) and 0.51 (BIRD) between seeds 0 and 1. The summed test then
gives p values that are too small; copying one seed's 66/52 three times turns
p=.23 into p=.029 with no new information. The pooled Wald interval for BIRD
has the same flaw. Recorded outcomes keep their original test (P2.22 already
used the clustered test; P2.27 and P2.29 are single-seed).

1. **Test.** For every pooled claim (R7, R12, R11 via R12): per question, the
   mean over seeds of (method EX - comparator EX). Spider passes if the mean
   is positive and the two-sided p of the normal test across questions is
   below .05; BIRD passes if the lower bound of the same clustered 95% CI is
   above -2.0. Implementation: `run_p222_ntd_seed1.pooled`. Inference is over
   questions, conditional on the training seeds used; between-seed variance
   is reported descriptively (per-seed deltas and whether their signs agree).
   The R12 question-bootstrap check stays as a sensitivity analysis.
2. **Seeds: three (0, 1, 2).** Power of the clustered test (normal
   approximation; pilots are selected seed-0 dev effects, so likely
   optimistic):

   | Claim T (Spider test) | rho 0.60 (P2.22) | rho 0.30 |
   |---|---:|---:|
   | 3 seeds, pilot effect +1.35 | 0.58 | 0.72 |
   | 3 seeds, half effect +0.68 | 0.19 | 0.25 |
   | 5 seeds, pilot effect | 0.62 | 0.80 |
   | 5 seeds, half effect | 0.20 | 0.29 |

   T's BIRD non-inferiority holds with probability 0.94-1.00 at the pilot
   BIRD effect (+1.89) and 0.66-0.83 if the true BIRD effect is zero. P has
   power 0.90-1.00 even at half its seed-0 effect. Because seeds are
   correlated, five seeds add 4-8 points of power for about 67% more compute;
   seeds are not the lever. A failed T is therefore likely even if the effect
   is real, and the paper says so. P2.22's rho comes from reseeding only the
   last round, so full-chain seeds likely correlate less (the rho 0.30
   column).
3. **Stopping rule.** No seed is added, replaced or dropped after any
   confirmation result is read. A run that fails technically is rerun with
   the same seed and command.
4. **Wording fixed by outcome.** The paper uses the line for the outcome
   that occurs:
   - P and T pass: teacher supervision adds to public cross-domain training.
   - P passes, T fails on Spider: "Public cross-domain training improves
     federated Text-to-SQL; the added benefit of teacher supervision over
     public gold was not confirmed under the pre-specified criterion." The
     estimate and CI are reported; no claim of equivalence or of no effect.
   - T's Spider estimate is negative: report that matched gold scored higher.
   - T passes Spider but fails BIRD non-inferiority: T fails (both parts are
     required); report the Spider gain with its BIRD cost.
   - P fails: no positive pipeline claim; the owner re-plans the paper.
   - In no case does a JOIN subgroup or another component replace a failed
     claim; JOIN becomes a claim only through R8.
   - Pre-specified secondary contrast, reported without a claim:
     `g_plain` - FL with the same test, so the paper can say whether public
     gold alone helps.
5. **D is a recipe comparison.** `h_plain` and `hinton_k2aaa` differ in K
   placement, NTD in A2 and stage structure, so D compares two recipes at a
   matched budget and does not isolate placement. Its criterion is unchanged.
6. **Selection disclosure (paper).**
   - The paper has a short chronology:
     - 2026-10-07: AKAKA is the default schedule unless K2AAA wins at p<.05.
     - 2026-10-08: co-primary Spider and BIRD criterion; method v1 fixed.
     - 2026-10-11:
       - R10 (Spider test) and R11 (K-first);
       - `h_plain` selected on seed 0 Spider dev after P2.29;
       - direction B (R12);
       - this amendment.
   - It states that 118 checkpoints were evaluated on protocol-v2 Spider dev
     during development. That count covers all students, bases and
     intermediate stages in `experiments/*/results`; 15 are Coder-1.5B (P2.27:
     14, P2.29: 1). Archived evaluations are not counted.
   - It states that BIRD dev was also used in development and is not a
     holdout.
   - Outcomes under the 2026-10-08 criterion are reported as recorded.
   - Seed 0 dev effects are described as exploratory signals, not forecasts.

## 2026-10-11: A2 test-suite EX on seed 0 Spider dev (descriptive)

Evidence: nested `081a684` (`scripts/audit_test_suite_ex.py`,
`audits/protocol_v2/test_suite_ex_s0/`; local commit, pushed after the
running lanes publish). CPU only, on published predictions. A prediction is
test-suite correct when it matches gold (same comparison as EX, 60 s per
query) on the original database and on all 695 official test-suite databases
of the 20 dev db_ids (Zhong et al., EMNLP 2020); no value plugging.

| Arm, seed 0 | EX | TS-EX | EX-only rows |
|---|---:|---:|---:|
| FL A3 | 67.60 | 62.19 | 56 |
| FedNTD A3 | 67.79 | 60.93 | 71 |
| gold v1 A3 | 67.89 | 61.32 | 68 |
| Hinton v1 A3 | 69.25 | 62.77 | 67 |
| h_plain | 71.76 | 66.05 | 59 |

| Contrast | EX all | TS-EX all | TS-EX JOIN | TS-EX no-JOIN |
|---|---|---|---|---|
| h_plain - FL A3 | +4.16 (p<.001) | +3.87 (91/51, p<.001) | +9.31 (p<.001) | +0.32 (p=.90) |
| h_plain - Hinton v1 A3 | +2.51 (p=.005) | +3.29 (p<.001) | +2.45 (p=.24) | +3.83 (p<.001) |
| Hinton v1 - gold v1 | +1.35 (p=.23) | +1.45 (p=.22) | +5.64 (p=.009) | -1.28 (p=.36) |
| Hinton v1 - FL A3 | +1.64 (p=.20) | +0.58 (p=.70) | +6.86 (p=.003) | -3.51 (p=.018) |

- EX overstates every arm by 5-7 points, about equally; the method has the
  fewest EX-only rows after FL. No seed-0 conclusion depends on false
  positives: every contrast keeps its sign and size under test-suite EX, and
  the JOIN/no-JOIN pattern of the previous entry holds.
- Paper: report test-suite EX next to EX for Spider dev. Spider test has no
  official test suite; its claims stay on EX (R10, R12).

## 2026-10-11: where the plain last round gains; R12 reporting additions

Descriptive, seed 0, Spider dev, recomputed from published predictions
(P2.27 nested `5604e61`, P2.29 `b4a52db`). Subsets by `\bjoin\b` in the
gold SQL (408 JOIN, 626 no-JOIN). "Over-join" = predicted SQL has JOIN where
gold has none.

| Contrast | JOIN | no-JOIN |
|---|---|---|
| h_plain - Hinton v1 A3 (NTD last round) | +0.98 (23/19, p=.64) | +3.51 (30/8, p<.001) |
| h_plain - FL A3 | +9.07 (53/16, p<.001) | +0.96 (32/26, p=.51) |

- Over-joins on the 626 no-JOIN questions: FL A3 87, Hinton v1 A3 84,
  h_plain 57. Of the 30 no-JOIN questions h_plain wins over v1, v1
  over-joined in 16.
- Reading (hypothesis for seeds 1-2): the method's gain over FL is on JOIN
  questions; the NTD last round keeps the post-K over-joining, which costs
  no-JOIN questions, and a plain last round removes it. This corrects an
  earlier note: the table-set proxy (P2.27 Hinton vs gold, JOIN 322 vs 315 of
  408, p=.39) checks tables only, not column linking, join keys or scope, so
  it does not rule out a schema-linking gain.
- Thresholds of R12 are unchanged. Added reporting, fixed before any seed
  1-2 or Spider test result: (a) every R12 contrast also per seed; (b) a
  question-level sensitivity check: per question, mean over seeds of
  (method EX - comparator EX), mean and 95% CI by question bootstrap and a
  one-sample t-test over questions; (c) the JOIN/no-JOIN split and over-join
  counts above for each R12 contrast. None of these changes a decision.
- Independent review of three optional screens (curriculum ordering in the
  last round, TAID-style target interpolation in K2, execution preferences):
  not run. Curriculum is the only candidate kept, after P2.35, with a rule
  written before any run; TAID (VRAM risk, K-stage gains fade after A,
  P2.24) and DPO (SENSE prior art, ACL 2025 counter-evidence) are parked.
  Measured stage times are higher than earlier estimates: Hinton K2 about
  4.5 h, plain A3 about 2.4 h.

## 2026-10-11: direction B (private domain first); rule R12 fixed before results

Owner decision, after P2.29 and before any seed 1-2 result, any Spider test
evaluation, `central`, or a gold arm with a plain last round at Coder-1.5B.

Why: the result that holds across all three students is a Spider gain of
Hinton KD over FL when the last private round is plain (0.5B +5.0, 1.5B-
Instruct about +4.5, Coder-1.5B `h_plain` +4.16, p=.0002), plus a Spider edge
over matched gold (+2.42, p=.020; +2.03, p=.033). The BIRD gain over FL is
large but expected (public gold gives +15.7). The 2026-10-08 co-primary
criterion was motivated by "Spider fades, BIRD persists", which the
2026-10-08 P2.20 entry already found does not hold at the final model; at
Coder-1.5B, last-round NTD removes most of the Spider gain (P2.29). Seed 0
dev results generated this hypothesis; the confirmation uses unread data
(seeds 1-2, Spider test for all seeds).

- **Design.** Per objective (Hinton, gold), one shared chain
  `A>K>A[ntd]>K`, then two last-round branches: plain A (the method branch,
  Spider point) and A[ntd] (v1, BIRD point). Method = Hinton chain with a
  plain last round (`h_plain`).
- **R12, claims (seeds 0-2 pooled, R7 test).** Each comparison passes if
  Spider test improves with p<.05 (exact conditional test on summed
  discordant pairs) and the pooled BIRD dev Wald 95% lower bound is above
  -2.0. (Test replaced by the question-clustered test, R13.) Three separate hypotheses, no multiplicity correction (stated):
  P = method vs FL `A>A>A` (pipeline); T = method vs `g_plain` (gold chain,
  plain last round; teacher); D = method vs `hinton_k2aaa` (R11, K-first at
  matched budget). R11's comparison now uses this criterion.
- **Reported, no claim:** the NTD branch for both objectives (v1 Hinton vs
  gold v1 under the old co-primary criterion, as R7 defined it), the
  Spider-BIRD plot of every arm, the Spider dev family, R8, R9.
- Earlier rule outcomes stand as recorded (P2.27 `teacher` fail, R1 keep
  NTD). FedNTD `A>A[ntd]>A[ntd]` is no longer a claim comparator; it may be
  dropped from seeds 1-2.

## 2026-10-11: P2.29 h_plain: keep NTD (R1); the last round sets a Spider-BIRD trade-off

Evidence: nested `b4a52db`; contrasts recomputed locally from the published
predictions. `h_plain` = P2.27 Hinton v1 K2 plus one plain private round.

| h_plain minus | Spider | DK | BIRD |
|---|---|---|---|
| Hinton v1 A3 (R1) | +2.51 (53/27, p=.0049, Wald [0.83, 4.20]) | -1.50 (p=.18) | -3.32 (55/106, p<.001, Wald [-4.94, -1.71]) |
| FL A3 | +4.16 (85/42, p=.0002) | +2.80 (p=.082) | +14.28 (p<.001) |
| gold v1 A3 | +3.87 (76/36, p=.0002) | +3.18 (p=.021) | -1.43 (p=.19) |

Also Realistic +2.17 (p=.15) and SYN +2.61 (p=.007) against Hinton v1 A3.

- R1: **keep NTD**. The BIRD lower bound (-4.94) is below -2.0. The method
  stays v1; P2.31 runs the P2.27 arms.
- At Coder-1.5B, client NTD in the last round trades Spider for BIRD: -2.5
  Spider, +3.3 BIRD. At 0.5B it cost no Spider (P2.22: +0.48 pooled). The
  plain round adapts more to the private domain; NTD holds the post-K
  distribution, which carries BIRD.
- Descriptive only (not under any rule; the matched gold arm has NTD, so the
  rows against gold v1 and FL are not matched comparisons): h_plain is the
  best Spider model so far (71.76) and beats FL on Spider by 4.16.
- Reading for the paper: the last private round chooses the operating point
  on the Spider-BIRD frontier; neither h_plain (71.76, 39.96) nor v1 (69.25,
  43.29) dominates. Report both points on the Spider-BIRD plot.
- Process lesson: the publication push was rejected because a docs commit
  had been pushed to the nested remote after the server's last pull. Fixed by
  an allowlisted fetch and rebase on the server.

## 2026-10-11: Spider test as the confirmatory set, K-first baseline; rules R10-R11

Owner decision. Written before any model was evaluated on Spider test and
before any P2.29, `central` or seed 1-2 result was read.

Why: Spider dev and its derived sets (Realistic, SYN, DK; same 20 DBs) chose
every design decision across 30+ arms, so they act as a validation family
and their numbers are optimistic. The schedule grid (P2.18/P2.20, 0.5B) never
showed AKAKA better than K-first (Hinton K2AAA 63.93 vs AKAKA 62.57 Spider, no
contrast p<.1); AKAKA was kept by the 2026-10-07 default rule, and no
schedule contrast exists at Coder-1.5B. No published baseline from prior art
has been run.

- **R10, Spider test (confirmatory).** The official Spider 1.0 test set
  (2,147 questions, 40 DBs disjoint from train and dev; public since
  2024-02, CC BY-SA 4.0; precedent: OmniSQL, VLDB 2025, reports dev and test)
  becomes the Spider endpoint of every R7 claim (C1, teacher, R11), pooled
  over seeds 0-2. BIRD dev stays the BIRD endpoint (BIRD test is hidden).
  Spider test is evaluated only on final adapters of arms named in R7 and
  R11 and on `central`; it never selects a configuration, epoch, schedule or
  arm. Spider dev, Realistic, SYN and DK are reported as the validation
  family. R8 is unchanged (dev); the JOIN split on test is descriptive.
  Limitation to state: public sets may appear in pretraining data of the
  teacher and the student.
- **R11, K-first baseline (GPT-FL style; Zhang et al., arXiv 2306.02210:
  server-side training on non-private data, then standard FL).** Arm
  `hinton_k2aaa` at Coder-1.5B, alpha 0.1: one continuous two-epoch Hinton K
  on the 9,428 BIRD rows from the base model (P2.27 K recipe), then three
  plain FedAvg rounds; seeds 0-2. Same budget as the method (two K epochs,
  three private rounds). Comparison: method (per R1) minus `hinton_k2aaa`,
  co-primary criterion with R7 pooled tests on Spider test and BIRD dev.
  Pass: the paper may claim the method beats K-first at matched budget.
  Fail: AKAKA is presented as a design choice and K-first as an equivalent
  alternative; reported either way. If R1 keeps NTD, the contrast is method
  versus baseline, not the schedule alone.

## 2026-10-11: method study round 2, split audit, direction A final, rules R8-R9

Written before any P2.29, P2.27 `central`, or seed 1-2 result was read
(nested origin head `6fae58a`; none of those results published).

Split audit (CPU, split files and P2.18 predictions):

- The k5 alpha 0.1 split skews domains (cluster mix 0.58-0.70 total
  variation from the global mix) but is mild for FL: 5 clients, full
  participation, 1 local epoch, client sizes within 1.9x. With identifiers
  and values masked, each client's training SQL covers the SQL pattern of
  65.9-77.9% of Spider dev questions (full train 85.0%, random 5-way split
  75.7-78.8%). Federated Semantic Parsing (ACL 2023), one dataset per
  client, reports FedAvg 16-30 points below centralized training.
- At matched data passes the FL penalty is real (0.5B, alpha 0.5): central
  minus FL Spider +4.64 (E1-A1, p=.001), +4.84 (E2-A2, p=.001), +1.84 (E3-A3,
  p=.166; central peaked at E2). It sits on JOIN questions (E2-A2: 41.2 vs
  31.1) and extra-hard ones; no-JOIN is about equal. Likely cause: fewer
  effective optimizer steps per pass (FedAvg rounds of 69-129 local steps
  versus about 541 per central epoch), not client drift; FedNTD (+0.19) and
  FedProx do not help.

Method study (two independent reviewers, two rounds, CPU only): no new
method with a useful chance of meeting the owner criterion. Best surviving
candidate: K on BIRD plus public synthetic SQL rows (SynSQL-2.5M) chosen by
the federated student's excess loss, with base-model and random selectors as
controls; estimated 18% central screen pass, about 5% for the full
criterion (FL carry-over plus a significant selector effect on three seeds),
about 53 GPU-h. Private-aware KL weighting, schema-perturbation KD, dual
adapters and LwF-style K objectives were rejected (retention effects shrink
to about 7% after the next private round, P2.24).

Owner decision: direction A is final. The paper is a framework paper: claim
C1 (one SLM for both domains) already passes at seed 0; the teacher claim
rests on the pooled three-seed BIRD test (R7); C3 is the K-stage forgetting
mechanism. S1 (P2.30) and S2 (P2.34) leave the queue; R4-R6 stay recorded
but will not be applied. Another reading kept open: the 1.5B student may
already sit near the ceiling of this teacher and pool (Hinton - FL Spider
+1.65, ns).

Rules fixed now:

- **R8, JOIN subgroup (confirmatory, seeds 1 and 2 only).** Subset = Spider
  dev questions whose gold SQL contains the token `JOIN` (case-insensitive;
  408 of 1,034). Stack the paired outcomes of Hinton (method per R1) minus
  matched gold at the final model over seeds 1 and 2 (seed 0 generated the
  hypothesis and is excluded): exact conditional test on the summed
  discordant pairs. Supported if the difference is positive with p<.05. The
  no-JOIN subset and DK JOIN are reported with the same test, descriptive.
- **R9, FL penalty at matched passes (descriptive).** For P2.27 `central`,
  report Spider and BIRD central minus FL at E1-A1, E2-A2, E3-A3 with exact
  McNemar, overall and split by R8's JOIN subset. No decision depends on it;
  R3 (E3 - A3 >= 3.0) is unchanged. In the paper, the FL penalty is shown at
  matched passes, not only at the final checkpoint.

## 2026-10-11: exploratory: the teacher's gain is on multi-table JOIN questions

Post hoc subgroup analysis (not a fixed rule), on committed predictions only.
Split: gold SQL contains `JOIN` (Spider dev 408 of 1,034; BIRD dev 1,140 of
1,534). Hinton minus matched gold at the final model, exact McNemar:

| Run | Spider JOIN | Spider no-JOIN | DK JOIN |
|---|---|---|---|
| P2.17 1.5B-Instruct AKAKA | +4.7 (p=.007) | +0.3 | +5.7 (p=.004) |
| P2.18 0.5B AKAKA | +6.1 (p=.001) | 0.0 | +4.4 (p=.041) |
| P2.18 0.5B AKKAA | +4.7 (p=.020) | -0.8 | +3.1 |
| P2.20 0.5B K2AAA | +5.1 (p=.008) | 0.0 | +1.3 |
| P2.25 0.5B v1 | +8.6 (p<.001) | +0.6 | +4.8 (p=.043) |
| P2.27 Coder-1.5B v1 | +5.1 (p=.014) | -1.1 | +7.5 (p=.003) |

- The split was chosen after looking at P2.27; the other five runs were then
  checked with the same split. All six use the same Spider dev questions and
  the same teacher, so they are six setups, not six independent samples.
- P2.27 versus FL on JOIN: Hinton +8.1 (Spider), +9.6 (DK), +8.3 (SYN), +10.0
  (Realistic), all p<=.001; gold +2.2 to +4.8, none p<.05. On no-JOIN
  questions the public stage costs 1-5 points for both arms.
- Correction (same day, independent re-check of P2.27 predictions): the
  teacher does not fix schema linking on net. On Spider JOIN questions at
  A3, Hinton and gold pick the correct table set at the same rate (78.9 vs
  77.2, discordant 28/21, p=.39; regex proxy) and the same SQL skeleton
  (p=.47); "no such column" counts are 61 vs 61 (K2: 102 vs 106). The gain is
  in queries that execute but return a wrong result (Hinton 106, gold 130).
  The earlier "88 no such column fixes" counted one direction only. The JOIN
  concentration is shown for the final model on Spider-family sets, not on
  BIRD dev and not at the K stages.
- Reading: the overall Spider gap (+1.35 at P2.27) averages a stable +5 to +9
  JOIN gain with a zero or slightly negative no-JOIN effect. Not a claim:
  rule R8 (entry above) tests it on seeds 1 and 2.

## 2026-10-11: P2.28 published; descriptive audit of the headroom

Evidence: nested `238ee10` (summary and per-question JSONL). The summary
matches the server-local numbers below. Descriptive only; no rule depends on
it.

| Parent | Greedy | pass@1 (T 0.7) | pass@8 | Rescued | Rescues with 1-2 of 8 hits | Variant (strong norm.) | Non-gold correct SQL per question |
|---|---:|---:|---:|---:|---:|---:|---:|
| FL A2 | 77.0 | 71.0 | 90.0 | 132 | 52% | 55.4% | 1.32 |
| gold v1 K2 | 66.9 | 61.1 | 84.7 | 180 | 51% | 63.9% | 1.81 |
| Hinton v1 K2 | 71.9 | 67.2 | 85.6 | 137 | 50% | 61.6% | 1.67 |

- One sample at T 0.7 is 5-6 points below greedy; the headroom exists only
  with eight samples and a gold oracle.
- Half of the rescued questions are hit by 1 or 2 of 8 samples. 22-31% of
  rescues have an empty or all-zero gold result (26% of all rows), where a
  wrong SQL can match by chance.
- Strong normalization (aliases, `count(...)`, quotes, spacing) lowers
  variant by 10-16 points; G3 still passes.
- K-stage forgetting is shallow: from FL A2 to gold K2, greedy falls 10.1
  points but pass@8 only 5.3; for Hinton K2, 5.1 and 4.4. The private
  domain is still reachable by sampling after K, consistent with the repair
  reading in A1.

## 2026-10-11: A1 churn (rule R2): no teacher-specific erasure

Evidence: P2.27 predictions in nested `5604e61` and `767d1e5`, row-matched by
`row_id`; CPU only, run after R2 was committed (paper `6b1e1c8`). T = rows
Hinton K2 right and gold K2 wrong; T' = the reverse.

| Set | T | Hinton A3 loses on T | T' | gold A3 loses on T' | Difference | Fisher p |
|---|---:|---:|---:|---:|---:|---:|
| BIRD dev | 161 | 42 (26.1%) | 91 | 29 (31.9%) | -5.8 | .38 |
| Spider dev | 89 | 14 (15.7%) | 58 | 16 (27.6%) | -11.9 | .096 |

- R2: **not supported** on BIRD (the judged set): Hinton keeps its
  teacher-only rows at least as well as gold keeps its gold-only rows. The
  narrowing Hinton - gold gap after A3 is symmetric churn plus gold catching
  up (gold A3 is right on 26.7% of BIRD T and 60.7% of Spider T), not erasure.
- This supports the other reading: gold CE forgets the private domain more
  during K and the private round repairs it (claim C3 in the direction plan).
- By R5, ExST cannot become the main method. S1 (P2.30) may still run as an
  analysis screen; it now ranks below P2.31-P2.33.

## 2026-10-11: P2.27 decision, P2.28 G3, paper direction A and rules fixed before results

Evidence: nested `5604e61` (fedntd and Hinton v1 to A3). Every number below
was recomputed from the published predictions (exact McNemar, Wald 95%).
`central` is still running and has not been read.

| Arm, A3 | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| FL | 67.60 | 59.65 | 53.68 | 53.27 | 25.68 |
| FedNTD | 67.79 | 57.09 | 53.38 | 51.96 | 24.32 |
| gold v1 | 67.89 | 59.06 | 55.61 | 52.90 | 41.40 |
| Hinton v1 | 69.25 | 60.83 | 56.38 | 57.57 | 43.29 |

P2.27 decision by the rule fixed 2026-10-10:

- `teacher` (Hinton v1 - gold v1): **fail**. Spider +1.35 (p=.23, Wald
  [-0.70, 3.41]); BIRD +1.89 (p=.076). DK +4.67 (p<.001) is outside the rule.
- `server_kd` (Hinton v1 - FedNTD): **pass**. BIRD +18.97 (p<.001); Spider
  +1.45, Wald lower -0.89. Robustness: DK +5.61 (p<.001), SYN +3.00 (p=.019),
  Realistic +3.74 (p=.037).
- `server_kd_spider_gain`: **fail** (p=.26).
- FedNTD - FL: Spider +0.19 (p=.91), BIRD -1.37 (p=.044), Realistic -2.56
  (p=.047). FedNTD does not help at 1.5B.
- Hinton - gold by stage: Spider +3.48 (K1, p=.002), +2.13 (A2, p=.043),
  +3.00 (K2, p=.013), +1.35 (A3); BIRD +1.83, +0.07, +4.56 (p<.001), +1.89.
  Two readings, not yet separated: private rounds erase teacher-specific
  knowledge, or gold CE forgets Spider more during K and the private round
  repairs both to the same ceiling. Rule R2 below decides.

P2.28 (G3, fixed before the run): **pass**. From the server-local summary
(later published in nested `238ee10`): greedy / pass@8 / headroom / variant = FL A2
77.0 / 90.0 / 13.0 / 65.3; gold v1 K2 66.9 / 84.7 / 17.8 / 76.8; Hinton v1 K2
71.9 / 85.6 / 13.7 / 77.4. Measured on training questions the adapters have
seen, so it is a ceiling, not a dev forecast.

Owner decision: paper direction A. Method v2 (ExST,
`paper/archive/directions_2026-10/method_v2_proposal_2026-10-11.md`) is not the main direction;
it becomes the main method only through rule R5. Literature check
(2026-10): no federated Text-to-SQL work with a server LLM teacher found;
PubSwap (arXiv 2604.12160) and FedMOA (arXiv 2602.00453) already cover
federated verifiable-reward training with LoRA for math, medical and code.

Rules, fixed 2026-10-11 before any of the results they judge (P2.29, the
churn analysis, `central`, S1, S2, seeds 1 and 2):

- **R1, NTD (P2.29).** `h_plain` (Hinton v1 K2, one plain A3) - Hinton v1 A3,
  seed 0: if both the Spider and the BIRD Wald lower bounds are above -2.0,
  drop client NTD (the method becomes Hinton AKAKA, matched gold becomes gold
  AKAKA); otherwise keep v1.
- **R2, churn (CPU, P2.27 predictions).** T = rows Hinton K2 right and gold
  K2 wrong; T' = rows gold K2 right and Hinton K2 wrong. "Private rounds erase
  teacher-specific knowledge" is supported on a set if Hinton's A3 loss rate on
  T minus gold's A3 loss rate on T' is at least 10 points with Fisher exact
  p<.05. Judged on BIRD dev; Spider dev reported.
- **R3, FL penalty (`central`).** Central E3 - FL A3 Spider >= 3.0 points
  makes client drift a target worth a method; below that, drift is analysis
  only.
- **R4, ExST screen (S1, P2.30).** From FL A2: A3[ExST] (k=8, T=0.7, top-p
  1.0, m=4, gold kept, FedAvg weights from original client sizes) versus
  A3 on gold repeated to the same number of steps (`fl_dup`). Pass: Spider
  difference >= +1.0 point and BIRD Wald lower bound > -2.0. One
  configuration, no tuning on reported sets. Fail closes ExST.
- **R5, promotion.** ExST becomes the main method only if R2 supports
  erasure, R3 >= 3.0 and R4 passes. Otherwise direction A stands and ExST
  enters the paper as analysis.
- **R6, execution-gated KD (S2, P2.34).** Same schedule as Hinton v1 to A2,
  K1 distils teacher logits only on the 5,319 teacher-correct rows and uses
  gold CE on the rest. Pass at A2 versus Hinton v1 A2: Spider >= +1.0 and BIRD
  Wald lower bound > -2.0. Fail closes it. No published source gates logit KD
  by execution; state it as our choice.
- **R7, confirmation (seeds 0-2, fixed split, training RNG varies).** For
  each claim, stack the paired per-question outcomes of three seeds: exact
  conditional test on the summed discordant pairs, CI from a bootstrap that
  resamples questions. (Replaced by the question-clustered test, R13.) C1 (method versus FedNTD and versus FL) and the teacher
  claim (method versus matched gold) use the co-primary criterion of
  2026-10-08 with these pooled tests. Single-seed tests are descriptive.

## 2026-10-10: P2.27 partial: base, FL and gold v1 complete, Hinton v1 to A2

Evidence: nested `767d1e5` (mid-run publication; no decision yet, the rule
needs `fedntd` and Hinton v1 A3). Seed 0, Coder-1.5B, alpha 0.1.

| Arm / stage | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| base | 59.19 | 46.26 | 45.94 | 47.66 | 21.32 |
| FL A1 / A2 | 65.57 / 68.28 | | | | 22.62 / 24.38 |
| FL A3 | 67.60 | 59.65 | 53.68 | 53.27 | 25.68 |
| gold v1 K1 / A2 / K2 | 58.70 / 66.34 / 60.54 | | | | 40.35 / 41.59 / 39.77 |
| gold v1 A3 | 67.89 | 59.06 | 55.61 | 52.90 | 41.40 |
| Hinton v1 K1 / A2 | 62.19 / 68.47 | | | | 42.18 / 41.66 |

- Teacher on Spider, as at 0.5B: Hinton - gold at K1 +3.48 (p=.0016), at A2
  +2.13 (p=.043); BIRD equal at A2 (+0.07).
- Gold v1 A3 - FL A3: Spider +0.29 (p=.87, Wald [-1.99, 2.57]), BIRD +15.71
  (p<.001). At matched private rounds Hinton v1 A2 - FL A2 is Spider +0.19
  (p=.94), BIRD +17.28.
- BIRD no longer drops in the private round after K (gold 40.35 -> 41.59,
  Hinton 42.18 -> 41.66; 0.5B lost 4-7 points). Size and client NTD are
  confounded: P2.27 has no plain A after K.
- FL peaks at A2 (A3 - A2 Spider -0.68, p=.47).

## 2026-10-10: P2.27 Coder-1.5B on the alpha 0.1 split queued, rule fixed before results

Owner decision: switch the student to Qwen2.5-Coder-1.5B-Instruct and the
clients to the k5 alpha 0.1 split, for a stronger federated story. Code:
nested `80bae67`; split: nested `02dabf4`. No memory probes (owner decision).

Why alpha 0.1: at alpha 0.5 the FL penalty was small (0.5B: central 59.38 vs
FL 57.54, 1.84 points), and each client spanned 9-13 of 20 domain clusters
with mild SQL-construct skew. At alpha 0.1 each client spans 6-8 clusters,
10 of 20 clusters belong to one client (alpha 0.5: 3), client sizes
1,097-2,061. Construct skew stays moderate (JOIN 30-66%, nested 10-27%).

Arms (seed 0): `base`, `fl` (AAA), `fedntd` (A, A[ntd], A[ntd]), `gold_v1`
and `hinton_v1` (A, K, A[ntd], K, A[ntd]), `central` (Spider E3). FedNTD
(Lee et al., NeurIPS 2022) is the published non-IID FL baseline, so `fedntd`
is also the method without server KD.

Rule, fixed before any P2.27 result, final models, exact McNemar and Wald 95%:

- `teacher` (role-based, as P2.25): `hinton_v1` - `gold_v1` passes if Spider
  gain with p<.05 and BIRD Wald lower bound > -2.0.
- `server_kd` (co-primary criterion, component claim): `hinton_v1` - `fedntd`
  passes if BIRD gain with p<.05 and Spider Wald lower bound > -2.0.
- `server_kd_spider_gain` (secondary, the federated claim): `hinton_v1` -
  `fedntd` Spider gain with p<.05, i.e. server KD improves the private domain
  beyond the best FL baseline under strong heterogeneity.
- Descriptive only: FL penalty (`central` - `fl` Spider), `base` row,
  per-stage trajectories, rounds to reach the final FL Spider.
- Not testable by P2.27 alone: whether the KD gain grows with heterogeneity.
  That needs Coder-1.5B at alpha 0.5; the 0.5B alpha 0.5 rows differ in model.

## 2026-10-10: P2.25 decision and P2.26 centralized reference

Evidence: nested `d826269` (P2.25), `849f0dd` (P2.26). Seed 0, final models.

| Arm | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| central_mix E3 (Spider+BIRD, no privacy) | 62.96 | 50.20 | 48.45 | 48.04 | 33.12 |
| Hinton v1 (Hinton K + client NTD) | 63.44 | 53.15 | 50.00 | 47.10 | 30.12 |
| gold v1 (gold K + client NTD) | 59.67 | 48.43 | 47.00 | 45.23 | 28.36 |
| Hinton AKAKA (no NTD) | 62.57 | 52.17 | 50.48 | 47.85 | 28.88 |
| central Spider only | 59.38 | 45.87 | 43.42 | 44.30 | 13.62 |
| FL AAA | 57.54 | 47.24 | 41.49 | 42.80 | 14.34 |

P2.25 decision (role-based rule, LAB_LOG 2026-10-08):

- `teacher_with_ntd`: pass. Hinton v1 - gold v1: Spider +3.77 (p=.001,
  Wald [1.55, 5.99]), BIRD +1.76 (p=.073, lower -0.09). Robustness also favours
  the teacher: Realistic +4.72 (p=.005), SYN +3.00 (p=.007), DK +1.87 (p=.22).
- `ntd_hinton`: fail. BIRD +1.24 (p=.14).
- `ntd_gold`: fail on Spider non-inferiority only. BIRD +2.61 (p=.002), Spider
  -0.48 with Wald lower -2.43.
- The two-seed pooled NTD BIRD effect (+1.89, p=.004, P2.22) stays the NTD
  evidence; at seed 0 alone it does not reach p<.05 for Hinton.

P2.26 reading (fixed 2026-10-08), arm minus central_mix at E3:

- Hinton v1: Spider +0.48 (p=.77, Wald [-2.07, 3.03]); BIRD -3.00 (p=.010).
  Both are `below` by the rule: Spider misses the -2.0 non-inferiority margin
  by 0.07 at one seed; BIRD is a real gap.
- Gold v1: Spider -3.29 (p=.018), BIRD -4.76 (p<.001). The teacher closes the
  Spider gap to the centralized reference and narrows the BIRD gap.
- Exposure (stated, not used for the decision): central_mix sees BIRD 3 times,
  the AKAKA chains twice. Central E2 (2 passes of each) is 63.25 / 31.81.
- Central training: 13.5 h, peak reserved 20.2 GiB, 1.12 examples/s.
