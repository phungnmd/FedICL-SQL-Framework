# Fed-ICKD — System Architecture

**Federated In-Context Knowledge Distillation for Text-to-SQL** *(repo name: FedICL-SQL)*

> **Rewritten 2026-07-08.** This document supersedes every prior version and all
> prior re-alignment notes. Architecture source: `Suggest.MD` (accepted), with **one
> amendment**: the server-distillation loss is **reverse-KL logit distillation from
> [10]** (`CE + RKL(q‖p)`), NOT Suggest.MD's forward `KL(τ=2, top-50)` + relational
> RKD. Relational KD (distance/angle-wise on hidden states) is dropped entirely.
>
> ⚠️ **Naming:** in this repo **RKD = Reverse Knowledge Distillation on gold data**
> ([10]'s ground-truth-data baseline) — never Park et al.'s *Relational* KD. The
> acronym clash with Suggest.MD's §2.2 is resolved by dropping relational KD.
>
> This is also the single decision/notation record — `DECISIONS.md` was folded in
> here and deleted 2026-07-08 (see §12–§14).

---

## GOAL — what this framework is for

A framework in which a **small open-source model** (student, 1.5B) reaches as
close as possible to the performance of a **larger model** (teacher, 7B) in a
**federated** setting — at a fraction of the larger model's serving cost — by
combining three ingredients: **SFT**, **KD**, and **ICL** (how each is
realized: the rest of this document).

The cost asymmetry is the selling point: the teacher's cost is paid **once, at
training time, at the server** — per-query serving cost is the small student's
(≈1/5 the teacher's params and VRAM, runs on a consumer GPU, no server
round-trip, no API calls — fully open-source stack). Success is measured as the
share of the base→teacher gap the student recovers on Spider dev
(`(fedkd − base)/(teacher − base)`; target share fixed after the PoC), never as
absolute parity with the teacher.

---

## 0. Status & scope (2026-07-08)

- **Running now:** centralized KD PoC (`KD_PLAN.md` §PoC) — `central_ft` /
  `central_rkd` / `central_kid` trained from base on identical Spider data,
  no federation. Purpose: validate the KD signal and pick the KD direction
  (RKD vs KID) **before** wiring the federated pipeline.
- **Deferred until the PoC has a verdict:**
  - which dataset serves as the **public pool `P`** (BIRD dropped 2026-07-07 —
    too heavy, dialect gap; candidate default = Spider held-out ~15%, DB-disjoint
    from clients; decision open),
  - the full federated pipeline (Flower simulation, server distillation step),
  - all Tier-2 ablations (§10).
- **Not planned by default:** DP noise on adapters (Tier 3 — add only if a reviewer
  demands it; otherwise handled in the Limitations/Discussion section). Do **not**
  claim formal DP in the paper.

---

## 1. Problem setting

`K` organizations (clients) each hold:

- a **private relational database** with schema `Sᵢ` — never leaves the client;
- a **private NL→SQL store** `Qᵢ = {(qₙ, sₙ)}` — never leaves the client.

Data is **non-IID by domain**: each client owns a few Spider databases
(Dirichlet partition over domain groups). Schema and query logs are sensitive —
centralizing them for fine-tuning is off the table.

**Goal:** collaboratively train a small local SQL model (student 1.5B) that
(1) benefits from cross-client knowledge without any private data crossing the
wire, and (2) closes as much as possible of the gap to a 7B teacher — via a
**server-side teacher that never touches client data**, distilling on a public
pool after each aggregation round.

**Novelty claims (paper):**
1. Federated Text-to-SQL with realistic non-IID partition by schema/domain (new formulation).
2. Server-side reverse-KL distillation on public data as a **consensus regularizer**
   for FedAvg — teacher fully isolated from private data.
3. DAIL-style ICL consistent between client training and inference, plus an analysis
   of how public-pool quality affects distillation effectiveness.

---

## 2. Architecture overview

```
┌──────────────────────── SERVER ─────────────────────────┐
│  Teacher M_T (7B, frozen)        Public pool P (TBD)     │
│                                                          │
│  [Phase 1 — offline, once]                               │
│  DAIL selection on P → teacher ICL forward               │
│  → cache teacher logits on gold y_pub (RKD-usable;       │
│    KID needs the teacher online — ŷ changes each round)  │
│                                                          │
│  [Phase 3 — every round]                                 │
│  FedAvg(LoRA adapters, nᵢ/n) → global student M_G        │
│  → distill on P:  L = λ_ft·CE(y_pub) + λ_kd·RKL(q‖p)     │
│    (a few hundred steps)                                 │
│  → broadcast adapters                                    │
└───────────▲──────────────────────────┬──────────────────┘
    adapters│(a few MB)                │adapters
┌───────────┴──────────────────────────▼──────────────────┐
│  CLIENT i (×K)  —  private: a few Spider domains         │
│                                                          │
│  [Phase 2 — every round]                                 │
│  DAIL selection from local pool → prompt [k demos +      │
│  schema + question] → student 1.5B + QLoRA               │
│  → L_CE(gold SQL) only, E local epochs — NO teacher      │
│                                                          │
│  [Phase 4 — inference]                                   │
│  Student + local DAIL retrieval, same k as training      │
└──────────────────────────────────────────────────────────┘
```

**Privacy guarantee:** raw data, demos, and embeddings of a client never leave
that client. The teacher only ever touches the public pool `P`. Only LoRA
adapters are transmitted (SSL/TLS channel). DP noise = optional Tier-3 add-on,
not a default claim.

---

## 3. Server components

### 3.1 Teacher `M_T` (frozen 7B)

- Lives **at the server**. Never receives client data — structurally, not by
  promise: nothing but adapters ever arrives at the server.
- Model id: default candidate **Qwen2.5-Coder-7B-Instruct** (switched from plain
  Qwen2.5-7B-Instruct 2026-07-08 — code-tuned, closer to SQL generation; shares
  the Qwen2.5 tokenizer so `rkl_div_loss`'s common-vocab-prefix slicing still
  applies). ⚠️ The teacher/student pair is **not finalized** — pick after the
  centralized PoC + a model sweep. Every run records the ids actually used in
  its `metrics.json` (`model` = student, `teacher_model` = teacher, `""` when
  no KD), so results are never ambiguous.
- Serves two roles:
  1. **KD scorer** (Phase 1/3): one teacher-forced forward over the KD target —
     logprob distribution `p`, no decoding.
  2. **Reference arm** (`teacher`, M4): teacher + DAIL ICL, zero fine-tune,
     inference-only.
- Teacher ICL: DAIL selection **within `P`** (k_teacher = 3, ablate 5). Teacher
  and student condition on the **same** ICL context when computing the KD pair
  (`p`, `q`) — scoring them under different contexts corrupts the divergence.

### 3.2 Public pool `P` — **dataset TBD**

- Requirements: public, DB-disjoint from every client's data **and** from the
  eval sets (no contamination), a few hundred–few thousand (question, SQL) pairs.
- Candidate default (Suggest.MD): Spider held-out ~15% (~1,000 samples, split by
  database, no overlap with clients). BIRD subset = distribution-gap ablation
  candidate only. **Decision deferred** until the centralized PoC has a verdict.
- Note: whatever becomes `P` cannot also be an eval benchmark (contamination).

### 3.3 Federated aggregation

```
θ_t ← θ_{t-1} + Σᵢ (nᵢ/n)·Δθᵢ      # McMahan weighting, NOT 1/K — non-IID sizes differ
M_G ← base_student + θ_t
```

- **Uploads/downloads = LoRA adapters only** (a few MB/round).
- LoRA-averaging caveat: averaging `A`,`B` factors separately ≠ averaging the
  products (`mean(BᵢAᵢ) ≠ mean(Bᵢ)·mean(Aᵢ)` — FedIT/FLoRA issue). Mitigated by
  re-initializing every client from the same aggregated adapter each round;
  acknowledge in one sentence in the paper.
- FedProx = Plan-B if drift under strong non-IID makes convergence unstable
  (Tier 3, triggered by ablation A4).

### 3.4 Server distillation (Phase 3 — the consensus regularizer)

After each FedAvg, the aggregated global student is distilled on `P` for a few
hundred steps (default 300, batch 16 — the server is not VRAM-constrained the
way clients are):

```
L = λ_ft · CE(student, y_pub)  +  λ_kd · RKL(q ‖ p)        # [10]'s recipe, defaults 1:1
```

- `p` = teacher logprobs over the KD target, `q` = student logprobs over the
  same target, **same DAIL ICL context** for both.
- **Reverse KL, never forward KL**: mode-seeking fits SQL's precise,
  low-diversity token distribution ([10]); forward KL is mean-seeking and
  smears mass over invalid continuations.
- KD target per direction (§8): gold `y_pub` (**RKD**) or imperfect `ŷ_pub`
  (**KID**, student one-pass rewrite of ρ-masked gold).
- Implementation notes carried over from the PoC code (`train_online_kd`):
  Qwen2.5 7B vs 1.5B logit dims differ (V=152064 vs 151936, embedding padding)
  → slice both to the common vocab prefix; compute RKL in float32 (fp16 sum
  over a 150k vocab loses precision).
- **Role:** after FedAvg on non-IID clients the global model's behaviour is a
  blend of divergent local optima; distilling every round toward one fixed
  teacher on one shared pool pulls the aggregate back to a consensus
  (FedDF/FedMD line of argument) — a regularizer, not a data-augmentation trick.

**Caching:** for **RKD** the target (gold `y_pub`) and the ICL context are fixed
→ teacher logits can be computed **once offline** (Phase 1) and reused every
round. For **KID** the target `ŷ_pub` depends on the current student → teacher
must run online each distillation step. (The hidden-state cache from Suggest.MD
Phase 1 is dropped with relational KD.)

---

## 4. Communication

| Direction | What crosses | Protected by |
|---|---|---|
| DOWN (server → client) | aggregated LoRA adapter (M_G) | SSL/TLS |
| UP (client → server) | LoRA delta `Δθᵢ` only | SSL/TLS (+ optional DP noise, Tier 3) |
| Never | raw rows, schema `Sᵢ`, `Qᵢ`, demos, embeddings, teacher outputs | stay local by design |

Threat model (short §3 paragraph in the paper): define precisely what "teacher
never sees private data" means (structural isolation at the server), what
residual risk adapter transmission carries (gradient-leakage literature), and
why that is acceptable at this threat level. Formal DP is a stated limitation,
not a claim.

---

## 5. Client components

### 5.1 Local data (private, never leaves)

- `Sᵢ` — relational schema (tables, columns, types, FK paths)
- `Qᵢ` — NL/gold-SQL pairs on `Sᵢ`'s databases; also the local ICL demo pool

### 5.2 DAIL selection (the ICL method — locked)

Per DAIL-SQL [9], demos are chosen by **dual similarity**:

- **Question similarity** — embed the question with **schema-specific tokens
  masked** (table/column names → placeholders), so similarity reflects the
  question's structural semantics, not domain vocabulary.
- **Query similarity** — a preliminary SQL (from the current student, or a
  skeleton) ranks candidates by SQL structure.
- Candidates satisfying both → top-k.
- **Prompt format: demos are `question + SQL` only — no demo schema/DDL**
  (DAIL's format; saves tokens, which matters for a 1.5B student, and keeps
  foreign schema out of the prompt).

Applied at three sites, always **within the local pool of whoever retrieves**:
(a) teacher on `P` retrieves from `P`; (b) client student retrieves from its
own `Qᵢ`; (c) server distillation retrieves the student's demos from `P`.

### 5.3 Student `Mᵢ` — 1.5B + QLoRA

- Default candidate: Qwen2.5-1.5B-Instruct (tokenizer-aligned with the Qwen
  teacher → RKL without vocabulary mapping). QLoRA r=16, α=32, targets attn+MLP.
- Initialized from the broadcast global adapter each round.
- 0.5B student = Tier-3 extra model pair (claim-strengthening, optional).

### 5.4 Local training (Phase 2 — CE only, no teacher)

```
L = CE(student(P_ICL(q, Sᵢ, demos_Qᵢ)), gold SQL)     # E local epochs
```

- Prompt = [k_student DAIL demos + schema + question]; **same k at training and
  inference** (default k_student = 2; ablate 0/1/2). Training with demos in
  context is what makes eval-time ICL in-distribution — the train/test-mismatch
  failure mode measured earlier (k0-trained student + k3 eval → schema bleed,
  −30 net flips, 54/109 hurts = `no such column`) is exactly what this removes.
- No teacher, no KD loss, no public data at the client. Light and
  VRAM-friendly — everything heavy lives at the server.

---

## 6. Federated round loop

```python
# Phase 1 (offline, once): teacher annotation on P
#   DAIL index over P; teacher ICL forwards → cache logits on gold y_pub

Round t = 1 .. T:                                # T = 15 default
  1. SERVER broadcasts adapter θ_{t-1} → all K clients

  2. CLIENT i (Phase 2, parallel — simulated sequentially on one GPU):
       student.load_lora(θ_{t-1})
       for E local epochs over Qᵢ:
           demos = DAIL(q, pool=Qᵢ, k=k_student)
           L = CE(student(P_ICL(q, Sᵢ, demos)), y)
           update_lora(student, L)
       upload Δθᵢ = θᵢ − θ_{t-1}                 # adapters only

  3. SERVER (Phase 3):
       θ̃_t ← θ_{t-1} + Σᵢ (nᵢ/n)·Δθᵢ            # FedAvg
       student.load_lora(θ̃_t)
       for step in range(300):                   # distill on P, batch 16
           x, y = next_batch(P);  demos = DAIL(x, pool=P, k=3)
           tgt = mask_rewrite(y, ρ) if KID else y
           p = teacher(P_ICL(x, demos), tgt)     # cached offline for RKD
           q = student(P_ICL(x, demos), tgt)
           L = λ_ft·CE(y) + λ_kd·RKL(q, p)
           update_lora(student, L)
       θ_t ← student adapter;  M_G ← base + θ_t

Inference (Phase 4, per client, no server / no teacher):
       demos = DAIL(q, pool=Qᵢ, k=k_student)     # same k as training
       M_G.generate(P_ICL(q, Sᵢ, demos)) → SQL
```

---

## 7. Inference (deployment)

Each client runs `M_G` locally: DAIL retrieval from its own `Qᵢ` (same k as
training) → prompt → generate SQL. No server round-trip, no teacher at
inference. Global arms are evaluated **once per client pool** and reported
mean±std over K.

---

## 8. KD directions — RKD and KID, both from [10]

Both are online logit-level **reverse-KL** distillation plus auxiliary gold-CE
(`L = λ_ft·CE + λ_kd·RKL`, defaults 1:1). They differ in exactly one
ingredient — the sequence the teacher scores — so `kid − rkd` cleanly isolates
the value of imperfect data.

| | **RKD** (gold-data baseline) | **KID** (primary candidate) |
|---|---|---|
| KD target | gold `y` | imperfect `ŷ` = student one-pass rewrite of ρ-masked gold (ρ=0.2, Random) |
| Extra machinery | none | mask → one-pass greedy fill → splice |
| Teacher | cacheable offline (fixed target) | online (target tracks the student) |
| What transfers | teacher's distribution on gold SQL | + calibration under inference-style errors |
| Cost | ~2.0× SFT step latency (0 with cache) | ~2.0–2.4× (one extra `no_grad` student forward) |
| Gain vs SFT in [10] | +1.9 … +3.1 avg | +3.2 … +5.8 avg |

Tokenizer alignment (teacher/student share the Qwen2.5 tokenizer) is required
for RKL without MinED-style mapping — a constraint on the model pair.

**Which direction ships is decided by the running centralized PoC**
(`central_rkd` vs `central_kid`), not assumed. Dropped and deleted 2026-07-07:
Struct-SQL [11] QP-CoT, SeqKD, the whole offline teacher-target pipeline —
[11] stays a related-work reference only.

### 8.1 Deferred variant — asymmetric-context KD (Tier 3, added 2026-07-08)

Orthogonal to the RKD/KID target choice: the **context** each side sees when
scoring the KD pair. Default (symmetric): teacher and student condition on the
same DAIL context. The asymmetric variant gives the **teacher demos and the
student none**:

```text
p = teacher(P_ICL(x, demos_k3), tgt)     # teacher WITH demos
q = student(prompt(x, schema), tgt)      # student k=0, same target sequence
```

RKL then transfers the *effect of the demos* into the student's weights
(context-distillation line: Snell et al. arXiv:2209.15189), not just the 7B→1.5B
capacity gap — the demos' contribution no longer cancels between `p` and `q`.
If it works, the deployed student runs **k=0**: no retrieval/FAISS at the
client, shorter prompts, and clients with poor non-IID demo pools still inherit
the teacher's ICL knowledge from `P`.

- **Probe arm:** `central_rkd_asym` (teacher k=3, student k=0) vs the matched
  symmetric floor `central_rkd` at k=0 — one trainer-prompt change, everything
  else reused; RKD's offline logit cache still applies (teacher context fixed).
  **Code ready 2026-07-09** (`--kd-teacher-k 3`; `rkl_asym_loss` aligns the two
  prompts' target spans; runbook `notebooks/kd/README.md` §P1-probe) — the run
  itself stays gated on the items below.
- **Kill criterion:** `asym − sym(k0)` < ~1 EX on the centralized PoC (1 seed)
  → drop the variant, stay symmetric.
- **Order:** only after the RKD-vs-KID PoC verdict; scope change vs the approved
  outline → needs advisor sign-off before it ships in the paper.
- **Novelty check before committing:** read arXiv:2602.12275 (On-Policy Context
  Distillation) — if it already does RKL-based context distillation, our delta
  narrows to federated + DAIL + Text-to-SQL (+ KID-style imperfect targets).
- **Known risk:** 1.5B capacity may be too small to internalize the demos'
  effect (context-distillation literature reports weaker gains at small scale)
  — if so, report as analysis per repo convention.
- Note: invariant §11.4 (train/inference-consistent k at the client) is *not*
  violated — under this variant the client trains **and** infers at k=0; the
  asymmetry lives only inside the server distillation step.

### 8.2 Deferred variant — skew RKL loss (Tier 2, added 2026-07-11)

Orthogonal to the RKD/KID target choice: the **divergence formula** itself.
Default `rkl_div_loss` computes `RKL(q‖p)` against the raw teacher
distribution `p`; plain RKL's gradient can blow up wherever the student
assigns probability mass the teacher assigns ~0 (`log p(v) → -∞`) — a known
instability source at large capacity gaps ([DistiLLM], Ko et al. 2024,
arXiv:2402.03898).

**Skew RKL:** replace the denominator `p` with the mixture
`(1-λ)·p + λ·q` (λ small, paper default ~0.1) — pulls the reference
distribution toward the student's own mass, damping the blowup without
changing which direction (mode-seeking) the loss pursues.

- **Implemented 2026-07-11**, `skew_lambda` param on `rkl_div_loss` /
  `rkl_asym_loss` (`fedicl_sql/training/losses.py`), CLI `--rkl-skew-lambda`
  on `experiments/client_train/run.py`. Default `0.0` = byte-identical to
  plain RKL (mid-run `_ckpt/` resume across the code change is safe; no
  existing run is affected unless the flag is passed).
- **Probe arm:** `central_rkd_srkd` (or `central_kid_srkd`) — same data/config
  as the PoC's `central_rkd`/`central_kid`, `--rkl-skew-lambda 0.1` added.
  One-flag change, teacher/CE/mask machinery untouched.
- **Order:** after the RKD-vs-KID PoC verdict — run as a same-cost extension
  of whichever direction wins (not a third co-equal arm), 1 seed.
- **Not the DistiLLM-2 unification** (skew-KL on teacher-side data + skew-RKL
  on student-side data combined in one loss, arXiv:2503.07067) — that is a
  separate, costlier Tier-3 item (extra teacher forward per step) gated on
  `rkd − kid` coming out too close to call.

---

## 9. Default configuration (locked unless broken)

| Component | Value |
|---|---|
| Teacher | 7B frozen at server — default candidate Qwen2.5-Coder-7B-Instruct; FP16, vLLM for inference |
| Student | Qwen2.5-1.5B-Instruct + QLoRA (r=16, α=32, attn+MLP) |
| k_teacher | 3 (ablate 5) |
| k_student | 2, **same train/inference** (ablate 0/1/2) |
| Clients K | 8 |
| Partition | non-IID by database (Dirichlet over domain groups, α=0.5; ablate 0.1/IID) |
| Rounds / local epochs | T = 15, E = 2 |
| Server distill | 300 steps/round on `P`, batch 16, `λ_ft:λ_kd = 1:1` |
| KD loss | `CE + RKL(q‖p)` per [10] — reverse KL, full-vocab (common prefix), float32 |
| Public pool `P` | **TBD** — candidate: Spider held-out ~15% (~1k, DB-disjoint) |
| Eval | Spider dev (EX + EM, official algorithms) + Spider-Realistic (robustness) |
| Seeds | 3 for main results, 1 for ablations |
| Hardware | 1× RTX A5000 24 GB; vLLM for all inference/eval, HF+PEFT for training |

Engineering musts: cache teacher logits (Phase 1, one pass) · cache FAISS
index + DAIL rankings · keep only final+best adapters per config · fixed seeded
splits shared by every experiment.

---

## 10. Experiment arms

Arms are named by **feature, never letters** (Suggest.MD's M1–M4 map below for
cross-reading only). ICL is an eval-time overlay → suffix (`@k2`).

### Tier 1 — main results (3 seeds)

| Arm | Suggest.MD | What it is | Role |
|---|---|---|---|
| `central` | M1 | centralized FT student on pooled data, no FL | upper bound |
| `fedavg` | M2 | FedAvg + ICL, **no** server distill | main FL baseline |
| `fedkd` | M3 | **full Fed-ICKD**: FedAvg + ICL + server RKL-distill | proposed |
| `teacher` | M4 | teacher 7B + DAIL, zero fine-tune | reference (inference-only) |

Story: `fedkd > fedavg` (distillation works) and `fedkd` approaches
`central`/`teacher`.

### Centralized KD PoC (running now — precedes everything federated)

| Arm | KD target | CLI |
|---|---|---|
| `central_ft` | none (gold CE floor) | `--kd-direction none` |
| `central_rkd` | gold `y` | `--kd-direction rkd --teacher-model <id> [--teacher-4bit]` |
| `central_kid` | imperfect `ŷ` (ρ=0.2 Random) | `--kd-direction kid --mask-ratio 0.2 --teacher-model <id> [--teacher-4bit]` |

Ladder on identical Spider data from base: `central_rkd − central_ft` =
teacher-logit value; `central_kid − central_rkd` = imperfect-data value.
Runbook: `notebooks/kd/README.md`; entry: `experiments/client_train/run.py`.

### Tier 2 — ablations (1 seed each)

| # | Ablation | Serves |
|---|---|---|
| A1 | loss: CE-only / +RKL(gold) / +RKL(ŷ) | KD-direction contribution (⚠ do not cut) |
| A2 | k_student = 0 / 1 / 2 | is ICL worth it on a 1.5B student |
| A3 | pool `P`: Spider held-out / alt corpus / mix | pool-quality finding (⚠ do not cut) |
| A4 | Dirichlet α = 0.1 / 0.5 / IID | heterogeneity robustness |
| A5 | DAIL vs random selection | justify DAIL |
| A6 | RKL vs skew-RKL (§8.2, λ~0.1) on the PoC winner | divergence-formula robustness |

Cut order if time burns: A4 first, then A5, then A6. A1 + A3 never.

### Tier 3 — optional

0.5B student · k-robust training (random k) · FedProx (if A4 shows drift) ·
DP noise on adapters (only if a reviewer demands) · asymmetric-context KD
(teacher k=3 → student k=0, §8.1 — probe `central_rkd_asym`, kill if
< ~1 EX over the symmetric k=0 floor).

Negative results are framed as analysis, never hidden (e.g. if A2 says k=0 wins →
report it, move default to k=0, keep DAIL for the teacher).

---

## 11. Key invariants (never violate)

1. **Private data never leaves the client** — raw rows, `Sᵢ`, `Qᵢ`, demos,
   embeddings: no outgoing arrow. Only LoRA adapters cross, both directions.
2. **Teacher never touches client data** — structural: the teacher lives at the
   server and the server only ever receives adapters. Teacher's world = `P`.
3. **KD loss = reverse KL per [10]** (`CE + RKL`), never forward KL, never
   relational/hidden-state KD. Direction (RKD/KID) picked by the PoC.
4. **DAIL ICL is train/inference-consistent at the client** — same k, same
   selection, same demo format (`question + SQL`, no demo DDL). Mixing
   (train k=0, eval k>0) reintroduces the measured schema-bleed failure.
5. **Demo pool = own train data, never the test set.** Client → `Qᵢ`;
   teacher/server-distill → `P`. Test DBs are schema-disjoint from train →
   retrieval is always cross-schema, no leave-one-out.
6. **`P` is DB-disjoint from all client data and all eval sets.** A dataset used
   as `P` is disqualified as an eval benchmark (contamination).
7. **Fixed seeded splits, shared by every experiment.** 3 seeds mean±std for the
   main table; per-run `metrics.json` records the exact model ids used.
8. **One stack per comparison** — never compare numbers across different
   hardware/precision stacks.

---

## 12. Notation (canonical)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 8) |
| `T` | # federated rounds (default 15) |
| `E` | local epochs per round (default 2) |
| `k_student` | ICL shots at client train & inference (default 2, ablate 0/1/2) |
| `k_teacher` | ICL shots for teacher scoring on `P` (default 3, ablate 5) |
| `P` | public pool at the server (dataset TBD) |
| `ρ` | masking ratio for KID's imperfect data (default 0.2, Random) |
| `ŷ` | imperfect SQL — student one-pass rewrite of ρ-masked gold (KID target) |
| `p`, `q` | teacher / student logprob distribution over the KD target |
| `M_T` | teacher LLM (7B, **frozen, at the server**) |
| `Mᵢ`, `M_G` | client-i student / global student (base + aggregated adapter) |
| `Sᵢ`, `Qᵢ` | client-i private schema / private NL-SQL pairs |
| `θ`, `Δθᵢ` | LoRA adapter params / client-i delta |
| `λ_ft`, `λ_kd` | CE / RKL loss weights (default 1:1) |

**Research questions** (verbatim from the approved outline — do not rename):
RQ1 = Federated Learning effectiveness · RQ2 = In-Context Learning
effectiveness · RQ3 = Large-to-Small LM knowledge transfer & efficiency.

---

## 13. Legacy alias map (for reading old runs/docs)

Historical result dirs keep their old slugs; rename going-forward only.

| old label / slug | current name |
|---|---|
| `B0`, `base` | `base` (untrained student floor) |
| `B1`, teacher zero/few-shot | `teacher` |
| `B2`, `slm_only` | `local` (per-client solo LoRA — retired as a Tier-1 arm, kept as a possible extra baseline) |
| `B3`, `centralized_ft`, `b3_k0/k3` | `central` |
| `B4`, Centralized-ICL | `central@k3` |
| `B6` / `Ab3`, `ab3_fedavg` | `fedavg` |
| `M_G`, `m_g` | `fedkd` |
| `B7`, Fed-ICL [5] adapted | `fedicl_baseline` |
| `poc_ft` / `poc_rkd` / `poc_kid` | `central_ft` / `central_rkd` / `central_kid` |

Superseded designs (do not implement): client-side local teacher (2026-06-16 →
2026-07-07) · sequential two-step client training (Step 1 KD-pretrain → Step 2
FT) · combined per-step `λ₁·L_FT + λ₂(t)·L_KD` loss · CoT/Struct-SQL offline
targets · train-k=0 official default with eval-k=3 overlay.

---

## 14. Reference anchors

- **[10] KID** (Zhong et al. 2024, arXiv:2410.11371) — source of **both KD
  directions** (RKD = reverse KL on gold; KID = reverse KL on imperfect data)
  and of the reverse-KL-for-SQL argument (mode-seeking fits precise low-diversity
  tokens). Also the train/inference-mismatch argument backing consistent-k ICL.
- **[9] DAIL-SQL** — the ICL selection method (masked-question + query dual
  similarity, `question + SQL` demo format, small k).
- **[5] Fed-ICL** — parameter-free answer-fusion, QA not SQL; potential extra
  baseline + privacy-attack methodology.
- **[7] FedMKT / [8] FedCoLLM** — related work: server-side co-tuning/KD lines.
  Fed-ICKD's server distill is closest to FedCoLLM's placement; differentiate on
  (a) reverse-KL logit loss, (b) ICL-consistent clients, (c) Text-to-SQL
  formulation + pool-quality analysis.
- **[11] Struct-SQL** — related work only (CoT direction dropped 2026-07-07).
- **[4] Light-SQL / [6] IFed-ICL** — side references (retrieval masking; implicit
  federated ICL vectors).
- Aggregation theory anchor: McMahan (FedAvg) / FedProx.

Mechanism figure: `fig_architecture_source.png` + `fig1_architecture.md` predate
the 2026-07-08 server-side pivot — **Fig. 1 must be redrawn** (teacher box moves
from client to server; public pool `P` added) before §3 of the paper is written.
