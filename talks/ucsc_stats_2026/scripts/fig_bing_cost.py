"""Created by JXP and Claude.

Figure for the slide "Expensive for one spectrum. Operational?"
(sub-line "Seconds per spectrum x 10^8 spectra a day") of the UCSC
Statistics talk, 2026.

Left  -- the measured wall-clock cost of one BING fit (Prochaska & Frouin
         2025) on this machine, from bing_timing.json written by
         time_bing_fit.py: data prep, the Levenberg-Marquardt start and
         the emcee run, as horizontal bars on a log axis (LM is ~1000x
         cheaper than the MCMC, which is the point of showing all three).
Right -- what that implies for PACE at scale: ~1e8 cloud-free ocean
         spectra per day times the seconds per spectrum, expressed as
         CPU-years per day and the number of cores needed to keep up.

Assumptions (printed on the figure): global ocean 3.6e8 km^2, ~1.2 km
pixels, 2-day repeat, about half cloud-free -> ~1e8 spectra/day.

Run from the repo root, after time_bing_fit.py:

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_bing_cost.py

Output: talks/ucsc_stats_2026/figures/bing_cost.png (FULL, 9.2 x 3.4 in)
"""
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:          # so `sms_outreach` imports uninstalled
    sys.path.insert(0, str(REPO))

import matplotlib.pyplot as plt
import numpy as np

from sms_outreach.slides import style
from sms_outreach.slides.style import SEA, STARS_GOLD, RED, MUTED, INK

FIGS = Path(__file__).resolve().parents[1] / "figures"
TIMING = FIGS / "bing_timing.json"
NAME = "bing_cost.png"
MANIFEST = FIGS / "sources.json"
SOURCE = ("Timing of one BING fit (time_bing_fit.py) on this machine; PACE "
          "count assumed ~1e8 cloud-free ocean spectra/day; "
          "J. X. Prochaska & Claude")
SLIDE = "Expensive for one spectrum. Operational?"

# PACE daily spectrum count and the assumptions behind it
OCEAN_KM2 = 3.6e8
PIXEL_KM = 1.2
REPEAT_DAYS = 2.0
CLOUD_FREE = 0.5
N_SPECTRA_DAY = 1e8          # rounded from the assumptions above (~0.6e8)
SEC_PER_DAY = 86400.0
SEC_PER_YEAR = 365.25 * SEC_PER_DAY


def daily_cost(sec_per_spectrum, n_spectra=N_SPECTRA_DAY):
    """Created by JXP and Claude. CPU-seconds, CPU-years and cores needed
    per day for n_spectra spectra at sec_per_spectrum each."""
    cpu_s = sec_per_spectrum * n_spectra
    return dict(cpu_seconds=cpu_s, cpu_years=cpu_s / SEC_PER_YEAR,
                cores=cpu_s / SEC_PER_DAY)


def fmt_seconds(s):
    """Created by JXP and Claude. Short label for a duration in seconds."""
    if s < 0.1:
        return f"{1e3 * s:.0f} ms"
    if s < 10:
        return f"{s:.1f} s"
    return f"{s:.0f} s"


def main():
    """Created by JXP and Claude. Read bing_timing.json and draw
    bing_cost.png."""
    t = json.loads(TIMING.read_text())
    sec = t["seconds"]
    mc = t["mcmc"]
    stages = [("prep", sec["prep"], MUTED),
              ("LM start", sec["lm"], SEA),
              ("emcee", sec["emcee"], RED)]
    per_spec = sec["per_spectrum"]
    cost = daily_cost(per_spec)
    machine = t["machine"].get("cpu_brand") or t["machine"]["processor"]
    scaled = " (scaled from a shorter run)" if mc.get(
        "scaled_from_shorter_run") else ""
    ksteps = (mc["nsteps"] + mc["nburn"]) / 1000.

    style.apply_style()
    fig, (ax, axr) = plt.subplots(
        1, 2, figsize=style.FULL,
        gridspec_kw=dict(width_ratios=[0.9, 1.1]))

    # ---- left: one spectrum, stage by stage (log seconds) --------------
    y = np.arange(len(stages))[::-1]
    floor = 1e-3                                   # log-axis bar origin
    for yi, (label, s, col) in zip(y, stages):
        ax.barh(yi, s - floor, left=floor, color=col, height=0.62, zorder=3)
        ax.text(s * 1.3, yi, fmt_seconds(s), va="center", ha="left",
                fontsize=15, color=col)
    ax.text(np.sqrt(floor * sec["emcee"]), y[-1],
            f"{mc['nwalkers']} walkers x {ksteps:.0f}k steps",
            va="center", ha="center", fontsize=12, color="white", zorder=4)
    ax.set_xscale("log")
    ax.set_xlim(floor, 3e2)
    ax.set_xticks([1e-3, 1e-2, 1e-1, 1, 10, 100])
    ax.set_xticklabels(["1 ms", "0.01", "0.1", "1", "10", "100"])
    ax.set_yticks(y)
    ax.set_yticklabels([s[0] for s in stages], fontsize=14)
    ax.set_ylim(-0.6, len(stages) - 0.4)
    ax.set_xlabel("seconds for ONE spectrum (1 core)", fontsize=13)
    ax.grid(True, axis="x", alpha=0.25)
    ax.grid(False, axis="y")
    ax.tick_params(axis="x", labelsize=12)
    ax.text(0.98, 0.97, f"total  {per_spec:.0f} s", transform=ax.transAxes,
            ha="right", va="top", fontsize=15, color=INK)

    # ---- right: PACE at scale --------------------------------------------
    axr.set_axis_off()
    big = 21
    kw = dict(va="top", transform=axr.transAxes)
    axr.text(0.0, 1.0, "PACE, every day:", fontsize=15, color=INK, **kw)
    axr.text(0.0, 0.86, r"$10^8$ spectra  $\times$  " + f"{per_spec:.0f} s",
             fontsize=15, color=INK, **kw)
    axr.text(0.0, 0.67, f"$\\approx$ {cost['cpu_years']:.0f} CPU-years per day",
             fontsize=big, color=RED, **kw)
    axr.text(0.0, 0.48, f"$\\approx$ {round(cost['cores'], -3):,.0f} cores"
             " to keep up", fontsize=big, color=STARS_GOLD, **kw)
    mant, expo = f"{cost['cpu_seconds']:.1e}".split("e+")
    axr.text(0.0, 0.33, f"({mant}" + r"$\times10^{" + f"{int(expo)}" +
             r"}$ CPU-seconds a day)", fontsize=12, color=MUTED, **kw)

    # ---- assumptions, small, under the numbers -----------------------------
    note = (r"Assumes ~$10^8$ cloud-free ocean spectra/day: global ocean "
            r"$3.6\times10^8$ km$^2$," + "\n"
            f"{PIXEL_KM} km pixels, {REPEAT_DAYS:.0f}-day repeat, "
            f"~{CLOUD_FREE:.0%} cloud-free.\n"
            f"One fit timed on {machine}{scaled}: k=5 model, PACE noise, "
            f"400-700 nm,\nLoisel+23 spectrum {t['spectrum']['index']}; "
            f"{mc['nwalkers']} walkers x {mc['nsteps']:,} steps "
            f"+ {mc['nburn']:,} burn-in.")
    axr.text(0.0, 0.0, note, fontsize=8.5, color=MUTED, ha="left",
             va="bottom", linespacing=1.3, transform=axr.transAxes)

    style.save(fig, FIGS, NAME, SOURCE, SLIDE, sources_json=MANIFEST)


if __name__ == "__main__":
    main()
