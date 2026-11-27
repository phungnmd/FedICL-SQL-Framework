#!/usr/bin/env python3
"""Draw the result charts of the paper from the committed evaluations.

  fig_rounds   Fig. 3: EX by round, FedAvg SFT and the method, BIRD dev and Spider test
  fig_errors   Fig. 4: incorrect predictions by round, split into execution errors and incorrect results

The points come from `curves()` of paper_numbers.py. The figure rules of the two journals
(paper/figures/STYLE.md, the table of journal limits) are built in:

  JIIS  119 mm wide, at most 195 mm high, parts lettered a, b
  CMC   119 mm wide (limit 165.1 mm), at most 200 mm high, parts lettered A, B

and for both: Arial of one size (8 pt), lines of 0.5 pt or more, no title inside the figure,
series told apart by marker, dash and hatch as well as colour, vector PDF with the fonts
embedded. The script stops if Arial is not found or a font is not embedded.

    uv run --no-project --with matplotlib==3.10.8 python tools/charts.py --journal jiis
"""
from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

import matplotlib

matplotlib.use("pdf")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib import font_manager  # noqa: E402

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_numbers as pn  # noqa: E402

FIG = HERE.parent / "figures"
MM = 1 / 25.4
JOURNALS = {
    "jiis": {"width": 119, "max_height": 195, "letters": "ab", "suffix": ""},
    "cmc": {"width": 119, "max_height": 200, "letters": "AB", "suffix": "_cmc"},
}
FONT, SIZE = "Arial", 8
BLUE, VIOLET, INK = "#2563EB", "#7C3AED", "#000000"   # federated side, the method (STYLE.md)
BLUE_FILL, VIOLET_FILL = "#E8F0FE", "#E9DFFD"
SETS = [("bird", "BIRD dev"), ("spider", "Spider test")]
SERIES = {
    "fedavg": {"label": "FedAvg SFT", "color": BLUE, "fill": BLUE_FILL, "marker": "o", "dash": (0, (4, 2))},
    "k2": {"label": "FedExec-SQL", "color": VIOLET, "fill": VIOLET_FILL, "marker": "s", "dash": "solid"},
}


def style() -> None:
    path = font_manager.findfont(FONT, fallback_to_default=False)
    if "arial" not in Path(path).name.lower():
        raise SystemExit(f"STOP: {FONT} not found (got {path})")
    plt.rcParams.update({
        "font.family": FONT, "font.size": SIZE, "axes.labelsize": SIZE, "axes.titlesize": SIZE,
        "xtick.labelsize": SIZE, "ytick.labelsize": SIZE, "legend.fontsize": SIZE,
        "text.color": INK, "axes.labelcolor": INK, "xtick.color": INK, "ytick.color": INK, "axes.edgecolor": INK,
        "axes.linewidth": 0.5, "xtick.major.width": 0.5, "ytick.major.width": 0.5, "lines.linewidth": 1.0,
        "lines.markersize": 4, "grid.linewidth": 0.5, "grid.color": "#CBD5E1", "hatch.linewidth": 0.5,
        "pdf.fonttype": 42, "axes.spines.top": False, "axes.spines.right": False,
        "legend.frameon": False, "savefig.transparent": False,
    })


def letter(ax, ch: str, name: str) -> None:
    """Part letter at the top left, with the name of the set beside it."""
    ax.text(0.0, 1.04, ch, transform=ax.transAxes, fontweight="bold", ha="left", va="bottom")
    ax.text(0.07, 1.04, name, transform=ax.transAxes, ha="left", va="bottom")


def fig_rounds(data: dict, j: dict):
    fig, axes = plt.subplots(1, 2, figsize=(j["width"] * MM, 58 * MM))
    for ax, (ds, name), ch in zip(axes, SETS, j["letters"]):
        for line in ("fedavg", "k2"):
            s, pts = SERIES[line], data[ds][line]
            ax.plot([p["r"] for p in pts], [p["ex"] for p in pts], color=s["color"], marker=s["marker"],
                    linestyle=s["dash"], markerfacecolor="white" if line == "fedavg" else s["color"],
                    markeredgewidth=1.0, label=s["label"], zorder=3 if line == "k2" else 2)
        ax.set_xlabel("Round")
        ax.set_xticks(range(0, max(p["r"] for p in data[ds]["fedavg"]) + 1))
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        letter(ax, ch, name)
    axes[0].set_ylabel("EX (%)")
    axes[1].legend(loc="lower right", handlelength=2.6)
    fig.tight_layout(pad=0.3, w_pad=1.2)
    return fig


def fig_errors(data: dict, j: dict):
    fig, axes = plt.subplots(1, 2, figsize=(j["width"] * MM, 62 * MM))
    width = 0.38
    for ax, (ds, name), ch in zip(axes, SETS, j["letters"]):
        rounds = [p["r"] for p in data[ds]["fedavg"]]
        both = {p["r"] for p in data[ds]["k2"]} - {pn.WARMUP}   # rounds with a bar of each line
        for line, off in (("fedavg", -width / 2), ("k2", width / 2)):
            s = SERIES[line]
            pts = [p for p in data[ds][line] if line == "fedavg" or p["r"] in both]  # the shared start is drawn once
            x = [p["r"] + (off if p["r"] in both else 0) for p in pts]
            err, wr = [p["err"] for p in pts], [p["wr"] for p in pts]
            ax.bar(x, wr, width, color=s["fill"], edgecolor=s["color"], linewidth=0.5)
            ax.bar(x, err, width, bottom=wr, color="white", edgecolor=s["color"], linewidth=0.5, hatch="////")
        ax.set_xlabel("Round")
        ax.set_xticks(rounds)
        ax.grid(axis="y")
        ax.set_axisbelow(True)
        letter(ax, ch, name)
    axes[0].set_ylabel("Incorrect predictions")
    from matplotlib.patches import Patch
    handles = [Patch(facecolor=SERIES["fedavg"]["fill"], edgecolor=BLUE, linewidth=0.5, label="FedAvg SFT, incorrect result"),
               Patch(facecolor="white", edgecolor=BLUE, linewidth=0.5, hatch="////", label="FedAvg SFT, execution error"),
               Patch(facecolor=SERIES["k2"]["fill"], edgecolor=VIOLET, linewidth=0.5, label="FedExec-SQL, incorrect result"),
               Patch(facecolor="white", edgecolor=VIOLET, linewidth=0.5, hatch="////", label="FedExec-SQL, execution error")]
    fig.legend(handles=handles, loc="lower center", ncol=2, handlelength=1.6, columnspacing=1.6, bbox_to_anchor=(0.5, 0.0))
    fig.tight_layout(pad=0.3, w_pad=1.2, rect=(0, 0.16, 1, 1))
    return fig


def check_pdf(path: Path, j: dict) -> None:
    """Size inside the journal limits, every font embedded and Arial."""
    if shutil.which("pdfinfo"):
        info = subprocess.run(["pdfinfo", str(path)], capture_output=True, text=True, check=True).stdout
        w, h = (float(x) for x in next(l for l in info.splitlines() if l.startswith("Page size")).split()[2:5:2])
        w_mm, h_mm = w / 72 * 25.4, h / 72 * 25.4
        if abs(w_mm - j["width"]) > 0.5 or h_mm > j["max_height"]:
            raise SystemExit(f"STOP: {path.name} is {w_mm:.1f} x {h_mm:.1f} mm")
    if shutil.which("pdffonts"):
        rows = subprocess.run(["pdffonts", str(path)], capture_output=True, text=True, check=True).stdout.splitlines()[2:]
        for line in rows:
            cols = line.split()
            emb = cols[-5]
            if "Arial" not in cols[0] or emb != "yes":
                raise SystemExit(f"STOP: {path.name}: font {cols[0]} (embedded: {emb})")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--journal", choices=sorted(JOURNALS), default="jiis")
    args = ap.parse_args()
    j = JOURNALS[args.journal]
    style()
    data = pn.curves()
    FIG.mkdir(exist_ok=True)
    for name, draw in (("fig_rounds", fig_rounds), ("fig_errors", fig_errors)):
        fig = draw(data, j)
        out = FIG / f"{name}{j['suffix']}.pdf"
        fig.savefig(out, metadata={"CreationDate": None, "ModDate": None})
        plt.close(fig)
        check_pdf(out, j)
        print(out.relative_to(HERE.parent))


if __name__ == "__main__":
    main()
