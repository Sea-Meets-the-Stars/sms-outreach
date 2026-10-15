"""Created by JXP and Claude.

Shared matplotlib style for slide figures (adapted from
ClimateIntelligence/presentations/py/slide_style.py, paths passed in).

Kraw-style slides are 10" x 5.625".  Figures are drawn at the physical size
they will occupy on the slide, so font sizes are what the audience sees:
  - FULL     : 9.2" x 3.4"  — spans the slide above a sub-line
  - FULL_TALL: 9.2" x 3.95" — spans the slide when there is no sub-line
  - HALF     : 4.45" x 3.4" — one side of a sea | stars pair
No in-figure titles (the slide title does that); the source goes on the
slide as text and into sources.json via `save`.
"""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # headless backend; we save PNGs, never display
import matplotlib.pyplot as plt

FULL = (9.2, 3.4)
FULL_TALL = (9.2, 3.95)
HALF = (4.45, 3.4)
DPI = 220

# Sea | stars palette: ocean blues on the left, night-sky indigo/gold on the right.
SEA, SEA_LIGHT, STARS, STARS_GOLD = "#1f5fa6", "#4a90d9", "#2c2a6b", "#e1a100"
RED, TEAL, GRAY = "#c0392b", "#16a085", "#7f8c8d"
INK, MUTED = "#222222", "#666666"


def apply_style():
    """Created by JXP and Claude. Set rcParams for slide-sized figures
    (large fonts, light grid, no top/right spines); registers the bundled
    Roboto so matplotlib can use it without a system install."""
    from matplotlib import font_manager
    from .layout import ROBOTO
    if "Roboto" not in {f.name for f in font_manager.fontManager.ttflist}:
        font_manager.fontManager.addfont(str(ROBOTO))
    plt.rcParams.update({
        "font.family": ["Roboto", "Helvetica Neue", "Arial", "DejaVu Sans"],
        "font.size": 15,
        "axes.labelsize": 16,
        "xtick.labelsize": 14,
        "ytick.labelsize": 14,
        "legend.fontsize": 13,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": "#444444",
        "text.color": INK,
        "axes.labelcolor": INK,
        "xtick.color": INK,
        "ytick.color": INK,
        "savefig.dpi": DPI,
        "savefig.facecolor": "white",
    })


def save(fig, out_dir, name, source, slide, sources_json=None):
    """Created by JXP and Claude. Save a slide figure and record its source.

    Inputs
    ------
    fig : matplotlib Figure (callers should not call tight_layout)
    out_dir : directory for the PNG
    name : file name, e.g. 'viirs_sst.png'
    source : data source (shown on the slide as text, kept in sources.json)
    slide : slide id or title it is made for
    sources_json : manifest path (default: out_dir/sources.json)

    Output: path of the written PNG.
    """
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    fig.tight_layout()
    out = out_dir / name
    fig.savefig(out)
    plt.close(fig)
    manifest_path = Path(sources_json) if sources_json else out_dir / "sources.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    entry = manifest.get(name, {})
    entry.update({"slide": slide, "source": source, "origin": "generated"})
    manifest[name] = entry
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {out}")
    return out
