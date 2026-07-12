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

- **PoC complete (2026-07-11):** `central_ft` / `central_rkd` / `central_kid`
  all trained and evaluated. KD signal is real: `rkd − ft` = +6.09 EX,
  McNemar p=3.1e-07 (107 vs 44 discordant rows). Direction: **RKD — locked**
  as the server-distill direction (2026-07-12, user) — beats KID at every
  condition incl. under the exec gate. Caveat carried, not a gate: the paired
  gap vs KID (38 vs 23 rows, p=0.072) is NOT significant at 1 seed; seed 2
  still needed before the gap size is a citable paper number, but the pick
  itself does not wait on it. Building the federated pipeline is unblocked
  and is now the top priority (the paper has no federated number yet).
- **Naming: "Fed-ICKD" stays**, regardless of the `k_teacher` 3-vs-0 ablation
  outcome (2026-07-12, user). ICL is an open experimental surface, not a
  single load-bearing ablation — apply it wherever it plausibly helps
  (teacher-distill context, client fallback retrieval, other points as they
  surface) and report what's found; the name does not hinge on any one of
  them landing.
- **No advisor gate on any pending item as of 2026-07-12** — server-side
  pivot, RKD pick, claim-3 reframe (§1), §8.1 kill, BIRD-`P` reversal (§3.2),
  the 3-tier ICL policy, and V2-1/V2-2 (§8.3/§8.4) are all locked by user
  decision. Nothing in this doc currently blocks on advisor sign-off.
- **Deferred until the PoC has a verdict:**
  - ~~which dataset serves as the public pool `P`~~ **DECIDED 2026-07-12:
    `P` = BIRD train** (user decision; reverses the 2026-07-07 drop for the
    pool role only — §3.2 has the caveats + the E0.1 transfer-probe gate),
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
│  Teacher M_T (7B, frozen)   Public pool P = BIRD train   │
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
│  [Phase 4 — inference, gated ICL]                        │
│  Student k=0 draft → execute on local DB → OK: done;     │
│  exec error only: retrieve k demos + regenerate          │
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

### 3.2 Public pool `P` — **BIRD train (decided 2026-07-12, user)**

- **`P` = BIRD train set** (~9.4k questions, ~70 DBs) — size comparable to
  Spider train (8.7k), human-curated, real DBs, well known to reviewers, and
  distribution-disjoint from every client's Spider data (the update-alignment
  rationale). A synthetic mega-corpus candidate (v2 proposal) was considered
  and dropped 2026-07-12 (2) — judged overkill for a distillation pool this
  size; not carried as a fallback.
- This **reverses the 2026-07-07 BIRD drop** *for the pool-`P` role only* —
  BIRD stays dropped as a secondary eval benchmark (no cross-dataset claim,
  and `P` cannot be an eval set anyway — contamination). The 07-07 drop
  reasons carry over as engineering caveats, mitigated by the narrower role:
  - **download weight — measured, not estimated (2026-07-12): ~49 GB
    extracted** (`train/` alone is 39 GB — `train.zip` 8.3 GB plus a
    redundant nested `train_databases.zip` 8.7 GB left over post-extraction
    that reclaims space if deleted; `dev_20240627/` adds 1.7 GB, not needed
    for `P` at all — only fetched because `download_bird.py` pulls both
    splits). Fetch once on the shared compute host (persistent disk per
    `CLAUDE.md`), delete both zip files after a verified extraction (~17 GB
    reclaimable), and prefer NOT downloading the dev split when it's only for
    the pool role (a `--train-only` flag would need adding to
    `download_bird.py`, not built yet — low priority, disk is fine for now).
  - **`evidence` field + `database_description/*.csv` — DECIDED 2026-07-12:
    drop both from every prompt on `P`.** Rationale, not laziness: clients
    train/deploy on Spider, which has neither field, and `fedicl_sql.prompts.
    builder.build_prompt` renders schema DDL straight from sqlite (identical
    codepath for Spider and BIRD) — dropping both keeps the distilled global
    student's prompt format byte-identical to what it trains and deploys on
    at the client — a design default motivated by train/inference format
    parity (§11 dropped the hard client-ICL-policy rule 2026-07-12, but the
    reasoning still applies here as a default, not a bylaw: nothing stops a
    future ablation from adding evidence to `P`'s prompts and measuring
    whether the mismatch actually costs anything, per the same "this is a
    research question, not a constraint" logic). **Implemented, not just
    declared:** `SpiderExample.evidence`
    (`fedicl_sql/data/spider.py`) captures the field from BIRD JSON
    (`fedicl_sql/data/bird.py`, default `""` for Spider/rows without one) so
    it survives into `processed_data/BIRD/*.csv` for the ablation below, but
    no prompt-building code reads it — `tests/test_bird_data.py` asserts the
    capture, `build_prompt` asserts nothing (silence is the contract).
    `database_description/*.csv` is left untouched entirely — schema stays
    `schema_style=full` DDL-only for both datasets, no wiring done.
  - **Known risk, not yet mitigated (rewritten 2026-07-12 — BOTH loss terms
    are exposed, not just RKL):** several BIRD gold queries are only decidable
    given `evidence` (enum/threshold definitions, cryptic column semantics).
    On those rows, with evidence dropped:
    1. **RKL term:** the teacher (`score_logits`, teacher-forced on gold)
       assigns low probability to gold tokens it can't justify → noisy RKL
       gradient at exactly those positions.
    2. **CE term (`λ_ft·CE(y_pub)`) — the worse one, previously unrecorded:**
       the server-distill CE trains the student to emit gold SQL that is
       *underivable from its own prompt* — i.e. it teaches the student to
       hallucinate columns/literals. Client CE is unaffected (never sees
       BIRD), but the global student takes this gradient every round.
    **Escalation ladder if `fedkd` on BIRD underperforms suspiciously
    (order revised 2026-07-12 — filter-first; the old asym-first path only
    fixed RKL and left CE poisoned):**
    - **D (first lever) — filter `P` by evidence-Δ scoring.** One offline
      teacher pass (2 teacher-forced forwards/row, same infra as the Phase-1
      RKD logit cache — near-free if run in that pass):
      `Δ = logprob_T(gold | prompt+evidence) − logprob_T(gold | prompt)`;
      keep low-Δ rows (gold self-contained given schema) for the distill
      subset, drop high-Δ rows. Fixes CE *and* RKL, keeps KD symmetric (the
      offline logit cache stays valid), and §3.2's subset requirement (a few
      hundred–few thousand of 9.4k per round) leaves ample room to filter.
      The `evidence` column is already captured in `processed_data/BIRD/*.csv`
      (2026-07-12) — no re-processing needed. **Bonus: the Δ histogram is a
      quantitative "what fraction of BIRD is evidence-dependent" number that
      feeds the A3 pool-quality analysis directly** — this filter is part of
      the pool-quality contribution, not a patch.
    - **B (second lever, only if filtering isn't enough)** — asymmetric
      teacher context: reuse `teacher_prompt_ids` (`dataset.py`) +
      `rkl_asym_loss` (`losses.py`, §8.1 — killed for its original k-mismatch
      purpose, plumbing generic) to score the teacher on an
      evidence-augmented prompt while the student-facing prompt stays
      evidence-free. Caveats: fixes RKL only (CE still poisoned unless
      combined with D), and a teacher made confident by evidence pulls the
      student toward tokens it cannot ground — memorization pressure.
    - **C (last resort, controlled ablation only)** — evidence in both
      prompts on `P`: fixes both terms but reintroduces the train/inference
      format mismatch at the server side (same failure class as the old
      −30-flip k-mismatch bug); only as a measured A3-adjacent ablation,
      never as a silent default.
    None of this is built now — scope discipline; the E0.1 probe stays the
    gate, and D's Δ-scoring may be run opportunistically inside the Phase-1
    cache pass even if the probe passes (near-zero marginal cost, feeds A3).
  - **`database_description/*.csv`: dropped permanently, no escalation.**
    Wiring it = a new `schema_style`, which no adapter has ever trained on
    (config audit 2026-07-10: 0/21 runs) → a separate, costly research axis
    unrelated to the pool role. `evidence` carries most of the
    gold-decidability information anyway.
  - **dialect gap** (BIRD SQLite is messier than Spider's): acceptable —
    `P` is a distillation corpus, not an eval set; the E0.1-style transfer
    probe (below) is the kill-switch if the gap poisons the student.
- **Gate before committing GPU time — two stages, both mandatory (2026-07-12):**
  1. **E0.1** — 1k BIRD-gold SFT **from base**, plain CE → eval Spider dev.
     Cheap data-quality kill-switch (BIRD dialect/distribution vs Spider).
  2. **E0.1b** — RKL-KD on the same 1k slice, warm-started from `central_ft`
     (already fine-tuned), not base. E0.1 alone does **not** validate the
     mechanism the server-distill step actually runs (RKL-KD on top of an
     already-trained student, not gold-CE from base) — it only clears the
     CE/data-quality half of the risk (the CE-poisoning note above); E0.1b
     is the check on the RKL/already-fine-tuned-model half. Run only after
     E0.1 passes.

  Either failing → escalate before building the distill loop on `P` (E0.1
  fail → reconsider `P` itself, §3.2 fallback; E0.1b fail → pull the
  evidence-Δ filter, lever D above, before building the full loop). Runbook:
  `notebooks/kd/README.md` §6/§6b.
- Requirements kept: public, DB-disjoint from clients **and** eval sets,
  distillation subset a few hundred–few thousand pairs (subset BIRD train,
  stratified; full 9.4k not required per round).

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

Applied at three sites, always **within the local pool of whoever retrieves**:
(a) teacher on `P` retrieves from `P`; (b) client student retrieves from its
own `Qᵢ`; (c) server distillation retrieves the student's demos from `P`.

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
  inference** (default k_student = 2; ablate 0/1/2). Rationale: training with
  demos should make eval-time ICL in-distribution, removing the
  train/test-mismatch failure measured earlier (k0-trained student + k3 eval →
  schema bleed, −30 net flips, 54/109 hurts = `no such column`).
  ⚠️ **Status: hypothesis, not established.** Centralized PoC evals (LAB_LOG
  2026-07-09/10 — 1 seed, Spider dev, Qwen-family) observed the opposite:
  train-time demo exposure did not immunize (the k3-trained arm regressed most
  under uniform eval-time ICL), while an exec-gated ICL overlay was net-positive
  on all arms tested. Narrow-scope observations — neither direction is a
  finding until seeds / Spider-Realistic / more families confirm; A2 decides.
  **Best measured config so far (2026-07-11, 1 seed): train k=0 + gated
  inference** (k=0 draft → exec check → k=3 fallback on error only; 70.79 EX
  vs 68.28 ungated k=0 on `central_rkd`). This also dissolves the
  train/inference-consistency tension: the student trains AND deploys at k=0
  for the ~86% of queries that pass the gate; the ICL fallback is a documented
  exception, not a mismatch. A2 is reframed accordingly (§10): the deciding
  comparison is `train-k0 + gate` vs `train-k2 consistent`, not uniform-k
  sweeps. Two honest caveats carried with it: (a) the gate is ≥ its own k=0
  floor **by construction** (fired rows are exec-failures, EX=0 already) — the
  empirical content is the repair rate (~15–18%) and the protection count, not
  the "beats k0" fact; (b) RESOLVED 2026-07-11: the A5 random-demos control ran — repair comes
  from prompt perturbation + execution verification, not demo content
  (random ≈ DAIL, McNemar p=1.00; §5.2) — so the overlay's honest name is
  **verifier-gated retry**, with ICL demos as the perturbation medium. Also: the gate needs SQL execution against the client's own DB at
  inference — fine in our federated setting (the DB is local), but a
  no-exec-at-inference deployment would need a static gate signal (open item).
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

Inference (Phase 4, per client, no server / no teacher — gated ICL):
       sql = M_G.generate(prompt(q, Sᵢ))          # k=0 draft, same as training
       if execute(sql, local_db) errors:          # gate fires on ~14–20% (1.5B)
           demos = retrieve(q, pool=Qᵢ, k=3)      # question-sim default (§5.2)
           sql = M_G.generate(P_ICL(q, Sᵢ, demos))
       return sql
```

---

## 7. Inference (deployment)

Each client runs `M_G` locally with the **exec-gated ICL policy** (§5.4):
k=0 draft → execute on the local DB → only on execution error, retrieve k
demos from its own `Qᵢ` (question-sim default) and regenerate. No server
round-trip, no teacher at inference; retrieval/FAISS cost is paid only on the
fallback path (~14–20% of queries for a 1.5B student, ~4% for 7B). Global
arms are evaluated **once per client pool** and reported mean±std over K.

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
- **Probe arm:** `central_rkd_srkd` (or `central_kid_srkd`) — same data/config
  as the PoC's `central_rkd`/`central_kid`, `--rkl-skew-lambda 0.1` added.
  One-flag change, teacher/CE/mask machinery untouched.
- **Order:** after the RKD-vs-KID PoC verdict — run as a same-cost extension
  of whichever direction wins (not a third co-equal arm), 1 seed.
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
| Student | Qwen2.5-1.5B-Instruct + QLoRA (r=16, α=32, attn+MLP) |
| k_teacher | 3 (ablate **0** first — teacher-ICL value is the one place selection/ICL can still earn its keep post-A5, §5.2; then 5) |
| k_student | train k=0 + **exec-gated k=3 fallback at inference** (measured leader 2026-07-11, 1 seed; A2 decides vs `train-k2 consistent`) |
| Clients K | 8 |
| Partition | non-IID by database (Dirichlet over domain groups, α=0.5; ablate 0.1/IID) |
| Rounds / local epochs | T = 15, E = 2 |
| Server distill | 300 steps/round on `P`, batch 16, `λ_ft:λ_kd = 1:1` |
| KD loss | `CE + RKL(q‖p)` per [10] — reverse KL, full-vocab (common prefix), float32 |
| Public pool `P` | **BIRD train** (decided 2026-07-12; distill subset a few k, stratified; E0.1 probe first — §3.2) |
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
   relational/hidden-state KD. Direction (RKD/KID) picked by the PoC.
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
- **FedEx-LoRA** — Singhal et al., ACL 2025, arXiv:2410.09432 — exact LoRA
  aggregation via a residual term on the frozen base weight, candidate fix
  for the §3.3 LoRA-averaging caveat (Tier 2, try if A4 shows the gap costs
  EX).

Mechanism figure: `fig_architecture_source.png` + `fig1_architecture.md` predate
the 2026-07-08 server-side pivot — **Fig. 1 must be redrawn** (teacher box moves
from client to server; public pool `P` added) before §3 of the paper is written.
