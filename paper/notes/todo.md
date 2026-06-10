# FedICL-SQL — TODO Checklist

Execution checklist, derived from `detailed_plan.md`. Mark `[x]` when done. Priority order top-down. 🔴 = blocks subsequent steps · ⭐ = make-or-break test for the project.

---

## P-1. Preparation (no GPU needed)

> **What:** Read the 4 core references, lock the 4 open design decisions (§8 plan), download datasets, secure compute.
> **Why:** [4] is our NL2SQL+ICL base, [5] the federated protocol we specialize, [7] the KD path. Decisions (variant / #clients / 2nd dataset / teacher access) gate every later phase — must settle before writing code. No GPU yet: pure reading + setup.

- [x] Read [4] Light-SQL (base single-client, same authors) → full read verified 2026-06-09 (plan "Reference grounding"); masking caveat extracted
- [x] Read [5] Fed-ICL §3 — Algorithm 1 (federated loop) → full read 2026-06-09; answer-fusion = baseline, §6.4 attack = F5a method
- [x] Skim [7] FedMKT (KD + MinED) → full read 2026-06-09; logit-space only, grounds P2 not engine ([8] FedCoLLM read too = engine anchor)
- [ ] 🔴 Confirm 4 decisions with supervisor (§8 plan): main variant (parametric teacher-KD), **clients = 3 + sweep {3,5,10}**, second dataset, teacher access. ⚠️ Decisions locked unilaterally so far — **supervisor sign-off is the Stage-B gate** (plan STAGING banner); must land before any paid spend, fine to run $0 PoC meanwhile
- [x] Download Spider (used by P0; local JSON + DBs working)
- [ ] Download Spider-Realistic (Tier-3, needed by Stage B T1 column — not a PoC blocker)
- [x] Compute secured for Stage A `[REV 2 2026-06-10]`: **teacher = Qwen2.5-72B paid API (DeepInfra, ~$2 cả bộ X)** + Kaggle/Colab free GPU for LoRA + M4 for FedAvg/eval (plan §8.4). Stage B chỉ còn nâng GPU (A100-class) sau gate — teacher giữ nguyên

---

## P0. Setup — single-client pipeline 🔴

> **What:** Build one working NL→SQL pipeline for a single client — no federation yet. SLM + retriever + prompt + eval, end-to-end.
> **Why:** Reproduces Light-SQL [4] as our floor and sanity check. Everything federated (P1+) is this pipeline run in a loop across clients, so it must work alone first. De-risks model loading, retrieval, and EX/EM scoring before adding complexity.

- [x] Repo as `fedicl_sql/` shared lib (subpkgs `data/ retrieval/ prompts/ models/ eval/ runtime/`) + per-experiment folders `experiments/<name>/run.py` + `scripts/`; uv env, hatchling, pytest (35 tests pass)
- [x] `data/spider.py`: `SpiderExample` dataclass, `db_to_ddl()` (sqlite_master), `load_spider()` (local JSON: train_spider+train_others merged = train; dev = validation), CSV helpers (`examples_to_csv`/`load_csv`)
- [x] `models/student.py`: `StudentModel` Phi-3-mini-4k-instruct, MPS float16 / CUDA 4-bit via `LOAD_IN_4BIT=1`; exposes `model_id`
- [x] `retrieval/retriever.py`: `DemoRetriever` — BAAI/bge-small-en-v1.5 + FAISS IndexFlatIP, cosine on L2-normalised
- [x] `prompts/builder.py`: `build_prompt()` σ(q,S,I,Q) Light-SQL structure
- [x] `eval/metrics.py`: `score_ex()` (sqlite result set), `score_em()` (sqlglot AST), `eval_batch()`
- [x] `runtime/results.py`: `save_results()` (enforces `model`/`time_average`/`gpu_vram`), `peak_vram_mb()`, `reset_peak_vram()`
- [x] `scripts/build_processed.py`: raw Spider JSON → `data/processed/centralized/{train,val,test}.csv` + meta.json (test=Spider dev FROZEN; val=seeded 10% slice of merged train). train=7793, val=866, test=1034
- [x] **Reproduce sanity:** `uv run python experiments/p0_sanity/run.py` (reads processed CSV) → EX=PASS, EM=PASS on Spider dev q "How many singers do we have?" (pred `SELECT count(*) FROM singer`). Fixed macOS faiss+torch duplicate-OpenMP SIGSEGV via `fedicl_sql/_ompfix.py` (2026-06-08)
- [x] Verify: `uv run python experiments/p0_eval50/run.py --n 50 --k 3` → **EX=80.0% (40/50), EM=48.0% (24/50)**, time_average=12.97 s/q, gpu_vram=9776 MB (Phi-3-mini, k=3, MPS, Spider dev, merged-train retrieval pool). Single-client floor established. Results: `experiments/p0_eval50/results/{summary.json,rows.csv}` (legacy pre-convention run kept as `p0_eval50.legacy.json`). Re-run on refactored code 2026-06-09 (was EX=78% on old 7000-only train pool) (2026-06-09)

---

## P1′ — Teacher-centric federated framework 🔴 ⭐

**Note:** P1 attempt-1 (cross-schema masked demo-store) was superseded 2026-06-09 — negative result, design error (shared *demos* not *answers*; masking misused; off-outline). Code deleted; findings archived at `fedicl-sql/docs/archive/p1-attempt1-cross-schema-demo-store/`. See plan REVISION banner for the full post-mortem.

> **What:** Re-anchor on the outline **and Fig. 1** (`fig1_architecture.md`): the federation engine is **parametric LLM-teacher → SLM-student knowledge distillation** — clients LoRA-train locally with SQL+KD+Structure+Exec loss, upload **weights only** (encrypted/compressed/DP-noised), server **FedAvg/FedProx**-aggregates into a **Global SLM** broadcast back. ICL (masking retrieval-only) serves RQ2 locally. Fed-ICL answer-fusion is only a parameter-free **baseline/variant**.
> **Why:** Fig. 1's aggregation engine = FedAvg/FedProx over SLM weights + Global SLM broadcast + on-client distillation losses → engine is **parametric**, not parameter-free demo-sharing. Outline weights teacher (3.3/3.5/3.7/3.8). FedCoLLM [8] anchors adapter-FedAvg; FedMKT [7] is reserved for later logit-KD/MinED. Avoids the schema-coupling wall attempt 1 hit.
> **✅ DIRECTION LOCKED 2026-06-09, RE-ALIGNED TO FIG.1:** parametric teacher-KD (LoRA + FedAvg) = primary engine; demo-level parameter-free KD + Fed-ICL fusion = variants/baselines; local ICL retrieval-only = RQ2. Clients evaluated on their **own schemas** (seen schema, unseen questions). Wire carries **weights only**, never data/schema/private demos.

**💰 SCOPE LOCKED 2026-06-10 REV 2 — P1′ = PoC ~$2 (plan STAGING banner).** Goal: pipeline works end-to-end + **directional** make-or-break signal. Config: **teacher = Qwen2.5-72B-Instruct thật (paid API — đúng model outline, dùng từ ngày 1, không còn thầy free tạm)**, Kaggle/Colab free GPU for LoRA, `L=3`, **1 seed**, eval subset (~200 q/client), `K=2–3` rounds, `E=1`, **no DP**. All results tagged `stage=poc` — never paper numbers (vì 1 seed + subset, không phải vì teacher). **Stage B = nâng GPU trả phí + ≥3 seeds + full tiers, gated on PoC-positive + supervisor sign-off; teacher targets dùng lại nguyên xi.**

**Reusable from attempt 1 (branch `p1-federated-sim`):** `prompts/masking.py` (→ retrieval-only use), `data/federated.py` (partition), `eval/`. **Attempt-1 code DELETED 2026-06-09** (`fedicl-sql/`): `federated/` (loop.py round-loop + aggregate.py demo-store-`G`), `experiments/p1_test_a1.py` + result json, `tests/test_loop.py` + `tests/test_aggregate.py`. Findings preserved at `docs/archive/p1-attempt1-cross-schema-demo-store/`. 35 tests pass post-clean.

- [x] 🔴 **Schema-disjoint split (anti-leakage):** partition Spider DBs into 3 pools — public `X` / client-private `{Sᵢ}` / held-out — with `schemas(X) ∩ private ∩ held-out = ∅`, no DB in two pools, eval Qs never in any train pool. Persist DB-id→pool, release it. → `fedicl_sql/data/federated.py::make_federated_split` (replaced attempt-1 `make_partition`) + `save_split`/`load_split`; CLI `scripts/build_federated.py` → `data/processed/federated/<L>c-a<α>-s<seed>/` (public_X.csv, client_{i}_{train,eval}.csv, held_out.csv, split.json, meta.json w/ db_pool_map). held-out = Spider dev. Real `3c-a1.0-s0`: **public X=29 DBs/1475 ex · clients=117 DBs (37/36/44) · held-out=20 DBs/1034 ex · disjoint OK**. 12 tests (`tests/test_federated_split.py`); full suite 39 pass. Spec+plan in `fedicl-sql/docs/superpowers/`. (2026-06-09)
- [x] Define **shared public NL→SQL set** `X` (public-schema Spider slice, disjoint from private+held-out) = teacher's KD-target medium + ICL-Hub demo source (Fig.1 ICL Hub) — never client-private → = `public_X` pool (default `public_frac=0.2` → 29 train DBs / 1475 ex), `public_X.csv`. Teacher-KD targets to be generated on it (next task). (2026-06-09)
- [ ] `models/`: server **LLM teacher** generates **SQL + reasoning steps (CoT)** on `X` `[RE-GROUNDED 2026-06-10 to Fig.1 duty #2 "Reasoning Guidance"]` — teacher target = **reasoning⊕SQL** (not SQL alone), exec-validated, cached → feeds **both** ICL-Hub demos + KD targets. **Teacher = Qwen2.5-72B-Instruct via paid API (cả PoC lẫn headline — REV 2 2026-06-10)**, DeepInfra primary (~$1–2 cả bộ X), wrapper provider-agnostic sẵn. Generate **once on `X` (~1475 ex), cache to `teacher_targets.csv`** (cols: question, db_id, db_path, gold, teacher_sql, reasoning, exec_ok, **exec_correct** — KD filters on exec_correct = **exec-match vs gold**, not mere executability; deployment story = exec-only fallback, own it in §3.7). Groq Llama-3.3-70B partial run giữ làm `teacher_targets.groq-llama33-70b.csv` (alt-teacher sensitivity, free).
- [ ] ⭐ **Parametric KD (primary, = Fig.1 engine, = FedCoLLM [8] for SQL):** client SLM LoRA-trains on **own private `Qᵢ` (supervised) + public `X` (teacher-KD)** — `L_i = L_sup(Qᵢ) + L_KD(X)`, `L_KD = SQL-CE + λ·KL(τ) + β·skeleton-CE` over **exec-filtered** teacher targets; upload **LoRA deltas only** (encrypted/compressed); server **FedAvg/SecureAvg** → **Global SLM `M_G`** broadcast. 🔴 **private-data term is mandatory** — train-on-`X`-only → identical deltas → FedAvg = single-client → RQ1 dies. NOTE: [8] anchor (adapter-FedAvg, clients have private data); **NOT FedMKT [7]** (logit-space, → P2). **`[RE-GROUNDED 2026-06-10 — Fig.1's 4 named losses, literal]`:** **SQL loss** = CE vs own gold (private `Qᵢ`) / vs teacher SQL (X); **KD loss** = **CoT distillation** — CE on teacher **reasoning⊕SQL** target (student learns the derivation, not just the answer; soft-logit KL→P2); **Structure loss** = skeleton-token CE (differentiable, weighted CE on clause/structural tokens — NOT AST-edit-distance); **Execution** = teacher-target **filtering**: **exec-match vs gold** in simulation (`exec_correct`; "runs"≠"right"), exec-only in deployment; non-differentiable → hard selection gate, not a gradient term — own the figure-vs-impl divergence in §3.7. Novelty = reasoning/CoT distillation + exec-filtering-in-fed-loop + skeleton loss (exec-guidance itself is prior art). (Soft-logit + MinED → P2.) **COMPUTE (locked 2026-06-10): trainer host-agnostic — real LoRA runs on FREE cloud GPU (Kaggle 30h/wk P100/2×T4 preferred, or Colab-free T4); M4 Mac MPS for tiny smoke tests only. FedAvg (delta averaging) + all eval run on Mac. Host = decide-later.**
- [ ] **Demo-level KD (variant, parameter-free):** teacher SQL on `X` → distilled into client SLM in-context (fine-tune-free) — cheap comparator to the parametric engine
- [ ] **ICL for RQ2 (local):** schema-aware retrieval, **masking retrieval-only**, demos same/related-schema, prompt shows **unmasked** demos — verify it beats zero-shot on *seen* schemas. ⚠️ caveat: in Light-SQL [4] masked-sim (37% EX) **< plain question-sim (41%)** — masking is a privacy/transfer lever, may **cost** accuracy; don't claim masking ↑ EX
- [ ] **Fed-ICL answer-fusion (baseline only):** clients answer shared queries; server fuses by execution-vote / Fusion-LM; iterate — parameter-free RQ1 comm-cost comparator (NOT in Fig.1; do not present as the method)
- [ ] **DP on weight updates → Stage B** `[RESTAGED 2026-06-10]`: preferred DP-SGD (Opacus) on LoRA; ⚠️ per-sample grads 2–3× memory, likely won't fit free T4 → fallback = Gaussian noise + clipping on aggregated per-client delta pre-upload (weaker guarantee — state which). PoC runs **no DP**; claim DP only with measured (ε, EX)
- [~] Federated partition: each client owns a Spider-DB partition (private schemas + example stores); eval = each client's **own-schema held-out questions**; public Spider-train slice = shared set `X` → **partition + per-client own-schema train/eval split DONE** in `make_federated_split` (Dirichlet(α) over private DBs, per-DB `train_frac=0.8`/eval); KD/training consumption pending. (2026-06-09)
- [ ] ⭐ **Make-or-break (PoC, directional), 4 arms `[+gold-CE arm 2026-06-10]`:** (1) **`M_G`** (full method) vs (2) **SLM-only** (own private data, no fed/teacher) vs (3) **X-only null** (single client trained on `X` only — FedAvg-no-op detector) vs (4) **gold-CE** (`L_sup(Qᵢ)` + CE on gold-X — same data as (1), labels swapped; early read on teacher-vs-gold risk, = Ablation 3 preview, +~2h GPU). Need: (1) > (2) and (1) > (3); watch (1) vs (4) — if gold-CE wins, teacher claim narrows to reasoning + unlabeled-X (plan §3.6 Ab3). **PoC standard: 1 seed, ~200 q/client subset, teacher Qwen-72B thật — directional only; gates Stage B.** (≥3 seeds + significance = Stage B.) Also sanity-check client LoRA deltas differ. (RQ1+RQ3) **→ code ready + smoke ✅ 2026-06-10:** `p1_make_or_break` (4-arm eval), `p1_fedavg` (FedAvg + no-op detector, exits 1 on identical deltas), `p1_client_train --kd-label teacher/gold/none` (+ X-only via no `--client`, `--init-adapter` for round t>1); 77 tests pass. Awaiting: teacher targets gen + Kaggle training runs.
- [ ] Fix federated hyperparams for PoC: `K=2–3` rounds, `E=1` local epoch, LoRA rank/α/lr logged in config; checkpoint per round (free sessions die — must resume)
- [ ] ⭐ **Cross-schema generalization (PRIMARY RQ2, = outline RQ2 + Fig.1 innovation #4):** eval `M_G` EX on **held-out unseen schemas** (skill from `M_G` + local ICL on that schema's own few demos) vs SLM-only — tests skill transfer, NOT demo-store `G`. Parametric route makes this defensible (skill transfers; attempt-1 failed sharing schema-coupled *demos*). Promoted from secondary → primary to match outline's literal RQ2.
- [ ] *(optional, secondary)* Horizontal federation (shared schema) experiment
- [ ] *(report as motivation)* attempt-1's demo-store `G` cross-schema negative → motivates the skill-transfer route (skill generalizes, schema-coupled demos don't)

---

## P2. KD enhancement — logit-level + MinED `[RE-ALIGNED 2026-06-09]`

> **What:** The **parametric LoRA+FedAvg KD engine moved up into P1′** (it's the Fig.1 primary engine). P2 is now only the **logit-level refinement on top**: soft-logit KD + MinED token alignment to bridge teacher/student tokenizers (sequence-level KD already in P1′).
> **Why:** Logit/soft-target KD is the RQ3 upper-bound on top of P1′'s sequence-level LoRA KD, deferred until the P1′ parametric engine + Global SLM are validated. Adapts FedMKT [7] (logits + MinED) / FedCoLLM [8] (LoRA co-tune).

- [ ] Logit-level KD: add `λ·KL(softmaxτ student ‖ softmaxτ teacher)` on shared public set `X` (P1′ already does sequence-CE KD)
- [ ] MinED token alignment [7] to bridge teacher/student tokenizers
- [ ] Compare logit-KD ceiling vs sequence-level KD (P1′) + demo-level KD variant on EX + cost (RQ3)
- [ ] *(moved to P1′:* teacher setup, parametric LoRA+FedAvg KD, Global SLM `M_G`, teacher caching)

---

## SB. Stage B — headline runs (paid) 🔴 `[ADDED 2026-06-10]`

> **What:** Re-run the validated pipeline at paper grade: outline models (Qwen2.5-72B-Instruct teacher), paid GPU, full seeds, tiered matrix (plan §3.8). Only `stage=headline` numbers enter the paper.
> **Why:** PoC numbers (free teacher, 1 seed, subset) are not publishable evidence. Stage B is where every paper claim gets its actual support. Gated — no paid spend before both gate conditions.

- [ ] 🔴 **GATE (both required):** (1) PoC make-or-break directionally positive (`M_G` > SLM-only AND > train-on-X null); (2) supervisor sign-off on §8 decisions + budget. Negative PoC → diagnose/redesign, no spend
- [ ] Secure paid GPU: A100-class (Colab Pro / RunPod / Lambda) for LoRA training. (Teacher = Qwen-72B paid API đã dùng từ PoC; `teacher_targets.csv` dùng lại nguyên xi — REV 2)
- [ ] Pick Stage-B `K` from PoC convergence curve (plateau, cap ≤10); keep `E=1–2`; FedProx μ if client drift seen
- [ ] **Tier 1 (must, ≥3 seeds + significance):** make-or-break re-run, T1 Spider (FedICL-SQL / SLM-only / LLM-only / Centralized-FT / FedAvg-LoRA), Ablation 3, T3
- [ ] **Tier 2 (should, ≥3 seeds where cheap):** T2, F2, F3, Ablations 1/2/4, Fed-ICL + Centralized-ICL baselines, RQ2 held-out
- [ ] **Tier 3 (nice, 1 seed flagged):** F4 α-sweep, F6 L-sweep, DP (ε, EX), Ablation 5, Spider-Realistic, F5b MIA. Budget out → cut Tier 3, say so in paper
- [ ] All results carry `stage=headline` + actual teacher id + GPU in `model`/`gpu_vram` fields

---

## P3. Baselines

> **What:** Run the comparison points — LLM-only (ceiling), SLM-only (floor = Light-SQL per client), centralized-ICL (privacy-violating ceiling), without-ICL, FedAvg-LoRA, and Fed-ICL [5] adapted to SQL.
> **Scale note `[2026-06-10]`:** implement now, but paper-grade runs happen at **Stage B** scale (tiers in SB phase). During PoC only SLM-only + train-on-X null run (they gate the ⭐).
> **Why:** Each baseline isolates one claim. SLM-only vs FedICL-SQL answers RQ1 (does federation help). Centralized-ICL bounds how close we get without violating privacy. Fed-ICL-adapted is the closest competitor — beating it justifies the SQL specialization. Without these, results have no reference frame.

- [ ] LLM-only: teacher zero/few-shot (centralized) — accuracy ceiling
- [ ] SLM-only: local SLM (own private data only), NO federation, NO teacher — floor
- [ ] **Centralized-FT: pool all private data, LoRA-train one SLM (no fed)** — true parametric ceiling; the "what does FedAvg cost vs centralized" reference reviewers demand
- [ ] Centralized ICL: pool all data + ICL — privacy-violating ceiling
- [ ] Without ICL: SLM zero-shot
- [ ] FedAvg-LoRA: FL without teacher, without ICL
- [ ] Fed-ICL [5] adapted for SQL — closest federated competitor

---

## P4. Evaluation — tables & figures

> **What:** Produce every table (T1–T3), figure (F2–F5), and the 5 ablations + privacy attack that the paper's §4.2 needs. **All numbers here = Stage B (`stage=headline`); priority = Tier 1 > 2 > 3 per plan §3.8 — budget out → cut Tier 3 and say so.**
> **Why:** Turns runs into evidence. Each artifact maps to a research question: T1/T3/F2/F4 → RQ1, ablations 1+4 → RQ2 (ICL value), T2/F3 + ablation 3 → RQ3 (teacher value), F5 + privacy attack → the privacy claim. Ablations prove each component is load-bearing by removing it. Every paper claim must trace to one of these.

- [ ] 🔴 **Stats rigor (all tables):** every headline number = **mean±std over ≥3 seeds**; make-or-break comparisons get a **significance test** (paired bootstrap on per-query EX / McNemar) + p or CI. Temp=0 ≠ variance control.
- [ ] **T1** Overall Performance: EX/EM × {Spider, Spider-Realistic} × {seen, held-out} (RQ1)
- [ ] **T2** Efficiency: latency / VRAM / FLOPs (RQ3)
- [ ] **T3** Communication: bytes/round + rounds-to-converge vs FedAvg/Fed-ICL (RQ1)
- [ ] **F2** Convergence: EX vs round, by α
- [ ] **F3** Pareto: EX vs cost
- [ ] **F4** Heterogeneity: EX vs Dirichlet α
- [ ] **F5a** Privacy (demo/ICL-Hub channel): prompt-extraction attack [5] §6.4, with/without masking — valid for the demo channel ONLY
- [ ] **F5b** Privacy (weights channel) `[ADDED 2026-06-10 — attack must match what we transmit]`: membership-inference on `M_G` (loss-threshold MIA) and/or DP (ε, EX) curve. If neither runs → scope weights-privacy claim to "encrypted + DP available", never cite F5a as weights evidence
- [ ] **F6** Client scaling: EX + comm-cost vs `L ∈ {3,5,10}` (robustness; preempts "3 too few" reviewer pushback) — **run with DP on**; report (ε, EX-cost). DP counts as a contribution only if measured here; else scope DP to future work.
- [ ] **Ablation 1:** Without ICL
- [ ] **Ablation 2:** Without federated learning
- [ ] **Ablation 3:** Without Teacher LLM = **gold-CE arm** (same data, gold labels on `X` instead of teacher reasoning⊕SQL — isolates teacher value from data quantity; plan §3.6)
- [ ] **Ablation 4:** retrieval size k ∈ {0,1,3,5} (expected inverted-U)
- [ ] **Ablation 5:** different SLMs (Phi-3 / Gemma-2B / TinyLlama)
- [ ] 🔴 Privacy attack (D1): = F5a (demo reconstruction) + F5b (weights channel) above — both channels reported, claims channel-matched

---

## P5. Writing (parallel with P1–P4, don't wait for results)

> **What:** Draft the paper into the IAJIT template. Method (§3), Related Work (§2), Intro (§1) first; §4/abstract/§5 once results land.
> **Why:** §3/§2/§1 don't depend on experiment output — writing them now overlaps with P1–P4 compute and forces method clarity early (often exposes design gaps before they cost runs). Results-dependent sections (§4, abstract, §5) wait for P4. Citation check guards against the journal's reference scrutiny.

- [ ] §3 Proposed Approach (3.1–3.8) + Fig.1 + Algorithm 1 + equations ← **write first**. §3.5 Teacher–Student Collaboration = **training-time KD roles only** `[LOCKED 2026-06-10]` (teacher: reasoning⊕SQL targets + ICL-Hub demos on `X`; students consume in LoRA training) — runtime escalation OUT (inference cost + leaks query patterns), mention in §5 future work. §3.6: make ICL **load-bearing** (it's in the title): ICL Hub = the federated-ICL piece; held-out adaptation = where ICL must show a delta
- [ ] §2 Related Work (2.1–2.6) + gap table (2.6)
- [ ] §1 Introduction: NL2SQL, 3 challenges, motivation, RQ1-3, contributions
- [ ] §4 Experiments: 4.1 setup + 4.2 results & discussion + 5 ablations
- [ ] §4.2: Privacy-Utility Trade-off subsection
- [ ] Abstract (150–250 words, NO symbols/math)
- [ ] §5 Conclusion + future work
- [ ] Format IAJIT (IEEE 2-column, ~10–14 pages)
- [ ] `/ars-citation-check` — check citations

---

## P6. Review & submit

> **What:** Simulated peer-review pass, revise until every claim is table/figure-backed, release code, final IAJIT format check, submit.
> **Why:** Catches reviewer objections (especially the "Spider isn't really federated" pushback) before real reviewers do. Code release + reproducible scripts strengthen acceptance odds at a WoS-Q3 venue. Last gate before submission — no new science, just hardening.

- [ ] Self-review: `/ars-reviewer` (simulated panel)
- [ ] Revise per review; every claim → backed by table/figure
- [ ] Release code on GitHub (partition scripts, prompts, eval, configs)
- [ ] Final check of IAJIT template
- [ ] Submit

---

## Critical path

```text
P0 single-client ✅ → [P1 attempt-1 ❌ superseded]
   → P1′ PoC ~$2: parametric teacher-KD (Qwen-72B API thật, free GPU, 1 seed) + ⭐directional make-or-break
   → 🔴 SB GATE (PoC positive + supervisor sign-off + budget)
   → SB Stage B headline runs (Qwen-72B, paid GPU, ≥3 seeds, Tier 1→2→3)
        ↳ P2 logit-KD + MinED · P3 baselines · P4 eval (all at Stage-B scale) → P6 submit
                          ↓
              P5 write §3,§2,§1 (parallel, after P1′ shape is fixed — don't wait for Stage B)
```

**Decision milestone `[RE-STAGED 2026-06-10]`:** P1′ PoC make-or-break = does **parametric teacher-KD (Global SLM `M_G`)** raise SLM EX vs SLM-only + beat the train-on-X null, **directionally, on free tier**? Positive → unlock Stage B paid headline runs (outline models, ≥3 seeds). Negative → diagnose before any spend. The old "shared store → held-out EX" milestone is retired (attempt 1, negative).

**Pitfalls to avoid:** 🔴 **FedAvg-no-op** — clients MUST train on own private `Qᵢ`, not only shared `X`, else deltas identical → federation adds nothing → RQ1 dead (PoC includes a delta-difference sanity check); don't reintroduce cross-schema masked-demo-store; masking is **retrieval-only**; engine is **parametric** (LoRA+FedAvg weights, per Fig.1) — Fed-ICL answer-fusion is a baseline, NOT the method; privacy claim = "no raw data/schema leaves" (weights DO transmit — never claim "no weights"); **prompt-extraction (F5a) is demo-channel evidence only — never cite it for the weights channel (F5b = MIA/DP)**; **DP claimed only if measured**; every headline number needs **≥3 seeds + significance** (PoC 1-seed numbers NEVER enter the paper); 🔴 **no paid spend before the SB gate** (PoC positive + supervisor sign-off); guarantee **schema-disjoint** X/private/held-out (no leakage). Don't wait for results to write §3/§2.

---

*Source: `detailed_plan.md`. See also `problems_and_solutions.md` for per-step risks.*
