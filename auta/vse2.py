# -*- coding: utf-8 -*-
"""Nove offsety pro vsech 18 aut: tuhy bod odvozeny z konvence VW T1 origsize."""
import io, json, math
import numpy as np
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
D=json.load(io.open(BASE+"/vse.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]
AL=[math.radians(45*k) for k in range(8)]; CO=[math.cos(a) for a in AL]; SI=[math.sin(a) for a in AL]
Mu=np.array([[1.0,s,c] for c,s in zip(CO,SI)]); Mv=np.array([[1.0,c,s] for c,s in zip(CO,SI)])
R=D["129"]                                   # 0x81 VW T1 origsize
du=np.array(R["ax"])-np.array(R["pu"]); dv=np.array(R["ay"])-np.array(R["pv"])
cu,*_=np.linalg.lstsq(Mu,du,rcond=None); cv,*_=np.linalg.lstsq(Mv,dv,rcond=None)
DU=Mu.dot(cu); DV=Mv.dot(cv)
print("Spolecna konvence (kotva proti stredu rozvoru na vozovce), tuhy bod:")
print("  vodorovne %.1f %+.1f*sin %+.1f*cos      svisle %.1f %+.1f*cos %+.1f*sin" % (cu[0],cu[1],cu[2],cv[0],cv[1],cv[2]))
print("  %-4s %8s %8s" % ("dir","vodor.","svisle"))
for k in range(8): print("  %-4s %8.1f %8.1f" % (SM[k],DU[k],DV[k]))
print()
nove={}
for key in sorted(D, key=lambda s:int(s)):
    v=D[key]; vid=int(key)
    nx=np.array(v["pu"])+DU; ny=np.array(v["pv"])+DV
    nove[key]=dict(jm=v["jm"], xo=[-int(round(x)) for x in nx], yo=[-int(round(y)) for y in ny],
                   sxo=[-int(x) for x in v["ax"]], syo=[-int(y) for y in v["ay"]])
json.dump(nove, io.open(BASE+"/nove_offsety.json","w"))
# vypis tri 1203
for key,nazev in (("130","Skoda 1203 Pajda karavan"),("131","TAZ 1203 valnik drevo"),("144","TAZ 1203 plachta bedna")):
    n=nove[key]
    print("=== 0x%02X %s ===" % (int(key), n["jm"]))
    print("  %-4s %10s %10s %12s" % ("dir","ted","nove","zmena x,y"))
    for k in range(8):
        print("  %-4s %5d,%-4d %5d,%-4d %7d,%-4d" % (SM[k], n["sxo"][k],n["syo"][k], n["xo"][k],n["yo"][k],
                                                    n["xo"][k]-n["sxo"][k], n["yo"][k]-n["syo"][k]))
    print()
