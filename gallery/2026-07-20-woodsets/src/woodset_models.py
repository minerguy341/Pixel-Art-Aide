"""Generate the blockstate + model + item JSON family for a wood set, staged for
new_age_thaum. Block SHAPES reuse the plank texture via vanilla parent templates
(stairs/slab/fence/gate/button/pressure-plate); only door/trapdoor/crafting-table
carry the new textures from make_woodset.py. Blockstate variant maps are taken
from the fetched vanilla oak blockstates (scratchpad) with oak->wood substitution.
Run from repo root:
  python3 gallery/2026-07-20-woodsets/src/woodset_models.py
"""
import json, pathlib

NS = "new_age_thaum"
STAGE = pathlib.Path("gallery/2026-07-20-woodsets/staging")
VAN = pathlib.Path("/tmp/claude-0/-home-user/e1ce8e98-01cb-5256-a7fd-6ca103c920b9/scratchpad/vanilla-wood")
WOODS = ["greatwood", "silverwood"]

def w(path, obj):
    p = STAGE / path; p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=2))

def blk(t): return f"{NS}:block/{t}"

def models_for(wd):
    P = blk(f"{wd}_planks")
    M = {}
    M[f"{wd}_planks"] = {"parent": "minecraft:block/cube_all", "textures": {"all": P}}
    st = {"bottom": P, "top": P, "side": P}
    M[f"{wd}_stairs"] = {"parent": "minecraft:block/stairs", "textures": st}
    M[f"{wd}_stairs_inner"] = {"parent": "minecraft:block/inner_stairs", "textures": st}
    M[f"{wd}_stairs_outer"] = {"parent": "minecraft:block/outer_stairs", "textures": st}
    M[f"{wd}_slab"] = {"parent": "minecraft:block/slab", "textures": st}
    M[f"{wd}_slab_top"] = {"parent": "minecraft:block/slab_top", "textures": st}
    for t in ("fence_post", "fence_side", "fence_inventory"):
        M[f"{wd}_{t}"] = {"parent": f"minecraft:block/{t}", "textures": {"texture": P}}
    for t, par in [("fence_gate", "template_fence_gate"), ("fence_gate_open", "template_fence_gate_open"),
                   ("fence_gate_wall", "template_fence_gate_wall"), ("fence_gate_wall_open", "template_fence_gate_wall_open")]:
        M[f"{wd}_{t}"] = {"parent": f"minecraft:block/{par}", "textures": {"texture": P}}
    for t, par in [("pressure_plate_up", "pressure_plate_up"), ("pressure_plate_down", "pressure_plate_down")]:
        M[f"{wd}_{t}"] = {"parent": f"minecraft:block/{par}", "textures": {"texture": P}}
    for t in ("button", "button_pressed", "button_inventory"):
        M[f"{wd}_{t}"] = {"parent": f"minecraft:block/{t}", "textures": {"texture": P}}
    # doors (new textures)
    dtex = {"top": blk(f"{wd}_door_top"), "bottom": blk(f"{wd}_door_bottom")}
    for half in ("bottom", "top"):
        for side in ("left", "right"):
            for op in ("", "_open"):
                nm = f"{wd}_door_{half}_{side}{op}"
                M[nm] = {"parent": f"minecraft:block/door_{half}_{side}{op}", "textures": dtex}
    # trapdoor (new texture)
    tt = {"texture": blk(f"{wd}_trapdoor")}
    M[f"{wd}_trapdoor_bottom"] = {"parent": "minecraft:block/template_orientable_trapdoor_bottom", "textures": tt}
    M[f"{wd}_trapdoor_top"] = {"parent": "minecraft:block/template_orientable_trapdoor_top", "textures": tt}
    M[f"{wd}_trapdoor_open"] = {"parent": "minecraft:block/template_orientable_trapdoor_open", "textures": tt}
    # crafting table (new faces)
    M[f"{wd}_crafting_table"] = {"parent": "minecraft:block/cube", "textures": {
        "particle": blk(f"{wd}_crafting_table_front"), "down": P, "up": blk(f"{wd}_crafting_table_top"),
        "north": blk(f"{wd}_crafting_table_front"), "south": blk(f"{wd}_crafting_table_side"),
        "east": blk(f"{wd}_crafting_table_side"), "west": blk(f"{wd}_crafting_table_front")}}
    return M

def items_for(wd):
    I = {}
    for t in ("planks", "stairs", "slab", "fence_inventory", "button_inventory",
              "pressure_plate_up", "trapdoor_bottom", "crafting_table"):
        nm = {"fence_inventory": "fence", "button_inventory": "button",
              "pressure_plate_up": "pressure_plate", "trapdoor_bottom": "trapdoor"}.get(t, t)
        I[f"{wd}_{nm}"] = {"parent": blk(f"{wd}_{t}")}
    I[f"{wd}_fence_gate"] = {"parent": blk(f"{wd}_fence_gate")}
    I[f"{wd}_door"] = {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{wd}_door"}}
    return I

def blockstates_for(wd):
    """substitute the fetched vanilla oak blockstates: model refs oak->wood, ns->ours."""
    BS = {}
    # planks + crafting_table are simple single-variant — construct directly
    BS[f"{wd}_planks"] = {"variants": {"": {"model": blk(f"{wd}_planks")}}}
    BS[f"{wd}_crafting_table"] = {"variants": {"": {"model": blk(f"{wd}_crafting_table")}}}
    for typ in ("stairs", "slab", "fence", "fence_gate", "door", "trapdoor", "pressure_plate", "button"):
        raw = (VAN / "blockstates" / f"oak_{typ}.json").read_text()
        raw = raw.replace("minecraft:block/oak_", f"{NS}:block/{wd}_").replace("block/oak_", f"block/{wd}_")
        BS[f"{wd}_{typ}"] = json.loads(raw)
    return BS

if __name__ == "__main__":
    nf = 0
    for wd in WOODS:
        for nm, obj in models_for(wd).items():
            w(f"models/block/{nm}.json", obj); nf += 1
        for nm, obj in items_for(wd).items():
            w(f"models/item/{nm}.json", obj); nf += 1
        for nm, obj in blockstates_for(wd).items():
            w(f"blockstates/{nm}.json", obj); nf += 1
    print("staged", nf, "JSON files ->", STAGE)
