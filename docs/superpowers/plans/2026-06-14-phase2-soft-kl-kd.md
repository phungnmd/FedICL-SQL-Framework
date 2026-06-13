# Phase 2 — Soft-KL KD via Teacher Logprobs Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make the KD loss a real hard+soft Hinton term — `L_KD = CE(teacher completion) + λ·KL_τ(student ‖ teacher top-20)` — by capturing per-token top-20 logprobs from the DeepInfra Qwen-72B teacher and adding a token-aligned soft-KL term to the trainer.

**Architecture:** Teacher API request gains `logprobs/top_logprobs`; targets persist the raw completion + a logprobs sidecar; `build_examples` attaches per-target-token teacher top-20 (ids+logprobs) to each KD `TrainExample`, aligned by re-tokenizing the teacher's *verbatim* completion (Qwen↔Qwen → identical ids); `collate` pads to `[B,T,K]`; a new `kd_soft_kl_loss` adds the soft term. A hard **alignment guard** drops to hard-CE-only on any mismatched position and counts drops, so a tokenization surprise degrades gracefully instead of training on garbage.

**Tech Stack:** Python, PyTorch, transformers tokenizers, urllib (existing teacher client), pytest.

**Spec:** `docs/superpowers/specs/2026-06-14-doc-rebaseline-advisor-faithful-design.md` §5.

**Scope split:** Tasks 1–6 = code + unit tests, runnable on Mac (no API, no GPU — tests use a tiny real Qwen tokenizer call or a fake). Task 7 = the actual data regen + train + eval, which needs the DeepInfra key + a CUDA box → **user-driven, not executed from this plan**.

**Branch:** create `feat/phase2-soft-kl-kd` off `main` before Task 1.

---

## Design decisions (locked here; raise at plan review if you disagree)

1. **KD target text = the teacher's verbatim completion** (not the reassembled `reasoning\nSQL:`). The student re-tokenizes the exact stored string; with a shared Qwen tokenizer the ids match the API's content tokens 1:1. `parse_teacher_output` is still used to extract SQL for exec-filtering and for the `gold` arm — it no longer reshapes the KD target.
2. **Truncated KL over top-20.** Teacher distribution is renormalised over the 20 returned tokens: `p_k = softmax(teacher_logprob_k / τ)`. Soft loss at a position = `−Σ_k p_k · logsoftmax(student_logits/τ)[id_k] · τ²` (standard KD temperature scaling). Default `τ=2.0`, `λ_soft=0.5` (config-exposed).
3. **Alignment guard.** At build time, map each teacher content-token string → a student vocab id via the shared tokenizer; if the re-tokenized target id at position t ≠ the teacher content-token id at t, mark that position `no-soft` (soft term skipped, hard CE unchanged) and increment a counter logged per client. Soft term only applies on `source=="kd"` positions that pass the guard.
4. **Logprobs persistence = JSONL sidecar** next to the CSV: `teacher_targets.<name>.logprobs.jsonl`, one line/question. Keeps the CSV human-readable and the committed-artifact contract intact (a few MB). `TeacherTarget` gains one field: `completion: str` (raw teacher text). Logprobs live only in the sidecar, joined by `question`.
5. **Back-compat:** none kept (per repo convention). `complete()` returns a `TeacherCompletion` dataclass; callers updated. Targets without a sidecar (old runs) train with **hard-CE only** (soft term simply absent) — not an error.

---

## Task 1: Teacher API returns top-20 logprobs

**Files:**
- Modify: `fedicl-sql/fedicl_sql/models/teacher.py`
- Test: `fedicl-sql/tests/test_teacher.py`

- [ ] **Step 1: Write the failing test** (append to `tests/test_teacher.py`)

```python
def test_complete_parses_top_logprobs(monkeypatch):
    from fedicl_sql.models import teacher as T

    fake_resp = {
        "choices": [{
            "message": {"content": "SELECT 1"},
            "logprobs": {"content": [
                {"token": "SELECT", "logprob": -0.1,
                 "top_logprobs": [{"token": "SELECT", "logprob": -0.1},
                                  {"token": "select", "logprob": -2.0}]},
                {"token": " 1", "logprob": -0.5,
                 "top_logprobs": [{"token": " 1", "logprob": -0.5}]},
            ]},
        }]
    }
    monkeypatch.setattr(T, "_post_json", lambda *a, **k: fake_resp)
    cfg = T.TeacherConfig(base_url="http://x", api_key="k", model="m")
    out = T.OpenAICompatibleTeacher(cfg).complete("sys", "usr", top_logprobs=20)
    assert out.text == "SELECT 1"
    assert [t.token for t in out.token_logprobs] == ["SELECT", " 1"]
    assert out.token_logprobs[0].top[0] == ("SELECT", -0.1)
    assert out.token_logprobs[0].top[1] == ("select", -2.0)
```

- [ ] **Step 2: Run it — expect FAIL** (`complete` returns str, no `top_logprobs` kwarg)

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py::test_complete_parses_top_logprobs -q`
Expected: FAIL (TypeError: unexpected keyword / AttributeError on `.text`).

- [ ] **Step 3: Implement** — add dataclasses + extend `complete`

At top of `teacher.py` (after the imports), add:

```python
@dataclass
class TokenLogprobs:
    token: str
    top: list[tuple[str, float]]  # [(token_str, logprob)], teacher's top-k incl. chosen


@dataclass
class TeacherCompletion:
    text: str
    token_logprobs: list[TokenLogprobs] | None  # None when logprobs not requested
```

Change `complete` signature to `def complete(self, system, user, progress=None, top_logprobs: int | None = None) -> TeacherCompletion:` and:
- in `body`, when `top_logprobs` is not None: `body["logprobs"] = True; body["top_logprobs"] = top_logprobs`.
- replace the success block (the `content = resp[...]["content"]` part) with:

```python
            try:
                choice = resp["choices"][0]
                content = choice["message"]["content"]
                tl = None
                if top_logprobs is not None:
                    raw = (choice.get("logprobs") or {}).get("content") or []
                    tl = [
                        TokenLogprobs(
                            token=tok["token"],
                            top=[(a["token"], float(a["logprob"]))
                                 for a in (tok.get("top_logprobs") or [])],
                        )
                        for tok in raw
                    ]
                if progress:
                    progress(f"teacher response_ok attempt={attempt + 1} chars={len(content)}")
                return TeacherCompletion(text=content, token_logprobs=tl)
            except (KeyError, IndexError, TypeError) as e:
                raise RuntimeError(f"unexpected teacher response shape: {resp!r}") from e
```

- [ ] **Step 4: Run it — expect PASS**

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py::test_complete_parses_top_logprobs -q`
Expected: PASS.

- [ ] **Step 5: Fix the other `complete()` caller** (gen script uses `.text` — handled in Task 3; runtime escalation, if any, in `fedicl_sql/runtime/`):

Run: `cd fedicl-sql && rg -n '\.complete\(' fedicl_sql scripts`
For each hit not in Task 3, update to use `.text`. Run the full teacher test file:
`uv run pytest tests/test_teacher.py -q` → expect PASS.

- [ ] **Step 6: Commit**

```bash
cd fedicl-sql && git add fedicl_sql/models/teacher.py tests/test_teacher.py
git commit -m "feat(teacher): complete() returns TeacherCompletion with optional top-k logprobs"
```

---

## Task 2: TeacherTarget carries raw completion; logprobs sidecar I/O

**Files:**
- Modify: `fedicl-sql/fedicl_sql/data/teacher_targets.py`
- Test: `fedicl-sql/tests/test_teacher.py`

- [ ] **Step 1: Write the failing test**

```python
def test_logprobs_sidecar_roundtrip(tmp_path):
    from fedicl_sql.data.teacher_targets import (
        TokenTop, save_logprobs_sidecar, load_logprobs_sidecar,
    )
    lp = {"q1": [TokenTop(token="SELECT", top=[("SELECT", -0.1), ("select", -2.0)])]}
    p = tmp_path / "t.logprobs.jsonl"
    save_logprobs_sidecar(lp, str(p))
    back = load_logprobs_sidecar(str(p))
    assert back["q1"][0].token == "SELECT"
    assert back["q1"][0].top == [("SELECT", -0.1), ("select", -2.0)]


def test_teachertarget_has_completion_field():
    from fedicl_sql.data.teacher_targets import TeacherTarget
    t = TeacherTarget("q", "db", "p", "g", "s", "r", True, True, completion="raw text")
    assert t.completion == "raw text"
```

- [ ] **Step 2: Run — expect FAIL** (no `TokenTop`/sidecar fns; `completion` not a field)

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py -k "sidecar or completion_field" -q`
Expected: FAIL (ImportError / unexpected kwarg).

- [ ] **Step 3: Implement** in `teacher_targets.py`

Add `import json` at top. Add `completion: str = ""` as the last field of `TeacherTarget` (default keeps `validate_target` and old CSVs valid). Add:

```python
@dataclass
class TokenTop:
    token: str
    top: list[tuple[str, float]]


def save_logprobs_sidecar(by_question: dict[str, list[TokenTop]], path: str) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        for q, toks in by_question.items():
            f.write(json.dumps({
                "question": q,
                "tokens": [{"t": tt.token, "top": [[a, b] for a, b in tt.top]} for tt in toks],
            }) + "\n")


def load_logprobs_sidecar(path: str) -> dict[str, list[TokenTop]]:
    out: dict[str, list[TokenTop]] = {}
    if not Path(path).exists():
        return out
    with open(path, encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            row = json.loads(line)
            out[row["question"]] = [
                TokenTop(token=t["t"], top=[(a, float(b)) for a, b in t["top"]])
                for t in row["tokens"]
            ]
    return out
```

Add `completion` to `targets_to_csv` (it's already in `_FIELDS` via `fields()`) — verify the row write handles it (string, no special-casing needed). In `load_targets`, add `completion=row.get("completion", "")` to the `TeacherTarget(...)` call (so old CSVs without the column still load).

- [ ] **Step 4: Run — expect PASS**

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py -k "sidecar or completion_field" -q`
Expected: PASS.

- [ ] **Step 5: Guard old-CSV load** — add a test that a CSV written without `completion` still loads:

```python
def test_load_targets_without_completion_column(tmp_path):
    import csv
    from fedicl_sql.data.teacher_targets import load_targets
    p = tmp_path / "old.csv"
    with open(p, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["question","db_id","db_path","gold",
                                          "teacher_sql","reasoning","exec_ok","exec_correct"])
        w.writeheader()
        w.writerow({"question":"q","db_id":"d","db_path":"p","gold":"g",
                    "teacher_sql":"s","reasoning":"r","exec_ok":"1","exec_correct":"1"})
    t = load_targets(str(p))[0]
    assert t.completion == ""
```

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py -k completion -q` → expect PASS.

- [ ] **Step 6: Commit**

```bash
cd fedicl-sql && git add fedicl_sql/data/teacher_targets.py tests/test_teacher.py
git commit -m "feat(targets): TeacherTarget.completion + top-k logprobs JSONL sidecar I/O"
```

---

## Task 3: gen_teacher_targets requests + persists logprobs

**Files:**
- Modify: `fedicl-sql/scripts/gen_teacher_targets.py`
- Test: `fedicl-sql/tests/test_teacher.py`

- [ ] **Step 1: Write the failing test** — drive `generate` with a fake teacher returning a `TeacherCompletion`, assert a sidecar is written next to `--out`.

```python
def test_generate_writes_logprobs_sidecar(tmp_path, monkeypatch):
    from pathlib import Path
    import scripts.gen_teacher_targets as G
    from fedicl_sql.models.teacher import TeacherCompletion, TokenLogprobs

    class FakeTeacher:
        config = type("C", (), {"model": "m", "base_url": "http://x", "timeout": 1, "retries": 0})()
        def complete(self, system, user, progress=None, top_logprobs=None):
            return TeacherCompletion(
                text="SELECT 1",
                token_logprobs=[TokenLogprobs("SELECT", [("SELECT", -0.1)])],
            )

    # one-row public CSV
    pub = tmp_path / "public_X.csv"
    pub.write_text("question,query,db_id,db_path\nQ?,SELECT 1,db,:memory:\n")
    monkeypatch.setattr(G, "db_to_ddl", lambda p: "TABLE t(c)")
    monkeypatch.setattr(G, "validate_target",
        lambda q, dbid, dbp, gold, sql, rsn: G.__dict__["validate_target"])  # replaced below
    # use the real validate_target but stub exec via metrics? simpler: monkeypatch validate
    from fedicl_sql.data.teacher_targets import TeacherTarget
    monkeypatch.setattr(G, "validate_target",
        lambda q, dbid, dbp, gold, sql, rsn: TeacherTarget(q, dbid, dbp, gold, sql, rsn, True, True, completion=sql))
    monkeypatch.setattr(G, "parse_teacher_output", lambda text: ("", text))
    monkeypatch.setattr(G, "build_teacher_prompt", lambda q, ddl: ("sys", "usr"))

    out = tmp_path / "tt.csv"
    G.generate(str(pub), str(out), FakeTeacher(), top_logprobs=20, progress=lambda *a, **k: None)
    side = Path(str(out).replace(".csv", ".logprobs.jsonl"))
    assert side.exists()
    from fedicl_sql.data.teacher_targets import load_logprobs_sidecar
    assert load_logprobs_sidecar(str(side))["Q?"][0].token == "SELECT"
```

- [ ] **Step 2: Run — expect FAIL** (`generate` has no `top_logprobs` param; no sidecar written)

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py::test_generate_writes_logprobs_sidecar -q`
Expected: FAIL.

- [ ] **Step 3: Implement** — in `generate(...)`:
  - add param `top_logprobs: int | None = None` to the signature.
  - build a `logprobs_by_q: dict[str, list[TokenTop]] = {}` (load existing sidecar if resuming, mirroring the `done` pattern).
  - call `comp = teacher.complete(system, user, progress=..., top_logprobs=top_logprobs)`; use `comp.text` for `parse_teacher_output`; set the target's `completion = comp.text`; if `comp.token_logprobs`, store `logprobs_by_q[ex.question] = [TokenTop(t.token, t.top) for t in comp.token_logprobs]`.
  - after each `targets_to_csv(...)`, also `save_logprobs_sidecar(logprobs_by_q, sidecar_path)` where `sidecar_path = out.replace(".csv", ".logprobs.jsonl")` (incremental flush, crash-safe).
  - import `TokenTop, save_logprobs_sidecar, load_logprobs_sidecar` from `fedicl_sql.data.teacher_targets`.
  - in `main()`, add `--top-logprobs` (type=int, default=20) and pass it through.

- [ ] **Step 4: Run — expect PASS**

Run: `cd fedicl-sql && uv run pytest tests/test_teacher.py::test_generate_writes_logprobs_sidecar -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
cd fedicl-sql && git add scripts/gen_teacher_targets.py tests/test_teacher.py
git commit -m "feat(gen): request top-20 logprobs, persist raw completion + sidecar"
```

---

## Task 4: build_examples attaches aligned teacher top-20 to KD examples

**Files:**
- Modify: `fedicl-sql/fedicl_sql/training/dataset.py`
- Test: `fedicl-sql/tests/test_training.py`

- [ ] **Step 1: Write the failing test** — a fake tokenizer with a known vocab; verify KD example carries per-target-token topk ids/logprobs and the alignment guard zeroes mismatches.

```python
def test_build_examples_attaches_aligned_topk():
    from fedicl_sql.training.dataset import build_examples
    from fedicl_sql.data.teacher_targets import TeacherTarget, TokenTop
    from fedicl_sql.data.spider import SpiderExample

    class FakeTok:
        pad_token_id = 0
        eos_token_id = 9
        chat_template = None  # take the base-model branch (encode prompt/target separately)
        _vocab = {"SELECT": 1, " 1": 2, "select": 3}
        def encode(self, s, add_special_tokens=False):
            return [self._vocab[t] for t in s.split("|") if t]
        def convert_ids_to_tokens(self, ids):
            inv = {v: k for k, v in self._vocab.items()}
            return [inv.get(i, "?") for i in ids]
        def convert_tokens_to_ids(self, tok):
            return self._vocab.get(tok, -1)

    tt = TeacherTarget("Q", "db", ":memory:", "g", "SELECT| 1", "", True, True,
                       completion="SELECT| 1")
    lp = {"Q": [TokenTop("SELECT", [("SELECT", -0.1), ("select", -2.0)]),
                TokenTop(" 1", [(" 1", -0.5)])]}
    exs = build_examples([], [tt], FakeTok(), schema_fn=lambda p: "S",
                         logprobs_by_question=lp)
    kd = [e for e in exs if e.source == "kd"][0]
    # two target tokens (+eos); first two carry topk, eos carries none
    assert kd.kd_topk_ids[0] == [1, 3]          # SELECT, select mapped to ids
    assert kd.kd_topk_logprobs[0] == [-0.1, -2.0]
    assert kd.kd_topk_ids[-1] == []             # eos: no teacher logprob → no soft
```

- [ ] **Step 2: Run — expect FAIL** (`build_examples` has no `logprobs_by_question`; `TrainExample` has no `kd_topk_*`)

Run: `cd fedicl-sql && uv run pytest tests/test_training.py::test_build_examples_attaches_aligned_topk -q`
Expected: FAIL.

- [ ] **Step 3: Implement**
  - Add to `TrainExample`: `kd_topk_ids: list[list[int]] = field(default_factory=list)` and `kd_topk_logprobs: list[list[float]] = field(default_factory=list)` (import `field`). Empty list per position means "no soft term here".
  - In `_assemble`, add optional param `topk: list[list[tuple[int,float]]] | None = None` aligned to `target_ids` *after* the same trimming. Build `kd_topk_ids`/`kd_topk_logprobs` as `[0.0]*len(prompt_ids)`-style prefixes of empty lists, then per target position append the topk (or `[]`). When `topk is None`, fill all-empty.
  - Add the **alignment + guard** in `build_examples` for the `kd_label=="teacher"` branch, only when `logprobs_by_question` has the question: re-tokenize via the same path; for each target position i, look up the teacher `TokenTop` for that content position; map each `(tok_str, logprob)` to `(tokenizer.convert_tokens_to_ids(tok_str), logprob)`; **guard**: if the position's teacher chosen-token id (first entry) ≠ `target_ids[i]`, set that position's topk to `[]` and increment a `dropped` counter. Account for the eos/template tail positions (no teacher entry) → `[]`.
  - `build_examples` signature gains `logprobs_by_question: dict[str, list[TokenTop]] | None = None`. Return value unchanged (list[TrainExample]); log the per-call dropped-position count via the existing return path is N/A — instead `print`/return is not available, so accumulate and attach nothing; the trainer logs it in Task 6 by summing positions. Simplest: keep a module-level-free design — count drops into a local and `print(f"kd soft-align dropped={dropped}")` is wrong for a lib; instead expose via a returned tuple is a breaking change. **Decision:** add an optional `stats: dict | None = None` param; if given, write `stats["soft_dropped"]`/`stats["soft_total"]`. Trainer passes a dict and logs it.

> Implementation note for the guard's token→id mapping: prefer `tokenizer.convert_tokens_to_ids(tok_str)`; some tokenizers need the raw piece (with `Ġ`/`▁`). If `convert_tokens_to_ids` returns `unk`/`-1` for a surface token, fall back to `tokenizer.encode(tok_str, add_special_tokens=False)` and take it only if it is a single id; else treat as a mismatch (drop). This keeps the guard conservative.

- [ ] **Step 4: Run — expect PASS** (the listed test plus a guard test below)

Add a guard test:

```python
def test_build_examples_guard_drops_misaligned():
    # teacher chosen token disagrees with the re-tokenized target at pos 0 → that pos drops
    ...  # same FakeTok; tt.completion tokenizes to [1,2] but teacher TokenTop[0].token="select"(id3)
```

Run: `cd fedicl-sql && uv run pytest tests/test_training.py -k "topk or guard" -q`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
cd fedicl-sql && git add fedicl_sql/training/dataset.py tests/test_training.py
git commit -m "feat(dataset): attach token-aligned teacher top-20 to KD examples with a hard guard"
```

---

## Task 5: collate pads top-k; soft-KL loss

**Files:**
- Modify: `fedicl-sql/fedicl_sql/training/losses.py`, `fedicl-sql/fedicl_sql/training/lora_trainer.py` (collate)
- Test: `fedicl-sql/tests/test_training.py`

- [ ] **Step 1: Write the failing test** for `kd_soft_kl_loss`

```python
def test_soft_kl_zero_when_student_matches_teacher():
    import torch
    from fedicl_sql.training.losses import kd_soft_kl_loss
    # 1 batch, 2 positions, vocab 4, K=2
    logits = torch.zeros(1, 3, 4)              # will be shifted → 2 active target steps
    # make student logits at target positions huge on the teacher's top token
    logits[0, 0, 1] = 50.0                     # predicts id=1 for position-1 label
    logits[0, 1, 2] = 50.0
    labels = torch.tensor([[ -100, 1, 2]])
    topk_ids = torch.tensor([[[0,0],[1,0],[2,0]]])         # [B,T,K]
    topk_lp = torch.tensor([[[0.,-1e4],[0.,-1e4],[0.,-1e4]]])
    mask = torch.tensor([[0,1,1]])                          # soft only on the 2 target steps
    loss = kd_soft_kl_loss(logits, labels, topk_ids, topk_lp, mask, tau=1.0)
    assert loss.item() < 1e-3
```

- [ ] **Step 2: Run — expect FAIL** (`kd_soft_kl_loss` undefined)

Run: `cd fedicl-sql && uv run pytest tests/test_training.py::test_soft_kl_zero_when_student_matches_teacher -q`
Expected: FAIL (ImportError).

- [ ] **Step 3: Implement** in `losses.py`

```python
def kd_soft_kl_loss(logits, labels, topk_ids, topk_logprobs, soft_mask, tau=2.0):
    """Truncated soft-KD over the teacher's top-k tokens, temperature-scaled.

    logits [B,T,V]; labels [B,T] (causal shift, -100 ignore); topk_ids/topk_logprobs [B,T,K]
    (teacher ids + raw logprobs, padded with id 0 / logprob -1e4); soft_mask [B,T] in {0,1}
    marking positions with a valid teacher distribution. Returns scalar (0 if no soft positions).
    """
    s_logits = logits[:, :-1, :]
    s_ids = topk_ids[:, 1:, :]
    s_tlp = topk_logprobs[:, 1:, :]
    s_mask = soft_mask[:, 1:].to(s_logits.dtype)

    # teacher dist over the k slots (pads have logprob -1e4 → ~0 prob), temperature τ
    t_p = torch.softmax(s_tlp / tau, dim=-1)                       # [B,T-1,K]
    student_logp = torch.log_softmax(s_logits / tau, dim=-1)       # [B,T-1,V]
    gathered = torch.gather(student_logp, -1, s_ids.clamp(min=0))  # [B,T-1,K]
    per_pos = -(t_p * gathered).sum(-1) * (tau * tau)              # [B,T-1]
    w = s_mask
    return (per_pos * w).sum() / w.sum().clamp(min=1e-8)
```

- [ ] **Step 4: Run — expect PASS**

Run: `cd fedicl-sql && uv run pytest tests/test_training.py::test_soft_kl_zero_when_student_matches_teacher -q`
Expected: PASS.

- [ ] **Step 5: Extend `collate`** in `lora_trainer.py` to emit `kd_topk_ids`/`kd_topk_logprobs`/`soft_mask` tensors `[B,T,K]`/`[B,T]` (K = max top-k width in the batch, ≥1; pad ids with 0, logprobs with -1e4, mask 0 where a position has no topk). Add a unit test `test_collate_pads_topk` asserting shapes and that an empty-topk position has `soft_mask==0`.

Run: `cd fedicl-sql && uv run pytest tests/test_training.py::test_collate_pads_topk -q` → expect PASS.

- [ ] **Step 6: Commit**

```bash
cd fedicl-sql && git add fedicl_sql/training/losses.py fedicl_sql/training/lora_trainer.py tests/test_training.py
git commit -m "feat(loss): truncated temperature-scaled soft-KL KD term + collate top-k padding"
```

---

## Task 6: wire soft-KL into the training step + config

**Files:**
- Modify: `fedicl-sql/fedicl_sql/training/lora_trainer.py`
- Test: `fedicl-sql/tests/test_training.py`

- [ ] **Step 1: Write the failing test** — a tiny end-to-end `train_client` smoke on `:memory:`-free fakes is heavy; instead test the **loss combination** in isolation:

```python
def test_total_loss_adds_soft_term_only_for_kd():
    import torch
    from fedicl_sql.training.losses import weighted_lm_loss, kd_soft_kl_loss
    logits = torch.randn(1, 4, 6)
    labels = torch.tensor([[-100, 1, 2, 3]])
    weights = torch.tensor([[0., 1., 1., 1.]])
    hard = weighted_lm_loss(logits, labels, weights)
    zero_mask = torch.zeros(1, 4)
    soft0 = kd_soft_kl_loss(logits, labels, torch.zeros(1,4,2,dtype=torch.long),
                            torch.full((1,4,2), -1e4), zero_mask)
    assert soft0.item() == 0.0          # no soft positions → no contribution
```

- [ ] **Step 2: Run — expect PASS already for the helper** (this guards the "soft=0 when masked" invariant the trainer relies on). If it fails, fix `kd_soft_kl_loss`'s empty-mask path.

Run: `cd fedicl-sql && uv run pytest tests/test_training.py::test_total_loss_adds_soft_term_only_for_kd -q`

- [ ] **Step 3: Implement** in `train_client`:
  - add to `LoraTrainConfig`: `lambda_soft: float = 0.5`, `kd_tau: float = 2.0`.
  - pass `logprobs_by_question` into `build_examples` (the caller — `experiments/p1_client_train/run.py` — loads the sidecar and passes it; for now `train_client` gains a `logprobs_by_question=None` param threaded to `build_examples`, plus a `stats={}` it logs).
  - in the step loop, after `out = model(...)`:

```python
        hard = weighted_lm_loss(out.logits, batch["labels"], batch["weights"])
        if config.lambda_soft and "soft_mask" in batch and batch["soft_mask"].any():
            soft = kd_soft_kl_loss(out.logits, batch["labels"], batch["kd_topk_ids"],
                                   batch["kd_topk_logprobs"], batch["soft_mask"], tau=config.kd_tau)
            loss = hard + config.lambda_soft * soft
        else:
            loss = hard
```
  - import `kd_soft_kl_loss`.
  - log `stats` (soft_dropped/soft_total) once after `build_examples`.

- [ ] **Step 4: Run the full training test file**

Run: `cd fedicl-sql && uv run pytest tests/test_training.py -q`
Expected: PASS (all, including pre-existing skeleton tests).

- [ ] **Step 5: Run the whole suite — no regressions**

Run: `cd fedicl-sql && uv run pytest -q`
Expected: PASS (≥81 prior tests + the new ones).

- [ ] **Step 6: Commit**

```bash
cd fedicl-sql && git add fedicl_sql/training/lora_trainer.py tests/test_training.py
git commit -m "feat(trainer): combine hard CE + lambda_soft*soft-KL; expose kd_tau/lambda_soft"
```

---

## Task 7: RUN (user-driven — needs DeepInfra key + CUDA; NOT executed from this plan)

Outline only. Document each run in `LAB_LOG.md` + `RUNS.csv`.

1. `export TEACHER_API_KEY=<deepinfra>` then `bash teacher2.sh` → regenerate `teacher_targets.qwen72b.csv` + `.logprobs.jsonl` on public X (one-time, cached, ~$1–2).
2. `p1_client_train --kd-label teacher` ×3 (now with soft-KL) → `p1_fedavg` → `M_G`; plus `gold_ce` and `x_only` arms.
3. Eval `M_G` vs `B2` vs `gold_ce` vs `x_only` on the **full held-out (1034)** (not `[:200]` — the spec's power fix).
4. Record the three deltas + the soft-align dropped-rate.

---

## Self-review notes

- **Spec coverage:** §5.1 (gen logprobs) → Tasks 1,3; §5.2 (soft term) → Tasks 4,5,6; §5.3 (retire MinED) → no scaffolding exists to remove (codegraph found none); §5.4 (run on 1034) → Task 7. ✓
- **Alignment guard** is the correctness keystone — Task 4 step 3 + its guard test.
- **No GPU/API in Tasks 1–6:** every test uses fakes or tiny tensors. Task 7 is explicitly user-driven.
- **Caller `experiments/p1_client_train/run.py`** must load the sidecar and pass `logprobs_by_question` — fold that one-line wiring into Task 6 step 3 (read the file first; it already calls `load_targets`).
