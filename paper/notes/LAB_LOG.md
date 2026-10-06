# FedLS-SQL — lab log

Newest first. Each entry says what ran, the key numbers, where the evidence
lives, and what was decided. All numbers are seed 0, EX (%), protocol v2.

Older detail:

- 2026-09-03 to 2026-09-26, full text:
  [`LAB_LOG_2026-09-03_to_2026-09-26.md`](../archive/lab_log_2026-09/LAB_LOG_2026-09-03_to_2026-09-26.md)
- Protocol v1 (no BIRD evidence):
  `paper/archive/protocol_v1_no_bird_evidence/LAB_LOG_v1.md`
- Before FedLS-SQL: `paper/archive/pre_fedls_2026-08/legacy_reports/LAB_LOG_through_2026-08-20.md`

## Where we are (2026-10-06, 0.5B implementation)

- Next: update the interrupted Coder-0.5B cohort to remove automatic counters,
  then resume the two lanes. The owner reports cache audit and probes passed;
  terminal results are not yet published. The frozen 7B teacher is unchanged.
- Method: not frozen. Best endpoint so far: `A>K[fkl]>A>K[fkl]>A` (Hinton with a
  second public stage), Spider 69.54, nested `bd4fdcb`, seed 0.
- Main objective: final Spider EX. A teacher method must beat full BIRD gold at
  the same chain and number of private passes, with SQL-only clients and
  inference.
- P2.17 (entry below): with two public stages, Hinton beats gold on all five
  sets at `A>K>A>K>A` (Spider +2.03, p = .033; DK +3.74, p = .002; BIRD +4.56,
  p < 1e-5). It passes the pre-registered +1 point rule. Seed 0 only.
- P2.16 FL recorded (`7e30ba9`): the public stage beats FL at 2-4 private
  passes. Centralized E1-E4 are not in the published manifest yet.
- Closed: the plan-task direction (P2.10, P2.14, `dss`, `goldplan`), A1 merge
  gate. Paused: P2.9.

## 2026-10-06: remove automatic shared-memory counters

- Owner report, not committed server evidence: prepare, cache audit and all
  three probes passed. FL later stopped at client progress 757/2377 because
  Get-Counter exited 1; this does not establish paging or a training failure.
- Per owner direction, remove all automatic counter polling and shared-memory
  gates, including warning-only monitors. The owner checks manually as needed.
  Recipes, allocator cap, reserved-VRAM probe budget and checkpoint paths stay
  unchanged. Child exit status remains authoritative.
- Nested `e15cc77` removes monitoring; `4b5eb8f` adds the checked one-time
  prepared/probe identity migration. Original identities and measurements are
  retained. Published to `fix/p218-remove-counter`, leaving remote `main`
  unchanged until the running cohort can safely update/publish.
- Validation: 720 CPU tests passed; reconstructed legacy identity matches
  `acbc641` across 142 tracked code files. No Windows GPU execution of this patch
  has been performed. Update and resume commands are in `PIPELINE_NEXT.md`.

## 2026-10-06: 0.5B runner, cache reuse audit and memory guard

- New P2.18 screen: FL AAA, continuous centralized E3, gold/Hinton AKAKA and
  AKKAA. KK means one public stage with two continuous epochs and epoch
  snapshots. Only initial A1 is shared; the public LR horizons differ.
- Preserve SQL-only P2.15/P2.17 recipes, `target_fp32`, batch 1/accumulation 16,
  fixed evaluation batch 16 and execution timeouts. No old student adapter
  initializes the fresh Coder-0.5B model.
- Cross-student cache reuse now requires full rendered-row and tensor audit,
  with runtime tokenizer/vocab/digest checks; original cache metadata stays
  unchanged. Local tokenizer mapping checks passed; the actual cache and BIRD
  databases are server-only, so full cache coverage is still unverified.
- Windows per-process paging guard and separate fresh GPU probes are implemented.
  Their acceptance thresholds are policy, not measured 0.5B memory figures.
- Code commits: nested `1ba8121` (runner), `12876b7` (cache/epoch wiring),
  `5109a0b` (paging guard), `acbc641` (Windows paths, runtime evidence and
  completed-stage recovery). Validation: 729 tests passed in 34.25 s using
  `UV_CACHE_DIR=/private/tmp/fedicl-uv-cache uv run --no-sync pytest -q`; CLI
  help/dry-run and `git diff --check` passed. All 9 PowerShell blocks pass
  structural checks; PowerShell/Windows execution was unavailable locally.
  Review findings were fixed with regression tests. No GPU result, performance
  gain or method advantage is claimed.

## 2026-10-05: implementation branches integrated into main

- Nested `main`: full-gold/interleaving history fast-forwarded; historical
  P2.9/P2.10 evidence merged (`343efed`), then cleanup merged (`dec9fc2`).
- Merge fixes preserve Hinton `target_fp32`, current runner imports,
  publication helpers, stage receipts, and historical identity values.
- Validation: 833 tests passed before cleanup; 688 passed after removal and
  archival of inactive paths, including two new Hinton integration tests.
  CPU checks only, no GPU run or server checkout change.
- The previous 1.5B queue is archived. New direction and preparation gates
  are in `PIPELINE_NEXT.md`; no smaller-student launch command exists yet.

## Evidence ledger — Spider private, BIRD public

`A` = one private round (5 clients, 1 local epoch, FedAvg). `K` = one public
server stage. Evaluation batch size 16. Exact paths and run IDs:
`RESULT_REGISTRY.md`.

| Trained artifact | Spider | Realistic | SYN | DK | BIRD | Result commit (nested) |
|---|---:|---:|---:|---:|---:|---|
| Teacher 7B, zero-shot | 76.69 | 71.06 | 63.83 | 62.43 | 47.07 | `e2ca26e`, `ec5b5e1` |
| Centralized E3 (Spider only) | 67.31 | 55.91 | 54.06 | 53.27 | 17.73 | `ec5b5e1` |
| Pure FL `A` (T1) | 57.35 | 54.92 | 49.32 | 45.23 | 14.80 | `ec5b5e1` |
| FL control `A>A` | 62.57 | 55.31 | 52.22 | 47.10 | 16.49 | `2a6e04c` |
| `A>K[fkl]` Hinton, 9,428 rows | 58.32 | 42.72 | 44.58 | 45.42 | 36.70 | `ec5b5e1` |
| `A>K[ce]` full gold, 9,428 rows | 55.03 | 47.05 | 43.91 | 40.93 | 32.14 | `5e4f005` |
| `A>K[fkl]>A` | 66.63 | 57.09 | 55.32 | 50.65 | 31.03 | `2a6e04c` |
| `A>K[ce]>A` full gold | 66.54 | 57.28 | 54.45 | 51.21 | 29.53 | `ccb3e91` |
| `A>K[seq]` SeqKD, 5,319 rows | 57.93 | 46.65 | 48.26 | 45.61 | 34.68 | `ec5b5e1`, `1e69ae3` |
| `A>K[ce]` selected gold, same 5,319 rows | 56.29 | 43.90 | 44.87 | 43.18 | 31.68 | `fb2329e` |
| `A>K[kid]` | 58.03 | 44.09 | 46.23 | 44.30 | 35.40 | `1e69ae3` |
| `A>K[seq]>A` | 64.99 | 57.68 | 54.55 | 50.28 | 28.42 | `1e69ae3` |
| `A>K[ce]>A` selected gold | 65.09 | 58.66 | 52.90 | 49.53 | 27.51 | `fb2329e` |
| `A>K[kid]>A` | 65.47 | 57.09 | 54.16 | 50.28 | 28.94 | `5d861f8` |
| `A>K3[ce]` P2.14 `seq`, 1,000 Struct-SQL rows, teacher SQL | 53.77 | 41.14 | 41.30 | 41.50 | 26.47 | `e622e1f` |
| `A>K3[seq+plan]` P2.14 `dss`, same rows + teacher plan task | 54.06 | 39.96 | 40.33 | 42.43 | 28.55 | `e622e1f` |
| `A>K3[ce]>A` P2.14 `seq` | 61.51 | 54.13 | 51.45 | 48.79 | 24.45 | `e622e1f` |
| `A>K3[seq+plan]>A` P2.14 `dss` | 63.35 | 56.30 | 50.97 | 48.97 | 24.05 | `e622e1f` |
| `A>K[ce]` P2.15 `gold`, 9,428 rows, `target_fp32` | 54.74 | 44.88 | 44.68 | 41.50 | 31.29 | `4e8aa80` |
| `A>K[seq+plan]` P2.15 `dss`, 4,109 Struct-SQL rows + plan task | 56.09 | 43.50 | 45.07 | 41.87 | 33.05 | `4e8aa80` |
| `A>K[ce]>A` P2.15 `gold` | 65.86 | 57.68 | 53.48 | 51.21 | 29.53 | `4e8aa80` |
| `A>K[seq+plan]>A` P2.15 `dss` | 64.89 | 56.89 | 52.71 | 50.09 | 25.62 | `4e8aa80` |
| `A>K[gold+plan]` P2.15 `goldplan`, gold SQL 9,428 rows + plan task 4,109 | 51.74 | 43.70 | 39.07 | 41.68 | 33.77 | `8bf615b` |
| `A>K[gold+plan]>A` P2.15 `goldplan` | 64.89 | 59.06 | 52.22 | 50.09 | 30.77 | `8bf615b` |
| `A>K[ce]>A>A` P2.15 `gold` | 67.89 | 60.83 | 56.38 | 50.84 | 30.05 | `4e8aa80` |
| `A>K[fkl]>A>A` Hinton | 67.60 | 56.89 | 55.61 | 52.90 | 30.90 | `4e8aa80` |
| `A>K[ce]>A>A>A` P2.15 `gold` | 68.09 | 58.46 | 55.32 | 53.08 | 29.20 | `4e8aa80` |
| `A>K[fkl]>A>A>A` Hinton | 67.79 | 59.06 | 55.03 | 53.46 | 31.81 | `4e8aa80` |
| FL control `A>A>A` | 64.22 | 57.28 | 52.32 | 47.85 | 17.60 | `7e30ba9` |
| FL control `A>A>A>A` | 64.80 | 56.30 | 52.03 | 50.09 | 17.67 | `7e30ba9` |
| `A>K[ce]>A>K[ce]` P2.17 gold | 58.03 | 50.00 | 46.62 | 43.74 | 33.57 | `bd4fdcb` |
| `A>K[fkl]>A>K[fkl]` P2.17 Hinton | 62.67 | 49.21 | 50.58 | 49.16 | 39.31 | `bd4fdcb` |
| `A>K[ce]>A>K[ce]>A` P2.17 gold | 67.50 | 58.07 | 55.42 | 50.65 | 31.62 | `bd4fdcb` |
| `A>K[fkl]>A>K[fkl]>A` P2.17 Hinton | **69.54** | 59.45 | 57.93 | 54.39 | 36.18 | `bd4fdcb` |
| `A>K[seq]>A[ret]`, λ = 1.0 | 61.61 | 50.79 | 49.90 | 46.92 | 30.31 | not committed (server) |
| `A>K[ce]>A[ret]` selected gold, λ = 1.0 | 60.74 | 50.20 | 49.42 | 45.79 | 28.88 | not committed (server) |

Reverse direction (BIRD private, Spider public), BIRD dev: pure FL 22.88,
selected gold 20.73, SeqKD 24.45 (`1b2c46a`).

BIRD-only baselines (BIRD private, no KD): base 15.97, centralized E1/E2
31.42/34.94, pure FL T1/T2/T3 22.75/28.36/31.10 (`e2ca26e`).

## What we have learned so far

1. The last private stage matters. `A>K[fkl]>A` beats `A>A` on all five sets
   (exact McNemar p = 0.000359/0.3557/0.00808/0.01834/<1e-40).
2. Hinton soft logits add nothing reliable after that stage. Against full-gold
   `A>K[ce]>A` the gap is +0.09/−0.19/+0.87/−0.56/+1.50 (p =
   1.000/1.000/.439/.749/.102).
3. KID ties SeqKD after the last stage and costs about 21.1 GPU-hours. Closed.
4. SeqKD beats selected gold at the public endpoint on all five sets. The last
   private stage removes most of the gap.
5. Keeping that gap with a retention loss (λ = 1.0) failed its gates.
6. The reverse direction agrees in sign: SeqKD beats FL, selected gold does
   not.

## 2026-10-04 - P2.17: a second public stage lets Hinton beat gold (seed 0)

- Run: nested `experiment/fullgold-plan`, code `7096718`, results `bd4fdcb`. A
  second K on the finished `A>K>A` rows, then one private round. Gold: P2.15
  recipe (`target_fp32`). Hinton: committed recipe and logit cache; the first K
  is the committed `full_bf16` row, the second K and every private round use
  `target_fp32` (fkl gained the target-window loss in `0af4455`).
- Five-set EX at `A>K>A>K>A` (three private passes):

| Set | gold | Hinton | Hinton - gold | p |
|---|---:|---:|---:|---:|
| Spider | 67.50 | 69.54 | +2.03 (55/34) | .033 |
| Realistic | 58.07 | 59.45 | +1.38 | .42 |
| SYN | 55.42 | 57.93 | +2.51 | .021 |
| DK | 50.65 | 54.39 | +3.74 | .002 |
| BIRD | 31.62 | 36.18 | +4.56 | < 1e-5 |

- Against the P2.15 chains with the same three private passes (`A>K>A>A`):
  Hinton interleaved vs Hinton +1.93 (p = .035), vs gold 67.89 +1.64 (p = .10).
  Gold gains nothing from the second K (-0.39, p = .75).
- After the second K (`A>K>A>K`, two passes): Hinton 62.67 vs gold 58.03
  (+4.64, p < 1e-4), both far below `A>K>A` (65.86/66.63). Ending on K is not
  useful; the private round after it is.
- Reading: the second K costs gold 7.8 Spider points and Hinton 4.0; the
  private round recovers both, and Hinton ends 2 points higher. This is the
  first chain where the teacher's edge survives the final private round. It
  reproduces the protocol-v1 number (69.54) under protocol v2, with evidence.
- Paired with the committed centralized Spider-only E3 (`ec5b5e1`, batch 16),
  Hinton `a3` minus E3: Spider +2.22 (96/73, p = .090), Realistic +3.54
  (p = .089), SYN +3.87 (p = .006), DK +1.12 (p = .61), BIRD +18.45. Gold `a3`
  minus E3: Spider +0.19 (p = .94). Gold stays at the centralized plateau;
  Hinton is above it on all five sets, not yet significant on Spider.
- Caveats: one seed, Spider p = .033; Hinton mixes loss modes across its two K
  stages (the gold chain does not). P2.16 E3/E4 are still missing.
- Resources: second K 20.3 GB for both arms (Hinton 3.3 h, gold 2.7 h); Hinton
  probe 19.8 GB. Recorded in `docs/A5000_RUN_CONFIG.md`.
- Decision: run a third K first (step 2, nested `eb6eaaf`), then replicate the
  better chain with more seeds.

## 2026-10-03 - P2.15 goldplan: the plan task does not help full gold (seed 0)

- Run: nested `experiment/fullgold-plan`, code `47aedc3`, results `8bf615b`.
  Gold SQL on all 9,428 rows plus the teacher plan task on the 4,109 admitted
  rows (Distilling Step-by-Step, labeled setting, weight 0.8).
- `goldplan - gold` at `A>K`: Spider -3.00 (p = .008), SYN -5.61 (p < 1e-4),
  BIRD +2.48 (p = .005). At `A>K>A`: Spider -0.97 (35/45, p = .31), Realistic
  +1.38, SYN -1.26, DK -1.12, BIRD +1.24 (p = .14); all p > .1.
- `goldplan - Hinton` at `A>K>A`: Spider -1.74 (p = .11), SYN -3.09 (p = .006).
- Reading: with the SQL rows held equal, the plan task costs Spider right after
  K and leaves nothing after the private round. The P2.14 gain (+1.84 over
  teacher-SQL `seq` on 1,000 rows) did not carry to full gold.
- Decision: close the plan-task direction; no depth rounds for `goldplan`.

## 2026-10-03 - P2.16 FL: the public stage beats FL at equal depth (seed 0)

- Run: nested `experiment/fullgold-plan`, code `9f9aa6b`, results `7e30ba9`.
  FL `A>A>A` and `A>A>A>A` grown from the committed `A>A` row with the P2.15
  private recipe (`target_fp32`). Centralized E1-E4 not finished.
- Spider EX by number of private Spider passes:

| Passes | FL | gold K | Hinton K |
|---:|---:|---:|---:|
| 2 | 62.57 | 65.86 | 66.63 |
| 3 | 64.22 | 67.89 | 67.60 |
| 4 | 64.80 | 68.09 | 67.79 |

- `gold - FL` Spider: +3.29 (p = .004), +3.68 (p = .0007), +3.29 (p = .003).
  `Hinton - FL`: +4.06, +3.38, +3.00 (p <= .011). BIRD: +11.5 to +14.5 at
  every depth (p < 1e-27). DK positive at every depth (p < .05).
- Reading: one BIRD public stage gives a stable offset of about 3.3 Spider
  points that neither grows nor fades over two more private passes. FL itself
  saturates near 65; the public-stage chains saturate near 68. The effect
  behaves like extra labeled data; on Spider the teacher's soft labels add
  nothing over gold at any depth, and keep about 1-2.6 more BIRD points.
- Claim this supports now: "a public server stage helps federated text-to-SQL
  at the same number of private passes". The centralized comparison waits for
  E1-E4.

## 2026-10-03 - P2.15: the plan task on full data does not beat gold (seed 0)

- Run: nested `experiment/fullgold-plan`, code `de57c27` (`dss`) and
  `b0d3808` (`gold`, depth), results `4e8aa80`. Teacher pool: 9,428 rows
  visited, parse 81.45%, 4,109 admitted (43.58%), 105 length-limited; longest
  `dss` example 7,579 tokens (max_len 8,448 for teacher arms). Depth rounds use
  `target_fp32`; Hinton depth grows from the committed `full_bf16` `A>K[fkl]>A`.
- Spider EX by endpoint (wins/losses, exact McNemar p in `summary.md`):

| Endpoint | gold | dss | Hinton |
|---|---:|---:|---:|
| `A>K` | 54.74 | 56.09 | 58.32 (old) |
| `A>K>A` | 65.86 | 64.89 | 66.63 |
| `A>K>A>A` | 67.89 | - | 67.60 |
| `A>K>A>A>A` | 68.09 | - | 67.79 |

- `dss - gold` at `A>K>A`: Spider −0.97 (51/61, p = .40), BIRD −3.91 (69/129,
  p = 2.4e-5). Right after K, `dss` led on BIRD (+1.76, p = .11) and Spider
  (+1.35, p = .34); the private round removed both and left BIRD below gold.
  BIRD execution errors at `A>K>A`: `dss` 44.1%, gold 35.6%.
- Loss-mode check: new gold (`target_fp32`) vs old full gold (`full_bf16`) at
  `A>K>A`: Spider −0.68 (11/18, p = .26), BIRD identical. Pairing with the
  committed Hinton row is fair.
- Gold vs Hinton: Spider −0.77/+0.29/+0.29 at the three depths (all p > .5).
  Hinton keeps BIRD better at every depth (−1.50, −0.85, −2.61; p = .006 at
  `A>K>A>A>A`). Gold `A>K>A` vs FL `A>A`: Spider +3.29 (83/49, p = .004).
- Reading: every arm that learns SQL on a subset (SeqKD 5,319, selected gold
  5,319, `dss` 4,109) lands near 65.0 at `A>K>A`; full gold lands at 65.9-66.5.
  The number of SQL rows decides, and the plan task recovers only a small part
  (roughly +0.5 by this comparison, against +1.84 over `seq` in P2.14). Spider
  saturates near 68 after three private passes for gold and Hinton alike,
  matching the centralized curve (62.19, 67.02, 67.60 in the legacy log).
- Decision: stop `dss` depth; run `goldplan`, which keeps gold SQL on all 9,428
  rows and adds only the teacher plan task (labeled setting of Distilling
  Step-by-Step). `goldplan - gold` isolates the plan. If it is near zero, close
  the plan-task direction. Missing controls for an equal-depth claim: protocol-v2
  FL `A>A>A`, `A>A>A>A` and centralized E1-E4 with epoch checkpoints.
- Resources: K reserved 20.3 GB (`gold`) and 20.4 GB (`dss`), RSS about 4.5 GB;
  private rounds 12.6 GB, about 1.6 h. Recorded in `docs/A5000_RUN_CONFIG.md`.

## 2026-10-02 - Amend P2.13 memory profile before GPU launch

- The owner confirmed preparation had finished and no GPU lane had started,
  then authorized the memory fix. Code commit `c38fb43` is on nested
  `experiment/fullgold-plan`, branched from `experiment/struct-aux-cot` at
  `3649595`; no cleanup/refactor branch is merged.
- All G/E/T K and terminal A stages now use target_fp32, retaining train batch
  1, accumulation 16, gradient checkpointing and max_len 7168/error. New
  p213_tfp32 roots preserve the earlier full_bf16 preparation. Fresh G is
  mandatory; historical fullgold/Hinton scores remain numerical references.
- Runner sets the Windows allocator and a 0.88 PyTorch CUDA memory fraction,
  with fixed eval batch 16 and no OOM halving. Preparation releases each arm's
  tokenized examples before constructing the next arm.
- Before each arm, isolated frozen longest-sequence/target/auxiliary probes
  run 32 microsteps and two AdamW updates, then enforce measured reserved
  memory <=21.5 GiB. Hash-bound compact reports retain process RSS. Probe
  adapters/targets remain server-side and do not feed the scientific runs.
- Motivation verified from existing artifacts: historical full-gold public K
  reserved 71,439.5 MB and process RSS 49,631.1 MB; recent private target_fp32
  stages reserved 7,912.6-10,003.4 MB and RSS 4,866.2-4,988.6 MB. Values use
  decimal MB. Private measurements do not prove this public-plan workload fits.
- Local verification: regression failures observed before implementation,
  795 full-suite tests passed, changed-file Ruff and CLI/dry-run passed.
  Review caught the need to probe with resident AdamW moments; corrected and
  reviewed again. Windows/A5000 live feasibility and EX remain unmeasured.
- Operational estimate, extrapolated from existing stage/eval timings:
  T about 6-8 hours, sequential G/E about 12-16 hours on the other GPU. It is
  not a paper resource measurement or a guaranteed runtime/RAM ceiling.

## 2026-10-02 - P2.14: the plan task helps Spider after FedAvg (seed 0)

- Run: nested `experiment/fullgold-plan`, code `5713ca8`, results `e622e1f`.
  1,000 Struct-SQL admitted rows, 3 public epochs, one SQL-only FedAvg round,
  five-set SQL-only evaluation at batch 16, seed 0.
- `dss - seq` (EX points, wins/losses, exact McNemar p):

| Endpoint | Spider | Realistic | SYN | DK | BIRD |
|---|---|---|---|---|---|
| after K | +0.29 (55/52, .85) | −1.18 (33/39, .56) | −0.97 (50/60, .39) | +0.93 (27/22, .57) | **+2.09** (97/65, .015) |
| after A | **+1.84** (46/27, .034) | +2.17 (26/15, .12) | −0.48 (40/45, .66) | +0.19 (15/14, 1.0) | −0.39 (56/62, .65) |

- Reading: right after K the plan task helps BIRD, the domain of the plans. After
  the private round the BIRD gain is gone (the usual pattern), but a Spider gain
  appears (+1.84; Spider-family mean +0.93). This is the first KD variant whose
  Spider edge grows after FedAvg instead of shrinking.
- Limits: one seed and ten contrasts (the Spider p = .034 does not survive a
  Bonferroni correction); `dss` makes twice the updates of `seq` (plan
  examples); both arms are weak in absolute terms (`seq` 61.51 is below FL
  `A>A` 62.57; Hinton and full gold reach about 66.6), because 1,000 rows over
  3 epochs pull the model further from Spider than the large pools.
- Resources: K reserved 20.2/20.4 GB, RSS 4.1 GB, 0.84-0.89 s/step; terminal A
  12.6 GB, about 1.6 h. Recorded in `docs/A5000_RUN_CONFIG.md`.

## 2026-10-02 - A1 merge gate fails; closed

- Training-free merges from the same FL T1 parent, evaluated SQL-only at batch
  16 on five sets: `wise0p5` (half the model after K, half the plain terminal)
  and task arithmetic `arith0p5`/`arith1p0` (FL `A>A` plus lambda times the K
  update). Source: server run output reported by the owner on 2026-10-02. The
  results are not committed; there is no result SHA, so they stay out of the
  paper.
- EX (Spider, Realistic, SYN, DK, BIRD); delta = teacher minus gold on the same
  merge (exact McNemar p):

| Merge | Teacher arm EX | Delta |
|---|---|---|
| SeqKD `wise0p5` | 63.64 / 52.76 / 51.45 / 49.72 / 33.25 | +1.84 (.07) / +1.38 (.4) / +1.16 (.31) / +1.87 (.17) / +1.37 (.16) |
| SeqKD `arith0p5` | 63.93 / 52.36 / 50.48 / 49.91 / 28.62 | +0.39 (.7) / +1.18 (.42) / +0.87 (.34) / +0.93 (.46) / +1.43 (.088) |
| SeqKD `arith1p0` | 57.54 / 43.11 / 46.23 / 45.05 / 34.42 | +2.03 (.089) / +1.38 (.51) / +2.80 (.019) / +1.50 (.4) / +1.96 (.057) |
| Hinton `wise0p5` | 63.15 / 52.95 / 51.84 / 50.84 / 36.57 | −0.77 (.5) / −1.97 (.22) / −0.58 (.62) / +1.87 (.13) / +4.43 (5.3e-6) |
| Hinton `arith0p5` | 62.38 / 50.20 / 48.16 / 48.97 / 31.03 | −0.39 (.74) / +0.00 (1) / −1.16 (.27) / +0.00 (1) / +2.80 (.00075) |
| Hinton `arith1p0` | 56.67 / 40.75 / 42.94 / 43.18 / 36.57 | +0.97 (.47) / −4.72 (.013) / −1.26 (.34) / +1.12 (.52) / +4.04 (.00011) |

- Gate (BIRD ≥ +1.5, Spider-family mean ≥ +1.0, no Spider-family set below
  −1.0, teacher Spider within 1.0 of its plain terminal): **no merge passes**.
  Closest is SeqKD `wise0p5` (BIRD +1.37, Spider −1.35 below 64.99).
- Every merge lowers Spider below the plain terminal (66.63 Hinton, 64.99
  SeqKD). The teacher's Spider-family edge appears only together with that
  Spider loss; Hinton keeps a strong BIRD edge but no Spider-family edge.
- Decision: A1 closed, no merge enters the method.

## 2026-10-02 - Replace P2.13 with the P2.14 plan-task screen (no GPU run)

- P2.13 stopped in its first memory probe: `torch.cuda.set_per_process_memory_fraction`
  rejects an unindexed `cuda` device (fixed in nested `722f6e8`). No training ran.
- Design review: P2.13 gave the plan task about 5% of the K gradient (1,000 of
  9,428 rows, weight 0.5, batch 1 with per-example token-mean loss) and paired
  teacher plans with gold SQL. Neither Struct-SQL nor Distilling Step-by-Step
  does this. Struct-SQL trains the teacher SQL of admitted rows; Distilling
  Step-by-Step gives every training row a rationale from the same teacher.
- P2.14 follows both on the existing 1,000 admitted rows: `seq` (teacher SQL)
  versus `dss` (teacher SQL plus teacher plan as a separate task, weight 0.8 as
  in PARSQL), 3 public epochs, one SQL-only FedAvg round, five-set evaluation.
- Nested commits: `91c4a5a` (multi-epoch auxiliary stages), `4de1025` (shared
  memory probe and allowlist; also removes a public-stage flag the CLI rejects,
  which would have stopped the P2.13 smoke), `5713ca8` (P2.14 runner). 807 tests
  pass; every P2.13/P2.14 stage command parses through the real CLI.

## 2026-10-02 - Fix missing P2.10 inputs in P2.13 bootstrap

- Server preparation failed before training: P2.13 branched before the P2.10
  artifact commit `9c3476e`, so the assumed plan files were missing.
- Fix `165a20e` adds a separate five-file restore from that pinned Git snapshot.
  Git normalized CSV record terminators; restoring the original CSV encoding
  reproduces its provenance hash exactly. All payloads are checked before
  writes; existing mismatched files are preserved and rejected.
- Verified the actual snapshot in a temporary directory: 1,000 original-gold
  joins, 1,000 sidecar records, 50 stratified sample IDs. Full pytest: 781 passed,
  including three regressions observed failing before implementation.
- Bootstrap and recovery commands updated. No GPU run, new target generation,
  EX result, or Windows-runtime validation. This fixes artifact provisioning;
  full server preparation still validates the local raw databases and parent.

## 2026-10-02 - Deliver P2.13 two-GPU runner (no GPU run)

- Code lives on nested branch `experiment/fullgold-plan`, implementation
  `b7706f8af783d7fad663d2747a406435691151c6`. GPU 0 runs T; GPU 1 runs G then E. Each arm
  bundles its own smoke, K, five-set eval, terminal A, and five-set eval.
- E uses original gold SQL on the plan IDs; T adds plan targets separately.
  Both keep the 9,428 gold base and weight-0.5 auxiliary slots. Private A and
  inference remain SQL-only. No new teacher generation is required.
- Intermediate stage receipts avoid Git mutation during concurrent jobs.
  Manifest locks, immutable inputs/code identity and per-lane locks protect
  resume; publication resolves only complete compact evidence after both lanes.
- Local full pytest: 778 passed. New regression tests were observed
  failing before implementation. CLI help/dry-run and changed-file checks pass.
  Review fixes cover missing completion metadata after a crash and ensuring
  public smokes actually include an auxiliary example.
- No server data/adapter validation, semantic target review, Windows execution,
  GPU training or EX measurement occurred locally. Timings from concurrent
  lanes are operational and cannot establish exclusive-hardware resource cost.

## 2026-10-02 - Select the full-gold auxiliary-plan screen (no GPU run)

- Chose P2.13 to answer the owner's direct full-gold comparison. It adds an
  auxiliary teacher-plan task on public data while preserving SQL-only
  private stages and inference. The current P2.11 runner uses a different,
  smaller teacher-SQL base; its artifacts and defaults are not repurposed.
- Require the same-row extra-SQL control immediately, so a gain over plain
  gold is not automatically credited to reasoning supervision. Data/weight,
  schedule, evaluation, and confirmation rules are owned by the active queue.
- Preserved the complete prior queue and commands in the
  [dated archive](../archive/completed_runbooks/PIPELINE_PRE_FULLGOLD_PLAN_2026-10-02.md).
  Removed competing launch paths from the current queue and aligned method/RQ
  statuses. This was a documentation decision: no new training result, code
  implementation, target generation, or live server-status check.

## 2026-10-02 - Research objective and continuation hypotheses (no GPU run)

- Subsequent owner clarification prioritizes a stronger teacher-CoT method
  over full BIRD-gold/Hinton at fixed `A>K>A`. Depth experiments are secondary.
  Added paper-grounded auxiliary-task and local STaR-SQL-style options, with
  explicit separation of existing runners, proposed variants, and unproven
  transfer to 1.5B federated Spider. No GPU run or code change followed.
- Owner clarified that the paper should establish useful public KD for
  federated Spider EX. CoT and a fixed `A>K>A>A>A` schedule are not requirements.
- The private MedQA example is an informal motivation only. No paper/repo was
  provided or audited; no result from it is treated as evidence for this task.
- Added A3: study consolidation depth after one public stage with matched FL
  and gold trajectories. Depth and stopping rule remain to be frozen; no new
  command, code, result, or GPU run was activated.
- Clarified the pipeline-versus-teacher claim ladder and centralized-reference
  limits. A gold tie restricts attribution without erasing a pipeline gain.
- Corrected P2.11 exposure-control wording and P2.12's unsupported claim that
  masking plan CE guarantees preserving plan generation. Kept the original
  A1 gate as a historical diagnostic alongside the new Spider-first objective.

## 2026-09-26 — P2.9 retention at λ = 1.0 fails; P2.9 paused

- Ran: `ret` for both arms, predictions read on the server (not committed).
- SeqKD − gold after `ret`: +0.87/+0.59/+0.48/+1.12/+1.43 (exact McNemar p
  .368/.78/.696/.362/.117).
- Gates: BIRD ≥ 1.5 fails. Spider-family mean (+0.77) ≥ 1.0 fails. No set
  below −1.0 passes. SeqKD Spider cost (−3.38) ≤ 1.0 fails.
- Retention buys +1.9 BIRD for −3.4 to −6.9 on every Spider-family set. It is
  dominated by a straight line between the public and plain-terminal points.
- Reading: the teacher edge shrinks as the model moves back to Spider
  (Spider-family mean +2.55 public, +0.77 `ret`, +0.33 terminal). The SQL-only
  edge looks like a gentler update, not extra knowledge.
- Decision: pause P2.9 and run P2.10 with a plain terminal stage. The
  target-NLL script was fixed first (nested `f210071`, `d8b4d5f`).

## 2026-09-25 — P2.9 variants added (no GPU run)

- Nested `78a34bd`: λ = 0.1 retention variant and WiSE-FT (exact LoRA
  midpoint). Reason: λ = 1.0 is 10× FedGKD's NLP weight.
- Nested `419a878`: D1 task arithmetic, `A>A + λ·(A>K − A)` with λ = 0.5 and
  1.0. It tells whether the KD update adds on top of FL. Tests: 690 pass.
- Literature check (LwF, FedGKD, FedNTD, WiSE-FT) is in
  `paper/archive/method_reviews_2026-09/KD_METHOD_REVIEW.md` §10–11.

## 2026-09-24 — Struct-SQL lineage implemented (P2.10, no GPU run)

- The P2.7/P2.8 plan format was not the paper's QP-CoT, and private stages
  were SQL-only. Nested `d66af7a` adds the real Struct-SQL lineage: format
  `qp_cot_v1`, private template `qp_ast_v1`, 75/25 ID/OOD split, 150+150
  validation rows, early stopping, stages `A[qp]`, `K[qp-ast]`,
  `K[qp-teacher]`, and a four-arm runner. Tests: 684 pass.
- CPU audits: template works on all 20,655 Spider/BIRD rows. Median target is
  247 tokens (Spider) and 297 (BIRD). BIRD has only 261 subquery-only rows, so
  that quota falls short; the shortfall is recorded.
- Deliberate differences from the paper: LoRA r = 16, zero-shot teacher, and
  our own validation cadence.

## 2026-09-24 — P2.6 public edge re-analyzed (CPU only)

SeqKD minus selected gold on the same 5,319 rows (committed batch-16
predictions from `fb2329e`), exact McNemar p in brackets:

| Endpoint | Spider | Realistic | SYN | DK | BIRD |
|---|---:|---:|---:|---:|---:|
| public `A>K` | +1.64 (.20) | +2.76 (.19) | +3.38 (.006) | +2.43 (.14) | +3.00 (.004) |
| terminal `A>K>A` | −0.10 (1.0) | −0.98 (.57) | +1.64 (.07) | +0.75 (.63) | +0.91 (.25) |

- At the public endpoint SeqKD also has fewer non-executable predictions on
  every set (for example Spider 19.5% → 14.1%).
- Decision: test whether a retention loss keeps the edge (P2.9, nested
  `e72ad2d`). P2.8 was archived unrun.

## Before 2026-09-24 (one line each)

Full text is in the archived log.

- 2026-09-23: P2.7 hardening (teacher journal, token counts). No new EX.
- 2026-09-22: P2.6 published (`fb2329e`). Terminal SeqKD − selected gold
  misses the promotion gate.
- 2026-09-20: P2.5 published. KID ties SeqKD; KID closed.
- 2026-09-17: GKD stopped for cost; partial artifacts are not evidence.
- 2026-09-16: P2.4a (`ccb3e91`): Hinton does not beat full-gold CE after
  terminal A. P2.3 (`2a6e04c`): `A>K>A` beats `A>A`.
- 2026-09-15: P2.2 published (`5e4f005`, `1b2c46a`, `ec5b5e1`). Stage chains
  (`run.py stage`) added (nested `810d8c4`, hardened to `014b118`).
- 2026-09-14: Hinton T1 learns BIRD but loses Spider robustness.
- 2026-09-11: teacher pools and BIRD baselines published (`e2ca26e`). Hinton
  forward KL replaces reverse KL as the soft-logit baseline.
- 2026-09-10: BIRD scorer set to the official 30-second pair timeout
  (`2178d5a`, `bird_official_set_pair_timeout30_v2`).
- 2026-09-06: P2.1 BIRD checkpoints rejected (974 truncated prompts). New
  7,168-token contract (`d21f777`).
- 2026-09-03: protocol reset. BIRD evidence had been left out of every prompt
  in protocol v1.
