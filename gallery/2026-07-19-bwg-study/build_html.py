"""Assemble findings.html for the BWG field study, embedding DERIVED charts
(palettes + stats — never BWG's pixels) as data URIs. Run from repo root:
    python3 gallery/2026-07-19-bwg-study/build_html.py
"""
import base64, pathlib
G = pathlib.Path("gallery/2026-07-19-bwg-study")

def uri(name):
    return "data:image/png;base64," + base64.b64encode((G/"previews"/name).read_bytes()).decode()

CSS = """
:root{ --ground:#17131E;--panel:#201A2B;--panel-2:#271F34;--ink:#E7E0F3;--ink-dim:#A99FC0;
  --line:#332A44;--accent:#B99BE0;--accent-2:#7FE8D8;--brass:#C79A55;
  --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--measure:70ch;}
@media(prefers-color-scheme:light){:root{--ground:#EDE9DC;--panel:#F6F2E8;--panel-2:#EFEADC;
  --ink:#282034;--ink-dim:#665C7C;--line:#DBD3C3;--accent:#6C4CA0;--accent-2:#1F8F82;--brass:#8C6C30;}}
:root[data-theme="dark"]{--ground:#17131E;--panel:#201A2B;--panel-2:#271F34;--ink:#E7E0F3;
  --ink-dim:#A99FC0;--line:#332A44;--accent:#B99BE0;--accent-2:#7FE8D8;--brass:#C79A55;}
:root[data-theme="light"]{--ground:#EDE9DC;--panel:#F6F2E8;--panel-2:#EFEADC;--ink:#282034;
  --ink-dim:#665C7C;--line:#DBD3C3;--accent:#6C4CA0;--accent-2:#1F8F82;--brass:#8C6C30;}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:min(900px,92vw);margin:0 auto;padding:0 20px 96px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
a:hover{border-bottom-color:var(--accent)}
:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px}
header{padding:70px 0 38px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-2);margin:0 0 18px}
h1{font-family:var(--mono);font-weight:600;font-size:clamp(27px,4.4vw,42px);line-height:1.14;letter-spacing:-.01em;margin:0 0 16px;text-wrap:balance}
h1 .g{color:var(--accent)}
.lede{font-family:var(--serif);font-size:clamp(17px,2.1vw,20px);max-width:60ch;margin:0 0 26px}
.meta{display:flex;flex-wrap:wrap;gap:8px 10px;font-family:var(--mono);font-size:12px}
.chip{border:1px solid var(--line);border-radius:2px;padding:4px 10px;color:var(--ink-dim);background:var(--panel)}
.chip b{color:var(--ink)}
section{margin-top:60px}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-dim);margin:0 0 6px}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(21px,2.9vw,29px);margin:0 0 10px;text-wrap:balance}
h2 .n{font-family:var(--mono);color:var(--accent);font-size:.6em;margin-right:.6em}
.intro{max-width:var(--measure);color:var(--ink-dim);margin:0 0 24px}
p{max-width:var(--measure)}
figure{margin:0 0 8px;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
figure img{display:block;width:100%;height:auto}
figcaption{padding:12px 18px;border-top:1px solid var(--line);font-size:13.5px;color:var(--ink-dim);font-family:var(--mono)}
.finds{display:grid;gap:13px;margin:22px 0 0;padding:0;list-style:none}
.finds li{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--accent);border-radius:4px;padding:14px 18px}
.finds .r{font-weight:600;margin:0 0 4px}
.finds .w{font-size:14.5px;color:var(--ink-dim);margin:0}
.pending{background:var(--panel-2);border:1px solid var(--accent-2);border-radius:6px;padding:22px 24px}
.pending.cand{border-style:dashed;border-color:var(--brass)}
.pending h2{margin-top:0}
.pending .note{font-family:var(--mono);font-size:12.5px;margin:0 0 14px}
.pending ol{margin:0;padding-left:22px;display:grid;gap:9px}
.pending li span{color:var(--ink-dim)}
.policy{margin-top:26px;background:var(--panel);border:1px solid var(--brass);border-radius:6px;padding:16px 20px;font-size:14px}
.policy b{color:var(--brass);font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
footer{margin-top:60px;padding-top:22px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--ink-dim)}
footer a{color:var(--ink-dim)}
"""

ADOPTED = [
 ("Distinct woods differ by value + hue, not structure",
  "23 of 25 BWG woods use exactly a 7-colour plank ramp; identity is where the ramp sits — value (ebony L7–20 vs white_mangrove L53–83) and hue. Add a wood by re-anchoring, not re-drawing grain."),
 ("Leaf hole density is a canopy-type lever",
  "Airy broadleaf run ~27–39% transparent; dense/weeping/coniferous run low (willow 9%, spirit 10%, mangrove/baobab 18%). Pick the % from the tree, not a default."),
 ("Leaf colour is an independent species axis",
  "Wood colour and leaf colour are decoupled — leaves needn’t be green (witch_hazel orange, skyris pink, jacaranda purple, zelkova red, aspen yellow). Flowering variants = plain leaf + sparse bright bloom accent."),
]

FLOWER_LESSON = (
  "A flowering plant’s palette decomposes into foliage + bloom + structural — author them as separate ramps.",
  "Classify pixels by hue/saturation before reading a palette: green = foliage, saturated non-green = bloom, near-grey = twig. Never aggregate a mixed category into one swatch — it hides the greens under whatever bloom is most common (here, jacaranda purple).")

CANDIDATES = [
 ("Transparency ≈ how much of the sprite is the object.",
  "solid ground 0–1%, ice ~8%, foliage 28–39%, cross-plants (flowers/cactus) 52–58%. Set alpha from the subject’s airiness, not a fixed value."),
 ("Material class reads from value + busyness together.",
  "sand = pale (L59–82) + calm (busy ~5); stone = mid (L50–75) + calm; foliage = darker + busier (~8–12). Two cheap dials place a material."),
 ("Natural ground & ripe fruit deliberately break the ‘few colours’ rule.",
  "dirt/mud/moss average 24 colours, fruit ~19 — many close tones for an organic/gradient read. ‘Few colours’ is for crafted/structured materials, not soil or ripening."),
 ("Cross-plant sprites are ~half transparent: green stem + bright bloom accent.",
  "flowers ~52% transparent, ~10 colours = stem greens + a small vivid petal cluster; the bloom is the only saturated thing."),
 FLOWER_LESSON,
]

def li(rows):
    return "\n".join(f'<li><p class="r">{r}</p><p class="w">{w}</p></li>' for r,w in rows)
adopted = li(ADOPTED)
cand = "\n".join(f'<li>{r} <span>— {w}</span></li>' for r,w in CANDIDATES)

HTML = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>BWG field study — what 994 textures taught the studio</title>
<style>{CSS}</style></head><body><div class="wrap">
<header>
  <p class="eyebrow">Pixel-Art-Aide · Field study · 2026-07-19</p>
  <h1>A biome’s worth of textures:<br>what <span class="g">Oh The Biomes We’ve Gone</span> taught us</h1>
  <p class="lede">994 textures studied for craft — 25 wood families and a whole biome of plants, stone, sand and fruit. Every finding here is derived data (palettes, transparency, busyness); none of the mod’s pixels were rendered or kept.</p>
  <div class="meta">
    <span class="chip"><b>994</b> textures</span><span class="chip"><b>25</b> wood types</span>
    <span class="chip"><b>3</b> lessons adopted</span><span class="chip"><b>5</b> candidate lessons</span>
    <span class="chip">study-only · <b>0</b> pixels committed</span>
  </div>
</header>

<section>
  <p class="kicker">The headline pattern</p>
  <h2><span class="n">01</span>Transparency encodes what a thing <em>is</em></h2>
  <p class="intro">Across every material class, the share of transparent pixels tracks how airy the object is — a single dial from solid rock to a wisp of a flower. It’s the cheapest signal of a material’s physical nature.</p>
  <figure><img src="{uri('transparency-by-class.png')}" alt="Bar chart: transparency by material class, stone 0% to cactus 58%"><figcaption>solid ground 0–1% · ice ~8% · foliage 28–39% · cross-plants 52–58% — derived from BWG, averaged per class</figcaption></figure>
</section>

<section>
  <p class="kicker">25 wood families</p>
  <h2><span class="n">02</span>Same grammar, re-anchored</h2>
  <p class="intro">Every wood is a tight ~7-colour plank ramp paired with a leaf ramp. What makes 25 trees feel distinct isn’t new structure — it’s where each ramp sits in value and hue, and a leaf colour that’s treated as a separate axis (often not even green).</p>
  <figure><img src="{uri('wood-palette-compare.png')}" alt="Palette comparison of 23 BWG woods: plank ramp vs leaf ramp and hole percentage"><figcaption>plank ramp vs leaf ramp + leaf hole %, sorted by wood hue — derived palettes, not the textures</figcaption></figure>
  <ul class="finds">{adopted}</ul>
</section>

<section>
  <p class="kicker">Material classes</p>
  <h2><span class="n">03</span>Value &amp; busyness place a material</h2>
  <p class="intro">Two cheap dials — where the value range sits and how busy the surface is — separate the classes cleanly. And two classes break the studio’s ‘few colours’ rule on purpose.</p>
  <figure><img src="{uri('class-palettes.png')}" alt="Aggregate palette and colour/busyness stats per material class"><figcaption>aggregate palette + avg colour-count · busyness per class — derived from BWG. Caveat: one aggregate swatch misrepresents a <em>mixed</em> category (see bushes below).</figcaption></figure>
  <ul class="finds">{li(CANDIDATES[1:3])}</ul>
</section>

<section>
  <p class="kicker">A correction — thanks to a sharp eye</p>
  <h2><span class="n">04</span>Split the plant, not the pile</h2>
  <p class="intro">The bush row above came out almost entirely purple, which is wrong for a “bush”. It’s an artefact: 13 of BWG’s 23 bushes are flowering jacaranda/allium/hydrangea variants, several of them <em>fully</em> purple, so a naive frequency count buries the green. Classify each pixel first — foliage (green), bloom (saturated non-green), structural (twig) — and the plant reads true: a green foliage ramp with a separate bloom accent.</p>
  <figure><img src="{uri('bush-split-palette.png')}" alt="Bush and flower palettes split into foliage, bloom, and structural ramps"><figcaption>each plant category split by pixel class — foliage (green) · bloom (flower) · structural (twig), with the share of pixels in each</figcaption></figure>
  <ul class="finds">{li([FLOWER_LESSON])}</ul>
</section>

<section>
  <div class="pending cand">
    <p class="kicker" style="color:var(--brass)">Proposed — pending your approval</p>
    <h2>Candidate lessons</h2>
    <p class="note" style="color:var(--brass)">↳ From the broad study. Approve any and they’ll join knowledge/lessons.md &amp; shading.md. Nothing here is committed yet.</p>
    <ol>{cand}</ol>
  </div>
  <div class="policy" style="margin-top:22px">
    <b>Reference policy honoured</b>
    <p style="margin:8px 0 0">The BWG zip was unpacked to the session scratchpad only. Everything above is derived analysis — palettes, percentages, averages — which is craft, not copyrightable pixel art. No BWG texture was rendered into this page, committed to either repo, or reproduced. See <code>knowledge/reference-policy.md</code>.</p>
  </div>
</section>

<footer>
  <p>Pixel-Art-Aide · BWG field study 2026-07-19 · charts generated by <code>gallery/2026-07-19-bwg-study/build_html.py</code> over textures in the scratchpad.</p>
  <p style="margin-top:14px">Source of study material: <a href="https://www.curseforge.com/minecraft/mc-mods/oh-the-biomes-weve-gone">Oh The Biomes We’ve Gone</a> (user-provided, studied locally; not redistributed).</p>
</footer>
</div></body></html>"""
(G/"findings.html").write_text(HTML)
print("wrote", G/"findings.html", len(HTML)//1024, "KB")
