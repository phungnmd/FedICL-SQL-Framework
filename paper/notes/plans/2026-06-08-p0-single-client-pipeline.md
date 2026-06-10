# P0 — Single-Client NL2SQL Pipeline Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a working single-client NL2SQL pipeline: Spider data → DDL serialisation → BGE retrieval → prompt assembly → Phi-3-mini inference → EX/EM scoring.

**Architecture:** Three independent modules (data, retrieval, prompts) feed a thin pipeline script. Model loading auto-selects MPS float16 (Apple Silicon dev) or CUDA 4-bit (GPU server). Eval uses native sqlite3 + sqlglot — no external eval server needed.

**Tech Stack:** Python 3.10+, uv, HuggingFace datasets + transformers, sentence-transformers (BAAI/bge-small-en-v1.5), faiss-cpu, sqlglot, sqlite3, pytest

**Hardware note:** Apple M4 Pro (MPS, 24GB RAM) for development — Phi-3-mini runs in float16 on MPS, no bitsandbytes needed. On CUDA server, set `LOAD_IN_4BIT=1` env var.

---

## File Map

```
fedicl-sql/
├── data/
│   ├── __init__.py
│   └── spider.py           # load_spider(), db_to_ddl(), SpiderExample dataclass
├── retrieval/
│   ├── __init__.py
│   └── retriever.py        # DemoRetriever: build_index(), retrieve()
├── prompts/
│   ├── __init__.py
│   └── builder.py          # build_prompt(question, schema_ddl, demos)
├── models/
│   ├── __init__.py
│   └── student.py          # StudentModel: __init__(), generate()
├── eval/
│   ├── __init__.py
│   └── metrics.py          # score_ex(), score_em(), eval_batch()
├── experiments/
│   └── p0_sanity.py        # end-to-end: 1 question, print result + EX
├── tests/
│   ├── conftest.py
│   ├── test_data.py
│   ├── test_retrieval.py
│   ├── test_prompts.py
│   └── test_eval.py
├── pyproject.toml
└── .gitignore
```

---

## Task 0: Repo skeleton + environment

**Files:**
- Create: `fedicl-sql/pyproject.toml`
- Create: `fedicl-sql/.gitignore`
- Create: all `__init__.py` stubs

- [ ] **Step 1: Init repo**

```bash
cd /Users/edric/Learning/FedICL-SQL
uv init fedicl-sql --no-workspace
cd fedicl-sql
git init
git checkout -b main
```

- [ ] **Step 2: Write pyproject.toml**

Replace the generated `pyproject.toml` with:

```toml
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[project]
name = "fedicl-sql"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = [
    "torch>=2.2",
    "transformers>=4.41",
    "faiss-cpu>=1.8",
    "sentence-transformers>=3.0",
    "datasets>=2.19",
    "sqlglot>=25.0",
    "pyyaml>=6.0",
    "tqdm>=4.0",
    "numpy>=1.26",
    "accelerate>=0.30",
]

[project.optional-dependencies]
gpu4bit = ["bitsandbytes>=0.43"]
dev = ["pytest>=8.0", "pytest-cov>=5.0"]

[tool.pytest.ini_options]
testpaths = ["tests"]
```

- [ ] **Step 3: Install dependencies**

```bash
uv sync --extra dev
```

Expected: resolves without error, creates `.venv/`.

- [ ] **Step 4: Create directory skeleton**

```bash
mkdir -p data retrieval prompts models eval experiments tests
touch data/__init__.py retrieval/__init__.py prompts/__init__.py \
      models/__init__.py eval/__init__.py
```

- [ ] **Step 5: Write .gitignore**

```
.venv/
__pycache__/
*.pyc
*.pyo
.DS_Store
*.db
*.sqlite
data/spider/
data/spider_realistic/
*.pt
*.bin
*.safetensors
.env
*.log
experiments/results/
```

- [ ] **Step 6: Commit**

```bash
git add pyproject.toml .gitignore data/ retrieval/ prompts/ models/ eval/ experiments/ tests/
git commit -m "chore: repo skeleton, pyproject.toml, directory layout"
```

---

## Task 1: Spider data loader + DDL serialiser

**Files:**
- Create: `data/spider.py`
- Create: `tests/test_data.py`
- Create: `tests/conftest.py`

- [ ] **Step 1: Write failing tests**

`tests/conftest.py`:
```python
import sqlite3
import tempfile
import os
import pytest

@pytest.fixture
def tmp_db(tmp_path):
    """Minimal SQLite DB for testing without downloading Spider."""
    db_path = tmp_path / "test.db"
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        CREATE TABLE orders (
            order_id INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL,
            total_amount REAL,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        );
        CREATE TABLE customers (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
    return str(db_path)
```

`tests/test_data.py`:
```python
from data.spider import db_to_ddl, SpiderExample

def test_db_to_ddl_contains_table_names(tmp_db):
    ddl = db_to_ddl(tmp_db)
    assert "orders" in ddl.lower()
    assert "customers" in ddl.lower()

def test_db_to_ddl_preserves_foreign_keys(tmp_db):
    ddl = db_to_ddl(tmp_db)
    assert "FOREIGN KEY" in ddl or "foreign key" in ddl.lower()

def test_db_to_ddl_preserves_types(tmp_db):
    ddl = db_to_ddl(tmp_db)
    assert "INTEGER" in ddl or "REAL" in ddl

def test_spider_example_fields():
    ex = SpiderExample(
        question="How many orders?",
        query="SELECT COUNT(*) FROM orders",
        db_id="test",
        db_path="/tmp/test.db",
    )
    assert ex.question == "How many orders?"
    assert ex.db_id == "test"
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
uv run pytest tests/test_data.py -v
```

Expected: `ImportError: cannot import name 'db_to_ddl'`

- [ ] **Step 3: Implement `data/spider.py`**

```python
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from datasets import load_dataset


@dataclass
class SpiderExample:
    question: str
    query: str
    db_id: str
    db_path: str


def db_to_ddl(db_path: str) -> str:
    """Extract CREATE TABLE statements from a SQLite file."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT sql FROM sqlite_master WHERE type='table' AND sql IS NOT NULL ORDER BY name"
    )
    stmts = [row[0].strip() for row in cursor.fetchall() if row[0]]
    conn.close()
    return ";\n\n".join(stmts) + ";"


def load_spider(split: str = "train", cache_dir: str = "data/spider") -> list[SpiderExample]:
    """
    Load Spider from HuggingFace datasets.
    Each example has db_path pointing to the downloaded SQLite file.
    split: 'train' or 'validation'
    """
    ds = load_dataset("spider", split=split, trust_remote_code=True, cache_dir=cache_dir)
    examples = []
    for row in ds:
        examples.append(SpiderExample(
            question=row["question"],
            query=row["query"],
            db_id=row["db_id"],
            db_path=row["db_path"],
        ))
    return examples
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
uv run pytest tests/test_data.py -v
```

Expected: 4 passed.

- [ ] **Step 5: Commit**

```bash
git add data/spider.py tests/test_data.py tests/conftest.py
git commit -m "feat(data): Spider loader, DDL serialiser, SpiderExample dataclass"
```

---

## Task 2: Retrieval module (BGE + FAISS)

**Files:**
- Create: `retrieval/retriever.py`
- Create: `tests/test_retrieval.py`

- [ ] **Step 1: Write failing tests**

`tests/test_retrieval.py`:
```python
from retrieval.retriever import DemoRetriever
from data.spider import SpiderExample

SAMPLE_EXAMPLES = [
    SpiderExample("How many students?", "SELECT COUNT(*) FROM students", "uni", "/tmp/uni.db"),
    SpiderExample("List all orders by date", "SELECT * FROM orders ORDER BY date", "shop", "/tmp/shop.db"),
    SpiderExample("What is the total revenue?", "SELECT SUM(amount) FROM sales", "finance", "/tmp/fin.db"),
    SpiderExample("Find students older than 20", "SELECT * FROM students WHERE age > 20", "uni", "/tmp/uni.db"),
]

def test_retriever_returns_k_results():
    r = DemoRetriever()
    r.build_index(SAMPLE_EXAMPLES)
    results = r.retrieve("How many people enrolled?", k=2)
    assert len(results) == 2

def test_retriever_returns_spider_examples():
    r = DemoRetriever()
    r.build_index(SAMPLE_EXAMPLES)
    results = r.retrieve("Count the number of employees", k=1)
    assert isinstance(results[0], SpiderExample)
    assert results[0].query != ""

def test_retriever_most_similar_first():
    r = DemoRetriever()
    r.build_index(SAMPLE_EXAMPLES)
    # "total sales amount" is most similar to "total revenue"
    results = r.retrieve("What is the total sales amount?", k=2)
    assert "SUM" in results[0].query or "revenue" in results[0].question.lower()

def test_retriever_k_capped_at_index_size():
    r = DemoRetriever()
    r.build_index(SAMPLE_EXAMPLES[:2])
    results = r.retrieve("any query", k=10)
    assert len(results) == 2
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
uv run pytest tests/test_retrieval.py -v
```

Expected: `ImportError: cannot import name 'DemoRetriever'`

- [ ] **Step 3: Implement `retrieval/retriever.py`**

```python
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from data.spider import SpiderExample


class DemoRetriever:
    """BGE-small + FAISS inner-product index (cosine on L2-normalised vecs)."""

    MODEL_ID = "BAAI/bge-small-en-v1.5"

    def __init__(self, model_id: str = MODEL_ID):
        self.encoder = SentenceTransformer(model_id)
        self.index: faiss.Index | None = None
        self.examples: list[SpiderExample] = []

    def build_index(self, examples: list[SpiderExample]) -> None:
        self.examples = list(examples)
        questions = [e.question for e in self.examples]
        embeddings = self.encoder.encode(
            questions,
            normalize_embeddings=True,
            show_progress_bar=False,
            batch_size=64,
        ).astype(np.float32)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatIP(dim)
        self.index.add(embeddings)

    def retrieve(self, query: str, k: int = 3) -> list[SpiderExample]:
        assert self.index is not None, "Call build_index() first"
        k = min(k, len(self.examples))
        q_emb = self.encoder.encode(
            [query], normalize_embeddings=True, show_progress_bar=False
        ).astype(np.float32)
        _, indices = self.index.search(q_emb, k)
        return [self.examples[i] for i in indices[0]]
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
uv run pytest tests/test_retrieval.py -v
```

Expected: 4 passed. (First run downloads BGE model ~130MB — takes ~1 min.)

- [ ] **Step 5: Commit**

```bash
git add retrieval/retriever.py tests/test_retrieval.py
git commit -m "feat(retrieval): BGE-small + FAISS demo retriever"
```

---

## Task 3: Prompt builder

**Files:**
- Create: `prompts/builder.py`
- Create: `tests/test_prompts.py`

- [ ] **Step 1: Write failing tests**

`tests/test_prompts.py`:
```python
from prompts.builder import build_prompt
from data.spider import SpiderExample

DDL = "CREATE TABLE orders (id INTEGER PRIMARY KEY, amount REAL);"
DEMOS = [
    SpiderExample("How many orders?", "SELECT COUNT(*) FROM orders", "shop", "/tmp/shop.db"),
    SpiderExample("Total revenue?", "SELECT SUM(amount) FROM orders", "shop", "/tmp/shop.db"),
]

def test_prompt_contains_question():
    p = build_prompt("What is the max amount?", DDL, DEMOS)
    assert "What is the max amount?" in p

def test_prompt_contains_schema():
    p = build_prompt("What is the max amount?", DDL, DEMOS)
    assert "CREATE TABLE" in p
    assert "orders" in p

def test_prompt_contains_demo_questions_and_sql():
    p = build_prompt("What is the max amount?", DDL, DEMOS)
    assert "How many orders?" in p
    assert "SELECT COUNT(*) FROM orders" in p

def test_prompt_ends_with_sql_marker():
    p = build_prompt("What is the max amount?", DDL, DEMOS)
    # Model should continue from this point
    assert p.strip().endswith("### SQL:")

def test_prompt_zero_demos():
    p = build_prompt("What is the max amount?", DDL, [])
    assert "CREATE TABLE" in p
    assert "What is the max amount?" in p
    assert p.strip().endswith("### SQL:")
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
uv run pytest tests/test_prompts.py -v
```

Expected: `ImportError: cannot import name 'build_prompt'`

- [ ] **Step 3: Implement `prompts/builder.py`**

```python
from data.spider import SpiderExample

_INSTRUCTION = (
    "You are an expert SQL generator. "
    "Generate a valid SQL query for the question below based on the provided schema. "
    "Output ONLY the SQL query — no explanation, no markdown, no extra text."
)


def build_prompt(question: str, schema_ddl: str, demos: list[SpiderExample]) -> str:
    """
    σ(q, S, I, Q) = instruction ⊕ schema ⊕ k demos ⊕ question
    Matches Light-SQL [4] prompt structure (Listing 1.2).
    """
    lines = [
        "### Instruction:",
        _INSTRUCTION,
        "",
        "### Schema:",
        schema_ddl,
        "",
    ]
    for demo in demos:
        lines += [
            f"### Question: {demo.question}",
            f"### SQL: {demo.query}",
            "",
        ]
    lines += [
        f"### Question: {question}",
        "### SQL:",
    ]
    return "\n".join(lines)
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
uv run pytest tests/test_prompts.py -v
```

Expected: 5 passed.

- [ ] **Step 5: Commit**

```bash
git add prompts/builder.py tests/test_prompts.py
git commit -m "feat(prompts): σ(q,S,I,Q) prompt builder matching Light-SQL structure"
```

---

## Task 4: Eval module (EX + EM)

**Files:**
- Create: `eval/metrics.py`
- Create: `tests/test_eval.py`

- [ ] **Step 1: Write failing tests**

`tests/test_eval.py`:
```python
import sqlite3
from eval.metrics import score_ex, score_em, eval_batch
from data.spider import SpiderExample

# ---- fixtures ----

def make_db(tmp_path, name="test"):
    db = tmp_path / f"{name}.db"
    conn = sqlite3.connect(db)
    conn.executescript("""
        CREATE TABLE employees (id INTEGER PRIMARY KEY, name TEXT, salary REAL, dept TEXT);
        INSERT INTO employees VALUES (1,'Alice',80000,'Eng');
        INSERT INTO employees VALUES (2,'Bob',70000,'Eng');
        INSERT INTO employees VALUES (3,'Carol',90000,'HR');
    """)
    conn.commit()
    conn.close()
    return str(db)

# ---- EX tests ----

def test_ex_correct_query(tmp_path):
    db = make_db(tmp_path)
    assert score_ex("SELECT COUNT(*) FROM employees", "SELECT COUNT(*) FROM employees", db) is True

def test_ex_semantically_equivalent(tmp_path):
    db = make_db(tmp_path)
    # Both return {(3,)} even though column alias differs
    assert score_ex(
        "SELECT COUNT(*) FROM employees",
        "SELECT count(id) FROM employees",
        db,
    ) is True

def test_ex_wrong_query(tmp_path):
    db = make_db(tmp_path)
    assert score_ex(
        "SELECT COUNT(*) FROM employees WHERE dept='Eng'",
        "SELECT COUNT(*) FROM employees",
        db,
    ) is False

def test_ex_syntax_error_returns_false(tmp_path):
    db = make_db(tmp_path)
    assert score_ex("SELECT FRUM employees", "SELECT COUNT(*) FROM employees", db) is False

# ---- EM tests ----

def test_em_identical():
    assert score_em("SELECT id FROM t WHERE x=1", "SELECT id FROM t WHERE x=1") is True

def test_em_normalises_whitespace():
    assert score_em("SELECT  id  FROM t", "SELECT id FROM t") is True

def test_em_different_queries():
    assert score_em("SELECT id FROM t", "SELECT name FROM t") is False

# ---- batch eval ----

def test_eval_batch(tmp_path):
    db = make_db(tmp_path)
    examples = [
        SpiderExample("Count all", "SELECT COUNT(*) FROM employees", "t", db),
        SpiderExample("Wrong", "SELECT * FROM employees WHERE dept='X'", "t", db),
    ]
    preds = ["SELECT COUNT(*) FROM employees", "SELECT name FROM employees"]
    result = eval_batch(examples, preds)
    assert result["ex"] == 0.5
    assert 0.0 <= result["em"] <= 1.0
```

- [ ] **Step 2: Run tests — expect FAIL**

```bash
uv run pytest tests/test_eval.py -v
```

Expected: `ImportError: cannot import name 'score_ex'`

- [ ] **Step 3: Implement `eval/metrics.py`**

```python
import sqlite3
import sqlglot
from data.spider import SpiderExample


def _execute(sql: str, db_path: str) -> tuple[frozenset | None, str | None]:
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = None
        cursor = conn.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        # Normalise: lowercase strings, round floats to 4dp for comparison stability
        normalised = frozenset(
            tuple(
                round(v, 4) if isinstance(v, float) else str(v).strip().lower() if v is not None else ""
                for v in row
            )
            for row in rows
        )
        return normalised, None
    except Exception as e:
        return None, str(e)


def score_ex(pred_sql: str, gold_sql: str, db_path: str) -> bool:
    """Execution accuracy: compare result sets."""
    pred_result, err = _execute(pred_sql, db_path)
    if err is not None:
        return False
    gold_result, _ = _execute(gold_sql, db_path)
    return pred_result == gold_result


def _normalise_sql(sql: str) -> str:
    try:
        ast = sqlglot.parse_one(sql.strip(), dialect="sqlite")
        return ast.sql(dialect="sqlite", pretty=False).lower()
    except Exception:
        return " ".join(sql.strip().lower().split())


def score_em(pred_sql: str, gold_sql: str) -> bool:
    """Exact match after AST normalisation via sqlglot."""
    return _normalise_sql(pred_sql) == _normalise_sql(gold_sql)


def eval_batch(
    examples: list[SpiderExample],
    predictions: list[str],
) -> dict[str, float]:
    """Return {"ex": float, "em": float} over a batch."""
    assert len(examples) == len(predictions)
    ex_scores, em_scores = [], []
    for ex, pred in zip(examples, predictions):
        ex_scores.append(score_ex(pred, ex.query, ex.db_path))
        em_scores.append(score_em(pred, ex.query))
    n = len(examples)
    return {
        "ex": sum(ex_scores) / n,
        "em": sum(em_scores) / n,
        "n": n,
    }
```

- [ ] **Step 4: Run tests — expect PASS**

```bash
uv run pytest tests/test_eval.py -v
```

Expected: 9 passed.

- [ ] **Step 5: Commit**

```bash
git add eval/metrics.py tests/test_eval.py
git commit -m "feat(eval): EX (sqlite execution match) + EM (sqlglot AST normalise)"
```

---

## Task 5: Student model (Phi-3-mini, MPS/CUDA auto)

**Files:**
- Create: `models/student.py`

No unit tests for model loading (requires ~7GB download). Integration tested in Task 6.

- [ ] **Step 1: Implement `models/student.py`**

```python
import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

_DEFAULT_MODEL = "microsoft/Phi-3-mini-4k-instruct"


def _get_device_and_dtype() -> tuple[str, torch.dtype]:
    """Auto-select: CUDA 4-bit > MPS float16 > CPU float32."""
    if torch.cuda.is_available():
        return "cuda", torch.float16
    if torch.backends.mps.is_available():
        return "mps", torch.float16
    return "cpu", torch.float32


class StudentModel:
    """
    Phi-3-mini (or any causal LM) with auto device selection.
    On CUDA + LOAD_IN_4BIT=1 env var: loads bitsandbytes 4-bit quantisation.
    On MPS: loads float16 (fits comfortably on 24GB M-series).
    """

    def __init__(self, model_id: str = _DEFAULT_MODEL, cache_dir: str = "models/cache"):
        device, dtype = _get_device_and_dtype()
        use_4bit = os.environ.get("LOAD_IN_4BIT", "0") == "1" and device == "cuda"

        self.tokenizer = AutoTokenizer.from_pretrained(
            model_id, trust_remote_code=True, cache_dir=cache_dir
        )

        if use_4bit:
            from transformers import BitsAndBytesConfig
            quant_cfg = BitsAndBytesConfig(
                load_in_4bit=True,
                bnb_4bit_compute_dtype=torch.float16,
                bnb_4bit_use_double_quant=True,
                bnb_4bit_quant_type="nf4",
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                quantization_config=quant_cfg,
                device_map="auto",
                trust_remote_code=True,
                cache_dir=cache_dir,
            )
        else:
            self.model = AutoModelForCausalLM.from_pretrained(
                model_id,
                torch_dtype=dtype,
                device_map=device,
                trust_remote_code=True,
                cache_dir=cache_dir,
            )

        self.model.eval()
        self.device = device

    def generate(self, prompt: str, max_new_tokens: int = 256) -> str:
        """Return generated SQL text (new tokens only, stripped)."""
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.inference_mode():
            output = self.model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                do_sample=False,          # temp=0 equivalent
                pad_token_id=self.tokenizer.eos_token_id,
                eos_token_id=self.tokenizer.eos_token_id,
            )
        new_tokens = output[0][inputs["input_ids"].shape[1]:]
        raw = self.tokenizer.decode(new_tokens, skip_special_tokens=True).strip()
        # Extract first SQL statement (stop at blank line or comment)
        sql = raw.split("\n\n")[0].split("--")[0].strip()
        return sql
```

- [ ] **Step 2: Commit**

```bash
git add models/student.py
git commit -m "feat(models): StudentModel auto-selects MPS/CUDA, LOAD_IN_4BIT env override"
```

---

## Task 6: End-to-end sanity run (1 question)

**Files:**
- Create: `experiments/p0_sanity.py`

- [ ] **Step 1: Implement `experiments/p0_sanity.py`**

```python
"""
P0 sanity check: run one Spider dev question through the full pipeline.
Usage: uv run python experiments/p0_sanity.py
Prints: prompt, predicted SQL, gold SQL, EX result.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from data.spider import load_spider, db_to_ddl
from retrieval.retriever import DemoRetriever
from prompts.builder import build_prompt
from models.student import StudentModel
from eval.metrics import score_ex, score_em


def main():
    print("=== P0 Sanity Check ===\n")

    # 1. Load data
    print("[1/5] Loading Spider train (retrieval pool) + dev (eval)...")
    train = load_spider(split="train")
    dev = load_spider(split="validation")
    print(f"  train={len(train)}, dev={len(dev)}")

    # Pick one dev example
    example = dev[0]
    print(f"\n  Question : {example.question}")
    print(f"  Gold SQL : {example.query}")
    print(f"  DB       : {example.db_id}")

    # 2. Build retrieval index on train examples with the same db_id
    #    (single-client: local store = training examples for this DB)
    print("\n[2/5] Building FAISS retrieval index...")
    local_store = [e for e in train if e.db_id == example.db_id]
    if not local_store:
        # Fall back to all train examples if no same-db examples
        local_store = train[:200]
        print(f"  (No same-db train examples found, using first 200 train)")
    else:
        print(f"  Found {len(local_store)} same-db train examples")
    retriever = DemoRetriever()
    retriever.build_index(local_store)

    # 3. Retrieve top-3 demos
    print("\n[3/5] Retrieving top-3 demos...")
    k = 3
    demos = retriever.retrieve(example.question, k=k)
    for i, d in enumerate(demos):
        print(f"  demo[{i}]: {d.question}")

    # 4. Build prompt
    print("\n[4/5] Building prompt...")
    schema_ddl = db_to_ddl(example.db_path)
    prompt = build_prompt(example.question, schema_ddl, demos)
    print(f"  Prompt length: {len(prompt)} chars, {len(prompt.split())} words")
    print("\n--- PROMPT (truncated to 800 chars) ---")
    print(prompt[:800])
    print("...")

    # 5. Load model + generate
    print("\n[5/5] Loading Phi-3-mini and generating SQL...")
    model = StudentModel()
    print(f"  Device: {model.device}")
    predicted_sql = model.generate(prompt)

    # 6. Score
    ex = score_ex(predicted_sql, example.query, example.db_path)
    em = score_em(predicted_sql, example.query)

    print("\n=== RESULT ===")
    print(f"  Predicted : {predicted_sql}")
    print(f"  Gold      : {example.query}")
    print(f"  EX        : {'PASS' if ex else 'FAIL'}")
    print(f"  EM        : {'PASS' if em else 'FAIL'}")
    print("\nPipeline OK — single-client P0 sanity check complete.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run sanity check**

```bash
uv run python experiments/p0_sanity.py
```

Expected output (example):
```
=== P0 Sanity Check ===
[1/5] Loading Spider train (retrieval pool) + dev (eval)...
  train=7000, dev=1034
  Question : How many singers are there?
  Gold SQL : SELECT count(*) FROM singer
  DB       : concert_singer
[2/5] Building FAISS retrieval index...
  Found 6 same-db train examples
[3/5] Retrieving top-3 demos...
[4/5] Building prompt...
[5/5] Loading Phi-3-mini and generating SQL...
  Device: mps
=== RESULT ===
  Predicted : SELECT count(*) FROM singer
  Gold      : SELECT count(*) FROM singer
  EX        : PASS
  EM        : PASS
Pipeline OK
```

If EX=FAIL on the first question, that's fine for now — correctness will be measured in Task 7.

- [ ] **Step 3: Commit**

```bash
git add experiments/p0_sanity.py
git commit -m "feat(experiments): P0 end-to-end sanity script — 1 question through full pipeline"
```

---

## Task 7: Batch eval on 50 Spider dev questions

**Files:**
- Create: `experiments/p0_eval50.py`

- [ ] **Step 1: Implement `experiments/p0_eval50.py`**

```python
"""
P0 batch eval: run 50 Spider dev questions, report EX + EM.
Usage: uv run python experiments/p0_eval50.py [--n 50] [--k 3]
Saves results to experiments/results/p0_eval50.json
"""
import sys
import json
import argparse
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from tqdm import tqdm
from data.spider import load_spider, db_to_ddl
from retrieval.retriever import DemoRetriever
from prompts.builder import build_prompt
from models.student import StudentModel
from eval.metrics import score_ex, score_em


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=50, help="Number of dev examples to evaluate")
    parser.add_argument("--k", type=int, default=3, help="Number of ICL demos")
    args = parser.parse_args()

    print(f"P0 Batch Eval — n={args.n}, k={args.k}")

    # Load data
    print("Loading Spider...")
    train = load_spider(split="train")
    dev = load_spider(split="validation")
    dev_subset = dev[:args.n]

    # Build per-db retrieval indices (cache them)
    print("Building retrieval indices per DB...")
    db_retrievers: dict[str, DemoRetriever] = {}
    for ex in tqdm(dev_subset):
        if ex.db_id not in db_retrievers:
            local = [e for e in train if e.db_id == ex.db_id]
            if not local:
                local = train[:500]
            r = DemoRetriever()
            r.build_index(local)
            db_retrievers[ex.db_id] = r

    # Load model once
    print("Loading model...")
    model = StudentModel()
    print(f"  Device: {model.device}")

    # Run predictions
    results = []
    ex_total, em_total = 0, 0

    for i, ex in enumerate(tqdm(dev_subset, desc="Evaluating")):
        retriever = db_retrievers[ex.db_id]
        demos = retriever.retrieve(ex.question, k=args.k)
        schema_ddl = db_to_ddl(ex.db_path)
        prompt = build_prompt(ex.question, schema_ddl, demos)

        predicted = model.generate(prompt)
        ex_pass = score_ex(predicted, ex.query, ex.db_path)
        em_pass = score_em(predicted, ex.query)
        ex_total += ex_pass
        em_total += em_pass

        results.append({
            "idx": i,
            "db_id": ex.db_id,
            "question": ex.question,
            "gold": ex.query,
            "predicted": predicted,
            "ex": ex_pass,
            "em": em_pass,
        })

    n = len(dev_subset)
    summary = {
        "n": n,
        "k": args.k,
        "ex": round(ex_total / n, 4),
        "em": round(em_total / n, 4),
        "device": model.device,
    }

    Path("experiments/results").mkdir(parents=True, exist_ok=True)
    out_path = "experiments/results/p0_eval50.json"
    with open(out_path, "w") as f:
        json.dump({"summary": summary, "results": results}, f, indent=2)

    print("\n=== P0 Batch Eval Results ===")
    print(f"  EX: {summary['ex']:.1%}  ({ex_total}/{n})")
    print(f"  EM: {summary['em']:.1%}  ({em_total}/{n})")
    print(f"  Saved to {out_path}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run batch eval**

```bash
uv run python experiments/p0_eval50.py --n 50 --k 3
```

Expected: EX between 30–60% on Spider dev (Light-SQL [4] gets ~41% on CORDIS; Spider is standard and harder). Any non-zero EX confirms the pipeline works.

If EX < 5%: check that `db_path` in `SpiderExample` points to an actual `.db` file (HuggingFace may store DBs differently — check `dev[0].db_path`).

- [ ] **Step 3: Record results in TODO**

Open `paper/notes/todo.md` and mark completed items under P0 with actual results. Example:
```
- [x] Reproduce sanity: run 1 question → SQL → score EX. Pipeline single-client done
- [x] Verify: EX/EM reasonable on ~50 Spider dev → EX=XX%, EM=XX% (2026-06-08, k=3, Phi-3-mini MPS float16)
```

- [ ] **Step 4: Final commit**

```bash
git add experiments/p0_eval50.py experiments/results/
git commit -m "feat(experiments): P0 batch eval 50 Spider dev questions; EX=XX% EM=XX%"
```

---

## All tests green check

```bash
uv run pytest tests/ -v --tb=short
```

Expected: 18+ passed, 0 failed.

---

## P0 complete checklist

- [ ] `uv run pytest tests/ -v` → all pass
- [ ] `uv run python experiments/p0_sanity.py` → prints EX/EM for 1 question
- [ ] `uv run python experiments/p0_eval50.py` → EX/EM printed + saved to JSON
- [ ] TODO `P0` items marked `[x]` with actual metrics
- [ ] Git log shows 7 commits: skeleton → data → retrieval → prompts → eval → model → sanity → eval50
