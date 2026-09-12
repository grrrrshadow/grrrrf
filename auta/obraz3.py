# -*- coding: utf-8 -*-
import io, json, os, math
from PIL import Image, ImageDraw
BASE="/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE+"/auta/s1203modradodavka/sprites")
voz=json.load(io.open(BASE+"/auta_sprity.json")); H=json.load(io.open(BASE+"/hotovo.json"))
SM=["N","NE","E","SE","S","SW","W","NW"]; T=0.5
PAR={0x80:dict(a=18.00,b=18.00*1.37/2.40,jm="vwt1",nm="VW T1 (nemeni se)"),
     0x82:dict(a=21.25,b=21.25*1.47/2.40,jm="skoda",nm="Skoda 1203")}
cache={}
def sh(f):
    if f not in cache: cache[f]=Image.open(f).convert("RGBA")
    return cache[f]
for cil in (0x80,0x82):
    P=PAR[cil]; h=H[str(cil)]
    for vid,jm,spr in voz:
        if vid!=cil: continue
        Z=4; CW=max(s["w"] for s in spr)+50; CH=max(s["h"] for s in spr)+40
        rady=[(h["ax"],h["ay"],"TED")] + ([] if cil==0x80 else [(h["nx"],h["ny"],"OPRAVENO")])
        out=Image.new("RGBA",(8*CW*Z, len(rady)*CH*Z+len(rady)*10*Z),(28,28,32,255)); dr=ImageDraw.Draw(out)
        for r,(kx,ky,pop) in enumerate(rady):
            oy=r*(CH*Z+10*Z)
            for k,s in enumerate(spr):
                al=math.radians(45*k); c,sn=math.cos(al),math.sin(al)
                cx=k*CW*Z+(CW*Z)//2; cy=oy+(CH*Z)//2+8*Z
                im=sh(s["file"]).crop((s["x"],s["y"],s["x"]+s["w"],s["y"]+s["h"]))
                im=im.resize((s["w"]*Z,s["h"]*Z),Image.NEAREST)
                out.alpha_composite(im,(int(cx-kx[k]*Z),int(cy-ky[k]*Z)))
                # vozovka: stred rozvoru na zemi, posunuty o (kotva - pocatek) daneho radku
                gx=cx-(kx[k]-h["pu"][k])*Z; gy=cy-(ky[k]-h["pv"][k])*Z
                rohy=[]
                for ex,dy_ in ((1,1),(1,-1),(-1,-1),(-1,1)):
                    Px,Py=ex*P["a"],dy_*P["b"]
                    rohy.append((gx+(-Px*sn+Py*c)*Z, gy+((Px*c+Py*sn)*T)*Z))
                dr.polygon(rohy,outline=(255,70,70,255))
                for q in rohy: dr.ellipse([q[0]-4,q[1]-4,q[0]+4,q[1]+4],outline=(255,70,70,255),width=2)
                dr.ellipse([cx-4,cy-4,cx+4,cy+4],fill=(255,240,60,255))
                dr.text((k*CW*Z+6,oy+4),"%s  %s"%(SM[k],pop),fill=(235,235,235,255))
        out.save(BASE+"/oprava_%s.png"%P["jm"]); print(P["jm"],out.size)
