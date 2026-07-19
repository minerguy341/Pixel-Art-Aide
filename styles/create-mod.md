# Style: create-mod

The industrial-mechanical idiom of the Create mod. This card is a
**description generated from study of Create's published art**, not sampled
from its files — hex values are calibrated approximations of the idiom, and
this project ships only original art.

## Identity

Create reads as "vanilla's engineering sibling": the same 16x detail density
and softness as vanilla, but with a disciplined industrial materials kit —
kinetic stone (andesite), warm brass, bright copper, and dark oxidized iron
frames. Machines look *assembled*: plates, rivets, axles, frames around
faces, never freehand organic shapes.

- Geometry is rectilinear. Faces are framed: a 1px darker frame or chamfer
  around a machine face is the signature Create move.
- Moving parts are visually separated from casings by value contrast
  (light wooden/brass mechanism vs darker stone casing, or inverse).
- Highlights are restrained — metal shines by ramp contrast, not white pixels.
- Saturation ceiling matches vanilla; nothing candy-colored. Copper is the
  loudest thing in the kit and even it stays earthy.

## Palette rules

4–6 steps per material. Metals get harder step transitions than stone/wood.

```palette andesite_casing
deep     = 5F5B55
shadow   = 6E6A63
base     = 807C74
light    = 928E86
high     = A19D95
```

```palette brass
shadow   = 8F6B38
dark     = A87F44
base     = C79A55
light    = DBB56C
high     = E8C983
```

```palette copper
shadow   = 8C4E33
dark     = A65D3B
base     = C06E43
light    = D48355
high     = E09A6B
```

```palette dark_iron_frame
deep     = 3E3C42
shadow   = 4A484F
base     = 57555C
light    = 66646B
```

## Composition habits

- Machine block faces: outer 1px frame (frame ramp), inner field (casing
  ramp), one functional focal element (axle socket, gauge, hatch) centered
  or grid-aligned — never floating at an odd offset.
- Rivets/bolts: single highlight pixel over single shadow pixel, placed at
  frame corners; use sparingly (4 corners max on a 16x face).
- Brass/copper trim on other materials is thin inlay banding, 1px lines with
  a 1px shadow — not full borders.
- Busyness target: 4–9; frames and plates keep interiors calmer than stone.

## Consistency checklist

- [ ] Face framed or deliberately frameless (casing continues to the edge for tiling)
- [ ] Metals: ≤2 specular pixels per 16x face, no pure white
- [ ] Mechanical elements axis-aligned and centered on the grid
- [ ] Reads correctly next to both vanilla stone and Create andesite machinery
- [ ] Warm metals hue-shift toward red-brown in shadow, never gray
