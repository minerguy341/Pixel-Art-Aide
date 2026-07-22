#!/usr/bin/env python3
"""Cycle 2 proof: render each noise-based stone with the legacy per-pixel base (cluster=0) vs the
new clustered-blotch base (cluster>0), side by side, so the vanilla-vs-static difference is visible.
Study-only comparison; does not overwrite the committed stone sources."""
import copy
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

STONE = Path(__file__).resolve().parent.parent / "2026-07-21-stone-practice"
sys.path.insert(0, str(STONE / "src"))
import make_stones as MS   # noqa: E402
import stonegen as SG      # noqa: E402

# clustered cell size per stone (bigger = coarser blobs); tuned to vanilla ~2-3px blotches
CLUSTER = {"marble": 3, "slate": 2, "shale": 2, "granite": 2, "basalt": 3, "sandstone": 2}

specs = json.load(open(STONE / "stones.json"))
rows = []
for name, cell in CLUSTER.items():
    legacy = SG.render(specs[name])                       # cluster absent -> per-pixel
    clus_spec = copy.deepcopy(specs[name]); clus_spec["cluster"] = cell
    clustered = SG.render(clus_spec)
    a = MS.lbl(MS.tile3(legacy), "per-pixel (old)")
    b = MS.lbl(MS.tile3(clustered), f"clustered cell={cell} (new)")
    h = max(a.height, b.height) + 18
    strip = Image.new("RGBA", (a.width + b.width + 24 + 8, h), MS.T)
    ImageDraw.Draw(strip).text((0, 2), name, fill=MS.INK)
    strip.alpha_composite(a, (0, 18)); strip.alpha_composite(b, (a.width + 24, 18))
    rows.append(strip)

out = Path(__file__).resolve().parent / "cluster-compare.png"
MS.sheet("MC-STYLE cycle 2 — per-pixel noise vs clustered blotches (left=old, right=new)", rows, out)
