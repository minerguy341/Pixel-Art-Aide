# Fantasy wand caps (2026-07-21)

Six caps for the magic-wand-topper vibe (studied from crystal wands, wizard
staff finials, crescent-moon staves): a crystal orb, a faceted quartz point, a
starburst, a crescent moon, a gem in a flared setting, and an ornate beaded
finial. Silhouettes in `src/` (via `gallery/capkit.py`); lift recipes in
`build_fantasy.py`.

| Cap | Lift | Reads as |
|---|---|---|
| A-orb | revolve | crystal-ball finial on a stem |
| B-crystal | hybrid · poly-6 | hexagonal quartz point (prism + pyramid tip) |
| C-starburst | hybrid · radial-6 | six-blade star burst |
| D-moon | hybrid · blade | crescent moon with horn-tip beads |
| E-gem-setting | revolve | a sphere cradled in a flared cup |
| F-beaded | revolve | turned finial, a tapering stack of beads |

Verified headless: each is a single connected 3D piece; iso previews in
`previews/`. Try the poly-6 crystal at the slider's **mid** stop — surface nets
keeps its hexagonal facets crisp while dropping the voxel stairs.

Sources studied (general craft, nothing committed): crystal-wand and wizard-staff
topper listings (orb / crystal-point / crescent-moon / claw-and-orb motifs).
