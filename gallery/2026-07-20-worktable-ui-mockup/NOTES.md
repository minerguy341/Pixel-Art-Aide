# worktable-ui-mockup

Geometry check for ArcaneWorktableScreen (T.N.A.) — mirrors the Java slot/ring/label
coords to eyeball placement without a game build. Confirmed: vis ring encircles the
grid with no pips inside cells; wand/result/arrow/cost all clear. mockup.png (3x).

## Primal glyphs + per-primal worktable layout
- src/make_glyphs.py downscales the 6 aspect icons to 16px GUI glyphs (copied to the mod
  at textures/gui/aspect/*.png). mockup_primals.png verified the hexagon geometry.
