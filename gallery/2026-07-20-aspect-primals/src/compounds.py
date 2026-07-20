"""Symbol candidates for compound aspects — 5 per aspect, filled-backdrop only.
Reuses the primal backdrop machinery (make_aspects.backdrop_canvas) so treatment
+ adaptive value contrast are identical. Colours are the canonical codes from
docs/aspects.md. Run via previews/compound_sheets.py.
"""
import math, sys
sys.path.insert(0, "gallery/2026-07-20-aspect-primals/src")
from make_aspects import (backdrop_canvas, _poly, _stroke, _stroke_sharp,
                          scale_about, N)

CX = CY = 31.5

# ---- shared little helpers ----
def star_pts(cx, cy, n, ro, ri, rot=0.0):
    pts = []
    for i in range(2*n):
        r = ro if i % 2 == 0 else ri
        a = math.pi*i/n + rot
        pts.append((cx + r*math.cos(a), cy - r*math.sin(a)))
    return pts

def disc(d, cx, cy, r, fill, key):
    d.ellipse([cx-r-1, cy-r-1, cx+r+1, cy+r+1], fill=key)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], fill=fill)

def ring(d, cx, cy, r, w, fill, key):
    d.ellipse([cx-r-1, cy-r-1, cx+r+1, cy+r+1], outline=key, width=w+2)
    d.ellipse([cx-r, cy-r, cx+r, cy+r], outline=fill, width=w)

def spark(d, cx, cy, r, fill, key):
    _poly(d, star_pts(cx, cy, 4, r, r*0.34), fill, key, 0.5)

# ===================== LUMEN — light (#FFE066) =====================
def lum_sun(d, f, k):
    for i in range(8):
        a = math.radians(i*45)
        dx, dy = math.cos(a), -math.sin(a); px, py = -dy, dx
        b = (CX+13*dx, CY+13*dy); tip = (CX+21*dx, CY+21*dy)
        c1 = (b[0]+3.4*px, b[1]+3.4*py); c2 = (b[0]-3.4*px, b[1]-3.4*py)
        d.polygon([tip, c1, c2], fill=k); d.polygon(scale_about([tip, c1, c2], 0.6, *b), fill=f)
    disc(d, CX, CY, 9, f, k)

def lum_sparkle(d, f, k):
    _poly(d, star_pts(CX, CY, 4, 19, 5.5), f, k, 0.5)
    spark(d, 47, 17, 4.5, f, k); spark(d, 19, 44, 3.5, f, k)

def lum_starburst(d, f, k):
    for i in range(12):
        a = math.radians(i*30)
        r1 = 19 if i % 2 == 0 else 13
        _stroke_sharp(d, [(CX+4*math.cos(a), CY-4*math.sin(a)),
                          (CX+r1*math.cos(a), CY-r1*math.sin(a))], 2, f, k)
    disc(d, CX, CY, 4, f, k)

def lum_dawn(d, f, k):
    hy = 41
    _stroke_sharp(d, [(12, hy), (52, hy)], 3, f, k)               # horizon
    d.pieslice([CX-12, hy-12, CX+12, hy+12], 180, 360, fill=k)    # rising sun
    d.pieslice([CX-11, hy-11, CX+11, hy+11], 180, 360, fill=f)
    for deg in (26, 60, 90, 120, 154):                            # rays fanning up
        a = math.radians(deg)
        _stroke_sharp(d, [(CX+13*math.cos(a), hy-13*math.sin(a)),
                          (CX+20*math.cos(a), hy-20*math.sin(a))], 2, f, k)

def lum_orb(d, f, k):
    disc(d, CX, CY, 8, f, k)
    ring(d, CX, CY, 13, 2, f, k); ring(d, CX, CY, 18, 2, f, k)

# ===================== VITA — life (#C43C55) =====================
def vit_heart(d, f, k):
    pts = [(32, 22), (28, 17), (22, 17), (18, 23), (19, 29),
           (32, 45), (45, 29), (46, 23), (42, 17), (36, 17)]
    _poly(d, pts, f, k, 0.82)

def vit_pulse(d, f, k):
    _stroke(d, [(13, 32), (23, 32), (27, 22), (32, 42), (37, 26), (41, 32), (51, 32)], 3, f, k)

def vit_sprout(d, f, k):
    _stroke(d, [(32, 46), (32, 26)], 3, f, k)                     # stem
    _poly(d, [(32, 30), (22, 24), (24, 33)], f, k, 0.7)           # left leaf
    _poly(d, [(32, 27), (43, 20), (41, 30)], f, k, 0.7)           # right leaf

def vit_seed(d, f, k):
    _poly(d, [(32, 46), (39, 36), (37, 27), (32, 23), (27, 27), (25, 36)], f, k, 0.82)  # seed
    _stroke(d, [(32, 24), (33, 17), (38, 14)], 3, f, k)           # sprout curl

def vit_spiral(d, f, k):
    pts = []                                                      # fiddlehead / unfurling life
    for t in range(0, 340, 12):
        a = math.radians(t); rr = 2 + t*0.045
        pts.append((CX + rr*math.cos(a), CY - rr*math.sin(a)))
    _stroke(d, pts, 4, f, k)
    _poly(d, [(pts[-1][0], pts[-1][1]-1), (pts[-1][0]+9, pts[-1][1]-6),
              (pts[-1][0]+7, pts[-1][1]+3)], f, k, 0.7)           # leaf at the tip

# ===================== ARCANUM — magic (#DD4FD0) =====================
def arc_rune(d, f, k):
    _stroke_sharp(d, [(32, 13), (32, 49)], 3, f, k)               # spine
    _stroke_sharp(d, [(32, 22), (43, 16)], 3, f, k)
    _stroke_sharp(d, [(32, 32), (21, 26)], 3, f, k)
    _stroke_sharp(d, [(32, 40), (42, 45)], 3, f, k)
    disc(d, 32, 13, 3, f, k); disc(d, 21, 26, 2.5, f, k)

def arc_sparkstar(d, f, k):
    _poly(d, star_pts(CX, CY, 4, 15, 4.5), f, k, 0.5)
    for a in (30, 150, 270):
        r = 21; spark(d, CX+r*math.cos(math.radians(a)), CY-r*math.sin(math.radians(a)), 2.6, f, k)

def arc_ring(d, f, k):
    ring(d, CX, CY, 14, 2, f, k)
    for a in (90, 210, 330):
        spark(d, CX+14*math.cos(math.radians(a)), CY-14*math.sin(math.radians(a)), 4, f, k)
    disc(d, CX, CY, 3, f, k)

def arc_wand(d, f, k):
    _stroke(d, [(21, 45), (39, 21)], 4, f, k)                     # wand
    _poly(d, star_pts(41, 18, 4, 7, 2.4), f, k, 0.5)             # star tip
    spark(d, 27, 26, 2.4, f, k)

def arc_swirl(d, f, k):
    pts = []
    for t in range(0, 300, 12):
        a = math.radians(t); rr = 2 + t*0.055
        pts.append((CX + rr*math.cos(a), CY - rr*math.sin(a)))
    _stroke(d, pts, 4, f, k)
    spark(d, 46, 24, 3, f, k); spark(d, 20, 40, 2.6, f, k)

ASPECTS = {
    "Lumen":   ("#FFE066", "light", [
        ("sun", "sun disc + rays", lum_sun),
        ("sparkle", "4-point sparkle", lum_sparkle),
        ("starburst", "radiant burst", lum_starburst),
        ("dawn", "sun over horizon", lum_dawn),
        ("orb", "haloed orb", lum_orb)]),
    "Vita":    ("#C43C55", "life", [
        ("heart", "heart", vit_heart),
        ("pulse", "heartbeat", vit_pulse),
        ("sprout", "seedling", vit_sprout),
        ("seed", "sprouting seed", vit_seed),
        ("spiral", "unfurling frond", vit_spiral)]),
    "Arcanum": ("#DD4FD0", "magic", [
        ("rune", "rune sigil", arc_rune),
        ("sparkstar", "sparkle + orbits", arc_sparkstar),
        ("ring", "arcane ring", arc_ring),
        ("wand", "wand + star", arc_wand),
        ("swirl", "magic swirl", arc_swirl)]),
}

def render(code, drawfn):
    im, d, fill, key = backdrop_canvas(code)
    drawfn(d, fill, key)
    return im
