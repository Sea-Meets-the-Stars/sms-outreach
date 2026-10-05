# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This repository holds the outreach materials and code for Sea Meets the Stars
(public talks, figures, and supporting analysis).

## Working Rules

- **Git**: The user will perform all git commands (commit, push, reset, etc.). Read-only git (`git status`, `git diff`, `git log`) is fine; do not run anything that changes repository state.
- **Calculations**: If you do any calculation, generate it as a Python script and write it to disk so that it can be added to the repository.
- **Python environment**: If you need to run Python, use the `ocean14` conda environment (e.g., `conda run -n ocean14 python script.py`).

## Layout

- `sms_outreach/` -- shared Python code (plotting, figure and slide helpers); tests in `sms_outreach/tests/`.
- `talks/<talk>/` -- one directory per talk, with `figures/`, `scripts/` (scripts that make the figures) and `slides/`.

## Slides

Talks are presented with Google Slides.  Generate slides as PowerPoint (`.pptx`, e.g. with `python-pptx`) in the talk's `slides/` directory; use LibreOffice (`soffice --headless --convert-to pdf ...`) to convert or render them for checking.  The user imports the `.pptx` into Google Slides.

## Prompt docs

Task instructions live in `claude_prompts/` (start with `start_up.md`). When pointed at a prompt doc, read it and execute only the numbered task requested, then record the work under that doc's `## Logs` section.
