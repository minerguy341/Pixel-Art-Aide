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
