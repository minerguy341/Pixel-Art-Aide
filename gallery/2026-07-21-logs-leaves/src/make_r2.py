#!/usr/bin/env python3
"""r2: more LOG (bark) candidates + CORE (end-grain) candidates for both woods, and more
SILVERWOOD LEAVES candidates shown with & without random rotation.

Greatwood leaves are DECIDED (C accent + rotation) so no new greatwood leaves here.
Self-contained (own palettes/helpers) so it's a standalone source of record. Deterministic.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math
import random
import sys

HERE = Path(__file__).resolve().parent
SESS = HERE.parent
OUT, SRC, PREV = SESS / "out", SESS / "src", SESS / "previews"
for d in (OUT, SRC, PREV):
    d.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(SESS.parent.parent))
from aide import grid as G  # noqa: E402
from aide import blockrender as BR  # noqa: E402

N = 16
T = (0, 0, 0, 0)
BG = (110, 110, 116, 255)
INK = (250, 250, 250, 255)


def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)


def h2(x, y, seed):
    h = (x * 73856093) ^ (y * 19349663) ^ (seed * 83492791)
    h &= 0xFFFFFFFF
    h ^= h >> 13
    return (h & 0xFFFFFFFF) % 100003 / 100003.0


GW = dict(k=hx(0x231712), f=hx(0x33251C), b=hx(0x47372A), r=hx(0x574230), h=hx(0x665038))
SW = dict(d=hx(0x878F86), s=hx(0x9EA69C), b=hx(0xC4C9BD), l=hx(0xD9DED9), h=hx(0xE9ECE2), t=hx(0x7FE8D8))
SL = dict(e=hx(0x6BA891), s=hx(0x8ABFA9), g=hx(0xA9D8C4), l=hx(0xC6E8D8), t=hx(0x7FE8D8), cf=hx(0xD8ECEC))


def blank():
    im = Image.new("RGBA", (N, N), T)
    return im, im.load()


# ============================================================ GREATWOOD BARK r2
def gw_fibrous():
    """Fine vertical fibres, no deep furrows — shaggy stringybark."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            base = GW["r"] if (x % 2) else GW["b"]
            if h2(x, y // 3, 41) < 0.30:            # broken fibre lines, 3px runs
                base = GW["f"]
            elif h2(x, y // 4, 42) < 0.12:
                base = GW["h"]
            px[x, y] = base
    return im


def gw_chunky():
    """Two wide deep furrows, rounded ridges with strong shoulder shading."""
    im, px = blank()
    furrows = {3, 11}
    for y in range(N):
        for x in range(N):
            df = min(min((x - c) % N, (c - x) % N) for c in furrows)
            if df == 0:
                c = GW["k"] if (y % 3) else GW["f"]
            elif df == 1:
                c = GW["f"]
            elif df == 2:
                c = GW["b"]
            elif df == 3:
                c = GW["r"]
            else:  # ridge crown
                c = GW["h"]
            if c in (GW["h"], GW["r"]) and h2(x, y // 3, 43) < 0.18:
                c = GW["b"]
            px[x, y] = c
    return im


def gw_cracked():
    """Blocky bark plates, brick-offset, craggy crack lines."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            band = y // 8
            xo = (x + (4 if band % 2 else 0)) % N
            plate_x = xo % 8
            plate_y = y % 8
            if plate_x == 0 or plate_y == 0:
                c = GW["k"] if ((x + y) % 2) else GW["f"]     # crack lines
            elif plate_x <= 2 and plate_y <= 2:
                c = GW["h"]                                    # plate lit corner (top-left)
            elif plate_x >= 6 or plate_y >= 6:
                c = GW["f"]                                    # plate shadow (bottom-right)
            else:
                c = GW["b"] if ((x + y) % 3) else GW["r"]
            px[x, y] = c
    return im


# ============================================================ SILVERWOOD BARK r2
def sw_runed():
    """Pale bark + faint vertical streaks + small etched arcane rune marks with teal glints."""
    im, px = blank()
    streaks = {4, 11}
    for y in range(N):
        for x in range(N):
            if x in streaks and (y % 4) != 1:
                c = SW["s"]
            elif h2(x, y // 3, 51) < 0.12:
                c = SW["b"]
            else:
                c = SW["l"]
            if (x + y) < 6:
                c = SW["h"]
            px[x, y] = c
    # two small vertical rune sigils (angular I-marks) + a teal glint each
    for (rx, ry) in ((6, 3), (10, 9)):
        for dy in range(4):
            px[rx, (ry + dy) % N] = SW["d"]
        px[(rx - 1) % N, ry] = SW["s"]
        px[(rx + 1) % N, (ry + 3) % N] = SW["s"]
        px[rx, (ry + 1) % N] = SW["t"]
    return im


def sw_polished():
    """Refined smooth silver: a soft central sheen band, minimal marks, rare teal."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            d = abs(x - 7.5)
            if d < 2:
                c = SW["h"]
            elif d < 4.5:
                c = SW["l"]
            elif d < 6.5:
                c = SW["b"]
            else:
                c = SW["s"]
            if h2(x, y // 4, 52) < 0.08:      # faint mottle so it isn't a flat gradient
                c = SW["b"] if c == SW["l"] else c
            px[x, y] = c
    for (x, y) in ((5, 4), (10, 11)):
        px[x, y] = SW["t"]
    return im


def sw_veined():
    """Vertical teal-tinged shimmer veins — most overtly magical bark."""
    im, px = blank()
    veins = {3, 8, 13}
    for y in range(N):
        for x in range(N):
            if x in veins:
                # broken vein: mostly cool streak, teal glints along it
                c = SW["t"] if (h2(x, y, 53) < 0.35) else SW["s"]
            elif h2(x, y // 3, 54) < 0.10:
                c = SW["b"]
            else:
                c = SW["l"]
            if (x + y) < 6 and c == SW["l"]:
                c = SW["h"]
            px[x, y] = c
    return im


# ============================================================ CORES (end grain)
def _rings(pal, ring_keys, pith, cx=7.5, cy=7.5, mod=3, rind=None):
    im, px = blank()
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - cx, y - cy)
            if r < 1.2:
                c = pith
            else:
                c = ring_keys[int(r) % len(ring_keys)]
            px[x, y] = c
    if rind:
        for i in range(N):
            for (x, y) in ((i, 0), (i, N - 1), (0, i), (N - 1, i)):
                px[x, y] = rind[0] if (i % 3) else rind[1]
    return im, px


def gw_core_rings():
    im, px = _rings(GW, [GW["f"], GW["b"], GW["r"]], GW["k"], rind=(GW["f"], GW["k"]))
    for y in range(N):                     # warm lit crown top-left
        for x in range(N):
            if (x + y) < 9 and px[x, y] == GW["r"]:
                px[x, y] = GW["h"]
    return im


def gw_core_star():
    """Dark heartwood + radial checking cracks (a cut-log split)."""
    im, px = _rings(GW, [GW["b"], GW["r"], GW["b"]], GW["k"], rind=(GW["f"], GW["k"]))
    cx = cy = 7.5
    for ang in range(0, 360, 60):
        a = math.radians(ang + 8)
        for t in range(0, 8):
            x = int(round(cx + math.cos(a) * t))
            y = int(round(cy + math.sin(a) * t))
            if 0 <= x < N and 0 <= y < N:
                px[x, y] = GW["k"] if t < 6 else GW["f"]
    for dy in range(-1, 2):                # solid dark heart
        for dx in range(-1, 2):
            px[7 + dx, 7 + dy] = GW["k"]
    return im


def gw_core_burl():
    """Eccentric off-centre swirling grain — an old burl end."""
    im, px = _rings(GW, [GW["f"], GW["b"], GW["r"], GW["b"]], GW["k"], cx=5.5, cy=6.5, rind=(GW["f"], GW["k"]))
    for y in range(N):                     # swirl nudge: shift some rings by a hashed twist
        for x in range(N):
            if px[x, y] == GW["b"] and h2(x, y, 61) < 0.16:
                px[x, y] = GW["r"]
            elif px[x, y] == GW["r"] and h2(x, y, 62) < 0.12:
                px[x, y] = GW["f"]
    return im


def sw_core_heart():
    im, px = _rings(SW, [SW["s"], SW["b"], SW["l"]], SW["t"], rind=(SW["s"], SW["d"]))
    for y in range(N):
        for x in range(N):
            if (x + y) < 9 and px[x, y] == SW["l"]:
                px[x, y] = SW["h"]
    return im


def sw_core_radiant():
    """Teal radiating out from the heart along the inner rings, fading pale outward."""
    im, px = _rings(SW, [SW["b"], SW["l"], SW["b"]], SW["t"], rind=(SW["s"], SW["d"]))
    cx = cy = 7.5
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - cx, y - cy)
            if r < 4 and int(r) % 2 == 1:            # inner ring lines glow teal
                px[x, y] = SW["t"]
            elif r < 2.2:
                px[x, y] = SW["t"]
    return im


def sw_core_runic():
    """A faint 6-point arcane star sigil at the heart, teal, over pale rings."""
    im, px = _rings(SW, [SW["s"], SW["b"], SW["l"]], SW["b"], rind=(SW["s"], SW["d"]))
    cx = cy = 7.5
    for ang in range(0, 360, 60):            # six radial spokes = a star sigil
        a = math.radians(ang)
        for t in range(0, 5):
            x = int(round(cx + math.cos(a) * t))
            y = int(round(cy + math.sin(a) * t))
            if 0 <= x < N and 0 <= y < N:
                px[x, y] = SW["t"] if t else SW["t"]
    px[7, 7] = px[8, 7] = px[7, 8] = px[8, 8] = SW["t"]
    return im


# ============================================================ SILVERWOOD LEAVES r2
def _leaf_field(pal, hole_frac, seed, clump_scale=2, lit_key="l",
                accent_key=None, accent_frac=0.0, accent_seed=0, blossom=0):
    im, px = blank()
    g, l, s, e = pal["g"], pal[lit_key], pal["s"], pal["e"]
    cs = clump_scale
    for y in range(N):
        for x in range(N):
            n = 0.6 * h2(x // cs, y // cs, seed) + 0.4 * h2(x, y, seed + 1)
            px[x, y] = l if n > 0.66 else (s if n < 0.34 else g)
    holes = set()

    def bad(x, y):
        for oy in (-1, 0):
            for ox in (-1, 0):
                q = [((x + ox + dx) % N, (y + oy + dy) % N) for dy in (0, 1) for dx in (0, 1)]
                if all((c in holes or c == (x, y)) for c in q):
                    return True
        return False

    for _, x, y in sorted((h2(x, y, seed + 7), x, y) for y in range(N) for x in range(N)):
        if len(holes) >= int(hole_frac * N * N):
            break
        if bad(x, y):
            continue
        holes.add((x, y))
        px[x, y] = T
    for y in range(N):
        for x in range(N):
            if px[x, y][3] and any(((x + dx) % N, (y + dy) % N) in holes for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                if px[x, y] != l or h2(x, y, seed + 3) < 0.5:
                    px[x, y] = e
    if accent_key and accent_frac:
        for y in range(N):
            for x in range(N):
                if px[x, y][3] and h2(x, y, accent_seed + 99) < accent_frac:
                    px[x, y] = pal[accent_key]
    if blossom:                                  # teal 2px glowing buds
        buds = [(3, 4), (11, 6), (6, 12), (13, 13), (8, 2)][:blossom]
        for (bx, by) in buds:
            for dx, dy in ((0, 0), (1, 0), (0, 1)):
                x, y = (bx + dx) % N, (by + dy) % N
                if px[x, y][3]:
                    px[x, y] = pal["t"]
    return im


def sw_leaf_clump():
    return _leaf_field(SL, 0.30, 71, clump_scale=3, accent_key="t", accent_frac=0.02, accent_seed=71)


def sw_leaf_blossom():
    return _leaf_field(SL, 0.30, 72, clump_scale=2, blossom=5)


def sw_leaf_frost():
    return _leaf_field(SL, 0.35, 73, clump_scale=2, lit_key="cf", accent_key="t", accent_frac=0.01, accent_seed=73)


# ============================================================ helpers: save + present
def save_both(img, name):
    (SRC / f"{name}.pxg").write_text(G.to_text(G.from_image(img)))
    G.save_texture(img, OUT / f"{name}.png")


def tile_grid(img, cols, rows, scale):
    w, h = img.size
    c = Image.new("RGBA", (w * cols, h * rows), T)
    for r in range(rows):
        for cc in range(cols):
            c.alpha_composite(img, (cc * w, r * h))
    return c.resize((c.width * scale, c.height * scale), Image.NEAREST)


def stack_iso(top, side, count, scale=8):
    n = top.width
    step = n * scale
    one = BR.iso_block(top, side, side, scale=scale)
    canvas = Image.new("RGBA", (one.width, one.height + step * (count - 1)), T)
    for i in range(count - 1, -1, -1):
        canvas.alpha_composite(one, (0, step * i))
    bb = canvas.getbbox()
    return canvas.crop(bb) if bb else canvas


ROTS = [Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]


def wall(tex, randomize, seed, side=6, scale=4):
    n = tex.width
    rng = random.Random(seed)
    c = Image.new("RGBA", (n * side, n * side), T)
    for by in range(side):
        for bx in range(side):
            t = tex
            if randomize:
                r = rng.randint(0, 3)
                if r:
                    t = tex.transpose(ROTS[r - 1])
            c.alpha_composite(t, (bx * n, by * n))
    return c.resize((c.width * scale, c.height * scale), Image.NEAREST)


def lbl(img, text, top=20):
    s = Image.new("RGBA", (img.width, img.height + top), T)
    s.alpha_composite(img, (0, top))
    ImageDraw.Draw(s).text((0, 4), text, fill=INK)
    return s


def two_col(a, b, label, gap=24):
    h = max(a.height, b.height)
    row = Image.new("RGBA", (a.width + b.width + gap, h + 18), T)
    ImageDraw.Draw(row).text((0, 2), label, fill=INK)
    row.alpha_composite(a, (0, 18))
    row.alpha_composite(b, (a.width + gap, 18))
    return row


def sheet(title, rows, out, pad=16, gap=22):
    w = max(r.width for r in rows) + 2 * pad
    h = sum(r.height for r in rows) + gap * (len(rows) - 1) + 2 * pad + 24
    canvas = Image.new("RGBA", (w, h), BG)
    ImageDraw.Draw(canvas).text((pad, 8), title, fill=INK)
    y = 28
    for r in rows:
        canvas.alpha_composite(r, (pad, y))
        y += r.height + gap
    canvas.save(out)
    print("wrote", out.name, canvas.size)


# ============================================================ build
def main():
    gw_bark = {"greatwood_log_fibrous": gw_fibrous(), "greatwood_log_chunky": gw_chunky(),
               "greatwood_log_cracked": gw_cracked()}
    sw_bark = {"silverwood_log_runed": sw_runed(), "silverwood_log_polished": sw_polished(),
               "silverwood_log_veined": sw_veined()}
    gw_cores = {"greatwood_core_rings": gw_core_rings(), "greatwood_core_star": gw_core_star(),
                "greatwood_core_burl": gw_core_burl()}
    sw_cores = {"silverwood_core_heart": sw_core_heart(), "silverwood_core_radiant": sw_core_radiant(),
                "silverwood_core_runic": sw_core_runic()}
    sw_leaves = {"silverwood_leaves_clump": sw_leaf_clump(), "silverwood_leaves_blossom": sw_leaf_blossom(),
                 "silverwood_leaves_frost": sw_leaf_frost()}
    allt = {**gw_bark, **sw_bark, **gw_cores, **sw_cores, **sw_leaves}
    for name, img in allt.items():
        save_both(img, name)

    gw_top = gw_cores["greatwood_core_rings"]
    sw_top = sw_cores["silverwood_core_heart"]
    gw_side = Image.open(OUT / "greatwood_log_straight.png").convert("RGBA")  # r1 pick as illustrative side
    sw_side = Image.open(OUT / "silverwood_log_smooth.png").convert("RGBA")

    # log r2 sheets: 2x3 tile | 3-tall trunk
    sheet("GREATWOOD LOG r2 - new bark candidates (2x3 tile | 3-tall trunk)", [
        two_col(lbl(tile_grid(gw_bark["greatwood_log_fibrous"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(gw_top, gw_bark["greatwood_log_fibrous"], 3), "3-tall trunk"), "D  fibrous - fine stringy fibres"),
        two_col(lbl(tile_grid(gw_bark["greatwood_log_chunky"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(gw_top, gw_bark["greatwood_log_chunky"], 3), "3-tall trunk"), "E  chunky - deep wide furrows, rounded ridges"),
        two_col(lbl(tile_grid(gw_bark["greatwood_log_cracked"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(gw_top, gw_bark["greatwood_log_cracked"], 3), "3-tall trunk"), "F  cracked - blocky brick-offset bark plates"),
    ], PREV / "sheet-greatwood-log-r2.png")

    sheet("SILVERWOOD LOG r2 - new bark candidates (2x3 tile | 3-tall trunk)", [
        two_col(lbl(tile_grid(sw_bark["silverwood_log_runed"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(sw_top, sw_bark["silverwood_log_runed"], 3), "3-tall trunk"), "D  runed - etched arcane sigils + teal glints"),
        two_col(lbl(tile_grid(sw_bark["silverwood_log_polished"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(sw_top, sw_bark["silverwood_log_polished"], 3), "3-tall trunk"), "E  polished - refined silver, soft central sheen"),
        two_col(lbl(tile_grid(sw_bark["silverwood_log_veined"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(sw_top, sw_bark["silverwood_log_veined"], 3), "3-tall trunk"), "F  veined - vertical teal shimmer veins"),
    ], PREV / "sheet-silverwood-log-r2.png")

    # core sheets: flat swatch | log-end block (top=core, sides=illustrative bark)
    def core_row(name, label, side):
        core = allt[name]
        return two_col(lbl(tile_grid(core, 1, 1, 12), "end grain (flat)"),
                       lbl(BR.iso_block(core, side, side, scale=10), "on a log end"), label)

    sheet("GREATWOOD CORES - end-grain candidates (side bark = illustrative)", [
        core_row("greatwood_core_rings", "1  rings - tight concentric growth rings", gw_side),
        core_row("greatwood_core_star", "2  star - dark heartwood + radial checking cracks", gw_side),
        core_row("greatwood_core_burl", "3  burl - eccentric off-centre swirling grain", gw_side),
    ], PREV / "sheet-greatwood-cores.png")

    sheet("SILVERWOOD CORES - end-grain candidates (side bark = illustrative)", [
        core_row("silverwood_core_heart", "1  heart - pale rings + small teal heart", sw_side),
        core_row("silverwood_core_radiant", "2  radiant - teal glow radiating along inner rings", sw_side),
        core_row("silverwood_core_runic", "3  runic - faint teal star sigil at the heart", sw_side),
    ], PREV / "sheet-silverwood-cores.png")

    # silverwood leaves r2: fixed | random-rotated
    def leaf_row(name, label, seed):
        tex = sw_leaves[name]
        return two_col(lbl(wall(tex, False, seed), "fixed"),
                       lbl(wall(tex, True, seed), "random-rotated"), label)

    sheet("SILVERWOOD LEAVES r2 - new candidates, fixed vs random-rotated (preview only)", [
        leaf_row("silverwood_leaves_clump", "D  clump - stronger lit/shadow depth, sparse teal", 301),
        leaf_row("silverwood_leaves_blossom", "E  blossom - teal shimmer in glowing 2px buds", 302),
        leaf_row("silverwood_leaves_frost", "F  frost - icy highlights, airier 35% holes", 303),
    ], PREV / "sheet-silverwood-leaves-r2.png")

    print("done:", len(allt), "textures")


if __name__ == "__main__":
    main()
