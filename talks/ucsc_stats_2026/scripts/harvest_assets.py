"""Created by JXP and Claude.

Harvest the figures for the UCSC Stats 2026 deck into talks/ucsc_stats_2026/figures/
(Build #2 of claude_prompts/stats_ucsc_2026.md) and record each one in
figures/sources.json and figures/credits.md.

Sources
-------
- pictures lifted from two earlier decks in context/ (python-pptx, chosen by
  slide number and shape id; the deck's own crop rectangle is applied);
- figure crops from the three papers in context/papers/ (PyMuPDF, boxes as
  page fractions, origin top-left, rendered at DPI);
- copies of figures made elsewhere (wmko_2026, EPFT-UP, the PAB report site's
  representative BING 2.0 fits to real PACE spectra at BGC-Argo floats);
- the UCSC ROMS 4D-Var SST analysis downloaded from oceanmodeling.ucsc.edu
  (CC BY 3.0; the newest date that exists, searching back from today).

Run (ocean14 env, from the repo root):
    python talks/ucsc_stats_2026/scripts/harvest_assets.py [--no-download]
"""
import argparse
import datetime as dt
import io
import json
import shutil
import urllib.request
import ssl
from pathlib import Path

import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

HERE = Path(__file__).resolve().parent
TALK = HERE.parent
REPO = TALK.parent.parent
FIGS = TALK / "figures"
CONTEXT = REPO / "context"
PAPERS = CONTEXT / "papers"
DPI = 250
ROBOTO = REPO / "sms_outreach" / "slides" / "data" / "Roboto.ttf"

NU = CONTEXT / "NU_2026_talk.pptx"
AWOC = CONTEXT / "AWOC_2025.pptx"
NU_VIA = "via NU_2026_talk.pptx (J. X. Prochaska, 2026)"
AWOC_VIA = "via AWOC_2025.pptx (J. X. Prochaska, 2025)"
HOFF = "Hoffmann, James, Prochaska, Pastor-Marazuela, Sharma & Connor 2026, arXiv:2609.27282"
BING = "Prochaska & Frouin 2025, Biogeosciences 22, 4705, doi:10.5194/bg-22-4705-2025 (CC BY 4.0)"
KRAMER = "Kramer, Siegel, Maritorena & Catlett 2022, Remote Sens. Environ. 270, 112879, doi:10.1016/j.rse.2021.112879 (CC BY)"
PAB_FIGS = Path("~/Oceanography/python/PAB/report_site/_static/figures").expanduser()
PAB_CREDIT = ("BING 2.0 fit to a real PACE OCI (L2 AOP V3.2) spectrum at a BGC-Argo float, PAB v2 "
              "representative fit (A. James, J. X. Prochaska et al. 2026, in prep.; PAB report site)")
ROMS_URL = "https://oceanmodeling.ucsc.edu/ccsnrt/webplots/da/SST/SST_{date}.png"
ROMS_CREDIT = ("UCSC Ocean Modeling and Data Assimilation group (C. A. Edwards, A. M. Moore), "
               "oceanmodeling.ucsc.edu, CC BY 3.0")

# (output name, deck, slide number, shape id, credit, slide it serves)
# Names in RAW are extracted without the deck's crop (the deck showed one panel of a larger figure).
RAW = {"awoc_bing_fit_sim.png", "awoc_three_models.png", "awoc_pace_fit.png"}
LIFT = [
    ("nu_lorimer_burst.png", NU, 15, 282, f"Lorimer et al. 2007, Science 318, 777 {NU_VIA}", "A multi-pronged attack"),
    ("nu_ne2001.png", NU, 16, 301, f"NE2001 Galactic electron model (Cordes & Lazio 2002) {NU_VIA}", "Dispersion measure"),
    ("nu_path_image.png", NU, 21, 402, f"PATH host association (Aggarwal et al. 2021; Bannister et al. 2019 field) {NU_VIA}", "PATH"),
    ("nu_host_spectra.png", NU, 21, 400, f"Keck/KCWI and Gemini/GMOS host spectra (Bannister et al. 2019) {NU_VIA}", "Redshift"),
    ("nu_macquart_2020.png", NU, 22, 412, f"Macquart et al. 2020, Nature 581, 391 {NU_VIA}", "Backup: Macquart 2020"),
    ("nu_macquart_2026.png", NU, 23, 425, f"Localized FRBs to 2026, compiled by J. X. Prochaska {NU_VIA}", "A multi-pronged attack; Results"),
    ("nu_dm_cliff.png", NU, 27, 463, f"p(DM_EG, z) from zdm (James et al. 2022) {NU_VIA}", "Population modeling: the model"),
    ("nu_baptista_F.png", NU, 28, 482, f"Baptista et al. 2024, ApJ {NU_VIA}", "Backup: F and feedback"),
    ("nu_connor_feedback.png", NU, 30, 503, f"Connor et al. 2025 (DSA-110) {NU_VIA}", "Backup: F and feedback"),
    ("nu_tau_cdf.png", NU, 47, 683, f"Scott et al. 2025 {NU_VIA}", "Backup: scattering"),
    ("nu_whost.png", NU, 48, 697, f"James et al. 2026 {NU_VIA}", "Backup: scattering"),
    ("nu_nfrb_vs_year.png", NU, 49, 705, f"FRB discoveries per year, compiled by J. X. Prochaska {NU_VIA}", "It starts with a radio telescope"),
    ("nu_outrigger_loc.png", NU, 50, 717, f"CHIME/FRB outrigger localization on a DECaLS image {NU_VIA}", "Localization"),
    ("nu_outrigger_photo.png", NU, 50, 718, f"CHIME outrigger photo (CHIME/FRB collaboration; owner to confirm) {NU_VIA}", "Localization"),
    ("nu_h0_contours.png", NU, 55, 786, f"p(DM_EG, z) for H0 = 60, 70, 80 from zdm (James et al. 2022) {NU_VIA}", "Backup: H0"),
    ("awoc_bing_fit_sim.png", AWOC, 7, 141, f"BING fit to a Loisel et al. 2023 Hydrolight spectrum with PACE noise {AWOC_VIA}", "(spare)"),
    ("awoc_corner.png", AWOC, 9, 167, f"BING 5-parameter posterior (emcee) {AWOC_VIA}", "Standard MCMC"),
    ("awoc_three_models.png", AWOC, 10, 175, f"k=5 / GIOP / GSM fits to one simulated PACE spectrum ({BING}, Fig. 10) {AWOC_VIA}", "Infinite templates I, II"),
    ("awoc_giop_bias.png", AWOC, 14, 211, f"GIOP retrievals vs truth with MODIS noise ({BING}, Fig. B4) {AWOC_VIA}", "(spare)"),
    ("awoc_dbic.png", AWOC, 15, 221, f"ΔBIC CDFs ({BING}, Fig. 6) {AWOC_VIA}", "Backup: ΔBIC"),
    ("awoc_pace_fit.png", AWOC, 17, 239, f"BING fit to a real PACE OCI v3 spectrum, pixel 1902368_013 {AWOC_VIA}", "PACE; Strong systematics; Poorly measured errors"),
    ("awoc_pab_matchups.png", AWOC, 20, 271, f"PACE × BGC-Argo match-ups (A. James et al. 2026, in prep.) {AWOC_VIA}", "Where do we take new data?"),
    ("awoc_pab_dbbp.png", AWOC, 21, 277, f"Relative Δb_bp, PACE minus BGC-Argo (A. James et al. 2026, in prep.) {AWOC_VIA}", "Poorly measured errors"),
]
# raw (uncropped) copies of the same source image, with a different crop applied
# (fractions left, top, right, bottom of the ORIGINAL image to keep)
SUBCROPS = [
    ("awoc_pace_fit_rrs.png", "awoc_pace_fit.png", (0.03, 0.10, 0.475, 0.56), "PACE; Strong systematics; Poorly measured errors"),
    ("ocean_sketch_forward.png", "ocean_sketch.png", (0.0, 0.0, 0.5, 1.0), "What is in the water?"),
    ("awoc_three_models_rrs.png", "awoc_three_models.png", (0.0, 0.0, 0.5, 0.5), "Infinite templates I"),
    ("awoc_three_models_bb.png", "awoc_three_models.png", (0.0, 0.5, 0.5, 1.0), "Infinite templates II"),
    ("awoc_three_models_aph.png", "awoc_three_models.png", (0.5, 0.0, 1.0, 0.5), "Infinite templates II"),
]
# trims of copied or downloaded files (fractions left, top, right, bottom to keep)
TRIMS = [
    ("moana_pc_loadings.png", (0.0, 0.085, 1.0, 1.0)),      # drop the file-name suptitle
    ("roms_sst_nowcast.png", (0.0, 0.085, 1.0, 0.935)),    # drop the title and footer lines
    ("pab_fit_5906450_140.png", (0.0, 0.04, 1.0, 0.49)),   # keep the R_rs panel, drop the fit-id title
    ("pab_fit_5907252_5.png", (0.0, 0.04, 1.0, 0.49)),
]
# telescope montage: (shape id, label)
TELESCOPES = [(4, 140, "MeerKAT"), (4, 141, "CHIME"), (4, 145, "ASKAP"), (14, 276, "Parkes")]   # (slide, shape id, name)
TELESCOPE_CREDIT = ("Telescope photos (MeerKAT: SARAO; CHIME: CHIME collaboration; ASKAP: CSIRO; "
                    "Parkes/Murriyang: CSIRO; owners to confirm) " + NU_VIA)

# (output name, pdf, page (1-based), box (x0, y0, x1, y1) as page fractions, credit, slide)
CROPS = [
    ("hoffmann_fig1_corner.png", "hoffmann2026.pdf", 6, (0.05, 0.13, 0.93, 0.79), f"Fig. 1 of {HOFF}", "Population modeling: MCMC"),
    ("hoffmann_fig1_nsfr_alpha.png", "hoffmann2026.pdf", 6, (0.05, 0.115, 0.26, 0.265), f"Fig. 1 (detail) of {HOFF}", "(spare)"),
    ("hoffmann_fig2_repetition.png", "hoffmann2026.pdf", 7, (0.04, 0.515, 0.48, 0.86), f"Fig. 2 of {HOFF}", "Backup: repetition"),
    ("hoffmann_fig3_chime_cdf.png", "hoffmann2026.pdf", 10, (0.51, 0.14, 0.93, 0.37), f"Fig. 3 of {HOFF}", "Results to date"),
    ("bing_fig4_degeneracy.png", "bing.pdf", 8, (0.08, 0.08, 0.92, 0.35), f"Fig. 4 of {BING}", "A physical degeneracy"),
    ("bing_fig8_beta_prior.png", "bing.pdf", 12, (0.17, 0.46, 0.84, 0.60), f"Fig. 8 (bottom row) of {BING}", "(spare)"),
    ("bing_fig10_priors.png", "bing.pdf", 14, (0.17, 0.08, 0.83, 0.29), f"Fig. 10 (a, b) of {BING}", "Priors"),
    ("bing_fig11_aph.png", "bing.pdf", 15, (0.19, 0.08, 0.485, 0.305), f"Fig. 11 (a) of {BING}", "Priors"),
    ("bing_fig6_dbic.png", "bing.pdf", 10, (0.17, 0.08, 0.83, 0.30), f"Fig. 6 of {BING}", "(spare)"),
    ("kramer_fig5_method.png", "kramer2022.pdf", 7, (0.067, 0.420, 0.936, 0.605), f"Fig. 5 (top row) of {KRAMER}", "Second derivative + PCA"),
    ("kramer_fig6_results.png", "kramer2022.pdf", 9, (0.165, 0.071, 0.834, 0.330), f"Fig. 6 (A, B) of {KRAMER}", "Second derivative + PCA"),
]
COPIES = [
    ("pace_moana.png", REPO / "talks" / "wmko_2026" / "figures" / "pace_moana.png",
     "NASA PACE OCI, MOANA picophytoplankton (Lange et al. 2020), L3 mapped daily, 1 July 2025 (NASA/GSFC/OBPG); "
     "figure made for talks/wmko_2026", "What is in the water?; PFTs"),
    ("moana_pc_loadings.png", Path("~/Oceanography/python/EPFT-UP/reports/figures/moana_pc_loadings.png").expanduser(),
     "MOANA PCA basis (Lange et al. 2020) re-derived in EPFT-UP (J. X. Prochaska & Claude, 2026)", "PCA of the spectrum"),
    # PAB v2 representative fits (B7): the median sat/float b_bp ratio, and the most productive tercile
    ("pab_fit_5906450_140.png",
     PAB_FIGS / "5906450_140_PACE_OCI.20250829T213217.L2.OC_AOP.V3_2.nc_1210_1019_ExpBPow_v2.0_fit.png",
     f"{PAB_CREDIT}: float 5906450 cycle 140, 29 Aug 2025, the median sat/float b_bp matchup", "PACE"),
    ("pab_fit_5907252_5.png",
     PAB_FIGS / "5907252_5_PACE_OCI.20260413T173323.L2.OC_AOP.V3_2.nc_573_956_ExpBPow_v2.0_fit.png",
     f"{PAB_CREDIT}: float 5907252 cycle 5, 13 Apr 2026, the most productive tercile (Chl 0.32 mg m⁻³)", "Strong systematics"),
    ("pab_bbp_scatter.png", PAB_FIGS.parent / "comparisons" / "bbp_scatter.png",
     "PACE/BING vs. BGC-Argo float b_bp(700 nm), 15,274 PAB v2 matchups (A. James, J. X. Prochaska et al. 2026, "
     "in prep.; PAB report site, built 2026-10-18)", "Poorly measured errors"),
]


def find_shape(shapes, shape_id):
    """Created by JXP and Claude. The shape with `shape_id`, searching groups."""
    for sh in shapes:
        if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
            hit = find_shape(sh.shapes, shape_id)
            if hit is not None:
                return hit
        elif sh.shape_id == shape_id:
            return sh
    return None


def picture_image(deck, slide_no, shape_id, apply_crop=True):
    """Created by JXP and Claude. The picture on `slide_no` with `shape_id` as a
    PIL image, with the deck's crop rectangle applied."""
    prs = Presentation(str(deck))
    sh = find_shape(prs.slides[slide_no - 1].shapes, shape_id)
    if sh is None:
        raise KeyError(f"{deck.name} slide {slide_no}: no shape {shape_id}")
    im = Image.open(io.BytesIO(sh.image.blob))
    if apply_crop and any(c > 0 for c in (sh.crop_left, sh.crop_right, sh.crop_top, sh.crop_bottom)):
        w, h = im.size
        im = im.crop((int(round(sh.crop_left * w)), int(round(sh.crop_top * h)),
                      int(round((1 - sh.crop_right) * w)), int(round((1 - sh.crop_bottom) * h))))
    return im


def flatten(im):
    """Created by JXP and Claude. RGB on white (transparent PNGs otherwise go black)."""
    if im.mode in ("RGBA", "LA") or (im.mode == "P" and "transparency" in im.info):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        return bg
    return im.convert("RGB")


def montage(deck, items, out):
    """Created by JXP and Claude. 2 x 2 montage of photos, centre-cropped to 16:9."""
    tiles = []
    for slide_no, shape_id, label in items:
        im = flatten(picture_image(deck, slide_no, shape_id))
        tiles.append((im, label))
    cell_w, cell_h = 900, 506          # 16:9 tiles; the slide caption names the telescopes
    sheet = Image.new("RGB", (2 * cell_w + 20, 2 * cell_h + 20), "white")
    for k, (im, label) in enumerate(tiles):
        w, h = im.size
        if w / h > cell_w / cell_h:        # centre-crop to 16:9
            nw = int(h * cell_w / cell_h)
            im = im.crop(((w - nw) // 2, 0, (w - nw) // 2 + nw, h))
        else:
            nh = int(w * cell_h / cell_w)
            im = im.crop((0, (h - nh) // 2, w, (h - nh) // 2 + nh))
        im = im.resize((cell_w, cell_h), Image.LANCZOS)
        sheet.paste(im, ((k % 2) * (cell_w + 20), (k // 2) * (cell_h + 20)))
    sheet.save(out, optimize=True)


def crop_pdf(pdf, page_no, box, out, dpi=DPI):
    """Created by JXP and Claude. Render a region of a PDF page to PNG."""
    doc = fitz.open(str(pdf))
    page = doc[page_no - 1]
    r = page.rect
    clip = fitz.Rect(r.x0 + box[0] * r.width, r.y0 + box[1] * r.height,
                     r.x0 + box[2] * r.width, r.y0 + box[3] * r.height)
    page.get_pixmap(dpi=dpi, clip=clip, alpha=False).save(str(out))
    doc.close()


def download_roms(out, days_back=14):
    """Created by JXP and Claude. The newest ROMS SST analysis image; returns its date."""
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE   # the site's certificate chain is incomplete
    today = dt.date.today()
    for k in range(days_back):
        d = today - dt.timedelta(days=k)
        url = ROMS_URL.format(date=d.strftime("%Y%m%d"))
        try:
            with urllib.request.urlopen(url, timeout=20, context=ctx) as r:
                blob = r.read()
        except Exception:
            continue
        if blob[:8] == b"\x89PNG\r\n\x1a\n":
            out.write_bytes(blob)
            return d
    raise RuntimeError("no ROMS SST image found in the last two weeks")


def main(argv=None):
    """Created by JXP and Claude. Harvest everything and write the manifests."""
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-download", action="store_true", help="skip the ROMS download")
    args = ap.parse_args(argv)
    FIGS.mkdir(exist_ok=True)
    manifest_path = FIGS / "sources.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    rows = []
    fresh = set()        # files written in this run (the only ones TRIMS may touch)

    def record(name, origin, source, slide, **extra):
        entry = {"slide": slide, "source": source, "origin": origin}
        entry.update(extra)
        manifest[name] = entry
        rows.append((name, origin, source))

    for name, deck, slide_no, shape_id, credit, slide in LIFT:
        im = flatten(picture_image(deck, slide_no, shape_id, apply_crop=name not in RAW))
        im.save(FIGS / name, optimize=True)
        record(name, "lifted", credit, slide, deck=deck.name, deck_slide=slide_no, shape_id=shape_id)
        print(f"lifted   {name:32s} {im.size[0]}x{im.size[1]}")
    for name, src, (l, t, r, b), slide in SUBCROPS:
        im = Image.open(FIGS / src)
        w, h = im.size
        im = im.crop((int(l * w), int(t * h), int(r * w), int(b * h)))
        im.save(FIGS / name, optimize=True)
        record(name, "lifted", manifest[src]["source"] + " (panel)", slide, crop_of=src)
        print(f"subcrop  {name:32s} {im.size[0]}x{im.size[1]}")
    montage(NU, TELESCOPES, FIGS / "telescopes_montage.png")
    record("telescopes_montage.png", "lifted", TELESCOPE_CREDIT, "It starts with a radio telescope", deck=NU.name, deck_slides=[4, 14])
    print("montage  telescopes_montage.png")
    for name, pdf, page_no, box, credit, slide in CROPS:
        crop_pdf(PAPERS / pdf, page_no, box, FIGS / name)
        record(name, "cropped", credit, slide, pdf=pdf, page=page_no, box=list(box))
        print(f"cropped  {name:32s} {pdf} p{page_no}")
    for name, src, credit, slide in COPIES:
        shutil.copyfile(src, FIGS / name)
        fresh.add(name)
        record(name, "copied", credit, slide, copied_from=str(src))
        print(f"copied   {name}")
    if not args.no_download:
        d = download_roms(FIGS / "roms_sst_nowcast.png")
        fresh.add("roms_sst_nowcast.png")
        record("roms_sst_nowcast.png", "downloaded", f"{ROMS_CREDIT}; SST analysis for {d.isoformat()}",
               "A model ocean constrained by data", url=ROMS_URL.format(date=d.strftime("%Y%m%d")), date=d.isoformat())
        print(f"download roms_sst_nowcast.png ({d})")

    for name, (l, t, r, b) in TRIMS:      # idempotent: only files (re)written above
        f = FIGS / name
        if name in fresh:
            im = Image.open(f)
            w, h = im.size
            im.crop((int(l * w), int(t * h), int(r * w), int(b * h))).save(f, optimize=True)
            manifest[name]["trimmed"] = [l, t, r, b]
            print(f"trimmed  {name}")
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")
    lines = ["# Figure credits — UCSC Stats 2026", "",
             "Written by `scripts/harvest_assets.py`; the full record is `sources.json`.  "
             "Credits appear in the speaker notes, not on the slides.", "",
             "| File | Origin | Source / credit |", "|---|---|---|"]
    for name, origin, source in rows:
        lines.append(f"| {name} | {origin} | {source} |")
    lines += ["", "Generated here (see `sources.json`): " +
              ", ".join(sorted(k for k, v in manifest.items() if v.get("origin") == "generated"))]
    (FIGS / "credits.md").write_text("\n".join(lines) + "\n")
    print(f"wrote {manifest_path} ({len(manifest)} entries) and credits.md")


if __name__ == "__main__":
    main()
