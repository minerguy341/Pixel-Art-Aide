"""Render a parsed Minecraft model (any axis-aligned cuboid shape) in 2:1 iso,
sampling each face's UV region from its texture and applying the exact vanilla
directional face multipliers. Works for cubes, stairs, slabs, pillars, rods,
multi-element item models — anything made of boxes.
"""

from __future__ import annotations

from PIL import Image, ImageDraw

from aide.model import Model, NORMALS

# vanilla "diffuse lighting" per face direction
SHADE = {"up": 1.0, "down": 0.5, "north": 0.8, "south": 0.8, "east": 0.6, "west": 0.6}
# camera looks from the (+X,+Y,+Z) octant toward the origin
VIEW = (1.0, 1.0, 1.0)


def _corners(el, d):
    """4 model-space corners of face `d` in texture order [tl,tr,br,bl]."""
    x0, y0, z0 = el.frm
    x1, y1, z1 = el.to
    return {
        "down":  [(x0, y0, z1), (x1, y0, z1), (x1, y0, z0), (x0, y0, z0)],
        "up":    [(x0, y1, z0), (x1, y1, z0), (x1, y1, z1), (x0, y1, z1)],
        "north": [(x1, y1, z0), (x0, y1, z0), (x0, y0, z0), (x1, y0, z0)],
        "south": [(x0, y1, z1), (x1, y1, z1), (x1, y0, z1), (x0, y0, z1)],
        "west":  [(x0, y1, z0), (x0, y1, z1), (x0, y0, z1), (x0, y0, z0)],
        "east":  [(x1, y1, z1), (x1, y1, z0), (x1, y0, z0), (x1, y0, z1)],
    }[d]


def _shade(c, f):
    return (int(c[0] * f), int(c[1] * f), int(c[2] * f), c[3])


def _lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def _bilerp(tl, tr, br, bl, a, b):
    top = _lerp(tl, tr, a)
    bot = _lerp(bl, br, a)
    return _lerp(top, bot, b)


def render_model(model: Model, textures: dict[str, Image.Image], scale: int = 12,
                 tints: dict[int, tuple] | None = None, pad_frac: float = 0.12) -> Image.Image:
    tints = tints or {}
    imgs = {k: v.convert("RGBA") for k, v in textures.items()}
    tw, th = model.texture_size
    s = scale / 16.0  # pixels per model unit (so a 16-unit block ~ `scale`px/tile)
    S = scale

    def P(pt):
        X, Y, Z = pt
        return (ox + (X - Z) * s, oy + (X + Z) * s * 0.5 - Y * s)

    # all 8 corners of every element, projected with origin 0, to size the canvas
    corners_all = []
    for el in model.elements:
        x0, y0, z0 = el.frm
        x1, y1, z1 = el.to
        for X in (x0, x1):
            for Y in (y0, y1):
                for Z in (z0, z1):
                    corners_all.append((X, Y, Z))
    sx = [(p[0] - p[2]) * s for p in corners_all]
    sy = [(p[0] + p[2]) * s * 0.5 - p[1] * s for p in corners_all]
    pad = max(4, int(pad_frac * S))
    W = int(max(sx) - min(sx)) + 2 * pad
    H = int(max(sy) - min(sy)) + 2 * pad
    ox, oy = -min(sx) + pad, -min(sy) + pad

    out = Image.new("RGBA", (max(1, W), max(1, H)), (0, 0, 0, 0))
    d = ImageDraw.Draw(out, "RGBA")

    # collect visible faces with a depth key, then painter-sort far->near
    faces = []
    for el in model.elements:
        for dirn, face in el.faces.items():
            n = NORMALS[dirn]
            if n[0] * VIEW[0] + n[1] * VIEW[1] + n[2] * VIEW[2] <= 0:
                continue  # backface
            corners = _corners(el, dirn)
            cx = sum(c[0] for c in corners) / 4
            cy = sum(c[1] for c in corners) / 4
            cz = sum(c[2] for c in corners) / 4
            depth = cx + cy + cz  # larger = nearer to camera
            faces.append((depth, el, dirn, face, corners))
    faces.sort(key=lambda f: f[0])

    def lookup(face):
        key = face.texture.lstrip("#")
        if key in imgs:            # provided by texture key ("0", "all", "side")
            return imgs[key]
        path = model.resolve_texture("#" + key)  # follow ref chain to a path
        if path and path in imgs:
            return imgs[path]
        return imgs.get("__single__")  # single-texture fallback

    for _, el, dirn, face, corners in faces:
        tex = lookup(face)
        if tex is None:
            continue
        px = tex.load()
        tl, tr, br, bl = [P(c) for c in _corners_rot(corners, face.rotation)]
        u1, v1, u2, v2 = face.uv
        du, dv = (u2 - u1), (v2 - v1)
        if du == 0 or dv == 0:
            continue
        # scale UV (in texture_size units) to the texture's pixel grid
        su, sv = tex.width / tw, tex.height / th
        tu1, tu2 = u1 * su, u2 * su
        tv1, tv2 = v1 * sv, v2 * sv
        umin, umax = sorted((tu1, tu2))
        vmin, vmax = sorted((tv1, tv2))
        shade = SHADE[dirn]
        tint = tints.get(face.tintindex) if face.tintindex is not None else None
        for ty in range(int(vmin), int(round(vmax))):
            fb0 = (ty - tv1) / (tv2 - tv1)
            fb1 = (ty + 1 - tv1) / (tv2 - tv1)
            for tx in range(int(umin), int(round(umax))):
                if not (0 <= tx < tex.width and 0 <= ty < tex.height):
                    continue
                c = px[tx, ty]
                if c[3] == 0:
                    continue
                if tint:
                    c = (c[0]*tint[0]//255, c[1]*tint[1]//255, c[2]*tint[2]//255, c[3])
                fa0 = (tx - tu1) / (tu2 - tu1)
                fa1 = (tx + 1 - tu1) / (tu2 - tu1)
                quad = [_bilerp(tl, tr, br, bl, fa0, fb0),
                        _bilerp(tl, tr, br, bl, fa1, fb0),
                        _bilerp(tl, tr, br, bl, fa1, fb1),
                        _bilerp(tl, tr, br, bl, fa0, fb1)]
                d.polygon(quad, fill=_shade(c, shade))
    return out


def render_door(bottom: Image.Image, top: Image.Image, scale: int = 12) -> Image.Image:
    """Render a full 2-tall door (vanilla geometry) from its two 16x16 halves."""
    from aide.model import door_model
    return render_model(door_model(), {"bottom": bottom, "top": top}, scale=scale)


def _corners_rot(corners, rotation):
    """Rotate the [tl,tr,br,bl] corner list by a face UV rotation (0/90/180/270)."""
    r = (rotation // 90) % 4
    for _ in range(r):
        corners = [corners[3], corners[0], corners[1], corners[2]]
    return corners
