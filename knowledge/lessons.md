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

## 2026-07-19 — hue shift lives in the extension steps
- Context: same session; thaumaturgy card fixes greatwood's 3 core steps,
  analyzer flagged the ramp as a straight value slide
- Observation: cool-shifting only the *added* deep seam step (4A3625 →
  4A312C) gave the ramp a 21° cool-ward shadow drift without touching any
  card color
- Rule: when a style card fixes a ramp's core steps, carry the hue shifting
  in the steps you add (deep shadows, speculars)
