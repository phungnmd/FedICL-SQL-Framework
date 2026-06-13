# Lab Log — FedICL-SQL

Where I actually work. **Append newest entry on top.** Plain words, not paper labels — write *what I did → what I got → what's next → open questions*. 4 lines/session is enough. Read the top entry to know where you are; never re-parse the plan.

- Numbers (EX/EM/loss/VRAM) live in `fedicl-sql/experiments/RUNS.csv` (auto) — here just note the headline + the *story* (why it moved, what broke).
- Stuck/risk → also check `problems_and_solutions.md`. Daily checklist → `todo.md` ▶️ Runbook.

Entry template:

```markdown
## YYYY-MM-DD
- did:
- got:
- next:
- Q:
```

---

## 📊 Scoreboard (glance) — split `3c-a1.0-s0`, n=200, seed 0, poc

Headline EX. Raw rows: `fedicl-sql/experiments/RUNS.csv`. Keep this table updated as arms land.

**Matched pair — held_out[:200], k=0, cuda (apples-to-apples):**

| arm | what | EX | EM | status |
|---|---|---|---|---|
| `p0_base_holdout` | base Qwen, **no training** (floor) | **40.5%** | 8.5% | ✅ cuda |
| `b3_centralized_ft` | trained, **all data pooled** (ceiling) | **49.5%** | 33.0% | ✅ cuda |

**Training gain: +9.0 EX** (40.5 → 49.5, same cuda stack). Beats old_train adapter (47.5%).

**Reference floors (different eval/setting):**

| arm | what | EX | note |
|---|---|---|---|
| `p0_eval50` | base + 3-shot ICL, Spider dev | 44.5% | mps, k=3 |
| old_train (external) | full-Spider LoRA, chat-template | 47.5% | T4, dev[:200] |

**Federation arms (RQ1 ⭐ make-or-break) — PENDING:**

| arm | what | EX | status |
|---|---|---|---|
| `slm_only` ×3 | each client alone, own data | — | ⏳ next ($0) |
| `gold_ce` | FedAvg gold deltas → M_G | — | ⏳ next ($0) |
| `m_g` | FedAvg teacher-KD deltas → M_G (**method**) | — | ⏳ needs teacher targets |
| `x_only` | public X only (FedAvg no-op check) | — | ⏳ needs teacher targets |

Decision rule: need `m_g` > `slm_only` AND `m_g` > `x_only`; watch `m_g` vs `gold_ce` (Ab3).

---

## 2026-06-13 (d) — base floor re-run on cuda (matched pair)

- did: re-ran `p0_base_holdout` via bootstrap §2.5 on Colab T4 (was mps) so base + B3 share one stack.
- got: base **EX 40.5%** (cuda) vs B3 **49.5%** (cuda) → clean +9.0 training gain, same hardware. Scoreboard above now pinned.
- next: $0 no-teacher federation arms (`slm_only`×3 + `gold_ce`) on Colab.
- Q: federation cost — how far does FedAvg(gold) trail the 49.5% pooled ceiling?

## 2026-06-13 (c) — B3 trained: 49.5%, fix fully validated

- did: full B3 centralized-FT on Colab T4 (after fixing a CPU→GPU runtime trap — `device:cpu` had it crawling): train 5744 pooled-private, 1 epoch, eval held_out[:200].
- got: **B3 EX=49.5% (99/200)**, EM=33.0%, eval 1.26s/q. Trained went **25.5%→49.5%** — the recipe fix (chat-template + cosine + batch-16) validated end-to-end; **beats old_train adapter (47.5%)** and clears the 40% base floor by +9.5. (B3 fixed §6 push cell typo: escaped quote `retry\"`.)
- next: no-teacher federation baselines (`slm_only`×3 + `gold_ce` FedAvg) vs this 49.5% ceiling; teacher groq shards (2 keys) → merge → ⭐ make-or-break.
- Q: how far does FedAvg(gold) trail centralized B3? (= the federation cost, RQ1).

## 2026-06-13 (b) — base floor verifies the fix

- did: ran `p0_base_holdout` (base Qwen2.5-1.5B, no adapter, held_out[:200], k=0) on Mac MPS to verify the chat-template fix on real data.
- got: **EX 40.0% (80/200)**, EM 8.5%, 1.41s/q — up from the broken **0%**, and above old_train's base (35.5%). Fix confirmed end-to-end (eval path). RUNS row `p0_base_holdout__poc__s0` (device=mps, stage=poc).
- next: **B3 centralized-FT train+eval** — the trained ceiling over this 40% floor; the real test of the *training* recipe (template+cosine+batch16: was 25.5%, target ~45–47%). Run on Colab GPU. Teacher groq shards filling in parallel (2 keys).
- Q: does B3 trained clear old_train parity (~47%) over the 40% base, or does the data gap (5744 vs 8659) cap it?

## 2026-06-13

- did: chased the trained-arm collapse. Base Qwen2.5-1.5B EX=**0%** on 200 held-out vs old_train base **35.5%** → engine fed the raw `### …` prompt straight to an **Instruct** model with **no chat template** (train + eval both). Patched the engine: route every prompt through the model's own chat template (`apply_chat_template`, system folded into the user turn → portable Qwen/Phi/Llama/Gemma) in `student.generate` + `dataset._assemble`; also added cosine LR + 3% warmup and bumped effective batch 8→16 in `lora_trainer` to match the old_train recipe. `builder.py` unchanged (its text is now the user-turn *content*, not a raw prompt).
- got: 81 tests green; chat-template assemble verified on the real Qwen tokenizer (prompt masked 93 tok, target=`SELECT count(*) FROM singer<|im_end|>` incl. stop token, skeleton up-weight intact). No metric run yet — code fix only.
- next: re-pull on Colab (§1 `reset --hard`), rerun p0_eval50 / B3 eval → expect base **0%→~35%**; then B3 train → target **~45–47%** (template + cosine + batch-16).
- Q: does cosine+batch-16 close the trained gap to old's 47.5%, or is the remainder just data (B3 pools 5744 vs old_train's full 8659)?

## 2026-06-12

- did: reran `p0_eval50` at `--n 200 --k 3 --stage poc --seed 0` on Mac MPS after the fd-leak fix.
- got: base Qwen2.5-1.5B + ICL floor = **EX 44.5% (89/200), EM 26.5% (53/200)**; `time_average=7.3981s/q`, `gpu_vram=5059.8MB`; run logged in `experiments/RUNS.csv` as `p0_eval50__poc__s0__20260612T051000`.
- next: stop spending on P0; run no-teacher training baselines next: **B3 centralized-FT** then **B2 SLM-only ×3** on split `3c-a1.0-s0`.
- Q: p0_eval50 is only a sanity/base floor; final ICL evidence should use the federated/public-X demo setting, not rely on centralized fallback demo logic.

## 2026-06-12

- did: set up tracking — LAB_LOG (this file) + ▶️ Runbook on top of todo.md, slimmed todo 242→~80 lines (cut P-1…P6 sprawl that duplicated detailed_plan), `device` col + cost tally into RUNS.csv/REGISTRY, codified 3-layer doc system in CONVENTION §5. Confirmed Mac M4 Pro 24GB trains the 1.5B student fp16 → all `$0` baselines run local.
- got: pipeline + 81 tests green · `p0_sanity` PASS on Qwen-1.5B · training resumable. Runbook step 1 done; **no metric-producing run yet**.
- next: runbook **step 2 `p0_eval50 --n 200 --k 3`** = first real number (base+ICL floor on Spider dev).
- Q: what EX does Qwen-1.5B+ICL hit on Spider dev? (the floor everything beats)
- bug+fix: p0_eval50 crashed mid-run — `unable to open database file` / `Too many open files`. Cause: `with sqlite3.connect()` manages a *transaction*, not the connection → never closes fd. Leaked 3 fds/query (`db_to_ddl` + `score_ex`×2) → hit the 256 open-file limit ~q85. Fixed both → explicit `conn.close()` in `finally`; verified fd-flat over 400 calls. Rerunning step 2.
