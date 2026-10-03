#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Nahled skladaneho pole z dlazdic (render_dlazdice.py) tak, jak by ho skladala hra: nejdriv zem vsech policek, pak
# vrstvy od zadu dopredu (podle x + y). Cesta je plny obrazek (ve hre prekryvajici, pod nim silnice), na konci cesty
# (x = 0) bouda, holky u okraju dvou dlazdic cesty.
#   python3 slozit_pole.py <adresar dlazdic> <zin 4|8> <vystupni adresar>
# Marihuana 5 x 4 (radky y 0, 1, 3 pole, y 2 cesta), brambory 3 x 3 (y 0, 2 pole, y 1 cesta), vzdy tri faze.
import json, os, sys
import numpy as np
from PIL import Image

D, ZIN, VYSTUP = sys.argv[1], int(sys.argv[2]), sys.argv[3]
os.makedirs(VYSTUP, exist_ok=True)
s = ZIN // 4
TU = os.path.dirname(os.path.abspath(__file__))

def nacti(jm):
    p = os.path.join(D, f"{jm}_zin{ZIN}.png")
    return Image.open(p).convert("RGBA") if os.path.exists(p) else None
info = json.load(open(os.path.join(D, f"cesta_zin{ZIN}.json"))) if os.path.exists(os.path.join(D, f"cesta_zin{ZIN}.json")) else \
    json.load(open(os.path.join(D, f"bram_zaklad_zin{ZIN}.json")))
NX, NY = (round(c) for c in info["rohy"]["sever"])
RAM_W, RAM_H = info["ram"]
def slozit(nx, ny, zem, vrstvy, jmeno):
    """zem(x, y) -> seznam obrazku zeme; vrstvy(x, y) -> seznam vrstev; policko (x, y) ma severni roh o
    (128 (y - x), 64 (x + y)) px ve 4x od severniho rohu policka (0, 0)"""
    W = 128 * s * (nx - 1 + ny - 1) + RAM_W; H = 64 * s * (nx - 1 + ny - 1) + RAM_H
    out = Image.new("RGBA", (W, H), (96, 128, 64, 255))
    pozice = {(x, y): (128 * s * (y - x + nx - 1), 64 * s * (x + y)) for x in range(nx) for y in range(ny)}
    poradi = sorted(pozice.items(), key=lambda k: (k[0][0] + k[0][1], k[0][1]))
    for (x, y), (px, py) in poradi:
        for im in zem(x, y):
            if im is not None: out.alpha_composite(im, (px, py))
    for (x, y), (px, py) in poradi:
        for im in vrstvy(x, y):
            if im is not None: out.alpha_composite(im, (px, py))
    out.convert("RGB").save(os.path.join(VYSTUP, jmeno))
    print("ulozeno", jmeno, out.size)
    return out

if os.path.exists(os.path.join(D, f"mari_zaklad_zin{ZIN}.png")):
    Z, C, BO = nacti("mari_zaklad"), nacti("cesta"), nacti("bouda")
    MA, VZ, HS, HJ = nacti("mari_male"), nacti("mari_vzrostle"), nacti("holky_sz"), nacti("holky_jv")
    CESTA_Y = 2
    # holky pri praci mezi kytkami (od 3. 10. vecer): kazda na sve dlazdici pole, vrstva podle faze (zakryvaji je
    # male, nebo vzrostle kytky); kladou se hned po kytkach sve dlazdice
    PRACE = {(1, 1): "prace_real", (3, 0): "prace_sedi", (2, 3): "prace_punk", (4, 1): "prace_pubg",
             (0, 3): "prace_char16", (4, 3): "prace_chill"}
    def zem(x, y):
        return [Z] if y != CESTA_Y else [C]
    for faze, kytky in ((1, None), (2, MA), (3, VZ)):
        def vrstvy(x, y, kytky=kytky, faze=faze):
            if y != CESTA_Y:
                return [kytky] + ([nacti(f"{PRACE[x, y]}_f{faze}")] if faze > 1 and (x, y) in PRACE else [])
            return ([BO] if x == 0 else []) + ([HS] if x == 2 else []) + ([HJ] if x == 3 else [])
        slozit(5, 4, zem, vrstvy, f"pole_marihuany_faze{faze}_zin{ZIN}.png")
if os.path.exists(os.path.join(D, f"bram_zaklad_zin{ZIN}.png")):
    Z, MA, VZ = nacti("bram_zaklad"), nacti("bram_male"), nacti("bram_vzrostle")
    C, BO = (nacti(j) or (Image.open(os.path.join(D, "..", "marihuana", f"{j}_zin{ZIN}.png")).convert("RGBA")
                              if os.path.exists(os.path.join(D, "..", "marihuana", f"{j}_zin{ZIN}.png")) else None)
                 for j in ("cesta", "bouda"))
    CESTA_Y = 1
    def zem(x, y):
        return [Z] if y != CESTA_Y else [C]
    for faze, kytky in ((1, None), (2, MA), (3, VZ)):
        def vrstvy(x, y, kytky=kytky):
            return [kytky] if y != CESTA_Y else ([BO] if x == 0 else [])
        slozit(3, 3, zem, vrstvy, f"pole_brambor_faze{faze}_zin{ZIN}.png")
