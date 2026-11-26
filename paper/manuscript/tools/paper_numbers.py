#!/usr/bin/env python3
"""Write the result numbers of the paper from the committed evaluations.

Every number comes from `load()` and `test()` of paper/notes/tools/overview_results.py,
the functions that fill the overview page, so a cell of the paper and the same cell of
the page are one value. A row enters by one line in ARMS of that script.

Writes, under paper/manuscript/generated/:
  numbers.tex   one macro per cell and per test the paper prints
  numbers.md    the same macros with their values and result commits (for the briefs)
  tab_*.tex     the tabular of each table (Tables 2 to 8); captions are the writer's
  missing.txt   the rows a table needs that are not committed

    python3 tools/paper_numbers.py            # write the files
    python3 tools/paper_numbers.py --check    # also compare every cell with overview.html
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUSCRIPT = HERE.parent
ROOT = MANUSCRIPT.parents[1]
CODE = ROOT / "fedicl-sql"
GEN = MANUSCRIPT / "generated"
sys.path.insert(0, str(ROOT / "paper" / "notes" / "tools"))
import overview_results as ov  # noqa: E402

MAIN = "qwen15"
MODEL_NAME = {"qwen15": "Qwen2.5-Coder-1.5B", "qwen05": "Qwen2.5-Coder-0.5B", "dsc13": "DeepSeek-Coder-1.3B"}
SET_NAME = {"bird": "BIRD dev", "spider": "Spider test", "spiderdev": "Spider dev", "syn": "Spider-Syn",
            "realistic": "Spider-Realistic", "dk": "Spider-DK"}
LEVELS = {"bird": (("simple", "s"), ("moderate", "mo"), ("challenging", "c"))}
SPIDER_LEVELS = (("easy", "e"), ("medium", "m"), ("hard", "h"), ("extra", "x"))
ALPHA = 0.05  # level of the star, after the Holm correction
MISSING = "--"
TABCOLSEP = "3.5pt"  # the text is 131 mm wide; the default padding overfills it

# Rows of the paper. A cell is (set, model, seed, line, round); the line names are those of
# ARMS in overview_results.py. Lines that no evaluation carries yet keep the names below:
#   local1 .. local5   local SFT of each client, 3 epochs
#   fedprox            FedProx SFT
#   fedavg_iid, k2_iid, fedavg_a05, k2_a05, fedavg_a05k10, k2_a05k10   the other Spider setups
ROUNDS = 4          # total rounds of the main rows
WARMUP = 2          # FedAvg SFT rounds before the preference rounds
EPOCHS = 3          # centralized and local SFT
LOCAL = [f"local{c}" for c in range(1, 6)]

# Comparisons the text may quote that no table carries: (set, model, line a, round a, line b, round b),
# read b against a. Each is a claim of CLAIMS.md.
TEXT_TESTS = [
    ("bird", MAIN, "fedavg", 3, "k2", 4),      # the method against the best FedAvg SFT round
    ("bird", MAIN, "fedavg", 3, "k2", 3),      # at 3 rounds
    ("spider", MAIN, "fedavg", 3, "k2", 3),
    ("bird", MAIN, "fedavg", 2, "k2", 3),      # the first preference round against its start
    ("spider", MAIN, "fedavg", 2, "k2", 3),
    ("bird", MAIN, "k2", 3, "k2", 4),          # the second preference round
    ("spider", MAIN, "k2", 3, "k2", 4),
    ("bird", MAIN, "fedavg", 2, "fedavg", 3),  # what a third and a fourth SFT round add
    ("bird", MAIN, "fedavg", 3, "fedavg", 4),
    ("spider", MAIN, "fedavg", 2, "fedavg", 3),
    ("spider", MAIN, "fedavg", 3, "fedavg", 4),
    ("spider", MAIN, "fedavg", 4, "fedavg", 5),
    ("spider", MAIN, "fedavg", 5, "k2", 4),
]
# Curves of Fig. 2 and Fig. 3: (line, rounds) per set; the method continues FedAvg SFT round WARMUP.
CURVES = {
    "bird": {"fedavg": [0, 1, 2, 3, 4], "k2": [3, 4]},
    "spider": {"fedavg": [0, 1, 2, 3, 4, 5], "k2": [3, 4]},
}


# ---------------------------------------------------------------- formatting
def f2(v: float) -> str:
    return f"{v:.2f}"


def count(n: int) -> str:
    return f"{n:,}".replace(",", "{,}")


def signed(d: float) -> str:
    return f"+{d:.2f}" if d >= 0 else f"$-${-d:.2f}"


def p_tex(p: float) -> str:
    s = ov.p_text(p)
    m = re.fullmatch(r"(\d(?:\.\d)?)e-(\d+)", s)
    return f"${m.group(1)}\\times10^{{-{m.group(2)}}}$" if m else s


def holm(ps: dict) -> dict:
    """Holm-adjusted p of every test of one family (key -> exact p)."""
    order = sorted(ps, key=lambda k: ps[k])
    m, out, running = len(order), {}, 0.0
    for i, k in enumerate(order):
        running = max(running, min(1.0, (m - i) * ps[k]))
        out[k] = running
    return out


# ---------------------------------------------------------------- data
class Data:
    def __init__(self) -> None:
        runs, self.rows_of, self.ts_of = ov.load()
        self.runs = {(x["ds"], x["model"], x["seed"], x["line"], x["r"]): x for x in runs}
        self.used_runs: dict = {}    # key -> tables
        self.used_tests: dict = {}   # (a, b) -> tables
        self.missing: dict = {}      # key -> tables
        self._tests: dict = {}
        self._pending: list = []     # p cells, written once the Holm family is complete

    def defer(self, a: tuple, b: tuple, kind: str) -> str:
        self._pending.append((a, b, kind))
        return f"<<P{len(self._pending) - 1}>>"

    def resolve(self, text: str) -> str:
        def cell(m: re.Match) -> str:
            a, b, kind = self._pending[int(m.group(1))]
            t = self._tests[(a, b)]
            p, adj = (t["pexact"], t["padj"]) if kind == "ex" else (t["tspexact"], t["tspadj"])
            return p_tex(p) + ("\\textsuperscript{*}" if adj < ALPHA else "")
        return re.sub(r"<<P(\d+)>>", cell, text)

    def run(self, key: tuple, where: str) -> dict | None:
        x = self.runs.get(key)
        if x is None:
            self.missing.setdefault(key, []).append(where)
            return None
        self.used_runs.setdefault(key, []).append(where)
        return x

    def test(self, a: tuple, b: tuple, where: str) -> dict | None:
        """b against a (fixed: wrong under a and right under b), None when a row is missing."""
        if a not in self.runs or b not in self.runs:
            return None
        if (a, b) not in self._tests:
            t = ov.test(self.rows_of, self.ts_of, a, b)
            t["pexact"] = ov.mcnemar(t["fixed"], t["broke"])
            t["d"] = round(self.runs[b]["ex"] - self.runs[a]["ex"], 2)
            if "tsfixed" in t:
                t["tspexact"] = ov.mcnemar(t["tsfixed"], t["tsbroke"])
                t["dts"] = round(self.runs[b]["ts"] - self.runs[a]["ts"], 2)
            self._tests[(a, b)] = t
        self.used_tests.setdefault((a, b), []).append(where)
        return self._tests[(a, b)]

    def adjust(self) -> None:
        """Holm inside each table: the tests of a table answer one question and form one family.

        A test is counted once, in the first table that prints it (the main rows come back in
        Tables 4 and 5); the comparisons quoted in the text only form a family of their own.
        A test-suite test belongs to the table that prints it."""
        families: dict = {}
        for (a, b), where in self.used_tests.items():
            t = self._tests[(a, b)]
            families.setdefault(family_of(where), {})[(a, b, "ex")] = t["pexact"]
            ts = [w for w in where if w.endswith(":ts")]
            if "tspexact" in t and ts:
                families.setdefault(family_of(ts), {})[(a, b, "ts")] = t["tspexact"]
        self.families = {name: len(tests) for name, tests in sorted(families.items())}
        for tests in families.values():
            for (a, b, kind), v in holm(tests).items():
                self._tests[(a, b)]["padj" if kind == "ex" else "tspadj"] = v


def family_of(where: list[str]) -> str:
    """The first table that prints a test; "text" for a comparison no table carries."""
    tables = sorted({w.removesuffix(":ts").split(",")[0] for w in where if w.startswith("Table")})
    return tables[0] if tables else "text"


def key(ds: str, line: str, r: int, model: str = MAIN, seed: int = 0) -> tuple:
    return (ds, model, seed, line, r)


# ---------------------------------------------------------------- tables
def tabular(spec: str, lines: list[str], sep: str = TABCOLSEP) -> str:
    return "\\setlength{\\tabcolsep}{" + sep + "}%\n\\begin{tabular}{" + spec + "}\n" + "\n".join(lines) + "\n\\end{tabular}\n"


def row(cells: list[str]) -> str:
    return " & ".join(cells) + " \\\\"


def bold(s: str) -> str:
    return "\\textbf{" + s + "}"


def best_of(values: list) -> float | None:
    vals = [v for v in values if v is not None]
    return max(vals) if len(vals) > 1 else None


def ex_cells(d: Data, ds: str, rows: list[dict], where: str) -> list[list[str]]:
    """EX and level cells of the rows of one set, the best value of each column in bold
    (rows marked ref are read and not ranked)."""
    levels = LEVELS.get(ds, SPIDER_LEVELS)
    cols = ["ex"] + [k for _, k in levels]
    got = [None if r_.get("key") is None else d.run(r_["key"], where) for r_ in rows]
    best = {c: best_of([x[c] if x and not r_.get("ref") else None for x, r_ in zip(got, rows)]) for c in cols}
    out = []
    for x, r_ in zip(got, rows):
        if x is None:
            out.append([MISSING] * len(cols))
            continue
        out.append([bold(f2(x[c])) if not r_.get("ref") and best[c] is not None and abs(x[c] - best[c]) < 1e-9
                    else f2(x[c]) for c in cols])
    return out


def diff_cells(d: Data, a: tuple, b: tuple, where: str) -> list[str]:
    """Difference of b over a and the p of the exact McNemar test, starred after Holm."""
    t = d.test(a, b, where)
    if t is None:
        return [MISSING, MISSING]
    return [signed(t["d"]), d.defer(a, b, "ex")]


def local_cells(d: Data, ds: str, where: str) -> list[str] | None:
    """Local SFT: mean over the clients, with the lowest and highest client."""
    got = [d.run(key(ds, line, EPOCHS), where) for line in LOCAL]
    if any(x is None for x in got):
        return None
    levels = LEVELS.get(ds, SPIDER_LEVELS)
    ex = [x["ex"] for x in got]
    cells = [f"{sum(ex) / len(ex):.2f} ({min(ex):.2f}--{max(ex):.2f})"]
    cells += [f2(sum(x[k] for x in got) / len(got)) for _, k in levels]
    return cells


def table_main(d: Data) -> str:
    """Table 3: the main rows on BIRD dev and Spider test at ROUNDS rounds."""
    lines = ["\\toprule"]
    for ds in ("bird", "spider"):
        where = f"Table 3, {SET_NAME[ds]}"
        levels = LEVELS.get(ds, SPIDER_LEVELS)
        pad = [""] * (4 - len(levels))
        fed = key(ds, "fedavg", ROUNDS)
        rows = [
            {"name": "No training", "key": key(ds, "base", 0), "ref": True},
            {"name": "Local SFT", "local": True, "ref": True},
            {"name": "Centralized SFT", "key": key(ds, "central", EPOCHS), "ref": True},
            {"name": "FedAvg SFT", "key": fed, "base": True},
            {"name": "FedProx SFT", "key": key(ds, "fedprox", ROUNDS)},
            {"name": "Federated DPO", "key": key(ds, "feddpo", ROUNDS)},
            {"name": "\\method", "key": key(ds, "k2", ROUNDS)},
        ]
        if ds == "bird":  # the two main rows on a second training seed
            rows += [
                {"name": "FedAvg SFT, second seed", "key": key(ds, "fedavg", ROUNDS, seed=1), "base": True, "ref": True},
                {"name": "\\method, second seed", "key": key(ds, "k2", ROUNDS, seed=1), "ref": True,
                 "against": key(ds, "fedavg", ROUNDS, seed=1)},
            ]
        cells = ex_cells(d, ds, rows, where)
        lines.append(row([SET_NAME[ds], "EX"] + [name.capitalize() for name, _ in levels] + pad + ["$\\Delta$", "$p$"]))
        lines.append("\\midrule")
        for r_, c in zip(rows, cells):
            if r_.get("local"):
                lc = local_cells(d, ds, where)
                c = lc if lc else c
                tail = ["", ""] if lc else [MISSING, MISSING]
            elif r_.get("base"):
                tail = ["", ""]
            else:
                tail = diff_cells(d, r_.get("against", fed), r_["key"], where)
            lines.append(row([r_["name"]] + c + pad + tail))
        lines.append("\\midrule" if ds == "bird" else "\\bottomrule")
    return tabular("@{}lrrrrrrl@{}", lines)


def table_models(d: Data) -> str:
    """Table 4: the other models, FedAvg SFT against the method at ROUNDS rounds."""
    where = "Table 4"
    lines = ["\\toprule", row(["Set", "Model", "No training", "FedAvg SFT", "\\method", "$\\Delta$", "$p$"]), "\\midrule"]
    groups = [("spider", ["qwen15", "qwen05", "dsc13"]), ("bird", ["qwen15", "dsc13"])]
    for gi, (ds, models) in enumerate(groups):
        for mi, m in enumerate(models):
            a, b = key(ds, "fedavg", ROUNDS, model=m), key(ds, "k2", ROUNDS, model=m)
            got = [d.run(key(ds, "base", 0, model=m), where), d.run(a, where), d.run(b, where)]
            cells = [f2(x["ex"]) if x else MISSING for x in got]
            lines.append(row([SET_NAME[ds] if mi == 0 else "", MODEL_NAME[m]] + cells + diff_cells(d, a, b, where)))
        if gi == 0:
            lines.append("\\midrule")
    lines.append("\\bottomrule")
    return tabular("@{}llrrrrl@{}", lines)


SETUPS = [
    # (set, split directory, partition label, FedAvg SFT line, method line)
    ("bird", "BIRD/original_train9428_dev1534/federated/alpha_0.1/k5", "$\\alpha=0.1$", "fedavg", "k2"),
    ("spider", "SPIDER/processed_train8659_dev1034/federated/alpha_0.1/k5", "$\\alpha=0.1$", "fedavg", "k2"),
    ("spider", "SPIDER/processed_train8659_dev1034/federated/alpha_0.5/k5", "$\\alpha=0.5$", "fedavg_a05", "k2_a05"),
    ("spider", "SPIDER/processed_train8659_dev1034/federated/iid/k5", "IID", "fedavg_iid", "k2_iid"),
    ("spider", "SPIDER/processed_train8659_dev1034/federated/alpha_0.5/k10", "$\\alpha=0.5$", "fedavg_a05k10", "k2_a05k10"),
]
TRAIN_NAME = {"bird": "BIRD", "spider": "Spider"}


def split_facts(split: str) -> dict:
    d = CODE / "processed_data" / "protocol_v2" / split
    meta = json.loads((d / "meta.json").read_text(encoding="utf-8"))
    with open(d / "clients.csv", encoding="utf-8", newline="") as h:
        clients = list(csv.DictReader(h))
    q = [int(c["questions"]) for c in clients]
    dbs = [int(c["databases"]) for c in clients]
    hard = [100 * (int(c["hard"]) + int(c["extra"])) / int(c["questions"]) for c in clients]
    if len(clients) != meta["n_clients"] or sum(dbs) != len(meta["db_client"]):
        raise SystemExit(f"{split}: clients.csv and meta.json disagree")
    return {"clients": len(clients), "questions": sum(q), "q_min": min(q), "q_max": max(q), "databases": sum(dbs),
            "db_min": min(dbs), "db_max": max(dbs), "hard_min": min(hard), "hard_max": max(hard), "seed": meta["seed"]}


def table_setups() -> tuple[str, dict]:
    """Table 2: the five federated setups, read from the committed split files."""
    lines = ["\\toprule",
             row(["", "", "", "\\multicolumn{2}{c}{Questions}", "\\multicolumn{2}{c}{Databases}", "Hard or extra"]),
             "\\cmidrule(lr){4-5}\\cmidrule(lr){6-7}",
             row(["Clients' data", "Partition", "Clients", "All", "Per client", "All", "Per client", "(\\%)"]),
             "\\midrule"]
    facts = {}
    for ds, split, label, _, _ in SETUPS:
        f = split_facts(split)
        tag = f"{ds}.{split.split('federated/')[1].replace('/', '.').replace('alpha_', 'a')}"
        for k_, v in f.items():
            facts[f"split.{tag}.{k_}"] = v
        lines.append(row([TRAIN_NAME[ds] + " train", label, str(f["clients"]), count(f["questions"]),
                          f"{count(f['q_min'])}--{count(f['q_max'])}", str(f["databases"]), f"{f['db_min']}--{f['db_max']}",
                          f"{f['hard_min']:.0f}--{f['hard_max']:.0f}"]))
    lines.append("\\bottomrule")
    return tabular("@{}llrrrrrr@{}", lines), facts


def table_federated(d: Data) -> str:
    """Table 5: FedAvg SFT against the method in the five setups at ROUNDS rounds."""
    where = "Table 5"
    lines = ["\\toprule", row(["Clients' data", "Partition", "Clients", "Evaluated on", "FedAvg SFT", "\\method", "$\\Delta$", "$p$"]),
             "\\midrule"]
    for ds, split, label, la, lb in SETUPS:
        f = split_facts(split)
        a, b = key(ds, la, ROUNDS), key(ds, lb, ROUNDS)
        got = [d.run(a, where), d.run(b, where)]
        cells = [f2(x["ex"]) if x else MISSING for x in got]
        lines.append(row([TRAIN_NAME[ds] + " train", label, str(f["clients"]), SET_NAME[ds]] + cells + diff_cells(d, a, b, where)))
    lines.append("\\bottomrule")
    return tabular("@{}llrlrrrl@{}", lines)


def table_robust(d: Data) -> str:
    """Table 6: Spider dev and the perturbed sets, EX and test-suite accuracy, at ROUNDS rounds."""
    cols = [("spiderdev", "ex"), ("spiderdev", "ts"), ("syn", "ex"), ("syn", "ts"), ("realistic", "ex"), ("realistic", "ts"),
            ("dk", "ex")]
    lines = ["\\toprule",
             row(["", "\\multicolumn{2}{c}{Spider dev}", "\\multicolumn{2}{c}{Spider-Syn}", "\\multicolumn{2}{c}{Spider-Realistic}",
                  "Spider-DK"]),
             "\\cmidrule(lr){2-3}\\cmidrule(lr){4-5}\\cmidrule(lr){6-7}\\cmidrule(lr){8-8}",
             row([""] + ["EX" if m == "ex" else "TS" for _, m in cols]),
             "\\midrule"]
    rows = [("No training", "base", 0), ("FedAvg SFT", "fedavg", ROUNDS), ("\\method, no warm-up", "k0", ROUNDS),
            ("\\method", "k2", ROUNDS)]
    for name, line, r in rows:
        cells = []
        for ds, m in cols:
            x = d.run(key(ds, line, r), f"Table 6, {SET_NAME[ds]}" + (":ts" if m == "ts" else ""))
            cells.append(MISSING if x is None or x.get(m) is None else f2(x[m]))
            if x is not None and x.get(m) is None:
                d.missing.setdefault(key(ds, line, r), []).append(f"Table 6, {SET_NAME[ds]}, test-suite accuracy")
        lines.append(row([name] + cells))
    # the method against FedAvg SFT, and against itself without the warm-up rounds
    for label, other in (("against FedAvg SFT", "fedavg"), ("against no warm-up", "k0")):
        deltas, ps = [], []
        for ds, m in cols:
            a, b = key(ds, other, ROUNDS), key(ds, "k2", ROUNDS)
            t = d.test(a, b, f"Table 6, {SET_NAME[ds]}" + (":ts" if m == "ts" else ""))
            if t is None or (m == "ts" and "dts" not in t):
                deltas.append(MISSING), ps.append(MISSING)
            else:
                deltas.append(signed(t["d"] if m == "ex" else t["dts"])), ps.append(d.defer(a, b, m))
        lines.append("\\midrule")
        lines.append(row(["$\\Delta$ " + label] + deltas))
        lines.append(row(["$p$"] + ps))
    lines.append("\\bottomrule")
    return tabular("@{}lrrrrrrr@{}", lines)


def table_ablation(d: Data) -> str:
    """Table 8: the parts of the method, each row against the method at the same rounds."""
    lines = ["\\toprule",
             row(["", "\\multicolumn{3}{c}{BIRD dev}", "\\multicolumn{3}{c}{Spider test}"]),
             "\\cmidrule(lr){2-4}\\cmidrule(lr){5-7}",
             row(["", "EX", "$\\Delta$", "$p$", "EX", "$\\Delta$", "$p$"])]
    blocks = [
        (f"{ROUNDS} rounds: {WARMUP} FedAvg SFT rounds, {ROUNDS - WARMUP} preference rounds", ROUNDS, [
            ("\\method", "k2", None),
            ("Fixed pairs and reference", "fixed", None),
            ("Without the preference term", "rft", None),
            ("No FedAvg SFT round", "k0", None),
            ("Three FedAvg SFT rounds", "k3", None),
            ("Clients pooled", "pooled", ("spider",)),
        ]),
        (f"{ROUNDS - 1} rounds: {WARMUP} FedAvg SFT rounds, {ROUNDS - 1 - WARMUP} preference round", ROUNDS - 1, [
            ("\\method", "k2", None),
            ("Without the NLL term", "feddpo", None),
            ("Without the preference term", "rft", None),
            ("Averaged by question count", "reaggq", None),
            ("Averaged with equal weights", "reagge", None),
        ]),
    ]
    for label, r, rows in blocks:
        lines += ["\\midrule", row([f"\\multicolumn{{7}}{{@{{}}l}}{{\\textit{{{label}}}}}"]), "\\midrule"]
        for name, line, only in rows:
            cells = [name]
            for ds in ("bird", "spider"):
                where = f"Table 8, {SET_NAME[ds]}"
                if only and ds not in only:
                    cells += ["", "", ""]
                    continue
                me, k_ = key(ds, "k2", r), key(ds, line, r)
                x = d.run(k_, where)
                if line == "k2":
                    cells += [f2(x["ex"]) if x else MISSING, "", ""]
                else:
                    cells += [f2(x["ex"]) if x else MISSING] + diff_cells(d, me, k_, where)
            lines.append(row(cells))
    lines.append("\\bottomrule")
    return tabular("@{}lrrlrrl@{}", lines, sep="2pt")


# ---------------------------------------------------------------- cost (Table 7)
FED_RUN = {"bird": "federated__fedavg__s0__7ecd649662f3__5e43d16b", "spider": "federated__fedavg__s0__2dd4b43f7431__74de6d4f"}
PREF_AUDIT = {"bird": "fedpref_bird_sftr2_p2_ddl_alpha01_s0", "spider": "fedpref_sftr2_ddlrows_alpha01_s0"}
PREF_TIMES = {"spider": "dpo_k2"}  # rounds timed from the queue logs (scripts/log_times.py)


def cost_facts() -> dict:
    """Seconds of a round on one RTX A5000, the five clients one after another, and the bytes
    a client sends: from the round records, or from the queue logs where a record has no timing."""
    out = {}
    for ds in ("bird", "spider"):
        sft = []
        for r in range(1, ROUNDS + 1):
            m = json.loads((CODE / "experiments/federated/results" / f"{FED_RUN[ds]}__r{r}" / "metrics.json").read_text())
            if m["resource_measurement"]["paper_timing_eligible"] and all(
                    (c["resource_measurement"].get("calls") or 1) == 1 for c in m["client_training"]):
                sft.append((r, sum(c["elapsed_seconds"] for c in m["client_training"])))
        if not sft:
            raise SystemExit(f"{ds}: no FedAvg SFT round with a clean timing")
        out[f"cost.{ds}.sft.train"] = sum(s for _, s in sft) / len(sft)
        out[f"cost.{ds}.sft.rounds"] = ", ".join(str(r) for r, _ in sft)
        for r in range(1, ROUNDS - WARMUP + 1):
            rec = json.loads((CODE / "audits/protocol_v2" / PREF_AUDIT[ds] / "dpo" / f"round_{r}" / "round.json").read_text())
            if "communication_bytes" in rec:
                out[f"cost.{ds}.adapter_bytes"] = rec["communication_bytes"]["global_adapter"]
            t = rec.get("timing")
            if t:
                if not (t["sampling"]["complete"] and t["training"]["complete"]) or t["sampling"]["interrupted_calls"]:
                    raise SystemExit(f"{ds} preference round {r}: timing not complete")
                gen, lab = t["sampling"]["seconds"]["generate"], t["sampling"]["seconds"]["label"]
                train = t["training"]["reference_seconds"] + t["training"]["update_seconds"]
            else:
                log = json.loads((CODE / "audits/protocol_v2/run_times" / PREF_TIMES[ds] / f"round_{r}.json").read_text())
                if not log["finished"]:
                    raise SystemExit(f"{ds} preference round {r}: log not finished")
                steps = [s for inv in log["invocations"] for s in inv["steps"]]
                gen = sum(s["seconds"] for s in steps if s["step"] == "generate")
                lab = sum(s["seconds"] for s in steps if s["step"] == "label")
                train = sum(s["seconds"] for s in steps if s["step"] == "train")
                if sorted(s["client"] for s in steps if s["step"] == "train") != [1, 2, 3, 4, 5]:
                    raise SystemExit(f"{ds} preference round {r}: a client trained in more than one call")
            out[f"cost.{ds}.pref{r}.sample"], out[f"cost.{ds}.pref{r}.label"], out[f"cost.{ds}.pref{r}.train"] = gen, lab, train
            stats = [c["pair_stats"] for c in rec["clients"].values()]
            out[f"cost.{ds}.pref{r}.pairs"] = sum(s["pairs"] for s in stats)
            out[f"cost.{ds}.pref{r}.questions"] = sum(s["questions"] for s in stats)
            # a question with correct and incorrect samples yields pairs unless its database holds no rows
            no_rows = sum(s.get("questions_empty_database_by_kind", {}).get("mixed", 0) for s in stats)
            out[f"cost.{ds}.pref{r}.paired"] = sum(s["questions_mixed"] for s in stats) - no_rows
            out[f"cost.{ds}.pref{r}.all_correct"] = sum(s["questions_all_correct"] for s in stats)
    if "cost.spider.adapter_bytes" not in out:  # same model and LoRA shape: one adapter size
        out["cost.spider.adapter_bytes"] = out["cost.bird.adapter_bytes"]
    return out


def minutes(s: float) -> str:
    return f"{s / 60:.0f}"


def table_cost(c: dict) -> str:
    """Table 7: what the clients train on in a round (questions; in a preference round the
    questions that yield pairs, and the pairs), its time by step and megabytes a client sends."""
    lines = ["\\toprule",
             row(["", "", "\\multicolumn{2}{c}{Trained on}", "\\multicolumn{4}{c}{Minutes per round}", ""]),
             "\\cmidrule(lr){3-4}\\cmidrule(lr){5-8}",
             row(["Clients' data", "Round", "Questions", "Pairs", "Sampling", "Labels", "Training", "Total",
                  "Sent (MB)"]),
             "\\midrule"]
    for i, ds in enumerate(("bird", "spider")):
        mb = f"{c[f'cost.{ds}.adapter_bytes'] / 1e6:.1f}"
        t = c[f"cost.{ds}.sft.train"]
        lines.append(row([TRAIN_NAME[ds] + " train", "FedAvg SFT", count(c[f"cost.{ds}.pref1.questions"]), "",
                          "", "", minutes(t), minutes(t), mb]))
        for r in range(1, ROUNDS - WARMUP + 1):
            s, la, tr = (c[f"cost.{ds}.pref{r}.{k_}"] for k_ in ("sample", "label", "train"))
            lines.append(row(["", f"Preference round {r}", count(c[f"cost.{ds}.pref{r}.paired"]),
                              count(c[f"cost.{ds}.pref{r}.pairs"]), minutes(s), minutes(la), minutes(tr),
                              minutes(s + la + tr), mb]))
        if i == 0:
            lines.append("\\midrule")
    lines.append("\\bottomrule")
    return tabular("@{}llrrrrrrr@{}", lines, sep="2.5pt")


# ---------------------------------------------------------------- macros
ACCESSORS = r"""%% Written by tools/paper_numbers.py from the committed evaluations. Do not edit.
\makeatletter
\newcommand{\pn@def}[2]{\expandafter\gdef\csname pn@\detokenize{#1}\endcsname{#2}}
\newcommand{\pn@get}[1]{\ifcsname pn@\detokenize{#1}\endcsname\csname pn@\detokenize{#1}\endcsname\else
  \textbf{??}\@latex@warning{No committed number for \detokenize{#1}}\fi}
%% a run: \ex[model]{set}{line}{round}; the model is the main model unless given
\newcommand{\ex}[4][qwen15]{\pn@get{ex/#1/#2/#3/#4}}
\newcommand{\lvl}[5][qwen15]{\pn@get{lvl/#1/#2/#3/#4/#5}}
\newcommand{\nerr}[4][qwen15]{\pn@get{err/#1/#2/#3/#4}}
\newcommand{\nwr}[4][qwen15]{\pn@get{wr/#1/#2/#3/#4}}
\newcommand{\ts}[4][qwen15]{\pn@get{ts/#1/#2/#3/#4}}
%% a comparison: \gain[model]{set}{line a}{round a}{line b}{round b}, b against a
\newcommand{\gain}[6][qwen15]{\pn@get{gain/#1/#2/#3/#4/#5/#6}}
\newcommand{\gap}[6][qwen15]{\pn@get{gap/#1/#2/#3/#4/#5/#6}}
\newcommand{\pval}[6][qwen15]{\pn@get{pval/#1/#2/#3/#4/#5/#6}}
\newcommand{\padj}[6][qwen15]{\pn@get{padj/#1/#2/#3/#4/#5/#6}}
\newcommand{\nfix}[6][qwen15]{\pn@get{nfix/#1/#2/#3/#4/#5/#6}}
\newcommand{\nbrk}[6][qwen15]{\pn@get{nbrk/#1/#2/#3/#4/#5/#6}}
\newcommand{\tsgain}[6][qwen15]{\pn@get{tsgain/#1/#2/#3/#4/#5/#6}}
\newcommand{\tspval}[6][qwen15]{\pn@get{tspval/#1/#2/#3/#4/#5/#6}}
%% a count or a cost: \fact{name}
\newcommand{\fact}[1]{\pn@get{fact/#1}}
"""


def run_id(k: tuple) -> str:
    return k[1] if k[2] == 0 else f"{k[1]}:s{k[2]}"


def macros(d: Data, facts: dict) -> tuple[str, str]:
    tex, md = [ACCESSORS], ["# Numbers of the paper", "",
                            "Written by `tools/paper_numbers.py`. Each macro with its value and the result commit of its row.", ""]

    def put(name: str, value: str, call: str, shown: str, sha: str = "") -> None:
        tex.append(f"\\pn@def{{{name}}}{{{value}}}")
        md.append(f"| `{call}` | {shown} | {sha} |")

    md += ["## Rows", "", "| Macro | Value | Result |", "|---|---|---|"]
    for k in sorted(d.used_runs):
        ds, _, _, line, r = k
        x, rid = d.runs[k], run_id(k)
        opt = "" if rid == MAIN else f"[{rid}]"
        arg = f"{{{ds}}}{{{line}}}{{{r}}}"
        put(f"ex/{rid}/{ds}/{line}/{r}", f2(x["ex"]), f"\\ex{opt}{arg}", f2(x["ex"]), x["sha"])
        for name, kk in LEVELS.get(ds, SPIDER_LEVELS):
            if x.get(kk) is not None:
                put(f"lvl/{rid}/{ds}/{line}/{r}/{name}", f2(x[kk]), f"\\lvl{opt}{arg}{{{name}}}", f2(x[kk]), x["sha"])
        put(f"err/{rid}/{ds}/{line}/{r}", count(x["err"]), f"\\nerr{opt}{arg}", str(x["err"]), x["sha"])
        put(f"wr/{rid}/{ds}/{line}/{r}", count(x["wr"]), f"\\nwr{opt}{arg}", str(x["wr"]), x["sha"])
        if x.get("ts") is not None:
            put(f"ts/{rid}/{ds}/{line}/{r}", f2(x["ts"]), f"\\ts{opt}{arg}", f2(x["ts"]), x["sha"])
    md += ["", "## Comparisons (b against a)", "",
           "`\\pval` is the exact McNemar p, `\\padj` its Holm-adjusted value inside the table that prints the test "
           "(tests per family: " + ", ".join(f"{k} {v}" for k, v in d.families.items()) + ").", "",
           "| Macro | Value | Used in |", "|---|---|---|"]
    for (a, b) in sorted(d.used_tests):
        t = d._tests[(a, b)]
        ds, rid = a[0], run_id(a)
        opt = "" if rid == MAIN else f"[{rid}]"
        arg = f"{{{ds}}}{{{a[3]}}}{{{a[4]}}}{{{b[3]}}}{{{b[4]}}}"
        tail = f"{rid}/{ds}/{a[3]}/{a[4]}/{b[3]}/{b[4]}"
        where = "; ".join(sorted(set(w.removesuffix(":ts") for w in d.used_tests[(a, b)])))
        put(f"gain/{tail}", signed(t["d"]), f"\\gain{opt}{arg}", f"{t['d']:+.2f}", where)
        put(f"gap/{tail}", f2(abs(t["d"])), f"\\gap{opt}{arg}", f2(abs(t["d"])), where)
        put(f"pval/{tail}", p_tex(t["pexact"]), f"\\pval{opt}{arg}", ov.p_text(t["pexact"]), where)
        put(f"padj/{tail}", p_tex(t["padj"]), f"\\padj{opt}{arg}", ov.p_text(t["padj"]), where)
        put(f"nfix/{tail}", count(t["fixed"]), f"\\nfix{opt}{arg}", str(t["fixed"]), where)
        put(f"nbrk/{tail}", count(t["broke"]), f"\\nbrk{opt}{arg}", str(t["broke"]), where)
        if "tspadj" in t:
            put(f"tsgain/{tail}", signed(t["dts"]), f"\\tsgain{opt}{arg}", f"{t['dts']:+.2f}", where)
            put(f"tspval/{tail}", p_tex(t["tspexact"]), f"\\tspval{opt}{arg}", ov.p_text(t["tspexact"]), where)
    md += ["", "## Counts and costs", "", "| Macro | Value | Source |", "|---|---|---|"]
    for name in sorted(facts):
        v, src = facts[name]
        shown = count(v) if isinstance(v, int) else v
        put(f"fact/{name}", shown, f"\\fact{{{name}}}", str(v) if isinstance(v, int) else v, src)
    tex.append("\\makeatother")
    return "\n".join(tex) + "\n", "\n".join(md) + "\n"


def all_facts(d: Data, splits: dict, cost: dict) -> dict:
    facts = {}
    for ds, name in SET_NAME.items():
        n = {x["n"] for k, x in d.runs.items() if k[0] == ds}
        if len(n) != 1:
            raise SystemExit(f"{ds}: evaluations of different sizes {n}")
        facts[f"questions.{ds}"] = (n.pop(), f"rows of the {name} evaluations")
    for k_, v in splits.items():
        if k_.endswith((".hard_min", ".hard_max")):
            v = f"{v:.0f}"
        facts[k_] = (v, "split files (clients.csv, meta.json)")
    for k_, v in cost.items():
        if k_.endswith(".rounds"):
            continue
        if k_.endswith("adapter_bytes"):
            facts[k_.replace("adapter_bytes", "adapter_mb")] = (f"{v / 1e6:.1f}", "round record, communication_bytes")
        elif k_.rsplit(".", 1)[1] in ("pairs", "questions", "paired", "all_correct"):
            facts[k_] = (v, "round record, pair_stats")
        else:
            src = "round records and queue logs" if ".pref" in k_ else f"FedAvg SFT rounds {cost[k_.rsplit('.', 1)[0] + '.rounds']}"
            facts[k_ + "_min"] = (minutes(v), src)
    return facts


# ---------------------------------------------------------------- the form of the answers
# Rows whose predictions are split by form: does a prediction read the tables and the
# table.column names of the gold SQL, or others (CLAIMS.md, C3).
FORM = [("bird", "base", 0), ("bird", "fedavg", 2), ("bird", "fedavg", 3), ("bird", "fedavg", 4), ("bird", "k2", 3),
        ("bird", "k2", 4), ("spider", "base", 0), ("spider", "fedavg", 4), ("spider", "k2", 4)]


def prompt_schema(prompt: str) -> dict:
    """Table -> columns of a database, from the CREATE TABLE statements of the prompt the model saw."""
    import sqlglot
    from sqlglot import exp

    out = {}
    for m in re.finditer(r"CREATE TABLE.*?\);", prompt, flags=re.S):
        table = sqlglot.parse_one(m.group(0), read="sqlite").this
        out[table.this.name] = [c.this.name for c in table.expressions if isinstance(c, exp.ColumnDef)]
    if not out:
        raise SystemExit("no CREATE TABLE statement in a prompt")
    return out


def form_facts(d: Data) -> dict:
    """Predictions of each row of FORM that read the gold SQL's tables and columns, and the others,
    with the right answers of each group. The names a query reads come from the parser of the
    preference rounds (`gold_tables_columns`, sqlglot, per query scope); a prediction that does
    not parse counts with the others. Needs sqlglot (the environment of the code repository)."""
    sys.path.insert(0, str(CODE))
    from fedls_sql.preference.hints import gold_tables_columns

    facts, schemas, gold = {}, {}, {}
    src = "committed predictions; tables and columns read by gold_tables_columns"
    for ds, line, r in FORM:
        k = key(ds, line, r)
        if d.run(k, "Section 5, form of the answers") is None:
            continue
        n = {"gold": 0, "gold_right": 0, "other": 0, "other_right": 0}
        for row_id, x in d.rows_of[k].items():
            if (ds, x["db_id"]) not in schemas:
                schemas[(ds, x["db_id"])] = prompt_schema(x["full_prompt"])
            schema = schemas[(ds, x["db_id"])]
            if (ds, row_id) not in gold:
                gold[(ds, row_id)] = gold_tables_columns(x["gold"], schema)
            g = gold[(ds, row_id)]
            p = gold_tables_columns(x["predicted"], schema) if x["predicted"].strip() else None
            same = g is not None and p is not None and set(g[0]) == set(p[0]) and set(g[1]) == set(p[1])
            group = "gold" if same else "other"
            n[group] += 1
            n[group + "_right"] += x["ex"] == "1"
        for name, v in n.items():
            facts[f"form.{ds}.{line}.{r}.{name}"] = (v, src)
    return facts


# ---------------------------------------------------------------- curves, for charts.py
def curves(d: Data | None = None) -> dict:
    """EX, execution errors and wrong results by round of the lines Fig. 2 and Fig. 3 draw."""
    d = d or Data()
    out = {}
    for ds, lines in CURVES.items():
        out[ds] = {"n": None}
        for line, rounds in lines.items():
            pts = []
            for r in rounds:
                x = d.run(key(ds, "base" if r == 0 else line, r), f"Fig. 2 and Fig. 3, {SET_NAME[ds]}")
                if x is None:
                    raise SystemExit(f"Fig. 2: no row for {ds} {line} round {r}")
                pts.append({"r": r, "ex": x["ex"], "err": x["err"], "wr": x["wr"]})
                out[ds]["n"] = x["n"]
            out[ds][line] = pts
        start = d.run(key(ds, "fedavg", WARMUP), f"Fig. 2 and Fig. 3, {SET_NAME[ds]}")
        out[ds]["k2"].insert(0, {"r": WARMUP, "ex": start["ex"], "err": start["err"], "wr": start["wr"]})
    return out


# ---------------------------------------------------------------- check against the page
def check_page(d: Data) -> None:
    page = ov.PAGE.read_text(encoding="utf-8")
    m = re.search(r"/\* RESULTS:BEGIN[^\n]*\*/\nvar DATA = (.*?);\n/\* RESULTS:END \*/", page, flags=re.S)
    if not m:
        raise SystemExit("no data block in overview.html")
    data = json.loads(m.group(1))
    on_page = {(x["ds"], x["model"], x["seed"], x["line"], x["r"]): x for x in data["runs"]}
    tests = {((t["ds"], t["model"], t["seed"], t["a"], t["ra"]), (t["ds"], t["model"], t["seed"], t["b"], t["rb"])): t
             for t in data["tests"]}
    bad, n_runs, n_tests, only_here = [], 0, 0, 0
    for k in d.used_runs:
        if k not in on_page:
            bad.append(f"row not on the page: {k}")
        elif on_page[k] != d.runs[k]:
            bad.append(f"row differs from the page: {k}")
        else:
            n_runs += 1
    for (a, b) in d.used_tests:
        t = d._tests[(a, b)]
        if (a, b) not in tests:
            only_here += 1
            continue
        p = tests[(a, b)]
        if (p["fixed"], p["broke"], p["p"]) != (t["fixed"], t["broke"], t["p"]) or p.get("tsp") != t.get("tsp"):
            bad.append(f"test differs from the page: {a} -> {b}")
        else:
            n_tests += 1
    if bad:
        raise SystemExit("STOP: the paper and overview.html disagree\n  " + "\n  ".join(bad))
    print(f"check: {n_runs} rows and {n_tests} tests equal the data block of overview.html; "
          f"{only_here} tests are computed here from rows of the page and are not listed on it")


# ---------------------------------------------------------------- main
def missing_text(d: Data) -> str:
    by_table: dict = {}
    for k, where in d.missing.items():
        ds, model, seed, line, r = k
        label = f"{SET_NAME.get(ds, ds)} | {MODEL_NAME[model]}{'' if seed == 0 else f', seed {seed}'} | {line} | round {r}"
        for w in sorted(set(where)):
            by_table.setdefault(w, set()).add(label)
    out = ["# Rows the tables need that are not committed (written by tools/paper_numbers.py)",
           "# table | set | model | line (ARMS name) | round or epoch", ""]
    for w in sorted(by_table):
        out += [f"{w} | {x}" for x in sorted(by_table[w])] + [""]
    if not by_table:
        out.append("none")
    return "\n".join(out).rstrip() + "\n"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="compare every cell with the data block of overview.html")
    args = ap.parse_args()
    d = Data()
    setups_tex, splits = table_setups()
    cost = cost_facts()
    tables = {
        "tab_setups": setups_tex,
        "tab_main": table_main(d),
        "tab_models": table_models(d),
        "tab_federated": table_federated(d),
        "tab_robust": table_robust(d),
        "tab_cost": table_cost(cost),
        "tab_ablation": table_ablation(d),
    }
    for ds, model, la, ra, lb, rb in TEXT_TESTS:
        a, b = (ds, model, 0, la, ra), (ds, model, 0, lb, rb)
        d.run(a, "text"), d.run(b, "text")
        d.test(a, b, "text")
    curves(d)
    form = form_facts(d)
    d.adjust()
    GEN.mkdir(exist_ok=True)
    for name, text in tables.items():
        (GEN / f"{name}.tex").write_text("%% Written by tools/paper_numbers.py. Do not edit.\n" + d.resolve(text),
                                         encoding="utf-8")
    tex, md = macros(d, {**all_facts(d, splits, cost), **form})
    (GEN / "numbers.tex").write_text(tex, encoding="utf-8")
    (GEN / "numbers.md").write_text(md, encoding="utf-8")
    (GEN / "missing.txt").write_text(missing_text(d), encoding="utf-8")
    families = ", ".join(f"{k} {v}" for k, v in d.families.items())
    print(f"{len(d.used_runs)} rows, {len(d.used_tests)} comparisons (Holm families: {families}), "
          f"{len(d.missing)} rows missing -> {GEN.relative_to(ROOT)}")
    if args.check:
        check_page(d)


if __name__ == "__main__":
    main()
