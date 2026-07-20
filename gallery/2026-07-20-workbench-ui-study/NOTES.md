# Study session — workbench design vs custom UIs (2026-07-20)

**Question (from Jacob):** the design of a workbench vs custom UIs — noting that
*crafting tables don't change their UIs*. When should T.N.A.'s **arcane worktable**
just reuse the vanilla crafting-grid screen, and when does it earn a **custom UI**?

This is a UX/design study (idioms + public docs only — no mod code/pixels shipped).
It's the UI companion to the texture work: we just gave the worktable a 3×3 grid
TOP face; this asks what happens when you *right-click* it.

## Why "crafting tables don't change their UIs" is the crux
Vanilla's crafting table is the canonical example of a station that keeps ONE
screen forever: 3×3 grid + result slot, shaped/shapeless/anything all render
through `CraftingMenu`. That invariance is a *feature* — muscle memory, JEI/REI
"+" recipe-transfer, recipe book, shift-click all "just work" because the slot
shape is standard. The design tension: an arcane workbench wants to SHOW things a
plain grid can't (vis/aspect cost, a wand/focus slot, validity), which pulls
toward a custom UI — and every step away from the standard grid costs you some of
that free familiarity + tooling.

## T.N.A.-specific grounding (already known this session)
- **We already have a custom-UI stack.** The Arcane Orrery is a 420×240
  `AbstractContainerScreen` with real slots, drag-and-drop, a scrollable list, and
  3D sphere rendering (per the `minecraft-ui-design` skill). So a custom worktable
  UI is NOT greenfield — the menu+screen triad, extended-open data (BlockPos),
  optimistic-client/authoritative-server edit loop, and the NeoForge
  registration-timing fix are all already solved in this repo.
- **TC4/TC6 precedent = grid + overlay.** Thaumcraft's Arcane Workbench was a
  vanilla-shaped 3×3 grid EXTENDED with a wand slot + a vis/aspect cost readout —
  it augmented the familiar grid rather than replacing it. That "middle path" is
  the leading candidate for us and matches the 3×3-grid TOP texture we just made.
- **UI palette already set** (from the skill): panel `0xF0100A18`, chrome
  `0xFF241B33`, primary text `0xE8D9FF` — a custom worktable screen would inherit
  the orrery's look for free.

## Three research threads (running)
1. Vanilla-grid REUSE family — why crafting tables never change their UI; mods that
   deliberately reuse the grid; the UX gains of not changing it.
2. Custom arcane/tech workbench UIs — TC4/6, Ars Nouveau, Botania, Astral, Blood
   Magic, Create, AE2, Tinkers — what each custom UI BUYS over the grid.
3. Decision framework — reuse vs overlay vs fully-custom; JEI/REI transfer costs;
   the middle path; costs & pitfalls; a checklist + smell tests.

## Deliverables (planned)
- `findings.html` (collapsible sections, like the mod-design study) OR a tight
  `findings.md` if it stays short.
- `decision.md` — the reuse / overlay / fully-custom checklist, oriented to the
  arcane worktable, with a concrete recommendation.
- Proposed lessons (user-gated) if any generalize.

_Status: research fanned out; compiling on return._
