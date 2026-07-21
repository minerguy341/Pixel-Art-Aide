#!/usr/bin/env python3
"""r3: bark + end-grain (cores) redone for both woods, applying the wood study.

Fixes:
- BARK EDGES FLOW: a furrow/groove STRADDLES the x=0/15 wrap and edge columns carry the same
  variation as the interior, so adjacent (parallel) logs merge instead of reading as framed panels.
- GREATWOOD: deep IRREGULAR wandering furrows + rounded ridges (ancient hardwood), sparse
  irregular checks — no brick grid.
- SILVERWOOD: young-birch PRISTINE & SERENE — smooth, pale, luminous, minimal marks; teal a faint
  whisper only (r2 veined 7% / radiant 14% were too loud).
- CORES redone: soft rings; greatwood warm/eccentric, silverwood serene pale + gentle luminous heart.

Leaves are DECIDED (greatwood r1 accent + rot, silverwood r2 frost + rot) — none here. Deterministic.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import math
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
# silverwood serene ramp: pale, luminous, gentle. sof = soft groove (only one step under base).
SW = dict(d=hx(0x9BA39A), s=hx(0xB4BBB0), sof=hx(0xC7CCC0), b=hx(0xD2D7CD), l=hx(0xE1E5DC), h=hx(0xF0F2EB), t=hx(0x7FE8D8))


def blank():
    im = Image.new("RGBA", (N, N), T)
    return im, im.load()


def circ(a, b):
    d = abs(a - b) % N
    return min(d, N - d)


# ============================================================ GREATWOOD BARK r3
def _gw_furrow_map():
    """Return df(x, y): circular distance to the nearest WANDERING furrow. One furrow straddles
    x=0 (so the wrap seam sits in a furrow → parallel logs merge). Wander tiles every 16 rows."""
    centers = [0, 5, 10, 13]                     # irregular spacing; 0 straddles the seam

    def eff(c, band):
        w = h2(c, band, 77)
        off = -1 if w < 0.34 else (1 if w > 0.66 else 0)
        return (c + off) % N

    def df(x, y):
        band = (y // 8) % 2                      # gentle wander in 8-row bands (repeats every 16 → tiles)
        return min(circ(x, eff(c, band)) for c in centers)
    return df


def gw_bark(variant):
    im, px = blank()
    df = _gw_furrow_map()
    for y in range(N):
        for x in range(N):
            d = df(x, y)
            if d == 0:
                c = GW["k"] if h2(x, y // 3, 88) < 0.35 else GW["f"]  # deep groove, crevices in 3px runs
            elif d == 1:
                c = GW["f"]
            elif d == 2:
                c = GW["b"]
            elif d == 3:
                c = GW["r"]
            else:
                c = GW["h"]
            if c in (GW["h"], GW["r"]) and h2(x, y // 3, 81) < 0.12:
                c = GW["b"]                              # lightly break flat ridge crowns
            px[x, y] = c

    if variant == "shaggy":
        for y in range(N):                              # fine vertical fibres on the ridges
            for x in range(N):
                if px[x, y] in (GW["h"], GW["r"], GW["b"]) and h2(x, y // 2, 82) < 0.24:
                    px[x, y] = GW["f"] if px[x, y] != GW["h"] else GW["b"]
    elif variant == "aged":
        for y in range(N):                              # sparse IRREGULAR horizontal checks
            for x in range(N):
                if df(x, y) >= 3 and h2(x, y, 83) < 0.05:
                    for dx in range(h2(x, y, 84) < 0.5 and 2 or 3):
                        xx = (x + dx) % N
                        if df(xx, y) >= 2:
                            px[xx, y] = GW["f"] if dx else GW["k"]
    return im


# ============================================================ SILVERWOOD BARK r3 (pristine/serene)
def sw_serene():
    """Smooth pale birch: a soft one-step groove straddling the seam + a gentle sheen band; whisper teal."""
    im, px = blank()
    grooves = {0, 9}                                    # 0 straddles the seam
    for y in range(N):
        for x in range(N):
            dg = min(circ(x, g) for g in grooves)
            if dg == 0:
                c = SW["b"]                              # soft groove — ONE step under base, no dark band
            elif dg == 1:
                c = SW["sof"]
            else:
                c = SW["l"]
            if 5 <= x <= 6:                              # gentle vertical sheen
                c = SW["h"]
            if c == SW["l"] and h2(x, y // 4, 91) < 0.05:
                c = SW["sof"]                            # faintest mottle so it isn't dead-flat
            px[x, y] = c
    px[12, 4] = SW["t"]                                 # two whisper teal specks
    px[3, 12] = SW["t"]
    return im


def sw_birch():
    """Smooth pale + subtle HORIZONTAL lenticels (young birch). Uniform vertically → merges perfectly."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            c = SW["l"]
            if 6 <= x <= 7:
                c = SW["h"]                              # soft central sheen
            if h2(x, y // 4, 92) < 0.05:
                c = SW["sof"]
            px[x, y] = c
    for (lx, ly, w) in ((1, 2, 3), (9, 5, 4), (4, 8, 3), (12, 11, 3), (6, 14, 4)):
        for dx in range(w):
            px[(lx + dx) % N, ly] = SW["d"] if dx == 1 else SW["s"]
    px[10, 8] = SW["t"]
    return im


def sw_moonlit():
    """Ethereal: a soft luminous cylindrical sheen (bright centre, gentle cool edges); faint teal.
    Edges are the SAME soft tone both sides → adjacent logs meet in a gentle channel, not a bright band."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            d = circ(x, 7)                              # 0 at centre col, up to 8 at seam
            if d <= 1:
                c = SW["h"]
            elif d <= 3:
                c = SW["l"]
            elif d <= 5:
                c = SW["b"]
            else:
                c = SW["sof"]
            if h2(x, y // 4, 93) < 0.05:
                c = SW["sof"] if c == SW["l"] else c
            px[x, y] = c
    for (tx, ty) in ((7, 3), (6, 10), (8, 13)):
        px[tx, ty] = SW["t"]
    return im


# ============================================================ CORES r3
def _rings(ring_keys, pith, cx=7.5, cy=7.5, rind=None):
    im, px = blank()
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - cx, y - cy)
            px[x, y] = pith if r < 1.2 else ring_keys[int(r) % len(ring_keys)]
    if rind:
        for i in range(N):
            for (x, y) in ((i, 0), (i, N - 1), (0, i), (N - 1, i)):
                px[x, y] = rind[0] if (i % 3) else rind[1]
    return im, px


def gw_core_rings():
    im, px = _rings([GW["f"], GW["b"], GW["r"]], GW["k"], rind=(GW["f"], GW["k"]))
    for y in range(N):
        for x in range(N):
            if (x + y) < 9 and px[x, y] == GW["r"]:
                px[x, y] = GW["h"]
    return im


def gw_core_heart():
    """Warm heartwood: darker core fading to lighter sapwood outward (radial value gradient)."""
    im, px = blank()
    cx = cy = 7.5
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - cx, y - cy)
            if r < 1.4:
                c = GW["k"]
            elif r < 4:
                c = GW["f"] if int(r) % 2 else GW["b"]
            elif r < 6.5:
                c = GW["b"] if int(r) % 2 else GW["r"]
            else:
                c = GW["r"] if int(r) % 2 else GW["h"]
            px[x, y] = c
    for i in range(N):
        for (x, y) in ((i, 0), (i, N - 1), (0, i), (N - 1, i)):
            px[x, y] = GW["f"] if (i % 3) else GW["k"]
    return im


def gw_core_burl():
    im, px = _rings([GW["f"], GW["b"], GW["r"], GW["b"]], GW["k"], cx=6.0, cy=6.5, rind=(GW["f"], GW["k"]))
    for y in range(N):
        for x in range(N):
            if px[x, y] == GW["b"] and h2(x, y, 61) < 0.15:
                px[x, y] = GW["r"]
    return im


def sw_core_heart():
    """Serene: soft pale rings, a gentle luminous heart, a single whisper of teal at the pith."""
    im, px = _rings([SW["s"], SW["b"], SW["l"]], SW["l"], rind=(SW["s"], SW["d"]))
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - 7.5, y - 7.5)
            if r < 1.4:
                px[x, y] = SW["h"]
            elif (x + y) < 9 and px[x, y] == SW["l"]:
                px[x, y] = SW["h"]
    px[7, 7] = SW["t"]                                   # a single teal whisper
    return im


def sw_core_halo():
    """Serene + one soft teal halo ring midway — the quiet magic tell."""
    im, px = _rings([SW["s"], SW["b"], SW["l"]], SW["h"], rind=(SW["s"], SW["d"]))
    cx = cy = 7.5
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - cx, y - cy)
            if 3.4 < r < 4.4:
                px[x, y] = SW["t"]
    return im


def sw_core_pale():
    """Ultra-clean: soft pale rings, NO teal — the fully-serene, non-magical core."""
    im, px = _rings([SW["s"], SW["b"], SW["l"]], SW["h"], rind=(SW["s"], SW["d"]))
    for y in range(N):
        for x in range(N):
            if (x + y) < 9 and px[x, y] == SW["l"]:
                px[x, y] = SW["h"]
    return im


# ============================================================ save + present
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


def main():
    gw_bark = {"greatwood_log_furrowed_r3": gw_bark_v("furrowed"), "greatwood_log_shaggy_r3": gw_bark_v("shaggy"),
               "greatwood_log_aged_r3": gw_bark_v("aged")}
    sw_bark = {"silverwood_log_serene_r3": sw_serene(), "silverwood_log_birch_r3": sw_birch(),
               "silverwood_log_moonlit_r3": sw_moonlit()}
    gw_cores = {"greatwood_core_rings_r3": gw_core_rings(), "greatwood_core_heart_r3": gw_core_heart(),
                "greatwood_core_burl_r3": gw_core_burl()}
    sw_cores = {"silverwood_core_heart_r3": sw_core_heart(), "silverwood_core_halo_r3": sw_core_halo(),
                "silverwood_core_pale_r3": sw_core_pale()}
    allt = {**gw_bark, **sw_bark, **gw_cores, **sw_cores}
    for name, img in allt.items():
        save_both(img, name)

    gw_top = gw_cores["greatwood_core_rings_r3"]
    sw_top = sw_cores["silverwood_core_heart_r3"]
    gw_side = gw_bark["greatwood_log_furrowed_r3"]
    sw_side = sw_bark["silverwood_log_serene_r3"]

    def bark_row(img, label, top):
        return two_col(lbl(tile_grid(img, 2, 3, 8), "2x3 tile (parallel logs)"),
                       lbl(stack_iso(top, img, 3), "3-tall trunk"), label)

    sheet("GREATWOOD LOG r3 - edges now flow across the seam (2x3 tile | 3-tall trunk)", [
        bark_row(gw_bark["greatwood_log_furrowed_r3"], "A  furrowed - deep irregular wandering furrows", gw_top),
        bark_row(gw_bark["greatwood_log_shaggy_r3"], "B  shaggy - furrows + fine vertical fibres", gw_top),
        bark_row(gw_bark["greatwood_log_aged_r3"], "C  aged - furrows + sparse irregular checks", gw_top),
    ], PREV / "sheet-greatwood-log-r3.png")

    sheet("SILVERWOOD LOG r3 - pristine & serene, edges flow (2x3 tile | 3-tall trunk)", [
        bark_row(sw_bark["silverwood_log_serene_r3"], "A  serene - smooth pale, soft grooves, whisper teal", sw_top),
        bark_row(sw_bark["silverwood_log_birch_r3"], "B  birch - horizontal lenticels, merges perfectly", sw_top),
        bark_row(sw_bark["silverwood_log_moonlit_r3"], "C  moonlit - soft cylindrical sheen, ethereal", sw_top),
    ], PREV / "sheet-silverwood-log-r3.png")

    def core_row(name, label, side):
        core = allt[name]
        return two_col(lbl(tile_grid(core, 1, 1, 12), "end grain (flat)"),
                       lbl(BR.iso_block(core, side, side, scale=10), "on a log end"), label)

    sheet("GREATWOOD CORES r3 - end-grain (side bark = furrowed r3)", [
        core_row("greatwood_core_rings_r3", "1  rings - tight warm growth rings", gw_side),
        core_row("greatwood_core_heart_r3", "2  heart - dark heartwood fading to sapwood", gw_side),
        core_row("greatwood_core_burl_r3", "3  burl - eccentric off-centre swirl", gw_side),
    ], PREV / "sheet-greatwood-cores-r3.png")

    sheet("SILVERWOOD CORES r3 - serene end-grain (side bark = serene r3)", [
        core_row("silverwood_core_heart_r3", "1  heart - luminous heart, single teal whisper", sw_side),
        core_row("silverwood_core_halo_r3", "2  halo - one soft teal ring, quiet magic", sw_side),
        core_row("silverwood_core_pale_r3", "3  pale - ultra-clean, no teal", sw_side),
    ], PREV / "sheet-silverwood-cores-r3.png")

    print("done:", len(allt), "textures")


# gw_bark name shadows the dict below; alias the builder
gw_bark_v = gw_bark

if __name__ == "__main__":
    main()
