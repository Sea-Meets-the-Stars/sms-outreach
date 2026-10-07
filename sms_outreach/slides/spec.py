"""Created by JXP and Claude.

Slide specification for a plan file.

A plan file (e.g. talks/wmko_2026/slides/plan.py) defines:
    TEMPLATE   : path to the Kraw master .pptx (read in place, never copied)
    FIG_DIRS   : list of directories searched, in order, for figure files
    OUTPUT     : path of the .pptx to write
    SLIDES     : list of Slide
and optionally MAX_SLIDES (main-deck limit checked by QA).

Kinds
-----
TITLE   : Kraw slide 1 (title + sea|sky hero image); `subtitle` is the
          sub-title line, `author` (if set) replaces the affiliation line.
CONTENT : title at top, optional one-line sub-line at the bottom, and the
          figures / bullets in between.
DIVIDER : a single title centred vertically (section break).
IMAGE   : one image filling the slide below an optional title (e.g. a slide
          rendered from another deck, or launch art).

Figures
-------
CONTENT slides take 0, 1 or 2 figures:
  0 : bullets only (or a placeholder box)
  1 : the figure fills the content area (bullets, if any, go to its right)
  2 : a pair, side by side; by convention sea on the LEFT, stars on the RIGHT.
A figure whose file is not found is drawn as a red PLACEHOLDER box labelled
with its `placeholder` text (or file name), so a deck always builds.
"""
from dataclasses import dataclass, field

TITLE = "title"
CONTENT = "content"
DIVIDER = "divider"
IMAGE = "image"
KINDS = (TITLE, CONTENT, DIVIDER, IMAGE)


@dataclass
class Fig:
    """Created by JXP and Claude. One image on a slide.

    path        : file name (searched in FIG_DIRS) or absolute path
    caption     : short label drawn above the image (used in pairs)
    placeholder : label for the red box if the file does not exist yet
    """
    path: str
    caption: str = ""
    placeholder: str = ""


@dataclass
class Slide:
    """Created by JXP and Claude. One slide of a plan."""
    title: str
    kind: str = CONTENT
    subtitle: str = ""
    figures: list = field(default_factory=list)
    bullets: list = field(default_factory=list)
    source: str = ""
    notes: str = ""
    section: str = ""
    placeholder: str = ""   # CONTENT slide with no figures: draw a red box with this label
    author: str = ""        # TITLE slide only: replaces the affiliation line
    backup: bool = False    # after the main deck; not counted against MAX_SLIDES
    plain: bool = False     # render `bullets` as plain paragraphs (quotes), no bullet marks

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"unknown slide kind {self.kind!r} for {self.title!r}")
        self.figures = [f if isinstance(f, Fig) else Fig(f) for f in self.figures]
        if len(self.figures) > 2:
            raise ValueError(f"{self.title!r}: at most 2 figures per slide")
        if self.kind == IMAGE and len(self.figures) != 1:
            raise ValueError(f"{self.title!r}: an IMAGE slide takes exactly one figure")
