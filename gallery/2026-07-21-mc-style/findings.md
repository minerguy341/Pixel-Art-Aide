# MC-style: vanilla-fit loop — findings

**Goal:** make our procedural stone types read as authentically Vanilla Minecraft, tested by a
blind oracle: each round, render the six stones as isometric cubes with neutral numeric labels
(no rock names), then ask a *fresh, memoryless* instance of Claude (no web/search — innate MC sense
only) which single block feels most out of place from vanilla. Fix the flagged stone's values in
`stones.json`, re-render, repeat. Harness: `blind_test.py`; the index→stone key is printed for us,
never drawn.

## The two-stage arc
1. **Cycles 0–3 (earlier):** kill the per-pixel `h2(x,y)` noise base → clustered potato-blobs
   (`cluster`/`mineral_cluster`). Craft foundation.
2. **This loop (rounds 1–8):** blind-judge-driven vanilla tuning. Key realisation surfaced in
   round 1: the UBC-mod study had pushed granite's saturation/contrast UP, which is exactly what
   reads as *mod, not vanilla*. Vanilla stone is a **tight, low-chroma, low-contrast band**.

## Per-round blind verdicts (outlier → fix)
| Round | Flagged outlier | Why (blind judge) | Fix applied |
|---|---|---|---|
| 1 | #4 granite | over-saturated salmon; pure-black noise specks; wide contrast | mute feldspar→brown, kill near-black, drop contrast |
| 2 | #5 basalt | saturated **green** — vanilla has no green stone; uniform dots | neutralise to dark grey; cluster pits + mid-tone bridge |
| 3 | #4 granite | too many hues; rust-orange too saturated; confetti | fewer hues, desaturate, bigger clusters |
| 4 | #2 slate | per-pixel static; oversaturated cool-cyan highlights | reduce foliation per-pixel weight (engine 0.4→0.25); neutralise ramp, calm flecks |
| 5 | #4 granite | dark grains form repeating X/cross motifs; too dark | cluster 3→2, compress value range, desaturate darks |
| 6 | #6 sandstone | too saturated/bright gold | desaturate ramp |
| 7 | #6 sandstone | still too saturated (candy/lemon) | greyed ochre, low chroma |
| 8 | #4 granite | **craft competent** — only a *concept* quibble: "no isotropically-mottled tan stone" | — (see convergence) |

## Convergence call
The judge's language moved from **execution failures** (saturation, pure-black noise, TV-static,
cross-motif artifacts) to, by round 8, "the craft itself is competent — good clustered noise, right
pixel-blob size, no salt-and-pepper." Five of six pass unnoticed every late round. **The style/craft
dimension has converged.**

The one residual flag on granite is *conceptual*, not craft: whether a warm mottled stone belongs in
vanilla. That's a debatable memory claim (vanilla granite *is* a warm mottled stone) and, more
importantly, a **mod-identity design choice** — Thaumaturgy legitimately wants distinct stone types.
Greying granite toward tuff to satisfy a strict blind judge would erase the block's identity. So we
stop here and hand that decision to Jacob rather than thrash it with the oracle.

## What changed in the shipped generator
- Engine: foliation per-pixel term 0.4→0.25 (clusters the grain).
- `stones.json`: granite (muted dusty tan, low-contrast clustered grains), basalt (neutral dark grey,
  green removed, clustered pits), slate (near-neutral dark grey, tight band, calmer flecks),
  sandstone (greyed low-chroma ochre). marble/shale unchanged (already passed).

## Lesson candidate (user-gated — not yet in lessons.md)
> **Vanilla-fit = low chroma + tight value band + clustering, and it's testable blind.** Vanilla
> stone never uses saturated hues (no green/candy-yellow/salmon stone), never puts pure black beside
> a light tone, and holds a narrow contrast band so walls tile calmly. A fresh memoryless instance
> asked "which block is out of place" is a cheap, honest style oracle — iterate until its complaints
> shift from execution to concept. A *mod* reference (UBC) is the wrong target for *vanilla* fit —
> mod stones run hotter/busier on purpose.

## Phase 3 — reference-anchored review (real vanilla as the oracle's anchor)
The memory-only judge's weakness (round 8 flagged granite on a *concept* claim that was arguably a
memory error — vanilla granite really is a warm mottled stone) motivated giving the oracle a real
anchor. Pulled actual vanilla textures into scratchpad (reference-policy: never committed) and built:
- `ref_blind_test.py` — our stones beside an authentic vanilla wall.
- `scene_ref.py` — a world **cross-section** (grass→dirt→stone strata w/ igneous blobs+ores→deepslate,
  desert sand→sandstone), our stones woven in as veins, vanilla sandstone beside ours for direct compare.

**Reframed the ask** (user's idea): don't tell the fresh instance the blocks aren't vanilla — ask it
*how to make them fit*. This flipped the output from an adversarial rotating-outlier hunt into concrete
per-block craft direction. Applied, with a new engine feature:
- Engine: `apply_columns` (vertical striations) for basalt's columnar-jointing signature.
- basalt: near-black → medium warm-grey + vertical columns (distinct from deepslate).
- granite: re-warmed to vanilla's pink-brown, `mineral_cluster:0` to kill a diagonal grain artifact
  (the one defect two independent reviewers agreed on).
- marble: capped highlights (no pure white 255→~236) + more visible veins.
- shale: warmer, finer laminae, lifted darkest value (distinct from slate, not a silhouette).
- sandstone: strong horizontal bedding to match vanilla sandstone beside it.

**Convergence signal:** by the final review, independent fresh instances gave *contradictory* notes
(granite too-pink ↔ too-brown; sandstone bedding too-strong ↔ too-faint). Cross-reviewer contradiction
on the remaining nits = the taste/variance floor, i.e. converged. The only cross-reviewer-consistent
defect (granite's directional grain) was fixed; the rest is preference.

## Not verified
In-game read at real scale/lighting/tiling across a wall — flat upscaled previews only. Every reviewer
flagged this as the real remaining unknown. Jacob's eye.
