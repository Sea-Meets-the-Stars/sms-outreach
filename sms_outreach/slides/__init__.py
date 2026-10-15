"""Created by JXP and Claude.

Kraw-style slide decks built with python-pptx.

Adapted from ClimateIntelligence/presentations/py (slide_style.py,
build_skeleton.py, assemble_deck.py, qa_deck.py), made repo-independent:
every path (template, figure directories, output) is passed in, and a talk is
described by one plan file (see `spec.Slide` and `build.load_plan`).

Modules
-------
spec    : Slide / Fig dataclasses and slide kinds
layout  : pure geometry (where each box goes), testable without a template
deck    : build a Presentation from a template + list of Slides
qa      : checks on a built deck (margins, fonts, notes, placeholders)
style   : matplotlib style for slide-sized figures
build   : command-line entry point (plan file -> .pptx [-> .pdf])

The bundled Roboto.ttf (data/) is the OFL-licensed Google font used by the
Kraw master; it is only used to measure text widths.
"""
