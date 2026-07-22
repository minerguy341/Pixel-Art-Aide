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
