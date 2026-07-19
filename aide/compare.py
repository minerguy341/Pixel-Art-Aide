"""Contact sheets: render N candidate textures side by side for user review."""

from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw

from aide.grid import load_texture
from aide.render import (
    SHEET_BG,
    LABEL_FG,
    grid_overlay,
    hstack,
    on_checker,
    palette_strip,
    stack,
    tiled,
    upscale,
)


def variant_column(img: Image.Image, label: str, tile: bool = False) -> Image.Image:
    factor = max(4, 128 // img.width)
    blocks = [
        _label(label),
        on_checker(img, cell=4),
        on_checker(upscale(img, factor), cell=8),
    ]
    if tile:
        tile_factor = max(2, 48 // img.width)
        blocks.append(upscale(tiled(img), tile_factor))
    blocks.append(palette_strip(img, swatch=12))
    return stack(blocks, pad=4)


def _label(text: str) -> Image.Image:
    im = Image.new("RGBA", (max(60, 6 * len(text) + 8), 14), SHEET_BG)
    ImageDraw.Draw(im).text((2, 1), text, fill=LABEL_FG)
    return im


def contact_sheet(paths: list[str | Path], tile: bool = False, labels: list[str] | None = None) -> Image.Image:
    cols = []
    for i, p in enumerate(paths):
        img = load_texture(p)
        label = labels[i] if labels else Path(p).stem
        cols.append(variant_column(img, label, tile=tile))
    return hstack(cols)
