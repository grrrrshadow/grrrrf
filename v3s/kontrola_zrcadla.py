# -*- coding: utf-8 -*-
# Zrcadlova kontrola stredu (hrac 28. 9.: "a zrcadlova verifikace stredu", postup v temata3.md,
# "Zarovnani spritu auticek"). Pohled pod azimutem -a je presne vodorovne zrcadlo pohledu +a, takze
# smer k a smer 8-k jsou zrcadla (SV-SZ, V-Z, JV-JZ) a sever a jih jsou zrcadlem sami sobe.
# Kdyz je kotva (bod -xoffs, -yoffs) na aute vsude tentyz bod, musi zrcadlo spritu 8-k polozene podle
# svych offsetu padnout presne na sprite k. Skript hleda posun, pri kterem se siluety kryji nejlip
# (nejvetsi IoU), a vypise ho: 0, 0 znamena, ze kotva sedi.
#   python3 kontrola_zrcadla.py <rozbaleny adresar sprites/> <soubor.yagl>
import os, re, sys
import numpy as np
from PIL import Image

ADR, YAGL = sys.argv[1], sys.argv[2]
text = open(os.path.join(ADR, YAGL), encoding="utf-8").read()
listy = {}
def obrazek(png, x, y, w, h):
    if png not in listy: listy[png] = Image.open(os.path.join(ADR, png)).convert("RGBA")
    return np.array(listy[png].crop((x, y, x + w, y + h)))[..., 3] > 32

sady = []
for rec in re.findall(r"sprite_sets<RoadVehicles[^>]*>.*?\n\}", text, re.S):
    for blok in re.split(r"\n    sprite_set", rec)[1:]:
        sp = [tuple(int(v) if i != 4 else v for i, v in enumerate(m.groups())) for m in re.finditer(
            r"\[(\d+), (\d+), (-?\d+), (-?\d+)\], zin4, [^\"]*\"([^\"]+)\", \[(\d+), (\d+)\]", blok)]
        if len(sp) == 8 and min(s[0] for s in sp) > 1:
            sady.append(sp)

def plocha(maska, xo, yo, R=160):
    """maska polozena tak, ze kotva je uprostred platna 2R x 2R"""
    p = np.zeros((2 * R, 2 * R), bool)
    h, w = maska.shape
    p[R + yo:R + yo + h, R + xo:R + xo + w] = maska
    return p

def srovnej(a, b, rozsah=12):
    nej = (0, None, None)
    for dy in range(-rozsah, rozsah + 1):
        for dx in range(-rozsah, rozsah + 1):
            bb = np.roll(np.roll(b, dy, 0), dx, 1)
            prunik = (a & bb).sum(); sjed = (a | bb).sum()
            if prunik < 0.5 * min(a.sum(), b.sum()): continue
            iou = prunik / sjed
            if iou > nej[0]: nej = (iou, dx, dy)
    return nej

JM = ["S", "SV", "V", "JV", "J", "JZ", "Z", "SZ"]
nejhorsi = 0
for si, sp in enumerate(sady):
    masky = [(obrazek(png, x, y, w, h), xo, yo) for (w, h, xo, yo, png, x, y) in sp]
    radky = []
    for k, z in ((0, 0), (4, 4), (1, 7), (2, 6), (3, 5)):
        m, xo, yo = masky[k]
        mz, xoz, yoz = masky[z]
        a = plocha(m, xo, yo)
        b = plocha(mz[:, ::-1], -xoz - mz.shape[1], yoz)
        iou, dx, dy = srovnej(a, b)
        nejhorsi = max(nejhorsi, abs(dx), abs(dy))
        co = f"{JM[k]} sam se sebou" if k == z else f"{JM[k]}-{JM[z]}"
        pozn = f"kotva {dx / 2:+.1f} px od osy" if k == z else f"kotvy od sebe {dx:+d}, {dy:+d} px"
        radky.append(f"  {co:14s} shoda {iou:.2f}, posun {dx:+d} {dy:+d}  ({pozn})")
    print(f"sada {si}:"); print("\n".join(radky))
print(f"nejvetsi odchylka {nejhorsi} px")
