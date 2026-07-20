#!/usr/bin/env python3
"""16x16 GUI glyphs for the six T.N.A. primals, downscaled from the HD aspect icons we
authored (gallery/2026-07-20-aspect-primals). Source of record = those generators + this
downscale. Used in the Arcane Worktable's per-primal vis ring."""
from PIL import Image
from pathlib import Path

SRC = Path("gallery/2026-07-20-aspect-primals/out")
OUT = Path("gallery/2026-07-20-primal-glyphs/out")
OUT.mkdir(parents=True, exist_ok=True)
PRIMALS = ["ventus", "tellus", "flamma", "unda", "forma", "discordia"]

for name in PRIMALS:
    icon = Image.open(SRC / f"{name}_backdrop.png").convert("RGBA")
    # 64 -> 16: LANCZOS keeps the badge legible; then a light alpha threshold crisps the rim.
    small = icon.resize((16, 16), Image.LANCZOS)
    px = small.load()
    for y in range(16):
        for x in range(16):
            r, g, b, a = px[x, y]
            px[x, y] = (r, g, b, 0 if a < 64 else (255 if a > 160 else a))
    small.save(OUT / f"{name}.png")
print("wrote", [p.name for p in OUT.glob("*.png")])
