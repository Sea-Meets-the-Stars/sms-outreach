"""Created by JXP and Claude.

Schematic for the slide "Coupling observations to models with AI"
(WMKO 2026 public lecture, Sea meets the stars).

Draws a three-stage cartoon that a lay audience can read in a few seconds:

  1. Observe   -- a satellite above a wavy sea, with a glider and a
                  profiling float below the surface (all drawn with
                  matplotlib patches; no external images).
  2. Model + AI -- a gridded globe ("virtual ocean") with a neural-net
                  glyph; "data in" arrow from the observations.
  3. Forecast  -- a weather-map panel of the Hawaiian Islands with a warm
                  marine-heat-wave blob and a hurricane symbol
                  ("tomorrow's ocean").

A gold feedback arrow runs from Forecast back to Observe, labelled
"where to look next" (the AI steering the gliders).

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_obs_model_ai.py

Output: talks/wmko_2026/figures/obs_model_ai.png
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyArrowPatch,
                                FancyBboxPatch, Polygon, Rectangle, Wedge)
from matplotlib.path import Path as MplPath
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, SEA_LIGHT, STARS, STARS_GOLD,
                                       RED, TEAL, GRAY, INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"

# Drawing canvas in data units: 1 unit ~ 0.1 in on the slide.
XMAX, YMAX = 92.0, 39.5
SEA_FILL = "#d6e6f5"      # pale water for the sea and the map
LAND = "#8aa36b"          # island green
GOLD_DARK = "#9c6f00"     # outline for gold shapes
HEAT = ["#fde3a7", "#fbb36d", "#f2703f", RED]  # warm blob, outside -> in

# Horizontal extents of the three stages and their centres.
OBS = (1.0, 25.0)
MOD = (30.0, 60.0)
FOR = (68.0, 91.0)
GLOBE_R = 9.6
Y_HEAD, Y_SUB = 37.2, 34.3   # header and sub-caption baselines
Y_TOP, Y_BOT = 32.0, 10.0    # vertical span of the stage drawings
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
    heads = [(OBS, "1. Observe", "satellites · gliders · floats"),
             (MOD, "2. Model + AI", "a virtual ocean"),
             (FOR, "3. Forecast", "tomorrow's ocean")]
    for span, head, sub in heads:
        x = _mid(span)
        ax.text(x, Y_HEAD, head, ha="center", va="center", fontsize=21,
                color=INK, path_effects=bold(INK, 1.1))
        ax.text(x, Y_SUB, sub, ha="center", va="center", fontsize=16,
                color=MUTED)


def draw_observe(ax):
    """Created by JXP and Claude. Satellite over a wavy sea with a glider
    and a profiling float below the surface."""
    x0, x1 = OBS
    y_surf = 21.0

    # --- sea: wavy surface, pale fill, darker surface line
    xs = np.linspace(x0, x1, 300)
    wave = y_surf + 0.55 * np.sin(2 * np.pi * (xs - x0) / 5.5)
    ax.fill_between(xs, Y_BOT, wave, color=SEA_FILL, lw=0, zorder=1)
    ax.plot(xs, wave, color=SEA, lw=2.2, zorder=2, solid_capstyle="round")

    # --- satellite
    sx, sy = 9.0, 28.6
    beam = Polygon([(sx, sy - 1.0), (sx - 4.2, y_surf + 0.3),
                    (sx + 4.2, y_surf + 0.3)], closed=True,
                   facecolor=STARS_GOLD, alpha=0.22, lw=0, zorder=1.5)
    ax.add_patch(beam)
    for px in (sx - 6.4, sx + 1.8):                        # solar panels
        ax.add_patch(Rectangle((px, sy - 0.7), 4.6, 1.4, facecolor=SEA,
                               edgecolor="white", lw=1.0, zorder=3))
        for k in range(1, 4):                              # panel cells
            ax.plot([px + k * 4.6 / 4] * 2, [sy - 0.7, sy + 0.7],
                    color="white", lw=0.8, zorder=3.5)
    ax.add_patch(Rectangle((sx - 1.8, sy - 1.1), 3.6, 2.2, facecolor="#555555",
                           edgecolor=INK, lw=1.0, zorder=4))         # body
    ax.add_patch(Wedge((sx, sy - 1.1), 1.1, 200, 340, facecolor="white",
                       edgecolor=INK, lw=1.0, zorder=4))             # dish

    # --- profiling float (white cylinder with antenna, up/down arrows)
    fx, fy0, fh = 5.6, 12.4, 5.2
    ax.plot([fx, fx], [fy0 + fh, y_surf + 1.4], color=INK, lw=1.2, zorder=3)
    ax.add_patch(FancyBboxPatch((fx - 0.8, fy0), 1.6, fh,
                                boxstyle="round,pad=0,rounding_size=0.5",
                                facecolor="white", edgecolor=INK, lw=1.4,
                                zorder=3))
    ax.add_patch(Rectangle((fx - 0.8, fy0 + 1.4), 1.6, 1.2, facecolor=TEAL,
                           lw=0, zorder=3.5))
    ax.annotate("", (fx + 1.9, fy0 + fh + 0.3), (fx + 1.9, fy0 - 0.3),
                arrowprops=dict(arrowstyle="<->", color=SEA, lw=1.6,
                                shrinkA=0, shrinkB=0), zorder=3)

    # --- glider: gold torpedo with wings, on a saw-tooth track
    gx, gy, ang = 19.3, 16.3, -14
    tx = np.array([9.6, 11.6, 13.6, 15.6, 17.2])
    ty = np.array([18.6, 12.6, 18.6, 12.6, 17.0])
    ax.plot(tx, ty, color=GRAY, lw=1.3, ls=(0, (2, 2)), zorder=2.5)
    ax.add_patch(Ellipse((gx, gy), 1.3, 3.6, angle=ang, facecolor=STARS_GOLD,
                         edgecolor=GOLD_DARK, lw=1.0, zorder=3))      # wings
    ax.add_patch(Ellipse((gx, gy), 5.8, 1.5, angle=ang, facecolor=STARS_GOLD,
                         edgecolor=GOLD_DARK, lw=1.2, zorder=3.5))    # hull
    th = np.radians(ang)
    tail = (gx - 2.4 * np.cos(th), gy - 2.4 * np.sin(th))
    ax.plot([tail[0], tail[0] - 0.9 * np.sin(th)],
            [tail[1], tail[1] + 0.9 * np.cos(th)], color=GOLD_DARK, lw=2.2,
            zorder=3.6, solid_capstyle="round")                       # fin


def draw_model(ax):
    """Created by JXP and Claude. Gridded globe (the virtual ocean) with a
    neural-net glyph tucked against its lower-right edge."""
    cx, cy, r = _mid(MOD), Y_MID, GLOBE_R
    ax.add_patch(Circle((cx, cy), r, facecolor=SEA_FILL, edgecolor=SEA,
                        lw=2.4, zorder=2))
    grid = dict(facecolor="none", edgecolor=SEA, lw=1.1, alpha=0.6, zorder=3)
    for k in (0.36, 0.72):                                   # meridians
        ax.add_patch(Ellipse((cx, cy), 2 * r * k, 2 * r, **grid))
    ax.plot([cx, cx], [cy - r, cy + r], color=SEA, lw=1.1, alpha=0.6, zorder=3)
    for f in (-0.55, 0.0, 0.55):                              # parallels
        half = r * np.sqrt(1 - f * f)
        ax.plot([cx - half, cx + half], [cy + f * r] * 2, color=SEA, lw=1.1,
                alpha=0.6, zorder=3)
    # a few land blobs so it reads as a planet
    for (dx, dy, w, h, a) in [(-3.6, 4.2, 4.8, 3.6, 20), (-1.8, -3.8, 3.0, 4.6, -25),
                              (4.2, 2.6, 3.4, 5.2, 10)]:
        ax.add_patch(Ellipse((cx + dx, cy + dy), w, h, angle=a, facecolor=LAND,
                             lw=0, alpha=0.85, zorder=2.5))

    # --- neural-net glyph on a white card
    bx, by, bw, bh = cx + 5.4, cy - 6.4, 9.6, 7.2
    ax.add_patch(FancyBboxPatch((bx - bw / 2, by - bh / 2), bw, bh,
                                boxstyle="round,pad=0,rounding_size=0.9",
                                facecolor="white", edgecolor=STARS_GOLD,
                                lw=2.2, zorder=5))
    cols = [3, 4, 3]
    xs = bx + np.array([-2.9, 0.0, 2.9])
    nodes = []
    for xc, n in zip(xs, cols):
        ys = by + (np.arange(n) - (n - 1) / 2) * (bh - 2.4) / max(cols[1] - 1, 1)
        nodes.append([(xc, yy) for yy in ys])
    for a, b in zip(nodes[:-1], nodes[1:]):
        for (xa, ya) in a:
            for (xb, yb) in b:
                ax.plot([xa, xb], [ya, yb], color=STARS, lw=0.8, alpha=0.5,
                        zorder=5.5)
    for layer in nodes:
        for (xn, yn) in layer:
            ax.add_patch(Circle((xn, yn), 0.55, facecolor=STARS_GOLD,
                                edgecolor=GOLD_DARK, lw=0.8, zorder=6))


def draw_hurricane(ax, cx, cy, size=2.6, color=INK):
    """Created by JXP and Claude. Two-armed spiral hurricane symbol."""
    th = np.linspace(0, 1.45 * np.pi, 80)
    rr = size * (0.28 + 0.72 * th / th[-1])
    for off in (0.0, np.pi):
        ax.plot(cx + rr * np.cos(th + off), cy + rr * np.sin(th + off),
                color=color, lw=2.6, zorder=6, solid_capstyle="round")
    ax.add_patch(Circle((cx, cy), 0.32 * size, facecolor="white",
                        edgecolor=color, lw=2.2, zorder=6.5))


def draw_forecast(ax):
    """Created by JXP and Claude. Weather-map panel: Hawaiian Islands, a
    warm marine-heat-wave blob and a hurricane symbol."""
    x0, x1 = FOR
    box = FancyBboxPatch((x0, Y_BOT), x1 - x0, Y_TOP - Y_BOT,
                         boxstyle="round,pad=0,rounding_size=1.0",
                         facecolor=SEA_FILL, edgecolor=GRAY, lw=1.6, zorder=2)
    ax.add_patch(box)
    for gx in np.arange(x0 + 6, x1, 6):                       # faint graticule
        ax.plot([gx, gx], [Y_BOT, Y_TOP], color="white", lw=1.0, zorder=2.5,
                clip_path=box)
    for gy in np.arange(Y_BOT + 5.5, Y_TOP, 5.5):
        ax.plot([x0, x1], [gy, gy], color="white", lw=1.0, zorder=2.5,
                clip_path=box)

    # heat-wave blob (nested warm ellipses)
    hx, hy = 85.0, 27.4
    for k, col in enumerate(HEAT):
        s = 1 - 0.26 * k
        ax.add_patch(Ellipse((hx, hy), 9.8 * s, 6.8 * s, angle=-12,
                             facecolor=col, lw=0, alpha=0.9, zorder=3 + 0.1 * k))

    # island chain (NW -> SE), Big Island largest
    for (ix, iy, w, h, a) in [(70.5, 28.4, 1.6, 1.3, 15), (72.8, 27.3, 2.0, 1.5, 25),
                              (75.2, 26.2, 2.2, 1.5, 20), (77.1, 24.8, 1.4, 1.0, 30)]:
        ax.add_patch(Ellipse((ix, iy), w, h, angle=a, facecolor=LAND, lw=0,
                             zorder=4))
    big = Polygon([(77.8, 23.8), (79.8, 24.4), (81.1, 22.8), (80.6, 20.9),
                   (79.1, 20.0), (77.5, 20.9), (77.1, 22.5)], closed=True,
                  facecolor=LAND, lw=0, zorder=4)
    ax.add_patch(big)

    draw_hurricane(ax, 73.0, 15.8, size=3.0, color=STARS)


def draw_arrows(ax):
    """Created by JXP and Claude. Forward arrows between the stages and the
    gold feedback loop from Forecast back to Observe."""
    y = Y_MID + 1.0
    half = np.sqrt(GLOBE_R ** 2 - (y - Y_MID) ** 2)   # globe half-width at y
    gl, gr = _mid(MOD) - half, _mid(MOD) + half
    fwd = dict(arrowstyle="-|>,head_length=0.9,head_width=0.45", color=INK,
               lw=2.6, shrinkA=0, shrinkB=0)
    ax.annotate("", (gl - 0.7, y), (OBS[1] + 0.8, y),
                arrowprops=fwd, zorder=7)
    ax.annotate("", (FOR[0] - 0.8, y), (gr + 0.7, y),
                arrowprops=fwd, zorder=7)
    ax.text(_mid((OBS[1], gl)), y + 2.6, "data in", ha="center",
            va="bottom", fontsize=16, color=INK)
    ax.text(_mid((gr, FOR[0])), y + 2.6, "predict", ha="center",
            va="bottom", fontsize=16, color=INK)

    # feedback loop: down from the map, along the bottom, up into the sea
    xa, xb, yb, yl = _mid(FOR) + 1.0, _mid(OBS) + 0.5, Y_BOT + 0.2, 4.3
    verts = [(xa, yb), (xa, yl + 2.2), (xa, yl), (xa - 2.2, yl),
             (xb + 2.2, yl), (xb, yl), (xb, yl + 2.2), (xb, yb)]
    codes = [MplPath.MOVETO, MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3,
             MplPath.LINETO, MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO]
    loop = FancyArrowPatch(path=MplPath(verts, codes),
                           arrowstyle="-|>,head_length=0.55,head_width=0.3",
                           color=STARS_GOLD, lw=2.8, mutation_scale=22,
                           shrinkA=0, shrinkB=0, zorder=7)
    ax.add_patch(loop)
    ax.text(0.5 * (xa + xb), yl, "where to look next", ha="center",
            va="center", fontsize=16, color=GOLD_DARK,
            path_effects=bold(GOLD_DARK, 0.7),
            zorder=8, bbox=dict(boxstyle="round,pad=0.35", facecolor="white",
                                edgecolor="none"))


def make_figure():
    """Created by JXP and Claude. Build and save the schematic."""
    style.apply_style()
    fig, ax = plt.subplots(figsize=style.FULL_TALL)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(1.5, YMAX)
    ax.set_aspect("equal")
    ax.set_axis_off()
    draw_headers(ax)
    draw_observe(ax)
    draw_model(ax)
    draw_forecast(ax)
    draw_arrows(ax)
    return style.save(fig, FIGS, "obs_model_ai.png",
                      source="Schematic: J. X. Prochaska & Claude",
                      slide="Coupling observations to models with AI")


if __name__ == "__main__":
    make_figure()
