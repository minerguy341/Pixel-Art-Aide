# Chipped study — textures & models (2026-07-19)

Studied terrarium-earth/Chipped (branch 1.21.x) in the scratchpad per
reference-policy.md — general craft only, no Chipped textures/models committed.
Rendered three workbenches through `aide.modelrender` as a study demo (shown to
the user transiently, not committed). CTM loading intentionally NOT studied —
Fusion is the studio's preferred CTM path (see reference/fusion-ctm.md).

## What Chipped does (derived observations)

1. **HD 64×64 textures** — 4× vanilla's 16. Chipped invests in resolution for
   smooth decorative furniture detail; one texture atlas per model.
2. **Real Blockbench furniture models, not cube variants** — its workbenches
   are 9–30 axis-aligned box elements (legs, apron, tabletop, tools) whose
   faces all UV-map onto the single 64×64 atlas. `texture_size: [64,64]`.
   (Model files credit "Made with Blockbench".)
3. **Themed workbench family** — carpenter (saw/wood), botanist (plants),
   glassblower (kiln/copper-red), alchemy, loom, mason, tinkering: a shared
   table silhouette re-dressed with profession props + a themed palette. The
   furniture analog of "one arrangement, many palettes".
4. **Variant-driven mod** — Chipped's core is many decorative variants of one
   vanilla block, picked in a chiseling GUI. A decorative mod scales by
   re-texturing/re-modelling ONE silhouette many ways.
5. **Elements exceed the 16-cube** — e.g. the carpenter's tabletop spans x
   0→32; Chipped furniture overhangs the block for a fuller read (MC allows
   element coords −16…32).

## Toolkit validation

`render_model` handled a real 64×64, 30-element Chipped model with fractional
UVs (e.g. `[10.25,10.75,11,13.5]`) and out-of-cube coords, producing coherent
tables. Good robustness signal for the model pipeline.

**Limitation surfaced:** element `rotation` with a real angle (22.5/45°) still
renders axis-aligned — these workbenches all use angle 0 (origin only), so they
render faithfully, but a Chipped model that tilts an element would be slightly
off. Real element rotation is the next renderer upgrade if we need it.

## Candidate lessons (pending user approval)

- Detailed furniture blocks = a Blockbench multi-element model + one HD (32/64)
  texture atlas with non-overlapping UV islands — not a cube. (Relevant if the
  arcane worktable ever graduates from a cube to a modelled table.)
- A workbench/furniture family = one table silhouette re-dressed per theme
  (props + palette) — the furniture analog of one-arrangement-many-palettes.
