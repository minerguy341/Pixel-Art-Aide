# arcane_stone — dressed arcane blue-grey ashlar (2026-07-20)

Authored for the T.N.A. Arcane Worktable slice: `arcane_stone` is both a building block and
the test recipe's output (4 stone → 4 arcane stone). It's the **neutral apparatus material**
from the design directives — a cool dressed blue-grey ashlar so saturated glow reads as the
magic against it, not the stone.

- Palette = the apparatus casing ramp (`242834` joint · `383E50` shadow · `474E62`/`414860`
  base · `5C6478` highlight). **No saturated fleck** — a single teal dot tiled into a regular
  grid artifact and fought the "neutral material" rule, so it's out (directives §0/§1).
- Seamless 16×16: offset ashlar courses (joints stagger across the wrap), top-lit edges,
  sparse deterministic grain (not a checker). Verified on a 3×3 tile (`previews/tiled3x3.png`).
- `src/make_arcane_stone.py` is the source of record; PNG copied to
  `thaumaturgy-the-new-age/.../textures/block/arcane_stone.png`.

The worktable's own faces reuse the existing `arcane_worktable_top/side/bottom` (the 3×3-grid
top from the revision pass) — exterior and the new screen now tell the same story.
