# T.N.A. texture revisions — assessed against the new mod-study lessons (2026-07-21)

Reviewed the 15 existing T.N.A. textures against the 9 new lessons. Most are
already close to grammar (earlier Create/Thaumcraft lessons pre-loaded much of it).
Candidates for a revision pass, prioritized:

1. **Arcane Worktable (side+top)** — STRONGEST. Current side = near-plain greatwood
   planks + a tiny socket; doesn't read as apparatus. Revised side (proto) applies
   the apparatus grammar: framed recessed panel + brass corner rivets + a central
   emissive aetherium/teal aspect socket. Top should become a clean "stage"
   (block-as-stage) with a subtle inlaid rune-ring. (before/after: previews/)
2. **Aura Node** — light pass: strengthen the SINGLE emissive core (glow-by-contrast:
   brighter teal centre, darker rim) so its "glowing aura source" identity is
   unmistakable — embodies make-invisible-visible + emissive-core.
3. **Aetherlens / Codex** — minor framed-relic polish (lens metal rim + glint;
   tome clasp + framed emblem). Optional.

Leave as-is (already on-grammar/correct): Arcane Orrery (framed brass + gem already),
ingots/nuggets, wand_base (grayscale-for-tint), the greatwood/silverwood set,
research papers/scrolls, metal/gilded blocks.

Staged in the studio only; nothing pushed to T.N.A. pending approval.

## Worktable top = 3x3 crafting grid (TC4 Arcane Workbench evoked, our style)
Studied TC4's Arcane Workbench read (a wizard's wooden crafting table: inlaid 3x3
grid + wand/focus slot + warm wood/tan-arcane-stone + runes) — idiom only, no
pixels copied. Our version keeps that "crafting table for wizards" read in the
thaumaturgy palette:
- greatwood board surface + brass frame + brass 3x3 grid lines.
- 9 recessed dark cells = block-as-stage slots (ingredients render in-world).
- aetherium corner studs; a teal arcane glint in the CENTRE cell = the focus/result.
- side = framed panel + brass rivets + emissive aetherium/teal socket.
Reads unmistakably as an arcane crafting station vs the current near-plain planks.
previews/worktable-grid.png. Staged only — not pushed to T.N.A.

## Node + framed-relic pass (src/make_relics.py → out/*_rev.png)
- **aura_node** — glow-by-contrast rebuild. Darkened the aetherium shell ramp and
  replaced the flat teal glass with a RADIAL bloom (deep glass rim → glint → hot →
  near-white core). The emissive teal core is now the only saturated light on the
  block; two pin-light glimmers keep the r1 "drifting mote" identity. Embodies
  emissive-core + make-invisible-visible.
- **aetherlens** — framed-relic idiom: brighter brass RIM enclosing a darker
  arcane lens CORE + one hot teal glint (was a flatter brass tube + pale lens).
- **codex** — framed-relic tome: the flat teal cross becomes a RECESSED framed
  emblem panel (dark border → teal sigil → hot centre); clasp brass brightened.
- One combined before/after: previews/revision-set.png (worktable iso + the three).
- Still studio-only until the before/after is approved for the T.N.A. PR.
