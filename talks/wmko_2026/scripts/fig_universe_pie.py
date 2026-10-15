"""Created by JXP and Claude.

Donut chart of what the Universe is made of, for the slide
"HIRES: weighing the Universe and finding planets" (WMKO 2026 public
lecture, Sea meets the stars).  It sits on the right half of the slide
next to the HIRES photo and replaces the D/H-vs-Omega_b plot, which was
too technical for a public audience.

Three slices: dark energy, dark matter and ordinary matter.  The ordinary
matter slice -- everything we can see: stars, gas, planets, us -- is the
one that HIRES deuterium measurements weigh, so it is gold and pulled out
of the ring; the two dark slices are muted indigo and gray.

Values: Planck 2018 base-LCDM, TT,TE,EE+lowE+lensing (Planck Collaboration
2020, A&A 641, A6, Table 2):
    Omega_Lambda = 0.6847,  Omega_c = 0.2645,  Omega_b = 0.0493
rounded for the public to 68 % / 27 % / 5 % (sum 100).

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or $SOURCES_JSON if set):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_universe_pie.py

Output: talks/wmko_2026/figures/universe_pie.png
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Wedge
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import STARS_GOLD, INK, MUTED

FIGS = Path(__file__).resolve().parents[1] / "figures"

# Planck 2018 (A&A 641, A6, Table 2, TT,TE,EE+lowE+lensing) density parameters.
PLANCK = {"dark energy": 0.6847, "dark matter": 0.2645, "ordinary matter": 0.0493}
# Public-facing rounded percentages (must sum to 100).
PERCENT = {"dark energy": 68, "dark matter": 27, "ordinary matter": 5}

GOLD_DARK = "#9c6f00"        # outline / text for the gold slice
INDIGO_MUTED = "#4e4c8f"     # dark energy (lightened night-sky indigo)
GRAY_MUTED = "#a9adb3"       # dark matter
COLORS = {"dark energy": INDIGO_MUTED, "dark matter": GRAY_MUTED,
          "ordinary matter": STARS_GOLD}

# Layout in inches: the axes shows (0, W) x (0, H) at equal aspect, so font
# sizes in points map directly onto the canvas (1 pt = 1/72 in).
FIGSIZE = (style.HALF[0], 3.7)
W, H = 4.0, 3.25
CX, CY = 0.98, 1.60          # donut centre
R_OUT, R_IN = 0.88, 0.50     # donut radii
EXPLODE = 0.15               # how far the gold slice is pulled out
MID_ORDINARY = 35.0          # degrees; the gold slice points at the call-out
X_COL = 2.12                 # left edge of the call-out text column


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def check_values():
    """Created by JXP and Claude. Sanity-check the Planck values and the
    public rounding before drawing anything."""
    total = sum(PLANCK.values())
    assert abs(total - 1.0) < 0.01, f"Planck Omegas sum to {total:.4f}"
    assert sum(PERCENT.values()) == 100, "rounded percentages must sum to 100"
    for k in PLANCK:
        assert abs(100 * PLANCK[k] - PERCENT[k]) < 1.5, k


def draw_donut(ax):
    """Created by JXP and Claude. Draw the three wedges clockwise from the
    gold slice, exploding the ordinary-matter slice.  Returns
    {name: mid-angle in degrees}."""
    order = ["ordinary matter", "dark energy", "dark matter"]
    ang = MID_ORDINARY + 180.0 * PERCENT["ordinary matter"] / 100.0  # start
    mids = {}
    for name in order:
        span = 360.0 * PERCENT[name] / 100.0
        a0, a1 = ang - span, ang            # clockwise: angles decrease
        mid = 0.5 * (a0 + a1)
        mids[name] = mid
        gold = name == "ordinary matter"
        cx, cy = CX, CY
        if gold:
            cx += EXPLODE * np.cos(np.radians(mid))
            cy += EXPLODE * np.sin(np.radians(mid))
        ax.add_patch(Wedge((cx, cy), R_OUT, a0, a1, width=R_OUT - R_IN,
                           facecolor=COLORS[name],
                           edgecolor=GOLD_DARK if gold else "white",
                           lw=2.0 if gold else 2.5, zorder=3 if gold else 2))
        ang = a0
    return mids


def draw_labels(ax, mids):
    """Created by JXP and Claude. Big plain-word labels outside the ring:
    dark matter above, dark energy below, and a gold call-out column to the
    right for ordinary matter (which the exploded slice points at) with a
    short description and the HIRES/deuterium note."""
    pct = dict(ha="center", fontsize=22, color=INK, zorder=5,
               path_effects=bold(INK, 0.9))
    name = dict(ha="center", fontsize=16, color=INK, zorder=5)

    # --- dark matter: stacked above the ring (its slice spans the top)
    y = CY + R_OUT + 0.06
    ax.text(CX, y, "dark matter", va="bottom", **name)
    ax.text(CX, y + 0.26, f"{PERCENT['dark matter']}%", va="bottom", **pct)

    # --- dark energy: stacked below the ring (its slice spans the bottom)
    y = CY - R_OUT - 0.06
    ax.text(CX, y, f"{PERCENT['dark energy']}%", va="top", **pct)
    ax.text(CX, y - 0.32, "dark energy", va="top", **name)

    # --- ordinary matter: gold call-out column to the right, with "5%"
    # level with the tip of the exploded slice (no leader line needed)
    th = np.radians(mids["ordinary matter"])
    y_tip = CY + (R_OUT + EXPLODE) * np.sin(th)
    y_top = y_tip + 0.48
    ax.text(X_COL, y_top, "5%", ha="left", va="top", fontsize=30,
            color=GOLD_DARK, path_effects=bold(GOLD_DARK, 1.3), zorder=5)
    ax.text(X_COL, y_top - 0.44, "ordinary matter", ha="left", va="top",
            fontsize=19, color=GOLD_DARK, path_effects=bold(GOLD_DARK, 0.9),
            zorder=5)
    ax.text(X_COL, y_top - 0.82, "everything we can see:\nstars, gas, planets, us",
            ha="left", va="top", fontsize=14, color=INK, linespacing=1.15,
            zorder=5)
    ax.text(X_COL, y_top - 1.36, "weighed with deuterium\n(HIRES)", ha="left",
            va="top", fontsize=13, color=MUTED, style="italic",
            linespacing=1.15, zorder=5)


def make_figure():
    """Created by JXP and Claude. Build and save the donut chart."""
    check_values()
    style.apply_style()
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.set_axis_off()
    mids = draw_donut(ax)
    draw_labels(ax, mids)
    ax.text(CX, CY, "the\nUniverse", ha="center", va="center", fontsize=14,
            color=INK, linespacing=1.1, zorder=5)
    return style.save(fig, FIGS, "universe_pie.png",
                      source="Planck 2018 (A&A 641, A6)",
                      slide="HIRES: weighing the Universe and finding planets",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
