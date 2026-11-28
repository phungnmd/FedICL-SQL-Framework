#!/usr/bin/env python3
"""Words of a section that stand in runs of five or more words found in other texts.

    python3 tools/overlap.py sections/03_method.tex OTHER [OTHER ...]

`make overlap` runs it for every section against the sources of the closest papers and
the example papers (.sources/, outside Git). A run that is not a stock phrase of the
field or a name is written again.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

ENV = (r"equation|align|algorithm|algorithmic|wrapfigure|wraptable|figure|table|tabular|lstlisting|tcolorbox|"
       r"gather|multline|eqnarray|minipage|verbatim|tikzpicture|subfigure|displaymath|array|CCSXML|abstract")


def strip_floats(text: str) -> str:
    for _ in range(3):
        text = re.sub(r"\\begin\{(%s)\*?\}.*?\\end\{\1\*?\}" % ENV, " ", text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    return re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)


def detex(par: str) -> str:
    par = re.sub(r"\$[^$]*\$", " X ", par)
    par = re.sub(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", par)
    par = re.sub(r"\\(?:ref|label|eqref|autoref|cref|Cref|url|footnote|vspace|hspace|includegraphics|setting|fact)"
                 r"\*?(?:\[[^\]]*\])*\{[^}]*\}", " ", par)
    par = re.sub(r"\\(?:sub)*section\*?\{[^}]*\}", " ", par)
    par = re.sub(r"\\(?:paragraph|subparagraph|textbf|noindent)\*?\{([^}]*)\}", r" \1. ", par)
    par = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?", " ", par)
    par = re.sub(r"[{}~\\]", " ", par)
    return re.sub(r"\s+", " ", par).strip()


def words(text: str) -> list[str]:
    return re.findall(r"[a-z]+(?:'[a-z]+)?", text.lower())


def overlap(path: Path, others: list[Path], run: int = 5) -> None:
    draft = words(detex(strip_floats(re.sub(r"(?m)(?<!\\)%.*$", "", path.read_text(encoding="utf-8")))))
    grams = set()
    for other in others:
        w = words(re.sub(r"`[^`]*`|\$[^$]*\$", " ", other.read_text(encoding="utf-8")))
        grams.update(tuple(w[i:i + run]) for i in range(len(w) - run + 1))
    marked = [False] * len(draft)
    for i in range(len(draft) - run + 1):
        if tuple(draft[i:i + run]) in grams:
            marked[i:i + run] = [True] * run
    share = 100 * sum(marked) / max(len(draft), 1)
    print(f"{path.name}: {sum(marked)} of {len(draft)} words ({share:.0f}%) stand in runs of {run} or more words "
          f"found in {', '.join(o.name for o in others)}")
    i = 0
    while i < len(draft):
        if marked[i]:
            j = i
            while j < len(draft) and marked[j]:
                j += 1
            print("  ", " ".join(draft[i:j]))
            i = j
        else:
            i += 1


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file", type=Path)
    ap.add_argument("others", type=Path, nargs="+")
    args = ap.parse_args()
    overlap(args.file, args.others)


if __name__ == "__main__":
    main()
