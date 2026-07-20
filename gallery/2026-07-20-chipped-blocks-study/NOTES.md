# Chipped study — decorative BLOCKS (2026-07-20)

Follow-up to the 2026-07-19 workbench/model study. Studied terrarium-earth/Chipped
(branch 1.21.x) decorative *blocks* in the session scratchpad per
reference-policy.md — general craft only, **no Chipped textures committed**. Only
derived aggregate metrics (counts, palette breadth, busyness, transparency,
luminance) are recorded here and charted. CTM loading intentionally not studied —
Fusion is the studio's preferred CTM path.

Sampled bases (folder totals in parens): cobblestone (66), bookshelf (33),
glass (21), glowstone (20), brown_terracotta (17). 6–16 variants sampled per base
and run through `aide.analyze`.

## The blocks vs the workbenches — the headline contrast

The workbenches were HD **64×64 multi-element models**. The decorative blocks are
the opposite: almost all **16×16, vanilla resolution, palette-mode PNGs** (one
32×32 outlier, `massive_cobblestone_bricks`). Chipped spends geometry/resolution on
*furniture*, and spends nothing but *arrangement* on *building blocks*. Two
different products under one mod.

## Similarities (what every base shares)

1. **Scale-by-variant.** The whole mod is "one vanilla block → dozens of decorative
   cuts, chosen in a chiseling GUI." cobblestone alone ships 66. (variant-scale.png)
2. **Palette fidelity to the source block.** Variants inherit the base block's
   palette and value range; the redesign is *structural*, not chromatic. A base
   reads as one coherent material even across 66 cuts. (palette-cohesion.png:
   cobblestone locked at 6–8 colours.)
3. **A shared pattern vocabulary,** reused across every material: `*_bricks`,
   `*_tiles`, `*_pillar`/`_column`, `chiseled_*`, `smooth_/polished_*`,
   `carved_/engraved_/inscribed_*`, plus playful carvings (the cobblestone face set:
   angry/sad/glad/unamused/duh + creeper/spider/runic). The same nouns recur folder
   to folder — a house style, not per-block improvisation.

## Differences — a different design *lever* per material class (design-levers.png)

- **cobblestone / stone** → **structure only.** Locked ~7-colour palette, busyness
  7–14; all the variation is layout (bricks, tiles, pillars, carvings, faces).
- **terracotta** → **subtle relief on a noisy coloured ground.** 35–47 near-colours
  (the mottled vanilla base) but near-flat busyness 2–3.5 — gentle patterns pressed
  into an already-busy surface. Recolours 1:1 across all 16 dye folders.
- **glass** → **the alpha is the design.** ~10 colours but transparency 6–54%:
  leaded muntins / oak frames over clear panes. Highest busyness of the set. The
  only class where the pattern is made of *holes*.
- **glowstone** → **luminance is the lever.** Brightest class (L mean up to 86) and
  the widest palette spread (11–147): splits into smooth photo-gradient glow
  (smooth 89, shimmering 147 colours) vs structured lantern framing.
- **bookshelf** → **object arrangement.** Books/webs/glow rearranged; 12–32 colours,
  moderate busyness; `oak_webbed` drops to 12 colours (sparse cobweb).

## In-world / in-game usage

Chosen via Chipped's chiseling bench (a GUI grid of cuts). Fixed-palette stone/
terracotta variants tile seamlessly and swap freely — pure build-detailing that
never clashes because the palette never moves. Pillars/columns read as structural
framing; leaded-glass variants are windows; glowstone lanterns are light fixtures;
the face carvings are accents/easter-eggs. The point is *granular palette-safe
detail*: a builder reaches for a different cut without introducing a new colour.

## My favourite

**`runic_carved_cobblestone`.** It's the thesis of the mod in one 16×16, 7-colour
tile: zero palette drift from vanilla cobblestone, all the character carried by an
engraved rune motif. It's the most restrained kind of decoration — reads as "old,
purposeful stone" — and it's the one variant that would drop straight into
Thaumaturgy's arcane stonework without any recolour. Runner-up: the leaded-glass
window family, for using alpha as the whole design.

## Candidate lessons (pending user approval)

1. A decorative block family = **one fixed source palette, variation carried by
   structure** (brick/tile/pillar/carve), not by new colours — so any two variants
   sit together without clashing. (The opposite discipline from a hero texture.)
2. **Match the design lever to the material:** opaque stone → rearrange structure on
   a locked palette; coloured ceramic → subtle relief on a noisy ground; glass →
   pattern *in the alpha*; emissive → push luminance. One vocabulary, different lever.
3. Keep decorative building blocks at **base resolution (16)**; reserve HD + models
   for *furniture/hero* pieces. Resolution is a budget spent where the eye lingers.
