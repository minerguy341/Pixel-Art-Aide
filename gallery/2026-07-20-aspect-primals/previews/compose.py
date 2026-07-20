"""Compose the aspect-primal comparison contact sheet. Run from repo root:
  python3 gallery/2026-07-20-aspect-primals/previews/compose.py
"""
import pathlib
from PIL import Image, ImageDraw, ImageFont
G = pathlib.Path("gallery/2026-07-20-aspect-primals")
OUT = G/"out"; PREV = G/"previews"

PRIMALS = [("ventus","Ventus","#CDE8F5","air · wind"),
           ("tellus","Tellus","#6BA84F","earth · soil"),
           ("flamma","Flamma","#F0552B","fire · heat"),
           ("unda","Unda","#3D9BE0","water · flow"),
           ("forma","Forma","#EDE9DC","order"),
           ("discordia","Discordia","#4A3459","chaos")]

BG=(38,40,48); SLOT=(28,29,35); INK=(226,224,235); DIM=(150,150,165); TEAL=(127,232,216); BRASS=(199,154,85)
def font(s):
    for p in ["/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf","/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        try: return ImageFont.truetype(p,s)
        except Exception: pass
    return ImageFont.load_default()
F=font(15); FS=font(12); FT=font(20); FB=font(15)

def load(name,mode): return Image.open(OUT/f"{name}_{mode}.png").convert("RGBA")

def sheet():
    cell=150; pad=20; x0=150; top=118
    W=x0+6*cell+pad; H=top+2*(cell+28)+180
    im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
    d.text((pad,26),"Primal aspect icons — frame vs full backdrop",font=FT,fill=INK)
    d.text((pad,54),"64x64 HD hexagon GUI icons · shown 2x on a GUI-slot bg · symbol = concept, colour = aspect code",font=FS,fill=DIM)
    # column headers
    for i,(nm,disp,code,concept) in enumerate(PRIMALS):
        cx=x0+i*cell+cell//2
        d.text((cx,86),disp,font=FB,fill=INK,anchor="mm")
        d.text((cx,102),code,font=FS,fill=DIM,anchor="mm")
    rows=[("BACKDROP","backdrop",top,TEAL,"✓ recommended"),("FRAME","frame",top+cell+28,DIM,"")]
    for label,mode,ry,col,tag in rows:
        d.text((pad,ry+cell//2-14),label,font=FB,fill=col,anchor="lm")
        if tag: d.text((pad,ry+cell//2+4),tag,font=FS,fill=col,anchor="lm")
        for i,(nm,disp,code,concept) in enumerate(PRIMALS):
            cellx=x0+i*cell
            d.rectangle([cellx+8,ry+8,cellx+cell-8,ry+cell-8],fill=SLOT,outline=(60,62,72))
            ic=load(nm,mode).resize((128,128),Image.NEAREST)
            im.paste(ic,(cellx+(cell-128)//2,ry+(cell-128)//2),ic)
    # legibility strip: actual GUI sizes on dark + light
    sy=top+2*(cell+28)+10
    d.text((pad,sy),"Legibility at GUI size (nearest):  48 / 32 / 20 px, on dark and light",font=FS,fill=DIM)
    for row,(bgc,tag) in enumerate([((22,23,28),"dark GUI"),((205,203,196),"light GUI")]):
        yy=sy+24+row*66
        d.text((pad,yy+24),tag,font=FS,fill=DIM,anchor="lm")
        xx=x0
        for nm,disp,code,concept in PRIMALS:
            ic=load(nm,"backdrop")
            for s in (48,32,20):
                sw=Image.new("RGB",(s+8,s+8),bgc)
                sw.paste(ic.resize((s,s),Image.NEAREST),(4,4),ic.resize((s,s),Image.NEAREST))
                im.paste(sw,(xx,yy))
                xx+=s+12
            xx+=10
    im.save(PREV/"candidates-r3.png"); print("wrote",PREV/"candidates-r3.png",im.size)

if __name__=="__main__": sheet()
