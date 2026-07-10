# FedICL-SQL — Lab Log

> One entry per working session. Auto-header from `analysis/log_session.py`, manual body.
> Compare all runs: `uv run python analysis/compare.py`

---

## Session 2026-06-29 — architecture pivot to KID + lock decisions

### What changed

**Architecture pivot:** KD mechanism replaced with KID (Learning from Imperfect Data, EMNLP Findings 2024). Primary driver: KID teacher runs forward-only per step (not autoregressive offline) → ~100× cheaper than old offline annotation.

**KD mechanism (new):**
- Teacher: Qwen2.5-7B frozen, co-loaded with student, online per training step
- Per step: student masks gold SQL (ratio `ρ`, Hard strategy) → rewrite → `ŷ` → teacher forward with ICL k=3 from `Qᵢ` → soft labels `p` → `L = λ(t)·MLE + (1-λ(t))·RKL(q‖p)`
- Alpha-decay `λ(t)`: 1.0 → 0 over training
- Reverse KL (mode-seeking, SQL-compatible)
- No offline annotation, no exec-filter, no L_struct, no CoT

**ICL:** follows DAIL-SQL [9] — question-similarity retrieval, never_schema demos, k=3 inference, k=0 training.

**Datasets locked:**
- Primary: Spider
- Secondary: BIRD *(locked)*

**Ablations locked:**
- `fedkd_teacher_k3` (default) vs `fedkd_teacher_k0` — value of ICL-enhanced teacher labels
- `fedkd@k3` vs `fedkd` — value of ICL at inference

**VRAM:** teacher (14 GB) + student (3 GB) co-loaded → A100 required. T4 PoC: 4-bit teacher.

### Files updated
- `system_architecture.md` — §5.2, §5.6, §6, §8, §9, §10, arm table, eval datasets
- `DECISIONS.md` — §2 notation, §3 decisions #1, #4, #5, #6
- `fig1_architecture.md` — three-plane, teacher, training loss, caption, innovations, outline mapping

### Next
- Implement KID training loop (`lora_trainer.py`): mask+rewrite pipeline + online teacher forward + RKL + alpha-decay
- Run `local` ×3 + `fedavg` ×3 (gold CE only, no teacher) → establish federation baseline
- Run `fedkd_teacher_k3` ×3 → full method
- Eval all arms on Spider + BIRD

---

## Session 2026-06-23 — naming refactor + retire detailed_plan

### What changed
Killed the A/B/Ab letter labels and the `detailed_plan.md` mega-doc. Arms now
named by **feature**, not letter. No pre-planned full roadmap — work is decided
per session and logged here.

**Naming map (old → new):**

| old | new | what it is |
|---|---|---|
| B0 / `base` | `base` | untrained SLM floor |
| B2 / `slm_only` | `local` | per-client solo LoRA (no fed, no teacher) |
| B3 / `centralized_ft` / `b3_k0` / `b3_k3` | `central` | pool-all centralized ceiling |
| B4 / Centralized-ICL | `central@k3` | central + ICL eval overlay |
| Ab3 / B6 / `ab3_fedavg` | `fedavg` | FedAvg, no teacher KD |
| M_G / `m_g` | `fedkd` | full method (FedAvg + teacher KD) |
| B1 | `teacher` | LLM teacher few-shot ceiling |

ICL = eval overlay (`@k3` suffix), not an arm. `M_G` kept **only** as the Fig.1
math symbol for the global SLM (notation, not an arm label).

**Scope = going-forward only.** Historical `RUNS.csv` rows + Drive result dirs keep
their old slugs; `compare.py` maps both old and new slugs to the same identity so
the scoreboard still renders. New runs emit new names.

### Files touched
- **new** `DECISIONS.md` — slim decision + notation record (migrated `detailed_plan` §0 notation + §8 locked decisions + the naming map). **`detailed_plan.md` deleted.**
- `compare.py` — `IDENTITY`/`LABEL` → feature names, legacy slugs still map; widened columns. Verified renders clean on existing RUNS.csv.
- `eval_arms/run.py`, `centralized_ft/run.py`, `client_train/run.py`, `dataset.py`, `lora_trainer.py`, `pool.py`, `retriever.py`, `icl_diff.py`, `icl_ab_local.py` — docstrings/comments → feature names.
- `notebooks/00_colab_bootstrap.ipynb` — all arm slugs + dir paths renamed (`m_g_round`→`fedkd_round`, etc.); JSON re-validated.
- Root `CLAUDE.MD`, `fedicl-sql/CLAUDE.md`, `README.md`, `system_architecture.md` — repointed `detailed_plan` → `DECISIONS.md`, arm-naming tables + delta language → feature names.

### Next
- Unchanged from below: train `local` ×3 + `fedavg` ×3 → CUDA; gen teacher targets; train `fedkd`; eval all arms (`fedkd − local`, `fedkd − fedavg`).

---

## Session 2026-06-18 — ICL demo-pool leakage fix

### Problem found
`eval_arms` built the ICL retrieval pool from the **test set itself** (`held_out`/`test.csv`), retrieving demos via leave-one-out within the same DB. Spider dev has many near-duplicate questions per DB → LOO handed the model a near-answer template → inflated EX. All prior k=3 ICL runs purged (leaky, non-citable).

### Design (confirmed w/ advisor intent)
Each client = org with own schema + train data `Qᵢ`. ICL demo pool = the model's **own train data**, never the test set. Verified disjointness: train 146 DBs ∩ test 20 DBs = **0**; every `client_i` pool ∩ test = 0. So retrieval is **cross-schema** (train demos → unseen test query) and needs **no LOO**. This *is* the RQ2 mechanism (general SQL-skeleton transfer, not schema-specific answers).

Decision (user): global federated arms (`M_G`, `ab3_fedavg`) evaluated **per client pool → mean±std** over K (privacy end-to-end + free per-client variance). `M_G−B3` gap = federation cost + private-pool restriction.

### Refactor (code)
- **new** `fedicl_sql/retrieval/pool.py` — `client_pools(split_dir, K)` + `centralized_pool(train_csv)`.
- `eval_arms/run.py` — rewritten: drop `_retrieve_loo` + per-DB test index. `--pool-mode per_client` (default) = per-client pools, `{i}` placeholder adapter, mean±std + per-pool breakdown; `--pool-mode centralized` = one centralized pool, single number (B3/B4). Single ICL-eval entrypoint.
- `centralized_ft/run.py` — unchanged (B3 = k=0). B4 Centralized-ICL = `eval_arms --pool-mode centralized --k 3` on the existing B3 adapter (no retrain).
- `notebooks/00_colab_bootstrap.ipynb` — §3b/§5a-3/§5b-2 eval cells updated to the new `--pool-mode`/`--split-dir` interface.
- **tests** +3 (`test_pool.py`): pool wiring + `pool ∩ test = ∅` invariant. **85 passed.**

### New runs (train-pool retriever, no leakage)

| experiment | arm   | k | pool              | EX         | EM     | n_eval | device | run_id                           |
|------------|-------|---|-------------------|------------|--------|--------|--------|----------------------------------|
| eval_arms  | b3_k3 | 3 | centralized train | **52.61%** | 37.14% | 1034   | cuda   | `eval_arms__s0__20260618T123344` |

### Key finding 🔴

B3+ICL k=3 (cross-schema, centralized train pool) = **52.61%** — **−9.1% vs B3 k=0 (61.7%)**. Cross-schema ICL hurts significantly. Prior 70.6% result was from leaky test-pool LOO → now invalidated and purged.

**Scoreboard (clean, train-pool only):**

```
B0  base Qwen-1.5B    k=0   EX=51.2%   EM=14.1%   (no training)
B3  centralized FT    k=0   EX=61.7%   EM=42.5%   (+10.5% from LoRA SFT)
B3  centralized FT    k=3   EX=52.61%  EM=37.14%  (−9.1% from cross-schema ICL 🔴)
```

**Implications for RQ2:** cross-schema ICL with train-pool demos actively hurts the centralized model. Per [4]: masked cross-schema ICL also costs EX. This means if M_G shows the same pattern, the paper's ICL contribution is at risk — title claims "In-Context Learning" but ICL hurts. Must surface at SB gate. Possible reframe: ICL as privacy/transfer lever, not accuracy lever (frame per §2.3 + [4]).

**However:** B3 is centralized and already sees all 8659 train examples (= strong baseline). M_G is federated with per-client ICL from smaller Qᵢ pools. The relative ICL contribution for M_G may differ. Confirm once M_G is trained.

### Next

- Proceed to step 4 (B2 solo LoRA ×3) + Ab3 (FedAvg no-KD) → CUDA.
- After M_G trained: re-run ICL eval with `--pool-mode per_client` to check whether M_G+ICL recovers or also loses vs k=0.
- B0/B3 k=0 numbers (51.2% / 61.7%) unaffected — clean, still valid.

---

## Session 2026-06-17

### New runs
| experiment | k | EX | EM | loss | n_eval | device | run_id |
|---|---|---|---|---|---|---|---|
| eval_base_floor | 0 | **51.2%** | 14.1% | — | 1034 | cuda | `eval_base_floor__s0__20260617T055325` |
| centralized_ft | 0 | **61.7%** | 42.5% | 0.0554 | 1034 | cuda | `centralized_ft__s0__20260617T073618` |

### Scoreboard

```
B0  base Qwen-1.5B    k=0   EX=51.2%   EM=14.1%   (no training)
B3  centralized FT    k=0   EX=61.7%   EM=42.5%   (+10.5% from LoRA SFT)
```

(k=3 ICL numbers pending — see 2026-06-18 demo-pool fix; must re-run with train-pool retriever.)

### Observations
- `_extract_sql()` fix likely accounts for ~5-8% of B0 improvement vs old 40.5% (old code failed when model output reasoning prefix)
- ToChar / DATEDIFF warnings = sqlglot EM scoring, does not affect EX
- Training speed: 0.49s/step on T4 → 8659 steps ≈ 70 min + 22 min eval
- Smoke run detection: `compare.py` now auto-filters n_eval < 50

### Decisions
- CUDA stack, alpha_0.1/k3, full 1034 test.csv = fixed baseline for all future runs
- log_session.py filters n_eval < 50 (smoke runs)

### Next
- [x] §2.5 B0 base floor
- [x] §3 B3 centralized ceiling
- [ ] §5a-1 `slm_only` ×3 — B2 floor, per-client solo LoRA (~72 min total)
- [ ] §5a-2 `ab3_fedavg` ×3 — Ab3, FedAvg no KD (~72 min)
- [ ] §5a-3 eval federation gain + ICL (ab3_fedavg − slm_only)
- [ ] §4b `gen_teacher_targets` ×3 — annotate Qᵢ, 7B 4-bit (~13 hr client_1)
- [ ] §5b-1 `m_g` ×3 — full method teacher-KD FedAvg (~72 min)
- [ ] §5b-2 eval all arms (m_g − slm_only, m_g − ab3_fedavg)

---

---

## 2026-06-30 — RQ2 reframed to Fed+ICL+KD synergy; +ref [10] KID

**Error analysis (k0 vs k3 flips, dail_select):**
- BASE (chưa FT): 49.0%→52.5% (+36 net; gain 137 / hurt 101). GAIN = structure fixes (over-join, alias, ORDER BY LIMIT); HURT = JOIN-heavy.
- CENTRAL (FT): 63.1%→60.2% (−30 net; gain 79 / hurt 109). **54/109 hurts = `no such column` exec errors = schema bleed** (student copies demo's table/col names from a different DB).
- Mechanism: ICL has 2 channels — *structure-transfer* (gain, schema-agnostic) + *schema-bleed* (hurt). FT saturates the gain channel (already knows structure) but not the bleed channel → net negative. = train/test MISMATCH (train k=0, eval k=3), NOT an ICL ceiling.

**Decision — RETIRE "never claim ICL improves FT" framing.** Goal restated: build Fed+ICL+KD → max EX on small model; target `(FT/KD)+ICL > either`. Path = **in-context tuning** (`train-k=3` + `skeleton` demos) so student learns to read demos + anti-bleed prior. Grounded in KID [10] (train/inference mismatch). Updated `system_architecture.md` (top note + §5.3 RQ2 + §5.6 FT stream + ICL-positions table + per-arm table) and `DECISIONS.md` ref list.

**Added reference [10]** = KID (Zhong et al. 2024, arXiv:2410.11371) — source of the adopted KD mechanism. PDF+MD in `paper/references/`.

### Next
- [ ] Verify `--train-k 3` + train-time `demo_style=skeleton` are wired in trainer + eval run.py
- [ ] Run synergy arm: `central` train-k=3 skeleton, eval k=3 skeleton (A100) vs `central` k0 vs `base@k3`. Count bleed-error drop (expect 54→low).
- [ ] If synergy confirmed → promote to RQ2 headline; else report honest k=0.

### 2026-06-30 addendum — 2 KD directions locked + ref [11]
- KD now has **two directions** benchmarked head-to-head (`system_architecture.md` §5.6.1):
  - **Dir A — KID [10]** (logit-level, RKL on imperfect ŷ, A100 co-load) = primary.
  - **Dir B — Struct-SQL [11]** (data/seq-level, SFT on QP-CoT⊕SQL, teacher offline → T4-friendly) = contender/fallback; subsumes skeleton-structure loss; composable with KID.
- Reason for B: not certain KID wins → need a proven NL2SQL-specific method on a different axis. Arms: `fedkd` (KID) / `fedkd_struct` (Struct-SQL) / `fedkd_seqkd` (optional classic).
- Also locked: KD-stream teacher+student now share `P_ICL` context (fixed latent k3-vs-k0 inconsistency); invariant #9 "train condition == inference condition" added.
- Added **reference [11]** = Struct-SQL (arXiv:2512.17053). PDF+MD in `paper/references/`.
- Next: verify QP-CoT fits 1.5B + T4 VRAM; run Dir A vs Dir B vs base@k3 on A100.

- KD impl plan → `paper/notes/KD_PLAN.md` (2 directions × ICL on/off matrix; Phase 0.5 = wire ICL into KD path first).

---

## 2026-07-06 — KD architecture review → 6 fixes locked; KD_PLAN rewritten with staged experiment list

**Review found 4 serious flaws in the KD design docs; all fixed today:**

1. **`kid − struct` was confounded** — KID distilled on BIRD, Struct-SQL traces were to be generated on `Qᵢ` (old offline pipeline) → the comparison differed on loss level AND data AND teacher mode at once. **Fix: both directions now distill on BIRD train** (Struct-SQL traces generated offline on BIRD, cached, exec-filtered).
2. **`fedkd − fedavg` confounded teacher with extra public data** (KD arms see Qᵢ+BIRD, fedavg sees Qᵢ only). **Fix: new `fedavg_bird` control** (CE on BIRD gold, no teacher) → control ladder `fedavg → fedavg_bird → seqkd → struct → kid`, each rung isolates one ingredient. Teacher value = `fedkd − fedavg_bird`. Same control used for exposure-fair BIRD-dev secondary eval.
3. **Demo-style mismatch baked in** — plan had train `skeleton` + eval `never_schema` (same class of train/test mismatch as the −30-flip bug). **Fix: style parity locked** — train style == eval style per arm; default `never_schema` end-to-end; paired `skeleton` = privacy cell (E3.4); style-shift = its own experiment (E3.5). Invariant #9 gains level (c).
4. **Doc self-contradictions** — §2 diagram still showed old offline-teacher-on-Qᵢ + 4-term loss; ablation table said teacher ICL "from Qᵢ" (violated invariant #2); `skeleton` vs `never_schema` inconsistent in pseudocode. All patched to match §5.2/§5.6.

**Also pinned:** FedAvg weighted `nᵢ/n` (McMahan, was 1/K) + LoRA A/B-averaging caveat; λ₂ alpha-decay = GLOBAL over cumulative steps across rounds; privacy reframed (BIRD = update-alignment rationale, not "privacy absolute" — teacher is on-premise); DP claim scoped to "(ε, EX) curve" at K=3, no strong-ε promise; new invariant #10 (KD data = BIRD for all directions + data-matched comparisons).

**KD_PLAN.md rewritten** — full staged experiment list:
- Stage 0 probes: E0.1 BIRD→Spider transfer probe (1k gold SFT, kill-switch before A100 spend) · E0.2 train-k=3 T4 VRAM probe · E0.3 pin KID mask-fill mechanics vs [10] (causal LM has no `[MASK]` — blocks Phase 2).
- Stage 1 direction bake-off on client_1 only (no FedAvg, ⅓ cost): local_1 / local_bird_1 / seqkd / struct±ICL / kid±ICL → gate G1: winner must beat `local_bird_1` else teacher adds nothing → ship `fedavg_bird` as method.
- Stage 2 federate winner: fedavg / fedavg_bird / fedkd(winner) / central.
- Stage 3 headline: 3 seeds + significance · ρ sweep (KID, 1 seed) · teacher-k0 · skeleton privacy cell · style-shift · k-sweep · bleed analysis · BIRD-dev · DP curve.

Updated: `KD_PLAN.md` (rewrite) · `system_architecture.md` (header note, §2 diagram, §3.1, §5.2, §5.3, §5.6, §5.6.1, §6, invariants #2/#9/#10, §10) · `DECISIONS.md` (§1 dec.1/4/6 amended, dec.8 added, λ notation).

### Next
- [ ] Phase 0 scaffold: `--kd-direction` flag, BIRD loader + FAISS pool, weighted-FedAvg fix
- [ ] E0.1 + E0.2 probes (T4) before any A100 booking
- [ ] E0.3: read KID [10] §method, pin mask-fill mechanics (left-to-right teacher-forced? sampling temp? stop-grad through ŷ)

---

## Session 2026-07-07 — BIRD dropped, KD scope cut to a PoC

### What changed

**BIRD dropped entirely** — too heavy (8.9 GB DB download) and too complex
(`evidence`-field dependence, dialect gap vs Spider) to justify as the KD stream, and
dropped as secondary eval benchmark too (no cross-dataset claim for now). **No
replacement public KD corpus is picked** — that decision is deferred, not re-locked
to anything else (not `train_others`, not a new corpus). Spider itself is unchanged
(same train/test split as always).

**Scope cut to a PoC before any further build:** compare, on an identical slice of
Spider data, training it as plain gold-CE FT (`central_ft`) vs as a KD signal via Struct-SQL
(`poc_struct`) vs via KID (`central_kid`, still blocked on E0.3's mask-fill mechanics) — all
from the base model, no dual-stream mixing, no federation. Isolates whether the KD
*signal* itself beats plain FT on the same data, independent of which corpus eventually
supplies a public KD stream.

**Code cleanup:**
- Deleted `fedicl_sql/data/bird.py`, `tests/test_bird.py`, `scripts/download_bird.py`,
  `scripts/build_bird_processed.py`.
- Renamed `--bird-train`/`--bird-teacher-targets` → `--kd-train`/`--kd-teacher-targets`
  in `experiments/client_train/run.py`; `train_dual_stream(bird, bird_teacher_targets, ...)`
  → `train_dual_stream(kd_data, kd_teacher_targets, ...)` in `lora_trainer.py`.
- Deleted the 6 KD notebooks (`notebooks/kd/00_bird_data_prep.ipynb` ..
  `04_stage3_headline.ipynb`); replaced with `notebooks/kd/README.md` (CLI-only PoC
  runbook — no notebooks going forward for this workstream).
- Removed the 1.4 GB local `data/raw/bird/` download (gitignored, was never committed).

### Files updated
- `DECISIONS.md` — §3 dec.1, 4, 5, 8 (dataset question reopened; PoC framing)
- `KD_PLAN.md` — full rewrite: `§PoC` (runnable now) + `§Deferred` (old BIRD-era
  4-stage plan, kept for reference, not built against)
- `system_architecture.md` — top note + BIRD→generic "public KD corpus (TBD)"
  throughout §5.2/§5.6/§5.6.1/§6/§8/§9
- `CLAUDE.md`, `README.md` — KD section rewritten for the PoC CLI flow

### Next
- [ ] Run the PoC: carve slice `X`, train `central_ft` + `poc_struct`, eval on frozen
      Spider test, read off `poc_struct − central_ft`
- [ ] E0.3: pin KID [10] mask-fill mechanics before attempting `central_kid`
- [ ] Once the PoC has a verdict, decide the public KD corpus question (or decide to
      skip a public corpus and reuse the private pool for Stream 2)

*(superseded same day by the session below — CoT direction dropped, PoC arms renamed)*

---

## Session 2026-07-07 (2) — CoT KD direction dropped; two directions = RKD + KID, both from [10]

### What changed

**The Struct-SQL [11] QP-CoT direction is removed entirely** (advisor direction:
try the two methods from the KID paper instead). No offline teacher traces, no CoT
targets, no SeqKD baseline. The two KD directions are now both from **[10]**, both
online logit-level with teacher + student co-loaded (1 teacher forward/step):

- **RKD** — `CE(gold) + RKL(q‖p)` scored on gold SQL `y` (+1.9…+3.1 avg in [10])
- **KID** — same loss scored on imperfect `ŷ` = student one-pass rewrite of ρ-masked
  gold (+3.2…+5.8 avg, ~2× SFT latency; best trade-off in [10])

RKD is KID minus the imperfect-data step → one trainer serves both, and
`kid − rkd` isolates the imperfect-data value. PoC arms renamed:
`central_ft / central_rkd / central_kid` (each rung adds one ingredient). Deferred federated
ladder renamed too: `fedavg → fedavg_pub → fedkd_rkd → fedkd`.

**Old E0.3 blocker closed by reading [10] in full:** masking = Random strategy,
ρ = 0.2 default (0.1–0.3 safe, 0.5 degrades); fill = ONE teacher-forced student
forward (`no_grad`, greedy — temp unspecified in paper, greedy is our call);
rewrite = splice predictions into gold at masked positions (rewriting beats
masking-only +3.3 EX, Table 5); loss = RKL + auxiliary MLE (paper: MLE important
for stability; weighting under-explored → 1:1 default).

**Implementation plan written** (`KD_PLAN.md` §Implementation plan, 6 steps):
(0) delete offline pipeline (`gen_teacher_targets.py`, `data/teacher_targets.py`,
`--kd-train`/`--kd-teacher-targets`/`train_dual_stream`) → (1) `rkl_div_loss`
(full-vocab, co-loaded teacher = no top-K caching) → (2) `mask_rewrite` →
(3) teacher `score_logits` forward + 4-bit option → (4) online KD trainer step →
(5) CLI `--kd-direction {none,rkd,kid}`, `--mask-ratio`, `--teacher-4bit` →
(6) run PoC. VRAM: 4-bit teacher + student fits the 16 GB profile; fp16 co-load
= A100.

### Files updated
- `KD_PLAN.md` — rewritten: two-direction table, KID mechanics pinned, PoC arms,
  implementation plan, deferred ladder simplified
- `DECISIONS.md` — dec.1 (KD step = RKD/KID, CoT removed), dec.4/5/8, notation
  (λ(t) row dropped — combined cross-dataset loss already retired), [11] footnote
  → dropped-reference stub, [10] footnote → source of both directions
- `system_architecture.md` — header notes condensed + new re-align entry; §2
  diagram, §5.2, §5.3 arm/ladder tables, §5.6 (Random ρ=0.2, `CE + RKL`
  pseudocode), §5.6.1 rewritten (RKD vs KID), §8, invariants #2/#7/#9, §10;
  stale E-number refs (E0.3/E1.6/E1.7/E3.4/E3.5) cleaned
- `FedICL-SQL/CLAUDE.md` — GPU note (co-load + `--teacher-4bit`), PoC arm table
- `FedICL-SQL/README.md` — Quickstart trimmed (teacher-FT + target-gen steps out),
  PoC section rewritten
- `notebooks/kd/README.md` — runbook rewritten for `central_ft/central_rkd/central_kid`

### Implementation (same day, later session) — plan steps 0–5 executed

All six steps built and unit-tested (125 pass; 16 pre-existing spacy failures
unrelated). Deleted: `gen_teacher_targets.py`, `fine_tune_teacher.py`,
`data/teacher_targets.py`, `train_dual_stream`, sparse top-K `kl_div_loss`, the
`qp_cot` teacher mode. Added: `rkl_div_loss` (full-vocab reverse KL),
`training/imperfect.py::mask_rewrite` (Random mask → one-pass greedy fill →
splice), `LocalHFTeacher.score_logits`, `train_online_kd` (co-loaded teacher,
`L = λ_ft·CE + λ_kd·RKL`, checkpoint/resume), CLI `--kd-direction {none,rkd,kid}`
`--mask-ratio --teacher-model --teacher-4bit`.

Review caught two bugs before commit: (1) Qwen2.5 7B vs 1.5B logit dims differ
(V=152064 vs 151936 — same tokenizer, different embedding padding) → RKL now
slices both to the common vocab prefix; (2) fp16 KL sum over a 150k vocab loses
precision → RKL computed in float32.

### Next
- [ ] Run P0 → P1 → P2 on the compute host (P1/P2 need GPU + real 7B teacher —
      only unit-tested with fakes so far)
- [ ] Read off `central_rkd − central_ft` (teacher-logit value) and `central_kid − central_rkd`
      (imperfect-data value) via `analysis/compare.py` (scans result folders, no ledger)
- [ ] Once the PoC has a verdict, decide the public KD corpus question

---

## Session 2026-07-07 (3) — RUNS.csv ledger removed entirely

### What changed

**Dropped `experiments/RUNS.csv` and every code path that wrote or read it.**
It was a derived index (one denormalized row per run, duplicating fields already
in each run's own `metrics.json`) and had already drifted from reality twice this
session: `analysis/compare.py`'s hardcoded arm→identity table silently swapped
columns for any arm not in its enumeration, and separately a `git checkout`/pull
reverted the ledger and lost two real eval rows while their `metrics.json` files
(untracked) survived untouched. A ledger that can silently lie or vanish isn't
worth maintaining — the result folders under `experiments/*/results/*/` are the
only source of truth now.

- `fedicl_sql/runtime/results.py`: removed `LEDGER_FIELDS`, `_append_ledger`,
  `_repo_relative` (only used by the ledger row), and the call to it in
  `save_results`. `save_results` now only ever writes `metrics.json` +
  `config.json` + `predictions/<arm>.csv`.
- `analysis/log_session.py`: `_new_runs()` rewritten to glob
  `experiments/*/results/*/metrics.json` directly instead of reading the ledger
  — one row per eval_arms arm (`ex_mean`/`em_mean`), one row per run otherwise
  (`final_loss`).
- `tests/test_results.py`: dropped ledger assertions from
  `test_writes_metrics_and_ledger` (renamed `test_writes_metrics`) and
  `test_reruns_never_overwrite`; both now check `metrics.json` content only.
- Deleted `experiments/RUNS.csv` (git rm).
- Docs updated to stop describing a ledger: `README.md`, `CLAUDE.md`,
  `analysis/README.md`, `artifacts/README.md`, `paper/README.md`,
  `notebooks/kd/README.md` (code repo); `DECISIONS.md` §1/§7 (this repo).

### Next
- [ ] Nothing pending from this change — `analysis/compare.py` (already
      rewritten this session to scan folders) and `analysis/log_session.py`
      are the two ledger consumers, both now folder-native.

---

## Session 2026-07-08 — Architecture pivot: server-side distillation (Suggest.MD accepted)

### What changed

**`system_architecture.md` rewritten from scratch.** `Suggest.MD` (Fed-ICKD,
user-authored 07/2026) accepted as the architecture, with ONE amendment: the
server-distillation loss is reverse-KL from [10] (`L = λ_ft·CE + λ_kd·RKL(q‖p)`,
directions RKD/KID unchanged) — NOT Suggest.MD's forward KL(τ=2, top-50) +
relational RKD. Relational KD (distance/angle-wise, hidden states) dropped
entirely, which also resolves the RKD acronym clash (repo RKD = Reverse KD on
gold, per [10]).

Key pivots vs the old architecture:
- **Teacher moves client → SERVER.** Frozen 7B at the server, distills the
  FedAvg'd global student on a public pool `P` every round (consensus
  regularizer, FedDF/FedMD argument). Reverses the 2026-06-16 client-side
  re-alignment.
- **Client training = CE only** (QLoRA, DAIL ICL demos in prompt) — no teacher,
  no KD at the client. The sequential two-step design (Step 1 KD-pretrain →
  Step 2 FT) is retired.
- **ICL: k consistent train/inference at the client** (default k_student=2,
  ablate 0/1/2) — replaces the `train-k=0` official default + eval-k=3 overlay.
  DAIL dual similarity (masked-question + query) locked as the selection method.
- **Config defaults now:** K=8, Dirichlet α=0.5 by database, T=15, E=2, server
  distill 300 steps/round batch 16, eval = Spider dev + Spider-Realistic,
  3 seeds main / 1 ablation, 1× A5000.
- **Pool `P` dataset = TBD** (BIRD stays dropped; candidate = Spider held-out
  ~15%). Decide after the PoC.
- **DP demoted to Tier-3 optional** — no formal DP claim; threat-model paragraph
  + limitations instead.

**`DECISIONS.md` deleted** — still-load-bearing content (arm naming, legacy
alias map, notation, [10] reference note, per-run model-id recording) folded
into `system_architecture.md` §10/§12–§14. Refs fixed in `README.md` +
`KD_PLAN.md`.

**Unchanged / still running:** the centralized KD PoC (`central_ft` /
`central_rkd` / `central_kid` on Spider, `KD_PLAN.md` §PoC) — it now decides
the KD direction for the SERVER distill step instead of the client step; the
ladder logic (`rkd−ft` = teacher-logit value, `kid−rkd` = imperfect-data value)
is unaffected by where the teacher sits.

### Known stale docs (not touched this session)

- `CLAUDE.md` (both repos): direction bullets still describe the client-side
  teacher + two-step design + DECISIONS.md refs — needs a rewrite pass.
- `fig1_architecture.md` + `fig_architecture_source.png`: predate the pivot;
  Fig. 1 must be redrawn (teacher box → server, add pool `P`).
- Advisor sign-off: the 2026-06-16 client-side teacher direction came from the
  advisor — the server-side pivot should be confirmed with them.

### Next

- [ ] Finish the centralized PoC runs → pick RKD vs KID
- [ ] Decide the public pool `P` dataset
- [x] Update CLAUDE.md direction text — both rewritten from scratch 2026-07-08
      (root `CLAUDE.MD` = paper workspace: mental model, status, doc map,
      conventions; `fedicl-sql/CLAUDE.MD` = operational: compute host,
      checkpoint/VRAM rules, runnable arms, eval CSV contract)
- [ ] Redraw Fig. 1 (teacher box → server, add pool `P`)
- [ ] Then: Flower simulation (8 clients) + server distillation step

---

## Session 2026-07-08 (2) — teacher default: Coder-7B; 3 KD-impl bug fixes; teacher eval plan

### Teacher model default switched

`system_architecture.md` §3.1/§9: default candidate teacher **Qwen2.5-7B-Instruct
→ Qwen2.5-Coder-7B-Instruct**. Rationale: code-tuned, closer to SQL generation
than the general-instruct variant; no code change needed (`--teacher-model` was
already a CLI arg), shares the Qwen2.5 tokenizer so `rkl_div_loss`'s
common-vocab-prefix slicing is unaffected. Still **not finalized** — decide
after the centralized PoC + a model sweep. `CLAUDE.md`'s teacher-model mention
(line 46) is part of the larger stale client-side-design paragraph flagged last
session — not patched piecemeal, needs the full rewrite pass.

### 3 KD implementation bugs fixed (code review before the PoC's first real run)

Reviewed `losses.py` / `imperfect.py` / `lora_trainer.py` against [10]'s recipe.
Fixed (inner repo, 3 commits `788f8a2`/`24288e8`/`b86f0b5`):
1. `mask_rewrite` (KID) could mask the sequence's trailing stop token — now
   excluded from the maskable span.
2. `rkl_div_loss` missing the temperature² scaling factor (Hinton KD
   convention) — added; no-op at the current default τ=1.
3. `train_from_examples`/`train_online_kd` called a trailing `opt.step()`
   unconditionally after the loop, applying a zero-grad AdamW update (still
   drifts params via momentum/weight-decay) when the loop ended exactly on a
   grad_accum boundary — now guarded.

All pre-existing + 2 new tests pass (`test_training.py` 23/23; repo-wide
130 passed / 16 pre-existing spacy failures unrelated).

### Teacher eval — no new script needed

`experiments/eval_arms/run.py` is model-agnostic (`StudentModel` wraps any HF
causal-LM id; no adapter = base model) → the `teacher` arm (M4, zero fine-tune +
DAIL ICL) reuses it directly: `--model Qwen/Qwen2.5-Coder-7B-Instruct --arms
teacher=`. `--retrieval question` for now (dail_select needs spacy
schema-linking, currently broken — 16 pre-existing test failures). Commands
for both `--k 0` (bare) and `--k 3` (ICL) staged for the CUDA compute host;
not yet run (7B not cached locally, this Mac is smoke-test-only per CLAUDE.md).

### Next

- [ ] Run teacher eval (bare + k3) on the compute host, `Qwen2.5-Coder-7B-Instruct`
- [ ] Run the KD PoC (P0→P1→P2) with the 3 fixes in place
- [ ] Fix spacy schema-linking so dail_select retrieval works again

---

## Session 2026-07-08 (3) — ICL×KD lit scan; asymmetric-context KD added as Tier-3 direction

### Lit scan: methods that combine ICL with KD

Web scan for §2 Related Work + method-direction check. Three families found
(details + links in the session transcript; key arXiv ids below):

1. **ICL-ability distillation** — teacher and student both see demos; student
   learns to *use* demos (Huang et al. 2212.10670, foundational; 2412.13243).
   Student still needs retrieval at inference → weak system value for us.
2. **Context distillation** — teacher sees demos, student doesn't; demos'
   effect gets pushed into weights (Snell 2209.15189; 2409.01930; 2411.15927;
   **2602.12275 On-Policy Context Distillation — must-read novelty check**).
3. **Federated × KD × ICL** — FICAL 2412.08054 (transmits knowledge
   compendiums, not params); 2509.01750 (federated logit KD); 2602.18749
   (Federated Reasoning Distillation — newest, check for overlap);
   survey 2406.10861. Theory: 2506.11516 ("ICL is implicit KD" — motivation
   anchor for the Fed-ICKD name). Also: PromptKD 2402.12842 (soft-prompt-tuned
   teacher, student-friendly distributions); Inter-Cascade 2509.22984
   (gradient-free in-context KD via strategy repository).

No paper found doing our combo (ICL-consistent client FT + FedAvg LoRA +
server-side RKL KD on a public pool, Text-to-SQL). Closest: FedCoLLM [8],
FICAL, 2602.18749.

### Decision: asymmetric-context KD → Tier 3 (`system_architecture.md` §8.1)

Observation driving it: in the current symmetric setup (teacher and student
score the KD pair under the *same* DAIL context) the demos' effect appears in
both `p` and `q` and largely cancels in RKL — ICL is background, not distilled
content. The asymmetric variant (teacher k=3, student k=0, same target) makes
the demos' effect the thing RKL transfers → student internalizes ICL, deploys
at k=0 (no client retrieval stack). Added as **Tier 3 deferred**, probe arm
`central_rkd_asym`, kill criterion < ~1 EX over the symmetric k=0 floor,
gated on: PoC verdict first, novelty check vs 2602.12275, advisor sign-off
(scope change vs approved outline).

### Next

- [ ] (unchanged) finish KD PoC P0→P2; teacher eval on compute host; pick `P`
- [ ] Read 2602.12275 + 2602.18749 — novelty/overlap check before any asym build
- [ ] Raise asymmetric-context direction with advisor together with the
      server-side pivot sign-off

## Session 2026-07-09 — RKD×ICL check: already implemented via `--train-k`

Question: does the RKD implementation support ICL in the KD context, per the
architecture? **Yes — no new code needed.** Mechanics verified in
`fedicl_sql/training/lora_trainer.py`:

- `--train-k K` → `_make_train_demo_fn` (DAIL retrieval over the training CSV,
  self excluded, cross-db preferred, committed `.dailcache.json` reused) →
  `build_examples` renders demos into each training prompt.
- **Symmetric context by construction:** in `train_online_kd` the RKD path sets
  `kd_input_ids = input_ids` (the demo-laden CE sequence) and
  `teacher.score_logits(kd_input_ids)` scores that same sequence — `p` and `q`
  share one ICL context (§3.4 invariant), automatically, for KID too (the mask
  only touches the target span after `n_prompt`; demos stay intact).
- Demo format = `question + SQL`, `never_schema` (§5.2 compliant).

Two flags raised, no changes made:

1. **Random-k deviation:** `build_examples` injects n ~ U{0..train_k} demos per
   example (deliberate — DAIL-SQL §4.4.4 train/eval-parity robustness), while
   `system_architecture.md` §5.4/§6 specifies *fixed* k (k_student=2, distill
   k=3) and lists "k-robust training (random k)" as Tier 3. Code default ≠ doc
   default — align one of them before the federated build (advisor/doc call).
2. **Current PoC runs are k=0:** the runbook P1/P2 commands pass no `--train-k`,
   so existing `central_rkd`/`central_kid` adapters trained without ICL. Added
   an optional P1-variant command (`central_rkd_k2`, train-k=2 + eval `--k 2`)
   to `notebooks/kd/README.md` — not part of the 3-arm verdict.

### Next

- [ ] (unchanged) finish KD PoC P0→P2; teacher eval on compute host; pick `P`
- [ ] Decide fixed-k vs random-k demo injection (code vs §5.4/§6 mismatch)
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-09 (2) — asymmetric-context KD implemented (`--kd-teacher-k`)

Built the §8.1 probe machinery (TDD, tests first). What changed in `fedicl-sql/`:

- `fedicl_sql/training/losses.py::rkl_asym_loss` — RKL when teacher and student
  condition on DIFFERENT prompts but the SAME target: slices each side to the
  window predicting the target (position `n_prompt−1` emits the logit for
  target token 0), delegates to the existing `rkl_div_loss`. Two alignment
  tests, incl. an off-by-one guard on the first target token.
- `fedicl_sql/training/dataset.py` — `TrainExample.teacher_prompt_ids`;
  `build_examples(kd_teacher_k, teacher_demo_fn)` attaches a demo-laden teacher
  prompt per example. Teacher k is FIXED (never the student's random 0..k) so
  the teacher's RKD context stays constant → offline logit cache stays possible.
  Left-trimmed so prompt+target fits max_len. Three builder tests.
- `train_online_kd` — if `teacher_prompt_ids` present: teacher forward on
  `teacher_prompt ⊕ kd_target` (gold y for RKD, rewritten ŷ for KID — both
  supported), `rkl_asym_loss` for the KD term. Else: symmetric path unchanged.
- CLI: `--kd-teacher-k N` on `experiments/client_train/run.py` (errors without
  `--kd-direction rkd/kid`).

Verified: 28/28 training tests pass (16 pre-existing failures elsewhere = spacy
`en_core_web_sm` missing on this Mac, untouched files); real-model smoke on
Qwen2.5-Coder-0.5B (asym rkd + asym kid + symmetric regression, 2 steps each,
losses finite). Runbook §P1-probe added (`central_rkd_asym`, teacher k=3,
student k=0, eval k=0); §8.1 marked "code ready, run gated".

**Not run.** Probe stays gated per §8.1: P0–P2 verdict first, novelty check
2602.12275, advisor sign-off. Floor already on file: symmetric `central_rkd`
k=0 = 68.28 EX; kill if `asym − 68.28 < ~1` EX.

### Next

- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] After verdict: `central_rkd_asym` probe (runbook §P1-probe) if gates clear
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-09 (3) — GOAL section added to system_architecture.md

Architecture review against the intended paper goal ("small open-source model
reaches a larger model's performance in a federated setting, at lower serving
cost, via SFT + KD + ICL"). Verdict: the idea was implicit in §1/RQ3 but never
stated as an explicit, measurable goal — and no cost dimension was
operationalized anywhere.

- Added a **GOAL** section at the top of `system_architecture.md` (before §0):
  small student ≈ larger teacher's performance at a fraction of serving cost;
  the three ingredients named generically (SFT, KD, ICL — realizations stay in
  the body sections, GOAL doesn't pin techniques); cost asymmetry framing (teacher cost paid once at training, per-query cost =
  student's); success metric = share of base→teacher gap recovered,
  `(fedkd − base)/(teacher − base)` — target share fixed after the PoC, never
  absolute parity.
- Flagged but NOT done (needs user/advisor call): efficiency metrics
  (VRAM/latency/throughput) are still not measured by any eval script; a 32B
  ceiling-probe teacher stays unproposed.

### Next

- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] After verdict: `central_rkd_asym` probe (runbook §P1-probe) if gates clear
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items
- [ ] Decide: add efficiency columns (VRAM/latency) to eval convention?

## Session 2026-07-09 (4) — why ICL stops helping after FT/KD + the fix direction

Question: every fine-tuned/distilled arm LOSES EX when we add k=3 DAIL demos at
eval (central_rkd 68.28 → 65.86; ft_no_icl 62.19 → 61.90; ft trained WITH
demos 64.02 → 59.09; even the 7B teacher 78.72 → 78.53). Ran per-record diffs
(`analysis/icl_diff.py`) on all four k0-vs-k3 pairs plus three new offline
probes on the existing prediction CSVs — no GPU needed.

### Bug found and fixed on the way

`analysis/icl_diff.py` looked for demos with the marker
`### Foreign Example SQL:` but the prompt builder writes `### Example SQL:` —
so the "schema bleed" cause was silently impossible (always 0) and everything
it should have caught was counted as structure_change. Fixed in the code repo.
Corrected cause split for central_rkd's 74 broken rows: 33 structure change,
22 identifier swap, 11 literals, 8 schema bleed. Structure change still the
top cause, but not as dominant as the buggy 65% first read.

### What the analysis actually says (plain language)

1. **ICL is a high-variance edit, near-zero on average.** Demos fix 4–7% of
   rows and break 7–12% of rows; the two nearly cancel. The rows it breaks are
   rows the model already had right zero-shot.
2. **Retrieval quality is NOT the problem.** Top-1 similarity of the demos is
   the same for helped rows and broken rows (~0.92 both). Worse: broken rows
   MORE often already had a demo whose SQL shape exactly matched the gold
   shape (73%) than helped rows did (47%). So "retrieve better demos" attacks
   the wrong bottleneck — the right demo was usually already in the prompt.
3. **Mechanism = demo-induced distraction, not clean copying.** Of the broken
   rows, about half changed query shape vs their k=0 answer, mostly AWAY from
   the gold shape, but only ~⅓ of those land exactly on a demo's shape. The
   demos perturb a small model off an answer it already knew; they don't
   simply overwrite it.
4. **Copying is asymmetric — that's the exploitable structure.** When the
   zero-shot answer is wrong, imitating demos helps (that's where all the
   gains live). When it's right, demos can only hurt. So ICL should be
   **gated on whether the zero-shot answer is trustworthy**, not applied
   uniformly.
5. **A trivially cheap gate already works, measured offline on existing runs.**
   Gate = "keep the k=0 answer; only if its SQL fails to execute, take the
   k=3 answer instead":
   - central_rkd: 68.28 → **70.41** EX (+2.13; oracle gate ceiling 73.02)
   - central_rkd_asym: 67.50 → 69.34 (+1.84)
   - qwen1b_ft_no_icl: 62.19 → 66.3–66.4 (+4.2)
   - teacher: 78.72 → 80.66 (+1.94)
   Every arm ends ABOVE both its k=0 and k=3 numbers — ICL becomes strictly
   helpful. The k=0 answer fails to execute on 14% of rows (central_rkd) and
   demos repair 15% of those; the teacher repairs 41% of its 4%.
6. **Train-time demo exposure does not immunize.** The arm trained WITH k=3
   demos is the WORST under eval-time ICL (−4.9 pp net) — it leans harder on
   demo shapes, not less.
7. **§8.1 kill criterion is met.** `central_rkd_asym − central_rkd` =
   67.50 − 68.28 = −0.78 EX < +1 EX floor (1 seed) → per the pre-registered
   criterion the asymmetric-context variant is dead. Needs the
   system_architecture.md §8.1 status flip + advisor note (not done this
   session — decision-record change, flagging first).

### Proposed solution track — "gated ICL" (ranked, cheapest first)

- **S1 — exec-error gate (build next).** New eval mode in
  `experiments/eval_arms/run.py`: pass 1 at k=0; only rows whose SQL errors
  get a pass 2 with k=3 demos. Offline numbers above ARE this gate's result,
  so the live run is a confirmation, not a gamble. Extra compute: second pass
  on ~14–20% of rows. Deployment story fits GOAL: per-query cost stays k=0
  for ~86% of queries; retrieval/FAISS only on the fallback path.
- **S2 — confidence gate (the analysis upgrade).** Exec-error only catches
  broken SQL, not wrong-but-runnable SQL; gap to the 73.02 oracle is rows
  where k=0 runs fine but is wrong. Capture the k=0 answer's sequence
  log-prob in the eval CSV (one new column), sweep the threshold offline on
  the same runs, keep exec-error as the always-on floor. This is the paper's
  ablation axis: gate ∈ {none, exec, exec+conf, oracle}.
- **S3 — execution voting.** Generate k=0 and k=3, execute both, prefer the
  one that runs / non-empty / agreement. Costs 2× generation on every row —
  only if S2 stalls.
- **S5 — demo-robustness training.** Train with demos where p% are randomly
  wrong/irrelevant while the target stays gold — teach "demos are reference,
  not template". New training arm; only worth it if S1/S2 numbers make the
  gated-ICL story central to the paper.

**Correction (same day, caught by user question):** the four k=3 eval runs
analysed above were NOT plain question-similarity kNN — `config.json` on all
four confirms `retrieval: dail_select, tau: 0.85`, i.e. the FULL DAIL
Selection gate was already active: model drafts SQL at k=0 first
(`predict_target_skeleton`), then the retriever keeps only demos whose gold
skeleton is Jaccard ≥ 0.85 vs the draft's skeleton before ranking by masked-
question similarity (`fedicl_sql/retrieval/dail_select.py:120-136`). So the
old "S4: wire up dail_select" item never applied — it was already running.
Deleted from the list above.

This makes finding 2 (broken rows had a shape-matched demo 73% of the time
vs 47% for helped rows) a **direct, expected consequence of the gate**, not
a coincidence — dail_select explicitly selects shape-matching demos. Net
effect: even with a real structural-similarity gate live, ICL still nets
negative on every trained arm. Strengthens the diagnosis — the failure isn't
retrieval quality at any sophistication level, it's that showing ANY demo to
an answer the student already had right can knock it off, regardless of how
well-chosen the demo is. Selective-ICL (gate on the *student's own answer's
trustworthiness*, not on demo quality) is the correct fix layer; nothing else
changes in the plan.

Paper angle: this is not damage control, it's a §5 analysis contribution —
"when does ICL help a fine-tuned small student" (it helps exactly when the
student's zero-shot answer is untrustworthy) + a cheap selective-ICL overlay
that turns a −2.4 pp liability into a +2.1 pp gain with sub-linear extra cost.
Fits Fed-ICKD unchanged: gate lives entirely client-side at inference.

### Next

- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-10 — S1/S2 selective-ICL gate implemented, code repo

Built S1 (exec gate) and S2 (confidence gate + free offline sweep) from the prior
session's plan. Nothing run yet — no adapters on this machine (compute host only);
next session on the host runs the commands below.

**`fedicl-sql/` changes:**
- `fedicl_sql/models/student.py` — `generate_scored` / `generate_batch_scored`:
  greedy batched generation + mean token log-prob per sequence, masking out
  batch-padding tokens after each sequence's own EOS (handles pad_id==eos_id and
  pad_id!=eos_id alike). Verified against a real model (Qwen2.5-Coder-0.5B,
  `.model_cache`): text output byte-identical to plain `generate_batch`, logprobs
  negative and sane, across a 2-prompt batch with different lengths.
- `fedicl_sql/eval/loop.py::eval_loop_gated` — new eval loop alongside `eval_loop`:
  scores a k=0 draft first (always logs `draft_predicted/draft_exec_error/
  draft_logprob`), only runs the caller's ICL prompt_fn as a second pass on rows
  that fail the gate. `gate="exec"`: fallback iff draft SQL errors. `gate="conf"`:
  also fallback iff `draft_logprob < conf_tau`. 5 new unit tests (fake model keyed
  by prompt text) — bad-gate-name / conf-without-tau raise, exec keeps a working
  draft with zero ICL calls, exec falls back on a broken draft, conf falls back on
  a *working* draft when confidence is low (the case exec alone would miss).
- `fedicl_sql/runtime/results.py::PREDICTION_FIELDS` — added `hardness` (was
  documented as a required eval CSV column in this repo's `CLAUDE.md` but silently
  dropped by `_write_predictions` since inception — pre-existing drift, fixed in
  passing) plus the 4 new gate diagnostic columns. Old committed CSVs are
  unaffected (they simply don't have these columns; `.get(k, "")` in the writer
  already handled the reverse case for old callers).
- `experiments/eval_arms/run.py` — `--icl-gate {none,exec,conf}` (default `none` =
  unchanged behavior) + `--conf-tau`; validates `conf` requires a tau and that a
  gate requires `--k > 0`. Builds a k=0 `prompt_fn` as the draft and the existing
  k=args.k `prompt_fn` as the ICL fallback, routes through `eval_loop_gated`.
  Per-arm metrics gain `icl_gate` + `gate_fire_rate`; ckpt filenames get a
  `__gate{name}` suffix so a gated and ungated resume never collide.
- `analysis/gate_sweep.py` (new) — sweeps `conf_tau` **without any new GPU run**:
  joins an S1 (`--icl-gate exec`) run's `draft_logprob` (logged for every row) against
  an existing full-k3 predictions CSV (e.g. `central_rkd_k3dail.csv` — same
  model/adapter/demos/seed ⇒ identical greedy ICL output regardless of which run
  produced it, so it's reusable as-is). Dry-run validated: at the most negative
  tau the sweep converges exactly to the exec-gate EX; the curve peaks at
  73.02% (session's earlier-computed oracle ceiling) under a synthetic
  logprob deliberately correlated with correctness — confirms the join/simulate
  logic before any real model logprobs exist.
- `notebooks/kd/README.md` §4b — S1 command, S2 sweep + confirm-live workflow for
  `central_rkd`, note to repeat for `central_rkd_asym`/`qwen1b_ft_no_icl`/`teacher`.
- `analysis/icl_diff.py` bug fix carried over from last session (wrong demo
  marker) already committed to code repo.

Verified: 161/161 repo tests pass (`.venv/bin/python -m pytest tests/`); CLI
validation (`--icl-gate conf` without `--conf-tau`, `--icl-gate exec` with `--k 0`)
both error as designed.

**Not run:** no GPU / adapters on this machine. Next: run S1 on the compute host
for `central_rkd` (+ `ft_no_icl`, `teacher` as cross-checks against the offline
numbers), then `analysis/gate_sweep.py` to pick `conf_tau`, then confirm S2 live.

### Next

- [ ] Run S1 (`--icl-gate exec`) on compute host: central_rkd, ft_no_icl, teacher — confirm ≈70.4 / 66.4 / 80.7
- [ ] `analysis/gate_sweep.py` on the S1 output → pick conf_tau per arm
- [ ] Confirm S2 (`--icl-gate conf --conf-tau <chosen>`) live per arm
- [ ] Flip §8.1 to killed (criterion met, −0.78 EX) + advisor note
- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-10 (2) — S1 bug found + fixed; S1 confirmed live on `central_rkd`

**Bug in `eval_loop_gated` (code repo), caught before it corrupted a real result.**
First live S1 run (`central_rkd_gate_exec`, since deleted) reported EX=88.10% with
0 wrong answers among the 888 non-fallback rows — impossible for a 1.5B model, so
treated as a bug signal, not a result. Two bugs, both in the non-fallback branch:
(1) `correct` was set from `draft_exec_error == ""` (SQL merely ran) instead of the
real `score_ex_detail` match against gold — any executable-but-wrong draft scored
ex=1. (2) fixing (1) added `ok` to the `drafts` tuple, which shifted the fallback
flag from index 3 to 4; the fallback-index filter still read index 3 (now the
log-prob float, always truthy) → every row fired the ICL pass regardless of intent.
Neither bug surfaced in unit tests because both fake-draft test cases happened to
be both executable AND correct — added a regression test (draft executes cleanly
but returns wrong rows: must NOT fire the gate, must still score ex=0) that catches
both. Fixed + committed (`fedicl-sql` `c493138`); 162/162 tests pass.

**S1 re-run on the compute host after the fix, real numbers:**

| | n | correct |
|---|---|---|
| draft (k=0), gate did not fire | 888 | 706 |
| ICL fallback (146 rows draft's SQL failed to execute) | 146 | 23 |
| **total** | 1034 | **729 → EX = 70.50%** |

706/888 exactly reproduces the standalone k=0 run's own EX numerator (706/1034 =
68.28%) — confirms the draft pass is a faithful, deterministic re-run of that
arm's k=0 eval, no adapter/environment drift. 23/146 = 15.8% repair rate on the
gated subset, matching the 15% estimated offline last session. **vs the three
comparators: k=0 alone 68.28%, full k=3 ICL 65.86%, exec gate 70.50% — beats
both** (+2.22pp vs k0, +4.64pp vs uniform ICL). S1 verdict: real, confirmed, works
as designed.

**S2 sweep (`analysis/gate_sweep.py`, zero extra GPU) on the corrected S1 output:**
peaks at `tau=-0.20` → EX=70.70% (+0.20pp over exec-only, +12 extra fallbacks),
flat at 70.41–70.50% for any more negative tau, and actively WORSE above -0.10
(69.54% at -0.10, 66.54% at -0.05 — too many false-positive fallbacks). **Verdict
for `central_rkd`: the confidence gate adds essentially nothing beyond the exec
gate here** (+0.2pp, likely within noise) — draft log-prob doesn't separate
right/wrong among executable queries much better than exec status alone. Not
worth a separate `--icl-gate conf` live run for this arm; report S1 (exec) as
the headline gate for `central_rkd`. Re-check this verdict per-arm (ft_no_icl,
teacher, central_rkd_asym) before generalizing — the sweep is cheap enough to
just run each time.

### Next

- [ ] Run S1 (`--icl-gate exec`) on `qwen1b_ft_no_icl`, `teacher`, `central_rkd_asym` — confirm/compare vs offline estimates (≈66.4 / 80.7)
- [ ] `gate_sweep.py` per arm — check whether conf gate earns its keep anywhere (central_rkd says no)
- [ ] Flip §8.1 to killed (criterion met, −0.78 EX) + advisor note
- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-10 (3) — gate confirmed 6/6 arms; codes-retrieval mixed; exec mechanism verified

**S1 (exec gate) now run on all 6 available arms, spanning 3 model scales — wins on every single one:**

| arm | model | k=0 | uniform ICL | gate exec | Δ vs k0 | Δ vs uniform | fire rate |
|---|---|---|---|---|---|---|---|
| central_rkd | 1.5B | 68.28 | 65.86 | 70.50 | +2.22 | +4.64 | 14.1% |
| central_rkd_asym | 1.5B | 67.50 | 65.38 | 69.15 | +1.65 | +3.77 | 14.6% |
| qwen1b_ft_no_icl | 1.5B | 62.19 | 61.90 | 66.54 | +4.35 | +4.64 | 20.4% |
| qwen1b_ft_icl_k3 | 1.5B | 64.02 | 59.09 | 67.02 | +3.00 | **+7.93** | 17.8% |
| qwen0.5b_ft_no_icl | 0.5B | 48.55 | 44.29 | 51.84 | +3.29 | +7.55 | 30.3% |
| qwen0.5b_ft_icl_k3 | 0.5B | 49.03 | 48.07 | 53.09 | +4.06 | +5.02 | 29.8% |
| teacher | 7B | 78.72 | 78.53 | 80.37 | +1.65 | +1.84 | 4.0% |

6/6 = 100%. Notably `qwen1b_ft_icl_k3` — the single worst uniform-ICL regression
(−4.93pp last session) — flips to the LARGEST recovery under the gate (+7.93pp):
training with demos doesn't make the student robust to eval-time ICL, but it
doesn't defeat the gate either. Fire rate scales inversely with model capacity
(0.5B ~30% vs 1.5B ~15–20% vs 7B ~4%) — weaker models draft more broken SQL — yet
the gate stays net-positive at every capacity level tested so far.

**S2 (confidence gate) offline-swept on all 4 arms with a matching full-k3 CSV
(central_rkd, central_rkd_asym, qwen1b_ft_no_icl, teacher): negligible everywhere.**
Best case +0.1–0.2pp over exec-only, within noise, and actively worse once tau
is loosened past roughly −0.1 (too many false-positive fallbacks). Verdict:
skip live `--icl-gate conf` runs; exec alone is the reportable gate for every
arm tested.

**codes-retrieval-inside-the-gate: 2/4 data points landed, EX consistent, speed
NOT.** `central_rkd`: dail_select-gate 70.50% @ 0.735s/q vs codes-gate 69.92%
@ 0.158s/q (−0.58pp, 4.65× faster). `qwen1b_ft_no_icl`: dail_select-gate 66.54%
@ 0.549s/q vs codes-gate 66.73% @ 0.620s/q (**+0.19pp, but SLOWER**). EX
conclusion holds (codes ≈ ties dail_select, both directions within ~0.6pp — safe
to say codes doesn't cost meaningful accuracy). **The earlier "codes is ~4.6×
faster" claim does NOT generalize from this second data point** — don't repeat
it as a general result yet; needs a controlled re-time (same arm, repeated
trials, explicit cache-warm state) before trusting either number. `--retrieval
codes` timing is currently unexplained/noisy, not a settled finding.
`central_rkd_asym_gate_exec_codes` and `teacher_gate_exec_codes` still pending
on the host (commands already issued, not yet returned).

**`--schema-style codes` (CodeS §6.3 metadata schema, separate axis from
`--retrieval codes`) discussed, NOT run.** Confirmed via config.json audit:
0/21 eval runs and 0 training runs have ever used it — every adapter was
trained with `schema_style=full` (CREATE-TABLE DDL). Can't eval-swap an
existing adapter onto `--schema-style codes` (model never saw that prompt
format) — would need a fresh `client_train` run first. Bigger-cost, separate
research question from the gate work; parked, not scheduled.

**Verified the eval/gate correctness signal is real SQL execution, not a cheaper
proxy.** `fedicl_sql/eval/metrics.py::_execute` (line 98) opens a real sqlite3
connection and does `cursor.execute(sql); cursor.fetchall()` — actual rows, not
`EXPLAIN QUERY PLAN` or a parse-only check. A real 60s timeout via SQLite's
`progress_handler` (polled during execution — `signal.alarm`/`asyncio` don't
preempt a blocking C-level call). Both `score_ex_detail` (final EX) and the
exec-gate's own decision (`eval_loop_gated`, same function) run through this —
no separate/cheaper check exists for SQLite (no server-side prepare-only step
that would catch semantic errors like an unknown column without actually
running). Conclusion: correct as-is, no change warranted; noted as a possible
future concern only if the public pool `P` scales to BIRD-sized DBs where
per-row execution cost might matter.

## Session 2026-07-10 (4) — KID/RKD trainer speed optimizations (loss-identical)

`central_kid` on the A5000 was slow; landed three optimizations in `fedicl-sql`
(`lora_trainer.py`, `imperfect.py`, `teacher_local.py`). All are numerically
identical to the old code — the loss math is unchanged, so a mid-run `_ckpt/`
resume stays valid and the PoC comparison is not confounded:

1. **RKL sliced to the target span.** The symmetric KD path ran float32
   log-softmax over the FULL sequence (up to 2560 positions) × full vocab (~152k)
   for both student and teacher — ~4.6 GB of transient float32 per step, inside
   the grad graph — when only the ~50–80 SQL-token positions at the end contribute
   (prompt positions are zeroed by the mask). Both logits and mask now slice to
   `[n_prompt-1:]` before `rkl_div_loss`. Equivalence pinned by a unit test.
2. **`logits_to_keep` on teacher + student-ŷ + fill forwards.** lm_head projection
   (`T×hidden @ hidden×152k`) now computed only for the target span (teacher +
   student KID forward) or only at the masked predictor positions (mask_rewrite
   fill, tensor-index form). Verified on real Qwen2 modeling code + peft LoRA
   wrapper: sliced logits match full-forward logits, grads flow. Asym path
   (§8.1, about to be killed anyway) left unoptimized.
3. **Per-step `loss.item()` sync removed** — losses buffered on-device, drained
   to floats at optimizer boundaries (every grad-accum), always before checkpoint.

NOT done (deliberate): teacher fp16 instead of 4-bit — ~2× faster forward but
changes the teacher's logit distribution = different stack than the finished
`central_rkd` run; would force an rkd rerun. Kept `--teacher-4bit`.

Expected wall-clock ~1.3–1.7× on long-prompt examples; actual number to be read
off the next KID run's `time_average`. Tests: 176/176 pass. Not yet committed
in `fedicl-sql`.

### Next

- [ ] Commit trainer optimization in `fedicl-sql`; restart/resume `central_kid` on A5000, note new s/step vs old
- [ ] Land `central_rkd_asym_gate_exec_codes` + `teacher_gate_exec_codes` (commands already issued)
- [ ] Controlled dail_select-vs-codes re-timing (same arm, repeated, explicit cache state) before citing any speed number
- [ ] Flip §8.1 to killed (criterion met, −0.78 EX) + advisor note
- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items
- [ ] Decide whether a fresh `--schema-style codes` training run is worth scoping (separate track from the gate result)
