"""Created by JXP and Claude.

Half-slide figure for "HIRES: weighing the Universe and finding planets"
(WMKO 2026 public lecture, Sea meets the stars).  It sits on the RIGHT half
of the slide, next to a photo of HIRES.

Two stacked panels:

  (top)    A schematic quasar absorption spectrum around Lyman-alpha: the
           deep, saturated H I trough and the small D I line 81.6 km/s
           blueward of it (Voigt profiles; labelled as a schematic).
  (bottom) The Big Bang nucleosynthesis (BBN) prediction of primordial D/H
           versus the baryon density Omega_b h^2, the HIRES-measured D/H
           band (Cooke et al. 2018) dropped onto the curve to give
           Omega_b h^2, and the Planck 2018 CMB value for comparison.

Published values used (verified on arXiv / ADS, 2026-10-05):

  * Primordial D/H = (2.527 +/- 0.030) x 10^-5 and
    100 Omega_b h^2 (BBN) = 2.166 +/- 0.015 (meas.) +/- 0.011 (BBN), i.e.
    Omega_b h^2 = 0.02166 +/- 0.00019 (errors added in quadrature), with
    the Marcucci et al. (2016) d(p,gamma)3He rate.
      Cooke, Pettini & Steidel 2018, ApJ, 855, 102 (arXiv:1710.11129),
      abstract and their Eq. 12.
  * Planck 2018 CMB: Omega_b h^2 = 0.02237 +/- 0.00015
      (TT,TE,EE+lowE+lensing; Planck Collaboration 2020, A&A, 641, A6,
      arXiv:1807.06209, Table 2).
  * First precise HIRES D/H measurements: Burles & Tytler 1998,
      ApJ, 499, 699 (Q1937-1009) and ApJ, 507, 732 (Q1009+2956).
  * BBN scaling: (D/H)_p is a power law in the baryon-to-photon ratio,
      (D/H)_p ~ eta_10^-1.6  with  eta_10 = 273.9 Omega_b h^2
      (Steigman 2012, Adv. High Energy Phys. 2012, 268321; quoted as
      (D/H)_p = 2.55e-5 (6/eta_10)^1.6 in Cooke et al. 2014, ApJ, 781, 31).
    The 2.55e-5 normalization predates the Marcucci et al. (2016) rate, so
    here the curve is anchored to the Cooke et al. 2018 solution instead:
      (D/H)_p = 2.527e-5 x (Omega_b h^2 / 0.02166)^-1.6
    i.e. it passes through the measured D/H at the quoted Omega_b h^2 by
    construction; the eta_10 conversion is only used for the top axis.
  * D I - H I isotope shift: 81.6 km/s (reduced-mass shift of the Lyman
    series; e.g. Cooke et al. 2014).

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or the manifest named by the
SOURCES_JSON environment variable):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_dh_omega_b.py

Output: talks/wmko_2026/figures/dh_omega_b.png
"""
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from scipy.special import wofz

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, STARS, STARS_GOLD, RED, GRAY,
                                       INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"

# ---------------------------------------------------------------- numbers
DH_P, DH_ERR = 2.527e-5, 0.030e-5        # Cooke et al. 2018
OMB_BBN, OMB_BBN_ERR = 0.02166, 0.00019  # Cooke et al. 2018, Eq. 12
OMB_CMB, OMB_CMB_ERR = 0.02237, 0.00015  # Planck 2018, Table 2
ETA_PER_OMB = 273.9                      # eta_10 = 273.9 Omega_b h^2
SLOPE = -1.6                             # (D/H)_p ~ eta^-1.6 (Steigman 2012)
DV_DI = -81.6                            # D I - H I shift, km/s

C_KMS = 299792.458
GOLD_DARK = "#9c6f00"


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


def dh_bbn(omega_b_h2):
    """Created by JXP and Claude. BBN primordial D/H as a function of
    Omega_b h^2: the Steigman (2012) eta^-1.6 power law, normalized to the
    Cooke et al. (2018) solution (D/H, Omega_b h^2) = (2.527e-5, 0.02166)."""
    return DH_P * (np.asarray(omega_b_h2) / OMB_BBN) ** SLOPE


def voigt_tau(v, tau0, b, gamma_kms=0.02):
    """Created by JXP and Claude. Optical depth of a Voigt profile centred
    at v = 0 (km/s): Doppler width b, tiny Lorentz width so the saturated
    H I line grows damping wings but the D I line stays Gaussian."""
    x = v / b
    a = gamma_kms / b
    return tau0 * np.real(wofz(x + 1j * a))


def draw_spectrum(ax):
    """Created by JXP and Claude. Schematic Lyman-alpha absorption spectrum
    (normalized flux vs velocity) with the H I trough and the D I line."""
    v = np.linspace(-260, 160, 2000)
    tau = voigt_tau(v, 60.0, 14.0) + voigt_tau(v - DV_DI, 1.4, 9.0)
    flux = np.exp(-tau)
    rng = np.random.default_rng(3)
    noise = 0.02 * rng.standard_normal(v.size)       # "data" look
    ax.plot(v, flux + noise, color=STARS, lw=1.3, zorder=3)
    ax.fill_between(v, 0, flux, color=STARS, alpha=0.08, lw=0, zorder=1)
    ax.axhline(1.0, color=GRAY, lw=0.8, ls=":", zorder=2)

    ax.text(0, 0.22, "H", ha="center", va="center", fontsize=20, color=STARS,
            path_effects=bold(STARS, 0.9), zorder=5)
    ax.annotate("D", xy=(DV_DI - 6, 0.62), xytext=(-150, 0.50),
                ha="center", va="center", fontsize=20, color=RED,
                path_effects=bold(RED, 0.9),
                arrowprops=dict(arrowstyle="-", color=RED, lw=1.4,
                                shrinkA=2, shrinkB=2), zorder=5)
    ax.text(-250, 1.12, "quasar light through pristine gas",
            ha="left", va="bottom", fontsize=14, color=MUTED)
    ax.text(152, 0.08, "schematic", ha="right", va="bottom", fontsize=14,
            color=MUTED, style="italic")

    ax.set_xlim(v[0], v[-1])
    ax.set_ylim(0, 1.42)
    ax.set_yticks([0, 1])
    ax.set_xticks([])
    ax.set_ylabel("flux", labelpad=2)
    ax.set_xlabel("wavelength  →", labelpad=1)
    ax.grid(False)


def draw_bbn(ax):
    """Created by JXP and Claude. BBN D/H vs Omega_b h^2 with the measured
    D/H band, the inferred Omega_b h^2 and the Planck CMB value."""
    omb = np.linspace(0.018, 0.027, 300)
    y = dh_bbn(omb) * 1e5
    ax.plot(omb, y, color=STARS, lw=2.6, zorder=3)
    ax.text(0.0183, 1.78, "Big Bang\nprediction", ha="left", va="bottom",
            fontsize=14, color=STARS, linespacing=1.05,
            path_effects=bold(STARS, 0.5))

    # measured D/H band (HIRES) -> drop to the curve -> Omega_b
    lo, hi = (DH_P - DH_ERR) * 1e5, (DH_P + DH_ERR) * 1e5
    ax.axhspan(lo, hi, color=RED, alpha=0.25, lw=0, zorder=2)
    ax.axhline(DH_P * 1e5, color=RED, lw=1.4, zorder=2.5)
    ax.text(0.0268, DH_P * 1e5 - 0.08, "HIRES D/H", ha="right", va="top",
            fontsize=14, color=RED, path_effects=bold(RED, 0.5))
    ax.axvspan(OMB_BBN - OMB_BBN_ERR, OMB_BBN + OMB_BBN_ERR, color=RED,
               alpha=0.25, lw=0, zorder=2)
    ax.annotate("", xy=(OMB_BBN, 1.72), xytext=(OMB_BBN, DH_P * 1e5),
                arrowprops=dict(arrowstyle="-|>,head_length=0.6,head_width=0.3",
                                color=RED, lw=1.6, shrinkA=0, shrinkB=0),
                zorder=4)

    # Planck CMB value for comparison
    ax.axvline(OMB_CMB, color=STARS_GOLD, lw=2.2, ls="--", zorder=2.5)
    ax.text(OMB_CMB + 0.0003, 3.27, "CMB\n(Planck)", ha="left", va="top",
            fontsize=14, color=GOLD_DARK, linespacing=1.0)

    ax.set_xlim(omb[0], omb[-1])
    ax.set_ylim(1.7, 3.3)
    ax.set_xticks([0.020, 0.022, 0.024, 0.026])
    ax.set_yticks([2.0, 2.5, 3.0])
    ax.set_xlabel(r"ordinary matter  $\Omega_b h^2$", labelpad=2)
    ax.set_ylabel(r"D/H  ($\times 10^{-5}$)", labelpad=2)
    ax.grid(False)


def make_figure():
    """Created by JXP and Claude. Build and save the two-panel figure."""
    style.apply_style()
    fig, (ax_top, ax_bot) = plt.subplots(
        2, 1, figsize=style.HALF, gridspec_kw=dict(height_ratios=[1.0, 1.35]))
    draw_spectrum(ax_top)
    draw_bbn(ax_bot)
    src = ("D/H and Ω_b h²: Cooke, Pettini & Steidel 2018, ApJ 855, 102; "
           "BBN scaling ∝ η^-1.6: Steigman 2012; Planck 2018 (A&A 641, A6); "
           "Keck/HIRES D/H: Tytler, Fan & Burles 1996; Burles & Tytler 1998. Spectrum schematic: "
           "J. X. Prochaska & Claude")
    return style.save(fig, FIGS, "dh_omega_b.png", source=src,
                      slide="HIRES: weighing the Universe and finding planets",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
