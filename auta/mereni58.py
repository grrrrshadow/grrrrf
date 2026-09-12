# -*- coding: utf-8 -*-
"""Zmeri vsech 58 sad: stred rozvoru na vozovce ve vsech 8 smerech."""
import io, json, os, math
import numpy as np
from PIL import Image
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/zpuv/sprites")
sady=json.load(io.open(BASE+"/sady.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]; T=0.5; POMER=0.59
AL=[math.radians(45*k) for k in range(8)]; CO=[math.cos(a) for a in AL]; SI=[math.sin(a) for a in AL]
cache={}
def sh(f):
    if f not in cache: cache[f]=np.array(Image.open(f).convert("RGBA"))
    return cache[f]
def mask(s):
    a=sh(s["file"])[s["y"]:s["y"]+s["h"], s["x"]:s["x"]+s["w"]]
    return a[:,:,3]>16
def reg(A,B,r=70):
    best=None; ha,wa=A.shape; hb,wb=B.shape
    A=A.astype(np.float32); B=B.astype(np.float32)
    mn=0.35*min(A.sum(),B.sum())
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            x0=max(0,-dx); x1=min(wa,wb-dx); y0=max(0,-dy); y1=min(ha,hb-dy)
            if x1<=x0 or y1<=y0: continue
            a=A[y0:y1,x0:x1]; b=B[y0+dy:y1+dy,x0+dx:x1+dx]
            sp=float((a*b).sum())
            if sp<mn: continue
            sj=float(a.sum()+b.sum()-sp); v=sp/sj if sj else 0
            if best is None or v>best[0]: best=(v,dx,dy)
    return best
def kolav(m, w):
    p=np.array([(np.where(m[:,x])[0][-1] if m[:,x].any() else -1) for x in range(w)])
    u=np.where(p>=p.max()-1)[0]
    sk=[];cur=[u[0]]
    for q in u[1:]:
        if q-cur[-1]<=2: cur.append(q)
        else: sk.append(cur);cur=[q]
    sk.append(cur)
    st=[(c[0]+c[-1])/2.0 for c in sk]
    return (min(st)+max(st))/2.0, (max(st)-min(st)), int(p.max())
vys=[]
for S in sady:
    spr=S["spr"]; M=[mask(s) for s in spr]
    dno=[int(np.where(m.any(axis=1))[0][-1]) for m in M]
    lev=[int(np.where(m.any(axis=0))[0][0]) for m in M]
    osa={}
    for k in (0,4):
        v,dx,dy=reg(M[k][:,::-1],M[k]); osa[k]=(spr[k]["w"]-1+dx)/2.0
    SS={}
    for k in (1,2,3):
        v,dx,dy=reg(M[k][:,::-1],M[8-k]); SS[k]=spr[k]["w"]-1+dx
    k2=kolav(M[2],spr[2]["w"]); k6=kolav(M[6],spr[6]["w"])
    a=(k2[1]+k6[1])/4.0; b=a*POMER
    pu=[0.0]*8; pu[0]=osa[0]; pu[4]=osa[4]; pu[2]=k2[0]; pu[6]=k6[0]
    F=pu[2]-lev[2]; R=pu[6]-lev[6]; dif=0.7071*(F-R)
    pu[1]=(SS[1]+dif)/2.0; pu[7]=(SS[1]-dif)/2.0
    pu[3]=(SS[3]+dif)/2.0; pu[5]=(SS[3]-dif)/2.0
    pv=[dno[k]-T*(a*abs(CO[k])+b*abs(SI[k])) for k in range(8)]
    vys.append(dict(vid=S["vid"],jm=S["jm"],sada=S["sada"],rozvor=2*a,pu=pu,pv=pv,
                    radky=[s["radek"] for s in spr],
                    xo=[s["xo"] for s in spr], yo=[s["yo"] for s in spr]))
    print("0x%02X %-30s %s rozvor %5.1f" % (S["vid"],S["jm"],S["sada"],2*a))
json.dump(vys, io.open(BASE+"/mereni58.json","w"))
