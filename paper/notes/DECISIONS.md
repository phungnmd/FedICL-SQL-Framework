# FedICL-SQL — Decisions & Notation

> Slim decision record. Replaces the retired `detailed_plan.md` (deleted 2026-06-23).
> Migrated here: the locked **notation** + the locked **decisions** that are still load-bearing.
> "What to build next" is **not** pre-planned — decided per session, logged in `LAB_LOG.md`.
> Change a decision here → note it in `LAB_LOG.md` the same session.

---

## 1. Naming — arms by feature, not letters

Experiments/arms are named for **what they are**, never `A`/`B`/`Ab` letters (retired 2026-06-23).
ICL is an **eval-time overlay** (k shots), not an arm → write it as a suffix, e.g. `fedkd@k3`.

| name | what it is | role |
|---|---|---|
| `base` | untrained SLM (Qwen2.5-1.5B), no LoRA | floor |
| `local` | per-client solo LoRA on own `Qᵢ` — no federation, no teacher | federation floor (RQ1) |
| `central` | one LoRA fine-tuned on the pooled private data | centralized ceiling (the RQ1 bar) |
| `fedavg` | LoRA + FedAvg, **no** teacher KD (gold-CE only) | FL-without-our-pieces |
| `fedkd` | full method: client LoRA (gold CE + teacher soft-KL + struct + exec-filter) + FedAvg → global SLM | **FedICL-SQL** |
| `teacher` | LLM teacher (Qwen2.5-7B) few-shot, local per client | accuracy ceiling |

**RQ deltas** (reported as measured analysis, not pass/fail gates):
- `fedkd − local` = **federation gain** (RQ1)
- `fedkd − fedavg` = **teacher value** via soft-KL + CoT (RQ3) — the signal gold CE lacks
- RQ1 bar = `fedkd` approaches the `central` ceiling (small federation gap)

### Legacy alias map (old letters → feature name)

Old docs/runs used letter labels. Historical `RUNS.csv` rows + result dirs keep their old slugs (going-forward rename only). Mapping for reading them:

| old label / slug | feature name |
|---|---|
| `B0`, `base` | `base` |
| `B1`, teacher zero/few-shot | `teacher` |
| `B2`, `slm_only` | `local` |
| `B3`, `centralized_ft`, `b3_k0`, `b3_k3` | `central` |
| `B4`, Centralized-ICL | `central@k3` |
| `B6` / `Ab3`, `ab3_fedavg` | `fedavg` |
| `M_G`, `m_g` | `fedkd` |
| `B7`, Fed-ICL [5] adapted | `fedicl_baseline` (Fed-ICL answer-fusion competitor) |

Ablation letters (`Ab1`–`Ab5`) retired too → name by feature: `no_icl`, `no_fl` (= `local`), `no_teacher` (= `fedavg`), `k_sweep` (k∈{0,1,3,5}), `slm_swap` (Phi-3 / Gemma-2B / TinyLlama).

---

## 2. Notation (paper-facing — matches Fig.1, used in §3)

| Symbol | Meaning | Note |
|---|---|---|
| `K` | # clients (default 3, sweep {3,5,10}) | not `L` (retired) |
| `T` | # federated rounds (PoC 2–3) | |
| `k` | # ICL shots (∈{0,1,3,5}) | lower-case |
| `E` | local epochs / round (1–2) | |
| `λ₁…λ₄` | loss weights: SQL / KD / struct / exec | Fig.1 verbatim |
| `M_T`, `Mᵢ`, `M_G` | teacher 7B (local, per client) / client-`i` student / global SLM | |
| `Sᵢ`, `Qᵢ` | client-`i` private schema / private (NL,SQL) pairs | never leave client |
| `θ` | LoRA params | no public set, no ICL Hub |

**Research questions** (verbatim from approved outline — do not rename):
RQ1 = Federated Learning effectiveness · RQ2 = In-Context Learning effectiveness · RQ3 = Large-to-Small LM knowledge transfer & efficiency.

---

## 3. Locked decisions

1. **Primary engine** — *(locked)* parametric teacher→student KD: client LoRA (SQL-CE + soft-KL + structure loss + exec filtering) → FedAvg/FedProx → `fedkd` global SLM. Demo-level KD = variant; Fed-ICL fusion = baseline.
2. **Client count** — *(locked)* 3 default + sweep `{3,5,10}`. Cross-silo; matches Fed-ICL [5] (FedCoLLM [8] uses 4 — note the offset in §4.1).
3. **Student model** — *(locked 2026-06-12)* Qwen2.5-1.5B-Instruct (tokenizer-aligned with Qwen2.5-7B teacher → soft-KL KD without MinED). Others → `slm_swap` ablation. ⚠️ **Outline drift:** approved outline §4.1 lists Phi-3-mini / Gemma-2B / TinyLlama and omits Qwen-1.5B. Update outline §4.1 to name Qwen-1.5B as primary (others → ablation) **+ supervisor sign-off**.
4. **Second dataset** — Spider-Realistic now; BIRD only if time allows. **(confirm)**
5. **Teacher access & compute** — *(locked 2026-06-16)* Qwen2.5-7B-Instruct local HuggingFace, no API cost. Per-client offline pipeline: `fine_tune_teacher.py` (LoRA-SFT on `Qᵢ`; A100 for fp16, `--max-steps 0` to skip on T4) → `gen_teacher_targets.py` (annotate `Qᵢ`; T4 OK with `--load-in-4bit`). Student 1.5B LoRA: T4 ~11 GB. **PoC**: Mac/Colab T4, skip teacher SFT, base 7B only ($0). **Headline**: paid A100-class (Colab Pro high-RAM / RunPod / Lambda); supervisor confirms budget.
6. **ICL demo rendering** — *(locked 2026-06-20)* default `demo_style=never_schema` (question + verbatim SQL, no source DDL). `skeleton` (identifier-masked) = stronger-privacy ablation. `full` (DDL+SQL) **removed** — reintroduced schema-bleed. Builder = `fedicl_sql/prompts/builder.py`; eval default = `experiments/eval_arms/run.py`.
7. **Tracking** — *(locked 2026-06-23)* progress in `LAB_LOG.md`, canonical numbers in `experiments/RUNS.csv` via `save_results`. No A/B letters. This file = decision/notation record.

---

*Grounded in [4] Light-SQL, [5] Fed-ICL, [6] IFed-ICL, [7] FedMKT, [8] FedCoLLM + the approved outline + Fig. 1. Mechanism source of truth: `fig1_architecture.md`. Full system: `system_architecture.md`.*
