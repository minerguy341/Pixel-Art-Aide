#!/usr/bin/env python3
"""r3: v-groove x weathered hybrid — tongue-&-groove bevel per board PLUS weathered hairline checks.
Direct merge of candidate 3 (v-groove) and candidate 8 (weathered) from r2, with a couple of
variations. Both woods, shown tiled/block/slab/stair. Reuses make_planks + make_planks_r2 helpers.
"""
import make_planks as MP
import make_planks_r2 as MP2

GW, SW, B = MP.GW, MP.SW, MP2.B


def arrangements(pal):
    return {
        "vgw": MP2.boards(pal, [(4, B)] * 4, [3, 9], groove=True, checks=True, sh_p=0.30, seed=21),
        "vgwrandom": MP2.boards(pal, [(6, B), (4, B), (6, B)], [2, 8], groove=True, checks=True,
                                sh_p=0.30, seed=22),
        "vgwheavy": MP2.boards(pal, [(4, B)] * 4, [1, 5, 9, 13], groove=True, checks=True,
                               grain=0.5, sh_p=0.36, seed=23),
    }


LABELS = {
    "vgw": "A  v-groove + weathered (direct merge, 4px boards)",
    "vgwrandom": "B  v-groove + weathered, random-width boards (6/4/6)",
    "vgwheavy": "C  v-groove + weathered, heavier checks + grain",
}


def main():
    for wood, pal in (("greatwood", GW), ("silverwood", SW)):
        arr = arrangements(pal)
        for key, img in arr.items():
            name = f"{wood}_planks_{key}_r3"
            (MP.SRC / f"{name}.pxg").write_text(MP.G.to_text(MP.G.from_image(img)))
            MP.G.save_texture(img, MP.OUT / f"{name}.png")
        rows = [MP.row(arr[k], LABELS[k]) for k in LABELS]
        MP.sheet(f"{wood.upper()} PLANKS r3 - v-groove x weathered hybrid (tiled | block | slab | stair)",
                 rows, MP.PREV / f"sheet-{wood}-planks-r3.png")


if __name__ == "__main__":
    main()
