#!/usr/bin/env python3
"""Fetch the abstract of every entry of references.bib into .sources/abstracts.json.

The file is outside Git (abstracts are the text of their authors) and is read when
Section 2 is written. Sources, in this order: the
arXiv API for an entry with an `eprint`, then Crossref and Semantic Scholar by DOI.
An entry with no abstract at any of them is listed at the end and left out.

usage: python3 tools/abstracts.py [--refresh]
"""
from __future__ import annotations

import argparse
import html
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIB = ROOT / "references.bib"
OUT = ROOT / ".sources" / "abstracts.json"
AGENT = {"User-Agent": "abstract-fetch/1.0"}
ATOM = "{http://www.w3.org/2005/Atom}"


def entries() -> dict[str, dict[str, str]]:
    """key -> {title, eprint, doi} from references.bib."""
    found: dict[str, dict[str, str]] = {}
    for block in re.split(r"(?m)^(?=@)", BIB.read_text(encoding="utf-8")):
        head = re.match(r"@\w+\{([^,\s]+),", block)
        if not head:
            continue
        fields = {}
        for name in ("title", "eprint", "doi"):
            m = re.search(rf"(?mi)^\s*{name}\s*=\s*\{{(.+?)\}},?\s*$", block)
            if m:
                fields[name] = re.sub(r"[{}]", "", m.group(1)).strip()
        found[head.group(1)] = fields
    return found


def get(url: str) -> bytes | None:
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=AGENT), timeout=60) as r:
            return r.read()
    except (urllib.error.URLError, TimeoutError):
        return None


def clean(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    return re.sub(r"\s+", " ", text).strip()


def from_arxiv(ids: list[str]) -> dict[str, str]:
    got: dict[str, str] = {}
    for i in range(0, len(ids), 25):
        chunk = ids[i:i + 25]
        raw = get("http://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(chunk))
        if raw:
            for e in ET.fromstring(raw).iter(f"{ATOM}entry"):
                ident = re.sub(r"v\d+$", "", (e.findtext(f"{ATOM}id") or "").rsplit("/abs/", 1)[-1])
                summary = e.findtext(f"{ATOM}summary")
                if ident and summary:
                    got[ident] = clean(summary)
        time.sleep(3)  # the arXiv API asks for a pause between calls
    return got


def from_doi(doi: str) -> tuple[str, str] | None:
    raw = get("https://api.crossref.org/works/" + urllib.parse.quote(doi))
    if raw:
        text = json.loads(raw).get("message", {}).get("abstract")
        if text:
            return clean(re.sub(r"(?i)^\s*<jats:title>abstract</jats:title>", "", text)), "Crossref"
    raw = get("https://api.semanticscholar.org/graph/v1/paper/DOI:" + urllib.parse.quote(doi) + "?fields=abstract")
    if raw:
        text = json.loads(raw).get("abstract")
        if text:
            return clean(text), "Semantic Scholar"
    return None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--refresh", action="store_true", help="fetch every entry again")
    args = ap.parse_args()

    refs = entries()
    store: dict[str, dict[str, str]] = {}
    if OUT.exists() and not args.refresh:
        store = json.loads(OUT.read_text(encoding="utf-8"))
    todo = {k: v for k, v in refs.items() if k not in store}

    arxiv = from_arxiv(sorted({v["eprint"] for v in todo.values() if "eprint" in v}))
    for key, f in todo.items():
        if f.get("eprint") in arxiv:
            store[key] = {"title": f.get("title", ""), "abstract": arxiv[f["eprint"]], "source": f"arXiv {f['eprint']}"}
        elif "doi" in f:
            hit = from_doi(f["doi"])
            if hit:
                store[key] = {"title": f.get("title", ""), "abstract": hit[0], "source": f"{hit[1]}, DOI {f['doi']}"}

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({k: store[k] for k in sorted(store)}, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    missing = sorted(k for k in refs if k not in store)
    print(f"{OUT.relative_to(ROOT)}: {len(store)} of {len(refs)} entries have an abstract")
    for k in missing:
        print(f"  no abstract: {k}")


if __name__ == "__main__":
    main()
