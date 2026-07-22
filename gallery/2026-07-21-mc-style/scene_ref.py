#!/usr/bin/env python3
"""World-cross-section reference. Builds a Minecraft-style vertical slice: a grassland (grass -> dirt
-> stone strata with igneous blobs + ores -> deepslate) meeting a desert (sand -> sandstone -> stone
-> deepslate), with OUR custom stone types woven in as veins/layers, exactly where a player would see
them in context. A legend strip below isolates + names each custom stone.

REFERENCE POLICY: vanilla textures are reference-only — read from scratchpad, composed image WRITTEN
to scratchpad, NEVER committed. Our own stone pixels (out/*_gen.png) + this code live in the repo.
"""
import random
import sys
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
STONE = HERE.parent / "2026-07-21-stone-practice"
sys.path.insert(0, str(STONE / "src"))
import make_stones as MS   # noqa: E402

SCRATCH = Path("/tmp/claude-0/-home-user/e1ce8e98-01cb-5256-a7fd-6ca103c920b9/scratchpad")
REF = SCRATCH / "vanilla-ref"
OUT = STONE / "out"
N, SCALE = 16, 4
W, H = 20, 15

def van(name):
    return Image.open(REF / f"{name}.png").convert("RGBA")

def ours(name):
    return Image.open(OUT / f"{name}_gen.png").convert("RGBA")

tex = {n: van(n) for n in ["grass_block_side", "dirt", "stone", "diorite", "andesite", "granite",
                           "coal_ore", "iron_ore", "gravel", "deepslate", "deepslate_coal_ore",
                           "deepslate_iron_ore", "sand", "sandstone"]}
for n in ["marble", "slate", "shale", "granite", "basalt", "sandstone"]:
    tex["our_" + n] = ours(n)

DESERT_X = 13
grid = [[None] * W for _ in range(H)]
for r in range(H):
    for c in range(W):
        if c < DESERT_X:                                   # grassland column
            grid[r][c] = ("grass_block_side" if r == 0 else "dirt" if r <= 2
                          else "stone" if r <= 9 else "deepslate")
        else:                                              # desert column
            grid[r][c] = ("sand" if r <= 2 else "sandstone" if r <= 5
                          else "stone" if r <= 9 else "deepslate")

# our custom stones as in-context blobs (name, c0,r0,c1,r1)
BLOBS = [("our_marble", 2, 4, 3, 5), ("our_granite", 9, 4, 10, 5), ("our_slate", 6, 6, 7, 7),
         ("our_shale", 3, 8, 4, 9), ("our_basalt", 5, 11, 6, 12), ("our_sandstone", 13, 3, 15, 5)]
claimed = set()
for name, c0, r0, c1, r1 in BLOBS:
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            grid[r][c] = name
            claimed.add((r, c))

# scatter vanilla igneous accents + ores into unclaimed stone/deepslate cells (deterministic)
rng = random.Random(11)
def scatter(kinds, zone_rows, n):
    placed = 0
    tries = 0
    while placed < n and tries < 400:
        tries += 1
        r = rng.randrange(*zone_rows); c = rng.randrange(0, W)
        if (r, c) in claimed:
            continue
        base = grid[r][c]
        if base not in ("stone", "deepslate"):
            continue
        grid[r][c] = rng.choice(kinds); claimed.add((r, c)); placed += 1
scatter(["diorite", "andesite", "granite"], (3, 10), 7)   # vanilla igneous blobs in stone
scatter(["coal_ore", "iron_ore"], (3, 10), 6)             # ores in stone
scatter(["gravel"], (3, 10), 2)
scatter(["deepslate_coal_ore", "deepslate_iron_ore"], (10, H), 4)  # deepslate ores

scene = Image.new("RGBA", (W * N, H * N))
for r in range(H):
    for c in range(W):
        scene.alpha_composite(tex[grid[r][c]], (c * N, r * N))
scene = scene.resize((scene.width * SCALE, scene.height * SCALE), Image.NEAREST)

# legend: our 6 custom stones isolated + named
legend_names = ["marble", "slate", "shale", "granite", "basalt", "sandstone"]
sw = 16 * SCALE
gap = 18
lg_w = len(legend_names) * (sw + gap)
lg_h = sw + 22

pad = 18
Wtot = max(scene.width, lg_w) + 2 * pad
Htot = 34 + scene.height + 40 + lg_h + pad
canvas = Image.new("RGBA", (Wtot, Htot), MS.BG)
d = ImageDraw.Draw(canvas)
d.text((pad, 10), "Cross-section of our Minecraft world: grassland (left) meeting desert (right)", fill=MS.INK)
canvas.alpha_composite(scene, (pad, 32))
y = 32 + scene.height + 12
d.text((pad, y), "The custom stone types we are adding to the mod (also woven into the world above):", fill=MS.INK)
y += 24
x = pad
for nm in legend_names:
    sw_img = tex["our_" + nm].resize((sw, sw), Image.NEAREST)
    canvas.alpha_composite(sw_img, (x, y))
    d.text((x, y + sw + 4), nm, fill=MS.INK)
    x += sw + gap

out = SCRATCH / "scene-ref.png"                            # scratchpad only (contains vanilla pixels)
canvas.save(out)
print("wrote", out)
