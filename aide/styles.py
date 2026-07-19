"""Style-card support.

Style cards are markdown files in styles/. Machine-readable palettes live in
fenced code blocks whose info string starts with `palette`, e.g.:

    ```palette greatwood_planks
    shadow    = 5E4530
    base      = 7A5B3C
    highlight = 8F6E4B
    ```

Lines are `name = RRGGBB[AA]`. Everything else in the card is prose for the
authoring agent.
"""

from __future__ import annotations

import re
from pathlib import Path

from PIL import Image, ImageDraw

from aide.grid import RGBA, parse_color
from aide.render import SHEET_BG, LABEL_FG, stack

_FENCE_RE = re.compile(r"^```palette\s*(\S*)\s*$")


def parse_style_palettes(text: str) -> dict[str, list[tuple[str, RGBA]]]:
    palettes: dict[str, list[tuple[str, RGBA]]] = {}
    current: str | None = None
    count = 0
    for line in text.splitlines():
        stripped = line.strip()
        if current is None:
            m = _FENCE_RE.match(stripped)
            if m:
                count += 1
                current = m.group(1) or f"palette_{count}"
                palettes[current] = []
        elif stripped.startswith("```"):
            current = None
        elif stripped and not stripped.startswith("#"):
            m = re.match(r"^(\S+)\s*=\s*(\S+)$", stripped)
            if m:
                palettes[current].append((m.group(1), parse_color(m.group(2))))
    return palettes


def load_style_palettes(path: str | Path) -> dict[str, list[tuple[str, RGBA]]]:
    return parse_style_palettes(Path(path).read_text())


def swatch_sheet(palettes: dict[str, list[tuple[str, RGBA]]], swatch: int = 22) -> Image.Image:
    blocks = []
    for name, colors in palettes.items():
        label = Image.new("RGBA", (max(80, 6 * len(name) + 8), 14), SHEET_BG)
        ImageDraw.Draw(label).text((2, 1), name, fill=LABEL_FG)
        row = Image.new("RGBA", (max(1, swatch * len(colors)), swatch), SHEET_BG)
        d = ImageDraw.Draw(row)
        for i, (_, c) in enumerate(colors):
            d.rectangle([i * swatch, 0, (i + 1) * swatch - 1, swatch - 1], fill=c)
        blocks.append(label)
        blocks.append(row)
    return stack(blocks, pad=4)
