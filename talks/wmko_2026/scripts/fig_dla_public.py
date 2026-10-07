"""Created by JXP and Claude.

Figure for the slide "My HIRES work: damped Lyα systems"
(WMKO 2026 public lecture, Sea meets the stars).

Two panels for a lay audience:

  left  -- an ILLUSTRATIVE quasar spectrum: a power-law continuum with a
           Lyα emission line, a mock Lyα forest, and one damped Lyα
           absorber (Voigt profile, N(HI) = 10^20.5 cm^-2) that carves a
           deep, wide trough out of the quasar's light.  Labelled
           "illustration"; no real data.
  right -- published DLA metallicities from Rafelski et al. 2012
           (ApJ 755, 89; VizieR J/ApJ/755/89, tables 2 + 3: [M/H] vs z)
           plotted against the age of the Universe (Planck 2018
           cosmology), with binned means.  The y axis is the metal
           fraction relative to the Sun on a log scale (1/1000 ... Sun).

The catalogue is fetched from VizieR on first run and cached under
scripts/data/ (rafelski2012_table{2,3}.tsv); later runs read the cache.

Run from the repo root (conda run does not pass stdin; the script writes
the PNG and updates figures/sources.json, or $SOURCES_JSON if set):

    conda run -n ocean14 python talks/wmko_2026/scripts/fig_dla_public.py

Output: talks/wmko_2026/figures/dla_public.png
"""
import os
import sys
import urllib.request
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
from scipy.special import wofz
from astropy.cosmology import Planck18
from astropy.io import ascii

from sms_outreach.slides import style
from sms_outreach.slides.style import (SEA, STARS, STARS_GOLD, RED, GRAY,
                                       INK, MUTED)

FIGS = Path(__file__).resolve().parents[1] / "figures"
DATA = Path(__file__).resolve().parent / "data"

VIZIER = "https://vizier.cds.unistra.fr/viz-bin/asu-tsv"
CATALOG = "J/ApJ/755/89"
COLS = "QSO,z,NHI,e_NHI,%5BM/H%5D,e_%5BM/H%5D,f_%5BM/H%5D"
SOURCE = ("Rafelski et al. 2012, ApJ 755, 89 (VizieR J/ApJ/755/89; 242 DLAs, "
          "mostly Keck/HIRES + ESI); left panel is an illustration")
GOLD_DARK = "#9c6f00"

# Lyα atomic data (Morton 2003)
LYA_A, LYA_F, LYA_GAMMA = 1215.6701, 0.4164, 6.265e8
C_KMS = 299792.458


def bold(color, lw=1.0):
    """Created by JXP and Claude. Faux-bold path effect: the bundled Roboto
    is a variable font and matplotlib cannot select its bold instance."""
    return [withStroke(linewidth=lw, foreground=color)]


# ----------------------------------------------------------------------
# data
# ----------------------------------------------------------------------
def fetch_table(table):
    """Created by JXP and Claude. Return the cached VizieR TSV path for
    `table` ('table2' or 'table3'), downloading it if absent."""
    DATA.mkdir(parents=True, exist_ok=True)
    path = DATA / f"rafelski2012_{table}.tsv"
    if not path.exists():
        url = (f"{VIZIER}?-source={CATALOG}/{table}&-out.max=unlimited"
               f"&-out={COLS}")
        print(f"fetching {url}")
        urllib.request.urlretrieve(url, path)
    return path


def load_dlas():
    """Created by JXP and Claude. Read Rafelski+2012 tables 2 (new) and 3
    (literature) and return arrays (z, [M/H], e_[M/H]) for every DLA with
    a metallicity.  VizieR TSV: '#' comments, a header line, a units line
    and a dashed line before the data."""
    zs, mh, emh = [], [], []
    for table in ("table2", "table3"):
        lines = [ln for ln in fetch_table(table).read_text().splitlines()
                 if ln and not ln.startswith("#")]
        header = lines[0].split("\t")
        for ln in lines[3:]:                      # skip header, units, dashes
            row = dict(zip(header, (c.strip() for c in ln.split("\t"))))
            if row["[M/H]"] == "":
                continue
            zs.append(float(row["z"]))
            mh.append(float(row["[M/H]"]))
            emh.append(float(row["e_[M/H]"]) if row["e_[M/H]"] else np.nan)
    return np.array(zs), np.array(mh), np.array(emh)


def age_gyr(z):
    """Created by JXP and Claude. Age of the Universe at redshift z (Gyr),
    Planck 2018 cosmology."""
    return Planck18.age(z).value


# ----------------------------------------------------------------------
# illustrative spectrum
# ----------------------------------------------------------------------
def tau_lya(wave, z, logn, b=20.0):
    """Created by JXP and Claude. Lyα optical depth of one absorber at
    redshift z with column density 10^logn cm^-2 and Doppler b (km/s);
    `wave` is observed wavelength (Å).  Voigt profile via the Faddeeva
    function (scipy.special.wofz)."""
    lam0 = LYA_A * (1 + z)                        # observed line centre
    x = (wave - lam0) / lam0 * C_KMS / b          # Doppler units
    a = LYA_GAMMA * LYA_A * 1e-8 / (4 * np.pi * b * 1e5)
    tau0 = 1.497e-2 * LYA_F * (LYA_A * 1e-8) * 10.0 ** logn / (b * 1e5)
    return tau0 * wofz(x + 1j * a).real


def mock_spectrum(z_qso=3.2, z_dla=2.9, logn_dla=20.5, seed=7):
    """Created by JXP and Claude. Mock quasar spectrum (observed Å, flux
    in arbitrary units) with a power-law continuum, a broad Lyα emission
    line, a random Lyα forest blueward of it, and one DLA."""
    rng = np.random.default_rng(seed)
    wave = np.linspace(4560.0, 5260.0, 4000)
    lam_em = LYA_A * (1 + z_qso)
    cont = (wave / lam_em) ** -1.5
    flux = cont * (1 + 1.4 * np.exp(-0.5 * ((wave - lam_em) / 28.0) ** 2)
                   + 0.5 * np.exp(-0.5 * ((wave - lam_em - 38.0) / 12.0) ** 2))
    # Lyα forest: random clouds between z = 2.5 and the quasar
    tau = np.zeros_like(wave)
    n_lines = 95
    for _ in range(n_lines):
        z = rng.uniform(wave[0] / LYA_A - 1, z_qso - 0.01)
        logn = 12.3 + rng.power(0.6) * 2.1       # 10^12.3 .. 10^14.4
        tau += tau_lya(wave, z, logn, b=rng.uniform(18, 35))
    tau_dla = tau_lya(wave, z_dla, logn_dla, b=25.0)
    flux *= np.exp(-(tau + tau_dla))
    flux += rng.normal(0, 0.025, wave.size)      # a little noise
    return wave, flux, lam_em, LYA_A * (1 + z_dla), tau_dla


def draw_spectrum(ax):
    """Created by JXP and Claude. Left panel: the illustrative spectrum
    with the DLA trough highlighted."""
    wave, flux, lam_em, lam_dla, tau_dla = mock_spectrum()
    ax.plot(wave, flux, color=STARS, lw=0.7, zorder=3)
    ax.fill_between(wave, 0, flux, color=STARS, alpha=0.12, lw=0, zorder=2)
    # gold band marking the trough (where the DLA alone absorbs > 25%)
    trough = wave[tau_dla > -np.log(0.75)]
    ax.axvspan(trough[0], trough[-1], color=STARS_GOLD, alpha=0.25, lw=0,
               zorder=1)
    ax.set_xlim(wave[0], wave[-1])
    ax.set_ylim(0, 2.95)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_xticks([], minor=True)
    ax.grid(False)
    ax.set_xlabel("wavelength (colour of light)", fontsize=14)
    ax.set_ylabel("brightness", fontsize=14)
    ax.text(lam_em, 2.72, "quasar", ha="center", va="bottom", fontsize=16,
            color=STARS, path_effects=bold(STARS, 0.6))
    ax.annotate("gas cloud\n(DLA)", (lam_dla, 0.1), (lam_dla + 20, 1.9),
                ha="center", va="bottom", fontsize=16, color=GOLD_DARK,
                path_effects=bold(GOLD_DARK, 0.6),
                arrowprops=dict(arrowstyle="-|>", color=GOLD_DARK, lw=1.6,
                                shrinkB=2), zorder=5)
    ax.text(0.02, 0.97, "illustration", transform=ax.transAxes, ha="left",
            va="top", fontsize=14, color=MUTED, style="italic")


# ----------------------------------------------------------------------
# metallicity panel
# ----------------------------------------------------------------------
def draw_metallicity(ax):
    """Created by JXP and Claude. Right panel: DLA metal fraction (vs. the
    Sun) against the age of the Universe, with binned means."""
    z, mh, _ = load_dlas()
    age = age_gyr(z)
    frac = 10.0 ** mh
    ax.scatter(age, frac, s=22, color=STARS_GOLD, edgecolor=GOLD_DARK,
               lw=0.4, alpha=0.85, zorder=3, label=f"{len(z)} clouds")

    # binned means in redshift (mean of log metallicity)
    edges = np.array([0.0, 0.7, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 5.5])
    xb, yb, eb = [], [], []
    for lo, hi in zip(edges[:-1], edges[1:]):
        sel = (z >= lo) & (z < hi)
        if sel.sum() < 3:
            continue
        xb.append(age[sel].mean())
        yb.append(mh[sel].mean())
        eb.append(mh[sel].std(ddof=1) / np.sqrt(sel.sum()))
    xb, yb, eb = map(np.array, (xb, yb, eb))
    ax.plot(xb, 10.0 ** yb, color=STARS, lw=2.6, zorder=4, label="average")
    ax.errorbar(xb, 10.0 ** yb, yerr=[10.0 ** yb - 10.0 ** (yb - eb),
                                      10.0 ** (yb + eb) - 10.0 ** yb],
                fmt="s", ms=7, color=STARS, mec="white", mew=0.8, lw=1.6,
                capsize=3, zorder=5)

    # Sun reference
    ax.axhline(1.0, color=RED, lw=1.4, ls=(0, (4, 3)), zorder=2)
    ax.text(13.6, 1.0, "the Sun", ha="right", va="bottom", fontsize=15,
            color=RED)

    ax.set_yscale("log")
    ax.set_ylim(10 ** -3.3, 10 ** 0.45)
    ax.set_yticks([1e-3, 1e-2, 1e-1, 1.0])
    ax.set_yticklabels(["1/1000", "1/100", "1/10", "1"])
    ax.yaxis.set_minor_locator(plt.NullLocator())
    ax.set_ylabel("metals (vs. the Sun)")
    ax.set_xlim(0.0, 13.9)
    ax.set_xlabel("age of the Universe (billion years)")

    # redshift marks along the top edge (twin/secondary axes break
    # tight_layout, so draw them by hand)
    tr = ax.get_xaxis_transform()            # x in data, y in axes coords
    for zv in (4, 2, 1, 0.5):
        a = age_gyr(zv)
        ax.plot([a, a], [0.97, 1.0], color=MUTED, lw=1.0, transform=tr,
                clip_on=False)
        ax.text(a, 0.955, f"z = {zv:g}" if zv == 4 else f"{zv:g}",
                ha="center", va="top", fontsize=14, color=MUTED, transform=tr)
    ax.text(13.8, 10 ** -3.15, "today", ha="right", va="bottom", fontsize=14,
            color=MUTED)

    ax.legend(loc="lower center", bbox_to_anchor=(0.6, 0.0), frameon=False,
              fontsize=14, handletextpad=0.4, borderaxespad=0.2,
              markerscale=1.3)
    return len(z)


def make_figure():
    """Created by JXP and Claude. Build and save the figure."""
    style.apply_style()
    # no wspace in gridspec_kw: explicit spacing disables tight_layout
    fig, (axl, axr) = plt.subplots(1, 2, figsize=style.FULL,
                                   gridspec_kw=dict(width_ratios=[1.0, 1.55]))
    draw_spectrum(axl)
    n = draw_metallicity(axr)
    print(f"{n} DLAs with [M/H]")
    return style.save(fig, FIGS, "dla_public.png", source=SOURCE,
                      slide="My HIRES work: damped Lyα systems",
                      sources_json=os.environ.get("SOURCES_JSON"))


if __name__ == "__main__":
    make_figure()
