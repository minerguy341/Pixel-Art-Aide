# Cycle 1 — Real-life tree architecture: how trunk, canopy, branches, roots & spacing co-vary

Scope: temperate hardwoods (oak, ash, sycamore, beech, birch) — the allometry that ties a
tree's parts together, and how **spacing** (open-grown vs forest-grown) changes its whole shape.

## Findings
- **Allometry is a linked system.** Trunk diameter, height, crown height and crown radius scale
  together; canopy width is ~**linear with height** (natural selection for light interception).
- **Height is spacing-INSENSITIVE; crown width & trunk girth are spacing-SENSITIVE.** Height growth
  is stable from solitary to dense stands, but crown size and stem diameter are *very* sensitive to
  competition. → spacing changes girth + spread, not so much height.
- **Open-grown vs forest-grown is the master variable.** At equal trunk diameter, open-grown trees
  have much **larger crowns**. Solitary/open = short bole, **wide low spreading crown**, thick
  **tapering** trunk, branches low to the ground. Forest/dense = **tall straight** trunk, **small
  crown high up**, **self-pruned** (bare lower trunk — lower branches die from shade), slender stem.
- **Roots track the crown and the trunk.** Root spread ≈ **2–4× the crown diameter**, and most root
  length is **beyond the dripline**; root radius : trunk diameter ≈ **38 : 1** — a fat trunk implies
  a wide root flare/buttress.
- **Shade tolerance shifts the ratio:** shade-tolerant species carry relatively **larger crowns at
  small stem diameters**.

## Growth→shape lessons (for depicting/worldgen-ing a tree)
1. **To show "grew crowded" vs "grew alone," vary CROWN WIDTH + TRUNK GIRTH + branch height — NOT
   overall height.** A dense-forest tree = tall, 1-wide straight trunk, small canopy near the top,
   no low branches. A field/solitary tree = shorter bole, 2×2 tapering trunk, broad low canopy,
   branches starting low.
2. **Canopy radius ∝ height (for a given openness).** A taller tree of the same species reads as a
   proportionally wider canopy — don't draw a tall trunk with a tiny hat unless it's forest-dense.
3. **A thick trunk demands a root flare.** Big-girth trees (solitary oaks, ancients) get visible
   buttress/root spread ~2–4× the crown; a fat trunk with no flare reads wrong.
4. **Self-pruning encodes density:** a bare lower trunk = grew in shade/competition; branches all
   the way down = grew in the open. Bark on the bare bole is what shows most in a dense forest.
5. **Spacing rule of thumb:** open-crown species need growing space ~ their crown diameter; so
   wide-canopy trees naturally stand **spaced apart**, narrow-crown forest species pack **close**.

## Sources (study only)
- Nature *Scientific Data* — allometry & growth of UK woodland taxa: https://www.nature.com/articles/sdata20156
- ScienceDirect — crown size & growing-space requirement (urban/park/forest): https://www.sciencedirect.com/science/article/pii/S1618866715000473
- Open-grown ash/sycamore crown allometry (Academia PDF)
- ISA Arboriculture — *Predicting Root Spread from Trunk Diameter & Branch Spread*: https://auf.isa-arbor.com/content/14/4/85
- DeepRoot — how wide tree roots spread: https://www.deeproot.com/blog/blog-entries/how-wide-do-tree-roots-spread/
- Wikipedia — tree crown measurement: https://en.wikipedia.org/wiki/Tree_crown_measurement
