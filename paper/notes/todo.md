# FedICL-SQL — Execution Roadmap

**Daily driver:** ▶️ Runbook below (tick boxes) + `LAB_LOG.md` (write each session). Method/experiment detail = `detailed_plan.md` (spec). Numbers = `fedicl-sql/experiments/RUNS.csv` (auto).

- `[ ]` todo · `[~]` doing · `[x]` done. 🔴 blocks.
- Metrics → headline + story in `LAB_LOG.md`; full row auto in `RUNS.csv`.
- Changing a locked decision → update **both** this file and detailed_plan §8.

**State (2026-06-16):** pipeline + 81 tests green · **arch re-aligned: teacher = local 7B per client, public X removed, ICL Hub G removed, 2-pool split** · split `3c-a1.0-s0` rebuilt (no public X · 3 clients · c1=45DB/2122tr · c2=45DB/1972tr · c3=56DB/2832tr · held-out=1034/20DB) · chat-template engine fix validated · **matched cuda pair: base floor EX=40.5% EM=8.5% → B3 centralized-FT EX=49.5% EM=33.0% (+9.0 EX, one stack)** · (`p0_eval50` EX=44.5% mps base+ICL = mixed-stack ref only, NOT comparable — CONVENTION §5) · training resumable (crash→resume validated) · **schema-aware retrieval wired**.

---

## ▶️ Runbook — the 9 steps (track here)

Whole project = **train a few models → eval → compare**. Core question: how close does federated teacher-KD bring the small SQL model to the centralized ceiling (`B3`), and how much does the teacher add over gold labels (Without-Teacher ablation)? Run from `fedicl-sql/`.

**Run now — Mac, $0, no teacher, no gate:**

- [x] **1. `p0_sanity`** — pipeline works on Qwen-1.5B? → EX=PASS EM=PASS (Mac MPS, 2026-06-12)
- [x] **2. `p0_eval50`** — base+ICL floor → **EX=44.5% EM=26.5%** (n=200 k=3, Mac MPS, 7.4s/q, 5.1GB, 2026-06-12). *PoC floor only; final paper eval should use the federated/public-X ICL setting.*
- [x] **3. `b3_centralized_ft`** — pooled-private LoRA = parametric **ceiling** (B3) → EX=49.5% EM=33.0% (CUDA, seed 0, n=200, 2026-06-13)
- [ ] **4. `p1_client_train --kd-label none` ×3** — per-client solo LoRA = **floor** (B2)

**Gate — unlocks 5–8 (~$2 teacher, can run pre-supervisor-gate):**

- [ ] **5. `gen_teacher_targets.py --private client_i_train.csv` ×3** — Qwen2.5-7B (local, per client) → `client_i_teacher_targets.csv` **with top-K logprobs** (once per client, cached; `--load-in-4bit` on T4)
- [ ] **6. `p1_client_train --kd-label none` ×3 → `p1_fedavg`** — FedAvg **without** KD = **Ab3** (federation gain without teacher signal)
- [ ] **7. `p1_client_train --kd-label teacher` ×3 → `p1_fedavg`** — **`M_G` = the method** (FedICL-SQL)

**Analysis (RQ evidence):**

- [ ] **8. `p1_teacher_value`** — eval `M_G` vs B2 vs Ab3 (fedavg-no-kd) on each client's own set
  - Report two deltas as RQ evidence (**not pass/fail gates**): `M_G − B2` (federation gain), `M_G − Ab3` (teacher value via soft-KL — dark knowledge gold labels lack).
  - Frame RQ1 as `M_G` → centralized ceiling **B3** (small federation gap), not the trivial `> B2`.

> Label decoder: **B#** = baseline · **Ab#** = ablation (remove-a-piece) · **arm** = the 4 models step 9 compares (`m_g`/`slm_only`/`gold_ce`/`x_only`) · **p0/p1/b3** = scripts. One model wears several labels (**B6 = Ab3 = arm `gold_ce`**; **B2 = arm `slm_only`**). 🔴 **Canonical labels + notation (K/T/k, B1–B7, Ab1–Ab5, T1–T3, F1–F6, stages, tiers) = detailed_plan §0** — single source, keep this file in sync with it.

---

## Beyond the runbook (coarse — full detail in detailed_plan)

**Writing — (results-independent; forces method clarity):**

- [ ] §3 Method + Fig.1 + Algorithm 1 + equations (**write first**) · §2 Related Work + gap table · §1 Intro

**After the PoC verdict:**

- [ ] 🔴 **SB gate** — PoC-positive + supervisor sign-off on §8 + budget. *No Stage-B paid spend before this.*
- [ ] **Stage-B headline** — Tier 1→3, ≥3 seeds + significance, DP measured. Only `stage=headline` is cited.
- soft-KL KD is part of P1 (DeepInfra top-20 logprobs, aligned tokenizer → no separate logit-KD phase, no MinED)
- [ ] §4 Experiments + §4.2 Privacy-Utility + Abstract + §5 → IAJIT format → `/ars-citation-check`
- [ ] `/ars-reviewer` → revise (every claim ↔ a table/figure) → release code → submit

---

## Locked design (reference)

- **Engine:** parametric teacher→student KD — clients LoRA-train on own private `Qᵢ` (gold CE + local teacher KD), upload **LoRA deltas only**, server **FedAvg → `M_G`**. = Fig.1 + **FedCoLLM [8]**.
- **Student:** Qwen2.5-1.5B-Instruct (tokenizer-aligned w/ teacher → soft-KL KD without MinED). Others → A5 ablation.
- **Teacher:** Qwen2.5-7B-Instruct (**local HF, per client, runs on own Qᵢ**), top-K logprobs via HF generate, targets cached once per client. No API cost.
- **Data split:** 2-pool only — `client_i_private` + `held_out`. No public X. All train DBs go to clients (more data per client than before).
- **Clients:** `K=3` default, sweep `{3,5,10}` (F6). Cross-silo. *(`K`=clients, `T`=rounds, `k`=shots — canonical, matches Fig.1.)*
- **ICL:** schema-aware retrieval, **masking retrieval-only** (planned), demos shown **unmasked**, pool = `Qᵢ` only (all stages). No ICL Hub G.
- **Privacy:** no raw rows/schema/teacher outputs leave client; teacher runs fully on-premise; only encrypted, DP-perturbed LoRA-deltas transmit. (Never "no weights leave".) **Stronger than before** — no external API call during KD.
- **Compute (3 tiers):** Mac M4 Pro MPS fp16 = dev + `$0` no-teacher baselines + B2/B3 PoC · Colab Pro T4 = teacher targets gen (7B, `--load-in-4bit` → ~4 GB) + student LoRA training (~11 GB) · paid A100 = Stage-B only. Sequential VRAM: teacher → unload → student. **One stack per comparison set.** Training = **plain LoRA fp16** (no 4-bit during training). Detail → CONVENTION §5.
- **Staging:** PoC (~$0, 1 seed, subset, Mac/Colab, no DP) → SB gate → Stage-B (paid GPU, ≥3 seeds + significance, DP). Only `headline` enters the paper.

---

## Pitfalls (guardrails)

🔴 **FedAvg-no-op** — clients MUST train on own private `Qᵢ`, not only `X` (delta-difference check). · **Teacher value** — on labeled Spider exec-filtered teacher SQL ⊆ gold, so teacher value comes from the **soft-KL term** (dark knowledge gold lacks) + **CoT**; report the Without-Teacher (Ab3) delta. · 🔴 **ICL-null** — masking *costs* EX ([4]); if −ICL ≈ full on seen AND held-out, the title overclaims → surface at gate. · Masking = **retrieval-only**. · Engine is **parametric** (weights); Fed-ICL fusion is a **baseline**. · Privacy claim = "no raw data/schema leaves" (weights DO transmit — never "no weights"). · **F5a = demo-channel only**, never weights evidence (F5b = MIA/DP). · DP = headline contribution; report (ε, EX) at Stage-B. · Headline = **≥3 seeds + significance** (PoC 1-seed numbers NEVER enter the paper). · 🔴 **No Stage-B paid spend before the SB gate**. · Guarantee **schema-disjoint** X/private/held-out. · Don't wait for results to write §3/§2.

---

*Spec: `detailed_plan.md`. Log: `LAB_LOG.md`. Numbers: `RUNS.csv` + `REGISTRY.md`. Mechanism: `fig1_architecture.md`.*
