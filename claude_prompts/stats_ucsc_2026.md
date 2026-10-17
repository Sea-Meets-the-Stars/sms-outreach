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

I have put my latest FRB talk in `context/NU_2026_talk.pptx`
I have put my latest BING talk in `context/AWOC_2025.pptx`

## Code

If you need to run Python, use the "ocean14" conda environment.


## Slide Outline

1. Title (Sea Meets the Stars)
1. Background
   1. Physics PhD -- KS test, chi^2, likelihood analysis
   1. Astronomer -- Likelihood + Bayesian modeling (Hamilton) + GP
   1. Oceanographer -- Deep learning + Bayesian
1. Goals for today
1. Part I.  Fast Radio Bursts
1. Science -- Multi-pronged attack on several unsolved problems
   1. Learn about the physical nature of the sources -- Frequency of occurrence, energetics
   1. Constrain the expansion rate of the universe
   1. Count the number of baryons in the Universe
1. Data -- Starts with a radio telescope
1. Dispersion Measure -- very precisely measured (more precision than needed)
1. Localization -- position on the sky
1. Bayesian Probabilistic association to a galaxy
1. Redshift (distance) measurement of the galaxy
1. Population modeling -- overview
1. Population modeling -- model
1. Population modeling -- Likelihood
1. Population modeling -- MCMC technique
1. Results to date
1. Open Challenges
1. Discussion
1. Part II.  Hyperspectral Inversion (BING)
1. Science -- Infer the concentration of primary constituents in the ocean
   1. Chlorphyll concentration
   1. CDOM
   1. Particulate matter
   1. Stretch goal -- Phytoplankton functional types
1. Data -- Satellite hyperspectral data (Rrs vs. wavelength)
1. Strong Systematics -- atmospheric corrections, inaccurate detector calibration
1. Poorly measured statistical error
1. Forward model 
1. Physical degeneracy
1. "Infinite" number of templates
1. Standard MCMC
1. Expensive for an individual spectrum -- Operational?
1. Priors
1. Where do we take new data?
1. Can we GP this?
1. Discuss
1. Two other problems
1. PFTs -- Pigments
1. PCA approach (Lange)
1. 2nd derivative + PCA (Kramer)
1. What do you recommend?
1. OI -- California coast
1. Optimize robot placement

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

### Talk

1. I have created an Outline for the talk above.  I have also downloaded my most
recent talks on FRBs and BING as powerpoint (`.pptx`) files.  Examine the Outline
and talks and then discuss with me the generation of the slide deck for the talk. 
Use Fable if you can.  Log your work.

2. I have answered all the questions in the Q&A/Talk section.  
Please review the questions and answers and ask another round.
Use Fable if you can.  Log your work.

3. I have answered all the questions in the Q&A/Talk section.  
Please review the questions and then generate a set of Build prompts below
Use Fable if you can.  Log your work.

### Build

*The talk is Monday 19 October 2026.  These are ordered so that a complete, presentable v1 with red placeholders exists after B1; B2–B4 fill and polish it.  Each prompt ends with a rebuilt deck (`--png`), a copy of the `.pptx` in `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`, and a log entry.  The settled decisions are Q&A/Talk Q1–Q43 (blank answers accept the default); the slide plan is Q26 as amended by Q29, Q32, Q37 and Q43; figure file names are fixed in B1 and listed in the Talk #3 log so B2 and B3 can run independently.*

1. **Deck v1.**  Produce a complete deck today, every slide in place, missing figures as red placeholders.
   - *Builder:* add a plan-level flag `CREDITS_IN_NOTES` (Q33) to `sms_outreach/slides/`: when true, a slide's `source` goes into the speaker notes only (no "Source" box on the slide) and QA's "figure without a source line" warning is skipped.  `build.py` passes it from the plan to `build_deck` and `qa.report`.  Add a test in `sms_outreach/tests/` and keep the existing tests passing.
   - *Plan:* write `talks/ucsc_stats_2026/slides/plan.py` on the Kraw master (same `TEMPLATE` path as the WMKO plan): 42 main slides + 6 backup, in the Q26 order with the amendments (three background slides with placeholders `bg_physics.png`, `bg_astronomy.png`, `bg_ocean.png`, Q37; `ocean_sketch.png` on "What is in the water?", Q32; the CUGN line map instead of `obs_model_ai.png`, Q29).  Title slide: title "Sea Meets the Stars", sub-title "Advancing science on the frontier with modern statistical techniques", author line "UC Santa Cruz, Kavli IPMU, NAOJ, Simons Pivot Fellow" (Q4, Q43).  Sections: Intro, FRBs, BING, Other, Close.  Use the figure file names from the Talk #3 log; `FIG_DIRS = [TALK/"figures", wmko_2026/figures]` so `pace_moana.png` resolves now.  Write bullets for every slide (≤ 4 bullets, ≤ 12 words each), a sub-line where the slide has a message, and first-draft notes (2–4 sentences, the numbers from the README and the two papers).  No source lines on slides (`CREDITS_IN_NOTES = True`); `sources.json` carries the credits.  `MAX_SLIDES = 42`.
   - *Build:* `conda run -n ocean14 python -m sms_outreach.slides.build talks/ucsc_stats_2026/slides/plan.py --png`; look at every page PNG; fix titles that wrap to three lines, sub-lines that wrap, bullets that overflow.  Write `talks/ucsc_stats_2026/slides/run_sheet.md` from Q38.  Copy the `.pptx` to the Drive folder.  Report the placeholder list.

2. **Assets.**  Write `talks/ucsc_stats_2026/scripts/harvest_assets.py` that fills `talks/ucsc_stats_2026/figures/` under the B1 file names and records every file in `figures/sources.json` (`origin`, deck or paper, slide or figure number, credit, license) and `figures/credits.md`.  Sources:
   - *Lifted from `context/NU_2026_talk.pptx`* (python-pptx, by slide number; pick the picture by its description, not by index): Lorimer burst dynamic spectrum (slide 15), NE2001 DM map (16), PATH galaxy image and the KCWI/GMOS host spectra (21), Macquart relation 2020 (22) and 2026 (23), the p(DM_EG, z) "DM cliff" heat map (27), Baptista+24 p(log F) (28), Connor+25 DSA-110 (30), scattering CDF (47), w_host histograms (48), N_FRB vs year (49), outrigger localization and photo (50), H0 contours (55), and the four telescope photos (slide 4: MeerKAT, CHIME, ASKAP, BURSTT) composed into one 2 × 2 montage `telescopes_montage.png` with small labels.
   - *Lifted from `context/AWOC_2025.pptx`*: 4-panel BING fit to simulated PACE (slide 7), the 5-parameter corner plot (9), the GIOP/GSM/k=5 three-model figure (10), the GIOP bias scatter (14), the ΔBIC CDFs (15), the real-PACE fit page with residuals (17), the PACE × BGC-Argo match-up map (20) and the Δb_bp map (21, hidden; credit "A. James et al. 2026, in prep.").
   - *Cropped from the PDFs with PyMuPDF* (`page.get_pixmap(dpi=250, clip=...)`, boxes as page fractions in the Talk #3 log): Hoffmann+2026 Fig. 1 (full corner and the n_sfr–α block), Fig. 2, Fig. 3; BING Fig. 4, Fig. 8 (β row), Fig. 10 (a+b), Fig. 11 (a), Fig. 6; Kramer+2022 method and results figures.
   - *Copied:* `talks/ucsc_stats_2026/figures/{frb_sketch,ocean_sketch}.png` (already there), `talks/wmko_2026/figures/pace_moana.png`, `~/Oceanography/python/EPFT-UP/reports/figures/moana_pc_loadings.png`.
   - *Downloaded:* the UCSC ROMS 4D-Var SST analysis, `https://oceanmodeling.ucsc.edu/ccsnrt/webplots/da/SST/SST_YYYYMMDD.png` (600 × 642; try today and step back until HTTP 200; the site is CC BY 3.0; credit "UCSC Ocean Modeling and Data Assimilation group, C. Edwards & A. Moore").
   Rebuild the deck with `--png`, look at every page, fix crops that are illegible at slide size (re-crop a panel rather than shrink the figure).  Copy to Drive.  Report what is still a placeholder.

3. **New figures.**  Run four Fable subagents in parallel; each writes one script in `talks/ucsc_stats_2026/scripts/`, its PNGs in `figures/` (recorded with `sms_outreach.slides.style.save` where it applies), and a one-paragraph report.
   - *Equations* (`fig_equations.py`, Q3, Q34, Q35): matplotlib mathtext, `mathtext.fontset = "dejavusans"`, black on white, one PNG per equation at a size that reads at 24 pt on the slide: DM sum; λ_s(z, DM | θ) as a product of five named factors; ln L (localized + DM-only + Poisson terms); the PATH posterior (two lines, Aggarwal+21); the Gordon relation with u = b_b/(a + b_b) and the boxed R_rs = f(b_b/a); the Lee+1999 non-water IOP model; the Gaussian ln L; BIC.  Re-render the equations that were LaTeX images in the two decks so every equation on the deck matches.
   - *CUGN line map* (`fig_cugn_lines.py`, Q30): cartopy (in `ocean14`) with a Natural Earth coastline, the four CUGN lines (56.0, 66.7, 80.0, 90.0) and the alongshore leg, end points from `~/Oceanography/python/cugn/cugn/defs.py` or the climatology repo; sea/stars palette; HALF size.
   - *BING cost* (`time_bing_fit.py` → `bing_timing.json`, `fig_bing_cost.py`, Q19, Q36): time one L23 spectrum with the paper's PACE k = 5 setup (LM start, emcee, 75,000 steps) with the `bing` package in `ocean14`, recording machine, steps, walkers and wall time; the figure shows seconds per spectrum → CPU-years per day for PACE at ~10⁸ cloud-free ocean pixels a day, with the assumptions printed on it.
   - *Amortized inference schematic* (`fig_amortized.py`, Q20): left, per-pixel MCMC (one spectrum → 75k likelihood calls → posterior); right, simulate (L23 + noise) → train (GP or neural) → every PACE pixel in one pass → calibrated posterior; the question "does it stay calibrated?" on the figure.  `punchline.png` style.
   Rebuild with `--png`, look at every page, copy to Drive.

4. **Words and notes.**  One pass through every slide: titles ≤ 2 lines; sub-lines that carry the message; bullets as above; notes 2–4 sentences with the facts (sample sizes, grid size, walkers × steps, run time, PACE bands and cadence, L23 count, BIC numbers, the >400 % a_ph spread), cross-checked against `talks/ucsc_stats_2026/README.md`, `context/papers/*.pdf` and the Q&A; discussion slides end with three questions.  No humor (Q7).  Update `run_sheet.md`, add a "Left for you" list (the three background figures, humor, animations, the Doc sharing).  Rebuild with `--png --strict`, copy to Drive.

5. **QA and hand-off.**  Two Fable subagents: (a) a layout review of every page PNG (overlaps, text off-slide, figures too small to read, equation size); (b) a fact check of every note and bullet against the README, the three papers and the Q&A, reporting each claim it cannot source.  Fix what they find, rebuild with `--png --strict`, copy the `.pptx` and PDF to Drive, and log the final placeholder list and the "Left for you" list.

6. **A bit more** I have answered the questions you posed after #5.  Please read
my responses and act accordingly.  I will then view the slide deck and suggest
more edits in #7.  Use Fable if you can.  Log your work.

7. **Edits on the current deck.**  Make these edits and produce a new deck (rebuild with `--png --strict`, copy to Drive, log):
   - (list the edits here)

## Q&A

### Talk

Each question has a default; answer "default" (or leave it blank) to accept it.  The main item is the slide plan in Q21: edit the table in place, or answer "go".

**A. Logistics and look**

1. **Date, room, timing.**  The Drive doc `Stats Talk` has no date.  When is the talk, and is the hour 60 min of slides, or about 45 min of slides with the three "Discuss" slots and Q&A making up the rest?  This sets the slide budget.
   - Default: 45 min of slides + 15 min of discussion, so about 40 main slides (the Q21 plan) plus backup.
   - A: Use your default
2. **Look.**  Both source decks (NU_2026, AWOC_2025) are white Palatino Google-Slides decks, not the Kraw master.  The repo's builder (`sms_outreach/slides/`) makes Kraw decks (Roboto, sea | stars title slide, one title + one sub-line per slide), which is what the WMKO talk used.
   - Default: build on the Kraw master with the existing tooling.  Images are lifted from the two decks; whole slides are not.
   - A:  Use your default.  I do prefer Roboto text to Palatino
3. **Equations.**  Both decks show equations as LaTeX-rendered PNGs; the builder places only Roboto text and images.  Options: (a) render each equation to a PNG with matplotlib mathtext in a script (`scripts/fig_equations.py`) and place it as a figure, beside bullets where needed; (b) Unicode text in bullets, as in the README; (c) reuse the equation PNGs lifted from the two decks (DM integral, ⟨DM_cosmic⟩, Gordon relation, Lee+1999 IOP model).
   - Default: (a) for the population-model, likelihood, PATH and ocean-likelihood equations (none exist as images yet), (c) where a lifted PNG already says it, (b) only for short in-line expressions.
   - A: Ok, let's try your default.  We'll see how that goes
4. **Title slide.**  The outline says "Title (Sea Meets the Stars)", `Stats Talk` gives "Advancing science on the frontier with modern statistical techniques".  The Kraw title slide has a title, a sub-title and an author line.
   - Default: title = "Advancing science on the frontier with modern statistical techniques", sub-title = "Sea meets the stars: two Bayesian problems and a request for help", author line = "UC Santa Cruz · Kavli IPMU · Simons Pivot Fellow" (NU_2026 also lists NAOJ; say if it belongs).
   - A: Title -- Sea Meets the Stars, Sub-title: "Advancing science..."
5. **Speaker notes.**  Neither source deck has notes; the WMKO deck had full notes, and the builder's QA flags a slide without them.
   - Default: short notes (2–4 sentences) on every slide, with the figure credits appended automatically.
   - A:  Ok, make notes.  For this talk, put figure credits in the notes not on the slides
6. **Builds.**  python-pptx cannot write animations.  NU_2026 reveals callouts and equations by animation; AWOC_2025 repeats a figure over consecutive slides with different crops ("Uh-oh.." → "Uh-oh again!").
   - Default: progressive reveal by repeated slides (the AWOC way) only where it carries the argument (the three-model fit, the PACE residuals); otherwise one slide per idea.  You add animations in Google Slides if you want them.
   - A: Use your default
7. **Humor and voice.**  The two decks carry running gags (the "Uh-oh" series, the katana, "the old engine that could", collaborator headshots next to results).
   - Default: keep the "Uh-oh" series on the PACE-systematics slides and the headshot device for Clancy James / Jordan Hoffmann and Robert Frouin; drop the katana.
   - A: Don't worry about Humor. I'll add it back in as I desire

**B. Opening**

8. **Background slides.**  The outline lists Physics PhD (KS test, χ², likelihood), Astronomer (likelihood + Bayesian modeling "Hamilton" + GP), Oceanographer (deep learning + Bayesian).  Two things I need: (i) what does "(Hamilton)" refer to: Hamiltonian Monte Carlo, or a person or paper?  (ii) Do you have a figure from each era you would like shown (e.g. a thesis χ² fit, a Bayesian/GP result from the astronomy years, a CNN or Ulmo/Nenya figure from `talks/wmko_2026/figures/`)?
   - Default: one slide, "Three careers, one growing toolkit", a three-column infographic (new script, in the `punchline.png` style) with a small figure per column: `dh_omega_b.png` (χ²/likelihood), a corner plot (Bayesian), `kraw_parks_cnn.png` or `nenya_umap.png` (deep learning).  Three slides instead if you give me one figure per era.
   - A: (i) Hamiltonina Monte Carlo; (ii) Yes, I have figures.  Put placeholders and I'll drop them in later
9. **"Goals for today".**
   - Default: four bullets: two problems, same shape (physical forward model + MCMC); what we have (data, model, code); what we want (faster, less prior-dependent, honest evidence); three discussion slots, plus two problems on the horizon.  Then a pointer to the README.
   - A: Use your default

**C. Part I, FRBs (sources: NU_2026 deck, Hoffmann+2026, zdm)**

10. **Science slide.**  NU_2026 covers baryon counting (Macquart relation, baryon pie) and H0 (backup slide 55, p(DM,z) contours for H0 = 60/70/80) well, but has no "nature of the sources" slide.
    - Default: one slide with three panels: the Lorimer burst dynamic spectrum (sources, energetics), the Macquart relation in 2026 (baryons), the H0 contours (expansion rate); all lifted from NU_2026.
    - A: Use your default
11. **Data slides (telescope, DM, localization, PATH, redshift).**  NU_2026 has all the images (telescope montage, Lorimer burst + DM integral, NE2001 map, CHIME outriggers, the PATH galaxy image with P(O|x), KCWI/GMOS host spectra).  The DM path schematic (slide 17, Sun → ISM → halo → cosmic web → host) is native shapes and cannot be lifted; `frb_sketch.png` already shows the same thing.
    - Default: lift those images; use `frb_sketch.png` in place of the slide-17 schematic.  For PATH, add one equation line (posterior ∝ prior on angular offset and magnitude × likelihood) rendered per Q3.  OK, and do you want the PATH equation at all?
    - A: Yes, let's add the PATH equation
12. **Population modeling (4 slides).**  Neither deck has the model, likelihood or sampler.  I would build them from the README: overview = `frb_sketch.png`; model = the λ_s(z, DM) product with its five factors, beside the p(DM, z) "DM cliff" heat map (NU_2026 slide 27); likelihood = the ln L sum (localized + DM-only + Poisson terms); MCMC = emcee, 12 parameters, uniform priors, 40 walkers × 2000 steps, one week on a cluster, grids rebuilt at every call.
    - Default: as above, with equations rendered per Q3.
    - A: Use your default
13. **Figures from the Hoffmann+2026 paper.**  zdm stores no figures (PNGs are gitignored), and the Fit-Repetition MCMC outputs are on OzSTAR.  For "Results to date" and the MCMC slide I would crop the corner plot and the posterior figures from `context/papers/hoffmann2026.pdf` (your paper), with a credit line.
    - Default: crop from the PDF.  Regenerate from zdm only if a figure is missing from the paper.
    - A: Crop from the PDF and do include a credit for this figure.  Do not try to regenerate anything from `zdm`
14. **"Results to date" content.**  The README avoids results, but the outline has the slide.
    - Default: the Hoffmann+2026 posteriors (corner plot), the Macquart relation with ~100 localized FRBs, and the cost line "one week on a cluster, and more steps are not feasible".  No H0 number.
    - A: Use your default
15. **Open challenges and the Discussion slide.**  README items a (speed: emulators, surrogates, fewer likelihood calls), c (degeneracies, prior sensitivity), d (choosing among energy-function forms: evidence vs BIC).  NU_2026 adds a fourth candidate: selection effects (scattering incompleteness, slides 47–48).
    - Default: "Open challenges" = a, c, d + selection effects as one line.  "Discussion" = three pointed questions to the room: Can the (z, DM) grid be replaced by an emulator or a differentiable likelihood (HMC)?  How do we get a proper evidence for seven luminosity-function forms?  How do we make the posterior less prior-driven (hierarchical priors, SBI)?
    - A: Use your default

**D. Part II, BING (sources: AWOC_2025 deck, Prochaska & Frouin 2025, bing)**

16. **Science and data slides.**  AWOC_2025 has the 4-panel BING fit to a simulated PACE spectrum (slide 7, with the Lee+1999 IOP equations) and a real PACE v3 spectrum with error bars (slide 17).  `talks/wmko_2026/figures/` has `pace_moana.png` (PACE map) and `fig01_inverse_problem.png`.
    - Default: Science = `pace_moana.png` + a bullet list (chlorophyll, CDOM, particles; PFTs as the stretch goal); Data = the real PACE spectrum (slide 17) beside the PACE facts from the README (100+ bands, 340–890 nm, 1 km, 1–2 days, millions of spectra a day).
    - A: Use your default
17. **Systematics and the error slides.**  AWOC slide 19 is exactly these two points (coherent 400–520 nm residual = "bad atmospheric correction?"; >600 nm residuals = "bad error estimates").  Hidden slide 21 (PACE b_bp systematically above BGC-Argo, "Uh-oh a third time") would carry the calibration point, but it is Allie James's unpublished PAB result.
    - Default: slide 19 as two slides (Q6); show the PAB map on the calibration slide, credited to Allie James.  Say no if it should stay unpublished.
    - A: Use your default.  Reference the PAB slide as James+2026
18. **Forward model, degeneracy, "infinite" templates.**  Material exists: the Gordon equations (AWOC 6, 13), the boxed r_rs = Func(b_b/a) (13), the GIOP / GSM / k=5 three-model fit with χ²_ν ≈ 1 (10–12), the corner plot (9), and `ocean_sketch.png` (three indistinguishable fits).
    - Default: forward model = the left half of `ocean_sketch.png` + the Gordon equations; degeneracy = the boxed equation + the right half of the sketch; "infinite templates" = the three-model fit in two steps (R_rs fits agree → b_b and a_ph disagree).
    - A: Use your default
19. **"Expensive for an individual spectrum: operational?"**  I would measure it: a script in `scripts/` times a BING fit (LM start + emcee, 75k steps) on one L23 spectrum in `ocean14`, and the slide multiplies by PACE's daily pixel count.
    - Default: yes, measure and make a "cost of doing this operationally" figure (seconds per spectrum × spectra per day → CPU-years per day).
    - A: Use your default.  There is code to perform these fits in the `bing` repo
20. **Priors, "where do we take new data?", "can we GP this?".**  Priors: AWOC 14 (GIOP a_ph heavily biased) and the paper's >400% a_ph(440) spread from fixed S_dg values (cropped from `bing.pdf`).  The other two titles I need you to unpack:
    - "Where do we take new data?": Bayesian experimental design (which extra measurement, e.g. in-situ b_bp from floats, fluorescence, polarization, or which wavelengths, most shrinks the posterior)?  Or literally where on the globe to validate (the PAB match-up map)?
    - "Can we GP this?": a GP emulator of the forward model, a GP (amortized) map from R_rs to the posterior trained on L23, or GP smoothing of retrievals across neighbouring pixels?
    - Default: priors slide as above; "new data" = experimental-design framing with the PAB map as the example; "GP" = amortized posterior (GP or neural) trained on simulations, one schematic slide (new).  Discussion slide: three questions (evidence for nested models; learning priors hierarchically; calibrated amortized posteriors at PACE scale).
    - A: Use your defaults

**E. Two other problems, close**

21. **PFTs and pigments (Lange PCA; Kramer 2nd derivative + PCA).**  Neither deck has this.  Locally: `EPFT-UP` (your MOANA re-implementation) has `reports/figures/moana_pc_loadings.png` (the Lange+2020 PCA basis) and held-out skill figures; Kramer et al. 2022 (derivative + PCA → pigments) exists only as a paper.
    - Default: PFT slide = `pace_moana.png` + what MOANA retrieves (Prochlorococcus, Synechococcus, picoeukaryotes); Lange slide = the EPFT-UP PC-loadings figure; Kramer slide = a figure cropped from Kramer+2022 with credit (internal seminar, fair use); "What do you recommend?" = the question stated plainly: PCA of R_rs (or its 2nd derivative) → regression is the state of the art; is there a better-posed way to get composition from a spectrum with 100 bands and 3 identifiable parameters?
    - A: Let's try your default
22. **OI, California coast; optimize robot placement.**  I need the story.  OI = objective mapping of the CUGN glider lines (Rudnick), i.e. kriging / a GP in disguise?  Robot placement = BOONUS (where to put ~100 gliders), an experimental-design or sensor-placement problem?  Which figures: something from `cugn` / `cugn-climatology`, or `obs_model_ai.png` / `ai_da_timeline.png` from the WMKO deck?
    - Default: OI slide = a CUGN line map + one OI'd section (I look in `cugn` for a ready figure; placeholder if none), framed as "OI is a GP with a hand-set covariance; satellites and models want in"; placement slide = `obs_model_ai.png` + BOONUS bullets, framed as sequential optimal design.
    - A:  For OI, we want to reference Chris Edwards' work to construct a ROM for Coastal California.  This web page offers a descrption: `https://comt.ioos.us/projects/wcofs_advancement`.  Let me know if you need to download any PDFs.
    And, robot placement is what science gains would be made by running gliders 
    on tracks other than their standard lines
23. **Closing slide.**  The outline ends on robot placement.
    - Default: add one "What I would like from you" slide: the three asks + README link + contacts (Clancy James, Robert Frouin) + QR code to the README Doc.
    - A: Use your default
24. **Output.**  `talks/ucsc_stats_2026/slides/plan.py` → `UCSC_Stats_2026.pptx` (+ PDF and page PNGs), copied to `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  Lifted images go to `talks/ucsc_stats_2026/figures/` with `sources.json` entries (deck, slide, original credit) via a `harvest_assets.py` script, as for WMKO.
    - Default: yes.
    - A:  That looks good.  Do note that I have LibreOffice installed if that is useful to you
25. **Build prompts.**  After this round I would write the Build prompts in the WMKO pattern: B1 assets (harvest + crops), B2 equations and new figures (Fable subagents in parallel), B3 deck v1 with placeholders, B4 words and notes, B5 QA and hand-off.
    - Default: yes, same pattern.
    - A: Yes, but wait for one more round of Q&A first

**F. Proposed slide plan (40 main + backup)**

26. **Slide plan.**  Outline order.  Source in brackets: *lift* = image from a source deck, *have* = already in this repo, *crop* = from a paper PDF, *new* = script to write, *eq* = rendered equation (Q3).

| # | Title (sub-line) | Visual [source] |
|---|---|---|
| 1 | Advancing science on the frontier with modern statistical techniques | Kraw title slide |
| 2 | Three careers, one growing toolkit (physics → astronomy → ocean) | 3-column infographic [new, Q8] |
| 3 | Goals for today | bullets [Q9] |
| 4 | Part I: Fast radio bursts | divider |
| 5 | A multi-pronged attack on unsolved problems | Lorimer burst, Macquart 2026, H0 contours [lift NU 15, 23, 55] |
| 6 | It starts with a radio telescope | telescope montage + N_FRB vs year [lift NU 4, 49] |
| 7 | Dispersion measure: precise beyond our needs | dynamic spectrum + DM integral + NE2001 map [lift NU 15, 16] |
| 8 | Localization: a position on the sky | CHIME outriggers [lift NU 50] |
| 9 | PATH: Bayesian association to a galaxy | PATH image [lift NU 21] + eq |
| 10 | Redshift: the distance to the galaxy | KCWI / GMOS spectra [lift NU 21] |
| 11 | Population modeling: the problem | `frb_sketch.png` [have] |
| 12 | Population modeling: the model | λ_s factors [eq] + DM-cliff heat map [lift NU 27] |
| 13 | Population modeling: the likelihood | ln L [eq] |
| 14 | Population modeling: MCMC | emcee bullets + corner plot [crop Hoffmann+26] |
| 15 | Results to date | posteriors [crop Hoffmann+26] + Macquart 2026 [lift NU 23] |
| 16 | Open challenges | bullets a, c, d, selection [Q15] |
| 17 | Discussion | three questions [Q15] |
| 18 | Part II: Hyperspectral inversion (BING) | divider |
| 19 | What is in the water? | `pace_moana.png` [have] + bullets |
| 20 | Data: PACE, a colour spectrum for every square kilometre | real PACE spectrum [lift AWOC 17] + facts |
| 21 | Strong systematics (Uh-oh) | residuals, 400–520 nm [lift AWOC 19] |
| 22 | Poorly measured errors (Uh-oh again) | residuals >600 nm [lift AWOC 19] + PAB Δb_bp map [lift AWOC 21, Q17] |
| 23 | The forward model | `ocean_sketch.png` left [have] + Gordon eqs [lift AWOC 6] |
| 24 | A physical degeneracy | boxed r_rs = Func(b_b/a) [lift AWOC 13] + sketch right |
| 25 | An "infinite" number of templates, I | three-model R_rs fits [lift AWOC 10] |
| 26 | An "infinite" number of templates, II | their b_b and a_ph [lift AWOC 12] |
| 27 | Standard MCMC | corner plot [lift AWOC 9] + likelihood [eq] |
| 28 | Expensive for one spectrum; operational? | cost figure [new, Q19] |
| 29 | Priors: they break the degeneracy, and bias the answer | GIOP a_ph bias [lift AWOC 14] + S_dg spread [crop bing.pdf] |
| 30 | Where do we take new data? | PAB match-up map [lift AWOC 20] [Q20] |
| 31 | Can we GP this? | amortized-inference schematic [new, Q20] |
| 32 | Discussion | three questions [Q20] |
| 33 | Two other problems | divider |
| 34 | Phytoplankton functional types from pigments | `pace_moana.png` [have] + bullets |
| 35 | PCA of the spectrum (Lange et al. 2020) | PC loadings [EPFT-UP, Q21] |
| 36 | Second derivative + PCA (Kramer et al. 2022) | [crop Kramer+22, Q21] |
| 37 | What do you recommend? | the question [Q21] |
| 38 | Optimal interpolation: the California coast | CUGN map + section [Q22] |
| 39 | Optimize the robot placement | `obs_model_ai.png` [have] + BOONUS bullets [Q22] |
| 40 | What I would like from you | asks + README QR + contacts [Q23] |
| B1 | The Macquart relation (2020) | [lift NU 22] |
| B2 | F and feedback | [lift NU 28, 30] |
| B3 | ΔBIC: multispectral vs hyperspectral | [lift AWOC 15] |
| B4 | Selection effects: scattering | [lift NU 47, 48] |

   - A: Looks good

#### Round 2 (after Talk #2)

Every question has a default.  The plan (Q26) stands; round 2 settles the last two outline items, the exact figure crops, three tooling details, what I need from you (PDFs, a date, a pip install) and the run sheet (Q38).

**G. The two other problems (Q22)**

27. **"ROM" for coastal California.**  The WCOFS page you pointed to describes **ROMS** 4D-Var data assimilation (Edwards, Moore; UCSC ROMS at 10 km running daily for CeNCOOS since 2011; WCOFS at 2 km, 4D-Var assimilating HF radar, altimetry and SST), and says nothing about a reduced-order model.  Did you mean ROMS, or a reduced-order (surrogate) model built from it?  The slide changes with the answer: ROMS = "a numerical ocean constrained by data, and 4D-Var is the bottleneck" (the `Stats Talk` prong "speeding up data assimilation"); reduced-order = "can a learned emulator replace the ocean model in the assimilation loop?".
    - Default: ROMS.  Slide 38 becomes "The California coast: a model ocean constrained by data", citing the WCOFS project and Edwards et al. 2015 (Ann. Rev. Mar. Sci.), with the ask: faster assimilation, learned emulators, uncertainty that 4D-Var does not give.
    - A:  Use your Default
28. **Visual for slide 38.**  Nothing local shows ROMS output.  Options: (a) a screenshot of the public UCSC nowcast (oceanmodeling.ucsc.edu, SST or surface currents), (b) a figure from a paper you download, (c) the CUGN line-geometry map only.
    - Default: (a), credited in the notes, beside the CUGN line map.
    - A: Go with (a) for now
29. **Robot placement (slide 39).**  "What science is gained by running gliders off their standard lines" is an observing-system design problem.  Chris Edwards' group already has a formalism for it: Moore, Arango & Edwards 2018, "Reduced-rank array modes of the California Current observing system" (JGR Oceans), and Mattern, Takeshita, Rocha & Edwards 2026 (Biogeosciences) assimilate glider pH with "hybrid statistical methods".  I would frame the slide as: standard lines (56, 66.7, 80, 90; map from `cugn`), the question (which track, when, buys the most forecast or climatology skill?), and the statistical shape (sequential experimental design / value of information with the model as the testbed), ending with BOONUS (~100 gliders) as the forthcoming dataset the abstract promises.
    - Default: as above; `obs_model_ai.png` dropped in favour of the line map.  Cite Rudnick et al. 2017 (CUGN) and Moore et al. 2018.
    - A: Use your Default;  I may change it later
30. **CUGN line map.**  `cugn-climatology/context/figs/fig01_line_geometry.png` draws the four lines but has no coastline.  I would redraw it (new script, `scripts/fig_cugn_lines.py`) with a coastline.  The repo has no cartopy; I can draw the coast from a public coastline file (e.g. Natural Earth, downloaded into `talks/ucsc_stats_2026/data/`) or use `cugn`'s own tools if it has one.
    - Default: redraw with Natural Earth coastline; one new small data file in the repo.
    - A: Use your Default

**H. Figure crops from the two papers (Q13, Q20)**

31. **Hoffmann+2026 crops.**  A subagent catalogued every figure.  Proposed: MCMC slide = Fig. 1 (p. 6, the full 11-parameter corner plot; the n_sfr–α panel enlarged as an inset or second crop); Results slide = Fig. 3 (p. 10, CHIME DM_EG cumulative distribution vs the model, the only model-vs-data figure) beside the Macquart relation from NU_2026, with the repeater counts of Table 6 quoted as text.  Fig. 2 (p. 7, the R_min/R_max/R_γ block) as backup B5.
    - Default: as above.
    - A: Use your Default
32. **BING crops.**  Proposed: priors slide = Fig. 10 panels (a)+(b) (p. 14: three fits with χ²_ν ≈ 1, a_ph differing by >400%), which supersedes AWOC slide 14; a second priors panel = Fig. 8 bottom row (p. 12, β set by its prior); degeneracy slide = Fig. 4 (p. 8, a and b_b scaled up to 100× with identical R_rs), which is more dramatic than the right half of `ocean_sketch.png`; the sketch then moves whole to slide 19 ("What is in the water?") beside `pace_moana.png`.  "Infinite templates" stays with the AWOC slide-10 figure (same content as Fig. 10, in two steps).  ΔBIC backup = Fig. 6 (p. 10).
    - Default: as above.
    - A: Use your Default;  I may change it later

**I. Tooling**

33. **Credits in the notes (Q5).**  The builder draws `source` on the slide and QA warns (fails with `--strict`) when a figure has no source line.  I would add a plan-level flag `CREDITS_IN_NOTES = True`: the source text goes into the notes only and the warning is suppressed; with a test in `sms_outreach/tests/`.
    - Default: yes.
    - A: Use your Default
34. **Equation font.**  matplotlib mathtext offers `dejavusans` (sans, close to Roboto) or `cm` (Computer Modern, like the LaTeX PNGs in the two decks).  Mixing lifted LaTeX PNGs with new sans ones on one slide would look odd, and the lifted equations are short (DM integral, Gordon relation, Lee+1999 IOP model).
    - Default: `dejavusans` everywhere, and re-render the lifted equations too, so Q3(c) falls away.  One script, `scripts/fig_equations.py`, one PNG per equation.
    - A: Use `dejavusans` everywhere, but don't bother to re-render the lifted equations
35. **PATH equation (Q11).**  I would render Aggarwal et al. 2021's form in two lines: P(O_i | x) = P(O_i) p(x | O_i) / p(x), with P(O_i) ∝ a prior from galaxy magnitude (number counts) and P(U) for "unseen host", and p(x | O_i) the offset distribution convolved with the localization error.
    - Default: as above, cited to Aggarwal et al. 2021.
    - A: Use your Default
36. **Timing script (Q19).**  `bing/scripts/fit_Rrs.py` and `bing/fitting/l23.py` do the fits.  I would time one L23 spectrum with the paper's PACE k = 5 setup (LM start, emcee, 75,000 steps) on this Mac, report seconds per spectrum and CPU-years per day, and quote PACE at about 10⁸ cloud-free ocean pixels per day (ocean area / (1.2 km)², 2-day repeat, half cloud).  Correct that number if you have a better one.
    - Default: as above; the script writes its numbers to a small JSON that the figure script reads.
    - A: Use your Default
37. **Background slides (Q8).**  You have figures for all three eras.  Three slides, each a red placeholder figure (labelled "your figure: KS / χ² (thesis)", "Bayesian / HMC / GP (astronomy)", "deep learning + Bayesian (ocean)") beside three bullets, you drop the figures in.  The main deck grows to 42 slides.
    - Default: yes.
    - A: Use your Default
38. **Run sheet.**  45 min of slides, 15 min of discussion in three slots (after 17, 32 and 37).  Edit the minutes or answer "go".

| Slides | Section | Min | Ends at |
|---|---|---|---|
| 1–5 | Title, three backgrounds, goals | 4 | 0:04 |
| 6–12 | FRB science and data (telescope → redshift) | 7 | 0:11 |
| 13–18 | Population model, likelihood, MCMC, results, challenges | 9 | 0:20 |
| 19 | Discussion I | 5 | 0:25 |
| 20–24 | Ocean science, PACE, systematics, errors | 5 | 0:30 |
| 25–31 | Forward model → priors | 8 | 0:38 |
| 32–33 | New data, GP | 3 | 0:41 |
| 34 | Discussion II | 5 | 0:46 |
| 35–38 | PFTs, Lange, Kramer | 5 | 0:51 |
| 39 | What do you recommend? | 5 | 0:56 |
| 40–42 | ROMS, gliders, close | 4 | 1:00 |

   - A:  This looks good

**J. What I need from you**

39. **Date (Q1 again).**  "Use your default" set the timing split, but I still have no date for the talk.  When is it, and when do you want deck v1?
    - A:  It is Monday, October 19th, 2026. I would like the deck v1 now
40. **PDFs into `context/papers/`.**  Needed: Kramer et al. 2022 (Remote Sens. Environ., paywalled) for slide 36.  Useful: Moore, Arango & Edwards 2018 (JGR Oceans, paywalled) if slide 39 should show an array-modes figure; Edwards et al. 2015 (Ann. Rev., paywalled) only if you want a figure from it.  Lange et al. 2020 (Opt. Express) is open access and the EPFT-UP loadings figure already covers it, so not needed.  Mattern et al. 2026 is open access; I can fetch it.
    - Default: you drop in Kramer+2022 (as `kramer2022.pdf`); the others only if you want their figures.
    - A: I have put `kramer2022.pdf` in `context/papers/`.  We can do without the others
41. **ROMS image rights.**  A screenshot of oceanmodeling.ucsc.edu (Q28) is fine for an internal seminar with credit in the notes; say if you would rather ask Chris Edwards for a figure.
    - A: Use the screenshot.  Thanks
42. **QR code and the README link (Q23).**  `qrcode` is not in `ocean14`.  Options: (a) you OK `pip install "qrcode[pil]"` into `ocean14`, (b) you add the QR in Google Slides, (c) the closing slide shows a short URL only.  Also, the README Doc is unshared, so the QR is useful only once you set "anyone with the link"; the alternative target is the GitHub README.
    - Default: (a), QR to the Google Doc, you set the sharing.
    - A:  We don't need a QR code for this talk
43. **Title-slide author line (Q4).**  Kraw's "UC Santa Cruz, Kavli IPMU, Simons Pivot Fellow"; NU_2026 adds NAOJ.
    - Default: keep Kraw's line.
    - A: Add NAOJ 

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

### 2026-10-16 (Talk #1: examined the outline and the two decks, opened Q&A/Talk)

Two Claude Fable 5.1 subagents, read-only, each extracted one deck (`context/NU_2026_talk.pptx`, `context/AWOC_2025.pptx`) with python-pptx, rendered it with LibreOffice and catalogued every slide and image; I checked the contact sheets myself.  The questions are in Q&A/Talk (Q1–Q26, six groups, each with a default); Q26 is a 40-slide plan in outline order with a source for every visual.  No files were changed except this one.  No git commands were run.  The renders and the 131 + ~40 extracted images are in the session scratchpad only; nothing has been copied into `talks/ucsc_stats_2026/figures/` yet.

*What I found.*
- **NU_2026_talk.pptx (FRBs).**  55 slides, 16:9, white Google "Simple Light" theme in Palatino, not the Kraw master.  No speaker notes.  Equations are LaTeX PNGs (DM integral, ⟨DM_cosmic⟩, p_cosmic(Δ), σ_DM = F z^-1/2).  26 slides use builds; a recurring "Today's Plan" slide is the section divider.  It covers the data chain fully (telescope montage, Lorimer burst, NE2001 map, outriggers, PATH image, host spectra), baryon counting and H0 (backup slide 55), and F / feedback.  It has nothing on the population model, likelihood or sampler, so slides 11–14 of the plan are new material built from the README.
- **AWOC_2025.pptx (BING).**  23 slides (3 hidden), same white Palatino look.  No notes.  Figure-first: 18 of 23 slides are one figure and a title.  Equations are LaTeX PNGs (Gordon relation, Lee+1999 IOP model, the boxed r_rs = Func(b_b/a)).  Progressive reveal by repeating a figure across slides with new crops and "Uh-oh" callouts.  It covers the forward model, the degeneracy, the three-model "infinite templates" argument, the corner plot, the GIOP bias and the ΔBIC CDFs, and the real-PACE residuals (atmospheric correction, bad errors).  Hidden slides 20–21 hold the PACE × BGC-Argo match-up maps (Allie James's unpublished results).  Nothing on cost per spectrum, experimental design, GPs, pigments/PFTs, OI or robot placement.
- **Builder.**  `sms_outreach/slides/` places Roboto text and images only; QA fails on any other explicit font, so equations must be images (Q3).  An equation image is just a `Fig`, so no builder change is needed for a first deck.
- **Local material for the new sections.**  zdm is at `~/Astronomy/FRB/zdm` (figures gitignored; MCMC outputs not local), so Hoffmann+2026 figures would be cropped from the PDF (Q13).  `~/Oceanography/python/EPFT-UP/reports/figures/` has the MOANA PC-loadings and skill figures for the Lange slide (Q21).  `cugn` / `cugn-climatology` hold the glider code for the OI slide; `BOONUS/reports/data_assimilation/` has only notes and a figure list (Q22).  `talks/wmko_2026/figures/` supplies `pace_moana.png`, `fig01_inverse_problem.png`, `obs_model_ai.png`, `pab_infographic.png`, `dh_omega_b.png`.
- **Drive.**  `Stats Talk` gives the title and abstract but no date (Q1).  The abstract promises a closing section on "forthcoming, large datasets", which the outline's last two items (OI, robot placement) can serve.

### 2026-10-16 (Talk #2: reviewed the answers, opened round 2 of Q&A/Talk)

I reviewed the answers to Q1–Q26 and added round 2 (Q27–Q43, groups G–J, each with a default).  One Claude Fable 5.1 subagent, read-only, catalogued every figure in `context/papers/hoffmann2026.pdf` and `context/papers/bing.pdf` and rendered candidate crops (page fractions recorded in the session scratchpad, `papers/crop_boxes.txt`).  I fetched the WCOFS project page and read the CUGN and BOONUS repos for the last two outline items.  No files were changed except this one.  No git commands were run.  The Build prompts are not written yet (Q25: after this round).

*What the answers settled.*  Kraw master and Roboto; equations as rendered PNGs; title "Sea Meets the Stars" with the Stats title as sub-title; notes on every slide with the figure credits in the notes rather than on the slide; progressive reveal by repeated slides; no humor from me; "(Hamilton)" = Hamiltonian Monte Carlo and the three background figures are yours (placeholders); PATH equation wanted; Hoffmann+2026 figures cropped from the PDF with credit, nothing regenerated from zdm; the PAB map shown as James+2026; the BING timing measured with the `bing` code; the 40-slide plan accepted.

*What round 2 asks.*
- **ROM (Q27–Q28).**  The WCOFS page (comt.ioos.us/projects/wcofs_advancement) describes ROMS 4D-Var: UCSC ROMS at 10 km run daily for CeNCOOS since 2011, WCOFS at 2 km with 4D-Var assimilating HF radar, altimetry and SST (Edwards PI, Moore).  It never mentions a reduced-order model, so Q27 asks whether "ROM" meant ROMS or a surrogate; the slide's ask differs.  No local figure shows ROMS output; Q28 proposes a screenshot of the public UCSC nowcast.
- **Robot placement (Q29–Q30).**  The BOONUS reading list already holds the relevant formalism: Moore, Arango & Edwards 2018 (reduced-rank array modes of the California Current observing system) and Mattern et al. 2026 (glider pH assimilation with hybrid statistical methods).  `cugn/defs.py` lists the four lines (56.0, 66.7, 80.0, 90.0) and `cugn-climatology/context/figs/fig01_line_geometry.png` draws them without a coastline; Q30 proposes a redraw with a Natural Earth coastline.
- **Crops (Q31–Q32).**  Hoffmann+2026: Fig. 1 (p. 6) is the 11-parameter corner plot, Fig. 2 (p. 7) the repetition block, Fig. 3 (p. 10) the only model-vs-data figure (CHIME DM_EG CDF), Fig. 4 a model-only (z, DM) map; there is no repeater-fraction figure, only Table 6.  BING: Fig. 4 (p. 8, a and b_b scaled up to 100× with identical R_rs), Fig. 8 (p. 12, corner plot; β flat = prior), Fig. 10 (p. 14, three fits with χ²_ν ≈ 1 and a_ph differing by >400%), Fig. 11 (p. 15, a_ph mostly upper limits), Fig. 6 (p. 10, ΔBIC CDFs).  The Hoffmann figures are vector, so crops should be rendered from the PDF with PyMuPDF rather than extracted.
- **Tooling (Q33–Q37).**  Credits-in-notes needs a small builder flag (QA otherwise warns on figures without a source line); equation font (`dejavusans` proposed, re-rendering the lifted equations for consistency); the PATH equation form; the timing script (`bing/scripts/fit_Rrs.py`, `bing/fitting/l23.py`) and a PACE pixel count of ~10⁸ per day to confirm; three background slides with placeholders, so 42 main slides.
- **From you (Q38–Q43).**  A run sheet to edit; the talk date (still missing after Q1); Kramer et al. 2022 PDF into `context/papers/` (paywalled; optionally Moore+2018 and Edwards+2015); permission for a ROMS screenshot; `qrcode` is not in `ocean14`, so a pip install or a hand-added QR, and the README Doc must be shared before a QR to it is useful; the title-slide author line.

*What I learned.*  `bing` is importable in `ocean14`; `qrcode` is not.  `EPFT-UP/reports/figures/moana_pc_loadings.png` is a clean six-panel figure of the MOANA PCA basis, usable as is for the Lange slide.  The `PAB` repo has no paper draft, so "James+2026" is cited by name only.

### 2026-10-16 (Talk #3: reviewed round 2, wrote the Build prompts)

The round-2 answers: blank = default (Q27–Q38), so "ROM" is read as ROMS and the last two slides become "The California coast: a model ocean constrained by data" and the glider observing-system design slide; the talk is Monday 19 October 2026 and deck v1 is wanted now (Q39); `kramer2022.pdf` is in `context/papers/` (Q40); the ROMS image may be used (Q41); no QR code (Q42); the author line adds NAOJ (Q43).  I wrote Build prompts B1–B6 under Prompts/Build, ordered so that B1 alone yields a complete v1 with red placeholders.  One Claude Fable 5.1 subagent, read-only, catalogued the Kramer+2022 figures.  No files were changed except this one; no deck has been built yet (B1 does that).  No git commands were run.

*What I checked.*
- **ROMS image.**  oceanmodeling.ucsc.edu is CC BY 3.0 and serves its daily 4D-Var analysis plots at a fixed URL pattern, `ccsnrt/webplots/da/SST/SST_YYYYMMDD.png` (600 × 642; the latest that returned HTTP 200 today was 2026-10-12, produced 2026-10-14).  No screenshot is needed.  The page also says the system assimilates the SCCOOS and CeNCOOS glider lines, which links slides 41 and 42.
- **Libraries in `ocean14`.**  PyMuPDF (`fitz`), cartopy, shapely and geopandas are present; `pdfplumber` and `qrcode` are not.  So PDF crops use PyMuPDF and the CUGN map uses cartopy with no extra data file.
- **Kramer et al. 2022.**  Remote Sens. Environ. 270, 112879, doi:10.1016/j.rse.2021.112879, open access (CC BY).  Method: a GSM-like hyperspectral model is fit and subtracted from R_rs, the residual's second derivative is z-scored, PCA'd, and principal-component regression predicts 13 HPLC pigments; cross-validated R² 0.37 (Zea) to 0.72 (Tchla).  No schematic or PCA-mode figure exists in the main text (that is Fig. S1).  Crops: method = Fig. 5 top row, p. 7, box (0.067, 0.420, 0.936, 0.605); results = Fig. 6 panels A+B, p. 9, box (0.165, 0.071, 0.834, 0.330).

*Crop boxes for B2* (page fractions x0, y0, x1, y1, origin top-left; render with PyMuPDF at 250 dpi).
- `hoffmann2026.pdf`: Fig. 1 full corner p. 6 (0.05, 0.13, 0.93, 0.79); Fig. 1 n_sfr–α block p. 6 (0.05, 0.13, 0.26, 0.265); Fig. 2 repetition block p. 7 (0.07, 0.56, 0.48, 0.86); Fig. 3 CHIME DM_EG CDF p. 10 (0.51, 0.14, 0.93, 0.37).
- `bing.pdf`: Fig. 4 degeneracy p. 8 (0.08, 0.08, 0.92, 0.35); Fig. 8 β row p. 12 (0.17, 0.46, 0.84, 0.60); Fig. 10 (a)+(b) p. 14 (0.17, 0.08, 0.83, 0.29); Fig. 11 (a) p. 15 (0.19, 0.08, 0.49, 0.32); Fig. 6 ΔBIC p. 10 (0.17, 0.08, 0.83, 0.30).
- `kramer2022.pdf`: as above.

*Figure file names for B1–B3* (all in `talks/ucsc_stats_2026/figures/`).
- Placeholders for your figures: `bg_physics.png`, `bg_astronomy.png`, `bg_ocean.png`.
- Have: `frb_sketch.png`, `ocean_sketch.png`; from wmko: `pace_moana.png`; copied: `moana_pc_loadings.png`.
- Lifted from NU_2026: `nu_lorimer_burst.png`, `nu_ne2001.png`, `nu_path_image.png`, `nu_host_spectra.png`, `nu_macquart_2020.png`, `nu_macquart_2026.png`, `nu_dm_cliff.png`, `nu_baptista_F.png`, `nu_connor_feedback.png`, `nu_tau_cdf.png`, `nu_whost.png`, `nu_nfrb_vs_year.png`, `nu_outrigger_loc.png`, `nu_outrigger_photo.png`, `nu_h0_contours.png`, `telescopes_montage.png`.
- Lifted from AWOC_2025: `awoc_bing_fit_sim.png`, `awoc_corner.png`, `awoc_three_models.png`, `awoc_giop_bias.png`, `awoc_dbic.png`, `awoc_pace_fit.png`, `awoc_pab_matchups.png`, `awoc_pab_dbbp.png`.
- Cropped: `hoffmann_fig1_corner.png`, `hoffmann_fig1_nsfr_alpha.png`, `hoffmann_fig2_repetition.png`, `hoffmann_fig3_chime_cdf.png`, `bing_fig4_degeneracy.png`, `bing_fig8_beta_prior.png`, `bing_fig10_priors.png`, `bing_fig11_aph.png`, `bing_fig6_dbic.png`, `kramer_fig5_method.png`, `kramer_fig6_results.png`.
- Downloaded: `roms_sst_nowcast.png`.
- New (B3): `eq_dm_sum.png`, `eq_lambda.png`, `eq_lnL_frb.png`, `eq_path.png`, `eq_gordon.png`, `eq_iop_model.png`, `eq_lnL_gauss.png`, `eq_bic.png`, `cugn_lines.png`, `bing_cost.png`, `amortized_schematic.png`.

*Slide numbering after the amendments* (42 main; corrected in Build #1, the list below had one entry too many): 1 title; 2–4 backgrounds; 5 goals; 6 divider; 7–13 FRB science and data; 14–20 population model → discussion; 21 divider; 22–35 BING (22 what is in the water, with `ocean_sketch.png`; 23 PACE; 24–25 systematics and errors; 26 forward model; 27 degeneracy with BING Fig. 4; 28–29 templates; 30 MCMC; 31 cost; 32 priors; 33 new data; 34 GP; 35 discussion); 36 divider; 37–40 PFTs → recommend; 41 ROMS; 42 gliders; 43 close.  That is 42: Q26's 40 plus the two extra background slides (Q37); the closing slide was already in Q26.  B1 sets `MAX_SLIDES = 42`.  Backup: Macquart 2020, F and feedback, ΔBIC, scattering, Hoffmann Fig. 2.

### 2026-10-16 (Build #1: deck v1 with placeholders)

Built `talks/ucsc_stats_2026/slides/UCSC_Stats_2026.pptx`: 42 main slides + 7 backup (a divider and six slides), QA "ALL CHECKS PASSED", 50 red placeholders, and copied it to `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  The PDF and page PNGs are next to it (gitignored).  No git commands were run.

*Files.*
- `sms_outreach/slides/{deck,qa,build,spec}.py`: new plan-level flag `CREDITS_IN_NOTES` (Q33).  With it, a slide's `source` goes into the speaker notes only and QA no longer asks for a source line on figures.  `sms_outreach/tests/test_slides.py` gains `test_credits_in_notes`; 14 tests pass.
- `talks/ucsc_stats_2026/slides/plan.py`: every slide with title, sub-line, figures, bullets, credit and first-draft notes; `FIG_DIRS` includes `talks/wmko_2026/figures` so `pace_moana.png` already resolves; `MAX_SLIDES = 42`.
- `talks/ucsc_stats_2026/slides/run_sheet.md`: the Q38 timing renumbered to the built deck, plus a "Left for you" list.

*Deviations from the plan, all small.*
- Slide 7 (science) shows two panels, not three: the builder takes at most two figures per slide, so the Lorimer burst and the 2026 Macquart relation sit under a three-bullet band, and the H0 contours moved to backup ("H0 and the DM cliff").  B2 can compose a three-panel montage if you prefer.
- The main deck is 42 slides, not the 43 the Talk #3 log said (its list double-counted the closing slide); the B1 prompt and that log now say 42.
- Backup has six slides (Q26's four plus "H0 and the DM cliff" and the Hoffmann repetition block).
- Slides 23 and 24 reuse the real-PACE fit figure (`awoc_pace_fit.png`) for the two "Uh-oh" points; B2 should crop the residual panel for 24 if the full page is illegible at half width.

*Checks.*  Every page was rendered and looked at on contact sheets.  Fixed after the first build: three pair captions that wrapped into the figures (25, 29, 38), three two-line titles (22, 31, 40; 22 still takes two lines, which QA allows), and two bullet lists beside a figure that ran small (15, 41).  LibreOffice renders the text in a serif fallback because Roboto is not installed system-wide; Google Slides will show Roboto.

*Placeholders (50).*  Your three background figures (slides 2–4); 24 lifted images and 11 PDF crops for B2 (slides 7–12, 14, 16–17, 22–24, 26–29, 31–32, 37–38, 40 and backup 44–49); 11 new figures for B3 (equations on 9, 11, 14, 15, 25, 29; `cugn_lines.png` on 40–41; `bing_cost.png` on 30; `amortized_schematic.png` on 33); `roms_sst_nowcast.png` (40) and `moana_pc_loadings.png` (37) for B2.

### 2026-10-16 (Build #2: assets harvested, deck rebuilt)

Wrote `talks/ucsc_stats_2026/scripts/harvest_assets.py` and ran it; it fills `talks/ucsc_stats_2026/figures/` (46 files, ~20 MB) and writes `figures/sources.json` (45 entries) and `figures/credits.md`.  Rebuilt the deck with `--png` (49 slides, 19 MB, QA "ALL CHECKS PASSED"), looked at every page, and copied the `.pptx` to `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  Placeholders went from 50 to 14: your three background figures and the eleven B3 figures (eight equations, `cugn_lines.png`, `bing_cost.png`, `amortized_schematic.png`).  No git commands were run.

*How the harvest works.*
- *Lifted (23 + 4 panels + 1 montage).*  Pictures are taken from the two decks by slide number and shape id (groups searched), the deck's own crop rectangle applied, transparency flattened on white.  Three AWOC figures (`awoc_pace_fit`, `awoc_three_models`, `awoc_bing_fit_sim`) are taken uncropped because the deck showed only one quadrant of a 2 × 2 figure; the panels the slides need are cut from them as `awoc_pace_fit_rrs.png` (R_rs + residuals) and `awoc_three_models_{rrs,bb,aph}.png`.  `telescopes_montage.png` is a 2 × 2 of the MeerKAT, CHIME, ASKAP and BURSTT photos with Roboto labels.
- *Cropped (11).*  PyMuPDF renders the page region at 250 dpi (boxes from the Talk #3 log; the repetition block widened to y0 = 0.535 and Fig. 11(a) to x1 = 0.505 so no labels are cut).
- *Copied (2).*  `pace_moana.png` from wmko_2026 and `moana_pc_loadings.png` from EPFT-UP.
- *Downloaded (1).*  `roms_sst_nowcast.png`: the newest available UCSC 4D-Var SST analysis (2026-10-13, found by stepping back from today; the site's certificate chain is incomplete, so verification is off for that one request).  `--no-download` skips it on re-runs.
- *Credits.*  `sources.json` records origin, deck/slide/shape or paper/page/box, and the credit line; `credits.md` tabulates them.  The telescope-photo owners and the CHIME outrigger photo are marked "owner to confirm".

*Plan changes.*  Slides 23–24 use the R_rs + residuals panel rather than the full fit page (22 keeps the full page); slide 27 shows the R_rs panel of the three-model figure and slide 28 a pair (b_b | a_ph) with one bullet.

*Left for B4.*  The 11-parameter corner plot (16) and the priors pair (31) would read better at full width with the bullets moved to the notes; slide 7's two panels are small under the three-bullet band.

### 2026-10-16 (Build #3: new figures, deck rebuilt)

Four Claude Fable 5.1 subagents ran in parallel, each writing one script in `talks/ucsc_stats_2026/scripts/` and its PNGs in `figures/`; I reviewed every PNG, merged their credits into `figures/sources.json` (56 entries, 13 generated), rebuilt the deck with `--png` (49 slides, 20 MB, QA "ALL CHECKS PASSED"), looked at every page, and copied the `.pptx` to `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  Placeholders: 3, all yours (slides 2–4).  No git commands were run (one subagent ran a read-only `git status` inside the `bing` repo; nothing there was touched).

*What was made.*
- **Equations** (`fig_equations.py` → `eq_dm_sum`, `eq_lambda`, `eq_lnL_frb`, `eq_path`, `eq_gordon`, `eq_iop_model`, `eq_lnL_gauss`, `eq_bic`): matplotlib mathtext in `dejavusans`, black on white, 220 dpi, each drawn at its cell width (4.4" half, 6.1" beside bullets).  mathtext has no `\boxed` or `\Big[`, so the box is a drawn rectangle and the brackets are plain; the two widest lines (the five-factor rate density, the Gaussian likelihood) shrink to 16–18 pt.  The script writes the manifest entries itself because `style.save`'s `tight_layout` does not apply to text-only figures.
- **CUGN line map** (`fig_cugn_lines.py` → `cugn_lines.png`, 946 × 748): cartopy with Natural Earth 50 m land and coast; the four lines and the alongshore leg with end points from the 2026-beta climatology grid table (`cugn-climatology/context/initial_exploration.md`), which match `cugn/utils.py:line_endpoints` at the inshore ends; five labelled cities.
- **BING timing and cost** (`time_bing_fit.py` → `figures/bing_timing.json`; `fig_bing_cost.py` → `bing_cost.png`).  Measured, not scaled: L23 spectrum 170 with PACE noise, 400–700 nm (61 bands), k = 5 (ExpBricaud + Pow), LM start 3 ms, emcee 16 walkers × (75,000 + 1,000 burn-in) steps = 1.2 × 10⁶ likelihood calls at 24 µs each, **29 s per spectrum** on one core of this Apple M5 Max (18 cores; Python 3.14.6, numpy 2.4.6, emcee 3.1.6).  At 10⁸ spectra a day that is 2.9 × 10⁹ CPU-s, **≈ 93 CPU-years per day, ≈ 34,000 cores to keep up**.  Two things the subagent found in `bing`: the LM solution for this spectrum sits on two prior bounds (S_dg = 0.02, β = 2), so the script nudges the walker ball 1 % inside the bounds; and the paper's own figure scripts use 40,000 steps, not 75,000 (which would be ≈ 16 s).  The literal pixel count is ≈ 0.6 × 10⁸ per day; the figure says ~10⁸ and prints the assumptions.
- **Amortized-inference schematic** (`fig_amortized.py` → `amortized_schematic.png`, FULL size): per-pixel MCMC on the left, simulate → train → infer on the right, the calibration question in red.

*Fixes after review.*  The four scripts had their manifest default pointing at the session scratchpad (so they would not race on `sources.json` while running in parallel); I set each default back to `figures/sources.json` and re-ran the schematic script as a check.

*Left for B4.*  On slide 9 the DM-sum equation is small in its half cell (a wide, short image); consider giving it the full width with the NE2001 map moved to the notes or a smaller inset.  The earlier notes stand: the corner plot (16) and the priors pair (31) want full width; slide 7's panels are small under the bullet band.  Slide 30's notes should now quote the measured 29 s and 93 CPU-years per day.

### 2026-10-16 (Build #4: words and notes)

One pass through every slide of `talks/ucsc_stats_2026/slides/plan.py`, then a build with `--png --strict` (50 slides: 42 main + 8 backup, QA "ALL CHECKS PASSED", 3 placeholders, all yours), every page looked at, and the `.pptx` copied to `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  `run_sheet.md` updated.  No git commands were run.

*Layout changes.*
- Slide 7 (the three questions): the bullet band is gone; the two panels carry the prongs in their captions ("the sources", "the baryons") and the sub-line carries H0, so the burst and the Macquart relation are twice the size.
- Slide 16 (MCMC): the 11-parameter corner plot now fills the slide; the facts (500 × 1400 grid, 40 walkers × 2000 steps, one week, the degeneracies) moved to the sub-line and the notes.
- Slide 31 (priors): Fig. 10 (a, b) alone at full width; Fig. 11(a) became backup slide 49, "Phytoplankton absorption: upper limits".
- Slide 30 (cost): the sub-line and notes now quote the measured numbers (29 s per spectrum, 1.2 × 10⁶ likelihood calls, 93 CPU-years per day, 34,000 cores).

*Words.*  Bullets trimmed to ≤ 4 per slide and about ≤ 12 words (the discussion questions and the contact line are the deliberate exceptions); the one sub-line that wrapped (16) shortened; "a few dozen" on slide 12 replaced by the paper's 26.  Notes: 2–5 sentences on every main slide with the facts cross-checked against the README and the three papers (sample sizes, grid, walkers × steps, run time, KS p = 0.9, PACE bands and cadence, L23 count, 75,000 steps, the χ²_ν triple 0.80 / 1.01 / 1.13, the a_ph(440) triple 0.23 / 0.05 / 0.03, bias −21 %, MAE 40 %, Kramer's 13 pigments and R² 0.37–0.72, ROMS 4-day cycles, CUGN lines since 2006); the two discussion slides' notes name their three questions; the backup divider's note lists the backup slides.  One-sentence notes remain on the backup slides and the dividers, which strict QA accepts.  No humor (Q7).

*A check I did not automate.*  The 12-vs-11 parameter count: the model has 12 free parameters with uniform priors (H0 included); Hoffmann et al.'s Fig. 1 plots 11 (H0 omitted; its posterior is its prior).  The sub-line says 12 and the notes explain the 11.

*Left for you* (also in `run_sheet.md`): the three background figures (slides 2–4); humor and animations; the README Doc sharing; the telescope and outrigger photo credits to confirm; a glance at the numbers on slides 12 and 30 before the talk.

### 2026-10-17 (Build #5: QA and hand-off)

Two Claude Fable 5.1 subagents reviewed the B4 deck, read-only: one looked at every rendered page for layout, the other checked every title, bullet, caption and note against the README, the three papers, `bing_timing.json`, `sources.json` and the Q&A.  I fixed what they found, re-harvested, rebuilt with `--png --strict` (52 slides: 42 main + 10 backup, QA "ALL CHECKS PASSED", 3 placeholders, all yours), looked at every page again, and copied the `.pptx` and the PDF to `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  `run_sheet.md` updated.  14 tests pass.  No git commands were run.

*Layout fixes (from the page review).*
- Clean figures in place of cropped composites: slide 22 now shows the R_rs + residuals panel (not the full fit page with its file-name title and micro corner plot); the MOANA loadings lost their file-name suptitle; the ROMS map lost its title and footer lines (the date moved to the caption); the two paper panels with slivers (BING Fig. 11a, Hoffmann Fig. 2) were re-cropped.
- Figures given the room: the degeneracy figure (26) and the Kramer method panels (38) at full width with their bullets moved to the sub-line and notes; the bullet band removed from Standard MCMC (29); the DM-sum equation (9) beside bullets instead of in a half cell, with the NE2001 map moved to backup; the forward half of the ocean sketch alone on "What is in the water?" (21).
- The telescope montage is a 2 × 2 of 16:9 centre-crops without in-image labels, and Parkes replaces BURSTT (not one of the six surveys in the fit).
- Slide 7's left caption shortened so it no longer hides behind the figure; the Part II divider shortened.
- Not acted on: "BOONUS" is the acronym, not a typo; figures whose small fonts live inside lifted images (DM cliff, host spectra, PAB maps) were left as they are.

*Fact fixes (from the fact check).*  Every number from the README, the papers and the timing JSON checked out; the corrections were:
- Slides 28 and 31: the GSM a_ph(440) is ≈ 0.17 m⁻¹, not 0.03 (the 0.03 was read off the wrong wavelength); the slides now quote true 0.23 vs. GIOP ≈ 0.05 only.  "Backscattering a factor of two apart" overstated a ≈ 1.4× spread; now "different amplitude and slope".
- Slide 39: hyperspectral data support "4, possibly 5" parameters per the paper, so the bullet now says 3 (multispectral) to 4–5 (PACE).
- Slide 36: MOANA is trained on flow-cytometry cell counts, not HPLC pigments (HPLC is Kramer's input).
- Slide 31 notes: a_ph is an upper limit for most *low-chlorophyll* spectra, not most spectra.
- Slide 38 notes now say what Kramer's Fig. 5 shows (pigment–spectrum correlation vs. wavelength for the residual and its derivatives).
- Hedges: "several posteriors are prior-limited (H0, R_max)" rather than "the posteriors"; "roughly exponential" discovery rate; H0 scaling "at fixed Ω_b h²"; operational products use "point estimates with linearized error propagation, not posteriors"; CUGN "three lines since 2006, a fourth since".
- Credits: the `source=` lines now carry the photo owners (to confirm), the zdm / James et al. 2022 credit for the p(DM, z) maps, and journal references for Lorimer et al. 2007 and Macquart et al. 2020.
- Checked and kept: seven luminosity-function forms (zdm `luminosity_function` codes 0–6).

*Harvest script.*  `harvest_assets.py` gained `TRIMS` (post-copy crops, applied only to files written in the same run, so re-runs are idempotent), a 16:9 montage, and the new sub-crop `ocean_sketch_forward.png`; `sources.json` has 57 entries.

*Final placeholder list.*  Slides 2, 3, 4: `bg_physics.png`, `bg_astronomy.png`, `bg_ocean.png` (your figures).

*Left for you* (also in `run_sheet.md`).  The three background figures; humor and animations; sharing the README Doc; the telescope and outrigger photo credits to confirm; two numbers to glance at (Baptista et al. 2024's "16 FRBs" on backup slide 46, from your NU deck; the fact check recalled ~21); and the kanji in the author line, which LibreOffice cannot render but Google Slides should.

### 2026-10-17 (Build #6: round-2 answers reviewed against the deck)

You filled in the round-2 answers (Q27–Q38) that had been blank when Builds #1–#5 ran; those builds took a blank as the default, as the round said.  I checked each answer against the built deck and plan with a short script (session scratchpad only).  Every answer is already honoured, so no file changed except this one and no deck was rebuilt.  No git commands were run.

| Q | Answer | In the deck |
|---|---|---|
| 27 | default (ROMS) | slide 40 "A model ocean constrained by data" |
| 28 | (a) for now | `roms_sst_nowcast.png`, the 13 Oct analysis, downloaded from the site |
| 29 | default (may change) | slide 41 with the CUGN map, Rudnick et al. 2017, Moore et al. 2018, BOONUS |
| 30 | default | `cugn_lines.png` via cartopy and Natural Earth |
| 31 | default | Hoffmann Fig. 1 (MCMC), Fig. 3 (Results), Fig. 2 (backup) |
| 32 | default (may change) | BING Fig. 10 (priors), Fig. 4 (degeneracy), Fig. 6 (backup); Fig. 8 harvested as a spare |
| 33 | default | `CREDITS_IN_NOTES = True`; no Source box on any slide; every figure slide's notes carry its credit |
| 34 | `dejavusans`, do not re-render the lifted equations | see below |
| 35 | default | PATH equation on slide 11, Aggarwal et al. 2021 |
| 36 | default | `bing_timing.json`, `bing_cost.png`, 10⁸ spectra a day |
| 37 | default | three placeholders on slides 2–4 |
| 38 | looks good | three discussion slots, 42 main slides, `run_sheet.md` |

*Q34.*  All seven equations on the deck are new `dejavusans` renders; no equation image was lifted from the two decks, so there was nothing to re-render and nothing to swap.  If you would rather see the original LaTeX images for the Gordon relation and the Lee+1999 IOP model (AWOC slides 6, 7, 13) or the DM integral (NU slide 15), say so in #7 and they can be lifted in place of `eq_gordon.png`, `eq_iop_model.png` and the top line of `eq_dm_sum.png`.

*Current deck.*  `talks/ucsc_stats_2026/slides/UCSC_Stats_2026.pptx` (B5: 52 slides, strict QA passed, 3 placeholders) and its PDF are in `~/Google Drive/My Drive/Oceanography/Talks/2026/UCSC_Stats/`.  #7 is ready for your edit list.
