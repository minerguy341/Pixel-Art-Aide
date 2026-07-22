# Mineral cycle 1 — crystal properties → how a crystal/gem sprite is built

Scope: the physical properties mineralogists use (habit, cleavage/fracture, luster, hardness,
diaphaneity) and how each maps to a pixel lever for crystals, gems, and ores.

## Findings
- **Crystal HABIT = the characteristic shape** (set by atomic structure + growth environment):
  **prismatic** (elongated, parallel faces, often striated along length) · **tabular** (flat plate,
  L&W >> thickness) · **botryoidal** (rounded grape-like lobes, concentric growth around nucleation
  centres) · **drusy** (a crust of tiny sparkling crystals lining a cavity) · **radiating/geode**
  (crystals grow outward from a centre, points lining the inside of a geode).
- **Cleavage vs fracture = how it breaks.** Cleavage = smooth flat **parallel planes** (weak bond
  directions) → straight clean facet edges. **Conchoidal fracture** (quartz, obsidian, glass) = curved,
  shell-like chips → rounded/irregular edges.
- **Luster = how the surface reflects light:** metallic · vitreous/glassy · adamantine (brilliant,
  diamond) · dull/earthy · pearly · silky.
- **Mohs hardness = atomic bond strength** — also tracks how well sharp edges survive (hard = crisp
  facets, soft = rounds/scratches).
- **Streak** = the mineral's powder colour (can differ from surface colour — a mineral's "true" colour).
- **Diaphaneity** = transparent / translucent / opaque.

## Crystal/gem pixel lessons
1. **HABIT sets the silhouette + facet layout** — prismatic = elongated hex shard; tabular = flat plate;
   botryoidal = rounded bubbly lobes; drusy = fine sparkle crust; geode = radiating points from a centre
   lining a cavity. Pick a crystal sprite's shape from its habit, not a generic lump.
2. **Cleavage vs fracture sets edge geometry** — cleavage minerals get **flat straight parallel facet
   edges** (clean, angular); conchoidal-fracture ones (quartz/obsidian/glass) get **curved, shell-like
   chipped** edges. (Refines the crystal/glass shorthand: "few large facets, each one flat step.")
3. **Luster sets the highlight treatment** — metallic → one bright specular cluster; vitreous/glassy →
   crisp highlight + partial transparency; adamantine → brilliant multi-point sparkle; dull/earthy →
   matte, no specular; pearly/silky → soft low sheen. (Extends the metal/crystal shorthand.)
4. **Hardness ↔ edge sharpness** — hard minerals keep sharp angular facets; soft ones round/erode.
   (Ties to the stone-study "hardness = weathering" lever.)
5. **Diaphaneity = the alpha budget** — a transparent gem = large facets with binary-alpha edges and a
   see-through core; a translucent stone dims what's behind; an opaque ore is solid. (Ties to the
   glass/leaves cutout-vs-translucent lessons.)

## Sources (study only)
- OpenGeology Mineralogy — properties: https://opengeology.org/Mineralogy/3-properties/
- Geology.com — crystal habits & forms: https://geology.com/minerals/crystal-habit/
- Geology In — crystal habits (photos): https://www.geologyin.com/2019/10/crystal-habits-and-forms.html
- Geosciences LibreTexts — identifying minerals: https://geo.libretexts.org/Courses/Coalinga_College/GEOL_001:_Intro_to_Physical_Geology/03:_Minerals/3.05:_Identifying_Minerals
