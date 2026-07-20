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

---

# Researched lessons — 2026-07-19 (batch 4: glass/stairs/ores + Thaumcraft + Create)

All 6 approved by the user (study-batch findings, `gallery/2026-07-19-study-batch/findings.html`).

## 2026-07-19 — glass = thin frame + streaks + empty interior
- Rule: author glass as a ~1px opaque border ring (+1-2px corner accents), 1-2
  diagonal specular streak lines, and leave ~80% of the interior fully
  transparent. A thick frame over a filled body reads as a solid framed box,
  not glass — the eye reads "pane" from the outline + streaks, not fill.
- Source: MC Wiki "List of block textures" https://minecraft.wiki/w/List_of_block_textures

## 2026-07-19 — clear glass is cutout, stained is translucent
- Rule: clear glass/panes render on the CUTOUT layer (binary alpha — any
  non-zero alpha becomes fully opaque, no soft edges); stained/tinted glass
  render TRANSLUCENT (real alpha blending, can dim/tint what's behind). Design
  streaks knowing the layer: cutout streaks must be fully opaque.
- VERSION: the block-model `render_type` field is NeoForge-only on 1.21.1
  (vanilla adds it in 1.21.4) — a pure-vanilla 1.21.1 pack can't move clear
  glass to translucent.
- Source: OptiFine render layers https://optifine.readthedocs.io/block_render_layers.html ; NeoForge models https://docs.neoforged.net/docs/1.21.1/resources/client/models/

## 2026-07-19 — stairs/slabs reuse the parent texture: keep it uniform
- Rule: stairs and slabs author NO new art — they sub-sample the parent
  block's texture across many small step/riser faces. So the full-face texture
  must be tileable and value-uniform; avoid any centered hero motif (a knot,
  emblem, big gradient) that fragments into meaningless slivers when cut.
  Test on an actual stair/slab model, not just a flat cube.
- Source: MC Wiki "Model" / "Tutorials/Models" https://minecraft.wiki/w/Model

## 2026-07-19 — vanilla ores bake the stone in; cluster the mineral
- Rule: vanilla ores are full textures with the host stone painted in (not a
  transparent overlay — that's a mod/pack pattern). Paint 2-4 CLUSTERED
  mineral shapes, each with a highlight (top-left) + shadow (bottom-right) for
  a faceted read; scattered single pixels read as dirt/noise. If doing the mod
  overlay split, alpha-bleed the mineral edges and use cutout_mipped.
- Source: MC Wiki "Ore" https://minecraft.wiki/w/Ore

## 2026-07-19 — the Create idiom: adopt the grammar, swap the material
- Rule: to sit beside Create machinery, use Create's *grammar* — frame every
  machine face (1px darker border around a lighter inner plate), corner
  rivets, horizontal banding/straps, panel seams, connected-texture panels,
  consistent top-left light, and speculars TINTED toward the material (never
  pure white) — but with our own arcane material ramps. Cohesion comes from
  process consistency, not specific hues; a parallel-but-distinct palette sits
  next to Create without being mistaken for it. Translate hardware into magic
  vocabulary: rivet -> rune-stud, strap -> sigil band, shaft slot -> glyph socket.
- Source: Create GitHub texture tree https://github.com/Creators-of-Create/Create ; create.fandom "Casing" https://create.fandom.com/wiki/Casing

## 2026-07-19 — the Thaumcraft grammar (evoke, don't copy)
- Rule: to read as Thaumcraft's successor without copying assets: (1) TWO
  purples with opposite jobs — a dignified grey-violet for refined magic metal
  (our aetherium), a sickly magenta for corruption, never blended; (2) cool
  DRESSED arcane stone (blue-grey, tidy mortar, subtle runes) — "quarried by
  wizards", not "mossy ruin"; (3) warm brass for all instruments/apparatus so
  tools feel like one kit; (4) reserve emissive GLOW for the truly magical
  (nodes, runes, essentia, one shimmer-wood), everything structural matte;
  (5) one icon shape + colour-coding system (they used the hexagon), flat
  minimal glowing-outlined glyphs legible at 16px; (6) encode order-vs-chaos
  in NOISE level — clean symmetric for civilised magic, veiny/asymmetric for
  corruption.
- Source: FTB Wiki (Arcane Stone, Aspects) https://ftb.fandom.com/wiki/Aspects_(Thaumcraft_4) ; Thaumcraft 4 Wiki (Silverwood, Thaumium, Taint, Aura Node) https://thaumcraft-4.fandom.com/wiki/Thaumium

## 2026-07-19 — leaves need vanilla-density transparent holes
- Context: greatwood/silverwood leaves read as solid green cubes; user flagged
- Observation: vanilla oak/spruce/birch leaves are 32-43% TRANSPARENT with holes
  scattered high-frequency across the whole tile; ours were ~8% (edge holes) and
  read as a solid cube
- Rule: leaves need ~30-40% scattered transparent holes (per-cell, not blobs;
  break up any 2x2 fully-transparent block). CHECK TRANSPARENCY when matching a
  material, not just colour. (Folded into shading.md leaves shorthand;
  generator: make_leaves.py.)
- Source: vanilla 1.21.1 oak/spruce/birch_leaves.png (mcasset / InventivetalentDev)

---

# Studied lessons — 2026-07-19 (BWG wood/leaf comparison, 25 wood types)

Approved by the user. Studied from "Oh The Biomes We've Gone" textures in the
session scratchpad (per reference-policy.md — general craft only, no pixels
committed).

## 2026-07-19 — distinct woods differ by value+hue, not structure
- Rule: a family of woods shares ONE ramp grammar (~7 colours per plank; 23 of
  25 BWG woods use exactly 7) and is differentiated by where the ramp sits —
  value range (ebony L7-20 vs white_mangrove L53-83) and hue (browns, reds,
  purples, blues, greens, greys). Add a new wood by re-anchoring value+hue, not
  by inventing new grain. Extends "one arrangement, many palettes".
- Source: BWG plank/log set (25 wood types)

## 2026-07-19 — leaf hole density is a canopy-type lever
- Rule: leaf transparency is not one number — it encodes canopy type. Airy
  broadleaf/deciduous run ~27-39% holes; dense, weeping, or coniferous canopies
  run low (willow 9%, spirit 10%, mangrove/baobab 18%). Pick the % from the
  tree's density, not a fixed default. (Our 33% greatwood/silverwood = broadleaf
  band; a dense magic canopy would drop to ~15-20%.) Refines the leaves lesson.
- Source: BWG leaves set (avg 27%, range 9-39%)

## 2026-07-19 — leaf colour is an independent species axis
- Rule: wood colour and leaf colour are DECOUPLED identity axes — leaves need
  not be green (BWG: witch_hazel orange, skyris pink, jacaranda purple, zelkova
  dark-red, aspen yellow; white_mangrove pale-grey wood + dark-green leaves).
  Use an off-green leaf as a species tell. Flowering/fruiting variants = the
  plain leaf base + SPARSE bright blossom/berry accents (that's all the high
  colour-count leaves are), not a busier field.
- Source: BWG leaves + flowering/ripe leaf variants

---

# Studied lessons — 2026-07-19 (BWG broad field study, 994 textures)

Approved by the user. Studied in the scratchpad (reference-policy.md); derived
data only, no BWG pixels committed.

## 2026-07-19 — transparency encodes how airy the object is
- Rule: the share of transparent pixels tracks the subject's physical airiness
  — solid ground 0-1%, ice ~8%, foliage 28-39%, cross-plants (flowers/cactus)
  52-58%. Set a sprite's alpha from what it *is*, not a fixed value.
- Source: BWG material-class survey

## 2026-07-19 — value + busyness place a material class
- Rule: two cheap dials separate materials — where the value range sits and how
  busy the surface is. sand = pale (L59-82) + calm (busy ~5); stone = mid
  (L50-75) + calm; foliage = darker + busier (~8-12).
- Source: BWG material-class survey

## 2026-07-19 — natural ground & ripe fruit break the "few colours" rule
- Rule: soil (dirt/mud/moss ~24 colours) and ripening fruit (~19) deliberately
  use many close tones for an organic/gradient read. "Few colours / tight ramp"
  is for crafted/structured materials, not natural ground or fruit.
- Source: BWG dirt/mud/moss + berry/fruit

## 2026-07-19 — cross-plants are ~half transparent: stem + bloom
- Rule: a cross-plant sprite is ~52% transparent, ~10 colours = green stem/leaf
  + a small vivid petal cluster; the bloom is the only saturated thing.
- Source: BWG flower/cross-plant set

## 2026-07-19 — split a plant palette into foliage + bloom + structural
- Rule: classify pixels BEFORE reading a palette — green hue = foliage,
  saturated non-green = bloom, near-grey = structural (twig/stem) — and author
  the three as separate ramps. Never aggregate a mixed category into one swatch;
  it hides the greens under the most common bloom (BWG bushes read "all purple"
  only because 13 of 23 are jacaranda-family blooms).
- Source: BWG bush/flower split analysis (user caught the purple artefact)

## 2026-07-19 — door/trapdoor ≈ the plank ramp near-verbatim
- Rule: a wood's door and trapdoor are ~90% its plank palette (doors avg 91%,
  most 95-100%) — recolour the planks and add only a small hardware accent
  (handle/hinge). The most wood-faithful derived block.
- Source: BWG furniture set (25 woods)

## 2026-07-19 — crafting table = wood base + tool motif; top is the wildcard
- Rule: the crafting-table FRONT keeps ~71% wood under a saw/grid graphic (a
  ~30% non-wood tool motif); the TOP is bimodal — either a woody grid (~100%)
  or a dark non-wood grid overlay (~5-20%). Front is consistent; the top is a
  free design choice. (Our arcane worktable = wood + brass/aetherium accent fits.)
- Source: BWG furniture set

## 2026-07-19 — bookshelf = plank frame + independent book-spine accent set
- Rule: a bookshelf is only ~50% the wood (the shelf frame); the other half is
  book spines whose bright colours are a SEPARATE accent palette, not drawn
  from the wood. Author the frame from the plank ramp, the books from their own
  set. (T.N.A.: greatwood frame + colourful codex/tome spines.)
- Source: BWG furniture set

## 2026-07-19 — sapling rides the LEAF colour, not the plank
- Rule: a sapling is ~75% its leaf palette and only ~46% its plank palette — a
  foliage-coloured sprout on a thin wood-brown stem. It reads as the young
  tree's leaves, so it inherits the leaf/species identity, not the wood.
  Reinforces "leaf colour is the independent species axis".
- Source: BWG sapling set (25 woods)
