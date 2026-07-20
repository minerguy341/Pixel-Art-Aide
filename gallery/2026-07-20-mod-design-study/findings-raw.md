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

<!-- ============ BATCH 2 ============ -->
# CATEGORY: Magic — celestial / occult / witchcraft (batch 2)

## Astral Sorcery
**Meta.** Celestial/starlight magic — marble apparatus family, constellation Journal UI, starlight beam/particle effects. ~10^7 (~70M+ CF). License: **All Rights Reserved** (assets off-limits).
**Techniques.** Cool desaturated palette: bluish-white marble (raw/chiseled/engraved/runed/pillar) as the structural family, offset by cyan/teal starlight glow + gold-amber crystal. 16x; the marble family reads as one apparatus set via shared base stone + escalating engraved-rune overlays — tier legibility from carving density, not new palette. Celestial altars are multiblocks (Luminous→Starlight→Celestial→Iridescent), each ringing the core with pillars + floating relays. Cosmic mood carried by EMISSIVE rendering: vertical starlight beams, drifting sparkles, rotating constellation glyphs. Journal = hand-drawn parchment sky-atlas; constellations are dot-and-line line art you trace to discover.
**Takeaways.** (1) One neutral base stone + escalating engraved-rune overlays = legible tiered-apparatus family without palette sprawl. (2) Push celestial mood into emissive/particle layers, keep blocks restrained. (3) Constellation UI as node-and-line line art on parchment — a superb model for the aspect/research web. (4) Multiblock altars ringed by pillars + relays make progression read spatially.
**Signature.** The hand-drawn constellation Journal — dot-and-line celestial glyphs you trace to unlock; research as intimate sky-cartography.

## Blood Magic
**Meta.** Visceral/sacrificial — filling Blood Altar, Blood-Rune tiers, floor-glyph rituals, sigils/Living Armor. ~10^8 (~108M CF). License: **CC BY 4.0** (attribution-permissive; still study-only per policy).
**Techniques.** Warm grim palette: arterial reds, blackened iron, bone/ash grey, demonic teal-green (Demon Will) as a second-resource accent. 16x. The Blood Altar's interior RED FLUID LEVEL RISES with stored LP — a live gauge built into the block via dynamic liquid render, with drain particles + failure smoke. Tiers grow pyramidally: rings of Blood Runes (dark stone tile + inscribed blood-red glyph) so power reads as an expanding engraved footprint. Rituals = Master Ritual Stone + patterned stones laid as floor sigils. Disciplined red-on-black + one accent.
**Takeaways.** (1) A live fluid-level gauge inside the altar turns the block into a resource readout — steal for a crucible/altar. (2) Inscribed glyph-runes tiled around a core convey tier as an engraved footprint. (3) Floor-laid glyph arrangements make rituals legible top-down. (4) A disciplined 2-colour story sells "visceral" like Astral's blue-on-white sells "cosmic".
**Signature.** The blood-filling altar basin — dynamic liquid render that doubles as a live resource gauge.

## Eidolon: Repraised
**Meta.** Dark alchemy/necromancy (port of Elucent's Eidolon). ~10^7 (~9M CF). License: **LGPL-3.0** (permissive for study).
**Techniques.** Low-sat near-vanilla 16px, grimdark palette — desaturated greys, bone-ivory, cold blues, sickly greens vs candle-warm accents. Sells occult through gloom + a few glowing focal pixels, not hue variety. Apparatus reads as a shabby-Gothic alchemist's study: Wooden Worktable (recipe overlay), a Crucible heated by a fire block below (bubbling, steam), a Brazier/Effigy/Altar ritual cluster emitting particle chants. Codex = hand-drawn tome with rune diagrams. Signature ambiance: floating soul-glyph particles, purple/green wisps, glowing sigils drawn mid-air during chants.
**Takeaways.** (1) Heat-from-below crucible: a block whose glow/bubbling reacts to an adjacent fire block — cheap legible research apparatus. (2) Emissive sigil/rune particles drawn in-air are the whole arcane read. (3) Muted grimdark base + a single warm candle accent per block. (4) Codex with hand-drawn rune plates sets tone.
**Signature.** Mid-air glowing glyph particle chants as the ritual's visual payload.

## Forbidden & Arcanus
**Meta.** Gothic dark-magic content/deco (explicitly Thaumcraft-inspired). ~10^7–10^8 (~66.7M CF). License: **All Rights Reserved** (assets look-study only).
**Techniques.** The cleanest "finished-AAA" texturing here — crisp 16px, tight high-contrast edges, richly saturated arcane accents (deep purples, gold Deorum, ember-orange, dark polished stone). Grammar is arcane-gothic: Polished Darkstone masonry set (chiseled/pillar/tile) + glowing Arcane Crystal blocks + the Arcane Crystal Obelisk. Centerpiece Hephaestus Forge = large multi-tier ritual altar, a strong hero-block silhouette. Edelwood = a gnarled dark tree with a full tool/wood set. Glow used sparingly but punchily.
**Takeaways.** (1) A cohesive cut-darkstone masonry family (base/chiseled/pillar/polished/tiled) = instant arcane-gothic vocabulary. (2) One hero ritual-altar block with a bold silhouette anchors progression. (3) A named exotic wood with a full set makes the mod feel like a material, not a gadget pack. (4) Reserve saturated glow for crystal/reagent focal blocks.
**Signature.** The tiered hero-altar (Hephaestus Forge) as a single visually dominant crafting monument.

## Hexerei
**Meta.** Cozy witchcraft / cottage-magic. ~10^7 (~26.4M CF). License: **MIT** (+ note in LICENSE.txt; confirm per-asset). Study-friendly.
**Techniques.** Warmest "cozy-occult" register: 16x, homey woody browns (Willow/Mahogany), sage greens, dried-herb ochres, candle-yellow. Soft shading, clutter-friendly props. Witch-cottage aesthetic from decorative density: colored Candles that MELT through visible burn stages, Herb Jars (drawer storage, contents on the label), hanging dried herbs, coffers, crystals, a Mixing Cauldron brew station. Broomstick traversal; Book of Shadows takes its cover colour from the dye used to craft it. Gentle glow (candle flicker, cauldron particles).
**Takeaways.** (1) Multi-stage "consumable state" blocks (melting candles) add life cheaply — model for burning reagents/incense. (2) Label-front storage jars that display contents = functional + decorative reagent shelving. (3) A dense kit of small decor props makes a space feel inhabited. (4) Tint-on-craft covers / dyeable items give ownership.
**Signature.** State-driven decorative props (candles that melt across visible stages) — living ambiance from block-state textures.

# CATEGORY: Decorative — texture-variant & furniture (batch 2)

## Rechiseled
**Meta.** Decorative block-variant / chisel mod (SuperMartijn642). ~10^7. License: **All Rights Reserved** (Extras pack GPLv2).
**Techniques.** One base block → a family of decorative tiles picked in a chiseling GUI, via tag-like "chiseling recipes" that auto-merge across packs. Each variant ships plain AND connecting-texture forms (tiles cut from one sheet, auto-selected by neighbour state; connection carries across full/stair/slab). Detail-density stays vanilla: variants are re-cuts, bevels, brick coursing, offset grids of the SAME palette — never new hues, only new geometry/layout.
**Takeaways.** (1) Group arcane variants under one base + a picker, not N recipes. (2) Author each variant as a re-cut of the base palette (brick/tile/herringbone/panel) — no new colours. (3) Offer plain + connecting versions of large-motif tiles; design the connecting set as one sheet. (4) Make connection span full/stair/slab.
**Signature.** Connecting-texture tiles cut from a single sheet, keyed by neighbours, sharing the base palette.

## Blockus
**Meta.** Block/material-expansion. ~10^7 (~9.3M CF). License: **LGPL-3.0**.
**Techniques.** Two moves. (1) Palette expansion by LAYOUT not hue: Herringbone Planks, Timber Frames, Mosaics for every wood — same plank palette rearranged into new tiling motifs, shipped as first-class blocks. (2) Coherent new-material families: new bases (Viridite, limestone/marble-like) each built out to the FULL shape matrix (block/stairs/slab/wall/pillar) so they feel vanilla-complete. Tight 3–5 value ramps, low busyness matching vanilla, seamless 16px motifs; stonecutter recipes reinforce "one source, many cuts".
**Takeaways.** (1) For a new arcane material, ship the WHOLE shape matrix or it reads unfinished. (2) Add herringbone/mosaic/timber-frame relays of our woodset — new motif, same plank ramp. (3) Keep each material to a 3–5 value ramp at vanilla busyness. (4) Gate variants behind stonecutter-style recipes.
**Signature.** Motif re-lays (herringbone/mosaic/timber frame) that expand a palette by rearrangement, not recoloring.

## Handcrafted
**Meta.** Furniture/decoration (Terrarium, makers of Chipped). ~10^7 (~19.9M Modrinth — top furniture mod). License: **Terrarium Licence** (custom; treat as ARR).
**Techniques.** 250+ pieces built from small reusable ELEMENT MODELS, not unique art per piece. A chair = a few box elements (legs/seat/back) skinned with the existing plank texture of a wood — one model auto-generates the full woodset by swapping material. Axis-aligned box UVs onto plank/log atlases so grain reads on legs/rails; detail is silhouette-driven (chunky legs, thin backs), vanilla density. Cushions/sheets are separate DYEABLE overlay layers.
**Takeaways.** (1) Build furniture from a small library of shared box elements; instantiate the whole woodset by swapping our plank texture — author planks once. (2) Keep box UVs axis-aligned onto the plank/log atlas so grain flows; don't paint bespoke furniture textures. (3) Model detail in silhouette, not texel busyness. (4) Add a dyeable overlay layer (cushions/cloth) for recolor without new models.
**Signature.** One parametric element-model skinned by material — the whole woodset of a piece falls out of a single model + our plank texture.

# CATEGORY: Themed dimensions & creature art (batch 2)

## The Twilight Forest
**Meta.** Themed dimension (biomes + boss-gated progression + block families). ~10^8 (~200M+ CF). License: code LGPL-2.1; assets separate ASSET_LICENSE (CC BY-NC-SA on the port); structures/sounds ARR. Study only.
**Techniques.** Whole dimension commits to ONE lighting key: perpetual dim twilight, desaturated ambient, warm-vs-cool contrast doing the mood work. Cohesion from a shared canopy palette that biomes push off of — Fire Swamp red/charred, Snowy/Aurora blue-white, Enchanted Forest a saturated rainbow (per-block hue-shifted leaves) as a deliberate palette reward. Bosses silhouette-first, each a one-glance read (segmented Naga, robe+crown Lich, crying-face Ur-Ghast). Dungeon block sets (mazestone/towerwood) make a room read as belonging to its boss.
**Takeaways.** (1) Pick one dimension-wide lighting key (for taint: a sickly desaturated cast); let biomes deviate in HUE, not value structure. (2) Give each structure/boss arena its own tight block set. (3) Reserve one hyper-saturated palette (rainbow-oak) as the "special grove" payoff — make the silverwood grove the bright exception. (4) Design each mob to a one-glance silhouette + one identifying accent.
**Signature.** A single committed twilight lighting key unifying wildly different biomes into "one place".

## Deeper and Darker
**Meta.** Themed dimension + block families + mobs (sculk/Otherside). ~10^6–10^7. License: **GPL-3.0** (assets reference-only).
**Techniques.** Monochrome-plus-one-accent masterclass: the Otherside is a cold blue-black sculk/gloomslate value range, and the ONLY natural light is sculk gleam — a teal-cyan emissive that becomes the signature accent against near-black. Because the base is so dark/low-chroma, tiny emissive touches carry huge weight (Echo trees = purple leaves + gleam nodes). Coherent, vanilla-legible families: sculk stone → brick/tiled/chiseled/pillar, gloomslate, echo wood, all sharing the cold palette. The Stalker boss = tall Enderman-height dark figure with a central splitting mouth — one uncanny feature. Ambient ash/smoke at zero palette cost.
**Takeaways.** (1) Build the taint/eldritch biome as low-chroma dark base + ONE emissive accent hue (corrupt violet or bilious green "taint gleam") as the only real light. (2) Derive a whole block family from one corrupted stone. (3) Eldritch boss = tall humanoid-but-wrong silhouette + a single uncanny feature. (4) Drifting particles sell atmosphere at zero palette cost.
**Signature.** Near-monochrome dark palette where a single emissive accent is the ONLY light — max eerie contrast from minimal colour.

## Friends & Foes
**Meta.** Vanilla-plus mobs (design-relevant: Copper Golem, Tuff Golem). ~10^7 (~60M+ CF). License: **CC BY-NC-ND 4.0** (no-derivatives; look-and-learn only).
**Techniques.** "Reads as vanilla, animates as character." Copper Golem = material-as-identity: stubby copper body, tiny limbs, villager-nose head, lightning-rod crown, bright glowing copper-bulb eyes (the one emissive cue). Signature = OXIDATION AS PALETTE LIFECYCLE: four discrete stages walk the vanilla copper ramp (bright orange → exposed → weathered → oxidized turquoise) so the same silhouette tells a time-story through hue/chroma alone. Tuff Golem applies it to stone + a "holds an item" hook. Both keep chunky vanilla proportions.
**Takeaways.** (1) For our golems, let the CORE MATERIAL be the identity (silverwood/brass/taint-crystal) and build the whole texture from that material's ramp. (2) Give each golem exactly ONE emissive cue (glowing eyes / socketed core) as the alive/charged tell; everything else matte. (3) A state-driven palette lifecycle (charge/taint) as a discrete hue/chroma ramp over a fixed silhouette. (4) Keep proportions chunky/vanilla-legible.
**Signature.** Oxidation-as-lifecycle — one silhouette, a discrete multi-stage colour ramp of the same material; reuse as a corruption/charge ramp.

# CATEGORY: Particles & effects (deep dive · batch 2)

## Particular
**Meta.** Ambience/particles (fireflies, leaves, cave dust). ~10^5–10^6. License: **LGPL-3.0**.
**Techniques.** Curated hand-authored ambient effects, not a generic engine: environmental storytelling through SPARSE SLOW particles. Fireflies = small emissive point-sprites spawned at flowers, dusk-gated, drifting on sine wander paths and BLINKING (alpha pulse) rather than moving fast. Cave dust = low-density slow motes reading as suspended air. Leaves arc/flutter (rotation + lateral drift). Everything biome/light-gated — density is the mood control. Sprites are tiny, soft-alpha, tinted per context.
**Takeaways.** (1) Essentia motes should be sparse and slow — a handful of drifting emissive dots reads as "magic in the air"; density, not brightness, sells it. (2) Blink/pulse alpha on aura shimmer (fade out and back), not constant glow. (3) Gate spawns by context (aura level, node proximity) so the effect MEANS something. (4) Give motes a lateral wander/arc, never straight-line.
**Signature.** Dusk-gated, blink-pulsing emissive point sprites with wander drift — the fireflies idiom, ideal for per-aspect essentia motes.

## Effective
**Meta.** Ambience + environmental-interaction particles (absorbed Illuminations bioluminescence). ~10^6. License: **unknown/ARR** (Ladysnake; confirm LICENSE before any reuse).
**Techniques.** Two families. (1) Water interaction: splashes/droplets/ripples on entity entry, waterfall mist where flow hits a source; splash sprites TINTED toward the water/biome colour so effects integrate. (2) Bioluminescence: glowing plankton (blue emissive points in dark), fireflies tracking humidity, will-o'-wisps in soul-sand valleys, floating sculk dust — additive emissive points visible in darkness. Plus non-particle polish: screen shake on big roars, entity trails.
**Takeaways.** (1) Tint interaction particles (crucible splashes, flux bursts) toward the SOURCE's colour so they read as belonging to the liquid/aura. (2) Low-light emissive point clouds are the template for taint/flux corruption haze (sickly-green/purple plankton-analog). (3) Distinct silhouette per phenomenon (wisp vs petal vs dust). (4) Screen shake is a cheap texture-free amplifier for a big ritual/flux beat.
**Signature.** Environment-integrated, biome/liquid-tinted interaction bursts (splash + drifting mist) — the model for reactive crucible/infusion effects.

## Photon
**Meta.** Particle/VFX engine (author tool). ~10^6 (~3.9M CF). License: **CC BY-NC-SA 4.0** (study module design; don't lift code/assets).
**Techniques.** Unity-inspired particle system: emitters with emission shapes (point/sphere/cone/edge), COLOR-OVER-LIFETIME gradients, SIZE-OVER-LIFETIME curves, velocity/rotation modules, texture-sheet flipbook animation, a TRAIL system for beams, and built-in BLOOM so emissive sprites glow without a shader pack. Philosophy: animate every property along the particle's lifetime via a curve/gradient rather than static sprites — a small POT sprite + a colour ramp + a size curve produces most of the look.
**Takeaways.** (1) Drive essentia motes with a colour-over-lifetime gradient keyed to the per-aspect hue (hot core → aspect hue → transparent tail) — one neutral white-hot soft dot recolors to ANY aspect; never per-aspect hand-painted sheets. (2) Size-over-lifetime: spawn small, bloom mid-life, shrink to zero — breathing shimmer. (3) Author beams/wisps as trail geometry (a moving head emitting a fading ribbon), not particle spam. (4) Additive soft-alpha POT sprites so one sheet + bloom serves motes, sparkles, beam cores across all aspects.
**Signature.** A neutral emissive POT sprite recolored by a per-aspect colour-over-lifetime gradient + shaped by a size curve, under bloom — one asset, every aspect hue.

> **Batch-2 north star (adds to batch 1):** Research web = Astral's node-and-line
> constellation Journal on parchment. Apparatus tiers = one neutral stone +
> escalating engraved-rune overlays (Astral) with a hero altar anchoring
> progression (F&A). Crucible/altar = a LIVE fluid/glow gauge in the block
> (Blood Magic/Eidolon). Taint biome = near-monochrome dark + ONE emissive
> "taint gleam" (Deeper&Darker). Golems = material-as-identity + one emissive
> cue + a state-driven colour lifecycle (Friends&Foes). Effects = ONE neutral
> emissive POT sprite recolored per-aspect by a colour-over-lifetime gradient,
> sparse/slow/context-gated, beams as trail ribbons (Photon/Particular/Effective).
> Decorative build-out = motif re-lays + variant pickers + element-model furniture
> off our plank (Blockus/Rechiseled/Handcrafted).

<!-- ============ BATCH 3 ============ -->
# CATEGORY: Storage, functional blocks & QoL (batch 3)

## Quark
**Meta.** Vanilla+ tweak/decoration/QoL (100+ toggleable modules, Vazkii). ~10^8 (~248M CF). License: **CC BY-NC-SA 3.0**.
**Techniques.** Decoration reads as base MC because it extends EXISTING vanilla families rather than inventing new ones: vertical planks, vertical slabs, posts, carved/framed wood, shingles, thatch, per-wood chests, glass items. 16x, drawn from vanilla's own ramps — no new hues, just recombinations, so a Quark block beside oak planks looks first-party. Systematic family structure: each material propagates through block→slab→vertical slab→stairs→wall→post; grouped "palettes" (Industrial/Oriental) stay internally coherent. UX = restrained vanilla-styled widgets: inventory sort button, chest deposit/restock/filter buttons, item-frame tweaks, subtle HUD/tooltip readouts — each small, individually toggleable, styled with vanilla chrome.
**Takeaways.** (1) Extend vanilla block FAMILIES (add slabs/posts/vertical variants of an arcane wood/stone); never a lone one-off. (2) Recombine the existing palette ramp; no new hue a magic block wouldn't justify. (3) Ship QoL UI as small vanilla-styled buttons/tooltips on existing screens, each toggleable. (4) Keep everything 16x + modular — cohesion sells authenticity.
**Signature.** Systematic family completion — define one arcane material, generate its entire vanilla derivative set (slab/vertical slab/stairs/wall/post) in the vanilla palette.

## Storage Drawers
**Meta.** Compartmental item-storage blocks. ~10^8 (~234M CF). License: **MIT**.
**Techniques.** The block FACE is the interface. Each compartment renders the stored item's 3D icon floating on a recessed front panel; empty = blank recessed panel — contents read at a glance, no GUI. A block subdivides its face into a fixed grid (1×1, 1×2, 2×2), so one block fronts 1/2/4 icons. Count text as small numerals (toggleable); a status-indicator upgrade adds a colored fill/level bar strip. Tier/material via the wood-type frame + a border trim; Framed drawers let players retexture. Readability rests on recessed-panel shadow separating icon from wood, consistent icon centering, quantity as a dimmer secondary layer.
**Takeaways.** (1) Reserve a RECESSED inset panel on the jar face where the aspect icon/essentia renders — frame = "container", inset = "contents". (2) Support a subdivided-face convention so a multi-aspect jar shows 2–4 aspect cells each with its own fill. (3) Draw fill as a discrete colored bar + count as small secondary numerals — two separate readout layers. (4) Encode tier through frame material + trim border, leaving the inset free.
**Signature.** Recessed content inset + floating item icon + optional fill-bar strip — contents and fill on the face, no GUI.

## Sophisticated Storage
**Meta.** Upgradeable barrels/chests with an upgrade-slot economy. ~10^7 (~81M CF). License: **All Rights Reserved** (study only).
**Techniques.** Two readability systems. (1) Tier trim as a METAL RING/banding: copper→iron→gold→diamond→netherite recolors a border accent on an otherwise wood body — tier reads instantly from a small trim colour while the body stays neutral. Two-colour dye (main+accent) applied per face, kept distinct from tier trim. (2) Limited Barrels put 1–4 item slots on the front panel (icon + count); higher tiers raise per-slot STACK LIMITS rather than adding slots, so the face stays legible. A Storage Tool toggles on-block overlays (locks/counts/tiers) — opt-in per property so a wall isn't noisy.
**Takeaways.** (1) A thin tier trim/ring in a metal ramp (copper→netherite) makes reagent-container tier a glanceable border accent, not a whole-block reskin. (2) Show aspect on the face as a displayed icon + count; prefer raising per-jar capacity by tier over adding icons. (3) Keep tier colour and aspect tint as independent layers so they never collide. (4) Make face overlays toggleable for large arrays.
**Signature.** Metal-ramp tier trim — identity through a small recolored border accent, body free for aspect colour.

## Jade + Iron Chests (container readouts)
**Meta.** Jade: look-at HUD/tooltip (MIT), ~10^8. Iron Chests: tiered containers (GPL-3.0); Crystal Chest = the canonical "see-the-contents" glass idiom.
**Techniques.** Jade renders a look-at HUD panel (not on-block art): icon+title row then plugin lines; its progress-bar component draws a horizontal FILL BAR with a numeric/percentage label — the reusable "how full/how far" primitive. For containers it lists top contents as icon+count rows. Discipline: hover reveals detail, the block stays clean. Iron Chests complements on the block: tiers read through body material colour, and Crystal/Diamond chests use a TRANSPARENT glass shell that literally exposes the item models stacked inside — contents shown by transparency, not overlay.
**Takeaways.** (1) Give essentia jars a Jade progress line: aspect icon + name + a labeled fill bar (exact %/amount) — precise level lives in the hover, not cramped pixels. (2) Keep the block-face read coarse (which aspect, rough fill via a liquid column); push exact counts to tooltip/HUD + comparator. (3) Borrow the Crystal-Chest transparency idiom: a glass jar whose internal essentia column HEIGHT = fill — the most intuitive display, no text. (4) One fill-bar primitive reused everywhere (jars/crucible/alembic) for a consistent readout language.
**Signature.** The labeled fill-bar progress primitive — one reusable "aspect + amount + bar" row for every reagent container.

## Farmer's Delight
**Meta.** Farming/cooking with functional workstation blocks. ~10^7 (~13M Modrinth port). License: **MIT** (study only).
**Techniques.** State/contents read through IN-WORLD RENDERING, not GUIs. The cutting board renders the placed item flat on the plank surface via a BlockEntityRenderer — so the board texture is a plain low-contrast wood slab acting as a STAGE for whatever floats on it. The cooking pot shows a small liquid/soup disc inside the rim + rising steam particles; the pot reads as dark cast iron with a bright inner "broth" quad that swaps colour per meal. The stove shows lit/unlit via an emissive fire quad in the grate. Tight rustic palette (warm browns, terracotta-red, blackened iron, cream). Boxy vanilla silhouettes + shallow inset trim so blocks read as tools.
**Takeaways.** (1) Author workstation surfaces as neutral low-contrast STAGES; let the rendered essentia jar / infusion item supply the colour + focal point. (2) Encode process state as a single swappable quad (broth disc, glowing grate), not a whole-block repaint. (3) Disciplined rustic palette so a dozen blocks read as one station set. (4) Boxy vanilla silhouettes + shallow inset trim beat complex geometry.
**Signature.** Block-as-stage — a deliberately plain surface whose job is to frame in-world item rendering.

## Reliquary
**Meta.** Magical relic/curio items (charms, fragments, tomes, pedestal). ~10^7–10^8 (~99M CF, Reincarnations fork). License: **All Rights Reserved** (assets not reusable).
**Techniques.** Item icons read "precious/arcane" at 16px through consistent moves: a strong FRAMED silhouette (coins/medallions/pendants get a gold/bronze rim enclosing a coloured gem or sigil centre), high value-contrast between a dark arcane core and a bright metallic edge, and 1–2 hyper-saturated gem/rune accent pixels implying glow without full emissive art. Fragments = torn/irregular shards with a jagged edge + faint inner motif; tomes = leather cover + clasp + coloured inset icon. The Altar/Pedestal displays a held item elevated and lit — the pedestal itself is understated stone with a glowing socket.
**Takeaways.** (1) Give arcane relics a metal FRAME + gem/sigil core so they read as jewelry-precious, not tool-plain. (2) Use 1–2 hyper-saturated accent pixels for glow instead of full-sprite emissivity. (3) Distinguish item classes by silhouette: framed/round = charm, jagged = fragment, clasp-book = tome/focus. (4) Make the pedestal a quiet lit socket; let the displayed focus be the focal point.
**Signature.** The framed-relic idiom — bright metallic rim enclosing a dark arcane core = instant "precious & magical" at 16px.

> **Essentia-jar synthesis (batch 3):** coarse-to-fine readout — a glass/liquid
> COLUMN on the block shows fill height + aspect colour (Crystal Chest + Drawers
> inset), a thin METAL TIER TRIM encodes container tier (Sophisticated), and a
> Jade FILL-BAR line gives exact amount/aspect name + comparator value on hover.
> Workstations are STAGES (Farmer's Delight); relics/foci use the framed-core
> idiom (Reliquary); build breadth by systematic vanilla family-completion (Quark).
