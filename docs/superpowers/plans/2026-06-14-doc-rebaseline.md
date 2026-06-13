# Doc Re-baseline (Advisor-Faithful) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Re-align the three working planning docs to the advisor's source artifacts (PDF + Fig.1), lock the six decisions from the spec, strip defensive cruft, and scrub a leaked API key — without touching the method, the split, the tests, or existing results.

**Architecture:** Pure markdown edits across `detailed_plan.md`, `todo.md`, `fedicl_sql_outline_v2.md`, `LAB_LOG.md`, plus one shell-script secret scrub. "Tests" for prose tasks are `grep` consistency checks: retired terms must be gone, locked decisions must be present and identical across docs. Code changes (soft-KL KD, DeepInfra logprobs) are a **separate Phase-2 plan** — see the final section.

**Tech Stack:** Markdown, `git`, `grep`/`rg`. No build, no runtime.

**Spec:** `docs/superpowers/specs/2026-06-14-doc-rebaseline-advisor-faithful-design.md`

**Working branch:** `docs/rebaseline-advisor-faithful` (already created; spec already committed there).

---

## Vocabulary lock (use these exact strings in all docs)

These must read identically wherever they appear. Tasks below insert/normalize to these:

- **Teacher:** `Qwen2.5-72B-Instruct (DeepInfra, OpenAI-compatible API, top_logprobs=20)`
- **Student (primary):** `Qwen2.5-1.5B-Instruct` — rationale phrase: `tokenizer-aligned with the teacher → soft-KL KD without MinED`
- **KD form:** `L_KD = CE(r̂_T⊕ŝ_T) + λ·KL_τ(top-20 teacher logprobs)`, teacher-forced, P1 (no P2/MinED split)
- **Teacher ablation name (advisor's):** `Without Teacher LLM` (NOT "make-or-break gate", NOT "kill-gate")

**Retired terms** (must NOT survive in the three working docs after this plan): `MinED`, `P2 logit-KD` (as a separate future phase), `make-or-break gate`, `kill-gate`, `Groq`, `Llama-3.3-70B` (except an optional one-line "alt-teacher sensitivity" mention).

---

## Task 1: Scrub leaked Groq API key from `teacher2.sh`

**Files:**
- Modify: `fedicl-sql/teacher2.sh`
- Modify/verify: `fedicl-sql/.gitignore` (ensure `PRIVATE.txt` and `*.key` ignored)

- [ ] **Step 1: Read the current script**

Run: `cat fedicl-sql/teacher2.sh` — confirm it contains a literal `gsk_...` key and `groq.com` base URL.

- [ ] **Step 2: Replace the script body with a DeepInfra Qwen-72B target-gen invocation reading the key from env**

Replace the entire file contents with:

```bash
# Teacher target generation — Qwen2.5-72B-Instruct via DeepInfra (logprobs-capable).
# Provider key MUST come from the environment, never hardcoded. Put it in PRIVATE.txt
# (gitignored) and `source` it, or export before running:
#   export TEACHER_API_KEY=...        # DeepInfra token
export TEACHER_BASE_URL="https://api.deepinfra.com/v1/openai"
export TEACHER_MODEL="Qwen/Qwen2.5-72B-Instruct"
export TEACHER_MAX_TOKENS=1024
export TEACHER_TOP_LOGPROBS=20
export SPLIT=data/processed/federated/3c-a1.0-s0

: "${TEACHER_API_KEY:?set TEACHER_API_KEY in env (see PRIVATE.txt) before running}"

uv run scripts/gen_teacher_targets.py --public $SPLIT/public_X.csv \
  --out $SPLIT/teacher_targets.qwen72b.csv \
  --sleep 2.0
```

> NOTE: `gen_teacher_targets.py` does not yet accept/emit `top_logprobs` — that wiring is Phase 2. This task only removes the secret and points the script at the correct provider/model.

- [ ] **Step 3: Ensure secrets are gitignored**

Confirm `fedicl-sql/.gitignore` contains `PRIVATE.txt`. If absent, append it. Run:
`grep -q '^PRIVATE.txt' fedicl-sql/.gitignore || echo 'PRIVATE.txt' >> fedicl-sql/.gitignore`

- [ ] **Step 4: Verify no key remains in tracked files**

Run: `git grep -nI 'gsk_' || echo "CLEAN"`
Expected: `CLEAN` (no matches).

- [ ] **Step 5: Commit**

```bash
git add fedicl-sql/teacher2.sh fedicl-sql/.gitignore
git commit -m "security: remove hardcoded Groq key from teacher2.sh; point at DeepInfra Qwen-72B via env"
```

- [ ] **Step 6: MANUAL (out-of-band, user action)**

Revoke the exposed Groq key (the `gsk_...` token that was in `teacher2.sh`) in the Groq console. It sat in a plaintext on-disk file and must be considered compromised. This step is not automatable; flag it to the user as required.

---

## Task 2: Re-baseline `detailed_plan.md`

**Files:**
- Modify: `paper/notes/detailed_plan.md`

- [ ] **Step 1: Read the file** so edits target current text.

- [ ] **Step 2: Teacher + Student rows (status table, ~lines 19–20)**

In the **Student `Mᵢ`** row, replace the rationale `tokenizer-aligned with the teacher → **MinED-free P2 logit-KD**` with `tokenizer-aligned with the teacher → **soft-KL KD without MinED (single-phase, no P2)**`.

In the **Teacher `M_T`** row, append after the existing DeepInfra text: `Requested with logprobs=true, top_logprobs=20 → enables soft-KL distillation (Qwen↔Qwen tokenizer aligned).`

- [ ] **Step 3: §0 SB-gate row + make-or-break arms (~lines 26, 64–66)**

Rewrite the SB-gate row so the success test is: `M_G approaches the centralized ceiling B3 (small federation gap) AND the Without-Teacher ablation quantifies teacher value` — delete the "gold-CE gate is the teacher-value test / kill" phrasing.

In the "Make-or-break arms" block, rename it `Teacher-value comparison (the Without-Teacher ablation)` and drop the `Gate:` line that reads `m_g > slm_only AND m_g > x_only AND m_g > gold_ce`. Replace with: `Report M_G vs slm_only (federation gain), vs gold_ce (teacher value), vs x_only (FedAvg-no-op diagnostic) — as analysis, not pass/fail gates.`

- [ ] **Step 4: §2.5 / §3.7 KD definition (~lines 166–178)**

Replace the line `P1 (API teacher, no logit vectors) = sequence-CE on r̂_T⊕ŝ_T; soft-logit λ·KL_τ + MinED → **P2** (needs teacher logits).` with:

`KD target = teacher reasoning⊕SQL on X. Loss = CE(r̂_T⊕ŝ_T) + λ·KL_τ(M_i ‖ teacher top-20 logprobs), teacher-forced on the aligned token sequence. DeepInfra returns top_logprobs (≤20) per token; Qwen-72B↔Qwen-1.5B share a tokenizer → no MinED, no separate P2 phase. Caveat: top-20 = truncated KL (not full vocab); cached targets store per-token top-20 logprobs.`

Delete the FedMKT/P2 sentence `**FedMKT [7]** is reserved for the P2 logit-KD/MinED refinement` → replace with `**FedMKT [7]** = logit-space KD reference (related work); our KD is sequence-level CE + truncated soft-KL.`

- [ ] **Step 5: §1.4 RQ framing (~lines 104–106) and §3.6 ablation 3/3b (~lines 277–278)**

RQ3: remove `**and does it beat free gold-label CE**` kill-framing; keep `better efficiency–performance tradeoff than LLM-only or SLM-only` and add `the Without-Teacher ablation isolates teacher value`.

Ablation 3 (Ab3a): keep the gold-CE-vs-teacher-KD comparison but delete the `this is now a **gate**` clause and the `teacher pillar dead` language. Ab3b (unlabeled-X): re-label as `secondary ablation (label-free KD regime)`, delete `the paper's "Large" pillar lives or dies on Ab3b`.

- [ ] **Step 6: §6 risk table (~line 339)**

Delete the row `Teacher adds nothing (M_G ≤ gold-CE) | kills the "Large" pillar / title`. Replace with: `Teacher value modest on labeled data | weak RQ3 | soft-KL carries info gold lacks; Without-Teacher ablation reports the delta; label-free (unlabeled-X) ablation shows the necessary-teacher regime.`

- [ ] **Step 7: Verify retired terms are gone from this file**

Run: `rg -n 'MinED|P2 logit-KD|make-or-break|kill-gate|gold-CE gate' paper/notes/detailed_plan.md || echo "CLEAN"`
Expected: `CLEAN`.

Run: `rg -n 'top_logprobs|soft-KL|Without-Teacher' paper/notes/detailed_plan.md`
Expected: present (the new locked terms).

- [ ] **Step 8: Commit**

```bash
git add paper/notes/detailed_plan.md
git commit -m "docs(plan): re-baseline to advisor-faithful — soft-KL KD via logprobs, demote gold-CE gate to Without-Teacher ablation"
```

---

## Task 3: Re-baseline `todo.md`

**Files:**
- Modify: `paper/notes/todo.md`

- [ ] **Step 1: Read the file.**

- [ ] **Step 2: Runbook teacher step (Gate block, ~lines 25–29)**

In step 5 `gen_teacher_targets.py`, change `Qwen-72B → teacher_targets.csv` to `Qwen2.5-72B (DeepInfra) → teacher_targets.qwen72b.csv with top-20 logprobs (once, cached)`.

- [ ] **Step 3: Step 9 + decision rule (~lines 33–35)**

Re-title step 9 from `⭐ p1_make_or_break` to `p1_teacher_value — eval M_G vs B2 vs gold_ce vs x_only (analysis)`. Delete the `WIN = ... AND ... AND ...` gate block and the `🔴 The M_G > gold_ce gate is the title's "Large" test` paragraph. Replace with: `Report three deltas as RQ evidence: M_G−B2 (federation gain), M_G−gold_ce (teacher value, expected positive via soft-KL), M_G−x_only (FedAvg-no-op check). Frame as measured results, not pass/fail gates.`

- [ ] **Step 4: State line + Locked-design teacher bullet (~lines 9, 61)**

In "Locked design → Teacher", change `Qwen2.5-72B-Instruct, paid API` to `Qwen2.5-72B-Instruct (DeepInfra, top_logprobs=20 → soft-KL KD)`. In "Student", change `MinED-free P2` to `soft-KL without MinED`.

- [ ] **Step 5: Pitfalls line (~line 72)**

In the Pitfalls block, delete the `Teacher-null ... if M_G ≤ gold_ce, the "Large" pillar is dead` sentence; replace with `Teacher value: on labeled Spider teacher SQL ⊆ gold, so teacher value comes from soft-KL (dark knowledge) + CoT + the label-free regime — report the Without-Teacher delta.`

- [ ] **Step 6: Verify**

Run: `rg -n 'make-or-break|MinED|gold_ce gate|pillar is dead|kill' paper/notes/todo.md || echo "CLEAN"`
Expected: `CLEAN`.

- [ ] **Step 7: Commit**

```bash
git add paper/notes/todo.md
git commit -m "docs(todo): de-gate teacher step, lock DeepInfra+logprobs teacher, soft-KL KD"
```

---

## Task 4: Re-baseline `fedicl_sql_outline_v2.md`

**Files:**
- Modify: `paper/drafts/fedicl_sql_outline_v2.md`

- [ ] **Step 1: Read the file.**

- [ ] **Step 2: Pillar-risk table (~lines 20–24)**

LLM-teacher row: change risk from `**high**` to `**medium**` and replace the "How v2 protects it" cell with: `soft-KL KD via DeepInfra top-20 logprobs (Qwen↔Qwen aligned) carries info gold lacks; Without-Teacher ablation reports the delta; label-free regime shows necessity [Δ]`.

- [ ] **Step 3: §3.4 student + §3.7 KD (~lines 67, 70–76)**

§3.4: change `tokenizer-aligned with the teacher → MinED-free P2` to `tokenizer-aligned with the teacher → soft-KL KD without MinED`.

§3.7 `L_KD` bullet: replace `P1 = seq-CE on r̂_T⊕ŝ_T, soft-logit KL+MinED → P2` with `CE(r̂_T⊕ŝ_T) + λ·KL_τ over teacher top-20 logprobs (teacher-forced, aligned tokenizer → no MinED, single-phase)`.

Delete the `⚠️ Teacher-necessity` clause's "lives or dies" framing; keep the factual note that labeled teacher SQL ⊆ gold and that value comes from soft-KL + CoT + label-free regime.

- [ ] **Step 4: Divergences list (~lines 113–123)**

Update item 2 (`RQ3 + Ablation 3 gated on gold-CE`) → `RQ3 keeps the advisor's "Without Teacher LLM" ablation (no kill-gate); soft-KL KD makes the teacher a fair, winnable comparison`. Update item 8 (`Convergence theory`) — keep. Add item: `Teacher logits available via DeepInfra → real hard+soft KD at P1; MinED/P2 retired.`

- [ ] **Step 5: Verify**

Run: `rg -n 'MinED|lives or dies|kill-gate|make-or-break' paper/drafts/fedicl_sql_outline_v2.md || echo "CLEAN"`
Expected: `CLEAN`.

- [ ] **Step 6: Commit**

```bash
git add paper/drafts/fedicl_sql_outline_v2.md
git commit -m "docs(outline-v2): downgrade teacher-pillar risk (soft-KL feasible), retire MinED/P2, relax gate to ablation"
```

---

## Task 5: Add `LAB_LOG.md` entry + de-gate scoreboard

**Files:**
- Modify: `paper/notes/LAB_LOG.md`

- [ ] **Step 1: Read the top of the file** (scoreboard + newest entry).

- [ ] **Step 2: De-gate the scoreboard decision rule (~line 49)**

Replace the `Decision rule (revised 06-13e): need m_g > slm_only AND m_g > x_only AND m_g > gold_ce ...` paragraph with: `Reporting (revised 06-14): report M_G−slm_only (federation gain), M_G−gold_ce (teacher value, expected positive via soft-KL), M_G−x_only (FedAvg-no-op check) as measured RQ evidence — not pass/fail gates. Teacher value channel = soft-KL (top-20 logprobs) + CoT, plus the label-free regime.`

- [ ] **Step 3: Prepend a new dated entry** directly under the entry-template `---` separator (newest on top, per the file's convention):

```markdown
## 2026-06-14 — advisor-faithful doc re-baseline (no code yet)

- did: brainstormed + spec'd a doc re-baseline (kept code/split/results; the method was already faithful to Fig.1). Verified DeepInfra returns top_logprobs (≤20) for Qwen2.5-72B → real hard+soft Hinton KD feasible via API with no MinED (Qwen↔Qwen aligned). Re-aligned detailed_plan/todo/outline-v2: teacher = Qwen-72B/DeepInfra+logprobs, KD = CE(CoT⊕SQL)+λ·KL_τ(top-20), demoted the gold-CE "kill-gate" to the advisor's "Without Teacher LLM" ablation, retired MinED/P2, stripped defensive cruft. Found + scrubbed a leaked Groq key in teacher2.sh.
- got: spec + plan under docs/superpowers/; three working docs re-baselined; Groq key removed from tracked files (manual revoke flagged).
- next: Phase-2 code plan — wire top_logprobs into gen_teacher_targets.py + add the λ·KL_τ soft term to the KD loss; then run the teacher-value comparison on full held-out (1034).
- Q: how much does soft-KL (dark knowledge) lift M_G over gold_ce on labeled Spider vs the label-free regime?
```

- [ ] **Step 4: Commit**

```bash
git add paper/notes/LAB_LOG.md
git commit -m "docs(lab-log): 2026-06-14 advisor-faithful re-baseline + logprobs finding; de-gate scoreboard"
```

---

## Task 6: Cross-doc consistency check

**Files:** (read-only verification across all four docs)

- [ ] **Step 1: Retired terms gone everywhere**

Run: `rg -n 'MinED|make-or-break|kill-gate|gold-CE gate|pillar is dead|Groq|Llama-3.3-70B' paper/notes/detailed_plan.md paper/notes/todo.md paper/drafts/fedicl_sql_outline_v2.md paper/notes/LAB_LOG.md || echo "CLEAN"`
Expected: `CLEAN` (or only an explicitly-labeled "alt-teacher sensitivity" Groq mention if intentionally kept).

- [ ] **Step 2: Locked terms present and consistent**

Run: `rg -n 'top_logprobs|top-20|soft-KL|DeepInfra|Without Teacher|Without-Teacher' paper/notes/detailed_plan.md paper/notes/todo.md paper/drafts/fedicl_sql_outline_v2.md`
Expected: teacher = DeepInfra Qwen-72B + top_logprobs in all three; KD = soft-KL in all three; teacher ablation named "Without Teacher". Manually confirm no contradictions (e.g., one doc still saying "no teacher logits").

- [ ] **Step 3: Confirm untouched invariants**

Run: `git status` and confirm NO changes to: `paper/notes/fig1_architecture.md`, `paper/drafts/fedicl_sql_outline.md`, `paper/drafts/fedicl_sql_outline.pdf`, anything under `fedicl-sql/fedicl_sql/`, `fedicl-sql/experiments/`, `fedicl-sql/data/`, `fedicl-sql/tests/`.
Expected: only the four docs + `teacher2.sh` + `.gitignore` + the spec/plan files appear.

- [ ] **Step 4: No commit** (verification only). If checks fail, fix in the owning task and re-run.

---

## Phase 2 — Code (SEPARATE plan, not executed here)

Per spec §5, the results-affecting code changes get their own TDD plan after the docs land. Outline only (do **not** implement from this plan):

1. **`gen_teacher_targets.py`** — accept `--top-logprobs N`; pass `logprobs=true, top_logprobs=N` to the DeepInfra chat call; persist per-token `{token, logprob, top_logprobs[]}` alongside `reasoning⊕SQL` in the cached targets. Tests: schema of the cached row; logprobs length ≤ N; token-alignment with the Qwen tokenizer.
2. **KD loss (`fedicl_sql/training/`)** — add `λ·KL_τ` over the stored top-20 teacher logprobs, teacher-forced on the target sequence; keep the existing CE(CoT⊕SQL). Tests: KL term is 0 when student==teacher dist; gradient flows; total loss = weighted sum per Fig.1.
3. **Retire MinED scaffolding** (if any exists in the lib).
4. **Run** the teacher-value comparison on **full held-out (1034)**, ≥1 seed (PoC), then ≥3 seeds at Stage-B.

When ready: invoke `superpowers:writing-plans` again with the spec §5 as input to produce the detailed Phase-2 plan.
```
