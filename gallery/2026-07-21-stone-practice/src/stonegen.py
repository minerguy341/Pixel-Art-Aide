#!/usr/bin/env python3
"""Data-driven stone generator. All tunable values live in `stones.json`; this file is the fixed
engine. Tweak stones by editing the JSON, or override any value on the CLI without touching code:

  python3 stonegen.py                       # render every stone in stones.json
  python3 stonegen.py --only marble,granite # subset
  python3 stonegen.py --set shale.laminae.density=0.4 --set marble.seed=7
  python3 stonegen.py --specs other.json    # a different spec file

Spec schema (per stone): ramp=[shadow,base,highlight] hex; structure=speckle|foliation|flat;
busy_lo/busy_hi (speckle/foliation thresholds); optional minerals[], veins[], laminae/bedding
(rows,color,density,wavy), flecks[]/pits[] (x,y,color), cleavage (rows,color,density), desc.
"""
import argparse
import json
import math
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SESS = HERE.parent
sys.path.insert(0, str(SESS.parent.parent))
import make_stones as MS  # noqa: E402  (reuse blank/h2/row/sheet/tile3/render helpers)

N, h2, blank = MS.N, MS.h2, MS.blank


def hexc(s):
    s = str(s).lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16), 255)


def lerp(c1, c2, t):
    return (int(c1[0] + (c2[0] - c1[0]) * t), int(c1[1] + (c2[1] - c1[1]) * t),
            int(c1[2] + (c2[2] - c1[2]) * t), 255)


# ---------------------------------------------------------------- structure primitives (value-driven)
def fill_base(px, spec):
    ramp = [hexc(c) for c in spec["ramp"]]
    struct = spec.get("structure", "speckle")
    seed = spec.get("seed", 1)
    lo = spec.get("busy_lo", 0.14)
    hi = spec.get("busy_hi", 0.12)
    for y in range(N):
        for x in range(N):
            if struct == "flat":
                g = 0.5
            elif struct == "foliation":
                g = 0.6 * h2(x // 2, y, seed) + 0.4 * h2(x, y, seed + 1)   # horizontally-biased grain
            else:                                                          # speckle
                g = h2(x, y, seed)
            px[x, y] = ramp[0] if g < lo else (ramp[2] if g > 1 - hi else ramp[1])


def apply_minerals(px, spec):
    seed = spec.get("seed", 1)
    minerals = [(hexc(m["color"]), m["p"]) for m in spec.get("minerals", [])]
    for y in range(N):
        for x in range(N):
            g = h2(x, y, seed + 5)
            acc = 0.0
            for color, p in minerals:
                acc += p
                if g < acc:
                    px[x, y] = color
                    break


def apply_bands(px, spec, key):
    b = spec.get(key)
    if not b:
        return
    color = hexc(b["color"])
    dens = b.get("density", 0.6)
    wavy = b.get("wavy", False)
    seed = spec.get("seed", 1)
    for ly in b["rows"]:
        for x in range(N):
            yy = (ly + (1 if (wavy and h2(x // 3, ly, seed + 7) < 0.3) else 0)) % N
            if h2(x, ly, seed + 8) < dens:
                px[x, yy] = color


def apply_veins(px, spec):
    for i, v in enumerate(spec.get("veins", [])):
        color, core = hexc(v["color"]), hexc(v["core"])
        bx, amp, slp = v["base_x"], v.get("amp", 2.2), v.get("slope", 1)
        sd = spec.get("seed", 1) + 20 + i
        for y in range(N):
            cx = int(round(bx + slp * y + amp * math.sin(y / 8 * 2 * math.pi))) % N
            px[cx, y] = core
            if h2(cx, y, sd) < 0.5:
                px[(cx + 1) % N, y] = color


def _anchor(name, crossings):
    """'T0' -> top edge at crossings[0], etc. Crossings must be a symmetric set (a+b=N-1) and are
    identical on all four edges, so 90-degree rotations map edge-crossings onto edge-crossings."""
    edge, idx = name[0], int(name[1])
    c = crossings[idx]
    return {"T": (c, 0), "B": (c, N - 1), "L": (0, c), "R": (N - 1, c)}[edge]


def apply_anchor_veins(px, spec):
    """Veins routed between edge anchors, wandering in the interior but pinned to the SAME crossing
    positions on every edge — so the lines line up across seams under any 90-degree rotation."""
    av = spec.get("anchor_veins")
    if not av:
        return
    crossings = av["crossings"]
    core = hexc(av["core"])                             # darkest end of the vein
    soft = hexc(av.get("soft", av.get("color", av["core"])))  # lightest end (close to base)
    amp = av.get("amp", 2.0)
    dot = av.get("dot", 1.0)                            # fraction of interior steps drawn (rest = gaps)
    bias = av.get("dark_bias", 1.7)                     # >1 keeps most pixels light, few dark
    seed = spec.get("seed", 1) + 30
    for pi, (a, b) in enumerate(av["pairs"]):
        ax, ay = _anchor(a, crossings)
        bx, by = _anchor(b, crossings)
        dx, dy = bx - ax, by - ay
        length = math.hypot(dx, dy) or 1.0
        pxu, pyu = -dy / length, dx / length            # perpendicular unit
        # per-vein curve: sum of sin harmonics (all zero at f=0,1 → endpoints stay pinned), random
        # amplitudes+signs per vein so no two veins share a shape and none read as a straight line.
        c1 = 0.7 + 0.6 * h2(pi, 1, seed)
        c2 = 1.4 * (h2(pi, 2, seed) - 0.5)
        c3 = 0.9 * (h2(pi, 3, seed) - 0.5)
        steps = (int(length) + 1) * 3
        for t in range(steps + 1):
            f = t / steps
            sh = c1 * math.sin(f * math.pi) + c2 * math.sin(2 * f * math.pi) + c3 * math.sin(3 * f * math.pi)
            jit = 0.4 * (h2(pi, t, seed + 9) - 0.5) * math.sin(f * math.pi)   # pixel wiggle, 0 at ends
            wob = amp * (sh + jit)
            xi = int(round(ax + dx * f + pxu * wob)) % N
            yi = int(round(ay + dy * f + pyu * wob)) % N
            if 0 < f < 1 and h2(xi, yi, seed + 3) > dot:
                continue                                # dotted gap — let the stone show through
            d = h2(xi, yi, seed + 4) ** bias            # RANDOM darkness per pixel (no uniform stroke)
            px[xi, yi] = lerp(soft, core, d)
            if 0 < f < 1 and h2(xi, yi, seed + 1) < 0.18:
                d2 = (h2(xi, yi, seed + 5) ** bias) * 0.5
                px[(xi + 1) % N, yi] = lerp(soft, core, d2)  # lighter feather
    for a, b in av["pairs"]:                             # pin edge crossings (mid tone → reads as a link)
        for nm in (a, b):
            cx, cy = _anchor(nm, crossings)
            px[cx, cy] = lerp(soft, core, 0.5)


def apply_points(px, spec, key):
    for p in spec.get(key, []):
        px[p["x"] % N, p["y"] % N] = hexc(p["color"])


def apply_cleavage(px, spec):
    cl = spec.get("cleavage")
    if not cl:
        return
    for y in cl["rows"]:
        for x in range(N):
            if h2(x, y, spec.get("seed", 1) + 9) < cl.get("density", 0.4):
                px[x, y] = hexc(cl["color"])


def render(spec):
    im, px = blank()
    fill_base(px, spec)
    apply_bands(px, spec, "laminae")
    apply_bands(px, spec, "bedding")
    apply_minerals(px, spec)
    apply_veins(px, spec)
    apply_anchor_veins(px, spec)
    apply_points(px, spec, "flecks")
    apply_points(px, spec, "pits")
    apply_cleavage(px, spec)
    return im


# ---------------------------------------------------------------- CLI value overrides
def set_path(specs, path, raw):
    keys = path.split(".")
    d = specs
    for k in keys[:-1]:
        d = d[int(k)] if isinstance(d, list) else d[k]
    try:
        val = int(raw)
    except ValueError:
        try:
            val = float(raw)
        except ValueError:
            val = raw
    last = keys[-1]
    if isinstance(d, list):
        d[int(last)] = val
    else:
        d[last] = val


from PIL import Image, ImageDraw  # noqa: E402
# full dihedral group D4: 4 rotations + 4 flips (all preserve a symmetric crossing set)
_ROT = [None, Image.ROTATE_90, Image.ROTATE_180, Image.ROTATE_270]
_D4 = _ROT + [Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.TRANSPOSE, Image.TRANSVERSE]
_AXIS = [None, Image.FLIP_LEFT_RIGHT, Image.FLIP_TOP_BOTTOM, Image.ROTATE_180]  # keep axes, no 90 turn
_HFLIP = [None, Image.FLIP_LEFT_RIGHT]                                          # keep the vertical look

# orientation-variety op sets by texture directionality (see shading.md)
ORIENT = {
    "d4": [("random rotation (4-way)", _ROT), ("rotation + flip (8-way)", _D4)],
    "rot4": [("random rotation (4-way)", _ROT)],
    "axis": [("h/v flip + 180 (keeps both axes)", _AXIS)],
    "hflip": [("horizontal flip only (keeps vertical look)", _HFLIP)],
}


def rot_wall(tex, ops, side=5, scale=4):
    canvas = Image.new("RGBA", (N * side, N * side), MS.T)
    for by in range(side):
        for bx in range(side):
            t = tex
            if len(ops) > 1:
                op = ops[int(h2(bx, by, 777) * len(ops)) % len(ops)]  # deterministic per-cell
                if op is not None:
                    t = tex.transpose(op)
            canvas.alpha_composite(t, (bx * N, by * N))
    return canvas.resize((canvas.width * scale, canvas.height * scale), Image.NEAREST)


def rotwall_sheet(name, tex, orient="d4"):
    cols = [(rot_wall(tex, [None]), "fixed")]
    for label, ops in ORIENT.get(orient, ORIENT["d4"]):
        cols.append((rot_wall(tex, ops), label))
    imgs = [MS.lbl(im, lab) for im, lab in cols]
    gap, pad = 22, 16
    w = sum(i.width for i in imgs) + gap * (len(imgs) - 1) + 2 * pad
    ht = max(i.height for i in imgs) + 2 * pad + 24
    canvas = Image.new("RGBA", (w, ht), MS.BG)
    ImageDraw.Draw(canvas).text((pad, 8), f"{name} — orientation variety (op matched to directionality)", fill=MS.INK)
    x = pad
    for im in imgs:
        canvas.alpha_composite(im, (x, 30))
        x += im.width + gap
    out = MS.PREV / f"sheet-{name}-rot.png"
    canvas.save(out)
    print("wrote", out.name)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--specs", default=str(SESS / "stones.json"))
    ap.add_argument("--only", default="")
    ap.add_argument("--set", dest="sets", action="append", default=[])
    ap.add_argument("--suffix", default="_gen")
    ap.add_argument("--rotwall", default="", help="also emit a fixed-vs-random-rotated wall for this stone")
    args = ap.parse_args()

    specs = json.load(open(args.specs))
    for s in args.sets:
        path, _, raw = s.partition("=")
        set_path(specs, path.strip(), raw.strip())

    if args.rotwall:
        sp = specs[args.rotwall]
        rotwall_sheet(args.rotwall, render(sp), sp.get("orient", "d4"))

    names = [n.strip() for n in args.only.split(",") if n.strip()] or list(specs)
    rows = []
    for name in names:
        spec = specs[name]
        img = render(spec)
        (MS.SRC / f"{name}{args.suffix}.pxg").write_text(MS.G.to_text(MS.G.from_image(img)))
        MS.G.save_texture(img, MS.OUT / f"{name}{args.suffix}.png")
        rows.append(MS.row(img, f"{name} - {spec.get('desc', '')}"))
    MS.sheet("STONES (data-driven from stones.json — tweak values, not code)",
             rows, MS.PREV / "sheet-stones-gen.png")
    print("rendered:", ", ".join(names))


if __name__ == "__main__":
    main()
