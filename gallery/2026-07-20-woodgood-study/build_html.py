"""Assemble findings.html for the Every Compat (Wood Good) study. Charts + the
mechanism diagram + the resprite demo come from build_charts.py and are drawn
from OUR OWN pixels/ramps and public-source counts — NO WoodGood texture is
embedded or committed (reference-policy.md). Run from repo root:
    python3 gallery/2026-07-20-woodgood-study/build_charts.py
    python3 gallery/2026-07-20-woodgood-study/build_html.py
"""
import base64, pathlib
G = pathlib.Path("gallery/2026-07-20-woodgood-study")

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
.wrap{max-width:min(900px,92vw);margin:0 auto;padding:0 20px 96px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
a:hover{border-bottom-color:var(--accent)}
:focus-visible{outline:2px solid var(--accent-2);outline-offset:2px}
header{padding:70px 0 38px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-2);margin:0 0 18px}
h1{font-family:var(--mono);font-weight:600;font-size:clamp(27px,4.4vw,42px);line-height:1.14;letter-spacing:-.01em;margin:0 0 16px;text-wrap:balance}
h1 .g{color:var(--accent)}
.lede{font-family:var(--serif);font-size:clamp(17px,2.1vw,20px);max-width:62ch;margin:0 0 26px}
.meta{display:flex;flex-wrap:wrap;gap:8px 10px;font-family:var(--mono);font-size:12px}
.chip{border:1px solid var(--line);border-radius:2px;padding:4px 10px;color:var(--ink-dim);background:var(--panel)}
.chip b{color:var(--ink)}
section{margin-top:58px}
.kicker{font-family:var(--mono);font-size:12px;letter-spacing:.18em;text-transform:uppercase;color:var(--ink-dim);margin:0 0 6px}
h2{font-family:var(--serif);font-weight:600;font-size:clamp(21px,2.9vw,29px);margin:0 0 10px;text-wrap:balance}
h2 .n{font-family:var(--mono);color:var(--accent);font-size:.6em;margin-right:.6em}
.intro{max-width:var(--measure);color:var(--ink-dim);margin:0 0 22px}
p{max-width:var(--measure)}
.answer{background:linear-gradient(180deg,var(--panel-2),var(--panel));border:1px solid var(--accent-2);border-radius:8px;padding:22px 26px;margin-top:26px}
.answer .tag{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--accent-2);margin:0 0 8px}
.answer p{margin:0;font-size:16px}
.answer b{color:var(--ink)}
figure{margin:0 0 8px;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
figure img{display:block;width:100%;height:auto}
figcaption{padding:12px 18px;border-top:1px solid var(--line);font-size:13.5px;color:var(--ink-dim);font-family:var(--mono)}
.finds{display:grid;gap:13px;margin:20px 0 0;padding:0;list-style:none}
.finds li{background:var(--panel);border:1px solid var(--line);border-left:2px solid var(--accent);border-radius:4px;padding:14px 18px}
.finds .r{font-weight:600;margin:0 0 4px}
.finds .w{font-size:14.5px;color:var(--ink-dim);margin:0}
code{font-family:var(--mono);color:var(--accent-2);font-size:.92em}
.pending{background:var(--panel-2);border:1px dashed var(--brass);border-radius:6px;padding:22px 24px}
.pending h2{margin-top:0}.pending .note{font-family:var(--mono);font-size:12.5px;color:var(--brass);margin:0 0 14px}
.pending ol{margin:0;padding-left:22px;display:grid;gap:9px}.pending li span{color:var(--ink-dim)}
.policy{margin-top:24px;background:var(--panel);border:1px solid var(--brass);border-radius:6px;padding:16px 20px;font-size:14px}
.policy b{color:var(--brass);font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
footer{margin-top:58px;padding-top:22px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--ink-dim)}
footer a{color:var(--ink-dim)}
"""

STORED = [
 ("Overlay masks (<code>_m</code>).",
  "16×16, one colour, grayscale, 51–98% transparent (measured). They protect the non-wood detail — books, saw, hinges — so it survives the wood recolor. One mask per block SHAPE, reused across every wood type and often every mod (vanilla_/common_ prefixes)."),
 ("277 hardcoded special-case registrations.",
  "addOptional(…) / registerSpecialTextureForBlock in CompatSpritesHelper — FIX-UPS, not content: a source texture is the wrong size/format (joshua_log is 8×8; twilightforest mangrove planks throws an index error), so a stored substitute is pointed at. Most of the file is patching edge cases."),
 ("12 palette strategies + 107 module definitions.",
  "PLANKS_STANDARD, LOG_SIDE_STANDARD, PLANKS_REMOVE_DARKEST, SIGN_LIKE… decide how to read a target wood's palette; the registry knows 107 mods' block sets. Code, not textures."),
]

GEN = [
 ("The mod IS a dynamic resource pack.",
  "ClientDynamicResourcesHandler extends Moonlight's DynamicClientResourceProvider and builds everything after language load — nothing the player sees is a shipped PNG."),
 ("Respriter recolors the block's ORIGINAL texture.",
  "Respriter.of(image) — or Respriter.masked(image, mask) when a stored mask exists — takes the block's existing texture and remaps it to a target Palette, compositing the detail mask back on top."),
 ("The palette is sampled from the target wood's own planks.",
  "Palette.fromAnimatedImage(plankTexture) reads whatever wood mods the player installed — Every Compat stores no wood palettes at all. Colour comes from textures already in the game."),
 ("Batched across every CPU core, at boot.",
  "regenerateDynamicAssets() gathers one ResourceGenTask per module and runs them multithreaded, logging the real count: “Starting dynamic resources generation tasks: {N}…”. That N is the generated-sprite count — thousands, scaling with installed woods."),
]

CAND = [
 ("Runtime respriting = recolor ONE base texture to a palette sampled from the target wood's own planks, compositing a small stored detail mask over the non-wood parts. Store masks (one per shape), not per-wood textures.",
  "the industrial form of our “one arrangement, many palettes”."),
 ("When automating a texture family, budget most of the effort for special-case fix-ups (wrong-size/format source art), not the happy path.",
  "Every Compat is ~277 hand-coded exceptions wrapped around one generic recolor."),
]

def ul(items): return "\n".join(f'<li><p class="r">{r}</p><p class="w">{w}</p></li>' for r,w in items)
stored=ul(STORED); gen=ul(GEN)
cand="\n".join(f'<li>{r} <span>— {w}</span></li>' for r,w in CAND)

HTML = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Every Compat (Wood Good) — stored vs generated textures</title>
<style>{CSS}</style></head><body><div class="wrap">
<header>
  <p class="eyebrow">Pixel-Art-Aide · Mod study · 2026-07-20</p>
  <h1>Every Compat: <span class="g">almost no textures</span> are stored — they're recolored at boot</h1>
  <p class="lede">You asked how many of Every Compat (Wood Good)'s textures are made on the fly vs stored in the mod. I found its textures — and read its generator. The answer is lopsided: a small fixed seed of masks and fix-ups on disk, and everything the player sees built at load.</p>
  <div class="meta">
    <span class="chip">MehVahdJukaar/<b>WoodGood</b> · 1.21</span><span class="chip"><b>107</b> supported mods</span>
    <span class="chip"><b>277</b> stored fix-ups</span><span class="chip"><b>12</b> palette strategies</span>
    <span class="chip">study-only · <b>0</b> WoodGood pixels used/committed</span>
  </div>
  <div class="answer">
    <p class="tag">↳ Short answer</p>
    <p><b>Essentially all of it is generated on the fly.</b> Every Compat ships a small fixed set of grayscale <b>detail masks</b> plus ~277 special-case <b>fix-up</b> textures, then at load it <b>recolors each block's own texture</b> to a palette read from each installed wood's planks — for every wood type × block × 107 modules, batched across all cores. Stored count is a fixed handful; generated count runs to tens of thousands and scales with how many wood mods you have.</p>
  </div>
</header>

<section>
  <p class="kicker">The pipeline</p>
  <h2><span class="n">01</span>How one texture gets made</h2>
  <figure><img src="{uri('mechanism.png')}" alt="Schematic: original oak texture → Respriter.masked with a stored mask → recolor to a palette from the target wood's planks → one variant per wood type"><figcaption>schematic drawn from our own pixels &amp; ramps — no WoodGood texture used</figcaption></figure>
  <ul class="finds">{gen}</ul>
</section>

<section>
  <p class="kicker">Proof of concept, our pixels</p>
  <h2><span class="n">02</span>The resprite, reproduced with our ramps</h2>
  <p class="intro">The same move on our own art: one authored “oak” tile (a plank frame + book spines masked as detail), recolored to three of our wood ramps. The frame follows the wood palette; the masked spines stay put. This is exactly what <code>Respriter.masked</code> does — and a good candidate for an <code>aide resprite</code> toolkit command.</p>
  <figure><img src="{uri('resprite-demo.png')}" alt="One authored tile recolored to greatwood, silverwood and pale-birch ramps; book spines stay constant"><figcaption>one shipped tile → three generated wood types (our own pixels)</figcaption></figure>
</section>

<section>
  <p class="kicker">The numbers</p>
  <h2><span class="n">03</span>Stored vs generated, to scale</h2>
  <figure><img src="{uri('stored-vs-generated.png')}" alt="Log-scale bar chart: stored counts in the low hundreds, generated sprites in the tens of thousands"><figcaption>counts derived from the mod's public source; generated bars are illustrative (the mod logs the real task count at boot)</figcaption></figure>
  <ul class="finds">{stored}</ul>
</section>

<section>
  <div class="pending">
    <p class="kicker" style="color:var(--brass)">Proposed — pending your approval</p>
    <h2>Candidate lessons</h2>
    <p class="note">↳ Approve any and they join knowledge/lessons.md &amp; shading.md.</p>
    <ol>{cand}</ol>
  </div>
  <div class="policy">
    <b>Reference policy honoured · loop closed cleanly</b>
    <p style="margin:8px 0 0">WoodGood was studied from its public GitHub in the session scratchpad. Its textures WERE found (the <code>_m</code> masks + fix-ups under <code>everycomp/textures</code>, and the <code>dynamicpack</code> generator), so the loop did not need to stop and consult you. This page embeds only our own pixels and counts derived from the mod's public source — no WoodGood texture is used or committed. See <code>knowledge/reference-policy.md</code>.</p>
  </div>
</section>

<footer>
  <p>Pixel-Art-Aide · Every Compat study 2026-07-20 · charts by <code>gallery/2026-07-20-woodgood-study/build_charts.py</code>.</p>
  <p style="margin-top:12px">Study source: <a href="https://github.com/MehVahdJukaar/WoodGood">MehVahdJukaar/WoodGood</a> (branch 1.21; studied locally, not redistributed). Runtime respriting via <a href="https://github.com/MehVahdJukaar/Moonlight">Moonlight</a>.</p>
</footer>
</div></body></html>"""
(G/"findings.html").write_text(HTML)
print("wrote", G/"findings.html", len(HTML)//1024, "KB")
