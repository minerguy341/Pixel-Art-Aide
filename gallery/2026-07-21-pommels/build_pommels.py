"""Lift the pommels and emit OBJs, iso previews, a contact sheet, and a viewer.
Run from repo root:  python3 gallery/2026-07-21-pommels/build_pommels.py
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
MATERIALS = {"aetherium": "#8A6BB6", "brass": "#C79A55", "iron": "#8B8D98"}

RECIPES = {
    "A-wheel":         ("revolve", "wheel / disc",     dict()),
    "B-sphere":        ("revolve", "spherical",        dict()),
    "C-pear":          ("revolve", "pear",             dict()),
    "D-scent-stopper": ("hybrid",  "scent-stopper (poly-6)", dict(head_mode="poly", sides=6)),
    "E-crescent":      ("hybrid",  "crescent",         dict(head_mode="blade", thickness=7)),
    "F-mushroom":      ("revolve", "onion / mushroom", dict()),
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
        print(f"{pxg.stem:16s} {label:22s} {vol.nx}x{vol.ny}x{vol.nz}  {len(vol.voxels)} voxels")

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
    (OUT / "pommels-3d.html").write_text(
        viewer_html(payloads, MATERIALS, title="Thaumaturgy — Pommels (3D)"))
    print(f"wrote out/pommels-3d.html ({len(payloads)} pommels)")


if __name__ == "__main__":
    main()
