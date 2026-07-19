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
