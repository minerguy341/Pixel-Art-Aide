# Wand tips — spear/arrowhead cross-section study (2026-07-21)

The first wand-cap set lifted every round head with a plain circular revolve,
which makes a spearhead read as a *blob*. Real spear and arrowhead tips are
never round in cross-section — so this set studies those forms and builds the
cross-sections into `aide.lift`, then designs six tips around them.

## What the study said (sources below)

- **Leaf / spear blades** are **lenticular** (a lens tapering to two sharp
  edges), usually with a raised **midrib** — a medial ridge that stiffens the
  blade like an I-beam while the thin lobes keep cutting edges.
- **Later thrusting points** (estoc-type) are **rhombic / diamond**: four flat
  facets, a central ridge, widest at the midpoint.
- **Bodkins** are a **square** (quadrangular) punch — mass concentrated to pierce
  armour, tapering to a fine point.
- **Broadheads** are **N thin blades radiating from the axis** (commonly 3 at
  120°) — the cross-section is a **Y**, not a solid; barbs sweep back from the base.

## What was implemented in the toolkit

`aide.lift` gained an axial **sweep engine** with a per-station cross-section,
plus a **radial** lifter:

| mode | cross-section | tip it makes |
|---|---|---|
| `lens` | flattened ellipse, sharp edges | flat leaf blade |
| `midrib` | lens + raised central spine | stiff leaf spearhead |
| `diamond` | rhombic, four facets + ridge | estoc / thrusting point |
| `square` | quadrangular | bodkin (armour-piercer) |
| `poly` | solid regular `sides`-gon | trilobate (3) / faceted spire (6) |
| `radial` | N fins at 360/N° (Y or +) | broadhead / winged pike |

`revolve` is now just `sweep(cross='round')`; `hybrid` takes a `head_mode`, so
every tip keeps a round turned collar (fits a wand core) welded to a forged head.

## The six tips (build_tips.py RECIPES)

| Tip | Head cross-section | Reads as |
|---|---|---|
| A leaf-spear | midrib (flat 0.42, ridge 0.55) | lenticular blade with a proud spine |
| B bodkin | square (flat 0.62) | quadrangular armour-piercing punch |
| C estoc | diamond (flat 0.60) | faceted rhombic thrusting point |
| D broadhead | radial (3 blades) | three-fin Y broadhead + rear barbs |
| E harpoon | lens (flat 0.40) | flat lenticular leaf with deep barbs |
| F winged | radial (4 blades) | four-fin `+` winged pike head |
| G trilobate | poly (sides 3) | solid triangular pyramidal 'Scythian' point |
| H swallowtail | lens (flat 0.42) | forked head, two tines + a forward V-notch |
| I winged-spear | midrib + stop-ring | boar spear: leaf blade with a round lug flange |
| J flamberge | diamond (flat 0.55) | flame blade, undulating edges |

## Everything so far, in one page

`gallery/build_showcase.py` builds `gallery/wand-showcase-3d.html` — a single
grouped viewer with all 17 models (the 7 caps + these 10 tips). That combined
page is the thing to publish/share; the two per-set viewers still build too.

## Smoothing

The viewer ships voxel *occupancy* and builds two surfaces in-browser: the crisp
cube shell and a **surface-nets** smooth skin (one relaxed vertex per boundary
cell + gradient normals) — a live **smooth ⇄ faceted** toggle (`aide.surface_nets`;
`aide lift --smooth` writes the smooth mesh as OBJ). Smoothing softens the crisp
cross-sections, so faceted mode is there when you want the sharp diamond/poly
edges back.

## Verified (headless)

- `python3 tests/smoke.py` passes (added sweep lens/diamond/midrib + radial +
  hybrid-head-mode assertions).
- Iso previews of all six (`previews/iso-all.png`) — cross-sections read.
- WebGL viewer screenshotted end-on: the 3-blade Y and 4-blade `+` sections and
  the leaf midrib are all clearly visible; no console errors.
- Each tip is a single connected 3D piece (radial hub welds to the collar).

## For a human to eyeball

- Spin each tip in `out/wand-tips-3d.html` (or the shared artifact); judge the
  `flat`/`ridge`/`blades` values against the look you want (all in
  `build_tips.py` RECIPES — cheap to retune and rebuild).
- Radial tips are intentionally *not* top/bottom symmetric (a broadhead isn't);
  say if you'd rather they were mirror-symmetric.

## Sources studied (general craft only; nothing committed)

- ACOUP, "The Mediterranean Iron Omni-Spear" — spear blade sections, midrib, fuller.
- Wikipedia, "Blade geometry" and "Bodkin point" — lenticular vs diamond; bodkin square section.
- Ancient Bronzes, "Anatomy of Ancient Arrowheads"; medievalhistoria.com arrowhead types.
- Vantage Point Archery / broadhead patents — 3-blade fixed-blade Y cross-section.
