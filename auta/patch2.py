# -*- coding: utf-8 -*-
"""Prepise 8 offsetu Skody 1203 primo v yaglu rozbaleneho hotoveho GRF."""
import io, re, json
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
H=json.load(io.open(BASE+"/hotovo.json"))["130"]
NOVE=[(-int(round(H["nx"][k])), -int(round(H["ny"][k]))) for k in range(8)]
p=BASE+"/zorig/sprites/VWT1.yagl"
lines=io.open(p,encoding="utf-8").read().split("\n")
SPR=re.compile(r'\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\],')
sada=[];posl=None;v=False;hotovo=False
for i,l in enumerate(lines):
    if l.startswith("    sprite_set"): v=True;sada=[]
    elif v and l.startswith("    }"):
        if len(sada)==8: posl=list(sada)
        v=False
    elif v and SPR.search(l): sada.append(i)
    m=re.match(r'\s*/\* 0x00([0-9A-F]{2}) \*/ "(.*)";', l)
    if m and posl:
        if int(m.group(1),16)==0x82:
            for k,ln in enumerate(posl):
                g=SPR.search(lines[ln])
                stary=(int(g.group(3)),int(g.group(4)))
                w,h=int(g.group(1)),int(g.group(2))
                lines[ln]=SPR.sub("[%d, %d, %d, %d]," % (w,h,NOVE[k][0],NOVE[k][1]), lines[ln], count=1)
                print("  sprite %d  [%d, %d]  %s -> %s" % (k,w,h,stary,NOVE[k]))
            print("0x82 %s: prepsano na radcich %d..%d" % (m.group(2), posl[0]+1, posl[-1]+1))
            hotovo=True
        posl=None
assert hotovo, "Skoda nenalezena"
io.open(p,"w",encoding="utf-8").write("\n".join(lines))
