"""Created by JXP and Claude.

Slide plan for "Sea Meets the Stars" — UCSC Statistics department seminar,
Monday 19 Oct 2026 (45 min of slides + 15 min of discussion in three slots).
Source of truth for slide order, titles, sub-lines, figures, credits and
speaker notes; follows Q&A/Talk Q1–Q43 and the Q26 plan in
claude_prompts/stats_ucsc_2026.md.

Build (ocean14 env, from the repo root):
    python -m sms_outreach.slides.build talks/ucsc_stats_2026/slides/plan.py --png

Figure files are looked up in FIG_DIRS; a file that does not exist yet is
drawn as a red PLACEHOLDER box (B2 harvests, B3 draws).  Credits go into the
speaker notes, not onto the slides (CREDITS_IN_NOTES, Q5).  Pairs are sea on
the LEFT, stars on the RIGHT where that applies.
"""
from pathlib import Path

from sms_outreach.slides.spec import DIVIDER, TITLE, Fig, Slide

HERE = Path(__file__).resolve().parent
TALK = HERE.parent
TEMPLATE = Path("~/Projects/ClimateIntelligence/presentations/2026_WMKO/Kraw_2024.pptx").expanduser()
FIG_DIRS = [TALK / "figures", TALK.parent / "wmko_2026" / "figures"]
OUTPUT = HERE / "UCSC_Stats_2026.pptx"
MAX_SLIDES = 42
CREDITS_IN_NOTES = True

S_INTRO, S_FRB, S_BING, S_OTHER, S_CLOSE, S_BACKUP = "Intro", "FRBs", "BING", "Other", "Close", "Backup"

NU = "NU_2026_talk.pptx (J. X. Prochaska, 2026)"
AWOC = "AWOC_2025.pptx (J. X. Prochaska, 2025)"
HOFF = "Hoffmann, James, Prochaska et al. 2026, arXiv:2609.27282"
BING = "Prochaska & Frouin 2025, Biogeosciences 22, 4705"
KRAMER = "Kramer, Siegel, Maritorena & Catlett 2022, RSE 270, 112879 (CC BY)"
ROMS = "UCSC Ocean Modeling and Data Assimilation group (C. Edwards, A. Moore), oceanmodeling.ucsc.edu, CC BY 3.0"
CLAUDE = "J. X. Prochaska & Claude"

SLIDES = [
    # ------------------------------------------------------------- intro
    Slide("Sea Meets the Stars", kind=TITLE, section=S_INTRO,
          subtitle="Advancing science on the frontier with modern statistical techniques",
          author="UC Santa Cruz, Kavli IPMU, NAOJ, Simons Pivot Fellow",
          notes="Thank Yunyi Shen for the invitation. The README went out ahead of time; this talk follows it: "
                "two Bayesian problems, one in astrophysics and one in ocean science, and a request for better "
                "methods. Three discussion slots; interrupt at any time."),
    Slide("A physicist's toolkit", section=S_INTRO,
          subtitle="KS tests, χ², likelihoods: the 1990s",
          figures=[Fig("bg_physics.png", placeholder="YOUR FIGURE: KS test / χ² / likelihood (PhD years)")],
          bullets=["PhD in physics: Kolmogorov–Smirnov tests and χ² fits",
                   "Maximum likelihood when χ² was not enough",
                   "Frequentist by training, Bayesian by necessity"],
          notes="Three slides on where my statistics come from. As a physics PhD student the tools were KS "
                "tests, chi-squared fits and, when those failed, a likelihood. (Figure to be dropped in by JXP.)"),
    Slide("An astronomer's toolkit", section=S_INTRO,
          subtitle="Likelihoods, Bayesian modeling, Hamiltonian Monte Carlo, Gaussian processes",
          figures=[Fig("bg_astronomy.png", placeholder="YOUR FIGURE: Bayesian / HMC / GP (astronomy years)")],
          bullets=["Likelihood analyses of quasar absorption lines",
                   "Bayesian population models sampled by MCMC, then HMC",
                   "Gaussian processes for spectra and light curves"],
          notes="As an astronomer: likelihood analyses of absorption-line surveys, then full Bayesian population "
                "models sampled with MCMC and Hamiltonian Monte Carlo, and Gaussian processes. (Figure by JXP.)"),
    Slide("An oceanographer's toolkit", section=S_INTRO,
          subtitle="Deep learning, and Bayes again",
          figures=[Fig("bg_ocean.png", placeholder="YOUR FIGURE: deep learning + Bayesian (ocean years)")],
          bullets=["Deep learning on satellite imagery (Ulmo, Nenya, Enki)",
                   "Bayesian inversion of ocean-colour spectra (BING)",
                   "The same questions in a new ocean: speed, priors, evidence"],
          notes="As an oceanographer since 2020: deep learning on satellite imagery, and then Bayesian inversion "
                "of ocean-colour spectra, which brought back the same questions. (Figure by JXP.)"),
    Slide("Goals for today", section=S_INTRO,
          subtitle="Two problems, one request",
          bullets=["Two problems, one shape: forward model, likelihood, MCMC",
                   "What we have: public data, public code, a working but slow method",
                   "What we want: faster, less prior-dependent, an honest evidence",
                   "Three discussion slots; two more problems at the end; details in the README"],
          notes="Both problems have the same shape: a physical forward model, a likelihood, MCMC. Both work and "
                "both are too slow or too prior-dependent. I will stop three times for discussion. The README "
                "has the equations and the links to the code (github.com/FRBs/zdm, github.com/ocean-colour/bing)."),
    # ------------------------------------------------------------- FRBs
    Slide("Part I: Fast radio bursts", kind=DIVIDER, section=S_FRB,
          notes="Part I. Fast radio bursts: millisecond flashes of radio waves from distant galaxies."),
    Slide("A multi-pronged attack on unsolved problems", section=S_FRB,
          subtitle="The sources, the baryons, and H0 (the normalization) from one population model",
          figures=[Fig("nu_lorimer_burst.png", caption="The sources: rates, energies, repetition"),
                   Fig("nu_macquart_2026.png", caption="The baryons: DM vs. z counts every electron")],
          source=f"Left: Lorimer et al. 2007, Science 318, 777, via {NU}; right: localized FRBs to 2026, compiled by J. X. Prochaska, via {NU}",
          notes="A fast radio burst is a millisecond flash of radio waves from a distant galaxy. Left: the first "
                "one (Lorimer et al. 2007); the sweep is dispersion, a delay proportional to the electron column "
                "times frequency to the minus two. Right: the Macquart relation in 2026, dispersion measure "
                "against redshift for about 100 localized bursts. Three questions ride on one population model: "
                "what the sources are (rates, energies, repetition), how many baryons sit in the cosmic web (the "
                "slope), and the expansion rate H0 (the normalization, which scales as 1/H0 at fixed Ω_b h²)."),
    Slide("It starts with a radio telescope", section=S_FRB,
          subtitle="Six telescopes, six beams, six thresholds",
          figures=[Fig("telescopes_montage.png", caption="MeerKAT, CHIME, ASKAP, Parkes"),
                   Fig("nu_nfrb_vs_year.png", caption="Bursts per year: all, and localized")],
          source=f"Telescope photos (SARAO, CHIME collaboration, CSIRO; owners to confirm) and the discovery curve compiled by J. X. Prochaska, via {NU}",
          notes="The data come from six telescopes with different beams, bandwidths and detection thresholds: "
                "CHIME (492 bursts in the sample), ASKAP/CRAFT, Parkes, DSA-110, FAST and MeerKAT. Each has its "
                "own selection function, which the model must carry. The discovery rate was roughly exponential; the "
                "localized fraction is small but growing."),
    Slide("Dispersion measure: precise beyond our needs", section=S_FRB,
          subtitle="DM is a sum of parts, and only the cosmic part carries the signal",
          figures=[Fig("eq_dm_sum.png")],
          bullets=["DM measured to 0.1%",
                   "The Milky Way term is modeled (NE2001), not measured",
                   "DM_cosmic at fixed z is skewed; its scatter is set by clumpiness F",
                   "DM_host: unknown, lognormal"],
          source=f"NE2001 map (Cordes & Lazio) via {NU}; equation rendered by {CLAUDE}",
          notes="Every burst gives a dispersion measure, the column density of free electrons, measured to a "
                "tenth of a percent. The catch: DM is a sum. The Milky Way part comes from a Galactic model "
                "(NE2001; map in the backup slides), the host part is unknown and modeled as lognormal, and the "
                "cosmic part, the one we want, is skewed at fixed redshift with a width set by the clumpiness "
                "parameter F. Precision is not the problem; decomposition is."),
    Slide("Localization: a position on the sky", section=S_FRB,
          subtitle="Arcsecond positions turn a burst into a galaxy",
          figures=[Fig("nu_outrigger_photo.png", caption="CHIME outrigger"),
                   Fig("nu_outrigger_loc.png", caption="A burst placed on a galaxy")],
          source=f"CHIME/FRB outrigger photo (CHIME/FRB collaboration, owner to confirm) and DECaLS localization image via {NU}",
          notes="To get a redshift you need a position good to about an arcsecond, which interferometers "
                "(ASKAP, DSA-110, the CHIME outriggers) now deliver for a growing minority of bursts. Only "
                "then can you find the host galaxy and measure its redshift."),
    Slide("PATH: Bayesian association to a galaxy", section=S_FRB,
          subtitle="Which galaxy is the host? A posterior over candidates, plus 'unseen'",
          figures=[Fig("nu_path_image.png", caption="Candidates with P(O|x)"),
                   Fig("eq_path.png", caption="Prior from galaxy counts × offset likelihood")],
          source=f"PATH image (Aggarwal et al. 2021) via {NU}; equation rendered by {CLAUDE}",
          notes="Host association is itself Bayesian (PATH, Aggarwal et al. 2021). Each candidate galaxy gets a "
                "prior from its brightness (number counts: faint galaxies are common, so a chance alignment is "
                "likely) and a likelihood from the burst's angular offset convolved with the localization error; "
                "an 'unseen host' hypothesis absorbs the rest. The posterior P(O|x) is what we use: here 0.94 "
                "for the obvious galaxy."),
    Slide("Redshift: the distance to the galaxy", section=S_FRB,
          subtitle="An optical spectrum of the host gives z, and the ruler for everything else",
          figures=[Fig("nu_host_spectra.png")],
          bullets=["Keck or Gemini spectrum of the host galaxy",
                   "Emission lines give z to four decimal places",
                   "About 100 bursts have one; the fitted sample has 26"],
          source=f"KCWI and GMOS host spectra (Bannister et al. 2019) via {NU}",
          notes="With a host in hand, an optical spectrum (Keck/KCWI, Gemini/GMOS) gives the redshift from "
                "emission lines. This is the expensive step: about 100 bursts have redshifts in total; the "
                "sample we fit has 26 after cuts. Every other burst has a DM and no z."),
    Slide("Population modeling: the problem", section=S_FRB,
          subtitle="Fit every survey at once: all bursts have DM, few have z",
          figures=[Fig("frb_sketch.png")],
          source=f"Sketch: {CLAUDE} (talks/ucsc_stats_2026/scripts/fig_frb_sketch.py)",
          notes="The whole problem on one sketch. Bursts at unknown redshifts pick up DM in their host, the "
                "cosmic web and the Milky Way; six telescopes with different beams and thresholds detect about "
                "600 of them, all with DM, a few dozen with z. We fit one population model to all surveys "
                "jointly, marginalizing over z for the bursts without one."),
    Slide("Population modeling: the model", section=S_FRB,
          subtitle="An inhomogeneous Poisson process on the (z, DM) plane, per survey",
          figures=[Fig("eq_lambda.png", caption="Rate density λ_s(z, DM | θ): five factors"),
                   Fig("nu_dm_cliff.png", caption="p(DM, z) for one survey: the 'DM cliff'")],
          source=f"Heat map: zdm (James et al. 2022) via {NU}; equation rendered by {CLAUDE}",
          notes="For survey s the bursts are an inhomogeneous Poisson process on the (z, DM) plane. The rate "
                "density is a product of five factors: a rate constant, the cosmic volume at z, source evolution "
                "following the star-formation history to a power n_sfr, p(DM|z) (cosmic plus host), and the "
                "survey's detection probability, which is the fraction of the energy function (power law with "
                "slope gamma and cutoff E_max) above threshold, averaged over beam and burst width. About 12 "
                "parameters. Right: the resulting p(DM, z) for one survey; the sharp edge, the 'DM cliff', is "
                "set by H0 and the scatter in DM_cosmic."),
    Slide("Population modeling: the likelihood", section=S_FRB,
          subtitle="Localized bursts enter in 2-D, DM-only bursts marginalized over z",
          figures=[Fig("eq_lnL_frb.png")],
          bullets=["Localized burst: the 2-D density λ_s(z_i, DM_i) / Λ_s",
                   "DM-only burst: the z-marginal, ∫ λ_s dz / Λ_s",
                   "Poisson terms for counts and for repeaters",
                   "The overall rate is profiled out"],
          source=f"Equation rendered by {CLAUDE}",
          notes="The extended Poisson likelihood. Localized bursts contribute the full 2-D density normalized by "
                "the survey's integral; DM-only bursts contribute the z-marginal. Poisson terms for the total "
                "counts and for the numbers of single versus repeating sources (each source repeats as a Poisson "
                "process with a power-law distribution of rates), plus a signal-to-noise term per burst. The "
                "overall rate constant is profiled out."),
    Slide("Population modeling: MCMC", section=S_FRB,
          subtitle="emcee, 12 parameters, uniform priors: one week on a cluster",
          figures=[Fig("hoffmann_fig1_corner.png")],
          source=f"Corner plot: Fig. 1 of {HOFF}",
          notes="How it is done today: the rate density is evaluated on a 500 by 1400 (z, DM) grid for every "
                "survey and rebuilt at every likelihood call. emcee with 40 walkers and 2000 steps took about a "
                "week on the OzSTAR cluster; the paper says more steps are not computationally feasible. The "
                "corner plot (Hoffmann et al. 2026, Fig. 1) shows 11 of the 12 parameters (H0 is omitted from "
                "the plot; its posterior is its prior). n_sfr against alpha, and R_min against R_gamma, are "
                "strongly degenerate."),
    Slide("Results to date", section=S_FRB,
          subtitle="The model reproduces the DM distribution; several posteriors are prior-limited",
          figures=[Fig("hoffmann_fig3_chime_cdf.png", caption="CHIME DM distribution: data vs. model"),
                   Fig("nu_macquart_2026.png", caption="The Macquart relation, ~100 localized FRBs")],
          source=f"Left: Fig. 3 of {HOFF}; right: via {NU}",
          notes="What the fit buys: the model reproduces the CHIME DM distribution (KS p = 0.9 for catalog 1) "
                "and predicts the number of repeating sources per survey (Hoffmann et al. 2026, Table 6). It "
                "constrains the source evolution and energy function. H0 is limited by its prior (restricted to "
                "the Planck–SH0ES range), and a week per fit means we cannot explore model variants freely."),
    Slide("Open challenges", section=S_FRB,
          subtitle="Speed, degeneracy, model choice, selection",
          bullets=["Speed: a week per fit; emulators, surrogates, fewer likelihood calls",
                   "Degeneracies: H0 with E_max, n_sfr with α; prior-sensitive posteriors",
                   "Model choice: seven energy-function forms; evidence or information criteria?",
                   "Selection: scattered bursts fall below threshold; how many?"],
          notes="Four open challenges. Speed: each likelihood call rebuilds the grids, so a fit takes a week. "
                "Degeneracies: H0 with the maximum energy, n_sfr with alpha; several posteriors (H0, R_max) follow their priors. "
                "Model choice: zdm implements seven luminosity-function forms and only one has been fit; we "
                "compare with BIC at best. Selection: scattering broadens bursts below threshold and the "
                "incompleteness is poorly known."),
    Slide("Discussion I", section=S_FRB,
          subtitle="Five minutes: what would you do differently?",
          bullets=["Can the (z, DM) grid be replaced by an emulator, or the likelihood made differentiable (HMC)?",
                   "How do we get a proper evidence for seven luminosity-function forms?",
                   "How do we make the posterior less prior-driven: hierarchical priors, simulation-based inference?"],
          notes="First discussion slot, five minutes. Three questions to the room: an emulator or a "
                "differentiable likelihood for the grid; a proper evidence across seven luminosity-function "
                "forms; hierarchical priors or simulation-based inference to loosen the prior's grip."),
    # ------------------------------------------------------------- BING
    Slide("Part II: Inverting ocean colour", kind=DIVIDER, section=S_BING,
          notes="Part II. From the colour of the ocean to what is in the water."),
    Slide("What is in the water?", section=S_BING,
          subtitle="Ocean colour encodes phytoplankton, dissolved organics and particles",
          figures=[Fig("ocean_sketch_forward.png", caption="The forward problem: sun, sea, satellite"),
                   Fig("pace_moana.png", caption="PACE: phytoplankton from space")],
          bullets=["Chlorophyll (phytoplankton), coloured dissolved organic matter, particles",
                   "Stretch goal: which phytoplankton (functional types)"],
          source=f"Sketch: {CLAUDE}; PACE MOANA map: NASA PACE / talks/wmko_2026",
          notes="The colour of the ocean is set by what absorbs and scatters light in the upper water: "
                "phytoplankton (chlorophyll), coloured dissolved organic matter (CDOM) and particles. These "
                "matter for the carbon cycle. The goal is to infer their concentrations, and ideally which "
                "phytoplankton, from a reflectance spectrum. Left: the forward problem (sun, sea, satellite) and "
                "the inverse problem; right: a PACE map of phytoplankton groups."),
    Slide("PACE: a colour spectrum per square kilometre", section=S_BING,
          subtitle="Millions of spectra a day, each with its own error bars",
          figures=[Fig("awoc_pace_fit_rrs.png")],
          bullets=["R_rs(λ): light leaving the water over incoming sunlight",
                   "100+ bands, 340–890 nm, ~1 km pixels",
                   "The globe every 1–2 days: ~10⁸ ocean spectra a day",
                   "Per-wavelength uncertainties supplied with the data"],
          source=f"Real PACE OCI spectrum with BING fit via {AWOC}",
          notes="NASA's PACE satellite (launched 2024) measures the remote-sensing reflectance, light leaving the "
                "water over incoming sunlight, in more than 100 bands from 340 to 890 nm, at about 1 km, over the "
                "whole globe every one to two days. That is of order a hundred million ocean spectra a day, each "
                "delivered with per-wavelength uncertainties. Shown: one real PACE spectrum with its error bars "
                "and a BING fit."),
    Slide("Strong systematics", section=S_BING,
          subtitle="Coherent residuals at 400–520 nm: the atmospheric correction?",
          figures=[Fig("awoc_pace_fit_rrs.png")],
          bullets=["The atmosphere contributes ~90% of the light at the sensor",
                   "Its removal leaves correlated residuals the model cannot absorb",
                   "χ²_ν = 1.44 for a 5-parameter fit"],
          source=f"Via {AWOC}",
          notes="Fit the real spectrum and the reduced chi-squared is 1.44. The residuals are not noise: a "
                "coherent run at 400 to 520 nm. The atmosphere contributes about 90 percent of the light at the "
                "sensor, and the correction that removes it leaves correlated errors our diagonal likelihood "
                "cannot describe."),
    Slide("Poorly measured errors", section=S_BING,
          subtitle="Residuals beyond 600 nm are many sigma: the error bars are wrong",
          figures=[Fig("awoc_pace_fit_rrs.png", caption="Residuals in units of σ"),
                   Fig("awoc_pab_dbbp.png", caption="PACE vs. float backscattering: a systematic offset")],
          source=f"Left via {AWOC}; right: A. James et al. 2026 (in prep.), PACE × BGC-Argo match-ups, via {AWOC}",
          notes="Beyond 600 nm the residuals are many sigma: the supplied uncertainties are too small there. And "
                "against independent in-water measurements (BGC-Argo floats, James et al. 2026), PACE "
                "backscattering is systematically high almost everywhere. Calibration, atmospheric correction "
                "and the error model all need work before the statistics can be trusted."),
    Slide("The forward model", section=S_BING,
          subtitle="Absorption and backscattering set the colour (Gordon et al. 1988)",
          figures=[Fig("eq_gordon.png", caption="R_rs from u = b_b / (a + b_b)"),
                   Fig("eq_iop_model.png", caption="Non-water parts: 2–5 parameters")],
          source=f"Equations rendered by {CLAUDE}",
          notes="The forward model is simple. Reflectance is a quadratic in u = b_b over (a + b_b), the "
                "backscattering fraction, with known coefficients (Gordon et al. 1988). Absorption and "
                "backscattering are each a known pure-water part plus a non-water part with a nested parametric "
                "form of two to five parameters: an exponential for dissolved and detrital matter (amplitude and "
                "slope S_dg), a phytoplankton template with an amplitude, and a power law for particle "
                "backscattering (amplitude and exponent beta)."),
    Slide("A physical degeneracy", section=S_BING,
          subtitle="Scale a and b_b together by 100×: the same R_rs. Only the water terms object.",
          figures=[Fig("bing_fig4_degeneracy.png")],
          source=f"Fig. 4 of {BING}",
          notes="The crux (Fig. 4 of the paper). Reflectance depends on a and b_b only through their ratio, so scaling both by the "
                "same factor, here up to 100 times, gives an identical spectrum. Only the pure-water parts, which "
                "do not scale, break the symmetry, and they are small where the signal is. So absorption and "
                "backscattering are not separately identifiable without priors, and the data support only a "
                "few non-water parameters."),
    Slide("An \"infinite\" number of templates, I", section=S_BING,
          subtitle="Three different models fit one spectrum equally well",
          figures=[Fig("awoc_three_models_rrs.png")],
          bullets=["k = 5 (ours): χ²_ν = 0.80",
                   "GIOP (NASA's operational model): χ²_ν = 1.01",
                   "GSM: χ²_ν = 1.13",
                   "Very different assumptions, same goodness of fit"],
          source=f"Via {AWOC} (Fig. 10 of {BING})",
          notes="Fit one simulated PACE spectrum with our five-parameter model, NASA's operational GIOP and the "
                "GSM model. All three have reduced chi-squared near one. Different priors and fixed parameters, "
                "indistinguishable fits."),
    Slide("An \"infinite\" number of templates, II", section=S_BING,
          subtitle="…and they disagree about what is in the water",
          figures=[Fig("awoc_three_models_bb.png", caption="Backscattering: different amplitude and slope"),
                   Fig("awoc_three_models_aph.png", caption="Phytoplankton absorption: >400% apart")],
          bullets=["Equal χ²; a_ph(440) = 0.23 m⁻¹ true vs. ~0.05 for GIOP"],
          source=f"Via {AWOC} (Fig. 10 of {BING})",
          notes="Same figure, other panels. The retrieved backscattering curves differ in amplitude and slope "
                "(30 to 40 percent apart), and the phytoplankton absorption at 440 nm by more than 400 percent: "
                "true 0.23 per metre, GIOP about 0.05, GSM in between with the wrong shape. The spectrum cannot "
                "tell them apart; the priors decide."),
    Slide("Standard MCMC", section=S_BING,
          subtitle="emcee per spectrum: 75,000 steps; nested models compared by BIC",
          figures=[Fig("awoc_corner.png", caption="Posterior of the 5 parameters"),
                   Fig("eq_lnL_gauss.png", caption="Gaussian likelihood; BIC from the LM fit")],
          source=f"Corner plot via {AWOC}; equation rendered by {CLAUDE}",
          notes="The inference is standard: an independent Gaussian likelihood with the supplied per-wavelength "
                "errors, log-uniform priors on amplitudes, uniform on S_dg (0.01 to 0.02 per nm) and beta (0 to "
                "2), emcee with 75,000 steps keeping the last 7,000, and nested models (k = 2 to 5) compared by "
                "BIC from a Levenberg–Marquardt best fit. The corner plot shows the degeneracies: the "
                "phytoplankton amplitude against the dissolved amplitude and slope."),
    Slide("Expensive for one spectrum. Operational?", section=S_BING,
          subtitle="29 s per spectrum × 10⁸ spectra a day ≈ 93 CPU-years per day",
          figures=[Fig("bing_cost.png", placeholder="NEW (B3): cost of per-pixel MCMC at PACE scale")],
          source=f"Timing: talks/ucsc_stats_2026/scripts/time_bing_fit.py on an Apple M5 Max, one core ({CLAUDE})",
          notes="Measured this week on one core of a laptop: the Levenberg–Marquardt start takes 3 ms, the emcee "
                "run (16 walkers, 75,000 steps plus burn-in, 1.2 million likelihood calls at 24 microseconds "
                "each) takes 29 seconds. PACE delivers of order a hundred million cloud-free ocean spectra a "
                "day, so per-pixel MCMC costs about 93 CPU-years per day, or 34,000 cores running flat out. "
                "That is why the operational products use point estimates with linearized error propagation, not posteriors."),
    Slide("Priors break the degeneracy, and bias the answer", section=S_BING,
          subtitle="Fix the slope S_dg differently and the phytoplankton changes fourfold",
          figures=[Fig("bing_fig10_priors.png")],
          source=f"Fig. 10 of {BING}",
          notes="Priors are the only way to break the degeneracy, and they bias the answer. GIOP and GSM fix the "
                "dissolved-matter slope S_dg at different values and get phytoplankton absorption at 440 nm that "
                "differs by more than 400 percent (0.23 true, about 0.05 for GIOP) with equal chi-squared. With "
                "our weak priors (backup slide), phytoplankton absorption is biased low by 21 percent over the "
                "simulated set and is only an upper limit for most low-chlorophyll spectra; the backscattering "
                "exponent beta simply "
                "returns its prior. How to choose or learn priors, perhaps hierarchically across pixels, is "
                "the open question."),
    Slide("Where do we take new data?", section=S_BING,
          subtitle="Which extra measurement shrinks the posterior most?",
          figures=[Fig("awoc_pab_matchups.png")],
          bullets=["In-water backscattering from robotic floats (BGC-Argo)",
                   "Fluorescence, polarization, more wavelengths?",
                   "An experimental-design question: value of information per measurement"],
          source=f"PACE × BGC-Argo match-ups via {AWOC} (A. James et al. 2026, in prep.)",
          notes="The degeneracy can be broken by data, not only priors. Which extra measurement buys the most: "
                "in-water backscattering from BGC-Argo floats (the match-up map shown), fluorescence, "
                "polarization, more wavelengths? That is an experimental-design question we have not posed "
                "formally."),
    Slide("Can we GP this?", section=S_BING,
          subtitle="Amortize: simulate, train, infer every pixel in one pass",
          figures=[Fig("amortized_schematic.png", placeholder="NEW (B3): per-pixel MCMC vs amortized inference")],
          source=f"Schematic: {CLAUDE}",
          notes="The alternative to per-pixel MCMC: simulate spectra from the forward model with realistic noise "
                "(we have 3,320 Hydrolight spectra and the Gordon model), train a Gaussian process or neural "
                "map from spectrum to posterior, and apply it to every PACE pixel in one pass. The question is "
                "whether the posteriors stay calibrated when the real data have the systematics we saw."),
    Slide("Discussion II", section=S_BING,
          subtitle="Five minutes: priors, evidence, scale",
          bullets=["How do we get a proper Bayesian evidence for the nested models, not BIC from a point estimate?",
                   "Informative priors break the degeneracy but bias the answer: can they be learned hierarchically?",
                   "Amortized or simulation-based inference at PACE scale: how do we keep the posteriors calibrated?"],
          notes="Second discussion slot, five minutes. Evidence for nested models beyond BIC; priors that are "
                "learned rather than imposed; amortized posteriors that stay calibrated at a hundred million "
                "spectra a day."),
    # ------------------------------------------------------------- other
    Slide("Two other problems", kind=DIVIDER, section=S_OTHER,
          notes="Two more problems, briefly, where I would like your opinion rather than present a method."),
    Slide("Phytoplankton functional types from pigments", section=S_OTHER,
          subtitle="Beyond chlorophyll: which phytoplankton?",
          figures=[Fig("pace_moana.png")],
          bullets=["PACE's MOANA product: Prochlorococcus, Synechococcus, picoeukaryotes",
                   "Trained on in-situ cell counts (flow cytometry) matched to spectra",
                   "Empirical, not physical: a regression on the spectrum"],
          source="PACE MOANA map: NASA PACE / talks/wmko_2026",
          notes="PACE's operational phytoplankton product (MOANA) maps three groups of small phytoplankton. It is "
                "empirical: a regression from the spectrum to cell counts, trained on ship measurements. Two "
                "approaches in the literature, next."),
    Slide("PCA of the spectrum (Lange et al. 2020)", section=S_OTHER,
          subtitle="Project each spectrum onto a fixed basis, regress the loadings on cell counts",
          figures=[Fig("moana_pc_loadings.png")],
          bullets=["Standardize R_rs(λ), project onto 6 principal components",
                   "Multiple linear regression of each group on the loadings (plus SST)",
                   "Re-implemented and retrained: recovers NASA's basis"],
          source="MOANA PCA basis, re-derived in EPFT-UP (J. X. Prochaska & Claude, 2026)",
          notes="Lange et al. 2020: standardize each spectrum, project it onto a fixed PCA basis (shown: the six "
                "components), and regress each group's abundance on the loadings plus sea-surface temperature. "
                "We re-implemented and retrained it and recover NASA's basis."),
    Slide("Second derivative + PCA (Kramer et al. 2022)", section=S_OTHER,
          subtitle="Subtract a smooth model, differentiate twice, regress on 13 pigments",
          figures=[Fig("kramer_fig5_method.png")],
          source=f"Fig. 5 (top row) of {KRAMER}",
          notes="Kramer et al. 2022: fit and subtract a smooth three-parameter model, take the second derivative "
                "of the residual to bring out narrow pigment features, PCA, then principal-component regression "
                "on 13 pigments measured by HPLC. The panels show the correlation between diatom pigments and the "
                "spectrum against wavelength: residual, first derivative, second derivative; the structure "
                "sharpens with each derivative. Cross-validated R-squared from 0.37 to 0.72 (backup slide)."),
    Slide("What do you recommend?", section=S_OTHER,
          subtitle="Five minutes: composition from a spectrum",
          bullets=["State of the art: PCA of R_rs (or of its second derivative) → linear regression",
                   "A spectrum has 100+ bands but supports 3 (multispectral) to 4–5 (PACE) parameters",
                   "Is there a better-posed way to get composition, with uncertainties?"],
          notes="Third discussion slot. PCA plus regression is the state of the art, and it works to a point. But "
                "a spectrum with 100 bands supports three physical parameters from multispectral data, four or five "
                "from PACE. Is there a better-posed "
                "way to get composition, with uncertainties?"),
    # ------------------------------------------------------------- close
    Slide("A model ocean constrained by data", section=S_CLOSE,
          subtitle="California coast, ROMS 4D-Var: four days of observations into a model, every day",
          figures=[Fig("roms_sst_nowcast.png", caption="UCSC 4D-Var analysis, 13 Oct 2026: SST, currents"),
                   Fig("cugn_lines.png", caption="The glider lines it assimilates")],
          bullets=["Satellites, tide gauges, Argo floats and gliders, assimilated by 4D-Var (Edwards, Moore)",
                   "The ask: faster assimilation, learned emulators, uncertainties 4D-Var does not give"],
          source=f"Left: {ROMS}; right: CUGN lines (Rudnick et al. 2017), drawn by {CLAUDE}",
          notes="A forthcoming data problem. Chris Edwards and Andy Moore run a ROMS 4D-Var state estimate of the "
                "California Current every day: four days of satellite sea level and temperature, tide gauges, "
                "Argo floats and the glider lines, into a 10 km model (2 km for NOAA's WCOFS). It works; it is "
                "slow, and it gives one state, not a distribution. Faster assimilation and learned emulators "
                "with honest uncertainties are what the field wants."),
    Slide("Optimize the robot placement", section=S_CLOSE,
          subtitle="What is gained by flying gliders off their standard lines?",
          figures=[Fig("cugn_lines.png")],
          bullets=["Three lines since 2006, a fourth since",
                   "Which track, when, buys the most skill?",
                   "Sequential design, the model as testbed",
                   "BOONUS: ~100 gliders, soon"],
          source=f"CUGN lines (Rudnick et al. 2017), drawn by {CLAUDE}; array modes: Moore, Arango & Edwards 2018",
          notes="The gliders have flown three fixed lines since 2006 and a fourth (56) more recently. What science is gained by flying them "
                "elsewhere, and when? Edwards' group has array modes (Moore et al. 2018) for the current system; "
                "the general problem is sequential experimental design with the model as the testbed. BOONUS, "
                "about 100 gliders around the U.S. coast, makes this urgent."),
    Slide("What I would like from you", section=S_CLOSE,
          subtitle="Data and code are public; the README has the details",
          bullets=["Faster inference for a week-long MCMC: emulators, differentiable likelihoods, SBI",
                   "Honest evidence and learned priors for nested, degenerate models",
                   "Calibrated amortized posteriors at 10⁸ spectra a day",
                   "Clancy James (FRBs) · Robert Frouin (ocean colour) · jxp@ucsc.edu · github.com/FRBs/zdm · github.com/ocean-colour/bing"],
          notes="Three asks: faster inference for the FRB fit, honest evidence and learned priors for the ocean "
                "fit, and calibrated amortized posteriors at satellite scale. Two collaborators to write to, two "
                "public repositories, and the README with the equations. Thank you."),
    # ------------------------------------------------------------- backup
    Slide("Backup", kind=DIVIDER, section=S_BACKUP, backup=True,
          notes="Backup slides: the 2020 Macquart relation, H0 and the DM cliff, F and feedback, the ΔBIC "
                "forecast, scattering selection, phytoplankton upper limits, repetition posteriors."),
    Slide("The Macquart relation (2020)", section=S_BACKUP, backup=True,
          figures=[Fig("nu_macquart_2020.png")],
          source=f"Macquart et al. 2020, Nature 581, 391, via {NU}",
          notes="The original detection of the missing baryons with five localized ASKAP FRBs."),
    Slide("H0 and the DM cliff", section=S_BACKUP, backup=True,
          figures=[Fig("nu_h0_contours.png")],
          source=f"zdm (James et al. 2022) via {NU}",
          notes="p(DM, z) contours for H0 = 60, 70, 80: the DM cliff moves with H0, and with E_max."),
    Slide("F and feedback", section=S_BACKUP, backup=True,
          figures=[Fig("nu_baptista_F.png", caption="Posterior on F from 16 FRBs"),
                   Fig("nu_connor_feedback.png", caption="DSA-110: low scatter, strong feedback")],
          source=f"Baptista et al. 2024; Connor et al. 2025; via {NU}",
          notes="The scatter in DM_cosmic (F) constrains galactic feedback; fixed in Hoffmann et al. 2026."),
    Slide("ΔBIC: multispectral vs. hyperspectral", section=S_BACKUP, backup=True,
          figures=[Fig("awoc_dbic.png")],
          source=f"Via {AWOC} (Fig. 6 of {BING})",
          notes="Multispectral data prefer 3 over 5 parameters in >99% of cases; PACE favours phytoplankton in "
                "only ~30%."),
    Slide("Selection effects: scattering", section=S_BACKUP, backup=True,
          figures=[Fig("nu_tau_cdf.png", caption="Scattering times: CHIME vs. ASKAP"),
                   Fig("nu_whost.png", caption="Burst widths and completeness")],
          source=f"Scott et al. 2025; James et al. 2026; via {NU}",
          notes="No physical cutoff in the scattering distribution: how many bursts are missed?"),
    Slide("Phytoplankton absorption: retrieved vs. true", section=S_BACKUP, backup=True,
          figures=[Fig("bing_fig11_aph.png")],
          source=f"Fig. 11(a) of {BING}",
          notes="Retrieved against true a_ph(440) on simulated PACE spectra: bias −21%, MAE 40%; most of the "
                "low-chlorophyll spectra give only an upper limit (light blue)."),
    Slide("Kramer et al. 2022: retrieved vs. measured pigments", section=S_BACKUP, backup=True,
          figures=[Fig("kramer_fig6_results.png")],
          source=f"Fig. 6 (A, B) of {KRAMER}",
          notes="Principal-component regression on the second-derivative residual spectra: cross-validated R² "
                "from 0.37 (zeaxanthin) to 0.72 (total chlorophyll a) over 13 HPLC pigments."),
    Slide("The Milky Way's share of DM: NE2001", section=S_BACKUP, backup=True,
          figures=[Fig("nu_ne2001.png")],
          source=f"NE2001 Galactic electron model (Cordes & Lazio 2002) via {NU}",
          notes="The Galactic contribution to DM is modeled, not measured: NE2001 (Cordes & Lazio 2002) gives "
                "tens of pc/cm³ at high latitude and hundreds in the plane, with its own uncertainty."),
    Slide("Repetition parameters", section=S_BACKUP, backup=True,
          figures=[Fig("hoffmann_fig2_repetition.png")],
          source=f"Fig. 2 of {HOFF}",
          notes="R_min, R_max, R_gamma: the R_min–R_gamma banana and an R_max lower limit only."),
]
