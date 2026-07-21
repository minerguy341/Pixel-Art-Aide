"""Lift the 7 wand-cap silhouettes into 3D and emit the deliverables:

  out/<name>.obj           — geometry, openable in any 3D tool / phone viewer
  previews/iso-<name>.png  — flat-shaded iso sanity render (headless review)
  previews/iso-all.png     — contact sheet of all seven
  out/wand-caps-3d.html    — self-contained rotatable WebGL gallery

Each silhouette's lift mode (revolve vs blade) is read from its .pxg header.
Run from repo root:  python3 gallery/2026-07-21-wand-caps/build_models.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from PIL import Image

from aide.lift import exposed_faces, lift, to_obj
from aide.liftviewer import build_payloads, render_iso, viewer_html

HERE = Path(__file__).resolve().parent
SRC, OUT, PREV = HERE / "src", HERE / "out", HERE / "previews"

# family base colours from the reference sheet
MATERIALS = {"aetherium": "#8A6BB6", "brass": "#C79A55"}

BLADE_THICK = 7


def read_mode(pxg: Path) -> str:
    m = re.search(r"lift mode:\s*(\w+)", pxg.read_text())
    return m.group(1) if m else "revolve"


def main():
    OUT.mkdir(exist_ok=True)
    PREV.mkdir(exist_ok=True)
    models = {}
    isos = []
    for pxg in sorted(SRC.glob("*.pxg")):
        name = pxg.stem
        mode = read_mode(pxg)
        vol = lift(pxg, mode=mode, thickness=BLADE_THICK)
        faces = exposed_faces(vol)
        (OUT / f"{name}.obj").write_text(to_obj(faces, name))
        iso = render_iso(faces, scale=13)
        iso.save(PREV / f"iso-{name}.png")
        isos.append((name, mode, iso, vol.nx, vol.ny, vol.nz, len(faces)))
        models[name] = (vol, mode)
        print(f"{name:14s} {mode:8s} {vol.nx}x{vol.ny}x{vol.nz}  "
              f"{len(vol.voxels)} voxels  {len(faces)} faces")

    # contact sheet of iso previews
    cols = len(isos)
    cw = max(i[2].width for i in isos) + 12
    ch = max(i[2].height for i in isos) + 30
    sheet = Image.new("RGBA", (cw * cols, ch), (26, 22, 34, 255))
    from PIL import ImageDraw
    d = ImageDraw.Draw(sheet)
    for k, (name, mode, iso, *_rest) in enumerate(isos):
        x = k * cw + (cw - iso.width) // 2
        sheet.paste(iso, (x, 24), iso)
        d.text((k * cw + 6, 6), f"{name} ({mode})", fill=(233, 228, 242, 255))
    sheet.save(PREV / "iso-all.png")
    print("wrote previews/iso-all.png")

    # self-contained interactive viewer
    payloads = build_payloads(models)
    html = viewer_html(payloads, MATERIALS, title="Thaumaturgy — Wand Caps (3D)")
    (OUT / "wand-caps-3d.html").write_text(html)
    kb = len(html) / 1024
    print(f"wrote out/wand-caps-3d.html  ({kb:.0f} KB, {len(payloads)} models)")


if __name__ == "__main__":
    main()
