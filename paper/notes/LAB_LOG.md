# FedLS-SQL lab log

Newest first. Each entry says what ran, the key numbers, where the evidence
lives, and what was decided. All numbers are seed 0, EX (%), protocol v2,
unless stated.

Older entries:

- 2026-10-10 to 2026-10-29 (Coder-1.5B K-chain, replay, freeze, P2.27-P2.54):
  [`LAB_LOG_2026-10-10_to_2026-10-29.md`](../archive/lab_log_2026-10/LAB_LOG_2026-10-10_to_2026-10-29.md)
- 2026-09-24 to 2026-10-09 (Coder-0.5B, Qwen2.5-1.5B-Instruct, P2.2-P2.26):
  [`LAB_LOG_2026-09-24_to_2026-10-09.md`](../archive/lab_log_2026-10/LAB_LOG_2026-09-24_to_2026-10-09.md)
- 2026-09-03 to 2026-09-26, full text:
  [`LAB_LOG_2026-09-03_to_2026-09-26.md`](../archive/lab_log_2026-09/LAB_LOG_2026-09-03_to_2026-09-26.md)
- Protocol v1 (no BIRD evidence): `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`
- Before FedLS-SQL: `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`

## 2026-11-05: owner keeps Spider as the target; CoT literature re-read

Owner: the two-domain framing is secondary; the target is beating the baselines on the private domain (Spider).
DIRECTION section 6 now judges step 1 on Spider only (Hinton - gold at least +1 on dev and test, else try Q).

CoT reading (full text; LITERATURE section 3.1): pro-CoT RL results sit at 7B and above, mostly on BIRD, often
with a GPT-4o teacher or voting; on Spider dev Liu et al. show +0.6 to +1.1 for CoT DPO, and AutoThinkSQL
(train BIRD, eval Spider, greedy) shows CoT DPO 69.14 against SQL-only 84.23. Liu et al. Table 7: SQL-only DPO
with an SFT loss gains +1.2 on BIRD, the size of `g3d` - `g2` here. VCoT-SQL gains mostly from filtering
writer traces, with CoT written on Spider train itself, which the teacher may not do here. `cot1` used 1,266
BIRD rows (pilot 300 plus 1,700 sampled); teacher CoT over all of BIRD was never generated.

## 2026-11-05: independent review of the directions; "P on two domains" proposed for the owner

An agent acting as a Q3 reviewer read the notes (not the discussion) and judged P, Q, R, D. Readings, with
the project's numbers it cited checked against the logs:

- RL compresses gaps between starting points: `sql2_e1` over `sql1_e2` +14.80 becomes `sql_rl9` - `s1_rl9`
  +1.35; `tp1` - `g1` -2.61 becomes `tp_r3` - `g_r3` -1.35. The Hinton - gold K2 gap (about 3.2 dev) is
  likely under 1 Spider point after RL.
- Teacher-specific effect on Spider is +0.47 test (K3); on BIRD dev it is large (replay teacher - gold
  +4.04, p<.001). Proposed: report Spider (RL) and BIRD dev (teacher) together, if federated DPO keeps the
  BIRD gain that SFT rounds erode (43.61 to 36.77). Rough odds from the reviewer: P on Spider alone about
  35%, P on two domains about 50%, Q alone 20%, R as main axis 10-15%, D alone 25%.
- Correction: FedCoLLM-style was run at seed 1 (Spider test 66.88, dev 63.73, BIRD dev 43.42, nested
  `ce51178`); earlier chat said it was never run.
- Overstated claims fixed in DIRECTION and RESEARCH_STATE: the "2-3 points on test" estimate for P (no SQL
  route has a test number), R2 (not equivalence; reward uses gold execution), R5 (different conditions from
  Liu et al., not a contradiction), C1 (starting points differ in data), K1 used as teacher evidence (it mixes
  public data and teacher), K2 (dev only), the FL gap (small on test, +3.77 on dev).

DIRECTION section 6 now lists the ordered plan (steps 0-6, about 250-300 GPU-h). Step 0 is eval only;
step 1 compares the `s1` route from the Hinton K2 adapter with the same route from the gold K2 adapter.
Owner has not approved.

## 2026-11-05: directions re-assessed again; P (teacher KD + federated execution DPO) recommended

Owner: RL need not be a new mechanism; apply it in the framework so EX clearly beats the baselines, not as a
fix for federated drift. KD on public at the server with private clients is the intended deployment.

Search (abstracts and excerpts): no paper found with federated learning plus RL or DPO for Text-to-SQL;
federated Text-to-SQL exists without teacher or RL (Zhang et al., ACL 2023); federated DPO (FedPDPO,
OpenFedLLM, POPri) and federated RLVR (FedMOA, PubSwap, Fed-GRPO) exist for other tasks; server-LLM KD in FL
exists for general tasks (FedCoLLM, FedMKT, FedCoT, KnowledgeSG). Liu et al. (ACL 2025) report that DPO
without CoT rarely helps on BIRD at 6.7B-15B; here SQL-only DPO + NLL works at 1.5B on Spider, and the
preference term carries it (P2.59 `g3d - g3n` +2.22, p=.004). CoT is therefore not a default for this setup;
BIRD dev, where CoT papers report gains, is untested for the CoT routes.

DIRECTION.md now recommends P (Hinton KD at the server, then federated execution DPO + NLL), with Q (teacher
pairs on public) as a teacher-in-RL complement, R (CoT as a variant) and D (CoT explorer) as extensions. The
deciding check before building FL: the P2.62 `s1` route from the `hinton_k2aaa` K2 adapter against `s1` from
`sql1_e2` (about gold K2). Owner has not chosen.

## 2026-11-05: directions re-assessed; candidate D, CoT as explorer for all-wrong questions (owner criteria)

Owner criteria: the paper is a framework that applies to the federated setup (the FedAvg-central gap is small on
this split), the roles of the teacher and of RL must both be clear, CoT and teacher are dropped only if evidence
shows they do not help, and the RL mechanism must be new and clearly effective. Re-assessed in DIRECTION.md:
A (KD start + federated DPO + replay), B (federated CoT-DPO) and C (teacher on-policy distillation at the
server) lack an RL mechanism of their own; A and B also have weak teacher roles on Spider test.

CPU check on published retry manifests (`p262_rl_from_bird_s0/data/{c1,s1}_rl8_rows.json`, nested `1eeaa6a`;
same question sets and rounds, neither route saw Spider gold): of 1,200 questions where all 8 `s1` SQL samples
failed, `c1` CoT sampling produced at least one correct SQL on 508 (42.3%); `s1` solved 386 of the 1,078 that
`c1` failed. `s1`'s own retry from a better checkpoint rescued 23.83%. The P2.60 SQL route rescued 996 (83.0%),
but it was SFT-trained on these questions' gold, so it is no explorer control. Fresh-round all-wrong counts:
about 1,078 (CoT) against about 1,400 (SQL).

Candidate D: the student learns a CoT mode from teacher CoT on BIRD; at clients the CoT mode explores the
questions the SQL mode fails completely, execution-checked SQL it finds becomes the chosen response for the
SQL-mode prompt, and only SQL mode is deployed. Closest work (abstracts only so far): AAPO, ADHint, LUFFY,
ReToolSQL and SERL-SQL need the teacher on the training question; PubSwap and Fed-GRPO have no teacher;
Masked Distillation and System 2 distillation move CoT-conditioned outputs into an answer-only policy and need a
careful read. Required controls: gold as chosen on the same questions, a second non-gold SQL explorer, and a
CoT mode learned without the teacher. Proposed pilot (not built): one DPO + NLL round from `s1_rl9` with
`c1_rl8` rescue pairs, gold-chosen pairs, or a plain retry. Owner has not chosen.

## 2026-11-04: workspace cleanup; old directions closed (owner)

Owner: drop the earlier directions and focus on combinations of teacher KD, CoT, RL, federated learning and
Text-to-SQL that are meaningful and not duplicated by prior work. Closed, not to be resumed by default:
P2.53 seed 2 and the rest of the FREEZE confirmation, E2 (0.5B student), P2.46, P2.41, P2.43 `central_bird`,
P2.37 `akaka_plain`. Their published results stay valid as evidence and baselines.

Docs: notes reduced to RESEARCH_STATE, DIRECTION (candidate directions, owner to choose), PIPELINE_NEXT,
LAB_LOG, RESULT_REGISTRY, LITERATURE and system_architecture. The 2026-10-28 direction, the 2026-11-03
federated CoT-RL proposal, COT_RL_RESEARCH, the novelty matrix and related_papers moved to
`paper/archive/directions_2026-11/`; the previous queue to
`paper/archive/completed_runbooks/PIPELINE_P227_P262_2026-11-04.md`; log entries up to 2026-10-29 to the
archive file above. Code cleanup in the nested repo: entry of the same date there and in its `AGENTS.md`.

## 2026-11-04: P2.62 `c1` and `s1` through RL9, P2.60 SQL to `sql_rl9`, `c1` Spider test (nested `1eeaa6a`)

Round 7 is empty on both routes (rounds 1-6 cover all about 6,997 eligible questions); rounds 8-9 are retries on
still-unsolved questions.

| Route | Start (dev) | Best (dev) | Best - start | Execution error at best | Tokens p50 | Spider test |
|---|---:|---:|---:|---:|---:|---:|
| `c1` (teacher CoT BIRD, then RL) | `cot1_e4` 60.64 | `c1_rl8` 70.89 | +10.25 (151/45) | 6.29 | 198 | 69.12 |
| `s1` (SQL BIRD, then RL) | `sql1_e2` 58.80 | `s1_rl9` 74.18 | +15.38 (184/25) | 5.13 | 25 | not run |
| P2.60 SQL (Spider SFT, then RL) | `sql2_e1` 73.60 | `sql_rl9` 75.53 | +1.93 | | | not run |

- Matched routes, dev: `c1_rl8 - s1_rl9` -3.29 (73/107, p=.014). CoT started 1.84 above SQL and ends 3.29 below.
  `s1` is still rising at the budget end (retries +2.03, +1.07); `c1` peaked at RL8 and fell 1.06 at RL9.
- CoT samples more correct answers on the same question sets (pass@8 84.9-86.3 against 81.1-82.5 in rounds 3-5)
  and yields more pairs (rounds 1-6: 5,184 against 2,781), yet gains less per round.
- RL alone from the BIRD SQL student reaches Spider SFT level: `s1_rl9 - sql2_e1` +0.58 (95/89, p=.71),
  `s1_rl9 - sql_rl9` -1.35 (81/95, p=.33).
- Spider test (2,147 rows, greedy): `c1_rl1` 63.86 (execution error 8.66), `c1_rl8` 69.12 (6.33, p50 208 tokens,
  peak 8.99 GiB, 0.71 h). `c1_rl8` was chosen on dev. For scale only (different setups): federated SQL-only
  FedAvg A3 scored 71.50 on test (2026-10-28). No SQL-route test number exists yet, so the CoT gap is dev-only.

## 2026-11-04: resume interrupted c1 RL8 and automatically test the best checkpoint

Owner accidentally closed the c1 lane during RL8 training and requested a resume command followed by
automatic Spider test evaluation. The active GPU-1 command now reruns the unchanged lane, waits for its
terminal round-9 eval receipt (including a skipped terminal round), selects the maximum dev EX among
completed c1 RL checkpoints, then fetches and runs the standalone test driver on that point. Ties keep
the earliest checkpoint. Test outputs remain under `p262_c1_spider_test_s0/<selected point>/`.

No trainer or lane code changed. Inspection confirms DPO saves adapter weights only after the full
training call; it has no mid-task optimizer resume. Consequently, interrupted RL8 DPO restarts from
its original parent using the already saved rollouts. Completed receipts are reused. The command never
pulls or rewrites code used by other running processes. Publication remains separate: the existing test
publication block accepts the chosen point, while the existing lane publication handles RL artifacts.

CPU validation checks the exact best-point selection expression on mocked completed, skipped and tied
rounds, including a best checkpoint before round 9. No GPU or PowerShell execution ran locally.

## 2026-11-04: fix empty Spider test row IDs in the standalone driver

The server launch failed with "expected 2147 unique Spider test rows, got 2147" before model loading.
Root cause reproduced on the committed CSV: all 2,147 `source_row_id` cells are empty; the test builder
constructs examples without filling this optional field and the loader correctly preserves it. The new
eval driver incorrectly assumed unique source IDs. Existing mocked tests did not exercise real CSV loading.

Fix (nested `e96cef1`) only the standalone driver's in-memory eval IDs: `test:0` through `test:2146`, assigned by immutable
CSV position. No rows are removed, reordered or rewritten. Bind the ID policy in identity and bump the
driver version to 2. The failed launch produced no predictions to migrate; rerun the same fetch/stdin
command with `--share-gpu`. Live lanes and their imported code are unchanged.

Validation: 48 targeted CPU tests pass, including real-format CSV loading with empty/repeated source IDs,
preservation of repeated questions and SQL order, deterministic reload and unchanged CSV bytes. Also
loaded the actual committed 2,147-row Spider test CSV with all database paths present: 2,147 unique eval
IDs, first `test:0`, last `test:2146`; input SHA-256 unchanged. No GPU inference ran locally.

## 2026-11-04: allow c1 test eval alongside running GPU tasks (owner correction)

Owner clarified that the c1 test command should share available GPU capacity with existing tasks rather
than require stopping a lane. Added `--share-gpu` (nested `8514ee4`) to `scripts/eval_p262_spider_test.py`: it skips only the
exclusive P2.37 GPU lock and always retains the per-point output lock. Default behavior without the flag
remains exclusive. CoT prompt, adapter, greedy decoding, batch 16, output identity and resume paths are
unchanged. No smoke prerequisite, Windows counter polling or automatic memory gate was added.

Validation: 45 targeted CPU tests pass, including a run while the GPU lane lock is held and rejection of
a duplicate eval writing the same output. PIPELINE_NEXT now launches shared mode via fetch/stdin and
requires no live-lane stop or checkout pull. Concurrent GPU performance/VRAM has not been measured locally.

## 2026-11-04: standalone c1 Spider test driver (owner request)

Implemented `scripts/eval_p262_spider_test.py` (nested `36dd39b`). It evaluates a completed c1 RL
adapter with the unchanged P2.62 CoT generation engine on full Spider test (2,147 rows), batch 16,
greedy, the same parsing/token limit and Spider execution evaluator. Process-local overrides select
test rows and a separate output path; they are restored on success or failure. Other lane processes,
dev predictions, receipts, training parents and stopping decisions are unchanged.

The driver binds the test CSV, rows, engine, adapter weights/config and source training receipt, rejects
duplicate/foreign rows and incomplete output, resumes partial predictions and verifies completed results
without loading a model. It holds the existing GPU lock and a separate per-point output lock. Same-GPU
overlap is not implemented. Outputs: `audits/protocol_v2/p262_c1_spider_test_s0/<point>/predictions.jsonl`
and `receipt.json`; publication validates the exact two-file allowlist. PIPELINE_NEXT has a Git-fetch/stdin
launch that does not pull or modify the running checkout, plus separate publication after lanes exit.

Validation: 43 CPU tests pass across the new driver, P2.60, P2.62 and RL continuation policy. No GPU or
PowerShell execution ran locally; no new Spider test EX or VRAM measurement is available. The requested
first checkpoint is `c1_rl1`, reported in chat at Spider dev EX 66.83, not a test result.

## 2026-11-04: report both Spider dev and test during development (owner)

Owner requested Spider test results for the current CoT/RL checkpoints and
using test, or both splits, for subsequent method development. Default to
reporting both Spider dev (1,034 rows) and Spider test (2,147 rows). Test
results may inform method and checkpoint choices; they are not held-out.

Local inspection found no test artifacts under the P2.58-P2.62 audit roots.
P2.60/P2.62 evaluation tasks load only Spider dev. No new test inference or
live GPU inspection ran here. Backfill completed checkpoints using separate
outputs; preserve running-lane receipts, adapter selection and stopping.

The owner reports about 50% GPU utilization. Historical P2.59 peaks are
14.5-18.7 GiB for K=8 sampling and 7.6-8.0 GiB for eval (A5000_RUN_CONFIG).
Those measurements do not establish that two simultaneous processes fit
the 21.5 GiB budget. Prefer a free GPU for backfill; overlapping eval with a
live lane needs a measured combined memory budget first. No concurrent GPU
run, new eval implementation or executable-queue change is claimed here.

## 2026-11-03: CoT/RL screens support a federated proposal (owner)

Owner requested one proposal to maintain until federated implementation begins:
[FEDERATED_COT_RL_PROPOSAL](../archive/directions_2026-11/FEDERATED_COT_RL_PROPOSAL_2026-11-03.md). The target stays BIRD
public at the server, Spider private at five clients, frozen 7B teacher and
Coder-1.5B LoRA student. The current centralized experiments support this target.

Target pipeline: teacher CoT BIRD -> student CoT SFT -> public teacher-pair DPO
-> repeated full-local student sampling/execution/DPO -> FedAvg. No self-CoT SFT
Spider in the main route. Keep the current prompt for the first FL test; public
CoT replay and later prompt-format comparisons remain separate extensions.
Full pool describes sampling coverage, not guaranteed SFT/DPO acceptance.

The proposal distinguishes the owner's target from untested pilot settings
(one pair/question, one local epoch, reference from the round's global adapter).
It maps P2.60/P2.62, the SQL references and teacher-pair counting to decisions
needed for FL. OpenFedLLM supports local DPO/adapter aggregation; FedPref is a
structured-output precedent with fixed pairs/reference and client-side teachers,
not a replication of this SQL setup. Current code, commands and GPU lanes are
unchanged; federated CoT-DPO and public teacher-DPO are not implemented here.

## 2026-11-03: RL continuation fixes (owner request, CPU-verified)

The owner requested three fixes: do not stop rising EX after two gains below 1 point; revisit questions whose
rollouts are all wrong; include the initial adapter when selecting the best observed point. The third fix was
partly in nested `4fd5673`; it now also reports the start when no RL update was evaluated.

Code: nested `167af94`, `d45df9e`. Implemented: (1) pin the rising SQL series 73.60, 74.18, 75.05 in a failing CPU regression; (2) retain the
seven immutable fresh-question sets, stop that phase only after two rounds without a new best, then add at most
two K=8 retry rounds of up to 1,200 previously sampled but still unsolved questions from the best prior adapter;
(3) freeze route-specific retry manifests, preserve completed/partial generation identities, archive legacy skip
receipts before reopening them; (4) test the retry/resume/summary behavior and update the active runbook. The
bounded retry schedule and patience are compute choices, not hyperparameters established by a paper. Both server
lanes must exit before pulling changed runner code. Reopening also holds both GPU lane locks, not only child-task
locks. The original seven-set manifest is not rewritten; retry sets have separate frozen manifests that bind
their source receipts. Empty shards load no model; batches with no usable pair skip their update/evaluation.

Validation: 981 CPU tests pass (one existing PyTorch scalar-conversion warning in `test_server_retention`). On a
temporary copy of the committed P2.60 receipts, reopening archives exactly 15 legacy SQL skips and makes
`sql_rl3_samp0` the next task; all successful receipt byte hashes stay identical. No GPU or Windows PowerShell
execution ran locally. PIPELINE_NEXT now has the stop/update/reopen sequence, continuation commands and a joint
publication command that accepts only the two runners' explicit compact allowlists. Old launch blocks are archived.

## 2026-11-03: P2.60 SQL route published (nested `d7c3ccb`)

Seed 0, Spider dev. `sql2_e1` 73.60, `sql_rl1` 74.18, `sql_rl2` 75.05; round 3 skipped by the rule (two gains below
1 point). `sql_rl2 - sql2_e1` +1.45 (31/16, p=.040); per round +0.58 (p=.41) and +0.87 (p=.14). Samples: pass@8
92.83 and 93.42, mixed questions 38.0% and 34.3%, pairs 658 and 586. A round costs about 1.2 GPU-h.

- The SQL mark for the CoT route is 75.05. The series was still rising when the rule stopped it, so it is a lower
  bound; more rounds are worth paying only if a CoT route comes within about two points.
- `cot1_e4 - sql1_e2` +1.84 (144/125, p=.27): after BIRD alone, the CoT student is level with the SQL student while
  trained on 1,266 rows against 9,428.
- The SQL route's lead comes from the Spider stage: SFT on all 8,659 gold rows. P2.62 `c1` has no such stage, so
  `c1` against `sql_rl2` mixes CoT with that stage; `s1` (the same rounds from `sql1_e2`) is the matched control
  and runs now on GPU 0.

## 2026-11-03: next CoT run is RL straight from `cot1` (P2.62 built)

An outside review of the paper comparison (COT_RL_RESEARCH section 14) corrected three readings, all accepted:

- Self-written CoT then SFT has a precedent: STaR-SQL (arXiv 2502.13550, checked) on Llama-3.1-8B-Instruct,
  3-shot, 8 samples per Spider question, gold SQL as a hint for failed questions, retraining from the base model
  each iteration: Spider dev 75.0 against SQL SFT 68.6, no best-of-N. The entry below ("none has a stage of SFT on
  the student's own outputs") and the claim that CoT wins only after RL are wrong. `cot2` lacked the hint, the
  restart and the iterations.
- Long reasoning is not shown to cause the 10-point gap: `tp2`, `cot2g` and `sql2` differ in parent and training
  rows. The same-parent pair `sqlc` 70.21 against `cot2g` 63.44 still differs in coverage (all rows against the 82%
  the student solved), and `cot2g` joins reasoning written toward the student's SQL with the gold SQL.
- 77.33% greedy copies and CE 0.11 suggest little new signal but do not prove it; the result that stands is that
  `cot2_e1` does not raise Spider dev EX.

Order decided (owner): (1) `cot1_e4` then DPO + NLL rounds on Spider, no `cot2`; (2) a short gold-blind teacher CoT
pilot on BIRD, then the same rounds; (3) a teacher DPO round on BIRD pairs, after counting them. P2.61 E2-E4 are not
queued. The P2.60 SQL lane continues: `sql2_e1` 73.60 is the SQL SFT mark, not the SQL ceiling after RL.

P2.62 (`scripts/run_p262_rl_from_bird.py`, nested `645e16d`, `cf408e1`) runs (1) as route `c1`, with the P2.60 round settings
and question sets (all Spider training rows whose gold returns a value, 1,200 new per round), and route `s1` from
`sql1` as the same route without CoT. `--phase pairs` counts the teacher rows for (3). Prior from P2.59 (SynSQL
roots, the same rounds): `g` 66.34 to 71.95 and `tp` 63.73 to 70.60 after three rounds, and `tp3 - tp_r3` +3.00
(p=.023), so RL straight from the public SFT ran below SFT then RL there.

## 2026-11-03: P2.61 at E1 (chat output, not committed)

Seed 0, Spider dev, from `cot1_e4`, E1 of a 4-epoch cosine like `cot2_e1` and `sql2_e1`.

| Point | EX | Execution error |
|---|---:|---:|
| `cot2_e1` own SQL | 60.35 | 14.12 |
| `cot2g_e1` gold SQL, same rows and reasoning | 63.44 | 13.93 |
| `sqlc_e1` SQL-only from `cot1_e4` | 70.21 | 11.51 |
| `sql2_e1` SQL-only from `sql1_e2` | 73.60 | 8.03 |

- Gold SQL helps a little: `cot2g - cot2` +3.09 (125/93, p=.036). The rest of the gap stays: `cot2g - sql2_e1` -10.15
  (57/162). So own SQL is a small part; the free-form reasoning is the large part at this point.
- Across arms the gap follows reasoning length: `tp2` (template, p50 63 tokens, gold SQL, all rows) 73.02 ties SQL,
  `cot2g` (p50 about 236) 63.44, `t2` (384) 62.48. `cot2g` covers 82% of the rows and `tp2` all, so length and coverage
  still move together.
- The CoT public stage is a weaker start for SQL: `sqlc - sql2_e1` -3.38 (46/81, p=.002), though `cot1_e4` is above
  `sql1_e2` on dev. `cot1` saw 1,266 rows against 9,428 and a different output format, so this does not isolate CoT.
- `sql2` stopped after `sql2_e2` 73.11, 0.49 below E1 (5 questions); its RL starts from `sql2_e1`. The SQL SFT ceiling
  may sit at E3-E4 after the learning rate falls, so 73.60 is a low mark for SQL.

## 2026-11-03: how close papers order SFT and RL

Read from the papers: all run one SFT on CoT written by a stronger source, then RL; none has a stage of SFT on the
student's own outputs. ExCoT: GPT-4o without gold on BIRD and Spider train, execution filter, then one off-policy and
two on-policy DPO rounds. SLM-SQL: SynSQL-Think-916K (with OmniSQL CoT for Spider and BIRD train), 2 epochs, then GRPO
on BIRD train, none on Spider. FINER-SQL: teacher corpus, SFT, then GRPO 2,000 steps. Think2SQL: 1,142 distilled rows,
then GRPO on BIRD train. Arctic-R1: GRPO from an OmniSQL checkpoint. OmniSQL has no RL. The teacher-only-on-public rule
blocks the Spider CoT of ExCoT and OmniSQL, so RL straight from `cot1` is the nearest route here: proposed after P2.61.

## 2026-11-03: P2.60 `cot2` targets checked, P2.61 controls built (chat output, not committed)

Owner suspected a training fault. Targets: no faults in `cot1` (1,266) or `cot2` (7,127), none dropped, tokens p95 444
and 404. A synthetic target round-trips through the real tokenizer. So nothing is cut.

The fault is the design: 5,511 of 7,127 `cot2` targets (77.33%) repeat the greedy output of `cot1_e4`, and the 1,532
rows it fails are dropped. Mean CE confirms it: `cot2_e1` 0.1147 on new data at 85% of peak lr, near `cot1_e4` 0.1009
at the end of its training and far from `cot1_e1` 0.2746. `sql2_e1` 0.1589, falling to 0.0507 at E2. The teacher rule
was gold-blind generation; carrying it to the student on Spider, where the client owns gold, was an agent choice.

Decision: stop the P2.60 CoT lane, keep its SQL route, run P2.61 (`cot2g`, `sqlc`) on one GPU.

## 2026-11-03: P2.60 CoT gap diagnosis (chat output, not committed)

Script `scripts/diagnose_p260_cot.py`, nested `aceca51`, Spider dev, points at the same learning-rate position.

- The Spider stage teaches `cot2` nothing on net: `cot2_e1 - cot1_e4` 101 wrong to right, 104 right to wrong, 70% of
  the SQL changed. SQL: `sql2_e1 - sql1_e2` 211 and 58 (+14.80, p<.001).
- `cot1_e4 - sql1_e2` +1.84 (144/125, p=.27): the public stage ties despite 13% of the rows.
- Dropped rows are not the main cause: 1,532 rows dropped, set operations 18.02% of dropped against 3.51% of kept, JOIN
  55.48% against 41.56%, but the gap is as wide on simple questions: no JOIN -11.82, no GROUP -11.49, not nested -12.93,
  no set operation -12.16. Set operations account for about 2.0 of the 13.25 points.
- Targets: own SQL textually gold 15.27%, same tables 81.55%, same clauses 75.94%; SQL is 11% of target chars at p50.
- Misses on the 192 questions only `sql2_e1` solves: execution error 69, same structure with wrong values 39, other
  tables 38, other clauses 30, fewer columns 11, more columns 5. Error gap 6.09 points, wrong-answer gap 7.16.

Reading: the student never sees gold SQL or a correction on Spider, and 89% of the target is reasoning. These two stay
confounded. Part of the error gap may close with the falling learning rate (`cot1` errors fell 17.79 to 12.48).
Proposed test, not queued: `cot2g` (same rows and reasoning, gold SQL) and `sqlc` (SQL-only gold from `cot1_e4`).

## 2026-11-03: P2.60 first Spider numbers, CoT gap under diagnosis (chat output, not committed)

| Epoch | `cot1` (1,266 rows) | `sql1` (9,428) | `cot2` (7,127, 82.31%) | `sql2` (8,659) |
|---|---:|---:|---:|---:|
| E1 | 54.64 | 49.13 | 60.35 | 73.60 |
| E2 | 55.90 | 58.80 | | |
| E3 | 59.57 | 58.22 | | |
| E4 | 60.64 | stopped | | |

- `sql1_e1` below base (59.19) is mainly the learning rate: E1 ends at 85% of peak, E2 at 50%. `sql1_e2` 58.80 is
  next to the old gold K2 (59.09) with the same data and lr, so the route is sound. The stop at E3 turned on -0.58.
- CoT is not behind on the public stage: `cot1_e4` is above `sql1_e2` with 13% of the rows, and it was still rising.
- The gap opens on Spider: SQL gains 14.80 from its public best, `cot2_e1` loses 0.29. Both are at the same lr point,
  so the lr does not explain it, though `cot2` has epochs left and `cot1` rose 6 points as the lr fell.
- Earlier arms: `tp2` 73.02 (gold SQL, all rows, target p50 63), `g2` 72.53 (29), `t2` 62.48 (76.48% of rows, 384),
  `cot2_e1` 60.35 (82.31%, own SQL, 236). Length, dropped rows and own SQL move together, so these do not separate them.
- `scripts/diagnose_p260_cot.py` measures the rows, the SQL and the misses. The status labels `cot_rl`, `sql_rl` name
  the best point of a route, here SFT points, not RL.

## 2026-11-02: P2.60 BIRD teacher pool done, `sql1_e1` (chat output, not committed)

Teacher 7B on BIRD with evidence, no gold SQL, greedy then K=2:

- Pilot: 277 of 300 rows checkable; solved 58.1% greedy, 68.2% after K=2. Pool: 927 greedy, 150 from K=2, 1,077 rows.
  Total 1,266 kept rows (Think2SQL distills 1,142).
- Selection is mild: gold p50 155 chars solved, 191 missed (SynSQL pilot 294, 876). Accepted SQL textually equal to
  gold 40 of 189 (SynSQL 6 of 88).
- Cost: 9.6-9.8 s/output, tokens p50 373, p95 548, peak 18.81 GiB; about 19 s per checkable row, so all of BIRD
  would be about 46 GPU-h and about 5,900 kept rows at this rate.
- `sql1_e1` (BIRD gold, first of at most 4 epochs under one cosine) Spider dev 49.13, execution error 17.21, wrong 33.66.

## 2026-11-02: P2.59 template route B published (nested `32a002b`)

Seed 0, Spider dev. Template CoT on SynSQL (`tp1`), then on Spider train (`tp2`, all 8,659 rows), then one DPO + NLL
round (`tp3`), against the same route on SQL.

| Point | EX | Execution error | Runs but wrong |
|---|---:|---:|---:|
| `g2` SQL SFT | 72.53 | 8.32 | 19.15 |
| `tp2` template SFT | 73.02 | 6.58 | 20.41 |
| `g3d` SQL + 1 RL round | 74.47 | 7.16 | 18.37 |
| `tp3` template + 1 RL round | 73.60 | 6.00 | 20.41 |

- `tp2-g2` +0.48 (74/69, p=.74); `tp3-g3d` -0.87 (64/73, p=.49). The format ties SQL on this route.
- `tp2-tp1` +9.28 (159/63): the CoT penalty after SynSQL closes once the student trains on Spider.
- RL gains less from the template: `tp3-tp2` +0.58 (26/20, p=.46), `g3d-g2` +1.93 (39/19, p=.012). Both rounds use
  about 300 questions with a pair (306 and 301), so pairs do not explain it.
- `tp3-tp_r3` +3.00 (103/72, p=.023): SFT on Spider then RL beats RL alone on this format. `tp_r3` 70.60, `g_r3` 71.95.
- The template trades 1.2-1.7 points of execution error for 1.3-2.0 points of wrong answers.

Owner, 2026-11-02: P2.60 uses BIRD, so `g3d` is not its mark; the template result shows the CoT direction can work.
Limit: the template restates the gold SQL, while P2.60 uses free-form CoT, whose P2.58 route reached `t3d` 65.09.

Reading: no sign yet of CoT above SQL, and no sign of a lower ceiling. `g3d` is one RL round, not a ceiling: the
SQL ceiling after many rounds is unmeasured, so `--stage sql` is needed for the claim even if P2.60 stays below 74.47.

## 2026-11-02: P2.60 pipeline on BIRD fixed (owner), SynSQL pilot published

Evidence: nested `814ecde` (SynSQL pilot; the 2026-11-01 entry's numbers are now committed). Reading accepted
outputs: most differ from gold only in style and answer correctly, a few pass with different logic (for example
`GROUP BY race_id` where gold groups by name), which is the weak SynSQL check.

Owner's pipeline: teacher CoT on a small BIRD set, as in Think2SQL; student SFT on the correct CoT; student writes
its own CoT on Spider train; SFT on its correct rows; RL over all Spider train; BIRD inside RL and more teacher
rows later. SFT stops at the first flat epoch, at most 4; RL adds rounds while it gains.

Choices made here: 2,000 BIRD rows, greedy then K=2, because sampling cost about four times more per kept row
than greedy on the SynSQL pilot and the aim is about 1,000 kept rows (Think2SQL 1,142). The stop reads Spider dev,
not Spider test, so test stays unused until the final choice (the owner raised test per epoch; 2,147 rows per
epoch cost more too). Epochs share one 4-epoch cosine, so a stop at E2 leaves the learning rate above its end
value. The second Spider pass (`csb`, `cot2b`) is gone: RL covers the hard rows. RL takes 1,200 new questions per
round for at most 7 rounds, the full train set, with the two-small-gains stop.

## 2026-11-01: P2.60 SynSQL pilot read, pool moves to BIRD (pilot numbers not committed yet)

Teacher 7B, no gold SQL, 300 SynSQL rows, greedy then up to 8 samples on unsolved rows (chat output, server):

- Only 142 of 300 rows have a gold result execution can check. On those, solved 40.1% greedy, 51.4%, 56.3%,
  59.9%, 62.0% after 8 samples. Extrapolated: about 1,000 usable rows of 3,336 for about 27 more GPU-h.
- Selection: gold SQL p50 294 chars on solved rows, 876 on missed. Accepted SQL textually equal to gold 6 of 88.
- Cost: 13-14.7 s/output (484 tokens p50, 747 p95), 67 s per checkable row, peak 17.46 GiB; twice the
  7 s/output measured at 384 new tokens in P2.59, so the earlier estimates were low.

Decision (owner proposed the move, 2026-11-01; the pilot numbers point the same way): BIRD replaces SynSQL as the P2.60 pool. Think2SQL
(arXiv 2504.15077) shows BIRD training lifting Spider against the untrained base (3B .725 to .770 with SFT,
7B .776 to .826 with SFT + RL), which does not isolate CoT from SQL-only on Spider. The reasons to move are
BIRD having no shipped CoT and real rows for the execution check. All 9,428 rows are out of budget (greedy
alone about 36 GPU-h), so `POOL_ROWS` takes a subset set from the BIRD pilot; Think2SQL distills 1,142 rows.
SynSQL marks `g3d`, `g2` stay rough marks only; a claim needs the matched `--stage sql`.

## 2026-11-01: P2.59 teacher-target design reviewed against distillation papers

Owner questions whether asking the teacher to fill a gold-derived format
can test its reasoning contribution. Read-only code review at nested
`a6d3204`; primary-paper research. No GPU run, code change or queue change.
Full assessment: [COT_RL_RESEARCH](../archive/directions_2026-11/COT_RL_RESEARCH_2026-11-03.md), section 12.

Confirmed implementation: `template_steps` renders gold SQL clauses through
sqlglot; teacher sees question, schema and gold SQL, writes similar labelled
lines. `writer_reasoning` accepts EOS, no reference mention and gold-table
names without requiring the writer's own SQL EX. Training then replaces
the writer's SQL with gold. A 384-token response limit and common-writer
intersection also remove usable reasoning and reduce coverage.

This tests one noisy rationalization recipe against an exact gold-derived
representation. It is not a general test of teacher reasoning distillation.
Template remains a valid strong comparator, not a theoretical ceiling.
Gold-conditioned reasoning itself is supported by OmniSQL, VCoT-SQL and
CodePLAN; the material gap is preserving and validating the rationale's
connection to the generated solution, not merely hiding gold.

Recommendation, not an owner decision: teacher-generated solving traces
verified against gold, with CROP/STaR-style rationalization backup and
PERsD/SCD-style feedback on the student's public errors. Keep the full
public pool and the owner's gold-SQL training targets; failed rationales
retain SQL-only supervision. Before substituting gold SQL into a target,
require a rationale compatible with it. Use stand-alone reasoning for
question-to-SQL; diagnosis of a prior error needs a separate repair input.
Teacher never processes private data. RL follows the corrected bootstrap.

P2.57 is published (`f8f3832`). A checked example in `t1_solve.jsonl`,
`data:1017027`, has EX=1 on a nonempty-gold case while omitting the gold's
Liquidity category filter. This supports checking semantic decisions as
well as execution on SynSQL's small databases. P2.59 server metrics remain
unpublished and were not recounted here. The narrowed-lane commands still
say owner confirmation is pending; this review does not stop a lane.

## 2026-11-01: teacher-CoT research recommendation

Owner asked which CoT + RL method is worth trying while retaining a real
server-teacher contribution. Research only; no GPU run or command queued.
Details and primary sources: [COT_RL_RESEARCH](../archive/directions_2026-11/COT_RL_RESEARCH_2026-11-03.md), section 10.

Recommendation: clause-grounded teacher CoT with SQL/schema checks, then
execution-based Iterative DPO + NLL. VCoT-SQL (EMNLP 2026) supports 7B target
synthesis; RetrySQL and SLM-SQL support reasoning at student size 1.5B.
Their full recipes do not match our LoRA, public/private split or budget.
GRPO is the first policy-gradient alternative, pending an A5000 smoke.

The proposed pilot compares Gold, Self-CoT and Teacher-CoT on the same public
pool, then through private training and aggregation. Private examples with
rejected rationales retain gold SQL supervision. P2.58 trained `t2` on only
6,622/8,659 private rows while `g2` used all rows; target quality, LR and
coverage remain confounded. Current recommendations prioritize teacher-CoT
over the SQL-only-first sequence in the entry below; this is not an owner
direction decision.

Corrections to the preceding literature assessment:

- Published SLM-SQL Figure 1 does contain SFT 54.26 for Coder-1.5B. The
  conflicting Table 6 does not justify saying the number is absent.
- P2.58 median training targets CoT/SQL are 566/123 on SynSQL and 384/29 on
  Spider. SQL 23 tokens refers to evaluation outputs, not matched targets.
- VCoT-SQL section 3.1 uses final SQL EX and heuristic schema matching; it
  does not execute each reasoning step. Teacher synthesis uses 7B models,
  but its students are also 7B, not 1.5B.
- Shorter CoT and more epochs remain hypotheses on our SQL task. Results
  from math do not identify the cause of P2.58's deficit. Similar EX for
  teacher and template would not establish an exactly zero teacher effect.
- The numerical success probabilities in the 2026-10-31 entry were
  subjective judgments, not calibrated estimates; they are not used to
  rank the present recommendation.

## 2026-11-01: P2.59 RL round 2 (not committed)

Spider dev, seed 0. `g_r1` 68.76, `g_r2` 70.99 (+2.23, 709 pairs): SQL RL-only is not flattening.
`tp_r1` 68.09, `tp_r2` 67.12 (-0.97, 702 pairs): the template's gap to SQL goes -2.61, -0.67, -3.87
(unpaired), so the narrowing at round 1 did not continue. Template output tokens p50 go 82, 60, 76,
so they are not shrinking steadily. Writer speed: `tc` about 7.1 s per output at p50 about 240 tokens.

## 2026-11-01: P2.59 published (nested `9456e09`, 63 of 119 tasks)

Spider dev, seed 0, greedy. Replaces the "not committed" P2.59 numbers below; every value matches. The
`tc` and `sf` tasks after round 1 and route B were not run (owner, narrowed).

| Point | EX | Execution error | Runs but wrong | Tokens p50 | RL pairs |
|---|---:|---:|---:|---:|---:|
| `g1` / `g_r1` / `g_r2` / `g_r3` | 66.34 / 68.76 / 70.99 / 71.95 | - / 9.09 / 7.35 / 7.93 | - / 22.15 / 21.66 / 20.12 | 26 | 867 / 709 / 566 |
| `tp1` / `tp_r1` / `tp_r2` / `tp_r3` | 63.73 / 68.09 / 67.12 / 70.60 | 9.96 / 9.09 / 7.74 / 6.48 | 26.31 / 22.82 / 25.15 / 22.92 | 82 / 60 / 76 / 75 | 896 / 702 / 613 |
| `tc1` / `tc_r1` | 59.28 / 62.48 | 17.70 / 15.18 | 23.02 / 22.34 | 123 / 126 | 1,114 |
| `sf1` / `sf_r1` | 52.32 / 58.80 | 19.05 / 18.57 | 28.63 / 22.63 | 207 / 209 | 1,260 |

- `tp_r3` - `g_r3` -1.35 (71/85, p=.30), union 78.82; `tp` trained on 2,132 shorter SynSQL rows, `g` on
  3,336. `tp_r3` - `tp1` +6.87 (104/33), `g_r3` - `g1` +5.61 (88/30). The gap goes -2.61, -0.67, -3.87,
  -1.35, so it does not narrow steadily. Template outputs keep 3 reasoning lines.
- `g_r3` - `g3d` -2.51 (69/95, p=.051): on SQL, SFT then one RL round ends above three RL rounds alone.
- `g3d` - `g3n` +2.22 (41/18, p=.004): the DPO gain comes from the preference term.
- `tc1` - `tp1` -4.45 (83/129, p=.002), `tc_r1` - `g_r1` -6.29 (69/134). `t1lr` - `t1` -1.45 (p=.32).
- pass@8 on new Spider questions: `tc_r1` samples 80.33-83.33, `sf_r1` 78.33-83.67, `tp_r1` 79.33-80.67,
  `g_r1` 83.08, `g_r3` 84.75. So a student straight from SynSQL solves about 82% at K=8; P2.60 `cs` at K=4
  will likely fall below the 90% line, and `csb` will likely run.
- Recommended next read: `tp2`, `tp3` against `g2`, `g3d` on the same route, about 4 GPU-h, no new code.

## 2026-11-01: where training saturated before, and the P2.60 order

Owner asks whether saturation should be checked, since earlier runs peaked early. Earlier evidence:
FL Coder-1.5B peaks at A2 (A3 - A2 -0.68, p=.47) and 0.5B central peaked at E2; Coder-1.5B central keeps
rising through its last epoch on Spider (`central_mix` 68.28, 71.66, 73.21; `central_k2` still rising
at E3), though with a 3-epoch cosine that schedule decays to its end. No run went past 3 epochs, so
the peak beyond is unknown. Decision: dev per epoch, which P2.60 already does; no Spider test between
epochs, since test is for the final point. The SQL route runs first (`--stage sql`), so saturation and
the mark are known before the teacher pool is paid for. A chosen epoch is rerun on the same 6-epoch
schedule, because a shorter cosine reaches a different point.

Revised the same day (owner): earlier runs already give the SQL marks, so SQL is not rerun for now. `g3d`
74.47 is the mark for the CoT route; a real SQL ceiling is measured only if CoT passes it, since only that
claim needs it. SFT stages go to 4 epochs, one past what earlier central runs reached. A CoT peak at
epoch 4 would need a longer schedule. A chosen epoch is rerun on the same schedule.

## 2026-11-01: P2.59 `g_r3` (not committed)

Spider dev, seed 0: `g1` 66.34, `g_r1` 68.76, `g_r2` 70.99, `g_r3` 71.95 (gains +2.42, +2.23, +0.96).
Three RL rounds on 3,600 questions end near `g2` 72.53 (2-epoch SFT on 8,659) and below `g3d` 74.47
(unpaired), so on SQL, SFT then RL ends higher than RL alone so far.

## 2026-11-01: P2.60 built (nested, pilot ready)

Choices made at build time: rows never solved are excluded with coverage reported; rows whose gold is
empty or all NULL are left out of the teacher's rows, since execution checks nothing on them; SFT stages
run their maximum and evaluate every epoch, so the stop rule acts only on RL rounds; the SQL route's own
6-epoch curve replaces treating `g1` and `g2` as its first points, because their cosine horizon differs.
SynSQL databases hold about two rows per table, so an accepted SQL can match gold by chance; the pilot
reports textual equality and `--phase preview` prints accepted outputs to read. `POOL_SAMPLES` stays
unset until the pilot. The P2.59 publication allowlist is widened for the new nested files.

## 2026-11-01: P2.59 failure split after RL (not committed)

Template outputs keep their reasoning under RL: has reasoning 100%, lines p50 4, 3, 3 (`tp1`, `tp_r1`,
`tp_r2`). Split of Spider dev failures, execution error / runs but wrong (100 - EX - error, unpaired):
`g_r1` 9.1/22.1, `tc_r1` 15.2/22.3, `tp_r1` 9.1/22.8, `sf_r1` 18.6/22.6; `g_r2` 7.4/21.6, `tp_r2`
7.7/25.2. After one RL round the `tc` gap to SQL is almost all execution errors; the wrong-answer
share is level. The `tp` gap at round 2 is wrong answers, with errors level. `sf_r1` no-SQL rows may
sit in its error share. For P2.60, read errors and wrong answers separately at every checkpoint.

## 2026-11-01: P2.60 compares ceilings (owner)

Owner: separating the teacher's contribution is out of scope, because the teacher is what supplies
the CoT. The question is whether CoT + RL beats SQL-only SFT, comparing ceilings and not equal steps.
A ceiling needs both routes trained to a plateau, so the SQL route gets its own curve: `g1` and `g2`
stop at 2 epochs and are not its ceiling. This replaces the fixed one or two Spider rounds below.

## 2026-11-01: P2.60 reduced to the teacher CoT route (owner)

Owner: for now only teacher CoT, and the teacher never sees gold SQL: keep rows it solves correctly,
with sampling on wrong rows to raise that share. Then SFT on that pool, Spider SFT, RL. Since the
teacher cannot run on Spider, Spider CoT comes from the student's own gold-blind samples. P2.58 `g1`,
`g2`, `g3d` serve as references. Without a Template arm, a win over SQL shows CoT helps but does not
isolate what the 7B adds beyond a format. Spider SFT: one round, a second only on failed rows if
coverage stays below about 90%, because `g3n` shows more NLL on chosen outputs adds nothing on SQL.

## 2026-11-01: ceiling run proposal reviewed against the literature

Another agent proposed: teacher solves without gold, bounded sampling on failures, rationalization
with gold for what remains, keep the writer's own SQL, no SQL-only fallback in CoT-SFT, compare on
accepted rows with Gold full pool as baseline. Sources checked:

- Lee et al. (arXiv 2607.14552, preprint): one-bit experiment on Qwen3-8B. Chains written with the
  gold answer and a request to reach it cost 16.2 points on MATH-500, three seeds, and also degrade
  code; correctness filters cannot see it. The harm tracks the rationalize-toward instruction: with
  neutral instructions the answer stays visible and the cost is about 1 point. Not tested on SQL.
- Rossiello et al. (arXiv 2502.06759, ICLR workshop): BIRD dev, 8B student. Gold-SQL rationalizer
  coverage 99.02% gives CoT long 67.41 vs Gold 66.17; coverage 73.86% gives 61.99 vs 63.95.
- Correction after checking the original CROP paper (Li et al., arXiv 2210.06726, section 3): it
  explicitly uses rationalization prompting with gold as backup when blind generation fails.
  The earlier survey-based reading that CROP supports only blind filtering was incomplete.

The CoT-SFT targets so far saw the SQL: OmniSQL `t1`, `t2`, P2.59 `tc`, `sf`. A teacher-blind SFT
arm has not been trained; student DPO rollouts are already blind. Gold-conditioning remains an
untested explanation of the SFT gap. Recommendation: generate blind
first and read coverage before training; add rationalization only if coverage is too low, and as a
separate arm with a neutral instruction. Spider stage for CoT arms: blind sampling with execution
filter, not rationalization. Not decided: the owner picks fallback or exclusion in CoT-SFT.

Follow-up source review, same day: Lee Table 11 also tests answer-hint rescues only on blind
failures: Qwen3-8B blind-only 95.2 vs STaR-rescue 91.2 on MATH-500. This is a direct reason to
keep rationalization separate rather than the default backup proposed earlier. Lee and Rossiello
do not test opposite answers to the same contrast: Lee compares CoT sources; Rossiello compares
CoT with SQL-only. Both results can hold. Design details in COT_RL_RESEARCH section 13.
No code, queue or GPU changes. If final SQL stays teacher-generated, matched SQL-only and template
controls must use that same SQL to isolate rationale value; original-gold/full remains the
whole-recipe baseline. Adding rationalized rows only on failures also changes training coverage,
so its benefit is a rescue-policy contrast, not an isolated test of answer visibility.

## 2026-11-01: P2.59 narrowed (owner confirmed and started it)

The rest of the queue spends most of its GPU time on `tc` and `sf`, whose prompt and row filter
the ceiling run replaces. Keep only `g_r2-3` and `tp_r2-3`: they give the shape of the RL curve
and whether template outputs keep their reasoning lines. What P2.59 shows so far: DPO beats NLL on
the same chosen rows, seed 0 Spider dev (+2.22); it does not settle CoT or the teacher.

## 2026-11-01: owner question for the CoT and RL phase

Owner: the experiments must show whether CoT and RL beat SQL-only SFT and how to combine them.
CoT alone may fall short yet reach a higher ceiling with enough training or enough RL. The
teacher's role is to write CoT on a public dataset that has none.

P2.59 reads RL to three rounds at fixed 2-epoch SFT, so it does not test more SFT epochs or RL
until a plateau. The proposed follow-up is a ceiling run: SQL, teacher CoT and template on the same
rows, an SFT curve, then RL rounds until the gain stops, three seeds on the final claim.

Owner, same day: every arm trains the full pool, not a filtered subset, and the teacher's role is
tested on a public dataset with no CoT (SynSQL ships one). For the ceiling run: a target always
ends in the complete gold SQL; a row whose reasoning fails is retried with a larger token budget,
and if it still fails it trains on gold SQL with the SQL-only prompt.

Owner, same day: SynSQL stays the main pool for now; other datasets may follow. The owner also
points out that a teacher shown the gold SQL and told to fill fixed lines is close to the template.
Checked in the papers: ExCoT gives GPT-4o no gold SQL, samples up to 32 candidates and keeps those
that match on execution; OmniSQL shows the SQL, samples 8 at T=0.8 with no fixed format and picks
by execution majority; VCoT-SQL shows the gold SQL and uses a clause template with few-shot; SCoTD
samples 30 rationales per question; in Li et al. asking a large teacher to be concise did not close
the gap to a small one. P2.59 `tc` shows the gold SQL, fixes the lines and takes one output, so it
tests only that form. Proposed teacher arm for the ceiling run: solve without gold, greedy first,
sampling only on failed rows, keep execution-correct outputs; other rows train on gold SQL.

## 2026-11-01: P2.59 writer diagnosis (not committed, 3,336 SynSQL rows)

Rows: the `eos` filter keeps 2,132 common rows; accepting complete reasoning before a cut SQL
would keep 2,799 (84%). Median gold SQL length: kept 343 characters, dropped 707, all 431, so CoT
roots train on shorter queries than `g1` and contrasts with `g1` are biased against CoT.

Writers on the kept rows, gold columns and literals named: `tc` 77.2/75.2, `sf` 77.4/72.6, `tp`
100/100 (substring match; it measures naming, not the logic of the reasoning). Labelled format:
`sf` 77.4% of rows, `tc` 100%. Own SQL when present matches gold 89.0% (`tc`), 87.7% (`sf`); `sf`
wrote no SQL on 2,594 rows, which explains its 19.5% overall.

Evaluation, no SQL / execution error: `tc1` 0.0/17.7, `sf1` 2.4/19.1, `tp1` 0.0/10.0, `tc_r1`
0.0/15.2, `sf_r1` 1.1/18.6, `tp_r1` 0.1/9.1. Output tokens p50: `tp1` 82, `tp_r1` 60. Missing or
cut SQL does not explain `tc1` below `tp1`, and explains at most 2.4 points of `sf1` below `tc1`.

Decision: lanes keep running; the filter is not refit, because it would not change `tc` against
`tp` and would retrain the tree. `g1m` (SQL on the 2,132 rows) with one RL round is the proposed
clean control, to run when the lanes are idle (owner decides).

## 2026-11-01: P2.59 writer preview (not committed, four rows per writer)

Read from `--phase preview` on shard 0. Base-student outputs often stop after the reasoning
with no SQL block, so the 19.5% own-SQL figure does not measure its reasoning; its training
targets still end in the gold SQL. A teacher row whose reasoning finished and whose SQL hit the
384-token cap was dropped, although the writer's SQL is replaced by gold, so the `eos` filter
removes usable rows. Teacher reasoning in the sample often omits join keys and conditions (one
HAVING missing); the template states them exactly. Four rows do not measure this:
`scripts/diagnose_p259_writers.py` (read-only) measures all of it over the full pool.

## 2026-11-01: P2.59 first signals (not committed, 39/119 tasks)

Reported from the server status; lanes running. Seed 0, Spider dev.

| Route | SFT on SynSQL | After RL round 1 | Gain | Pairs | Gap to SQL, SFT then r1 |
|---|---:|---:|---:|---:|---|
| SQL (`g1`, `g_r1`, 3,336 rows) | 66.34 | 68.76 | +2.42 | 867 | |
| Template (`tp`, 2,132 rows) | 63.73 | 68.09 | +4.36 | 896 | -2.61, -0.67 |
| Teacher (`tc`, 2,132 rows) | 59.28 | 62.48 | +3.20 | 1,114 | -7.06, -6.28 |
| Base student (`sf`, 2,132 rows) | 52.32 | 58.80 | +6.48 | 1,260 | -14.02, -9.96 |

- `tc1` - `tp1` -4.45 (83/129, p=.002): the teacher's reasoning is below a template that only
  restates the SQL, on the same rows. `tc1` - `sf1` +6.96 (171/99, p<.001), but the base student's
  own SQL matches gold on only 19.5% of rows here (75.33 with the long P2.57 prompt), so `sf` may
  be a weak control. Teacher own SQL 78 (91.33 in P2.57).
- Rows: the writer filters keep 2,132 of 3,336 rows (64%; truncation at 384 tokens 12-14% teacher,
  19-20% student). `g1` trained on all 3,336, so every contrast with `g1` or `g_r1` mixes format
  with 36% fewer, probably simpler, rows. The contrasts among `tc`, `sf`, `tp` are matched.
- `t1lr` - `t1` -1.45 (p=.32): lr does not explain the long-CoT gap. `tc1` - `t1` +1.06 (p=.49,
  fewer rows): the teacher's shorter target gains little by itself. Target p50: 237 `tc`, 191 `tp`.
- `g3d` - `g3n` +2.22 (41/18, p=.004) and `g3n` 72.24 against `g2` 72.53: the DPO gain comes from
  the preference term, not from NLL.
- RL narrows the gap on every CoT route, more from a lower start. One round; the endpoints
  `tc3`, `tp3` against `g3d` and `*_r3` against `g_r3` are not in.

## 2026-11-01: P2.59 teacher CoT then RL queued (owner)

Owner: teacher CoT in the first phase teaches the student to reason; in the second
phase the student improves that reasoning by RL. CoT may lose after SFT and still win
after RL, as in ExCoT and Schema-R1, so arms are read after RL, not after SFT. This
drops the SFT stop proposed on 2026-10-31. Nested code: `scripts/run_p259_cot_then_rl.py`.

Design, seed 0, Spider dev, greedy, Spider test not touched:

| Stage | Arms | Source |
|---|---|---|
| 1, SFT on SynSQL, same rows, final SQL always gold | `tc1` teacher, `sf1` base student, `tp1` template; `t1lr` long CoT at lr 5e-5; references P2.58 `g1`, `t1` | short CoT Li et al. 2502.12143, Chen et al. 2502.18001; execution-order steps RetrySQL; cleaning SLM-SQL; hidden reference STaR |
| 2a, RL only, 3 rounds, new 1,200 questions each | `tc_r*`, `sf_r*`, `tp_r*`, SQL `g_r*` from `g1` | on-policy DPO with NLL: Iterative RPO, ExCoT |
| 2b, SFT on Spider, then 1 RL round | `tc2`, `sf2` self-written, `tp2` template, then `*3`; references `g2`, `g3d` | STaR, ExCoT |
| Control | `g3n`, the NLL term of `g3d` alone | Iterative RPO |

Writer filter, from VCoT-SQL section 3.1: finished, no mention of the reference, names the
gold tables. Its execution filter on the writer's own SQL is not applied: the base student
would lose about a quarter of the rows (75.33 on SynSQL), and the final SQL is gold in every
arm. Rows with a rejected rationale at stage 2b keep their gold SQL with the SQL-only prompt,
so coverage matches `g2` (COT_RL_RESEARCH section 10.3; P2.58 lost 2,037 rows).

Differences from COT_RL_RESEARCH section 10.4: `tp1` stays as an arm, since teacher against
template is what a reviewer will ask and it needs no generation; SFT stays at lr 2e-4 so the
SQL reference `g1` is matched, with `t1lr` as the lr contrast; this run is centralized, and
the Teacher minus Self contrast after FL follows only if the arms separate here.

Without a source: labelled-line format, its one worked example, replacing the writer's
SQL with gold, 1,200 questions per round, K=8, and three rounds on new questions. GRPO
is not in this run: it needs a new trainer and online generation, and Xiong et al.
(2504.11343) rank Iterative DPO lowest on math, so it is the next RL to test if the
interaction appears but stays weak.

Reading: `tc_r3` and `tc3` against the SQL endpoints `g_r3` and `g3d` answer whether CoT
then RL beats RL alone; against `sf_*` and `tp_*` they answer whether the teacher adds
anything. Judgment, not measured: a short-CoT endpoint above its SQL comparator, about
30%; the teacher arm at least 2 points above both controls at the endpoint, about 15%.
Teacher writer quality is checked with `--phase preview` before the result is read.

## 2026-10-31: outside CoT + RL proposal checked against the papers

Recommendation, not an owner decision; no run queued. Local recount from the
committed P2.58 predictions (seed 0, Spider dev; script not committed).

Outside proposal: iterative DPO + NLL next, GRPO as the direct RL option, short
SQL-operation CoT, NLL-only control. The DPO order and the control hold. The
CoT case is weaker than it states:

- SLM-SQL (arXiv 2507.22478): 61.95 and 67.08 are right; 54.26 is in neither
  results table (Table 6 SFT 54.17, and its SFT + RL 50.59 looks like a typo).
  Spider, 16 samples, RL on BIRD only: SFT 74.53, SFT + RL 75.15 on dev, 77.35
  and 78.42 on test; with CSC 76.66, 76.72 and 79.13, 79.06. The large RL gain
  is on BIRD.
- RetrySQL (arXiv 2507.02529): numbers right. For Qwen2.5-Coder 1.5B no SQL-only
  row exists; BIRD gains nothing from retry (55.96, 55.65, 56.36); Spider 77.18
  at corruption 0.2, 75.11 at 0.3. GPT-4o writes steps from gold on the training
  rows, which our private-data rule excludes. Gold schema links, 5 runs.
- FINER-SQL (arXiv 2605.03465): 59.4 to 63.1 right (BIRD dev). 1.5B Spider 80.0
  uses schema filtering and 30-candidate voting; at 0.5B greedy is about 35,
  voting about 49. Removing both dense rewards costs 2.16 at 1.5B. No teacher
  ablation.
- Li et al. (arXiv 2502.12143): 27.0 and 34.2 right. Omitted: at 1.5B a larger
  teacher does not help (32.2 vs 33.0). Long CoT stays flat from 2 to 5 epochs
  (.270 to .286; short .341), so the extra-epoch probe proposed in the entry
  below has low value. LR matters (1e-4 .133, 1e-5 .276, full fine-tuning).
- ExCoT (arXiv 2503.19988): CoT SFT is below SQL SFT there too (Spider 81.42 vs
  83.00), and only 3 DPO rounds with 32 candidates on 70B flip it (86.59). The
  first off-policy round on GPT-4o candidates matters (BIRD 68.51 vs 66.30 and
  67.08 on-policy only). No-CoT DPO is 81.00 on Spider, +2.19 over the base
  model 78.81 and below SQL SFT 83.00; its starting checkpoint is not stated,
  so it does not compare with `g3d` +1.93 over its own SFT (corrected
  2026-10-31; this entry first called the two close). CoT gap at SFT: ExCoT
  -1.58, P2.58 -10.06.
- GRPO: main advantage is dropping all-wrong prompts, RAFT competitive (Xiong et
  al., arXiv 2504.11343). The P2.58 RFT result is confounded: lr 2e-4 vs DPO 1e-5.
- Not in the proposal: plain federated DPO loses accuracy as clients grow
  (FedPDPO, arXiv 2603.19741, DistilGPT2 on IMDB, 3 to 10 clients 82.73 to
  76.45); FedMOA (arXiv 2602.00453) and FedDPO in OpenFedLLM (arXiv 2402.06954)
  are the closest federated work to cite.

P2.58 slices, `t3d` - `g3d`: JOIN -13.5, no JOIN -6.7, GROUP BY -13.7, nested
-8.2. Of the 157 questions only `g3d` solves, `t3d` runs a wrong query on 98 and
names a missing column or table on 55, so the gap is mostly logic, not only
schema linking. Union of both 80.27, `t3d` alone solves 60. Text after the final
SQL is 13.6% of a `t3d` output at p50, so cleaning it does not make CoT short.

P2.57 is not published: no `p257` audit files in nested `origin/main`.

Cached teacher negatives: `raw/train.csv` holds teacher SQL for all 9,428 BIRD
rows, 5,319 match gold, 4,109 do not (3,727 where the gold passes the audit).
These give gold versus teacher-wrong pairs with no teacher run, the closest
available match to the ExCoT off-policy round. Teacher SQL on Spider stays out.

Recommended order, costs from P2.58 receipts:

1. Spider test on `g2`, `g3d`, `t2`, `t3d` (about 2.4 h): does the gain hold?
2. `g3n`: NLL only on the `g3d` chosen rows, same lr and updates (about 0.5 h).
3. SQL-only iterative DPO, 3 rounds on the 7,000 question pool, plus seed 1 of
   `g1`, `g2`, `g3d` (about 15 GPU-h).
4. One CoT rescue on the other GPU: base student CoT on Spider dev (0.5 h), then
   teacher short CoT on SynSQL and SFT against `g1` and `t1` (about 7 h,
   estimate). Earlier structured CoT also lost (P2.10, old student, template
   plans). CoT stays only if the gap is near the ExCoT size.
5. Federated: one client DPO round from existing A3 adapters of FedAvg,
   `gold_k2aaa`, `hinton_k2aaa` (about 18 GPU-h): survival under non-IID and the
   teacher contrast.
6. Teacher as negatives: server DPO on cached teacher pairs against student
   pairs on the same rows, then the private rounds (about 10 GPU-h).

Judgment, not measured: DPO gain holds on test and seed 1, about 55%; CoT beats
SQL-only greedy at 1.5B on this data, 10-15%; federated DPO beats FedAvg, about
60%; a teacher edge above one point on Spider test through this path, about
20%. The likeliest outcome is a strong federated execution-RL result with a small
teacher share, which the current paper goal does not accept on its own.

## 2026-10-31: P2.58 published, CoT training diagnosis

Evidence: nested `6dd0cb0`,
`audits/protocol_v2/p258_cot_rl_screen_s0/{summary.json,done/,eval/}`.
Local recount from the committed predictions reproduces all eight EX values
and all eight paired contrasts below, including exact McNemar p-values.
No GPU training or generation was rerun for this review.

The screen supports execution-preference training as a candidate, but does
not yet support CoT as the useful component: DPO + NLL adds 1.93 points to
SQL-only and 2.61 to CoT; the CoT endpoint still trails by 9.38 points.
The 0.68-point difference between those gains is descriptive, not evidence
of a CoT-specific DPO advantage. The two arms also have different preference
data (433 versus 1,057 pairs). RFT lowers both endpoints in this screen.
These are centralized, seed-0 results, without our server teacher; they do
not establish a federated or teacher contribution. One batch of sampled
preferences followed by DPO is not a test of iterative online GRPO.

Does CoT need more training? That remains open, rather than the established
cause of the gap:

- T1 and T2 each train for two epochs, lr 2e-4, LoRA r16. T1 has 417
  optimizer updates on 3,336 SynSQL rows, T2 828 on 6,622 Spider rows.
  Final reported CE is 0.3512 and 0.0691 respectively. These are training
  summaries, not an epoch-wise validation curve or a SQL-only loss.
- T2 finds SQL in all 1,034 dev outputs and none is truncated; output
  length p50/p95 is 395/585 tokens. The failure is not inability to finish
  the requested format. Prediction records contain 124 execution errors
  versus G2's 86; missing-column/table errors are 119 versus 79.
- Sampled train pass@1 is 66.90 for T2 versus 88.21 for G2, but this uses
  temperature 0.7 on 1,200 non-empty-gold questions. It is neither greedy
  train EX nor performance restricted to the rows admitted to T2 training:
  284 of those 1,200 questions are outside T2's admitted SFT rows.
  Its proximity to dev greedy EX does not diagnose underfitting.
- Stage 2 changes coverage as well as target/prompt: 6,622 rows for T2
  versus 8,659 for G2. The gap already exists on identical stage-1 rows,
  but the contribution of those 2,037 omitted rows at stage 2 is unmeasured.
- Self-rationalizations are checked by final-SQL execution, not by the
  correctness of the reasoning. The SynSQL targets also contain 259
  reference mentions; T2 still mentions a reference on 41 dev questions.
  These are target-quality concerns, not proof of the cause of the gap.

Recommendation, not a queued run or an owner decision: test additional SFT
from T2 on the same targets and settings, saving each epoch, and evaluate
greedy solve-mode EX on a fixed subset of admitted training questions and
Spider dev before and after. Report reasoning and final-SQL CE separately.
An additional two epochs took about 2.6 h for the original T2 stage; allow
extra time for evaluations. A restart from adapter weights is a new SFT
stage with a new optimizer/schedule, not a continuous four-epoch run.
If training EX improves without dev EX, more repetition is not improving
generalization; if both improve, extra optimization benefits this recipe.
This probe tests extra optimization on existing targets, not the value of
more distinct CoT examples. Do not launch a full federated chain on this
screen alone.

Literature checked for this interpretation:
[OmniSQL](https://arxiv.org/html/2503.02240v2) also uses two epochs, but with
7B+ students and different adaptation/data. Its CoT-enhanced Spider+BIRD
ablation improves even without the 2.5M synthetic pool, so the current
failure cannot simply be attributed to not using millions of rows.
[ExCoT](https://aclanthology.org/2025.findings-acl.982/) demonstrates gains
through execution-based preference optimization, but on 32B/70B models
and multiple DPO rounds, not this 1.5B LoRA screen.
[Li et al., Findings ACL 2025](https://aclanthology.org/2025.findings-acl.1301/)
find that smaller models can benefit more from simpler reasoning; this
motivates adapting targets, not declaring 1.5B incapable of CoT.

## 2026-10-30: P2.58 screen results (published 2026-10-31)

Initially reported from server receipts; now committed in nested `6dd0cb0`.
`eval_g1`, `eval_t1` and
`eval_g2` were run by hand ahead of the lane order, which puts every
evaluation after the RL tasks; the order does not change any result.

| Adapter | Target | Data | Spider dev EX | Tokens p50/p95 |
|---|---|---|---:|---|
| `g1` | SQL | SynSQL 3,336 | 66.34 | 28/72 |
| `t1` | CoT | SynSQL 3,336 | 58.22 | 390/563 |
| `g2` | SQL | `g1`, then Spider 8,659 | 72.53 | 23/70 |
| `t2` | CoT | `t1`, then Spider rationalizations 6,622 | 62.48 | 395/585 |
| `g3d` | SQL | `g2`, then DPO + NLL, 433 pairs | 74.47 | 23/69 |
| `g3r` | SQL | `g2`, then RFT, 1,624 examples | 71.66 | 21/64 |
| `t3d` | CoT | `t2`, then DPO + NLL, 1,057 pairs | 65.09 | 400/599 |
| `t3r` | CoT | `t2`, then RFT, 1,887 examples | 61.70 | 415/583 |

- DPO helps both formats by about the same amount: `g3d` - `g2` +1.93 (39/19,
  p=.012), `t3d` - `t2` +2.61 (91/64, p=.036). RFT does not: `g3r` - `g2` -0.87
  (52/61, p=.45), `t3r` - `t2` -0.77 (100/108, p=.63).
- RL does not close the CoT gap: `t3d` - `g3d` -9.38 (60/157, p<.001), `t3r` -
  `g3r` -9.96 (71/174, p<.001).
- RL samples, K=8 at T=0.7 on 1,200 training questions: `g2` pass@1 88.21,
  pass@8 97.17, mixed 25.08; `t2` pass@1 66.90, pass@8 88.58, mixed 54.67.
  These sampled train scores and greedy dev EX do not measure the same
  decoding setting, and the T2 sampling pool includes rows excluded from
  its SFT data; their difference does not establish underfitting.
- Spider test was not touched. No teacher ran in this screen.

- `t2` - `g2` -10.06 (65/169, p<.001). The gap was already -8.12 before
  Spider on the same rows. Missing stage-2 rows cannot explain the stage-1
  gap; their contribution to the final gap has not been isolated.
- Owner stopped both lanes on 2026-10-31 during `t2_samp0` and `t2_samp1`; their
  finished rows are kept.
- Owner, 2026-10-31: the 2026-10-28 paper direction is not convincing enough; a
  new direction is being sought, and CoT + RL is the current candidate. P2.58 ran
  to the end after this; P2.53 seed 2 stays on hold.

- `t1` - `g1` -8.12 (80/164, p<.001). `t1` is below the untrained base on the
  SQL-only prompt (59.19). Base student with the CoT prompt on Spider dev was
  not measured.
- `g2` 72.53 against the published seed-0 centralized runs: `central` E3 71.37,
  `central_mix` E3 73.21 (not paired here).
- `t2_rat0-7`: T1 rationalizes all 8,659 Spider training rows at EX 83.21
  (non-empty gold 81.89), SQL found 99.95, truncated 0.02, mentions the
  reference 8.01. The base student kept 83.5 on 200 rows (P2.57 T3), so the
  SynSQL stage does not move this number. It sees the gold SQL, so it measures
  copying more than solving.
- `t2` trains on 6,622 rows (76.5%); `g2` on all 8,659.
- The 8.01 is learned from the targets: 259 of 3,336 SynSQL `cot` rows (7.76%)
  mention a "reference solution" or similar, and stage 1 does not filter them
  (stage 2 does). The P2.57 base student's rate on SynSQL was 0%. Runs continue
  unchanged; any later arm on SynSQL CoT filters these rows.
- `t1` and `g1` kept all 3,336 pool rows (`wrong_result` 0), not the 3,335
  written in the queue entry below. Wall 2.6 h and 2.1 h, peak reserved 19.2
  and 18.1 GiB.

## 2026-10-30: P2.58 CoT x RL screen queued (owner)

Owner, 2026-10-30: before any federated run, check centrally whether CoT
and RL help on Spider; use SynSQL's published CoT instead of teacher CoT
(saves about 17 h of teacher generation); drop the self-CoT arm; seed 2
of P2.53 can wait; use both GPUs. Code: nested `3406fb5`.

Design (seed 0, Spider dev only, student Coder-1.5B, LoRA r16, `target_fp32`):

| Stage | G (SQL only) | T (CoT) |
|---|---|---|
| 1, SynSQL pool (3,335 of 3,336 rows; one CoT SQL misses the gold result) | SFT on gold SQL, 2 epochs | SFT on SynSQL `cot` (OmniSQL), solve prompt, 2 epochs |
| 2, Spider train (8,659) | SFT on gold SQL, 2 epochs | rationalize every row with T1 (gold as hidden reference), SFT on the execution-correct ones, 2 epochs |
| 3, RL on 1,200 fixed Spider training questions with non-empty gold (of 7,000) | K=8 samples, T=0.7; `d` DPO + NLL, `r` RFT | same |

- Choices and sources. CoT recipe: OmniSQL (SynSQL CoT, execution-voted;
  CoT vs SQL-only at 7B, Spider dev +3.4, test +5.9); STaR rationalization
  for the Spider targets. RL: on-policy DPO with an NLL term on the chosen
  response (Iterative RPO, Pang et al., NeurIPS 2024), pairs from
  execution feedback with the nearest final SQL (ExCoT, arXiv 2503.19988;
  ExCoT found CoT SFT alone below SQL SFT and the gain coming from DPO on
  CoT), beta 0.1, lr 1e-5 for LoRA (ExCoT full fine-tuning 1e-6; LoRA
  about 10x, "LoRA Without Regret"), 2 epochs, at most 2 pairs per
  question. RFT (RAFT, Dong et al., TMLR 2023) as the cheap comparator;
  RAFT-style rejection sampling matches GRPO on math reasoning (Xiong et
  al., arXiv 2504.11343), so no online GRPO (it needs fast generation we
  do not have).
- SynSQL CoT targets: p50 566, p95 876 tokens (SQL targets p50 123).
  Short CoT suits a 1.5B student better (learnability gap, arXiv
  2502.12143).
- Not sourced: the 1,200-question RL subset, K=8 and the 2 epochs per
  stage were set for the two-GPU budget.
- G and T differ in stage 2 data: G trains on all rows, T on the rows
  whose rationalization is correct (coverage reported).
- If T beats G, a follow-up with teacher-7B CoT on SynSQL is needed:
  SynSQL CoT is not our teacher's contribution.
- First launch stopped at `t2_rat1`: gold SQL `train:4513` does not execute
  (ORDER BY before INTERSECT) and the evaluator raises. Three Spider training
  golds and two Spider dev golds fail this way. Fixed (scored 0, as the
  project eval loop does; those rows cannot enter the T training data or the
  RL pool); finished rows are kept.

## 2026-10-30: P2.57 CoT probe results (not committed yet)

Reported from the server table; publication pending. Seed 0, inference
only, OmniSQL-style prompts. EX (%); on SynSQL the second number is EX on
rows whose gold result is not empty (the databases hold about two rows per
table, so SynSQL EX is a weak check).

| Writer | SynSQL rationalize (gold as hidden reference) | SynSQL solve (no gold) |
|---|---:|---:|
| teacher 7B | 91.33 / 88.03 | 52.33 / 40.85 |
| base student 1.5B | 75.33 / 71.83 | 19.00 / 12.68 |

- On public SynSQL the teacher reasons much better than the student: +33
  points without gold, +16 with gold (the student often rewrites the
  reference into a wrong query; it copies gold in 62% of rows, the teacher
  73%). Reference leaks: teacher 2%, student 0%.
- T4, teacher on Spider dev: CoT 75.73 vs SQL-only 76.89, -1.16 (71/83,
  p=.38). Zero-shot CoT does not help the teacher on Spider.
- T3, base student on 200 Spider training rows: rationalization keeps a
  gold-equivalent final SQL in 83.5% of rows; CoT sampling pass@1 42.6,
  pass@4 71.0.
- Cost (docs/A5000_RUN_CONFIG.md, nested `2316763`): rationalizing all
  8,659 Spider training rows about 5.8 h per round; K=4 sampling about
  25 h per round; teacher CoT on the 3,336 SynSQL rows about 17 h.

## 2026-10-30: owner: Spider only; P2.57 CoT probe queued

Owner, 2026-10-30: focus on Spider dev and test; BIRD EX is no longer a
target. Question: can the server teacher contribute on Spider through
reasoning (CoT) rather than SQL targets, which match gold on about 95% of
top-1 tokens?

Reading of the earlier CoT runs (all with the old Qwen2.5-1.5B-Instruct
student): the P2.10 drop (FL in QP-CoT format, Spider 56.38 vs 62.57
SQL-only) came from template client plans and CoT at inference, not from
BIRD; the BIRD-specific part was the weak teacher (47.07 on BIRD, 43.6% of
plans admitted), which also made P2.15 `dss` lose on SQL row count. An
outside review (2026-10-30) judged a SynSQL-only SFT screen (CoT vs SQL)
uninformative: post-K Spider differences have not predicted post-A ones
(P2.15 `dss` +1.35 after K, -0.97 after A; `goldplan` -3.00, -0.97;
P2.14 +0.29, +1.84), and the paper needs teacher CoT against student
self-written CoT, both after Spider training. It also corrected that the
SynSQL CoT field was written by open-source models, not GPT-4o.

Candidate direction (not adopted): teacher writes CoT on public SynSQL
with the gold SQL as a hidden reference (OmniSQL CoT synthesis); clients
rationalize their own gold SQL (STaR) or self-train on sampled CoT; FedAvg.

P2.57 (nested `31a2774`, one GPU, seed 0, inference only) measures what
decides the next step: T1 teacher and T2 base student CoT on 300 SynSQL
rows (rationalize and solve), T3 base student cost on 200 Spider training
rows (one rationalization, K=4 samples), T4 teacher CoT vs SQL-only on
Spider dev (reference). No reading rule fixed; the training screen
(server S-gold / S-teacher / S-self, then one Spider pass) is designed
after P2.57.

## 2026-10-30: audit of the Spider data, split and EX scoring

Owner asked why FedAvg is not below `central` on Spider test. Local
check (script not committed), seed 0 predictions:

- Spider test CSV equals the raw `test.json` row for row (2,147, same
  order, gold and database); databases from `test_database`. Dev equals
  `dev.json` (1,034). Central train equals `train_spider` +
  `train_others` (8,659, multiset equal).
- Train, dev and test databases are disjoint (146 / 20 / 40). 27 test
  questions and 42 gold SQL strings also occur in train as text, all
  generic ("How many clubs are there?") on other databases.
- The five `alpha_0.1/k5` clients partition central train exactly
  (1,896 + 1,801 + 2,061 + 1,097 + 1,804); each database belongs to one
  client.
- Every test gold executes; 54 return an empty result.
- Re-scoring with the official test-suite comparison: our EX equals it on
  every row when DISTINCT is kept; the official default removes DISTINCT
  and gives about +0.7 to +1.1 to every arm (central 71.91, FedAvg
  72.19, method 73.92; dev central 72.44, FedAvg 68.67). Central minus
  FedAvg: test -0.28 (163/169), dev +3.77 (106/67), as before.
- Reading: the data and the metric are correct; at seed 0 the dev FL
  penalty does not appear on test.

## 2026-10-30: P2.55 FedProx published

Evidence: nested `eb69e5a`. P2.27 FedAvg recipe (Spider only,
`alpha_0.1/k5`, 3 rounds) with FedProx mu 0.01, seed 0, A3. EX / EM,
paired with FedAvg A3 (exact McNemar):

| Set | FedProx | FedAvg EX | FedProx minus FedAvg (EX) |
|---|---:|---:|---:|
| Spider test | 70.42 / 58.69 | 71.50 | -1.07 (50/73, p=.047) |
| Spider dev | 67.12 / 59.57 | 67.60 | -0.48 (33/38, p=.64) |
| Realistic | 57.68 / 50.20 | 59.65 | -1.97 (15/25, p=.15) |
| SYN | 52.03 / 43.81 | 53.68 | -1.64 (29/46, p=.064) |
| DK | 51.96 / 46.36 | 53.27 | -1.31 (11/18, p=.27) |
| BIRD dev | 24.64 / 3.85 | 25.68 | -1.04 (31/47, p=.089) |

- FedProx at mu 0.01 is below FedAvg on every set, by about 1 point; no
  mu tuning. With 3 rounds of 1 local epoch, client drift is small, so
  the proximal term mainly slows local fitting.
- Spider test 0.34 s per question (measured while the other GPU ran);
  the advisor table keeps the shared SLM latency 0.30. The runtime
  reports carry no VRAM peak.
- Advisor table filled: `paper/results/ADVISOR_TABLE_4_2_2026-10-30.md`.

## 2026-10-30: P2.56 teacher 5-shot published

Evidence: nested `cfaad25`. Teacher Qwen2.5-Coder-7B, 4-bit, five fixed
Spider training demonstrations, seed 0. EX / EM:

| Set | 5-shot | Zero-shot | 5-shot minus zero-shot (EX) |
|---|---:|---:|---:|
| Spider test | 76.25 / 59.34 | 77.22 / 46.48 | -0.97 (126/147, p=.23) |
| Spider dev | 77.27 / 63.73 | 76.69 / 51.35 | +0.58 |
| Realistic | 69.88 / 53.94 | 71.06 | -1.18 |
| SYN | 59.09 / 46.62 | 63.83 | -4.74 |
| DK | 62.80 / 54.58 | 62.43 | +0.37 |

- EX does not move on Spider test (exact McNemar); SYN falls 4.74. The
  demonstrations teach the gold SQL style: Spider test EM +12.86.
- 0.74 s per question on Spider test (zero-shot 0.83), peak reserved
  18.9 GB. Advisor table: `paper/results/ADVISOR_TABLE_4_2_2026-10-30.md`.
- Only the dev variants were compared unpaired here; the Spider test pair
  is paired.

