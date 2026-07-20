"""Derived charts + a schematic mechanism diagram + an ORIGINAL resprite demo for
the Every Compat (Wood Good) study. No WoodGood pixels are used or committed
(reference-policy.md): the mechanism diagram and the resprite demo are drawn from
our OWN pixels/ramps; the charts show only counts derived from the mod's public
source (registry size, hardcoded-sprite count, palette-strategy count).
Run from repo root:
    python3 gallery/2026-07-20-woodgood-study/build_charts.py
"""
import math, pathlib
from PIL import Image, ImageDraw, ImageFont

OUT = pathlib.Path("gallery/2026-07-20-woodgood-study/previews")
OUT.mkdir(parents=True, exist_ok=True)

GROUND=(23,19,30); PANEL=(32,26,43); PANEL2=(39,31,52); LINE=(51,42,68)
INK=(231,224,243); DIM=(169,159,192); ACCENT=(185,155,224); TEAL=(127,232,216)
BRASS=(199,154,85); ROSE=(224,140,150)

def font(sz):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p, sz)
        except Exception: pass
    return ImageFont.load_default()
F=font(15); FS=font(12); FT=font(19); FB=font(16)
def canvas(w,h): im=Image.new("RGB",(w,h),GROUND); return im, ImageDraw.Draw(im)
def text(d,xy,s,f=F,fill=INK,anchor="la"): d.text(xy,s,font=f,fill=fill,anchor=anchor)

# ---- ramps (OURS — from the thaumaturgy card family; used for the demo) ----
SRC   =[(60,44,32),(92,66,44),(120,88,56),(150,112,72),(178,140,96)]   # generic oak-ish source
GREAT =[(38,26,34),(66,44,54),(96,66,74),(128,92,96),(160,120,120)]     # greatwood (purple-brown)
SILVER=[(60,70,86),(92,104,120),(126,140,156),(160,176,190),(200,214,224)] # silverwood (cool grey-blue)
BIRCHY=[(120,104,74),(160,142,104),(196,180,140),(220,208,176),(240,232,208)] # pale
BOOK  =[(150,40,40),(40,90,150),(200,170,60),(60,140,80)]               # book-spine accents (stay via mask)

# ================= 1. schematic mechanism diagram =================
def _tile(ramp, mask_books):
    """our own 16x16 'bookshelf-ish' tile: plank frame (recolorable) + book row
    (kept via mask). Returns (img, mask) where mask marks the KEPT detail."""
    im=Image.new("RGBA",(16,16),(0,0,0,0)); px=im.load()
    mk=Image.new("RGBA",(16,16),(0,0,0,0)); mp=mk.load()
    for y in range(16):
        for x in range(16):
            # frame: outer ring + central divider -> plank ramp by simple shade
            frame = x in (0,15) or y in (0,7,8,15)
            if frame:
                idx = 1 if (x+y)%3 else 2
                px[x,y]=ramp[idx]+(255,)
            else:
                # book rows (two shelves) -> accent spines, marked in mask
                shelf = 0 if y<7 else 1
                spine=(x*7+shelf*3)%4
                col=BOOK[spine]
                px[x,y]=col+(255,)
                if mask_books: mp[x,y]=(255,255,255,255)
    return im, mk

def _recolor(base, mask, src, dst):
    """map base's src-ramp pixels to dst ramp by nearest src index; keep masked."""
    out=base.copy(); bp=base.load(); op=out.load(); mp=mask.load()
    def nearest(c):
        best,bi=1e9,0
        for i,s in enumerate(src):
            d=sum((c[k]-s[k])**2 for k in range(3))
            if d<best: best,bi=d,i
        return bi
    for y in range(16):
        for x in range(16):
            c=bp[x,y]
            if c[3]==0: continue
            if mp[x,y][3]>0: continue          # masked detail kept as-is
            op[x,y]=dst[nearest(c)]+(255,)
    return out

def mechanism():
    s=8
    W,H=980,352; im,d=canvas(W,H)
    text(d,(28,20),"How Every Compat makes a texture — at load, not on disk",FT)
    text(d,(28,50),"schematic, drawn from our own pixels & ramps — no WoodGood texture is used",FS,fill=DIM)
    base,mask=_tile(SRC, True)
    def paste(img,x,y,sc=s):
        big=img.resize((16*sc,16*sc),Image.NEAREST)
        d.rectangle([x-2,y-2,x+16*sc+1,y+16*sc+1],fill=PANEL2,outline=LINE)
        im.paste(big,(x,y),big)
    def arrow(x0,x1,y,label,sub=None):
        d.line([x0,y,x1-8,y],fill=ACCENT,width=2)
        d.polygon([(x1,y),(x1-10,y-5),(x1-10,y+5)],fill=ACCENT)
        text(d,((x0+x1)//2,y-22),label,FS,fill=ACCENT,anchor="mm")
        if sub: text(d,((x0+x1)//2,y-8),sub,FS,fill=DIM,anchor="mm")
    y0=100; cy=y0+16*s//2; tile=16*s
    # 1 base
    paste(base,40,y0)
    text(d,(40,y0+tile+8),"1 · mod's own oak",FS,fill=TEAL)
    text(d,(40,y0+tile+23),"texture (shipped once)",FS,fill=DIM)
    # arrow -> 2
    ax=40+tile
    arrow(ax+8,ax+150,cy,"Respriter.masked","stored _m mask →")
    # 2 mask
    mx=ax+158
    paste(mask,mx,y0)
    text(d,(mx,y0+tile+8),"2 · stored mask",FS,fill=BRASS)
    text(d,(mx,y0+tile+23),"protects the detail",FS,fill=DIM)
    # arrow -> 3
    bx=mx+tile
    arrow(bx+8,bx+178,cy,"recolor to Palette","from target wood's planks")
    # 3 outputs stacked, medium
    s2=6; ox=bx+186; th=16*s2
    for i,(nm,dst) in enumerate([("greatwood",GREAT),("silverwood",SILVER)]):
        r=_recolor(base,mask,SRC,dst).resize((th,th),Image.NEAREST)
        oy=y0-6+i*(th+12)
        d.rectangle([ox-2,oy-2,ox+th+1,oy+th+1],fill=PANEL2,outline=LINE)
        im.paste(r,(ox,oy),r)
        text(d,(ox+th+10,oy+th//2),nm,FS,fill=TEAL,anchor="lm")
    text(d,(ox,y0+2*th+18),"3 · one generated variant",FS,fill=TEAL)
    text(d,(ox,y0+2*th+33),"per installed wood type  ×N",FS,fill=DIM)
    im.save(OUT/"mechanism.png")

# ================= 2. resprite demo (bigger, our pixels) =================
def demo():
    base,mask=_tile(SRC,True)
    s=14
    cols=[("source",SRC,base_no:=base)]
    variants=[("greatwood",GREAT),("silverwood",SILVER),("pale birch",BIRCHY)]
    imgs=[("mod's oak\n(shipped once)",base)]
    for nm,dst in variants:
        imgs.append((nm+"\n(generated)",_recolor(base,mask,SRC,dst)))
    W=40+len(imgs)*(16*s+30); H=16*s+90
    im,d=canvas(W,H)
    text(d,(24,18),"One shipped texture → every wood type, recolored at load",FB)
    x=24
    for lab,img in imgs:
        big=img.resize((16*s,16*s),Image.NEAREST)
        d.rectangle([x-2,52-2,x+16*s+1,52+16*s+1],fill=PANEL2,outline=LINE)
        im.paste(big,(x,52),big)
        for k,ln in enumerate(lab.split("\n")):
            text(d,(x,52+16*s+8+k*15),ln,FS,fill=TEAL if "generated" in ln else DIM)
        x+=16*s+30
    im.save(OUT/"resprite-demo.png")

# ================= 3. stored vs generated scale =================
def scale_chart():
    # stored (counts from public source) vs generated (scales with installed woods)
    W,H=940,330; im,d=canvas(W,H)
    text(d,(28,22),"Stored on disk  vs  generated at load",FT)
    text(d,(28,52),"log scale · stored = a fixed handful of masks + fix-ups; generated grows with installed wood mods",FS,fill=DIM)
    rows=[("supported modules (registry)",107,BRASS,"stored/code"),
          ("hardcoded special-case sprites",277,BRASS,"stored/code"),
          ("base+mask PNGs in /block root",43,BRASS,"stored"),
          ("palette strategies",12,BRASS,"stored/code"),
          ("generated sprites (≈, 60 woods)",107*8*60,TEAL,"generated ≈"),
          ("generated sprites (≈, 200 woods)",107*8*200,TEAL,"generated ≈")]
    x0,top=300,96; span=W-x0-120; lo,hi=0,math.log10(200000)
    def X(v): return x0+int(span*(math.log10(max(1,v))-lo)/(hi-lo))
    for gx in (10,100,1000,10000,100000):
        text(d,(X(gx),top-14),f"{gx:,}",FS,fill=DIM,anchor="mm")
        d.line([X(gx),top-2,X(gx),top+len(rows)*34],fill=LINE)
    for i,(nm,v,col,tag) in enumerate(rows):
        y=top+i*34+10
        text(d,(x0-14,y),nm,FS,fill=INK,anchor="rm")
        d.rectangle([x0,y-9,X(v),y+9],fill=col)
        text(d,(X(v)+8,y),f"{v:,}",FS,fill=col,anchor="lm")
    text(d,(x0,top+len(rows)*34+8),"generated ≈ modules × ~8 wood blocks each × installed wood types (illustrative; the mod logs the real task count at boot)",FS,fill=DIM)
    im.save(OUT/"stored-vs-generated.png")

if __name__=="__main__":
    mechanism(); demo(); scale_chart()
    print("charts ->", OUT)
