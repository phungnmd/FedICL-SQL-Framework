# FedICL-SQL — Problems & Possible Solutions

Anticipated problems across **method, experiment, engineering, novelty, and review**, each with root cause, evidence from the references, primary solution, and fallback. Use this to de-risk *before* coding and to pre-empt reviewer objections.

> **RE-ALIGNED 2026-06-09 to Fig.1 + verified refs.** Engine = **parametric** teacher→student KD: clients LoRA-train on **own private `Qᵢ` (supervised) + shared public `X` (teacher-KD)** — `L_i = L_sup(Qᵢ) + L_KD(X)` — upload **LoRA deltas only**, server **FedAvg/SecureAvg → Global SLM `M_G`** (= FedCoLLM [8] for SQL). The private-data term is mandatory (else FedAvg is a no-op → see A0). Demos stay local; nothing schema-coupled crosses the wire. The old risks built on a cross-client masked-demo store `G` / held-out-DB make-or-break (attempt-1) are retired — see `fig1_architecture.md` + Detailed-Plan REVISION banner.

Severity: 🔴 can kill the paper · 🟡 hurts a claim · 🟢 minor/polish.

Reference shorthand: [4] Light-SQL · [5] Fed-ICL (answer-fusion, QA — baseline) · [6] IFed-ICL · [7] FedMKT (logit-KD+MinED — P2) · [8] FedCoLLM (LoRA-FedAvg+KD — **engine anchor**).

---

## A. Methodological problems (the core risk area)

### A0. 🔴 FedAvg-no-op — clients training only on shared `X` makes federation vacuous
**Problem.** If every client LoRA-trains on the **same** public `X` with the **same** teacher targets, all clients' deltas are near-identical → `FedAvg ≈ single-client training on X` → aggregation adds nothing → **RQ1 is false by construction** (no gap between FedICL-SQL and one client training on `X`).
**Why it bites.** Federation only has value when clients carry **heterogeneous** signal. Identical data + identical targets = identical gradients = trivial average.
**Evidence.** FedCoLLM [8]'s clients each hold **private local data** and LoRA-train on it; the public set is only the KD-alignment medium, not the sole training signal. Remove the private-data term and FedCoLLM's federation collapses too.
**Primary solution.** Client objective has two parts: `L_i = L_sup(private Qᵢ) + L_KD(public X)`. `L_sup` = supervised CE on the client's **own private** `(q, gold-SQL)` (own schema, never leaves) → makes each delta org-specific → FedAvg pools real cross-org skill into `M_G`. `L_KD` = teacher distillation on `X` (alignment + general skill).
**Verification.** The make-or-break must beat the **null**: `M_G` EX > a single client trained on `X` alone. If it doesn't, federation is cosmetic.
**Fallback.** If private `Qᵢ` is too small to train on, increase per-client data via the Dirichlet partition granularity, or frame the public-`X`-only variant honestly as "distributed distillation" (not federation) — weaker claim.

### A1. 🔴 Public-set KD may not transfer to private client schemas — the central existential risk
**Problem.** The Global SLM `M_G` is distilled on a **public** NL→SQL set `X` (public schemas). If that skill doesn't transfer to a client's **own private schema** at inference, RQ1 fails and the "Fed" premise collapses.
**Why it bites.** SQL is schema-coupled. Attempt-1 proved cross-*schema* demo transfer fails (held-out EX 50%→3%). The bet now is different: KD teaches **general SQL skill** (JOIN/agg/nesting/aliasing), schema-agnostic; schema-specifics come from **local ICL** at inference.
**Evidence.** FedMKT [7]/FedCoLLM [8]: server-LLM KD on a public set raises client-SLM accuracy on *their own* tasks (e.g. CQA +6–8% over Standalone) — model-level skill transfer, not data transfer. Light-SQL [4]: local ICL supplies the schema-specific demos.
**Primary solution.**
- Eval on each client's **own schema, held-out questions** (seen schema, unseen Q) — the realistic + supported setting. `M_G` should beat SLM-only because it has stronger general SQL skill.
- **Decouple skill vs schema:** weights carry skill (from `X`), local ICL carries schema (from client's own store) — they compose, don't compete.
- **Exec-filter teacher targets:** only executable teacher SQL on `X` enters KD → clean supervision, no noise accumulation.
**Fallback.** If gains are marginal, reposition contribution as **privacy + efficiency at equal accuracy** ("near-centralized-LLM accuracy, on-prem SLM cost, no data shared") — still publishable.

### A2. 🟡 Negative transfer / catastrophic forgetting from LoRA-KD on `X`
**Problem.** LoRA-training Phi-3 on public `X` SQL might *degrade* it on a client's own-schema questions (distribution shift, overfit to `X` style).
**Why.** `X`'s public schemas differ from private ones; aggressive KD can overwrite useful priors.
**Solution.**
- Small LoRA (r=8) + low LR + few epochs; early-stop on a client own-schema dev slice.
- KD loss = `SQL-CE(teacher) + λ·KL(τ)` with modest λ; keep base frozen (LoRA only).
- **FedAvg regularizes:** averaging 3 clients' adapters damps any single client's overfit.
- Ablation: `M_G` EX **with vs without** KD on each client → must be net-positive per client, not just on average.
**Fallback.** Demo-level KD variant (teacher SQL as ICL demos, no weight update) — zero forgetting risk; cheaper comparator.

### A3. 🟡 Teacher-target generation on `X` is unprincipled / noisy
**Problem.** Teacher (72B) SQL on `X` may be wrong → distilling errors into `M_G`. (Note: parametric KD generates targets **offline on `X`**, not via per-query inference-time escalation — that was the attempt-1 framing.)
**Solution.**
- **Execution-filter:** drop teacher SQL that fails to execute on `X`'s public DBs → only gold-grade targets distilled.
- Optional **self-consistency:** sample teacher k× on hard `X` queries, keep majority-executable.
- Report teacher EX on `X` as the supervision-quality ceiling.
**Fallback.** Use Spider-train **gold** SQL directly as targets where available (teacher only for queries lacking gold) — guarantees clean supervision.

### A4. 🟡 "Convergence" claim from Fed-ICL doesn't transfer cleanly
**Problem.** Fed-ICL's [5] convergence proof is for **linear regression / linear self-attention**, not generative SQL or FedAvg-LoRA. Citing it as *your* guarantee is a stretch a reviewer will catch. (Applies to the Fed-ICL fusion **baseline**, not the parametric engine.)
**Solution.** Cite as **theoretical motivation** only for the fusion baseline; report **empirical convergence** (EX vs. round plateau) for both engine + baseline. For the parametric engine, lean on FedAvg convergence intuition (FedCoLLM [8]), not Fed-ICL's proof.
**Fallback.** Drop theoretical framing; present as an empirical systems paper.

---

## B. Experimental problems

### B1. 🔴 Spider is not natively federated — validity attack
**Problem.** Reviewer: "you *invented* the federation by partitioning a centralized dataset; results are an artifact of your split."
**Solution.**
- State explicitly it is a **simulated federation**, the standard methodology — Fed-ICL [5] §6.1, FedMKT [7], FedCoLLM [8], IFed-ICL [6] all do exactly this (Dirichlet partition). Cite as precedent.
- Justify with a **concrete privacy scenario** (multiple hospitals/banks, each a client owning private schemas).
- Run the **Dirichlet α sweep** (0.1/1.0/100) to show conclusions hold across heterogeneity.
- Report **mean ± std over multiple random partitions/seeds**.
**Fallback.** Add a second naturally-multi-schema setting (CORDIS from [4], or BIRD's many DBs) as a robustness check.

### B2. 🟡 SLM execution accuracy on Spider may look low
**Problem.** Light-SQL [4] hit only 41% EX on CORDIS. Low absolute numbers read as a weak system.
**Solution.**
- Strong SLM (Phi-3-mini), report **EX and EM**; lead with **relative** gains (`M_G` vs SLM-only), not absolute SOTA.
- Frame headline as **efficiency–privacy tradeoff** (Pareto: near-teacher accuracy at fraction of cost).
**Fallback.** Report on *easy/medium* Spider buckets separately; acknowledge hard-query gap as future work.

### B3. 🟡 72B teacher is compute-heavy / hard to reproduce
**Problem.** Qwen2.5-72B needs an A100 or paid API; reviewers care about reproducibility.
**Solution.**
- Teacher runs **once, offline, on the shared set `X` only** (not full workload, not per-query) → bounded calls.
- **Cache** teacher SQL (deterministic, temp=0) → re-runs free; release the cache.
- **Smaller-teacher ablation** (7B/14B) to show framework works without a 72B.
**Fallback.** Hosted API for the teacher; report cost in $ and note the cache.

### B4. 🟡 Communication-cost comparison can be gamed / unfair
**Problem.** Comparing LoRA-delta bytes vs full-FedAvg GB is apples-to-oranges; or vs Fed-ICL's text answers.
**Solution.** Report **bytes/round AND rounds-to-converge** (total cost) + **accuracy-per-byte**, against three fair points: full-weight FedAvg (upper), Fed-ICL [5] answer-fusion (parameter-free, lower), ours (LoRA deltas, middle). Be explicit what's counted.
**Fallback.** Present comm cost descriptively, not as the central claim.

### B5. 🟢 Metric mismatch (EM too strict, EX needs live DB)
**Problem.** EM penalizes valid SQL; EX requires executing on actual DB instances.
**Solution.** **EX primary** (Spider official evaluator), EM secondary, per [4]/Spider. Use standard Spider test-suite execution scripts.

### B6. 🟠 Missing the true parametric ceiling — Centralized-FT
**Problem.** Outline lists "Centralized ICL" as the upper bound, but for a **parametric** (FedAvg) method the honest ceiling is **centralized fine-tuning** (pool all private data, LoRA-train one SLM). Without it, reviewers ask "how much does FedAvg lose vs just centralizing the training?" — and the federation cost is unquantified.
**Solution.** Add **Centralized-FT** to baselines (P3). Report the FedAvg→Centralized-FT gap; small gap = federation is "free", which strengthens the privacy story.
**Fallback.** If compute-bound, run Centralized-FT on one (Spider) setting only as a reference point.

### B7. 🔴 Single-run numbers are not credible
**Problem.** temp=0 gives a deterministic *decode*, but partition split + LoRA init + retrieval sampling still vary run-to-run. A "+Z pts EX" claim from one run has no error bar → reviewers discount it.
**Solution.** Every headline number = **mean ± std over ≥3 seeds**. Make-or-break comparisons (FedICL-SQL vs SLM-only; vs Centralized-FT) get a **significance test** — paired bootstrap over per-query EX, or McNemar on exec-correct/incorrect — report p / CI.
**Fallback.** If ≥3 seeds is too costly for *every* cell, do it for the headline T1 rows + make-or-break, single-run for ablations (state this).

---

## C. Engineering / technical problems

### C1. 🟡 Non-differentiable execution loss (Fig.1 "Execution loss") + structure loss must be differentiable
**Problem.** Fig.1 client box lists "Execution loss" and "Structure loss." Execution correctness is **non-differentiable** (can't backprop through a DB engine). And "Structure loss = AST/clause match" is *also* non-differentiable if defined as a discrete AST-edit-distance.
**Solution.**
- **Execution loss → target filtering**, NOT a gradient term: keep only executable teacher SQL on `X` before KD. Stated honestly in §3. (Exec-guidance for SQL is **prior art** — claim only the *federated-KD-filtering* angle as novel, not exec-guidance itself.)
- **Structure loss → differentiable skeleton-token CE**: weighted CE on SQL clause/structural tokens (`SELECT/FROM/JOIN/WHERE/GROUP BY/agg`, identifiers stripped). Normal CE → backprops cleanly. NOT AST-edit-distance.
**Fallback.** Drop both extra terms; pure sequence-CE + KL KD — still valid, simpler. (Or fold structure in as a higher CE weight on skeleton tokens.)

### C2. 🟡 Tokenizer mismatch breaks logit-level distillation (P2)
**Problem.** Teacher (Qwen) and student (Phi) tokenize differently → can't align token-level logits for soft-KD.
**Evidence/solution.** **MinED** (minimum-edit-distance token alignment) from FedMKT [7] §3.2 — the exact fix, **deferred to P2**. P1′ uses **sequence-level KD** (train student on teacher's SQL *strings*) which needs **no** logit alignment.
**Fallback.** Stay sequence-level (no logits, no MinED) for the whole paper; logit-KD becomes optional future work.

### C3. 🟡 Schema + demos overflow the SLM context window
**Problem.** Large schemas + k demos can exceed an SLM's context; [4] shows k=5 already degrades.
**Solution.** **Schema linking/pruning** (only question-relevant tables/cols); keep **k=1–3** ([4] optimum); SQL-only demo organization to fit more in fewer tokens.
**Fallback.** Cap schema serialization; truncate to top-N relevant tables by question-similarity.

### C4. 🟢 Non-determinism hurts reproducibility
**Problem.** Sampling randomness → unstable EX.
**Solution.** **temperature=0**, fixed seeds, deterministic decoding (per [4]). Report mean±std over seeds for partition + LoRA-init randomness.

### C5. 🟢 FL simulation engineering overhead
**Problem.** Real multi-node FL is heavy.
**Solution.** **Simulate** clients sequentially on one GPU (a round = loop over clients: each LoRA-trains, server averages adapters). Flower or a lightweight custom loop. No real network needed.

---

## D. Privacy problems (a claimed contribution → must defend)

### D1. 🔴 Privacy claim is asserted, not proven
**Problem.** "We preserve privacy" without evidence invites rejection. **Note the corrected threat model:** what crosses the wire = **encrypted LoRA-delta weights** (+ DP noise), NOT demos. LoRA deltas can in principle leak training-data signal.
**Solution.**
- **Threat model precise:** raw rows + schema stay local (Fig.1 "Local Data & Schema" has no outgoing data arrow); only DP-perturbed, encrypted LoRA deltas + teacher/public demos transmit. Server semi-honest (per [7][8]).
- **DP-SGD on LoRA** (gradient perturbation, Fig.1) for a formal (ε,δ) guarantee + privacy-utility curve. ⚠️ **Claim DP as a contribution only if measured** — report (ε, EX-cost) and run the reconstruction attack with DP *on*. If unmeasured, scope DP to future work, don't headline it.
- **Prompt-extraction / reconstruction attack** (Fed-ICL [5] §6.4) adapted: adversary tries to reconstruct client private questions from `M_G` / deltas; report low success.
**Fallback.** Scope honestly to "no raw data/schema transmitted; only model-update weights" + DP ablation, without over-claiming.

### D2. 🟡 Masking weakens utility (privacy–utility tension)
**Problem.** More masking = more privacy but worse demos. **Confirmed in [4]:** masked-similarity MQS_S=37% EX **< plain QTS_S=41%** — masking *costs* accuracy.
**Solution.** Frame masking as a **retrieval/privacy lever with a measured cost**, not an accuracy win. Plot EX vs masking level / DP-noise (the outline's required "Privacy-Utility Trade-off" subsection). Show the knee where privacy is high and utility barely drops. Masking is **retrieval-only** (never in the generation prompt).

---

## E. Novelty / positioning problems

### E1. 🔴 "Just a combination of existing parts" — incremental-novelty rejection
**Problem.** LLM-SLM KD (FedMKT/FedCoLLM), Fed-ICL, and SLM-NL2SQL (Light-SQL) all exist. A reviewer may call this mere assembly.
**Solution.**
- Sharpen the **gap table** (§2.6): **no reference does federated Text-to-SQL** — [5][6][7][8] are all QA/classification; [4] is single-client. The Federated + LLM-SLM-KD + schema-aware-ICL + **NL2SQL-with-schema-privacy** combination is empty in the literature.
- Emphasize genuinely new pieces: (a) **federated SQL KD over a public query set with private schemas kept local**, (b) **execution-guided KD-target filtering** (SQL-specific, no ref has it), (c) **DP on the SQL-KD deltas**.
- Show the combo unlocks something parts can't: cross-org SQL skill transfer without data sharing.
**Fallback.** Lean on **application novelty** (first federated LLM-SLM-KD framework *for Text-to-SQL*) + thorough empirical study — acceptable for an applied Q3 journal.

### E2. 🟡 Overlap with very recent concurrent work
**Problem.** Federated-ICL/KD is hot (2024–25: [5][6][7][8]); something near-identical may appear.
**Solution.** Differentiate on **task** (generative structured SQL vs QA/classification), **schema-aware local ICL**, and **execution-grounded KD**. Cite [5][6][7][8] as related-but-different (none touch SQL over private schemas).

---

## F. Writing / review-process problems

### F1. 🟡 IAJIT formatting / template compliance
**Problem.** Wrong template → desk reject. No math/symbols in title or abstract.
**Solution.** Use the IAJIT IEEE two-column template from the start; abstract symbol-free (150–250 words); run `/ars-citation-check` and `/ars-format-convert`. Target ~10–14 pages.

### F2. 🟡 Reproducibility expectations
**Problem.** Reviewers expect code for an empirical FL paper.
**Solution.** Release a GitHub repo (partition scripts, LoRA-KD, FedAvg, eval, configs) as [4] did. Fixed seeds, cached teacher outputs, config files.

### F3. 🟢 Claims outrunning evidence
**Problem.** Over-claiming "privacy-preserving" / "SOTA" without backing.
**Solution.** Every claim → a table/figure. Run `/ars-reviewer` before submission.

---

## Priority triage (do these first)

| Rank | Problem | Why first |
|---|---|---|
| 1 | **A0** FedAvg-no-op (train on private `Qᵢ` + public `X`) | most fundamental; if clients train on `X` only, federation is vacuous and RQ1 cannot be true. Fix the objective before anything else. |
| 2 | **A1** public-KD → private-schema transfer | existential; this IS the make-or-break (does `M_G` beat SLM-only on own schema) |
| 3 | **A2** negative transfer / forgetting | the most likely way A1 silently fails; ablate per-client |
| 4 | **D1** prove privacy | claimed contribution; needs DP (measured) + reconstruction attack |
| 5 | **B1** simulated-federation validity | reviewer's first attack; lock partition + α sweep |
| 6 | **E1** combination-novelty | shapes framing + §2.6 gap table |

**Earliest decisive test (in TODO P1′):** P0 single-client ✅ → teacher SQL on public `X` (exec-filtered) → client LoRA-train on **private `Qᵢ` + KD on `X`** → FedAvg → `M_G` → eval EX on each client's **own-schema held-out questions** vs three points: SLM-only floor, **single-client-trained-on-`X` null** (kills A0 if `M_G` doesn't beat it), LLM-only ceiling+cost. Report **mean±std over ≥3 seeds + significance**. If `M_G` EX > floor AND > the no-op null, at cost << ceiling, **A0+A1 answered and the paper is alive** — ~1–2 weeks tells you.

---

*Companion files: `detailed_plan.md` (build + experiment plan), `fig1_architecture.md` (architecture mechanism), `learning_primer_vi.md` (concepts). Problems grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM and the approved outline.*
