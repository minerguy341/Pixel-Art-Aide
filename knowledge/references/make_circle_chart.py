#!/usr/bin/env python3
"""Generate our own pixel-circle chart (replaces the old user-provided .webp).

Pure algorithm — the Bresenham midpoint-circle outline — so the output is entirely original
and safe to publish. Odd diameters (integer centre) from 3..21; each ring is drawn on its own
pixel grid, labelled by diameter, with the 16x16-relevant sizes (11, 13) flagged.

Run: python3 knowledge/references/make_circle_chart.py  (writes pixel-circle-chart.png beside it)
"""
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
DIAMS = [3, 5, 7, 9, 11, 13, 15, 17, 19, 21]
CELL = 9          # px per texture-pixel
BG = (244, 244, 240, 255)
GRID = (216, 216, 210, 255)
ON = (38, 34, 30, 255)          # ring cell
FLAG = (127, 232, 216, 255)     # teal flag for 16x16-fit sizes
INK = (40, 40, 40, 255)
COLS = 5
PAD = 18
LABEL_H = 18


def outline(d):
    """Bresenham midpoint circle outline for an odd diameter d → set of (x,y) cells."""
    r = (d - 1) // 2
    cx = cy = r
    cells = set()
    x, y, err = r, 0, 1 - r
    while x >= y:
        for sx, sy in ((x, y), (y, x), (-x, y), (-y, x), (x, -y), (y, -x), (-x, -y), (-y, -x)):
            cells.add((cx + sx, cy + sy))
        y += 1
        if err < 0:
            err += 2 * y + 1
        else:
            x -= 1
            err += 2 * (y - x) + 1
    return cells


def draw_circle(d):
    cells = outline(d)
    w = d * CELL + 1
    img = Image.new("RGBA", (w, w + LABEL_H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img)
    # pixel grid
    for i in range(d + 1):
        dr.line([(i * CELL, LABEL_H), (i * CELL, LABEL_H + d * CELL)], fill=GRID)
        dr.line([(0, LABEL_H + i * CELL), (d * CELL, LABEL_H + i * CELL)], fill=GRID)
    for (x, y) in cells:
        x0, y0 = x * CELL + 1, LABEL_H + y * CELL + 1
        dr.rectangle([x0, y0, x0 + CELL - 1, y0 + CELL - 1], fill=ON)
    fits = d in (11, 13)
    tag = "  (fits 16x16)" if fits else ""
    dr.text((0, 3), f"d={d}  r={(d - 1) // 2}{tag}", fill=(FLAG if fits else INK))
    return img


def main():
    tiles = [draw_circle(d) for d in DIAMS]
    tw = max(t.width for t in tiles)
    th = max(t.height for t in tiles)
    rows = (len(tiles) + COLS - 1) // COLS
    W = COLS * tw + (COLS + 1) * PAD
    H = rows * th + (rows + 1) * PAD + 40
    canvas = Image.new("RGBA", (W, H), BG)
    dr = ImageDraw.Draw(canvas)
    dr.text((PAD, 12), "PIXEL CIRCLE CHART  -  odd diameters, Bresenham midpoint outline (generated, CC0)",
            fill=INK)
    dr.text((PAD, 26), "Place the ring cells exactly; never freehand. Teal = fills a 16x16 sprite (13 = 1px margin, 11 = room for glow).",
            fill=(90, 90, 90, 255))
    for i, t in enumerate(tiles):
        r, c = divmod(i, COLS)
        x = PAD + c * (tw + PAD)
        y = 40 + PAD + r * (th + PAD)
        canvas.alpha_composite(t, (x, y))
    out = HERE / "pixel-circle-chart.png"
    canvas.save(out)
    print("wrote", out, canvas.size)


if __name__ == "__main__":
    main()
