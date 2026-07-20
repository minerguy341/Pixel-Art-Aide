"""Symbol candidates for compound aspects — 5 per aspect, filled-backdrop only.
Reuses the primal backdrop machinery (make_aspects.backdrop_canvas) so treatment
+ adaptive value contrast are identical. Colours are the canonical codes from
docs/aspects.md. Run via previews/compound_sheets.py.
"""
import math, sys
sys.path.insert(0, "gallery/2026-07-20-aspect-primals/src")
from make_aspects import (backdrop_canvas, _poly, _stroke, _stroke_sharp,
                          scale_about, N, hx, to_hsv, hsv)

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

def line(d, seg, col):
    d.line(seg, fill=col, width=1)

# ===================== VIGOR — energy (#F2C230) =====================
def vig_bolt(d, f, k):
    _poly(d, [(35, 13), (23, 33), (31, 33), (27, 51), (43, 29), (35, 29), (39, 13)], f, k, 0.72)

def vig_boltcircle(d, f, k):
    ring(d, CX, CY, 17, 2, f, k)
    _poly(d, [(34, 18), (26, 32), (32, 32), (29, 45), (40, 30), (33, 30), (37, 18)], f, k, 0.66)

def vig_core(d, f, k):
    for i in range(8):
        a = math.radians(i*45); dx, dy = math.cos(a), -math.sin(a)
        _stroke_sharp(d, [(CX+9*dx, CY+9*dy), (CX+18*dx, CY+18*dy)], 2, f, k)
    disc(d, CX, CY, 7, f, k)

def vig_battery(d, f, k):
    _stroke_sharp(d, [(23, 21), (41, 21), (41, 48), (23, 48), (23, 21)], 2, f, k)
    _poly(d, [(29, 16), (35, 16), (35, 21), (29, 21)], f, k, 0.5)
    _poly(d, [(34, 25), (29, 34), (33, 34), (31, 44), (38, 33), (33, 33), (36, 25)], f, k, 0.55)

def vig_dblbolt(d, f, k):
    _poly(d, [(30, 14), (21, 31), (27, 31), (24, 48), (35, 30), (29, 30), (33, 14)], f, k, 0.55)
    _poly(d, [(44, 20), (36, 35), (41, 35), (38, 50), (47, 34), (42, 34), (46, 20)], f, k, 0.55)

# ===================== GEMMA — crystal (#9FE6C9) =====================
def gem_brilliant(d, f, k):
    _poly(d, [(24, 23), (40, 23), (48, 31), (32, 50), (16, 31)], f, k, 0.86)
    for seg in ([(16, 31), (48, 31)], [(32, 23), (32, 31)], [(24, 23), (32, 31)],
                [(40, 23), (32, 31)], [(24, 31), (32, 50)], [(40, 31), (32, 50)]):
        line(d, seg, k)

def gem_cluster(d, f, k):
    _poly(d, [(20, 46), (26, 27), (31, 46)], f, k, 0.68)
    _poly(d, [(28, 48), (35, 17), (41, 48)], f, k, 0.78)
    _poly(d, [(38, 46), (44, 31), (49, 46)], f, k, 0.68)

def gem_emerald(d, f, k):
    # rectangular step (emerald) cut — distinct from the hexagon backdrop
    outer = [(20, 22), (44, 22), (47, 42), (17, 42)]
    inner = [(25, 27), (39, 27), (41, 37), (23, 37)]
    _poly(d, outer, f, k, 0.86)
    for a, b in zip(inner, inner[1:] + inner[:1]):
        line(d, [a, b], k)
    for o, i2 in zip(outer, inner):
        line(d, [o, i2], k)

def gem_point(d, f, k):
    _poly(d, [(27, 21), (37, 21), (37, 41), (32, 50), (27, 41)], f, k, 0.86)
    _poly(d, [(30, 14), (34, 14), (37, 21), (27, 21)], f, k, 0.82)
    for seg in ([(32, 14), (32, 50)], [(27, 21), (37, 21)]):
        line(d, seg, k)

def gem_round(d, f, k):
    disc(d, CX, CY, 13, f, k)                                     # round brilliant, top view
    d.ellipse([CX-6, CY-6, CX+6, CY+6], outline=k, width=1)       # table
    for i in range(8):                                            # crown facets
        a = math.radians(i*45 + 22)
        line(d, [(CX+6*math.cos(a), CY-6*math.sin(a)), (CX+13*math.cos(a), CY-13*math.sin(a))], k)
    spark(d, CX+10, CY-11, 2.6, f, k)

# ===================== AES — metal / ore (#ADAFBC) =====================
def aes_ingot(d, f, k):
    _poly(d, [(15, 39), (49, 39), (44, 29), (20, 29)], f, k, 0.82)
    line(d, [(23, 33), (41, 33)], k)

def aes_anvil(d, f, k):
    _poly(d, [(15, 23), (49, 23), (44, 29), (39, 29), (41, 33), (23, 33), (25, 29), (20, 29)], f, k, 0.82)
    _poly(d, [(27, 33), (37, 33), (41, 46), (23, 46)], f, k, 0.82)

def aes_ore(d, f, k):
    _poly(d, [(18, 41), (16, 28), (26, 19), (40, 20), (48, 30), (44, 43), (30, 47)], f, k, 0.88)
    for x, y in [(28, 30), (35, 26), (31, 38), (40, 35)]:
        disc(d, x, y, 2.4, k, k)

def aes_gear(d, f, k):
    for i in range(8):
        a = math.radians(i*45); dx, dy = math.cos(a), -math.sin(a)
        x, y = CX+14*dx, CY+14*dy
        _poly(d, [(x-3, y-3), (x+3, y-3), (x+3, y+3), (x-3, y+3)], f, k, 0.7)
    disc(d, CX, CY, 13, f, k)
    disc(d, CX, CY, 4.5, k, k)

def aes_nugget(d, f, k):
    for x, y, r in [(25, 29, 7), (39, 31, 6), (31, 41, 6)]:
        disc(d, x, y, r, f, k)
        d.arc([x-r+2, y-r+2, x+2, y+2], 205, 300, fill=k, width=1)

# ---- Gemma: gem tilted toward top-down so the faceted crown dominates (like #5, in 3D) ----
def _oct(cx, cy, rx, ry, off=0):
    return [(cx+rx*math.cos(math.radians(a+off)), cy-ry*math.sin(math.radians(a+off))) for a in range(0, 360, 45)]

def gem_toptilt(d, f, k, cy=25, ry=9, culet=48):
    cx, rx = 31, 16
    o = _oct(cx, cy, rx, ry)                       # foreshortened crown rim (0=E..315)
    cp = (cx, culet)
    outer = [o[4], o[3], o[2], o[1], o[0], o[7], cp, o[5]]   # back rim + front down to culet
    _poly(d, outer, f, k, 0.92)
    for p in o:                                    # crown facets from centre
        line(d, [(cx, cy), p], k)
    it = _oct(cx, cy, rx*0.5, ry*0.5)              # table
    for a, b in zip(it, it[1:] + it[:1]):
        line(d, [a, b], k)
    for i in (5, 6, 7):                            # pavilion facets to the culet
        line(d, [o[i], cp], k)

def gem_toptilt_flat(d, f, k):   # more top-down (shallower body)
    gem_toptilt(d, f, k, cy=26, ry=11, culet=44)

def gem_toptilt_deep(d, f, k):   # a touch more side showing
    gem_toptilt(d, f, k, cy=23, ry=8, culet=51)

# ---- Aes: isometric ingots (3-face shaded mini-render, not a flat glyph) ----
def _metal_shades(code):
    h, s, _ = to_hsv(hx(code))
    return (hsv(h, s*0.55, 0.56),      # top  (lit)
            hsv(h, s*0.75, 0.38),      # left / south face
            hsv(h, s*0.85, 0.24),      # right / east face
            hsv(h, min(1, s), 0.09),   # edge outline
            hsv(h, s*0.28, 0.84))      # shine (specular streak)

def _facebox(d, P, x0, y0, z0, W, D, H, top, left, right, edge, shine=None, spec=True):
    south = [P(x0, y0, z0+D), P(x0+W, y0, z0+D), P(x0+W, y0+H, z0+D), P(x0, y0+H, z0+D)]
    east = [P(x0+W, y0, z0), P(x0+W, y0+H, z0), P(x0+W, y0+H, z0+D), P(x0+W, y0, z0+D)]
    topf = [P(x0, y0+H, z0), P(x0+W, y0+H, z0), P(x0+W, y0+H, z0+D), P(x0, y0+H, z0+D)]
    for poly, col in ((south, left), (east, right), (topf, top)):
        d.polygon(poly, fill=col, outline=edge)
    if spec and shine:                                          # specular streak + glint (metal)
        streak = [P(x0+1.5, y0+H, z0+0.22*D), P(x0+W-1.5, y0+H, z0+0.22*D),
                  P(x0+W-2.5, y0+H, z0+0.40*D), P(x0+2.5, y0+H, z0+0.40*D)]
        d.polygon(streak, fill=shine)
        gx, gy = P(x0+3.5, y0+H, z0+0.31*D)
        d.rectangle([gx-1, gy-1, gx+1, gy+1], fill=shine)
        d.line([P(x0, y0+H, z0+D), P(x0+W, y0+H, z0+D)], fill=shine, width=1)

def _iso_box(d, ox, oy, W, D, H, s, *shades):
    def P(x, y, z): return (ox + (x-z)*s, oy + (x+z)*s*0.5 - y*s)
    _facebox(d, P, 0, 0, 0, W, D, H, *shades)

def iso_single(code):
    im, d, _, _ = backdrop_canvas(code)
    _iso_box(d, 24, 27, 17, 10, 6, 1.7, *_metal_shades(code))
    return im

def iso_wide(code):
    im, d, _, _ = backdrop_canvas(code)
    _iso_box(d, 20, 26, 21, 8, 5, 1.6, *_metal_shades(code))     # longer, flatter bar
    return im

def iso_pair(code):
    im, d, _, _ = backdrop_canvas(code)
    sh = _metal_shades(code)
    _iso_box(d, 25, 20, 15, 9, 5, 1.6, *sh)
    _iso_box(d, 23, 31, 15, 9, 5, 1.6, *sh)
    return im

def _iso_scene(d, ox, oy, s, boxes, *shades):
    """Draw several boxes in ONE iso space, painter-sorted far->near so they
    occlude correctly instead of clipping. Each box = (x0, y0, z0, W, D, H)."""
    def P(x, y, z): return (ox + (x-z)*s, oy + (x+z)*s*0.5 - y*s)
    for x0, y0, z0, W, D, H in sorted(boxes, key=lambda b: (b[0]+b[3]/2)+(b[2]+b[4]/2)+(b[1]+b[5]/2)):
        _facebox(d, P, x0, y0, z0, W, D, H, *shades)

def iso_stack(code):
    im, d, _, _ = backdrop_canvas(code)
    W, D, H = 13, 7, 5
    boxes = [(0, 0, 0, W, D, H),              # bottom, front
             (0, 0, D+1, W, D, H),            # bottom, back (small gap, no clip)
             (0, H, (D+1)/2, W, D, H)]        # top, centred on the two
    _iso_scene(d, 33, 30, 1.5, boxes, *_metal_shades(code))
    return im

# ---- Aes: ingot options, round 2 (researched real ingot shapes) ----
def _goldbar(d, cx, cy, w, f, k, stamp=True):
    # 3/4 bullion bar: top face wider, tapering DOWN (mould draft); top parallelogram recedes up-right
    fTL, fTR = (cx-w, cy), (cx+w, cy)
    fBL, fBR = (cx-w+3, cy+10), (cx+w-3, cy+10)
    tBL, tBR = (cx-w+5, cy-8), (cx+w+5, cy-8)
    _poly(d, [tBL, tBR, fTR, fBR, fBL, fTL], f, k, 0.94)
    line(d, [fTL, fTR], k)                               # top/front seam
    line(d, [tBL, fTL], k); line(d, [tBR, fTR], k)       # back edges
    if stamp:
        line(d, [(cx-w+7, cy-5), (cx+w+2, cy-5)], k)     # top-face shine
        d.rectangle([cx-5, cy+3, cx+5, cy+7], outline=k, width=1)  # front stamp

def aes_goldbar(d, f, k):
    _goldbar(d, 30, 28, 17, f, k)

def aes_goldstack(d, f, k):
    _goldbar(d, 31, 21, 13, f, k, stamp=False)
    _goldbar(d, 29, 34, 17, f, k)

def aes_sycee(d, f, k):
    # Chinese sycee / yuanbao boat ingot: up-swept pointed ends, concave waist, centre knob
    outer = [(14, 29), (23, 39), (28, 36), (32, 38), (36, 36), (41, 39), (50, 29),
             (52, 40), (41, 46), (23, 46), (12, 40)]
    _poly(d, outer, f, k, 0.9)
    d.pieslice([25, 27, 39, 41], 180, 360, fill=k)        # centre knob
    d.pieslice([26, 28, 38, 40], 180, 360, fill=f)
    line(d, [(20, 42), (44, 42)], k)                      # hull waterline

def aes_flatbar(d, f, k):
    # vanilla-style beveled bar lying flat, lit from the top-left
    _poly(d, [(15, 31), (20, 27), (44, 27), (49, 31), (44, 37), (20, 37)], f, k, 0.9)
    line(d, [(21, 29), (43, 29)], k)                      # top shine
    line(d, [(20, 34), (44, 34)], k)                      # lower groove

def aes_loaf(d, f, k):
    # rough cast loaf ingot: flat base, rounded top
    d.pieslice([16, 22, 48, 46], 180, 360, fill=k)
    d.pieslice([17, 23, 47, 45], 180, 360, fill=f)
    _poly(d, [(16, 34), (48, 34), (46, 42), (18, 42)], f, k, 0.9)
    line(d, [(22, 29), (34, 27)], k)                      # top highlight

# ---- Aes: ingot options (first pass) ----
def _bar(d, cx, cy, w, f, k, shine=True):
    outer = [(cx-w+6, cy-7), (cx+w+6, cy-7), (cx+w, cy), (cx+w-3, cy+9),
             (cx-w+3, cy+9), (cx-w, cy)]
    _poly(d, outer, f, k, 0.94)
    line(d, [(cx-w, cy), (cx+w, cy)], k)           # top/front seam
    line(d, [(cx-w+6, cy-7), (cx-w, cy)], k); line(d, [(cx+w+6, cy-7), (cx+w, cy)], k)
    if shine:
        line(d, [(cx-w+3, cy-4), (cx+w+2, cy-4)], k)   # top shine
        line(d, [(cx-w+4, cy+4), (cx+w-4, cy+4)], k)   # front highlight

def aes_bar(d, f, k):
    _bar(d, 30, 27, 17, f, k)

def aes_stack(d, f, k):
    _bar(d, 31, 20, 14, f, k)
    _bar(d, 29, 33, 17, f, k)

def aes_pyramid(d, f, k):
    _bar(d, 22, 34, 11, f, k)
    _bar(d, 42, 34, 11, f, k)
    _bar(d, 32, 22, 11, f, k)

def aes_iso(d, f, k):
    # true isometric ingot: top rhombus + left & right faces, faces split by keyline
    top = [(31, 15), (50, 25), (31, 31), (12, 25)]
    _poly(d, [(12, 25), (31, 31), (50, 25), (48, 38), (31, 45), (14, 38)], f, k, 0.94)  # body
    _poly(d, top, f, k, 0.9)                        # top face
    line(d, [(31, 31), (31, 45)], k)                # front vertical edge
    line(d, [(50, 25), (48, 38)], k); line(d, [(12, 25), (14, 38)], k)

def gem_angled(d, f, k):
    # 3/4 brilliant: rhombus table seen from above + crown facets + pavilion point
    outer = [(32, 13), (49, 27), (32, 52), (15, 27)]              # kite silhouette
    _poly(d, outer, f, k, 0.9)
    table = [(32, 19), (41, 27), (32, 33), (23, 27)]             # table (seen at angle)
    for a, b in zip(table, table[1:] + table[:1]):
        line(d, [a, b], k)
    line(d, [(15, 27), (49, 27)], k)                             # girdle
    line(d, [(32, 13), (32, 19)], k)                             # crown ridges
    line(d, [(49, 27), (41, 27)], k); line(d, [(15, 27), (23, 27)], k)
    for tv in (table[1], table[2], table[3]):                    # pavilion facets to culet
        line(d, [tv, (32, 52)], k)

def gem_angled2(d, f, k):
    # tilted brilliant: table skewed to one side (stronger 3D read)
    outer = [(28, 13), (50, 24), (36, 52), (14, 30)]
    _poly(d, outer, f, k, 0.9)
    table = [(30, 20), (41, 25), (34, 33), (23, 27)]
    for a, b in zip(table, table[1:] + table[:1]):
        line(d, [a, b], k)
    line(d, [(14, 30), (50, 24)], k)                             # girdle (tilted)
    line(d, [(28, 13), (30, 20)], k)
    line(d, [(50, 24), (41, 25)], k); line(d, [(14, 30), (23, 27)], k)
    for tv in (table[1], table[2], table[3]):
        line(d, [tv, (36, 52)], k)

# ---- Aes: better, dimensional ingot ----
def aes_ingot2(d, f, k):
    # 3D bar: top parallelogram + front face, edges + shine picked out in the keyline
    outer = [(21, 29), (53, 29), (48, 37), (43, 47), (19, 47), (14, 37)]
    _poly(d, outer, f, k, 0.92)
    line(d, [(14, 37), (48, 37)], k)                             # top/front seam
    line(d, [(21, 29), (14, 37)], k); line(d, [(53, 29), (48, 37)], k)  # back edges
    line(d, [(27, 32), (47, 32)], k)                             # top-face shine
    line(d, [(23, 42), (38, 42)], k)                             # front-face highlight

VIGOR5 = ("#F2C230", "energy", [
    ("bolt", "lightning bolt", vig_bolt),
    ("boltcircle", "bolt in circle", vig_boltcircle),
    ("core", "power core", vig_core),
    ("battery", "charged cell", vig_battery),
    ("dblbolt", "double bolt", vig_dblbolt)])
GEMMA5 = ("#9FE6C9", "crystal", [
    ("brilliant", "cut gem", gem_brilliant),
    ("cluster", "crystal cluster", gem_cluster),
    ("emerald", "emerald cut", gem_emerald),
    ("point", "crystal point", gem_point),
    ("round", "polished jewel", gem_round)])
AES5 = ("#ADAFBC", "metal / ore", [
    ("ingot", "ingot", aes_ingot),
    ("anvil", "anvil", aes_anvil),
    ("ore", "ore chunk", aes_ore),
    ("gear", "cog", aes_gear),
    ("nugget", "nugget cluster", aes_nugget)])

# ===================== GLACIES — ice (#A9E7F5) =====================
def gla_snowflake(d, f, k):
    R = 20
    for i in range(6):
        a = math.radians(i*60); dx, dy = math.cos(a), -math.sin(a); px, py = -dy, dx
        tip = (CX+R*dx, CY+R*dy)
        _stroke_sharp(d, [(CX, CY), tip], 2, f, k)               # arm
        _poly(d, [tip, (tip[0]-3*dx+2*px, tip[1]-3*dy+2*py),     # sharp diamond tip
                  (tip[0]-3*dx-2*px, tip[1]-3*dy-2*py)], f, k, 0.5)
        for rr, bl in ((9, 6), (14.5, 5)):                       # two symmetric branch pairs, pointed
            bx, by = CX+rr*dx, CY+rr*dy
            for sgn in (1, -1):
                ex = bx + bl*(dx+sgn*px)/1.414
                ey = by + bl*(dy+sgn*py)/1.414
                _stroke_sharp(d, [(bx, by), (ex, ey)], 1, f, k)
    _poly(d, star_pts(CX, CY, 6, 5.5, 2.4, math.radians(90)), f, k, 0.4)  # crisp hex core

def gla_icicles(d, f, k):
    _stroke_sharp(d, [(15, 18), (49, 18)], 3, f, k)
    for x, ln in [(21, 15), (29, 22), (37, 13), (44, 18)]:
        _poly(d, [(x-3, 18), (x+3, 18), (x, 18+ln)], f, k, 0.55)

def gla_shards(d, f, k):
    _poly(d, [(21, 48), (18, 25), (26, 33), (27, 48)], f, k, 0.7)
    _poly(d, [(28, 49), (33, 15), (39, 49)], f, k, 0.78)
    _poly(d, [(39, 48), (46, 27), (48, 48)], f, k, 0.7)

def gla_frost(d, f, k):
    _poly(d, star_pts(CX, CY, 4, 18, 4), f, k, 0.5)
    _poly(d, star_pts(CX, CY, 4, 12, 3.5, math.radians(45)), f, k, 0.5)
    for a in (45, 135, 225, 315):
        spark(d, CX+20*math.cos(math.radians(a)), CY-20*math.sin(math.radians(a)), 2, f, k)

def gla_cube(d, f, k):
    hexp = [(32, 15), (47, 24), (47, 40), (32, 49), (17, 40), (17, 24)]
    _poly(d, hexp, f, k, 0.9)
    line(d, [(32, 15), (32, 32)], k); line(d, [(32, 32), (17, 24)], k); line(d, [(32, 32), (47, 24)], k)
    spark(d, 26, 22, 2.6, f, k)

# ===================== LETUM — death (#45403E) =====================
def let_skull(d, f, k):
    _poly(d, [(20, 18), (44, 18), (46, 31), (40, 38), (24, 38), (18, 31)], f, k, 0.9)
    disc(d, 27, 28, 3.6, k, k); disc(d, 37, 28, 3.6, k, k)       # eye sockets
    _poly(d, [(32, 30), (34, 35), (30, 35)], k, k)               # nose
    _poly(d, [(25, 38), (39, 38), (38, 45), (26, 45)], f, k, 0.8)  # jaw
    for x in (29, 32, 35):
        line(d, [(x, 39), (x, 45)], k)                           # teeth

def let_scythe(d, f, k):
    _stroke(d, [(35, 50), (31, 14)], 3, f, k)                    # snath
    _stroke(d, [(31, 15), (22, 16), (16, 21), (14, 29)], 3, f, k)  # curved blade

def let_bones(d, f, k):
    for ang in (35, -35):
        a = math.radians(ang); dx, dy = math.cos(a), -math.sin(a); px, py = -dy, dx
        _stroke(d, [(CX-16*dx, CY-16*dy), (CX+16*dx, CY+16*dy)], 3, f, k)
        for s in (-1, 1):
            ex, ey = CX+s*16*dx, CY+s*16*dy
            disc(d, ex+2.5*px, ey+2.5*py, 2, f, k); disc(d, ex-2.5*px, ey-2.5*py, 2, f, k)

def let_grave(d, f, k):
    d.pieslice([18, 14, 46, 42], 180, 360, fill=k); d.pieslice([19, 15, 45, 41], 180, 360, fill=f)
    _poly(d, [(18, 28), (46, 28), (46, 47), (18, 47)], f, k, 0.92)
    _stroke_sharp(d, [(32, 32), (32, 43)], 2, k, k); _stroke_sharp(d, [(27, 36), (37, 36)], 2, k, k)
    _stroke_sharp(d, [(13, 47), (51, 47)], 2, f, k)

def let_skullcross(d, f, k):
    _poly(d, [(23, 15), (41, 15), (43, 25), (38, 30), (26, 30), (21, 25)], f, k, 0.9)  # skull
    disc(d, 29, 22, 2.6, k, k); disc(d, 35, 22, 2.6, k, k)
    _poly(d, [(28, 30), (36, 30), (35, 34), (29, 34)], f, k, 0.8)
    for ang in (28, -28):                                        # crossbones below
        a = math.radians(ang); dx, dy = math.cos(a), -math.sin(a); px, py = -dy, dx
        _stroke(d, [(20, 40-8*dx*0), (44, 40)] if False else [(CX-13*dx, 42-13*dy), (CX+13*dx, 42+13*dy)], 3, f, k)
        for s in (-1, 1):
            ex, ey = CX+s*13*dx, 42+s*13*dy
            disc(d, ex+2*px, ey+2*py, 1.6, f, k); disc(d, ex-2*px, ey-2*py, 1.6, f, k)

# ===================== AETHER — aura (#B37FE8) =====================
def aeth_node(d, f, k):
    _poly(d, star_pts(CX, CY, 4, 7, 3), f, k, 0.5)
    for i in range(8):
        a = math.radians(i*45); dx, dy = math.cos(a), -math.sin(a)
        _stroke_sharp(d, [(CX+9*dx, CY+9*dy), (CX+17*dx, CY+17*dy)], 2, f, k)
    for i in range(4):
        a = math.radians(i*90+45); spark(d, CX+20*math.cos(a), CY-20*math.sin(a), 2, f, k)

def aeth_swirl(d, f, k):
    for arm in (0.0, math.pi):
        pts = [(CX+(2+t*0.062)*math.cos(math.radians(t)+arm), CY-(2+t*0.062)*math.sin(math.radians(t)+arm))
               for t in range(0, 200, 10)]
        _stroke(d, pts, 3, f, k)
    spark(d, 45, 21, 2.6, f, k); spark(d, 19, 42, 2.4, f, k)

def aeth_rings(d, f, k):
    disc(d, CX, CY, 4, f, k)
    ring(d, CX, CY, 10, 2, f, k); ring(d, CX, CY, 16, 2, f, k)
    for a in (0, 90, 180, 270):
        spark(d, CX+16*math.cos(math.radians(a)), CY-16*math.sin(math.radians(a)), 2.4, f, k)

def aeth_wisp(d, f, k):
    _stroke(d, [(30, 49), (35, 40), (27, 32), (35, 23), (30, 15)], 4, f, k)
    spark(d, 30, 14, 3, f, k); spark(d, 38, 30, 2.2, f, k)

def aeth_mote(d, f, k):
    _poly(d, star_pts(CX, CY, 4, 13, 4), f, k, 0.5)
    ring(d, CX, CY, 18, 1, f, k)

def iso_skull(code):
    # blocky isometric skull: bone-shaded cube (cranium) + jaw block + sunken features
    im, d, _, _ = backdrop_canvas(code)
    top, left, right, edge = (232, 228, 214), (196, 190, 176), (150, 144, 130), (34, 30, 28)
    dark = (46, 40, 40)
    ox, oy, s = 32, 26, 1.55
    def P(x, y, z): return (ox + (x-z)*s, oy + (x+z)*s*0.5 - y*s)
    W, D, H = 16, 15, 13
    _facebox(d, P, 0, 0, 3, W, D, H, top, left, right, edge, spec=False)      # cranium
    _facebox(d, P, 3, -4, 6, W-6, D-6, 4, top, left, right, edge, spec=False)  # jaw (lower, forward)
    def qs(x0, x1, y0, y1, z):   # quad on the south face (z const)
        return [P(x0, y0, z), P(x1, y0, z), P(x1, y1, z), P(x0, y1, z)]
    def qe(z0, z1, y0, y1, x):   # quad on the east face (x const)
        return [P(x, y0, z0), P(x, y0, z1), P(x, y1, z1), P(x, y1, z0)]
    d.polygon(qs(8.5, 13, 8, 11.5, D+3), fill=dark)    # left eye  (south, toward front edge)
    d.polygon(qe(8.5, 13, 8, 11.5, W), fill=dark)      # right eye (east, toward front edge)
    d.polygon([P(W, 6.5, D+3), P(W-1.5, 5, D+1.5), P(W-1, 8, D+2)], fill=dark)  # nose at the ridge
    for t in range(3):                                 # teeth gaps on the jaw front faces
        d.line([P(5+t*2.2, -4, D-0.02), P(5+t*2.2, 0, D-0.02)], fill=dark, width=1)
        d.line([P(W-0.02, -4, 6+t*2.2), P(W-0.02, 0, 6+t*2.2)], fill=dark, width=1)
    return im

# ---- Letum: tombstone / grave-marker candidates ----
def grave_rip(d, f, k):
    d.pieslice([19, 13, 45, 39], 180, 360, fill=k); d.pieslice([20, 14, 44, 38], 180, 360, fill=f)
    _poly(d, [(19, 26), (45, 26), (45, 45), (19, 45)], f, k, 0.92)
    _stroke_sharp(d, [(32, 30), (32, 41)], 2, k, k); _stroke_sharp(d, [(27, 34), (37, 34)], 2, k, k)  # cross
    _stroke_sharp(d, [(13, 46), (51, 46)], 2, f, k)                # ground
    for gx in (17, 47):
        _stroke_sharp(d, [(gx, 46), (gx-2, 42)], 1, f, k); _stroke_sharp(d, [(gx, 46), (gx+2, 42)], 1, f, k)

def grave_cross(d, f, k):
    _poly(d, [(29, 14), (35, 14), (35, 44), (29, 44)], f, k, 0.85)  # upright
    _poly(d, [(21, 22), (43, 22), (43, 28), (21, 28)], f, k, 0.85)  # arms
    d.pieslice([16, 40, 48, 54], 180, 360, fill=k); d.pieslice([17, 41, 47, 53], 180, 360, fill=f)  # mound
    _stroke_sharp(d, [(13, 47), (51, 47)], 2, f, k)

def grave_arch(d, f, k):
    _poly(d, [(20, 45), (20, 24), (32, 13), (44, 24), (44, 45)], f, k, 0.92)  # gothic pointed arch
    for yy in (29, 34, 39):
        line(d, [(25, yy), (39, yy)], k)                           # engraved lines
    _stroke_sharp(d, [(14, 46), (50, 46)], 2, f, k)

def grave_crack(d, f, k):
    d.pieslice([19, 13, 45, 39], 180, 360, fill=k); d.pieslice([20, 14, 44, 38], 180, 360, fill=f)
    _poly(d, [(19, 26), (45, 26), (45, 45), (19, 45)], f, k, 0.92)
    _stroke_sharp(d, [(30, 15), (33, 24), (29, 33), (32, 45)], 1, k, k)   # crack
    d.polygon([(45, 26), (45, 33), (40, 27)], fill=k)              # chipped corner
    _stroke_sharp(d, [(13, 46), (51, 46)], 2, f, k)

def grave_celtic(d, f, k):
    _poly(d, [(29, 12), (35, 12), (35, 45), (29, 45)], f, k, 0.85)  # upright
    _poly(d, [(21, 23), (43, 23), (43, 29), (21, 29)], f, k, 0.85)  # arms
    ring(d, 32, 26, 8, 2, f, k)                                    # halo ring
    d.pieslice([16, 41, 48, 55], 180, 360, fill=k); d.pieslice([17, 42, 47, 54], 180, 360, fill=f)
    _stroke_sharp(d, [(13, 47), (51, 47)], 2, f, k)

LETUM_GRAVES = ("#45403E", "death", [
    ("rip", "rounded + cross", grave_rip),
    ("cross", "cross marker", grave_cross),
    ("arch", "gothic arch", grave_arch),
    ("crack", "weathered", grave_crack),
    ("celtic", "celtic cross", grave_celtic)])

# ---- Aether: more aura candidates (batch 2) ----
def aeth_orb(d, f, k):
    disc(d, CX, CY, 8, f, k)
    for i in range(6):
        a = math.radians(i*60); dx, dy = math.cos(a), -math.sin(a)
        _stroke_sharp(d, [(CX+11*dx, CY+11*dy), (CX+18*dx, CY+18*dy)], 2, f, k)
    ring(d, CX, CY, 13, 1, f, k)

def aeth_crystal(d, f, k):
    _poly(d, [(32, 14), (41, 28), (34, 50), (23, 28)], f, k, 0.86)      # floating shard
    line(d, [(32, 14), (32, 50)], k); line(d, [(23, 28), (41, 28)], k)  # facets
    for x, y in [(45, 20), (19, 40), (44, 43)]:
        spark(d, x, y, 2.4, f, k)                                       # emanating motes

def aeth_mist(d, f, k):
    for cx, cy, r in [(24, 31, 7), (33, 28, 8), (40, 32, 6)]:
        disc(d, cx, cy, r, f, k)
    _poly(d, [(17, 35), (47, 35), (45, 40), (19, 40)], f, k, 0.9)       # cloud base
    spark(d, 33, 18, 2.6, f, k)

def aeth_aurora(d, f, k):
    for oy in (-7, 0, 7):
        pts = [(x, CY+oy+4*math.sin((x-14)/5.0)) for x in range(14, 51, 3)]
        _stroke(d, pts, 2, f, k)
    spark(d, 45, 18, 2.6, f, k); spark(d, 19, 45, 2.2, f, k)

def aeth_motes(d, f, k):
    for x, y, r in [(24, 24, 4), (40, 22, 3.2), (32, 34, 4.6), (21, 41, 3), (43, 43, 3.6), (33, 49, 2.6)]:
        spark(d, x, y, r, f, k)

def aeth_pulse(d, f, k):
    disc(d, CX, CY, 3.5, f, k)
    for r in (8, 13, 18):
        d.arc([CX-r, CY-r, CX+r, CY+r], 205, 335, fill=k, width=3)
        d.arc([CX-r, CY-r, CX+r, CY+r], 205, 335, fill=f, width=1)

AETHER_MORE = ("#B37FE8", "aura", [
    ("orb", "radiant orb", aeth_orb),
    ("crystal", "crystal node", aeth_crystal),
    ("mist", "aura mist", aeth_mist),
    ("aurora", "aurora bands", aeth_aurora),
    ("motes", "drifting motes", aeth_motes),
    ("pulse", "aura pulse", aeth_pulse)])

GLACIES5 = ("#A9E7F5", "ice", [
    ("snowflake", "snowflake", gla_snowflake), ("icicles", "icicles", gla_icicles),
    ("shards", "ice shards", gla_shards), ("frost", "frost sparkle", gla_frost),
    ("cube", "ice block", gla_cube)])
LETUM5 = ("#45403E", "death", [
    ("skull", "skull", let_skull), ("scythe", "scythe", let_scythe),
    ("bones", "crossed bones", let_bones), ("grave", "tombstone", let_grave),
    ("skullcross", "skull & crossbones", let_skullcross)])
AETHER5 = ("#B37FE8", "aura", [
    ("node", "radiant node", aeth_node), ("swirl", "aura swirl", aeth_swirl),
    ("rings", "aura rings", aeth_rings), ("wisp", "spirit wisp", aeth_wisp),
    ("mote", "haloed mote", aeth_mote)])

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
    R = 16.5                                                      # star inscribed in the ring
    p = [(CX+R*math.cos(math.radians(90+i*72)), CY-R*math.sin(math.radians(90+i*72))) for i in range(5)]
    _stroke_sharp(d, [p[i] for i in (0, 2, 4, 1, 3, 0)], 2, f, k)  # {5/2} pentagram first
    ring(d, CX, CY, 18, 2, f, k)                                 # ring on top -> circle uninterrupted

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
