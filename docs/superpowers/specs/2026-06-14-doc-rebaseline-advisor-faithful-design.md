# Design — Doc Re-baseline to Advisor-Faithful Spec

**Date:** 2026-06-14
**Topic:** Re-align FedICL-SQL planning docs to the advisor's source artifacts (outline PDF + Fig.1), lock the model/teacher/KD decisions, strip accumulated defensive cruft. **Code, data splits, tests, and existing results are kept** — this is a documentation + decision re-baseline, not a project reset.

---

## 1. Context & motivation

A review compared the working docs (`detailed_plan.md`, `todo.md`, `fedicl_sql_outline_v2.md`) against the advisor's two source-of-truth artifacts: `paper/drafts/fedicl_sql_outline.pdf` and `paper/figures/fig_architecture_source.png` (transcribed in `paper/notes/fig1_architecture.md`).

**Finding: the method/mechanism never drifted.** The implemented engine (client 4-loss `L = λ₁L_SQL + λ₂L_KD + λ₃L_struct + λ₄L_exec` → upload weights only → FedAvg → Global SLM `M_G`; teacher feeds both the ICL Hub and the KD targets) is faithful to Fig.1.

What *did* accumulate:
- A `Qwen2.5-1.5B` student choice not literally listed in the PDF (PDF says "e.g., Phi-3 Mini, Gemma 2B, TinyLlama,…").
- A teacher-KD setup that diverged from Fig.1's intent: the active script (`fedicl-sql/teacher2.sh`) used **Groq Llama-3.3-70B** (tokenizer-mismatched with the Qwen student), and the KD term had degraded to text-only SFT (no soft-logit), because an API teacher was assumed to expose no logits.
- A self-imposed "gold-CE kill-gate" + heavy `⚠️` defensive framing that is stricter than the advisor's open RQ wording and reads as project drift.

The advisor has **not** raised any of these; the cleanup is proactive (inferred from PDF + Fig.1), not a response to advisor feedback.

**Key enabling fact (verified 2026-06-14):** DeepInfra's OpenAI-compatible API returns `logprobs` + `top_logprobs` (1–20 alternatives per token) for **Qwen2.5-72B-Instruct** ([docs.deepinfra.com/chat/log-probs](https://docs.deepinfra.com/chat/log-probs)). With a Qwen-72B teacher and a Qwen-1.5B student sharing one tokenizer, real soft-KL (Hinton) KD is feasible *via API* with no MinED and no self-hosting. This rescues the teacher pillar rather than merely picking a teacher.

## 2. Goal & non-goals

**Goal:** planning docs that (a) state the method exactly per Fig.1, (b) lock the six decisions below with rationale, (c) drop defensive cruft while keeping genuine rigor, and (d) carry a short advisor sign-off list.

**Non-goals (explicitly NOT touched):**
- The method/mechanism (faithful — unchanged).
- `fig1_architecture.md` (canonical transcription — unchanged).
- The schema-disjoint 3-pool split, the data pipeline, the 81 tests.
- Existing results (base EX=40.5%, B3 centralized-FT EX=49.5%, the matched cuda pair).
- The approved `fedicl_sql_outline.pdf` / `.md` (never edited).

## 3. Locked decisions

1. **Method/mechanism — unchanged.** Faithful to Fig.1. Client 4-loss → FedAvg → `M_G`; teacher authors ICL Hub demos + KD targets on public `X` only.

2. **Student — Qwen2.5-1.5B-Instruct = primary.** Rationale: tokenizer-aligned with the Qwen2.5-72B teacher → enables soft-KL KD without MinED. Phi-3-mini / Gemma-2B / TinyLlama → SLM-architecture ablation (the PDF's "Different SLM Architectures"). Adds Qwen to the PDF's "e.g." list → advisor sign-off line.

3. **Teacher — Qwen2.5-72B-Instruct via DeepInfra**, requested with `logprobs=true, top_logprobs=20`. Drop the Groq/Llama-3.3-70B teacher (tokenizer-mismatched). Groq may remain at most as an optional alt-teacher sensitivity data point, never the primary.

4. **KD form — real hard+soft Hinton KD at P1.**
   `L_KD = CE(M_i(x), r̂_T ⊕ ŝ_T) + λ·KL_τ( M_i(x) ‖ teacher_top20(x) )`
   teacher-forced on the teacher's target sequence, tokenizer-aligned (Qwen↔Qwen). Soft term uses the top-20 truncated teacher distribution per token (documented approximation). MinED dropped (aligned tokenizer). P2 logit-KD collapses into P1; the old P2 distinction is retired.
   - Honest caveats recorded in §3.7: top-20 = truncated KL (not full-vocab); cached targets store per-token top-20 logprobs (~20 floats/token, larger cache); requesting logprobs adds negligible generation cost.

5. **Gates / RQ framing — relaxed to advisor's spec.** The "gold-CE kill-gate" is demoted to the PDF's existing **"Without Teacher LLM"** ablation (a fair test the teacher can now win, since soft-KL carries information gold labels do not). RQ3 returns to the advisor's open wording. The unlabeled-X arm (Ab3b) is kept as a *secondary* ablation, not a make-or-break gate.

6. **Strip defensive cruft.** From `detailed_plan.md`, `todo.md`, `fedicl_sql_outline_v2.md`: remove attempt-1 archaeology, the `⚠️` warning thicket, and the make-or-break-gate framing. **Keep** the real rigor: schema-disjoint split, ≥3 seeds + significance, RUNS.csv provenance, one-stack-per-comparison rule, eval-provenance disclosure.

## 4. What changes, per artifact

- **`detailed_plan.md`** — status table + §0 notation: teacher row → Qwen-72B/DeepInfra+logprobs; KD section §2.5/§3.7 → hard+soft form, MinED/P2 retired; remove gate framing in §0/§3.6/§6; student rationale updated. Keep §3.1 data pipeline, §7 repo layout, tiering.
- **`todo.md`** — Runbook: teacher step → DeepInfra Qwen-72B + store top_logprobs; step 9 "make-or-break gate" → reframed as the Without-Teacher ablation + the three honest comparisons (no kill language); scoreboard decision rule de-gated.
- **`fedicl_sql_outline_v2.md`** — pillar-risk table: teacher pillar risk downgraded (soft-KL feasible); divergences list updated (teacher logits resolved, gate relaxed, student justified). Keep `[Δ]` tagging convention.
- **`LAB_LOG.md`** — one new top entry recording this re-baseline + the logprobs finding.
- **`fig1_architecture.md`** — unchanged.

## 5. Code touch-list (minimal — separate plan)

Decisions that imply code (scoped, executed via the implementation plan, not now):
- `gen_teacher_targets.py` → point at DeepInfra Qwen-72B; request + persist `top_logprobs=20` per token in the cached targets CSV/JSON.
- KD loss in `fedicl_sql/training/` → add the `λ·KL_τ` soft term over the stored top-20 teacher logprobs (teacher-forced); keep the CE(CoT⊕SQL) term.
- Retire Groq/Llama path in `teacher2.sh` (and any MinED scaffolding).
- No changes to split builders, retrieval, eval, or the FedAvg loop.

## 6. Security

`fedicl-sql/teacher2.sh` contains a live Groq API key in plaintext. **Revoke that key**, and keep all provider keys out of committed files (env vars / gitignored `PRIVATE.txt`). Independent of the docs work; do it regardless.

## 7. Advisor sign-off list (carry into next meeting)

1. Primary student = Qwen2.5-1.5B (added to the PDF's "e.g." list) — tokenizer-aligned with the teacher for clean soft-KL KD.
2. Teacher = Qwen2.5-72B/DeepInfra with logprobs → real hard+soft KD (faithful to Fig.1).
3. RQ3 + "Without Teacher LLM" kept as the advisor's ablation (no kill-gate).
4. Second benchmark: Spider-Realistic now; BIRD recommended over it if Spider contamination caps headroom.

## 8. Success criteria

- The three working docs read as a clean, advisor-faithful plan: method = Fig.1, decisions locked with rationale, no kill-gate framing, rigor retained.
- Teacher/KD/student decisions are internally consistent (Qwen↔Qwen tokenizer → soft-KL → top-20 logprobs) across all three docs and §0 notation.
- Code touch-list + advisor sign-off list are explicit so nothing silently drifts again.
- Zero edits to the mechanism, the split, the results, or the approved PDF.
