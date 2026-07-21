"""Generate the 7 wand-cap silhouette profiles (A–G) as .pxg sources.

Each cap is a SIDE VIEW: a ringed ferrule collar (left) + a short neck + a
decorative head (right), drawn about a horizontal centreline (the wand-shaft
axis). These are the *2D* sources; `aide.lift` infers the third dimension from
them (revolve for round heads, blade for flat heads).

Geometry is authored analytically here so it's precise and easy to tweak; the
emitted .pxg files are the editable source of record. Silhouette only — a single
opaque colour per family; lifting/texturing happens downstream.

Run from repo root:  python3 gallery/2026-07-21-wand-caps/make_profiles.py
"""

from __future__ import annotations

import math
from pathlib import Path

W, H = 46, 24
CY = (H - 1) / 2.0            # centreline row (11.5)
HERE = Path(__file__).resolve().parent

# collar / neck geometry shared by every cap
COLLAR_X0, COLLAR_X1 = 0, 8   # ferrule columns
NECK_X0, NECK_X1 = 9, 12      # thin neck columns
HEAD_X0 = 13                  # heads start here
COLLAR_HALF = 8               # ferrule half-height
NECK_HALF = 2


def blank():
    return [[False] * W for _ in range(H)]


def fill_col(m, x, half):
    """Fill column x symmetric about the centreline to +/- half."""
    if x < 0 or x >= W or half <= 0:
        return
    lo = int(round(CY - half))
    hi = int(round(CY + half))
    for y in range(max(0, lo), min(H - 1, hi) + 1):
        m[y][x] = True


def add_collar_and_neck(m):
    for x in range(COLLAR_X0, COLLAR_X1 + 1):
        # subtle rings: two raised lips and one groove for a turned look
        half = COLLAR_HALF
        if x in (1, 6):
            half = COLLAR_HALF + 1
        elif x in (3,):
            half = COLLAR_HALF - 1
        fill_col(m, x, half)
    for x in range(NECK_X0, NECK_X1 + 1):
        fill_col(m, x, NECK_HALF)


def head_span():
    return range(HEAD_X0, W)


# ---- revolve heads (round in cross-section) -------------------------------

def head_spearhead(m):
    """A: leaf-blade — widest a third of the way out, pointed tip."""
    xs = list(head_span())
    L = xs[-1] - xs[0]
    Hm = 9.0
    raw = [((i / L) ** 0.45) * (1 - i / L) for i in range(L + 1)]
    peak = max(raw) or 1.0
    for i, x in enumerate(xs):
        fill_col(m, x, Hm * raw[i] / peak)


def head_flame(m):
    """D: teardrop — round bulb near the neck, drawn to a point."""
    xs = list(head_span())
    xb, Rb = 21, 9.0                 # bulb centre / radius
    xtip = xs[-1]
    for x in xs:
        if x <= xb:
            d = x - xb
            half = math.sqrt(max(0.0, Rb * Rb - d * d))
        else:
            t = (x - xb) / (xtip - xb)
            half = Rb * (1 - t) ** 0.8
        fill_col(m, x, half)


def head_spire(m):
    """F: faceted spire — a thin, long double-cone (spindle when revolved)."""
    xs = list(head_span())
    mid = (xs[0] + xs[-1]) / 2.0
    Hm = 5.0
    for x in xs:
        t = 1 - abs(x - mid) / (mid - xs[0])
        fill_col(m, x, Hm * max(0.0, t))


# ---- blade heads (flat, forged) -------------------------------------------

def head_broadhead(m):
    """E: broadhead arrow — a triangle to a point, with two swept-back barbs."""
    xs = list(head_span())
    base_x, tip_x = xs[0] + 4, xs[-1]
    base_half = 7.5
    for x in xs:
        if x < base_x:
            continue
        t = (x - base_x) / (tip_x - base_x)
        fill_col(m, x, base_half * (1 - t))
    # two solid barbs sweeping back from the base corners toward the neck
    for k in range(6):
        x = xs[0] + k
        outer = 8.5 - k * 0.4          # tip of the barb, near the base corner
        inner = 3.0 + k * 0.9          # inner edge sweeps in toward the shaft
        for sgn in (-1, 1):
            lo = int(round(CY + sgn * inner))
            hi = int(round(CY + sgn * outer))
            for y in range(min(lo, hi), max(lo, hi) + 1):
                if 0 <= y < H:
                    m[y][x] = True


def head_crescent(m):
    """B: crescent — outer disc minus a right-shifted inner disc (opens right)."""
    ox, orad = 24.0, 11.0
    ix, irad = 29.0, 9.2
    for y in range(H):
        for x in head_span():
            do = (x - ox) ** 2 + (y - CY) ** 2
            di = (x - ix) ** 2 + (y - CY) ** 2
            if do <= orad * orad and di > irad * irad:
                m[y][x] = True


def head_trident(m):
    """C: trident — a base bar and three pronged tines with pointed tips."""
    xs = list(head_span())
    x0 = xs[0]
    # base bar
    for x in range(x0, x0 + 4):
        fill_col(m, x, 9)
    tips_x = xs[-1]
    prongs = [0.0, 8.0, -8.0]        # centre offset of each tine
    for off in prongs:
        yc = CY + off
        reach = tips_x - (x0 + 3) - (2 if off else 0)
        end = x0 + 3 + reach
        for x in range(x0 + 3, end + 1):
            t = (x - (x0 + 3)) / max(1, end - (x0 + 3))
            half = 1.6 * (1 - t) + 0.4     # taper to a point
            lo = int(round(yc - half))
            hi = int(round(yc + half))
            for y in range(max(0, lo), min(H - 1, hi) + 1):
                m[y][x] = True


def head_fleur(m):
    """G: fleur finial — a central pointed leaf flanked by two curved barbs."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    # central leaf
    L = tip - x0
    for i, x in enumerate(xs):
        t = i / L
        half = 6.0 * ((t + 0.05) ** 0.5) * (1 - t) / 0.30
        fill_col(m, x, min(6.0, half))
    # two side barbs curving up/out from the base, like a fleur-de-lis
    for sgn in (-1, 1):
        for k in range(9):
            x = x0 + 2 + k
            rise = 3.0 + 2.4 * math.sin(min(1.0, k / 8.0) * math.pi * 0.75)
            y = CY + sgn * (3.0 + rise * (k / 8.0) ** 0.6)
            for yy in (int(round(y)), int(round(y)) + sgn):
                if 0 <= yy < H:
                    m[yy][x] = True


HEADS = {
    "A-spearhead": (head_spearhead, "revolve"),
    "B-crescent":  (head_crescent, "blade"),
    "C-trident":   (head_trident, "blade"),
    "D-flame":     (head_flame, "revolve"),
    "E-broadhead": (head_broadhead, "blade"),
    "F-spire":     (head_spire, "revolve"),
    "G-fleur":     (head_fleur, "blade"),
}


def to_pxg(m, mode: str) -> str:
    lines = [
        f"# wand-cap silhouette — lift mode: {mode}",
        f"size: {W}x{H}",
        "[palette]",
        ". = none",
        "a = 8A6BB6   # AETHERIUM base (silhouette only; family recolour is downstream)",
        "[grid]",
    ]
    for y in range(H):
        lines.append("".join("a" if m[y][x] else "." for x in range(W)))
    return "\n".join(lines) + "\n"


def main():
    (HERE / "src").mkdir(exist_ok=True)
    for name, (head_fn, mode) in HEADS.items():
        m = blank()
        add_collar_and_neck(m)
        head_fn(m)
        (HERE / "src" / f"{name}.pxg").write_text(to_pxg(m, mode))
        print(f"wrote src/{name}.pxg  ({mode})")


if __name__ == "__main__":
    main()
