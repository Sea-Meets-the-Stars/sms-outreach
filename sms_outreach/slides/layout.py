"""Created by JXP and Claude.

Pure layout geometry for Kraw-style slides (no python-pptx, no template).

Slide: 10" x 5.625".  Measured from the Kraw_2024 master:
  - title text box  : x 0.17, y 0.02, w 9.75; Roboto Bold 38 pt, top-anchored
  - sub-line box    : x 0.17, y 4.48, w 9.75; Roboto 25 pt, top-anchored
  - UCSC logo       : x 0.10-1.76, y 5.24-5.56 (master)
  - slide number    : x 9.27-9.87, y 5.10-5.53 (master)
Our rules:
  - nothing we place within EDGE (0.4") of the side edges;
  - the content area runs from below the title to above the sub-line
    (or above the source line when there is no sub-line);
  - the source line is small grey text, right-aligned, between the logo and
    the slide number, at the very bottom.

All lengths are inches.  A box is (x, y, w, h).
"""
import math
from pathlib import Path

from PIL import ImageFont

SLIDE_W, SLIDE_H = 10.0, 5.625
EDGE = 0.25                 # side margin (images lead: B7)
X0, X1 = EDGE, SLIDE_W - EDGE

TITLE_PT = 38
TITLE_MIN_PT = 30
TITLE_TEXT_W = 9.3          # 9.75" box minus insets, minus a little slack
SUBLINE_TOP = 4.62           # Kraw puts its sub-line at 4.48; moved down to give images room (B7)
SUBLINE_PT = 25
CONTENT_GAP = 0.04

SRC_X, SRC_W = 1.95, 7.2    # right of the logo, left of the slide number
SRC_TOP, SRC_H = 5.30, 0.15  # in the logo row
SRC_MAX_PT, SRC_MIN_PT = 7, 5  # credits are deliberately tiny (B7)
BOTTOM_LIMIT = 5.45         # nothing we place may extend below this

CAPTION_H = 0.36            # pair captions (Roboto 16 pt)
CAPTION_PT = 16
BULLET_PT = 28              # bullets alone on a slide
BULLET_SIDE_PT = 18         # bullets beside a figure
PAIR_GAP = 0.15
FIG_BULLET_SPLIT = 0.66     # figure width fraction when a figure shares the slide with bullets

ROBOTO = Path(__file__).resolve().parent / "data" / "Roboto.ttf"
_FONTS = {}


def text_width(text, pt, weight="Regular"):
    """Created by JXP and Claude. Rendered width (inches) of one line of
    `text` in Roboto `weight` at `pt` points."""
    if weight not in _FONTS:
        font = ImageFont.truetype(str(ROBOTO), 400)
        font.set_variation_by_name(weight)
        _FONTS[weight] = font
    return _FONTS[weight].getlength(text) / 400 * pt / 72


def title_size(title):
    """Created by JXP and Claude. (points, n_lines) for a slide title: the
    largest size <= TITLE_PT that keeps it on one line, but not below
    TITLE_MIN_PT; titles that still do not fit wrap to two lines."""
    if not title:
        return TITLE_PT, 0
    w = text_width(title, TITLE_PT, "Bold")
    pt = min(TITLE_PT, math.floor(TITLE_PT * TITLE_TEXT_W / w))
    if pt >= TITLE_MIN_PT:
        return pt, 1
    return TITLE_MIN_PT, 2


def title_bottom(title):
    """Created by JXP and Claude. Bottom (inches) of a Kraw title: 0.02"
    offset + 0.1" top inset + lines x 1.2 x size + a small gap."""
    pt, lines = title_size(title)
    if lines == 0:
        return EDGE
    return 0.02 + 0.1 + lines * pt * 1.2 / 72 + 0.04


def source_size(source):
    """Created by JXP and Claude. Font size for the one-line source text:
    the largest of SRC_MAX_PT..SRC_MIN_PT that fits SRC_W (else the minimum,
    and the text wraps)."""
    for pt in range(SRC_MAX_PT, SRC_MIN_PT - 1, -1):
        if text_width(source, pt) <= SRC_W - 0.05:
            return pt
    return SRC_MIN_PT


SUBLINE_TEXT_W = 9.5       # 9.75" Kraw sub-line box minus insets
SUBLINE_MIN_PT = 18
BULLET_MIN_PT = 16
BULLET_LEADING = 1.25


def subline_size(subline):
    """Created by JXP and Claude. Font size for the one-line sub-line: the
    largest of SUBLINE_PT..SUBLINE_MIN_PT that keeps it on one line (a
    wrapped sub-line would run into the source line and logo)."""
    for pt in range(SUBLINE_PT, SUBLINE_MIN_PT - 1, -1):
        if text_width(subline, pt) <= SUBLINE_TEXT_W:
            return pt
    return SUBLINE_MIN_PT


def wrapped_lines(text, pt, width):
    """Created by JXP and Claude. Number of lines `text` takes when
    word-wrapped at `width` inches in Roboto at `pt`."""
    lines, cur = 1, ""
    for word in text.split():
        trial = f"{cur} {word}".strip()
        if cur and text_width(trial, pt) > width:
            lines, cur = lines + 1, word
        else:
            cur = trial
    return lines


def bullets_height(bullets, pt, width):
    """Created by JXP and Claude. Height (inches) of a bullet list."""
    n = sum(wrapped_lines(b, pt, width) for b in bullets)
    return n * pt * BULLET_LEADING / 72


def bullet_size(bullets, box, max_pt):
    """Created by JXP and Claude. The largest size <= max_pt (>= BULLET_MIN_PT)
    at which the bullets fit `box`; None if they do not fit even at the minimum."""
    _, _, w, h = box
    for pt in range(max_pt, BULLET_MIN_PT - 1, -1):
        if bullets_height(bullets, pt, w) <= h:
            return pt
    return None


def content_area(title, has_subtitle):
    """Created by JXP and Claude. (top, bottom) of the content area."""
    top = title_bottom(title)
    bottom = (SUBLINE_TOP if has_subtitle else SRC_TOP) - CONTENT_GAP
    return top, bottom


def fit(aspect, box_w, box_h):
    """Created by JXP and Claude. Largest (w, h) with width/height = aspect
    inside box_w x box_h."""
    w = min(box_w, box_h * aspect)
    return w, w / aspect


def centered(aspect, box):
    """Created by JXP and Claude. An image of `aspect`, fitted and centred in box."""
    x, y, w, h = box
    fw, fh = fit(aspect, w, h)
    return (x + (w - fw) / 2, y + (h - fh) / 2, fw, fh)


def content_boxes(title, has_subtitle, aspects, n_bullets=0, captions=()):
    """Created by JXP and Claude. Boxes for a CONTENT slide.

    Inputs
    ------
    title : str
    has_subtitle : bool
    aspects : list of width/height for 0-2 figures (None = placeholder box,
              which fills its whole cell)
    n_bullets : number of bullet lines (0 = none)
    captions : per-figure caption strings (pairs)

    Output
    ------
    dict with keys 'figures' (list of boxes), 'captions' (list of boxes or
    None), 'bullets' (box or None).
    """
    top, bottom = content_area(title, has_subtitle)
    out = {"figures": [], "captions": [], "bullets": None}
    n = len(aspects)
    if n == 0:
        if n_bullets:
            out["bullets"] = (X0 + 0.3, top, X1 - X0 - 0.6, bottom - top)
        return out
    if n == 1:
        cell_w = (X1 - X0) * (FIG_BULLET_SPLIT if n_bullets else 1.0)
        cells = [(X0, top, cell_w, bottom - top)]
        if n_bullets:
            bx = X0 + cell_w + PAIR_GAP
            out["bullets"] = (bx, top, X1 - bx, bottom - top)
    else:
        if n_bullets:       # a band of (one-line) bullets on top, the pair below
            band_h = n_bullets * BULLET_SIDE_PT * BULLET_LEADING / 72 + 0.1
            out["bullets"] = (X0 + 0.3, top, X1 - X0 - 0.6, band_h)
            top += band_h + 0.1
        cell_w = (X1 - X0 - PAIR_GAP) / 2
        cells = [(X0, top, cell_w, bottom - top), (X0 + cell_w + PAIR_GAP, top, cell_w, bottom - top)]
    any_caption = any(captions)
    for k, (aspect, cell) in enumerate(zip(aspects, cells)):
        x, y, w, h = cell
        if any_caption:     # reserve caption room, then sit the caption on top of the fitted figure
            y, h = y + CAPTION_H, h - CAPTION_H
        fig = (x, y, w, h) if aspect is None else centered(aspect, (x, y, w, h))
        out["figures"].append(fig)
        has_cap = any_caption and k < len(captions) and captions[k]
        out["captions"].append((x, fig[1] - CAPTION_H, w, CAPTION_H) if has_cap else None)
    return out


def image_box(title, aspect):
    """Created by JXP and Claude. Box for an IMAGE slide: as large as fits
    below the (optional) title and above the source line."""
    top = title_bottom(title) if title else 0.15
    return centered(aspect if aspect else 16 / 9, (X0, top, X1 - X0, SRC_TOP - 0.1 - top))


def inside(box, edge=EDGE, bottom=BOTTOM_LIMIT, tol=0.01):
    """Created by JXP and Claude. True if `box` respects the side margins and
    the bottom limit."""
    x, y, w, h = box
    return x >= edge - tol and x + w <= SLIDE_W - edge + tol and y >= -tol and y + h <= bottom + tol
