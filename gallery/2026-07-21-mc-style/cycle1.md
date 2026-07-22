# MC-style cycle 1 — aggressive critique of our stone output vs vanilla Minecraft

Goal: compare our generated textures to how vanilla Minecraft actually looks, find where our style
diverges, and fix it. Study-only (reference-policy: learn the look, no committed pixels).

## What makes a texture read as "Minecraft" (Blockbench style guide + Faithful docs)
1. **Deliberate pixel placement, NOT noise.** The style guide explicitly calls random per-pixel
   brighten/darken ("noise") a *novice* technique that "adds no information" and can make a texture
   unrecognisable. Pixels are placed on purpose.
2. **Structured CLUSTERS, not chaos.** Detail comes from small organised clusters (and ordered
   dithering for transitions), not scattered singles.
3. **Limited AND contrasty palette.** Few colours, with real value contrast between them — not a
   near-flat wash.
4. **16x16, clear read.** Small res, but each block is instantly identifiable; features are defined.

## Honest critique of OUR stones (gallery/2026-07-21-stone-practice)
- **The base fill is per-pixel `h2(x,y)` noise — the exact anti-pattern.** marble/slate/shale/
  basalt/sandstone bases are independent per-pixel speckle → they read as fine "TV static", the
  computer-generated look, not vanilla's hand-placed blotches. **This is our biggest style gap.**
  (Ironic: our own `shading.md` already says "noise reads as dirt; detail comes from CLUSTERS —
  irregular rounded potato shapes" — the procedural generator violated our own rule.)
- **Contrast too low.** The subtle 3-tone ramps (esp. the near-white marble) are lower-contrast than
  vanilla stone, which has clearer darks/pits. Reads washed-out / flat.
- **Granite is closest to right** (multi-mineral specks read as crystals) but is still per-pixel, so
  it sparkles as static rather than clustering into grains.
- **What we already do right:** deliberate structured *features* (veins with edge anchors, laminae,
  bedding, vesicle pits), limited palettes, 16x16, tiling discipline, rotation-safety.

## The #1 fix (cycle 2)
Replace the per-pixel noise base with **clustered blotches**: sample the base variation at a coarser
scale (2-3px cells) and/or grow small irregular clusters, so the fill reads as deliberate potato-shape
blobs like vanilla — then bump contrast a notch. Add a `cluster` value to stonegen (data-driven) and
render per-pixel-vs-clustered side by side to prove the difference. Keep the good structured features.

## Sources (study only)
- Blockbench — Minecraft Style Guide: https://www.blockbench.net/wiki/guides/minecraft-style-guide/
- Faithful Docs — texturing glossary (noise, dithering, contrast): https://docs.faithfulpack.net/pages/textures/glossary
