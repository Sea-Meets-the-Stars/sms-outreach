"""Created by JXP and Claude.

Slide plan for "Sea meets the stars" — WMKO public evening lecture,
Big Island, 6 Oct 2026 (45 min).  Source of truth for slide order, titles,
figures, sources and speaker notes; follows the Q36 table in
claude_prompts/wmko_2026.md.

Build (ocean14 env, from the repo root):
    python -m sms_outreach.slides.build talks/wmko_2026/slides/plan.py --pdf

Figure files are looked up in FIG_DIRS; a file that does not exist yet is
drawn as a red PLACEHOLDER box (B2 harvests existing images, B4 makes the
new ones).  Pairs are sea on the LEFT, stars on the RIGHT.
"""
from pathlib import Path

from sms_outreach.slides.spec import CONTENT, DIVIDER, IMAGE, TITLE, Fig, Slide

HERE = Path(__file__).resolve().parent
TALK = HERE.parent
TEMPLATE = Path("~/Projects/ClimateIntelligence/presentations/2026_WMKO/Kraw_2024.pptx").expanduser()
FIG_DIRS = [TALK / "figures"]
OUTPUT = HERE / "WMKO_2026_Sea_Meets_the_Stars.pptx"
MAX_SLIDES = 42   # 41 planned + the launch-art break

S_INTRO, S_ASTRO, S_AI, S_OCEAN, S_LANG, S_CLAUDE, S_RISK, S_DATA, S_WMKO, S_CLOSE = (
    "Intro", "Astronomy", "AI arrives", "Ocean", "AI on ocean imagery", "Claude", "Risk",
    "AI needs data", "WMKO + AI", "Close")

SLIDES = [
    # ------------------------------------------------------------- intro
    Slide("Sea meets the stars", kind=TITLE, section=S_INTRO,
          subtitle="How artificial intelligence is accelerating the scientific pursuit",
          author="UC Santa Cruz, Kavli IPMU, Simons Pivot Fellow, WMKO lover",
          notes="Kraw 2024 title slide (sea|sky hero image)."),
    Slide("Exploring the unknown: sea and sky", section=S_INTRO,
          figures=[Fig("kraw_sea_unknown.jpg", placeholder="Kraw 2/5: ocean exploration image"),
                   Fig("kraw_sky_unknown.jpg", placeholder="Kraw 2/5: sky exploration image")],
          notes="Punchline up front: astronomy and oceanography are data-driven fields exploring the "
                "unknown. AI is an accelerant on data analysis, but not (yet) on data collection."),
    Slide("My first observing run: Lick, 1994", section=S_INTRO,
          figures=[Fig("lick_observatory.jpg", placeholder="Lick Observatory photo (Wikimedia Commons)")],
          notes="Weathered out. Lick turned 150 this year (Act of Congress, 7 Jun 1876; celebrated 7 Jun 2026)."),
    Slide("Lick: a history of firsts", section=S_INTRO,
          bullets=["First permanently staffed mountaintop observatory (1888)",
                   "First sodium laser guide star adaptive optics (1990s)",
                   "The iodine cell: hunting planets (Marcy & Butler 1992)"],
          notes="Claire Max et al. (LLNL/Lick) sodium LGS AO on the Shane 3-m; iodine cell on the Hamilton echelle."),
    Slide("Keck, 1995: losing my PhD to clouds?", section=S_INTRO,
          figures=[Fig("keck_domes.jpg", placeholder="Keck domes [Honokaʻa 3]")],
          notes="Second run, also mostly weathered out."),
    Slide("33 years of Keck science (one more than my marriage)", section=S_INTRO,
          figures=[Fig("login_card.jpg", placeholder="UCO/Lick profile card photo [Honokaʻa 2]")],
          bullets=["1995: first visit to Hawaii", "1998: PhD (UC San Diego)", "2002: Professor (UC Santa Cruz)",
                   "2017: introduced to AI", "2020: Ocean Sciences"],
          notes="Keck science began May 1993; married 16 Jul 1994 (32 years)."),
    # --------------------------------------------------------- astronomy
    Slide("HIRES: weighing the Universe and finding planets", section=S_ASTRO,
          figures=[Fig("hires.jpg", placeholder="HIRES photo [CI]"),
                   Fig("dh_omega_b.png", placeholder="NEW (B4d): D/H → Ω_b schematic")],
          notes="D/H with HIRES → baryon density; HIRES + iodine cell → exoplanets."),
    Slide("My HIRES work: damped Lyα systems", section=S_ASTRO,
          figures=[Fig("dla_public.png", placeholder="NEW (B4e): DLA public figure")],
          notes="Damped Lyα systems: gas reservoirs for galaxy formation."),
    Slide("2020s: the Wolfe disk", section=S_ASTRO,
          figures=[Fig("wolfe_disk.jpg", placeholder="NRAO/ALMA Wolfe disk press image")],
          notes="Neeleman et al. 2020, Nature. Named for Arthur M. Wolfe."),
    Slide("2020s: an FRB from the first 3 billion years", section=S_ASTRO,
          figures=[Fig("frb_keck_lris.png", caption="Keck/LRIS: nothing", placeholder="Keck/LRIS R-band image"),
                   Fig("frb_jwst_nircam.png", caption="JWST: a host at z = 2.148",
                       placeholder="JWST NIRCam (Caleb+ Fig. 2)")],
          notes="FRB 20240304B; Caleb et al., Science (press release Thu 8 Oct 2026)."),
    # --------------------------------------------------------- AI arrives
    Slide("My entry into AI (2017)", section=S_AI,
          figures=[Fig("mbari_cnn.png", placeholder="Haussler / Parks [Kraw 19, MBARI 3]")],
          notes="Introduced by David Parks and David Haussler (UCSC Genomics Institute)."),
    Slide("AI 2012: cats and dogs", section=S_AI,
          figures=[Fig("kraw_cats_dogs.jpg", placeholder="[Kraw 14]")]),
    Slide("AI on quasar spectra: finding DLAs", section=S_AI,
          figures=[Fig("kraw_parks_cnn.png", placeholder="[Kraw 19] Parks et al. CNN")],
          notes="Parks et al. 2018."),
    Slide("Describe what you see", section=S_AI,
          figures=[Fig("dots.png", placeholder="dots [MBARI 13]"),
                   Fig("squiggles.png", placeholder="squiggles [MBARI 13]")]),
    Slide("Stars are dots; the ocean is squiggles", section=S_AI,
          figures=[Fig("sst_cutout.png", placeholder="VIIRS SST cutout [MBARI 14]"),
                   Fig("cmb_sky.png", placeholder="CMB / sky [MBARI 14]")]),
    # -------------------------------------------------------------- ocean
    Slide("Ocean satellites: temperature", section=S_OCEAN,
          figures=[Fig("viirs_sst.png", placeholder="NEW (B4a): VIIRS L4 global SST")]),
    Slide("Ocean satellites: color", section=S_OCEAN,
          figures=[Fig("pace_moana.png", placeholder="NEW (B4b): PACE MOANA map")]),
    Slide("Ocean models: a virtual ocean", section=S_OCEAN,
          figures=[Fig("llc4320_sst.png", placeholder="LLC4320 SST [wrangler]")]),
    # ------------------------------------------------ AI on ocean imagery
    Slide("Nenya: learning the language of SST", section=S_LANG,
          figures=[Fig("nenya_umap.png", placeholder="UMAP mosaic [MBARI 24]")]),
    Slide("Ulmo: finding the unusual words", section=S_LANG,
          figures=[Fig("ulmo_outliers.png", placeholder="[MBARI 5 / Kraw 31]")]),
    Slide("Enki: filling in the missing words", section=S_LANG,
          figures=[Fig("enki_reconstruction.png", placeholder="[MBARI 33/35]")]),
    Slide("It was language all along", section=S_LANG,
          placeholder="MBARI 14 'AI: a new language for science' + LLM link"),
    Slide("Math is a language too", section=S_LANG,
          figures=[Fig("lample_charton.png", placeholder="NEW (B4c): Lample & Charton bar chart")],
          notes="Lample & Charton 2020 (FAIR): integration 98–99.6% vs Mathematica 84%."),
    # ------------------------------------------------------------- Claude
    Slide("", kind=IMAGE, section=S_CLAUDE,
          figures=[Fig("launch_art.png", placeholder="'And then this happened' [MBARI 6]")],
          notes="And then this happened..."),
    Slide("November 2025: Claude will surpass me", section=S_CLAUDE,
          placeholder="Quote: 'codes better than me and all of my science colleagues – put together!'"),
    Slide("June 13, 2026: Claude surpassed me", section=S_CLAUDE,
          figures=[Fig("sacbee.png", placeholder="SacBee op-ed screenshot [CI]")],
          notes="VLT technical justification better than a 10-astronomer team; caught their error."),
    Slide("I will never write another line of code", section=S_CLAUDE,
          figures=[Fig("loc_over_time.png", placeholder="~/bin loc_over_time.png")],
          notes="674k lines 1995–2026; 49k AI-generated after 13 Jun 2026."),
    Slide("Writing: proposals and papers", section=S_CLAUDE,
          figures=[Fig("a5_arxiv.png", placeholder="arXiv flood [CI]"),
                   Fig("a6_proposals.png", placeholder="15 identical proposals [CI]")]),
    Slide("Claude's PhD: waiting on the committee to grade", section=S_CLAUDE,
          figures=[Fig("fig01_inverse_problem.png", placeholder="Claude's PhD fig01")]),
    # --------------------------------------------------------------- risk
    Slide("Nothing more powerful than Fable in the wild", section=S_RISK,
          figures=[Fig("a2_bio_uplift.png", placeholder="bio uplift [CI]")],
          notes="Gates quote (Fortune, 30 Sep 2026)."),
    Slide("...and cyber", section=S_RISK,
          figures=[Fig("a3_hacking.png", placeholder="hacking [CI]")]),
    Slide("What can be done", section=S_RISK,
          bullets=["Strict liability for AI harms", "Tiered regulation, with a kill switch",
                   "Compute caps, with international verification"]),
    # ------------------------------------------------------ AI needs data
    Slide("AI needs data", section=S_DATA,
          figures=[Fig("s4_senses.png", placeholder="senses [CI]")],
          notes="'It doesn't have the data' — my wife, Nov 2025."),
    Slide("Watching the ocean from within: BGC-Argo + PACE", section=S_DATA,
          figures=[Fig("pab_infographic.png", placeholder="PAB infographic [MBARI 40]")]),
    Slide("BOONUS: a weather map for our coastal ocean", section=S_DATA,
          placeholder="BOONUS one-pager framing (+ glider image)"),
    Slide("Coupling observations to models with AI", section=S_DATA,
          figures=[Fig("ai_da_timeline.png", placeholder="BOONUS ai_da_timeline.png")]),
    # ---------------------------------------------------------- WMKO + AI
    Slide("WMKO + AI: reading the manual, building new optics", section=S_WMKO,
          figures=[Fig("hinz_slumping.png", placeholder="Hinz slide 2 (glass slumping)")],
          notes="Slide courtesy of Phil Hinz (KASM: Keck Adaptive Secondary Mirror, 3106 actuators)."),
    Slide("The Holy Grail: every Keck spectrograph, calibrated blind", section=S_WMKO,
          figures=[Fig("holy_grail_arc.png", placeholder="pr_figure_2panels.png")],
          notes="Anthropic AI for Science grant; news.ucsc.edu/2026/09/prochaska-ai-science-grant/"),
    Slide("Re-finding Keck's first planet in 12 days", section=S_WMKO,
          figures=[Fig("fig7_three_ways.png", placeholder="first-hires-exoplanet fig7")]),
    Slide("You could do this (and so could a classroom)", section=S_WMKO,
          figures=[Fig("exo_public_1.png", placeholder="public_summary slide 1"),
                   Fig("exo_public_2.png", placeholder="public_summary slide 2")]),
    # -------------------------------------------------------------- close
    Slide("Why science isn't hard", section=S_CLOSE,
          notes="Title only — author fills in (the book)."),
    Slide("Summary", section=S_CLOSE,
          bullets=["Sea and sky: data-driven exploration of the unknown",
                   "AI accelerates analysis — not (yet) data collection"]),
    # ------------------------------------------------------------- backup
    Slide("Backup", kind=DIVIDER, section="Backup", backup=True, notes="Backup slides."),
    Slide("KCWI: Lyα and Hα", section="Backup", backup=True,
          placeholder="KCWI Lyα / Hα figure (proposal in progress)"),
    Slide("It takes a village", section="Backup", backup=True,
          figures=[Fig("team_ai_remote_sensing.png", placeholder="AI on Remote Sensing team [MBARI 4]")]),
]
