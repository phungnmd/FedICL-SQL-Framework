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
- `paper/notes/DECISIONS.md` — **slim decision + notation record**: arm naming map (feature names, no A/B letters), locked decisions, notation table. **Source of truth for "the rules we locked".** (Replaced the retired `detailed_plan.md`; "what to build next" is decided per session, not pre-planned.)
- `paper/notes/fig1_architecture.md` — verbatim transcription of the Fig.1 architecture PNG + mechanism implications + reference grounding. **Source of truth for "the method's mechanism"** (engine = parametric, weights-only wire).
- `paper/notes/system_architecture.md` — **full system architecture document** (10 sections): 3-plane diagram, all components, round loop pseudocode, data flows, key invariants, notation table. **Read this before writing §3 or answering any architecture question.**
- `paper/notes/LAB_LOG.md` — **session log + progress & RESULTS tracking** (see convention below).

## Convention: track progress in `LAB_LOG.md` + results in `RUNS.csv`

Progress/results tracking (`paper/notes/todo.md` retired 2026-06-23):
- **`paper/notes/LAB_LOG.md`** — session log: what was done, current phase, decisions, next steps. Read first each session; append after finishing.
- **`fedicl-sql/experiments/RUNS.csv`** — canonical numbers (auto via `save_results`): run_id, EX/EM, model, retrieval, k, seed, git_sha. Headline metrics come from here, never re-typed.
- **`DECISIONS.md` §3** — decision record. Changing a decision (variant, clients, dataset, default) → update §3 + note in LAB_LOG.
- **Arm names = feature names, no A/B/Ab letters** (retired 2026-06-23): `base` / `local` / `central` / `fedavg` / `fedkd` / `teacher`; ICL = eval overlay → suffix `@k3`. Map in `DECISIONS.md` §1.
- Teacher-value = report **deltas** (`fedkd` vs `local` = federation gain; vs `fedavg` = teacher value), measured analysis **not pass/fail gates**. RQ1 bar = `fedkd` approaches the `central` ceiling.


## Working conventions
- When outline and a decision conflict → outline (PDF file) wins; update `DECISIONS.md` to match.
- Must follow the architecture in `paper/figures/fig_architecture_source.png`.
- Direction (RE-ALIGNED 2026-06-16 — advisor: local client teacher): federation engine = **PARAMETRIC** LLM-teacher → SLM-student KD — clients **LoRA-train** on **own private `Qᵢ`** (gold CE + local 7B teacher KD on same `Qᵢ`; `SQL-CE + λ·KL_τ(top-K) + skeleton-structure + exec-filter`), upload **LoRA deltas only**, server **FedAvg/SecureAvg → Global SLM `M_G`**. No public X pool. No ICL Hub G. Aggregation theory = **McMahan/FedProx**; **FedCoLLM [8]** = co-tuning related-work. **FedMKT [7] = logit-space KD, does NOT FedAvg weights → related-work ref.** Fed-ICL [5] answer-fusion = parameter-free **baseline** (share answers, not demos). Cross-client transfer = general SQL skill via Global SLM.
- **Models locked (2026-06-16):** teacher = **Qwen2.5-7B-Instruct** (**local HuggingFace, per client**, runs on client's own `Qᵢ`, top-K logprobs via HF generate); student = **Qwen2.5-1.5B-Instruct** (tokenizer-aligned → soft-KL KD without MinED; Phi-3/Gemma-2B/TinyLlama = `slm_swap` ablation). `L_KD = CE(reasoning⊕SQL) + λ·KL_τ(top-K teacher logprobs)` — single-phase hard+soft, **no P2/MinED**. Sequential VRAM: unload 7B teacher before loading 1.5B student.
- Build order: **parametric LoRA+FedAvg KD (= Fig.1, primary) first** — hard CE + soft-KL via local 7B logprobs, single-phase → Fed-ICL fusion as baseline.
- ICL = retrieval-only masking (Light-SQL [4]): mask only for retrieval similarity; demos shown to the model are unmasked. Never put masked SQL in the generation prompt. ICL serves RQ2, runs locally per client, pool = `Qᵢ` only. ⚠️ masking can **cost** accuracy ([4]: MQS_S 37% < QTS_S 41% EX) — frame as privacy/transfer lever, not an accuracy win.
- Privacy claim: **no raw rows / no schema / no teacher outputs leave the client; teacher runs fully on-premise; only encrypted, DP-perturbed LoRA-delta weights transmit** (Fig.1 "Weights Only"). Do NOT claim "no weights leave" — weights DO cross. Masking + DP (gradient perturbation) are the privacy mechanisms. Novelties = exec-based KD-target filtering + CoT distillation + **skeleton-token structure loss**. DP (gradient perturbation on LoRA deltas) = privacy contribution; report (ε, EX) at Stage-B.
- Data hygiene: tune only on `val` (a slice of Spider train); the `test` split (= Spider dev, since Spider test is hidden) is frozen — touch once for final numbers. Headline results need ≥3 seeds + a significance test.
- Repository, data & experiment conventions (raw/processed split, CSV processed data, per-experiment folders, results carry `model`/`time_average`/`gpu_vram`) → see `README.md`. **MANDATORY.**
- Write §3 Method + §2 Related Work in parallel while coding (no need to wait for results).
