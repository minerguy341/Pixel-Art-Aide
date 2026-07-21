"""Lift the spear/arrowhead tips with the forged cross-section that suits each,
and emit OBJs, iso previews, a contact sheet, and a rotatable WebGL gallery.

Every tip is a round revolved collar (fits a wand core) welded to a shaped head
(hybrid mode). The head cross-section is the studied-from-real-weapons part:

  A leaf-spear  midrib  lenticular blade + raised central spine (I-beam stiffener)
  B bodkin      square  quadrangular punch tapering to a point (armour-piercer)
  C estoc       diamond rhombic: four flat facets + central ridge (thrusting point)
  D broadhead   radial  three thin blades at 120° (Y cross-section) + rear barbs
  E harpoon     lens    flat lenticular leaf with deep backward barbs
  F winged      radial  four thin blades at 90° (+ cross-section, winged pike)

Run from repo root:  python3 gallery/2026-07-21-wand-tips-study/build_tips.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3]))

from PIL import Image, ImageDraw

from aide.lift import exposed_faces, lift, to_obj
from aide.liftviewer import build_payloads, render_iso, viewer_html

HERE = Path(__file__).resolve().parent
SRC, OUT, PREV = HERE / "src", HERE / "out", HERE / "previews"

MATERIALS = {"aetherium": "#8A6BB6", "brass": "#C79A55"}

# name -> (head cross-section, label, kwargs for lift)
RECIPES = {
    "A-leaf-spear": ("midrib",  "lenticular + midrib", dict(flat=0.42, ridge=0.55)),
    "B-bodkin":     ("square",  "square bodkin",        dict(flat=0.62)),
    "C-estoc":      ("diamond", "rhombic / diamond",    dict(flat=0.60)),
    "D-broadhead":  ("radial",  "3-blade broadhead",    dict(blades=3, bladethick=0.20)),
    "E-harpoon":    ("lens",    "lenticular barbed",    dict(flat=0.40)),
    "F-winged":     ("radial",  "4-blade winged",       dict(blades=4, bladethick=0.20)),
    "G-trilobate":  ("poly",    "trilobate (poly-3)",   dict(sides=3)),
    "H-swallowtail": ("lens",   "swallowtail forked",   dict(flat=0.42)),
    "I-winged-spear": ("midrib", "boar spear + stop-ring", dict(flat=0.45, ridge=0.5)),
    "J-flamberge":  ("diamond", "flamberge (wavy)",     dict(flat=0.55)),
}


def main():
    OUT.mkdir(exist_ok=True)
    PREV.mkdir(exist_ok=True)
    models, isos = {}, []
    for pxg in sorted(SRC.glob("*.pxg")):
        name = pxg.stem
        head_mode, label, kw = RECIPES[name]
        vol = lift(pxg, mode="hybrid", head_mode=head_mode, **kw)
        faces = exposed_faces(vol)
        (OUT / f"{name}.obj").write_text(to_obj(faces, name))
        iso = render_iso(faces, scale=13)
        iso.save(PREV / f"iso-{name}.png")
        isos.append((name, label, iso))
        models[name] = (vol, label)
        print(f"{name:14s} {label:22s} {vol.nx}x{vol.ny}x{vol.nz}  "
              f"{len(vol.voxels)} voxels  {len(faces)} faces")

    cols = len(isos)
    cw = max(i[2].width for i in isos) + 12
    ch = max(i[2].height for i in isos) + 34
    sheet = Image.new("RGBA", (cw * cols, ch), (26, 22, 34, 255))
    d = ImageDraw.Draw(sheet)
    for k, (name, label, iso) in enumerate(isos):
        sheet.paste(iso, (k * cw + (cw - iso.width) // 2, 28), iso)
        d.text((k * cw + 6, 6), name, fill=(233, 228, 242, 255))
        d.text((k * cw + 6, 16), label, fill=(154, 143, 181, 255))
    sheet.save(PREV / "iso-all.png")
    print("wrote previews/iso-all.png")

    payloads = build_payloads(models)
    html = viewer_html(payloads, MATERIALS, title="Thaumaturgy — Wand Tips (3D study)")
    (OUT / "wand-tips-3d.html").write_text(html)
    print(f"wrote out/wand-tips-3d.html  ({len(html)/1024:.0f} KB, {len(payloads)} tips)")


if __name__ == "__main__":
    main()
