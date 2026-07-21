# 2026-07-21 — logs & leaves retry (greatwood + silverwood)

Retry of the wood-type textures, **logs + leaves only** (planks/doors/tables were the
2026-07-20-woodsets session). Style: `thaumaturgy`. 16x16, tiling blocks.

## Subjects & candidates
- **Greatwood log** (bark side + shared end-grain top): A straight / B gnarled / C plated
- **Silverwood log** (bark side + shared end-grain top): A smooth / B lenticel / C shimmer
- **Greatwood leaves**: A broadleaf 33% / B dense 22% / C accent 32%+fleck
- **Silverwood leaves**: A airy 33% / B canopy 18% / C glow 30%

## Design grounds (knowledge base)
- Wood grain = vertical RUNS (3px+), one darker furrow per ridge; no 1-2px flecks (brick/dirt).
- Leaves = ~30-40% scattered tiling holes, no 2x2 fully-transparent block, lit/shadow clumps
  + deep-edge rim for the lacy read. Dense magic canopy may drop toward ~18% (BWG).
- Greatwood = warm, ancient, matte, NO teal. Value ~10-32% (greatwood is the sanctioned
  dark exception to the 25-80% mid-value rule; bark rides the same lane as its planks).
- Silverwood = pale grove exception (L ~55-92%), carries the teal shimmer #7FE8D8 as SPARSE
  1-2px accents — the magic tell. End grain has a faint teal heart.

## Presentation (per request)
- Leaves: 3x3 tile + iso block render.
- Logs: 2-wide x 3-tall tile + 3-block-tall trunk render (stack_iso composites 3 iso cubes,
  bottom-first, so only the top cube's end grain shows).

## Self-critique (eyeballed)
- Greatwood: **straight** reads cleanest (calm smooth-bark log, a touch paneled); **plated**
  is the character option but its horizontal cracks tile a little brick-regular; **gnarled**
  is the busiest/noisiest — knot-notches read as a repeat. Leaning straight or plated.
- Silverwood: **smooth** is elegant with the most visible shimmer; **lenticel** reads most
  authentically "birch" (horizontal eye-dashes); **shimmer** adds a faint teal seam = most magic.
- Leaves both woods tile seamlessly (3x3 clean, no landmark). Value clumping is a bit subtle —
  could push lit/shadow separation harder if the user wants more depth.

## Metrics
- Greatwood logs L9.9-32.5% (dark exception, intended). Silverwood logs L55-92% (grove
  exception). Teal ≤2.3% of pixels. Leaf holes 33/22/32 (gw), 33/18/30 (sw). Seams: all
  ratio ≤1.54, plated/silverwood ~1.0 (invisible); eyeballed clean in the 3x3 / 2x3 tiles.

## Open (for user)
Pick a direction per subject (or ask for changes). The teal-heart end grain is shared across
silverwood candidates; greatwood top is shared rings. Not yet placed into the mod assets tree.

## r2 (make_r2.py) — more logs, cores, silverwood leaves
Greatwood leaves DECIDED: C accent + random rotation. r2 adds:
- **Greatwood bark**: D fibrous / E chunky / F cracked. Eyeball: E chunky is the standout
  (deep furrows, rounded-ridge depth); D fibrous a nice organic option; F cracked reads a
  bit brick/masonry (blocky offset plates) — polarizing.
- **Silverwood bark**: D runed / E polished / F veined. E polished = elegant refined silver;
  F veined = clear teal shimmer veins (most magical); D runed is busier/noisier.
- **Greatwood cores**: 1 rings / 2 star (radial checking cracks) / 3 burl (eccentric). All read.
- **Silverwood cores**: 1 heart (restrained) / 2 radiant (teal glow, bold) / 3 runic (star sigil).
- **Silverwood leaves r2**: D clump (more lit/shadow depth — fixes r1's subtle clumping) /
  E blossom (teal 2px glowing buds) / F frost (icy highlights, airier 35%). Shown fixed|random.

### Accent-level flags (teal % of opaque pixels; card guidance is ≤~3% for normal materials)
- silverwood_log_veined **7%**, silverwood_core_radiant **14%**, silverwood_leaves_blossom **7%**
  — deliberately over the card's teal rule (magical variants). Can dial back on request.
- Cores are end-grain (top face only), so a bolder teal there is less of a whole-block field.

## r3 (make_r3.py) — bark + cores redone (study-driven)
Study: study-wood-r3.md. Both leaves DECIDED (gw r1 accent+rot, sw r2 frost+rot).
- **Edge fix**: a furrow/groove now STRADDLES the x=0/15 wrap and edge columns carry interior
  variation → parallel logs MERGE (no framing band). Verified in the 2x3 (parallel-logs) tiles.
- **Greatwood bark**: A furrowed / B shaggy / C aged — deep IRREGULAR wandering furrows (8-row
  gentle wander, low mottle after a cleanup pass; the first 4-row wander read staggered/noisy).
- **Silverwood bark**: pristine & serene, brighter/cooler ramp — A serene (smooth + soft grooves
  + whisper teal) / B birch (horizontal lenticels, merges perfectly, no vertical bands) / C moonlit
  (soft cylindrical sheen, ethereal). Teal a whisper only (~1-2%), per the magic-wood study.
- **Greatwood cores**: 1 rings / 2 heart (dark heartwood→sapwood gradient) / 3 burl.
- **Silverwood cores**: 1 heart (single teal whisper) / 2 halo (one soft teal ring) / 3 pale (no teal).
Eyeball leans: gw bark A furrowed; sw bark A serene or B birch; cores gw 2 heart, sw 1 heart / 3 pale.

## r4 (make_r4.py) — more logs + silverwood grain with/without teal heart
Approved tree-growth lessons landed in knowledge/lessons.md this session.
- **Greatwood bark**: G deep-fissured (clean deep wide fissures — standout) / H interlaced
  (diagonal interlocked grain — distinctive, polarizing) / I knotted (branch-scar knot, but the
  single knot tiles into a regular grid → reads repetitive). All keep the r3 edge-flow fix.
- **Silverwood grain (teal-free bark)**: A silk (ultra-pristine near-flat) / B woven (gentle wavy
  interlocked) / C dappled (soft canopy-light dapples) — each shown as a trunk WITH the teal-heart
  core and WITHOUT (plain), + the two cores compared. Bark carries no teal so the heart is the only
  variable; per the study the teal heart is CANON, offered both ways per user request.
Eyeball leans: gw G deep-fissured; sw B woven or A silk; heart = with (canon) unless a plain
non-magical grain is wanted.

## r5 (make_r5.py) — 6 more silverwood grain candidates
Greatwood bark DECIDED: G deep-fissured. 6 new silverwood grains, all pristine/serene, pale,
teal-free bark, edges flow (trunks topped with canon teal-heart core to show intended look):
- D flowing — long soft meandering flow-lines (silk); pristine. STRONG.
- E marbled — soft wandering pale veins; elegant marble. STRONG.
- F frosted — cool sheen + white sparkle specks (icy); on-theme for cold magic. STRONG.
- G damask — faint woven diamond lattice; refined but reads decorative/fabric, least wood-like. POLARIZING.
- H satin — soft vertical sheen ribbons; luminous, pristine. STRONG.
- I ghost-ring — faint HORIZONTAL growth banding; merges perfectly but reads bamboo-ish. POLARIZING.
Eyeball leans: D flowing / E marbled / H satin for a refined trunk; F frosted for the icy-magic angle.
