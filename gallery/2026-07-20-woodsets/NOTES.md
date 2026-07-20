# Greatwood & Silverwood wood-sets (2026-07-20)

Applied the mod-design-study wood-set synthesis (Framed/Macaw's/Supplementaries):
author only the plank + the genuinely-new faces; UV-map the plank through vanilla
parent models for every shape; one SHARED iron hardware ramp binds the family.

## New textures (make_woodset.py — the source of record)
Per wood: door_bottom, door_top, door (item), trapdoor, crafting_table_top/front/side.
- Plank ramps are canonical (styles/thaumaturgy.md); grain authored as RUNS (3–7px)
  per the wood-grain lesson (fixed an initial per-pixel-noise pass).
- Iron hardware (hinges/handle/bolts/saw) is ONE shared ramp #2B2D33/474A53/6D7079/9297A1,
  invariant across both woods (Macaw's idiom) — the accent is the brand, wood is the variable.

## Models (woodset_models.py) — 100 JSON files staged
- Shapes reuse the plank via vanilla parents (no new art): planks, stairs(+inner/outer),
  slab(+top), fence(post/side/inv), fence_gate(+open/wall/wall_open), pressure_plate(up/down),
  button(+pressed/inventory).
- New-art blocks: door (8 models), trapdoor (bottom/top/open), crafting_table (cube w/ our faces).
- Blockstates taken from vanilla oak (scratchpad) with oak->wood + ns substitution; planks &
  crafting_table constructed directly. All 100 JSON validate.
- STAGED only (gallery/.../staging) — not pushed to T.N.A. pending approval + Java registration.

## Rendered on real shapes
previews/woodset-families.png — planks/stairs/crafting iso, full door (door model), trapdoor.

## Remaining wood-set items (follow-up)
- Boats + chest boats: MC entity texture (specific atlas layout) + item sprite — a separate
  entity-texture pipeline; deferred.
- Signs + hanging signs: entity sign texture + item; deferred.
- Slab "double" model reuses planks (implicit).
Verification: previews only; not claiming in-game correctness (blockstate wiring is a T.N.A. task).
