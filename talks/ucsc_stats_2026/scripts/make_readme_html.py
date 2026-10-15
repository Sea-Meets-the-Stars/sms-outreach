"""Created by JXP and Claude.

Convert talks/ucsc_stats_2026/README.md into a self-contained HTML file
for upload to Google Drive (Drive converts it into a Google Doc).

Handles only the Markdown this README uses: headings, paragraphs,
**bold**, *italic*, `- ` bullets, 4-space-indented display equations and
one two-column table of figures with captions.  Figures are downscaled
to JPEG and embedded as data URIs so the HTML needs no hosting.

    conda run -n ocean14 python talks/ucsc_stats_2026/scripts/make_readme_html.py OUT.html [--placeholders]

With --placeholders each figure is replaced by a short highlighted line
naming the PNG to insert by hand.  This keeps the HTML small enough to
pass through the Drive connector, which takes the file inline.
"""
import base64
import html
import io
import re
import sys
from pathlib import Path

from PIL import Image

TALK = Path(__file__).resolve().parents[1]
FIG_WIDTH_PX = 1000          # ~300 dpi at half the page width
FIG_WIDTH_PT = 230           # displayed width in the Doc
PLACEHOLDERS = "--placeholders" in sys.argv


def img_tag(rel):
    """Created by JXP and Claude. Embed one figure as a JPEG data URI."""
    if PLACEHOLDERS:
        return ('<span style="background-color:#fff2cc"><b>[Insert figure: '
                f'talks/ucsc_stats_2026/{rel}]</b></span>')
    im = Image.open(TALK / rel).convert("RGB")
    h = round(im.height * FIG_WIDTH_PX / im.width)
    im = im.resize((FIG_WIDTH_PX, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=90)
    b64 = base64.b64encode(buf.getvalue()).decode()
    hpt = round(FIG_WIDTH_PT * h / FIG_WIDTH_PX)
    return (f'<img src="data:image/jpeg;base64,{b64}" '
            f'width="{FIG_WIDTH_PT}" height="{hpt}">')


def inline(text):
    """Created by JXP and Claude. Escape, then apply bold/italic/links."""
    t = html.escape(text, quote=False)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<i>\1</i>", t)
    t = re.sub(r"(github\.com/[\w./-]+\w)", r'<a href="https://\1">\1</a>', t)
    t = re.sub(r"doi:(10\.[\w./-]+\w)", r'<a href="https://doi.org/\1">doi:\1</a>', t)
    t = re.sub(r"arXiv:(\d{4}\.\d{4,5})",
               r'<a href="https://arxiv.org/abs/\1">arXiv:\1</a>', t)
    return t


def convert(md):
    """Created by JXP and Claude. Markdown (this README's subset) -> HTML."""
    out, para, bullets = [], [], []
    lines = md.splitlines()

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()
        if bullets:
            out.append("<ul>" + "".join(f"<li>{inline(b)}</li>"
                                        for b in bullets) + "</ul>")
            bullets.clear()

    i = 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|"):                       # figure table
            flush()
            rows = []
            while i < len(lines) and lines[i].startswith("|"):
                cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
                if not all(re.fullmatch(r":?-+:?", c) for c in cells):
                    rows.append(cells)
                i += 1
            out.append('<table style="border-collapse:collapse">')
            for cells in rows:
                tds = []
                for c in cells:
                    m = re.fullmatch(r"!\[\]\((.+?)\)", c)
                    content = img_tag(m.group(1)) if m else inline(c)
                    tds.append('<td style="vertical-align:top;padding:4pt;'
                               f'font-size:9pt">{content}</td>')
                out.append("<tr>" + "".join(tds) + "</tr>")
            out.append("</table>")
            continue
        m = re.match(r"(#{1,3}) (.*)", ln)
        if m:
            flush()
            level = len(m.group(1))
            out.append(f"<h{level}>{inline(m.group(2))}</h{level}>")
        elif ln.startswith("    ") and ln.strip():   # display equation
            flush()
            out.append('<p style="margin-left:24pt;font-family:\'Cambria Math\','
                       f'Cambria,serif">{inline(ln.strip())}</p>')
        elif ln.startswith("- "):
            if para:
                flush()
            bullets.append(ln[2:])
        elif not ln.strip():
            flush()
        else:
            para.append(ln.strip())
        i += 1
    flush()
    return out


def main():
    out_path = Path(sys.argv[1])
    md = (TALK / "README.md").read_text()
    body = "\n".join(convert(md))
    doc = ('<!DOCTYPE html><html><head><meta charset="utf-8">'
           "<style>body{font-family:Arial,sans-serif;font-size:11pt}</style>"
           f"</head><body>\n{body}\n</body></html>\n")
    out_path.write_text(doc)
    print(f"wrote {out_path} ({len(doc) / 1024:.0f} KB)")


if __name__ == "__main__":
    main()
