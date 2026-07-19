# Fusion connected textures — reference

Studied 2026-07-19 from the Fusion wiki (git-cloned) and the FusionExamples
template PNGs (dimensions measured directly). Fusion by **SuperMartijn642**.

**Why this is in the studio's knowledge:** unlike OptiFine CTM (which we
flagged as out of scope), Fusion runs natively on **Fabric / Forge / NeoForge
/ Quilt** with one unified format — i.e. it works on Thaumaturgy's exact
loader stack (Fabric + NeoForge via Architectury). So Fusion is the *viable*
connected-textures path if T.N.A. ever wants CTM. It's still a **runtime mod
dependency** (client-side), so CTM is never a base-vanilla deliverable — a
Fusion tile-sheet is only meaningful when the Fusion mod is installed.

Links: GitHub https://github.com/SuperMartijn642/Fusion ·
wiki https://github.com/SuperMartijn642/Fusion/wiki ·
templates https://github.com/SuperMartijn642/FusionExamples/tree/main/templates ·
Modrinth https://modrinth.com/mod/fusion-connected-textures ·
CurseForge https://www.curseforge.com/minecraft/mc-mods/fusion-connected-textures

## Format (not ctm.properties, not .png.json)

Fusion piggybacks on vanilla `.mcmeta`. For `foo.png` you write
`foo.png.mcmeta` beside it with a `"fusion"` section; `type` selects behavior:

```
assets/<ns>/textures/block/<name>.png
assets/<ns>/textures/block/<name>.png.mcmeta   ← definition here
```

```json
{ "fusion": { "type": "connecting", "layout": "pieced",
              "connections": [ { "type": "is_same_block" } ] },
  "animation": { }  /* optional vanilla animation block */ }
```

Texture `type` values: `base` (emissive / render_type / tinting overrides,
shared by all), `connecting` (CTM), `continuous` (one image stretched over an
N×M block grid), `random` (pseudo-random tile per position), `scrolling`.
Types nest via `sub_texture` (e.g. a connecting texture whose tiles are each
`random`).

`pack.mcmeta` must declare the minimum Fusion version (numeric part only):

```json
{ "pack": { "pack_format": 34, "description": "…" },
  "fusion": { "min_version": "1.3.0" } }
```

Optional-dependency packing: set `fusion.overrides_folder` in `pack.mcmeta`
and mirror the `assets/…` tree inside it — those files load only when Fusion
is present, so the pack degrades gracefully without the mod.

## Connecting-texture schema

| key | values | default |
|---|---|---|
| `type` | `"connecting"` | — |
| `layout` | pieced · simple · full · vertical · horizontal · compact · overlay | `full` |
| `connections` | one predicate or an array of them | `is_same_state` |
| `sub_texture` | nested texture metadata | none |
| `per_tile_animation` | bool | false |
| + all `base` keys | emissive · render_type · tinting | — |

Connection predicates (evaluated per neighbor direction → a boolean the layout
consumes): `is_same_block`, `is_same_state` (default: same block+blockstate),
`match_block` (`block`/`blocks` array, `ignore_missing` for absent modded
IDs), `match_state` (+ required `properties`), `match_block_in_front` /
`match_state_in_front` (test the block on top of a neighbor), `is_direction`
(`top,top_right,right,bottom_right,bottom,bottom_left,left,top_left`),
`is_face_visible` (neighbor face not covered by opaque block), `and` / `or`
(`predicates`), `not` (`predicate`), `true` / `false`.

There is **no block-tag predicate** — enumerate blocks in `blocks: [...]` with
`ignore_missing: true`, combine with `and`/`or`/`not`.

## Tile-sheet layouts (1× = 16px/tile; sheet scales with pack res)

Tiles indexed left→right, top→bottom. Fully-transparent tiles are skipped and
not atlas-stitched, so unused slots can be left blank.

| layout | px (1×) | grid | tiles | connects | use |
|---|---|---|---|---|---|
| **pieced** | 80×16 | 5×1 | 5 | 8-way (approx) | **recommended starter** — composites corner pieces into borders; least art |
| **simple** | 64×64 | 4×4 | 16 | 4 cardinal | 2⁴ states, no diagonals |
| **full** | 128×96 | 8×6 | 48 | all 8 | classic "47-tile" CTM in 48 slots; inner corners/diagonals |
| **horizontal** | 64×16 | 4×1 | 4 | left/right | 2² states |
| **vertical** | 16×64 | 1×4 | 4 | up/down | 2² states |
| **compact** | 80×16 | 5×1 | 5 | pseudo | end/center/vertical/horizontal/cross — cheap connected look |
| **overlay** | 96×48 | 6×3 | 18 | 8-way overlay | composites over a base block (grime/borders), doesn't replace |

Runtime: for each visible face, Fusion evaluates `connections` for the up-to-8
neighbors *in that face's plane* → 8 booleans → the layout maps that pattern
to a tile (or composites sub-tiles per quadrant for pieced/overlay).

## Model-level alternative (`fusion:model`)

Put connection logic in a block model instead of the texture `.mcmeta`, so
different faces use different predicates:

```json
{ "loader": "fusion:model", "type": "connecting",
  "parent": "block/cube_all", "textures": { "all": "block/oak_tiles" },
  "connections": [ { "type": "is_same_block" },
                   { "type": "match_block", "block": "acacia_tiles" } ] }
```

A named form (`connections: {"blue":[...], "default":{...}}`) lets element
faces reference a set via `"connections": "#blue"`. The texture still needs
its connecting-layout `.png.mcmeta` for the tile sheet.

## Authoring rules

- A connecting sheet is **NOT one 16× tile tiled** — draw the seam/border set:
  interior fill, straight edges, outer corners, and (for `full`) inner
  concave corners.
- **Pick the smallest layout that reads.** Wiki recommends `pieced` (5) for
  beginners; use `simple` (16) if you only need cardinal edges; reserve `full`
  (48) for when diagonals/inner corners genuinely matter.
- Use the official template PNGs (+ `… border.png` guides) as the exact tile
  slotting reference — order is left→right, top→bottom.
- Keep every tile square and identical size; total sheet = grid × tile exactly
  (32× pack: full = 256×192, simple = 128×128, …).
- `overlay` is drawn as layers over the base block, not a replacement.
- Studio integration: this fits the "one arrangement, many palettes" and
  seamless-tiling lessons — a Fusion sheet is the *engine-assisted* version of
  the "2–3 variants to break wall repetition" rule, letting edges/corners
  resolve automatically instead of by random placement.

## Pitfalls

- Using OptiFine `ctm.properties` (Fusion ignores it) or a `.png.json`
  (wrong — it's `.png.mcmeta`).
- Wrong sheet dimensions (misaligns every tile).
- Forgetting `pack.mcmeta` → `fusion.min_version`.
- Forgetting Fusion must actually be installed (client-side); on Sodium < 0.6
  (Fabric) also needs **Indium**.

## 1.21.1 status (Fabric + NeoForge)

Supported. The `1.2.11`/`1.2.12` line covers MC 1.21–1.21.1 on both Fabric/
Quilt and NeoForge (and Forge) — pick the `mc1.21`/`mc1.21.1` artifact, not a
`mc1.21.9` build. Texture types (connecting/continuous/random/scrolling) are
stable across 1.2.x; custom *entity* models are flagged experimental. Fusion
ships separate Fabric and NeoForge jars consuming the **identical** pack
format, so one tile-sheet set works on both loaders — no per-loader branching.
Verify the exact latest `1.2.1x` build on the Modrinth files page before
pinning `min_version`.
