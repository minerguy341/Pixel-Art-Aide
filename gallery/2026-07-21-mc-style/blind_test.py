#!/usr/bin/env python3
"""Blind vanilla-fit test harness. Renders every stone in stones.json as an isometric block in a grid
labelled with NEUTRAL NUMBERS ONLY (no rock names — the judge must not be biased by geology words).
A separate memoryless instance of Claude (no web) is shown the sheet and asked which block feels most
out of place from vanilla Minecraft. The index->stone key is printed to stdout (for us), NOT drawn."""
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

STONE = Path(__file__).resolve().parent.parent / "2026-07-21-stone-practice"
sys.path.insert(0, str(STONE / "src"))
import make_stones as MS   # noqa: E402
import stonegen as SG      # noqa: E402
from aide import blockrender as BR  # noqa: E402

specs = json.load(open(STONE / "stones.json"))
order = list(specs)                                   # stable stones.json order
scale = 9
cell_w = 16 * scale * 2 + 40
cell_h = 16 * scale * 2 + 60
cols = 3
rows = (len(order) + cols - 1) // cols
canvas = Image.new("RGBA", (cols * cell_w + 24, rows * cell_h + 40), MS.BG)
d = ImageDraw.Draw(canvas)
d.text((16, 12), "Which block feels most OUT OF PLACE from vanilla Minecraft?", fill=MS.INK)
for i, name in enumerate(order):
    img = SG.render(specs[name])
    blk = BR.iso_block(img, img, img, scale=scale)
    cx = 12 + (i % cols) * cell_w
    cy = 36 + (i // cols) * cell_h
    canvas.alpha_composite(blk, (cx + (cell_w - blk.width) // 2, cy + 24))
    d.text((cx + cell_w // 2 - 6, cy), f"#{i + 1}", fill=MS.INK)
out = Path(__file__).resolve().parent / "blind-test.png"
canvas.save(out)
print("wrote", out.name, canvas.size)
print("KEY (not shown to judge):", {i + 1: n for i, n in enumerate(order)})
