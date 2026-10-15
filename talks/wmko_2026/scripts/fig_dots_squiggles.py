"""Created by JXP and Claude.

Dots and squiggles for the slide "Describe what you see" (WMKO 2026 public
lecture, Sea meets the stars).  Replaces two low-resolution web images of
unknown origin with our own:

  dots.png      -- a regular 12 x 12 grid of black dots
  squiggles.png -- a black/white labyrinth from a Gray-Scott
                   reaction-diffusion simulation (Turing pattern)

Run from the repo root (conda run does not pass stdin):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_dots_squiggles.py
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt

from sms_outreach.slides import style

FIGS = Path(__file__).resolve().parents[1] / "figures"
SIZE = (4.2, 4.2)        # inches: one side of a sea | stars pair
SLIDE = "Describe what you see"


def dots_figure():
    """Created by JXP and Claude. A 12 x 12 grid of black dots."""
    fig, ax = plt.subplots(figsize=SIZE)
    x, y = np.meshgrid(np.arange(12), np.arange(12))
    ax.scatter(x.ravel(), y.ravel(), s=260, color="black")
    ax.set_xlim(-0.7, 11.7)
    ax.set_ylim(-0.7, 11.7)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig


def gray_scott(n=256, steps=12000, f=0.037, k=0.06, du=0.16, dv=0.08, seed=3):
    """Created by JXP and Claude. Gray-Scott reaction-diffusion on an n x n
    periodic grid (explicit Euler, dt = 1); these (f, k) give labyrinths.
    Returns the V field."""
    rng = np.random.default_rng(seed)
    u = np.ones((n, n))
    v = np.zeros((n, n))
    v += (rng.random((n, n)) < 0.08) * 0.5     # random seeds everywhere
    u -= v

    def lap(z):
        return (np.roll(z, 1, 0) + np.roll(z, -1, 0) + np.roll(z, 1, 1) + np.roll(z, -1, 1) - 4 * z)

    for _ in range(steps):
        uvv = u * v * v
        u += du * lap(u) - uvv + f * (1 - u)
        v += dv * lap(v) + uvv - (f + k) * v
    return v


def squiggles_figure():
    """Created by JXP and Claude. Threshold a Gray-Scott pattern to black/white."""
    v = gray_scott()
    fig, ax = plt.subplots(figsize=SIZE)
    ax.imshow(v > np.median(v), cmap="gray_r", interpolation="bicubic")
    ax.axis("off")
    return fig


def main():
    """Created by JXP and Claude. Make and save both figures."""
    style.apply_style()
    src = os.environ.get("SOURCES_JSON")
    style.save(dots_figure(), FIGS, "dots.png", source="J. X. Prochaska & Claude", slide=SLIDE,
               sources_json=src)
    style.save(squiggles_figure(), FIGS, "squiggles.png",
               source="Gray-Scott reaction-diffusion simulation (J. X. Prochaska & Claude)", slide=SLIDE,
               sources_json=src)


if __name__ == "__main__":
    main()
