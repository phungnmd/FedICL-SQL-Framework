# Fed-ICKD — System Architecture

**Federated In-Context Knowledge Distillation for Text-to-SQL** *(repo name: FedICL-SQL)*

> **Rewritten 2026-07-08; KD-pool consistency pass 2026-07-20.** This document
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

## 0. Status & scope (2026-07-13; decision-status legend added 2026-07-15)

**Decision-status legend (softening pass 2026-07-15, user):** older text says
"locked" — read that as *build-order pick*, not immutable truth. Three grades:

- **invariant** — hygiene/privacy/comparability rules (§11). Hard. Not
  empirical claims, so no retest can overturn them.
- **closed finding** — replicated or externally corroborated (BIRD-gold ban:
  probe + independent 52.8% annotation-error report; centralized
  selection-null: replicated across 4 model families). Reopen only on new
  contrary evidence, not on re-argument.
- **provisional default** — best current pick on incomplete evidence
  (typically 1 seed); build proceeds on it, a scheduled retest can overturn
  it. Currently: **RKD direction** (p=0.072 vs KID → seed-2 + A1 + §8.3),
  **asym-KD kill** (−0.78, 1 seed, within noise — stays shelved, grade
  noted), **rehearsal-not-needed** (→ §3.4 instrumentation + A3 trigger),
  **SC-vote inference overlay** (full 1034-row test set, McNemar p=0.00042 —
  strong for 1 run, but the run's only source of randomness is the sampling
  seed; seed-2 would confirm stability before this is a citable paper number,
  §5.4).

**Settled:**

- **Centralized KD PoC — COMPLETE (2026-07-11).** `central_ft` / `central_rkd`
  / `central_kid` trained and evaluated. KD signal is real: `rkd − ft` =
  +6.09 EX, McNemar p=3.1e-07 (107 vs 44 discordant rows). **Direction: RKD —
  provisional default** (2026-07-12, user; regraded 2026-07-15 per the legend
  above) — beat KID at every condition incl. under the exec gate. Caveat
  carried, not a gate: the paired gap vs KID (38 vs 23 rows, p=0.072) is NOT
  significant at 1 seed; seed 2 still needed before the gap size is a citable
  paper number, but the build pick does not wait on it.
- **Pool `P` — RESOLVED (2026-07-12/13): BIRD schemas/DBs only.** BIRD's own
  (question, gold-SQL) pairs are permanently banned as CE/RKL targets
  (annotation quality — gate trace in §3.2); server-distill targets come from
  §8.0's implemented Phase-1 construction (§8.3/§8.4 = future online upgrade,
  still unbuilt). **Canonical KD data freeze (locked 2026-07-20): all KD arms
  use the same 3,873-row teacher-generated EX-match pool.** Counts such as
  831 or 1,200 elsewhere in this document are retained only as historical
  probe/budget counts; they are not the default KD pool and must not be
  substituted silently. A previously reported “8,128 rows” was `wc -l` on a
  multiline CSV, not a sample count, and is corrected in §8.0.
- **ICL role settled empirically (§5.2/§5.4):** selection sophistication never
  pays (4 model families, uniform + gated); the verifier-gated retry (single
  k=3-demo retry on exec failure) was the shipping overlay through
  2026-07-15. **Superseded 2026-07-16: self-consistency execution-voting
  (`sc`, N=8 samples at k=0, vote on execution-RESULT equivalence, no ICL
  demos at all) is now the default inference overlay** — beat the gate
  head-to-head on the full 1034-row Spider dev test set, same adapter
  (`central_rkd`), same seed: EX 72.73 vs 69.92 (+2.81), EM 65.67 vs 63.83
  (+1.84), McNemar exact p=0.00042 (47 rows sc-only-right vs 18 gate-only-
  right). Cost: 1.37× latency (3.37 vs 2.46 s/q), 1.34× VRAM (4.49 vs
  3.36 GB) — accepted (2026-07-16, user): the framework's cost claim is
  deployment footprint (model size, no server round-trip), not per-query
  latency. Client retrieval infra is now fully optional, not just
  accuracy-neutral: `sc` needs zero demos, so the ~14% fallback-retrieval
  path the gate used is gone too. Full trace: LAB_LOG 2026-07-16.
- **Naming: "Fed-ICKD" stays**, regardless of the `k_teacher` 3-vs-0 ablation
  outcome (2026-07-12, user). ICL is an open experimental surface, not a
  single load-bearing ablation — apply it wherever it plausibly helps and
  report what's found.
- **No advisor gate on any pending item as of 2026-07-12** — server-side
  pivot, RKD pick, claim-3 reframe (§1), §8.1 kill, BIRD-`P` (§3.2), and
  V2-1/V2-2 (§8.3/§8.4) are all locked by user decision. Nothing in this doc
  currently blocks on advisor sign-off.

**Next (top priority; revised 2026-07-20):** run the newly implemented
**weighted FLoRA-NA** custom sequential simulator at K=2/T=1, then K=8/T=1,
using the paired Tier-1 aggregation × server-step ladder in §10. This code is
not Flower. Factor-wise weighted FedAvg remains the required baseline, not the
proposed aggregator. The paper has no federated number yet.
GPU-idle item (elevated 2026-07-15): seed 2 for
`central_rkd`/`central_kid` — the RKD-vs-KID gap is p=0.072 at 1 seed
(caveat above), cheapest retest in the queue; the pick itself doesn't wait.

**Deferred:** Tier-2 ablations (§10) until the Tier-1 ladder has numbers; the
v2 extension arms (`florana_kd_onpolicy`/`florana_kd_onpolicy_exec`, §10) after the
FLoRA-NA Tier-1 ladder lands.

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
2. Server-side reverse-KL distillation on public data as a **consensus
   regularizer after weighted FLoRA-NA aggregation** — teacher fully isolated
   from private data. Factor-wise FedAvg is the principal FL baseline.
3. An ICL analysis finding + a cheap **execution-verified inference overlay**:
   on a fine-tuned/distilled student, demo *content* stops mattering — the
   full selection thang converges (random ≈ question-sim ≈ DAIL ≈ CodeS,
   uniform AND gated; repair sets nearly disjoint across demo sets) — so
   eval-time demos act as prompt perturbation, not in-context knowledge
   (2026-07-11, 1 seed — see §5.2/§5.4). The shipped overlay pushes that
   finding one step further: **self-consistency execution-voting (`sc`,
   N=8 samples at k=0, temperature as the perturbation medium, vote on
   execution-RESULT equivalence) needs no ICL demos at all** and beats the
   single-retry verifier-gated overlay it replaced — +2.81 EX / +1.84 EM on
   the full Spider dev test set, McNemar p=0.00042 (2026-07-16, 1 sampling
   seed — see §5.4). Confirms the load-bearing component is the execution
   verifier, not the demos: removing ICL from the overlay entirely and
   replacing the perturbation source with temperature sampling still wins.
   Plus an analysis of how public-pool quality affects distillation
   effectiveness.
   *(Reframed 2026-07-11 twice: from "DAIL-style ICL consistent between client
   training and inference" → "selective-ICL usage policy" → the verifier-
   gated-retry framing, after the A5 random-demos attribution control landed
   (random repairs 22/146 vs DAIL 23/146, McNemar p=1.00). Locked 2026-07-12
   (user) — changes the approved outline's RQ2 emphasis, no advisor gate.
   Overlay itself superseded 2026-07-16 by SC-vote; the underlying finding
   — demos are perturbation, not knowledge — is unchanged, just pushed
   further than the original framing anticipated.)*

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
│  filter on P's DBs → targets y_pub (§8.0)                │
│  → cache teacher logits on y_pub (target fixed → RKD     │
│    cacheable; future §8.3 on-policy needs teacher online)│
│                                                          │
│  [Phase 3 — every round]                                 │
│  weighted FLoRA-NA(adapters, nᵢ/n) → global adapter     │
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

> **Rule (scope clarified 2026-07-13; REGRADED to provisional 2026-07-18):**
> BIRD's own (question, gold-SQL) pairs are off-limits as training targets —
> but the evidence grade is **split by loss term** (§0 legend audit,
> 2026-07-18):
>
> - **As plain-CE targets: confirmed harmful** (gate table below — E0.1 at 1k
>   from base lands under the untrained floor; 1 seed, 1k scale).
> - **As CE+RKL targets: never tested.** The 2026-07-13 "permanently
>   off-limits" wording extrapolated the CE result to RKL. Counter-signal
>   discovered since: CE-only continuation on BIRD-domain *teacher* text also
>   regresses (−2.81, §3.4) and **RKL neutralizes that drift** — RKL may
>   likewise neutralize gold-text drift. Unknown which force wins; teacher
>   logprobs on BIRD gold may also be noisier (annotation errors + style).
>   E0.1b's retirement is **reversed in controlled form** — decisive arm:
>   `central_ft_then_kd_bird_gold` (same warm-start + rows as
>   `central_ft_then_kd_bird_exmatch`; on exmatch rows teacher-text and gold
>   are execution-equivalent, so the ONLY variable is whose *text* the
>   student distills on). Until it runs, teacher-generated targets (§8.0)
>   stay the default and the ban stays operative-but-provisional.
>
> Server-distill targets come from **§8.0's implemented Phase-1 construction**
> (teacher zero-shot + exec-filter, now + EX-match-vs-gold filter) — §8.3/§8.4
> are the *future* online upgrade (student on-policy sampling), still unbuilt,
> not what §6e/§6f/§6g actually run on. Runbook: `notebooks/kd/README.md`
> §6/§6c/§6e/§6f/§6g (§6b marked retired in place).
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
domain/dialect. Independent (weaker-than-we-first-wrote) corroboration: the
CIDR 2026 audit ("Text-to-SQL Benchmarks are Broken") reports **52.8% of the
~500-example Mini-Dev subset has some annotation issue** — a broad category
that includes ambiguous questions and evidence problems, NOT "52.8% of gold
SQL is wrong"; most flagged gold still executes, and the train split (our
pool `P`) was never audited. Read it as "BIRD gold is an unreliable oracle,"
not "majority-poisoned" — the load-bearing evidence for our own decisions
stays our E0.1/lever-D probes above, with 52.8% as directional support
(scope note added 2026-07-19). Side
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

### 3.3 Federated aggregation — weighted FLoRA-NA (proposed main method)

> **Decision 2026-07-19; implemented 2026-07-20.** Weighted FLoRA-NA is now
> implemented in `fedicl_sql/federated/aggregate.py` and exposed as
> `florana`/`florana_pub`/`florana_kd`. Weighted factor-wise FedAvg remains
> unchanged as the paired `fedavg`/`fedavg_pub`/`fedkd` baseline. Existing
> `fedkd` artifacts are still factor-average artifacts, never FLoRA-NA.

For client `i`, let `p_i = n_i / Σ_j n_j` and its trained LoRA update be
`ΔW_i = B_i A_i`. The model-space aggregation target is

```
ΔW*_t = Σᵢ pᵢ BᵢAᵢ
```

Factor-wise FedAvg instead produces `(ΣᵢpᵢBᵢ)(ΣᵢpᵢAᵢ)`, which is generally
not `ΔW*_t`; common initialization does not remove the cross-client terms.
Therefore **weighted factor-wise FedAvg is the principal baseline, not the
default proposed aggregator**.

Weighted FLoRA-NA keeps one rank-`r` adapter by solving on the server for
client-combination coefficients `u,v`:

```
u*,v* = argmin || (Σᵢ uᵢBᵢ)(Σᵢ vᵢAᵢ) - Σᵢ pᵢBᵢAᵢ ||²_F
B_hat = Σᵢ u*ᵢBᵢ
A_hat = Σᵢ v*ᵢAᵢ
θ_t_preKD = (A_hat, B_hat)
```

This is the required **sample-weighted extension** of FLoRA-NA's equal-client
formulation; the target must retain McMahan weights because client sizes differ.
It is nearly accurate, not exact: the global update remains constrained to
rank `r`. The output is nevertheless a standard LoRA adapter, so the existing
server CE/RKL trainer can continue optimizing both `A_hat` and `B_hat`, and
the post-KD result remains one broadcastable adapter against the unchanged
frozen base.

- **Communication:** uploads and downloads remain one rank-`r` LoRA adapter
  per client/round. Report measured bytes for the actual model/rank/dtype.
- **Primary baseline:** weighted factor-wise FedAvg (`fedavg`). It matches the
  current implementation and standard FedIT-style practice while exposing the
  aggregation error FLoRA-NA is intended to reduce.
- **Required diagnostic:** log
  `e_agg = ||ΔW*_t-B_hat A_hat||_F/(||ΔW*_t||_F+ε)` for FLoRA-NA and the same
  quantity with factor averages for FedAvg, per layer and overall.
- **Exact reference, not the main method:** FedEx-LoRA (ACL 2025) can be run at
  T=1 or Tier 2. It folds the exact residual into the frozen base and therefore
  requires base/residual state plus the adapter; its downlink scales up to
  rank `K·r`, conflicting with the paper's simple immutable-base/one-adapter
  round contract.
- **Communication-first alternative, Tier 2:** Fed-SB aggregates only a small
  `R` between fixed bases. It is exact but constrains both private CE and public
  KD to a fixed subspace, adding a capacity confound to the KD question.
- FedProx remains Plan-B only if drift under strong non-IID is unstable after
  aggregation error is measured separately; it does not repair LoRA factor
  averaging.

### 3.4 Server distillation (Phase 3 — the consensus regularizer)

After weighted FLoRA-NA (or the matched FedAvg baseline), the aggregated global
student is distilled on `P` for a few hundred steps (default 300, batch 16 —
the server is not VRAM-constrained the way clients are):

```
L = λ_ft · CE(student, y_pub)  +  λ_kd · RKL(q ‖ p)        # [10]'s recipe, defaults 1:1
```

- `p` = teacher logprobs over the KD target, `q` = student logprobs over the
  same target, **same DAIL ICL context** for both.
- **Reverse KL, never forward KL**: mode-seeking fits SQL's precise,
  low-diversity token distribution ([10]); forward KL is mean-seeking and
  smears mass over invalid continuations.
- **`y_pub` = the frozen 3,873-row teacher EX-match pool** (§8.0):
  teacher-generated SQL on `P`'s schemas, execution-filtered and then retained
  only when its execution result matches gold. Gold is used only by the
  selector; the training target remains the teacher's SQL text. This pool is
  mandatory for every default KD arm; exec-only and BIRD-gold pools are
  explicit ablations, never implicit substitutes.
- **Direction: RKD — provisional default (2026-07-12; regraded 2026-07-15)**
  (gold-target reverse KL; PoC §8). KID trailed the PoC (−1.45 EX) but the
  paired gap is **not significant at 1 seed (p=0.072)** — the pick stands on
  cost (RKD's target is fixed → logits cacheable offline; KID needs the
  teacher online), not on statistics. Scheduled retests: seed-2 (§0),
  A1 at federated scale, §8.3 on-policy (the mask-token hypothesis). §8.3 +
  §8.4 (execution-anchored) are Tier-2 **future online** target upgrades on
  top of RKD, once the round loop exists — §8.0 is what `y_pub` runs on today.
- Implementation notes carried over from the PoC code (`train_online_kd`):
  Qwen2.5 7B vs 1.5B logit dims differ (V=152064 vs 151936, embedding padding)
  → slice both to the common vocab prefix; compute RKL in float32 (fp16 sum
  over a 150k vocab loses precision).
- **Role:** after aggregation of non-IID clients the global model's behaviour is a
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

- **Scaled up to the full exec-bootstrap pool (2026-07-17,
  `central_ft_then_kd_bird_exmatch`, same warm-start, 3873 steps vs the
  probe's 831):** EX=65.47/EM=32.50/exec_err=111 (k=0) — CE+RKL edge over
  pre-continuation baseline grows to **+3.28 EX**, exec_err keeps dropping
  (211→157→111 across baseline→probe→full-scale). Paired-row churn check
  (baseline vs full-scale, n=1034): 123 rows flip to correct, 89 flip away —
  net +34 = the +3.3pp, but this is a boundary shift, not a strict-superset
  gain, and EM stays collapsed (57.16→32.50) at the same scale as the probe —
  not a small-n artifact. **Caveat that matters for the paper: under +ICL
  (k=3, gate_exec — the actual deployed inference condition per §5.4), the
  EX edge nearly vanishes (+3.28pp → +0.29pp, 66.83 vs baseline's 66.54,
  inside the ~0.5pp noise floor)** — ICL alone recovers most of what this
  continuation step buys (baseline +ICL: +4.35 EX; exmatch +ICL: only
  +1.36 EX), i.e. KD-continuation and inference-time ICL are substantially
  redundant on the failure mode both target. The one gain that survives ICL
  is exec-reliability, not EX: exec_err 75 vs baseline's 125 even with demos
  in context. **Report this as an exec-reliability effect, not an EX
  headline** — the deployed-condition EX delta is noise-level. LAB_LOG
  2026-07-17 has the full churn table and prediction spot-checks.

- **Round-loop drift instrumentation (pre-registered 2026-07-15):** the proxy
  above is ONE continuation step; the round loop repeats the dynamic T=15
  times, so a per-round +0.09 "flat within noise" could still compound into
  real drift. Counterweight (user, 2026-07-15): the loop itself alternates —
  each round's Phase 2 re-trains every client on the same private Spider data
  (**implicit rehearsal by construction**, the very step the centralized proxy
  did NOT include). Whether the alternation converges or oscillates is an
  empirical question → instrument, don't assume: log a fixed Spider-dev-slice
  EX for `M_G` **twice per round** — post-FedAvg (pre-distill) and
  post-distill — so the FT-vs-KD tug-of-war is visible per phase, not just
  per round. **Pre-registered trigger:** if post-distill EX decays
  monotonically across rounds despite RKL, activate A3's *mix* arm early
  (Spider held-out mixed into `P` as explicit rehearsal) instead of waiting
  for the ablation grid. Symmetric risk the same instrumentation catches:
  E×T = 30 epochs over the same small `Qᵢ` may overfit clients — there the
  server KD step is the counter-regularizer, visible as post-distill >
  post-FedAvg.

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
>
> **Scope grade (2026-07-15, §0 legend):** *closed finding* for the
> centralized regime (null replicated across 4 families — strongest
> replication in the repo); **untested** for federated small, domain-skewed
> `Qᵢ` fallback pools — that gap is logged for free by §7's per-client gate
> instrumentation, no selection machinery gets rebuilt on speculation.

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
Related Work as the closest prior-art anchor for the shipped `sc` overlay
(§5.4): DPC selects among generated candidates by execution consistency,
same mechanism `self_consistency.vote()` implements (majority on
execution-RESULT equivalence, not SQL text) — differentiate on ours being
paired with temperature sampling at k=0 (no demos in the loop at all) inside
a federated Text-to-SQL client, not a retrieval alternative.

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

- **Default (2026-07-16, full test set, 1 sampling seed): train k=0;
  inference = self-consistency execution-voting (`sc`, N=8)** — sample N=8
  candidates at k=0 (temperature 0.8, top_p 0.95), execute each on the
  client's local DB, majority-vote on execution-RESULT equivalence (ties →
  highest mean log-prob), `fedicl_sql/eval/self_consistency.py`. Beat the
  prior verifier-gated-retry default head-to-head on the full 1034-row
  Spider dev test set, same adapter (`central_rkd`), same seed: **EX 72.73
  vs 69.92 (+2.81), EM 65.67 vs 63.83 (+1.84), McNemar exact p=0.00042** (47
  sc-only-right rows vs 18 gate-only-right rows). Training is unaffected —
  still plain gold-CE at k=0 (§5.4's `L` above); only the inference-time
  overlay changed. Cost: 1.37× latency (3.37 vs 2.46 s/q), 1.34× VRAM (4.49
  vs 3.36 GB) — accepted (2026-07-16, user): the cost claim is deployment
  footprint, not per-query latency. **Zero ICL demos, zero retrieval infra**
  at the client now — a strictly simpler deployment story than the gate it
  replaced (which still needed a demo pool + retrieval for its ~14% fallback
  path). Full trace: LAB_LOG 2026-07-16. **N=8/temp=0.8 matches CSC-SQL's
  own default** (§14 anchors) — grounded starting point, not yet tuned;
  N sweep (8/16/32) deferred (2026-07-16, user — cite now, sweep later).
- **Superseded (shipped through 2026-07-15) — verifier-gated retry**: k=0
  draft → exec check → k=3 fallback on error only; 70.79 EX vs 68.28 ungated
  k=0 on `central_rkd`. Kept runnable (`eval_arms.py --overlay none
  --icl-gate exec`) as the comparison baseline for any future overlay probe —
  `sc` had to beat this number, not raw greedy, to earn the default slot.
- **A2 (§10), retargeted 2026-07-16:** was `train-k0+gate` vs `train-k2
  consistent`; now compares **`train-k0 + sc`** (current default) vs
  `train-k2 consistent` (same k at training and inference, the outline-era
  default) — the training-regime question is orthogonal to which inference
  overlay sits on top, so A2 still stands, just pointed at the current
  overlay. `train-k2 consistent`'s rationale: training with demos makes
  eval-time ICL in-distribution, removing the train/test-mismatch failure
  measured earlier (k0-trained student + k3 eval → schema bleed, −30 net
  flips, 54/109 hurts = `no such column`). ⚠️ Hypothesis, not established —
  centralized evals (LAB_LOG 2026-07-09/10, 1 seed) observed the opposite:
  the k3-trained arm regressed *most* under uniform eval-time ICL; train-time
  demo exposure did not immunize.
- Honest caveats carried with `sc`: (a) repair still traces to execution
  verification, not demo/ICL content — `sc` removes ICL from the loop
  entirely and still wins, which is a *stronger* version of the A5 finding
  (§5.2: random ≈ DAIL demos), not a break from it — temperature sampling is
  now the perturbation medium; (b) `sc` needs SQL execution against the
  client's own DB at inference (same requirement the gate had) — fine in our
  federated setting (the DB is local), but a no-exec-at-inference deployment
  would need a different mechanism entirely (Tier 3, static signal — voting
  on execution results has no fallback if execution itself is unavailable);
  (c) 1 sampling seed — the N=8 draw is itself random, so a second `--seed`
  run is the cheap remaining check before this is a citable paper number
  (the *pick* doesn't wait on it, same posture as the RKD direction, §0).
- No teacher, no KD loss, no public data at the client. Light and
  VRAM-friendly — everything heavy lives at the server.

---

## 6. Federated round loop

> **Status: complete implementation 2026-07-20; real headline runs pending.**
> `fedicl-sql/experiments/federated/run.py` runs all six paired arms — client
> local FT (`train_client`) → weighted factor-wise FedAvg or weighted
> FLoRA-NA → none / public CE / public CE+RKD-RKL. Per-stage checkpoint/resume
> via `adapter_done()`
> (`fedicl_sql/runtime/checkpoint.py`) — a crash/kill resumes at the first
> incomplete client/fedavg/server stage, not the whole run. Smoke-tested
> end-to-end on real Spider+BIRD data (2 clients, 1–2 rounds, tiny step caps);
> real T=15/K=8 runs are not yet executed (compute-host queue item). Both
> aggregators log per-layer and overall model-space `e_agg`; the no-op guard
> uses true round deltas, including an exact saved pre-training PEFT reference
> at round 1. Pool/cache/adapter fingerprints
> fail loudly on provenance drift. The old three arms remain baselines and
> must not be renamed retroactively.
>
> **Existing baseline pilot = R2.0-old (designed 2026-07-19, LAB_LOG (4)/(5));
> retained as a smoke/diagnostic, no longer the complete Tier-1 pilot.** Its
> round-1 client training + factor-wise FedAvg are identical across the old
> three arms (same init/split/seed) → trained once, then
> **shared by pointing `round`'s `--client-out` at one directory** for all
> three arms' round-1 invocations (2026-07-19 (5) — `run.py` split into
> `client`/`fedavg`/`server`/`round`/`run` subcommands; `check_fingerprint()`
> fails loudly if the shared stage's config actually drifted between arms,
> replacing the earlier copy-adapter-directories design). The three arms
> therefore share one post-FedAvg adapter and differ ONLY in the server step
> (none / CE-on-P / RKL-on-P), making T=1 a fully paired, row-level-McNemar-
> able ablation of the server step at full scale (the §3.4 drift question,
> previously only proxied by the centralized continuation probe). After the
> T=1 read, T grows incrementally on the same `--out` dirs (`run --rounds 2`,
> `--rounds 3`, … — resume semantics in the run.py docstring); arms diverge
> from round 2 onward by design (clients warm-start from arm-specific `M_G`).
> Each arm's M_G is resolved via `fedicl_sql.runtime.manifest.resolve_m_g`
> (never by globbing `round_*/m_g`) — see §6 "Results/artifacts" below.
>
> The teacher logit cache below (Phase 1) is also implemented
> (`fedicl_sql/training/logit_cache.py`, `scripts/build_teacher_logit_cache.py`)
> — **one caveat vs the original design note**: it stores **full-vocab fp16
> logits** per cached example (size depends strongly on target length, not
> top-K), because
> `rkl_div_loss` was already decided full-vocab-online (`losses.py`'s "no
> top-K logprob caching needed" comment predates this cache and describes a
> *different, retired* sparse-KL design — not a conflict with this one, just a
> naming collision worth flagging). **Canonical policy (2026-07-20): cache
> identity and sampling population are the complete frozen 3,873-row pool.**
> Every default KD server invocation consumes one complete epoch over that
> pool. `--pool-size 0 --distill-steps 0` encodes this full-data default;
> positive caps are smoke/data-budget ablations only. Full-vocab caching is
> optional; online teacher scoring is valid when the full cache is not
> economical. RKD-only
> (KID's `ŷ` is re-sampled every step) and symmetric-context-only
> (`kd_teacher_k=0` — §8.1's asymmetric variant is shelved anyway). A
> cache/config mismatch (pool content, train_k/demo_k_fixed/seed/schema_style/
> retrieval drift between the offline build and the round loop) fails before
> training; an individual missing rendered key also fails loudly (`KeyError`).
> Neither case silently falls back to a live teacher forward.

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

  3. SERVER (Phase 3 — proposed full method):
       ΔW*_t ← Σᵢ (nᵢ/n)·BᵢAᵢ                    # ideal weighted target
       u*,v* ← weighted_FLoRA_NA({Aᵢ,Bᵢ,nᵢ})     # minimize model-space error
       θ̃_t ← (Σᵢv*ᵢAᵢ, Σᵢu*ᵢBᵢ)                 # one rank-r adapter
       student.load_lora(θ̃_t)
       for step in range(300):                   # distill on P, batch 16
           x, y_pub = next_batch(P);  demos = DAIL(x, pool=P, k=k_teacher)
           p = teacher(P_ICL(x, demos), y_pub)   # cached offline (RKD locked;
           q = student(P_ICL(x, demos), y_pub)   #  §8.3 samples ŷ instead)
           L = λ_ft·CE(y_pub) + λ_kd·RKL(q, p)
           update_lora(student, L)
       θ_t ← student adapter;  M_G ← base + θ_t

Inference (Phase 4, per client, no server / no teacher — sc-vote, §5.4):
       candidates = M_G.sample(prompt(q, Sᵢ), n=8, temp=0.8, top_p=0.95)  # k=0, no demos
       executed = [(sql, lp, execute(sql, local_db)) for sql, lp in candidates]
       sql = majority_vote(executed, tiebreak=logprob)  # vote on execution RESULT, §5.4
       return sql
```

### 6.1 Round loop CLI + results/artifacts (2026-07-19)

`run.py` splits into six subcommands instead of one monolithic invocation —
`client` / legacy `fedavg` / generic `aggregate` / `server` run one stage standalone (debugging, or
building a custom orchestration like R2.0's arm-sharing); `round` runs one
full round (client+fedavg+server) of a given arm; `run` is the T-round loop
for one arm (headline runs), internally just calling `round`'s logic for
t=1..T. Full flag reference lives in the script's own docstring, not
duplicated here — this doc records the *design*, the code is the source of
truth for exact flags.

Three storage tiers, each with a distinct job:

1. **`<out>/round_<t>/<stage>_meta.json`** — one training call's own metrics
   (loss, step count, gpu_vram), written beside its adapter by every stage.
   Low-level, per-invocation provenance; not meant for cross-run comparison.
2. **`<out>/manifest.json`** (`fedicl_sql/runtime/manifest.py`) — the
   arm-run-level index: which rounds are complete, and each one's
   `client_out`/`aggregation_method`/`aggregation_adapter`/`m_g` paths
   (plus legacy `fedavg_adapter` compatibility). `resolve_m_g(out_dir)` is the
   one call eval/analysis code should use to find an arm's current M_G —
   works identically whether round 1 lived inside `--out` (plain `run`) or
   in a directory shared across arms via `--client-out` (R2.0). Avoids
   re-deriving adapter paths from CLI flags in every downstream script.
3. **`experiments/federated/results/<run_id>/metrics.json`** — one row PER
   COMPLETED ROUND (not per process invocation), via the standard
   `save_results` convention (§ conventions doc / repo `CLAUDE.md`) so
   `analysis/compare.py` picks it up with no new tooling. `time_average`/
   `gpu_vram` cover only the stages actually (re)trained that round — a
   resumed round where every stage was already done reports ~0, not a
   diluted average over skipped rounds (fixed a real bug in the pre-split
   version, which divided total elapsed time by the target `--rounds` even
   when most of those rounds were skip-resumed).

**R2.0's arm-sharing mechanism, concretely:** round 1's client+FedAvg stage
needs identical config across `fedavg`/`fedavg_pub`/`fedkd` (same split,
seed, init=None) — so instead of training it three times (or the earlier
copy-directories design), point all three arms' `round --round 1 --client-out
<shared-dir>` at the same directory. `adapter_done()` skips every already-
trained client/fedavg stage on the 2nd and 3rd calls; `check_fingerprint()`
(`fedicl_sql/runtime/checkpoint.py`) writes the config on first use and
raises loudly on any later call with a different config touching the same
directory — the same fail-loud philosophy as the teacher-logit-cache
key-mismatch `KeyError`. Each arm still gets its own `--out` (own
`manifest.json`, own `round_<t>/m_g` for the server step) — only the
client+fedavg artifacts are physically shared, never copied.

---

## 7. Inference (deployment)

Each client runs `M_G` locally with **self-consistency execution-voting**
(`sc`, §5.4, default 2026-07-16): sample N=8 candidates at k=0 (temperature
0.8, top_p 0.95), execute every candidate on the local DB, majority-vote on
execution-RESULT equivalence (ties → highest mean log-prob). No server
round-trip, no teacher at inference, **no ICL demos and no retrieval
infrastructure at all** — a simplification over the verifier-gated retry it
replaced (that overlay still needed a demo pool + retrieval for its ~14–20%
fallback path; `sc` needs neither, ever). Global arms are evaluated **once
per client pool** and reported mean±std over K.

Cost trade vs the superseded gate: 1.37× latency, 1.34× VRAM (N=8 candidates
generated + executed per query instead of 1–2) — accepted per the framework's
cost framing (deployment footprint, not per-query latency, §5.4).

Instrumentation carried from the gate era (2026-07-15): log fire/repair-style
diagnostics **per client** — for `sc` this is `sc_n_executable`/`sc_n_groups`/
`sc_winner_group_size`/`sc_tie_broken` per row (`PREDICTION_FIELDS`,
`fedicl_sql/runtime/results.py`), the equivalent of the old gate-fire-rate.
§5.2's selection findings are all centralized (demo pool = full Spider
train); moot for `sc` itself (no demos), but still relevant to the
`train-k2 consistent` A2 alternative if that arm ever ships instead.

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

**Verdict (PoC 2026-07-11; provisional default 2026-07-12, regraded
2026-07-15): RKD ships as the build default.** Evidence grade is split:
`rkd − ft` = +6.09 EX is **strong** (McNemar p=3.1e-07); `kid − rkd` =
**−1.45 EX is weak** (p=0.072, 1 seed) — opposite [10]'s own headline, and
scheduled for retest (seed-2, A1, §8.3). Leading suspect: the mask token (`pad_token_id`) substituted
mid-sequence is an artifact outside the pretrain distribution — §8.3's full
on-policy variant tests exactly that. Dropped and deleted 2026-07-07:
Struct-SQL [11] QP-CoT, SeqKD, the whole offline teacher-target pipeline —
[11] stays a related-work reference only.

### 8.0 IMPLEMENTED — Phase-1 target construction (`y_pub`, offline, teacher zero-shot)

> **Status: built and running (2026-07-12/14) — distinct from §8.3/§8.4 below.**
> §8.3/§8.4 describe the **student** sampling `ŷ` **online, every round**
> (unbuilt — no federation loop exists yet). This section is the **teacher**
> generating `y_pub` **offline, once** (Phase 1, §2/§3.4) — the mechanism
> every §6e/§6f/§6g result (`notebooks/kd/README.md`) already runs on. §3.2's
> line "server-distill targets come from §8.3+§8.4 only" was inaccurate on
> this point — fixed to point here instead; §8.3/§8.4 remain the *future*
> online upgrade once the round loop exists.

Two filter stages, both implemented, both gated (never assumed better than
the last without measuring):

1. **Exec-only filter** (`scripts/build_exec_bootstrap_probe.py`) — teacher
   zero-shot generates one SQL candidate per question on `P`'s schema (no
   ICL, no gold), kept only if it executes without error (ExeSQL recipe,
   §3.2). **Gate-verified PASS** at the floor (50.00 EX, 1k-scale probe,
   §3.2's gate trace). Data: `processed_data/BIRD/bootstrap_full/train.csv`
   (9630→committed, exec-pass yield ~85%).
2. **EX-match filter** (`scripts/score_bootstrap_ex_match.py`, 2026-07-14) —
   re-scores stage 1's checkpoint against BIRD's own gold via
   `score_ex_detail` (no new generation): keeps a row only if the execution
   **result** matches gold's, not just "ran without error." **Caveat, not an
   assumed upgrade:** BIRD gold is an unreliable oracle (52.8% of Mini-Dev
   flagged for annotation issues — broad category, see the scope note under
   the gate trace above), so gold-as-oracle here inherits noise as a
   selection bias in the *other*
   direction (wrongly rejects correct-but-gold-disagreeing teacher SQL,
   wrongly accepts SQL that mimics gold's own errors) — must be gated
   against stage 1's own numbers before it replaces anything (`kd/README.md`
   §6f vs §6g). That comparison is historical; the resulting method was
   subsequently selected as the default data policy. The training target
   stays teacher's own SQL text either way
   (never gold's text) — this only changes which rows get selected, so it
   does not reintroduce E0.1's failure mode. Data:
   `processed_data/BIRD/bootstrap_full_exmatch/train.csv`, which contains
   exactly **3,873 logical CSV records** across 69 DBs. It has 8,128 physical
   text lines because quoted SQL/evidence fields contain embedded newlines;
   `wc -l` therefore does not measure examples. Every real run must validate
   the 3,873 parsed records and record the file SHA-256 in its manifest.

Both stages checkpoint/resume + parallelize the SQLite exec pass
(`ThreadPoolExecutor` — a sequential loop hit the same pathological-query
timeout problem twice, fixed both times the same way).

### 8.1 KILLED — asymmetric-context KD (Tier 3, added 2026-07-08, killed 2026-07-11)

> **Status: shelved by its own pre-registered criterion.** `central_rkd_asym`
> k=0 = 67.50 vs symmetric `central_rkd` k=0 = 68.28 → `asym − sym` =
> **−0.78 EX** < the +1 EX kill floor (measured 2026-07-09, 1 seed; doc
> flipped 2026-07-11). Closed 2026-07-12 (user); **evidence grade regraded
> 2026-07-15 (§0 legend): 1 seed, gap within noise** — the kill is honored
> because the criterion was pre-registered, but this is a provisional
> negative, not a closed finding. Revive = GPU-idle Tier-3 only (expected
> value low: context-distillation literature reports weak gains at small
> student scale). Section kept for the record.

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
> with full on-policy (`florana_kd_onpolicy_exec`, §10) is the strongest combined
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
| k_student (train) | k=0, plain gold-CE (§5.4) — unaffected by the inference-overlay change below |
| Inference overlay | **self-consistency execution-voting (`sc`, N=8, temp 0.8, top_p 0.95)** — provisional default 2026-07-16 (§0 legend; full test set, p=0.00042; seed-2 retest pending); superseded the exec-gated k=3 fallback (§5.4/§7) |
| Clients K | 8 |
| Partition | non-IID by database (Dirichlet over domain groups, α=0.5; ablate 0.1/IID) — **implemented 2026-07-15**: 146 train DBs → 20 schema-embedding k-means clusters (`scripts/build_db_groups.py`, `processed_data/SPIDER/db_groups.json`), one shared Dirichlet(α) vector drawn per cluster (`make_federated_split(db_groups=...)`); committed splits at `processed_data/SPIDER/federated_noniid/alpha_{0.1,0.5}/k8/` + `federated_iid/k8/`, seed=0. Fixed a bug where the old flat per-DB Dirichlet draw made α a near no-op and produced 14–40-example starved clients at K=8; a `min_client_examples=150` resample guard now backstops the floor regardless of α |
| Rounds / local epochs | T = 15, E = 2 — headline target only. Execution plan: use the old R2.0 T=1 run as a baseline smoke/diagnostic, then run the revised paired FedAvg/FLoRA-NA ladder from identical local adapters (LAB_LOG 2026-07-19 (7)); grow T incrementally and commit to T=15 only if the per-round trend justifies it |
| Server distill | **One full epoch over all 3,873 rows every KD round** (`pool_size=0`, `distill_steps=0`); batch 1 with gradient accumulation 16 (effective batch 16); `λ_ft:λ_kd = 1:1`. Positive caps are smoke/ablation only |
| KD loss | `CE + RKL(q‖p)` per [10] — reverse KL, full-vocab (common prefix), float32 |
| KD direction | **RKD — provisional default 2026-07-12** (§0 legend; retests: seed-2/A1/§8.3); §8.3/§8.4 = future Tier-2 target upgrades |
| Public pool `P` | **Fixed 3,873-row BIRD teacher-generated EX-match snapshot** — never BIRD gold SQL text. All default KD arms use this identical pool and record its hash; smaller counts are explicit smoke/legacy ablations only |
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

### Tier 1 — main results (3 seeds; revised 2026-07-19)

| Arm | Suggest.MD | What it is | Role |
|---|---|---|---|
| `central` | M1 | centralized FT student on pooled data, no FL | upper bound |
| `fedavg` | M2 | weighted factor-wise FedAvg, **no** server step | principal FL/aggregation baseline |
| `florana` | — | weighted FLoRA-NA, **no** server step | isolates aggregation value: `florana − fedavg` |
| `florana_pub` | — | weighted FLoRA-NA + CE-only on `P`, no teacher | matched public-exposure/drift control |
| `florana_kd` | M3 | **full Fed-ICKD**: weighted FLoRA-NA + server CE+RKL | proposed method; teacher value = `florana_kd − florana_pub` |
| `teacher` | M4 | teacher 7B + DAIL, zero fine-tune | reference (inference-only) |

Required diagnostic arm (one seed first, promote if informative): existing
`fedkd` = factor-wise FedAvg + server CE+RKL. The interaction
`(florana_kd−florana_pub) − (fedkd−fedavg_pub)` compares the matched
teacher/RKL effect after each aggregator, testing whether RKD remains useful
after reducing aggregation error instead of merely repairing factor averaging.
The existing `fedavg_pub` is the factor-average CE-only control.

Headline story: `florana > fedavg` establishes aggregation value;
`florana_kd > florana_pub` establishes teacher/RKL value beyond identical
public exposure; and `florana_kd` approaches `central`/`teacher`. Do not assume
the ordering before results. At T=1, share the client outputs across all arms;
each aggregator/server branch must start from the identical local adapters.

### Federated v2 extension arms (Tier 2, proposed, locked — no advisor gate, §8.3/§8.4)

Same server-distill step, target/filtering swapped one ingredient at a time.
Run **after** the Tier-1 ladder above has real numbers — these are additive,
not a replacement for the headline pair.

| Arm | Adds vs `florana_kd` | Mechanism |
|---|---|---|
| `florana_kd_onpolicy` | KD target: gold `y` → student-sampled `ŷ` | §8.3 — tests the mask-token-artifact hypothesis behind `kid − rkd` |
| `florana_kd_onpolicy_exec` | + execution filter/weight on the sampled `ŷ` | §8.4 — execution-anchored distillation; the stronger novelty differentiator vs FedCoLLM [8] |

Build order (`fed_ickd_v2_proposal.md` §Thứ tự build): weighted
FLoRA-NA + `e_agg` **implemented** → T=1 paired Tier-1 ladder → multi-round/3-seed headline
→ these two on-policy rows as arms bolted onto the standing ladder → Tier-3
cheap items in parallel when GPU is idle.

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
| A2 | `train-k0 + sc` (current default, retargeted 2026-07-16 from `+exec-gate`) vs `train-k2 consistent` (uniform k=0/1/2 as secondary rows) | which training regime pairs best with the shipped inference overlay |
| A3 | pool `P`: BIRD train (default) / Spider held-out / mix | pool-quality finding (⚠ do not cut) — Spider held-out = the in-distribution contrast to BIRD's cross-distribution default. *mix* doubles as explicit rehearsal — early-trigger target of §3.4's round-drift instrumentation; note the round loop already rehearses implicitly (client re-FT on same `Qᵢ` every round), so *mix* is the escalation, not the first line |
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
existing adapter; superseded in scope by SC-vote below, which subsumes it —
vote size 1 ≈ this) · **static-demos gate** (fallback uses one fixed cached
demo set — zero retrieval infra at the client; 1 confirmation run, predicted
≈ random per §5.2) · **`fedkd_ens` ensemble-consensus distill** (added
2026-07-15, FedDF-style: server-distill target = ensemble of the K client
adapters on `P` instead of the 7B teacher — separates "teacher quality" from
"mere consensus signal", the reviewer question `fedavg_pub` doesn't cover;
proxy data = `P`, never Spider dev; K=8 × 1.5B forwards, feasible on the
A5000) · ~~asymmetric-context KD~~ (**killed 2026-07-11**, §8.1 —
criterion met at −0.78 EX) · ~~Skills Similarity (SS) retrieval~~ (**closed
2026-07-11**, §5.2 — A5 thang converged 4/4 incl. random; selection
sophistication is dead post-FT/KD, SS included; code in-tree, no run).

**Inference-overlay probe verdict (2026-07-16, LAB_LOG same date) — SC-vote
adopted.** Probed against the then-shipped verifier-gated retry on the full
1034-row Spider dev test set, same adapter (`central_rkd`):

- **SC-vote — ADOPTED, now the §5.4/§7 default** (moved out of Tier 3):
  sample N=8 candidates at k=0, execute each, majority-vote on execution-
  result equivalence (ties → highest mean log-prob) —
  `fedicl_sql/eval/self_consistency.py`. EX 72.73 vs gate's 69.92 (+2.81),
  McNemar p=0.00042. Generalized the multi-retry-gate idea above (vote size
  1 ≈ that) — this item is now superseded/subsumed, not a separate build
  target.
- Self-debug/error-feedback retry considered, dropped by the user
  (2026-07-16) — not built.
- Probe harness: `eval_arms.py --overlay sc` (`--overlay none --icl-gate
  exec` still runs the superseded baseline for comparison).
- **`sc` N sweep (8/16/32) — deferred, not run** (2026-07-16, user: cite the
  method's grounding now, try higher N later). Motivation: CSC-SQL's own
  N-sweep on a 3B model (close to our 1.5B) shows EX still climbing well
  past N=8 (58.15→62.17→63.49→64.91→65.28 for N=4/8/16/32/64, plateau only
  after ~32, §14 anchors) — our current N=8 is a grounded starting default,
  not yet a tuned one. `--sc-n 16`/`32` already work end-to-end
  (`eval_arms.py --overlay sc`), pure cost tradeoff to run, no code change
  needed.

Negative results are framed as analysis, never hidden (e.g. if A2 says k=0 wins →
report it, move default to k=0, keep DAIL for the teacher).

---

## 11. Key invariants (never violate)

> **Why these stay hard under the 2026-07-15 softening pass:** the pass
> regrades *empirical findings* (1-seed picks → provisional defaults). The
> items below are not findings — they are methodology commitments (privacy,
> contamination, comparability) whose violation invalidates the paper
> regardless of what any experiment says; no retest can make test-set leakage
> acceptable. The one empirical claim that had crept in here (RKD direction,
> #3) is demoted accordingly.

1. **Private data never leaves the client** — raw rows, `Sᵢ`, `Qᵢ`, demos,
   embeddings: no outgoing arrow. Only LoRA adapters cross, both directions.
2. **Teacher never touches client data** — structural: the teacher lives at the
   server and the server only ever receives adapters. Teacher's world = `P`.
3. **KD loss = reverse KL per [10]** (`CE + RKL`), never forward KL, never
   relational/hidden-state KD. *(Design commitment; A6 probes the formula
   variant.)* The **RKD direction is NOT part of this invariant** — demoted
   to provisional default 2026-07-15 (§0 legend, §8): a 1-seed p=0.072 pick
   doesn't belong in a never-violate list.
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
| `y_pub` | server-distill target on `P` — teacher-generated, execution-filtered (+ optional EX-match) SQL (§8.0) |
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
- Aggregation theory anchors: McMahan (FedAvg) as the weighted factor-average
  baseline; Nguyen et al., **FLoRA-NA** (arXiv:2509.26399, preprint) as the
  proposed nearly-accurate, fixed-rank aggregator. Our implementation must
  target `Σᵢ(nᵢ/n)BᵢAᵢ`, not the equal-client mean.
- **FedEx-LoRA** — Singhal et al., ACL 2025, arXiv:2410.09432 — exact LoRA
  aggregation via a residual term on the frozen base weight; exact reference,
  not the main method, because the resulting state is residual/base + adapter
  and exact downlink scales with `K·r`.
- **Fed-SB** — Singhal et al., arXiv:2502.15436 — exact aggregation of a small
  trainable `R` between fixed bases; communication-first Tier-2 alternative,
  not the default because its fixed subspace confounds the server-KD capacity
  question.
- **ExeSQL** — arXiv:2505.17231 — execution-driven bootstrap (generate →
  exec-filter → train); the recipe behind §8.0's implemented Phase-1 target
  construction (`scripts/build_exec_bootstrap_probe.py` +
  `scripts/score_bootstrap_ex_match.py`) and the future §8.4 online
  execution-anchored distillation.
- **Self-consistency execution-voting (`sc`, §5.4/§7) — hyperparameter
  grounding (2026-07-16, literature search, no local PDF for these 3):**
  N=8/temperature=0.8 (this repo's default) exactly matches **CSC-SQL**
  (arXiv:2505.13271, 2025) — the closest prior-art match (open small-model
  SQL generator, not a GPT-4 API method, N sweep 4/8/16/32/64). Their own
  sweep on a 3B model (close to our 1.5B) shows EX still climbing well past
  N=8 (58.15→62.17→63.49→64.91→65.28 for N=4/8/16/32/64 — plateau only
  after ~32), so N=8 is a well-grounded *starting* default, not a tuned
  optimum — **N sweep (8/16/32) deferred, not run yet** (2026-07-16, user:
  cite the method now, try higher N later). **DAIL-SQL** [9] itself uses SC
  too (temp=1.0, N=5, GPT-4-only, Spider-leaderboard submission — 86.2%→
  86.6%, small δ because GPT-4 starts near ceiling) — confirms the "raise
  temperature only for SC, keep it 0 everywhere else" pattern our own
  default follows. **C3** (arXiv:2307.07306) uses N=20 for its SQL-level
  self-consistency step (temperature unreported). **Query and Conquer**
  (arXiv:2503.24364, 2025) reports gains visible from N=3, "N=15 = strong
  accuracy/cost balance," plateau ~N=50, at temp=0.7. **top_p: none of the
  4 papers above report tuning it for SC** — the literature's whole lever is
  temperature; our top_p=0.95 is transformers' own default, unexamined by
  any cited source, not a deliberate choice.

Mechanism figure: `fig_architecture_source.png` + `fig1_architecture.md` predate
the 2026-07-08 server-side pivot — **Fig. 1 must be redrawn** (teacher box moves
from client to server; public pool `P` added) before §3 of the paper is written.
