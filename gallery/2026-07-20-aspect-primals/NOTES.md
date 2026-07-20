# Aspect primals icon mockup — 6 primals (2026-07-20)

Mockup for the 6 T.N.A. primal aspect icons. HD hexagonal GUI icons (the
sanctioned exception to 16x, per art-direction.md / aspects.md). Authored at
**64×64** — HD enough for a clear symbol inside a hexagon, still pixel-art.
Nothing committed to the T.N.A. repo; this is a mockup for approval.

## The 6 primals (docs/aspects.md — canonical, do not invent)

| Aspect | Concept | Color | Symbol (concept) |
|---|---|---|---|
| Ventus | Air, wind | #CDE8F5 | wind swirl / gust |
| Tellus | Earth, soil | #6BA84F | mountain peaks + horizon |
| Flamma | Fire, heat | #F0552B | flame |
| Unda | Water, flow | #3D9BE0 | wave crests (flow) |
| Forma | Order, structure | #EDE9DC | square grid (windowpane) |
| Discordia | Chaos, entropy | #4A3459 | jagged shatter-burst |

Distinct silhouettes (swirl / mountains / flame / wave / grid / burst) — passes
the silhouette test; no two read alike.

## Design tension the user flagged

Two primals have extreme-value codes: **Forma #EDE9DC is near-white**,
**Discordia #4A3459 is very dark**. So "symbol in the aspect color on a neutral
bed" fails at both ends (a dark frame + dark symbol for Discordia; a pale symbol
lost on light for Forma). Legibility must come from **value contrast**, chosen
adaptively, not from the hue.

## Two approaches, both built for all 6

- **Frame**: hexagon ring in the aspect ramp (bevelled), dark neutral interior,
  symbol in the bright aspect tint. Color identity = the ring.
- **Backdrop**: hexagon filled with the aspect ramp (the colour IS the identity),
  symbol drawn as an adaptive glyph — light-on-dark or dark-on-light chosen by
  the bed's luminance — plus a thin opposite-value keyline (selout) so it reads
  on ANY aspect colour.

Decision goes to whichever keeps every symbol legible at GUI size (16–64px) AND
gives the strongest at-a-glance colour identity. Prediction: backdrop + adaptive
keyed glyph, because the frame hides dark aspects and weakens colour ID.

## Decision (r2)

**Full backdrop wins.** Reasons, verified on the r1/r2 sheets by eye + the
GUI-size legibility strip (48/32/20px on dark AND light):
- Colour identity holds at every size — you read "the green one / the purple
  one" instantly even at 20px. With 41 colour-coded aspects that at-a-glance
  read is the whole point; the frame reduces colour to a thin ring and at 20px
  every frame icon looks like the same dark hexagon.
- The frame collapses for dark aspects: Discordia's dark ring melts into the
  dark interior and a dark GUI slot (visible bottom-left of the frame row).
- Backdrop symbols stay legible because the glyph tint is pinned to true
  near-white / near-black by the bed's luminance (r2 fix), + a thin opposite
  keyline (selout). Forma (near-white bed → dark glyph) and Discordia (dark bed
  → near-white glyph) both read; the aspect's own extreme code no longer fights
  the symbol.

Verification note: these are 64x GUI icons on transparency, so the block/item
tiling + value analyzer doesn't apply; verified by eye at 1x and at GUI sizes.
Not claiming in-game correctness — hexagon size/placement in real GUIs is Jacob's
eyeball check.

## Open polish options (if we proceed)
- Ventus swirl reads a touch like a "C"; a clearer double-gust would say "wind"
  harder.
- Slightly stronger rim on the two light aspects (Forma, Ventus) for light GUIs.

## r3 — Ventus & Flamma reworked (user feedback: loved the other 4)
- Ventus: dropped the single spiral (read as a "C") for three flowing wind
  gusts, each ending in an upward curl — the universal breeze glyph. Reads as
  wind at 48/32px; slightly dense at 20px but still airy.
- Flamma: replaced the plain teardrop with an asymmetric licking flame + an
  amber hot-core (the one aspect that gets a second symbol colour, justified —
  fire reads as white-hot body around a glowing centre). Distinct from Unda's
  wave now.
- Other 4 (Tellus/Unda/Forma/Discordia) unchanged — user-approved.

## Discordia symbol options (user asked for a few designs)
Four on the same #4A3459 backdrop (previews/discordia-options.png):
- burst — spiky solid star (current r3); reads explosion/burst.
- crack — shattered-glass web (radial cracks + connecting web; sharp capless
  strokes so it doesn't bead); reads "broken surface".
- shards — a form split into separated flying triangular pieces.
- scatter — a solid block dissolving into scattered squares; the most literal
  "entropy / order→disorder". Added _stroke_sharp helper + sym_crack/shards/
  scatter to make_aspects.py.
