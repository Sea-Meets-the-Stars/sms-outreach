"""Created by JXP and Claude.

BING 2.0 fits to real PACE spectra with residuals, for the UCSC Statistics
talk (2026), slides "PACE: a colour spectrum per square kilometre" and
"Strong systematics" (Build #7).

The fits are two of the eight *representative* PAB v2 fits chosen by the PAB
report site (``~/Oceanography/python/PAB``, ``claude_prompts/v2/
report_improvements.md``, Edit E5): float 5906450 cycle 140 (the median
sat/float b_bp matchup) and float 5907252 cycle 5 (the most productive
chlorophyll tercile).  Each fit is reconstructed exactly as PAB's own figure
code does it (``pab.plotting.fit_fig.reconstruct_fit``: the chains NPZ, the
``fits`` row for the RT configuration, the pixel geometry, BING's
``robust_hybrid`` forward model) and drawn here with the supplied
per-wavelength uncertainties and the residuals in units of sigma.

Inputs (not in this repository; fetched into a scratch directory):
    the PAB v2 database   https://s3-west.nrp-nautilus.io/pab/v2/pab.db  (public)
    the chain NPZ files   rclone copy AIOcean:PAB/v2/fit_chains/ <data_dir>/fit_chains/ \\
                              --include "5906450_140_*" --include "5907252_5_*" --no-traverse

Run from the repo root (ocean14 env, with PAB and bing importable):
    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/fig_pab_fit.py \\
        --db <scratch>/pab_v2.db --data-dir <scratch>

Outputs: talks/ucsc_stats_2026/figures/pab_fit_{median,productive}.png
(+ sources.json entries).
"""
import argparse
import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

import numpy as np
import matplotlib.pyplot as plt

from sms_outreach.slides import style

OUT_DIR = REPO / "talks" / "ucsc_stats_2026" / "figures"
PAB_CREDIT = ("BING 2.0 fit to a real PACE OCI (L2 AOP V3.2) spectrum at a BGC-Argo float, PAB v2 "
              "representative fit (A. James, J. X. Prochaska et al. 2026, in prep.), reconstructed with "
              "pab.plotting.fit_fig and drawn by J. X. Prochaska & Claude")
FITS = [
    ("pab_fit_median.png", "5906450_140_PACE_OCI.20250829T213217.L2.OC_AOP.V3_2.nc_1210_1019_ExpBPow_v2.0",
     "float 5906450 cycle 140, 29 Aug 2025: the median sat/float b_bp matchup", "PACE"),
    ("pab_fit_productive.png", "5907252_5_PACE_OCI.20260413T173323.L2.OC_AOP.V3_2.nc_573_956_ExpBPow_v2.0",
     "float 5907252 cycle 5, 13 Apr 2026: the most productive tercile (Chl 0.32 mg m⁻³)", "Strong systematics"),
]
SIZE = (5.6, 3.6)          # beside bullets on the slide (height-limited)
N_FREE = 6                 # A_dg, S_dg, A_ph, B_nw, beta, B_p


def draw(wave, obs, sig, med, lo, hi, name, label, slide):
    """Created by JXP and Claude. Residuals (sigma) over R_rs with error bars."""
    resid = (obs - med) / sig
    chi2 = float(np.sum(resid ** 2) / (len(obs) - N_FREE))
    fig, (a0, a1) = plt.subplots(2, 1, figsize=SIZE, sharex=True,
                                 gridspec_kw={"height_ratios": [1, 2.4]})
    a0.axhline(0, color=style.INK, lw=0.8)
    for s in (-2, 2):
        a0.axhline(s, color=style.GRAY, lw=0.8, ls=":")
    a0.plot(wave, resid, ".", color=style.INK, ms=4)
    a0.set_ylabel("resid. (σ)", fontsize=13)
    lim = max(3.0, float(np.nanmax(np.abs(resid))) * 1.1)
    a0.set_ylim(-lim, lim)
    a0.tick_params(labelsize=12)
    a1.fill_between(wave, lo * 1e3, hi * 1e3, color=style.SEA_LIGHT, alpha=0.35, label="5–95%")
    a1.plot(wave, med * 1e3, color=style.SEA, lw=1.6, label="BING fit")
    a1.errorbar(wave, obs * 1e3, yerr=sig * 1e3, fmt=".", color=style.INK, ms=4, lw=0.7, label="PACE")
    a1.set_xlabel("wavelength (nm)")
    a1.set_ylabel("R$_{rs}$(λ)  (10⁻³ sr⁻¹)")
    a1.set_xlim(395, 705)
    a1.legend(fontsize=12, frameon=False, loc="upper right")
    a1.text(0.03, 0.08, f"χ²$_ν$ = {chi2:.2f}", transform=a1.transAxes, fontsize=14)
    print(f"{name}: n={len(obs)} chi2_nu={chi2:.2f} max|resid|={np.nanmax(np.abs(resid)):.1f}")
    style.save(fig, OUT_DIR, name, f"{PAB_CREDIT}: {label}", slide)
    return chi2


def main(argv=None):
    """Created by JXP and Claude. Reconstruct the two fits and draw them."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--db", required=True, help="PAB v2 pab.db (downloaded)")
    ap.add_argument("--data-dir", required=True, help="directory holding fit_chains/<fit_id>.npz")
    args = ap.parse_args(argv)
    os.environ["PAB_DATA_DIR"] = str(Path(args.data_dir).expanduser().resolve())
    from pab.db.store import Store                      # after PAB_DATA_DIR is set
    from pab.fit import artifacts
    from pab.plotting.fit_fig import reconstruct_fit

    style.apply_style()
    store = Store.open(args.db, create=False)
    for name, fit_id, label, slide in FITS:
        wave, obs, med, lo, hi, _, _, _ = reconstruct_fit(store, fit_id)
        npz = artifacts.load_chains(fit_id)
        sig = np.sqrt(np.asarray(npz["varRrs"], dtype=float))
        draw(wave, obs, sig, med, lo, hi, name, label, slide)


if __name__ == "__main__":
    main()
