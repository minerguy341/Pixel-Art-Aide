"""Assemble findings.html for the Chipped BLOCKS study. DERIVED data only — no
Chipped textures are embedded/committed (reference-policy.md). Charts come from
build_charts.py. Run from repo root:
    python3 gallery/2026-07-20-chipped-blocks-study/build_charts.py
    python3 gallery/2026-07-20-chipped-blocks-study/build_html.py
"""
import base64, pathlib
G = pathlib.Path("gallery/2026-07-20-chipped-blocks-study")

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
.fav{background:linear-gradient(180deg,var(--panel-2),var(--panel));border:1px solid var(--brass);border-radius:8px;padding:24px 26px}
.fav .tag{font-family:var(--mono);font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:var(--brass);margin:0 0 10px}
.fav h2{margin:0 0 8px}
.fav code{font-family:var(--mono);color:var(--accent-2)}
.pending{background:var(--panel-2);border:1px dashed var(--brass);border-radius:6px;padding:22px 24px}
.pending h2{margin-top:0}.pending .note{font-family:var(--mono);font-size:12.5px;color:var(--brass);margin:0 0 14px}
.pending ol{margin:0;padding-left:22px;display:grid;gap:9px}.pending li span{color:var(--ink-dim)}
.policy{margin-top:24px;background:var(--panel);border:1px solid var(--brass);border-radius:6px;padding:16px 20px;font-size:14px}
.policy b{color:var(--brass);font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
footer{margin-top:58px;padding-top:22px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--ink-dim)}
footer a{color:var(--ink-dim)}
"""

SIM = [
 ("Scale by variant — one block, dozens of cuts.",
  "The whole mod is “vanilla block → many decorative cuts, picked in a chiseling GUI.” cobblestone alone ships 66 variants; bookshelf 33, glass 21, glowstone 20, terracotta 17."),
 ("Palette fidelity — the redesign is structural, never chromatic.",
  "Variants inherit the source block’s palette and value range. A base reads as one material even across 66 cuts — cobblestone stays locked at 6–8 colours the whole way."),
 ("A shared pattern vocabulary reused on every material.",
  "bricks · tiles · pillar/column · chiseled · smooth/polished · carved/engraved/inscribed — plus the playful cobblestone face set (angry/sad/glad/unamused + creeper/spider/runic). The same nouns recur folder to folder: a house style, not per-block improvisation."),
 ("Vanilla resolution — the opposite of the workbenches.",
  "Nearly every block is 16×16 palette-mode (one 32×32 outlier). Chipped spends HD + geometry on furniture; on building blocks it spends only arrangement. Two products, one mod."),
]

LEVERS = [
 ("cobblestone / stone", "structure only", "Locked ~7-colour palette, busyness 7–14 — all variation is layout: bricks, tiles, pillars, carvings, faces."),
 ("terracotta", "relief on a noisy ground", "35–47 near-colours (the mottled base) but near-flat busyness 2–3.5 — gentle patterns pressed into an already-busy surface. Recolours 1:1 across all 16 dyes."),
 ("glass", "the alpha IS the design", "~10 colours but 6–54% transparent: leaded muntins / oak frames over clear panes. The only class whose pattern is made of holes."),
 ("glowstone", "luminance", "Brightest class (L mean up to 86) and widest palette spread (11–147): smooth photo-gradient glow vs structured lantern framing."),
 ("bookshelf", "object arrangement", "Books/webs/glow rearranged; 12–32 colours. oak_webbed drops to 12 (sparse cobweb)."),
]

CAND = [
 ("A decorative block family = one fixed source palette, variation carried by structure (brick/tile/pillar/carve) — not by new colours, so any two variants sit together without clashing.",
  "the opposite discipline from a hero texture; the rule for building out T.N.A.’s stone/wood detail sets."),
 ("Match the design lever to the material: opaque stone → rearrange structure on a locked palette; coloured ceramic → subtle relief; glass → pattern in the alpha; emissive → push luminance.",
  "one vocabulary, a different knob per material class."),
 ("Keep decorative building blocks at base resolution (16); reserve HD + models for furniture/hero pieces.",
  "resolution is a budget — spend it where the eye lingers, not on wallpaper."),
]

sim  = "\n".join(f'<li><p class="r">{r}</p><p class="w">{w}</p></li>' for r,w in SIM)
lev  = "\n".join(f'<li><p class="r">{n} — <span style="color:var(--accent-2)">{k}</span></p><p class="w">{w}</p></li>' for n,k,w in LEVERS)
cand = "\n".join(f'<li>{r} <span>— {w}</span></li>' for r,w in CAND)

HTML = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chipped blocks — one vocabulary, a lever per material</title>
<style>{CSS}</style></head><body><div class="wrap">
<header>
  <p class="eyebrow">Pixel-Art-Aide · Blocks study · 2026-07-20</p>
  <h1>Chipped’s blocks: <span class="g">one vocabulary</span>, a different lever per material</h1>
  <p class="lede">Where the workbenches were HD models, the decorative blocks are the opposite discipline — 16×16, palette-locked, and scaled by the dozen. Studied five bases (cobblestone, bookshelf, glass, glowstone, terracotta) for how their similarities and differences actually work.</p>
  <div class="meta">
    <span class="chip"><b>5</b> bases sampled</span><span class="chip"><b>66</b> cobblestone cuts</span>
    <span class="chip"><b>16×16</b> vanilla-res</span><span class="chip">CTM ignored · Fusion preferred</span>
    <span class="chip">study-only · <b>0</b> Chipped pixels committed</span>
  </div>
</header>

<section>
  <p class="kicker">The shape of the mod</p>
  <h2><span class="n">01</span>Scale by variant</h2>
  <figure><img src="{uri('variant-scale.png')}" alt="Bar chart of decorative variant counts per base block"><figcaption>folder totals — a decorative mod scales by re-cutting one silhouette many ways</figcaption></figure>
  <ul class="finds">{sim}</ul>
</section>

<section>
  <p class="kicker">Same nouns, different knob</p>
  <h2><span class="n">02</span>A different design lever per material</h2>
  <p class="intro">The vocabulary (bricks, tiles, pillars, carvings) is shared — but which property does the visual work changes with the material. Each cell below is normalized down its column; the hot cell in a row is that material’s signature move.</p>
  <figure><img src="{uri('design-levers.png')}" alt="Heatmap of palette breadth, busyness, transparency and luminance per base"><figcaption>palette breadth · structure · transparency · luminance — derived medians per base</figcaption></figure>
  <ul class="finds">{lev}</ul>
</section>

<section>
  <p class="kicker">Why the variants never clash</p>
  <h2><span class="n">03</span>Palette cohesion</h2>
  <p class="intro">The reason a builder can mix 66 cobblestone cuts freely: the palette never moves. Colour-count spread within a base measures it — a tight bar means every variant reads as the same stone; a wide bar means the base grew genuine sub-styles (glowstone’s smooth-glow vs lantern split blows it open to 11–147).</p>
  <figure><img src="{uri('palette-cohesion.png')}" alt="Range chart of colour-count spread within each base block"><figcaption>colour-count min–max per base (log axis)</figcaption></figure>
</section>

<section>
  <p class="kicker">In-world / in-game</p>
  <h2><span class="n">04</span>How they’re actually used</h2>
  <p>Cuts are chosen from Chipped’s chiseling bench — a GUI grid of variants for whatever block you insert. Fixed-palette stone and terracotta cuts tile seamlessly and swap freely: pure build-detailing that never clashes because the palette never moves. Pillars and columns read as structural framing, leaded-glass variants are windows, glowstone lanterns are light fixtures, and the face carvings are accents and easter-eggs. The whole point is <em>granular, palette-safe detail</em> — reach for a different cut without ever introducing a new colour.</p>
</section>

<section>
  <div class="fav">
    <p class="tag">★ My favourite</p>
    <h2><code>runic_carved_cobblestone</code></h2>
    <p>The thesis of the mod in one 16×16, 7-colour tile: zero palette drift from vanilla cobblestone, all the character carried by an engraved rune motif. It’s the most restrained kind of decoration — it just reads as “old, purposeful stone” — and it’s the one cut that would drop straight into <strong>Thaumaturgy’s arcane stonework</strong> with no recolour at all. Runner-up: the leaded-glass window family, for making the whole design out of alpha.</p>
  </div>
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
    <p style="margin:8px 0 0">Chipped’s blocks were studied from its public GitHub in the session scratchpad. This page embeds only derived aggregates (variant counts, colour-count spread, busyness/transparency/luminance medians) — no Chipped texture is rendered into it or committed. See <code>knowledge/reference-policy.md</code>.</p>
  </div>
</section>

<footer>
  <p>Pixel-Art-Aide · Chipped blocks study 2026-07-20 · charts by <code>gallery/2026-07-20-chipped-blocks-study/build_charts.py</code>.</p>
  <p style="margin-top:12px">Study source: <a href="https://github.com/terrarium-earth/Chipped">terrarium-earth/Chipped</a> (branch 1.21.x; studied locally, not redistributed).</p>
</footer>
</div></body></html>"""
(G/"findings.html").write_text(HTML)
print("wrote", G/"findings.html", len(HTML)//1024, "KB")
