# Mineral cycle 3 — geography & landforms → placement, cliffs, caves, formations

Scope: how rock reads at world scale (strata, differential weathering, cave speleothems, geodes) →
worldgen placement + surface texture cues; connects the habit/chromophore cycles to the landscape.

## Findings
- **Strata / bedding.** Sedimentary rock appears as horizontal **bands/stripes of alternating layers**
  (Grand Canyon cliff faces). Beds are usually horizontal but can **tilt** (tectonics) or **cross-bed**
  (angled internal laminae from the original deposition gradient, up to ~30°).
- **Differential weathering shapes the land.** Resistant strata (sandstone, limestone, lava flows) stand
  as **cliffs / caprock / spires / hoodoos**; soft strata (shale) erode to **slopes**. Hoodoos = stacked
  hard/soft layers. Cliff-and-bench topography is strongest in arid climates.
- **Cave speleothems** (calcite from limestone, redeposited as acidic water degasses CO₂ / evaporates):
  **stalactite** (tapered, ceiling-down) · **stalagmite** (floor-up) · **flowstone** (smooth banded
  sheets) · **soda straw** (thin hollow tube) · **anthodite** (radiating spiky needle clusters) ·
  **drapery** (wavy curtains). Colours **tan / orange / brown** (calcite + humic acids); some **fluoresce
  under UV**.
- **Growth = concentric/layered deposition.** Flowstone and speleothem cross-sections show **concentric
  banding**; a geode is a cavity **lined with radiating crystal points** grown inward toward a hollow centre.

## Pixel / design lessons
1. **Layered rock reads as horizontal BANDS** of alternating value/hue (tilt or cross-bed for drama) — the
   world-scale form of the stone-study "structure = bands" axis; expose banding on cliff/strata blocks.
2. **Differential weathering couples hardness to BOTH texture and worldgen** — resistant rock = sharp
   blocky texture + cliffs/spires/hoodoos; soft rock = rounded texture + slopes. (Extends "hardness =
   weathering" to placement, not just edges.)
3. **Cave formations are their own material family** — build them from the speleothem vocabulary
   (stalactite/stalagmite taper, flowstone smooth banded sheet, soda-straw tube, **anthodite = the
   radiating crystal habit from cycle 1**, drapery curtain), warm tan/orange/brown, with an optional
   faint glow (UV fluorescence → a ready magic-glow hook). Don't render cave decor as generic rock.
3b. **A geode / crystal cavity = dark rough host rind + inward-radiating bright crystal points around a
   hollow centre**, the crystal hue set by its chromophore (cycle 2). Dark host + bright facets + one
   saturated hue is the whole recipe.
4. **Formations grow in concentric layers** — a cut geode/flowstone shows **concentric rings** around a
   centre (same grammar as tree end-grain / agate); use rings for any deposited/precipitated cross-section.

## For T.N.A.
Arcane/aura crystals read naturally as **geode-lined cavities** or **anthodite-like radiating clusters**;
the "magic glow" maps onto real **UV-fluorescent calcite**; aura-crystal growth = concentric deposited
banding. Cool blue-grey arcane stone can host a teal crystal geode as its "charged" state.

## Sources (study only)
- USGS — Geology of Bryce Canyon (hoodoos / differential weathering): https://www.usgs.gov/geology-and-ecology-of-national-parks/geology-bryce-canyon-national-park
- OpenGeology — weathering, erosion & sedimentary rocks: https://opengeology.org/textbook/5-weathering-erosion-and-sedimentary-rocks/
- Wikipedia — cross-bedding: https://en.wikipedia.org/wiki/Cross-bedding
- National Speleological Society — mineral deposits / formations: https://caves.org/virtualcave/mineral-deposits/
- Encyclopedia.com — cave minerals & speleothems: https://www.encyclopedia.com/science/encyclopedias-almanacs-transcripts-and-maps/cave-minerals-and-speleothems
