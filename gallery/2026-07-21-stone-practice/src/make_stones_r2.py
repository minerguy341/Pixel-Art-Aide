#!/usr/bin/env python3
"""Regular stones only (no magic): refine shale, keep marble/slate, add granite/basalt/sandstone —
a practice set spanning the rock classes with the geology lessons applied. Reuses make_stones helpers.
"""
import make_stones as MS

hx, blank, h2, speckle, vein = MS.hx, MS.blank, MS.h2, MS.speckle, MS.vein
N = MS.N


# reuse the strong ones
marble = MS.marble
slate = MS.slate


def shale():
    """Refined: soft dark layered mudstone — thin BROKEN laminae, minimal flecks, no brick rhythm (L1)."""
    im, px = blank()
    base = (hx(0x322F31), hx(0x3E3B3D), hx(0x4A474A))
    # very low-contrast mottle base
    for y in range(N):
        for x in range(N):
            g = 0.6 * h2(x, y // 2, 91) + 0.4 * h2(x, y, 92)
            px[x, y] = base[0] if g < 0.16 else (base[2] if g > 0.86 else base[1])
    # thin, broken, slightly wavy laminae (not every-row, not full-width)
    for ly in (2, 7, 12):
        for x in range(N):
            yy = (ly + (1 if h2(x // 3, ly, 93) < 0.3 else 0)) % N
            if h2(x, ly, 94) < 0.62:
                px[x, yy] = hx(0x2A272A)
    return im


def granite():
    """Felsic plutonic salt-and-pepper — several DISTINCT mineral colours (S4 exception), busy but clustered."""
    im, px = blank()
    base, feld, qtz, mica, white = (hx(0xB4ADA6), hx(0xC6A79A), hx(0x9A9A93), hx(0x3A3532), hx(0xDCD8D0))
    for y in range(N):
        for x in range(N):
            g = h2(x, y, 101)
            px[x, y] = base
            if g < 0.10:
                px[x, y] = mica          # black mica specks
            elif g < 0.24:
                px[x, y] = feld          # pink feldspar
            elif g < 0.31:
                px[x, y] = white
            elif g < 0.40:
                px[x, y] = qtz
    # nudge a few 2px feldspar clusters so it reads crystalline, not pure noise
    for (cx, cy) in [(3, 4), (10, 3), (6, 11), (12, 12)]:
        px[cx, cy] = feld
        px[(cx + 1) % N, cy] = feld
    return im


def basalt():
    """Mafic volcanic — dark, fine, near-flat, low busyness, a few vesicle pits."""
    im, px = blank()
    base = (hx(0x26302A)[:3] + (255,), hx(0x2F3A32), hx(0x3A463C))  # dark grey, faint green-grey
    speckle(px, base, 111, p_lo=0.14, p_hi=0.08)
    for (vx, vy) in [(4, 3), (11, 6), (7, 11), (13, 13), (2, 9)]:
        px[vx, vy] = hx(0x171D18)                       # vesicle pit
        px[(vx + 1) % N, vy] = hx(0x202821)
    return im


def sandstone():
    """Sedimentary — warm pale tan, fine grains + faint horizontal bedding lines."""
    im, px = blank()
    base = (hx(0xC8AE76), hx(0xD8C088), hx(0xE6D29C))
    speckle(px, base, 121, p_lo=0.16, p_hi=0.14)
    for by in (3, 8, 13):                               # faint bedding
        for x in range(N):
            if h2(x, by, 122) < 0.5:
                px[x, by] = hx(0xC2A76C)
    return im


def main():
    stones = {
        "marble": marble(), "slate": slate(), "shale": shale(),
        "granite": granite(), "basalt": basalt(), "sandstone": sandstone(),
    }
    for name, img in stones.items():
        (MS.SRC / f"{name}_r2.pxg").write_text(MS.G.to_text(MS.G.from_image(img)))
        MS.G.save_texture(img, MS.OUT / f"{name}_r2.png")
    labels = {
        "marble": "marble - pale calcite + wandering grey veins",
        "slate": "slate - cool blue-grey foliation + mica flecks",
        "shale": "shale - soft dark mudstone, thin broken laminae",
        "granite": "granite - felsic salt-and-pepper (pink feldspar/quartz/mica)",
        "basalt": "basalt - mafic dark, near-flat, vesicle pits",
        "sandstone": "sandstone - warm tan grains + faint bedding",
    }
    rows = [MS.row(stones[k], labels[k]) for k in ["marble", "slate", "shale", "granite", "basalt", "sandstone"]]
    MS.sheet("REGULAR STONES (no magic) — rock classes, geology lessons applied",
             rows, MS.PREV / "sheet-regular-stones.png")
    print("done")


if __name__ == "__main__":
    main()
