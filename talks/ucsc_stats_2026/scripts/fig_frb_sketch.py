"""Created by JXP and Claude.

Sketch of the FRB population-inference problem for the UCSC Statistics
department README (talk "Advancing science on the frontier with modern
statistical techniques", 2026).  It is meant to be read at about half a
page wide, so the text is large and sparse.

Generative-model cartoon, left to right (all matplotlib patches, no
external images):

  1. An FRB goes off in a host galaxy at redshift z.
  2. The pulse crosses the host, the cosmic web and the Milky Way; each
     adds electrons along the path (DM), so DM_obs is a sum of three terms,
     of which only the cosmic-web term depends on z.
  3. Several telescopes, each with its own beam and detection threshold,
     catch some of the bursts.
  4. The catalogue: every burst has a DM, only a few also have z.

Below the cartoon, an inset of the DM-z ("Macquart") relation: the mean
curve, scatter that grows with z, localised bursts as (DM, z) points and
unlocalised bursts as ticks on the DM axis only.

Run from the repo root (writes the PNG and updates figures/sources.json):

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_frb_sketch.py

Output: talks/ucsc_stats_2026/figures/frb_sketch.png  (8 x 4.5 in, 200 dpi)
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyArrowPatch,
                                FancyBboxPatch, Polygon, Wedge)
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, SEA_LIGHT, STARS, STARS_GOLD,
                                       GRAY, INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"
FIGSIZE = (8.0, 4.5)      # landscape, half-page width in the Google Doc
DPI = 200

# Drawing canvas in data units (1 unit = 0.1 in).
XMAX, YMAX = 80.0, 45.0
SEA_FILL = "#d6e6f5"      # pale water blue for the cosmic-web band
GOLD_DARK = "#9c6f00"     # outline for gold shapes
HOST = "#8e86c9"          # pale indigo for the host-galaxy segment
BAND = "#bcd3ee"          # scatter band in the inset
Y_PATH = 33.0             # the signal path (cartoon mid-line)

# Font sizes.  The PNG is shown at ~0.42 scale, so 15 pt here reads as
# ~6 pt in the document: nothing smaller than 13.
F_HEAD, F_LAB, F_SMALL = 16, 14, 13


def bold(color, lw=0.9):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def spiral_galaxy(ax, cx, cy, r, color, angle=0.0, zorder=3):
    """Created by JXP and Claude. Tilted disc with a brighter bulge."""
    ax.add_patch(Ellipse((cx, cy), 2 * r, 0.42 * r, angle=angle,
                         facecolor=color, edgecolor="none", alpha=0.55,
                         zorder=zorder))
    ax.add_patch(Ellipse((cx, cy), 0.9 * r, 0.6 * r, angle=angle,
                         facecolor=color, edgecolor="none", alpha=0.9,
                         zorder=zorder + 0.1))


def burst(ax, cx, cy, size, zorder=5):
    """Created by JXP and Claude. Gold star-burst marking the FRB."""
    for k in range(8):
        th = np.pi * k / 4
        ln = size * (1.0 if k % 2 == 0 else 0.6)
        ax.plot([cx - ln * np.cos(th), cx + ln * np.cos(th)],
                [cy - ln * np.sin(th), cy + ln * np.sin(th)],
                color=STARS_GOLD, lw=2.2, solid_capstyle="round",
                zorder=zorder)
    ax.add_patch(Circle((cx, cy), 0.32 * size, facecolor="white",
                        edgecolor=GOLD_DARK, lw=1.2, zorder=zorder + 0.1))


def dish(ax, cx, cy, size, zorder=4):
    """Created by JXP and Claude. Small radio-dish icon (bowl + mast)."""
    ax.add_patch(Wedge((cx, cy), size, 20, 160, facecolor="white",
                       edgecolor=INK, lw=1.2, zorder=zorder))
    ax.plot([cx, cx], [cy, cy - 0.9 * size], color=INK, lw=1.4,
            zorder=zorder)
    ax.plot([cx - 0.45 * size, cx + 0.45 * size], [cy - 0.9 * size] * 2,
            color=INK, lw=1.4, solid_capstyle="round", zorder=zorder)


# ----------------------------------------------------------------------
def draw_source(ax):
    """Created by JXP and Claude. Host galaxy with the FRB at redshift z."""
    cx, cy = 7.0, Y_PATH
    spiral_galaxy(ax, cx, cy, 5.0, STARS, angle=-18)
    burst(ax, cx + 1.4, cy + 0.9, 2.3)
    ax.text(cx, cy - 4.4, "FRB at\nredshift z", ha="center", va="top",
            fontsize=F_LAB, color=INK, linespacing=1.15,
            path_effects=bold(INK, 0.6))


def draw_path(ax):
    """Created by JXP and Claude. The pulse crosses host, cosmic web and
    Milky Way; each segment adds its DM."""
    x_host, x_web0, x_web1, x_mw1 = 12.6, 18.0, 38.0, 45.0
    y = Y_PATH

    # cosmic-web band: pale blue with a few filaments
    ax.add_patch(FancyBboxPatch((x_web0, y - 5.0), x_web1 - x_web0, 10.0,
                                boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor=SEA_FILL, edgecolor="none",
                                zorder=1))
    rng = np.random.default_rng(7)
    nodes = np.column_stack([rng.uniform(x_web0 + 1, x_web1 - 1, 14),
                             rng.uniform(y - 4.2, y + 4.2, 14)])
    for i in range(len(nodes)):
        d = np.hypot(*(nodes - nodes[i]).T)
        for j in np.argsort(d)[1:3]:
            ax.plot([nodes[i, 0], nodes[j, 0]], [nodes[i, 1], nodes[j, 1]],
                    color=SEA_LIGHT, lw=1.0, alpha=0.7, zorder=1.5)
    ax.scatter(nodes[:, 0], nodes[:, 1], s=14, color=SEA, alpha=0.6,
               lw=0, zorder=1.6)

    # Milky Way disc at the end of the path
    spiral_galaxy(ax, x_mw1 - 2.6, y, 3.4, GRAY, angle=75, zorder=2)

    # the pulse: three coloured segments then an arrow into the telescopes
    segs = [((x_host, x_web0), HOST), ((x_web0, x_web1), SEA),
            ((x_web1, x_mw1), GRAY)]
    for (x0, x1), col in segs:
        ax.plot([x0, x1], [y, y], color=col, lw=3.2, solid_capstyle="butt",
                zorder=3)
    ax.annotate("", (50.2, y), (x_mw1, y),
                arrowprops=dict(arrowstyle="-|>,head_length=0.8,head_width=0.4",
                                color=INK, lw=2.2, shrinkA=0, shrinkB=0),
                zorder=3)

    # DM terms above, plain names below
    terms = [(0.5 * (x_host + x_web0), "DM$_{\\rm host}$", "host"),
             (0.5 * (x_web0 + x_web1), "+ DM$_{\\rm cosmic}$(z)", "cosmic web"),
             (0.5 * (x_web1 + x_mw1), "+ DM$_{\\rm MW}$", "Milky Way")]
    for x, top, bot in terms:
        ax.text(x, y + 5.7, top, ha="center", va="bottom", fontsize=F_LAB,
                color=INK)
        ax.text(x, y - 5.7, bot, ha="center", va="top", fontsize=F_SMALL,
                color=MUTED)
    ax.text(0.5 * (x_host + x_mw1), y + 9.3,
            "DM = electrons along the path", ha="center", va="bottom",
            fontsize=F_HEAD, color=INK, path_effects=bold(INK))


def draw_telescopes(ax):
    """Created by JXP and Claude. Column of dishes, one per survey."""
    x0, w = 50.0, 12.0
    y0, h = Y_PATH - 7.6, 15.2
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle="round,pad=0,rounding_size=1.0",
                                facecolor="white", edgecolor=GRAY, lw=1.4,
                                zorder=2))
    names = ["CHIME", "ASKAP", "DSA", "Parkes", "MeerKAT", "FAST"]
    ys = y0 + h - 1.8 - np.arange(len(names)) * 2.3
    for name, yy in zip(names, ys):
        dish(ax, x0 + 1.7, yy - 0.3, 0.85)
        ax.text(x0 + 3.3, yy - 0.4, name, ha="left", va="center",
                fontsize=F_SMALL, color=INK)
    ax.text(x0 + w / 2, y0 + h + 1.2, "6 telescopes", ha="center",
            va="bottom", fontsize=F_HEAD, color=INK, path_effects=bold(INK))
    ax.text(x0 + w / 2, y0 - 0.9, "own beam\n+ threshold", ha="center",
            va="top", fontsize=F_SMALL, color=MUTED, linespacing=1.1)


def draw_catalog(ax):
    """Created by JXP and Claude. The observed catalogue: all DM, few z."""
    x0, w = 66.0, 13.0
    y0, h = Y_PATH - 7.6, 15.2
    ax.annotate("", (x0 - 0.3, Y_PATH), (x0 - 3.7, Y_PATH),
                arrowprops=dict(arrowstyle="-|>,head_length=0.8,head_width=0.4",
                                color=INK, lw=2.2, shrinkA=0, shrinkB=0),
                zorder=3)
    ax.add_patch(FancyBboxPatch((x0, y0), w, h,
                                boxstyle="round,pad=0,rounding_size=1.0",
                                facecolor="white", edgecolor=GRAY, lw=1.4,
                                zorder=2))
    ax.text(x0 + w / 2, y0 + h + 1.2, "catalogue", ha="center",
            va="bottom", fontsize=F_HEAD, color=INK, path_effects=bold(INK))
    # mini table: DM for every row, z for a few
    xc_dm, xc_z = x0 + 3.6, x0 + 9.6
    yh = y0 + h - 1.9
    ax.text(xc_dm, yh, "DM", ha="center", va="center", fontsize=F_SMALL,
            color=INK, path_effects=bold(INK, 0.6))
    ax.text(xc_z, yh, "z", ha="center", va="center", fontsize=F_SMALL,
            color=INK, path_effects=bold(INK, 0.6))
    ax.plot([x0 + 1.2, x0 + w - 1.2], [yh - 1.4] * 2, color=GRAY, lw=0.9,
            zorder=3)
    rows = [("612", "0.34"), ("1071", "–"), ("483", "–"), ("952", "–"),
            ("…", "…")]
    for k, (dm, z) in enumerate(rows):
        yy = yh - 2.7 - 2.3 * k
        ax.text(xc_dm, yy, dm, ha="center", va="center", fontsize=F_SMALL,
                color=INK)
        ax.text(xc_z, yy, z, ha="center", va="center", fontsize=F_SMALL,
                color=SEA if z not in ("–", "…") else MUTED)
    ax.text(x0 + w / 2, y0 - 0.9, "~600 bursts\n~30 with z", ha="center",
            va="top", fontsize=F_SMALL, color=MUTED, linespacing=1.1)


def draw_inset(ax):
    """Created by JXP and Claude. DM-z relation: mean curve, scatter that
    grows with z, localised points and DM-only ticks on the DM axis."""
    ins = ax.inset_axes([37.0, 5.6, 41.0, 12.6], transform=ax.transData)
    ins.set_in_layout(False)   # else tight_layout shrinks the main axes
    rng = np.random.default_rng(3)
    z = np.linspace(0, 1.2, 200)
    mean = 100.0 + 950.0 * z                     # host + cosmic-web mean
    sig = 60.0 + 260.0 * np.sqrt(z)              # scatter grows with z
    ins.fill_between(z, mean - 2 * sig, mean + 2 * sig, color=BAND,
                     alpha=0.5, lw=0)
    ins.fill_between(z, mean - sig, mean + sig, color=BAND, lw=0)
    ins.plot(z, mean, color=SEA, lw=2.0)

    # localised bursts: (DM, z) points drawn from the model
    zl = rng.uniform(0.05, 0.55, 12)
    dml = 100.0 + 950.0 * zl + rng.normal(0, 1, 12) * (60 + 260 * np.sqrt(zl))
    ins.scatter(zl, dml, s=42, color=SEA, edgecolor="white", lw=1.0,
                zorder=4, label="localised: (DM, z)")
    # unlocalised bursts: DM known, z unknown -> ticks on the DM axis
    dmu = rng.uniform(150, 1250, 22)
    ins.scatter(np.full_like(dmu, 0.03), dmu, marker="_", s=90,
                color=STARS_GOLD, lw=1.8, zorder=5, label="DM only (most)")

    ins.set_xlim(0, 1.2)
    ins.set_ylim(-500, 1900)   # white strip at the bottom for the legend
    ins.set_xticks([0, 0.5, 1.0])
    ins.set_yticks([])
    ins.tick_params(labelsize=F_SMALL - 1, length=3, pad=2)
    ins.set_xlabel("z", fontsize=F_LAB, labelpad=1)
    ins.set_ylabel("DM", fontsize=F_LAB, labelpad=4)
    ins.grid(False)
    for s in ("left", "bottom"):
        ins.spines[s].set_color("#444444")
    ins.set_facecolor("white")
    ins.legend(loc="lower right", fontsize=F_SMALL - 1, frameon=False,
               handletextpad=0.4, borderaxespad=0.2, labelspacing=0.25)
    ins.text(0.03, 0.96, "mean DM(z) and its scatter", transform=ins.transAxes,
             ha="left", va="top", fontsize=F_SMALL, color=MUTED)


def draw_goal(ax):
    """Created by JXP and Claude. What is observed and what is inferred."""
    lines = ["Each burst: DM, signal/noise,",
             "telescope;  a few also have z",
             "Infer: population + DM scatter,",
             "jointly across all surveys"]
    y = 15.6
    for line in lines:
        ax.text(1.5, y, line, ha="left", va="center", fontsize=F_LAB,
                color=INK)
        y -= 3.2


def make_figure():
    """Created by JXP and Claude. Build and save the sketch."""
    style.apply_style()
    plt.rcParams["savefig.dpi"] = DPI
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(0, YMAX)
    ax.set_aspect("equal")
    ax.set_axis_off()
    draw_source(ax)
    draw_path(ax)
    draw_telescopes(ax)
    draw_catalog(ax)
    draw_goal(ax)
    draw_inset(ax)
    return style.save(fig, FIGS, "frb_sketch.png",
                      source="Sketch: J. X. Prochaska & Claude",
                      slide="UCSC Statistics README: FRB problem")


if __name__ == "__main__":
    make_figure()
