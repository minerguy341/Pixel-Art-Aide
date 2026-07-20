#!/usr/bin/env python3
"""Before/after contact sheet for the three relic/node revisions."""
from PIL import Image, ImageDraw
from pathlib import Path
from aide.render import upscale, on_checker

ROOT = Path(__file__).resolve().parents[4]
TNA  = ROOT / "thaumaturgy-the-new-age/src/main/resources/assets/new_age_thaum/textures"
OUT  = Path(__file__).resolve().parent.parent / "out"
PREV = Path(__file__).resolve().parent.parent / "previews"
PREV.mkdir(parents=True, exist_ok=True)

PAIRS = [
    ("aura node",  TNA / "block/aura_node.png",   OUT / "aura_node_rev.png"),
    ("aetherlens", TNA / "item/aetherlens.png",   OUT / "aetherlens_rev.png"),
    ("codex",      TNA / "item/codex.png",        OUT / "codex_rev.png"),
]

SC = 10          # upscale
PAD = 14
GAP = 22
LBL = 20
CELL = 16 * SC
BG = (30, 28, 38, 255)

def load(p):
    return on_checker(upscale(Image.open(p).convert("RGBA"), SC), cell=SC)

rows = len(PAIRS)
W = PAD * 2 + CELL * 2 + GAP + 120
H = PAD * 2 + LBL + rows * (CELL + LBL + GAP)
sheet = Image.new("RGBA", (W, H), BG)
d = ImageDraw.Draw(sheet)

y = PAD
d.text((PAD, y), "BEFORE", fill=(200, 200, 210, 255))
d.text((PAD + CELL + GAP, y), "AFTER", fill=(160, 240, 220, 255))
y += LBL

for name, before, after in PAIRS:
    d.text((PAD, y), name, fill=(220, 215, 225, 255))
    y += LBL
    sheet.alpha_composite(load(before), (PAD, y))
    sheet.alpha_composite(load(after), (PAD + CELL + GAP, y))
    y += CELL + GAP

sheet.save(PREV / "relics-before-after.png")
print("wrote", PREV / "relics-before-after.png", sheet.size)
