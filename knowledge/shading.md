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
- **Doubles**: the stray adjacent pixel a stroke leaves when it clips two
  cells of the grid — thickens a line unevenly and dents its flow. Distinct
  from noise (which is scattered singles); hunt doubles along every line.

## Outlines (selout)

- Items get an outline; blocks do not. When you outline, use **selective
  outlining**: on the lit (top-left) edge replace the dark line with a
  lighter *body* color, and keep the dark outline only where the form meets
  the background. A uniform keyline flattens the sprite and fights the light.
- The dark outline is a **dark version of the object's own darkest hue**,
  darker than whatever sits behind it — never pure `#000` (looks stickered,
  muddies the ramp, clashes on light backgrounds).

## Dithering — when and which

- Dither is a **texture/transition tool, not default shading**. Reach for a
  palette color first; dither only when you genuinely can't add one.
- **Size gate**: no dithering below ~16–32px or on small key shapes (keep it
  off 16x item icons — it just reads as noise). It earns its place on
  64–128px block surfaces where the pattern can resolve.
- For large smooth or **tiling/animated** fills use **ordered/Bayer** dither
  (2×2→8×8): the fixed matrix tiles seamlessly and stays stable frame to
  frame. Hand-scattered dither shimmers and "crawls" when tiled or animated.

## Anti-aliasing at low res

- Match an AA half-tone run's length to the **stair-step it softens** (short
  step → short nub); uniform dabs on unequal steps read as bumps.
- **Never AA a pure 45° line or a straight H/V run** — already clean; AA only
  blurs them and burns palette slots.
- Judge AA **and** dithering **at 1x nearest-neighbor, never zoomed**. If it
  only helps at 800% it does nothing at play size and adds a dirty halo.

## Color for form (beyond hue-shift)

- As a ramp climbs in brightness, **pull saturation down toward the
  highlights** (saturation peaks in the midtones). Bright + saturated pixels
  glow and read as radioactive.

## Palette economy

- **One ramp per material, shared endpoints**: give each material its own
  hue-shifted ramp, but let every ramp bottom out in the *same* near-black
  and top out in the *same* near-white/highlight. Anchors the whole palette
  and cuts slot count; unique black+white per material makes them feel like
  different games. (Ties to the style cards' per-material ```palette blocks.)
- **Each color earns multiple roles**: under a tight cap (~16), make one slot
  serve several contexts — a shadow that's also the darkest wood and a metal
  mid. Order colors into connected ramps so neighbors can be borrowed.
- Starting-point palettes to study: **Sweetie 16** (4 hue-shifted ramps,
  shared light/dark) and **Spectrum Ramps** on Lospec.

## Readability tests (run before shipping)

- **Silhouette test**: flood the whole sprite to one solid color — is it
  still identifiable? Interior detail can't rescue an ambiguous outline.
- **Squint / value test**: squint or blur until detail drops; adjacent
  shapes must still separate by *value*, not hue alone, or they merge into
  one blob at small size or in motion.

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
- **Wall variety ≠ seam-matching**: even a perfectly seamless single tile
  forms a visible grid at game distance. For blocks placed in bulk, author
  2–3 subtle variants (different crack/grain, one a touch darker) so
  placement variety breaks the repeat. Separate step from the 3x3 check.

## Size-specific notes

- **16x16**: every pixel is a decision; author the whole grid by hand in .pxg.
- **32x32**: still hand-authorable; think in 2x2 "brush".
- **64x/128x**: do not place pixels one at a time. Author a 16x or 32x
  *structure* first, upscale nearest-neighbor, then refine: re-cut stair-step
  curves, add intermediate ramp steps, re-cluster flat areas. Or compose
  programmatically with a short script importing `aide.grid`.

## Minecraft format rules

- Block/item textures: **power-of-two square** PNGs, RGBA (16, 32, 64…).
  Everything stitches into one atlas with up to 4 mip levels; a non-POT block
  sprite breaks clean mip halving and can blur the whole atlas. GUI textures
  are exempt (blitted, not stitched) — HD/non-POT widgets are fine.
- Prefer **binary alpha** (0 or 255). `cutout`/`cutout_mipped` layers hard-
  threshold alpha, so partial alpha won't soften edges — it fringes. Real
  translucency (glass, water) is the `translucent` layer. (`alpha.partial`.)
- **Alpha-bleed is automatic** on export (`save_texture`/`aide render`): every
  transparent pixel carries its nearest opaque neighbor's RGB so mipmaps don't
  grow dark halos at distance. Never hand-author black under transparency.
- **No isolated 1px detail on cutouts**: the first mip average erases 1px
  features and thin stems drop below the alpha threshold at range. Keep
  meaningful detail ≥2px; sparse 1px *accents* (a shimmer speck) are an
  accepted exception — they're meant to fade at distance.
- House value rule for block albedo: keep luminance ~25–80% so blocks sit
  next to vanilla without glowing or reading as a hole. Accents may exceed it
  deliberately.

## Directional face shading (the engine pre-shades for you)

Minecraft multiplies each face by a fixed constant **before** your texture's
own shading shows: **top 1.0 · bottom 0.5 · N/S 0.8 · E/W 0.6**.

- **Do not bake a top-to-bottom gradient into a block** — it double-shades.
- Paint side and bottom textures at **full brightness**, near-symmetric; one
  side texture serves all four walls (rendered at 0.8 on two, 0.6 on two), so
  a pre-darkened or asymmetric side reads inconsistently.
- `aide block` previews use these exact multipliers (top 1.0 / left 0.8 /
  right 0.6), so an iso preview matches how the block shades in-game.

## Tinting (grayscale-for-tint)

- A tinted texture is **multiplied** by its tint color, so author it in
  **grayscale / neutral** and let the tint supply the hue. Painting the hue in
  too doubles it (wrong, oversaturated). Our wand `wand_base` is grayscale for
  exactly this — the client tints rod/caps per material.
- A model face receives tint only if it declares `"tintindex"`. Vanilla-tinted
  slots: grass, leaves, plants, vines, water, redstone, leather, potions, map,
  spawn eggs, firework stars.

## Model / UV notes (when a texture maps onto a custom model)

- Java models are **per-face UV**, snapped to the pixel grid (off-grid blurs).
- Give every face its **own non-overlapping UV region** (+1px gutter) — two
  faces on one rectangle edit together and smear (the wand-model bug).
- Non-16 textures need `"texture_size":[w,h]` or texel density drifts.
- Point each block model's **`particle`** slot at its main texture, or break
  particles render the wrong/missing (purple) color.
- North is the model's default facing; author the "front" there or account for
  the blockstate `y` rotation. Avoid two coplanar faces at one depth (z-fight).

## Animated, mod, and pack specifics

- pack_format for **1.21.1 = 34**; layout `assets/<namespace>/textures/
  block|item/` (singular).
- `.mcmeta` animation: see the "Animated textures" section above.
- **[MOD/shader only — never a base-1.21.1 default]** CTM connected textures
  (OptiFine/Iris/Continuity), labPBR `_s`/`_n` maps, `_e` emissive overlays,
  and custom per-block colormaps. Flag and skip unless the pack targets them.

## Animated textures (.mcmeta — vanilla-safe on 1.21.1)

- Frames are a **single vertical strip**, top = frame 0 (a 16x16 block → a
  16×N px PNG = N frames); ship `<texture>.png.mcmeta` beside it. Non-square
  frames need explicit `width`/`height`.
- `frametime` = **ticks per frame** (1 = 20fps, the ceiling). Slow shimmer
  uses higher values; per-frame overrides via `{"index":4,"time":2}` and a
  reordered/repeated index list `[0,1,2,3,2]` for ping-pong.
- `interpolate: true` **crossfades** between listed frames, so author only a
  few keyframes at high `frametime` for smooth drift (water, glow). Leave it
  **off** for sharp motion (fire, bubbling lava) — it smears them.
- Frame-count by material: fire/portal ~32 (interp off); water/lava ~20–32
  (interp on); most decorative blocks want just a **2–4 frame shimmer at
  frametime 6–12**. Over-animating makes a wall "boil" and wastes VRAM.

## Mod / shader-only (out of scope for base 1.21.1 — flag, never default)

- **CTM / connected textures**: OptiFine/Iris/Continuity only. Not requested
  here; skip unless the pack explicitly targets those.
- **labPBR** specular/normal maps (`_s`: R=smoothness, G=reflectance,
  A=emission where 254=full and 255=ignored; `_n`=normal): shader-pack only.
  Renders nothing in unmodified 1.21.1 — never a default deliverable.
