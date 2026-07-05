# KD Full Plan — Two Directions × ICL, Staged Experiments

> Goal: build Fed + ICL + KD framework that maximizes EX on a *small* student
> (Qwen2.5-1.5B). Two distillation directions compared head-to-head **on the same KD
> data (BIRD)**, each crossed with ICL on/off, with a data-matched control so every
> delta is attributable to exactly one ingredient.
>
> Refs: KID **[10]** (arXiv:2410.11371) · Struct-SQL **[11]** (arXiv:2512.17053).
> Full system: `system_architecture.md` §5.6 / §5.6.1. Decision record: `DECISIONS.md`.
> **Rev 2026-07-06** — post-review fixes: (1) both KD directions on BIRD (kills the
> data confound), (2) `fedavg_bird` data control added, (3) demo-style parity locked
> (train style == eval style; style-shift = its own experiment), (4) teacher demos =
> BIRD always, (5) staged run order (probes → single-client bake-off → federate winner
> → seeds/ablations).

---

## 0. Locked rules (fixes from 2026-07-06 review)

1. **KD data = public BIRD train for EVERY KD direction** (KID, Struct-SQL, SeqKD).
   Teacher never runs on `Qᵢ`. Rationale = shared public distillation corpus →
   aligned client updates (less FedAvg drift) + cross-schema structural transfer.
   (NOT a privacy argument — teacher is on-premise, reading `Qᵢ` would leak nothing.)
2. **Control ladder** — every rung differs from the previous by ONE ingredient:

   | rung | Stream 2 (BIRD) content | isolates |
   |---|---|---|
   | `fedavg` | none | — (floor) |
   | `fedavg_bird` | CE on BIRD **gold** SQL | value of extra public data |
   | `fedkd_seqkd` | CE on **teacher** SQL | teacher-sequence value |
   | `fedkd_struct` | CE on teacher **QP-CoT ⊕ SQL** | structured-reasoning value |
   | `fedkd` (KID) | RKL on teacher **logits** over imperfect `ŷ` | logit-level / mismatch-correction value |

   `fedkd − fedavg_bird` = pure teacher value. `fedkd − fedavg` alone confounds
   teacher with extra data — never report it without the ladder.
3. **Demo-style parity**: within any arm, train demo style == eval demo style.
   Default = `never_schema` end-to-end. `skeleton` train+eval = paired
   privacy cell. Train-skeleton → eval-never_schema = **style-shift experiment**
   (E3.5), never a default.
4. **Teacher ICL demos = BIRD train only** (k=3, question-similarity, `never_schema`).
   Student KD-stream forward shares the exact same `P_ICL` context (invariant #9).
   Student FT-stream demos (when train-k=3) = own `Qᵢ` — same pool + style as its
   inference condition.
5. **λ₂ alpha-decay is GLOBAL**: 1.0 → 0 over cumulative steps across all rounds
   (`t = round·local_steps + step`), not restarted per round. Per-round restart =
   ablation only if convergence is unstable.
6. **Weighted FedAvg**: `θ_t ← θ_{t-1} + Σᵢ (nᵢ/n)·Δθᵢ` (McMahan), not 1/K —
   non-IID α=0.1 makes client sizes very unequal.
7. **BIRD-dev secondary eval caveat**: KD arms saw BIRD-train → on BIRD-dev compare
   KD arms against `fedavg_bird` (data-matched), not bare `fedavg`; state the
   exposure in the paper.

---

## 1. Two KD directions (both = Stream-2 variants on BIRD)

| | **Dir A — KID [10]** | **Dir B — Struct-SQL [11]** |
|---|---|---|
| Method axis | logit / distribution-level | data / sequence-level |
| Teacher emits | top-K logprobs over imperfect `ŷ_bird` | QP-CoT trace + SQL on BIRD train |
| Student loss | `RKL(q‖p)` on `ŷ_bird` (soft) | `CE` on `QP-CoT ⊕ SQL` (hard) |
| Teacher in loop | online, co-loaded per step | offline, generate once + cache |
| KD data | **BIRD train** | **BIRD train** (same — no confound) |
| Exec-filter | n/a (imperfect `ŷ` is the point) | ✓ on cached traces (BIRD DBs local) |
| Hardware | A100 (7B+1.5B co-load) | T4-friendly |
| Build cost | high (new: mask_rewrite, RKL, decay) | low (reuses trainer + CE path) |

Stream 1 (FT: gold CE on private `Qᵢ`) is identical for all arms. Only Stream 2 varies.
Composable later: QP-CoT⊕SQL as the sequence KID masks+rewrites (Stage 4, optional).

---

## 2. What exists vs what to build

| Component | File | State |
|---|---|---|
| Top-K soft-KL (forward) | `losses.py` `kl_div_loss` | ✅ |
| Weighted CE + skeleton weight | `losses.py` `weighted_lm_loss` | ✅ |
| LoRA trainer + KD config | `training/lora_trainer.py` | ✅ |
| Teacher generate (local HF) | `models/teacher_local.py` | ✅ |
| Train-time demo injection | `training/dataset.py` `build_examples(train_k=...)` | ✅ hook, off |
| Offline teacher-target pipeline | `data/teacher_targets.py` | ✅ exists — **repoint to BIRD** (was Qᵢ) |
| `--kd-direction {kid,struct,seqkd,none,gold}` flag | trainer + `run.py` | ❌ build (Phase 0) |
| BIRD loader + FAISS pool (BIRD train demos) | data/retrieval | ❌ build (Phase 0) |
| `build_teacher_prompt(..., demos=)` | `models/teacher_prompt.py` | ❌ build (Phase 0.5) |
| QP-CoT teacher template | `teacher_prompt.py` | ❌ build (Phase 1) |
| `mask_rewrite` + `rkl_div_loss` + global λ₂(t) | student / losses / trainer | ❌ build (Phase 2) |
| Weighted FedAvg (nᵢ/n) | aggregation script | ❌ small fix (Phase 0) |

⚠️ Phase-2 blocker: pin KID's exact mask-fill mechanics from [10] before coding —
causal LM has no `[MASK]`; confirm left-to-right teacher-forced fill vs iterative,
sampling temperature, and stop-grad through `ŷ` generation.

---

## 3. Build phases

### Phase 0 — scaffold (T4)

- `--kd-direction` flag; arms: `fedavg_bird` / `fedkd_seqkd` / `fedkd_struct` / `fedkd`.
- BIRD train loader + BIRD FAISS demo pool (question-only embedding, `never_schema`).
- Weighted FedAvg fix.

### Phase 0.5 — ICL wiring (T4)

- `build_teacher_prompt(question, schema, demos=None)` renders `P_ICL`.
- Teacher path retrieves k=3 from **BIRD** (never `Qᵢ`).
- Student `train_k` + `demo_style` exposed per arm; **style forced equal to the arm's
  eval style** (single CLI value drives both).

### Phase 1 — Dir B: Struct-SQL on BIRD (T4)

- QP-CoT template; generate + cache BIRD teacher traces (exec-filter kept).
- `dataset.py` targets `QP-CoT ⊕ SQL` for struct, teacher-SQL for seqkd, gold for
  `fedavg_bird`.

### Phase 2 — Dir A: KID on BIRD (A100)

- `mask_rewrite` (per [10] mechanics), `rkl_div_loss`, global-λ₂ decay, co-load.

### Phase 3+ — run the staged experiments below

---

## 4. Experiment list (staged — run in this order)

**Fixed everywhere:** student Qwen2.5-1.5B, teacher Qwen2.5-7B, Spider test = frozen
eval, `never_schema` unless the cell says otherwise, eval k == train k per arm,
ρ = KID-paper default until E3.2. Every run → RUNS.csv via `save_results`.

### Stage 0 — probes (T4, ~1 day, before any A100 spend)

| ID | run | question it answers | kill-switch |
|---|---|---|---|
| E0.1 | `probe_bird_sft`: student CE on ~1k BIRD gold → eval Spider | does BIRD training transfer to Spider at all? | Spider EX drops >2pp → rethink BIRD as KD data |
| E0.2 | `probe_vram_k3`: 1 short epoch, train-k=3, T4 | does +ICL Dir B fit T4? | OOM → Dir B +ICL moves to A100 |
| E0.3 | (code review, no run) pin KID mask-fill mechanics vs [10] | blocks Phase 2 | — |

### Stage 1 — KD direction bake-off (centralized data, NO federation)

**Rev 2026-07-06b:** run on **full centralized Spider train** (`processed_data/SPIDER/centralized/train.csv`),
not `client_1` — this slots directly into the gain chain already run/committed
(`central` FT → `central@k3` FT+ICL, via `experiments/centralized_ft/run.py` +
`experiments/eval_arms/run.py --pool-mode centralized`): the new KD arms extend that
SAME chain instead of opening a second, harder-to-compare federated-shard ladder.
`central`/`central@k3` adapters are **reused as-is** (no retrain) — only the KD arms
below are new training runs. Floor/control first, then directions, −ICL before +ICL.

| ID | arm | Stream 1 (FT) | Stream 2 (KD) | train/eval k | HW |
|---|---|---|---|---|---|
| — | `central` (existing) | centralized gold CE | none | 0/0 | reused |
| — | `central@k3` (existing) | centralized gold CE | none | 3/3 | reused |
| E1.2 | `central_bird` | centralized gold CE | BIRD gold CE | 0/0 | T4 |
| E1.3 | `central_seqkd` | centralized gold CE | teacher SQL CE | 0/0 | T4 |
| E1.4 | `central_struct` | centralized gold CE | QP-CoT⊕SQL CE | 0/0 | T4 |
| E1.5 | `central_kid` | centralized gold CE | RKL on `ŷ` | 0/0 | A100 |
| E1.6 | `central_struct +ICL` | centralized gold CE (train-k=3) | QP-CoT⊕SQL CE | 3/3 | T4 or A100 (per E0.2) |
| E1.7 | `central_kid +ICL` | centralized gold CE (train-k=3) | RKL on `ŷ` | 3/3 | A100 |

Gain chain read-off: `central_struct − central` = pure KD value (FT+KD vs FT alone);
`central_struct@k3 − central_struct` = ICL value on top of KD; `central_struct@k3 −
central@k3` = KD value under ICL; `central_struct@k3 − central` = total gain (headline).
`central_struct − central_bird` = teacher value, data-matched (same ladder logic as
before, renamed `central_bird` in place of `fedavg_bird` — no federation in this stage).

Federated variants of the same arms (`fedavg_bird`/`fedkd_*`) are Stage 2 (below), run
**after** a direction is picked here — not a substitute for this stage.

**Read-offs:** `central_bird − central` = data value · `central_seqkd − central_bird` =
teacher-sequence value · `central_struct − central_seqkd` = QP-CoT value ·
`central_kid − central_struct` = logit-level value ·
`central_struct@k3 − central_struct`, `central_kid@k3 − central_kid` = ICL synergy per direction ·
count `no such column` errors ±ICL = bleed check.

**Decision gate G1:** primary direction = best EX at its best ICL setting, and it
must beat `central_bird` — otherwise teacher adds nothing over free public
data → ship `central_bird`/`fedavg_bird` as the method and reframe. Lock ICL on/off per evidence.

### Stage 2 — federate the winner (K=3, T rounds)

| ID | arm | notes |
|---|---|---|
| E2.1 | `fedavg` | floor (reuse if already run) |
| E2.2 | `fedavg_bird` | federated data control |
| E2.3 | `fedkd` = winning direction, winning ICL setting | the method |
| E2.4 | `central` / `central@k3` | ceiling (reuse existing; @k3 re-run under parity: train-k == eval-k, same style) |

**Read-offs:** E2.3−E2.2 = teacher value in federation (headline RQ3) ·
E2.3−`local` mean = federation gain (RQ1) · E2.3 vs E2.4 = gap to ceiling (RQ1 bar).

### Stage 3 — headline + ablations (winner config only)

| ID | exp | scope |
|---|---|---|
| E3.1 | 3 seeds × {`fedavg`, `fedavg_bird`, `fedkd`, `central`} + significance test | headline table |
| E3.2 | ρ sweep {0.1, 0.2, 0.3, 0.4, 0.5} | KID only, 1 seed, centralized |
| E3.3 | `fedkd_teacher_k0` (teacher scores without ICL) | teacher-ICL value |
| E3.4 | demo-style privacy cell: train+eval `skeleton` (paired) vs paired `never_schema` | RQ2 privacy lever |
| E3.5 | style-shift: train `skeleton` → eval `never_schema` (and reverse) | robustness analysis — separate exp, never default |
| E3.6 | eval k-sweep {0,1,3,5} on final model | inverted-U check |
| E3.7 | bleed analysis: `no such column` counts across E3.1 arms ±ICL | mechanism evidence |
| E3.8 | BIRD-dev secondary eval, KD arms vs `fedavg_bird` | cross-dataset claim (exposure-fair) |
| E3.9 | DP curve: (ε, EX) at 2–3 noise levels | scoped claim: "DP-ready pipeline + ε–utility curve", no strong-ε promise at K=3 |

### Stage 4 — optional / stretch

- Compose B→A: QP-CoT⊕SQL as KID's mask+rewrite target.
- `slm_swap`, K∈{5,10} sweep — outside KD plan.

---

## 5. Risks

(a) QP-CoT may not help 1.5B ([11] used 4B) — E1.4 answers.
(b) +ICL prompt length OOMs T4 — E0.2 answers.
(c) 1.5B may not learn read-demos meta-skill — E1.6/E1.7 answer.
(d) BIRD→Spider transfer weak (dialect/evidence gap) — E0.1 answers *before* A100 spend.
(e) KID mask-fill under causal LM ill-defined — E0.3 blocks Phase 2 until pinned.
All decided by the matrix, not assumed.
