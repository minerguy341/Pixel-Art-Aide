#!/usr/bin/env python3
"""8 plank candidates for greatwood + silverwood, each shown tiled / full block / slab / stair.

One arrangement, many palettes: each plank layout is a palette-parameterised function, recoloured
per wood (greatwood dark ramp / silverwood pale ramp, from styles/thaumaturgy.md). Vanilla plank
grammar: horizontal boards, no full-height joints, grain in horizontal RUNS of close tones, broken
dark seam rows, staggered board-end joints. Plus two decorative arrangements (basketweave, diagonal).
Deterministic.
"""
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

N = 16
T = (0, 0, 0, 0)
BG = (110, 110, 116, 255)
INK = (250, 250, 250, 255)
SHADES = BR.SHADES


def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)


def h2(x, y, seed):
    h = (x * 73856093) ^ (y * 19349663) ^ (seed * 83492791)
    h &= 0xFFFFFFFF
    h ^= h >> 13
    return (h & 0xFFFFFFFF) % 100003 / 100003.0


# per-wood plank ramps (from the style card; greatwood is the dark exception)
GW = dict(dk=hx(0x2A1C16), sh=hx(0x3E2C1F), bs=hx(0x4F3B25), hi=hx(0x60492C))
SW = dict(dk=hx(0x9AA095), sh=hx(0xA8AC9D), bs=hx(0xCFD3C4), hi=hx(0xE4E7DA))


def blank():
    im = Image.new("RGBA", (N, N), T)
    return im


# ------------------------------------------------------------- horizontal-board planks
def hplanks(pal, bh, phases, grain_run=4, sh_p=0.26, hi_p=0.20, bevel=False, knots=False, seed=1):
    dk, sh, bs, hi = pal["dk"], pal["sh"], pal["bs"], pal["hi"]
    im = blank()
    px = im.load()
    nboards = N // bh
    for y in range(N):
        board = y // bh
        for x in range(N):
            r = x // grain_run
            g = h2(r, board, seed)
            px[x, y] = sh if g < sh_p else (hi if g > 1 - hi_p else bs)
    for board in range(nboards):
        y0 = board * bh
        for x in range(N):                                   # broken dark seam row (board top)
            px[x, y0] = dk if ((x + board) % 4) else sh
        if bevel:
            for x in range(N):
                px[x, (y0 + 1) % N] = hi                      # lit top edge
                px[x, (y0 + bh - 1) % N] = sh                 # shadow bottom edge
        p = phases[board % len(phases)]                       # staggered end joints (two 8-long planks)
        for jx in (p % N, (p + 8) % N):
            for ry in range(1, bh):
                px[jx, y0 + ry] = sh
                if bh >= 4:
                    px[jx, y0 + 1] = dk
    if knots:
        for (kx, ky) in ((5, 6), (11, 13)):
            for dyk in range(-1, 2):
                for dxk in range(-1, 2):
                    rad = max(abs(dxk), abs(dyk))
                    px[(kx + dxk) % N, (ky + dyk) % N] = dk if rad == 0 else sh
    return im


# ------------------------------------------------------------- decorative
def basketweave(pal, seed=7):
    dk, sh, bs, hi = pal["dk"], pal["sh"], pal["bs"], pal["hi"]
    im = blank()
    px = im.load()
    B = 8
    for y in range(N):
        for x in range(N):
            bx, by = x // B, y // B
            horiz = (bx + by) % 2 == 0
            ix, iy = x % B, y % B
            if ix == 0 or iy == 0:
                c = dk                                        # block border
            else:
                line = (iy if horiz else ix)
                c = hi if line % 3 == 1 else (sh if line % 3 == 2 else bs)
            px[x, y] = c
    return im


def diagonal(pal, seed=8):
    dk, sh, bs, hi = pal["dk"], pal["sh"], pal["bs"], pal["hi"]
    im = blank()
    px = im.load()
    for y in range(N):
        for x in range(N):
            s = (x + y) % N
            if s % 4 == 0:
                c = dk                                        # diagonal seam
            else:
                band = (s // 4) % 3
                c = hi if band == 0 else (sh if band == 2 else bs)
            px[x, y] = c
    return im


# ------------------------------------------------------------- the 8 arrangements (palette -> image)
def arrangements(pal):
    return {
        "classic": hplanks(pal, 4, [2, 6], seed=1),
        "wide": hplanks(pal, 8, [2, 10], grain_run=5, seed=2),
        "fine": hplanks(pal, 2, [2, 6, 10, 14], grain_run=3, seed=3),
        "runningbond": hplanks(pal, 4, [0, 4, 8, 12], seed=4),
        "beveled": hplanks(pal, 4, [2, 6], bevel=True, seed=5),
        "rustic": hplanks(pal, 4, [2, 6], grain_run=3, sh_p=0.34, hi_p=0.26, knots=True, seed=6),
        "basketweave": basketweave(pal),
        "diagonal": diagonal(pal),
    }


LABELS = {
    "classic": "1  classic - 4px boards, brick stagger",
    "wide": "2  wide - tall 8px boards",
    "fine": "3  fine - thin 2px boards",
    "runningbond": "4  running-bond - 4-phase staircase joints",
    "beveled": "5  beveled - lit/shadow board edges (framed)",
    "rustic": "6  rustic - heavy grain + knots",
    "basketweave": "7  basketweave - alternating-grain squares",
    "diagonal": "8  diagonal - 45deg decorative planks",
}


# ------------------------------------------------------------- renderers
def iso_slab(top, side, scale=8, height=0.5):
    n = top.width
    s = scale
    pt = top.convert("RGBA").load()
    ps = side.convert("RGBA").load()
    pad = int(0.15 * n * s)
    W = Hh = int(2 * n * s) + 2 * pad
    out = Image.new("RGBA", (W, Hh), T)
    d = ImageDraw.Draw(out, "RGBA")
    ox, oy = n * s + pad, n * s + pad

    def P(X, Y, Z):
        return (ox + (X - Z) * n * s, oy + (X + Z) * n * s * 0.5 - Y * n * s)

    def sh(c, f):
        return (int(c[0] * f), int(c[1] * f), int(c[2] * f), c[3])

    hc = int(round(height * n))
    # side x=1 (right, 0.6)
    for i in range(n):
        for j in range(hc):
            c = ps[i, n - 1 - j]
            if c[3] == 0:
                continue
            q = [P(1, (j + 1) / n, i / n), P(1, (j + 1) / n, (i + 1) / n),
                 P(1, j / n, (i + 1) / n), P(1, j / n, i / n)]
            d.polygon(q, fill=sh(c, SHADES[2]))
    # front z=1 (left, 0.8)
    for i in range(n):
        for j in range(hc):
            c = ps[i, n - 1 - j]
            if c[3] == 0:
                continue
            q = [P(i / n, (j + 1) / n, 1), P((i + 1) / n, (j + 1) / n, 1),
                 P((i + 1) / n, j / n, 1), P(i / n, j / n, 1)]
            d.polygon(q, fill=sh(c, SHADES[1]))
    # top y=height (1.0)
    for i in range(n):
        for j in range(n):
            c = pt[i, j]
            if c[3] == 0:
                continue
            q = [P(i / n, height, j / n), P((i + 1) / n, height, j / n),
                 P((i + 1) / n, height, (j + 1) / n), P(i / n, height, (j + 1) / n)]
            d.polygon(q, fill=sh(c, SHADES[0]))
    return out


def tile3(img, scale=5):
    w, h = img.size
    c = Image.new("RGBA", (w * 3, h * 3), T)
    for r in range(3):
        for cc in range(3):
            c.alpha_composite(img, (cc * w, r * h))
    return c.resize((c.width * scale, c.height * scale), Image.NEAREST)


def lbl(img, text, top=16):
    s = Image.new("RGBA", (max(img.width, 60), img.height + top), T)
    s.alpha_composite(img, (0, top))
    ImageDraw.Draw(s).text((0, 3), text, fill=INK)
    return s


def row(img, label, sc=6):
    tiled = lbl(tile3(img, 4), "tiled 3x3")
    block = lbl(BR.iso_block(img, img, img, scale=sc), "block")
    slab = lbl(iso_slab(img, img, scale=sc), "slab")
    stair = lbl(BR.iso_stair(img, img, scale=sc), "stair")
    views = [tiled, block, slab, stair]
    gap = 16
    h = max(v.height for v in views) + 18
    w = sum(v.width for v in views) + gap * (len(views) - 1)
    strip = Image.new("RGBA", (w, h), T)
    ImageDraw.Draw(strip).text((0, 2), label, fill=INK)
    x = 0
    for v in views:
        strip.alpha_composite(v, (x, 18 + (h - 18 - v.height)))
        x += v.width + gap
    return strip


def sheet(title, rows, out, pad=16, gap=18):
    w = max(r.width for r in rows) + 2 * pad
    h = sum(r.height for r in rows) + gap * (len(rows) - 1) + 2 * pad + 24
    canvas = Image.new("RGBA", (w, h), BG)
    ImageDraw.Draw(canvas).text((pad, 8), title, fill=INK)
    y = 30
    for r in rows:
        canvas.alpha_composite(r, (pad, y))
        y += r.height + gap
    canvas.save(out)
    print("wrote", out.name, canvas.size)


def main():
    for wood, pal in (("greatwood", GW), ("silverwood", SW)):
        arr = arrangements(pal)
        for key, img in arr.items():
            name = f"{wood}_planks_{key}"
            (SRC / f"{name}.pxg").write_text(G.to_text(G.from_image(img)))
            G.save_texture(img, OUT / f"{name}.png")
        rows = [row(arr[k], LABELS[k]) for k in LABELS]
        sheet(f"{wood.upper()} PLANKS - 8 candidates (tiled | block | slab | stair)",
              rows, PREV / f"sheet-{wood}-planks.png")


if __name__ == "__main__":
    main()
