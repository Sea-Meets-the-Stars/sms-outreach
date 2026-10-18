"""Created by JXP and Claude.

Build a Kraw-style deck from a template and a list of `spec.Slide`.

Kraw content slides do not use title placeholders: each is the 'TITLE'
layout with its placeholders deleted, a Roboto 38 pt bold centred title text
box at the top and a Roboto 25 pt sub-line text box at the bottom.  To match
exactly, the builder deep-copies those two boxes (and the slide-number
placeholder) from Kraw slide 3 and reuses them on every new slide.  Kraw
slide 1 (title + sea|sky hero image) is kept as the title slide; every other
Kraw slide is dropped, which also drops its media.

Shape names written here (used by `qa`):
    Title, Sub-line, Figure, Caption, Bullets, Source, PLACEHOLDER, Footer

Text markup: `H_{0}` renders "0" as a subscript run and `10^{8}` renders
"8" as a superscript run (titles, sub-lines, bullets, captions); the width
estimates in `layout` strip the markup.  A plan may set FOOTER (e.g. "UCSC
Stats 2026-10-19"): the master's "UC SANTA CRUZ | Science" logo is replaced
by that text and, on the title slide, the word "Science" in the top band is
covered by it.
"""
import copy
import hashlib
import json
import re
import tempfile
from pathlib import Path

from lxml import etree
from PIL import Image, ImageOps
from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, PP_ALIGN
from pptx.util import Emu, Inches, Pt

from . import layout as L
from .spec import CONTENT, DIVIDER, IMAGE, TITLE

CONTENT_LAYOUT = "TITLE"                                            # what Kraw's content slides use
TITLE_BOX_TEXT = "Deciphering our past"                             # Kraw slide 3 title
SUBLINE_BOX_TEXT = "How did we get here?  What are our origins?"    # Kraw slide 3 sub-line
SLIDE_NUMBER_IDX = 12
AUTHOR_IDX, SUBTITLE_IDX, TITLE_IDX = 4, 3, 0                       # Kraw slide 1 placeholders
DIVIDER_TOP = 2.0

INK = RGBColor(0x22, 0x22, 0x22)
GREY = RGBColor(0x66, 0x66, 0x66)
RED = RGBColor(0xD0, 0x1C, 0x1C)
PLACEHOLDER_FILL = RGBColor(0xFD, 0xEC, 0xEC)

MAX_PX = 2200                 # larger images are downsampled (copies only); 2200 keeps style.FULL @ 220 dpi as-is
MAX_BYTES = 600_000

A = "{http://schemas.openxmlformats.org/drawingml/2006/main}"
P = "{http://schemas.openxmlformats.org/presentationml/2006/main}"

MARKUP = re.compile(r"([_^])\{([^}]*)\}")
BASELINE = {"sub": "-25000", "sup": "30000"}        # OOXML baseline offsets (1/1000 %)
LOGO_TITLE = "Science Logo"                         # cNvPr title of the master's footer logo
FOOTER_BLUE = RGBColor(0x00, 0x3C, 0x6C)             # the Kraw band colour (sampled from the master)
FOOTER_PT, FOOTER_W = 11, 3.2
TITLE_BAND_COVER = (2.12, 0.33, 2.9, 0.47)          # title slide: box over the word "Science"
TITLE_BAND_TEXT = (2.17, 0.40, 2.8, 0.33)
TITLE_BAND_PT = 15


# ----------------------------------------------------------------- helpers
def runs_of(text):
    """Created by JXP and Claude. Split `text` on the subscript / superscript
    markup: [(piece, kind)] with kind None, 'sub' or 'sup'."""
    out, pos = [], 0
    for m in MARKUP.finditer(text):
        if m.start() > pos:
            out.append((text[pos:m.start()], None))
        out.append((m.group(2), "sub" if m.group(1) == "_" else "sup"))
        pos = m.end()
    if pos < len(text):
        out.append((text[pos:], None))
    return out or [("", None)]


def find_shape(slide, text):
    """Created by JXP and Claude. The shape on `slide` whose text is `text`."""
    for sh in slide.shapes:
        if sh.has_text_frame and sh.text_frame.text.strip() == text:
            return sh
    raise ValueError(f"shape with text {text!r} not found on template slide")


def set_size(sp_element, pt):
    """Created by JXP and Claude. Set the font size of every run in a text box."""
    for tag in ("rPr", "endParaRPr"):
        for el in sp_element.iter(f"{A}{tag}"):
            el.set("sz", str(int(pt * 100)))


def set_text(sp_element, text):
    """Created by JXP and Claude. Replace the text of a text-box element,
    keeping the first run's formatting; `text` may carry the sub / sup
    markup, which becomes baseline-shifted runs."""
    txBody = sp_element.find(f".//{P}txBody")
    paras = txBody.findall(f"{A}p")
    for p in paras[1:]:
        txBody.remove(p)
    para = paras[0]
    runs = para.findall(f"{A}r")
    for r in runs[1:]:
        para.remove(r)
    for br in para.findall(f"{A}br"):
        para.remove(br)
    run0 = runs[0]
    para.remove(run0)
    end = para.find(f"{A}endParaRPr")
    for piece, kind in runs_of(text):
        r = copy.deepcopy(run0)
        r.find(f"{A}t").text = piece
        rPr = r.find(f"{A}rPr")
        if rPr is None:
            rPr = etree.Element(f"{A}rPr")
            r.insert(0, rPr)
        if kind:
            rPr.set("baseline", BASELINE[kind])
        elif "baseline" in rPr.attrib:
            del rPr.attrib["baseline"]
        if end is not None:
            end.addprevious(r)
        else:
            para.append(r)


def next_shape_id(slide):
    """Created by JXP and Claude. A shape id not yet used on `slide`."""
    ids = [int(e.get("id")) for e in slide.shapes._spTree.iter() if e.tag.endswith("}cNvPr")]
    return max(ids + [1]) + 1


def add_box(slide, template_el, text, name, pt=None):
    """Created by JXP and Claude. Append a copy of a template text box with new text."""
    el = copy.deepcopy(template_el)
    cnv = el.find(f".//{P}cNvPr")
    cnv.set("id", str(next_shape_id(slide)))
    cnv.set("name", name)
    set_text(el, text)
    if pt:
        set_size(el, pt)
    slide.shapes._spTree.append(el)
    return slide.shapes[-1]


def drop_slides(prs, keep):
    """Created by JXP and Claude. Remove every slide whose index is not in `keep`."""
    sld_ids = prs.slides._sldIdLst
    for i, sld_id in enumerate(list(sld_ids)):
        if i not in keep:
            prs.part.drop_rel(sld_id.rId)
            sld_ids.remove(sld_id)


def layout_by_name(prs, name):
    """Created by JXP and Claude. The slide layout called `name`."""
    for lay in prs.slide_layouts:
        if lay.name == name:
            return lay
    raise ValueError(f"layout {name!r} not in template")


def resolve(name, fig_dirs):
    """Created by JXP and Claude. Path of a figure (absolute, or the first
    match in fig_dirs), or None if it does not exist yet."""
    path = Path(name).expanduser()
    if path.is_absolute():
        return path if path.exists() else None
    for d in fig_dirs:
        cand = Path(d).expanduser() / name
        if cand.exists():
            return cand
    return None


def slide_ready(path, cache_dir):
    """Created by JXP and Claude. The image as it should go on a slide.

    The original is used when it is small, upright (no EXIF rotation) and in
    a plain mode.  Otherwise a copy is written to cache_dir: EXIF-rotated,
    converted to RGB(A), downsampled to MAX_PX.  PNG sources stay PNG
    (figures keep crisp text); photos become JPEG.  Originals are untouched."""
    with Image.open(path) as im:
        rotated = im.getexif().get(0x0112, 1) not in (0, 1)
        plain = im.mode in ("RGB", "RGBA", "L", "LA", "P")
        if max(im.size) <= MAX_PX and path.stat().st_size < MAX_BYTES and plain and not rotated:
            return path
        cache_dir.mkdir(parents=True, exist_ok=True)
        small = ImageOps.exif_transpose(im)
        if small.mode not in ("RGB", "RGBA"):
            alpha = small.mode in ("LA", "PA") or (small.mode == "P" and "transparency" in small.info)
            small = small.convert("RGBA" if alpha else "RGB")
        small.thumbnail((MAX_PX, MAX_PX))
        tag = hashlib.md5(str(path.resolve()).encode()).hexdigest()[:6]
        if path.suffix.lower() == ".png" or small.mode == "RGBA":
            out = cache_dir / f"{path.stem}_{tag}_slide.png"
            small.save(out, optimize=True)
        else:
            out = cache_dir / f"{path.stem}_{tag}_slide.jpg"
            small.convert("RGB").save(out, quality=88)
    return out


def aspect_of(path):
    """Created by JXP and Claude. width / height of an image file, after EXIF rotation."""
    with Image.open(path) as im:
        w, h = im.size
        if im.getexif().get(0x0112, 1) in (5, 6, 7, 8):   # rotated by 90 degrees
            w, h = h, w
        return w / h


def add_text(slide, text, box, pt, color=INK, name="Text", align=None, bold=False, anchor=None):
    """Created by JXP and Claude. A plain Roboto text box; `text` may be a
    list of paragraphs."""
    x, y, w, h = box
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = True
    for side in ("margin_left", "margin_right", "margin_top", "margin_bottom"):
        setattr(tf, side, 0)
    if anchor:
        tf.vertical_anchor = anchor
    paras = text if isinstance(text, list) else [text]
    for k, line in enumerate(paras):
        para = tf.paragraphs[0] if k == 0 else tf.add_paragraph()
        if align:
            para.alignment = align
        for piece, kind in runs_of(line):
            run = para.add_run()
            run.text = piece
            run.font.size = Pt(pt)
            run.font.name = "Roboto"
            run.font.bold = bold
            run.font.color.rgb = color
            if kind:
                run.font._rPr.set("baseline", BASELINE[kind])
    tb.name = name
    return tb


def set_footer(prs, text):
    """Created by JXP and Claude. Replace the master's footer logo
    ("UC SANTA CRUZ | Science") with `text` in Roboto, and cover the word
    "Science" in the title slide's top band with the same text."""
    title_slide = prs.slides[0]
    for master in prs.slide_masters:
        for pic in list(master.shapes):
            cnv = pic._element.find(f".//{P}cNvPr")
            if cnv is not None and LOGO_TITLE in (cnv.get("title") or ""):
                box = (Emu(pic.left).inches, Emu(pic.top).inches, FOOTER_W, Emu(pic.height).inches)
                pic._element.getparent().remove(pic._element)
                tb = add_text(title_slide, text, box, FOOTER_PT, FOOTER_BLUE, "Footer", bold=True,
                              anchor=MSO_ANCHOR.MIDDLE)
                el = tb._element
                el.getparent().remove(el)
                master.shapes._spTree.append(el)
    x, y, w, h = TITLE_BAND_COVER
    cover = title_slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    cover.fill.solid()
    cover.fill.fore_color.rgb = FOOTER_BLUE
    cover.line.fill.background()
    cover.name = "Footer"
    band = text[5:] if text.startswith("UCSC ") else text     # the band keeps the UC SANTA CRUZ wordmark
    add_text(title_slide, band, TITLE_BAND_TEXT, TITLE_BAND_PT, RGBColor(0xFF, 0xFF, 0xFF), "Footer",
             bold=True, anchor=MSO_ANCHOR.MIDDLE)


def add_placeholder(slide, box, label):
    """Created by JXP and Claude. A red, dashed, labelled box for a figure
    that does not exist yet (counted by `qa`)."""
    x, y, w, h = box
    shp = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    shp.fill.solid()
    shp.fill.fore_color.rgb = PLACEHOLDER_FILL
    shp.line.color.rgb = RED
    shp.line.width = Pt(2)
    shp.line.dash_style = 4  # MSO_LINE_DASH_STYLE.DASH
    tf = shp.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.text = f"PLACEHOLDER\n{L.plain(label)}"
    for k, para in enumerate(tf.paragraphs):
        para.alignment = PP_ALIGN.CENTER
        for run in para.runs:
            run.font.size = Pt(20 if k == 0 else 16)
            run.font.bold = k == 0
            run.font.name = "Roboto"
            run.font.color.rgb = RED
    shp.name = "PLACEHOLDER"
    return shp


def add_figure(slide, fig, box, fig_dirs, cache_dir, fill_cell):
    """Created by JXP and Claude. Place a figure in `box` (already fitted to
    its aspect unless `fill_cell`), or a placeholder if the file is missing."""
    path = resolve(fig.path, fig_dirs)
    if path is None:
        return add_placeholder(slide, box, fig.placeholder or fig.path)
    path = slide_ready(path, cache_dir)
    if fill_cell:
        box = L.centered(aspect_of(path), box)
    x, y, w, h = box
    pic = slide.shapes.add_picture(str(path), Inches(x), Inches(y), Inches(w), Inches(h))
    pic.name = "Figure"
    return pic


def add_source(slide, source):
    """Created by JXP and Claude. Small grey right-aligned source line
    between the master's logo and the slide number."""
    pt = L.source_size(source)
    add_text(slide, source, (L.SRC_X, L.SRC_TOP, L.SRC_W, L.SRC_H), pt, GREY, "Source", align=PP_ALIGN.RIGHT)


def load_sources(fig_dirs):
    """Created by JXP and Claude. Merge the sources.json manifests found in
    fig_dirs (earlier directories win): {file name: entry}."""
    merged = {}
    for d in reversed(fig_dirs):
        manifest = Path(d) / "sources.json"
        if manifest.exists():
            merged.update(json.loads(manifest.read_text()))
    return merged


def notes_text(spec, missing, sources=None):
    """Created by JXP and Claude. Speaker notes: the plan's notes, the source
    line, each figure's full source/credit from sources.json, and any missing
    figures.  Empty when the plan gives no notes (so `qa` can flag it)."""
    parts = [L.plain(spec.notes)]
    if spec.source:
        parts.append(f"Source: {L.plain(spec.source)}")
    for fig in spec.figures:
        entry = (sources or {}).get(Path(fig.path).name)
        if entry:
            credit = "; ".join(entry[k] for k in ("source", "credit", "license") if entry.get(k))
            parts.append(f"Figure {Path(fig.path).name}: {credit}")
    if missing:
        parts.append("MISSING FIGURES: " + ", ".join(missing))
    if not any(parts):
        return ""
    head = f"[{spec.section}]" if spec.section else ""
    return "\n\n".join(p for p in [head] + parts if p)


# ---------------------------------------------------------------- builders
def fill_title_slide(slide, spec):
    """Created by JXP and Claude. Kraw slide 1: title, sub-title, author line."""
    for ph in slide.placeholders:
        idx = ph.placeholder_format.idx
        if idx == TITLE_IDX and spec.title:
            set_text(ph._element, spec.title)
        elif idx == SUBTITLE_IDX and spec.subtitle:
            set_text(ph._element, spec.subtitle)
        elif idx == AUTHOR_IDX and spec.author:
            # Kraw: one paragraph, run 0 = name, <a:br>, run 1 = affiliations
            runs = [r for para in ph.text_frame.paragraphs for r in para.runs]
            assert len(runs) == 2, f"unexpected Kraw author line: {[r.text for r in runs]}"
            runs[1].text = spec.author


def fill_content_slide(slide, spec, fig_dirs, cache_dir):
    """Created by JXP and Claude. Figures / bullets / placeholder of a CONTENT slide."""
    paths = [resolve(f.path, fig_dirs) for f in spec.figures]
    aspects = [aspect_of(p) if p else None for p in paths]
    captions = [f.caption for f in spec.figures]
    n_bullets = len(spec.bullets)
    if not spec.figures and spec.placeholder:
        boxes = L.content_boxes(spec.title, bool(spec.subtitle), [None], n_bullets)
        add_placeholder(slide, boxes["figures"][0], spec.placeholder)
    else:
        boxes = L.content_boxes(spec.title, bool(spec.subtitle), aspects, n_bullets, captions)
        for fig, box, cap_box in zip(spec.figures, boxes["figures"], boxes["captions"]):
            add_figure(slide, fig, box, fig_dirs, cache_dir, fill_cell=False)
            if cap_box:
                add_text(slide, fig.caption, cap_box, L.CAPTION_PT, INK, "Caption", align=PP_ALIGN.CENTER)
    if boxes["bullets"]:
        max_pt = L.BULLET_SIDE_PT if spec.figures or spec.placeholder else L.BULLET_PT
        lines = list(spec.bullets) if spec.plain else [f"• {b}" for b in spec.bullets]
        pt = L.bullet_size(lines, boxes["bullets"], max_pt)
        if pt is None:      # too much text: build anyway at the minimum; qa reports the overflow
            pt = L.BULLET_MIN_PT
        add_text(slide, lines, boxes["bullets"], pt, INK, "Bullets", anchor=MSO_ANCHOR.MIDDLE)
    return [f.path for f, p in zip(spec.figures, paths) if p is None]


def build_deck(template, slides, fig_dirs, cache_dir=None, credits_in_notes=False, footer=None):
    """Created by JXP and Claude. Build the deck in memory.

    Inputs
    ------
    template : path to the Kraw master .pptx
    slides : list of spec.Slide; the first must be kind TITLE
    fig_dirs : directories searched for figure files
    cache_dir : where downsampled photo copies go (default: system temp)
    credits_in_notes : if True, a slide's `source` goes into the speaker
        notes only (no Source box is drawn on the slide)
    footer : if set, replaces the master's "UC SANTA CRUZ | Science" logo
        (and the word "Science" in the title slide's band) with this text

    Output
    ------
    (Presentation, report) where report is a list of (slide number, title, what).
    """
    cache_dir = Path(cache_dir) if cache_dir else Path(tempfile.gettempdir()) / "sms_slide_images"
    fig_dirs = [Path(d).expanduser() for d in fig_dirs]
    sources = load_sources(fig_dirs)
    prs = Presentation(str(template))
    kraw3 = prs.slides[2]
    title_el = copy.deepcopy(find_shape(kraw3, TITLE_BOX_TEXT)._element)
    subline_el = copy.deepcopy(find_shape(kraw3, SUBLINE_BOX_TEXT)._element)
    # python-pptx does not clone slide-number placeholders from the layout
    slidenum_el = copy.deepcopy(next(sh for sh in kraw3.placeholders
                                     if sh.placeholder_format.idx == SLIDE_NUMBER_IDX)._element)
    drop_slides(prs, keep={0})
    content_layout = layout_by_name(prs, CONTENT_LAYOUT)

    if not slides or slides[0].kind != TITLE:
        raise ValueError("the first slide of a plan must be kind TITLE")
    report = []
    first = prs.slides[0]
    fill_title_slide(first, slides[0])
    first.notes_slide.notes_text_frame.text = notes_text(slides[0], [], sources)
    if footer:
        set_footer(prs, footer)
    report.append((1, slides[0].title, "title slide"))

    for n, spec in enumerate(slides[1:], start=2):
        if spec.kind == TITLE:
            raise ValueError(f"slide {n}: only the first slide may be kind TITLE")
        slide = prs.slides.add_slide(content_layout)
        for ph in list(slide.placeholders):
            ph._element.getparent().remove(ph._element)
        num = copy.deepcopy(slidenum_el)
        num.find(f".//{P}cNvPr").set("id", str(next_shape_id(slide)))
        slide.shapes._spTree.append(num)

        if spec.title:
            pt, _ = L.title_size(spec.title)
            box = add_box(slide, title_el, spec.title, "Title", pt)
            if spec.kind == DIVIDER:
                box.top = Inches(DIVIDER_TOP)
        if spec.subtitle and spec.kind == CONTENT:
            sub = add_box(slide, subline_el, spec.subtitle, "Sub-line", L.subline_size(spec.subtitle))
            sub.top = Inches(L.SUBLINE_TOP)

        missing = []
        if spec.kind == CONTENT:
            missing = fill_content_slide(slide, spec, fig_dirs, cache_dir)
        elif spec.kind == IMAGE:
            fig = spec.figures[0]
            path = resolve(fig.path, fig_dirs)
            box = L.image_box(spec.title, aspect_of(path) if path else None)
            add_figure(slide, fig, box, fig_dirs, cache_dir, fill_cell=False)
            missing = [] if path else [fig.path]
        if spec.source and not credits_in_notes:
            add_source(slide, spec.source)
        slide.notes_slide.notes_text_frame.text = notes_text(spec, missing, sources)
        what = spec.kind + (f", MISSING {missing}" if missing else "")
        report.append((n, spec.title, what))
    return prs, report
