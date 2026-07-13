# Fed-ICKD — System Architecture

**Federated In-Context Knowledge Distillation for Text-to-SQL** *(repo name: FedICL-SQL)*

> **Rewritten 2026-07-08; last consistency pass 2026-07-13.** This document
> supersedes every prior version and all prior re-alignment notes. Architecture
> source: `Suggest.MD` (accepted), with **one amendment**: the server-distillation
> loss is **reverse-KL logit distillation from [10]** (`CE + RKL(q‖p)`), NOT
> Suggest.MD's forward `KL(τ=2, top-50)` + relational RKD. Relational KD
> (distance/angle-wise on hidden states) is dropped entirely.
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

## 0. Status & scope (2026-07-13)

**Settled:**

- **Centralized KD PoC — COMPLETE (2026-07-11).** `central_ft` / `central_rkd`
  / `central_kid` trained and evaluated. KD signal is real: `rkd − ft` =
  +6.09 EX, McNemar p=3.1e-07 (107 vs 44 discordant rows). **Direction locked:
  RKD** (2026-07-12, user) — beats KID at every condition incl. under the exec
  gate. Caveat carried, not a gate: the paired gap vs KID (38 vs 23 rows,
  p=0.072) is NOT significant at 1 seed; seed 2 still needed before the gap
  size is a citable paper number, but the pick itself does not wait on it.
- **Pool `P` — RESOLVED (2026-07-12/13): BIRD schemas/DBs only.** BIRD's own
  (question, gold-SQL) pairs are permanently banned as CE/RKL targets
  (annotation quality — gate trace in §3.2); server-distill targets come from
  §8.3 (on-policy) + §8.4 (execution-anchored).
- **ICL role settled empirically (§5.2/§5.4):** selection sophistication never
  pays (4 model families, uniform + gated); the shipping overlay is the
  **verifier-gated retry**; current client default = train k=0 + gated
  fallback (measured leader, 1 seed — A2 decides vs `train-k2 consistent`).
- **Naming: "Fed-ICKD" stays**, regardless of the `k_teacher` 3-vs-0 ablation
  outcome (2026-07-12, user). ICL is an open experimental surface, not a
  single load-bearing ablation — apply it wherever it plausibly helps and
  report what's found.
- **No advisor gate on any pending item as of 2026-07-12** — server-side
  pivot, RKD pick, claim-3 reframe (§1), §8.1 kill, BIRD-`P` (§3.2), and
  V2-1/V2-2 (§8.3/§8.4) are all locked by user decision. Nothing in this doc
  currently blocks on advisor sign-off.

**Next (top priority):** the federated pipeline — Flower simulation (K=8),
weighted FedAvg, server-distill step on §8.3/§8.4 targets. The paper has no
federated number yet.

**Deferred:** Tier-2 ablations (§10) until the Tier-1 ladder has numbers; the
v2 extension arms (`fedkd_onpolicy`/`fedkd_onpolicy_exec`, §10) after
`fedavg`/`fedavg_pub`/`fedkd` land.

**Not planned by default:** DP noise on adapters (Tier 3 — add only if a
reviewer demands it; otherwise handled in the Limitations/Discussion section).
Do **not** claim formal DP in the paper.

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
3. An ICL analysis finding + a cheap **verifier-gated retry** overlay: on a
   fine-tuned/distilled student, demo *content* stops mattering — the full
   selection thang converges (random ≈ question-sim ≈ DAIL ≈ CodeS, uniform
   AND gated; repair sets nearly disjoint across demo sets) — so eval-time
   demos act as prompt perturbation, not in-context knowledge. The overlay
   (k=0 draft → SQL execution check → one retry under a perturbed prompt)
   is net-positive on every arm tested (+1.65…+4.35 EX); its load-bearing
   component is the execution verifier, with ICL as the perturbation medium
   (2026-07-11, 1 seed — see §5.2/§5.4). Plus an analysis of how public-pool
   quality affects distillation effectiveness.
   *(Reframed 2026-07-11 twice: from "DAIL-style ICL consistent between client
   training and inference" → "selective-ICL usage policy" → this, after the
   A5 random-demos attribution control landed (random repairs 22/146 vs DAIL
   23/146, McNemar p=1.00). Locked 2026-07-12 (user) — changes the approved
   outline's RQ2 emphasis, no advisor gate.)*

---

## 2. Architecture overview

```
┌──────────────────────── SERVER ─────────────────────────┐
│  Teacher M_T (7B, frozen)   Public pool P                │
│                             (BIRD schemas/DBs — never    │
│                              BIRD's own gold SQL, §3.2)  │
│                                                          │
│  [Phase 1 — offline, once]                               │
│  teacher generates SQL on P's schemas → execution        │
│  filter on P's DBs → targets y_pub (§8.4)                │
│  → cache teacher logits on y_pub (target fixed → RKD     │
│    cacheable; §8.3 on-policy needs the teacher online)   │
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
│  prompt [schema + question] (train k=0 default, §5.4)    │
│  → student 1.5B + LoRA (fp16 base)                        │
│  → L_CE(gold SQL) only, E local epochs — NO teacher      │
│                                                          │
│  [Phase 4 — inference, verifier-gated retry]             │
│  Student k=0 draft → execute on local DB → OK: done;     │
│  exec error only: retrieve k demos (any cheap method,    │
│  §5.2) + regenerate                                      │
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
  applies). ⚠️ The teacher/student pair is **not finalized** — the PoC verdict
  runs (P1/P2, LAB_LOG 2026-07-11 (2)) already used Qwen2.5-Coder-7B-Instruct
  as teacher; a model sweep (e.g. against Qwen2.5-Coder-1.5B as student) is
  still open. Every run records the ids actually used in its `metrics.json`
  (`model` = student, `teacher_model` = teacher, `""` when no KD), so results
  are never ambiguous.
- Serves two roles:
  1. **KD scorer** (Phase 1/3): one teacher-forced forward over the KD target —
     logprob distribution `p`, no decoding.
  2. **Reference arm** (`teacher`, M4): teacher + DAIL ICL, zero fine-tune,
     inference-only.
- Teacher ICL: DAIL selection **within `P`** (k_teacher = 3, ablate 5). Teacher
  and student condition on the **same** ICL context when computing the KD pair
  (`p`, `q`) — scoring them under different contexts corrupts the divergence.

### 3.2 Public pool `P` — BIRD schemas/DBs only (RESOLVED 2026-07-12/13)

> **Rule (scope clarified 2026-07-13):** BIRD's own (question, gold-SQL) pairs
> are **permanently off-limits as CE/RKL training targets** — confirmed by
> gate testing below (BIRD's own gold is the poison, not the schemas).
> Server-distill targets come from **§8.3 (on-policy) + §8.4
> (execution-anchored)** only. E0.1b (RKL on BIRD's native gold) is retired —
> do not run; its premise is moot now that the gold itself is known-poisoned.
> Runbook: `notebooks/kd/README.md` §6/§6c/§6e (§6b marked retired in place).
>
> **Not banned:** using BIRD's own gold as a **diagnostic/eval signal for
> teacher-side design decisions** (e.g. the `k_teacher` 0-vs-3 ICL ablation,
> §9) — the frozen teacher is never trained on it, so this doesn't reintroduce
> the poisoning mechanism (bad labels entering the student's parameters via
> CE/RKL). Report any such number with the same noise caveat as the gate
> trace below (BIRD Mini-Dev's documented 52.8% annotation-error rate) —
> treat as directional, not citable, especially for small deltas.

**Why BIRD:** `P` = BIRD train set (~9.4k questions, ~70 DBs) — size
comparable to Spider train (8.7k), human-curated, real executable DBs, well
known to reviewers, and distribution-disjoint from every client's Spider data
(the update-alignment rationale). A synthetic mega-corpus candidate (v2
proposal) was considered and dropped 2026-07-12 — overkill for a pool this
size, not carried as a fallback. This reverses the 2026-07-07 BIRD drop *for
the pool-`P` role only* — BIRD stays dropped as an eval benchmark **for
reporting the trained/distilled model's accuracy** (no cross-dataset claim;
`P` can't be an eval set for a model trained on it — contamination, invariant
#5). This is distinct from the teacher-diagnostic use above: the teacher is
frozen and never trained on `P`, so evaluating *it* on BIRD is not the
invariant-#5 violation — no claim about the federated model's accuracy is
being made either way.

**Gate trace (full detail: LAB_LOG 2026-07-12 sessions (9)–(15)):**

| probe | setup | EX (untrained floor = 50.00) | verdict |
|---|---|---|---|
| E0.1 | 1k BIRD-gold SFT from base, plain CE | 47.10 | FAIL — below the floor |
| Lever D | + evidence-Δ filter (drop most evidence-dependent rows) | 46.71 | FAIL — evidence-dependence is not the driver |
| Exec-bootstrap | ExeSQL-style (arXiv:2505.17231): drop BIRD gold entirely; teacher zero-shot SQL on BIRD schemas → keep what executes (831/1000) → CE | **50.00** | **PASS, exactly at the floor** — bootstrap-CE no longer harmful; the real value test = federated `fedavg` vs `fedkd` |

**Root cause:** BIRD's own annotation quality — not evidence-dependence, not
domain/dialect. Independent confirmation: BIRD Mini-Dev is documented 52.8%
annotation-error (VLDB CIDR 2026, "Text-to-SQL Benchmarks are Broken"). Side
signal: the exec-bootstrap arm also had the lowest exec-error rate of any arm
tested (20.5%, below even the Spider control's 26.7%) — execution-verified
targets teach more executable-SQL habits generally, not just fix BIRD.

**Engineering caveats (operative):**

- **Download weight — measured 2026-07-12: ~49 GB extracted** (`train/` alone
  39 GB; `dev_20240627/` adds 1.7 GB, not needed for the pool role —
  `download_bird.py` pulls both splits; a `--train-only` flag is unbuilt, low
  priority). Fetch once on the shared compute host (persistent disk per
  `CLAUDE.md`); delete both zip files after a verified extraction (~17 GB
  reclaimable).
- **`evidence` field + `database_description/*.csv`: drop both from every
  prompt on `P`** (decided 2026-07-12). Rationale: clients train/deploy on
  Spider, which has neither field, and `fedicl_sql.prompts.builder.
  build_prompt` renders schema DDL straight from sqlite (identical codepath
  for Spider and BIRD) — dropping both keeps the distilled global student's
  prompt format byte-identical to what it trains and deploys on at the
  client. A default motivated by train/inference format parity, not a bylaw —
  a future ablation may add evidence to `P`'s prompts and measure the cost.
  **Implemented:** `SpiderExample.evidence` (`fedicl_sql/data/spider.py`)
  captures the field from BIRD JSON into `processed_data/BIRD/*.csv` (default
  `""`), but no prompt-building code reads it (`tests/test_bird_data.py`
  asserts the capture). `database_description/*.csv` left untouched — wiring
  it = a new `schema_style` no adapter ever trained on (config audit
  2026-07-10: 0/21 runs), a costly research axis unrelated to the pool role.
- **Dialect gap** (BIRD SQLite is messier than Spider's): acceptable — `P` is
  a distillation corpus, not an eval set; largely moot now that BIRD's own
  gold is banned and targets are teacher-generated + execution-filtered.
- **Requirements kept:** public, DB-disjoint from clients **and** eval sets,
  distillation subset a few hundred–few thousand pairs per round (stratified;
  full 9.4k not required).

**Historical — evidence-poisoning escalation ladder (closed 2026-07-12/13):**
an escalation ladder (D: evidence-Δ filter → B: asymmetric teacher context
via `rkl_asym_loss` → C: evidence in both prompts as controlled ablation) was
staged against the risk that evidence-dependent BIRD gold poisons both loss
terms. D was built (`scripts/score_evidence_delta.py`,
`Δ = logprob_T(gold | prompt+evidence) − logprob_T(gold | prompt)`) and run
as the gate's second rung — **it failed** (table above), so the ladder is
closed along with its premise. Live remnant: the Δ histogram quantifies what
fraction of BIRD is evidence-dependent and feeds the A3 pool-quality
analysis.

### 3.3 Federated aggregation

```
θ_t ← θ_{t-1} + Σᵢ (nᵢ/n)·Δθᵢ      # McMahan weighting, NOT 1/K — non-IID sizes differ
M_G ← base_student + θ_t
```

- **Uploads/downloads = LoRA adapters only** (a few MB/round).
- LoRA-averaging caveat: averaging `A`,`B` factors separately ≠ averaging the
  products (`mean(BᵢAᵢ) ≠ mean(Bᵢ)·mean(Aᵢ)` — FedIT/FLoRA issue). Default
  mitigation: re-initializing every client from the same aggregated adapter
  each round; acknowledge in one sentence in the paper.
- **Candidate fix — FedEx-LoRA (ACL 2025, arXiv:2410.09432), Tier 2, to try:**
  a different mechanism from FedProx below — this one corrects the
  *aggregation math itself*, not client drift. Instead of only averaging
  `A`/`B` (inexact by construction), FedEx-LoRA adds a **residual error
  term to the frozen base weight matrix** each round to make the aggregated
  update exact (`Σᵢ BᵢAᵢ` recovered, not `mean(Bᵢ)·mean(Aᵢ)`), at claimed
  "minimal computational and communication overhead" — no architecture
  change, still adapter-only upload. Directly targets the caveat above
  instead of just acknowledging it. **Try if A4 (Dirichlet α sweep) shows
  the averaging-inexactness gap actually costs EX** — cheap to test (one
  aggregation-step change in `fedicl_sql/federated/aggregate.py`, same
  round loop) before assuming the one-sentence acknowledgment is enough.
- FedProx = Plan-B if drift under strong non-IID makes convergence unstable
  (Tier 3, triggered by ablation A4) — a client-objective fix, orthogonal to
  FedEx-LoRA's aggregation fix; both could apply if A4 shows problems on
  both fronts.

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
- **`y_pub` = execution-bootstrapped targets** (§3.2 rule: teacher-generated
  SQL on `P`'s schemas, execution-filtered on `P`'s DBs — never BIRD's own
  gold).
- **Direction: RKD — locked 2026-07-12** (gold-target reverse KL; PoC verdict
  §8). KID lost the PoC (−1.45 EX vs RKD); §8.3 (on-policy) + §8.4
  (execution-anchored) are the Tier-2 target upgrades on top of RKD.
- Implementation notes carried over from the PoC code (`train_online_kd`):
  Qwen2.5 7B vs 1.5B logit dims differ (V=152064 vs 151936, embedding padding)
  → slice both to the common vocab prefix; compute RKL in float32 (fp16 sum
  over a 150k vocab loses precision).
- **Role:** after FedAvg on non-IID clients the global model's behaviour is a
  blend of divergent local optima; distilling every round toward one fixed
  teacher on one shared pool pulls the aggregate back to a consensus
  (FedDF/FedMD line of argument) — a regularizer, not a data-augmentation trick.
- **Empirically validated, not just argued by analogy (2026-07-12/13,
  centralized proxy for the round mechanism):** warm-started an already
  fine-tuned student (`ft_no_icl`, EX=62.19) and continued training on the
  same BIRD exec-bootstrap slice (§6e, n=831), matched step count (831),
  CE-only vs CE+RKL:

  | continuation | EX | Δ vs pre-continuation (62.19) |
  |---|---|---|
  | CE-only (`central_ft_extra_bird`) | 59.38 | **−2.81** |
  | CE+RKL (`central_ft_then_kd_bird`) | 62.28 | **+0.09** |

  Plain further CE training on public data actively regresses an already-
  converged model (−2.81 EX, a forgetting-style drift); adding the teacher's
  RKL term neutralizes it (+0.09, flat within noise). Matched-control KD
  value = 62.28 − 59.38 = **+2.90 EX**. This is exactly the round-loop's own
  dynamic (client CE this round → server continues training the result) —
  the finding says server KD isn't optional polish, it's what stops the
  repeated-CE-rounds drift the regularizer framing predicts. LAB_LOG
  2026-07-12 (16) has the full trace.

**Caching:** for **RKD** the target (`y_pub`) and the ICL context are fixed
once Phase 1 generates them → teacher logits can be computed **once offline**
and reused every round. §8.3's on-policy targets track the current student →
teacher must run online each distillation step (the cost class KID paid). (The
hidden-state cache from Suggest.MD Phase 1 is dropped with relational KD.)

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

### 5.2 Demo selection — DAIL [9], demoted to baseline (2026-07-11/12)

> **Status:** no regime found where selection sophistication pays — uniform,
> gated, base, or FT/KD, across 4 model families (evidence below). DAIL
> survives as (i) the related-work baseline and (ii) the `teacher-k3 vs k0`
> distill ablation (§9/§10). Client fallback retrieval = anything cheap
> (random or a static cached demo set).

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

⚠️ **Status downgrade (2026-07-11, 1 seed, now COMPLETE 4/4): on a trained
(FT/KD) student, demo content does not matter.** Full A5 thang on
`central_rkd`, same adapter, same 146 gate-fired rows:

| retrieval | uniform k3 | gate exec | repairs |
|---|---|---|---|
| random | 66.83 | 70.41 | 22/146 |
| question-sim | 65.28 | 70.79 | 26/146 |
| dail_select | 65.86 | 70.50 | 23/146 |
| codes | — | 69.92 | 17/146 |

Gate spread 0.87pp, McNemar random-vs-DAIL **p=1.00**; uniform random-vs-DAIL
p=0.40. Repair sets nearly disjoint (pairwise overlap 9–11, all-4 common 5,
union 50/146 = 34%). **Attribution verdict: the repair mechanism is prompt
perturbation + execution verification, NOT in-context knowledge transfer** —
random demos from unrelated DBs repair broken drafts exactly as well as
DAIL-selected ones. Bonus trend (not significant, but mechanism-consistent):
uniform damage *increases* with demo relevance (breaks: random 58 < DAIL 74 <
qsim 83) — more-similar demos are more seductive to copy.

⚠️ **Extended 2026-07-12: selection sophistication is dead on base models too
— not just post-FT/KD.** Ran the full 4-way selection thang (dail/question/
random/codes, uniform k3, McNemar vs each family's own k0) across **4 base
model families**: Qwen2.5-0.5B/1.5B-Instruct, gemma-2-2b-it,
Llama-3.2-1B-Instruct.

| family (k0 EX) | dail | question | random | codes | dail vs random |
|---|---|---|---|---|---|
| qwen0.5B (23.31) | 28.05 (+49,p=.0007) | 27.76 (+46,p=.003) | **30.08 (+70,p=1e-5)** | 25.82 (n.s.) | p=0.20 |
| qwen1.5B (50.00) | **54.26 (+44,p=.004)** | 50.77 (n.s.) | 53.58 (+37,p=.012) | 52.13 (n.s.) | p=0.66 |
| gemma-2-2b (52.22) | 50.77 (n.s.) | 47.78 (**−46,p=.002**) | 49.52 (n.s.) | 50.97 (n.s.) | p=0.39 |
| llama-3.2-1b (37.33) | 35.01 (n.s.) | **30.46 (−71,p=1e-5)** | 35.69 (n.s.) | 37.23 (n.s.) | p=0.70 |

`dail vs random` never significant in any of the 4 families — including
qwen0.5B, where ICL helps most (+49…+70 EX net) **random beats DAIL there**
(30.08 vs 28.05). Two new findings:
- **ICL's sign is a model-family property, not a method property.** Positive
  and significant on both Qwen sizes; flat/negative on gemma and Llama. This
  mirrors (inverted) the post-FT pattern (gemma_ft +1.35 vs Qwen FT arms
  negative) — family idiosyncrasy dominates over anything method-level,
  4 families now on record for the scope caveat.
- **Question-sim is the worst performer, 3/4 families**, significantly
  harmful on 2 (gemma p=.002, llama p=1e-5) — plausible mechanism: pure
  question-similarity pulls in near-duplicate questions from *other* schemas,
  maximizing schema-bleed; random's dissimilarity makes it easier to ignore.

Consequences (supersedes the base-model exception below): (a) client fallback
retrieval = anything cheap; **random or a static cached demo set makes the
FAISS/retrieval stack optional entirely**, on base models too (static-demos
confirmation run = open Tier-3 item); (b) **no regime found where selection
sophistication pays** — not uniform, not gated, not base, not FT/KD, across
4 families. DAIL survives only as (i) a related-work baseline and (ii) the
`teacher-k3 vs k0` distill ablation (§5.6, §9) — expectations for (ii) are
now low: teacher itself shows uniform k3 ≈ k0 (78.53 vs 78.72, §5.6 eval),
so teacher-generation-time ICL doesn't help either; run it anyway (soft-label
distillation is a different regime from greedy generation) but don't bank
on it; (c) union 50 > any single set's ~23 motivates a **multi-retry gate**
(up to N retries with fresh random demos, keep first executable — ceiling ≈
oracle 73.0; open Tier-3 item).

Retrieval sites, always **within the local pool of whoever retrieves**:
(a) teacher on `P` retrieves from `P` (DAIL — the §9 `k_teacher` ablation);
(b) client student retrieves from its own `Qᵢ` (fallback path only — any
cheap method per the status above); (c) server distillation retrieves the
student's demos from `P`.

**Alternative selection methods considered, not adopted:** MARLO's learned
retriever and DCG-SQL's schema-link graph beat DAIL on base/API models
(+5.5/+10.9 EX resp., `icl_methods_survey.md` §2) but need a trained encoder
or graph — cite-only, no build. **Skills Similarity (SS)** — MARLO's own
baseline, LLM-summarized "skill" per question → embed → retrieve, no
training — is the one candidate cheap enough to probe (+2.6 EX over
masked-question sim on the same paper's ladder). **Implemented 2026-07-11**
(`--retrieval ss`, `fedicl_sql/retrieval/ss_select.py` — our own few-shot
prompt/exemplars, neither MARLO nor Skill-KNN [An et al. 2023] publishes
theirs; eval-time only, needs `--ss-gen-model`, default Qwen2.5-1.5B-Instruct
— verified the 0.5B generator collapses to boilerplate and tanks retrieval,
1.5B follows the pattern correctly). **Closed 2026-07-11 — do not run:** the
A5 gate condition fired (question-sim filled its column and converged with
DAIL/CodeS, uniform and gated) → SS is presumed to converge too; code stays
in-tree, no experiment scheduled. **DPC** (arXiv:2604.15163, training-free
execution-consistency candidate selection) is a different axis entirely
(selects among generated SQL candidates, not among demos) — cite in §2
Related Work as a training-free/execution-aware relative of the
selective-ICL gate (§8.1 analysis), not a retrieval alternative.

### 5.3 Student `Mᵢ` — 1.5B + LoRA

- Default candidate: Qwen2.5-1.5B-Instruct (tokenizer-aligned with the Qwen
  teacher → RKL without vocabulary mapping). LoRA r=16, α=32, targets attn+MLP,
  fp16 base (not quantized — 1.5B fp16 ≈3GB already fits the VRAM budget;
  4-bit is reserved for the 7B teacher on co-load, `--teacher-4bit`).
- Initialized from the broadcast global adapter each round.
- 0.5B student = Tier-3 extra model pair (claim-strengthening, optional).

### 5.4 Local training (Phase 2 — CE only, no teacher)

```
L = CE(student(P_ICL(q, Sᵢ, demos_Qᵢ)), gold SQL)     # E local epochs
```

- **Default (measured leader 2026-07-11, 1 seed): train k=0; inference =
  verifier-gated retry** (k=0 draft → exec check → k=3 fallback on error only;
  70.79 EX vs 68.28 ungated k=0 on `central_rkd`). This dissolves the
  train/inference-consistency tension: the student trains AND deploys at k=0
  for the ~86% of queries that pass the gate; the ICL fallback is a documented
  exception, not a mismatch. **A2 decides** (§10) between this and the
  alternative below — one seed is not a finding.
- **A2 comparison arm — `train-k2 consistent`** (same k at training and
  inference, the outline-era default). Its rationale: training with demos
  makes eval-time ICL in-distribution, removing the train/test-mismatch
  failure measured earlier (k0-trained student + k3 eval → schema bleed,
  −30 net flips, 54/109 hurts = `no such column`). ⚠️ Hypothesis, not
  established — centralized evals (LAB_LOG 2026-07-09/10, 1 seed) observed
  the opposite: the k3-trained arm regressed *most* under uniform eval-time
  ICL; train-time demo exposure did not immunize.
- Honest caveats carried with the gate: (a) it is ≥ its own k=0 floor **by
  construction** (fired rows are exec-failures, EX=0 already) — the empirical
  content is the repair rate (~15–18%) and the protection count, not the
  "beats k0" fact; (b) repair comes from prompt perturbation + execution
  verification, not demo content (A5 random-demos control, random ≈ DAIL,
  McNemar p=1.00; §5.2) — hence the honest name **verifier-gated retry**,
  with ICL demos as the perturbation medium; (c) the gate needs SQL execution
  against the client's own DB at inference — fine in our federated setting
  (the DB is local), but a no-exec-at-inference deployment would need a
  static gate signal (Tier 3).
- No teacher, no KD loss, no public data at the client. Light and
  VRAM-friendly — everything heavy lives at the server.

---

## 6. Federated round loop

```python
# Phase 1 (offline, once): target bootstrap + logit cache on P (§3.2 rule)
#   teacher zero-shot SQL on P's schemas → execution filter on P's DBs
#   → y_pub; cache teacher logits on y_pub (fixed target → cache valid)

Round t = 1 .. T:                                # T = 15 default
  1. SERVER broadcasts adapter θ_{t-1} → all K clients

  2. CLIENT i (Phase 2, parallel — simulated sequentially on one GPU):
       student.load_lora(θ_{t-1})
       for E local epochs over Qᵢ:
           L = CE(student(prompt(q, Sᵢ)), y)     # train k=0 default (§5.4; A2)
           update_lora(student, L)
       upload Δθᵢ = θᵢ − θ_{t-1}                 # adapters only

  3. SERVER (Phase 3):
       θ̃_t ← θ_{t-1} + Σᵢ (nᵢ/n)·Δθᵢ            # FedAvg
       student.load_lora(θ̃_t)
       for step in range(300):                   # distill on P, batch 16
           x, y_pub = next_batch(P);  demos = DAIL(x, pool=P, k=k_teacher)
           p = teacher(P_ICL(x, demos), y_pub)   # cached offline (RKD locked;
           q = student(P_ICL(x, demos), y_pub)   #  §8.3 samples ŷ instead)
           L = λ_ft·CE(y_pub) + λ_kd·RKL(q, p)
           update_lora(student, L)
       θ_t ← student adapter;  M_G ← base + θ_t

Inference (Phase 4, per client, no server / no teacher — verifier-gated retry):
       sql = M_G.generate(prompt(q, Sᵢ))          # k=0 draft, same as training
       if execute(sql, local_db) errors:          # gate fires on ~14–20% (1.5B)
           demos = retrieve(q, pool=Qᵢ, k=3)      # any cheap method (§5.2)
           sql = M_G.generate(P_ICL(q, Sᵢ, demos))
       return sql
```

---

## 7. Inference (deployment)

Each client runs `M_G` locally with the **verifier-gated retry** (§5.4):
k=0 draft → execute on the local DB → only on execution error, retrieve k
demos from its own `Qᵢ` (any cheap method — random/static, §5.2) and
regenerate. No server
round-trip, no teacher at inference; retrieval/FAISS cost is paid only on the
fallback path (~14–20% of queries for a 1.5B student, ~4% for 7B). Global
arms are evaluated **once per client pool** and reported mean±std over K.

---

## 8. KD directions — RKD and KID, both from [10]

Both are online logit-level **reverse-KL** distillation plus auxiliary gold-CE
(`L = λ_ft·CE + λ_kd·RKL`, defaults 1:1). They differ in exactly one
ingredient — the sequence the teacher scores — so `kid − rkd` cleanly isolates
the value of imperfect data.

| | **RKD** (gold-data baseline — **shipped**) | **KID** (lost the PoC) |
|---|---|---|
| KD target | gold `y` | imperfect `ŷ` = student one-pass rewrite of ρ-masked gold (ρ=0.2, Random) |
| Extra machinery | none | mask → one-pass greedy fill → splice |
| Teacher | cacheable offline (fixed target) | online (target tracks the student) |
| What transfers | teacher's distribution on gold SQL | + calibration under inference-style errors |
| Cost | ~2.0× SFT step latency (0 with cache) | ~2.0–2.4× (one extra `no_grad` student forward) |
| Gain vs SFT in [10] | +1.9 … +3.1 avg | +3.2 … +5.8 avg |

Tokenizer alignment (teacher/student share the Qwen2.5 tokenizer) is required
for RKL without MinED-style mapping — a constraint on the model pair.

**Verdict (PoC 2026-07-11; locked 2026-07-12): RKD ships.** `rkd − ft` =
+6.09 EX (McNemar p=3.1e-07); `kid − rkd` = **−1.45 EX** — opposite [10]'s
own headline. Leading suspect: the mask token (`pad_token_id`) substituted
mid-sequence is an artifact outside the pretrain distribution — §8.3's full
on-policy variant tests exactly that. Dropped and deleted 2026-07-07:
Struct-SQL [11] QP-CoT, SeqKD, the whole offline teacher-target pipeline —
[11] stays a related-work reference only.

### 8.1 KILLED — asymmetric-context KD (Tier 3, added 2026-07-08, killed 2026-07-11)

> **Status: dead by its own pre-registered criterion.** `central_rkd_asym`
> k=0 = 67.50 vs symmetric `central_rkd` k=0 = 68.28 → `asym − sym` =
> **−0.78 EX** < the +1 EX kill floor (measured 2026-07-09, 1 seed; doc
> flipped 2026-07-11). No further asym runs. Closed 2026-07-12 (user) — no
> advisor note needed, it died before shipping. Section kept for the record.

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
- **Order:** moot — killed before shipping (see status banner above).
- **Novelty check before committing:** read arXiv:2602.12275 (On-Policy Context
  Distillation) — if it already does RKL-based context distillation, our delta
  narrows to federated + DAIL + Text-to-SQL (+ KID-style imperfect targets).
- **Known risk:** 1.5B capacity may be too small to internalize the demos'
  effect (context-distillation literature reports weaker gains at small scale)
  — if so, report as analysis per repo convention.
- Note: the client trains **and** infers at k=0 under this variant either way
  (the asymmetry lives only inside the server distillation step) — moot now
  that §11's client-ICL-policy rule was dropped, but recorded for clarity.

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
- **Probe arm:** `central_rkd_srkd` — same data/config as the PoC's
  `central_rkd` (the winning direction), `--rkl-skew-lambda 0.1` added.
  One-flag change, teacher/CE machinery untouched.
- **Order:** A6 (§10) — a same-cost extension of RKD, 1 seed.
- **Not the DistiLLM-2 unification** (skew-KL on teacher-side data + skew-RKL
  on student-side data combined in one loss, arXiv:2503.07067) — that is a
  separate, costlier Tier-3 item (extra teacher forward per step) gated on
  `rkd − kid` coming out too close to call.

### 8.3 PROPOSED — on-policy distillation (Tier 2, from `fed_ickd_v2_proposal.md` V2-1, merged + locked 2026-07-12)

> **Status: proposed, not built, locked (user, no advisor gate).** Order:
> after `fedavg`/`fedavg_pub`/`fedkd` headline numbers land (§10).

Natural extension of the RKD→KID ladder. Lit: GKD (Agarwal et al.,
arXiv:2306.13649), on-policy distillation survey (arXiv:2604.00626), Thinking
Machines' practitioner writeup. Mechanism: student samples a full SQL `ŷ` →
teacher runs **one forward pass** scoring the student's own tokens → reverse-KL
per-token as the signal. No reward model, no rollout search.

- **Why it fits:** `train_online_kd` already co-loads the teacher (4-bit) and
  computes RKL/skew-RKL (§8.2) — the only change is swapping KID's
  `mask_rewrite` step (mask → one-pass fill → splice) for the student
  sampling its own complete target. Small trainer change, same VRAM profile,
  same loss code.
- **Motivating anomaly it directly tests:** `kid − rkd` = −1.45 EX (opposite
  [10]'s own headline, LAB_LOG 2026-07-11 (2)) — leading suspect is the
  mask-token (`pad_token_id`) substituted mid-sequence being an artifact
  outside the pretrain distribution. Full on-policy removes masking entirely
  — if the gap closes or flips, that confirms the mask-token hypothesis
  rather than "KID doesn't work here."
- **Ladder (one ingredient per rung, isolates the masking variable cleanly):**
  `rkd` (off-policy, gold `y`) → `kid` (semi, masked-splice `ŷ`) →
  `onpolicy` (full, sampled `ŷ`).
- **Cost:** literature reports 9–30× cheaper than off-policy KD, 50–100×
  cheaper than RL (Thinking Machines' numbers — external claim, not yet
  measured on this stack). On our stack the cost class matches KID's (teacher
  forward once per step, no offline logit cache — same as KID already pays).
- **Risk:** student generation adds per-step cost beyond KID's single
  fill-forward. Mitigation: pre-batch sampling per round (semi-online)
  instead of per-step, teacher still one forward per sample.

### 8.4 PROPOSED — execution-anchored server distillation (Tier 2, from `fed_ickd_v2_proposal.md` V2-2, merged + locked 2026-07-12)

> **Status: proposed, not built, locked (user, no advisor gate).** Does
> **not** strictly require §8.3 — KID's existing masked-splice `ŷ` can also
> be execution-filtered (imperfect targets can fail to execute too); pairing
> with full on-policy (`fedkd_onpolicy_exec`, §10) is the strongest combined
> arm but not a hard dependency.

Lit consensus 2025–26 for small-model text-to-SQL converges on execution
feedback: SLM-SQL (arXiv:2507.22478 — 1.5B reaches 67.08 EX on BIRD dev via
SFT+GRPO), FINER-SQL (arXiv:2605.03465 — dense execution reward),
Arctic-Text2SQL-R1 (GRPO execution reward, SOTA BIRD), ExeSQL
(execution-driven rejection sampling). **Not full RL** — no reward model, no
GRPO:

- During server distill, the student-sampled `ŷ` (from §8.3, or KID's
  masked-splice `ŷ`) executes against `P`'s DB → only distill (or upweight)
  samples that execute successfully.
- **Infra:** reuses the SQLite execution + 60s progress-handler timeout
  already in `fedicl_sql/eval/metrics.py` — no new execution engine. Requires
  `P` to have real executable DBs — satisfied by BIRD (§3.2).
- **Novelty value:** the strongest available differentiator vs FedCoLLM [8]
  (novelty claim 2, §1) — FedCoLLM distills blind on public data with no
  verifier; this attaches a cheap per-sample verifier to the distill loop.
  Proposed name: **execution-anchored server distillation**.
- **Risk:** filter bias toward easy queries (hard queries execute less
  often). Mitigation: report a soft-weight mode alongside the hard-filter
  mode, and measure the hardness mix of kept samples, not just aggregate EX.
- **Full GRPO explicitly rejected:** compute (N samples/query + reward
  pipeline on one A5000) and scope don't allow it. Note as a Tier-3 item only
  if a reviewer demands it.

---

## 9. Default configuration (locked unless broken)

| Component | Value |
|---|---|
| Teacher | 7B frozen at server — default candidate Qwen2.5-Coder-7B-Instruct; FP16, vLLM for inference |
| Student | Qwen2.5-1.5B-Instruct + LoRA, fp16 base (r=16, α=32, attn+MLP) |
| k_teacher | 3 (ablate **0** first — teacher-ICL value is the one place selection/ICL can still earn its keep post-A5, §5.2; then 5) |
| k_student | train k=0 + **exec-gated k=3 fallback at inference** (measured leader 2026-07-11, 1 seed; A2 decides vs `train-k2 consistent`) |
| Clients K | 8 |
| Partition | non-IID by database (Dirichlet over domain groups, α=0.5; ablate 0.1/IID) |
| Rounds / local epochs | T = 15, E = 2 |
| Server distill | 300 steps/round on `P`, batch 16, `λ_ft:λ_kd = 1:1` |
| KD loss | `CE + RKL(q‖p)` per [10] — reverse KL, full-vocab (common prefix), float32 |
| KD direction | **RKD — locked 2026-07-12** (PoC verdict, §8); §8.3/§8.4 = Tier-2 target upgrades |
| Public pool `P` | **BIRD schemas/DBs** — never BIRD's own gold SQL (resolved 2026-07-12/13, §3.2); targets via §8.3/§8.4 only; distill subset a few k, stratified |
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
| `fedavg_pub` | — | FedAvg + CE-only on `P` gold, **no** teacher | control (added 2026-07-12): isolates public-data exposure from teacher-distill effect — confounded away otherwise, `fedkd` sees `P` data AND a teacher, `fedavg` sees neither (session 2026-07-06). `fedkd − fedavg_pub` = the real teacher value |
| `fedkd` | M3 | **full Fed-ICKD**: FedAvg + ICL + server RKL-distill | proposed |
| `teacher` | M4 | teacher 7B + DAIL, zero fine-tune | reference (inference-only) |

Story: `fedkd > fedavg_pub > fedavg` (distillation adds value beyond just
seeing public data, which itself adds value beyond none) and `fedkd`
approaches `central`/`teacher`.

### Federated v2 extension arms (Tier 2, proposed, locked — no advisor gate, §8.3/§8.4)

Same server-distill step, target/filtering swapped one ingredient at a time.
Run **after** the Tier-1 ladder above has real numbers — these are additive,
not a replacement for the headline pair.

| Arm | Adds vs `fedkd` | Mechanism |
|---|---|---|
| `fedkd_onpolicy` | KD target: gold `y` → student-sampled `ŷ` | §8.3 — tests the mask-token-artifact hypothesis behind `kid − rkd` |
| `fedkd_onpolicy_exec` | + execution filter/weight on the sampled `ŷ` | §8.4 — execution-anchored distillation; the stronger novelty differentiator vs FedCoLLM [8] |

Build order (`fed_ickd_v2_proposal.md` §Thứ tự build): probe `P` + student
sweep → `fedavg`/`fedavg_pub`/`fedkd` (make-or-break) → these two rows as
arms bolted onto a standing ladder → Tier-3 cheap items in parallel when GPU
is idle.

### Centralized KD PoC — COMPLETE 2026-07-11, verdict: RKD

| Arm | KD target | CLI |
|---|---|---|
| `central_ft` | none (gold CE floor) | `--kd-direction none` |
| `central_rkd` | gold `y` | `--kd-direction rkd --teacher-model <id> [--teacher-4bit]` |
| `central_kid` | imperfect `ŷ` (ρ=0.2 Random) | `--kd-direction kid --mask-ratio 0.2 --teacher-model <id> [--teacher-4bit]` |

Ladder on identical Spider data from base: `central_rkd − central_ft` = +6.09
EX (teacher-logit value, McNemar p=3.1e-07); `central_kid − central_rkd` =
−1.45 EX (imperfect-data value — negative here; §8.3 tests the mask-token
hypothesis). Arms stay runnable for seeds + A1/A6.
Runbook: `notebooks/kd/README.md`; entry: `experiments/client_train/run.py`.

### Tier 2 — ablations (1 seed each)

| # | Ablation | Serves |
|---|---|---|
| A1 | loss: CE-only / +RKL(gold) / +RKL(ŷ) | KD-direction contribution (⚠ do not cut) |
| A2 | `train-k0 + exec-gate` vs `train-k2 consistent` (uniform k=0/1/2 as secondary rows) | which ICL usage policy ships — reframed 2026-07-11, gate is the measured leader |
| A3 | pool `P`: BIRD train (default) / Spider held-out / mix | pool-quality finding (⚠ do not cut) — Spider held-out = the in-distribution contrast to BIRD's cross-distribution default |
| A4 | Dirichlet α = 0.1 / 0.5 / IID | heterogeneity robustness |
| A5 | selection thang: random / question-sim / DAIL / codes, uniform + exec-gate, same adapter (`central_rkd`) | **DONE 4/4, 2026-07-11 — converged** (gate: 70.41 / 70.79 / 70.50 / 69.92, random-vs-DAIL p=1.00). Attribution settled: repair = perturbation + exec-verify, not demo content (§5.2). Table ships as-is in §5; no further A5 runs |
| A6 | RKL vs skew-RKL (§8.2, λ~0.1) on the PoC winner | divergence-formula robustness |

Cut order if time burns: A4 first, then A5, then A6. A1 + A3 never.

### Tier 3 — optional

0.5B student · k-robust training (random k) · FedProx (if A4 shows drift) ·
DP noise on adapters (only if a reviewer demands) · static/exec-free gate
signal (deployment variant of the exec gate for settings where inference-time
DB execution is unavailable) · **multi-retry gate** (up to N retries with
fresh random demos on exec-failure, keep first executable — A5 union says
ceiling ≈ oracle 73.0 on `central_rkd`, i.e. ~+4.8pp vs k0; 1 eval run,
existing adapter) · **static-demos gate** (fallback uses one fixed cached
demo set — zero retrieval infra at the client; 1 confirmation run, predicted
≈ random per §5.2) · ~~asymmetric-context KD~~ (**killed 2026-07-11**, §8.1 —
criterion met at −0.78 EX) · ~~Skills Similarity (SS) retrieval~~ (**closed
2026-07-11**, §5.2 — A5 thang converged 4/4 incl. random; selection
sophistication is dead post-FT/KD, SS included; code in-tree, no run).

Negative results are framed as analysis, never hidden (e.g. if A2 says k=0 wins →
report it, move default to k=0, keep DAIL for the teacher).

---

## 11. Key invariants (never violate)

1. **Private data never leaves the client** — raw rows, `Sᵢ`, `Qᵢ`, demos,
   embeddings: no outgoing arrow. Only LoRA adapters cross, both directions.
2. **Teacher never touches client data** — structural: the teacher lives at the
   server and the server only ever receives adapters. Teacher's world = `P`.
3. **KD loss = reverse KL per [10]** (`CE + RKL`), never forward KL, never
   relational/hidden-state KD. Direction: **RKD** (PoC verdict, locked
   2026-07-12).
4. **Demo pool = own train data, never the test set.** Client → `Qᵢ`;
   teacher/server-distill → `P`. Test DBs are schema-disjoint from train →
   retrieval is always cross-schema, no leave-one-out.
5. **`P` is DB-disjoint from all client data and all eval sets.** A dataset used
   as `P` is disqualified as an eval benchmark (contamination).
6. **Fixed seeded splits, shared by every experiment.** 3 seeds mean±std for the
   main table; per-run `metrics.json` records the exact model ids used.
7. **One stack per comparison** — never compare numbers across different
   hardware/precision stacks.

*(Dropped 2026-07-12: the former #4, "client ICL usage policy declared, not
mixed" — it hard-forbade uniform eval-time ICL on a k=0-trained model, but
that exact configuration is what A2/A5/the k3dail runs already explore on
purpose, and is where §5's findings come from. The underlying observation
(uniform ICL hurts the tested arms; the gate is the current measured leader)
stays as an empirical §5.4 finding — status "hypothesis, not established,"
explicitly not a bylaw. A "never violate" invariant is the wrong container
for a result that a future run could overturn; ICL config choices are a
research question, not a constraint like privacy/leakage/hygiene are.)*

---

## 12. Notation (canonical)

| Symbol | Meaning |
|---|---|
| `K` | # clients (default 8) |
| `T` | # federated rounds (default 15) |
| `E` | local epochs per round (default 2) |
| `k_student` | ICL shots at client training (default **0**; inference = gated k=3 fallback, §5.4; A2 decides) |
| `k_teacher` | ICL shots for teacher scoring on `P` (default 3, ablate 0 then 5) |
| `P` | public pool at the server — **BIRD schemas/DBs, never BIRD's own gold** (§3.2) |
| `y_pub` | server-distill target on `P` — teacher-generated, execution-filtered SQL (§3.2/§8.4) |
| `ρ` | masking ratio for KID's imperfect data (default 0.2, Random) |
| `ŷ` | imperfect SQL — KID: student one-pass rewrite of ρ-masked gold; §8.3: student-sampled |
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
- **FedEx-LoRA** — Singhal et al., ACL 2025, arXiv:2410.09432 — exact LoRA
  aggregation via a residual term on the frozen base weight, candidate fix
  for the §3.3 LoRA-averaging caveat (Tier 2, try if A4 shows the gap costs
  EX).
- **ExeSQL** — arXiv:2505.17231 — execution-driven bootstrap (generate →
  exec-filter → train); the recipe behind `P`'s target rule (§3.2) and the
  §8.4 execution-anchored distillation.

Mechanism figure: `fig_architecture_source.png` + `fig1_architecture.md` predate
the 2026-07-08 server-side pivot — **Fig. 1 must be redrawn** (teacher box moves
from client to server; public pool `P` added) before §3 of the paper is written.
