# Campaign session: T.N.A. texture pass (standing /loop task)

See BACKLOG.md for the work list. This file logs per-iteration decisions and
TC-idiom comparisons (judged from knowledge — no TC assets fetched/used).

## Iteration 1 — 2026-07-19

Shipped to T.N.A. (`claude/texture-generation-prompts-qyp1w7`):

- `docs/art-direction.md` sync: greatwood plank ramp darkened to the
  approved TC-era values, recorded as a sanctioned mid-value exception.
- `block/greatwood_planks.png` — the approved r3_deeper from the
  greatwood-planks session (block not registered yet; asset staged).
- `block/arcane_orrery_{top,side,bottom}.png` + model swap `cube_all`
  (lodestone placeholder) → `cube_bottom_top`.

Orrery design decisions: dark greatwood casing; brass inlay band + corner
plates (Create-style framed faces); inset aetherium viewport / hub with
single teal glint. Analyzer: value warnings are the greatwood exception +
brass accents; bottom face pillow_r=0.47 is a false positive from the framed
composition (frame dark, field lighter — structural, not shading).

**TC comparison:** TC never had an orrery; the nearest reference is TC's
greatwood-and-gold arcane furniture. Verdict: our darker wood + brass +
aetherium version fits both the TC memory and the Create-adjacent direction;
chose it over a stone-based alternative (not drawn — wood casing better
matches the registered worktable/wand woodiness).

**Not verified in-game** (no build possible in this sandbox; model JSON is
schema-valid and uses only vanilla parents). Human smoke test: place the
orrery — faces should show brass ring top / banded side; check the hologram
still renders above the top face; greatwood_planks.png is staged for when
the block registers.

Next iteration: wand/stave UV remap + real grayscale wand_base (tint
regions rod=0 cap_a=1 cap_b=2), then codex + aetherlens + research papers.

## Iteration 2 — 2026-07-19

Shipped to T.N.A.:

- `item/wand_base.png` — real grayscale tint template: rod strip (cols 0-1,
  lit edge + carved rings) and cap patch (cols 4-7, metal steps), disjoint.
  Remapped cap UVs in wand.json (12 faces), stave.json (12), and
  wand_cap_base.json (6) to the new patch; rod UVs unchanged. Tint
  simulation preview (`previews/wand_base-tints.png`) verified all four
  material colors read correctly under multiply-tint.
- `item/codex.png` + model repoint — aetherium-purple tome, brass clasp
  (r2 simplified the beaded strap to a solid band + buckle), teal sigil,
  page block right. TC verdict: same role as the Thaumonomicon (purple book,
  metal furniture) without copying its trim; chose closed-tome-with-strap
  over an open-book design that would collide with vanilla book sprites.
- `item/aetherlens.png` + model repoint — diagonal brass lens instrument
  with aetherium glass, teal glint, greatwood grip. TC verdict: evokes the
  thaumometer's brass+purple instrument reading; diagonal silhouette chosen
  over a symmetric monocle, which reads as a ring at 16x.

Analyzer notes: item sprites legitimately exceed the block albedo band
(borders/speculars); aetherlens busyness 17.6 is diagonal-edge inflation,
silhouette clean in preview. All JSON models re-validated after edits.

Not verified in-game. Human smoke test: wand + stave in hand (rod shows
wood rings, caps shade correctly, tints per material); codex/aetherlens in
inventory + item frame; standalone cap item no longer shows a smeared
corner region.

Next: research papers x5 (tier-graded seals), then greatwood log/leaves +
silverwood set.

## Iteration 3 — 2026-07-19

Shipped to T.N.A.: `item/research_paper_{fledgling,apprentice,scholar,
master,grandmaster}.png` + 5 model repoints. Composed programmatically
(`src/make_research_papers.py`) from one base sheet with a tier grammar:
writing lines accumulate with tier; seal steps none -> brass -> brass+ribbon
-> aetherium -> aetherium+glint with gilt corners.

r1 -> r2: uniform dark frame read as a framed tile, seal diamond read as a
cross — lit top/left edges now paper-toned (border-shade bottom/right only)
and the seal is a rounded 3x3 wax blob, lit top-left.

TC verdict: TC research used scroll/note items with distinct tiers only in
GUI; ours grade the item itself, which reads better in inventories. Kept
paper white-cream (forma) rather than TC parchment-brown so the seals carry
the tier color story.

Not verified in-game. Human smoke test: all five papers side by side in an
inventory row — tiers should be tellable apart at a glance.

Next: greatwood log side/top + leaves, then the silverwood set.

## Iteration 4 — 2026-07-19

Shipped to T.N.A. (staged, blocks unregistered): `block/greatwood_log.png`,
`block/greatwood_log_top.png`, `block/greatwood_leaves.png`,
`block/silverwood_planks.png`.

- Log side: card bark colors + one in-lane ridge highlight; wobbling furrow
  columns, two knots; tiles vertically with zero seam contrast. Bark ramp
  straight-slide flag accepted: both bark steps are card-fixed.
- Log top: bark rim + concentric rings in the dark plank ramp. r1 -> r2:
  ring breaks clustered into a G-shaped glyph that repeated loudly in 3x3 —
  solidified the inner ring, symmetrized the heart.
- Leaves: clump-shaded deep green, colored directly (no biome tint), ~5%
  holes; seam ratio 1.0. TC verdict: TC greatwood canopies were near-black
  green; ours keeps the deep-green read at vanilla-legal values.
- Silverwood planks: same staggered composition as approved greatwood
  (family consistency). r1 -> r2: hard dark seam read as brick mortar on
  pale wood — seam lifted to soft teal-gray 8A948E.

Human smoke test (when blocks register): log pillar x3 — bark should not
band; log top ring should not read as a glyph when 4 tops adjoin; leaves
cube vs vanilla oak — density should feel vanilla-adjacent.

Next: silverwood log/leaves/saplings + both saplings, then metals
(ingots/nuggets/blocks), then gilded planks, aura_node revisit.

## Iteration 5 — 2026-07-19 (user feedback round)

User direction: papers should read like vanilla (not a flat sheet); add
rolled "finished paper" scrolls with tier-indicating wax seals; greatwood
log needs improving, mainly the core.

Shipped to T.N.A.:

- `item/research_paper_*.png` x5 REDONE — tilted sheet with folded corner
  (vanilla paper idiom), stepped ink lines following the tilt, wax seal on
  the high edge. Seal palette unified across families and made 5-distinct:
  fledgling wax-red -> apprentice brass -> scholar blue -> master aetherium
  -> grandmaster gold + teal glint. (r3 used gray for fledgling — invisible
  against the border shade; switched to classic sealing-wax red-brown.)
- `item/research_scroll_*.png` x5 NEW, STAGED — vertical rolled scroll,
  end curls, ribbon band in the seal's lowlight color, centered wax seal.
  No such items are registered yet: models/registrations are Jacob's call
  (suggested id `research_scroll_<tier>` / "finished research").
  TC verdict: TC's iconic research notes were exactly a ribboned scroll —
  this is the homage slot, done in our seal-color language.
- `block/greatwood_log.png` r2 — horizontal plate breaks, proper knot
  (dark ring, ridge-highlight eye) that diverts the adjacent furrow.
- `block/greatwood_log_top.png` r3 — end grain rebuilt: sap ring, two
  inner growth rings tightening toward center, chamfered corners so rings
  don't read as squares, dense checkered heart.

Human smoke test: papers+scrolls in one inventory row (5 seal colors
distinct, sheets read as paper not cards); log pillar + top faces.
