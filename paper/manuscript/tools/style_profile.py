#!/usr/bin/env python3
"""Style measures of published papers by kind of section, and of a draft against them.

  style_profile.py profile --sources DIR [--out FILE]   measure the reference papers
  style_profile.py compare FILE.tex --sources DIR       one draft section beside them

DIR holds the LaTeX source of each paper in a folder named by its arXiv id (the sources
are downloaded from arXiv and are not kept in the repository). The measures are those of
the ARS style calibration protocol: sentence length, paragraph length, vocabulary (hedges,
transitions, reporting verbs, formality), citation integration, modifiers, and how they
shift between the kinds of section. They describe a register; none of them is a target.
"""
from __future__ import annotations

import argparse
import re
import statistics
from collections import Counter
from pathlib import Path

# arXiv id: (short name, venue, main file)
PAPERS = {
    "2509.01308": ("GradeSQL", "J. Intell. Inf. Syst. 2026", "x/main.tex"),
    "2402.16347": ("CodeS", "SIGMOD 2024", "x/main.tex"),
    "2305.03111": ("BIRD", "NeurIPS 2023 (Datasets and Benchmarks)", "x/neurips_data_2023.tex"),
    "2010.02840": ("Test suites", "EMNLP 2020", "x/emnlp2020.tex"),
    "2411.05199": ("CodeLutra", "", "tmlr.tex"),
    "2305.18290": ("DPO", "NeurIPS 2023", "x/main.tex"),
    "2106.09685": ("LoRA", "ICLR 2022", "x/iclr2022_conference.tex"),
    "1602.05629": ("FedAvg", "AISTATS 2017", "x/aistats17_fed_averaging.tex"),
    "1812.06127": ("FedProx", "MLSys 2020", "x/FedProx_CRC.tex"),
    "2402.06954": ("OpenFedLLM", "", "x/main.tex"),
}
KINDS = ["introduction", "related work", "method", "experiments", "discussion and conclusion"]
KIND_PATTERNS = [
    ("introduction", r"introduction"),
    ("related work", r"related|background|prior work|existing solutions"),
    ("discussion and conclusion", r"discussion|conclusion|conlusion|limitation|future|broader|ethic"),
    ("experiments", r"experiment|result|evaluation|analysis|ablation|setup|empirical|understanding|benchmark|statistic"),
    ("method", r"method|approach|framework|algorithm|preliminar|overview|optimization|our |desiderata|fuzz|"
               r"problem|construction|annotation|pipeline|design|training|model|theor|test suite|data|codelutra|adaption"),
]
HEDGES = ["may", "might", "could", "suggest", "suggests", "indicate", "indicates", "appear", "appears", "likely",
          "possibly", "potentially", "hypothesize", "seems", "seem", "presumably", "roughly", "approximately"]
TRANSITIONS = ["however", "thus", "therefore", "moreover", "furthermore", "in contrast", "specifically", "for example",
               "for instance", "additionally", "finally", "instead", "notably", "in particular", "in addition",
               "consequently", "hence", "as a result", "similarly", "nevertheless", "importantly", "intuitively",
               "in practice", "to this end", "that is", "in other words", "while", "although", "whereas", "since",
               "because"]
REPORTING = ["show", "shows", "showed", "shown", "find", "finds", "found", "propose", "proposes", "proposed",
             "demonstrate", "demonstrates", "demonstrated", "observe", "observes", "observed", "report", "reports",
             "reported", "introduce", "introduces", "introduced", "present", "presents", "presented", "argue",
             "argues", "note", "notes", "noted", "achieve", "achieves", "achieved", "outperform", "outperforms",
             "improve", "improves", "improved", "evaluate", "evaluates", "evaluated", "compare", "compares",
             "compared", "adopt", "adopts", "adopted", "employ", "employs", "employed", "use", "uses", "used",
             "leverage", "leverages", "utilize", "utilizes", "utilized", "denote", "denotes", "denoted", "define",
             "defines", "defined", "consider", "considers", "considered"]
INTENSIFIERS = ["very", "significantly", "highly", "extremely", "substantially", "remarkably", "greatly", "strongly",
                "considerably", "dramatically", "notably", "clearly", "consistently", "effectively"]
EVERYDAY = ["write", "writes", "wrote", "run", "runs", "give", "gives", "get", "gets", "say", "says", "keep", "keeps",
            "leave", "leaves", "hold", "holds", "let", "lets", "teach", "right", "built", "cut"]
# how the field names the things this paper describes: one group per concept
TERMS = {
    "the SQL a model outputs": ["predicted sql", "generated sql", "sql candidate", "candidate sql", "candidates",
                                "candidate", "sampled", "samples", "responses", "predictions", "outputs", "completions"],
    "the reference SQL": ["gold sql", "gold query", "ground-truth", "ground truth", "reference sql", "gold"],
    "producing SQL": ["generate", "generates", "generated", "generating", "sample", "sampling", "predict", "predicts",
                      "write", "writes"],
    "running SQL": ["execute", "executes", "executed", "executing", "execution", "run", "runs", "running"],
    "outcome of a query": ["correct", "incorrect", "wrong", "erroneous", "failed", "rejected", "preferred",
                           "dispreferred", "execution error", "syntax error", "executable"],
    "federated roles": ["client", "clients", "device", "devices", "participant", "participants", "server",
                        "global model", "local model", "local training", "communication round", "round", "rounds",
                        "aggregate", "aggregation"],
    "adapting a model": ["fine-tune", "fine-tuning", "fine-tuned", "finetune", "finetuning", "train", "training",
                         "optimize", "optimization", "adapt", "adaptation"],
}

ENV = (r"equation|align|algorithm|algorithmic|wrapfigure|wraptable|figure|table|tabular|lstlisting|tcolorbox|"
       r"gather|multline|eqnarray|minipage|verbatim|tikzpicture|subfigure|displaymath|array|CCSXML|abstract")


def expand(path: Path, depth: int = 0) -> str:
    text = re.sub(r"(?m)(?<!\\)%.*$", "", path.read_text(encoding="utf-8", errors="replace"))
    if depth > 4:
        return text

    def sub(m: re.Match) -> str:
        name = m.group(1).strip()
        for cand in (path.parent / name, path.parent / (name + ".tex")):
            if cand.is_file():
                return expand(cand, depth + 1)
        return " "
    return re.sub(r"\\(?:input|include)\{([^}]+)\}", sub, text)


def body(text: str) -> str:
    start = text.find("\\begin{document}")
    text = text[start:] if start >= 0 else text
    ends = [m.start() for m in re.finditer(r"\\appendix\b|\\begin\{appendi|\\bibliography\{|\\begin\{thebibliography\}"
                                           r"|\\printbibliography", text)]
    return text[:min(ends)] if ends else text


def strip_floats(text: str) -> str:
    for _ in range(3):
        text = re.sub(r"\\begin\{(%s)\*?\}.*?\\end\{\1\*?\}" % ENV, " ", text, flags=re.S)
    text = re.sub(r"\$\$.*?\$\$", " ", text, flags=re.S)
    return re.sub(r"\\\[.*?\\\]", " ", text, flags=re.S)


def cite_counts(par: str) -> tuple[int, int]:
    """(narrative, parenthetical) citations of a paragraph, counted on the raw LaTeX."""
    narrative = len(re.findall(r"\\(?:citet|citeauthor|textcite|citeyear)\*?(?:\[[^\]]*\])*\{", par))
    narrative += len(re.findall(r"et al\.?[~\s]*\\cite[p]?\*?(?:\[[^\]]*\])*\{", par))
    every = len(re.findall(r"\\[a-zA-Z]*cite[a-zA-Z]*\*?(?:\[[^\]]*\])*\{", par))
    return narrative, max(every - narrative, 0)


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


def sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z])", text) if len(s.split()) >= 4]


def kind_of(title: str) -> str | None:
    low = title.lower()
    for kind, pat in KIND_PATTERNS:
        if re.search(pat, low):
            return kind
    return None


def split_sections(text: str) -> list[tuple[str, str]]:
    marks = list(re.finditer(r"\\section\*?\{((?:[^{}]|\{[^{}]*\})*)\}", text))
    return [(m.group(1), text[m.end():(marks[i + 1].start() if i + 1 < len(marks) else len(text))])
            for i, m in enumerate(marks)]


class Measure:
    def __init__(self) -> None:
        self.sent_len: list[int] = []
        self.par_sents: list[int] = []
        self.words: list[str] = []
        self.sents: list[str] = []
        self.narrative = self.parenthetical = self.paragraphs = 0

    def add(self, raw: str) -> None:
        for par in re.split(r"\n\s*\n", strip_floats(raw)):
            clean = detex(par)
            if len(clean.split()) < 20:
                continue
            ss = sentences(clean)
            if not ss:
                continue
            n, p = cite_counts(par)
            self.narrative += n
            self.parenthetical += p
            self.paragraphs += 1
            self.par_sents.append(len(ss))
            self.sents.extend(ss)
            self.sent_len.extend(len(s.split()) for s in ss)
            self.words.extend(w.lower() for w in re.findall(r"[A-Za-z][A-Za-z\-']+", clean) if w != "X")

    def rate(self, vocab: list[str]) -> float:
        text = " " + " ".join(self.words) + " "
        hits = sum(text.count(" " + v + " ") for v in vocab)
        return 1000 * hits / max(len(self.words), 1)

    def top(self, vocab: list[str], k: int = 8) -> str:
        text = " " + " ".join(self.words) + " "
        c = Counter({v: text.count(" " + v + " ") for v in vocab})
        return ", ".join(f"{v} {n}" for v, n in c.most_common(k) if n)

    def row(self) -> dict:
        n = max(len(self.words), 1)
        s = max(len(self.sents), 1)
        we = sum(bool(re.search(r"\b(?:we|our|us)\b", x, flags=re.I)) for x in self.sents)
        passive = sum(bool(re.search(r"\b(?:is|are|was|were|be|been|being)\s+(?:\w+ly\s+)?\w+(?:ed|en|own|ade|uilt)\b", x))
                      for x in self.sents)
        cites = self.narrative + self.parenthetical
        return {
            "words": len(self.words),
            "sentence mean": statistics.mean(self.sent_len) if self.sent_len else 0,
            "sentence sd": statistics.pstdev(self.sent_len) if self.sent_len else 0,
            "paragraph sentences": statistics.mean(self.par_sents) if self.par_sents else 0,
            "letters per word": sum(map(len, self.words)) / n,
            "long words %": 100 * sum(len(w) >= 9 for w in self.words) / n,
            "we sentences %": 100 * we / s,
            "passive sentences %": 100 * passive / s,
            "hedges /1k": self.rate(HEDGES),
            "intensifiers /1k": self.rate(INTENSIFIERS),
            "-ly adverbs /1k": 1000 * sum(w.endswith("ly") and len(w) > 4 for w in self.words) / n,
            "everyday verbs /1k": self.rate(EVERYDAY),
            "citations per paragraph": cites / max(self.paragraphs, 1),
            "narrative citations %": 100 * self.narrative / cites if cites else 0,
        }


COLS = ["words", "sentence mean", "sentence sd", "paragraph sentences", "letters per word", "long words %",
        "we sentences %", "passive sentences %", "hedges /1k", "intensifiers /1k", "-ly adverbs /1k",
        "everyday verbs /1k", "citations per paragraph", "narrative citations %"]


def fmt(v: float, col: str) -> str:
    return f"{int(v):,}" if col == "words" else f"{v:.2f}" if col == "letters per word" else f"{v:.1f}"


def table(rows: list[tuple[str, dict]]) -> str:
    out = ["| | " + " | ".join(COLS) + " |", "|---|" + "---:|" * len(COLS)]
    out += [f"| {name} | " + " | ".join(fmt(r[c], c) for c in COLS) + " |" for name, r in rows]
    return "\n".join(out)


def load(sources: Path) -> tuple[dict, dict, list[str]]:
    by_kind = {k: Measure() for k in KINDS}
    by_paper, unmatched = {}, []
    for arxiv, (name, _venue, main) in PAPERS.items():
        path = sources / arxiv / main
        if not path.is_file():
            raise SystemExit(f"missing source: {path}")
        whole = Measure()
        for title, text in split_sections(body(expand(path))):
            kind = kind_of(title)
            whole.add(text)
            if kind is None:
                unmatched.append(f"{name}: {title}")
            else:
                by_kind[kind].add(text)
        by_paper[name] = whole
    return by_kind, by_paper, unmatched


def profile(sources: Path, out: Path | None) -> None:
    by_kind, by_paper, unmatched = load(sources)
    lines = ["# Style measures of the reference papers", "",
             "Written by `tools/style_profile.py profile`. Do not edit.", "",
             "Papers: " + "; ".join(f"{n} ({v + ', ' if v else ''}arXiv {a})" for a, (n, v, _m) in PAPERS.items()) + ".", "",
             "## By kind of section, the ten papers together", "", table([(k, by_kind[k].row()) for k in KINDS]), "",
             "## By paper, all sections", "", table([(n, m.row()) for n, m in by_paper.items()]), "",
             "## Words, by kind of section (count in the ten papers)", ""]
    for label, vocab in (("Hedges", HEDGES), ("Transitions", TRANSITIONS), ("Reporting and method verbs", REPORTING)):
        lines += [f"### {label}", "", "| Kind of section | Most used |", "|---|---|"]
        lines += [f"| {k} | {by_kind[k].top(vocab, 10)} |" for k in KINDS] + [""]
    everything = Measure()
    for m in by_paper.values():
        everything.words += m.words
    lines += ["## How the papers name things (count in the ten papers, all sections)", "",
              "| Concept | Terms |", "|---|---|"]
    lines += [f"| {concept} | {everything.top(vocab, 12)} |" for concept, vocab in TERMS.items()]
    if unmatched:
        lines += ["", "Section titles not assigned to a kind: " + "; ".join(unmatched) + "."]
    text = "\n".join(lines) + "\n"
    if out:
        out.write_text(text, encoding="utf-8")
        print(out)
    else:
        print(text)


def compare(path: Path, sources: Path, kind: str) -> None:
    by_kind, _by_paper, _ = load(sources)
    draft = Measure()
    draft.add(re.sub(r"(?m)(?<!\\)%.*$", "", path.read_text(encoding="utf-8")))
    print(table([(path.name, draft.row()), (f"reference: {kind}", by_kind[kind].row())]))
    print("\neveryday verbs in the draft:", draft.top(EVERYDAY, 12) or "none")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("profile")
    p.add_argument("--sources", type=Path, required=True)
    p.add_argument("--out", type=Path)
    c = sub.add_parser("compare")
    c.add_argument("file", type=Path)
    c.add_argument("--sources", type=Path, required=True)
    c.add_argument("--kind", choices=KINDS, default="method")
    args = ap.parse_args()
    if args.cmd == "profile":
        profile(args.sources, args.out)
    else:
        compare(args.file, args.sources, args.kind)


if __name__ == "__main__":
    main()
