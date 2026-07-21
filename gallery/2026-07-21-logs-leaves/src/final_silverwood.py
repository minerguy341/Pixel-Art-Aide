#!/usr/bin/env python3
"""Confirmation render of the DECIDED silverwood log: D flowing bark + PLAIN (no-teal) end grain."""
from PIL import Image, ImageDraw
import make_r3 as R

OUT, PREV = R.OUT, R.PREV
bark = Image.open(OUT / "silverwood_grain_flowing_r5.png").convert("RGBA")
end = Image.open(OUT / "silverwood_core_plain_r4.png").convert("RGBA")

tile = R.lbl(R.tile_grid(bark, 2, 3, 8), "2x3 tile (parallel logs)")
trunk = R.lbl(R.stack_iso(end, bark, 3), "3-tall trunk (plain end)")
grain = R.lbl(R.tile_grid(end, 1, 1, 12), "end grain (plain, no teal)")
row = R.two_col(tile, R.two_col(trunk, grain, "", gap=18), "DECIDED - silverwood log: D flowing + plain end")
R.sheet("SILVERWOOD LOG - final pick (D flowing bark, plain no-teal end grain)", [row],
        PREV / "final-silverwood-log.png")
print("wrote final-silverwood-log.png")
