# -*- coding: utf-8 -*-
# Divky u otevrenych dveri TAZ 1203, TAZ 1500 busu a Skody 1203 Pajda karavan, kdyz stoji na zastavce (sada spritu
# "na zastavce", dvere otevrene). Hrac 1. 10.: "holka u tech otevrenych dveri, muze byt i vzadu u dveri kufru, klidne
# dve", "nesmi vstoupit do vozovky ke kufru, aby nebyl konflikt s dalsim autem, nesmi za bilou caru silnice, jen
# z boku ke kufru a k prednim dverim", velikost 2x jako na zastavce.
#
#   python3 holky_u_aut.py foto [4|8]        vyfoti divky (postavy/fotka_postavy.py) do foto/, 8 = priblizeni 8x
#   python3 holky_u_aut.py vrstvy            slozi obrazky vrstev 4x i 8x do vrstvy/ a vrstvy/holky.json
#   python3 holky_u_aut.py nahled <yagl> <list.png> <vystup.png> [4|8]   nahled na autech z rozbaleneho GRF dodavek
#
# Priblizeni 8x (2. 10.): kolega dal hre uroven ZoomLevel::In8x (kod zoomu 6 v GRF, v yaglu "zin8"), hrac: "zkusime to
# na dvanacttrojkach na prikladacich studentkach, dame maximum detailu, jsou to malicky obrazky, ktere jen prikladame".
# Fotky 8x maji dvojnasobne rozliseni (24,4 px/m) a vic vzorku. Vrstva 8x je presne dvojnasobek vrstvy 4x (velikost
# i posun od kotvy; hra to u vice urovni jednoho spritu vyzaduje): 8x se sklada na dvojnasobne pozice a oba ramecky
# jsou spolecne, pixely 4x zustavaji jako dosud, jen se ramecek rozsiri, kdyz 8x presahuje.
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
ZIN = {4: dict(px_m=12.2, ram=RAM, samples=64, pripona=""),            # jako dosud (zin4)
       8: dict(px_m=24.4, ram=2 * RAM, samples=1024, pripona="_z8")}   # 8x jen pro nasi hru (zin8), max. detail

DIVKY = {"A": dict(postava="character_people_girl_001", poza="stoji", vyska=1.68),
         "B": dict(postava="college_girl", poza="ruce_dolu", vyska=1.62)}
# smer jizdy (cislo spritu) -> [(divka, a, c, natoceni[, zvednout])]
#   a: jednotky delky hry dopredu od stredu rozvoru (predni naprava +1,9, zadni naraznik -3,5)
#   c: jednotky ven od linky kol na prave strane (bok karoserie +0,35)
#   natoceni jako u postavy/fotka_postavy.py: 0 k jihozapadu, 45 k divakovi, 90 k jihovychodu, 180 k severovychodu
#   zvednout: o kolik px (4x) vys na obrazovce. Hrac 2. 10. (verze 8): "severovychodni smer zvednem holku trochu vejs,
#   protoze ji chybi bota". Chodnik zastavky CZTR je sprite s vlastni krabici bliz k divakovi nez auto, hra ho kresli
#   az po aute i s holkami a prekryje, co z nich lezi na nem: boty. Zmereno ve zkusebni hre (8x): holce B u kufru
#   schova az 8 px (8x), tedy 4 px (4x); holka A u prednich dveri stoji o 0,3 jednotky hloubeji, podle teze hrany
#   by prisla o 10 px (4x); s 11 px ale koukala hlavou nad strechu pristresku CZTR, proto jen 8 px (spicky bot
#   tam muze ztratit, v tom smeru je stejne pod pristreskem). Zvednuti 6 a 8 px.
MISTA = {1: [("A", 1.6, 1.8, 65, 8), ("B", -3.1, 1.5, 0, 6)],
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


def foto_jmeno(divka, natoceni, zin=4):
    return os.path.join(FOTO, f"{divka.lower()}_k{MERITKO:g}_s{natoceni}{ZIN[zin]['pripona']}.png")


def bod(k, a, c):
    """(x, y) chodidel v souradnicich kotvy a jestli je divka za autem"""
    za = not PRAVA_K_DIVAKOVI[k]
    cc = -(ROZCHOD + c) if za else c
    return N[k][0] + a * F[k][0] + cc * NV[k][0], N[k][1] + a * F[k][1] + cc * NV[k][1], za


def foto(zin=4):
    os.makedirs(FOTO, exist_ok=True)
    z = ZIN[zin]
    potreba = sorted({(d, s) for m in MISTA.values() for d, _, _, s, *_ in m})
    for d, s in potreba:
        cil = foto_jmeno(d, s, zin)
        if os.path.exists(cil):
            continue
        p = DIVKY[d]
        env = dict(os.environ, POSTAVA=p["postava"], POZA=p["poza"], VYSKA=str(p["vyska"]), SMER=str(s),
                   MERITKO=str(MERITKO), SAMPLES=str(z["samples"]), RAM=str(z["ram"]), PX_M=str(z["px_m"]), STIN="0")
        subprocess.run([sys.executable, os.path.join(TU, "..", "postavy", "fotka_postavy.py"), cil], env=env, check=True,
                       cwd=os.path.join(TU, "..", "postavy"), stdout=subprocess.DEVNULL)
        print("vyfoceno", cil)


def vrstvy():
    """obrazky vrstev pro smery 0-7: (za autem, pred autem) ve 4x a 8x; prazdne smery 1 x 1 (8x 2 x 2) pruhledny.
    Vrstva 8x je presne dvojnasobek 4x: kazda fotka 8x lezi na dvojnasobku celociselne polohy fotky 4x a ramecek je
    spolecny (sjednoceni obou, v 4x pixelech), takze w8 = 2 w, xo8 = 2 xo."""
    os.makedirs(VRSTVY, exist_ok=True)
    popis = {"meritko": MERITKO, "zin8": {"px_m": ZIN[8]["px_m"], "samples": ZIN[8]["samples"]}, "za": [], "pred": []}
    for k in range(8):
        for druh in ("za", "pred"):
            O, O8 = 200, 400                           # kotva uprostred platna (4x a 8x)
            img = Image.fromarray(np.zeros((400, 400, 4), np.uint8), "RGBA")
            img8 = Image.fromarray(np.zeros((800, 800, 4), np.uint8), "RGBA")
            kusy = []
            for d, a, c, s, *zv in MISTA.get(k, []):
                x, y, za = bod(k, a, c)
                if za != (druh == "za"):
                    continue
                kusy.append((y, Image.open(foto_jmeno(d, s)).convert("RGBA"), x, Image.open(foto_jmeno(d, s, 8)).convert("RGBA"),
                             zv[0] if zv else 0))
            for y, g, x, g8, zv in sorted(kusy, key=lambda t: t[0]):    # vzdalenejsi driv
                assert g8.size == (2 * g.width, 2 * g.height), (g.size, g8.size)
                px, py = round(x - g.width / 2), round(y - g.height / 2) - zv
                img.alpha_composite(g, (O + px, O + py))
                img8.alpha_composite(g8, (O8 + 2 * px, O8 + 2 * py))
            bb, bb8 = img.getbbox(), img8.getbbox()
            jm, jm8 = f"{druh}_{k}.png", f"{druh}_{k}_z8.png"
            if bb is None and bb8 is None:
                Image.new("RGBA", (1, 1), (0, 0, 0, 0)).save(os.path.join(VRSTVY, jm))
                Image.new("RGBA", (2, 2), (0, 0, 0, 0)).save(os.path.join(VRSTVY, jm8))
                popis[druh].append({"soubor": jm, "w": 1, "h": 1, "xo": 0, "yo": 0,
                                    "zin8": {"soubor": jm8, "w": 2, "h": 2, "xo": 0, "yo": 0}})
                continue
            bb = bb or bb8; bb8 = bb8 or bb
            x0, y0 = min(bb[0], bb8[0] // 2), min(bb[1], bb8[1] // 2)
            x1, y1 = max(bb[2], -(-bb8[2] // 2)), max(bb[3], -(-bb8[3] // 2))
            img.crop((x0, y0, x1, y1)).save(os.path.join(VRSTVY, jm))
            img8.crop((2 * x0, 2 * y0, 2 * x1, 2 * y1)).save(os.path.join(VRSTVY, jm8))
            popis[druh].append({"soubor": jm, "w": x1 - x0, "h": y1 - y0, "xo": x0 - O, "yo": y0 - O,
                                "zin8": {"soubor": jm8, "w": 2 * (x1 - x0), "h": 2 * (y1 - y0), "xo": 2 * (x0 - O), "yo": 2 * (y0 - O)}})
    json.dump(popis, open(os.path.join(VRSTVY, "holky.json"), "w"), indent=1)
    print("vrstvy", [(p["w"], p["h"], p["xo"], p["yo"]) for p in popis["za"] + popis["pred"]])


def nahled(yagl, list_png, vystup, zin=4):
    """auta 0x8C, 0x8B, 0x94, 0x82 v sadach na zastavce ve smerech 1 3 5 7 s vrstvami, zvetseno 3x; zin 8: auto
    zdvojene (tak ho hra v 8x kresli, kdyz ma jen 4x) a divky z vrstev 8x, zvetseno 1,5x"""
    import re
    m8 = 2 if zin == 8 else 1
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
            W, H, O = 180 * m8, 130 * m8, (90 * m8, 80 * m8)
            img = Image.new("RGBA", (W, H), (150, 160, 150, 255))
            for druh in ("za", None, "pred"):
                if druh is None:
                    auto = sprite(soubor, int(w), int(h), int(x), int(y))
                    if m8 == 2:
                        auto = auto.resize((auto.width * 2, auto.height * 2), Image.NEAREST)
                    img.alpha_composite(auto, (O[0] + m8 * int(xo), O[1] + m8 * int(yo)))
                else:
                    p = popis[druh][k]
                    if m8 == 2:
                        p = p["zin8"]
                    g = Image.open(os.path.join(VRSTVY, p["soubor"])).convert("RGBA")
                    img.alpha_composite(g, (O[0] + p["xo"], O[1] + p["yo"]))
            bunky.append(img)
        radky.append(bunky)
    out = Image.new("RGBA", (W * 4, H * len(radky)))
    for r, bb in enumerate(radky):
        for j, b in enumerate(bb):
            out.paste(b, (j * W, r * H))
    z = 3 if m8 == 1 else 1.5
    out.resize((int(out.width * z), int(out.height * z)), Image.NEAREST).save(vystup)
    print("nahled", vystup)


if __name__ == "__main__":
    if sys.argv[1] == "foto":
        foto(int(sys.argv[2]) if len(sys.argv) > 2 else 4)
    elif sys.argv[1] == "vrstvy":
        vrstvy()
    elif sys.argv[1] == "nahled":
        nahled(*sys.argv[2:5], int(sys.argv[5]) if len(sys.argv) > 5 else 4)
