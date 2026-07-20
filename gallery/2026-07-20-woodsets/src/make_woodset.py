"""Generator (source of record) for greatwood + silverwood wood-set art that
needs NEW pixels: doors (top/bottom halves + item), trapdoors, crafting-table
faces. Everything else in the set (stairs/slab/fence/gate/button/pressure-plate)
reuses the existing plank texture via vanilla parent models — no new art (see the
mod-design-study wood-set synthesis: Framed/Macaw's/Supplementaries).

Wood ramps are the canonical plank ramps from styles/thaumaturgy.md; the iron
hardware ramp is a single SHARED accent, invariant across both woods (Macaw's
idiom). Run from repo root:
  python3 gallery/2026-07-20-woodsets/src/make_woodset.py
"""
import pathlib, random
from PIL import Image

OUT = pathlib.Path("gallery/2026-07-20-woodsets/out"); OUT.mkdir(parents=True, exist_ok=True)

def hx(v): return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)

# canonical plank ramps (styles/thaumaturgy.md) + a derived seam for silverwood
GREATWOOD = dict(seam=hx(0x30201C), shadow=hx(0x3E2C1F), base=hx(0x4F3B25), hi=hx(0x60492C))
SILVERWOOD = dict(seam=hx(0x8A8E82), shadow=hx(0xA8AC9D), base=hx(0xCFD3C4), hi=hx(0xE4E7DA))
# ONE shared iron hardware ramp (invariant across woods)
IRON = dict(dark=hx(0x2B2D33), shadow=hx(0x474A53), base=hx(0x6D7079), hi=hx(0x9297A1))

def _put(px, x, y, c):
    if 0 <= x < 16 and 0 <= y < 16:
        px[x, y] = c

def plank_field(ramp, seed, boards=(0, 6, 11), vertical=True):
    """16x16 plank field: grain as RUNS along the plank length (no lone flecks,
    per the wood-grain lesson) + seam lines between boards."""
    im = Image.new("RGBA", (16, 16), ramp["base"]); px = im.load()
    rnd = random.Random(seed)
    seams = [b - 1 for b in boards if b > 0]
    for cross in range(16):                               # each grain column
        if cross in seams:
            for long in range(16):
                x, y = (cross, long) if vertical else (long, cross)
                px[x, y] = ramp["seam"]
            continue
        long = 0
        while long < 16:
            r = rnd.random()
            tone = ramp["hi"] if r > 0.90 else ramp["shadow"] if r > 0.74 else ramp["base"]
            run = rnd.randint(3, 6) if tone is not ramp["base"] else rnd.randint(3, 7)
            for k in range(run):
                if long + k < 16:
                    x, y = (cross, long + k) if vertical else (long + k, cross)
                    px[x, y] = tone
            long += run
    return im

def bevel(im, ramp):
    px = im.load()
    for i in range(16):
        px[i, 0] = ramp["hi"]; px[0, i] = ramp["hi"]          # top/left catch light
        px[i, 15] = ramp["seam"]; px[15, i] = ramp["seam"]    # bottom/right shadow
    return im

def rrect(px, x0, y0, x1, y1, c):
    for x in range(x0, x1+1):
        for y in range(y0, y1+1):
            _put(px, x, y, c)

def hinge(px, y):                                             # iron hinge band on the left edge
    rrect(px, 0, y, 3, y+2, IRON["shadow"])
    rrect(px, 0, y, 3, y, IRON["hi"]); _put(px, 1, y+1, IRON["base"]); _put(px, 2, y+2, IRON["dark"])

def handle(px, cx, cy):                                       # round iron knob + backplate
    rrect(px, cx-1, cy-2, cx+1, cy+2, IRON["shadow"])
    rrect(px, cx-1, cy-1, cx, cy+1, IRON["base"]); _put(px, cx-1, cy-1, IRON["hi"])
    _put(px, cx+1, cy+2, IRON["dark"])

def door_half(ramp, half):
    im = bevel(plank_field(ramp, seed=1 if half == "bottom" else 2), ramp); px = im.load()
    if half == "bottom":
        hinge(px, 11); handle(px, 13, 3)                      # hinge low, handle by the split (top)
    else:
        hinge(px, 3); handle(px, 13, 12)                      # hinge high, handle by the split (bottom)
    return im

def trapdoor(ramp):
    im = bevel(plank_field(ramp, seed=3, boards=(0,), vertical=False), ramp); px = im.load()
    for y in (2, 13):                                         # two iron cross-bands
        rrect(px, 1, y, 14, y+1, IRON["shadow"]); rrect(px, 1, y, 14, y, IRON["base"])
        for bx in (2, 13):                                    # bolts
            _put(px, bx, y, IRON["hi"]); _put(px, bx, y+1, IRON["dark"])
    handle(px, 13, 7)
    return im

def door_item(ramp):
    """flat inventory sprite: a small standing door silhouette."""
    im = Image.new("RGBA", (16, 16), (0, 0, 0, 0)); px = im.load()
    for y in range(1, 15):
        for x in range(4, 12):
            r = (x*3 + y*7) % 10
            px[x, y] = ramp["hi"] if r > 8 else ramp["shadow"] if r > 6 else ramp["base"]
    for y in range(1, 15):                                    # frame
        px[4, y] = ramp["seam"]; px[11, y] = ramp["seam"]
    for x in range(4, 12):
        px[x, 1] = ramp["hi"]; px[x, 14] = ramp["seam"]
    handle(px, 10, 8)
    return im

def crafting_faces(ramp):
    """top (grid over planks), front (wood + saw/tool motif), side (planks)."""
    top = bevel(plank_field(ramp, seed=5, boards=(0, 8), vertical=False), ramp); tp = top.load()
    for i in range(1, 15):                                    # 3x3 grid lines
        for g in (5, 10):
            tp[g, i] = ramp["seam"]; tp[i, g] = ramp["seam"]
    front = bevel(plank_field(ramp, seed=6), ramp); fp = front.load()
    # a brass-free arcane worktable-adjacent tool motif: a saw-tooth band + a knob
    for x in range(3, 13):                                    # saw blade
        fp[x, 6] = IRON["base"]; fp[x, 7] = IRON["shadow"] if x % 2 else IRON["dark"]
    rrect(fp, 5, 8, 10, 9, ramp["seam"])                      # handle bar
    side = bevel(plank_field(ramp, seed=7), ramp)
    return top, front, side

WOODS = {"greatwood": GREATWOOD, "silverwood": SILVERWOOD}
if __name__ == "__main__":
    n = 0
    for name, ramp in WOODS.items():
        door_half(ramp, "bottom").save(OUT / f"{name}_door_bottom.png")
        door_half(ramp, "top").save(OUT / f"{name}_door_top.png")
        trapdoor(ramp).save(OUT / f"{name}_trapdoor.png")
        door_item(ramp).save(OUT / f"{name}_door.png")
        t, f, s = crafting_faces(ramp)
        t.save(OUT / f"{name}_crafting_table_top.png")
        f.save(OUT / f"{name}_crafting_table_front.png")
        s.save(OUT / f"{name}_crafting_table_side.png")
        n += 7
    print("wrote", n, "textures ->", OUT)
