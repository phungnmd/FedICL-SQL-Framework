"""Print the page count of a build from its LaTeX log, against the limit of the journal.

    python3 tools/pages.py build/main.log
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

LIMIT = 25  # JIIS: pages at submission, with references, tables and figures


def main() -> None:
    log = Path(sys.argv[1]).read_text(encoding="latin-1")
    m = re.search(r"Output written on .*?\((\d+) pages?", log, flags=re.S)
    if not m:
        raise SystemExit("no page count in the log")
    pages = int(m.group(1))
    print(f"{pages} pages (limit {LIMIT})")
    if pages > LIMIT:
        raise SystemExit(f"STOP: {pages} pages, over the limit of {LIMIT}")


if __name__ == "__main__":
    main()
