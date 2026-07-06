# KD Plan — PoC First, Full Plan Deferred

> Goal: build Fed + ICL + KD framework that maximizes EX on a *small* student
> (Qwen2.5-1.5B). Two distillation directions: KID **[10]** (arXiv:2410.11371) ·
> Struct-SQL **[11]** (arXiv:2512.17053).
> Full system: `system_architecture.md` §5.6/§5.6.1. Decision record: `DECISIONS.md`.
>
> **Rev 2026-07-07 — BIRD dropped, scope cut to a PoC.** BIRD (8.9 GB download,
> `evidence`-field dependence, dialect gap vs Spider) is out entirely — not worth it as
> KD stream or as secondary eval. **No replacement public corpus is picked yet** —
> that decision is deferred. Before spending any more build time on the full
> dual-stream federated design, run a cheap **PoC on Spider itself**: does training
> on a slice of Spider data as a KD signal (either direction) beat training on the
> exact same slice as plain gold-CE FT? Everything below Stage-0/1/2/3 from the old
> BIRD-era plan is kept only as a **deferred reference** (§Deferred) — do not build
> against it until the PoC has a verdict and a public corpus is chosen.

---

## PoC — KD vs FT on the same Spider data, base model

**Question:** for each direction (KID, Struct-SQL), does distilling from the teacher
on data slice `X` produce a better student than plain gold-CE fine-tuning on the
same `X`? This isolates the value of the KD *signal* itself, decoupled from the
public-corpus and federation questions.

**Setup:**
- Base model: `Qwen2.5-1.5B-Instruct` (untrained, no existing adapter — start fresh
  each arm, not from `central`/`fedavg`).
- Data slice `X`: a subsample of `processed_data/SPIDER/centralized/train.csv`
  (reuse existing Spider processed data — no new corpus, no new download).
- Eval: frozen `processed_data/SPIDER/centralized/test.csv` (Spider dev), `k=0` (no
  ICL — isolates the training signal, not retrieval).

**Arms (all trained from base, on the identical `X`):**

| ID | arm | what it is | teacher active | HW |
|---|---|---|---|---|
| P0 | `poc_ft` | gold-CE SFT on `X` (no teacher) — the floor | no | T4 |
| P1 | `poc_struct` | SFT on teacher `QP-CoT ⊕ SQL` for `X` (Struct-SQL [11]) | offline, before training | T4 |
| P2 | `poc_kid` | `RKL(q‖p)` on teacher-scored imperfect `ŷ` for `X` (KID [10]) | online, co-loaded | A100 — **blocked**, see E0.3 below |

**Read-off:** `poc_struct − poc_ft` = Struct-SQL's KD-vs-FT value. `poc_kid − poc_ft`
= KID's KD-vs-FT value. `poc_kid − poc_struct` = which direction wins (secondary —
not the PoC's primary question).

**Decision gate:** if neither KD arm beats `poc_ft` by a real margin, the KD signal
itself doesn't earn its build cost — rethink before investing in the full dual-stream
federated design. If one or both do, that direction becomes the candidate for the
full method once a public corpus is picked (§Deferred).

### E0.3 — pin KID [10] mask-fill mechanics (reading task, no code) — blocks `poc_kid`

A causal LM has no `[MASK]` token, so "mask ρ% of gold tokens → 1 forward fill → ŷ"
needs a concrete recipe before `mask_rewrite`/`rkl_div_loss` can be built. Read
`paper/references/md/[10]-...KID....md` and confirm before starting `poc_kid`:

- [ ] Left-to-right teacher-forced fill, or iterative resample-and-refeed?
- [ ] Sampling temperature / top-p for the fill step?
- [ ] Stop-gradient through `ŷ` generation (no backprop through the sampling step)?
- [ ] Masking ratio `ρ` default before the Stage-later sweep (start at one fixed value)?

`poc_struct` does not need this — it's a straightforward SFT on offline-cached
teacher traces, no masking involved.

### Build needed for the PoC

| Component | File | State |
|---|---|---|
| Top-K soft-KL (forward) | `losses.py` `kl_div_loss` | done |
| Weighted CE + skeleton weight | `losses.py` `weighted_lm_loss` | done |
| LoRA trainer + KD config | `training/lora_trainer.py` | done |
| Teacher generate (local HF) | `models/teacher_local.py` | done |
| Offline teacher-target pipeline | `data/teacher_targets.py` | done — point `--private` at the Spider slice |
| `--kd-direction {struct,gold,none}` on `experiments/client_train/run.py` | trainer + CLI | done (generic `--kd-train`/`--kd-teacher-targets`, no BIRD-specific naming) |
| `mask_rewrite` + `rkl_div_loss` (KID) | student / losses / trainer | not built — blocked by E0.3 |

### Running the PoC (CLI)

```bash
# 1. Carve a slice X out of Spider centralized train (any reasonable subsample; keep
#    it fixed across P0/P1/P2 so the comparison is apples-to-apples)
uv run python -c "
from fedicl_sql.data.spider import load_csv, examples_to_csv
import random
rows = load_csv('processed_data/SPIDER/centralized/train.csv')
random.Random(0).shuffle(rows)
examples_to_csv(rows[:1000], 'artifacts/kd_poc/slice_x.csv')
"

# 2. P0 — poc_ft: plain gold-CE SFT on X, from base
uv run python experiments/client_train/run.py \
    --client artifacts/kd_poc/slice_x.csv \
    --kd-label none \
    --out artifacts/kd_poc/poc_ft/adapter \
    --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0

# 3. Generate teacher QP-CoT targets for X (once, offline)
uv run python scripts/gen_teacher_targets.py \
    --private artifacts/kd_poc/slice_x.csv \
    --out artifacts/kd_poc/slice_x_qpcot_targets.csv \
    --teacher-model Qwen/Qwen2.5-7B-Instruct --mode qp_cot --teacher-k 3

# 4. P1 — poc_struct: SFT on teacher QP-CoT ⊕ SQL for X, from base
uv run python experiments/client_train/run.py \
    --client artifacts/kd_poc/slice_x.csv \
    --kd-direction struct --kd-train artifacts/kd_poc/slice_x.csv \
    --kd-teacher-targets artifacts/kd_poc/slice_x_qpcot_targets.csv \
    --out artifacts/kd_poc/poc_struct/adapter \
    --batch-size 1 --grad-accum 16 --save-steps 200 --seed 0

# 5. P2 — poc_kid: blocked until E0.3 is pinned and mask_rewrite/rkl_div_loss exist

# 6. Eval P0/P1 on frozen Spider test, k=0
uv run python experiments/eval_arms/run.py --pool-mode centralized \
    --test-csv processed_data/SPIDER/centralized/test.csv \
    --k 0 --batch-size 16 --retrieval question --seed 0 \
    --resume-dir artifacts/kd_poc/eval_ckpt \
    --arms poc_ft=artifacts/kd_poc/poc_ft/adapter poc_struct=artifacts/kd_poc/poc_struct/adapter
```

Pull EX from `experiments/RUNS.csv` / `predictions/{poc_ft,poc_struct}.csv` and fill
in the read-off above.

---

## Deferred — full staged plan (BIRD-era, kept for reference only)

Everything below described the pre-2026-07-07 plan built around BIRD as the public
KD corpus: a locked control ladder (`fedavg → fedavg_bird → fedkd_seqkd →
fedkd_struct → fedkd`), demo-style parity, sequential Step-1(KD-pretrain on
BIRD)/Step-2(FT on `Qᵢ`) training, and a 4-stage experiment ladder (probes →
single-client bake-off → federate winner → seeds/ablations). **None of that is
built or run against right now.** Once the PoC above has a verdict and a public
corpus is chosen (or the decision is made to skip a public corpus and reuse the
private pool itself for Stream 2), re-derive the staged plan against that corpus
rather than resurrecting the BIRD-specific numbers — the mechanism (dual-stream,
sequential training, control ladder) still applies, only the corpus name changes.

Design invariants that carry forward regardless of corpus:
1. **KD data = public and equal for every direction being compared** (whatever
   corpus is chosen) — keeps `kid − struct` free of a data confound.
2. **Control ladder, one ingredient per rung**: floor → data-matched gold-CE control
   → teacher-SQL-only → teacher-structured-reasoning → teacher-logit-level. Teacher
   value = last rung minus the data-matched control, never minus the bare floor.
3. **Demo-style parity**: train `demo_style` == eval `demo_style` within any arm.
4. **Weighted FedAvg** (`nᵢ/n`, McMahan), not `1/K`.
5. **Sequential two-step local training** (KD-pretrain to completion, then FT,
   LoRA-init from the KD-pretrain checkpoint) — not a combined per-step loss.

Risks noted at the time, still relevant once this resumes: QP-CoT may not help a
1.5B student ([11] used 4B); `+ICL` training-time context may not fit a 16 GB card
(needs a VRAM probe before committing to `train-k=3` arms); KID mask-fill mechanics
must be pinned (E0.3) before `mask_rewrite`/`rkl_div_loss` exist; a sequential
KD-pretrain→FT design risks the FT step partially overwriting what KD-pretrain
taught (no rehearsal) — measure before assuming either way.
