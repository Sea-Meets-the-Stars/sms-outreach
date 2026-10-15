"""Created by JXP and Claude.

Build a deck from a plan file, run QA, and (optionally) render it to PDF.

Usage (ocean14 env):
    python -m sms_outreach.slides.build talks/wmko_2026/slides/plan.py [-o OUT.pptx] [--pdf] [--png] [--strict]

--pdf renders OUT.pdf next to the deck with LibreOffice (soffice --headless);
--png also writes one low-resolution PNG per page (pdftoppm) into
OUT_pages/ for a quick visual check.
"""
import argparse
import runpy
import shutil
import subprocess
import sys
from pathlib import Path

from . import qa
from .deck import build_deck


def load_plan(path):
    """Created by JXP and Claude. Execute a plan file and return its namespace
    (TEMPLATE, FIG_DIRS, OUTPUT, SLIDES, optional MAX_SLIDES)."""
    ns = runpy.run_path(str(path))
    for key in ("TEMPLATE", "FIG_DIRS", "OUTPUT", "SLIDES"):
        if key not in ns:
            raise KeyError(f"plan file {path} does not define {key}")
    return ns


def render_pdf(pptx, png=False):
    """Created by JXP and Claude. LibreOffice -> PDF (and pdftoppm -> PNGs).
    Returns the PDF path."""
    pptx = Path(pptx)
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(pptx.parent), str(pptx)],
                   check=True, capture_output=True)
    pdf = pptx.with_suffix(".pdf")
    if png:
        pages = pptx.parent / (pptx.stem + "_pages")
        shutil.rmtree(pages, ignore_errors=True)
        pages.mkdir()
        subprocess.run(["pdftoppm", "-r", "60", "-png", str(pdf), str(pages / "p")], check=True)
    return pdf


def main(argv=None):
    """Created by JXP and Claude. Command-line entry point."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("plan", help="plan file (python) defining TEMPLATE, FIG_DIRS, OUTPUT, SLIDES")
    p.add_argument("-o", "--output", help="override OUTPUT")
    p.add_argument("--pdf", action="store_true", help="render a PDF with LibreOffice")
    p.add_argument("--png", action="store_true", help="also write per-page PNGs (implies --pdf)")
    p.add_argument("--strict", action="store_true", help="QA warnings (notes, sources) count as failures")
    args = p.parse_args(argv)

    plan = load_plan(args.plan)
    out = Path(args.output or plan["OUTPUT"]).expanduser()
    prs, report = build_deck(plan["TEMPLATE"], plan["SLIDES"], plan["FIG_DIRS"], plan.get("CACHE_DIR"))
    for n, title, what in report:
        print(f"slide {n:2d}: {title[:48]:48s} {what}")
    out.parent.mkdir(parents=True, exist_ok=True)
    prs.save(str(out))
    print(f"wrote {out}: {len(prs.slides)} slides, {out.stat().st_size / 1e6:.1f} MB")

    n_backup = sum(s.backup for s in plan["SLIDES"])
    ok = qa.report(out, plan.get("MAX_SLIDES"), n_backup, strict=args.strict)
    if args.pdf or args.png:
        pdf = render_pdf(out, png=args.png)
        print(f"rendered {pdf}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
