#!/usr/bin/env python3
"""Random-tiling PREVIEW for the leaf candidates — a visualisation only, NOT a blockstate.

Vanilla leaves are a single fixed-orientation model (no random rotation). This shows what a
wall of each leaf candidate would look like IF we gave it a 4-way random-rotation blockstate
(y-rotation only, like vanilla's stone/dirt/sand): each block tile independently rotated
0/90/180/270. Fixed wall on the left (what ships today) vs random-rotated on the right, so the
repeat-breaking is legible. Deterministic per candidate (seeded) so re-runs are identical.
"""
from pathlib import Path
from PIL import Image, ImageDraw
import random

HERE = Path(__file__).resolve().parent
OUT = HERE.parent / "out"
PREV = HERE.parent / "previews"
WALL = 6          # blocks per side
SCALE = 4
BG = (110, 110, 116, 255)
INK = (250, 250, 250, 255)
GAP = 24
PAD = 16
ROTS = [Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]  # + identity


def wall(tex, randomize, seed):
    n = tex.width
    rng = random.Random(seed)
    canvas = Image.new("RGBA", (n * WALL, n * WALL), (0, 0, 0, 0))
    for by in range(WALL):
        for bx in range(WALL):
            t = tex
            if randomize:
                r = rng.randint(0, 3)
                if r:
                    t = tex.transpose(ROTS[r - 1])
            canvas.alpha_composite(t, (bx * n, by * n))
    return canvas.resize((canvas.width * SCALE, canvas.height * SCALE), Image.NEAREST)


def labelled(img, text):
    strip = Image.new("RGBA", (img.width, img.height + 20), (0, 0, 0, 0))
    strip.alpha_composite(img, (0, 20))
    ImageDraw.Draw(strip).text((0, 4), text, fill=INK)
    return strip


def candidate_row(name, label, seed):
    tex = Image.open(OUT / f"{name}.png").convert("RGBA")
    fixed = labelled(wall(tex, False, seed), "fixed (ships today)")
    rand = labelled(wall(tex, True, seed), "random-rotated (preview)")
    h = max(fixed.height, rand.height)
    w = fixed.width + rand.width + GAP
    row = Image.new("RGBA", (w, h + 18), (0, 0, 0, 0))
    ImageDraw.Draw(row).text((0, 2), label, fill=INK)
    row.alpha_composite(fixed, (0, 18))
    row.alpha_composite(rand, (fixed.width + GAP, 18))
    return row


def sheet(title, rows, out):
    w = max(r.width for r in rows) + 2 * PAD
    h = sum(r.height for r in rows) + GAP * (len(rows) - 1) + 2 * PAD + 26
    canvas = Image.new("RGBA", (w, h), BG)
    ImageDraw.Draw(canvas).text((PAD, 8), title, fill=INK)
    y = 30
    for r in rows:
        canvas.alpha_composite(r, (PAD, y))
        y += r.height + GAP
    canvas.save(out)
    print("wrote", out.name, canvas.size)


sheet("GREATWOOD LEAVES  -  fixed vs random-rotated wall (preview only, no blockstate)", [
    candidate_row("greatwood_leaves_broadleaf", "A  broadleaf 33%", 101),
    candidate_row("greatwood_leaves_dense", "B  dense 22%", 102),
    candidate_row("greatwood_leaves_accent", "C  accent 32%", 103),
], PREV / "sheet-greatwood-leaves-randomtile.png")

sheet("SILVERWOOD LEAVES  -  fixed vs random-rotated wall (preview only, no blockstate)", [
    candidate_row("silverwood_leaves_airy", "A  airy 33%", 201),
    candidate_row("silverwood_leaves_canopy", "B  canopy 18%", 202),
    candidate_row("silverwood_leaves_glow", "C  glow 30%", 203),
], PREV / "sheet-silverwood-leaves-randomtile.png")
