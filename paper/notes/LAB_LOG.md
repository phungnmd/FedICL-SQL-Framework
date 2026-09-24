# FedLS-SQL — active lab log

## Current state

- Active protocol: `v2`, dataset profiles explicit (BIRD with evidence).
- Primary metric: execution accuracy (EX).
- Method status: open. Hinton, KID and flat SeqKD do not show a sufficiently
  strong teacher-specific terminal advantage. At the public endpoint, however,
  row-matched SeqKD beats gold CE on all five sets (2026-09-24 re-analysis).
  P2.9 tests whether client-side retention keeps that edge after terminal A.
- Published: P2.1R BIRD baselines and both public-teacher lanes (`e2ca26e`),
  Hinton headline (`ec5b5e1`), reverse T1 ladder (`1b2c46a`), and full-gold
  control (`5e4f005`), P2.3 terminal endpoints (`2a6e04c`), and terminal
  full-public gold control (`ccb3e91`), SeqKD endpoints and KID public
  (`1e69ae3`), KID terminal (`5d861f8`), and P2.6 matched selected-gold
  endpoints (`fb2329e`).
- Finding: `A>K[fkl]>A` beats matched `A>A` on all five sets at seed 0,
  reaching 66.63 Spider and 31.03 BIRD EX. However, it does not reliably beat
  `A>K[ce]>A`; the result is not soft-logit-specific.
- Finding: terminal SeqKD and KID are statistically indistinguishable on all
  five sets. Their Spider-family means are 56.87 and 56.75; BIRD EX is 28.42
  and 28.94. KID's public stage cost about 21.1 GPU-hours, so it is closed.
- Finding: against matched selected-gold terminal CE, terminal SeqKD changes
  Spider/Realistic/SYN/DK/BIRD EX by -0.10/-0.98/+1.65/+0.75/+0.91 points.
  BIRD gain is below 1.0 and the Spider-family mean gain is only +0.33, so P2.6
  does not justify scaling unchanged flat SeqKD.
- Next: P2.9 terminal-retention gate (`A>K>A[ret]`, SeqKD versus matched
  gold) plus a target-NLL diagnostic, on nested branch
  `experiment/terminal-retention`. Then P2.10, the Struct-SQL QP-CoT lineage in
  every stage (`d66af7a`), with the terminal retention weight set by P2.9.
  P2.10 supersedes the deferred SQL-only P2.8 gate.
- Historical record: `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`.

## 2026-09-25 — KD/FL ordering diagnostic added to P2.9 (no GPU run)

Concern raised: FL gets only 1–2 private rounds (T1/T2/T3 Spider EX
57.35/62.19/64.31), so a KD benefit measured after one terminal round may not
survive FL trained closer to convergence. With one terminal round, WiSE-FT at
α = 0.5 mainly halves the Spider update, so it is a reviewer baseline only.

Nested commit `419a878` adds D1, task arithmetic, as two training-free P2.9
variants: θ_{A>A} + λ·(θ_{A>K} − θ_A) with λ = 0.5 and 1.0. `combine_lora`
builds exact linear combinations of LoRA updates, and WiSE-FT reuses it. The
analyzer applies the registered gates to D1 and reports an ordering signal.
The signal is merge-first when the KD task vector is additive, and replay
otherwise. The full nested suite passes (690 tests). P2.9 now takes about 14 h
per GPU lane.

An R = 4 ordering study is planned in `PIPELINE_NEXT.md`: Sequential,
K-first, Merge, and Replay, each against FL `A⁴` with the same rounds. It is
not implemented yet.

## 2026-09-25 — P2.9 aligned with the retention literature (no GPU run)

A literature check (KD_METHOD_REVIEW §10) found that the P2.9 retention loss
matches LwF, FedGKD, and FedNTD in KL direction, reference model, and data. The
registered weight λ = 1.0 is 10× FedGKD's NLP weight. Nested commit `78a34bd`
adds:
- λ = 0.1 as a second retention variant;
- WiSE-FT as a training-free competitor. It is an exact LoRA weight midpoint
  of the post-K and plain terminal adapters, built by rank concatenation and
  verified to about 1e-7.

The analyzer applies the registered gates to every variant. It reports the
best passing λ for P2.10 and falls back to WiSE-FT only when no retention
variant passes. The λ = 1.0 stage and evaluation names are unchanged. The full
nested suite passes (688 tests). The P2.9 lanes now take about 11 h each on two
GPUs.

## 2026-09-24 — Struct-SQL QP-CoT lineage implemented (P2.10, no GPU run)

Review of the P2.7/P2.8 rationale code found two departures from Struct-SQL.
First, the plan format was a TABLES/COLUMNS/OPERATIONS list that restated SQL
fragments, not the paper's QP-CoT. Second, private stages and the P2.8 final
evaluation were SQL-only, so the format changed between stages. The AST plan
also collapsed correlated aliases (3 BIRD rows), rewrote `SUBSTR` as
`SUBSTRING` (150 BIRD rows), and crashed on ORDER BY after UNION.

Nested commit `d66af7a` adds the Struct-SQL lineage without changing any
existing recipe identity:
- Response format `qp_cot_v1`: the paper's QP-CoT layout and student prompt,
  strict parsing, and a zero-shot teacher prompt.
- Deterministic private template `qp_ast_v1`: correlated aliases kept, SQLite
  spelling kept.
- Struct-SQL data construction: 75/25 ID/OOD databases, the paper's strata,
  and 150+150 validation rows.
- Per-split teacher generation.
- Public stages `K[qp-ast]` and `K[qp-teacher]` with validation early stopping
  that keeps the best adapter.
- Private stage `A[qp]`.
- Four-arm runner (`fl`, `gold`, `tsql`, `teacher`) with analysis and
  publication allowlist.

CPU audits:
- Template: no failures on 20,655 Spider/BIRD train+dev rows. Target median is
  247 tokens (Spider) and 297 (BIRD), comparable to the paper's 362.
- Spider client sequences: at most 2,921 tokens, far below `max_len` 7168.
- BIRD train has only 261 subquery-only rows, below the paper's 22.9% quota.
  The shortfall moves downstream and is recorded.

Deliberate deviations: LoRA r = 16 (federated communication), zero-shot teacher
prompt, and a validation cadence chosen for the A5000 (not reported by the
paper). The full nested suite passes (684 tests). The P2.10 runbook in
`PIPELINE_NEXT.md` starts only after the P2.9 decision, which fixes the
terminal retention weight.

## 2026-09-24 — P2.6 public edge re-analyzed; P2.9 retention gate queued

CPU-only re-analysis of committed batch-16 predictions (no new training).
Row-matched SeqKD minus selected-gold CE on the same 5,319 BIRD rows:

| Endpoint | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| public `A>K` | +1.64 (p=.20) | +2.76 (.19) | +3.38 (.006) | +2.43 (.14) | +3.00 (.004) |
| terminal `A>K>A` | −0.10 (1.0) | −0.98 (.57) | +1.64 (.07) | +0.75 (.63) | +0.91 (.25) |

Values are EX deltas with exact McNemar p. At the public endpoint the SeqKD arm
also has fewer non-executable predictions (share of each set, matched gold →
SeqKD): Spider 19.5 → 14.1, Realistic 25.8 → 18.9, SYN 25.7 → 19.7, DK
25.0 → 20.2, BIRD 28.6 → 26.6. Reading: training on BIRD through
teacher-generated SQL transfers BIRD knowledge with less damage to Spider-style
schema grounding than training on BIRD gold SQL. After terminal A, both arms'
Spider-family error rates converge (16.3 versus 16.5 on Spider). BIRD
non-executable predictions rise again, to 37.2 for SeqKD. The plain private
stage therefore erases the edge.

Decision (user, 2026-09-24): test whether the edge survives terminal A before
more Struct-SQL work. Nested commit `e72ad2d` adds `A[ret]`. It is a private
stage whose clients add `1.0 · KL(post-K global ‖ student)` on SQL target
tokens. The reference is the stage's frozen warm-start adapter; there is no
teacher at the clients and no extra communication. The commit also adds the
P2.9 runner and analyzer, a target-NLL diagnostic (pure-FL student NLL on
teacher versus gold SQL), and a publication allowlist. Existing `A` stage
identities are unchanged, and the full nested suite passes (634 tests). No GPU
was used locally. The P2.8 runbook moved intact to
`archive/superseded_runbooks/P28_STRUCT_GOLD_GATE_DEFERRED_2026-09-24.md`.

## 2026-09-23 — matched-gold terminal gate supersedes public-only screen

The operator reports P2.7 Step 1 completed on the server; local artifacts were
not available for verification here. The current queue requires provenance
checks before training. Its primary contrast is teacher plan+SQL versus source
gold SQL on the exact 1,000 admitted BIRD rows, both from the same Spider-private
parent and both followed by the same Spider-private A. Terminal EX is the
decision; public EX is diagnostic. Final inference uses SQL-only prompts for
both arms because the terminal A trains SQL-only targets. No new EX result is
claimed. The old three-arm public-only queue was archived intact.

## 2026-09-23 — P2.7 engineering hardening (no new EX result)

The joint teacher plan+SQL generator now journals raw outputs before scoring,
rescoring cached output if source SQLite bytes change and preserving the
original batch shape on resume. The run freezes its visited generations for
compact publication. Teacher generation and P2.7 eval record output-token
counts and stopping reasons to expose length-capped responses. P2.7 evaluation
can overlap bounded CPU SQL scoring with GPU decoding; legacy eval defaults,
fingerprints, and CSV columns remain unchanged. These are provenance and
throughput changes, not evidence of a new KD gain. The subsequent P2.8
matched-gold terminal gate is now the next scientific decision.

## 2026-09-22 — P2.6 closed; bounded structured-rationale gate activated

P2.6 published matched selected-gold public/terminal endpoints at `fb2329e`.
At the terminal endpoint, matched gold reaches 65.09/58.66/52.90/49.53/27.51
EX on Spider/Realistic/SYN/DK/BIRD, versus 64.99/57.68/54.55/50.28/28.42 for
SeqKD. The comparison therefore does not meet the registered BIRD or
Spider-family mean promotion thresholds. This closes scaling the same flat
SeqKD recipe; it does not show that teacher-generated SQL has zero value.

P2.7 isolates the remaining hypothesis: whether a validated teacher query plan
adds useful large-to-small structure beyond the teacher SQL itself. The screen
uses a deterministic 1,000-row subset and compares flat SeqKD, deterministic
AST-plan supervision, and teacher-plan supervision under matched training and
evaluation. It is experimental until the quality gate and five-set paired
analysis complete.

## 2026-09-20 — P2.5 complete; KID closed; matched-gold gate activated

P2.5 published both endpoints for SeqKD and protocol-v2 KID. Public EX for
SeqKD/KID is 57.93/58.03 Spider, 46.65/44.09 Realistic, 48.26/46.23 SYN,
45.61/44.30 DK, and 34.68/35.40 BIRD. After the identical terminal private
stage it is 64.99/65.47, 57.68/57.09, 54.55/54.16, 50.28/50.28, and
28.42/28.94. No terminal KID-minus-SeqKD difference is paired-significant.
The terminal private stage repairs Spider-family robustness but reduces BIRD
by 6.26 points after SeqKD and 6.45 after KID.

KID therefore adds substantial compute without a measurable accuracy benefit
and is no longer an active method candidate. GKD remains closed for compute;
clean RKL/MiniLLM and deeper Hinton are not opened by this negative result.

The next gate reuses the committed one-epoch matched-gold parent on the same
5,319 BIRD row identities as SeqKD. One GPU evaluates its public endpoint and
the other appends/evaluates the missing terminal `A`. Only after this paired
teacher-target-versus-gold comparison may the project choose between terminal
knowledge retention, matched SeqKD-2/gold-CE-2, or a structured-rationale
screen.

## 2026-09-17 — GKD closed for cost; protocol-v2 KID activated

The autoregressive on-policy GKD lane was stopped before publication: it was
technically valid but too expensive for the available A5000 schedule. Its
partial artifacts are diagnostic only and must not be resumed or cited.

Protocol-v2 KID is now implemented as the bounded replacement. It uses the same
5,319 BIRD public prompt identities as SeqKD, row-matched clean gold SQL,
evidence-aware prompts, a frozen 4-bit Qwen2.5-Coder-7B teacher, 20% random
masking, one-pass greedy student rewriting, clean-gold CE, and token-level
`KL(p_student || p_teacher)` on rewritten prefixes at `T=1`. It does not use an
autoregressive rollout or a teacher-logit cache. The implementation includes
exact crash resume and immutable stage/result identities; the full nested test
suite passes 461 tests. Active endpoints are `A>K` and `A>K>A` on five sets.

SeqKD and KID share public prompts but not targets/objectives, so this is an
end-to-end method comparison. If KID passes, a matched clean-RKL arm is required
before attributing the gain specifically to imperfect-data rewriting.

## 2026-09-17 — cancellation requested; SeqKD/GKD comparison planned (superseded)

User requested stopping both K2 lanes and comparing SeqKD with on-policy GKD
before/after identical terminal A. No remote server connection was available
to verify termination. Keep partial checkpoints, not completed evidence. Archived
K2 commands; proposed same-parent, same-5,319-prompt comparison with frozen teacher.
GKD was subsequently implemented, then closed before publication because its
measured execution cost was impractical. Existing matched gold CE remains a
control. The KID decision above supersedes this entry.

## 2026-09-16 — P2.4a does not isolate retained Hinton value

Follow-up decision: test the under-training hypothesis first with matched
two-epoch public CE/Hinton from the same FL parent. P2.4c uses fresh roots,
the existing 9,428-row cache, and planned two-epoch schedules. Both public and
terminal-private endpoints are evaluated. Phase-1 publication is required
before terminal A because stage parents must be committed. Earlier advice
to defer all Hinton depth experiments was too strong; non-significance at
one epoch is not evidence of equivalence. SeqKD remains available afterward.

Nested commit `ccb3e91` publishes `A>K[ce]>A` and five row-matched evaluations.
CE/Hinton EX is 66.54/66.63 Spider, 57.28/57.09 Realistic, 54.45/55.32 SYN,
51.21/50.65 DK, and 29.53/31.03 BIRD. The Hinton-minus-CE deltas are
+0.09/−0.19/+0.87/−0.56/+1.50 points; exact paired McNemar p-values are
1.000/1.000/.439/.749/.102. The four-set Spider-family means are 57.37 and
57.42. Thus terminal consolidation is useful, but the current result does not
show that soft logits cause the gain.

Do not launch Hinton-only K2 or recurrence from this evidence. The next cheap
causal test appends the identical terminal `A` to the published selected-row
matched-gold and SeqKD parents. It holds the 5,319 rows and private compute
fixed and changes only gold versus teacher-generated sequence targets. See
`paper/results/P24_TEACHER_SIGNAL_REVIEW.md`.

## 2026-09-16 — separate active queue from completed runbooks

Moved completed P2.1R/P2.2 commands, direction/prerequisite notes, and prior
decision gates to [the completed runbook](../archive/completed_runbooks/P2_1R_P2_2_COMPLETED_2026-09-16.md).
PIPELINE_NEXT now contains only P2.3 launch, publication, and the next method
decision. All five active PowerShell blocks and the archived command blocks
are unchanged. No code, results, adapters, or server artifacts were modified.

## 2026-09-16 — server launch queue

P2.3 now separates one-time Git sync from resumable GPU commands. Run the
Hinton-parent two-step/client smoke, publish only its metrics/config, then
launch student-only `A>A` on GPU 0 and `A>K[fkl]>A` on GPU 1. Each adds one
private epoch/client and FedAvg; no teacher/cache generation. Keep smoke
artifacts; removed the automatic cleanup command. After both jobs exit, run
the shared five-set evaluation and publish its compact records. No P2.3 GPU
completion or new accuracy result has been reported yet.

### Follow-up — continuous GPU lanes

User reports smoke running. Replaced manual train/eval handoffs with two
single-line lanes: each trains its terminal private stage and evaluates all
five sets. No server code change or mid-smoke pull is needed. Training is
parallel; a shared Windows-session mutex serializes eval because the current
evaluator names result directories at second resolution. Each lane/dataset
has separate resume state; training roots and scientific settings are unchanged.
Smoke publication is deferred to the single final publication command alongside
the two full stages and ten single-arm eval records. Stop only after results
are ready for method selection (or on a real error). CONVENTION §6.1 now makes
bundling already-decided steps the default; publication stays separate from
concurrent computation.

### Follow-up — remove eval serialization

Nested `362aced` replaces timestamp-only auto-generated result IDs with
timestamp + optional fingerprint hash + UUID, using exclusive directory
creation with collision retries. Eval supplies its existing manifest
fingerprint; explicit training/stage IDs and old result paths are unchanged.
Removed the temporary mutex from both P2.3 commands: train and five-set eval
can now run concurrently in output-disjoint lanes. No scientific recipe or
scoring change. Finish smoke before syncing the new code; a passed smoke
does not need retraining. Existing exact-fingerprint resume works as before;
code-SHA changes are not silently ignored by eval checkpoints.

Validation: 76 targeted tests passed, including 16 same-second concurrent
publications, forced UUID-collision recovery, and completed-manifest skip for
both old and new directory names. Ruff passed. No GPU run performed locally.

## 2026-09-16 — P2.3 terminal consolidation passes the seed-0 gate

Nested result commit `2a6e04c` publishes the smoke, `A>A`, `A>K[fkl]>A`, and
ten five-set evaluation records. EX for `A>A` versus `A>K[fkl]>A` is
62.57/66.63 Spider, 55.31/57.09 Realistic, 52.22/55.32 SYN, 47.10/50.65 DK,
and 16.49/31.03 BIRD. Exact paired McNemar p-values for the terminal-Hinton
advantage are 0.000359/0.3557/0.00808/0.01834/<1e-40. The Realistic delta is
positive but not individually significant; all claims remain seed 0.

The result is more than a terminal-A recovery effect because the final Hinton
chain beats matched-private-compute `A>A` on every evaluation. Against teacher
7B it closes 48.0/13.4/41.4/31.5/50.3 percent of the Pure-FL gap on
Spider/Realistic/SYN/DK/BIRD. It does not establish teacher parity.

The next gate at that point was `A>K[ce]>A`; P2.4a above has now resolved it
without a reliable Hinton advantage. Explicit `--server-epochs` support and K2
lineage labels remain available in nested commit `fca5eef`, but K2/recurrence
is deferred while terminal SeqKD is tested. Multi-local-epoch `A[e2/e3]`
remains outside the active screen because non-IID client drift is the stronger
prior. Detailed P2.3 evidence is in
`paper/results/P23_TERMINAL_CONSOLIDATION_REVIEW.md`.

## 2026-09-10 — official BIRD timeout closure

Source audit found that BIRD's original and Mini-Dev EX evaluators assign one
30-second deadline to the combined prediction/gold execution. MAC-SQL likewise
uses 30 seconds for EX and 60 seconds only for VES. The previous live scorer
used 60 seconds independently for each SQL, although its set-of-row-tuples
comparison was correct. Nested commit `2178d5a` replaces it with
`bird_official_set_pair_timeout30_v2` and adds a fingerprinted, resumable CPU
rescorer for saved prediction CSVs. Training and generation remain valid; no
model inference needs repeating. The independent BIRD-train gold audit remains
at 60 seconds because it is a data-integrity diagnostic, not benchmark EX.

## 2026-09-03 — BIRD protocol reset

Audit confirmed that BIRD `evidence` existed in processed source rows but was
deliberately excluded by the common Spider prompt builder. Consequently the
teacher, target generation, student SFT/KD, and BIRD evaluation all operated in
a no-knowledge setting. BIRD officially allows this setting, so old numbers are
not fabricated; however, they cannot serve as the standard with-evidence BIRD
baseline or as canonical evidence for the revised paper without explicit
relabeling.

Observed selection evidence:

- evidence populated: 93.16% of BIRD source and 90.34% of the Qwen pool;
- selected examples have shorter evidence on average: 79.24 vs 95.96 chars;
- selection retention declines from 52.19% for 1–60 chars to 25.60% for at
  least 131 chars;
- evidence length and selection have Spearman `r=-0.2207`, `p=2.35e-104`;
- an existing 512-row diagnostic did not show teacher-CE gain increasing with
  evidence length (`r=0.0128`, `p=.779`).

Interpretation: the no-evidence selector is biased toward examples requiring
less external knowledge. This motivates the reset, but does not itself prove
that evidence explains every prior gain.

Implementation completed:

- `Text2SQLExample` introduced with backward-compatible `SpiderExample` alias;
- explicit `spider`, `bird_with_evidence`, `bird_no_evidence`, and `legacy`
  profiles added;
- evidence is rendered consistently in client SFT, server SFT/KD, teacher
  targets, teacher-logit caches, and evaluation;
- profiles/evidence modes enter fingerprints and incompatible data fail before
  model loading;
- federated split construction now accepts arbitrary processed train/test CSVs;
- server artifact retirement is dry-run/quarantine based and never deletes;
- versioned explicit BIRD JSON/database ingestion now supports filtered-train
  and cleaned/original dev without relying on archive layout;
- full nested test suite: 345 passed.

P2.0a then froze deterministic audits at nested commit `4ae6e35`. Spider has
8,659 train and 1,034 test rows. Original BIRD has 9,428/1,534 rows with
8,783/1,386 populated evidence values. Both train/test pairs have zero DB
overlap; the BIRD prompt probe contains `### Evidence:` and the Spider probe
does not.

## 2026-09-04 — overnight baseline preparation

Nested commits `346342c` and `11ab685` close the remaining training-input mechanics:
immutable protocol-v2 CSV materialization, semantic schema grouping for a
BIRD K5 split, immutable shard hashes, and deterministic `client_train` result
paths. Full test suite: 347 passed.

The official filtered/cleaned release and evaluator remain open. Nevertheless,
the audited original 9,428/1,534 BIRD release is a valid explicitly labeled
with-evidence compatibility track. Centralized E1/E2 and pure-FL T1–T3 may be
trained now because evaluation implementation cannot change their checkpoints.
No EX result from this track becomes canonical until every checkpoint is scored
through the same official BIRD evaluator.

## 2026-09-04 — baseline runner and evaluator closure

Nested commit `9d777db` fixes a final protocol gap: although dataset profiles
previously recorded `evaluator=bird`, the shared loop still executed Spider EX.
Evaluation now dispatches the official BIRD SQLite set-of-row-tuples comparison,
records scorer identity `bird_official_set_v1` in resume fingerprints, and has
fixtures showing the intended differences from Spider column/order semantics.
This historical identity was superseded by the 30-second pair contract in
`2178d5a`; only its saved SQL, not its embedded EX, remains reusable.

The same commit adds `scripts/run_protocol_v2_baselines.ps1`. Separate phases
validate code, quarantine 31 exact invalid v1 roots, materialize and publish
inputs, run training/evaluation, then publish only manifest-resolved compact
outputs. The P2.1 suite yields base, centralized E1/E2, and pure-FL T1/T2/T3
under BIRD-original with evidence. Full nested suite: 350 passed.
Nested commit `40255f4` briefly added two-GPU parallel orchestration. Commit
`e1f3127` supersedes it at operator request: all four compute stages now run
sequentially on physical GPU 0, with scientific flags, output roots, and exact
resume behavior unchanged. Full nested suite remains 350 passed.
Commit `8a17542` fixes server validation only: the runner resolves the locked
`dev` extra for `pytest` and accepts descendants of the required refactor base
without a misleading warning. No scientific or checkpoint contract changed.
Commit `767301d` additionally forces UTF-8 for Python and inherited subprocesses
after a Windows CP1252 console rejected a Unicode diagnostic arrow during the
split test. This is an environment-compatibility fix only.
Commit `d1df12d` normalizes absolute Windows result paths from the federated
manifest before applying the publication allowlist. P2.1 artifacts and metrics
were unaffected; only compact result publication had failed.

## 2026-09-06 — P2.1 audit result and context repair

P2.1q audited all 9,428 train prompts and independently rescored all saved dev
SQL. It found 974 truncated prompts; 754 lost all provided evidence. The old
Spider-tuned `max_len=2560` checkpoints are therefore rejected as canonical.
Scoring itself is stable: only centralized E1 changed by one correct row
(31.55→31.62 EX), five arms were unchanged, no disk-full error recurred, and
1,532/1,534 dev gold queries completed within 60 seconds.

Official BIRD's current fine-tuning example uses a long 18k context and gradient
checkpointing. Nested `d21f777` introduces a measured 7,168-token contract for
our frozen Qwen/full-schema setup, fail-closed overflow handling, fingerprinted
gradient checkpointing, longest-eight-row VRAM smoke, and new immutable roots.
P2.1R must finish before the reference FedLS ladder. The 6,601-row filtered
release remains a separate, explicitly labeled final-release/data-quality gate.

## 2026-09-06 — active-result cleanup

`VALID_RESULTS_AND_ADAPTERS.md` now lists the only retained accuracy rows,
server adapters, and missing baseline/ablation cells. Active result scanners
retain Spider-only Base/Centralized/FL/FedProx, Gemma Base/FL, Secure Sum, and
the independent teacher resource reference. BIRD-dependent v1 results,
truncated-context P2.1 trained arms, mixed/superseded probes, generated teacher
targets, and final-adapter resource comparisons were moved to recoverable Git
archives. No historical evidence was deleted. Nested commit `7b487bd` records
the archive moves, adds the second server-quarantine manifest, and makes active
FedLS examples explicit about BIRD evidence, 4,096-token context, and v2 output
roots. Full nested suite: 356 passed.

## 2026-09-10 — independent direction runners

P2.1R baseline computation completed on the experiment server; its saved BIRD
SQL still requires the official 30-second rescore before publication. The
BIRD-public Qwen-7B target generator has a valid partial row checkpoint. Its
new progress bar counts only pending rows, so `0/2300` denotes a resume after
roughly 7,128 completed rows rather than regeneration of all 9,428 rows.

Nested commit `8caa610` replaces the hard-coded GPU-0/GPU-1 closure scheduler
with two output-disjoint entry points. `run_protocol_v2_spider_private.ps1`
prepares BIRD-public targets for Spider-private/evaluation;
`run_protocol_v2_bird_private.ps1` prepares Spider-public targets for
BIRD-private/evaluation. The calling PowerShell process selects exactly one GPU
through `CUDA_VISIBLE_DEVICES`. The same commit freezes metadata-complete
Spider v2 train/dev files and the existing semantic K5 partition under a new
immutable root. Full nested test suite: 364 passed.

## 2026-09-10 — direction-runner technical review

The two directions were audited end to end. `spider_private` uses Spider K5
private clients/evaluation and BIRD-original public supervision with evidence;
`bird_private` reverses those roles and retains evidence in every BIRD client
and evaluation prompt. Teacher target generation uses full schema, zero demos,
256 output tokens and the declared public profile. Selection first rejects
non-executable SQL, then applies the dataset-specific EX evaluator; the gold-CE
control uses the exact same selected source indices and differs only in target
SQL. Both public teacher dev evaluations together provide the Qwen-7B anchor on
both Spider and BIRD without duplicate inference.

Nested `c13fc9f` adds read-only SQLite execution, atomic recovery of only a
partial final teacher-target checkpoint line, generic source-gold provenance,
and stronger frozen dataset/split guards. Evaluator identities are unchanged,
so accepted historical results are not invalidated. Nested `8c72764` pins the
reviewed runner base. Full nested suite: 369 passed.

The runners deliberately stop after teacher/pool prerequisites. They do not
yet produce FedLS adapters. The next scientific gate is the matched T1 ladder:
pure FL, matched public-gold CE, execution-matched teacher-target CE, and the
  same target CE plus Hinton forward KL from one shared T1 client/FedAvg initialization.

On 2026-09-11, the BIRD teacher dev evaluation completed at EX `47.1%`, EM
`6.5%`, but the wrapper failed afterward because its resume directory contained
three manifests rather than exactly one. No inference result was lost.
Nested `633743c` now validates evaluator, arm set and artifact existence across
all manifests, selects the newest compatible completion, and skips model
inference when such a result already exists. Nested `3b98b54` pins this fix for
server runs. Full nested suite: 370 passed.

## 2026-09-11 — soft-KD baseline reset

Hinton forward KL replaces reverse KL as the active soft-logit baseline. The
server loss is target CE plus `T^2 KL(p_teacher^T || p_student^T)`, with `T=2`
and equal loss weights by default. Nested commits `3e85e77` and `951960b`
remove the RKL/KID implementation and CLI, fingerprint temperature, and require
new caches marked `kd_objective=hinton_forward_kl`; 362 tests pass. Existing
RKL artifacts remain historical only and cannot resume into the new lineage.
No further KD objective is opened until the corrected two-direction T1 ladder
has been evaluated.

## 2026-09-11 — protocol-v2 prerequisite closure and first matched T1

Nested result commit `e2ca26e` publishes both dataset-correct teacher pools,
teacher dev predictions, corrected BIRD baselines, and the first matched T1
ladder. BIRD public→Spider private retains 5,319/9,428 targets (56.42%);
Spider public→BIRD private retains 7,251/8,659 (83.74%). Teacher zero-shot EX
is 47.07 on BIRD dev and 76.69 on Spider.

The official BIRD 30-second pair rescore gives Base 15.97, Centralized E1/E2
31.42/34.94, and Pure FL T1/T2/T3 22.75/28.36/31.10 EX. In the first matched
transfer direction, Pure FL is 56.96, matched-gold CE 56.09, and SeqKD 57.64
EX on Spider. Paired rows show SeqKD corrects 140 Pure-FL errors but regresses
133 Pure-FL successes, a net gain of seven. This does not open T2/T3. Next are
the reverse matched T1 ladder and Hinton-forward-KL T1; method selection remains
open.

## 2026-09-12 — separate SeqKD from canonical Hinton KD

The planned 5,319-row `teacher-target CE + Hinton FKL` hybrid is removed from
the active matrix. Its partially generated full-logit cache uses selected
teacher-SQL prefixes and cannot support canonical Hinton KD. The operator
approved permanent deletion of its exact active/quarantine roots to reclaim
disk; it must not be resumed or regenerated.

The two KD baselines are now intentionally separate: SeqKD trains on the 5,319
execution-verified teacher sequences, while canonical Hinton KD compares full
public-gold CE against full public-gold CE plus `T^2 KL(teacher || student)` on
all 9,428 BIRD public rows under gold-prefix teacher forcing. This requires a
new cache and lineage. GKD/on-policy KD, MiniLLM, and a newly implemented RKL
lineage remain conditional follow-ups after these baselines and the reverse T1
ladder are complete.

The canonical BIRD-public cache is activated at
`artifacts/protocol_v2/teacher_logit_cache/p22d_bird_gold9428_qwen7b_to_qwen15b_raw_logits_s0`.
It renders all 9,428 original BIRD training rows with evidence and gold SQL,
stores full-vocabulary fp16 teacher logits (temperature is applied later by
training, with canonical `T=2`), and is output-disjoint from
the concurrently running reverse T1 ladder. It remains an uncommitted
intermediate; the downstream training result will publish its fingerprints.

The cache completed in 67,379.4 seconds (7.15 seconds/example): 9,428 examples
map to 9,425 unique content-addressed shards because three rendered token
sequences are duplicates. The downstream T1 comparison is now active on GPU 1:
full-public-gold CE versus balanced Hinton FKL (`lambda_ft=lambda_kd=0.5`,
`T=2`), sharing the accepted Spider-private FedAvg initialization. SeqKD stays
a separate sequence-level reference arm.

Execution priority is now the headline direction: Spider-private client CE ->
FedAvg -> BIRD-public Hinton FKL -> T1. GPU 1 runs Hinton before full-gold CE,
then evaluates Centralized-E3, Pure-FL-T1, SeqKD-T1 and Hinton-T1 on Spider,
Realistic, SYN, DK and BIRD. Existing teacher anchors (Spider 76.69 EX; BIRD
47.07 EX) are reused, with new teacher evaluation only for the three Spider
variants. GPU 0 continues the independent reverse matched T1 ladder unchanged.

## 2026-09-13 — prioritize a terminal-FedAvg endpoint test

An implementation audit corrected the assumed round endpoint. The current
reference runs client LoRA training -> FedAvg -> public server KD and returns
the post-KD `m_g`; repeated rounds also end after KD. It has not historically
deployed a final FedAvg adapter after KD.

The first method-improvement gate after the active T1 jobs is therefore a
private re-anchoring endpoint: `A -> K -> A`, where `A` is client training plus
FedAvg and `K` is public KD. The causal comparison must include `A`, current
`A -> K`, matched-compute no-KD `A -> A`, and candidate `A -> K -> A`. One local
epoch is tested first. Terminal FedAvg is promoted only if it beats both
`A -> K` and `A -> A` on primary Spider/variant EX while retaining useful BIRD
transfer; extra communication is reported. This scheduling test now precedes
new KD objectives and recurrent T2/T3 expansion.

## 2026-09-14 — Hinton T1 exposes public adaptation versus private retention

The P2.2d headline suite completed. On a single shared batch-size-16 evaluation,
Centralized-E3/Pure-FL-T1/SeqKD-T1/Hinton-T1 EX is
67.31/57.35/57.93/58.32 on Spider, 55.91/54.92/46.65/42.72 on Realistic,
54.06/49.32/48.26/44.58 on SYN, 53.27/45.23/45.61/45.42 on DK, and
17.73/14.80/34.68/36.70 on BIRD. Teacher EX on the three newly measured Spider
variants is 71.06 Realistic, 63.83 SYN, and 62.43 DK.

Hinton improves over Pure FL by 0.97 points on Spider and 21.90 on BIRD, but
regresses 12.20 on Realistic and 4.74 on SYN; DK changes by only +0.19. Its
mean over Spider plus the three variants is 47.76 versus 51.71 for Pure FL.
The result therefore supports a domain-retention diagnosis: the terminal BIRD
public update learns BIRD but overwrites part of the Spider-private robustness.
It does not isolate the value of teacher logits because the full-BIRD gold-CE
control is not yet available.

Next, run full-public-gold CE from the identical T1 FedAvg checkpoint and
implement the one-epoch `A -> K -> A` terminal-FedAvg candidate with matched
`A -> A`. Do not open seeds, recurrent T2/T3, or alternative KD losses yet.
The completed manifests and paths were operator-verified, but compact result
publication is still pending. Headline batch size 16 also explains why its
shared-arm numbers must be reconciled rather than silently replacing the
earlier batch-size-8 matched ladder.

## 2026-09-15 — full-gold CE isolates useful logits but not retention

P2.2f evaluates the full-BIRD-public gold-CE adapter at the same batch size 16
as the headline suite. EX is 55.0 Spider, 47.0 Realistic, 43.9 SYN, 40.9 DK,
and 32.1 BIRD. Relative Hinton FKL deltas are +3.32, -4.28, +0.68, +4.52, and
+4.60 points respectively. Forward-KL teacher logits therefore provide signal
beyond ordinary public gold CE on four of five datasets, most clearly on BIRD,
DK, and Spider. They do not solve the Realistic regression.

Against Pure FL, full-gold CE loses 2.35/7.92/5.42/4.33 points on
Spider/Realistic/SYN/DK while gaining 17.30 on BIRD. Together with Hinton, this
confirms that the main observed failure is the terminal public stage shifting
the model away from private Spider robustness. P2.3a terminal private
re-anchoring (`A -> K -> A`) with matched `A -> A` is now the next experiment.
The BIRD NLTK/hardness warnings affect only EM and hardness diagnostics, not EX.
Compact training/evaluation publication remains pending.

## 2026-09-15 — published P2.2 artifacts verified

Result commits `5e4f005`, `1b2c46a`, and `ec5b5e1` publish full-gold control,
reverse ladder, and Hinton headline. All student counts and EX were recomputed
from CSVs. Paired row identities and full prompts match on every dataset.
Exact full-gold EX is 55.03/47.05/43.91/40.93/32.14; this supersedes the rounded
values and deltas in the preceding entry. Hinton-minus-gold is
+3.29/−4.33/+0.67/+4.49/+4.56 points on Spider/Realistic/SYN/DK/BIRD.

Hinton corrects/loses 104/70 full-gold answers on Spider and 157/87 on BIRD;
against Pure FL the Spider net is only +10. Realistic loses 62 net FL answers
despite fewer execution errors. Reverse FL/gold/SeqKD is 22.88/20.73/24.45 EX;
reverse SeqKD corrects 175 and loses 151 (net +24).

The earlier batch-size-8 and headline batch-size-16 FL/SeqKD predictions
differ in 86/58 rows with identical prompts. Batch size is a known difference,
not a proven sole explanation. Prior statements that public KD 'confirms'
forgetting or that batching 'explains' drift should be read as hypotheses.
These single-seed results compare the combined Hinton objective with CE,
including its changed CE weight. They do not isolate logits alone.

Updated the main tables, valid adapter ledger, registry, architecture, TODO,
and queue. Detailed artifact map and paired counts are in
`paper/results/P22_TRANSFER_REVIEW.md`. Next is implement/smoke terminal
private consolidation, then `A→A` and `A→K→A` at one local epoch; if useful,
add `A→gold CE→A`. No new teacher cache is needed.

## 2026-09-15 — composable stage chains for terminal consolidation

The fixed `round` CLI could not append a private stage after KD: round `t` must
start from round `t-1` inside the same output root, and each root is locked to
one arm. Nested `810d8c4` adds `run.py stage private|public`
(`fedicl_sql/federated/stage_chain.py`). A stage warm-starts from a committed
parent result row, derives its chain from that row (`fedavg` r1 = `A`,
`fedkd` r1 = `A>K[fkl]`), hashes the parent adapter at run time, and writes an
immutable `stage.json` plus one `federated_stage__...` result row with client,
aggregation, communication, and resource records. Changing the parent row,
parent adapter bytes, or recipe for an existing stage root fails closed.

`round`/`run` behavior and all published setup/run IDs are unchanged; after
extracting shared recipe helpers, setup IDs were verified identical to the
previous code for `fedavg`, `fedavg_pub`, `fedkd`, and `florana_kd`. A private
stage reuses the round seed and deterministic client order, so `A>A` from Pure
FL T1 is the Pure FL T2 recipe. Mocked-training tests: 373 passed. Adapters
exist only on the GPU server, so the Mac check confirmed only CLI wiring and
parsing of the real Windows-path Hinton row. Next: server smoke, then `A>A` and
`A>K[fkl]>A` on two GPUs and the five-set batch-size-16 evaluation
(`PIPELINE_NEXT.md`, *Active P2.3 commands*).

## 2026-09-15 — stage-chain review fixes

- `4961fb6`: validate result pairs on resume; recover incomplete publication
  without retraining, retain interrupted bytes, and exclude resumed timing.
- `ecfcd5a`: bind complete parent metrics/config SHA256 values; require both
  files committed and unchanged. Infer Hinton only from recorded server
  `kd_direction=fkl`; reject historical reverse-KL/unknown parents.
- `014b118`: atomic version-2 stage contracts and explicit plaintext private
  aggregation. Version-1 roots are not silently migrated; preserve and inspect
  any already-created roots before selecting a new one.

Validation: 86 targeted CPU/mock tests passed across stage chains, round loop,
checkpoint/result recovery, dataset profiles, and federated splits. Tests use
the real published P2.3 FL/Hinton parent rows, cover Git CRLF checkout and
committed/uncommitted parent drift, and simulate interrupted publication.
Ruff and private-stage CLI help passed. No GPU training was run locally.
Scientific settings, existing round results/adapters, and teacher cache are
unchanged. Next remains P2.3 server smoke, then matched `A>A` / `A>K[fkl]>A`.
