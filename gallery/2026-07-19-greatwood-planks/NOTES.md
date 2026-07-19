# Session: greatwood planks (demo / toolkit proof)

- **Prompt**: greatwood planks, 16x16 tiling block — first real run of the
  pixel-artist workflow.
- **Style**: `styles/thaumaturgy.md`, `greatwood_planks` ramp (5E4530 /
  7A5B3C / 8F6E4B) + one added deep seam step in the greatwood hue lane.
- **Plan**: three deliberately different compositions — A staggered
  horizontal planks with grain, B vertical planks with end-joints, C calm
  wide boards (most vanilla-adjacent).

## Round 1 (self-critique, not shown to user)

Analyzer: ramp flagged as straight value slide in all three; seam ratios
1.57–1.93; A/C max flat run 16 (the seam rows — intentional).

Eyeball: A's 2px grain clusters read as dirt blobs, composition leaned
brick; B ladder-regular (every plank identically lit); C's full-width
highlight rows banded hard in the 3x3 tile preview.

## Round 2 (presented)

- Deep seam step cool-shifted `4A3625` → `4A312C`: the card's core steps are
  fixed, so the added step carries the hue shift — ramp now reads 21°
  cool-ward in shadow.
- A: grain lengthened to 3px runs, highlight rows broken with base.
- B: de-laddered — several plank left-edges drop highlight to base.
- C: highlights broken into segments, grain grouped, one 2px knot (band 3).

Analyzer r2: value 21–45% (dark wood, inside house band), busyness 6.2–7.0,
seam ratios 1.48–1.79 — elevated because the wrap edge *is* a plank seam,
identical to interior seams; 3x3 previews confirm no visible wrap artifact.

Sheet: `previews/candidates-r2.png`.

## Status

Awaiting user pick / feedback (r3 on request).

## Lesson candidates (proposed, NOT yet approved)

1. At 16x, 2px grain clusters read as dirt; wood grain needs 3px+ runs.
2. Banded textures legitimately score seam_ratio ~1.4–1.9 when the wrap edge
   is a real seam — treat as false alarm once the 3x3 preview is clean.
3. When a style card fixes a ramp's core steps, put the hue shift in the
   added extension steps.
