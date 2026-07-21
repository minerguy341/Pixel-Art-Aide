# 2026-07-21 — planks (greatwood + silverwood), 8 candidates

8 plank arrangements, each palette-parameterised and recoloured per wood (greatwood dark ramp /
silverwood pale ramp, from styles/thaumaturgy.md) — "one arrangement, many palettes". Each shown
tiled 3x3 / full block / slab / stair (added an `iso_slab` renderer in the generator).

Vanilla plank grammar: horizontal boards, no full-height joints, grain in horizontal RUNS of close
tones, broken dark seam rows, staggered board-end joints. Two decorative arrangements included.

## Candidates
1. classic — 4px boards, brick stagger, subtle grain (the safe default)
2. wide — tall 8px boards
3. fine — thin 2px boards
4. running-bond — 4-phase staircase joints (strong brick offset)
5. beveled — lit/shadow board edges (framed / Create-ish panel)
6. rustic — heavy grain + knots (character)
7. basketweave — alternating-grain squares (decorative parquet)
8. diagonal — 45° decorative planks (busiest)

## Eyeball
- Solid standard planks: 1 classic / 4 running-bond / 5 beveled. 2 wide & 3 fine are proportion
  variants. 6 rustic for character. 7 basketweave = clean decorative option. 8 diagonal is the most
  decorative/busy (chevrons where faces meet on the block).
- Silverwood (pale) shows joints/grain more than greatwood (dark exception) — both read as planks and
  tile cleanly. Stair/slab confirm the full-face texture stays value-uniform (no hero motif to shatter).

## Note
Style card already carries greatwood_planks / silverwood_planks palettes; these use those ramps.
`.pxg` sources + PNGs in src/ + out/. Not yet placed in the mod (planks textures already exist there
from the woodsets session — swap in once a candidate is picked).

## r2 (make_planks_r2.py) — 8 MORE, all BOARD STYLE
User picked board style; these stay in the horizontal-board family (no basketweave/diagonal).
Fixed after first pass: grain now runs ALONG the board (horizontal broken streaks, per wood
grammar) instead of vertical; tight-clean's end-joints softened so it reads smooth not gridded.
1. random-width — mixed board heights (natural)
2. shiplap — recessed shadow channel between boards
3. v-groove — tongue-&-groove bevel per board (paneling)
4. tight-clean — smooth wide boards, minimal grain, subtle joints (refined; good for silverwood)
5. pegged — board-end dowel pegs (busiest)
6. wide-grain — tall 8px boards, prominent grain
7. board-and-batten — wide board + raised batten strip (distinct rhythm)
8. weathered — hairline checks along the grain (aged character)
Eyeball leans: 1 random-width / 2 shiplap / 3 v-groove for character; 4 tight-clean for a refined
silverwood; 7 board-and-batten for a distinct siding look.
