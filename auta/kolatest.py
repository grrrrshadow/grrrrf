# -*- coding: utf-8 -*-
"""Kontrola modelu: nakresli promitnuty obdelnik rozvor x rozchod na kola."""
import io, json, os, math
import numpy as np
from PIL import Image, ImageDraw
BASE = "/tmp/claude-0/-home-user-forclaude/a279456f-73fc-5ed8-ace3-5cf5b22fbe35/scratchpad"
os.chdir(BASE + "/auta/s1203modradodavka/sprites")
voz = json.load(io.open(BASE + "/auta_sprity.json"))
op  = json.load(io.open(BASE + "/oprava.json"))
SM = ["N","NE","E","SE","S","SW","W","NW"]
T = 0.5   # svisle zkraceni zeme (OTTD 2:1)
cache={}
def sh(f):
    if f not in cache: cache[f]=Image.open(f).convert("RGBA")
    return cache[f]

PAR = {0x80: dict(a=18.0, pomer=1.37/2.40, jm="vwt1"),
       0x82: dict(a=21.25, pomer=1.47/2.40, jm="skoda")}

for cil in (0x80, 0x82):
    o = op[str(cil)]; P = PAR[cil]
    a = P["a"]; b = a*P["pomer"]
    po = o["po"]; dno = o["dno"]
    # svisla poloha pocatku: v bocnim pohledu jsou kola o T*b nize
    # pocatek se promita po celem otoceni stejne -> urcim ho ze smeru 2 a dopocitam
    # pres tuhy posun kotvy (kotva = pocatek + posun)
    for vid,jm,spr in voz:
        if vid!=cil: continue
        Z=4
        CW = max(s["w"] for s in spr)+40; CH = max(s["h"] for s in spr)+40
        out = Image.new("RGBA",(8*CW*Z, CH*Z),(30,30,34,255)); dr=ImageDraw.Draw(out)
        pv0 = dno[2] - T*b            # pocatek v ve smeru 2 (sprite souradnice)
        for k,s in enumerate(spr):
            al = math.radians(45*k); c, sn = math.cos(al), math.sin(al)
            cx = k*CW*Z + (CW*Z)//2; cy = (CH*Z)//2
            im = sh(s["file"]).crop((s["x"],s["y"],s["x"]+s["w"],s["y"]+s["h"]))
            im = im.resize((s["w"]*Z,s["h"]*Z), Image.NEAREST)
            # pocatek: u = po[k], v = dno[k] - (podpora dna) ... misto toho pouzij
            # ze pocatek je tuhy bod -> jeho v urcim tak, aby kola sedla; zde
            # odhad: v = dno[k] - T*(a*|cos|+b*|sin|)
            pv = dno[k] - T*(a*abs(c)+b*abs(sn))
            out.alpha_composite(im, (int(cx-po[k]*Z), int(cy-pv*Z)))
            for ex in (+1,-1):
                for dy_ in (+1,-1):
                    Px, Py = ex*a, dy_*b
                    u = -Px*sn + Py*c; v = (Px*c + Py*sn)*T
                    X = cx+u*Z; Y = cy+v*Z
                    dr.ellipse([X-4,Y-4,X+4,Y+4], outline=(255,60,60,255), width=2)
            dr.ellipse([cx-3,cy-3,cx+3,cy+3], fill=(255,255,0,255))
            dr.text((k*CW*Z+4,4), SM[k], fill=(230,230,230,255))
        out.save(BASE+"/kolatest_%s.png" % P["jm"]); print(P["jm"], out.size)
