# -*- coding: utf-8 -*-
# Porovnani s VW T1 orig size (hracova reference, "linka mezi koly"): v kazdem smeru se sprity polozi
# kotvou na spolecny krizek, vedle sebe VW T1, V3S mala a V3S velka. Pod kazdym je vodorovna cara
# ve vysce spodku siluety (linka kol) a svisla cara stredu. Vypise, kde lezi linka kol a stred
# siluety proti kotve.
#   python3 kontrola_vw.py <vw sprites/> <vw.yagl> <cislo zaznamu s VW> <v3s mala sprites/> <yagl> <v3s velka sprites/> <yagl> <vystup.png>
import os, re, sys
import numpy as np
from PIL import Image, ImageDraw

def sady(adr, yagl, zaznam=None):
    text = open(os.path.join(adr, yagl), encoding="utf-8").read()
    if zaznam is not None:
        text = text.split(f"// Record #{zaznam}\n", 1)[1].split("// Record #", 1)[0]
    out = []
    for rec in re.findall(r"sprite_sets<RoadVehicles[^>]*>.*?\n\}", text, re.S):
        for blok in re.split(r"\n    sprite_set", rec)[1:]:
            sp = [tuple(int(v) if i != 4 else v for i, v in enumerate(m.groups())) for m in re.finditer(
                r"\[(\d+), (\d+), (-?\d+), (-?\d+)\], zin4, [^\"]*\"([^\"]+)\", \[(\d+), (\d+)\]", blok)]
            if len(sp) == 8 and min(s[0] for s in sp) > 1: out.append(sp)
    return out

_l = {}
def vyrez(adr, s):
    w, h, xo, yo, png, x, y = s
    k = os.path.join(adr, png)
    if k not in _l: _l[k] = Image.open(k).convert("RGBA")
    return _l[k].crop((x, y, x + w, y + h)), xo, yo

a = sys.argv[1:]
vw = sady(a[0], a[1], int(a[2]))[0]
mala = sady(a[3], a[4])[0]
velka = sady(a[5], a[6])[0]
radky = [("VW T1 orig size", a[0], vw), ("V3S malá", a[3], mala), ("V3S velká", a[5], velka)]
BUN = 190; R = 95
obr = Image.new("RGBA", (BUN * 8, BUN * 3 + 20), (120, 124, 116, 255))
d = ImageDraw.Draw(obr)
JM = ["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ"]
for ri, (jm, adr, sp) in enumerate(radky):
    for k in range(8):
        im, xo, yo = vyrez(adr, sp[k])
        cx, cy = k * BUN + R, 20 + ri * BUN + R
        obr.alpha_composite(im, (cx + xo, cy + yo))
        al = np.array(im)[..., 3] > 32
        spodek = cy + yo + np.nonzero(al.any(1))[0].max()
        d.line([(k * BUN + 10, spodek + 1), (k * BUN + BUN - 10, spodek + 1)], fill=(255, 220, 0, 255))
        d.line([(cx - 6, cy), (cx + 6, cy)], fill=(255, 0, 0, 255)); d.line([(cx, cy - 6), (cx, cy + 6)], fill=(255, 0, 0, 255))
        sl = np.nonzero(al.any(0))[0]
        print(f"{jm:16s} {JM[k]:2s} linka kol {spodek - cy:+4d} px pod kotvou, silueta {cx + xo + sl.min() - cx:+4d} az {cx + xo + sl.max() - cx:+4d}")
    d.text((4, 4 + ri * BUN + 18), jm, fill=(255, 255, 255, 255))
for k in range(8): d.text((k * BUN + R - 6, 4), JM[k], fill=(255, 255, 255, 255))
obr.save(a[7])
