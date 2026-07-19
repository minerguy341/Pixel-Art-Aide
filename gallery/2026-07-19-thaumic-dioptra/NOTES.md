# Thaumic Dioptra texture — session notes

Subject: re-texture the dioptra block (user: "more stone body, not obsidian").
Style: `thaumaturgy`. The block model is a mostly-full block + basin rim (TC6-style),
two texture keys: `dark` (body, all body/basin/rim-inner faces) and `band`
(base accent + rim outer). 16x16 tiling blocks, no transparency.

Direction (from lessons "Thaumcraft grammar" + mid-value rule):
- Body = cool DRESSED arcane stone (blue-grey, tidy, subtle mottle) — quarried by
  wizards, not mossy ruin. Luminance ~24–56%, hue-shifted cool in shadow.
- Band = aetherium grey-violet rune/sigil band (refined magic metal), sparse teal
  glint `#7FE8D8` as the magic tell (<3% of pixels).

Candidates:
- stone_a: smooth mottled dressed stone (subtle potato clusters).
- stone_b: dressed ashlar (running-bond arcane bricks, tidy mortar).
Both share the aetherium `band`.
