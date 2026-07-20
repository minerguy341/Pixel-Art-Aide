"""Generator (source of record) for the 6 T.N.A. primal aspect icon mockups.
64x64 HD hexagonal GUI icons. Builds BOTH a 'frame' and a 'backdrop' treatment
for each primal so we can compare and decide. Colours are the canonical aspect
codes from docs/aspects.md; symbol legibility is enforced by adaptive value
contrast + a selout keyline (see knowledge/shading.md, lessons.md).
Run from repo root:
  python3 gallery/2026-07-20-aspect-primals/src/make_aspects.py
"""
import colorsys, math, pathlib
from PIL import Image, ImageDraw

OUT = pathlib.Path("gallery/2026-07-20-aspect-primals/out")
OUT.mkdir(parents=True, exist_ok=True)
N = 64
CX = CY = 31.5
R = 30.0  # hexagon circumradius

# --- 6 primals: name, concept color, symbol key ---
PRIMALS = [
    ("ventus",    "#CDE8F5", "swirl"),
    ("tellus",    "#6BA84F", "mountain"),
    ("flamma",    "#F0552B", "flame"),
    ("unda",      "#3D9BE0", "wave"),
    ("forma",     "#EDE9DC", "grid"),
    ("discordia", "#4A3459", "burst"),
]

def hx(s):
    s = s.lstrip("#"); return tuple(int(s[i:i+2], 16) for i in (0, 2, 4))
def hsv(h, s, v):
    r, g, b = colorsys.hsv_to_rgb(h, max(0, min(1, s)), max(0, min(1, v)))
    return (int(r*255), int(g*255), int(b*255))
def to_hsv(c):
    return colorsys.rgb_to_hsv(c[0]/255, c[1]/255, c[2]/255)
def lum(c):
    return 0.299*c[0] + 0.587*c[1] + 0.114*c[2]

def ramp(code):
    """derive a small ramp from an aspect code (hue-shifted, per shading.md)."""
    h, s, v = to_hsv(hx(code))
    # shadows cool-shift slightly, highlights warm/desaturate
    return {
        "deep":   hsv((h-0.02) % 1, min(1, s*1.18), max(0.06, v*0.34)),
        "shadow": hsv((h-0.01) % 1, min(1, s*1.10), max(0.10, v*0.60)),
        "base":   hx(code),
        "hi":     hsv((h+0.01) % 1, s*0.72, min(1.0, v*1.10)),
        "light":  hsv((h+0.02) % 1, s*0.30, min(1.0, v*1.06 + 0.10)),
    }

def hexagon(cx, cy, r, pointy=True):
    pts = []
    for k in range(6):
        a = math.radians(60*k + (90 if pointy else 60))
        pts.append((cx + r*math.cos(a), cy - r*math.sin(a)))
    return pts

def scale_about(pts, k, cx=CX, cy=CY):
    return [(cx + (x-cx)*k, cy + (y-cy)*k) for x, y in pts]

# ---------- symbol drawing (returns nothing; draws on d) ----------
def _stroke(d, pts, w, fill, key):
    d.line(pts, fill=key, width=w+3, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0]-(w+3)/2, p[1]-(w+3)/2, p[0]+(w+3)/2, p[1]+(w+3)/2], fill=key)
    d.line(pts, fill=fill, width=w, joint="curve")
    for p in (pts[0], pts[-1]):
        d.ellipse([p[0]-w/2, p[1]-w/2, p[0]+w/2, p[1]+w/2], fill=fill)

def _poly(d, pts, fill, key, keyw=0.80):
    d.polygon(pts, fill=key)
    d.polygon(scale_about(pts, keyw), fill=fill)

def sym_swirl(d, fill, key):
    # three flowing wind gusts, each ending in an upward curl (breeze glyph)
    def gust(y, x0, x1):
        pts = []
        for x in range(x0, x1 + 1, 2):
            pts.append((x, y + 2.4*math.sin((x - x0) / 6.5)))
        cx, cy = pts[-1]                      # curl the tail into a loop
        for a in range(0, 250, 18):
            ang = math.radians(a)
            pts.append((cx + 5.5*math.sin(ang), cy - (5.5 - 5.5*math.cos(ang))))
        _stroke(d, pts, 4, fill, key)
    gust(23, 14, 39)
    gust(33, 12, 47)
    gust(43, 17, 38)

def sym_mountain(d, fill, key):
    base_y = 46
    pts = [(14, base_y), (27, 22), (34, 32), (40, 24), (50, base_y)]
    _poly(d, pts, fill, key, 0.86)
    # snow/strata notch: a horizon line
    _stroke(d, [(16, base_y-1), (48, base_y-1)], 3, fill, key)

def sym_flame(d, fill, key, core=None):
    # asymmetric flame: rounded base, main tongue + a side lick; inner tongue
    outer = [(31, 12), (35, 19), (40, 22), (42, 30), (41, 38), (38, 44),
             (40, 47), (33, 50), (25, 49), (21, 42), (23, 34), (27, 37),
             (26, 28), (31, 31), (30, 21)]
    _poly(d, outer, fill, key, 0.84)
    # inner tongue — a hot core if given, else the dark keyline for depth
    inner = [(32, 27), (37, 34), (35, 43), (31, 47), (27, 42), (29, 34)]
    if core is not None:
        d.polygon(inner, fill=key)                 # thin dark rim
        d.polygon(scale_about(inner, 0.78, 31, 38), fill=core)
    else:
        d.polygon(inner, fill=key)

def sym_wave(d, fill, key):
    for oy in (-6, 6):
        pts = []
        for x in range(14, 51, 3):
            pts.append((x, CY + oy + 6*math.sin((x-14)/6.0)))
        _stroke(d, pts, 4, fill, key)

def sym_grid(d, fill, key):
    a, b = 17, 47
    _poly(d, [(a, a), (b, a), (b, b), (a, b)], fill, key, 0.72)
    mid = (a+b)//2
    _stroke(d, [(mid, a+3), (mid, b-3)], 3, fill, key)
    _stroke(d, [(a+3, mid), (b-3, mid)], 3, fill, key)

def sym_burst(d, fill, key):
    # asymmetric jagged shatter star
    spikes = [(32,12,10),(41,20,4),(48,30,9),(40,38,4),(45,48,8),
              (33,44,4),(22,50,9),(26,38,4),(15,33,9),(25,24,4),(20,16,7)]
    pts = [(x, y) for x, y, _ in spikes]
    _poly(d, pts, fill, key, 0.62)

SYMS = {"swirl": sym_swirl, "mountain": sym_mountain, "flame": sym_flame,
        "wave": sym_wave, "grid": sym_grid, "burst": sym_burst}

# ---------- treatments ----------
def _hex_shade(im, d, rp, light_top=True):
    """fill hexagon with a soft top-lit ramp bed."""
    hexpts = hexagon(CX, CY, R)
    # base fill
    d.polygon(hexpts, fill=rp["base"])
    # vertical shade: lighter top third, darker bottom third
    px = im.load()
    hi, sh, base = rp["hi"], rp["shadow"], rp["base"]
    mask = Image.new("L", (N, N), 0)
    md = ImageDraw.Draw(mask); md.polygon(hexpts, fill=255)
    mp = mask.load()
    for y in range(N):
        t = (y - 6) / (N - 12)  # 0 top -> 1 bottom
        for x in range(N):
            if mp[x, y] == 0:
                continue
            if t < 0.34:
                k = (0.34 - t) / 0.34 * 0.55
                px[x, y] = tuple(int(base[i] + (hi[i]-base[i])*k) for i in range(3)) + (255,)
            elif t > 0.66:
                k = (t - 0.66) / 0.34 * 0.6
                px[x, y] = tuple(int(base[i] + (sh[i]-base[i])*k) for i in range(3)) + (255,)

def _hex_outline(d, rp, col, w=3):
    hexpts = hexagon(CX, CY, R)
    d.line(hexpts + [hexpts[0]], fill=col, width=w, joint="curve")

def make_backdrop(code, symkey):
    rp = ramp(code)
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    _hex_shade(im, d, rp)
    _hex_outline(d, rp, rp["deep"], 3)           # dark rim for definition
    _hex_outline(d, {}, rp["hi"], 1) if False else None
    # adaptive symbol contrast — pinned to true near-white / near-black by
    # luminance so even extreme aspect codes (Forma light, Discordia dark) read
    h, s, v = to_hsv(hx(code))
    sym_light = hsv(h, 0.20, 0.95)   # near-white, faint aspect tint
    sym_dark  = hsv(h, min(1, s*1.1), 0.16)
    bed = lum(rp["base"])
    if bed > 150:   # light bed -> dark symbol, light keyline
        fill, key = sym_dark, sym_light
    else:           # dark/mid bed -> light symbol, dark keyline
        fill, key = sym_light, sym_dark
    if symkey == "flame":
        SYMS[symkey](d, fill, sym_dark, core=hsv(0.11, 0.88, 1.0))  # white-hot body, amber core
    else:
        SYMS[symkey](d, fill, key)
    return im

def make_frame(code, symkey):
    rp = ramp(code)
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    hexpts = hexagon(CX, CY, R)
    # dark neutral interior (aspect-tinted near-black)
    h, s, v = to_hsv(hx(code))
    interior = hsv(h, min(1, s*0.6), 0.14)
    d.polygon(hexpts, fill=interior + (255,))
    # bevelled ring: highlight top-left, shadow bottom-right, base ring between
    d.line(hexpts + [hexpts[0]], fill=rp["shadow"], width=6, joint="curve")
    d.line(scale_about(hexpts, 0.995) + [scale_about(hexpts, 0.995)[0]], fill=rp["base"], width=4, joint="curve")
    # top-left highlight arc (first 3 edges)
    tl = hexpts[1:4]
    d.line(tl, fill=rp["hi"], width=2, joint="curve")
    d.line(hexpts + [hexpts[0]], fill=rp["deep"], width=1, joint="curve")
    # symbol in bright aspect tint on the dark interior
    fill, key = rp["hi"], (0, 0, 0)
    # if aspect is very light, hi still bright -> fine on dark interior
    if symkey == "flame":
        SYMS[symkey](d, fill, rp["deep"], core=hsv(0.11, 0.88, 1.0))
    else:
        SYMS[symkey](d, fill, rp["deep"])
    return im

if __name__ == "__main__":
    for name, code, symkey in PRIMALS:
        make_backdrop(code, symkey).save(OUT / f"{name}_backdrop.png")
        make_frame(code, symkey).save(OUT / f"{name}_frame.png")
    print("wrote 12 icons ->", OUT)
