# -*- coding: utf-8 -*-
"""Prepise offsety ve vsech 58 sadach rozbaleneho puvodniho GRF."""
import io, re, json
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
V=json.load(io.open(BASE+"/nove58.json"))
p=BASE+"/zpuv/sprites/VWT1.yagl"
L=io.open(p,encoding="utf-8").read().split("\n")
SPR=re.compile(r'\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\],')
zm=0
for v in V:
    for k,ln in enumerate(v["radky"]):
        g=SPR.search(L[ln]); assert g, (v["vid"],ln)
        w,h,xo,yo=(int(x) for x in g.groups())
        assert (xo,yo)==(v["xo"][k],v["yo"][k]), (hex(v["vid"]),v["sada"],k,(xo,yo),(v["xo"][k],v["yo"][k]))
        L[ln]=SPR.sub("[%d, %d, %d, %d]," % (w,h,v["nxo"][k],v["nyo"][k]), L[ln], count=1)
        if (xo,yo)!=(v["nxo"][k],v["nyo"][k]): zm+=1
io.open(p,"w",encoding="utf-8").write("\n".join(L))
print("sad:", len(V), " zmenenych spritu:", zm, "z", 8*len(V))
