"""Compose one candidate sheet per compound aspect (5 candidates each).
Run from repo root:
  python3 gallery/2026-07-20-aspect-primals/previews/compound_sheets.py
"""
import pathlib, sys
sys.path.insert(0, "gallery/2026-07-20-aspect-primals/src")
from PIL import Image, ImageDraw, ImageFont
import compounds as C

PREV = pathlib.Path("gallery/2026-07-20-aspect-primals/previews")
BG=(38,40,48); SLOT=(28,29,35); INK=(226,224,235); DIM=(150,150,165); TEAL=(127,232,216)
def font(s):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p,s)
        except Exception: pass
    return ImageFont.load_default()
FT=font(21); FB=font(14); FS=font(12)

def sheet(title, code, concept, cands, outname):
    name=title
    cell=170; x0=20; top=120; n=len(cands)
    W=x0+n*cell+10; H=top+cell+96
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((x0,24),f"{name} — {concept}  ·  {code}",font=FT,fill=INK)
    d.text((x0,54),f"{n} symbol candidates · filled backdrop · shown 2.3x; strip = 48/32/20px on dark & light",font=FS,fill=DIM)
    for i,(key,desc,fn) in enumerate(cands):
        ic=C.render(code,fn); cx=x0+i*cell
        d.text((cx+cell//2,86),f"{i+1}. {desc}",font=FB,fill=TEAL,anchor="mm")
        d.rectangle([cx+8,top,cx+cell-8,top+cell-14],fill=SLOT,outline=(60,62,72))
        big=ic.resize((146,146),Image.NEAREST)
        im.paste(big,(cx+(cell-146)//2,top+(cell-14-146)//2),big)
        xx=cx+14; yy=top+cell-2
        for bgc in ((22,23,28),(205,203,196)):
            x2=xx
            for s in (30,20):
                sw=Image.new("RGB",(s+6,s+6),bgc); r=ic.resize((s,s),Image.NEAREST)
                sw.paste(r,(3,3),r); im.paste(sw,(x2,yy)); x2+=s+6
            xx=x2+8
    out=PREV/outname; im.save(out); print("wrote",out,im.size)

if __name__=="__main__":
    for n,(code,concept,cands) in C.ASPECTS.items():
        sheet(n, code, concept, cands, f"compound-{n.lower()}.png")
    code,concept,cands = C.ARCANUM_MORE
    sheet("Arcanum — more options", code, concept, cands, "compound-arcanum2.png")
