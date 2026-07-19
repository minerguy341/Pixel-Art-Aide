# T.N.A. texturing campaign — backlog

Standing task (user, 2026-07-19): texture everything in Thaumaturgy: The New
Age; custom sizes allowed for wand/stave models; judge against original
Thaumcraft's idiom (from knowledge — TC assets are never fetched or reused,
per T.N.A. PLAN §1.4); push textures + art-direction changes to the T.N.A.
repo, branch `claude/texture-generation-prompts-qyp1w7`.

Statuses: [ ] todo · [~] in progress · [x] shipped to T.N.A. · [d] deferred

## Registered content (highest priority — replaces placeholders)

- [x] greatwood planks — approved 2026-07-19 session (r3_deeper), ship as `block/greatwood_planks`
- [x] arcane orrery block: `block/arcane_orrery_{top,side,bottom}` + model JSON cube_bottom_top (iter 1)
- [x] wand_base grayscale replacement — UV remap done (wand/stave/cap_base now use disjoint rod strip cols 0-1 + cap patch cols 4-7): rod (cols 0-2 × rows 0-16) and caps (cols 0-3 × rows 0-2) overlap in the current model JSONs; remap wand.json/stave.json/wand_rod_base.json/wand_cap_base.json to disjoint regions, then author grayscale regions for tint (rod=0, cap_a=1, cap_b=2). Optionally 32x with texture_size bump.
- [x] aetherlens (`item/aetherlens`, replaces spyglass)
- [x] codex (`item/codex`, replaces enchanted_book)
- [ ] research papers ×5, tier-graded (`item/research_paper_{fledgling,apprentice,scholar,master,grandmaster}`)
- [ ] aura_node block — real art exists but is placeholder-grade; revisit vs TC node look (glassy orb)

## Planned content (art-direction materials)

- [ ] greatwood log side/top, leaves, sapling
- [ ] silverwood planks, log side/top, leaves, sapling (glow accent 7FE8D8)
- [ ] brass ingot/nugget + brass block
- [ ] aetherium ingot/nugget + aetherium block
- [ ] gilded planks ×4 (greatwood+brass, silverwood+aetherium, cross pairs)
- [ ] arcane worktable faces
- [d] M3 foci ×3 (wait for item design)
- [d] M4 essentia set (crucible, alembic, tubes, jars, furnace…) — wait for M4
- [d] taint set — wait for design
- [d] aspect icons (41, HD 512px hexagon masters) — separate GUI-art workflow, not 16x pipeline

## TC-comparison ground rules

Judgment criteria per texture: does it evoke the TC original's *role* (dark
arcane wood, purple metal, brassy instruments) while staying inside T.N.A.'s
vanilla+Create detail ceiling? Recorded per texture in NOTES.md. No TC files
are downloaded, diffed, or committed.
