# Shading & pixel technique reference

Read this before authoring. It is the accumulated craft knowledge the analyzer
heuristics in `aide/analyze.py` were built to check. When a lesson in
`knowledge/lessons.md` refines a rule here, fold it in (user-approved edits only).

## Ramps

A **ramp** is the ordered set of colors used to shade one material,
dark → light. Build the ramp *before* placing pixels.

- 16x16 textures: 3–5 steps per material ramp. More steps than that at 16x
  reads as mud because each step gets too few pixels to form a shape.
- 32x32: 4–6 steps. 64x/128x: 6–8, and cluster shading matters more than
  ramp length.
- Steps should be distinguishable at 1x on both dark and light backgrounds:
  aim for ~8–15% luminance between adjacent steps.

### Hue shifting

Never build a ramp by only sliding value (the analyzer calls this a "straight
value slide"). As a material goes into shadow, rotate its hue toward the cool
pole (blue/purple) and usually raise saturation a touch; toward highlights,
rotate toward the light source's color (warm yellow for default sunlight) and
drop saturation slightly.

- Typical shift for natural materials: 10–30° total across the ramp.
- Metals exaggerate: bigger value jumps between adjacent steps, stronger
  hue swing, and one near-specular highlight step used *sparsely*.
- Deliberate exceptions exist (eerie/magic light can shift warm-in-shadow);
  when a style card says so, it wins.

## Light direction

- Minecraft blocks: light reads from the **top**, slightly toward the
  viewer. Top edges of raised features get the highlight step; bottom edges
  get the shadow step. Left/right stay near base.
- Items (held/inventory sprites): vanilla idiom lights from **top-left**.

## The classic failures (what the analyzer flags)

- **Pillow shading**: shading in concentric rings around a shape's center
  regardless of light direction. Looks puffy and amateur. Fix: pick the light
  direction first, shade *forms*, not outlines. (`pillow_r` metric.)
- **Banding**: parallel single-pixel stripes of adjacent ramp steps hugging
  an edge — reads as a blurry outline. Fix: vary run lengths, merge steps,
  or break the band with clusters.
- **Straight value slides**: see hue shifting above. (`ramps` metric.)
- **Noise**: single stray pixels of a ramp step scattered to "add detail".
  At 16x, every pixel is ~6% of the width — strays read as dirt. Detail comes
  from **clusters** (2–5 px groups shaped like the material's micro-forms).
  (`busyness` metric — compare against the style card's target.)
- **Over-dithering**: checkerboard dithering is a last resort at 16x; vanilla
  barely uses it. At 64x+ it becomes a legitimate texture tool.

## Circles

Never freehand a pixel circle — use the odd-diameter circle chart at
`knowledge/references/pixel-circle-chart.webp` (user-provided, 2026-07-19)
and place its outline cells exactly. Freehand rounds come out lumpy
(the first aura-node orb did). For a 16x16 sprite, diameter 13 fills the
canvas with a 1px margin; 11 leaves room for glow/outline effects.

## Material shorthand

- **Wood planks**: vertical or horizontal grain in long 2–4 px clusters; one
  darker seam line per plank row; knots are 2x2 max, used rarely.
- **Stone**: irregular rounded clusters (potato shapes) of the mid steps with
  shadow only on each cluster's lower-right; avoid axis-aligned cracks.
- **Metal**: broad flat base regions, hard 2-step transitions, one bright
  specular cluster near the lit edge; brushed metal = long thin highlight runs.
- **Crystal/glass**: few large facets, each facet one flat step; highlight
  facet adjacent to shadow facet (no gradient between); binary alpha holes ok.
- **Organic/leaves**: high-frequency cluster noise is acceptable *here*;
  keep 2 hue families (lit leaf / shadow leaf) plus sparse accent.

## Tiling (blocks)

- Author with wrap-around in mind: a cluster that touches the right edge
  continues on the left edge at the same rows (the seam metrics check the
  luminance step across the wrap).
- Kill the "obvious repeat": avoid one high-contrast landmark pixel-group —
  in a 3x3 tile preview your eye finds it instantly. Distribute 2–3 medium
  features instead of 1 loud one.
- Check every block texture with `--tile` and eyeball the 3x3 strip.

## Size-specific notes

- **16x16**: every pixel is a decision; author the whole grid by hand in .pxg.
- **32x32**: still hand-authorable; think in 2x2 "brush".
- **64x/128x**: do not place pixels one at a time. Author a 16x or 32x
  *structure* first, upscale nearest-neighbor, then refine: re-cut stair-step
  curves, add intermediate ramp steps, re-cluster flat areas. Or compose
  programmatically with a short script importing `aide.grid`.

## Minecraft format rules

- Block/item textures: power-of-two square PNGs, RGBA.
- Prefer **binary alpha** (0 or 255). Semi-transparency needs special render
  layers for blocks and looks wrong on items. (`alpha.partial` metric.)
- House value rule for block albedo: keep luminance ~25–80% so blocks sit
  next to vanilla without glowing or reading as a hole. Accents may exceed it
  deliberately.
