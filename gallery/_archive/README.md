# Archived — Wand parts 3D study (2026-07-21)

An archived experiment: lifting 2D wand-part silhouettes into rotatable 3D voxel
models. Set aside, not active work.

**The reusable rendering tech is NOT here — it stays in the toolkit:**
`aide/lift.py` (silhouette → voxels: revolve / blade / hybrid / forged
cross-sections lens·diamond·square·midrib·poly / radial; surface-nets smoothing)
and `aide/liftviewer.py` (static iso preview + the self-contained WebGL viewer
with the faceted→mid→smooth slider). Those are covered by `tests/smoke.py` and
documented in the repo `CLAUDE.md`. Use `python3 -m aide lift …` to make new ones.

**What's archived here** — the generated outputs of the test:

| Dir / file | What |
|---|---|
| `2026-07-21-wand-caps/` | 7 caps lifted from the original concept art (A–G) |
| `2026-07-21-wand-tips-study/` | 10 forged spear/arrowhead tips (cross-section study) |
| `2026-07-21-fantasy-caps/` | 6 fantasy toppers (orb, crystal, starburst, moon, …) |
| `2026-07-21-pommels/` | 6 Oakeshott-family pommels (wheel, sphere, pear, …) |
| `capkit.py` | silhouette-authoring helpers shared by the fantasy/pommel sets |
| `build_showcase.py` | assembles all 29 models into one grouped viewer |
| `wand-showcase-3d.html` | the combined interactive gallery (build product) |

Each set dir keeps its own `NOTES.md`, `src/*.pxg`, `out/`, `previews/`.

Still runnable from the repo root, e.g. `python3 gallery/_archive/build_showcase.py`
(paths were rebased for the archived location); the toolkit it calls is unchanged.
