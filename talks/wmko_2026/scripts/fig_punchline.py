"""Created by JXP and Claude.

Schematic for the slide "The punchline" (WMKO 2026 public lecture,
Sea meets the stars).

States the talk's main message graphically, with almost no words:
astronomy and oceanography are data-driven explorations of the unknown
(sea and sky); AI is an accelerant on data ANALYSIS but not (yet) on
data COLLECTION.

Three nodes joined by two process arrows:

  [Sea + Sky]  --Collect-->  [Data]  ==Analyze==>  [Discover]

  * Sea + Sky -- a night-sky band with stars, a telescope dome on a
                 mountain and a satellite, above a wavy sea with a glider
                 (all matplotlib patches; no external images).
  * Collect   -- a thin gray arrow with an hourglass: "years", tagged
                 "AI: not yet".
  * Data      -- a stack of blue disks.
  * Analyze   -- a fat gold turbo arrow with speed lines and a neural-net
                 chip: "AI: 100x faster".
  * Discover  -- a light bulb with a gold starburst.

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates the sources manifest, figures/sources.json by default
or the file named by the SOURCES_JSON environment variable):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_punchline.py

Output: talks/wmko_2026/figures/punchline.png
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyArrowPatch,
                                FancyBboxPatch, Polygon, Rectangle, Wedge)
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, SEA_LIGHT, STARS, STARS_GOLD,
                                       GRAY, INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"

# Drawing canvas in data units: 1 unit ~ 0.1 in on the slide.
XMAX, YMAX = 92.0, 39.5
SEA_FILL = "#d6e6f5"      # pale water
SKY_FILL = "#3a377f"      # night sky (a lighter STARS so the dome shows)
MOUNTAIN = "#6b5b4e"      # Mauna Kea brown
GOLD_DARK = "#9c6f00"     # outline for gold shapes
GOLD_LIGHT = "#fff1c2"    # pale gold for the AI chip card
SLOW = "#9aa3a8"          # the plain, slow "collect" arrow

# Horizontal extents of the three nodes and the two arrows.
SCENE = (1.0, 25.0)
DATA = (40.5, 50.0)
DISC = (79.0, 91.0)
COLLECT = (SCENE[1] + 1.5, DATA[0] - 1.5)
ANALYZE = (DATA[1] + 6.5, DISC[0] - 1.5)   # room for the flame at the tail
Y_HEAD = 36.6                # node/arrow titles
Y_TOP, Y_BOT = 32.5, 5.0     # vertical span of the scene
Y_MID = 0.5 * (Y_TOP + Y_BOT)   # the pipeline axis


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def _mid(span):
    """Created by JXP and Claude. Midpoint of an (x0, x1) span."""
    return 0.5 * (span[0] + span[1])


def draw_titles(ax):
    """Created by JXP and Claude. Titles over the nodes (dark) and over the
    two process arrows (gray for Collect, gold for Analyze)."""
    nodes = [(SCENE, "Sea + Sky", INK), (DATA, "Data", INK),
             (DISC, "Discover", INK)]
    for span, head, col in nodes:
        ax.text(_mid(span), Y_HEAD, head, ha="center", va="center",
                fontsize=22, color=col, path_effects=bold(col, 1.1))
    ax.text(_mid(COLLECT), Y_HEAD, "Collect", ha="center", va="center",
            fontsize=22, color=MUTED, path_effects=bold(MUTED, 1.1))
    ax.text(_mid(ANALYZE), Y_HEAD, "Analyze", ha="center", va="center",
            fontsize=22, color=GOLD_DARK, path_effects=bold(GOLD_DARK, 1.1))


def draw_dome(ax, cx, base_y, r=2.6):
    """Created by JXP and Claude. Telescope dome (white hemisphere on a
    cylinder with a dark slit) sitting on base_y."""
    h = 1.6 * r * 0.5
    ax.add_patch(Rectangle((cx - r, base_y), 2 * r, h, facecolor="#f2f2f2",
                           edgecolor=INK, lw=1.0, zorder=4))
    ax.add_patch(Wedge((cx, base_y + h), r, 0, 180, facecolor="white",
                       edgecolor=INK, lw=1.0, zorder=4))
    ax.add_patch(Wedge((cx, base_y + h), r * 0.96, 70, 100,
                       facecolor=INK, lw=0, zorder=4.5))          # slit


def draw_satellite(ax, sx, sy):
    """Created by JXP and Claude. Small satellite with solar panels."""
    for px in (sx - 4.4, sx + 1.4):
        ax.add_patch(Rectangle((px, sy - 0.55), 3.0, 1.1, facecolor=SEA_LIGHT,
                               edgecolor="white", lw=0.8, zorder=4))
        for k in range(1, 3):
            ax.plot([px + k] * 2, [sy - 0.55, sy + 0.55], color="white",
                    lw=0.7, zorder=4.5)
    ax.add_patch(Rectangle((sx - 1.4, sy - 0.9), 2.8, 1.8, facecolor="#bbbbbb",
                           edgecolor="white", lw=0.8, zorder=5))
    ax.add_patch(Wedge((sx, sy - 0.9), 0.9, 200, 340, facecolor="white",
                       edgecolor="#bbbbbb", lw=0.8, zorder=5))


def draw_scene(ax):
    """Created by JXP and Claude. Night sky (stars, satellite, dome on a
    mountain) over a wavy sea with a glider: the unknown we explore."""
    x0, x1 = SCENE
    y_surf = 19.5
    card = FancyBboxPatch((x0, Y_BOT), x1 - x0, Y_TOP - Y_BOT,
                          boxstyle="round,pad=0,rounding_size=1.2",
                          facecolor=SKY_FILL, edgecolor="none", zorder=1)
    ax.add_patch(card)

    # --- stars
    rng = np.random.default_rng(7)
    n = 38
    stx = rng.uniform(x0 + 1, x1 - 1, n)
    sty = rng.uniform(y_surf + 4.0, Y_TOP - 0.8, n)
    sts = rng.uniform(6, 26, n)
    ax.scatter(stx, sty, s=sts, color="white", lw=0, zorder=2, clip_path=card)
    ax.scatter([x1 - 4.6], [Y_TOP - 2.6], s=170, marker="*", color=STARS_GOLD,
               lw=0, zorder=2.5)

    # --- mountain with a dome
    mtn = Polygon([(x0, y_surf), (x0 + 5.0, y_surf), (x0 + 8.0, y_surf + 4.2),
                   (x0 + 12.5, y_surf + 7.2), (x0 + 17.0, y_surf + 3.0),
                   (x0 + 21.0, y_surf)], closed=True, facecolor=MOUNTAIN,
                  lw=0, zorder=3)
    ax.add_patch(mtn)
    draw_dome(ax, x0 + 12.5, y_surf + 7.0, r=2.2)
    draw_satellite(ax, x0 + 5.4, Y_TOP - 3.4)

    # --- sea: pale fill under a wavy surface
    xs = np.linspace(x0, x1, 300)
    wave = y_surf + 0.5 * np.sin(2 * np.pi * (xs - x0) / 5.0)
    ax.fill_between(xs, Y_BOT, wave, color=SEA_FILL, lw=0, zorder=3.2,
                    clip_path=card)
    ax.plot(xs, wave, color=SEA, lw=2.2, zorder=3.5, solid_capstyle="round")
    for yy in (y_surf - 4.0, y_surf - 8.0):                 # faint swells
        ax.plot(xs, yy + 0.35 * np.sin(2 * np.pi * (xs - x0) / 5.0 + 1.0),
                color=SEA_LIGHT, lw=1.0, alpha=0.5, zorder=3.4, clip_path=card)

    # --- glider: gold torpedo with wings on a saw-tooth track
    gx, gy, ang = x0 + 17.5, y_surf - 5.4, -14
    tx = x0 + np.array([3.0, 5.5, 8.0, 10.5, 13.0, 15.2])
    ty = y_surf + np.array([-2.0, -8.2, -2.0, -8.2, -2.0, -5.0])
    ax.plot(tx, ty, color=GRAY, lw=1.3, ls=(0, (2, 2)), zorder=3.6)
    ax.add_patch(Ellipse((gx, gy), 1.3, 3.6, angle=ang, facecolor=STARS_GOLD,
                         edgecolor=GOLD_DARK, lw=1.0, zorder=3.7))     # wings
    ax.add_patch(Ellipse((gx, gy), 5.8, 1.5, angle=ang, facecolor=STARS_GOLD,
                         edgecolor=GOLD_DARK, lw=1.2, zorder=3.8))     # hull
    th = np.radians(ang)
    tail = (gx - 2.4 * np.cos(th), gy - 2.4 * np.sin(th))
    ax.plot([tail[0], tail[0] - 0.9 * np.sin(th)],
            [tail[1], tail[1] + 0.9 * np.cos(th)], color=GOLD_DARK, lw=2.2,
            zorder=3.9, solid_capstyle="round")                        # fin


def draw_hourglass(ax, cx, cy, h=4.2, w=3.0, color=MUTED):
    """Created by JXP and Claude. Hourglass glyph: two triangles, sand in
    the bottom, caps top and bottom."""
    top = Polygon([(cx - w / 2, cy + h / 2), (cx + w / 2, cy + h / 2),
                   (cx, cy + 0.15)], closed=True, facecolor="white",
                  edgecolor=color, lw=1.8, zorder=7)
    bot = Polygon([(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2),
                   (cx, cy - 0.15)], closed=True, facecolor="white",
                  edgecolor=color, lw=1.8, zorder=7)
    ax.add_patch(top)
    ax.add_patch(bot)
    sand = Polygon([(cx - w * 0.3, cy - h / 2 + 0.25),
                    (cx + w * 0.3, cy - h / 2 + 0.25), (cx, cy - h * 0.22)],
                   closed=True, facecolor=color, lw=0, zorder=7.5)
    ax.add_patch(sand)
    ax.add_patch(Polygon([(cx - w * 0.14, cy + h / 2 - 0.3),
                          (cx + w * 0.14, cy + h / 2 - 0.3), (cx, cy + 0.6)],
                         closed=True, facecolor=color, lw=0, zorder=7.5))
    for yy in (cy + h / 2, cy - h / 2):
        ax.plot([cx - w / 2 - 0.3, cx + w / 2 + 0.3], [yy, yy], color=color,
                lw=3.0, zorder=7.6, solid_capstyle="round")


def draw_collect(ax):
    """Created by JXP and Claude. The slow collect arrow: thin, gray, with
    an hourglass in the middle, 'years' and an 'AI: not yet' tag."""
    x0, x1 = COLLECT
    y = Y_MID
    ax.plot([x0, x1 - 1.8], [y, y], color=SLOW, lw=2.6, ls=(0, (2.2, 1.6)),
            zorder=6, solid_capstyle="butt")
    ax.add_patch(Polygon([(x1 - 2.2, y - 1.1), (x1, y), (x1 - 2.2, y + 1.1)],
                         closed=True, facecolor=SLOW, lw=0, zorder=6))
    draw_hourglass(ax, _mid((x0, x1)), y + 0.1, h=5.0, w=3.4, color=MUTED)
    # cover the arrow shaft behind the hourglass with a white halo
    ax.add_patch(Circle((_mid((x0, x1)), y), 1.7, facecolor="white", lw=0,
                        zorder=6.5))
    ax.text(_mid((x0, x1)), y - 4.2, "years", ha="center", va="top",
            fontsize=19, color=MUTED)
    ax.text(_mid((x0, x1)), y + 4.2, "AI: not yet", ha="center", va="bottom",
            fontsize=18, color=MUTED, zorder=8,
            bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                      edgecolor=SLOW, lw=1.4, ls=(0, (3, 2))))


def draw_data(ax):
    """Created by JXP and Claude. Stack of blue disks (a database)."""
    cx, w, hh, ry = _mid(DATA), DATA[1] - DATA[0] - 2.0, 2.6, 0.9
    y0 = Y_MID - 1.5 * hh - 1.0
    for k in range(3):
        yb = y0 + k * hh
        ax.add_patch(Rectangle((cx - w / 2, yb), w, hh, facecolor=SEA_LIGHT,
                               edgecolor=SEA, lw=1.6, zorder=5))
        ax.add_patch(Ellipse((cx, yb), w, 2 * ry, facecolor=SEA_LIGHT,
                             edgecolor=SEA, lw=1.6, zorder=5.2))
    ax.add_patch(Ellipse((cx, y0 + 3 * hh), w, 2 * ry, facecolor=SEA,
                         edgecolor=SEA, lw=1.6, zorder=5.4))
    for k in range(3):                                      # side ticks
        yb = y0 + k * hh + hh * 0.5
        ax.plot([cx - w / 2 + 1.0, cx - w / 2 + 2.2], [yb, yb], color=SEA,
                lw=1.4, zorder=5.3)


def draw_chip(ax, cx, cy, w=7.4, h=5.6):
    """Created by JXP and Claude. Neural-net glyph on a pale-gold chip."""
    ax.add_patch(FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                facecolor="white", edgecolor=GOLD_DARK,
                                lw=2.0, zorder=8))
    cols = [3, 4, 3]
    xs = cx + np.array([-2.3, 0.0, 2.3])
    nodes = []
    for xc, n in zip(xs, cols):
        ys = cy + (np.arange(n) - (n - 1) / 2) * (h - 2.0) / (cols[1] - 1)
        nodes.append([(xc, yy) for yy in ys])
    for a, b in zip(nodes[:-1], nodes[1:]):
        for (xa, ya) in a:
            for (xb, yb) in b:
                ax.plot([xa, xb], [ya, yb], color=STARS, lw=0.8, alpha=0.5,
                        zorder=8.5)
    for layer in nodes:
        for (xn, yn) in layer:
            ax.add_patch(Circle((xn, yn), 0.46, facecolor=STARS_GOLD,
                                edgecolor=GOLD_DARK, lw=0.8, zorder=9))


def draw_analyze(ax):
    """Created by JXP and Claude. The turbo analyze arrow: fat, gold, with
    speed lines, a flame at the tail, an AI chip and '100x faster'."""
    x0, x1 = ANALYZE
    y = Y_MID
    body_h = 4.4
    head_w = 6.4
    arrow = Polygon([(x0, y - body_h / 2), (x1 - head_w, y - body_h / 2),
                     (x1 - head_w, y - body_h * 0.95), (x1, y),
                     (x1 - head_w, y + body_h * 0.95),
                     (x1 - head_w, y + body_h / 2), (x0, y + body_h / 2)],
                    closed=True, facecolor=STARS_GOLD, edgecolor=GOLD_DARK,
                    lw=1.6, zorder=6)
    ax.add_patch(arrow)
    # flame at the tail
    for s, col in ((1.0, "#f2703f"), (0.6, "#ffd166")):
        ax.add_patch(Polygon([(x0 + 0.2, y + 1.7 * s), (x0 - 3.4 * s, y),
                              (x0 + 0.2, y - 1.7 * s)], closed=True,
                             facecolor=col, lw=0, zorder=5.8))
    # speed lines streaking off the tail, above and below the flame
    for dy, xa, xb in ((3.6, x0 - 5.2, x0 - 1.0), (-3.6, x0 - 5.2, x0 - 1.0),
                       (0.0, x0 - 6.2, x0 - 4.2)):
        ax.plot([xa, xb], [y + dy, y + dy], color=STARS_GOLD, lw=2.6,
                alpha=0.8, zorder=5.5, solid_capstyle="round")
    draw_chip(ax, _mid((x0, x1 - head_w)) + 0.6, y + 0.1, w=8.0, h=6.2)
    ax.text(_mid((x0, x1)), y - 4.6, "AI: 100× faster", ha="center", va="top",
            fontsize=20, color=GOLD_DARK, path_effects=bold(GOLD_DARK, 0.8))


def draw_discover(ax):
    """Created by JXP and Claude. Light bulb with a gold starburst."""
    cx, cy = _mid(DISC), Y_MID + 1.6
    r = 4.4
    # rays over the upper half of the bulb
    for deg in (0, 30, 60, 90, 120, 150, 180):
        th = np.radians(deg)
        r0, r1 = r + 1.2, r + 3.4
        ax.plot([cx + r0 * np.cos(th), cx + r1 * np.cos(th)],
                [cy + r0 * np.sin(th), cy + r1 * np.sin(th)], color=STARS_GOLD,
                lw=3.0, zorder=5, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), r, facecolor="#fff6d6", edgecolor=GOLD_DARK,
                        lw=2.0, zorder=6))
    # neck and base
    ax.add_patch(Polygon([(cx - 2.0, cy - r * 0.86), (cx + 2.0, cy - r * 0.86),
                          (cx + 1.6, cy - r - 1.4), (cx - 1.6, cy - r - 1.4)],
                         closed=True, facecolor="#fff6d6", edgecolor=GOLD_DARK,
                         lw=2.0, zorder=6.5))
    for k in range(3):
        yb = cy - r - 1.6 - k * 0.9
        ax.add_patch(Rectangle((cx - 1.5 + 0.15 * k, yb), 3.0 - 0.3 * k, 0.65,
                               facecolor="#8c8c8c", edgecolor=INK, lw=0.6,
                               zorder=6.5))
    # filament: a little star inside the bulb
    ax.scatter([cx], [cy + 0.2], s=420, marker="*", color=STARS_GOLD,
               edgecolor=GOLD_DARK, lw=0.8, zorder=7)


def make_figure():
    """Created by JXP and Claude. Build and save the schematic."""
    style.apply_style()
    fig, ax = plt.subplots(figsize=style.FULL_TALL)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(1.5, YMAX)
    ax.set_aspect("equal")
    ax.set_axis_off()
    draw_titles(ax)
    draw_scene(ax)
    draw_collect(ax)
    draw_data(ax)
    draw_analyze(ax)
    draw_discover(ax)
    return style.save(fig, FIGS, "punchline.png",
                      source="Schematic: J. X. Prochaska & Claude",
                      slide="The punchline",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
