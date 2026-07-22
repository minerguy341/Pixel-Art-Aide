# MC-style cycle 2 — fix the per-pixel noise base (clustered blotches)

Acted on cycle 1's #1 finding: our stone bases were per-pixel `h2(x,y)` noise (the vanilla
anti-pattern — reads as TV static). Fixed it data-drivenly.

## What changed
- `stonegen.py`: added `_cluster_val(x,y,seed,cell)` — value noise sampled on a coarse `cell`-px
  grid with jittered cell edges, so light/dark patches form deliberate irregular **potato-shape
  blobs** (~2-3px, vanilla blotch size) instead of independent per-pixel speckle. `fill_base` reads
  a new `cluster` value from the spec (0 = legacy per-pixel, so nothing else changes). Foliation
  clusters along the grain.
- `stones.json`: set `cluster` per stone — marble 3, basalt 3, slate/shale/sandstone 2. All still
  tiling-safe (cell sampling wraps with the 16px grid via the same `h2`).
- `compare_cluster.py` + `cluster-compare.png`: side-by-side proof, old (per-pixel) vs new
  (clustered) for all six stones.

## Result (see cluster-compare.png and the re-rendered sheet-stones-gen.png)
- marble / slate / shale / basalt / sandstone: patches now cluster into readable blobs — the static
  "computer-generated" read is gone, blocks look hand-placed like vanilla stone. **Clear win.**
- granite: deliberately left per-pixel this cycle — its look is driven by the `apply_minerals`
  overlay (also per-pixel), not the base, so clustering only the base did little. Clustering the
  mineral scatter into 2-3px grains is the next candidate.

## Verified
- `python3 tests/smoke.py` → OK. Legacy `cluster:0` path is byte-unchanged (default), so no other
  session's stones move.
- Tiling: `_cluster_val` uses the same wrapping `h2`; 3x3 tiled renders show no seams.

## Not verified (needs a human eye)
- In-game read at real block scale / lighting. cluster-compare.png is a flat upscaled preview.

## Candidate lesson (for user approval — not yet written to lessons.md)
> **Procedural bases must cluster, not speckle.** A per-pixel `h2(x,y)` fill reads as TV static (the
> noise anti-pattern our own shading.md warns about). Sample base variation on a coarse 2-3px cell
> grid with jittered edges so value patches form deliberate potato-shape blobs — matches how vanilla
> stone is hand-placed. Keep it data-driven (`cluster` value) so cell size tunes per rock.

## Next cycle candidate
Cluster the granite mineral scatter (and any other per-pixel overlay: slate flecks are already
placed, but `apply_minerals` isn't). Then re-compare.
