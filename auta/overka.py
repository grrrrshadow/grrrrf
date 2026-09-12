# -*- coding: utf-8 -*-
"""Kontrola: vsechna auta vedle sebe, kotva na spolecnem krizku."""
import io, json, os
from PIL import Image, ImageDraw
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/auta/s1203modradodavka/sprites")
voz=json.load(io.open(BASE+"/auta_sprity.json"))
N=json.load(io.open(BASE+"/nove_offsety.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]
cache={}
def sh(f):
    if f not in cache: cache[f]=Image.open(f).convert("RGBA")
    return cache[f]
Z=3
for smer,nazev in ((2,"E-bok"),(1,"NE-primy"),(0,"N-zataceni")):
    CW=120; CH=90
    out=Image.new("RGBA",(18*CW*Z, 2*CH*Z+24),(28,28,32,255)); dr=ImageDraw.Draw(out)
    for radek in (0,1):
        oy=radek*CH*Z+ (12 if radek else 0)
        cy=oy+int(CH*Z*0.62)
        dr.line([(0,cy),(out.size[0],cy)],fill=(255,80,80,220),width=1)
        dr.text((4,oy+2), ("TED" if radek==0 else "SPOLECNY ZAKLAD")+"  smer "+nazev, fill=(240,240,240,255))
        for i,(vid,jm,spr) in enumerate(voz):
            s=spr[smer]; n=N[str(vid)]
            xo,yo = (s["xo"],s["yo"]) if radek==0 else (n["xo"][smer],n["yo"][smer])
            cx=i*CW*Z+CW*Z//2
            im=sh(s["file"]).crop((s["x"],s["y"],s["x"]+s["w"],s["y"]+s["h"])).resize((s["w"]*Z,s["h"]*Z),Image.NEAREST)
            out.alpha_composite(im,(int(cx+xo*Z),int(cy+yo*Z)))
            dr.line([(cx,oy+10),(cx,oy+CH*Z-2)],fill=(120,160,255,170),width=1)
    out.save(BASE+"/overka_%s.png"%nazev); print(nazev, out.size)
