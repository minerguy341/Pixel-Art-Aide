"""Compose the 5 tier-graded research paper sprites from one base sheet.

Tier grammar: writing lines accumulate with tier; seal steps brass ->
aetherium; grandmaster adds a teal seal-glint and gilt border corners.
Run from the Pixel-Art-Aide repo root:
    python3 gallery/2026-07-19-tna-texture-pass/src/make_research_papers.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from aide.grid import Pxg, parse_color, to_image, to_text

SESSION = Path(__file__).resolve().parents[1]

PALETTE = {
    ".": "none",
    "X": "8F8875",  # border shade
    "P": "EDE9DC",  # sheet light (forma cream)
    "p": "DCD5C0",  # sheet mid
    "d": "C2BAA2",  # sheet shade
    "i": "6E6880",  # ink (gray-purple)
    "n": "8F6B38",  # brass shadow
    "m": "C79A55",  # brass base
    "o": "E8C983",  # brass highlight
    "q": "8A6BB5",  # aetherium base
    "r": "B99BE0",  # aetherium highlight
    "g": "7FE8D8",  # teal glint
}

# Lit top/left edges stay paper-toned; border-shade only bottom/right.
BASE = [
    "................",
    "..ppppppppppppX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pPPPPPPPPPpdX.",
    "..pppppppppppdX.",
    "..XXXXXXXXXXXXX.",
    "................",
    "................",
]

# Ink lines: (row, string placed starting at col 4). Varied lengths/breaks.
INK = {
    4: "iiiii.ii",
    6: "ii.iiii",
    8: "iiiiii",
    10: "iii.ii",
}

def seal(cells: dict, kind: str, glint: bool = False) -> None:
    hi, base_, lo = (("o", "m", "n") if kind == "brass" else ("r", "q", "n"))
    if kind == "aetherium":
        lo = "5A4380"  # placed via direct key below
    # rounded 3x3 wax blob centered (10,10), lit top-left
    cells[(9, 9)] = hi
    cells[(10, 9)] = base_
    cells[(11, 9)] = "s_lo"
    cells[(9, 10)] = base_
    cells[(10, 10)] = "g" if glint else base_
    cells[(11, 10)] = "s_lo"
    cells[(9, 11)] = base_
    cells[(10, 11)] = "s_lo"
    cells[(11, 11)] = "s_lo"

TIERS = {
    "fledgling": {"ink_rows": [4], "seal": None},
    "apprentice": {"ink_rows": [4, 6], "seal": "brass"},
    "scholar": {"ink_rows": [4, 6, 8], "seal": "brass", "ribbon": True},
    "master": {"ink_rows": [4, 6, 8, 10], "seal": "aetherium"},
    "grandmaster": {"ink_rows": [4, 6, 8, 10], "seal": "aetherium", "glint": True, "gilt": True},
}

def build(tier: str, spec: dict) -> Pxg:
    rows = [list(r) for r in BASE]
    for row in spec["ink_rows"]:
        for i, ch in enumerate(INK[row]):
            if ch == "i":
                rows[row][4 + i] = "i"
    cells: dict = {}
    if spec.get("seal"):
        seal(cells, spec["seal"], glint=spec.get("glint", False))
    if spec.get("ribbon"):
        cells[(9, 12)] = "s_lo"
        cells[(11, 12)] = "s_lo"
    lo_key = "n" if spec.get("seal") == "brass" else "u"
    for (x, y), ch in cells.items():
        rows[y][x] = lo_key if ch == "s_lo" else ch
    if spec.get("gilt"):
        for x, y in [(2, 1), (13, 1), (2, 13), (13, 13)]:
            rows[y][x] = "o"
    palette = dict(PALETTE)
    palette["u"] = "5A4380"  # aetherium shadow (seal lowlight)
    pal = {k: parse_color(v) for k, v in palette.items()}
    return Pxg(width=16, height=16, palette=pal, rows=["".join(r) for r in rows])

def main() -> None:
    comments = {"u": "aetherium shadow"}
    for tier, spec in TIERS.items():
        pxg = build(tier, spec)
        name = f"research_paper_{tier}"
        (SESSION / "src" / f"{name}.pxg").write_text(to_text(pxg, comments))
        to_image(pxg).save(SESSION / "out" / f"{name}.png")
        print(name)

if __name__ == "__main__":
    main()
