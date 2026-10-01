# -*- coding: utf-8 -*-
# Divky u otevrenych dveri TAZ 1203, TAZ 1500 busu a Skody 1203 Pajda karavan, kdyz stoji na zastavce (sada spritu
# "na zastavce", dvere otevrene). Hrac 1. 10.: "holka u tech otevrenych dveri, muze byt i vzadu u dveri kufru, klidne
# dve", "nesmi vstoupit do vozovky ke kufru, aby nebyl konflikt s dalsim autem, nesmi za bilou caru silnice, jen
# z boku ke kufru a k prednim dverim", velikost 2x jako na zastavce.
#
#   python3 holky_u_aut.py foto              vyfoti divky (postavy/fotka_postavy.py) do foto/
#   python3 holky_u_aut.py vrstvy            slozi obrazky vrstev do vrstvy/ a vrstvy/holky.json
#   python3 holky_u_aut.py nahled <yagl> <list.png> <vystup.png>   nahled na autech z rozbaleneho GRF dodavek
#
# Obe divky stoji na prave strane auta (k chodniku): A (Character Girl, s kabelkou) u prednich dveri, B (College Girl,
# tmavovlasa) z boku u kufru. Ve smerech 1 a 3 je prava strana k divakovi, divky jsou pred autem (vrstva po aute).
# Ve smerech 5 a 7 je prava strana odvracena, divka stoji za autem (vrstva pred autem, auto ji zakryje); je tam jen ta,
# ktera je videt z boku za koncem auta, druha by koukala jen hrudnikem nad strechou.
import json, os, subprocess, sys
import numpy as np
from PIL import Image

TU = os.path.dirname(os.path.abspath(__file__))
FOTO = os.path.join(TU, "foto")
VRSTVY = os.path.join(TU, "vrstvy")
MERITKO = 2.0                       # jako divky na zastavce a budovy
RAM = 120                           # px fotky, chodidla presne uprostred

DIVKY = {"A": dict(postava="character_people_girl_001", poza="stoji", vyska=1.68),
         "B": dict(postava="college_girl", poza="ruce_dolu", vyska=1.62)}
# smer jizdy (cislo spritu) -> [(divka, a, c, natoceni)]
#   a: jednotky delky hry dopredu od stredu rozvoru (predni naprava +1,9, zadni naraznik -3,5)
#   c: jednotky ven od linky kol na prave strane (bok karoserie +0,35)
#   natoceni jako u postavy/fotka_postavy.py: 0 k jihozapadu, 45 k divakovi, 90 k jihovychodu, 180 k severovychodu
MISTA = {1: [("A", 1.6, 1.8, 65), ("B", -3.1, 1.5, 0)],
         3: [("A", 1.6, 1.8, 25), ("B", -3.1, 1.5, 300)],
         5: [("A", 1.6, 1.8, 90)],
         7: [("B", -3.1, 1.5, 90)]}
# c o pul jednotky dal nez v prvnim nahledu: ve hre (CZTR silnice) stala divka u auta v blizsim pruhu chodidly na bile
# care, takhle stoji na chodniku (hrac: "nesmi za bilou caru silnice")

# Geometrie auta v souradnicich kotvy spritu (4x): N je bod na vozovce mezi blizkymi koly (zmereno na TAZ 1203 bus 0x8C,
# sada na zastavce; ostatni busy a Pajda jsou zarovnane na stejnou linku kol, auta/README.md), F je smer dopredu
# a NV smer k divakovi, oboji na jednotku delky hry. Prava strana je k divakovi ve smerech 1 a 3.
N = {1: (2.6, 26.0), 3: (-5.6, 22.1), 5: (19.6, 22.0), 7: (0.1, 26.0)}
F = {1: (8, -4), 3: (8, 4), 5: (-8, 4), 7: (-8, -4)}
NV = {1: (8, 4), 3: (-8, 4), 5: (8, 4), 7: (-8, 4)}
ROZCHOD = 2.2                       # od linky blizkych kol ke vzdalenym
PRAVA_K_DIVAKOVI = {1: True, 3: True, 5: False, 7: False}


def foto_jmeno(divka, natoceni):
    return os.path.join(FOTO, f"{divka.lower()}_k{MERITKO:g}_s{natoceni}.png")


def bod(k, a, c):
    """(x, y) chodidel v souradnicich kotvy a jestli je divka za autem"""
    za = not PRAVA_K_DIVAKOVI[k]
    cc = -(ROZCHOD + c) if za else c
    return N[k][0] + a * F[k][0] + cc * NV[k][0], N[k][1] + a * F[k][1] + cc * NV[k][1], za


def foto():
    os.makedirs(FOTO, exist_ok=True)
    potreba = sorted({(d, s) for m in MISTA.values() for d, _, _, s in m})
    for d, s in potreba:
        cil = foto_jmeno(d, s)
        if os.path.exists(cil):
            continue
        p = DIVKY[d]
        env = dict(os.environ, POSTAVA=p["postava"], POZA=p["poza"], VYSKA=str(p["vyska"]), SMER=str(s),
                   MERITKO=str(MERITKO), SAMPLES="64", RAM=str(RAM), STIN="0")
        subprocess.run([sys.executable, os.path.join(TU, "..", "postavy", "fotka_postavy.py"), cil], env=env, check=True,
                       cwd=os.path.join(TU, "..", "postavy"), stdout=subprocess.DEVNULL)
        print("vyfoceno", cil)


def vrstvy():
    """obrazky vrstev pro smery 0-7: (za autem, pred autem); prazdne smery 1 x 1 pruhledny"""
    os.makedirs(VRSTVY, exist_ok=True)
    popis = {"meritko": MERITKO, "za": [], "pred": []}
    for k in range(8):
        for druh in ("za", "pred"):
            platno = np.zeros((400, 400, 4), np.uint8)
            O = 200                                    # kotva uprostred platna
            img = Image.fromarray(platno, "RGBA")
            kusy = []
            for d, a, c, s in MISTA.get(k, []):
                x, y, za = bod(k, a, c)
                if za != (druh == "za"):
                    continue
                kusy.append((y, Image.open(foto_jmeno(d, s)).convert("RGBA"), x))
            for y, g, x in sorted(kusy, key=lambda t: t[0]):        # vzdalenejsi driv
                img.alpha_composite(g, (O + round(x - g.width / 2), O + round(y - g.height / 2)))
            bb = img.getbbox()
            jm = f"{druh}_{k}.png"
            if bb is None:
                Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(os.path.join(VRSTVY, jm))
                popis[druh].append({"soubor": jm, "w": 1, "h": 1, "xo": 0, "yo": 0})
            else:
                img.crop(bb).save(os.path.join(VRSTVY, jm))
                popis[druh].append({"soubor": jm, "w": bb[2] - bb[0], "h": bb[3] - bb[1], "xo": bb[0] - O, "yo": bb[1] - O})
    json.dump(popis, open(os.path.join(VRSTVY, "holky.json"), "w"), indent=1)
    print("vrstvy", [(p["w"], p["h"], p["xo"], p["yo"]) for p in popis["za"] + popis["pred"]])


def nahled(yagl, list_png, vystup):
    """auta 0x8C, 0x8B, 0x94, 0x82 v sadach na zastavce ve smerech 1 3 5 7 s vrstvami, zvetseno 3x"""
    import re
    t = open(yagl, encoding="utf-8").read()
    zaz = re.split(r"\n(?=// Record #\d+\n)", t)
    listy = {}
    def sprite(soubor, w, h, x, y):
        if soubor not in listy:
            listy[soubor] = np.array(Image.open(os.path.join(os.path.dirname(yagl), soubor)).convert("RGBA"))
        return Image.fromarray(listy[soubor][y:y + h, x:x + w], "RGBA")
    popis = json.load(open(os.path.join(VRSTVY, "holky.json")))
    radky = []
    for vid in (0x8C, 0x8B, 0x94, 0x82):
        i = [n for n, z in enumerate(zaz) if re.search(rf"^properties<RoadVehicles, 0x{vid:04X}>", z, re.M)][0]
        sady = re.split(r"(?=    sprite_set // )", zaz[i - 2])[1:]
        sada = sady[-1]                               # na zastavce: posledni sada (prazdny na zastavce)
        sp = re.findall(r"\[(-?\d+), (-?\d+), (-?\d+), (-?\d+)\], zin4, c32bpp \| chunked, \"([^\"]+)\", \[(\d+), (\d+)\]", sada)
        bunky = []
        for k in (1, 3, 5, 7):
            w, h, xo, yo, soubor, x, y = sp[k]
            W, H, O = 180, 130, (90, 80)
            img = Image.new("RGBA", (W, H), (150, 160, 150, 255))
            for druh in ("za", None, "pred"):
                if druh is None:
                    img.alpha_composite(sprite(soubor, int(w), int(h), int(x), int(y)), (O[0] + int(xo), O[1] + int(yo)))
                else:
                    p = popis[druh][k]
                    g = Image.open(os.path.join(VRSTVY, p["soubor"])).convert("RGBA")
                    img.alpha_composite(g, (O[0] + p["xo"], O[1] + p["yo"]))
            bunky.append(img)
        radky.append(bunky)
    out = Image.new("RGBA", (180 * 4, 130 * len(radky)))
    for r, bb in enumerate(radky):
        for j, b in enumerate(bb):
            out.paste(b, (j * 180, r * 130))
    out.resize((out.width * 3, out.height * 3), Image.NEAREST).save(vystup)
    print("nahled", vystup)


if __name__ == "__main__":
    if sys.argv[1] == "foto":
        foto()
    elif sys.argv[1] == "vrstvy":
        vrstvy()
    elif sys.argv[1] == "nahled":
        nahled(*sys.argv[2:5])
