# Lessons log

Append-only. Every entry was **approved by the user** before landing — the
skill proposes candidate lessons at the end of a session and commits only the
approved ones (see the pixel-artist skill, "Learning" section).

Future sessions: read this whole file before authoring. When a lesson has
graduated into `knowledge/shading.md` or a style card, its entry stays here
with a `[folded into …]` marker so the history remains.

Entry format:

    ## YYYY-MM-DD — short title
    - Context: what was being made, which style
    - Observation: what went wrong / what worked unusually well
    - Rule: the reusable takeaway, stated as an instruction

---

## 2026-07-19 — grain reads as dirt below 3px
- Context: greatwood planks (thaumaturgy style), 16x16, session r1
- Observation: 2px shadow clusters scattered as "grain" read as dirt blobs
  and pushed the texture toward brick
- Rule: at 16x, wood grain is runs of 3px+ along the plank direction; never
  lone 1–2px flecks

## 2026-07-19 — seam-ratio false alarm on banded textures
- Context: same session; analyzer tiling metric on all plank candidates
- Observation: seam_ratio scored 1.48–1.93 while the 3x3 previews were
  visually seamless — the wrap edge *is* a plank seam, identical to the
  interior ones, so the metric's interior average (diluted by flat runs)
  understates legitimate seam contrast
- Rule: when the wrap edge coincides with a designed seam line, treat an
  elevated seam_ratio as a false alarm once the 3x3 preview is clean
  (candidate for a smarter check in `aide/analyze.py` eventually)

## 2026-07-19 — accent colors must beat the border, not just each other
- Context: research paper tier seals (T.N.A. texture pass, iteration 5)
- Observation: a gray wax seal was invisible against the sheet's gray
  border-shade even though it was distinct from the other four seal colors
- Rule: pick accent/marker colors against the sprite's border-shade family
  first; distinctness within the accent set alone is not enough

## 2026-07-19 — paper-family items tilt
- Context: research papers r1-r2 read as framed UI cards
- Observation: an axis-aligned sheet at 16x reads as interface, not item;
  vanilla paper is a diagonal kite with a folded corner
- Rule: flat sheet items (paper, notes, maps) use the tilted vanilla
  silhouette; text/ornament follows the sheet's rotation (the lower-left
  "\" edge is the bottom; content flows top-left -> down-right)

## 2026-07-19 — vanilla wood grammar
- Context: plank/log rebuild after studying real 1.21.1 assets
- Observation: vanilla planks have NO vertical joints; grain is 1-5px runs
  of 4-5 close tones (<~10% luminance apart); seam rows are broken mixes of
  three darks. My staggered joints + discrete dark clusters read as bricks
- Rule: wood grain = runs of close tones, seams broken, no full-height
  joints; save discrete high-contrast clusters for stone

## 2026-07-19 — one arrangement, many palettes
- Context: same study; spruce and birch planks are the identical pixel grid
- Observation: vanilla achieves family consistency by recoloring a single
  arrangement per material class
- Rule: author one arrangement per family (planks, logs, saplings...) and
  recolor per material; do not redraw structure per material

## 2026-07-19 — import real refs, not memory
- Context: nugget/ingot/paper vanilla-matching (user linked mcasset.cloud)
- Observation: from-memory approximations got the nugget ~50% too big and
  the ingot on the wrong axis; importing the real sprite and mapping roles
  cell-for-cell fixed both immediately
- Rule: when matching vanilla, fetch the actual sprite (mcasset /
  InventivetalentDev minecraft-assets) and `aide import` it; never draw a
  vanilla shape from memory

## 2026-07-19 — re-anchor transplanted ramps
- Context: brass ingot direct role-map from gold read butter-pale
- Observation: color-role transplants from a saturated material to a muted
  one overbrighten, because the bright roles dominate coverage
- Rule: after transplanting a role map, re-anchor each role to the target
  material's card ramp (bright role = card highlight, not lighter)

## 2026-07-19 — vanilla refs stay out of the repos
- Context: same reference workflow
- Observation: reference PNGs are Mojang assets; committing them would
  violate the no-asset-reuse rule even as "references"
- Rule: vanilla refs live in the session scratchpad only; only silhouettes
  and structural grammar are learned from them, never pixels, and nothing
  vanilla is ever committed to either repo

## 2026-07-19 — hue shift lives in the extension steps
- Context: same session; thaumaturgy card fixes greatwood's 3 core steps,
  analyzer flagged the ramp as a straight value slide
- Observation: cool-shifting only the *added* deep seam step (4A3625 →
  4A312C) gave the ramp a 21° cool-ward shadow drift without touching any
  card color
- Rule: when a style card fixes a ramp's core steps, carry the hue shifting
  in the steps you add (deep shadows, speculars)
