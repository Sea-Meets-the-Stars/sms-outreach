# Run sheet — "Sea Meets the Stars", UCSC Statistics seminar, Monday 19 Oct 2026

60 minutes: 45 of slides, 15 of discussion in three slots.  42 main slides (+ 11 backup).  Clock times are cumulative.  Numbering follows the B7 deck (`plan.py`).

| Slides | Section | Minutes | Ends at | Key line |
|---|---|---|---|---|
| 1–5 | Title, three toolkits, outline | 4 | 0:04 | "Two problems with the same shape, one request." |
| 6–12 | FRBs: the three questions, telescope → DM → localization → PATH → redshift | 7 | 0:11 | "Every burst has a DM; a few dozen have a redshift." |
| 13–18 | Population model, likelihood, MCMC, results, open challenges | 9 | 0:20 | "A week per fit, and the posteriors follow the priors." |
| 19 | Discussion I | 5 | 0:25 | Emulator? Evidence for seven forms? Less prior-driven? |
| 20–24 | Ocean colour: what is in the water, PACE, systematics, errors | 5 | 0:30 | "10⁸ spectra a day, with correlated errors and error bars we do not trust." |
| 25–31 | Forward model, degeneracy, biology (pigments) → three models fit equally well, MCMC, cost, priors | 8 | 0:38 | "R_rs depends on a and b_b only through their ratio; the template is a choice." |
| 32–33 | Where to take new data; can we GP this? | 3 | 0:41 | "Simulate, train, infer every pixel in one pass." |
| 34 | Discussion II | 5 | 0:46 | Evidence? Learned priors? Calibrated amortized posteriors? |
| 35–38 | PFTs: MOANA, Lange PCA, Kramer 2nd derivative + PCA | 5 | 0:51 | "100 bands, 3 identifiable parameters." |
| 39 | What do you recommend? | 5 | 0:56 | Composition from a spectrum, with uncertainties. |
| 40–42 | ROMS 4D-Var, glider placement, what I would like from you | 4 | 1:00 | "Faster, less prior-dependent, with an honest evidence." |

**Pace check:** be at slide 13 (population model) by ~0:11, slide 20 (Part II) by ~0:25, and slide 35 (two other problems) by ~0:46.  If behind, shorten slides 8–12 (data chain) and drop slide 24 (poorly measured errors; its point is on slide 23).

**Backup (43–53):** Macquart relation 2020, H₀ and the DM cliff, F and feedback, ΔBIC, scattering selection, phytoplankton absorption retrieved vs. true, the three-model backscattering panel, Kramer retrieved vs. measured pigments, the NE2001 Milky Way DM map, repetition parameters.

## Left for you

- **Slides 2–4:** three red placeholders for your own figures (`bg_physics.png`, `bg_astronomy.png`, `bg_ocean.png` in `talks/ucsc_stats_2026/figures/`; drop the files in and rebuild, or paste them in Google Slides).
- **Humor and animations:** none added (Q6, Q7); add in Google Slides.
- **README Doc:** still unshared; the closing slide names the README but has no link or QR (Q42).
- **Credits to confirm:** the four telescope photos (MeerKAT, CHIME, ASKAP, Parkes) and the CHIME outrigger photo (see `figures/credits.md`); every credit is in the speaker notes.
- **Two numbers to check before the talk:** slide 46's caption says Baptista et al. 2024 used 16 FRBs (from your NU deck; the fact check recalled ~21); and the "seven" luminosity-function forms (zdm codes 0–6) is right but only one has been fit.
- **Numbers to glance at before the talk:** slide 30 quotes the fit timed on this laptop (29 s per spectrum, 93 CPU-years per day at 10⁸ spectra); slide 12 says ~100 localized bursts in total and 26 in the fitted sample.
- **Fonts:** the PDF renders in a serif fallback because Roboto is not installed for LibreOffice; Google Slides will show Roboto.
- **Slide 24:** kept, with the new PAB figures (χ²_ν = 0.20 median fit; the satellite-vs-float b_bp scatter); drop it if you decide its point is already made on slide 23.
- **PAB inputs:** the two fit figures on slides 22–24 are rebuilt by `scripts/fig_pab_fit.py` from the public v2 database and two chain files fetched from the Drive backup (paths in the script); those inputs are not in this repository.
