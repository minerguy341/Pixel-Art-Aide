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

def _radii(mask, w, h, axis_y=None):
    """Per-column outer radius (axis→outer-edge distance) and the axis row.
    This is the lathe profile every axial-sweep mode shares."""
    cols = _columns(mask, w, h)
    filled_ys = [y for y in range(h) for x in range(w) if mask[y][x]]
    if not filled_ys:
        return None, None
    if axis_y is None:
        axis_y = (min(filled_ys) + max(filled_ys)) / 2.0
    radii = []
    for span in cols:
        if span is None:
            radii.append(0.0)
        else:
            y0, y1 = span
            radii.append(max(abs(y0 - axis_y), abs(y1 - axis_y)) + 0.5)
    return radii, axis_y


def _odd_frame(maxz):
    """Depth + integer centre for a half-extent, kept odd so centres align."""
    nz = int(round(maxz * 2)) + 1
    if nz % 2 == 0:
        nz += 1
    return nz, (nz - 1) // 2


# A cross-section is the shape of the tip in the Y–Z plane at an axial station
# of radius r. `_ZHALF[name](dy, r, k)` gives the Z half-thickness at vertical
# offset dy (|dy|<=r), where k bundles the tuning knobs. Real blades are never
# round: lenticular tapers to sharp edges, diamond adds four flat facets, square
# is a bodkin punch, midrib raises a stiffening spine down the centre.
def _zhalf(name, dy, r, flat, ridge):
    if r <= 0 or abs(dy) > r:
        return -1.0
    import math
    if name == "round":
        return math.sqrt(max(0.0, r * r - dy * dy))
    if name == "lens":
        return flat * math.sqrt(max(0.0, r * r - dy * dy))
    if name == "diamond":
        return flat * (r - abs(dy))
    if name == "square":
        return flat * r
    if name == "midrib":                      # lens blade + raised central spine
        lens = flat * math.sqrt(max(0.0, r * r - dy * dy))
        spine = ridge * r * max(0.0, 1.0 - abs(dy) / (0.30 * r))
        return lens + spine
    raise ValueError(f"unknown cross-section {name!r}")


_ZPROFILE_CROSS = ("round", "lens", "diamond", "square", "midrib")


def _poly_inside(ny, nz, sides):
    """Is normalised point (ny, nz) inside a regular `sides`-gon of circumradius 1
    with a vertex pointing up (+Y)? A faceted point — triangle (3) is the solid
    'pyramidal' trilobate section, hexagon (6) a many-faceted spire, etc."""
    import math
    ap = math.cos(math.pi / sides)                # apothem for circumradius 1
    for k in range(sides):                        # each edge's outward normal
        a = math.pi / 2 + math.pi / sides + k * 2 * math.pi / sides
        if ny * math.cos(a) + nz * math.sin(a) > ap + 1e-9:
            return False
    return True


def sweep(mask, w, h, cross="round", flat=0.5, ridge=0.45, sides=3,
          axis_y=None) -> Volume:
    """Lathe the silhouette about its long (X) axis, but give each cross-section
    a *forged blade* shape rather than a plain disc — `cross` selects lenticular,
    rhombic, square (bodkin), lens-with-midrib, or a regular `poly`gon (faceted /
    trilobate). `flat` is the depth/width ratio (1.0 == round); `ridge` is the
    midrib height as a fraction of radius; `sides` is the polygon face count."""
    radii, axis_y = _radii(mask, w, h, axis_y)
    if radii is None:
        return Volume(set(), 1, 1, 1)
    maxr = max(radii)
    is_poly = cross == "poly"
    maxz = maxr if is_poly else max(
        (_zhalf(cross, dy, maxr, flat, ridge)
         for dy in range(-int(maxr), int(maxr) + 1)), default=0.0)
    nz, zc = _odd_frame(maxz)
    yc = (h - 1) - axis_y

    voxels: set[tuple[int, int, int]] = set()
    for x in range(w):
        r = radii[x]
        if r <= 0:
            continue
        y0 = max(0, int(round(yc - r)))
        y1 = min(h, int(round(yc + r)) + 1)
        for Y in range(y0, y1 + 1):
            dy = Y - yc
            if is_poly:
                for z in range(nz):
                    if _poly_inside(dy / r, (z - zc) / r, sides):
                        voxels.add((x, Y, z))
                continue
            zh = _zhalf(cross, dy, r, flat, ridge)
            if zh < 0:
                continue
            for z in range(int(round(zc - zh)), int(round(zc + zh)) + 1):
                voxels.add((x, Y, z))
    return Volume(voxels, w, h, nz)


def revolve(mask, w, h, axis_y: float | None = None) -> Volume:
    """Spin the silhouette about its long axis into a solid of revolution (round
    cross-section). Depth equals local height. This is `sweep(cross='round')`."""
    return sweep(mask, w, h, cross="round", flat=1.0, axis_y=axis_y)


def radial(mask, w, h, blades=3, thickness=0.22, hub=0.16,
           axis_y=None) -> Volume:
    """The broadhead read: N thin blades radiating from the axis at 360/N°, so
    the cross-section is a Y (3) or + (4) rather than a solid. The silhouette
    gives each blade's reach; `thickness`/`hub` are fractions of the max radius.
    One blade points up so the side view still matches the drawn profile."""
    import math
    radii, axis_y = _radii(mask, w, h, axis_y)
    if radii is None:
        return Volume(set(), 1, 1, 1)
    maxr = max(radii)
    nz, zc = _odd_frame(maxr)
    yc = (h - 1) - axis_y
    angs = [math.pi / 2 + k * 2 * math.pi / blades for k in range(blades)]
    thalf = thickness * maxr
    hubr = hub * maxr

    voxels: set[tuple[int, int, int]] = set()
    for x in range(w):
        r = radii[x]
        if r <= 0:
            continue
        for Y in range(max(0, int(round(yc - r))), min(h, int(round(yc + r)) + 1) + 1):
            dy = Y - yc
            for z in range(nz):
                dz = z - zc
                rho = math.hypot(dy, dz)
                if rho > r:
                    continue
                if rho <= hubr:
                    voxels.add((x, Y, z))
                    continue
                for a in angs:
                    along = dy * math.cos(a) + dz * math.sin(a)
                    perp = abs(-dy * math.sin(a) + dz * math.cos(a))
                    if along >= 0 and perp <= thalf:
                        voxels.add((x, Y, z))
                        break
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


def _lift_region(mask, w, h, mode, kw, axis_y=None):
    """Lift one masked region in a single mode (no collar welding)."""
    if mode == "blade":
        return blade(mask, w, h, thickness=kw.get("thickness", 6))
    if mode == "radial":
        return radial(mask, w, h, blades=kw.get("blades", 3),
                      thickness=kw.get("bladethick", 0.22),
                      hub=kw.get("hub", 0.16), axis_y=axis_y)
    if mode in _ZPROFILE_CROSS or mode in ("revolve", "poly"):
        cross = "round" if mode == "revolve" else mode
        return sweep(mask, w, h, cross=cross, flat=kw.get("flat", 0.5),
                     ridge=kw.get("ridge", 0.45), sides=kw.get("sides", 3),
                     axis_y=axis_y)
    raise ValueError(f"unknown head/region mode {mode!r}")


def hybrid(mask, w, h, collar_end: int = 14, head_start: int = 13,
           head_mode: str = "blade", axis_y: float | None = None, **kw) -> Volume:
    """A round, lathe-turned collar welded to a shaped head — every cap keeps a
    cylindrical ferrule that fits a round wand core, while its head takes whatever
    forged cross-section suits it (blade, lens/midrib spearhead, diamond or square
    point, or a radial broadhead). Columns up to `collar_end` are revolved; from
    `head_start` on use `head_mode`; the overlap welds them into one solid piece."""
    collar = revolve(_restrict(mask, w, h, lambda x: x <= collar_end), w, h,
                     axis_y=axis_y)
    head = _lift_region(_restrict(mask, w, h, lambda x: x >= head_start), w, h,
                        head_mode, kw, axis_y=axis_y)
    return merge(collar, head, w, h)


def lift(path_or_mask, mode: str = "revolve", **kw) -> Volume:
    """Lift a silhouette (path/`.pxg`/PNG, or a ready mask tuple). `mode` is
    'revolve', 'blade', a cross-section ('lens'/'diamond'/'square'/'midrib'),
    'radial' (N-blade broadhead), or 'hybrid' (round collar + a `head_mode`)."""
    if isinstance(path_or_mask, tuple):
        mask, w, h = path_or_mask
    else:
        mask, w, h = load_mask(path_or_mask)
    if mode == "hybrid":
        return hybrid(mask, w, h, collar_end=kw.get("collar_end", 14),
                      head_start=kw.get("head_start", 13),
                      head_mode=kw.get("head_mode", "blade"),
                      axis_y=kw.get("axis_y"), **{
                          k: kw[k] for k in
                          ("thickness", "flat", "ridge", "sides", "blades",
                           "bladethick", "hub") if k in kw})
    return _lift_region(mask, w, h, mode, kw, axis_y=kw.get("axis_y"))


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


# ---------------------------------------------------------------------------
# voxels -> smooth surface (naive surface nets)
# ---------------------------------------------------------------------------

# the 8 corners of a lattice cell and its 12 edges (corner index pairs)
_SN_CORNERS = [(0, 0, 0), (1, 0, 0), (0, 1, 0), (1, 1, 0),
               (0, 0, 1), (1, 0, 1), (0, 1, 1), (1, 1, 1)]
_SN_EDGES = [(0, 1), (0, 2), (0, 4), (1, 3), (1, 5), (2, 3),
             (2, 6), (4, 5), (4, 6), (3, 7), (5, 7), (6, 7)]


def surface_nets(vol: Volume, relax: int = 2):
    """Smooth the blocky voxel model into a dual surface (naive surface nets):
    every cell straddling the solid/empty boundary contributes ONE vertex placed
    at the centroid of its edge crossings, then a few Laplacian passes relax the
    staircase into a smooth faceted skin. Per-vertex normals come from the
    occupancy gradient, so shading is smooth. Returns (verts, tris, normals).

    This is the "square-or-triangle portion per pixel" read of the model: flat
    runs stay flat, and every boundary voxel is cut by the surface instead of
    standing as a full cube."""
    import math

    S = vol.voxels
    if not S:
        return [], [], []
    xs = [v[0] for v in S]
    ys = [v[1] for v in S]
    zs = [v[2] for v in S]
    x0, x1 = min(xs) - 1, max(xs) + 1
    y0, y1 = min(ys) - 1, max(ys) + 1
    z0, z1 = min(zs) - 1, max(zs) + 1
    has = S.__contains__

    cell_vert: dict[tuple[int, int, int], int] = {}
    verts: list[list[float]] = []
    norms: list[list[float]] = []
    for i in range(x0, x1 + 1):
        for j in range(y0, y1 + 1):
            for k in range(z0, z1 + 1):
                s = [1 if has((i + cx, j + cy, k + cz)) else 0
                     for cx, cy, cz in _SN_CORNERS]
                tot = sum(s)
                if tot == 0 or tot == 8:
                    continue
                px = py = pz = 0.0
                c = 0
                for a, b in _SN_EDGES:
                    if s[a] != s[b]:
                        ca, cb = _SN_CORNERS[a], _SN_CORNERS[b]
                        px += (ca[0] + cb[0]) / 2
                        py += (ca[1] + cb[1]) / 2
                        pz += (ca[2] + cb[2]) / 2
                        c += 1
                cell_vert[(i, j, k)] = len(verts)
                verts.append([i + px / c, j + py / c, k + pz / c])
                nx = (s[1] + s[3] + s[5] + s[7]) - (s[0] + s[2] + s[4] + s[6])
                ny = (s[2] + s[3] + s[6] + s[7]) - (s[0] + s[1] + s[4] + s[5])
                nz = (s[4] + s[5] + s[6] + s[7]) - (s[0] + s[1] + s[2] + s[3])
                norms.append([-nx, -ny, -nz])

    cv = cell_vert.get
    tris: list[int] = []
    # one quad per lattice edge whose endpoints straddle the surface; the 4 cells
    # sharing that edge own the 4 corners. Winding is unused (normals are shaded,
    # backfaces aren't culled), so emit two triangles either way.
    for i in range(x0, x1 + 2):
        for j in range(y0, y1 + 2):
            for k in range(z0, z1 + 2):
                if has((i, j, k)) != has((i + 1, j, k)):
                    q = (cv((i, j - 1, k - 1)), cv((i, j, k - 1)),
                         cv((i, j, k)), cv((i, j - 1, k)))
                    if None not in q:
                        tris += [q[0], q[1], q[2], q[0], q[2], q[3]]
                if has((i, j, k)) != has((i, j + 1, k)):
                    q = (cv((i - 1, j, k - 1)), cv((i, j, k - 1)),
                         cv((i, j, k)), cv((i - 1, j, k)))
                    if None not in q:
                        tris += [q[0], q[1], q[2], q[0], q[2], q[3]]
                if has((i, j, k)) != has((i, j, k + 1)):
                    q = (cv((i - 1, j - 1, k)), cv((i, j - 1, k)),
                         cv((i, j, k)), cv((i - 1, j, k)))
                    if None not in q:
                        tris += [q[0], q[1], q[2], q[0], q[2], q[3]]

    # Laplacian relaxation: pull each vertex toward the mean of its edge-neighbours
    if relax > 0 and verts:
        adj: list[set] = [set() for _ in verts]
        for t in range(0, len(tris), 3):
            a, b, cc = tris[t], tris[t + 1], tris[t + 2]
            adj[a].update((b, cc)); adj[b].update((a, cc)); adj[cc].update((a, b))
        for _ in range(relax):
            new = [v[:] for v in verts]
            for vi, nb in enumerate(adj):
                if not nb:
                    continue
                sx = sy = sz = 0.0
                for n in nb:
                    sx += verts[n][0]; sy += verts[n][1]; sz += verts[n][2]
                m = len(nb)
                # blend halfway toward the neighbour centroid
                new[vi][0] = 0.5 * verts[vi][0] + 0.5 * sx / m
                new[vi][1] = 0.5 * verts[vi][1] + 0.5 * sy / m
                new[vi][2] = 0.5 * verts[vi][2] + 0.5 * sz / m
            verts = new

    for n in norms:
        L = math.sqrt(n[0] * n[0] + n[1] * n[1] + n[2] * n[2]) or 1.0
        n[0] /= L; n[1] /= L; n[2] /= L
    return verts, tris, norms


def to_obj_mesh(verts, tris, norms=None, name: str = "model") -> str:
    """Wavefront OBJ of a smooth triangle mesh (from `surface_nets`), centred on
    its bbox, with vertex normals for smooth shading. Untextured."""
    if not verts:
        return f"# {name}: empty\n"
    cx = (min(v[0] for v in verts) + max(v[0] for v in verts)) / 2
    cy = (min(v[1] for v in verts) + max(v[1] for v in verts)) / 2
    cz = (min(v[2] for v in verts) + max(v[2] for v in verts)) / 2
    out = [f"# {name} — smoothed (surface nets) by aide.lift", f"o {name}"]
    for v in verts:
        out.append(f"v {v[0]-cx:.3f} {v[1]-cy:.3f} {v[2]-cz:.3f}")
    if norms:
        for n in norms:
            out.append(f"vn {n[0]:.3f} {n[1]:.3f} {n[2]:.3f}")
    for t in range(0, len(tris), 3):
        a, b, c = tris[t] + 1, tris[t + 1] + 1, tris[t + 2] + 1
        out.append(f"f {a}//{a} {b}//{b} {c}//{c}" if norms else f"f {a} {b} {c}")
    return "\n".join(out) + "\n"
