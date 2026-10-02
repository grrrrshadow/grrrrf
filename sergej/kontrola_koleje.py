# -*- coding: utf-8 -*-
# Kontrola zarovnani na kolej: rozbaleny GRF (yagl -d) se postavi do vsech 8 smeru tak, jak ho
# kresli hra (hra.py), a pod nej se nakresli kolejnice. Zoom 4 (zin4) nebo 8 (zin8, vse dvojnasobne).
#   python3 kontrola_koleje.py <rozbaleny adresar sprites> <jmeno.yagl> <orig|bryle> <vystup.png> [4|8]
import sys, os
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hra import ROVNE, SMER, remap, kotva_hry, odstupy, nacti_sady, obrazek

SD, YG, VAR, OUT = sys.argv[1:5]
ZIN = int(sys.argv[5]) if len(sys.argv) > 5 else 4
M = ZIN // 4
DELKY = {"orig": (2, 8, 2), "bryle": (3, 8, 3)}[VAR]
N_H, N_Z = odstupy(DELKY)
sady = nacti_sady(SD, YG, ZIN)     # pro kazdy nater: hlava, stred, zad, nakup
NATERY = ("zeleny", "cerveny", "rzd")
bunky = []
W, H = 520 * M, 300 * M
for b, n in enumerate(NATERY):
    b *= 4
    for d in range(8):
        c = Image.new("RGBA", (W, H), (96, 118, 74, 255)); dr = ImageDraw.Draw(c)
        ox, oy = W // 2, H // 2 + 20 * M
        ux, uy = SMER[d]; px, py = -uy, ux; norm = (px * px + py * py) ** 0.5
        for strana in (-0.49, 0.49):          # kolejnice: rozchod 1435 mm pri ~1,47 m na osminu
            ax, ay = px / norm * strana, py / norm * strana
            p1 = remap(ax - 12 * ux, ay - 12 * uy); p2 = remap(ax + 12 * ux, ay + 12 * uy)
            dr.line((ox + M * p1[0], oy + M * p1[1], ox + M * p2[0], oy + M * p2[1]), fill=(230, 230, 230, 255), width=M)
        dily = [(sady[b][d], (N_H * ux, N_H * uy), DELKY[0]), (sady[b + 1][d], (0, 0), DELKY[1]),
                (sady[b + 2][d], (-N_Z * ux, -N_Z * uy), DELKY[2])]
        dily.sort(key=lambda t: t[1][0] + t[1][1])            # nejdriv to, co je od divaka dal
        for sp, (wx, wy), L in dily:
            im, xo, yo = obrazek(SD, sp)
            if im.size == (1, 1): continue
            sx, sy = remap(wx + kotva_hry(L, d)[0], wy + kotva_hry(L, d)[1])
            c.alpha_composite(im, (ox + M * sx + xo, oy + M * sy + yo))
        for wx, wy in ((N_H * ux, N_H * uy), (0, 0), (-N_Z * ux, -N_Z * uy)):
            sx, sy = remap(wx, wy); dr.line((ox + M * sx - 3, oy + M * sy, ox + M * sx + 3, oy + M * sy), fill=(255, 0, 0, 255))
        dr.text((4, 4), f"{n} zin{ZIN} smer {d}", fill=(255, 255, 255, 255))
        bunky.append(c)
out = Image.new("RGBA", (W * 4, H * len(NATERY) * 2), (30, 30, 30, 255))
for i, c in enumerate(bunky):
    out.alpha_composite(c, ((i % 4) * W, (i // 4) * H))
out.save(OUT); print(OUT, out.size)
