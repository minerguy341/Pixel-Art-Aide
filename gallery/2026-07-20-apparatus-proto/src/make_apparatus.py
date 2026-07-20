"""Part-B experiment: an arcane apparatus 'casing' block applying the mod-study
north star — a restrained neutral dressed-stone MATERIAL with a framed panel +
corner rune-studs (Create/Mekanism grammar), and a central EMISSIVE aspect socket
in the teal glint (Embers/Malum emissive-core idiom). Original pixels. The magic
reads as the accent, so the block sits beside Create without copying its brass.
Run from repo root:
  python3 gallery/2026-07-20-apparatus-proto/src/make_apparatus.py
"""
import pathlib
from PIL import Image
OUT = pathlib.Path("gallery/2026-07-20-apparatus-proto/out"); OUT.mkdir(parents=True, exist_ok=True)

def hx(v): return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)
# cool dressed arcane stone (Thaumcraft-grammar: blue-grey, tidy, subtle runes)
STONE = dict(mortar=hx(0x2A2E3B), shadow=hx(0x383E50), base=hx(0x474E62), hi=hx(0x5C6478))
AETH = dict(shadow=hx(0x5A4380), base=hx(0x8A6BB5), hi=hx(0xB99BE0))   # aetherium rune-studs
TEAL = hx(0x7FE8D8)                                                    # emissive aspect glint
TEAL_D = hx(0x3E9E92)

def face(top=False):
    im = Image.new("RGBA", (16, 16), STONE["base"]); px = im.load()
    # tidy stone speckle (clusters, not noise): a few 2px shadow/hi dabs
    for (x, y, c) in [(3, 4, STONE["shadow"]), (11, 3, STONE["hi"]), (4, 11, STONE["hi"]),
                      (12, 12, STONE["shadow"]), (8, 7, STONE["shadow"])]:
        px[x, y] = c; px[x+1, y] = c
    # framed panel: recessed border 2px in, beveled (hi top-left, shadow bottom-right)
    for i in range(2, 14):
        px[i, 2] = STONE["hi"]; px[2, i] = STONE["hi"]
        px[i, 13] = STONE["mortar"]; px[13, i] = STONE["mortar"]
    for i in range(3, 13):
        px[i, 3] = STONE["shadow"]; px[3, i] = STONE["shadow"]   # inner recess line
    # corner rune-studs (aetherium)
    for (cx, cy) in [(3, 3), (12, 3), (3, 12), (12, 12)]:
        px[cx, cy] = AETH["base"]; px[cx, cy] = AETH["hi"]
        # tiny 2x2 stud
        for dx in (0, 1):
            for dy in (0, 1):
                xx, yy = cx-(1 if cx > 8 else 0)+dx, cy-(1 if cy > 8 else 0)+dy
                px[xx, yy] = AETH["base"]
        px[cx-(1 if cx > 8 else 0), cy-(1 if cy > 8 else 0)] = AETH["hi"]
    # central socket: recessed diamond with an emissive teal aspect glint
    cx = cy = 8
    for (dx, dy) in [(0, -2), (0, 2), (-2, 0), (2, 0)]:
        px[cx+dx, cy+dy] = STONE["mortar"]
    for (dx, dy) in [(0, -1), (0, 1), (-1, 0), (1, 0), (0, 0)]:
        px[cx+dx, cy+dy] = TEAL_D
    px[cx, cy] = TEAL; px[cx, cy-1] = TEAL          # bright emissive core
    if top:   # top face: a rune ring instead of a socket, same frame
        for (dx, dy) in [(0, 0), (0, -1), (0, 1), (-1, 0), (1, 0)]:
            px[cx+dx, cy+dy] = STONE["base"]
        for (dx, dy) in [(-2, -2), (2, -2), (-2, 2), (2, 2)]:
            px[cx+dx, cy+dy] = AETH["base"]
        px[cx, cy] = TEAL
    return im

if __name__ == "__main__":
    face(top=False).save(OUT / "arcane_casing_side.png")
    face(top=True).save(OUT / "arcane_casing_top.png")
    print("wrote arcane_casing side+top ->", OUT)
