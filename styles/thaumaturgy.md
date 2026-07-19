# Style: thaumaturgy

The art direction of *Thaumaturgy: The New Age* (`new_age_thaum`). Palettes
are copied verbatim from the mod's `docs/art-direction.md` (decided
2026-07-14) — **that document is the source of truth**; if it changes, update
this card to match, never the other way around.

## Identity

Vanilla + Create compatible magic. Textures must sit beside vanilla and
Create blocks without either side looking out of place: 16x16, saturation and
detail density **no higher than Create's**. Magic reads through hue pairings
and sparse accent glints, not through glow, noise, or high contrast.

- **Mid-value rule (hard)**: block albedo ~25–80% luminance per channel.
  Contrast comes from hue and texture, not extreme values.
- Two woods, two metals, cross-paired: warm pair greatwood+brass, cool pair
  silverwood+aetherium. Swapped pairings exist as decor variants.
- The teal accent `#7FE8D8` is the signature magic tell (silverwood shimmer,
  aetherium glint). Use it in *single pixels or 2px clusters*, never fields.
- GUI aspect art is the exception to 16x (HD hexagon icons); everything in
  this card concerns block/item textures.

## Palettes (verbatim from art-direction.md)

```palette greatwood_planks
shadow    = 5E4530
base      = 7A5B3C
highlight = 8F6E4B
```

```palette greatwood_bark
furrow    = 3A2D22
bark      = 4E3D2E
```

```palette silverwood_planks
shadow    = A8AC9D
base      = CFD3C4
highlight = E4E7DA
```

```palette silverwood_bark
streak    = AAB2AC
bark      = D9DED9
```

```palette brass
shadow    = 8F6B38
base      = C79A55
highlight = E8C983
```

```palette aetherium
shadow    = 5A4380
base      = 8A6BB5
highlight = B99BE0
glint     = 7FE8D8
```

```palette leaves
greatwood  = 3E6B2F
silverwood = A9D8C4
magic_glow = 7FE8D8
```

Aspect colors (for aspect-related items/particles) live in the mod's
`docs/aspects.md` — 6 primals + ~35 compounds, each with a fixed hex. Copy
the specific color needed into the .pxg palette at authoring time.

## Composition habits

- 3-step ramps above are *cores*: it is fine to add one deeper shadow or one
  intermediate step, staying inside the material's hue lane and the mid-value
  rule.
- Silverwood is pale: its "shadow" step is still light — do not deepen it to
  make shading easier; use hue (gray-green vs warm-gray) for separation.
- Gilded planks: metal trim is thin inlay banding Create-style — 1px metal
  lines with 1px shadow, not full metal borders.
- Aetherium always carries its teal glint somewhere; brass never does —
  the glint is what says "magic metal" instead of "plumbing".
- Busyness target: 3–8, same band as vanilla/Create.

## Consistency checklist

- [ ] All albedo luminance within ~25–80% (analyzer value range)
- [ ] Detail density ≤ Create's; no dithering fields
- [ ] Correct pairing grammar (warm/warm, cool/cool by default)
- [ ] Teal accent ≤ ~3% of opaque pixels, absent on non-magic materials
- [ ] Palettes match this card's hexes exactly for the core steps
- [ ] Blocks tile: seam ratio ≤ ~1.3, no loud landmark in the 3x3 preview
