"""Created by JXP and Claude.

Figure for the slide "Math is a language too" (WMKO 2026 public lecture,
Sea meets the stars).

Message: a neural network that learned mathematics as a *language*
(Lample & Charton, Facebook AI Research, "Deep Learning for Symbolic
Mathematics", ICLR 2020, arXiv:1912.01412) solved integrals better than the
best computer-algebra software.

Left: horizontal bar chart, "Integrals solved correctly (%)", Matlab, Maple
and Mathematica in grey against the neural network in gold.
Right: one integral from the paper's Table 4 that Mathematica (and Matlab)
could not do and the network did.

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or the manifest named by the
SOURCES_JSON environment variable):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_lample_charton.py

    # verify the Table 4 example with sympy (d/dx of the solution == integrand)
    conda run -n ocean14 python talks/wmko_2026/scripts/fig_lample_charton.py --check

Output: talks/wmko_2026/figures/lample_charton.png
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke

from sms_outreach.slides import style
from sms_outreach.slides.style import STARS_GOLD, GRAY, INK, MUTED

FIGS = Path(__file__).resolve().parents[1] / "figures"

# ---------------------------------------------------------------------------
# Numbers, verified against the arXiv PDF (v1, 2 Dec 2019) on 2026-10-05.
#
# Lample, G. & Charton, F. (Facebook AI Research), "Deep Learning for
# Symbolic Mathematics", ICLR 2020, arXiv:1912.01412.
#
# Table 3: accuracy (%) on a test subset of 500 equations; "Integration (BWD)"
# column.  Mathematica 12.0 was given a timeout of 30 s per equation (Table 8:
# with no timeout its accuracy "would not exceed 86.2%"); Maple 2019 and
# Matlab R2019a had no timeout.  Caption: "On a given equation, our model
# typically finds the solution in less than a second."
#
#   Mathematica (30 s)   84.0
#   Matlab               65.2
#   Maple                67.4
#   model, beam size 1   98.4   <- used here (greedy decoding: one guess)
#   model, beam size 10  99.6
#   model, beam size 50  99.6
# ---------------------------------------------------------------------------
RESULTS = [                      # bottom -> top of the chart
    ("Matlab", 65.2, GRAY),
    ("Maple", 67.4, GRAY),
    ("Mathematica", 84.0, GRAY),
    ("Neural network\n(2019)", 98.4, STARS_GOLD),
]
TIMEOUT_S = 30                   # Mathematica's per-equation budget
MODEL_BEAM = 1                   # which model row is plotted

# Table 4, first row (model solved with greedy decoding; Mathematica and
# Matlab found no solution):
#   y' = (16x^3 - 42x^2 + 2x) / (-16x^8 + 112x^7 - 204x^6 + 28x^5 - x^4 + 1)^(1/2)
#   y  = sin^-1(4x^4 - 14x^3 + x^2)
EX_INTEGRAL = (r"$\int \dfrac{(16x^3 - 42x^2 + 2x)\,dx}"
               r"{(-16x^8 + 112x^7 - 204x^6 + 28x^5 - x^4 + 1)^{1/2}}$")
EX_SOLUTION = r"$\sin^{-1}\!\left(4x^4 - 14x^3 + x^2\right)$"

GOLD_DARK = "#9c6f00"


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def check_example():
    """Created by JXP and Claude. Verify the Table 4 example symbolically:
    d/dx asin(4x^4 - 14x^3 + x^2) must equal the integrand."""
    import sympy as sp
    x = sp.symbols("x")
    y = sp.asin(4 * x**4 - 14 * x**3 + x**2)
    integrand = ((16 * x**3 - 42 * x**2 + 2 * x)
                 / sp.sqrt(-16 * x**8 + 112 * x**7 - 204 * x**6
                           + 28 * x**5 - x**4 + 1))
    diff = sp.simplify(sp.diff(y, x) - integrand)
    print("d/dx(solution) - integrand =", diff)
    assert diff == 0, "Table 4 example does not check out"
    print("Table 4 example verified.")


def draw_bars(ax):
    """Created by JXP and Claude. Horizontal bars, values in big type inside
    the bar ends; the neural network highlighted in gold."""
    names = [r[0] for r in RESULTS]
    vals = [r[1] for r in RESULTS]
    cols = [r[2] for r in RESULTS]
    ys = range(len(RESULTS))
    ax.barh(ys, vals, height=0.66, color=cols, zorder=3)
    for y, v, c in zip(ys, vals, cols):
        ax.text(v - 2.0, y, f"{v:.0f}%", ha="right", va="center",
                fontsize=22, color="white", zorder=4,
                path_effects=bold("white", 0.9))
    ax.set_yticks(list(ys))
    ax.set_yticklabels(names, fontsize=17)
    for lab, c in zip(ax.get_yticklabels(), cols):
        if c == STARS_GOLD:
            lab.set_color(GOLD_DARK)
            lab.set_path_effects(bold(GOLD_DARK, 0.7))
    ax.set_xlim(0, 100)
    ax.set_ylim(-0.6, len(RESULTS) - 0.4)
    ax.set_xticks([0, 50, 100])
    ax.set_xticklabels(["0", "50", "100%"], fontsize=16)
    ax.set_xlabel("Integrals solved correctly", fontsize=17, color=INK)
    ax.grid(axis="y", visible=False)
    ax.grid(axis="x", alpha=0.3, zorder=0)
    ax.spines["left"].set_visible(False)
    ax.tick_params(axis="y", length=0)
    ax.tick_params(axis="x", length=3)
    # the three grey bars are the traditional programs
    ax.text(72.5, 0.5, "math\nsoftware", ha="left", va="center", fontsize=16,
            color=MUTED, style="italic", linespacing=1.1, clip_on=False,
            zorder=5)


def draw_example(ax):
    """Created by JXP and Claude. Right panel: the worked example from
    Table 4 (a \\dfrac keeps the numerator and denominator at full size)
    and the time contrast."""
    ax.set_axis_off()
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.text(0.0, 1.0, "It learned math as a language,\n"
            "and did integrals the software couldn't:",
            ha="left", va="top", fontsize=16, color=INK, linespacing=1.25)
    ax.text(0.5, 0.60, EX_INTEGRAL, ha="center", va="center", fontsize=16,
            color=INK, clip_on=False)
    ax.text(0.0, 0.30, f"Mathematica ({TIMEOUT_S} s):  no answer",
            ha="left", va="center", fontsize=16, color=MUTED)
    ax.text(0.0, 0.11, "Network (< 1 s):  " + EX_SOLUTION,
            ha="left", va="center", fontsize=17, color=GOLD_DARK,
            path_effects=bold(GOLD_DARK, 0.5))


def make_figure():
    """Created by JXP and Claude. Build and save the figure."""
    style.apply_style()
    fig, (ax_bar, ax_ex) = plt.subplots(
        1, 2, figsize=style.FULL, gridspec_kw=dict(width_ratios=[0.62, 1.6]))
    draw_bars(ax_bar)
    draw_example(ax_ex)
    return style.save(fig, FIGS, "lample_charton.png",
                      source="Lample & Charton 2020 (ICLR), Table 3",
                      slide="Math is a language too",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    if "--check" in sys.argv[1:]:
        check_example()
    make_figure()
