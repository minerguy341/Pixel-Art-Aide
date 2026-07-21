# Wand caps — silhouette → 3D (2026-07-21)

New capability: **generate a 3D model from 2D art**. From a reference sheet of
seven unlit wand-cap silhouettes (side profiles: ringed ferrule collar → neck →
decorative head), infer the missing depth and hand back a rotatable 3D model.

## Pipeline

1. `make_profiles.py` — authors the 7 silhouettes analytically into `src/*.pxg`
   (opaque pixel = shape). These `.pxg` files are the editable source of record;
   tweak the math or hand-edit the grids.
2. `aide.lift` — infers the third dimension ("expand the width"):
   - **revolve**: lathe the profile about its long (shaft) axis → round
     cross-section. Depth is inferred from height. Used for A / D / F and every
     collar that's on a revolve cap.
   - **blade**: keep the outline, give it a Z thickness that tapers toward the
     edges (thick spine, thin rim) via a distance transform → flat forged look.
   - **hybrid**: a round revolved collar welded to a bladed head, so a flat cap
     still gets a cylindrical base that fits a round wand core. Used for the
     flat heads B / C / E / G; the round heads A / D / F revolve whole (their
     collar is already a cylinder). `merge()` reconciles the two depth frames.
3. `aide.liftviewer` — static iso PNG (headless review) + a self-contained
   WebGL page (orbit by mouse/touch, pinch/scroll zoom, material toggle,
   voxel-face view). No external requests → runs in a locked-down sandbox.
4. `build_models.py` — runs all seven, writes `out/*.obj`, `previews/iso-*.png`,
   and `out/wand-caps-3d.html`.

## Per-shape lift choice

| Cap | Head | Mode | Reads as |
|---|---|---|---|
| A | leaf-blade spearhead | revolve | round spindle spearhead on a turned collar |
| B | crescent | hybrid | round collar + flat crescent, edge-tapered horns |
| C | trident | hybrid | round collar + three flat pronged tines |
| D | flame | revolve | round teardrop bulb drawn to a point |
| E | broadhead arrow | hybrid | round collar + flat broadhead with swept-back barbs |
| F | faceted spire | revolve | thin round double-cone spindle |
| G | fleur finial | hybrid | round collar + flat symmetric leaf flanked by barbs |

Rule of thumb: **round/turned head → revolve; flat forged head → hybrid** (so its
base is still a round cylinder). Every cap now has a cylindrical collar.

Guarantees enforced in the generator + verified per build: each cap is one
connected piece (no floating tips — 2D and 6-connected 3D), and every silhouette
is exactly symmetric top/bottom about the centreline.

## What was verified (headless)

- `python3 tests/smoke.py` passes (added a lift assertion block).
- Iso previews of all seven — geometry reads correctly (`previews/iso-all.png`).
- The WebGL viewer renders + all controls work, checked by headless-Chromium
  screenshots (model switch, material toggle, voxel-face inset, camera framing).

## What a human should eyeball

- Open `out/wand-caps-3d.html` (or the shared artifact) on a phone/desktop and
  spin each cap — confirm the inferred depth matches the intent per shape.
- Decide the collar treatment on the blade caps (B/C/E/G): the ferrule there is
  currently a flat-ish bar, not a turned cylinder (see "Known tradeoffs").
- Confirm the two family colours (AETHERIUM `#8A6BB6`, BRASS `#C79A55`).

## Known tradeoffs / next steps

- Voxel resolution follows the silhouette (~46×24). Bump the source canvas for
  finer models; the viewer/OBJ scale fine.
- Untextured by request. When texturing: the `.obj` UVs aren't authored yet;
  `aide autotex`/`aide model` cover the existing (JSON-model) texture path.
