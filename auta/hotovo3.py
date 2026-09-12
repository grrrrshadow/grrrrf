# -*- coding: utf-8 -*-
"""Skoda dostane presne stejny vztah kotva<->kola jako ma VW T1, smer po smeru.
   VW T1 se nemeni vubec."""
import io, json, math
import numpy as np
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
voz=json.load(io.open(BASE+"/auta_sprity.json")); op=json.load(io.open(BASE+"/oprava.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]
AL=[math.radians(45*k) for k in range(8)]; CO=[math.cos(a) for a in AL]; SI=[math.sin(a) for a in AL]
T=0.5
PAR={0x80:dict(a=18.00,b=18.00*1.37/2.40), 0x82:dict(a=21.25,b=21.25*1.47/2.40)}
st={}
for cil in (0x80,0x82):
    o=op[str(cil)]; P=PAR[cil]
    st[cil]=dict(pu=np.array(o["po"]),
                 pv=np.array([o["dno"][k]-T*(P["a"]*abs(CO[k])+P["b"]*abs(SI[k])) for k in range(8)]),
                 ax=np.array(o["ax"],float), ay=np.array(o["ay"],float))
T1=st[0x80]
du=T1["ax"]-T1["pu"]; dv=T1["ay"]-T1["pv"]
print("VW T1 - poloha kotvy proti stredu rozvoru na vozovce (to je ta hotova konvence):")
print("  %-3s %10s %10s" % ("dir","vodorovne","svisle"))
for k in range(8): print("  %-3s %10.1f %10.1f" % (SM[k],du[k],dv[k]))
print()
S=st[0x82]; nx=S["pu"]+du; ny=S["pv"]+dv
for vid,jm,spr in voz:
    if vid!=0x82: continue
    print("=== Skoda 1203 (0x0082) - nove offsety ===")
    print("  %-3s %-12s | %5s %5s | %9s %6s | %9s %6s" %
          ("dir","","w","h","xoffs ted","novy","yoffs ted","novy"))
    for k in range(8):
        a=-int(round(nx[k])); b=-int(round(ny[k]))
        hv="primy smer" if k in (1,3,5,7) else "zataceni"
        print("  %-3s %-12s | %5d %5d | %9d %6d | %9d %6d    (%+d,%+d)" %
              (SM[k],hv,spr[k]["w"],spr[k]["h"],spr[k]["xo"],a,spr[k]["yo"],b,
               a-spr[k]["xo"], b-spr[k]["yo"]))
json.dump(dict({"130":dict(nx=list(nx),ny=list(ny),ax=list(S["ax"]),ay=list(S["ay"]),
                           pu=list(S["pu"]),pv=list(S["pv"]))},
               **{"128":dict(nx=list(T1["ax"]),ny=list(T1["ay"]),ax=list(T1["ax"]),ay=list(T1["ay"]),
                             pu=list(T1["pu"]),pv=list(T1["pv"]))}),
          io.open(BASE+"/hotovo.json","w"))
