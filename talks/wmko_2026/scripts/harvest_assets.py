"""Created by JXP and Claude.

Gather every existing image the WMKO 2026 plan needs into
talks/wmko_2026/figures/, and record each one's origin, credit and license
in figures/sources.json and figures/credits.md.

Each entry of ASSETS maps a target file name (as used in slides/plan.py) to
one source:
    File(path)                          copy a file
    Picture(pptx, slide, pick)          extract an embedded picture from a deck
                                        (pick = index among the slide's pictures in
                                        shape order, or "largest")
    SlideImage(pptx, slide)             render a whole slide (LibreOffice -> PDF -> PNG)
    Url(url)                            download
and optional `crop` = (left, top, right, bottom) as fractions of the image.

Usage (ocean14 env, from the repo root):
    python talks/wmko_2026/scripts/harvest_assets.py [--only NAME ...] [--force]
Existing targets are skipped unless --force.  Rendered decks are cached in
figures/.cache/ (git-ignored).
"""
import argparse
import io
import json
import shutil
import subprocess
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from PIL import Image
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

TALK = Path(__file__).resolve().parents[1]
REPO = TALK.parents[1]
FIGS = TALK / "figures"
CACHE = FIGS / ".cache"
HOME = Path.home()

KRAW = HOME / "Projects/ClimateIntelligence/presentations/2026_WMKO/Kraw_2024.pptx"
MBARI = REPO / "context/MBARI_2026.pptx"
HONO = REPO / "context/Honokaʻa_HS_2026.pptx"
HINZ = REPO / "context/Integrating Claude into instrumentation research.pptx"
CI_FIGS = HOME / "Projects/ClimateIntelligence/presentations/2026_WMKO/figs"
EXO = HOME / "Projects/PypeIt/first-hires-exoplanet"
UA = "Mozilla/5.0 (sms-outreach harvest_assets; jxp@ucsc.edu)"


@dataclass
class File:
    path: Path


@dataclass
class Picture:
    pptx: Path
    slide: int
    pick: object = "largest"


@dataclass
class SlideImage:
    pptx: Path
    slide: int
    dpi: int = 200


@dataclass
class Url:
    url: str


@dataclass
class Asset:
    """Created by JXP and Claude. One target image and where it comes from."""
    src: object
    source: str             # what it is / where it is from (for notes and credits.md)
    credit: str = ""
    license: str = ""
    crop: tuple = None      # (left, top, right, bottom) fractions


# ----------------------------------------------------------------- ASSETS
# Filled from the B2 survey of each deck / repo / web page (see the log).
ASSETS = {
}


# ---------------------------------------------------------------- helpers
def pictures(slide):
    """Created by JXP and Claude. Picture shapes on a slide in shape order
    (descending into groups)."""
    out = []

    def walk(shapes):
        for sh in shapes:
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                walk(sh.shapes)
            elif sh.shape_type == MSO_SHAPE_TYPE.PICTURE or hasattr(sh, "image"):
                try:
                    sh.image
                except (AttributeError, ValueError):
                    continue
                out.append(sh)
    walk(slide.shapes)
    return out


_DECKS = {}


def open_deck(path):
    """Created by JXP and Claude. python-pptx Presentation, cached per path."""
    if path not in _DECKS:
        _DECKS[path] = Presentation(str(path))
    return _DECKS[path]


def extract_picture(src):
    """Created by JXP and Claude. (bytes, extension) of an embedded picture."""
    slide = open_deck(src.pptx).slides[src.slide - 1]
    pics = pictures(slide)
    if not pics:
        raise ValueError(f"{src.pptx.name} slide {src.slide}: no pictures")
    if src.pick == "largest":
        pic = max(pics, key=lambda p: p.image.size[0] * p.image.size[1])
    else:
        pic = pics[src.pick]
    return pic.image.blob, pic.image.ext


def render_slide(src):
    """Created by JXP and Claude. PNG bytes of one slide rendered with
    LibreOffice (the deck's PDF is cached)."""
    CACHE.mkdir(parents=True, exist_ok=True)
    pdf = CACHE / (src.pptx.stem + ".pdf")
    if not pdf.exists():
        subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", str(CACHE), str(src.pptx)],
                       check=True, capture_output=True)
    stem = CACHE / f"{src.pptx.stem}_s{src.slide}"
    subprocess.run(["pdftoppm", "-r", str(src.dpi), "-f", str(src.slide), "-l", str(src.slide), "-png",
                    "-singlefile", str(pdf), str(stem)], check=True)
    return Path(str(stem) + ".png").read_bytes(), "png"


def download(src):
    """Created by JXP and Claude. Bytes of a URL (with a polite User-Agent)."""
    req = urllib.request.Request(src.url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=60) as r:
        data = r.read()
    return data, src.url.rsplit(".", 1)[-1].split("?")[0].lower()


def fetch(asset):
    """Created by JXP and Claude. (bytes, extension) for an asset's source."""
    src = asset.src
    if isinstance(src, File):
        return Path(src.path).read_bytes(), Path(src.path).suffix.lstrip(".").lower()
    if isinstance(src, Picture):
        return extract_picture(src)
    if isinstance(src, SlideImage):
        return render_slide(src)
    if isinstance(src, Url):
        return download(src)
    raise TypeError(src)


def write_image(name, data, crop):
    """Created by JXP and Claude. Save `data` as figures/<name>, converting
    the format to match the target extension and applying `crop`."""
    out = FIGS / name
    im = Image.open(io.BytesIO(data))
    if crop:
        l, t, r, b = crop
        w, h = im.size
        im = im.crop((round(l * w), round(t * h), round(r * w), round(b * h)))
    if out.suffix.lower() in (".jpg", ".jpeg"):
        im.convert("RGB").save(out, quality=92)
    else:
        if im.mode == "CMYK":
            im = im.convert("RGB")
        im.save(out)
    return out, im.size


def describe(src):
    """Created by JXP and Claude. Short human-readable origin of a source."""
    if isinstance(src, File):
        return str(Path(src.path)).replace(str(HOME), "~")
    if isinstance(src, Picture):
        return f"{src.pptx.name}, slide {src.slide}, picture {src.pick}"
    if isinstance(src, SlideImage):
        return f"{src.pptx.name}, slide {src.slide} (rendered)"
    return src.url


def write_manifests():
    """Created by JXP and Claude. Update sources.json (keeping entries made
    by figure scripts) and rewrite credits.md from ASSETS."""
    manifest_path = FIGS / "sources.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    for name, a in ASSETS.items():
        entry = manifest.get(name, {})
        entry.update({"origin": describe(a.src), "source": a.source, "credit": a.credit, "license": a.license})
        manifest[name] = entry
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    lines = ["# Image credits — WMKO 2026 \"Sea meets the stars\"", "",
             "Generated by `talks/wmko_2026/scripts/harvest_assets.py`; figures made by our own scripts "
             "are listed in `sources.json` with origin `generated`.", "",
             "| File | What | Credit | License | Origin |", "|---|---|---|---|---|"]
    for name, a in sorted(ASSETS.items()):
        cells = [name, a.source, a.credit or "—", a.license or "—", describe(a.src)]
        lines.append("| " + " | ".join(c.replace("|", "/") for c in cells) + " |")
    (FIGS / "credits.md").write_text("\n".join(lines) + "\n")


def main():
    """Created by JXP and Claude. Harvest all (or --only) assets."""
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--only", nargs="+", help="target names to (re)harvest")
    p.add_argument("--force", action="store_true", help="overwrite existing targets")
    args = p.parse_args()
    FIGS.mkdir(parents=True, exist_ok=True)
    names = args.only or sorted(ASSETS)
    failed = []
    for name in names:
        out = FIGS / name
        if out.exists() and not args.force:
            print(f"skip   {name} (exists)")
            continue
        try:
            data, _ = fetch(ASSETS[name])
            out, size = write_image(name, data, ASSETS[name].crop)
            print(f"wrote  {name:28s} {size[0]}x{size[1]}  <- {describe(ASSETS[name].src)}")
        except Exception as err:  # keep going; report at the end
            failed.append(name)
            print(f"FAILED {name}: {err}")
    write_manifests()
    print(f"{len(names) - len(failed)} ok, {len(failed)} failed {failed if failed else ''}")
    shutil.rmtree(CACHE / "tmp", ignore_errors=True)


if __name__ == "__main__":
    main()
