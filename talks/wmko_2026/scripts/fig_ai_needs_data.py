"""Created by JXP and Claude.

Schematic for the slide "AI needs data" (sub-line "It can't solve what it
can't see"; WMKO 2026 public lecture, Sea meets the stars).

A left-to-right flow a lay audience can read in a few seconds:

  ?  -> Data  -> AI model -> People learn

  * A dashed, empty "?" box at the far left stands for the data nobody has
    collected yet (the bottleneck: no data, no answer).
  * Data -- a telescope dome on a mountain, a satellite, and a glider and
    profiling float under a wavy sea (all matplotlib patches; no images).
  * AI model -- a glowing, gold-edged neural-net card.
  * People learn -- three head-and-shoulder silhouettes under a lightbulb.

Blue arrow "data" feeds the model; gold arrow "insight" feeds the people.

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or the manifest named by the
SOURCES_JSON environment variable):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_ai_needs_data.py

Output: talks/wmko_2026/figures/ai_needs_data.png
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyBboxPatch, Polygon,
                                Rectangle, Wedge)
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, STARS, STARS_GOLD, TEAL, GRAY,
                                       INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"

# Drawing canvas in data units: 1 unit ~ 0.1 in on the slide.
XMAX, YMAX = 92.0, 34.0
SEA_FILL = "#d6e6f5"      # pale water
LAND = "#8aa36b"          # mountain green
GOLD_DARK = "#9c6f00"     # outline for gold shapes, gold text
GOLD_PALE = "#fff3cc"     # lightbulb glow

# Horizontal extents of the stages.
GAP = (1.0, 10.0)         # dashed "?" box: data still to collect
DAT = (14.0, 38.0)        # data icons
AI = (49.5, 62.5)         # neural-net card
PPL = (73.0, 91.0)        # people
Y_HEAD, Y_SUB = 31.4, 28.6   # header and sub-caption baselines
Y_TOP, Y_BOT = 26.0, 3.5     # vertical span of the stage drawings
Y_MID = 0.5 * (Y_TOP + Y_BOT)


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def _mid(span):
    """Created by JXP and Claude. Midpoint of an (x0, x1) span."""
    return 0.5 * (span[0] + span[1])


def draw_headers(ax):
    """Created by JXP and Claude. Stage titles and one-line captions."""
    heads = [(DAT, "Data", "collected by people"),
             (AI, "AI model", "finds the patterns"),
             (PPL, "People learn", "new understanding")]
    for span, head, sub in heads:
        x = _mid(span)
        ax.text(x, Y_HEAD, head, ha="center", va="center", fontsize=21,
                color=INK, path_effects=bold(INK, 1.1))
        ax.text(x, Y_SUB, sub, ha="center", va="center", fontsize=16,
                color=MUTED)


def draw_gap(ax):
    """Created by JXP and Claude. Dashed empty box with a question mark:
    the data nobody has collected yet, with a dashed arrow into Data."""
    x0, x1 = GAP
    w, h = x1 - x0, 14.0
    y0 = Y_MID - h / 2
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor="none", edgecolor=GRAY, lw=2.0,
                                ls=(0, (4, 3)), zorder=3))
    ax.text(_mid(GAP), Y_MID + 0.3, "?", ha="center", va="center",
            fontsize=40, color=GRAY, path_effects=bold(GRAY, 1.2), zorder=4)
    ax.text(_mid(GAP), Y_HEAD, "not yet", ha="center", va="center",
            fontsize=18, color=MUTED)
    ax.text(_mid(GAP), Y_SUB, "collected", ha="center", va="center",
            fontsize=18, color=MUTED)
    ax.text(_mid(GAP), y0 - 2.4, "no data,\nno answer", ha="center",
            va="top", fontsize=16, color=MUTED, linespacing=1.1)
    xa, xb = x1 + 0.6, DAT[0] - 0.6
    ax.plot([xa, xb - 1.2], [Y_MID, Y_MID], color=GRAY, lw=2.0,
            ls=(0, (3, 2.5)), zorder=5)                         # dashed shaft
    ax.annotate("", (xb, Y_MID), (xb - 1.4, Y_MID),
                arrowprops=dict(arrowstyle="-|>,head_length=0.8,head_width=0.4",
                                color=GRAY, lw=2.0, shrinkA=0, shrinkB=0),
                zorder=5)                                        # solid head


def draw_dome(ax, cx, cy, r=2.0):
    """Created by JXP and Claude. Telescope dome: white half-sphere on a
    short cylinder, with a dark open slit."""
    base_h = 1.3
    ax.add_patch(Rectangle((cx - r, cy), 2 * r, base_h, facecolor="white",
                           edgecolor=INK, lw=1.3, zorder=4))
    ax.add_patch(Wedge((cx, cy + base_h), r, 0, 180, facecolor="white",
                       edgecolor=INK, lw=1.3, zorder=4))
    ax.add_patch(Wedge((cx, cy + base_h), r - 0.15, 62, 92,
                       facecolor=STARS, lw=0, zorder=4.5))             # slit


def draw_satellite(ax, sx, sy):
    """Created by JXP and Claude. Satellite with two solar panels and a dish."""
    for px in (sx - 6.0, sx + 1.6):                        # solar panels
        ax.add_patch(Rectangle((px, sy - 0.65), 4.4, 1.3, facecolor=SEA,
                               edgecolor="white", lw=1.0, zorder=3))
        for k in range(1, 4):                              # panel cells
            ax.plot([px + k * 4.4 / 4] * 2, [sy - 0.65, sy + 0.65],
                    color="white", lw=0.8, zorder=3.5)
    ax.add_patch(Rectangle((sx - 1.6, sy - 1.0), 3.2, 2.0, facecolor="#555555",
                           edgecolor=INK, lw=1.0, zorder=4))         # body
    ax.add_patch(Wedge((sx, sy - 1.0), 1.0, 200, 340, facecolor="white",
                       edgecolor=INK, lw=1.0, zorder=4))             # dish


def draw_float(ax, fx, fy0, y_surf, fh=4.4):
    """Created by JXP and Claude. Profiling float: white cylinder with an
    antenna to the surface and an up/down arrow."""
    ax.plot([fx, fx], [fy0 + fh, y_surf + 1.2], color=INK, lw=1.2, zorder=3)
    ax.add_patch(FancyBboxPatch((fx - 0.75, fy0), 1.5, fh,
                                boxstyle="round,pad=0,rounding_size=0.5",
                                facecolor="white", edgecolor=INK, lw=1.4,
                                zorder=3))
    ax.add_patch(Rectangle((fx - 0.75, fy0 + 1.2), 1.5, 1.1, facecolor=TEAL,
                           lw=0, zorder=3.5))
    ax.annotate("", (fx + 1.8, fy0 + fh + 0.3), (fx + 1.8, fy0 - 0.3),
                arrowprops=dict(arrowstyle="<->", color=SEA, lw=1.5,
                                shrinkA=0, shrinkB=0), zorder=3)


def draw_glider(ax, gx, gy, ang=-14):
    """Created by JXP and Claude. Gold torpedo glider with wings and fin."""
    ax.add_patch(Ellipse((gx, gy), 1.2, 3.3, angle=ang, facecolor=STARS_GOLD,
                         edgecolor=GOLD_DARK, lw=1.0, zorder=3))      # wings
    ax.add_patch(Ellipse((gx, gy), 5.4, 1.4, angle=ang, facecolor=STARS_GOLD,
                         edgecolor=GOLD_DARK, lw=1.2, zorder=3.5))    # hull
    th = np.radians(ang)
    tail = (gx - 2.2 * np.cos(th), gy - 2.2 * np.sin(th))
    ax.plot([tail[0], tail[0] - 0.9 * np.sin(th)],
            [tail[1], tail[1] + 0.9 * np.cos(th)], color=GOLD_DARK, lw=2.2,
            zorder=3.6, solid_capstyle="round")                       # fin


def draw_data(ax):
    """Created by JXP and Claude. The data stage: a dome on a mountain, a
    satellite overhead, and a glider and float under a wavy sea."""
    x0, x1 = DAT
    y_surf = 12.0

    # --- sea: wavy surface, pale fill
    xs = np.linspace(x0, x1, 300)
    wave = y_surf + 0.5 * np.sin(2 * np.pi * (xs - x0) / 5.5)
    ax.fill_between(xs, Y_BOT, wave, color=SEA_FILL, lw=0, zorder=1)
    ax.plot(xs, wave, color=SEA, lw=2.2, zorder=2, solid_capstyle="round")

    # --- shield volcano with a dome on the summit (Maunakea)
    mx, mw, mh = x0 + 6.8, 13.6, 7.2             # centre, width, height
    xm = np.linspace(mx - mw / 2, mx + mw / 2, 120)
    ym = y_surf - 0.2 + mh * np.cos(np.pi * (xm - mx) / mw) ** 2
    ax.add_patch(Polygon(np.column_stack([xm, ym]), closed=True,
                         facecolor=LAND, lw=0, zorder=1.5))
    draw_dome(ax, mx, y_surf - 0.2 + mh - 0.3)

    # --- satellite with a beam onto the sea
    sx, sy = x0 + 18.0, 23.0
    ax.add_patch(Polygon([(sx, sy - 1.0), (sx - 3.6, y_surf + 0.3),
                          (sx + 3.6, y_surf + 0.3)], closed=True,
                         facecolor=STARS_GOLD, alpha=0.22, lw=0, zorder=1.4))
    draw_satellite(ax, sx, sy)

    # --- under the sea: float at left, glider on a saw-tooth track at right
    draw_float(ax, x0 + 4.0, Y_BOT + 1.6, y_surf)
    tx = x0 + np.array([8.4, 10.2, 12.0, 13.8, 15.4])
    ty = np.array([9.6, 5.4, 9.6, 5.4, 8.4])
    ax.plot(tx, ty, color=GRAY, lw=1.3, ls=(0, (2, 2)), zorder=2.5)
    draw_glider(ax, x0 + 18.6, 7.6)


def draw_ai(ax):
    """Created by JXP and Claude. Glowing, gold-edged neural-net card."""
    cx, cy = _mid(AI), Y_MID
    bw, bh = AI[1] - AI[0], 16.0
    for k in range(8, 0, -1):                                   # soft glow
        pad = 0.4 * k
        ax.add_patch(FancyBboxPatch((cx - bw / 2 - pad, cy - bh / 2 - pad),
                                    bw + 2 * pad, bh + 2 * pad,
                                    boxstyle="round,pad=0,rounding_size=1.4",
                                    facecolor=STARS_GOLD, alpha=0.035, lw=0,
                                    zorder=2))
    ax.add_patch(FancyBboxPatch((cx - bw / 2, cy - bh / 2), bw, bh,
                                boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor="white", edgecolor=STARS_GOLD,
                                lw=2.6, zorder=5))
    cols = [3, 5, 5, 3]
    xs = cx + np.array([-4.5, -1.5, 1.5, 4.5])
    nodes = []
    for xc, n in zip(xs, cols):
        ys = cy + (np.arange(n) - (n - 1) / 2) * (bh - 4.0) / (max(cols) - 1)
        nodes.append([(xc, yy) for yy in ys])
    for a, b in zip(nodes[:-1], nodes[1:]):
        for (xa, ya) in a:
            for (xb, yb) in b:
                ax.plot([xa, xb], [ya, yb], color=STARS, lw=0.8, alpha=0.45,
                        zorder=5.5)
    for layer in nodes:
        for (xn, yn) in layer:
            ax.add_patch(Circle((xn, yn), 0.6, facecolor=STARS_GOLD,
                                edgecolor=GOLD_DARK, lw=0.8, zorder=6))


def draw_person(ax, cx, y0, s=1.0, color=STARS):
    """Created by JXP and Claude. Head-and-shoulders silhouette."""
    ax.add_patch(Wedge((cx, y0), 4.0 * s, 0, 180, facecolor=color, lw=0,
                       zorder=4))                                   # shoulders
    ax.add_patch(Rectangle((cx - 4.0 * s, y0 - 1.0), 8.0 * s, 1.0,
                           facecolor=color, lw=0, zorder=4))
    ax.add_patch(Circle((cx, y0 + 5.2 * s), 2.3 * s, facecolor=color, lw=0,
                        zorder=4))                                  # head


def draw_bulb(ax, cx, cy, r=2.4):
    """Created by JXP and Claude. Lightbulb with rays: the idea."""
    ax.add_patch(Circle((cx, cy), r * 2.0, facecolor=GOLD_PALE, lw=0,
                        zorder=2.5))                                # glow
    for ang in np.radians([25, 65, 90, 115, 155]):                   # rays
        ax.plot([cx + 1.35 * r * np.cos(ang), cx + 1.95 * r * np.cos(ang)],
                [cy + 1.35 * r * np.sin(ang), cy + 1.95 * r * np.sin(ang)],
                color=GOLD_DARK, lw=2.2, solid_capstyle="round", zorder=3)
    ax.add_patch(Circle((cx, cy), r, facecolor=STARS_GOLD, edgecolor=GOLD_DARK,
                        lw=1.4, zorder=3.5))                        # bulb
    ax.add_patch(Rectangle((cx - 0.75, cy - r - 1.1), 1.5, 1.2,
                           facecolor=GRAY, edgecolor=INK, lw=1.0, zorder=3.6))
    ax.plot([cx - 0.75, cx + 0.75], [cy - r - 0.5] * 2, color=INK, lw=0.8,
            zorder=3.7)                                              # thread


def draw_people(ax):
    """Created by JXP and Claude. Three people under a lightbulb."""
    x0, x1 = PPL
    cx = _mid(PPL)
    draw_bulb(ax, cx, Y_TOP - 4.6)
    draw_person(ax, x0 + 4.4, Y_BOT + 2.2, s=0.95, color="#5a5894")
    draw_person(ax, x1 - 4.4, Y_BOT + 2.2, s=0.95, color="#5a5894")
    draw_person(ax, cx, Y_BOT + 1.4, s=1.1, color=STARS)


def draw_arrows(ax):
    """Created by JXP and Claude. Blue "data" arrow into the model and gold
    "insight" arrow out to the people."""
    y = Y_MID
    head = "-|>,head_length=0.9,head_width=0.45"
    ax.annotate("", (AI[0] - 1.0, y), (DAT[1] + 1.0, y),
                arrowprops=dict(arrowstyle=head, color=SEA, lw=3.0,
                                shrinkA=0, shrinkB=0), zorder=7)
    ax.annotate("", (PPL[0] - 1.0, y), (AI[1] + 1.0, y),
                arrowprops=dict(arrowstyle=head, color=STARS_GOLD, lw=3.0,
                                shrinkA=0, shrinkB=0), zorder=7)
    ax.text(_mid((DAT[1], AI[0])), y + 2.2, "data", ha="center", va="bottom",
            fontsize=18, color=SEA, path_effects=bold(SEA, 0.6), zorder=8)
    ax.text(_mid((AI[1], PPL[0])), y + 2.2, "insight", ha="center",
            va="bottom", fontsize=18, color=GOLD_DARK,
            path_effects=bold(GOLD_DARK, 0.6), zorder=8)


def make_figure():
    """Created by JXP and Claude. Build and save the schematic."""
    style.apply_style()
    fig, ax = plt.subplots(figsize=style.FULL)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, YMAX)
    ax.set_aspect("equal")
    ax.set_axis_off()
    draw_headers(ax)
    draw_gap(ax)
    draw_data(ax)
    draw_ai(ax)
    draw_people(ax)
    draw_arrows(ax)
    return style.save(fig, FIGS, "ai_needs_data.png",
                      source="Schematic: J. X. Prochaska & Claude",
                      slide="AI needs data",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
