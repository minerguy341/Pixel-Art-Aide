#!/usr/bin/env python3
"""Reference-anchored blind test. Builds ONE image: (top) an authentic vanilla Minecraft wall
assembled from real vanilla block textures as the judge's anchor, and (bottom) our candidate stones
numbered neutrally. A fresh memoryless instance is asked which of OUR stones would look out of place
if placed in that vanilla wall.

REFERENCE POLICY: the vanilla textures are reference-only. They live in the scratchpad, this script
READS them from there, and the composed image is WRITTEN to the scratchpad — NEVER committed. Only
our own stone pixels + this code live in the repo.
"""
import json
import random
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
STONE = HERE.parent / "2026-07-21-stone-practice"
sys.path.insert(0, str(STONE / "src"))
import make_stones as MS   # noqa: E402
import stonegen as SG      # noqa: E402

SCRATCH = Path("/tmp/claude-0/-home-user/e1ce8e98-01cb-5256-a7fd-6ca103c920b9/scratchpad")
REF = SCRATCH / "vanilla-ref"
N, SCALE = 16, 5

def load(name):
    return Image.open(REF / f"{name}.png").convert("RGBA")

# vanilla wall: mostly stone, sprinkled with the full stone family so every candidate has a fair
# same-family comparator (incl. warm sandstone/granite and pale calcite, not just grey stone).
palette = (["stone"] * 9 + ["diorite", "andesite", "granite", "dirt", "gravel",
                            "coal_ore", "iron_ore", "sandstone", "calcite", "tuff"])
vt = {n: load(n) for n in set(palette)}
cols, rows = 9, 5
rng = random.Random(7)
wall = Image.new("RGBA", (cols * N, rows * N))
for r in range(rows):
    for c in range(cols):
        wall.alpha_composite(vt[rng.choice(palette)], (c * N, r * N))
wall = wall.resize((wall.width * SCALE, wall.height * SCALE), Image.NEAREST)

# our candidates: flat 3x3 tiles, numbered
specs = json.load(open(STONE / "stones.json"))
order = list(specs)
tiles = []
for i, name in enumerate(order):
    t = MS.lbl(MS.tile3(SG.render(specs[name])), f"#{i + 1}")
    tiles.append(t)

pad, gap = 20, 16
tile_w = max(t.width for t in tiles)
per_row = 3
trows = (len(tiles) + per_row - 1) // per_row
tile_h = max(t.height for t in tiles)
grid_w = per_row * tile_w + (per_row - 1) * gap
W = max(wall.width, grid_w) + 2 * pad
H = 30 + wall.height + 40 + trows * (tile_h + gap) + pad
canvas = Image.new("RGBA", (W, H), MS.BG)
d = ImageDraw.Draw(canvas)
d.text((pad, 8), "AUTHENTIC VANILLA MINECRAFT WALL (reference — this is the real look to match)", fill=MS.INK)
canvas.alpha_composite(wall, (pad, 30))
y0 = 30 + wall.height + 12
d.text((pad, y0), "CANDIDATE STONES #1-#6 — which would look OUT OF PLACE if placed in that wall?", fill=MS.INK)
y0 += 26
for i, t in enumerate(tiles):
    cx = pad + (i % per_row) * (tile_w + gap)
    cy = y0 + (i // per_row) * (tile_h + gap)
    canvas.alpha_composite(t, (cx, cy))

out = SCRATCH / "ref-blind-test.png"       # scratchpad only (contains vanilla pixels)
canvas.save(out)
print("wrote", out)
print("KEY (not shown to judge):", {i + 1: n for i, n in enumerate(order)})
