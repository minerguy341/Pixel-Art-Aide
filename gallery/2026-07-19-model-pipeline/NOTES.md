# Model pipeline — read shape · auto-texture · render (any shape)

User request: read the shape of a model, generate a texture for it, and render
it even if it's not a full cube.

## What shipped (aide toolkit)

- `aide/model.py` — parse a Minecraft Java model's SHAPE: cuboid `elements`
  with per-face `uv`/`texture`/`tintindex`/`rotation`, `texture_size`,
  `textures` map (follows `#ref` chains). Synthesizes the standard element for
  the common `cube_all` / `cube_column` / `cube_bottom_top` / `cube` parents;
  errors clearly on other parents (needs the parent file's elements).
- `aide/modelrender.py` — `render_model()`: 2:1 iso render of any axis-aligned
  box model. Per-face UV sampling (per-texel quads, crisp), backface culling by
  normal, painter-sorted, exact vanilla face multipliers (up 1.0 / down 0.5 /
  N-S 0.8 / E-W 0.6), optional per-tintindex tint.
- `aide/autotex.py` — `autotexture()`: reads every face's UV rect and paints a
  directionally-shaded starter (top→highlight … bottom→shadow) with a 1px
  panel frame (Create idiom). Flags UV overlaps (same-texture overlaps on
  multi-shape blocks like stairs are expected — last face wins).
- CLI: `aide model <json> -o out.png` (auto-textures if no texture given;
  `--single` / `--tex key=path` / `--texdir` / `--tint idx=hex` / `--scale`);
  `aide autotex <json> -o tex.png` (`--base`, `--no-frame`).

## Verified

Smoke test extended (parse → autotex → render + cube_bottom_top synthesis).
Demo lineup `previews/model-pipeline-lineup.png`: the real T.N.A. wand item
model (rod + 2 caps, material-tinted), a stair auto-textured, the same stair
with the real plank texture, and the orrery from its `cube_bottom_top` parent.
`previews/stairs-autotex-10x.png` shows a generated starter texture.

## Limits (noted, not blocking)

- Element `rotation` (22.5° tilts) is read but rendered as axis-aligned; UV
  `rotation` (0/90/180/270) is honored.
- Non-`cube*` parents (block/stairs, block/orientable, …) need the parent's
  elements — supply a model with explicit `elements`, or extend `_CUBE_PARENTS`.
