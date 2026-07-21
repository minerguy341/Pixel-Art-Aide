# CLAUDE.md — Pixel-Art-Aide

A Claude-driven pixel-texture studio: the **pixel-artist skill**
(`.claude/skills/pixel-artist/SKILL.md`) is the main interface, the `aide`
Python package is its toolkit. Humans mostly interact by prompting for
textures and picking from contact sheets.

## Layout

| Path | What it is |
|---|---|
| `aide/` | Toolkit: `.pxg` format, rendering, analyzers, contact sheets, style parsing, model read/render/auto-texture, silhouette→3D lift |
| `styles/*.md` | Style cards — palettes in ```palette blocks + prose rules + checklist |
| `knowledge/shading.md` | Craft reference; read before authoring |
| `knowledge/lessons.md` | Append-only lessons log — **user-approved entries only** |
| `knowledge/reference-policy.md` | Licensing: study the look, never ship others' pixels; refs stay in scratchpad |
| `gallery/` | One dir per session: `src/*.pxg`, `out/*.png`, `previews/`, `NOTES.md` |
| `tests/smoke.py` | End-to-end toolkit test |

## Commands

- Setup: `pip install -r requirements.txt` (just Pillow)
- Verify toolkit: `python3 tests/smoke.py` — this is the definition of "the toolkit works"
- CLI: `python3 -m aide {render,preview,analyze,compare,swatch,import,bleed,block,model,autotex,lift}` (run from repo root; `--help` for flags)
- Model pipeline: `python3 -m aide model <model.json> -o out.png` reads any Minecraft
  model's shape and renders it (auto-textures if no `--tex/--single/--texdir`
  given); `python3 -m aide autotex <model.json> -o tex.png` writes a starter
  texture laid out for the model's UVs. Works for non-cube shapes (stairs,
  rods, multi-element items).
- Model-from-art (the inverse): `python3 -m aide lift <silhouette.pxg/.png> --html view.html`
  infers a third dimension from a flat side-view silhouette and writes a voxel
  model. `--mode revolve` laths the profile about its long axis (round finials);
  `--mode blade` keeps the outline and gives it an edge-tapered thickness (flat
  forged shapes). Emits `.obj`, an iso preview PNG, and/or a self-contained
  rotatable WebGL page (mouse + touch, no external requests). Geometry only —
  untextured (see `aide/lift.py`, `aide/liftviewer.py`).

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
5. **Study the look, never ship others' pixels** (`knowledge/reference-policy.md`).
   Reference files (vanilla, mods) live in the session scratchpad only — never
   commit them. Learn general craft (palettes, structure, idioms); never trace
   or reproduce a specific mod's texture.
6. Analyzer thresholds encode house rules; if a rule changes, change
   `aide/analyze.py` and the relevant doc together.

## Conventions

- Commit style: `area: what changed` (`aide: seam ratio in analyze`,
  `gallery: greatwood-planks r2`, `styles: create-mod busyness band`).
- Session dirs: `gallery/YYYY-MM-DD-<slug>/`, append-only.
- Python: 3.11+, Pillow only; no numpy unless a real need appears.
