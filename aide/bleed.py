"""Alpha bleed — fill transparent pixels with their nearest opaque neighbor's
RGB while keeping alpha at 0.

Minecraft generates mipmaps by averaging 2x2 blocks *including the RGB stored
under alpha-0 pixels*. If transparent pixels hold black (our .pxg `none` =
(0,0,0,0)), distant cutout textures (leaves, glass, plants) grow dark halos.
Bleeding the edge color outward makes the mip average correct. Purely a
distance-correctness fix: nothing changes at 1x since alpha stays 0.

See knowledge/lessons.md "fill transparent pixels with neighbour RGB".
"""

from __future__ import annotations

from PIL import Image


def alpha_bleed(img: Image.Image, max_passes: int = 32) -> Image.Image:
    """Return a copy whose alpha-0 pixels carry the averaged RGB of adjacent
    opaque/already-filled pixels. Alpha channel is untouched."""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    out = img.copy()
    op = out.load()

    # "known" = has real coverage (alpha>0) or has been filled this run
    known = [[px[x, y][3] > 0 for x in range(w)] for y in range(h)]
    remaining = sum(row.count(False) for row in known)
    if remaining in (0, w * h):
        return out  # nothing transparent, or nothing opaque to bleed from

    neigh = [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]
    for _ in range(max_passes):
        if remaining == 0:
            break
        newly = []
        for y in range(h):
            for x in range(w):
                if known[y][x]:
                    continue
                r = g = b = n = 0
                for dx, dy in neigh:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < w and 0 <= ny < h and known[ny][nx]:
                        c = op[nx, ny]
                        r += c[0]; g += c[1]; b += c[2]; n += 1
                if n:
                    newly.append((x, y, (r // n, g // n, b // n)))
        if not newly:
            break  # disconnected transparent region; leave as-is
        for x, y, rgb in newly:
            op[x, y] = (rgb[0], rgb[1], rgb[2], 0)  # keep fully transparent
            known[y][x] = True
        remaining -= len(newly)
    return out
