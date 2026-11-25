"""Render a figure SVG of this folder to PNG and PDF with headless Chrome.

    python3 paper/figures/render.py paper/figures/fig_method_overview.svg
    python3 paper/figures/render.py paper/figures/fig_method_overview.svg --eps

The SVG is drawn in points at its printed size (STYLE.md), so --scale is
pixels per point: 6 gives 432 dpi for drafts and email. The PDF keeps the
figure as vectors at its printed size, with the fonts embedded. --eps also
writes a vector EPS from that PDF, the format both target journals take for
line art; it needs pdftops (poppler). Standard library only.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"


def size_of(svg: str) -> tuple[float, float]:
    box = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', svg)
    if not box:
        raise SystemExit('the SVG needs viewBox="0 0 W H" in points')
    return float(box.group(1)), float(box.group(2))


def chrome(profile: str, *args: str) -> None:
    command = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars",
               f"--user-data-dir={profile}", *args]
    done = subprocess.run(command, capture_output=True, text=True, timeout=120)
    if done.returncode != 0:
        raise SystemExit(done.stderr.strip() or "Chrome failed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("svg", type=Path)
    parser.add_argument("--scale", type=float, default=6.0, help="pixels per point of the PNG")
    parser.add_argument("--eps", action="store_true", help="also write a vector EPS for submission")
    args = parser.parse_args()

    source = args.svg.resolve()
    text = source.read_text(encoding="utf-8")
    width, height = size_of(text)
    body = text[text.index("<svg"):]
    png, pdf = source.with_suffix(".png"), source.with_suffix(".pdf")

    with tempfile.TemporaryDirectory() as tmp:
        base = "<!doctype html><meta charset='utf-8'><style>html,body{margin:0;background:#fff}svg{display:block}"
        screen = Path(tmp) / "screen.html"
        screen.write_text(f"{base}svg{{width:{width}px;height:{height}px}}</style>{body}", encoding="utf-8")
        paper = Path(tmp) / "paper.html"
        paper.write_text(
            f"{base}@page{{size:{width}pt {height}pt;margin:0}}svg{{width:{width}pt;height:{height}pt}}</style>{body}",
            encoding="utf-8",
        )
        profile = str(Path(tmp) / "profile")
        chrome(profile, f"--window-size={round(width)},{round(height)}",
               f"--force-device-scale-factor={args.scale}", f"--screenshot={png}", screen.as_uri())
        chrome(profile, "--no-pdf-header-footer", f"--print-to-pdf={pdf}", paper.as_uri())

    written = [png, pdf]
    if args.eps:
        pdftops = shutil.which("pdftops")
        if not pdftops:
            raise SystemExit("--eps needs pdftops (brew install poppler)")
        eps = source.with_suffix(".eps")
        subprocess.run([pdftops, "-eps", "-level3", str(pdf), str(eps)], check=True)
        written.append(eps)

    for out in written:
        if not out.exists():
            sys.exit(f"not written: {out}")
        print(out)


if __name__ == "__main__":
    main()
