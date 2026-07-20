"""Render the Discordia symbol options on its backdrop and compose a sheet.
Run from repo root:
  python3 gallery/2026-07-20-aspect-primals/previews/discordia_variants.py
"""
import pathlib, sys
sys.path.insert(0, "gallery/2026-07-20-aspect-primals/src")
from PIL import Image, ImageDraw, ImageFont
import make_aspects as M

PREV = pathlib.Path("gallery/2026-07-20-aspect-primals/previews")
CODE = "#4A3459"
OPTS = [("burst",   "Shatter-burst", "spiky solid star"),
        ("crack",   "Fracture",      "shattered glass"),
        ("shards",  "Broken shards", "flying pieces"),
        ("scatter", "Entropy",       "order → disorder")]

BG=(38,40,48); SLOT=(28,29,35); INK=(226,224,235); DIM=(150,150,165); TEAL=(127,232,216)
def font(s):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p,s)
        except Exception: pass
    return ImageFont.load_default()
FT=font(20); FB=font(15); FS=font(12)

def sheet():
    cell=170; x0=24; top=118
    W=x0+len(OPTS)*cell+10; H=top+cell+150
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((x0,26),"Discordia — chaos / entropy · symbol options",font=FT,fill=INK)
    d.text((x0,54),"same full-backdrop treatment (#4A3459), shown 2.4x; strip below = 48/32/20px",font=FS,fill=DIM)
    for i,(key,name,desc) in enumerate(OPTS):
        ic=M.make_backdrop(CODE,key)
        cx=x0+i*cell
        d.text((cx+cell//2,88),name,font=FB,fill=TEAL,anchor="mm")
        d.text((cx+cell//2,104),desc,font=FS,fill=DIM,anchor="mm")
        d.rectangle([cx+8,top,cx+cell-8,top+cell-16],fill=SLOT,outline=(60,62,72))
        big=ic.resize((150,150),Image.NEAREST)
        im.paste(big,(cx+(cell-150)//2,top+(cell-16-150)//2),big)
        # small sizes
        xx=cx+18; yy=top+cell-2
        for s in (48,32,20):
            sw=Image.new("RGB",(s+8,s+8),(22,23,28))
            r=ic.resize((s,s),Image.NEAREST); sw.paste(r,(4,4),r)
            im.paste(sw,(xx,yy)); xx+=s+10
    im.save(PREV/"discordia-options.png"); print("wrote",PREV/"discordia-options.png",im.size)

if __name__=="__main__": sheet()
