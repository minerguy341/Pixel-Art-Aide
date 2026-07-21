"""Author the silhouettes for a set of spear/arrowhead-inspired wand tips.

This set exists to exercise the forged cross-sections added to `aide.lift`
(lens/midrib, diamond, square, radial) — studied from real spear and arrowhead
geometry, where a tip is never round: a leaf blade is lenticular with a raised
midrib, an estoc point is rhombic, a bodkin is a square punch, a broadhead is
three thin blades in a Y. Each cap is still a side-view silhouette (round collar
+ neck + head); the *cross-section* is chosen per tip in build_tips.py.

Run from repo root:  python3 gallery/2026-07-21-wand-tips-study/make_tips.py
"""

from __future__ import annotations

import math
from pathlib import Path

W, H = 46, 24
CY = (H - 1) / 2.0
HERE = Path(__file__).resolve().parent

COLLAR_X0, COLLAR_X1 = 0, 8
NECK_X0, NECK_X1 = 9, 14        # overlaps the head so every tip welds to the base
HEAD_X0 = 13
COLLAR_HALF, NECK_HALF = 8, 2


def blank():
    return [[False] * W for _ in range(H)]


def fill_col(m, x, half):
    if x < 0 or x >= W or half <= 0:
        return
    n = int(round(half))
    for y in range(max(0, 12 - n), min(H - 1, 11 + n) + 1):
        m[y][x] = True


def symmetrize(m):
    return [[m[y][x] or m[(H - 1) - y][x] for x in range(W)] for y in range(H)]


def add_collar_and_neck(m):
    for x in range(COLLAR_X0, COLLAR_X1 + 1):
        half = COLLAR_HALF + (1 if x in (1, 6) else -1 if x == 3 else 0)
        fill_col(m, x, half)
    for x in range(NECK_X0, NECK_X1 + 1):
        fill_col(m, x, NECK_HALF)


def head_span():
    return range(HEAD_X0, W)


def _leaf_halfs(hm, power=0.45):
    xs = list(head_span())
    L = xs[-1] - xs[0]
    raw = [((i / L) ** power) * (1 - i / L) for i in range(L + 1)]
    peak = max(raw) or 1.0
    return xs, [hm * r / peak for r in raw]


# ---- heads (side profiles; the 3D cross-section is set in build_tips.py) ----

def head_leaf_spear(m):
    """Broad leaf → lifted lenticular with a midrib (a stiff forged spearhead)."""
    xs, hs = _leaf_halfs(9.0)
    for x, half in zip(xs, hs):
        fill_col(m, x, half)


def head_bodkin(m):
    """Narrow armour-piercing punch: a short shoulder, then a long taper to a
    fine point → lifted as a square (quadrangular) cross-section."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    shoulder = x0 + 6
    for x in xs:
        if x <= shoulder:
            half = 3.6
        else:
            t = (x - shoulder) / (tip - shoulder)
            half = 3.6 * (1 - t)
        fill_col(m, x, half)


def head_estoc(m):
    """Long slender point → lifted rhombic (diamond): four flat facets, a central
    ridge, widest at the midpoint (an estoc / thrusting spike)."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    mid = x0 + (tip - x0) * 0.42
    hm = 5.5
    for x in xs:
        if x <= mid:
            half = hm * (x - x0) / (mid - x0)
        else:
            half = hm * (1 - (x - mid) / (tip - mid))
        fill_col(m, x, max(0.0, half))


def head_broadhead(m):
    """Triangular blade → lifted as a 3-blade broadhead (Y cross-section), with
    two rear-swept barbs."""
    xs = list(head_span())
    base_x, tip = xs[0] + 4, xs[-1]
    base_half = 8.0
    for x in xs:
        if x < base_x:
            continue
        t = (x - base_x) / (tip - base_x)
        fill_col(m, x, base_half * (1 - t))
    for k in range(6):                          # rear barbs at the base corners
        x = xs[0] + k
        outer, inner = 8.5 - 0.4 * k, 3.0 + 0.9 * k
        lo, hi = int(round(CY + inner)), int(round(CY + outer))
        for y in range(min(lo, hi), max(lo, hi) + 1):
            if 0 <= y < H:
                m[y][x] = True


def head_harpoon(m):
    """Leaf with deep backward hooks → lifted lenticular (a flat barbed harpoon)."""
    xs, hs = _leaf_halfs(7.5, power=0.6)
    for x, half in zip(xs, hs):
        fill_col(m, x, half)
    x0 = xs[0]
    for k in range(7):                          # two long rear-swept barbs
        x = x0 + 2 + k
        tip_h = 6.5 + 0.7 * k
        lo, hi = int(round(CY + 2.5)), int(round(CY + tip_h))
        for y in range(lo, hi + 1):
            if 0 <= y < H:
                m[y][x] = True


def head_winged(m):
    """Short stout point → lifted as a 4-blade radial (a + cross-section winged
    pike head)."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    base_half = 7.0
    reach = x0 + int((tip - x0) * 0.8)
    for x in xs:
        if x > reach:
            break
        t = (x - x0) / (reach - x0)
        fill_col(m, x, base_half * (1 - 0.85 * t))


def head_trilobate(m):
    """Slender socketed point → lifted as a solid triangular (poly-3) section:
    the pyramidal 'Scythian' trilobate arrowhead."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    mid = x0 + (tip - x0) * 0.34
    hm = 5.5
    for x in xs:
        half = hm * (x - x0) / (mid - x0) if x <= mid else hm * (1 - (x - mid) / (tip - mid))
        fill_col(m, x, max(0.0, half))


def head_swallowtail(m):
    """Forked/swallowtail head: a broad base that splits into two diverging tines
    with a deep V-notch opening forward (a rope-cutter / flight broadhead)."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    base_x = x0                                     # start at the neck so it welds
    fork = x0 + int((tip - x0) * 0.42)
    base_half = 8.5
    for x in range(base_x, fork):
        fill_col(m, x, base_half * (1 - 0.28 * (x - base_x) / max(1, fork - base_x)))
    for x in range(fork, tip + 1):
        t = (x - fork) / max(1, tip - fork)
        center = base_half * (0.38 + 0.55 * t)      # tine centres diverge outward
        halfw = max(0.6, 2.4 * (1 - t))             # each tine tapers to a point
        for sgn in (-1, 1):
            yc = CY + sgn * center
            for y in range(int(round(yc - halfw)), int(round(yc + halfw)) + 1):
                if 0 <= y < H:
                    m[y][x] = True


def head_winged_spear(m):
    """Leaf-blade boar spear: a lenticular/midrib blade with a round stop-flange
    (the lugs/wings) at the base that keeps it from over-penetrating."""
    xs, hs = _leaf_halfs(8.0)
    for x, half in zip(xs, hs):
        fill_col(m, x, half)
    for x in (12, 13):                              # flange -> revolves to a stop-ring
        fill_col(m, x, 6)


def head_flamberge(m):
    """Flame blade: a slender leaf whose edges undulate down its length."""
    xs = list(head_span())
    x0, tip, L = xs[0], xs[-1], xs[-1] - xs[0]
    hm = 5.6
    for i, x in enumerate(xs):
        t = i / L
        env = hm * ((t + 0.03) ** 0.4) * (1 - t) / 0.33
        wave = 1.0 + 0.26 * math.sin(t * math.pi * 5)
        fill_col(m, x, min(hm, max(0.0, env * wave)))


HEADS = {
    "A-leaf-spear": head_leaf_spear,
    "B-bodkin":     head_bodkin,
    "C-estoc":      head_estoc,
    "D-broadhead":  head_broadhead,
    "E-harpoon":    head_harpoon,
    "F-winged":     head_winged,
    "G-trilobate":  head_trilobate,
    "H-swallowtail": head_swallowtail,
    "I-winged-spear": head_winged_spear,
    "J-flamberge":  head_flamberge,
}


def to_pxg(m) -> str:
    lines = [f"size: {W}x{H}", "[palette]", ". = none",
             "a = 8A6BB6   # silhouette (recolour + cross-section are downstream)",
             "[grid]"]
    for y in range(H):
        lines.append("".join("a" if m[y][x] else "." for x in range(W)))
    return "\n".join(lines) + "\n"


def main():
    (HERE / "src").mkdir(parents=True, exist_ok=True)
    for name, head_fn in HEADS.items():
        m = blank()
        add_collar_and_neck(m)
        head_fn(m)
        m = symmetrize(m)
        (HERE / "src" / f"{name}.pxg").write_text(to_pxg(m))
        print(f"wrote src/{name}.pxg")


if __name__ == "__main__":
    main()
