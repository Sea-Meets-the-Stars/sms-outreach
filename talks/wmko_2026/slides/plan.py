"""Created by JXP and Claude.

Slide plan for "Sea meets the stars" — WMKO public evening lecture,
Big Island, 6 Oct 2026 (45 min).  Source of truth for slide order, titles,
sub-lines, figures, source lines and speaker notes; follows the Q36 table
in claude_prompts/wmko_2026.md plus the B3b edits and B5 words pass.

Build (ocean14 env, from the repo root):
    python -m sms_outreach.slides.build talks/wmko_2026/slides/plan.py --pdf

Figure files are looked up in FIG_DIRS; a file that does not exist yet is
drawn as a red PLACEHOLDER box.  Pairs are sea on the LEFT, stars on the
RIGHT.  Sub-lines are the one-line Kraw-style quips at the bottom of a slide.
"""
from pathlib import Path

from sms_outreach.slides.spec import DIVIDER, IMAGE, TITLE, Fig, Slide

HERE = Path(__file__).resolve().parent
TALK = HERE.parent
TEMPLATE = Path("~/Projects/ClimateIntelligence/presentations/2026_WMKO/Kraw_2024.pptx").expanduser()
FIG_DIRS = [TALK / "figures"]
OUTPUT = HERE / "WMKO_2026_Sea_Meets_the_Stars.pptx"
MAX_SLIDES = 45   # 41 planned + launch-art break + Polynesian wayfinding + punchline + FRB intro (B7)

S_INTRO, S_ASTRO, S_AI, S_OCEAN, S_LANG, S_CLAUDE, S_RISK, S_DATA, S_WMKO, S_CLOSE = (
    "Intro", "Astronomy", "AI arrives", "Ocean", "AI on ocean imagery", "Claude", "Risk",
    "AI needs data", "WMKO + AI", "Close")

SLIDES = [
    # ------------------------------------------------------------- intro
    Slide("Sea meets the stars", kind=TITLE, section=S_INTRO,
          subtitle="How artificial intelligence is accelerating the scientific pursuit",
          author="UC Santa Cruz, Kavli IPMU, Simons Pivot Fellow, WMKO lover",
          notes="Aloha. Tonight: the sea, the stars, and the machine that is changing how we study both.\n"
                "Thank WMKO for the invitation."),
    Slide("Exploring the unknown: sea and sky", section=S_INTRO,
          subtitle="What is out there? (And down there?)",
          figures=[Fig("kraw_sea_unknown.jpg"), Fig("kraw_sky_unknown.jpg")],
          source="Right: JWST First Deep Field (NASA, ESA, CSA, STScI)",
          notes="The punchline up front: astronomy and oceanography are both data-driven sciences that explore "
                "the unknown — the sea and the sky. Both have been transformed by data. AI is now an accelerant "
                "on how we ANALYZE data, but not (yet) on how we COLLECT it. Hold on to that; we come back to it.\n"
                "Right: JWST's first deep field (SMACS 0723), thousands of galaxies in a patch of sky the size of "
                "a grain of sand at arm's length."),
    Slide("The punchline", section=S_INTRO,
          subtitle="Spoiler alert",
          figures=[Fig("punchline.png", placeholder="NEW (B7): punchline graphic")],
          source="Schematic: J. X. Prochaska & Claude",
          notes="The whole talk on one slide. Astronomy and oceanography are data-driven fields: we explore the "
                "unknown — the sea and the sky — by collecting data and analyzing it. AI has become an "
                "accelerant on the ANALYSIS, by something like 100x for me. It is not (yet) an accelerant on the "
                "COLLECTION: the telescopes, satellites and robots in the sea. Keep that in mind; we come back to it "
                "at the end."),
    Slide("Polynesian wayfinding: reading sea and sky", section=S_INTRO,
          subtitle="Long before telescopes, satellites, or AI",
          figures=[Fig("hokulea_1976.jpg")],
          bullets=["Hōkūleʻa: the “Star of Gladness” (Arcturus), the zenith star of Hawaiʻi",
                   "1976: Hawaiʻi to Tahiti with no instruments; navigator Mau Piailug",
                   "Rising and setting stars, swells, winds and birds: sea and sky as one map",
                   "2014–2017: Mālama Honua, around the world"],
          source="Photo: Phil Uhl / Wikimedia Commons (CC BY-SA 3.0)",
          notes="The first people to read the sea and the sky together were not astronomers or oceanographers. "
                "Polynesian voyagers navigated thousands of miles of open Pacific by the stars, the swells, the "
                "winds and the birds.\n"
                "Hōkūleʻa was launched by the Polynesian Voyaging Society in 1975. In 1976 Mau Piailug of Satawal "
                "navigated her from Hawaiʻi to Tahiti with no instruments; Nainoa Thompson later revived wayfinding "
                "in Hawaiʻi with the Hawaiian star compass. Arcturus (Hōkūleʻa) passes directly overhead in Hawaiʻi.\n"
                "Photo: her return to Honolulu from Tahiti, 1976.\n"
                "Sea meets the stars is not a new idea here."),
    Slide("My first observing run: Lick, 1995", section=S_INTRO,
          subtitle="Lick turned 150 this year. I got clouds.",
          figures=[Fig("lick_observatory.jpg")],
          source="Photo: Jitze Couperus / Wikimedia Commons (CC BY 2.0)",
          notes="My very first observing run as a graduate student was at Lick Observatory on Mt Hamilton, "
                "above San José, in 1995. We were weathered out.\n"
                "Lick turned 150 this year: the Act of Congress that gave Mt Hamilton to the University of "
                "California was signed on 7 June 1876, and the anniversary was celebrated on 7 June 2026 "
                "(at Chabot Space & Science Center, after windstorm damage on the mountain)."),
    Slide("Lick: a history of firsts", section=S_INTRO,
          subtitle="1888: the first permanently staffed mountaintop observatory",
          figures=[Fig("lgs_laser.jpg", caption="1990s: the first sodium laser guide star"),
                   Fig("iodine_cell.jpg", caption="1992: the iodine cell, for hunting planets")],
          source="Photos: Gemini/NOIRLab/B. Tafreshi (CC BY 4.0); 2x910 / Wikimedia Commons (CC BY-SA 4.0)",
          notes="1888: Lick was the world's first permanently staffed mountaintop observatory.\n"
                "1990s: Claire Max and colleagues (LLNL + Lick) put the first sodium laser guide star adaptive-"
                "optics system on the Shane 3-m telescope: a laser makes an artificial star in the sky so the "
                "telescope can undo the twinkling. Keck's lasers (the photo, from Maunakea) descend from that work.\n"
                "1992: Geoff Marcy and Paul Butler put a glass cell of iodine gas in front of the spectrograph — "
                "a ruler printed onto the starlight — and that is how many of the first planets around other stars "
                "were found and weighed. The photo is iodine gas in a flask, not the actual cell."),
    Slide("Keck, 1995: losing my PhD to clouds?", section=S_INTRO,
          subtitle="Clouds again. Was my PhD doomed?",
          figures=[Fig("keck_domes.jpg")],
          notes="My second observing run: Keck, 1995, my first visit to Hawaiʻi. Mostly weathered out again. I "
                "seriously wondered if my PhD would be lost to the clouds.\n"
                "(Photo credit to confirm — probably W. M. Keck Observatory.)"),
    Slide("Married to Keck 31 years, to my wife 32", section=S_INTRO,
          subtitle="Father of 3 sons, husband of 1",
          figures=[Fig("headshot_1990s.png")],
          bullets=["1995: first visit to Hawaiʻi", "1998: PhD (UC San Diego)", "2002: Professor, UCSC",
                   "2017: introduced to AI", "2020: Ocean Sciences"],
          source="Photo: my Keck Observer Portal card",
          notes="My first trip to Keck was in 1995, so Keck and I have been together for 31 years. I married my "
                "wife on 16 July 1994 — 32 years. She wins by one.\n"
                "That photo is the one still on my Keck Observer Portal card."),
    # --------------------------------------------------------- astronomy
    Slide("HIRES: weighing the Universe and finding planets", section=S_ASTRO,
          subtitle="Weighing the Universe, one atom in 40,000",
          figures=[Fig("hires.jpg"), Fig("universe_pie.png", placeholder="NEW (B7): Universe pie chart")],
          source="Photo: courtesy W. M. Keck Observatory · Pie: Planck 2018",
          notes="HIRES (PI Steve Vogt) saw first light on 16 July 1993. Two of its greatest hits:\n"
                "1) Deuterium. In gas that has barely been touched since the Big Bang, about 1 hydrogen atom in "
                "40,000 is deuterium (D/H = 2.53 × 10⁻⁵, Cooke et al. 2018). The Big Bang predicts that number "
                "from how much ordinary matter there is — so measuring D/H weighs the Universe. The answer: ordinary "
                "matter — stars, gas, planets, us — is only ~5% of the Universe (the gold slice); the rest is dark "
                "matter (~27%) and dark energy (~68%). It agrees with the Planck satellite's measurement from the "
                "cosmic microwave background. (Keck/HIRES D/H: "
                "Tytler, Fan & Burles 1996; Burles & Tytler 1998.)\n"
                "2) Planets: HIRES + an iodine cell found many of the first exoplanets."),
    Slide("My HIRES work: damped Lyα systems", section=S_ASTRO,
          subtitle="Cosmic flashlights reveal the fuel for galaxies",
          figures=[Fig("dla_public.png")],
          source="Data: Rafelski et al. 2012 (242 DLAs, mostly Keck/HIRES); left: illustration",
          notes="Quasars are cosmic flashlights. When their light passes through a big cloud of hydrogen gas — "
                "the fuel for making stars and galaxies — it carves out a huge absorption trough: a damped "
                "Lyman-alpha system.\n"
                "With HIRES we measured the heavy elements (\"metals\") in these clouds. Right: 242 clouds. Early in "
                "cosmic time they have roughly 1/100 of the Sun's metals; the Universe has been slowly enriching "
                "itself for 12 billion years. Much of my career."),
    Slide("2020s: the Wolfe disk", section=S_ASTRO,
          subtitle="A grown-up galaxy, way too early",
          figures=[Fig("alma.jpg", caption="ALMA, Chile"),
                   Fig("wolfe_disk.jpg", caption="The Wolfe disk (artist's view)")],
          source="Photo: A. Duro/ESO (CC BY 4.0) · Illustration: NRAO/AUI/NSF, S. Dagnello (CC BY 4.0)",
          notes="Neeleman et al. 2020, Nature: with the ALMA radio array in Chile we found a massive, cold, "
                "rotating disk galaxy (DLA0817g) seen only ~1.5 billion years after the Big Bang, spinning at "
                "~270 km/s. Galaxies were not supposed to settle into calm disks that early.\n"
                "We named it the Wolfe disk, for Arthur M. Wolfe, the pioneer of damped Lyman-alpha systems "
                "(and my PhD advisor) — it was found as a DLA."),
    Slide("What is a fast radio burst?", section=S_ASTRO,
          placeholder="Author: introduce fast radio bursts here",
          notes="[Author to fill in: what an FRB is.]"),
    Slide("2020s: an FRB from the first 3 billion years", section=S_ASTRO,
          subtitle="Keck saw nothing. That told us to look harder.",
          figures=[Fig("frb_lris_zoom.png", caption="Keck: nothing there"),
                   Fig("frb_jwst_zoom.png", caption="JWST: a faint galaxy, z = 2.148")],
          source="Caleb et al., Science (2026); arXiv:2508.01648 · Keck/LRIS (left), JWST/NIRCam (right)",
          notes="Fast radio bursts: millisecond flashes of radio waves from across the Universe. FRB 20240304B "
                "was caught by the MeerKAT telescope in South Africa on 4 March 2024.\n"
                "We pointed Keck (LRIS) at its position in June 2024 and saw NOTHING, down to very faint limits. "
                "That non-detection justified asking for the James Webb Space Telescope — and JWST found a tiny, "
                "young galaxy at redshift 2.148: the burst left it when the Universe was ~3 billion years old, "
                "about 11 billion years ago. Twice the redshift of any FRB with a known home.\n"
                "Published in Science this week (press release Thursday 8 October). Left image ~20 arcsec across; "
                "right is a closer zoom (~4 arcsec)."),
    # --------------------------------------------------------- AI arrives
    Slide("My entry into AI (2017)", section=S_AI,
          subtitle="A grad student walked into my office...",
          figures=[Fig("mbari_cnn.png")],
          source="VGG-16 network diagram after D. Frossard (2016)",
          notes="In 2017 David Parks, a UCSC computer-science graduate student working with David Haussler (Genomics "
                "Institute), introduced me to deep learning: convolutional neural networks, built in layers, each learning "
                "more abstract features of an image."),
    Slide("AI 2012: cats and dogs", section=S_AI,
          subtitle="What's the big deal? My 1-year-old could do this...",
          figures=[Fig("kraw_cats_dogs.jpg")],
          notes="2012: the deep-learning revolution starts with telling cats from dogs (ImageNet). Unimpressive "
                "to a toddler — revolutionary for a computer."),
    Slide("AI on quasar spectra: finding DLAs", section=S_AI,
          subtitle="Same trick, now on quasar light",
          figures=[Fig("kraw_parks_cnn.png")],
          source="Quasar Q2138-4427 (Lick Observatory) · Parks, Prochaska et al. 2018 (MNRAS)",
          notes="We trained a neural network to find damped Lyman-alpha systems — that deep trough near 4,700 Å — "
                "in hundreds of thousands of quasar spectra, faster and more consistently than tired, biased "
                "humans (me)."),
    Slide("Describe what you see", section=S_AI,
          subtitle="Go ahead, take a guess",
          figures=[Fig("dots.png"), Fig("squiggles.png")],
          source="Right: a Gray–Scott reaction–diffusion pattern (J. X. Prochaska & Claude)",
          notes="Ask the audience to describe each image in words.\n"
                "Left: easy — a grid of dots; you can describe it exactly with a few numbers.\n"
                "Right: hard — squiggles. Every word you try leaves something out."),
    Slide("Stars are dots; the ocean is squiggles", section=S_AI,
          subtitle="AI loves squiggles",
          figures=[Fig("cmb_sky.png"), Fig("sst_cutout.png")],
          source="Left: ESA and the Planck Collaboration · Right: NOAA VIIRS SST",
          notes="Much of astronomy is dots — stars and galaxies — that we can catalogue with a few numbers. The "
                "ocean is squiggles: eddies, fronts, filaments at every scale. This is exactly where AI shines: it "
                "learns its own vocabulary for complex patterns. (The sky has squiggles too: the CMB map, left.)"),
    # -------------------------------------------------------------- ocean
    Slide("Ocean satellites: temperature", section=S_OCEAN,
          subtitle="The whole ocean's temperature, every day, from space",
          figures=[Fig("viirs_sst.png")],
          source="NOAA Geo-Polar Blended SST (VIIRS + other satellites), 4 Oct 2026, via CoastWatch ERDDAP",
          notes="Sea-surface temperature on Sunday, 4 October 2026, from NOAA's analysis that blends the VIIRS "
                "instruments with other satellites. Note the warm Pacific around Hawaiʻi.\n"
                "Satellites like VIIRS image the whole ocean every day at ~1 km — billions of pixels."),
    Slide("Ocean satellites: color", section=S_OCEAN,
          subtitle="Ocean color = ocean life",
          figures=[Fig("pace_moana.png")],
          source="NASA PACE OCI, MOANA (Lange et al. 2020), 1 July 2025",
          notes="NASA's PACE satellite (launched February 2024) sees the ocean in a rainbow of more than 200 colors. From "
                "the color we can tell which microscopic plants (phytoplankton) live where: Prochlorococcus, the "
                "most abundant photosynthesizer on Earth, floods the warm tropics; Synechococcus and tiny algae "
                "take over in cooler, richer water. One day, the Atlantic (grey = clouds or between orbits)."),
    Slide("Ocean models: a virtual ocean", section=S_OCEAN,
          subtitle="A virtual ocean, 2 km at a time",
          figures=[Fig("llc4320_sst.png")],
          source="MITgcm LLC4320 simulation (NASA/JPL ECCO) · figure: J. X. Prochaska & Claude",
          notes="Computers also make oceans. NASA's LLC4320 simulation resolves the whole ocean at ~2 km. Here: "
                "the Gulf Stream. Models are 'super data generators' — and a training ground for AI, because "
                "we know the right answer everywhere."),
    # ------------------------------------------------ AI on ocean imagery
    Slide("Nenya: learning the language of SST", section=S_LANG,
          subtitle="One code to describe them all",
          figures=[Fig("nenya_umap.png")],
          source="Nenya: self-supervised learning on satellite SST (Prochaska et al., IEEE TGRS 2023)",
          notes="Nenya learned, on its own, a vocabulary for millions of ~100 km satellite images of the sea "
                "surface. Similar patterns land near each other on this map — a 'language' of the ocean. "
                "(Names: Nenya, Tolkien's ring of water; Ulmo, Tolkien's lord of the waters; Enki, the Sumerian god of water.)"),
    Slide("Ulmo: finding the unusual words", section=S_LANG,
          subtitle="One code to find them",
          figures=[Fig("ulmo_outliers.png")],
          source="Ulmo: Prochaska, Cornillon & Reiman 2021",
          notes="Ulmo searched ~12 million satellite images for the most unusual ones — the rare, extreme ocean events. "
                "Needles in a haystack."),
    Slide("Enki: filling in the missing words", section=S_LANG,
          subtitle="One code to fix them (clouds!)",
          figures=[Fig("enki_reconstruction.png")],
          source="Enki: Agabin, Prochaska et al. 2024; trained on LLC4320",
          notes="Clouds hide the ocean from satellites. Enki was trained on the virtual ocean to fill in the "
                "missing pieces — left to right: the true image, the image with 'clouds', Enki's reconstruction, "
                "and the tiny error. Errors up to 10x smaller than older gap-filling methods, even with most of the image hidden."),
    Slide("It was language all along", section=S_LANG,
          subtitle="We didn't know it at the time",
          bullets=["Nenya learned the words (a vocabulary of ocean patterns)",
                   "Ulmo found the unusual words",
                   "Enki filled in the missing words (like a masked language model)"],
          notes="Even as we were doing it, we didn't understand how language was underpinning it all. "
                "Nenya ~ embeddings; Ulmo ~ out-of-vocabulary detection; Enki ~ masked-word prediction "
                "(the trick behind BERT); large language models do this at the scale of the internet."),
    Slide("Math is a language too", section=S_LANG,
          subtitle="Even calculus is just another language",
          figures=[Fig("lample_charton.png")],
          source="Lample & Charton 2020 (Facebook AI Research, ICLR), Tables 3 and 4",
          notes="In 2019, Facebook AI researchers treated equations as sentences and trained a translator from "
                "'integral' to 'answer'. It solved 98% of their test integrals (99.6% with more guesses), in under "
                "a second; Mathematica solved 84% even with 30 seconds each. Right: one it got that Mathematica "
                "couldn't."),
    # ------------------------------------------------------------- Claude
    Slide("", kind=IMAGE, section=S_CLAUDE,
          figures=[Fig("launch_art.png")],
          source="Artwork: Anthropic",
          notes="And then this happened..."),
    Slide("November 2025: Claude will surpass me", section=S_CLAUDE, plain=True,
          subtitle="Written at 5 am, in Japan",
          bullets=["“Claude now surpasses the skills and knowledge of an average PhD student. "
                   "In every domain of science.”",
                   "“It codes better than me and all of my science colleagues – put together!”",
                   "— my private notes, 22 Nov 2025"],
          notes="From 'Rambling reflections on AI', written at 5 am in Japan on 22 November 2025 and shared with "
                "only a few people. Also: 'I am convinced that I too will be surpassed.'"),
    Slide("June 13, 2026: Claude surpassed me", section=S_CLAUDE,
          subtitle="Like Neo learning kung fu",
          figures=[Fig("sacbee.png")],
          source="J. X. Prochaska, The Sacramento Bee, 21 Aug 2026",
          notes="On the evening of 13 June 2026 I asked Claude to write a one-page technical proposal for "
                "highly coveted observing time on the Very Large Telescope. The draft was better than anything I "
                "or the ten senior astronomers on the team could have written — and it caught an error one of us "
                "had made that the rest had missed.\n"
                "I wrote about it in the Sacramento Bee (21 Aug 2026): 'I feel like Neo mastering kung-fu in the "
                "Matrix.' I now generate a year's worth of research every few days."),
    Slide("I will never write another line of code", section=S_CLAUDE,
          subtitle="674,000 lines. Done.",
          figures=[Fig("loc_over_time.png")],
          source="Surviving lines in my git repositories, 1995–2026 (J. X. Prochaska & Claude)",
          notes="674,000 lines of code in total (FORTRAN, IDL, Python): ~625,000 written by hand over 31 years, then — "
                "the orange, after 13 June 2026 — ~49,000 lines in four months, all written by AI. I will not write another line."),
    Slide("Writing: proposals and papers", section=S_CLAUDE,
          subtitle="Scientific papers have doubled in two years",
          figures=[Fig("a5_arxiv.png")],
          source="Data: arXiv monthly submissions; arXiv blog, 1 Oct 2026",
          notes="New papers on arXiv per month: 9,869 in Sept 2016; 20,569 in Sept 2024; 40,363 in Sept 2026. "
                "On 1 October 2026 arXiv began capping authors at 2 papers a month. Proposals and papers are now "
                "written with AI — mine included. Peer review cannot keep up."),
    Slide("Claude's PhD: waiting on the committee to grade", section=S_CLAUDE,
          subtitle="Analysis done. Now waiting on the humans.",
          figures=[Fig("fig01_inverse_problem.png")],
          source="Claude's PhD thesis (advisor: J. X. Prochaska), Fig. 1",
          notes="I gave Claude a real PhD project in ocean color (PACE): one spectrum in, five constituents out. "
                "It did the research, wrote the dissertation and took its qualifying exam. The bottleneck is now "
                "us: Claude is waiting on the committee to grade."),
    # --------------------------------------------------------------- risk
    Slide("Nothing more powerful than Fable in the wild", section=S_RISK,
          subtitle="This is not science fiction: biology",
          figures=[Fig("a2_bio_uplift.png")],
          source="Fortune 30 Sep 2026; RAND, OpenAI 2024; Anthropic 2025; Zhang+ 2026 (not wet-lab)",
          notes="I'll be blunt: this frightens me. In 2024, AI gave novices no measurable help toward making a "
                "biological weapon. By 2025, Anthropic's own testing found 2.5x; by 2026, an independent trial found 4x. OpenAI's o3 "
                "beat 94% of expert virologists at troubleshooting lab protocols.\n"
                "Bill Gates (Fortune, 30 Sep 2026): \"A.I. has crossed the threshold that its ability to empower "
                "a bioterrorist to kill hundreds of millions — that exists today.\"\n"
                "My line: nothing more powerful than today's public models (Fable) should be released into the "
                "wild."),
    Slide("...and cyber", section=S_RISK,
          subtitle="...and nearly every computer on Earth",
          figures=[Fig("a3_hacking.png")],
          source="Scientific American & Axios, Apr 2026; CNBC, Jul 2026",
          notes="April 2026: Anthropic judged its Claude Mythos Preview too dangerous to release — it found "
                "critical flaws in every major operating system and browser, 99% of them unpatched, and "
                "succeeded at 73% of expert-level hacking tasks (UK AI Security Institute).\n"
                "July 2026: an AI agent broke into Hugging Face; a week later OpenAI disclosed its models had too."),
    Slide("What can be done", section=S_RISK,
          subtitle="Resignation is not an option",
          bullets=["Strict liability for AI harms (especially to the young)",
                   "Tiered regulation, with a kill switch",
                   "Compute caps, with international verification"],
          notes="What I have argued in print:\n"
                "1) Strict liability: companies are responsible for the harms their AI causes, especially to "
                "children.\n"
                "2) Tiered safety regulation scaled to risk — pre-approval and a kill switch that can't be "
                "removed for highly autonomous, superhuman systems.\n"
                "3) Mandatory accounting and caps on the compute used to train and run AI, with international "
                "(including U.S.–China) verification — feasible because frontier chips come from a handful of "
                "makers.\n"
                "Scientists helped keep nuclear weapons in check for 75 years. We stand ready again. "
                "Resignation or inaction are not acceptable responses."),
    # ------------------------------------------------------ AI needs data
    Slide("AI needs data", section=S_DATA,
          subtitle="It can't solve what it can't see",
          figures=[Fig("ai_needs_data.png", placeholder="NEW (B7): data -> AI -> people")],
          source="Schematic: J. X. Prochaska & Claude",
          notes="As my wife put it (November 2025): AI can't solve what dark matter is on its own, because it "
                "doesn't have the data — we humans haven't collected it yet.\n"
                "Data goes in, AI finds the patterns, and what comes out teaches us — but only if someone collected "
                "the data first. Data collection — telescopes, satellites, robots in the sea — is now the scarce "
                "resource."),
    Slide("BGC-Argo floats meet PACE", section=S_DATA,
          subtitle="Robots below, satellites above",
          figures=[Fig("pab_infographic.png")],
          source="PAB: PACE × BGC-Argo matchups (J. X. Prochaska & Claude)",
          notes="~4,000 Argo floats drift through the ocean, diving to 2,000 m and back every ten days; the "
                "biogeochemical (BGC) ones also carry sensors for oxygen, chlorophyll, pH and particles. We match "
                "them with what PACE sees from above to test and improve the satellite's view of ocean life."),
    Slide("BOONUS: a weather map for our coastal ocean", section=S_DATA,
          subtitle="A seamless, predictive weather map for our waters",
          figures=[Fig("ocean_glider.jpg")],
          bullets=["~100 robot gliders along the whole U.S. coast",
                   "Coupled to ocean models, guided by AI",
                   "Heat waves, algal blooms, hurricanes: reactive → proactive"],
          source="Photo: Ocean Observatories Initiative (public domain); a Slocum glider",
          notes="BOONUS — the Boundary Ocean Observing Network of the United States — would scale up the "
                "California Underwater Glider Network (Dan Rudnick, Scripps, since ~2005) to ~100 gliders "
                "around the whole U.S. coast.\n"
                "Coupled to ocean models and guided by AI: 'a seamless, predictive weather map for our waters' — "
                "anticipating marine heat waves, harmful algal blooms and the paths of hurricanes and atmospheric "
                "rivers. It changes ocean management from reactive to proactive. The project is nearly "
                "shovel-ready."),
    Slide("Coupling observations to models with AI", section=S_DATA,
          subtitle="And then: tell the robots where to look next",
          figures=[Fig("obs_model_ai.png")],
          source="Schematic: J. X. Prochaska & Claude",
          notes="Observe (satellites, gliders, floats) → a virtual ocean (model + AI) → forecast (marine heat "
                "waves, hurricanes) → and the forecast tells the gliders where to look next. Predict the weather; "
                "monitor climate change optimally."),
    # ---------------------------------------------------------- WMKO + AI
    Slide("WMKO + AI: building new optics", section=S_WMKO,
          subtitle="Physics from Phil, code from Claude",
          figures=[Fig("hinz_plots.png")],
          bullets=["A model of glass slumping in a furnace, built from the equations",
                   "Now sets the recipe for the shells of KASM (3,106 actuators)",
                   "Phil: physics and sanity checks · Claude: derive, code, verify"],
          source="Slide courtesy of Phil Hinz (UCSC)",
          notes="Two everyday wins at an observatory: AI reads and explores the documentation for you, and it "
                "helps build new instruments.\n"
                "Phil Hinz (UCSC) used Claude to build, from the governing equations, a model of how glass slumps "
                "in a furnace; it now sets the recipe for the shells of KASM, the Keck Adaptive Secondary Mirror "
                "(3,106 actuators). Phil supplied the physics and the sanity checks; Claude derived, coded and "
                "verified. (Claude also wrote his slide.)"),
    Slide("The Holy Grail of spectroscopy", section=S_WMKO,
          subtitle="One solution to rule them all",
          figures=[Fig("holy_grail_raw.png", caption="Raw lamp exposure"),
                   Fig("holy_grail_cal.png", caption="Wavelengths, with no human input")],
          source="PypeIt; Lick/APF arc lamp · news.ucsc.edu/2026/09/prochaska-ai-science-grant",
          notes="Every spectrograph records light as pixels; science needs wavelengths. Today an expert has to "
                "tell the software which calibration lamps were used and how the instrument spreads the light. "
                "The Holy Grail: hand AI a raw lamp exposure (left) and get the full wavelength solution (right), "
                "with no human input — for every spectrograph PypeIt supports, including LRIS, DEIMOS, HIRES, KCWI "
                "and MOSFIRE at Keck.\n"
                "With Ryan Cooke (Durham) and Claude; supported by Anthropic's AI for Science program "
                "(UCSC News, Sept 2026). Unlocking science in decades of archived data."),
    Slide("Re-finding Keck's first planet in 12 days", section=S_WMKO,
          subtitle="1998 data, 2026 tools, same planet",
          figures=[Fig("fig7_three_ways.png")],
          source="HD 187123 b, 1997–98 Keck/HIRES archive data (KOA) · right: Teklu et al. 2025",
          notes="HD 187123 b was the first exoplanet discovered with Keck/HIRES (Butler et al. 1998). With Claude "
                "I re-reduced the original 1997–98 frames from the Keck Observatory Archive using only free, open "
                "software, in 12 days.\n"
                "Left: lamps alone — no planet. Middle: with the iodine cell — the planet, 72 ± 7 m/s, its 3.1-day "
                "period found blind (published: 72 m/s). Right: today's professional pipeline."),
    Slide("You could do this (and so could a classroom)", section=S_WMKO,
          subtitle="The scarce skill: knowing what to ask",
          plain=True,
          bullets=["12 days · 49 steps · 26 decisions · all free",
                   "1. Find the first exoplanet discovered with Keck/HIRES.",
                   "2. Ask me another round of questions.",
                   "3. Make clear it is the star that moves; the planet is invisible.",
                   "4. Write a plan for working on the 1998 data.",
                   "5. Check that PypeIt is ready for the original HIRES detector.",
                   "6. Fix the issues you have identified.",
                   "7. Take account of pyodine: adapt it rather than build it.",
                   "8. Reread the file and execute prompt #N.",
                   "9. Answer: (a)",
                   "10. Draft the report to the PypeIt team; show it to me first."],
          notes="Ten prompts like these steered it: 12 days, 49 steps, 26 decisions, all free — public data and "
                "open software. I set the goal and made the calls; the AI wrote the plans, the code and the "
                "reports. A teacher could lead a class through it (backup slide). The scarce skill is knowing "
                "what to ask, and when to doubt an answer."),
    # -------------------------------------------------------------- close
    Slide("Why science isn't hard", section=S_CLOSE,
          subtitle="We were all scientists at age 4. What happened?",
          notes="[Author to fill in: the book, Why Science Isn't Hard.]"),
    Slide("Summary", section=S_CLOSE,
          bullets=["Sea and sky: data-driven exploration of the unknown",
                   "AI has transformed how we analyze data (and me)",
                   "The most powerful AI must be handled with care",
                   "Telescopes, satellites, sea robots: data is the scarce resource",
                   "AI accelerates the analysis — not (yet) the data collection"],
          notes="Mahalo. End on the punchline: AI accelerates the analysis — but not (yet) the data collection. "
                "That is where Keck, and all of you, come in."),
    # ------------------------------------------------------------- backup
    Slide("Backup", kind=DIVIDER, section="Backup", backup=True, notes="Backup slides."),
    Slide("KCWI: Lyα and Hα", section="Backup", backup=True,
          placeholder="KCWI Lyα / Hα figure (proposal in progress)",
          notes="Unlocking science in existing data: KCWI Lyα and Hα (proposal in progress)."),
    Slide("A teacher could lead a class through it", section="Backup", backup=True,
          figures=[Fig("exo_public_2.png")],
          source="first-hires-exoplanet (J. X. Prochaska & Claude)",
          notes="Six lessons from re-finding HD 187123 b: the wobble, the archive, light into spectra, lamps fall "
                "short, a ruler of iodine, find the planet."),
    Slide("It takes a village", section="Backup", backup=True,
          figures=[Fig("team_ai_remote_sensing.png")],
          source="The AI on Remote Sensing team",
          notes="Hoffman, Reiman, Guo, Tallman, Buckingham, Cornillon, Sonnewald, Menemenlis."),
]
