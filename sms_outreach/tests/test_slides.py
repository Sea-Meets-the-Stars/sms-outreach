"""Created by JXP and Claude. Tests for sms_outreach.slides."""
import json
from pathlib import Path

import pytest
from PIL import Image

from sms_outreach.slides import layout as L
from sms_outreach.slides import qa
from sms_outreach.slides.spec import CONTENT, IMAGE, TITLE, Fig, Slide

KRAW = Path("~/Projects/ClimateIntelligence/presentations/2026_WMKO/Kraw_2024.pptx").expanduser()
TITLES = ["Short", "Nothing more powerful than Fable in the wild",
          "WMKO + AI: reading the manual, building new optics, and much more besides"]
ASPECTS = [16 / 9, 1.0, 0.6, 3.0]


@pytest.mark.parametrize("title", TITLES)
@pytest.mark.parametrize("has_sub", [True, False])
def test_content_boxes_inside(title, has_sub):
    """Every layout (0/1/2 figures, with/without bullets and captions) stays inside the margins
    and above the sub-line / source line."""
    _, bottom = L.content_area(title, has_sub)
    cases = [([], 3, ()), ([None], 0, ()), ([1.5], 0, ()), ([1.5], 4, ())]
    cases += [([a, b], 0, ("sea", "stars")) for a in ASPECTS for b in ASPECTS]
    cases += [([a, None], 0, ()) for a in ASPECTS]
    cases += [([a, b], 3, ("laser", "iodine")) for a in ASPECTS for b in ASPECTS]
    for aspects, n_bul, caps in cases:
        boxes = L.content_boxes(title, has_sub, aspects, n_bul, caps)
        allb = boxes["figures"] + [c for c in boxes["captions"] if c] + ([boxes["bullets"]] if boxes["bullets"] else [])
        for box in allb:
            assert L.inside(box), (title, aspects, box)
            assert box[1] + box[3] <= bottom + 0.01
            assert box[1] >= L.title_bottom(title) - 0.01


def test_pair_is_side_by_side():
    """Two figures: the first (sea) is left of the second (stars), no overlap."""
    boxes = L.content_boxes("A pair", True, [1.0, 1.0])
    (x1, _, w1, _), (x2, _, _, _) = boxes["figures"]
    assert x1 + w1 <= x2


def test_title_size():
    pt, lines = L.title_size("Short")
    assert (pt, lines) == (L.TITLE_PT, 1)
    pt, lines = L.title_size(TITLES[-1])
    assert pt == L.TITLE_MIN_PT and lines == 2


def test_image_box_inside():
    for a in ASPECTS + [None]:
        assert L.inside(L.image_box("", a))
        assert L.inside(L.image_box("A title", a))


def test_spec_validation():
    with pytest.raises(ValueError):
        Slide("x", kind="bogus")
    with pytest.raises(ValueError):
        Slide("x", figures=["a", "b", "c"])
    with pytest.raises(ValueError):
        Slide("x", kind=IMAGE)
    assert isinstance(Slide("x", figures=["a.png"]).figures[0], Fig)


@pytest.mark.skipif(not KRAW.exists(), reason="Kraw master not available")
def test_build_counts_placeholders(tmp_path):
    """A deck with one real figure and two missing ones builds, passes QA,
    and reports exactly the missing figures as placeholders."""
    from sms_outreach.slides.deck import build_deck

    Image.new("RGB", (800, 450), "steelblue").save(tmp_path / "real.png")
    (tmp_path / "sources.json").write_text(json.dumps({"real.png": {"source": "Credit X"}}))
    slides = [
        Slide("Test deck", kind=TITLE, author="Somewhere"),
        Slide("A real figure", subtitle="with a sub-line", figures=["real.png"], source="Made up", notes="n"),
        Slide("A pair", figures=[Fig("real.png", caption="Sea"), Fig("missing.png", caption="Stars")], notes="n"),
        Slide("A box", placeholder="to come", notes="n"),
        Slide("Bullets", bullets=["one", "two"], notes="n"),
    ]
    prs, report = build_deck(KRAW, slides, [tmp_path], cache_dir=tmp_path / "cache")
    out = tmp_path / "t.pptx"
    prs.save(out)
    assert len(prs.slides) == len(slides)
    problems, warnings, ph = qa.check(out, max_slides=10)
    assert problems == []
    assert [(i, label) for i, _, label in ph] == [(3, "missing.png"), (4, "to come")]
    assert "MISSING" in report[2][2]
    # the pair has a real figure but no source line -> a warning, a failure only when strict
    assert any("without a source" in w for w in warnings)
    assert qa.check(out, max_slides=10, strict=True)[0]
    # sources.json credit reaches the speaker notes
    assert "Credit X" in prs.slides[1].notes_slide.notes_text_frame.text


def test_subline_and_bullets_fit():
    """Long sub-lines shrink to one line; long bullet lists shrink or are reported as overflowing."""
    long = "A deliberately long sub-line that would never fit on one line at twenty-five points"
    assert L.subline_size("Short and sweet") == L.SUBLINE_PT
    assert L.subline_size(long) < L.SUBLINE_PT
    box = (0.4, 1.0, 9.2, 3.4)
    assert L.bullet_size(["one", "two"], box, L.BULLET_PT) == L.BULLET_PT
    assert L.bullet_size([long * 3] * 12, box, L.BULLET_PT) is None


def test_slide_ready_modes(tmp_path):
    """CMYK and EXIF-rotated JPEGs are converted/rotated; PNG figures stay PNG."""
    from sms_outreach.slides.deck import aspect_of, slide_ready

    cmyk = tmp_path / "cmyk.jpg"
    Image.new("CMYK", (300, 200)).save(cmyk)
    out = slide_ready(cmyk, tmp_path / "cache")
    assert out != cmyk and Image.open(out).mode == "RGB"

    rot = tmp_path / "rot.jpg"
    im = Image.new("RGB", (300, 200))
    exif = im.getexif()
    exif[0x0112] = 6
    im.save(rot, exif=exif)
    assert aspect_of(rot) == pytest.approx(200 / 300)
    assert Image.open(slide_ready(rot, tmp_path / "cache")).size == (200, 300)

    big = tmp_path / "big.png"
    Image.new("RGB", (3000, 1500), "white").save(big)
    out = slide_ready(big, tmp_path / "cache")
    assert out.suffix == ".png" and max(Image.open(out).size) <= 2200
