"""Fill the results block of paper/notes/overview.html from committed evaluations.

Reads every evaluation under fedicl-sql/experiments/eval_arms/results, maps each
arm to (dataset, line, round) with ARMS below, recounts the wrong rows from the
prediction CSV (execution error incl. cut output, wrong result), computes the
exact McNemar test of every row against FedAvg SFT at the same round, and of the
pairs in TESTS, and writes the result as JSON between the RESULTS markers of the
page. A new evaluation needs one line in ARMS; a new model or seed is picked up
from the metrics file. Test-suite accuracy is read from the committed audits under
audits/protocol_v2/test_suite (field ts of a run, tsfixed/tsbroke/tsp of a test). The page draws the sets of DATASET_OF_SET: Spider test, Spider
dev, Spider-Syn, Spider-Realistic, Spider-DK and BIRD dev (by official difficulty).

    python3 paper/notes/tools/overview_results.py          # write the page
    python3 paper/notes/tools/overview_results.py --check  # print, write nothing
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import subprocess
import sys
from math import comb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CODE = ROOT / "fedicl-sql"
RESULTS = CODE / "experiments" / "eval_arms" / "results"
PAGE = ROOT / "paper" / "notes" / "overview.html"

# arm name (prediction CSV stem without _vllm_inproc) -> (line, round or epoch)
ARMS = {
    "zs_ddl_rows": ("base", 0),
    "fedavg_ddl_rows_a01_r1": ("fedavg", 1),
    "fedavg_ddl_rows_a01_r2": ("fedavg", 2),
    "fedavg_ddl_rows_a01_r3": ("fedavg", 3),
    "fedavg_ddl_rows_a01_r4": ("fedavg", 4),
    "fedpref_base_p2_dpo_ddl_rows_a01_r1": ("k0", 1),
    "fedpref_base_p2_dpo_ddl_rows_a01_r2": ("k0", 2),
    "fedpref_base_p2_dpo_ddl_rows_a01_r3": ("k0", 3),
    "fedpref_base_p2_dpo_ddl_rows_a01_r4": ("k0", 4),
    "fedpref_base_p2_goldrule_dpo_ddl_rows_a01_r1": ("k0gold", 1),
    "fedpref_base_p2_goldrule_dpo_ddl_rows_a01_r2": ("k0gold", 2),
    "fedpref_sftr2_dpo_ddl_rows_a01_r1": ("k2", 3),
    "fedpref_sftr2_dpo_ddl_rows_a01_r2": ("k2", 4),
    "fedpref_sft_dpo_ddl_rows_a01_r1": ("k3", 4),
    "fedpref_sftr2_fixed_dpo_ddl_rows_a01_r1": ("fixed", 3),
    "fedpref_sftr2_fixed_dpo_ddl_rows_a01_r2": ("fixed", 4),
    "fedpref_sftr2_nonll_dpo_ddl_rows_a01_r1": ("feddpo", 3),
    "fedpref_sftr2_rft_ddl_rows_a01_r1": ("rft", 3),
    "fedpref_sftr2_nearest_dpo_ddl_rows_a01_r1": ("nearest", 3),
    "fedpref_sftr2_goldchosen_dpo_ddl_rows_a01_r1": ("goldchosen", 3),
    "fedpref_sftr2_wrfirst_dpo_ddl_rows_a01_r1": ("wrfirst", 3),
    "fedpref_sftr2_rand1wr2_dpo_ddl_rows_a01_r2": ("wrfirst", 4),
    "central_ddl_rows_e1": ("central", 1),
    "central_ddl_rows_e2": ("central", 2),
    "central_ddl_rows_e3": ("central", 3),
    "zs_bird_ddl": ("base", 0),
    "fedavg_bird_ddl_a01_r1": ("fedavg", 1),
    "fedavg_bird_ddl_a01_r2": ("fedavg", 2),
    "fedpref_bird_base_p2_dpo_ddl_a01_r1": ("k0", 1),
    "fedavg_bird_ddl_a01_r3": ("fedavg", 3),
    "fedpref_bird_base_p2_dpo_ddl_a01_r2": ("k0", 2),
    "fedpref_bird_base_p2_goldrule_dpo_ddl_a01_r1": ("k0gold", 1),
    "fedpref_bird_base_p2_goldnll_dpo_ddl_a01_r2": ("k0goldnll", 2),
    "fedpref_bird_base_p2_fixed_dpo_ddl_a01_r2": ("k0fixed", 2),
    "fedpref_bird_sftr1_p2_dpo_ddl_a01_r1": ("k1", 2),
    "fedpref_bird_sftr2_p2_dpo_ddl_a01_r1": ("k2", 3),
    "fedpref_bird_sftr2_p2_dpo_ddl_a01_r2": ("k2", 4),
    "fedavg_bird_ddl_a01_r4": ("fedavg", 4),
    # round 2 of bird_k2 on round 1's pairs and reference (the on-policy ablation at k = 2)
    "fedpref_bird_sftr2_p2_fixed_dpo_ddl_a01_r2": ("fixed", 4),
    # NLL on the correct samples alone, round 1 from FedAvg SFT round 2 (the preference-term ablation)
    "fedpref_bird_sftr2_p2_rft_ddl_a01_r1": ("rft", 3),
    "fedavg_ddl_rows_a01_r5": ("fedavg", 5),
    # strict labels on 10 database variants: databases with rows only (strict), and with the
    # databases without rows paired under the rule `differs` (strictd)
    "fedpref_sftr2_strict10_dpo_ddl_rows_a01_r1": ("strict", 3),
    "fedpref_sftr2_strict10ed_dpo_ddl_rows_a01_r1": ("strictd", 3),
}
# the client adapters of the first DPO + NLL round of k = 2 averaged again by question count
# (reaggq) and with equal weights (reagge); the round itself is weighted by pair count
for _w, _l in (("questions", "reaggq"), ("equal", "reagge")):
    ARMS[f"fedpref_sftr2_reagg_{_w}_dpo_ddl_rows_a01_r1"] = (_l, 3)
    ARMS[f"fedpref_bird_sftr2_p2_reagg_{_w}_dpo_ddl_a01_r1"] = (_l, 3)
# the other student models on Spider test: the line of the 1.5B with the model changed
for _m in ("qwen05b", "deepseek13b"):
    ARMS[f"zs_{_m}_ddl_rows"] = ("base", 0)
    for _r in (1, 2, 3, 4):
        ARMS[f"fedavg_{_m}_ddl_rows_a01_r{_r}"] = ("fedavg", _r)
    ARMS[f"fedpref_{_m}_sftr2_p2_dpo_ddl_rows_a01_r1"] = ("k2", 3)
    ARMS[f"fedpref_{_m}_sftr2_p2_dpo_ddl_rows_a01_r2"] = ("k2", 4)
# the 0.5B from later starts: one DPO + NLL round from FedAvg SFT round 4 and round 6,
# and FedAvg SFT to round 7
for _r in (5, 6, 7):
    ARMS[f"fedavg_qwen05b_ddl_rows_a01_r{_r}"] = ("fedavg", _r)
ARMS["fedpref_qwen05b_sftr4_p2_dpo_ddl_rows_a01_r1"] = ("k4", 5)
ARMS["fedpref_qwen05b_sftr6_p2_dpo_ddl_rows_a01_r1"] = ("k6", 7)
# the two DPO + NLL rounds of k = 2 with the five clients pooled into one (no aggregation)
ARMS["fedpref_pooled_sftr2_p2_dpo_ddl_rows_r1"] = ("pooled", 3)
ARMS["fedpref_pooled_sftr2_p2_dpo_ddl_rows_r2"] = ("pooled", 4)
ARMS["fedpref_sftr2_nearest_dpo_ddl_rows_a01_r2"] = ("nearest", 4)
# prompt B, kept in the notes only; zs_dsc13b: DeepSeek with a tokenizer that dropped
# every space and newline (fixed in code 58cd89f7), not a result
SKIP = {"zs_ddl_values", "zs_dsc13b_ddl_rows"}

# extra pairs (dataset, line a, round a, line b, round b): b measured against a
TESTS = [
    ("spider", "k2", 3, "feddpo", 3),
    ("spider", "k2", 3, "rft", 3),
    ("spider", "k2", 3, "nearest", 3),
    ("spider", "k2", 3, "goldchosen", 3),
    ("spider", "k2", 3, "wrfirst", 3),
    ("spider", "k2", 4, "wrfirst", 4),
    ("spider", "fixed", 4, "k2", 4),
    ("spider", "k0", 4, "k2", 4),
    ("spider", "k0", 4, "k3", 4),
    ("spider", "k0", 1, "k0gold", 1),
    ("spider", "k0", 2, "k0gold", 2),
    ("spider", "fedavg", 2, "feddpo", 3),
    ("spider", "central", 2, "k0", 2),
    ("spider", "central", 2, "fedavg", 2),
    ("bird", "base", 0, "fedavg", 1),
    ("bird", "fedavg", 1, "fedavg", 2),
    ("bird", "fedavg", 2, "k0", 1),
    ("bird", "fedavg", 1, "k1", 2),
    ("spider", "central", 3, "k0", 3),
    ("spider", "central", 2, "central", 3),
    ("bird", "fedavg", 2, "fedavg", 3),
    ("bird", "fedavg", 3, "k1", 2),
    ("bird", "k0", 1, "k0", 2),
    ("bird", "k0", 2, "k1", 2),
    ("bird", "k0fixed", 2, "k0", 2),
    ("bird", "k0", 1, "k0gold", 1),
    ("bird", "k0", 2, "k0goldnll", 2),
    ("bird", "k1", 2, "k0goldnll", 2),
    ("bird", "fedavg", 3, "fedavg", 4),
    ("bird", "fedavg", 4, "k2", 3),
    ("bird", "fedavg", 2, "k2", 3),
    ("bird", "k1", 2, "k2", 3),
    ("bird", "k0", 2, "k2", 3),
    ("spider", "base", 0, "fedavg", 1),
    ("spider", "fedavg", 1, "fedavg", 2),
    ("spider", "fedavg", 2, "fedavg", 3),
    ("spider", "fedavg", 2, "k2", 3),
    ("spider", "fedavg", 3, "fedavg", 4),
    ("spider", "k2", 3, "k2", 4),
    ("spider", "fedavg", 4, "fedavg", 5),
    ("spider", "fedavg", 4, "k4", 5),
    ("spider", "fedavg", 6, "k6", 7),
    ("spider", "fedavg", 6, "fedavg", 7),
    ("spider", "fedavg", 6, "k2", 4),
    ("spider", "fedavg", 7, "k2", 4),
    ("spider", "k2", 3, "k4", 5),
    ("spider", "k2", 4, "k6", 7),
    ("spider", "k2", 3, "pooled", 3),
    ("spider", "k2", 4, "pooled", 4),
    ("spiderdev", "fedavg", 4, "k4", 5),
    ("spiderdev", "fedavg", 6, "k6", 7),
    ("spiderdev", "k2", 3, "k2", 4),
    ("spiderdev", "k0", 4, "k2", 4),
    ("spiderdev", "central", 2, "k2", 4),
    # the paper tables: the method against its ablations and against FedAvg SFT at other rounds
    ("bird", "fixed", 4, "k2", 4),
    ("bird", "k2", 3, "k2", 4),
    ("bird", "fedavg", 3, "k2", 4),
    ("bird", "rft", 3, "k2", 3),
    ("bird", "feddpo", 3, "k2", 3),
    ("bird", "feddpo", 4, "k2", 4),
    ("bird", "rft", 4, "k2", 4),
    ("bird", "central", 3, "k2", 4),
    ("spider", "feddpo", 4, "k2", 4),
    ("spider", "rft", 4, "k2", 4),
    ("spider", "k3", 4, "k2", 4),
    ("spider", "fedavg", 5, "k2", 4),
    ("spider", "central", 3, "k2", 4),
    ("spiderdev", "fedavg", 4, "fedavg", 5),
    ("spiderdev", "fedavg", 5, "k2", 4),
    ("spiderdev", "k3", 4, "k2", 4),
    ("spiderdev", "rft", 3, "k2", 3),
    ("spiderdev", "feddpo", 3, "k2", 3),
    ("spiderdev", "feddpo", 4, "k2", 4),
    ("spiderdev", "rft", 4, "k2", 4),
    ("spiderdev", "fedavg", 2, "rft", 3),
    ("spiderdev", "fedavg", 2, "feddpo", 3),
] + [t for ds in ("spider", "spiderdev", "bird") for t in (
    (ds, "k2", 3, "reaggq", 3),
    (ds, "k2", 3, "reagge", 3),
)] + [t for ds in ("spider", "spiderdev") for t in (
    (ds, "k2", 3, "strict", 3),
    (ds, "k2", 3, "strictd", 3),
)] + [t for ds in ("spiderdev", "syn", "realistic", "dk") for t in (
    (ds, "base", 0, "fedavg", 4),
    (ds, "fixed", 4, "k2", 4),
    (ds, "k0", 4, "k2", 4),
    (ds, "central", 2, "k0", 4),
    (ds, "central", 2, "k2", 4),
)]

# the sets the page draws (the `eval_set` of a metrics file); an arm keeps its name on every set
DATASET_OF_SET = {
    "processed_data/SPIDER_TEST/test.csv": "spider",
    "processed_data/protocol_v2/SPIDER/processed_train8659_dev1034/centralized/test.csv": "spiderdev",
    "processed_data/SPIDER_SYN/test.csv": "syn",
    "processed_data/SPIDER_REALISTIC/test.csv": "realistic",
    "processed_data/SPIDER_DK/test.csv": "dk",
    "processed_data/protocol_v2/BIRD/original_train9428_dev1534/centralized/test.csv": "bird",
}
# BIRD dev is read by its official difficulty (dev.json, same row order as the evaluation
# file; row_id is the index), the Spider sets by the Spider hardness of the prediction CSV
BIRD_DEV_JSON = CODE / "data" / "raw" / "bird" / "dev_20240627" / "dev.json"
LEVELS = {"bird": (("simple", "s"), ("moderate", "mo"), ("challenging", "c"))}
SPIDER_LEVELS = (("easy", "e"), ("medium", "m"), ("hard", "h"), ("extra", "x"))
# test-suite accuracy (Zhong et al., EMNLP 2020), scored on the Mac from the committed predictions:
# each summary.json names the prediction file of every row it scored
TEST_SUITE = CODE / "audits" / "protocol_v2" / "test_suite"
MODEL_SHORT = {"Qwen/Qwen2.5-Coder-1.5B-Instruct": "qwen15", "Qwen/Qwen2.5-Coder-0.5B-Instruct": "qwen05",
               "deepseek-ai/deepseek-coder-1.3b-instruct": "dsc13"}


def mcnemar(wins: int, losses: int) -> float:
    n = wins + losses
    if n == 0:
        return 1.0
    return min(1.0, 2 * sum(comb(n, k) for k in range(min(wins, losses) + 1)) / 2**n)


def p_text(p: float) -> str:
    if p < 1e-3:
        return f"{p:.1e}".replace("e-0", "e-")
    return f"{p:.2g}" if p < 0.1 else f"{p:.2f}"


def failure(row: dict) -> str | None:
    if int(row["ex"]):
        return None
    if row.get("finish_reason") == "length":
        return "cut"
    return "exec_error" if row.get("exec_error") else "wrong_result"


def commit_of(path: Path) -> str:
    out = subprocess.run(["git", "log", "--diff-filter=A", "--format=%h", "-1", "--", str(path.relative_to(CODE))],
                         cwd=CODE, capture_output=True, text=True, check=True).stdout.strip()
    return out[:8]


def bird_difficulty() -> list[str]:
    return [q["difficulty"] for q in json.loads(BIRD_DEV_JSON.read_text(encoding="utf-8"))]


def test_suite() -> dict:
    """(results dir, prediction CSV name) -> {row_id: 0 or 1}, test-suite correct."""
    out = {}
    for summary in sorted(TEST_SUITE.glob("*/summary.json")):
        d = json.loads(summary.read_text(encoding="utf-8"))
        with open(summary.parent / "per_question.csv", encoding="utf-8", newline="") as h:
            table = list(csv.DictReader(h))
        for name, src in d["sources"].items():
            path = Path(src["path"])
            key = (path.parts[-3], path.name)
            score = {row["row_id"]: int(row[f"{name}_ts"]) for row in table}
            # one prediction file may be scored in several audits; the scores must agree
            if key in out and out[key] != score:
                raise SystemExit(f"two different test-suite scores for {key}")
            out[key] = score
            ts = round(100 * sum(out[key].values()) / len(out[key]), 2)
            if abs(ts - d["accuracy"][name]["ts_ex"]) > 0.006:
                raise SystemExit(f"{summary.parent.name} {name}: TS {ts} against {d['accuracy'][name]['ts_ex']}")
    return out


def load() -> tuple[list[dict], dict, dict]:
    runs, rows_of, ts_of = [], {}, {}
    bird_dev = None
    suite = test_suite()
    for metrics in sorted(RESULTS.glob("*/metrics.json")):
        d = json.loads(metrics.read_text(encoding="utf-8"))
        ds = DATASET_OF_SET.get(Path(d.get("eval_set", "")).as_posix())
        if ds is None:
            continue
        model = MODEL_SHORT.get(d.get("model"), d.get("model"))
        for arm, a in d["arms"].items():
            stem = arm.removesuffix("_vllm_inproc")
            if stem in SKIP:
                continue
            if stem not in ARMS:
                print(f"not mapped, left out: {arm} ({metrics.parent.name})", file=sys.stderr)
                continue
            line, r = ARMS[stem]
            with open(metrics.parent / "predictions" / f"{arm}.csv", encoding="utf-8", newline="") as h:
                rows = {row["row_id"]: row for row in csv.DictReader(h)}
            kinds = [failure(row) for row in rows.values()]
            n = len(rows)
            ex = round(100 * sum(int(row["ex"]) for row in rows.values()) / n, 2)
            if abs(ex - 100 * a["ex"]) > 0.006:
                raise SystemExit(f"{arm}: EX {ex} from the CSV against {a['ex']} in metrics.json")
            if ds == "bird":
                bird_dev = bird_dev or bird_difficulty()
                if len(bird_dev) != n:
                    raise SystemExit(f"{arm}: {n} rows against {len(bird_dev)} in dev.json")
                level_of = {i: bird_dev[int(i)] for i in rows}
            else:
                level_of = {i: row.get("hardness") for i, row in rows.items()}
            hard = {}
            for name, key in LEVELS.get(ds, SPIDER_LEVELS):
                sub = [rows[i] for i in rows if level_of[i] == name]
                hard[key] = round(100 * sum(int(x["ex"]) for x in sub) / len(sub), 2) if sub else None
            run = {"ds": ds, "model": model, "seed": int(d.get("seed", 0)), "line": line, "r": r, "n": n, "ex": ex,
                   **hard,
                   "err": sum(k in ("exec_error", "cut") for k in kinds), "cut": sum(k == "cut" for k in kinds),
                   "wr": sum(k == "wrong_result" for k in kinds), "sha": commit_of(metrics)}
            key = (ds, model, run["seed"], line, r)
            if key in rows_of:
                raise SystemExit(f"two evaluations for {key}")
            rows_of[key] = rows
            ts = suite.pop((metrics.parent.name, f"{arm}.csv"), None)
            if ts is not None:
                if set(ts) != set(rows):
                    raise SystemExit(f"{arm}: test-suite rows differ from the predictions")
                run["ts"] = round(100 * sum(ts.values()) / n, 2)
                ts_of[key] = ts
            runs.append(run)
    if suite:
        print(f"test-suite scores of unmapped rows, left out: {sorted(suite)}", file=sys.stderr)
    return runs, rows_of, ts_of


def test(rows_of: dict, ts_of: dict, a: tuple, b: tuple) -> dict | None:
    if a not in rows_of or b not in rows_of:
        return None
    ra, rb = rows_of[a], rows_of[b]
    if set(ra) != set(rb):
        raise SystemExit(f"{a} and {b} were not evaluated on the same rows")
    fixed = sum(1 for i in ra if not int(ra[i]["ex"]) and int(rb[i]["ex"]))
    broke = sum(1 for i in ra if int(ra[i]["ex"]) and not int(rb[i]["ex"]))
    p = mcnemar(fixed, broke)
    t = {"ds": a[0], "model": a[1], "seed": a[2], "a": a[3], "ra": a[4], "b": b[3], "rb": b[4],
         "fixed": fixed, "broke": broke, "p": p_text(p), "pv": float(f"{p:.3g}")}
    if a in ts_of and b in ts_of:
        ta, tb = ts_of[a], ts_of[b]
        fixed = sum(1 for i in ta if not ta[i] and tb[i])
        broke = sum(1 for i in ta if ta[i] and not tb[i])
        p = mcnemar(fixed, broke)
        t.update({"tsfixed": fixed, "tsbroke": broke, "tsp": p_text(p)})
    return t


def build() -> dict:
    runs, rows_of, ts_of = load()
    tests = []
    for (ds, model, seed, line, r) in sorted(rows_of):
        if line in ("fedavg", "base", "central"):
            continue
        t = test(rows_of, ts_of, (ds, model, seed, "fedavg", r), (ds, model, seed, line, r))
        if t:
            tests.append(t)
    seeds = sorted({(x["ds"], x["model"], x["seed"]) for x in runs})
    for ds, la, ra, lb, rb in TESTS:
        for d_, model, seed in seeds:
            if d_ == ds:
                t = test(rows_of, ts_of, (ds, model, seed, la, ra), (ds, model, seed, lb, rb))
                if t:
                    tests.append(t)
    order = {k: i for i, k in enumerate(["base", "fedavg", "k0", "k0gold", "k0goldnll", "k0fixed", "k1", "k2", "k3", "k4", "k6", "pooled", "fixed", "feddpo", "rft",
                                          "nearest", "goldchosen", "wrfirst", "strict", "strictd", "reaggq", "reagge", "central"])}
    runs.sort(key=lambda x: (x["ds"], x["model"], order.get(x["line"], 99), x["r"], x["seed"]))
    return {"runs": runs, "tests": tests}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    data = build()
    text = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    text = text.replace('},{"ds"', '},\n{"ds"')
    if args.check:
        print(text)
        return
    page = PAGE.read_text(encoding="utf-8")
    new, n = re.subn(r"(/\* RESULTS:BEGIN[^\n]*\*/\n).*?(\n/\* RESULTS:END \*/)",
                     lambda m: m.group(1) + "var DATA = " + text + ";" + m.group(2), page, flags=re.S)
    if n != 1:
        raise SystemExit("RESULTS markers not found once in the page")
    PAGE.write_text(new, encoding="utf-8")
    print(f"{len(data['runs'])} runs, {len(data['tests'])} tests written to {PAGE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
