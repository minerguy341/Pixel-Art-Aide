"""Assemble findings.html for the Chipped study. DERIVED data only — no Chipped
textures or models are embedded/committed (reference-policy.md). Run from root:
    python3 gallery/2026-07-19-chipped-study/build_html.py
"""
import base64, pathlib
G = pathlib.Path("gallery/2026-07-19-chipped-study")

def uri(name):
    return "data:image/png;base64," + base64.b64encode((G/"previews"/name).read_bytes()).decode()

CSS = """
:root{--ground:#17131E;--panel:#201A2B;--panel-2:#271F34;--ink:#E7E0F3;--ink-dim:#A99FC0;
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
.wrap{max-width:min(880px,92vw);margin:0 auto;padding:0 20px 96px}
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
section{margin-top:58px}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-dim);margin:0 0 6px}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(21px,2.9vw,29px);margin:0 0 10px;text-wrap:balance}
h2 .n{font-family:var(--mono);color:var(--accent);font-size:.6em;margin-right:.6em}
.intro{max-width:var(--measure);color:var(--ink-dim);margin:0 0 22px}
p{max-width:var(--measure)}
figure{margin:0 0 8px;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
figure img{display:block;width:100%;height:auto}
figcaption{padding:12px 18px;border-top:1px solid var(--line);font-size:13.5px;color:var(--ink-dim);font-family:var(--mono)}
.finds{display:grid;gap:13px;margin:20px 0 0;padding:0;list-style:none}
.finds li{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--accent);border-radius:4px;padding:14px 18px}
.finds .r{font-weight:600;margin:0 0 4px}
.finds .w{font-size:14.5px;color:var(--ink-dim);margin:0}
.pending{background:var(--panel-2);border:1px dashed var(--brass);border-radius:6px;padding:22px 24px}
.pending h2{margin-top:0}.pending .note{font-family:var(--mono);font-size:12.5px;color:var(--brass);margin:0 0 14px}
.pending ol{margin:0;padding-left:22px;display:grid;gap:9px}.pending li span{color:var(--ink-dim)}
.policy{margin-top:24px;background:var(--panel);border:1px solid var(--brass);border-radius:6px;padding:16px 20px;font-size:14px}
.policy b{color:var(--brass);font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
footer{margin-top:58px;padding-top:22px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--ink-dim)}
footer a{color:var(--ink-dim)}
"""

FINDS = [
 ("HD 64×64 textures — 4× vanilla.",
  "Every workbench ships one 64×64 texture atlas (texture_size [64,64]). Chipped spends resolution on smooth decorative detail where vanilla stays 16."),
 ("Real Blockbench furniture models, not cube variants.",
  "The seven workbenches are 9–30 box elements each (legs, apron, tabletop, tools) whose faces all UV-map onto the single 64×64 atlas — modelled tables, not textured cubes."),
 ("A themed workbench family: one table, re-dressed per profession.",
  "carpenter (saw/wood) · botanist (plants) · glassblower (kiln) · alchemy · loom · mason · tinkering — a shared table silhouette with profession props + a themed palette. The furniture analog of ‘one arrangement, many palettes’."),
 ("Furniture deliberately overhangs the block.",
  "The carpenter’s tabletop spans x 0→32; Chipped tables exceed the 16-cube for a fuller read (Minecraft allows element coords −16…32)."),
]

CANDIDATES = [
 ("Detailed furniture = a Blockbench multi-element model + one HD (32/64) texture atlas with non-overlapping UV islands — not a cube.",
  "the pattern to follow if the arcane worktable ever graduates from a cube to a modelled table."),
 ("A furniture family = one silhouette re-dressed per theme (props + palette).",
  "carpenter/botanist/glassblower share a table; the theme is the props and the colour, not the geometry — furniture’s one-arrangement-many-palettes."),
]

finds = "\n".join(f'<li><p class="r">{r}</p><p class="w">{w}</p></li>' for r,w in FINDS)
cand = "\n".join(f'<li>{r} <span>— {w}</span></li>' for r,w in CANDIDATES)

HTML = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chipped study — HD furniture models &amp; the renderer that ate them</title>
<style>{CSS}</style></head><body><div class="wrap">
<header>
  <p class="eyebrow">Pixel-Art-Aide · Model study · 2026-07-19</p>
  <h1>Chipped: <span class="g">HD furniture models</span>, and a renderer stress-test</h1>
  <p class="lede">Studied terrarium-earth/Chipped’s workbench textures and models — its decorative furniture is a step up in resolution and geometry from vanilla, which made it the perfect thing to throw at the studio’s model renderer.</p>
  <div class="meta">
    <span class="chip"><b>7</b> workbenches</span><span class="chip"><b>64×64</b> textures</span>
    <span class="chip"><b>9–30</b> elements each</span><span class="chip">CTM ignored · Fusion preferred</span>
    <span class="chip">study-only · <b>0</b> Chipped pixels/models committed</span>
  </div>
</header>

<section>
  <p class="kicker">What Chipped does</p>
  <h2><span class="n">01</span>Modelled furniture at 4× resolution</h2>
  <figure><img src="{uri('detail-ladder.png')}" alt="Detail ladder: vanilla 16px cube, BWG recoloured variant, Chipped 64px multi-element model"><figcaption>the furniture detail ladder — derived from the model files</figcaption></figure>
  <ul class="finds">{finds}</ul>
</section>

<section>
  <p class="kicker">The renderer stress-test</p>
  <h2><span class="n">02</span>What the model renderer could — and couldn’t — eat</h2>
  <p class="intro">The studio’s <code>render_model</code> took these real 64×64, up-to-30-element models straight from Chipped’s files, with fractional UVs and out-of-cube coordinates — good robustness. But it treats every element as axis-aligned, and 4 of the 7 workbenches use real 22.5°/45° element rotations, so those render only approximately.</p>
  <figure><img src="{uri('workbench-complexity.png')}" alt="Bar chart of element counts per workbench, coloured by whether the renderer handles it faithfully"><figcaption>element count per workbench — teal renders faithfully (axis-aligned), brass has 22.5/45° rotations the renderer approximates</figcaption></figure>
  <ul class="finds"><li><p class="r">Renderer verdict: faithful on angle-0 models, approximate on rotated ones.</p><p class="w">carpenter / glassblower / mason (angle 0) render true; botanist / alchemy / loom / tinkering tilt elements the renderer flattens. Real element rotation is the next renderer upgrade if we need it.</p></li></ul>
</section>

<section>
  <p class="kicker">The payoff for Thaumaturgy</p>
  <h2><span class="n">03</span>Our wood on the workbench</h2>
  <p class="intro">Because the renderer reads any model’s UVs, our own greatwood and silverwood planks map straight onto the workbench geometry — a live preview of what a <em>modelled</em> arcane worktable could look like, instead of today’s cube. (Shown to the user as a transient prototype: it borrows Chipped’s geometry, so a shippable T.N.A. worktable still needs our own model — but the concept renders.)</p>
</section>

<section>
  <div class="pending">
    <p class="kicker" style="color:var(--brass)">Proposed — pending your approval</p>
    <h2>Candidate lessons</h2>
    <p class="note">↳ Approve any and they join knowledge/lessons.md &amp; shading.md.</p>
    <ol>{cand}</ol>
  </div>
  <div class="policy">
    <b>Reference policy honoured</b>
    <p style="margin:8px 0 0">Chipped was studied from its public GitHub in the session scratchpad. This page embeds only derived data (element counts, texture sizes, the themed-family analysis) — no Chipped texture or model is rendered into it or committed. Study renders (their textures on their models, and our wood on their geometry) were shown to the user transiently and kept out of the repo. See <code>knowledge/reference-policy.md</code>.</p>
  </div>
</section>

<footer>
  <p>Pixel-Art-Aide · Chipped study 2026-07-19 · charts by <code>gallery/2026-07-19-chipped-study/build_html.py</code>.</p>
  <p style="margin-top:12px">Study source: <a href="https://github.com/terrarium-earth/Chipped">terrarium-earth/Chipped</a> (branch 1.21.x; studied locally, not redistributed).</p>
</footer>
</div></body></html>"""
(G/"findings.html").write_text(HTML)
print("wrote", G/"findings.html", len(HTML)//1024, "KB")
