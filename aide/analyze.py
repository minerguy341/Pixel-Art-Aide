"""Texture analyzers.

Every metric here is a heuristic signal for the reviewing agent, not a verdict:
the numbers point at *where to look* in the rendered preview. Thresholds encode
the Minecraft-first house rules (see styles/ and knowledge/shading.md).
"""

from __future__ import annotations

import colorsys
import math
from PIL import Image

RGBA = tuple[int, int, int, int]


def luminance(c) -> float:
    """Relative luminance 0..1 (Rec. 709 weights on gamma-encoded values —
    fine for comparing texture values, not for photometry)."""
    r, g, b = c[0] / 255, c[1] / 255, c[2] / 255
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def _hex(c: RGBA) -> str:
    s = f"#{c[0]:02X}{c[1]:02X}{c[2]:02X}"
    return s if c[3] == 255 else s + f"{c[3]:02X}"


def _pixels(img: Image.Image) -> list[list[RGBA]]:
    img = img.convert("RGBA")
    px = img.load()
    return [[px[x, y] for x in range(img.width)] for y in range(img.height)]


def analyze(img: Image.Image, expect_tiling: bool = False) -> dict:
    """Return a metrics dict; see report() for the human rendering of it."""
    grid = _pixels(img)
    w, h = img.width, img.height
    opaque = [(x, y, grid[y][x]) for y in range(h) for x in range(w) if grid[y][x][3] > 0]

    m: dict = {"size": f"{w}x{h}"}

    # --- palette ---
    counts: dict[RGBA, int] = {}
    for _, _, c in opaque:
        counts[c] = counts.get(c, 0) + 1
    total = max(1, len(opaque))
    palette = sorted(counts.items(), key=lambda kv: -kv[1])
    m["color_count"] = len(palette)
    m["palette"] = [
        {"hex": _hex(c), "share": round(100 * n / total, 1), "luminance": round(100 * luminance(c), 1)}
        for c, n in palette
    ]

    # --- alpha ---
    partial = sum(1 for row in grid for c in row if 0 < c[3] < 255)
    transparent = w * h - len(opaque) - partial
    m["alpha"] = {"opaque": len(opaque), "partial": partial, "transparent": transparent}

    # --- value range (Minecraft house rule: block albedo ~25-80% luminance) ---
    if opaque:
        lums = [luminance(c) for _, _, c in opaque]
        m["value"] = {
            "min": round(100 * min(lums), 1),
            "max": round(100 * max(lums), 1),
            "mean": round(100 * sum(lums) / len(lums), 1),
        }

    # --- local contrast / busyness: mean |luminance delta| between neighbors ---
    diffs, runs = [], []
    for y in range(h):
        run = 1
        for x in range(w):
            c = grid[y][x]
            if x + 1 < w:
                n = grid[y][x + 1]
                if c[3] > 0 and n[3] > 0:
                    diffs.append(abs(luminance(c) - luminance(n)))
                run = run + 1 if n == c else _push_run(runs, run)
            if y + 1 < h and c[3] > 0 and grid[y + 1][x][3] > 0:
                diffs.append(abs(luminance(c) - luminance(grid[y + 1][x])))
        _push_run(runs, run)
    m["busyness"] = round(100 * sum(diffs) / len(diffs), 2) if diffs else 0.0
    m["max_flat_run"] = max(runs) if runs else 0

    # --- tileability: seam contrast across wrap edges vs interior contrast ---
    if expect_tiling and diffs:
        seam = []
        for y in range(h):
            a, b = grid[y][w - 1], grid[y][0]
            if a[3] > 0 and b[3] > 0:
                seam.append(abs(luminance(a) - luminance(b)))
        for x in range(w):
            a, b = grid[h - 1][x], grid[0][x]
            if a[3] > 0 and b[3] > 0:
                seam.append(abs(luminance(a) - luminance(b)))
        interior = sum(diffs) / len(diffs)
        seam_mean = sum(seam) / len(seam) if seam else 0.0
        m["tiling"] = {
            "seam_contrast": round(100 * seam_mean, 2),
            "interior_contrast": round(100 * interior, 2),
            "seam_ratio": round(seam_mean / interior, 2) if interior > 0 else 0.0,
        }

    # --- pillow shading: does luminance track distance from the centroid? ---
    if len(opaque) > 8:
        cx = sum(x for x, _, _ in opaque) / len(opaque)
        cy = sum(y for _, y, _ in opaque) / len(opaque)
        dists = [-math.hypot(x - cx, y - cy) for x, y, _ in opaque]
        lums = [luminance(c) for _, _, c in opaque]
        m["pillow_r"] = round(_pearson(dists, lums), 2)

    # --- hue ramps: cluster colors by hue, check for hue shift across values ---
    m["ramps"] = _ramp_report(palette)

    return m


def _push_run(runs: list[int], run: int) -> int:
    runs.append(run)
    return 1


def _pearson(xs: list[float], ys: list[float]) -> float:
    n = len(xs)
    mx, my = sum(xs) / n, sum(ys) / n
    cov = sum((a - mx) * (b - my) for a, b in zip(xs, ys))
    vx = math.sqrt(sum((a - mx) ** 2 for a in xs))
    vy = math.sqrt(sum((b - my) ** 2 for b in ys))
    return cov / (vx * vy) if vx > 0 and vy > 0 else 0.0


def _ramp_report(palette: list[tuple[RGBA, int]]) -> list[dict]:
    """Group colors into hue clusters and report the shadow->highlight hue drift.

    Direction is judged by which ramp end sits closer to the cool pole (240°,
    blue): shadows nearer blue than highlights = 'cool' (the natural-light
    convention), the reverse = 'warm', tiny deltas = 'none'.
    """
    entries = []
    for c, _ in palette:
        r, g, b = c[0] / 255, c[1] / 255, c[2] / 255
        hue, light, sat = colorsys.rgb_to_hls(r, g, b)
        entries.append({"c": c, "h": hue * 360, "l": light, "s": sat})

    clusters: list[list[dict]] = []
    for e in sorted(entries, key=lambda e: e["h"]):
        if e["s"] < 0.08:  # near-grays don't carry usable hue
            continue
        for cl in clusters:
            if _hue_dist(cl[-1]["h"], e["h"]) < 35:
                cl.append(e)
                break
        else:
            clusters.append([e])

    report = []
    for cl in clusters:
        if len(cl) < 2:
            continue
        by_light = sorted(cl, key=lambda e: e["l"])
        dark, light = by_light[0], by_light[-1]
        magnitude = _hue_dist(dark["h"], light["h"])
        toward_cool = _hue_dist(dark["h"], 240) - _hue_dist(light["h"], 240)
        direction = "none" if magnitude < 6 else ("cool" if toward_cool < 0 else "warm")
        report.append(
            {
                "colors": [_hex(e["c"]) for e in by_light],
                "steps": len(cl),
                "hue_shift_deg": round(magnitude, 1),
                "shadow_direction": direction,
            }
        )
    return report


def _hue_dist(a: float, b: float) -> float:
    d = abs(a - b) % 360
    return min(d, 360 - d)


def report(m: dict, expect_tiling: bool = False) -> str:
    lines = [f"size {m['size']}, {m['color_count']} colors"]
    pal = ", ".join(f"{p['hex']} ({p['share']}%, L{p['luminance']})" for p in m["palette"][:16])
    lines.append(f"palette: {pal}" + (" …" if m["color_count"] > 16 else ""))

    a = m["alpha"]
    if a["partial"]:
        lines.append(f"ALPHA: {a['partial']} semi-transparent pixels — Minecraft block/item textures should use binary alpha")
    if a["transparent"]:
        lines.append(f"alpha: {a['transparent']} transparent px (item-style cutout)")

    if "value" in m:
        v = m["value"]
        flag = ""
        if v["min"] < 20 or v["max"] > 85:
            flag = "  <- outside the mid-value band (house rule ~25-80%); fine for accents, check it's intentional"
        lines.append(f"value range: {v['min']}%..{v['max']}% (mean {v['mean']}%){flag}")

    busy = m["busyness"]
    busy_note = "very flat" if busy < 2 else "calm" if busy < 5 else "moderate" if busy < 10 else "busy — likely noisier than vanilla/Create"
    lines.append(f"local contrast: {busy} ({busy_note}); longest flat run {m['max_flat_run']}px")

    if "tiling" in m:
        t = m["tiling"]
        verdict = "seam likely invisible" if t["seam_ratio"] <= 1.3 else "seam may show" if t["seam_ratio"] <= 2.0 else "SEAM WILL SHOW — fix wrap edges"
        lines.append(f"tiling: seam contrast {t['seam_contrast']} vs interior {t['interior_contrast']} (ratio {t['seam_ratio']}) — {verdict}")

    if "pillow_r" in m:
        r = m["pillow_r"]
        if r >= 0.45:
            lines.append(f"pillow-shading r={r} — brightness tracks the center; check for concentric shading")
        else:
            lines.append(f"pillow-shading r={r} (ok)")

    for ramp in m["ramps"]:
        if ramp["shadow_direction"] == "none":
            note = "no hue shift — ramp is a straight value slide"
        elif ramp["shadow_direction"] == "cool":
            note = f"hue shifts {ramp['hue_shift_deg']:.0f}° cool-ward in shadow (good)"
        else:
            note = f"hue shifts {ramp['hue_shift_deg']:.0f}° WARM-ward in shadow (usually backwards)"
        lines.append(f"ramp {' -> '.join(ramp['colors'])}: {note}")

    lines.append("(metrics are pointers, not verdicts — always eyeball the rendered preview)")
    return "\n".join(lines)
