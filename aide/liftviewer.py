"""Present a lifted voxel model: a static 2:1-iso PNG preview (for headless
review) and a self-contained, dependency-free WebGL page you can spin with a
mouse or a finger on a phone.

Both consume the compact `(x, y, z, dir)` face list from `aide.lift`. Geometry
only — the model is shown flat-shaded (one colour per material, lit by face
normal). No texture is applied; texturing is a separate, later step.

The HTML embeds every model as a small integer face array and rebuilds the
geometry in-page, so the whole gallery is one file with no external requests —
it renders inside a locked-down artifact sandbox and on a phone browser alike.
"""

from __future__ import annotations

import json

from PIL import Image, ImageDraw

from aide.lift import FACE_NORMALS, Volume

# ---- static iso preview ---------------------------------------------------

_SHADE = {0: 0.62, 1: 0.62, 2: 1.0, 3: 0.5, 4: 0.82, 5: 0.72}  # per dir code
_VIEW = (1.0, 0.9, 1.0)

_FACE_CORNERS = [
    [(1, 0, 0), (1, 1, 0), (1, 1, 1), (1, 0, 1)],  # +X
    [(0, 0, 1), (0, 1, 1), (0, 1, 0), (0, 0, 0)],  # -X
    [(0, 1, 0), (0, 1, 1), (1, 1, 1), (1, 1, 0)],  # +Y
    [(0, 0, 1), (0, 0, 0), (1, 0, 0), (1, 0, 1)],  # -Y
    [(0, 0, 1), (1, 0, 1), (1, 1, 1), (0, 1, 1)],  # +Z
    [(1, 0, 0), (0, 0, 0), (0, 1, 0), (1, 1, 0)],  # -Z
]


def render_iso(faces, color=(0x8A, 0x6B, 0xB6), scale: int = 14,
               yaw_flip: bool = False) -> Image.Image:
    """Flat-shaded 2:1 iso PNG of a face list — a quick headless sanity view."""
    if not faces:
        return Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    s = scale

    def proj(p):
        x, y, z = p
        return ((x - z) * s, (x + z) * s * 0.5 - y * s)

    pts = [proj((x + ox, y + oy, z + oz))
           for (x, y, z, d) in faces for ox, oy, oz in _FACE_CORNERS[d]]
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    pad = s
    ox0, oy0 = -min(xs) + pad, -min(ys) + pad
    W = int(max(xs) - min(xs)) + 2 * pad
    H = int(max(ys) - min(ys)) + 2 * pad
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    dr = ImageDraw.Draw(img, "RGBA")

    drawable = []
    for (x, y, z, d) in faces:
        n = FACE_NORMALS[d]
        if n[0] * _VIEW[0] + n[1] * _VIEW[1] + n[2] * _VIEW[2] <= 0:
            continue
        corners = [(x + cx, y + cy, z + cz) for cx, cy, cz in _FACE_CORNERS[d]]
        depth = sum(c[0] + c[1] + c[2] for c in corners)
        drawable.append((depth, d, corners))
    drawable.sort(key=lambda t: t[0])

    for depth, d, corners in drawable:
        poly = [(ox0 + px, oy0 + py) for px, py in (proj(c) for c in corners)]
        f = _SHADE[d]
        fill = (int(color[0] * f), int(color[1] * f), int(color[2] * f), 255)
        dr.polygon(poly, fill=fill, outline=fill)
    return img


# ---- interactive WebGL gallery --------------------------------------------

def _model_payload(name, vol: Volume, mode: str) -> dict:
    """Compact per-model record: flat voxel occupancy + centre + dims. The viewer
    builds BOTH the crisp cube surface and the smooth surface-nets mesh from this
    occupancy in-browser, so the page stays small and the smooth/faceted toggle is
    live (no second mesh to ship)."""
    vox = sorted(vol.voxels)
    flat = [c for v in vox for c in v]
    xs = [v[0] for v in vox] + [v[0] + 1 for v in vox]
    ys = [v[1] for v in vox] + [v[1] + 1 for v in vox]
    zs = [v[2] for v in vox] + [v[2] + 1 for v in vox]
    return {
        "name": name,
        "mode": mode,
        "vox": flat,
        "nvox": len(vox),
        "center": [(min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2,
                   (min(zs) + max(zs)) / 2],
        "dims": [vol.nx, vol.ny, vol.nz],
    }


def build_payloads(models: dict[str, tuple[Volume, str]],
                   group: str | None = None) -> list[dict]:
    """models: name -> (Volume, mode-label). Returns viewer-ready records. Pass
    `group` to tag a whole set so the viewer can render labelled chip rows."""
    out = []
    for name, (vol, mode) in models.items():
        rec = _model_payload(name, vol, mode)
        if group:
            rec["group"] = group
        out.append(rec)
    return out


def viewer_html(payloads: list[dict], materials: dict[str, str],
                title: str = "Wand Caps — 3D") -> str:
    """A single self-contained HTML page: shape picker + material toggle +
    orbit/zoom by mouse or touch. No external requests; safe in a sandbox."""
    data_js = json.dumps(payloads, separators=(",", ":"))
    mats_js = json.dumps(materials, separators=(",", ":"))
    return _TEMPLATE.replace("__TITLE__", title) \
                    .replace("/*__DATA__*/0", data_js) \
                    .replace("/*__MATS__*/0", mats_js)


# The template is intentionally dependency-free vanilla WebGL. Face data is
# {x,y,z,dir} ints; the CPU expands them to two triangles with a per-face
# normal, then the vertex shader does flat directional lighting.
_TEMPLATE = r"""<style>
  :root{--bg:#17141f;--panel:#221c30;--ink:#e9e4f2;--muted:#9a8fb5;--edge:#3a3350;--accent:#8a6bb6;}
  @media (prefers-color-scheme: light){:root{--bg:#efeaf4;--panel:#fbf9ff;--ink:#241d33;--muted:#6a5f85;--edge:#d8cfe6;}}
  :root[data-theme=dark]{--bg:#17141f;--panel:#221c30;--ink:#e9e4f2;--muted:#9a8fb5;--edge:#3a3350;}
  :root[data-theme=light]{--bg:#efeaf4;--panel:#fbf9ff;--ink:#241d33;--muted:#6a5f85;--edge:#d8cfe6;}
  *{box-sizing:border-box}
  body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.5 ui-sans-serif,system-ui,-apple-system,Segoe UI,Roboto,sans-serif;-webkit-user-select:none;user-select:none;overflow:hidden}
  #wrap{position:fixed;inset:0;display:flex;flex-direction:column}
  header{padding:12px 16px 6px;text-align:center}
  header h1{margin:0;font-size:16px;font-weight:650;letter-spacing:.02em}
  header p{margin:2px 0 0;font-size:12px;color:var(--muted)}
  #stage{flex:1;position:relative;touch-action:none}
  canvas{display:block;width:100%;height:100%}
  #hint{position:absolute;left:0;right:0;bottom:10px;text-align:center;font-size:11px;color:var(--muted);pointer-events:none}
  #bar{display:flex;gap:6px;flex-wrap:wrap;justify-content:center;padding:10px 10px 6px}
  .grp{flex-basis:100%;text-align:center;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin:8px 0 -2px}
  .chip{border:1px solid var(--edge);background:var(--panel);color:var(--ink);border-radius:999px;padding:7px 12px;font-size:13px;cursor:pointer;transition:.12s}
  .chip:hover{border-color:var(--accent)}
  .chip[aria-pressed=true]{background:var(--accent);border-color:var(--accent);color:#fff}
  #mats{display:flex;gap:8px;justify-content:center;padding:0 10px 4px}
  .sw{width:26px;height:26px;border-radius:50%;border:2px solid var(--edge);cursor:pointer}
  .sw[aria-pressed=true]{border-color:var(--ink);box-shadow:0 0 0 2px var(--bg),0 0 0 4px var(--ink)}
  #meta{text-align:center;font-size:11px;color:var(--muted);padding:2px 0 10px}
  #tog{display:flex;gap:14px;justify-content:center;font-size:12px;color:var(--muted);padding-bottom:6px}
  #tog label{cursor:pointer}
</style>
<div id="wrap">
  <header><h1>__TITLE__</h1><p>Drag to rotate · pinch / scroll to zoom · untextured geometry</p></header>
  <div id="stage"><canvas id="c"></canvas><div id="hint">drag to rotate</div></div>
  <div id="mats"></div>
  <div id="bar"></div>
  <div id="tog"><label><input type="checkbox" id="smooth" checked> smooth</label><label><input type="checkbox" id="spin" checked> auto-spin</label><label><input type="checkbox" id="edges"> grid faces</label></div>
  <div id="meta"></div>
</div>
<script>
const MODELS=/*__DATA__*/0, MATS=/*__MATS__*/0;
const MATKEYS=Object.keys(MATS);
const FN=[[1,0,0],[-1,0,0],[0,1,0],[0,-1,0],[0,0,1],[0,0,-1]];
const CORN=[
 [[1,0,0],[1,1,0],[1,1,1],[1,0,1]],[[0,0,1],[0,1,1],[0,1,0],[0,0,0]],
 [[0,1,0],[0,1,1],[1,1,1],[1,1,0]],[[0,0,1],[0,0,0],[1,0,0],[1,0,1]],
 [[0,0,1],[1,0,1],[1,1,1],[0,1,1]],[[1,0,0],[0,0,0],[0,1,0],[1,1,0]]];

const cv=document.getElementById('c');
const gl=cv.getContext('webgl',{antialias:true,alpha:true});
const vs=`attribute vec3 p;attribute vec3 n;uniform mat4 mvp;uniform mat3 nm;
varying float sh;void main(){vec3 wn=normalize(nm*n);
vec3 L=normalize(vec3(0.5,0.9,0.6));
float dif=max(dot(wn,L),0.0);float amb=0.42+0.18*(wn.y*0.5+0.5);
sh=min(1.0,amb+0.62*dif);gl_Position=mvp*vec4(p,1.0);}`;
const fs=`precision mediump float;varying float sh;uniform vec3 col;
void main(){gl_FragColor=vec4(col*sh,1.0);}`;
function sh(t,s){const o=gl.createShader(t);gl.shaderSource(o,s);gl.compileShader(o);
 if(!gl.getShaderParameter(o,gl.COMPILE_STATUS))throw gl.getShaderInfoLog(o);return o;}
const prog=gl.createProgram();
gl.attachShader(prog,sh(gl.VERTEX_SHADER,vs));gl.attachShader(prog,sh(gl.FRAGMENT_SHADER,fs));
gl.linkProgram(prog);gl.useProgram(prog);
const A_p=gl.getAttribLocation(prog,'p'),A_n=gl.getAttribLocation(prog,'n');
const U_mvp=gl.getUniformLocation(prog,'mvp'),U_nm=gl.getUniformLocation(prog,'nm'),U_col=gl.getUniformLocation(prog,'col');
gl.enable(gl.DEPTH_TEST);

// reconstruct the occupancy set for a model (cached)
function voxSet(m){
 if(m._set)return m._set;
 const s=new Set(),v=m.vox;
 for(let i=0;i<v.length;i+=3)s.add(v[i]+','+v[i+1]+','+v[i+2]);
 m._set=s;return s;
}
function finish(pos,nor){
 let r2=0;for(let i=0;i<pos.length;i+=3){const d=pos[i]*pos[i]+pos[i+1]*pos[i+1]+pos[i+2]*pos[i+2];if(d>r2)r2=d;}
 return {pos:new Float32Array(pos),nor:new Float32Array(nor),count:pos.length/3,radius:Math.sqrt(r2)||10};
}
// CRISP: cull faces between a filled voxel and empty space -> cube quads
function buildCrisp(m,inset){
 const c=m.center,S=voxSet(m),v=m.vox,pos=[],nor=[],ins=inset||0,tri=[0,1,2,0,2,3];
 for(let i=0;i<v.length;i+=3){const x=v[i],y=v[i+1],z=v[i+2];
  for(let d=0;d<6;d++){const nn=FN[d];
   if(S.has((x+nn[0])+','+(y+nn[1])+','+(z+nn[2])))continue;
   const q=CORN[d].map(o=>[x+o[0]-c[0],y+o[1]-c[1],z+o[2]-c[2]]);
   if(ins){const cx=(q[0][0]+q[1][0]+q[2][0]+q[3][0])/4,cy=(q[0][1]+q[1][1]+q[2][1]+q[3][1])/4,cz=(q[0][2]+q[1][2]+q[2][2]+q[3][2])/4;
    for(const p of q){p[0]+=(cx-p[0])*ins;p[1]+=(cy-p[1])*ins;p[2]+=(cz-p[2])*ins;}}
   for(const k of tri){pos.push(q[k][0],q[k][1],q[k][2]);nor.push(nn[0],nn[1],nn[2]);}}}
 return finish(pos,nor);
}
// SMOOTH: naive surface nets — one relaxed vertex per boundary cell, gradient
// normals. Turns the voxel staircase into a smooth faceted skin.
const SN_C=[[0,0,0],[1,0,0],[0,1,0],[1,1,0],[0,0,1],[1,0,1],[0,1,1],[1,1,1]];
const SN_E=[[0,1],[0,2],[0,4],[1,3],[1,5],[2,3],[2,6],[4,5],[4,6],[3,7],[5,7],[6,7]];
function buildSmooth(m,relax){
 const c=m.center,S=voxSet(m),v=m.vox;
 let x0=1e9,y0=1e9,z0=1e9,x1=-1e9,y1=-1e9,z1=-1e9;
 for(let i=0;i<v.length;i+=3){x0=Math.min(x0,v[i]);x1=Math.max(x1,v[i]);
  y0=Math.min(y0,v[i+1]);y1=Math.max(y1,v[i+1]);z0=Math.min(z0,v[i+2]);z1=Math.max(z1,v[i+2]);}
 const H=(i,j,k)=>S.has(i+','+j+','+k)?1:0;
 const cellV=new Map(),verts=[],norms=[];
 for(let i=x0-1;i<=x1+1;i++)for(let j=y0-1;j<=y1+1;j++)for(let k=z0-1;k<=z1+1;k++){
  const s=SN_C.map(o=>H(i+o[0],j+o[1],k+o[2]));const tot=s[0]+s[1]+s[2]+s[3]+s[4]+s[5]+s[6]+s[7];
  if(tot===0||tot===8)continue;
  let px=0,py=0,pz=0,cn=0;
  for(const [a,b] of SN_E)if(s[a]!==s[b]){const A=SN_C[a],B=SN_C[b];
   px+=(A[0]+B[0])/2;py+=(A[1]+B[1])/2;pz+=(A[2]+B[2])/2;cn++;}
  cellV.set(i+','+j+','+k,verts.length);
  verts.push([i+px/cn,j+py/cn,k+pz/cn]);
  norms.push([-((s[1]+s[3]+s[5]+s[7])-(s[0]+s[2]+s[4]+s[6])),
              -((s[2]+s[3]+s[6]+s[7])-(s[0]+s[1]+s[4]+s[5])),
              -((s[4]+s[5]+s[6]+s[7])-(s[0]+s[1]+s[2]+s[3]))]);
 }
 const cv=(i,j,k)=>cellV.get(i+','+j+','+k),tris=[];
 for(let i=x0-1;i<=x1+2;i++)for(let j=y0-1;j<=y1+2;j++)for(let k=z0-1;k<=z1+2;k++){
  if(H(i,j,k)!==H(i+1,j,k)){const q=[cv(i,j-1,k-1),cv(i,j,k-1),cv(i,j,k),cv(i,j-1,k)];
   if(q.every(x=>x!==undefined))tris.push(q[0],q[1],q[2],q[0],q[2],q[3]);}
  if(H(i,j,k)!==H(i,j+1,k)){const q=[cv(i-1,j,k-1),cv(i,j,k-1),cv(i,j,k),cv(i-1,j,k)];
   if(q.every(x=>x!==undefined))tris.push(q[0],q[1],q[2],q[0],q[2],q[3]);}
  if(H(i,j,k)!==H(i,j,k+1)){const q=[cv(i-1,j-1,k),cv(i,j-1,k),cv(i,j,k),cv(i-1,j,k)];
   if(q.every(x=>x!==undefined))tris.push(q[0],q[1],q[2],q[0],q[2],q[3]);}
 }
 // Laplacian relaxation
 if(relax>0){const adj=verts.map(()=>new Set());
  for(let t=0;t<tris.length;t+=3){const a=tris[t],b=tris[t+1],d=tris[t+2];
   adj[a].add(b);adj[a].add(d);adj[b].add(a);adj[b].add(d);adj[d].add(a);adj[d].add(b);}
  for(let it=0;it<relax;it++){const nv=verts.map(p=>p.slice());
   for(let i=0;i<verts.length;i++){const nb=adj[i];if(!nb.size)continue;
    let sx=0,sy=0,sz=0;nb.forEach(n=>{sx+=verts[n][0];sy+=verts[n][1];sz+=verts[n][2];});
    const mn=nb.size;nv[i][0]=0.5*verts[i][0]+0.5*sx/mn;nv[i][1]=0.5*verts[i][1]+0.5*sy/mn;nv[i][2]=0.5*verts[i][2]+0.5*sz/mn;}
   for(let i=0;i<verts.length;i++)verts[i]=nv[i];}}
 for(const n of norms){const L=Math.hypot(n[0],n[1],n[2])||1;n[0]/=L;n[1]/=L;n[2]/=L;}
 const pos=[],nor=[];
 for(let t=0;t<tris.length;t++){const vi=tris[t],p=verts[vi],n=norms[vi];
  pos.push(p[0]-c[0],p[1]-c[1],p[2]-c[2]);nor.push(n[0],n[1],n[2]);}
 return finish(pos,nor);
}
function buildGeom(m,inset){return smooth?buildSmooth(m,2):buildCrisp(m,inset);}
const posB=gl.createBuffer(),norB=gl.createBuffer();
let geom=null,radius=10;
function upload(g){geom=g;radius=g.radius;
 gl.bindBuffer(gl.ARRAY_BUFFER,posB);gl.bufferData(gl.ARRAY_BUFFER,g.pos,gl.STATIC_DRAW);
 gl.bindBuffer(gl.ARRAY_BUFFER,norB);gl.bufferData(gl.ARRAY_BUFFER,g.nor,gl.STATIC_DRAW);}

// ---- tiny mat4 ----
function persp(f,a,n,fa){const t=1/Math.tan(f/2);return[t/a,0,0,0, 0,t,0,0, 0,0,(fa+n)/(n-fa),-1, 0,0,2*fa*n/(n-fa),0];}
function mul(a,b){const o=new Array(16);for(let i=0;i<4;i++)for(let j=0;j<4;j++){let s=0;for(let k=0;k<4;k++)s+=a[k*4+j]*b[i*4+k];o[i*4+j]=s;}return o;}
function rotY(t){const c=Math.cos(t),s=Math.sin(t);return[c,0,-s,0,0,1,0,0,s,0,c,0,0,0,0,1];}
function rotX(t){const c=Math.cos(t),s=Math.sin(t);return[1,0,0,0,0,c,s,0,0,-s,c,0,0,0,0,1];}
function trans(x,y,z){return[1,0,0,0,0,1,0,0,0,0,1,0,x,y,z,1];}

let yaw=-0.7,pitch=-0.35,dist=2.55,spin=true,inset=0,smooth=true;
let curMat=MATKEYS[0],curModel=0;

function draw(){
 const dpr=Math.min(devicePixelRatio||1,2);
 const w=cv.clientWidth,h=cv.clientHeight;
 if(cv.width!==w*dpr||cv.height!==h*dpr){cv.width=w*dpr;cv.height=h*dpr;}
 gl.viewport(0,0,cv.width,cv.height);
 gl.clearColor(0,0,0,0);gl.clear(gl.COLOR_BUFFER_BIT|gl.DEPTH_BUFFER_BIT);
 if(!geom)return;
 const D=radius*dist;
 const P=persp(0.9,cv.width/cv.height,Math.max(0.1,D-radius*2),D+radius*3);
 let V=trans(0,0,-D);
 let M=mul(rotX(pitch),rotY(yaw));
 const MV=mul(V,M);const MVP=mul(P,MV);
 gl.uniformMatrix4fv(U_mvp,false,new Float32Array(MVP));
 // normal matrix = rotation part of M (orthonormal) -> 3x3
 const nm=[M[0],M[1],M[2],M[4],M[5],M[6],M[8],M[9],M[10]];
 gl.uniformMatrix3fv(U_nm,false,new Float32Array(nm));
 const col=hex(MATS[curMat]);gl.uniform3f(U_col,col[0],col[1],col[2]);
 gl.bindBuffer(gl.ARRAY_BUFFER,posB);gl.enableVertexAttribArray(A_p);gl.vertexAttribPointer(A_p,3,gl.FLOAT,false,0,0);
 gl.bindBuffer(gl.ARRAY_BUFFER,norB);gl.enableVertexAttribArray(A_n);gl.vertexAttribPointer(A_n,3,gl.FLOAT,false,0,0);
 gl.drawArrays(gl.TRIANGLES,0,geom.count);
}
function hex(h){h=h.replace('#','');return[parseInt(h.substr(0,2),16)/255,parseInt(h.substr(2,2),16)/255,parseInt(h.substr(4,2),16)/255];}

let last=0;
function loop(t){const dt=(t-last)/1000;last=t;if(spin)yaw+=dt*0.5;draw();requestAnimationFrame(loop);}

function select(i){curModel=i;const m=MODELS[i];upload(buildGeom(m,inset));
 document.querySelectorAll('#bar .chip').forEach((c,k)=>c.setAttribute('aria-pressed',k===i));
 document.getElementById('meta').textContent=`${m.name} · ${m.mode} · ${m.nvox} voxels · ${smooth?'smooth':'faceted'} · ${geom.count/3|0} tris`;}

// ---- UI ----
const bar=document.getElementById('bar');
let lastG=null;
MODELS.forEach((m,i)=>{
 if(m.group&&m.group!==lastG){lastG=m.group;const g=document.createElement('div');
  g.className='grp';g.textContent=m.group;bar.appendChild(g);}
 const b=document.createElement('button');b.className='chip';
 b.textContent=m.name;b.onclick=()=>select(i);bar.appendChild(b);});
const mats=document.getElementById('mats');
MATKEYS.forEach(k=>{const s=document.createElement('button');s.className='sw';
 s.style.background=MATS[k];s.title=k;s.setAttribute('aria-pressed',k===curMat);
 s.onclick=()=>{curMat=k;document.querySelectorAll('#mats .sw').forEach(e=>e.setAttribute('aria-pressed',e.title===k));};
 mats.appendChild(s);});
document.getElementById('smooth').onchange=e=>{smooth=e.target.checked;
 document.getElementById('edges').disabled=smooth;select(curModel);};
document.getElementById('spin').onchange=e=>spin=e.target.checked;
document.getElementById('edges').onchange=e=>{inset=e.target.checked?0.12:0;select(curModel);};

// ---- pointer / touch orbit ----
const stage=document.getElementById('stage');let drag=null,pinch=null;
stage.addEventListener('pointerdown',e=>{drag={x:e.clientX,y:e.clientY};spin=false;document.getElementById('spin').checked=false;document.getElementById('hint').style.opacity=0;stage.setPointerCapture(e.pointerId);});
stage.addEventListener('pointermove',e=>{if(!drag)return;yaw+=(e.clientX-drag.x)*0.01;pitch+=(e.clientY-drag.y)*0.01;pitch=Math.max(-1.5,Math.min(1.5,pitch));drag={x:e.clientX,y:e.clientY};});
stage.addEventListener('pointerup',()=>drag=null);
stage.addEventListener('wheel',e=>{e.preventDefault();dist*=(1+Math.sign(e.deltaY)*0.1);dist=Math.max(1.2,Math.min(7,dist));},{passive:false});
let tps=[];
stage.addEventListener('touchmove',e=>{if(e.touches.length===2){e.preventDefault();const dx=e.touches[0].clientX-e.touches[1].clientX,dy=e.touches[0].clientY-e.touches[1].clientY;const d=Math.hypot(dx,dy);if(pinch)dist*=pinch/d,dist=Math.max(1.2,Math.min(7,dist));pinch=d;}},{passive:false});
stage.addEventListener('touchend',()=>pinch=null);

if(matchMedia('(prefers-reduced-motion: reduce)').matches){spin=false;document.getElementById('spin').checked=false;}
document.getElementById('edges').disabled=smooth;
select(0);requestAnimationFrame(loop);
</script>
"""
