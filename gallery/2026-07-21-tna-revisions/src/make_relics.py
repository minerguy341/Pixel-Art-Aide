#!/usr/bin/env python3
"""T.N.A. relic/node revisions — apply the emissive-core + framed-relic lessons.

Three 16x16 revisions:
  aura_node   — glow-by-contrast: darker aetherium shell, a bright radial teal
                bloom core that is the ONLY saturated light on the block
                (emissive-core / make-invisible-visible).
  aetherlens  — framed-relic: brighter brass RIM enclosing a dark arcane lens
                CORE + one hot glint; grip stays greatwood.
  codex       — framed-relic tome: brass clasp + a framed teal emblem panel on
                a dark aetherium cover (rim/core read, not a flat sheet).

Idioms only (Reliquary / Embers / Malum / Eidolon) — no mod pixels used.
PNG is the build product; this script is the source of record (the aura node is a
radial gradient, so a generator is the honest source — same precedent as the
aspect icons; the lens/codex grids are legible inline above).
"""
from PIL import Image
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "out"
OUT.mkdir(parents=True, exist_ok=True)

def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)

def new():
    return Image.new("RGBA", (16, 16), (0, 0, 0, 0))

def lerp(a, b, t):
    return tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(4))

# ---------------------------------------------------------------- aura node
def aura_node():
    im = new()
    px = im.load()
    cx, cy = 7.5, 7.5
    R = 6.6                      # orb radius
    # aetherium shell ramp (darkened from r1 so the core out-glows it)
    SH_LIT = hx(0x9C7FCB)        # top-left lit
    SH_MID = hx(0x6E52A0)        # base
    SH_LO  = hx(0x40305E)        # bottom shadow rim (deep)
    # emissive teal bloom ramp (dark glass edge -> hot white core)
    GLOW = [
        hx(0x2E6A63),   # 0 deep glass (inner shell contact)
        hx(0x3E8B80),   # 1
        hx(0x55A89E),   # 2 mid
        hx(0x7FE8D8),   # 3 glint
        hx(0xA8F4E8),   # 4 hot
        hx(0xE8FFFA),   # 5 near-white
        hx(0xFFFFFF),   # 6 core
    ]
    import math
    for y in range(16):
        for x in range(16):
            dx, dy = x + 0.5 - cx, y + 0.5 - cy
            dist = math.hypot(dx, dy)
            if dist > R + 0.35:
                continue
            if dist > R - 1.0:
                # 1px shell — lit by top-left light direction
                ndl = -(dx + dy) / (dist + 1e-6)      # +1 top-left .. -1 bottom-right
                if ndl > 0.35:
                    px[x, y] = SH_LIT
                elif ndl < -0.35:
                    px[x, y] = SH_LO
                else:
                    px[x, y] = SH_MID
                continue
            # interior: radial bloom, hottest at (slightly up-left of) centre
            gx, gy = x + 0.5 - (cx - 0.6), y + 0.5 - (cy - 0.6)
            gd = math.hypot(gx, gy)
            t = 1.0 - min(gd / (R - 0.6), 1.0)        # 0 edge .. 1 core
            t = t ** 1.35                              # tighten the hot core
            f = t * (len(GLOW) - 1)
            i = int(f)
            if i >= len(GLOW) - 1:
                px[x, y] = GLOW[-1]
            else:
                px[x, y] = lerp(GLOW[i], GLOW[i + 1], f - i)
    # two drifting core glimmers (kept from r1 identity) — pin lights that read
    # as internal shimmer, not stray pixels: the near one hot, the far one softer
    px[6, 6] = GLOW[6]
    px[9, 8] = GLOW[4]
    im.save(OUT / "aura_node_rev.png")
    return im

# ---------------------------------------------------------------- aetherlens
def aetherlens():
    im = new()
    px = im.load()
    # brass rim ramp (brighter, encloses a darker lens core)
    Bd = hx(0x5A3F1E)   # brass border/deep
    Bs = hx(0x8F6B38)   # brass shadow
    Bb = hx(0xC79A55)   # brass base
    Bh = hx(0xF0D488)   # brass highlight (brighter than r1)
    # lens core (dark arcane) + hot glint
    Ls = hx(0x342552)   # lens shadow (darker core)
    Lb = hx(0x6E52A0)   # lens base
    Lh = hx(0xB99BE0)   # lens highlight
    G  = hx(0x9FF4E6)   # hot teal glint
    Gc = hx(0xE8FFFA)   # glint core
    # greatwood grip
    D = hx(0x2A1C18); Bw = hx(0x4F3B25); H = hx(0x60492C)
    n, m, o = None, None, None
    P = {
        'N': Bd, 'n': Bs, 'm': Bb, 'o': Bh,
        's': Ls, 'q': Lb, 'r': Lh, 'g': G, 'w': Gc,
        'D': D, 'B': Bw, 'H': H, '.': (0,0,0,0),
    }
    art = [
        ".........NNNN...",
        "........NooomN..",
        ".......NorrqmN..",
        "......NorwgqsN..",
        ".....NmorgqssN..",
        "....NmoqqqssN...",
        "....Nmon.NNN....",
        "...NmonN........",
        "..NmonN.........",
        "..NonN..........",
        ".HBBN...........",
        ".HBDB...........",
        "HBDB............",
        "HBDB............",
        ".DB.............",
        "................",
    ]
    for y, row in enumerate(art):
        for x, c in enumerate(row):
            if c != '.':
                px[x, y] = P[c]
    im.save(OUT / "aetherlens_rev.png")
    return im

# ---------------------------------------------------------------- codex
def codex():
    im = new()
    px = im.load()
    X = hx(0x241733)   # deepest purple border / core shadow
    p = hx(0x453268)   # cover shadow
    q = hx(0x6E52A0)   # cover base
    r = hx(0x9C7FCB)   # cover highlight
    # framed emblem panel
    e = hx(0x2E6A63)   # emblem bed (dark teal)
    g = hx(0x7FE8D8)   # teal sigil
    w = hx(0xCFFAF1)   # sigil hot
    # brass clasp
    n = hx(0x8F6B38); m = hx(0xC79A55); o = hx(0xF0D488)
    # page block
    Pg = hx(0xEDE9DC); d = hx(0xCFC7B0)
    P = {'X':X,'p':p,'q':q,'r':r,'e':e,'g':g,'w':w,'n':n,'m':m,'o':o,'P':Pg,'d':d,'.':(0,0,0,0)}
    art = [
        "................",
        "..XXXXXXXXXXX...",
        ".XrrqqqqqqqXPX..",
        ".XrqXeeeeXqXPX..",
        ".XrqeegewqXPX..",
        ".XrqeggggeqXPX..",
        ".XrqewgeeqXPX...",  # placeholder — corrected below
        ".XnmmmmmmommmX..",
        ".XrqqqqqqqqXdX..",
        ".XrqqqqqqqpXdX..",
        ".XpqqqqqqppXdX..",
        ".XppqqqpppqXdX..",
        ".XpppppppppXdX..",
        "..XXXXXXXXXXX...",
        "................",
        "................",
    ]
    # rebuild emblem rows cleanly (5x5 recessed teal panel, sigil inside)
    art = [
        "................",
        "..XXXXXXXXXXX...",
        ".XrrqqqqqqqXPX..",
        ".XrqXXXXXqqXPX..",
        ".XrqXegeXqqXPX..",
        ".XrqXgwgXqqXPX..",
        ".XrqXegeXqqXPX..",
        ".XnmmmmmmommmX..",
        ".XrqqqqqqqqXdX..",
        ".XrqqqqqqqpXdX..",
        ".XpqqqqqqppXdX..",
        ".XppqqqpppqXdX..",
        ".XpppppppppXdX..",
        "..XXXXXXXXXXX...",
        "................",
        "................",
    ]
    for y, row in enumerate(art):
        for x, c in enumerate(row):
            if c != '.':
                px[x, y] = P[c]
    im.save(OUT / "codex_rev.png")
    return im

if __name__ == "__main__":
    aura_node()
    aetherlens()
    codex()
    print("wrote aura_node_rev, aetherlens_rev, codex_rev to", OUT)
