#!/usr/bin/env python3
"""Practice: marble / shale / slate applying the stone-study lessons, then an arcane (magic-infused)
stone that reuses those techniques. 16x16 tiling blocks. Deterministic.

Lessons applied (knowledge/lessons.md, 2026-07-21):
- S2 colour=chemistry: marble pale (calcite/felsic), shale/slate dark cool.
- S3 structure axis: marble=wandering veins, shale=horizontal bands (L1), slate=foliation.
- S1 grain=cluster/busyness: all fine-grained → low busyness, near-flat.
- C4/L2 hardness→edges: slate a touch sharper than soft shale.
- G1/O3 chromophore: arcane teal is the "vis" colour-code; O4 pale gangue halo; O2 vein hosting.
- S5 dressed/refined + emissive reserved for the runed/charged variant.
"""
import math
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
SESS = HERE.parent
OUT, SRC, PREV = SESS / "out", SESS / "src", SESS / "previews"
for d in (OUT, SRC, PREV):
    d.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SESS.parent.parent))
from aide import grid as G          # noqa: E402
from aide import blockrender as BR  # noqa: E402
from aide import render as RENDER   # noqa: E402

N = 16
T = (0, 0, 0, 0)
BG = (110, 110, 116, 255)
INK = (245, 245, 245, 255)


def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)


def h2(x, y, seed):
    h = (x * 73856093) ^ (y * 19349663) ^ (seed * 83492791)
    h &= 0xFFFFFFFF
    h ^= h >> 13
    return (h & 0xFFFFFFFF) % 100003 / 100003.0


def blank():
    im = Image.new("RGBA", (N, N), T)
    return im, im.load()


def speckle(px, ramp, seed, p_lo=0.14, p_hi=0.12):
    """Fine even speckle base (low busyness) — the fine-grained-rock read."""
    lo, mid, hi = ramp
    for y in range(N):
        for x in range(N):
            g = h2(x, y, seed)
            px[x, y] = lo if g < p_lo else (hi if g > 1 - p_hi else mid)


def vein(px, color, core, base_x, seed, amp=2.2, slope=1):
    """A wavy diagonal vein that tiles (period-8 sine, integer slope → wraps at y=16)."""
    for y in range(N):
        cx = (base_x + slope * y + amp * math.sin(y / 8 * 2 * math.pi))
        xi = int(round(cx)) % N
        px[xi, y] = core
        if h2(xi, y, seed) < 0.5:                       # broken 2px width
            px[(xi + 1) % N, y] = color


# ---------------------------------------------------------------- REAL stones (practice)
def marble():
    """Metamorphosed calcite: pale body + wandering grey veins (S2 pale, S3 veins, low busyness)."""
    im, px = blank()
    base = (hx(0xC6C4BA), hx(0xDCDAD1), hx(0xECEAE3))   # shadow / base / highlight — warm white
    speckle(px, base, 41, p_lo=0.10, p_hi=0.10)
    vein(px, hx(0xA8A69C), hx(0x8C8A80), 4, 42, amp=2.4, slope=1)
    vein(px, hx(0xB6B4AA), hx(0x9A988E), 11, 43, amp=1.6, slope=-1)
    return im


def shale():
    """Fine soft sedimentary: dark cool grey + thin HORIZONTAL laminae (L1), flat, low busyness."""
    im, px = blank()
    base = (hx(0x363A3E), hx(0x474B50), hx(0x565A5F))
    speckle(px, base, 51, p_lo=0.16, p_hi=0.10)
    for y in range(N):
        if y % 3 == 0:                                  # broken lamina line every 3px
            for x in range(N):
                if h2(x, y, 52) < 0.75:
                    px[x, y] = hx(0x2E3236)
        elif y % 3 == 1:
            for x in range(N):
                if h2(x, y, 53) < 0.28:
                    px[x, y] = hx(0x565A5F)
    return im


def slate():
    """Metamorphosed shale: cool blue-grey, subtle foliation grain + mica flecks; a touch sharper (C4)."""
    im, px = blank()
    base = (hx(0x363E48), hx(0x46505A), hx(0x58636F))
    for y in range(N):
        for x in range(N):
            g = 0.6 * h2(x // 2, y, 61) + 0.4 * h2(x, y, 62)   # horizontally-biased grain = foliation
            px[x, y] = base[0] if g < 0.20 else (base[2] if g > 0.82 else base[1])
    for (fx, fy) in [(3, 2), (11, 5), (6, 9), (13, 12), (2, 13)]:
        px[fx, fy] = hx(0x76828E)                       # mica sheen flecks
    for y in (5, 11):                                   # faint cleavage lines
        for x in range(N):
            if h2(x, y, 63) < 0.4:
                px[x, y] = hx(0x303842)
    return im


# ---------------------------------------------------------------- ARCANE (magic-infused)
AR = dict(dk=hx(0x3A424C), base=hx(0x4C5560), lt=hx(0x5E6874), hi=hx(0x6E7A86),
          teal=hx(0x7FE8D8), teal_dk=hx(0x3FA898), halo=hx(0x7C8894))


def arcane_base(px, seed):
    speckle(px, (AR["dk"], AR["base"], AR["lt"]), seed, p_lo=0.12, p_hi=0.10)


def arcane_veined():
    """Marble-vein technique + teal chromophore + pale gangue halo (O4) = infused vis veins."""
    im, px = blank()
    arcane_base(px, 71)
    for (bx, sd, amp, slp) in [(5, 72, 2.4, 1), (11, 73, 1.8, -1)]:
        for y in range(N):
            cx = int(round(bx + slp * y + amp * math.sin(y / 8 * 2 * math.pi))) % N
            px[(cx - 1) % N, y] = AR["halo"] if h2(cx, y, sd) < 0.6 else px[(cx - 1) % N, y]  # gangue halo
            px[cx, y] = AR["teal"] if h2(cx, y, sd) < 0.4 else AR["teal_dk"]                  # glowing vein
    return im


def arcane_geode():
    """Ore/geode technique: sparse teal crystal clusters (faceted hi+shadow) in dressed stone."""
    im, px = blank()
    arcane_base(px, 74)
    for (cx, cy) in [(4, 5), (11, 10)]:
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                x, y = (cx + dx) % N, (cy + dy) % N
                d = abs(dx) + abs(dy)
                px[x, y] = AR["teal"] if d == 0 else (AR["teal_dk"] if d == 2 else AR["halo"])
        px[cx, (cy - 1) % N] = hx(0xB8F4EA)             # bright light-return facet (G3)
    return im


def arcane_runed():
    """Dressed stone (S5) + a faint engraved rune with a teal glow — the charged/runed variant."""
    im, px = blank()
    arcane_base(px, 75)
    # a small angular sigil (engraved dark) glowing teal at its core
    strokes = [(7, 3), (7, 4), (7, 5), (7, 6), (7, 7), (5, 5), (6, 5), (8, 5), (9, 5),
               (6, 3), (8, 7), (10, 9), (10, 10), (10, 11), (9, 11), (11, 11)]
    for (x, y) in strokes:
        px[x, y] = AR["dk"]
        if h2(x, y, 76) < 0.5:
            px[x, y] = AR["teal_dk"]
    px[7, 5] = AR["teal"]
    px[10, 10] = AR["teal"]
    return im


# ---------------------------------------------------------------- present
def tile3(img):
    return RENDER.upscale(RENDER.tiled(img, 3, 3), 5)


def lbl(img, text, top=16):
    s = Image.new("RGBA", (max(img.width, 70), img.height + top), T)
    s.alpha_composite(img, (0, top))
    ImageDraw.Draw(s).text((0, 3), text, fill=INK)
    return s


def row(img, label):
    tiled = lbl(tile3(img), "tiled 3x3")
    block = lbl(BR.iso_block(img, img, img, scale=7), "block")
    h = max(tiled.height, block.height) + 18
    strip = Image.new("RGBA", (tiled.width + block.width + 20 + 8, h), T)
    ImageDraw.Draw(strip).text((0, 2), label, fill=INK)
    strip.alpha_composite(tiled, (0, 18 + (h - 18 - tiled.height)))
    strip.alpha_composite(block, (tiled.width + 20, 18 + (h - 18 - block.height)))
    return strip


def sheet(title, rows, out, pad=16, gap=18):
    w = max(r.width for r in rows) + 2 * pad
    ht = sum(r.height for r in rows) + gap * (len(rows) - 1) + 2 * pad + 24
    canvas = Image.new("RGBA", (w, ht), BG)
    ImageDraw.Draw(canvas).text((pad, 8), title, fill=INK)
    y = 30
    for r in rows:
        canvas.alpha_composite(r, (pad, y))
        y += r.height + gap
    canvas.save(out)
    print("wrote", out.name, canvas.size)


def main():
    reals = {"marble": marble(), "shale": shale(), "slate": slate()}
    arcs = {"arcane_veined": arcane_veined(), "arcane_geode": arcane_geode(), "arcane_runed": arcane_runed()}
    for name, img in {**reals, **arcs}.items():
        (SRC / f"{name}.pxg").write_text(G.to_text(G.from_image(img)))
        G.save_texture(img, OUT / f"{name}.png")
    sheet("REAL STONES (practice) — geology lessons applied", [
        row(reals["marble"], "marble - pale calcite + wandering grey veins (S2/S3)"),
        row(reals["shale"], "shale - dark cool + horizontal laminae, soft/flat (L1)"),
        row(reals["slate"], "slate - cool blue-grey foliation + mica flecks (S3/C4)"),
    ], PREV / "sheet-real-stones.png")
    sheet("ARCANE / MAGIC-INFUSED STONE — techniques reused", [
        row(arcs["arcane_veined"], "A veined - glowing teal vis veins + pale gangue halo (marble+O4)"),
        row(arcs["arcane_geode"], "B geode - sparse teal crystal clusters, faceted (ore/geode)"),
        row(arcs["arcane_runed"], "C runed - dressed stone + engraved sigil glowing teal (S5)"),
    ], PREV / "sheet-arcane-stone.png")
    print("done")


if __name__ == "__main__":
    main()
