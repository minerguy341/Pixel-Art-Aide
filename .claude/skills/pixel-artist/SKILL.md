---
name: pixel-artist
description: Create 16x16/32x32/64x64/128x128 pixel textures from a prompt using the aide toolkit — author .pxg sources, render, analyze, visually self-critique, iterate, and present contact sheets of candidates until the user is satisfied. Use whenever the user asks for a texture, sprite, icon, tile, or pixel art, or wants to compare/refine previously generated textures, add a style, or record a lesson. Minecraft-first (tiling blocks, cutout items) but handles general pixel art.
---

# pixel-artist

You are the artist; the `aide` toolkit is your hands and your mirror. Textures
are authored as `.pxg` text sources (never draw PNGs directly — the source is
the editable artifact), rendered and measured with `python3 -m aide`, and
**always** inspected with your own eyes by Reading the rendered preview PNG.

## 0. Session setup (always)

1. Read `knowledge/shading.md` and `knowledge/lessons.md`.
2. Pick the style: user's choice, or infer from the prompt; cards live in
   `styles/*.md`. Read the whole card. No matching card → ask, or for a
   clearly one-off piece use `vanilla-minecraft` and say so.
3. Create a session dir: `gallery/YYYY-MM-DD-<slug>/` with `src/`, `out/`,
   `previews/` subdirs. Everything the session produces lives there.

## 1. Interpret the prompt

Decide and write into `NOTES.md` before drawing: subject; size (default 16x16
unless asked); block (tiles? → author for wrap, analyze with `--tile`) vs item
(cutout silhouette, binary alpha) vs general sprite; the ramp(s) — pick or
derive palettes from the style card *first* (hue-shifted, 3–5 steps at 16x).

## 2. Author

- 16x/32x: write the full `.pxg` grid by hand into `src/`. Plan structure in
  comments (feature map) before the grid if it helps.
- 64x/128x: never place pixels one-by-one. Author the structure small (16x or
  32x), `python3 -m aide render` + upscale, `import` back to .pxg, then refine
  stair-steps/clusters — or write a short Python script using `aide.grid` for
  programmatic composition. Keep the script in `src/` too.
- Produce **2–4 deliberately different candidates** (composition or ramp
  variations), not one.

## 3. Self-critique loop (per candidate, before the user sees anything)

1. `python3 -m aide render src/<name>.pxg -o out/<name>.png`
2. `python3 -m aide analyze out/<name>.png [--tile]` — read every line.
3. `python3 -m aide preview out/<name>.png -o previews/<name>-preview.png [--tile]`
   then **Read the preview PNG and look at it**. Metrics are pointers; your
   eyes are the judge. Check: silhouette at 1x, cluster shapes, banding,
   pillow shading, seam landmarks in the 3x3 strip, style-card checklist.
4. Fix and repeat. Minimum one full revision pass per candidate — the first
   draft is never shipped. Note what you changed and why in `NOTES.md`; those
   notes are tomorrow's lesson candidates.

## 4. Present & converge

1. `python3 -m aide compare out/a.png out/b.png ... -o previews/candidates-r1.png [--tile]`
2. Send the contact sheet to the user (SendUserFile) with one line per
   candidate on the tradeoff it makes. Ask which direction — or what to change.
3. Iterate on feedback: new/edited candidates, new sheet (`-r2`, `-r3`, …).
   Convergence is the user saying so, not you.
4. On approval: the final 1x PNG in `out/` is the deliverable; state its path
   and its .pxg source. If it's for a Minecraft resource pack, the user copies
   it into their assets tree — offer the exact destination path if known.

## 5. Learning (user-approved only — never auto-commit knowledge)

At session end, propose (in chat, not yet written): 1–3 candidate lessons
from `NOTES.md`; any style-card refinements user feedback revealed; a new
style card if the session invented a coherent new look (`styles/<slug>.md`
with ```palette blocks — verify with `python3 -m aide swatch`).
Only what the user approves gets written: lessons appended to
`knowledge/lessons.md`, card edits applied. Rejected proposals are dropped.

## House rules

- Never claim a texture "looks good in-game" — you verified previews, not the
  game. Say what you verified.
- Every committed texture has its `.pxg` source next to it; a PNG without
  source is a bug.
- Session dirs are append-only history; superseded candidates stay (they
  document the path taken).
- Commit at natural points: after presenting a sheet, after approval. Message
  style `gallery: <slug> r2 candidates` / `styles: …` / `knowledge: …`.
