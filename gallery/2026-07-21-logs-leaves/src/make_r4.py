#!/usr/bin/env python3
"""r4: MORE wood-log (bark) candidates for both woods, and SILVERWOOD grain shown WITH and WITHOUT
the teal heart (the heartwood node — canon per the tree-growth study, but offered both ways).

Builds on make_r3 helpers (palettes, hash, edge-flow furrow logic, renderers). Bark keeps the r3
edge fix (a furrow/groove straddles the wrap so parallel logs merge). Silverwood bark is teal-free
so the ONLY teal is the core, making the with/without-heart comparison clean. Deterministic.
"""
import math
from PIL import Image, ImageDraw
import make_r3 as R  # same dir; reuse palettes + helpers

GW, SW, N, T = R.GW, R.SW, R.N, R.T
blank, circ, h2 = R.blank, R.circ, R.h2
tile_grid, stack_iso, lbl, sheet = R.tile_grid, R.stack_iso, R.lbl, R.sheet
BR = R.BR
OUT, PREV = R.OUT, R.PREV
INK = (250, 250, 250, 255)


# ---------------------------------------------------------------- furrow map (seam-straddling)
def furrow_map(centers, band=8):
    def eff(c, b):
        w = h2(c, b, 77)
        off = -1 if w < 0.34 else (1 if w > 0.66 else 0)
        return (c + off) % N

    def df(x, y):
        bb = (y // band) % (N // band)
        return min(circ(x, eff(c, bb)) for c in centers)
    return df


# ---------------------------------------------------------------- GREATWOOD BARK r4
def gw_deep_fissured():
    """Two deep wide fissures (one straddles the seam) with broad rounded highlighted ridges."""
    im, px = blank()
    df = furrow_map([0, 8], band=8)
    for y in range(N):
        for x in range(N):
            d = df(x, y)
            if d == 0:
                c = GW["k"] if h2(x, y // 3, 88) < 0.4 else GW["f"]
            elif d == 1:
                c = GW["f"]
            elif d == 2:
                c = GW["b"]
            elif d == 3:
                c = GW["r"]
            else:
                c = GW["h"]
            if c in (GW["h"], GW["r"]) and h2(x, y // 3, 41) < 0.14:
                c = GW["b"]
            px[x, y] = c
    return im


def gw_interlaced():
    """Diagonal interlocked grain — furrows lean 0.5 col/row and wrap every 16 rows (tiles)."""
    im, px = blank()
    centers = [0, 8]
    for y in range(N):
        eff = {(c + (y // 2)) % N for c in centers}
        for x in range(N):
            d = min(circ(x, e) for e in eff)
            if d == 0:
                c = GW["f"] if (y % 2) else GW["k"]
            elif d == 1:
                c = GW["b"]
            elif d == 2:
                c = GW["r"]
            else:
                c = GW["h"] if ((x + y) % 5) else GW["r"]
            if c in (GW["h"], GW["r"]) and h2(x, y, 42) < 0.12:
                c = GW["b"]
            px[x, y] = c
    return im


def gw_knotted():
    """Furrowed base + a large oval branch-scar knot (greatwood has radiating branches)."""
    im, px = blank()
    df = furrow_map([0, 5, 10, 13], band=8)
    for y in range(N):
        for x in range(N):
            d = df(x, y)
            c = (GW["k"] if h2(x, y // 3, 88) < 0.35 else GW["f"]) if d == 0 else \
                GW["f"] if d == 1 else GW["b"] if d == 2 else GW["r"] if d == 3 else GW["h"]
            if c in (GW["h"], GW["r"]) and h2(x, y // 3, 43) < 0.12:
                c = GW["b"]
            px[x, y] = c
    # branch-scar knot: concentric ovals around (7,6)
    kx, ky = 7, 6
    for y in range(N):
        for x in range(N):
            rr = math.hypot((x - kx) / 1.15, (y - ky) / 1.5)
            if rr < 1.1:
                px[x, y] = GW["k"]
            elif rr < 2.2:
                px[x, y] = GW["f"]
            elif rr < 3.1:
                px[x, y] = GW["b"] if ((x + y) % 2) else GW["r"]
    return im


# ---------------------------------------------------------------- SILVERWOOD BARK r4 (serene, TEAL-FREE)
def sw_silk():
    """Ultra-pristine: near-flat pale, one soft seam groove, one faint sheen column. No teal."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            dg = circ(x, 0)
            c = SW["b"] if dg == 0 else SW["sof"] if dg == 1 else SW["l"]
            if 6 <= x <= 7:
                c = SW["h"]
            if c == SW["l"] and h2(x, y // 5, 61) < 0.04:
                c = SW["sof"]
            px[x, y] = c
    return im


def sw_woven():
    """Gentle wavy interlocked pale grain — soft streaks displaced by a sine of y. No teal."""
    im, px = blank()
    bases = [3, 8, 13]
    for y in range(N):
        shift = int(round(1.5 * math.sin(y / 16 * 2 * math.pi)))
        streaks = {(b + shift) % N for b in bases}
        for x in range(N):
            if x in streaks:
                c = SW["sof"]
            elif any(circ(x, s) == 1 for s in streaks):
                c = SW["b"]
            else:
                c = SW["l"]
            if (x + y) < 5 and c == SW["l"]:
                c = SW["h"]
            px[x, y] = c
    return im


def sw_dappled():
    """Soft low-frequency dapples on pale bark (light through canopy). No teal."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            n = 0.5 * h2(x // 3, y // 3, 71) + 0.5 * h2(x // 2, y // 4, 72)
            c = SW["h"] if n > 0.70 else SW["b"] if n < 0.32 else SW["l"]
            # keep a soft seam groove so logs still merge cleanly
            if circ(x, 0) == 0:
                c = SW["sof"]
            px[x, y] = c
    return im


# ---------------------------------------------------------------- SILVERWOOD CORES: with / without heart
def sw_core_teal():
    im, px = R._rings([SW["s"], SW["b"], SW["l"]], SW["l"], rind=(SW["s"], SW["d"]))
    for y in range(N):
        for x in range(N):
            r = math.hypot(x - 7.5, y - 7.5)
            if r < 1.4:
                px[x, y] = SW["h"]
            elif (x + y) < 9 and px[x, y] == SW["l"]:
                px[x, y] = SW["h"]
    px[7, 7] = SW["t"]  # the node — a single luminous teal heart
    return im


def sw_core_plain():
    im, px = R._rings([SW["s"], SW["b"], SW["l"]], SW["h"], rind=(SW["s"], SW["d"]))
    for y in range(N):
        for x in range(N):
            if (x + y) < 9 and px[x, y] == SW["l"]:
                px[x, y] = SW["h"]
    return im  # no teal at all


# ---------------------------------------------------------------- present
def three_col(a, b, c, label, gap=20):
    h = max(a.height, b.height, c.height)
    row = Image.new("RGBA", (a.width + b.width + c.width + 2 * gap, h + 18), T)
    ImageDraw.Draw(row).text((0, 2), label, fill=INK)
    x = 0
    for im in (a, b, c):
        row.alpha_composite(im, (x, 18))
        x += im.width + gap
    return row


def two_col(a, b, label, gap=24):
    return R.two_col(a, b, label, gap)


def main():
    gw = {"greatwood_log_deepfissured_r4": gw_deep_fissured(),
          "greatwood_log_interlaced_r4": gw_interlaced(),
          "greatwood_log_knotted_r4": gw_knotted()}
    sw = {"silverwood_log_silk_r4": sw_silk(),
          "silverwood_log_woven_r4": sw_woven(),
          "silverwood_log_dappled_r4": sw_dappled()}
    cores = {"silverwood_core_teal_r4": sw_core_teal(), "silverwood_core_plain_r4": sw_core_plain()}
    for name, img in {**gw, **sw, **cores}.items():
        R.save_both(img, name)

    gw_top = Image.open(OUT / "greatwood_core_rings_r3.png").convert("RGBA")
    core_teal = cores["silverwood_core_teal_r4"]
    core_plain = cores["silverwood_core_plain_r4"]

    # GREATWOOD r4: 2x3 tile | 3-tall trunk
    sheet("GREATWOOD LOG r4 - more bark candidates (2x3 tile | 3-tall trunk)", [
        two_col(lbl(tile_grid(gw["greatwood_log_deepfissured_r4"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(gw_top, gw["greatwood_log_deepfissured_r4"], 3), "3-tall trunk"),
                "G  deep-fissured - two deep wide fissures, broad ridges"),
        two_col(lbl(tile_grid(gw["greatwood_log_interlaced_r4"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(gw_top, gw["greatwood_log_interlaced_r4"], 3), "3-tall trunk"),
                "H  interlaced - diagonal interlocked grain"),
        two_col(lbl(tile_grid(gw["greatwood_log_knotted_r4"], 2, 3, 8), "2x3 tile"),
                lbl(stack_iso(gw_top, gw["greatwood_log_knotted_r4"], 3), "3-tall trunk"),
                "I  knotted - furrows + a branch-scar knot"),
    ], PREV / "sheet-greatwood-log-r4.png")

    # SILVERWOOD r4: each grain shown WITH the teal heart and WITHOUT
    hdr = two_col(lbl(tile_grid(core_teal, 1, 1, 10), "core: WITH teal heart"),
                  lbl(tile_grid(core_plain, 1, 1, 10), "core: WITHOUT (plain)"),
                  "the two end-grain cores compared")

    def sw_row(name, label):
        tex = sw[name]
        return three_col(lbl(tile_grid(tex, 2, 3, 8), "2x3 tile"),
                         lbl(stack_iso(core_teal, tex, 3), "trunk + teal heart"),
                         lbl(stack_iso(core_plain, tex, 3), "trunk, no heart"),
                         label)

    sheet("SILVERWOOD LOG r4 - serene grain, shown WITH and WITHOUT the teal heart", [
        hdr,
        sw_row("silverwood_log_silk_r4", "A  silk - ultra-pristine near-flat pale"),
        sw_row("silverwood_log_woven_r4", "B  woven - gentle wavy interlocked grain"),
        sw_row("silverwood_log_dappled_r4", "C  dappled - soft canopy-light dapples"),
    ], PREV / "sheet-silverwood-log-r4.png")

    print("done:", len(gw) + len(sw) + len(cores), "textures")


if __name__ == "__main__":
    main()
