#!/usr/bin/env python3
"""Layout mock of ArcaneWorktableScreen (194x196) to eyeball slot/ring/label placement
without a game build. Mirrors the Java coordinates exactly. Renders the INSUFFICIENT state
(partial ring) since it's the busiest. Not the real render — a geometry check."""
from PIL import Image, ImageDraw
from pathlib import Path

W, H = 194, 196
GRID_X, GRID_Y = 44, 24
RESULT_X, RESULT_Y = 150, 42
WAND_X, WAND_Y = 16, 42
INV_X, INV_Y = 16, 114
HOTBAR_Y = 172
RING_PIPS = 16

im = Image.new("RGB", (W, H), (16, 10, 24))
d = ImageDraw.Draw(im)
d.rectangle([0, 0, W - 1, 13], fill=(36, 27, 51))  # chrome

def slot(x, y, col=(55, 48, 74)):
    d.rectangle([x - 1, y - 1, x + 16, y + 16], fill=(11, 9, 18))
    d.rectangle([x, y, x + 15, y + 15], fill=col)

# grid 3x3
for r in range(3):
    for c in range(3):
        slot(GRID_X + c * 18, GRID_Y + r * 18)
slot(WAND_X, WAND_Y, (60, 50, 40))     # wand slot
slot(RESULT_X, RESULT_Y, (48, 60, 58)) # result
# inventory + hotbar
for r in range(3):
    for c in range(9):
        slot(INV_X + c * 18, INV_Y + r * 18)
for c in range(9):
    slot(INV_X + c * 18, HOTBAR_Y)

# vis ring (rectangle perimeter just outside the grid), INSUFFICIENT -> ~60% lit
rx0, ry0 = GRID_X - 5, GRID_Y - 5
w = h = 54 + 10
perim = 2 * (w + h)
step = perim / RING_PIPS
lit = round(RING_PIPS * 0.6)
for i in range(RING_PIPS):
    dd = i * step
    if dd < w:
        px, py = rx0 + int(dd), ry0
    elif dd < w + h:
        px, py = rx0 + w, ry0 + int(dd - w)
    elif dd < 2 * w + h:
        px, py = rx0 + w - int(dd - w - h), ry0 + h
    else:
        px, py = rx0, ry0 + h - int(dd - 2 * w - h)
    col = (224, 138, 138) if i < lit else (55, 48, 74)  # WARN vs off
    d.rectangle([px - 1, py - 1, px + 1, py + 1], fill=col)

# arrow
ay = RESULT_Y + 8
ax = GRID_X + 54 + 8
d.rectangle([ax, ay - 1, ax + 21, ay + 1], fill=(106, 100, 128))
for k in range(7):
    d.rectangle([ax + 22 + k, ay - (7 - k), ax + 22 + k, ay + (7 - k)], fill=(106, 100, 128))

# labels (approx positions)
d.text((WAND_X - 2, WAND_Y + 20), "Wand", fill=(154, 140, 191))
costY = GRID_Y + 54 + 12
d.text((GRID_X + 27 - 12, costY), "Vis:17", fill=(224, 138, 138))
d.text((8, 4), "Arcane Worktable", fill=(232, 217, 255))
d.text((INV_X, INV_Y - 11), "Inventory", fill=(154, 140, 191))

out = Path(__file__).resolve().parent
im.resize((W * 3, H * 3), Image.NEAREST).save(out / "mockup.png")
print("wrote", out / "mockup.png")
