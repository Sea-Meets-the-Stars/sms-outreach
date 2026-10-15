# UCSC Stats 2026 Talk

## Goals

Generate a README and talk for the UCSC Stats 2026 department.  
The talk will be 1 hour long and cover the following topics:

- Bayesian fitting of FRB DM and redshifts from multiple surveys
- Bayesian fitting of hyperspectral observations of the ocean

## Context

All of the figures (and related code) in this Repository.

I give my talks as Google Slides.

My Oceanography talks in the Google Drive, `GDrive:Oceanography/Talks/` provide examples of the kind of presentation I tend to give.  See the talk in `2026/AOGS` in particular

We will put the slides in the Google Drive, `GDrive:Oceanography/Talks/2026/UCSC_Stats` 

We will share a README for the Department giving a basic introduction
to the data that will be presented in the talk.

The FRB analysis uses the code in the `Projects/FRBs/zdm` repository
The hyperspectral analysis uses the code in the `Oceanography/python/bing` repository

There is a paper on the `zdm` analysis in `context/papers/hoffmann2026.pdf`
The BING papers in in `context/papers/bing.pdf`

## Code

If you need to run Python, use the "ocean14" conda environment.


## Slide Outline

## Prompts

### README

1. Examine the files described in the Context section.  Then start a conversation with 
me about the README for the Department.
Put your questions in the Q&A/Setup section.
Use Fable if you can.  Log your work.

2. I have answered all the questions in the Q&A/README section.  
Please review the questions and answers and ask more as needed.
Also note that I added two PDFs to `context/papers/`, as described in the Context section.
These may be helpful to you.
Last, we wish to include two sketches in the Google doc to illustrate the two problems.
Use Fable if you can.  Log your work.

3. I have answered all the questions in the Q&A/README section.  
Please proceed to generate the README docs.
Use Fable if you can.  Log your work.


## Q&A

### README

(The prompt says "Q&A/Setup"; this doc has no Setup subsection, so the questions are here under Q&A/README.)  Each question has a proposed default; answer "default" to accept it.

**A. Audience, format, delivery**

1. **Audience and level.**  The Drive doc `UCSC_Stats/Stats Talk` says the README goes out "a day or two ahead".  I would write for Statistics faculty and PhD students who know Bayesian inference, MCMC and point processes but have no astronomy or ocean-optics background.  So: no jargon left undefined, and physics only as far as it is needed to understand the likelihood.
   - Default: as above.
   - A: Use your default
2. **Talk date, room, host.**  What is the date, and who is the departmental host?  This sets the README deadline, and the header should name them.
   - A: The deadline is today.  My host is Prof. Yunyi Shen
3. **Format and location.**  Default: Markdown at `talks/ucsc_stats_2026/README.md` (renders on GitHub), plus a Google Doc or PDF copy in `GDrive:Oceanography/Talks/2026/UCSC_Stats` to circulate.  Would you rather the department get a GitHub link, a PDF, or a Doc?
   - A: I wish for it to be a Google Doc in the GDrive folder.
4. **Length.**  Default: about 3–4 pages.  That is a one-paragraph overview, ~1.5 pages per problem (science goal → data → model/likelihood → current method → where we want help), and a short "data access" section.
   - A: Aim for a paragraph summary and no more than 1 page of text
5. **Title.**  `Stats Talk` gives "Advancing science on the frontier with modern statistical techniques".  Keep it for both the README and the talk?
   - A: Yes, keep it.
6. **"Simple stats" prong.**  `Stats Talk` lists "Simple stats" as the first prong.  What did you mean by it: a primer on how astronomers and oceanographers use statistics (χ², BIC, emcee), or something else?  Should it appear in the README?
   - A: Ignore it for the README
7. **Hands-on data.**  Should the README let people actually use the data?  Default: yes, a small curated bundle with pointers to the public repos (`github.com/FRBs/zdm`, `github.com/ocean-colour/bing`):
   - the FRB survey tables (`zdm/data/Surveys/*.ecsv`: DM, S/N, z, threshold, beam, ...);
   - a subset of the Loisel+2023 Hydrolight spectra (public on Dryad, doi:10.6076/D1630T; truth known);
   - one or two real PACE spectra with uncertainties.

   Or would you prefer description only?
   - A: Description only

**B. FRB problem (zdm)**

8. **Scope of the data.**  zdm covers ~700 FRBs from about 10 surveys: CHIME Cat-1 (492), DSA-110 (60, 40 with z), ASKAP/CRAFT ICS and CRACO, Parkes, MeerTRAP and FAST.  About 100 are localized (have a redshift).  Default: a table of all surveys with N and N_z, stressing (i) the mix of localized and unlocalized events (marginalizing over z) and (ii) selection functions that differ by survey (beam, fluence threshold, DM smearing).  OK?
   - A: Just a qualitative description, emphasizing the data are a mix of origins and selection functions.
9. **How much model to show.**  Default: one display equation for the inhomogeneous Poisson likelihood, ln L = Σ ln p(DM_i, z_i, SNR_i | θ) − N_exp(θ).  Add a short list of components: Macquart DM_cosmic with feedback F, lognormal DM_host, energy function (E_max, γ), source evolution (n_sfr), and H0.  Note that the rate constant is profiled out.  Is that the right depth?
   - A: Yes, include a few of the equations, but keep jargon to a bare minimum.
10. **Headline result to quote.**  Which numbers and paper should be the current state of the art: James+2022 (H0), Baptista+2024 (F), or a newer MCMC result (Hoffmann et al.)?  Is there a 2026 result I should cite?
   - A: No need to comment on results.  We are focusing on methods.
11. **"Where we need help" for FRBs.**  `Stats Talk` asks for a "better/faster way" to sample.  From the code, candidates are:
    - (a) each MCMC step rebuilds the 500×1400 (z,DM) grids, so emcee takes ~48 h on 20 CPUs; emulators or surrogates could help;
    - (b) a finite PENALTY for "impossible" FRBs makes the posterior non-smooth;
    - (c) the H0–E_max and H0–F degeneracies;
    - (d) choosing among 6 luminosity-function forms (evidence vs. BIC);
    - (e) the hierarchical PATH host-association extension.

    Which should go in the README?  Default: a, c, d.
   - A: a, c, d
12. **Collaborators.**  Who should be credited for zdm (e.g. Clancy James, Jordan Hoffmann, ...)?  Any of them to name as contacts?
   - A: Clancy James

**C. Hyperspectral ocean problem (bing)**

13. **Data to feature.**  Default: both of these.
    - Loisel+2023 Hydrolight simulations (3,320 spectra, 81 bands from 350–750 nm, true a and b_b known) as the controlled test.
    - Real PACE OCI spectra matched to BGC-Argo b_bp (PAB, ~250 match-ups, 38 "gold") as the reality check.

    OK?
   - A: Yes, include both.
14. **The identifiability message.**  The Prochaska & Frouin paper finds three things:
    - R_rs depends only on b_b/(a+b_b), so a and b_b are not separately identifiable without priors;
    - multispectral data support ≤3 non-water parameters (ΔBIC);
    - a_ph is undetectable without strict S_dg priors.

    I would make this the centerpiece of the ocean half, since it is the most "statistical" result.  What is the paper's status (accepted? citation)?
   - A: Accepted, and a copy is now in `context/papers/bing.pdf`
15. **"Where we need help" for oceans.**  Candidates:
    - (a) full or correlated noise covariance (the current fit uses an independent Gaussian);
    - (b) proper evidence vs. BIC from Levenberg–Marquardt;
    - (c) forward-model (Gordon approximation) error;
    - (d) informative priors and the bias they bring;
    - (e) scaling MCMC to millions of PACE pixels per day (amortized or simulation-based inference);
    - (f) label switching and degeneracy in two-component b_b models.

    Default: a, b, d, e.
   - A: Use b, d, e
16. **Data assimilation.**  `Stats Talk` also lists "Speeding up data assimilation" (BOONUS gliders?) under "Where I need help".  Is that a third topic for the README, a one-line teaser, or out of scope?  The prompt names only the two Bayesian problems.  Default: a one-line teaser in the closing "forthcoming large datasets" paragraph.
   - A:  I won't include this in the README.
17. **Collaborators.**  Default credit: Robert Frouin (bing); the ocean-optics team from AOGS slide 5 (James, Gray, Frouin, Housekeeper).  Corrections?
   - A: Robert Frouin

**D. Sources I plan to draw on**

18. **OK to use these?**  Do any of them shouldn't be used, or are there others I've missed?
    - Drive `BING` deck (May 2026): "Why Bayesian?", the corner plot, degeneracy.
    - AOGS_2026 slides 7–8 and 10–14: carbon-cycle motivation, the Bayesian-inversion pipeline, IOPtics, PAB.
    - The `fig_pillar_III` Macquart-relation slide (NSF_FRB_2025).
    - The Overleaf BING figures: `fig_deg_170`, `fig_bic_modis_pace`, the corner plot.
    - Regenerated zdm figures: zdm stores no PNGs, so `papers/H0_I/Figures/py/figs_zdm_H0_I.py` would need to be run.
   - A: Yes, use all of them.

#### Round 2 (after README #2)

The two sketches are in `talks/ucsc_stats_2026/figures/` (`frb_sketch.png`, `ocean_sketch.png`), made by the scripts in `talks/ucsc_stats_2026/scripts/`.  Because the deadline is today, every question has a default.

19. **The sketches.**  Please look at both.
    - FRB: burst → host / cosmic web / Milky Way (DM = electrons along the path) → 6 telescopes, each with its own beam and threshold → catalogue (every burst has DM, few have z).  An inset shows the DM–z relation with its growing scatter, localized points, and DM-only ticks.
    - Ocean: on the left, the forward problem (sun → sea → PACE, with the Gordon relation).  On the right, the inverse problem: three fits that match within PACE noise come from non-water absorption ×1, ×3 and ×10 with b_b adjusted.  The spectrum is the paper's L23 example #170, computed with bing.

    Default: use them as they are.
   - A: Yes, use them as they are.
20. **Proposed captions.**
    - FRB: "A burst at redshift z picks up dispersion measure (DM) in its host galaxy, the cosmic web and the Milky Way.  Six telescopes with different beams and thresholds detect ~600 bursts, all with DM but only ~30 with z.  The population model is fit to all surveys jointly."
    - Ocean: "Sunlight absorbed (a) and backscattered (b_b) by seawater and its contents sets the colour spectrum R_rs(λ) seen by PACE.  But R_rs depends only on b_b/(a+b_b), so very different oceans give spectra that are indistinguishable within the noise."

    OK?
   - A: OK
21. **Which FRB sample to describe.**  The Hoffmann et al. paper fits ~600 bursts from 6 telescopes, ~30 with z (after cuts; CHIME is 492 of them).  The zdm repo holds more (~700, ~100 with z, adding newer DSA and CRACO data).  Default: quote the paper's sample ("~600 bursts, a few dozen with redshifts"), as the sketch does.
   - A: Use the default
22. **FRB citation.**  Hoffmann, James, Prochaska, Pastor-Marazuela, Sharma & Connor, arXiv:2609.27282 (Sep 2026).  The template looks like PASA.  Should I cite it as "arXiv:2609.27282", or is it submitted or accepted somewhere?
   - A: arXiv:2609.27282
23. **FRB degeneracies (help item c).**  The H0–E_max and H0–F degeneracies come from James et al. 2022; F is fixed in Hoffmann et al.  The degeneracies Hoffmann et al. themselves report are n_sfr–α and repetition-rate R_min/R_max–R_γ, and H0 is limited by its prior.  Default: one generic sentence, "several population parameters are strongly degenerate (e.g. the expansion rate H0 with the maximum burst energy), so posteriors are prior-sensitive", with no extra citation.
   - A: Use the default
24. **Repeaters.**  Hoffmann et al.'s main addition is FRB repetition: every source repeats as a Poisson process with a power-law distribution of rates.  It adds Poisson terms for single vs. repeating sources.  Default: one sentence only, since it adds jargon.
   - A: Use the default
25. **Ocean citation and data.**  The paper is published: Prochaska & Frouin 2025, *Biogeosciences* 22, 4705 (doi:10.5194/bg-22-4705-2025).  It uses only the L23 simulations, with spectra regenerated by the Gordon model, and simulated MODIS/SeaWiFS/PACE noise.  The PACE + BGC-Argo match-ups (Q13) are unpublished follow-up in the bing repo.  Default: describe them as "ongoing: real PACE spectra matched to robotic-float measurements of backscattering", with no numbers.
   - A: Ongoing is fine, but do describe a bit what PACE provides
26. **Equations in a Google Doc.**  Docs can't render LaTeX through the API.  Options:
    - (a) plain Unicode inline, e.g. `u = b_b/(a + b_b)`, `R_rs ≈ G₁u + G₂u²`;
    - (b) small rendered equation images;
    - (c) I insert them as plain text and you convert them with the Docs equation editor.

    Default: (a), with at most 2 equations per problem: the DM sum plus the extended Poisson likelihood, and the Gordon relation plus the Gaussian likelihood.
   - A: Use (a). It is ok to include more equations if they are needed to understand the problem.
27. **One page.**  Default: the 1-page limit applies to text.  The two sketches are extra, half-width, side by side below the summary paragraph.  Or should everything fit on one page?
   - A:  That is right, the 1-page limit applies to text.  And if the equations push us past 1 page that is ok
28. **Creating the Doc.**  Default: create a new Google Doc, "UCSC Stats 2026 – README", in `GDrive:Oceanography/Talks/2026/UCSC_Stats`.  It would get the title, your name and affiliation, host Prof. Yunyi Shen, a summary paragraph, one section per problem (science goal → data → model → method → where we need help), contacts (Clancy James, Robert Frouin), the code links and the two sketches.  It stays unshared; you share it.  Also write a Markdown copy to `talks/ucsc_stats_2026/README.md`?  Default: yes to both.
   - A: Yes to both
29. **Paper typos (FYI).**  While reading `bing.pdf`, the agent found two apparent typos.  The S_dg prior is printed as U[0.1, 0.2] nm⁻¹ where the code uses [0.01, 0.02].  The above-surface conversion prints 1.17 where Lee et al. 2002 and the code use 1.7.  The README will use the code values.
   - A: OK

## Logs

### 2026-10-15 (README #1: examined context, opened Q&A)

I used three Claude Fable 5.1 subagents, each read-only, to survey the sources in parallel: the zdm repo, the bing repo, and Google Drive.  The questions are in Q&A/README (18, in four groups); the doc has no "Q&A/Setup" subsection.  No files were changed except this one.  No git commands were run.  Drive renders of AOGS_2026 are in the session scratchpad only.

*What I found.*
- **zdm (`~/Projects/FRBs/zdm`, github FRBs/zdm).**
  - *Likelihood.*  An inhomogeneous Poisson likelihood on a (z, DM) grid (`zdm/grid.py`, `zdm/iteration.py`).  It includes p(z,DM) for localized FRBs, p(DM) for unlocalized ones (marginalized over z), p(SNR), Poisson N with the rate constant profiled out, repeaters, widths and scattering, and new PATH host-association terms.
  - *Model.*  DM_cosmic follows Macquart+2020 (feedback F).  DM_host is lognormal.  MW ISM and halo uncertainties are integrated over.  There are 6 energy-function forms, including the new Break-Schechter (PR #89).
  - *Inference.*  emcee (`zdm/MCMC.py`) with uniform box priors (`zdm/data/MCMC/params.json`); grids are rebuilt every step, so one run takes ~48 h on 20 CPUs.  The older likelihood cube has been retired.
  - *Data.*  `zdm/data/Surveys/*.ecsv`, ~700 FRBs (CHIME Cat-1 492, DSA 60, CRAFT ICS/CRACO, Parkes, MeerTRAP, FAST), ~100 with redshifts.
  - *Figures.*  PNG and PDF files are gitignored, so figures must be regenerated (e.g. `papers/H0_I/Figures/py/figs_zdm_H0_I.py`).
- **bing (`~/Oceanography/python/bing`, github ocean-colour/bing).**
  - *Model.*  The Gordon quadratic forward model, R_rs(b_b/(a+b_b)), with nested parameterizations of a_nw and b_bnw (k = 2–6, standard ExpBricaud+Pow).  Priors are log-uniform on amplitudes, with optional Gaussian S_dg and CDOM/a_ph ratio priors.
  - *Inference.*  An independent Gaussian likelihood with per-sensor noise (PACE σ from OCI `Rrs_unc`).  Sampling uses emcee with an LM start, and models are compared by AIC/BIC.
  - *Data.*  Loisel+2023 Hydrolight (3,320 × 81 bands), PACE OCI granules, BGC-Argo match-ups, MODIS/SeaWiFS match-ups.
  - *Paper.*  Prochaska & Frouin (Overleaf `BING/`; slide-ready figures in `Overleaf/BING/Figures/`).  Its key message is non-identifiability: a vs b_b, ≤3 parameters from multispectral data, and a_ph not detectable without priors.
- **Drive.**
  - *Talks folder.*  `Oceanography/Talks/2026/` holds Soka, MBARI, OceanAI, AOGS and UCSC_Stats.
  - *AOGS_2026.*  17 slides, 15 min, image-heavy, one figure per slide, no equations, several Claude-made infographics.  The Bayesian-inversion pipeline is slide 8, and the PAB match-up statistics are slides 13–14.
  - *UCSC_Stats.*  The folder holds only the doc `Stats Talk`.  It gives the title, the abstract (two Bayesian problems; invites ideas from traditional and modern stats, ML and AI; README circulated beforehand) and the "where I need help" prongs: retrievals, faster FRB sampling, speeding up data assimilation.
  - *Other decks.*  The richest ocean-stats deck is `BING` (May 2026), with "Why Bayesian?", a corner plot and the degeneracy slides.  No FRB/zdm talk exists; the one ready-made figure is `fig_pillar_III` (the Macquart relation).  `UCSC_AM_2025` (Applied Math seminar) is a model for pitching methods to a quantitative audience.
- **This repo.**  `talks/wmko_2026/figures/` already has `fig01_inverse_problem.png`, `pace_moana.png`, `pab_infographic.png` and FRB host images that could be reused.
### 2026-10-15 (README #2: reviewed answers, read the papers, made the two sketches)

I reviewed the answers to Q1–Q18 and added round 2 (Q19–Q29, each with a default).  Two Claude Fable 5.1 subagents each read one paper in `context/papers/` and drew one sketch.  I reviewed both sketches and fixed what I found.  No git commands were run, the Google Doc has not been created yet (Q28), and the zdm and bing repos were only read.

*Files added.*
- `talks/ucsc_stats_2026/{figures,scripts,slides}/`, each with a `.gitkeep`.
- `scripts/fig_frb_sketch.py` → `figures/frb_sketch.png` (8 × 4.5 in, 200 dpi; patches only).
- `scripts/fig_ocean_sketch.py` → `figures/ocean_sketch.png` (8 × 4.5 in, 200 dpi).  It imports `bing.rt.rrs.calc_Rrs`, the L23 loader and bing's PACE noise table, read-only.
- `figures/sources.json`, with both figures listed as generated.

Run both with `conda run -n ocean14 python talks/ucsc_stats_2026/scripts/<script>.py`.

*My fixes after review.*
- FRB sketch: it said "6 telescopes" but listed 5, so I added FAST and tightened the rows, which also stopped "MeerKAT" being clipped by the box edge.  I gave the inset a white strip at the bottom and kept the localized points and DM ticks out of the legend and title.
- Ocean sketch: moved the "water alone" label in the absorption panel off the grey curve.
- One simplification is left: the ocean sketch's equation box labels the Gordon relation R_rs, though it strictly gives the sub-surface r_rs.  This is acceptable for a sketch.

*What I learned: FRB (`hoffmann2026.pdf`).*
- *Citation.*  Hoffmann, James, Prochaska, Pastor-Marazuela, Sharma & Connor, arXiv:2609.27282 (23 Sep 2026).
- *Sample.*  ~606 bursts from CHIME (492, in 6 declination bins), ASKAP/CRAFT ICS and Fly's Eye, Parkes, DSA, FAST and MeerKAT; 26 have redshifts after cuts.
- *Likelihood.*  The paper gives no equations; it defers to James+2022b and Hoffmann+2025.  The structure, checked against zdm, is an extended inhomogeneous Poisson likelihood on a 500 × 1400 (z, DM) grid per survey.  Localized bursts enter through λ_s(z,DM)/Λ_s and unlocalized ones through ∫λ_s dz.  There are p(SNR) terms, one normalization profiled across surveys, and Poisson terms for repeaters.
- *Priors and sampler.*  12 uniform priors (H0 restricted to the Planck–SH0ES 1σ range; F fixed).  emcee with 40 walkers × 2000 steps took about 1 week on OzSTAR; the paper calls more steps "not computationally feasible".
- *Degeneracies.*  n_sfr–α and R_min/R_max–R_γ; H0 is set by its prior.
- *Luminosity functions.*  Only the Gamma form is fit.  zdm implements 7 forms, so the model comparison is still open.

*What I learned: ocean (`bing.pdf`).*
- *Citation.*  Published, not just accepted: Prochaska & Frouin 2025, *Biogeosciences* 22, 4705–4728, doi:10.5194/bg-22-4705-2025.
- *Data and model.*  The fits use only the L23 simulations, with R_rs regenerated by the Gordon model (a "perfect forward model"), on 400–700 nm.  The noise models are for MODIS, SeaWiFS and PACE; noise is diagonal in practice, though Eq. 4 allows a full covariance C.
- *Sampler and model selection.*  emcee with 75k steps, keeping the last 7k.  BIC/AIC are computed from the LM χ²; the code has no MCMC-based evidence, which supports help item (b).
- *Main results.*  β_nw is set almost entirely by its prior, and a_ph is biased low and mostly an upper limit.  GIOP/GSM's fixed S_dg values lead to differences of >400% in a_ph(440) with χ²_ν ≈ 1.
- *Typos.*  The paper prints S_dg ~ U[0.1, 0.2] and the constant 1.17; the code uses [0.01, 0.02] and 1.7 (Q29).
- *Not in the paper.*  The PACE + BGC-Argo match-ups are unpublished follow-up in bing (`papers/biomass/`).

### 2026-10-15 (README #3: wrote the README, created the Google Doc)

A Claude Fable 5.1 subagent drafted `talks/ucsc_stats_2026/README.md` from the answers to Q1–Q29 and the facts gathered in #1–#2.  I reviewed the draft and fixed two points:
- DM_MW is estimated from Galactic models, not "known";
- F is now defined (how clumpy the intergalactic gas is).

I then created the Google Doc [UCSC Stats 2026 – README](https://docs.google.com/document/d/1I01EHa-QnfNHt_8evr-7-qYof5EsorYFDQxjgMdxsiw/edit) in `GDrive:Oceanography/Talks/2026/UCSC_Stats`.  It is unshared.  No git commands were run.

*How the Doc is built.*  `talks/ucsc_stats_2026/scripts/make_readme_html.py` converts `README.md` to HTML, and Drive `create_file` converts that HTML into a Doc.  The script handles only the Markdown subset this README uses, and with no flag it embeds the figures as JPEG data URIs.

*The figures are placeholders.*  Only the Drive connector is available (no Google Docs editor connector).  The Drive connector takes file content inline, so the 284 KB HTML with embedded figures would have had to be copied through the call by hand.  I uploaded the `--placeholders` version instead.  Each figure cell holds a highlighted "[Insert figure: …]" line, and **the two PNGs must be inserted by hand** (Insert → Image → Upload from computer, into the two top table cells).

*Checks.*
- I exported the Doc to PDF and looked at the pages.  Page 1 holds the title, summary, figure/caption table and all of the FRB section.  Page 2 holds the ocean section, code and papers, and contacts.
- The prose is ~3,500 characters, about 15% over the ~3,000 target.  The equations and footer push the Doc onto a second page, which Q27 allows.
- Equations are plain Unicode (Q26a).
- Docs' HTML import set the paragraphs with no space between them, and used Arial rather than Cambria for the equations.  Both can be adjusted by hand (Format → Line & paragraph spacing).

*Edits from here on.*  The Doc has to be edited by hand, or the Google Docs connector turned on.  A Drive-only change would mean creating a new file and a new link.
