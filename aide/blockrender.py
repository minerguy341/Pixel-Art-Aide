"""Isometric block renderer — vanilla inventory-icon style previews.

Projects square face textures onto a 2:1 dimetric cube: top face full
brightness, left face ~82%, right face ~62% (Minecraft's icon shading).
Each texel is drawn as a filled quad, so pixels stay crisp at any scale.
Cutout texels (alpha 0) are skipped; the hole shows through, which matches
how leaf-block icons read.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

# Exact vanilla directional face multipliers (Minecraft "diffuse lighting"):
# top Y+ = 1.0, N/S = 0.8, E/W = 0.6, bottom = 0.5. The iso view shows the top
# plus one N/S side (left) and one E/W side (right).
SHADES = (1.0, 0.8, 0.6)  # top, left (N/S), right (E/W)


def _shade(c, f: float):
    return (int(c[0] * f), int(c[1] * f), int(c[2] * f), c[3])


def iso_block(
    top: Image.Image,
    left: Image.Image,
    right: Image.Image | None = None,
    scale: int = 8,
    shades: tuple[float, float, float] = SHADES,
) -> Image.Image:
    """Render one block. All faces must be same-size squares."""
    right = right or left
    n = top.width
    for face in (top, left, right):
        if face.size != (n, n):
            raise ValueError(f"face sizes differ: {face.size} vs {(n, n)}")
    k = scale
    out = Image.new("RGBA", (2 * n * k, 2 * n * k), (0, 0, 0, 0))
    d = ImageDraw.Draw(out)

    def corners_top(u, v):
        return (n * k + (u - v) * k, (u + v) * k / 2)

    def corners_left(u, v):
        return (u * k, n * k / 2 + u * k / 2 + v * k)

    def corners_right(u, v):
        return (n * k + u * k, n * k - u * k / 2 + v * k)

    for face, project, f in ((top, corners_top, shades[0]),
                             (left, corners_left, shades[1]),
                             (right, corners_right, shades[2])):
        px = face.convert("RGBA").load()
        for v in range(n):
            for u in range(n):
                c = px[u, v]
                if c[3] == 0:
                    continue
                quad = [project(u, v), project(u + 1, v), project(u + 1, v + 1), project(u, v + 1)]
                d.polygon(quad, fill=_shade(c, f))
    return out


def iso_stair(top: Image.Image, side: Image.Image, scale: int = 8,
              shades: tuple[float, float, float] = SHADES) -> Image.Image:
    """Render a bottom stair (the block's texture carved into a step), with the
    exact vanilla face multipliers. A stair exposes top + riser + front + side,
    so it shows directional face-shading far more than a cube — the demo shape
    for the 'don't bake a gradient' lesson.

    Geometry in block space: X right, Z depth (0 back .. 1 front), Y up.
    Lower half Y0..0.5 full; upper-back half Y0.5..1 over Z0..0.5.
    """
    n = top.width
    s = scale
    px_top = top.convert("RGBA").load()
    px_side = side.convert("RGBA").load()
    pad = int(0.15 * n * s)
    W = int(2 * n * s) + 2 * pad
    H = int(2 * n * s) + 2 * pad
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(out, "RGBA")
    ox, oy = n * s + pad, n * s + pad  # screen y spans oy-ns .. oy+ns

    def P(X, Y, Z):  # block-space (0..1) -> screen
        return (ox + (X - Z) * n * s, oy + (X + Z) * n * s * 0.5 - Y * n * s)

    def face(sampler, shade, cells):
        """cells: list of (screen quad, texel color) already shaded."""
        for quad, c in cells:
            d.polygon(quad, fill=_shade(c, shade))

    # Each face is drawn as n*n/2-ish texel quads by sampling the texture.
    def top_face(y, z0, z1, tex):  # horizontal, varies X(0..1),Z(z0..1)
        cells = []
        zc = int(round((z1 - z0) * n))
        for i in range(n):          # X texel
            for j in range(zc):     # Z texel
                X0, X1 = i / n, (i + 1) / n
                Z0, Z1 = z0 + j / n, z0 + (j + 1) / n
                quad = [P(X0, y, Z0), P(X1, y, Z0), P(X1, y, Z1), P(X0, y, Z1)]
                cells.append((quad, tex[i, int(z0 * n) + j]))
        face(None, shades[0], cells)

    def front_face(z, y0, y1, tex):  # +Z plane, varies X(0..1), Y(y0..1)
        cells = []
        yc = int(round((y1 - y0) * n))
        for i in range(n):
            for j in range(yc):
                X0, X1 = i / n, (i + 1) / n
                Y0, Y1 = y0 + j / n, y0 + (j + 1) / n
                quad = [P(X0, Y1, z), P(X1, Y1, z), P(X1, Y0, z), P(X0, Y0, z)]
                ty = n - 1 - (int(y0 * n) + j)
                cells.append((quad, tex[i, ty]))
        face(None, shades[1], cells)

    def side_face(x, segments, tex):  # +X plane, list of (z0,z1,y0,y1)
        cells = []
        for (z0, z1, y0, y1) in segments:
            for i in range(int(round((z1 - z0) * n))):
                for j in range(int(round((y1 - y0) * n))):
                    Z0, Z1 = z0 + i / n, z0 + (i + 1) / n
                    Y0, Y1 = y0 + j / n, y0 + (j + 1) / n
                    quad = [P(x, Y1, Z0), P(x, Y1, Z1), P(x, Y0, Z1), P(x, Y0, Z0)]
                    tz = int(z0 * n) + i
                    ty = n - 1 - (int(y0 * n) + j)
                    cells.append((quad, tex[tz, ty]))
        face(None, shades[2], cells)

    # draw back-to-front: side, then fronts, then tops
    side_face(1.0, [(0.0, 1.0, 0.0, 0.5), (0.0, 0.5, 0.5, 1.0)], px_side)
    front_face(0.5, 0.5, 1.0, px_side)   # riser
    front_face(1.0, 0.0, 0.5, px_side)   # lower front
    top_face(1.0, 0.0, 0.5, px_top)      # upper step tread
    top_face(0.5, 0.5, 1.0, px_top)      # lower tread
    return out


def iso_slab(top: Image.Image, side: Image.Image, scale: int = 8, height: float = 0.5,
             shades: tuple[float, float, float] = SHADES) -> Image.Image:
    """Render a bottom slab (a box filling Y0..height) with the vanilla face multipliers.
    Same dimetric projection as iso_stair; shows the top tread + one N/S front + one E/W side."""
    n = top.width
    s = scale
    px_top = top.convert("RGBA").load()
    px_side = side.convert("RGBA").load()
    pad = int(0.15 * n * s)
    side_px = int(2 * n * s) + 2 * pad
    out = Image.new("RGBA", (side_px, side_px), (0, 0, 0, 0))
    d = ImageDraw.Draw(out, "RGBA")
    ox, oy = n * s + pad, n * s + pad

    def P(X, Y, Z):
        return (ox + (X - Z) * n * s, oy + (X + Z) * n * s * 0.5 - Y * n * s)

    hc = int(round(height * n))
    # side x=1 (E/W, shades[2])
    for i in range(n):
        for j in range(hc):
            c = px_side[i, n - 1 - j]
            if c[3] == 0:
                continue
            quad = [P(1, (j + 1) / n, i / n), P(1, (j + 1) / n, (i + 1) / n),
                    P(1, j / n, (i + 1) / n), P(1, j / n, i / n)]
            d.polygon(quad, fill=_shade(c, shades[2]))
    # front z=1 (N/S, shades[1])
    for i in range(n):
        for j in range(hc):
            c = px_side[i, n - 1 - j]
            if c[3] == 0:
                continue
            quad = [P(i / n, (j + 1) / n, 1), P((i + 1) / n, (j + 1) / n, 1),
                    P((i + 1) / n, j / n, 1), P(i / n, j / n, 1)]
            d.polygon(quad, fill=_shade(c, shades[1]))
    # top y=height (shades[0])
    for i in range(n):
        for j in range(n):
            c = px_top[i, j]
            if c[3] == 0:
                continue
            quad = [P(i / n, height, j / n), P((i + 1) / n, height, j / n),
                    P((i + 1) / n, height, (j + 1) / n), P(i / n, height, (j + 1) / n)]
            d.polygon(quad, fill=_shade(c, shades[0]))
    return out


def lineup(blocks: list[tuple[str, Image.Image]], pad: int = 12) -> Image.Image:
    """Labelled row of iso-rendered blocks on the sheet background."""
    from aide.render import SHEET_BG, LABEL_FG

    h = max(im.height for _, im in blocks) + 26 + pad * 2
    w = sum(im.width for _, im in blocks) + pad * (len(blocks) + 1)
    out = Image.new("RGBA", (w, h), SHEET_BG)
    d = ImageDraw.Draw(out)
    x = pad
    for label, im in blocks:
        d.text((x + 2, pad), label, fill=LABEL_FG)
        out.alpha_composite(im, (x, pad + 18))
        x += im.width + pad
    return out
