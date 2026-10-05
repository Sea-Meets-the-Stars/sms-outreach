# Getting started 

## Goals

This repository will hold the outreach materials and code for Sea Meets the Stars.

## Prompts

1. Read this file.  Execute the 1st task under "Claude/CLAUDE.md file"
2. Read this file.  Execute the 1st task under "Claude/Skills"
3. Read this file.  Execute the 1st task under "Claude/Settings"
4. Read this file.  Execute the 1st task under "Basic start up"


## Claude

### CLAUDE.md file

1. Please generate a basic CLAUDE.md file for this project.  Have it indicate:

- I will perform git commands
- Add to the CLAUDE.md file:  If you do any calculation, generate it as a python script and write it to disk so that I can add it to the Repository.
- Add to the CLAUDE.md file:  If you need to run Python, use the "ocean14" conda environment.

### Skills

1. Copy over the skills/ files from the `IOPtics` repository (/Users/xavier/Oceanography/python/IOPtics/.claude/skills).

### Settings

1. Copy over the settings.json file from the `IOPtics` repository (/Users/xavier/Oceanography/python/IOPtics/.claude/settings.json).  Copy the policy, not the accumulated path-specific allow entries.

## Basic start up

1. Generate the basic files that one needs for a Python GitHub repository, e.g. a file for dependencies.  Examine the other Repositories in Oceanography/python to see how I tend to organize things.  Also, make a suggestion of which of their settings.json files to copy into this one.

## Q&A

1. **Is a Python package the right shape for this repo?**  I followed the house layout (`sms_outreach/` package, `setup.py`, `requirements.txt`, `pytest.ini`), but `claude_prompts/wmko_2026.md` suggests the main products are talks.  Would you like a talk-oriented layout on top of it, e.g. `talks/wmko_2026/{figures,scripts,slides}/`, with the package holding only shared plotting/figure code?
   - A: Yes, a Python repo is fine.  We will write plenty of code
2. **What format will the slides be in?**  (Keynote, PowerPoint, Google Slides, LaTeX/Beamer, reveal.js, ...)  This decides whether we need extra dependencies or build tooling.
   - A: I will present with Google Slides, but you will likely generate Powerpoint with LibreOffice.
3. **Which domain packages should be dependencies?**  I kept only the core scientific stack.  Candidates: `astropy` (astronomy figures), `xarray`/`h5netcdf` (ocean data), `cartopy` (maps).
   - A: Core is fine for now
4. **WebFetch allowlist.**  The IOPtics domains (Optica, Wiley, doi.org, Taylor & Francis) are aimed at checking the ocean-optics literature.  For outreach it may be more useful to allow image/press sites (e.g. NASA, ESA, NOAA, Wikimedia Commons).  Add them?
   - A: Yes, add NASA, ESA, NOAA, Wikimedia Commons.
5. **Outreach siblings.**  `~/Projects` has other non-research repos (e.g. `why-science-isnt-hard`, `star-island`).  Should future setup tasks follow those rather than `Oceanography/python`?
   - A: No
6. **Goals line.**  "This repository will hold the outreach materials and code for Sea Meets the Stars" was inferred from the README.  Please correct it if needed.
   - A: That's fine

## Logging

The "Logs" section will record Claude's work.  Please use the following format:

### <Date> (Short summary of the work)

<Detailed description of the work and what you learned>

...

## Logs

### 2026-10-05 (Executed start-up prompts #1-#4)

**#1 CLAUDE.md file.**  Generated `CLAUDE.md`, modeled on `victor-class/CLAUDE.md`.  It says the user performs all git commands (read-only git allowed), that calculations become Python scripts written to disk, and that Python runs in the `ocean14` conda environment.  I also added a short note telling Claude to take its instructions from `claude_prompts/` and log work under `## Logs`.

**#2 Skills.**  Copied `.claude/skills/` from IOPtics, giving the `critical-partner` and `grill-me` skills.

**#3 Settings.**  Copied `.claude/settings.json` from IOPtics, keeping the policy and dropping what had piled up: 37 of its 65 `allow` entries are kept.  The 28 dropped entries were one-off Crossref lookups and commands tied to IOPtics paths and scratchpads.  `deny` (sudo, `rm -rf /` and `~`, git push/commit/reset/rebase) and `ask` (`rm`) are unchanged.  I added `.claude/settings.local.json` to `.gitignore` so machine-local permissions are not committed.

**#4 Basic start up.**  Added `setup.py`, `requirements.txt`, `pytest.ini`, `sms_outreach/__init__.py` and `sms_outreach/tests/__init__.py`, following the victor-class / cugn-climatology pattern (setuptools `setup_keywords`, `requirements.txt` kept in sync with `install_requires`, `python_requires >= 3.12`, BSD).  I left out `pyproject.toml`, as in the sibling repos.  Checked: `import sms_outreach` works in `ocean14` (Python 3.14.6) and `pytest` finds the test directory (no tests yet).

*settings.json suggestion.*  All five siblings with a `settings.json` (OETHER, victor-class, PAB, retrieve-or-bust, cugn-climatology) have the same `deny`/`ask` policy; they differ only in their `allow` lists.  I recommend the trimmed IOPtics copy now in place.  victor-class has the same publisher domains.  retrieve-or-bust adds GitHub and Crossref `WebFetch`, which would be the one to borrow from if you want those.  See Q&A #4 about adding outreach-oriented domains instead.

*What I learned.*  The repo's remote is `Sea-Meets-the-Stars/sms-outreach`, the same GitHub org as OETHER and cugn-climatology.  Unlike its siblings it lives in `~/Projects`, not `~/Oceanography/python`.  A second prompt doc, `claude_prompts/wmko_2026.md` (a 45-minute WMKO 2026 public talk), was in progress, so this repo is mainly about talks; open questions about layout are in the Q&A section.  No git commands were run.

### 2026-10-05 (Acted on Q&A answers)

- **Q1 (layout):** Kept the Python package and added the talk layout `talks/wmko_2026/{figures,scripts,slides}/`.  Each folder has a `.gitkeep` so git tracks it while empty.  The layout is described in `CLAUDE.md`.
- **Q2 (slides):** Added `python-pptx` to `requirements.txt` and `setup.py`.  It is slide tooling, not a domain package, so it doesn't go against the Q3 answer.  I allowed `Bash(soffice:*)` in `.claude/settings.json` and added a "Slides" section to `CLAUDE.md`: generate `.pptx` into `talks/<talk>/slides/`, render or check it with LibreOffice, and the user imports it into Google Slides.  Checked: `python-pptx` 1.0.2 is already in `ocean14`, and `soffice` (`/opt/homebrew/bin/soffice`) converted a test `.pptx` to PDF.
- **Q3 (dependencies):** No change; core stack only.
- **Q4 (WebFetch):** Added NASA (www, science, images, images-api, svs.gsfc, earthobservatory, apod), ESA (www.esa.int, esahubble.org, esawebb.org), NOAA (www, oceanservice, oceanexplorer) and Wikimedia Commons (commons, upload).  I listed hosts one by one rather than using wildcards; add more as other subdomains come up.
- **Q5, Q6:** No change.  Future setup follows `Oceanography/python`, and the Goals line stays as it is.

No git commands were run.
