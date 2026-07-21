#!/usr/bin/env python3
"""r2: 8 MORE plank candidates — all BOARD STYLE (horizontal boards), for greatwood + silverwood.

Stays in the board family (no basketweave/diagonal); varies board rhythm, seam/groove treatment,
and edge detail. Palette-parameterised, recoloured per wood. Reuses make_planks renderers
(tiled/block/slab/stair). Deterministic.
"""
import make_planks as MP
from PIL import Image

GW, SW, N = MP.GW, MP.SW, MP.N
h2, blank = MP.h2, MP.blank


def boards(pal, spec, phases, grain=0.34, sh_p=0.26, hi_p=0.20, seam="dark",
           groove=False, batten=False, pegs=False, checks=False, joint="full", seed=1):
    """spec: list of (height, kind) summing to 16; kind in {'board','batten'}.
    Grain runs ALONG the board (horizontal broken streaks), per wood grammar."""
    dk, sh, bs, hi = pal["dk"], pal["sh"], pal["bs"], pal["hi"]
    im = blank()
    px = im.load()
    ys, y = [], 0
    for (h, kind) in spec:
        ys.append((y, h, kind))
        y += h
    for bi, (y0, bh, kind) in enumerate(ys):
        if kind == "batten":                              # raised thin cover strip
            for ry in range(bh):
                for x in range(N):
                    px[x, y0 + ry] = hi if ry == 0 else (sh if ry == bh - 1 else bs)
            continue
        for ry in range(bh):                              # board body + HORIZONTAL grain streaks
            rt = h2(bi, ry, seed)                          # is this row a grain streak?
            tone = sh if rt < grain * sh_p / 0.26 else (hi if rt > 1 - grain * hi_p / 0.20 else None)
            for x in range(N):
                c = bs
                if tone is not None and h2(x // 4, bi * 7 + ry, seed + 2) < 0.72:
                    c = tone                              # broken run along the board length
                px[x, y0 + ry] = c
        # seam row (board top)
        if seam == "dark":
            for x in range(N):
                px[x, y0] = dk if ((x + bi) % 4) else sh
        elif seam == "tight":
            for x in range(N):
                px[x, y0] = sh
        elif seam == "channel":                           # shiplap: shadow gap + lit lip below
            for x in range(N):
                px[x, y0] = dk
                if bh >= 3:
                    px[x, y0 + 1] = hi
        if groove and bh >= 4:                            # V-groove: lit top, dark valley bottom
            for x in range(N):
                px[x, y0 + 1] = hi
                px[x, y0 + bh - 1] = sh
                px[x, y0] = dk
        if checks:                                        # weathered hairline checks along grain
            for x in range(N):
                if bh >= 3 and h2(x, bi, seed + 5) < 0.06:
                    px[x, y0 + bh // 2] = sh if h2(x, bi, seed + 6) < 0.5 else dk
        # staggered board-end joints
        if joint == "none":
            jxs = ()
        elif joint == "subtle":
            jxs = (phases[bi % len(phases)] % N,)          # one faint joint
        else:
            p = phases[bi % len(phases)]
            jxs = (p % N, (p + 8) % N)
        for jx in jxs:
            for ry in range(1, bh):
                px[jx, y0 + ry] = sh
            if pegs and bh >= 3:                           # small dowel peg at the joint
                py = y0 + bh // 2
                px[jx, py] = hi
                px[(jx + 1) % N, py] = sh
                px[jx, (py + 1) % N] = sh
    return im


B = "board"
BT = "batten"


def arrangements(pal):
    return {
        "randomwidth": boards(pal, [(3, B), (5, B), (2, B), (6, B)], [2, 6, 10], seed=11),
        "shiplap": boards(pal, [(4, B)] * 4, [2, 6], seam="channel", seed=12),
        "vgroove": boards(pal, [(4, B)] * 4, [3, 9], groove=True, seed=13),
        "tightclean": boards(pal, [(4, B)] * 4, [4, 12], grain=0.16, seam="tight",
                             joint="subtle", seed=14),
        "pegged": boards(pal, [(4, B)] * 4, [2, 6], pegs=True, seed=15),
        "widegrain": boards(pal, [(8, B), (8, B)], [2, 10], grain=0.55, sh_p=0.32, hi_p=0.26, seed=16),
        "boardbatten": boards(pal, [(6, B), (2, BT), (6, B), (2, BT)], [3, 9], seed=17),
        "weathered": boards(pal, [(4, B)] * 4, [1, 5, 9, 13], checks=True, sh_p=0.30, seed=18),
    }


LABELS = {
    "randomwidth": "1  random-width - mixed board heights (natural)",
    "shiplap": "2  shiplap - recessed shadow channel between boards",
    "vgroove": "3  v-groove - tongue-&-groove bevel per board",
    "tightclean": "4  tight-clean - smooth wide boards, minimal grain",
    "pegged": "5  pegged - board-end dowel pegs",
    "widegrain": "6  wide-grain - tall boards, prominent grain runs",
    "boardbatten": "7  board-and-batten - wide board + raised batten",
    "weathered": "8  weathered - hairline checks along the grain",
}


def main():
    for wood, pal in (("greatwood", GW), ("silverwood", SW)):
        arr = arrangements(pal)
        for key, img in arr.items():
            name = f"{wood}_planks_{key}_r2"
            (MP.SRC / f"{name}.pxg").write_text(MP.G.to_text(MP.G.from_image(img)))
            MP.G.save_texture(img, MP.OUT / f"{name}.png")
        rows = [MP.row(arr[k], LABELS[k]) for k in LABELS]
        MP.sheet(f"{wood.upper()} PLANKS r2 - 8 board-style candidates (tiled | block | slab | stair)",
                 rows, MP.PREV / f"sheet-{wood}-planks-r2.png")


if __name__ == "__main__":
    main()
