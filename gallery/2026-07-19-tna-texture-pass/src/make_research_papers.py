"""Research paper (flat, vanilla-style tilted sheet) + finished scroll sprites.

User direction (2026-07-19): flat papers must read like vanilla paper — a
tilted sheet with a folded corner, not a flat framed card. Finished research
is a rolled scroll with a wax seal whose color tells the tier. Seal colors
are unified across both families:

    fledgling gray -> apprentice brass -> scholar blue -> master aetherium
    -> grandmaster gold (+ teal glint)

Flat papers additionally accumulate ink lines with tier (1/2/3/3/3).
Run from the Pixel-Art-Aide repo root:
    python3 gallery/2026-07-19-tna-texture-pass/src/make_research_papers.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aide.grid import Pxg, parse_color, to_image, to_text

SESSION = Path(__file__).resolve().parents[1]

COMMON = {
    ".": "none",
    "X": "8F8875",  # border shade
    "P": "EDE9DC",  # sheet light
    "p": "DCD5C0",  # sheet mid (fold face, under-edges)
    "d": "C2BAA2",  # sheet shade (scroll end curls)
    "i": "6E6880",  # ink
    "g": "7FE8D8",  # teal glint (grandmaster only)
}

# (highlight, base, lowlight) wax per tier; lowlight doubles as ribbon color
SEALS = {
    "fledgling": ("B0705C", "8A4E3E", "663A2E"),
    "apprentice": ("E8C983", "C79A55", "8F6B38"),
    "scholar": ("6EB5E8", "3D9BE0", "2A6FA8"),
    "master": ("B99BE0", "8A6BB5", "5A4380"),
    "grandmaster": ("F7DC6A", "F2C230", "A8861F"),
}
INK_LINES = {"fledgling": 1, "apprentice": 2, "scholar": 3, "master": 3, "grandmaster": 3}

# Tilted sheet: column bands step up left->right; folded corner top-left
# (p face, X crease); inner shade p along the right and bottom edges.
SHEET = [
    "................",
    "...........XXX..",
    "........XXXPPX..",
    ".....XXXPPPPpX..",
    "..XXXPPPPPPPpX..",
    "..XpXPPPPPPPpX..",
    "..XXPPPPPPPPpX..",
    "..XPPPPPPPPPpX..",
    "..XPPPPPPPPPpX..",
    "..XPPPPPPPPppX..",
    "..XPPPPPPppXXX..",
    "..XPPPppXXX.....",
    "..XppXXX........",
    "..XXX...........",
    "................",
    "................",
]

# Vertical scroll, rolled ends (d curls), ribbon band rows 6-7, seal on top.
SCROLL = [
    "................",
    "....XXXXXXXX....",
    "...XPPdPPdPpX...",
    "...XPPPPPPPpX...",
    "...XPPPPPPPpX...",
    "...XPPPPPPPpX...",
    "...XRRRRRRRRX...",
    "...XRRRRRRRRX...",
    "...XPPPPPPPpX...",
    "...XPPPPPPPpX...",
    "...XPPPPPPPpX...",
    "...XPPPPPPPpX...",
    "...XPPdPPdPpX...",
    "....XXXXXXXX....",
    "................",
    "................",
]

# Stepped ink lines following the sheet tilt: (row, start col, pattern)
INK = [(7, 4, "iiPii"), (9, 4, "iiii"), (11, 4, "iii")]


def seal_cells(cx: int, cy: int, glint: bool) -> dict:
    """Rounded 3x3 wax blob with top-left corner (cx, cy), lit top-left."""
    return {
        (cx, cy): "1", (cx + 1, cy): "2", (cx + 2, cy): "3",
        (cx, cy + 1): "2", (cx + 1, cy + 1): "g" if glint else "2", (cx + 2, cy + 1): "3",
        (cx, cy + 2): "2", (cx + 1, cy + 2): "3", (cx + 2, cy + 2): "3",
    }


def build(base: list[str], tier: str, kind: str) -> Pxg:
    hi, mid, lo = SEALS[tier]
    glint = tier == "grandmaster"
    rows = [list(r) for r in base]
    if kind == "paper":
        for row, start, pattern in INK[: INK_LINES[tier]]:
            for i, ch in enumerate(pattern):
                if ch == "i":
                    rows[row][start + i] = "i"
        cells = seal_cells(10, 7, glint)
    else:
        cells = seal_cells(7, 6, glint)
    for (x, y), ch in cells.items():
        rows[y][x] = ch
    palette = dict(COMMON)
    palette.update({"1": hi, "2": mid, "3": lo, "R": lo})
    pal = {k: parse_color(v) for k, v in palette.items()}
    grid = ["".join(r).replace("R", "R") for r in rows]
    # scroll base uses R for ribbon; paper base has none — harmless either way
    return Pxg(width=16, height=16, palette=pal, rows=grid)


def main() -> None:
    comments = {"1": "seal highlight", "2": "seal base", "3": "seal lowlight / ribbon"}
    for tier in SEALS:
        for kind, base, stem in [
            ("paper", SHEET, f"research_paper_{tier}"),
            ("scroll", SCROLL, f"research_scroll_{tier}"),
        ]:
            pxg = build(base, tier, kind)
            (SESSION / "src" / f"{stem}.pxg").write_text(to_text(pxg, comments))
            to_image(pxg).save(SESSION / "out" / f"{stem}.png")
            print(stem)


if __name__ == "__main__":
    main()
