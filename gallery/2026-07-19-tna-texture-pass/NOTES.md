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
