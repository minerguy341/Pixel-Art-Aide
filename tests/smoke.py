"""End-to-end smoke test: author -> render -> analyze -> compare -> import.

Run from the repo root:  python3 tests/smoke.py
"""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from PIL import Image

from aide import analyze, compare, styles
from aide.grid import from_image, load_pxg, parse_pxg, to_image, to_text
from aide.render import preview_sheet

SAMPLE = """\
# a tiny 8x8 test tile: warm ramp block with one transparent corner
size: 8x8
[palette]
. = none
d = 5E4530   # shadow
b = 7A5B3C   # base
h = 8F6E4B   # highlight
[grid]
.bbbbbbb
bbhhbbdb
bhbbbbdb
bbbbdbbb
bdbbbbhb
bdbbhhbb
bbbdbbbb
bbbbbbbb
"""


def main() -> None:
    tmp = Path(tempfile.mkdtemp(prefix="aide-smoke-"))

    # parse + render
    pxg = parse_pxg(SAMPLE, source="sample")
    assert (pxg.width, pxg.height) == (8, 8)
    img = to_image(pxg)
    assert img.size == (8, 8) and img.getpixel((0, 0))[3] == 0
    assert img.getpixel((1, 0)) == (0x7A, 0x5B, 0x3C, 255)

    # round-trip: text -> image -> pxg -> text renders identically
    rt = to_image(from_image(img))
    assert rt.tobytes() == img.tobytes()
    reparsed = parse_pxg(to_text(pxg))
    assert to_image(reparsed).tobytes() == img.tobytes()

    # save + analyze
    png = tmp / "sample.png"
    img.save(png)
    m = analyze.analyze(img, expect_tiling=True)
    assert m["color_count"] == 3
    assert m["alpha"]["transparent"] == 1
    assert "tiling" in m and m["tiling"]["interior_contrast"] > 0
    text = analyze.report(m, expect_tiling=True)
    assert "palette" in text and "tiling" in text

    # ramp detection sees the warm wood ramp with its 3 steps
    assert any(r["steps"] == 3 for r in m["ramps"]), m["ramps"]

    # preview + contact sheet render and are non-trivially sized
    prev = tmp / "preview.png"
    preview_sheet(img, label="sample", tile=True).save(prev)
    assert Image.open(prev).width > 100

    sheet = tmp / "sheet.png"
    compare.contact_sheet([png, png], tile=True, labels=["a", "b"]).save(sheet)
    assert Image.open(sheet).width > 200

    # isometric block render: right size, transparent corners, opaque center
    from aide.blockrender import iso_block

    iso = iso_block(img, img, scale=4)
    assert iso.size == (64, 64)
    assert iso.getpixel((0, 0))[3] == 0
    assert iso.getpixel((32, 32))[3] == 255

    # model pipeline: parse a 2-box model -> auto-texture -> render (non-cube)
    from aide.model import parse_model
    from aide.autotex import autotexture, default_ramp
    from aide.modelrender import render_model

    slab_model = parse_model({
        "texture_size": [16, 16], "textures": {"all": "x:block/y"},
        "elements": [{"name": "s", "from": [0, 0, 0], "to": [16, 8, 16], "faces": {
            "up": {"uv": [0, 0, 16, 16], "texture": "#all"},
            "south": {"uv": [0, 0, 16, 8], "texture": "#all"},
            "east": {"uv": [0, 0, 16, 8], "texture": "#all"}}}]})
    assert len(slab_model.elements) == 1 and slab_model.texture_size == (16, 16)
    atex, _warns = autotexture(slab_model, default_ramp("7A5B3C"))
    assert atex.size == (16, 16)
    rendered = render_model(slab_model, {"__single__": atex}, scale=64)
    assert rendered.width > 20 and rendered.getpixel((rendered.width // 2, rendered.height // 2))[3] > 0
    # a cube_bottom_top parent synthesizes 6 faces
    cbt = parse_model({"parent": "minecraft:block/cube_bottom_top",
                       "textures": {"top": "x:t", "side": "x:s", "bottom": "x:b"}})
    assert len(cbt.elements[0].faces) == 6

    # style palette parsing
    card = "# X\n```palette wood\nshadow = 5E4530\nbase = 7A5B3C\n```\n"
    pal = styles.parse_style_palettes(card)
    assert pal == {"wood": [("shadow", (0x5E, 0x45, 0x30, 255)), ("base", (0x7A, 0x5B, 0x3C, 255))]}
    styles.swatch_sheet(pal).save(tmp / "swatch.png")

    # error paths
    for bad in ["size: 4x4\n[grid]\nabcd\n", SAMPLE.replace("size: 8x8", "size: 9x8")]:
        try:
            parse_pxg(bad)
        except ValueError:
            pass
        else:
            raise AssertionError(f"expected ValueError for {bad[:30]!r}")

    print(f"smoke OK (artifacts in {tmp})")


if __name__ == "__main__":
    main()
