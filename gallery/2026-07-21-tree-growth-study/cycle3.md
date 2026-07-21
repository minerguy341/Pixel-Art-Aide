# Cycle 3 — How Minecraft mods model tree growth, shape & spacing

Scope: Dynamic Trees, TerraFirmaCraft, Biomes O' Plenty / OTBWG, and vanilla worldgen structure —
how mods turn the real-world growth rules (cycles 1–2) into actual block generation.

## Findings
- **Dynamic Trees reproduces real competition directly.** Trees are a live multi-block structure
  (rooty soil + branch network + leaves) grown by a **cellular-automata** (leaves) + **branch-network**
  (trunk/branches) algorithm, **per species**. Crucially: *"Trees compete for sunlight when placed near
  each other and grow taller and skinnier than trees in the open"* → an emergent forest canopy; the
  canopy blocks skylight (dark forests, saplings fail beneath). This is cycles 1–2's open-vs-forest
  rule as running code.
- **Mature size is CLIMATE-driven, not a per-species constant.** DT growth rate + mature size depend
  on **biome, temperature, rainfall**; TFC decides tree type purely by **climate**, not biome id.
  Warm+wet → bigger/lusher; cold+dry → stunted.
- **Trunk thickness is a first-class lever.** DT exposes **trunk thickness** (+ growth shape) as a
  tunable; vanilla encodes "big tree" as a **2×2 trunk** (mega spruce, large jungle, dark oak) vs the
  default 1×1. Thick trunk ⇒ big canopy ⇒ (per allometry) wide spacing.
- **Density/spacing is a worldgen knob + uneven ages.** TFC uses a `tree_count` provider for forest
  density and spawns occasional **old-growth** giants among normal trees; vanilla scatters trees by a
  per-biome frequency. Real stands are uneven-aged — a few giants among many smaller.
- **Form comes from a growth RULE, not a stamped schematic.** DT branches are a network (thin branches
  climbable, thick ones slow to fell); believable trees emerge from an algorithm, where vanilla stamps
  a handful of fixed templates + variants.

## Growth→shape lessons
1. **The open-vs-forest rule is implementable and expected** — if trees can be dense, forest ones
   should read taller/skinnier with high canopies, open ones shorter/wider with low branches. Even a
   *static* set benefits from shipping a "forest form" and an "open form," not one silhouette.
2. **Scale mature size to CLIMATE.** A mod tree's size/lushness should track temperature + rainfall of
   where it grows — a cold-biome variant is stunted, a warm-wet one large. Don't hardcode one size.
3. **Trunk width is the primary "this is a big/old tree" signal** — reach for a 2×2 (or thicker) trunk
   for giants/old-growth, and pair it with a proportionally wider canopy + visible root flare.
4. **Populate forests with uneven ages**: mostly normal trees + occasional old-growth giants, not a
   uniform grid of identical trees. Spacing/density is a deliberate worldgen parameter.
5. **Prefer a growth grammar over a single schematic** for variety: even without Dynamic Trees, author
   2–3 size/age stages (sapling → young → mature/old-growth) so a stand looks grown, not stamped.

## Implication for T.N.A. (greatwood/silverwood)
- **Greatwood = ancient/large**: thick (2×2) trunk, wide canopy, visible roots, spawns as occasional
  **old-growth giants** among smaller trees — the "grew big & alone" form from cycle 1.
- **Silverwood = rare, pristine grove**: spaced special trees (luminous), low density — matches its
  "special-grove payoff" identity rather than a common packed forest.

## Sources (study only)
- Dynamic Trees — CurseForge: https://www.curseforge.com/minecraft/mc-mods/dynamictrees ; Modrinth: https://modrinth.com/mod/dynamictrees
- TerraFirmaCraft — Trees & Forests worldgen: https://terrafirmacraft.github.io/Documentation/1.20.x/worldgen/features/trees/
- TerraFirmaCraft Wiki — Trees: https://1710-wiki.terrafirmacraft.com/Trees
