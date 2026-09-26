# -*- coding: utf-8 -*-
# Kontrola spoju na rovne koleji: kusy hlavy, stredu a zadi z rozbaleneho GRF postavene na herni
# polohy musi dat presne puvodni fotku (rozdil nejvys 1 ze zaokrouhleni).
#   python3 kontrola_spoju.py <rozbaleny adresar sprites> <jmeno.yagl> <orig|bryle> <adresar s fotkami>
import sys, os, json
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hra import ROVNE, SMER, remap, kotva_hry, odstupy, nacti_sady, obrazek

SD, YG, VAR, FOTKY = sys.argv[1:5]
DELKY = {"orig": (2, 8, 2), "bryle": (3, 8, 3)}[VAR]
N_H, N_Z = odstupy(DELKY)
sady = nacti_sady(SD, YG)
spatne = 0
for n, b in (("zeleny", 0), ("cerveny", 4)):
    info = json.load(open(os.path.join(FOTKY, f"{VAR}_{n}", "kotvy.json")))
    for d in ROVNE:
        ux, uy = SMER[d]; o = 300
        platno = np.zeros((700, 700, 4), int)
        for sp, (wx, wy), L in ((sady[b][d], (N_H * ux, N_H * uy), DELKY[0]), (sady[b + 1][d], (0, 0), DELKY[1]),
                                (sady[b + 2][d], (-N_Z * ux, -N_Z * uy), DELKY[2])):
            im, xo, yo = obrazek(SD, sp)
            sx, sy = remap(wx + kotva_hry(L, d)[0], wy + kotva_hry(L, d)[1])
            a = np.array(im).astype(int); m = a[..., 3] > 0          # kusy se neprekryvaji: vlozit, ne michat
            X, Y = o + sx + xo, o + sy + yo
            platno[Y:Y + im.height, X:X + im.width][m] = a[m]
        foto = np.array(Image.open(os.path.join(FOTKY, f"{VAR}_{n}", f"d{d}.png")).convert("RGBA")).astype(int)
        kx, ky = info["smery"][str(d)]["kotva"]; rx, ry = remap(*kotva_hry(DELKY[1], d))
        fx = o + rx + int(round(-kx - rx)); fy = o + ry + int(round(-ky - ry))
        ref = np.zeros_like(platno); ref[fy:fy + foto.shape[0], fx:fx + foto.shape[1]] = foto
        rozdil = np.abs(platno - ref).max(axis=2)
        print(f"{VAR} {n} smer {d}: nejvetsi rozdil {rozdil.max()}, pixelu s rozdilem > 2: {(rozdil > 2).sum()}")
        spatne += (rozdil > 2).sum()
print("SPOJE V PORADKU" if spatne == 0 else f"SPATNE PIXELY: {spatne}")
