# -*- coding: utf-8 -*-
import io, json, math
import numpy as np
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
V=json.load(io.open(BASE+"/mereni58.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]
AL=[math.radians(45*k) for k in range(8)]; CO=[math.cos(a) for a in AL]; SI=[math.sin(a) for a in AL]
Mu=np.array([[1.0,s,c] for c,s in zip(CO,SI)]); Mv=np.array([[1.0,c,s] for c,s in zip(CO,SI)])
R=[v for v in V if v["vid"]==0x81 and v["sada"]=="0x0000"][0]
du=np.array([-x for x in R["xo"]])-np.array(R["pu"]); dv=np.array([-y for y in R["yo"]])-np.array(R["pv"])
cu,*_=np.linalg.lstsq(Mu,du,rcond=None); cv,*_=np.linalg.lstsq(Mv,dv,rcond=None)
DU=Mu.dot(cu); DV=Mv.dot(cv)
print("Konvence VW T1 origsize, prolozena tuhym bodem:")
for k in range(8): print("  %-3s vodorovne %+6.1f  svisle %+6.1f   (namereno %+6.1f %+6.1f)" % (SM[k],DU[k],DV[k],du[k],dv[k]))
print()
for v in V:
    nx=np.array(v["pu"])+DU; ny=np.array(v["pv"])+DV
    v["nxo"]=[-int(round(x)) for x in nx]; v["nyo"]=[-int(round(y)) for y in ny]
json.dump(V, io.open(BASE+"/nove58.json","w"))
# kontrola: shoda mezi sadami tehoz vozidla (stejny podvozek -> stejna zmena)
print("Kontrola shody mezi sadami tehoz vozidla (rozptyl kotvy proti podvozku):")
from collections import defaultdict
g=defaultdict(list)
for v in V: g[v["vid"]].append(v)
for vid,ls in sorted(g.items()):
    if len(ls)<2: continue
    d=[]
    for k in range(8):
        xs=[l["nxo"][k]-(-l["pu"][k]) for l in ls]; ys=[l["nyo"][k]-(-l["pv"][k]) for l in ls]
        d.append(max(xs)-min(xs)); d.append(max(ys)-min(ys))
    print("  0x%02X %-30s max rozdil %.1f px" % (vid, ls[0]["jm"], max(d)))
