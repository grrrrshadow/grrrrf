# -*- coding: utf-8 -*-
"""Zakladni sada (0x0000) vsech 18 aut: ted vs po zarovnani."""
import io, json, os
from PIL import Image, ImageDraw
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/zpuv/sprites")
V=json.load(io.open(BASE+"/nove58.json")); S=json.load(io.open(BASE+"/sady.json"))
sp={(s["vid"],s["sada"]):s["spr"] for s in S}
zakl=[v for v in V if v["sada"]=="0x0000"]
SM=["N","NE","E","SE","S","SW","W","NW"]
cache={}
def sh(f):
    if f not in cache: cache[f]=Image.open(f).convert("RGBA")
    return cache[f]
Z=3
for smer,nm in ((2,"E-bok"),(1,"NE-primy")):
    CW=115; CH=95
    out=Image.new("RGBA",(len(zakl)*CW*Z, 2*CH*Z+20),(28,28,32,255)); dr=ImageDraw.Draw(out)
    for radek in (0,1):
        oy=radek*CH*Z+(10 if radek else 0); cy=oy+int(CH*Z*0.60)
        dr.line([(0,cy),(out.size[0],cy)],fill=(255,80,80,230),width=2)
        dr.text((4,oy+2),("TED (nenalozene)" if radek==0 else "PO ZAROVNANI")+u"   smer "+nm,fill=(245,245,245,255))
        for i,v in enumerate(zakl):
            s=sp[(v["vid"],"0x0000")][smer]
            xo,yo=(v["xo"][smer],v["yo"][smer]) if radek==0 else (v["nxo"][smer],v["nyo"][smer])
            cx=i*CW*Z+CW*Z//2
            im=sh(s["file"]).crop((s["x"],s["y"],s["x"]+s["w"],s["y"]+s["h"])).resize((s["w"]*Z,s["h"]*Z),Image.NEAREST)
            out.alpha_composite(im,(int(cx+xo*Z),int(cy+yo*Z)))
            dr.line([(cx,oy+10),(cx,oy+CH*Z-2)],fill=(120,160,255,160),width=1)
    out.save(BASE+"/zaklad_%s.png"%nm)
    w=out.size[0]//2
    out.crop((0,0,w,out.size[1])).save(BASE+"/zaklad_%s_1.png"%nm)
    out.crop((w,0,out.size[0],out.size[1])).save(BASE+"/zaklad_%s_2.png"%nm)
    print(nm, out.size)
