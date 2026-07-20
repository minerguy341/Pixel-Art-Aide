# Decision — arcane worktable UI (terse checklist)

The one rule: **every step off the vanilla 3×3 buys expressive power and costs free
infrastructure** (recipe book, JEI/REI "+" transfer, quick-move, universal recipe compat).
Go custom only for a mechanic the grid can't hold — and budget rebuilding the parity.

## Reuse the vanilla grid IF
- crafting is plain 3×3 shaped/shapeless with no cost the player must see
- the magic is in the ingredients/outputs, not the act of crafting
- you want recipe-book + JEI/REI auto-fill free, zero plugin work

## Add an arcane overlay (grid + readout) IF  ← **default for an arcane workbench**
- still grid-shaped, but a cost/requirement (vis/aspects) must be shown and can gate the craft
- a non-consumed tool (wand/focus) participates without joining the recipe grammar
- the new mechanic is a *modifier on grid crafting* — chips/bars/labels around an unchanged grid

## Go fully custom IF (need ≥1) — and you've budgeted MenuType+Screen+sync+validation+JEI+REI
- recipe shape isn't a grid (radial / node-graph / pedestal-orbit / sequential)
- a resource axis must be interactively *manipulated*, not just displayed
- validity/cost is a live-recomputing feedback surface central to the interaction
- search/category browsing of a large set (research tree, spell builder)
- preview-then-commit

## Smell tests
- **reskin sin:** custom screen = a 3×3 with a nicer background and nothing else → revert
- can't name the grid-breaking mechanic in one sentence → don't go custom
- recipe JSON grew cost/aspect/tool fields explained in tooltip/wiki not UI → wants an overlay
- cost readout only updates on reopen → not recomputing on change / not syncing
- failed craft gives no reason → add the "why" tooltip
- empty arcane slots look identical to grid slots → add ghost hints/labels

---

## Verdict for T.N.A.
**Arcane worktable = grid + overlay** (Thaumcraft's augment-don't-replace):
- real vanilla-shaped 3×3 + result (vanilla recipes work; JEI/recipe-book largely survive)
- a **wand/focus slot** with a ghost-wand empty-state hint
- a **ring of aspect/vis cost chips** — appear only when the recipe needs them, live-recompute
  on slot change; result slot locks with a "why" tooltip when unaffordable
- matches the **3×3-grid top face** we just shipped; reuses the **Arcane Orrery** menu+screen+sync
  stack, the dark-purple UI palette, the **C2S-validation** craft packet, **data-components** for
  wand vis / research state

**Reserve fully-custom** for genuinely different shapes, not the worktable:
- **infusion** — central pedestal + orbiting input pedestals (in-world)
- **research web** — node-and-line browser + search
- **essentia** — fill columns + tier-trim, from the container-readout lesson

## Candidate lessons (user-gated — not written until approved)
1. **UI-reuse contract** — a crafting station should reuse the vanilla 3×3 screen unless it needs
   a mechanic the grid structurally can't hold; going custom forfeits recipe-book + JEI/REI "+"
   + quick-move + universal recipe compat, which you then owe by hand (JEI *and* REI plugin +
   category + validated transfer handler).
2. **Augment-don't-replace for arcane crafting** — the default arcane-workbench UI is the vanilla
   grid + an overlay (tool/battery slot + a ring of cost/validity chips that appear only when
   relevant and live-recompute), never a bespoke reskinned grid. Reserve fully-custom UIs for
   genuinely non-grid shapes (infusion pedestal-ring, research node-graph, essentia columns).
