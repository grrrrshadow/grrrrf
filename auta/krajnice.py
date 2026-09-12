# -*- coding: utf-8 -*-
"""Vzdalenost kotvy od linky kol v bocnim pohledu = poloha ke krajnici."""
import io, json, os
import numpy as np
from PIL import Image
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/zpuv/sprites")
V=json.load(io.open(BASE+"/nove58.json")); S=json.load(io.open(BASE+"/sady.json"))
sp={(s["vid"],s["sada"]):s["spr"] for s in S}
cache={}
def sh(f):
    if f not in cache: cache[f]=np.array(Image.open(f).convert("RGBA"))
    return cache[f]
print("Smer E (bok): kolik pixelu je linka kol POD kotvou.  Stejne cislo = stejne daleko od krajnice.")
print("%-34s %6s %6s %8s" % ("auto (zakladni sada)","ted","nove","zmena"))
ted=[]; nov=[]
for v in V:
    if v["sada"]!="0x0000": continue
    s=sp[(v["vid"],"0x0000")][2]
    a=sh(s["file"])[s["y"]:s["y"]+s["h"], s["x"]:s["x"]+s["w"]]
    m=a[:,:,3]>16
    dno=int(np.where(m.any(axis=1))[0][-1])       # linka kol v bocnim pohledu
    t=dno-(-v["yo"][2]); n=dno-(-v["nyo"][2])
    ted.append(t); nov.append(n)
    print("0x%02X %-29s %6d %6d %+8d" % (v["vid"], v["jm"], t, n, n-t))
print()
print("rozptyl:  ted %d az %d  (rozdil %d px)      nove %d az %d  (rozdil %d px)" %
      (min(ted),max(ted),max(ted)-min(ted),min(nov),max(nov),max(nov)-min(nov)))

print()
print("Vsech 8 smeru - rozptyl mezi auty (nejnizsi pixel siluety proti kotve):")
SM=["N","NE","E","SE","S","SW","W","NW"]
print("  %-4s %14s %14s" % ("dir","ted","nove"))
for k in range(8):
    t=[];n=[]
    for v in V:
        if v["sada"]!="0x0000": continue
        s=sp[(v["vid"],"0x0000")][k]
        a=sh(s["file"])[s["y"]:s["y"]+s["h"], s["x"]:s["x"]+s["w"]]
        m=a[:,:,3]>16
        dno=int(np.where(m.any(axis=1))[0][-1])
        t.append(dno-(-v["yo"][k])); n.append(dno-(-v["nyo"][k]))
    print("  %-4s %4d..%-4d (%2d) %4d..%-4d (%2d)" % (SM[k],min(t),max(t),max(t)-min(t),min(n),max(n),max(n)-min(n)))
