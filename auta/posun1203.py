# -*- coding: utf-8 -*-
"""Hracuv posun u dvanacttrojek: sprite 3 (JV) a 5 (JZ).
Cisla spritu od nuly. Posun se pricita k offsetum, na vsechny sady vozidla."""
import io, re, sys
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
p=BASE+"/krok2/sprites/VWT1.yagl"
SM=["N","NE","E","SE","S","SW","W","NW"]
# posun v offsetech (kotva se hybe opacne)
POSUN={3:(+4,-4), 5:(-4,-4)}
def je1203(jm):
    return True   # hrac: "vsechny i taz a vw"
L=io.open(p,encoding="utf-8").read().split("\n")
SPR=re.compile(r'\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\],')
cur=None; blok=[]; zmen=0; voz=set(); preskoc=set()
for i,l in enumerate(L):
    if re.match(r'    sprite_set // 0x[0-9A-F]+', l): cur=[]
    elif cur is not None and l.startswith("    }"):
        if len(cur)==8: blok.append(list(cur))
        cur=None
    elif cur is not None:
        if SPR.search(l): cur.append(i)
    m=re.match(r'\s*/\* 0x00([0-9A-F]{2}) \*/ "(.*)";', l)
    if m:
        jm=m.group(2)
        if je1203(jm):
            for sada in blok:
                for k,(dx,dy) in POSUN.items():
                    ln=sada[k]; g=SPR.search(L[ln])
                    w,h,xo,yo=(int(x) for x in g.groups())
                    L[ln]=SPR.sub("[%d, %d, %d, %d]," % (w,h,xo+dx,yo+dy), L[ln], count=1)
                    zmen+=1
            voz.add((m.group(1),jm,len(blok)))
        elif blok:
            preskoc.add((m.group(1),jm,len(blok)))
        blok=[]
io.open(p,"w",encoding="utf-8").write("\n".join(L))
print("POSUNUTO (dvanacttrojky):")
for v in sorted(voz): print("  0x%s %-34s %d sad" % v)
print("\nBEZE ZMENY:")
for v in sorted(preskoc): print("  0x%s %-34s %d sad" % v)
print("\nzmenenych spritu: %d  (= %d vozidel, sady, 2 sprity)" % (zmen, len(voz)))
