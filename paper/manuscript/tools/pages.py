"""Print the page count of a build from its LaTeX log, against what the journal sets.

    python3 tools/pages.py build/main.log --journal cmc

CMC has no page limit; its fee covers 15 pages and each further page is charged
(paper/notes/JOURNAL_BAR.md, section 1). JIIS takes 25 pages at submission, with references,
tables and figures.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

LIMIT = {"jiis": 25}
FEE_PAGES = {"cmc": 15}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("log")
    ap.add_argument("--journal", choices=("cmc", "jiis"), default="cmc")
    args = ap.parse_args()
    log = Path(args.log).read_text(encoding="latin-1")
    m = re.search(r"Output written on .*?\((\d+) pages?", log, flags=re.S)
    if not m:
        raise SystemExit("no page count in the log")
    pages = int(m.group(1))
    if args.journal in LIMIT:
        print(f"{pages} pages (limit {LIMIT[args.journal]})")
        if pages > LIMIT[args.journal]:
            raise SystemExit(f"STOP: {pages} pages, over the limit of {LIMIT[args.journal]}")
    else:
        covered = FEE_PAGES[args.journal]
        print(f"{pages} pages (no limit; the fee covers {covered}, {max(pages - covered, 0)} above)")


if __name__ == "__main__":
    main()
