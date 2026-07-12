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

## Session 2026-07-11 — skew RKL implemented (§8.2, Tier-2 A6)

Built the loss-side half of the "better KD/ICL fit" research pass (advisor/PhD-review
question this session). Implemented **skew RKL** (DistiLLM, Ko et al. 2024,
arXiv:2402.03898 §3.1): plain `RKL(q‖p)` can blow up wherever the student assigns
mass the teacher assigns ~0 (`log p → -∞`) — skew mixes the teacher denominator with
the student's own distribution, `(1-λ)·p + λ·q`, damping the gradient without
changing the mode-seeking direction.

**`fedicl-sql/` changes:**
- `fedicl_sql/training/losses.py::rkl_div_loss` — new `skew_lambda: float = 0.0` param.
  `0.0` (default) takes the exact old code path (`log_denom = t_log`, no extra exp/clamp)
  — byte-identical output, confirmed by `torch.equal` in the new test, so existing
  `_ckpt/` resumes and the finished `central_rkd` run are unaffected. `>0` mixes in
  probability space (`t_log.exp()` + `q`), clamps before `.log()` for numerical safety.
  `rkl_asym_loss` gained the same param, forwarded straight through (asym path already
  computed in §8.1, unaffected unless the flag is passed).
- `fedicl_sql/training/lora_trainer.py` — `LoraTrainConfig.rkl_skew_lambda: float = 0.0`;
  both call sites (symmetric + asym) pass it through.
- `experiments/client_train/run.py` — CLI `--rkl-skew-lambda` (default 0.0), validated
  to require `--kd-direction rkd/kid` (same pattern as `--kd-teacher-k`).
- 4 new tests: skew=0 matches plain exactly (`torch.equal`), skew=0.1 strictly damps
  divergence on a full-disagreement case (both `rkl_div_loss` and `rkl_asym_loss`),
  `LoraTrainConfig` default assertion. 179/179 repo tests pass (was 176).

**Docs:** `system_architecture.md` §8.2 (new, mirrors §8.1's structure) + Tier-2
ablation table A6 (`rkl vs skew-rkl on the PoC winner, λ~0.1`).

**Not run** — no GPU on this machine. Scoped as a same-cost extension of whichever
PoC arm wins (`central_rkd_srkd` or `central_kid_srkd`), 1 seed, after the
RKD-vs-KID verdict — not a third co-equal arm.

### Next

- [ ] (unchanged) P2 `central_kid` on compute host → RKD-vs-KID verdict
- [ ] After verdict: run A6 (`--rkl-skew-lambda 0.1`) on the winning arm, 1 seed
- [ ] (unchanged) S1/S2 gate loose ends (see 2026-07-10 sessions) — static/exec-free
      gate signal still needed for production (no-exec-at-inference constraint)
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-11 — ICL methods survey note + scope caveat on ICL-after-FT observations

### What changed

**New note: `paper/notes/icl_methods_survey.md`** — taxonomy 4 trục của ICL
text-to-SQL (selection / demo source / organization / usage policy), tóm tắt
12 phương pháp (DAIL, CodeS, ACT, DIN, DCG-SQL, SAFE-SQL, ODIS, MARLO, ASTRES,
Fed-ICL/IFed-ICL/FICAL, 2 survey), bản đồ "ai compare ai" với số fetch từ paper
gốc (DCG-SQL có compare DAIL: 82.1 vs 71.2 trên Llama 3.1-8B, 87.5 vs 82.8 trên
GPT-4; SAFE-SQL: 87.9 vs DAIL 83.6 GPT-4o Spider; MARLO +0.8 vs metadata-masking),
và đối chiếu với số nội bộ.

**DAIL-vs-codes-vs-question verdict từ results hiện có (33 runs scanned):**
DAIL ≥ codes ở mọi điểm đo nhưng chỉ rõ trên base model (0.5B base k3: 28.05 vs
25.82); trong exec-gate thì hòa (±0.6pp trên subset fire nhỏ). Question-sim
thường: **chưa có run sạch nào ở k3** — cột trống của ablation A5; cần 1–2 run
`--retrieval question` trên central_rkd (uniform + gate) để thang
random/question/dail/codes đủ chân.

**Scope caveat declared (user direction): "ICL giúp base / hại FT" KHÔNG được
phát biểu như finding.** Phạm vi test hiện tại quá hẹp (Spider dev, 1 seed/arm,
chủ yếu Qwen; gemma_ft +1.35 là counter-datapoint 1 seed). Mọi statement trong
docs giữ ở mức "current observation, pending confirmation": cần nhiều seed,
Spider-Realistic, thêm model family trước khi khái quát. LAB_LOG entries cũ giữ
nguyên (log lịch sử, số per-arm vẫn đúng cho arm đã đo) — riêng
`system_architecture.md` §5.4 được sửa: rationale "same k train/inference"
flip từ khẳng định → hypothesis-under-test, kèm ghi chú quan sát ngược chiều
(k3-trained arm regress mạnh nhất dưới uniform ICL; exec-gate dương trên mọi
arm đã test) + pointer A2 là ablation quyết định.

### Next

- [ ] A5 mở rộng: chạy `--retrieval question` k3 (uniform + gate exec) trên
      central_rkd — lấp cột trống trước khi viết §5
- [ ] Recheck gemma_ft k3 (+1.35) + mở rộng seeds/Spider-Realistic trước mọi
      câu khái quát ICL-sau-FT
- [ ] (unchanged) P2 `central_kid` verdict; flip §8.1 killed + advisor note;
      2602.12275 + 2602.18749 novelty check; advisor sign-off items

## Session 2026-07-11 (2) — P2 `central_kid` verdict: RKD wins EX, KID wins ICL-robustness

### What changed

**PoC ladder complete** (P0 proxy / P1 `central_rkd` / P2 `central_kid`, all 3
ICL conditions each, `Qwen2.5-1.5B-Instruct` ← `Qwen2.5-Coder-7B-Instruct`
4-bit teacher, seed 0, matched hyperparams confirmed by diffing
`experiments/client_train/results/*/config.json` for both adapters — identical
`epochs/lr/lora_r/max_len/beta_struct=2.0/lambda_ft=lambda_kd=1.0/teacher_4bit/
train_k=0/seed`, differ only in `kd_direction` + `mask_ratio` (kid-only)):

| condition | RKD | KID | Δ(KID−RKD) |
|---|---|---|---|
| k=0 (floor) | 68.28 | 66.83 | −1.45 |
| k=3 dail uniform | 65.86 | 65.96 | **+0.10** |
| k=3 dail gate_exec | 70.50 | 69.15 | −1.35 |

`rkd − ft_proxy(qwen1b_ft_no_icl_k0=62.19)` = **+6.09 EX** (teacher-logit KD
signal is real, validates building further). `kid − rkd` = **−1.45 EX** at the
floor — **opposite [10]'s own headline result** (KID ≥ RKD on every pair they
report, e.g. QWen1.5-0.5B←1.8B: RKD 62.7 vs KID 63.7, +1.0). Margin size is
comparable (~1–1.5pp both directions), just flipped sign.

**Second finding, not just noise — KID is more ICL-robust, not just weaker:**
Δ(uniform ICL vs own k=0) = RKD −2.42 vs KID **−0.87** (2.8× smaller hit).
Consistent losing/tying across all 3 conditions (never a clean KID win except
the trivial +0.10 tie) argues against pure 1-seed noise — noise would more
likely flip sign inconsistently across conditions, not lose 2/3 + tie 1/3.
The robustness delta echoes [10]'s own claimed benefit (paper reports KID
+2.7 Spider-DK / +2.1 Spider-Realistic robustness gains) — same underlying
mechanism (mask-rewrite exposure → less brittle under prompt perturbation),
different measurement axis (ICL-injection sensitivity here vs domain-shift
benchmarks there).

**Research pass: checked our implementation against [10] itself (no public
code exists — verified via arXiv page, GitHub search, PapersWithCode,
OpenReview, full paper text: zero code-availability statement anywhere).**
Masking (Random, ρ=0.2) and rewrite (student one-pass greedy fill) match the
paper's prose exactly. Two things the paper explicitly leaves undefined —
confirmed by direct quote: *"the better combination of the distillation loss
and MLE loss is still under-explored, which is in our future work"* (no λ
schedule, no formula) — are candidate levers for the EX gap, both isolated to
KID only (RKD untouched by either):

1. **Mask-token choice** (`fedicl_sql/training/imperfect.py:43`,
   `mask_token_id = tokenizer.pad_token_id`) — verified Qwen2.5-1.5B's
   pad_token_id (151643, `<|endoftext|>`) is distinct from eos (151645,
   `<|im_end|>`), so not an eos-collision bug, but still a semantically-loaded
   special token substituted mid-sequence, unlike anything in the base
   model's pretrain distribution. Causal LMs have no true `[MASK]` — the
   paper doesn't pin a substitute either.
2. **λ_ft:λ_kd = 1:1 static weighting** (`lora_trainer.py` `LoraTrainConfig`)
   — applied identically to both arms so it can't bias one over the other by
   itself, but RKD's clean-target signal and KID's noisy-target signal may
   simply want different ratios; paper gives zero guidance to pick one over
   the other.

### Read for the paper

Two-axis story, not a single pass/fail: **RKD wins accuracy** (ships as the
headline arm per raw EX at every condition tested) — **KID wins robustness**
(smaller ICL-sensitivity delta, worth reporting as a §5 analysis finding
regardless of which direction ships, ties directly into the gated-ICL
narrative: an arm's inherent robustness to prompt content changes how much a
gate is even needed).

### Next

- [ ] Decide RKD ships as the server-distill direction (§8/§9) — pending
      advisor sign-off; KID's robustness finding still worth a §5 sentence
      either way
- [ ] Second seed (both `central_rkd` + `central_kid`) before stating the EX
      gap as a firm number — pattern is consistent across 3 conditions but
      still 1 seed each
- [ ] Optional diagnostic (cheap): swap `mask_token_id` to a less
      semantically-loaded token, rerun `central_kid` 1 seed — check if the EX
      gap closes (candidate #1 above)
- [ ] Optional diagnostic: sweep `--rkl-skew-lambda` or a KID-only
      `--lambda-kd` on top of the existing skew-RKL code (§8.2) instead of
      assuming 1:1 (candidate #2 above)
- [ ] Flip §8.1 to killed (criterion met, −0.78 EX) + advisor note (carried
      over, still not done)
- [ ] (unchanged) A5 question-sim gap-fill; 2602.12275 + 2602.18749 novelty
      check; advisor sign-off items

## Session 2026-07-11 (3) — row-level gate audit + A5 question-sim lands; claims re-based on data; architecture updated

Full row-level pass over the prediction CSVs (all 8 gate arms + KD ladder +
the 2 new runs), not the aggregate metrics. Every number below recomputed
from `predictions/*.csv`, paired per `row_id`.

### New runs (A5 question-sim gap-fill, `central_rkd` adapter)

| run | arm | EX |
|---|---|---|
| `eval_arms__s0__20260711T121940` | `central_rkd_qsim_k3` (uniform) | 65.28 |
| `eval_arms__s0__20260711T122827` | `central_rkd_qsim_k3gate` (exec gate) | **70.79** |

### Finding 1 — the gate's "beats k=0" is mechanical, its real content is the repair rate

Verified on data: all 146 fired rows (`central_rkd`) have k0 EX = 0 (exec
error ⇒ wrong by definition), and every non-fired row's answer is identical
to the k0 run's. So **gate ≥ k0 by construction**; the empirical content is
`fire_rate × repair_rate` only (repair = 23/146 = 15.8%). Paper must frame it
this way — "wins 6/6 arms vs k0" is true but empty.

### Finding 2 — gate value vs uniform ICL is mostly *protection*, not repair

Decomposition (rows), all arms:

| arm | repair | protect | fallback also exec-fails | McNemar vs uniform |
|---|---|---|---|---|
| central_rkd | +23 | +47 | 106/146 (73%) | p=2.7e-06 |
| rkd_asym | +17 | +41 | 115/151 | p=9.3e-05 |
| ft_no_icl | +45 | +46 | 125/211 | p=1.4e-05 |
| ft_icl_k3 | +31 | +84 | 118/184 | p=1.8e-10 |
| 0.5b_ft | +34 | +79 | 240/313 (77%) | p=1.7e-10 |
| teacher | +17 | +19 | 16/41 | p=0.048 (borderline) |
| central_kid | +24 | +34 | 120/167 | p=9.2e-04 |
| gemma_ft | +31 | +16 | 113/166 | **p=0.12 n.s.** |

2/3 of the gate-vs-uniform delta = *not* showing demos to good drafts. The
ICL fallback itself fails to execute 68–77% of the times it is called.
**gemma breaks the universality**: uniform ICL is positive there (+1.35) and
gate-vs-uniform is not significant — "uniform ICL hurts FT models" is a
Qwen-family observation (consistent with the 2026-07-11 scope caveat).
Repairs also don't reach hard queries: central_rkd fired extra=45 → repaired
2, hard=32 → repaired 1; 88% of draft errors are `no such column`, demos fix
17/129 of those.

### Finding 3 — repair looks like perturbation, not demo-knowledge transfer 🔴

Same adapter, same 146 fired rows, three demo sets: dail repairs 23, qsim 26,
codes 17 — **only 6 rows repaired by all three** (union 44). Which rows get
repaired is nearly idiosyncratic to the demo set. Combined with Finding 2 and
qsim ≈ dail everywhere (uniform p=0.69, gated p=0.72), the working hypothesis
is now: **post-KD, ICL's repair effect is stochastic prompt perturbation**.
Attribution control = the A5 `random`-demos rung (one cheap run, decides
whether §5 says "ICL repairs" or "selective retry repairs").

### Finding 4 — KD ladder significance (paired McNemar, k=0)

- `rkd − ft` = +6.09 EX: 107 vs 44 discordant, **p=3.1e-07 — solid**. The KD
  signal is the paper's backbone; federation build is justified.
- `rkd − kid` = −1.45 EX: 38 vs 23, **p=0.072 — NOT significant at 1 seed**.
  The earlier "consistent across 3 conditions ⇒ not noise" argument is weak
  (same adapters, same test set — conditions aren't independent). RKD stays
  the provisional direction; seed 2 required before it's a paper number.
- Stack noise floor measured: 17/146 fired rows produce different greedy
  output across runs with identical prompts (batching nondeterminism) —
  deltas under ~0.5pp are unreadable.

### Decisions / doc changes (`system_architecture.md`, this session)

1. §0 status: PoC marked complete; RKD provisional winner; federation = top
   priority (paper has zero federated numbers).
2. §1 novelty claim 3 reframed: DAIL-consistency → **ICL usage-policy
   contribution** (selective gate + retrieval-insensitivity + pool-quality
   analysis). Flagged for advisor sign-off (touches approved outline's RQ2).
3. §2/§6/§7: Phase 4 inference = **gated ICL** (k=0 draft → exec on local DB
   → k=3 fallback on error only); retrieval on fallback = question-sim
   default (simpler stack, equal EX, drops the broken-spacy dependency).
4. §5.4 + §9 + invariant #4: best measured config = train k=0 + gated
   inference; A2 reframed to `train-k0+gate` vs `train-k2 consistent`;
   invariant amended (gate = documented exception, not train/test mismatch);
   both honesty caveats (mechanical floor, unresolved attribution) written in.
5. §8.1 asym flipped to **KILLED** (−0.78 EX vs pre-registered +1 floor;
   advisor note still owed, informational).
6. SS retrieval **closed without running** (A5 convergence condition fired).
7. A5 table: 3/4 columns done; only `random` left (= attribution control).

### Next (priority order)

- [ ] Build federation: pick pool `P` (Spider held-out ~15% candidate,
      nothing in the data argues against it), generate K=8 α=0.5 split,
      FedAvg + server-distill loop → `fedavg` vs `fedkd` is the paper's
      make-or-break pair
- [ ] Seed 2 for `central_rkd` + `central_kid` (settles the −1.45 direction
      question) — cheap, run alongside
- [ ] A5 `random`-demos rung (uniform + gate, `central_rkd`) — attribution
      control for the whole gate story
- [ ] Advisor sign-off bundle: server-side pivot + novelty-claim-3 reframe +
      §8.1 kill note + RKD provisional pick
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check

## Session 2026-07-11 (4) — A5 random rung lands: attribution settled, gate renamed verifier-gated retry

### New runs (`central_rkd` adapter, seed 0)

| run | arm | EX |
|---|---|---|
| `eval_arms__s0__20260711T133139` | `central_rkd_random_k3` (uniform) | 66.83 |
| `eval_arms__s0__20260711T134219` | `central_rkd_random_k3gate` (exec gate) | 70.41 |

### A5 thang COMPLETE 4/4 — full table (same adapter, same 146 fired rows)

| retrieval | uniform k3 | gate exec | repairs |
|---|---|---|---|
| random | 66.83 | 70.41 | 22/146 |
| question-sim | 65.28 | 70.79 | 26/146 |
| dail_select | 65.86 | 70.50 | 23/146 |
| codes | — | 69.92 | 17/146 |

### Findings

1. **Attribution settled: repair = prompt perturbation + execution verify,
   NOT demo content.** Random demos from unrelated DBs repair broken drafts
   exactly as well as DAIL-selected demos (22 vs 23 repairs, McNemar p=1.00).
   Gate spread across all 4 demo sets = 0.87pp (noise floor ~0.5pp). This was
   the open control since session (3) — it ran, it decided.
2. **Repair sets nearly disjoint:** pairwise overlap 9–11 rows, all-4 common
   only 5, union 50/146 (34%). Which rows get repaired is idiosyncratic to
   the demo set — consistent with stochastic perturbation, and it motivates
   a multi-retry gate (ceiling ≈ union ≈ oracle 73.0 EX, +4.8pp vs k0).
3. **Inverse-relevance trend at uniform (not significant, mechanism-consistent):**
   damage grows with demo relevance — breaks: random 58 < DAIL 74 < qsim 83
   (uniform random 66.83 > DAIL 65.86 > qsim 65.28, random-vs-DAIL p=0.40).
   Better selection provides zero protection and possibly more temptation to
   copy.
4. **Answers to the session's three questions:** (a) yes — all selection
   methods measurably equal on a FT/KD student, both usage modes; (b) ICL
   contributes nothing *as knowledge* post-FT/KD (Qwen/Spider/1-seed scope;
   base + teacher models still benefit from selection); (c) the exec gate is
   NOT random — +2.1–2.2pp reproduced across 4 demo sets, deterministic fired
   set, p<1e-5 vs uniform — but its mechanism is execution verification +
   perturbed retry, so it is renamed **verifier-gated retry**; ICL is just
   the perturbation medium.

### Doc changes (`system_architecture.md`)

- §1 claim 3 re-reframed (2nd time today): "selective-ICL usage policy" →
  **verifier-gated retry** + demo-content-doesn't-matter finding; advisor
  sign-off flag kept.
- §5.2 status block: full 4/4 A5 table + attribution verdict + consequences
  (fallback retrieval = anything cheap; static cached demos make the client
  retrieval stack optional; DAIL's remaining home = teacher-side ICL in
  server distill; multi-retry motivation).
- §5.4 caveat (b) flipped to RESOLVED.
- §10 A5 row: DONE 4/4, no further runs; ships as the §5 table.
- §9 k_teacher: ablate 0 first (teacher-ICL value = the one live ICL question).
- Tier 3 += multi-retry gate (1 eval run) + static-demos gate (1 run).

### ICL direction going forward (decided this session)

- Paper §5: lead with "demo content stops mattering post-FT/KD" (thang +
  disjoint repairs + inverse trend), then verifier-gated retry as the cheap
  test-time-verification overlay (CSC-SQL cited as the expensive relative).
- Framework: the only place ICL can still earn its name = **teacher-side ICL
  during server distillation** (k_teacher 3-vs-0 ablation, priority when
  federation is built). Context distillation (2602.12275) stays a gated
  novelty-check item, opened only if teacher-ICL shows signal.
- Cheap Tier-3 runs queued: multi-retry gate, static-demos gate.

### Next

- [ ] (top, unchanged) federation build: pool `P` probe + FedAvg +
      server-distill RKD → `fedavg` vs `fedkd`
- [ ] Seed 2 rkd/kid; coder-base student PoC rerun (v2 proposal §build-order)
- [ ] Tier-3 quickies when GPU idle: multi-retry gate, static-demos gate
- [ ] Advisor bundle: pivot + claim-3 (now verifier-gated retry) + §8.1 kill +
      RKD pick + v2 proposal
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check

## Session 2026-07-12 — ICL selection thang extended to 4 base-model families: no regime found where selection sophistication pays

### New runs (uniform k3, base models, no gate) — 16 runs, seed 0

| family | k0 | dail | question | random | codes |
|---|---|---|---|---|---|
| qwen0.5B | 23.31 | 28.05 | 27.76 | 30.08 | 25.82 |
| qwen1.5B | 50.00 | 54.26 | 50.77 | 53.58 | 52.13 |
| gemma-2-2b | 52.22 | 50.77 | 47.78 | 49.52 | 50.97 |
| llama-3.2-1b | 37.33 | 35.01 | 30.46 | 35.69 | 37.23 |

### Findings

1. **ICL's sign is a base-model-family property, not a method property.**
   Qwen (both sizes): every selection method net-positive vs k0, DAIL and
   random both significant. gemma + Llama: flat-to-negative across every
   method, question-sim significantly harmful on both (p=.002, p=1e-5).
   Mirrors (inverted) the FT-side family split already on record
   (gemma_ft +1.35 vs Qwen FT arms negative) — 4 families now confirm
   family idiosyncrasy dominates any general "ICL helps/hurts" claim.
2. **Selection sophistication doesn't pay even where ICL itself pays.**
   `dail vs random` McNemar never significant in any of the 4 families
   (p=0.20–0.70). On qwen0.5B — the family with the largest ICL gain
   (+49…+70 EX net) — **random (30.08) beats full DAIL (28.05)**. This
   closes the last place selection sophistication could have mattered (the
   2026-07-11 doc note "DAIL stays relevant... base models (0.5B: DAIL
   28.05 vs codes 25.82)" is now stale — codes was the wrong comparison;
   random beats both).
3. **Question-sim is the worst-performing method, 3/4 families**, and the
   only one to land significantly *harmful* on two of them. Mechanism read:
   pure question-similarity retrieves near-duplicate questions from other
   schemas — maximal schema-bleed exposure — whereas random's dissimilarity
   is easier for the model to discount.
4. **Combined with the 2026-07-11 post-FT/KD result: no regime found across
   the whole project where demo-selection sophistication measurably pays** —
   not uniform, not gated, not FT/KD, not base, across 4 model families and
   2 usage policies. The only remaining open question is teacher-side ICL
   during server distillation (soft-label regime, not yet tested) — and even
   there the prior is now low: the teacher's own uniform-ICL eval already
   shows k3 ≈ k0 (78.53 vs 78.72, session 2026-07-08).

### Doc changes (`system_architecture.md`)

- §5.2: added the 2026-07-12 extension block (4-family table + both
  findings) superseding the stale 2026-07-11 "DAIL stays relevant... base
  models" line; consequences rewritten — no surviving regime for selection
  sophistication; `teacher-k3 vs k0` ablation reframed as low-prior-but-still-
  worth-running (soft-label regime differs from greedy generation).

### Next

- [ ] (top, unchanged) federation build: pool `P` probe + FedAvg +
      server-distill RKD → `fedavg` vs `fedkd`
- [ ] Seed 2 rkd/kid; coder-base student PoC rerun (v2 proposal §build-order)
- [ ] Tier-3 quickies when GPU idle: multi-retry gate, static-demos gate
- [ ] `teacher-k3 vs k0` distill ablation once federation is built — expect
      null, run for completeness
- [ ] Advisor bundle: pivot + claim-3 (verifier-gated retry, now backed by
      4-family base evidence too) + §8.1 kill + RKD pick + v2 proposal
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check

## Session 2026-07-12 (2) — ICL theory research; policy locked 3 tầng; KD+ICL roadmap; probe P staged

### Research pass: vì sao mình thấy khác lit (chi tiết: `icl_methods_survey.md` §6 mới)

- **TR vs TL** (Pan 2305.09731): student 0.5–2B = task-recognition regime —
  demos chỉ scaffold format, selection không thể giúp; thang selection của
  lit toàn đo trên GPT-4/Claude/Codex (TL-capable). random ≈ DAIL của mình =
  dự đoán của theory, không phải anomaly.
- **Min 2202.12837**: demo đúng/sai gần như không đổi kết quả ICL — khớp
  random > DAIL trên 0.5B base + question-sim tệ nhất (near-duplicate +
  schema sai = kênh copy độc nhất).
- **2602.23197** (02/2026): chứng minh FT zero-shot-loss làm suy giảm ICL
  (linear attention); lối ra: value-only FT hoặc auxiliary few-shot loss.
  Random-k injection mặc định của `build_examples` = dạng aux-loss →
  `ft_icl_k3` đọc lại là tín hiệu yếu ủng hộ (k0 floor +1.8, gate +7.93).
- **Chính [9] đã thấy hiện tượng**: *"after fine-tuning we also observe a
  decrease in in-context learning capability, which requires further study"*
  — §5 của mình là further study đó. Mở §5 bằng quote này.

### Quyết định — ICL policy 3 tầng (chốt, chờ advisor bundle)

client training k=0 · client inference = verifier-gated retry (fallback
question-sim) · teacher distill context = DAIL k_teacher=3, ablate 0.
Selection method KHÔNG phải contribution; §5 analysis + usage policy là.
Nếu k_teacher 0 ≈ 3 → tên "Fed-ICKD" chỉ còn chống bằng inference policy —
đưa câu hỏi đổi tên vào advisor bundle.

### Roadmap KD+ICL (queue, thứ tự cứng)

1. Probe P (SynSQL 1k vs Spider-1k control) — staged xong session này
2. PoC rerun trên Qwen2.5-Coder-1.5B (chốt student trước federation)
3. Split K=8 α=0.5 + FedAvg + server-distill → `fedavg` vs `fedkd_rkd` (sống còn)
4. `k_teacher 3-vs-0` (gắn vào bước 3)
5. Seed 2 rkd/kid (nền)
6. `fedkd_onpolicy` → `+exec-filter` (v2 §V2-1/2)
7. Tier-3 rẻ: multi-retry gate · static-demos gate · Spider-Realistic §5 ·
   (opt) LoRA value-only ablation (2602.23197)
Cắt nếu thiếu thời gian: 6–7. Không bao giờ cắt 3.

### Probe P staged (code repo) — v1 broken, fixed same day

- **new** `scripts/build_synsql_probe.py` — v1 dùng
  `datasets.load_dataset("seeklhy/SynSQL-2.5M", streaming=True)` không
  `data_files=` → **chạy trên compute host báo lỗi**
  (`ArrowInvalid: JSON parse error... databases.zip::.../*.sqlite`): HF loader
  glob cả 3 file của repo (`data.json` 9.36GB, `tables.json` 307MB,
  `databases.zip` 54.5MB) vào chung 1 JSON builder, cố parse từng `.sqlite`
  trong zip như JSON.
  **Root cause + fix** (đối chiếu `train_and_evaluate/process_dataset.py`
  của chính OmniSQL/SynSQL trên GitHub): SynSQL-2.5M không phải
  `datasets`-loadable split — `data.json` là 1 JSON array lớn (field thật:
  `question`, `sql`/`query`, `db_id`, `cot`, không có field DDL sẵn),
  `databases.zip` chứa SQLite thật tại `databases/<db_id>/<db_id>.sqlite`.
  Viết lại: `huggingface_hub.hf_hub_download` tải riêng `data.json` +
  `databases.zip`; stream `data.json` bằng `ijson` (thêm dep `ijson>=3.3`
  vào `pyproject.toml`) + **reservoir sampling** (Algorithm R, constant
  memory, không cần giữ 2.5M record) lấy 1k; `db_path` trỏ thẳng SQLite
  **thật** đã extract (không phải DB rỗng như v1 — sẵn sàng cho bước
  exec-filter distill sau này luôn, khỏi làm lại). + control slice 1k từ
  Spider centralized train (cùng seed, không đổi). Smoke-tested local
  (reservoir algorithm + zip-extract layout `databases/<id>/<id>.sqlite`).
  Chưa test full path với network thật (data.json 9.36GB) — chạy trên
  compute host sẽ lộ nếu field name suy đoán (`sql`/`query`/`SQL`) sai; script
  in ra `columns: question=... sql=... complexity=...` dòng đầu để soi ngay.
- `notebooks/kd/README.md` §6 — lệnh chạy KHÔNG đổi (vẫn 3 bước: build →
  2× train → 1 eval chung); read-off pre-registered: pass nếu
  `synsql1k ≥ 50.00` (base floor) và `spider1k − synsql1k ≤ ~5 EX`; fail →
  P = Spider held-out 15%.

### Docs touched

`icl_methods_survey.md` (§3 bảng nội bộ đủ 4 cột + §6 theory + 5 refs mới) ·
`notebooks/kd/README.md` (§6 probe) · `scripts/build_synsql_probe.py` (new) ·
`system_architecture.md` §5.2 đã có block 4-family từ session trước (user).

### Next

- [ ] Chạy probe P trên compute host (runbook §6) → verdict pool
- [ ] (queue #2) PoC rerun Coder-1.5B
- [ ] Advisor bundle (giờ gồm cả policy 3 tầng + câu hỏi tên Fed-ICKD)
- [ ] (unchanged) 2602.12275 + 2602.18749 novelty check

## Session 2026-07-12 — pool `P` DECIDED: BIRD train (user); ICL research pass anchored in theory

### Decision — `P` = BIRD train (user, 2026-07-12)

Reverses the 2026-07-07 BIRD drop **for the pool-`P` role only** (BIRD stays
dropped as an eval benchmark). Rationale: ~9.4k train questions ≈ Spider's
8.7k — right-sized for a distillation pool, human-curated, real executable
SQLite DBs (satisfies the v2 exec-filter precondition), distribution-disjoint
from client data, reviewer-familiar. Chosen over the v2 proposal's SynSQL-2.5M
subset (judged overkill); SynSQL demoted to fallback + A3 ablation candidate.

Caveats carried from the 07-07 drop, mitigated by the narrower role:
multi-GB train_databases download (once, host, train split only); `evidence`
field handling = single declared config choice, never mixed in a comparison;
dialect gap acceptable for a distill corpus. **Mandatory kill-switch before
any distill build: E0.1 probe** (1k BIRD-gold SFT from base → eval Spider
dev; if the Spider floor drops → escalate, fallback Spider held-out / SynSQL).

Docs updated: `system_architecture.md` §0 / §2 diagram / §3.2 (rewritten with
decision + caveats + probe gate) / §9 config table / §10 A3 row;
`fed_ickd_v2_proposal.md` V2-3 rewritten + pipeline/build-order/risk rows +
stale lines fixed (random-rung status, P status).

### ICL research pass (same session, earlier) — why our phenomenon matches the lit

- **[9] DAIL-SQL itself observed it**: "after fine-tuning we also observe a
  decrease in in-context learning capability, which requires further study"
  (verbatim, their conclusions). Our §5 = that further study.
- **Theory**: TR-vs-TL (Pan et al. 2305.09731; Min et al. 2202.12837) — 0.5–1.5B
  students are in the task-recognition regime where demo *content* cannot
  matter (random ≈ selected is the predicted outcome); every lit selection
  ladder (DAIL/MARLO/SAFE/ODIS) was measured on TL-capable API-class models.
  **2602.23197** proves FT-on-zero-shot-loss structurally degrades ICL
  (linear-attention analysis) and suggests value-only FT + auxiliary few-shot
  loss as mitigations — our random-k `build_examples` default is close to the
  aux-loss recipe, and `ft_icl_k3`'s better k0 floor (64.02 vs 62.19) + best
  gate recovery (+7.93) reads as weak supporting evidence.
- **ICL policy for the paper (3 tiers, decided)**: client train k=0 · client
  inference = verifier-gated retry with question-sim fallback · teacher-side
  DAIL k_teacher=3 (ablate 0 — decides the "IC" in Fed-ICKD's name; advisor
  question flagged).
- Candidate extra runs (Tier-2/3): LoRA value-only ablation (theory check),
  multi-retry gate, static-demos gate, Spider-Realistic for §5 claims.

### Consolidated run queue (KD + ICL, priority order)

1. E0.1 BIRD→Spider probe (kill-switch for `P`) — ~1–2h
2. Coder-1.5B student PoC rerun (`ft`/`rkd` + k0/gate evals) — ~half day
3. **K=8 α=0.5 split + FedAvg + server-distill → `fedavg` vs `fedkd_rkd`** —
   the paper's first federated numbers (make-or-break)
4. `k_teacher` 3-vs-0 (rides along step 3)
5. Seed 2 `central_rkd`/`central_kid` (background)
6. v2 arms: `fedkd_onpolicy` → `+exec_filter`
7. Tier-3 cheap: multi-retry gate, static-demos gate, Spider-Realistic, (opt)
   LoRA value-only

Parallel, no GPU: write §2/§5, redraw Fig. 1, send advisor bundle (pivot +
RKD pick + claim-3 reframe + §8.1 kill + v2 proposal + BIRD-P decision +
Fed-ICKD naming question).

### Next

- [ ] E0.1 BIRD probe on compute host (blocks distill build)
- [ ] Download BIRD train split (once, host)
- [ ] (queue above, in order)
- [ ] Advisor bundle — now includes the BIRD-P reversal (advisor saw the
      07-07 drop rationale; the reversal needs their eyes too)

## Session 2026-07-12 (2) — BIRD evidence/description handling decided + implemented

### Decision

Both dropped from every prompt on `P` (BIRD train): `evidence` (per-question
hint string BIRD ships) and `database_description/*.csv` (per-column meaning
files BIRD ships, separate from the sqlite DBs). Not laziness — clients
train/deploy on Spider (neither field exists there), and `build_prompt`
already renders schema DDL straight from sqlite for both datasets. Dropping
both on `P` keeps the distilled global student's prompt format identical to
what it deploys on at the client — the alternative (include on `P` only)
reintroduces the exact train/inference mismatch invariant #9 forbids, just
moved to the server side.

### Implemented (`fedicl-sql/`)

- `fedicl_sql/data/spider.py` — `SpiderExample.evidence: str = ""` (trailing
  default, backward-compatible with every existing positional 4-arg call
  site — verified: full suite still 189/189 green).
- `fedicl_sql/data/bird.py` — `load_bird` now captures `row.get("evidence", "")`
  onto the example; docstring points at spider.py for why it's unused.
- `tests/test_bird_data.py` — both tests assert the field (captured with a
  real string in one, defaulted `""` when absent in the other) — makes the
  "captured but never read by the prompt builder" contract a tested fact,
  not an accident that could silently reverse.
- `processed_data/BIRD/{raw,centralized}/*.csv` rebuilt via
  `build_processed_bird.py` — new `evidence` column present (9,428 train /
  1,534 dev rows). `database_description/*.csv` left untouched, not wired
  anywhere — `schema_style=full` DDL-only stays the schema source for BIRD,
  same as Spider.

### Known risk, flagged not fixed

RKD/KID teacher-force-score gold BIRD SQL (`score_logits`) — BIRD columns are
often cryptic and some gold queries are only decidable given `evidence`
(enum/threshold definitions the schema alone doesn't state). Without it the
teacher may assign low probability to gold tokens it can't justify, injecting
noisy RKL signal specifically at those positions. Client CE is unaffected
(never sees BIRD). **Escalation path if `fedkd_bird` underperforms
suspiciously:** reuse the asymmetric-context KD machinery already built for
§8.1 (`teacher_prompt_ids`, `rkl_asym_loss` — killed for its original
k-mismatch purpose, plumbing is generic) to score the teacher on an
evidence-augmented prompt while the student-facing target prompt on `P` stays
evidence-free. Not built now — only pull this lever if the E0.1 probe or
early distill numbers actually implicate evidence.

### Docs updated

`system_architecture.md` §3.2 — evidence/description caveat rewritten from
"pick one, TBD" to the decided-and-implemented policy + the risk/escalation
paragraph above.

### Next

- [ ] (top, unchanged) E0.1 BIRD→Spider probe — the real test of whether
      dropping evidence (among other gaps) hurts transfer
- [ ] (unchanged) rest of the federation build queue from session (1)

## Session 2026-07-12 (3) — dropped the client-ICL-policy invariant (over-rigid)

User call: §11's former #4 ("client ICL usage policy declared, not mixed" —
hard-forbade uniform eval-time ICL on a k=0-trained model) was too rigid — it
literally forbade the exact configuration A2/A5/`*_k3dail` runs already use
on purpose, which is where §5's findings come from. A "never violate" rule
is the wrong container for something a future run can overturn.

**Removed** from §11 (was #4), list renumbered 1–7 (old 5→4 ... 8→7). The
underlying observation is unaffected — it stays exactly where it already
lived, §5.4, tagged "hypothesis, not established," which is the correct
epistemic status. Fixed 3 now-dangling cross-references: §3.2's evidence-drop
rationale (reworded from "invariant forbids" to "design default, itself
open to a future ablation"), §8.1's asym-KD note (reworded, no invariant
citation needed — it was just a factual observation about that variant).

Reviewed the other 7 invariants for the same rigidity problem — none qualify:
1/2 (privacy: raw data/teacher never touch each other) are structural, not
research choices. 4/5 (demo pool ≠ test set; `P` DB-disjoint from
clients+eval) are anti-contamination rules tied to eval integrity (5's LOO
leak already burned the project once, 2026-06-18) — same category as "don't
peek at the test set," not a methodology preference. 6/7 (seeded splits +
provenance; one stack per comparison) are bookkeeping hygiene, block nothing.
#3 (KD loss = reverse KL, never forward/relational) is a build decision with
a documented rationale (the 07-08 pivot) and doesn't currently forbid any
planned run — left as-is, flagged as the next candidate to revisit if it
ever blocks a real ablation the same way #4 did.

### Next

- [ ] (unchanged) rest of the federation build queue

## Session 2026-07-12 (4) — BIRD evidence escalation revised: CE-poisoning risk recorded, filter-first ladder

### What changed

Architecture-review pass on the BIRD evidence/description decision (session (2)
above) found the recorded risk **understated**: on evidence-dependent rows of
`P`, dropping `evidence` exposes **both** server-distill loss terms, not just
the teacher's RKL scoring:

1. **RKL** (already recorded): teacher-forced `score_logits` on gold it can't
   justify → noisy gradient at exactly the evidence-dependent positions.
2. **CE (`λ_ft·CE(y_pub)`) — new, previously unrecorded:** the distill CE
   trains the global student to emit gold SQL underivable from its own prompt
   (enum/threshold literals, cryptic columns) = hallucination training, taken
   every round. Client CE unaffected (never sees BIRD).

This breaks the old escalation path: asym teacher-evidence (`rkl_asym_loss`
reuse) fixes RKL only and leaves CE poisoned.

### Decision — escalation ladder reordered (default unchanged: drop both)

`system_architecture.md` §3.2 rewritten:

- **D (first lever) — filter `P` by evidence-Δ scoring.** One offline teacher
  pass, `Δ = logprob_T(gold | prompt+evidence) − logprob_T(gold | prompt)`,
  2 teacher-forced forwards/row — same infra as the Phase-1 RKD logit cache
  (near-free if run in that pass). Keep low-Δ rows for the distill subset
  (§3.2 only needs a few hundred–few thousand of 9.4k). Fixes CE **and** RKL,
  keeps KD symmetric (offline cache valid). The Δ histogram doubles as a
  quantitative "fraction of BIRD that is evidence-dependent" number feeding
  the A3 pool-quality analysis — part of the contribution, not a patch.
  `evidence` column already in `processed_data/BIRD/*.csv` (session (2)).
- **B (second) — asym teacher-evidence** (§8.1 plumbing): only if filtering
  isn't enough; caveats recorded (RKL-only fix; evidence-confident teacher
  pulls the student toward ungroundable tokens).
- **C (last resort) — evidence in both prompts on `P`:** controlled
  A3-adjacent ablation only, never a silent default (server-side rerun of the
  −30-flip train/inference-mismatch failure class).

**`database_description/*.csv`: dropped permanently, no escalation** — wiring
it = a new `schema_style` no adapter ever trained on (config audit 07-10:
0/21 runs); separate costly axis, and `evidence` carries most of the
gold-decidability information.

Nothing built — E0.1 probe stays the gate. D's Δ-scoring may run
opportunistically inside the Phase-1 cache pass even if the probe passes
(near-zero marginal cost, feeds A3).

### Next

- [ ] (top, unchanged) E0.1 BIRD→Spider probe on compute host
- [ ] When building Phase-1 logit cache: run evidence-Δ scoring in the same
      pass → Δ histogram for A3
- [ ] (unchanged) rest of the federation build queue from session (1)

## Session 2026-07-12 (5) — SynSQL removed entirely (user decision); real `load_csv` bug found + fixed

### What changed

**SynSQL-2.5M dropped completely** (user decision) — it was only ever a
fallback-pool candidate for `P`, superseded 2026-07-12 by BIRD, and had never
been run (§V2-3, LAB_LOG session (1)). Removed: `fedicl-sql/scripts/
build_synsql_probe.py` (dead code, unused since BIRD decided); every SynSQL
mention in `system_architecture.md` §3.2, `fed_ickd_v2_proposal.md` (V2-3
title/body, risk table, references list), and `notebooks/kd/README.md` §6's
escalation line. Fallback for a failed E0.1 probe is now **Spider held-out
15% only** — no second fallback candidate. Historical LAB_LOG entries
(session (1) above) are left untouched per convention (session log, not a
live doc); this entry is the record of the removal, not a rewrite of that one.

### Also found + fixed (while building §6/§7/§8 of the runbook)

**Real bug in `fedicl_sql/data/spider.py::load_csv`**, introduced when
`evidence: str = ""` was added to `SpiderExample` (session (2) above):
`load_csv` built each row via `row[k] for k in _CSV_FIELDS` (hard KeyError on
any missing column) instead of tolerating the dataclass default — every
Spider CSV predates the `evidence` column, so **any run reading a Spider CSV
through `load_csv` would crash** (`experiments/client_train/run.py`,
`experiments/eval_arms/run.py`, `experiments/sanity/run.py`,
`scripts/build_retrieval_cache.py`, `fedicl_sql/retrieval/pool.py` — every
one of them). Not caught by the 189/189 "green" claim in session (2) because
no test exercised `load_csv` against an old-format Spider CSV. Fixed:
`{k: row[k] for k in _CSV_FIELDS if k in row}` — missing columns fall back to
the dataclass default. Verified 189/189 still pass after the fix.

**New:** `scripts/build_e01_probe.py` — builds the E0.1 probe's two 1k slices
(BIRD + Spider control, paired seed) via the existing `load_csv`/
`examples_to_csv`, replacing the dead SynSQL probe script for that role.
`notebooks/kd/README.md` gained real §6 (E0.1 probe)/§7 (Coder-1.5B student
rerun)/§8 (seed 2 rkd/kid) — the old §6 pointer in LAB_LOG session (1) never
actually existed in the file; it does now.

### Next

- [ ] `git push` the `load_csv` fix + new script + K=8 α=0.5 split before
      anyone runs client_train/eval_arms on the A5000 host — the bug blocks
      every Spider-CSV run until pulled
- [ ] (top, unchanged) E0.1 BIRD→Spider probe on compute host (§6 runbook)
- [ ] (unchanged) Coder-1.5B student rerun (§7) before the federation build
- [ ] (unchanged) rest of the federation build queue from session (1)

## Session 2026-07-12 (6) — v2 proposal merged into system_architecture.md (V2-1/V2-2, pending sign-off); `fedavg_pub` control restored to §10

### What changed

Reviewed `fed_ickd_v2_proposal.md`'s two still-draft items (V2-3/pool=BIRD was
already merged 2026-07-12) and merged both:

- **V2-1 on-policy distillation → §8.3.** Verdict: sound — reuses
  `train_online_kd`'s existing teacher co-load/RKL/skew-RKL, one trainer
  change (student samples the full target instead of KID's mask-rewrite),
  and directly tests the leading hypothesis for `kid − rkd` = −1.45 EX (the
  `pad_token_id` mask substitution as an out-of-distribution artifact).
- **V2-2 execution-anchored server distillation → §8.4.** Verdict: sound and
  higher-priority novelty-wise — reuses the SQLite exec + 60s timeout already
  in `eval/metrics.py`, no RL/reward model, and is the strongest available
  differentiator vs FedCoLLM [8] (blind public-data distill vs a cheap
  per-sample verifier). Noted it does **not** strictly require V2-1 — KID's
  existing masked-splice `ŷ` can be exec-filtered too; on-policy + exec-filter
  combined (`fedkd_onpolicy_exec`) is the strongest arm, not a hard
  dependency chain.

Both merged as **PROPOSED, Tier 2, pending advisor sign-off** (scope change
vs the approved outline — same gate as §8.1/§8.2's Tier-2/3 items) — not
built, not Tier 1, ordered strictly after the `fedavg`/`fedkd` headline pair
in §10's new "Federated v2 extension arms" table.

**Also fixed while touching §10's Tier-1 table:** `fedavg_pub` control was
locked back in session 2026-07-06 ("`fedkd − fedavg` confounded teacher with
extra public data") but never made it into the 2026-07-08 architecture
rewrite — restored as a Tier-1 row (FedAvg + CE-only on `P`, no teacher);
`fedkd − fedavg_pub` is the real teacher-value number, not `fedkd − fedavg`.

`fed_ickd_v2_proposal.md` header updated: MERGED (all 3 items now live in
`system_architecture.md`), file kept for historical rationale/lit citations
only — read the architecture doc for current status.

### Next

- [ ] (top, unchanged) E0.1 BIRD→Spider probe on compute host (§6 runbook)
- [ ] (unchanged) Coder-1.5B student rerun (§7) before the federation build
- [ ] Federation build now targets 3 Tier-1 arms (`fedavg`/`fedavg_pub`/
      `fedkd`), not 2 — one extra arm, same round-loop
- [ ] `fedkd_onpolicy`/`fedkd_onpolicy_exec` (§8.3/§8.4) — after the Tier-1
      ladder stands
- [x] Advisor bundle items resolved by user, see session (7) below

## Session 2026-07-12 (7) — all 8 advisor-bundle items locked by user, no advisor gate

### What changed

User reviewed the 8-item advisor bundle list and self-decided all of it —
no advisor sign-off remains outstanding on any currently-pending item:

1. **Server-side pivot** — confirmed.
2. **RKD** — locked as the server-distill direction. `system_architecture.md`
   §0 language changed "RKD provisional winner" → "RKD — locked". Caveat kept
   as an empirical to-do, not a gate: `rkd − kid` = −1.45 EX at p=0.072 (1
   seed, not significant) — seed 2 still needed before the *gap size* is a
   citable number, but the *pick* doesn't wait on it.
3. **Claim-3 reframe** (verifier-gated retry) — confirmed, §1.
4. **§8.1 asym-KD kill** — confirmed, closed. "Advisor note owed" language
   removed (it died before shipping, nothing to bring to advisor).
5. **BIRD-`P` reversal** — confirmed (already required no advisor gate,
   §3.2 — user's own decision).
6. **ICL policy 3 tiers** (client train k=0 · inference verifier-gated retry
   · teacher-distill DAIL k=3 ablate 0) — confirmed; already the doc's live
   default, no explicit gate existed to remove.
7. **Naming: "Fed-ICKD" stays"** regardless of the `k_teacher` 3-vs-0
   ablation result. New line in §0: ICL is reframed as an open experimental
   surface (try it wherever it plausibly helps — teacher-distill context,
   client fallback retrieval, other points as they surface) rather than a
   single ablation the paper's title depends on.
8. **V2-1 (on-policy distill, §8.3) / V2-2 (execution-anchored distill,
   §8.4)** — locked, not built. "Pending advisor sign-off" replaced with
   "locked (user, no advisor gate)" in both status banners and in §10's
   "Federated v2 extension arms" heading.

### Doc changes

`system_architecture.md`: §0 (RKD language, new naming note, new "no advisor
gate" summary line), §1 (claim-3 sentence), §8.1 (status banner + moot the
stale "needs advisor sign-off" order note), §8.3/§8.4 (status banners),
§10 (extension-arms heading). `fed_ickd_v2_proposal.md` banner updated to
"MERGED + LOCKED — user quyết, không cần advisor."

Grep-verified: no remaining `advisor` mention in `system_architecture.md`
implies an open gate — the only hits left are the confirmation lines
themselves.

### Next

- [ ] (top, unchanged) E0.1 BIRD→Spider probe on compute host (§6 runbook)
- [ ] (unchanged) Coder-1.5B student rerun (§7) before the federation build
- [ ] Federation build targets 3 Tier-1 arms (`fedavg`/`fedavg_pub`/`fedkd`)
- [ ] `fedkd_onpolicy`/`fedkd_onpolicy_exec` (§8.3/§8.4) after the Tier-1
      ladder stands — no longer sign-off-gated, just ordering
- [ ] Seed 2 `central_rkd`/`central_kid` — still needed for the `rkd − kid`
      gap-size number, unrelated to the (now resolved) direction pick

## Session 2026-07-12 (8) — E0.1 gap found: doesn't test KD on an already fine-tuned model; E0.1b added

### What changed

User question caught a real methodology gap: E0.1 (§3.2, `notebooks/kd/
README.md` §6) trains gold-CE **from base** — but the real server-distill
step runs **RKL-KD on top of an already fine-tuned/FedAvg'd student**
(`M_G`), not plain CE from base. Two untested confounds:

1. **Starting point** — base vs an already-Spider-specialized model. Whether
   BIRD-distribution noise interacts differently with an already-fine-tuned
   model (more forgetting-prone, or more anchored) is untested either way.
2. **Loss mechanism** — E0.1 only exercises the CE term. The RKL/teacher-scored
   term is completely untested by it — this is exactly half of the
   CE-poisoning risk already on record (session (4) above: both CE and RKL
   are exposed on evidence-dependent BIRD rows, E0.1 only probes CE).

E0.1 is still worth running as-is — cheap (~1-2h), catches severe
dialect/distribution mismatch fast — but passing it does **not** clear the
RKL/already-fine-tuned-model risk. Added **E0.1b**: RKL-KD on the same BIRD
1k slice, warm-started from `central_ft` (`--init-adapter`) instead of base.
Pre-registered read-off: pass iff `central_ft_bird1k_rkd − 62.19 ≥ −3 EX`
(tighter band than E0.1's ~5 EX — this tests the real mechanism, not just
raw data). Fail → pull the evidence-Δ filter (§3.2 lever D) before building
the federated loop, not just re-run E0.1's data-only check.

### Docs updated

`notebooks/kd/README.md` — new §6b (E0.1b, 2 commands, reuses `central_ft`
+ the §6 BIRD slice, no new data build). `system_architecture.md` §3.2 —
gate paragraph rewritten as two mandatory stages (E0.1 + E0.1b), explains
why E0.1 alone doesn't validate the production mechanism.

### Next

- [ ] (top, unchanged) E0.1 on compute host (§6) — gate for §6b
- [ ] E0.1b on compute host (§6b) — gate for the federation build, not just E0.1
- [ ] (unchanged) Coder-1.5B student rerun (§7) before the federation build
- [ ] (unchanged) rest of the federation build queue

## Session 2026-07-12 (9) — E0.1 result: FAIL, BIRD-CE regresses below the untrained floor

### Result (compute host, `git_sha` eaceddf, both n=1000, k=0, seed 0)

| arm | EX | EM | exec_errors |
|---|---|---|---|
| `bird1k_ft` | 47.10 | 19.83 | 274/1034 (26.5%) |
| `spider1k_ft` | 51.74 | 43.52 | 276/1034 (26.7%) |

**Read-off: FAIL.** `bird1k_ft ≥ 50.00` (base floor, 4-family table session 07-12)
fails outright — 47.10 is **below the untrained base model's own k=0 score**,
i.e. 1k rows of BIRD gold-CE actively regresses the model versus no training
at all. The paired gap sub-condition (`spider1k_ft − bird1k_ft ≤ ~5 EX` →
4.64) would pass alone, but the floor condition is the one that matters and
it fails clearly, not marginally.

**Not a sample-size artifact:** both arms trained on n=1000 / 1000 steps,
identical config except data source — the paired design already controls for
that. EX exec-error rates are nearly identical between arms (26.5% vs
26.7%) — **EX itself is trustworthy** (`score_ex_detail` is pure sqlite
execution, no dependency on the Spider-grammar parser). The verdict rests on
EX/the floor, not on EM.

**EM caveat (found 2026-07-12, user):** EM diverges by 23.7pp (19.83 vs
43.52), much larger than the 4.64pp EX gap — but `score_em` parses
*predicted* SQL through the vendored Spider-only grammar (`_vendor/spider/
process_sql.py::get_sql`), which chokes on BIRD SQL syntax (measured
separately: 84.7% parse-fail on a random 1k BIRD-train sample). `_parse_pred`
catches the exception and defaults to an empty parse → automatic EM=False.
`bird1k_ft`'s predictions (fine-tuned on BIRD-flavored SQL, even though
answering Spider-dev questions) plausibly trip this more often than
`spider1k_ft`'s, inflating part of the EM gap as a **parser-compatibility
artifact, not proven semantic wrongness**. Gold-side parsing is unaffected
here (both arms eval on the same Spider-dev `test.csv`, Spider-format gold —
the 84.7% failure rate was measured against BIRD *train* gold, a different,
non-eval set). Net: treat the 23.7pp EM number as upper-bound/noisy, not a
clean second signal — **lean on EX alone** for the FAIL verdict, which the
parser issue does not touch.

Reading (EX-only, revised): `bird1k_ft`'s SQL executes about as often as
`spider1k_ft`'s, but when it does execute it is wrong more often. This is
still consistent with the CE-poisoning mechanism already flagged
theoretically (session (4) above, §3.2): the model absorbing BIRD-specific
literal/pattern habits it can't justify from the Spider-style prompt. But
now stated on EX evidence alone. By-hardness breakdown is uneven, not a
uniform shift (medium −8.07pp, easy −4.03pp, hard actually +2.3pp) — another
signal against generic noise, consistent with a specific poisoned subset
rather than a blanket distribution shift.

### Decision — do not run E0.1b yet; escalate per §3.2's own order

§6b's contract ("run only after §6 passes") is honored — E0.1 failed, stop
there rather than layering RKL on top of an already-failing CE signal.
Per §3.2's pre-registered escalation order: **lever D (evidence-Δ filter)
before the Spider-held-out fallback.** Lever D is not built yet (flagged
session (4), still open) — that is now the actual next required step, not
an optional nice-to-have:

1. Build the evidence-Δ scorer (`Δ = logprob_T(gold|+evidence) −
   logprob_T(gold)`, one teacher pass per row — same infra as the Phase-1
   RKD logit cache).
2. Filter the BIRD 1k probe slice to low-Δ rows, re-run E0.1 (CE-only) on
   the filtered slice.
3. Filtered slice still fails floor → BIRD is out as `P`, fall back to
   Spider held-out ~15% (no advisor gate, straightforward switch per §3.2).
   Filtered slice passes → evidence-dependence confirmed as the mechanism,
   lever D is a real fix, proceed with BIRD (filtered) as `P`.

### Next

- [ ] Build evidence-Δ scorer (lever D, §3.2) — now blocking, not opportunistic
- [ ] Re-run E0.1 (CE-only) on the Δ-filtered BIRD slice
- [ ] E0.1b stays gated on a passing E0.1 (filtered or otherwise)
- [ ] If lever D fails too: switch `P` to Spider held-out ~15%, drop BIRD
- [ ] (unchanged) Coder-1.5B student rerun (§7) — independent of the `P` question

## Session 2026-07-12 (10) — lever D built: `scripts/score_evidence_delta.py`

### What changed

Built the evidence-Δ scorer flagged as blocking in session (9): teacher-forced
`Δ = logprob_T(gold | prompt+evidence) − logprob_T(gold | prompt)` per BIRD row
(`LocalHFTeacher.score_logits`, 2 forwards/row, same cost class as one RKD pass).
Writes a per-row Δ CSV and, optionally, a filtered `train.csv` keeping the
lowest-Δ `--keep-frac` (default 0.7) of rows — the escalation lever from §3.2.

- Evidence is injected into the scored prompt via a string insert
  (`### Hint: {evidence}` before `### SQL:`) since `build_prompt` has no
  evidence param by design (§3.2) — this script is diagnostic-only, doesn't
  change what the real pipeline ever prompts with.
- Tokenization mirrors `training/dataset.py::_assemble`'s chat-template
  convention (inlined, not imported — that function is private and this
  script's needs are simpler: no weights/skeleton, no KD-example dataclass).
- 189/189 tests still pass (script adds no new import cycles); `--help`
  sanity-checked on Mac (no GPU needed to verify wiring).

`notebooks/kd/README.md` gained §6c (the lever-D runbook: score → filter →
re-run E0.1 on the filtered slice) between §6 (now has its real FAIL result
logged) and §6b (still gated on a passing E0.1).

### Next

- [ ] Push this + run §6c on compute host: score Δ, filter, re-run E0.1 on
      the filtered slice
- [ ] Filtered E0.1 pass → §6b on the filtered slice → BIRD (filtered) as `P`
- [ ] Filtered E0.1 fail → drop BIRD, `P` = Spider held-out ~15% (§3.2)
- [ ] (unchanged) Coder-1.5B student rerun (§7) — independent of the `P` question

## Session 2026-07-12 (11) — EM caveat on the E0.1 FAIL: parser-compatibility artifact, EX verdict unaffected

### What changed

User question (independently measured: `get_sql`/`process_sql.py` from
`_vendor/spider` parse-fails on 84.7% of a random 1k BIRD-train sample) —
does the Spider-only vendored parser explain session (9)'s E0.1 FAIL?

Read `fedicl_sql/eval/metrics.py` + `eval/loop.py` to answer precisely:

- **`score_ex_detail` (EX) has zero dependency on `get_sql`** — pure
  `sqlite3` execution + row comparison (`_execute`). The 47.10/51.74 EX
  numbers and the floor-breach FAIL verdict are **unaffected** by the parser
  issue.
- **`score_em` does depend on `get_sql`**, on both pred and gold sides.
  Gold-side is safe in E0.1's own run — both arms eval on the same
  `processed_data/SPIDER/centralized/test.csv` (Spider-format gold); the
  84.7% failure rate was measured against BIRD **train** gold, a different,
  non-eval set. **Pred-side is the real exposure**: `_parse_pred` catches
  parse exceptions and defaults to an empty parse → automatic EM=False.
  `bird1k_ft`'s predictions (fine-tuned on BIRD-flavored SQL syntax, even
  though answering Spider-dev questions) plausibly trip the Spider-only
  grammar more often than `spider1k_ft`'s — inflating part of the 23.7pp EM
  gap as a measurement artifact rather than proven semantic wrongness.
- Both `score_em` and `sql_hardness` are wrapped in per-row try/except at
  every call site in `eval/loop.py` — no crash risk in the standard eval
  path even when `get_sql` raises on BIRD-flavored SQL.

**Verdict:** E0.1's FAIL stands — it rests on EX/the 50.00 floor, which the
parser issue doesn't touch. The EM number (19.83 vs 43.52) should be read as
upper-bound/noisy for BIRD-trained arms, not cited as independent
corroboration the way session (9)'s original write-up did.

### Docs updated

`paper/notes/LAB_LOG.md` session (9) — EM paragraph rewritten in place (same
working day, direct factual correction) with the caveat + EX-only reading.
`notebooks/kd/README.md` §6 result note — same caveat, shorter.

### Next

- [ ] (unchanged) §6c on compute host: score Δ, filter, re-run E0.1 (EX
      read-off) on the filtered slice
- [ ] Latent bug noted, not urgent: `score_em`'s gold-side `_parse()` call
      (`metrics.py` line ~161) is unguarded *internally* — safe today because
      every real call site wraps it externally, but a future standalone
      script calling `score_em`/`sql_hardness` directly on BIRD gold (e.g. if
      `P` is ever scored for hardness diagnostics) should wrap it too

## Session 2026-07-12 (12) — FedEx-LoRA added as a candidate fix for the LoRA-averaging caveat

### What changed

Web research pass (triggered by the BIRD-P failure, scoped to "public pool P
for KD" but surfaced this as a bonus) found FedEx-LoRA (Singhal et al., ACL
2025, arXiv:2410.09432) — directly targets the LoRA-averaging caveat already
on record in §3.3 (`mean(BᵢAᵢ) ≠ mean(Bᵢ)·mean(Aᵢ)`), which was previously
only "mitigated" by re-init-from-aggregate + a one-sentence acknowledgment,
no actual fix. FedEx-LoRA's mechanism: adds a residual error term to the
frozen base weight matrix each round so the aggregated update is exact
(recovers `Σᵢ BᵢAᵢ`, not the mean-of-factors approximation), claimed minimal
compute/communication overhead, no architecture change.

Added to `system_architecture.md` §3.3 as a **Tier-2 candidate to try**
(distinct from FedProx, which fixes client-objective drift, not the
aggregation math) — gated on A4 (Dirichlet α sweep) actually showing the
averaging-inexactness gap costs real EX before spending the implementation
effort. Reference added to §14.

### Next

- [ ] (unchanged) decide BIRD-DB-with-synthetic-annotation (option B) vs
      Spider-held-out fallback (option A) for pool `P` — main open item
- [ ] FedEx-LoRA stays parked until A4 runs and shows a real gap
- [ ] (unchanged) rest of the federation build queue

## Session 2026-07-12 (13) — reframed the BIRD-P question; built + staged the execution-bootstrap probe (§6e)

### What changed

Research pass (user push-back: Spider is itself cross-domain, so "domain
mismatch" was the wrong frame; teacher must never see client data/schema —
constrains candidate fixes) corrected the diagnosis:

- **Spider's whole design point is cross-database generalization** — domain
  novelty is not what BIRD failed on. The real gap is **annotation
  convention** (SQL-writing style, question phrasing), not domain.
- **New, stronger data point:** a published benchmark-quality analysis found
  BIRD Mini-Dev is **52.8% annotation-error** (VLDB CIDR 2026, "Text-to-SQL
  Benchmarks are Broken"). This outranks the evidence-dependence hypothesis
  (§3.2 lever D, already tested and failed, session (9)-(11)) as the likely
  dominant cause of E0.1's floor breach — training CE on BIRD's own gold may
  simply be training on noisy/wrong labels at a high rate, unrelated to
  style or evidence.
- **Matching fix found in lit:** ExeSQL (arXiv:2505.17231) adapts a
  text-to-SQL model to a new SQL dialect **without any human-annotated
  target-dialect gold** — schema → self-generated questions → source-dialect
  model generates SQL candidates → execution-filter → self-train loop.
  Reports parity or better vs training on human-annotated cross-dialect
  data. Crucially: the teacher only ever touches the target schema, never
  client data — compatible with invariant #2 as-is.
- This reframes §8.3 (on-policy)/§8.4 (exec-anchored), already merged
  2026-07-12, from "nice-to-have upgrades" to **the literature-validated fix
  for exactly the failure just measured** — model-generated + execution-
  filtered targets are reported to beat fixed external gold specifically
  because they sidestep annotation-convention/quality mismatch.

### Built (before running anything on GPU)

`scripts/build_exec_bootstrap_probe.py` — drops BIRD's own gold SQL entirely.
Keeps the same probe_1k schemas+questions (directly comparable to §6/§6c).
Teacher (`StudentModel(model_id=teacher_model)`, no adapter, zero-shot,
k=0/no ICL) generates one SQL candidate per question via the existing
`generate_batch` (batched, OOM-safe, already does SQL cleaning); kept only if
`fedicl_sql.eval.metrics.executes()` passes. Output is a bootstrapped
`train.csv` in the same `SpiderExample` schema, re-runs through the identical
E0.1 CE-only train+eval commands for a same-floor comparison. 189/189 tests
pass; `--help` sanity-checked.

`notebooks/kd/README.md` — §6c gained its real result (FAIL, 46.7 EX, barely
moved from unfiltered — evidence-Δ filter confirmed NOT the fix); new §6e
runbook (bootstrap → train → eval, same 50.00 floor read-off).

### Next

- [ ] Push + run §6e on compute host: bootstrap, train, eval — read off vs
      50.00 floor
- [ ] Pass → BIRD annotation confirmed as root cause; build the real
      server-distill pipeline on §8.3/§8.4 (BIRD schemas/DBs only, never
      BIRD's own gold SQL)
- [ ] Fail → BIRD's schemas/DBs themselves are the problem, not just
      annotation — drop BIRD, `P` = Spider held-out ~15% (§3.2)
- [ ] §6b (RKL probe) stays gated behind a passing §6/§6c/§6e result
- [ ] (unchanged) Coder-1.5B student rerun (§7) — independent of the `P`
      question
- [ ] (unchanged) FedEx-LoRA parked until A4

## Session 2026-07-12 (14) — exec-bootstrap probe: timeout fix + checkpoint/resume

### What changed

Host run of §6e (`scripts/build_exec_bootstrap_probe.py`) measured ~312-400s
per 16-row batch — 63 batches × that rate ≈ 5.5-7h for a "cheap" 1k-row
diagnostic. Root cause: `executes()` (reused from `fedicl_sql.eval.metrics`)
hardcodes `TIMEOUT_SECONDS=60` (correct for real EX scoring, wrong for a bulk
exec-filter pass on zero-shot SQL against real BIRD DBs) — a handful of
cartesian-join queries per batch each eating the full 60s ceiling accounts
for the observed rate. Added a script-local `_quick_execute()` with
`--exec-timeout` (default 8s — a query that slow is garbage anyway, same
filtering spirit) and dropped `--max-new-tokens` 256→128. Caps worst-case at
~128s/batch instead of ~960s.

**Second gap found (user question):** the script had **no checkpoint/resume**
— a kill lost all progress, since results only wrote to the final CSV after
the whole loop finished. Direct violation of this repo's own CLAUDE.md rule
("MANDATORY for any loop that may take >30s: checkpoint/resume"). Fixed:
every row's result now appends to `<out>.ckpt.jsonl` immediately after
exec-scoring (flushed per row); a restart skips already-checkpointed
indices; the final CSV and reported stats rebuild from the full checkpoint
(all runs combined). Verified the checkpoint load/resume/overwrite logic
with a standalone unit test (fake JSONL, no GPU needed) — later lines win
per index, stats correct.

189/189 tests still pass after both fixes.

### Next

- [ ] Kill the stale host process (started before the timeout fix), pull,
      restart §6e with the checkpointed version — should now run in minutes,
      not hours, and survives interruption
- [ ] (unchanged) rest of the queue — §6e result decides BIRD's fate as `P`

## Session 2026-07-12 (15) — §6e result: PASS at the floor; BIRD-P question RESOLVED

### Result

| arm | EX | EM | exec_errors | n_train |
|---|---|---|---|---|
| `bird1k_ft` (BIRD gold, §6) | 47.10 | 19.83 | 274/1034 (26.5%) | 1000 |
| `bird1k_filtered_ft` (evidence-Δ, §6c) | 46.71 | 20.89 | 284/1034 (27.5%) | 700 |
| **`bird1k_bootstrap_ft` (exec-bootstrap, §6e)** | **50.00** | 22.44 | **212/1034 (20.5%)** | 831 |
| `spider1k_ft` (control) | 51.74 | 43.52 | 276/1034 (26.7%) | 1000 |
| base floor | 50.00 | — | — | — |

Exec-filter yield: 831/1000 teacher zero-shot generations executed on BIRD
schemas (8s timeout). `bird1k_bootstrap_ft` = 50.00 EX — **exactly at the
floor**, the read-off's pass condition (`≥ 50.00`) met, but by the thinnest
possible margin. Read carefully: this is "no longer actively harmful," not
"proven to add value" — it ties the untrained baseline rather than beating
it. The real value test is the federated `fedavg` vs `fedkd` numbers, not
this CE-only floor probe.

**Notable side effect:** exec_error rate (20.5%) is the **lowest of all 4
arms tested**, below even the Spider-CE control (26.7%) — training on
execution-verified targets appears to teach more executable-SQL habits
generally, not just fix the BIRD-specific problem. By-hardness:
`bird1k_bootstrap_ft` beats `spider1k_ft` on "hard" (36.21 vs 30.46), close
elsewhere.

### Decision — BIRD-P question RESOLVED

Root cause confirmed: BIRD's own gold-SQL annotation was the poison (not
evidence-dependence, session (9)-(11); not domain/dialect, session (13)'s
lit reframe + BIRD Mini-Dev's documented 52.8% annotation-error rate).

- **BIRD stays as `P`'s schema/DB source.**
- **BIRD's own (question, gold-SQL) pairs are permanently off-limits** for
  any CE or RKL target.
- **The server-distill step must build on §8.3 (on-policy) + §8.4
  (execution-anchored)** — already merged 2026-07-12, now empirically
  supported, not just literature-backed.
- **§6b (E0.1b, RKL probe on BIRD's native gold via `central_ft`) is
  retired** — its premise no longer applies.
- Spider-held-out-15% fallback is **not needed** — BIRD survives, under the
  new annotation rule.

### Docs updated

`system_architecture.md` §3.2 (rewritten: BIRD = schemas/DBs only, full
E0.1→lever-D→exec-bootstrap trace, rule stated), §9 (`Public pool P` row
updated). `notebooks/kd/README.md` §6e (result logged), §6b (marked
RETIRED, do-not-run banner added).

### Next

- [ ] Build the real server-distill step on §8.3/§8.4 (on-policy +
      execution-anchored), BIRD schemas/DBs only, as the next concrete
      federation-build task
- [ ] (unchanged) Coder-1.5B student rerun (§7) — independent, still open
- [ ] (unchanged) FedEx-LoRA parked until A4
- [ ] (unchanged) rest of the federation build queue from session (1)
