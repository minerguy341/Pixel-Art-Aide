"""Author six wand/sword pommel silhouettes — the counter-weight knob at the
BUTT of the wand. Types follow the Oakeshott families: wheel/disc, sphere,
pear, scent-stopper (faceted), crescent, and an onion/mushroom knob.

A pommel attaches by a short neck where the shaft/tang enters, then a knob body.
Run from repo root:  python3 gallery/2026-07-21-pommels/make_pommels.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # gallery/_archive/ for capkit

from capkit import CY, H, add_collar, blank, circle_halfs, fill_col, symmetrize, to_pxg

HERE = Path(__file__).resolve().parent
BODY_X0 = 15


def collar(m):
    """A small shaft stub (pommels aren't ferruled like the tip caps)."""
    add_collar(m, collar_x1=6, neck_x1=15, collar_half=4, neck_half=2, rings=False)


def wheel(m):
    """Disc / wheel pommel: a tall, thin lens revolved into a flat wheel."""
    cx, ax, ay = 20, 6, 9
    for x in range(cx - ax, cx + ax + 1):
        fill_col(m, x, ay * math.sqrt(max(0.0, 1 - ((x - cx) / ax) ** 2)))


def sphere(m):
    """Spherical (oblate) pommel."""
    for x, h in zip(*circle_halfs(22, 9)):
        fill_col(m, x, h)


def pear(m):
    """Pear / conical pommel: narrow at the neck, swelling to a rounded far end."""
    x0, x1 = BODY_X0, 33
    for x in range(13, x0 + 2):                # stem so the taper welds to the neck
        fill_col(m, x, 2.6)
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        # small at the neck, fattest ~70% out, rounded tail
        half = 9 * math.sin(min(1.0, t * 1.15) * math.pi * 0.5) ** 1.3
        if t > 0.85:
            half *= math.sqrt(max(0.0, 1 - ((t - 0.85) / 0.15) ** 2))
        fill_col(m, x, half)


def scent_stopper(m):
    """Scent-stopper pommel: a faceted bottle shape (lifted poly-6)."""
    x0, x1 = BODY_X0, 32
    for x in range(x0, x1 + 1):
        t = (x - x0) / (x1 - x0)
        if t < 0.55:
            half = 3.5 + 5.0 * t          # shoulders swell out
        else:
            half = 6.25 * (1 - (t - 0.55) / 0.45)   # taper to the stopper tip
        fill_col(m, x, max(0.0, half))


def crescent(m):
    """Crescent pommel (flat blade)."""
    ox, orad, ix, irad = 22.0, 9.5, 26.5, 8.0
    for y in range(H):
        for x in range(BODY_X0 - 3, W_END):
            do = (x - ox) ** 2 + (y - CY) ** 2
            di = (x - ix) ** 2 + (y - CY) ** 2
            if do <= orad * orad and di > irad * irad:
                m[y][x] = True


def mushroom(m):
    """Onion / mushroom knob: a waisted stem flaring to a domed cap."""
    x0 = BODY_X0
    for x in range(x0, 34):
        t = (x - x0) / (34 - x0)
        if t < 0.35:
            half = 3.0 + 2.0 * t          # slim stem
        else:
            u = (t - 0.35) / 0.65         # dome
            half = 3.7 + 6.0 * math.sin(u * math.pi) ** 0.8
            if u > 0.8:
                half *= math.sqrt(max(0.0, 1 - ((u - 0.8) / 0.2) ** 2))
        fill_col(m, x, max(0.0, half))


W_END = 40
BODIES = {
    "A-wheel":         wheel,
    "B-sphere":        sphere,
    "C-pear":          pear,
    "D-scent-stopper": scent_stopper,
    "E-crescent":      crescent,
    "F-mushroom":      mushroom,
}


def main():
    (HERE / "src").mkdir(parents=True, exist_ok=True)
    for name, fn in BODIES.items():
        m = blank()
        collar(m)
        fn(m)
        m = symmetrize(m)
        (HERE / "src" / f"{name}.pxg").write_text(to_pxg(m, note="pommel"))
        print(f"wrote src/{name}.pxg")


if __name__ == "__main__":
    main()
