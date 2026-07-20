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

## Discordia round 2 — researched chaos/entropy idioms
Grounded in a web pass on chaos/entropy iconography (studied idioms only, own
pixels — reference-policy). previews/discordia-options2.png:
- chaosstar — radiating uneven arrows (Moorcock Symbol of Chaos idiom); iconic
  but hub is busy at 20px.
- vortex — two-arm turbulent spiral; clean, reads as whirl.
- butterfly — Lorenz attractor (the scientific symbol of chaos); two overlapping
  tilted loops; elegant, distinct.
- hourglass — entropy/time + order<->chaos balance; top full, sand dispersing out
  the base; clearest read at every size.
Added _arrow/_ellipse_pts helpers + sym_chaosstar/vortex/butterfly/hourglass.
Sources: Symbol of Chaos (Wikipedia); Lorenz attractor as the symbol of chaos.

## Discordia locked — polished chaos star (r4)
User picked the chaos star; reworked for legibility: even 45° arrow spacing
(chaos lives in the uneven lengths, not the crowding), each arrow = straight
shaft + a crisp filled triangle head (new _arrow2), and a clean central diamond
hub so the shafts read as radiating instead of a blob. Discordia symbol in
make_aspects.py switched burst->chaosstar. Final 6 primals: previews/candidates-r4.png.

## Filled-backdrop locked + Tellus centred + compound candidates (user request)
- Treatment decision final: **filled backdrop only** (frame dropped). Refactored
  make_aspects: backdrop_canvas(code) -> (im,d,fill,key) shared bed + adaptive
  contrast; make_backdrop uses it.
- Tellus re-centred: dominant central peak + left shoulder, bbox ~y19..44,
  vertically balanced about the hex centre (was bottom-heavy).
- Picked 3 compounds and gave 5 candidates each (compounds.py + previews/
  compound_sheets.py):
  - Lumen (light #FFE066): sun / sparkle / radiant burst / dawn / haloed orb
  - Vita (life #C43C55): heart / heartbeat / seedling / sprouting seed / frond
  - Arcanum (magic #DD4FD0): rune / sparkle+orbits / arcane ring / wand+star / swirl
  Adaptive contrast handled all: Lumen light bed -> dark glyph, Vita/Arcanum ->
  light glyph. Fixed lum_dawn rays (first pass read as grass).

## Picks + Arcanum round 2
- Chosen: Lumen = sparkle (candidate 2); Vita = heartbeat/pulse (candidate 2).
- Arcanum: user wanted more options. Second batch (compound-arcanum2.png):
  runic seal · 6-point star · scrying orb · alchemical sigil · crescent+star ·
  comet. (First batch was rune/sparkle+orbits/ring/wand+star/swirl.)

## Arcanum batch 3 — researched arcane iconography (10 candidates)
Web pass on magic/occult/alchemy symbols (studied idioms, own pixels). 10 in
compound-arcanum3.png: pentacle · ouroboros · triquetra · runic compass
(vegvisir) · mercury glyph · third eye · grimoire · bold rune · mandala ·
alchemist's phial. Sources: Pentagram/Pentacle, Ouroboros, Triquetra, Alchemical
symbol, Vegvisir (Wikipedia/sacred-geometry refs).
Pentacle tidied: star inscribed so its 5 points touch the ring (was floating with
a gap); ring drawn first, pentagram on top.
Note: third eye overlaps conceptually with a future Acies (perception) aspect —
flag if both get used.

## Arcanum locked = Pentacle
User chose the pentacle. Fixed so the circle is uninterrupted: draw the pentagram
FIRST then the ring on top (was ring-first, star drawn over it broke the circle).
R=16.5 so the 5 points tuck just under the ring. Final picks: Lumen=sparkle,
Vita=heartbeat, Arcanum=pentacle.

## Three more aspects, 5 candidates each (material/energy set)
compounds.py + compound-{vigor,gemma,aes}.png:
- Vigor (energy #F2C230): bolt · bolt-in-circle · power core · charged cell · double bolt
- Gemma (crystal #9FE6C9): cut gem · crystal cluster · emerald cut · crystal point · polished jewel
- Aes (metal/ore #ADAFBC): ingot · anvil · ore chunk · cog · nugget cluster
All three are light beds -> dark glyphs. Swapped Gemma hex-gem (blended with the
hexagon backdrop) for an emerald cut; gave polished jewel real facets.

## Vigor locked + Gemma tilt / Aes ingot revisions
- Vigor = lightning bolt (locked).
- Gemma: reworked to a top-tilted faceted gem (crown/table dominant like #5 but
  3D with a culet point). 3 tilt degrees: tilt A / more-top / more-side
  (gem_toptilt*). Earlier "angled A/B" (front kite) superseded.
- Aes ingot: 3 dimensional options (aes_bar single 3D bar, aes_stack pair,
  aes_pyramid 3-bar pile) via a shared _bar() helper. Dropped aes_iso — two
  same-tone faces can't separate with only 2 colours (read as a dark blob).
  Sheet: previews/gemma-aes-r3.png.

## Gemma locked + Aes ingots round 2 (researched real ingots)
- Gemma = original cut gem (#1 gem_brilliant, front brilliant). Tilt experiments
  set aside.
- Aes: web pass on real ingot shapes (bullion draft angle; Chinese sycee/yuanbao
  boat ingot). 5 candidates in compound-aes2.png: gold bar (bullion, 3/4 with
  stamp) · stacked bars · sycee (boat ingot, swept ends + knob) · flat bar
  (vanilla-ish) · cast loaf. Sources: Sycee (Wikipedia), bullion bar refs.

## Aes isometric ingots (user: "maybe an isometric angle?")
Added a small iso-box renderer (_iso_box) + _metal_shades deriving a 4-tone metal
ramp (top lit / left mid / right dark / edge) from the aspect code. 4 candidates
(iso_single, iso_wide, iso_pair, iso_stack ×3) in compound-aes-iso.png. These are
a deliberate exception to the flat 2-tone glyph system — a metal ingot reads far
better as a 3-face shaded mini-render (same reasoning as Flamma's hot core). The
earlier flat aes_iso failed because 2 tones can't separate 3 faces; this fixes it
with real face values. Holds down to ~20px (stack strongest).

## Aes LOCKED = iso stack ×3 (with shine)
Added a specular streak + glint on each ingot's top face (_facebox) so they read
as polished metal, not bricks; _metal_shades now returns a 5th shine tone.
All 12 aspects locked: 6 primals + Lumen(sparkle) Vita(heartbeat) Arcanum(pentacle)
Vigor(bolt) Gemma(cut gem) Aes(iso stack). Milestone sheet: previews/locked-12.png.

## Three more aspects, 5 candidates each (ice / death / aura)
compounds.py + compound-{glacies,letum,aether}.png:
- Glacies (ice #A9E7F5): snowflake · icicles · ice shards · frost sparkle · ice block
- Letum (death #45403E): skull · scythe · crossed bones · tombstone · skull & crossbones
- Aether (aura #B37FE8): radiant node · aura swirl · aura rings · spirit wisp · haloed mote
Glacies/Aether are light beds -> dark glyphs; Letum is a dark bed -> light glyphs.

## Picks + Aether batch 2
- Glacies = snowflake (sharpened: pointed diamond arm-tips, symmetric pointed
  branch pairs, crisp 6-point hex core).
- Letum = tombstone (let_grave). (Iso skull built too — iso_skull() — kept in
  code as a reusable option but not chosen.)
- Aether batch 2 (compound-aether2.png): radiant orb · crystal node · aura mist
  · aurora bands · drifting motes · aura pulse. (Batch 1 was node/swirl/rings/
  wisp/mote.)

## Aether locked + Letum tombstone candidates
- Aether = radiant orb (aeth_orb).
- Letum: 5 tombstone/grave candidates (compound-letum2.png): rounded+cross ·
  cross marker · gothic arch · weathered · celtic cross. Improves the earlier
  plain grave.

## Tombstones — symmetry fix
Rebuilt all 5 grave candidates mirror-symmetric about the icon centre-line
(AX=31.5) via shared _round_stone/_ground helpers (were built about x=32, 0.5px
off, plus the weathered chip broke silhouette symmetry). Symbol asymmetry ~halved
(gothic arch 3.4%). Weathered now keeps a symmetric silhouette with a short upper
crack instead of a full-height split. (Backdrop hexagon carries ~5.9% sub-pixel
rasterisation asymmetry — baked into all icons, not visually lopsided; left as-is
so the 15 locked icons don't change.)

## Letum LOCKED = celtic cross. 15 aspects locked.
6 primals + Lumen(sparkle) Vita(heartbeat) Arcanum(pentacle) Vigor(bolt)
Gemma(cut gem) Aes(iso stack) Glacies(snowflake) Letum(celtic cross) Aether(radiant orb).
Milestone: previews/locked-15.png.

## Overnight batch — first-pass candidate for EVERY remaining aspect (26)
One draft icon each for all 26 remaining compounds (REMAINING list in
compounds.py), grouped by tier, for morning review. Concepts:
T1: Impetus(motion chevrons) Inane(void rings) Procella(storm cloud+bolt)
    Toxicum(poison drop) Mutatio(cyclic arrows)
T2: Anima(ghost) Umbra(crescent+stars) Aviditas(toothed maw) Remedium(plus)
    Flora(flower) Fera(paw) Via(signpost) Ala(spread wings)
T3: Mens(head+spiral) Acies(eye) Macula(dripping taint) Silva(tree) Caro(meat)
    Larva(skeletal hand) Persona(mask)
T4: Artificium(hammer) Automata(gears) Ensis(sword) Praesidium(shield)
    Opes(coin stack) Barathrum(eldritch eye+tentacles)
Fixed Silva (was lollipop → wide bumpy crown) and Ala (was blocky → spread wings).
Deliverables: previews/remaining-26.png (labelled by tier/concept),
previews/full-41.png (all 41 = 15 locked + 26 candidates). These are DRAFTS,
user picks/refines per aspect tomorrow.
