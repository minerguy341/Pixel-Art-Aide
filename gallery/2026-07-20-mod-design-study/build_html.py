"""Build findings.html for the mod design study from findings-raw.md.
Collapsible <details> per category (page stays short) + per-mod cards.
Reference policy: idioms only; no mod pixels embedded. Run from repo root:
  python3 gallery/2026-07-20-mod-design-study/build_html.py
"""
import html, pathlib, re
G = pathlib.Path("gallery/2026-07-20-mod-design-study")
raw = (G / "findings-raw.md").read_text()

def inline(s):
    s = html.escape(s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"`(.+?)`", r"<code>\1</code>", s)
    s = re.sub(r"\[(.+?)\]\((.+?)\)", r'<a href="\2">\1</a>', s)
    return s

# --- parse ---
cats = []  # [{name, mods:[{name, fields:{}, sources:[]}], notes:[]}]
cur_cat = cur_mod = None
for line in raw.splitlines():
    if line.startswith("# CATEGORY:"):
        cur_cat = {"name": line.split(":", 1)[1].strip(), "mods": [], "notes": []}
        cats.append(cur_cat); cur_mod = None
    elif line.startswith("## ") and cur_cat is not None:
        cur_mod = {"name": line[3:].strip(), "fields": [], "sources": []}
        cur_cat["mods"].append(cur_mod)
    elif line.startswith("> ") and cur_cat is not None:
        cur_cat["notes"].append(line[2:])
    elif line.startswith("**") and cur_mod is not None:
        m = re.match(r"\*\*(.+?)\.\*\*\s*(.*)", line)
        if m:
            cur_mod["fields"].append((m.group(1), m.group(2)))
    elif line.startswith("- ") and cur_mod is not None and cur_mod["fields"]:
        k, v = cur_mod["fields"][-1]
        cur_mod["fields"][-1] = (k, v + "<br>• " + line[2:])

FIELD_ORDER = ["Meta", "Techniques", "Takeaways", "Signature", "Sources"]
CATCOLOR = {"Magic mods": "var(--accent)", "Decorative / block-family mods (wood-set guidance)": "var(--accent-2)",
            "Effects / apparatus grammar": "var(--brass)", "Mob / creature design": "var(--rose)",
            "UI / HUD / guidebook": "var(--accent-2)"}

CSS = """
:root{--ground:#17131E;--panel:#201A2B;--panel-2:#271F34;--ink:#E7E0F3;--ink-dim:#A99FC0;
 --line:#332A44;--accent:#B99BE0;--accent-2:#7FE8D8;--brass:#C79A55;--rose:#E08C96;
 --mono:ui-monospace,"SF Mono","JetBrains Mono",Menlo,monospace;
 --serif:"Iowan Old Style","Palatino Linotype",Palatino,Georgia,serif;
 --sans:system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;--measure:74ch;}
@media(prefers-color-scheme:light){:root{--ground:#EDE9DC;--panel:#F6F2E8;--panel-2:#EFEADC;
 --ink:#282034;--ink-dim:#665C7C;--line:#DBD3C3;--accent:#6C4CA0;--accent-2:#1F8F82;--brass:#8C6C30;--rose:#B4545E;}}
:root[data-theme="dark"]{--ground:#17131E;--panel:#201A2B;--panel-2:#271F34;--ink:#E7E0F3;--ink-dim:#A99FC0;--line:#332A44;--accent:#B99BE0;--accent-2:#7FE8D8;--brass:#C79A55;--rose:#E08C96;}
:root[data-theme="light"]{--ground:#EDE9DC;--panel:#F6F2E8;--panel-2:#EFEADC;--ink:#282034;--ink-dim:#665C7C;--line:#DBD3C3;--accent:#6C4CA0;--accent-2:#1F8F82;--brass:#8C6C30;--rose:#B4545E;}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);font-family:var(--sans);line-height:1.6;-webkit-font-smoothing:antialiased}
.wrap{max-width:min(920px,93vw);margin:0 auto;padding:0 20px 96px}
a{color:var(--accent);text-decoration:none;border-bottom:1px solid color-mix(in srgb,var(--accent) 35%,transparent)}
a:hover{border-bottom-color:var(--accent)}
header{padding:64px 0 34px;border-bottom:1px solid var(--line)}
.eyebrow{font-family:var(--mono);font-size:12px;letter-spacing:.22em;text-transform:uppercase;color:var(--accent-2);margin:0 0 16px}
h1{font-family:var(--mono);font-weight:600;font-size:clamp(26px,4.2vw,40px);line-height:1.15;margin:0 0 14px;text-wrap:balance}
h1 .g{color:var(--accent)}
.lede{font-family:var(--serif);font-size:clamp(17px,2.1vw,20px);max-width:64ch;margin:0 0 22px;color:var(--ink-dim)}
.meta{display:flex;flex-wrap:wrap;gap:8px 10px;font-family:var(--mono);font-size:12px}
.chip{border:1px solid var(--line);border-radius:2px;padding:4px 10px;color:var(--ink-dim);background:var(--panel)}
.chip b{color:var(--ink)}
.northstar{margin:26px 0 0;background:linear-gradient(180deg,var(--panel-2),var(--panel));border:1px solid var(--accent-2);border-radius:8px;padding:20px 24px}
.northstar h2{font-family:var(--mono);font-size:13px;letter-spacing:.14em;text-transform:uppercase;color:var(--accent-2);margin:0 0 12px}
.northstar ul{margin:0;padding-left:20px;display:grid;gap:8px}.northstar li{color:var(--ink-dim);font-size:15px}
.northstar b{color:var(--ink)}
details.cat{margin-top:18px;border:1px solid var(--line);border-radius:8px;background:var(--panel);overflow:hidden}
details.cat>summary{list-style:none;cursor:pointer;padding:18px 22px;display:flex;align-items:center;gap:12px;font-family:var(--serif);font-size:clamp(18px,2.4vw,23px);font-weight:600}
details.cat>summary::-webkit-details-marker{display:none}
.tw{font-family:var(--mono);font-size:12px;color:var(--ink-dim);margin-left:auto}
.caret{width:9px;height:9px;border-right:2px solid var(--accent);border-bottom:2px solid var(--accent);transform:rotate(-45deg);transition:transform .18s;flex:none}
details[open]>summary .caret{transform:rotate(45deg)}
.catbody{padding:4px 22px 22px}
.mod{border:1px solid var(--line);border-left:3px solid var(--barc,var(--accent));border-radius:6px;background:var(--panel-2);padding:16px 18px;margin-top:14px}
.mod h3{margin:0 0 4px;font-family:var(--mono);font-size:17px}
.lic{font-family:var(--mono);font-size:11px;color:var(--brass);border:1px solid color-mix(in srgb,var(--brass) 45%,transparent);border-radius:3px;padding:2px 7px;margin-left:8px;white-space:nowrap}
.mod p{margin:9px 0 0;font-size:14.5px;color:var(--ink-dim);max-width:var(--measure)}
.mod p .k{font-family:var(--mono);font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--accent-2);display:block;margin-bottom:2px}
.mod .sig{color:var(--ink)}
.note{margin-top:16px;background:var(--panel);border:1px dashed var(--brass);border-radius:6px;padding:14px 18px;font-size:14px;color:var(--ink-dim)}
.policy{margin-top:26px;background:var(--panel);border:1px solid var(--brass);border-radius:6px;padding:16px 20px;font-size:14px;color:var(--ink-dim)}
.policy b{color:var(--brass);font-family:var(--mono);font-size:12px;letter-spacing:.1em;text-transform:uppercase}
footer{margin-top:44px;padding-top:20px;border-top:1px solid var(--line);font-family:var(--mono);font-size:12px;color:var(--ink-dim)}
"""

NORTH = [
 "Keep blocks & mobs <b>vanilla-scale 16px and restrained</b> — magic is added on top, never by out-detailing the base game (Alex's/Mowzie's/Occultism).",
 "Spend the arcane budget on a <b>fixed per-aspect hue system</b> propagated through icons + particles + UI (Iron's Spellbooks) — we already have the 41-aspect palette.",
 "Reserve saturated colour for <b>additive glowing energy</b> — wisp particles over dark blocks, emissive cores on active apparatus, data-tintable per aspect (Malum/Embers/Cataclysm).",
 "Apparatus stay a <b>restrained neutral material</b> with framed-panel + rivet grammar (Create/Mekanism) so glow reads as the magic — sits beside Create without copying its brass.",
 "<b>Make invisible systems visible</b>: essentia/aura/mana as travelling glowing arcs & motes between blocks (Botania/Embers).",
 "Codex = Patchouli's <b>category → entry → node-graph with gated reveal</b>; Arcane Worktable = Ars Nouveau's <b>searchable palette + ordered slot chain + live vis-cost readout</b>; all on 1.21 nine-slice sprites.",
 "Wood sets: author only the <b>plank + ~4–5 new faces</b> (door, trapdoor, sign, boat); UV-map the plank through vanilla parents for the rest; one shared iron hardware ramp binds the family (Framed/Macaw's/Supplementaries).",
]

def lic_of(fields):
    for k, v in fields:
        if k == "Meta":
            m = re.search(r"License:\s*\*\*(.+?)\*\*", v)
            if m: return m.group(1)
    return ""

parts = []
for c in cats:
    color = CATCOLOR.get(c["name"], "var(--accent)")
    mods_html = []
    for mod in c["mods"]:
        lic = lic_of(mod["fields"])
        fld = []
        for k, v in mod["fields"]:
            cls = ' class="sig"' if k == "Signature" else ""
            fld.append(f'<p{cls}><span class="k">{html.escape(k)}</span>{inline(v)}</p>')
        licbadge = f'<span class="lic">{html.escape(lic)}</span>' if lic else ""
        mods_html.append(
            f'<div class="mod" style="--barc:{color}"><h3>{html.escape(mod["name"])}{licbadge}</h3>{"".join(fld)}</div>')
    notes = "".join(f'<div class="note">{inline(n)}</div>' for n in c["notes"])
    parts.append(
        f'<details class="cat"><summary><span class="caret"></span>{html.escape(c["name"])}'
        f'<span class="tw">{len(c["mods"])} mods</span></summary>'
        f'<div class="catbody">{"".join(mods_html)}{notes}</div></details>')

north = "".join(f"<li>{n}</li>" for n in NORTH)
HTML = f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mod design study — 38 mods for Thaumaturgy</title><style>{CSS}</style></head>
<body><div class="wrap">
<header>
  <p class="eyebrow">Pixel-Art-Aide · Design study · 2026-07-20</p>
  <h1>What the big mods do — <span class="g">38 mods</span> studied for Thaumaturgy</h1>
  <p class="lede">Design idioms from highly-downloaded mods that add UI, blocks, mobs, and effects — read for what a Thaumcraft successor should steal. Sections collapse; open one to read the per-mod breakdowns.</p>
  <div class="meta">
    <span class="chip"><b>38</b> mods</span><span class="chip"><b>11</b> categories</span>
    <span class="chip">magic·deco·effects·mobs·UI·storage</span>
    <span class="chip">study-only · <b>0</b> mod pixels used</span>
  </div>
  <div class="northstar"><h2>★ North star — the synthesis</h2><ul>{north}</ul></div>
</header>
{"".join(parts)}
<div class="policy"><b>Reference policy honoured</b><p style="margin:8px 0 0">Every mod was studied for its public, documented DESIGN idioms only — no mod's pixel art, models, or asset files were fetched, traced, or reproduced. Licenses are recorded per mod; all are treated as study-only regardless (several are ARR or copyleft). See <code>knowledge/reference-policy.md</code>.</p></div>
<footer><p>Pixel-Art-Aide · mod design study 2026-07-20 · compiled from parallel research passes into <code>findings-raw.md</code>.</p></footer>
</div></body></html>"""
(G / "findings.html").write_text(HTML)
print("wrote", G / "findings.html", len(HTML)//1024, "KB ·", sum(len(c["mods"]) for c in cats), "mods")
