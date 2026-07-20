"""Compose the 10-candidate Arcanum sheet (batch 3, researched arcane iconography).
Run from repo root:
  python3 gallery/2026-07-20-aspect-primals/previews/magic10_sheet.py
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

def sheet():
    code, concept, cands = C.MAGIC10
    cols=5; cell=210; x0=20; top=104
    W=x0+cols*cell+6; H=top+2*cell+10
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((x0,24),f"Arcanum — 10 more magic candidates  ·  {code}",font=FT,fill=INK)
    d.text((x0,54),"researched arcane/occult/alchemy iconography · filled backdrop · shown 2.6x; strip = 32/20px on dark & light",font=FS,fill=DIM)
    for i,(key,desc,fn) in enumerate(cands):
        ic=C.render(code,fn); cx=x0+(i%cols)*cell; cy=top+(i//cols)*cell
        d.text((cx+cell//2,cy+10),f"{i+1}. {desc}",font=FB,fill=TEAL,anchor="mm")
        d.rectangle([cx+10,cy+26,cx+cell-10,cy+26+150],fill=SLOT,outline=(60,62,72))
        big=ic.resize((140,140),Image.NEAREST)
        im.paste(big,(cx+(cell-140)//2,cy+31),big)
        xx=cx+30; yy=cy+182
        for bgc in ((22,23,28),(205,203,196)):
            for s in (32,20):
                sw=Image.new("RGB",(s+6,s+6),bgc); r=ic.resize((s,s),Image.NEAREST)
                sw.paste(r,(3,3),r); im.paste(sw,(xx,yy)); xx+=s+6
            xx+=8
    out=PREV/"compound-arcanum3.png"; im.save(out); print("wrote",out,im.size)

if __name__=="__main__": sheet()
