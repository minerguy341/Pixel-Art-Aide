#!/usr/bin/env python3
"""Granite, take 2 — informed by studying the 1.7.10 Underground Biomes Constructs igneous style
(study only; no pixels copied). UBC igneous reads CHUNKIER and HIGHER-CONTRAST than vanilla: distinct
2-3px mineral phenocrysts (near-black biotite, near-white quartz/plagioclase, a genuinely present warm
salmon feldspar) on a light neutral base — and it splits granite into warm 'red' and dark 'black'
variants. Candidates A-E below apply that; A is our current granite for reference."""
import copy
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw

STONE = Path(__file__).resolve().parent.parent / "2026-07-21-stone-practice"
sys.path.insert(0, str(STONE / "src"))
import make_stones as MS   # noqa: E402
import stonegen as SG      # noqa: E402

base = json.load(open(STONE / "stones.json"))["granite"]

def spec(**kw):
    s = copy.deepcopy(base)
    s.update(kw)
    return s

# Every candidate now gives the MATRIX real clustered value variation (3-tone ramp + busy_lo/hi +
# cluster) so the background between grains isn't a solid fill. A_flat is the old solid-base granite,
# kept only to show the problem the user flagged.
RED_MIN = [{"color": "2A2320", "p": 0.11},   # near-black biotite
           {"color": "C48C7A", "p": 0.17},   # salmon feldspar, genuinely present
           {"color": "F2ECE4", "p": 0.10},   # near-white quartz/plagioclase
           {"color": "8E8880", "p": 0.08}]   # grey mica
CANDS = {
    "A flat-old": base,
    "B red-granite": spec(
        desc="warm feldspar + varied matrix (base blotches, not solid)",
        ramp=["B2A69A", "C6BAAF", "DED3C8"], busy_lo=0.26, busy_hi=0.26, cluster=2,
        minerals=RED_MIN, mineral_cluster=2),
    "C red-warmer": spec(
        desc="B with a warmer, slightly darker matrix + more feldspar",
        ramp=["B49E90", "CBB4A6", "E1D2C6"], busy_lo=0.28, busy_hi=0.26, cluster=2,
        minerals=[{"color": "281F1B", "p": 0.12}, {"color": "C0846F", "p": 0.19},
                  {"color": "F3EDE6", "p": 0.09}, {"color": "94847C", "p": 0.07}],
        mineral_cluster=2),
    "D red-chunky": spec(
        desc="B with cluster=3 (bigger matrix blotches + grains)",
        ramp=["B2A69A", "C6BAAF", "DED3C8"], busy_lo=0.26, busy_hi=0.26, cluster=3,
        minerals=RED_MIN, mineral_cluster=3),
    "E black-granite": spec(
        desc="gabbro: dark varied matrix, light plagioclase laths (UBC black granite)",
        ramp=["26242A", "2E2C34", "3C3A44"], busy_lo=0.30, busy_hi=0.26, cluster=2,
        minerals=[{"color": "1B1A1C", "p": 0.14},   # black
                  {"color": "C7C2CC", "p": 0.13},   # light plagioclase
                  {"color": "7C8494", "p": 0.09},   # blue-grey
                  {"color": "9A6F64", "p": 0.05}],  # sparse warm feldspar
        flecks=[], mineral_cluster=2),
}

rows = [MS.row(SG.render(s), f"{name} — {s.get('desc','')}") for name, s in CANDS.items()]
out = Path(__file__).resolve().parent / "granite-candidates.png"
MS.sheet("GRANITE take 2 — UBC-informed (study only): warm/black variants, chunky high-contrast grains",
         rows, out)
