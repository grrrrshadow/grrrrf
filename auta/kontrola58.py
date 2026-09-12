# -*- coding: utf-8 -*-
"""Opravdova kontrola: po zarovnani musi podvozek sadu od sady sednout na stejne misto."""
import io, json, os
import numpy as np
from PIL import Image
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/zpuv/sprites")
V=json.load(io.open(BASE+"/nove58.json")); S=json.load(io.open(BASE+"/sady.json"))
cache={}
def sh(f):
    if f not in cache: cache[f]=np.array(Image.open(f).convert("RGBA"))
    return cache[f]
def pas(s, D=15):
    a=sh(s["file"])[s["y"]:s["y"]+s["h"], s["x"]:s["x"]+s["w"]]
    m=(a[:,:,3]>16)
    dno=int(np.where(m.any(axis=1))[0][-1])
    out=np.zeros_like(m); out[max(0,dno-D):dno+1,:]=m[max(0,dno-D):dno+1,:]
    return out.astype(np.float32)
def reg(A,B,ax,ay,bx,by,r=14):
    """A a B umistene podle kotev; hleda zbytkovy posun"""
    best=None
    HA,WA=A.shape; HB,WB=B.shape
    for dy in range(-r,r+1):
        for dx in range(-r,r+1):
            # bod (x,y) v A odpovida (x-ax+bx+dx, y-ay+by+dy) v B
            ox=int(round(-ax+bx+dx)); oy=int(round(-ay+by+dy))
            x0=max(0,-ox); x1=min(WA,WB-ox); y0=max(0,-oy); y1=min(HA,HB-oy)
            if x1<=x0 or y1<=y0: continue
            a=A[y0:y1,x0:x1]; b=B[y0+oy:y1+oy,x0+ox:x1+ox]
            sp=float((a*b).sum())
            if sp<0.3*min(A.sum(),B.sum()): continue
            sj=float(a.sum()+b.sum()-sp); v=sp/sj if sj else 0
            if best is None or v>best[0]: best=(v,dx,dy)
    return best
sp={(s["vid"],s["sada"]):s["spr"] for s in S}
from collections import defaultdict
g=defaultdict(list)
for v in V: g[v["vid"]].append(v)
print("Zbytkovy posun podvozku mezi sadami tehoz vozidla, smer E (0 = sedi):")
for vid,ls in sorted(g.items()):
    if len(ls)<2: continue
    zak=ls[0]; radky=[]
    for l in ls[1:]:
        A=pas(sp[(vid,zak["sada"])][2]); B=pas(sp[(vid,l["sada"])][2])
        r=reg(A,B,-zak["nxo"][2],-zak["nyo"][2],-l["nxo"][2],-l["nyo"][2])
        radky.append("%s:(%+d,%+d)/IoU%.2f" % (l["sada"], r[1], r[2], r[0]) if r else "%s:-"%l["sada"])
    print("  0x%02X %-30s %s" % (vid, zak["jm"], "  ".join(radky)))
