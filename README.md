# Pixel-Art-Aide

A Claude-driven studio for small pixel textures (16x16 → 128x128,
Minecraft-first). You describe a texture; Claude authors it as a reviewable
text source, renders it, measures it, critiques it with its own eyes, and
hands you a contact sheet of candidates to choose from — iterating until
you're happy. What each session teaches is distilled into style cards and a
lessons log (with your approval), so the studio gets better over time.

## How it works

1. **Author** — textures are written as `.pxg` files: a palette plus a
   character grid, one char per pixel. Human-readable, diffable, editable.
2. **Render & measure** — `python3 -m aide` renders PNGs and preview sheets
   (upscales, pixel grid, 3x3 tiling) and runs analyzers: palette/value
   stats, seam-tileability scoring, pillow-shading and hue-shift detection,
   busyness, alpha hygiene.
3. **Critique & iterate** — the pixel-artist skill (in `.claude/skills/`)
   makes Claude inspect its own rendered output and revise before you ever
   see it.
4. **Compare** — candidates arrive as a contact-sheet PNG; you pick, comment,
   and rounds continue until satisfied. Sessions live in `gallery/`.
5. **Learn** — approved lessons land in `knowledge/lessons.md`; styles are
   catalogued in `styles/` (seeded: `vanilla-minecraft`, `create-mod`,
   `thaumaturgy`).

## Quick start (human)

```
pip install -r requirements.txt
python3 tests/smoke.py                                   # toolkit self-check
python3 -m aide swatch styles/thaumaturgy.md -o /tmp/sw.png
python3 -m aide analyze some_texture.png --tile
```

Then ask Claude for a texture — the skill does the rest.
