"""Rendering helpers: nearest-neighbor upscales, grids, tiling, preview sheets."""

from __future__ import annotations

from PIL import Image, ImageDraw

CHECKER_A = (58, 58, 62, 255)
CHECKER_B = (72, 72, 78, 255)
SHEET_BG = (34, 34, 38, 255)
LABEL_FG = (225, 225, 220, 255)
GRID_LINE = (0, 0, 0, 90)


def upscale(img: Image.Image, factor: int) -> Image.Image:
    return img.resize((img.width * factor, img.height * factor), Image.NEAREST)


def checkerboard(w: int, h: int, cell: int = 8) -> Image.Image:
    bg = Image.new("RGBA", (w, h))
    d = ImageDraw.Draw(bg)
    for y in range(0, h, cell):
        for x in range(0, w, cell):
            c = CHECKER_A if ((x // cell) + (y // cell)) % 2 == 0 else CHECKER_B
            d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=c)
    return bg


def on_checker(img: Image.Image, cell: int = 8) -> Image.Image:
    bg = checkerboard(img.width, img.height, cell)
    bg.alpha_composite(img)
    return bg


def grid_overlay(img: Image.Image, factor: int) -> Image.Image:
    """Upscale and draw pixel-boundary gridlines."""
    big = upscale(img, factor).convert("RGBA")
    d = ImageDraw.Draw(big, "RGBA")
    for x in range(0, big.width + 1, factor):
        d.line([(x, 0), (x, big.height)], fill=GRID_LINE)
    for y in range(0, big.height + 1, factor):
        d.line([(0, y), (big.width, y)], fill=GRID_LINE)
    return big


def tiled(img: Image.Image, nx: int = 3, ny: int = 3) -> Image.Image:
    out = Image.new("RGBA", (img.width * nx, img.height * ny))
    for j in range(ny):
        for i in range(nx):
            out.paste(img, (i * img.width, j * img.height))
    return out


def palette_strip(img: Image.Image, swatch: int = 14) -> Image.Image:
    """Unique opaque-ish colors sorted dark->light as a swatch row."""
    from aide.analyze import luminance

    rgba = img.convert("RGBA")
    px = rgba.load()
    counts: dict[tuple, int] = {}
    for y in range(rgba.height):
        for x in range(rgba.width):
            c = px[x, y]
            if c[3] > 0:
                counts[c] = counts.get(c, 0) + 1
    colors = sorted(counts, key=lambda c: luminance(c))
    strip = Image.new("RGBA", (max(1, swatch * len(colors)), swatch), SHEET_BG)
    d = ImageDraw.Draw(strip)
    for i, c in enumerate(colors):
        d.rectangle([i * swatch, 0, (i + 1) * swatch - 1, swatch - 1], fill=c)
    return strip


def _label(text: str, width: int) -> Image.Image:
    im = Image.new("RGBA", (width, 14), SHEET_BG)
    ImageDraw.Draw(im).text((2, 1), text, fill=LABEL_FG)
    return im


def stack(blocks: list[Image.Image], pad: int = 6, bg=SHEET_BG) -> Image.Image:
    """Stack image blocks vertically, left-aligned, on the sheet background."""
    w = max(b.width for b in blocks) + pad * 2
    h = sum(b.height for b in blocks) + pad * (len(blocks) + 1)
    out = Image.new("RGBA", (w, h), bg)
    y = pad
    for b in blocks:
        out.alpha_composite(b, (pad, y))
        y += b.height + pad
    return out


def hstack(blocks: list[Image.Image], pad: int = 10, bg=SHEET_BG) -> Image.Image:
    w = sum(b.width for b in blocks) + pad * (len(blocks) + 1)
    h = max(b.height for b in blocks) + pad * 2
    out = Image.new("RGBA", (w, h), bg)
    x = pad
    for b in blocks:
        out.alpha_composite(b, (x, pad))
        x += b.width + pad
    return out


def preview_sheet(img: Image.Image, label: str = "", tile: bool = False) -> Image.Image:
    """One texture's full preview: 1x, big upscale, gridded upscale, optional 3x3 tiling, palette."""
    factor = max(4, 192 // img.width)
    blocks = [
        _label(f"{label}  {img.width}x{img.height}", 200),
        on_checker(img, cell=4),
        on_checker(upscale(img, factor), cell=8),
        grid_overlay(img, factor),
    ]
    if tile:
        tile_factor = max(2, 64 // img.width)
        blocks.append(_label("tiled 3x3", 200))
        blocks.append(upscale(tiled(img), tile_factor))
    blocks.append(palette_strip(img))
    return stack(blocks)
