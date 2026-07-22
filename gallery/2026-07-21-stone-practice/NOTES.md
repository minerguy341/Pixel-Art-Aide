# 2026-07-21 — stone practice (geology lessons applied) + magic-infused stone

Practice piece: author marble/shale/slate applying the new stone-study lessons, then reuse the
techniques for an arcane (magic-infused) stone. 16x16 tiling. Generator: src/make_stones.py.

## Real stones (lessons applied)
- **marble** — pale calcite body + 2 wandering grey veins (S2 pale/felsic, S3 vein structure, low
  busyness). Reads clearly as marble; veins tile. STRONG.
- **shale** — dark cool grey + thin horizontal laminae every 3px + fine flecks (L1 bands, soft/flat).
  Reads as layered fissile shale; a touch brick-ish from the lamina+fleck rhythm but on-type.
- **slate** — cool blue-grey, horizontally-biased foliation grain + mica sheen flecks + faint cleavage
  lines (S3 foliation, C4 slightly sharper). Reads as slate.

## Arcane / magic-infused (techniques reused)
- **A veined** — glowing teal vis veins wander through blue-grey stone + pale gangue halo (marble-vein
  technique + O3 chromophore + O4 halo). Reads as "vis coursing through stone." STRONG — most compelling.
- **B geode** — sparse teal crystal clusters, faceted with a bright light-return facet (ore/geode +
  G3 bright/dark facet). Reads as arcane ore/crystal deposit. Clusters tile a bit regularly (grid) — would
  vary positions for a final.
- **C runed** — dressed stone + an engraved sigil glowing teal (S5 dressed + emissive reserved for runed).
  Concept right, but the sigil reads MESSY (scattered teal marks, not a clean glyph) — needs a crisper,
  studied rune shape (see the aspect-glyph lessons: study real iconography, draw the motif clearly).

## Takeaway
The geology lessons transfer cleanly: marble's wandering-vein technique → glowing vis veins (A) is the
strongest "magic-infused stone." B is the ore/geode read. C needs a better glyph. All tile (seam ratios
~0.4-1.0). Teal on A/B is above the card's ≤3% (deliberate for a charged/vis-rich block).
Not placed in the mod — practice only.

## r2 (make_stones_r2.py) — regular stones only (no magic)
Refined shale (thin BROKEN laminae — fixed the brick rhythm), kept marble/slate, added granite/
basalt/sandstone to span the rock classes:
- marble (metamorphic vein) / slate (metamorphic foliation) — kept, both strong.
- shale (sedimentary laminae) — REFINED, now reads as soft layered mudstone not brick.
- granite (igneous plutonic salt-and-pepper, S4 multi-mineral) — STANDOUT, textbook granite.
- basalt (igneous volcanic, dark near-flat + vesicles) — reads dark volcanic (faint green-grey).
- sandstone (sedimentary, warm tan grains + faint bedding) — clean.
All tile cleanly; each rock class shows its structure axis (speckle/bands/veins/foliation/flat).
Practice only, none placed in the mod.

## r3 (stonegen.py + stones.json) — data-driven engine
Refactored: the generator is now a FIXED engine (stonegen.py) driven entirely by values in
stones.json. Tweak stones by editing the JSON, or override any value on the CLI without touching
code, e.g. `--set shale.laminae.density=0.4 --set marble.seed=7`. Structure primitives are
value-parameterised (speckle/foliation/flat + minerals/veins/laminae/bedding/flecks/pits/cleavage).
Reproduces all six stones from r2. Verified: `--set granite.minerals.1.p=0.30` changes the output.

## r4 — rotation-safe marble veins (data-driven)
Added `anchor_veins` to the engine: veins routed between EDGE ANCHORS whose crossing positions are a
symmetric set ({4,11}, a+b=15) IDENTICAL on all four edges, so 90-degree rotations map edge-crossings
onto edge-crossings and the lines line up across seams. Interior wanders (sin*hash, 0 at endpoints so
crossings stay exact) → real placement variety under random rotation, veins never float at an edge.
Verified with `--rotwall marble` (fixed vs random-rotated 5x5 wall). Base is low-contrast noise, which
is rotation-agnostic; only the structured veins needed the crossing alignment. All still value-driven
(crossings/pairs/amp in stones.json); `--rotwall NAME` emits the proof wall for any stone.

## r5 — softer, dotted marble veins
anchor_veins now supports `soft` (light blend tone) + `dot` (fraction of interior steps drawn; rest
are gaps). Marble veins are now mostly a light blend tone close to the base, with sparse darker
accents, broken into dots (dot=0.6) so they read as subtle veining that melts into the stone rather
than a drawn line. Crossings still pinned (mid tone) so rotation alignment holds — dotted veins still
connect at seams. All value-driven in stones.json (soft/color/core/dot).

## r6 — random per-pixel vein darkness
Each vein pixel is now a continuous lerp(soft, core, d) where d = hash**dark_bias — random darkness
per pixel (mostly faint, few dark), instead of a few fixed tones. Kills the uniform-marker read; the
vein fades in and out along its length like real marble. Value-driven: soft/core = light/dark ends,
dark_bias (>1 keeps it mostly light), dot = gaps. Crossings pinned to the mid tone so rotation aligns.

## r7 — curvy veins, less grid
Two fixes for the straight-line/grid look: (1) each vein now curves via a per-vein sum of sin
harmonics (c1·sin πf + c2·sin 2πf + c3·sin 3πf, random amplitudes/signs, all zero at f=0,1 so
endpoints stay pinned) + a small per-pixel jitter — no two veins share a shape, none read straight;
(2) pairs rerouted as a PINWHEEL (each edge → the next edge CW: T0→R1, R0→B1, B0→L1, L0→T1) instead
of the symmetric cross, so the tile no longer stamps a regular X. amp bumped 2.3→2.8 for more bend.
Rotation still aligns (crossings unchanged at 4/11). All value-driven.

## r8 — add random flipping (8-way / D4)
rot_wall now shows fixed | 4-way rotation | 8-way rotation+flip (full dihedral D4: +FLIP_LEFT_RIGHT,
FLIP_TOP_BOTTOM, TRANSPOSE, TRANSVERSE). Safe because the crossing set {4,11} is flip-symmetric
(4<->11), so mirrored tiles still align → veins connect. 8-way reads most varied.
CAVEAT: vanilla Minecraft blockstates do ONLY 90-degree rotation (x/y), NOT mirroring — so real
in-game flipping needs pre-flipped model/texture variants (extra assets) or a mod (CTM/Fusion).
The flip variety here is a studio/preview capability; rotation-only is the vanilla-safe subset.
