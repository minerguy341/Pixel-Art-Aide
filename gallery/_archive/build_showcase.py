"""Build ONE interactive page with everything modelled so far — the seven wand
caps lifted from the original art plus the ten forged spear/arrowhead tips —
grouped and labelled in a single self-contained WebGL gallery.

Output: gallery/wand-showcase-3d.html  (publish this as the combined artifact)
Run from repo root:  python3 gallery/build_showcase.py
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # gallery/_archive
ROOT = HERE.parents[1]                           # repo root
sys.path.insert(0, str(ROOT))

from aide.lift import lift
from aide.liftviewer import build_payloads, viewer_html

CAPS = HERE / "2026-07-21-wand-caps"
TIPS = HERE / "2026-07-21-wand-tips-study"
FANTASY = HERE / "2026-07-21-fantasy-caps"
POMMELS = HERE / "2026-07-21-pommels"
MATERIALS = {"aetherium": "#8A6BB6", "brass": "#C79A55", "moonstone": "#B9C4E0"}


def _import(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build_caps() -> dict:
    """The original 7 caps: round heads revolve; flat heads use a round collar
    welded to a blade (hybrid) — same recipe as their own build script."""
    out = {}
    for pxg in sorted((CAPS / "src").glob("*.pxg")):
        head = "revolve" if "revolve" in pxg.read_text().splitlines()[0] else "blade"
        if head == "revolve":
            vol, label = lift(pxg, mode="revolve"), "revolve"
        else:
            vol, label = lift(pxg, mode="hybrid", head_mode="blade", thickness=7), "blade + round base"
        out[pxg.stem] = (vol, label)
    return out


def build_tips() -> dict:
    """The 10 forged tips, via their build script's RECIPES (single source)."""
    recipes = _import(TIPS / "build_tips.py").RECIPES
    out = {}
    for pxg in sorted((TIPS / "src").glob("*.pxg")):
        head_mode, label, kw = recipes[pxg.stem]
        out[pxg.stem] = (lift(pxg, mode="hybrid", head_mode=head_mode, **kw), label)
    return out


def _build_from(dirn: Path, script: str) -> dict:
    """Generic: lift a set from its build script's RECIPES = {name: (mode, label, kw)}."""
    recipes = _import(dirn / script).RECIPES
    out = {}
    for pxg in sorted((dirn / "src").glob("*.pxg")):
        mode, label, kw = recipes[pxg.stem]
        out[pxg.stem] = (lift(pxg, mode=mode, **kw), label)
    return out


def main():
    caps = build_caps()
    tips = build_tips()
    fantasy = _build_from(FANTASY, "build_fantasy.py")
    pommels = _build_from(POMMELS, "build_pommels.py")
    payloads = (build_payloads(caps, group="Caps · lifted from the art")
                + build_payloads(tips, group="Forged tips · cross-section study")
                + build_payloads(fantasy, group="Fantasy caps · orbs, crystals, moons")
                + build_payloads(pommels, group="Pommels · butt-end knobs"))
    html = viewer_html(payloads, MATERIALS,
                       title="Thaumaturgy — Wand Parts (3D)")
    out = HERE / "wand-showcase-3d.html"
    out.write_text(html)
    print(f"wrote {out.relative_to(ROOT)}  ({len(html)/1024:.0f} KB, {len(payloads)} models: "
          f"{len(caps)} caps + {len(tips)} tips + {len(fantasy)} fantasy + {len(pommels)} pommels)")


if __name__ == "__main__":
    main()
