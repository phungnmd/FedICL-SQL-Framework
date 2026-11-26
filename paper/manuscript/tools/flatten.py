#!/usr/bin/env python3
"""Write the submission copy of the manuscript: one directory, one .tex file.

What the journal asks for (JIIS submission guidelines; the Springer template itself says
"do not use \\input", "submit as one .tex document"):

  - one .tex file: every \\input is put in, the number and setting macros are replaced by
    their values, comment lines are dropped
  - the reference list pasted in from the .bbl in place of \\bibliography
  - no subfolders; figure files named Fig1, Fig2, ... in the order they appear
  - the class and the reference style beside it, and the compiled PDF

The copy is compiled in its own directory, with nothing else on the TeX path of the
manuscript, so a file that is missing from it stops the build here and not at the journal.

    python3 tools/flatten.py --journal jiis     # after `make`, which leaves build/main.bbl
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUSCRIPT = HERE.parent
WRAPPER = {"jiis": ("main.tex", ["sn-jnl.cls", "sn-basic.bst"])}
NAME = "manuscript"
GENERATED_MACROS = ("generated/numbers", "generated/settings")
# accessor -> (key prefix, number of mandatory arguments); the optional argument is the model
ACCESSORS = {"ex": ("ex", 3), "lvl": ("lvl", 4), "nerr": ("err", 3), "nwr": ("wr", 3), "ts": ("ts", 3),
             "gain": ("gain", 5), "gap": ("gap", 5), "pval": ("pval", 5), "padj": ("padj", 5), "nfix": ("nfix", 5),
             "nbrk": ("nbrk", 5), "tsgain": ("tsgain", 5), "tspval": ("tspval", 5)}


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def values() -> tuple[dict, dict]:
    """key -> value of every number macro and of every setting macro."""
    pat = r"\\%s@def\{([^{}]*)\}\{((?:[^{}]|\{(?:[^{}]|\{[^{}]*\})*\})*)\}"
    numbers = dict(re.findall(pat % "pn", read(MANUSCRIPT / "generated" / "numbers.tex")))
    settings = dict(re.findall(pat % "st", read(MANUSCRIPT / "generated" / "settings.tex")))
    return numbers, settings


def inline(text: str, seen: tuple = ()) -> str:
    """Put every \\input in, except the two files of macro definitions."""
    def put(m: re.Match) -> str:
        name = m.group(1).strip()
        if name in GENERATED_MACROS:
            return ""
        path = MANUSCRIPT / (name if name.endswith(".tex") else name + ".tex")
        if path in seen:
            raise SystemExit(f"STOP: {name} includes itself")
        return inline(read(path), seen + (path,)).rstrip("\n")
    return re.sub(r"\\input\{([^{}]*)\}", put, uncomment(text))


def uncomment(text: str) -> str:
    """Drop the lines that are only a comment; a % that ends a line of code stays."""
    return "\n".join(l for l in text.split("\n") if not l.lstrip().startswith("%"))


def expand(text: str, numbers: dict, settings: dict) -> str:
    missing = []

    def number(m: re.Match) -> str:
        prefix, n = ACCESSORS[m.group(1)]
        args = re.findall(r"\{([^{}]*)\}", m.group(3))
        if len(args) != n:
            raise SystemExit(f"STOP: {m.group(0)} has {len(args)} arguments, not {n}")
        key = "/".join([prefix, m.group(2) or "qwen15"] + args)
        if key not in numbers:
            missing.append(m.group(0))
            return m.group(0)
        return numbers[key]

    def simple(table: dict, prefix: str):
        def put(m: re.Match) -> str:
            key = prefix + m.group(1)
            if key not in table:
                missing.append(m.group(0))
                return m.group(0)
            return table[key]
        return put

    text = re.sub(r"\\(" + "|".join(sorted(ACCESSORS, key=len, reverse=True)) + r")(?:\[([^\]]*)\])?((?:\{[^{}]*\})+)", number, text)
    text = re.sub(r"\\fact\{([^{}]*)\}", simple(numbers, "fact/"), text)
    text = re.sub(r"\\setting\{([^{}]*)\}", simple(settings, ""), text)
    if missing:
        raise SystemExit("STOP: no committed value for " + ", ".join(sorted(set(missing))))
    return text


def figures(text: str, out: Path) -> str:
    """Copy each figure file as Fig<n> in order of first appearance and point the text at it."""
    order: dict = {}

    def put(m: re.Match) -> str:
        src = m.group(2).strip()
        if src not in order:
            path = MANUSCRIPT / src
            path = path if path.suffix else path.with_suffix(".pdf")
            if not path.exists():
                raise SystemExit(f"STOP: figure file {src} not found")
            order[src] = f"Fig{len(order) + 1}"
            shutil.copyfile(path, out / (order[src] + path.suffix))
        return f"\\includegraphics{m.group(1) or ''}{{{order[src]}}}"
    return re.sub(r"\\includegraphics(\[[^\]]*\])?\{([^{}]*)\}", put, text)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--journal", choices=sorted(WRAPPER), default="jiis")
    ap.add_argument("--out", default="submit")
    args = ap.parse_args()
    wrapper, style_files = WRAPPER[args.journal]
    out = MANUSCRIPT / args.out
    if out.exists():
        shutil.rmtree(out)
    out.mkdir()
    numbers, settings = values()
    text = expand(inline(read(MANUSCRIPT / wrapper)), numbers, settings)
    bbl = MANUSCRIPT / "build" / (Path(wrapper).stem + ".bbl")
    if re.search(r"\\cite", text):
        if not bbl.exists():
            raise SystemExit("STOP: the text cites and build/main.bbl is missing; run `make` first")
        text = re.sub(r"\\bibliography\{[^{}]*\}", lambda m: read(bbl).rstrip("\n"), text)
    else:
        text = re.sub(r"\\bibliography\{[^{}]*\}\n?", "", text)
    text = figures(text, out)
    text = re.sub(r"\n{3,}", "\n\n", text)
    left = re.findall(r"\\(?:input|bibliography)\{[^{}]*\}|\\pn@|\\st@", text)
    if left:
        raise SystemExit(f"STOP: left in the flat file: {sorted(set(left))}")
    (out / f"{NAME}.tex").write_text(text, encoding="utf-8")
    for f in style_files:
        shutil.copyfile(MANUSCRIPT / f, out / f)
    for i in range(3):
        run = subprocess.run(["pdflatex", "-interaction=nonstopmode", "-halt-on-error", f"{NAME}.tex"], cwd=out,
                             capture_output=True, text=True, errors="replace")
        if run.returncode != 0:
            raise SystemExit("STOP: the flat copy does not compile\n" + run.stdout[-1500:])
    log = (out / f"{NAME}.log").read_text(encoding="latin-1")
    if re.search(r"Warning: (?:Reference|Citation) .* undefined|File .* not found", log):
        raise SystemExit("STOP: the flat copy has an undefined reference or a missing file")
    for f in out.iterdir():
        if f.suffix in {".aux", ".log", ".out", ".toc", ".blg"}:
            f.unlink()
    if any(f.is_dir() for f in out.iterdir()):
        raise SystemExit("STOP: a subfolder in the submission copy")
    pages = re.search(r"Output written on .*?\((\d+) pages?", log, flags=re.S).group(1)
    print(f"{out.relative_to(MANUSCRIPT)}/: " + ", ".join(sorted(f.name for f in out.iterdir())) + f" ({pages} pages)")


if __name__ == "__main__":
    main()
