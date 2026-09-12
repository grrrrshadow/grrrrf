# -*- coding: utf-8 -*-
"""Prepise offsety vsech 18 vozidel v rozbalenem hotovem GRF."""
import io, re, json
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
N=json.load(io.open(BASE+"/nove_offsety.json"))
p=BASE+"/zorig2/sprites/VWT1.yagl"
lines=io.open(p,encoding="utf-8").read().split("\n")
SPR=re.compile(r'\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\],')
sada=[];posl=None;v=False;pocet=0
for i,l in enumerate(lines):
    if l.startswith("    sprite_set"): v=True;sada=[]
    elif v and l.startswith("    }"):
        if len(sada)==8: posl=list(sada)
        v=False
    elif v and SPR.search(l): sada.append(i)
    m=re.match(r'\s*/\* 0x00([0-9A-F]{2}) \*/ "(.*)";', l)
    if m and posl:
        vid=int(m.group(1),16)
        if str(vid) in N:
            n=N[str(vid)]
            for k,ln in enumerate(posl):
                g=SPR.search(lines[ln]); w,h=int(g.group(1)),int(g.group(2))
                assert (int(g.group(3)),int(g.group(4)))==(n["sxo"][k],n["syo"][k]), (vid,k,g.groups(),n["sxo"][k],n["syo"][k])
                lines[ln]=SPR.sub("[%d, %d, %d, %d]," % (w,h,n["xo"][k],n["yo"][k]), lines[ln], count=1)
            pocet+=1
            print("0x%02X %-32s prepsano" % (vid, m.group(2)))
        posl=None
print("vozidel:", pocet)
io.open(p,"w",encoding="utf-8").write("\n".join(lines))
