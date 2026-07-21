"""Lift the fantasy caps with a fitting cross-section, and emit OBJs, iso
previews, a contact sheet, and a rotatable WebGL gallery.

Run from repo root:  python3 gallery/2026-07-21-fantasy-caps/build_fantasy.py
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image, ImageDraw

from aide.lift import exposed_faces, lift, to_obj
from aide.liftviewer import build_payloads, render_iso, viewer_html

HERE = Path(__file__).resolve().parent
SRC, OUT, PREV = HERE / "src", HERE / "out", HERE / "previews"
MATERIALS = {"aetherium": "#8A6BB6", "brass": "#C79A55", "moonstone": "#B9C4E0"}

# name -> (mode, label, lift kwargs)
RECIPES = {
    "A-orb":         ("revolve", "crystal orb",        dict()),
    "B-crystal":     ("hybrid",  "hex crystal (poly-6)", dict(head_mode="poly", sides=6)),
    "C-starburst":   ("hybrid",  "6-blade starburst",  dict(head_mode="radial", blades=6, bladethick=0.16)),
    "D-moon":        ("hybrid",  "crescent moon",      dict(head_mode="blade", thickness=7)),
    "E-gem-setting": ("revolve", "gem in a setting",   dict()),
    "F-beaded":      ("revolve", "beaded finial",      dict()),
}


def main():
    OUT.mkdir(exist_ok=True)
    PREV.mkdir(exist_ok=True)
    models, isos = {}, []
    for pxg in sorted(SRC.glob("*.pxg")):
        mode, label, kw = RECIPES[pxg.stem]
        vol = lift(pxg, mode=mode, **kw)
        faces = exposed_faces(vol)
        (OUT / f"{pxg.stem}.obj").write_text(to_obj(faces, pxg.stem))
        iso = render_iso(faces, scale=13)
        iso.save(PREV / f"iso-{pxg.stem}.png")
        isos.append((pxg.stem, label, iso))
        models[pxg.stem] = (vol, label)
        print(f"{pxg.stem:14s} {label:22s} {vol.nx}x{vol.ny}x{vol.nz}  "
              f"{len(vol.voxels)} voxels")

    cw = max(i[2].width for i in isos) + 12
    ch = max(i[2].height for i in isos) + 34
    sheet = Image.new("RGBA", (cw * len(isos), ch), (26, 22, 34, 255))
    d = ImageDraw.Draw(sheet)
    for k, (name, label, iso) in enumerate(isos):
        sheet.paste(iso, (k * cw + (cw - iso.width) // 2, 28), iso)
        d.text((k * cw + 6, 6), name, fill=(233, 228, 242, 255))
        d.text((k * cw + 6, 16), label, fill=(154, 143, 181, 255))
    sheet.save(PREV / "iso-all.png")

    payloads = build_payloads(models)
    (OUT / "fantasy-caps-3d.html").write_text(
        viewer_html(payloads, MATERIALS, title="Thaumaturgy — Fantasy Caps (3D)"))
    print(f"wrote out/fantasy-caps-3d.html ({len(payloads)} caps)")


if __name__ == "__main__":
    main()
