"""Created by JXP and Claude.

Public version of Phil Hinz's glass-slumping result for the slide
"WMKO + AI: building new optics" (WMKO 2026 public lecture, Sea meets the
stars).  Replaces three technical plots with one side-view cartoon:

  1. Before: a flat glass disk (1.6 m across) resting on a ring, with
     ~9 kg of sand piled on it in the dome shape Claude's model chose.
  2. Into the furnace (1170 °F).
  3. After: the glass has sagged into a curved shell, 65 mm deep at the
     centre, matching the shape needed to better than half a micron.

Numbers are from Hinz's slides (context/Integrating Claude into
instrumentation research.pptx, slide 2: sand peak 5.7 mm, 9.2 kg, base ring
r = 800 mm, optical aperture r = 700 mm, deflection ~65 mm at 1170 °F,
optical-aperture residual P-V = 0.476 µm).  Vertical sizes are exaggerated
for clarity; this is an illustration, not a plot.

Run from the repo root (conda run does not pass stdin):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_hinz_public.py

Output: talks/wmko_2026/figures/hinz_public.png
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon, Rectangle
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import SEA, STARS_GOLD, RED, INK, MUTED

FIGS = Path(__file__).resolve().parents[1] / "figures"
GLASS = "#9cc7e8"
GLASS_EDGE = SEA
SAND = "#d9c48f"
SAND_EDGE = "#8c6d3a"
RING = "#555555"
GOLD_DARK = "#9c6f00"

# Canvas in data units (1 unit ~ 0.1 in on the slide)
XMAX, YMAX = 92.0, 37.0
HALF = 15.0                  # half-width of the glass disk in canvas units (r = 800 mm)


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect (the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance)."""
    return [withStroke(linewidth=lw, foreground=color)]


def sand_profile(x):
    """Created by JXP and Claude. Dome-shaped sand height (canvas units) at
    canvas position x relative to the disk centre: zero outside the optical
    aperture (r = 700 mm), a smooth dome peaking at the centre (shape after
    Hinz's sand-height plot, height exaggerated)."""
    r = np.abs(x) / HALF * 800.0                      # mm
    h = np.where(r < 700.0, np.sqrt(np.clip(1 - (r / 700.0) ** 2, 0, 1)) ** 0.8, 0.0)
    return 4.0 * h


def draw_ring(ax, cx, y):
    """Created by JXP and Claude. The two visible posts of the support ring."""
    for sx in (-1, 1):
        ax.add_patch(Rectangle((cx + sx * HALF - 0.9, y - 5.0), 1.8, 5.0, color=RING, zorder=2))
    ax.plot([cx - HALF - 2.5, cx + HALF + 2.5], [y - 5.0, y - 5.0], color=RING, lw=2.5, zorder=2)


def draw_before(ax, cx, y):
    """Created by JXP and Claude. Flat glass on the ring with the sand dome."""
    draw_ring(ax, cx, y)
    ax.add_patch(Rectangle((cx - HALF, y), 2 * HALF, 1.0, facecolor=GLASS, edgecolor=GLASS_EDGE, lw=1.5, zorder=3))
    x = np.linspace(-HALF, HALF, 400)
    h = sand_profile(x)
    ax.fill_between(cx + x, y + 1.0, y + 1.0 + h, color=SAND, zorder=4)
    ax.plot(cx + x, y + 1.0 + h, color=SAND_EDGE, lw=2, zorder=5)
    ax.text(cx, y + 6.0, "~9 kg of sand\n(Claude's recipe)", fontsize=16, color=SAND_EDGE,
            ha="center", va="bottom", linespacing=1.1, zorder=6)
    ax.annotate("", xy=(cx - HALF, y - 7.0), xytext=(cx + HALF, y - 7.0),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.5))
    ax.text(cx, y - 8.6, "1.6 m of glass", ha="center", va="top", fontsize=16, color=MUTED)


def draw_after(ax, cx, y):
    """Created by JXP and Claude. The sagged shell (deflection exaggerated)."""
    draw_ring(ax, cx, y)
    x = np.linspace(-HALF, HALF, 400)
    sag = 4.2 * (1 - (x / HALF) ** 2) ** 1.0           # parabola-like, edges clamped (exaggerated)
    top = y + 1.0 - sag
    bot = y - sag
    poly = np.column_stack([np.r_[cx + x, (cx + x)[::-1]], np.r_[top, bot[::-1]]])
    ax.add_patch(Polygon(poly, closed=True, facecolor=GLASS, edgecolor=GLASS_EDGE, lw=1.5, zorder=3))
    ax.plot([cx - HALF, cx + HALF], [y + 1.0, y + 1.0], color=MUTED, lw=1, ls=":")
    ax.annotate("", xy=(cx, y - 4.2), xytext=(cx, y + 1.0),
                arrowprops=dict(arrowstyle="<->", color=MUTED, lw=1.5))
    ax.text(cx, y + 2.0, "sags 65 mm", ha="center", va="bottom", fontsize=16, color=MUTED)
    ax.text(cx, y - 8.6, "right shape to < ½ micron", ha="center", va="top", fontsize=18,
            color=GOLD_DARK, path_effects=bold(GOLD_DARK, 0.8))
    ax.text(cx, y - 11.7, "(1/100 of a hair's width)", ha="center", va="top", fontsize=15, color=MUTED)


def draw_furnace(ax, cx, y):
    """Created by JXP and Claude. Arrow with simple flames: into the furnace."""
    ax.add_patch(FancyArrowPatch((cx - 9, y), (cx + 9, y), arrowstyle="simple,head_width=12,head_length=12",
                                 mutation_scale=2.2, color=RED, zorder=2))
    for dx, s in ((-4.5, 1.0), (0.0, 1.3), (4.5, 1.0)):
        fx, fy = cx + dx, y - 6.5
        flame = Polygon([[fx - 1.4 * s, fy], [fx, fy + 4.2 * s], [fx + 1.4 * s, fy]], closed=True,
                        facecolor=STARS_GOLD, edgecolor=RED, lw=1.2, zorder=2)
        ax.add_patch(flame)
    ax.text(cx, y + 3.0, "furnace", ha="center", va="bottom", fontsize=18, color=INK,
            path_effects=bold(INK, 0.6))
    ax.text(cx, y - 8.5, "1170 °F", ha="center", va="top", fontsize=16, color=MUTED)


def make_figure():
    """Created by JXP and Claude. Before -> furnace -> after."""
    fig, ax = plt.subplots(figsize=style.FULL)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(3, YMAX)
    ax.set_aspect("equal")
    ax.axis("off")
    y0 = 19.0
    xb, xf, xa = 18.0, 46.0, 74.0
    ax.text(xb, YMAX - 1, "1. Flat glass + sand", ha="center", va="top", fontsize=21, color=INK,
            path_effects=bold(INK, 0.8))
    ax.text(xa, YMAX - 1, "2. A curved mirror shell", ha="center", va="top", fontsize=21, color=INK,
            path_effects=bold(INK, 0.8))
    draw_before(ax, xb, y0)
    draw_furnace(ax, xf, y0 + 1.0)
    draw_after(ax, xa, y0)
    return fig


def main():
    """Created by JXP and Claude. Draw and save the figure."""
    style.apply_style()
    fig = make_figure()
    style.save(fig, FIGS, "hinz_public.png",
               source="After Phil Hinz (UCSC): Claude's glass-slumping model for KASM; illustration, not to scale",
               slide="WMKO + AI: building new optics", sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    main()
