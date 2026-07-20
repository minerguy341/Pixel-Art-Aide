"""Derived charts for the Chipped BLOCKS study. Draws only aggregate metrics
(variant counts, palette breadth, busyness, transparency, luminance) computed
from Chipped textures studied in the session scratchpad — NO Chipped pixels are
embedded or committed (see knowledge/reference-policy.md). Pillow only.
Run from repo root:  python3 gallery/2026-07-20-chipped-blocks-study/build_charts.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path("gallery/2026-07-20-chipped-blocks-study/previews")
OUT.mkdir(parents=True, exist_ok=True)

# --- arcane palette (matches the study design system) ---
GROUND=(23,19,30); PANEL=(32,26,43); PANEL2=(39,31,52); LINE=(51,42,68)
INK=(231,224,243); DIM=(169,159,192); ACCENT=(185,155,224); TEAL=(127,232,216)
BRASS=(199,154,85); ROSE=(224,140,150)
BASECOL={"cobblestone":(150,150,158),"terracotta":(150,96,72),"glass":(127,200,216),
         "glowstone":(224,196,110),"bookshelf":(150,110,70)}

def font(sz, bold=False):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()
F=font(15); FB=font(16); FS=font(12); FT=font(19)

def canvas(w,h):
    im=Image.new("RGB",(w,h),GROUND); return im, ImageDraw.Draw(im)
def text(d,xy,s,f=F,fill=INK,anchor="la"): d.text(xy,s,font=f,fill=fill,anchor=anchor)

# ---------- Chart 1: variants per base (Chipped scales by variant) ----------
def chart_scale():
    data=[("cobblestone",66),("bookshelf",33),("glass",21),("glowstone",20),("terracotta",17)]
    W,H=760,326; im,d=canvas(W,H)
    text(d,(28,22),"Decorative variants per base block",FT)
    text(d,(28,52),"a decorative mod scales by re-cutting ONE silhouette many ways — Chipped's core move",FS,fill=DIM)
    x0,top,bw,gap=210,92,66,26; maxv=66; span=W-x0-40
    for i,(name,n) in enumerate(data):
        y=top+i*(30+8)
        text(d,(x0-14,y+14),name,F,fill=INK,anchor="ra")
        w=int(span*n/maxv)
        d.rectangle([x0,y,x0+w,y+30],fill=BASECOL[name])
        text(d,(x0+w+10,y+14),str(n),FB,fill=INK,anchor="lm")
    text(d,(x0,top+5*38+6),"(counts are the full folder totals; a sample of each was studied for the metrics below)",FS,fill=DIM)
    im.save(OUT/"variant-scale.png")

# ---------- Chart 2: the design-lever heatmap ----------
# per-base median of four normalized levers; shows each material pulls a DIFFERENT lever
def chart_levers():
    # (base, palette_breadth cols, busyness, transparency%, luminance mean)
    rows=[("cobblestone",7,11,0,48),
          ("bookshelf",25,14,0,41),
          ("glass",10,18,20,53),
          ("glowstone",33,15,0,66),
          ("terracotta",42,2.7,0,21)]
    cols=[("palette\nbreadth","cols",lambda r:r[1],47),
          ("structure\n(busyness)","busy",lambda r:r[2],22),
          ("transparency","% clear",lambda r:r[3],54),
          ("luminance","L mean",lambda r:r[4],86)]
    W,H=760,360; im,d=canvas(W,H)
    text(d,(28,20),"One vocabulary, a different lever per material",FT)
    text(d,(28,50),"cells normalized per column; the hot cell in each row is that material's signature move",FS,fill=DIM)
    x0,y0,cw,ch,gap=190,110,124,40,6
    for j,(title,unit,_,_) in enumerate(cols):
        cx=x0+j*(cw+gap)+cw//2
        for k,ln in enumerate(title.split("\n")):
            text(d,(cx,y0-40+k*15),ln,FS,fill=TEAL,anchor="mm")
        text(d,(cx,y0-8),unit,FS,fill=DIM,anchor="mm")
    for i,r in enumerate(rows):
        y=y0+i*(ch+gap)
        text(d,(x0-14,y+ch//2),r[0],F,fill=INK,anchor="rm")
        for j,(_,_,get,mx) in enumerate(cols):
            v=get(r); t=min(1.0,v/mx)
            x=x0+j*(cw+gap)
            base=PANEL; hot=BASECOL[r[0]]
            col=tuple(int(base[c]+(hot[c]-base[c])*t) for c in range(3))
            d.rectangle([x,y,x+cw,y+ch],fill=col,outline=LINE)
            lab=f"{v:g}" if v==int(v) else f"{v:g}"
            text(d,(x+cw//2,y+ch//2),lab,FS,fill=INK if t>.35 else DIM,anchor="mm")
    im.save(OUT/"design-levers.png")

# ---------- Chart 3: palette cohesion range ----------
# color-count min..max per base — cobblestone locked tight, glowstone wildly variable
def chart_cohesion():
    data=[("cobblestone",6,8),("glass",9,11),("terracotta",35,47),
          ("bookshelf",12,32),("glowstone",11,147)]
    W,H=760,300; im,d=canvas(W,H)
    text(d,(28,22),"Palette cohesion — colour count spread within a base",FT)
    text(d,(28,52),"log axis · a tight bar = every variant reads as the same material; wide = sub-styles diverge",FS,fill=DIM)
    import math
    x0,top=190,100; span=W-x0-70; lo,hi=math.log10(5),math.log10(160)
    def X(v): return x0+int(span*(math.log10(v)-lo)/(hi-lo))
    for gx in (10,50,100):
        text(d,(X(gx),top-16),str(gx),FS,fill=DIM,anchor="mm")
        d.line([X(gx),top-4,X(gx),top+5*38],fill=LINE)
    for i,(name,a,b) in enumerate(data):
        y=top+i*38+14
        text(d,(x0-14,y),name,F,fill=INK,anchor="rm")
        d.line([X(a),y,X(b),y],fill=BASECOL[name],width=8)
        d.ellipse([X(a)-5,y-5,X(a)+5,y+5],fill=BASECOL[name])
        d.ellipse([X(b)-5,y-5,X(b)+5,y+5],fill=BASECOL[name])
        text(d,(X(b)+12,y),f"{a}–{b}",FS,fill=DIM,anchor="lm")
    im.save(OUT/"palette-cohesion.png")

if __name__=="__main__":
    chart_scale(); chart_levers(); chart_cohesion()
    print("charts ->", OUT)
