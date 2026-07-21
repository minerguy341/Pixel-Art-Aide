#!/usr/bin/env python3
"""Arcane Worktable red/gold cloth — source of record.

Two products for the T.N.A. worktable (greatwood + brass workshop palette):
  worktable_cloth.png (70x76) — a fancy red-velvet + gold runner for the GUI, blitted behind
    the 3x3 grid: gold embroidered border, hanging tassels top & bottom, drape/fold shading.
  arcane_worktable_top.png (16x16) — the block's top face: greatwood board + brass frame +
    red cloth cells + gold grid lines + gold corner studs (mirrors the GUI motif).
"""
from PIL import Image
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"
OUT.mkdir(parents=True, exist_ok=True)
T = (0, 0, 0, 0)

def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)

R_SH, R_BASE, R_MID, R_SHEEN = hx(0x5A1420), hx(0x8E2233), hx(0xA6394A), hx(0xC25A54)
G_D, G_B, G_H = hx(0x7A5A22), hx(0xC9A24A), hx(0xF2D98A)

def cloth():
    # Fitted velvet mat that hugs the 54px 3x3 grid (62x62 = ~4px margin all round). A gold
    # embroidered border + small corner tassels keep it "fancy" without an oversized overhang.
    S = 62
    im = Image.new("RGBA", (S, S), T)
    px = im.load()

    def vel(x, y):
        v = R_BASE
        if x % 6 == 0:
            v = R_SH                       # fold crease
        elif (x // 6) % 2 == 0 and (x % 6) in (2, 3):
            v = R_MID
        if (x + y) % 9 == 0:
            v = R_SHEEN                    # sparse velvet sheen
        return v

    for y in range(S):
        for x in range(S):
            px[x, y] = vel(x, y)

    # gold embroidered border: a 2px band inset 2px from the edge, with highlight studs
    x0, y0, x1, y1 = 2, 2, S - 3, S - 3
    for x in range(x0, x1 + 1):
        px[x, y0] = px[x, y1] = G_B
        px[x, y0 + 1] = px[x, y1 - 1] = G_D
    for y in range(y0, y1 + 1):
        px[x0, y] = px[x1, y] = G_B
        px[x0 + 1, y] = px[x1 - 1, y] = G_D
    for x in range(x0 + 3, x1 - 2, 6):
        px[x, y0] = px[x, y1] = G_H
    for y in range(y0 + 3, y1 - 2, 6):
        px[x0, y] = px[x1, y] = G_H

    # small corner tassels poking out each corner
    for cx, cy, dx, dy in [(0, 0, -1, -1), (S - 1, 0, 1, -1), (0, S - 1, -1, 1), (S - 1, S - 1, 1, 1)]:
        px[cx, cy] = G_H
        for k in range(1, 3):
            xx, yy = cx + dx * k, cy + dy * k
            if 0 <= xx < S and 0 <= yy < S:
                px[xx, yy] = G_B

    im.save(OUT / "worktable_cloth.png")
    return im

def block_top():
    GW_D, GW_B, GW_H = hx(0x30201C), hx(0x4F3B25), hx(0x60492C)
    BR_D, BR_B = hx(0x6B4F28), hx(0x8F6B38)
    t = Image.new("RGBA", (16, 16))
    p = t.load()
    for y in range(16):
        for x in range(16):
            p[x, y] = GW_B if (x + y) % 2 else GW_H
    for x in range(16):
        p[x, 0] = p[x, 15] = GW_D
    for y in range(16):
        p[0, y] = p[15, y] = GW_D
    for x in range(1, 15):
        p[x, 1] = BR_B
        p[x, 14] = BR_D
    for y in range(1, 15):
        p[1, y] = BR_B
        p[14, y] = BR_D
    for y in range(3, 13):
        for x in range(3, 13):
            p[x, y] = R_MID if x % 3 == 0 else (R_SH if (x + y) % 5 == 0 else R_BASE)
    for k in (6, 9):
        for i in range(3, 13):
            p[k, i] = G_B
            p[i, k] = G_B
    for sx, sy in [(2, 2), (13, 2), (2, 13), (13, 13)]:
        p[sx, sy] = G_H
    t.save(OUT / "arcane_worktable_top.png")
    return t

if __name__ == "__main__":
    cloth()
    block_top()
    print("wrote worktable_cloth.png (62x62) + arcane_worktable_top.png (16x16) to", OUT)
