# Fed-ICKD (repo: FedICL-SQL) — Paper Workspace

Paper project: **Fed-ICKD — Federated In-Context Knowledge Distillation for
Text-to-SQL** (working method name since the 2026-07-08 architecture pivot;
the original title was "FedICL-SQL: A Novel Federated Large-Small Language
Models Framework with In-Context Learning for NL to SQL").

**The mental model (read this first):** train a small SQL model (1.5B) across
K clients without moving private data. Clients fine-tune with plain CE + DAIL
ICL prompts; the server FedAvgs the LoRA adapters, then a frozen 7B teacher
distills the aggregated student on a **public pool P** with **reverse-KL KD**
(from [10]) every round. Pipeline = a handful of trained artifacts → eval on
Spider dev → compare arms. That's the whole project; everything else is
bookkeeping.

## Where things stand (2026-07-08)

- **Running now:** centralized KD PoC — `central_ft` vs `central_rkd` vs
  `central_kid` on identical Spider data, no federation. It picks the KD
  direction (RKD = RKL on gold / KID = RKL on imperfect ŷ) before we build
  anything federated.
- **Decided:** server-side teacher distillation (architecture per
  `paper/notes/system_architecture.md`, rewritten 2026-07-08 from `Suggest.MD`
  with one amendment: reverse KL per [10], not forward KL + relational KD);
  public pool `P` = BIRD train (2026-07-12, pool role only — BIRD is still
  not an eval benchmark; caveats + E0.1 probe gate in
  `system_architecture.md` §3.2).
- **Open:** teacher/student model pair (candidates: student Qwen2.5-1.5B-Instruct,
  teacher Qwen2.5-Coder-7B-Instruct since 2026-07-08 — every run records its
  actual ids in `metrics.json`); venue (IAJIT was the original target;
  `Suggest.MD` proposes KBS / NCA / J. Supercomputing / IEEE Access — confirm
  with advisor); **advisor sign-off on the server-side pivot** (the 2026-06-16
  client-side-teacher direction came from the advisor).

## Documents — who wins what

**Single source of truth for architecture + decisions + notation + arm naming:**
`paper/notes/system_architecture.md`. (`DECISIONS.md` was folded into it and
deleted 2026-07-08.) Read it before writing §3 or answering any architecture
question. On any mechanism dispute, it wins.

**Input documents (user-provided):**
- `paper/drafts/fedicl_sql_outline.pdf` — approved outline. Still governs paper
  *section structure*, but its mechanism text predates the 2026-07-08 pivot —
  where they conflict, `system_architecture.md` wins and the conflict gets
  flagged for advisor sign-off (do not silently follow either).
- `paper/figures/fig_architecture_source.png` + `paper/notes/fig1_architecture.md`
  — the old Fig. 1. **Stale: predates the pivot** (teacher was client-side).
  Fig. 1 must be redrawn before §3 is written. Don't modify these files; don't
  follow them either.
- `paper/templates/iajit_template.md` — journal template (only if IAJIT stays
  the target).
- `paper/references/pdf/` + `paper/references/md/` — reference papers.
  Shorthand: [4] Light-SQL · [5] Fed-ICL (answer-fusion baseline) ·
  [6] IFed-ICL · [7] FedMKT (logit-space KD, no weight FedAvg) ·
  [8] FedCoLLM (server-side co-tuning — our closest relative; differentiate on
  reverse-KL loss, ICL-consistent clients, Text-to-SQL + pool-quality analysis) ·
  [9] DAIL-SQL (the ICL selection method) · [10] KID (source of BOTH KD
  directions and the reverse-KL argument) · [11] Struct-SQL (related work only,
  CoT direction dropped).
- `Suggest.MD` — the accepted architecture proposal (07/2026). Historical input;
  the live version of it is `system_architecture.md`.

**Working documents (Claude-maintained):**
- `paper/notes/LAB_LOG.md` — session log: what happened, decisions, next steps.
  Read first each session; append after finishing. Changing a locked decision →
  update `system_architecture.md` + note it here, same session.
- `paper/notes/KD_PLAN.md` — the KD PoC plan + mechanics pinned from [10].

## Conventions

- **Arm names = feature names, never A/B/M letters:** `base` / `local` /
  `central` / `fedavg` / `fedkd` / `teacher`; PoC arms `central_ft` /
  `central_rkd` / `central_kid`. ICL is an eval overlay → suffix (`@k2`).
  Naming map + legacy aliases: `system_architecture.md` §10/§13.
- **Numbers live in run folders, not in docs:** canonical metrics =
  `fedicl-sql/experiments/*/results/<run_id>/metrics.json` (no ledger — it
  drifted and was removed 2026-07-07). Headline numbers need ≥3 seeds; the
  frozen test set (Spider dev) is touched once for final numbers.
- **Report deltas as analysis, not pass/fail gates:** `fedkd − fedavg` =
  distillation value; `fedkd` vs `central` = federation gap. Negative findings
  get reported and framed, never hidden.
- **Privacy wording:** only LoRA adapters cross the wire; teacher only ever
  touches the public pool. Do NOT claim formal DP (it's a Tier-3 optional
  add-on) and do NOT claim "no weights leave" — weights do cross.
- **Two-repo layout:** this outer repo = private paper workspace (plans, notes,
  references — reference PDFs must never be published). `fedicl-sql/` = its own
  git repo (gitignored here), the releasable code + results trail. Commit code
  progress there, plan/doc changes here. Full repo law: `CONVENTION.MD`
  (mandatory).
- Write §3 Method + §2 Related Work in parallel while experiments run — only
  hold §3's figure until Fig. 1 is redrawn.
- Keep docs plain-language and linear; track by runnable step / trained
  artifact, not by paper label. No parallel tracker files — they drift.
