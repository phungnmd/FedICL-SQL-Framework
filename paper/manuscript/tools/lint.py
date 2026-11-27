#!/usr/bin/env python3
"""Checks on the text of the manuscript. The writer does not see this file.

A STOP finding stops a section (exit code 1); a note is advice for the main session.

  STOP  a result number or a setting typed by hand (it must be a macro)
        a \\cite key that is not in references.bib; an entry without DOI, arXiv id or address
        a \\usepackage outside the package list of the journal (for JIIS, the Springer template)
        the abstract outside the word range of the journal, in several paragraphs or with a citation
        the keyword count outside the range of the journal
        a heading below the third level; a footnote that is only a citation
        JIIS: a figure caption that ends with a full stop
        CMC: more than 5 references in one bracket
  note  an abbreviation not defined at its first use (abstract and body apart)
        words of the lab (student, arm, queue, run names), file paths, commands
        sentences that tell the making of the paper or certify it
        hedging outside the limitations; em dashes
        an earlier label that TERMS.md replaced (wrong result, right answer); British spelling

    python3 tools/lint.py --journal cmc           # every section
    python3 tools/lint.py sections/03_method.tex  # one file
    python3 tools/lint.py --inventory             # macros and cite keys of every section
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
MANUSCRIPT = HERE.parent
SECTIONS = MANUSCRIPT / "sections"

JOURNALS = {
    "jiis": {"abstract": (150, 250), "keywords": (4, 6), "max_cite": None, "caption_stop": True},
    "cmc": {"abstract": (200, 400), "keywords": (3, 10), "max_cite": 5, "caption_stop": False},
}
# the wrapper of each journal and the packages it may load: for JIIS those of the Springer template, for CMC
# those added to what the class of Tech Science Press loads itself
WRAPPERS = {
    "jiis": ("main_jiis.tex", {"graphicx", "multirow", "amsmath", "amssymb", "amsfonts", "amsthm", "mathrsfs", "appendix", "xcolor",
                               "textcomp", "manyfoot", "booktabs", "algorithm", "algorithmicx", "algpseudocode", "listings"}),
    "cmc": ("main.tex", {"algorithm", "algorithmicx", "algpseudocode", "listings", "catchfile"}),
}
NUMBER_MACROS = ("ex", "lvl", "nerr", "nwr", "ts", "gain", "gap", "pval", "padj", "errpval", "errpadj", "wrpval", "wrpadj", "nfix", "nbrk", "tsgain", "tsgap", "tspval", "fact", "setting",
                 "expect")  # \expect{value}: a guess for a number that waits, marked in the PDF (macros.tex)
# names that are not abbreviations to define (datasets, models, tools, the language itself)
KNOWN_NAMES = {"SQL", "BIRD", "SQLITE", "II", "III", "IV", "RQ", "ID", "DDL", "GPU", "CUDA", "MB", "GB", "EX", "TS",
               "IID", "DK", "QWEN", "PEFT", "AI", "JSON", "CSV", "CODELUTRA"}
LAB_WORDS = [r"\bstudents?\b", r"\bteachers?\b", r"\barms?\b", r"\bqueued?\b", r"\bk[0-9]\b", r"\bbird_[a-z0-9_]+", r"\bfeddpo\b",
             r"\brft\b", r"\bfedpref\b", r"\bsftr\d\b", r"\bablations? row\b", r"\bbaseline row\b", r"\bthe lab\b", r"\bpacket\b",
             r"\bowner\b", r"\bprotocol_v2\b", r"\bseed 0\b"]
LAB_TRACES = [r"\b[\w/]+\.(?:py|json|csv|toml|md)\b", r"\bpython3? ", r"\bwe first\b", r"\bwas then chosen\b", r"\bwe then\b",
              r"\ball numbers come from\b", r"\bno test data was used\b", r"\bit should be noted\b", r"\bwe (?:initially|originally)\b",
              r"\bafter (?:some|several) (?:trials|attempts|experiments)\b", r"\bin an earlier version\b", r"\bwe decided\b",
              r"\bwas (?:selected|picked|tuned) (?:on|after|by looking)\b"]
# The earlier labels that TERMS.md replaced; ordinary words are not checked
OFF_TERMS = [(r"\bwrong (?:results?|samples?|quer(?:y|ies)|answers?|predictions?)\b", "incorrect"),
             (r"\bright (?:answers?|quer(?:y|ies)|samples?|results?|predictions?)\b", "correct")]
BRITISH = r"\b\w*(?:labell|modell|organis|optimis|minimis|maximis|initialis|normalis|generalis|centralis|summaris|behaviour|favour|neighbour)\w*"
HEDGES = [r"\bmay\b", r"\bmight\b", r"\bappears? to\b", r"\bseems? to\b", r"\bit is worth noting\b", r"\barguably\b", r"\bsomewhat\b",
          r"\bpotentially\b", r"\bperhaps\b", r"\bto some extent\b", r"\bwe believe\b"]
LIMITATION_FILES = {"07_discussion.tex"}
# Related work types the numbers of other papers (model sizes, counts); the cited-work audit checks them against the brief
CITED_NUMBER_FILES = {"02_related.tex"}


def strip_comment(line: str) -> str:
    return re.sub(r"(?<!\\)%.*", "", line)


def blank(text: str, pattern: str) -> str:
    """Replace what a pattern matches with spaces, keeping the positions."""
    return re.sub(pattern, lambda m: " " * len(m.group(0)), text, flags=re.S)


def prose(text: str) -> str:
    """The text a reader reads, with macro calls, references, math and floats blanked out."""
    t = "\n".join(strip_comment(l) for l in text.split("\n"))
    for env in ("equation", "align", "algorithm", "algorithmic", "lstlisting", "tabular", "verbatim"):
        t = blank(t, r"\\begin\{" + env + r"\*?\}.*?\\end\{" + env + r"\*?\}")
    t = blank(t, r"\\(?:" + "|".join(NUMBER_MACROS) + r")(?:\[[^\]]*\])?(?:\{[^{}]*\})+")
    t = blank(t, r"\\(?:label|ref|eqref|cite[tp]?|input|includegraphics|bibliography|begin|end|vspace|hspace)(?:\[[^\]]*\])?\{[^{}]*\}")
    t = blank(t, r"\$[^$]*\$")
    t = blank(t, r"\\\([^)]*\\\)")
    return t


def cites(text: str) -> list[tuple[int, list[str]]]:
    out = []
    for i, line in enumerate(text.split("\n"), 1):
        for m in re.finditer(r"\\cite[tp]?(?:\[[^\]]*\])*\{([^{}]*)\}", strip_comment(line)):
            out.append((i, [k.strip() for k in m.group(1).split(",") if k.strip()]))
    return out


def bib_entries() -> dict:
    text = (MANUSCRIPT / "references.bib").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,\s]+)\s*,(.*?)\n\}", text, flags=re.S):
        out[m.group(2)] = m.group(3)
    return out


class Report:
    def __init__(self) -> None:
        self.items: list[tuple[str, str, int, str, str]] = []

    def add(self, level: str, path: Path, line: int, check: str, msg: str) -> None:
        self.items.append((level, path.name, line, check, msg))

    def show(self) -> int:
        for level, name, line, check, msg in sorted(self.items, key=lambda x: (x[0] != "STOP", x[1], x[2])):
            print(f"{name}:{line}: {level} {check}: {msg}")
        stops = sum(1 for x in self.items if x[0] == "STOP")
        notes = len(self.items) - stops
        print(f"{stops} STOP, {notes} notes")
        return 1 if stops else 0


def check_numbers(path: Path, text: str, rep: Report) -> None:
    p = prose(text)
    for i, line in enumerate(p.split("\n"), 1):
        for m in re.finditer(r"(?<![\w.])\d+(?:\{,\}\d{3}|,\d{3})*(?:\.\d+)?(?:e-?\d+)?(?:\s*\\?%)?", line):
            tok = m.group(0).strip()
            before = line[:m.start()].rstrip()
            if re.search(r"(?:Table|Tables|Fig\.|Figs\.|Figure|Section|Sections|Algorithm|Eq\.|Equation|Appendix|RQ|Resource|line|lines|step|Step)~?$",
                         before):
                continue
            decimal = "." in tok or "%" in tok or "e" in tok
            value = float(re.sub(r"[^\d.]", "", tok.split("e")[0]) or 0)
            if path.name in CITED_NUMBER_FILES and (decimal or value >= 10):
                rep.add("note", path, i, "number", f"'{tok}': a number of a cited paper has a row in the brief (cited-work audit); one of ours is a macro")
            elif decimal or value >= 10:
                rep.add("STOP", path, i, "number", f"'{tok}' is typed by hand; a result or a setting is a macro")
            elif value >= 2:
                rep.add("note", path, i, "number", f"'{tok}': a count or a setting? then a macro")


def setting_values() -> dict:
    """What each \\setting{name} prints, from generated/settings.tex."""
    source = MANUSCRIPT / "generated" / "settings.tex"
    if not source.exists():
        return {}
    return dict(re.findall(r"\\st@def\{([^}]+)\}\{(.*)\}\s*$", source.read_text(encoding="utf-8"), flags=re.M))


def check_text(path: Path, text: str, rep: Report) -> None:
    p = prose(text)
    lines = p.split("\n")
    for i, line in enumerate(lines, 1):
        low = line.lower()
        for pat in LAB_WORDS:
            for m in re.finditer(pat, low):
                rep.add("note", path, i, "lab word", f"'{m.group(0)}'")
        for pat in LAB_TRACES:
            for m in re.finditer(pat, low):
                rep.add("note", path, i, "the lab showing", f"'{m.group(0).strip()}'")
        if path.name not in LIMITATION_FILES:
            for pat in HEDGES:
                for m in re.finditer(pat, low):
                    rep.add("note", path, i, "hedge", f"'{m.group(0)}'")
        for pat, term in OFF_TERMS:
            for m in re.finditer(pat, low):
                rep.add("note", path, i, "term", f"'{m.group(0)}': the label of the paper is '{term}' (TERMS.md)")
        for m in re.finditer(BRITISH, low):
            rep.add("note", path, i, "spelling", f"'{m.group(0)}': American spelling")
        if "---" in line or "\u2014" in line:
            rep.add("note", path, i, "dash", "an em dash")
    raw = [strip_comment(l) for l in text.split("\n")]
    values = setting_values()
    for i, line in enumerate(raw, 1):
        for m in re.finditer(r"\\setting\{([^}]+)\}(?:~|\\[,; ]|\s)*([A-Za-z%]+)", line):
            printed = values.get(m.group(1), "").split()
            if len(printed) > 1 and printed[-1] == m.group(2):
                rep.add("STOP", path, i, "unit", f"\\setting{{{m.group(1)}}} prints '{values[m.group(1)]}'; "
                                                 f"the '{m.group(2)}' after it is printed twice")
        if re.search(r"\\(?:paragraph|subparagraph)\*?\{", line):
            rep.add("STOP", path, i, "heading", "a heading below the third level")
        if re.search(r"\\footnote\{\s*\\cite[tp]?\{[^{}]*\}\s*\.?\s*\}", line):
            rep.add("STOP", path, i, "footnote", "a footnote that is only a citation")
        if re.search(r"\\usepackage", line):
            rep.add("STOP", path, i, "package", "a package is loaded inside a section")


def check_abbreviations(files: list[tuple[Path, str]], rep: Report, part: str) -> None:
    """First use of each abbreviation in reading order: it should stand in brackets after its long form."""
    seen = set()
    for path, text in files:
        for i, line in enumerate(prose(text).split("\n"), 1):
            for m in re.finditer(r"(?<![\\\w])([A-Z][A-Za-z]*[A-Z][A-Za-z]*)(?:s\b)?", line):
                ab = m.group(1)
                if ab.upper() in KNOWN_NAMES or ab in seen or len(ab) < 2:
                    continue
                seen.add(ab)
                if not (line[:m.start()].rstrip().endswith("(") and line[m.end():].lstrip().startswith(")")):
                    rep.add("note", path, i, "abbreviation", f"'{ab}' is first used in the {part} without its long form before it")


def check_refs(files: list[tuple[Path, str]], rep: Report, journal: dict) -> None:
    bib = bib_entries()
    used = set()
    for path, text in files:
        for line, keys in cites(text):
            used.update(keys)
            for k in keys:
                if k not in bib:
                    rep.add("STOP", path, line, "reference", f"'{k}' is not in references.bib")
            if journal["max_cite"] and len(keys) > journal["max_cite"]:
                rep.add("STOP", path, line, "reference", f"{len(keys)} references in one bracket (at most {journal['max_cite']})")
    bibpath = MANUSCRIPT / "references.bib"
    for k, body in bib.items():
        if not re.search(r"\b(?:doi|eprint)\s*=", body, flags=re.I):
            if re.search(r"\burl\s*=", body, flags=re.I):
                rep.add("note", bibpath, 0, "reference", f"'{k}' has an address but no DOI and no arXiv id")
            else:
                rep.add("STOP", bibpath, 0, "reference", f"'{k}' has no DOI, no arXiv id and no address")
        if k not in used:
            rep.add("note", bibpath, 0, "reference", f"'{k}' is not cited")


def check_front(rep: Report, journal: dict) -> None:
    ab = SECTIONS / "00_abstract.tex"
    text = "\n".join(strip_comment(l) for l in ab.read_text(encoding="utf-8").split("\n")).strip()
    if text:
        words = len(re.findall(r"[A-Za-z0-9][\w'-]*", re.sub(r"\\[a-zA-Z]+", " w ", prose(text))))
        lo, hi = journal["abstract"]
        if not lo <= words <= hi:
            rep.add("STOP", ab, 1, "abstract", f"{words} words (the journal asks for {lo} to {hi})")
        if re.search(r"\n\s*\n", text):
            rep.add("STOP", ab, 1, "abstract", "more than one paragraph")
        if re.search(r"\\cite", text):
            rep.add("STOP", ab, 1, "abstract", "a citation in the abstract")
    kw = SECTIONS / "00_keywords.tex"
    text = "\n".join(strip_comment(l) for l in kw.read_text(encoding="utf-8").split("\n")).strip()
    if text:
        n = len([k for k in re.split(r",|;|\\kwsep|\\sep", text) if k.strip()])
        lo, hi = journal["keywords"]
        if not lo <= n <= hi:
            rep.add("STOP", kw, 1, "keywords", f"{n} keywords (the journal asks for {lo} to {hi})")


def check_preamble(rep: Report, journal_name: str) -> None:
    wrapper, packages = WRAPPERS[journal_name]
    for name in (wrapper, "macros.tex"):
        path = MANUSCRIPT / name
        for i, line in enumerate(path.read_text(encoding="utf-8").split("\n"), 1):
            for m in re.finditer(r"\\usepackage(?:\[[^\]]*\])?\{([^{}]*)\}", strip_comment(line)):
                for pkg in m.group(1).split(","):
                    if pkg.strip() not in packages:
                        rep.add("STOP", path, i, "package", f"'{pkg.strip()}' is not in the package list of this journal (tools/lint.py)")


def check_captions(files: list[tuple[Path, str]], rep: Report, journal: dict) -> None:
    if not journal["caption_stop"]:
        return
    for path, text in files:
        clean = "\n".join(strip_comment(l) for l in text.split("\n"))
        for m in re.finditer(r"\\begin\{figure\*?\}.*?\\end\{figure\*?\}", clean, flags=re.S):
            cap = re.search(r"\\caption\{((?:[^{}]|\{[^{}]*\})*)\}", m.group(0), flags=re.S)
            if cap and cap.group(1).rstrip().endswith("."):
                line = clean[:m.start() + cap.start()].count("\n") + 1
                rep.add("STOP", path, line, "caption", "a figure caption ends with a full stop")


def inventory(files: list[tuple[Path, str]]) -> None:
    """Macros and cite keys of each section, sorted, with their counts: diff two runs of this."""
    for path, text in files:
        clean = "\n".join(strip_comment(l) for l in text.split("\n"))
        macros = Counter(m.group(0) for m in re.finditer(
            r"\\(?:" + "|".join(NUMBER_MACROS) + r")(?:\[[^\]]*\])?(?:\{[^{}]*\})+", clean))
        keys = Counter(k for _, ks in cites(text) for k in ks)
        print(f"== {path.name}: {sum(macros.values())} number macros, {sum(keys.values())} citations")
        for k in sorted(macros):
            print(f"  {macros[k]} {k}")
        for k in sorted(keys):
            print(f"  {keys[k]} \\cite{{{k}}}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("files", nargs="*", help="section files (default: every section)")
    ap.add_argument("--journal", choices=sorted(JOURNALS), default="cmc")
    ap.add_argument("--inventory", action="store_true")
    args = ap.parse_args()
    paths = [Path(f) if Path(f).is_absolute() else MANUSCRIPT / f for f in args.files] or sorted(SECTIONS.glob("*.tex"))
    files = [(p, p.read_text(encoding="utf-8")) for p in paths]
    if args.inventory:
        inventory(files)
        return
    journal = JOURNALS[args.journal]
    rep = Report()
    for path, text in files:
        if path.name.startswith(("B_", "A_")):  # the appendices hold the prompt and the generated settings table
            continue
        check_numbers(path, text, rep)
        check_text(path, text, rep)
    body = [(p, t) for p, t in files if not p.name.startswith(("00_", "90_", "A_", "B_"))]
    check_abbreviations([(p, t) for p, t in files if p.name == "00_abstract.tex"], rep, "abstract")
    check_abbreviations(body, rep, "text")
    check_refs(files, rep, journal)
    check_captions(files, rep, journal)
    if not args.files:
        check_front(rep, journal)
        check_preamble(rep, args.journal)
    sys.exit(rep.show())


if __name__ == "__main__":
    main()
