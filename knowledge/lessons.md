# Lessons log

Append-only. Every entry was **approved by the user** before landing — the
skill proposes candidate lessons at the end of a session and commits only the
approved ones (see the pixel-artist skill, "Learning" section).

Future sessions: read this whole file before authoring. When a lesson has
graduated into `knowledge/shading.md` or a style card, its entry stays here
with a `[folded into …]` marker so the history remains.

Entry format:

    ## YYYY-MM-DD — short title
    - Context: what was being made, which style
    - Observation: what went wrong / what worked unusually well
    - Rule: the reusable takeaway, stated as an instruction

---

## 2026-07-19 — grain reads as dirt below 3px
- Context: greatwood planks (thaumaturgy style), 16x16, session r1
- Observation: 2px shadow clusters scattered as "grain" read as dirt blobs
  and pushed the texture toward brick
- Rule: at 16x, wood grain is runs of 3px+ along the plank direction; never
  lone 1–2px flecks

## 2026-07-19 — seam-ratio false alarm on banded textures
- Context: same session; analyzer tiling metric on all plank candidates
- Observation: seam_ratio scored 1.48–1.93 while the 3x3 previews were
  visually seamless — the wrap edge *is* a plank seam, identical to the
  interior ones, so the metric's interior average (diluted by flat runs)
  understates legitimate seam contrast
- Rule: when the wrap edge coincides with a designed seam line, treat an
  elevated seam_ratio as a false alarm once the 3x3 preview is clean
  (candidate for a smarter check in `aide/analyze.py` eventually)

## 2026-07-19 — accent colors must beat the border, not just each other
- Context: research paper tier seals (T.N.A. texture pass, iteration 5)
- Observation: a gray wax seal was invisible against the sheet's gray
  border-shade even though it was distinct from the other four seal colors
- Rule: pick accent/marker colors against the sprite's border-shade family
  first; distinctness within the accent set alone is not enough

## 2026-07-19 — paper-family items tilt
- Context: research papers r1-r2 read as framed UI cards
- Observation: an axis-aligned sheet at 16x reads as interface, not item;
  vanilla paper is a diagonal kite with a folded corner
- Rule: flat sheet items (paper, notes, maps) use the tilted vanilla
  silhouette; text/ornament follows the sheet's rotation (the lower-left
  "\" edge is the bottom; content flows top-left -> down-right)

## 2026-07-19 — vanilla wood grammar
- Context: plank/log rebuild after studying real 1.21.1 assets
- Observation: vanilla planks have NO vertical joints; grain is 1-5px runs
  of 4-5 close tones (<~10% luminance apart); seam rows are broken mixes of
  three darks. My staggered joints + discrete dark clusters read as bricks
- Rule: wood grain = runs of close tones, seams broken, no full-height
  joints; save discrete high-contrast clusters for stone

## 2026-07-19 — one arrangement, many palettes
- Context: same study; spruce and birch planks are the identical pixel grid
- Observation: vanilla achieves family consistency by recoloring a single
  arrangement per material class
- Rule: author one arrangement per family (planks, logs, saplings...) and
  recolor per material; do not redraw structure per material

## 2026-07-19 — import real refs, not memory
- Context: nugget/ingot/paper vanilla-matching (user linked mcasset.cloud)
- Observation: from-memory approximations got the nugget ~50% too big and
  the ingot on the wrong axis; importing the real sprite and mapping roles
  cell-for-cell fixed both immediately
- Rule: when matching vanilla, fetch the actual sprite (mcasset /
  InventivetalentDev minecraft-assets) and `aide import` it; never draw a
  vanilla shape from memory

## 2026-07-19 — re-anchor transplanted ramps
- Context: brass ingot direct role-map from gold read butter-pale
- Observation: color-role transplants from a saturated material to a muted
  one overbrighten, because the bright roles dominate coverage
- Rule: after transplanting a role map, re-anchor each role to the target
  material's card ramp (bright role = card highlight, not lighter)

## 2026-07-19 — vanilla refs stay out of the repos
- Context: same reference workflow
- Observation: reference PNGs are Mojang assets; committing them would
  violate the no-asset-reuse rule even as "references"
- Rule: vanilla refs live in the session scratchpad only; only silhouettes
  and structural grammar are learned from them, never pixels, and nothing
  vanilla is ever committed to either repo

## 2026-07-19 — hue shift lives in the extension steps
- Context: same session; thaumaturgy card fixes greatwood's 3 core steps,
  analyzer flagged the ramp as a straight value slide
- Observation: cool-shifting only the *added* deep seam step (4A3625 →
  4A312C) gave the ramp a 21° cool-ward shadow drift without touching any
  card color
- Rule: when a style card fixes a ramp's core steps, carry the hue shifting
  in the steps you add (deep shadows, speculars)

---

# Researched lessons — 2026-07-19

The block below was distilled from web pixel-art tutorials (Saint11,
Slynyrd, MortMort, Pixel Parmesan, Lospec, Pixnote, Derek Yu) and **approved
by the user** in this session. Sources are cited per entry.

## 2026-07-19 — AA run length matches the step it softens
- Rule: an anti-alias half-tone run should be as long as the stair-step it
  smooths (2-long step → short nub, 4-long → longer); uniform AA dabs on
  unequal steps read as bumps, lumpier than the raw jaggies
- Source: Saint11 "Anti-Alias and Banding"; Lospec/st0ven

## 2026-07-19 — don't AA clean lines
- Rule: never anti-alias a pure 45° line or a perfectly straight H/V run —
  those edges are already clean; intermediate pixels only blur them and burn
  palette slots (costly at 16x)
- Source: MortMort "Basic Anti-Aliasing"; Pixel Parmesan

## 2026-07-19 — judge AA and dithering at 1x only
- Rule: evaluate anti-aliasing and dithering at 1x nearest-neighbor, never
  zoomed; smoothing visible only at 800% does nothing at play size and often
  adds a faint dirty halo. (Extends the existing "eyeball the preview" rule.)
- Source: "Dithering in Pixel Art — When to Use It"

## 2026-07-19 — selective outlining (selout)
- Rule: on the lit (top-left) edge, replace the dark outline with a lighter
  body color; keep the dark outline only where the form meets the
  background. A uniform black keyline flattens the sprite and fights the
  light direction
- Source: Pixnote "Sel-Out"; yarrninja Ch.12

## 2026-07-19 — outlines are tinted dark, never pure black
- Rule: outline with a dark version of the object's own darkest hue, and
  make it darker than whatever sits behind it — pure #000 looks stickered,
  muddies the ramp, and clashes on light backgrounds
- Source: Lospec "Pixel Art Outlines Part 2: Using Color"

## 2026-07-19 — dither is a texture tool, not default shading
- Rule: reach for a palette color first; dither only when you genuinely
  can't add one. Habitual checkerboarding makes busy, crunchy surfaces and
  hides a missing midtone a single flat color renders cleaner
- Source: Pixel Parmesan "Dithering for Pixel Artists"; Spearite

## 2026-07-19 — dither size gate
- Rule: no dithering below ~16–32px or on small key shapes (keep it off 16x
  item icons); reserve it for 64–128 block surfaces where the pattern can
  resolve. Below that it just reads as noise
- Source: "Dithering in Pixel Art — When to Use It"

## 2026-07-19 — ordered/Bayer dither for tiling and animated fills
- Rule: for large smooth or tiling fills use ordered/Bayer dither (2x2→8x8);
  its fixed matrix tiles seamlessly and stays stable frame to frame, where
  hand-scattered dither shimmers and "crawls" — ideal for animated MC blocks
  (water, foliage). Pairs with the seamless-tiling rule in shading.md
- Source: ASCII Magic "Complete Guide to Dithering"; Pixnote

## 2026-07-19 — clean diagonals and no doubles
- Rule: build diagonals from equal-length segments; if you must mix lengths,
  vary them monotonically (5-2-2-1-1, never 5-2-1-2-1) or a short segment
  sandwiched between longer ones lumps the curve. Separately, hunt and
  remove "doubles" — the stray adjacent pixel a stroke leaves when it clips
  two cells — which thickens a line unevenly (distinct from scattered noise)
- Source: Derek Yu "Pixel Art Basics"; OpenGameArt; Lospec "Lines/Curves/Jaggies"

## 2026-07-19 — desaturate toward the highlights
- Rule: as a ramp climbs in brightness, pull saturation down toward the
  highlights (let saturation peak in the midtones); high-brightness +
  high-saturation pixels glow/vibrate and look radioactive. (Complements the
  hue-shift lesson — that governs hue, this governs saturation.)
- Source: Slynyrd "Pixelblog 1: Color Palettes"

## 2026-07-19 — silhouette test
- Rule: flood the whole sprite/icon to one solid color and check it is still
  identifiable; interior detailing can't rescue an ambiguous outline, and if
  the silhouette fails the icon won't read in an inventory or at a glance.
  (Formalizes the "readable silhouette at 1x" checklist item)
- Source: Pixnote glossary

## 2026-07-19 — squint / value test
- Rule: squint or blur until detail drops; adjacent shapes must still
  separate by value, not hue alone — shapes that differ only in hue merge
  into one blob at small size or in motion. Ties to the analyzer's value
  metrics
- Source: Pixnote "Tips & Tricks"; Sprite-AI

---

# Researched lessons — 2026-07-19 (Minecraft/voxel focus)

Second research batch, **approved by the user** (candidates 10–14, 16–19;
material-rendering and CTM candidates were not selected). Per user directive,
future craft research is geared toward Minecraft/voxel texture work.

## 2026-07-19 — animation frame strip is one vertical column
- Rule: stack square frames vertically (16x16 block → 16×N px = N frames,
  top = frame 0) and ship `<texture>.png.mcmeta` beside it; non-square
  frames need explicit width/height. Vanilla-safe on 1.21.1
- Source: MoreMcmeta Animation Format —
  https://github.com/MoreMcmeta/core/wiki/User-Docs:-Animation-Format

## 2026-07-19 — frametime is ticks, 20 fps is the ceiling
- Rule: `frametime` = ticks per frame (default 1 = 20fps, the max). Slow
  shimmer uses higher values; per-frame overrides `{"index":4,"time":2}`
  and index lists `[0,1,2,3,2]` give ping-pong. Sub-tick smoothness is
  impossible — get it from `interpolate`, not more frames
- Source: MoreMcmeta Animation Format (as above)

## 2026-07-19 — interpolate crossfades, so author fewer keyframes
- Rule: with `interpolate: true` Minecraft blends the in-betweens, so smooth
  flow (water, portal glow) needs only a few hand-drawn keyframes at high
  frametime. Leave it OFF for sharp motion (fire, bubbling lava) — it smears
  the frames
- Source: MoreMcmeta Animation Format; MC Forum interpolate thread —
  https://www.minecraftforum.net/forums/mapping-and-modding-java-edition/resource-packs/resource-pack-help/2478530

## 2026-07-19 — animation frame-count by material
- Rule: fire/nether portal ~32 frames, interpolate off (chaotic motion);
  water/lava ~20–32, interpolate on (slow flow); most decorative blocks want
  just a 2–4 frame shimmer at frametime 6–12. Over-animating makes a wall
  of blocks "boil" and wastes VRAM
- Source: MC Wiki "Procedural animated texture generation" —
  https://minecraft.wiki/w/Procedural_animated_texture_generation

## 2026-07-19 — ship 2–3 block variants to break wall repetition
- Rule: author 2–3 subtly different versions of a block (different crack/
  grain, one darker) so placement variety breaks visible repetition across a
  wall. This is SEPARATE from the 3x3 seam check — a single perfect tile
  still forms a grid at distance; variety across the surface defeats the eye
- Source: Axidus "How to make seamless pixel art textures" —
  https://axidus.io/blog/how-to-make-seamless-pixel-art-textures

## 2026-07-19 — one ramp per material, shared darkest + lightest
- Rule: give each material its own hue-shifted ramp, but let every ramp
  bottom out in the SAME near-black and top out in the SAME near-white (or
  shared highlight). Anchors the palette and slashes slot count; unique
  black/white per material makes materials feel like different games
- Source: Lospec Sweetie 16 — https://lospec.com/palette-list/sweetie-16 ;
  palette list — https://lospec.com/palette-list

## 2026-07-19 — each color earns multiple roles
- Rule: under a ~16-color cap, force each slot to serve several contexts (a
  shadow that is also darkest wood AND a metal mid); order colors into
  connected ramps so adjacent colors can be borrowed between materials.
  Single-purpose colors bloat the palette and cause disharmony
- Source: Lospec palette-making —
  https://forums.lospec.com/topic/36/how-do-you-go-about-making-your-palettes

## 2026-07-19 — reference palettes for shared-endpoint ramps
- Rule: keep Sweetie 16 (16 colors, 4 hue-shifted ramps, shared light/dark)
  and Spectrum Ramps (per-hue ramps) on hand as starting points for a
  shared-endpoint Minecraft palette
- Source: https://lospec.com/palette-list/sweetie-16 ;
  https://lospec.com/palette-list/spectrum-ramps

## 2026-07-19 — labPBR specular/normal maps [SHADER-ONLY, optional]
- Rule: ONLY if the pack targets shaders (Iris/OptiFine + shader pack). Add a
  `_s` map: R = smoothness, G = reflectance/metalness, A = emission (0=none …
  254=full; 255 is IGNORED, emits nothing), plus a `_n` normal map. Lets
  metal reflect and ores/torches self-emit without changing base color.
  Does NOTHING in unmodified 1.21.1 — never a default deliverable
- Source: shaderLABS "LabPBR Material Standard" —
  https://shaderlabs.org/wiki/LabPBR_Material_Standard

---

# Researched lessons — 2026-07-19 (Minecraft engine / texture pipeline)

Third research batch, **all 16 approved by the user**, who directed that they
be applied to revise every texture shipped so far (done: alpha-bleed on all,
un-darkened bottom faces, block renderer corrected). Vanilla 1.21.1 unless a
[MOD] flag says otherwise. pack_format for 1.21.1 = 34.

## 2026-07-19 — don't bake directional gradients into blocks
- Rule: the engine multiplies each face BEFORE your shading shows —
  top 1.0, bottom 0.5, N/S 0.8, E/W 0.6. Paint side/bottom textures at FULL
  brightness and near-symmetric; one side texture renders at 0.8 on two walls
  and 0.6 on the other two. Pre-darkening double-darkens. `"shade": false`
  opts a face out. (Fixed our orrery/worktable bottoms; blockrender.py now
  uses the exact 1.0/0.8/0.6 multipliers.)
- Source: greyminecraftcoder "Lighting" http://greyminecraftcoder.blogspot.com/2020/04/lighting-1144.html ; MC Wiki "Light" https://minecraft.wiki/w/Light

## 2026-07-19 — alpha-bleed transparent pixels
- Rule: fill every alpha-0 pixel with the RGB of its nearest opaque neighbor
  (keep alpha 0). Mipmaps average in the RGB *under* transparent pixels; black
  there (our .pxg `none`) gives distant cutouts dark halos. Now automatic in
  `save_texture`/`aide render` and `aide bleed`; applied to all shipped art.
- Source: MC Wiki "Texture atlas" https://minecraft.wiki/w/Texture_atlas

## 2026-07-19 — no isolated 1px details on cutouts
- Rule: the first mip halving averages away 1px features, and 1px-thin cutout
  limbs drop below the alpha threshold and vanish at distance; keep meaningful
  detail >=2px, thicken thin stems. (Our leaf/sapling 1px shimmer accents are
  kept deliberately — sparse accents, acceptable to fade at range.)
- Source: MC Wiki "Texture atlas" (mipmap section, as above)

## 2026-07-19 — cutout alpha stays binary
- Rule: `cutout`/`cutout_mipped` layers hard-threshold alpha, so partial alpha
  won't soften leaf edges — it just gets clipped and, with mipmaps, fringes.
  Author hard edges + rely on alpha-bleed; reserve real translucency for the
  `translucent` layer (stained glass, water). (Analyzer already flags partial
  alpha.)
- Source: MC Wiki "Texture atlas" / render-layer notes

## 2026-07-19 — author tinted textures in grayscale
- Rule: tint is a MULTIPLY (texture RGB × tint color); paint grass green and
  the biome multiply doubles it wrong. Store tinted textures gray/neutral so
  the multiply supplies the hue. Vanilla-tinted: grass, leaves, plants, vines,
  water, redstone, leather, potions, map, spawn eggs, firework stars. A model
  face receives tint only via `"tintindex"`. (Validates our grayscale
  wand_base tint template.) [MOD] custom per-block colormaps = OptiFine-only.
- Source: MC Wiki "Color" https://minecraft.wiki/w/Color ; ResourcePackCreator https://resourcepackcreator.com/biome-tint

## 2026-07-19 — per-face UV, snapped to the grid
- Rule: Java block/item models are per-face UV only; snap every UV to the
  pixel grid or it samples between texels and blurs. (Box UV is a Bedrock/
  entity feature, not Java JSON models.)
- Source: Blockbench "Box vs Per-Face UV" https://blockbench.org/box-uv-vs-per‑face-uv-in-blockbench-which-method-should-you-use/

## 2026-07-19 — set texture_size to the real resolution
- Rule: model UV space is 0-16 by default; a non-16 texture needs
  `"texture_size":[w,h]` or texel density is inconsistent across faces.
- Source: Blockbench UV docs https://blockbench.org/blockbench-uv-editor-tutorial-basics-to-advanced/

## 2026-07-19 — non-overlapping UV islands (+1px gutter)
- Rule: give every model face its own UV region; two faces on one rectangle
  edit together and stretch/smear (our wand case), and touching islands bleed
  at edges/mip levels. (This is the general form of the wand UV-remap fix.)
- Source: Blockbench "How to UV Map" https://blockbench.org/how-to-uv-map-in-blockbench/

## 2026-07-19 — pack_format 34 + namespaced layout for 1.21.1
- Rule: `"pack_format": 34` = 1.21/1.21.1 exactly (datapack numbers are a
  separate scale). `pack.mcmeta` + `pack.png` at root, then
  `assets/<namespace>/textures/block|item/` (singular since 1.13).
- Source: MC Wiki "Pack format" https://minecraft.wiki/w/Pack_format ; MineVinyl https://www.minevinyl.com/guides/pack-format-explained

## 2026-07-19 — world sprites stay power-of-two square
- Rule: all block/item textures stitch into one atlas with up to 4 mip levels;
  non-POT/non-square block sprites break clean mip halving and can blur the
  whole atlas. (Animated frames stack vertically but each frame stays
  POT-square.)
- Source: MC Wiki "Texture atlas" (as above)

## 2026-07-19 — GUI textures are exempt from POT
- Rule: GUI/screen sprites are blitted, not stitched/mipmapped, so HD widgets
  and non-POT sizes are fine; only world textures need POT. (Relevant to the
  future HD aspect-icon workflow.)
- Source: MC Wiki "Resource pack" https://minecraft.wiki/w/Resource_pack

## 2026-07-19 — nine_slice for stretchable GUI panels
- Rule: 1.21's GUI sprite system slices a sprite into fixed corners + tiled
  edges/center via `"type":"nine_slice"` + `border`, so a small panel scales
  to any window without distorting the border. (1.20.2+ system; applies to
  1.21.1.)
- Source: MC Wiki "Java Edition GUI textures" https://minecraft.wiki/w/Java_Edition_GUI_textures

## 2026-07-19 — no coplanar faces at identical depth
- Rule: two overlapping quads at the same depth z-fight and flicker; offset an
  overlay element ~0.001-0.01 block, or delete the hidden face.
- Source: MC Wiki "Model" https://minecraft.wiki/w/Model

## 2026-07-19 — north is the model's default facing
- Rule: the north face is the reference orientation (UV [0,0] = top-left);
  blockstate `y` rotations turn the model from that baseline. Author the
  "front" on the north face or account for the rotation.
- Source: MC Wiki "Model" (as above)

## 2026-07-19 — CTM on Fabric/NeoForge is Fusion, not OptiFine [MOD]
- Rule: connected textures are not OptiFine-exclusive — **Fusion**
  (SuperMartijn642) provides CTM natively on Fabric/Forge/NeoForge/Quilt via a
  `.png.mcmeta` `"fusion"` block (NOT `ctm.properties`, NOT `.png.json`), with
  layouts pieced(5)/simple(16)/full(48)/… This is the viable CTM path for
  Thaumaturgy's stack. Full reference: `knowledge/references/fusion-ctm.md`.
  Still a runtime mod dependency — never a base-vanilla deliverable.
- Source: Fusion wiki https://github.com/SuperMartijn642/Fusion/wiki ;
  corrects the earlier "CTM = OptiFine-only" flag

## 2026-07-19 — emissive _e overlays are OptiFine-only [MOD]
- Rule: vanilla 1.21.1 has NO per-texture block emissive system. `<base>_e.png`
  fullbright overlays are OptiFine-only (ETF on Fabric replicates). Don't ship
  `_e` expecting vanilla glow — use the in-texture glow-by-contrast approach
  for base packs.
- Source: OptiFine "Emissive Textures" https://optifine.readthedocs.io/emissive_textures.html

## 2026-07-19 — point each block model's particle slot at its texture
- Rule: break/step/landing particles sample the model's `"particle"` texture
  slot; omit or mis-set it and particles show the wrong/missing (purple)
  color. Point `particle` at the main face texture.
- Source: MC Wiki "Model" (textures -> particle, as above)
