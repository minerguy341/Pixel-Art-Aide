#!/usr/bin/env python3
"""Assemble 4 contact sheets (greatwood/silverwood x log/leaves), each showing every
candidate with BOTH requested views: logs = 2x3 tile + 3-tall trunk; leaves = 3x3 tile
+ block render. Labelled, on a neutral mid-grey so pale silverwood and dark greatwood
both read."""
from pathlib import Path
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
PREV = HERE.parent / "previews"
BG = (110, 110, 116, 255)
INK = (250, 250, 250, 255)
PAD = 16
GAP = 20


def load(name):
    return Image.open(PREV / name).convert("RGBA")


def row(views, label):
    """One candidate: a label strip + its view images side by side."""
    h = max(v.height for v in views)
    w = sum(v.width for v in views) + GAP * (len(views) - 1)
    strip = Image.new("RGBA", (w, h + 22), (0, 0, 0, 0))
    x = 0
    for v in views:
        strip.alpha_composite(v, (x, 22 + (h - v.height)))
        x += v.width + GAP
    d = ImageDraw.Draw(strip)
    d.text((0, 4), label, fill=INK)
    return strip


def sheet(title, rows, out):
    w = max(r.width for r in rows) + 2 * PAD
    h = sum(r.height for r in rows) + GAP * (len(rows) - 1) + 2 * PAD + 26
    canvas = Image.new("RGBA", (w, h), BG)
    d = ImageDraw.Draw(canvas)
    d.text((PAD, 8), title, fill=INK)
    y = 30
    for r in rows:
        canvas.alpha_composite(r, (PAD, y))
        y += r.height + GAP
    canvas.save(out)
    print("wrote", out.name, canvas.size)


def log_row(name, label):
    return row([load(f"{name}_tile2x3.png"), load(f"{name}_trunk3.png")], label)


def leaf_row(name, label):
    return row([load(f"{name}_tile3x3.png"), load(f"{name}_block.png")], label)


sheet("GREATWOOD LOG  -  candidates (2x3 tile | 3-tall trunk)", [
    log_row("greatwood_log_straight", "A  straight - calm deep furrows"),
    log_row("greatwood_log_gnarled", "B  gnarled - furrows + small knots"),
    log_row("greatwood_log_plated", "C  plated - craggy cross-cracked bark"),
], PREV / "sheet-greatwood-log.png")

sheet("SILVERWOOD LOG  -  candidates (2x3 tile | 3-tall trunk)", [
    log_row("silverwood_log_smooth", "A  smooth - birch bark + sparse teal shimmer"),
    log_row("silverwood_log_lenticel", "B  lenticel - birch eye-dashes + teal"),
    log_row("silverwood_log_shimmer", "C  shimmer - faint teal seam, more magic"),
], PREV / "sheet-silverwood-log.png")

sheet("GREATWOOD LEAVES  -  candidates (3x3 tile | block)", [
    leaf_row("greatwood_leaves_broadleaf", "A  broadleaf - 33% holes, airy"),
    leaf_row("greatwood_leaves_dense", "B  dense - 22% holes, fuller canopy"),
    leaf_row("greatwood_leaves_accent", "C  accent - 32% holes + rare dead-leaf fleck"),
], PREV / "sheet-greatwood-leaves.png")

sheet("SILVERWOOD LEAVES  -  candidates (3x3 tile | block)", [
    leaf_row("silverwood_leaves_airy", "A  airy - 33% holes, sparse teal shimmer"),
    leaf_row("silverwood_leaves_canopy", "B  canopy - 18% holes, dense magic canopy"),
    leaf_row("silverwood_leaves_glow", "C  glow - 30% holes, more teal shimmer"),
], PREV / "sheet-silverwood-leaves.png")
