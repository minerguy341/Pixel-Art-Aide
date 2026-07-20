"""Read a Minecraft Java block/item model's SHAPE — its cuboid elements and
per-face UVs — so we can auto-texture and render it, cube or not.

Handles models with explicit `elements`, and synthesizes the standard element
for the common vanilla `cube*` parents (cube_all / cube_column / cube_bottom_top
/ cube). Element `rotation` (the 22.5°/45° tilts) is parsed into a `Rotation`
and applied by the renderer (origin/axis/angle/rescale); faces with a `rotation`
UV spin are honored.
"""

from __future__ import annotations

import json
import math
from dataclasses import dataclass, field
from pathlib import Path

DIRECTIONS = ("down", "up", "north", "south", "west", "east")
# outward normal per face (model space: X east, Y up, Z south)
NORMALS = {
    "down": (0, -1, 0), "up": (0, 1, 0),
    "north": (0, 0, -1), "south": (0, 0, 1),
    "west": (-1, 0, 0), "east": (1, 0, 0),
}


@dataclass
class Face:
    direction: str
    uv: tuple[float, float, float, float]  # u1,v1,u2,v2 in texture_size space
    texture: str                            # resolved texture key (no '#')
    tintindex: int | None = None
    rotation: int = 0                       # 0/90/180/270 UV rotation


@dataclass
class Rotation:
    """Minecraft element rotation: spin the box `angle`° about `axis` through
    `origin` (model space). `rescale` grows the perpendicular axes by 1/|cos| so
    a tilted element still fills its footprint (vanilla uses it for 22.5°/45°)."""
    origin: tuple[float, float, float]
    axis: str          # "x" | "y" | "z"
    angle: float       # degrees
    rescale: bool = False


def rotate_point(pt, rot: "Rotation | None"):
    """Rotate a model-space point about the rotation's origin/axis (+ rescale)."""
    if rot is None or rot.angle == 0:
        return pt
    ox, oy, oz = rot.origin
    x, y, z = pt[0] - ox, pt[1] - oy, pt[2] - oz
    a = math.radians(rot.angle)
    c, s = math.cos(a), math.sin(a)
    if rot.axis == "x":
        y, z = y * c - z * s, y * s + z * c
    elif rot.axis == "y":
        x, z = x * c + z * s, -x * s + z * c
    else:  # z
        x, y = x * c - y * s, x * s + y * c
    if rot.rescale and c != 0:
        f = 1.0 / abs(c)
        if rot.axis == "x":
            y, z = y * f, z * f
        elif rot.axis == "y":
            x, z = x * f, z * f
        else:
            x, y = x * f, y * f
    return (x + ox, y + oy, z + oz)


def rotate_vec(v, rot: "Rotation | None"):
    """Rotate a direction vector (normal) about the axis only — no origin/rescale."""
    if rot is None or rot.angle == 0:
        return v
    x, y, z = v
    a = math.radians(rot.angle)
    c, s = math.cos(a), math.sin(a)
    if rot.axis == "x":
        return (x, y * c - z * s, y * s + z * c)
    if rot.axis == "y":
        return (x * c + z * s, y, -x * s + z * c)
    return (x * c - y * s, x * s + y * c, z)


@dataclass
class Element:
    frm: tuple[float, float, float]
    to: tuple[float, float, float]
    faces: dict[str, Face] = field(default_factory=dict)
    name: str = ""
    rotation: Rotation | None = None


@dataclass
class Model:
    elements: list[Element]
    texture_size: tuple[int, int] = (16, 16)
    textures: dict[str, str] = field(default_factory=dict)  # key -> path (may be #ref)
    parent: str | None = None

    def resolve_texture(self, key: str) -> str | None:
        """Follow #ref chains in the textures map to a concrete path."""
        seen = set()
        while key and key.startswith("#"):
            key = key[1:]
            if key in seen:
                return None
            seen.add(key)
            key = self.textures.get(key, "")
        return key or None


def _default_uv(frm, to, direction):
    """Vanilla auto-UV for a face when the model omits it (project the box)."""
    x0, y0, z0 = frm
    x1, y1, z1 = to
    if direction in ("north", "south"):
        return (x0, 16 - y1, x1, 16 - y0)
    if direction in ("east", "west"):
        return (z0, 16 - y1, z1, 16 - y0)
    if direction in ("up", "down"):
        return (x0, z0, x1, z1)
    return (0, 0, 16, 16)


def _cube_element(face_tex: dict[str, str]) -> Element:
    frm, to = (0.0, 0.0, 0.0), (16.0, 16.0, 16.0)
    faces = {}
    for d in DIRECTIONS:
        tex = face_tex.get(d)
        if tex:
            faces[d] = Face(d, _default_uv(frm, to, d), tex)
    return Element(frm, to, faces, name="cube")


_CUBE_PARENTS = {
    "cube_all": {d: "#all" for d in DIRECTIONS},
    "cube_column": {"up": "#end", "down": "#end", "north": "#side",
                    "south": "#side", "east": "#side", "west": "#side"},
    "cube_column_horizontal": {"up": "#side", "down": "#side", "north": "#end",
                               "south": "#end", "east": "#side", "west": "#side"},
    "cube_bottom_top": {"up": "#top", "down": "#bottom", "north": "#side",
                        "south": "#side", "east": "#side", "west": "#side"},
    "cube": {d: f"#{d}" for d in DIRECTIONS},
}


def parse_model(data: dict) -> Model:
    parent = data.get("parent")
    tex_size = tuple(data.get("texture_size", [16, 16]))
    textures = dict(data.get("textures", {}))

    elements = []
    if "elements" in data:
        for el in data["elements"]:
            frm = tuple(float(v) for v in el["from"])
            to = tuple(float(v) for v in el["to"])
            faces = {}
            for d, fd in el.get("faces", {}).items():
                uv = tuple(fd["uv"]) if "uv" in fd else _default_uv(frm, to, d)
                faces[d] = Face(d, uv, fd.get("texture", "#missing").lstrip(""),
                                fd.get("tintindex"), int(fd.get("rotation", 0)))
            rot = None
            if isinstance(el.get("rotation"), dict):
                r = el["rotation"]
                rot = Rotation(
                    tuple(float(v) for v in r.get("origin", [8, 8, 8])),
                    r.get("axis", "y"), float(r.get("angle", 0)),
                    bool(r.get("rescale", False)))
            elements.append(Element(frm, to, faces, el.get("name", ""), rot))
    elif parent:
        short = parent.split("/")[-1].split(":")[-1]
        if short in _CUBE_PARENTS:
            elements.append(_cube_element(_CUBE_PARENTS[short]))
        else:
            raise ValueError(
                f"model has no 'elements' and parent {parent!r} is not a known "
                f"cube* variant — can't derive its shape without the parent file")
    else:
        raise ValueError("model has neither 'elements' nor a 'parent'")

    return Model(elements, tex_size, textures, parent)


def load_model(path: str | Path) -> Model:
    return parse_model(json.loads(Path(path).read_text()))


def door_model() -> Model:
    """A full 2-tall door built to the exact vanilla geometry (each half is a
    3 x 16 x 16 slab; stacked = 3 wide-thick x 16 x 32 tall). Bottom half uses
    the `bottom` texture key, top half `top`. Faces + UVs match
    minecraft:block/door_{bottom,top}_left (big east/west faces carry the full
    16x16; the 3px north/south edges take a slice)."""
    def half(y0, key):
        f = {
            "north": Face("north", (3, 0, 0, 16), f"#{key}"),
            "south": Face("south", (0, 0, 3, 16), f"#{key}"),
            "west":  Face("west", (0, 0, 16, 16), f"#{key}"),
            "east":  Face("east", (16, 0, 0, 16), f"#{key}"),
            "up":    Face("up", (0, 3, 16, 0), f"#{key}", rotation=90),
            "down":  Face("down", (16, 13, 0, 16), f"#{key}", rotation=90),
        }
        return Element((0.0, float(y0), 0.0), (3.0, float(y0 + 16), 16.0), f, f"door_{key}")

    return Model([half(0, "bottom"), half(16, "top")], (16, 16),
                 {"bottom": "#bottom", "top": "#top"})
