# FedLS-SQL — run queue

This is the only file with commands to run. Each command is one line of
PowerShell. Run it from the `fedicl-sql/` root on the Windows GPU server.
Results and decisions go to `LAB_LOG.md` after a run finishes.

## Now (2026-09-30)

What we know (details in `LAB_LOG.md`):

- A public BIRD stage followed by one more FedAvg round beats FL alone on all
  five sets at seed 0, with the same private-training budget. The public stage
  adds compute; the centralized E3 reference has a different private budget.
- Hinton's BIRD advantage over full-gold CE shrinks from +4.56 at `A>K` to
  +1.50 at `A>K>A`; the terminal Spider-family mean difference is +0.05.
  There is no reliable terminal teacher advantage yet. SeqKD shows a similar
  narrowing against its selected-gold control.
- Struct-SQL (P2.10) looks worse at the public endpoint. Terminal results and
  SQL-marker rescoring still need to be consolidated; this file is not a live
  GPU-status report.

**Fixed boundary (owner decision, 2026-09-30):** Spider private data stay at
clients. BIRD public data, the frozen 7B teacher and teacher-logit caches stay
at the server. Clients train the SLM and exchange adapters only. Public replay
at clients, public-buffer downloads and client logit-cache transfers are
excluded because of their storage, communication and compute cost.

The next work, in order:

1. **Finish P2.10** and check whether the QP-CoT format already hurts after the
   first FedAvg round, before any KD (commands below).
2. **A1: server-side merge screen.** Evaluate Hinton/full-gold first using
   existing checkpoints. SeqKD/selected-gold are secondary comparisons.
3. **A2: two-round server KD.** Plan `A>k1>A>k2`, with one total public K
   budget, against `A>A>K` and matched gold controls. Implementation is still
   required. A failed merge does not rule out this schedule.

Changing the public dataset is deferred. Keep the teacher, student, client
split and BIRD pool fixed during A1/A2. Interleaving is established prior art;
the question is whether it preserves useful teacher transfer under this
public/private distribution shift.

Paused: P2.9 retention (`ret0p1` and the target-NLL diagnostic). The runbook is
in the [paused P2.9 file](../archive/paused_runbooks/P29_TERMINAL_RETENTION_PAUSED_2026-09-26.md).
Its merge variants now run as Direction A1 below.

Useful read-only views (CPU, any time):

```powershell
$env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python scripts/show_p210_results.py; uv run python scripts/rescore_p210_sql_marker.py
```

```powershell
$env:PYTHONUTF8='1'; $env:CUDA_VISIBLE_DEVICES=''; uv run python scripts/show_p29_merges.py
```

## 1. Finish P2.10 (Struct-SQL)

Required nested commit: `e735779` or later. The last recorded lanes finish
the terminal stages of `teacher` (GPU 0) and `gold` (GPU 1). The `tsql`
terminal stage is optional and skipped: it is not in the gate.

Confirm running jobs have exited before any Git sync or publication. Do not
restart completed training merely to follow an archived runbook.

**Does QP-CoT hurt before KD?** Struct-SQL uses only 1,000 public rows, so the
FL parent itself must be checked. This evaluates the QP-CoT model after the
first FedAvg round (`fl/t1`) on all five sets. Sets already done are skipped.
Compare its row with `sql FL T1` in `show_p210_results.py` (57.35 / 54.92 /
49.32 / 45.23 / 14.80).

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; uv run python scripts/run_p210_struct_sql.py --phase eval --arm fl --endpoint t1; if ($LASTEXITCODE -ne 0) { throw 'FL t1 eval failed' }; uv run python scripts/show_p210_results.py
```

When both lanes print `complete`, analyze and publish:

```powershell
$ErrorActionPreference='Stop'; $env:PYTHONUTF8='1'; uv run python scripts/run_p210_struct_sql.py --phase analyze; if ($LASTEXITCODE -ne 0) { throw 'P2.10 analysis failed' }; Get-Content audits/protocol_v2/p210_struct_sql_s0/summary.md; uv run python scripts/rescore_p210_sql_marker.py; $Rel=@(uv run python scripts/list_p210_publication.py); if ($LASTEXITCODE -ne 0) { throw 'P2.10 allowlist failed' }; git add -- $Rel audits/protocol_v2/p210_struct_sql_s0/rescore_sql_marker.json; git diff --cached --check; if ($LASTEXITCODE -ne 0) { throw 'Staged content check failed' }; git commit -m 'results: publish P2.10 Struct-SQL lineage'; git push origin experiment/terminal-retention
```

Report both scores: the strict parser (plan must have three sections) and the
SQL-marker rescoring, which is how the Struct-SQL release scores EX.

Keep P2.10's existing gate: terminal `teacher - gold` BIRD >= +1.0 point,
Spider-family mean >= +0.5, and no Spider-family set below -1.0. Report the
gate under both scoring rules; do not silently replace the original strict
result with SQL-marker EX. If neither supports a useful terminal advantage,
close this configuration as a negative result and continue to A1. If the two
scores disagree, diagnose format failures before deciding. No larger teacher
or full-pool expansion is queued. Without terminal `tsql`, do not attribute a
terminal difference specifically to the teacher's plan.

Original design, completed steps and deferred options are preserved in the
[superseded P2.10 runbook](../archive/superseded_runbooks/P210_STRUCT_SQL_ORIGINAL_RUNBOOK_2026-09-30.md).

## 2. Direction A — BIRD public pool

### A1. Merge screen (evaluation only, no training)

Question: does a weight merge keep the teacher's edge after FedAvg? Four arms,
all from the same FL T1 parent and committed rows:

| Arm | Public stage | Rows | Control for |
|---|---|---:|---|
| `seqkd` | SeqKD (teacher SQL) | 5,319 | — |
| `gold` | gold CE on the same rows | 5,319 | `seqkd` |
| `hinton` | gold CE + Hinton forward KL | 9,428 | — |
| `fullgold` | gold CE | 9,428 | `hinton` |

Three merges per arm, each built in seconds on CPU:

- `wise0p5`: half the model after K plus half the model after the last FedAvg.
- `arith0p5`, `arith1p0`: FL `A>A` plus λ × (model after K − FL T1), λ = 0.5, 1.0.

These are exact combinations of effective LoRA updates, not averages of the
A/B factors. With r16 sources, `wise0p5` stores rank 32 and the arithmetic
variants rank 48. Report adapter bytes/rank and deployment cost; compression
back to r16 would be a separate experiment.

Read teacher minus gold for the **same merge** (`show_p29_merges.py`), and each
arm versus its own plain terminal. The prospective A1 screen is:

- teacher minus gold: BIRD >= +1.5 points; Spider-family mean >= -0.5 and no
  individual Spider-family set below -1.0;
- merged teacher versus its own plain terminal: BIRD must improve,
  Spider-family mean >= -0.5 and no individual Spider-family set below -1.0;
- report the gold arm's absolute changes too, so a larger teacher gap caused
  only by degrading gold is not treated as successful retention.

This replaces the earlier requirement for >= +1.0 Spider-family teacher gain
for future A1 selection. Preserve any earlier gate verdicts separately; do
not relabel P2.9 or P2.10. These margins are screening choices, not proof of
equivalence or significance. All fixed variants are reported; seed 0 is
exploratory, not a final test used to tune and certify a winning merge.

Run when the P2.10 lanes are done. About 1–1.5 h per merge per arm, so about
7–9 h per lane. Required nested commit: `9ad7239` or later.

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='0'; $env:PYTHONUTF8='1'; $R='scripts/run_p29_retention_gate.py'; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; foreach ($A in 'hinton','seqkd') { foreach ($V in 'arith0p5','wise0p5','arith1p0') { uv run python $R --phase merge --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V merge failed" }; uv run python $R --phase eval --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V eval failed" } } }; Write-Host 'GPU0 merges complete'
```

```powershell
$ErrorActionPreference='Stop'; $env:CUDA_VISIBLE_DEVICES='1'; $env:PYTHONUTF8='1'; $R='scripts/run_p29_retention_gate.py'; git pull --ff-only origin experiment/terminal-retention; if ($LASTEXITCODE -ne 0) { throw 'Pull failed' }; foreach ($A in 'fullgold','gold') { foreach ($V in 'arith0p5','wise0p5','arith1p0') { uv run python $R --phase merge --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V merge failed" }; uv run python $R --phase eval --arm $A --variant $V; if ($LASTEXITCODE -ne 0) { throw "$A $V eval failed" } } }; Write-Host 'GPU1 merges complete'
```

Hinton and full gold go first, because Hinton has the largest edge after K
(BIRD 36.70 versus 32.14).

Publication follow-up: `list_p29_publication.py` currently also requires the
paused retention/NLL evidence. A merge-only, fingerprint-checked allowlist
and its separate publication command are still needed; do not run paused
training just to satisfy that resolver. The existing compute lanes above
remain the A1 screen; do not claim merge evidence is published before that
publication path is ready.

If saved terminal client adapters are available, evaluate their BIRD
retention on a fixed diagnostic set before and after aggregation. This can
separate local adaptation from aggregation loss without retraining. Keep
public inputs on the server, publish no private examples, and label this as a
diagnostic; parameter-space aggregation error alone cannot explain EX loss.

### A2. Two-round interleaving (planned, not implemented)

A1 informs this experiment but is **not a pass/fail prerequisite**. Repeating
server distillation has precedents in
[FedCoLLM](https://arxiv.org/html/2411.11707v3) and
[FedDF](https://proceedings.neurips.cc/paper/2020/file/18df51b97ccd68128e994804f3eccc87-Paper.pdf).
Here the teacher stays frozen and all K computation stays on the server.

Start with two A rounds, matching the existing private budget:

```text
interleaved:        A -> k1 -> A -> k2     Hinton and full-gold CE
late public:        A -> A  -> K          Hinton and full-gold CE
historical anchor:  A -> K  -> A          existing Hinton and full-gold CE
private-only:       A -> A               existing FL control
```

**Budget and lineage contract.**

- Keep the same five clients, split, one local epoch per A, LoRA r16,
  aggregation, SQL-only format and evaluator. Two A rounds have the same
  private exposure and adapter exchanges as `A>K>A`. Three rounds would
  change both training and communication budgets, so are deferred.
- `k1 + k2` uses the same 9,428 BIRD rows/gold prefixes and one total public
  pass as K. Build one deterministic public batch stream, balance its two
  disjoint shards by database/SQL structure where feasible, and split at
  optimizer-step boundaries. The late-public K consumes the exact same ordered
  concatenation `k1 || k2`; neither schedule resamples the public rows.
  Fix padding, accumulation, loss normalization and truncation;
  verify visited-row hashes, target-token exposure and exact update counts.
  Reuse the fixed teacher-logit cache at the server only.
- Retain Hinton's 0.5 CE + 0.5 T-squared forward KL, T=2, versus full-gold CE.
  Both arms use identical public rows, ordering, stage boundaries and budgets.
  This is labeled-public KD, not an unlabeled-public setting.
- Use one planned public LR horizon and global K-step counter across k1/k2.
  Freeze an explicit server optimizer-state policy before execution. The
  `A>A>K` control must use the same policy at a virtual k1/k2 boundary, including
  any reset of optimizer moments. Record private-stage optimizer resets too.
  Historical runs remain anchors if their optimizer policy differs.
- `A>A` matches private budget only. Hinton and CE also have different teacher
  overhead. Report public updates/tokens, client/server time and offline cache
  cost separately; do not claim total-compute equality.

**Read two different contrasts.** Hinton minus gold within each schedule tests
the teacher; interleaved minus `A>A>K` within each objective tests the schedule.
An improvement over the historical `A>K>A` alone does not distinguish
interleaving from the effect of ending on K. Evaluate after the second A and
after k2; Spider retention after the final K is the main risk.

Use BIRD advantage with Spider-family noninferiority as the selection objective.
Before new runs, freeze the primary contrast, margins and validation-selection
rule. Use the A1 teacher/gold margins as the default screen; a schedule-benefit
claim additionally needs an improvement over matched `A>A>K` without material
Spider-family degradation. Report all five sets, paired uncertainty and per-seed
results. Final confirmation needs a validation split separate from the reported
evaluation and at least three matched seeds; any changed training split requires
rerunning the corresponding parents/controls. Merge is a separately reported
fallback if final K hurts Spider, not an unreported last-stage adjustment.

**Implementation required before activation:** shard/batch identities, resumable
K-stage counters and optimizer policy, the two-round runner, intermediate/final
evaluations, and a verified publication resolver with a separate publication
command. No executable A2 commands are provided yet. Re-estimate the GPU budget
for this two-round/four-new-arm design; the old three-round estimate does not
apply. Expand rounds or model families only after this screen gives useful
evidence.

## 3. Deferred alternatives

Spider-derived public data is not in the active queue. Same-dataset public data
can be a valid control, but it does not guarantee no forgetting. FedMKT's
[same-dataset split](https://arxiv.org/html/2406.02224v3#A4.SS2) uses supervised
public training; it is not evidence that our current gold-prefix KD is
unlabeled. Revisiting a Spider-public split would require new private baselines.
Client public replay remains excluded, regardless of the A1/A2 outcome.

Older finished runbooks: `paper/archive/completed_runbooks/` and
`paper/archive/superseded_runbooks/`. They are history, not the queue.
