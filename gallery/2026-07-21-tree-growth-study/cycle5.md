# Cycle 5 — Synthesis: seasonal form + translating growth behaviour into blocky/voxel trees

Scope: deciduous vs evergreen (leaf type ↔ crown shape ↔ climate), and how to turn cycles 1–4 into
actual blocky tree construction. Closes the loop and produces the unified spec.

## Findings
- **Leaf type, crown shape and climate are ONE decision.** Deciduous = broad thin leaves, seasonal
  drop (abscission conserves water in cold/short days), **broad spreading crown**, branches
  concentrated in the crown. Evergreen = needles/scales (low surface:volume, waxy — water-thrifty),
  **conical / inverted-cone** (wider at base), on cold/dry/poor sites. Broadleaf→round; needle→cone.
- **Deciduous form must have believable BRANCHES — they show bare half the year;** evergreen hides
  its structure inside a filled cone, so its interior can be simpler.
- **Voxel trunk:canopy ≈ golden ratio.** Minecraft's big-oak `heightAttenuation` = trunkHeight :
  heightLimit ≈ **1/φ ≈ 0.618** — trunk ~0.6 of total height, canopy ~0.4. A natural proportion.
- **Build the WOOD FRAME first, hang leaves on branches.** Trunk + asymmetric branches (never
  identical or at the same height — one lower/smaller), canopy **offset** off-centre; then leaves ON
  the branches, not a clump floating on a bare pole. Canopy steps **inward as it rises** (dome/pyramid),
  spreading more up than down.

## Growth→shape lessons
1. **Pick leaf type + crown silhouette + climate together** — a broadleaf on a conical frame (or
   needles on a round spreading crown) reads wrong.
2. **Give a deciduous tree a real branch frame** (visible in winter); an evergreen can be a denser
   filled cone. Match interior complexity to whether the structure is exposed.
3. **Proportion a big blocky tree ~0.6 trunk : 0.4 canopy** (golden-ratio), canopy offset off-centre,
   branches at varied heights/sizes — not a symmetric lollipop.
4. **Frame-then-foliage**: place trunk + branches, then hang leaf clusters on the branch tips with the
   ~30–40 % transparent holes from the leaf lessons — never a solid crown on a bare stick.
5. **Uneven, asymmetric, offset** at every level (branch heights, canopy centre, stand ages) is what
   separates "grown" from "stamped."

## UNIFIED SPEC — greatwood vs silverwood (from all 5 cycles)
| Axis | **Greatwood** (warm, common giant) | **Silverwood** (cool, rare special) |
|---|---|---|
| Trunk footprint | **2×2**, straight, mammoth | **3×3 plus** tapering to 1 (TC canon) |
| Height / proportion | tall old-growth, ~0.6 trunk : 0.4 canopy | tall, slender taper |
| Canopy | broad, radiating branches + thick leaf clusters | pale, sparkling blue/teal, airy |
| Core / heartwood | warm heartwood→sapwood rings | **holds a node — luminous teal heart** (canon) |
| Roots | visible flare/buttress (thick trunk ⇒ wide roots) | subtler, pristine |
| Leaves | deep forest green, ~32 % holes (accent fleck) | icy/frost, teal shimmer, ~30 % holes |
| Spacing / worldgen | common (~4 %/chunk), old-growth giants among smaller | **rare, spaced grove-seeder** (makes its own biome) |
| Form driver | open-grown giant: thick trunk, low wide branches | rare magical anchor: pale, node-hearted |

## Sources (study only)
- Price Right Trees — evergreen vs deciduous: https://pricerighttrees.com/evergreen-vs-deciduous-trees-differences-garden/
- Minecraft big-oak growth algorithm (golden-ratio heightAttenuation): https://gist.github.com/Earthcomputer/41addf80c12d001dfa4391c3a0d03be8
- Bedrock `minecraft:tree_feature` reference: https://learn.microsoft.com/en-us/minecraft/creator/reference/content/featuresreference/examples/features/minecrafttree_feature
- DiamondLobby — building believable custom trees: https://diamondlobby.com/minecraft/how-to-build-custom-tree-in-minecraft/
