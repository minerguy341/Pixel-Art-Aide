"""Auto-generate a STARTER texture laid out for a model's UVs.

Reads every face's UV rectangle from a parsed model and fills it with a
material ramp shaded by the face's direction (top → highlight, sides → base,
bottom → shadow), plus a 1px darker edge so each face reads as a distinct
panel (the Create framed-face idiom). The result maps back onto the model as a
directionally-lit block — a base an artist then refines in .pxg, not a
finished texture. Overlapping UVs are filled once (last face wins) and flagged.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from aide.model import Model
from aide.grid import RGBA, parse_color

# how each face direction maps onto a 5-step ramp [deepshadow, shadow, base, light, highlight]
_FACE_STEP = {"up": 4, "down": 0, "north": 2, "south": 2, "east": 1, "west": 1}


def default_ramp(base_hex: str = "8A6BB5") -> list[RGBA]:
    """Build a 5-step ramp around a base color (aetherium by default)."""
    r, g, b, _ = parse_color(base_hex)
    def scale(f):
        return (max(0, min(255, int(r * f))), max(0, min(255, int(g * f))),
                max(0, min(255, int(b * f))), 255)
    return [scale(0.55), scale(0.72), scale(1.0), scale(1.18), scale(1.34)]


def autotexture(model: Model, ramp: list[RGBA] | None = None,
                frame: bool = True) -> tuple[Image.Image, list[str]]:
    """Return (texture, warnings). Texture is at the model's texture_size."""
    ramp = ramp or default_ramp()
    tw, th = model.texture_size
    img = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    warnings = []
    painted = Image.new("1", (tw, th), 0)
    pd = ImageDraw.Draw(painted)

    faces = [(el, dirn, f) for el in model.elements for dirn, f in el.faces.items()]
    for el, dirn, face in faces:
        u1, v1, u2, v2 = face.uv
        x0, y0 = int(min(u1, u2)), int(min(v1, v2))
        x1, y1 = int(round(max(u1, u2))), int(round(max(v1, v2)))
        if x1 <= x0 or y1 <= y0:
            continue
        step = _FACE_STEP.get(dirn, 2)
        fill = ramp[step]
        # overlap check
        for yy in range(y0, y1):
            for xx in range(x0, x1):
                if 0 <= xx < tw and 0 <= yy < th and painted.getpixel((xx, yy)):
                    warnings.append(f"UV overlap at ({xx},{yy}) — {dirn} face of "
                                    f"'{el.name or 'element'}' overwrites another face")
                    break
            else:
                continue
            break
        d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=fill)
        pd.rectangle([x0, y0, x1 - 1, y1 - 1], fill=1)
        if frame and (x1 - x0) >= 3 and (y1 - y0) >= 3:
            edge = ramp[max(0, step - 1)]
            d.rectangle([x0, y0, x1 - 1, y1 - 1], outline=edge)
            # a lit top-left inner highlight pixel
            d.point((x0 + 1, y0 + 1), fill=ramp[min(4, step + 1)])

    # dedupe warnings, keep concise
    seen, uniq = set(), []
    for w in warnings:
        k = w.split(" — ")[1]
        if k not in seen:
            seen.add(k)
            uniq.append(w)
    return img, uniq
