"""Created by JXP and Claude.

Pigment-specific absorption spectra for the UCSC Statistics talk (2026),
slide "Biology makes almost any a(λ) possible" (Build #7).

Data: in vivo pigment-specific absorption coefficients a*(λ) (m² mg⁻¹) from
Bricaud, Claustre, Ras & Oubelkheir (2004, JGR 109, C11010), as packaged in
``ocpy`` (``ocpy/data/phytoplankton/Bricaud_2004.csv``).  Seven pigments are
drawn in a fixed order with the sea/stars palette; a legend names them.

Run from the repo root (ocean14 env):
    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_pigments.py

Output: talks/ucsc_stats_2026/figures/pigment_absorption.png (+ sources.json entry).
"""
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import matplotlib.pyplot as plt
from ocpy.ph import load_data as load_ph

from sms_outreach.slides import style

OUT_DIR = REPO / "talks" / "ucsc_stats_2026" / "figures"
SOURCE = ("Pigment-specific absorption spectra from Bricaud et al. 2004, JGR 109, C11010 "
          "(via ocpy); drawn by J. X. Prochaska & Claude")
SIZE = (6.1, 3.5)                       # beside bullets on the slide

# (column in Bricaud_2004.csv, label, colour) in a fixed order
PIGMENTS = [
    ("Chl-a", "Chlorophyll a", style.SEA),
    ("Chl-b", "Chlorophyll b", style.TEAL),
    ("Chl-c12", "Chlorophyll c₁+c₂", style.SEA_LIGHT),
    ("FUCO", "Fucoxanthin", style.STARS_GOLD),
    ("Peri", "Peridinin", style.RED),
    ("19'-HF", "19′-Hexanoyloxyfucoxanthin", style.STARS),
    ("Zea", "Zeaxanthin", style.GRAY),
]


def main():
    """Created by JXP and Claude. Draw and save the figure."""
    style.apply_style()
    df = load_ph.bricaud()
    sel = (df["wave"] >= 400) & (df["wave"] <= 700)
    fig, ax = plt.subplots(figsize=SIZE)
    for col, label, color in PIGMENTS:
        ax.plot(df.loc[sel, "wave"], df.loc[sel, col], color=color, lw=2, label=label)
    ax.set_xlabel("wavelength (nm)")
    ax.set_ylabel("a*(λ)  (m² mg⁻¹)")
    ax.set_xlim(400, 700)
    ax.set_ylim(0, 0.085)                 # room for the legend above the red Chl-a peak
    ax.legend(fontsize=11, ncol=1, frameon=False, loc="upper right", handlelength=1.6)
    style.save(fig, OUT_DIR, "pigment_absorption.png", SOURCE,
               "Biology makes almost any a(λ) possible")


if __name__ == "__main__":
    main()
