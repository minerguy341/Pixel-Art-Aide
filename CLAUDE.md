# CLAUDE.md — Pixel-Art-Aide

A Claude-driven pixel-texture studio: the **pixel-artist skill**
(`.claude/skills/pixel-artist/SKILL.md`) is the main interface, the `aide`
Python package is its toolkit. Humans mostly interact by prompting for
textures and picking from contact sheets.

## Layout

| Path | What it is |
|---|---|
| `aide/` | Toolkit: `.pxg` format, rendering, analyzers, contact sheets, style parsing |
| `styles/*.md` | Style cards — palettes in ```palette blocks + prose rules + checklist |
| `knowledge/shading.md` | Craft reference; read before authoring |
| `knowledge/lessons.md` | Append-only lessons log — **user-approved entries only** |
| `gallery/` | One dir per session: `src/*.pxg`, `out/*.png`, `previews/`, `NOTES.md` |
| `tests/smoke.py` | End-to-end toolkit test |

## Commands

- Setup: `pip install -r requirements.txt` (just Pillow)
- Verify toolkit: `python3 tests/smoke.py` — this is the definition of "the toolkit works"
- CLI: `python3 -m aide {render,preview,analyze,compare,swatch,import}` (run from repo root; `--help` for flags)

## Hard rules

1. **Textures are authored as `.pxg` sources**; the PNG is a build product.
   Never commit a texture PNG without its source.
2. **Learning is user-gated.** Never edit `knowledge/lessons.md` or a style
   card without explicit user approval of the specific change in that session.
3. **Never claim in-game visual correctness** — previews and metrics only.
   Hand off with what was verified and what the user should eyeball.
4. `styles/thaumaturgy.md` mirrors `docs/art-direction.md` in the
   `thaumaturgy-the-new-age` repo; that doc is upstream. Don't invent palette
   values — sync from it.
5. Analyzer thresholds encode house rules; if a rule changes, change
   `aide/analyze.py` and the relevant doc together.

## Conventions

- Commit style: `area: what changed` (`aide: seam ratio in analyze`,
  `gallery: greatwood-planks r2`, `styles: create-mod busyness band`).
- Session dirs: `gallery/YYYY-MM-DD-<slug>/`, append-only.
- Python: 3.11+, Pillow only; no numpy unless a real need appears.
