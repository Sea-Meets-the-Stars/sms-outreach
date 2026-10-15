"""Created by JXP and Claude.

Sketch of the ocean-colour inverse problem for the UCSC Statistics README
(talk "Advancing science on the frontier with modern statistical
techniques", 2026).  Meant to sit at half-page width in a Google Doc, so
the text is large and sparse.

Left  -- the forward problem as a cartoon: sunlight enters the sea; water,
         phytoplankton, dissolved organic matter (CDOM) and particles absorb
         (a) and backscatter (b_b) it; a satellite (PACE) records the colour
         spectrum Rrs(lambda).  The Gordon forward model is written out.
Right -- the inverse problem: (top) one Rrs(lambda) spectrum with its PACE
         error band and three model fits that are *identical*; (bottom)
         the three very different (a, b_b) pairs that produced them --
         non-water absorption scaled by 1, 3 and 10 with the backscattering
         adjusted so that u = b_b/(a+b_b) is unchanged (the bb/a degeneracy
         of Prochaska & Frouin 2025, their Fig. 4).

The degeneracy curves are computed properly: the "truth" is spectrum
index 170 of the Loisel et al. (2023) Hydrolight set (loaded read-only
through ocpy), Rrs follows the Gordon relation with BING's constants
(bing.rt.rrs; imported read-only), and the PACE noise is BING's median
Level-2 uncertainty table.

Run from the repo root:

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_ocean_sketch.py

Output: talks/ucsc_stats_2026/figures/ocean_sketch.png  (8 x 4.5 in, 200 dpi)
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Rectangle, Wedge
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import SEA, STARS_GOLD, RED, INK, MUTED, GRAY

FIGS = Path(__file__).resolve().parents[1] / "figures"
OUT = FIGS / "ocean_sketch.png"
FIGSIZE, DPI = (8.0, 4.5), 200

# Palette: sea blue / gold / red for the three degenerate solutions, each
# with its own line style so identity never rests on colour alone.
SOLUTIONS = [(1.0, SEA, "-", 2.6), (3.0, STARS_GOLD, "--", 2.2),
             (10.0, RED, ":", 2.4)]
SEA_FILL = "#d6e6f5"
GOLD_DARK = "#9c6f00"
GREEN = "#3c8d3c"
CDOM = "#b48a3c"
WAVE_LO, WAVE_HI = 400.0, 700.0
L23_INDEX = 170                     # the paper's representative example


def bold(color, lw=0.9):
    """Created by JXP and Claude. Faux-bold path effect (the bundled Roboto
    is a variable font and matplotlib cannot pick its bold instance)."""
    return [withStroke(linewidth=lw, foreground=color)]


# ----------------------------------------------------------------------
# Physics: truth, PACE noise and the degenerate family of solutions
# ----------------------------------------------------------------------
def load_truth():
    """Created by JXP and Claude. Return (wave, a_w, a_nw, bb_w, bb_nw) for
    the L23 example spectrum on 400-700 nm (5 nm sampling)."""
    from ocpy.hydrolight import loisel23              # read-only
    ds = loisel23.load_ds(4, 0)
    wave = ds.Lambda.data
    keep = (wave >= WAVE_LO) & (wave <= WAVE_HI)
    a = ds.a.data[L23_INDEX][keep]
    anw = ds.anw.data[L23_INDEX][keep]
    bb = ds.bb.data[L23_INDEX][keep]
    bbnw = ds.bbnw.data[L23_INDEX][keep]
    return wave[keep], a - anw, anw, bb - bbnw, bbnw


def pace_sigma(wave):
    """Created by JXP and Claude. Median PACE/OCI Level-2 Rrs uncertainty
    (BING's table) interpolated to `wave`."""
    from importlib import resources
    import bing                                        # read-only
    tab = pd.read_csv(Path(resources.files("bing")) / "data" / "PACE"
                      / "PACE_error.csv")
    return np.interp(wave, tab["wave"].values, tab["PACE_sig"].values)


def degenerate_family(a_w, a_nw, bb_w, bb_nw):
    """Created by JXP and Claude. For each scale factor s in SOLUTIONS,
    scale the non-water absorption by s and solve for the backscattering
    that keeps u = bb/(a+bb) -- hence Rrs -- exactly unchanged.

    Returns list of (s, a_total, bb_total, Rrs)."""
    from bing.rt import rrs as bing_rrs                # read-only
    a0, bb0 = a_w + a_nw, bb_w + bb_nw
    u = bb0 / (a0 + bb0)
    out = []
    for s, *_ in SOLUTIONS:
        a_s = a_w + s * a_nw
        bb_s = u * a_s / (1.0 - u)
        out.append((s, a_s, bb_s, bing_rrs.calc_Rrs(a_s, bb_s)))
    return out


# ----------------------------------------------------------------------
# Left: the forward problem as a cartoon
# ----------------------------------------------------------------------
def draw_cartoon(ax):
    """Created by JXP and Claude. Sun, satellite, sea with constituents."""
    W, H = 46.0, 56.0
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.set_axis_off()

    ax.text(1.0, H - 1.5, "Forward problem", ha="left", va="top", fontsize=14,
            color=INK, path_effects=bold(INK))
    ax.text(1.0, H - 5.0, "light in  →  colour out", ha="left",
            va="top", fontsize=11.5, color=MUTED)

    # --- sea
    y_surf = 31.0
    xs = np.linspace(0, W, 300)
    wave = y_surf + 0.5 * np.sin(2 * np.pi * xs / 6.0)
    ax.fill_between(xs, 7.0, wave, color=SEA_FILL, lw=0, zorder=1)
    ax.plot(xs, wave, color=SEA, lw=1.8, zorder=2)

    # --- sun
    sx, sy = 6.5, 41.0
    for ang in np.arange(0, 360, 45):
        th = np.radians(ang)
        ax.plot([sx + 3.3 * np.cos(th), sx + 4.6 * np.cos(th)],
                [sy + 3.3 * np.sin(th), sy + 4.6 * np.sin(th)],
                color=STARS_GOLD, lw=1.6, zorder=3)
    ax.add_patch(Circle((sx, sy), 2.7, facecolor=STARS_GOLD,
                        edgecolor=GOLD_DARK, lw=1.0, zorder=3))

    # --- satellite (PACE)
    px, py = 36.0, 43.0
    for dx in (-5.6, 1.6):                                 # solar panels
        ax.add_patch(Rectangle((px + dx, py - 0.65), 4.0, 1.3, facecolor=SEA,
                               edgecolor="white", lw=0.8, zorder=3))
        for k in range(1, 4):
            ax.plot([px + dx + k] * 2, [py - 0.65, py + 0.65], color="white",
                    lw=0.7, zorder=3.5)
    ax.add_patch(Rectangle((px - 1.6, py - 1.0), 3.2, 2.0, facecolor="#555555",
                           edgecolor=INK, lw=0.9, zorder=4))
    ax.add_patch(Wedge((px, py - 1.0), 1.0, 200, 340, facecolor="white",
                       edgecolor=INK, lw=0.9, zorder=4))
    ax.text(px, py + 2.2, "PACE satellite", ha="center", va="bottom",
            fontsize=11, color=INK)

    # --- light path: sun -> sea -> satellite
    arrow = dict(arrowstyle="-|>,head_length=0.7,head_width=0.35",
                 color=GOLD_DARK, lw=2.0, shrinkA=0, shrinkB=0)
    ax.annotate("", (16.5, y_surf + 0.2), (9.2, 38.2), arrowprops=arrow,
                zorder=5)
    ax.annotate("", (21.5, 20.5), (16.5, y_surf + 0.2),
                arrowprops=dict(arrowstyle="-", color=GOLD_DARK, lw=2.0,
                                shrinkA=0, shrinkB=0), zorder=5)
    ax.annotate("", (px - 0.5, py - 2.4), (21.5, 20.5),
                arrowprops=dict(arrowstyle="-|>,head_length=0.7,head_width=0.35",
                                color=SEA, lw=2.0, shrinkA=0, shrinkB=0),
                zorder=5)
    ax.text(38.8, 34.5, "colour spectrum\n$R_{rs}(\\lambda)$", ha="center",
            va="center", fontsize=12, color=SEA, path_effects=bold(SEA, 0.6),
            zorder=6, bbox=dict(boxstyle="round,pad=0.25", facecolor="white",
                                edgecolor="none", alpha=0.9))

    # --- constituents in the water
    for (cx, cy, w, h, a) in [(8.5, 24.5, 2.6, 1.3, 20), (11.0, 23.2, 2.4, 1.2, -10),
                              (7.5, 21.0, 2.0, 1.1, 35), (12.5, 14.0, 2.6, 1.3, -25),
                              (7.5, 10.5, 2.2, 1.2, 10)]:
        ax.add_patch(Ellipse((cx, cy), w, h, angle=a, facecolor=GREEN,
                             edgecolor="#1f5b1f", lw=0.7, zorder=3))
    ax.add_patch(Ellipse((30.0, 13.0), 17.0, 7.6, facecolor=CDOM, lw=0,
                         alpha=0.28, zorder=2.5))
    rng = np.random.default_rng(3)
    ax.scatter(rng.uniform(24, 44, 22), rng.uniform(21.5, 27.3, 22), s=9,
               color=GRAY, zorder=3)

    # labels (sparse, plain words)
    lab = dict(fontsize=10.5, color=INK, zorder=6,
               bbox=dict(boxstyle="round,pad=0.15", facecolor="white",
                         edgecolor="none", alpha=0.75))
    ax.text(9.5, 27.0, "phytoplankton", ha="center", va="bottom", **lab)
    ax.text(34.0, 27.8, "particles", ha="center", va="bottom", **lab)
    ax.text(30.0, 13.0, "dissolved organic\nmatter (CDOM)", ha="center",
            va="center", **lab)
    ax.text(23.5, 18.9, "absorb $a(\\lambda)$, backscatter $b_b(\\lambda)$",
            ha="center", va="top", fontsize=11.5, color=INK,
            path_effects=bold(INK, 0.5), zorder=6,
            bbox=dict(boxstyle="round,pad=0.2", facecolor="white",
                      edgecolor="none", alpha=0.85))

    # --- the forward model
    ax.add_patch(FancyBboxPatch((0.6, 0.4), W - 1.2, 6.0,
                                boxstyle="round,pad=0,rounding_size=0.8",
                                facecolor="white", edgecolor=GRAY, lw=1.0,
                                zorder=2))
    ax.text(W / 2, 3.4,
            "$R_{rs}(\\lambda) \\approx G_1 u + G_2 u^2, \\quad "
            "u = \\dfrac{b_b}{a + b_b}$",
            ha="center", va="center", fontsize=12.5, color=INK, zorder=3)


# ----------------------------------------------------------------------
# Right: the inverse problem
# ----------------------------------------------------------------------
def draw_rrs(ax, wave, family, sigma):
    """Created by JXP and Claude. Observed Rrs with PACE error band and the
    three (identical) model curves."""
    rng = np.random.default_rng(7)
    truth = 1e3 * family[0][3]
    sigma = 1e3 * sigma
    obs = truth + rng.normal(0, sigma)
    ax.fill_between(wave, truth - sigma, truth + sigma, color=GRAY, alpha=0.3,
                    lw=0)
    ax.scatter(wave[::3], obs[::3], s=9, color=INK, zorder=3)
    for (s, col, ls, lw), (_, _, _, R) in zip(SOLUTIONS, family):
        ax.plot(wave, 1e3 * R, color=col, ls=ls, lw=lw, zorder=4,
                label=f"fit, $a_{{nw}}\\times{s:g}$")
    ax.legend(loc="lower right", bbox_to_anchor=(0.99, 0.03), frameon=False,
              fontsize=9.5, handlelength=2.0, borderaxespad=0.0,
              labelspacing=0.25)
    ax.set_xlim(WAVE_LO, WAVE_HI)
    ax.set_ylim(0, 1.15 * (truth + sigma).max())
    ax.set_ylabel("$R_{rs}\\times10^{3}$  [sr$^{-1}$]", fontsize=10.5)
    ax.set_xlabel("wavelength $\\lambda$  [nm]", fontsize=10.5, labelpad=0)
    ax.tick_params(labelsize=9.5)
    ax.text(0.97, 0.92, "3 fits, all identical", transform=ax.transAxes,
            ha="right", va="top", fontsize=11, color=INK,
            path_effects=bold(INK, 0.5))
    ax.text(0.97, 0.76, "band = PACE noise, dots = data", transform=ax.transAxes,
            ha="right", va="top", fontsize=9.5, color=MUTED)


def draw_iops(ax_a, ax_b, wave, family, a_w, bb_w):
    """Created by JXP and Claude. The three (a, b_b) pairs behind the
    identical fits, with pure water for reference."""
    for ax, idx, ylab in ((ax_a, 1, "absorption $a$"),
                          (ax_b, 2, "backscatter $b_b$")):
        for (s, col, ls, lw), sol in zip(SOLUTIONS, family):
            ax.plot(wave, sol[idx], color=col, ls=ls, lw=lw,
                    label=f"$a_{{nw}}\\times{s:g}$")
        ax.plot(wave, a_w if idx == 1 else bb_w, color=GRAY, lw=1.0,
                alpha=0.8, zorder=1)
        ax.set_yscale("log")
        ax.set_xlim(WAVE_LO, WAVE_HI)
        ax.set_xticks([400, 550, 700])
        ax.tick_params(labelsize=9.5)
        ax.set_title(ylab + " (m$^{-1}$)", fontsize=10, pad=3)
        ax.set_xlabel("$\\lambda$  [nm]", fontsize=11, labelpad=1)
    ax_a.set_ylim(3e-3, 1.5)
    ax_b.set_ylim(2e-4, 1e-1)
    ax_a.text(560, 3.4e-3, "water alone", ha="left", va="bottom", fontsize=9,
              color=GRAY)
    ax_b.text(408, 2.3e-4, "water alone", ha="left", va="bottom", fontsize=9,
              color=GRAY)


def make_figure():
    """Created by JXP and Claude. Build and save the sketch."""
    style.apply_style()
    plt.rcParams.update({"axes.grid": False, "mathtext.fontset": "dejavusans"})
    wave, a_w, a_nw, bb_w, bb_nw = load_truth()
    family = degenerate_family(a_w, a_nw, bb_w, bb_nw)
    sigma = pace_sigma(wave)

    fig = plt.figure(figsize=FIGSIZE)
    ax_c = fig.add_axes([0.0, 0.0, 0.46, 1.0])
    ax_r = fig.add_axes([0.575, 0.615, 0.405, 0.26])
    ax_a = fig.add_axes([0.575, 0.12, 0.185, 0.27])
    ax_b = fig.add_axes([0.795, 0.12, 0.185, 0.27])
    draw_cartoon(ax_c)
    draw_rrs(ax_r, wave, family, sigma)
    draw_iops(ax_a, ax_b, wave, family, a_w, bb_w)

    fig.text(0.50, 0.975, "Inverse problem", ha="left", va="top", fontsize=14,
             color=INK, path_effects=bold(INK))
    fig.text(0.50, 0.92, "the satellite sees only $u = b_b/(a+b_b)$",
             ha="left", va="top", fontsize=11.5, color=MUTED)
    fig.text(0.50, 0.50, "...but from very different oceans:", ha="left",
             va="top", fontsize=11, color=INK)
    fig.text(0.50, 0.463, "non-water absorption $a_{nw}$ $\\times$1, $\\times$3, "
             "$\\times$10; $b_b$ adjusted",
             ha="left", va="top", fontsize=10.5, color=MUTED)

    FIGS.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI, facecolor="white")
    plt.close(fig)
    print(f"Wrote {OUT}")
    return OUT


if __name__ == "__main__":
    make_figure()
