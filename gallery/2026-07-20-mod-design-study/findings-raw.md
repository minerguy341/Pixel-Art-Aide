# Mod design study — raw findings (2026-07-20)

Studied via parallel research agents. Reference policy: idioms/design only, no
pixels or asset files reproduced. Licenses recorded per mod (study-only regardless).

<!-- ============ MAGIC — spell/apparatus/effects ============ -->
# CATEGORY: Magic mods

## Ars Nouveau
**Meta.** Spell-crafting UI, magic apparatus blocks, automation critters, casting particles. ~3.2M+ Modrinth (millions more CF). License: **GPL-3.0-only** (open source).
**Techniques.** Cool jewel-toned palette: arcane blues/teals for "Source", violet+gold glyph accents, warm sandstone-white Archwood family — high chroma on desaturated stone. 16x vanilla-res, clean silhouettes, restrained dithering. Apparatus share a grammar: carved-stone base + floating glowing focal gem, so Enchanting Apparatus / Scribes Table / Imbuement Chamber read as one family. GUI = Patchouli codex + custom Spell Book screen; glyphs are square icon tiles laid Form→Effect→Augment like a sentence, each a bold pictogram on a flat plaque. Particles: soft additive-glow motes drifting up with sinusoidal sway, color-keyed to spell school.
**Takeaways.** (1) Encode magic grammar visually: shared base + swappable glowing focus makes an apparatus family legible. (2) Icon glyphs = flat bold pictograms on plaques. (3) Color-key particles to school, not block. (4) Keep 16x silhouettes clean; let glow carry the magic, not dithering.
**Signature.** Composable spell-sentence UI — uniform glyph tiles read left-to-right; meaning from order, not bespoke art.

## Botania
**Meta.** Floral/apparatus blocks, Lexica Botania codex, glow/spark particles. ~3.4M+ Modrinth. License: **custom "Botania License"** (CC-BY-NC-SA-like, noncommercial; source public).
**Techniques.** Disciplined 16-dye palette: each mystical flower one saturated hue on a muted green/stem base — a unified rainbow set from one template. 16x with soft rounded shading, gentle top-light, minimal hard outlines — "storybook" softness vs vanilla's harder edges. Living-wood/rock apparatus share an organic carved grammar (runework, swirling grain) so machines feel grown. Lexica = bespoke illustrated book GUI (paginated, inset diagrams). Effects: emissive flower glow + floating sparkles; Mana Spreaders fire visible glowing projectile bursts that arc — invisible flow made physical.
**Takeaways.** (1) Derive a family from one hue-swapped template on a shared neutral base. (2) Soft rounded shading + reduced outlines = "natural magic". (3) Make invisible systems visible as traveling glowing bursts. (4) Codex as designed art, not text.
**Signature.** Physicalized resource flow — mana travels as a visible glowing arc between blocks.

## Occultism
**Meta.** Ritual/summoning — chalk pentacle multiblocks, familiars, Dictionary of Spirits guidebook. ~10^7 total. License: **MIT** code; textures separately credited (Ridanisaurus) — don't reuse art.
**Techniques.** Vanilla 16px matched to MC palette so occult objects read diegetic, not hi-res. The occult read is layout+symbol, not saturation: pentacles are flat chalk glyph tiles in a few chalk colors, arranged into geometric circles. Apparatus muted browns/golds — Golden Sacrificial Bowl + candles use warm metallic highlights on desaturated stone/wood. Arcane cue = warm gold + ritual geometry + candle points, not glow spam. Dictionary of Spirits = Modonomicon parchment book with an in-world multiblock GHOST preview showing where each glyph/skull/candle goes.
**Takeaways.** (1) Draw rituals as flat floor-glyph tiles in a few named chalk colors; pattern carries the read. (2) Anchor with one warm-gold hero apparatus amid desaturated supports. (3) Ship a guidebook with in-world multiblock ghost preview.
**Signature.** Floor-glyph pentacle as multiblock — power as player-drawn geometry of small sigil tiles.

## Malum
**Meta.** Dark/soul magic — Spirit Altar + orbiting pedestals, Spirit Crucible, runewood/soulwood sets; VFX-forward. ~10^6. License: **LGPL-3.0-or-later** (uses author's Lodestone VFX lib).
**Techniques.** Cohesive moody art direction over vanilla-matching. Limited dark palette — deep runewood browns, pale cold soulwood — with carved arcane linework on plate faces. Signature is the VFX layer, not block pixels: Lodestone drives soft additive colored glow particles (spirit hues: gold/crimson/aqua/purple) that rise/swirl/trail, plus screen-space particles over item sprites so items shimmer in inventory. Bloom + smooth alpha falloff = volumetric magic on dark blocks. Spirit Altar = low pedestal + floating item + orbiting ingredient pedestals — composition signals ritual before any UI.
**Takeaways.** (1) Spend the magic budget on additive-glow particles over restrained 16px blocks — cheap blocks, expensive light. (2) One saturated wisp hue per energy type, reused across particles/item-shimmer/altar. (3) Compose apparatus as floating item + orbiting pedestals. (4) Screen-space sprite shimmer makes key items feel enchanted.
**Signature.** Additive glowing wisp particles in a fixed per-element hue set — identity lives in light, not texels.

## Iron's Spells 'n Spellbooks
**Meta.** RPG spellcasting — 100+ spells, spellbooks, Inscription Table, combat VFX. ~10^7. License: **All Rights Reserved** (source public for contribution; assets NOT free — study only).
**Techniques.** Defining system = school-based color coding across nine schools (Fire, Ice, Lightning, Holy, Ender, Blood, Evocation, Nature, Eldritch), each a fixed hue + focus item. Palette propagates everywhere: spell icons, tooltip/UI accents, particles, damage type. Spell icons = clean high-contrast 16–18px emblems with a consistent silhouette language so a grid scans as one set. Spellbook/Inscription GUI = slotted loadout screen (fill spell slots), reads like an RPG hotbar, not a chest. Lavish colored animated projectiles/auras keyed to each school.
**Takeaways.** (1) Fix a per-school/per-aspect hue palette up front; propagate through icons, UI, particles — one lookup table drives consistency. (2) Design aspect icons as a matched emblem set (shared silhouette, high contrast, uniform frame). (3) Model magic UI as a slot-based loadout, not a chest.
**Signature.** A fixed per-school color system as the single source of visual identity.

<!-- ============ DECORATIVE — wood-set completion guidance ============ -->
# CATEGORY: Decorative / block-family mods (wood-set guidance)

## Supplementaries
**Meta.** Vanilla+ decoration/utility (Architectury). ~212M+ CF. License: **custom** (author terms; treat art as ARR). Author MehVahdJukaar.
**Techniques.** Reference for wood-derived families driven by DATA, not new pixels. Signs, hanging signs, sign posts, planters etc. generated per wood by reusing plank+log textures through model UVs — a new wood "just works" by pointing at that wood's atlas entries. Complex blocks get bespoke art; anything wood-bodied reuses plank faces + a small unique overlay (rope, iron band, hinge) as a separate texture. Low-element, vanilla-parented models; detail density held at/under plank noise.
**Takeaways.** (1) Model wood-body blocks by UV-mapping the plank texture; author new pixels only for the non-wood accent. (2) One shared model template per family member; vary only the wood texture ref. (3) Cap added detail at plank busyness. (4) Accents on a separate small overlay, not baked into the plank.
**Signature.** Data-driven per-wood family generation from a single plank/log reference — new wood = new palette, zero new geometry.

## Macaw's (Furniture / Doors / Bridges)
**Meta.** Decoration/furniture ecosystem. Furniture ~84.6M+ CF; Doors/Bridges tens of millions. License: **custom/author-specific** (modpack-permissive; verify before asset reuse). Author sketch_macaw.
**Techniques.** Reference for HARDWARE-ACCENTED wood variants. Doors/trapdoors reuse the plank palette as the panel field, add a small consistent metal accent (handle, hinge plate, bolt) in a fixed 2–3px iron ramp identical across every wood — the accent is the brand, the wood is the variable. Each door "style" = one model + one texture template restamped per wood. Bridges reuse plank faces on multi-element models; new art reserved for rope/metal fittings. Flat low-noise textures tile cleanly.
**Takeaways.** (1) Give doors/gates a FIXED hardware accent palette (one iron ramp) reused identically across both woods — that's what unifies the set. (2) Build each door/trapdoor as model + template texture, restamped per wood. (3) Put hardware on a distinct UV region so the wood field stays pure plank. (4) Boats/bridges reuse plank faces; new art only for rope/metal.
**Signature.** A single invariant metal-hardware accent stamped over per-wood plank fields.

## FramedBlocks
**Meta.** Retexturable shape blocks. ~84.7M+ CF. License: **LGPL-3.0** (most reuse-friendly; a code reference here).
**Techniques.** Extreme of geometry-decoupled-from-texture: a huge shape library (slab, stair, corner, slope, panel, door, trapdoor, fence, sign) carrying NO art — appearance is the "camo" block re-UV'd onto framed geometry at runtime. Lesson for a normal wood set: every wood-shape member can share ONE plank texture via model UVs, and vanilla's stair/slab/fence/gate/door/trapdoor parent models already define correct UV layouts to inherit.
**Takeaways.** (1) Parent every shape (stairs/slabs/fence/gate/button/pressure plate) to the VANILLA model and feed it the plank texture — no new pixels. (2) Only door, trapdoor, sign, boat need dedicated textures. (3) One plank texture = single source of truth; shared UVs guarantee cohesion. (4) Reserve custom art for the ~4 blocks with unique geometry faces.
**Signature.** Geometry-first — shapes are UV containers, one plank texture fills the whole family via vanilla parents.

> **Wood-set synthesis:** for 2 woods, author only the plank texture + ~4–5 new
> faces (door top/bottom, trapdoor, sign board, boat, optionally log). Generate
> stairs/slab/fence/gate/button/pressure-plate/crafting-table by UV-mapping the
> plank through vanilla parent models. Add ONE shared iron hardware ramp for
> door/trapdoor/gate fittings, invariant across both woods. Hold new art at plank busyness.

<!-- ============ EFFECTS / APPARATUS grammar ============ -->
# CATEGORY: Effects / apparatus grammar

## Create
**Meta.** Kinetic tech; the reference for restrained cohesive block art. ~10^7–10^8 (Modrinth ~21.5M, CF 100M+). License: **MIT code / ARR assets** — study look only.
**Techniques.** Narrow desaturated palette (brass/gunmetal/andesite + few saturated accents) applied consistently so every block reads one material family. Grammar = framed-face + banding: recessed panel + lighter rim, corner rivets, horizontal bands = "casing". State shown via geometry + low-frame diegetic animation (gear teeth, belt scroll), not glow. Visual-mechanical isomorphism: a cog looks like it meshes; silhouette tells function. Speculars subtle — one lighter highlight row per material.
**Takeaways.** (1) Lock a tight neutral base palette for all arcane apparatus; reserve saturated hues for essentia/aura energy. (2) Framed-panel + rivet grammar, distinguished from Create by MATERIAL (stone/greatwood/thaumium, not brass). (3) Diegetic animation only — motion = process state. (4) One highlight row per material.
**Signature.** Visual-mechanical isomorphism — the texture is the tooltip.

## Embers Rekindled
**Meta.** Effects-forward dwarven "Ember" energy; closest tonal cousin to a Thaumcraft successor. ~10^6. License: **MIT** (study look only).
**Techniques.** Identity = flowing energy particle language: warm ember streams (deep red→orange→pale yellow ramp) travel visibly between apparatus along conduits — power is a seen fluid. Additive glow, soft edges that fade on clip, gentle arcing motion. Exposes resource-pack-TINTABLE particle colors — color is a data parameter, not baked. Blocks = dark riveted metal with glowing inset runes/cores; emissive accents mark the active region.
**Takeaways.** (1) Give essentia/flux a visible 3-stop color ramp per aspect (dark core→mid→pale hot tip); drive particle tint from a data value. (2) Make transport legible with slow motes along the path. (3) Emissive inset cores show active vs idle; base block stays dark. (4) Soft-fade particles on geometry clip.
**Signature.** Data-driven tintable particle ramps — one system recolored per aspect.

## Mekanism
**Meta.** Tiered industrial machinery; studied for machine-UI + block grammar at scale. ~10^8. License: **MIT** (safer study target than ARR Thermal).
**Techniques.** Modular material library: every machine = same framed steel chassis + swappable front-face operation panel (colored progress arrow, tinted glass port, indicator light) — dozens of blocks with instant kinship, identified by their face. Tier shown by frame-color banding (basic→advanced→elite→ultimate) — progression as palette shift on one silhouette. Tinted speculars on glass/energy ports (saturated core behind glassy highlight). Consistent GUI chrome across all machines. Connected casing keeps multiblocks reading as one.
**Takeaways.** (1) Shared apparatus chassis + swappable front panel; identify each device by its face (aspect glyph / colored port). (2) Encode tier as palette banding on one silhouette (thaumium→void-metal). (3) Standardize GUI chrome — one essentia-bar + slot grammar across crucible/alembic/infuser. (4) Tinted specular over a saturated core = magical glass/containment.
**Signature.** Chassis-plus-face — a consistent frame carrying an information-bearing front panel.

<!-- ============ MOBS ============ -->
# CATEGORY: Mob / creature design

## Alex's Mobs
**Meta.** ~89 creatures. ~10^8 (~149M CF). License: GPL-family (GPL-3/LGPL-3 reported) — study only.
**Techniques.** Benchmark for vanilla-cohesive creatures. Models modestly above vanilla (a few extra cubes for ears/tails/fins), same chunky proportions. Textures at vanilla texel density (16px/block-unit), muted low-sat palette, hard 1px AO — blend seamlessly. Animation via Citadel: idle sway, tail flicks, attack wind-ups, but shapes stay blocky. Readability from strong real-animal silhouettes. Bosses (Void Worm) read at scale via repeated segmented cubes, not more texture.
**Takeaways.** (1) Match vanilla texel density + palette first; magic added on top, never by out-detailing. (2) Keep silhouettes anatomically legible. (3) Life through animation, not geometry. (4) Scale menace by repeating simple forms, not resolution.
**Signature.** Vanilla-first restraint — creatures feel official because they stay within vanilla's texel/palette/cube rules.

## Mowzie's Mobs
**Meta.** Few, curated bosses. ~10^8 (~106M CF). License: **custom/proprietary** — no reuse/trace.
**Techniques.** Benchmark for character-driven mobs. Few creatures, each heavily crafted; models push past vanilla cube counts for expressive anatomy but keep vanilla texel density + flat hand-shading, so complexity reads as "detailed Minecraft". Signature = GeckoLib keyframed cinematic animation: weighty, heavily TELEGRAPHED attacks with anticipation + follow-through. Bosses read via silhouette + staging (dramatic idle poses, screen shake, readable tells). Mythic/tribal palette (earthy + warm accents).
**Takeaways.** (1) Fewer, more crafted creatures beat many shallow ones. (2) Telegraph every attack — the wind-up pose is a feature. (3) Push model complexity but hold vanilla texel density + flat shading. (4) One silhouette-defining feature per creature (mask, mane, weapon).
**Signature.** Cinematic telegraphed keyframe animation — bosses get weight and teach their moveset by pose.

## L_Ender's Cataclysm
**Meta.** Boss-focused dungeon mod. ~10^8 (100M+ CF). License: **CC-BY-NC-ND-4.0** — no derivatives/reuse.
**Techniques.** Benchmark for large-scale spectacle bosses. High cube counts, often above 16px texel density for armored/metallic surfaces — deliberately a step above vanilla. GeckoLib multi-phase fights with phase-change poses. Readability at scale via strong EMISSIVE cues: glowing eyes/cracks/cores/weak-points legible across an arena, signalling element (nether=orange, ender=purple). Silhouettes built around one dominating feature (blade-arm, crown, mask); small readable focal "face". Menace via proportion (oversized upper bodies).
**Takeaways.** (1) Emissive glow (eyes/cracks/cores) = primary magical/eldritch cue + long-range readability. (2) Color-code element via glow hue (arcane cyan/violet; taint sickly green-purple). (3) Boss silhouette around one oversized signature feature + a small focal face. (4) If going above vanilla res for epic bosses, commit consistently.
**Signature.** Emissive weak-point/eye glow — signals arcane element and keeps giant bosses readable.

> **Cross-mod north star:** keep blocks & mobs vanilla-scale 16px and restrained;
> spend the "arcane" budget on (a) a FIXED per-aspect hue system (Iron's) across
> icons+particles+UI, (b) ADDITIVE glowing wisp particles over dark blocks
> (Malum/Embers, data-tintable per aspect), (c) EMISSIVE cores/eyes for active
> apparatus and mob elements (Cataclysm/Embers), (d) ritual-as-floor-geometry
> with an in-world multiblock ghost preview (Occultism). Apparatus stay a
> restrained neutral MATERIAL (Create/Mekanism) so saturated glow reads as the
> magic — letting the mod sit beside Create without copying its brass.

<!-- ============ UI / HUD / guidebook ============ -->
# CATEGORY: UI / HUD / guidebook

## JEI / REI (recipe viewers)
**Meta.** Item/recipe browser UI. JEI ~10^8 (one of the most-downloaded ever); REI ~10^7. License: **JEI MIT**, **REI MIT** (config Apache-2.0) — freely studyable.
**Techniques.** Fixed vertical item-list panel docked right (paged 18x18 slot grid) + bottom search bar with prefix filters (`@mod`, `#tag`). Recipe view = category-tabbed: left icon column, paged recipe pane, `<`/`>` arrows. Built from small reusable widgets (slot bg, arrows, +/= glyphs) from a shared sheet — neutral chrome, not themed art. REI adds rounded panels, settings gear, favorites, dark mode. Hover highlight = translucent white quad over focused slot.
**Takeaways.** (1) Codex needs a persistent search field with prefix filters (`@school`, `#aspect`). (2) Reuse one slot sprite + hover-highlight widget everywhere. (3) Nav = left icon rail + paged pane + prev/next arrows. (4) Click-to-see-uses cross-linking between an aspect and its consumers.
**Signature.** Docked, filterable slot-grid list with prefix-search.

## Jade (WTHIT fork)
**Meta.** Look-at info HUD. ~10^8. License: **CC BY-NC-SA 4.0** — study composition, don't copy assets/code.
**Techniques.** Single floating tooltip card at top-center for the targeted block/entity. Composition: horizontal icon+title+subtitle header (block sprite, name, muted-italic mod footer), then stacked plugin-provided rows (energy/fluid/progress/inventory). Background = nine-slice rounded panel with accent border, drawn every frame in screen space, scaled to content. Rows contributed via data-driven plugin API. Fade-in on target change; compact progress/arrow bars reusing furnace-style sprites.
**Takeaways.** (1) Arcane tooltips = nine-slice card, fixed header (icon+name) + stacked flavor rows (aspect icons, vis cost, "requires research X"). (2) Muted footer line (aspect school) as recurring identity cue. (3) Drive extra rows from data. (4) Inline icon+number chips (aspect glyph + count), not prose, for magical costs.
**Signature.** Nine-slice card with a stacked, plugin-fed typed-row model.

## Patchouli (guidebook framework)
**Meta.** Data-driven guidebook. ~10^8. License: **CC BY-NC-SA 3.0** — study-only; Codex should be an original impl of the ideas.
**Techniques.** Two-page open-book background; content in left/right regions. Hierarchy: book → category grid → entry list → paged entry. Landing = grid of category icons; category → scrollable entry list (icon+title, lock/greyed for un-researched); entry = sequence of pages flipped with corner arrows. Typed page templates: `text`, `crafting`, `spotlight`, `image`, `entity`, `multiblock`, `relations` (a link-graph of related entries) + custom. Rich text with inline item icons, color codes, clickable cross-links. Locked/hidden entries gate content behind advancements — reveal-as-you-progress.
**Takeaways.** (1) Adopt book → category → entry → page hierarchy for the Codex. (2) Locked/greyed entries tied to research state (Thaumonomicon reveal). (3) Typed page templates so authors work in data. (4) The `relations` link-graph page is the seed for our node-graph — entries as nodes with prerequisite edges.
**Signature.** Data-driven typed pages with advancement-gated greyed-out entry reveal.

## Ars Nouveau (codex + spell-crafting UI)
**Meta.** Magic guide + spell-builder UI. ~10^7. License: **code LGPL-3.0; art All Rights Reserved** — study interaction/layout only.
**Techniques.** Spell-crafting screen: large scrollable glyph palette grouped Forms / Effects / Augments, each glyph a bordered icon button with hover tooltip (cost + behavior); search bar filters. Spell under construction = horizontal slot sequence (ordered glyph "recipe") read left-to-right; multiple spell tabs per book. Live validity/cost readout updates as glyphs are placed; invalid sequences flagged. Name + color customization per spell. Parchment/arcane framing so it reads as a wizard's tool.
**Takeaways.** (1) Categorized searchable icon palette + ordered slot sequence maps 1:1 onto our Arcane Worktable (aspects/foci as palette). (2) Live cost/validity readout beside the build area = home for the vis-cost display. (3) Group palette by semantic school with visual bands. (4) Name/color personalization of the result deepens ownership.
**Signature.** Live-validated glyph-sequence builder — searchable typed palette → ordered slot chain → real-time cost/validity feedback.

## Implementation note — 1.21 nine-slice sprites
Since 1.20.5+, GUI textures are individual sprites under `assets/<ns>/textures/gui/sprites/`, drawn via `GuiGraphics.blitSprite(...)`; a `.mcmeta` declares `type: stretch | tile | nine_slice` (border keeps corners fixed, tiles/stretches edges, fills center). This is the modern resolution-independent way to draw Codex/worktable panels, buttons, and tooltip cards at any size without POT constraints — author panels as nine-slice sprites, not fixed bitmaps. (minecraft.wiki "Gui.png-atlas"; NeoForge 1.21.1 GUI docs.)

> **UI north star:** Patchouli's category→entry→node-graph hierarchy with gated
> reveal for the Codex; Ars Nouveau's searchable palette + ordered slot chain +
> live cost readout for the Arcane Worktable/vis display; JEI/REI's filterable
> slot-grid + prefix search for browsing aspects; Jade's nine-slice info card
> with stacked typed rows for arcane tooltips. All on 1.21 nine-slice sprites.
