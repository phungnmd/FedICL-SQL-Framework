# KD Plan — Two Directions from [10]: RKD and KID

> Goal: build Fed + ICL + KD framework that maximizes EX on a *small* student
> (Qwen2.5-1.5B). Both distillation directions come from **[10] KID** (Zhong et al.
> 2024, arXiv:2410.11371): **RKD** (Reverse KL on gold data) and **KID** (Reverse KL
> on imperfect data). Full system + decision record: `system_architecture.md`
> (§8 KD directions; `DECISIONS.md` folded in and deleted 2026-07-08).
>
> **Rev 2026-07-07 (2) — CoT direction dropped.** The Struct-SQL [11] QP-CoT
> direction (`poc_struct`, offline teacher traces, `gen_teacher_targets.py` pipeline)
> is **removed entirely**. Both remaining directions are online logit-level KD from
> [10]: teacher + student co-loaded, one teacher forward per step, no offline target
> generation, no CoT targets. Earlier the same day: BIRD dropped, scope cut to a
> Spider PoC (unchanged — still the active scope).

---

## The two directions (from [10], Table 1 + §3)

Both use **Reverse KL** — `RKL(q‖p) = Σ q·log(q/p)`, mode-seeking, better than
forward KL for SQL's precise low-diversity tokens ([10] Table 2: RKD 60.1–62.7 vs
FKD ~57.3 EX). Both add the **auxiliary MLE (gold-CE) loss** — [10] found it
important for stable training. Both need teacher + student **co-loaded** (one
teacher forward per step, no decoding).

| | **RKD** | **KID** |
|---|---|---|
| KD target sequence | gold SQL `y` | imperfect `ŷ` (student rewrite of masked `y`) |
| Loss | `CE(y) + RKL(q‖p)` on `y` | `CE(y) + RKL(q‖p)` on `ŷ` |
| Extra machinery | none | mask → one-pass fill → rewrite (§mechanics) |
| [10] gains vs SFT | +1.89 … +3.14 avg | +3.17 … +5.83 avg (best trade-off) |
| Training latency vs SFT | ~2.0× | ~2.0–2.4× |

RKD is a strict subset of KID (drop the imperfect-data step) → one trainer serves
both, and `kid − rkd` cleanly isolates the value of imperfect data.

## KID mechanics — pinned from [10] (closes old E0.3)

The old E0.3 blocker ("mask-fill mechanics unclear") is resolved by the paper:

1. **Masking** — sample `ρ` fraction of the **gold SQL tokens** and replace with a
   mask token (paper uses `<s>`; any reserved token works — it's just a corrupted
   input for one forward pass, not a trained `[MASK]` embedding). Strategy =
   **Random** (paper default; entropy-based Easy/Hard are unstable). Ratio
   **ρ = 0.2** default (0.1–0.3 all safe; 0.5 degrades).
2. **Predicting** — feed the masked sequence through the **student in ONE
   teacher-forced forward pass** (not autoregressive, not iterative), take the
   student's prediction at each masked position. `no_grad` — ŷ is data, no backprop
   through the fill. Fill = greedy argmax (paper doesn't specify a temperature;
   greedy is our default, note as our choice).
3. **Rewriting** — splice the predicted tokens into the gold sequence at the masked
   positions → `ŷ`. (Rewriting beats leaving raw mask tokens by +3.3 EX in [10]
   Table 5 — do not skip this step.)

Then teacher forward on `ŷ` → `p`, student forward on `ŷ` → `q`,
`L = CE(gold y) + RKL(q‖p)`.

---

## PoC — KD vs FT on the same Spider data, base model

**Question:** does distilling from the teacher on data `X` (either direction) beat
plain gold-CE fine-tuning on the exact same `X`? Isolates the KD *signal* itself,
decoupled from the public-corpus and federation questions.

**Setup:**

- Base model: `Qwen2.5-1.5B-Instruct` (fresh each arm, no existing adapter).
- Teacher: `Qwen2.5-7B-Instruct`, frozen, co-loaded (4-bit on 16 GB cards).
- Data `X` = full `processed_data/SPIDER/centralized/train.csv` (8659 rows, as-is).
- Eval: frozen `processed_data/SPIDER/centralized/test.csv` (Spider dev), `k=0`.

**Arms (all trained from base, on the identical `X`):**

| ID | arm | loss | teacher |
|---|---|---|---|
| P0 | `central_ft` | gold CE only — the floor | no |
| P1 | `central_rkd` | `CE + RKL(q‖p)` on gold `y` | co-loaded, 1 forward/step |
| P2 | `central_kid` | `CE + RKL(q‖p)` on imperfect `ŷ` (ρ=0.2, Random) | co-loaded, 1 forward/step |

**Read-off (each rung adds one ingredient):**

- `central_rkd − central_ft` = value of teacher logits (RKL) on gold data
- `central_kid − central_rkd` = value of imperfect data on top
- `central_kid − central_ft` = full KID value

**Decision gate:** if neither KD arm beats `central_ft` by a real margin, the KD signal
doesn't earn its build cost — rethink before investing in the full federated design.
If one or both do, that direction goes into the full method once a public corpus is
picked (§Deferred).

---

## Implementation plan

Existing code that carries over: `LoraTrainConfig` / `train_from_examples` loop +
checkpointing (`lora_trainer.py`), `LocalHFTeacher` (`models/teacher_local.py`),
`weighted_lm_loss` (`losses.py`), eval stack. The offline Struct-SQL pipeline is
retired (step 0).

**0. Retire the CoT/offline-target path** — delete `scripts/gen_teacher_targets.py`,
`fedicl_sql/data/teacher_targets.py`, the `--kd-train`/`--kd-teacher-targets`/
`--kd-direction struct` plumbing and `train_dual_stream` in `lora_trainer.py`
(+ their tests). No legacy shims.

**1. `rkl_div_loss` in `losses.py`** — full-vocab reverse KL
`Σ softmax(q)·(log_softmax(q) − log_softmax(p))` over answer-token positions only
(prompt masked out), mean over tokens. Teacher is co-loaded → full logits available,
no top-K caching needed. Optional temperature `τ` (default 1.0). Unit test against a
hand-computed small tensor + `RKL(p‖p) = 0`.

**2. `mask_rewrite` (new `fedicl_sql/training/imperfect.py`)** — input: tokenized
prompt+gold, gold-span indices, `ρ`; random-mask ρ of gold positions → one student
forward under `no_grad` → argmax at masked positions → return rewritten ids `ŷ`.
Unit test: ρ=0 returns gold unchanged; masked positions differ only where sampled.

**3. Teacher scoring forward** — add `score_logits(input_ids) -> logits` to
`LocalHFTeacher` (plain forward, `no_grad`, no generate). Supports 4-bit load for
16 GB cards.

**4. Online KD trainer** — extend the `train_from_examples` step: per batch build
prompt (k=0 for PoC), if `kid` run `mask_rewrite` to get target sequence (else gold),
teacher forward → `p`, student forward → `q`,
`loss = lambda_ft·CE(gold) + lambda_kd·rkl_div_loss(q, p)` (defaults 1.0/1.0, CLI
`--lambda-ft/--lambda-kd` already exist). Teacher stays loaded the whole run
(sequential-VRAM unload rule doesn't apply — co-load is the design).

**5. CLI** — `experiments/client_train/run.py`: `--kd-direction {none,rkd,kid}`
(replaces `{struct,gold,none}`), `--mask-ratio 0.2`, `--teacher-model`,
`--teacher-4bit`. Each run's `metrics.json` records `teacher_model` as always (no ledger).

**6. Run the PoC** (order: P0 → P1 → P2; P2 only differs from P1 by `--kd-direction`):

```bash
# P0 — central_ft
uv run python experiments/client_train/run.py \
    --client processed_data/SPIDER/centralized/train.csv \
    --kd-direction none \
    --out artifacts/kd_poc/central_ft/adapter \
    --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0

# P1 — central_rkd  (add teacher, RKL on gold)
uv run python experiments/client_train/run.py \
    --client processed_data/SPIDER/centralized/train.csv \
    --kd-direction rkd --teacher-model Qwen/Qwen2.5-7B-Instruct --teacher-4bit \
    --out artifacts/kd_poc/central_rkd/adapter \
    --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0

# P2 — central_kid  (same + imperfect data)
uv run python experiments/client_train/run.py \
    --client processed_data/SPIDER/centralized/train.csv \
    --kd-direction kid --mask-ratio 0.2 \
    --teacher-model Qwen/Qwen2.5-7B-Instruct --teacher-4bit \
    --out artifacts/kd_poc/central_kid/adapter \
    --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0

# Eval all three on frozen Spider test, k=0
uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --test-csv processed_data/SPIDER/centralized/test.csv \
    --k 0 --batch-size 16 --retrieval question --seed 0 \
    --resume-dir artifacts/kd_poc/eval_ckpt \
    --arms central_ft=artifacts/kd_poc/central_ft/adapter \
           central_rkd=artifacts/kd_poc/central_rkd/adapter \
           central_kid=artifacts/kd_poc/central_kid/adapter
```

Pull EX with `uv run python analysis/compare.py` (scans result folders directly,
no ledger) or read `predictions/{central_ft,central_rkd,central_kid}.csv` directly.

**VRAM:** teacher 4-bit (~5–6 GB) + student fp16 (~3 GB) + activations fits the
16 GB A5000/T4 profile (`--batch-size 1 --grad-accum 16`); fp16 teacher co-load
(~17 GB) needs A100. Both directions cost the same — RKD and KID differ only by one
extra student `no_grad` forward (the fill).

---

## Deferred — full staged plan (kept for reference only)

The full federated design (dual data streams, sequential Step-1 KD-pretrain on a
public corpus → Step-2 FT on `Qᵢ`, control ladder, 4-stage experiment ladder) is
deferred. Status 2026-07-12: **both former blockers are resolved** — the PoC has
its verdict (RKD provisional winner, LAB_LOG 2026-07-11 (2)) and the public KD
corpus is decided (`P` = BIRD train, `system_architecture.md` §3.2 — with the
mandatory E0.1 transfer probe before any distill build). Note the architecture
has ALSO changed since this section was written (server-side distill per the
2026-07-08 pivot — no sequential two-step design, no client-side teacher);
re-derive the staged plan from `system_architecture.md` + `fed_ickd_v2_proposal.md`,
not from the 4-stage ladder below. Design invariants that carry forward:

1. **KD data = public and equal for every direction compared** — keeps `kid − rkd`
   free of a data confound.
2. **Control ladder, one ingredient per rung**: floor → data-matched gold-CE control
   (`fedavg_pub`) → teacher-logit on gold (`fedkd_rkd`) → teacher-logit on imperfect
   data (`fedkd` = KID). Teacher value = KD rung minus the data-matched control,
   never minus the bare floor.
3. **Demo-style parity**: train `demo_style` == eval `demo_style` within any arm.
4. **Weighted FedAvg** (`nᵢ/n`, McMahan), not `1/K`.
5. **Sequential two-step local training** (KD-pretrain to completion, then FT,
   LoRA-init from the KD-pretrain checkpoint) — not a combined cross-dataset loss.
   (Within the KD step itself, `CE + RKL` on the same data is [10]'s recipe and stays.)

Open risks once this resumes: FT (Step 2) may partially overwrite what KD-pretrain
taught (no rehearsal) — measure, don't assume; `train-k=3` context may not fit a
16 GB card (VRAM probe before committing); MLE/RKL weighting under-explored per [10]
— default 1:1, sweep only if the PoC signal is positive.
