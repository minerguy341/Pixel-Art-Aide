# Campaign session: T.N.A. texture pass (standing /loop task)

See BACKLOG.md for the work list. This file logs per-iteration decisions and
TC-idiom comparisons (judged from knowledge — no TC assets fetched/used).

## Iteration 1 — 2026-07-19

Shipped to T.N.A. (`claude/texture-generation-prompts-qyp1w7`):

- `docs/art-direction.md` sync: greatwood plank ramp darkened to the
  approved TC-era values, recorded as a sanctioned mid-value exception.
- `block/greatwood_planks.png` — the approved r3_deeper from the
  greatwood-planks session (block not registered yet; asset staged).
- `block/arcane_orrery_{top,side,bottom}.png` + model swap `cube_all`
  (lodestone placeholder) → `cube_bottom_top`.

Orrery design decisions: dark greatwood casing; brass inlay band + corner
plates (Create-style framed faces); inset aetherium viewport / hub with
single teal glint. Analyzer: value warnings are the greatwood exception +
brass accents; bottom face pillow_r=0.47 is a false positive from the framed
composition (frame dark, field lighter — structural, not shading).

**TC comparison:** TC never had an orrery; the nearest reference is TC's
greatwood-and-gold arcane furniture. Verdict: our darker wood + brass +
aetherium version fits both the TC memory and the Create-adjacent direction;
chose it over a stone-based alternative (not drawn — wood casing better
matches the registered worktable/wand woodiness).

**Not verified in-game** (no build possible in this sandbox; model JSON is
schema-valid and uses only vanilla parents). Human smoke test: place the
orrery — faces should show brass ring top / banded side; check the hologram
still renders above the top face; greatwood_planks.png is staged for when
the block registers.

Next iteration: wand/stave UV remap + real grayscale wand_base (tint
regions rod=0 cap_a=1 cap_b=2), then codex + aetherlens + research papers.
