# Quick study — real wood + mod logs (before r3 bark/cores)

Study only (reference-policy: learn the look, no pixels committed). Drives the r3 redo of
bark + end grains for both woods, targeting two pieces of user feedback:
1. bark **edge columns are solid** → the wrap doesn't flow → **parallel logs look separated**.
2. **silverwood should read pristine & serene** outwardly.

## Findings

- **Bark must MERGE across adjacent logs, not frame each one.** Vanilla bark/hewn-log blocks
  are built so the texture is consistent and connects between neighbours. A uniform (esp.
  *lighter*) edge column makes a bright vertical band at every log-to-log seam → reads as a gap.
  **Fix:** put a furrow/groove **straddling the x=0/15 wrap** so a continuous groove runs across
  the join, and carry the same variation density to the edge columns as the interior.
- **Young birch = the pristine/serene template.** Birch bark is smooth, resinous, pale, marked by
  **horizontal lenticels**, peeling in thin sheets; it only turns deeply furrowed / broken into
  plates when **old**. So silverwood = *young birch*: smooth, luminous, minimal marks — NOT
  furrowed. Bonus: horizontal lenticels create no vertical edge band, so they directly fix the
  "parallel logs separated" problem.
- **Furrowed hardwood bark is IRREGULAR.** Furrows wander and deepen with age and break into
  *irregular* plates — never a regular brick grid (my r2 "cracked" was too masonry-like).
  Greatwood = ancient hardwood → deep **wandering** furrows, rounded ridges, sparse irregular checks.
- **Magic-wood idiom** (Botania livingwood→dreamwood is the pale/ethereal one; Ars archwood is
  luminous): pale ethereal wood + a **whisper** of glow, kept smooth. Confirms dialing silverwood's
  teal back to a serene ≤~3% (r2 veined 7% / radiant 14% were too loud).

## r3 rules
- **Seam-straddling groove** on every bark side; edge columns as busy as interior (kills the frame).
- **Greatwood**: deep IRREGULAR wandering furrows + rounded ridges; sparse irregular checks (no brick grid).
- **Silverwood**: young-birch smooth + pale + luminous; soft grooves or horizontal lenticels;
  teal a faint whisper only. Pristine & serene.
- **End grain**: soft concentric rings; greatwood warm/eccentric, silverwood serene pale + gentle
  luminous heart (subtle teal, not a teal block).

Sources (study, not copied): Minecraft Wiki *Log/Wood*; birch bark refs (Britannica, Crow's Path
tree anatomy, tree-ID bark guides); Botania *Livingwood/Dreamwood* rework PR; Ars Nouveau *Archwood*.
