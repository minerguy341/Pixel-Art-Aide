# Every Compat (Wood Good) study — stored vs generated textures (2026-07-20)

User question: how many of Every Compat's textures are made on the fly vs stored
in the mod? Studied MehVahdJukaar/WoodGood (branch `1.21`, MC 1.21.1) from its
public GitHub in the session scratchpad per reference-policy.md — **no WoodGood
pixels are used or committed.** The mechanism diagram and resprite demo on the
findings page are drawn entirely from OUR own pixels/ramps; the charts show only
counts derived from the mod's public source.

## Answer: almost everything is generated at load; a small stored set seeds it

Every Compat's whole job is to add every wood-based block from many mods in every
installed wood type. It does this **at runtime**, not by shipping PNGs.

### The runtime pipeline (cited from source)

- `dynamicpack/ClientDynamicResourcesHandler extends
  moonlight...DynamicClientResourceProvider` — the mod IS a dynamically generated
  client resource pack, built after language load.
- `regenerateDynamicAssets()` collects a `ResourceGenTask` from every module
  (`EveryCompat.forAllModules(m -> m.addDynamicClientResources(...))`), then runs
  them **batched across all CPU cores**. It logs the real count at boot:
  `"Starting dynamic resources generation tasks: {N} in batches of {batchSize}"`.
- Each task uses Moonlight's **`Respriter`**: `Respriter.of(image)` — or
  `Respriter.masked(image, mask)` when a stored `_m` mask exists — takes the
  block's ORIGINAL texture and recolors it to a target **`Palette`**.
- The target palette is **read from the target wood's own planks/log texture**
  already present in the game — `PaletteStrategies.PLANKS_STANDARD`,
  `LOG_SIDE_STANDARD`, `PLANKS_REMOVE_DARKEST`, `SIGN_LIKE`, … (12 public
  strategies) via `Palette.fromAnimatedImage(plankTexture)`. Every Compat stores
  no wood palettes; it samples whatever wood mods the player installed.

So the color comes from textures already in the game, the shape/detail from a
small stored mask, and the recolor happens at boot — for every wood type × block
× module.

### What IS stored on disk (the seed set)

- **`_m` overlay masks** — measured a handful: 16×16, **1 colour, grayscale,
  51–98% transparent**. They mark the non-wood detail (books, saw, hinges) that
  must be composited back after the wood area is palette-swapped. One mask per
  block SHAPE, reused across all wood types and often all mods (`vanilla_`,
  `common_` prefixes). `everycomp/textures/block` = 43 base+mask PNGs in the root
  plus ~20 per-mod subfolders; there's also `recolorable_textures/`, and small
  `item/entity/model` sets.
- **277 hardcoded special-case registrations** (`addOptional(...)` /
  `registerSpecialTextureForBlock` in `CompatSpritesHelper`) — these are FIX-UPS,
  not content: a mod's source texture is the wrong size/format (joshua_log is
  8×8, twilightforest mangrove planks throws an index error, etc.), so a stored
  substitute is pointed at. The bulk of the file is patching edge cases so the
  automatic path works.
- **107 supported modules** (mod-registry.json) — the code that knows each mod's
  block set; not textures.

### Scale (illustrative)

Stored: ~dozens of masks + 277 fix-up registrations + 12 palette strategies — a
fixed, small number. Generated ≈ modules × wood-blocks-each × installed wood
types — with 60–200 wood mods that's ~50k–170k sprites, all at boot, none on
disk. The mod even injects into the `minecraft` and `quark` namespaces at runtime.

## Loop outcome

Textures WERE found (masks + fix-ups in `everycomp/textures` + the dynamicpack
generator), so the loop did not need to close-and-consult. Answer delivered as
`findings.html`.

## Relevance to us

Every Compat is the industrial version of our own lessons "one arrangement, many
palettes" and "distinct woods differ by value+hue, not structure" — it literally
recolors one arrangement to each wood's plank palette. The `Respriter.masked`
pattern (recolor the wood region, composite a stored detail mask on top) is
exactly the bookshelf/crafting-table split we already documented (frame = wood,
books/tools = separate accent). A candidate toolkit feature: an `aide resprite`
that palette-swaps a grayscale-masked base to a target wood ramp — the demo on
the page is a hand-rolled version of it.

## Candidate lessons (pending user approval)

1. Runtime respriting = recolor ONE base texture to a palette **sampled from the
   target wood's own planks**, compositing a small stored **detail mask** over
   the non-wood parts. Store masks (one per shape), not per-wood textures.
2. When automating a texture family, budget most of the work for **special-case
   fix-ups** (wrong-size/format source art), not the happy path — Every Compat is
   ~277 hand-coded exceptions around one generic recolor.
