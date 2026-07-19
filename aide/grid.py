"""The .pxg source format: a human/Claude-editable text form of a pixel texture.

Format:

    # comment
    size: 16x16
    [palette]
    . = none            # transparent
    s = 6B7075          # base stone
    S = 545A5E 80       # hex may carry an alpha byte as a second token (0-255)
    [grid]
    ssssSsss...
    (height rows of exactly width chars, each char defined in [palette])

Rules:
- Palette keys are single printable non-whitespace chars; '#' is reserved for
  comments and may not be a key.
- Color is `none` (fully transparent), RRGGBB, or RRGGBBAA hex. An optional
  second decimal token overrides alpha.
- Grid rows are raw (no inline comments); blank lines and comment lines are
  skipped everywhere.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image

RGBA = tuple[int, int, int, int]

_HEX_RE = re.compile(r"^[0-9a-fA-F]{6}([0-9a-fA-F]{2})?$")


@dataclass
class Pxg:
    width: int
    height: int
    palette: dict[str, RGBA] = field(default_factory=dict)  # char -> RGBA
    rows: list[str] = field(default_factory=list)  # height strings of width chars

    def color_at(self, x: int, y: int) -> RGBA:
        return self.palette[self.rows[y][x]]


def parse_color(token: str, alpha: str | None = None) -> RGBA:
    if token.lower() == "none":
        return (0, 0, 0, 0)
    if not _HEX_RE.match(token):
        raise ValueError(f"bad color {token!r}: expected 'none', RRGGBB or RRGGBBAA")
    r, g, b = int(token[0:2], 16), int(token[2:4], 16), int(token[4:6], 16)
    a = int(token[6:8], 16) if len(token) == 8 else 255
    if alpha is not None:
        a = max(0, min(255, int(alpha)))
    return (r, g, b, a)


def parse_pxg(text: str, source: str = "<string>") -> Pxg:
    size: tuple[int, int] | None = None
    palette: dict[str, RGBA] = {}
    rows: list[str] = []
    section = None

    for lineno, raw in enumerate(text.splitlines(), start=1):
        line = raw.rstrip("\n")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue

        def err(msg: str) -> ValueError:
            return ValueError(f"{source}:{lineno}: {msg}")

        if stripped.lower().startswith("size:"):
            m = re.match(r"size:\s*(\d+)\s*[xX]\s*(\d+)$", stripped)
            if not m:
                raise err(f"bad size line {stripped!r}, expected 'size: WxH'")
            size = (int(m.group(1)), int(m.group(2)))
        elif stripped == "[palette]":
            section = "palette"
        elif stripped == "[grid]":
            section = "grid"
        elif section == "palette":
            body = stripped.split("#", 1)[0].strip()
            m = re.match(r"^(\S)\s*=\s*(\S+)(?:\s+(\d+))?$", body)
            if not m:
                raise err(f"bad palette entry {stripped!r}, expected 'c = RRGGBB'")
            key, color, alpha = m.group(1), m.group(2), m.group(3)
            if key == "#":
                raise err("'#' cannot be a palette key (reserved for comments)")
            if key in palette:
                raise err(f"duplicate palette key {key!r}")
            palette[key] = parse_color(color, alpha)
        elif section == "grid":
            rows.append(stripped)
        else:
            raise err(f"unexpected line {stripped!r} before any section")

    if size is None:
        raise ValueError(f"{source}: missing 'size:' line")
    w, h = size
    if len(rows) != h:
        raise ValueError(f"{source}: grid has {len(rows)} rows, size says {h}")
    for i, row in enumerate(rows):
        if len(row) != w:
            raise ValueError(f"{source}: grid row {i + 1} has {len(row)} chars, size says {w}")
        for ch in row:
            if ch not in palette:
                raise ValueError(f"{source}: grid row {i + 1} uses undefined key {ch!r}")
    return Pxg(width=w, height=h, palette=palette, rows=rows)


def load_pxg(path: str | Path) -> Pxg:
    p = Path(path)
    return parse_pxg(p.read_text(), source=str(p))


def to_text(pxg: Pxg, comments: dict[str, str] | None = None) -> str:
    lines = [f"size: {pxg.width}x{pxg.height}", "[palette]"]
    for key, (r, g, b, a) in pxg.palette.items():
        color = "none" if a == 0 and (r, g, b) == (0, 0, 0) else f"{r:02X}{g:02X}{b:02X}" + (f"{a:02X}" if a != 255 else "")
        note = f"   # {comments[key]}" if comments and key in comments else ""
        lines.append(f"{key} = {color}{note}")
    lines.append("[grid]")
    lines.extend(pxg.rows)
    return "\n".join(lines) + "\n"


def to_image(pxg: Pxg) -> Image.Image:
    img = Image.new("RGBA", (pxg.width, pxg.height))
    px = img.load()
    for y in range(pxg.height):
        for x in range(pxg.width):
            px[x, y] = pxg.color_at(x, y)
    return img


# Key pool for importing images: '.' is reserved for transparent.
_KEY_POOL = (
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    "!$%&*+-/:;<=>?@^_~"
)


def from_image(img: Image.Image, max_colors: int = 64) -> Pxg:
    """Convert a small RGBA image into an editable Pxg (one key per unique color)."""
    img = img.convert("RGBA")
    w, h = img.size
    px = img.load()
    keys: dict[RGBA, str] = {}
    palette: dict[str, RGBA] = {}
    rows: list[str] = []
    pool = iter(_KEY_POOL)
    for y in range(h):
        row = []
        for x in range(w):
            c = px[x, y]
            if c[3] == 0:
                c = (0, 0, 0, 0)
            if c not in keys:
                key = "." if c == (0, 0, 0, 0) else next(pool, None)
                if key is None:
                    raise ValueError(f"image has more than {max_colors} unique colors; quantize first")
                keys[c] = key
                palette[key] = c
            row.append(keys[c])
        rows.append("".join(row))
    if len(palette) > max_colors:
        raise ValueError(f"image has {len(palette)} unique colors (max {max_colors}); quantize first")
    return Pxg(width=w, height=h, palette=palette, rows=rows)


def load_texture(path: str | Path) -> Image.Image:
    """Load either a .pxg source or an image file as an RGBA image."""
    p = Path(path)
    if p.suffix.lower() == ".pxg":
        return to_image(load_pxg(p))
    return Image.open(p).convert("RGBA")
