#!/usr/bin/env python3
"""r5: SIX more silverwood grain candidates — all pristine & serene, pale, edges flow (parallel logs
merge), teal-free bark (the teal HEART stays a separate core axis; trunks are topped with the canon
teal-heart core just to show the intended look).

New directions, distinct from every prior silverwood attempt (smooth/lenticel/shimmer, runed/polished/
veined, serene/birch/moonlit, silk/woven/dappled): flowing · marbled · frosted · damask · satin · ghostring.
Builds on make_r3 helpers. Deterministic.
"""
import math
from PIL import Image
import make_r3 as R

SW, N, T = R.SW, R.N, R.T
blank, circ, h2 = R.blank, R.circ, R.h2
tile_grid, stack_iso, lbl, two_col, sheet = R.tile_grid, R.stack_iso, R.lbl, R.two_col, R.sheet
OUT, PREV = R.OUT, R.PREV
CF = ((0xEA), (0xF2), (0xF0), 255)  # cool near-white for frost


def sw_flowing():
    """Long soft vertical flow-lines that meander slowly — silk/water read. Streaks run full height."""
    im, px = blank()
    bases = [0, 5, 10]                      # 0 straddles the seam
    for y in range(N):
        shift = int(round(1.2 * math.sin(y / 16 * 2 * math.pi)))
        lines = {(b + shift) % N for b in bases}
        for x in range(N):
            if x in lines:
                c = SW["b"]
            elif any(circ(x, l) == 1 for l in lines):
                c = SW["sof"]
            else:
                c = SW["l"]
            if 6 <= x <= 7 and c == SW["l"]:
                c = SW["h"]
            px[x, y] = c
    return im


def sw_marbled():
    """Soft wandering thin veins over pale — pristine marble. Veins wrap (tile)."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            c = SW["l"] if h2(x, y // 4, 11) > 0.06 else SW["sof"]
            px[x, y] = c
    # two wandering 1px veins that return to their start (tileable)
    for seed, base in ((21, 4), (22, 11)):
        x = base
        for y in range(N):
            px[x % N, y] = SW["s"]
            px[(x + 1) % N, y] = SW["sof"]
            step = -1 if h2(x, y, seed) < 0.34 else (1 if h2(x, y, seed) > 0.66 else 0)
            x += step
        # nudge back toward base so the wrap seam matches (soft)
    return im


def sw_frosted():
    """Cool frosty sheen + tiny white sparkle specks (NO teal) — icy pristine."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            n = 0.5 * h2(x // 3, y // 3, 31) + 0.5 * h2(x, y // 2, 32)
            c = CF if n > 0.72 else SW["b"] if n < 0.30 else SW["l"]
            if circ(x, 0) == 0:
                c = SW["sof"]                 # soft seam groove so logs merge
            px[x, y] = c
    for (sx, sy) in ((4, 3), (11, 6), (7, 10), (13, 13), (2, 12)):
        px[sx, sy] = SW["h"]                  # sparkle specks (near-white, not teal)
    return im


def sw_damask():
    """Faint woven diamond lattice (patterned silk) — very low contrast, refined."""
    im, px = blank()
    for y in range(N):
        for x in range(N):
            # diamond lattice with period 8 (tiles): |dx|+|dy| within a cell
            cx, cy = x % 8, y % 8
            d = abs(cx - 4) + abs(cy - 4)
            if d == 4:
                c = SW["sof"]                 # faint lattice line
            elif d < 2:
                c = SW["h"]                    # tiny bright node
            else:
                c = SW["l"]
            px[x, y] = c
    return im


def sw_satin():
    """Soft vertical satin sheen bands (bright ribbons) — smooth & luminous."""
    im, px = blank()
    bands = {2, 8, 13}                         # bright ribbon centres; edges fall between → merge
    for y in range(N):
        for x in range(N):
            db = min(circ(x, b) for b in bands)
            if db == 0:
                c = SW["h"]
            elif db == 1:
                c = SW["l"]
            elif db == 2:
                c = SW["b"]
            else:
                c = SW["sof"]
            if h2(x, y // 5, 51) < 0.04 and c == SW["l"]:
                c = SW["sof"]
            px[x, y] = c
    return im


def sw_ghostring():
    """Faint HORIZONTAL growth banding — merges horizontally perfectly (no vertical seam)."""
    im, px = blank()
    for y in range(N):
        band = (y // 2) % 3
        row = SW["l"] if band == 0 else SW["b"] if band == 1 else SW["sof"]
        for x in range(N):
            c = row
            if h2(x, y, 61) < 0.05:
                c = SW["h"]                    # faint sparkle in the bands
            px[x, y] = c
    return im


def main():
    grains = {
        "silverwood_grain_flowing_r5": sw_flowing(),
        "silverwood_grain_marbled_r5": sw_marbled(),
        "silverwood_grain_frosted_r5": sw_frosted(),
        "silverwood_grain_damask_r5": sw_damask(),
        "silverwood_grain_satin_r5": sw_satin(),
        "silverwood_grain_ghostring_r5": sw_ghostring(),
    }
    for name, img in grains.items():
        R.save_both(img, name)

    top = Image.open(OUT / "silverwood_core_teal_r4.png").convert("RGBA")  # canon teal-heart top

    def row(name, label):
        tex = grains[name]
        return two_col(lbl(tile_grid(tex, 2, 3, 8), "2x3 tile (parallel logs)"),
                       lbl(stack_iso(top, tex, 3), "3-tall trunk"), label)

    sheet("SILVERWOOD GRAIN r5 (1/2) - pristine & serene, teal-free bark (trunk top = canon teal heart)", [
        row("silverwood_grain_flowing_r5", "D  flowing - long soft meandering flow-lines (silk)"),
        row("silverwood_grain_marbled_r5", "E  marbled - soft wandering pale veins"),
        row("silverwood_grain_frosted_r5", "F  frosted - cool sheen + white sparkle specks (icy)"),
    ], PREV / "sheet-silverwood-grain-r5-1.png")

    sheet("SILVERWOOD GRAIN r5 (2/2) - pristine & serene, teal-free bark (trunk top = canon teal heart)", [
        row("silverwood_grain_damask_r5", "G  damask - faint woven diamond lattice (patterned silk)"),
        row("silverwood_grain_satin_r5", "H  satin - soft vertical sheen ribbons (luminous)"),
        row("silverwood_grain_ghostring_r5", "I  ghost-ring - faint horizontal growth banding"),
    ], PREV / "sheet-silverwood-grain-r5-2.png")

    print("done:", len(grains), "grains")


if __name__ == "__main__":
    main()
