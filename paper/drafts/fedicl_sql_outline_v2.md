# FedICL-SQL — Revised Outline (v2, working draft)

> **Status: PROPOSED revision of the approved outline — supervisor sign-off pending.**
> The approved source of truth stays `fedicl_sql_outline.pdf` / `fedicl_sql_outline.md` (DO NOT edit those).
> This v2 keeps the approved **section structure** (outline wins on structure) and only (a) de-risks the
> two fragile title pillars (Teacher, ICL) and (b) reconciles the outline with `detailed_plan.md` + Fig.1.
> Every change from the approved outline is tagged **`[Δ]`** so the diff is reviewable at a glance.
> **Labels & notation** (K=clients, T=rounds, k=shots, B1–B7, Ab1–Ab5, T1–T3, F1–F6, stages/tiers) are canonical in **`detailed_plan.md §0`** — this outline follows it verbatim.

**Title:** *FedICL-SQL: A Novel Federated Large-Small Language Models Framework with In-Context Learning for Natural Language to SQL*
**Authors:** Student + Quang-Hung Le* (corresponding) — Dept. of IT, Quy Nhon University, Vietnam.
**Venue:** International Arab Journal of Information Technology (IAJIT), WoS-Q3 — IEEE two-column, ~10–14 pp, no math/symbols in title or abstract, keywords required.

---

## Reading guide — the 3 pillars and their risk

The title sells three pillars. Honest risk assessment drives this outline:

| Pillar | Mechanism | Risk on labeled Spider | How v2 protects it |
|---|---|---|---|
| **Federated** (RQ1) | LoRA + FedAvg → Global SLM `M_G` | *low* — FedAvg works; but `M_G > B2-solo` is **near-trivial** (pools ~K× data) | reframe RQ1 around **`M_G` → centralized ceiling B3** (small federation gap), not `> B2` `[Δ]` |
| **LLM teacher** (RQ3) | 72B teacher → 1.5B student KD (hard+soft) | **medium** — labeled teacher SQL ⊆ gold, but **soft-KL** carries dark knowledge gold lacks | soft-KL via DeepInfra top-20 logprobs (Qwen↔Qwen aligned) makes the teacher a fair, winnable comparison; **Without-Teacher ablation** reports the delta; label-free regime shows necessity `[Δ]` |
| **Schema-aware ICL** (RQ2) | retrieval + ICL-Hub demos | **high** — masking *costs* EX [4]; delta may be ~0 | ICL must be load-bearing on **held-out**; if flat seen+held-out, reframe at gate `[Δ]` |

**One-sentence thesis:** *a cloud LLM teacher and many on-premise SLM students collaboratively raise Text-to-SQL accuracy across heterogeneous private databases — approaching centralized fine-tuning while transmitting only encrypted, DP-perturbed LoRA-delta weights and teacher-authored public demonstrations, never raw schemas or data.*

---

## Abstract (150–250 w, no symbols) — write after results
Background (Text-to-SQL importance; distributed enterprise DBs) → Problem (privacy, schema heterogeneity, LLM cost) → Method (federated LLM-SLM + schema-aware ICL + federated KD; weights-only transmission) → Headline results (EX/EM vs SLM-only floor and centralized ceiling; communication + efficiency; privacy-utility) → Deployment implication.

---

## 1. Introduction
- **Natural Language to SQL** — task, enterprise value.
- **Three challenges** — (i) data-privacy constraints across organizations, (ii) schema heterogeneity / unseen DBs, (iii) high compute cost of LLMs at inference.
- **Motivation** — Federated Learning (collaborate w/o sharing data); LLMs (strong SQL synthesis); SLMs (cheap on-prem deployment); ICL (rapid adaptation to unseen schemas).
- **Research questions:**
  - **RQ1 (FL effectiveness):** does federation let the global SLM **approach centralized fine-tuning** (B3) while keeping data private — not merely beat isolated per-client SLM? `[Δ: was "improve performance in federated environments"; sharpened so the trivial >B2 result isn't the claim]`
  - **RQ2 (ICL effectiveness):** does schema-aware ICL improve generalization to **unseen/held-out** schemas?
  - **RQ3 (LLM→SLM transfer & efficiency):** does teacher KD give a better efficiency–performance trade-off than LLM-only or SLM-only — **and does it beat free gold-label CE** (gold-CE), the test that the LLM teacher earns its place? `[Δ: added the gold-CE clause]`
- **Objective** — a privacy-preserving Text-to-SQL framework (FedICL-SQL) integrating FL + LLM-SLM collaboration + ICL across distributed DBs.
- **Contributions:**
  1. Federated LLM–SLM framework for Text-to-SQL (server teacher + global ICL Hub + aggregation engine; client SLM students with private schemas) — Fig. 1.
  2. Schema-aware ICL (schema-aware retrieval + prompt construction; masking is **retrieval-only**, demos shown unmasked). `[Δ: state masking-is-retrieval-only here so reviewers don't read masked SQL into the prompt]`
  3. Federated SQL knowledge distillation — primary novelty = **(i) reasoning/CoT distillation** + **(ii) exec-based KD-target filtering inside the federated loop**; skeleton-token structure loss is a **secondary** claim, reported only if its ablation moves EX with a CI. `[Δ: demoted skeleton loss from co-equal novelty]`
  4. Privacy-preserving collaborative optimization — encrypted/compressed LoRA-delta transmission + secure aggregation; **DP (ε, EX) reported as a contribution only if measured**, else scoped to future work. `[Δ: was unconditional; standard secure-FL alone is not novel]`
  5. Extensive evaluation on Spider + Spider-Realistic under a federated non-IID partition; FL / efficiency / privacy metrics; five ablations.

---

## 2. Related Work
- **2.1 Natural Language to SQL** — schema linking, exec accuracy, Spider protocol.
- **2.2 LLMs for Text-to-SQL** — prompting/ICL, cost.
- **2.3 Small Language Models** — Light-SQL [4] (ICL + retrieval-only masking; same corresponding author).
- **2.4 Federated Learning** — FedAvg [McMahan] / FedProx [Li] (parametric weight aggregation — our engine's theory); Fed-ICL [5] (parameter-free answer-fusion + convergence proof — **baseline**, different mechanism); FedMKT [7] (logit-space KD, no weight FedAvg — related work, different mechanism); FedCoLLM [8] (LoRA-adapter FedAvg + global SLM + CE+λKL KD — **engine anchor**); federated BART [1]. `[Δ: cite McMahan/FedProx for convergence; do NOT lean on Fed-ICL's fusion proof for our parametric engine]`
- **2.5 In-Context Learning** — ICL survey [3]; IFed-ICL [6] (implicit vectors, classification — side ref).
- **2.6 Research Gap** — gap table (Light-SQL/Fed-ICL/FedMKT/IFed-ICL/FedCoLLM × NL2SQL/Federated/LLM-SLM/ICL/schema-privacy). Gap = no framework jointly delivers cross-org collaboration without sharing schemas/data **+** schema-aware ICL to unseen DBs **+** LLM→SLM transfer, *for Text-to-SQL*.

---

## 3. Proposed Approach  *(structure = approved outline; mechanism = Fig.1 + detailed_plan §2)*
- **3.1 Problem Formulation** — server `S` + `K` clients; client `i` holds private schema `Sᵢ`, private pairs `Qᵢ`, local SLM `Mᵢ`; server holds teacher `M_T`, global ICL Hub `G`, aggregation engine `A`, broadcast `M_G`. Goal: maximize mean EX across clients while `Sᵢ`, raw `Qᵢ` stay private; only protected LoRA deltas cross the wire.
- **3.2 Framework Overview (Fig. 1)** — three planes (server / secure-channel / clients); name the five figure flows; offline-once teacher pass on **public X only** feeds both ICL Hub demos and KD targets.
- **3.3 Global LLM Teacher** — Qwen2.5-72B-Instruct (DeepInfra API, `top_logprobs=20`); produces `reasoning ⊕ SQL` + per-token top-20 logprobs on public X, exec-validated, cached; never sees client schema/rows.
- **3.4 Local SLM Student** — **Qwen2.5-1.5B-Instruct (primary)** — tokenizer-aligned with the teacher → soft-KL KD without MinED. Phi-3-mini / Gemma-2B / TinyLlama → SLM-arch ablation (A5). `[Δ: approved outline named Phi-3/Gemma/TinyLlama as "e.g."; Qwen-1.5B added as primary (justified: tokenizer-aligned → clean soft-KL) — NEEDS supervisor sign-off]`
- **3.5 Teacher–Student Collaboration** — **training-time KD roles only** (matches Fig.1: reasoning-guidance + teacher demos → ICL Hub + KD loss). Runtime low-confidence escalation is **out** (adds inference-time teacher cost + leaks client query patterns) — noted as a §5 deployment option. `[Δ: explicitly scope to training-time; the figure shows no answer-vote/escalation box]`
- **3.6 Schema-Aware ICL** — prompt `σ(q,S,I,Q)=q⊕S⊕I⊕Q`; BGE + FAISS top-`k` (`k∈{1,3}`, inverted-U at 5 [4]); **masking = retrieval-similarity only, demos shown unmasked**; ICL runs locally; shared ICL Hub = teacher/public-sourced demos on X. Cross-schema generalization (RQ2) = Global-SLM skill + local ICL on the held-out schema's own demos, **not** shared private cross-schema demos.
- **3.7 Federated SQL Knowledge Distillation** — present Fig.1's verbatim loss `L = λ₁L_SQL + λ₂L_KD + λ₃L_struct + λ₄L_exec`, then define:
  - `L_SQL` token CE: vs own gold on `Qᵢ` (= `L_sup`), vs teacher SQL on X;
  - `L_KD` distil teacher *behavior* on X **incl. reasoning (CoT)**: `CE(r̂_T⊕ŝ_T) + λ·KL_τ` over teacher top-20 logprobs (teacher-forced, aligned tokenizer → no MinED, single-phase);
  - `L_struct` skeleton-token CE — **secondary**; differentiable; overlaps `L_SQL` → claim only if λ₃ ablation moves EX;
  - `L_exec` = **non-differentiable → realized as exec-match target filtering**, not a gradient term — own this divergence.
  - ⚠️ **Federation-validity guard:** clients train on own private `Qᵢ` + public X; training on X alone makes all deltas identical → FedAvg degenerates → RQ1 dies. `[kept]`
  - ⚠️ **Teacher value:** on labeled Spider, exec-filtered teacher SQL ⊆ gold → teacher's value = **soft-KL** (dark knowledge gold lacks) + **CoT distil**, plus the **label-free unlabeled-X regime** (no gold exists) — measured in §4. `[Δ: soft-KL now feasible via top-20 logprobs]`
- **3.8 Federated Optimization (Algorithm 1)** — round loop: broadcast `M_G` → local ICL → local LoRA-train `L_sup(Qᵢ)+L_KD(X)` → encrypt/compress/DP-perturb delta → upload **weights only** → FedAvg/FedProx → `M_G`. Convergence: **McMahan/Li theory** as motivation; report **empirical** EX-vs-rounds. Privacy mechanisms: no raw rows/schema leave; encrypted+compressed LoRA deltas; DP (Stage-B); secure agg (SSL/TLS); identifier masking. `[Δ: theory citation corrected]`

---

## 4. Experiments
### 4.1 Experimental Setup
- **Datasets:** Spider (primary; schema-disjoint 3-pool split: public X / client-private / held-out, `∩=∅`, persisted DB→pool map); **Spider-Realistic (Tier-2, near-free — same DBs, paraphrased Qs)** `[Δ: promoted from "nice-to-have"; a single-benchmark headline is thin for Q3]`. Dirichlet(α∈{0.1,1,100}) over the private pool; default `K=3` cross-silo, sweep `{3,5,10}`. **Eval provenance stated openly:** own-schema eval = 20% per-DB slice of Spider train; held-out = Spider dev (frozen, touched once).
- **Models:** teacher Qwen2.5-72B (DeepInfra, `top_logprobs=20`, targets cached once on X); students Qwen2.5-1.5B (primary) + Phi-3/Gemma-2B/TinyLlama (A5); retriever bge-small + FAISS; 4-bit QLoRA, temp=0, max-new=256.
- **Baselines:** B1 LLM-only (ceiling) · B2 SLM-only (RQ1 floor) · **B3 Centralized-FT (true parametric ceiling — the RQ1 bar)** · B4 Centralized-ICL · B5 Without-ICL (=Ab1) · B6 FedAvg-LoRA no-teacher (**=gold-CE, the teacher-value bar**) · B7 Fed-ICL [5] adapted to SQL.
- **Metrics:** EX (primary) + EM (Spider); communication (bytes/round, total) + convergence (EX vs round); efficiency (latency, VRAM, FLOPs); privacy (channel-matched — see §4.2). **Stats:** ≥3 seeds, mean±std; significance via paired bootstrap/McNemar **pooling per-query EX across all clients** (3×~200 q → low per-client power); report effect size + CI. `[Δ: pooled-significance + effect-size made explicit]`

### 4.2 Results & Discussion
- **Overall Performance (T1)** — EX/EM, all methods × {Spider, Spider-Realistic}, seen vs held-out.
- **Impact of ICL** — `[risk: must be load-bearing on held-out; if flat seen+held-out, reframe title claim]`
- **Impact of LLM Teacher** — full teacher-KD vs **gold-CE (B6)** (the Without-Teacher ablation): isolates teacher value; soft-KL + CoT are the channels gold lacks. `[Δ: reported as an ablation delta, not a gate]`
- **Impact of Federated Learning** — `M_G` vs B2 (expected gain) **and the gap to B3 ceiling** (the real RQ1 story).
- **Communication Efficiency (T3)** — bytes/round + rounds-to-converge vs FedAvg-LoRA & Fed-ICL.
- **Privacy–Utility Trade-off** — channel-matched: **F5a** prompt-extraction ±masking (demo/ICL-Hub channel only); **F5b** membership-inference on `M_G` and/or DP (ε, EX) (weights channel). Never cite F5a for the weights channel.
- **Ablations:**
  1. Without ICL.
  2. Without federated learning (local-only).
  3. **Without Teacher = gold-CE (Ab3a)** — identical data, target-only difference → isolates teacher value. Report the delta; teacher value = soft-KL (dark knowledge) + CoT, which gold-CE lacks.
  3b. **Label-free KD = unlabeled-X (Ab3b)** `[Δ NEW, secondary]` — strip gold from X; KD on exec-validated teacher `reasoning⊕SQL` + soft logprobs only. The regime where the 72B is *necessary* (no gold exists); matches the deployment story.
  4. Retrieval size `k∈{0,1,3,5}`.
  5. Different SLMs (Qwen-1.5B / Phi-3 / Gemma-2B / TinyLlama).
- **Figures:** F1 architecture (=Fig.1) · F2 convergence (EX vs round, per α) · F3 Pareto (EX vs cost) · F4 heterogeneity (EX vs α) · F5 privacy (F5a/F5b) · F6 client scaling (EX + comm vs K∈{3,5,10}, **caption reports per-client N** — K=10 thinning is data-starvation, not a method failure `[Δ]`).

---

## 5. Conclusion
- Summary of FedICL-SQL; main findings (federation→ceiling gap; teacher value scope; ICL on held-out; comm/efficiency; privacy-utility).
- Practical implications (on-prem privacy-constrained Text-to-SQL).
- Future work: runtime low-confidence teacher escalation; Federated RAG; multi-database reasoning; agentic SQL; continual federated learning; real-world enterprise deployment; **DP at scale** if not measured here.

---

## Divergences from the approved outline — for supervisor sign-off
1. **RQ1 reframed** — "approach centralized ceiling B3", not the trivial "beat isolated SLM".
2. **RQ3 keeps the advisor's "Without Teacher LLM" ablation** (no kill-gate) — soft-KL KD makes the teacher a fair, winnable comparison; report the delta.
3. **New Ablation 3b (label-free unlabeled-X)** — secondary; the teacher's necessary-value regime.
4. **Primary student = Qwen2.5-1.5B** — the approved outline §4.1 listed Phi-3/Gemma/TinyLlama as "e.g."; Qwen-1.5B added as primary. Justification: tokenizer-aligned with the 72B teacher → soft-KL KD without MinED.
5. **Skeleton-token loss demoted** to a secondary, must-be-measured claim (overlaps `L_SQL`).
6. **Privacy contribution conditional** on measured DP (ε, EX); else method-detail, not headline.
7. **Spider-Realistic promoted to Tier-2** (near-free; Q3 expects ≥2 benchmarks).
8. **Convergence theory** = McMahan/FedProx (parametric), not Fed-ICL's parameter-free fusion proof.
9. **Teacher–student collaboration scoped to training-time KD** (runtime escalation → §5), matching Fig.1.
10. **Teacher logits available via DeepInfra** (`top_logprobs=20`) → real hard+soft Hinton KD at P1; MinED/separate-P2 phase retired (Qwen↔Qwen aligned).

*Grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM + `detailed_plan.md` + `fig1_architecture.md` (mechanism) + the approved outline (structure).*
