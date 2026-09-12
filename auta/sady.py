# -*- coding: utf-8 -*-
"""Vsech 58 sad po 8 spritech z rozbaleneho puvodniho GRF."""
import io, re, json
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
p=BASE+"/zpuv/sprites/VWT1.yagl"
L=io.open(p,encoding="utf-8").read().split("\n")
SPR=re.compile(r'\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\], (\w+), [^"]*"([^"]+)", \[(\d+), (\d+)\]')
sady=[]; cur=None; setname=None; blok=[]
for i,l in enumerate(L):
    m0=re.match(r'    sprite_set // (0x[0-9A-F]+)', l)
    if m0: cur=[]; setname=m0.group(1)
    elif cur is not None and l.startswith("    }"):
        if len(cur)==8: blok.append((setname,list(cur)))
        cur=None
    elif cur is not None:
        m=SPR.search(l)
        if m:
            w,h,xo,yo,z,f,x,y=m.groups()
            cur.append(dict(radek=i,w=int(w),h=int(h),xo=int(xo),yo=int(yo),file=f,x=int(x),y=int(y)))
    mm=re.match(r'\s*/\* 0x00([0-9A-F]{2}) \*/ "(.*)";', l)
    if mm:
        for sn,sp in blok:
            sady.append(dict(vid=int(mm.group(1),16), jm=mm.group(2), sada=sn, spr=sp))
        blok=[]
print("sad:", len(sady))
json.dump(sady, io.open(BASE+"/sady.json","w"))
for s in sady[:6]:
    print(" 0x%02X %-28s %s  %s" % (s["vid"],s["jm"],s["sada"]," ".join("%dx%d"%(t["w"],t["h"]) for t in s["spr"][:3])))
