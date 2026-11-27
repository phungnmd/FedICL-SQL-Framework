#!/usr/bin/env python3
"""Assemble what the writer of one section reads: build/pack_NN/ and build/start_NN.md.

The writer runs in an isolated session (the cold-session skill) and sees this
directory only (paper/notes/WRITING_PLAN.md, section 3.2). The pack holds the
work in full as science and nothing of the lab; after assembling it this tool
searches it for dates, "owner" and lab words and stops when it finds any.

usage: python3 tools/pack.py NN [--also NN ...] [--accepted NN ...] [--brief FILE]
       python3 tools/pack.py --check FILE...
  NN          the section to write (01 ... 07)
  --also      further sections the same writer writes (07 with 06, 00 with 01)
  --accepted  the sections already accepted, given to the writer to read
  --brief     the brief, when it is not briefs/NN_name.md
  --check     search the files (an answer to the writer, editor's notes, a file sent
              with them) for the same traces, without assembling a pack
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from lint import LAB_WORDS  # noqa: E402  (the same list the drafts are read against)

WEB_SECTIONS = {"01", "02", "06"}  # sections on other work: web search is on (plan, section 2.1)
NOT_A_BRIEF = re.compile(r"_(checks|outline|notes|notes_editor|rows|table1_rows)\.md$")
FACT_SHEETS = ("briefs/02_related_rows.md", "briefs/02_related_table1_rows.md")
FLOATS = {
    "fig_method_overview.pdf": "Fig. 2, the overview of the framework",
    "fig_rounds_cmc.pdf": "Fig. 3, EX by round; included with \\chart{fig_rounds}",
    "fig_errors_cmc.pdf": "Fig. 4, incorrect predictions by kind and round; included with \\chart{fig_errors}",
    "tab_setups.tex": "Table 2, the federated setups",
    "tab_main.tex": "Table 3, main results",
    "tab_models.tex": "Table 5, other models",
    "tab_federated.tex": "Table 6, other federated setups",
    "tab_robust.tex": "Table 7, Spider dev and the perturbed sets, EX and TS",
    "tab_cost.tex": "Table 8, the cost of a round for a client",
    "tab_ablation.tex": "Table 4, ablations; BIRD dev also under test-suite accuracy",
    "tab_settings.tex": "Appendix B, settings (first part)",
    "tab_settings_2.tex": "Appendix B, settings (second part)",
}
SETS = {"bird": "BIRD dev", "spider": "Spider test", "spiderdev": "Spider dev", "syn": "Spider-Syn",
        "realistic": "Spider-Realistic", "dk": "Spider-DK"}
ROWS = {
    "base": "the pretrained model (round 0)",
    "fedavg": "FedAvg SFT",
    "central": "centralized SFT (the last argument is the epoch)",
    "local": "local SFT",
    "fedprox": "FedProx SFT",
    "k2": "\\method in its default configuration (two warm-up rounds)",
    "k0": "\\method without warm-up rounds",
    "k3": "\\method with three warm-up rounds",
    "fixed": "\\method with the preference pairs and the reference model of the first preference round",
    "rft": "\\method without the preference term",
    "feddpo": "FedDPO; its first preference round is \\method without the NLL term",
    "k0gold": "\\method without warm-up rounds, with pairs of the gold SQL query for questions that have no correct sample",
    "reagge": "\\method aggregated with equal weights",
    "reaggq": "\\method aggregated with weights by number of questions",
    "pooled": "the preference rounds on the pooled data of the clients",
}
MODELS = {"qwen05": "Qwen2.5-Coder-0.5B-Instruct", "dsc13": "DeepSeek-Coder-1.3B-Instruct"}
START = """You are the author of Section {n} ({title}) of a machine learning research
manuscript prepared for Computers, Materials & Continua. Your working
directory holds the material of the paper; README.md lists it. Read
README.md, paper.md, guide.md and brief.md first, and open the rest as
you need it.
{web}
The editor is one of the researchers of the study. Whenever the material
does not settle something you need, write your questions to
notes/questions.md and stop; the editor answers them.

First deliverable: the outline that guide.md describes, written to
notes/outline.md. Stop there and wait for the editor's response.
"""
WEB = """
You may search the web to check a detail of a cited paper or to find
related work. List in notes/notes.md every fact and every reference you
take from the web, each with its URL and the place in the source.
"""


def cells(line: str) -> list[str]:
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def drop_columns(md: str, drop: set[str]) -> str:
    """Remove the named columns from every Markdown table of `md`."""
    out, idx = [], None
    for line in md.splitlines():
        if not line.startswith("|"):
            idx = None
            out.append(line)
            continue
        row = cells(line)
        if idx is None:
            idx = [i for i, c in enumerate(row) if c not in drop]
        out.append("| " + " | ".join(row[i] for i in idx if i < len(row)) + " |")
    return "\n".join(out) + "\n"


def macros_md() -> tuple[str, list[str]]:
    """generated/numbers.md for the writer: a legend of the arguments, no result commits."""
    src = (ROOT / "generated/numbers.md").read_text(encoding="utf-8")
    body = src[src.index("## Rows"):]
    body = re.sub(r"(?m)^(\| `\\[a-z]+(?:\[[a-z0-9]+\])?\{[^|]*\| [^|]* \|) [0-9a-f]{8} \|$", r"\1", body)
    body = body.replace("| Macro | Value | Result |\n|---|---|---|", "| Macro | Prints |\n|---|---|", 1)
    counts = body.index("## Counts and costs")
    body = body[:counts] + drop_columns(body[counts:], {"Source"})
    args = re.findall(r"`\\[a-z]+(?:\[([a-z0-9]+)\])?\{([a-z]+)\}\{([a-z0-9]+)\}", body)
    unknown = sorted({m for m, _, _ in args if m and m not in MODELS} | {s for _, s, _ in args if s not in SETS}
                     | {r for _, _, r in args if r not in ROWS})
    used_sets = [s for s in SETS if any(a[1] == s for a in args)]
    used_rows = [r for r in ROWS if any(a[2] == r for a in args)]
    head = ["# Macros of the results", "",
            "Every result is written as a macro and never as digits. A macro of a row takes the evaluation",
            "set, the row and the number of rounds, as in `\\ex{bird}{k2}{4}`; a comparison takes two rows,",
            "the reference first, as in `\\gain{bird}{fedavg}{4}{k2}{4}`. An optional first argument names",
            "another model, as in `\\ex[qwen05]{spider}{k2}{4}`. A macro whose result is awaited is absent",
            "from the lists below and prints a placeholder.", "",
            "| Evaluation set | |", "|---|---|"]
    head += [f"| `{s}` | {SETS[s]} |" for s in used_sets]
    head += ["", "| Row | |", "|---|---|"] + [f"| `{r}` | {ROWS[r]} |" for r in used_rows]
    head += ["", "| Model | |", "|---|---|", "| (none) | Qwen2.5-Coder-1.5B-Instruct |"]
    head += [f"| `{m}` | {MODELS[m]} |" for m in MODELS]
    head += ["", "| Macro | Meaning |", "|---|---|",
             "| `\\ex`, `\\ts` | execution accuracy, test-suite accuracy |",
             "| `\\lvl` | EX on one difficulty level (last argument) |",
             "| `\\nerr`, `\\nwr` | number of predictions that are execution errors, incorrect results |",
             "| `\\gain`, `\\gap`, `\\tsgain` | difference of the second row from the first: signed, unsigned, in TS |",
             "| `\\pval`, `\\padj` | exact McNemar p of the comparison; its Holm-adjusted value |",
             "| `\\nfix`, `\\nbrk` | questions correct only in the second row, only in the first |",
             "| `\\errpval`, `\\wrpval`, `\\wrpadj` | the same test on execution errors, on incorrect results |",
             "| `\\fact`, `\\setting` | a count or a cost; a configuration value (`settings.md`) |", ""]
    return "\n".join(head) + "\n" + body, unknown


def bib_entries() -> dict[str, dict[str, str]]:
    found = {}
    for block in re.split(r"(?m)^(?=@)", (ROOT / "references.bib").read_text(encoding="utf-8")):
        head = re.match(r"@\w+\{([^,\s]+),", block)
        if not head:
            continue
        f = {}
        for name in ("title", "author", "year", "booktitle", "journal", "eprint", "doi"):
            m = re.search(rf"(?mi)^\s*{name}\s*=\s*\{{(.+?)\}},?\s*$", block)
            if m:
                f[name] = re.sub(r"[{}]", "", m.group(1)).strip()
        found[head.group(1)] = f
    return found


def fact_rows(key: str) -> str:
    """The verified statements about one paper, without the quotations and the reading record."""
    parts = []
    for sheet in FACT_SHEETS:
        text = (ROOT / sheet).read_text(encoding="utf-8")
        for block in re.split(r"(?m)^(?=## )", text):
            if f"(`{key}`)" not in block.splitlines()[0]:
                continue
            body = "\n".join(block.splitlines()[1:]).strip()
            # the version the locators refer to; where and when it was read is the lab's record
            body = re.sub(r"(?m)^(Version read: .*?)(?:, (?:the )?PDF\b|, read |, https?://|, Secs?\.).*$", r"\1.", body)
            parts.append(drop_columns(body, {"Quotation"}).strip())
    return "\n\n".join(parts)


def related_md(key: str, bib: dict[str, str], abstracts: dict) -> str:
    venue = bib.get("booktitle") or bib.get("journal") or ("arXiv preprint" if "eprint" in bib else "")
    ident = " ".join(x for x in (f"arXiv {bib['eprint']}" if "eprint" in bib else "", f"DOI {bib['doi']}" if "doi" in bib else "") if x)
    lines = [f"# {bib.get('title', key)}", "", f"Citation key: `{key}`", "",
             f"{bib.get('author', '')}. {venue}, {bib.get('year', '')}. {ident}".strip(), ""]
    if key in abstracts:
        lines += ["## Abstract", "", abstracts[key]["abstract"], ""]
    rows = fact_rows(key)
    if rows:
        lines += ["## Statements verified in the source", "", rows, ""]
    return "\n".join(lines)


def scan(pack: Path, only: list[Path] | None = None) -> list[str]:
    """Dates, 'owner' and lab words in what the writer will read: a pack, or the files `only`."""
    hits = []
    for f in only if only is not None else sorted(pack.rglob("*")):
        rel = f.relative_to(pack) if only is None else Path(f.name)
        if not f.is_file() or f.suffix not in {".md", ".tex", ".txt"} or rel.parts[0] == "examples":
            continue
        patterns = [r"\b20\d\d-\d\d-\d\d\b", r"(?i)\bowner\b", r"(?i)\bread on\b"]

        if rel.parts[0] not in {"related", "sections"}:  # other authors' words; drafts are read by make lint
            # FedDPO is a term of the paper; only the lowercase run name is a lab word
            patterns += [w if "feddpo" in w else "(?i)" + w for w in LAB_WORDS]
            patterns += [r"(?i)\blaborator", r"\bLAB_LOG\b", r"\bCLAIMS\b", r"\bAGENTS\b", r"(?i)\bchecks file"]
        for i, line in enumerate(f.read_text(encoding="utf-8").splitlines(), 1):
            bare = re.sub(r"`[^`]*`|\\[a-z]+(?:\[[a-z0-9]+\])?(?:\{[^{}]*\})+", " ", line)
            found = [re.search(pat, bare) for pat in patterns]
            if rel.parts[0] == "related":  # a pointer to a file or a note of the lab inside a verified statement
                found.append(re.search(r"\b[\w/]+\.md\b|for the editor", line))
            hits += [f"{rel}:{i}: '{m.group(0)}'" for m in found if m]
    return list(dict.fromkeys(hits))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("section", nargs="?")
    ap.add_argument("--also", nargs="*", default=[])
    ap.add_argument("--accepted", nargs="*", default=[])
    ap.add_argument("--brief")
    ap.add_argument("--check", nargs="+", metavar="FILE")
    a = ap.parse_args()
    if a.check:
        hits = scan(ROOT, [Path(f) for f in a.check])
        print("\n".join(hits) if hits else "clean: " + ", ".join(a.check))
        return 1 if hits else 0
    if not a.section:
        ap.error("give the section to write, or --check FILE...")
    nn = a.section

    def section_files(numbers: list[str]) -> list[Path]:
        return [f for n in numbers for f in sorted((ROOT / "sections").glob(f"{n}_*.tex"))]

    own = section_files([nn] + a.also)
    if not own:
        sys.exit(f"STOP: no file sections/{nn}_*.tex")
    if a.brief:
        brief = Path(a.brief)
    else:
        briefs = [f for f in sorted((ROOT / "briefs").glob(f"{nn}_*.md")) if not NOT_A_BRIEF.search(f.name)]
        if len(briefs) != 1:
            sys.exit(f"STOP: expected one brief briefs/{nn}_name.md, found {[b.name for b in briefs]}")
        brief = briefs[0]
    brief_text = brief.read_text(encoding="utf-8")

    pack = ROOT / "build" / f"pack_{nn}"
    shutil.rmtree(pack, ignore_errors=True)
    for d in ("results", "related", "examples", "sections"):
        (pack / d).mkdir(parents=True)
    listing: list[tuple[str, str]] = []

    guide = (ROOT / "WRITING_GUIDE.md").read_text(encoding="utf-8")
    cut = guide.index("# Working guide")
    (pack / "paper.md").write_text(guide[:cut].rstrip() + "\n", encoding="utf-8")
    (pack / "guide.md").write_text(guide[cut:], encoding="utf-8")
    shutil.copy(ROOT / "VOICE_GUIDE.md", pack / "voice.md")
    shutil.copy(ROOT / "TERMS.md", pack / "terms.md")
    (pack / "brief.md").write_text(brief_text, encoding="utf-8")
    listing += [("paper.md", "the manuscript on one page"), ("guide.md", "how to work, and what binds"),
                ("voice.md", "the register, and the organization of each kind of section"),
                ("terms.md", "terminology and notation"), ("brief.md", "this section: its aim, its points, its materials")]

    macros, unknown = macros_md()
    (pack / "results/macros.md").write_text(macros, encoding="utf-8")
    settings = (ROOT / "generated/settings.md").read_text(encoding="utf-8")
    settings = "# Settings\n\n" + drop_columns(settings[settings.index("| Group"):], {"Source"})
    (pack / "results/settings.md").write_text(settings, encoding="utf-8")
    listing += [("results/macros.md", "every result macro with what it prints"),
                ("results/settings.md", "every configuration value with its macro")]
    for name, what in FLOATS.items():
        src = ROOT / ("figures" if name.endswith(".pdf") else "generated") / name
        if not src.exists():
            print(f"note: {src.relative_to(ROOT)} is missing")
            continue
        if name.endswith(".tex"):
            text = "".join(l for l in src.read_text(encoding="utf-8").splitlines(True) if not l.startswith("%%"))
            (pack / "results" / name).write_text(text, encoding="utf-8")
            what += f"; included with \\input{{generated/{name[:-4]}}}"
        else:
            shutil.copy(src, pack / "results" / name)
        listing.append((f"results/{name}", what))
    floats = ROOT / "build/floats.pdf"
    if floats.exists():
        shutil.copy(floats, pack / "results/tables_rendered.pdf")
        listing.append(("results/tables_rendered.pdf", "every table and chart as it prints"))
    else:
        print("note: build/floats.pdf is missing (make floats)")

    bib = bib_entries()
    store = ROOT / ".sources/abstracts.json"
    abstracts = json.loads(store.read_text(encoding="utf-8")) if store.exists() else {}
    keys = [k for k in bib if re.search(rf"(?<![\w-]){re.escape(k)}(?![\w-])", brief_text)]
    for k in keys:
        (pack / "related" / f"{k}.md").write_text(related_md(k, bib[k], abstracts), encoding="utf-8")
        if k not in abstracts:
            print(f"note: no abstract stored for {k} (tools/abstracts.py)")
    listing.append(("related/", f"the {len(keys)} cited works of the brief, one file per citation key: abstract and verified statements"))

    examples = sorted((ROOT / ".sources/examples").glob("*.pdf"))
    for f in examples:
        shutil.copy(f, pack / "examples" / f.name)
    if not examples:
        print("note: no example paper in .sources/examples/")
    listing.append(("examples/", "published papers on other subjects, as examples of form; they supply neither facts nor wording"))

    for f in section_files(a.accepted):
        shutil.copy(f, pack / "sections" / f.name)
        listing.append((f"sections/{f.name}", "written"))
    for f in own:
        shutil.copy(f, pack / "sections" / f.name)
        listing.append((f"sections/{f.name}", "to write"))

    readme = ["# Files", "", "| File | Content |", "|---|---|"] + [f"| `{n}` | {w} |" for n, w in listing]
    readme += ["", "Your own files go to `notes/` and to the files marked \"to write\"."]
    (pack / "README.md").write_text("\n".join(readme) + "\n", encoding="utf-8")

    title = re.search(r"\\section\{([^}]*)\}", own[0].read_text(encoding="utf-8"))
    start = START.format(n=int(nn), title=title.group(1) if title else own[0].stem, web=WEB if nn in WEB_SECTIONS else "")
    (ROOT / "build" / f"start_{nn}.md").write_text(start, encoding="utf-8")

    print(f"build/pack_{nn}/: {sum(1 for f in pack.rglob('*') if f.is_file())} files; brief {brief.name}; "
          f"{len(keys)} cited works; web {'on' if nn in WEB_SECTIONS else 'off (-N)'}")
    status = 0
    if unknown:
        print("STOP: macro arguments without a name in tools/pack.py (SETS, ROWS, MODELS): " + ", ".join(unknown))
        status = 1
    hits = scan(pack)
    if hits:
        print(f"STOP: {len(hits)} traces of the lab in the pack; correct them in the source file")
        print("\n".join("  " + h for h in hits[:40]))
        status = 1
    return status


if __name__ == "__main__":
    sys.exit(main())
