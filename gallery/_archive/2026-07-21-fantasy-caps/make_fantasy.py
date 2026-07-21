"""Author six fantasy wand-cap silhouettes — the orb/crystal/moon vibe of magic
wand toppers (crystal-ball finials, faceted gem points, starbursts, crescent
moons, a gem in a flared setting, and an ornate beaded finial).

The 3D cross-section per cap is chosen in build_fantasy.py.
Run from repo root:  python3 gallery/2026-07-21-fantasy-caps/make_fantasy.py
"""

from __future__ import annotations

import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # gallery/_archive/ for capkit

from capkit import (CY, H, add_collar, blank, circle_halfs, fill_col,
                    head_span, symmetrize, to_pxg)

HERE = Path(__file__).resolve().parent


def orb(m):
    """Crystal-ball finial: a short stem carrying a sphere."""
    cx, r = 29, 9
    for x in range(13, cx - r + 2):
        fill_col(m, x, 2.5)
    for x, h in zip(*circle_halfs(cx, r)):
        fill_col(m, x, h)


def crystal(m):
    """Quartz point: a hexagonal prism drawn to a pyramidal tip (lifted poly-6)."""
    xs = list(head_span())
    x0, tip, L = xs[0], xs[-1], xs[-1] - xs[0]
    hm = 6.5
    for x in xs:
        t = (x - x0) / L
        if t < 0.2:
            half = hm * t / 0.2
        elif t < 0.62:
            half = hm
        else:
            half = hm * (1 - (t - 0.62) / 0.38)
        fill_col(m, x, max(0.0, half))


def starburst(m):
    """A pointed body lifted as a 6-blade radial star."""
    xs = list(head_span())
    x0, tip = xs[0], xs[-1]
    mid = x0 + (tip - x0) * 0.34
    hm = 8.0
    for x in xs:
        half = hm * (x - x0) / (mid - x0) if x <= mid else hm * (1 - (x - mid) / (tip - mid))
        fill_col(m, x, max(0.0, half))


def moon(m):
    """Ornate crescent moon (flat blade), with a small bead at each horn tip."""
    ox, orad, ix, irad = 25.0, 11.0, 30.0, 9.3
    for y in range(H):
        for x in head_span():
            do = (x - ox) ** 2 + (y - CY) ** 2
            di = (x - ix) ** 2 + (y - CY) ** 2
            if do <= orad * orad and di > irad * irad:
                m[y][x] = True
    for cx, cyo in ((22, CY - 9.5), (22, CY + 9.5)):     # horn-tip beads
        for x in head_span():
            for y in range(H):
                if (x - cx) ** 2 + (y - cyo) ** 2 <= 4:
                    m[y][x] = True


def gem_setting(m):
    """A gem cradled in a flared setting: a cup that opens outward, then a sphere."""
    for x in range(13, 21):                               # flared cup (cone)
        fill_col(m, x, 2 + (x - 13) * 0.8)
    for x in range(20, 24):                               # short waist / claws
        fill_col(m, x, 2.4)
    for x, h in zip(*circle_halfs(31, 8)):                # the gem
        fill_col(m, x, h)


def beaded(m):
    """Turned ornate finial: a tapering stack of beads ending in a point."""
    xs = list(head_span())
    x0, L = xs[0], xs[-1] - xs[0]
    hm = 6.0
    for x in xs:
        t = (x - x0) / L
        env = hm * (1 - 0.75 * t)
        bead = 0.55 + 0.45 * abs(math.sin(t * math.pi * 4))
        half = env * bead
        if t > 0.9:                                        # draw to a point
            half *= (1 - t) / 0.1
        fill_col(m, x, max(0.0, half))


HEADS = {
    "A-orb":         orb,
    "B-crystal":     crystal,
    "C-starburst":   starburst,
    "D-moon":        moon,
    "E-gem-setting": gem_setting,
    "F-beaded":      beaded,
}


def main():
    (HERE / "src").mkdir(parents=True, exist_ok=True)
    for name, fn in HEADS.items():
        m = blank()
        add_collar(m)
        fn(m)
        m = symmetrize(m)
        (HERE / "src" / f"{name}.pxg").write_text(to_pxg(m, note="fantasy cap"))
        print(f"wrote src/{name}.pxg")


if __name__ == "__main__":
    main()
