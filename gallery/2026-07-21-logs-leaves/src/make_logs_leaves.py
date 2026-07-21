#!/usr/bin/env python3
"""Greatwood + Silverwood LOGS (bark side + end-grain top) and LEAVES — source of record.

Retry of the wood-type textures, logs + leaves only. A few candidates each for
{greatwood, silverwood} x {log-side, leaves}; one matching end-grain top per wood.

Design grounds (knowledge base):
- Wood grain = vertical RUNS of close tones (3px+), one darker furrow line per ridge;
  no lone 1-2px flecks (that reads as brick/dirt). [vanilla wood grammar]
- Leaves need ~30-40% scattered TRANSPARENT holes, high-frequency per-cell, no 2x2
  fully-transparent blocks; 2 hue families (lit/shadow) + sparse accent. Dense magic
  canopy may drop toward ~18%. [leaves lessons]
- Silverwood is the bright grove exception (pale, luminance can ride high) and carries
  the teal shimmer #7FE8D8 as SPARSE 1-2px accents — the magic tell. Greatwood is warm,
  ancient, matte, NO teal. [thaumaturgy card]
- Blocks tile: value depends on x%16 / y%16 so both axes wrap seamlessly.

Everything is deterministic (own integer hash, no PRNG state) so re-runs are identical.
Emits .pxg sources (editable) AND .png build products to ../src and ../out, plus the
presentation composites (leaf 3x3 tile + block render; log 2x3 tile + 3-tall trunk) to
../previews.
"""
from pathlib import Path
from PIL import Image
import sys

HERE = Path(__file__).resolve().parent
SESS = HERE.parent
OUT = SESS / "out"
SRC = SESS / "src"
PREV = SESS / "previews"
for d in (OUT, SRC, PREV):
    d.mkdir(parents=True, exist_ok=True)

# import the studio toolkit
sys.path.insert(0, str(SESS.parent.parent))
from aide import grid as G  # noqa: E402
from aide import blockrender as BR  # noqa: E402

N = 16
T = (0, 0, 0, 0)


def hx(v):
    return ((v >> 16) & 255, (v >> 8) & 255, v & 255, 255)


def h2(x, y, seed):
    """Deterministic 0..1 hash of a wrapped cell — tiles because caller passes x%16,y%16."""
    h = (x * 73856093) ^ (y * 19349663) ^ (seed * 83492791)
    h &= 0xFFFFFFFF
    h ^= h >> 13
    h &= 0xFFFFFFFF
    return (h % 100003) / 100003.0


# ---------------------------------------------------------------- palettes
# Greatwood bark: ancient warm brown, deep furrows (matte, no teal).
GW = dict(k=hx(0x231712), f=hx(0x33251C), b=hx(0x47372A), r=hx(0x574230), h=hx(0x665038))
# Silverwood bark: pale silver, cool grey-green streaks + sparse teal shimmer.
SW = dict(d=hx(0x878F86), s=hx(0x9EA69C), b=hx(0xC4C9BD), l=hx(0xD9DED9), h=hx(0xE9ECE2), t=hx(0x7FE8D8))
# Greatwood leaves: deep forest green + rare warm dead-leaf accent.
GL = dict(e=hx(0x21401C), s=hx(0x2C5324), g=hx(0x3E6B2F), l=hx(0x4E7D3A), a=hx(0x5C4A24))
# Silverwood leaves: pale mint + teal shimmer glow.
SL = dict(e=hx(0x6BA891), s=hx(0x8ABFA9), g=hx(0xA9D8C4), l=hx(0xC6E8D8), t=hx(0x7FE8D8))


def blank():
    im = Image.new("RGBA", (N, N), T)
    return im, im.load()


# ---------------------------------------------------------------- greatwood bark
def gw_bark(variant):
    """variant: 'straight' | 'gnarled' | 'plated'. Vertical furrows, warm ancient bark."""
    im, px = blank()
    # furrow centres (columns), spaced to wrap across 16
    furrows = {1, 6, 11}
    for y in range(N):
        for x in range(N):
            # base ridge shading: distance from nearest furrow column decides ridge vs valley
            df = min((x - c) % N for c in furrows)
            df = min(df, min((c - x) % N for c in furrows))
            if x in furrows:
                c = GW["k"] if (y % 4) else GW["f"]  # furrow line, broken with a darker crevice run
            elif df == 1:
                c = GW["f"]
            elif df == 2:
                c = GW["b"]
            else:
                # ridge crown: lit run, varied along y in 3px+ bands
                band = (y + x) // 3 % 2
                c = GW["h"] if band else GW["r"]
            # long vertical tone runs: nudge some ridge cells darker in 3px runs
            if c in (GW["r"], GW["h"]) and h2(x, y // 3, 11) < 0.28:
                c = GW["b"]
            px[x, y] = c

    if variant == "gnarled":
        # two small knots (concentric 3x3) sitting on ridges
        for kx, ky in ((4, 5), (9, 11)):
            for dy in range(-2, 3):
                for dx in range(-2, 3):
                    x, y = (kx + dx) % N, (ky + dy) % N
                    rad = max(abs(dx), abs(dy))
                    px[x, y] = (GW["k"] if rad == 0 else GW["f"] if rad == 1 else GW["b"])
    elif variant == "plated":
        # horizontal cross-cracks splitting ridges into craggy plates
        for y in (3, 10):
            for x in range(N):
                if x not in furrows:
                    px[x, y] = GW["k"] if (x % 3) else GW["f"]
                    if y + 1 < N and x not in furrows and (x % 2):
                        px[x, (y + 1) % N] = GW["f"]
    return im


def gw_top():
    """Greatwood end grain: concentric growth rings, dark pith, warm ramp."""
    im, px = blank()
    cx, cy = 7.5, 7.5
    for y in range(N):
        for x in range(N):
            r = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            ring = int(r) % 3
            if r < 1.2:
                c = GW["k"]  # pith
            elif ring == 0:
                c = GW["f"]  # ring line
            elif ring == 1:
                c = GW["b"]
            else:
                c = GW["r"]
            # slight warm crown toward the lit top-left
            if (x + y) < 9 and c == GW["r"]:
                c = GW["h"]
            px[x, y] = c
    # bark rind on the outer edge
    for i in range(N):
        for (x, y) in ((i, 0), (i, N - 1), (0, i), (N - 1, i)):
            px[x, y] = GW["f"] if (i % 3) else GW["k"]
    return im


# ---------------------------------------------------------------- silverwood bark
def sw_bark(variant):
    """variant: 'smooth' | 'lenticel' | 'shimmer'. Pale birch-like silverwood."""
    im, px = blank()
    streaks = {3, 12}
    for y in range(N):
        for x in range(N):
            if x in streaks and (y % 5) != 2:
                c = SW["s"]  # faint vertical streak, broken
            elif x in (2, 4, 11, 13):
                c = SW["b"]
            else:
                c = SW["l"]
            # sparse cool mottle in 3px vertical runs
            if c == SW["l"] and h2(x, y // 3, 5) < 0.16:
                c = SW["b"]
            # top-left catches the highlight
            if c == SW["l"] and (x + y) < 6:
                c = SW["h"]
            px[x, y] = c

    if variant in ("smooth", "shimmer"):
        # sparse teal shimmer specks (the magic tell) — 1px, well under 3% of pixels
        specks = [(6, 2), (10, 8), (5, 13)] if variant == "smooth" else [(6, 2), (9, 7), (10, 8), (5, 13), (12, 11)]
        for (x, y) in specks:
            px[x, y] = SW["t"]
        if variant == "shimmer":
            # a faint 2px vertical shimmer seam segment
            for y in (4, 5, 6):
                px[8, y] = SW["t"] if y == 5 else SW["d"]
    elif variant == "lenticel":
        # horizontal birch lenticel dashes in cool grey + a couple teal
        for (x, y, w) in ((2, 4, 3), (8, 6, 4), (5, 11, 3), (11, 13, 3)):
            for dx in range(w):
                px[(x + dx) % N, y] = SW["d"] if dx else SW["s"]
        px[9, 6] = SW["t"]
        px[6, 11] = SW["t"]
    return im


def sw_top():
    """Silverwood end grain: pale rings, faint teal heart."""
    im, px = blank()
    cx, cy = 7.5, 7.5
    for y in range(N):
        for x in range(N):
            r = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            ring = int(r) % 3
            if r < 1.4:
                c = SW["t"]  # faint teal heart
            elif ring == 0:
                c = SW["s"]
            elif ring == 1:
                c = SW["b"]
            else:
                c = SW["l"]
            if (x + y) < 9 and c == SW["l"]:
                c = SW["h"]
            px[x, y] = c
    for i in range(N):
        for (x, y) in ((i, 0), (i, N - 1), (0, i), (N - 1, i)):
            px[x, y] = SW["s"] if (i % 3) else SW["d"]
    return im


# ---------------------------------------------------------------- leaves
def _leaf_field(pal, hole_frac, seed, accent_key=None, accent_frac=0.0, accent_seed=0):
    """Shared leaf builder: clumped lit/base/shadow, scattered tiling holes, rimmed edges."""
    im, px = blank()
    g, l, s, e = pal["g"], pal["l"], pal["s"], pal["e"]
    # 1) clumped value field (two octaves of wrapped hash) -> lit / base / shadow
    for y in range(N):
        for x in range(N):
            n = 0.6 * h2(x // 2, y // 2, seed) + 0.4 * h2(x, y, seed + 1)
            if n > 0.66:
                c = l
            elif n < 0.34:
                c = s
            else:
                c = g
            px[x, y] = c
    # 2) punch tiling holes, never completing a 2x2 fully-transparent block
    holes = set()

    def would_make_2x2(x, y):
        for oy in (-1, 0):
            for ox in (-1, 0):
                quad = [((x + ox + dx) % N, (y + oy + dy) % N) for dy in (0, 1) for dx in (0, 1)]
                if all((cx, cy) in holes or (cx, cy) == (x, y) for (cx, cy) in quad):
                    return True
        return False

    order = sorted(((h2(x, y, seed + 7), x, y) for y in range(N) for x in range(N)))
    target = int(hole_frac * N * N)
    for _, x, y in order:
        if len(holes) >= target:
            break
        if would_make_2x2(x, y):
            continue
        holes.add((x, y))
        px[x, y] = T
    # 3) rim leaf cells that touch a hole with the deep edge colour (lacy read)
    rim = []
    for y in range(N):
        for x in range(N):
            if px[x, y][3] == 0:
                continue
            if any(((x + dx) % N, (y + dy) % N) in holes for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                rim.append((x, y))
    for (x, y) in rim:
        if px[x, y] != l or h2(x, y, seed + 3) < 0.5:  # keep some lit edges bright
            px[x, y] = e
    # 4) sparse accent
    if accent_key and accent_frac > 0:
        for y in range(N):
            for x in range(N):
                if px[x, y][3] and h2(x, y, accent_seed + 99) < accent_frac:
                    px[x, y] = pal[accent_key]
    return im


def gw_leaves(variant):
    if variant == "broadleaf":
        return _leaf_field(GL, 0.33, 21)
    if variant == "dense":
        return _leaf_field(GL, 0.22, 22)
    if variant == "accent":
        return _leaf_field(GL, 0.32, 23, accent_key="a", accent_frac=0.03, accent_seed=23)


def sw_leaves(variant):
    if variant == "airy":
        return _leaf_field(SL, 0.33, 31, accent_key="t", accent_frac=0.02, accent_seed=31)
    if variant == "canopy":
        return _leaf_field(SL, 0.18, 32, accent_key="t", accent_frac=0.03, accent_seed=32)
    if variant == "glow":
        return _leaf_field(SL, 0.30, 33, accent_key="t", accent_frac=0.05, accent_seed=33)


# ---------------------------------------------------------------- presentation
def tile_grid(img, cols, rows, scale):
    w, h = img.size
    canvas = Image.new("RGBA", (w * cols, h * rows), T)
    for r in range(rows):
        for c in range(cols):
            canvas.alpha_composite(img, (c * w, r * h))
    return canvas.resize((canvas.width * scale, canvas.height * scale), Image.NEAREST)


def stack_iso(top, side, count, scale=8):
    """Render `count` cubes stacked vertically (a trunk). Bottom drawn first; each higher
    cube composited over, shifted up by one face height, so only the top cube's top shows."""
    n = top.width
    step = n * scale  # screen-y height of one vertical face
    one = BR.iso_block(top, side, side, scale=scale)
    ow, oh = one.size
    canvas = Image.new("RGBA", (ow, oh + step * (count - 1)), T)
    for i in range(count - 1, -1, -1):  # bottom (largest y) first
        y = step * i
        canvas.alpha_composite(one, (0, y))
    # crop away empty top margin
    bbox = canvas.getbbox()
    return canvas.crop(bbox) if bbox else canvas


def save_both(img, name):
    """Write .pxg source + .png build product."""
    pxg = G.from_image(img)
    (SRC / f"{name}.pxg").write_text(G.to_text(pxg))
    G.save_texture(img, OUT / f"{name}.png")


# ---------------------------------------------------------------- build
def main():
    logs = {
        "greatwood_log_straight": gw_bark("straight"),
        "greatwood_log_gnarled": gw_bark("gnarled"),
        "greatwood_log_plated": gw_bark("plated"),
        "silverwood_log_smooth": sw_bark("smooth"),
        "silverwood_log_lenticel": sw_bark("lenticel"),
        "silverwood_log_shimmer": sw_bark("shimmer"),
    }
    tops = {"greatwood_log_top": gw_top(), "silverwood_log_top": sw_top()}
    leaves = {
        "greatwood_leaves_broadleaf": gw_leaves("broadleaf"),
        "greatwood_leaves_dense": gw_leaves("dense"),
        "greatwood_leaves_accent": gw_leaves("accent"),
        "silverwood_leaves_airy": sw_leaves("airy"),
        "silverwood_leaves_canopy": sw_leaves("canopy"),
        "silverwood_leaves_glow": sw_leaves("glow"),
    }

    for name, img in {**logs, **tops, **leaves}.items():
        save_both(img, name)

    # presentation composites
    for name, img in logs.items():
        wood = "greatwood" if name.startswith("greatwood") else "silverwood"
        top = tops[f"{wood}_log_top"]
        tile_grid(img, 2, 3, 8).save(PREV / f"{name}_tile2x3.png")   # 2 wide x 3 tall
        stack_iso(top, img, 3).save(PREV / f"{name}_trunk3.png")     # 3-block-tall trunk
    for name, img in leaves.items():
        tile_grid(img, 3, 3, 8).save(PREV / f"{name}_tile3x3.png")   # 3x3
        BR.iso_block(img, img, img, scale=8).save(PREV / f"{name}_block.png")

    print("wrote", len(logs) + len(tops) + len(leaves), "textures + composites")


if __name__ == "__main__":
    main()
