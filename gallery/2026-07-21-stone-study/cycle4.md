# Mineral cycle 4 — ores & veins → ore-on-host sprite rules

Scope: how ore minerals actually occur in rock (vein / disseminated / massive), their colours, and
the Minecraft ore idiom → concrete rules for authoring ore blocks and arcane/vis ore.

## Findings
- **Ore = ore minerals + gangue, in a host rock.** Ore minerals (native gold/silver, sulfides
  galena/chalcopyrite/**pyrite**, oxides magnetite/cassiterite/hematite) are deposited **together with
  gangue** — the worthless quartz/calcite that surrounds them — inside a country/host rock.
- **Vein deposit** = a preexisting fracture/fissure **filled by circulating hydrothermal fluids** → a
  well-defined, usually **inclined, narrow band** of ore + quartz/calcite gangue cutting **across** the
  host rock.
- **Disseminated deposit** = ore scattered as **fine grains through** the host (porphyry copper,
  disseminated gold) — no single band.
- **Native/mineral colours are diagnostic**: gold yellow, silver white, copper green/red, pyrite brass,
  galena grey-metallic, magnetite black, hematite red, malachite green, cinnabar red.
- **Minecraft ore idiom**: a **dark host base + bright mineral fragments** clustered in it, **high contrast,
  sharp edges**, subtle glow — vanilla bakes the host stone into the ore texture (the transparent-overlay
  split is a mod pattern).

## Ore pixel lessons
1. **Ore = mineral clusters ON a copy of the host rock** — the host is most of the block, the mineral is
   the accent: paste 2–4 **clustered** mineral shapes onto the host stone, each **faceted** (highlight
   top-left + shadow bottom-right), high contrast, sharp edges. (Confirms the existing ore shorthand.)
2. **Hosting style is the arrangement axis** — **vein** (a diagonal/branching band cutting across, with a
   gangue halo) · **disseminated** (fine specks scattered through) · **massive** (one big clustered pocket).
   Pick from the deposit type; a vein reads distinctly richer than vanilla's scattered blobs.
3. **Ore colour codes the mineral** — use the real mineral's colour (gold=yellow, copper=green/red,
   pyrite=brass, magnetite=black, hematite/cinnabar=red, malachite=green); a fictional/arcane ore picks a
   plausible **saturated hue that beats the host value** (ties to accent-beats-the-border + aspect coding).
4. **A gangue halo sells "natural deposit"** — real vein ore sits in pale quartz/calcite; a thin **pale rim
   around the ore mineral** reads as grown-in rock, not a sticker slapped on. (New, grounded detail.)
5. **Contrast + sharp edges = ore readability** — dark host + bright mineral, sharp pixel edges, strong
   value gap so it reads at 16 px; reserve a **subtle glow** for magic/emissive ores only.

## For T.N.A.
Arcane / vis ore = **teal crystal clusters in cool blue-grey arcane stone** — a **vein** for a rich lode
or a **geode pocket** (cycle 3) for a node; the emissive glow is the "subtle glow" + UV-fluorescence hook
(cycle 3), and the teal `#7FE8D8` is the mineral colour-code. A pale quartz gangue halo keeps it grounded.

## Sources (study only)
- earthsci.org — vein deposits: https://earthsci.org/mineral/mindep/vein/vein.html ; ore deposit terms: https://earthsci.org/mineral/mindep/ore_def/ore_def.html
- Wikipedia — gangue: https://en.wikipedia.org/wiki/Gangue ; massive sulfide deposits: https://en.wikipedia.org/wiki/Massive_sulfide_deposits
- Geology In — veins & hydrothermal deposits: https://www.geologyin.com/2014/11/veins-and-hydrothermal-deposits.html
- Minecraft Wiki — Tutorial:Pixel art (ore/stone readability): https://minecraft.wiki/w/Tutorial:Pixel_art
