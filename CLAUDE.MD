Project requirements:
Paper "FedICL-SQL: A Novel Federated Large-Small Language Models Framework with In-Context Learning for Natural Language to SQL"

Prepare paper draft & run experiments following the outline - `paper/drafts/fedicl_sql_outline.pdf`

Reference this image for "Fig. 1: Architecture of the Proposed Framework": `paper/figures/fig_architecture_source.png`

Reference papers: `paper/references/pdf/`

Target journal: "International Arab Journal of Information Technology" (https://www.iajit.org). International scientific journal ranked WoS-Q3.

Use the journal's LaTeX template per instructions at: https://www.iajit.org/app/webroot/upload/files/IAJIT%20templet(1).docx

---

## Project file structure

**Input documents (provided by user — DO NOT modify):**
- `paper/figures/fig_architecture_source.png` — architecture diagram, used for "Fig. 1: Architecture of the Proposed Framework".
- `paper/notes/fig1_architecture.md` - transcription of `paper/figures/fig_architecture_source.png`; must follow this architecture.
- `paper/drafts/fedicl_sql_outline.pdf` — approved outline; source of truth for paper structure.
- `paper/templates/iajit_template.md` — journal template (IEEE 2-column) for formatting the draft.
- `paper/references/pdf/` — reference PDFs.
- `paper/references/md/` — markdown versions of the references for quick reading. Shorthand: [4] Light-SQL (base NL2SQL+ICL; masking retrieval-only), [5] Fed-ICL (parameter-free answer-fusion, QA not SQL — our baseline + privacy-attack method), [6] IFed-ICL (implicit vectors, classification — side ref), [7] FedMKT (**logit**-space KD; does NOT FedAvg weights → related-work ref), [8] FedCoLLM (**LoRA-adapter FedAvg + global SLM + CE+λKL KD** — co-tuning ref; note it does *server-side* KD, we do *client-side*). Aggregation theory anchor = McMahan/FedProx.

**Working documents (created & maintained by Claude):**
- `paper/notes/detailed_plan.md` — detailed plan: method definition (equation-level), experiment matrix, section → template mapping, milestones, repo layout. **Source of truth for "what to build".**
- `paper/notes/fig1_architecture.md` — verbatim transcription of the Fig.1 architecture PNG + mechanism implications + reference grounding. **Source of truth for "the method's mechanism"** (engine = parametric, weights-only wire).
- `paper/notes/system_architecture.md` — **full system architecture document** (10 sections): 3-plane diagram, all components, round loop pseudocode, data flows, key invariants, notation table. **Read this before writing §3 or answering any architecture question.**
- `paper/notes/todo.md` — **execution checklist + progress & RESULTS tracking** (see convention below).

## Convention: use `paper/notes/todo.md` to track progress & results

`paper/notes/todo.md` is a live tracking file. RULES:
- Task done → change `[ ]` to `[x]`.
- After each experiment/step with metrics → record **actual results immediately below that task** (EX/EM, latency, comm cost, escalation rate, run date, config). Example: `[x] T1 Overall Performance → FedICL-SQL EX=XX%, SLM-only=YY%, held-out +Z pts (2026-06-XX)`.
- Teacher-value comparison (P1′, exp `p1_teacher_value`): report **deltas** — `M_G` vs SLM-only (federation gain), vs Ab3-FedAvg-no-KD (teacher value via soft-KL) — as measured analysis, **not pass/fail gates**. RQ1 bar = `M_G` approaches the centralized ceiling B3, not the trivial `> SLM-only`. (Old TEST A1 "shared ICL store" retired — attempt 1, negative; see fedicl-sql/docs/archive/p1-attempt1-cross-schema-demo-store/.)
- Each working session: read TODO first to know current phase, update TODO after finishing.
- When changing a decision (variant, number of clients, dataset...) → update both TODO and Detailed-Plan §8.

## Working conventions
- When outline and plan conflict → outline (PDF file) wins; update plan to match.
- Must follow the architecture in `paper/figures/fig_architecture_source.png`.
- Direction (RE-ALIGNED 2026-06-16 — advisor: local client teacher): federation engine = **PARAMETRIC** LLM-teacher → SLM-student KD — clients **LoRA-train** on **own private `Qᵢ`** (gold CE + local 7B teacher KD on same `Qᵢ`; `SQL-CE + λ·KL_τ(top-K) + skeleton-structure + exec-filter`), upload **LoRA deltas only**, server **FedAvg/SecureAvg → Global SLM `M_G`**. No public X pool. No ICL Hub G. Aggregation theory = **McMahan/FedProx**; **FedCoLLM [8]** = co-tuning related-work. **FedMKT [7] = logit-space KD, does NOT FedAvg weights → related-work ref.** Fed-ICL [5] answer-fusion = parameter-free **baseline** (share answers, not demos). Cross-client transfer = general SQL skill via Global SLM.
- **Models locked (2026-06-16):** teacher = **Qwen2.5-7B-Instruct** (**local HuggingFace, per client**, runs on client's own `Qᵢ`, top-K logprobs via HF generate); student = **Qwen2.5-1.5B-Instruct** (tokenizer-aligned → soft-KL KD without MinED; Phi-3/Gemma-2B/TinyLlama = A5 ablation). `L_KD = CE(reasoning⊕SQL) + λ·KL_τ(top-K teacher logprobs)` — single-phase hard+soft, **no P2/MinED**. Sequential VRAM: unload 7B teacher before loading 1.5B student.
- Build order: **parametric LoRA+FedAvg KD (= Fig.1, primary) first** — hard CE + soft-KL via local 7B logprobs, single-phase → Fed-ICL fusion as baseline.
- ICL = retrieval-only masking (Light-SQL [4]): mask only for retrieval similarity; demos shown to the model are unmasked. Never put masked SQL in the generation prompt. ICL serves RQ2, runs locally per client, pool = `Qᵢ` only. ⚠️ masking can **cost** accuracy ([4]: MQS_S 37% < QTS_S 41% EX) — frame as privacy/transfer lever, not an accuracy win. ⚠️ **masking is PLANNED, not yet wired** into the retriever.
- Privacy claim: **no raw rows / no schema / no teacher outputs leave the client; teacher runs fully on-premise; only encrypted, DP-perturbed LoRA-delta weights transmit** (Fig.1 "Weights Only"). Do NOT claim "no weights leave" — weights DO cross. Masking + DP (gradient perturbation) are the privacy mechanisms. Novelties = exec-based KD-target filtering + CoT distillation + **skeleton-token structure loss**. DP (gradient perturbation on LoRA deltas) = privacy contribution; report (ε, EX) at Stage-B.
- Data hygiene: tune only on `val` (a slice of Spider train); the `test` split (= Spider dev, since Spider test is hidden) is frozen — touch once for final numbers. Headline results need ≥3 seeds + a significance test.
- Repository, data & experiment conventions (raw/processed split, CSV processed data, per-experiment folders, results carry `model`/`time_average`/`gpu_vram`) → see `README.md`. **MANDATORY.**
- Write §3 Method + §2 Related Work in parallel while coding (no need to wait for results).
