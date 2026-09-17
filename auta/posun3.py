# -*- coding: utf-8 -*-
"""Hracuv dalsi posun: jen sprite 3 (JV), vsechna auta.
Hrac pise cisla tak, jak je cte v souboru bez minusu (= kotva):
posun -1 +1 tam znamena v offsetech xoffs +1, yoffs -1."""
import io, re
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
p=BASE+"/krok3/sprites/VWT1.yagl"
POSUN={3:(+1,-1)}   # (dx pro xoffs, dy pro yoffs)
L=io.open(p,encoding="utf-8").read().split("\n")
SPR=re.compile(r'\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\],')
cur=None; blok=[]; zmen=0; voz=[]
for i,l in enumerate(L):
    if re.match(r'    sprite_set // 0x[0-9A-F]+', l): cur=[]
    elif cur is not None and l.startswith("    }"):
        if len(cur)==8: blok.append(list(cur))
        cur=None
    elif cur is not None and SPR.search(l): cur.append(i)
    m=re.match(r'\s*/\* 0x00([0-9A-F]{2}) \*/ "(.*)";', l)
    if m:
        for sada in blok:
            for k,(dx,dy) in POSUN.items():
                ln=sada[k]; g=SPR.search(L[ln])
                w,h,xo,yo=(int(x) for x in g.groups())
                L[ln]=SPR.sub("[%d, %d, %d, %d]," % (w,h,xo+dx,yo+dy), L[ln], count=1)
                zmen+=1
        if blok: voz.append((m.group(1),m.group(2),len(blok)))
        blok=[]
io.open(p,"w",encoding="utf-8").write("\n".join(L))
print("vozidel: %d, sad: %d, zmenenych spritu: %d" % (len(voz), sum(v[2] for v in voz), zmen))
