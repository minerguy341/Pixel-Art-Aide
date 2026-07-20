# Reference materials & licensing policy

Read before studying any external art. This governs how the studio uses
reference material (vanilla Minecraft, other mods, tutorials, palettes) so we
improve quality **without** reusing anyone's copyrighted pixels. It applies to
every session and overrides convenience.

## The one line

**Study the *look*; never ship the *pixels*.** General craft (palette
tendencies, hole density, framing idioms, silhouette proportions, shading
grammar) is fair to learn and reproduce in our own art. A specific texture's
pixel arrangement is the author's copyrighted work — never trace, recolor, or
reproduce it closely, and never commit it.

## What counts as which

| Fair to learn (not copyrightable) | Off-limits (the author's work) |
|---|---|
| "Create's brass ramp sits ~`#8F6B38`→`#E8C983`" | copying `brass_block.png`'s exact pixels |
| "vanilla leaves run ~32–43% transparent holes" | tracing `oak_leaves.png` cell-for-cell |
| "ores cluster minerals in 3s with a highlight+shadow" | recoloring a mod's ore sprite |
| "this mod frames machine faces with a 1px border" | reproducing its casing so it's recognizably theirs |

Silhouette-matching to **vanilla** (nugget/ingot/paper shapes) is acceptable
because those simple functional shapes are effectively standard; matching a
distinctive *mod* texture's composition is not.

## Handling reference files

1. **Reference files live in the session scratchpad only — never in either
   repo.** Not `gallery/`, not anywhere committed. (See the "vanilla refs stay
   out of the repos" lesson.)
2. **Fetch public references yourself** (mcasset.cloud / InventivetalentDev
   for vanilla, official wikis for mod *descriptions*) rather than having the
   user hand over extracted mod files, which are usually redistribution-
   restricted (many mods are All-Rights-Reserved).
3. If the user *does* drop mod files in the scratchpad: study them for
   **general craft only**, extract the pattern into a palette note or an
   (approved) lesson, and delete/leave them in scratchpad. Never `git add`
   them; never reproduce a specific texture from them.
4. **When in doubt, ask.** If a requested texture would end up recognizably
   like a specific mod's asset, flag it and propose an original alternative.

## Why this project cares

Thaumaturgy's `PLAN.md` §1.4 forbids reusing Thaumcraft/vanilla assets — this
policy is the studio-side enforcement of that, extended to all mods. It's also
just correct: other creators' textures are their work.

## The mechanism note (so expectations are right)

Reference images help **only within a session, as study material while
authoring** — they don't "train" anything persistent. What actually compounds
quality is this knowledge base (`lessons.md`, `shading.md`, style cards) and
user feedback on candidates. So the highest-leverage inputs are the mod's own
art-direction decisions, feedback, and pointers to *what to study* — not piles
of copied files.
