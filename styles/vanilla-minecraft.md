# Style: vanilla-minecraft

The default style for anything meant to sit beside unmodified Minecraft
blocks. Modeled on modern vanilla (post–Texture-Update, 1.14+ "Jappa" idiom).

## Identity

- 16x16 base size. Calm, readable, mid-contrast. Nothing glows, nothing is
  near-black.
- **No outlines on blocks.** Items get a dark *border-shade* (a darkened
  edge of the material's own ramp, not pure black) on their silhouette.
- Detail via clusters, not noise: vanilla stone has ~5 colors and large,
  soft potato-shaped clusters. Emulate that density, not old-school 8-bit
  dithering.

## Palette rules

- 4–7 colors per material; whole texture usually under 10.
- Adjacent ramp steps ~8–12% luminance apart; subtle hue shift (8–20°),
  cool-ward in shadow.
- Saturation stays moderate (vanilla reads slightly desaturated next to most
  mod art). Block albedo luminance ~25–80%.

Reference ramps sampled from the vanilla idiom (approximations, for tone
calibration — not for copying textures):

```palette stone_like
deep     = 58524C
shadow   = 6B655F
base     = 7E7871
light    = 8F8A83
high     = 9D9891
```

```palette oak_like
shadow   = 5C4A2F
seam     = 6E5936
base     = 8A6D42
light    = 9C7E4D
high     = AF9256
```

```palette foliage_like
deep     = 2E4A1E
shadow   = 3E6428
base     = 4E7D31
light    = 60943C
```

## Composition habits

- Blocks: 2–3 medium features distributed for tiling; no single loud landmark.
- Items: strong silhouette first — if the 1x silhouette isn't readable, no
  amount of shading saves it. Border-shade the outside, light from top-left.
- Busyness target (analyzer metric): roughly 3–8 for blocks; flat crafted
  materials (planks, concrete) lower, organics higher.

## Consistency checklist

- [ ] Sits next to vanilla stone/planks without popping (saturation + value)
- [ ] No pure black, no pure white
- [ ] Blocks: seam ratio ≤ ~1.3 and no obvious repeat landmark in 3x3
- [ ] Items: readable silhouette at 1x, border-shade present, binary alpha
- [ ] Ramps hue-shift cool-ward in shadow
