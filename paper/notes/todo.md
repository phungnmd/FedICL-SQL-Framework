# FedICL-SQL — Execution Roadmap

**Daily driver:** ▶️ Runbook below (tick boxes) + `LAB_LOG.md` (write each session). Method/experiment detail = `detailed_plan.md` (spec). Numbers = `fedicl-sql/experiments/RUNS.csv` (auto).

- `[ ]` todo · `[~]` doing · `[x]` done. 🔴 blocks.
- Metrics → headline + story in `LAB_LOG.md`; full row auto in `RUNS.csv`.
- Changing a locked decision → update **both** this file and detailed_plan §8.

**State (2026-06-13):** pipeline + 81 tests green · split `3c-a1.0-s0` built (X=29 DB · 3 clients · held-out=20) · chat-template engine fix validated · **matched cuda pair: base floor EX=40.5% EM=8.5% → B3 centralized-FT EX=49.5% EM=33.0% (+9.0 EX, one stack)** · (`p0_eval50` EX=44.5% mps base+ICL = mixed-stack ref only, NOT comparable to the cuda pair — CONVENTION §5) · training resumable (crash→resume validated).

---

## ▶️ Runbook — the 9 steps (track here)

Whole project = **train a few models → eval → compare**. Core question: how close does federated teacher-KD bring the small SQL model to the centralized ceiling (`B3`), and how much does the teacher add over gold labels (Without-Teacher ablation)? Run from `fedicl-sql/`.

**Run now — Mac, $0, no teacher, no gate:**

- [x] **1. `p0_sanity`** — pipeline works on Qwen-1.5B? → EX=PASS EM=PASS (Mac MPS, 2026-06-12)
- [x] **2. `p0_eval50`** — base+ICL floor → **EX=44.5% EM=26.5%** (n=200 k=3, Mac MPS, 7.4s/q, 5.1GB, 2026-06-12). *PoC floor only; final paper eval should use the federated/public-X ICL setting.*
- [ ] **3. `b3_centralized_ft`** — pooled-private LoRA = parametric **ceiling** (B3)
- [ ] **4. `p1_client_train --kd-label none` ×3** — per-client solo LoRA = **floor** (B2)

**Gate — unlocks 5–8 (~$2 teacher, can run pre-supervisor-gate):**

- [ ] **5. `gen_teacher_targets.py`** — Qwen2.5-72B (DeepInfra) → `teacher_targets.qwen72b.csv` **with top-20 logprobs** (once, cached)
- [ ] **6. `p1_client_train --kd-label gold` ×3 → `p1_fedavg`** — FedAvg-no-teacher = **B6** (= Ablation-3)
- [ ] **7. `p1_client_train --kd-label teacher` ×3 → `p1_fedavg`** — **`M_G` = the method** (FedICL-SQL)
- [ ] **8. `p1_client_train` (omit `--client`) `--kd-label teacher`** — **X-only null** arm

**Analysis (RQ evidence):**

- [ ] **9. `p1_teacher_value`** — eval `M_G` vs B2 vs gold_ce vs X-only on each client's own set
  - Report three deltas as RQ evidence (**not pass/fail gates**): `M_G − B2` (federation gain), `M_G − gold_ce` (teacher value, expected positive via soft-KL — dark knowledge gold lacks), `M_G − X-only` (FedAvg-no-op check).
  - Frame RQ1 as `M_G` → centralized ceiling **B3** (small federation gap), not the trivial `> B2`. The label-free unlabeled-X ablation (Ab3b) shows the necessary-teacher regime.

> Label decoder: **B#** = baseline · **Ab#** = ablation (remove-a-piece) · **arm** = the 4 models step 9 compares (`m_g`/`slm_only`/`gold_ce`/`x_only`) · **p0/p1/b3** = scripts. One model wears several labels (**B6 = Ab3a = arm `gold_ce`**; **B2 = arm `slm_only`**). 🔴 **Canonical labels + notation (K/T/k, B1–B7, Ab1–Ab5, T1–T3, F1–F6, stages, tiers) = detailed_plan §0** — single source, keep this file in sync with it.

---

## Beyond the runbook (coarse — full detail in detailed_plan)

**Writing — start NOW, parallel (results-independent; forces method clarity):**

- [ ] §3 Method + Fig.1 + Algorithm 1 + equations (**write first**) · §2 Related Work + gap table · §1 Intro

**After the PoC verdict:**

- [ ] 🔴 **SB gate** — PoC-positive + supervisor sign-off on §8 + budget. *No Stage-B paid spend before this.*
- [ ] **Stage-B headline** — Tier 1→3, ≥3 seeds + significance, DP measured. Only `stage=headline` is cited.
- soft-KL KD is part of P1 (DeepInfra top-20 logprobs, aligned tokenizer → no separate logit-KD phase, no MinED)
- [ ] §4 Experiments + §4.2 Privacy-Utility + Abstract + §5 → IAJIT format → `/ars-citation-check`
- [ ] `/ars-reviewer` → revise (every claim ↔ a table/figure) → release code → submit

---

## Locked design (reference)

- **Engine:** parametric teacher→student KD — clients LoRA-train on own private `Qᵢ` + public `X` (teacher targets), upload **LoRA deltas only**, server **FedAvg → `M_G`**. = Fig.1 + **FedCoLLM [8]**.
- **Student:** Qwen2.5-1.5B-Instruct (tokenizer-aligned w/ teacher → soft-KL KD without MinED). Others → A5 ablation.
- **Teacher:** Qwen2.5-72B-Instruct (DeepInfra, `top_logprobs=20` → soft-KL KD), ~$1–2 all of `X`, targets cached once.
- **Clients:** `K=3` default, sweep `{3,5,10}` (F6). Cross-silo. *(`K`=clients, `T`=rounds, `k`=shots — canonical, matches Fig.1; old `L`=clients retired.)*
- **ICL:** schema-aware retrieval, **masking retrieval-only**, demos shown **unmasked**, local per client.
- **Privacy:** no raw rows/schema leave; only encrypted, DP-perturbed LoRA-deltas transmit. (Never "no weights leave".)
- **Compute (3 tiers):** Mac M4 Pro MPS fp16 = dev + `$0` no-teacher baselines + PoC · Colab Pro = heavier PoC / 4-bit QLoRA · paid A100 = Stage-B only · teacher = paid API. **One stack per comparison set** (Mac-fp16 ≠ CUDA-4bit). Detail → CONVENTION §5.
- **Staging:** PoC (~$2, 1 seed, subset, Mac/Colab, no DP) → SB gate → Stage-B (paid GPU, ≥3 seeds + significance, DP). Only `headline` enters the paper.

---

## Pitfalls (guardrails)

🔴 **FedAvg-no-op** — clients MUST train on own private `Qᵢ`, not only `X` (delta-difference check). · **Teacher value** — on labeled Spider exec-filtered teacher SQL ⊆ gold, so teacher value comes from the **soft-KL term** (dark knowledge gold lacks) + **CoT** + the **label-free regime** (unlabeled-X, Ab3b); report the Without-Teacher delta. · 🔴 **ICL-null** — masking *costs* EX ([4]); if −ICL ≈ full on seen AND held-out, the title overclaims → surface at gate. · Masking = **retrieval-only**. · Engine is **parametric** (weights); Fed-ICL fusion is a **baseline**. · Privacy claim = "no raw data/schema leaves" (weights DO transmit — never "no weights"). · **F5a = demo-channel only**, never weights evidence (F5b = MIA/DP). · **DP claimed only if measured** (else item-4 = standard secure FL, not a headline contribution). · Headline = **≥3 seeds + significance** (PoC 1-seed numbers NEVER enter the paper). · 🔴 **No Stage-B paid spend before the SB gate**. · Guarantee **schema-disjoint** X/private/held-out. · Don't wait for results to write §3/§2.

---

*Spec: `detailed_plan.md`. Log: `LAB_LOG.md`. Numbers: `RUNS.csv` + `REGISTRY.md`. Risks: `problems_and_solutions.md`. Mechanism: `fig1_architecture.md`.*
