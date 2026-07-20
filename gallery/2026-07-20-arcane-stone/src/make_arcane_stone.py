#!/usr/bin/env python3
"""arcane_stone — dressed arcane blue-grey ashlar, the neutral apparatus material for T.N.A.
Seamless 16x16. Palette = the apparatus casing ramp (2A2E3B..5C6478) + one faint teal fleck,
so it reads as 'built arcane stone' and lets emissive accents pop against it. Original pixels
(reference-policy: study idioms, ship our own). Generator is the source of record."""
from PIL import Image
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"
OUT.mkdir(parents=True, exist_ok=True)

def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)

MORTAR = hx(0x242834)  # deep joint
SHADOW = hx(0x383E50)
BASE   = hx(0x474E62)
BASE2  = hx(0x414860)
HI     = hx(0x5C6478)
TEAL   = hx(0x4E7E78)  # muted arcane fleck (not saturated — keeps the block neutral)

im = Image.new("RGBA", (16, 16))
px = im.load()

# Ashlar courses: two rows of offset blocks. Horizontal mortar at y=0 and y=8 (wraps),
# vertical joints staggered per course. Fill blocks with base + gentle top-lit shading.
# sparse deterministic speck mask (blue-noise-ish), keeps the field from reading as a checker
SPECK = {(2, 3), (5, 6), (3, 12), (11, 4), (13, 10), (7, 9), (10, 13), (6, 2)}
LIGHT = {(4, 5), (12, 6), (9, 11), (2, 10)}

def block_face(x0, x1, y0, y1):
    for y in range(y0, y1):
        for x in range(x0, x1):
            xx, yy = x % 16, y % 16
            if y == y0:
                c = HI            # top edge catches the light
            elif y == y1 - 1:
                c = SHADOW        # bottom edge in shadow
            elif (xx, yy) in SPECK:
                c = BASE2         # scattered darker grain
            elif (xx, yy) in LIGHT:
                c = HI            # a few catch-lights
            else:
                c = BASE
            px[xx, yy] = c

# base fill
for y in range(16):
    for x in range(16):
        px[x, y] = BASE

# course 1 (y 1..7): joints at x=0 and x=8
block_face(1, 8, 1, 8)
block_face(9, 16, 1, 8)
# course 2 (y 9..15): offset joint at x=4 and x=12 (staggered), wraps across the seam
block_face(5, 12, 9, 16)
block_face(13, 16, 9, 16)   # right stub
block_face(0, 4, 9, 16)     # left stub (wraps with the right stub → seamless)

# mortar joints (horizontal wraps at y=0/y=8; verticals per course)
for x in range(16):
    px[x, 0] = MORTAR
    px[x, 8] = MORTAR
for y in range(1, 8):
    px[0, y] = MORTAR
    px[8, y] = MORTAR
for y in range(9, 16):
    px[4, y] = MORTAR
    px[12, y] = MORTAR

# a few deeper weathering pits (no saturated fleck: the neutral material stays neutral so
# emissive apparatus accents read as the magic — apparatus grammar, directives §1/§0)
px[3, 4] = SHADOW
px[11, 3] = SHADOW
px[6, 13] = SHADOW
px[14, 11] = SHADOW

im.save(OUT / "arcane_stone.png")
print("wrote", OUT / "arcane_stone.png")
