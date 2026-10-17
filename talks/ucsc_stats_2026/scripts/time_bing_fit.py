"""Created by JXP and Claude.

Time one BING Bayesian fit of a single ocean-colour spectrum, for the slide
"Expensive for one spectrum. Operational?" (UCSC Statistics talk, 2026).

The fit is the one of Prochaska & Frouin (2025, Biogeosciences 22, 4705):
the standard k=5 model (ExpBricaud absorption: A_dg, S_dg, A_ph; Pow
backscattering: B_nw, beta), PACE noise, 400-700 nm (61 PACE bands),
Loisel et al. (2023) Hydrolight spectrum index 170 (the paper's example),
a Levenberg-Marquardt start and then emcee with 75,000 steps after a
1,000-step burn-in, with the walker count BING chooses itself
(max(16, 2 ndim) = 16).

Three stages are timed separately with time.perf_counter():
  prep  -- load the L23 spectrum, resample to PACE bands, build the models,
           priors and the PACE noise vector (bing.fitting.l23.prep_one_l23);
           timed cold (includes reading the L23 netCDF) and warm
  LM    -- scipy curve_fit through bing.fitting.chisq_fit.fit
  emcee -- bing.fitting.inference.fit_one (burn-in + production)

A short pilot run first projects the full emcee time; if that exceeds
~20 min the production run is cut to 7,500 steps and scaled linearly, and
the JSON says so.  The noise realisation and walker ball are seeded, so
the script is re-runnable.  The bing package and the L23 data are read
only; the only file written is

    talks/ucsc_stats_2026/figures/bing_timing.json

Run from the repo root:

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/time_bing_fit.py
"""
import json
import os
import platform
import subprocess
import sys
import time
from pathlib import Path

import numpy as np

OUT = Path(__file__).resolve().parents[1] / "figures" / "bing_timing.json"

L23_INDEX = 170          # the paper's representative (low-Chl) spectrum
NSTEPS = 75_000          # production steps (paper)
NBURN = 1_000            # burn-in steps (bing default)
NSTEPS_SHORT = 7_500     # fallback if the full run would take > MAX_SECONDS
MAX_SECONDS = 20 * 60
PILOT_STEPS, PILOT_BURN = 500, 50
SEED = 12345


def machine_info():
    """Created by JXP and Claude. Describe the machine the timing ran on."""
    info = dict(machine=platform.machine(), processor=platform.processor(),
                cpu_count=os.cpu_count(), system=platform.platform())
    for key, name in [("machdep.cpu.brand_string", "cpu_brand"),
                      ("hw.model", "mac_model")]:
        try:
            info[name] = subprocess.run(
                ["sysctl", "-n", key], capture_output=True, text=True,
                timeout=5, check=True).stdout.strip()
        except Exception:                      # not a Mac, or no sysctl
            info[name] = None
    return info


def versions():
    """Created by JXP and Claude. Record the software versions used."""
    import emcee
    import scipy
    import bing
    return dict(python=platform.python_version(), numpy=np.__version__,
                scipy=scipy.__version__, emcee=emcee.__version__,
                bing_path=str(Path(bing.__file__).resolve().parent))


def lm_bounds(p):
    """Created by JXP and Claude. Prior bounds for curve_fit, as in
    bing.fitting.l23.fit_with_LM (Gordon backend, fixed B_p)."""
    lo = [d["pmin"] for d in p.apriors] + [d["pmin"] for d in p.bpriors]
    hi = [d["pmax"] for d in p.apriors] + [d["pmax"] for d in p.bpriors]
    return np.array(lo, float), np.array(hi, float)


def run_emcee_stage(prep, rt_dict, p0, idx, nsteps, nburn):
    """Created by JXP and Claude. Time one emcee run on prepared data;
    returns (seconds, sampler)."""
    from bing.fitting import inference as bing_inf
    pdict = dict(prep["pdict"])
    pdict["nsteps"], pdict["nburn"] = nsteps, nburn
    # Single-spectrum hack mirrored from bing.fitting.l23.fit_one: the
    # Chl / Y arrays are looked up by spectrum index.
    pdict["Chl"] = np.zeros(idx + 1)
    pdict["Chl"][idx] = prep["odict"]["Chl"]
    pdict["Y"] = np.zeros(idx + 1)
    pdict["Y"][idx] = prep["odict"]["Y"]
    item = (prep["model_Rrs"], prep["model_varRrs"], p0, idx, prep["geom"])
    t0 = time.perf_counter()
    sampler, _ = bing_inf.fit_one(item, models=prep["models"], pdict=pdict,
                                  chains_only=False, rt_dict=rt_dict)
    return time.perf_counter() - t0, sampler


def main():
    """Created by JXP and Claude. Time prep, LM and emcee for one L23
    spectrum and write bing_timing.json."""
    from bing.parameters import standard
    from bing.fitting import l23, chisq_fit
    from bing.rt import defs as rt_defs

    np.random.seed(SEED)
    p = standard.expb_pow(scl_noise="PACE", add_noise=True,
                          nsteps=NSTEPS, nburn=NBURN)
    idx = L23_INDEX

    # --- Stage 1: data prep (cold = includes reading the L23 netCDF) ----
    t0 = time.perf_counter()
    prep = l23.prep_one_l23(p, idx)
    t_prep_cold = time.perf_counter() - t0
    np.random.seed(SEED)                       # same noise realisation
    t0 = time.perf_counter()
    prep = l23.prep_one_l23(p, idx)
    t_prep_warm = time.perf_counter() - t0
    models = prep["models"]
    rt_dict = rt_defs.rt_dict_from_p(p)
    nwave = int(models[0].wave.size)
    ndim = int(prep["pdict"]["ndim"])
    nwalkers = int(prep["pdict"]["nwalkers"])

    # --- Stage 2: Levenberg-Marquardt (scipy curve_fit) -----------------
    lo, hi = lm_bounds(p)
    item = (prep["model_Rrs"], prep["model_varRrs"], prep["p0"], idx,
            prep["geom"])
    t0 = time.perf_counter()
    ans, cov, _ = chisq_fit.fit(item, models, rt_dict, bounds=(lo, hi))
    t_lm = time.perf_counter() - t0
    # Start the walkers at the LM solution, nudged off any prior bound so
    # the walker ball is strictly inside the priors.
    p0 = np.clip(ans, lo + 0.01 * (hi - lo), hi - 0.01 * (hi - lo))

    # --- Stage 3: emcee --------------------------------------------------
    np.random.seed(SEED)
    t_pilot, _ = run_emcee_stage(prep, rt_dict, p0, idx, PILOT_STEPS,
                                 PILOT_BURN)
    projected = t_pilot / (PILOT_STEPS + PILOT_BURN) * (NSTEPS + NBURN)
    scaled = projected > MAX_SECONDS
    nsteps_run = NSTEPS_SHORT if scaled else NSTEPS
    print(f"pilot: {t_pilot:.2f} s for {PILOT_STEPS + PILOT_BURN} steps "
          f"-> projected {projected:.0f} s for {NSTEPS + NBURN}; "
          f"running {nsteps_run} steps")
    np.random.seed(SEED)
    t_run, sampler = run_emcee_stage(prep, rt_dict, p0, idx, nsteps_run,
                                     NBURN)
    scale = (NSTEPS + NBURN) / (nsteps_run + NBURN)
    t_emcee = t_run * scale
    chain = sampler.get_chain()
    median = np.median(chain.reshape(-1, chain.shape[-1]), axis=0)
    n_eval = nwalkers * (NSTEPS + NBURN)
    t_total = t_prep_warm + t_lm + t_emcee

    out = dict(
        description=("Wall-clock time of one BING fit (Prochaska & Frouin "
                     "2025) of one PACE-like spectrum on this machine"),
        spectrum=dict(dataset="Loisel et al. 2023 Hydrolight (ds 4, 0)",
                      index=idx, Chl_mg_m3=float(prep["odict"]["Chl"]),
                      wv_min_nm=p.wv_min, wv_max_nm=p.wv_max,
                      n_bands=nwave, satellite=p.satellite,
                      noise="PACE Level-2 median uncertainty table "
                            "(ocpy PACE_error.csv), noise added, seed "
                            f"{SEED}"),
        model=dict(names=list(p.model_names),
                   parameters=list(models[0].pnames) + list(models[1].pnames),
                   ndim=ndim, rt_backend=rt_dict.get("rt_backend", "gordon"),
                   variable_Gordon=p.variable_Gordon),
        mcmc=dict(sampler="emcee EnsembleSampler (default stretch move, "
                          "serial, no pool)",
                  nwalkers=nwalkers, nwalkers_rule="max(16, 2*ndim)",
                  nsteps=NSTEPS, nburn=NBURN, nsteps_run=nsteps_run,
                  scaled_from_shorter_run=bool(scaled),
                  scale_factor=float(scale),
                  n_likelihood_evaluations=int(n_eval),
                  mean_acceptance_fraction=float(
                      np.mean(sampler.acceptance_fraction))),
        seconds=dict(prep_cold_incl_L23_load=t_prep_cold,
                     prep=t_prep_warm, lm=t_lm,
                     emcee_measured=t_run, emcee=t_emcee,
                     emcee_pilot=t_pilot,
                     per_likelihood_evaluation_us=1e6 * t_emcee / n_eval,
                     per_spectrum=t_total),
        fit=dict(lm_params=[float(x) for x in ans],
                 posterior_median=[float(x) for x in median],
                 emcee_start="LM solution, clipped 1% inside prior bounds"),
        machine=machine_info(), versions=versions(),
        assumptions=[
            "Timing is single-core wall clock (time.perf_counter); emcee "
            "runs serially, log_prob is pure numpy (not jitted).",
            "per_spectrum = prep (warm) + lm + emcee; cold prep includes "
            "reading the L23 netCDF once and is excluded.",
            "emcee seconds are for nburn + nsteps steps; if "
            "scaled_from_shorter_run is true they are a linear extrapolation "
            "from nsteps_run production steps.",
            "Walkers start at the Levenberg-Marquardt solution as in the "
            "paper's LM-then-MCMC workflow.",
        ],
        script=str(Path(__file__).resolve().relative_to(
            Path(__file__).resolve().parents[3])),
        timestamp=time.strftime("%Y-%m-%d %H:%M:%S"),
    )
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=2) + "\n")
    print(f"prep {t_prep_warm:.3f} s (cold {t_prep_cold:.2f} s), "
          f"LM {t_lm:.4f} s, emcee {t_emcee:.1f} s "
          f"({nwalkers} walkers x {NSTEPS + NBURN} steps) -> "
          f"{t_total:.1f} s per spectrum")
    print(f"wrote {OUT}")
    return out


if __name__ == "__main__":
    main()
