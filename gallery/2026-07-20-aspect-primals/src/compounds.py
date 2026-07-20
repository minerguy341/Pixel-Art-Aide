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
    _stroke(d, [(32, 47), (32, 29)], 4, f, k)                     # stem
    _poly(d, [(31, 35), (23, 29), (18, 32), (22, 38), (30, 38)], f, k, 0.80)  # left leaf
    _poly(d, [(33, 31), (41, 22), (46, 26), (41, 33), (34, 34)], f, k, 0.80)  # right leaf

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

# ---- Arcanum, second batch (user wanted more magic options) ----
def arc_seal(d, f, k):
    ring(d, CX, CY, 15, 2, f, k)
    for i in range(12):                                           # runic rim ticks
        a = math.radians(i*30); L = 20 if i % 2 == 0 else 18
        _stroke_sharp(d, [(CX+15*math.cos(a), CY-15*math.sin(a)),
                          (CX+L*math.cos(a), CY-L*math.sin(a))], 2, f, k)
    spark(d, CX, CY, 5.5, f, k)

def arc_hexstar(d, f, k):
    _poly(d, star_pts(CX, CY, 6, 18, 8, rot=math.radians(90)), f, k, 0.62)
    disc(d, CX, CY, 3, f, k)

def arc_orb(d, f, k):
    cy = 29
    ring(d, CX, cy, 13, 2, f, k)                                  # crystal sphere
    d.arc([CX-8, cy-8, CX+3, cy+3], 205, 300, fill=f, width=2)    # highlight
    _stroke_sharp(d, [(CX-8, 45), (CX+8, 45)], 3, f, k)           # stand
    _stroke_sharp(d, [(CX-5, 42), (CX-7, 46)], 2, f, k)
    _stroke_sharp(d, [(CX+5, 42), (CX+7, 46)], 2, f, k)
    spark(d, CX+10, 20, 2.8, f, k)

def arc_sigil(d, f, k):
    ring(d, CX, CY, 15, 2, f, k)
    tri = [(32, 18), (45, 40), (19, 40)]                          # alchemical triangle
    _stroke_sharp(d, tri + [tri[0]], 2, f, k)
    disc(d, CX, 33, 2.6, f, k)

def arc_crescent(d, f, k):
    c1, R1 = (30, 31), 15
    c2, R2 = (37, 30), 13
    outer = [(c1[0]+R1*math.cos(math.radians(t)), c1[1]-R1*math.sin(math.radians(t)))
             for t in range(58, 303, 9)]
    inner = [(c2[0]+R2*math.cos(math.radians(t)), c2[1]-R2*math.sin(math.radians(t)))
             for t in range(302, 57, -9)]
    poly = outer + inner
    cxc = sum(p[0] for p in poly)/len(poly); cyc = sum(p[1] for p in poly)/len(poly)
    d.polygon(poly, fill=k); d.polygon(scale_about(poly, 0.86, cxc, cyc), fill=f)
    spark(d, 43, 20, 3.2, f, k)                                   # star in the hollow

def arc_comet(d, f, k):
    _stroke(d, [(38, 25), (23, 42)], 4, f, k)                     # tail
    _stroke(d, [(40, 27), (29, 45)], 2, f, k)
    _poly(d, star_pts(40, 22, 4, 8, 2.6), f, k, 0.5)             # head

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

# ---- Arcanum, batch 3: researched arcane/occult/alchemy iconography ----
def mg_pentacle(d, f, k):
    R = 17                                                        # star inscribed in the ring
    p = [(CX+R*math.cos(math.radians(90+i*72)), CY-R*math.sin(math.radians(90+i*72))) for i in range(5)]
    ring(d, CX, CY, 18, 2, f, k)                                 # circle first (star sits on top)
    _stroke_sharp(d, [p[i] for i in (0, 2, 4, 1, 3, 0)], 2, f, k)  # {5/2} pentagram, points touch ring

def mg_ouroboros(d, f, k):
    bb = [CX-14, CY-14, CX+14, CY+14]
    d.arc(bb, 300, 210, fill=k, width=6)                          # body (gap at lower-right)
    d.arc(bb, 300, 210, fill=f, width=3)
    a = math.radians(-35); hx, hy = CX+14*math.cos(a), CY-14*math.sin(a)  # head end
    _poly(d, [(hx+5, hy-3), (hx-4, hy-5), (hx-1, hy+5)], f, k, 0.55)      # head
    disc(d, hx, hy-1, 1.3, k, k)                                  # eye

def mg_triquetra(d, f, k):
    r = 10
    cs = [(CX+8*math.cos(math.radians(90+i*120)), CY-8*math.sin(math.radians(90+i*120))) for i in range(3)]
    for c in cs:
        d.ellipse([c[0]-r-1, c[1]-r-1, c[0]+r+1, c[1]+r+1], outline=k, width=4)
    for c in cs:
        d.ellipse([c[0]-r, c[1]-r, c[0]+r, c[1]+r], outline=f, width=2)

def mg_vegvisir(d, f, k):
    for i in range(8):
        a = math.radians(i*45); dx, dy = math.cos(a), -math.sin(a); px, py = -dy, dx
        base, tip = (CX+3*dx, CY+3*dy), (CX+19*dx, CY+19*dy)
        _stroke_sharp(d, [base, tip], 2, f, k)
        cb = (CX+14*dx, CY+14*dy)
        _stroke_sharp(d, [(cb[0]+3*px, cb[1]+3*py), (cb[0]-3*px, cb[1]-3*py)], 2, f, k)
        if i % 2 == 0:
            _stroke_sharp(d, [tip, (tip[0]+3*px+1*dx, tip[1]+3*py+1*dy)], 2, f, k)
            _stroke_sharp(d, [tip, (tip[0]-3*px+1*dx, tip[1]-3*py+1*dy)], 2, f, k)
        else:
            disc(d, tip[0], tip[1], 2, f, k)
    disc(d, CX, CY, 2.5, f, k)

def mg_mercury(d, f, k):
    d.arc([CX-7, 13, CX+7, 27], 200, 340, fill=k, width=4)        # horns
    d.arc([CX-7, 13, CX+7, 27], 200, 340, fill=f, width=2)
    ring(d, CX, 32, 7, 2, f, k)                                   # circle
    _stroke_sharp(d, [(CX, 39), (CX, 49)], 3, f, k)               # cross
    _stroke_sharp(d, [(CX-5, 44), (CX+5, 44)], 3, f, k)

def mg_eye(d, f, k):
    _stroke_sharp(d, [(17, 31), (24, 25), (40, 25), (47, 31)], 3, f, k)  # upper lid
    _stroke_sharp(d, [(17, 31), (24, 37), (40, 37), (47, 31)], 3, f, k)  # lower lid
    disc(d, CX, 31, 5, f, k); disc(d, CX, 31, 2, k, k)           # iris + pupil
    for dx in (-8, 0, 8):
        _stroke_sharp(d, [(CX+dx, 19), (CX+dx*1.25, 13)], 2, f, k)       # insight rays

def mg_grimoire(d, f, k):
    _poly(d, [(15, 23), (32, 27), (32, 45), (14, 41)], f, k, 0.88)  # left page
    _poly(d, [(49, 23), (32, 27), (32, 45), (50, 41)], f, k, 0.88)  # right page
    _stroke_sharp(d, [(32, 27), (32, 45)], 2, k, k)               # spine
    spark(d, 23, 34, 2.6, k, k)                                   # rune on page

def mg_runestone(d, f, k):
    _stroke_sharp(d, [(32, 13), (32, 51)], 4, f, k)               # bold stave
    _stroke_sharp(d, [(32, 25), (44, 15)], 4, f, k)
    _stroke_sharp(d, [(32, 25), (20, 15)], 4, f, k)
    _stroke_sharp(d, [(32, 39), (43, 47)], 4, f, k)

def mg_mandala(d, f, k):
    ring(d, CX, CY, 17, 2, f, k)
    for i in range(8):
        a = math.radians(i*45 + 22.5)
        spark(d, CX+12*math.cos(a), CY-12*math.sin(a), 2.3, f, k)
    ring(d, CX, CY, 6, 2, f, k); disc(d, CX, CY, 2, f, k)

def mg_phial(d, f, k):
    body = [(28, 16), (36, 16), (36, 25), (44, 43), (39, 48), (25, 48), (20, 43), (28, 25)]
    _stroke_sharp(d, body + [body[0]], 2, f, k)                   # glass flask
    _poly(d, [(27, 12), (37, 12), (37, 17), (27, 17)], f, k, 0.55)  # cork
    spark(d, 32, 40, 3, f, k)                                     # bubbling spark

MAGIC10 = ("#DD4FD0", "magic", [
    ("pentacle", "pentacle", mg_pentacle),
    ("ouroboros", "ouroboros", mg_ouroboros),
    ("triquetra", "triquetra", mg_triquetra),
    ("vegvisir", "runic compass", mg_vegvisir),
    ("mercury", "mercury glyph", mg_mercury),
    ("eye", "third eye", mg_eye),
    ("grimoire", "grimoire", mg_grimoire),
    ("runestone", "bold rune", mg_runestone),
    ("mandala", "mandala", mg_mandala),
    ("phial", "alchemist's phial", mg_phial)])

ARCANUM_MORE = ("#DD4FD0", "magic", [
    ("seal", "runic seal", arc_seal),
    ("hexstar", "6-point star", arc_hexstar),
    ("orb", "scrying orb", arc_orb),
    ("sigil", "alchemical sigil", arc_sigil),
    ("crescent", "crescent + star", arc_crescent),
    ("comet", "comet", arc_comet)])

def render(code, drawfn):
    im, d, fill, key = backdrop_canvas(code)
    drawfn(d, fill, key)
    return im
