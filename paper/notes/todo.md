# FedICL-SQL — Execution Roadmap

**Daily driver:** ▶️ Runbook below (tick boxes) + `LAB_LOG.md` (write each session). Method/experiment detail = `detailed_plan.md` (spec). Numbers = `fedicl-sql/experiments/RUNS.csv` (auto).

- `[ ]` todo · `[~]` doing · `[x]` done. 🔴 blocks · ⭐ make-or-break.
- Metrics → headline + story in `LAB_LOG.md`; full row auto in `RUNS.csv`.
- Changing a locked decision → update **both** this file and detailed_plan §8.

**State (2026-06-12):** pipeline + 81 tests green · split `3c-a1.0-s0` built (X=29 DB · 3 clients · held-out=20) · `p0_sanity` PASS on Qwen-1.5B · `p0_eval50` rerun at n=200 gives base+ICL floor **EX=44.5% EM=26.5%** · training resumable (crash→resume validated).

---

## ▶️ Runbook — the 9 steps (track here)

Whole project = **train a few models → eval → compare**. One verdict: does federated teacher-KD make the small SQL model beat going-solo (`> B2`) AND beat the cheat-null (`> X-only`). Run from `fedicl-sql/`.

**Run now — Mac, $0, no teacher, no gate:**

- [x] **1. `p0_sanity`** — pipeline works on Qwen-1.5B? → EX=PASS EM=PASS (Mac MPS, 2026-06-12)
- [x] **2. `p0_eval50`** — base+ICL floor → **EX=44.5% EM=26.5%** (n=200 k=3, Mac MPS, 7.4s/q, 5.1GB, 2026-06-12). *PoC floor only; final paper eval should use the federated/public-X ICL setting.*
- [ ] **3. `b3_centralized_ft`** — pooled-private LoRA = parametric **ceiling** (B3)
- [ ] **4. `p1_client_train --kd-label none` ×3** — per-client solo LoRA = **floor** (B2)

**Gate — unlocks 5–8 (~$2 teacher, can run pre-supervisor-gate):**

- [ ] **5. `gen_teacher_targets.py`** — Qwen-72B → `teacher_targets.csv` (once, cached)
- [ ] **6. `p1_client_train --kd-label gold` ×3 → `p1_fedavg`** — FedAvg-no-teacher = **B6** (= Ablation-3)
- [ ] **7. `p1_client_train --kd-label teacher` ×3 → `p1_fedavg`** — **`M_G` = the method** (FedICL-SQL)
- [ ] **8. `p1_client_train` (omit `--client`) `--kd-label teacher`** — **X-only null** arm

**Verdict:**

- [ ] **9. ⭐ `p1_make_or_break`** — eval `M_G` vs B2 vs null vs B6 on each client's own set
  - **WIN = `M_G` > B2 AND `M_G` > X-only null.** Positive → SB gate → Stage-B. Negative → diagnose, no spend.

> Label decoder: **B#** = baseline to beat · **Ablation #** = remove-a-piece-measure-drop · **arm** = the 4 models step 9 compares · **p0/p1/b3** = the scripts. One trained model wears several labels (B6 = Ab3 = arm 4). Canonical defs → detailed_plan §3.3 / §3.6.

---

## Beyond the runbook (coarse — full detail in detailed_plan)

**Writing — start NOW, parallel (results-independent; forces method clarity):**

- [ ] §3 Method + Fig.1 + Algorithm 1 + equations (**write first**) · §2 Related Work + gap table · §1 Intro

**After the PoC verdict:**

- [ ] 🔴 **SB gate** — PoC-positive + supervisor sign-off on §8 + budget. *No Stage-B paid spend before this.*
- [ ] **Stage-B headline** — Tier 1→3, ≥3 seeds + significance, DP measured. Only `stage=headline` is cited.
- [ ] P2 logit-KD + MinED (likely skippable — aligned tokenizer)
- [ ] §4 Experiments + §4.2 Privacy-Utility + Abstract + §5 → IAJIT format → `/ars-citation-check`
- [ ] `/ars-reviewer` → revise (every claim ↔ a table/figure) → release code → submit

---

## Locked design (reference)

- **Engine:** parametric teacher→student KD — clients LoRA-train on own private `Qᵢ` + public `X` (teacher targets), upload **LoRA deltas only**, server **FedAvg → `M_G`**. = Fig.1 + **FedCoLLM [8]**.
- **Student:** Qwen2.5-1.5B-Instruct (tokenizer-aligned w/ teacher → MinED-free P2). Others → A5 ablation.
- **Teacher:** Qwen2.5-72B-Instruct, paid API (DeepInfra ~$1–2 all of `X`), targets cached once.
- **Clients:** `L=3` default, sweep `{3,5,10}` (F6). Cross-silo.
- **ICL:** schema-aware retrieval, **masking retrieval-only**, demos shown **unmasked**, local per client.
- **Privacy:** no raw rows/schema leave; only encrypted, DP-perturbed LoRA-deltas transmit. (Never "no weights leave".)
- **Compute (3 tiers):** Mac M4 Pro MPS fp16 = dev + `$0` no-teacher baselines + PoC · Colab Pro = heavier PoC / 4-bit QLoRA · paid A100 = Stage-B only · teacher = paid API. **One stack per comparison set** (Mac-fp16 ≠ CUDA-4bit). Detail → CONVENTION §5.
- **Staging:** PoC (~$2, 1 seed, subset, Mac/Colab, no DP) → SB gate → Stage-B (paid GPU, ≥3 seeds + significance, DP). Only `headline` enters the paper.

---

## Pitfalls (guardrails)

🔴 **FedAvg-no-op** — clients MUST train on own private `Qᵢ`, not only `X` (make-or-break has a delta-difference check). · Masking = **retrieval-only**. · Engine is **parametric** (weights); Fed-ICL fusion is a **baseline**. · Privacy claim = "no raw data/schema leaves" (weights DO transmit — never "no weights"). · **F5a = demo-channel only**, never weights evidence (F5b = MIA/DP). · **DP claimed only if measured**. · Headline = **≥3 seeds + significance** (PoC 1-seed numbers NEVER enter the paper). · 🔴 **No Stage-B paid spend before the SB gate**. · Guarantee **schema-disjoint** X/private/held-out. · Don't wait for results to write §3/§2.

---

*Spec: `detailed_plan.md`. Log: `LAB_LOG.md`. Numbers: `RUNS.csv` + `REGISTRY.md`. Risks: `problems_and_solutions.md`. Mechanism: `fig1_architecture.md`.*
