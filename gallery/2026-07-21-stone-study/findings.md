# Stone & rock study — Arcane Stone + geology → pixel rules (for T.N.A.)

Study/reference only (reference-policy: learn the idiom, no committed pixels). Goal: a craft base
for authoring the mod's **Arcane Stone** and future stone blocks. Three angles: Thaumcraft's Arcane
Stone, mod/vanilla stone texturing, and real geology (chemistry → coarseness/color/structure).

## 1. Real geology → the pixel levers
Rocks are classified by exactly two things — **texture (grain) and composition (chemistry)** — and
those map cleanly onto our two texture dials (arrangement/busyness and palette).

- **Grain size = coarseness = how the rock formed.** Visible interlocking crystals (>2 mm) = slow/deep
  igneous (granite, gabbro) or coarse metamorphic (gneiss); **no visible grain** = fast-cooled surface
  igneous (basalt, rhyolite) or fine sedimentary. → **Cluster size** in the texture: coarse rock =
  larger, distinct 2–4 px mineral clusters; fine rock = near-flat base + fine 1 px speckle.
- **Color = chemistry (silica vs iron/magnesium).** **Felsic** (>65 % silica; quartz + feldspar + mica)
  = **light** — pink/white/light grey (granite, rhyolite, quartzite, marble). **Mafic** (45–55 % silica,
  high Fe/Mg) = **dark** — black/dark-grey/greenish (basalt, gabbro). **Iron oxide** = warm red/brown/
  orange (banded iron, weathered/rusted rock). → Pick **base value + hue from composition**: felsic pale-
  cool, mafic dark, iron warm.
- **Structure = the formation process** (a third axis, independent of palette):
  - **Plutonic igneous** (granite/gabbro) → **salt-and-pepper speckle** of several distinct mineral colours.
  - **Volcanic igneous** (basalt) → **near-flat**, uniform, occasional vesicle.
  - **Sedimentary** (sandstone) → uniform cemented grains + **faint horizontal bedding**; grains stay
    intact when broken (loosely bound).
  - **Metamorphic foliation** (gneiss) → **alternating dark/light BANDS** (wavy, not straight).
  - **Metamorphic vein** (marble = metamorphosed limestone/calcite) → smooth pale body + **wandering veins**
    (quartz veins literally cut across the rock).
- **Hardness = weathering resistance.** Quartz-rich rock (quartzite) is hard and keeps **sharp angular**
  edges; softer rock **rounds/erodes**. → sharp clusters for hard stone, rounded for soft/weathered.

## 2. Mod & vanilla stone idioms
- Vanilla's stone family (stone, andesite, diorite, granite, tuff, deepslate, calcite, basalt) is **one
  speckle grammar differentiated by value + hue**: andesite = neutral grey-green mottle, diorite = light
  speckle, granite = pink speckle, tuff = grey-brown, deepslate = dark with a near-vertical grain. This is
  the geology rule (§1 color+grain) already applied — and matches our existing lessons: *"value + busyness
  place a material class"* and *decorative variant families = one palette, structural variation*.
- Craft rules already in `shading.md` hold: **clusters, not noise** (irregular rounded "potato" shapes,
  shadow lower-right); base resolution 16; tileable; value-uniform full face (so stairs/slabs/walls don't
  shatter a hero motif); ship 2–3 variants to break wall repetition.

## 3. Thaumcraft Arcane Stone (evoke, never copy)
- **What it is:** crafted from 8 stone + a vis shard (Terra + Ignis vis) at the Arcane Workbench → 9 Arcane
  Stone; works like stone (stairs, slabs, **bricks**), "aesthetically pleasing." Higher tiers substitute
  **Ancient/Eldritch stone** for infusion altars. So it's a **dressed, refined, quarried-by-wizards** stone
  — not rough natural rock, not mossy ruin.
- Our style card already fixes the look: *"cool DRESSED arcane stone (blue-grey, tidy mortar, subtle
  runes) — quarried by wizards, not mossy ruin"* + reserve emissive glow for the truly magical.

## 4. Proposed Arcane Stone spec (fits the thaumaturgy card)
- **Material read:** a **refined dressed ashlar** — closer to fine metamorphic/cut-stone than rough granite.
  Cool **blue-grey**, mid value (~40–60 % luminance, inside the house band), **low busyness** (2–4, calm),
  fine speckle only. Smooth and tidy, not craggy.
- **Family** (per "systematic family completion" + "decorative variant" lessons): raw arcane stone (smooth
  dressed) → **arcane bricks** (tidy mortar lines) → **chiseled/runed** (a faint engraved sigil) → pillar.
  One locked palette; variation is structural (brick/tile/pillar/carve), not new colour.
- **Arcane accent:** faint engraved **runes**, minimal + glowing-outlined, on the chiseled/runed variant
  only; the teal `#7FE8D8` glint reserved for that emissive variant, sparse — the base stays matte cool grey.
- **Structure choice:** the base could lean **subtle foliation/vein** (metamorphic, "quarried by wizards"
  reads refined) or a very fine even speckle — both fit; worth trying both as candidates.

## Sources (study only)
- Rock classification & felsic/mafic: MEKA (rock types) https://www.mekaglobal.com/en/blog/rock-types-igneous-sedimentary-metamorphic ; Britannica "felsic rock" https://www.britannica.com/science/felsic-rock ; Geology In (mafic vs felsic) https://www.geologyin.com/2023/09/mafic-vs-felsic-rocks-difference.html ; Utah Geological Survey https://geology.utah.gov/map-pub/survey-notes/glad-you-asked/igneous-sedimentary-metamorphic-rocks/
- Structure: Wikipedia Gneiss https://en.wikipedia.org/wiki/Gneiss ; Banded iron formation https://en.wikipedia.org/wiki/Banded_iron_formation ; Geosciences LibreTexts metamorphic textures https://geo.libretexts.org/Bookshelves/Geology/Book:_An_Introduction_to_Geology_(Johnson_Affolter_Inkenbrandt_and_Mosher)/06:_Metamorphic_Rocks/6.03:_Metamorphic_Textures
- MC stone family: Minecraft Wiki "List of block textures" https://minecraft.wiki/w/List_of_block_textures
- Thaumcraft Arcane Stone: Thaumcraft 4 Wiki https://thaumcraft-4.fandom.com/wiki/Arcane_Stone ; FTB Wiki (TC6) https://ftb.fandom.com/wiki/Arcane_Stone_(Thaumcraft_6)
