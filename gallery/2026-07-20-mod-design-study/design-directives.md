# T.N.A. art-direction directives — distilled from the 32-mod study

Actionable rules synthesized from the mod design study (findings.html). A studio
deliverable for review; sync the keepers into `docs/art-direction.md` (upstream)
when approved. Every rule is an IDIOM learned by study — no mod pixels are used.

## 0. The one meta-rule
Keep blocks, items, and mobs **vanilla-scale 16px and restrained**. Spend the
"arcane" budget on **light** (emissive cores, glowing particles) and **the
per-aspect hue system** — never on out-detailing the base game. This single rule
is what makes Alex's Mobs, Occultism, Create, and Deeper&Darker all read as
"official." (Cataclysm-scale bosses are the only sanctioned resolution bump, and
only if committed to consistently.)

## 1. Apparatus blocks (crucible, alembic, worktable, infusion, orrery…)
- **Neutral material, magic as accent.** Apparatus are a restrained material
  (cool dressed arcane blue-grey stone; brass instruments; aetherium trim), so
  saturated glow reads as the magic. Distinguished from Create by MATERIAL, not
  by copying its brass. (Create/Mekanism/F&A)
- **Framed-panel grammar.** Recessed panel + beveled rim + corner rune-studs +
  subtle banding = "built apparatus." One highlight row per material; matte.
- **Emissive core = state.** A single glowing inset (teal glint / aspect hue)
  marks active/charged; base block stays dark. (Embers/Malum/Eidolon)
- **The block IS the gauge.** Show resource in the block: a rising fluid level
  (crucible), a filling glow, bubbling + steam over a fire block below. Make cost
  visible and dramatic. (Blood Magic/Eidolon)
- **Tier = engraved density, not new palette.** One base stone + escalating
  carved-rune overlays reads as a tiered family. Anchor progression with ONE
  hero altar of bold silhouette. (Astral Sorcery/F&A)
- **Ritual = floor geometry.** Multiblock rituals as flat glyph-tile
  arrangements (master stone + patterned stones); a few named chalk/rune colours;
  ship an in-world ghost preview in the Codex. (Occultism/Blood Magic)
- **Apparatus family = shared base + swappable focus/face.** A chassis carrying an
  information-bearing front (aspect glyph / colored port) identifies each device.
  (Ars Nouveau/Mekanism)

## 2. Effects / particles (essentia, aura, flux, beams)
- **One neutral emissive POT sprite, recolored at runtime** by the per-aspect hue
  — never per-aspect hand-painted sheets. (Photon)
- **Animate along lifetime:** colour-over-lifetime (hot core → aspect hue → clear
  tail) + size curve (grow→peak→shrink) + alpha blink for shimmer; under bloom.
- **Sparse, slow, context-gated.** A handful of drifting motes = "magic in the
  air"; density tracks aura strength; wander/arc, never straight lines. (Particular)
- **Give each aspect a 3-stop ramp** (dark core → mid → pale hot tip); drive the
  tint from a data value so aura/essentia/flux each get a family. (Embers)
- **Tint reactive bursts to their source** (crucible splash, flux field) so they
  integrate. Distinct silhouette per phenomenon (mote/wisp/haze/beam). (Effective)
- **Beams/wisps = fading trail ribbons**, not particle spam. Make invisible flow
  visible: mana/essentia travels as a glowing arc/mote-stream between blocks.
  (Photon/Botania/Embers)

## 3. GUIs (Codex, Arcane Worktable, tooltips, aspect grid)
- **Codex hierarchy:** book → category grid → entry list → paged entry, with
  **locked/greyed entries** gated on research; typed page templates; a
  **relations link-graph** page as the seed of the aspect/research web. (Patchouli)
- **Research web = node-and-line line art on parchment** you trace to discover —
  the aspect-linking globe/grid's visual language. (Astral Sorcery)
- **Worktable = searchable categorized palette + ordered slot chain + live
  vis-cost/validity readout**, recomputed on every change. (Ars Nouveau)
- **Browse large aspect sets** with a docked filterable slot-grid + prefix search
  (`@school`, `#aspect`) + click-to-see-uses cross-links. (JEI/REI)
- **Tooltips/HUD = nine-slice card**, fixed header (icon+name), stacked typed
  rows (aspect glyph + count chips, vis cost, "requires research X"), a muted
  footer identity line. Drive rows from data. (Jade)
- Build all panels/buttons/cards as **1.21 nine-slice sprites** for HD scaling.

## 4. Icons (the 41 aspects — already in progress)
- **Fixed per-aspect hue system** is the single source of visual identity;
  propagate the same hue through icon, particles, UI accents, damage type.
  (Iron's Spellbooks) — we already have the palette.
- Matched emblem set: shared silhouette language, high contrast, uniform frame;
  a grid scans as one set. (done for our 15 locked + 26 drafts.)

## 5. Creatures (golems, eldritch/taint mobs)
- **Material-as-identity:** build the whole texture from one material's value ramp
  (silverwood/brass/thaumium/taint-crystal). (Friends&Foes)
- **Exactly one emissive cue** per creature (glowing eyes / socketed arcane core)
  = the alive/charged tell; everything else matte. (Cataclysm/Friends&Foes)
- **State-driven colour lifecycle:** a discrete hue/chroma ramp over a fixed
  silhouette for charge level or taint corruption. (Friends&Foes oxidation idiom)
- **Silhouette-first, one signature feature**; chunky vanilla proportions;
  telegraphed weighty animation for bosses. (Alex's/Mowzie's)
- **Arcane = cyan/violet glow; taint/corruption = sickly green-purple.**

## 6. Biomes (silverwood grove, taint/eldritch)
- **One committed lighting key per dimension/biome;** biomes deviate in HUE, not
  value structure. Taint = a sickly desaturated cast. (Twilight Forest)
- **Taint/eldritch = near-monochrome dark base + ONE emissive "taint gleam"** as
  the only real light; derive a whole block family from one corrupted stone;
  drifting ash/spore particles at zero palette cost. (Deeper&Darker)
- Reserve ONE hyper-saturated palette as the "special grove" payoff — make the
  **silverwood grove the bright exception**. (Twilight Forest)

## 7. Decoration & material build-out
- **Wood/material families:** author the plank once; UV-map it through vanilla
  parents for every shape; author new pixels only for door/trapdoor/sign/boat +
  one **shared iron hardware ramp**. (Framed/Macaw's/Supplementaries — done for
  greatwood/silverwood.)
- **Expand a palette by re-lay, not recolour:** herringbone / mosaic / timber-
  frame / brick motifs of the same plank ramp; ship the FULL shape matrix per new
  material or it reads unfinished. (Blockus)
- **Variants under one base + a chiseling picker**, not N recipes; plain +
  connecting-texture forms from one sheet. (Rechiseled/Chipped)
- **Furniture from a small library of shared box element-models** skinned by our
  plank + a dyeable cushion overlay. (Handcrafted)
- **Labeled/visual storage** (essentia jars): show aspect + fill on the block
  face; comparator-readable; tiered trim. (storage study — batch 3)
- **State-driven decor props** (melting candles, filling jars) add living
  ambiance cheaply. (Hexerei)

## Licensing note
Every mod above was studied for public documented idioms only. Licenses ranged
MIT/LGPL/GPL/CC-BY to ARR and CC-BY-NC-ND — **all treated as study-only**. Any
reference capture stays in scratchpad; shipped art is original, aspect hues sync
from `docs/art-direction.md`. (`knowledge/reference-policy.md`.)
