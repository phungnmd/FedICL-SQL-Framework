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

## Where we are (2026-10-23)

- Exploration at seed 0 on the dev sets under the simplified rules (entry
  2026-10-12); the paper story is fixed in a dated entry before any seed 1-2
  run or Spider test evaluation. Primary metric Spider EX (owner,
  2026-10-16). Findings, open questions and rules, including the Q3 floor
  and aim: [`RESEARCH_STATE.md`](RESEARCH_STATE.md).
- Published: P2.27 (`5767704`), P2.28, P2.29, P2.36 (`31a568e`); P2.37
  `hinton_k2aaa`, `gold_k2aaa`, `central_mix` (`5b01fc1`), `local`
  (`3e0dc0b`); P2.38 (`d326854`), P2.39 pilot (`4acba5b`), P2.40
  (`640d534`), P2.42 (`c40e090`); P2.43 `hinton_k2aaa_rev` K2 and A1
  (`91a9ea5`).
- P2.41 not run (its condition failed). Deferred: the P2.37 `akaka_plain`
  pair. P2.43 `hinton_k2aaa_rev` A3 and `gold_k2aaa_rev` K2/A1 evaluated,
  not committed yet. P2.44 `self_k2aaa` complete (entry 2026-10-24, not
  committed yet). P2.43 both chains to A3 and `fl_bird` complete (entry 2026-10-24, not
  committed yet); running: GPU 0 P2.43 `central_bird`; GPU 1 idle. Plan and readings: entry 2026-10-23.
  P2.46 and P2.41 deferred; P2.47 client replay published (`80d1091`, entry 2026-10-24).
  P2.48 compact replay and server learning published (nested `8b79530`, entry 2026-10-25).
  P2.49 matched no-teacher pipeline built, readings fixed (entry 2026-10-25).
  P2.49 `gmixkd50_k2aaa` stopped by the owner to free GPU 1; P2.50 placement controls built (entry 2026-10-25).
  P2.49 `gmixgold_k2aaa` published (nested `db2cc09`, entry 2026-10-26); `gmixkd50_k2aaa` and P2.50 `fslm_k2sasasa` dropped.
  P2.50 `k2plus_aaa` published (nested `015429c`, entry 2026-10-26).
  P2.51 execution-filtered replay built, client drift audit done (nested `4e4641e`, entry 2026-10-26); freeze after P2.51.
  P2.52 reverse-roles replay built (nested `1838b63`, entry 2026-10-26); the freeze does not wait for it.
  P2.51 complete (analyzed on the server, not committed yet; entry 2026-10-26): the row filter does not help; `mixkd50_k2aaa` stays.
  Freeze entry drafted (2026-10-26), awaiting owner approval.

## 2026-10-27: P2.54 SynSQL-2.5M as the public pool built

Owner decision (2026-10-27): no limitation story for the role swap; find a
public dataset that suits Spider clients and try SynSQL-2.5M (Li et al.,
OmniSQL, arXiv 2503.02240, Apache-2.0), without its external knowledge,
since a public pool closer to Spider may help Spider more.

Pool (nested `5b47a89`, `processed_data/protocol_v2/SYNSQL/pool_tok508k`):
SynSQL samples ranked by sha256 of their index at the pinned revision; kept
when they have no external knowledge, no database or question shared with
Spider or BIRD, a new question, executable gold SQL and a sequence under
7,168 tokens; stopped at the BIRD pool's 508,285 SQL target tokens (so the
teacher cache and KD signal have the BIRD size, about 155 GB instead of 440
GB for 9,428 SynSQL rows). Result: 3,336 rows over 3,027 databases; Simple
341, Moderate 997, Complex 1,134, Highly Complex 864. The SynSQL databases
hold about two rows per table (21% of tables empty), so no EX is measured
on SynSQL; BIRD dev is an unseen domain in this setting.

P2.54 (`scripts/run_p254_synsql_public.py --seed N`): the P2.53 recipes of
`hinton_k2`, `gold_k2`, `mixkd50_k2aaa`, `hinton_k2aaa` and
`gmixgold_k2aaa`, with only the public pool, its profile (`synsql`, no
evidence) and the teacher cache swapped. Final adapters on Spider test and
the five dev sets. Seed 0 first; seeds 1-2 after it.

## 2026-10-27: owner: rules are guidance; E3 leaves the confirmation

Owner decision (2026-10-27): the selection and reporting rules are guidance,
not gates; choose what makes the paper strongest for a Q3 journal. E3
(reverse roles) is removed from the frozen confirmation after the P2.52 A3
result was read; it gets no seeds 1-2 and becomes exploratory. Its seed-0
result may appear in the paper as a boundary condition (public-domain
retention in both directions, private-domain gain only with BIRD public) or
stay out, decided at writing; if it stays out, the paper makes no claim
about swapped roles. The main setting (C1-C5, seeds 0-2, Spider test) and
E1, E2 are unchanged. One reverse variant (replay ratio 0.1) is an option
for a free GPU after the main seeds, not queued.

## 2026-10-27: P2.52 reverse-roles replay: no private-domain gain

Evidence: nested `90fc918`, `audits/protocol_v2/p252_reverse_replay_s0/summary.md`.
Seed 0, dev sets, exact McNemar. Reverse roles: BIRD private (primary),
Spider public.

| Arm (A3) | BIRD | Spider | Realistic | SYN | DK |
|---|---:|---:|---:|---:|---:|
| `mixkd50_k2aaa_rev` | 39.63 | 71.18 | 62.40 | 58.32 | 57.01 |
| `hinton_k2aaa_rev` | 41.33 | 64.89 | 56.10 | 54.16 | 54.39 |
| `gold_k2aaa_rev` | 40.22 | 64.70 | 56.10 | 52.13 | 52.34 |
| `fl_bird` | 39.18 | 60.44 | 51.77 | 50.87 | 47.85 |

- Against `hinton_k2aaa_rev`, BIRD -1.04 / -2.02 / -1.69 at A1-A3
  (A3 76/102, p=.061, CI [-3.40, 0.01]); Spider +6.29 at A3 (p<.001).
  Against `gold_k2aaa_rev` BIRD -0.59 (p=.57); against `fl_bird` +0.46
  (p=.68).
- The replay keeps the public domain in both directions (main setting BIRD
  +6.26, here Spider +6.29 over the same chain without replay); the
  private-domain gain of the main setting (Spider +1.55, p=.068) does not
  carry over: here the private domain is level or slightly lower.
- Losses spread over all BIRD difficulty levels; execution errors 16.2% vs
  14.5% (wrong-table columns, extra joins). Post hoc, one seed: a
  hypothesis, not a finding.
- E3 stays as frozen (seed 0 counts, no tuning); seeds 1-2 decide its
  wording.

## 2026-10-26: P2.53 confirmation runner built

Owner approved the freeze (2026-10-26). P2.53 (nested `23e97c0`,
`scripts/run_p253_confirmation.py --seed N`) runs the frozen comparison:
the seed-0 recipes of `hinton_k2aaa`/`gold_k2aaa` K2 (P2.37),
`mixkd50_k2aaa` (P2.48), `gmixgold_k2aaa` (P2.49), `k2plus_aaa` (P2.50)
and the FedCoLLM-style A > K > A > K > A > K, with only `--seed` changed.
At each seed `k2plus_aaa` trains exactly the rows the method replays at
that seed. Seed 0 reuses the published adapters and dev evaluations; its
FedCoLLM-style arm is the P2.37 `hinton_akaka_plain` chain plus one K.
Every final adapter is evaluated on Spider test and the five dev sets; no
intermediate endpoint is evaluated at seeds 1-2.

Implementation of the frozen test, fixed before any confirmation result:
the Holm family holds five p values, BIRD dev for C2, C3 and C4 and both
C5 branches (Spider test and BIRD dev), which is stricter than one p per
claim. Runbook: PIPELINE_NEXT P2.53.

## 2026-10-26: FREEZE: method, comparators, seeds, claims

Status: approved 2026-10-26 by the owner. Binding: nothing below changes
after a seed 1-2, Spider test or FedCoLLM-style result is read.

Selection record (R13): seed 0, Spider dev, BIRD dev and the three Spider
variants; 17 federated configurations of the 1.5B student evaluated per round
(Spider and BIRD dev) and at the final round (all five sets), from P2.27 to
P2.51; rules of 2026-10-12 and 2026-10-26.

### Method (fixed)

`mixkd50_k2aaa`, exactly the P2.48 recipe: server warm-start 2 epochs over
the 9,428 BIRD rows with 0.5 gold CE + 0.5 T^2 KL (T=2) to the frozen
Qwen2.5-Coder-7B; 3 FedAvg rounds (1 local epoch, lr 2e-4, LoRA r16) on the
Spider `alpha_0.1/k5` split; every client replays 20% of its private row
count from a fixed seeded 2,000-row BIRD subset on 0.5 gold CE + 0.5 KL to
the teacher's top-50 tokens plus tail (T=2). Student
Qwen2.5-Coder-1.5B-Instruct. Only `--seed` changes between seeds (LoRA
init, data order, replay subset and samples); the client split stays fixed.

### Main setting: comparators (all seeds 0, 1, 2)

- `gmixgold_k2aaa`: matched pipeline without teacher (gold warm-start, gold
  replay).
- `hinton_k2aaa`: server KD warm-start + FedAvg.
- `k2plus_aaa`: the same replay rows trained at the server.
- FedCoLLM-style (Fan et al., arXiv 2411.11707): A > K > A > K > A > K,
  server KD after every round including the last, as in its Algorithm 1;
  each K is one epoch over the BIRD pool with gold CE + KL to the teacher
  (FedCoLLM: CE + lambda KL; here 0.5/0.5, lambda = 1 up to scale, as in our
  server KD). FedCoLLM also tunes the LLM with LoRA (mutual KD); here the
  teacher stays frozen (one-way), because updating the 7B at the server
  invalidates the logit cache and does not fit the compute budget; the paper
  states this difference. Its first five stages are the P2.37
  `hinton_akaka_plain` chain; the final model is the one after the last K.
  Its seed 0 has not been run; it counts as a confirmation seed because it
  played no part in selection.
- Reference rows without claims: FedAvg, base model, teacher zero-shot.

Seed 0 adapters of the method and the first three comparators are reused;
seeds 1 and 2 are trained new. Every arm is evaluated at A3 on Spider test
(2,147, primary), Spider dev, Realistic, SYN, DK and BIRD dev.

### Test

Pooled over 3 seeds with the question-clustered test (R13): per-question
mean of the paired EX difference, normal test across questions, two-sided,
95% CI. Non-inferiority margin 2.0 EX points (lower 95% bound > -2.0).
Secondary claims C2-C5 use Holm correction at family alpha .05. Number of
seeds fixed at 3 (power check: 5 seeds add little because the cross-seed
correlation is about 0.6).

### Claims and wording per outcome

- C1 (primary): method > `gmixgold_k2aaa` on Spider test EX.
  Significant and positive: "The server teacher raises private-domain EX by
  X points over the matched pipeline without a teacher." Otherwise: "Spider
  test EX differs by X (95% CI [a, b]); the difference is not significant",
  with no teacher-contribution claim on Spider.
- C2: method > `gmixgold_k2aaa` on BIRD dev EX with Spider test
  non-inferior. Holds: "the teacher also raises public-domain EX by X".
- C3: method > `hinton_k2aaa` on BIRD dev EX with Spider test
  non-inferior. Holds: "replaying teacher targets at the clients keeps the
  public-domain gain that plain FedAvg rounds lose".
- C4: method > `k2plus_aaa` on BIRD dev EX with Spider test non-inferior.
  Holds: "the same rows, teacher and steps help only when mixed into the
  client rounds, not when spent on more server KD".
- C5: method against the FedCoLLM-style arm. Spider test significantly higher:
  "outperforms the FedCoLLM-style schedule"; Spider non-inferior and BIRD
  significantly higher: "matches it on the private domain and exceeds it on
  the public domain"; otherwise the numbers are reported without a claim.
- Ranking (descriptive): the pooled Spider test EX of every arm is reported;
  "highest of the evaluated federated configurations" is written only if the
  method's point estimate is the highest.
- Any claim that fails is reported with its numbers; no other claim is
  added after the results are read.

### Extension settings (pre-registered, no tuning, seeds 0, 1, 2)

Arms in each: the method, the matched pipeline without teacher, the server
KD warm-start + FedAvg, all with the main recipe.

- E1 non-IID alpha 0.5: Spider `alpha_0.5/k5` split. Primary Spider test.
- E2 student Qwen2.5-Coder-0.5B-Instruct on `alpha_0.1/k5` (the BIRD
  teacher cache reused under the cross-student audit). Primary Spider test.
- E3 reverse roles: removed from the confirmation by the owner on
  2026-10-27, after the P2.52 A3 result (entry of that date). It stays
  exploratory; no seeds 1-2.
- Claims per setting: the C1 and C3 tests on that setting's primary metric,
  each reported with its numbers; wording "consistent with the main
  setting" only where both directions match and C1 is significant.

## 2026-10-26: P2.51: execution-filtered replay does not help; the unfiltered method stays

Evidence: P2.51 analysis on the server (`audits/protocol_v2/p251_exec_filtered_replay_s0/summary.md`),
not committed yet; it is published after the P2.52 lane stops. Seed 0, dev
sets, exploratory, exact McNemar.

| Arm | A1 Spider / BIRD | A2 Spider / BIRD | A3 Spider | Realistic | SYN | DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|---:|---:|
| `mixkd50_k2aaa` | 69.73 / 41.92 | 72.82 / 43.74 | 74.08 | 63.58 | 58.70 | 57.20 | 44.78 |
| `xmixkd50_k2aaa` (filtered) | 70.21 / 42.11 | 72.92 / 43.94 | 73.02 | 62.40 | 59.09 | 58.50 | 44.26 |

- Filtered minus unfiltered at A3: Spider -1.06 (10/21, p=.071), BIRD -0.52
  (p=.40); level at A1 and A2. Restricting the replay KL to teacher-correct
  rows gives no gain; the 0.5 gold CE on every replay row seems enough to
  offset the teacher's wrong targets. Method unchanged: `mixkd50_k2aaa`.
- Against the matched pipeline without teacher, the filtered variant gives
  Spider +1.45 (p=.15) and BIRD +3.00 (p=.003), against +2.51 and +3.52 for
  the selected method. Two near-identical variants differ by about 1 Spider
  point in their teacher margin, so the seed-0 margin of the selected method
  is likely optimistic; the confirmation power check should use the
  half-effect scenario (Spider power 0.63 at three seeds), not the seed-0
  effect.

## 2026-10-26: P2.52 client replay in the reverse roles built

Owner decision (2026-10-26): GPU 1 is idle, so check whether the method also
works in the reverse roles (P2.43: BIRD at the clients, Spider at the server,
primary metric BIRD EX). Exploratory; the freeze does not wait for it. If
BIRD gains, the freeze may add a reverse-roles claim; if not, the paper
claims the main setting only.

P2.52 (nested `1838b63`): `mixkd50_k2aaa_rev` repeats the three P2.43
`hinton_k2aaa_rev` private rounds from its published Hinton K2 adapter; each
client also replays 20% of its private row count from a fixed 2,000-row
seeded subset of the 8,659 Spider training rows, on 0.5 CE + 0.5 KL to the
P2.43 Spider teacher cache (top-50 plus tail, T=2). Comparators: P2.43
`hinton_k2aaa_rev` (A3 BIRD 41.33, Spider 64.89), `gold_k2aaa_rev` and
`fl_bird`. Seed 0, dev sets.

## 2026-10-26: P2.51 execution-filtered replay built; client drift audit shows no teacher effect on client agreement

Owner decision (2026-10-26): before the freeze, try one change that could
alter the method, and the CPU drift audit; no A4 extension. In the freeze the
method is claimed as the best configuration so far, including against
`k2plus_aaa`.

P2.51 (nested `7892d0d`, shared option `ab62ce6`): `xmixkd50_k2aaa` repeats
`mixkd50_k2aaa` from the same Hinton K2 adapter, except that the replay pool
is first restricted to the 5,319 BIRD training rows whose teacher SQL
executes to the gold result (the SeqKD exmatch file, matched by
`source_row_id`); the 2,000-row seeded subset is drawn from them. Ratio,
0.5 CE + 0.5 top-50 tail KL and T=2 are unchanged, so the teacher's KL no
longer acts on rows where its SQL is wrong. Grounding: selection by
correctness (STaR, Zelikman et al., 2022; RFT, Yuan et al., 2023), here by
SQL execution as in the SeqKD pool. Seed 0, dev sets, exploratory.

Client drift audit (nested `30c45e0`, `audits/protocol_v2/client_drift_s0/`),
from the published per-round `delta_stats` (factor-space cosine of the client
LoRA updates) and FedAvg weights:

| Arm | A1 cosine / dispersion | A2 | A3 |
|---|---|---|---|
| `hinton_k2aaa` | 0.388 / 0.490 | 0.036 / 0.761 | 0.004 / 0.787 |
| `gmixgold_k2aaa` | 0.385 / 0.490 | 0.049 / 0.750 | 0.014 / 0.777 |
| `mixgold_k2aaa` | 0.337 / 0.529 | 0.051 / 0.748 | 0.021 / 0.770 |
| `mixkd50_k2aaa` | 0.314 / 0.547 | 0.056 / 0.744 | 0.018 / 0.774 |
| `k2plus_aaa` | 0.371 / 0.504 | 0.037 / 0.761 | 0.001 / 0.789 |

- Replay of any kind makes later client updates slightly more aligned
  (A3 dispersion 0.770-0.777 against 0.787-0.789 without replay), as
  shared public data predicts (Zhao et al., 2018). The teacher adds nothing
  on this measure: `mixkd50` and `mixgold` are level at every round.
- The teacher's effect therefore does not run through client agreement; the
  account of where its knowledge goes stays the one in the evaluations
  (server-side BIRD gains are lost in the next private round; replayed at
  the clients they stay). The drift audit is not a paper claim.

## 2026-10-26: P2.50: the same replay rows trained at the server keep Spider but lose the BIRD gain

Evidence: nested `015429c` (`audits/protocol_v2/p250_server_replay_rows_s0/summary.md`).
Seed 0, dev sets, exploratory, exact McNemar. `k2plus_aaa` = Hinton K2, one
more Hinton stage at the server on the 5,193 rows the `mixkd_k2aaa` clients
replayed, then three plain rounds. `fslm_k2sasasa` was not run (owner,
2026-10-26).

| Arm | S Spider / BIRD | A1 Spider / BIRD | A2 Spider / BIRD | A3 Spider | Realistic | SYN | DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| `hinton_k2aaa` | | 71.57 / 36.77 | 71.86 / 38.66 | 72.53 | 61.81 | 56.38 | 58.32 | 38.53 |
| `k2plus_aaa` | 61.99 / 42.96 | 71.28 / 37.87 | 72.63 / 38.66 | 73.21 | 62.01 | 58.80 | 57.57 | 37.81 |
| `mixkd50_k2aaa` | | 69.73 / 41.92 | 72.82 / 43.74 | 74.08 | 63.58 | 58.70 | 57.20 | 44.78 |

- Placement, `mixkd50 - k2plus` at A3: Spider +0.87 (42/33, p=.36),
  Realistic +1.57, SYN -0.10, DK -0.37 (all n.s.), BIRD +6.98 (185/78,
  p<1e-10). The full-target `mixkd_k2aaa` gives the same picture (Spider
  +0.77, BIRD +7.43).
- The extra server stage lifts BIRD to 42.96 at S; the first private round
  takes it back to 37.87 and A3 ends at 37.81, level with `hinton_k2aaa`
  (-0.72, p=.36). Spider +0.68 over `hinton_k2aaa` (p=.40); SYN +2.42
  (p=.007) is a post hoc subgroup on one seed.
- Under the primary-metric rule (Spider level, higher BIRD wins)
  `mixkd50_k2aaa` stays the candidate. The noted prediction (A3 BIRD about
  40-41) was too high: the BIRD gain of server KD on these rows is lost
  completely.
- Alternative reading: on Spider the placement makes no measurable
  difference at seed 0; the replay's measured value is keeping the
  public-domain skill, and the method's Spider margin over the matched
  no-teacher pipeline (+2.51, P2.49) comes mostly from the teacher at K2.

GPU: S 20,277 MB, 2.17 h for 5,193 rows; A rounds 14,527 MB.

## 2026-10-26: P2.49: against the matched pipeline without a teacher, the candidate gains +2.51 Spider and +3.52 BIRD

Evidence: nested `db2cc09` (`audits/protocol_v2/p249_gold_k2_replay_s0/summary.md`).
Seed 0, dev sets, exploratory, exact McNemar. `gmixgold_k2aaa` = gold K2
plus the same three replay rounds on gold CE (no teacher anywhere).

| Arm | K2 objective | Replay objective | A1 Spider / BIRD | A2 Spider / BIRD | A3 Spider | Realistic | SYN | DK | A3 BIRD |
|---|---|---|---:|---:|---:|---:|---:|---:|---:|
| `gold_k2aaa` | gold | none | 70.12 / 40.74 | 69.83 / 39.90 | 70.41 | 61.22 | 56.38 | 52.34 | 40.03 |
| `gmixgold_k2aaa` | gold | gold | 69.73 / 42.44 | 70.41 / 42.44 | 71.57 | 62.01 | 55.13 | 53.83 | 41.26 |
| `mixgold_k2aaa` | Hinton | gold | 70.41 / 39.11 | 71.95 / 40.29 | 73.21 | 62.20 | 58.51 | 57.01 | 40.74 |
| `mixkd50_k2aaa` | Hinton | teacher top-50 | 69.73 / 41.92 | 72.82 / 43.74 | **74.08** | 63.58 | 58.70 | 57.20 | **44.78** |

- Whole teacher contribution, `mixkd50 - gmixgold` at A3: Spider +2.51
  (59/33, p=.009), SYN +3.58 (p<.001), DK +3.36 (p=.010), Realistic +1.57
  (p=.39), BIRD +3.52 (149/95, p<.001). At A1 the two are level (Spider
  45/45); the gap opens at A2 (+2.42, p=.009).
- The two placements of the teacher add up and split by domain: at K2
  (`mixgold - gmixgold`) Spider +1.64 (p=.068), DK +3.18, BIRD -0.52; in the
  replay (`mixkd50 - mixgold`) Spider +0.87 (p=.18), BIRD +4.04 (p<.001).
  1.64 + 0.87 = 2.51.
- Replay without a teacher (`gmixgold - gold_k2aaa`) at A3: Spider +1.16
  (p=.22), BIRD +1.24 (p=.23). The Spider gain of the method comes from the
  teacher, not from replaying public data.
- Reading noted before the run (now a note under the 2026-10-26 rule): the
  first case holds (Spider +1.0 or more, BIRD not lower).

This is the seed-0 teacher contribution against the matched gold pipeline
that the Q3 floor asks for; it must hold in the three-seed confirmation.

## 2026-10-26: owner rule: lean exploration, strongest story; P2.48-P2.50 readings are notes

Owner decision (2026-10-26), now in AGENTS.md (evidence rules): during
exploration run only controls that could change the method or that reviewers
will certainly ask for, with no criteria fixed before the run; the paper
carries the strongest supported story and leaves out weak or neutral results
that test no claim it makes; rule 3 (disclose) is narrowed to stating that
dev numbers are exploratory and how many variants and checkpoints were
evaluated. Fixed criteria remain only in the freeze entry before seeds 1-2
and Spider test. The "readings fixed before the run" in the P2.48, P2.49 and
P2.50 entries were written against the 2026-10-12 rule 1 (no pass/fail rule
before an exploratory run); they stay as notes of what was expected, not as
criteria.

## 2026-10-25: P2.50 same replay rows trained at the server; readings fixed before the run

Owner decision (2026-10-25): confirm the method as early as possible. The
one open alternative that could change the method is spending the replay
rows on more server KD instead of mixing them into the client rounds.
P2.49 `gmixkd50_k2aaa` (decomposition only) is stopped to free GPU 1 and
resumes later from its checkpoint; P2.49 `gmixgold_k2aaa` keeps GPU 0.
Code: nested `d177c4e`. Seed 0, dev sets, exploratory.

Both arms start from the published `hinton_k2aaa` K2 adapter and train
Hinton KD (0.5 CE + 0.5 T^2 KL, T=2, full cached 7B logits, lr 2e-4, one
pass) at the server on exactly the rows the `mixkd_k2aaa` clients replayed
(the same multiset, 1,731 per round, 5,193 in all); private rounds are plain.
Rows, targets, lr and optimizer steps on public rows match `mixkd_k2aaa`;
only the placement differs.

- `k2plus_aaa`: K2 > S(all 5,193 rows) > A > A > A. Longer server KD before
  FL; the baseline a reviewer asks first. Runs first (GPU 1).
- `fslm_k2sasasa`: K2 > S1 > A > S2 > A > S3 > A, each S on its round's rows.
  FSL matched in data and step size (P2.48 `fsl` used fewer rows and a
  smaller lr). Runs after P2.49 `gmixgold_k2aaa` frees GPU 0.

Readings, fixed before any P2.50 result (A3 against the candidate
`mixkd50_k2aaa`, 74.08 / 44.78; `mixkd_k2aaa` 73.98 / 45.24 is reported as
the exact match):

1. Arm Spider more than 1.0 above `mixkd50_k2aaa`: the method changes to
   that placement (no client replay) and the freeze is built around it.
2. Spider within 1.0: the higher BIRD wins (primary-metric rule).
3. Spider more than 1.0 below: mixing the replay into the client rounds
   beats spending the same rows and steps on server KD.

Prediction recorded, not a criterion: A3 BIRD about 40-41 for both arms,
since every run so far loses public-domain gains in the following private
rounds (K2 to A3, `central_k2`, P2.48 `fsl`).

## 2026-10-25: P2.49 gold K2 plus replay built (matched no-teacher pipeline); readings fixed before the run

Owner decision (2026-10-25): run the matched pipeline proposed in the P2.48
entry on both GPUs. Code: nested `e41ddfb`. Seed 0, dev sets, exploratory.

Both arms repeat the P2.47/P2.48 replay rounds (20% of each client's private
rows from the fixed 2,000-row BIRD subset, same seeds) from the published
P2.37 `gold_k2aaa` K2 adapter instead of the Hinton one:

- `gmixgold_k2aaa`: replay on gold CE. No teacher anywhere; the matched
  comparator of the candidate `mixkd50_k2aaa`.
- `gmixkd50_k2aaa`: replay on 0.5 CE + 0.5 KL to the top-50 plus tail
  teacher target (as `mixkd50_k2aaa`). Teacher in replay only.

With P2.47 `mixgold_k2aaa` (teacher at K2 only) and P2.48 `mixkd50_k2aaa`
(both) this is a 2x2: K2 objective (gold, Hinton) x replay objective (gold,
teacher). References at A3: `mixkd50_k2aaa` 74.08 / 44.78, `mixgold_k2aaa`
73.21 / 40.74, `gold_k2aaa` 70.41 / 40.03 (Spider / BIRD).

Readings, fixed before any P2.49 result (A3, primary metric Spider, BIRD
counts only when Spider is not lower):

1. Whole teacher contribution, `mixkd50_k2aaa - gmixgold_k2aaa`:
   - Spider +1.0 or more and BIRD not lower: the teacher contributes to the
     candidate at seed 0; it goes to the freeze entry and the three-seed
     confirmation.
   - Spider within 1.0 and BIRD +1.5 or more: the teacher contributes on the
     public domain only; a Spider claim is not supported.
   - Spider more than 1.0 lower: the teacher pipeline is not supported over
     the matched pipeline without a teacher.
2. Where it comes from, descriptive, no threshold: teacher in replay
   (`gmixkd50 - gmixgold`, `mixkd50 - mixgold`) and teacher at K2
   (`mixkd50 - gmixkd50`, `mixgold - gmixgold`). Parts may simply add up;
   no synergy is required (floor, AGENTS.md).
3. Alternative reading fixed now: if `gmixgold_k2aaa` reaches Spider within
   1.0 of `mixkd50_k2aaa`, the Spider gain over `gold_k2aaa` comes from
   public replay itself, not from the teacher.

After P2.49 the seed-0 set of controls for this method is complete; the
next step is a freeze entry (method, comparators, test, number of seeds
from a power check), which is the owner's decision.

## 2026-10-25: P2.48: compact replay targets match full ones; server learning keeps Spider but loses the BIRD gain each private round

Evidence: nested `8b79530` (`audits/protocol_v2/p248_replay_compact_fsl_s0/summary.md`).
Seed 0, dev sets, exploratory, exact McNemar. Readings were fixed in the
entry below before the run.

| Arm (from Hinton K2) | A1 Spider / BIRD | A2 Spider / BIRD | A3 Spider | Realistic | SYN | DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|---:|---:|
| `hinton_k2aaa` (no replay) | 71.57 / 36.77 | 71.86 / 38.66 | 72.53 | 61.81 | 56.38 | 58.32 | 38.53 |
| `mixkd_k2aaa` (P2.47, full targets) | 69.83 / 42.24 | 72.15 / 44.07 | 73.98 | 61.81 | 58.03 | 57.01 | 45.24 |
| `mixkd50_k2aaa` (top-50 + tail) | 69.73 / 41.92 | 72.82 / 43.74 | **74.08** | 63.58 | 58.70 | 57.20 | 44.78 |
| `fsl_k2asasa` (A1 of `hinton_k2aaa`, then S>A>S>A) | | 72.05 / 39.77 | 73.21 | 62.40 | 58.90 | 58.50 | 40.29 |

`fsl_k2asasa` by stage, Spider / BIRD: A1 71.57 / 36.77, S1 65.57 / 45.18,
A2 72.05 / 39.77, S2 68.28 / 43.68, A3 73.21 / 40.29.

Against the fixed readings:

1. Compact targets keep quality: **holds**. `mixkd50 - mixkd_k2aaa` at A3
   Spider +0.10 (11/10, p=1), BIRD -0.46 (29/36, p=.46); within 0.7 Spider
   and 0.5 BIRD at every round. Realistic +1.77 (p=.049) is one of nine
   contrasts and not read. The teacher replay signal survives a cut from
   16.7 MB to about 16.6 KB per row (about 33 MB per client, sent once).
2. Server learning: **holds** as fixed. `fsl - hinton_k2aaa` A3 Spider +0.68
   (p=.47), BIRD +1.76 (95/68, p=.041), SYN +2.51 (p=.002).
3. Placement: client replay stays the candidate. `fsl - mixkd_k2aaa` A3
   Spider -0.77 (p=.40) is within 1.0, but BIRD -4.95 (67/143, p<.001).
4. As fixed, this says nothing about AKAKA against K2AAA.

- Where the server step goes: each S raises BIRD (+8.4 at S1, +3.9 at S2)
  and costs Spider (-6.0, -3.8, even at 18% of an epoch and half the lr);
  the next private round recovers Spider and gives back most of the BIRD
  gain (-5.4, -3.4). Alternating public and private steps forgets the
  public signal; mixing it into the client objective (replay) keeps it.
  This is the AKAKA pattern at a small scale. Hypothesis from one seed.
- Other reading: `fsl` saw fewer public rows (3,462 against 5,193), so part
  of the BIRD gap could be volume. S1 alone reached 45.18 BIRD, above the
  `mixkd` A3, so volume did not limit what the server step learned; the loss
  happens in the following round.
- `fsl - gold_k2aaa` A3 DK +6.17 (41/8): the K2 teacher edge on DK holds
  under server steps; it is inherited from the Hinton K2 parent.
- Measured: replay rounds peak 20,227 MB reserved (19.8 GiB), 2.1-3.3 h
  per round; S steps 20,317 MB, 0.58 h each; plain rounds 14,527 MB.

Candidate method after P2.48: Hinton K2, then private rounds with
compact teacher replay (`mixkd50_k2aaa`): Spider 74.08, BIRD 44.78 at A3,
communication 33 MB per client once plus the adapters. Still missing for
the Q3 floor: the matched pipeline without any teacher (gold K2 plus gold
replay) and gold K2 plus teacher replay, both available from the published
P2.37 `gold_k2aaa` K2 adapter.

## 2026-10-25: P2.48 compact replay targets and server learning built; readings fixed before the run

Owner decision (2026-10-25): run two directions next, one per GPU, before
the matched gold K2 plus gold replay pipeline proposed in the P2.47 entry.
Code: nested `227e433`, `e90e75a`. Seed 0, dev sets, exploratory.

- `mixkd50_k2aaa` (cost of `mixkd_k2aaa`). Same rounds, rows and seeds as
  P2.47 `mixkd_k2aaa`; the replay KL at T=2 sees only the teacher's top-50
  tokens per position plus one tail bucket `r = 1 - sum(top-50)`, and the
  student is coarsened over the same partition. The server then ships the
  2,000-row subset once as about 16.6 KB per row (50 ids, 50 fp16
  probabilities, `r`, per target token), about 33 MB per client instead of
  the full 16.7 MB per row. At T=2 about 20% of the teacher mass lies
  beyond the top 50 tokens (17% beyond the top 1,000; entry 2026-10-24); the
  renormalized cut of P2.46 drops it, the tail bucket keeps it as one number. Source: the residual tail bucket of RG-OPD
  (Akhondzadeh et al., arXiv 2607.04037, App. A.2), there reverse KL on the
  student's top-k; here forward KL on the teacher's top-k from a cache. The
  cut KL never exceeds the full KL (data processing), and equals it when the
  teacher puts no mass outside its top-k (unit test).
- `fsl_k2asasa` (teacher kept at the server). Server learning, FSL (Mai,
  La, Zhang, IEEE TAI 2024; arXiv 2210.02614): after FedAvg the server takes
  small steps on its own data at a decaying step size. From the published
  `hinton_k2aaa` A1 adapter: S > A > S > A. S is one Hinton pass (0.5 CE +
  0.5 T^2 KL, T=2, cached 7B logits) over 1,731 BIRD rows, the public volume
  of one replay round (sum of round(0.2 n_i)), sampled per stage from the same
  2,000-row subset; lr gamma * 2e-4, gamma 0.5 after A1 and 0.25 after A2.
  A is the plain P2.37 round. Deviations from FSL, disclosed: no server
  step after the last round (the endpoint stays a client average, like every
  other arm), and the server data is the teacher-labeled public pool.
  Why this is not AKAKA: each AKAKA K was a full 9,428-row epoch at full lr
  with its own schedule and cost about 5 Spider points; S is 18% of an epoch
  at half and a quarter of the lr. Public rows over the chain: 3,462 for
  `fsl` against 5,193 for `mixkd`.

Readings, fixed before any P2.48 result (A3 unless stated; a Spider dev
question is about 0.1 point, a BIRD dev question about 0.07):

1. Compact targets keep quality: `mixkd50 - mixkd_k2aaa` within 1.0 point
   on Spider and within 1.5 on BIRD. Spider more than 1.0 lower, or BIRD more
   than 1.5 lower, means the cut loses quality; then a larger k (200) is the
   next test. This is a tolerance at one seed, not an equivalence test.
2. Server learning keeps the teacher in FL without shipping targets:
   `fsl - hinton_k2aaa` Spider not lower and BIRD higher. Spider more than
   1.0 lower means even small decayed server steps pull the student off the
   private domain (the AKAKA failure persists at small scale).
3. Choice between the two placements: rank by Spider, then BIRD, under the
   primary-metric rule. If `fsl` is within 1.0 Spider of `mixkd_k2aaa` and
   not lower on BIRD, server learning is preferred (clients receive only the
   adapter); otherwise client replay stays the candidate.
4. Any reading of `fsl` speaks for a small, decaying server step after K2,
   not for AKAKA as run in P2.37: AKAKA beating K2AAA is not tested here.

Limits: `fsl - hinton_k2aaa` mixes server learning with teacher KD (a gold
CE server step would isolate the teacher); both arms add compute against
`hinton_k2aaa`. The teacher contrast at matched compute stays `mixkd -
mixgold` (P2.47).

## 2026-10-24: P2.47 client replay: teacher replay keeps Spider and lifts BIRD to 45.24; candidate method holds

Evidence: nested `80d1091` (`audits/protocol_v2/p247_client_replay_s0/summary.md`).
Seed 0, dev sets, exploratory, exact McNemar. Readings were fixed in the
entry below before the run.

| Arm (from Hinton K2) | A1 Spider / BIRD | A2 Spider / BIRD | A3 Spider | Realistic | SYN | DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|---:|---:|
| `hinton_k2aaa` (no replay) | 71.57 / 36.77 | 71.86 / 38.66 | 72.53 | 61.81 | 56.38 | 58.32 | 38.53 |
| `mixgold_k2aaa` | 70.41 / 39.11 | 71.95 / 40.29 | 73.21 | 62.20 | 58.51 | 57.01 | 40.74 |
| `mixkd_k2aaa` | 69.83 / 42.24 | 72.15 / 44.07 | **73.98** | 61.81 | 58.03 | 57.01 | **45.24** |
| `gold_k2aaa` (reference) | 70.12 / 40.74 | 69.83 / 39.90 | 70.41 | 61.22 | 56.38 | 52.34 | 40.03 |
| `central_mix` (pooled, no privacy) | | | 73.21 | 62.99 | 58.90 | 58.69 | 43.68 |

Against the fixed readings:

1. Teacher inside FL, `mixkd - mixgold` A3 Spider +0.77 (22/14, p=.24): no
   reading at seed 0. On BIRD the teacher replay is ahead in every round:
   +3.13, +3.78, +4.50 (113/44, p<.001). Spider is not lower, so the BIRD
   gain counts under the primary-metric rule.
2. Replay itself, `mixgold - hinton_k2aaa` A3 Spider +0.68 (p=.49): no
   reading; BIRD +2.22 (p=.031).
3. Candidate method, `mixkd - hinton_k2aaa` A3 Spider +1.45 (44/29, p=.10),
   BIRD +6.71 (p<.001): **holds** (Spider +1 or more, BIRD not lower).
   DK -1.31 (p=.28), Realistic 0.00, SYN +1.64.

- `mixkd_k2aaa` is above `central_mix` on Spider (+0.77) and BIRD (+1.56)
  while keeping data at the clients; its BIRD (45.24) is 1.8 below the 7B
  teacher (47.07).
- Against the gold pipeline without replay, `mixkd - gold_k2aaa`: Spider
  +3.58 (67/30, p<.001), DK +4.67, BIRD +5.22. This mixes the teacher at K2,
  replay, and the teacher in replay; the matched comparator is gold K2 plus
  gold replay, not run yet.
- Replay rounds start lower on Spider at A1 (-1.16 and -1.74 against
  `hinton_k2aaa`) and pass it by A3: the replay rows cost private progress
  early and the extra steps catch up.
- Other reading: replay adds optimizer steps (20% more rows per round), so
  part of `mix* - hinton_k2aaa` is compute; `mixkd - mixgold` has equal
  compute and isolates the teacher.

Next (per the entry below): the matched no-teacher pipeline, gold K2 plus
gold replay. Proposed with it, to make a 2x2 (K2 objective x replay
objective): gold K2 plus teacher replay. Teacher contribution at K2 and in
replay then each have a matched contrast at A3.

## 2026-10-24: teacher off-gold mass by SQL token role: KD already leans to SQL structure; token-role KD dropped

CPU audit of the P2.27 BIRD teacher cache (`scripts/audit_teacher_token_roles.py`,
nested `9e68cfb`): 1,000 rows sampled with seed 0, 54,543 target tokens, all
parsed by sqlglot. Off-gold mass = 1 - p_teacher(gold), the part of the Hinton
target that differs from gold CE. Output on the server, not committed yet.

| T=2 | Token share | Mean off-gold mass | Share of off-gold mass | Teacher argmax not gold |
|---|---:|---:|---:|---:|
| keyword or function | 0.213 | 0.350 | 0.279 | 0.070 |
| operator or punctuation | 0.169 | 0.313 | 0.198 | 0.063 |
| schema identifier | 0.407 | 0.225 | 0.344 | 0.052 |
| literal value | 0.156 | 0.202 | 0.118 | 0.020 |
| other (end token) | 0.055 | 0.294 | 0.061 | 0.021 |

- Structure tokens (keyword, operator) are 38% of target tokens and carry 48%
  of the off-gold mass; schema and values are 56% of tokens and carry 46%.
  Per token the teacher departs from gold most on keywords. At T=1 the order
  is the same, with all off-gold masses 3-4 times smaller.
- Reading fixed before the run (2026-10-24, chat): schema and values well
  above half of the off-gold mass would support token-role KD; structure
  tokens taking most of it would not. The result is the second case: Hinton
  KD already puts more of its signal per token on SQL structure, so
  reweighting toward structure changes little. Token-role KD (direction 1) is
  dropped. Next build: FSL-style server KD after each FedAvg round with a
  decreasing weight (Mai et al., IEEE TAI 2024), after P2.47.
- Other reading: off-gold mass measures how far the target is from gold, not
  which part of it transfers; schema-token alternatives (46% of the signal)
  may still be the part that does not transfer. The audit cannot separate
  this; only a K2 run with role weights could, at about 6 GPU-h.

## 2026-10-24: owner reopens shared replay; P2.47 client replay built, readings fixed before the run

Owner decision (2026-10-24): reopen shared teacher replay (rejected
2026-10-12) and run it before the compression tests. P2.46 and P2.41 are
deferred: they only matter if replay helps, to show its targets are cheap
to send.

Why now: in both role directions the teacher edge is created at K2 and
shrinks in the private rounds, and the public domain is forgotten there
(forward Hinton K2 -> A3: Spider edge +3.19 -> +2.13, BIRD 43.61 -> 38.53;
reverse: BIRD edge +3.59 -> +1.11). `central_mix`, which trains both domains
at once, keeps both (73.21 / 43.68).

P2.47 (nested `e95a153`, `26b007a`), seed 0, dev sets. Both arms repeat the
three plain private rounds of P2.37 `hinton_k2aaa` from its published K2
adapter. In every round each client also trains on 20% of its private row
count (about 1,730 BIRD rows per round in total), drawn per round and client
from one fixed 2,000-row seeded subset of the BIRD train pool.

- `mixgold_k2aaa`: replay rows on gold CE (shared public data, Zhao et al.,
  2018, "Federated Learning with Non-IID Data").
- `mixkd_k2aaa`: replay rows on 0.5 gold CE + 0.5 T^2 KL to the cached 7B
  logits at T=2, the K2 objective (public-data distillation at the clients,
  FedMD, Li and Wang, 2019). The teacher runs only at the server; clients
  receive public rows and the teacher's outputs on them. The full cached
  target is used (about 16 MB per row in a real deployment); P2.46/P2.41 say
  later whether a cheap target keeps the effect.
- FedAvg weights stay the private row counts. Private rows train exactly as
  in `hinton_k2aaa`.

Readings, fixed now (Spider primary; seed-0 MDE about 3.2, so these are
directions; one Spider question is about 0.1 point):

1. Teacher inside FL, `mixkd - mixgold` at A3 Spider: +2 or more reads as a
   teacher contribution during FL; between -1 and +2, no reading at seed 0;
   -1 or less, teacher replay costs Spider.
2. Replay itself, `mixgold - hinton_k2aaa` at A3 Spider: +1 or more helps,
   -1 or less costs Spider. More optimizer steps per round come with the
   replay rows, so this contrast is replay plus compute.
3. Candidate method: `mixkd - hinton_k2aaa` at A3 Spider +1 or more with
   BIRD not lower. BIRD gains count only when Spider is not lower.
4. References: `central_mix` 73.21 / 43.68 (pooled, no privacy), gold K2AAA
   70.41 / 40.03.

If reading 1 or 3 holds, the matched no-teacher pipeline (gold K2 plus gold
replay) is the next arm, since the paper's teacher contribution is measured
against the matched gold pipeline.

## 2026-10-24: teacher mass kept by top-k: at T=2 about 20% sits beyond the top 1,000 tokens

CPU audit of the P2.27 BIRD teacher cache (`scripts/audit_teacher_topk_mass.py`,
nested `4a2f8c1`): 1,000 of 9,425 rows sampled with seed 0, 55,357 KD
positions, student vocabulary. Output `audits/protocol_v2/teacher_topk_mass_s0/`
on the server, not committed yet. Descriptive.

| Mean kept mass | top-1 | top-10 | top-50 | top-200 | top-1000 |
|---|---:|---:|---:|---:|---:|
| T=1 | 0.967 | 0.9997 | 0.9999 | 1.000 | 1.000 |
| T=2 | 0.747 | 0.791 | 0.801 | 0.811 | 0.825 |

KL(top-k target || full target) at T=2: 0.262 (k=50), 0.246 (k=200), 0.221
(k=1000); at T=1 it is 0.0003 at k=10. The 5th percentile of kept mass at
T=2 is 0.39 (k=50).

- At T=1 the teacher is sharp: the top 10 tokens hold all its mass, so top-10
  KD at T=1 is the full Hinton T=1 target (about 3 KB per BIRD row to ship).
- At T=2 about 17.5% of the mass lies beyond the top 1,000 tokens, spread over
  about 151k tokens the teacher gives almost no probability at T=1. The
  published Hinton K2 target is therefore about 75% gold, 5% ranked
  alternatives and 20% far tail; the P2.38 virtual teacher is 73% gold and
  27% uniform.
- Top-50 and top-200 at T=2 are nearly the same target (kept mass 0.80 and
  0.81). Running both measures k twice. P2.46 top-50 renormalizes to about
  93% gold; it tests whether the far tail matters.
- Plan change (exploration choice, owner to confirm by running): GPU 0 runs
  P2.46 `top50_k2aaa` to K2; GPU 1 runs P2.41 `hinton_t1_k2aaa` (built and
  prepared since 2026-10-13, not run) instead of `top200_k2aaa`. Hinton T=1
  equals cheap top-10 replay, so it reads both the temperature question and
  the replay cost. If both lose the edge, the next candidate is top-k plus
  the remaining mass spread evenly (one extra number per token), or the
  sampled tail of Sparse Logit Sampling (Anshumann et al., ACL 2025, to
  verify before citing).

Readings for Hinton T=1 at K2, fixed now, same thresholds as P2.46: kept at
61.28 or more Spider (and at least 2 above gold K2 59.09); lost at 60.09 or
less; between, no reading at seed 0. My estimate before the runs: 35-45%
that either arm reads "kept", since both targets put 93-97% on gold.

## 2026-10-24: P2.46 top-k teacher logits at K2 built; readings fixed before the run

Question: does Hinton K2 keep its edge over gold K2 when the teacher target
is cut to its top-k tokens per position? It decides whether shipping teacher
outputs to the clients is cheap enough to matter. Shared teacher replay (the
server sends teacher soft labels on a public subset, clients replay them in
private rounds) was rejected on 2026-10-12; this run only measures its
communication cost. Reopening it stays the owner's decision.

- Cost of shipping the full target: 152,064 fp16 logits per token (about
  304 KB), 53.3 target tokens per BIRD gold SQL on average, so about 16 MB
  per row. Top-k as fp16 value plus int32 index: about 16 KB per row at
  k=50 and 64 KB at k=200 (32 MB and 128 MB for 2,000 rows, sent once).
- Risk: the edge may live in the tail. At T=2 about 80% of the off-gold
  teacher mass lies outside the top 10 (P2.38 prepare), and the virtual
  teacher, which keeps the gold token and a uniform tail, is 2.9 Spider
  points below gold at K2 and 2.0 below Hinton at A3 (P2.38).
- Arms (nested `14fa97d`, `4a9553c`): `top50_k2aaa`, `top200_k2aaa`. Every
  P2.37 `hinton_k2aaa` command, adding only `--kd-teacher-topk` at K2: the
  same P2.27 teacher cache, cut on load to the top-k logits, renormalized
  over them at T=2, same 0.5 gold CE + 0.5 KD. The trainer logs the mean
  teacher mass at T=2 that the cut keeps. Run to K2 first (`--until k2`),
  one arm per GPU, about 5-6 h each.
- Comparators: published P2.37 K2, Hinton 62.28 Spider / 43.61 BIRD, gold
  59.09 / 43.48 (Hinton - gold +3.19 Spider).

Readings, fixed now, for each arm's K2 Spider EX (seed 0, descriptive; one
Spider question is about 0.1 point and the seed-0 MDE is about 3.2, so these
are directions, not tests):

1. Kept: at least 61.28 (within 1 point of full Hinton) and at least 2
   points above gold K2. Top-k is enough at that k; client replay costs
   kilobytes per row. Next: the owner decides whether to reopen replay.
2. Lost: at most 60.09 (within 1 point of gold K2). The edge needs the
   tail; replay at this k is not worth building.
3. Between: no reading at seed 0. If top-200 reads "kept" and top-50 does
   not, k=200 is the replay setting.

BIRD K2 EX is reported for both and read under the primary-metric rule.
A1-A3 are run only if an arm reads "kept" and the owner wants the full
chain.

## 2026-10-24: Spider error types at K2 and A3: BIRD training fixes executability, the teacher adds semantic correctness

Analysis of published seed-0 Spider dev predictions (P2.27 base, P2.37 K2
and A3, P2.38 K2); computed ad hoc, script not committed. Exploratory, post
hoc (R8 applies to any subgroup).

| Spider dev (%) | EX | Execution error | Executes, wrong result |
|---|---:|---:|---:|
| base | 59.19 | 24.47 | 16.34 |
| gold K2 | 59.09 | 11.12 | 29.79 |
| virtual K2 | 56.19 | 11.32 | 32.50 |
| Hinton K2 | 62.28 | 11.22 | 26.50 |
| gold K2AAA A3 | 70.41 | 8.80 | 20.79 |
| Hinton K2AAA A3 | 72.53 | 8.61 | 18.86 |

- Two BIRD epochs with any objective halve Spider execution errors (24.5 to
  about 11): public training teaches executable SQL on unseen schemas, and
  gold CE gets that much without the teacher.
- Gold and virtual turn the fixed errors into executable but wrong queries;
  Hinton has 3.3 points fewer of them at K2 and 1.9 fewer at A3, where
  execution errors are level. The surviving edge is semantic correctness on
  the unseen domain.
- Hinton - gold at K2 is spread over hardness levels (easy +3.2, medium
  +3.1, extra +9.0, hard -2.3) and over JOIN (+2.5) and no-JOIN (+3.7); at
  A3 it sits more on JOIN (+3.7, p=.058) and hard (+4.0) questions.
- Owner reading (2026-10-24): server KD teaches general SQL competence on
  the public domain; the BIRD-specific part is not kept, but the general
  part transfers to the private domain and survives FL. Consistent with the
  table, with the reverse K2 result (BIRD +3.59 while Spider in-domain is
  -2.42) and with Hinton losing more BIRD than gold during the private
  rounds. Related published mechanism: KD as pre-training with better
  transferability (He et al., CVPR 2022, to check before citing).

## 2026-10-24: what the surviving teacher edge is: closer to the centralized level, not knowledge the private data lacks

Analysis of published seed-0 dev predictions (P2.27 `central` E3, FL A3,
base; P2.37 `hinton_k2aaa`/`gold_k2aaa` A3 and `central_mix` E3; P2.42
`central_k2` E3); computed ad hoc, script not committed. Exploratory.

| Spider / DK EX | base | FL A3 | gold K2AAA | Hinton K2AAA | central (Spider only) | `central_mix` | `central_k2` |
|---|---:|---:|---:|---:|---:|---:|---:|
| Spider | 59.19 | 67.60 | 70.41 | 72.53 | 71.37 | 73.21 | 74.66 |
| DK | 47.66 | 53.27 | 52.34 | 58.32 | 58.50 | 58.69 | 58.50 |

- Centralized Spider alone (no teacher, no BIRD) reaches the DK level of
  Hinton K2AAA (58.50 vs 58.32). The DK edge (+5.98 over gold) is therefore
  not domain knowledge that Spider train lacks; it closes most of the DK gap
  between the federated gold chain and centralized training. The chat
  suggestion of 2026-10-24 ("the surviving edge is what private data cannot
  teach") is withdrawn.
- FL-penalty questions (central E3 right, FL A3 wrong): Spider 104, Hinton
  right on 57, gold on 51; DK 58, Hinton 32, gold 22. On DK, 10 of the net
  32 Hinton-over-gold questions sit there.
- Share of each side's wins on which a reference is right (Hinton wins /
  gold wins, Spider): central 62% / 53% (p=.49), `central_mix` 65% / 60%
  (p=.64), `central_k2` 69% / 50% (p=.10), FL 38% / 43%. No signature
  reaches p<.05 with 52/30 discordant questions.
- Pooled gold without privacy (`central_mix`) is level with or above
  Hinton K2AAA on Spider (+0.68, n.s.) and DK (+0.37). The teacher adds
  nothing beyond what pooled gold data reaches; under the federated
  constraint it brings the chain close to that level, where the gold
  bootstrap does not (Spider 70.41, DK 52.34).

Reading: the 7B attribution (P2.44: gold, virtual and self all at the gold
level) is unchanged; what changes is the description of the gain: it
reduces the federated shortfall against centralized training. Open test
of whether the teacher's help depends on federation: centralized Spider
from the gold K2 adapter (`central_gold_k2`, not run) against `central_k2`.
Near 74.66 means the K2 start matters only under FL; near 71-72 means the
teacher start helps centralized training too.

## 2026-10-24: P2.43 reverse roles at A3: teacher edge on BIRD fades to +1.11 (n.s.); both chains beat FL

Evidence: P2.43 summary from the server (`--phase analyze`), not committed
yet; publication waits for `central_bird`. Seed 0, dev sets, exploratory,
exact McNemar. Private BIRD is the primary metric here (entry 2026-10-17).

| Arm | K2 | A1 | A2 | A3 BIRD | A3 Spider | A3 DK |
|---|---:|---:|---:|---:|---:|---:|
| `hinton_k2aaa_rev` (BIRD) | 28.75 | 37.16 | 40.35 | 41.33 | 64.89 | 54.39 |
| `gold_k2aaa_rev` (BIRD) | 25.16 | 34.68 | 38.59 | 40.22 | 64.70 | 52.34 |
| `fl_bird` (BIRD) | | 32.53 | 37.74 | 39.18 | 60.44 | 47.85 |

- Hinton - gold, BIRD: K2 +3.59 (p<.001), A1 +2.48 (p=.004), A2 +1.76
  (p=.040), A3 +1.11 (93/76, p=.22, CI [-0.55, +2.77]). Spider A3 +0.19;
  SYN +2.03 (p=.078), DK +2.06 (p=.22).
- Against FL, BIRD A3: Hinton +2.15 (104/71, p=.015), gold +1.04 (p=.28).
  Spider A3: Hinton +4.45, gold +4.26 (both p<.001).

Reading:

- The early-signal gain shrank every round: about 70% of the K2 edge is gone
  at A3, more than in the main direction (+3.19 at K2 to +2.13 at A3, about
  one third gone). BIRD clients hold 9,428 rows and FL alone still rises at
  A3 (32.53, 37.74, 39.18), so the private rounds may wash out any start.
- In the reverse the public gold alone does not beat FL on BIRD at A3
  (+1.04, n.s.); the chain with the teacher does (+2.15, p=.015). The
  teacher - gold contrast that would carry a claim is +1.11 and not
  significant at seed 0.
- Reverse is consistent in sign with the main direction but adds no second
  significant teacher contrast. Anchoring was not tested in the reverse (no
  reverse self-teacher). Whether the reverse enters the confirmation (it
  needs its own BIRD holdout, entry 2026-10-17) is the owner's choice in the
  freeze entry; `central_bird` (running) gives its FL penalty reference.

## 2026-10-24: P2.44 self-teacher: the Spider edge comes from the 7B, not from anchoring

Evidence: P2.44 summary from the server (`--phase analyze`), not committed
yet; publication waits until no P2.43 lane runs. Seed 0, dev sets,
exploratory, exact McNemar. `self_k2aaa` = `hinton_k2aaa` with the base
Coder-1.5B as the K2 teacher. Readings were fixed on 2026-10-23.

| Arm | K2 Spider / BIRD | A1 Spider / BIRD | A3 Spider | A3 DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|
| `hinton_k2aaa` | 62.28 / 43.61 | 71.57 / 36.77 | 72.53 | 58.32 | 38.53 |
| `gold_k2aaa` | 59.09 / 43.48 | 70.12 / 40.74 | 70.41 | 52.34 | 40.03 |
| `virtual_k2aaa` | 56.19 / 44.07 | 67.99 / 39.05 | 70.50 | 55.70 | 39.83 |
| `self_k2aaa` | 58.03 / 28.94 | 68.47 / 32.01 | 70.21 | 52.71 | 32.27 |

- Hinton - self, Spider: K2 +4.26 (114/70, p=.0015), A1 +3.09 (p=.0016),
  A2 +1.74 (p=.073), A3 +2.32 (62/38, p=.021); A3 DK +5.61 (45/15,
  p<.001), Realistic +0.79, SYN +1.55; BIRD A3 +6.26 (p<.001).
- Self - gold, Spider: K2 -1.06 (p=.50), A3 -0.19 (45/47, p=.92); DK +0.37;
  BIRD K2 -14.54, A3 -7.76 (both p<.001).
- Paired recovery at A3, Spider: of the 52 questions Hinton wins over gold,
  self is right on 24 (46%); of the 30 gold wins, on 17 (57%). At K2: 58/95
  (61%) and 23/62 (37%).

Reading (against the readings fixed 2026-10-23):

- K2 (mechanism): the anchoring prediction holds for BIRD (self K2 28.94,
  far below gold 43.48: the base-model target pulls hard against gold CE)
  but fails for Spider (58.03, not at or above gold 59.09). The Spider edge
  of Hinton K2 (+3.19 over gold) is not reproduced by pulling toward the
  base model.
- A3 (paper endpoint): self is level with gold (-0.19) and Hinton is above
  self (+2.32, p=.021). The recovery shares go the "from the 7B" way (low
  first share, higher second). Three teacher-free references now sit at the
  gold level on Spider A3: gold 70.41, virtual 70.50, self 70.21; Hinton is
  72.53. On DK the same holds (52.34 / 55.70 / 52.71 vs 58.32).
- The KD headroom audit (2026-10-23) could not detect a teacher signature on
  Spider at A3; with 52/30 discordant questions that test had little power,
  and P2.44 is the direct test.
- Other reading still open: the self-teacher is a stronger anchor than the
  7B (it puts less mass on gold tokens, which is why BIRD collapses), so
  P2.44 rules out "anchoring of this strength", not a milder pull toward the
  base model at the 7B's gold mass (0.728). A matched-strength control (base
  logits mixed with the gold one-hot to the same mean gold mass, from the
  existing P2.44 cache) would close it at the cost of one chain. Owner's
  choice.
- Status for the floor: the teacher contribution at the final endpoint is
  about +2 Spider against each of three controls (gold, smoothing, self);
  seed 0 only, and the +2.13 against gold is still the selected recipe
  (reviewer's shrunk estimate about +1.4). The confirmation over seeds
  decides.

## 2026-10-23: direction review (Codex) and per-question KD headroom audit

Codex research review (read-only, from a self-contained brief; report not
committed). Its main conclusion matches ours: no new loss or client tweak has
an expected effect near the seed-0 MDE (about 3.2 points at 80% power with
about 140 discordant questions), so controls and confirmation decide more
than another component. Our review of its eight directions:

- Kept: finish P2.43; a segmented central control that resets AdamW and the
  cosine schedule per segment like FL (separates optimizer resets from
  federation in the FL penalty); central from gold K2 if the paper claims
  the teacher reduces the FL penalty; FedAdam (Reddi et al., ICLR 2021) as
  a stronger FL baseline; a DB-disjoint BIRD holdout as the reverse
  confirmation set.
- Rejected: more frequent sync at the same passes (6 x 0.5 epoch). The
  2026-10-11 diagnosis puts the FL penalty on few optimizer steps per pass
  (69-129 local steps vs about 541 per central epoch) with fresh AdamW and
  warmup per round; halving local epochs doubles the resets.
- Rejected for the teacher story: LoRA+ (moves gold and Hinton alike);
  selective KD, DKD, AdaKD (each refits soft labels on gold; expected 0 to
  +1, below the MDE, and each adds to the seed-0 search); FedDAT (25-35 GPU-h
  for 0 to +1.5; dual adapters rejected 2026-10-11).
- Low priority: Pure-KD (Zhu et al., NAACL Industry 2025: teacher prompt 23%
  of the student's, student +1.9 TS, fine-tuned teacher). A gold-pruned
  schema is oracle input, so the target moves toward gold and loses the
  schema alternatives the soft label carries.
- Correction to our diagnosis 1: the marginal EX gap is not the KD ceiling.
- Manuscript note: Hinton uses all 9,428 rows on gold prefixes; execution
  selection belongs to SeqKD only.

KD headroom audit (CPU, published seed-0 predictions; nested `1384045`,
`audits/protocol_v2/kd_headroom_s0/summary.md`; local commit, pushed after
the P2.43 and P2.44 publications because their pull allowlists reject a new
script). Teacher-only = teacher right, student wrong.

| Spider dev | EX | Teacher-only | Student-only | Neither |
|---|---:|---:|---:|---:|
| base | 59.19 | 223 | 42 | 199 |
| FL A3 | 67.60 | 149 | 55 | 186 |
| `gold_k2aaa` A3 | 70.41 | 128 | 63 | 178 |
| `hinton_k2aaa` A3 | 72.53 | 112 | 69 | 172 |
| `central_mix` E3 | 73.21 | 108 | 72 | 169 |

Share of each side's wins on which the teacher is right (Hinton - gold):

| Set, endpoint | Hinton wins | Gold wins | Fisher p |
|---|---:|---:|---:|
| Spider K2 | 86/95 (90.5%) | 48/62 (77.4%) | .036 |
| Spider A3 | 37/52 (71.2%) | 21/30 (70.0%) | 1.0 |
| BIRD K2 | 88/128 (68.8%) | 58/126 (46.0%) | <.001 |
| BIRD A3 | 63/89 (70.8%) | 61/112 (54.5%) | .020 |

Reading (exploratory, one seed):

- Headroom per question is larger than the marginal gap: the teacher answers
  112 Spider dev questions (10.8 points) that Hinton A3 misses. Gold data
  removes most of the base model's teacher-only set (223 to 128); Hinton
  removes 16 more.
- On BIRD, where KD runs, Hinton's wins sit on teacher-correct questions at
  K2 and still at A3. On Spider the signature is present at K2 and not
  detected at A3: 71.2% vs 70.0%, but with 52 and 30 questions the
  difference has a 95% CI of about -19 to +22 points, so a K2-sized gap (+13)
  is not excluded. F13 points the same way (8 of 52 A3 edge questions were
  K2 edge questions).
- The Spider A3 edge may be a general effect of the Hinton K2 start rather
  than the teacher's answers carried through the private rounds; this audit
  cannot tell. It neither confirms nor rules out the anchoring reading P2.44
  tests: dark knowledge can also help on questions the teacher misses.
- Diagnosis 1 restated: the bottleneck is the channel (soft labels on
  another domain's gold, then private rounds), not a small teacher lead.
- Follow-up: rerun the audit on P2.43 (BIRD private) once `gold_k2aaa_rev`
  A3 is published, to see whether the signature survives private rounds when
  the private domain is the harder one.

## 2026-10-23: P2.43 reverse roles: teacher ahead of gold on BIRD at K2 and A1 (not committed)

Source: server `--phase analyze` summary sent in chat; nested result commit
pending (publication waits until no P2.43 lane runs). Not committed: stays
out of the paper until published. Seed 0, dev sets, exploratory, exact
McNemar. BIRD is the private (primary) domain here.

| Endpoint | Hinton BIRD | gold BIRD | Hinton Spider | gold Spider |
|---|---:|---:|---:|---:|
| P2.27 `base` | 21.32 | 21.32 | 59.19 | 59.19 |
| K2 | 28.75 | 25.16 | 70.50 | 72.92 |
| A1 | 37.16 | 34.68 | 64.60 | 64.99 |
| A2 | 40.35 | - | 65.47 | - |
| A3 | 41.33 | - | 64.89 | - |

Hinton A3 robustness: Realistic 56.10, SYN 54.16, DK 54.39.

Hinton - gold: K2 BIRD +3.59 (145/90, p<.001), Spider -2.42 (51/76,
p=.033); A1 BIRD +2.48 (102/64, p=.004), Spider -0.39 (p=.76).

Reading:

- The early-signal condition of 2026-10-17 (about +2 or more on BIRD at A1,
  p<.05) is met; both chains already run to A3, so nothing changes in the
  queue.
- The direction mirrors the main setting: on the domain the server did not
  train on, Hinton K2 is ahead of gold K2 (+3.59 BIRD here, +3.19 Spider in
  P2.37), and gold fits the server domain better (Spider -2.42 here; in
  P2.37 Hinton was ahead on BIRD by only +0.13 at K2).
- Here gold K2 already lifts the unseen domain above base (BIRD +3.84), and
  Hinton adds the same again. Other reading: anchoring is still not ruled
  out; P2.44 tests it only in the main direction, and a reverse self-teacher
  would need its own Spider cache from the base model.
- Gold loses more Spider in the first BIRD round (-7.93 vs -5.90), as in F4.
- In the main direction A1 edges faded by A3. The primary contrast is
  Hinton - gold BIRD at A3, then the FL penalty against `central_bird`
  and the gain over `fl_bird`; none is in yet.

## 2026-10-23: independent reviews; plan to submission at Q3; P2.44 self-teacher built, readings fixed before the run

Three rounds of review by an agent without repository access, from
self-contained briefs (no new runs). What changed in our reading:

- The K2AAA teacher contrast at Coder-1.5B (+2.13 Spider, p=.020) is not a
  best-of-four pick: K2AAA entered the arm list from the 0.5B grid (P2.20,
  Hinton - gold +2.03, p=.048) before any 1.5B number. Pooled over the seven
  high-dose teacher - gold contrasts (mean +1.67), with a shared-question
  discount, the reviewer puts the true effect at about +1.4 (plausible +0.5
  to +2.3) and three-seed Spider test power at about 0.6 (about 0.7 one-sided).
- "Hinton K2 is above base while gold K2 equals base" does not rule out
  anchoring: a KL toward the base model can keep what gold CE learns on BIRD
  while removing what it forgets on Spider, and so land above base. The 0.5B
  half of that argument was a misreading (47.00 is gold K2, not base; the 0.5B
  base EX is not in the log). The virtual teacher (P2.38, Hinton - virtual
  +2.03 Spider, p=.031) rules out generic smoothing, not anchoring. So the
  self-teacher control is needed.
- Claims to drop or reword: BIRD +12.84 over FL is expected (FL never sees
  BIRD); the Spider +4.93 over FL splits into public gold +2.81 (`gold_k2aaa`
  - FL) and teacher +2.13; the fair centralized reference is `central_mix`
  (0.68 above Hinton), not "level with central Spider"; among the robustness
  sets only DK moves (Hinton - gold at A3: Realistic +0.59, SYN 0.00, DK
  +5.98).
- The reviewer's estimate of acceptance at a Q3 journal within one or two
  submissions: about 75-80% if the teacher contrast confirms, 40-50% if it
  does not, about 50% if the self-teacher matches Hinton; about 60-65%
  overall. Main expected objection: limited novelty (KD then FedAvg, close to
  FedCoLLM and FedMKT). Answer planned: the decomposition public gold /
  virtual / self / 7B teacher, not a new method.

Owner decisions (2026-10-23):

- Judge the plan by acceptance at a Q3 journal; for this assessment the floor
  text and the "K2AAA alone is too simple" decision (2026-10-13) are set
  aside.
- P2.45 (teacher-path KD: teacher SQL as the target on the 5,319
  execution-verified rows, Kim and Rush 2016) is not run: its likely outcome is
  a tie with Hinton, which adds a component with no measured gain.
- No seed 1-2 or Spider test run until every seed 0 control is in and the
  method is fixed in a freeze entry.
- Seed 0 queue, in order: P2.43 both chains to A3 plus `fl_bird` and
  `central_bird`; P2.44 self-teacher; a KL-to-base diagnostic on the K2
  adapters (script not written yet); then, if time allows, Coder-0.5B on the
  `alpha_0.1` split (FL, gold, Hinton K2AAA) and a 3B teacher.

P2.44 (`scripts/run_p244_self_teacher.py`, nested `e3a3e22`): `self_k2aaa`
repeats `hinton_k2aaa` with the base Coder-1.5B (fp16, no adapter) as the K2
teacher through its own BIRD logit cache; LoRA starts at zero, so the KL is a
pull back toward the start, as in LwF (Li and Hoiem, ECCV 2016). Readings
fixed before the run (exploration, no pass/fail rule; one contrast at seed 0
has an SE of about 1.15 points, so only large gaps are read):

- K2 (mechanism): if the edge is anchoring, `self_k2aaa` K2 has BIRD below
  gold K2 (43.48) and Spider at or above gold K2 (59.09). The base model's
  soft target puts less mass on BIRD gold tokens than the 7B does (7B mean
  0.73), so it pulls against gold CE more. Hinton K2: BIRD 43.61, Spider 62.28.
- A3 (what the paper would say): self - gold and Hinton - self on Spider,
  plus the paired recovery: of the questions Hinton gets right and gold gets
  wrong at A3, the share the self-teacher also gets right, next to the same
  share on the questions gold wins over Hinton. Self close to Hinton (high
  first share, low second) means the edge is mostly anchoring; self close to
  gold (the reverse) means it comes from the 7B.
- Whatever the result, the reviewer's proposal is to take the self-teacher
  into the three-seed confirmation, tested after Hinton - gold in a fixed
  sequence. That is decided in the freeze entry, not here.

## 2026-10-22: P2.43 `hinton_k2aaa_rev` K2 and A1 published; gold comparator not run yet

Evidence: nested `91a9ea5` (`audits/protocol_v2/p243_reverse_roles_s0/summary.md`).
Seed 0, dev sets, exploratory. The GPU 1 lane (`gold_k2aaa_rev` to A1, then
`fl_bird`) trained nothing (cause not known yet), so there is no contrast.

| Endpoint | BIRD (private) | Spider (public) |
|---|---:|---:|
| P2.27 `base` | 21.32 | 59.19 |
| `hinton_k2aaa_rev` K2 | 28.75 | 70.50 |
| `hinton_k2aaa_rev` A1 | 37.16 | 64.60 |

Flips on BIRD dev (lost / gained): base to K2 91/205, K2 to A1 99/228. On
Spider: base to K2 53/170, K2 to A1 111/50.

Reading:

- Two Spider epochs at the server raise BIRD by 7.43 points before any BIRD
  data; one BIRD round adds 8.41. Whether the teacher causes any of the K2
  transfer is unknown until `gold_k2aaa_rev` K2. In the main direction the
  transfer to the domain the server did not train on came from the teacher
  (Hinton K2 Spider 62.28, gold K2 59.09, base 59.19).
- The first private round loses 99 BIRD questions that K2 had right (6.5%),
  more than the main-direction analogue (47-57 Spider questions, 4.5-5.5%).
- Spider (secondary) drops 5.90 after one BIRD round.

## 2026-10-17: reverse roles: BIRD EX is the primary metric there; P2.43 built with an early-signal stop

Written before any P2.43 result exists.

Owner decisions (2026-10-17):

1. In the reverse setting (BIRD at the clients, Spider at the server) the
   primary metric is EX on the private domain, BIRD dev with evidence.
   Spider EX is secondary under the rule of 2026-10-16 with the roles
   swapped: a Spider gain counts only when BIRD EX is not lower, and breaks
   ties between options whose BIRD EX does not differ. Never trade BIRD for
   Spider. The main direction keeps Spider as primary.
2. The P2.43 pilot is approved: `fl_bird`, `gold_k2aaa_rev`,
   `hinton_k2aaa_rev`, plus `central_bird` (all BIRD train rows in one place,
   three epochs, the FL-penalty reference).
3. An early signal comes first, before the full chains.

Open point the metric decision creates: BIRD has no public test set; our
BIRD `test.csv` is BIRD dev, which exploration uses. A confirmation set for
the reverse setting (for example a DB-disjoint part of BIRD train held out
before seeds 1-2) must be fixed in the freeze entry. Spider test stays the
confirmation set of the main direction.

Build (nested `7694f3f`, `dbd7a34`, `ffc169b`, `68f04bc`):

- Split: `BIRD/original_train9428_dev1534/federated_noniid/alpha_0.1/k5`,
  built from the BIRD DB groups, seed 0; clients of 2,761, 1,449, 3,929, 817
  and 472 rows; audit passed
  (`audits/protocol_v2/p243_reverse_roles_s0/bird_split_audit.json`).
- `scripts/run_p243_reverse_roles.py`. The chain arms are the P2.37
  `hinton_k2aaa` and `gold_k2aaa` commands with only the data, the cache and
  the outputs swapped (Spider pool, Spider profile, BIRD split; tested flag by
  flag). `fl_bird` and `central_bird` are the P2.27 FL and central commands on
  BIRD. Max length 7,168 everywhere (Spider prompts are under 3,000 tokens;
  all 9,428 BIRD rows fit 7,168 in P2.17). A new Spider teacher logit cache
  (`--phase cache`; the runner needs 130 GB free). `--until k2|a1` stops a
  chain; a later run continues from the last recorded stage.

Early signal (seed 0, dev, descriptive):

- GPU 1: `gold_k2aaa_rev` to A1 (needs no cache), then `fl_bird`.
- GPU 0: the Spider cache, then `hinton_k2aaa_rev` to A1.
- Read as soon as each endpoint is evaluated (`--phase analyze` is safe while
  lanes run): `hinton_k2aaa_rev - gold_k2aaa_rev` on BIRD at K2 (teacher
  knowledge moved from Spider to BIRD before any BIRD training) and at A1
  (after one private round, the primary metric). References: P2.27 `base`
  BIRD 21.32 / Spider 59.19; in the main direction Hinton - gold at K2 on the
  domain the server did not train on was +3.19 (Spider).

How to read it (exploration; no pass/fail rule):

- Scale: one BIRD dev question is 0.065 points; with about 150-200
  discordant questions a paired contrast has a Wald 95% half-width near 1.7
  points.
- A clear Hinton - gold gain on BIRD at A1 (about +2 or more, p<.05) is a
  reason to run both chains to A3 and `central_bird`; it is not a result. In
  the main direction A1 gains faded by A3 (TAID BIRD A1 +3.19, A3 +1.04).
- Near zero at both K2 and A1: the teacher's Spider knowledge does not reach
  BIRD at this stage; report before spending A2-A3 (about 6-7 GPU-h per
  chain). Continuing is the owner's choice.
- Other reading of a K2 gain: soft targets can help through output smoothing
  alone. The P2.38 virtual-teacher control separates that and can be repeated
  here if the gain holds.
- Selection: the reverse adds two recipes to the seed-0 search (note of
  2026-10-17); any teacher edge here needs seeds 1-2 before a claim.

## 2026-10-16: Spider is the primary metric (owner decision)

Owner decision, fixed for every phase from now on: **Spider EX**, the
clients' private domain, is the primary metric (Spider dev in exploration,
Spider test at confirmation). BIRD EX, the public domain, is secondary: rank
options by Spider first; a BIRD gain counts only when Spider EX is not lower,
and between options whose Spider EX does not differ the higher BIRD wins.
Never trade Spider for BIRD. Both are still reported for every arm. Written
into both `AGENTS.md` files, `RESEARCH_STATE.md`, `system_architecture.md` and
`DIRECTION_PROPOSAL.md`.

Effect on today's readings (below): the BIRD erosion after K2 (F14, and the
teacher-specific part in P2.38) is a secondary result to report, not the
main weakness to fix; the target is the teacher's Spider contribution
(Hinton - virtual A3 +2.03, Hinton - gold +2.13), with `central_mix` level
with `hinton_k2aaa` on Spider (+0.68, n.s.).

Direction evaluated the same day at the owner's request: "FedCoLLM +
SQL-aware selective KD". Verdict (details in `DIRECTION_PROPOSAL.md`): do not
adopt the FedCoLLM part (two-way KD and LLM LoRA update each round), which
needs K after private rounds, mainly helps the LLM rather than the deployed
SLM, invalidates the teacher logit cache (about one day per round,
estimated) and makes FedCoLLM a required baseline. Keep selective KD as a
candidate K-stage objective next to TAID (Wang et al., ACL 2021; execution
selection is our adaptation; SQL token-type weighting has no published
source). Not queued; owner decides after P2.40.

## 2026-10-17: owner direction: reverse roles (BIRD private, Spider public) before other directions; compared with FedDAT

Owner decision: the next direction is the reverse setting, with BIRD (with
evidence) at the clients and Spider at the server, before FedDAT or any other
client method. Evaluation against FedDAT, from the evidence so far:

| | Reverse roles | FedDAT in the current direction |
|---|---|---|
| What it changes | The setting: where the private and public data sit | One client method inside K2AAA |
| Room on the metric it targets | FL penalty on BIRD private is large in the one earlier run (Qwen2.5-1.5B-Instruct, alpha 0.5: central E1/E2 31.42/34.94 against FL T1/T2 22.75/28.36) | About 2 Spider points left after Hinton K2 (F17, p=.061), near one-seed resolution |
| Teacher signal behind it | In the current direction the teacher edge appears on the domain the server did not train on (Hinton - gold at K2: Spider +3.19, BIRD +0.13); the reverse tests the same transfer the other way | Its mechanism keeps global knowledge during FedAvg; P2.42 shows the BIRD loss is not from federation, so most of that target is the secondary metric |
| Code | Mostly present: dataset profiles, stage chain, Spider SeqKD targets (7,251 rows), cache builder; new: a Spider teacher logit cache and a runner | New trainer: three adapter states, mutual KD, 3 forward + 2 backward per step; no SQL evidence |
| Cost per arm | About 13-15 GPU-h (K2 on Spider about 3-4 h, BIRD rounds about 3 h each) plus a one-time Spider cache (estimated 100 GB disk, a few GPU-h) | About 2.5 times a plain round per private round, plus implementation |
| Main risk | Spider-to-BIRD transfer may be weak: BIRD needs evidence and value grounding Spider never shows. Earlier reverse T1 (one round): SeqKD 24.45, FL 22.88, gold 20.73 | Small headroom; a gain may come from extra compute rather than the method |

Reading: the reverse setting has more measured room and reuses most of the
code; FedDAT stays a candidate client method for whichever setting is chosen.
Two points stay open and are the owner's:

- Metric: the primary metric (owner, 2026-10-16) is Spider EX as the clients'
  private domain. In the reverse setting the private domain is BIRD. Which
  metric is primary there must be fixed in a dated entry before any reverse
  result is read.
- The reverse adds recipes to the seed-0 search, so the selection note of
  2026-10-17 (best of several recipes) applies to it as well; its teacher
  edge also needs seeds 1-2 before any claim.

Proposed pilot (P2.43, not built yet): fresh Coder-1.5B, BIRD clients on a
new `alpha_0.1/k5` split built from the BIRD DB groups (a trial build gives
clients of 2,761, 1,449, 3,929, 817 and 472 rows), Spider public with all
8,659 rows. Arms: `fl_bird` (AAA), `gold_k2aaa_rev` (gold CE K2 on Spider,
then AAA on BIRD), `hinton_k2aaa_rev` (Hinton T=2 K2 with a Spider teacher
logit cache, then AAA). Evaluation: BIRD dev and Spider dev after each stage,
all five sets at A3. Main contrast: `hinton_k2aaa_rev - gold_k2aaa_rev` at A3
on BIRD.

## 2026-10-17: P2.40 TAID below Hinton on Spider at A3; P2.37 `local` published

Evidence: nested `640d534` (`audits/protocol_v2/p240_taid_s0/summary.md`),
`3e0dc0b` (`local`). Seed 0, dev sets, exploratory, exact McNemar. TAID ran
1,179 K2 updates with `t` from 0.4 to 1.0 (linear, as expected).

| Arm | K2 Spider / BIRD | A1 Spider / BIRD | A3 Spider | A3 DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|
| `taid_k2aaa` | 62.19 / 44.85 | 71.57 / 39.96 | 70.70 | 54.21 | 39.57 |
| `hinton_k2aaa` | 62.28 / 43.61 | 71.57 / 36.77 | 72.53 | 58.32 | 38.53 |
| `gold_k2aaa` | 59.09 / 43.48 | 70.12 / 40.74 | 70.41 | 52.34 | 40.03 |

- TAID - Hinton: Spider K2 -0.10, A1 0.00, A2 -0.58, A3 -1.84 (33/52,
  p=.050); A3 DK -4.11 (11/33, p=.001), Realistic +0.39, SYN +0.77; BIRD A1
  +3.19 (125/76, p<.001), A3 +1.04 (p=.29).
- TAID - gold at A3: Spider +0.29 (p=.80), DK +1.87 (p=.12), BIRD -0.46.
- `local` (each client alone, 3 epochs) Spider / BIRD: c1 67.02 / 23.99, c2
  64.99 / 21.32, c3 64.60 / 21.64, c4 65.38 / 24.12, c5 65.47 / 23.73; mean
  Spider 65.49. P2.27 FL A3 - best local (c1): Spider +0.58 (p=.69), BIRD
  +1.69 (p=.069). `hinton_k2aaa` A3 - best local: Spider +5.51 (p<.001).

Reading (Spider primary; the P2.41 condition was written before P2.40,
entry 2026-10-16):

- By the metric rule Hinton is ahead of TAID at A3 (Spider -1.84, DK -4.11).
  TAID kept the Spider edge over gold through A1 and took the BIRD loss of
  Hinton away at A1, but both effects faded by A3, where TAID sits at the
  gold level. The P2.41 condition (P2.40 ahead of Hinton) fails, so P2.41
  is not run.
- Other readings: TAID differs from Hinton in target and temperature (T=1 vs
  2); the A3 loss may come from T=1 rather than from the interpolation.
  Untested, and testing it no longer serves the choice of method.
- Plain FL is barely above the best single client on Spider (+0.58, n.s.) at
  this split; the K-first pipeline is what lifts the clients (+5.51).
- Teacher - gold on Spider at the final endpoint, all seed 0, across the
  recipes tried: Hinton v1 (NTD rounds) +1.35, `h_plain` +0.39,
  `hinton_k2aaa` +2.13 (p=.020), `taid_k2aaa` +0.29. Only one recipe
  reaches p<.05, and it is the best of four. With the selection effect noted
  in the 2026-10-12 rules (best of several null variants shows about +1.7),
  the +2.13 is a candidate, not a finding, until seeds 1-2 confirm it.
- Open for the owner: freeze `hinton_k2aaa` against `gold_k2aaa` (with
  `virtual_k2aaa` as the smoothing control) and confirm over seeds 1-2, which
  tests whether the floor holds at all, or keep exploring for a method above
  K2AAA first. Either way, the next teacher claim depends on the seed check.

## 2026-10-16: P2.42 central from the Hinton K2 adapter; FL penalty after K2 about 2 Spider points, BIRD loss is not from federation

Evidence: nested `c40e090` (`audits/protocol_v2/p242_central_from_k2_s0/summary.md`).
Seed 0, dev sets, exploratory, exact McNemar. `central_k2`: the P2.27 central
Spider run (all Spider train rows in one place, three epochs) started from
the `hinton_k2aaa` K2 adapter. Pass N = epoch eN against round aN (rule R9).

| Arm / pass | 1 Spider / BIRD | 2 Spider / BIRD | 3 Spider | 3 DK | 3 BIRD |
|---|---:|---:|---:|---:|---:|
| `central_k2` | 68.76 / 33.90 | 73.31 / 32.59 | 74.66 | 58.50 | 34.03 |
| `hinton_k2aaa` | 71.57 / 36.77 | 71.86 / 38.66 | 72.53 | 58.32 | 38.53 |
| P2.27 `central` | 67.50 / 23.27 | 71.18 / 24.71 | 71.37 | 58.50 | 25.75 |
| P2.27 `fl` | 65.57 / 22.62 | 68.28 / 24.38 | 67.60 | 53.27 | 25.68 |

- FL penalty on Spider, central minus FL from the same start: from the Hinton
  K2 adapter pass 1 -2.80 (FL ahead, p=.016), pass 2 +1.45, pass 3 +2.13
  (74/52, p=.061); from the base model (P2.27) +1.93, +2.90, +3.77 (p=.003).
  DK at pass 3: +0.19 after K2, +5.23 from base.
- BIRD: centralized Spider training after K2 loses more BIRD than FL does
  (pass 3 -4.50, p<.001; 34.03 against 38.53).
- `central_k2` E3 against `central_mix` E3: Spider +1.45 (p=.21), DK -0.19,
  BIRD -9.65. Against `gold_k2aaa` A3: Spider +4.26 (p<.001), DK +6.17.
- `central_k2` - P2.27 `central` at E3: Spider +3.29 (p=.004), BIRD +8.28.

Reading (Spider is the primary metric, owner 2026-10-16):

- After the teacher K2, the FL penalty on Spider is about 2 points at pass 3
  (p=.061) and none on DK; from the base model it is 3.77 and 5.23. One seed,
  and the difference between the two penalties is not tested; it is a
  direction that K2 narrows the FL gap, not a result.
- `central_k2` is still rising at E3, so the pass-3 penalty is not hidden by a
  central run past its peak.
- The BIRD erosion after K2 comes from training on Spider, not from
  federation: FedAvg rounds keep more BIRD than pooled Spider training. With
  BIRD secondary, a BIRD-retention arm is not a priority; the earlier note
  (central_mix entry) that BIRD retention is the largest gap is superseded.
- `central_k2` - P2.27 `central` (+3.29 Spider) shows that the Hinton K2 start
  helps centralized training too, but it does not isolate the teacher: there
  is no gold-K2 central arm.
- For the aim: the remaining Spider gap that a client-side method could close
  is about 2 points, near the one-seed resolution. A client method is worth
  queueing only if it targets that gap and can be read at three seeds.

## 2026-10-16: P2.38 virtual teacher published; the Spider edge is teacher-specific, part of DK is smoothing

Evidence: nested `d326854` (`audits/protocol_v2/p238_virtual_teacher_s0/summary.md`).
Seed 0, dev sets, exploratory, exact McNemar. Teacher at T=2 on the 9,428 BIRD
rows (prepare): gold-token probability `a` = 0.728, mass on its top 10
non-gold tokens 0.057, entropy 2.96 nats. `virtual_k2aaa` puts 0.728 on gold
and spreads 0.272 evenly over the vocabulary.

| Arm | K2 Spider / BIRD | A1 Spider / BIRD | A3 Spider | A3 DK | A3 BIRD |
|---|---:|---:|---:|---:|---:|
| `hinton_k2aaa` | 62.28 / 43.61 | 71.57 / 36.77 | 72.53 | 58.32 | 38.53 |
| `virtual_k2aaa` | 56.19 / 44.07 | 67.99 / 39.05 | 70.50 | 55.70 | 39.83 |
| `gold_k2aaa` | 59.09 / 43.48 | 70.12 / 40.74 | 70.41 | 52.34 | 40.03 |

- Hinton - virtual: Spider K2 +6.09 (109/46, p<.001), A1 +3.58 (p<.001), A2
  +1.74 (p=.073), A3 +2.03 (54/33, p=.031); A3 DK +2.62 (29/15, p=.049),
  Realistic +0.98, SYN +1.35 (both n.s.); BIRD A1 -2.28 (p=.013), A3 -1.30
  (p=.19).
- Virtual - gold: Spider K2 -2.90 (p=.014), A1 -2.13 (p=.020), A3 +0.10
  (38/37); A3 DK +3.36 (34/16, p=.015); BIRD A3 -0.20.

Reading, against the guide written before the run (entry 2026-10-13):

- Spider: virtual is at or below gold at every endpoint, and Hinton - virtual
  (A3 +2.03) matches Hinton - gold (+2.13). This is the guide's "edge comes
  from where the teacher puts its mass" case. At K2 and A1 virtual is clearly
  below gold, so the guide's rule applies: compare Hinton with the better of
  the two, which is gold there (K2 +3.19); the reading does not change.
- DK: both contrasts positive. Of the +5.98 Hinton - gold at A3, smoothing
  accounts for +3.36 and the teacher for +2.62 (p=.049).
- BIRD: the extra erosion after Hinton K2 is teacher-specific: virtual tracks
  gold on BIRD (A1 39.05 vs 40.74, A3 39.83 vs 40.03) while Hinton drops to
  36.77 at A1 (-2.28 against virtual).
- Other readings: the uniform spread over about 152k tokens is a harsher
  smoother than label smoothing with epsilon 0.1 (Spider K2 -2.90 against
  gold), so the standard LS control stays open; at A3 it would sit between
  gold and virtual, both about 2 points under Hinton on Spider, so it is not
  expected to change the Spider reading. "Teacher-specific" is not yet
  "7B-specific": a smaller teacher's (or the student's own) distribution
  could give part of it, untested. One seed; p values near .05 are
  directions, not claims.
- Together with `central_mix` (entry below): with the teacher, K2AAA is level
  with pooled training on Spider and DK, and the Spider part of that is not
  explained by smoothing. The open weakness is BIRD retention after the
  teacher stage.

Next (exploration choice, owner to confirm by running): P2.40 TAID on one
GPU, since the teacher-specific signal is what a stronger KD objective would
raise; P2.42 central from the Hinton K2 adapter on the other, since its BIRD
trajectory shows whether the BIRD erosion comes from federated averaging or
from Spider-only training after K2. P2.41 (Hinton T=1) runs only if P2.40 is
ahead of Hinton. LS epsilon 0.1 and a self-distillation control are
candidates for the confirmation set, not queued.

## 2026-10-16: P2.37 `central_mix` published; teacher K2AAA level with it on Spider and DK, not on BIRD

Evidence: nested `5b01fc1` (`central_mix`), `4acba5b` (P2.39 pilot A1, as
logged 2026-10-13; B-only client upload 206.4 MB against a 369.6 MB full
adapter payload per round). Seed 0, dev sets, exploratory, exact McNemar.
`central_mix`: all Spider train rows and the 9,428 BIRD rows in one place,
gold CE, three epochs; no privacy and no teacher.

| Arm / stage | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| `central_mix` E1 / E2 | 68.28 / 71.66 | | | | 39.57 / 44.20 |
| `central_mix` E3 | 73.21 | 62.99 | 58.90 | 58.69 | 43.68 |
| `hinton_k2aaa` A3 | 72.53 | 61.81 | 56.38 | 58.32 | 38.53 |
| `gold_k2aaa` A3 | 70.41 | 61.22 | 56.38 | 52.34 | 40.03 |
| P2.27 `central` E3 (Spider only) | 71.37 | 61.61 | 56.00 | 58.50 | 25.75 |

- `central_mix` E3 - `hinton_k2aaa` A3: Spider +0.68 (67/60, p=.60), DK
  +0.37 (p=.90), Realistic +1.18 (p=.58), SYN +2.51 (92/66, p=.046), BIRD
  +5.15 (202/123, p<.001).
- `central_mix` E3 - `gold_k2aaa` A3: Spider +2.80 (83/54, p=.016), DK +6.36
  (53/19, p<.001), BIRD +3.65 (p=.002).
- Matched passes over the private data, `central_mix` minus `hinton_k2aaa`:
  E1-A1 Spider -3.29 (p=.007), E2-A2 -0.19, E3-A3 +0.68; BIRD +2.80, +5.54,
  +5.15.
- `central_mix` - `central` E3: Spider +1.84 (p=.14), BIRD +17.93.

Reading (one seed):

- Private domain: `hinton_k2aaa` is level with pooled training on Spider and
  DK (under one point, unresolved), while `gold_k2aaa`, with the same public
  data and no teacher, stays below (Spider -2.80, DK -6.36). Within K2AAA,
  the gap to pooled training on Spider and DK closes only in the teacher
  arm. Whether that is teacher knowledge or soft-target smoothing is the
  P2.38 question.
- Public domain: the remaining gap is BIRD (+5.15). K2 reaches 43.61, the
  same as `central_mix` E3 (43.68); the private rounds then lose it (36.77 at
  A1, 38.53 at A3). The measured FL loss in this setup is forgetting of the
  public domain after K2.
- Other readings: Spider parity is within the one-seed noise (about 2
  points), so "level" is not "equal". `central_mix` has no teacher, so it is
  a pooled-data reference, not a ceiling for a teacher method.
- For the queue: P2.40 changes the K2 target and so aims at the teacher
  effect on Spider and DK, where this seed shows little gap left to
  `central_mix`; BIRD retention after K2 has the largest measured gap and no
  queued arm targets it. P2.40 and P2.41 start only after P2.38 is read.

## 2026-10-13: frozen A dropped; P2.41 Hinton T=1 and P2.42 central from K2 queued

Owner decision: the frozen-A line stops at the P2.39 pilot (entry below) and
RoLoRA is not queued. The pilot's A1 is still published (P2.39 step 5).

Two arms added, both written before any of their results (exploration, seed
0, dev sets). They are pulled with P2.40; P2.41 runs next to P2.40 on the
other GPU. Amended 2026-10-14, before any P2.41 or P2.42 result, after a
review: the P2.41 readings claimed more isolation than the arm gives, and the
"about 2 points" marks below set priority for the next step, not pass/fail.

P2.41 (code: nested `9849a46`): `hinton_t1_k2aaa` repeats every
`hinton_k2aaa` command with `--kl-temperature 1` at K2 (the T^2 factor of the
KD term is then 1). Same teacher cache, same 0.5 gold CE + 0.5 KD, same
rounds.

- Why: TAID minus Hinton (P2.40) changes the target and the temperature
  together. TAID minus Hinton T=1 changes only the target. Hinton T=1 minus
  Hinton T=2 tests the temperature recipe: T changes the teacher's and the
  student's distributions and the gradient together, so it does not isolate
  the tail. At T=2 the teacher keeps 0.728 on the gold token and about 80% of
  its off-gold mass is outside its top 10 tokens (P2.38 prepare); at T=1 the
  target is sharper.
- TAID - Hinton T=1 clearly positive (Spider about 2 points or more at K2 or
  A3, DK, or less BIRD erosion after K2): supports TAID's interpolated target
  as the server objective; TAID - Hinton T=2 then says whether it also beats
  the published recipe.
- Hinton T=1 clearly below Hinton T=2: the temperature recipe matters, which
  suggests without showing that the softened tail carries part of the effect.
  Sampled KD (Anshumann et al., ACL 2025) keeps an unbiased sample of the
  teacher's tail and would test it directly; it is mainly an efficiency
  method, so it enters only as that test.
- All three near each other: neutral. Temperature and TAID's interpolation do
  not change the teacher effect at this scale; other KD forms stay open.
- Teacher contribution of each arm = arm minus `gold_k2aaa`, read as in the
  P2.38 and P2.40 guides. The P2.41 summary holds every contrast; its analysis
  needs the finished P2.40 run.

P2.42 (code: nested `129c8ee`): `central_k2` repeats the P2.27 `central`
command (all 8,659 Spider train rows pooled, three epochs on one cosine
schedule, epoch snapshots) from the published `hinton_k2aaa` K2 adapter.
Epoch N sees the private data N times, as round aN does (one local epoch per
round), so eN is read against aN (R9).

- Why: it measures the FL penalty after K2, which decides whether a
  federated-side method has room.
- Main contrast: `central_k2` eN - `hinton_k2aaa` aN, Spider and BIRD at each
  pass, all five sets at pass 3. Reference, recomputed in the summary: the
  P2.27 penalty from the base model (central - FL: Spider +1.93, +2.90,
  +3.77; BIRD about 0).
- Penalty after K2 about as large as from base (Spider about 2 points or more
  at pass 2-3): the private rounds limit what K2 gives; a client-side method
  that keeps the K2 knowledge during FedAvg has room (candidate: FedDAT, Chen
  et al., AAAI 2024; it would need its own entry).
- Penalty after K2 within about 1 point: little room on the FL side; method
  effort stays on the server objective.
- BIRD: if `central_k2` E1 also falls from 43.61 (K2) by a similar amount as
  `hinton_k2aaa` A1 (36.77), the erosion comes from Spider training itself,
  not from aggregation, and an FL-side method will not stop it.
- `central_k2` - P2.27 `central` at each pass: whether the K2 start helps
  pooled training as it helps FL (for reference, `hinton_k2aaa` A3 is 1.16
  Spider points above central E3 from the base model).
- A comparator, not an upper bound: Spider only, the same schedule, and E3
  may be past its peak.

Cost: P2.41 about 20 h on one GPU; P2.42 about 7-8 h of training plus nine
evaluations (about 3-4 h).

## 2026-10-13: P2.39 frozen-A pilot: Spider lower, BIRD erosion not stopped

Evidence: on the server, not committed yet; published with P2.39 step 5 after
the P2.40 pull (nested `e0d1f55` lets the lister publish A1 alone). Seed 0,
dev sets, exploratory. One private round from the published Hinton K2 adapter
with LoRA A frozen (`hinton_k2_fa` A1), against the same round with A trained
(`hinton_k2aaa` A1).

| Arm, A1 | Spider | BIRD |
|---|---:|---:|
| `hinton_k2_fa` (A frozen) | 70.02 | 37.61 |
| `hinton_k2aaa` (A trained) | 71.57 | 36.77 |

- Spider -1.55 (9/25, p=.009, Wald [-2.65, -0.45]); BIRD +0.85 (50/37,
  p=.20).
- Communication per round: client upload 206.4 MB (B only) against 369.6 MB
  for full adapters, -44%. B is 56% of this adapter because the MLP gate and
  up projections have wide outputs. Broadcast has the same ratio.
- Pre-written reading: Spider clearly lower, so the guide's next step is
  RoLoRA.
- Reading against the mechanism: BIRD falls from 43.61 at K2 to 37.61 with A
  frozen and to 36.77 with A trained, so about 88% of the first-round erosion
  (6.00 of 6.84 points) goes through B alone. The hypothesis behind frozen A
  (the K2 knowledge sits in A) is not supported. RoLoRA alternates A and B to
  fix how the two factors are aggregated; it does not target this erosion, so
  here it would only carry the communication saving.
- Alternative reading: B-only training may need a larger learning rate
  (FFA-LoRA tunes it). That could recover Spider, but moving B more would not
  reduce the erosion, and each retuned variant adds dev selection.
- Known trade-off from earlier arms: client retention toward the K model
  keeps BIRD but costs Spider (`hinton_v1` with A[ntd]: Spider 69.25, BIRD
  43.29; `h_plain`: 71.76, 39.96).
- Recommendation, for the owner to decide: stop the frozen-A line at the
  pilot and do not queue RoLoRA. Meanwhile GPU 1 runs P2.37 `central_mix`
  (no new code).

## 2026-10-13: P2.40 TAID at K2 queued

Code: nested `c5d9735` (TAID in the Hinton public stage), `02c30d3` (runner).
Written before any P2.40 result; exploration, seed 0, dev sets.

`taid_k2aaa` repeats every `hinton_k2aaa` command; only the K2 soft target
changes, to TAID (Shing et al., ICLR 2025; official SakanaAI/TAID code): the
target is softmax((1-t) * detached student logits + t * teacher logits), the
loss is forward KL to it, `t` goes from 0.4 to 1 with alpha 5e-4 and beta 0.99,
and there is no temperature (T=1).

Choices that are ours, not the paper's:

- Loss 0.5 gold CE + 0.5 TAID KL, as in the Hinton reference; the paper
  trains on the KD loss alone.
- `t` moves once per optimizer update (16 accumulated rows), on the mean TAID
  loss of that update, as in the paper's algorithm (one step per batch). The
  official code calls the update on every forward call, which with gradient
  accumulation would move `t` up to 16 times per update.
- With 1,180 K2 updates, `t` follows the linear floor exactly: the adaptive
  step, alpha * sigmoid(momentum) * (1 - t), is at most 3e-4, below the
  floor's increment 0.6 / 1,180 = 5.1e-4. P2.40 therefore tests TAID's
  interpolated target on a linear schedule; the adaptive part is inactive at
  the published alpha. The K2 metrics record `t` after every update.

How to read it (comparators: published `hinton_k2aaa` and `gold_k2aaa`, and
P2.38 `virtual_k2aaa` once published):

- TAID minus Hinton changes the target and the temperature (1 against 2). It
  compares the two published objectives and does not isolate the
  interpolation; if TAID is ahead, a Hinton arm at T=1 separates the two.
- Main look: the teacher contribution, arm minus `gold_k2aaa`, at K2 and A3 on
  Spider, DK and BIRD, against Hinton's (Spider K2 +3.19, A3 +2.13; DK A3
  +5.98; BIRD A1 -3.98, A3 -1.50), and whether BIRD erodes less after K2
  (Hinton 43.61 at K2, 36.77 at A1).
- One seed: a Spider question is about 0.1 point and Spider differences under
  about 2 points are not resolved; a non-significant difference is not
  equivalence. A choice made from this result goes to the confirmation runs.
- Cost: K2 about 7-8 h, three rounds and evaluations about 12 h, on one GPU.
  Step 1 pulls code every lane imports, so it runs only when no lane runs.

## 2026-10-13: working direction beyond K2AAA; P2.39 frozen-A pilot queued

Owner decision: K2AAA alone is too simple to be the paper's contribution; it
becomes the strongest simple baseline the method must beat. Working direction
(not fixed; the story is fixed only before confirmation):

- Server: a stronger KD objective at K for the 7B to 1.5B gap, TAID (Shing et
  al., ICLR 2025), reusing the P2.27 logit cache. Code after P2.38.
- Clients: freeze LoRA A after K2 and train and send only B, FFA-LoRA (Sun et
  al., ICLR 2024). Here A is the one learned at K2 (with or without the
  teacher), not a random A. Upload is about half (P2.39 records exact bytes).
- P2.38 (virtual teacher) runs first. Remaining P2.37 arms: `central_mix` and
  `local` after P2.38 and P2.39; the `akaka_plain` pair is deferred, needed
  only if the paper claims the K-first schedule.

Why frozen A: the private rounds erode what K2 learned (Hinton BIRD 43.61 at
K2, 36.77 at A1; gold 43.48 to 40.74), and the Spider questions behind the
teacher edge change between K2 and A3 (entry below).

P2.39 (code: nested `fe5ed88`, `7e8e3ba`): `hinton_k2_fa` and `gold_k2_fa`
repeat the private rounds of the P2.37 K-first arms from the same K2 adapters
with `--client-freeze-lora-a` as the only change. Pilot: one round of
`hinton_k2_fa`. How to read the pilot (written before it runs; exploration):

- Against `hinton_k2aaa` A1 (Spider 71.57, BIRD 36.77). BIRD clearly higher
  (one BIRD question is about 0.065 point; about 2 points is resolvable) with
  Spider within about 1 point: continue to A3 and run `gold_k2_fa`.
- Spider clearly lower (B alone underfits the private data): try RoLoRA
  (Chen et al., 2024, alternating A and B) instead.
- Both flat: frozen A brings only the communication saving; keep it only if
  the paper wants that claim.

## 2026-10-13: P2.37 K-first pair; P2.38 virtual-teacher control queued

Evidence: nested `5cfd646` (`hinton_k2aaa`), `dcac509` (`gold_k2aaa`). Seed 0,
dev sets, exploratory. Both arms train two server epochs on the 9,428 BIRD rows
from the base model (K2), then three plain private rounds.

| Arm / stage | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| `hinton_k2aaa` K2 / A1 / A2 | 62.28 / 71.57 / 71.86 | | | | 43.61 / 36.77 / 38.66 |
| `hinton_k2aaa` A3 | 72.53 | 61.81 | 56.38 | 58.32 | 38.53 |
| `gold_k2aaa` K2 / A1 / A2 | 59.09 / 70.12 / 69.83 | | | | 43.48 / 40.74 / 39.90 |
| `gold_k2aaa` A3 | 70.41 | 61.22 | 56.38 | 52.34 | 40.03 |

- Hinton - gold, Spider: K2 +3.19 (95/62, p=.010), A1 +1.45 (p=.14), A2
  +2.03 (p=.038), A3 +2.13 (52/30, p=.020, Wald [+0.42, +3.84]). At A3: DK
  +5.98 (36/4, p<.001), Realistic +0.59, SYN 0.00, BIRD -1.50 (p=.12). BIRD at
  A1 -3.98 (p<.001): the first private round erodes BIRD more after Hinton.
- `hinton_k2aaa` A3 against references: FL Spider +4.93, DK +5.05, BIRD
  +12.84; `central` Spider +1.16, DK -0.19. `gold_k2aaa` A3 against `central`:
  DK -6.17 (p<.001); against `g_plain`: Spider -0.97 (p=.34).
- Reading: under K-first the teacher edge is made in K2 and the net Spider
  gap at A3 is about two thirds of the K2 gap; on DK it is large. The
  questions behind the gap change: of the 95 questions only Hinton solved at
  K2, 8 are still Hinton-only at A3 and 76 are solved by both; only 8 of the
  52 Hinton-only questions at A3 were Hinton-only at K2. So the two-thirds
  ratio describes the net gap, not retained knowledge, and does not predict
  how much of a larger K gain would survive. One seed; DK as a subgroup is a
  hypothesis until other seeds confirm it (R8).

Open alternative reading. The Hinton K loss is 0.5 gold CE + 0.5 T^2 KL to the
teacher at T=2. Any soft target regularizes, and Yuan et al. (CVPR 2020,
"Revisiting Knowledge Distillation via Label Smoothing Regularization") get
much of the KD gain from a hand-made "virtual teacher". The edge could come
from the softening, not from what the 7B knows. Two controls are not used:

- Gold CE weighted 0.5: AdamW updates do not change when the whole loss is
  scaled, so it equals `gold_k2aaa`.
- KL toward the base model (anchoring): gold K2 already keeps Spider at the
  base level (59.09 vs base 59.19), while Hinton K2 is 3.1 points above it;
  less forgetting cannot explain a gain above base. Lower priority.

P2.38 (code: nested `4a8225c`, `94ed37b`): `virtual_k2aaa` repeats every
`hinton_k2aaa` command with the teacher replaced by the Tf-KD_reg virtual
teacher of Yuan et al.: probability `a` on the gold token, the rest spread
evenly over the vocabulary, same T=2 and 0.5/0.5 weights, no teacher model or
cache. `a` is the real teacher's mean gold-token probability at T=2 on the same
rows (read from the P2.27 cache at prepare time, weighted as the loss weights
rows), so both arms move the same probability mass off the gold token and
differ only in where it goes. Prepare also records the teacher's mass on its
top 10 non-gold tokens and its entropy. Owner decision 2026-10-13: run it
before the remaining P2.37 arms.

How to read P2.38 (written before any P2.38 result; exploration, no pass/fail;
amended the same day, still before any result, after a second review):

- Main contrasts at every endpoint: `hinton_k2aaa - virtual_k2aaa` (teacher
  knowledge beyond the softening) and `virtual_k2aaa - gold_k2aaa` (softening
  alone).
- One seed gives a direction, not a verdict. A non-significant difference
  does not show two arms are equal; seed 0 only decides whether this control
  joins the confirmation set.
- Virtual near gold, Hinton - virtual near Hinton - gold (A3: Spider about +2,
  DK about +6): supports that the edge comes from where the teacher puts its
  mass, not from the softening.
- Virtual near Hinton: weakens the case that the 7B teacher is needed in this
  recipe; the owner decides whether to confirm it over seeds and how the story
  changes. It says nothing about other KD forms (TAID and others need their
  own comparison).
- Both contrasts positive: report the split between the two.
- Virtual clearly below gold: the even spread over about 152k tokens may be a
  harsher regularizer than the teacher's own target. Compare Hinton with the
  better of gold and virtual, say so, and read it with the top-10 mass from
  prepare. The next control is then standard label smoothing on gold CE
  (epsilon 0.1; Szegedy et al., CVPR 2016).
- If prepare gives a low `a` (the virtual target then moves much mass), the
  owner may add that epsilon 0.1 arm before the run; `a` is a teacher
  statistic, not a result.
- Precision at one seed: one Spider question is about 0.1 point, one DK
  question about 0.19 point; Spider differences under about 2 points are not
  resolved.

## 2026-10-12: rules simplified (owner decision)

Why: the old rules wrote a pass/fail criterion before every exploratory run
and fixed the phase E arm list. That slowed exploration (37 phases, story
still open) and blocked plain diagnostics, such as checking whether client
drift exists before testing a method against it. What those rules protect is
narrower: the same dev numbers must not both choose a configuration and serve
as its evidence. With about 140 discordant questions per Spider dev contrast
(standard error about 1.1 points), the best of ten variants with no true
effect still shows about +1.7 points, and roughly 40% of such searches yield
one p<.05 (independent contrasts assumed; shared data lowers it somewhat).

New rules (also in both `AGENTS.md` files and `RESEARCH_STATE.md` section 5):

1. Exploration is open: on seed 0 and the dev sets, any result may choose the
   next arm, setting, schedule or direction; arms may be added after reading
   results; no pass/fail rule is needed first. Every run and choice is logged
   here.
2. Freeze, then confirm: a dated entry fixes method, configuration,
   comparators, test and claims before any seed 1-2 run or Spider test
   evaluation. Paper claims come only from those confirmation runs. Kept with
   this rule: R10, R13, R8.
3. Disclose: the paper states what was tried on dev and calls dev numbers
   exploratory.

- Retired: R1-R6, R11, R12 and the fixed phase E arm list. Outcomes recorded
  under them stand as history. R9 stays as a reporting practice.
- P2.37 keeps running as baselines; new arms may be added.
- Owner constraint, same day: the teacher runs only at the server, on public
  data. A first proposal with client-side teacher KD was rejected.
- A second proposal (shared teacher replay: server-computed teacher soft
  labels on a shared BIRD subset, replayed inside private rounds) was also
  rejected.
- Direction proposal (teacher teaches short CoT at the server on BIRD; clients
  self-generate and execution-check CoT for their private rows; pilot with
  stop criteria first): [`DIRECTION_PROPOSAL.md`](DIRECTION_PROPOSAL.md).

## 2026-10-12: P2.36 `g_plain` published; teacher edge on Spider gone with a plain last round

Evidence: nested `31a568e` (`audits/protocol_v2/p236_g_plain_s0/summary.md`).
`g_plain` = P2.27 gold v1 K2 plus one plain private round, the gold control
of `h_plain`. Seed 0 dev, descriptive (phase E, no decision rule).

| Contrast | Spider | Realistic | SYN | DK | BIRD |
|---|---|---|---|---|---|
| `g_plain` (EX) | 71.37 | 61.02 | 56.09 | 54.39 | 40.35 |
| `g_plain` - gold v1 A3 (plain vs NTD last round) | +3.48 (69/33, p<.001) | +1.97 (p=.26) | +0.48 (p=.69) | +1.50 (p=.30) | -1.04 (p=.21) |
| `h_plain` - `g_plain` (teacher - gold, plain) | +0.39 (50/46, p=.76) | +1.97 (p=.25) | +2.90 (76/46, p=.008) | +1.68 (p=.21) | -0.39 (p=.73) |
| Hinton v1 - gold v1 (teacher - gold, NTD; P2.27) | +1.35 (p=.23) | +1.77 (p=.36) | +0.77 (p=.58) | +4.67 (p<.001) | +1.89 (p=.076) |
| `g_plain` - FL A3 | +3.77 (90/51, p=.001) | +1.38 (p=.46) | +2.42 (p=.068) | +1.12 (p=.52) | +14.67 (p<.001) |
| `g_plain` - central E3 | +0.00 (97/97) | -0.59 (p=.84) | +0.10 (p=1) | -4.11 (30/52, p=.020) | +14.60 (p<.001) |

The last two rows were computed locally from the published predictions with
the P2.27 paired test (not in the P2.36 summary).

- Teacher - gold on Spider dev is +0.39 with a plain last round, against
  +1.35 with NTD. At Coder-1.5B the Spider edge of soft labels does not
  survive a plain private round (consistent with F4: the round repairs what
  gold K forgets; gold gains +3.48 from it, Hinton +2.51).
- On the three robustness sets teacher - gold is positive in all six cells
  (two chains), but which set reaches p<.05 changes (DK with NTD, SYN plain)
  and both chains share A1 and K1. Exploratory: a hypothesis for seeds that
  did not generate it (R8), not a finding.
- Gold labels alone take the pipeline to central on Spider dev (71.37 both)
  and add 14.6 BIRD points; the pipeline has more passes than central E3, so
  this is not a matched-pass comparison (R9). DK stays 4.1 below central.
- Open for the teacher (Q2): the K-first pair (`hinton_k2aaa`, `gold_k2aaa`)
  and the interleaved plain pair in P2.37.

## 2026-10-11: P2.27 `central` published; R3 and R9

Evidence: nested `5767704` (final P2.27 manifest and summary). Central Spider
E1-E3 on the same 8,659 rows, one continuous 3-epoch cosine run; E1 and E2
are snapshots inside that schedule. Central minus FL at matched passes:

| Passes | Spider all | Spider JOIN (408) | Spider no-JOIN (626) | BIRD |
|---|---|---|---|---|
| 1 (E1 - A1) | +1.93 (90/70, p=.13) | +5.39 (p=.032) | -0.32 (p=.90) | +0.65 (p=.55) |
| 2 (E2 - A2) | +2.90 (102/72, p=.028) | +4.17 (p=.12) | +2.08 (p=.14) | +0.33 (p=.78) |
| 3 (E3 - A3) | +3.77 (104/65, p=.003) | +4.41 (p=.079) | +3.35 (p=.020) | +0.07 (p=1) |

Central E3: Spider 71.37, Realistic 61.61, SYN 56.00, DK 58.50, BIRD 25.75.

- R3 (rule written before this result): central E3 - FL A3 = +3.77 >= 3.0,
  so by the rule's wording client drift is "a target worth a method". R5
  still fails (R2 did not support erasure), so ExST stays dropped. The rule
  measures the size of the FL penalty, not its cause.
- R9 (descriptive): unlike 0.5B alpha 0.5 (+4.6/+4.8/+1.8, central
  overfit at E3), the Coder-1.5B penalty grows with passes. FL peaks at A2
  (68.28) and drops at A3 (67.60) while central keeps rising. The JOIN gap
  appears first (pass 1); the no-JOIN gap opens later. BIRD shows no penalty.
- Earlier split-audit reading ("the penalty mostly vanishes at E3; likely
  fewer effective steps, not drift") was 0.5B-specific; at Coder-1.5B the
  cause is open (Q1 in RESEARCH_STATE).
- Descriptive, not a claim: Hinton v1 - central Spider -2.13 (p=.11), BIRD
  +17.54; `h_plain` (71.76) is level with central E3 on Spider.

## 2026-10-11: phase E arm list (P2.37), fixed before any run

Coder-1.5B, alpha 0.1, seed 0, P2.27 recipe and evaluation; Spider dev, its
variants and BIRD dev only. Code: nested `ed6fa57`
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
numbers: nested `4386775` (`scripts/audit_power_clustered.py`,
`audits/protocol_v2/power_clustered/`).

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

Evidence: nested `19274e9` (`scripts/audit_test_suite_ex.py`,
`audits/protocol_v2/test_suite_ex_s0/`). CPU only, on published predictions. A prediction is
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
