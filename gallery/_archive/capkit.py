"""Shared silhouette-authoring helpers for wand-part sets (fantasy caps, pommels).

A part is a side view about a horizontal centreline: a short round collar/neck
where the shaft meets it, then a decorative body. `aide.lift` infers the third
dimension; this module just makes clean, symmetric `.pxg` silhouettes.
"""

from __future__ import annotations

import math

W, H = 46, 24
CY = (H - 1) / 2.0
HEAD_X0 = 13                       # bodies start here; neck overlaps 13–14


def blank():
    return [[False] * W for _ in range(H)]


def fill_col(m, x, half):
    """Fill column x symmetric about the half-integer centreline to ±half."""
    if x < 0 or x >= W or half <= 0:
        return
    n = int(round(half))
    for y in range(max(0, 12 - n), min(H - 1, 11 + n) + 1):
        m[y][x] = True


def symmetrize(m):
    return [[m[y][x] or m[(H - 1) - y][x] for x in range(W)] for y in range(H)]


def add_collar(m, collar_x1=8, neck_x1=14, collar_half=8, neck_half=2, rings=True):
    """Round ferrule (0..collar_x1) + thin neck (..neck_x1) that overlaps the body
    start so the lift always welds. Pommels pass a smaller collar."""
    for x in range(0, collar_x1 + 1):
        half = collar_half
        if rings:
            half += 1 if x in (1, max(1, collar_x1 - 2)) else -1 if x == 3 else 0
        fill_col(m, x, half)
    for x in range(collar_x1 + 1, neck_x1 + 1):
        fill_col(m, x, neck_half)


def head_span(x0=HEAD_X0):
    return range(x0, W)


def circle_halfs(cx, r):
    """Half-height of a circle of radius r centred at column cx (for orbs/beads)."""
    xs = list(head_span())
    return xs, [math.sqrt(max(0.0, r * r - (x - cx) ** 2)) for x in xs]


def to_pxg(m, base_hex="8A6BB6", note="silhouette") -> str:
    lines = [f"size: {W}x{H}", "[palette]", ". = none",
             f"a = {base_hex}   # {note}", "[grid]"]
    for y in range(H):
        lines.append("".join("a" if m[y][x] else "." for x in range(W)))
    return "\n".join(lines) + "\n"
