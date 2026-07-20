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
    ("discordia", "#4A3459", "chaosstar"),
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
    # centred range: a dominant central peak + a lower left shoulder, vertically
    # balanced about the hexagon centre (bbox ~y19..44)
    base_y = 44
    pts = [(14, base_y), (22, 33), (27, 37), (32, 19), (41, 33), (50, base_y)]
    _poly(d, pts, fill, key, 0.86)
    _stroke(d, [(16, base_y-1), (48, base_y-1)], 3, fill, key)  # horizon

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

def _stroke_sharp(d, pts, w, fill, key):
    """stroke with no ball end-caps — for angular cracks."""
    d.line(pts, fill=key, width=w+2, joint="curve")
    d.line(pts, fill=fill, width=w, joint="curve")

def sym_crack(d, fill, key):
    # shattered-glass fracture: radial cracks from an off-centre impact + a web
    ip = (33, 27)
    radials = [[(32, 20), (30, 13)], [(40, 25), (46, 21)], [(41, 33), (48, 38)],
               [(34, 40), (35, 50)], [(26, 37), (18, 43)], [(25, 27), (14, 25)]]
    for r in radials:
        _stroke_sharp(d, [ip, r[0], r[1]], 3, fill, key)
    web = [[(32, 20), (25, 27)], [(40, 25), (41, 33)],
           [(41, 33), (34, 40)], [(26, 37), (25, 27)]]
    for wseg in web:
        _stroke_sharp(d, wseg, 2, fill, key)

def sym_shards(d, fill, key):
    # a form broken into separated shards (gaps = flying apart)
    shards = [
        [(32, 12), (41, 25), (24, 25)],            # top
        [(45, 29), (39, 45), (32, 33)],            # right
        [(20, 30), (31, 36), (22, 49)],            # lower-left
        [(35, 40), (30, 51), (26, 42)],            # small bottom bit
    ]
    for s in shards:
        _poly(d, s, fill, key, 0.72)

def sym_scatter(d, fill, key):
    # order -> disorder: a solid block dissolving into scattered squares (entropy)
    _poly(d, [(15, 21), (27, 21), (27, 43), (15, 43)], fill, key, 0.80)
    bits = [(30, 24, 5), (34, 31, 5), (31, 39, 4), (37, 26, 4), (39, 35, 4),
            (36, 43, 3), (43, 29, 4), (46, 38, 3), (44, 23, 3), (48, 32, 3)]
    for x, y, s in bits:
        d.rectangle([x, y, x+s, y+s], fill=key)
        d.rectangle([x+1, y+1, x+s-1, y+s-1], fill=fill)

def _arrow2(d, cx, cy, ang, r0, r1, fill, key, hl=6, hw=4.2):
    """clean arrow: straight shaft r0->r1 + a filled triangle head."""
    dx, dy = math.cos(ang), -math.sin(ang)
    px, py = -dy, dx                       # perpendicular
    sx, sy = cx + r0*dx, cy + r0*dy        # shaft start (hub gap)
    bx, by = cx + r1*dx, cy + r1*dy        # head base centre
    _stroke_sharp(d, [(sx, sy), (bx, by)], 3, fill, key)
    tip = (cx + (r1+hl)*dx, cy + (r1+hl)*dy)
    c1 = (bx + hw*px, by + hw*py)
    c2 = (bx - hw*px, by - hw*py)
    d.polygon([tip, c1, c2], fill=key)
    d.polygon(scale_about([tip, c1, c2], 0.6, bx, by), fill=fill)

def sym_chaosstar(d, fill, key):
    # 8 arrows, evenly spaced; the chaos is in the UNEVEN lengths, not the crowding
    lens = [18, 13, 17, 12, 18, 14, 16, 12]
    for i in range(8):
        _arrow2(d, 32, 31, math.radians(i*45 + 8), 6.5, lens[i], fill, key)
    # clean central hub so shafts read as radiating, not a blob
    hub = [(32, 25.5), (37.5, 31), (32, 36.5), (26.5, 31)]
    d.polygon(hub, fill=key)
    d.polygon(scale_about(hub, 0.6, 32, 31), fill=fill)

def sym_vortex(d, fill, key):
    # a two-armed turbulent spiral (whirl/vortex)
    for arm in (0.0, math.pi):
        pts = []
        for t in range(0, 210, 9):
            a = math.radians(t) + arm
            rr = 2.2 + t*0.077
            pts.append((32 + rr*math.cos(a), 31 - rr*math.sin(a)))
        _stroke(d, pts, 4, fill, key)

def _ellipse_pts(cx, cy, rx, ry, rot, steps=44):
    r = math.radians(rot); out = []
    for i in range(steps+1):
        a = 2*math.pi*i/steps
        x, y = rx*math.cos(a), ry*math.sin(a)
        out.append((cx + x*math.cos(r) - y*math.sin(r), cy + x*math.sin(r) + y*math.cos(r)))
    return out

def sym_butterfly(d, fill, key):
    # Lorenz-attractor butterfly: two overlapping tilted loops (symbol of chaos)
    _stroke(d, _ellipse_pts(27, 31, 8.5, 15, 24), 3, fill, key)
    _stroke(d, _ellipse_pts(37, 31, 8.5, 15, -24), 3, fill, key)

def sym_hourglass(d, fill, key):
    # entropy / order<->chaos: hourglass, top full, sand dispersing out the base
    frame = [(19, 14), (45, 14), (33, 31), (45, 48), (19, 48), (31, 31)]
    _stroke_sharp(d, frame + [frame[0]], 3, fill, key)
    _poly(d, [(23, 17), (41, 17), (32, 29)], fill, key, 0.9)     # sand in the top
    for x, y, s in [(31, 40, 3), (34, 44, 2), (29, 45, 2), (37, 47, 2),
                    (26, 48, 2), (40, 44, 2), (24, 43, 2)]:       # dispersing grains
        d.rectangle([x, y, x+s, y+s], fill=key)
        d.rectangle([x, y, x+s-1, y+s-1], fill=fill)

SYMS = {"swirl": sym_swirl, "mountain": sym_mountain, "flame": sym_flame,
        "wave": sym_wave, "grid": sym_grid, "burst": sym_burst,
        "crack": sym_crack, "shards": sym_shards, "scatter": sym_scatter,
        "chaosstar": sym_chaosstar, "vortex": sym_vortex,
        "butterfly": sym_butterfly, "hourglass": sym_hourglass}

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

def backdrop_canvas(code):
    """the shared filled-hexagon bed + adaptive symbol colours (fill, key).
    Symbol colours are pinned to near-white / near-black by the bed's luminance
    so even extreme aspect codes (Forma light, Discordia dark) stay legible."""
    rp = ramp(code)
    im = Image.new("RGBA", (N, N), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    _hex_shade(im, d, rp)
    _hex_outline(d, rp, rp["deep"], 3)           # dark rim for definition
    h, s, v = to_hsv(hx(code))
    sym_light = hsv(h, 0.20, 0.95)
    sym_dark  = hsv(h, min(1, s*1.1), 0.16)
    bed = lum(rp["base"])
    fill, key = (sym_dark, sym_light) if bed > 150 else (sym_light, sym_dark)
    return im, d, fill, key

def make_backdrop(code, symkey):
    im, d, fill, key = backdrop_canvas(code)
    if symkey == "flame":
        SYMS[symkey](d, fill, key, core=hsv(0.11, 0.88, 1.0))  # white-hot body, amber core
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
