"""Lift a 2D silhouette into a 3D voxel model — the "make a model from art" path.

The studio's other model code (`aide/model.py`, `modelrender.py`) *reads* an
existing Minecraft model and renders it. This module goes the other way: it
takes a flat side-view silhouette (any `.pxg`/PNG whose opaque pixels are the
shape) and *infers the missing third dimension*, producing a voxel volume you
can turn in 3D.

Two ways to infer the depth ("expand the width"):

- **revolve** — treat the silhouette as a lathe profile and spin it about its
  long axis. A column of half-height `r` becomes a disc of radius `r`. This is
  the right read for turned/forged finials that are round in cross-section
  (spearheads, flames, spires, the ferrule collar). Depth == height, inferred.

- **blade** — keep the silhouette's outline and give it a thickness, tapering
  toward the outline edges (thick down the spine, thin at the rim) so it reads
  as a forged blade rather than a flat slab. The taper comes from a Chebyshev
  distance transform. This is the read for flat shapes: crescents, tridents,
  broadheads, fleurs.

Output is a `Volume` (a set of filled integer voxels) plus helpers to turn it
into a culled face list — every face between a filled voxel and empty space,
each described compactly as `(x, y, z, dir)`. That face list drives both the
OBJ exporter and the self-contained WebGL viewer (`aide/liftviewer.py`), and it
stays tiny because a unit voxel face needs only a corner and a direction.

Model space is Y-up: image row 0 (top) maps to the highest Y, so lifted models
stand upright. The long/lathe axis is X (image columns), depth is Z.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from pathlib import Path

# face directions, index == dir code used everywhere downstream
#   0:+X 1:-X 2:+Y 3:-Y 4:+Z 5:-Z
FACE_NORMALS = [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]


@dataclass
class Volume:
    """A set of filled unit voxels on an integer grid, plus its bounding dims."""
    voxels: set[tuple[int, int, int]]
    nx: int
    ny: int
    nz: int

    def __bool__(self) -> bool:
        return bool(self.voxels)


# ---------------------------------------------------------------------------
# silhouette -> boolean mask
# ---------------------------------------------------------------------------

def mask_from_image(img) -> tuple[list[list[bool]], int, int]:
    """Opaque (alpha>0) pixels are the shape. Returns (mask[y][x], w, h)."""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    mask = [[px[x, y][3] > 0 for x in range(w)] for y in range(h)]
    return mask, w, h


def load_mask(path: str | Path) -> tuple[list[list[bool]], int, int]:
    """Load a `.pxg` or image file as a silhouette mask."""
    from aide.grid import load_texture

    return mask_from_image(load_texture(path))


def _columns(mask, w, h):
    """For each column x, the (min_y, max_y) span of filled pixels, or None."""
    out = []
    for x in range(w):
        ys = [y for y in range(h) if mask[y][x]]
        out.append((min(ys), max(ys)) if ys else None)
    return out


# ---------------------------------------------------------------------------
# distance transform (for blade taper)
# ---------------------------------------------------------------------------

def _chebyshev_distance(mask, w, h) -> list[list[int]]:
    """Chebyshev distance from each filled pixel to the nearest empty pixel/edge.
    Filled pixels on the outline get 1; interior spine pixels get the largest
    values. Empty pixels are 0. Multi-source BFS over 8-neighbourhoods."""
    INF = w + h
    dist = [[0 if not mask[y][x] else INF for x in range(w)] for y in range(h)]
    q = deque()
    for y in range(h):
        for x in range(w):
            if not mask[y][x]:
                continue
            # a filled pixel touching the border or an empty neighbour is depth 1
            edge = x == 0 or y == 0 or x == w - 1 or y == h - 1
            if not edge:
                for dx in (-1, 0, 1):
                    for dy in (-1, 0, 1):
                        if not mask[y + dy][x + dx]:
                            edge = True
                            break
                    if edge:
                        break
            if edge:
                dist[y][x] = 1
                q.append((x, y))
    while q:
        x, y = q.popleft()
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < w and 0 <= ny < h and dist[ny][nx] > dist[y][x] + 1:
                    dist[ny][nx] = dist[y][x] + 1
                    q.append((nx, ny))
    return dist


# ---------------------------------------------------------------------------
# lift modes
# ---------------------------------------------------------------------------

def revolve(mask, w, h, axis_y: float | None = None) -> Volume:
    """Spin the silhouette about its long (X) axis. Each column's outer radius
    (max distance from the axis to a filled pixel) becomes a solid disc, so the
    inferred depth equals the silhouette's local height. `axis_y` defaults to the
    vertical centre of the whole silhouette (the shaft centreline)."""
    cols = _columns(mask, w, h)
    filled_ys = [y for y in range(h) for x in range(w) if mask[y][x]]
    if not filled_ys:
        return Volume(set(), 1, 1, 1)
    if axis_y is None:
        axis_y = (min(filled_ys) + max(filled_ys)) / 2.0

    radii = []
    for span in cols:
        if span is None:
            radii.append(0.0)
            continue
        y0, y1 = span
        radii.append(max(abs(y0 - axis_y), abs(y1 - axis_y)) + 0.5)
    maxr = max(radii)
    nz = int(round(maxr * 2)) + 1
    if nz % 2 == 0:  # keep depth odd so the axis lands on an integer voxel centre
        nz += 1
    zc = (nz - 1) // 2
    yc = (h - 1) - axis_y  # centre in Y-up model space

    voxels: set[tuple[int, int, int]] = set()
    for x in range(w):
        r = radii[x]
        if r <= 0:
            continue
        r2 = r * r
        lo = int(round(yc - r))
        hi = int(round(yc + r))
        for Y in range(max(0, lo), min(h, hi + 1) + 1):
            dyc = Y - yc
            for z in range(nz):
                dzc = z - zc
                if dyc * dyc + dzc * dzc <= r2:
                    voxels.add((x, Y, z))
    return Volume(voxels, w, h, nz)


def blade(mask, w, h, thickness: int = 6) -> Volume:
    """Keep the silhouette's outline; give it a `thickness` in Z that tapers to
    the outline edges (thick spine, thin rim) via a distance transform, so it
    reads as a forged blade rather than a flat slab."""
    dist = _chebyshev_distance(mask, w, h)
    maxd = max((dist[y][x] for y in range(h) for x in range(w)), default=0)
    if maxd == 0:
        return Volume(set(), w, h, 1)
    nz = thickness + 1
    if nz % 2 == 0:  # odd depth -> integer centre, matches revolve for merging
        nz += 1
    zc = (nz - 1) // 2
    half_max = thickness / 2.0

    voxels: set[tuple[int, int, int]] = set()
    for y in range(h):
        Y = (h - 1) - y  # flip to Y-up
        for x in range(w):
            if not mask[y][x]:
                continue
            half = half_max * (dist[y][x] / maxd)
            lo = int(round(zc - half))
            hi = int(round(zc + half))
            for z in range(lo, hi + 1):
                voxels.add((x, Y, z))
    return Volume(voxels, w, h, nz)


def _restrict(mask, w, h, keep):
    """Copy of a mask with only the columns for which keep(x) is true."""
    return [[mask[y][x] and keep(x) for x in range(w)] for y in range(h)]


def merge(a: Volume, b: Volume, w: int, h: int) -> Volume:
    """Union two volumes into one shared depth frame, aligning their Z centres.
    Both must have odd depth (revolve/blade guarantee it), so the shift is an
    integer and no voxel lands off-grid."""
    nz = max(a.nz, b.nz)
    cf = (nz - 1) // 2
    out: set[tuple[int, int, int]] = set()
    for vol in (a, b):
        shift = cf - (vol.nz - 1) // 2
        for (x, y, z) in vol.voxels:
            out.add((x, y, z + shift))
    return Volume(out, w, h, nz)


def hybrid(mask, w, h, collar_end: int = 14, head_start: int = 13,
           thickness: int = 6, axis_y: float | None = None) -> Volume:
    """A round, lathe-turned collar joined to a flat, forged head — the read for
    caps whose head is a blade but whose ferrule should still be a cylinder that
    fits a round wand core. Columns up to `collar_end` are revolved; columns from
    `head_start` on are bladed; the two overlap in [head_start, collar_end] so
    they always weld into one solid piece. Depths are reconciled by `merge`."""
    collar = revolve(_restrict(mask, w, h, lambda x: x <= collar_end), w, h,
                     axis_y=axis_y)
    head = blade(_restrict(mask, w, h, lambda x: x >= head_start), w, h,
                 thickness=thickness)
    return merge(collar, head, w, h)


def lift(path_or_mask, mode: str = "revolve", **kw) -> Volume:
    """Convenience: lift a silhouette (path/`.pxg`/PNG, or a ready mask tuple)."""
    if isinstance(path_or_mask, tuple):
        mask, w, h = path_or_mask
    else:
        mask, w, h = load_mask(path_or_mask)
    if mode == "revolve":
        return revolve(mask, w, h, axis_y=kw.get("axis_y"))
    if mode == "blade":
        return blade(mask, w, h, thickness=kw.get("thickness", 6))
    if mode == "hybrid":
        return hybrid(mask, w, h, collar_end=kw.get("collar_end", 14),
                      head_start=kw.get("head_start", 13),
                      thickness=kw.get("thickness", 6), axis_y=kw.get("axis_y"))
    raise ValueError(
        f"unknown lift mode {mode!r} (want 'revolve', 'blade' or 'hybrid')")


# ---------------------------------------------------------------------------
# voxels -> culled faces
# ---------------------------------------------------------------------------

def exposed_faces(vol: Volume) -> list[tuple[int, int, int, int]]:
    """Every face between a filled voxel and empty space, as (x, y, z, dir).
    Internal faces (both voxels filled) are dropped — this is the surface mesh."""
    vox = vol.voxels
    faces = []
    for (x, y, z) in vox:
        for dcode, (dx, dy, dz) in enumerate(FACE_NORMALS):
            if (x + dx, y + dy, z + dz) not in vox:
                faces.append((x, y, z, dcode))
    faces.sort()
    return faces


# corner offsets per face dir, wound CCW when viewed from outside
_FACE_CORNERS = [
    [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)],  # +X
    [(0, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0)],  # -X
    [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)],  # +Y
    [(0, 0, 1), (0, 0, 0), (1, 0, 0), (1, 0, 1)],  # -Y
    [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],  # +Z
    [(1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0)],  # -Z
]


def to_obj(faces, name: str = "model") -> str:
    """A Wavefront OBJ of the culled faces (centred on the model's bbox), openable
    in any 3D tool or phone model viewer. Untextured — geometry only."""
    if not faces:
        return f"# {name}: empty\n"
    xs = [x for x, _, _, _ in faces] + [x + 1 for x, _, _, _ in faces]
    ys = [y for _, y, _, _ in faces] + [y + 1 for _, y, _, _ in faces]
    zs = [z for _, _, z, _ in faces] + [z + 1 for _, _, z, _ in faces]
    cx = (min(xs) + max(xs)) / 2.0
    cy = (min(ys) + max(ys)) / 2.0
    cz = (min(zs) + max(zs)) / 2.0

    verts: dict[tuple[int, int, int], int] = {}
    lines = [f"# {name} — lifted from a 2D silhouette by aide.lift", f"o {name}"]
    vlines: list[str] = []
    flines: list[str] = []

    def vid(p):
        if p not in verts:
            verts[p] = len(verts) + 1
            vlines.append(f"v {p[0] - cx:.3f} {p[1] - cy:.3f} {p[2] - cz:.3f}")
        return verts[p]

    for (x, y, z, dcode) in faces:
        ids = [vid((x + ox, y + oy, z + oz)) for ox, oy, oz in _FACE_CORNERS[dcode]]
        flines.append(f"f {ids[0]} {ids[1]} {ids[2]} {ids[3]}")

    lines.extend(vlines)
    lines.extend(flines)
    return "\n".join(lines) + "\n"
