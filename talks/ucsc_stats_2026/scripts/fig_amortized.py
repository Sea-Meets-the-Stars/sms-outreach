"""Created by JXP and Claude.

Schematic for the slide "Can we GP this?" (UCSC Statistics 2026,
sub-line "Amortize: simulate, train, infer every pixel in one pass").

Contrasts two ways of inferring ocean constituents from one satellite
reflectance spectrum R_rs(lambda), drawn with matplotlib patches and text
only (no external images), in the sea | stars palette:

  LEFT  (sea)   "Today: per-pixel MCMC"
        one spectrum icon -> [Gordon forward model + Gaussian likelihood]
        --emcee: 75,000 steps, ~10^6 likelihood calls--> corner-plot icon,
        "posterior for ONE pixel"; in red: seconds-minutes per spectrum
        x 10^8 spectra a day.
  RIGHT (stars) "Amortized: simulate, train, infer"
        [simulate: 3,320 Hydrolight spectra (L23) + PACE noise, forward
        model] -> [train: GP or neural map, spectrum -> posterior] ->
        pixel-grid icon + [infer: every PACE pixel in one pass ->
        posterior for EVERY pixel]; in red: does it stay calibrated when
        the real data have systematics?

Both halves are three rows (A: input/model, B: the expensive step, C: the
posterior) at the same heights, separated by a thin vertical divider.

Run from the repo root (the script writes the PNG and updates the sources
manifest named by the SOURCES_JSON environment variable, else the
scratch MANIFEST below, to be merged into figures/sources.json):

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_amortized.py

Output: talks/ucsc_stats_2026/figures/amortized_schematic.png (9.2 x 3.4 in)
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, FancyArrowPatch, FancyBboxPatch, Rectangle
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, SEA_LIGHT, STARS, STARS_GOLD,
                                       RED, INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"
# Sources manifest: a scratch file during drafting (merged into
# figures/sources.json later); override with the SOURCES_JSON env variable.
MANIFEST = os.environ.get("SOURCES_JSON", str(FIGS / "sources.json"))

# Drawing canvas in data units: 1 x-unit ~ 0.1 in on the slide.
XMAX, YMIN, YMAX = 92.0, -2.0, 36.0
X_DIV = 46.0                      # the sea | stars divider
SEA_FILL, STARS_FILL = "#e4eef9", "#ebe9f6"   # pale box fills
GOLD_DARK = "#9c6f00"

# Row extents (y0, y1) shared by both halves, plus the header and red lines.
ROW_A = (25.0, 31.5)
ROW_B = (15.0, 21.5)
ROW_C = (5.0, 11.5)
Y_HEAD = 34.0
Y_RED = 1.0                       # centre of the two red lines
# Horizontal extents.
L_ICON = (2.0, 11.0)              # left-half icons (spectrum, corner plot)
L_BOX = (14.0, 44.0)              # left-half boxes
R_BOX = (48.5, 90.5)              # right-half full-width boxes
R_ICON = (48.5, 55.5)             # pixel-grid icon
R_BOX_C = (58.0, 90.5)            # the infer box beside it


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def _mid(span):
    """Created by JXP and Claude. Midpoint of an (x0, x1) span."""
    return 0.5 * (span[0] + span[1])


def box(ax, xs, ys, text, edge, fill, fontsize=14, color=INK, lw=1.6):
    """Created by JXP and Claude. Rounded box spanning xs x ys with centred
    text."""
    ax.add_patch(FancyBboxPatch((xs[0], ys[0]), xs[1] - xs[0], ys[1] - ys[0],
                                boxstyle="round,pad=0,rounding_size=1.2",
                                facecolor=fill, edgecolor=edge, lw=lw,
                                zorder=3))
    ax.text(_mid(xs), _mid(ys), text, ha="center", va="center",
            fontsize=fontsize, color=color, linespacing=1.25, zorder=4)


def arrow(ax, p0, p1, color, lw=1.8, scale=16):
    """Created by JXP and Claude. Straight arrow from p0 to p1."""
    ax.add_patch(FancyArrowPatch(p0, p1, arrowstyle="-|>",
                                 mutation_scale=scale, color=color, lw=lw,
                                 shrinkA=0, shrinkB=0, zorder=5))


def draw_spectrum_icon(ax, xs, ys):
    """Created by JXP and Claude. One R_rs(lambda) spectrum with PACE-like
    error bars in a small white card."""
    x0, x1 = xs
    y0, y1 = ys
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                facecolor="white", edgecolor=SEA, lw=1.4,
                                zorder=3))
    # tiny axes inside the card
    ax0, ax1 = x0 + 2.4, x1 - 0.7
    ay0, ay1 = y0 + 1.5, y1 - 0.7
    ax.plot([ax0, ax0, ax1], [ay1, ay0, ay0], color=MUTED, lw=0.9, zorder=4)
    # the spectrum: a blue-green hump that fades into the red
    lam = np.linspace(0, 1, 60)
    rrs = np.exp(-((lam - 0.28) / 0.28) ** 2) + 0.08 * np.exp(-((lam - 0.72) / 0.06) ** 2)
    rrs /= rrs.max()
    px = ax0 + 0.6 + lam * (ax1 - ax0 - 1.0)
    py = ay0 + 0.5 + rrs * (ay1 - ay0 - 1.0)
    ax.plot(px, py, color=SEA, lw=1.8, zorder=5)
    k = np.arange(4, 60, 8)
    ax.errorbar(px[k], py[k], yerr=0.07 * (ay1 - ay0) * (1 + lam[k]),
                fmt="o", ms=2.6, color=SEA, ecolor=SEA_LIGHT, elinewidth=1.2,
                capsize=1.5, zorder=6)
    ax.text(0.5 * (ax0 + ax1), ay0 - 0.2, r"$\lambda$", ha="center",
            va="top", fontsize=11, color=MUTED, zorder=6)
    ax.text(ax0 - 0.35, 0.5 * (ay0 + ay1), r"$R_{rs}$", ha="right",
            va="center", fontsize=11, color=MUTED, zorder=6)


def draw_corner_icon(ax, xs, ys):
    """Created by JXP and Claude. A 2x2 corner plot: two histograms on the
    diagonal and nested contours below."""
    x0, x1 = xs
    y0, y1 = ys
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                facecolor="white", edgecolor=SEA, lw=1.4,
                                zorder=3))
    pad = 0.9
    w = (x1 - x0 - 2 * pad - 0.6) / 2
    h = (y1 - y0 - 2 * pad - 0.6) / 2
    cells = {"tl": (x0 + pad, y0 + pad + h + 0.6),
             "bl": (x0 + pad, y0 + pad),
             "br": (x0 + pad + w + 0.6, y0 + pad)}
    for key, (cx, cy) in cells.items():
        ax.plot([cx, cx, cx + w], [cy + h, cy, cy], color=MUTED, lw=0.8,
                zorder=4)
        if key in ("tl", "br"):                      # histogram
            nb = 9
            centres = cx + (np.arange(nb) + 0.5) * w / nb
            prof = np.exp(-((np.arange(nb) - 4.2) / 1.7) ** 2)
            if key == "br":
                prof = np.exp(-((np.arange(nb) - 3.4) / 2.4) ** 2)
            for xc, p in zip(centres, prof):
                ax.add_patch(Rectangle((xc - 0.5 * w / nb, cy), w / nb,
                                       p * (h - 0.25), facecolor=SEA_LIGHT,
                                       edgecolor=SEA, lw=0.6, zorder=5))
        else:                                        # banana-ish contours
            for s, col in ((1.0, SEA_LIGHT), (0.62, SEA)):
                ax.add_patch(Ellipse((cx + 0.5 * w, cy + 0.5 * h),
                                     0.85 * w * s, 0.55 * h * s, angle=35,
                                     facecolor=col, edgecolor=SEA, lw=0.6,
                                     alpha=0.9, zorder=5))


def draw_pixel_grid(ax, xs, ys, n=6, seed=3):
    """Created by JXP and Claude. A small image grid (many pixels) shaded
    in blues like a PACE scene."""
    x0, x1 = xs
    y0, y1 = ys
    rng = np.random.default_rng(seed)
    cmap = plt.get_cmap("Blues")
    w = (x1 - x0) / n
    h = (y1 - y0) / n
    xx, yy = np.meshgrid(np.arange(n), np.arange(n))
    field = 0.45 + 0.45 * np.sin(0.9 * xx + 0.4 * yy) * np.cos(0.5 * yy)
    field = np.clip(field + 0.12 * rng.standard_normal(field.shape), 0.15, 1.0)
    for i in range(n):
        for j in range(n):
            ax.add_patch(Rectangle((x0 + j * w, y0 + i * h), w, h,
                                   facecolor=cmap(field[i, j]),
                                   edgecolor="white", lw=0.8, zorder=4))
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0, facecolor="none",
                           edgecolor=STARS, lw=1.4, zorder=5))


def draw_left(ax):
    """Created by JXP and Claude. Today: per-pixel MCMC."""
    xc = _mid((L_ICON[0], L_BOX[1]))
    ax.text(xc, Y_HEAD, "Today: per-pixel MCMC", ha="center", va="center",
            fontsize=16, color=SEA, path_effects=bold(SEA, 0.9))
    # Row A: one spectrum -> forward model + likelihood
    draw_spectrum_icon(ax, L_ICON, ROW_A)
    arrow(ax, (L_ICON[1] + 0.3, _mid(ROW_A)), (L_BOX[0] - 0.3, _mid(ROW_A)), SEA)
    box(ax, L_BOX, ROW_A, "Gordon forward model\n+ Gaussian likelihood",
        SEA, SEA_FILL)
    # Row B: the long emcee arrow down to the posterior, labelled beside it
    x_arr = L_BOX[0] + 4.5
    arrow(ax, (x_arr, ROW_A[0] - 0.3), (x_arr, ROW_C[1] + 0.3), SEA, lw=2.2,
          scale=18)
    ax.text(x_arr + 2.2, _mid(ROW_B),
            "emcee: 75,000 steps,\n~10$^{6}$ likelihood calls",
            ha="left", va="center", fontsize=14, color=INK, linespacing=1.25)
    # Row C: the posterior for one pixel
    draw_corner_icon(ax, L_ICON, ROW_C)
    box(ax, L_BOX, ROW_C, "posterior for ONE pixel", SEA, SEA_FILL)
    ax.text(xc, Y_RED, "seconds–minutes per spectrum\n×  10$^{8}$ spectra a day",
            ha="center", va="center", fontsize=13, color=RED, linespacing=1.2)


def draw_right(ax):
    """Created by JXP and Claude. Amortized: simulate, train, infer."""
    xc = _mid(R_BOX)
    ax.text(xc, Y_HEAD, "Amortized: simulate, train, infer", ha="center",
            va="center", fontsize=16, color=STARS, path_effects=bold(STARS, 0.9))
    box(ax, R_BOX, ROW_A,
        "simulate: 3,320 Hydrolight spectra (L23)\n+ PACE noise, forward model",
        STARS, STARS_FILL, fontsize=13)
    x_arr = _mid(R_BOX_C)
    arrow(ax, (x_arr, ROW_A[0] - 0.3), (x_arr, ROW_B[1] + 0.3), STARS, lw=2.2,
          scale=18)
    box(ax, R_BOX, ROW_B, "train: GP or neural map,\nspectrum → posterior",
        STARS, STARS_FILL, fontsize=13)
    arrow(ax, (x_arr, ROW_B[0] - 0.3), (x_arr, ROW_C[1] + 0.3), STARS, lw=2.2,
          scale=18)
    draw_pixel_grid(ax, R_ICON, ROW_C)
    box(ax, R_BOX_C, ROW_C,
        "infer: every PACE pixel, one pass\n→ posterior for EVERY pixel",
        STARS, STARS_FILL, fontsize=13)
    ax.text(xc, Y_RED, "does it stay calibrated\nwhen the real data have systematics?",
            ha="center", va="center", fontsize=13, color=RED, linespacing=1.2)


def main():
    """Created by JXP and Claude. Build and save the schematic."""
    style.apply_style()
    fig, ax = plt.subplots(figsize=style.FULL)
    ax.set_xlim(0, XMAX)
    ax.set_ylim(YMIN, YMAX)
    ax.set_axis_off()
    ax.plot([X_DIV, X_DIV], [YMIN + 0.5, YMAX - 0.5], color=MUTED, lw=0.9,
            alpha=0.6, zorder=2)
    draw_left(ax)
    draw_right(ax)
    return style.save(fig, FIGS, "amortized_schematic.png",
                      source="Schematic: J. X. Prochaska & Claude",
                      slide="Can we GP this?", sources_json=MANIFEST)


if __name__ == "__main__":
    main()
