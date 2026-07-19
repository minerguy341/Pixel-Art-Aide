"""Assemble findings.html for the study batch, embedding rendered PNGs as
data URIs (Artifact/standalone CSP blocks external images). Run from repo root:
    python3 gallery/2026-07-19-study-batch/build_html.py
"""
import base64, pathlib

G = pathlib.Path("gallery/2026-07-19-study-batch")


def uri(name: str) -> str:
    b = (G / "previews" / name).read_bytes()
    return "data:image/png;base64," + base64.b64encode(b).decode()


CSS = """
:root{
  --ground:#17131E; --panel:#201A2B; --panel-2:#271F34;
  --ink:#E7E0F3; --ink-dim:#A99FC0; --line:#332A44;
  --accent:#B99BE0; --accent-2:#7FE8D8; --brass:#C79A55; --before:#D98A8A;
  --mono:ui-monospace,"SF Mono","JetBrains Mono","Cascadia Code",Menlo,monospace;
  --serif:"Iowan Old Style","Palatino Linotype",Palatino,"Book Antiqua",Georgia,serif;
  --sans:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  --measure:72ch;
}
@media (prefers-color-scheme:light){
  :root{ --ground:#EDE9DC; --panel:#F6F2E8; --panel-2:#EFEADC;
    --ink:#282034; --ink-dim:#665C7C; --line:#DBD3C3;
    --accent:#6C4CA0; --accent-2:#1F8F82; --brass:#8C6C30; --before:#B25A5A; }
}
:root[data-theme="dark"]{ --ground:#17131E; --panel:#201A2B; --panel-2:#271F34;
  --ink:#E7E0F3; --ink-dim:#A99FC0; --line:#332A44;
  --accent:#B99BE0; --accent-2:#7FE8D8; --brass:#C79A55; --before:#D98A8A; }
:root[data-theme="light"]{ --ground:#EDE9DC; --panel:#F6F2E8; --panel-2:#EFEADC;
  --ink:#282034; --ink-dim:#665C7C; --line:#DBD3C3;
  --accent:#6C4CA0; --accent-2:#1F8F82; --brass:#8C6C30; --before:#B25A5A; }

*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);
  line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:min(920px,92vw);margin:0 auto;padding:0 20px 96px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
a:hover{border-bottom-color:var(--accent)}
:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px;border-radius:2px}

/* header */
header{padding:72px 0 40px;border-bottom:1px solid var(--line);margin-bottom:8px}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;
  color:var(--accent-2);margin:0 0 20px}
h1{font-family:var(--mono);font-weight:600;font-size:clamp(28px,4.6vw,44px);line-height:1.12;
  letter-spacing:-.01em;margin:0 0 18px;text-wrap:balance}
h1 .glint{color:var(--accent)}
.lede{font-family:var(--serif);font-size:clamp(17px,2.2vw,21px);color:var(--ink);
  max-width:60ch;margin:0 0 28px}
.meta{display:flex;flex-wrap:wrap;gap:8px 10px;font-family:var(--mono);font-size:12px}
.chip{border:1px solid var(--line);border-radius:2px;padding:4px 10px;color:var(--ink-dim);
  background:var(--panel)}
.chip b{color:var(--ink);font-weight:600}

section{margin-top:64px}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;
  color:var(--ink-dim);margin:0 0 6px}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(22px,3vw,30px);margin:0 0 10px;
  letter-spacing:-.01em;text-wrap:balance}
h2 .num{font-family:var(--mono);color:var(--accent);font-size:.6em;vertical-align:middle;margin-right:.6em}
.section-intro{max-width:var(--measure);color:var(--ink-dim);margin:0 0 28px}
p{max-width:var(--measure)}

/* before/after figure cards */
.demos{display:grid;gap:22px}
figure{margin:0;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
figure img{display:block;width:100%;height:auto;background:#141019}
figcaption{padding:16px 20px 18px;border-top:1px solid var(--line)}
.lesson-tag{font-family:var(--mono);font-size:11px;letter-spacing:.14em;text-transform:uppercase;
  color:var(--accent-2);margin:0 0 6px}
figcaption .t{font-family:var(--serif);font-size:18px;color:var(--ink);margin:0 0 6px}
figcaption p{font-size:14.5px;color:var(--ink-dim);margin:0;max-width:64ch}
figcaption .delta{font-family:var(--mono);font-size:12.5px;margin-top:10px;color:var(--ink)}
figcaption .delta .b{color:var(--before)} figcaption .delta .a{color:var(--accent-2)}

/* findings list */
.finds{display:grid;gap:14px;margin:0;padding:0;list-style:none}
.finds li{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--accent);
  border-radius:4px;padding:15px 18px}
.finds .rule{font-weight:600;color:var(--ink);margin:0 0 4px}
.finds .why{font-size:14.5px;color:var(--ink-dim);margin:0}
.finds .src{font-family:var(--mono);font-size:11.5px;margin-top:8px;color:var(--ink-dim)}
.flag{font-family:var(--mono);font-size:10.5px;letter-spacing:.1em;text-transform:uppercase;
  border:1px solid var(--brass);color:var(--brass);border-radius:2px;padding:1px 6px;margin-left:8px}

/* palette swatches for the studies */
.ramp{display:flex;gap:0;margin:14px 0 4px;border-radius:3px;overflow:hidden;border:1px solid var(--line);max-width:var(--measure)}
.ramp span{flex:1;height:34px;display:flex;align-items:flex-end;justify-content:center;
  font-family:var(--mono);font-size:9px;color:#0008;padding-bottom:2px}
.ramp-label{font-family:var(--mono);font-size:11px;color:var(--ink-dim);letter-spacing:.1em;text-transform:uppercase}

/* candidate lessons */
.pending{background:var(--panel-2);border:1px dashed var(--brass);border-radius:6px;padding:22px 24px}
.pending h2{margin-top:0}
.pending .note{font-family:var(--mono);font-size:12.5px;color:var(--brass);margin:0 0 16px}
.pending ol{margin:0;padding-left:22px;display:grid;gap:9px}
.pending li{color:var(--ink)} .pending li span{color:var(--ink-dim)}

footer{margin-top:72px;padding-top:24px;border-top:1px solid var(--line);
  font-family:var(--mono);font-size:12px;color:var(--ink-dim)}
footer a{color:var(--ink-dim)}
.srcgrid{columns:2;column-gap:32px;margin-top:12px}
@media(max-width:600px){.srcgrid{columns:1}}
.srcgrid a{display:block;break-inside:avoid;margin-bottom:6px;font-size:11.5px}
"""

DEMOS = [
    ("demo1-directional-cube.png", "Directional face shading",
     "Don’t bake a light gradient into a block",
     "The engine already multiplies each face by a fixed constant (top 1.0 · sides 0.8/0.6 · bottom 0.5). A texture that also shades itself top-bright / bottom-dark double-shades and reads muddy and over-contrasted.",
     "baked vertical gradient", "flat, engine does the shading"),
    ("demo2-stair-motif.png", "Multi-shape blocks (stairs / slabs)",
     "Keep the texture uniform — no centred hero motif",
     "Stairs and slabs reuse the parent block’s texture, cut across many small step faces. A centred knot or emblem fragments into meaningless slivers on the risers; uniform, tileable grain survives any cut.",
     "centred knot fragments on the steps", "even grain reads at every cut"),
    ("demo3-glass-frame.png", "Glass",
     "Thin 1px frame + streaks + empty interior",
     "Glass reads from the edge frame that outlines the cube plus a couple of specular streaks — not from a filled body. A thick frame over a filled interior reads as a solid framed box; leaving ~80% transparent is what makes it glass.",
     "thick frame, filled body → opaque box", "thin frame, transparent body → glass"),
    ("demo3b-alpha-bleed-mip.png", "Cutout edges at distance",
     "Alpha-bleed transparent pixels (mipmap fix)",
     "Simulated a few mip levels down: black stored under transparent pixels bleeds into the visible edge as the texture averages toward the horizon. Filling the transparent RGB with the neighbour colour keeps distant leaves clean.",
     "dark muddied edges at range", "clean colour at range"),
]

MC_FINDS = [
    ("Clear glass is <b>cutout</b> (binary alpha); stained glass is <b>translucent</b> (real blending).",
     "On the cutout layer any non-zero alpha pixel becomes fully opaque — you cannot soften clear-glass edges with partial alpha; only stained/tinted glass can dim what’s behind it.",
     "OptiFine render layers · NeoForge models"),
    ("The block-model <code>render_type</code> field is <b>NeoForge-only</b> in 1.21.1.",
     "Vanilla hard-codes render layers in Java and only added render_type to model JSON in 1.21.4 — a pure-vanilla pack can’t move clear glass to translucent on 1.21.1.",
     "MinecraftForge #10294 · NeoForge docs", "1.21.1"),
    ("Stairs & slabs author <b>nothing new</b> — they reuse the parent texture via model parents.",
     "The only implication is the full-face texture must survive being sub-sampled: keep it tileable and value-uniform so half-cuts and step faces read correctly.",
     "minecraft.wiki/Model · Tutorials/Models"),
    ("Vanilla ores <b>bake the stone in</b>; the stone+overlay split is a mod/pack pattern.",
     "For vanilla, paint clustered mineral (2–4 shapes, each highlight+shadow) directly onto a copy of the host stone — clusters read as a vein, scattered pixels read as noise.",
     "minecraft.wiki/Ore"),
    ("Runtime-tinted textures (redstone, grass, stems, lily pad) ship <b>grayscale</b>.",
     "Tint is a multiply, so author neutral and let the colour provider supply the hue — same rule that makes our grayscale wand template correct.",
     "minecraft.wiki/Model (tintindex)"),
]

CREATE_FINDS = [
    ("<b>Frame every machine face</b> — a 1px darker border around a lighter inner plate.",
     "The single strongest ‘this is Create’ tell; vanilla essentially never frames a face. Our brass/aetherium storage blocks already do this.",
     "Create GitHub texture tree"),
    ("Curate a <b>small material library</b>, each a narrow desaturated 3–4 value ramp.",
     "Cohesion comes from process consistency, not any single hue — a brass gear, an andesite casing and a copper tank read as one product line.",
     "Create GitHub · create.fandom (Casing)"),
    ("Restrain speculars — <b>highlights tinted toward the material, never pure white</b>.",
     "Small speculars only on relief edges (rivets, bands) give an industrial-matte read instead of glossy plastic. Matches our ‘no pure white’ metal rule.",
     "Create GitHub texture tree"),
    ("Detail is <b>structure, not noise</b>: corner rivets, banding, panel seams, connected panels.",
     "Organised man-made geometry over vanilla’s random dithering is what makes a block read as ‘assembled’ rather than ‘natural’.",
     "Create GitHub · Fusion connected textures"),
]

TC_TAKEAWAYS = [
    ("Two purples, opposite jobs", "a muted grey-violet for refined magic metal (our aetherium), a sickly magenta for corruption — never let them blend; the contrast is the brand."),
    ("Cool dressed stone as the backbone", "arcane masonry cleaner, lighter and more geometric than vanilla stone — ‘quarried by wizards’, not ‘mossy ruin’. (Our new arcane_stone follows this.)"),
    ("Warm brass for all instruments", "wands’ caps, scanners, distillation glass, piping — one gold-brown ‘Victorian-alchemy’ metal so tools feel like one kit against the cool stone."),
    ("Reserve emissive glow for the truly magical", "structural textures stay matte; glow only on nodes, runes, essentia and one shimmer-wood, so it always signals ‘power here’."),
    ("One icon shape + colour-coding", "they used the hexagon; a consistent colour-per-concept carries meaning across book, labels and UI — flat, minimal, glowing-outlined glyphs legible at 16px."),
    ("Encode order-vs-chaos in noise", "clean symmetrical textures for civilised magic; high-noise, veiny, asymmetric textures for corruption."),
]

CANDIDATES = [
    ("Glass = thin 1px frame + 1–2 specular streaks + ~80% transparent interior.", "clear glass on cutout / binary alpha; a thick filled frame reads as a solid box."),
    ("Stairs/slabs reuse the parent texture — keep it uniform & tileable, no centred motif.", "a hero knot fragments into slivers across the small step faces."),
    ("Clear glass = cutout, stained = translucent; render_type JSON is NeoForge-only on 1.21.1.", "can’t move clear glass to translucent from a pure-vanilla pack."),
    ("Vanilla ores bake stone in; cluster mineral (2–4 shapes) rather than scatter.", "stone+overlay is a mod pattern; scattered pixels read as noise."),
    ("Create idiom = framed faces + corner rivets + banding + curated desaturated ramps + tinted (never white) speculars.", "adopt the grammar, swap the material — inherit believability, stay distinct."),
    ("Thaumcraft grammar = two opposed purples, cool dressed stone, warm brass tools, glow reserved for the magical, one hexagon icon system, order-vs-chaos by noise level.", "evokes TC’s role without copying its assets."),
]

SOURCES = [
    ("minecraft.wiki — Model", "https://minecraft.wiki/w/Model"),
    ("minecraft.wiki — Ore", "https://minecraft.wiki/w/Ore"),
    ("minecraft.wiki — Texture atlas", "https://minecraft.wiki/w/Texture_atlas"),
    ("OptiFine — block render layers", "https://optifine.readthedocs.io/block_render_layers.html"),
    ("NeoForge — models (1.21.1)", "https://docs.neoforged.net/docs/1.21.1/resources/client/models/"),
    ("MinecraftForge — render_type #10294", "https://github.com/MinecraftForge/MinecraftForge/issues/10294"),
    ("Create — GitHub (Creators-of-Create)", "https://github.com/Creators-of-Create/Create"),
    ("Create Wiki — Casing", "https://create.fandom.com/wiki/Casing"),
    ("Create Wiki — Copper", "https://create.fandom.com/wiki/Copper"),
    ("FTB Wiki — Arcane Stone Block", "https://feed-the-beast.fandom.com/wiki/Arcane_Stone_Block"),
    ("Thaumcraft 4 Wiki — Silverwood", "https://thaumcraft-4.fandom.com/wiki/Silverwood"),
    ("Thaumcraft 4 Wiki — Thaumium", "https://thaumcraft-4.fandom.com/wiki/Thaumium"),
    ("Thaumcraft 4 Wiki — Aura Node", "https://thaumcraft-4.fandom.com/wiki/Aura_Node"),
    ("FTB Wiki — Aspects (TC4)", "https://ftb.fandom.com/wiki/Aspects_(Thaumcraft_4)"),
    ("Thaumcraft 4 Wiki — Taint", "https://thaumcraft-4.fandom.com/wiki/Taint"),
    ("Blockbench", "https://www.blockbench.net/"),
]


def finds_html(rows):
    out = []
    for r in rows:
        rule, why, src = r[0], r[1], r[2]
        flag = f'<span class="flag">{r[3]}</span>' if len(r) > 3 else ""
        out.append(f'<li><p class="rule">{rule}{flag}</p><p class="why">{why}</p>'
                   f'<p class="src">{src}</p></li>')
    return "\n".join(out)


def demos_html():
    out = []
    for img, tag, title, body, before, after in DEMOS:
        out.append(f"""<figure>
  <img src="{uri(img)}" alt="Before and after: {title}">
  <figcaption>
    <p class="lesson-tag">{tag}</p>
    <p class="t">{title}</p>
    <p>{body}</p>
    <p class="delta"><span class="b">before</span> {before} &nbsp;→&nbsp; <span class="a">after</span> {after}</p>
  </figcaption>
</figure>""")
    return "\n".join(out)


tc = "\n".join(f'<li><p class="rule">{t}</p><p class="why">{d}</p></li>' for t, d in TC_TAKEAWAYS)
cand = "\n".join(f'<li>{r} <span>— demonstrates: {w}</span></li>' for r, w in CANDIDATES)
srcs = "\n".join(f'<a href="{u}">{n}</a>' for n, u in SOURCES)

HTML = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Study Batch — Minecraft texturing, Thaumcraft &amp; Create</title>
<style>{CSS}</style>
</head>
<body>
<div class="wrap">
<header>
  <p class="eyebrow">Pixel-Art-Aide · Research log · 2026-07-19</p>
  <h1>Studying the neighbours:<br>Minecraft, <span class="glint">Thaumcraft</span> &amp; Create</h1>
  <p class="lede">A batch of texture-craft research turned into rules you can see. Each lesson is shown as a rendered block — the mistake on the left, the fix on the right.</p>
  <div class="meta">
    <span class="chip"><b>3</b> studies</span>
    <span class="chip"><b>4</b> before/after demos</span>
    <span class="chip"><b>3</b> new textures</span>
    <span class="chip"><b>6</b> candidate lessons <span style="color:var(--brass)">· pending approval</span></span>
    <span class="chip">target <b>MC 1.21.1</b> · Fabric + NeoForge</span>
  </div>
</header>

<section>
  <p class="kicker">The lessons, rendered</p>
  <h2>Before &amp; after</h2>
  <p class="section-intro">Every demo is a real texture rendered through the studio’s block renderer (exact vanilla face multipliers) or its mipmap-distance simulator — not a mock-up.</p>
  <div class="demos">
{demos_html()}
  </div>
</section>

<section>
  <p class="kicker">Made for this batch</p>
  <h2>New textures</h2>
  <p class="section-intro">Authored to demonstrate the lessons — an arcane glass (thin frame, teal-tinted), a cool blue-grey arcane stone in the Thaumcraft idiom, and greatwood stairs reusing the shipped plank texture.</p>
  <figure><img src="{uri('new-blocks-lineup.png')}" alt="Arcane glass, arcane stone, and greatwood stairs rendered as blocks"></figure>
</section>

<section>
  <p class="kicker">Study 01 · from minecraft.wiki, OptiFine, NeoForge</p>
  <h2><span class="num">01</span>Minecraft texture pipeline</h2>
  <p class="section-intro">Glass, stairs and ores — how the engine actually treats them, and two premises that turned out to be wrong.</p>
  <ul class="finds">
{finds_html(MC_FINDS)}
  </ul>
</section>

<section>
  <p class="kicker">Study 02 · from the FTB &amp; Thaumcraft wikis</p>
  <h2><span class="num">02</span>The Thaumcraft aesthetic</h2>
  <p class="section-intro">What made Thaumcraft <em>look</em> like Thaumcraft — studied to evoke the role, never to copy the pixels. Three colour families do the work:</p>
  <p class="ramp-label">Dignified violet (our aetherium) vs sickly taint magenta vs warm brass</p>
  <div class="ramp">
    <span style="background:#5A4380"></span><span style="background:#8A6BB5"></span><span style="background:#B99BE0"></span>
    <span style="background:#6B2E7A"></span><span style="background:#8A3A9C"></span><span style="background:#B65AC8"></span>
    <span style="background:#8F6B38"></span><span style="background:#C79A55"></span><span style="background:#E8C983"></span>
  </div>
  <p class="ramp-label" style="margin-top:16px">Cool dressed arcane stone · silverwood shimmer · teal glint</p>
  <div class="ramp">
    <span style="background:#5D5F68"></span><span style="background:#8A8D96"></span><span style="background:#B9BCC4"></span>
    <span style="background:#AFB7C4"></span><span style="background:#DCE0E6"></span><span style="background:#6FE0E6"></span>
    <span style="background:#7FE8D8"></span>
  </div>
  <ul class="finds" style="margin-top:26px">
{tc}
  </ul>
</section>

<section>
  <p class="kicker">Study 03 · from Create’s GitHub texture tree</p>
  <h2><span class="num">03</span>The Create idiom</h2>
  <p class="section-intro">So our magic blocks sit believably next to Create machinery. The trick: adopt the grammar, swap the material.</p>
  <ul class="finds">
{finds_html(CREATE_FINDS)}
  </ul>
</section>

<section>
  <div class="pending">
    <p class="kicker" style="color:var(--brass)">Not yet written to the knowledge base</p>
    <h2>Candidate lessons</h2>
    <p class="note">↳ Learning is user-gated. These are proposals distilled from this batch — approve the ones you want and they’ll be recorded in knowledge/lessons.md &amp; shading.md. Nothing here is committed yet.</p>
    <ol>
{cand}
    </ol>
  </div>
</section>

<footer>
  <p>Pixel-Art-Aide · study batch 2026-07-19 · rendered with <code>aide.blockrender</code> + <code>aide.bleed.mip_sim</code>. No Minecraft, Thaumcraft or Create assets were fetched, copied or committed — only silhouettes, structure and palette tendencies were studied.</p>
  <p class="kicker" style="margin-top:20px">Sources</p>
  <div class="srcgrid">
{srcs}
  </div>
</footer>
</div>
</body>
</html>"""

(G / "findings.html").write_text(HTML)
print("wrote", G / "findings.html", len(HTML), "bytes")
