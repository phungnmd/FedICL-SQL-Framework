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
